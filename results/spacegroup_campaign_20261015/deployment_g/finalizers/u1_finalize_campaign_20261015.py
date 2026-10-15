"""Verify and collect a complete immutable campaign on its compute node."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import tarfile
import time

parser = argparse.ArgumentParser()
parser.add_argument('--tag', required=True)
parser.add_argument('--runner-pid', required=True, type=int)
parser.add_argument('--node', required=True)
parser.add_argument('--source-tag', required=True)
args = parser.parse_args()
base = Path('/home/user/xyren/AllFSPT_insulator')
if socket.gethostname().split('.')[0] != args.node:
    raise SystemExit('Wrong node')
if any('/' in value or not value.startswith('sgfull-20261015-') for value in (args.tag, args.source_tag)):
    raise SystemExit('Unexpected campaign name')
root = base / 'runs' / args.tag
snapshot = base / 'snapshots' / args.source_tag
postprocessor = base / 'snapshots/sgfull-20261015-g'
e8 = base / 'runs' / (args.tag + '-e8')
accepted = base / 'runs' / (args.tag + '-accepted')
status = base / 'runs' / (args.tag + '-finalization.json')
report = dict(tag=args.tag, node=args.node, state='waiting',
              runnerPID=args.runner_pid, source=str(snapshot),
              postprocessor=str(postprocessor),
              startedUTC=datetime.now(timezone.utc).isoformat())
with status.open('x') as handle:
    json.dump(report, handle, indent=2, sort_keys=True)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save():
    temporary = status.with_suffix('.tmp')
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    temporary.replace(status)

def alive():
    try:
        command = Path('/proc/%d/cmdline' % args.runner_pid).read_bytes().split(b'\0')
    except FileNotFoundError:
        return False
    return str(root).encode() in command and str(snapshot / 'scripts/classify.py').encode() in command

try:
    selection = json.loads((root / 'selection.json').read_text())
    source = json.loads((root / 'source.json').read_text())
    runtime = json.loads((root / 'formula_runtime.json').read_text())
    report.update(selectionSHA256=digest(root / 'selection.json'),
                  sourceSHA256=source['sha256'], selectedCount=len(selection))
    save()
    while alive():
        time.sleep(20)
    if digest(root / 'selection.json') != report['selectionSHA256']:
        raise ValueError('Selection changed')
    for relative, expected in source['files'].items():
        if digest(snapshot / relative) != expected:
            raise ValueError('Runtime source changed: ' + relative)
    library = Path(runtime['libraryPath'])
    if library.is_file() != runtime['libraryPresent'] or (library.is_file() and digest(library) != runtime['librarySHA256']):
        raise ValueError('Formula VM changed')
    rows = [json.loads((root / case / 'run.json').read_text()) for case in selection]
    incomplete = [row['id'] for row in rows if row['status'] != 'complete' or row.get('exitCode') != 0]
    if incomplete:
        report.update(state='incomplete', retryCases=incomplete)
        save()
        raise SystemExit(1)
    report.update(state='extending_E8', sourceVerified=True, runtimeVerified=True)
    save()
    environment = dict(os.environ, LC_ALL='C', LANG='C', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    environment['PATH'] = str(base / 'runtime/bin') + ':' + environment['PATH']
    commands = [
        [str(base / 'runtime/bin/python3'), str(postprocessor / 'scripts/extend_e8_3p1.py'),
         '--ci-root', str(root), '--output', str(e8)],
        [str(base / 'runtime/bin/python3'), str(postprocessor / 'scripts/collect_expansion.py'),
         '--ci-root', str(root), '--e8-root', str(e8), '--output', str(accepted)],
    ]
    report['commands'] = commands
    save()
    with (base / 'runs' / (args.tag + '-postprocess.log')).open('x') as log:
        for command in commands:
            subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, env=environment, check=True)
    collection = json.loads((accepted / 'collection.json').read_text())
    if not collection['accepted'] or sum(item['count'] for item in collection['collections']) != len(selection):
        raise ValueError('Accepted coverage does not equal selection')
    archive = base / 'runs' / (args.tag + '-evidence.tar.gz')
    with tarfile.open(archive, 'x:gz') as tar:
        for path in (root, e8, accepted):
            tar.add(path, arcname=path.name)
    report.update(state='complete', acceptedCount=len(selection), archive=str(archive),
                  archiveSHA256=digest(archive), archiveBytes=archive.stat().st_size,
                  endedUTC=datetime.now(timezone.utc).isoformat())
    save()
except Exception as error:
    report.update(state='failed', error=type(error).__name__ + ': ' + str(error),
                  endedUTC=datetime.now(timezone.utc).isoformat())
    save()
    raise
print(json.dumps(report, sort_keys=True), flush=True)
