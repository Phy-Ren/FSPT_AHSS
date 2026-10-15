"""Paired timing follows observed driver markers, independently of file clocks."""
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("u1_timed_runner", ROOT / "scripts/classify.py")
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)
CASES = ("spacegroup_001_spin_half", "spacegroup_001_spinless")


def marker(index):
    return ("U1_PAIR_CASE_DONE " + CASES[index] + "\n").encode()


def emit(data, delay=0):
    return {"op": "stdout", "hex": data.hex(), "delay": delay}


class PairedRunnerTiming(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="u1-runner-timing-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def run_fixture(self, name, events, timeout=2, terminate_bytes=b""):
        base = self.base / name
        base.mkdir()
        output = base / "output"
        output.mkdir()
        inputs = []
        for case, spin in zip(CASES, ("spin_half", "spinless")):
            path = base / (case + ".json")
            path.write_text(json.dumps({"id": case, "family": "spacegroup", "index": 1,
                                        "dimension": 3, "spin": spin}))
            inputs.append(path)
        (base / "events.json").write_text(json.dumps({"events": events, "terminate": terminate_bytes.hex()}))
        fake = base / "gap-fixture"
        fake.write_text("#!" + sys.executable + "\n" + r'''
import json, os, re, signal, sys, time
from pathlib import Path
config=json.loads((Path(__file__).parent/'events.json').read_text())
driver=Path(sys.argv[-1]).read_text()
paths=[Path(json.loads(x)) for x in re.findall(r'OutputTextFile\(("(?:\\.|[^"\\])*"),false\)',driver)]
assert len(paths)==2
def write(fd, data):
    while data:
        data=data[os.write(fd,data):]
def terminate(signum, frame):
    write(1,bytes.fromhex(config['terminate']))
    raise SystemExit(7)
if config['terminate']:
    signal.signal(signal.SIGTERM,terminate)
for event in config['events']:
    time.sleep(event.get('delay',0))
    if event['op']=='native':
        path=paths[event['index']]
        path.write_text(json.dumps({'torsion':[],'freeRank':0,'presentation':[],
                                   'witnesses':[],'scope':'runner timing fixture'}))
        os.utime(path,(event['mtime'],event['mtime']))
    elif event['op']=='stdout':
        write(1,bytes.fromhex(event['hex']))
    elif event['op']=='stderr':
        write(2,bytes.fromhex(event['hex']))
    elif event['op']!='sleep':
        raise ValueError(event)
''')
        fake.chmod(0o755)
        started = time.monotonic()
        rows = RUNNER.run_spin_pair(inputs, output, str(fake), timeout, "1g", {"sha256": "test-source"})
        duration = time.monotonic() - started
        for case, row in zip(CASES, rows):
            self.assertEqual(json.loads((output / case / "run.json").read_text()), row)
        self.assertEqual((output / CASES[0] / "stdout.log").read_bytes(),
                         (output / CASES[1] / "stdout.log").read_bytes())
        return rows, output, duration

    def test_past_and_future_file_times_do_not_change_separate_monotonic_intervals(self):
        for name, mtimes in (("past_future", (1, 4102444800)), ("future_past", (4102444800, 1))):
            with self.subTest(name=name):
                prefix = b"ordinary non-UTF8 output: \xff\x00\n" + b"x" * 100000 + b"\n"
                events = [emit(prefix), {"op": "native", "index": 0, "mtime": mtimes[0]},
                          emit(marker(0)[:13], 0.04), emit(marker(0)[13:], 0.04),
                          {"op": "native", "index": 1, "mtime": mtimes[1]}, emit(marker(1), 0.12)]
                rows, output, duration = self.run_fixture(name, events)
                self.assertEqual((output / CASES[0] / "stdout.log").read_bytes(), prefix + marker(0) + marker(1))
                for row in rows:
                    self.assertEqual(row["status"], "complete")
                    self.assertTrue(row["completionMarkerObserved"])
                    self.assertTrue(row["caseTimingAvailable"])
                    self.assertTrue(row["stdoutCapture"]["eofObserved"])
                    self.assertGreater(row["elapsedSeconds"], 0.03)
                    self.assertLess(row["elapsedSeconds"], 2)
                    self.assertIn("time.monotonic", row["timingMethod"])
                self.assertEqual(rows[0]["batchElapsedSeconds"], rows[1]["batchElapsedSeconds"])
                self.assertLessEqual(sum(row["elapsedSeconds"] for row in rows), rows[0]["batchElapsedSeconds"] + 0.002)
                self.assertLess(duration, 3)

    def test_only_exact_ordered_markers_define_boundaries_and_duplicates_do_not_reset(self):
        misleading = (b"prefix " + marker(0) + marker(0).rstrip(b"\n") + b" trailing\n"
                      + b"U1_PAIR_CASE_DONE wrong_case\n" + marker(1))
        events = [emit(misleading), {"op": "native", "index": 0, "mtime": 1},
                  emit(marker(0), 0.06), emit(marker(0), 0.10),
                  {"op": "native", "index": 1, "mtime": 4102444800}, emit(marker(1), 0.10)]
        rows, output, _ = self.run_fixture("ordered", events)
        self.assertLess(rows[0]["elapsedSeconds"], 0.15)
        self.assertGreater(rows[1]["elapsedSeconds"], 0.16)
        self.assertEqual((output / CASES[0] / "stdout.log").read_bytes(), misleading + marker(0) * 2 + marker(1))

    def test_missing_exact_markers_leave_timing_unavailable_without_changing_acceptance(self):
        output = marker(0).rstrip(b"\n") + b" ordinary output\n" + marker(1).rstrip(b"\n")
        events = [{"op": "native", "index": 0, "mtime": 1},
                  {"op": "native", "index": 1, "mtime": 4102444800}, emit(output)]
        rows, directory, _ = self.run_fixture("no_markers", events)
        for row in rows:
            self.assertEqual(row["status"], "complete")
            self.assertIsNone(row["elapsedSeconds"])
            self.assertFalse(row["caseTimingAvailable"])
            self.assertFalse(row["completionMarkerObserved"])
            self.assertIn("timingUnavailableReason", row)
        self.assertEqual((directory / CASES[0] / "stdout.log").read_bytes(), output)

    def test_shared_timeout_keeps_completed_first_case_and_drains_termination_logs(self):
        termination = b"owned group terminated\x00\xff\n"
        events = [{"op": "native", "index": 0, "mtime": 1}, emit(marker(0)),
                  {"op": "stderr", "hex": b"stderr before timeout\n".hex()}, {"op": "sleep", "delay": 10}]
        rows, output, duration = self.run_fixture("timeout", events, timeout=0.15, terminate_bytes=termination)
        self.assertLess(duration, 2)
        self.assertEqual(rows[0]["status"], "complete")
        self.assertTrue(rows[0]["caseTimingAvailable"])
        self.assertEqual(rows[0]["exitCode"], 0)
        self.assertEqual(rows[0]["batchExitCode"], 7)
        self.assertEqual(rows[1]["status"], "timeout")
        self.assertIsNone(rows[1]["elapsedSeconds"])
        self.assertFalse((output / CASES[1] / "result.json").exists())
        self.assertGreaterEqual(rows[1]["batchElapsedSeconds"], 0.3)
        self.assertEqual((output / CASES[0] / "stdout.log").read_bytes(), marker(0) + termination)
        self.assertEqual((output / CASES[0] / "stderr.log").read_bytes(), b"stderr before timeout\n")

    def test_open_inherited_pipe_cannot_hold_finished_runner_forever(self):
        reader, writer = os.pipe()
        log = io.BytesIO()
        observed, errors, capture = {}, [], {"eofObserved": False}
        stop = threading.Event()
        stream = os.fdopen(reader, "rb", buffering=0)
        thread = threading.Thread(target=RUNNER._pump_pair_stdout,
                                  args=(stream, log, list(CASES), observed, stop, errors, capture), daemon=True)
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(2)"],
                                 stdout=writer, stderr=subprocess.DEVNULL)
        try:
            payload = b"finite output before exit\n" + marker(0)
            os.write(writer, payload)
            os.close(writer)
            writer = None
            stop.set()  # The writer remains open, as with an inherited descriptor.
            started = time.monotonic()
            thread.start()
            thread.join(timeout=2)
            self.assertFalse(thread.is_alive())
            self.assertLess(time.monotonic() - started, 1)
            self.assertIsNone(child.poll())  # The pump did not signal the unrelated holder.
            self.assertFalse(errors)
            self.assertEqual(log.getvalue(), payload)
            self.assertIn(CASES[0], observed)
            self.assertTrue(capture["inheritedPipeClosedAfterIdle"])
        finally:
            if writer is not None:
                os.close(writer)
            thread.join(timeout=2)
            child.wait(timeout=3)


if __name__ == "__main__":
    unittest.main()
