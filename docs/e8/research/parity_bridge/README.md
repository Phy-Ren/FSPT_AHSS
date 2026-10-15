# Parity bridge and intrinsic-row review

Date: 2026-10-15 UTC. This directory is a standalone mathematical review. It does not change the insulator implementation or add a superconducting runtime dependency. All extended states use E8-first order $(e_p,n_p,n_{p+2},\nu_{p+3})$, $p=d-2$.

The main findings are in [parity_bridge.md](parity_bridge.md) and [intrinsic_response.md](intrinsic_response.md). The formal symmetry scope is a finite quotient of a lattice of rank at most four; the auxiliary charge circle retains its topology.

| Result | Status | Evidence |
|---|---|---|
| Same-symmetry circle quotient and parity carry | Exact group/cochain identities | Bridge §1; supplied v0.7 formulas |
| Closed CF-only source, product, short-gauge comparison in spatial dimensions 2, 3, 4 | Exact identities; open-charge remainder retained | Bridge §3; 96 exact checks |
| Pure neutral $16e_2$ source, product, compatible prism gauge in spatial dimension 4 | Established for the stated legal parity-formula domain | Bridge §4; conservative full-DAG certificate; 4 source and 28 nonbinary product-face checks |
| Intrinsic $4+1$D interacting Spin-c response basis and Spin restriction | Primitive integral basis established | Intrinsic §1–2; exact bordism-cycle evaluations |
| Nonzero-CI universal terminal parity map and paired stacking primitive | Open | Bridge §5; explicit residual equations, not installed as zero |
| Integral equivariant differentials leaving the intrinsic row | Open | Intrinsic §3; rational polynomial candidate is not an integral differential proof |

The pure neutral product result includes a universal vanishing argument for the binary completion. The sampled evaluator checks cover the source and nonbinary part; they are not described as a numerical run of the full binary recurrence. Exact-division domain assumptions and every supported arithmetic opcode are stated in the main report.

Reproduce the bounded exact evidence from this directory:

```bash
python check_charge_bridge.py
python check_intrinsic_lattice.py
python probe_parity_sixteen_valuation.py --public-reference /home/xingyu/FSPT_AHSS_public
python check_sixteen_reference.py --public-reference /home/xingyu/FSPT_AHSS_public --e8-reference /home/xingyu/AllFSPT_reviews/e8_v09_da3ad936/E8_AHSS_v0_9
```

The first two scripts record the exact reference hashes used. The parity comparison scripts accept a configurable read-only source path. Their immutable public reference revision is `ac45fa7ed0acd992a2f3a69273762dc9dceb2a97`. The source and local-artifact hashes are listed in [provenance.json](provenance.json). No new physical-spectrum completeness claim follows merely from these local comparison identities.
