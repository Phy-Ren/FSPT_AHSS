"""Exact raw occurrence census by a weighted expression DAG.

No index set or y6 is assigned the cost one. Nonlinear canonical lifts,
standard Bocksteins on displayed sums, and exact numerator divisions keep
an explicit interior census; those interiors are never distributed as if
linear. Counts precede typed normalization/physical-face cancellation.
"""
from pathlib import Path
from itertools import product,combinations
from math import comb
import json,hashlib,sys
CURRENT="--current" in sys.argv
HERE=Path(__file__).resolve().parent
WEIGHTS=json.loads((HERE/'FOUR_DIMENSIONAL_WEIGHT_DATA.json').read_text())
class S:
 def __init__(self,M=0,C=0,F=0,topC=0,topF=0):self.M=M;self.C=C;self.F=F;self.topC=topC;self.topF=topF
 def __add__(self,b):return S(self.M+b.M,self.C+b.C,self.F+b.F,self.topC+b.topC,self.topF+b.topF)
 def __neg__(self):return self
 def __sub__(self,b):return self+b
 def scale(self,c):return self if c else S()
 def norm(self,*args):return self
 def repeat(self,n):return S(self.M*n,self.C*n,self.F*n,self.topC*n,self.topF*n)
 def dump(self):return {'cochain_atoms':self.C,'face_binomial_monomials':self.F,'total_raw_atom_occurrences':self.C+self.F,'outer_monomial_occurrences':self.M}
P=S
def atom(name):return S(1)
def prod(vals):
 z=1
 for v in vals:z*=v
 return z
def op(name,*args):
 M=prod(x.M for x in args);C=M;F=0
 for j,x in enumerate(args):
  weight=prod(y.M for k,y in enumerate(args)if k!=j);C+=(x.C-x.topC)*weight;F+=(x.F-x.topF)*weight
 return S(M,C,F,M,0)
def cup(a,b,i=0):return op('cup',a,b)
def ms(word,*args):return op('MS',*args)
def d(a):return op('d',a)
def barrier(name,a,binary=False):return S(1,a.C,a.F,0,0)
def bar(a):return barrier('bar',a)
def lift(a):return barrier('lift',a)
def second(a):return barrier('second',a)
def beta(a):return barrier('standard beta',a)
from fractions import Fraction as F
# Identical visible formulas, now interpreted in the exact count semiring.
src=(HERE/'four_dimensional_formula_definitions.py').read_text()
if CURRENT:
 src=src.replace('cup(s,cup(d(u),v,4)+cup(u+v,t,3))','cup(s,cup(u+v,t,3))')
 src=src.replace('+cup(cup(b,b),cup(W,a),4)+cup(d(t),cup(W,a+b),4)','+cup(cup(W,a,2),b+cup(a,b,2))+cup(cup(W,b,2),a)')
exec(src)
if CURRENT:
 rows=WEIGHTS['current_majorana_rows']
 assert len(rows)==1090
# Independent explicit AST baseline checks for the repeated visible polynomials.
assert (Vg.C,Vm.C,Vp.C)==(9,163,89),(Vg.dump(),Vm.dump(),Vp.dump())
assert (Eg.C,Em.C,Ep.C)==(2,5 if CURRENT else 6,27)
assert (Xi.C,kappa.C)==(13,5)
# Fully expanded R7 in SOURCE_OPERATIONS. Integer canonical barriers retained.
bsint=atom('beta_s W');betaA=beta(A);barbetaA=bar(betaA);plusbetaA=barrier('beta-plus carry: (beta A+bar beta A)/2',betaA+barbetaA)
core=(cup(w,Bp)+cup(Bp,Bp,2)+cup(betaA,Bp,3)-cup(Bp,cup(bsint,n),3)).scale(4)
core=core-lift(Cartan).scale(4)+cup(Ptw,n)+cup(W,cup(n,n)).scale(2)+cup(w,lift(A)).scale(4)+lift(cup(A,atom('bar beta w')+cup(s,w),1)).scale(8)
M7=ms('123134343',w,w,A,A)
table={'x4_words':WEIGHTS['source_adem_words']}
for word in table['x4_words']:M7=M7+ms(word,A,A,A,A)
M7=(M7+cup(cup(A,A,2),cup(w,A),5)+cup(cup(A,A,2),cup(s,barbetaA),5)+cup(cup(w,A),cup(s,barbetaA),5)
 +ms('123143434',s,s,barbetaA,barbetaA)+cup(cup(w,s,1),barbetaA)+cup(s,cup(A,A,2))+cup(cup(s,s),plusbetaA))
