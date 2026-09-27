# Public release scope

This repository is a clean public snapshot of the project's independently
implemented code, mathematical exposition, computed results, and validation
reports. It starts a separate Git history. The complete local working history
and private comparison archive are retained by the author and are not pushed.

The source checkout is `/home/xingyu/FSPT_AHSS`; the separate publishing checkout
is `/home/xingyu/FSPT_AHSS_public`. These are author-local paths, not installation
requirements. `PUBLICATION_MANIFEST.json` identifies the source commit, copied
file hashes, publication-only documentation changes, and excluded-file hashes.
The snapshot-builder script and its isolated tests are explicit tooling overlays
from the reviewed publishing workspace; their exact hashes are recorded too.
The original working repository has no publishing remote. The numerical GAP
source and result archives retain their accepted bytes. The public Python
launcher additionally accepts `AFS_GAP` or a `gap` executable on `PATH`, with
the original cluster path as fallback; its GAP arguments are unchanged.

## Private comparison materials

Unpublished collaborator PDFs, their text/glyph transcriptions, recovered draft
answer tables, original legacy logs, and full reference-row comparison payloads
are not distributed. Aggregate comparison statistics, source hashes, our own
analysis, and independently computed finite controls remain available. The
reference-input manifest records provenance only; it does not contain the input
bytes. Historical validation documents describe the complete local audit, so
commands requiring those optional reference materials need separately supplied
authorized copies. Production classification, stacking, saved-result audits and
reports do not require them.

The generated obstruction/product coefficients are mathematical inputs evaluated
by this implementation. No SptSet or collaborator implementation is included or
loaded by production. No license grant for omitted third-party material is
implied by publication of this repository.

## Reproduce and synchronize

Install the GAP packages and Python environment described in `README.md`. Run
`scripts/run_group.py` for one complete classification/stacking calculation, or
follow `docs/CLUSTER_RUN.md` to create fresh compute allocations for all 230.
The accepted results and exact source snapshots are in `results/space_groups`
(crystalline spin-half, internal spinless) and `results/space_groups_spinless`
(crystalline spinless, internal spin-half). Their archived bytes are unchanged
in this release. The second archive distinguishes a unique abstract upper
extension from an actual marked upper cochain witness. The missing upper
CF/bosonic twisters are not supplied by publication of an abstract group.

Run self-contained saved-result, scheduling and publication tests without private
reference inputs:

```sh
PYTHONPATH=tests python3 -m unittest test_stacking test_stack_result_cli \
  test_audit_run test_report_results test_collect_performance \
  test_archive_campaign test_comparison_archive test_boss_current \
  test_external_comparison test_deadline_archive test_deadline_evidence \
  test_deadline_guard test_submit_campaign test_worker_input test_publish_snapshot
PYTHONPATH=tests python3 -m unittest test_audit_background_run \
  test_report_background_results test_background_performance \
  test_background_provenance_review test_pip_diagnostics test_stack_result_background \
  test_compare_background_runs test_report_physical_conventions
PYTHONPATH=tests python3 -m unittest test_boss_parser test_c4_pip_square_cf \
  test_closed_cf_phase test_free_pip_universal test_pip_incoming_formula
PYTHONPATH=tests python3 -m unittest test_point_group_audit test_point_group_marked_controls
```

An unrestricted `unittest discover` also selects optional unchanged-reference
oracle tests, which require the omitted `vendor/` formula bundles and collaborator
modules. Missing reference imports in those tests do not affect production or
the self-contained suite above; no such test is counted as passed without its
original input.

For a subsequent public release, first commit and review the intended changes
in the source checkout, then prepare the separate clean publishing checkout:

```sh
python3 /home/xingyu/FSPT_AHSS/scripts/publish_snapshot.py \
  --source /home/xingyu/FSPT_AHSS --ref HEAD \
  --output /home/xingyu/FSPT_AHSS_public --update
```

The script refuses an unclean publishing checkout, copies only committed source
bytes within its explicit allowlist, reapplies the reference exclusions, scans
common credential signatures, and does not commit or push. Review the generated
manifest and `git diff` in the publishing checkout before committing and pushing
there. Never attach this public remote to the full local working repository.
New result directories require an explicit publication-policy review; they are
excluded until added to the allowlist.
