# Unified E8-first notation

Use `(e_p,n_p,n_{p+2},nu_{p+3})`, with `p=spatial_dimension-2`.
The first coordinate is neutral E8, the second is integer CI, the third is
localized integer charge, and the last is the **one shared phase**.
Both leading coordinates have sign `s1`; charge has sign `rho1`; phase
has sign `s1`. The extension lift has sign `rho1+s1`.

The Python representation is `insulator.E8State(e_p,n_p,n_p2,nu_p3)`.
Source arguments and gauge parameters follow the same E8-first order.
The existing `insulator.State` remains the CI-only interface.

The thermal coefficient map is `n_p_SC=16e_p+2n_p`. This is not the full
parity-state map: lower binary fields, the circle quotient, and phase
transport must also be retained. Integer charge cannot be replaced by
its parity without preserving the missing circle response.

Supplied archives and dated historical reviews retain their original
bytes and notation as provenance.
