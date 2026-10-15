# Independent review of the ordered-edge U1Cup candidate

The isolated patch in `../cup_candidate/change.patch` preserves the cochain operation. No runtime or campaign file was changed by this review. This is a review of that exact patch, not a deployment approval or a full new campaign validation.

For one-based vertex indices, put `v_k=x_1 ... x_(k-1)`. For `a<b`, adjacent group cancellation gives

`v_a^-1 v_b = x_a ... x_(b-1)`.

The candidate constructs this product by starting at `x_a` and multiplying on the right by each subsequent edge, in its original order. No commutativity is assumed. It also constructs `vs[1]=1` and `vs[k]=edges[1][k]`, exactly the original prefixes. Therefore both local coefficient actions are evaluated on the same original bases. Integer term signs, the binary branch, final mod-two reduction, arity checking, zero pruning and memoization are unchanged.

The edge array supplies only strictly increasing pairs. The independent structural scan of all 81 pinned cup tables finds 252 terms and 1829 edge accesses; every pair is strictly increasing and in range. Thus the patch does not encounter a missing diagonal or reversed pair on the supported table domain.

For total degree zero, GAP's `[1..0]` and `[2..1]` are empty. Both construction loops are empty, the prefix list remains `[1]`, and `c0_0_0` calls both factors on empty argument lists with identity coefficient actions. For exactly one degree-zero factor and positive total degree, that factor still receives its original singleton-vertex coefficient action, including the full terminal prefix when it is the right factor.

`check_cut_domain.py` reproduces the structural scan and the GAP empty-range assertion and records exact candidate/cut/patch hashes in `result.json`. The already supplied nonabelian numerical checks and SG195 complete-run comparison were inspected as supporting evidence, not rerun. No correctness issue was found in this bounded review.
