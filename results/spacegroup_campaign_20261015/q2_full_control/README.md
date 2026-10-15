# Q2 transfer: complete same-node control

The isolated q2-only candidate preserves the complete SG141 spin-half result,
but shows **no whole-run speed benefit** in this control. It is not integrated
into the production default and these diagnostic runs are not catalogue inputs.

| GNU time measurement | Frozen H | Q2-only candidate |
| --- | ---: | ---: |
| Wall seconds | 1342.36 | 1356.01 |
| User plus system CPU seconds | 1239.58 | 1268.61 |
| Maximum resident set size, KiB | 10590784 | 10632752 |

Both runs used n08, one job, a 16g GAP workspace cap, a 2400-second limit,
the same catalogue input, optimized GAP, formula VM, Python environment and
classification modes. They ran concurrently. These are single observations;
GNU time reports its process high-water metric, not an aggregate simultaneous
process-tree peak. The candidate's earlier improvement on an SG226 source
evaluation stage does not establish a complete-classification speedup.

The only source differences are the retained three-file `candidate_overlay`:
generic mod-two bar pullback, its import, and its use for the certified q2
source. Integer charge, integral phase transfer, homotopy corrections,
quarter-valued primitives, gauges and full stacking witnesses are unchanged.

All **35 scientific and certificate fields** agree literally with the fresh
baseline and the previously accepted H result. Only the three explicitly
listed runtime fields were excluded; worker call and cache statistics also
happen to agree. Each classifier performed its full equation checks. The
collector validated the complete parents and saved native completion/chain
certificates, and independently checked the Smith group and filling. Its
saved findings are in `exact_comparison.json`; this is implementation agreement,
not a proof of the full physical CI-kernel identification.

`raw.tar.gz` retains 38 original runtime artifacts and the capture proof.
The before/archive/after acquisition checks, runtime hashes and full source
hashes are retained. The baseline source is reconstructible from the Git
commit in `provenance.json`; the three-file overlay reconstructs the candidate.
This package adds no E8 or catalogue result.

Run `python3 results/spacegroup_campaign_20261015/q2_full_control/verify.py`
from any directory. The offline verifier checks retained hashes, safe archive
membership, both source sets against Git and the overlay, ordinary successful
wrappers, input/native bindings, literal field equality, and measurements
against the original GNU time reports. It does not rerun classification or
the original collector.
