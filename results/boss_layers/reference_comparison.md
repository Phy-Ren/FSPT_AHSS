# Frozen independent calculation vs supplied boss PDF

**920/920 layer entries match. Mismatches: 0. Missing current-reference entries: 0.**

The independent 230-group classification was frozen before opening this reference. Every frozen result SHA-256 was rechecked. The comparison uses the PDF’s **This calculation** columns; its adjacent **Draft** columns describe an earlier manuscript.

| Layer | Match | Mismatch | Missing reference |
|---|---:|---:|---:|
| p+ip | 230 | 0 | 0 |
| Majorana | 230 | 0 | 0 |
| Complex fermion | 230 | 0 | 0 |
| Bosonic | 230 | 0 | 0 |

## Differences

None across all 230 groups and four layers.

## Meaning and source audit

Both calculations use the full infinite affine group, physical spin-half convention, determinant orientation sign and effective `omega=0`, retaining weak and atomic fermion-parity phases (PDF pages 1–2). The comparison concerns final associated-graded groups. The PDF does not provide a full stacking group or the embedding/index of a surviving free p+ip lattice; agreement here cannot certify either.

All 230 rows on PDF pages 7–13 were parsed from positioned text glyphs. The parser distinguishes the baseline, superscript multiplicity and subscript cyclic order, including powers such as `Z2^16` and `Z2^24`. It uses no OCR and consumes every nonspace group-cell glyph. `parsed_reference.json` retains glyph coordinates for every current and historical cell.

As a separate extraction cross-check, the PDF current-vs-historical-draft columns give:

| Layer | Match | Mismatch | Historical blank |
|---|---:|---:|---:|
| p+ip | 200 | 30 | 0 |
| Majorana | 226 | 1 | 3 |
| Complex fermion | 226 | 1 | 3 |
| Bosonic | 226 | 1 | 3 |

p+ip historical differences: SG 7, 9, 27, 29, 30, 32, 33, 34, 37, 41, 43, 45, 103, 104, 106, 110, 112, 114, 116, 117, 118, 120, 122, 158, 159, 161, 184, 218, 219, 220. Historical blanks: none.

Majorana historical differences: SG 1. Historical blanks: 210, 219, 228.

Complex fermion historical differences: SG 1. Historical blanks: 210, 219, 228.

Bosonic historical differences: SG 1. Historical blanks: 210, 219, 228.

Those historical-draft differences are not discrepancies with the newly frozen independent results.

Reference: [supplied PDF](../../PUBLIC_RELEASE.md#private-comparison-materials). Independent freeze: [manifest](../classification_frozen/manifest.json).

Reference PDF SHA-256: `c1421f2c2d26778a9bc3417181e4ef231e596b11ca79448115a472532c4f6d3a`.

Frozen manifest SHA-256: `42e42ce70900bf0df2dada35624198474f07e4a98dfe95770d462a69169ec438`.

The CSV contains every one of the 920 comparisons, its PDF page and independent source ID. JSON preserves the reference hashes and all frozen result hashes. No production formula or frozen result was modified by this comparison.
