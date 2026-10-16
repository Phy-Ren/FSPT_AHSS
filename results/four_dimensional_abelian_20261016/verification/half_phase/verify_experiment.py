"""Reproduce the isolated charge-completion parity/provenance audit."""
from pathlib import Path
import hashlib
import json
import re
import tarfile
import tempfile

ARTIFACT_ROOT = Path(__file__).resolve().parent
workspace = tempfile.TemporaryDirectory(prefix='abelian-half-phase-replay-')
with tarfile.open(ARTIFACT_ROOT / 'snapshot_and_runs.tar.gz') as archive:
    archive.extractall(workspace.name, filter='data')
ROOT = Path(workspace.name) / 'abelian_half_phase_review_20261016'
PRIOR = ARTIFACT_ROOT.parent / 'native_benchmark/bar'
EXCLUDED = ['closedChargeCompletionMode']

def read(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def normalize(value):
    return {key: item for key, item in value.items() if key not in EXCLUDED}

report = {'status': 'PASS', 'classificationParityExcludedKeys': EXCLUDED,
          'classificationParityIncludesRuntimeAndFormulaWorkerCalls': True,
          'sourceManifests': {}, 'cases': [], 'sourceControl': read(ARTIFACT_ROOT / 'source_control.json')}
assert report['sourceControl']['status'] == 'PASS'
assert digest(ARTIFACT_ROOT / 'snapshot_and_runs.tar.gz') == 'd3429db6ccc77586c88a1c610cb7cc1cf24b1b40334d06f6db6729562105af80'
for label in ('baseline', 'candidate'):
    raw = ROOT / (label + '_raw')
    manifest = read(raw / 'source.json')
    assert canonical_digest(manifest['files']) == manifest['sha256']
    for path, expected in manifest['files'].items():
        assert digest(ROOT / label / path) == expected, (label, path)
    campaign = read(raw / 'campaign.json')
    assert campaign == {'status': 'complete', 'cases': 2, 'sourceSHA256': manifest['sha256']}
    report['sourceManifests'][label] = {'sha256': manifest['sha256'], 'verifiedFiles': len(manifest['files'])}
    expected_selection = ['internal_abelian_2x2_4p1', 'internal_abelian_2x2x2_4p1']
    selection = read(raw / 'selection.json')
    assert selection == expected_selection, selection

for factors in ('2x2', '2x2x2'):
    identifier = f'internal_abelian_{factors}_4p1'
    records = {}
    runs = {}
    stages = {}
    for label in ('baseline', 'candidate'):
        directory = ROOT / (label + '_raw') / identifier
        result = read(directory / 'result.json')
        run = read(directory / 'run.json')
        inputs = read(directory / 'input.json')
        native = read(directory / 'native.json')
        assert result['input'] == inputs
        assert result['run'] == run
        assert result['classification'] == native
        assert run['inputSHA256'] == digest(directory / 'input.json')
        assert run['sourceSHA256'] == report['sourceManifests'][label]['sha256']
        assert run['exitCode'] == 0 and run['status'] == 'complete'
        assert run['elapsedSeconds'] < 300
        records[label] = result
        runs[label] = run
        stages[label] = {name: int(cpu) for name, cpu in re.findall(
            r'U1_ABELIAN stage=(\w+)(?:(?!U1_ABELIAN).)*?cpu_ms=(\d+)',
            (directory / 'stdout.log').read_text(), re.S)}
    assert records['baseline']['input'] == records['candidate']['input']
    baseline = records['baseline']['classification']
    candidate = records['candidate']['classification']
    prior = read(PRIOR / identifier / 'result.json')['classification']
    assert baseline == normalize(candidate)
    assert baseline == prior
    assert candidate['closedChargeCompletionMode'] == 'certified'
    timings = {label: runs[label]['elapsedSeconds'] for label in runs}
    report['cases'].append({
        'id': identifier,
        'allClassificationFieldsEqual': True,
        'allSavedNativeFieldsEqual': True,
        'previousImmutableBarClassificationEqual': True,
        'canonicalClassificationSHA256': canonical_digest(baseline),
        'classificationFieldCount': len(baseline),
        'formulaWorkerCalls': baseline['formulaWorkerCalls'],
        'wallSeconds': timings,
        'candidateOverBaselineWallRatio': timings['candidate'] / timings['baseline'],
        'gapStageEntryCPUms': stages,
        'chargeCompletionCPUms': {label: stage['root_relations'] - stage['charge_lifts']
                                  for label, stage in stages.items()},
        'rawFileSHA256': {label: {name: digest(ROOT / (label + '_raw') / identifier / name)
                         for name in ('input.json', 'run.json', 'native.json', 'result.json', 'stdout.log', 'stderr.log')}
                         for label in ('baseline', 'candidate')},
    })
base_files = read(ROOT / 'baseline_raw/source.json')['files']
candidate_files = read(ROOT / 'candidate_raw/source.json')['files']
changed = [name for name in sorted(base_files.keys() | candidate_files.keys())
           if base_files.get(name) != candidate_files.get(name)]
assert changed == ['gap/abelian4p1.g', 'gap/charge_source.g', 'scripts/classify_abelian_4p1.py'], changed
report['changedSnapshotFiles'] = changed
report['recommendation'] = 'Do not adopt this isolated shortcut alone: complete-run wall time showed no speedup. Preserve prototype for future cache/completion integration.'
(ARTIFACT_ROOT / 'parity_and_timings.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': report['status'], 'cases': len(report['cases']), 'sourceManifests': report['sourceManifests']}, indent=2))
