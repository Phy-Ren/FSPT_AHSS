#!/usr/bin/env python3
"""Compare frozen independent layers with the supplied boss PDF, read-only.

PyMuPDF is used only by this post-computation report. Positioned PDF glyphs
distinguish subscripts from superscripts; no OCR or expected-answer corrections
are used. The reference's historical Draft columns are retained separately.
"""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import sys

import fitz

from audit_run import check_complete_witnesses, check_result
from report_results import group_name

LAYERS = ('pip', 'majorana', 'complex_fermion', 'bosonic')
LABELS = dict(zip(LAYERS, ('p+ip', 'Majorana', 'Complex fermion', 'Bosonic')))
CURRENT_FORMULA_CONVENTION = 'normalized-pip-aw-edge-transport-v2'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def positioned_spans(page):
    spans = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            for span in line['spans']:
                if not span['text'].strip():
                    continue
                box = fitz.Rect(span['bbox']) * page.rotation_matrix
                origin = fitz.Point(span['origin']) * page.rotation_matrix
                spans.append(dict(text=span['text'].strip(), box=list(box), x=origin.x,
                                  y=origin.y, font_size=span['size']))
    return spans


def parse_group(spans):
    """Parse cyclic factors using actual baseline geometry, consuming all spans."""
    ordered = sorted(spans, key=lambda s: (round(s['x'], 2), s['y']))
    texts = [s['text'] for s in ordered]
    if texts == ['0']:
        return []
    if len(texts) == 1 and texts[0] in ('–', '−', '—', '-'):
        return None
    bases = [s for s in ordered if s['text'] == 'Z']
    if not bases:
        raise ValueError('unrecognized group cell: %r' % texts)
    assigned = {id(z): dict(sub=[], sup=[]) for z in bases}
    plus = 0
    for span in ordered:
        if span['text'] == 'Z':
            continue
        if span['text'] in ('⊕', '+'):
            plus += 1
            continue
        if not re.fullmatch(r'[0-9]+', span['text']):
            raise ValueError('unrecognized group glyph: %r' % span)
        prior = [z for z in bases if z['x'] < span['x'] + 0.05]
        if not prior:
            raise ValueError('numeric annotation without preceding Z')
        base = max(prior, key=lambda z: z['x'])
        delta = span['y'] - base['y']
        if span['font_size'] >= base['font_size'] - 1 or abs(delta) < 0.5:
            raise ValueError('unresolved superscript/subscript: %r' % texts)
        assigned[id(base)]['sub' if delta > 0 else 'sup'].append(span)
    if plus != len(bases)-1:
        raise ValueError('unexpected number of direct-sum symbols: %r' % texts)
    orders = []
    for base in bases:
        parts = assigned[id(base)]
        for key in parts:
            parts[key].sort(key=lambda s: s['x'])
        sub = ''.join(s['text'] for s in parts['sub'])
        sup = ''.join(s['text'] for s in parts['sup'])
        order = int(sub) if sub else 0
        count = int(sup) if sup else 1
        if order == 1 or order < 0 or not 1 <= count <= 100:
            raise ValueError('invalid group order/power: %r' % texts)
        orders.extend([order]*count)
    return sorted(orders)


