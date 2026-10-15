#!/bin/bash
set -euo pipefail
export PATH=/home/user/xyren/AllFSPT_insulator/runtime/bin:$PATH
export LC_ALL=C LANG=C OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
exec python3 /home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-e/scripts/classify.py --output /home/user/xyren/AllFSPT_insulator/runs/sgfull-20261015-e-smoke --gap /home/user/xyren/software/gap-4.13.1-o2-20261015/gap-o2 --jobs 3 --memory 3g --timeout 3600 --pair-spins --largest-first --case spacegroup_014_spinless --case spacegroup_014_spin_half --case spacegroup_166_spinless --case spacegroup_166_spin_half --case spacegroup_214_spinless --case spacegroup_214_spin_half
