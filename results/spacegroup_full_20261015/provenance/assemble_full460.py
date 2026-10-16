#!/usr/bin/env python3
"""Validate full parent campaigns, then accept an explicit disjoint 460-case union.

Manifest: a nonempty list of {ci, e8, cases?, reason?, label?}, or an object
with schema='u1-spacegroup-assembly-v1' and that list under 'campaigns'.
Relative campaign paths are relative to the manifest. Omitting cases selects
all cases in that pair of parents. No parent ledger or selection is rewritten.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

DEFAULT_REPOSITORY = Path('/home/xingyu/FSPT_AHSS_insulator')


class CoverageError(ValueError):
    def __init__(self, selected, expected):
        self.selected_count = len(selected)
        self.missing = sorted(expected - selected)
        self.extra = sorted(selected - expected)
        super().__init__('Incomplete or unexpected exact coverage: selected=%s required=460 missing=%s extra=%s'
                         % (len(selected), self.missing, self.extra))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def manifest_entries(path):
    raw = path.read_bytes()
    value = json.loads(raw)
    if isinstance(value, dict):
        if set(value) != {'schema', 'campaigns'} or value['schema'] != 'u1-spacegroup-assembly-v1':
            raise ValueError('Unknown assembly manifest schema or fields')
        value = value['campaigns']
    if not isinstance(value, list) or not value:
        raise ValueError('Assembly manifest must contain a nonempty campaign list')
    entries = []
    for item in value:
        if not isinstance(item, dict) or not {'ci', 'e8'} <= set(item) or set(item) - {'ci', 'e8', 'cases', 'reason', 'label'}:
            raise ValueError('Each manifest entry requires ci/e8 paths and only optional cases/reason/label')
        entry = dict(item)
        for kind in ('ci', 'e8'):
            name = entry[kind]
            if not isinstance(name, str) or not name.strip() or '\x00' in name:
                raise ValueError('Campaign root must be a nonempty filesystem path')
            root = Path(name)
            if not root.is_absolute():
                root = path.parent / root
            entry[kind] = root.resolve()
            if not entry[kind].is_dir():
                raise ValueError('Campaign root does not exist: ' + str(entry[kind]))
        for field in ('reason', 'label'):
            if field in entry and not isinstance(entry[field], str):
                raise ValueError('Manifest label/reason must be text')
        if 'cases' in entry:
            cases = entry['cases']
            if (not isinstance(cases, list) or not cases
                    or any(not isinstance(c, str) or not c or Path(c).name != c or c in ('.', '..') for c in cases)
                    or len(set(cases)) != len(cases)):
                raise ValueError('Explicit cases must be a nonempty distinct list of case identifiers')
        entries.append(entry)
    return raw, entries


def preflight(repository, manifest, allow_recovered=False):
    sys.path.insert(0, str(repository))
    from scripts.collect_expansion import load_campaign
    from scripts.recover_paired_campaign import scientific_checks

    source_names = ['scripts/collect_expansion.py', 'scripts/recover_paired_campaign.py',
                    'insulator/e8_h1.py', 'insulator/e8_pointgroup.py', 'insulator/e8_spacegroup.py']
    code_hashes = {name: sha((repository / name).read_bytes()) for name in source_names}
    manifest_raw, entries = manifest_entries(manifest)
    catalog = repository / 'insulator_catalog/generated'
    expected = {'spacegroup_%03d_%s' % (n, spin) for n in range(1, 231) for spin in ('spinless', 'spin_half')}
    paths = {p.stem: p for p in catalog.glob('spacegroup_*_spin*.json')}
    if set(paths) != expected:
        raise ValueError('The exact catalogue must contain groups1..230 in both spins, exactly460 inputs')
    catalog_hashes = {case: sha(path.read_bytes()) for case, path in sorted(paths.items())}
    seen, root_keys, plans, campaigns, scientific = set(), set(), [], [], []
    for item in entries:
        ci, e8 = item['ci'], item['e8']
        for kind in ('ci', 'e8'):
            key = (kind, item[kind])
            if key in root_keys:
                raise ValueError('Repeated campaign root; combine its explicit cases in one entry: ' + str(key))
            root_keys.add(key)
        c, _, cp = load_campaign(ci, 'ci', allow_recovered=allow_recovered)
        e, _, ep = load_campaign(e8, 'e8', allow_recovered=allow_recovered)
        if set(c) != set(e):
            raise ValueError('Full parent CI/E8 selections disagree: ' + str(ci))
        # Check every parent pair, including unselected entries. A subset is
        # never used to hide an unrelated or invalid E8-consumed CI record.
        for case in c:
            if (e[case]['directory'] / 'ci_result.json').read_bytes() != (c[case]['directory'] / 'result.json').read_bytes():
                raise ValueError('Parent E8 consumed a different exact CI artifact: ' + case)
        chosen = item.get('cases', sorted(c))
        if not set(chosen) <= set(c):
            raise ValueError('Requested cases missing from the fully validated parents: ' + str(sorted(set(chosen) - set(c))))
        overlap = seen & set(chosen)
        if overlap:
            raise ValueError('Duplicated selected catalogue IDs: ' + str(sorted(overlap)))
        for case in chosen:
            if case not in paths:
                raise ValueError('Selected case is outside the exact230×2 catalogue: ' + case)
            raw = paths[case].read_bytes()
            data = json.loads(raw)
            record = c[case]['record']
            if data.get('id') != case or data != record['input']:
                raise ValueError('Selected input differs from the exact affine catalogue: ' + case)
            if (c[case]['directory'] / 'input.json').read_bytes() != raw:
                raise ValueError('Selected input bytes differ from the pinned catalogue artifact: ' + case)
            checked = scientific_checks(record['classification'], data)
            scientific.append(dict(id=case, runStatus=record['run']['status'], **checked))
        seen.update(chosen)
        for kind in ('ci', 'e8'):
            plans.append({'kind': kind, 'root': str(item[kind]), 'cases': list(chosen)})
        campaigns.append({'label': item.get('label'), 'selectionReason': item.get('reason', 'Explicit manifest selection'),
                          'ciRoot': str(ci), 'e8Root': str(e8), 'selectedCases': list(chosen),
                          'originalCIProvenance': cp, 'originalE8Provenance': ep,
                          'selectedCIResultHashes': {case: cp['resultHashes'][case] for case in chosen},
                          'selectedE8ResultHashes': {case: ep['resultHashes'][case] for case in chosen}})
    if seen != expected:
        raise CoverageError(seen, expected)
    if any(sha((repository / name).read_bytes()) != value for name, value in code_hashes.items()):
        raise ValueError('Validation source changed during assembly preflight')
    report = {'schema': 'u1-full-spacegroup-assembly-v1', 'preflightPassed': True,
              'manifestSHA256': sha(manifest_raw), 'manifestPath': str(manifest),
              'expectedCount': 460, 'selectedCount': len(seen), 'selectedCases': sorted(seen),
              'exactCatalogInputSHA256': catalog_hashes, 'campaigns': campaigns,
              'validationSourceSHA256': code_hashes, 'assemblerSHA256': sha(Path(__file__).read_bytes()),
              'nativeChecks': scientific,
              'nativeCheckScope': 'Independent integer presentation/filling checks, exact root-vector shape/rational typing and saved native-chain/completion certificates. The collector does not re-evaluate nonlinear bar cochains or reconstruct absent differential matrices.',
              'allowRecovered': allow_recovered,
              'selectionPolicy': 'Explicit disjoint manifest; complete original parents validated, no source ledger or selection modified.'}
    return manifest_raw, plans, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--audit-dir', '--views', dest='audit_dir', required=True, type=Path,
                        help='New assembly evidence directory; no campaign subsets are copied')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--repository', type=Path, default=DEFAULT_REPOSITORY)
    parser.add_argument('--allow-recovered', action='store_true')
    args = parser.parse_args()
    repository, manifest = args.repository.resolve(), args.manifest.resolve()
    audit, output = args.audit_dir.resolve(), args.output.resolve()
    if audit.exists() or output.exists() or audit == output:
        raise ValueError('Assembly evidence and accepted output must be new distinct paths')
    manifest_raw, plans, report = preflight(repository, manifest, args.allow_recovered)
    for item in report['campaigns']:
        for kind in ('ciRoot', 'e8Root'):
            root = Path(item[kind])
            if audit == root or root in audit.parents or output == root or root in output.parents:
                raise ValueError('Assembly output must not modify an original campaign tree')
    # Every original parent and the exact disjoint460-case union have passed.
    audit.mkdir(parents=True, exist_ok=False)
    (audit / 'input_manifest.json').write_bytes(manifest_raw)
    plan = audit / 'selection_plan.json'
    write(plan, plans)
    command = [sys.executable, str(repository / 'scripts/collect_expansion.py'),
               '--selection-plan', str(plan), '--output', str(output)]
    if args.allow_recovered:
        command += ['--allow-recovered']
    report.update(selectionPlanSHA256=sha(plan.read_bytes()), collectorCommand=command,
                  acceptedOutput=str(output), accepted=False)
    write(audit / 'assembly.json', report)
    with (audit / 'collector.stdout.log').open('wb') as out, (audit / 'collector.stderr.log').open('wb') as err:
        subprocess.run(command, check=True, stdout=out, stderr=err)
    collection = read(output / 'collection.json')
    if not collection.get('accepted') or len(collection['collections']) != 1:
        raise ValueError('Collector did not produce one accepted space-group collection')
    item = collection['collections'][0]
    if (item['family'], item['path'], item['count']) != ('spacegroup', '3p1d/space_groups', 460):
        raise ValueError('Collector output is not the required460-case space-group collection')
    folder = output / item['path']
    for name, expected in item['filesSHA256'].items():
        if sha((folder / name).read_bytes()) != expected:
            raise ValueError('Accepted collector file hash changed: ' + name)
    ci, e8 = read(folder / 'ci_results.json'), read(folder / 'results.json')
    for records in (ci, e8):
        ids = [record['input']['id'] for record in records]
        if len(ids) != 460 or set(ids) != set(report['selectedCases']):
            raise ValueError('Accepted records do not reproduce the exact460-case union')
    original_cases = {case: campaign for campaign in report['campaigns'] for case in campaign['selectedCases']}
    for a, b in zip(ci, e8):
        if a['input'] != b['input'] or a['classification'] != b['classification']['ciSector']:
            raise ValueError('Accepted CI/E8 scientific records no longer match')
        case = a['input']['id']
        original = original_cases[case]
        for kind, record in (('ci', a), ('e8', b)):
            raw = (Path(original[kind + 'Root']) / case / 'result.json').read_bytes()
            expected = original['selected' + kind.upper() + 'ResultHashes'][case]
            if sha(raw) != expected or json.loads(raw) != record:
                raise ValueError('Accepted artifact changed since preflight: ' + kind + ' ' + case)
        catalog_path = repository / 'insulator_catalog/generated' / (case + '.json')
        if sha(catalog_path.read_bytes()) != report['exactCatalogInputSHA256'][case]:
            raise ValueError('Catalogue changed since preflight: ' + case)
        if a['input'] != read(catalog_path):
            raise ValueError('Accepted result differs from catalogue at final check')
    for name, expected in report['validationSourceSHA256'].items():
        if sha((repository / name).read_bytes()) != expected:
            raise ValueError('Validation source changed before collector completion')
    report.update(accepted=True, collectionSHA256=sha((output / 'collection.json').read_bytes()),
                  acceptedFilesSHA256=item['filesSHA256'])
    write(audit / 'assembly.json', report)
    files = {p.name: sha(p.read_bytes()) for p in sorted(audit.iterdir()) if p.is_file()}
    write(audit / 'artifact_manifest.json', {'files': files})
    print(json.dumps({'accepted': True, 'count': 460, 'auditDirectory': str(audit),
                      'output': str(output), 'collectionSHA256': report['collectionSHA256']}, sort_keys=True))


if __name__ == '__main__':
    main()
