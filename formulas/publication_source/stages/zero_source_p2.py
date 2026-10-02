"""Exact zero-background evaluation of the supplied d4 (not a new formula).
The only acceleration is the pre-expanded existing prism transgression.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,sq
from polynomial_tables import total_cochain
from compact import beta_open,integer_inputs,kappa
from explicit_pip import full_terms16,sum_terms
D=json.loads(ROOT.joinpath('stages/data/T6_zero_anf.json').read_text())
FACES=[tuple(f) for f in D['faces']];MASKS=[int(m) for m in D['ANF_masks']]

def T6(u):
 def ev(f):
  bits=sum(int(u(tuple(f[i] for i in g)))<<j for j,g in enumerate(FACES))
  return sum(1 for m in MASKS if bits&m==m)%2
 return C(6,fun=ev)

def source16(n,u,c,*,repair=False):
 from cochains import pure_parity
 p=2;w=C(2);s=C(1);A,K,bA,_=integer_inputs(n,w,s)
 b=beta_open(u);Xi=pure_parity(n,w,s)
 y=total_cochain(n,w,s,'Y6_word_total.json',6)
 out=(sq(c,2)+T6(u)+cup(kappa(u,w,s),Xi,4)+y).lift().scaled(8)
 out=out+(cup(b,b,2)+cup(b,b.d(),3)+cup(K,K,2)+cup(bA,K,3)).scaled(4)
 if repair:out=out+cup(cup(n,n),n).scaled(4)
 return out
