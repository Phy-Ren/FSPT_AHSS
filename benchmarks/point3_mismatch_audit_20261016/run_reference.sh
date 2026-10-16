#!/bin/bash
set -eu
export LC_ALL=C LANG=C OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
export PATH=/home/user/xyren/AllFSPT_insulator/runtime/bin:$PATH
cd /home/user/xyren/AllFSPT_insulator/mismatch_audit_20261016/source
exec /home/user/xyren/AllFSPT_insulator/runtime/bin/python3 scripts/classify_3p1d.py --case point3_06_spin_half --case point3_24_spin_half --case point3_32_spinless --jobs 3 --memory 8g --timeout 1200 --charge-primary bar --phase-class native --closed-charge-source reference --vacuum-reduction reference --formula-mode reference --gap /home/user/xyren/software/gap-4.13.1-o2-20261015/gap-o2 --output /home/user/xyren/AllFSPT_insulator/mismatch_audit_20261016/reference_run
