"""Eight explicit tetrahedral polynomials in the printed normal form.
No coefficient lookup or primitive solver is used by this module.
"""
from model import C,cup,digit

def tetrahedral(n,u,side,i):
    def ev(f):
        p=n(f[:3]);q=n((f[0],f[1],f[3]))-p;r=n(f[1:])
        x,y,z=(digit(t,0) for t in (p,q,r))
        X,Y,Z=(digit(t,1) for t in (p,q,r));eps=u(f)
        S=x+y+z;Q=X+Y+Z
        L2=(y+Y)*(x+z)+y*(X*(1+z)+Z*(1+x))
        R3=(Y*(X+Z)+x*z*(Y+Z)+y*(x*Y+X*z)
             +eps*(S+S*Q+x*y*z))
        if side=='L':
            if i==1:ans=(x+y)*(z+Z)+eps*(1+S+y*z*(1+x)+(x+y)*Q+z*Z)
            elif i==2:ans=L2
            elif i==3:ans=L2+Y*(X+Z)+eps*(S+z*(x+y)+(x+y)*Q+z*Z)
            elif i==4:ans=Y*(X+Z)+y*(x*(1+z+X+Y)+z*(Y+Z))
            else:raise ValueError(i)
        elif side=='R':
            if i==1:ans=R3+x*z*(1+y)+eps*(1+S+x*z*(1+y))
            elif i==2:ans=Y*(X+Z)+y*z*(1+x)
            elif i==3:ans=R3
            elif i==4:ans=y*z*(1+x)
            else:raise ValueError(i)
        else:raise ValueError(side)
        return ans%2
    return C(3,fun=ev)

def gamma(n,e):
    """Binomial(n,e) modulo two, including negative integer values."""
    if not 0 <= e < 8:raise ValueError('This evaluator implements 0 <= e < 8')
    def ev(f):
        out=1
        for b in range(3):
            if e>>b&1:out*=digit(n(f),b)
        return out%2
    return C(2,fun=ev)

def tensor5(n,u,m,v):
    out=C(5)
    for i in range(1,5):
        out=out+cup(gamma(n,i),tetrahedral(m,v,'L',i))+cup(tetrahedral(n,u,'R',i),gamma(m,i))
    return out