closed_source=cup(A,A,2)+cup(s,cup(A,A,3))+cup(w,A)
Rnum=d(core)+lift(cup(Xi,Xi,3)+cup(closed_source,Xi,4)+cup(w,Xi)).scale(8)+M7.scale(8)+(cup(w,betaA)+cup(betaA,betaA,3)).scale(4)
R=barrier('whole exactly divisible numerator /8 then parity',Rnum)
# Expand all numerical coordinate differences by finite Vandermonde sums.
AW_COUNT=0
for block in WEIGHTS['source_numerical_blocks']:
 for mask,background_mask in block['terms']:
  mask=int(mask);multiplicity=1
  for slot,(row_r,row_t)in enumerate(combinations(range(1,block['j']+1),2)):
   exponent=(mask>>(4*slot))&15
   if exponent and row_t>row_r+1:multiplicity*=exponent+1
  for slot,(row_r,row_t)in enumerate(combinations(range(1,block['k']+1),2)):
   if (int(background_mask)>>slot)&1 and row_t>row_r+1:multiplicity*=2
  AW_COUNT+=multiplicity
assert AW_COUNT==5602

# 1086 explicit three-factor source grids, plus every physical AW binomial row.
Y=S(1086+AW_COUNT,R.C*1086,R.F*1086+AW_COUNT,topF=AW_COUNT)

COLORS=(1,3,2)
def add(xs):
 z=S()
 for x in xs:z=z+x
 return z
