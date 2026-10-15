#!/usr/bin/env python3
"""Verify the frozen H launch and coverage; do not infer job completion."""
import hashlib
import json
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[2]
REMOTE = "/home/user/xyren/AllFSPT_insulator/"


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
    plan, expected, source = (read(BASE / name) for name in ("plan.json", "expected.json", "source.json"))
    launch = read(BASE / "launch.json")
    remote = read(BASE / "remote_verification.json")
    origins = read(BASE / "metadata_origins.json")
    for local, original in origins.items():
        assert original.startswith(REMOTE)
        assert sha((BASE / local).read_bytes()) == remote["metadataFilesSHA256"][original[len(REMOTE):]]
    assert remote["sourceFilesVerified"] and remote["noProcessSignalsOrClassificationLaunch"]
    assert source == expected["source"] == launch["source"]
    assert source["files"] == remote["sourceFilesSHA256"]
    assert source["sha256"] == plan["sourceSHA256"] == remote["sourceManifestSHA256"]
    assert sha(json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()) == source["sha256"]
    assert expected["archiveSHA256"] == plan["snapshotSHA256"] == remote["snapshotArchiveSHA256"] == launch["snapshotSHA256"]
    assert expected["sourceCommit"] == plan["sourceCommit"] == launch["sourceCommit"]
    for name, digest in source["files"].items():
        blob = subprocess.check_output(["git", "show", plan["sourceCommit"] + ":" + name], cwd=REPO)
        assert sha(blob) == digest, name
    runtime = read(BASE / "formula_runtime.json")
    reuse = read(BASE / "vm_reuse.json")
    library = read(BASE / "formula_library_verification.json")
    assert runtime == launch["formulaRuntime"] == reuse["formulaRuntime"] == remote["formulaRuntime"]
    assert runtime["libraryPresent"] and runtime["requestedMode"] == "auto"
    assert library["verified"] and library["libraryPath"] == runtime["libraryPath"]
    assert library["actualLibrarySHA256"] == library["declaredLibrarySHA256"] == runtime["librarySHA256"]
    assert reuse["sourceCommit"] == plan["sourceCommit"] and reuse["sourceSHA256"] == source["sha256"]
    assert reuse["archiveSHA256"] == expected["archiveSHA256"]
    old_vm = read(BASE.parent / "deployment_g/vm_reuse.json")
    assert old_vm["binarySHA256"] == runtime["librarySHA256"]
    old_source = read(BASE.parent / "deployment_g/nodes/n02/source.json")
    for name, digest in reuse["verifiedIdenticalSources"].items():
        assert source["files"][name] == digest == old_source["files"][name]
    assert len(plan["shards"]) == 1
    shard = plan["shards"][0]
    assert all(launch[key] == value for key, value in shard.items())
    assert launch["state"] == "launched" and launch["node"] == "n08" and launch["pid"] == 10189
    assert launch["planSHA256"] == sha((BASE / "plan.json").read_bytes())
    selected = read(BASE / "selection.json")
    assert set(selected) == set(shard["cases"]) and len(selected) == len(set(selected)) == shard["caseCount"] == 5
    command = launch["command"]
    assert "--pair-spins" not in command
    assert command[command.index("--jobs") + 1] == "5"
    assert command[command.index("--memory") + 1] == "8g"
    assert command[command.index("--vacuum-reduction") + 1] == "canonical"
    assert [command[i + 1] for i, word in enumerate(command) if word == "--case"] == shard["cases"]
    prior = set()
    for row in plan["completedPriorEvidence"]:
        original = Path(row["path"])
        local = BASE / "prior_evidence" / original.parent.name / original.name
        assert sha(local.read_bytes()) == row["sha256"]
        content = read(local)
        ids = content["preservedCases"] if original.name == "recovery.json" else content
        assert ids == row["cases"]
        prior.update(ids)
        if "-f-" in original.parent.name:
            node = original.parent.name.split("-")[3]
            assert local.read_bytes() == (BASE.parent / "preserved_f/nodes" / node / "recovery.json").read_bytes()
        elif "-d-" in original.parent.name:
            node = original.parent.name.split("-")[3]
            assert local.read_bytes() == (BASE.parent / "preserved_d/nodes" / node / "recovery.json").read_bytes()
    reserved = set(plan["reservedG"])
    gplan = read(BASE.parent / "deployment_g/plan.json")
    assert reserved == {case for entry in gplan["shards"] for case in entry["cases"]}
    remaining = set(selected)
    assert prior.isdisjoint(reserved) and prior.isdisjoint(remaining) and reserved.isdisjoint(remaining)
    universe = {"spacegroup_%03d_%s" % (n, spin) for n in range(1, 231) for spin in ("spinless", "spin_half")}
    assert prior | reserved | remaining == universe
    assert len(prior) == 254 and len(reserved) == 201 and len(remaining) == plan["remainingCount"] == 5
    assert len(universe) == plan["exactUnionCount"] == 460
    finalizer = read(BASE / "finalizers/launch.json")
    assert finalizer["pid"] == 10326 and finalizer["runnerPID"] == launch["pid"]
    cmd = finalizer["command"]
    assert int(cmd[cmd.index("--runner-pid") + 1]) == launch["pid"]
    assert cmd[cmd.index("--source-tag") + 1] == plan["tag"]
    assert cmd[1] == REMOTE + "snapshots/u1_finalize_campaign_20261015.py"
    log = (BASE / "integrated_116_tests.log").read_text()
    assert "Ran 116 tests in 68.609s" in log and log.rstrip().endswith("OK")
    invocation = read(BASE / "validation_122/invocation.json")
    validation = read(BASE / "validation_122/result.json")
    assert all(validation[k] == v for k, v in invocation.items())
    assert validation["exitCode"] == 0 and validation["changedFiles"] == []
    newlog = (BASE / "validation_122/tests.log").read_bytes()
    assert sha(newlog) == validation["logSHA256"]
    assert b"Ran 122 tests in 69.325s" in newlog and newlog.rstrip().endswith(b"OK")
    for name, digest in validation["sourceFilesBefore"].items():
        blob = subprocess.check_output(["git", "show", validation["gitCommit"] + ":" + name], cwd=REPO)
        assert sha(blob) == digest, name
    return {"verified": True, "sourceFilesCheckedAgainstGit": len(source["files"]),
            "priorEvidenceUnion": len(prior), "reservedG": len(reserved), "launchedH": len(remaining),
            "recordedRunnerPID": launch["pid"], "completionClaimedForH": False}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
