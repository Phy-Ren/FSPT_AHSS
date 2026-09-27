"""Independent local closure audit of the complete marked p+ip square."""
import json,random,sys
from pathlib import Path
from fractions import Fraction
from itertools import combinations
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fspt.formulas import formula,evaluate
from fspt.formulas_pip_compile import evaluate_program
from fspt.pip_coordinates import phase_reference_shift,integer_gauge_phase
sys.path.insert(0,str(ROOT/'vendor/p_ip_d4_normalized_package/code'))
import cochains as q

def main():
    data=json.loads((ROOT/'runs/formula_audit/pip_diagonal.json').read_text())
    nums=data['numerators'];den=data['modulus']
    program=json.loads((ROOT/'gap/pip_o5_program.json').read_text())
    for seed in range(256):
        random.seed(10701+seed);N=5;s=q.random_cochain(0,N).d();w=q.C(2)
        n=s.lift();b=q.primitive(q.cup(s,q.sq(s,1)))+q.random_cochain(1,N).d()
        fields={'n':n,'b':b,'s':s,'w':w}
        Q=q.C(4,fun=lambda f:evaluate(formula('pip_parity',1),fields,f))
        c=q.primitive(Q)+q.random_cochain(2,N).d();fields['c']=c
        s3=q.cup(q.cup(s,s),s)
        K=q.cup(b,b,1)+q.cup(b,b.d(),2)+q.cup(s,b);beta=K+s3
        @lru_cache(None)
        def gamma(f):
            key=sum(s((f[0],f[i]))<<(i-1) for i in range(1,5))
            key+=sum(b((f[0],f[i],f[j]))<<(4+r) for r,(i,j) in enumerate(combinations(range(1,5),2)))
            key+=sum(c((f[0],f[i],f[j],f[k]))<<(10+r) for r,(i,j,k) in enumerate(combinations(range(1,5),3)))
            return Fraction(nums[key],den)
        @lru_cache(None)
        def correction(f):
            return (2*phase_reference_shift(1,b,c,s,f)+gamma(f)
                    -phase_reference_shift(2,w,K,s,f)+integer_gauge_phase(K,s,f))%1
        H=q.C(4,fun=correction,mod=None);face=tuple(range(6))
        native=Fraction(evaluate_program(program,fields),16)
        target=Fraction(evaluate(formula('obstruction',2),{'a':w,'c':beta,'s':s,'w':w}),8)
        assert (q.ds(H,s)(face)+2*native-target)%1==0,('square',seed)
        # Explicitly remove the s^3 incoming Majorana boundary including its phase.
        mcphase=q.C(4,fun=lambda f:Fraction(evaluate(formula('obstruction',1),{'a':s,'c':w,'s':s,'w':w},f),8),mod=None)
        cross=q.cup(beta,s3,2)
        reduced=q.C(4,fun=lambda f:H(f)+mcphase(f)+Fraction(cross(f),2),mod=None)
        targetK=Fraction(evaluate(formula('obstruction',2),{'a':w,'c':K,'s':s,'w':w}),8)
        assert (q.ds(reduced,s)(face)+2*native-targetK)%1==0,('incoming-phase',seed)
    print('PASS256 random legal5simplex full marked squares and incoming Majorana phase gauges')
    # The table represents a normalized operation on group bar cochains.
    # Check every local input that collapses an adjacent vertex, including
    # its off-cone faces, rather than merely forcing the output to zero.
    from derive_pip_diagonal import legal_tower
    count=0
    for sm in range(16):
        for bm in range(64):
            for cm in range(16):
                s,b,c,_=legal_tower(sm,bm,cm)
                for collapse in range(4):
                    if s((collapse,collapse+1)):continue
                    replace=lambda f:tuple(collapse if x==collapse+1 else x for x in f)
                    if (all(b(f)==b(replace(f)) for f in combinations(range(5),3))
                        and all(c(f)==c(replace(f)) for f in combinations(range(5),4))):
                        assert nums[sm+16*bm+1024*cm]==0,(sm,bm,cm,collapse)
                        count+=1;break
    print('PASS diagonal normalization on',count,'degenerate legal towers')
if __name__=='__main__':main()
