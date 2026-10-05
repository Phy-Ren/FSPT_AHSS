# 1+1D finite internal symmetries

6 retained named calculations. Group arrays in the CSV are invariant factors.

| Input | Dimension | Gb | Grading / crystalline spin | omega2 representative | p+ip | Majorana | CF | Bosonic | Stacking group |
|---|---|---|---|---|---|---|---|---|---|
| [d1_C1_trivial](../inputs/d1_C1_trivial.json) | 1+1D | C1 | [] | 0 | 0 | Z2 | 0 | 0 | Z2 |
| [d1_C2_w0_s0](../inputs/d1_C2_w0_s0.json) | 1+1D | C2 | [0] | 0 | 0 | Z2 | Z2 | 0 | Z2^2 |
| [d1_C2_w0_s1](../inputs/d1_C2_w0_s1.json) | 1+1D | C2 | [1] | 0 | 0 | Z2 | Z2 | Z2 | Z8 |
| [d1_C2_w1_s0](../inputs/d1_C2_w1_s0.json) | 1+1D | C2 | [0] | nonzero ([exact input](../inputs/d1_C2_w1_s0.json)) | 0 | 0 | 0 | 0 | 0 |
| [d1_C2_w1_s1](../inputs/d1_C2_w1_s1.json) | 1+1D | C2 | [1] | nonzero ([exact input](../inputs/d1_C2_w1_s1.json)) | 0 | 0 | Z2 | 0 | Z2 |
| [d1_C3_exact_extension_section](../inputs/d1_C3_exact_extension_section.json) | 1+1D | C3 | [0] | nonzero ([exact input](../inputs/d1_C3_exact_extension_section.json)) | 0 | Z2 | 0 | 0 | Z2 |

The four layer columns are final filtration quotients; their direct product need not be the stacking group.
Finite input links fix the full multiplication table, grading and parity-extension cocycle. A nonzero representative of omega is not by itself a claim that its cohomology class is nontrivial.
For the two zero-chiral controls, the stacking column is the saved zero-chiral fiber; the catalog separately records its abstract chiral completion.
