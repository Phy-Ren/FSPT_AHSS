# 4+1D geometric pairing checks

The archive contains the graph construction of the F and P moves with the
effective Majorana zero modes, the exact comparisons with the formulas, and the
two examples of the manuscript, together with the manuscript files they read.

Extract and run with Python 3.10+ and NumPy:

```bash
tar -xzf geometric_4d_verification.tar.gz
cd manuscript
python verification/verify_pip_examples.py
cd verification/geometric_4d
python check_geometry.py
python certify_geometry.py
python check_reference_formulas.py
python check_circuits.py
python check_cleanup.py
python check_negative_control.py
```

- `verify_pip_examples.py` builds the graphs of the two examples, checks every
  arrow of their figures and the tables of changing dimers, and recomputes the
  matrix Pfaffians. The intrinsic example has one odd ten-edge loop; in the
  full-background example an odd eight-edge loop and an odd two-edge loop
  cancel.
- `check_geometry.py` builds 1,280 P graphs and 384 F graphs with both
  backgrounds and compares their loop parities with the formulas.
- `certify_geometry.py` proves the source and product identities as exact
  Boolean coefficient identities on the whole local domain: 45 input bits for
  the source (30 remain in its reduced polynomial), 42 for the product and 75
  for their compatibility. All residuals vanish.
- `check_reference_formulas.py` evaluates the printed
  [pairing reference](../../FOUR_DIMENSIONAL_GEOMETRIC_REFERENCE.md) independently.
- `check_circuits.py` replays the even psi circuits.
- `check_cleanup.py` follows the P move until every reference dimer is back in
  place (about two minutes on one CPU).
- `check_negative_control.py` removes the contact on an input where it matters
  and confirms that the identity then fails.

`VERIFICATION.json` records the results and the hash of every archived file.
The graph runs are samples, not a census of all Boolean assignments; arbitrary
layer numbers are covered by the local matching and integer shuffle arguments,
which the explicit graphs test independently.
