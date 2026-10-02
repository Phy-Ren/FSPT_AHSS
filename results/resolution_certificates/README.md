# Integral resolution certificates

These two saved certificates contain the full finite group multiplication table,
integer boundaries, contracting homotopy, and the explicit transport from the
factor resolution group to the original model group. All indices are one-based.
A chain term is `[integer_coefficient, basis_index, group_element_index]`.
Boundaries use left multiplication by the input group element; contractions are
recorded separately on every translated cell and are not assumed equivariant.

Run the independent integer replay on a compute node:

```sh
python3 scripts/check_resolution_certificate.py --output runs/resolution_replay.json
```

The checker requires only Python's standard library. It uses no GAP, supplied
formula tables, expected physical group, or private file. It verifies group
associativity, the transport multiplication table, augmentation, `d*d=0` through
degree seven and `d*h+h*d=1` through degree six on every translated basis cell.
The degree-zero identity includes the explicit augmentation contraction.

| Family | Resolution ranks in degrees 0–7 | d² cells | Contraction cells | Recorded construction CPU time |
|---|---|---:|---:|---:|
| D8 × C2 | 1, 3, 6, 11, 18, 27, 39, 54 | 2480 | 1680 | 0.405 s |
| Q8 × C2 | 1, 3, 6, 9, 11, 13, 16, 19 | 1184 | 944 | 0.128 s |

Each replay also checks 256 transport products and 4096 associativity triples.
The recorded GAP 4.13.1 profile took 26.85 s and 22.20 s wall time respectively,
including startup, integral checks, export and independent Python replay.
[PROFILE.json](PROFILE.json) retains the exact timing values and certificate
hashes. These are resolution profiles, not full FSPT timings or new accepted
physical examples. Construction ranks and timings may vary with GAP/HAP versions.

The executable builders are `AFSFullInputGeneratorsResolution` and
`AFSFullDirectProductResolution` in [full_resolution.g](../../gap/full_resolution.g).
The input-generators option is separate from the two factor certificates here.
Successful resolution identities establish valid integral chain arithmetic;
they do not establish a guessed physical obstruction or stacking law.
