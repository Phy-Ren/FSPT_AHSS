#!/usr/bin/env python3
"""Check audit and resolution CLI validation without numerical calculations."""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_full_finite.py"


class ReachedGapBoundary(Exception):
    pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Use a fresh report path.")
    spec = importlib.util.spec_from_file_location("full_finite_cli_under_test", RUNNER)
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    checks = []
    with tempfile.TemporaryDirectory(prefix="fspt-finite-cli-") as directory:
        work = Path(directory)
        catalog = work / "models.json"
        model = dict(id="argument-fixture", group="C1", order=1,
                     productTable=[[1]], s1=[0], omega2=[[0]], generatorIndices=[])
        catalog.write_text(json.dumps({"models": [model]}))
        base = [str(RUNNER), "--catalog", str(catalog), "--model", model["id"],
                "--dimension", "4", "--output", str(work / "out/result.json"),
                "--gap", "must-not-execute-gap"]
        invalid = [
            ("positive-missing-names", ["--bar-audit-samples", "32"], "requires explicit"),
            ("positive-empty-names", ["--bar-audit-samples", "1", "--bar-audit-generators", ""], "requires explicit"),
            ("positive-empty-member", ["--bar-audit-samples", "1", "--bar-audit-generators", "C1,,P1"], "requires explicit"),
            ("positive-whitespace-member", ["--bar-audit-samples", "1", "--bar-audit-generators", "C1,  "], "requires explicit"),
            ("negative-sample-count", ["--bar-audit-samples", "-1", "--bar-audit-generators", "P1"], "nonnegative"),
        ]
        resolutions = [('--tensor-abelian',), ('--dihedral-resolution',),
                       ('--input-generators-resolution',),
                       ('--direct-product-resolution', 'D8xC2')]
        for left, right in itertools.combinations(resolutions, 2):
            invalid.append(('exclusive-' + left[0][2:] + '-' + right[0][2:],
                            list(left + right), 'Choose only one alternate resolution'))
        invalid.append(('unsupported-direct-product', ['--direct-product-resolution', 'C4xC2'], 'invalid choice'))
        for name, extra, message in invalid:
            stderr = io.StringIO()
            with patch.object(sys, "argv", base + extra), contextlib.redirect_stderr(stderr), \
                    patch.object(Path, "read_text", side_effect=AssertionError("catalog was read")), \
                    patch.object(runner, "freeze_runtime", side_effect=AssertionError("runtime was frozen")), \
                    patch.object(runner.subprocess, "Popen", side_effect=AssertionError("GAP was invoked")):
                try:
                    runner.main()
                except SystemExit as error:
                    assert error.code == 2, (name, error.code)
                else:
                    raise AssertionError((name, "invalid arguments were accepted"))
            assert message in stderr.getvalue(), (name, stderr.getvalue())
            assert not (work / "out").exists(), name
            checks.append(dict(name=name, status="passed", stopped_before_catalog_and_freeze=True))

        valid = [
            ("default-zero-samples", [], None),
            ("explicit-zero-ignores-selectors", ["--bar-audit-samples", "0", "--bar-audit-generators", "B2"], None),
            ("positive-explicit-selectors", ["--bar-audit-samples", "32", "--bar-audit-generators", "C1,C3,B1,P1"],
             '["C1","C3","B1","P1"]'),
            ("explicit-duplicates-preserved", ["--bar-audit-samples", "32", "--bar-audit-generators", "P1,P1"],
             '["P1","P1"]'),
            ("membership-still-deferred-to-strict-gap-guard", ["--bar-audit-samples", "32", "--bar-audit-generators", "B2"],
             '["B2"]'),
        ]
        entries = [
            ('tensor-resolution', ['--tensor-abelian'], 'run_full_finite_tensor.g'),
            ('dihedral-resolution', ['--dihedral-resolution'], 'run_full_finite_dihedral.g'),
            ('input-generators-resolution', ['--input-generators-resolution'], 'run_full_finite_marked.g'),
            ('D8-product-resolution', ['--direct-product-resolution', 'D8xC2'], 'run_full_finite_product.g'),
            ('Q8-product-resolution', ['--direct-product-resolution', 'Q8xC2'], 'run_full_finite_product.g'),
        ]
        valid += [(name, extra, None) for name, extra, entry in entries]
        for name, extra, names in valid:
            captured = []

            def intercept(command, **kwargs):
                assert command[0] == "must-not-execute-gap"
                captured.append(Path(command[-1]).read_text())
                raise ReachedGapBoundary()

            with patch.object(sys, "argv", base + extra), \
                    patch.object(runner, "freeze_runtime", return_value=(work, {})) as freeze, \
                    patch.object(runner.subprocess, "Popen", side_effect=intercept):
                try:
                    runner.main()
                except ReachedGapBoundary:
                    pass
                else:
                    raise AssertionError((name, "driver boundary not reached"))
            assert freeze.call_count == 1 and len(captured) == 1, name
            driver = captured[0]
            selected = [entry for label, extra_flags, entry in entries if label == name]
            if selected:
                assert '/gap/' + selected[0] in driver, (name, driver)
            if '--direct-product-resolution' in extra:
                family = extra[extra.index('--direct-product-resolution') + 1]
                assert 'AFS_FULL_DIRECT_PRODUCT_FAMILY:="' + family + '";;' in driver
            if names is None:
                assert "AFS_FULL_BAR_AUDIT_" not in driver, name
            else:
                assert "AFS_FULL_BAR_AUDIT_SAMPLES:=32;;" in driver, name
                assert "AFS_FULL_BAR_AUDIT_GENERATORS:=" + names + ";;" in driver, name
                assert "AFS_FULL_BAR_AUDIT_SEED:=20261001;;" in driver, name
            assert not (work / "out/result.json").exists(), name
            checks.append(dict(name=name, status="passed", driver_prepared_without_execution=True))

    report = dict(success=True, checks=checks, numerical_processes_started=0,
                  scope="Argument validation and exact generated-driver settings only; no classification or arithmetic audit.",
                  runner=str(RUNNER.relative_to(ROOT)),
                  runner_sha256=hashlib.sha256(RUNNER.read_bytes()).hexdigest(),
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    print(json.dumps(dict(success=True, checks=len(checks), numerical_processes_started=0)))


if __name__ == "__main__":
    main()
