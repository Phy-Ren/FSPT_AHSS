#!/usr/bin/env python3
"""Replay the archived primary-class checks without modifying the evidence."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--gap', default='gap')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    evidence = Path(__file__).resolve().parent / 'independent'
    manifest = json.loads((evidence / 'source_manifest.json').read_text())
    args.output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix='u1-primary-replay-') as name:
        work = Path(name)
        for path, expected in manifest['sourceFiles'].items():
            data = subprocess.check_output(['git', 'show', manifest['u1Commit'] + ':' + path], cwd=args.repo)
            if hashlib.sha256(data).hexdigest() != expected:
                raise ValueError('Frozen source hash mismatch: ' + path)
            target = work / 'source' / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        for name in manifest['genericFiles']:
            shutil.copyfile(evidence / name, work / name)
        for stem in ('check', 'check_extra'):
            source = (evidence / (stem + '.g')).read_text()
            source = source.replace('REVIEW_ROOT:="/home/xingyu/AllFSPT_reviews/z2_charge_primary_reuse_20261015";',
                                    'REVIEW_ROOT:=' + json.dumps(str(work)) + ';')
            script = work / (stem + '.g')
            script.write_text(source)
            result = subprocess.run([args.gap, '-q', '-b', str(script)], capture_output=True, text=True, timeout=180)
            (args.output / (stem + '.log')).write_text(result.stdout + result.stderr)
            result.check_returncode()
        for name in ('result.json', 'result_extra.json'):
            shutil.copyfile(work / name, args.output / name)
    print('Both archived primary-class checks passed:', args.output)


if __name__ == '__main__':
    main()
