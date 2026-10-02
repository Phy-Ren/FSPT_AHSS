"""Exact ordered-simplex cochains in the uploaded draft's cup-i convention.

All phase routines return an INTEGER NUMERATOR with a stated denominator.
No floating-point phase comparison is used. This is a local cochain test
engine, not a group-bordism or AHSS classification package.
"""
from __future__ import annotations
from functools import lru_cache
from itertools import combinations
from typing import Callable, Optional
import random

Face = tuple[int, ...]

@lru_cache(None)
def interval_terms(word: tuple[int,...], degrees: tuple[int,...]):
    k=len(degrees); L=len(word); n=sum(degrees)-L+k
    if n<0 or sorted(set(word))!=list(range(1,k+1)) or any(x==y for x,y in zip(word,word[1:])):
        return ()
    targets=[degrees[j]+1-word.count(j+1) for j in range(k)]
    if min(targets)<0: return ()
    lengths=[0]*L; result=[]
    def recurse(j,remaining):
        if j==L:
            if any(remaining): return
            cuts=[0]
            for length in lengths: cuts.append(cuts[-1]+length)
            faces=[[] for _ in degrees]
            for pos,label in enumerate(word): faces[label-1].extend(range(cuts[pos],cuts[pos+1]+1))
            if any(len(set(f))!=len(f) for f in faces): return
            inner=[word[pos] in word[pos+1:] for pos in range(L)]
            lam=[lengths[pos]+int(inner[pos]) for pos in range(L)]
            exponent=sum(cuts[pos+1] for pos in range(L) if inner[pos])
            exponent+=sum(lam[pos]*lam[jj] for pos in range(L) for jj in range(pos+1,L) if word[pos]>word[jj])
            result.append((tuple(tuple(f) for f in faces),(-1)**(exponent%2)))
            return
        label=word[j]-1
        vals=[remaining[label]] if word[j] not in word[j+1:] else range(remaining[label]+1)
        for length in vals:
            lengths[j]=length; rem=remaining.copy(); rem[label]-=length
            recurse(j+1,rem)
    recurse(0,targets)
    return tuple(result)

class C:
    """A normalized cochain, evaluated lazily on ordered faces."""
    def __init__(self,degree: int,values: Optional[dict]=None,
                 fun: Optional[Callable[[Face],int]]=None,mod: Optional[int]=2):
        self.deg=degree; self.mod=mod; self.values=values; self.fun=fun; self.cache={}
        if values is None and fun is None: self.values={}
        self.known_zero=(self.values=={})
        self.closed=self.known_zero
    def __call__(self,face):
        face=tuple(face)
        if len(face)!=self.deg+1: raise ValueError((self.deg,face))
        if len(set(face))<len(face): return 0
        if face not in self.cache:
            value=self.values.get(face,0) if self.values is not None else self.fun(face)
            self.cache[face]=value%self.mod if self.mod else value
        return self.cache[face]
    def __add__(self,other):
        if self.deg!=other.deg or self.mod!=other.mod: raise ValueError('incompatible cochains')
        if self.known_zero:return other
        if other.known_zero:return self
        out=C(self.deg,fun=lambda f:self(f)+other(f),mod=self.mod);out.closed=self.closed and other.closed;return out
    def __sub__(self,other):
        if self.deg!=other.deg or self.mod!=other.mod: raise ValueError('incompatible cochains')
        if other.known_zero:return self
        out=C(self.deg,fun=lambda f:self(f)-other(f),mod=self.mod);out.closed=self.closed and other.closed;return out
    def scaled(self,k):
        if not k or self.known_zero:return C(self.deg,mod=self.mod)
        out=C(self.deg,fun=lambda f:k*self(f),mod=self.mod);out.closed=self.closed;return out
    def reduce(self,mod):
        if self.known_zero:return C(self.deg,mod=mod)
        out=C(self.deg,fun=self,mod=mod);out.closed=self.closed and self.mod is None;return out
    def lift(self):return self.reduce(None)
    def div(self,k):
        if self.mod is not None: raise ValueError('Divide integers before reduction')
        def evaluate(f):
            value=self(f)
            if value%k: raise ArithmeticError(('nonintegral quotient',value,k,f))
            return value//k
        if self.known_zero:return C(self.deg,mod=None)
        out=C(self.deg,fun=evaluate,mod=None);out.closed=self.closed;return out
    def d(self):
        if self.closed:return C(self.deg+1,mod=self.mod)
        out=C(self.deg+1,fun=lambda f:sum((-1)**j*self(f[:j]+f[j+1:]) for j in range(len(f))),mod=self.mod);out.closed=True;return out

