"""p+ip-to-complex-fermion stacking, binary native manuscript coordinates.
Explicit products in degrees p=1,2. The existing Majorana files are unchanged.
The functions ending in _compact are the final displayed representatives;
seed functions are retained only to reproduce the termwise derivation.
"""
from cochains import C, cup, word, faces

def zero(x,d=None):return C(x.N,x.d if d is None else d,{})
def sq(x,j):return cup(x,x,x.d-j)+cup(x,x.di(),x.d-j+1)
def q(a):return cup(a,a,a.d-2)
def r(a):return cup(a,a,a.d-1)
def zeta(W,a):return word('123134' if a.d==1 else '1231343',W,W,a,a)
def xpsi(a):return zero(a,a.d+3) if a.d==1 else zeta(a,a)
def intrinsic(a,b):
    if a.d==1:return cup(a,a*b,1)*b
    return (word('12413423',a,a,a,b)+word('12314132',a,a,b,b)
       +word('12314324',a,a,b,b)+word('12341321',a,a,b,b)
       +word('12132413',a,b,b,b)+word('12324214',a,b,b,b))
def pure_source(a,h,W,s,short=True):
    p=a.d;R=r(a);Q=q(a);v=cup(W,W,1)
    out=zeta(W,a)+(v+s*W)*h+(cup(v,s,1)+s*cup(s,W,1))*a
    if p==1 and short:return out
    out=out+xpsi(a)+cup(Q,W*a,p+1)+s*cup(Q,W*a,p+2)
    out=out+sq(h,3)+cup(R,s*a,p-1)+s*(cup(a,R,p-1)+Q)
    if p==2:out=out+s*cup(a,s,1)*a
    return out

def source(a,h,c,W,s,short=True):
    return sq(c,2)+s*sq(c,1)+(W+s*s)*c+pure_source(a,h,W,s,short)

def lower(a,h,c,b,k,e):
    p=a.d
    return a+b,h+k+cup(a,b,p),c+e+cup(a,b,p-1)

def upper_product(a,c,b,e,s):
    p=a.d;t=cup(a,b,p-1)
    return (cup(c,e,p)+cup(c.di(),e,p+1)+cup(c+e,t,p)
      +s*(cup(c,e,p+1)+cup(c.di(),e,p+2)+cup(c+e,t,p+1)))

def residual(a,h,b,k,W,s,short=True):
    p=a.d;t=cup(a,b,p-1);u=cup(a,b,p);F=q(a)+W*a;G=q(b)+W*b
    return (sq(t,2)+s*sq(t,1)+(W+s*s)*t+cup(F,G,p+1)+s*cup(F,G,p+2)
      +cup(F+G,t,p)+cup(t,F+G,p)
      +s*(cup(F+G,t,p+1)+cup(t,F+G,p+1))
      +pure_source(a+b,h+k+u,W,s,short)+pure_source(a,h,W,s,short)+pure_source(b,k,W,s,short))

def unitary_seed(a,h,b,k,W):
    p=a.d;t=cup(a,b,p-1);u=cup(a,b,p);R=r(a)
    bg=cup(W*(a+b),t,p+1)+cup(q(b),W*a,p+2)+cup(t.di(),W*(a+b),p+2)
    hh=cup(h,k,p-2)+cup(R,k,p-1)+cup(h+k,u,p-2)
    vb=cup(h,b,p-2)+cup(a,k,p-2)
    return intrinsic(a,b)+bg+hh+vb

def free_primitive(N,d,F,offset):
    from boolean_polynomials import free_cocycle
    c,end=free_cocycle(N,d,offset)
    for f in faces(N,d):
        if f[0]:c.v[f]=c[f]+F[(0,)+f]
    return c,end

def free_data(p,N=None,s_on=True,W_on=True,upper=True):
    from boolean_polynomials import free_cocycle
    if N is None:N=p+3
    s,j=free_cocycle(N,1,0)
    if not s_on:s=zero(s);j=0
    W,j=free_cocycle(N,2,j)
    if not W_on:W=zero(W);j= len([f for f in faces(N,1) if f[0]==0]) if s_on else 0
    a,j=free_cocycle(N,p,j);b,j=free_cocycle(N,p,j)
    h,j=free_primitive(N,p,r(a)+s*a,j)
    k,j=free_primitive(N,p,r(b)+s*b,j)
    if upper:
        c,j=free_primitive(N,p+1,q(a)+W*a,j)
        e,j=free_primitive(N,p+1,q(b)+W*b,j)
    else:c=zero(a,p+1);e=zero(a,p+1)
    return a,h,c,b,k,e,W,s,j

