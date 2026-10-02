from model import *
from itertools import combinations
pairs=list(combinations(range(1,7),2));terms=[]
for nc,wc in YTERMS:
    es=tuple((int(nc)>>(4*j))&15 for j in range(15))
    if any(e and v!=6 for (u,v),e in zip(pairs,es)):continue
    word=tuple(es[pairs.index((u,6))] for u in range(1,6))
    if any(e==0 for e in word):raise AssertionError('Source is not normalized')
    terms.append(word)
print('suspended y6 words',terms)

def comps(n,l):
 if l==1:
    if n>0:yield (n,)
    return
 for i in range(1,n-l+2):
    for c in comps(n-i,l-1):yield (i,)+c

def boundary(word):
    out=set()
    for j,e in enumerate(word):
        for k in range(1,e):
            out.symmetric_difference_update([word[:j]+(k,e-k)+word[j+1:]])
    return out
sol=[];records=[]
for w in sorted(set(sum(t) for t in terms)):
    candidates=list(comps(w,4));piv={}
    for j,t in enumerate(candidates):
        c=boundary(t);wit=1<<j
        while c:
            i=max(c)
            if i not in piv:piv[i]=(c,wit);break
            cc,z=piv[i];c.symmetric_difference_update(cc);wit^=z
    target=set(t for t in terms if sum(t)==w);z=0
    while target:
        i=max(target)
        if i not in piv:break
        cc,zz=piv[i];target.symmetric_difference_update(cc);z^=zz
    assert not target
    solved=[t for j,t in enumerate(candidates) if z>>j&1];sol+=solved
    records.append({'weight':w,'source_terms':[t for t in terms if sum(t)==w],'primitive_terms':solved})
print('endpoint4',sol)
Path(__file__).with_name('suspension_endpoint.json').write_text(json.dumps({'source_words':terms,'primitive_words':sol,'checks':records},indent=2))
