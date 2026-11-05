# Closed Majorana obstructions and stacking twisters

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

Read the complete section for the physical dimension:
[2+1D](#majorana-2d), [3+1D](#majorana-3d), or [4+1D](#majorana-4d).
The [1+1D fMPS endpoint](#fmps-1d) is stated separately.
Each section presents all obstruction functions first, followed by all
stacking twisters. There is no integer decoration in this appendix.

The superscripts follow the manuscript's operator factorization:
$`c`$ labels the complex-fermion part, $`\gamma`$ the Majorana part, and
$`c\gamma`$ their mixed part. They label contributions, not additional
cochains. In particular, $`dn_j`$ in a mixed term is fixed by the lower
obstruction equation of that dimension.

## Arithmetic and operations

Use the [common notation](../FORMULA_GUIDE.md#conventions-and-coordinates).
Lower-layer equations and half-valued brackets are binary. In integer
expressions, each named binary cochain means its canonical zero-or-one
representative; sums, differentials, and cups are then integral.
An outer $`[\cdot]_2`$ first reduces the entire indicated expression modulo two.
Thus an integer $`x\cup_i y`$ and $`[x\cup_i y]_2`$ are different
operations in a quarter-valued phase. Their complete evaluation rules are
in [Operations](OPERATIONS.md#arithmetic-and-carries).

The Bockstein $`\beta`$, its second carry $`\beta^+`$, and their signed
products have untwisted integer coefficients here. The phase instead has
coefficients $`(\mathbb R/\mathbb Z)_{s_1}`$ and differential $`d_{s_1}`$.
A phase and its additive value use the same symbol, as in the common notation above.
A prime denotes the second input, and $`N_j`$ the stacked binary field.
The lower fields and all subscripts are fixed anew
at the start of each dimensional section.

The formulas below use the operator ordering of the complex fermions.

<a id="majorana-2d"></a>
## 2+1D

The physical fields are the binary Majorana cochain $`n_1`$,
the binary complex-fermion cochain $`n_2`$, and the phase $`\nu_3`$.

### Obstruction functions

#### Majorana obstruction

<a id="eq-m2-majorana-2d"></a>

**(M2γ, 2+1D)**

{{equation:majorana-and-endpoints--majorana-obstruction--1}}

#### Complex-fermion obstruction

<a id="eq-m2-2d"></a>

**(M2, 2+1D)**

{{equation:majorana-and-endpoints--complex-fermion-obstruction--2}}

##### Majorana contribution

<a id="eq-m2-gamma-2d"></a>

**(M2γ→c, 2+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--3}}

#### Bosonic obstruction

<a id="eq-m3-2d"></a>

**(M3, 2+1D: obstruction)**

{{equation:majorana-and-endpoints--bosonic-obstruction--4}}

##### Complex-fermion contribution

<a id="eq-m3-c-2d"></a>

**(M3c, 2+1D)**

{{equation:majorana-and-endpoints--complex-fermion-contribution--5}}

##### Complex-fermion–Majorana contribution

<a id="eq-m3-cgamma-2d"></a>

**(M3cγ, 2+1D)**

{{equation:majorana-and-endpoints--complex-fermion-majorana-contribution--6}}

##### Majorana contribution

<a id="eq-m6"></a>

**(M6, 2+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--7}}

### Stacking twisters

#### Majorana stacking

<a id="eq-m1-2d"></a>

**(M1γ, 2+1D)**

{{equation:majorana-and-endpoints--majorana-stacking--8}}

There is no stacking correction in this layer.

#### Complex-fermion stacking

<a id="eq-m1-fermion-2d"></a>

**(M1c, 2+1D)**

{{equation:majorana-and-endpoints--complex-fermion-stacking--9}}

##### Majorana contribution

<a id="eq-m1-gamma-2d"></a>

**(M1γ→c, 2+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--10}}

#### Bosonic stacking

<a id="eq-m3-stacking-2d"></a>

**(M3E, 2+1D)**

{{equation:majorana-and-endpoints--bosonic-stacking--11}}

##### Complex-fermion contribution

<a id="eq-m3-stacking-c-2d"></a>

**(M3Ec, 2+1D)**

{{equation:majorana-and-endpoints--complex-fermion-contribution--12}}

##### Complex-fermion–Majorana contribution

<a id="eq-m3-stacking-cgamma-2d"></a>

**(M3Ecγ, 2+1D)**

{{equation:majorana-and-endpoints--complex-fermion-majorana-contribution--13}}

##### Majorana contribution

<a id="eq-m11"></a>

**(M11, 2+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--14}}

