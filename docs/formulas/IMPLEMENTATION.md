# Executable interfaces and exact local transport

The [formula guide](../FORMULA_GUIDE.md) is the mathematical entry point.
`insulator.E8State(e_p,n_p,n_p2,nu_p3)` implements the full E8-first
state, its source validation, stacking, complete gauges, inverse, arbitrary
powers, and background transport. Neutral source/twister/gauge corrections
are included in the one shared phase. `insulator.e8.source` evaluates that
complete terminal source.

The lower-level `insulator.api` interface supplies the calibrated CI and
charge blocks used inside the full state. The API mapping is:

| Operation | Python API | Specification |
| --- | --- | --- |
| Charge-to-phase differential representative | `d2`, `charge_source` | [Charge source](OPERATIONS.md#charge-source-twister-and-gauge) |
| CI-to-charge differential representative | `d3`, `integer_obstruction` | Dimensional obstruction equations |
| Completed CI-to-phase secondary representative | `d4`, `source` | Dimensional hatted source equations |
| Integer charge stacking correction | `integer_product` | Dimensional integer product equations |
| Complete stacking twister | `product` | Dimensional hatted product equations |
| Joint sheet/charge gauge | `gauge` | Dimensional source-cylinder constructions |
| Shorter charge gauge at fixed sheet | `charge_gauge` | [Charge gauge](OPERATIONS.md#charge-source-twister-and-gauge) |
| Extension lift or section transport | `background_change` | `06_equivalence.tex`, dimensions 3 and 4; [2+1D endpoint derivation](TWO_DIMENSIONAL.md) |
| Lower exchange homotopy | `lower_exchange` | `06_equivalence.tex`, lower-comm3 and lower-comm4 |
| Canonical 3+1D associator | `associator_3p1` | Parameter tetrahedron integration |
| Complete inverse and arbitrary powers | `State.inverse`, `State.power` | Complete lower product and phase twister |
| Integral Cartan correction and ordered cubic polarization | `integral_cartan`, `cubic_polarizer` | [Operations](OPERATIONS.md) and [4+1D](FOUR_DIMENSIONAL.md) |

The shorter charge gauge and joint cylinder gauge are distinct representatives;
they must not be assumed equal pointwise. Both satisfy their complete source
transport identities. Every recorded root relation must retain the phase from
the gauge actually used.

`Cochain(N, p, values, sign)` is a degree-p exact local cochain on an ordered
N-simplex. `values` maps increasing vertex tuples to integers or `Fraction`;
omitted faces have value zero. `sign` assigns one character bit to each vertex.
The independent signs are `s1` for sheets/phases, `rho1` for charge, and
`rho1+s1` for the extension. `Symmetry` takes the **unshifted** extension lift.

The local evaluator returns cochain representatives, not a cohomology verdict.
The global solver must form the permitted quotient, include incoming images,
complete actual roots, and extract all root-power relations.

## Persistent JSONL worker

Run `python scripts/formula_worker.py`. Each input line is one JSON object and
produces one response line. The process survives a malformed request. It does
not require a finite multiplication table or another repository checkout.

Required fields for a local evaluation are `op`, `dimension` (2, 3, or 4) and
`simplex_dimension`. Vertex arrays `s` and `rho` default to zero. Cochain fields
are sparse dictionaries with comma-separated face indices or dense arrays in
lexicographic face order. Scalars are integers or rational strings; floats are
rejected. Omitted cochain fields are zero.

```json
{"op":"d2","dimension":2,"simplex_dimension":4,"charge":{"0,1,2":"1","0,1,4":"1","0,3,4":"1","1,2,3":"1","2,3,4":"1"},"return":"top"}
```

The background field is `omega`; lower inputs are `sheet` and `charge`. A product
adds `sheet_prime` and `charge_prime`. A gauge adds `sheet_parameter` (dimensions
3 and 4 only) and `charge_parameter`. Background transport uses
`background_parameter` and `op:background_lift` or `op:background_section`.
`charge_degree` permits incoming charge operations below the spatial dimension.

The default response is `{id, ok, result}` or `{id, ok:false, error}`. Product and
gauge results have `sheet`, `charge` and `phase` components. Set
`output_component:"phase"` to select one, and `return:"top"` to obtain a single
rational string when output degree equals simplex dimension.
`response_format:"gap"` emits a valid GAP record on one line. `op:"batch"` takes
a `requests` array; `op:"ping"` returns protocol and convention metadata.
Identical local requests share a bounded 4,096-entry LRU cache, independent of
request ID and output transport. `op:"cache_info"` reports hits and misses;
`op:"cache_clear"` clears cached evaluations.

`validate:false` skips lower-state closure/completion validation for evaluation
on truncated simplices. Exact scalar, sign, and symmetry checks still run.
It does not assert that arbitrary supplied lower data define a valid state.

## Verification

Run `python -m unittest discover -s tests -p 'test_formulas*.py' -v`.

The tests evaluate source closure, full stacking and gauge identities, background
transport, inverses, independent coefficient actions, negative integer carries,
incoming charge images and complete C2 root powers. Nine exact regression
vectors were generated with the untouched source archive's public API and are
stored in `reference_vectors.json`. Universal Boolean-polynomial certificates
verify all coefficients of the 814-term Cartan and 3,117-term charge-conjugation
tables, including normalized degeneracies; they do not use random fitting.
