#!/usr/bin/env python3
"""Collect independent campaign outputs. No external classification is loaded."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("run")
ap.add_argument("--write", action="store_true")
a = ap.parse_args()
base = Path(a.run).resolve()
results = {}
for path in base.glob("sg*.json"):
    if ".raw." in path.name:
        continue
    data = json.loads(path.read_text())
    results[data["space_group"]] = data
computed = [n for n, d in results.items() if d["status"] == "computed"]
unresolved = [n for n, d in results.items() if d["status"] != "computed"]
missing = sorted(set(range(1, 231)) - results.keys())
summary = dict(computed=len(computed), unresolved=sorted(unresolved), missing=missing,
               observed_cpu_hours=sum(d.get("total_cpu_ms", d["cpu_ms"]) for d in results.values())/3600000,
               max_group_wall_seconds=max((d["wall_seconds"] for d in results.values()), default=0),
               source_ids=sorted({d.get("source_id", "legacy-probe") for d in results.values()}))
for layer in ("majorana", "complex_fermion", "bosonic"):
    summary[layer + "_histogram"] = dict(Counter(str(d[layer]) for d in results.values()))
summary["pip_histogram"] = dict(Counter(str(d["pip"]["orders"]) for d in results.values() if d["pip"]["status"] == "computed"))
if any("stacking" in d for d in results.values()):
    summary["stacking_status"] = dict(Counter(d.get("stacking", {}).get("status", "missing") for d in results.values()))
    summary["stacking_histogram"] = dict(Counter(str(d["stacking"]["invariants"]) for d in results.values() if d.get("stacking", {}).get("status") == "computed"))
summary["slowest"] = sorted([dict(group=n,wall_seconds=d["wall_seconds"],cpu_ms=d["cpu_ms"]) for n,d in results.items()], key=lambda x:x["wall_seconds"], reverse=True)[:10]
print(json.dumps(summary, indent=2, sort_keys=True))
if a.write:
    (base / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True)+"\n")
    with (base / "classification.csv").open("w", newline="") as stream:
        out = csv.writer(stream)
        out.writerow(["space_group", "status", "pip", "majorana", "complex_fermion", "bosonic", "wall_seconds", "cpu_ms", "source_id"])
        for n in range(1, 231):
            if n not in results:
                out.writerow([n, "missing", "", "", "", "", "", "", ""])
            else:
                d = results[n]
                out.writerow([n,d["status"],json.dumps(d["pip"]["orders"]),json.dumps(d["majorana"]),json.dumps(d["complex_fermion"]),json.dumps(d["bosonic"]),d["wall_seconds"],d["cpu_ms"],d.get("source_id", "")])
