# Exact simplex-kernel performance review

Frozen baseline: commit `80d565de744bbd5ef6ac4cca3530511f549547f4`. The formula, differential, gauge, and stacking conventions are unchanged. The candidate changes only `insulator/_engine/simplex.py`; the focused regression is `tests/test_simplex_exact_kernel.py`.

## Measurements

All measurements here are local, using Python 3.12.3, GAP 4.12.1, and a Ryzen 9950X3D. They are not cluster throughput measurements.

A bounded 90-second cProfile run of SG14 spin-half captured 1,473 cache-miss requests. Its 733 nonzero-sheet source calls accounted for 78.9 of 80.0 profiled CPU seconds. The repeated parent cochain evaluation spent 49.1 seconds in higher cup products, generating about 31.5 million Fraction arithmetic-wrapper calls and 46.6 million gcd calls.

Uncached replay of the same complete requests, in fresh processes:

| Kernel | CPU seconds | Baseline / candidate |
| --- | ---: | ---: |
| Frozen baseline | 22.2868 | 1.00 |
| Exact integer scalar representation | 10.0524 | 2.22 |
| Plus cup geometry and literal-zero factors | 5.7918 | 3.85 |
| Final: plus boundary geometry and exact-type check | 3.5542 | 6.27 |

Every replay response is identical. Complete-response SHA256: `8c51566473e69c1f8ebc71179467ac96a89c5b46b1c35a46b8957781f13bd3ea`.

The complete SG14 spin-half classification takes 345.367 seconds with the baseline and 70.919 seconds with the final candidate (4.87 times faster). Input and all native scientific fields agree exactly, including 19,418 worker calls, cache counts, complete roots, root relations, obstructions, gauge parameters, phase completions, and primitive-cell fillings. Only `resolutionBuildTimings` is excluded from this comparison. See `sg14_full_equivalence.json` and the two original run directories.

## Exactness argument

1. A Python Fraction with denominator one and its integer numerator are the same element of Q. The conversion retains every nonintegral Fraction. Addition, subtraction, multiplication, exact rational scaling, integer floor, and remainder therefore have identical numeric values, including negative values and carry terms. Wire serialization already converts both representations through Fraction. No value is reduced modulo an assumed period.
2. The cup plan records precisely the ordered face embeddings returned by the existing interval-cut enumeration. Its key is `(simplex dimension, left degree, right degree, cup index)`. It contains no cochain values or coefficient actions. Each signed term still reads the current independent left and right vertex actions. Factor order and cut order are retained; the cup operation is never treated as commutative.
3. Skipping a term requires a numerically zero multiplicand, not an exact cochain or a zero cohomology class. Every omitted summand is literally zero in Q. The output still includes the same full face dictionary.
4. The boundary plan stores only faces and alternating signs. Its first face keeps the original twisted coefficient factor evaluated from the current cochain. The remaining faces have precisely their original alternating signs.

These statements prove equality of the underlying rational cochains before reduction modulo one, and hence equality of every formula built from these operations. Geometry caches cannot mix spins or backgrounds because they contain neither. They are bounded (256 face/boundary plans, 512 cup plans).

Construction now owns a numerically canonical copy of its dictionary instead of retaining caller aliasing; `ret()` consequently also copies. The runtime and tests do not mutate `.v`, and no documented aliasing contract is used. This representation change is explicitly limited to the existing value-based cochain engine.

## Validation

- All 79 tests in the isolated frozen-C candidate pass, including frozen reference vectors, coefficient certificates, source/product/gauge/inverse identities, incoming relations, nonabelian GAP face transport, and the new primitive regression. Log: `full-suite-final.log`.
- Independent direct-face oracle: 1,578 constructor/arithmetic/boundary/cup comparisons, with 183 explicitly noncommuting cup cases, independent vertex actions, negative integers, and nonintegral rational values.
- The production regression independently expands 1,335 boundary/cup results across six simplex sizes and all compatible degrees; it does not reuse the geometry plans.
- All 36 additional source/product/gauge requests across spatial dimensions 2, 3, 4, with independent signs and nonintegral rational extension lifts whose coboundaries are integral, return successful identical responses. No validation error is counted as a successful formula comparison. These use the same partial-simplex `validate=false` operation as the solver transport; arbitrary input sheets in this auxiliary test are not asserted to be completed global states.
- Peer reviewer independently checked 1,533 further boundary/cup cases, including empty faces and cup indices outside the ordinary range. See `independent_peer_review.json`.

## Reproduction

Apply `exact_kernel.patch` to a fresh frozen-C checkout and copy `test_simplex_exact_kernel.py` into its tests directory. The archived baseline was modified only in its worker launch wrapper to dump a profile on SIGTERM and capture each cache-miss request; its mathematical kernels were unchanged. The full runtime manifests are retained in `sg14_baseline/source.json` and `sg14_candidate/source.json`, and the exact launch-wrapper instrumentation is `review_instrumentation.patch`. The complete baseline run enabled request capture; the complete candidate run did not. Capture adds only JSON logging, which does not change any worker response.

Decompress `requests.jsonl.gz`, then run:

```sh
python replay.py BASELINE_ROOT requests.jsonl baseline-replay.json
python replay.py CANDIDATE_ROOT requests.jsonl candidate-replay.json
python check_kernel_equivalence.py BASELINE_ROOT CANDIDATE_ROOT kernel-review.json
```

Repeat the replay with `signed-rational-requests.jsonl.gz` to check the 36 rational-background requests. Compare the `results` arrays exactly; elapsed times are diagnostic only.

From either checkout, the complete case is:

```sh
python scripts/classify.py --case spacegroup_014_spin_half --jobs 1 --memory 4g --timeout 420 --gap /usr/bin/gap --output DISTINCT_OUTPUT_DIRECTORY
```

The optimized checkout can run `python -m unittest discover -s tests -v`. Existing cluster D jobs and frozen source C were not changed. A cluster successor pilot is required before assigning cluster speedups or rescheduling jobs; GAP-dominated cases need not benefit substantially.

Run `python check_evidence.py` in this directory to verify all archived bytes, compressed captures, complete response arrays, and full native scientific equality. The source of each captured request is identified by its frozen commit and kernel hashes in `metadata.json`; duplicate source snapshots are omitted.
