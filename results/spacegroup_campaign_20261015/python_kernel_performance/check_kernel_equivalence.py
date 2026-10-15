import importlib.util,sys,json,random,hashlib
from pathlib import Path
from fractions import Fraction
from itertools import combinations
baseline=Path(sys.argv[1]);candidate=Path(sys.argv[2]);sys.path.insert(0,str(baseline))
from insulator._engine import simplex as original
spec=importlib.util.spec_from_file_location('insulator._engine.simplex_candidate',candidate/'insulator/_engine/simplex.py')
new=importlib.util.module_from_spec(spec);spec.loader.exec_module(new)
rng=random.Random(105142026)
values=[0,1,-1,3,-7,Fraction(0),Fraction(3),Fraction(-11),Fraction(1,2),Fraction(-5,3),Fraction(7,12),Fraction(10**30+1,17)]
checks=0;digest=hashlib.sha256();noncommuting=0

def compare(a,b):
 global checks
 assert (a.N,a.p,a.tw)==(b.N,b.p,b.tw)
 assert a.v==b.v,(a.N,a.p,a.tw,a.v,b.v)
 digest.update(repr((a.N,a.p,a.tw,[(f,str(Fraction(x))) for f,x in a.v.items()])).encode());checks+=1
for N in range(1,7):
 for p in range(N+1):
  faces=tuple(combinations(range(N+1),p+1))
  for trial in range(3):
   tw=tuple(rng.randrange(2) for _ in range(N+1));v={f:rng.choice(values) for f in faces if rng.randrange(3)}
   a=original.C(N,p,v,tw);b=new.C(N,p,v,tw)
   compare(a,b);compare(a.d(),b.d());compare(a.mod(2),b.mod(2));compare(a.sc(Fraction(-5,7)),b.sc(Fraction(-5,7)))
   for q in range(N+1):
    tf=tuple(rng.randrange(2) for _ in range(N+1));w={f:rng.choice(values) for f in combinations(range(N+1),q+1) if rng.randrange(3)}
    c=original.C(N,q,w,tf);d=new.C(N,q,w,tf)
    for i in range(min(p,q)+1):
     if p+q-i>N:continue
     for binary in (False,True):compare(a.cup(c,i,binary),b.cup(d,i,binary))
    if p+q<=N and a.cup(c).v!=c.cup(a).v:noncommuting+=1
assert noncommuting>0
report={'checks':checks,'noncommuting_cup_cases':noncommuting,'values':'integers, denominator-one Fractions, negative and nonintegral rationals; independent arbitrary vertex actions','kernel_output_sha256':digest.hexdigest(),'geometry_cache':str(new._cup_plan.cache_info()),'status':'PASS'}
print(json.dumps(report,indent=2));Path(sys.argv[3]).write_text(json.dumps(report,indent=2)+'\n')