def kernel(p):
 # p is the exact raw number of pip-origin face-product terms in each decoded u.
 ug={1:atom('u'),3:S(),2:S(p,F=p,topF=p)};vg={1:atom('v'),3:S(),2:S(p,F=p,topF=p)}
 cols=[(ug,n,a),(vg,m,b),({1:ug[1]+vg[1],3:S(),2:ug[2]+vg[2]+t},N,Na)]
 Bs=[];Bet=[];Ks=[];source=[];V={};l={};e={}
 for ur,nj,aj in cols:
  Aj=cup(aj,aj)+cup(W,aj);K=(lift(Aj)-cup(nj,nj)-cup(W,nj)).scale(F(1,2))
  be={1:beta(ur[1]),2:beta(ur[2]),3:-d(cup(ur[1],ur[2],3))+cup(bar(d(ur[1])),bar(d(ur[2])),4)}
  B={1:be[1],3:be[3],2:be[2]+K};Bs.append(B);Bet.append(be);Ks.append(K)
  kg=cup(ur[1],ur[1],1)+cup(s,cup(ur[1],ur[1],2))+cup(w,ur[1])
  km=(cup(ur[1],ur[2],1)+cup(ur[2],ur[1],1)+cup(ur[1],Aj,2)+cup(s,cup(ur[1],ur[2],2)+cup(ur[2],ur[1],2)+cup(ur[1],Aj,3)))
  kp=cup(ur[2],ur[2],1)+cup(ur[2],Aj,2)+cup(s,cup(ur[2],ur[2],2)+cup(ur[2],Aj,3))+cup(w,ur[2])
  X=psi(aj,atom('digit nj'));kap={1:kg,3:km,2:kp};source.append({1:kg,3:km,2:kp+X})
  T={r:S()for r in COLORS}
  # All 1176 specified ordinary words and all their finite input-origin choices.
  for row in rows:
   options=[]
   for x in row['inputs']:
    options.append([(1,ur[1]),(2,ur[2])]if x=='u'else[(2,Aj)]if x=='A'else[(0,w if x=='w'else s)])
   for choice in product(*options):
    color=0
    for rr,_ in choice:color|=rr
    T[color]=T[color]+ms(row['word'],*(xx for rr,xx in choice))
  carries={1:second(be[1]),2:second(be[2]),3:second(be[3])+cup(bar(be[1]),bar(be[2]),4)+cup(bar(be[1]),bar(be[3]),4)+cup(bar(be[2]),bar(be[3]),4)}
  for r0 in COLORS:T[r0]=T[r0]+cup(cup(s,s),carries[r0])
  bgexpr=atom('bar beta w')+cup(s,w)
  H={1:T[1]+cup(ur[1],bgexpr),3:T[3]+cup(kg+km,X,4)+cup(bar(be[1])+bar(be[3]),bar(K),2)+cup(s,cup(bar(be[1])+bar(be[3]),bar(K),3))+cup(aj,bar(B[1])+bar(B[3])),
     2:T[2]+cup(ur[2],bgexpr)+cup(kp,X,4)+Y+cup(bar(be[2]),bar(K),2)+cup(s,cup(bar(be[2]),bar(K),3))+cup(aj,bar(B[2]))+cup(cup(aj,bs,1),aj)}
  source[-1]['H']=H
 B,Bprime=Bs[:2]
 for r0 in COLORS:
  ll=S()
  for i,j in product(COLORS,repeat=2):
   if i|j==r0:ll=ll+cup(ug[i],vg[j],3)
  for i in COLORS:
   if i|2==r0:ll=ll+cup(ug[i]+vg[i],t,3)
  if r0==2:ll=ll+lp
  l[r0]=ll
 for r0 in COLORS:
  z=S()
  for i,j in product(COLORS,repeat=2):
   if i|j!=r0:continue
   D=d(l[j])+(cup(b,a)if j==2 else S())
   z=z+cup(bar(B[i]),bar(Bprime[j]),3)+cup(d(bar(B[i])),bar(Bprime[j]),4)+cup(bar(B[i])+bar(Bprime[i]),D,3)+cup(d(bar(B[i]))+d(bar(Bprime[i])),D,4)+cup(l[i],l[j],1)+cup(l[i],d(l[j]),2)
  for j in COLORS:
   if j|2==r0:z=z+cup(cup(b,a),d(l[j]),3)
  z=z+cup(w,l[r0])
  for i in COLORS:
   if i|2==r0:z=z+cup(vg[i],a)+cup(b,ug[i])
  if r0==2:z=z+cup(bs2+bs,r)+ms('1231343',b,b,a,a)+cup(cup(W,b,1),a)+cup(k,cup(a,a,1))+cup(cup(s,b),h)+cup(cup(s,cup(b,s,1)),a)
  V[r0]=z
 def Q(x):return cup(x,x,2)+cup(x,d(x),3)
 def C(x,y):return cup(x,y,2)+cup(y,x,2)+cup(x,d(y),3)+cup(y,d(x),3)
 D={}
 for r0 in COLORS:
  z=add(Q(Bj[r0])+cup(w,Bj[r0])for Bj in Bs)-op('d_s',lift(V[r0]))
  if r0==3:
   for Bj in Bs:z=z+C(Bj[1],Bj[3])+C(Bj[1],Bj[2])+C(Bj[3],Bj[2])
  if r0==2:z=z+lift(Cartan).repeat(3)+cup(W,cup(m,n))+cup(bsint,cup(n,m,1))
  D[r0]=z
 carry={1:second(D[1]),2:second(D[2]),3:second(D[3])+cup(bar(D[1]),bar(D[3]),6)+cup(bar(D[1]),bar(D[2]),6)+cup(bar(D[3]),bar(D[2]),6)+d(cup(V[1],V[3],5)+cup(V[1],V[2],5)+cup(V[3],V[2],5))}
 # Actual E4+ab coefficient, with the complete explicit pure polynomial.
 for r0 in COLORS:
  z=S()
  for i,j in product(COLORS,repeat=2):
   if i|j==r0:z=z+cup(ug[i],vg[j],2)+cup(s,cup(ug[i],vg[j],3))
  for j in COLORS:
   if 2|j==r0:z=z+cup(A,vg[j],3)+(S()if CURRENT else cup(s,cup(A,vg[j],4)))
  for i in COLORS:
   if i|2==r0:z=z+cup(ug[i]+vg[i],t,2)+cup(s,cup(ug[i]+vg[i],t,3))
  if r0==2:z=z+Ep+cup(a,b)
  e[r0]=z
 rho={}
 for r0 in COLORS:
  z=cup(w,e[r0])
  for i,j in product(COLORS,repeat=2):
   if i|j!=r0:continue
   z=z+cup(e[i],e[j],2)+cup(e[i],d(e[j]),3)+cup(source[0][i],source[1][j],4)+cup(source[0][i]+source[1][i],e[j],3)+cup(e[i],source[0][j]+source[1][j],3)
  z=z+add(ss['H'][r0]for ss in source)+carry[r0]
  if r0==2:z=z+cup(W,d(t))+cup(bs,t)
  rho[r0]=z
 return rho

# Exact raw tensor expansion of q=x-y by Vandermonde and the displayed origin bracket.
td={key:{'binomial_coefficients':rows}for key,rows in WEIGHTS['tensor_binomial_rows'].items()}
def tensors(p):
 counts={1:0,3:0,2:0}
 for side,values in td.items():
  for ii,jj,kk,ll,ee in values['binomial_coefficients']:
   if not ee:counts[2]+=kk+1
   else:counts[3]+=kk+1;counts[2]+=(kk+1)*(p+(1 if side=='23' else 0))
 # Ls expands into twelve additive ordinary cup terms.
 return {1:S(),3:S(counts[3],F=counts[3],topF=counts[3]),2:S(counts[2]+12,C=12,F=counts[2],topC=12,topF=counts[2])}

