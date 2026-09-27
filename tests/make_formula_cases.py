"""Generate local simplicial fixtures for a cross-language runtime check."""
from itertools import combinations
from pathlib import Path
import json
import random
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
from test_formulas import test_fields
from fspt.formulas import evaluate,formula
from fspt.formulas_export import gap_literal
from fspt.formulas_pip_compile import evaluate_program


def encoded(data,N):
    vertices=[0]
    for i in range(N):vertices.append(vertices[-1]+2**i)
    result=[]
    for name,values in data.items():
        rows=[]
        for face,value in values.items():
            rows.append([[vertices[j]-vertices[i] for i,j in zip(face,face[1:])],value])
        result.append([name,rows])
    return result


cases=[]
for p in (1,2):
    for seed in (23,51):
        for name in ('obstruction','stacking','majorana_source'):
            expression=formula(name,p);N=expression.degree;data=test_fields(p,N,seed)
            expected=evaluate(expression,data)
            cases.append([name,p,N,8 if name in ('obstruction','stacking') else 1,expected,encoded(data,N)])
            data['w']={face:0 for face in data['w']}
            expected=evaluate(expression,data)
            cases.append([name,p,N,8 if name in ('obstruction','stacking') else 1,expected,encoded(data,N)])

sys.path.insert(0,str(ROOT/'vendor/p_ip_d4_normalized_package/code'))
import cochains as ref
program=json.loads((ROOT/'gap/pip_o5_program.json').read_text())
for seed in (12,17):
    random.seed(seed);N=5;s=ref.random_cochain(0,N).d();w=ref.C(2)
    n=s.lift() if seed%2 else ref.ds(ref.random_cochain(0,N,16).lift(),s)
    P=ref.cup(s,ref.sq(n.reduce(2),1));b=ref.primitive(P)+ref.random_cochain(1,N).d()
    Q=ref.parity(n,b,w,s);c=ref.primitive(Q)+ref.random_cochain(2,N).d()
    fields={'n':n,'b':b,'c':c,'s':s}
    data={name:{f:x(f) for f in combinations(range(N+1),x.deg+1)} for name,x in fields.items()}
    cases.append(['pip_obstruction',1,5,16,evaluate_program(program,data),encoded(data,N)])

(ROOT/'tests/formula_cases.g').write_text('AFSFormulaCases := '+gap_literal(cases)+';;\n')
