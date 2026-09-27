"""Derive the exact full-tower bridge between pip n=0 and closed-MC CA.

The universal4cochain D(s,B) is quarter-valued. The complete phase shift
is D+lift(Sq2 B)/4+s*C/2, proved on32768 local lower simplices and checked
on128 complete legal towers. No collaborator code or SGanswer is imported.
"""
import sys,json,time,random
from pathlib import Path
from itertools import combinations
from functools import lru_cache
import numpy as np
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
(root/'runs/formula_audit').mkdir(parents=True,exist_ok=True)
from fspt.formulas import evaluate,formula
program=json.loads((root/'gap/pip_o5_program.json').read_text())
def native(fields,face):
 vals=[]
 for item in program['program']:
  op=item[0]
  if op=='const':v=item[1]
  elif op=='field':v=fields[item[1]](tuple(face[i] for i in item[2]))
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
from fractions import Fraction
from fspt.formulas_pip_compile import evaluate_program
from fspt.formulas_fast_compile import compile_expression
B,output,active=compile_expression(formula('obstruction',2),('w',))
mcprogram={'program':B.nodes,'output':output}
pipprogram=program
choices=np.arange(1024,dtype=np.int64);rows=[]
for sm in range(32):
 eps=[0]+[(sm>>i)&1 for i in range(5)]
 s=lambda f:(eps[f[0]]+eps[f[1]])%2
 table={(0,)+f:(choices>>i)&1 for i,f in enumerate(combinations(range(1,6),2))}
 def b(f):
  if len(set(f))<3:return 0
  if 0 in f:return table[f]
  return sum(table[(0,)+f[:j]+f[j+1:]] for j in range(3))%2
 def Q(f):return (b(f[:3])*b(f[2:])+s(f[:2])*((sum((-1)**j*b(f[1:][:j]+f[1:][j+1:]) for j in range(4))//2)%2))%2
 def square(f):return b(f[:3])*b(f[2:])
 f=tuple(range(6));quarterdelta=((1-2*s(f[:2]))*square(f[1:])+sum((-1)**j*square(f[:j]+f[j+1:]) for j in range(1,6)))
 fields={'n':lambda f:0,'b':b,'a':b,'c':lambda f:0,'s':s}
 program=pipprogram;v=native(fields,f)
 program=mcprogram;w=native(fields,f)*2
 rhs=(v-w-4*quarterdelta-8*s(f[:2])*Q(f[1:]))%16
 rows.append(rhs)
np.save(root/'runs/formula_audit/pip_zero_mc_difference.npy',np.array(rows))
print('generated zero-MC comparison')

rhs=np.array(rows)
choices=np.arange(1024,dtype=np.int64);allkeys=[];signs=[]
for sm in range(32):
 eps=[0]+[(sm>>i)&1 for i in range(5)]
 s=lambda f:(eps[f[0]]+eps[f[1]])%2 if f[0]!=f[1] else 0
 table={(0,)+f:(choices>>i)&1 for i,f in enumerate(combinations(range(1,6),2))}
 def b(f):
  if len(set(f))<3:return 0
  if 0 in f:return table[f]
  return ((0%2)*s((0,f[0]))*s((f[0],f[1]))*s((f[1],f[2]))+sum(table[(0,)+f[:i]+f[i+1:]] for i in range(3)))%2
 ks=[]
 for omit in range(6):
  f=tuple(i for i in range(6) if i!=omit)
  key=sum(s((f[0],f[i]))<<(i-1) for i in range(1,5))
  key=key+sum(b((f[0],f[i],f[j]))<<(4+r) for r,(i,j) in enumerate(combinations(range(1,5),2)))
  ks.append(key)
 allkeys.append(np.array(ks).T);signs.append([(-1)**s((0,1)), -1,1,-1,1,-1])
allkeys=np.array(allkeys);signs=np.array(signs)

normal=[]
for sm in range(16):
 eps=[0]+[(sm>>i)&1 for i in range(4)]
 s=lambda f:(eps[f[0]]+eps[f[1]])%2 if f[0]!=f[1] else 0
 for bm in range(64):
  table={(0,)+f:(bm>>i)&1 for i,f in enumerate(combinations(range(1,5),2))}
  def b(f):
   if len(set(f))<3:return 0
   if 0 in f:return table[f]
   return ((0%2)*s((0,f[0]))*s((f[0],f[1]))*s((f[1],f[2]))+sum(table[(0,)+f[:i]+f[i+1:]] for i in range(3)))%2
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
  (root/'runs/formula_audit/pip_zero_mc_coordinate.json').write_text(json.dumps(result)+'\n')
  break
 except ValueError as error:print('FAILED',mod,str(error)[:300],flush=True)

sys.path.insert(0,str(root/'vendor/p_ip_d4_normalized_package/code'))
import cochains as q
program=json.loads((root/'gap/pip_o5_program.json').read_text());data=json.loads((root/'runs/formula_audit/pip_zero_mc_coordinate.json').read_text())
for seed in range(128):
 random.seed(67434+seed);s=q.random_cochain(0,5).d();b=q.random_cochain(1,5).d();n=q.C(1,mod=None);w=q.C(2)
 Q=q.parity(n,b,w,s);c=q.primitive(Q)+q.random_cochain(2,5).d()
 def T(f):
  key=sum(s((f[0],f[i]))<<(i-1) for i in range(1,5))
  key+=sum(b((f[0],f[i],f[j]))<<(4+r) for r,(i,j) in enumerate(combinations(range(1,5),2)))
  return Fraction(data['numerators'][key],data['modulus'])+Fraction(b(f[:3])*b(f[2:]),4)+Fraction(s(f[:2])*c(f[1:]),2)
 x=Fraction(evaluate_program(program,{'n':n,'b':b,'c':c,'s':s}),16)
 y=Fraction(evaluate(formula('obstruction',2),{'a':b,'c':c,'s':s,'w':w}),8)
 delta=q.ds(q.C(4,fun=T,mod=None),s)(tuple(range(6)))
 assert (x-y-delta)%1==0,(seed,x,y,delta)
print('PASS128 complete-tower pip n0 vs CA Majorana coordinate identity')
