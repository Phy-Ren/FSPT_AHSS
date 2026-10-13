# Insulator branch conventions

This branch implements U(1)^f insulators only. Keep superconducting formula engines, results, CLI options, and documentation on the main branch. Generic exact cochain and group-resolution code may be copied here with explicit provenance, without runtime dependencies on another checkout.

Use English for reasoning, code, comments, derivations, documentation, reports, and agent collaboration. Use Chinese only in direct conversation with the user.

The authoritative formula input is U1f_AHSS_Consolidated_v0_7_complete.zip, SHA256 a1410f854828f012dc9be56cfd62dc0eb4a195779c09eed273e6a70f2ca97a4a. Adopt its calibrated sheet-linear convention, cubic coefficient 1/6 and additional product coefficient epsilon=0. Preserve source, product and gauge coordinates together. Declare independent s1, rho1 and rho1+s1 coefficient actions.

Keep 2+1D, 3+1D and 4+1D distinct. In each dimensional reference put obstruction equations before stacking equations. Use exact integers and rationals. Retain complete phase completions, integer gauge corrections, incoming identifications, arbitrary root orders and free summands. Only an obstruction class surviving permitted lower adjustments rejects a state.

State scope: CI-generated, localized-charge and group-cohomological phase sector. Do not claim unimplemented neutral E8, intrinsic higher-response or universal terminal parity comparison sectors. Do not install missing operations as zero.

Reuse persistent SSH masters for cuhk-cluster3 and its compute nodes. The user explicitly confirmed on 2026-10-13 that current cluster practice is direct execution on idle compute nodes; a head/PBS allocation is not required. Check load first, limit concurrency and memory, and run classification campaigns on compute nodes. Preserve immutable run inputs, hashes, logs and witnesses. Do not overwrite accepted or running results.

Make reviewable commits. Never stage another agent's unfinished work without coordination. Tests must substantiate mathematical identities or end-to-end classification behavior.
