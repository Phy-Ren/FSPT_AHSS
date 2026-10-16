#!/usr/bin/env python3
"""Render the mismatch inventory from current E8-inclusive source cells."""
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCES = ('Debray', 'R3_arxiv', 'R3_journal')
METHODS = {
    6: ('D2 degree count and independent charge obstruction', 'debray_d2.md'),
    10: ('C4 determinant Thom cofiber and exact Gysin presentation', 'S4_gysin.md'),
    14: ('Independent D8 Steenrod/Koszul bordism computation', 'd2d_bordism.md'),
    17: ('Normal C3 reduction to the Pin-c/Ci anchor', 'other_mismatches.md'),
    20: ('Normal C3 reduction to the independent C2h anchor', 'other_mismatches.md'),
    23: ('Normal C3 reduction to the independent C2h anchor', 'other_mismatches.md'),
    24: ('D2 bordism anchor and odd-kernel/odd-prime checks', 'debray_d2.md'),
    26: ('Normal C3 reduction to the C2v anchor', 'other_mismatches.md'),
    32: ('Independent Oh Adams calculation and shifted-ku summand', 'oh_audit.md'),
}


def group(value):
    if value is None:
        return 'UNVERIFIED'
    pieces = []
    rank = value.get('freeRank', 0)
    if rank:
        pieces.append('Z' if rank == 1 else 'Z^' + str(rank))
    for order, multiplicity in sorted(Counter(value['torsion']).items()):
        pieces.append('Z' + str(order) + ('^' + str(multiplicity) if multiplicity > 1 else ''))
    return ' × '.join(pieces) or '0'


def build(spin):
    path = ROOT / 'results/current/3p1d' / spin / 'point_groups.json'
    raw = path.read_bytes()
    table = json.loads(raw)
    rows = [r for r in table['rows'] if any(
        r['cells'][s].get('comparison_status') == 'mismatch' for s in SOURCES)]
    title = 'Spinless' if spin == 'spinless' else 'Spin-1/2'
    lines = [f'# 3+1D {title} point-group mismatch audit', '',
             'Audit date: 2026-10-16. All displayed groups include E8. These are',
             'interacting classifications. Each source column retains its printed value;',
             '**✓** / **×** compare that value with the current computation.',
             'UNVERIFIED means no pinned printed entry was extracted for that source.', '',
             '[Audit scope and conclusions](README.md). Independent calculations below',
             'support the current groups within the crystalline/bordism ansatz. They',
             'are our recomputations, not author-issued corrections.', '',
             '| Group | E8 layer | Current stacking | Arun Debray v3 (2026) | Zhang–Ning–Qi–Gu arXiv v2 (2024) | Zhang–Ning–Qi–Gu PRX (2025) | Independent audit |',
             '| --- | --- | --- | --- | --- | --- | --- |']
    records = []
    for row in rows:
        cells = row['cells']
        method, note = METHODS[int(row['id'].split('_')[1])]
        parts = [row['name'], group(cells['e']['group']), group(cells['stacking']['group'])]
        for source in SOURCES:
            cell = cells[source]
            marker = {'match': ' **✓**', 'mismatch': ' **×**'}.get(cell.get('comparison_status'), '')
            parts.append(group(cell.get('group')) + marker)
        parts.append(f'[{method}]({note})')
        lines.append('| ' + ' | '.join(parts) + ' |')
        records.append({'current_row': row, 'audit': {'method': method, 'note': note,
                        'conclusion': 'Independent bordism supports current stacking group',
                        'scope': 'Under the interacting crystalline/bordism ansatz; no universal formula-spectrum equivalence asserted'}})
    lines.extend(['', '## Sources', ''])
    for source in SOURCES:
        entry = table['sources'][source]
        lines.append(f"- {entry['authors']}, [{entry['title']}]({entry['url']}); {entry['version']}. Method: {entry['method']}.")
    lines.extend(['', 'The spinless D3h discrepancy is confined to the older arXiv version.' if spin == 'spinless'
                  else 'For C6h, the older arXiv value agrees; the journal value differs.', ''])
    (HERE / (spin + '.md')).write_text('\n'.join(lines))
    data = {'auditDate': '2026-10-16', 'physicalSpin': spin,
            'spacetimeDimension': 4, 'e8Included': True,
            'sourceTable': str(path.relative_to(ROOT)),
            'sourceTableSHA256': hashlib.sha256(raw).hexdigest(),
            'sources': {s: table['sources'][s] for s in SOURCES}, 'rows': records}
    (HERE / (spin + '.json')).write_text(json.dumps(data, indent=2) + '\n')
    return len(rows)


if __name__ == '__main__':
    print(json.dumps({spin: build(spin) for spin in ('spinless', 'spin_half')}))
