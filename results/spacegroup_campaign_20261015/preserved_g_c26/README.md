# Preserved G parents with c26 validation

The two preserved parents contain **105 accepted cases: 100 ordinary completions
and five strictly validated recovered records**. Final assembly needs exactly
88 of them, and **all 88 required cases are original ordinary completions**.
The other 17 are retained controls: twelve ordinary and five recovered.

| Shard | Original selection | Preserved full parent | Required ordinary cases | Extra controls | Original retries |
| --- | ---: | ---: | ---: | ---: | ---: |
| [n02](n02/README.md) | 56 | 51 | 42 | 9 | 5 |
| [n03](n03/README.md) | 60 | 54 | 46 | 8 | 6 |

No original campaign is relabelled successful. The byte-exact archives retain
both entire original raw parents, including failed results and logs, the stop
reports and process evidence, full preservation ledgers, preserved CI/E8 parents,
accepted collections and operation logs. The original selections and ledgers
remain intact; `assembly_entry.json` selects the required 42/46 only after
validation of each full preserved parent. Nothing here updates the current
catalogue or claims completed full-460 acceptance.

Root stopped only the redundant owned G process trees after fresh identity and
coverage preflights at `2026-10-15T16:58:58.711323+00:00` (n02) and
`2026-10-15T16:59:11.869593+00:00` (n03). The stop reports subsequently record all
captured processes absent. The required G88 records were already ordinary
complete; every still-active G case was covered by the separately accepted H24.
The four failed original G tail cases remain failed and were absent from active
jobs. Their replacements are outside this package. The archived readiness
report explicitly did not itself authorize signals; root's action scripts,
immediate preflight logs and resulting reports are retained separately.

CI results retain frozen G commit `c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`,
source SHA256 `17150f175fffd703f2d1008ec0066f53f25d23abfc63dbb15dd71440243a08fc`.
Preservation, E8 and acceptance use the exact 65-file helper snapshot at
`c26f3dea716a6f5b2552c9b340b918d44f6151cd`, tree SHA256
`2b5fec1dcaf50b2e44184ad0bf421ce50f1a0aa1bd5b36c2e95800b9fcc107ad`.
The pipeline SHA256 is
`70cc4c24c29a348b51b37bba0322e223cc29d234d89fd80030358dc76cea7c57`.
Its source/config, deployment and prior local validation are in `common/pipeline/`;
`common/root_actions/` and `common/readiness/` preserve the exact action and
readiness records. Historical preparation-only wording in copied records refers
to that earlier preparation stage.

Run the portable offline verifier with Python, SymPy and this Git history:

```sh
python3 results/spacegroup_campaign_20261015/preserved_g_c26/verify.py
```

It reconstructs the exact c26 helper from Git in a temporary directory and
runs the retained pipeline's **verify** mode for both complete preserved parents.
It checks package and archive hashes, safe members, exact G source and input
bytes, ordinary wrappers, recovered certificates, all CI/E8 parent bytes,
presentations, filling and full frozen-collector replay. Accepted CI/E8 results
and validation bytes must reproduce exactly; only temporary provenance paths
differ. It never invokes the pipeline's remote **run** mode, an action script,
SSH, GAP classification or process signals. A relocated package accepts
`--repository /path/to/checkout`; optional `--replay-log` writes to a new external
path. Independent review logs are retained in `review/`.

This is acceptance of the supplied four-data model with
`physicalClassificationCertified: false`. It does not establish the remaining
physical CI-kernel identification. Raw ordinary execution status, including any
nonzero paired `batchExitCode`, remains unchanged. Recovered records keep
`status: recovered_complete` and do not receive fabricated successful exits.
