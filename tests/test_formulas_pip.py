"""Check compiled full p+ip O5 against the unchanged supplied evaluator."""
from pathlib import Path
from itertools import combinations
import json
import random
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fspt.formulas_pip_compile import evaluate_program
from fspt.formulas import evaluate,formula


class PipTests(unittest.TestCase):
    def test_native_parity_and_full_phase(self):
        sys.path.insert(0,str(ROOT/'vendor/p_ip_d4_normalized_package/code'))
        import cochains as ref
        from pip_d4 import evaluate_simplex
        program=json.loads((ROOT/'gap/pip_o5_program.json').read_text())
        for seed in range(12):
            random.seed(7513+seed)
            N=5;s=ref.random_cochain(0,N).d();w=ref.C(2)
            n=s.lift() if seed%2 else ref.ds(ref.random_cochain(0,N,16).lift(),s)
            P=ref.sq(n.reduce(2),2)+ref.cup(w,n.reduce(2))+ref.cup(s,ref.sq(n.reduce(2),1))
            b=ref.primitive(P)+ref.random_cochain(1,N).d()
            Q=ref.parity(n,b,w,s)
            c=ref.primitive(Q)+ref.random_cochain(2,N).d()
            data={'n':n,'b':b,'c':c,'s':s,'w':w}
            for face in combinations(range(N+1),5):
                self.assertEqual(evaluate(formula('pip_parity',1),data,face),Q(face),(seed,face))
            expected=evaluate_simplex(1,n_integer=n,n_majorana=b,n_fermion=c,omega2=w,s1=s)
            self.assertEqual(evaluate_program(program,data),expected['numerator_mod16'],seed)


if __name__=='__main__':unittest.main(verbosity=2)
