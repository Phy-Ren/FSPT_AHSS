#!/usr/bin/env python3
"""Check immutable deployment provenance and coverage, never process state."""
import hashlib
import json
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def verify():
    manifest = read(BASE / "manifest.json")
    actual = {str(p.relative_to(BASE)) for p in BASE.rglob("*")
              if p.is_file() and p.name != "manifest.json" and "__pycache__" not in p.parts}
    assert actual == set(manifest["filesSHA256"])
    for name, digest in manifest["filesSHA256"].items():
        assert sha((BASE / name).read_bytes()) == digest, name
    plan = read(BASE / "plan.json")
    plan_hash = sha((BASE / "plan.json").read_bytes())
    remote = read(BASE / "remote_verification.json")
    origins = read(BASE / "metadata_origins.json")
    prefix = "/home/user/xyren/AllFSPT_insulator/"
    for local, original in origins.items():
        assert original.startswith(prefix)
        assert sha((BASE / local).read_bytes()) == remote["metadataFilesSHA256"][original[len(prefix):]]
    assert remote["sourceFilesVerified"] and remote["noProcessSignalsOrClassificationLaunch"]
    assert remote["sourceManifestSHA256"] == plan["sourceSHA256"]
    assert remote["snapshotArchiveSHA256"] == plan["snapshotSHA256"]
    reused = read(BASE / "vm_reuse.json")
    assert reused["originalBuild"] == read(BASE / "original_vm_build.json")
    assert reused["binarySHA256"] == reused["originalBuild"]["binarySHA256"] == remote["formulaLibrarySHA256"]
    source = read(BASE / "nodes/n02/source.json")
    assert source["files"] == remote["sourceFilesSHA256"]
    assert source["sha256"] == plan["sourceSHA256"]
    assert sha(json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()) == source["sha256"]
    for name, digest in source["files"].items():
        blob = subprocess.check_output(["git", "show", plan["sourceCommit"] + ":" + name], cwd=REPO)
        assert sha(blob) == digest, name
    original_build = reused["originalBuild"]
    assert source["files"]["insulator/_compiled/u1_dag_vm.cpp"] == original_build["sourceSHA256"]
    for name, digest in original_build["integerDAGs"].items():
        assert source["files"]["insulator/_compiled/" + name] == digest
    expected_reused = {"insulator/_compiled/u1_dag_vm.cpp", "insulator/_compiled/source3.json", "insulator/_compiled/product3.json"}
    assert set(reused["sourceFilesEqual"]) == expected_reused
    launched = set()
    pid_expected = {"n02": 40405, "n03": 38671, "n08": 9271}
    for shard in plan["shards"]:
        node = shard["node"]
        launch = read(BASE / "nodes" / node / "launch.json")
        assert all(launch[k] == v for k, v in shard.items()), node
        assert launch["pid"] == pid_expected[node] and launch["state"] == "launched"
        assert launch["planSHA256"] == plan_hash and launch["sourceCommit"] == plan["sourceCommit"]
        assert launch["snapshotSHA256"] == plan["snapshotSHA256"]
        assert launch["source"] == source == read(BASE / "nodes" / node / "source.json")
        runtime = read(BASE / "nodes" / node / "formula_runtime.json")
        assert launch["formulaRuntime"] == runtime and launch["vmReuse"] == reused
        assert runtime["libraryPresent"] and runtime["librarySHA256"] == reused["binarySHA256"]
        assert runtime["requestedMode"] == "auto"
        selected = read(BASE / "nodes" / node / "selection.json")
        assert len(selected) == len(set(selected)) == shard["caseCount"]
        assert set(selected) == set(shard["cases"])
        assert launched.isdisjoint(selected)
        launched.update(selected)
        command_cases = [launch["command"][i + 1] for i, word in enumerate(launch["command"]) if word == "--case"]
        assert command_cases == shard["cases"]
    preserved = set()
    for entry in plan["preservation"]:
        node = Path(entry["path"]).parent.name.split("-")[-2]
        path = BASE.parent / "preserved_d/nodes" / node / "recovery.json"
        assert sha(path.read_bytes()) == entry["sha256"]
        ledger = read(path)
        assert ledger["preservedCases"] == entry["cases"] and preserved.isdisjoint(entry["cases"])
        preserved.update(entry["cases"])
    pilots = {case for pilot in plan["pilots"] for case in pilot["cases"]} - preserved
    smoke = set(plan["completedSmoke"]["cases"]) - preserved - pilots
    groups = {"preservedD": preserved, "reservedFPilot": pilots, "completedEOnly": smoke, "launchedG": launched}
    partition = read(BASE / "coverage_partition.json")
    for name, values in groups.items():
        assert set(partition[name]) == values and len(values) == partition["counts"][name]
    universe = {"spacegroup_%03d_%s" % (n, spin) for n in range(1, 231) for spin in ("spinless", "spin_half")}
    assert set.union(*groups.values()) == universe
    assert sum(map(len, groups.values())) == len(universe) == partition["totalCases"] == 460
    assert len(launched) == plan["remainingCount"] == 201
    finalizer_origins = read(BASE / "finalizers/origins.json")
    finalizer_capture = read(BASE / "finalizers/remote_verification.json")
    for name, original in finalizer_origins.items():
        assert sha((BASE / "finalizers" / name).read_bytes()) == finalizer_capture["filesSHA256"][original]
        if name.endswith("-launch.json"):
            row = read(BASE / "finalizers" / name)
            assert row["state"] == "launched" and type(row["pid"]) is int and row["pid"] > 0
            cmd = row["command"]
            assert cmd[1] == prefix + "snapshots/u1_finalize_campaign_20261015.py"
            node = cmd[cmd.index("--node") + 1]
            assert row["node"] == node
            if name.startswith("sgfull-20261015-g-"):
                assert int(cmd[cmd.index("--runner-pid") + 1]) == pid_expected[node]
                assert cmd[cmd.index("--source-tag") + 1] == "sgfull-20261015-g"
    return {"verified": True, "counts": partition["counts"], "sourceFilesCheckedAgainstGit": len(source["files"]),
            "recordedPIDs": pid_expected, "completionClaimedForLaunchedJobs": False}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
