"""Derive the normalized 2s-to-zero cylinder gauge and verify its lower tower.

Uses only the independently compiled supplied O5 and cochain prism; no
reference implementation or target-group result is imported.
"""
import sys,json,time
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
def setup(N,sm,choices):
 eps=[0]+[(sm>>i)&1 for i in range(N)]
 def base_s(f):return (eps[f[0]]+eps[f[1]])%2
 table={(0,)+f:(choices>>i)&1 for i,f in enumerate(combinations(range(1,N+1),3))}
 def base_c(f):
  if len(set(f))!=len(f):return 0
  if 0 in f:return table[f]
  return sum(table[(0,)+f[:j]+f[j+1:]] for j in range(4))%2
 def s(f):return base_s(tuple(x//2 for x in f))
 def n(f):return 2*s(f)+(f[1]%2-f[0]%2)-2*s(f)*(f[1]%2)
 def b(f):return s(f[:2])*(f[1]%2)*((f[2]+f[1])%2)
 fields={'n':n,'b':b,'w':lambda f:0,'s':s}
 @lru_cache(None)
 def Q(f):return evaluate(formula('pip_parity',1),fields,f)
 @lru_cache(None)
 def KQ(f):return sum(Q(tuple(2*(x//2) for x in f[:j+1])+f[j:]) for j in range(len(f)))%2
 def c(f):
  if len(set(f))!=len(f):return 0
  return (base_c(tuple(x//2 for x in f))+KQ(f))%2
 fields['c']=c
 return fields,Q,KQ,base_s,base_c
rows=[];cfrows=[]
for sm in range(16):
 fields,Q,KQ,_,_=setup(4,sm,np.arange(16,dtype=np.int64))
 ans=np.zeros(16,dtype=np.int64)
 for j in range(5):
  face=tuple(2*i for i in range(j+1))+tuple(2*i+1 for i in range(j,5))
  ans=ans+(-1)**j*native(fields,face)
 rows.append(ans%16)
 # check lower equations on all prism faces
 for j in range(5):
  z=tuple(2*i for i in range(j+1))+tuple(2*i+1 for i in range(j,5))
  for f in combinations(z,4):
   dn=sum(fields['b'](f[:i]+f[i+1:]) for i in range(4))%2
   expected=evaluate(formula('pip_majorana',1),fields,f)
   assert dn==expected,('B',f,dn,expected)
  for f in combinations(z,5):
   dc=sum(fields['c'](f[:i]+f[i+1:]) for i in range(5))%2
   assert np.all(dc==Q(f)),('C',f,dc,Q(f))
 print('gauge',sm,np.unique(ans%16),flush=True)
for sm in range(8):
 _,Q,KQ,_,_=setup(3,sm,np.array([0],dtype=np.int64))
 cfrows.append(KQ(tuple(2*i+1 for i in range(4))))
result={'modulus':16,'numerators':np.array(rows).T.reshape(-1).tolist(),'cf_shift':cfrows,'states':256}
(root/'runs/formula_audit/pip_integer_gauge.json').write_text(json.dumps(result)+'\n')
print('CF',cfrows)

# Independent universal five-simplex verification of the resulting local phase.
d=json.loads((root/'runs/formula_audit/pip_integer_gauge.json').read_text());arr=np.array(d['numerators'])
count=0
for sm in range(32):
 fields,Q,KQ,s,c=setup(5,sm,np.arange(1024,dtype=np.int64))
 def phase(f):
  key=sum(s((f[0],f[i]))<<(i-1) for i in range(1,5))
  key+=sum(c((f[0],f[i],f[j],f[k]))<<(4+r) for r,(i,j,k) in enumerate(combinations(range(1,5),3)))
  return arr[key]
 delta=(-1)**s((0,1))*phase((1,2,3,4,5))+sum((-1)**i*phase(tuple(j for j in range(6) if j!=i)) for i in range(1,6))
 cube=lambda f:s(f[:2])*s(f[1:3])*s(f[2:])
 fields0={'n':lambda f:2*s(f),'b':lambda f:0,'c':c,'s':s}
 fields1={'n':lambda f:0,'b':lambda f:0,'c':lambda f:(c(f)+cube(f))%2,'s':s}
 expected=native(fields1,tuple(range(6)))-native(fields0,tuple(range(6)))
 assert np.all((delta-expected)%16==0),(sm,delta%16,expected%16)
 count+=1024
print('PASS integer cylinder gauge on',count,'universal legal5simplex states')
# ANF for half-integer remaining binary term
vals=np.array(d['numerators']);truth=[]
for key,v in enumerate(vals):
 sm=key&15;eps=[0]+[(sm>>i)&1 for i in range(4)];s4=np.prod([(eps[i]+eps[i+1])%2 for i in range(4)])
 x=(v-13*s4)%16
 assert x%8==0
 truth.append(int(x//8))
for j in range(8):
 for i in range(256):
  if i&(1<<j):truth[i]^=truth[i^(1<<j)]
print('GAUGE ANF', [i for i,x in enumerate(truth) if x])
