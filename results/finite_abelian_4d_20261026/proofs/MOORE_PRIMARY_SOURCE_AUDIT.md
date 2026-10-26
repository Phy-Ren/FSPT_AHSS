# Primary-source audit of the low Moore-spectrum facts

Completed 2026-10-26.

Source: Shichiro Oka, **Multiplications on the Moore spectrum**, Memoirs of the Faculty of Science, Kyushu University, Series A, 38 (1984), 257--276.
DOI: https://doi.org/10.2206/kyushumfs.38.257.

The complete paper was retrieved using arxiv-tools `fulltext 10.2206/kyushumfs.38.257`.
The extracted text is OCR, so journal pages 261 and 262 were rendered and inspected visually.

## Facts explicitly stated in Oka

The definition of M_q on p.257 is exactly the stable cofiber of q:S^0 -> S^0 used in our notes.
Lemma 7(a), p.261, gives

    pi_0(M_q)=C_q,
    pi_1(M_q)=C_2 for even q,
    pi_2(M_q)=C_4 for q=2 mod4,
    pi_2(M_q)=C_2 x C_2 for q=0 mod4.

The paragraph preceding the lemma defines the lift eta_tilde_q with q eta_tilde_q=eta, where q here denotes the top-cell quotient map in our notation.
It states that this lift has order four when the cyclic order is 2 mod4 and order two when the cyclic order is 0 mod4.
It also gives the Toda relation {2,eta,2}=eta^2.
For M_2 this identifies twice the order-four lift with the bottom-cell image of eta^2.

Lemma 7(b), p.262, gives the stable mapping groups.
Setting its two cyclic orders equal shows that the identity of M_q has order q when 4 divides q and order 2q when q=2 mod4.
Thus

    q id_(M_q)=0       for 4|q,
    4 id_(M_2)=0,
    2 id_(M_2) != 0.

The nonzero twice-identity of M_2 is i eta q: it vanishes on the bottom cell and factors through the top quotient, and the cofiber sequence identifies the nonzero kernel element with that map.
These are exactly the nullmultiplication facts used to split the iterated Moore smashes.

## The two-Moore stem-one group

Finite Spanier--Whitehead duality gives D M_2 = Sigma^{-1} M_2.
Consequently

    pi_1(M_2 smash M_2)
      = [S^1,M_2 smash M_2]
      = [S^1 smash D M_2,M_2]
      = [M_2,M_2]
      = C_4,

where the final equality is Oka Lemma 7(b).
This supplies the order-four extension in the four-factor block directly from the primary source, without a separate guessed extension.
Under the same duality, twice this generator is the bottom eta class, corresponding to 2 id_(M_2)=i eta q.

## Audit conclusion

All low stable-homotopy inputs used in `THREE_FACTOR_MOORE_DERIVATION.md` and `FOUR_FACTOR_MOORE_DERIVATION.md` are supported by this primary source and elementary cofiber/duality arguments.
There is no remaining unidentified Moore-spectrum assumption.
