#!/usr/bin/env python3
"""Export or check frozen manuscript equations from the maintained source."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def manuscript_tex(text):
    """Typography only: mathematical tokens and input order are preserved."""
    return (text.replace('𝒪', 'O').replace('ℰ', 'E')
            .replace(r'\mathop{\mathrm{MS}}\nolimits', r'\smile')
            .replace(r'\operatorname{MS}', r'\smile'))


def update(path, check):
    data = json.loads(path.read_text())
    records = data.get('equations', data.get('files', []))
    if not records:
        raise ValueError(f'No equation records in {path}')
    changed = []
    for record in records:
        if 'source' in record:
            source = ROOT / record['source']
        else:
            source = ROOT / data['source_directory'] / record['file']
        if 'output' in record:
            manuscript_root = next(p for p in path.parents if (p / 'equations').is_dir())
            target = manuscript_root / record['output']
            checksum_key = 'output_sha256'
        else:
            target = path.parent / record.get('target', record.get('file'))
            checksum_key = 'target_sha256' if 'target' in record else 'export_sha256'
        source_text = source.read_text()
        exported = manuscript_tex(source_text)
        source_hash = sha256(source_text.encode()).hexdigest()
        export_hash = sha256(exported.encode()).hexdigest()
        stale = (not target.exists() or target.read_text() != exported or
                 record.get('source_sha256') != source_hash or
                 record.get(checksum_key) != export_hash)
        if stale:
            changed.append(str(target))
            if not check:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(exported)
                record['source_sha256'] = source_hash
                record[checksum_key] = export_hash
    if not check:
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        for key in ('repository_commit', 'source_commit', 'public_commit'):
            if key in data:
                data[key] = revision
        path.write_text(json.dumps(data, indent=2) + '\n')
    return {'manifest': str(path), 'equations': len(records), 'changed': changed,
            'status': 'FAIL' if check and changed else 'PASS'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifests', type=Path, nargs='+')
    parser.add_argument('--check', action='store_true', help='Reject source, export or hash drift without writing')
    args = parser.parse_args()
    results = [update(p.resolve(), args.check) for p in args.manifests]
    print(json.dumps(results, indent=2))
    return int(any(r['status'] == 'FAIL' for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
