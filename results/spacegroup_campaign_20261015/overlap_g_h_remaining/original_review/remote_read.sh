/home/user/xyren/AllFSPT_insulator/runtime/bin/python3 - <<'PYREMOTE'

import base64,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
base=Path('/home/user/xyren/AllFSPT_insulator/runs')
selected=[('spacegroup_133_spinless','n02','n03'),('spacegroup_134_spinless','n03','n03'),
 ('spacegroup_201_spinless','n02','n02'),('spacegroup_203_spinless','n03','n03'),('spacegroup_218_spinless','n03','n02'),
 ('spacegroup_140_spin_half','n02','n02'),('spacegroup_142_spin_half','n02','n03'),('spacegroup_206_spin_half','n02','n02'),
 ('spacegroup_220_spin_half','n02','n02'),('spacegroup_223_spin_half','n02','n02'),('spacegroup_224_spin_half','n02','n03'),('spacegroup_227_spin_half','n02','n03')]
case_names=('input.json','run.json','native.json','result.json','driver.g','stdout.log','stderr.log')
files={};pairs=[];failed=[]
for case,hn,gn in selected:
 h=base/('sgfull-20261015-h-remaining-'+hn);g=base/('sgfull-20261015-g-'+gn)
 try:
  paths=[]
  for root in (g,h):
   paths += [root/name for name in ('source.json','selection.json','formula_runtime.json')]
   paths += [root/case/name for name in case_names]
  present={str(p.relative_to(base)) for p in paths if p.is_file()}
  copied={name:(base/name).read_bytes() for name in present}
  assert {str(p.relative_to(base)) for p in paths if p.is_file()}==present,'Artifact set changed during read'
  assert all((base/name).read_bytes()==raw for name,raw in copied.items()),'Artifact bytes changed during read'
  hr=json.loads(copied[str(h.relative_to(base)/case/'result.json')]);assert hr['run']['status']=='complete' and hr['run']['exitCode']==0
  gresult=copied.get(str(g.relative_to(base)/case/'result.json')); gr=json.loads(gresult) if gresult else None
  ordinary=bool(gr and gr['run']['status']=='complete' and gr['run']['exitCode']==0)
  for name,raw in copied.items():
   if name in files:assert files[name]==raw,'Shared root metadata changed'
  files.update(copied)
  pairs.append(dict(id=case,G=g.name,H=h.name,gOrdinaryComplete=ordinary,gResultPresent=gr is not None,
                    scope='completed-parent-overlap' if ordinary else 'native-only-diagnostic-not-accepted',stableDuringRead=True))
 except (ValueError,AssertionError,KeyError,OSError) as error:
  failed.append(dict(id=case,error=type(error).__name__+': '+str(error)))
print(json.dumps(dict(capturedUTC=datetime.now(timezone.utc).isoformat(),remoteBase=str(base),fixedSelectedCases=[x[0] for x in selected],pairs=pairs,failed=failed,
 files={name:dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest(),base64=base64.b64encode(raw).decode()) for name,raw in sorted(files.items())}),sort_keys=True))

PYREMOTE
