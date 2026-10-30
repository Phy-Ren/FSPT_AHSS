# Unified E8-first notation

Use `(e_p,n_p,n_{p+2},nu_{p+3})`, with `p=spatial_dimension-2`.
The first coordinate is neutral E8, the second is integer CI, the third is
localized integer charge, and the last is the **one shared phase**.
Both leading coordinates have sign `s1`; charge has sign `r1`; phase
has sign `s1`. The extension lift has sign `rho1`.
The approved meanings are `rho1` for the charge-circle action, `s1` for
antiunitarity, and `r1=rho1+s1` modulo two for charge reversal.
See [notation and current inputs](../NOTATION_AND_INPUTS.md).

The Python representation is `insulator.E8State(e_p,n_p,n_p2,nu_p3)`.
Source arguments and gauge parameters follow the same E8-first order.
The existing `insulator.State` remains the CI-only interface.

## AHSS page indices in this tower

Use `d_r:(a,q) -> (a+r,q-r+1)`. The coefficient row `q` records the
spacetime dimension of the invertible decoration, not the cochain degree
of its field. The specified tower has rows

- `(e_p,n_p)` in `(a,q)=(p,3)`: E8 and IQH decorations;
- `n_{p+2}` in `(p+2,1)`: localized integer charge;
- `nu_{p+3}` in `(p+3,0)`: the shared bosonic phase coordinate.

The possible nonempty targets give `d_2` from charge to phase, `d_3` from
the E8/IQH row to charge, and `d_4` from that row to phase. A possible
target does not assert that every component of its operation is nonzero.
There are no `d_5` or `d_6` differentials in this four-coordinate tower.
Higher operations are evaluated after the preceding equations and their
allowed trivializations, with their product and gauge corrections.

An additional **intrinsic 4+1D** coefficient row would instead have
`q=5`, with a separate uniform field `r0`. That optional enlargement is
discussed only in the dedicated intrinsic-response research files. Its
possible `d_5,d_6` must not be described as missing operations of the
specified `(e_p,n_p,n_{p+2},nu_{p+3})` framework.

The thermal coefficient map is `n_p_SC=16e_p+2n_p`. This is not the full
parity-state map: lower binary fields, the circle quotient, and phase
transport must also be retained. Integer charge cannot be replaced by
its parity without preserving the missing circle response.

Supplied archives and dated historical reviews retain their original
bytes and notation as provenance.