def parse_reference(pdf):
    document = fitz.open(str(pdf))
    entries = {}
    pages = []
    for page_index, page in enumerate(document):
        spans = positioned_spans(page)
        no_headers = [s for s in spans if s['text'] == 'No.']
        draft_headers = [s for s in spans if s['text'] == 'Draft']
        this_headers = [s for s in spans if s['text'] == 'This']
        if len(draft_headers) != 4 or len(this_headers) != 4 or len(no_headers) != 1:
            continue
        header_y = draft_headers[0]['y']
        if any(abs(s['y']-header_y) > 0.1 for s in draft_headers+this_headers):
            raise ValueError('table headers do not share a baseline')
        number_header = no_headers[0]
        if number_header['y'] > header_y + 0.1:
            raise ValueError('unexpected number header below layer header')
        calculations = sorted([s for s in spans if s['text'] == 'calculation' and abs(s['y']-header_y) < 0.1], key=lambda s: s['x'])
        this_headers.sort(key=lambda s: s['x'])
        draft_headers.sort(key=lambda s: s['x'])
        if len(calculations) != 4:
            raise ValueError('missing current-calculation headers')
        centers = []
        for current, tail, draft in zip(this_headers, calculations, draft_headers):
            centers.extend([(current['box'][0]+tail['box'][2])/2,
                            (draft['box'][0]+draft['box'][2])/2])
        left = this_headers[0]['box'][0]
        bounds = [left]+[(a+b)/2 for a, b in zip(centers, centers[1:])]+[draft_headers[-1]['box'][2]+12]
        row_numbers = sorted([s for s in spans if re.fullmatch(r'[0-9]+', s['text'])
                              and number_header['box'][0]-2 <= s['box'][0] <= number_header['box'][2]
                              and abs(s['font_size']-number_header['font_size']) < 0.1
                              and s['y'] > header_y+5], key=lambda s: s['y'])
        page_groups = []
        for number in row_numbers:
            n = int(number['text'])
            if not 1 <= n <= 230 or n in entries:
                raise ValueError('duplicate/invalid table group %s on page %s' % (n, page_index+1))
            y = number['y']
            row = [s for s in spans if abs(s['y']-y) < 5.5]
            names = sorted([s for s in row if number_header['box'][2]+4 <= s['x'] < left], key=lambda s: s['x'])
            if not names:
                raise ValueError('missing space group name for SG%d' % n)
            name = ''.join(s['text'] for s in names)
            cells = []
            for lo, hi in zip(bounds, bounds[1:]):
                glyphs = [s for s in row if lo <= s['x'] < hi]
                orders = parse_group(glyphs)
                cells.append(dict(orders=orders, group=group_name(orders) if orders is not None else None,
                                  glyphs=[dict(text=s['text'], x=round(s['x'], 5), baseline_y=round(s['y'], 5),
                                               font_size=round(s['font_size'], 5), box=[round(v, 5) for v in s['box']]) for s in glyphs]))
            entries[n] = dict(space_group=n, name=name, pdf_page=page_index+1,
                              baseline_y=round(y, 5), current=dict(zip(LAYERS, cells[::2])),
                              historical_draft=dict(zip(LAYERS, cells[1::2])))
            page_groups.append(n)
        pages.append(dict(page=page_index+1, groups=page_groups, column_centers=centers))
    if set(entries) != set(range(1, 231)):
        raise ValueError('incomplete reference table: missing %r' % sorted(set(range(1, 231))-set(entries)))
    return dict(entries=entries, pages=pages, page_count=len(document),
                parser='positioned PDF glyph baselines; direct sum/subscript/superscript parsed independently',
                pymupdf_version=fitz.VersionBind)


def load_frozen(directory):
    if not __debug__:
        raise ValueError('Run without Python -O: the shared source/certificate auditor uses assertions')
    manifest_path = directory / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    if manifest['groups'] != 230 or manifest['external_answers_consulted'] is not False:
        raise ValueError('input is not a complete pre-reference classification freeze')
    expected = {'sg%d.json' % n for n in range(1, 231)}
    if set(manifest['result_sha256']) != expected:
        raise ValueError('frozen manifest does not certify exactly 230 groups')
    records = {}
    for n in range(1, 231):
        path = directory / ('sg%d.json' % n)
        if digest(path) != manifest['result_sha256'][path.name]:
            raise ValueError('frozen result hash mismatch: ' + path.name)
        data = json.loads(path.read_text())
        if data['space_group'] != n:
            raise ValueError('frozen result filename/group mismatch')
        check_result(data)
        records[n] = data
    return records, manifest, digest(manifest_path)


