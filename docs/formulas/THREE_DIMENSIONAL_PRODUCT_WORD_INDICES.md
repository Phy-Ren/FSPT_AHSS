# Finite ordinary-word indices for the 3+1D product

This coefficient definition replaces the 24,935-row ordinary product
list by finite seed and index rules. Every final summand is a standard
normalized MS operation on physical cochains. The temporary labels below
belong only to the coefficient grammar. They are not cochains on an
auxiliary space and are erased before evaluating the physical formula.

## Physical sums and ordinary word arithmetic

The lower half-valued polynomial is the ordinary sum with indices

```math
\begin{aligned}
\mathcal I_4={}&\mathcal I_T+\mathcal I_{\rm other}
 +\mathcal I_q+\mathcal I_{\rm CF}
 +{s_1}^2[{\check n_2}\cup_2({\bar n_1}{\bar n'_1})]\\
&+{s_1}{\mathcal{ℰ}_3}+H_4[{\check N_2}]+H_4[{\check n_2}]+H_4[{\check n'_2}]+P_4[{\check N_2},{\mathcal{ℰ}_3}]
 +dH_3^{\rm pure}[{\check n_2},{\check n'_2}]\\
&+{\mathcal{𝒪}_4}\cup_4{\mathcal{𝒪}_4}'+{\mathcal{ℰ}_3}\cup_3{\mathcal{𝒪}_4}^{\rm out}
 +\mathcal I_{4,F}.
\end{aligned}
```

Here additions denote symmetric differences of ordinary-word index lists;
the products and derivatives generate ordinary words as specified below.
The lower output and full CF obstruction inputs are

```math
\begin{aligned}
\check N_2&=\check n_2+\check n'_2+\bar n_1\bar n'_1,\\
\mathcal{𝒪}_4&=(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[\check n_2]
                  +\mathcal{𝒪}_4^\psi[n_1],\\
\mathcal{𝒪}'_4&=(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[\check n'_2]
                  +\mathcal{𝒪}_4^\psi[n'_1],\\
\mathcal{𝒪}^{\rm out}_4&=(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[\check N_2]
                  +\mathcal{𝒪}_4^\psi[n_1+n'_1].
\end{aligned}
```

