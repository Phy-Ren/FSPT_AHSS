# Batch performance and evidence size

Calculations ran directly on idle compute nodes through the reused cluster3
SSH connection, from immutable source snapshots. Python was 3.13.12 and SymPy
1.14.0. Node selection used current load and available memory.

| Complete workload | Node | Parallel workers | Measured time |
|---|---|---:|---:|
| 23 new cyclic inputs, including physical eta-kernel comparison | n08 | 8 | 150.817 s execution interval |
| C64, longest cyclic case | n08 | 1 | 150.472 s |
| Four translation ranks, including certificate replay | n09 | 1 | 7.039 s campaign interval |
| Sum of four translation case times | n09 | 1 | 6.969 s |
| Rank-four translations, including certificate replay | n09 | 1 | 6.746 s |

These are complete-run measurements, not extrapolated universal speedups.
The translation tests additionally ran six checks in 19.372 s on n09.

The cyclic source, complete roots, gauges and source evaluations are retained.
Deterministic gzip reduces the full witness JSON from **189,833,767 bytes** to
**3,234,519 bytes**. Compression is lossless, independently round-trip tested,
and changes neither the mathematical calculation nor the retained evidence.
Acceptance hashes the actual compressed artifact. Existing uncompressed
campaigns remain readable.

The translation implementation uses a complete finite classifying space.
For rank four its normalized cell counts are `(1,15,50,60,24,0,0)`.
Unimodular lattice decompositions, cup products and gauge reductions operate
on these cells, avoiding an enumeration of elements of the infinite group.

Exact measurements are in [performance.json](performance.json). Source
archives and source-manifest replay are linked from the [batch README](README.md).
