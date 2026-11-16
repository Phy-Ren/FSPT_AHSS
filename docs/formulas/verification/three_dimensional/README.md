# 3+1D verification

Exact checks of the [3+1D formulas](../../THREE_DIMENSIONAL.md), the
[3+1D self-stacking formulas](../../THREE_DIMENSIONAL_SELF_STACKING.md), and the
lattice construction of the 3+1D stacking paper. All arithmetic is exact:
binary values, integers and rationals modulo one. Run from this directory:

```sh
python check_lattice.py          # about one second
python check_formulas.py 300     # about five minutes on 32 cores
python check_code.py 60
python generate_self_tables.py   # about three minutes on 32 cores
```

Each script writes its receipt to [`results/`](results).

## Modules

| File | Content |
|---|---|
| [`lattice.py`](lattice.py) | Effective Majorana zero modes of the p+ip layers: the complete pairings of an F move and of a stacking move, and their parity change from the transition loops. No formula for $`\mathcal O_4`$ or $`\mathcal E_3`$ is used. |
| [`formulas.py`](formulas.py) | The displayed formulas: lower obstructions and stacking laws, $`\mathcal O_5`$ and $`\mathcal E_4`$ by contribution. The mixed and p+ip word sums are read from the [term manifests](../../term_census/three_dimensional/INDEX.json). |
| [`closed.py`](closed.py) | The closed-sector formulas ($`n_1=0`$) of the [Majorana projector calculation](../../MAJORANA_AND_ENDPOINTS.md#majorana-3d). |
| [`self_stacking.py`](self_stacking.py) | The two branches of the self-stacking page, with its face tables read from the page. |
| [`towers.py`](towers.py) | Random exact solutions of the lower equations, and the torsion branch $`n_1=s_1`$ from its 20 independent face values. |
| [`code_phases/`](code_phases) | Complex-fermion and Majorana phases of the publication code, as term lists. |

## Checks

**Lattice** (`check_lattice.py`). In each of the four background sectors
($`s_1`$ and $`\omega_2`$ zero or not):

- the parity change of the F move $`(1234,0134,0123)\to(0124,0234)`$ equals
  $`\mathcal O_4(01234)`$;
- the parity change of stacking two states on $`(0123)`$ equals $`\mathcal E_3(0123)`$,
  and for $`n_1=n'_1=0`$ the closed-sector law $`n_2\cup_1n'_2+s_1(n_2\cup_2n'_2)`$;
- the three worked F moves of the paper give parity $`0,1,1`$.

The order of the effective Majorana zero modes in a tetrahedron is
$`(\langle013\rangle_B,\langle123\rangle_B,\psi\ldots,\langle012\rangle_A,\langle023\rangle_A)`$.

**Formulas** (`check_formulas.py`):

- closure: $`d_{s_1}\mathcal O_5=0`$ on random solutions of the lower equations;
- stacking: $`d_{s_1}\mathcal E_4=\mathcal O_5[N]-\mathcal O_5[n]-\mathcal O_5[n']`$;
- closed sector: for $`n_1=n'_1=0`$, $`\mathcal O_5`$ and $`\mathcal E_4`$ equal the
  closed-sector formulas on every face, and the $`c\psi`$, $`\gamma\psi`$, $`\psi`$
  contributions vanish;
- self-stacking: the page formulas for $`n_1=0`$, and every contribution of
  the page formulas for $`n_1=s_1`$, equal $`\mathcal E_4`$ with equal upper and lower states;
- $`\mathbb Z_4^{f,T}`$ ($`s_1=m_1`$, $`\omega_2=m_1^2`$): on all bar simplices, the
  four roots $`(m_1,0,0,i^{m_1^4})`$, $`(0,m_1^2,0,i^{m_1^4})`$, $`(0,0,m_1^3,1)`$,
  $`(0,0,0,(-1)^{m_1^4})`$ solve all equations, and their squares are
  $`(2m_1,m_1^2,0,i^{m_1^4})`$, $`(0,0,m_1^3,1)`$, $`(0,0,0,(-1)^{m_1^4})`$ and $`(0,0,0,1)`$.

**Code** (`check_code.py`): the formulas equal the phases of the publication
code after the change stated in
[From the code to the 3+1D formulas](../../THREE_DIMENSIONAL_GEOMETRIC_REFERENCE.md).

**Face tables** (`generate_self_tables.py`): for $`n_1=s_1`$ the mixed and pure
p+ip contributions of the general formula with equal upper and lower states, minus the
explicit terms of the self-stacking page, are evaluated on all $`2^{16}`$
values of $`s_1`$, $`\omega_2`$, $`n_2`$ on the faces containing the vertex $`0`$.
Their algebraic normal forms are the two
[face tables](../../THREE_DIMENSIONAL_SELF_STACKING_FACES.md); the script
compares them row by row with the printed tables.