The reduction modulo two inside $`\Delta[[n_1^3]_2]`$ and the reduction modulo two of
$`[s_1n_1n'_1]_2`$ reduce each complete indicated product. The
$`\Delta`$ in the mixed half-valued contribution is binary; in the
eighth-valued contribution it subtracts the complete integer lifts. In contrast, $`n_1\cup_1n'_1`$ in the
quarter-valued bracket is a signed integer cup; its differential is also
integral.

This twister is the Majorana stacking law of the fixed-point lattice
construction, with the forward and inverse moves of the
[phase convention](../FORMULA_GUIDE.md#phase-convention). Its antiunitary
quarter term is $`-\frac14[s_1n_1n'_1]_2`$.

The binary antiunitary term is

<a id="eq-m10"></a>

**(M10, 2+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--15}}

### Chiral domain

These formulas compute the zero-integer fiber. For split unitary symmetry
($`\omega_2=s_1=0`$), an independent neutral chiral $`\mathbb Z`$ factor can
be adjoined. For the two nonsplit unitary controls in the example catalog,
the finite subgroup and its abstract infinite-cyclic completion are
reported separately; a marked minimal chiral generator is not specified.
The endpoint formulas do not cover general nonsplit nonzero-chiral cochain
inputs.

<a id="majorana-3d"></a>
## 3+1D

These formulas are written in the physical point-fermion occupation $`n_3`$
of the original geometric Majorana pairing, with the lattice sign of the
Majorana phase: they are the hand-written closed-sector formulas, with the
local stacking rephasing of the layer-combining move absorbed. The lower
parity and its product coincide pointwise with the restriction of
[the full reference](THREE_DIMENSIONAL.md). The terminal phase of that
reference is instead written in $`\widetilde{n}_3=n_3+n_2\cup_1n_2`$, where the
quarter-valued Majorana terms have the opposite sign; the explicit
[bridging identity and dictionary](THREE_DIMENSIONAL.md#closed-sector-bridging-identity)
relate the two forms. The microscopic ordinary modes and the original
projection schedule are unchanged.

The physical fields are the binary Majorana cochain $`n_2`$,
the binary complex-fermion cochain $`n_3`$, and the phase $`\nu_4`$.

### Obstruction functions

#### Majorana obstruction

<a id="eq-m2-majorana"></a>

**(M2γ, 3+1D)**

{{equation:majorana-and-endpoints--majorana-obstruction--16}}

#### Complex-fermion obstruction

<a id="eq-m2"></a>

**(M2, 3+1D)**

{{equation:majorana-and-endpoints--complex-fermion-obstruction--17}}

##### Majorana contribution

<a id="eq-m2-gamma"></a>

**(M2γ→c, 3+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--18}}

#### Bosonic obstruction

<a id="eq-m3"></a>

**(M3, 3+1D: obstruction)**

{{equation:majorana-and-endpoints--bosonic-obstruction--19}}

##### Complex-fermion contribution

<a id="eq-m3-c"></a>

**(M3c, 3+1D)**

{{equation:majorana-and-endpoints--complex-fermion-contribution--20}}

##### Complex-fermion–Majorana contribution

<a id="eq-m3-cgamma"></a>

**(M3cγ, 3+1D)**

{{equation:majorana-and-endpoints--complex-fermion-majorana-contribution--21}}

##### Majorana contribution

<a id="eq-m4"></a>

**(M4, 3+1D)**

This is the pure Majorana polynomial of the complete 3+1D tower at
$`n_1=0`$, where $`\widetilde{n}_2=n_2`$ and $`\beta^- n_2=\beta n_2`$, with the
lattice sign of the quarter bracket appropriate to the physical occupation
$`n_3`$:

{{equation:majorana-and-endpoints--majorana-contribution--22}}

Its word operations are

{{equation:three-dimensional--majorana-decoration--15}}

The intrinsic Adem cochain of a binary two-cochain $`x`$ is

<a id="eq-m5"></a>

**(M5, 3+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--24}}

### Stacking twisters

#### Majorana stacking

<a id="eq-m1"></a>

**(M1γ, 3+1D)**

{{equation:four-dimensional--1-p-ip-stacking--19}}

There is no stacking correction in this layer.

#### Complex-fermion stacking

<a id="eq-m1-fermion"></a>

**(M1c, 3+1D)**

{{equation:majorana-and-endpoints--complex-fermion-stacking--25}}

