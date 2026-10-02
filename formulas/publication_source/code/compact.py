"""Compact Majorana stacking in the fixed manuscript obstruction coordinate.
All phases are represented by their integer numerator over eight.
The formula contains only signed higher cups, Bocksteins, carries and
explicit May--Steenrod words. No primitive solver or phase table is called.
"""
from cochains import *

def carry(a):
    """The manuscript's integer second carry beta^+a; no old formula is used."""
    P = a.beta()
    return C(a.N, a.d+1, {f:(v+v%2)//2 for f,v in P.v.items()}, None)

INTRINSIC_TERMS = [['12131432412', 1],
 ['12343213431', 1],
 ['23412342324', 1],
 ['12123434123', 2],
 ['12131412324', 2],
 ['12134131234', 2],
 ['12312412423', 2],
 ['12314324123', 2],
 ['12314342413', 2],
 ['13242412314', 2],
 ['13412321341', 2],
 ['13412321413', 2],
 ['13413142134', 2],
 ['13432412314', 2],
 ['31214124324', 2],
 ['12413432312', 3],
 ['cup', [2, [2, 'a', 'b'], 'b']],
 ['cup', [2, [2, 'b', 'b'], [3, 'a', 'b']]],
 ['cup', [4, [2, 'a', 'b'], [1, 'b', 'b']]],
 ['cup', [2, [3, 'a', 'b'], [2, 'b', 'b']]],
 ['cup', [3, 'b', [2, 'a', [2, 'a', 'b']]]],
 ['cup', [3, [2, 'b', 'b'], [2, 'a', 'a']]],
 ['cup', [2, [3, 'a', 'b'], [2, 'b', 'a']]],
 ['cup', [4, [2, 'a', 'b'], [1, 'a', 'a']]],
 ['cup', [2, [3, 'a', 'b'], [2, 'a', 'a']]],
 ['cup', [2, [2, 'a', 'a'], [3, 'a', 'b']]],
 ['quarticN', '12131432412', ['b', 'a', 'a', 'N']],
 ['quarticN', '12131432412', ['N', 'a', 'a', 'b']],
 ['quarticN', '12131432412', ['N', 'b', 'b', 'a']],
 ['quarticN', '12134341321', ['N', 'b', 'b', 'a']],
 ['ternary', '1212312', ['N', 'b', 'u']],
 ['ternary', '12313123', ['b', 'a', 't']],
 ['ternary', '12131232', ['r', 'b', 'b']],
 ['ternary', '123131212', ['B', 'a', 'N']],
 ['ternary', '123131212', ['AN', 'b', 'a']]]

def desuspend_word(w,arity):
    if len(set(w[-arity:])) != arity:return None
    out=w[:-(arity-1)]
    return out if set(out)==set(w) else None

def intrinsic(a,b):
    """z^0_{p+2}, p=2,3; p=2 is literal cone-last desuspension."""
    p=a.d
    if p not in (2,3) or b.d!=p:raise ValueError('Expected degree-two or degree-three cocycles')
    shift=3-p;N=a+b
    f={'a':a,'b':b,'N':N,'u':cup(a,b,p),'t':cup(a,b,p-1),
       'tb':cup(b,a,p-1),'r':a.beta().red(),'rb':b.beta().red(),
       'A':cup(a,a,p-2),'B':cup(b,b,p-2),'AN':cup(N,N,p-2)}
    def cexpr(e):
        if isinstance(e,str):return f[e]
        i,l,r=e;return cup(cexpr(l),cexpr(r),i-shift)
    out=C(a.N,p+2,{})
    for term in INTRINSIC_TERMS:
        if term[0]=='cup':out=out+cexpr(term[1]);continue
        if term[0] in ('ternary','quarticN'):
            _,wd,args=term;xs=[f[x] for x in args]
        else:
            wd,split=term;xs=[a]*split+[b]*(4-split)
        for _ in range(shift):
            wd=desuspend_word(wd,len(xs))
            if wd is None:break
        if wd is not None:out=out+word(wd,*xs)
    return out

def binary_polynomial(a,b,w,s):
    """The complete z_{p+2}: the displayed intrinsic and background blocks."""
    p=a.d;N=a+b;u=cup(a,b,p);t=cup(a,b,p-1);m=t+s*u
    r=a.beta().red();rp=b.beta().red();A=cup(a,a,p-2);B=cup(b,b,p-2)
    dq=(carry(N)-carry(a)-carry(b)).red()
    z=(intrinsic(a,b)+cup(w*N,m,p+1)+cup(t.di(),w*N,p+2)
       +cup(B,w*a,p+2)+cup(B+w*b,s*r,p+2)+cup(w,s,1)*u
       +cup(t,s*(r+rp),p+1)+cup(cup(N,N,p-2),s*u,p+1)+cup(t,s*u,p)
       +s*(m+cup(r,rp,p+1)+cup(u,u,p-1)+cup(r+rp,s*u,p+1)+cup(s*u,u,p)+dq))
    return z

def fractional_bracket(a,b,w):
    p=a.d;P=a.beta();Q=b.beta();R=(a+b).beta();u=cup(a,b,p).lift()
    return (cup(P,Q,p,integer=True).scale((-1)**(p+1))
       +cup(P+Q,u,p-1,integer=True).scale((-1)**p)
       -cup(u,R,p-1,integer=True)+cup(u,u,p-2,integer=True)-cup(w,u,integer=True))

def majorana_stable(a,b,w,s):
    if (a.d,b.d,w.d,s.d) not in ((3,3,2,1),(2,2,2,1)):
        raise ValueError('Expected degrees (3,3,2,1) or (2,2,2,1)')
    if len({x.N for x in (a,b,w,s)})!=1 or any(x.mod!=2 for x in (a,b,w,s)):
        raise ValueError('Inputs must be binary cochains on the same simplex')
    return phase((4,binary_polynomial(a,b,w,s)),(2,fractional_bracket(a,b,w)))

def majorana(a,b,w,s):
    """Eight times the compact E^gamma_5, including both backgrounds."""
    if a.d!=3 or b.d!=3:raise ValueError('4+1D requires degree-three Majorana inputs')
    return majorana_stable(a,b,w,s)
