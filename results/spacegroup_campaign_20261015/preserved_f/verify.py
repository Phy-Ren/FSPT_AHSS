#!/usr/bin/env python3
"""Verify immutable preserved evidence; optionally repeat its frozen collector."""
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
    assert actual == set(manifest["filesSHA256"]), "Package file inventory differs"
    for name, digest in manifest["filesSHA256"].items():
        assert sha((BASE / name).read_bytes()) == digest, name
    mirrors = read(BASE / "archive_mirrors.json")
    all_ids, counts = set(), []
    for node in ("n02", "n03"):
        prefix = "sgfull-20261015-f-" + node + "-pilot"
        local = BASE / "nodes" / node
        metadata = read(local / "archive_metadata.json")
        archive = BASE / "archives" / Path(metadata["archive"]["path"]).name
        assert sha(archive.read_bytes()) == metadata["archive"]["sha256"]
        assert archive.stat().st_size == metadata["archive"]["bytes"]
        with tarfile.open(archive) as tar:
            members = tar.getmembers()
            names = [m.name for m in members]
            assert len(names) == len(set(names)), "Duplicate archive member"
            assert all(not m.name.startswith("/") and ".." not in Path(m.name).parts
                       and (m.isfile() or m.isdir()) for m in members)
            raw = {m.name: tar.extractfile(m).read() for m in members if m.isfile()}
        j = lambda name: json.loads(raw[name])
        for name, link in mirrors.items():
            if link["archive"] == str(archive.relative_to(BASE)):
                assert (BASE / name).read_bytes() == raw[link["member"]], name
        retained = prefix + "-preserved"
        e8 = prefix + "-preserved-e8"
        accepted = prefix + "-preserved-accepted"
        ledger = j(retained + "/recovery.json")
        ids = set(ledger["preservedCases"])
        recovered = set(ledger["recoveredCases"])
        ordinary = set(ledger["ordinaryCompleteCases"])
        assert recovered.isdisjoint(ordinary) and recovered | ordinary == ids
        assert ids.isdisjoint(all_ids)
        all_ids.update(ids)
        assert ids == set(j(retained + "/selection.json")) == set(j(e8 + "/selection.json"))
        for name, digest in ledger["filesSHA256"].items():
            assert sha(raw[retained + "/" + name]) == digest, name
        source = j(retained + "/source.json")
        assert sha(json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()) == source["sha256"]
        assert source["sha256"] == ledger["sourceSHA256"]
        stop = j(prefix + "-stop/cancellation.json")
        assert sha(raw[prefix + "-stop/cancellation.json"]) == ledger["cancellationReportSHA256"]
        assert stop["allOwnedProcessesStopped"] and stop["sourceSnapshotVerified"] and stop["formulaRuntimeVerified"]
        assert stop["verifiedSourceSHA256"] == stop["sourceSHA256"] == source["sha256"]
        for case in sorted(ids):
            root = retained + "/" + case
            result, run, data = (j(root + "/" + name + ".json") for name in ("result", "run", "input"))
            native = j(root + "/native.json")
            assert result["run"] == run and result["input"] == data
            assert result["classification"] == native and data["id"] == run["id"] == case
            assert run["inputSHA256"] == sha(raw[root + "/input.json"])
            assert run["sourceSHA256"] == source["sha256"]
            assert native["nativeChainIdentitiesVerified"] is True
            assert type(native["nativeCompletionChecks"]) is int and native["nativeCompletionChecks"] > 0
            if case in recovered:
                assert run["status"] == "recovered_complete"
                assert not {"exitCode", "batchExitCode", "elapsedSeconds", "startedUTC"} & set(run)
                assert run["executionExitStatus"] == "not_inferred_from_native_completion"
            else:
                assert run["status"] == "complete" and run["exitCode"] == 0
            extended_root = e8 + "/" + case
            extended = j(extended_root + "/result.json")
            erun = j(extended_root + "/run.json")
            edata = j(extended_root + "/input.json")
            esource = j(e8 + "/source.json")
            assert extended["run"] == erun and extended["input"] == edata == data
            assert erun["status"] == "complete" and erun["exitCode"] == 0
            assert erun["inputSHA256"] == sha(raw[extended_root + "/input.json"])
            assert erun["sourceSHA256"] == esource["sha256"]
            assert sha(json.dumps(esource["files"], sort_keys=True, separators=(",", ":")).encode()) == esource["sha256"]
            assert raw[extended_root + "/ci_result.json"] == raw[root + "/result.json"]
            assert erun["ciResultSHA256"] == sha(raw[root + "/result.json"])
            assert erun["ciRun"] == run and erun["ciSourceSHA256"] == source["sha256"]
            assert extended["classification"]["ciSector"] == native
            assert extended["classification"]["physicalClassificationCertified"] is False
        collection = j(accepted + "/collection.json")
        assert collection["accepted"] is True
        assert sum(row["count"] for row in collection["collections"]) == len(ids)
        for row in collection["collections"]:
            folder = accepted + "/" + row["path"]
            for name, digest in row["filesSHA256"].items():
                assert sha(raw[folder + "/" + name]) == digest
            validation = j(folder + "/validation.json")
            assert validation["accepted"] and not validation["missingOrFailedSelectedCases"]
            assert set(validation["selectedCases"]) == ids
            for origin in j(folder + "/provenance.json"):
                original_folder = Path(origin["directory"]).name
                for case, digest in origin["resultHashes"].items():
                    assert sha(raw[original_folder + "/" + case + "/result.json"]) == digest
        if validator_root is not None:
            validator_root = Path(validator_root).resolve()
            assert sha((validator_root / "scripts/recover_paired_campaign.py").read_bytes()) == ledger["recoveryHelperSHA256"]
            assert sha((validator_root / "scripts/collect_expansion.py").read_bytes()) == collection["collectorSHA256"]
            for name, digest in j(e8 + "/source.json")["files"].items():
                assert sha((validator_root / name).read_bytes()) == digest, name
            with tempfile.TemporaryDirectory(prefix="u1-preserved-f-verify-") as temp:
                with tarfile.open(archive) as tar:
                    tar.extractall(temp)
                subprocess.run([sys.executable, str(validator_root / "scripts/collect_expansion.py"),
                                "--ci-root", str(Path(temp) / retained), "--e8-root", str(Path(temp) / e8),
                                "--allow-recovered", "--output", str(Path(temp) / "rechecked")], check=True)
                for row in collection["collections"]:
                    for name in ("results.json", "ci_results.json", "validation.json"):
                        output = Path(temp) / "rechecked" / row["path"] / name
                        assert sha(output.read_bytes()) == row["filesSHA256"][name], name
        finalizer = read(local / "original_finalizer/finalization.json")
        assert finalizer["state"] == "incomplete"
        assert finalizer["sourceSHA256"] == source["sha256"]
        assert set(finalizer["retryCases"]).issubset(ledger["requestedCases"])
        assert set(ledger["retryCases"]).isdisjoint(ids)
        assert set(ledger["retryCases"]) | ids == set(ledger["requestedCases"])
        assert metadata["status"] == "complete" and all(x["exitCode"] == 0 for x in metadata["commands"])
        assert metadata["preservedCases"] == ledger["preservedCases"]
        assert metadata["recoveredCases"] == ledger["recoveredCases"]
        assert metadata["ordinaryCompleteCases"] == ledger["ordinaryCompleteCases"]
        assert metadata["stopReportSHA256"] == ledger["cancellationReportSHA256"]
        assert metadata["orchestratorSHA256"] == sha(raw[prefix + "-preserve-postprocess-5ed6b9c/orchestrator.py"])
        assert metadata["sourceArchiveSHA256"] == sha((BASE / "archives/f-preserve-5ed6b9c.tar.gz").read_bytes())
        assert metadata["sourceManifestSHA256"] == sha((BASE / "postprocessor_source.json").read_bytes())
        postprocessor = read(BASE / "postprocessor_source.json")
        assert postprocessor["filesSHA256"] == metadata["sourceFilesSHA256"]
        with tarfile.open(BASE / "archives/f-preserve-5ed6b9c.tar.gz") as posttar:
            for name, digest in postprocessor["filesSHA256"].items():
                assert sha(posttar.extractfile(name).read()) == digest, name
        counts.append({"node": node, "preserved": len(ids), "ordinary": len(ordinary),
                       "recovered": len(recovered), "retry": len(ledger["retryCases"])})
    assert all_ids == set(read(BASE / "selection.json")) and len(all_ids) == 4
    assert sum(row["recovered"] for row in counts) == 2
    assert sum(row["ordinary"] for row in counts) == 2
    assert sum(row["retry"] for row in counts) == 6
    return {"verified": True, "nodes": counts, "frozenCollectorRepeated": validator_root is not None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--validator-root", help="Optional checkout with the exact frozen 5ed6b9c validator files")
    args = parser.parse_args()
    print(json.dumps(verify(args.validator_root), indent=2, sort_keys=True))
