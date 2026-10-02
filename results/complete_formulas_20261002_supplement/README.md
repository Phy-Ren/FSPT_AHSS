# Accepted finite examples, 2026-10-02 supplement

These five completed 4+1D internal-symmetry calculations are separate from the
original 832-record release. Their exact input catalogs contain the complete
multiplication table, normalized omega2, grading s1 and generator indices.

| Input | Bosonic quotient | Full stacking group | Final Bos / CF / Majorana / p+ip |
|---|---|---|---|
| S4_orbit_000 | S4, omega2=s1=0 | Trivial | 0 / 0 / 0 / 0 |
| Q24_orbit_000 | Q24, omega2=s1=0 | Z2 × Z2 | 0 / Z2 / Z2 / 0 |
| Q24_orbit_004 | Binary dihedral Q24 of order 24 | Trivial | 0 / 0 / 0 / 0 |
| Q24_orbit_005 | Binary dihedral Q24 of order 24 | Z4 | Z2 / Z2 / 0 / 0 |
| Q24_orbit_006 | Binary dihedral Q24 of order 24 | Trivial | 0 / 0 / 0 / 0 |

Q24 names the **bosonic quotient** here, not a fermionic group with a smaller
bosonic quotient. All five cases passed complete classification, stacking, incoming
gauge reduction, recorded coherence checks, and independent integer presentation
and filtration audits. Q24_orbit_000 matches an independent full-group target.
For the trivial background, quotienting the normal C3 subgroup gives Q8 and
identifies the full two-primary Spin bordism group. The published Q8 result is
Z2 squared ([Davighi, Gripaios and Lohitsiri, Table 1 and Appendix A](https://arxiv.org/abs/2207.10700)).
The remaining three-primary part vanishes because quotient conjugation inverts
C3 and acts by minus one on its degree-five Spin group. This target was prepared
before the new calculation.

S4_orbit_000 also has an independent transfer proof, obtained **after** observing
its computed result. At two, transfer into its index-three Sylow D8 subgroup is
injective and the published untwisted D8 degree-five Spin group vanishes. At
three, transfer into C3 is injective; the normalizer acts by inversion, with
no fixed class on either total-degree-five Spin AHSS piece. Hence the S4 group
vanishes. Transfer injectivity here follows from the finite AHSS filtration
and the invertible covering degree; a literal scalar stable transfer map is
not assumed ([Becker–Gottlieb, Sections 3 and 5](https://www.math.purdue.edu/~gottlieb/Bibliography/Transfb.pdf)).
The supplement therefore adds two independent full-target comparisons: one
prospective and one post hoc, separately from the original catalog's 49.

The other three Q24 cases agree with separately prepared predictions transferred
from previously computed Q8 backgrounds. These comparisons are not independent
full-group calibrations. [Q24_COMPARISON.json](Q24_COMPARISON.json) records their
more limited scope.

The Q24 calculations used `input-generators`; S4 used the default resolution.
The Q24_005 and S4 complete-pipeline elapsed times were 1409.15 s and 1766.01 s,
for these specific inputs and settings. They are not general runtime guarantees.
This supplement is frozen at the 13:59 HKT acceptance cutoff on 2026-10-02.

Verify the saved bytes and independently replay Smith/Hermite arithmetic:

```sh
python3 scripts/verify_complete_results.py \
  --index results/complete_formulas_20261002_supplement/index.json --arithmetic
```

Reproduce a new complete calculation on a compute node:

```sh
python3 scripts/run_complete_example.py \
  --index results/complete_formulas_20261002_supplement/index.json \
  --case d4_Q24_orbit_005 --output runs/q24_005.json --gap "$AFS_GAP" --audit
```

The wrapper retains the recorded resolution strategy. Add `--dry-run` to inspect
the command or `--resolution default` to explicitly select the default builder.
Expected groups are compared only after the calculation finishes.

[index.json](index.json) records original and exported hashes. Export removes
only the machine-local top-level `source_snapshot` field; all scientific fields
are retained. [ACCEPTANCE.json](ACCEPTANCE.json) records the successful pipeline
receipt hashes and recorded coherence scope. It does not replace replay of the
integer certificates or provide an independent physical target.
