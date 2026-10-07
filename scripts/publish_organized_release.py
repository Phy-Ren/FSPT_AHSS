#!/usr/bin/env python3
"""Apply a committed, additive documentation/result update to a clean public clone.

The public history and earlier scientific archives are preserved. This command
does not fetch, commit, push, or run a numerical calculation.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess


PREFIXES = {
    'publication/computed_examples/': 'results/computed_examples/',
    'publication/formula_reference/': 'formulas/',
    'publication/site/': '',
    'docs/formulas/': 'docs/formulas/',
}
EXACT = {
    'README.md': 'README.md',
    'PUBLIC_RELEASE.md': 'PUBLIC_RELEASE.md',
    'docs/ARCHIVES.md': 'docs/ARCHIVES.md',
    'docs/FORMULA_GUIDE.md': 'docs/FORMULA_GUIDE.md',
    'publication/publish_organized_release.py': 'scripts/publish_organized_release.py',
}
EXTENSIONS = {'.md', '.json', '.csv', '.tsv', '.py', '.tex', '.g', '.txt'}
IMMUTABLE_PREFIXES = ('results/computed_examples/raw/',
                      'results/computed_examples/inputs/',
                      'results/computed_examples/records/')
RETAINED_MANIFESTS = {'COMPLETE_RELEASE_MANIFEST.json', 'RESOLUTION_UPDATE.json',
                      'PUBLICATION_MANIFEST.json', 'formulas/SOURCE_MANIFEST.json',
                      'ORGANIZATION_MANIFEST.json'}


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compressed_coefficients(name):
    return (name.startswith('docs/formulas/coefficients/')
            and name.endswith('.json.gz'))


def destination(name):
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or '.git' in path.parts:
        raise ValueError('Unsafe source path')
    target = EXACT.get(name)
    if target is None:
        for prefix, replacement in PREFIXES.items():
            if name.startswith(prefix):
                target = replacement + name[len(prefix):]
                break
    if target is None:
        return None
    out = PurePosixPath(target)
    if (out.is_absolute() or '..' in out.parts or '.git' in out.parts
            or (out.suffix not in EXTENSIONS
                and not compressed_coefficients(target))):
        raise ValueError('Unreviewed publication path: ' + name)
    if out.parts[0] in {'internal_notes', 'vendor', 'reference', 'runs'}:
        raise ValueError('Private publication destination: ' + target)
    if target.startswith('results/') and not target.startswith('results/computed_examples/'):
        raise ValueError('Earlier result archives are outside this update: ' + target)
    if target.startswith('formulas/publication_source/'):
        raise ValueError('Frozen formula source is outside this documentation update')
    if target in RETAINED_MANIFESTS:
        raise ValueError('An existing archive or generated manifest cannot be overlaid: ' + target)
    return target


def read_payload(source, ref):
    commit = git(source, 'rev-parse', ref + '^{commit}').decode().strip()
    names = git(source, 'ls-tree', '-r', '--name-only', '-z', commit).decode().split('\0')
    payload = {}
    for name in filter(None, names):
        target = destination(name)
        if target is None:
            continue
        if target in payload:
            raise ValueError('Duplicate publication destination: ' + target)
        mode = git(source, 'ls-tree', commit, '--', name).decode().split()[0]
        if mode not in {'100644', '100755'}:
            raise ValueError('Only ordinary tracked files may be published: ' + name)
        data = git(source, 'show', commit + ':' + name)
        payload[target] = {'data': data, 'mode': int(mode[-3:], 8), 'source': name}
    if not payload or 'docs/FORMULA_GUIDE.md' not in payload:
        raise ValueError('The committed canonical formula guide is required')
    if 'results/computed_examples/index.json' not in payload:
        raise ValueError('The committed consolidated example index is required')
    return commit, payload


def validate_payload(payload):
    secret = re.compile(
        rb'-----BEGIN (?:RSA |DSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----'
        rb'|\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b'
        rb'|https?://[^\s/:@]{2,}:[^\s/@]{5,}@'
    )
    for name, item in payload.items():
        data = item['data']
        if secret.search(data):
            raise ValueError('Credential-pattern review required; value redacted: ' + name)
        if name.endswith('.json') or compressed_coefficients(name):
            decoded = gzip.decompress(data) if compressed_coefficients(name) else data
            json.loads(decoded)
            if decoded is not data and secret.search(decoded):
                raise ValueError('Credential-pattern review required; value redacted: ' + name)
        # GitHub rejects ordinary files of 100 MiB or larger. Large runtime
        # packets must not silently replace compact published scientific data.
        if len(data) >= 100 * 1024**2:
            raise ValueError('Publication file exceeds 100 MiB: ' + name)


def apply(source, ref, output, expected_head):
    source, output = Path(source).resolve(), Path(output).resolve()
    if source == output or source in output.parents or output in source.parents:
        raise ValueError('Source and public checkouts must be separate')
    if git(output, 'status', '--porcelain', '--untracked-files=all').strip():
        raise ValueError('Public checkout must be clean before synchronization')
    head = git(output, 'rev-parse', 'HEAD').decode().strip()
    if head != expected_head:
        raise ValueError('Public HEAD changed; review the new base first')
    commit, payload = read_payload(source, ref)
    validate_payload(payload)
    manifest_path = output / 'ORGANIZATION_MANIFEST.json'
    if manifest_path.is_symlink():
        raise ValueError('The generated manifest cannot be a symlink')
    for name, item in payload.items():
        target = output / name
        if output not in target.resolve().parents or target.is_symlink():
            raise ValueError('Unsafe output path: ' + name)
        if any(parent.is_symlink() for parent in target.parents if parent != output and output in parent.parents):
            raise ValueError('Symlink parent in output path: ' + name)
        if target.exists() and name.startswith(IMMUTABLE_PREFIXES):
            if target.read_bytes() != item['data']:
                raise ValueError('An archived scientific payload is immutable: ' + name)
    manifest = {
        'schema': 'fspt-organized-publication-v1',
        'source_commit': commit,
        'public_base_commit': head,
        'scope': 'Additive example catalogue and canonical formula documentation; prior archives preserved.',
        'files': {name: {'sha256': digest(item['data']), 'bytes': len(item['data'])}
                  for name, item in sorted(payload.items())},
    }
    for name, item in sorted(payload.items()):
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(item['data'])
        target.chmod(item['mode'])
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    return {'source_commit': commit, 'public_base_commit': head,
            'files': len(payload), 'bytes': sum(len(v['data']) for v in payload.values())}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--ref', default='HEAD')
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--expected-public-head', required=True)
    args = ap.parse_args()
    print(json.dumps(apply(args.source, args.ref, args.output, args.expected_public_head)))


if __name__ == '__main__':
    main()