The set $`\mathcal I_{4,F}`$ is the explicitly printed 58-word lower table in
[the relative-word table](THREE_DIMENSIONAL_PRODUCT_CF_WORDS.md). Its obstruction inputs are the full indicated
physical lower obstructions. $`H_4`$ and $`P_4`$ have respectively the nine and
eight ordinary terms printed in [the stacking formulas](THREE_DIMENSIONAL.md#eq-t3b). Thus they are fixed
finite phase polynomials, not evaluators with hidden instructions.

An entry is a surjection word with ordered physical input labels. Equal
entries cancel modulo two. Adjacent equal letters give zero. Normalize
labels by order of first occurrence, and discard degree-impossible
interval cuts. To replace a slot occurring r times by an L-letter word,
choose all integers

```math
0\le t_1\le\cdots\le t_{r-1}\le L-1
```

and insert its successive inclusive substrings
`[0,t1],[t1,t2],...,[t(r-1),L-1]`. Relabel the inserted slots distinctly,
sum all choices, and normalize. This completely specifies composition.
A cup-i seed is the alternating word with i+2 letters. A differential
deletes each letter occurrence whose label still remains elsewhere, and
differentiates each input by the stated lower law. A Steenrod square
includes its derivative term. Words with labels above9 are comma-separated
integer sequences, never concatenated ambiguous decimal strings.

## Two-crossing index selection

The three formal degree-one markers are denoted L,R,D. No cochain is
assigned to any of them. After expanding a seed, retain a word only if:

1. Exactly two marker input slots occur once. Their types are respectively
   L and R, with the L occurrence before the R occurrence.
2. Every other marker input slot occurs exactly twice.
3. Let the positions before L, between L and R, and after R have labels
   0,1,2. The two appearances of any repeated marker lie in one of the
   following ordered region pairs:

| Marker type | Allowed region pairs |
|---|---|
| L | (0,1),(0,2) |
| R | (0,2),(1,2) |
| D | (0,2) |

Erase all marker letters and marker input slots and normalize the remaining
ordinary word. This finite index rule is denoted S2 below. The notation
never appears in the physical formula; it only specifies which standard
MS indices occur.

For the single-marker rule S1, use L alone. Scan until every marker input
slot has appeared once, rejecting a word with a marked repeat before that
point. Delete earlier marked letters. Require every marker slot now to
occur once, then erase all marker slots and normalize.

One more index rearrangement, C, is used in a seed below. Color marker
slots zero and physical slots one. For each occurrence j of a color-one
label in a word `p j t`, form `p j t0 j t1`, with `t0,t1` the respective
colored subwords of the tail in their original order. Sum and normalize.
This is an explicit operation on integer index words, not on fields.

## Common finite seeds

For this coefficient definition only, put

```math
\begin{aligned}
X&=L{\bar n_1}+R{\bar n'_1},\\
H&=L{\widetilde n_1}+R{\widetilde n'_1}+({s_1}\cup_1L){\bar n_1}+({s_1}\cup_1R){\bar n'_1}+D({\bar n_1}\cup_1{\bar n'_1}),\\
V&=L{\check n_2}+R{\check n'_2}+\mathop{\mathrm{MS}}\nolimits_{1213}({\check\omega_2},L,{\bar n_1})
              +\mathop{\mathrm{MS}}\nolimits_{1213}({\check\omega_2},R,{\bar n'_1})
              +D({\bar n_1}{\bar n'_1})+\mathop{\mathrm{MS}}\nolimits_{12324}(L,{\bar n_1},R,{\bar n'_1}),\\
A&=\mathop{\mathrm{MS}}\nolimits_{1234}(L,{\bar n_1},R,{\bar n'_1})+{\check\omega_2}L{\bar n_1}+{\check\omega_2}R{\bar n'_1},\\
K&=HX+XH+({s_1}\cup_1X)X+{\check\omega_2}H+({s_1}\cup_1{\check\omega_2})X+X^2\cup_4({\check\omega_2}X),\\
\Xi&=\mathop{\mathrm{MS}}\nolimits_{1231343}({\check\omega_2},{\check\omega_2},X,X)
 +\mathop{\mathrm{MS}}\nolimits_{1231343}(X,X,X,X)+X^2\cup_3({\check\omega_2}X)\\
&\quad+H[(X\cup_1X)+{s_1}X]+(X\cup_1X)\cup_1({s_1}X)\\
&\quad+{s_1}[X^2\cup_4({\check\omega_2}X)+(X\cup_1{s_1})X+X\cup_1(X\cup_1X)+X^2]\\
&\quad+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2})H
 +[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})]X,\\
J&=V\cup_1V+V\cup_2A+{\omega_2}V+{s_1}(V\cup_2V+V\cup_3A)+\Xi.
\end{aligned}
```

These are finite word seeds of fixed graded input types. `A` is the legal
differential of the seed V; the equality is used before expansion and
includes both p+ip input branches and the actual lower stacking carry.
The background and low-field differential rules are

```math
d{\check n_2}={\check\omega_2}{\bar n_1},\quad d{\check n'_2}={\check\omega_2}{\bar n'_1},\quad d{\widetilde n_1}={\bar n_1}^2+{s_1}{\bar n_1},\quad d{\widetilde n'_1}={\bar n'_1}^2+{s_1}{\bar n'_1},
\quad dD=LR,
\quad d{\bar n_1}=d{\bar n'_1}=d{\check\omega_2}=d{\omega_2}=d{s_1}=dL=dR=0.
```

### Majorana and two additional source blocks

Use the completely stated universal T word grammar in
[the Majorana seed indices](THREE_DIMENSIONAL_WORD_INDICES.md#the-majorana-seed-indices). Its only numerical input is the existing 453-word Adem table.
Keep its 1,176 ordinary words in the four formal arguments $`y,dy,\omega_2,s_1`$,
after replacing Bockstein parities by the stated cochain Sq1 expressions
and separating the single second-carry term. Substitute `y=V,dy=A` and
apply S2. This is `I_T`; it has 13,288 ordinary physical indices. The exact
separated carry is the already displayed $`s_1^2[\check n_2\cup_2(\bar n_1\bar n'_1)]`$, and must not be
added a second time.

The two remaining source blocks have the short combined index seed

```math
\mathcal I_{\rm other}
 =S2\left[(J+\Xi)\cup_4\Xi
 +(V\cup_2V+V\cup_3A)\cup_2K
 +{s_1}((V\cup_2V+V\cup_3A)\cup_3K)\right].
```

The respective terms have 1,413 and 375 physical indices. The omitted
possible term $`V(\mathrm{Sq}^1\omega_2+s_1\omega_2)`$ has no allowed S2 index, identically.

### CF block

The small low-degree seed polynomials required here are

```math
\begin{aligned}
D_3({\bar n_1},{\widetilde n_1},{\check n_2})&={\check\omega_2}{\widetilde n_1}+{\check n_2}\cup_2({\check\omega_2}{\bar n_1})+({s_1}\cup_1{\omega_2}){\bar n_1},\\
g_2&={\widetilde n_1}{\bar n'_1}+({\bar n_1}+{\widetilde n_1}){\widetilde n'_1}+({\bar n_1}{\bar n'_1})\cup_2({\check n_2}+{\check n'_2})+{\bar n_1}{\bar n'_1}\\
&\quad+({s_1}\cup_1{\bar n_1})({\bar n_1}\cup_1{\bar n'_1})
 +({s_1}\cup_1({\bar n_1}\cup_1{\bar n'_1}))({\bar n_1}+{\bar n'_1}),\\
G&=C(J)+LD_3({\bar n_1},{\widetilde n_1},{\check n_2})+RD_3({\bar n'_1},{\widetilde n'_1},{\check n'_2})\\
&\quad+D\big[{\mathcal{ℰ}_3}+D_3({\bar n_1}+{\bar n'_1},{\widetilde n_1}+{\widetilde n'_1}+{\bar n_1}\cup_1{\bar n'_1},{\check N_2})
                 +D_3({\bar n_1},{\widetilde n_1},{\check n_2})+D_3({\bar n'_1},{\widetilde n'_1},{\check n'_2})\big]+LRg_2,\\
dG&=J+L{\mathcal{𝒪}_4}+R{\mathcal{𝒪}_4}'.
\end{aligned}
```

For the one-input phase, retain only the unprimed terms with the marker L
in the common seeds: delete terms containing R or D and all primed inputs.
Then use the displayed J with those reduced seeds. The binary phase numerator is

```math
f_{c,*}({\bar n_1},{\widetilde n_1},{\check n_2},n_3)
 =S1\big[(C(J)+LD_3({\bar n_1},{\widetilde n_1},{\check n_2}))\cup_3(Ln_3)
       +(J+L\mathcal{𝒪}_4[n_1,{\check n_2}])\cup_4(Ln_3)\big].
```

Every coefficient of this ordinary degree-four phase is fixed by these
word rules. In the product set use only the low-source field indicated
by the substituted physical arguments. Then

```math
\mathcal I_{\rm CF}
 =S2[G\cup_2G+G\cup_3dG+{\omega_2}G+dG\cup_4(L{\mathcal{𝒪}_4}+R{\mathcal{𝒪}_4}')]
   +f_{c,*}({\bar n_1}+{\bar n'_1},{\widetilde n_1}+{\widetilde n'_1}+{\bar n_1}\cup_1{\bar n'_1},{\check N_2},{\mathcal{ℰ}_3}).
```

This generates exactly 9,162 physical indices. The five-word intrinsic
output gauge and eight-word P bridge have already been applied in the
relative CF tables; adding either a second time would change the product.

### Quarter-polarization half block

Only for these finite seeds, write $`\bar B_3`$, $`\bar B'_3`$, and $`\alpha=\overline{\beta_{s_1}\check\omega_2}`$. They are existing integral residuals reduced modulo
two, not new fields. Use $`d\bar B_3=\alpha\bar n_1,\ d\bar B'_3=\alpha\bar n'_1`$. Define

```math
\begin{aligned}
x&=L{\check n_2},\\
y&=R{\check n'_2},\\
z&=D({\bar n_1}{\bar n'_1}),\\
q_L&=\mathop{\mathrm{MS}}\nolimits_{1213}({\check\omega_2},L,{\bar n_1}),\\
q_R&=\mathop{\mathrm{MS}}\nolimits_{1213}({\check\omega_2},R,{\bar n'_1}),\\
q_N&=\mathop{\mathrm{MS}}\nolimits_{12324}(L,{\bar n_1},R,{\bar n'_1}),\\
Q(p,{\bar n_1},{\widetilde n_1})&=({\check\omega_2}\cup_1p){\widetilde n_1}+[({s_1}\cup_1{\check\omega_2})\cup_1p]{\bar n_1},\\
\bar\lambda_2^\psi&={\widetilde n_1}{\bar n'_1}+{\bar n_1}{\widetilde n'_1}+({s_1}\cup_1{\bar n_1}){\bar n'_1},\\
R_q&=\sum_{i\lt j}x_i\cup_3x_j+D\bar\lambda_2^\psi
 +Q(L,{\bar n_1},{\widetilde n_1})+Q(R,{\bar n'_1},{\widetilde n'_1})+({\check\omega_2}\cup_1D)({\bar n_1}\cup_1{\bar n'_1})\\
&\quad+q_L\cup_3q_N+q_R\cup_3q_N
 +(LR\cup_2{\check\omega_2})({\bar n_1}\cup_1{\bar n'_1})\\
&\quad+L[({\widetilde n_1}\cup_1R){\bar n'_1}+({\bar n_1}\cup_1R){\widetilde n'_1}+(({s_1}\cup_1{\bar n_1})\cup_1R){\bar n'_1}],
\qquad (x_1,x_2,x_3,x_4)=(x,y,z,q_L+q_R+q_N),\\
C_q&=L\bar B_3+R\bar B'_3,\qquad
Z=(\alpha\cup_1L){\bar n_1}+(\alpha\cup_1R){\bar n'_1},
\qquad\eta=dR_q+Z.
\end{aligned}
```

Differentiate every seed by the word boundary and displayed input laws.
The bulk indices are

```math
\begin{aligned}
I_{q,2}=S2[&C_q\cup_2\eta+dC_q\cup_3\eta
 +R_q\cup_1dR_q+R_q^2+(\mathrm{Sq}^1{\omega_2})R_q
 +Z\cup_2dR_q+dZ\cup_3dR_q]\\
 +{s_1}S2[&C_q\cup_3\eta+dC_q\cup_4\eta
 +R_q\cup_1R_q+R_q\cup_2dR_q+{\omega_2}R_q
 +Z\cup_3dR_q+dZ\cup_4dR_q].
\end{aligned}
```

For the edge indices set, in binary word arithmetic only,

```math
\begin{aligned}
\lambda&={\check n_2}\cup_2{\check n'_2}+({\check n_2}+{\check n'_2})\cup_2({\bar n_1}{\bar n'_1})+\bar\lambda_2^\psi,\quad B=\bar B_3+\bar B'_3,\\
R_{\rm edge}&=(L{\check N_2})\cup_3\mathop{\mathrm{MS}}\nolimits_{1213}({\check\omega_2},L,{\bar n_1}+{\bar n'_1})
       +Q(L,{\bar n_1}+{\bar n'_1},{\widetilde n_1}+{\widetilde n'_1}+{\bar n_1}\cup_1{\bar n'_1})+L\lambda,\\
Z_{\rm edge}&=(\alpha\cup_1L)({\bar n_1}+{\bar n'_1}),\qquad S=L\lambda.
\end{aligned}
```

The remaining indices and the full quarter-polarization half set are

```math
\begin{aligned}
I_{q,1}={}&B\cup_1\lambda+\lambda\cup_1B+\lambda^2
 +\lambda\cup_1d\lambda+\lambda\cup_2dB\\
&+{s_1}[\lambda\cup_2B+B\cup_2\lambda+\lambda\cup_2d\lambda]\\
&+S1[S\cup_2dR_{\rm edge}+R_{\rm edge}\cup_1S+Z_{\rm edge}\cup_3dS]\\
&+{s_1}S1[S\cup_3dR_{\rm edge}+R_{\rm edge}\cup_2S+Z_{\rm edge}\cup_4dS],\\
\mathcal I_q={}&I_{q,2}+I_{q,1}.
\end{aligned}
```

There are 289 bulk and 1,076 edge indices, with 1,237 in their symmetric
difference. The even integer terms of the quarter polarization have
therefore been retained explicitly in the half coefficient block.

## Accepted-Majorana bridge and physical origin labels

The ten-word polynomial whose derivative occurs in $`\mathcal I_4`$ is

```math
\begin{aligned}
H_3^{\rm pure}[{\check n_2},{\check n'_2}]={}&\mathop{\mathrm{MS}}\nolimits_{1231213}({\check n_2},{\check n'_2},\mathrm{Sq}^1{\check n'_2})
 +\mathop{\mathrm{MS}}\nolimits_{12312312}({\check n_2},\mathrm{Sq}^1{\check n'_2},\mathrm{Sq}^1{\check n'_2})\\
&+(\mathop{\mathrm{MS}}\nolimits_{123412431}+\mathop{\mathrm{MS}}\nolimits_{124314324})({\check n_2},{\check n_2},{\check n_2},{\check n'_2})\\
&+(\mathop{\mathrm{MS}}\nolimits_{123242314}+\mathop{\mathrm{MS}}\nolimits_{123413421}
  +\mathop{\mathrm{MS}}\nolimits_{132421324}+\mathop{\mathrm{MS}}\nolimits_{134213124}
  +\mathop{\mathrm{MS}}\nolimits_{314324312})({\check n_2},{\check n_2},{\check n'_2},{\check n'_2})\\
&+\mathop{\mathrm{MS}}\nolimits_{121341234}({\check n_2},{\check n'_2},{\check n'_2},{\check n'_2}).
\end{aligned}
```

The labels psi and not-psi are attached to ordinary **input choices before
word composition**. In each occurrence choose the actual lower-function
summands

```math
\begin{aligned}
B_3&=\beta^\circ {\check n_2}+B_3^\psi,&
B'_3&=\beta^\circ {\check n'_2}+B_3^{\psi\prime},\\
{\mathcal{𝒪}_4}&=(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[{\check n_2}]+\mathcal{𝒪}_4^\psi[n_1],&
{\mathcal{𝒪}_4}'&=(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[{\check n'_2}]+\mathcal{𝒪}_4^\psi[n'_1],\\
{\mathcal{ℰ}_3}&=\mathcal{ℰ}_3^\gamma+\mathcal{ℰ}_3^{\gamma\psi}+\mathcal{ℰ}_3^\psi,&
{\check N_2}&={\check n_2}+{\check n'_2}+{\bar n_1}{\bar n'_1}.
\end{aligned}
```

The all-p+ip choice has no incoming Majorana decoration or its integer
Bockstein. It retains the induced output
$`\check N_2=\bar n_1\bar n'_1`$ and its differential and Sq operations.
Choose $`\mathcal{𝒪}_4=\mathcal{𝒪}_4^\psi[n_1]`$, its primed counterpart,
and $`\mathcal{ℰ}_3=\mathcal{ℰ}_3^\psi`$. In the output obstruction retain
$`(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[\bar n_1\bar n'_1]
+\mathcal{𝒪}_4^\psi[n_1+n'_1]`$.
Apply these same choices to each displayed source and output phase,
including $`H_4[\bar n_1\bar n'_1]`$ and
$`P_4[\bar n_1\bar n'_1,\mathcal{ℰ}_3^\psi]`$.
The full characteristic derivative is replaced by its legal pure-integer
source before selecting its summands.

These choices define $`\mathcal I_{4,\psi}`$; all other choices define $`\mathcal I_{4,\neg\psi}`$.
They are taken in formal ordinary cochain expressions, not by setting
illegal root-face variables to zero. The accepted gamma half polynomial
is then added to the relative mixed part and displayed positively as the
intrinsic gamma part; their identical binary copies cancel in the total.
The exact paired bridge proves that the relative mixed *phase* vanishes
on the closed-Majorana tower, including its quarter terms. A term inside
one displayed coefficient bracket need not vanish independently.

The pure word set comprises the 8,593 ordinary indices plus

```math
\mathcal{𝒪}_4^\psi[n_1]\cup_4\mathcal{𝒪}_4^\psi[n'_1]
+\mathcal{ℰ}_3^\psi\cup_3[
  (\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[{\bar n_1}{\bar n'_1}]+\mathcal{𝒪}_4^\psi[n_1+n'_1]].
```

All 58 F-table entries retain incoming Majorana inputs, so none supplies an
additional pure choice. This zero is a literal formal-word check.

## Intrinsic Majorana completion

For binary degree-two arguments $`x,y`$, with canonical integer carries
$`\beta^\circ x,\beta^\circ y`$, the required ordinary formula is

```math
\begin{aligned}
z^0_4(x,y)={}&\sum_{v\in\mathcal V_4}\mathop{\mathrm{MS}}\nolimits_v(x,x,y,y)
 +\mathop{\mathrm{MS}}\nolimits_{12123}(x+y,y,x\cup_2y)
 +\mathop{\mathrm{MS}}\nolimits_{123131}(y,x,x\cup_1y)\\
&+(x\cup_1y)\cup_1y
 +(\overline{\beta^\circ x}+\overline{\beta^\circ y})\cup_1(x\cup_2y)\\
&+(x\cup_2y)\cup_1
  (\overline{\beta^\circ x}+\overline{\beta^\circ y}+y\cup_1x)\\
&+(x\cup_1y)\cup_3(x^2+y^2)
 +y\cup_2[x\cup_1(x\cup_1y)]
 +\overline{\beta^\circ y}\cup_2\overline{\beta^\circ x},\\
\mathcal V_4={}&\{12123434,12134131,12314324,12314342,
                13242412,13413142,13432412\}.
\end{aligned}
```

This is the finite degree-two specialization of the standard word formula.
The open continuation is fixed explicitly by the displayed integer carry.
