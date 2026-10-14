# Which literature results are admissible comparisons?

This project studies charge-conserving **interacting invertible electronic
phases** with `exp(i pi Q)=(-1)^F`. Intrinsic topological order is outside
this classification problem. A phase that has a band representative is
still part of the interacting classification; what changes is the allowed
equivalence, including strongly interacting paths, and the possibility of
additional phases with no band representative.

Free-fermion K-theory, symmetry indicators, band representations and the
ten-fold-way free tables are not substitutes for this interacting group.
The label "class A" in a bordism paper specifies the charge-conserving
symmetry type; it does not mean the calculation assumes free fermions.
Likewise connective K-homology may be a mathematical tool for a low-degree
bordism computation without being the physical free-band classification.

## Source types kept separate

| Evidence | How it is used |
|---|---|
| Interacting bordism / invertible field theory | An independent mathematical method, with its symmetry structure and physical ansatz recorded. Read the proof as well as the table. |
| Interacting lattice / real-space construction | Compare the actual allowed decorations, adjoining operations and completed root relations. |
| Complete interacting response / anomaly indicators | Compare under explicit response restrictions; seek a map from program roots to those indicators. |
| Interacting reduction of band-generated phases | A diagnostic for the image of band phases, not a completeness benchmark. |
| Many-body atomic / fragile invariants | A diagnostic for the stated atomic equivalence or response; not automatically a stable invertible-phase classification. |
| Free-band classification | Excluded from the main comparison tables. |

Each table file contains exactly one physical spin convention and one
catalog family. Spinless and spin-half results never share a table. In
2+1D, `n0=0` and all allowed `n0` have separate files, and all current
tables have `e0=0`. E8-inclusive tables are deferred until that decoration
is implemented and reviewed. Distinct papers have distinct columns;
changed preprint and journal versions have distinct columns. A charge or
phase filtration layer has its own column and is not presented as a full
stacking group. Missing source coverage is explicit.
There is no majority vote over columns and no author-level reliability
score. Shared constructions or revisions following another paper's results
are recorded as limits on independence.

The tables are generated from frozen calculation outputs and separate
reference fixtures. Reference data never enter the classifier. Abstract
agreement is a check; physical calibration additionally requires matching
the symmetry extension, crystalline action, response normalization,
adjoining equivalence, and individual generators and relations.

## Newly checked sources and exclusions

Arun Debray, [arXiv:2102.02941v3](https://arxiv.org/abs/2102.02941v3),
first posted 2021-02-05, revised 2026-02-03, computes interacting phase
homology under the generalized-homology ansatz. Only its class-A columns
are transcribed. The pinned source covers all 20 planar cases and 40 of
the 64 spatial-three-dimensional cases. It is a distinct mathematical
method, but v3 explicitly discusses revisions following comparison with
Zhang-Ning-Qi-Gu (2025), so final table agreement is not blind independence.
The source's own proof arithmetic is subject to the same scrutiny as any
other reference.

Ning, Mao, Li, and Wang,
[PRB 104, 075111 (2021), arXiv:2105.02682v1](https://arxiv.org/abs/2105.02682v1),
derive interacting mirror classifications and complete anomaly indicators.
The exact symmetry and detector dictionary support the two `Cs` source
cells. Their derivation builds on earlier mirror-plane constructions;
this connection is recorded rather than counted as blind replication.

Manjunath, Calvera, and Barkeshli,
[PRB 109, 035168 (2024)](https://doi.org/10.1103/PhysRevB.109.035168),
give the interacting response classification for the five
orientation-preserving wallpaper groups. The same paper also contains
free classifications and a free-to-interacting map. The new main tables
use **only the interacting column** and response-defined restrictions.

Liu, Vishwanath, and Khalaf,
[PRX 9, 031003 (2019), Sec.VI B](https://doi.org/10.1103/PhysRevX.9.031003),
analyze interacting equivalences among band-generated phases. The cyclic
center relations are useful, but the paper does not claim that the cited
calculation excludes all interaction-only roots. Its results have been
moved to the separate diagnostic table and are absent from the main
complete-classification comparison.

Herzog-Arbeitman, Bernevig, and Song,
[Interacting Topological Quantum Chemistry in 2D with Many-Body Real Space Invariants](https://arxiv.org/abs/2212.00030),
was checked as a further lead. Its local invariants classify many-body
atomic states and constrain fragile topology; it also constructs global
many-body invariants. Its atomic equivalence and diagnostic coverage must
not be silently replaced by our whole invertible-phase problem. No cells
from that paper have been promoted to complete classification benchmarks
in this review.

Soldini, Aksoy, and Neupert,
[PR Research 6, 033205 (2024), arXiv:2404.11650v2](https://arxiv.org/abs/2404.11650v2),
do study fully interacting wallpaper insulators. However their symmetry
includes **additional spinful time reversal**, with square fermion parity.
The present crystallographic campaigns do not include that extra internal
symmetry. Their tables are therefore not direct comparisons for our
current rows, even where a wallpaper group has the same name.

The formal correction search is recorded separately in
[corrections and versions](corrections_and_versions.md). A formal erratum,
a preprint revision, a source-internal inconsistency and a disagreement
with this program are four different facts and retain different labels.
