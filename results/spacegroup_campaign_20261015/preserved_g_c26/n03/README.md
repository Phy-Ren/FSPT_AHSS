# Preserved G n03

The full preserved parent has 54 cases: 52 ordinary and two recovered.
All 46 cases required for final assembly are ordinary completions. Eight extra
controls remain in the parent, including the recovered SG227 and SG142 spin-half
cases. Six original selected cases remain retries; failed originals are retained
unchanged.

`evidence.tar.gz` is the exact 2,842,572-byte finalized archive, SHA256
`0986e8439e1244d44261861b95d5d311e78fb366c75e7e6726c7375993cbfd37`,
containing 1,078 original/operation/preserved/accepted files. The original
selection had 60 cases. `completion.json` and its second download are byte-exact;
the download and frozen-replay proofs are retained beside them.

`recovery.json` preserves the full ledger. `assembly_entry.json` retains the
exact required 46-case subset without changing the parent selection. Use the
[common verifier](../README.md) to validate this archive and replay the full
parent. This is preserved-subset acceptance, not successful completion of the
failed/stopped original G campaign.
