"""Non-signaling ownership preflight tests for future campaign preservation."""
import copy
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest import mock

from scripts import stop_owned_campaign as stop


class StopOwnedSingletonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.snapshot = self.base / 'snapshot'
        (self.snapshot / 'scripts').mkdir(parents=True)
        (self.snapshot / 'scripts/classify.py').write_text('# immutable fixture\n')
        self.root = self.base / 'campaign'
        self.root.mkdir()
        self.cases = ['spacegroup_019_spin_half', 'spacegroup_019_spinless',
                      'spacegroup_226_spin_half']
        files = {'scripts/classify.py': stop.sha(self.snapshot / 'scripts/classify.py')}
        self.source = {'files': files, 'sha256': hashlib.sha256(
            json.dumps(files, sort_keys=True, separators=(',', ':')).encode()).hexdigest()}
        self.write(self.root / 'source.json', self.source)
        self.write(self.root / 'selection.json', self.cases)
        self.runner = self.row(1001, 900, 1001,
                              [sys.executable, str(self.snapshot / 'scripts/classify.py'),
                               '--output', str(self.root)])
        self.rows = {1001: self.runner}
        for index, case in enumerate(self.cases):
            folder = self.root / case
            folder.mkdir()
            data = {'id': case, 'dimension': 3, 's': [0, 1], 'rho': [0, 1]}
            self.write(folder / 'input.json', data)
            driver_case = self.cases[0] if index < 2 else case
            command = [sys.executable, str(self.root / driver_case / 'driver.g')]
            record = {'id': case, 'status': 'running', 'command': command,
                      'host': socket.gethostname(), 'sourceSHA256': self.source['sha256'],
                      'inputSHA256': stop.sha(folder / 'input.json')}
            if index < 2:
                record.update(pairedSpins=True, batchCaseIDs=self.cases[:2])
            self.write(folder / 'run.json', record)
            (folder / 'driver.g').write_text(
                'U1_ROOT:=' + json.dumps(str(self.snapshot)) + ';;\n'
                'U1_INPUT:=' + stop.gap_literal(data) + ';;\n'
                'output:=OutputTextFile(' + json.dumps(str(folder / 'native.json')) + ',false);;\n'
                'CloseStream(output);;\n')
            if index != 1:
                pid = 1002 + index
                self.rows[pid] = self.row(pid, 1001, pid, command)
                self.rows[pid + 10] = self.row(pid + 10, pid, pid,
                                               [sys.executable, '-u', str(self.snapshot / 'scripts/formula_worker.py')])
        self.singleton = self.root / self.cases[2]

    @staticmethod
    def write(path, value):
        path.write_text(json.dumps(value, indent=2) + '\n')

    @staticmethod
    def row(pid, ppid, pgid, argv):
        return {'pid': pid, 'ppid': ppid, 'pgid': pgid, 'uid': os.getuid(),
                'startTicks': pid * 100, 'state': 'S', 'argv': argv,
                'host': socket.gethostname(), 'executablePath': sys.executable,
                'executableSHA256': stop.sha(Path(sys.executable))}

    def validate(self, rows=None):
        return stop.validate_tree(rows or self.rows, self.runner, self.root,
                                  self.source, self.cases)

    def test_mixed_owned_tree_keeps_singleton_out_of_recovery_batches(self):
        with mock.patch.object(stop.os, 'kill') as kill, mock.patch.object(stop.os, 'killpg') as killpg:
            captured, gaps, batches = self.validate()
        self.assertEqual(set(captured), set(self.rows))
        self.assertEqual({x['pid'] for x in gaps}, {1002, 1004})
        self.assertEqual(len(batches), 1)
        self.assertEqual(batches[0]['caseIDs'], self.cases[:2])
        self.assertEqual(batches[0]['gapPID'], 1002)
        kill.assert_not_called()
        killpg.assert_not_called()

    def test_bad_singleton_preflight_rejects_before_freeze_or_signals(self):
        run_path = self.singleton / 'run.json'
        driver_path = self.singleton / 'driver.g'
        input_path = self.singleton / 'input.json'
        original_run, original_driver, original_input = (p.read_bytes() for p in [run_path, driver_path, input_path])
        changes = {
            'argv': lambda r: r['command'].insert(1, '--unexpected'),
            'source': lambda r: r.update(sourceSHA256='0' * 64),
            'host': lambda r: r.update(host='other-host'),
            'id': lambda r: r.update(id=self.cases[0]),
            'batch_contamination': lambda r: r.update(batchCaseIDs=self.cases[:2]),
            'nonboolean_pair': lambda r: r.update(pairedSpins=1),
            'input_hash': lambda r: r.update(inputSHA256='f' * 64),
        }
        driver_changes = {
            'source_root': lambda text: text.replace(str(self.snapshot), str(self.base / 'other')),
            'input_binding': lambda text: text.replace('dimension:=3', 'dimension:=4'),
            'duplicate_input': lambda text: text + 'U1_INPUT:=rec();;\n',
            'output_binding': lambda text: text.replace(str(self.singleton / 'native.json'), str(self.root / self.cases[0] / 'native.json')),
            'pair_marker': lambda text: text + 'Print("U1_PAIR_CASE_DONE ");;\n',
        }
        for name in list(changes) + list(driver_changes) + ['input_bytes']:
            with self.subTest(name=name):
                run_path.write_bytes(original_run)
                driver_path.write_bytes(original_driver)
                input_path.write_bytes(original_input)
                if name in changes:
                    record = json.loads(original_run)
                    changes[name](record)
                    self.write(run_path, record)
                elif name in driver_changes:
                    driver_path.write_text(driver_changes[name](original_driver.decode()))
                else:
                    input_path.write_bytes(original_input + b' ')
                output = self.base / ('rejected-' + name)
                argv = ['stop', '--root', str(self.root), '--snapshot', str(self.snapshot),
                        '--runner-pid', str(self.runner['pid']), '--output', str(output),
                        '--replacement', 'synthetic non-signaling regression']
                with mock.patch.object(sys, 'argv', argv), \
                        mock.patch.object(stop, 'process', return_value=self.runner), \
                        mock.patch.object(stop, 'scan_owned', return_value=self.rows), \
                        mock.patch.object(stop, 'freeze_tree') as freeze, \
                        mock.patch.object(stop.os, 'kill') as kill, \
                        mock.patch.object(stop.os, 'killpg') as killpg:
                    with self.assertRaises((ValueError, RuntimeError)):
                        stop.main()
                freeze.assert_not_called()
                kill.assert_not_called()
                killpg.assert_not_called()
                self.assertFalse(output.exists())
        run_path.write_bytes(original_run)
        driver_path.write_bytes(original_driver)
        input_path.write_bytes(original_input)

    def test_topology_and_missing_identity_fail_closed(self):
        for name, change in [
                ('argv', lambda row: row.update(argv=[])),
                ('executable', lambda row: row.pop('executableSHA256')),
                ('pgid', lambda row: row.update(pgid=self.runner['pgid'])),
                ('parent', lambda row: row.update(ppid=1002))]:
            with self.subTest(name=name):
                rows = copy.deepcopy(self.rows)
                change(rows[1004])
                with self.assertRaises(RuntimeError):
                    self.validate(rows)
        rows = copy.deepcopy(self.rows)
        rows[self.runner['pid']]['startTicks'] += 1
        with self.assertRaises(RuntimeError):
            self.validate(rows)

    def test_explicit_false_is_valid_but_incomplete_singleton_has_no_batch(self):
        path = self.singleton / 'run.json'
        record = json.loads(path.read_bytes())
        record['pairedSpins'] = False
        self.write(path, record)
        _, gaps, batches = self.validate()
        self.assertEqual(record['status'], 'running')
        self.assertEqual(len(gaps), 2)
        self.assertEqual(len(batches), 1)
        self.assertNotIn(self.cases[2], batches[0]['caseIDs'])


if __name__ == '__main__':
    unittest.main()
