#!/usr/bin/env python3
"""Run complete matched-coordinate classification and stacking for one space group."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.finite_examples import gap_literal
from fspt.full_run import freeze_runtime, publish_result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("group", type=int)
    parser.add_argument("--crystalline-spin", choices=("half", "spinless"), default="half")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--gap", default=os.environ.get("AFS_GAP") or shutil.which("gap"))
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--cf-primary", choices=("bar", "native", "compare"), default="native")
    parser.add_argument("--mc-primary", choices=("bar", "native", "compare"), default="native")
    parser.add_argument("--mc-n0-kernel", action="store_true",
                        help="Use the exact compiled Majorana cylinder when the integer field vanishes.")
    parser.add_argument("--cf-n0-kernel", action="store_true",
                        help="Use the exact compiled fermion cylinder when both lower fields vanish.")
    parser.add_argument("--vector-request-cache", action="store_true")
    parser.add_argument("--pure-cf-source", action="store_true",
                        help="Use the exact composed d3 source when integer and Majorana fields vanish.")
    parser.add_argument("--n0-source", action="store_true",
                        help="Use the exact composed d3 source for a legal tower with zero integer field.")
    parser.add_argument("--closed-cf-source", action="store_true",
                        help="Use the certified direct d3 closed-CF source for marked native cocycle lifts.")
    parser.add_argument("--mc-partial-cache-limit", type=int, default=0,
                        help="Retain up to this many exact n=0 partial Majorana states and source projections (0 disables).")
    parser.add_argument("--f2-parity-filter", action="store_true",
                        help="Filter exact even/duplicate coefficients before F2 cochain evaluation.")
    args = parser.parse_args()
    if not 0 <= args.mc_partial_cache_limit <= 1024:
        parser.error("Partial Majorana cache limit must be between 0 and 1024.")
    if not 1 <= args.group <= 230 or not args.gap:
        parser.error("Provide a space-group number 1..230 and --gap/AFS_GAP.")
    if args.output.exists():
        parser.error("Output exists; use a fresh result path to retain provenance.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    source, provenance = freeze_runtime(ROOT)
    started = time.time()
    with tempfile.TemporaryDirectory(prefix="fspt-complete-sg-") as directory:
        work = Path(directory)
        settings = {"AFS_ROOT": str(source), "AFS_SG": args.group,
                    "AFS_CRYSTALLINE_SPIN": args.crystalline_spin,
                    "AFS_FULL_PYTHON": args.python, "AFS_STACK_AUDIT": args.audit,
                    "AFS_FULL_CF_PRIMARY": args.cf_primary,
                    "AFS_FULL_MC_PRIMARY": args.mc_primary,
                    "AFS_FULL_MAJORANA_N0_KERNEL": args.mc_n0_kernel,
                    "AFS_FULL_FERMION_N0_KERNEL": args.cf_n0_kernel,
                    "AFS_FULL_VECTOR_REQUEST_CACHE": args.vector_request_cache,
                    "AFS_FULL_PURE_CF_SOURCE": args.pure_cf_source,
                    "AFS_FULL_N0_SOURCE": args.n0_source,
                    "AFS_FULL_CLOSED_CF_SOURCE": args.closed_cf_source,
                    "AFS_FULL_MC_PARTIAL_CACHE_LIMIT": args.mc_partial_cache_limit,
                    "AFS_FULL_F2_PARITY_FILTER": args.f2_parity_filter,
                    "AFS_OUT": str(work / "raw.json")}
        driver = "".join(k + ":=" + gap_literal(v) + ";;\n" for k, v in settings.items())
        driver += 'Read(Concatenation(AFS_ROOT,"/gap/run_full_space_group.g"));\n'
        (work / "driver.g").write_text(driver)
        process = subprocess.Popen([args.gap, "-q", "-r", "-b", "-T", str(work / "driver.g")],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        complete, error = False, False
        for line in process.stdout:
            print(line, end="", flush=True)
            complete |= "AFS_FULL_SPACE_GROUP_COMPLETE" in line
            error |= line.startswith(("Error,", "Syntax error:"))
        if process.wait() or not complete or error:
            raise SystemExit("Complete space-group calculation failed.")
        result = json.loads((work / "raw.json").read_text())
    result.update(provenance)
    result["pureCFSource3Kernel"] = args.pure_cf_source
    result["n0Source3Kernel"] = args.n0_source
    result.update(started=started, finished=time.time(), wall_seconds=time.time() - started)
    publish_result(args.output, result)


if __name__ == "__main__":
    main()
