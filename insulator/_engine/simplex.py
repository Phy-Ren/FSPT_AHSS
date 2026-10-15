"""Adapted from the frozen U1f consolidated v0.7 formula archive."""
from itertools import combinations, combinations_with_replacement
from fractions import Fraction as F
from functools import lru_cache
from .cochains import interval_cuts

@lru_cache(maxsize=256)
def _faces(N, degree):
    return tuple(combinations(range(N + 1), degree + 1))

@lru_cache(maxsize=512)
def _cup_plan(N, p, q, i):
    cuts = interval_cuts(p, q, i)
    return tuple((f, tuple((tuple(f[j] for j in left),
                           tuple(f[j] for j in right), sign)
                          for left, right, sign in cuts))
                 for f in _faces(N, p + q - i))

@lru_cache(maxsize=256)
def _boundary_plan(N, p):
    return tuple((f, f[1:], tuple(((-1)**j, f[:j]+f[j+1:])
                                  for j in range(1, len(f))))
                 for f in _faces(N, p+1))

class C:
    def __init__(self,N,p,v,tw=None):
        self.N=N;self.p=p;self.v={f:(x.numerator if type(x) is F and x.denominator==1 else x) for f,x in v.items()};self.tw=tuple(tw or [0]*(N+1))
    def __call__(self,f): return self.v.get(tuple(f),0)
    def d(self):
        out={};values=self.v;tw=self.tw
        for f,first,rest in _boundary_plan(self.N,self.p):
            value=(-1)**(tw[f[0]]+tw[f[1]])*values.get(first,0)
            for sign,face in rest:value+=sign*values.get(face,0)
            out[f]=value
        return C(self.N,self.p+1,out,tw)
    def sc(self,a): return C(self.N,self.p,{f:a*v for f,v in self.v.items()},self.tw)
    def __add__(self,b):
        assert self.N==b.N and self.p==b.p
        return C(self.N,self.p,{f:self(f)+b(f) for f in combinations(range(self.N+1),self.p+1)},self.tw)
    def __sub__(self,b): return self+b.sc(-1)
    def mod(self,m): return C(self.N,self.p,{f:v%m for f,v in self.v.items()},self.tw)
    def ret(self,tw): return C(self.N,self.p,self.v,tw)
    def cup(self,b,i=0,binary=False):
        p=self.p;q=b.p;D=p+q-i;out={}
        av=self.v;bv=b.v;at=self.tw;bt=b.tw
        for f,cuts in _cup_plan(self.N,p,q,i):
            val=0
            for ff,gg,sg in cuts:
                left=av.get(ff,0)
                if not left: continue
                right=bv.get(gg,0)
                if not right: continue
                sign=1 if binary else sg*(-1)**(at[f[0]]+at[ff[0]]+bt[f[0]]+bt[gg[0]])
                val+=sign*left*right
            out[f]=val%2 if binary else val
        return C(self.N,D,out,[a^b for a,b in zip(at,bt)])
    def sq(self,k): return (self.cup(self,self.p-k,True)+self.cup(self.d(),self.p-k+1,True)).mod(2)
    def pw(self,b): return C(self.N,self.p,{f:self(f)*b(f) for f in self.v},self.tw)
    def maxabs(self): return max([abs(v) for v in self.v.values()]+[0])

def rand(N,p,tw=None,rng=None,lo=-3,hi=4):
    import random
    rng=rng or random
    return C(N,p,{f:rng.randrange(lo,hi) for f in combinations(range(N+1),p+1)},tw)

def char(N,tw): return C(N,1,{(i,j):tw[i]^tw[j] for i,j in combinations(range(N+1),2)})

def primitive(q):
    p=q.p-1
    return C(q.N,p,{f:(0 if 0 in f else (-1)**(q.tw[0]+q.tw[f[0]])*q((0,)+f)) for f in combinations(range(q.N+1),p+1)},q.tw)

