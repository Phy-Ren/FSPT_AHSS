"""Audit-only derivation of the n=s upper-coordinate coboundary.

The reference source is a mathematical oracle at build time. Production
imports none of its modules. All32768 local lower states are enumerated.
"""
import sys,time,json
from pathlib import Path
from itertools import combinations
from fractions import Fraction
import numpy as np
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
(root/'runs/formula_audit').mkdir(parents=True,exist_ok=True)
from fspt.formulas import evaluate,formula,pip_cf_coordinate
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--reference-root',type=Path,required=True)
parser.add_argument('--verify-current',action='store_true',help='Verify the stored historical base D4 plus the explicit corrected-AW s^4/4 term; do not solve or overwrite it')
args=parser.parse_args()
sys.path.insert(0,str(args.reference_root/'python/stacking_model'));sys.path.insert(0,str(args.reference_root/'python'))
import upper_phase_diagnostic as up,cochain_tools as ct
p=up.p

def divide(c,k,name=''):
 def value(z):
  v=c(z)
  if np.any(v%k):raise ArithmeticError((name,v))
  return v//k
 return p.Cochain(c.degree,value)
p.divide=divide

def word_op(word,*cochains,integral_index=None):
 degree=sum(c.degree for c in cochains)-(len(word)-len(cochains));terms=ct.cut_terms(word,tuple(c.degree for c in cochains),integral_index)
 def value(z):
  out=0
  for faces,weight in terms:
   v=weight
   for c,f in zip(cochains,faces):v=v*c(tuple(z[j] for j in f))
   out=out+v
  return out if integral_index is not None else out%2
 return p.Cochain(degree,value)
ct.word_op=word_op;p.word_op=word_op

def chi(c):
 faces,masks=p.chi_anf(c.degree)
 def value(z):
  active=np.uint64(0)
  for i,f in enumerate(faces):active=active+(np.asarray(c(tuple(z[j] for j in f)),dtype=np.uint64)<<np.uint64(i))
  out=0
  for mask in masks:out=out+((active&np.uint64(mask))==np.uint64(mask)).astype(np.int64)
  return out%2
 return p.Cochain(c.degree+3,value)
p.chi=chi
program=json.loads((root/'gap/pip_o5_program.json').read_text())
def native(fields):
 vals=[]
 for item in program['program']:
  op=item[0]
  if op=='const':v=item[1]
  elif op=='field':v=fields[item[1]](tuple(item[2]))
  elif op=='add':v=vals[item[1]]+vals[item[2]]
  elif op=='mul':v=vals[item[1]]*vals[item[2]]
  elif op=='mod':v=vals[item[1]]%item[2]
  elif op=='floor':v=vals[item[1]]//item[2]
  elif op=='bit':v=(vals[item[1]]>>item[2])&1
  elif op=='div':
   v=vals[item[1]]
   if np.any(v%item[2]):raise ArithmeticError('native division')
   v=v//item[2]
  vals.append(v)
 return vals[program['output']]
N=5;choices=np.arange(1024,dtype=np.int64)
rows=[]
for sm in range(32):
 start=time.time();eps=[0]+[(sm>>i)&1 for i in range(N)]
 s=lambda f:(eps[f[0]]+eps[f[1]])%2 if f[0]!=f[1] else 0
 table={(0,)+f:(choices>>i)&1 for i,f in enumerate(combinations(range(1,N+1),2))}
 def b(f):
  if len(set(f))<3:return 0
  if 0 in f:return table[f]
  return (s((0,f[0]))*s((f[0],f[1]))*s((f[1],f[2]))+sum(table[(0,)+f[:i]+f[i+1:]] for i in range(3)))%2
 fields={'n':s,'b':b,'c':lambda f:0,'s':s,'w':lambda f:0}
 def lam(f):
  x,y,z=b((f[0],f[1],f[2])),b((f[0],f[1],f[3])),b((f[0],f[2],f[3]))
  return (y+x*y+x*z+y*z)%2
 l=p.Cochain(3,lam);sn=p.Cochain(1,s);bn=p.Cochain(2,b)
 q=p.Cochain(4,lambda f:evaluate(formula('pip_parity',1),fields,f))
 phase=up.production_phase(1,sn,bn,l,sn,p.zero(2))(tuple(range(6)))
 extra=p.cup(p.binary(p.differential(l)),q,3)(tuple(range(6)))
 out=16*phase-native(fields)+8*extra
 out=np.asarray([int(x) if Fraction(x).denominator==1 else (_ for _ in ()).throw(ValueError(x)) for x in out],dtype=np.int64)%16
 rows.append(out)
 print(sm,'values',np.unique(out),'sec',time.time()-start,flush=True)
np.save(root/'runs/formula_audit/pip_upper_difference.npy',np.array(rows))

# Solve exact signed coboundary equations over Z/16.
rhs=np.array(rows)
choices=np.arange(1024,dtype=np.int64);allkeys=[];signs=[]
for sm in range(32):
 eps=[0]+[(sm>>i)&1 for i in range(5)]
 s=lambda f:(eps[f[0]]+eps[f[1]])%2 if f[0]!=f[1] else 0
 table={(0,)+f:(choices>>i)&1 for i,f in enumerate(combinations(range(1,6),2))}
 def b(f):
  if len(set(f))<3:return 0
  if 0 in f:return table[f]
  return (s((0,f[0]))*s((f[0],f[1]))*s((f[1],f[2]))+sum(table[(0,)+f[:i]+f[i+1:]] for i in range(3)))%2
 ks=[]
 for omit in range(6):
  f=tuple(i for i in range(6) if i!=omit)
  key=sum(s((f[0],f[i]))<<(i-1) for i in range(1,5))
  key=key+sum(b((f[0],f[i],f[j]))<<(4+r) for r,(i,j) in enumerate(combinations(range(1,5),2)))
  ks.append(key)
 allkeys.append(np.array(ks).T);signs.append([(-1)**s((0,1)), -1,1,-1,1,-1])
