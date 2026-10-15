# Insulator branch conventions

This branch implements U(1)^f insulators only. Keep superconducting formula engines, results, CLI options, and documentation on the main branch. Generic exact cochain and group-resolution code may be copied here with explicit provenance, without runtime dependencies on another checkout.

Use English for reasoning, code, comments, derivations, documentation, reports, and agent collaboration. Use Chinese only in direct conversation with the user.

The authoritative formula input is U1f_AHSS_Consolidated_v0_7_complete.zip, SHA256 a1410f854828f012dc9be56cfd62dc0eb4a195779c09eed273e6a70f2ca97a4a. Adopt its calibrated sheet-linear convention, cubic coefficient 1/6 and additional product coefficient epsilon=0. Preserve source, product and gauge coordinates together. Declare independent s1, rho1 and rho1+s1 coefficient actions.

Keep 2+1D, 3+1D and 4+1D distinct. In each dimensional reference put obstruction equations before stacking equations. Use exact integers and rationals. Retain complete phase completions, integer gauge corrections, incoming identifications, arbitrary root orders and free summands. Only an obstruction class surviving permitted lower adjustments rejects a state.

The default classifier scope remains CI-generated, localized-charge and group-cohomological phase sector. The separate E8State API implements the reviewed neutral closed-sheet addition locally. Do not claim that the global classifier includes E8, intrinsic higher-response or universal terminal parity comparison sectors. Do not install missing operations as zero.

The reviewed E8 supplement is E8_AHSS_v0_9_complete.zip, SHA256 da3ad9368390e8d075f27e0039e8486f14890fefb3ccbf0aea4d85a5ba0685cd. Extended states use (e_p,n_p,n_{p+2},nu_{p+3}), E8 first, p=spatial_dimension-2. The target includes infinite space groups with finite holonomy and finite-rank translations; continuous groups are exploratory, not a completion requirement. Preserve explicit physical-spectrum and intrinsic-row boundaries.

Current user priority: finish the original four-data theory first, including complete d2/d3/d4, stacking twisters, and gauge/incoming relations. Do not replace explicit formulas with an abstract-group-only shortcut. Intrinsic 4+1D r0 work is deferred; save its existing notes separately and do not introduce its possible d5/d6 into the four-data completion requirements or runtime.

Active comparisons must first separate spacetime dimensions into independent directories and index pages, then separate physical spins and response sectors. Do not combine 2+1D and 3+1D result links into a shared spin table. Spinless and spin-half results require separate table files, not alternating rows or adjacent spin columns. In 2+1D, keep n0=0 and all allowed n0 in separate files, and keep e0=0 separate from any future e0-inclusive results. Render matching classifications with bold ✓ and differing classifications with bold ×; keep unverified cases distinct. Full E8-inclusive tables require separate global implementation and review; the reviewed local E8 API alone does not supply them. Preserve existing raw calculation inputs, outputs, and reference fixtures as provenance; they are not active presentation tables.

Reuse persistent SSH masters for cuhk-cluster3 and its compute nodes. The user explicitly confirmed on 2026-10-13 that current cluster practice is direct execution on idle compute nodes; a head/PBS allocation is not required. Check load first, limit concurrency and memory, and run classification campaigns on compute nodes. Preserve immutable run inputs, hashes, logs and witnesses. Do not overwrite accepted or running results.

Make reviewable commits. Never stage another agent's unfinished work without coordination. Tests must substantiate mathematical identities or end-to-end classification behavior.