def halves(x): return C(x.N,x.p,{f:(v//2)%2 for f,v in x.v.items()})

def bin0(x): return x.mod(2).ret([0]*(x.N+1))

@lru_cache(None)
def wordcuts(w,degrees):
    N=sum(degrees)-len(w)+len(degrees); L=len(w);out=[]
    for mids in combinations_with_replacement(range(N+1),L-1):
        cuts=(0,)+mids+(N,);S=[[] for _ in degrees]
        for j,label in enumerate(w):S[label-1].extend(range(cuts[j],cuts[j+1]+1))
        if any(len(S[i])!=degrees[i]+1 or len(set(S[i]))!=len(S[i]) for i in range(len(S))):continue
        out.append(tuple(tuple(s) for s in S))
    return tuple(out)

def word(w,*args):
    N=args[0].N;D=sum(a.p for a in args)-len(w)+len(args);cuts=wordcuts(tuple(w),tuple(a.p for a in args));v={}
    for f in combinations(range(N+1),D+1):
        total=0
        for faces in cuts:
            term=1
            for a,ff in zip(args,faces):term*=a(tuple(f[i] for i in ff))
            total+=term
        v[f]=total%2
    return C(N,D,v)

def cartan31(z,x):
    h=z.cup(x,1,True);u=x.cup(z,0,True)
    return (word((1,2,3,1,4,3,4),x,x,z,z)+h.sq(2)+u.cup(h.d(),3,True)+x.sq(1).cup(z.sq(1),1,True)+x.cup(z.sq(2),1,True)).mod(2)

def H31(B,k,s):
    z=bin0(B);x=bin0(k);t=char(B.N,B.tw);ss=bin0(s)
    return (cartan31(z,x)+halves(B).cup(x.sq(1),0,True)+t.cup(z,0,True).cup(halves(k),0,True)+t.cup(z.cup(ss,1,True),0,True).cup(x,0,True)).mod(2)

def background(a,s):
    A=a-bin0(s).cup(bin0(s)).ret(a.tw).sc(F(1,2))
    return A,A.d()

def Fopen(n,m):
    p=n.p
    return (bin0(n).cup(bin0(m),p-1,True)+bin0(n).d().cup(bin0(m),p,True)).sc(F(1,2))

def cartan12(r,L):
    h=L.cup(r,1,True);u=r.cup(L,0,True)
    return (word((1,2,3,1,3,4),L,L,r,r)+h.sq(2)+u.cup(h.d(),2,True)+r.sq(1).cup(L.sq(1),1,True)+r.cup(L.sq(2),1,True)).mod(2)


def cartan32(z,x):
    h=x.cup(z,1,True);u=z.cup(x,0,True)
    return (word((1,2,3,1,3,4,3,4),x,x,z,z)+h.sq(2)+u.cup(h.d(),4,True)+z.cup(x.sq(2),1,True)+x.cup(z.sq(2),1,True)+z.sq(1).cup(x.sq(1),1,True)).mod(2)

def H32(B,k,s):
    z=bin0(B);x=bin0(k);t=char(B.N,B.tw);ss=bin0(s)
    return (cartan32(z,x)+halves(B).cup(x.sq(1),0,True)+t.cup(z,0,True).cup(halves(k),0,True)+t.cup(z.cup(ss,1,True),0,True).cup(x,0,True)).mod(2)

def Jr6(k,r,s):
    x=bin0(k);rr=bin0(r);ss=bin0(s);L=k.cup(k);ell=bin0(L)
    K=(word((1,2,3,1,3,4,3),x,x,x,x)+halves(k).cup(x.sq(1),0,True)+ss.cup(x,0,True).cup(halves(k),0,True)+ss.cup(x.cup(ss,1,True),0,True).cup(x,0,True)).mod(2)
    re=(rr.cup(ss,1,True).cup(rr,0,True)+ss.sq(1).cup(rr,1,True)).cup(ell,0,True)
    return (word((1,2,3,1,4,3,4,3),rr,rr,ell,ell)+rr.sq(1).cup(halves(L),0,True)+rr.cup(K,0,True)+re).mod(2)

def Q4d(a,k,s,r):
    A,B=background(a,s)
    return (B.cup(k)+r.cup(k.cup(k))).sc(-1)

def O4d(a,k,n,s,r,lam=F(1,6)):
    A,B=background(a,s);L=k.cup(k);z=bin0(B);x=bin0(k);rr=bin0(r);ss=bin0(s);tt=char(a.N,a.tw)
    T=z.cup(x,0,True);V=rr.cup(x.cup(x,0,True),0,True)
    eta=tt.cup(ss,0,True)
    nat=A.cup(n)+(bin0(n).sq(2)+eta.cup(bin0(n),0,True)).sc(F(1,2))
    nat=nat+(A.cup(A)+A.cup(B,1)).cup(k).sc(F(1,2))-A.cup(L.ret(r.tw)).sc(F(1,2))+rr.cup(rr).cup(L).sc(F(1,4))
    nat=nat+(H32(B,k,s)+Jr6(k,r,s)+T.cup(V,4,True)).sc(F(1,2))+k.cup(k).cup(k).sc(lam)
    R=s.ret(a.tw).cup(n).sc(F(1,4)).ret(s.tw)
    return nat.ret(s.tw)-R.d()

def O4d_display(a,k,n,s,r,lambda_cubic=F(1,6)):
    """Displayed parent formula, independently arranged from O4d's rephasing proof."""
    A,B=background(a,s);Q=Q4d(a,k,s,r);x=bin0(k);rr=bin0(r);L=k.cup(k)
    T=bin0(B).cup(x,0,True);V=rr.cup(x.cup(x,0,True),0,True)
    out=a.cup(n)+bin0(n).sq(2).sc(F(1,2))+(A.cup(A)+A.cup(B,1)).cup(k).sc(F(1,2))
    out=out-A.cup(L.ret(r.tw)).sc(F(1,2))+rr.cup(rr).cup(L).sc(F(1,4))
    out=out+(H32(B,k,s)+Jr6(k,r,s)+T.cup(V,4,True)).sc(F(1,2))+s.ret(A.tw).cup(Q).sc(F(1,4))
    return (out+k.cup(k).cup(k).sc(lambda_cubic)).ret(s.tw)

def E4d_integer(k,kp,r):
    """The adopted integer charge polarizer paired with the fixed epsilon=0 product."""
    return k.cup(kp).ret(r.tw)+r.cup(k.cup(kp,1))