def load_current(directory):
    """Audit a complete later run; never describe it as a pre-reference freeze."""
    if not __debug__:
        raise ValueError('Run without Python -O: complete-witness checks use assertions')
    expected = {'sg%d.json' % n for n in range(1, 231)}
    actual = {p.name for p in directory.glob('sg*.json') if '.raw.' not in p.name}
    if actual != expected:
        raise ValueError('current run must contain exactly 230 complete results; missing=%r extra=%r' %
                         (sorted(expected-actual), sorted(actual-expected)))
    records, result_hashes, source_hashes = {}, {}, {}
    for n in range(1, 231):
        path = directory / ('sg%d.json' % n)
        raw = path.read_bytes()
        data = json.loads(raw)
        if data['space_group'] != n:
            raise ValueError('current result filename/group mismatch: ' + path.name)
        try:
            check_complete_witnesses(data, CURRENT_FORMULA_CONVENTION)
        except (AssertionError, KeyError, TypeError, ValueError, IndexError) as exc:
            raise ValueError('current %s failed strict witness audit: %s' % (path.name, exc)) from exc
        source = data['source_id']
        if source in source_hashes and source_hashes[source] != data['source_sha256']:
            raise ValueError('inconsistent source hashes for ' + source)
        source_hashes[source] = data['source_sha256']
        result_hashes[path.name] = hashlib.sha256(raw).hexdigest()
        records[n] = data
    return records, dict(directory=str(directory.resolve()), groups=len(records),
        comparison_role='post-reference formula/performance regression run; not a pre-reference freeze',
        complete_witnesses_required=True, complete_witnesses_passed=True,
        required_formula_convention=CURRENT_FORMULA_CONVENTION,
        source_ids=sorted(source_hashes), source_sha256=source_hashes,
        result_sha256=result_hashes)


def compare(reference, frozen):
    rows = []
    for n in range(1, 231):
        ref = reference['entries'][n]
        actual = frozen[n]
        for layer in LAYERS:
            ours = sorted(actual['pip']['orders'] if layer == 'pip' else actual[layer])
            expected = ref['current'][layer]['orders']
            draft = ref['historical_draft'][layer]['orders']
            status = 'missing-reference' if expected is None else ('match' if ours == expected else 'mismatch')
            rows.append(dict(space_group=n, space_group_name=ref['name'], layer=layer,
                independent_orders=ours, independent_group=group_name(ours),
                reference_orders=expected, reference_group=group_name(expected) if expected is not None else None,
                status=status, historical_draft_orders=draft,
                historical_draft_group=group_name(draft) if draft is not None else None,
                current_reference_vs_draft='blank' if draft is None else ('match' if expected == draft else 'mismatch'),
                pdf_page=ref['pdf_page'], independent_source_id=actual['source_id']))
    return rows


def compare_current(frozen_report, current, provenance):
    """Keep original freeze provenance intact and compare all three layer sets."""
    rows = []
    for old in frozen_report['rows']:
        n, layer = old['space_group'], old['layer']
        data = current[n]
        orders = sorted(data['pip']['orders'] if layer == 'pip' else data[layer])
        ref_orders = old['reference_orders']
        rows.append(dict(space_group=n, space_group_name=old['space_group_name'], layer=layer,
            current_orders=orders, current_group=group_name(orders),
            frozen_orders=old['independent_orders'], frozen_group=old['independent_group'],
            reference_orders=ref_orders, reference_group=old['reference_group'],
            current_vs_frozen='match' if orders == old['independent_orders'] else 'mismatch',
            current_vs_reference='missing-reference' if ref_orders is None else
                                 ('match' if orders == ref_orders else 'mismatch'),
            frozen_vs_reference=old['status'], pdf_page=old['pdf_page'],
            frozen_source_id=old['independent_source_id'], current_source_id=data['source_id'],
            current_result_sha256=provenance['result_sha256']['sg%d.json' % n]))
    comparisons = ('current_vs_frozen', 'current_vs_reference', 'frozen_vs_reference')
    counts = {comparison: dict(Counter(row[comparison] for row in rows)) for comparison in comparisons}
    return dict(schema='fspt-boss-current-four-layer-comparison-v1',
        compared_at=datetime.now(timezone.utc).isoformat(),
        reference=frozen_report['reference'], frozen=frozen_report['frozen'], current=provenance,
        convention=frozen_report['convention'],
        scope=frozen_report['scope'],
        free_lattice_comparison=frozen_report['free_lattice_comparison'],
        full_stacking_comparison=frozen_report['full_stacking_comparison'],
        chronology='The original independent classification freeze preceded consultation of external answers. '
                   'The current run is a later formula/performance regression run; it is not claimed to precede that consultation.',
        total_entries=len(rows), counts=counts,
        counts_by_layer={comparison: {layer: dict(Counter(row[comparison] for row in rows if row['layer'] == layer))
                                     for layer in LAYERS} for comparison in comparisons},
        mismatches={comparison: [row for row in rows if row[comparison] == 'mismatch'] for comparison in comparisons},
        missing_reference_entries=[row for row in rows if row['current_vs_reference'] == 'missing-reference'],
        rows=rows)


