#!/usr/bin/env python3
"""Verify the completed primary H archive independently of the immutable launch package."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

BASE = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def verify(validator_root=None):
    manifest = read(BASE / "manifest.json")
    actual = {str(p.relative_to(BASE)) for p in BASE.rglob("*")
              if p.is_file() and p.name != "manifest.json" and "__pycache__" not in p.parts}
    assert actual == set(manifest["filesSHA256"])
    for name, digest in manifest["filesSHA256"].items():
        assert sha((BASE / name).read_bytes()) == digest, name
    all_ids, rows = set(), []
    for folder in sorted((BASE / "nodes").iterdir()):
        node = folder.name
        final = read(folder / "finalization.json")
        assert final["state"] == "complete" and final["sourceVerified"] and final["runtimeVerified"]
        tag = final["tag"]
        archive = BASE / "archives" / Path(final["archive"]).name
        assert sha(archive.read_bytes()) == final["archiveSHA256"]
        assert archive.stat().st_size == final["archiveBytes"]
        with tarfile.open(archive) as tar:
            members = tar.getmembers()
            assert len({m.name for m in members}) == len(members)
            assert all(not m.name.startswith("/") and ".." not in Path(m.name).parts
                       and (m.isfile() or m.isdir()) for m in members)
            raw = {m.name: tar.extractfile(m).read() for m in members if m.isfile()}
        j = lambda name: json.loads(raw[name])
        download = read(folder / "download_verification.json")
        assert download["requiredCompleteBeforeDownload"] and download["finalizationUnchangedAcrossDownload"]
        assert download["finalizationSHA256"] == sha((folder / "finalization.json").read_bytes())
        assert download["archiveSHA256"] == final["archiveSHA256"] and download["archiveBytes"] == final["archiveBytes"]
        assert download["archiveMemberSafetyVerified"] and download["originalFilesUnchanged"]
        assert download["frozenCollectorExactReplay"] and download["frozenCollectorExitCode"] == 0
        assert download["acceptedCount"] == final["acceptedCount"]
        for name, digest in download["originalFilesSHA256"].items():
            assert sha(raw[name]) == digest, name
        for name, member in read(folder / "archive_mirrors.json").items():
            assert (folder / name).read_bytes() == raw[member]
        launch = read(BASE.parent / "deployment_h/launch.json")
        source = j(tag + "/source.json")
        assert source == launch["source"] and source["sha256"] == final["sourceSHA256"]
        assert sha(json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()) == source["sha256"]
        e8_source = j(tag + "-e8/source.json")
        assert sha(json.dumps(e8_source["files"], sort_keys=True, separators=(",", ":")).encode()) == e8_source["sha256"]
        assert j(tag + "/formula_runtime.json") == launch["formulaRuntime"]
        selected = j(tag + "/selection.json")
        ids = set(selected)
        assert len(selected) == len(ids) == final["selectedCount"] == final["acceptedCount"]
        assert ids == set(launch["cases"]) == set(j(tag + "-e8/selection.json"))
        assert sha(raw[tag + "/selection.json"]) == final["selectionSHA256"]
        assert all_ids.isdisjoint(ids)
        all_ids.update(ids)
        for case in sorted(ids):
            ci = j(tag + "/" + case + "/result.json")
            run = j(tag + "/" + case + "/run.json")
            data = j(tag + "/" + case + "/input.json")
            native = j(tag + "/" + case + "/native.json")
            assert ci["run"] == run and ci["input"] == data and ci["classification"] == native
            assert run["status"] == "complete" and run["exitCode"] == 0
            assert data["id"] == run["id"] == case and run["sourceSHA256"] == source["sha256"]
            assert sha(raw[tag + "/" + case + "/input.json"]) == run["inputSHA256"]
            assert native["nativeChainIdentitiesVerified"] is True
            assert type(native["nativeCompletionChecks"]) is int and native["nativeCompletionChecks"] > 0
            e8 = j(tag + "-e8/" + case + "/result.json")
            e8_prefix = tag + "-e8/" + case
            e8_run = j(e8_prefix + "/run.json")
            assert e8["run"] == e8_run and e8["input"] == data == j(e8_prefix + "/input.json")
            assert raw[e8_prefix + "/ci_result.json"] == raw[tag + "/" + case + "/result.json"]
            assert e8_run["ciResultSHA256"] == sha(raw[e8_prefix + "/ci_result.json"])
            assert e8_run["ciSourceSHA256"] == source["sha256"] and e8_run["ciRun"] == run
            assert e8_run["inputSHA256"] == sha(raw[e8_prefix + "/input.json"])
            assert e8_run["sourceSHA256"] == e8_source["sha256"] and e8_run["id"] == case
            assert e8["classification"]["ciSector"] == native
            assert e8["run"]["status"] == "complete" and e8["run"]["exitCode"] == 0
            assert e8["classification"]["physicalClassificationCertified"] is False
        collection = j(tag + "-accepted/collection.json")
        assert collection["accepted"] and sum(r["count"] for r in collection["collections"]) == len(ids)
        for row in collection["collections"]:
            prefix = tag + "-accepted/" + row["path"]
            for name, digest in row["filesSHA256"].items():
                assert sha(raw[prefix + "/" + name]) == digest
            validation = j(prefix + "/validation.json")
            assert validation["accepted"] and set(validation["selectedCases"]) == ids
            assert not validation["missingOrFailedSelectedCases"]
            for origin in j(prefix + "/provenance.json"):
                for case, digest in origin["resultHashes"].items():
                    path = Path(origin["directory"]).name + "/" + case + "/result.json"
                    assert sha(raw[path]) == digest
        if validator_root is not None:
            validator_root = Path(validator_root).resolve()
            assert sha((validator_root / "scripts/collect_expansion.py").read_bytes()) == collection["collectorSHA256"]
            for name, digest in j(tag + "-e8/source.json")["files"].items():
                assert sha((validator_root / name).read_bytes()) == digest, name
            with tempfile.TemporaryDirectory(prefix="u1-completed-h-verify-") as temp:
                with tarfile.open(archive) as tar:
                    tar.extractall(temp)
                output = Path(temp) / "rechecked"
                subprocess.run([sys.executable, str(validator_root / "scripts/collect_expansion.py"),
                                "--ci-root", str(Path(temp) / tag), "--e8-root", str(Path(temp) / (tag + "-e8")),
                                "--output", str(output)], check=True)
                for row in collection["collections"]:
                    for name in ("results.json", "ci_results.json", "validation.json"):
                        assert sha((output / row["path"] / name).read_bytes()) == row["filesSHA256"][name]
        rows.append({"node": node, "acceptedCount": len(ids), "archiveSHA256": final["archiveSHA256"]})
    assert all_ids == set(read(BASE.parent / "deployment_h/selection.json")) and len(all_ids) == 5
    assert all_ids.isdisjoint(read(BASE.parent / "preserved_d/selection.json"))
    assert all_ids.isdisjoint(read(BASE.parent / "preserved_f/selection.json"))
    gplan = read(BASE.parent / "deployment_g/plan.json")
    assert all_ids.isdisjoint({case for shard in gplan["shards"] for case in shard["cases"]})
    tool = read(BASE / "download_tool/launch.json")
    assert sha((BASE / "download_tool/download_completed.py").read_bytes()) == tool["scriptSHA256"]
    return {"verified": True, "completedShards": rows, "acceptedTotal": len(all_ids),
            "frozenCollectorRepeated": validator_root is not None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--validator-root", help="Optional exact frozen c07c6e5 collector checkout")
    args = parser.parse_args()
    print(json.dumps(verify(args.validator_root), indent=2, sort_keys=True))
