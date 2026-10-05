# Closed Majorana laws and lower-dimensional endpoints

This appendix gives the closed-Majorana source and product through $4+1$D,
then the separately implemented $1+1$D endpoint. It uses the same
[cochain operations](OPERATIONS.md) as the main guide. The closed-Majorana
CA coordinate and its operator-coordinate transport are stated explicitly;
neither is silently identified with the nonzero-integer publication
coordinate of the [main guide](../FORMULA_GUIDE.md). In this appendix the
canonical integer lifts of the binary fields, their ordinary Bocksteins,
and their signed integer cup products have **untwisted integer** coefficients.
The final additive phase takes values in $(\mathbb R/\mathbb Z)_s$; its
differential is $d_s$. These two coefficient conventions have different
roles and must be kept distinct.

## Closed-Majorana tower

Let $q=1,2,3$, so spatial dimension is $d=q+1$. In this appendix only,
write $a=n_q$, $b=n'_q$ for **closed Majorana** cochains and
$c=n_{q+1}$, $c'=n'_{q+1}$ for complex-fermion cochains. There is no integer
layer here. Set

<a id="eq-m1"></a>

$$
N=a+b,\qquad P=\beta a,\quad P'=\beta b,\quad P_N=\beta N,
\quad r=[P]_2,\quad r'=[P']_2,
\quad o=a\cup_q b,\quad t=a\cup_{q-1}b,\quad m=t+so.
\tag{M1}
$$

The lower equation and product are

<a id="eq-m2"></a>

$$
dc=S^2a+wa+sr,\qquad C=c+c'+m.
\tag{M2}
$$

In the CA coordinate, the entire source and phase product factor as

<a id="eq-m3"></a>

