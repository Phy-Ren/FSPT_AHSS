"""Fixed normalized Eilenberg--Zilber homotopy, independent of either phase.

All operations are finite formal sums over F_2. The same recursion is used
in each dimension; no coefficient table, obstruction, or primitive is loaded.
"""
from functools import lru_cache

@lru_cache(None)
def simplex_shuffles(n:int):
    """G AW of the n-simplex diagonal in a threefold simplicial product."""
    result=[]
    for a in range(n+1):
        for b in range(a,n+1):
            counts=[a,b-a,n-b];path=[(0,a,b)]
            def rec():
                if not any(counts):result.append(tuple(path));return
                for d in range(3):
                    if counts[d]:
                        counts[d]-=1;v=list(path[-1]);v[d]+=1;path.append(tuple(v))
                        rec();path.pop();counts[d]+=1
            rec()
    return tuple(result)

@lru_cache(None)
def ez_homotopy(n:int):
    """Normalized acyclic-carrier EZ homotopy H_n, with dH+Hd=id+GAW."""
    if n==0:return ()
    zero=(0,0,0);out=set()
    for simplex in simplex_shuffles(n):
        if simplex[0]==zero:continue
        out.symmetric_difference_update(((zero,)+simplex,))
    for simplex in ez_homotopy(n-1):
        shifted=tuple(tuple(c+1 for c in v) for v in simplex)
        out.symmetric_difference_update(((zero,)+shifted,))
    return tuple(sorted(out))

def chain_boundary(chain):
    ans=set()
    for simplex in chain:
        for j in range(len(simplex)):
            face=simplex[:j]+simplex[j+1:]
            if len(set(face))<len(face):continue
            ans.symmetric_difference_update((face,))
    return ans

def verify_ez(max_degree=6):
    records=[]
    for n in range(1,max_degree+1):
        lhs=chain_boundary(ez_homotopy(n))
        for omit in range(n+1):
            vs=[j for j in range(n+1) if j!=omit]
            for simplex in ez_homotopy(n-1):
                lhs.symmetric_difference_update((tuple(tuple(vs[c] for c in v) for v in simplex),))
        rhs=set(simplex_shuffles(n));rhs.symmetric_difference_update((tuple((j,j,j) for j in range(n+1)),))
        assert lhs==rhs,(n,len(lhs^rhs))
        for collapse in range(n):
            image=set()
            for simplex in ez_homotopy(n):
                out=tuple(tuple(c-(c>collapse) for c in v) for v in simplex)
                if len(set(out))<len(out):continue
                image.symmetric_difference_update((out,))
            assert not image,('degeneracy',n,collapse,len(image))
        records.append({'degree':n,'H_simplices':len(ez_homotopy(n)),'Stokes':True,'degeneracies':True})
    return records

