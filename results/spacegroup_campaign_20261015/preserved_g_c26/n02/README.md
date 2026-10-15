# Preserved G n02

The full preserved parent has 51 cases: 48 ordinary and three recovered.
All 42 cases required for final assembly are ordinary completions. Nine extra
controls remain in the parent, including the recovered SG223, SG228 and SG206
spin-half cases. Five original selected cases remain retries; failed originals
are retained unchanged.

`evidence.tar.gz` is the exact 2,673,206-byte finalized archive, SHA256
`3033f3f61425422b7b157b768792a25cd93e9559eed90028d6d91d160613939c`,
containing 1,015 original/operation/preserved/accepted files. The original
selection had 56 cases. `completion.json` and its second download are byte-exact;
the download and frozen-replay proofs are retained beside them.

`recovery.json` preserves the full ledger. `assembly_entry.json` retains the
exact required 42-case subset without changing the parent selection. Use the
[common verifier](../README.md) to validate this archive and replay the full
parent. This is preserved-subset acceptance, not successful completion of the
failed/stopped original G campaign.
