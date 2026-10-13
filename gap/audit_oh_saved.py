#!/usr/bin/env python3
"""Recheck saved Oh native equations and subgroup maps without classification."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("insulator_runner", ROOT / "scripts/classify.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=ROOT / "results/three_dimensional_20261013/results.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("The output already exists; choose a new immutable audit path")
    rows = json.loads(args.results.read_text())
    selected = {}
    input_hashes = {}
    for index in (15, 29, 30, 31, 32):
        identity = f"point3_{index:02}_spinless"
        matches = [row for row in rows if row["input"]["id"] == identity]
        if len(matches) != 1:
            parser.error(f"Expected exactly one saved {identity} result")
        selected[f"p{index}"] = matches[0]["classification"]
        input_hashes[identity] = digest(ROOT / "insulator_catalog/generated" / f"{identity}.g")
    with tempfile.TemporaryDirectory(prefix="u1-oh-audit-") as directory:
        tmp = Path(directory)
        raw = tmp / "audit.json"
        script = tmp / "audit.g"
        script.write_text(
            'OnBreak:=function() Where(10);QUIT_GAP(1);end;;\n'
            f'U1_ROOT:={runner.gap_literal(str(ROOT))};;Read(Concatenation(U1_ROOT,"/gap/load.g"));\n'
            f'U1_OH_SAVED:={runner.gap_literal(selected)};;\n'
            f'U1_OH_AUDIT_OUT:={runner.gap_literal(str(raw))};;\n'
            'Read(Concatenation(U1_ROOT,"/gap/audit_oh.g"));QUIT_GAP(0);\n'
        )
        process = subprocess.run(["gap", "-q", "-b", str(script)], capture_output=True, text=True, timeout=300)
        if process.returncode or not raw.exists():
            raise RuntimeError(process.stdout + process.stderr)
        audit = json.loads(raw.read_text())
    audit["provenance"] = {
        "saved_results_path": str(args.results.resolve()),
        "saved_results_sha256": digest(args.results),
        "catalog_gap_inputs_sha256": input_hashes,
        "audit_runner_sha256": digest(__file__),
        "current_backend_source_manifest": runner.source_manifest(),
        "verification": "Recomputed exact native equations, charge gauge and subgroup maps; did not rerun complete classification",
        "gap_stdout": process.stdout,
        "gap_stderr": process.stderr,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(audit, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"output": str(args.output), "checks": audit["checks"],
                      "subgroup_phase_image_ranks": {item["name"]: item["finalPhaseImageRank"] for item in audit["subgroups"]}}))


if __name__ == "__main__":
    main()
