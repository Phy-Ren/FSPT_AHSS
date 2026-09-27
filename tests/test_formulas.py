"""Exact local identities and independent agreement with the supplied oracle."""
import importlib.util
from itertools import combinations
from pathlib import Path
import random
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fspt.formulas import evaluate, field, formula, majorana_product, majorana_source, obstruction, stacking, zero, phase, cup, square


def coboundary(values,degree,N,mod=2):
    return {f:sum((-1)**i*values[f[:i]+f[i+1:]] for i in range(len(f)))%mod
            for f in combinations(range(N+1),degree+2)}


def test_fields(p,N,seed):
    rng=random.Random(seed)
    raw=lambda d:{f:rng.randrange(2) for f in combinations(range(N+1),d+1)}
    result={'s':coboundary(raw(0),0,N),'w':coboundary(raw(1),1,N)}
    for aname,cname in [('a','c'),('b','cp')]:
        a=coboundary(raw(p-1),p-1,N);result[aname]=a
        source=formula('majorana_source',p)
        values={**result,'a':a}
        arbitrary=coboundary(raw(p),p,N)
        result[cname]={f:(arbitrary[f]+(0 if 0 in f else evaluate(source,values,(0,)+f)))%2
                       for f in combinations(range(N+1),p+2)}
    return result


class FormulaTests(unittest.TestCase):
    def test_incoming_gauge_dictionary(self):
        a,c,w,s=field('a',1),field('c',2),field('w',2),field('s',1)
        P=majorana_source(a,w,s)
        first=(obstruction(a,zero(2),w,s).twisted_differential(s)
               -obstruction(zero(2),P,w,s)).reduce(8)
        # With dc=P the extra CF product term is the boundary of S^1(c)/2.
        second=(phase((4,cup(P,P,2)))-phase((4,square(c,1))).twisted_differential(s)).reduce(8)
        for seed in range(16):
            data=test_fields(1,5,801+seed)
            # The current space-group setting has omega=0.
            data['w']={f:0 for f in data['w']}
            source=formula('majorana_source',1)
            data['c']={f:0 if 0 in f else evaluate(source,data,(0,)+f)
                       for f in combinations(range(6),3)}
            self.assertEqual(evaluate(first,data),0)
            self.assertEqual(evaluate(second,data),0)

    def test_closure_and_product(self):
        for p in (1,2):
            a,b,c,cp=field('a',p),field('b',p),field('c',p+1),field('cp',p+1)
            w,s=field('w',2),field('s',1)
            O=obstruction(a,c,w,s)
            U=stacking(a,c,b,cp,w,s)
            residual=(U.twisted_differential(s)-obstruction(a+b,c+cp+majorana_product(a,b,s),w,s)
                      +O+obstruction(b,cp,w,s)).reduce(8)
            for seed in range(12):
                data=test_fields(p,p+4,seed)
                self.assertEqual(evaluate(O.twisted_differential(s),data),0,(p,seed,'closure'))
                self.assertEqual(evaluate(residual,data),0,(p,seed,'product'))

    def test_supplied_independent_oracle(self):
        path=ROOT/'vendor/FSPT_STACKING_MANUSCRIPT_ALIGNED_20260925/code'
        # The two supplied bundles both expose a module named cochains.
        # Keep their distinct APIs isolated when unittest discovers both suites.
        names=('cochains','manuscript')
        previous={name:sys.modules.pop(name,None) for name in names}
        sys.path.insert(0,str(path))
        try:
            import cochains as reference_cochains
            import manuscript as reference_manuscript
            spec=importlib.util.spec_from_file_location('supplied_formulas',path/'formulas.py')
            reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
            for p in (1,2):
                N=p+3
                for seed in range(8):
                    data=test_fields(p,N,100+seed)
                    degrees={'s':1,'w':2,'a':p,'b':p,'c':p+1,'cp':p+1}
                    obj={name:reference_cochains.C(N,degrees[name],values) for name,values in data.items()}
                    expected=reference_manuscript.Oca(obj['a'],obj['c'],obj['w'],obj['s']).top()
                    self.assertEqual(evaluate(formula('obstruction',p),data),expected)
                    expected=reference.Uca(obj['a'],obj['c'],obj['b'],obj['cp'],obj['w'],obj['s'])
                    for face in combinations(range(N+1),p+3):
                        self.assertEqual(evaluate(formula('stacking',p),data,face),expected[face])
        finally:
            sys.path.remove(str(path))
            for name in names:
                sys.modules.pop(name,None)
                if previous[name] is not None:
                    sys.modules[name]=previous[name]


if __name__=='__main__':unittest.main(verbosity=2)
