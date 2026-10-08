"""Verify the current Majorana phase transport with public data only.

This is an exact Boolean/integer coefficient check on arbitrary open
three-cochains and closed backgrounds. It verifies the displayed relative
coefficient file against the fixed height-transgression construction.
"""
from pathlib import Path
from collections import Counter
import json, re, sys, random, time
HERE=Path(__file__).resolve().parent
PUBLIC=HERE.parent
sys.path.insert(0,str(PUBLIC/'formulas/publication_source/reference/d4_input/code'))
from cochains import C,cup,op,sq,ds,zeta1,zeta2,random_cochain
from compact import beta_open,kappa
random.seed(2026100813)
words=json.loads((PUBLIC/'formulas/publication_source/stages/data/mc3_zero_dictionary.json').read_text())['words']
text=(PUBLIC/'docs/formulas/source/pages/FOUR_DIMENSIONAL_MAJORANA_WORD_COEFFICIENTS.md').read_text()
pure=[];oldmixed=[]
for block in text.split('## Coefficient block ')[1:]:
    args=re.search(r'```math\n\((.*?)\)\.\n```',block,re.S).group(1).split(',')
    ws=re.search(r'```text\n(.*?)\n```',block,re.S).group(1).split()
    (oldmixed if r'd\check n_3' in args else pure).extend((w,args)for w in ws)
assert len(pure)==85 and len(oldmixed)==1005
coefficient_path=PUBLIC/'docs/formulas/data/four_dimensional_majorana_relative_words.json'
rows=json.loads(coefficient_path.read_text())['terms']
assert len(rows)==1897
# The Markdown table is the editable reader source; the JSON is a checked,
# lossless machine copy. Compare multiplicities as well as ordered inputs.
relative_text=(PUBLIC/'docs/formulas/source/pages/FOUR_DIMENSIONAL_MAJORANA_RELATIVE_WORD_COEFFICIENTS.md').read_text()
relative_blocks=relative_text.split('## Coefficient block ')[1:]
input_names={r'\check n_3':'u',r'd\check n_3':'A',r'\omega_2':'w',r's_1':'s'}
reader_rows=[]
for block in relative_blocks:
    args=re.search(r'```math\n\((.*?)\)\.\n```',block,re.S).group(1).split(',')
    block_words=re.search(r'```text\n(.*?)\n```',block,re.S).group(1).split()
    declared_count=int(re.search(r'This block contains \*\*(\d+) terms',block).group(1))
    assert declared_count==len(block_words)
    reader_rows.extend((word,tuple(input_names[a]for a in args))for word in block_words)
assert len(relative_blocks)==77
assert Counter(reader_rows)==Counter((row['word'],tuple(row['inputs']))for row in rows)
phase_text=(PUBLIC/'docs/formulas/source/pages/FOUR_DIMENSIONAL_MAJORANA_PHASE.md').read_text()
phase_words=re.search(r'```text\n(.*?)\n```',phase_text,re.S).group(1).split()
assert len(phase_words)==32 and Counter(phase_words)==Counter(words)

def H5(u,w,s):
    B=beta_open(u);b=B.reduce(2);bw=beta_open(w).reduce(2)
    H=sum((op(word,u,u,u,u)for word in words),C(5))
    H+=cup(u,b,2)+cup(u,bw,1)
    H+=op('131321',u,u,w)+op('1241431232',u,u,u,w)+op('1412432131',u,u,u,w)
    H+=op('131212',u,b,s)+op('1312121',b,b,s)
    H+=op('1241312132',u,u,b,s)+op('1241323132',u,u,b,s)
    H+=op('1241323213',u,u,b,s)+op('1243123231',u,u,b,s)
    return H+op('1321',u,w,s)

def R0(u,w,s): return H5(u,w,s).lift().scaled(2)+cup(u.lift(),u.lift(),1)
def R(u,c,w,s):return R0(u,w,s)+cup(s,c).lift().scaled(2)

def Jhalf_no_second_carry(u,w,s):
    B=beta_open(u);b=B.reduce(2);q=cup(u,u,1);wu=cup(w,u);sb=cup(s,b)
    X=sum((op(v,u,u,u,u)for v in ['1213243142','1213431412','1232431421','1234314212']),C(6))+cup(b,b,2)
    return zeta2(w,u)+X+cup(q,wu,4)+cup(q,sb,4)+cup(wu,sb,4)+zeta1(s,b)+cup(cup(w,s,1),b)+cup(s,q)

