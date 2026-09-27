# FSPT_AHSS

Independent exact computation of decoration-layer classifications and abstract
stacking groups for three-dimensional crystalline fermionic SPT phases.

The results cover all **230 space groups and 32 crystallographic point groups
in both physical spin conventions**: 524 calculations in total.
The [result tables](results/group_tables/README.md) list the four surviving
decoration layers and the final stacking group.

| Physical convention | Effective internal background | Space groups | Point groups |
|---|---|---:|---:|
| Crystalline spin-half = internal spinless | `s=w1`, `omega=0` | 230 | 32 |
| Crystalline spinless = internal spin-half | `s=w1`, `omega=w2+w1^2` | 230 | 32 |

Space-group calculations use the full infinite affine group, including
translations and weak phases. Point-group calculations use the actual finite
three-dimensional matrix group, without translations. The final group includes
the extensions between decoration layers; it is not generally their direct sum.

The implementation uses GAP/HAP, CrystCat and Polycyclic for general group and
resolution operations. It does not load or wrap SptSet. Exact integer and
rational arithmetic is used for the cochain operations and group presentations.
External answer tables are not calculation inputs.

## Running a calculation

The tested cluster environment is GAP 4.13.1, HAP 1.62, CrystCat 1.1.10,
Polycyclic 2.16, the GAP JSON package and Python 3.8.16. Set `AFS_GAP` to the GAP
executable when it is not available on `PATH`.

For one space group:

```sh
python3 scripts/run_group.py 219 --mode full --output runs/sg219.json
python3 scripts/run_group.py 219 --mode full --crystalline-spin spinless \
  --output runs/sg219_spinless.json
```

For one finite point group:

```sh
python3 scripts/run_point_group.py 10 --crystalline-spin half \
  --output runs/point10_half.json
python3 scripts/run_point_group.py 10 --crystalline-spin spinless \
  --output runs/point10_spinless.json
```

Each calculation is one sequential GAP process: it computes the classification,
then computes stacking using the same classification object. Parallelism is
across groups. The [cluster guide](docs/CLUSTER_RUN.md) describes compute-node
allocation, bounded workers and persistent SSH connection reuse.

## Results and reproducibility

The numerical archives retain exact results, classification checkpoints, frozen
GAP source, task records and file hashes:

- [Crystalline spin-half space groups](results/space_groups)
- [Crystalline spinless space groups](results/space_groups_spinless)
- [Both finite point-group conventions](results/point_groups)
- [Classification and final group tables](results/group_tables/README.md)

Use the archive's `source/` directory with `--source` to reproduce its recorded
version. Result records retain the original computation metadata. The public
tables present the associated-graded layers and final abstract group structure.

```sh
python3 scripts/audit_run.py results/space_groups
python3 scripts/audit_background_run.py results/space_groups_spinless
python3 scripts/audit_point_groups.py results/point_groups \
  --source results/point_groups/source
```

The two 230-space-group campaigns took 3 h 31 min 39 s and 3 h 47 min 35 s.
They shared compute resources; these elapsed times include queueing and other
validation tasks. The 64 finite point-group calculations took about 71 seconds
on one compute node with 28 worker slots, using 24 CPU minutes in total and a
maximum of 0.86 GiB per task. Original timings are retained with the archives.

The authoritative cluster directory is `/home/user/xyren/AllFSPT` on
`cuhk-cluster3`. The public repository is
[Phy-Ren/FSPT_AHSS](https://github.com/Phy-Ren/FSPT_AHSS).
See [public release and reproduction instructions](PUBLIC_RELEASE.md) for the
snapshot process and self-contained tests.