$$
\begin{aligned}
\widehat O_{q+3}(a,c)&=\frac12(S^2c+wc)+\widehat O^\gamma_{q+3}(a),\\
\widehat E_{q+2}(a,c;b,c')&=\frac12\big[c\cup_qc'+dc\cup_{q+1}c'
 +(c+c')\cup_qm\big]+\widehat E^\gamma_{q+2}(a,b).
\end{aligned}
\tag{M3}
$$

The output additive logarithmic phase is the sum of the two input additive
logarithmic phases and $\widehat E$; the paper's multiplicative phase is
$\nu\nu'\exp(2\pi i\widehat E)$.

## Pure Majorana sources

For $q=2,3$, define $A=a\cup_{q-2}a$, $B=wa$, $R=sr$ and

<a id="eq-m4"></a>

$$
\begin{aligned}
\widehat O^\gamma_{q+3}(a)={}&\frac12\big[
 \zeta_{2,q}(w,a)+x_q(a)+A\cup_{q+1}B+A\cup_{q+1}R+B\cup_{q+1}R\\
&\qquad+\zeta_{1,q+1}(s,r)+(w\cup_1s)r+sA+s^2[\beta^+a]_2\big]\\
&+\frac14\big[\widetilde w P+P\cup_{q-1}P\big].
\end{aligned}
\tag{M4}
$$

The four word operations are

| $q$ | $\zeta_{2,q}(w,a)$ | $\zeta_{1,q+1}(s,r)$ |
|---|---|---|
| 2 | $\operatorname{MS}_{1231343}(w,w,a,a)$ | $\operatorname{MS}_{1231434}(s,s,r,r)$ |
| 3 | $\operatorname{MS}_{12313434}(w,w,a,a)$ | $\operatorname{MS}_{12314343}(s,s,r,r)$ |

The intrinsic source polynomials are

<a id="eq-m5"></a>

$$
\begin{aligned}
x_2(a)&=(\operatorname{MS}_{1213243}+\operatorname{MS}_{1213431}
 +\operatorname{MS}_{1232141}+\operatorname{MS}_{1234321})(a,a,a,a),\\
x_3(a)&=(\operatorname{MS}_{1213243142}+\operatorname{MS}_{1213431412}
 +\operatorname{MS}_{1232431421}+\operatorname{MS}_{1234314212})(a,a,a,a)
 +r\cup_2r.
\end{aligned}
\tag{M5}
$$

For $q=1$ the endpoint source is instead

<a id="eq-m6"></a>

$$
\begin{aligned}
\widehat O^\gamma_4(a)={}&\frac12\big[
 \operatorname{MS}_{123134}(w,w,a,a)+(wa)\cup_2(sr)
 +(w\cup_1s)r+s(s+a)r\big]\\
&+\frac14\big[\widetilde w P+\widetilde s\,\widetilde a\,P\big].
\end{aligned}
\tag{M6}
$$

All terms inside the half bracket are binary; the quarter bracket uses
integer lifts and signed cups.

## Pure Majorana products for $q=2,3$

One degree-indexed expression gives the product in both dimensions:

<a id="eq-m7"></a>

$$
\begin{aligned}
\widehat E^\gamma_{q+2}={}&\frac12z_{q+2}
 +\frac14\big[(-1)^{q+1}P\cup_qP'
 +(-1)^q(P+P')\cup_{q-1}\widetilde o\\
&\qquad-\widetilde o\cup_{q-1}P_N
 +\widetilde o\cup_{q-2}\widetilde o-\widetilde w\,\widetilde o\big].
\end{aligned}
\tag{M7}
$$

Lift the binary overlap $o$ after forming it. With
$A_N=N\cup_{q-2}N$ and $B_b=b\cup_{q-2}b$, the binary completion is

<a id="eq-m8"></a>

$$
\begin{aligned}
z_{q+2}={}&z^0_{q+2}+(wN)\cup_{q+1}m
 +dt\cup_{q+2}(wN)+B_b\cup_{q+2}(wa)\\
&+(B_b+wb)\cup_{q+2}(sr)+(w\cup_1s)o
 +t\cup_{q+1}[s(r+r')]\\
&+A_N\cup_{q+1}(so)+t\cup_q(so)\\
&+s\big[m+r\cup_{q+1}r'+o\cup_{q-1}o
 +(r+r')\cup_{q+1}(so)+(so)\cup_qo
 +[\beta^+N-\beta^+a-\beta^+b]_2\big].
\end{aligned}
\tag{M8}
$$

Here is the entire intrinsic polynomial $z^0_{q+2}$. First sum the word
groups in this table, applying the degree rule immediately below it:

| Words | Ordered inputs |
|---|---|
| `12131432412`, `12343213431`, `23412342324` | $(a,b,b,b)$ |
| `12123434123`, `12131412324`, `12134131234`, `12312412423`, `12314324123`, `12314342413`, `13242412314`, `13412321341`, `13412321413`, `13413142134`, `13432412314`, `31214124324` | $(a,a,b,b)$ |
| `12413432312` | $(a,a,a,b)$ |
| `12131432412` | $(b,a,a,N)$ |
| `12131432412` | $(N,a,a,b)$ |
| `12131432412`, `12134341321` | $(N,b,b,a)$ |
| `1212312` | $(N,b,o)$ |
| `12313123` | $(b,a,t)$ |
| `12131232` | $(r,b,b)$ |
| `123131212` | $(b\cup_{q-2}b,a,N)$ |
| `123131212` | $(N\cup_{q-2}N,b,a)$ |

For $q=3$, use the displayed words unchanged. For $q=2$, a word with $k$
input labels contributes only if its final $k$ letters contain every label
exactly once. In that case remove its final $k-1$ letters; if any label is
then missing, the result is zero. Otherwise evaluate the shortened word on
the table's inputs. This is an explicit finite desuspension rule, including
the groups whose first input has degree greater than $q$.

To that word sum add all six cup terms:

<a id="eq-m9"></a>

$$
\begin{aligned}
z^0_{q+2}={}&\text{word sum}
 +t\cup_{q-1}b+(r+r')\cup_{q-1}o
 +o\cup_{q-1}(r+r'+b\cup_{q-1}a)\\
&+t\cup_{q+1}(a\cup_{q-2}a+b\cup_{q-2}b)
 +b\cup_q(a\cup_{q-1}t)+r'\cup_qr.
\end{aligned}
\tag{M9}
$$

Equations (M7)--(M9) are the compact closed-Majorana product used by
`fspt/majorana_complete.py`. At $q=2$ this representative is the stated
desuspension of the $q=3$ product; the earlier manuscript's longer product
uses a stacking-move boundary dictionary. One must compare complete
products in matching coordinates, not individual pure terms.

## The $q=1$ product

The $2+1$D endpoint is stated explicitly to retain its fractional carries.
Use $N,P,P',o,t,m$ from (M1); here $t=ab$. Form the **integer** signed cup
$S=\widetilde a\cup_1\widetilde b$ and $T=dS$. Set
$e_a=s\cup_1a$, $e_b=s\cup_1b$, $e_o=s\cup_1o$ and the binary expression

<a id="eq-m10"></a>

$$
\begin{aligned}
L_s={}&s(e_a+e_b+e_o)o+e_a oN
 +(e_a a+a e_b+sa+as)o+s(oa+ab+bo).
\end{aligned}
\tag{M10}
$$

Then the pure phase is

<a id="eq-m11"></a>

$$
\begin{aligned}
\widehat E^\gamma_3={}&
\frac14\big[P\cup_1P'-(P+P')S-S(P+P')+ST\big]\\
&+\frac12[a\cup_1(ab)]b
 -\frac18\widetilde{N^3}+\frac18\widetilde{a^3}+\frac18\widetilde{b^3}\\
&+\frac12(wN)\cup_2(ab)-\frac14\widetilde w S
 +\frac12L_s+\frac14\widetilde{sab}\\
&+\frac12\big[(w\cup_1s)o+(wN)\cup_2(so)+(wb)\cup_3(sa^2)\big]
 \pmod1.
\end{aligned}
\tag{M11}
$$

The tildes on the eighth-valued and $\widetilde{sab}$ terms mean lift the
displayed **binary product**. The first line and $\widetilde w S$ instead
remain integral signed products. Add the mixed complex-fermion bracket of
(M3) to obtain the complete phase. This is the implemented endpoint law;
discarding negative cup indices in (M7) alone would miss its coordinate
correction.

## CA and operator coordinates

For the same lower fields, define the single-state phase correction

$$
\Gamma(c)=\frac12c\cup_{q+1}dc.
$$

The paired transport is

<a id="eq-m12"></a>

$$
\widehat O^{\rm op}=\widehat O^{\rm CA}+d_s\Gamma(c),\qquad
\widehat E^{\rm op}=\widehat E^{\rm CA}
 +\Gamma(C)-\Gamma(c)-\Gamma(c').
\tag{M12}
$$

This gives both coordinates without duplicating a long polynomial. It does
not identify either one with a different integer-layer convention.

## The implemented $2+1$D chiral domain

The degree-one Majorana formulas above compute the zero-integer fiber.
For split unitary symmetry ($w=s=0$), an independent neutral chiral
$\mathbb Z$ factor can be adjoined. For the two supplied nonsplit unitary
controls, the `--zero-chiral-fiber` mode reports the computed finite subgroup and its
abstract infinite-cyclic completion separately; it does not produce a
marked minimal chiral generator. General nonsplit nonzero-chiral cochain
requests are unsupported by this endpoint. This limitation does not remove
any term from the complete $3+1$D or $4+1$D formulas.

## The implemented $1+1$D fMPS endpoint

The independent fMPS coordinate has fields
$\gamma\in Z^0(G_b,\mathbb Z_2)$,
$\beta\in C^1(G_b,\mathbb Z_2)$,
$\alpha\in C^2(G_b,(\mathbb R/\mathbb Z)_s)$ and no integer layer.
In the runtime they are `a,c,v`. Its equations are

<a id="eq-m13"></a>

$$
d\gamma=0,\qquad d\beta=\gamma w,\qquad
d_s\alpha=\frac12\beta w.
\tag{M13}
$$

For nonzero $\gamma$ the evaluator requires $w=0$ pointwise. If the
extension cocycle is nonzero but exact, explicitly trivialize it before
using the split odd sector. For two admissible inputs, the product is

<a id="eq-m14"></a>

$$
\begin{aligned}
\gamma''&=\gamma+\gamma',\\
\beta''&=\beta+\beta'+\gamma\gamma's,\\
\alpha''&=\alpha+\alpha'+\frac12\beta\beta'
 +\begin{cases}\frac12\beta_{\rm even}^2,&\gamma\ne\gamma',\\
 0,&\gamma=\gamma'.\end{cases}
\end{aligned}
\tag{M14}
$$

$\beta_{\rm even}$ is the degree-one cochain of the input with $\gamma=0$.
The equivalence includes the residual parity gauge
$\alpha\sim\alpha+w/2$. This gauge quotient is part of the classification,
not an optional change to (M14). The coordinate is implemented in
[`fspt/full_formula/fmps1.py`](../../fspt/full_formula/fmps1.py);
no unstated dictionary to the manuscript's $\nu$ coordinate is used.