##### Majorana contribution

<a id="eq-m1-gamma"></a>

**(M1γ→c, 3+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--26}}

#### Bosonic stacking

<a id="eq-m3-stacking"></a>

**(M3E, 3+1D)**

{{equation:majorana-and-endpoints--bosonic-stacking--27}}

##### Complex-fermion contribution

<a id="eq-m3-stacking-c"></a>

**(M3Ec, 3+1D)**

{{equation:majorana-and-endpoints--complex-fermion-contribution--23}}

##### Complex-fermion–Majorana contribution

<a id="eq-m3-stacking-cgamma"></a>

**(M3Ecγ, 3+1D)**

{{equation:majorana-and-endpoints--complex-fermion-majorana-contribution--29}}

##### Majorana contribution

<a id="eq-m7"></a>

**(M7, 3+1D)**

This is the Majorana contribution of the complete 3+1D product with
$`\widetilde{n}_2=n_2`$, $`\widetilde{n}'_2=n'_2`$, $`\beta^-=\beta`$, and
$`\lambda_2^\gamma=[n_2\cup_2n'_2]_2`$, again with the lattice sign of the
quarter bracket. The lower output here is $`N_2=[n_2+n'_2]_2`$, and
$`\mathcal{ℰ}_3^\gamma=\mathcal{ℰ}_3`$.

{{equation:majorana-and-endpoints--majorana-contribution--30}}

Here the binary completion is

<a id="eq-m8"></a>

**(M8, 3+1D)**

{{equation:three-dimensional--majorana-decoration--32}}

The second carry obeys $`\beta^{-+}=\beta^+`$ in this closed sector.
The complete intrinsic term is the same two-input operation as in the
full product:

{{equation:three-dimensional--majorana-decoration--33}}

The displayed sum contains seven word terms; the complete $`z_4^0`$
has 20 distributed terms. The [interval-cut convention](OPERATIONS.md)
fixes their finite cochain evaluation.

<a id="majorana-4d"></a>
## 4+1D

The physical fields are the binary Majorana cochain $`n_3`$,
the binary complex-fermion cochain $`n_4`$, and the phase $`\nu_5`$.
Here $`n_4`$ is the physical point-fermion occupation of the original
pairing arrows, and the Majorana contribution has the lattice sign of the
heptagon loop: its quarter-valued bracket is $`-1/4`$. The complete
[4+1D tower](FOUR_DIMENSIONAL.md) writes its terminal layer in the shifted
occupation $`\widetilde{n}_4=n_4+R_4`$; for $`n_2=0`$ this is
$`\widetilde{n}_4=n_4+\mathrm{Sq}^1n_3`$. In that argument the same Majorana
contribution appears with the opposite quarter sign. The two forms are
related by the [bridging identity](FOUR_DIMENSIONAL.md#bridging-identity-4d).
Since $`d\,\mathrm{Sq}^1n_3=0`$ for closed $`n_3`$, the lower equations
below are the same in both arguments.

### Obstruction functions

#### Majorana obstruction

<a id="eq-m2-majorana-4d"></a>

**(M2γ, 4+1D)**

{{equation:majorana-and-endpoints--majorana-obstruction--32}}

#### Complex-fermion obstruction

<a id="eq-m2-4d"></a>

**(M2, 4+1D)**

{{equation:majorana-and-endpoints--complex-fermion-obstruction--33}}

##### Majorana contribution

<a id="eq-m2-gamma-4d"></a>

**(M2γ→c, 4+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--34}}

#### Bosonic obstruction

<a id="eq-m3-4d"></a>

**(M3, 4+1D: obstruction)**

{{equation:majorana-and-endpoints--bosonic-obstruction--35}}

##### Complex-fermion contribution

<a id="eq-m3-c-4d"></a>

**(M3c, 4+1D)**

{{equation:majorana-and-endpoints--complex-fermion-contribution--36}}

##### Complex-fermion–Majorana contribution

<a id="eq-m3-cgamma-4d"></a>

**(M3cγ, 4+1D)**

{{equation:majorana-and-endpoints--complex-fermion-majorana-contribution--37}}

##### Majorana contribution

<a id="eq-m4-4d"></a>

**(M4, 4+1D)**

Here the integer decoration is zero, so $`\widetilde{n}_3=n_3`$ and
$`\beta^- n_3=\beta n_3`$. In the physical occupation $`n_4`$ the
Majorana contribution is

{{equation:majorana-and-endpoints--majorana-contribution--73}}

