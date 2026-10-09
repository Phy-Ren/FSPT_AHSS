"""Verify the maintained wrapper against independently built directed matchings."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fspt.geometric_reference_3d import *
import tempfile,tarfile
workspace=tempfile.TemporaryDirectory(prefix='fspt-geometric-')
with tarfile.open(ROOT/'docs/formulas/verification/geometric_3d/complete_local_census_20261009.tar.gz') as archive:
 archive.extractall(workspace.name,filter='data')
sys.path.insert(0,workspace.name)
from audit_references import corrected_P,corrected_F,prepare,generate,loops
from itertools import combinations
stats={'P':0,'F':0,'backgrounds':{},'mismatches':0}
for bg in ('zero','w','s','both'):
 for seed in range(128):
  data=generate(5,bg,130000+seed)
  n=C(1,values=data['n1'],mod=None);u=C(2,values=data['n2']);w=C(2,values=data['omega2']);s=C(1,values=data['s1'])
  row,changed=corrected_F(data)
  counted=loops(changed['in'],changed['out'],row['mode_count'])['parity_change']
  assert obstruction(n,u,w,s)(tuple(range(5)))==counted
  stats['F']+=1
  data=generate(4,bg,130000+seed)
  n=C(1,values=data['n1'],mod=None);np=C(1,values=data['n1prime'],mod=None)
  u=C(2,values=data['n2']);up=C(2,values=data['n2prime']);w=C(2,values=data['omega2']);s=C(1,values=data['s1'])
  raw,math,pad=prepare(data);row,ini,fin=corrected_P(raw)
  counted=loops(ini,fin,len(row['modes']))['parity_change']
  N,N2,E=lower_product(n,np,u,up,w,s)
  assert E(tuple(range(4)))==counted
  from reference3 import target
  old=target(*math)
  m,mp=checked_majorana(n,u,s),checked_majorana(np,up,s)
  M=checked_majorana(N,N2,s)
  B=pair_reference(n,np,m,mp,s)
  delta=single_reference(M)+single_reference(m)+single_reference(mp)
  assert (E+delta+B.d())(tuple(range(4)))==old
  stats['P']+=1
 stats['backgrounds'][bg]=256
(ROOT/'docs/formulas/verification/geometric_3d/current_module_checks.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats))
