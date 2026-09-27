"""Exact unary bridge/gauge tests; optional unchanged collaborator oracle."""
import argparse,json,random,sys
from pathlib import Path
from fractions import Fraction
from itertools import combinations
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from fspt.pip_coordinates import phase_reference_shift,integer_gauge_phase
from fspt.formulas import pip_cf_coordinate
from fspt.formulas_pip_compile import evaluate_program
from fspt.formulas_export import gap_literal
sys.path.insert(0,str(root/'vendor/p_ip_d4_normalized_package/code'))
import cochains as q

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--reference-root',type=Path)
    args=parser.parse_args();oracle=None
    if args.reference_root:
        sys.path.insert(0,str(args.reference_root/'python/stacking_model'))
        sys.path.insert(0,str(args.reference_root/'python'))
        import upper_phase_diagnostic as oracle
    program=json.loads((root/'gap/pip_o5_program.json').read_text())
    fixtures=[]
    for seed in range(32):
        random.seed(8637+seed);N=5;s=q.random_cochain(0,N).d();w=q.C(2)
        for k in (1,2):
            n=s.lift().scaled(k)
            if k==1:
                b=q.primitive(q.cup(s,q.sq(n.reduce(2),1)))+q.random_cochain(1,N).d()
                Q=q.parity(n,b,w,s);c=q.primitive(Q)+q.random_cochain(2,N).d()
            else:b=q.C(2);c=q.random_cochain(2,N).d()
            L=q.C(3,fun=lambda f:pip_cf_coordinate(k,b,s,f))
            if oracle:
                cv=lambda x:oracle.p.Cochain(x.deg,lambda f:x(f))
                cref=oracle.production_phase(1,cv(n),cv(b),cv(c+L),cv(s),cv(w))(tuple(range(6)))
                native=Fraction(evaluate_program(program,{'n':n,'b':b,'c':c,'s':s}),16)
                witness=q.C(4,fun=lambda f:phase_reference_shift(k,b,c,s,f),mod=None)
                assert (cref-native-q.ds(witness,s)(tuple(range(6))))%1==0
            phase=phase_reference_shift(k,b,c,s,tuple(range(5)))
            encoded=[]
            for name,field in [('s',s),('b',b),('c',c)]:
                rows=[]
                for face in combinations(range(5),field.deg+1):
                    rows.append([[sum(2**i for i in range(a,z)) for a,z in zip(face,face[1:])],field(face)])
                encoded.append([name,rows])
            fixtures.append([k,phase.numerator,phase.denominator,encoded])
            if k==2:
                gauge=integer_gauge_phase(c,s,tuple(range(5)))
                fixtures.append([0,gauge.numerator,gauge.denominator,encoded])
    (root/'tests/pip_coordinate_cases.g').write_text('AFSPipCoordinateCases := '+gap_literal(fixtures)+';;\n')
    print('PASS',len(fixtures),'exact unary coordinate fixtures'+(' and64 unchanged scalar phase checks' if oracle else ''))
if __name__=='__main__':main()
