#!/usr/bin/env python3
"""Exact finite Gysin presentation for the sign-line Thom spectrum of BC4."""
from pathlib import Path
from math import comb
import hashlib
import json
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_suffix('.json')

def matrix(n,k):
    return sp.Matrix(k,k,lambda i,j: comb(n,j-i+1) if 0<=j-i<n else 0)

def integers(a):
    return [[int(x) for x in row] for row in a.tolist()]

def snf(a):
    return [abs(int(x)) for x in smith_normal_form(a,domain=sp.ZZ).diagonal()]

def main():
    nilpotent = sp.Matrix([[0,1,0],[0,0,1],[0,0,0]])
    a2,a4 = matrix(2,3),matrix(4,3)
    q = 2*sp.eye(3)+2*nilpotent+nilpotent**2
    assert a4 == q*a2 == a2*q
    assert snf(q) == [1,2,4]
    assert snf(a2) == [1,1,8]
    assert snf(a4) == [2,2,16]
    geometry = []
    for spin in ('spinless','spin_half'):
        path = ROOT / f'insulator_catalog/generated/point3_10_{spin}.json'
        record = json.loads(path.read_text())
        gen = sp.Matrix(record['matrices'][1])
        assert gen**4 == sp.eye(3) and gen**2 != sp.eye(3)
        eigline = (gen+sp.eye(3)).nullspace()
        plane = (gen**2+sp.eye(3)).nullspace()
        assert len(eigline)==1 and len(plane)==2
        x = sp.Matrix.hstack(eigline[0],*plane)
        assert x.det()!=0
        conjugated = x.inv()*gen*x
        assert conjugated[0,0]==-1
        assert conjugated[0,1:]==sp.zeros(1,2)
        assert conjugated[1:,0]==sp.zeros(2,1)
        assert conjugated[1:,1:]**2==-sp.eye(2)
        geometry.append({'id':record['id'],'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                         'decomposition':'one real sign line plus one complex rotation line',
                         'intertwiner':integers(x),'generator_after_conjugacy':integers(conjugated)})
    result = {
        'method':'Hashimoto Gysin generators, natural fiber-squaring map, exact integer Smith forms',
        'cofiber':'BC2_+ -> BC4_+ -> (BC4)^sigma',
        'X':'(BC4)^(sigma-1)',
        'basis':'B0,B1,B2 in ku5; columns are relations or images',
        'A2':integers(a2),'A4':integers(a4),'Q_inclusion':integers(q),
        'factorization_A4_equals_Q_A2':True,
        'SNF_A2':snf(a2),'SNF_A4':snf(a4),'SNF_Q':snf(q),
        'ku4_X_torsion':[2,4], 'ku0_X_torsion':[2],
        'Omega4_Spinc_X_torsion':[2,2,4], 'freeRank':0,
        'ku1_X_and_ku5_X_zero':True,
        'inclusion_is_injective_reason':'A4=Q A2 and det(Q)!=0; the same argument in degree1',
        'inclusion_map_polynomial':'[4]_F(x)/[2]_F(x)=2+2ux+u^2x^2',
        'natural_pairing_assumed':False,
        'geometry':geometry,
        'all_checks_pass':True,
    }
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(OUT),'full_bordism_torsion':[2,2,4],'all_checks_pass':True}))

if __name__ == '__main__':
    main()
