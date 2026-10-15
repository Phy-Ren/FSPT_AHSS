# Global formula-wiring audit

These exact checks accompanied the new point-group campaign. The files retain
original paths and logs; set `U1_ROOT` to the checkout path to rerun a GAP
script. The committed portable regression is
`tests/test_backend_source_cache.py`.

- `audit.g` / `audit.log`: 7,500 saturated-kernel membership checks, all 64
  nonabelian D4 multiplication pairs, and six incoming-charge-gauge comparisons
  on nonzero C2h roots. This first log records discovery of the source-cache bug.
- `bar_completion.g` / `bar_completion.log`: the corrected cache and 72 explicit
  normalized-bar completion identities in C2h, with spin conventions evaluated
  independently. The same six stabilizer comparisons pass.
- `odd_primary.g` / `odd_primary.log`: C3, C5, C6, and C9 controls with complete
  inverses and root powers. Their groups are Z3^2, Z5^2, Z3 x Z12, and Z9^2.
- `unittest.log`: 69 tests passed in 72.719 seconds, including the context-cache
  regression and finite-point-group neutral E8 extension certificates.

The fixed bug concerned reusing one state object with different background
contexts. The old cache omitted the context; the new cache checks context
identity. `classify.py` creates one new context in one fresh GAP process per
case, so no change to the previously calculated groups follows from this fix.
The new campaign nonetheless uses the corrected source snapshot `f572a98`.

This is verification of the operative formulas and their implementation.
It does not settle the universal physical CI-kernel identification. Neither
literature values nor anticipated group types are classification inputs.
