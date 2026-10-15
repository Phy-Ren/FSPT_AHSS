#!/bin/bash
set -euo pipefail
export LC_ALL=C LANG=C OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export PATH=/home/user/xyren/AllFSPT_insulator/runtime/bin:$PATH
exec python3 /home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-f/scripts/classify.py --output /home/user/xyren/AllFSPT_insulator/runs/sgfull-20261015-f-n02-pilot --gap /home/user/xyren/software/gap-4.13.1-o2-20261015/gap-o2 --jobs 2 --memory 8g --timeout 3600 --pair-spins --largest-first --charge-primary native --phase-class cycles --case spacegroup_141_spin_half --case spacegroup_141_spinless --case spacegroup_221_spin_half --case spacegroup_221_spinless
