# Geometric pairing coordinate in 3+1D

The current reference uses the original Majorana arrows on every ordinary
component and the same single-layer rule for both inputs and the output.
The direct parity count is the current O4 and E3 in
[the physical formula page](THREE_DIMENSIONAL.md).
This page compares to the previous coordinate and proves the full phase transport.

## Single-state map and inverse

{{equation:three-dimensional-geometric-reference--checked-fermion}}

The previous complex-fermion coordinate is `check n3`; the current one is
`n3`. All other single-state fields, including the additive phase, retain
their values. The inverse adds the same binary B3. In particular this map
does not move or reverse any ordinary Majorana operator.
The previous obstruction is `O4+dB3`. The difference is exactly the
higher-cup boundary
`dB3 = d(check n2) cup1 check n2 + check n2 cup1 d(check n2)`.
The pure p+ip obstruction is unchanged.

## Product map

{{equation:three-dimensional-geometric-reference--pair-cochain}}

{{equation:three-dimensional-geometric-reference--phase-input-product}}

Thus the previous product, evaluated on the checked inputs, has output
`check N3+dB2`; the current product mapped into that coordinate has
output `check N3`. The face conversion changes adjacent point occupations
together. The lower source/product identity is exact, with the full
Majorana output, for both omega2 and s1. When the sheets vanish,
`dB3=0` and `Delta B3=dB2`, so O4 and E3 reduce pointwise to the original
Majorana laws. Their original projector sequence is retained.

## Complete phase transport

{{equation:three-dimensional-geometric-reference--phase-transport}}

The suffix `old` is confined to this comparison. The main page prints all
six transported contributions in the current variables. No additional
phase primitive has to be solved for. Its point-fermion contribution
includes the explicitly displayed face-reference phase; the other two
CF exchange contributions include their changed output evaluations.
The remaining three contributions retain their existing coefficient tables.

To verify the new phase, let x be any binary three-cochain and b any binary
two-cochain. The CF source is the half-valued quadratic expression

```math
Q(x)=\frac12[\omega_2x+x\cup_1x+dx\cup_2x].
```

Its finite variation is

```math
Q(x+db)-Q(x)=d_{s_1}\frac12[
\omega_2b+b^2+db\cup_1b+x\cup_2db].
```

This is an identity of cochains for closed omega2, with arbitrary s1.
All other terms of the source depend on x only through dx or on lower
fields, so they are unchanged by db. Substitute
`x=check N3+dB2` and `b=B2` to obtain the complete source/product identity.
The inverse traverses the same face conversion backwards and subtracts
its phase. This also transports all cylinder gauges, associators, and
exchange homotopies; a source-only substitution would be incorrect.

## Self-stacking and the time-reversal example

The diagonal of the new pure sheet term has two terms, because
`z3psi(a,a)=0` for a closed binary one-cochain. Thus
`N3=Sq1(check n2)+s1 check n2+tilde n1 (bar n1)^2+s1 tilde n1 bar n1`.
For either finite-root branch, `n1=0` or `n1=s1`, one has
`B2=check n2` and `B3[check N2]=0`. The previous output in every retained
self-stacking coefficient formula is consequently `N3+d check n2`.
The current self-stacking page applies this substitution and its finite
phase together.

For Z4^{f,T}, `s1=m1`, `omega2=m1^2`, the displayed root representatives
have B3=0. B2 vanishes for the p+ip square and equals m1^2 for the
Majorana square. Its differential vanishes, and its phase is
`(omega2 B2+B2^2)/2=0 mod 1`. The complete root phases and the Z16 group
therefore remain unchanged, now checked in the new coordinate.

## Reproducibility and retained data

The old coefficient tables are fixed polynomial kernels, not independent
current coordinates. Their CF input is now check n3. Current source and
product wrappers apply the maps printed above; frozen historical
certificates retain their original variable names and hashes.
The geometric lower census covers all 2^24 local P matchings and all 2^24
local F matchings. The phase-variation proof is a zero polynomial in 45
independent binary inputs, with a nonzero negative control when omega2 B2
is omitted. These are exact identities, not a new computation of the
microscopic bosonic stacking amplitude.

The [reproduction bundle](verification/geometric_3d/README.md) contains the
complete directed-matching census and current API comparison. The
[finite phase identity](coefficients/verify_three_dimensional_geometric_phase_transport.py)
and [complete current self-stacking identity](coefficients/verify_three_dimensional_geometric_self_stacking.py)
verify the phase transport and all six diagonal contributions separately.
