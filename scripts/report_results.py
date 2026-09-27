#!/usr/bin/env python3
"""Report one accepted independent run as CSV/Markdown, without external answers.

The input directory is selected explicitly. This script does not choose between
runs, recompute groups, or open any source/answer paths named inside a result.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import sys

from audit_run import check_result, check_complete_witnesses, determinant

FIELDS = [
    'space_group', 'classification_status', 'result_status',
    'pip_orders', 'pip_group', 'majorana_orders', 'majorana_group',
    'complex_fermion_orders', 'complex_fermion_group', 'bosonic_orders', 'bosonic_group',
    'stacking_status', 'stacking_orders', 'stacking_group',
    'torsion_upper_witness', 'upper_completion', 'free_pip_rank', 'free_pip_scope',
    'free_pip_lattice_basis_available', 'free_pip_lattice_index', 'free_pip_lattice_basis',
    'free_pip_h1_coordinates', 'free_pip_phase_witness', 'free_pip_certificate',
    'free_pip_h1_orders', 'free_pip_certificate_level', 'free_pip_checked_comparison_support',
    'stacking_scope', 'lower_scope',
    'persisted_witness_type', 'full_bar_cochains_persisted', 'independent_audit',
    'classification_cpu_ms', 'total_cpu_ms', 'post_classification_cpu_ms',
    'wall_seconds', 'started_utc', 'finished_utc', 'stage_timings', 'resolution_timings',
    'convention', 'formula_convention', 'classification_scope', 'mode', 'libraries', 'source_id', 'source_snapshot',
    'accepted_result_file', 'accepted_result_sha256', 'assembly_selected_from', 'assembly_candidate_history',
]
FREE_SCOPE = 'abstract free rank; surviving geometric lattice basis/index not supplied'
FREE_NOTE = (
    'Rows marked † describe only an abstract Z^r summand. Those outputs do '
    'not supply a basis or index of the surviving lattice inside the original '
    'H^1(G,Z_s) free part, nor explicit bar-cochain lifts for every free generator. '
    'This is sufficient for the abstract abelian group type once the finite '
    'extension is determined; it is not a geometric generator normalization.'
)


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def free_lattice(data):
    """Validate optional marked free generators without rerunning cochains."""
    rank = data['pip']['free_rank']
    result = dict(free_pip_lattice_basis_available=False if rank else '',
                  free_pip_scope=FREE_SCOPE if rank else 'no free p+ip factor')
    free = data['pip'].get('free_lattice')
    if free is None or free.get('status') != 'computed':
        return result
    if type(free['rank']) is not int or free['rank'] != rank:
        raise ValueError('free-lattice rank does not match the graded layer')
    basis = free['latticeBasis']
    integer = lambda x: type(x) is int
    if len(basis) != rank or any(len(row) != rank or not all(map(integer, row)) for row in basis):
        raise ValueError('free-lattice basis is not a square integer matrix')
    index = free['latticeIndex']
    if not integer(index) or index < 1 or abs(determinant(basis)) != index:
        raise ValueError('free-lattice index does not equal its determinant')
    indices = free['freeIndices']
    if len(indices) != rank or len(set(indices)) != rank or any(not integer(i) or i < 1 for i in indices):
        raise ValueError('invalid original free H1 coordinate indices')
    h1_orders = free.get('h1BasisOrders')
    if h1_orders is not None:
        group_name(h1_orders)
        if indices != [i+1 for i, order in enumerate(h1_orders) if order == 0]:
            raise ValueError('free H1 indices disagree with original H1 orders')
    parity = free['survivingParityBasis']
    pivots = []
    for row in parity:
        if len(row) != rank or any(type(x) is not int or x not in (0, 1) for x in row) or 1 not in row:
            raise ValueError('invalid surviving parity basis')
        pivots.append(row.index(1))
    if pivots != sorted(set(pivots)) or any(parity[i][p] != (i == j) for j, p in enumerate(pivots) for i in range(len(parity))):
        raise ValueError('surviving parity basis is not in reduced row-echelon form')
    if index != 2 ** (rank - len(parity)):
        raise ValueError('free-lattice index disagrees with the parity dimension')
    for row in basis:
        residual = [x % 2 for x in row]
        for pivot, vector in zip(pivots, parity):
            if residual[pivot]:
                residual = [(a+b) % 2 for a, b in zip(residual, vector)]
        if any(residual):
            raise ValueError('free-lattice basis is outside the surviving parity span')
    generators = free['generators']
    if len(generators) != rank or type(free['fullFreePhaseWitness']) is not bool:
        raise ValueError('invalid free generator/witness count')
    dimensions = data['resolution_dimensions']
    for i, generator in enumerate(generators):
        coordinates = generator['h1Coordinates']
        if not all(map(integer, coordinates)) or len(coordinates) < max(indices, default=0):
            raise ValueError('invalid free generator H1 coordinates')
        if h1_orders is not None and len(coordinates) != len(h1_orders):
            raise ValueError('free generator H1 coordinate count differs from original basis')
        if [coordinates[j-1] for j in indices] != basis[i]:
            raise ValueError('free generator H1 coordinates disagree with the lattice basis')
        if generator['name'] != 'Pfree%d' % (i+1):
            raise ValueError('free generator names/order disagree with the marked basis')
        for key, degree in [('integer1', 1), ('majorana2', 2), ('fermion3', 3)]:
            values = generator[key]
            if len(values) != dimensions[degree] or not all(map(integer, values)) or (degree > 1 and any(x not in (0, 1) for x in values)):
                raise ValueError('invalid native free generator field ' + key)
        phase = generator['phase4']
        if len(phase) != dimensions[4] or any(len(x) != 2 or not all(map(integer, x)) or not 0 <= x[0] < x[1] for x in phase):
            raise ValueError('invalid rational native free generator phase')
    result.update(free_pip_lattice_basis_available=True if rank else '',
                  free_pip_lattice_index=index, free_pip_lattice_basis=compact(basis),
                  free_pip_h1_coordinates=compact([g['h1Coordinates'] for g in generators]),
                  free_pip_phase_witness=free['fullFreePhaseWitness'],
                  free_pip_certificate=free['certificate'],
                  free_pip_h1_orders=compact(h1_orders) if h1_orders is not None else '',
                  free_pip_certificate_level=free.get('certificateLevel', ''),
                  free_pip_checked_comparison_support=free.get('checkedComparisonSupport', ''),
                  free_pip_scope=('primitive surviving H1 lattice and actual complete defining towers'
                                  if free['fullFreePhaseWitness'] else 'primitive surviving H1 lattice; full phase witness not supplied')
                                  if rank else 'no free p+ip factor')
    return result


def group_name(orders):
    """Format exact cyclic factors; zero means Z and [] means the trivial group."""
    if not isinstance(orders, list) or any(type(x) is not int or (x != 0 and x <= 1) for x in orders):
        raise ValueError('invalid cyclic-factor list: %r' % (orders,))
    counts = Counter(orders)
    parts = []
    for order in sorted(counts):
        name = 'Z' if order == 0 else 'Z%d' % order
        count = counts[order]
        parts.append(name if count == 1 else ('%s^%d' % (name, count) if order == 0 else '(%s)^%d' % (name, count)))
    return ' + '.join(parts) if parts else '0'


def utc(value):
    return '' if value is None else datetime.fromtimestamp(value, timezone.utc).isoformat()


def number(value, name):
    if value is None:
        return ''
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise ValueError('invalid nonnegative timing %s=%r' % (name, value))
    return value


def upper_witness(data):
    stack = data.get('stacking', {})
    if stack.get('status') != 'computed':
        return 'not-computed' if not stack else 'unresolved'
    if not any(data['pip']['orders']):
        return 'not-needed'
    if stack.get('fullUpperPhaseWitness') is True:
        return 'actual-phase-witness'
    if (stack.get('fullUpperPhaseWitness') is False or 'pipExtensionCertificate' in stack
            or stack.get('upperCompletion', '').startswith('abstract-')):
        return 'abstract-certificate'
    return 'not-reported'


def load_results(directory, allow_partial):
    if not __debug__:
        raise ValueError('Run without Python -O: the shared certificate auditor uses assertions')
    assembly_path = directory / 'assembly.json'
    assembly_bytes = assembly_path.read_bytes() if assembly_path.exists() else None
    assembly = json.loads(assembly_bytes) if assembly_bytes is not None else {}
    selected = assembly.get('selected', {})
    histories = assembly.get('candidate_history', {})
    records, hashes, errors = {}, {}, []
    for path in sorted(directory.glob('sg*.json')):
        if '.raw.' in path.name:
            continue
        match = re.fullmatch(r'sg([0-9]+)\.json', path.name)
        if not match:
            errors.append('%s: unexpected result filename' % path.name)
            continue
        try:
            payload = path.read_bytes()
            data = json.loads(payload)
            n = data['space_group']
            if type(n) is not int or not 1 <= n <= 230 or n != int(match.group(1)) or n in records:
                raise ValueError('invalid, duplicate, or filename-mismatched space group')
            kind = check_result(data)
            row = {field: '' for field in FIELDS}
            row.update(space_group=n, classification_status=data.get('classification_status', data['status']),
                       result_status=data['status'], independent_audit=kind)
            layers = [('pip', data['pip']['orders']), ('majorana', data['majorana']),
                      ('complex_fermion', data['complex_fermion']), ('bosonic', data['bosonic'])]
            for layer, orders in layers:
                row[layer + '_orders'] = compact(orders)
                row[layer + '_group'] = group_name(orders)
            stack = data.get('stacking', {})
            row['stacking_status'] = stack.get('status', 'not-computed')
            if row['stacking_status'] == 'computed':
                row['stacking_orders'] = compact(stack['invariants'])
                row['stacking_group'] = group_name(stack['invariants'])
            row.update(torsion_upper_witness=upper_witness(data), upper_completion=stack.get('upperCompletion', ''),
                       free_pip_rank=data['pip']['free_rank'],
                       stacking_scope=stack.get('scope', ''), lower_scope=stack.get('lower', {}).get('scope', ''),
                       persisted_witness_type=stack.get('persistedWitnessType', ''),
                       full_bar_cochains_persisted=stack.get('fullBarCochainsPersisted', ''))
            row.update(free_lattice(data))
            for key, field in [('cpu_ms', 'classification_cpu_ms'), ('total_cpu_ms', 'total_cpu_ms'), ('wall_seconds', 'wall_seconds')]:
                row[field] = number(data.get(key), key)
            if row['total_cpu_ms'] != '' and row['classification_cpu_ms'] != '':
                row['post_classification_cpu_ms'] = number(row['total_cpu_ms'] - row['classification_cpu_ms'], 'post_classification_cpu_ms')
            row.update(started_utc=utc(data.get('started')), finished_utc=utc(data.get('finished')),
                       stage_timings=compact(data.get('stage_timings', [])),
                       resolution_timings=compact(data.get('resolution_timings', {})),
                       convention=data['convention'], classification_scope=data.get('scope', ''),
                       formula_convention=data.get('formula_convention', 'unversioned-development-formulas'),
                       mode=data.get('mode', ''), libraries=compact(data.get('libraries', {})),
                       source_id=data['source_id'], source_snapshot=data.get('source_snapshot', ''),
                       accepted_result_file=str(path.resolve()),
                       accepted_result_sha256=hashlib.sha256(payload).hexdigest(),
                       assembly_selected_from=selected.get(str(n), ''),
                       assembly_candidate_history=compact(histories.get(str(n), [])))
            records[n] = (row, data)
            hashes[path.name] = row['accepted_result_sha256']
        except (AssertionError, KeyError, ValueError, TypeError, IndexError, OverflowError) as exc:
            errors.append('%s: %s: %s' % (path.name, type(exc).__name__, exc))
    missing = sorted(set(range(1, 231)) - records.keys())
    if errors:
        raise ValueError('Input certificates rejected; no report written:\n' + '\n'.join(errors))
    if missing and not allow_partial:
        raise ValueError('Missing accepted results for SG %s; use --allow-partial for a clearly marked development report' % missing)
    return records, hashes, assembly_bytes, missing


def make_manifest(directory, records, hashes, assembly_bytes, missing):
    rows = [record[0] for _, record in sorted(records.items())]
    cohorts = {}
    for n, (row, data) in sorted(records.items()):
        cohort = cohorts.setdefault(row['source_id'], dict(groups=[], source_sha256=data['source_sha256'],
                                                         source_snapshots=[], library_versions=[]))
        cohort['groups'].append(n)
        if row['source_snapshot'] not in cohort['source_snapshots']:
            cohort['source_snapshots'].append(row['source_snapshot'])
        versions = data.get('libraries', {})
        if versions not in cohort['library_versions']:
            cohort['library_versions'].append(versions)
    measured_cpu = [row['total_cpu_ms'] if row['total_cpu_ms'] != '' else row['classification_cpu_ms'] for row in rows]
    return dict(schema='fspt-independent-results-report-v1', generated_utc=datetime.now(timezone.utc).isoformat(),
                input_directory=str(directory), external_answers_consulted=False, groups_present=len(records),
                classification_complete=not missing, missing=missing,
                stacking_status_counts=dict(Counter(row['stacking_status'] for row in rows)),
                stacking_complete=not missing and all(row['stacking_status'] == 'computed' for row in rows),
                torsion_upper_witness_counts=dict(Counter(row['torsion_upper_witness'] for row in rows)),
                free_pip_groups=[row['space_group'] for row in rows if row['free_pip_rank']],
                free_pip_primitive_lattice_groups=[row['space_group'] for row in rows if row['free_pip_rank'] and row['free_pip_lattice_basis_available']],
                free_pip_abstract_only_groups=[row['space_group'] for row in rows if row['free_pip_rank'] and not row['free_pip_lattice_basis_available']],
                free_pip_scope=FREE_NOTE,
                cyclic_factor_encoding='0 denotes Z; an empty factor list denotes the trivial group',
                layer_histograms={layer: dict(Counter(row[layer + '_orders'] for row in rows)) for layer in ['pip', 'majorana', 'complex_fermion', 'bosonic']},
                stacking_histogram=dict(Counter(row['stacking_orders'] for row in rows if row['stacking_status'] == 'computed')),
                timings=dict(recorded_cpu_hours_lower_bound=sum(x for x in measured_cpu if x != '') / 3600000,
                             total_cpu_measurements=sum(row['total_cpu_ms'] != '' for row in rows),
                             classification_cpu_measurements=sum(row['classification_cpu_ms'] != '' for row in rows),
                             wall_measurements=sum(row['wall_seconds'] != '' for row in rows),
                             maximum_group_wall_seconds=max((row['wall_seconds'] for row in rows if row['wall_seconds'] != ''), default=None),
                             interpretation='CPU counters are GAP Runtime() values, not GNU time user+system for the complete task process tree; the sum is not campaign elapsed time. Classification-only fallback is a lower bound.'),
                input_sha256=hashes, input_set_sha256=hashlib.sha256(compact(hashes).encode()).hexdigest(),
                assembly_sha256=hashlib.sha256(assembly_bytes).hexdigest() if assembly_bytes is not None else None,
                source_cohorts=cohorts)


def markdown(records, manifest, output):
    cohort_names = {value: 'S%02d' % (i + 1) for i, value in enumerate(sorted(manifest['source_cohorts']))}
    computed = manifest['stacking_status_counts'].get('computed', 0)
    lines = ['# Independently computed space-group results', '',
             'This report reads only the explicitly selected independent result directory. No external answer table was consulted.', '',
             '**Classification:** %d/230 accepted results. **Full stacking:** %d/230 computed results.' % (len(records), computed)]
    if manifest['missing']:
        lines.extend(['', '**Partial development report. Missing groups:** ' + ', '.join(map(str, manifest['missing'])) + '.'])
    lines.extend(['', 'The four layer columns are the associated graded. Their direct product is not substituted for the final stacking group.', '',
                  '`0` in a displayed group means the trivial group; `Z` is an infinite cyclic factor. In the CSV factor lists, integer `0` denotes `Z`, while `[]` denotes the trivial group.', '',
                  'Upper-witness labels: **actual** = explicit torsion generator and phase relation; **abstract** = certified abstract extension without that phase witness; **none** = no torsion p+ip relation is needed; **unreported/pending** retain the stated limitation.', '',
                  '**† Free-factor scope:** ' + FREE_NOTE, '',
                  'A free-lattice entry `index N; actual` identifies the primitive surviving H1 lattice and complete defining towers. The CSV retains its integer basis and full H1 coordinates; the linked result contains the native fields.', '',
                  'Wall time is the recorded per-group invocation time. CPU is the total GAP Runtime() counter when supplied, otherwise classification CPU marked `*`; missing timing is `—`. This excludes the separate GNU time process-tree measurement. Timings from mixed source cohorts are not a single-campaign benchmark.', '',
                  '| SG | p+ip | Majorana | CF | Bosonic | Full stacking | Upper | Free lattice | Wall s | CPU s | Source |',
                  '|---:|---|---|---|---|---|---|---|---:|---:|---|'])
    labels = {'actual-phase-witness': 'actual', 'abstract-certificate': 'abstract', 'not-needed': 'none',
              'not-reported': 'unreported', 'unresolved': 'pending', 'not-computed': 'pending'}
    for n in range(1, 231):
        if n not in records:
            lines.append('| %d | — | — | — | — | missing | — | — | — | — | — |' % n)
            continue
        row = records[n][0]
        relative = os.path.relpath(row['accepted_result_file'], output).replace(os.sep, '/')
        abstract_free = row['free_pip_rank'] and not row['free_pip_lattice_basis_available']
        layer_text = ['`%s`%s' % (row[layer + '_group'], ' †' if layer == 'pip' and abstract_free else '')
                      for layer in ['pip', 'majorana', 'complex_fermion', 'bosonic']]
        stack = '`%s`%s' % (row['stacking_group'], ' †' if abstract_free else '') if row['stacking_status'] == 'computed' else row['stacking_status']
        free = ('abstract †' if abstract_free else ('index %s; %s' % (row['free_pip_lattice_index'], 'actual' if row['free_pip_phase_witness'] else 'no phase')) if row['free_pip_rank'] else '—')
        wall = '—' if row['wall_seconds'] == '' else '%.2f' % row['wall_seconds']
        cpu = '%.2f' % (row['total_cpu_ms'] / 1000) if row['total_cpu_ms'] != '' else ('%.2f*' % (row['classification_cpu_ms'] / 1000) if row['classification_cpu_ms'] != '' else '—')
        cells = ['[%d](<%s>)' % (n, relative)] + layer_text + [stack, labels[row['torsion_upper_witness']], free, wall, cpu, cohort_names[row['source_id']]]
        lines.append('| ' + ' | '.join(cells) + ' |')
    lines.extend(['', '## Source and timing provenance', '',
                  'Each CSV row records the complete source ID, result SHA-256, selected assembly origin, library versions, stage timestamps and measurement scope. `independent_report.json` preserves every source-file hash by cohort and the hash of the complete input set.', '',
                  '| Cohort | Groups | Source ID |', '|---|---:|---|'])
    for source, label in cohort_names.items():
        lines.append('| %s | %d | `%s` |' % (label, len(manifest['source_cohorts'][source]['groups']), source))
    timing = manifest['timings']
    lines.extend(['', 'Sum of available GAP Runtime() counters: %.3f CPU hours; %d/%d rows report total CPU. This sum is a lower bound where only classification CPU is available, and is not parallel campaign elapsed time.' %
                  (timing['recorded_cpu_hours_lower_bound'], timing['total_cpu_measurements'], len(records)), '',
                  'The report reuses the independent certificate audit: source-digest consistency, absence of SptSet, graded order/rank agreement, and applicable exact Smith identities. It does not rerun bar-cochain proofs or enlarge the mathematical normalization/coherence scope described in `docs/VALIDATION.md`.', ''])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path, help='One explicitly accepted/assembled result directory')
    parser.add_argument('--output', type=Path, help='New report directory; default RUN/report')
    parser.add_argument('--allow-partial', action='store_true', help='Allow missing groups, visibly marked in all outputs')
    parser.add_argument('--require-full-stacking', action='store_true', help='Reject any result without completed stacking')
    parser.add_argument('--require-complete-witnesses', action='store_true', help='Require all 230 full results with actual torsion and primitive free lifts')
    parser.add_argument('--require-formula-convention', help='Require one named formula convention in every result')
    args = parser.parse_args()
    directory = args.run.resolve();output = (args.output or directory / 'report').resolve()
    try:
        if not directory.is_dir():raise ValueError('Input directory does not exist: %s' % directory)
        records, hashes, assembly, missing = load_results(directory, args.allow_partial)
        manifest = make_manifest(directory, records, hashes, assembly, missing)
        if args.require_full_stacking and not manifest['stacking_complete']:
            raise ValueError('Full stacking is incomplete; no report written')
        if args.require_complete_witnesses or args.require_formula_convention:
            if missing:
                raise ValueError('The complete witness report requires all 230 results')
            for n, (_, data) in records.items():
                try:
                    check_complete_witnesses(data, args.require_formula_convention)
                except AssertionError as exc:
                    raise ValueError('SG%d: %s' % (n, exc)) from exc
        stream = io.StringIO(newline='');writer = csv.DictWriter(stream, fieldnames=FIELDS);writer.writeheader()
        for n in range(1, 231):
            if n in records:writer.writerow(records[n][0])
            else:writer.writerow(dict(space_group=n, classification_status='missing', result_status='missing', stacking_status='missing'))
        files = {'independent_results.csv': stream.getvalue(), 'independent_results.md': markdown(records, manifest, output),
                 'independent_report.json': json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + '\n'}
        output.mkdir(parents=True, exist_ok=True)
        for name, content in files.items():
            target = output / name;temporary = target.with_suffix(target.suffix + '.tmp')
            temporary.write_text(content, encoding='utf-8');temporary.replace(target)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + '\n')
    print(json.dumps(dict(output=str(output), classification_groups=len(records), stacking_computed=manifest['stacking_status_counts'].get('computed', 0),
                          missing=missing, external_answers_consulted=False), sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