def anti_carry_seed(a,h,b,k,s):
    p=a.d;N=a+b;u=cup(a,b,p)
    return (cup(s*a,k,p-1)+cup(s*N,u,p-1)+cup(s*a,r(b),p)+cup(u.di(),s*N,p))

def remaining_anti(a,b,s):
    p=a.d;t=cup(a,b,p-1);u=cup(a,b,p);N=a+b
    zz=zero(a,p+3)
    if p==2:zz=s*(cup(a,s,1)*b+cup(b,s,1)*a)
    dr=cup(N,r(N),p-1)+cup(a,r(a),p-1)+cup(b,r(b),p-1)
    return (cup(s*a,s*b,p-1)+cup(s*a,b,p-2)+cup(a,s*b,p-2)+zz
       +s*(dr+t.di()+sq(t,1)+cup(q(a),q(b),p+2)+cup(q(a)+q(b),t,p+1)+cup(t,q(a)+q(b),p+1))
       +s*s*t)

def cup_carry(a,b):
    """Parity of (signed cup_{p-1}(a~,b~) - lift(a cup_{p-1}b))/2.
    Explicit native binary form for p=1,2.
    """
    p=a.d
    if p==1:return zero(a,p+1)
    if p!=2:raise ValueError('Only p=1,2')
    return C(a.N,3,{f:(a[(f[0],f[2],f[3])]*b[(f[0],f[1],f[2])]+1)*a[(f[0],f[1],f[3])]*b[(f[1],f[2],f[3])] for f in faces(a.N,3)})

def anti_final(a,b,s):
    p=a.d;t=cup(a,b,p-1);u=cup(a,b,p);N=a+b
    return (cup(a,s*b,p-1)+s*(t+s*u+cup(a,r(b)+s*b,p)+cup_carry(a,b))
      +cup(s*u,N,p-1)+cup(cup(N,s,1),u,p-2))

def endpoint(a,s):return cup(r(a),s,1)*a

def pure_product(a,h,b,k,W,s,short=True):
    p=a.d
    out=unitary_seed(a,h,b,k,W)+anti_carry_seed(a,h,b,k,s)+anti_final(a,b,s)
    if p==1 and short:out=out+endpoint(a+b,s)+endpoint(a,s)+endpoint(b,s)
    return out

def product(a,h,c,b,k,e,W,s,short=True):
    return upper_product(a,c,b,e,s)+pure_product(a,h,b,k,W,s,short)

def normalized_cup_carry(a,b):
    """Suspension-normalized signed-cup carry, explicitly two May words in p=2."""
    if a.d==1:return zero(a,2)
    return (word('123142341',a,b,a,b)+word('123412143',b,b,a,b))

def pure_product_compact(a,h,b,k,W,s,short=True):
    """Stable, normalized native pure p+ip-to-fermion correction, p=1,2.
    All divisions have disappeared from this binary expression.
    """
    p=a.d;N=a+b;t=cup(a,b,p-1);u=cup(a,b,p)
    out=(intrinsic(a,b)+cup(W*N,t,p+1)+cup(q(b),W*a,p+2)+cup(t.di(),W*N,p+2)
      +cup(h+a,k+b,p-2)+cup(h.di(),k,p-1)+cup(h+k,u,p-2)
      +cup(s*a,r(b),p)+cup(a,s*b,p-1)+cup(u,s*N,p-1)
      +s*(s*u+cup(a,k.di(),p)+cup(u,N,p-1)+normalized_cup_carry(a,b)))
    if p==1 and short:out=out+endpoint(N,s)+endpoint(a,s)+endpoint(b,s)
    return out

def product_compact(a,h,c,b,k,e,W,s,short=True):
    return upper_product(a,c,b,e,s)+pure_product_compact(a,h,b,k,W,s,short)
