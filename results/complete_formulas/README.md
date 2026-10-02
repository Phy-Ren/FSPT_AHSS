# Completed classification and stacking results

This is the current complete-formula result set. Every production calculation
includes classification, stacking and the full incoming gauge quotient. The
[JSON index](index.json) gives exact result hashes, inputs, final filtrations and
independent-target status. All 832 retained presentations have passed independent
Smith/Hermite arithmetic and GAP unimodular-certificate verification. The
[release validation receipt](VALIDATION.json) additionally records 17 exact core
formula recompilations and six fresh end-to-end calculations.

| Collection | Records | Table |
|---|---:|---|
| 230 space groups, both crystalline spin conventions | 460 | [Space groups](space_groups.csv) |
| 32 finite point groups, both conventions | 64 | [Point groups](point_groups.csv) |
| Finite internal symmetries in 3+1D | 16 | [3D finite inputs](finite_3d.csv) |
| Finite internal symmetries in 4+1D | 229 | [All exact 4D inputs](finite_4d_exact.csv) |
| Canonical 4+1D physical catalog, contained in the preceding row | 202 | [Typed physical cases](finite_4d_canonical_202.csv) |
| Separate completed calibration controls | 63 | [Controls](supplemental_controls.csv) |

The first four rows total **769 production records**. The 229 exact 4D inputs
comprise the 202 canonical cases and 27 historical coordinate representatives.
The canonical catalog contains 197 automorphism-orbit cases plus five cyclic or
dihedral supplements. The historical 53-row table and the canonical table share
26 results; they are not additive collections.

The **63 separate controls** are 42 Bott cases across dimensions 2–4, ten 3+1D
cases with bosonic quotient `Q16`, two 3+1D `Pin+ x C4/C8` cases, seven fMPS/exact
section-change endpoint calculations, and two zero-chiral unitary controls.
They are additional retained calculations and may repeat physical symmetries
already represented elsewhere. No count here asserts that all records describe
inequivalent physical backgrounds.

`Zk` denotes `Z/k`; `Z` is infinite cyclic and `0` is the trivial group. The four
layer columns are the final associated-graded quotients after incoming gauge
identifications. Their direct product need not equal the full stacking group.
For zero-chiral controls, the table reports the explicitly labeled abstract
chiral completion; the saved presentation describes the finite zero-chiral fiber.

## Selected internal-symmetry results

These examples illustrate the full extension computation. The input catalogs
fix `omega2` and `s1` exactly; a group name alone does not specify a fermionic
symmetry.

| Dimension | Symmetry/background | Full group | Record |
|---|---|---|---|
| 3+1D | `C2`, nontrivial extension and antiunitary grading | `Z16` | `d3_C2_w1_s1` |
| 4+1D | `Gb=Q8`, split unitary | `Z2^2` | `d4_Q8_w0_s0` |
| 4+1D | `Gf=Q8`, `Gb=C2 x C2`, unitary | `Z2^4` | canonical `C2xC2_orbit_003` |
| 4+1D | `Gf=Q16`, `Gb=D8`, unitary | `Z2^4 x Z4` | `d4_D8_orbit_005` |
| 4+1D | `Gb=Q16`, canonical background 005 | `Z4` | `d4_Q16_orbit_005` |
| 4+1D | `Gb=C64`, split unitary | `Z16 x Z64` | `d4_C64_w0_s0` |
| 4+1D | `Gb=C64`, nonsplit unitary, lift `R^64=F` | `Z32 x Z512` | `d4_C64_w1_s0` |
| 4+1D | `Pin+ x C4` | `Z4^2` | canonical `C4xC2_orbit_007` |
| 4+1D | `Pin+ x C8` | `Z4 x Z8` | canonical `C8xC2_orbit_007` |
| 3+1D | `Pin+ x C4` and `Pin+ x C8` | `Z2 x Z4 x Z16` each | control table |

Here `D8` has order 8 and `Q16` has order 16. `Gf=Q16` and `Gb=Q16` are different
inputs. In the Pin rows, the antiunitary generator satisfies `T^2=F` and commutes
with the unitary cyclic factor.

## Independent calibration

The 202 canonical cases have 49 independent full-group targets: 26 published
full-group targets, nine Bott-derived targets, and 14 targets independently
derived from primary results. All 49 agree. The status column distinguishes these
categories. A linked primary paper is the foundation of a derived target; it need
not print that target in this repository's notation. The remaining 153 cases
include 151 without a full-group target and two with only an eta-invariant
exponent lower bound.

All 524 crystalline final groups and layer quotients agree with the earlier
archived computation. This is a regression check. The current crystalline audit
does not attach an independent full-group target to these rows; it must not be
read as an independent physical proof for every point or space group.

Only completed accepted calculations appear in this inventory. The formula
implementation's agreement with its definitions, local coherence, integer
quotient arithmetic, and independent physical targets are separate validation
questions. See the [reproduction guide](../../PUBLIC_RELEASE.md) for exact checks
and [formula scope](../../formulas/README.md) for lower-dimensional endpoints.