Here $`\beta^+n_3=(\beta n_3+[\beta n_3]_2)/2`$. It has the half-valued terms
of the [compact formula](FOUR_DIMENSIONAL.md#majorana-phase-4d) of the complete
tower at $`n_2=0`$, and its quarter-valued bracket has the opposite sign, as
the [bridging identity](FOUR_DIMENSIONAL.md#bridging-identity-4d) requires for
the physical occupation; here
$`\tfrac14s_1^2(\beta n_3+[\beta n_3]_2)=\tfrac12s_1^2\beta^+n_3`$.

Its word operations are

{{equation:four-dimensional-majorana-phase--cartan--2}}

The intrinsic polynomial is

<a id="eq-m5-4d"></a>

**(M5, 4+1D)**

{{equation:four-dimensional-majorana-phase--intrinsic--1}}

### Stacking twisters

#### Majorana stacking

<a id="eq-m1-4d"></a>

**(M1γ, 4+1D)**

{{equation:majorana-and-endpoints--majorana-stacking--41}}

There is no stacking correction in this layer.

#### Complex-fermion stacking

<a id="eq-m1-fermion-4d"></a>

**(M1c, 4+1D)**

{{equation:majorana-and-endpoints--complex-fermion-stacking--42}}

##### Majorana contribution

<a id="eq-m1-gamma-4d"></a>

**(M1γ→c, 4+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--43}}

#### Bosonic stacking

<a id="eq-m3-stacking-4d"></a>

**(M3E, 4+1D)**

{{equation:majorana-and-endpoints--bosonic-stacking--44}}

##### Complex-fermion contribution

<a id="eq-m3-stacking-c-4d"></a>

**(M3Ec, 4+1D)**

{{equation:majorana-and-endpoints--complex-fermion-contribution--45}}

##### Complex-fermion–Majorana contribution

<a id="eq-m3-stacking-cgamma-4d"></a>

**(M3Ecγ, 4+1D)**

Here $`dn_4=\mathcal{𝒪}_5^\gamma`$ and $`N_4`$ is the binary output above:

{{equation:majorana-and-endpoints--complex-fermion-majorana-contribution--46}}

##### Majorana contribution

<a id="eq-m7-4d"></a>

**(M7, 4+1D)**

This is the [complete two-input law](FOUR_DIMENSIONAL.md#eq-t4c)
restricted to $`n_2=n'_2=0`$, $`\widetilde{n}_3=n_3`$, and $`dn_3=dn'_3=0`$,
written in the physical occupation $`n_4`$.
In particular $`\beta^-=\beta`$, $`\lambda_4^\gamma=0`$, and
$`\mathcal{ℰ}_4^\gamma=\mathcal{ℰ}_4`$; the terms containing
$`\lambda_4^\gamma`$ or a derivative of a closed integer Bockstein vanish
and are omitted. In the physical occupation the quarter-valued bracket and
the quarter-valued term of each $`B_5[\cdot,0]`$ carry the opposite sign.

{{equation:majorana-and-endpoints--majorana-contribution--74}}

The coefficient sets $`\mathcal I_5^\gamma`$ and $`\mathcal J_5^\gamma`$ are the shared
[general definitions](FOUR_DIMENSIONAL.md#eq-t4c), evaluated on closed inputs;
$`B_5`$ is the same
[phase-change cochain](FOUR_DIMENSIONAL_MAJORANA_PHASE.md).
The lower laws coincide with those of the complete tower, and
$`d_{s_1}\mathcal{ℰ}_5=\mathcal{𝒪}_6[N]-\mathcal{𝒪}_6[n]-\mathcal{𝒪}_6[n']`$
holds exactly.
The [zero-p+ip self-stacking formula](FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md)
is the equal-input specialization of these closed laws.

<a id="eq-m8-4d"></a>
The mathematical intrinsic word operation is retained in the
[derivation below](#intrinsic-word-products); its role does not define a
second terminal stacking convention.

<a id="fmps-1d"></a>
## 1+1D fMPS endpoint

The physical fields are $`n_0\in Z^0(G_b,\mathbb Z_2)`$,
$`n_1\in C^1(G_b,\mathbb Z_2)`$, and
$`\nu_2\in C^2(G_b,(\mathbb R/\mathbb Z)_{s_1})`$.
There is no integer layer. This fMPS representative is a distinct phase
coordinate; its physical field names do not imply an unstated coordinate
transformation to another manuscript representative.

### Obstruction functions

#### Majorana obstruction

<a id="eq-m13"></a>

**(M13γ, 1+1D)**

{{equation:majorana-and-endpoints--majorana-obstruction--49}}

#### Complex-fermion obstruction

<a id="eq-m13-fermion"></a>

**(M13c, 1+1D)**

{{equation:majorana-and-endpoints--complex-fermion-obstruction--50}}

##### Majorana contribution

<a id="eq-m13-gamma"></a>

**(M13γ→c, 1+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--51}}

The nonzero $`n_0`$ sector requires $`\omega_2=0`$ pointwise in this
representative. If the extension cocycle is nonzero but exact, trivialize
it explicitly before using that sector.

#### Bosonic obstruction

<a id="eq-m13-phase"></a>

**(M13O, 1+1D)**

{{equation:majorana-and-endpoints--bosonic-obstruction--52}}

##### Complex-fermion contribution

{{equation:majorana-and-endpoints--complex-fermion-contribution--53}}

##### Complex-fermion–Majorana contribution

{{equation:majorana-and-endpoints--complex-fermion-majorana-contribution--54}}

##### Majorana contribution

{{equation:majorana-and-endpoints--majorana-contribution--55}}

### Stacking twisters

#### Majorana stacking

<a id="eq-m14"></a>

**(M14γ, 1+1D)**

{{equation:majorana-and-endpoints--majorana-stacking--56}}

There is no stacking correction in this layer.

#### Complex-fermion stacking

<a id="eq-m14-fermion"></a>

**(M14c, 1+1D)**

{{equation:majorana-and-endpoints--complex-fermion-stacking--57}}

##### Majorana contribution

<a id="eq-m14-gamma"></a>

**(M14γ→c, 1+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--58}}

#### Bosonic stacking

<a id="eq-m14-phase"></a>

**(M14E, 1+1D)**

{{equation:majorana-and-endpoints--bosonic-stacking--59}}

##### Complex-fermion contribution

{{equation:majorana-and-endpoints--complex-fermion-contribution--60}}

##### Complex-fermion–Majorana contribution

{{equation:majorana-and-endpoints--complex-fermion-majorana-contribution--61}}

Here $`n_1^{\mathrm{even}}`$ is the degree-one cochain of the input whose
$`n_0=0`$.

##### Majorana contribution

{{equation:majorana-and-endpoints--majorana-contribution--62}}

Classification also quotients by the residual parity gauge
$`\nu_2\sim\nu_2+\omega_2/2`$; this remains part of the
equivalence relation.

<a id="intrinsic-word-products"></a>
## Shared mathematical word operation

This section defines a mathematical operation on two closed binary cochains
$`x,y`$ of the same degree $`q=2`$ or $`q=3`$. Substituting the fields from
3+1D gives $`z^0_4(n_2,n'_2)`$; substituting those from 4+1D gives
$`z^0_5(n_3,n'_3)`$. All sums and word evaluations in this section are binary.

<a id="eq-m9"></a>

**(M9)**

{{equation:majorana-and-endpoints--shared-mathematical-word-operation--63}}

The word sum in this formula consists of the following ordered evaluations.

| Words | Ordered inputs |
|---|---|
| `12131432412`, `12343213431`, `23412342324` | $`(x,y,y,y)`$ |
| `12123434123`, `12131412324`, `12134131234`, `12312412423`, `12314324123`, `12314342413`, `13242412314`, `13412321341`, `13412321413`, `13413142134`, `13432412314`, `31214124324` | $`(x,x,y,y)`$ |
| `12413432312` | $`(x,x,x,y)`$ |
| `12131432412` | $`(y,x,x,(x+y))`$ |
| `12131432412` | $`((x+y),x,x,y)`$ |
| `12131432412`, `12134341321` | $`((x+y),y,y,x)`$ |
| `1212312` | $`((x+y),y,(x\cup_qy))`$ |
| `12313123` | $`(y,x,(x\cup_{q-1}y))`$ |
| `12131232` | $`([\beta x]_2,y,y)`$ |
| `123131212` | $`(y\cup_{q-2}y,x,(x+y))`$ |
| `123131212` | $`((x+y)\cup_{q-2}(x+y),y,x)`$ |

For input degree three, use the words as written. For input degree two, a
word with $`k`$ input labels contributes only if its final $`k`$ letters
contain every label exactly once. Remove those final $`k-1`$ letters; if a
label is then missing, the term is zero. Otherwise evaluate the shortened
word on the listed inputs. This finite desuspension rule includes words
whose first input has degree greater than $`q`$.
