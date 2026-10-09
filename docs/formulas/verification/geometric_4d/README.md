# Native 4+1D pairings and their canonical comparison

The portable archive contains the physical graph constructor, frozen author-supplied
inputs, exact Boolean coefficient comparisons, even local circuits, complete
cleanup and inverse-reset tests, and both regenerated manuscript examples.
The constructor does not import its mathematical comparator. The five ordinary
four-end configurations are independently transcribed from the original diagram.

Extract and run with Python 3.10+ and NumPy:

```bash
tar -xzf geometric_4d_verification.tar.gz
python manuscript/verification/verify_pip_examples.py
cd manuscript/verification/geometric_4d
python check_geometry.py
python certify_geometry.py
python check_reference_formulas.py
python check_circuits.py
python check_cleanup.py
python check_reset.py
python check_negative_control.py
```

`VERIFICATION.json` records the individual results and every archived file hash.
The graph census covers 1,280 P graphs, 384 reduced F graphs and 128 unreduced
F graphs with both backgrounds, supplemented by separate circuit, cleanup,
negative-integer and reset cases. It is not a census of all Boolean assignments.
The exact polynomial comparisons cover the complete local domain: 45 input
bits for the source (30 survive in its reduced polynomial), 42 for the product,
and 75 for their compatibility. All coefficient residuals vanish. The proof
for arbitrary central-list lengths and integer shuffles is separate from
these finite graph checks. The capped effective mass model was also checked
with 97,828 signed partner cases and 32 independent matrix Pfaffians.

The current physical rule is the one in
[the reference comparison](../../FOUR_DIMENSIONAL_GEOMETRIC_REFERENCE.md).
Its complete F count is O5 + d B4; its complete P count is
E4 + Delta B4 + d B3, using the actual lower product. Neither a closed
residual nor a reference dimer is dropped. The canonical terminal phase,
gauge maps and self-products keep their established common coordinate.
The lower parity calculation does not constitute a new microscopic terminal
U(1) phase derivation.

The archive's `frozen/` inputs are byte-preserved, including historical
comments from stages before the capped contact was supplied. Their present
status is specified by the new wrapper and tests, not by those old comments.
The mass calculation concerns the specified stabilized effective seam model;
it is not a uniqueness theorem for a microscopic chiral parent.
