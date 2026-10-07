#!/usr/bin/env python3
"""Replay the exact Majorana carry reduction using only public coefficient files.

Python3 standard library only. Binary and signed integer cochains are evaluated
on ordered simplices; canonical lifts remain whole. This is a formula replay,
not a group-cohomology or physical-calibration calculation.
"""
from pathlib import Path
from functools import lru_cache
from itertools import combinations
import argparse
import hashlib
import json
import random

HERE=Path(__file__).resolve().parent

@lru_cache(None)
def interval_terms(word,degrees):
    targets=[degrees[j]+1-word.count(j+1)for j in range(len(degrees))]
    if min(targets)<0:return()
    lengths=[0]*len(word);answer=[]
    def visit(i,remaining):
        if i==len(word):
            if any(remaining):return
            cuts=[0]
            for value in lengths:cuts.append(cuts[-1]+value)
            faces=[[]for _ in degrees]
            for k,label in enumerate(word):faces[label-1].extend(range(cuts[k],cuts[k+1]+1))
            if any(len(set(f))!=len(f)for f in faces):return
            inner=[word[k]in word[k+1:]for k in range(len(word))]
            lam=[lengths[k]+int(inner[k])for k in range(len(word))]
            exponent=sum(cuts[k+1]for k in range(len(word))if inner[k])
            exponent+=sum(lam[k]*lam[j]for k in range(len(word))for j in range(k+1,len(word))if word[k]>word[j])
            answer.append((tuple(map(tuple,faces)),(-1)**exponent));return
        j=word[i]-1
        choices=[remaining[j]]if word[i]not in word[i+1:]else range(remaining[j]+1)
        for value in choices:
            lengths[i]=value;left=remaining.copy();left[j]-=value;visit(i+1,left)
    visit(0,targets)
    return tuple(answer)

def degree(a):return len(next(iter(a)))-1

def differential(a):
    return{f:sum((-1)**j*a[f[:j]+f[j+1:]]for j in range(len(f)))for f in combinations(range(6),degree(a)+2)}

def reduce2(a):return{f:v%2 for f,v in a.items()}

