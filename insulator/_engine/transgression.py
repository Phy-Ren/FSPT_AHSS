"""Adapted from the frozen U1f consolidated v0.7 formula archive."""
from .simplex import C, F, background, Q4d, O4d
from .prism import pull_on_path
from itertools import combinations
def shuffles(m,D):
    for positions in combinations(range(m+D),m):
        positions=set(positions);i=j=0;path=[(0,0)];exp=0
        for step in range(m+D):
            if step in positions:i+=1;exp+=j
            else:j+=1
            path.append((i,j))
        yield tuple(path),(-1)**exp

def parent_fields(a,ks,ns,s,r,path):
    aa,ss,rr=[pull_on_path(c,path) for c in (a,s,r)];K=[pull_on_path(c,path) for c in ks];NN=[pull_on_path(c,path) for c in ns];N=len(path)-1
    A,B=background(aa,ss)
    theta=[]
    for j in range(1,len(ks)+1):
        eta=C(N,0,{(i,):int(p>=j) for i,(p,v) in enumerate(path)})
        theta.append(eta.d())
    kp=C(N,2,{},ss.tw);np=C(N,4,{},rr.tw)
    for th,k,n in zip(theta,K,NN):
        kp=kp+th.cup(k)
        np=np+th.cup(n)+B.cup(th,1).cup(k)
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
            chi=theta[i].cup(theta[j],1);L=K[i].cup(K[j])
            Z=chi.cup(L)+theta[i].cup(K[i].cup(theta[j],1)).cup(K[j])
            np=np+rr.cup(Z)+rr.cup(chi,1).cup(L).d()
    return aa,kp,np,ss,rr

def integrate_parent(a,ks,ns,s,r,lam=F(1,6),validate=False):
    m=len(ks);D=6-m;vals={}
    for f in combinations(range(a.N+1),D+1):
        value=F(0)
        for path,sign in shuffles(m,D):
            path=tuple((p,f[v]) for p,v in path)
            aa,kp,np,ss,rr=parent_fields(a,ks,ns,s,r,path)
            if validate:
                assert kp.d().maxabs()==0
                assert (np.d()-Q4d(aa,kp,ss,rr)).maxabs()==0
            value+=sign*O4d(aa,kp,np,ss,rr,lam)(tuple(range(7)))
        vals[f]=value%1
    return C(a.N,D,vals,s.tw)

def O3canonical(a,k,n,s,r):return integrate_parent(a,[k],[n],s,r)

def E3canonical(r,k,kp):return r.cup(k.cup(kp)).sc(-1)

def E4canonical(a,k,n,kp,np,s,r):return integrate_parent(a,[k,kp],[n,np],s,r)

def A3canonical(a,ks,ns,s,r):return integrate_parent(a,ks,ns,s,r).sc(-1)

