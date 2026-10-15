# Exact proofs and calibration evidence

These reports and scripts record the 2026-10-15 closure work. The original
review directory is `/home/xingyu/AllFSPT_reviews/e8_closure_20261015` and its
cluster3 mirror is `/home/user/xyren/AllFSPT_insulator/reviews/e8_closure_20261015`.
Full downloaded papers remain outside Git. Original artifact hashes and the
one internal-link adaptation are recorded in `review_import.json`.

## 2+1D

- [Uniform response and free-quotient proof](general_groups/uniform_2p1.md).
- [Physical coefficient dictionary](physical/coefficient_2p1.md).

## 3+1D

- [Infinite translation, mirror, glide, screw, and magnetic examples](general_groups/examples_3p1.md).
- [Interacting mirror calibration](physical/mirror_3p1.md).

## 4+1D

- [Free translation decorations and explicit completions](general_groups/examples_4p1.md).
- [Lens/APS dictionary and cyclic electronic controls](physical/eta_dictionary.md).
- [Intrinsic Spin-c response lattice and remaining operations](parity_bridge/intrinsic_response.md).

## General proofs and comparison maps

- [Finite-holonomy cohomology and constructive completion](general_groups/general_groups.md).
- [Read-only review of the new E8 implementation](general_groups/runtime_review.md).
- [U1f/parity comparison, source/product/gauge and limitations](parity_bridge/parity_bridge.md).
- [Comparison certificates and source provenance](parity_bridge/README.md).

The exact audit scripts accompany each report. Some preserve the absolute
cache paths used in the original review; scripts comparing the separate
public parity checkout accept explicit reference arguments where indicated.
They are historical-reference audits, not production dependencies. The
self-contained branch tests are under `tests/`.

No result table combines dimensions, physical spins, or response sectors.
These are theorem/example audits and physical controls, not a new global
classification campaign. The status of the entire construction is stated
in [the closure ledger](../README.md).
