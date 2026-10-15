/home/user/xyren/AllFSPT_insulator/runtime/bin/python3 - <<'PYREMOTE'

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

PYREMOTE
