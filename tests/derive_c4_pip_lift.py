"""Independently derive/check a complete universal C4^T torsion tower.

The finite group is only a source of flat cochains for pullback along a proved
homomorphism from the infinite affine group. It is never used to replace the
space-group classification. Retain ordered simplex vertex indices throughout:
repeated group vertices need not be simplicial degeneracies.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
import hashlib
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fspt.formulas import evaluate,formula
from fspt.formulas_pip_compile import evaluate_program
from derive_pip_coordinate import solve_binary


def bar_boundary(t):
    return [t[1:]]+[t[:i]+((t[i]+t[i+1])%4,)+t[i+2:] for i in range(len(t)-1)]+[t[:-1]]


def simplex_fields(t,c):
    vertices=[0]
    for x in t:vertices.append((vertices[-1]+x)%4)
    def differences(face):return tuple((vertices[face[i+1]]-vertices[face[i]])%4 for i in range(len(face)-1))
    s=lambda f:differences(f)[0]%2
    b=lambda f:(differences(f)[0]%2)*(differences(f)[1]//2)
    return dict(n=s,s=s,b=b,c=lambda f:c(differences(f)),w=lambda f:0)


def derive(directory,phase_file=None,original_oracle=True):
    fs3=list(product(range(1,4),repeat=3));i3={t:i for i,t in enumerate(fs3)}
    fs4=list(product(range(1,4),repeat=4));i4={t:i for i,t in enumerate(fs4)}
    equations=[]
    for t in fs4:
        mask=0
        for f in bar_boundary(t):
            if 0 not in f:mask^=1<<i3[f]
        rhs=evaluate(formula('pip_parity',1),simplex_fields(t,lambda f:0))
        equations.append((mask,rhs))
    solution,rank=solve_binary(equations)
    cvalues=[(solution>>i)&1 for i in range(27)]
    def c(t):return 0 if 0 in t else cvalues[i3[t]]
    # Include all degenerate tuples: these are tested, not assumed normalized.
    for t in product(range(4),repeat=4):
        Q=evaluate(formula('pip_parity',1),simplex_fields(t,c))
        assert sum(c(f) for f in bar_boundary(t))%2==Q
    program=json.loads((ROOT/'gap/pip_o5_program.json').read_text())
    @lru_cache(None)
    def O(t):return evaluate_program(program,simplex_fields(t,c))%16
    for t in product(range(4),repeat=6):
        value=sum(((-1)**t[0] if i==0 else (-1)**i)*O(f) for i,f in enumerate(bar_boundary(t)))
        assert value%16==0,(t,value)
    fs5=list(product(range(1,4),repeat=5));values=[O(t) for t in fs5];rows=[]
    for t in fs5:
        row=[0]*81
        for i,f in enumerate(bar_boundary(t)):
            if 0 not in f:row[i4[f]]+=((-1)**t[0] if i==0 else (-1)**i)
        rows.append(row)
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'c4_pip_matrix.g').write_text('AFS_C4_D5:='+str(rows)+';;\nAFS_C4_O5:='+str(values)+'/16;;\nAFS_C4_C3:='+str(cvalues)+';;\n')
    record=dict(group='C4 with odd generator acting by coefficient sign',
                n='t mod2',b='(g mod2)*floor(h/2)',c3=cvalues,
                normalized_cf_equation_rank=rank,all_cf_equations_checked=256,
                all_top_closure_equations_checked=4096,modulus=16,obstruction_numerators=values)
    if phase_file is not None:
        phase=json.loads(phase_file.read_text());vvalues=[Fraction(a,b) for a,b in phase['phase4']]
        def v(t):return Fraction(0) if 0 in t else vvalues[i4[t]]
        # Check against the unmodified delivered scalar evaluator as well as
        # the compiler. This catches a shared compiler/flat-tower mistake.
        if original_oracle:
            sys.path.insert(0,str(ROOT/'vendor/p_ip_d4_normalized_package/code'))
            from cochains import C
            from pip_d4 import evaluate_simplex
        for t in product(range(4),repeat=5):
            value=sum(((-1)**t[0] if i==0 else (-1)**i)*v(f) for i,f in enumerate(bar_boundary(t)))
            assert (value-Fraction(O(t),16))%1==0,(t,value,O(t))
            if original_oracle:
                f=simplex_fields(t,c)
                original=evaluate_simplex(1,n_integer=C(1,fun=f['n'],mod=None),
                    n_majorana=C(2,fun=f['b']),n_fermion=C(3,fun=f['c']),
                    omega2=C(2),s1=C(1,fun=f['s']))['numerator_mod16']
                assert original==O(t),(t,original,O(t))
        record.update(phase4=phase['phase4'],all_phase_equations_checked=1024,
                      unchanged_supplied_oracle_equations_checked=1024 if original_oracle else 0,
                      phase_denominators=sorted(set(x.denominator for x in vvalues)),
                      phasePrimitiveVerified=True,
                      phaseInputSha256=hashlib.sha256(phase_file.read_bytes()).hexdigest(),
                      obstructionProgramSha256=hashlib.sha256(
                          (ROOT/'gap/pip_o5_program.json').read_bytes()).hexdigest())
        if 'transportCorrection' in phase:
            record['transportCorrection']=phase['transportCorrection']
            record['originalPhaseSha256']=phase['originalPhaseSha256']
        literals=lambda values:'['+','.join(str(Fraction(*x)) for x in values)+']'
        (ROOT/'gap/pip_c4_data.g').write_text('# Exact universal C4 flat tower, verified on all normalized and degenerate tuples.\nAFSC4PipC3 := '+str(cvalues)+';;\nAFSC4PipPhase4 := '+literals(phase['phase4'])+';;\n')
    (directory/'c4_pip_lift.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ['c3','phase4','obstruction_numerators']}))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--phase-file',type=Path)
    ap.add_argument('--skip-original-oracle',action='store_true')
    ap.add_argument('--directory',type=Path,default=ROOT/'runs/formula_audit');a=ap.parse_args()
    derive(a.directory,a.phase_file,not a.skip_original_oracle)
