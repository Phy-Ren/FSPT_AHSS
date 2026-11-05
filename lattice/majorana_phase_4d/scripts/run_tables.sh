#!/bin/bash
# Compute the full tables with JOBS parallel processes and compare their SHA-256 sums.
#   bash scripts/run_tables.sh [JOBS] [OUTDIR]
set -e
cd "$(dirname "$0")/.."
JOBS=${1:-8}; OUT=${2:-out}
mkdir -p "$OUT/parts"
run() {   # program total chunks name
    local prog=$1 total=$2 n=$3 name=$4
    seq 0 $((n - 1)) | xargs -P "$JOBS" -I{} sh -c \
        "lo=\$(( {} * $total / $n )); hi=\$(( ({} + 1) * $total / $n ));
         f=\$(printf '$OUT/parts/${name}_%04d.bin' {});
         if [ ! -s \$f ]; then bin/$prog \$lo \$hi \$f.tmp > \$f.log; mv \$f.tmp \$f; fi"
    cat $(ls "$OUT"/parts/${name}_*.bin | sort) > "$OUT/$name.bin"
    awk '{for (i = 1; i < NF; i++) if ($i ~ /^(vanishing|no_candidate)/) s += $(i + 1)} END {print "'"$name"': vanishing or uncovered", s + 0}' "$OUT"/parts/${name}_*.log
}
run e5_stacking 8388608 256 E5gamma_23bit
run o6_heptagon 33554432 1024 O6gamma_25bit
python3 - "$OUT" <<'PY'
import hashlib, json, sys
ref = json.load(open("data/SHA256.json"))
for f in ("E5gamma_23bit.bin", "O6gamma_25bit.bin"):
    h = hashlib.sha256(open(f"{sys.argv[1]}/{f}", "rb").read()).hexdigest()
    print(f, "matches the reference SHA-256" if h == ref[f] else "DIFFERS from the reference SHA-256")
PY
