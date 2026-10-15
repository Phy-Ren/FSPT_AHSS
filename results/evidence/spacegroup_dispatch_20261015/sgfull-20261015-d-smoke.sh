#!/bin/bash
set -euo pipefail
export PATH=/home/user/xyren/AllFSPT_insulator/runtime/bin:$PATH
export LC_ALL=C LANG=C OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
exec python3 /home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-c/scripts/classify.py --output /home/user/xyren/AllFSPT_insulator/runs/sgfull-20261015-d-smoke --gap /home/user/xyren/software/gap-4.13.1-o2-20261015/gap-o2 --jobs 2 --memory 4g --timeout 3600 --pair-spins --case spacegroup_014_spinless --case spacegroup_014_spin_half --case spacegroup_019_spinless --case spacegroup_019_spin_half
