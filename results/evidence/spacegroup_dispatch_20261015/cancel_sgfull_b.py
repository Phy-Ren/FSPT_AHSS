#!/usr/bin/env python3
"""Cancel only the identified superseded owned campaign on its compute node."""
import datetime
import json
import os
from pathlib import Path
import signal
import socket
import sys
import time

node = socket.gethostname().split('.')[0]
expected = {'n02': 36478, 'n03': 36086, 'n08': 2408}
if node not in expected:
    raise SystemExit('Wrong compute node')
pid = expected[node]
tag = 'sgfull-20261015-b'
base = Path('/home/user/xyren/AllFSPT_insulator')
root = base / 'runs' / (tag + '-' + node)
command = Path('/proc/%d/cmdline' % pid).read_bytes().replace(b'\0', b' ').decode()
if str(root) not in command or str(base / 'snapshots' / tag / 'scripts/classify.py') not in command:
    raise SystemExit('Runner identity did not match the owned campaign')
event = {'node': node, 'runnerPID': pid, 'runnerCommand': command,
         'startedUTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'reason': 'Superseded by independently reviewed exact-cache and literal-zero performance snapshot C',
         'replacement': 'sgfull-20261015-c', 'terminatedGAPProcessGroups': []}
os.kill(pid, signal.SIGSTOP)
for proc in Path('/proc').iterdir():
    if not proc.name.isdigit():
        continue
    try:
        args = (proc / 'cmdline').read_bytes().split(b'\0')
    except (FileNotFoundError, PermissionError):
        continue
    if args and args[0].decode().endswith('/gap') and any(
            arg.decode().startswith(str(root) + '/') and arg.decode().endswith('/driver.g') for arg in args):
        child = int(proc.name)
        if os.getpgid(child) != child:
            raise RuntimeError('Owned GAP job did not have its expected independent process group')
        event['terminatedGAPProcessGroups'].append(child)
        os.killpg(child, signal.SIGTERM)
time.sleep(3)
for child in event['terminatedGAPProcessGroups']:
    try:
        os.killpg(child, signal.SIGKILL)
    except ProcessLookupError:
        pass
os.kill(pid, signal.SIGTERM)
os.kill(pid, signal.SIGCONT)
time.sleep(1)
rows = []
for path in sorted(root.glob('*/run.json')):
    row = json.loads(path.read_text())
    if row['status'] == 'running':
        row.update(status='cancelled', cancellationReason=event['reason'],
                   replacementCampaign=event['replacement'],
                   endedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat())
        path.write_text(json.dumps(row, indent=2, sort_keys=True) + '\n')
    rows.append(row)
(root / 'summary.json').write_text(json.dumps(rows, indent=2, sort_keys=True) + '\n')
event['endedUTC'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
event['preservedCompletedCases'] = [r['id'] for r in rows if r['status'] == 'complete']
event['cancelledStartedCases'] = [r['id'] for r in rows if r['status'] == 'cancelled']
event['unstartedCases'] = sorted(set(json.loads((root / 'selection.json').read_text())) - {r['id'] for r in rows})
(root / 'cancellation.json').write_text(json.dumps(event, indent=2, sort_keys=True) + '\n')
print(node, 'terminated GAP groups', len(event['terminatedGAPProcessGroups']),
      'preserved completed cases', len(event['preservedCompletedCases']))
