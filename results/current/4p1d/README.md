# 4+1D insulator examples

This collection contains **57 configured symmetry inputs** and **110 response-sector entries**. Internal groups carry no crystalline spin labels; pure translations contain no rotations and have no separate spin lifts. Coprime product presentations can describe a cyclic group already represented by a separate control input.

- [37 commuting cyclic inputs: zero intrinsic response](internal_cyclic/intrinsic_zero.md).
- [37 commuting cyclic inputs: all intrinsic responses](internal_cyclic/intrinsic_all.md).
- [12 commuting abelian product inputs: zero intrinsic response](internal_abelian/intrinsic_zero.md).
- [12 commuting abelian product inputs: all intrinsic responses](internal_abelian/intrinsic_all.md).
- [4 translation ranks: zero intrinsic response](translations/intrinsic_zero.md).
- [4 translation ranks: all intrinsic responses](translations/intrinsic_all.md).
- [Unitary charge conjugation](charge_conjugation.md): the intrinsic row is symmetry-forbidden.
- [AI/AII: zero intrinsic response](time_reversal_intrinsic_zero.md).

Each computation retains the full `(e2,n2,n4,nu5)` products, joint gauges, incoming identifications and root relations. Cyclic cases compare the entire relation lattice with independent eta characters. Abelian products retain mixed charge and phase classes, incoming gauge images and commutator witnesses. Translation cases use a complete finite simplicial torus and an explicit integral coordinate change that resolves their stacking extension.

The all-intrinsic tables use the symmetry-independent I,J section for the specified direct products. This is separate from a general opened-intrinsic implementation. AI/AII full groups and embedded response lattices remain distinct from their computed zero-intrinsic kernels.

Reference answers appear in separate columns with their exact symmetry and response scope. An additive bordism match for an abelian product is distinct from the labelled character-kernel certificate available for the cyclic examples.

## Calculation and calibration

- [Cyclic formulas and physical calibration](../../../docs/formulas/FOUR_DIMENSIONAL_CYCLIC_EXAMPLES.md).
- [Abelian product calculation](../../../docs/4p1d/calibration/ABELIAN_PRODUCTS.md).
- [Translation calculation and integer stacking coordinates](../../../docs/4p1d/calibration/TRANSLATIONS.md).
- [Signed C2 calculation](../../../docs/4p1d/calibration/SIGNED_C2.md).
- [Cyclic and signed bordism sources](../../../docs/4p1d/calibration/BORDISM_TARGETS.md).
- [Additional finite-group and translation benchmarks](../../../docs/4p1d/calibration/BATCH2_TARGETS.md).

## Accepted calculation lineage

The following pinned collections supply the current rows. Each new batch extends its accepted parents; unfinished runs are excluded.

- [results/four_dimensional_20261016/accepted.json](../../four_dimensional_20261016/accepted.json): 18 accepted inputs.
- [results/four_dimensional_batch2_20261016/accepted.json](../../four_dimensional_batch2_20261016/accepted.json): 27 accepted inputs.
- [results/four_dimensional_abelian_20261016/accepted.json](../../four_dimensional_abelian_20261016/accepted.json): 12 accepted inputs.

[Catalogue](../README.md) · [Provenance and scope](../PROVENANCE.md).
