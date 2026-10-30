# Integral first obstruction for the optional intrinsic 4+1D row

Date: 2026-10-15 UTC. This is separate research on an **enlarged** theory with intrinsic coordinate $r_0$. It is not a missing differential of the specified four-coordinate tower $(e_2,n_2,n_4,\nu_5)$, and it introduces no runtime operation. The subscript in $d_3$ is an AHSS page index, not a spacetime dimension.

## 1. Statement and exact scope

Take $s_1=r_1=0$: the symmetry is unitary and preserves charge. Its physical central-circle extension has class $\omega\in H^2(G,\mathbb R/\mathbb Z)$ and integral Bockstein

$$B=[d\omega_2^{\mathbb R}]\in H^3(G,\mathbb Z).$$

Use the interacting Spin-c phase spectrum, twisted by this charge gerbe. Any additional tangent twist must already be included in this symmetry identification; the theorem does not silently discard an independent twist. The intrinsic coefficient group is

$$A=\mathrm{TP}_5(\mathrm{Spin}^c)=\mathbb Z\{I,J\},\qquad
I=\frac{c^3-cp_1}{48},\quad J=\frac{c^3}{2}.$$

The target coefficient group is

$$C=\mathrm{TP}_3(\mathrm{Spin}^c)=\mathbb Z\{E_8,\mathrm{IQH}\},\qquad
E_8=-p_1/3,\quad \mathrm{IQH}=c^2/8-p_1/24.$$

Here $c$ is the determinant-line class, so a charge-one line changes $c$ by twice its Chern class. The target is ordered E8 first. In the repository's convention, fixed by the existing uniform-IQH equation $dn_2=-B_3n_0$, the first intrinsic obstruction is the **integral** operation

$$\boxed{\quad
\mathcal O^{\mathrm{intr}}_3(r_0^I,r_0^J)
=B_3\begin{pmatrix}0&3\\-1&-24\end{pmatrix}
\binom{r_0^I}{r_0^J}.
\quad}$$

Its cohomology class is the intrinsic $d_3$ in that convention. Thus the first completion equations in the enlarged model are

$$de_2=3B_3r_0^J,\qquad
dn_2=-B_3(r_0^I+24r_0^J).$$

This theorem determines the first obstruction from the added coefficient row $q=5$ to the E8/CI coefficient row $q=3$. It is distinct from the already supplied operation from a CI sheet $n_2$ to charge $n_4$. It neither changes the latter formula on closed sheets nor extends that formula to these newly open sheets without further work.

## 2. Why the normalization is integral

The charge gerbe acts on Spin-c structures by tensoring with a genuine line bundle. If $x$ is its first Chern class, the determinant class changes by

$$c\longmapsto c+2x.$$

To determine the resulting integral degree-two action on phase coefficients, take $S^2\times M^4$, give $S^2$ its spin structure with trivial determinant, and choose the twisting line with $\int_{S^2}x=1$. Since $x^2=0$, slanting the pulled-back response with $[S^2]$ gives

$$T(I)=\mathrm{IQH},\qquad
T(J)=24\,\mathrm{IQH}-3E_8.$$

This is an operation on integral phase classes, not differentiation of a rational polynomial followed by an unsupported torsion extrapolation. Its integer values can be measured on a primitive target basis. On $M=\mathbb{CP}^2$ with determinant $c=th$, $t=1,3$, one has

| Detector | $(E_8,\mathrm{IQH})$ | $(T(I),T(J))$ |
|---|---|---|
| $(\mathbb{CP}^2,c=h)$ | $(-1,0)$ | $(0,3)$ |
| $(\mathbb{CP}^2,c=3h)$ | $(-1,1)$ | $(1,27)$ |

The determinant of the target evaluation matrix is $-1$. These two manifolds therefore distinguish every integral target coefficient. There is no invisible torsion target: $\Omega_3^{\mathrm{Spin}^c}=0$ and $\Omega_4^{\mathrm{Spin}^c}=\mathbb Z^2$, so the relevant Anderson-dual coefficient is precisely the free integral dual lattice. Equivalently, direct evaluation on the six-manifolds gives

$$\int c^3=6t^2,\qquad \int cp_1=6,\qquad
(I,J)=((t^2-1)/8,3t^2),$$

which yields the same integer matrix without any division modulo torsion. The exact geometric calculations are independently reproduced in [check_intrinsic_line_action_4p1.py](check_intrinsic_line_action_4p1.py) and its [34-check result](check_intrinsic_line_action_4p1.json).

## 3. From line action to the universal integral transgression

The underlying integral geometry is the fiber sequence

