# Formula implementation map

The [canonical formula guide](../docs/FORMULA_GUIDE.md) is the mathematical
reference for notation, complete obstruction and stacking equations, and the
explicit finite operations. The [operation registry](FORMULA_REGISTRY.json)
connects its equation labels to source files and compiler targets. This page
provides the runtime dictionary and implementation entry points.

The complete 3+1D and 4+1D engine evaluates every supplied obstruction and stacking
correction. This directory supplies the readable definitions used to compile the
scalar instruction tables. Their source bytes and the supplied bundle hash are
listed in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json). The runtime is a separate
implementation of scalar evaluation and finite chain transfer. The supplied
reference evaluator's optional C++ residual engine and text programs are also
included; production uses `fspt/full_formula/native.cpp` instead. Direct reference
evaluation can use `accelerate=False` without that optional engine.

## Fields and coordinates

In spatial dimension `d`, the public fields are

| Field | Degree | Coefficients | Meaning |
|---|---:|---|---|
| `n` | `d-2` | signed integers with grading twist | p+ip decoration |
| `a` | `d-1` | binary | native Majorana decoration |
| `c` | `d` | binary | complex-fermion decoration |
| `w` | 2 | binary | fermion-parity extension `omega2` |
| `s` | 1 | binary | antiunitary character `s1` |

The terminal phase has degree `d+1` in `R/Z_s`. Integer fields retain their signed
values. Mathematical floors, canonical binary lifts and exact divisions are
applied where the formulas specify them. A required nonintegral quotient raises
an error. In this API dictionary `a` denotes the native Majorana field; the formula guide
uses `n_M` for that field and reserves its temporary mathematical `a` for the
parity of `n`. The internal shifted Majorana field is `u = a + s cup carry(n)`, where
`carry(n) = floor(n/2) mod 2`; the runtime applies this conversion once.

The lower tower is solved before the terminal source. A source value is an
obstruction cochain. Its class is tested separately by the group engine: nonzero
exact cochains are solved, not rejected. Stacking first combines lower fields,
then adds the complete terminal correction, and finally reduces by all gauge
identifications.

## Definition map

All paths below are relative to `publication_source/` unless explicitly stated.
Each cited function is an executable, term-by-term definition.

| Operation | Readable definition | Compiled/runtime implementation |
|---|---|---|
| Cup, higher cup, signed differential, ordered word operations, lifts and carries | `reference/d4_input/code/cochains.py` | `fspt/formulas.py`, compiler scalar operations |
| Native lower obstruction tower | `cochains.py:parity`, `compact.py:kappa`; `full3/lower.py` | `source_3_majorana`, `source_3_fermion`, `source_4_majorana`, `source_4_fermion` |
| Pure p+ip higher source terms and binary completion | `reference/d4_input/code/explicit_pip.py:pure_terms16,binary_completion`, adjacent `Y5_*`/`Y6_*` tables | `y6`, `h6`, `high6`; source assembly in `runtime.py` |
| Shared six-cochain source blocks | `full3/source.py:blocks,high_source16`; `joint/cubic_repair.py` | `high6`, including its ordered cubic output |
| 3+1D full source and product | `full3/source.py:source16,product16`; `full3/lower.py`; `omega3/prism.py` | `lift3_source`, `lift3_product`, lower source/product DAGs and interval/triangle integration |
| 4+1D lower product | `full4/product_full.py:lower` | `product_4_majorana`, `product_4_fermion` |
| 4+1D nonbinary terminal product | `full4/product_full.py:collected_blocks,phase48` | `nonbinary4` |
| 4+1D binary terminal product | `full4/product_full.py:Zvalue,Ls`; `full4/kernel_full.py:rho`; `full4/graded_full.py` | `rho4`, `tensor4`, normalized finite transfer in `runtime.py` |
| Balanced tensor polynomials | `terminal_general/tensor_compact.py`; `unitary4/transfer_model.py` | `tensor4` |
| Closed-Majorana CA and operator laws, degrees 1–3 | `fspt/majorana_complete.py` | `majorana_*` DAGs and `fspt/majorana_backend.py` |
| Complete gauge cylinders and reductions | `gap/full_stacking.g`, `gap/finite_full.g` | General cylinders plus exact compiled `gauge_*`/`vacuum_*` specializations |

Here `cochains.py` and `compact.py` in the lower-tower row mean the versions in
`reference/d4_input/code/`. The four-dimensional lower fermion product includes
the closed `ab` correction once. The source and product retain their matched
ordered cubic terms. The three-dimensional construction retains its full
multiplicative-suspension coordinate. CA/operator fields are explicitly named
and are not silently substituted into the publication coordinate.

## Runtime interface

```python
from fspt.full_formula import Backend
backend = Backend()
value = backend.source(d, "bosonic", fields)
correction = backend.product(d, "bosonic", left, right, background)
```

A field is a tuple of length `2**(D+1)` on an ordered `D`-simplex. The entry at
`sum(1 << v for v in face)` stores that face's value; other degrees are zero.
`fields` has keys `n,a,c,w,s`; `left` and `right` contain `n,a,c`, and `background`
contains `w,s`. All entries are exact integers.

The stage is `majorana`, `fermion` or `bosonic`. Source output degrees are
`d,d+1,d+2`; product correction degrees are `d-1,d,d+1`. A product returns the
correction only, before adding the two input fields. Binary outputs are bits;
terminal outputs are exact `Fraction` values modulo one. Local coefficients may
have denominator 16 or 48; the state phases and gauge witnesses are not restricted
to those denominators. Integer overflow in the optional native evaluator falls
back to exact Python arithmetic.

`scripts/full_formula_worker.py` provides the same interface as a persistent
JSONL process. Requests use `operation=source|product`, `dimension`, `stage` and
the field dictionaries above. Binary responses have `value,modulus`; phases have
`numerator,denominator`. Errors return `ok=false` and are never replaced with zero.

Every compiled table in `fspt/data/full_formula/` is a directed acyclic program:
`const` and `field` introduce integers, `add`/`mul` reference earlier nodes,
`mod` uses a positive modulus, `div` requires exact divisibility, `floor` is
mathematical integer division, and `bit` extracts a binary digit. `outputs` lists
the terminal node indices. These rules and the readable functions give complete
operation definitions without external lookup or a primitive-fitting solver.

## Lower-dimensional endpoints

The complete publication-coordinate source/product implementation is for spatial
dimensions 3 and 4. The engine additionally provides independently calibrated
endpoints:

- Dimension 1 uses the explicit fMPS coordinate in `fspt/full_formula/fmps1.py`,
  including its parity gauge quotient. An exact nonzero extension is explicitly
  trivialized before using a split odd sector.
- Dimension 2 uses the known degree-one Majorana source and stacking law when
  the integer decoration is absent. The antiunitary Bott controls lie here.
- Split unitary symmetry admits a separate neutral chiral integer factor.
  For the two supplied nonsplit unitary controls, `--zero-chiral-fiber` computes
  the finite subgroup and separately records its abstract infinite-cyclic
  completion. A marked chiral generator and minimal chiral index are not computed.

General nonsplit nonzero-chiral cochain requests remain unsupported. The optional
experimental descent API is not a validated physical endpoint and is not used by
any accepted public example. These scope statements do not remove any 3+1D or
4+1D obstruction or stacking term.
