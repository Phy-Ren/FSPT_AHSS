# Self-stacking in 4+1D with no p+ip decoration

Take a complete state with $`n_2=0`$, closed binary Majorana cochain
$`n_3`$, complex-fermion cochain $`n_4`$ satisfying
$`dn_4=\mathcal{𝒪}_5^\gamma[n_3]`$, and phase $`\widehat\nu_5`$
satisfying the terminal obstruction equation. Here $`\check n_3=n_3`$.
All stacking corrections below have identical complete inputs. The
compact output representative differs from the current general reader
formula by the explicit bosonic coboundary given below.

## 1. p+ip stacking

{{equation:four-dimensional-majorana-diagonal--1-p-ip-stacking--1}}

## 2. Majorana stacking

{{equation:four-dimensional-majorana-diagonal--2-majorana-stacking--2}}

## 3. Complex-fermion stacking

{{equation:four-dimensional-majorana-diagonal--3-complex-fermion-stacking--3}}

## 4. Bosonic stacking

{{equation:four-dimensional-majorana-diagonal--4-bosonic-stacking--4}}

### Complex fermions

{{equation:four-dimensional-majorana-diagonal--complex-fermions--5}}

### Complex fermions and Majorana decoration

{{equation:four-dimensional-majorana-diagonal--complex-fermions-and-majorana-decoration--6}}

### Majorana decoration

{{equation:four-dimensional-majorana-diagonal--majorana-decoration--7}}

The lower output $`N_4`$ is the one computed above. The lower obstruction
and Bockstein retain their existing meanings:

{{equation:four-dimensional-majorana-diagonal--majorana-decoration--8}}

The first sum contains **sixteen MS terms**, with the following complete
word list. Every word has the same four arguments printed in the formula.

```text
12131432412  12343213431  23412342324  12123434123
12131412324  12134131234  12312412423  12314324123
12314342413  13242412314  13412321341  13412321413
13413142134  13432412314  31214124324  12413432312
```

There are **23 half-valued terms and five quarter-valued terms**, hence
**28 Majorana terms** with the defined lower operations retained. Adding
the one complex-fermion term and one exchange term gives **30 terms for
the complete self-stacking phase correction**: 25 half-valued and five
quarter-valued terms. This is the zero-p+ip diagonal specialization; the general open two-input law is
[given separately](FOUR_DIMENSIONAL.md).

In the quarter bracket, the unbarred
$`n_3\cup_1n_3`$ is the signed integer cup of canonical input
values. Its barred counterpart is the canonical value of the **whole**
binary operation. Their difference is even but can be nonzero modulo four.
The whole bar on $`\mathcal{𝒪}_5^\gamma`$ is required for the same reason.

## Explicit output gauge

The relation to the current complete reader representative is exact:

{{equation:four-dimensional-majorana-diagonal--explicit-output-gauge--9}}

The binary gauge primitive has only three face products:

{{equation:four-dimensional-majorana-diagonal--explicit-output-gauge--10}}

The complex-fermion and exchange contributions already equal their
current general-reader specializations. Adding this output bosonic
coboundary therefore gives the complete reader self-stack;
subtracting it gives the displayed 30-term total representative. The obstruction is
unchanged. The primitive is normalized, and
$`d_{s_1}(K_4^\gamma/2)=dK_4^\gamma/2\pmod1`$.

The equality was proved by complete binary coefficient comparison and
checked independently against the frozen complete phase and its explicit
gauge. The final lower-operation expression passes 1,024 closed-input
checks. No closed-input restriction has been imposed on the separate
complete two-input formula.

The input complex-fermion completion and incoming phase are retained.
The formula supplies a complete product in the zero-p+ip sector; a
p+ip root with nonzero integer decoration requires its own full cyclic
power formula. The [presentation theorem](ROOT_POWER_PRESENTATIONS.md)
explains how such powers determine the final abstract group.
