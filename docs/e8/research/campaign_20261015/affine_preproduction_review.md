# 3+1D affine classification review

Review date: 2026-10-15 UTC. Runtime frozen at `80d565de744bbd5ef6ac4cca3530511f549547f4`. This was a read-only review of the classifier; no runtime code was changed by this review.

**Decision:** no mathematical blocker was found for the 460 verified space-group inputs. This is a bounded code and input review, not a claim that the 460 classifications have run or that the computed model has been identified with the complete physical spectrum.

## Exact evidence

Run `python3 benchmarks/audit_affine_sheet_kernels.py --check` from the repository root. The [saved certificate](../../../../results/spacegroup_campaign_20261015/affine_kernel_review.json) pins every reviewed runtime file, the audit script, all 460 input files, and the geometry export. Its export SHA256 is `7ed9423b1c76690bcc8bdabcf359116762b76d8c19e81aab427c22d3fc1fbbb7`.

The audit uses GAP's actual integer kernel and Smith routines, with an independent exhaustive membership predicate. For raw sheets `Z2 + Z + Z`, it tests both an obstruction that removes the torsion direction and one that preserves it. Each case then passes through the terminal quotient `Z6 / <3> = Z3`; 343 vectors per case are checked. Transporting the original relation `(2,0,0)` through both kernels yields respectively `Z²` and `Z2 + Z²`. Empty source and target cases are also checked. These are lattice controls, not substitutes for completed cochain tests.

All 460 generated inputs reproduce the exported affine generators, finite-presentation generators and relators, and primitive translation words and matrices. Point-matrix sets agree; generated catalogues intentionally put the identity first. The earlier [neutral-sector audit](../../../../results/spacegroup_campaign_20261015/e8_reference_audit.json) independently checks every affine relator and translation word and finds all 230 neutral H1 groups equal to the separately sourced neutral reference. That comparison is not a full electronic classification benchmark.

## Reviewed mechanisms

- `gap/classification.g`, `U1MapKernel` and `U1AffineSheetLattice`: both obstruction kernels are integral preimage lattices. The terminal obstruction is projected modulo the pure-charge source image. Surviving roots are reconstructed with the full nonlinear stacking law, charge adjustments and phase primitives; completed-state checks are retained. Original sheet torsion relations are transported using the inverse combined lattice. Free directions are not assigned finite-order relations. Additivity of the terminal obstruction is needed only in the quotient by charge adjustments, not for an arbitrary fixed choice of seed completion.
- `gap/context.g`, `U1SpaceGroupFilling`: the translation basis is checked to generate the entire holonomy kernel, oriented by its determinant, and used in the alternating bar 3-cycle. Both charge and completed CI roots contribute. Every final relation must have zero filling. The total image and charge-only image are distinct outputs.
- `U1AffineContext` and `U1SiblingContext`: the resolution is for the full infinite affine group. Only background characters/cocycles are inflated from holonomy. Reuse requires the same geometry and coefficient characters; omega-dependent state/source evaluation remains attached to the new context.
- The final cache-only follow-up was inspected: exact worker requests include all background and state fields in their keys; geometry caches remain context-local. Consecutive products used for a face edge equal `v_i^-1 v_j` even in a nonabelian group. Preserving the literal zero under a coboundary avoids an unnecessary formula call without changing the cochain. The independently owned cache regression tests and final campaign smoke tests provide the execution evidence for this optimization.
- `insulator/e8_spacegroup.py`, `spacegroup_h1`: exact affine word evaluation, a saturated signed-integer cocycle kernel, the principal quotient, and root witnesses are retained. Screw-axis primitive periods are not discarded.
- `insulator/e8_pointgroup.py`, `_extend_classification`: the E8 section and CI sector are combined as actual integer presentations and reduced together. Free summands are counted from presentation rank. The selected neutral section has zero charge, so its filling coordinates are zero.

## Nonblocking interface limits

`spacegroup_h1` trusts the certified-export flags `isomorphism_verified` and `basis_of_full_translation_kernel`. Its local checks prove consistency and independent translation vectors, but do not prove full primitiveness for an arbitrarily edited external presentation. For example, simultaneously doubling a translation word and its claimed matrix cannot be excluded merely by checking their equality. Production inputs are covered by the hash-pinned export and the GAP full-kernel check.

At review time `_extend_classification` rejected `nativeChainIdentitiesVerified=False`, but did not reject a missing field. The fresh runner supplies `True`, and the strict collection step requires it; this is an arbitrary-input API hardening opportunity, not a gap in the accepted campaign inputs.

The extended output retains the filling witness in `ciSector`. A consumer displaying it in the combined E8-first root basis must prepend zeros for the neutral roots using the recorded coordinate blocks. The saved CI vector must not be presented as already using the enlarged basis.

The separately run focused runtime tests remain responsible for complete source/product/gauge identities and paired-spin classification. This review does not claim to duplicate their entire coverage. Runtime/source hashes in the certificate identify the reviewed version; subsequent source changes require checking the certificate again or an explicitly scoped follow-up review.