paths={'depths':[{'depth':j,'indices_after_exact_equal_root_branch_cancellation':count*2**j}for j,count in enumerate((1,116,4176,41760,83520,0))]};tot={r:S()for r in COLORS};unpruned={r:S()for r in COLORS};weighted=[]
for row in paths['depths']:
 J=row['depth'];gridseq=row['indices_after_exact_equal_root_branch_cancellation']//2**J
 for ones in range(J+1):
  branchmult=comb(J,ones);p=2+2*ones;rho=kernel(p);ten=tensors(p)
  multiplier=gridseq*branchmult;rawmult=116**J*branchmult
  for r0 in COLORS:
   term=rho[r0].repeat(358)+ten[r0];tot[r0]=tot[r0]+term.repeat(multiplier);unpruned[r0]=unpruned[r0]+term.repeat(rawmult)
  weighted.append({'depth':J,'epsilon_ones':ones,'raw_pip_face_terms_per_input':p,'pruned_path_occurrences':multiplier,'kernel_per_final_grid':{str(r):rho[r].dump()for r in COLORS},'tensor_per_path':{str(r):ten[r].dump()for r in COLORS}})
result={'status':'EXACT_RAW_WEIGHTED_DAG_OCCURRENCE_CENSUS','version':'reduced_1090_and_lower_E4'if CURRENT else 'baseline_1176' ,'boundary':'A writable ordinary cup/MS/differential summand counts one. Every y6/R7/M7/O/E/V/B/lambda and finite row set is expanded. Nonlinear canonical lifts, floor digits and standard Bocksteins on polynomial arguments keep explicit interiors, counted recursively per occurrence. Exact quotient linear numerators distribute. Signed physical n2 inputs and their standard digits/binomials remain typed scalar factors. Interval-cut scalar expansion and face degeneracy/coincidence cancellation are NOT applied to these cochain-level counts.','R7_numerator':Rnum.dump(),'y6_complete_raw':Y.dump(),'I5_raw':{str(r):unpruned[r].dump()for r in COLORS},'I5_after_proved_path_pruning':{str(r):tot[r].dump()for r in COLORS},'weighted_cases':weighted,'color_dictionary':{'1':'gamma','3':'gamma_psi','2':'psi'},'collected_final_scalar_count':None,'cautions':['Raw occurrence counts can be enormously larger than actual normalized nonzero expressions. They are neither computational costs nor lower bounds on a minimal formula.','Standard Bockstein arguments are counted with their displayed interiors, not expanded into omitted-face integer sums. This uses the shared permitted standard-operation boundary.','Source y6 uses the complete 1086-grid R7 bracket plus all 5602 Vandermonde physical binomial occurrences from the numerical table. It is never counted as one.','Path coefficients retain all p=2+2*epsilon_ones physical face terms even if particular maps degenerate or coincide; this is an exact pre-normalization occurrence census.']}
# Independently compare every derived per-kernel weight to the aggregate data.
aggregate=json.loads((HERE/'FOUR_DIMENSIONAL_COUNT_DATA.json').read_text())
expected=aggregate['current_kernel_by_epsilon_weight'if CURRENT else 'baseline_kernel_by_epsilon_weight']
for case in weighted:
 item=expected[str(case['epsilon_ones'])]
 assert case['kernel_per_final_grid']==item['kernel'],case
 assert case['tensor_per_path']==item['tensor'],case
assert Rnum.C==aggregate['source_residual_atoms']
check={'status':'PASS_REDERIVED_ALL_FORMULA_WEIGHTS','current':CURRENT,'source_residual_atoms':Rnum.C,'y6_raw_atoms':Y.C+Y.F,'weighted_cases':len(weighted),'source_word_rows':len(rows),'scope':'Every weight is rederived from the literal formula definitions and complete local coefficient rows; no private data or precomputed kernel weight is an input to the derivation. The adjacent aggregate weights are read only afterward for an exact comparison.'}
(HERE/('FOUR_DIMENSIONAL_WEIGHT_CHECK_CURRENT.json'if CURRENT else 'FOUR_DIMENSIONAL_WEIGHT_CHECK_BASELINE.json')).write_text(json.dumps(check,indent=2)+'\n')
print(json.dumps(check,indent=2))
