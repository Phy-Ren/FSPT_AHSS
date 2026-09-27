#!/usr/bin/env python3
"""Archive only the small read-only inputs needed to reproduce comparisons.

This does not archive or accept a production campaign. Existing destinations
are rejected; all source bytes and legacy-log hashes are checked first.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


BOSS_FILES = (
    'output/space_group_230/draft_table.json',
    'output/space_group_230/backend/FOUNDATIONS.md',
    'output/space_group_230/backend/hap_all230_e2.json',
    'output/space_group_230/backend/h1_all230.json',
)
FINITE_REFERENCE = 'data/extension-paper-results-20260926-transfer.json'
LEGACY_GROUPS = (68, 81, 82, 101)


def collect_inputs(boss_root, reference_root, legacy_root, pdf, text, finite_controls):
    items = []
    for relative in BOSS_FILES:
        items.append((boss_root / relative, 'boss/'+relative, None, None))
    items.append((reference_root / FINITE_REFERENCE, 'fermionAHSS/'+FINITE_REFERENCE, None, None))
    items += [(pdf, 'space_group_230_layers.pdf', None, None),
              (text, 'space_group_230_layers.txt', None, None),
              (finite_controls, 'finite_c2_controls.json', None, None)]
    legacy_manifest_path = legacy_root / 'manifest.json'
    legacy = json.loads(legacy_manifest_path.read_text())
    for number in LEGACY_GROUPS:
        name = 'sg%03d.log' % number
        source = legacy[name]
        items.append((legacy_root / name, 'legacy_sg%03d.txt' % number,
                      source['sha256'], source['original']))
    material = {}
    for source, destination, expected, original in items:
        raw = source.read_bytes()
        checksum = hashlib.sha256(raw).hexdigest()
        if expected is not None and checksum != expected:
            raise ValueError('legacy source hash mismatch: ' + str(source))
        material[destination] = (raw, dict(source_path=str(source.resolve()),
            original_source_path=original, sha256=checksum, bytes=len(raw)))
    return material, hashlib.sha256(legacy_manifest_path.read_bytes()).hexdigest()


def write_archive(output, material, metadata):
    if output.exists():
        raise ValueError('destination exists; choose a fresh input archive directory')
    output.mkdir(parents=True)
    for relative, (raw, _) in material.items():
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        if hashlib.sha256(target.read_bytes()).hexdigest() != hashlib.sha256(raw).hexdigest():
            raise OSError('copied input hash mismatch: ' + relative)
    manifest = dict(schema='fspt-small-comparison-input-archive-v1',
        scope='Reference inputs and independent finite controls only; no production solver code or acceptance claim.',
        boss_archive_scope='Only the listed recoverable files from the truncated supplied archive.',
        legacy_log_storage='Original .log bytes retained unchanged under .txt filenames; original paths and hashes recorded.',
        inputs={relative: info for relative, (_, info) in material.items()}, **metadata)
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--boss-root', required=True, type=Path)
    parser.add_argument('--reference-root', required=True, type=Path)
    parser.add_argument('--legacy-root', type=Path, default=Path('reference/legacy_stacking_context'))
    parser.add_argument('--pdf', type=Path, default=Path('reference/space_group_230_layers.pdf'))
    parser.add_argument('--text', type=Path, default=Path('reference/space_group_230_layers.txt'))
    parser.add_argument('--finite-controls', type=Path, default=Path('runs/finite_c2_controls.json'))
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError('destination exists; choose a fresh input archive directory')
        material, legacy_hash = collect_inputs(args.boss_root, args.reference_root, args.legacy_root,
            args.pdf, args.text, args.finite_controls)
        commit = None
        if (args.reference_root / '.git').exists():
            commit = subprocess.check_output(['git', '-C', str(args.reference_root), 'rev-parse', 'HEAD'], text=True).strip()
        manifest = write_archive(args.output, material,
            dict(legacy_manifest_sha256=legacy_hash, reference_checkout_commit=commit))
        print(json.dumps(dict(output=str(args.output), files=len(material),
                              bytes=sum(info['bytes'] for info in manifest['inputs'].values())), sort_keys=True))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        parser.exit(1, '%s: %s\n' % (type(exc).__name__, exc))


if __name__ == '__main__':
    main()
