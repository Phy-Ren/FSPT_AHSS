#!/usr/bin/env python3
"""Preserve certified completed cases from an already stopped paired campaign.

This offline program never queries or signals a process. A separately captured
stop report supplies process-identity and stopped-state evidence. Raw inputs,
outputs, logs and original metadata are copied without alteration to a new
subset; a recovered result never receives a fabricated successful exit status.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SCHEMA = 'u1-paired-stop-v1'
RECOVERY_SCHEMA = 'u1-paired-recovery-v1'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON value')))


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def _relative(name):
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('Expected a safe relative artifact path')
    path = PurePosixPath(name)
    if path.is_absolute() or str(path) != name or any(x in ('', '.', '..') for x in path.parts):
        raise ValueError('Unsafe artifact path: ' + name)
    return name


def _case(case):
    if _relative(case) != PurePosixPath(case).name:
        raise ValueError('Invalid case ID')
    return case


def _hash(value):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
        raise ValueError('Expected a lowercase SHA256 digest')
    return value


def _timestamp(value):
    if not isinstance(value, str):
        raise ValueError('Missing observed UTC timestamp')
    stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0:
        raise ValueError('Timestamp must explicitly use UTC')
    return stamp


def _absolute(value):
    if not isinstance(value, str) or not value.startswith('/') or str(PurePosixPath(value)) != value:
        raise ValueError('Expected an absolute original path')
    if '..' in PurePosixPath(value).parts:
        raise ValueError('Original paths must not contain parent traversal')
    return value


def _positive(value, zero=False):
    if type(value) is not int or value < (0 if zero else 1):
        raise ValueError('Missing exact process identity integer')
    return value


def _argv(value):
    if not isinstance(value, list) or not value or any(not isinstance(x, str) or not x for x in value):
        raise ValueError('Missing exact argv vector')
    return value


def validate_stop_report(report):
    """Validate the supplied attestation, not the state of any live machine."""
    if report.get('schema') != SCHEMA or report.get('allOwnedProcessesStopped') is not True:
        raise ValueError('A confirmed stopped-campaign report is required')
    _absolute(report.get('originalCampaignRoot'))
    _absolute(report.get('sourceSnapshotPath'))
    _hash(report.get('sourceSHA256'))
    if report.get('sourceSnapshotVerified') is not True or report.get('verifiedSourceSHA256') != report['sourceSHA256']:
        raise ValueError('The original source-file list was not independently verified after stop')
    _timestamp(report.get('stoppedObservedUTC'))
    if not isinstance(report.get('artifactsSHA256'), dict):
        raise ValueError('Post-stop artifact hashes are required')
    for name, value in report['artifactsSHA256'].items():
        _relative(name)
        _hash(value)
    evidence = report.get('evidence')
    if not isinstance(evidence, list) or not evidence:
        raise ValueError('Raw process-observation evidence is required')
    seen = set()
    for item in evidence:
        name = _relative(item['path'])
        if name in seen or name == 'cancellation.json' or name.startswith('original_campaign/') or name.startswith('original_runs/'):
            raise ValueError('Duplicated or reserved process-evidence path')
        seen.add(name)
        _hash(item['sha256'])
    processes = {}
    for process in report.get('processes', []):
        host = process.get('host')
        if not isinstance(host, str) or not host:
            raise ValueError('Missing process host')
        for name in ('pid', 'pgid', 'startTicks'):
            _positive(process.get(name))
        for name in ('ppid', 'uid'):
            _positive(process.get(name), zero=True)
        _argv(process.get('argv'))
        if process.get('role') not in ('runner', 'gap', 'formula-worker', 'other'):
            raise ValueError('Unknown owned process role')
        if process.get('role') == 'runner' and (
                report['originalCampaignRoot'] not in process['argv']
                or str(PurePosixPath(report['sourceSnapshotPath']) / 'scripts/classify.py') not in process['argv']):
            raise ValueError('Runner argv does not identify the exact campaign and source snapshot')
        if process.get('observedState') not in ('absent', 'zombie'):
            raise ValueError('An owned process is not confirmed stopped')
        _absolute(process.get('executablePath'))
        _hash(process.get('executableSHA256'))
        key = (host, process['pid'])
        if key in processes:
            raise ValueError('Duplicate process identity')
        processes[key] = process
    if not processes or not any(p['role'] == 'runner' for p in processes.values()):
        raise ValueError('The stopped campaign runner identity is required')
    batches = {}
    for batch in report.get('batches', []):
        cases = batch.get('caseIDs')
        if not isinstance(cases, list) or len(cases) != 2 or len(set(cases)) != 2:
            raise ValueError('A captured batch must name exactly two ordered case IDs')
        for case in cases:
            _case(case)
        host = batch.get('host')
        gap = processes.get((host, batch.get('gapPID')))
        runner = processes.get((host, batch.get('runnerPID')))
        if gap is None or runner is None or gap['role'] != 'gap' or runner['role'] != 'runner':
            raise ValueError('A batch lacks its exact stopped GAP and runner identities')
        if gap['uid'] != runner['uid'] or gap['pid'] == runner['pid']:
            raise ValueError('Batch processes must have one owner and distinct identities')
        cursor, visited = gap, set()
        while cursor['pid'] != runner['pid']:
            if cursor['pid'] in visited or cursor['uid'] != runner['uid']:
                raise ValueError('Invalid owned parent chain')
            visited.add(cursor['pid'])
            cursor = processes.get((host, cursor['ppid']))
            if cursor is None:
                raise ValueError('The captured GAP parent chain does not reach the runner')
        if batch.get('allOwnedDescendantsStopped') is not True or batch.get('remainingOwnedPIDs') != []:
            raise ValueError('The batch process tree is not confirmed stopped')
        launched = _argv(batch.get('launchedCommand'))
        _absolute(batch.get('launcherPath'))
        _hash(batch.get('launcherSHA256'))
        if batch['launcherPath'] != launched[0] or len(launched) < 2:
            raise ValueError('Launcher identity differs from the recorded command')
        if len(gap['argv']) < len(launched) or gap['argv'][-len(launched[1:]):] != launched[1:]:
            raise ValueError('Actual GAP argv lacks the exact launched-command suffix')
        for case in cases:
            if case in batches:
                raise ValueError('Case occurs in multiple captured batches')
            batches[case] = batch
    return batches


class OriginalArtifacts:
    def __init__(self, root, report):
        self.root, self.report, self.cache = root, report, {}

    def __call__(self, name):
        _relative(name)
        if name not in self.cache:
            path = self.root / name
            if path.is_symlink() or not path.is_file():
                raise ValueError('Missing regular original artifact: ' + name)
            raw = path.read_bytes()
            if self.report['artifactsSHA256'].get(name) != sha(raw):
                raise ValueError('Missing or mismatched post-stop artifact hash: ' + name)
            self.cache[name] = raw
        return self.cache[name]

    def unchanged(self):
        for name, raw in self.cache.items():
            if (self.root / name).read_bytes() != raw:
                raise ValueError('Original artifact changed during preservation: ' + name)


def _campaign(read_raw, report):
    source = parse(read_raw('source.json'))
    selection = parse(read_raw('selection.json'))
    if not isinstance(selection, list) or not selection or len(selection) != len(set(selection)):
        raise ValueError('Invalid original campaign selection')
    for case in selection:
        _case(case)
    if not isinstance(source.get('files'), dict) or not source['files']:
        raise ValueError('Invalid original source manifest')
    actual = sha(json.dumps(source['files'], sort_keys=True, separators=(',', ':')).encode())
    if source.get('sha256') != actual or report['sourceSHA256'] != actual:
        raise ValueError('Original source manifest does not match the stopped campaign')
    return source, selection


def scientific_checks(native, data):
    """Independent integer checks plus required saved solver certificates."""
    from scripts.collect_expansion import presentation_check, filling_check
    if not isinstance(native, dict) or not isinstance(data, dict):
        raise ValueError('Native output and catalog input must be JSON objects')
    if data.get('family') != 'spacegroup' or data.get('dimension') != 3:
        raise ValueError('Recovery currently covers paired 3+1D space groups only')
    if (native.get('theory') != 'U(1)^f insulator' or native.get('spatialDimension') != 3
            or not isinstance(native.get('scope'), str) or not native['scope']):
        raise ValueError('Missing native dimensional/scope identity')
    count = native.get('presentationGeneratorCount')
    if type(count) is not int or count < 0 or type(native.get('freeRank')) is not int:
        raise ValueError('Malformed integer presentation dimensions')
    if not isinstance(native.get('presentation'), list) or any(
            not isinstance(row, list) or len(row) != count or any(type(x) is not int for x in row)
            for row in native['presentation']):
        raise ValueError('Malformed integer presentation')
    if not isinstance(native.get('torsion'), list) or any(type(x) is not int or x <= 1 for x in native['torsion']):
        raise ValueError('Malformed Smith invariant factors')
    if not isinstance(native.get('generators'), list) or len(native['generators']) != count:
        raise ValueError('Missing complete root list')
    dimensions = native.get('resolutionDimensions')
    if not isinstance(dimensions, list) or len(dimensions) < 6 or any(type(x) is not int or x < 0 for x in dimensions):
        raise ValueError('Missing native resolution dimensions')
    for generator in native['generators']:
        if not isinstance(generator, dict):
            raise ValueError('Malformed completed root')
        fields = {'phase': [('nativePhase', 4)],
                  'charge': [('nativeCharge', 3), ('nativePhase', 4)],
                  'CI': [('nativeSheet', 1), ('nativeCharge', 3), ('nativePhase', 4)]}.get(generator.get('kind'))
        if fields is None:
            raise ValueError('Unknown completed root kind')
        for key, degree in fields:
            vector = generator.get(key)
            if not isinstance(vector, list) or len(vector) != dimensions[degree]:
                raise ValueError('Incomplete native root vector: ' + key)
            if any(type(x) not in (int, str) for x in vector):
                raise ValueError('Native root entries must be exact integer/rational scalars')
            values = [Fraction(x) for x in vector]
            if key != 'nativePhase' and any(x.denominator != 1 for x in values):
                raise ValueError('Integer decoration contains a noninteger root entry')
    for name in ('witnesses', 'gaugeReductionWitnesses'):
        if not isinstance(native.get(name), list) or any(not isinstance(x, dict) for x in native[name]):
            raise ValueError('Missing or malformed saved root/gauge witnesses')
    if type(native.get('nativeCompletionChecks')) is not int or native['nativeCompletionChecks'] < 1:
        raise ValueError('Missing completed-state certificate')
    if native.get('nativeChainIdentitiesVerified') is not True:
        raise ValueError('Missing native chain-map certificate')
    validation = native.get('inputValidation')
    if not isinstance(validation, dict) or validation.get('independentCharactersChecked') is not True:
        raise ValueError('Missing coefficient-character certificate')
    return {'independentSmithGroup': presentation_check(native),
            'independentPresentationFillingCheck': filling_check(native),
            'nativeCompletionChecks': native['nativeCompletionChecks'],
            'nativeChainIdentitiesVerified': True, 'completeWitnessListsPresent': True}


def _inspect_case(read_raw, report, batches, source, selection, case):
    prefix = case + '/'
    data, run = parse(read_raw(prefix + 'input.json')), parse(read_raw(prefix + 'run.json'))
    native = parse(read_raw(prefix + 'native.json'))
    if not all(isinstance(x, dict) for x in (data, run, native)):
        raise ValueError('Input, run, and native output must be JSON objects')
    if data.get('id') != case or run.get('id') != case:
        raise ValueError('Case input/run identity mismatch')
    if run.get('inputSHA256') != sha(read_raw(prefix + 'input.json')) or run.get('sourceSHA256') != source['sha256']:
        raise ValueError('Original input/source hash mismatch')
    pair = run.get('batchCaseIDs')
    if (run.get('pairedSpins') is not True or not isinstance(pair, list) or len(pair) != 2
            or len(set(pair)) != 2 or case not in pair or not set(pair) <= set(selection)):
        raise ValueError('Missing original ordered paired-batch metadata')
    for item in pair:
        _case(item)
    command = _argv(run.get('command'))
    expected_driver = str(PurePosixPath(report['originalCampaignRoot']) / pair[0] / 'driver.g')
    if command[-1] != expected_driver:
        raise ValueError('Original command does not target the captured campaign driver')
    driver_raw = read_raw(prefix + 'driver.g')
    driver = driver_raw.decode('utf-8')
    root_match = re.search(r'^U1_ROOT:=("(?:[^"\\]|\\.)*");;', driver)
    if root_match is None or json.loads(root_match.group(1)) != report['sourceSnapshotPath']:
        raise ValueError('Driver does not use the captured immutable source snapshot')
    if driver_raw != read_raw(pair[0] + '/driver.g'):
        raise ValueError('Paired driver copies differ')
    # The marker must be an entire output line, emitted only after closing the
    # native JSON stream in this driver. A substring/partial line is insufficient.
    marker = ('U1_PAIR_CASE_DONE ' + case).encode()
    stdout_name, stderr_name = pair[0] + '/stdout.log', pair[0] + '/stderr.log'
    stdout = read_raw(stdout_name)
    read_raw(stderr_name)
    if sum(line in (marker + b'\n', marker + b'\r\n') for line in stdout.splitlines(keepends=True)) != 1:
        raise ValueError('Missing or duplicated durable driver completion marker')
    close_marker = 'CloseStream(output);;\nPrint("U1_PAIR_CASE_DONE ",U1_INPUT.id,"\\n");;'
    if driver.count(close_marker) != 2:
        raise ValueError('Driver does not emit completion markers after closing native output')
    checks = scientific_checks(native, data)
    base = {'case': case, 'input': data, 'originalRun': run, 'classification': native,
            'pair': pair, 'stdoutSource': stdout_name, 'stderrSource': stderr_name, 'checks': checks}
    if run.get('status') == 'complete' and run.get('exitCode') == 0:
        result = parse(read_raw(prefix + 'result.json'))
        if result.get('run') != run or result.get('input') != data or result.get('classification') != native:
            raise ValueError('Existing completed result is inconsistent')
        base['kind'] = 'ordinary_complete'
        return base
    # Existing failed/incomplete result wrappers are never silently replaced.
    if prefix + 'result.json' in report['artifactsSHA256']:
        raise ValueError('An existing noncomplete result requires a separate review')
    batch = batches.get(case)
    if batch is None:
        raise ValueError('No captured stopped GAP identity for this incomplete paired run')
    if batch['caseIDs'] != pair or batch['host'] != run.get('host') or batch['launchedCommand'] != command:
        raise ValueError('Captured process batch differs from original run metadata')
    if _timestamp(report['stoppedObservedUTC']) < _timestamp(run.get('startedUTC')):
        raise ValueError('Observed process stop predates the original run')
    base['kind'] = 'recovered_complete'
    return base


def _recovered_run(case, original, report, report_hash, original_run_hash):
    # These are recovery metadata, not evidence of an execution exit or a
    # completion time. Preserve all original execution metadata separately.
    return {'id': case, 'status': 'recovered_complete',
            'operation': 'offline-paired-native-recovery',
            'inputSHA256': original['inputSHA256'], 'sourceSHA256': original['sourceSHA256'],
            'pairedSpins': True, 'batchCaseIDs': original['batchCaseIDs'],
            'originalCampaignRoot': report['originalCampaignRoot'],
            'originalRunSHA256': original_run_hash,
            'cancellationReportSHA256': report_hash,
            'executionExitStatus': 'not_inferred_from_native_completion',
            'completionEvidence': 'closed native output followed by exact driver marker'}


def preserve_campaign(campaign, report_path, output, cases=None):
    campaign, report_path, output = Path(campaign).resolve(), Path(report_path).resolve(), Path(output).resolve()
    if output.exists() or output == campaign or campaign in output.parents:
        raise ValueError('Recovery requires a new output outside the original campaign')
    report_raw = report_path.read_bytes()
    report = parse(report_raw)
    batches = validate_stop_report(report)
    evidence = {}
    for item in report['evidence']:
        path = report_path.parent / item['path']
        if path.is_symlink() or not path.is_file():
            raise ValueError('Process-observation evidence is missing or changed')
        raw = path.read_bytes()
        if sha(raw) != item['sha256']:
            raise ValueError('Process-observation evidence is missing or changed')
        evidence[item['path']] = raw
    read_raw = OriginalArtifacts(campaign, report)
    source, selection = _campaign(read_raw, report)
    if (campaign / 'formula_runtime.json').is_file() and report.get('formulaRuntimeVerified') is not True:
        raise ValueError('The original optional formula runtime was not verified after stop')
    requested = selection if cases is None else list(cases)
    if not requested or len(set(requested)) != len(requested) or not set(requested) <= set(selection):
        raise ValueError('Requested cases must be distinct members of the original selection')
    accepted, retries = [], []
    for case in requested:
        try:
            existing = campaign / case / 'result.json'
            if existing.exists() and case + '/result.json' not in report['artifactsSHA256']:
                raise ValueError('Existing result wrapper is omitted from the stop report')
            accepted.append(_inspect_case(read_raw, report, batches, source, selection, case))
        except (KeyError, ValueError, TypeError, IndexError, OSError, ArithmeticError) as error:
            retries.append({'id': case, 'reason': type(error).__name__ + ': ' + str(error)})
    read_raw.unchanged()
    if report_path.read_bytes() != report_raw:
        raise ValueError('Stop report changed during preservation')
    payload, copied = {}, {}

    def copy(name, destination=None):
        destination = name if destination is None else destination
        payload[destination] = read_raw(name)
        copied[destination] = name

    copy('source.json')
    copy('selection.json', '_recovery/original_campaign/selection.json')
    for name in ('summary.json', 'formula_runtime.json', 'runtime_plan.json'):
        if (campaign / name).is_file():
            copy(name, '_recovery/original_campaign/' + name)
    for item in accepted:
        case, prefix = item['case'], item['case'] + '/'
        for name in ('input.json', 'native.json', 'driver.g'):
            copy(prefix + name)
        # Preserve the actual original stream bytes even if the externally
        # terminated parent never copied them to the second case directory.
        copy(item['stdoutSource'], prefix + 'stdout.log')
        copy(item['stderrSource'], prefix + 'stderr.log')
        copy(item['pair'][0] + '/driver.g', '_recovery/original_runs/' + item['pair'][0] + '/driver.g')
        if item['kind'] == 'ordinary_complete':
            copy(prefix + 'run.json')
            copy(prefix + 'result.json')
        else:
            copy(prefix + 'run.json', '_recovery/original_runs/' + prefix + 'run.json')
            run = _recovered_run(case, item['originalRun'], report, sha(report_raw), sha(read_raw(prefix + 'run.json')))
            payload[prefix + 'run.json'] = encoded(run)
            payload[prefix + 'result.json'] = encoded({'input': item['input'], 'classification': item['classification'], 'run': run})
    payload['_recovery/cancellation.json'] = report_raw
    for name, raw in evidence.items():
        payload['_recovery/' + name] = raw
    payload['selection.json'] = encoded([item['case'] for item in accepted])
    payload['retry.json'] = encoded(retries)
    ledger = {'schema': RECOVERY_SCHEMA, 'preparedUTC': datetime.now(timezone.utc).isoformat(),
              'originalCampaignRoot': report['originalCampaignRoot'],
              'cancellationReportSHA256': sha(report_raw), 'sourceSHA256': source['sha256'],
              'requestedCases': requested, 'preservedCases': [item['case'] for item in accepted],
              'recoveredCases': [item['case'] for item in accepted if item['kind'] == 'recovered_complete'],
              'ordinaryCompleteCases': [item['case'] for item in accepted if item['kind'] == 'ordinary_complete'],
              'retryCases': [item['id'] for item in retries],
              'copiedFromOriginal': copied,
              'checks': {item['case']: item['checks'] for item in accepted},
              'filesSHA256': {name: sha(raw) for name, raw in payload.items()},
              'recoveryHelperSHA256': sha(Path(__file__).read_bytes())}
    payload['recovery.json'] = encoded(ledger)
    read_raw.unchanged()
    if report_path.read_bytes() != report_raw or any(
            (report_path.parent / name).read_bytes() != raw for name, raw in evidence.items()):
        raise ValueError('Stop evidence changed during preservation')
    output.mkdir(parents=True, exist_ok=False)
    for name, raw in payload.items():
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    return ledger


def validate_recovered_case(root, case):
    """Recheck a recovered record from copied evidence without the old campaign."""
    root = Path(root)
    _case(case)
    ledger = parse((root / 'recovery.json').read_bytes())
    if ledger.get('schema') != RECOVERY_SCHEMA or case not in ledger.get('recoveredCases', []):
        raise ValueError('Missing explicit recovery ledger for the selected case')
    report_raw = (root / '_recovery/cancellation.json').read_bytes()
    if sha(report_raw) != ledger.get('cancellationReportSHA256'):
        raise ValueError('Recovery report hash mismatch')
    report = parse(report_raw)
    batches = validate_stop_report(report)
    for name, expected in ledger['filesSHA256'].items():
        _relative(name)
        path = root / name
        if path.is_symlink() or sha(path.read_bytes()) != expected:
            raise ValueError('Preserved recovery artifact changed: ' + name)
    for item in report['evidence']:
        if sha((root / '_recovery' / item['path']).read_bytes()) != item['sha256']:
            raise ValueError('Preserved process evidence differs from the report')
    originals = {}
    for destination, original in ledger['copiedFromOriginal'].items():
        _relative(destination)
        _relative(original)
        raw = (root / destination).read_bytes()
        if report['artifactsSHA256'].get(original) != sha(raw):
            raise ValueError('Preserved raw bytes differ from the stopped-campaign hash')
        if original in originals and originals[original] != raw:
            raise ValueError('Inconsistent copies of an original artifact')
        originals[original] = raw

    def read_raw(name):
        if name not in originals:
            raise ValueError('Missing copied original evidence: ' + name)
        return originals[name]

    source, selection = _campaign(read_raw, report)
    if 'formula_runtime.json' in originals and report.get('formulaRuntimeVerified') is not True:
        raise ValueError('Missing original formula-runtime verification')
    item = _inspect_case(read_raw, report, batches, source, selection, case)
    if item['kind'] != 'recovered_complete' or item['checks'] != ledger['checks'][case]:
        raise ValueError('Recovered scientific checks changed')
    expected = _recovered_run(case, item['originalRun'], report, sha(report_raw), sha(read_raw(case + '/run.json')))
    run, result = parse((root / case / 'run.json').read_bytes()), parse((root / case / 'result.json').read_bytes())
    if run != expected or result != {'input': item['input'], 'classification': item['classification'], 'run': expected}:
        raise ValueError('Recovered wrapper changed or fabricates execution evidence')
    return dict(item['checks'], recoveredComplete=True, cancellationReportSHA256=sha(report_raw),
                driverCompletionMarkerVerified=True, capturedProcessTreeStopped=True,
                originalInputSourceAndNativeBytesVerified=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--campaign', type=Path, required=True)
    parser.add_argument('--stop-report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--case', action='append')
    args = parser.parse_args()
    ledger = preserve_campaign(args.campaign, args.stop_report, args.output, args.case)
    print(json.dumps({key: ledger[key] for key in ('preservedCases', 'recoveredCases', 'ordinaryCompleteCases', 'retryCases')}, indent=2))


if __name__ == '__main__':
    main()