allkeys=np.array(allkeys);signs=np.array(signs)

if args.verify_current:
 data=json.loads((root/'fspt/data/pip_upper_coordinate.json').read_text())
 arr=np.array(data['numerators'],dtype=np.int64)*(16//data['modulus'])
 for key in range(1024):
  eps=[0]+[(key>>i)&1 for i in range(4)]
  arr[key]=(arr[key]+4*np.prod([(eps[i]+eps[i+1])%2 for i in range(4)]))%16
 actual=np.sum(arr[allkeys]*signs[:,None,:],axis=2)%16
 assert np.array_equal(actual,rhs),('corrected unary dictionary',np.count_nonzero(actual-rhs))
 print('PASS32768 corrected-AW unary phase equations using stored D4+s4/4',flush=True)
 sys.exit(0)

normal=[]
for sm in range(16):
 eps=[0]+[(sm>>i)&1 for i in range(4)]
 s=lambda f:(eps[f[0]]+eps[f[1]])%2 if f[0]!=f[1] else 0
 for bm in range(64):
  table={(0,)+f:(bm>>i)&1 for i,f in enumerate(combinations(range(1,5),2))}
  def b(f):
   if len(set(f))<3:return 0
   if 0 in f:return table[f]
   return (s((0,f[0]))*s((f[0],f[1]))*s((f[1],f[2]))+sum(table[(0,)+f[:i]+f[i+1:]] for i in range(3)))%2
  for collapse in range(4):
   if s((collapse,collapse+1)):continue
   if all(b(f)==b(tuple(collapse if x==collapse+1 else x for x in f)) for f in combinations(range(5),3)):
    normal.append(sm+(bm<<4));break

def solve(rows,modulus,depth=0):
 piv={};remaining=[]
 for data,value in rows:
  data={int(k):int(v)%modulus for k,v in data.items() if v%modulus};value=int(value)%modulus
  while True:
   matches=[j for j in data if j in piv]
   if not matches:break
   j=min(matches);factor=data.pop(j);row,v=piv[j];value=(value-factor*v)%modulus
   for k,x in row.items():
    if k==j:continue
    z=(data.get(k,0)-factor*x)%modulus
    if z:data[k]=z
    else:data.pop(k,None)
  odd=[j for j,v in data.items() if v%2]
  if odd:
   j=min(odd);inv=pow(data[j],-1,modulus)
   piv[j]=({k:(v*inv)%modulus for k,v in data.items()},(value*inv)%modulus)
  elif value%2:
   raise ValueError(('inconsistent',modulus,len(piv),len(remaining),data,value))
  elif data:
   remaining.append(({k:v//2 for k,v in data.items()},value//2))
  elif value:
   raise ValueError(('nonzero empty',modulus,value))
 print('level',depth,'mod',modulus,'pivots',len(piv),'remaining',len(remaining),flush=True)
 # Newly added pivots must also be eliminated from early even rows.
 if remaining:
  restored=[({k:2*v for k,v in d.items()},2*y) for d,y in remaining]
  reduced=[]
  for data,value in restored:
   for j,(row,v) in piv.items():
    if j not in data:continue
    factor=data.pop(j);value=(value-factor*v)%modulus
    for k,x in row.items():
     if k==j:continue
     z=(data.get(k,0)-factor*x)%modulus
     if z:data[k]=z
     else:data.pop(k,None)
   if any(v%2 for v in data.values()) or value%2:raise ValueError('unexpectedodd')
   reduced.append(({k:v//2 for k,v in data.items()},value//2))
  sol=solve(reduced,modulus//2,depth+1) if modulus>2 else {}
 else:sol={}
 for j,(row,value) in reversed(list(piv.items())):
  sol[j]=(value-sum(v*sol.get(k,0) for k,v in row.items() if k!=j))%modulus
 return sol
for mod,divisor in [(4,4),(8,2),(16,1)]:
 if np.any(rhs%divisor):continue
 rows=[]
 for sm in range(32):
  for bm in range(1024):
   d={}
   for k,sg in zip(allkeys[sm,bm],signs[sm]):d[int(k)]=d.get(int(k),0)+int(sg)
   rows.append((d,int(rhs[sm,bm])//divisor))
 rows.extend(({key:1},0) for key in normal)
 try:
  start=time.time();solution=solve(rows,mod);arr=np.array([solution.get(i,0) for i in range(1024)],dtype=np.int64)
  actual=np.sum(arr[allkeys]*signs[:,None,:],axis=2)%mod
  print('RESULT',mod,np.count_nonzero(actual-rhs//divisor),time.time()-start,flush=True)
  if np.any(actual!=rhs//divisor):raise AssertionError('verification')
  result={'modulus':mod,'numerators':arr.tolist(),'equations':32768,'normalized_states':len(normal)}
  (root/'runs/formula_audit/pip_upper_coordinate.json').write_text(json.dumps(result)+'\n')
  break
 except ValueError as error:print('FAILED',mod,str(error)[:300],flush=True)
