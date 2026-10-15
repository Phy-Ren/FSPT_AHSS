from datetime import datetime, timezone
import json
from pathlib import Path
import runpy
import socket
import subprocess

base = Path('/home/user/xyren/AllFSPT_insulator')
tag = 'sgfull-20261015-f'
node = socket.gethostname().split('.')[0]
plan = json.loads((base / 'snapshots' / (tag + '-plan.json')).read_text())
shard, = [item for item in plan['shards'] if item['node'] == node]
report_path = base / 'runs' / (tag + '-' + node + '-launch.json')
if report_path.exists() or Path(shard['output']).exists():
    raise SystemExit('A launch/output already exists; refusing duplicate launch')
runner = runpy.run_path(str(base / 'snapshots' / tag / 'scripts/classify.py'))
report = dict(shard)
report.update(sourceCommit=plan['sourceCommit'], snapshotSHA256=plan['snapshotSHA256'],
              source=runner['source_manifest'](), formulaRuntime=runner['formula_runtime_manifest'](),
              node=node, startedUTC=datetime.now(timezone.utc).isoformat())
report['vmBuild'] = json.loads((base / 'runs' / (tag + '-vm-build.json')).read_text())
with report_path.open('x') as output:
    json.dump(dict(report, state='starting'), output, indent=2, sort_keys=True)
log_path = base / 'runs' / (tag + '-' + node + '-pilot.log')
with log_path.open('x') as log:
    process = subprocess.Popen(['bash', shard['remoteScript']], stdin=subprocess.DEVNULL,
                               stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
report.update(state='launched', pid=process.pid, log=str(log_path))
report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
print(json.dumps({key: report[key] for key in ('node','pid','state','output')}, sort_keys=True))
