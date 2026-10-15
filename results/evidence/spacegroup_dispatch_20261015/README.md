# Full affine campaign dispatch

These are immutable launch and cancellation records, not accepted classification results. The D campaign selects exactly 460 distinct inputs: all 230 rank-three space groups for spinless and spin-half electrons. It runs the source snapshot C at commit `80d565de744bbd5ef6ac4cca3530511f549547f4`, using the separately validated optimized GAP kernel.

| Node | Selected inputs | Paired GAP processes | Per-process GAP cap |
|---|---:|---:|---:|
| n02 | 164 | 40 | 8 GiB |
| n03 | 164 | 40 | 8 GiB |
| n08 | 132 | 32 | 3 GiB |

The cap is a limit, not reserved memory or a measured peak. Each process also has one persistent exact Python worker. Spin pairs share permitted geometry and linear algebra while retaining independent extensions and states. The plan records all case assignments; the runtime manifest records source, executable, package and environment identities. The [performance archive](../../spacegroup_campaign_20261015/performance/README.md) separates exact comparison evidence from timing measurements.

The B campaign was stopped only for this project's recorded process groups. Its two completed SG195 inputs were preserved, along with all interrupted raw outputs. The compressed cancellation records give the actual process IDs and case statuses. Their replacement field names the source snapshot C; D is the production run using that source with the optimized GAP kernel.

`finalize_sgfull_d.py` waits for its owned shard to exit, requires every selected case to be complete, computes the E8 extension from those exact CI records, and archives both roots. It never accepts a partial shard. Final table acceptance is a separate step in `scripts/collect_expansion.py`, including source/input hashes, completed native records, exact E8 parents, independent Smith reductions and presentation-filling checks.

The finalizer's E8 extension implements the selected three-dimensional neutral section. These dispatch records make no new claim about physical-spectrum identification. A later run or retry must have its own directory and source manifest.
