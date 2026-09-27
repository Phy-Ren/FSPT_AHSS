#!/usr/bin/env python3
"""Compute one finite 3D point group; preserve input matrices and frozen source."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


def matrix_metadata(record):
    matrices = record['point_group']['matrices']
    canonical = json.dumps(sorted(matrices), separators=(',', ':')).encode()
    record['point_group']['matrix_set_sha256'] = hashlib.sha256(canonical).hexdigest()
    record['point_group']['matrix_hash_encoding'] = 'UTF-8 compact JSON of lexicographically sorted integer matrices'
    return record


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('group', type=int)
    ap.add_argument('--crystalline-spin', choices=['half', 'spinless'], required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--source', type=Path, help='Frozen runtime containing gap/')
    args = ap.parse_args(argv)
    if not 1 <= args.group <= 32:
        ap.error('point-group index must be 1..32')
    root = Path(__file__).resolve().parents[1]
    out = args.output.resolve()
    raw, driver = out.with_suffix('.raw.json'), out.with_suffix('.g')
    checkpoint = out.parent/'classification'/out.name
    for p in (out, raw, driver, checkpoint):
        if p.exists() or p.is_symlink():
            ap.error('refuse existing output: '+str(p))
    source = args.source.resolve() if args.source else out.with_suffix('.source')
    if not args.source:
        if source.exists() or source.is_symlink():
            ap.error('source snapshot exists')
        shutil.copytree(root/'gap', source/'gap')
    files = sorted((source/'gap').glob('*.g'))
    if not (source/'gap/run_point_group.g').is_file() or not files:
        ap.error('finite driver missing from source snapshot')
    hashes = {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    source_id = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    out.parent.mkdir(parents=True, exist_ok=True)
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    variables = {'AFS_ROOT': str(source), 'AFS_PG': args.group, 'AFS_OUT': str(raw),
                 'AFS_CLASS_OUT': str(checkpoint), 'AFS_SOURCE_ID': source_id,
                 'AFS_CRYSTALLINE_SPIN': args.crystalline_spin}
    driver.write_text(''.join('%s := %s;;\n' % (key, json.dumps(value)) for key, value in variables.items())
                      +'Read(%s);\n' % json.dumps(str(source/'gap/run_point_group.g')))
    started = time.time()
    code = subprocess.call([sys.executable, str(root/'scripts/run_gap.py'),
                            '--sentinel', 'AFS_POINT_GROUP_WRITTEN', str(driver)])
    if code or not raw.is_file() or not checkpoint.is_file():
        return code or 1
    result = json.loads(raw.read_bytes())
    check = json.loads(checkpoint.read_bytes())
    for data in (result, check):
        if data.get('point_group_index') != args.group or data.get('crystalline_spin') != args.crystalline_spin:
            raise ValueError('wrong finite point-group result')
        if 'space_group' in data or data['point_group']['translationSubgroupPresent']:
            raise ValueError('affine result in finite point-group runner')
        matrix_metadata(data)
    result.update(wall_seconds=time.time()-started, started=started, finished=time.time(),
                  source_sha256=hashes, source_id=source_id, source_snapshot=str(source), mode='full')
    # The untouched GAP outputs remain available: the classification checkpoint
    # adds only a deterministic matrix-set digest in this Python wrapper.
    check_raw = checkpoint.with_suffix('.raw.json')
    if check_raw.exists() or check_raw.is_symlink():
        raise ValueError('checkpoint raw evidence exists')
    checkpoint.replace(check_raw)
    checkpoint.write_text(json.dumps(check, indent=2, sort_keys=True)+'\n')
    temporary = out.with_suffix('.tmp')
    if temporary.exists() or temporary.is_symlink():
        raise ValueError('temporary output exists')
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    temporary.replace(out)
    print('AFS_POINT_GROUP_SAVED', args.group, args.crystalline_spin, result['status'], str(out), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
