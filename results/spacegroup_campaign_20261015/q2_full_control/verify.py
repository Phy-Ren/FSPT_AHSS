#!/usr/bin/env python3
"""Verify the retained diagnostic control without executing either solver."""
import argparse
import hashlib
import json
import subprocess
import tarfile
from pathlib import Path, PurePosixPath


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=here.parents[2])
    args = parser.parse_args()
    read = lambda name: json.loads((here / name).read_bytes())
    manifest = read("manifest.json")["files"]
    assert set(manifest) == {str(p.relative_to(here)) for p in here.rglob("*")
                             if p.is_file() and p.name != "manifest.json"}
    for name, digest in manifest.items():
        assert sha((here / name).read_bytes()) == digest, name
    proof = read("provenance.json")
    assert sha((here / "raw.tar.gz").read_bytes()) == proof["archiveSHA256"]
    with tarfile.open(here / "raw.tar.gz") as archive:
        members = archive.getmembers()
        assert len({m.name for m in members}) == len(members) == 39
        for m in members:
            path = PurePosixPath(m.name)
            assert m.isfile() and not path.is_absolute() and ".." not in path.parts
        raw = {m.name: archive.extractfile(m).read() for m in members}
    assert {name: sha(data) for name, data in raw.items()} == proof["archiveMembers"]
    load = lambda name: json.loads(raw[name])
    case = "spacegroup_141_spin_half"
    tags = {
        "baseline": "sg141-h-baseline-overlap-n08-20261015",
        "candidate": "sg141-h-q2mod2-overlap-n08-retry-20261015",
    }
    before, after = read("before.json"), read("after.json")
    assert before["files"] == after["files"]
    assert before["roles"] == after["roles"]
    artifact_hashes = {name: sha(data) for name, data in raw.items()
                       if name != "capture_remote_proof.json"}
    assert before["files"] == read("capture_verification.json")["files"] == artifact_hashes
    for key in ("gapBinarySHA256", "librarySHA256", "pythonExecutableSHA256"):
        assert before["roles"]["baseline"][key] == before["roles"]["candidate"][key]
    source_sets, native = {}, {}
    measurements = read("resources_comparison.json")["runs"]
    for role, tag in tags.items():
        source = load(tag + "/source.json")
        source_sets[role] = source["files"]
        assert source["files"] == before["roles"][role]["sourceFiles"]
        assert source["sha256"] == before["roles"][role]["sourceSHA256"]
        for name, digest in source["files"].items():
            overlay = here / "candidate_overlay" / name
            if role == "candidate" and name in proof["exactSourceDifferences"]:
                data = overlay.read_bytes()
            else:
                data = subprocess.check_output(
                    ["git", "show", proof["baselineCommit"] + ":" + name],
                    cwd=args.repository)
            assert sha(data) == digest, (role, name)
        run = load(tag + "/" + case + "/run.json")
        result = load(tag + "/" + case + "/result.json")
        native[role] = load(tag + "/" + case + "/native.json")
        assert load(tag + "/selection.json") == [case]
        assert run["status"] == "complete" and type(run["exitCode"]) is int and run["exitCode"] == 0
        assert load(tag + "-finished.json")["exitCode"] == 0
        assert run["sourceSHA256"] == source["sha256"]
        assert run["inputSHA256"] == sha(raw[tag + "/" + case + "/input.json"])
        assert result["run"] == run and result["classification"] == native[role]
        assert result["input"] == load(tag + "/" + case + "/input.json")
        assert run["command"][run["command"].index("-K") + 1] == "16g"
        assert run["timeoutSeconds"] == 2400
        report = raw[tag + "-resources.txt"].decode()
        fields = dict(line.strip().rsplit(": ", 1) for line in report.splitlines() if ": " in line)
        measure = measurements[role]
        assert float(fields["User time (seconds)"]) == measure["userCPUSeconds"]
        assert float(fields["System time (seconds)"]) == measure["systemCPUSeconds"]
        assert int(fields["Maximum resident set size (kbytes)"]) == measure["maximumResidentSetSizeKiB"]
        elapsed = fields["Elapsed (wall clock) time (h:mm:ss or m:ss)"].split(":")
        seconds = 0.0
        for part in elapsed:
            seconds = 60 * seconds + float(part)
        assert abs(seconds - measure["wallSeconds"]) < 1e-8
        assert int(fields["Exit status"]) == 0
    assert raw[tags["baseline"] + "/" + case + "/input.json"] == raw[tags["candidate"] + "/" + case + "/input.json"]
    differences = sorted(name for name in set(source_sets["baseline"]) | set(source_sets["candidate"])
                         if source_sets["baseline"].get(name) != source_sets["candidate"].get(name))
    assert differences == proof["exactSourceDifferences"]
    excluded = {"resolutionBuildTimings", "formulaWorkerCalls", "formulaCacheStats"}
    scientific = sorted(set(native["baseline"]) - excluded)
    assert set(native["baseline"]) == set(native["candidate"])
    assert len(scientific) == 35
    assert scientific == read("exact_comparison.json")["exactScientificFields"]
    assert all(native["baseline"][key] == native["candidate"][key] for key in scientific)
    print("PASS: retained sources, ordinary completion, 35 exact fields and full-run measurements; diagnostic only")


if __name__ == "__main__":
    main()
