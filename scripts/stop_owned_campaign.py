#!/usr/bin/env python3
"""Stop only a named owned run, preserving raw records and process identities."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import time


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


_EXECUTABLE_HASHES = {}


def executable_sha(path):
    # Reuse hashes only while the exact regular-file identity and metadata agree.
    st = path.stat()
    key = (str(path), st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
    if key not in _EXECUTABLE_HASHES:
        _EXECUTABLE_HASHES[key] = sha(path)
    return _EXECUTABLE_HASHES[key]


def process(pid):
    root = Path('/proc') / str(pid)
    try:
        fields = (root / 'stat').read_text().rsplit(')', 1)[1].split()
        argv = [x.decode(errors='replace') for x in (root / 'cmdline').read_bytes().split(b'\0') if x]
        row = dict(pid=pid, ppid=int(fields[1]), pgid=int(fields[2]),
                   startTicks=int(fields[19]), uid=root.stat().st_uid,
                   state=fields[0], argv=argv, host=socket.gethostname())
        if fields[0] != 'Z':
            try:
                executable = Path(os.readlink(str(root / 'exe')))
                row.update(executablePath=str(executable), executableSHA256=executable_sha(executable))
            except (FileNotFoundError, PermissionError, ProcessLookupError) as error:
                row['executableCaptureError'] = type(error).__name__
        return row
    except (FileNotFoundError, ProcessLookupError):
        return None


def same_identity(left, right):
    return right is not None and all(left[k] == right[k] for k in ('pid','uid','startTicks'))


def signal_one(row, sig):
    current = process(row['pid'])
    if same_identity(row, current) and current['state'] != 'Z':
        try:
            os.kill(row['pid'], sig)
            return True
        except ProcessLookupError:
            pass
    return False


def scan_owned(uid):
    result = {}
    for path in Path('/proc').iterdir():
        try:
            if path.name.isdigit() and path.stat().st_uid == uid:
                row = process(int(path.name))
                if row:
                    result[row['pid']] = row
        except (FileNotFoundError, ProcessLookupError):
            continue
    return result


def descendants(rows, parent):
    selected = {parent}
    while True:
        expanded = selected | {pid for pid,row in rows.items() if row['ppid'] in selected}
        if expanded == selected:
            return selected
        selected = expanded


def validate_tree(rows, runner, root, source, selection):
    """Read-only identity/topology validation, before or after scheduling stops."""
    current = rows.get(runner['pid'])
    if not same_identity(runner, current) or current['state'] == 'Z':
        raise RuntimeError('Campaign runner exited or changed identity')
    owned = descendants(rows, runner['pid'])
    captured = {pid: rows[pid] for pid in owned}
    gaps, batches = [], []
    for pid in sorted(owned):
        row = rows[pid]
        if row['state'] == 'Z':
            continue
        if not row['argv'] or not row.get('executablePath') or not row.get('executableSHA256'):
            raise RuntimeError('An active owned process lacks complete argv/executable identity')
        if pid == runner['pid']:
            continue
        drivers = [Path(x) for x in row['argv'] if x.startswith(str(root) + '/') and x.endswith('/driver.g')]
        if not drivers:
            if row['ppid'] == runner['pid']:
                raise RuntimeError('An active direct runner child lacks its campaign driver argv')
            continue
        if len(drivers) != 1 or row['pgid'] != pid or row['ppid'] != runner['pid']:
            raise RuntimeError('Unexpected owned GAP process topology')
        driver = drivers[0]
        if driver.parent.name not in selection or not driver.is_file():
            raise RuntimeError('GAP driver is outside the selected campaign cases')
        record = json.loads((driver.parent / 'run.json').read_text())
        command = record.get('command')
        if (not isinstance(command, list) or len(command) < 2
                or any(not isinstance(x, str) or not x for x in command)
                or row['argv'][-len(command[1:]):] != command[1:]
                or command[-1] != str(driver)):
            raise RuntimeError('GAP launch arguments differ from the saved run')
        cases = record.get('batchCaseIDs')
        if (not isinstance(cases, list) or len(cases) != 2 or len(set(cases)) != 2
                or not set(cases) <= set(selection) or cases[0] != driver.parent.name
                or record.get('id') != cases[0] or record.get('pairedSpins') is not True
                or record.get('sourceSHA256') != source['sha256']
                or record.get('host') != row['host']):
            raise RuntimeError('GAP batch metadata does not identify the owned campaign')
        if any(item['pgid'] == pid and item['pid'] not in owned for item in rows.values()):
            raise RuntimeError('A GAP process group contains an unrelated process')
        launcher = Path(command[0])
        if not launcher.is_absolute() or not launcher.is_file():
            raise RuntimeError('The recorded GAP launcher has no exact file identity')
        gaps.append(row)
        batches.append(dict(caseIDs=cases, host=row['host'], gapPID=pid,
                            runnerPID=runner['pid'], launchedCommand=command,
                            launcherPath=command[0], launcherSHA256=sha(launcher)))
    return captured, gaps, batches


def freeze_tree(runner, root, source, selection, captured, gaps, batches, output):
    """Freeze exact PIDs, rescan, then permit termination only after validation.

    No group signal is used during validation. On any failure only identities
    stopped here are resumed, and no termination signal is sent.
    """
    frozen = {}
    gap_rows = {row['pid']: row for row in gaps}
    batch_rows = {row['gapPID']: row for row in batches}

    def freeze(row):
        current = process(row['pid'])
        if not same_identity(row, current) or current['state'] == 'Z':
            return
        if current['state'] not in ('T', 't') and signal_one(row, signal.SIGSTOP):
            frozen[row['pid']] = row
        # STOP is asynchronous: observe the same identity stopped before scanning
        # its descendants. A vanished identity needs no further signal.
        deadline = time.monotonic() + 2.0
        while time.monotonic() < deadline:
            observed = process(row['pid'])
            if not same_identity(row, observed) or observed['state'] in ('T', 't', 'Z'):
                return
            time.sleep(0.01)
        raise RuntimeError('An owned process did not acknowledge its scheduling stop')

    try:
        freeze(runner)
        for attempt in range(6):
            rows = scan_owned(runner['uid'])
            observed, new_gaps, new_batches = validate_tree(rows, runner, root, source, selection)
            for pid, row in observed.items():
                if pid in captured and not same_identity(captured[pid], row):
                    raise RuntimeError('Captured PID identity changed during freeze')
                if pid not in captured or (row['argv'] and row.get('executablePath')):
                    captured[pid] = row
            for row in new_gaps:
                gap_rows[row['pid']] = row
            for row in new_batches:
                batch_rows[row['gapPID']] = row
            active = [row for row in observed.values() if row['state'] not in ('T', 't', 'Z')]
            if not active:
                return captured, list(gap_rows.values()), list(batch_rows.values())
            # Parents are frozen before any later-discovered descendants.
            for row in sorted(active, key=lambda x: (x['ppid'] != runner['pid'], x['pid'])):
                freeze(row)
            time.sleep(0.05)
        raise RuntimeError('Owned process tree did not become stably stopped')
    except BaseException as error:
        resumed = []
        for row in reversed(list(frozen.values())):
            if signal_one(row, signal.SIGCONT):
                resumed.append(row['pid'])
        write(output / 'validation_failure.json', dict(observedUTC=now(),
              error=type(error).__name__ + ': ' + str(error),
              terminationSignalsSent=False, resumedOwnedPIDs=resumed))
        raise


def verify_source_runtime(root, snapshot, source):
    """Verify the original recorded file list; never invent a newer manifest."""
    files = source.get('files')
    if (not isinstance(files, dict) or not files
            or source.get('sha256') != hashlib.sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode()).hexdigest()):
        raise RuntimeError('Campaign source manifest is invalid')
    for name, expected in files.items():
        path = Path(name)
        if (not isinstance(name, str) or not name or path.is_absolute()
                or str(path) != name or any(part in ('.', '..') for part in path.parts)
                or not isinstance(expected, str) or len(expected) != 64
                or any(c not in '0123456789abcdef' for c in expected)):
            raise RuntimeError('Unsafe source manifest entry')
        target = snapshot / path
        if snapshot not in target.resolve().parents or not target.is_file() or sha(target) != expected:
            raise RuntimeError('Original source snapshot file changed: ' + name)
    runtime_path = root / 'formula_runtime.json'
    runtime = dict(configured=False, reason='not_configured')
    if runtime_path.is_file():
        declared = json.loads(runtime_path.read_text())
        library = Path(declared.get('libraryPath', ''))
        present = declared.get('libraryPresent')
        expected = declared.get('librarySHA256')
        if not library.is_absolute() or type(present) is not bool:
            raise RuntimeError('Formula runtime manifest is malformed')
        if library.is_file() != present or (present and sha(library) != expected) or (not present and expected is not None):
            raise RuntimeError('Recorded formula runtime library changed')
        runtime = dict(configured=True, manifestSHA256=sha(runtime_path),
                       libraryPath=str(library), libraryPresent=present, librarySHA256=expected)
    return dict(sourceSnapshotVerified=True, verifiedSourceSHA256=source['sha256'],
                verifiedSourceFileCount=len(files), formulaRuntimeVerified=True,
                formulaRuntimeVerification=runtime)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--snapshot', required=True, type=Path)
    parser.add_argument('--runner-pid', required=True, type=int)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--replacement', required=True)
    args = parser.parse_args()
    root, snapshot = args.root.resolve(), args.snapshot.resolve()
    source_raw = (root / 'source.json').read_bytes()
    source = json.loads(source_raw)
    selection = json.loads((root / 'selection.json').read_text())
    runner = process(args.runner_pid)
    if (runner is None or runner['uid'] != os.getuid()
            or str(root) not in runner['argv']
            or str(snapshot / 'scripts/classify.py') not in runner['argv']):
        raise SystemExit('Runner identity does not match the exact owned campaign')
    output = args.output.resolve()
    if output == root or root in output.parents or output == snapshot or snapshot in output.parents:
        raise SystemExit('Stop evidence requires a new directory outside campaign and snapshot')
    if (not isinstance(selection, list) or not selection or len(selection) != len(set(selection))
            or any(not isinstance(case, str) or not case or Path(case).name != case for case in selection)):
        raise SystemExit('Campaign selection is invalid')
    if (not isinstance(source.get('files'), dict) or not source['files']
            or source.get('sha256') != hashlib.sha256(json.dumps(source['files'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()):
        raise SystemExit('Campaign source manifest is invalid')
    verify_source_runtime(root, snapshot, source)
    # Strict preflight: existing malformed child identities cause zero signals.
    captured, gaps, batches = validate_tree(scan_owned(runner['uid']), runner, root, source, selection)
    output.mkdir(parents=True, exist_ok=False)
    captured, gaps, batches = freeze_tree(runner, root, source, selection,
                                          captured, gaps, batches, output)
    before = [captured[pid] for pid in sorted(captured)]
    gap_ids = {row['pid'] for row in gaps}
    for row in before:
        row['role'] = 'runner' if row['pid'] == runner['pid'] else 'gap' if row['pid'] in gap_ids else 'formula-worker'
    write(args.output / 'processes_before.json', dict(observedUTC=now(), processes=before))
    for row in gaps:
        if same_identity(row, process(row['pid'])):
            try:
                os.killpg(row['pid'], signal.SIGTERM)
                os.killpg(row['pid'], signal.SIGCONT)
            except ProcessLookupError:
                pass
    time.sleep(3)
    for row in before:
        if row['pid'] != runner['pid']:
            signal_one(row, signal.SIGKILL)
    signal_one(runner, signal.SIGTERM)
    signal_one(runner, signal.SIGCONT)
    time.sleep(2)
    signal_one(runner, signal.SIGKILL)
    time.sleep(1)
    after, remaining = [], []
    for row in before:
        current = process(row['pid'])
        state = 'absent' if not same_identity(row, current) else 'zombie' if current['state'] == 'Z' else 'active'
        item = dict(row, observedState=state)
        after.append(item)
        if state == 'active':
            remaining.append(row['pid'])
    observed = now()
    write(args.output / 'processes_after.json', dict(observedUTC=observed, processes=after))
    artifacts = {}
    for name in ['source.json','selection.json','summary.json','formula_runtime.json','runtime_plan.json','runtime.json']:
        if (root / name).is_file():
            artifacts[name] = sha(root / name)
    for case in selection:
        for name in ['input.json','run.json','result.json','native.json','driver.g','stdout.log','stderr.log']:
            path = root / case / name
            if path.is_file():
                artifacts[str(path.relative_to(root))] = sha(path)
    for batch in batches:
        group = {row['pid'] for row in before if row['pgid'] == batch['gapPID']}
        batch.update(allOwnedDescendantsStopped=not bool(group & set(remaining)),
                     remainingOwnedPIDs=sorted(group & set(remaining)))
    captured_complete = [row for row in after if row.get('argv') and row.get('executablePath')]
    uncaptured_exited = [row for row in after if row not in captured_complete]
    if any(row['observedState'] not in ('absent','zombie') for row in uncaptured_exited):
        raise RuntimeError('An incompletely captured process is still active')
    if (root / 'source.json').read_bytes() != source_raw:
        raise RuntimeError('Campaign source manifest changed during stop')
    verification = verify_source_runtime(root, snapshot, source)
    write(args.output / 'source_verification.json', dict(observedUTC=now(), **verification))
    report = dict(schema='u1-paired-stop-v1', originalCampaignRoot=str(root),
                  sourceSHA256=source['sha256'], sourceSnapshotPath=str(snapshot),
                  stoppedObservedUTC=observed, allOwnedProcessesStopped=not remaining,
                  processes=captured_complete, uncapturedExitedProcesses=uncaptured_exited,
                  batches=batches, artifactsSHA256=artifacts,
                  replacement=args.replacement,
                  reason='Exact native primary, Smith-period and formula-DAG paths independently validated; preserve completed records and migrate unfinished cases',
                  evidence=[dict(path=name, sha256=sha(args.output / name))
                            for name in ['processes_before.json','processes_after.json','source_verification.json']],
                  **verification)
    write(args.output / 'cancellation.json', report)
    if remaining:
        raise SystemExit('Owned processes remain active: ' + repr(remaining))
    print(json.dumps(dict(root=str(root), stoppedGroups=len(gaps), stoppedProcesses=len(after),
                         artifactCount=len(artifacts), report=str(args.output / 'cancellation.json')), sort_keys=True))


if __name__ == '__main__':
    main()
