#!/usr/bin/env python3
"""Fetch one fixed new-overlap batch; no process, classification or acceptance actions."""
import base64,hashlib,json,subprocess
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent
REMOTE=r'''
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
'''
command=['ssh','-o','BatchMode=yes','cuhk-cluster3','bash -s']
script="/home/user/xyren/AllFSPT_insulator/runtime/bin/python3 - <<'PYREMOTE'\n"+REMOTE+"\nPYREMOTE\n"
(BASE/'remote_read.sh').write_text(script)
run=subprocess.run(command,input=script.encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
(BASE/'ssh.stderr.log').write_bytes(run.stderr)
assert run.returncode==0,run.stderr
(BASE/'transport.json').write_bytes(run.stdout)
value=json.loads(run.stdout); rawroot=BASE/'raw';rawroot.mkdir(exist_ok=False)
for name,meta in value['files'].items():
 rel=Path(name);assert not rel.is_absolute() and '..' not in rel.parts
 raw=base64.b64decode(meta['base64'],validate=True)
 assert len(raw)==meta['size'] and hashlib.sha256(raw).hexdigest()==meta['sha256']
 target=rawroot/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
value['command']=command;value['exitCode']=run.returncode
for meta in value['files'].values():del meta['base64']
(BASE/'download.json').write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
print(json.dumps({'pairs':value['pairs'],'failed':value['failed'],'files':len(value['files'])},indent=2))
