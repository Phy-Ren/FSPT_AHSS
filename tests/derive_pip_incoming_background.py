"""Derive a CA-coordinate H0 integer boundary, using exact local equations.

The even-input calibration is the supplied degree-zero phase -P(omega)/8.
No space-group answer is an input. The odd half-valued ambiguity is retained
as an explicitly checked ambiguity of a cyclic boundary generator.
"""
from pathlib import Path
from itertools import combinations
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fspt.formulas import field,cup,formula
from fspt.formulas_fast_compile import compile_expression


def universal_w(dimension):
    choices=np.arange(1 << (dimension*(dimension-1)//2),dtype=np.int64)
    table={(0,)+f:(choices>>i)&1
           for i,f in enumerate(combinations(range(1,dimension+1),2))}
    def value(f):
        if len(set(f))<3:return np.zeros_like(choices)
        return table[f] if f[0]==0 else sum(table[(0,)+f[:i]+f[i+1:]] for i in range(3))%2
    return choices,value


def evaluate(expression,fields,face):
    builder,output,active=compile_expression(expression,())
    values={}
    for i in active:
        op,*args=builder.nodes[i]
        if op=='const':v=args[0]
        elif op=='field':v=fields[args[0]](tuple(face[j] for j in args[1]))
        elif op=='add':v=values[args[0]]+values[args[1]]
        elif op=='mul':v=values[args[0]]*values[args[1]]
        elif op=='mod':v=values[args[0]]%args[1]
        elif op=='div':
            assert np.all(values[args[0]]%args[1]==0)
            v=values[args[0]]//args[1]
        else:raise ValueError(op)
        values[i]=v
    return values[output]


def key(w,face):
    return sum(w((face[0],face[i],face[j])) << k
               for k,(i,j) in enumerate(combinations(range(1,len(face)),2)))


def solve_binary(equations):
    pivots={}
    for mask,rhs in equations:
        while mask:
            j=(mask&-mask).bit_length()-1
            if j in pivots:
                row,value=pivots[j];mask^=row;rhs^=value
            else:pivots[j]=(mask,rhs);break
        else:
            if rhs:raise ArithmeticError('No calibrated normalized incoming boundary')
    solution=0
    for j,(mask,rhs) in sorted(pivots.items(),reverse=True):
        if (bin(mask&solution).count('1')%2)^rhs:solution|=1<<j
    return solution,pivots


def derive():
    wexpr=field('w',2)
    pont=cup(wexpr.lift(),wexpr.lift(),integer=True)+cup(
        wexpr.lift(),wexpr.lift().differential(),1,integer=True)
    zero=lambda f:0
    _,w4=universal_w(4);face4=tuple(range(5))
    fields=dict(a=w4,b=w4,w=w4,s=zero,c=zero,cp=zero)
    P4=evaluate(pont,fields,face4)
    U4=evaluate(formula('stacking',2),fields,face4)
    base=(-P4-U4)%8  # 2F+U = -P/8, before selecting F's last bit.
    _,w5=universal_w(5);face5=tuple(range(6))
    fields5=dict(a=w5,w=w5,s=zero,c=zero)
    O5=2*evaluate(formula('obstruction',2),fields5,face5)
    faces=[face5[:i]+face5[i+1:] for i in range(6)]
    keys=np.array([key(w5,f) for f in faces])
    residual=(O5-sum((-1)**i*base[keys[i]] for i in range(6)))%16
    assert np.all(residual%8==0)
    equations=[]
    for j in range(1024):
        mask=0
        for i in range(6):mask^=1<<int(keys[i,j])
        equations.append((mask,int(residual[j]//8)))
    degenerate=set()
    for collapse in range(4):
        same=np.ones(64,dtype=bool)
        for f in combinations(range(5),3):
            collapsed=tuple(collapse if i==collapse+1 else i for i in f)
            same &= w4(f)==w4(collapsed)
        for i in np.flatnonzero(same):
            assert base[i]==0
            degenerate.add(int(i));equations.append((1<<int(i),0))
    solution,pivots=solve_binary(equations)
    values=(base+8*np.array([(solution>>i)&1 for i in range(64)]))%16
    actual=sum((-1)**i*values[keys[i]] for i in range(6))%16
    assert np.array_equal(actual,O5%16)
    assert np.all((2*values+2*U4+2*P4)%16==0)
    assert all(values[i]==0 for i in degenerate)
    # Sq1 omega equals the parity of the integral Bockstein pointwise here.
    def r(f):return (sum((-1)**i*w5(f[:i]+f[i+1:]) for i in range(4))//2)%2
    cf=evaluate(formula('obstruction',2),dict(a=zero,c=r,w=w5,s=zero),face5)
    dP=evaluate(pont.differential(),dict(w=w5),face5)
    assert np.all((cf+dP)%8==0)
    for f in combinations(range(6),4):
        assert np.all(r(f)==evaluate(cup(wexpr,wexpr,1),dict(w=w5),f))
    # Homogeneous freedom after the square calibration: F -> F+T/2.
    # Compute its full normalized closed-cochain kernel and compare with
    # ordinary coboundaries plus omega^2/2, which is 8 times the generator.
    homogeneous=[(mask,0) for mask,_ in equations]
    _,hpivots=solve_binary(homogeneous)
    dimension=64-len(hpivots)
    _,w3=universal_w(3);normal3=set()
    for collapse in range(3):
        same=np.ones(8,dtype=bool)
        for f in combinations(range(4),3):
            collapsed=tuple(collapse if i==collapse+1 else i for i in f)
            same &= w3(f)==w3(collapsed)
        normal3.update(map(int,np.flatnonzero(same)))
    delta3=[]
    keys3=np.array([key(w4,face4[:i]+face4[i+1:]) for i in range(5)])
    for basis in range(8):
        if basis in normal3:continue
        vector=np.sum(keys3==basis,axis=0)%2
        delta3.append(sum(int(x)<<i for i,x in enumerate(vector)))
    def rank(rows):return len(solve_binary((int(row),0) for row in rows)[1])
    square_values=w4((0,1,2))*w4((2,3,4))
    square_mask=sum(int(x)<<i for i,x in enumerate(square_values))
    assert rank(delta3)==3 and rank(delta3+[square_mask])==dimension==4
    for vector in delta3+[square_mask]:
        assert all((bin(vector&mask).count('1')%2)==0 for mask,_ in homogeneous)
    # Quadrupling differs from -P/4 only by the exact half phase below.
    def r4(f):return (sum((-1)**i*w4(f[:i]+f[i+1:]) for i in range(4))//2)%2
    rexpr=field('r',3)
    fourth=evaluate(cup(rexpr,rexpr,2),dict(r=r4),face4)
    eta_eq=[]
    for j in range(64):
        mask=0
        for i in range(5):mask^=1<<int(keys3[i,j])
        eta_eq.append((mask,int(fourth[j])))
    eta_eq.extend((1<<i,0) for i in normal3)
    eta,_=solve_binary(eta_eq)
    eta_values=[(eta>>i)&1 for i in range(8)]
    assert np.all((sum(np.array(eta_values)[keys3[i]] for i in range(5))-fourth)%2==0)
    return dict(denominator=16,numerators=list(map(int,values)),
        formula='unitary-incoming-pip-H0-CA-boundary',omega_degree=2,
        calibration='a=omega,c=0; delta F=O_CA; 2F+U_CA=-P(omega)/8',
        checks=dict(closed_omega_five_simplices=1024,
                    square_equations=64,normalized_states=len(degenerate),
                    even_boundary_closure=1024,
                    residual_normalized_half_phase_dimension=dimension,
                    exact_half_phase_dimension=3,
                    residual_generator='omega^2/2 = 8X',
                    quadruple_coboundary_equations=64),
        quadruple_gauge3_binary=eta_values,
        calibration_source='supplied fermionAHSS/python/low_phases.py::R0 at A=2,b=0',
        ambiguity_status='all solutions differ by exact half-phase plus 8X; cyclic subgroup unchanged')


if __name__=='__main__':
    result=derive()
    dest=ROOT/'runs/formula_audit/pip_incoming_background.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
