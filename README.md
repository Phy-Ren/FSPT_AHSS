# FSPT_AHSS

Independent exact computation of three-dimensional crystalline fermionic SPT
decoration layers and stacking extensions for the 230 ordinary space groups.

All **230 classifications and complete stacking calculations are finished**.
The accepted uniform run reached all classification checkpoints in **13 min
3 s** and all full results in **3 h 31 min 39 s**, including queue delays on
five shared PBS workers. Its saved mathematical fields agree exactly with the
complete generic baseline for all 230 groups.

Start with the [Chinese project report](docs/PROJECT_REPORT_ZH.md),
[formula PDF](notes/independent_space_group_formulas.pdf),
[230-group table](results/space_groups/report/space_groups.pdf), and
[measured performance](results/space_groups/performance.pdf).
The [cluster guide](docs/CLUSTER_RUN.md) gives the persistent SSH and fresh PBS
allocation procedure. This public repository is a clean release snapshot. See
[publication scope and synchronization](PUBLIC_RELEASE.md) for the retained
local history and omitted private reference materials.

The first campaign fixes physical spin-half superconducting fermions, no extra
onsite symmetry, the full affine space group, determinant sign action, and
effective internal fermion-parity extension omega = 0. Weak phases and atomic
fermion parity are retained.

## Independence

The implementation does not load, wrap, or build upon SptSet. GAP/HAP, CrystCat,
and Polycyclic provide generic group and resolution infrastructure. The cochain
adapters, exact quotient computations, classification pipeline, and stacking
engine are independently implemented. The user's delivered obstruction and
stacking formulas are mathematical inputs. The collaborator's calibrated
cochain product supplies an additional mathematical input for the torsion
p+ip square; its universal coefficients are independently evaluated and
compiled into this implementation. Production imports no collaborator engine.
The old SptSet implementation and external result tables are comparison
references only; production must not consult them.

## Computation

The authoritative working directory is `/home/user/xyren/AllFSPT` on
`cuhk-cluster3`. Numerical work runs inside PBS allocations on compute nodes.
The local Git checkout is `/home/xingyu/FSPT_AHSS`.
`scripts/worker.pbs` starts a bounded task worker; `scripts/submit_task.py`
queues commands and each task retains status, stdout, CPU time, and peak memory.

The tested cluster environment is GAP 4.13.1, HAP 1.62, CrystCat 1.1.10,
Polycyclic 2.16, the GAP JSON package, and Python 3.8.16. The runtime uses the
compiled files under `gap/`; it does not require the supplied formula archives
or collaborator checkout. Regenerating the formulas and running their reference
oracle tests additionally uses the unmodified inputs under `vendor/` and a
modern Python interpreter. Those inputs are kept outside Git.

The complete calculation for **one space group is one sequential GAP process**:

```text
AFSBackend(group)
    -> AFSClassify(context)
    -> AFSFreePipFromClassification(classification_object), when needed
    -> AFSExplicitPipStacking(classification_object)
    -> export results and certificates
```

The classification object retains the actual cocycles, obstruction primitives,
incoming boundaries, and marked quotient coordinates. Stacking uses that same
object to lift and multiply its generators. A layer's abstract group orders are
not sufficient input. Parallel workers handle different space groups; they do
not split these dependent stages across processes.

Set `AFS_GAP=/path/to/gap` if GAP is not on your `PATH`. Run the complete pipeline with:

```sh
python3 scripts/run_group.py 6 --mode full --output runs/example/sg6.json
```

Use this command inside a compute-node allocation or through the task queue.
The classification-only mode exists for development checks. Separate development
campaigns may repeat classification when testing the complete pipeline.

For a freshly allocated set of workers, freeze and queue the entire calculation
with the following pattern; substitute the five live queue names created by the
[cluster guide](docs/CLUSTER_RUN.md):

```sh
python3 scripts/submit_campaign.py --run runs/new_campaign \
  --queues NEW_Q1 NEW_Q2 NEW_Q3 NEW_Q4 NEW_Q5 \
  --groups 1-230 --mode full --source results/space_groups/source \
  --timings results/space_groups --timeout 27000
```

Immediately after submission, run the observer in a separate login-node
terminal and leave it running until completion:

```sh
python3 scripts/watch_campaign.py runs/new_campaign
```

This records classification and full completion on one clock, including queue
delays. If that terminal is interrupted, restart the same command with
`--resume` to preserve the existing observation history.

Queue names must identify live PBS workers. The scheduler starts known long
calculations and previously unfinished groups early. Prior runtimes affect only
the task order; the numerical calculation reads no previous classification.
The timeout is a per-group scheduling limit, not a measured or predicted runtime.
Its default is 27000 seconds (7.5 hours); the worker allocation must leave
enough time for each queued task and cleanup. The accepted run preserves its
completed scheduling-extension evidence in the archive; see
`docs/SCHEDULING_EXTENSIONS.md`. Its SG219 task actually finished before its
original four-hour limit and the original worker recorded `done`, exit zero.
Each worker limits simultaneous single-threaded GAP processes to its slot count.
The supplied PBS templates request 28 CPU cores per node; worker counts must be
between 1 and 28, including values supplied through `AFS_WORKERS`.
The measured campaigns share five workers with a combined limit of 140 tasks;
other candidate and validation tasks were also running. Their observed elapsed
times include queueing, shared load, and observation delay, rather than measuring
exclusive use of 140 cores. Classification completion is observed within the
full pipeline, not in a separate classification-only benchmark.
`campaign.json` records the frozen source hashes, commands, and scheduling plan.
A classification checkpoint is written before stacking, which continues with
the same in-memory object.

Audit and use saved generator relations without another GAP calculation:

```sh
python3 scripts/audit_run.py results/space_groups --require-complete-witnesses \
  --require-formula-convention normalized-pip-aw-edge-transport-v2
python3 scripts/stack_result.py results/space_groups/sg219.json \
  --left '{"P1":1}' --right '{"P1":1}'
```

Generator coordinates belong to the specific saved presentation; labels from
different source versions need not describe the same representatives. When
`pip.free_lattice.fullFreePhaseWitness` is true, `Pfree` coordinates refer to the
exported primitive surviving lattice basis and its complete defining towers.
Earlier development files without that export describe only an abstract free
splitting. See `docs/VALIDATION.md` for the precise mathematical scope and
`docs/STATUS.md` for the current formula-correction audit.

For SG219 this returns `P1 + P1 = C1`, with `P1` of order four. All 44 groups
with nonzero free p+ip rank export an actual primitive surviving lattice basis
and complete generator towers. All 32 surviving torsion p+ip cases include the
upper phase relation. These exports do not mean that every group has undergone
the separate full comparison-support audit; completed audit cases and the
mathematical assumptions are recorded in `docs/VALIDATION.md`.

The accepted archive is `results/space_groups`, from `full_closed_cf_v09` with
source ID `9c16c0714da16a1ed5dc23b7830701afc01e6d7a37ee6d243f536ee4dc9ecd96`.
The live `gap/*.g` files exactly match that frozen source: closed-CF/half-phase
evaluation is enabled, the mod-two bar comparison map is disabled, and native
mod-two classification contraction remains enabled. Source, checkpoints, task
logs, exact results, scheduling evidence and performance are retained together.

All 920 graded-layer entries match the supplied current boss PDF. Its full
stacking extensions are not supplied. The historical full-stacking comparison
has 179 equal groups, 21 changes already involving graded layers, four
same-layer extension differences, and 26 empty reference entries. The provided
Weicheng materials support finite-model checks, without an affine-230 stacking
table. Details are in the project report and `docs/STATUS.md`.
