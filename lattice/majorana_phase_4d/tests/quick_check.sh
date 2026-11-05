#!/bin/bash
# Quick self-test: evaluator, table slices, and short runs of the three checks.
set -e
cd "$(dirname "$0")/.."
JOBS=${1:-8}
bin/test_gauss | tail -1
python3 - <<'PY'
import json, subprocess, numpy as np
g = json.load(open("tests/golden.json"))
for f, v in g.items():
    prog = "bin/e5_stacking" if v["table"] == "E5" else "bin/o6_heptagon"
    subprocess.run([prog, str(v["first"]), str(v["first"] + v["count"]), "/tmp/_golden.bin"], check=True, capture_output=True)
    a, b = np.fromfile("/tmp/_golden.bin", dtype=np.int8), np.fromfile("tests/" + f, dtype=np.int8)
    print(f"{v['table']} rows {v['first']}..{v['first'] + v['count']}:", "equal to the reference" if (a == b).all() else "DIFFERENT")
    assert (a == b).all()
PY
mkdir -p out
[ -s out/E5gamma_23bit.bin ] && [ -s out/O6gamma_25bit.bin ] || { echo "(full tables not in out/: run 'make tables' for the three checks)"; exit 0; }
python3 scripts/check_stacking.py out/E5gamma_23bit.bin out/O6gamma_25bit.bin 7340032 7344128 --jobs "$JOBS"
python3 scripts/check_o6_formula.py out/O6gamma_25bit.bin --samples 2000 --jobs "$JOBS"
python3 scripts/check_e5_formula.py out/E5gamma_23bit.bin 7340032 7344128 --jobs "$JOBS"
