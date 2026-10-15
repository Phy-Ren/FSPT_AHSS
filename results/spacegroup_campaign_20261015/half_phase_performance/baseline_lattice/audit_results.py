from pathlib import Path
import hashlib,json
from sympy import Matrix,ZZ
from sympy.matrices.normalforms import smith_normal_form
BASE=Path(__file__).resolve().parent
rows=[]
for group in (141,229):
 pair=[]
 for mode in ('koszul','hap'):
  folder=BASE/f'spacegroup_{group:03d}_spin_half_{mode}'
  low=json.loads((folder/'lower.json').read_text());roots=json.loads((folder/'completed_roots.json').read_text());result=json.loads((folder/'result.json').read_text())
  K=Matrix(low['kernel']);Q=Matrix(low['chargeGenerators']);Dq=Matrix(low['chargeDifferential']);Dp=Matrix(low['phaseDifferential'])
  relations=Matrix.diag(*low['chargeOrders'])*K.inv();assert all(x.q==1 for x in relations)
  S=smith_normal_form(relations,domain=ZZ);diag=[abs(int(S[i,i]))for i in range(S.rows)]
  subgroup={'freeRank':diag.count(0),'torsion':[x for x in diag if x>1]}
  assert K*Q*Dq==Matrix.zeros(K.rows,Dq.cols)
  for i,root in enumerate(roots):
   q=Matrix([root['nativeCharge']]);o=Matrix([[ZZ(x) if isinstance(x,int) else __import__('sympy').Rational(x) for x in root['nativeSource']]])
   v=Matrix([[__import__('sympy').Rational(x) for x in root['nativePrimitive']]])
   checked=root['completedNative'];p=Matrix([[__import__('sympy').Rational(x) for x in checked['nativePhase']]])
   assert list(q)==list(K[i,:]*Q)
   assert all(x.q==1 for x in v*Dp-o)
   assert all(x.q==1 for x in p*Dp-o)
   assert checked['nativeCharge']==root['nativeCharge']
  pair.append(dict(group=group,latticeResolution=mode,chargeOrders=low['chargeOrders'],phaseOrders=low['phaseOrders'],targetOrders=low['targetOrders'],survivingChargeSubgroup=subgroup,kernelIndex=abs(int(K.det())),completedRoots=len(roots),literalEvenRoots=sum(all(v%2==0 for v in list((K*Q)[i,:])) for i in range(K.rows)),nativeEquationsVerified=True,result=result))
 assert all(pair[0][k]==pair[1][k] for k in ('chargeOrders','phaseOrders','targetOrders','survivingChargeSubgroup','kernelIndex','completedRoots'))
 rows.extend(pair)
out={'status':'PASS','scope':'Independent exact integer/phase native equations and abstract initial charge kernel; no assertion of literal cross-resolution coordinates or final stacking group','cases':rows}
(BASE/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