def beta_open(a):return{f:v//2 for f,v in differential(a).items()}

def add(a,b,sign=1):return{f:a[f]+sign*b[f]for f in a}

def cup(a,b,i=0):
    p,q=degree(a),degree(b);d=p+q-i
    word=tuple(1+j%2 for j in range(i+2));cuts=interval_terms(word,(p,q))
    pref=(-1)**(i*(p+q)+i*(i-1)//2)
    return{f:pref*sum(sign*a[tuple(f[j]for j in ff)]*b[tuple(f[j]for j in gg)]for(ff,gg),sign in cuts)for f in combinations(range(6),d+1)}

def closed(rng,d):
    out={(0,)+f:rng.randrange(2)for f in combinations(range(1,6),d)}
    for f in combinations(range(1,6),d+1):out[f]=sum(out[(0,)+f[:j]+f[j+1:]]for j in range(d+1))%2
    return out

def binary_polynomial(terms,fields):
    value=0
    for term in terms:
        product=1
        for factor in term:product*=fields[factor['cochain']][tuple(factor['face'])]%2
        value^=product
    return value

def replay(old_path,new_path,cases=512):
    old=json.loads(old_path.read_text());new=json.loads(new_path.read_text())
    assert len(old['terms'])==old['term_count']==5707
    assert [r['term_count']for r in new['rows']]==[5,15,10,116]
    assert [r['coefficient']for r in new['rows']]==[1,-1,-1,1]
    assert all(len(r['terms'])==r['term_count']for r in new['rows'])
    assert sum(r['term_count']for r in new['rows'])==new['total_interior_terms']==146
    rng=random.Random(61760482624);top=tuple(range(6));classes=set();lift_patterns=set();carry_classes=set()
    for case in range(cases):
        u,v=[{f:rng.randrange(2)for f in combinations(range(6),4)}for _ in range(2)]
        w=closed(rng,2);A,Ap=reduce2(differential(u)),reduce2(differential(v));B,Bp=beta_open(u),beta_open(v)
        L={f:u[f]*v[f]for f in u};J={f:A[f]*Ap[f]for f in A};dL=differential(L);X=add(add(B,Bp),dL,-1)
        fields={r'\check n_3':u,r"\check n'_3":v,r'\overline{d\check n_3}':A,r"\overline{d\check n'_3}":Ap,
                r'\overline{\beta^\circ\check n_3}':reduce2(B),r"\overline{\beta^\circ\check n'_3}":reduce2(Bp),
                r'\widetilde{\beta^\circ\check n_3}':{f:(x//2)%2 for f,x in B.items()},r"\widetilde{\beta^\circ\check n'_3}":{f:(x//2)%2 for f,x in Bp.items()},
                r'\overline{\beta\overline{d\check n_3}}':reduce2(beta_open(A)),r"\overline{\beta\overline{d\check n'_3}}":reduce2(beta_open(Ap)),
                r'\bar B_4^\gamma':reduce2(B),r'\bar B_4^{\gamma\prime}':reduce2(Bp)}
        old_value=binary_polynomial(old['terms'],fields)
        values=[binary_polynomial(row['terms'],fields)for row in new['rows']]
        signed_lifts=sum(row['coefficient']*value for row,value in zip(new['rows'],values))
        def j(face):return J[tuple(map(int,face))]
        def l(face):return L[tuple(map(int,face))]
        half=j('12345')*l('0145')+j('01235')*l('0345')
        integer_N=j('01235')*j('01345')-j('02345')*j('01245')+j('01235')*j('12345')+j('01345')*j('12345')
        replacement=2*half+cup(X,J,3)[top]-integer_N+signed_lifts
        assert(2*old_value-replacement)%4==0,('carry',case)
        # The unchanged quarter terms test signed cups and all four residues.
        BN=beta_open(reduce2(add(u,v)));dB,dBp=differential(B),differential(Bp)
        unchanged=(cup(B,Bp,3)[top]+cup(add(B,Bp),L,2)[top]-cup(L,BN,2)[top]+cup(L,L,1)[top]-cup(w,L)[top]
                   +cup(add(dB,dBp),L,3)[top]+cup(L,J,2)[top]+cup(dB,Bp,4)[top]-cup(add(dB,dBp),dL,4)[top])
        classes.add((unchanged+replacement)%4);carry_classes.add(replacement%4);lift_patterns.add(tuple(values))
    assert classes=={0,1,2,3},classes
    assert len(lift_patterns)==16,lift_patterns
    counts=new['complete_formula_counts']
    assert counts['outer_total']==455+2+2+12+3+4+4==482
    assert counts['total_with_lift_wrappers_replaced_by_their_interior_terms']==482-4+146==624
    return{'status':'PASS','cases':cases,'domain':'arbitrary open binary degree-three inputs; exact open Bocksteins and canonical binary differentials; closed backgrounds',
           'comparison':'Exact pointwise equality modulo1 of the old5707-term half coefficient and the new ordinary-cup/canonical-lift expression; no representative change',
           'quarter_residues_with_unchanged_terms':sorted(classes),'carry_residues':sorted(carry_classes),'canonical_lift_patterns':len(lift_patterns),'counts':counts,
           'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in[old_path,new_path]}}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--old-table',type=Path,default=HERE/'FOUR_DIMENSIONAL_MAJORANA_STACKING_FACES.json')
    parser.add_argument('--new-table',type=Path,default=HERE/'FOUR_DIMENSIONAL_MAJORANA_STACKING_LIFTS.json')
    parser.add_argument('--cases',type=int,default=512)
    args=parser.parse_args();print(json.dumps(replay(args.old_table,args.new_table,args.cases),indent=2))
