"""Derive and exhaustively check the torsion-sector CF coordinate dictionary.

This audit imports the collaborator's mathematical secondary operation solely
as a comparison oracle. Production classification never imports that checkout.
Usage: python tests/derive_pip_coordinate.py --reference-root /path/to/fermionAHSS
"""
from pathlib import Path
from itertools import combinations
import argparse
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fspt.formulas import evaluate,formula


def lower_tower(dimension,sign_bits,majorana_bits,multiple):
    epsilon=[0]+[(sign_bits>>i)&1 for i in range(dimension)]
    s=lambda f:(epsilon[f[0]]+epsilon[f[1]])%2 if f[0]!=f[1] else 0
    n=lambda f:multiple*s(f)
    faces=list(combinations(range(1,dimension+1),2))
    values={(0,)+f:(majorana_bits>>i)&1 for i,f in enumerate(faces)}
    def b(f):
        if len(set(f))<3:return 0
        if 0 in f:return values[f]
        source=(multiple%2)*s((0,f[0]))*s((f[0],f[1]))*s((f[1],f[2]))
        return (source+sum(values[(0,)+f[:i]+f[i+1:]] for i in range(3)))%2
    return n,b,s


def simplex_key(s,b,face):
    return (sum(s((face[0],face[i]))<<(i-1) for i in range(1,4))
            +sum(b((face[0],face[i],face[j]))<<(3+r)
                 for r,(i,j) in enumerate(combinations(range(1,4),2))))


def solve_binary(equations):
    pivots={}
    for mask,rhs in equations:
        while mask:
            j=(mask&-mask).bit_length()-1
            if j in pivots:
                row,value=pivots[j];mask^=row;rhs^=value
            else:pivots[j]=(mask,rhs);break
        else:
            if rhs:raise ArithmeticError('Coordinate difference has no normalized local primitive')
    solution=0
    for j,(mask,rhs) in sorted(pivots.items(),reverse=True):
        if (bin(mask&solution).count('1')%2)^rhs:solution|=1<<j
    return solution,len(pivots)


def derive(reference_root):
    sys.path.insert(0,str(reference_root/'python'))
    import phase_eval as p
    import low_phases as low
    records=[]
    for multiple in range(4):
        equations=[];difference_count=0
        for sign_bits in range(16):
            for b_bits in range(64):
                n,b,s=lower_tower(4,sign_bits,b_bits,multiple)
                fields={'n':n,'b':b,'s':s,'w':lambda f:0}
                native=evaluate(formula('pip_parity',1),fields)
                reference=low.secondary(p.Cochain(1,n),p.Cochain(2,b),p.Cochain(1,s),p.zero(2))((0,1,2,3,4))
                rhs=native^int(reference);difference_count+=rhs;row=0
                for omit in range(5):
                    row^=1<<simplex_key(s,b,tuple(j for j in range(5) if j!=omit))
                equations.append((row,rhs))
        # Enforce zero on every degenerate ordered three-simplex.
        for sign_bits in range(8):
            for b_bits in range(8):
                n,b,s=lower_tower(3,sign_bits,b_bits,multiple)
                for collapse in range(3):
                    if s((collapse,collapse+1)):continue
                    compatible=True
                    for face in combinations(range(4),3):
                        image=tuple(collapse if x==collapse+1 else x for x in face)
                        if b(face)!=b(image):compatible=False
                    if compatible:equations.append((1<<simplex_key(s,b,(0,1,2,3)),0))
        solution,rank=solve_binary(equations)
        assert all(bin(row&solution).count('1')%2==rhs for row,rhs in equations)
        coefficients=[(solution>>i)&1 for i in range(64)]
        for bit in range(6):
            for i in range(64):
                if i&(1<<bit):coefficients[i]^=coefficients[i^(1<<bit)]
        records.append(dict(integer_multiple=multiple,all_legal_four_simplex_states=1024,
                            normalized=True,difference_count=difference_count,rank=rank,
                            truth_table=solution,anf=[i for i,v in enumerate(coefficients) if v]))
    return records


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--reference-root',type=Path,required=True)
    args=parser.parse_args();reference=args.reference_root.resolve()
    result={'reference_revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=reference,text=True).strip(),
            'variables':['s01','s02','s03','B012','B013','B023'],
            'identity':'d Lambda_k = native_short_d3 + collaborator_secondary, n1=k*s1, omega2=0',
            'records':derive(reference)}
    directory=ROOT/'runs/formula_audit';directory.mkdir(parents=True,exist_ok=True)
    (directory/'pip_c_coordinate_torsion.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
