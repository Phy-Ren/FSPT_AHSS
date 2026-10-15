#!/bin/bash
set -euo pipefail
export LC_ALL=C LANG=C OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export PATH=/home/user/xyren/AllFSPT_insulator/runtime/bin:/home/user/xyren/miniforge3/envs/gap-centos6/bin:$PATH
cd /home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-f
python3 scripts/build_formula_vm.py --compiler 'g++ -Wl,-rpath,/home/user/xyren/miniforge3/envs/gap-centos6/lib' --metadata /home/user/xyren/AllFSPT_insulator/runs/sgfull-20261015-f-vm-build.json
python3 -m unittest discover -s tests -p test_compiled_source3.py -v
