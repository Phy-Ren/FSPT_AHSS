# Koszul versus HAP lattice contraction: bounded charge completion

Date: 2026-10-15 UTC. Four isolated local drivers used immutable insulator G source `c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`. The only mathematical implementation selection was `U1_USE_KOSZUL=true/false`. The false branch is the generic `ResolutionNilpotentGroup` lattice path used by superconducting main's public full runner at commit `0864495b90297d3e1a0747b77aae17980f6d1f3f`. No superconducting formulas were loaded. Production sources and cluster jobs were untouched.

All initial charge completions finished within their 120-second stage bounds, including the full source transfer, selected phase primitive, and the production native completion equations. All runs made zero Python formula-worker calls. They do not include later sheet completion, incoming gauges, root powers, or a final stacking presentation.

| Spin-half case | Lattice path | Native primary CPU s | Charge completion CPU s | Completed roots | Literally even native roots |
|---|---|---:|---:|---:|---:|
| SG141 | Koszul | 4.851 | 60.853 | 5 | 0 |
| SG141 | HAP | 5.427 | 41.902 | 5 | 2 |
| SG229 | Koszul | 2.966 | 74.107 | 6 | 0 |
| SG229 | HAP | 3.830 | 73.837 | 6 | 0 |

SG141's 1.45-fold completion-stage difference is not a demonstrated general contraction improvement. The HAP coordinate basis has two literally even kernel generators, whose certified sources vanish and finish immediately. The first nonzero primitive costs 25.444 CPU s with HAP versus 26.054 with Koszul. SG229 has six odd generators in both bases and essentially identical total completion time. No resolution switch is recommended from this evidence.

The independent `audit_results.py` checks the saved exact integer charge equations and both the selected and fully transferred phase primitive equations. It also computes the initial surviving charge subgroup from `diag(HQ.orders) * inverse(K)` by integer Smith normal form. Both resolution choices give `Z + Z2^3`: source-map kernel index 4 for SG141, 8 for SG229. Native matrices and generator coordinates differ, so these are independent equation checks and matching abstract charge kernels, not a claim that individual coordinates are literally identical or that final stacking groups have been compared.

The selected-function profiles show source evaluation/transfer dominates. `U1SolveNative` takes only milliseconds; `U1Native` accumulates tens of seconds of direct evaluation and contraction work. This supports studying exact half-valued source transfer and lazy normalized degree-three cup-one evaluation while preserving the full integral comparison homotopy. It does not justify a cohomology-only primitive or dropping gauge witnesses.

Each run stores its driver, logs, exact lower cohomology/kernel matrices, every completed root witness, and timing metadata. `summary.json` pins all GAP source and input hashes. `audit.json` records independent validation. Reproduction uses `run_controls.py` with fresh case directories, then `audit_results.py`. Four controls ran concurrently locally; no cross-host or whole-campaign speedup is claimed.
