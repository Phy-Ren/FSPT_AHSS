#!/usr/bin/env python3
"""Archive one audited crystalline-spinless campaign with exact uncertainty scope.

All inputs are validated before the destination is created. Saved result,
checkpoint, source and task bytes are retained, including original absolute
provenance paths. No reference answer is read.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

from audit_background_run import check_background_result
from background_performance import collect_background_performance
from deadline_evidence import read_index

FORMULA_CONVENTION = 'normalized-pip-aw-edge-transport-v2'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def archive(run, source, tasks_root, output):
    require(__debug__, 'Run without Python -O: certificate checks use assertions')
    require(not output.exists() and not output.is_symlink(), 'destination already exists: ' + str(output))
    run, source, tasks_root, output = (p.resolve() for p in (run, source, tasks_root, output))
    for original in (run, source, tasks_root):
        require(original != output and original not in output.parents,
                'destination must be outside the input directories')
    expected = {'sg%d.json' % n for n in range(1, 231)}
    for directory in (run, run/'classification'):
        actual = {p.name for p in directory.glob('sg*.json') if '.raw.' not in p.name}
        require(actual == expected, 'require all 230 result files in %s; missing=%r extra=%r' %
                (directory, sorted(expected-actual), sorted(actual-expected)))

    # Keep the exact validated bytes in memory. Later writes do not reread
    # source files or rewrite JSON; performance provenance is cross-checked
    # against the same byte snapshot below.
    material, entries, audits = {}, {}, {}

    def add(path, relative):
        require(relative not in material, 'duplicate archive destination: ' + relative)
        raw = path.read_bytes()
        material[relative] = raw
        entries[relative] = dict(original_path=str(path), archive_path=relative,
                                 sha256=digest(raw), bytes=len(raw))
        return raw

    campaign = json.loads(add(run/'campaign.json', 'campaign.json'))
    require(sorted(campaign['groups']) == list(range(1, 231)), 'campaign must contain exactly SG1 through SG230')
    require(campaign.get('crystalline_spin') == 'spinless', 'wrong physical convention')
    require(campaign.get('mode') == 'full' and campaign.get('prepared_only') is False,
            'require a submitted full campaign')
    source_hashes = {}
    for path in sorted((source/'gap').glob('*.g')):
        relative = str(path.relative_to(source))
        source_hashes[relative] = digest(add(path, 'source/'+relative))
    require('gap/run_one.g' in source_hashes, 'frozen source has no gap/run_one.g')
    require(source_hashes == campaign['source_sha256'], 'actual frozen source files differ from campaign source hashes')
    source_id = digest(json.dumps(source_hashes, sort_keys=True).encode())
    require(source_id == campaign['source_id'], 'actual frozen source ID differs from campaign')

    for number in range(1, 231):
        name = 'sg%d.json' % number
        result = json.loads(add(run/name, name))
        require(result.get('space_group') == number, 'result filename/group mismatch: ' + name)
        require(result.get('source_id') == source_id and result.get('source_sha256') == source_hashes,
                'result has mixed source: ' + name)
        audits[number] = check_background_result(result, strict_background=True)
        checkpoint = json.loads(add(run/'classification'/name, 'classification/'+name))
        require(checkpoint.get('space_group') == number and checkpoint.get('source_id') == source_id,
                'classification checkpoint group/source mismatch: ' + name)
        require(checkpoint.get('formula_convention') == FORMULA_CONVENTION,
                'classification checkpoint formula convention differs: ' + name)
        if 'source_sha256' in checkpoint:
            require(checkpoint['source_sha256'] == source_hashes,
                    'classification checkpoint source hashes differ: ' + name)
        # Checkpoint JSON omits this hash map; attach the independently
        # verified campaign map only to the in-memory auditor input.
        require(checkpoint.get('classification_status') == 'computed', 'incomplete classification checkpoint: '+name)
        require(checkpoint.get('convention') == 'physical-spinless-det-sign-Pin-minus', 'wrong checkpoint convention')
        for key in ('pip', 'majorana', 'complex_fermion', 'bosonic', 'ranks',
                    'resolution_dimensions', 'cpu_ms'):
            require(checkpoint.get(key) == result.get(key),
                    'checkpoint/result %s mismatch: %s' % (key, name))

    add(run/'observation.json', 'observation.json')
    extensions = read_index(run, {})
    require(not extensions, 'background archive does not accept deadline extensions without their strict audit')
    for task in campaign['tasks']:
        ident = task['id']
        require(isinstance(ident, str) and ident not in ('', '.', '..') and Path(ident).name == ident,
                'invalid task ID')
        for original_name, archived_name in (('status.json', 'status.json'),
                                              ('metrics.txt', 'metrics.txt'),
                                              ('stdout.log', 'stdout.txt')):
            add(tasks_root/ident/original_name, 'tasks/'+ident+'/'+archived_name)

    performance = collect_background_performance(run, tasks_root, audits)
    require(performance['complete'] and performance['groups'] == list(range(1, 231))
            and performance['source_id'] == source_id, 'performance report does not certify this complete campaign')
    by_original = {entry['original_path']: entry for entry in entries.values()}
    for path, checksum in performance['evidence_sha256'].items():
        require(path in by_original and by_original[path]['sha256'] == checksum,
                'performance input changed during audit: ' + path)
    for entry in entries.values():
        require(digest(Path(entry['original_path']).read_bytes()) == entry['sha256'],
                'input changed during audit: ' + entry['original_path'])
    require({str(p.relative_to(source)): digest(p.read_bytes()) for p in (source/'gap').glob('*.g')} == source_hashes,
            'frozen source file set changed during audit')

    performance_raw = (json.dumps(performance, indent=2, sort_keys=True)+'\n').encode()
    material['performance.json'] = performance_raw
    entries['performance.json'] = dict(original_path=None, archive_path='performance.json',
        generated_by='background_performance.collect_background_performance(run, tasks_root, audits)',
        sha256=digest(performance_raw), bytes=len(performance_raw))
    script_dir = Path(__file__).resolve().parent
    manifest = dict(schema='fspt-crystalline-spinless-campaign-archive-v1',
        archived_at_utc=datetime.now(timezone.utc).isoformat(),
        original_run=str(run), original_source=str(source), original_tasks_root=str(tasks_root),
        source_id=source_id, source_sha256=source_hashes,
        groups=list(range(1, 231)), formula_convention=FORMULA_CONVENTION,
        physical_convention='physical-spinless-det-sign-Pin-minus',
        per_group_audits=audits,
        unique_full_groups=sum(bool(x['full_group']) for x in audits.values()),
        groups_with_complete_marked_evidence=sum(bool(x['marked_witnesses']) for x in audits.values()),
        archive_file_count=len(material)+1, payload_bytes=sum(map(len, material.values())),
        files=entries,
        audit_tool_sha256={name: digest((script_dir/name).read_bytes()) for name in
                          ('archive_background_campaign.py', 'audit_background_run.py', 'background_performance.py', 'collect_performance.py', 'deadline_evidence.py')},
        audit_scope=dict(reference_answers_read=False, complete_stored_witness_audit=False,
            stored_evidence_audit="Physical background, affine cocycle gauge, exact lower CA relations, H0 quotient, filtered lattices, free period and upper Ext family; actual upper witnesses only when explicitly supplied",
            exact_smith_presentation_audit=True, actual_frozen_source_hashes_verified=True,
            performance_collection='all task and result provenance, successful processes and exact observer counts; mathematical uniqueness recorded separately',
            comparison_support_cochains_reexecuted=False,
            input_bytes_modified=False, original_absolute_provenance_paths_preserved=True,
            deadline_extensions='Nonempty extension indexes rejected; all tasks must satisfy their original worker deadlines',
            stdout_storage='Original stdout.log bytes retained unchanged under stdout.txt names'))
    archive_raw = (json.dumps(manifest, indent=2, sort_keys=True)+'\n').encode()

    # No destination or parent directory is created until all audits pass.
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir(exist_ok=False)
    try:
        for relative, raw in material.items():
            path = output/relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            require(digest(path.read_bytes()) == entries[relative]['sha256'],
                    'archived byte verification failed: ' + relative)
        (output/'archive.json').write_bytes(archive_raw)
    except BaseException:
        shutil.rmtree(output)
        raise
    return dict(output=str(output), source_id=source_id, groups=230,
                files=len(material)+1, bytes=sum(map(len, material.values()))+len(archive_raw),
                unique_full_groups=manifest["unique_full_groups"],
                archive_sha256=digest(archive_raw), complete=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--tasks-root', type=Path, default=Path('runs/tasks'))
    parser.add_argument('--output', type=Path, default=Path('results/space_groups_spinless'))
    args = parser.parse_args(argv)
    try:
        result = archive(args.run, args.source, args.tasks_root, args.output)
    except (OSError, ValueError, AssertionError, KeyError, TypeError, IndexError) as exc:
        print('Campaign archive refused: '+str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
