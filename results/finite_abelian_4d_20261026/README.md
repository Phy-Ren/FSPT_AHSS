# Finite Abelian fermionic SPT groups in 4+1 dimensions

This folder evaluates the complete abstract stacking group for finite **unitary Abelian** fermionic symmetry

\[
G_f=C_{2m}^{f}\times\prod_i C_{N_i}.
\]

Fermion parity is the element of order two in the distinguished cyclic factor.
The default `--fermionic-order 2` is the split case, \(C_2^f\times A\).
Arbitrary positive spectator orders are allowed.
The output lists cyclic invariant factors in divisibility order.
An empty list denotes the trivial group.
The calculation first separates prime powers and then uses closed formulas for factors of bounded rank; it does not rerun the full AHSS computation.

The general answer is a **mathematical classification**.
It does not claim a physical construction of the terminal \(p+ip\) Berry phase.
The elementary family \(C_4^f\times C_2^r\) is independent of that missing physical construction: its integer-decoration summand is split off by projection to \(C_4^f\), and the remaining summands have no integer decoration.

## Run

Use Python 3 and the exact-arithmetic dependency in `requirements.txt`:

```sh
python -m pip install -r requirements.txt
python classify.py --fermionic-order 4 --spectators 2 2 2
python classify.py --fermionic-order 2 --spectators 4 4 4
python classify.py --fermionic-order 8 --spectators 4 4
python check.py --output verification_report.json
```

All scripts also work when invoked by their full path from another working directory.
The first example returns

\[
C_2^{12}\times C_4^3\times C_8^3\times C_{16}.
\]

The optional `python check.py --deep` additionally repeats 1,822 numerical matrix comparisons.
Those comparisons are regression tests, not the proof for arbitrary exponents.

## What is proved

The stable product splitting reduces the classification to cyclic-factor supports.
For split symmetry, the support formulas follow from the cyclic calculation, low Moore-spectrum groups, and the explicitly described cell attachments.
For nonsplit symmetry, the cyclic and one-spectator groups follow from the two-circle Gysin complex and its integral index lattice.
Supports with at least two spectators reduce to the tensor-resolution cochain matrices for \(\operatorname{Sq}^2+\omega_2\), including the incoming identifications and the complex-fermion doubling relations.

The two- and three-spectator closed formulas are proved for **all exponents**.
The tensor differential splits into Koszul blocks.
An integral basis change normalizes each block to its smallest cyclic order.
Modulo two, only the order comparisons and the factors of order two remain.
The resulting 16 and 40 order patterns are exhaustive.
For each pattern, the supplied integer or polynomial matrices satisfy an exact unimodular Smith identity.
The polynomial identities hold for an unrestricted parameter, so no exponent cutoff enters the proof.
The one-spectator reduction is also verified symbolically through Newton differences and an explicit two-generator relation matrix.

The principal proof files are:

- `proofs/FULL_SPLIT_FORMULA.md`, with the two-, three-, and four-factor Moore-space derivations.
- `proofs/TWO_FACTOR_GYSIN_PROOF.md` and `proofs/ONE_SPECTATOR_SYMBOLIC_SMITH_PROOF.md`.
- `proofs/EXACT_HIGH_SUPPORT_SMITH_FORMULA.md` and `proofs/ALL_EXPONENT_SMITH_CERTIFICATE.md`.
- `proofs/MOORE_PRIMARY_SOURCE_AUDIT.md`, which identifies the precise topological input in Oka's Moore-spectrum paper.

The six primitive index polynomials have an independent integral certificate in `data/primitive_index_lattice.json`.
Its geometric index rows generate the entire lattice; the stored integer left inverse and determinant-one evaluation matrix are checked by `check.py`.

## Reproducibility checks

`check.py` verifies the following:

1. All 51 previously archived full groups: 26 split and 25 nonsplit.
2. Both elementary rank formulas for ranks zero through eight, 32 independent cyclic eta computations, and 64 exact rank-two Smith computations.
3. The six archived nonsplit higher-support blocks, including their bosonic and complex-fermion graded groups.
4. Every one of the 56 exhaustive symbolic order-pattern certificates, regenerated from the cochain matrices, together with the one-spectator symbolic identities and primitive index certificate.
5. Four independent marked-Majorana obstruction calculations, including their raw-file SHA-256 receipts.
6. A separate full computation for \(C_2^f\times C_4^3\), including its exact Smith transformations, giving \(C_2^4\times C_4^{10}\).
7. The hashes of the distributed files in `SHA256SUMS.json`.

`verification_report.json` records the completed default checks.
`data/high_support_grid_original.json` records the separate 1,822-case regression grid.

## Data provenance

`data/archived_51.json` contains the archived classifications, marked extension data, support decompositions, and the original result hashes.
Its `FSPT_AHSS/...` references are paths relative to the public formula repository; the original large calculation outputs are not duplicated here.
The check compares these archived results with the formulas in this folder.
It does not claim to regenerate all 51 full runs.

The four raw files `checkpoints/*/secondary.json` are preserved byte for byte.
They test the class \(x_1x_2x_3\): it survives for \(C_4^3\) and \(C_2\times C_8^2\), and is obstructed for \(C_2\times C_4^2\) and \(C_2\times C_4\times C_8\).
These are marked-class checks, not full-group computations.
The original schema name is retained as provenance.
The source pin and the corrected export-instrumentation pin share the same scientific source identifier.
Their only instrumentation difference concerns exporting the rational target basis and differential matrices.

`full_results/split_C4_C4_C4/` contains a separate full-group result, input check, completion record, and filtration certificate.
In its portable result file, only the absolute source-snapshot path was replaced by a content-addressed identifier; JSON whitespace was compacted.
The receipt records the original hash, the distributed-file hash, and a canonical hash of every unchanged scientific field.
The full presentation and both unimodular Smith transformations are checked directly.

## Code map

- `classify.py`: command-line interface using the physical order of the fermionic factor.
- `split_closed_formula.py`, `nonsplit_closed_formula.py`, `higher_support.py`: the closed formulas.
- `supercohomology_blocks.py`: independent exact cochain-matrix computation for nonsplit higher supports.
- `koszul_stabilization.py`: construction and verification of the exhaustive symbolic Smith certificates.
- `one_spectator_symbolic_certificate.py`: unrestricted symbolic one-spectator reduction.
- `two_factor_cubic_lattice.py`, `cyclic_eta_smith.py`: exact low-support relation matrices.
- `low_operations.py`: the split tensor-resolution differential and Steenrod operations used in the proof notes.
- `check.py`: the reproducibility checks described above.
