# The closed Majorana diagonal in 4+1D

For $`d\check n_3=0`$, the Majorana self-stacking phase has the following
representative. Its explicit relation to the complete open formula is
given below.

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_{5,\mathrm{diag}}^\gamma
={}&\frac12\Big[
 \sum_{\vartheta\in\mathcal W}
  \mathop{\mathrm{MS}}\nolimits_{\vartheta}
       (\check n_3,\check n_3,\check n_3,\check n_3)\\
&\quad+\mathop{\mathrm{MS}}\nolimits_{12313123}
       (\check n_3,\check n_3,\mathrm{Sq}^1\check n_3)
 +\mathop{\mathrm{MS}}\nolimits_{12131232}
       (\mathrm{Sq}^1\check n_3,\check n_3,\check n_3)\\
&\quad+\check n_3\cup_2\mathrm{Sq}^1\check n_3
 +\check n_3\cup_3
       (\check n_3\cup_2\mathrm{Sq}^1\check n_3)\\
&\quad+\mathrm{Sq}^1\check n_3\cup_3
               \mathcal{ℰ}_4^\gamma[\check n_3,\check n_3]
 +(\omega_2\cup_1s_1)\check n_3
 +s_1\big[(s_1\check n_3)\cup_3\check n_3\big]\Big]\\
&+\frac14\Big[
 B_4^\gamma\cup_3B_4^\gamma
 +\check n_3\cup_1\check n_3
 -\overline{\check n_3\cup_1\check n_3}
 -s_1\mathrm{Sq}^1\check n_3
 -\overline{\mathcal{𝒪}_5^\gamma[\check n_3]}
 \Big]\pmod1.
\end{aligned}
```

The lower obstruction and lower self-stacking correction retain their
existing meanings:

```math
\begin{aligned}
B_4^\gamma&=\beta\check n_3,
&\overline{B_4^\gamma}&=\mathrm{Sq}^1\check n_3,\\
\mathcal{𝒪}_5^\gamma[\check n_3]
 &=\mathrm{Sq}^2\check n_3+\omega_2\check n_3
                       +s_1\mathrm{Sq}^1\check n_3,\\
\mathcal{ℰ}_4^\gamma[\check n_3,\check n_3]
 &=\mathrm{Sq}^1\check n_3+s_1\check n_3.
\end{aligned}
```

The first sum contains **sixteen MS terms**, with the following complete
word list. Every word has the same four arguments printed in the formula.

```text
12131432412  12343213431  23412342324  12123434123
12131412324  12134131234  12312412423  12314324123
12314342413  13242412314  13412321341  13412321413
13413142134  13432412314  31214124324  12413432312
```

There are **23 half-valued terms and five quarter-valued terms**, hence
**28 terms** with the defined lower operations retained. This small formula
is the closed diagonal specialization; the general open two-input law is
[given separately](FOUR_DIMENSIONAL.md).

In the quarter bracket, the unbarred
$`\check n_3\cup_1\check n_3`$ is the signed integer cup of canonical input
values. Its barred counterpart is the canonical value of the **whole**
binary operation. Their difference is even but can be nonzero modulo four.
The whole bar on $`\mathcal{𝒪}_5^\gamma`$ is required for the same reason.

## Explicit output gauge

The relation to the existing complete representative is exact:

```math
\widehat{\mathcal{ℰ}}_5^\gamma[\check n_3,\check n_3]
=\widehat{\mathcal{ℰ}}_{5,\mathrm{diag}}^\gamma
 +d_{s_1}\frac{K_4^\gamma[\check n_3]}2.
```

The binary gauge primitive has only three face products:

```math
\begin{aligned}
(K_4^\gamma[\check n_3])_{01234}
={}&(\check n_3)_{0123}(\check n_3)_{0134}\\
&+(\check n_3)_{0124}(\check n_3)_{0134}(\check n_3)_{0234}\\
&+(\check n_3)_{0123}(\check n_3)_{0124}
              (\check n_3)_{0134}(\check n_3)_{0234}.
\end{aligned}
```

Adding this output bosonic coboundary gives the complete representative;
subtracting it gives the 28-term representative. The obstruction is
unchanged. The primitive is normalized, and
$`d_{s_1}(K_4^\gamma/2)=dK_4^\gamma/2\pmod1`$.

The equality was proved by complete binary coefficient comparison and
checked independently against the frozen complete phase and its explicit
gauge. The final lower-operation expression passes 1,024 closed-input
checks. No closed-input restriction has been imposed on the separate
complete two-input formula.