def J(u,w,s):
    B=beta_open(u);b=B.reduce(2)
    H=Jhalf_no_second_carry(u,w,s)+cup(cup(s,s),(B+b.lift()).div(2).reduce(2))
    return H.lift().scaled(2)+cup(w.lift(),B)+cup(B,B,2)

def Gamma(u,w,s):
    B=beta_open(u);b=B.reduce(2);fields={r'\check n_3':u,r'\omega_2':w,r's_1':s}
    T=sum((op(word,*(fields[a]for a in args))for word,args in pure),C(6))
    ell=beta_open(w).reduce(2)+cup(s,w)
    H=T+cup(cup(s,s),(B-b.lift()).div(2).reduce(2))+cup(u,ell)
    return H.lift().scaled(2)+cup(B,B,2)+cup(B,B.d(),3)+cup(w.lift(),B),T


def balanced(items):
    items=list(items)
    while len(items)>1: items=[items[i]+items[i+1] if i+1<len(items) else items[i] for i in range(0,len(items),2)]
    return items[0] if items else C(6)

def residual(U,W,S):
    A=U.d();B=beta_open(U)
    f={r'\check n_3':U,r'd\check n_3':A,r'\omega_2':W,r's_1':S}
    mixed=balanced(op(word,*(f[a]for a in args))for word,args in oldmixed)
    nf={'u':U,'A':A,'w':W,'s':S}
    K=balanced(op(row['word'],*(nf[a]for a in row['inputs']))for row in rows)
    Q=cup(B,beta_open(A),3).scaled(-1)
    Q=Q-cup(A.lift(),U.lift(),1)+cup(U.lift(),A.lift(),1)
    old,_=Gamma(U,W,S)
    return old+mixed.lift().scaled(2)-J(U,W,S)-K.lift().scaled(2)-Q-ds(R0(U,W,S),S)-cup(S,kappa(U,W,S)).lift().scaled(2)
start=time.monotonic();top=tuple(range(7));scalars=[]
for i in range(16):
    u=random_cochain(3,6);w=random_cochain(1,6).d();s=random_cochain(0,6).d()
    value=residual(u,w,s)(top)%4
    assert value==0,(i,value)
    scalars.append(value)
# Exact coefficient identity, keeping every open u face independent.
sys.path.insert(0,str(PUBLIC/'formulas/publication_source/joint'))
import symbolic_lazy
symbolic_lazy.PREC=8
from symbolic_lazy import Bit,Z
from itertools import combinations
original_scaled=C.scaled
def scaled_mod4(self,k):
    if k==2 and hasattr(self,'_binary_origin'):
        origin=self._binary_origin
        return C(self.deg,fun=lambda f:Z({m:2 for m in Bit.cast(origin(f)).t},4),mod=None)
    return original_scaled(self,k)
C.scaled=scaled_mod4
variables=[]
def free(d,name,faces):
    vals={}
    for face in faces:
        vals[face]=Bit.var(len(variables));variables.append({'field':name,'face':face})
    return C(d,values=vals)
u=free(3,'u',combinations(top,4))
w=free(1,'w_potential',combinations(range(1,7),2)).d()
s=free(0,'s_potential',[(i,)for i in range(1,7)]).d()
for face in combinations(top,5):
    assert not Bit.cast((beta_open(u).reduce(2)+sq(u,1))(face))
r=residual(u,w,s)(top)%4
open_variables=len(variables)
closed_u=free(2,'closed_u_potential',combinations(range(1,7),3)).d()
closed_fields={'u':closed_u,'A':closed_u.d(),'w':w,'s':s}
closed_value=Bit.cast(balanced(op(row['word'],*(closed_fields[x]for x in row['inputs']))for row in rows)(top))
assert not closed_value
report={'status':'PASS'if not r else'FAIL','scalar_cases':len(scalars),'symbolic_variables':open_variables,'symbolic_residual_terms':len(r.t),'open_bockstein_equals_Sq1_all_faces':True,'closed_restriction_independent_variables':41,'closed_restriction_residual_terms':len(closed_value.t),'reader_relative_blocks':len(relative_blocks),'reader_relative_coefficients_equal_JSON':True,'reader_phase_words_equal_verified_dictionary':True,'new_MS_terms':len(rows),'construction_pure_MS_terms':85,'construction_mixed_MS_terms':len(oldmixed),'scope':'Exact unrestricted open-u source identity, all closed backgrounds, modulo one. Original mixed quadratic and carry terms occur unchanged on both sides.','seconds':time.monotonic()-start}

print(json.dumps(report),flush=True)
assert not r
