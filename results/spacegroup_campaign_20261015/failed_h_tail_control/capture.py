#!/usr/bin/env python3
"""Archive ended H-tail control bytes without changing remote artifacts."""
import base64
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REMOTE = r'''
import base64,datetime,gzip,hashlib,io,json,tarfile
from pathlib import Path
base=Path('/home/user/xyren/AllFSPT_insulator')
tag='sgfull-20261015-h-tail-n08';root=base/'runs'/tag
snapshot=base/'snapshots/sgfull-20261015-h'
expected_source='80e0a57b1ac611b348d748da2becbfe64d4aa17f196df9ffae3addea3e22940b'
expected_vm='0c026ca103e9ba8b674c006d6042ca23bfe526ca62b4e96b3c1b79c4d318dec2'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(p.read_bytes())
source=read(root/'source.json');runtime=read(root/'formula_runtime.json')
assert source['sha256']==expected_source==digest(json.dumps(source['files'],sort_keys=True,separators=(',',':')).encode())
source_checks={name:digest((snapshot/name).read_bytes()) for name in source['files']}
assert source_checks==source['files'] and len(source_checks)==60
assert runtime['libraryPath']==str(snapshot/'insulator/_compiled/u1_dag_vm.so')
assert runtime['libraryPresent'] is True and runtime['requestedMode']=='auto'
assert digest(Path(runtime['libraryPath']).read_bytes())==runtime['librarySHA256']==expected_vm
selected=read(root/'selection.json')
assert set(selected)=={'spacegroup_%03d_%s'%(n,s) for n in [226,230] for s in ['spin_half','spinless']} and len(selected)==4
paths=[p for p in root.rglob('*') if p.is_file()]
extras=[base/'runs'/(tag+suffix) for suffix in ['-finalization.json','-finalizer.log','-launch.json','-finalizer-launch.json','.log']]
paths+=extras
assert all(p.is_file() and not p.is_symlink() for p in paths)
files={str(p.relative_to(base)):p.read_bytes() for p in paths}
for cid in selected:
 case=root/cid;run=read(case/'run.json');data=read(case/'input.json')
 assert run['id']==data['id']==cid and run['sourceSHA256']==expected_source
 assert digest((case/'input.json').read_bytes())==run['inputSHA256']
 assert (case/'input.json').read_bytes()==(snapshot/'insulator_catalog/generated'/(cid+'.json')).read_bytes()
 if cid.startswith('spacegroup_226_'):
  assert run['status']=='failed' and run['exitCode']==1
  assert not(case/'native.json').exists() and not(case/'result.json').exists()
 else:
  assert run['status']=='complete' and type(run['exitCode']) is int and run['exitCode']==0
  assert read(case/'result.json')=={'input':data,'run':run,'classification':read(case/'native.json')}
final=read(base/'runs'/(tag+'-finalization.json'))
assert final['state']=='incomplete' and set(final['retryCases'])=={'spacegroup_226_spin_half','spacegroup_226_spinless'}
assert all((base/name).read_bytes()==raw for name,raw in files.items())
buf=io.BytesIO()
with tarfile.open(fileobj=buf,mode='w:') as tar:
 for name,raw in sorted(files.items()):
  info=tarfile.TarInfo(name);info.size=len(raw);info.mtime=0;info.mode=0o444;tar.addfile(info,io.BytesIO(raw))
archive=gzip.compress(buf.getvalue(),mtime=0)
print(json.dumps({'schema':'u1-failed-h-tail-control-capture-v1','capturedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'remoteBase':str(base),'tag':tag,'sourceSnapshot':str(snapshot),'sourceSHA256':expected_source,
 'sourceSnapshotFilesSHA256':source_checks,'sourceSnapshotVerified':True,'formulaRuntime':runtime,
 'actualFormulaLibrarySHA256':expected_vm,'formulaRuntimeVerified':True,'artifactsStableAcrossRead':True,
 'sourceArtifactSHA256':digest((root/'source.json').read_bytes()),'selectionSHA256':digest((root/'selection.json').read_bytes()),
 'files':{n:{'bytes':len(r),'sha256':digest(r)} for n,r in sorted(files.items())},
 'archiveBytes':len(archive),'archiveSHA256':digest(archive),'archiveBase64':base64.b64encode(archive).decode(),
 'remoteFilesChanged':False,'signalsSent':False,'classificationRun':False,'acceptedClassificationClaimed':False},sort_keys=True))
'''
result = subprocess.run(['ssh', '-o', 'ControlMaster=no', '-o', 'ProxyCommand=false', 'cuhk-cluster3', 'bash -s'],
                        input="/home/user/xyren/AllFSPT_insulator/runtime/bin/python3 - <<'CONTROL_CAPTURE'\n" + REMOTE + "\nCONTROL_CAPTURE\n",
                        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(HERE / 'capture.stderr.log').write_text(result.stderr)
result.check_returncode()
data = json.loads(result.stdout)
archive = base64.b64decode(data.pop('archiveBase64'))
assert len(archive) == data['archiveBytes'] and hashlib.sha256(archive).hexdigest() == data['archiveSHA256']
(HERE / 'raw.tar.gz').write_bytes(archive)
(HERE / 'capture.json').write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
print(json.dumps({'archiveBytes': data['archiveBytes'], 'archiveSHA256': data['archiveSHA256'], 'files': len(data['files'])}, indent=2))
