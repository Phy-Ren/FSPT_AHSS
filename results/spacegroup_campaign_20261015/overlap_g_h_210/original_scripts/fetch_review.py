#!/usr/bin/env python3
"""Read two completed overlap records without editing either running campaign."""
import base64, hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent
REMOTE = r'''
import base64,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
base=Path('/home/user/xyren/AllFSPT_insulator/runs')
case='spacegroup_210_spinless'
files={}
for tag in ('sgfull-20261015-g-n03','sgfull-20261015-h-remaining-n02'):
 root=base/tag
 result=json.loads((root/case/'result.json').read_bytes())
 assert result['run']['status']=='complete' and result['run']['exitCode']==0
 for name in ('source.json','formula_runtime.json','selection.json'):
  files[str(Path(tag)/name)]=(root/name).read_bytes()
 for name in ('input.json','run.json','native.json','result.json','driver.g','stdout.log','stderr.log'):
  files[str(Path(tag)/case/name)]=(root/case/name).read_bytes()
for name,raw in files.items():
 assert (base/name).read_bytes()==raw, 'Artifact changed while copying: '+name
print(json.dumps({'remoteBase':str(base),'capturedUTC':datetime.now(timezone.utc).isoformat(),'unchangedDuringRead':True,'files':{name:{'sha256':hashlib.sha256(raw).hexdigest(),'size':len(raw),'base64':base64.b64encode(raw).decode()} for name,raw in sorted(files.items())}},sort_keys=True))
'''
command=['ssh','-o','BatchMode=yes','cuhk-cluster3','bash -s']
script="/home/user/xyren/AllFSPT_insulator/runtime/bin/python3 - <<'PYREMOTE'\n"+REMOTE+"\nPYREMOTE\n"
(ROOT/'remote_read.sh').write_text(script)
start=datetime.now(timezone.utc).isoformat()
p=subprocess.run(command,input=script.encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
(ROOT/'ssh.stderr.log').write_bytes(p.stderr)
if p.returncode: raise RuntimeError('SSH read failed: '+p.stderr.decode(errors='replace'))
(ROOT/'transport.json').write_bytes(p.stdout)
value=json.loads(p.stdout)
dest=ROOT/'raw'; dest.mkdir(exist_ok=False)
for name,item in value['files'].items():
 rel=Path(name)
 assert not rel.is_absolute() and '..' not in rel.parts
 raw=base64.b64decode(item['base64'],validate=True)
 assert len(raw)==item['size'] and hashlib.sha256(raw).hexdigest()==item['sha256']
 out=dest/rel; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(raw)
manifest={key:value[key] for key in ('remoteBase','capturedUTC','unchangedDuringRead')}
manifest.update(command=command,startedUTC=start,endedUTC=datetime.now(timezone.utc).isoformat(),exitCode=p.returncode,
                files={name:{k:v for k,v in item.items() if k!='base64'} for name,item in value['files'].items()})
(ROOT/'download.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps({'files':len(manifest['files']),'destination':str(dest)},indent=2))
