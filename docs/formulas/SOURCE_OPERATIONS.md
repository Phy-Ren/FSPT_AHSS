# Fixed operations in the terminal source

The [shared source](../FORMULA_GUIDE.md#shared-terminal-source) uses two fixed
binary operations, $`T_6`$ and $`y_6`$. The first continues the closed
Majorana source to an open three-cochain; the second completes the integer
layer. This appendix defines both by finite sums.

All fields retain the notation of the guide: $`n_2`$ is the integer layer,
$`\omega_2,s_1`$ are the backgrounds, a bar takes parity, and a tilde lifts a
binary expression to the integers. The check denotes the specific shifts
already defined there, including
$`\check\omega_2=\omega_2+s_1\cup s_1`$ and
$`\check{\mathcal O}_4=\bar n_2^2+\check\omega_2\bar n_2`$.
The Bocksteins $`\beta,\beta_{s_1},\beta^+`$, cup products, and integration
are defined in [Operations](OPERATIONS.md).

The substantial operations used in this appendix are:

| Operation | Output and purpose | Definition |
|---|---|---|
| $`\mathcal X_7[z]`$ | Binary degree-seven Adem operation on a closed four-cochain | (S4), [word table](COEFFICIENTS.md#adem-words) |
| $`M_7[z;\omega_2,s_1]`$ | Binary degree-seven closed-cochain source | (S4) |
| $`T_6[z;\omega_2,s_1]`$ | Binary degree-six continuation to an open three-cochain | (S5) |
| $`V_6,\Theta_6`$ | Exact rational degree-six source pieces | (S6) |
| $`B^{\rm par}_7`$ | Binary degree-seven remainder of the lower source | (S6) |
| $`\widehat M_7`$ | Degree-seven additive phase correction, with its displayed rational representative | (S6) |
| $`R_7`$ | Binary degree-seven remainder after exact integer division | (S6) |
| $`y_6[n_2;\omega_2,s_1]`$ | Binary degree-six integer-layer completion | (S7)–(S8) |

The quantities $`\mathcal C_6`$ and $`B_4^\psi`$ retain their
definitions in (S1)–(S2) of the guide. The latter is the integer part of the
carry that depends only on $`n_2`$ and the backgrounds; it has degree four.

## Closed degree-four operation

For a closed binary four-cochain $`z`$, define

<a id="eq-s4"></a>

**(S4)**

```math
\begin{aligned}
M_7[z;\omega_2,s_1]={}&\zeta_{2,4}(\omega_2,z)+\mathcal X_7[z]\\
&+(z\cup_2z)\cup_5(\omega_2z)
 +(z\cup_2z)\cup_5(s_1\overline{\beta z})\\
&+(\omega_2z)\cup_5(s_1\overline{\beta z})
 +\zeta_{1,5}(s_1,\overline{\beta z})\\
&+(\omega_2\cup_1s_1)\overline{\beta z}
 +s_1(z\cup_2z)+s_1^2\overline{\beta^+z},\\
\zeta_{2,4}(\omega_2,z)={}&
 \mathop{\mathrm{MS}}\nolimits_{123134343}(\omega_2,\omega_2,z,z),\\
\zeta_{1,5}(s_1,\overline{\beta z})={}&
 \mathop{\mathrm{MS}}\nolimits_{123143434}
 (s_1,s_1,\overline{\beta z},\overline{\beta z}),\\
\mathcal X_7[z]={}&\sum_{\eta\in\mathcal W_4}
 \mathop{\mathrm{MS}}\nolimits_\eta(z,z,z,z).
\end{aligned}
```

All **453 words** of $`\mathcal W_4`$ are printed in
[Coefficients](COEFFICIENTS.md#adem-words). The subscript of $`\mathcal X_7`$
is its output degree; that of the word set $`\mathcal W_4`$ is the input
degree. No coefficient is fitted or chosen during evaluation.

## Open degree-three continuation

For an arbitrary binary three-cochain $`z`$, use a height interval $`J=[0,1]`$.
On its product with a base simplex set

```math
z^J((t_0,x_0),\ldots,(t_3,x_3))=t_0z(x_0,\ldots,x_3).
```

Backgrounds are pulled from the base. The lower source acting on this field
is $`\mathrm{Sq}^2z^J+s_1\mathrm{Sq}^1z^J+\omega_2z^J`$; its output degree is
five. Thus define

<a id="eq-s5"></a>

**(S5)**

```math
\begin{aligned}
T_6[z;\omega_2,s_1]=\tau_J\big[&
 (\mathrm{Sq}^2+\omega_2\cup)
 (\mathrm{Sq}^2z^J+s_1\mathrm{Sq}^1z^J+\omega_2z^J)\\
&+\mathrm{Sq}^3\mathrm{Sq}^1z^J
 +s_1\mathrm{Sq}^2\mathrm{Sq}^1z^J\\
&+(\overline{\beta\omega_2}+s_1\omega_2)\mathrm{Sq}^1z^J
 +M_7[dz^J;\omega_2,s_1]\big].
\end{aligned}
```

Here $`(\mathrm{Sq}^2+\omega_2\cup)x`$ means
$`\mathrm{Sq}^2x+\omega_2\cup x`$. The integration is the seven-path binary
sum (O8). The input to the Bockstein inside $`M_7`$ is the **closed**
four-cochain $`dz^J`$, not the open three-cochain $`z`$.

<a id="source-completion"></a>
## Integer-layer completion

Let $`n_2`$ be a twisted integer two-cocycle. The following expressions use
the guide's $`\check{\mathcal O}_4,B_4^\psi,\mathcal C_6,\mathcal O^\psi_5`$ and do not
require a choice of Majorana or complex-fermion decoration:

<a id="eq-s6"></a>

**(S6)**

```math
\begin{aligned}
V_6={}&\frac14\big[
 \widetilde{\omega_2}B_4^\psi+B_4^\psi\cup_2B_4^\psi
 +(\beta\check{\mathcal O}_4)\cup_3B_4^\psi\\
&\qquad-B_4^\psi\cup_3[(\beta_{s_1}\check\omega_2)n_2]
 -\widetilde{\mathcal C_6}\big]\\
&+\frac1{16}\mathcal P_{s_1}(\check\omega_2)n_2
 +\frac18\widetilde{\check\omega_2}n_2^2,\\
\Theta_6={}&\frac14\widetilde{\omega_2}\widetilde{\check{\mathcal O}_4}
 +\frac12\big[\check{\mathcal O}_4\cup_1
 (\overline{\beta\omega_2}+s_1\omega_2)\big],\\
B^{\rm par}_7={}&\mathcal O^\psi_5\cup_3\mathcal O^\psi_5
 +(\mathrm{Sq}^2\check{\mathcal O}_4
 +s_1\mathrm{Sq}^1\check{\mathcal O}_4
 +\omega_2\check{\mathcal O}_4)\cup_4\mathcal O^\psi_5+\omega_2\mathcal O^\psi_5,\\
\widehat M_7={}&\frac12M_7[\check{\mathcal O}_4;\omega_2,s_1]
 +\frac14\big[\widetilde{\omega_2}\,\beta\check{\mathcal O}_4
 +(\beta\check{\mathcal O}_4)\cup_3(\beta\check{\mathcal O}_4)\big],\\
R_7={}&\overline{\frac{
 d_{s_1}(16V_6+16\Theta_6)
 +8\widetilde{B^{\rm par}_7}+16\widehat M_7}{8}}.
\end{aligned}
```

Here $`\check{\mathcal O}_4`$ is closed, so its ordinary Bockstein is
defined. Every rational term in (S6), including $`\widehat M_7`$, is retained
as the exact displayed rational cochain during assembly. Form the whole
numerator defining $`R_7`$ over the integers, divide by eight, and only then
take parity. Its numerator is pointwise divisible by eight.

The required binary operation is

<a id="eq-s7"></a>

**(S7)**

```math
y_6[n_2;\omega_2,s_1]
 =(\mathsf h^{(3)}_6)^*R_7
 +\mathop{\mathrm{AW}}\nolimits^*Y^{\rm tot}_6.
```

For the first term use the three-factor grid (O11), ordered
$`(s_1,n_2,\omega_2)`$. On grid vertices $`(r_i,t_i,v_i)`$, pull $`s_1`$ along
$`r`$ and $`\omega_2`$ along $`v`$. Pull the integer field along $`t`$ with
first-vertex transport:

<a id="eq-s8"></a>

**(S8)**

```math
n_2^{\rm grid}(i_0i_1i_2)=(-1)^{s_1(r_{i_0},t_{i_0})}
 n_2(t_{i_0},t_{i_1},t_{i_2}).
```

Evaluate the entire expression (S6) on each pulled-back input and sum over
$`\mathsf h^{(3)}_6`$. This defines $`(\mathsf h^{(3)}_6)^*R_7`$.

The second term is the finite numerical polynomial specified in
[Coefficients](COEFFICIENTS.md#numerical-polynomial). It has eleven
tridegrees, uses explicit generalized integer binomials and first-vertex
transport, and contains no implicit primitive. That appendix prints every
coefficient, together with a lossless machine-readable copy.

The three-factor source operation here and the terminal product operation
assign fields differently to the same grid. Here $`s_1`$ and $`\omega_2`$
occupy separate factors; in the terminal product they share one background
factor. These assignments fix the coefficient transports.
