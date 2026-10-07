# Why the complete Majorana carry becomes smaller

The revised four-dimensional formula is exactly the previous open-cochain
representative. Its 5,707-term binary carry can be replaced before expanding
the second binary digit. The result has two half-valued face products,
seven additional ordinary quarter-valued terms, and four separately lifted
binary polynomials. Their interiors contain 146 terms.

The following notation is local to this proof. Write

```math
\begin{gathered}
u=\check n_3,\quad v=\check n'_3,\quad
A=du,\quad A'=dv,\quad
B=\beta^\circ u,\quad B'=\beta^\circ v,\\
r=\beta A,\quad r'=\beta A',\quad
L=u\cup_3v,\quad J=A\cup_4A',\quad X=B+B'-dL.
\end{gathered}
```

Here $`A,A'`$ are binary differentials, canonically lifted in integer
arithmetic. Thus $`dB=-r`$, $`dB'=-r'`$, and $`dX=-(r+r')`$.
All higher cups below are signed integer cups.

The old integer numerator before taking its second digit is

```math
\begin{aligned}
P={}&r\cup_4r'+X\cup_2J+J\cup_2X+J\cup_2J
 +X\cup_3dJ-J\cup_3(r+r')+J\cup_3dJ+\omega_2J.
\end{aligned}
```

A signed cup identity gives

```math
\begin{aligned}
P={}&V+dF+2Q,\\
V={}&-r\cup_4r'+(r+r')\cup_3J
 -J\cup_3\beta(A+A')+J\cup_2J-\omega_2J,\\
F={}&X\cup_3J,\\
Q={}&X\cup_2J+r\cup_4r'+\omega_2J.
\end{aligned}
```

This is an integer identity, including the canonical carry
$`\beta(A+A')=r+r'-dJ`$. It has been verified by complete integer
coefficient comparison, not only modulo two.

Let $`H_{\mathbb Z}`$ be the signed integer version of the fixed normalized
Eilenberg–Zilber homotopy used to construct the original coefficient. It
satisfies $`dH_{\mathbb Z}+H_{\mathbb Z}d=1-\mathrm{AW}`$ and reduces to
the original binary homotopy, denoted below by $`H`$. Here $`\mathrm{AW}`$
denotes the full shuffle–Alexander–Whitney projection onto the tensor
model and back. For these particular cochains,

```math
H_{\mathbb Z}F=0,\qquad \mathrm{AW}F=0,
\qquad H_{\mathbb Z}dF=F.
```

The first equality follows by evaluating every normalized contribution;
each vanishes. The second also follows from normalization on the two
original degree-three input axes: their relative tensor starts in degree
six, above the degree-five cochain $`F`$. Consequently no new output gauge,
ordinary or twisted, remains in this reduction.

For every integer $`P`$,
$`\widetilde P/2=(P-\bar P)/4\pmod1`$. The preceding identity therefore
gives

```math
\frac12H\widetilde P
=\frac12HQ
 +\frac14\big[H_{\mathbb Z}V+F-H_{\mathbb Z}\bar P\big]
 \pmod1.
```

In $`HQ`$, the integer $`Q`$ is first reduced modulo two; the following
identity is an identity of binary cochains. Its terms are explicit:

```math
(HQ)_{012345}=J_{12345}L_{0145}+J_{01235}L_{0345},
```

```math
\begin{aligned}
(H_{\mathbb Z}V)_{012345}
={}&-J_{01235}J_{01345}+J_{02345}J_{01245}\\
&-J_{01235}J_{12345}-J_{01345}J_{12345}.
\end{aligned}
```

Finally, $`-H_{\mathbb Z}\bar P`$ is exactly the four signed canonical
lifts in the [complete coefficient table](FOUR_DIMENSIONAL_MAJORANA_STACKING_LIFTS.md).
Substituting $`L=-\lambda_3^\gamma`$ and $`J=-\lambda_4^\gamma`$ yields
the revised physical formula. Whole binary lifts are retained throughout;
$`P`$ itself need not be even.

The [standalone integer-chain certificate](coefficients/verify_majorana_signed_transfer.py)
checks the signed chain identity and normalization exactly through the
required degrees. The complete phase passes 1,024 arbitrary open-input
checks against the original frozen formula and its existing gauge. An
independent native-cochain implementation checks the signed reduction
without using its scalar compiler. The public
[standalone replay](coefficients/verify_majorana_carry_reduction.py) compares
the new expression with the archived 5,707-term table on 512 arbitrary open
inputs, exercises all sixteen lift patterns, and covers all four quarter
residues with the unchanged terms. The
[public receipt](coefficients/FOUR_DIMENSIONAL_MAJORANA_CARRY_REPLAY.json)
records the coefficient-file hashes and counts.
