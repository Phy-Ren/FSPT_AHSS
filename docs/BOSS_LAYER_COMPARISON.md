> Public release: this document describes the complete local audit. [Private reference inputs](../PUBLIC_RELEASE.md#private-comparison-materials) are not distributed; production and independent result audits remain reproducible.

# Boss PDF layer comparison

After the independent 230-group classification was frozen, the supplied PDF
`reference/space_group_230_layers.pdf` was parsed and compared using
`scripts/compare_boss.py`. It compares the PDF's **This calculation** columns
with `runs/classification_frozen`, verifying every hash in its manifest before
reading the numerical layer values.

All 920 layer entries agree: 230 p+ip, 230 Majorana, 230 complex-fermion and
230 bosonic entries. No current reference entry is missing. The outputs are
`results/boss_layers/reference_comparison.json`, `.csv`, and `.md`; the
positioned glyphs and both reference column sets are retained in
`parsed_reference.json`.

The PDF is dated 21 September 2026. It explicitly computes associated-graded
decoration layers and excludes stacking extensions. Its physical spin-half,
full infinite affine-group, determinant-sign and effective `omega=0`
conventions match the independent calculation. It retains weak phases and
atomic fermion parity. It provides abstract free factors, without a marked
surviving p+ip lattice, its index or primitive generators. Those stronger
independent outputs have no counterpart in this reference.

The PDF SHA-256 is
`c1421f2c2d26778a9bc3417181e4ef231e596b11ca79448115a472532c4f6d3a`.
It was checked against the original remote file
`/home/user/xyren/papers/space_group_230_layers.pdf`, not only the local copy.
The parser uses embedded text positions, without OCR. It assigns numerical
glyphs to their actual subscript or superscript baseline, so `Z_4`, `Z^3`, and
`Z_2^24` remain distinct. Every nonspace glyph in all eight group columns is
consumed; duplicate rows, incomplete tables and unrecognized annotations fail.

Rendered pages 7, 8 and 13 were also inspected visually, including SG1's free
rank, the mixed `Z + Z2` entries, SG16 and SG47's large powers, SG220's `Z4`,
and the three historically blank rows SG210, SG219 and SG228. These checks
agree with the extracted entries. Parsing the adjacent historical **Draft**
columns independently reproduces the PDF's own comparison summary: 30 p+ip
differences; one difference in each lower layer, at SG1; and three historical
blanks in each lower layer. These are differences from that older manuscript,
not from the newly frozen independent calculation.

Reproduce with Python and PyMuPDF:

```sh
python3 scripts/compare_boss.py
python3 tests/test_boss_parser.py
```

For a later complete production run, a separate comparison can be generated:

```sh
python3 scripts/compare_boss.py --current runs/FINAL_RUN
python3 tests/test_boss_current.py
```

This optional mode requires exactly 230 complete full results. Each must
pass the strict stored-witness audit, including actual torsion p+ip phase
relations and primitive free p+ip generators wherever those layers occur,
and use `normalized-pip-aw-edge-transport-v2`. Partial runs, classification-only
outputs, missing phase witnesses and older formula conventions are rejected
before any report is written.

The later run is explicitly described as a **post-reference formula/performance
regression run**, not as another calculation frozen before external answers
were read. The original `classification_frozen` manifest, its timestamp and
its result hashes remain unchanged. All 920 current layer entries are
compared both with that original freeze and with the PDF, with separate
counts and row-level differences. The current run's 230 result hashes and
its complete source-file hash maps are recorded separately.

The optional mode writes `current_reference_comparison.json`, `.csv` and
`.md` under the output directory. It preserves the original
`reference_comparison.*` files and records their hashes when present.
No later-run comparison has been declared complete here yet; it is run
only after the final 230 full results are available and accepted.

The new controls cover incomplete-run rejection, missing torsion/free phase
witnesses, obsolete formula conventions, all 230 current-result hashes,
separate difference counts, preservation of frozen provenance, and the
CLI's refusal to modify an existing report on failure. A separate regression
run without `--current` reproduced the original 920 matches and identical
frozen metadata, without changing the original manifest or reports.

This is a post-computation comparison utility. Neither the PDF, its parsed
values, nor the comparison script enters the independent production solver.
