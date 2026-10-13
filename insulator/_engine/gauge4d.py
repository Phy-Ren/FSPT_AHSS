"""Adapted from the frozen U1f consolidated v0.7 formula archive."""
from .product4d import lower_gauge
from .simplex import C, F, O4d, combinations
from .prism import pull_on_path, evalface, interval_paths
def gauge_phase(a,k,n,s,r,u,v,lam=F(1,6)):
    if u.p!=1 or v.p!=3 or u.tw!=k.tw or v.tw!=n.tw:
        raise ValueError('Gauge cochains require degrees 1,3 and sheet,charge coefficients.')
    vals={}
    for f in combinations(range(a.N+1),6):
        total=F(0)
        for local_path,sign in interval_paths(5):
            path=tuple((tt,f[j]) for tt,j in local_path)
            aa,kk,nn,ss,rr=[pull_on_path(c,path) for c in (a,k,n,s,r)]
            fields=[]
            for c in (u,v):
                fields.append(C(6,c.p,{ff:path[ff[0]][0]*evalface(c,tuple(path[j][1] for j in ff)) for ff in combinations(range(7),c.p+1)},[c.tw[j] for _,j in path]))
            U,V=fields
            K,N=lower_gauge(aa,kk,nn,U,V,ss,rr)
            total+=sign*O4d(aa,K,N,ss,rr,lam)(tuple(range(7)))
        vals[f]=total%1
    return C(a.N,5,vals,s.tw)

