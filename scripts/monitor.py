#!/usr/bin/env python3
"""Read-only compact campaign monitor, including explicit failures/unresolved cases."""
import argparse
from collections import Counter
import json
from pathlib import Path
import time

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
ap.add_argument("--queue", default="queue")
ap.add_argument("--prefix", default="", help="Only show tasks with this ID prefix")
a = ap.parse_args()
root = Path(a.root)
worker = root / "runs" / a.queue / "worker.json"
if worker.exists():
    w = json.loads(worker.read_text())
    print("worker", w["hostname"], w["pbs_job"], "controller_minus_heartbeat_s", round(time.time()-w["heartbeat"], 1), "active", len(w["active"]), "slots", w["slots"])
counts = Counter()
for path in sorted((root / "runs" / "tasks").glob("*/status.json")):
    if not path.parent.name.startswith(a.prefix):
        continue
    data = json.loads(path.read_text())
    if data.get("queue", "queue") != a.queue:
        continue
    counts[data["status"]] += 1
    if data["status"] in ("running", "failed", "timeout", "launch_error", "worker_stopped"):
        now = w["heartbeat"] if worker.exists() else time.time()
        print(data["status"], path.parent.name, "elapsed_s", round(data.get("elapsed_s", now-data.get("started", now)), 1))
print("tasks", dict(counts))
print("pending", len(list((root / "runs" / a.queue / "pending").glob("*.json"))))
