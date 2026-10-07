# Self-stacking twisters in 2+1D

Stack two identical complete states, including the complex-fermion
completion and bosonic phase. The fields are the binary Majorana cochain
$`n_1`$, the binary complex-fermion cochain $`n_2`$, and the phase $`\nu_3`$.
Use the [common notation](../FORMULA_GUIDE.md#conventions-and-coordinates)
and the obstruction equations in the [2+1D reference](TWO_DIMENSIONAL.md).
The phase representative is unchanged. As in that reference, this page
covers the zero-integer-decoration sector; a general nonzero chiral input
is outside its stated domain.

## 1. Majorana self-stacking

{{equation:three-dimensional-majorana-self-stacking--1-p-ip-stacking--1}}

## 2. Complex-fermion self-stacking

{{equation:two-dimensional-self-stacking--2-complex-fermion-self-stacking--1}}

Both terms come from Majorana decoration. The nonzero output must be
retained when the doubled state is used in a subsequent doubling.

## 3. Bosonic self-stacking

{{equation:two-dimensional-self-stacking--3-bosonic-self-stacking--2}}

### Complex fermions

{{equation:two-dimensional-self-stacking--complex-fermions--3}}

### Complex fermions and Majorana decoration

{{equation:two-dimensional-self-stacking--complex-fermions-and-majorana-decoration--4}}

Here $`dn_2=\mathcal{𝒪}_3^\gamma[n_1]`$ is the already defined lower
obstruction. Every allowed completion $`n_2`$ is included.

### Majorana decoration

{{equation:two-dimensional-self-stacking--majorana-decoration--5}}

The complete bosonic twister has **eight terms: six half-valued and two
quarter-valued terms**. The obstruction in the quarter bracket is the
canonical integer lift of its whole binary value. It must not be replaced
by the sum of separately lifted terms. The integer Bockstein is
$`\beta n_1=dn_1/2`$, with the differential taken before reduction;
for this closed binary degree-one cochain it equals $`n_1^2`$.

The [exact coefficient verification](coefficients/verify_two_dimensional_self_stacking.py)
compares the complete formula with the general law on twelve independent
binary inputs, using signed integer arithmetic. The residual is zero;
no coboundary or change of phase coordinate is used.
The [root-power presentation](ROOT_POWER_PRESENTATIONS.md) explains how
complete doubled states determine the finite extension data.
