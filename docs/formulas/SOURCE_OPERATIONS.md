# Fixed operations in the terminal source

The terminal formulas use the finite operations $`T_6`$ and $`y_6`$ defined
here. Their degree-two integer argument is a physical field in
[4+1D](../FORMULA_GUIDE.md#four-dimensional-pair). In
[3+1D](../FORMULA_GUIDE.md#three-dimensional-pair), it is instead the
explicitly constructed interval or triangle field; it is not a physical
3+1D degree-two integer decoration. The degrees of all arguments in this
appendix are fixed, independently of those two uses.

The backgrounds are $`\omega_2,s_1`$, and a bar takes parity. In integer
arithmetic a binary field means its canonical value $`0,1`$. A bar around
a composite expression means: form that entire binary expression first,
then use its value $`0,1`$. In particular it cannot be replaced by the
unreduced sum of its integer-valued terms. The coefficient transports are
fixed in [Operations](OPERATIONS.md).

The shifted background is $`\check\omega_2=\omega_2+s_1\cup s_1`$ and the
closed degree-four source is
$`\check{\mathcal O}_4=\bar n_2^2+\check\omega_2\bar n_2`$.
The source $`\mathcal O^\psi_5`$, the residual $`B_4^\psi`$, and the
Pontryagin-square representative $`\mathcal P_{s_1}`$ have the definitions
in the guide. The Bocksteins $`\beta,\beta_{s_1},\beta^+`$ and finite cup
operations have the definitions in [Operations](OPERATIONS.md).

Only the following operations are named here:

| Operation | Purpose | Definition |
|---|---|---|
| $`M_7`$ | Binary degree-seven operation on a closed four-cochain, shared by the two constructions below | (S4) |
| $`T_6`$ | Its continuation to an open degree-three cochain by a fixed interval sum | (S5) |
| $`R_7`$ | The binary remainder evaluated on the three-factor grids | (S6) |
| $`y_6`$ | Integer-layer completion by the fixed grid and coefficient sums | (S7)–(S8) |

## Closed degree-four operation

For a closed binary four-cochain $`z`$, define

<a id="eq-s4"></a>

**(S4)**

```math
\begin{aligned}
M_7[z;\omega_2,s_1]={}&\mathop{\mathrm{MS}}\nolimits_{123134343}(\omega_2,\omega_2,z,z)
 +\sum_{\eta\in\mathcal W_4}\mathop{\mathrm{MS}}\nolimits_\eta(z,z,z,z)\\
&+(z\cup_2z)\cup_5(\omega_2z)
 +(z\cup_2z)\cup_5(s_1\overline{\beta z})\\
&+(\omega_2z)\cup_5(s_1\overline{\beta z})
 +\mathop{\mathrm{MS}}\nolimits_{123143434}(s_1,s_1,\overline{\beta z},\overline{\beta z})\\
&+(\omega_2\cup_1s_1)\overline{\beta z}
 +s_1(z\cup_2z)+s_1^2\overline{\beta^+z}.
\end{aligned}
```

All **453 words** of $`\mathcal W_4`$ are printed in
[Coefficients](COEFFICIENTS.md#adem-words). The subscript of the word set $`\mathcal W_4`$ is the input degree. No coefficient is fitted or chosen during evaluation.

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

Let $`n_2`$ be a twisted integer two-cocycle. No Majorana or
complex-fermion decoration is chosen in this construction. The following
formula replaces separate names for the rational pieces: assemble the
**entire integer numerator**, divide by eight, and then take parity.

<a id="eq-s6"></a>

**(S6)**

```math
\begin{aligned}
R_7=\frac18\Big\{&d_{s_1}\Big[
 4\big(\omega_2B_4^\psi+B_4^\psi\cup_2B_4^\psi
 +(\beta\check{\mathcal O}_4)\cup_3B_4^\psi
 -B_4^\psi\cup_3[(\beta_{s_1}\check\omega_2)n_2]\big)\\
&\qquad-4\overline{\left[\begin{gathered}\mathop{\mathrm{MS}}\nolimits_{12132434}
 (\overline{\beta_{s_1}\check\omega_2},\overline{\beta_{s_1}\check\omega_2},\bar n_2,\bar n_2)
 +\overline{\beta_{s_1}\check\omega_2}^{[1]}(\bar n_2\cup_1\bar n_2)\\{}+(s_1\overline{\beta_{s_1}\check\omega_2})\bar n_2^{[1]}
 +s_1(\overline{\beta_{s_1}\check\omega_2}\cup_1s_1)\bar n_2\end{gathered}\right]}\\
&\qquad+\mathcal P_{s_1}(\check\omega_2)n_2
 +2\check\omega_2n_2^2+4\omega_2\check{\mathcal O}_4
 +8\overline{\big[\check{\mathcal O}_4\cup_1(\overline{\beta\omega_2}+s_1\omega_2)\big]}\Big]\\
&+8\overline{\big[\mathcal O^\psi_5\cup_3\mathcal O^\psi_5
 +(\mathrm{Sq}^2\check{\mathcal O}_4+s_1\mathrm{Sq}^1\check{\mathcal O}_4
 +\omega_2\check{\mathcal O}_4)\cup_4\mathcal O^\psi_5
 +\omega_2\mathcal O^\psi_5\big]}\\
&+8M_7[\check{\mathcal O}_4;\omega_2,s_1]
 +4\big[\omega_2\beta\check{\mathcal O}_4
 +(\beta\check{\mathcal O}_4)\cup_3(\beta\check{\mathcal O}_4)\big]\Big\}
 \pmod2.
\end{aligned}
```

The numerator is pointwise divisible by eight. All operations inside the
outer braces are integer operations, including the differential on the
square bracket. Each barred subexpression supplies its canonical binary
value before that integer assembly. In particular no fraction is reduced
modulo one partway through the calculation. The ordinary Bockstein of
$`\check{\mathcal O}_4`$ is defined because that source is closed.

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
