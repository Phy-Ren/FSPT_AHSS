#!/usr/bin/env python3
"""Verify the archived exact comparisons without launching a classification."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PERFORMANCE_FIELDS = {"resolutionBuildTimings", "formulaWorkerCalls", "formulaCacheStats"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(first, second, ignored=PERFORMANCE_FIELDS):
    a, b = [json.loads(p.read_text())["classification"] for p in (first, second)]
    assert a.keys() == b.keys(), "Classification field sets changed"
    checked = []
    for key in a:
        if key not in ignored:
            assert a[key] == b[key], (str(first), key)
            checked.append(key)
    return len(checked)


def main():
    counts = {}
    for operation in ("closed_charge", "cup"):
        counts[operation] = []
        for spin in ("spin_half", "spinless"):
            name = "spacegroup_195_" + spin + ".json"
            counts[operation].append(compare(ROOT / operation / "baseline" / name,
                                             ROOT / operation / "candidate" / name))
    assert "CLOSED_CHARGE_SOURCE_POINTWISE_CHECKS 9664 EVEN_NATIVE_ZERO 60" in (ROOT / "closed_charge/check.log").read_text()
    assert "NONABELIAN_CUP_EXACT_CHECKS 19440" in (ROOT / "cup/nonabelian_check.log").read_text()
    for name, expected in json.loads((ROOT / "cup/peer_review/result.json").read_text())["hashes"].items():
        assert sha(ROOT / "cup/cup_candidate" / name) == expected
    if (ROOT / "sg221/baseline/result.json").is_file():
        counts["sg221"] = compare(ROOT / "sg221/baseline/result.json", ROOT / "sg221/candidate/result.json",
                                   {"resolutionBuildTimings"})
    manifest = ROOT / "package_manifest.json"
    if manifest.is_file():
        for name, expected in json.loads(manifest.read_text())["files"].items():
            assert sha(ROOT / name) == expected, name
    print(json.dumps({"status": "pass", "literalFieldsComparedPerCase": counts}, indent=2))


if __name__ == "__main__":
    main()
