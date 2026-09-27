#!/usr/bin/env python3
"""Replay accepted marked relations; no GAP or cochain calculation is run.

This checks the relation-algebra consumer against the archived presentation.
It is not a substitute for the archive's mathematical/cochain audit.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.stacking import PresentedStackingGroup, UnresolvedStacking


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run(directory):
    archive_raw = (directory / "archive.json").read_bytes()
    archive = json.loads(archive_raw)
    records, sources, conventions = [], set(), set()
    for sg in range(1, 231):
        name = f"sg{sg}.json"
        raw = (directory / name).read_bytes()
        digest = sha(raw)
        require(digest == archive["files"][name]["sha256"], f"hash mismatch: {name}")
        result = json.loads(raw)
        require(result["space_group"] == sg and result["status"] == "computed",
                f"incomplete or wrong group: {name}")
        require(result["formula_convention"] == "normalized-pip-aw-edge-transport-v2",
                f"wrong formula convention: {name}")
        sources.add(result["source_id"])
        conventions.add(result["convention"])
        stacking = result["stacking"]
        require(result["source_id"] == archive["source_id"], f"archive source mismatch: {name}")
        require(stacking["status"] == "computed", f"incomplete stacking: {name}")
        if "pipExtensionCertificate" in stacking:
            require(stacking.get("fullUpperPhaseWitness") is False,
                    f"unexpected family witness scope: {name}")
            try:
                PresentedStackingGroup(result)
            except UnresolvedStacking:
                records.append(dict(space_group=sg, result_sha256=digest,
                                    status="abstract-family-correctly-refused"))
                continue
            raise ValueError(f"unknown marked carry silently accepted: {name}")
        group = PresentedStackingGroup(result)
        free = group.free_rank
        names = group.generator_names
        lower_names = names[free:]
        if "fullPresentation" in stacking:
            rows = stacking["fullPresentation"]
            transform = stacking["fullSmithColumnTransform"]
            diagonal = stacking["fullSmithDiagonal"]
        else:
            rows = stacking["lower"]["presentation"]
            transform = stacking["lower"]["smithColumnTransform"]
            diagonal = stacking["lower"]["smithDiagonal"]
        diagonal = [abs(x) for x in diagonal] + [0] * (len(lower_names)-len(diagonal))
        zero = (0,) * len(group.invariants)
        for index, row in enumerate(rows):
            coefficients = dict(zip(lower_names, row))
            require(group.canonical(coefficients) == zero,
                    f"nonzero relation canonical image: SG{sg} row {index}")
            require(group.stack_marked(coefficients, {}) == {},
                    f"nonzero relation marked replay: SG{sg} row {index}")
        for case in range(4):
            # Deterministic signs and large exact integers, without phase enumeration.
            scale = 1 if case < 3 else (1 << 70) + 3
            left = {n: (-1 if (i+case) % 2 else 1) * (sg+i+1) * scale
                    for i, n in enumerate(names)}
            right = {n: (-1 if (i+case) % 3 else 1) * (2*i+case+1)
                     for i, n in enumerate(names)}
            marked = group.stack_marked(left, right)
            canonical = group.stack(left, right)
            require(group.canonical(marked) == canonical,
                    f"marked/canonical mismatch: SG{sg} case {case}")
            require(all(marked.get(n, 0) == left[n]+right[n] for n in names[:free]),
                    f"free coordinate changed: SG{sg} case {case}")
            # Independent lattice-membership check using the archived Smith map.
            difference = [left[n]+right[n]-marked.get(n, 0) for n in lower_names]
            smith_difference = [sum(difference[i]*transform[i][j]
                                    for i in range(len(lower_names)))
                                for j in range(len(lower_names))]
            require(all(x % d == 0 if d else x == 0
                        for x, d in zip(smith_difference, diagonal)),
                    f"returned representative changed the coset: SG{sg} case {case}")
            inverse = {n: -v for n, v in left.items()}
            require(group.stack_marked(left, inverse) == {},
                    f"integer inverse replay failed: SG{sg} case {case}")
        records.append(dict(space_group=sg, result_sha256=digest,
                            status="marked-relation-replay-passed",
                            saved_relation_count=len(rows), coordinate_cases=4,
                            marked_reduction=group.marked_reduction,
                            free_generator_scope=group.free_generator_scope))
    require(len(sources) == 1 and len(conventions) == 1, "mixed archive sources/conventions")
    return dict(schema=1, status="passed", scope="persisted-relation-algebra-only",
                cochains_recomputed=False, gap_executed=False,
                source_id=sources.pop(), convention=conventions.pop(),
                archive_sha256=sha(archive_raw),
                consumer_sha256=sha((ROOT / "fspt/stacking.py").read_bytes()),
                replay_script_sha256=sha(Path(__file__).read_bytes()),
                group_count=len(records),
                marked_groups=sum(r["status"] == "marked-relation-replay-passed" for r in records),
                refused_abstract_families=sum(r["status"] == "abstract-family-correctly-refused" for r in records),
                saved_relations=sum(r.get("saved_relation_count", 0) for r in records),
                records=records)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = run(args.archive)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in evidence.items() if k != "records"}, indent=2))
