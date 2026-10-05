# Fixed operations in the terminal source

The [shared source](../FORMULA_GUIDE.md#shared-terminal-source) uses only two
larger binary operations, $`T_6`$ and $`y_6`$. This appendix defines both by
bounded sums. Use the conventions in [Operations](OPERATIONS.md) and the
shared quantities $`A_4,K_4,v_3,\ell^\omega_3,\mathcal C_6,\Xi_5`$ of the guide.

## Closed degree-four operation

For a closed binary four-cochain $`z`$, set $`b_z=[\beta z]_2`$ and
$`\beta^+z=(\beta z+\widetilde b_z)/2`$. Define

<a id="eq-s4"></a>

**(S4)**

```math
\begin{aligned}
M_7(z;w,s)={}&\zeta_{2,4}(w,z)+x_4(z)
 +(z\cup_2z)\cup_5(wz)+(z\cup_2z)\cup_5(sb_z)\\
&+(wz)\cup_5(sb_z)+\zeta_{1,5}(s,b_z)
 +(w\cup_1s)b_z+s(z\cup_2z)+s^2[\beta^+z]_2,\\
\zeta_{2,4}(w,z)={}&\mathop{\mathrm{MS}}\nolimits_{123134343}(w,w,z,z),\\
\zeta_{1,5}(s,b_z)={}&\mathop{\mathrm{MS}}\nolimits_{123143434}(s,s,b_z,b_z).
\end{aligned}
```

$`x_4(z)`$ is the sum $`\sum_{v\in\mathcal W_4}\mathop{\mathrm{MS}}\nolimits_v(z,z,z,z)`$,
where **all 453 words** of $`\mathcal W_4`$ are printed in
[Coefficients](COEFFICIENTS.md#adem-words). No coefficient is fitted or chosen
during evaluation.

## Open degree-three continuation

For an arbitrary binary three-cochain $`z`$, use a height interval $`J=[0,1]`$.
On its product with a base simplex set

```math
z^J((t_0,x_0),\ldots,(t_3,x_3))=t_0z(x_0,\ldots,x_3).
```

Backgrounds are pulled from the base. Form

<a id="eq-s5"></a>

**(S5)**

```math
\begin{aligned}
P&=S^2z^J+sS^1z^J+wz^J,\qquad V=S^1z^J,\\
T_6(z;w,s)&=\tau_J\big[S^2P+wP+S^3V+sS^2V
 +\ell^\omega_3V+M_7(dz^J;w,s)\big].
\end{aligned}
```

The integration is the seven-path binary sum (O8). The input to the
Bockstein inside $`M_7`$ is the **closed** four-cochain $`dz^J`$, not the open
three-cochain $`z`$.

<a id="source-completion"></a>
## Integer-layer completion

For a twisted integer two-cocycle $`n`$, use $`a=[n]_2`$,
$`h=[\lfloor n/2\rfloor]_2`$, $`A_4=a^2+Wa`$, and the guide's background and
carry definitions. The following expressions do not require a choice of
Majorana or complex-fermion decoration:

<a id="eq-s6"></a>

**(S6)**

```math
\begin{aligned}
V_6={}&\frac14\big[\widetilde w K_4+K_4\cup_2K_4
 +(\beta A_4)\cup_3K_4-K_4\cup_3(v_3n)
 -\widetilde{\mathcal C_6}\big]\\
&+\frac1{16}\mathcal P_s(W)n+\frac18\widetilde W n^2,\\
\Theta_6={}&\frac14\widetilde w\,\widetilde A_4
 +\frac12(A_4\cup_1\ell^\omega_3),\\
B^{\rm par}_7={}&\Xi_5\cup_3\Xi_5
 +(S^2A_4+sS^1A_4+wA_4)\cup_4\Xi_5+w\Xi_5,\\
\widehat M_7={}&\frac12M_7(A_4;w,s)
 +\frac14\big[\widetilde w\,\beta A_4
 +(\beta A_4)\cup_3(\beta A_4)\big],\\
R_7={}&\left[\frac{d_s(16V_6+16\Theta_6)
 +8\widetilde{B^{\rm par}_7}+16\widehat M_7}{8}\right]_2.
\end{aligned}
```

Here $`A_4`$ is closed, so its ordinary Bockstein is defined. Every rational
term in (S6) is an exact rational cochain during assembly. In particular,
form the whole numerator defining $`R_7`$ over the integers, divide by eight,
and only then take parity. Its numerator is pointwise divisible by eight.

The required binary operation is

<a id="eq-s7"></a>

**(S7)**

```math
y_6(n;w,s)=\mathcal H^{(3)}_6R_7+\mathop{\mathrm{AW}}\nolimits^*Y^{\rm tot}_6.
```

For the first term use the three-factor grid (O11), with factors ordered
$`(s,n,w)`$. On grid vertices $`(r_i,t_i,v_i)`$, pull $`s`$ along $`r`$ and $`w`$ along
$`v`$. Pull the integer field along $`t`$ with the necessary first-vertex
transport:

<a id="eq-s8"></a>

**(S8)**

```math
n^{\rm grid}(i_0i_1i_2)=(-1)^{s(r_{i_0},t_{i_0})}
 n(t_{i_0},t_{i_1},t_{i_2}).
```

Evaluate the **entire** known expression (S6) on each pulled-back input and
sum over $`h_6`$. This defines $`\mathcal H^{(3)}_6R_7`$.

The second term is the finite numerical polynomial specified in
[Coefficients](COEFFICIENTS.md#numerical-polynomial). It has eleven
tridegrees, uses explicit generalized integer binomials and first-vertex
transport, and contains no implicit primitive. That appendix prints every
coefficient, as well as a lossless machine-readable copy.

The three-factor source operation here and the terminal product operation
use different assignments to the same grid recursion. In this appendix
$`s`$ and $`w`$ occupy separate factors; in the terminal product they share one
background factor. Keeping this distinction is necessary for the formulas
to retain the stated coefficient transports.
