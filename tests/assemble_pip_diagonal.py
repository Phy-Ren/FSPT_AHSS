"""Assemble and independently compile universal diagonal operation shards."""
from pathlib import Path
from itertools import combinations
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fspt.formulas import cuts
from derive_pip_diagonal import legal_tower


def cup_value(i,p,a,q,b,f):
    word=tuple(1+j%2 for j in range(i+2));total=0
    for faces,weight in cuts(word,(p,q)):
        total+=a(tuple(f[j] for j in faces[0]))*b(tuple(f[j] for j in faces[1]))
    return total%2


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--directory',type=Path,default=ROOT/'runs/formula_audit/pip_diagonal');args=ap.parse_args()
    table=[None]*16384;revision=None
    for sign in range(16):
        record=json.loads((args.directory/('sign%02d.json'%sign)).read_text())
        assert record['sign']==sign and record['start']==0 and record['batched_CF']
        assert len(record['numerators'])==64
        if revision is None:revision=record['reference_revision']
        assert revision==record['reference_revision']
        for b,row in enumerate(record['numerators']):
            assert len(row)==16
            for c,value in enumerate(row):table[sign+16*b+1024*c]=value
            s,B,C,cr=legal_tower(sign,b,0)
            def dB(f):return sum(B(f[:i]+f[i+1:]) for i in range(4))%2
            f=(0,1,2,3)
            K=(cup_value(1,2,B,2,B,f)+cup_value(2,2,B,3,dB,f)+s(f[:2])*B(f[1:]))%2
            beta=(K+s((0,1))*s((1,2))*s((2,3)))%2
            assert record['beta_reference_0123'][b]==beta,(sign,b,beta,record['beta_reference_0123'][b])
    assert None not in table
    coefficients=table[:]
    for bit in range(14):
        for mask in range(16384):
            if mask&(1<<bit):coefficients[mask]=(coefficients[mask]-coefficients[mask^(1<<bit)])%16
    terms=[(mask,c) for mask,c in enumerate(coefficients) if c]
    restored=coefficients[:]
    for bit in range(14):
        for mask in range(16384):
            if mask&(1<<bit):restored[mask]=(restored[mask]+restored[mask^(1<<bit)])%16
    assert restored==table
    artifact=dict(reference_revision=revision,coordinate='native input; reference output',
       formula='diagonal production phase4, n=s, omega=0',modulus=16,
       variables=['s01','s02','s03','s04','B012','B013','B014','B023','B024','B034','C0123','C0124','C0134','C0234'],
       numerators=table,multilinear_polynomial=terms,all_local_states=16384,
       beta_identity='beta_reference=S1(B)+sB+s^3',beta_checks=1024)
    (ROOT/'runs/formula_audit/pip_diagonal.json').write_text(json.dumps(artifact,indent=2)+'\n')
    lines=['# Independently evaluated universal diagonal formula; no SG answers.',
           '# Source revision '+revision,
           '# All16384local legal states; beta relation checked1024times.',
           'AFSPipDiagonalNumerators := '+str(table)+';;',
           'AFSPipDiagonalPolynomial := '+str([list(x) for x in terms])+';;',
           'AFSPipReferenceDiagonal := function(ctx,b,c)',
           'return AFSMemo(function(g,h,j,l)',
           'local bits,key;',
           'bits:=[ctx.s(g),ctx.s(g*h),ctx.s(g*h*j),ctx.s(g*h*j*l),',
           'b(g,h),b(g,h*j),b(g,h*j*l),b(g*h,j),b(g*h,j*l),b(g*h*j,l),',
           'c(g,h,j),c(g,h,j*l),c(g,h*j,l),c(g*h,j,l)];',
           'key:=Sum([1..14],i->2^(i-1)*(bits[i] mod 2));',
           'return AFSPipDiagonalNumerators[key+1]/16;',
           'end);end;;']
    (ROOT/'gap/pip_diagonal_data.g').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(states=len(table),terms=len(terms),beta_checks=1024,reference_revision=revision)))

if __name__=='__main__':main()
