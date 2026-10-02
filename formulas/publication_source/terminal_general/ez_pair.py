from functools import lru_cache
from itertools import combinations
@lru_cache(None)
def gaw(n):
    out=set()
    for a in range(n+1):
        for ones in combinations(range(n),a):
            s=set(ones);i=0;j=a;path=[(i,j)]
            for k in range(n):
                if k in s:i+=1
                else:j+=1
                path.append((i,j))
            out.add(tuple(path))
    return out
@lru_cache(None)
def homotopy(n):
    if n==0:return ()
    out=set()
    for f in gaw(n):
        if f[0]!=(0,0):out.symmetric_difference_update([((0,0),)+f])
    for f in homotopy(n-1):out.symmetric_difference_update([((0,0),)+tuple((i+1,j+1) for i,j in f)])
    return tuple(sorted(out))
def boundary(chain):
    out=set()
    for f in chain:
        for j in range(len(f)):
            ff=f[:j]+f[j+1:]
            if len(set(ff))<len(ff):continue
            out.symmetric_difference_update([ff])
    return out

def verify(degree=6):
    for n in range(1,degree+1):
        lhs=boundary(homotopy(n))
        for j in range(n+1):
            face=[i for i in range(n+1) if i!=j]
            for ff in homotopy(n-1):lhs.symmetric_difference_update([tuple((face[a],face[b]) for a,b in ff)])
        rhs=set(gaw(n));rhs.symmetric_difference_update([tuple((i,i) for i in range(n+1))]);assert lhs==rhs
    return True
