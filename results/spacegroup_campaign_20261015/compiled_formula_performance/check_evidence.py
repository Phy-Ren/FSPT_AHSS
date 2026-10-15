#!/usr/bin/env python3
"""Verify frozen evidence; optionally replay all 19,099 original worker inputs."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(name):
    return json.loads((HERE / name).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--mode', choices=('auto', 'python', 'reference'), default='auto')
    args = parser.parse_args()
    manifest = read('artifact_manifest.json')
    for name, expected in manifest['files'].items():
        assert digest((HERE / name).read_bytes()) == expected, name
    raw = gzip.decompress((HERE / 'full_requests.jsonl.gz').read_bytes())
    provenance = read('provenance.json')
    assert digest(raw) == provenance['requests']['uncompressed_sha256']
    assert len(raw.splitlines()) == provenance['requests']['count']
    a, b = read('sg14_reference/native.json'), read('sg14_compiled/native.json')
    for result in (a, b):
        result.pop('resolutionBuildTimings', None)
    assert a == b, 'Complete native records differ'
    normalized = digest(json.dumps(b, sort_keys=True, separators=(',', ':')).encode())
    assert normalized == read('sg14_equivalence.json')['normalized_native_sha256']
    assert read('sg14_reference/input.json') == read('sg14_compiled/input.json')
    replay = read('full_replay.json')
    assert len({v['responses_sha256'] for v in replay['modes'].values()}) == 1
    for operation, info in provenance['compiled_programs'].items():
        data = json.loads((ROOT / 'insulator/_compiled' / (operation + '3.json')).read_text())
        payload = {k: data[k] for k in ('program', 'output', 'denominator', 'full_uncompacted_nodes')}
        assert digest(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()) == info['payload_sha256']
    result = {'status': 'PASS', 'files': len(manifest['files']),
              'full_native_equality': True, 'captured_requests': len(raw.splitlines())}
    if args.replay:
        sys.path.insert(0, str(ROOT))
        os.environ['U1_DAG_MODE'] = args.mode
        from insulator.worker import _evaluate
        start = time.process_time()
        responses = hashlib.sha256()
        for line in raw.splitlines():
            request = json.loads(line)
            try:
                response = {'ok': True, 'result': _evaluate(request)}
            except Exception as error:
                response = {'ok': False, 'error': type(error).__name__ + ': ' + str(error)}
            responses.update(json.dumps(response, sort_keys=True, separators=(',', ':')).encode() + b'\n')
        assert responses.hexdigest() == replay['modes']['reference']['responses_sha256']
        rational = gzip.decompress((HERE / 'rational_requests.jsonl.gz').read_bytes()).splitlines()
        expected = read('rational_responses.json')['results']
        for line, old in zip(rational, expected):
            assert {'ok': True, 'result': _evaluate(json.loads(line))} == old
        assert len(rational) == len(expected) == 36
        result.update(replay_mode=args.mode, cpu_seconds=time.process_time() - start,
                      responses_sha256=responses.hexdigest(), rational_responses_equal=36)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
