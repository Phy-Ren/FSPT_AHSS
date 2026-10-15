#!/usr/bin/env python3
"""Run one packaged LOCAL charge-completion driver against an explicit source."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import time

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--group", type=int, choices=(141, 229), required=True)
parser.add_argument("--variant", choices=("baseline", "half"), required=True)
parser.add_argument("--lattice", choices=("koszul", "hap"), default="koszul")
parser.add_argument("--stage-timeout", type=float, default=120)
parser.add_argument("--gap", default=shutil.which("gap"))
args = parser.parse_args()
if not args.gap or args.stage_timeout <= 0:
    parser.error("GAP and a positive stage timeout are required")
if args.variant == "half" and args.lattice != "koszul":
    parser.error("The packaged half-source controls use the fixed Koszul path")
source, output = args.source.resolve(), args.output.resolve()
output.mkdir(parents=True, exist_ok=False)
snapshot = output / "snapshot"
shutil.copytree(source / "gap", snapshot / "gap")
case = f"spacegroup_{args.group:03d}_spin_half"
inputs = snapshot / "insulator_catalog/generated"
inputs.mkdir(parents=True)
shutil.copyfile(source / "insulator_catalog/generated" / (case + ".g"), inputs / (case + ".g"))
folder = (HERE / "baseline_lattice" if args.variant == "baseline" else HERE) / (case + "_" + args.lattice)
text = (folder / "driver.g").read_text()
text = re.sub(r'^U1_ROOT:="[^"]*"', lambda match: "U1_ROOT:=" + json.dumps(str(snapshot)), text, count=1)
for filename in ("lower.json", "completed_roots.json", "result.json"):
    text = re.sub(r'"[^"\n]*/' + filename.replace(".", r"\.") + r'"', lambda match: json.dumps(str(output / filename)), text)
(output / "driver.g").write_text(text)
hashes = {str(p.relative_to(snapshot)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(snapshot.rglob("*")) if p.is_file()}
(output / "snapshot_hashes.json").write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n")
command = [args.gap, "-q", "-b", "-o", "4g", str(output / "driver.g")]
started = stage_start = time.monotonic()
phase, interrupted = "setup", False
with (output / "stdout.log").open("wb") as out, (output / "stderr.log").open("wb") as err:
    child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=out, stderr=err, start_new_session=True)
    while child.poll() is None:
        raw = (output / "stdout.log").read_bytes()
        latest = "completion" if b"STAGE_STARTED completion" in raw else "primary" if b"STAGE_STARTED primary" in raw else "setup"
        if latest != phase:
            phase, stage_start = latest, time.monotonic()
        if time.monotonic() - stage_start >= args.stage_timeout:
            interrupted = True
            child.send_signal(signal.SIGINT)
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
            break
        time.sleep(.15)
record = {"command": command, "elapsedSeconds": time.monotonic() - started,
          "lastStage": phase, "interruptedAtBound": interrupted,
          "exitCode": child.returncode, "complete": (output / "result.json").is_file()}
(output / "run.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, sort_keys=True))