def render_current(report):
    lines = ['# Current regression run vs original freeze and supplied boss PDF', '',
        report['chronology'], '',
        'All 230 current full results passed strict complete-witness and `%s` checks. '
        'The original frozen manifest and each of its result hashes were rechecked without modification.' %
        CURRENT_FORMULA_CONVENTION, '',
        '| Comparison | Match | Mismatch | Missing reference |', '|---|---:|---:|---:|']
    for key in ('current_vs_frozen', 'current_vs_reference', 'frozen_vs_reference'):
        counts = report['counts'][key]
        lines.append('| %s | %d | %d | %d |' %
                     (key, counts.get('match', 0), counts.get('mismatch', 0), counts.get('missing-reference', 0)))
    lines += ['', 'The PDF supplies four abstract filtration quotients. It supplies neither full stacking '
              'extensions nor marked free-lattice embeddings; these comparisons do not validate those additional outputs.', '',
              'Original frozen manifest SHA-256: `%s`.' % report['frozen']['manifest_sha256'], '',
              'Current source IDs: '+', '.join('`%s`' % s for s in report['current']['source_ids'])+'.', '',
              'The JSON retains all original frozen result hashes and, separately, all current result '
              'and source-file hashes. The original `reference_comparison.*` reports are preserved.', '',
              '## Differences', '']
    different = [row for row in report['rows'] if row['current_vs_frozen'] != 'match' or row['current_vs_reference'] != 'match']
    if not different:
        lines.append('None across all 230 groups and four layers.')
    else:
        lines += ['| SG | Layer | Original frozen | Current | PDF current |', '|---:|---|---|---|---|']
        for row in different:
            lines.append('| %d | %s | `%s` | `%s` | `%s` |' %
                         (row['space_group'], LABELS[row['layer']], row['frozen_group'],
                          row['current_group'], row['reference_group']))
    return '\n'.join(lines)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, default=Path('reference/space_group_230_layers.pdf'))
    parser.add_argument('--text', type=Path, default=Path('reference/space_group_230_layers.txt'))
    parser.add_argument('--frozen', type=Path, default=Path('runs/classification_frozen'))
    parser.add_argument('--current', type=Path,
                        help='Optional complete later run: audit all 230 full AW-v2 witnesses and write separate current comparison reports')
    parser.add_argument('--output', type=Path, default=Path('results/boss_layers'))
    args = parser.parse_args()
    try:
        current, current_provenance = load_current(args.current) if args.current is not None else (None, None)
        reference = parse_reference(args.pdf)
        frozen, manifest, manifest_hash = load_frozen(args.frozen)
        rows = compare(reference, frozen)
        counts = {layer: dict(Counter(r['status'] for r in rows if r['layer'] == layer)) for layer in LAYERS}
        draft_counts = {layer: dict(Counter(r['current_reference_vs_draft'] for r in rows if r['layer'] == layer)) for layer in LAYERS}
        mismatches = [r for r in rows if r['status'] == 'mismatch']
        missing = [r for r in rows if r['status'] == 'missing-reference']
        report = dict(schema='fspt-boss-four-layer-comparison-v1', compared_at=datetime.now(timezone.utc).isoformat(),
            reference=dict(title='Spin-half crystalline fermionic SPT phases: AHSS decoration layers for all 230 space groups',
                           date='2026-09-21', pdf=str(args.pdf.resolve()), pdf_sha256=digest(args.pdf),
                           extracted_text=str(args.text.resolve()), extracted_text_sha256=digest(args.text),
                           columns_compared='This calculation; the Draft columns are historical context only',
                           pages=reference['pages'], parser=reference['parser'], pymupdf_version=reference['pymupdf_version']),
            frozen=dict(directory=str(args.frozen.resolve()), manifest_sha256=manifest_hash,
                        frozen_at=manifest['frozen_at'], external_answers_consulted_at_freeze=False,
                        result_sha256=manifest['result_sha256']),
            convention=dict(independent='physical-spin-half-det-sign-omega0', reference_pages=[1, 2, 6],
                matching=True, description='Full infinite affine space groups; s=det orientation character; effective omega=0; weak phases and atomic fermion parity retained; no extra onsite time reversal or charge conservation.'),
            scope='four final associated-graded abstract layer groups, not a stacking extension or a marked free lattice',
            free_lattice_comparison='not available: PDF specifies abstract Z^r factors and no primitive lattice basis/index',
            full_stacking_comparison='not available: PDF expressly excludes stacking-extension computation',
            counts=counts, matches=sum(r['status']=='match' for r in rows), total_entries=len(rows),
            mismatches=mismatches, missing_reference_entries=missing,
            current_reference_vs_historical_draft=draft_counts,
            historical_draft_details={layer: dict(
                mismatch_groups=[r['space_group'] for r in rows if r['layer'] == layer and r['current_reference_vs_draft'] == 'mismatch'],
                blank_groups=[r['space_group'] for r in rows if r['layer'] == layer and r['current_reference_vs_draft'] == 'blank']) for layer in LAYERS},
            rows=rows)
        stream = io.StringIO(newline='')
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, separators=(',', ':')) if isinstance(v, list) else v for k, v in row.items()})
        lines = ['# Frozen independent calculation vs supplied boss PDF', '',
            '**%d/%d layer entries match. Mismatches: %d. Missing current-reference entries: %d.**' %
            (report['matches'], len(rows), len(mismatches), len(missing)), '',
            'The independent 230-group classification was frozen before opening this reference. Every frozen result SHA-256 was rechecked. The comparison uses the PDF’s **This calculation** columns; its adjacent **Draft** columns describe an earlier manuscript.', '',
            '| Layer | Match | Mismatch | Missing reference |', '|---|---:|---:|---:|']
        for layer in LAYERS:
            c = counts[layer]
            lines.append('| %s | %d | %d | %d |' % (LABELS[layer], c.get('match', 0), c.get('mismatch', 0), c.get('missing-reference', 0)))
        lines += ['', '## Differences', '']
        if not mismatches and not missing:
            lines.append('None across all 230 groups and four layers.')
        else:
            lines += ['| SG | Layer | Independent | PDF current | Page |', '|---:|---|---|---|---:|']
            for r in mismatches+missing:
                lines.append('| %d | %s | `%s` | `%s` | %d |' % (r['space_group'], LABELS[r['layer']], r['independent_group'], r['reference_group'], r['pdf_page']))
        lines += ['', '## Meaning and source audit', '',
            'Both calculations use the full infinite affine group, physical spin-half convention, determinant orientation sign and effective `omega=0`, retaining weak and atomic fermion-parity phases (PDF pages 1–2). The comparison concerns final associated-graded groups. The PDF does not provide a full stacking group or the embedding/index of a surviving free p+ip lattice; agreement here cannot certify either.', '',
            'All 230 rows on PDF pages 7–13 were parsed from positioned text glyphs. The parser distinguishes the baseline, superscript multiplicity and subscript cyclic order, including powers such as `Z2^16` and `Z2^24`. It uses no OCR and consumes every nonspace group-cell glyph. `parsed_reference.json` retains glyph coordinates for every current and historical cell.', '',
            'As a separate extraction cross-check, the PDF current-vs-historical-draft columns give:', '',
            '| Layer | Match | Mismatch | Historical blank |', '|---|---:|---:|---:|']
        for layer in LAYERS:
            c = draft_counts[layer]
            lines.append('| %s | %d | %d | %d |' % (LABELS[layer], c.get('match', 0), c.get('mismatch', 0), c.get('blank', 0)))
        for layer in LAYERS:
            detail = report['historical_draft_details'][layer]
            different = ', '.join(map(str, detail['mismatch_groups'])) or 'none'
            blank = ', '.join(map(str, detail['blank_groups'])) or 'none'
            lines += ['', '%s historical differences: SG %s. Historical blanks: %s.' % (LABELS[layer], different, blank)]
        lines += ['',
            'Those historical-draft differences are not discrepancies with the newly frozen independent results.', '',
            'Reference: [supplied PDF](../../reference/space_group_230_layers.pdf). Independent freeze: [manifest](../../runs/classification_frozen/manifest.json).', '',
            'Reference PDF SHA-256: `%s`.' % report['reference']['pdf_sha256'], '',
            'Frozen manifest SHA-256: `%s`.' % manifest_hash, '',
            'The CSV contains every one of the 920 comparisons, its PDF page and independent source ID. JSON preserves the reference hashes and all frozen result hashes. No production formula or frozen result was modified by this comparison.', '']
        if current is not None:
            report = compare_current(report, current, current_provenance)
            report['preserved_original_report_sha256'] = {
                p.name: digest(p) for p in
                [args.output / ('reference_comparison.'+suffix) for suffix in ('json', 'csv', 'md')]
                if p.is_file()}
            stream = io.StringIO(newline='')
            writer = csv.DictWriter(stream, fieldnames=list(report['rows'][0]))
            writer.writeheader()
            for row in report['rows']:
                writer.writerow({k: json.dumps(v, separators=(',', ':')) if isinstance(v, list) else v
                                 for k, v in row.items()})
            args.output.mkdir(parents=True, exist_ok=True)
            for suffix, content in [('json', json.dumps(report, indent=2, sort_keys=True)+'\n'),
                                    ('csv', stream.getvalue()), ('md', render_current(report))]:
                (args.output / ('current_reference_comparison.'+suffix)).write_text(content, encoding='utf-8')
            print(json.dumps(dict(output=str(args.output), current_groups=230,
                                  counts=report['counts'], original_freeze_unchanged=True), sort_keys=True))
            return
        args.output.mkdir(parents=True, exist_ok=True)
        outputs = dict(reference_comparison_json=json.dumps(report, indent=2, sort_keys=True)+'\n',
                       reference_comparison_csv=stream.getvalue(), reference_comparison_md='\n'.join(lines),
                       parsed_reference_json=json.dumps(reference, indent=2, sort_keys=True)+'\n')
        for key, content in outputs.items():
            stem, extension = key.rsplit('_', 1)
            (args.output / (stem+'.'+extension)).write_text(content, encoding='utf-8')
        print(json.dumps(dict(output=str(args.output), counts=counts, matches=report['matches'],
                              mismatches=len(mismatches), missing=len(missing), historical_draft=draft_counts), sort_keys=True))
    except (OSError, ValueError, AssertionError, KeyError, TypeError, IndexError) as exc:
        parser.exit(1, '%s: %s\n' % (type(exc).__name__, exc))


if __name__ == '__main__':
    main()
