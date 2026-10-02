"""Binary coherence witnesses for the p+ip / Majorana / fermion tower.

The compact stacking rule is in pip_third.py. Homotopies here certify only
its equivalences; they are not part of the formula's definition.
"""
from cochains import C, cup, faces
from pip_third import (sq,q,r,lower,source,upper_product,free_primitive,
                       pure_product_compact as P,product_compact as E,zero)

def B(x,y,p,s):return cup(x,y,p)+s*cup(x,y,p+1)
def D(x,y,p,s):return cup(x,y,p+1)+s*cup(x,y,p+2)

def gauge(a,h,c,u,W,s):
    p=a.d;v=u.di()
    return sq(u,2)+s*sq(u,1)+(W+s*s)*u+B(c,v,p,s)+D(c.di(),v,p,s)

def comm_residual(a,h,b,k,W,s):
    p=a.d;fa=q(a)+W*a;fb=q(b)+W*b
    u=cup(a,b,p);v=u.di();rev=cup(b,a,p-1)
    return (P(a,h,b,k,W,s)+P(b,k,a,h,W,s)+cup(fa,fb,p+2)
      +B(rev,v,p,s)+D(fa+fb+rev.di(),v,p,s)
      +sq(u,2)+s*sq(u,1)+(W+s*s)*u)

def assoc_residual(a,h,b,k,d,l,W,s):
    p=a.d;m=cup(a,b,p-1);n=cup(b,d,p-1);t=cup(a,d,p-1)
    fa=q(a)+W*a;fd=q(d)+W*d
    return (P(a,h,b,k,W,s)+P(a+b,h+k+cup(a,b,p),d,l,W,s)
       +P(b,k,d,l,W,s)+P(a,h,b+d,k+l+cup(b,d,p),W,s)
       +D(m,fd,p,s)+D(fa,n,p,s)+B(m,t+n,p,s)+B(n,m+t,p,s))

def transported_pull(a,h,s,grid,j):
    """Pull a twisted integral input, retaining its two binary digits.

    The value on the jth projection is transported from that projection's
    first vertex to the background projection's first vertex. A sign change
    leaves parity a unchanged and replaces the second bit h by h+a.
    """
    from coherence import pull
    ap=pull(a,grid,j);hp=pull(h,grid,j)
    for f in faces(len(grid)-1,a.d):
        x,y=grid[f[0]][0],grid[f[0]][j]
        transport=s[tuple(sorted((x,y)))] if x!=y else 0
        hp.v[f]=hp[f]+transport*ap[f]
    return ap,hp

def leading_primitive(callback,inputs,W,s,out_degree):
    """Fixed Eilenberg--Zilber H*, valid when the projection is zero.

    inputs is a sequence of (a,h) pairs, not independent a/h factors.
    Every use in the note includes a projection calculation.
    """
    from coherence import pull,signed_H_k
    k=1+len(inputs);vv={}
    hs=[(g,c) for g,c in signed_H_k(out_degree,k).items()
        if (c%2) and all(len({v[j+1] for v in g})>=a.d+1
                         for j,(a,h) in enumerate(inputs))]
    for f in faces(W.N,out_degree):
        out=0
        for g,c in hs:
            grid=tuple(tuple(f[x] for x in v) for v in g)
            Wp,sp=pull(W,grid,0),pull(s,grid,0)
            aa=[]
            for j,(a,h) in enumerate(inputs):
                aa.extend(transported_pull(a,h,s,grid,j+1))
            out=out+callback(*aa,Wp,sp).top()
        vv[f]=out
    return C(W.N,out_degree,vv)

def assoc_boundary(a,h,c,b,k,e,d,l,f,W,s):
    p=a.d
    return D(cup(a,b,p-1),f,p,s)+leading_primitive(assoc_residual,[(a,h),(b,k),(d,l)],W,s,p+1)

def comm_leading_boundary(a,h,b,k,W,s):
    if a.d==2:
        return leading_primitive(comm_residual,[(a,h),(b,k)],W,s,3)
    # The direct degree-one AW projection is not zero. Descend the proved
    # degree-two witness instead of incorrectly declaring that projection zero.
    from descent import susp,tau,extend_bg
    return tau(leading_primitive(comm_residual,
        [(susp(a),susp(h)),(susp(b),susp(k))],extend_bg(W),extend_bg(s),3))

def comm_boundary(a,h,c,b,k,e,W,s):
    return cup(c,e,a.d+1)+comm_leading_boundary(a,h,b,k,W,s)
