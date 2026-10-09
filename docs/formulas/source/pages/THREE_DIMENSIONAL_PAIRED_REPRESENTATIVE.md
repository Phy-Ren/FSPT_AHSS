# Auxiliary phase comparison in 3+1D

This retained comparison is evaluated after the current lower-field map
$`n_3\mapsto\check n_3=n_3+\mathcal B_3`$. Its output is
$`\check N_3+d\mathcal B_2`$. The current formulas additionally include
the explicit face phase in [the geometric reference](THREE_DIMENSIONAL_GEOMETRIC_REFERENCE.md).
In this auxiliary calculation only, symbols without checks on the CF field denote that mapped field.
The following terminal change then applies:

{{equation:three-dimensional-paired-representative--paired-phase-representative-in-3-1d--1}}

The inverse subtracts the displayed phase. All lower fields of this auxiliary calculation are fixed; the preceding lower-coordinate map must not be omitted. The symbol `Delta` means evaluation on
the actual lower stacked tower, minus the two input evaluations.
The nine-term `H4` is printed in [the stacking formulas](THREE_DIMENSIONAL.md#eq-t3b).
The former `P4` has been replaced by its [exact lower-obstruction identity](THREE_DIMENSIONAL_CF_EXCHANGE_REDUCTION.md); this changes no phase value.
The additive phase `hat f_cstar` is one half of the explicitly indexed
binary numerator in [the CF index rule](THREE_DIMENSIONAL_PRODUCT_WORD_INDICES.md#cf-block).

The constructions in this coordinate proof define the comparison with the
native representative. They are separate from the ordinary physical
formulas, which contain no auxiliary field evaluation.

## Integer characteristic phase

The interval and triangle cochains, orientation, normalized shuffle sums,
and first-vertex coefficient transport are fixed in
[the retained mathematical construction](THREE_DIMENSIONAL_TERMINAL.md).
For the following comparison only, write `n=n1,m=n1prime`,
`u=check n2,v=check n2prime`, and `W=check omega2`. Their integral residuals are

{{equation:three-dimensional-paired-representative--integer-characteristic-phase--2}}

On the triangle let `theta,phi,chi` be its fixed one-cochains and let
`mathcal U` be the retained binary Majorana lift. Explicitly,

{{equation:three-dimensional-paired-representative--integer-characteristic-phase--3}}

Use the canonical binary value of this entire sum in the integer quotient

{{equation:three-dimensional-paired-representative--integer-characteristic-phase--4}}

Every integer product retains its actual local system. In particular the
numerator subtracts the positively defined signed primitive
`theta(n cup1phi)m`. On an interval the primed and triangle-only terms are
absent. The integer phase numerator is `f_natural=tau_I F5` there, with the
oriented normalized shuffle sum acting on a base four-simplex.

Let `Re,Ee` be the output-edge restrictions of the displayed triangle
fields, and put `S=theta lambda`, `X=B+Bprime`. The corresponding degree-three
integer output gauge is

{{equation:three-dimensional-paired-representative--integer-characteristic-phase--5}}

The two `lambda cup1lambda` terms have canceled as integers. The exact
identity `B_high=C+dR+E` and integer cup polarization give
`O_new=O_native+d_s f_natural/4` and
`E_new=E_native+Delta f_natural/4-d_s g_natural/4` before the other displayed
coordinate changes. All even polarization terms remain in the half-valued
physical formulas.

## Complete output gauge

For the CF construction let `C_CF=theta n3+phi n3prime` and let `G_CF` be
the retained binary CF lift with both incoming CF decorations set to zero.
Its complete ordinary-word definition is the `G` seed and the explicit
index rearrangement in [the CF index rule](THREE_DIMENSIONAL_PRODUCT_WORD_INDICES.md#cf-block).
Then `g_CF=tau_triangle[G_CF cup3C_CF+dG_CF cup4C_CF]` is binary.
Its intrinsic Majorana restriction, continued as the same ordinary words,
is

{{equation:three-dimensional-paired-representative--complete-output-gauge--6}}

Put `lambda_gamma=u cup2v`, as its canonical binary lift. The intrinsic
characteristic gauge is the following integer cochain:

{{equation:three-dimensional-paired-representative--complete-output-gauge--7}}

Finally let

{{equation:three-dimensional-paired-representative--complete-output-gauge--8}}

The ten ordinary words of `H3pure` are printed in
[the word appendix](THREE_DIMENSIONAL_PRODUCT_WORD_INDICES.md#accepted-majorana-bridge-and-physical-origin-labels).
All half-valued brackets are binary; the quarter-valued cup1 term is the
canonical lift of its whole binary sum. These reduction boundaries fix
the output gauge, including its open-Majorana continuation. Its closed-Majorana operator comparison is in the auxiliary CF coordinate.
The current-coordinate comparison includes the single-state and output maps above.
