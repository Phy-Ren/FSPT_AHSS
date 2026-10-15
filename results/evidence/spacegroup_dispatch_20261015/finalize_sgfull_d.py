#!/usr/bin/env python3
"""Finalize one complete owned shard; never accept a partial selection."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import socket
import subprocess
import tarfile
import time

base = Path('/home/user/xyren/AllFSPT_insulator')
node = socket.gethostname().split('.')[0]
pids = {'n02': 38339, 'n03': 36684, 'n08': 7500}
if node not in pids:
    raise SystemExit('Wrong compute node')
tag = 'sgfull-20261015-d-' + node
root = base / 'runs' / tag
target = base / 'runs' / (tag + '-e8')
status = base / 'runs' / (tag + '-finalization.json')
runtime = base / 'snapshots' / 'sgfull-20261015-d-runtime.json'
report = {'tag': tag, 'node': node, 'state': 'waiting',
          'startedUTC': datetime.now(timezone.utc).isoformat()}

def save():
    temporary = status.with_suffix('.tmp')
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    temporary.replace(status)

def runner_alive():
    try:
        command = Path('/proc/%d/cmdline' % pids[node]).read_bytes().replace(b'\0', b' ').decode()
    except FileNotFoundError:
        return False
    return str(root) in command and 'scripts/classify.py' in command

save()
while True:
    try:
        selected = json.loads((root / 'selection.json').read_text())
        rows = [json.loads((root / case / 'run.json').read_text()) for case in selected]
        complete = all(row.get('status') == 'complete' and row.get('exitCode') == 0 for row in rows)
    except (FileNotFoundError, ValueError):
        complete = False
    alive = runner_alive()
    if not alive:
        break
    time.sleep(20)
if not complete:
    report.update(state='incomplete', reason='The classifier exited with an incomplete selected shard')
    save()
    raise SystemExit(1)
report.update(state='extending_E8', selectedCount=len(selected))
save()
shutil.copyfile(runtime, root / 'runtime.json')
command = ['/home/user/xyren/AllFSPT_insulator/runtime/bin/python3',
           str(base / 'snapshots/sgfull-20261015-c/scripts/extend_e8_3p1.py'),
           '--ci-root', str(root), '--output', str(target)]
report['e8Command'] = command
with (base / 'runs' / (tag + '-e8.log')).open('w') as log:
    result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
if result.returncode:
    report.update(state='extension_failed', exitCode=result.returncode)
    save()
    raise SystemExit(result.returncode)
shutil.copyfile(runtime, target / 'runtime.json')
archive = base / 'runs' / (tag + '-evidence.tar.gz')
with tarfile.open(archive, 'w:gz') as packed:
    packed.add(root, arcname=root.name)
    packed.add(target, arcname=target.name)
report.update(state='complete', archive=str(archive),
              archiveSHA256=hashlib.sha256(archive.read_bytes()).hexdigest(),
              archiveBytes=archive.stat().st_size,
              endedUTC=datetime.now(timezone.utc).isoformat())
save()
print(json.dumps(report, sort_keys=True), flush=True)
