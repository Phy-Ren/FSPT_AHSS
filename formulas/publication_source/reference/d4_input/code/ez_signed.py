"""Signed normalized EZ chain homotopy: dH+Hd = identity-shuffle*AW."""
from functools import lru_cache
from collections import Counter

def clean(counter):return {k:v for k,v in counter.items() if v}

@lru_cache(None)
def signed_G(n):
    out=Counter()
    for a in range(n+1):
        for b in range(a,n+1):
            counts=[a,b-a,n-b];path=[(0,a,b)];letters=[]
            def rec():
                if not any(counts):
                    inv=sum(letters[i]>letters[j] for i in range(n) for j in range(i+1,n))
                    out[tuple(path)]+=(-1)**inv;return
                for d in range(3):
                    if counts[d]:
                        counts[d]-=1;v=list(path[-1]);v[d]+=1;path.append(tuple(v));letters.append(d)
                        rec();letters.pop();path.pop();counts[d]+=1
            rec()
    return clean(out)

@lru_cache(None)
def signed_H(n):
    if n==0:return {}
    zero=(0,0,0);out=Counter()
    for f,coef in signed_G(n).items():
        if f[0]!=zero:out[(zero,)+f]-=coef
    for f,coef in signed_H(n-1).items():
        out[(zero,)+tuple(tuple(c+1 for c in v) for v in f)]-=coef
    return clean(out)

def boundary(chain):
    out=Counter()
    for f,c in chain.items():
        for j in range(len(f)):
            ff=f[:j]+f[j+1:]
            if len(set(ff))<len(ff):continue
            out[ff]+=c*((-1)**j)
    return clean(out)

def verify(maxdegree=5):
    records=[]
    for n in range(1,maxdegree+1):
        lhs=Counter(boundary(signed_H(n)))
        for r in range(n+1):
            f=[j for j in range(n+1) if j!=r]
            for simplex,c in signed_H(n-1).items():lhs[tuple(tuple(f[j] for j in v) for v in simplex)]+=((-1)**r)*c
        rhs=Counter({tuple((j,j,j) for j in range(n+1)):1})
        for f,c in signed_G(n).items():rhs[f]-=c
        assert clean(lhs)==clean(rhs)
        for collapse in range(n):
            images=Counter()
            for f,c in signed_H(n).items():
                ff=tuple(tuple(v-(v>collapse) for v in x) for x in f)
                if len(set(ff))==len(ff):images[ff]+=c
            assert not clean(images)
        records.append({'degree':n,'support':len(signed_H(n)),'signed_identity':True,'all_degeneracies':True})
    return records
if __name__=='__main__':print(verify())
