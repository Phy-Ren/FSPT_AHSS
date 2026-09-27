#!/usr/bin/env python3
"""Atomically queue an argv command for the allocated compute-node worker."""
import argparse
import json
from pathlib import Path
import time
import uuid

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
ap.add_argument("--name", default="task")
ap.add_argument("--timeout", type=int, default=3600)
ap.add_argument("--queue", default="queue", help="Queue namespace under runs/")
ap.add_argument("command", nargs=argparse.REMAINDER)
a = ap.parse_args()
command = a.command[1:] if a.command and a.command[0] == "--" else a.command
if not command:
    ap.error("a command is required")
root = Path(a.root).resolve()
if not a.queue or Path(a.queue).name != a.queue:
    ap.error("queue must be a single directory name")
pending = root / "runs" / a.queue / "pending"
pending.mkdir(parents=True, exist_ok=True)
ident = "%s-%s-%s" % (time.strftime("%Y%m%dT%H%M%S"), a.name, uuid.uuid4().hex[:8])
tmp = pending / (ident + ".tmp")
tmp.write_text(json.dumps(dict(command=command, cwd=str(root), timeout_s=a.timeout, created=time.time()), indent=2) + "\n")
tmp.replace(pending / (ident + ".json"))
print(ident)
