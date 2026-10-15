import json
from pathlib import Path
import socket
import subprocess
from datetime import datetime, timezone

base = Path('/home/user/xyren/AllFSPT_insulator')
node = socket.gethostname().split('.')[0]
tasks = {
    'n02': [('sgfull-20261015-g-n02', 40405, 'g'), ('sgfull-20261015-f-n02-pilot', 39611, 'f')],
    'n03': [('sgfull-20261015-g-n03', 38671, 'g'), ('sgfull-20261015-f-n03-pilot', 37879, 'f')],
    'n08': [('sgfull-20261015-g-n08', 9271, 'g'), ('sgfull-20261015-e-smoke', 8094, 'e')],
}[node]
for tag, pid, source in tasks:
    path = base / 'runs' / (tag + '-finalizer-launch.json')
    command = [str(base / 'runtime/bin/python3'), str(base / 'snapshots/u1_finalize_campaign_20261015.py'),
               '--tag', tag, '--runner-pid', str(pid), '--node', node, '--source-tag', 'sgfull-20261015-' + source]
    report = dict(node=node, command=command, startedUTC=datetime.now(timezone.utc).isoformat())
    with path.open('x') as handle:
        json.dump(dict(report, state='starting'), handle, indent=2)
    with (base / 'runs' / (tag + '-finalizer.log')).open('x') as log:
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=log,
                                   stderr=subprocess.STDOUT, start_new_session=True)
    report.update(state='launched', pid=process.pid)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(tag=tag, pid=process.pid, node=node)))
