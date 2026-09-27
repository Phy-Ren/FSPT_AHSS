# FSPT_AHSS

Independent exact computation of three-dimensional crystalline fermionic SPT
decoration layers and stacking extensions for the 230 ordinary space groups.

Both physical conventions now have **all 230 classifications and abstract
stacking groups determined**, using the full infinite affine space groups.
Translations, weak phases and atomic fermion parity are retained.

| Physical convention | Effective internal extension | Complete campaign | Marked stacking evidence |
|---|---|---|---|
| Crystalline spin-half = internal spinless | `omega = 0`, `s = w1` | 3 h 31 min 39 s | 230/230 |
| Crystalline spinless = internal spin-half | `omega = w2 + w1^2`, `s = w1` | 3 h 47 min 35 s | 214/230 |

For the other 16 spinless groups, the actual upper p+ip-to-CF/bosonic carries
remain unknown. Every allowed carry has the same certified abstract group;
the program retains that family and refuses unsupported marked stacking.
See the [precise scope and group list](docs/PIP_DIFFERENTIAL_DIAGNOSTICS_SPINLESS.md).
Each convention agrees with its complete numerical baseline in all saved
mathematical fields and native witnesses. These are regression comparisons
between independently run configurations of this implementation.

Start with the [Chinese project report](docs/PROJECT_REPORT_ZH.md),
[460-row comparison](results/optimization_validation/background_v3/physical_conventions/README.md),
and the two tables: [spin-half](results/space_groups/report/space_groups.pdf),
[spinless](results/space_groups_spinless/report/space_groups.pdf).
Formula notes are provided for [omega zero](notes/independent_space_group_formulas.pdf)
and the [Pin-minus background](notes/crystalline_spinless_formulas.pdf).
The p+ip diagnostics distinguish outgoing H1 obstructions from incoming H0
relations: [spin-half](docs/PIP_DIFFERENTIAL_DIAGNOSTICS.md),
[spinless](docs/PIP_DIFFERENTIAL_DIAGNOSTICS_SPINLESS.md).

The first convention reached all classification checkpoints in 13 min 3 s.
For the nonzero background, the checkpoint follows the integrated stacking
calculation and is **not a standalone classification timing**. Both campaigns
shared five PBS workers; elapsed times include queue delays and competing
control calculations. See the measured [spin-half](results/space_groups/performance.pdf)
and [spinless](results/space_groups_spinless/performance.pdf) performance.

