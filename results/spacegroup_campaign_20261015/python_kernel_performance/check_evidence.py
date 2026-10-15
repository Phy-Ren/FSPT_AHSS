#!/usr/bin/env python3
"""Check exact archived request responses, native roots, and artifact hashes."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def scientific(value):
    if isinstance(value, dict):
        return {k: scientific(v) for k, v in value.items()
                if k != 'resolutionBuildTimings'}
    if isinstance(value, list):
        return [scientific(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.directory
    read = lambda name: json.loads((root / name).read_text())
    manifest = read('artifact_manifest.json')
    for item in manifest['files']:
        data = (root / item['path']).read_bytes()
        assert len(data) == item['bytes'], item['path']
        assert sha(data) == item['sha256'], item['path']
    meta = read('metadata.json')
    for item in meta['compressed_captures']:
        raw = (root / item['file']).read_bytes()
        assert sha(raw) == item['compressed_sha256']
        data = gzip.decompress(raw)
        assert sha(data) == item['uncompressed_sha256']
        assert len(data) == item['uncompressed_bytes']
        assert len(data.splitlines()) == item['requests']
    baseline = read('replay-baseline.json')['results']
    for name in ['replay-canonical-int.json', 'replay-int-cup-plan.json',
                 'replay-int-cup-boundary.json']:
        assert read(name)['results'] == baseline, name
    assert len(baseline) == 1473 and all(r['ok'] for r in baseline)
    replay_digest = sha(json.dumps(baseline, sort_keys=True).encode())
    assert replay_digest == '8c51566473e69c1f8ebc71179467ac96a89c5b46b1c35a46b8957781f13bd3ea'
    rational = read('signed-rational-baseline.json')['results']
    assert read('signed-rational-candidate-boundary.json')['results'] == rational
    assert len(rational) == 36 and all(r['ok'] for r in rational)
    old_source = read('sg14_baseline/source.json')
    new_source = read('sg14_candidate/source.json')
    assert set(old_source['files']) == set(new_source['files'])
    changed = [k for k in old_source['files']
               if old_source['files'][k] != new_source['files'][k]]
    assert changed == ['insulator/_engine/simplex.py'], changed
    for name, source in [('baseline', old_source), ('candidate', new_source)]:
        assert source['sha256'] == read('sg14_' + name + '/run.json')['sourceSHA256']
    old_native = read('sg14_baseline/native.json')
    new_native = read('sg14_candidate/native.json')
    assert scientific(old_native) == scientific(new_native)
    assert old_native['formulaWorkerCalls'] == 19418
    old = read('sg14_baseline/result.json')
    new = read('sg14_candidate/result.json')
    assert old['input'] == new['input']
    assert scientific(old['classification']) == scientific(new['classification'])
    digest = sha(json.dumps(scientific(old_native), sort_keys=True,
                            separators=(',', ':')).encode())
    assert digest == read('sg14_full_equivalence.json')['native_scientific_sha256']
    result = {'status': 'PASS', 'verified_manifest_files': len(manifest['files']),
              'identical_sg14_replay_responses': len(baseline),
              'successful_identical_rational_responses': len(rational),
              'native_equal_except_resolution_timing': True,
              'all_19418_calls_and_cache_statistics_equal': True,
              'scientific_native_sha256': digest,
              'replay_response_sha256': replay_digest}
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
