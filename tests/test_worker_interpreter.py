"""Real single and paired classifications cannot select PATH's wrong Python."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
import venv


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")
CASES = ("point3_04_spin_half", "point3_04_spinless")
EXECUTION_FIELDS = {"formulaCacheStats", "formulaWorkerCalls", "pairedGeometryReuse",
                    "resolutionBuildTimings"}


@unittest.skipUnless(GAP, "GAP and HAP are required")
class WorkerInterpreterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="u1-worker-interpreter-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.marker = self.base / "wrong-python-used"
        hostile = self.base / "hostile-bin"
        hostile.mkdir()
        fake = hostile / "python3"
        fake.write_text("#!/bin/sh\nprintf 'unexpected worker interpreter\\n' > "
                        + shlex.quote(str(self.marker)) + "\nexit 91\n")
        fake.chmod(0o755)
        self.clean = dict(os.environ, U1_DAG_MODE="reference")
        self.hostile = dict(self.clean, PATH=str(hostile) + os.pathsep + os.environ.get("PATH", ""))
        # Prove that the hostile PATH really selects the failing executable.
        probe = subprocess.run(["python3", "--version"], env=self.hostile,
                               capture_output=True, timeout=5)
        self.assertEqual(probe.returncode, 91)
        self.assertTrue(self.marker.exists())
        self.marker.unlink()

    def calculate(self, label, cases, paired, env, interpreter=None):
        interpreter = interpreter or sys.executable
        output = self.base / label
        command = [interpreter, str(ROOT / "scripts/classify.py"),
                   "--gap", GAP, "--jobs", "1", "--timeout", "60", "--memory", "2g",
                   "--output", str(output)]
        for case in cases:
            command += ["--case", case]
        if paired:
            command.append("--pair-spins")
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=150)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        records = {}
        for case in cases:
            folder = output / case
            record = json.loads((folder / "result.json").read_bytes())
            native, run = record["classification"], record["run"]
            self.assertEqual(run, json.loads((folder / "run.json").read_bytes()))
            self.assertEqual((run["status"], run["exitCode"]), ("complete", 0))
            self.assertEqual(run["formulaWorkerPython"], os.path.abspath(interpreter))
            binding = "U1_FORMULA_PYTHON:=" + json.dumps(os.path.abspath(interpreter)) + ";;"
            self.assertIn(binding, (folder / "driver.g").read_text())
            self.assertEqual((native["freeRank"], native["torsion"]), (0, [8]))
            self.assertTrue(native["nativeChainIdentitiesVerified"])
            self.assertGreater(native["nativeCompletionChecks"], 0)
            self.assertGreater(native["formulaWorkerCalls"], 0)  # Exercise a real worker.
            if paired:
                self.assertTrue(run["pairedSpins"])
                self.assertTrue(run["completionMarkerObserved"])
            records[case] = record
        return records

    def check_mode(self, paired):
        cases = CASES if paired else CASES[:1]
        expected = self.calculate("control", cases, paired, self.clean)
        actual = self.calculate("hostile", cases, paired, self.hostile)
        self.assertFalse(self.marker.exists(), "The formula worker ran PATH's hostile python3")
        for case in cases:
            self.assertEqual(actual[case]["input"], expected[case]["input"])
            science = lambda record: {k: v for k, v in record["classification"].items()
                                      if k not in EXECUTION_FIELDS}
            self.assertEqual(science(actual[case]), science(expected[case]))

    def test_single_case_pins_worker_despite_hostile_path(self):
        self.check_mode(False)

    def test_paired_cases_pin_worker_and_keep_exact_scientific_outputs(self):
        self.check_mode(True)

    def test_virtualenv_interpreter_path_preserves_symlink_and_gap_escaping(self):
        environment = self.base / 'venv with "quotes" and spaces'
        venv.EnvBuilder(with_pip=False, system_site_packages=True, symlinks=True).create(environment)
        interpreter = environment / "bin/python"
        self.assertNotEqual(str(interpreter), str(interpreter.resolve()))
        self.calculate("venv", CASES[:1], False, self.hostile, str(interpreter))
        self.assertFalse(self.marker.exists())


if __name__ == "__main__":
    unittest.main()
