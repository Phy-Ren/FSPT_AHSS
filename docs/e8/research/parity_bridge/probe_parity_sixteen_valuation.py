"""Conservative 2-adic abstract interpretation of read-only parity DAGs.
A proved zero is universal for the substituted inputs; an unknown is not failure.
"""
from pathlib import Path
import json,hashlib,argparse
ap=argparse.ArgumentParser()
ap.add_argument("--public-reference",type=Path,default=Path("/home/xingyu/FSPT_AHSS_public"))
args=ap.parse_args()
ROOT=args.public_reference/'fspt/data/full_formula'
INF=10**9

def val(x):
 if not x:return INF
 return (abs(x)&-abs(x)).bit_length()-1

def audit(name):
 data=json.loads((ROOT/(name+'.json')).read_text());values=[];unproved=0;opcodes=set()
 for node in data['program']:
  op=node[0];opcodes.add(op)
  if op=='const': out=(val(node[1]),node[1])
  elif op=='field':
   if node[1] in ('n','m'):out=(4,None)
   elif node[1] in ('a','b','c','cp','y'):out=(INF,0)
   elif node[1] in ('w','s'):out=(0,None)
   else:raise ValueError(node)
  else:
   a,ca=values[node[1]]
   if op in ('add','mul'):
    b,cb=values[node[2]]
    if ca is not None and cb is not None:
     c=ca+cb if op=='add' else ca*cb;out=(val(c),c)
    elif op=='add':out=(min(a,b),None)
    elif ca==0 or cb==0:out=(INF,0)
    else:out=(min(INF,a+b),None)
   elif ca is not None:
    k=node[2]
    if op=='mod':c=ca%k
    elif op in ('floor','div'):
     if op=='div':assert ca%k==0,(name,node,ca)
     c=ca//k
    elif op=='bit':c=(ca>>k)&1
    else:raise ValueError(node)
    out=(val(c),c)
   elif op=='mod':
    k=node[2]
    out=(INF,0) if k&(k-1)==0 and a>=val(k) else (min(a,val(k)),None)
   elif op=='bit':out=(INF,0) if a>node[2] else (0,None)
   elif op in ('floor','div'):
    k=node[2]
    assert k>0
    if op=='div' and a<val(k):unproved+=1
    out=(max(0,a-val(k)),None) if k&(k-1)==0 or op=='div' else (0,None)
   else:raise ValueError(node)
  values.append(out)
 return {'name':name,'outputs':[values[i] for i in data['outputs']],'nodes':len(values),'opcodes':sorted(opcodes),'exact_divisions_not_proved_by_valuation':unproved,'sha256':hashlib.sha256((ROOT/(name+'.json')).read_bytes()).hexdigest()}
lower_packets=('source_4_majorana','source_4_fermion','product_4_majorana','product_4_fermion')
result=[audit(name) for name in lower_packets+('y6','h6','high6','rho4','tensor4','nonbinary4')]
for item in result:
 if item['name'] in lower_packets+('y6','h6','rho4','tensor4'):assert all(x[1]==0 for x in item['outputs'])
 if item['name']=='high6':assert item['outputs'][0][1]==0
 if item['name']=='nonbinary4':assert item['outputs'][0][0]>=4
Path(__file__).with_suffix('.json').write_text(json.dumps({'status':'PASS','meaning':'Universal conservative divisibility certificate; not random sampling','substitution':'n,m divisible16; a,b,c,cp,y=0; s,w arbitrary integer arrays; conclusions on legal lower towers','public_reference':str(args.public_reference),'programs':result},indent=2)+'\n')
print(json.dumps(result,indent=2))
