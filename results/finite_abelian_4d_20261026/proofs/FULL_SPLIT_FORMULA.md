# Full split unitary finite-Abelian formula in 4+1D

Result, 2026-10-26.
This covers arbitrary rank and every prime, for total symmetry

    G_f = Z_2^f x A,    A = product_p product_{i=1}^{r_p} C_{p^{a_{p,i}}}.

It gives the full abstract stacking group, including all extensions.
It is not only an associated-graded classification.
The formula is evaluated by `../split_closed_formula.py` using integer arithmetic.

## Product over supports

For each prime p and each nonempty subset S of its cyclic factors with |S|<=5, take the block specified below.
The full group is the direct product of these blocks.
Subsets with more than five factors contribute zero.
All exponents within an individual block are ordered increasingly.
C_1 and an empty block mean the trivial group.

## Odd primes

For one factor of order p^a:

    p=3:   C_{3^{a-1}} x C_{3^{a+1}};
    p>=5:  C_{p^a}^2.

For k>=2 factors, put g=p^{min a_i}.

    k=2: C_g^2;
    k=3: C_g^4;
    k=4: C_g^3;
    k=5: C_g.

## Prime two

### One factor

    a=1:   0;
    a>=2:  C_{2^{a-2}} x C_{2^a}.

### Two factors, a<=b

    a=b=1:     0;
    a=1,b=2:   C_2;
    a=1,b>=3:  C_4;
    2<=a=b:    C_{2^{a-1}} x C_{2^a};
    2<=a<b:    C_{2^{a-1}} x C_{2^{a+1}}.

### Three factors, a<=b<=c, g=2^a

    a=b=c=1:   C_2^3;
    a=b=1<c:   C_2^4;
    a=1,b=2:   C_4 x C_2^3;
    a=1,b>=3:  C_8 x C_2^3;
    2<=a=b:    C_2 x C_g^4;
    2<=a<b:    C_2 x C_{2g} x C_g^3.

### Four factors

Let g be the smallest cyclic order and t the number of factors of order two.

    t=0:    C_2 x C_g^3;
    t=1:    C_2^4;
    t=2:    C_4 x C_2^2;
    t>=3:   C_2^3.

### Five factors

    C_g, where g is the smallest cyclic order.

## Proof architecture

1. The stable product splitting separates the factors with different supports.
   Connectivity removes all supports of size greater than five.
2. At odd primes, a mixed support has no lower nonzero spin-bordism coefficient in total degree five, so ordinary integral Kunneth gives the blocks directly.
3. The two-factor 2-primary theorem follows from explicit cohomology operations and naturality, using only three fixed exact small certificates for the secondary obstruction and extensions.
4. The three-factor blocks follow from the low cell presentation of BC_N, standard Moore-spectrum identities, exact upper/lower order bounds, and explicit self-stacking relations.
5. The four-factor block is the first stable homotopy group of the smash of four Moore spectra.
6. Five-factor connectivity leaves only ordinary H_5.

The detailed proofs are in:

- `ESTABLISHED_RESULTS_AND_GAPS.md`: stable splitting, odd primes, and elementary-Abelian formula; its original gap discussion is superseded by the later notes.
- `PAIR_BLOCK_THEOREM.md`.
- `THREE_FACTOR_MOORE_DERIVATION.md`.
- `FOUR_FACTOR_MOORE_DERIVATION.md`.

## Checks

The closed formula matches all 26 existing split unitary Abelian backgrounds in the saved exact catalog.
The complete comparison is in `../verification_report.json`.
Two new, independent exact cochain checkpoints confirm the predicted survival of the Majorana class x_1x_2x_3 for C_4^3 and C_2 x C_8^2.
In each case the secondary obstruction vanishes already in the original target cohomology, before quotienting by complex-fermion images.
These checks sharply distinguish the new result from the old C_2 x C_4^2 case, where that class is obstructed.

A completed independent full-group calculation for C_4^3 gives C_2^4 x C_4^10.
Its full presentation, exact Smith transformations, and receipts are included in `../full_results/split_C4_C4_C4/`.
The four marked-class checks, including the obstructed C_2 x C_4^2 and C_2 x C_4 x C_8 cases, are in `../checkpoints/`.
The standard Moore-spectrum facts have been audited in Oka's primary paper; see `MOORE_PRIMARY_SOURCE_AUDIT.md`.
There is no remaining unspecified exponent or rank case in the split formula itself.

## Separation from terminal p+ip formulas

For every mixed support X_S with |S|>=2,

    H^2(X_S,Z)=0,    H^1(X_S,Z)=0.

Thus every mixed block can be derived without the p+ip integer-decoration layer or its terminal stacking twister.
All p+ip dependence is confined to cyclic singleton factors under this stable splitting.
This is a statement about the abstract group, not about whether a chosen cochain coordinate contains a mixed correction term.
The main-text/appendix placement should be decided separately for the singleton factors whose abstract group requires the terminal p+ip stacking data.
