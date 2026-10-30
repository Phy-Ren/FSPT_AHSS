# 3+1D: even relations of a completed charge root

This appendix derives a cohomology-class formula for an even multiple of a
completed state `(e_1,n_1,n_3,nu_4)=(0,0,q,nu)`. The formula is proved below
but is **not implemented as a replacement for the full root calculation**.
It does not identify the literal saved phase or gauge witnesses. The
existing differential, product and gauge conventions are those of
[Operations](OPERATIONS.md#charge-source-twister-and-gauge) and the
[3+1D theory](THREE_DIMENSIONAL.md).

## Hypotheses and completion

Let `q in Z3(G,Z_r)` be the actual closed integer bar cochain. Assume the
chosen extension lift satisfies

```math
2\omega_R\in C^2(G,\mathbb Z_{\rho}),\qquad
d_{\rho}\omega_R\in C^3(G,\mathbb Z_{\rho}).
```

Then `W=2 omega_R mod 2` is a closed ordinary binary two-cochain. The
pure-charge source is

```math
O_5(q)=\omega_R\cup q+\frac12\mathrm{Sq}^2\bar q,
\qquad d_s\nu=O_5(q),\qquad 2O_5(q)=0\pmod1.
```

The argument assumes an actual completion, not merely a vanishing
uncomputed obstruction. Write the solver's completed phase as

```math
\nu=G^*b-H^*O_5(q)\pmod1,\qquad d_s b=F^*O_5(q).
```

Here `F*` transfers bar cochains to the native resolution, `G*` pulls
native cochains back to the bar resolution, and the integral comparison
homotopy has the engine's sign convention

```math
dH^*+H^*d=G^*F^*-1.
```

These maps use each cochain's coefficient system. The native phase seed
`b` is an actual rational cochain; it can contain quarters or finer
fractions. Even multiplication kills `H*O_5`, but need not kill `b`.

## The full bar relation for every even integer

Let `m in 2Z`, positive, zero or negative. A charge-removal relation
requires an integer native two-cochain `x` with

```math
A=F^*q,\qquad d_r x=-mA.
```

The full solver then supplies the bar parameter

```math
v=G^*x+mH^*q,\qquad
d_r v=-mG^*F^*q+m(G^*F^*q-q)=-mq,
\qquad \bar v=G^*\bar x.
```

Use `A=F*q` even when the original charge was constructed as `q=G*Q`.
The vector `F*G*Q` need not equal `Q`; replacing it can change the actual
removal seed and gauge witness.

For closed charges the original twister reduces to the bilinear map

```math
B(q,r)=\frac12\bar q\cup_2\bar r\pmod1.
```

Consequently the phase of the actual `m`-fold product is
`m nu + binom(m,2) B(q,q)`. This holds for all integers: bilinearity and
`binom(m+n,2)=binom(m,2)+binom(n,2)+mn` give the product law and its
inverse. Here `binom(m,2)=m(m-1)/2`, also for negative `m`; it is not a
count restricted to nonnegative powers.

The full cylinder gauge and shorter fixed-sheet gauge satisfy

```math
G^{\rm cylinder}_4(v;mq)-\widehat G^c_4(v;mq)
=d_s\left[\frac12\overline{mq}\cup_2\bar v\right]=0\pmod1.
```

The last equality is pointwise because `m` is even. In the short gauge,
the extra product `E^c_4(mq,d_r v)` also vanishes pointwise, while
`d bar v=0`. Combining the full product and charge removal therefore
gives the actual reduced bar phase

```math
R_m=mG^*b+
\frac12\left[
\epsilon_m\,\bar q\cup_2\bar q
+W\cup\bar v+\bar v\cup\bar v
\right]\pmod1,
\qquad \epsilon_m=\binom m2\bmod2.
```

Each term is closed modulo one. In particular, `d_s(mb)=0` follows from
the half-valued source. The integer charge remains `mq` until the full
integer gauge `v` removes it; it is never discarded by binary reduction.
For `m=2`, this retains `2G*b`, which can be a nonzero half-valued phase
when `b` has quarter entries.

## The native cohomology class

All binary inputs below are closed. Set `W_R=F*W` and
`r_R=F*r`, using binary coefficients. The coefficient map

```math
j:\mathbb F_2\longrightarrow(\mathbb R/\mathbb Z)_s,
\qquad j(1)=\frac12
```

is equivariant for either sign: `-1/2=1/2 mod 1`. Write `j_*` for its
induced cohomology map. Naturality under the comparison maps gives

```math
[R_m]=[mb]+j_*\left(
\epsilon_m\,\mathrm{Sq}^1[\bar A]
+[W_R]\cup[\bar x]+\mathrm{Sq}^2[\bar x]
\right)
\quad\in H^4(G,(\mathbb R/\mathbb Z)_s).
```

The degree-two square is the cup square. The other square can also be
written using ordinary native cups. With `r(g)` lifted to `0` or `1`,
the inhomogeneous differential gives the exact integer identity

```math
(d_0q-d_r q)(g_1,g_2,g_3,g_4)
=2r(g_1)q(g_2,g_3,g_4).
```

Thus `d_0q=2 r cup q`, with an ordinary untwisted cup in this integer
identity: here `q` is viewed as an integer function without its coefficient
transport. All cups in the resulting binary class formula are ordinary.
The ordinary integral Bockstein, reduced modulo two, is `Sq1`; hence
`Sq1[bar q]=[r] cup [bar q]`. Transfer gives

```math
\boxed{\displaystyle
[R_m]=\left[
mb+\frac12\left(
\epsilon_m\,r_R\cup\bar A
+W_R\cup\bar x+\bar x\cup\bar x
\right)\right].}
```

The cups on the right are native binary cups from a compatible diagonal.
This is equality of classes, not equality to the transferred vector
`F*R_m`. If `r=0`, the `Sq1` term vanishes as a class; the original bar
twister need not be pointwise zero. The derivation requires neither a
finite group nor commuting group elements.

## Incoming relations and retained witnesses

The map `j_*` need not be injective. Evaluate the displayed class in the
actual signed `H4(G,U1_s)` coordinates; binary coordinates cannot be read
as independent phase generators.

Changing the removal primitive by a closed integer two-cochain `z`
changes the phase class by the closed charge-gauge image
`j_*([W] cup [bar z] + Sq2[bar z])`. Thus the choice of primitive is
absorbed by the already included incoming charge-gauge relation. For
`m=0`, a nonzero closed choice of removal parameter likewise represents
an incoming gauge, rather than an additional vacuum root.

The resulting root relation must then enter the **full existing
presentation**. Closed CI sheet gauges can shift both charge and phase;
they need not define an independent phase-only quotient. Keep their
coupled rows, charge-root relations, CI-root relations and neutral E8
factor exactly as prescribed by the full four-data model. The formula
above does not replace that presentation by a quotient of `H4` alone.

The class identity leaves two representative comparisons unresolved:
`F*G*(mb)` can differ from `mb` by a coboundary, and transferred bar cups
and squares can differ from the chosen native operations by coboundaries.
The Bockstein-to-cup change is also a class statement. Explicit comparison
primitives are required before substituting this formula for any saved
native phase, full charge primitive, gauge or root witness. No such
substitution or performance claim is made here. For odd `m` the source
homotopy term need not vanish; that case is outside this identity.

The derivation uses the current charge blocks in
[cochains.g](../../gap/cochains.g), the exact completion in
[backend_half_phase.g](../../gap/backend_half_phase.g), and the full
root/incoming presentation in [classification.g](../../gap/classification.g).
It was checked against their `d3b2dcc` conventions. It adds no physical
spectrum identification beyond the supplied model.