$$K(\mathbb Z,2)\longrightarrow B\mathrm{Spin}^c
\longrightarrow BSO\xrightarrow{W_3}K(\mathbb Z,3).$$

Tensoring the Spin-c structure with a line is the indicated $K(\mathbb Z,2)$ action. It lifts to the Thom spectrum. A gerbe twist is formed by the associated bundle of spectra over the base; the phase theory is its fiberwise Anderson dual. These are integral constructions, valid for torsion as well as nontorsion gerbe classes.

Restrict the universal gerbe to a generating $S^3\to K(\mathbb Z,3)$. Trivialize it on the two hemispheres. Its clutching function on their equatorial $S^2$ is the generator of $\pi_2K(\mathbb Z,2)$, namely the line used in §2. Extending a constant intrinsic phase over this three-cell has obstruction given by the reduced coefficient of its clutching action. That reduced coefficient is exactly the integral map $T:A\to C$ computed above.

The universal base is 2-connected and

$$H^3(K(\mathbb Z,3);C)\cong C.$$

Consequently the clutching calculation determines the entire first universal obstruction, with no extra unsigned 2-primary term left undetected on that base. Pulling the universal construction back along the classifying map of $B$ gives $B\,T$ for every $B$, including a finite-group torsion Bockstein. This use of integral naturality is what was missing from the earlier purely rational characteristic-polynomial candidate.

The overall sign depends on the gerbe and Anderson-dual conventions. Here it is fixed by the already chosen lower equation: the same line action sends $\mathrm{IQH}$ to the unit-charge coefficient, while the repository uses $dn_2=-B_3n_0$. Therefore its obstruction convention is $-B\,T$. This gives the displayed E8-first matrix and agrees with the chosen formal convention $d_3c=-2B$; the latter is a consistency check, not the proof of integral normalization.

## 4. Cochain consequences at this first stage

Set $v(r)=(3r^J,-r^I-24r^J)$. A representative of the first obstruction is $B_3v(r)$. At this truncated stage, intrinsic coefficients and the two first completions add:

$$r_{\mathrm{out}}=r+r',\qquad
(e_2,n_2)_{\mathrm{out}}=(e_2,n_2)+(e'_2,n'_2).$$

The equations are exactly additive because $v$ is integral linear. Integer gauge changes $(e_2,n_2)\mapsto(e_2,n_2)+d(u_1,v_1)$ preserve them. A change of real extension lift $\omega_2^{\mathbb R}\mapsto\omega_2^{\mathbb R}+k_2$ changes $B_3$ by $dk_2$ and is transported at this stage by

$$ (e_2,n_2)\longmapsto(e_2,n_2)+k_2v(r).$$

There is no degree-minus-one gauge for $r_0$. These statements give a compatible first-stage representative and its additive/gauge behavior. They do not supply the remaining charge and phase completions or their stacking twisters in the enlarged theory.

For signed backgrounds, restricting to any subgroup on which both $s_1$ and $r_1$ vanish must recover this theorem. This is a rigorous constraint on a future signed formula. It does not determine possible sign-dependent torsion operations; replacing $B$ by a twisted Bockstein in the displayed matrix alone is not asserted to be the complete signed answer.

## 5. Provenance and boundary

The interacting coefficient groups and primitive response basis are recorded with primary provenance in [intrinsic_response.md](intrinsic_response.md). The new integral gerbe-action input is supported by Fei Han and Yuanchu Li, *Differential Models for the Anderson Dual to Twisted Spin-c-Bordism and a Twisted Anomaly Map*, [arXiv:2510.27286v2](https://arxiv.org/abs/2510.27286v2): cached source lines 1072–1093 give the fiber sequence, lifted action, and associated spectrum; lines 745–756 give the integral parametrized AHSS; lines 2174–2192 define the fiberwise Anderson dual; lines 2207–2217 give its integral Ext/Hom sequence. Their real coefficient action at lines 1514–1549 is a consistency check; the primitive integral detectors above provide the normalization used here.

Full TeX: `/home/arxiv/2510.27286_[_][c]_Differential_Models_for_the_Ander/arxiv_v2_0526.tex`, SHA256 `005d6b50cd3eef643d1d0d25610ff44705534fd75ddaf947f3602c368e910196`. The universal-geometry sourcing was independently reviewed; the geometric integer detector calculation was independently implemented. The deduction of the displayed obstruction is the argument in this note, not a claim that the cited paper prints this matrix.

The optional intrinsic row has further secondary and terminal questions after this first obstruction. They are not part of the user-specified four-coordinate theory and are not being used as blockers for completing that theory's $d_2,d_3,d_4$, stacking twisters, and gauges. No intrinsic operation is integrated into the runtime by this note.
