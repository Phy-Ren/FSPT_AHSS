# Explicit scheduling extensions

The numerical GAP sources and their frozen campaign hashes are separate from
task supervision. A task cap is an execution budget, not a mathematical failure
criterion or a predicted runtime. A healthy calculation may be given a longer
budget before its original deadline, within its existing PBS allocation.

`scripts/deadline_guard.py` supports this exceptional case for the already
running workers, which keep their original timeout values in memory. Editing a
task JSON file cannot change those values. The guard is itself submitted to the
same worker, validates every active task and its exact process identity, then
temporarily stops only the worker PID. Its numerical child processes continue.
An independent watchdog is armed first. The guard waits for each task to exit
or reach its declared extended deadline, then resumes the original worker.
Unexpected guard failure returns control to the original worker through the
watchdog. The PBS allocation remains an external upper bound.

The guard does not modify numerical source, results, task payloads or task
status files. It writes a separate ledger containing the declaration made
before the original deadline, byte copies of original records, process
identities, the frozen guard source, and exit observations. Kernel wait status
is unavailable on the cluster's old Linux version; that absence is explicit.
Successful acceptance still requires the original worker's actual reaped exit
code and the independent GNU time record, both zero.

The original worker can report `timeout` with `exit_code=0` after a successful
extended command. That record remains unchanged. Its `elapsed_s` can include
time between the command's exit and the worker's later resumption. Command
runtime comes from GNU time and the guard's exit observation interval. A
polling observation is an interval, not an exact kernel exit timestamp. The
campaign observer continues on its original clock throughout supervision.

## Auditing and archival

A campaign explicitly associates an extended task with its ledger through
`deadline_extensions.json`:

```json
{
  "schema": "fspt-deadline-extension-index-v1",
  "tasks": {"TASK_ID": "../deadline_guards/LEDGER_DIRECTORY"}
}
```

`deadline_evidence.py` checks the declaration, original task and process
identities, source of the supervisor, guard/watchdog ordering, both deadline
clocks, actual GNU time bytes, and the original worker's successful reap. The
performance collector retains `task_status: timeout` when present and reports
the separate `effective_task_status: done_with_audited_deadline_extension`.
Absent valid extension evidence, a timeout still prevents strict acceptance.
No mathematical or numerical-source audit is relaxed.

The campaign archiver preserves the index and every original ledger byte,
records their old and archived paths, and hashes them along with the ordinary
results and task records. Archived indices are resolved through that mapping;
the original absolute paths inside records remain historical provenance.

The supervisor has local controls for separate task completion times, guard
failure recovery, exhausted budgets, identity mismatches, older kernel
interfaces and recovery before log I/O. The evidence reader has separate
negative controls for expired, inconsistent, nonzero-exit or tampered records.
These controls establish supervision and accounting behavior; the mathematical
results still require the full ordinary result audits.

## Completed campaign evidence

All three supervised SG219 tasks finished successfully, neither supervisor
sent a terminating signal, and both watchdogs completed normally. Every
original worker reaped exit zero. All five PBS allocations have been released.

The accepted v09 task completed before its original four-hour cap and retains
raw status `done`. The comparison v08 task exceeded that original cap but
finished within its predeclared extension, retaining raw `timeout`. Both
complete 230-group campaigns passed strict mathematical/source/performance
acceptance. Their original indices and ledgers are in
`results/space_groups/deadline_extensions` and
`results/optimization_validation/full_optimized_v08/deadline_extensions`.
Strict performance collection was repeated from each portable archive.

The same-source generic v07 retry exited before its original cap but was
reaped after the other n01 task completed, so its raw record is also `timeout`,
exit zero. Its GNU time and guard exit interval establish the earlier real
completion. It belongs only to the explicitly assembled mathematical baseline,
not to a continuous full-230 performance campaign.
