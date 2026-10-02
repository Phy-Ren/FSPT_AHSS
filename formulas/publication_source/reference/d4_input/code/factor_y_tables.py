"""Exact blockwise separation of integer and extension variables.

This is matrix-rank factorization over F2, NOT a conversion to surjection words.
It neither changes the cochain nor adds a closed counterterm.
"""
from pathlib import Path
import json

def factor_block(block):
    ns=sorted({int(n) for n,w in block['terms']})
    ws=sorted({w for n,w in block['terms']})
    wx={w:i for i,w in enumerate(ws)}
    rows={n:0 for n in ns}
    for n,w in block['terms']: rows[int(n)]^=1<<wx[w]
    pivots={};basis=[];combinations={}
    for n in ns:
        r=rows[n];comb=0
        while r:
            p=r.bit_length()-1
            if p in pivots:
                v,i=pivots[p];r^=v;comb^=1<<i
            else:
                i=len(basis);pivots[p]=(r,i);basis.append(r);comb^=1<<i;break
        combinations[n]=comb
    factors=[]
    for i,row in enumerate(basis):
        factors.append({'n_codes':[str(n) for n in ns if combinations[n]>>i&1],
                        'w_masks':[w for j,w in enumerate(ws) if row>>j&1]})
    expanded=set()
    for f in factors:
        for n in f['n_codes']:
            for w in f['w_masks']:
                pair=(int(n),w)
                if pair in expanded:expanded.remove(pair)
                else:expanded.add(pair)
    assert expanded=={(int(n),w) for n,w in block['terms']}
    return {'i':block['i'],'j':block['j'],'k':block['k'],'rank':len(basis),
            'coefficient_count':len(block['terms']),'factors':factors}

def main():
    root=Path(__file__).parent
    out={}
    for r in (5,6):
        data=json.loads((root/f'Y{r}_word_total.json').read_text())
        blocks=[factor_block(b) for b in data['blocks']]
        result={'degree':r,'meaning':'F2 matrix factorization in each (s,n,omega) degree block; not surjection words',
                'all_expansions_exact':True,'blocks':blocks,
                'total_rank':sum(b['rank'] for b in blocks),
                'total_coefficients':sum(b['coefficient_count'] for b in blocks)}
        (root/f'Y{r}_tensor_factors.json').write_text(json.dumps(result,indent=2))
        out[str(r)]={key:result[key] for key in ('all_expansions_exact','total_rank','total_coefficients')}
        print(r,out[str(r)])
    (root/'factorization_certificate.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
