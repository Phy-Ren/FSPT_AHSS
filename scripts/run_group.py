#!/usr/bin/env python3
"""Compute one group with fresh output and preserve source and timing provenance."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("group", type=int)
ap.add_argument("--output", required=True)
ap.add_argument("--mode", choices=["classification", "full"], default="full",
                help="Full sequential classification and stacking (default); classification is a development check")
ap.add_argument("--source", help="Immutable source snapshot containing gap/")
a = ap.parse_args()
if not 1 <= a.group <= 230:
    ap.error("space group must be 1..230")
root = Path(__file__).resolve().parents[1]
out = Path(a.output).resolve()
out.parent.mkdir(parents=True, exist_ok=True)
if out.exists():
    ap.error("output exists; use a new run directory to preserve provenance")
raw = out.with_suffix(".raw.json")
if raw.exists():
    ap.error("raw output exists; use a new run directory")
if a.source:
    source = Path(a.source).resolve()
else:
    # Development edits may continue while GAP runs. Freeze the whole runtime
    # before startup, including stacking loaded after classification completes.
    source = out.with_suffix(".source")
    if source.exists():
        ap.error("source snapshot exists; use a new run directory")
    shutil.copytree(root / "gap", source / "gap")
driver = out.with_suffix(".g")
source_files = sorted((source / "gap").glob("*.g"))
hashes = {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files}
source_id = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
checkpoint = out.parent / "classification" / out.name
checkpoint.parent.mkdir(parents=True, exist_ok=True)
text = 'AFS_ROOT := %s;;\nAFS_SG := %d;;\nAFS_OUT := %s;;\nAFS_MODE := %s;;\nAFS_CLASS_OUT := %s;;\nAFS_SOURCE_ID := %s;;\nRead(%s);\n' % (json.dumps(str(source)), a.group, json.dumps(str(raw)), json.dumps(a.mode), json.dumps(str(checkpoint)), json.dumps(source_id), json.dumps(str(source / "gap" / "run_one.g")))
driver.write_text(text)
start = time.time()
rc = subprocess.call([sys.executable, str(root / "scripts" / "run_gap.py"), "--sentinel", "AFS_RESULT_WRITTEN", str(driver)])
if rc or not raw.exists():
    sys.exit(rc or 1)
result = json.loads(raw.read_text())
if result.get("space_group") != a.group:
    raise ValueError("wrong space group in result")
result.update(wall_seconds=time.time()-start, source_sha256=hashes, source_id=source_id, source_snapshot=str(source), started=start, finished=time.time(), mode=a.mode)
temp = out.with_suffix(".tmp")
temp.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
temp.replace(out)
print("AFS_GROUP_SAVED", a.group, result["status"], str(out), flush=True)
