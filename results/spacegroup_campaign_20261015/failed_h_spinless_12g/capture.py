#!/usr/bin/env python3
"""Read-only capture of a completed-but-incomplete failed campaign; no signals."""
from pathlib import Path
import hashlib,io,json,subprocess,tarfile
BASE=Path(__file__).resolve().parent
REMOTE=r'''
from pathlib import Path
import datetime,hashlib,io,json,sys,tarfile
base=Path('/home/user/xyren/AllFSPT_insulator');tag='sgfull-20261015-h-tail-spinless-n08';root=base/'runs'/tag
paths=list(root.rglob('*'))+[base/'runs'/(tag+s) for s in ['-launch.json','-finalizer-launch.json','-finalization.json','-finalizer.log','.log']]
paths=sorted(p for p in paths if p.is_file());assert all(not p.is_symlink() for p in paths)
files={str(p.relative_to(base)):p.read_bytes() for p in paths}
assert files=={str(p.relative_to(base)):p.read_bytes() for p in paths},'Raw campaign changed'
run=json.loads(files['runs/'+tag+'/spacegroup_226_spinless/run.json'])
assert run['status']=='failed' and type(run['exitCode']) is int and run['exitCode']!=0
assert b'cannot extend the workspace any more' in files['runs/'+tag+'/spacegroup_226_spinless/stderr.log']
assert not (root/'spacegroup_226_spinless/native.json').exists()
metadata={'captureUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'originalRoot':str(root),'twoReadsEqual':True,'readOnly':True,'classificationOrSignals':False,'failedCase':'spacegroup_226_spinless','ordinaryCompanion':'spacegroup_230_spinless','originalParentAccepted':False,'files':{n:{'sha256':hashlib.sha256(d).hexdigest(),'bytes':len(d)} for n,d in files.items()}}
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|gz') as t:
 for n,d in sorted(files.items()):
  x=tarfile.TarInfo('raw/'+n);x.size=len(d);t.addfile(x,io.BytesIO(d))
 d=(json.dumps(metadata,indent=2,sort_keys=True)+'\n').encode();x=tarfile.TarInfo('capture.json');x.size=len(d);t.addfile(x,io.BytesIO(d))
'''
p=subprocess.run(['ssh','-o','ControlMaster=no','-o','ProxyCommand=false','cuhk-cluster3','bash -s'],input=("python3 - <<'CAPTURE_PY'\n"+REMOTE+"\nCAPTURE_PY\n").encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
(BASE/'capture.stderr.log').write_bytes(p.stderr);(BASE/'raw.tar.gz').write_bytes(p.stdout)
files={}
with tarfile.open(fileobj=io.BytesIO(p.stdout),mode='r:gz') as t:
 for m in t.getmembers():
  n=Path(m.name);assert m.isfile() and not n.is_absolute() and '..' not in n.parts and m.name not in files
  files[m.name]=t.extractfile(m).read()
meta=json.loads(files['capture.json'])
for n,v in meta['files'].items():assert hashlib.sha256(files['raw/'+n]).hexdigest()==v['sha256'] and len(files['raw/'+n])==v['bytes']
for n,d in files.items():o=BASE/n;o.parent.mkdir(parents=True,exist_ok=True);o.write_bytes(d)
summary={'archiveSHA256':hashlib.sha256(p.stdout).hexdigest(),'files':len(meta['files']),'verifiedRemoteLocalHashes':True,'failedRun':json.loads(files['raw/runs/sgfull-20261015-h-tail-spinless-n08/spacegroup_226_spinless/run.json']),'stderr':files['raw/runs/sgfull-20261015-h-tail-spinless-n08/spacegroup_226_spinless/stderr.log'].decode()}
(BASE/'failure.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print(json.dumps(summary,indent=2,sort_keys=True))