def cup(a:C,b:C,i:int=0,s:C|None=None,twists:tuple[int,int]=(0,0))->C:
    """Signed cup-i, with optional local-system parallel transport.

    twists=(e,f) means inputs in Z_{e*s}, Z_{f*s}; output in
    Z_{(e+f)*s}. Mod-two cups ignore parallel transport.
    """
    if a.mod!=b.mod: raise ValueError('coefficient mismatch')
    degree=a.deg+b.deg-i
    if i<0 or a.known_zero or b.known_zero:return C(degree,mod=a.mod)
    word=tuple(1+j%2 for j in range(i+2))
    terms=interval_terms(word,(a.deg,b.deg))
    sign=(-1)**((i*(a.deg+b.deg)+i*(i-1)//2)%2)
    def evaluate(face):
        total=0
        for faces,cut_sign in terms:
            ff=tuple(face[j] for j in faces[0]); gg=tuple(face[j] for j in faces[1])
            transport=0
            if s is not None and a.mod!=2:
                if twists[0] and ff[0]!=face[0]: transport+=s((face[0],ff[0]))
                if twists[1] and gg[0]!=face[0]: transport+=s((face[0],gg[0]))
            total+=cut_sign*(-1)**(transport%2)*a(ff)*b(gg)
        return sign*total
    out=C(degree,fun=evaluate,mod=a.mod)
    out.closed=(a.closed and b.closed and (i==0 or (a is b and a.mod==2))) and s is None
    return out

def op(word:str,*args:C)->C:
    word=tuple(map(int,word)); degrees=tuple(a.deg for a in args)
    if any(a.mod!=2 for a in args): raise ValueError('word operations here are binary')
    if any(a.known_zero for a in args):return C(sum(degrees)-len(word)+len(args))
    terms=interval_terms(word,degrees)
    def evaluate(face):
        result=0
        for faces,_ in terms:
            value=1
            for a,f in zip(args,faces): value*=a(tuple(face[j] for j in f))
            result^=value
        return result
    return C(sum(degrees)-len(word)+len(args),fun=evaluate)

def sq(a:C,k:int)->C:
    return cup(a,a,a.deg-k)+cup(a,a.d(),a.deg-k+1)

def ds(a:C,s:C,twist:int=1)->C:
    return a.d()-cup(s.lift(),a).scaled(2) if twist%2 else a.d()

def random_cochain(degree:int,dimension:int,mod:int=2)->C:
    return C(degree,values={f:random.randrange(mod) for f in combinations(range(dimension+1),degree+1)},mod=mod)

def primitive(z:C)->C:
    """Simplex contraction. Only used to GENERATE test data, not define a natural operation."""
    return C(z.deg-1,fun=lambda f:0 if 0 in f else z((0,)+tuple(f)),mod=z.mod)

def zeta2(a:C,b:C)->C:
    return op('12313'+''.join(str(4 if j%2==0 else 3) for j in range(b.deg)),a,a,b,b)

def zeta1(a:C,b:C)->C:
    return op('12314'+''.join(str(3 if j%2==0 else 4) for j in range(b.deg-1)),a,a,b,b)

def adem(a:C)->C:
    if a.deg==2: words=['1213243','1213431','1232141','1234321']
    elif a.deg==3: words=['1213243142','1213431412','1232431421','1234314212']
    elif a.deg==4:
        import json
        from pathlib import Path
        words=json.loads(Path(__file__).with_name('x4_words.json').read_text())
    else: raise ValueError('Only degrees 2,3,4 are implemented')
    out=C(a.deg+3)
    for word in words: out=out+op(word,a,a,a,a)
    if a.deg==3:
        t=a.lift().d().div(2).reduce(2)
        out=out+cup(t,t,2)
    return out

def mc_phase4(b:C,c:C,w:C,s:C)->C:
    """Four times the draft's Majorana phase. Requires db=0; c may be off shell."""
    r=b.deg; beta=b.lift().d().div(2); t=beta.reduce(2)
    q=cup(b,b,r-2); wb=cup(w,b); st=cup(s,t)
    carry=(beta+t.lift()).div(2).reduce(2)
    half=sq(c,2)+cup(w,c)+zeta2(w,b)+adem(b)
    half=half+cup(q,wb,r+1)+cup(q,st,r+1)+cup(wb,st,r+1)
    half=half+zeta1(s,t)+cup(cup(w,s,1),t)+cup(s,q)+cup(cup(s,s),carry)
    quarter=cup(w.lift(),beta)+cup(beta,beta,r-1)
    return half.lift().scaled(2)+quarter

def parity(N:C,b:C,w:C,s:C)->C:
    """Native SHORT p=1 and native p=2 parity equations of the uploaded draft."""
    p=N.deg; a=N.reduce(2); h=C(p,fun=lambda f:N(f)//2)
    t=cup(a,a,p-1); W=w+cup(s,s); bp=b+cup(s,h); q=cup(a,a,p-2); v=cup(W,W,1)
    out=sq(bp,2)+cup(w,bp)+cup(s,sq(bp,1))
    out=out+zeta2(W,a)+cup(v+cup(s,W),h)+cup(cup(v,s,1)+cup(s,cup(s,W,1)),a)
    if p==1: return out
    if p==2:
        out=out+zeta2(a,a)+cup(q,cup(W,a),3)+cup(h,h.d())+cup(t,cup(s,a),1)
        out=out+cup(s,cup(q,cup(W,a),4)+cup(cup(a,s,1),a)+cup(a,t,1)+q)
        return out
    raise ValueError('Only p=1,2 are implemented')

def background_data(w:C,s:C):
    W=w+cup(s,s); vz=ds(W.lift(),s).div(2); alpha=vz.reduce(2)
    hv=(vz-alpha.lift()).div(2).reduce(2)
    pontryagin=cup(W.lift(),W.lift(),s=s,twists=(1,1))+cup(W.lift(),ds(W.lift(),s),1,s=s,twists=(1,1))
    return W,vz,alpha,hv,pontryagin

def cartan3(alpha:C,m:C)->C:
    p=m.deg
    if p==1: swapped=zeta1(m,alpha)
    elif p==2: swapped=zeta2(m,alpha)
    else: raise ValueError('Only degrees 1,2 are implemented')
    u=cup(alpha,m); v=cup(m,alpha)
    return (swapped+sq(cup(alpha,m,1),2)+cup(u,v,p+2)
            +cup(sq(alpha,2),m,1)+cup(alpha,sq(m,2),1)+cup(sq(alpha,1),sq(m,1),1))

def cartan_carry(N:C,w:C,s:C):
    W,vz,alpha,hv,pontryagin=background_data(w,s)
    a=N.reduce(2); h=(N-a.lift()).div(2).reduce(2)
    E=cup(hv,sq(a,1))+cup(cup(s,alpha),h)+cup(cup(s,cup(alpha,s,1)),a)
    return cartan3(alpha,a)+E

def residual_data(N:C,b:C,c:C,w:C,s:C):
    """Full-twist fractional seed and its remaining binary boundary.

    Returns (seed_numerator_over_16, residual_R, auxiliary_dict).
    This intermediate seed has the opposite Pontryagin-line sign; the final
    entry point uses positive_residual_data. No linear solve is performed here.
    """
    p=N.deg; a=N.reduce(2); h=(N-a.lift()).div(2).reduce(2)
    bp=b+cup(s,h); W,vz,alpha,hv,pontryagin=background_data(w,s)
    KN=cup(N,N,p-2,s=s,twists=(1,1))
    L=KN+cup(W.lift(),N,s=s,twists=(1,1))
    B=(bp.lift().d()-L).div(2); U=B.reduce(2); Z=B.d()
    LB=cup(B,B,p)+cup(B,Z,p+1)
    Cbin=cartan_carry(N,w,s)
    Kpoly=cup(pontryagin,N,s=s,twists=(0,1))+cup(W.lift(),KN,s=s,twists=(1,0)).scaled(2)
    DN=(cup(cup(W.lift(),vz,s=s,twists=(1,1))+cup(vz,vz,1,s=s,twists=(1,1)),N,s=s,twists=(0,1))
        +cup(vz,KN,s=s,twists=(1,0)))
    numerator=cup(Z,Z,p+1)+cup(w.lift(),Z)-DN-ds(Cbin.lift(),s)
    R2=numerator.div(2).reduce(2)
    v0=w.lift().d().div(2).reduce(2)
    Q=parity(N,b,w,s)
    R=sq(Q,2)+cup(w,Q)+sq(U,3)+cup(s,sq(U,2))+cup(v0+cup(s,w),U)+R2
    seed=(sq(c,2)+cup(w,c)).lift().scaled(8)+(LB+cup(w.lift(),B)).scaled(4)-Kpoly-Cbin.lift().scaled(4)
    return seed,R,{'B':B,'U':U,'Z':Z,'Q':Q,'KN':KN,'L':L,'DN':DN,'C':Cbin,'R2':R2,'W':W,'v':vz,'P':pontryagin}

def random_data(p:int,n:int,even:bool=False):
    s=random_cochain(0,n).d(); w=random_cochain(1,n).d()
    N=ds(random_cochain(p-1,n,16).lift(),s)
    if even:N=N.scaled(2)
    a=N.reduce(2); A=sq(a,2)+cup(w,a)+cup(s,sq(a,1))
    b=primitive(A)+random_cochain(p,n).d()
    Q=parity(N,b,w,s)
    c=primitive(Q)+random_cochain(p+1,n).d()
    return N,b,c,w,s

def mc_half(b:C,w:C,s:C)->C:
    """The binary half-valued bracket of the MC phase, excluding its c terms."""
    r=b.deg; beta=b.lift().d().div(2); t=beta.reduce(2)
    q=cup(b,b,r-2); wb=cup(w,b); st=cup(s,t)
    carry=(beta+t.lift()).div(2).reduce(2)
    return (zeta2(w,b)+adem(b)+cup(q,wb,r+1)+cup(q,st,r+1)+cup(wb,st,r+1)
            +zeta1(s,t)+cup(cup(w,s,1),t)+cup(s,q)+cup(cup(s,s),carry))

def pure_parity(N:C,w:C,s:C)->C:
    h=(N-N.reduce(2).lift()).div(2).reduce(2)
    # Set native b=s*h, so b'=0, even when its first-stage equation is not obeyed.
    return parity(N,cup(s,h),w,s)

def pure_residual(N:C,w:C,s:C):
    """Pure-base residual after a formal unrestricted-b transgression.
    Returns R_base, and data sufficient to reconstruct the polarization.
    """
    p=N.deg;a=N.reduce(2);a.closed=True;W,vz,alpha,hv,PW=background_data(w,s)
    A=sq(a,2)+cup(W,a)
    KN=cup(N,N,p-2,s=s,twists=(1,1))
    L=KN+cup(W.lift(),N,s=s,twists=(1,1))
    K=(A.lift()-L).div(2).reduce(2)
    Z=cup(vz,N,s=s,twists=(1,1)).scaled(-1);D=Z.reduce(2)
    Cbin=cartan_carry(N,w,s)
    DN=(cup(cup(W.lift(),vz,s=s,twists=(1,1))+cup(vz,vz,1,s=s,twists=(1,1)),N,s=s,twists=(0,1))
        +cup(vz,KN,s=s,twists=(1,0)))
    R2=(cup(Z,Z,p+1)+cup(w.lift(),Z)-DN-ds(Cbin.lift(),s)).div(2).reduce(2)
    zeta=pure_parity(N,w,s);F=sq(A,2)+cup(w,A)+cup(s,sq(A,1));H=sq(A,1)
    v0=w.lift().d().div(2).reduce(2);ell=v0+cup(s,w)
    RN=(cup(zeta,zeta,p+1)+cup(F,zeta,p+2)+cup(w,zeta)
        +cup(K,K,p-1)+cup(H,K,p)+cup(K,D,p)
        +cup(s,cup(K,K,p)+cup(H,K,p+1)+cup(K,D,p+1))
        +cup(ell,K)+R2)
    return RN+mc_half(A,w,s),{'A':A,'K':K,'D':D,'zeta':zeta,'RN':RN,'R2':R2,'DN':DN.reduce(2),'D1':cup(cup(W.lift(),vz,s=s,twists=(1,1))+cup(vz,vz,1,s=s,twists=(1,1)),N,s=s,twists=(0,1)).reduce(2),'D2':cup(vz,KN,s=s,twists=(1,0)).reduce(2)}

def offshell_rb(b:C,w:C,s:C)->C:
    P=sq(b,2)+cup(s,sq(b,1))+cup(w,b)
    V=sq(b,1);ell=w.lift().d().div(2).reduce(2)+cup(s,w)
    return sq(P,2)+cup(w,P)+sq(V,3)+cup(s,sq(V,2))+cup(ell,V)

def prism_transgression(b:C,w:C,s:C)->C:
    """Explicit background-preserving prism primitive of R_b+J(db).

    Vertices of the ordered prism are encoded as (2*base_vertex+height).
    No cocycle condition is imposed on b. This does not choose a primitive
    of the remaining pure (N,w,s) residual.
    """
    def pull(a:C)->C:
        return C(a.deg,fun=lambda f:a(tuple(v//2 for v in f)),mod=a.mod)
    wI=pull(w);sI=pull(s)
    bI=C(b.deg,fun=lambda f:(f[0]%2)*b(tuple(v//2 for v in f)))
    psi=offshell_rb(bI,wI,sI)+mc_half(bI.d(),wI,sI)
    def evaluate(face):
        return sum(psi(tuple(2*v for v in face[:j+1])+tuple(2*v+1 for v in face[j:]))
                   for j in range(len(face)))
    return C(b.deg+3,fun=evaluate)

def positive_residual_data(N:C,b:C,c:C,w:C,s:C):
    seed,R,aux=residual_data(N,b,c,w,s)
    Kpoly=cup(aux['P'],N,s=s,twists=(0,1))+cup(aux['W'].lift(),aux['KN'],s=s,twists=(1,0)).scaled(2)
    return seed+Kpoly.scaled(2),R+aux['DN'].reduce(2),aux

def pure_target(N:C,w:C,s:C):
    R,aux=pure_residual(N,w,s)
    ell=w.lift().d().div(2).reduce(2)+cup(s,w)
    return R+aux['DN']+cup(aux['A'],ell)

def polarization(N:C,b:C,w:C,s:C):
    p=N.deg;h=(N-N.reduce(2).lift()).div(2).reduce(2);bp=b+cup(s,h)
    pure,aux=pure_residual(N,w,s)
    P=sq(bp,2)+cup(s,sq(bp,1))+cup(w,bp);V=sq(bp,1)
    return (cup(P,aux['zeta'],p+2)+cup(V,aux['K'],p)
            +cup(s,cup(V,aux['K'],p+1)))
