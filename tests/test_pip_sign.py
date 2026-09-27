"""Exact n=s O5 restriction, compared to the full generic specification."""
import json,random,sys
from pathlib import Path
from itertools import combinations
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from fspt.formulas_pip_compile import evaluate_program
from fspt.formulas_export import gap_literal
sys.path.insert(0,str(root/'vendor/p_ip_d4_normalized_package/code'))
import cochains as q
from pip_d4 import evaluate_simplex
full=json.loads((root/'gap/pip_o5_program.json').read_text())
fast=json.loads((root/'gap/pip_o5_sign.json').read_text())
# Complete exact BC2 pullback identities: pure O5=9*s^5/16, Xi(s)=0.
for mask in range(32):
 eps=[0]+[(mask>>i)&1 for i in range(5)];s=q.C(1,fun=lambda f:(eps[f[0]]+eps[f[1]])%2)
 fields={'n':s,'b':q.C(2),'c':q.C(3),'s':s}
 expected=1
 for i in range(5):expected*=s((i,i+1))
 assert evaluate_program(full,fields)==9*expected
 assert evaluate_simplex(1,n_integer=s,n_majorana=fields['b'],n_fermion=fields['c'],omega2=q.C(2),s1=s,validate=False)['numerator_mod16']==9*expected
 assert q.pure_parity(s.lift(),q.C(2),s)(tuple(range(5)))==0
fixtures=[]
for seed in range(512):
 random.seed(3876+seed);N=5;s=q.random_cochain(0,N).d();w=q.C(2)
 if seed%2:
  b=q.primitive(q.cup(s,q.sq(s,1)))+q.random_cochain(1,N).d()
  c=q.primitive(q.parity(s.lift(),b,w,s))+q.random_cochain(2,N).d()
 else:b=q.random_cochain(2,N);c=q.random_cochain(3,N)
 fields={'n':s,'b':b,'c':c,'s':s}
 old=evaluate_program(full,fields);new=evaluate_program(fast,fields)
 assert (old-new)%16==0,(seed,old,new)
 if seed<32:
  encoded=[]
  for name,field in [('s',s),('b',b),('c',c)]:
   rows=[]
   for face in combinations(range(6),field.deg+1):
    rows.append([[sum(2**i for i in range(a,z)) for a,z in zip(face,face[1:])],field(face)])
   encoded.append([name,rows])
  fixtures.append([new,encoded])
(root/'tests/pip_sign_cases.g').write_text('AFSPipSignCases := '+gap_literal(fixtures)+';;\n')
print('PASS complete sign identities and512 generic/special O5 cases, half legal/half arbitrary')
