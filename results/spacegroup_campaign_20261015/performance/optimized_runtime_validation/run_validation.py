#!/usr/bin/env python3
"""Run a bounded compatibility suite against an immutable full commit archive."""
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import resource
import runpy
import shutil
import socket
import subprocess
import sys
import time
import unittest

MODULES = ["test_backend", "test_backend_cochains", "test_backend_source_cache",
           "test_formula_cache", "test_backend_spacegroup", "test_spacegroup"]
EXPECTED_BINARY_SHA = "873e902ee797706160601846c1ad6582c05e0aebd069bdd7efcff3d081f96fea"
EXPECTED_SOURCE_SHA = "63887ca47cf557f30a3a867bac16392b05c8d107a8cdb87ffbd4d47784ccdc88"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


class TimedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timings = []

    def startTest(self, test):
        self.start_time = time.monotonic()
        super().startTest(test)

    def stopTest(self, test):
        self.timings.append({"id": test.id(), "wallSeconds": time.monotonic()-self.start_time})
        super().stopTest(test)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--launcher", type=Path, required=True)
    parser.add_argument("--binary", type=Path, required=True)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    source = base / "source"
    output = base / "validation_o2"
    output.mkdir(exist_ok=False)
    archive = json.loads((base / "archive_manifest.json").read_text())
    def verify_source():
        for name, record in archive["files"].items():
            if digest(source / name) != record["sha256"]:
                raise ValueError("Archived source changed: " + name)
    verify_source()
    if digest(args.binary) != EXPECTED_BINARY_SHA:
        raise ValueError("Unexpected optimized GAP binary")
    sys.path[:0] = [str(source), str(source / "tests")]
    runner = runpy.run_path(str(source / "scripts/classify.py"))
    manifest = runner["source_manifest"]()
    if manifest["sha256"] != EXPECTED_SOURCE_SHA:
        raise ValueError("Runtime differs from snapshot C")
    bin_directory = output / "bin"
    bin_directory.mkdir()
    (bin_directory / "gap").symlink_to(args.launcher)
    os.environ["PATH"] = str(bin_directory) + os.pathsep + os.environ["PATH"]
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    if Path(shutil.which("gap")).resolve() != args.launcher.resolve():
        raise ValueError("Focused tests would use the wrong GAP executable")
    os.chdir(source)
    gap_script = output / "versions.g"
    gap_script.write_text('''U1_ROOT:="%s";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;
info:=rec(gapVersion:=GAPInfo.Version,architecture:=GAPInfo.Architecture,packages:=rec());;
for name in ["HAP","Cryst","CrystCat","Polycyclic"] do
 package:=PackageInfo(name)[1];;info.packages.(name):=rec(version:=package.Version,path:=package.InstallationPath);;
od;
out:=OutputTextFile("%s",false);;SetPrintFormattingStatus(out,false);;
WriteLine(out,U1JSON(info));;CloseStream(out);;QUIT_GAP(0);
''' % (source, output / "versions.json"))
    version = subprocess.run([str(args.launcher), "-q", "-b", "--quitonbreak", str(gap_script)],
                             text=True, capture_output=True, timeout=90)
    (output / "versions.stdout").write_text(version.stdout)
    (output / "versions.stderr").write_text(version.stderr)
    if version.returncode:
        raise ValueError(version.stdout+version.stderr)
    versions = json.loads((output / "versions.json").read_text())
    metadata = {"gitCommit": archive["gitCommit"], "archiveSHA256": archive["archiveSHA256"],
                "runtimeSourceSHA256": manifest["sha256"], "runtimeFileCount": len(manifest["files"]),
                "host": socket.gethostname(), "python": platform.python_version(), "pythonExecutable": sys.executable,
                "environment": {key: os.environ.get(key) for key in
                                ("PATH", "LC_ALL", "LANG", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "PYTHONDONTWRITEBYTECODE")},
                "launcher": str(args.launcher), "launcherSHA256": digest(args.launcher),
                "binary": str(args.binary), "binarySHA256": digest(args.binary), "versions": versions,
                "command": [sys.executable, *sys.argv], "invocationWorkingDirectory": str(base),
                "testWorkingDirectory": str(source), "modules": MODULES,
                "scriptSHA256": digest(base / "run_validation.py"),
                "startedUTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "loadBefore": os.getloadavg(), "expectedTests": 15}
    save(output / "metadata.json", metadata)
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(name) for name in MODULES)
    started = time.monotonic()
    with (output / "tests.log").open("w") as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=TimedResult).run(suite)
    backend = importlib.import_module("test_backend")
    if hasattr(backend.BackendTests, "results"):
        save(output / "backend_exact_results.json", backend.BackendTests.results)
    verify_source()
    report = {"status": "PASS" if result.wasSuccessful() and result.testsRun == 15 and not result.skipped else "FAIL",
              "testsRun": result.testsRun, "expectedTests": 15, "skipped": [(t.id(), why) for t,why in result.skipped],
              "errors": [(t.id(), why) for t,why in result.errors], "failures": [(t.id(), why) for t,why in result.failures],
              "timings": result.timings, "wallSeconds": time.monotonic()-started,
              "loadAfter": os.getloadavg(), "maxChildRSSKiB": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              "all1610ArchivedFilesUnchanged": True, "finishedUTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "metadataSHA256": digest(output / "metadata.json"), "testLogSHA256": digest(output / "tests.log"),
              "backendResultsSHA256": digest(output / "backend_exact_results.json") if (output / "backend_exact_results.json").exists() else None}
    save(output / "result.json", report)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