The [cluster guide](docs/CLUSTER_RUN.md) gives persistent SSH reuse and fresh PBS
allocation instructions. The public repository is
[Phy-Ren/FSPT_AHSS](https://github.com/Phy-Ren/FSPT_AHSS); its publishing history
is separate from the private working history and comparison inputs.
The [background derivation](docs/CRYSTALLINE_SPINLESS_BACKGROUND.md) and
[H0 incoming quotient](docs/BACKGROUND_QUOTIENT.md) explain the second convention.

## Independence

The implementation does not load, wrap, or build upon SptSet. GAP/HAP, CrystCat,
and Polycyclic provide generic group and resolution infrastructure. The cochain
adapters, exact quotient computations, classification pipeline, and stacking
engine are independently implemented. The user's delivered obstruction and
stacking formulas are mathematical inputs. The collaborator's calibrated
cochain product supplies an additional mathematical input for the torsion
p+ip square; its universal coefficients are independently evaluated and
compiled into this implementation. Production imports no collaborator engine.
The old SptSet files may be consulted for formula conventions, including the
supplied H0 unary normalization, and for result comparisons. Production never
loads that engine or reads external answer tables.

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
AFSBackend(group), with the selected physical background
    -> decoration cycles and obstruction primitives
    -> surviving integer p+ip lattice and complete free generator towers
    -> lower-layer lifts and products; H0 incoming quotient when present
    -> upper stacking extension from that same classification object
    -> final classification, stacking results and certificates
```

The classification object retains the actual cocycles, obstruction primitives,
incoming boundaries, and marked quotient coordinates. Stacking uses that same
object to lift and multiply its generators. A layer's abstract group orders are
not sufficient input. Parallel workers handle different space groups; they do
not split these dependent stages across processes. For a nonzero background,
the H0 p+ip incoming map has higher filtered components: computing its full
image requires the actual lower-layer product. These lower relations are
therefore computed before the final classification checkpoint.
In the current nonzero-background implementation, that checkpoint follows
the integrated background stacking routine even for groups with no H0 input.
Its elapsed time is therefore not a separate classification-only benchmark.

Set `AFS_GAP=/path/to/gap` if GAP is not on your `PATH`. Run the complete pipeline with:

```sh
python3 scripts/run_group.py 6 --mode full --output runs/example/sg6.json
python3 scripts/run_group.py 6 --mode full --crystalline-spin spinless \
  --output runs/example_spinless/sg6.json
```

Use this command inside a compute-node allocation or through the task queue.
The classification-only mode exists for development checks. Separate development
campaigns may repeat classification when testing the complete pipeline.
For a nonzero background, classification-only mode still runs the integrated
background stacking routine and omits its final stacking export.

For a freshly allocated set of workers, freeze and queue the entire calculation
with the following pattern; substitute the five live queue names created by the
[cluster guide](docs/CLUSTER_RUN.md):

```sh
python3 scripts/submit_campaign.py --run runs/new_campaign \
  --queues NEW_Q1 NEW_Q2 NEW_Q3 NEW_Q4 NEW_Q5 \
  --groups 1-230 --mode full --source results/space_groups/source \
  --timings results/space_groups --timeout 27000
```

For crystalline spinless, select the physical convention explicitly and use
its own frozen source:

```sh
python3 scripts/submit_campaign.py --run runs/new_spinless_campaign \
  --queues NEW_Q1 NEW_Q2 NEW_Q3 NEW_Q4 NEW_Q5 \
  --groups 1-230 --mode full --crystalline-spin spinless \
  --source results/space_groups_spinless/source \
  --timings results/space_groups_spinless --timeout 27000
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
enough time for each queued task and cleanup. The original spin-half run preserves its
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
The classification checkpoint records the completed classification within the
same process. Its `checkpoint_stage` distinguishes the original early
classification checkpoint from the later checkpoint after the integrated
background stacking calculation. Neither path reconstructs stacking from
abstract layer orders alone.

Audit and use saved generator relations without another GAP calculation:

```sh
python3 scripts/audit_run.py results/space_groups --require-complete-witnesses \
  --require-formula-convention normalized-pip-aw-edge-transport-v2
python3 scripts/stack_result.py results/space_groups/sg219.json \
  --left '{"P1":1}' --right '{"P1":1}'
python3 scripts/audit_background_run.py results/space_groups_spinless
```

Generator coordinates belong to the specific saved presentation; labels from
different source versions need not describe the same representatives. When
`pip.free_lattice.fullFreePhaseWitness` is true, `Pfree` coordinates refer to the
exported primitive surviving lattice basis and its complete defining towers.
Earlier development files without that export describe only an abstract free
splitting. See `docs/VALIDATION.md` for the precise mathematical scope and
`docs/STATUS.md` for the current formula-correction audit.

For crystalline spin-half SG219 this returns `P1 + P1 = C1`, with `P1` of order four. In that convention all 44 groups
with nonzero free p+ip rank export an actual primitive surviving lattice basis
and complete generator towers. All 32 surviving torsion p+ip cases include the
upper phase relation. These exports do not mean that every group has undergone
the separate full comparison-support audit; completed audit cases and the
mathematical assumptions are recorded in `docs/VALIDATION.md`.

The replay command also accepts strictly audited crystalline-spinless results
when their marked relations are available. For a nontriangular H0 quotient it
returns a representative lifted through the exact inverse Smith transform;
the output labels this `smith-representative`. A unique abstract upper group
with unknown p+ip carry is insufficient for marked replay and is explicitly
rejected. It is still a determined abstract stacking group, as reported by
`scripts/report_background_results.py`; no arbitrary carry is substituted.

The accepted spin-half archive is `results/space_groups`, from `full_closed_cf_v09` with
source ID `9c16c0714da16a1ed5dc23b7830701afc01e6d7a37ee6d243f536ee4dc9ecd96`.
Use `--source results/space_groups/source` to reproduce that precise version.
The live runtime additionally supports the nonzero physical background.
Closed-CF/half-phase evaluation is enabled, the mod-two bar comparison map is
disabled, and native mod-two classification contraction remains enabled.
Source, checkpoints, task
logs, exact results, scheduling evidence and performance are retained together.

All 920 graded-layer entries match the supplied current boss PDF. Its full
stacking extensions are not supplied. The historical full-stacking comparison
has 179 equal groups, 21 changes already involving graded layers, four
same-layer extension differences, and 26 empty reference entries. The provided
Weicheng materials support finite-model checks, without an affine-230 stacking
table. Details are in the project report and `docs/STATUS.md`.
