# A specific grading inconsistency in the printed D2 bordism derivation

Audit date: 2026-10-14. This is our mathematical audit, **not a published erratum**. The printed reference fixture remains unchanged. The result below concerns one explicitly identified derivation; it supports no general judgement about either author or paper.

Arun Debray's [arXiv:2102.02941v3](https://arxiv.org/abs/2102.02941v3), dated 2026-02-03, prints \(\mathbb Z_2^3\) for spin-half proper \(D_2,D_6\) in Table 5, p.52. Theorem 4.82, p.57, states \(\Omega_4^{\mathrm{Spin}^c}(B(\mathbb Z_2^2))=\mathbb Z^2\oplus\mathbb Z_2^3\). This transcription is correct. However, the degree count in item (4) of that theorem's proof contradicts its cited Eq. (4.59), p.49.

Write \(P=B\mathbb Z_2\), \(V=\mathbb Z_2^2\), and \(ku\) for connective complex K-theory. Equation (4.59) states

\[
ku\wedge P\wedge P\simeq
(ku\wedge\Sigma^2P)\vee\Sigma^2H(\mathbb F_2[u,v]),
\qquad |u|=|v|=2.
\]

The proof on p.57 assigns the last summand rank \(k-1\) in every degree \(k\ge2\). Its actual degree \(k\) basis consists of \(u^av^b\) satisfying \(2+2a+2b=k\). Consequently

\[
\pi_k\Sigma^2H(\mathbb F_2[u,v])=
\begin{cases}
\mathbb F_2^{k/2},&k\ge2\text{ even},\\
0,&k\text{ odd or }k<2.
\end{cases}
\]

In degree four there are precisely two basis monomials, \(u\) and \(v\).

This is independently corroborated by Robert Bruner, Khairia Mira, Laura Stanley and Victor Snaith, *Ossa's Theorem via the Kunneth Formula*, **Mathematics and Statistics 3(3)**, 58–64 (2015), [arXiv:1008.0166](https://arxiv.org/abs/1008.0166), Theorem 2.12. At \(p=2\), their Eilenberg–Mac Lane summands have suspension degrees \(2i+2j-2\), with \(i,j>0\). Degree four therefore receives only \((i,j)=(1,2),(2,1)\). Their notation \(bu\) denotes the same connective complex K-homology; this is a mathematical tool for the interacting bordism computation, not a free-band classification being substituted for it.

## Reduced and unreduced summands

The stable splitting

\[
\Sigma^\infty(BV)_+\simeq S\vee\Sigma^\infty P\vee\Sigma^\infty P
\vee\Sigma^\infty(P\wedge P)
\]

adds exactly one unreduced \(ku_*(\mathrm{pt})\) summand. Reduced \(ku_{2j}(P)=0\) and \(ku_{2j+1}(P)=\mathbb Z_{2^{j+1}}\) for \(j\ge0\). Thus

\[
ku_4(BV)=\mathbb Z\oplus\mathbb Z_2^2,
\qquad ku_0(BV)=\mathbb Z.
\]

Using the low-degree Anderson–Brown–Peterson comparison invoked in the source, \(\Omega_k^{\mathrm{Spin}^c}(X)\cong ku_k(X)\oplus ku_{k-4}(X)\) in the degrees at issue, gives the following explicit check. All nontrivial reduced torsion for \(V\) is 2-primary.

| Degree | From the graded splitting | Printed Theorem 4.82 at \(n=2\) |
|---|---|---|
| 0 | \(\mathbb Z\) | \(\mathbb Z\) |
| 1 | \(\mathbb Z_2^2\) | \(\mathbb Z_2^2\) |
| 2 | \(\mathbb Z\oplus\mathbb Z_2\) | \(\mathbb Z\oplus\mathbb Z_2\) |
| 3 | \(\mathbb Z_4^2\oplus\mathbb Z_2\) | \(\mathbb Z_4^2\oplus\mathbb Z_2^3\) |
| 4 | \(\mathbb Z^2\oplus\mathbb Z_2^2\) | \(\mathbb Z^2\oplus\mathbb Z_2^3\) |
| 5 | \(\mathbb Z_8^2\oplus\mathbb Z_4\oplus\mathbb Z_2^2\) | \(\mathbb Z_8^2\oplus\mathbb Z_4\oplus\mathbb Z_2^6\) |
| 6 | \(\mathbb Z^2\oplus\mathbb Z_2^4\) | \(\mathbb Z^2\oplus\mathbb Z_2^6\) |

The discrepancy starts in degree three, so it cannot be explained by a different convention for an unreduced degree-zero summand. It is also not an unresolved extension: the cited primary result is already an isomorphism of groups (and the source quotes a splitting of spectra).

For spatial dimension three the Anderson-dual sequence uses \(\operatorname{Ext}(\Omega_4,\mathbb Z)\) and \(\operatorname{Hom}(\Omega_5,\mathbb Z)\). The latter vanishes because \(\Omega_5\) is torsion. The graded splitting therefore yields \(\mathbb Z_2^2\), rather than the printed \(\mathbb Z_2^3\). For proper \(D_6\), the source's inclusion \(V\hookrightarrow D_{12}\) gives the same 2-primary result; its odd-primary degree-four contribution vanishes, and degree five has no free part. The same conclusion follows for that case.

This is targeted mathematical corroboration for the group order produced by our retained model in these two cases, **conditional on the cited low-degree bordism comparison and the stated crystalline symmetry dictionary**. It does not identify our individual cochain roots with bordism invariants, establish the remaining point groups, or calibrate nonzero 2D IQH sectors. No E8 factor was deleted in this derivation.

## Reproduction and provenance

Run:

```sh
python benchmarks/audit_debray_ku_grading.py \
  --output results/foundation_review_20261014/diagnostics/debray_d2_ku_grading_audit.json
```

The [script](../../benchmarks/audit_debray_ku_grading.py) checks both independent monomial indexings, all seven low degrees, and the phase-group extraction. It reads no classifier output. The [result](../../results/foundation_review_20261014/diagnostics/debray_d2_ku_grading_audit.json) preserves the printed theorem separately from the derived groups and records source hashes.

The inspected v3 source archive is pinned separately in the [printed fixture](../../benchmarks/debray_class_a_2102.02941v3.json). The 105-page author PDF was downloaded from [the author's site](https://adebray.github.io/papers/crystalline_phases.pdf), SHA256 `e3ee818735646e68fe382ead0580e92e57425bd47ac9ccff15ba91285a727929`; pp.49 and 57 were also inspected visually. Bruner–Mira–Stanley–Snaith's complete TeX was retrieved through the academic fulltext workflow and read at Theorem 2.12. This is a checked discrepancy between printed assertions and their stated ingredients, not a claim that either author has issued or endorsed a correction.
