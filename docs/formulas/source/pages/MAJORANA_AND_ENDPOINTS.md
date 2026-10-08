# Closed Majorana obstructions and stacking twisters

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
An outer bar first reduces the entire indicated expression modulo two.
Thus an integer $`x\cup_i y`$ and $`\overline{x\cup_i y}`$ are different
operations in a quarter-valued phase. Their complete evaluation rules are
in [Operations](OPERATIONS.md#arithmetic-and-carries).

The Bockstein $`\beta`$, its second carry $`\beta^+`$, and their signed
products have untwisted integer coefficients here. The phase instead has
coefficients $`(\mathbb R/\mathbb Z)_{s_1}`$ and differential $`d_{s_1}`$.
A hat denotes an additive phase, a prime the second input, and $`N_j`$ the
stacked binary field. The lower fields and all subscripts are fixed anew
at the start of each dimensional section.

The physical formulas below use the manuscript's operator phase coordinate.
The [explicit change of phase representative](#phase-coordinate-maps)
transports both obstruction and stacking laws. This coordinate is not
implicitly identified with the full integer-layer phase coordinate in the
main guide.

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

The bar inside $`\Delta[\overline{n_1^3}]`$ and the bar on
$`\overline{s_1n_1n'_1}`$ reduce each complete indicated product. The
$`\Delta`$ in the mixed half-valued contribution is binary; in the
eighth-valued contribution it subtracts the complete integer lifts. In contrast, $`n_1\cup_1n'_1`$ in the
quarter-valued bracket is a signed integer cup; its differential is also
integral.

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

This is the same pure Majorana formula as in the complete 3+1D tower.
Here $`n_1=0`$, so $`\check n_2=n_2`$ and
$`\beta^\circ n_2=\beta n_2`$. Its physical origin is Majorana;
the common expression also defines this contribution for a nonclosed
Majorana input in the full tower.

{{equation:three-dimensional--majorana-decoration--14}}

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

{{equation:majorana-and-endpoints--complex-fermion-contribution--28}}

##### Complex-fermion–Majorana contribution

<a id="eq-m3-stacking-cgamma"></a>

**(M3Ecγ, 3+1D)**

{{equation:majorana-and-endpoints--complex-fermion-majorana-contribution--29}}

##### Majorana contribution

<a id="eq-m7"></a>

**(M7, 3+1D)**

Use the same $`\widehat{\mathcal{ℰ}}_4^\gamma`$ as in the complete
3+1D product, with $`\check n_2=n_2`$, $`\check n'_2=n'_2`$,
$`\beta^\circ=\beta`$, and
$`\lambda_2^\gamma=\overline{n_2\cup_2n'_2}`$.
The lower output here is $`N_2=\overline{n_2+n'_2}`$, and
$`\mathcal{ℰ}_3^\gamma=\mathcal{ℰ}_3`$.

{{equation:three-dimensional--majorana-decoration--31}}

Here the binary completion is

<a id="eq-m8"></a>

**(M8, 3+1D)**

{{equation:three-dimensional--majorana-decoration--32}}

The second carry obeys $`\beta^{\circ+}=\beta^+`$ in this closed sector.
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

{{equation:majorana-and-endpoints--majorana-contribution--38}}

Its word operations are

{{equation:majorana-and-endpoints--majorana-contribution--39}}

The intrinsic polynomial is

<a id="eq-m5-4d"></a>

**(M5, 4+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--40}}

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

{{equation:majorana-and-endpoints--complex-fermion-majorana-contribution--46}}

##### Majorana contribution

<a id="eq-m7-4d"></a>

**(M7, 4+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--47}}

Here the binary completion is

<a id="eq-m8-4d"></a>

**(M8, 4+1D)**

{{equation:majorana-and-endpoints--majorana-contribution--48}}

The complete intrinsic term $`z^0_5(n_3,n'_3)`$ is given by the
[finite word definition](#intrinsic-word-products).

<a id="fmps-1d"></a>
## 1+1D fMPS endpoint

The physical fields are $`n_0\in Z^0(G_b,\mathbb Z_2)`$,
$`n_1\in C^1(G_b,\mathbb Z_2)`$, and
$`\widehat\nu_2\in C^2(G_b,(\mathbb R/\mathbb Z)_{s_1})`$.
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
$`\widehat\nu_2\sim\widehat\nu_2+\omega_2/2`$; this remains part of the
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
| `12131232` | $`(\overline{\beta x},y,y)`$ |
| `123131212` | $`(y\cup_{q-2}y,x,(x+y))`$ |
| `123131212` | $`((x+y)\cup_{q-2}(x+y),y,x)`$ |

For input degree three, use the words as written. For input degree two, a
word with $`k`$ input labels contributes only if its final $`k`$ letters
contain every label exactly once. Remove those final $`k-1`$ letters; if a
label is then missing, the term is zero. Otherwise evaluate the shortened
word on the listed inputs. This finite desuspension rule includes words
whose first input has degree greater than $`q`$.

<a id="phase-coordinate-maps"></a>
## Change of phase representative

The displayed physical laws use the operator representative. The maps
below record the exact change from the previous phase coordinate and its
inverse. All lower cochains and their product laws are unchanged. Source
and product transform together; these equations do not introduce a new
physical contribution.

### 2+1D phase coordinate

<a id="eq-m12-2d"></a>

**(M12, 2+1D: phase coordinate)**

{{equation:majorana-and-endpoints--2-1d-phase-coordinate--64}}

#### Obstruction transport

<a id="eq-m12-source-2d"></a>

**(M12O, 2+1D)**

{{equation:majorana-and-endpoints--obstruction-transport--65}}

#### Stacking transport

<a id="eq-m12-stacking-2d"></a>

**(M12E, 2+1D)**

{{equation:majorana-and-endpoints--stacking-transport--66}}

### 3+1D phase coordinate

<a id="eq-m12"></a>

**(M12, 3+1D: phase coordinate)**

{{equation:majorana-and-endpoints--3-1d-phase-coordinate--67}}

#### Obstruction transport

<a id="eq-m12-source"></a>

**(M12O, 3+1D)**

{{equation:majorana-and-endpoints--obstruction-transport--68}}

#### Stacking transport

<a id="eq-m12-stacking"></a>

**(M12E, 3+1D)**

{{equation:majorana-and-endpoints--stacking-transport--69}}

### 4+1D phase coordinate

<a id="eq-m12-4d"></a>

**(M12, 4+1D: phase coordinate)**

{{equation:majorana-and-endpoints--4-1d-phase-coordinate--70}}

#### Obstruction transport

<a id="eq-m12-source-4d"></a>

**(M12O, 4+1D)**

{{equation:majorana-and-endpoints--obstruction-transport--71}}

#### Stacking transport

<a id="eq-m12-stacking-4d"></a>

**(M12E, 4+1D)**

{{equation:majorana-and-endpoints--stacking-transport--72}}
