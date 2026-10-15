"""The public workflow completes only after exact four-data acceptance."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import classify_3p1d as workflow

ROOT = Path(__file__).resolve().parents[1]
CASE = 'point3_04_spinless'  # Mirror: a nonzero neutral H1 direction.


class WorkflowFailures(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='u1-four-data-workflow-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def arguments(self, output, *extra):
        return ['--case', CASE, '--gap', sys.executable, '--output', str(output), *extra]

    def test_invalid_selection_and_flags_reject_before_output(self):
        bad = [[], ['--family', 'point2'], ['--case', 'point2_02_spinless'],
               ['--case', 'internal_cyclic_3_4p1'], ['--case', 'missing'],
               ['--case', CASE, '--spin', 'spin_half'], ['--case', CASE, '--jobs', '0'],
               ['--case', CASE, '--timeout', '0'], ['--case', CASE, '--memory', '8g;bad'],
               ['--case', CASE, '--uniform-iqh'], ['--case', CASE, '--dimension', '4'],
               ['--case', CASE, '--case', CASE], ['--case', CASE, '--formula-mode', 'invalid']]
        for index, options in enumerate(bad):
            output = self.base / str(index)
            with self.subTest(options=options), contextlib.redirect_stderr(io.StringIO()), \
                    patch.object(workflow.subprocess, 'run') as run:
                with self.assertRaises(SystemExit) as caught:
                    workflow.main(['--gap', sys.executable, '--output', str(output), *options])
                self.assertEqual(caught.exception.code, 2)
                run.assert_not_called()
                self.assertFalse(output.exists())

    def test_each_stage_failure_stops_without_claiming_complete(self):
        for failure_index, failure_stage in enumerate(('ci', 'e8', 'acceptance')):
            output = self.base / failure_stage
            calls = []
            def execute(command, **kwargs):
                index = len(calls)
                calls.append(command)
                kwargs['stdout'].write(b'stage-output\xff\n')
                kwargs['stderr'].write(b'stage-error\n')
                if index < failure_index:
                    directory = output / ('ci', 'e8')[index]
                    directory.mkdir()
                    (directory / 'selection.json').write_text(json.dumps([CASE]))
                return subprocess.CompletedProcess(command, 17 if index == failure_index else 0)
            with self.subTest(stage=failure_stage), patch.object(workflow.subprocess, 'run', side_effect=execute), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(workflow.main(self.arguments(output)), 1)
            record = json.loads((output / 'workflow.json').read_bytes())
            self.assertEqual((record['status'], record['stage']), ('failed', failure_stage))
            self.assertEqual(len(calls), failure_index + 1)
            self.assertEqual(record['stages'][-1]['exitCode'], 17)
            self.assertEqual(record['stages'][-1]['status'], 'failed')
            self.assertNotIn('acceptedCount', record)
            self.assertFalse((output / 'accepted').exists())
            self.assertEqual((output / 'logs' / (failure_stage + '.stdout.log')).read_bytes(), b'stage-output\xff\n')

    def test_zero_exit_without_accepted_artifacts_is_failure(self):
        output = self.base / 'missing-acceptance'
        calls = []
        def execute(command, **kwargs):
            calls.append(command)
            if len(calls) < 3:
                directory = output / ('ci', 'e8')[len(calls) - 1]
                directory.mkdir()
                (directory / 'selection.json').write_text(json.dumps([CASE]))
            return subprocess.CompletedProcess(command, 0)
        with patch.object(workflow.subprocess, 'run', side_effect=execute), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            code = workflow.main(self.arguments(output))
        self.assertEqual(code, 1)
        record = json.loads((output / 'workflow.json').read_bytes())
        self.assertEqual((record['status'], record['stage']), ('failed', 'verify_accepted'))
        self.assertEqual([row['exitCode'] for row in record['stages']], [0, 0, 0])
        self.assertNotIn('acceptedCount', record)

    def test_exact_modes_and_task_options_forwarded(self):
        output = self.base / 'options'
        argv = self.arguments(output, '--spin', 'spinless', '--pair-spins', '--largest-first',
                              '--jobs', '3', '--timeout', '91', '--memory', '2g',
                              '--charge-primary', 'compare', '--phase-class', 'native',
                              '--closed-charge-source', 'reference', '--vacuum-reduction', 'reference',
                              '--formula-mode', 'python')
        args = workflow.parser().parse_args(argv)
        selected = workflow.preflight(args)
        command = workflow.commands(args, selected)[0][1]
        for option, value in [('--spin', 'spinless'), ('--jobs', '3'), ('--timeout', '91'),
                              ('--memory', '2g'), ('--charge-primary', 'compare'),
                              ('--phase-class', 'native'), ('--closed-charge-source', 'reference'),
                              ('--vacuum-reduction', 'reference')]:
            self.assertEqual(command[command.index(option) + 1], value)
        self.assertIn('--pair-spins', command)
        self.assertIn('--largest-first', command)
        with patch.object(workflow.subprocess, 'run', return_value=subprocess.CompletedProcess(command, 9)) as run, \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(workflow.run_workflow(args, selected), 1)
        self.assertEqual(run.call_args.kwargs['env']['U1_DAG_MODE'], 'python')


@unittest.skipUnless(shutil.which('gap'), 'GAP and HAP are required')
class WorkflowActualPointGroup(unittest.TestCase):
    def test_nonzero_e8_end_to_end_and_no_overwrite(self):
        with tempfile.TemporaryDirectory(prefix='u1-public-three-dimensional-') as temp:
            output = Path(temp) / 'calculation'
            command = [sys.executable, str(ROOT / 'scripts/classify_3p1d.py'), '--case', CASE,
                       '--timeout', '90', '--memory', '2g', '--output', str(output)]
            result = subprocess.run(command, text=True, capture_output=True, timeout=120)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            record = json.loads((output / 'workflow.json').read_bytes())
            self.assertEqual((record['status'], record['stage'], record['acceptedCount']), ('complete', 'complete', 1))
            self.assertEqual([stage['status'] for stage in record['stages']], ['succeeded'] * 3)
            self.assertTrue(all(stage['exitCode'] == 0 for stage in record['stages']))
            ci_raw = (output / 'ci' / CASE / 'result.json').read_bytes()
            self.assertEqual((output / 'e8' / CASE / 'ci_result.json').read_bytes(), ci_raw)
            collection = json.loads((output / 'accepted/3p1d/point_groups/results.json').read_bytes())
            final = collection[0]['classification']
            self.assertEqual(final['e8H1']['torsion'], [2])
            self.assertTrue(final['neutralE8Included'])
            self.assertFalse(final['physicalClassificationCertified'])
            self.assertEqual(final['ciSector'], json.loads(ci_raw)['classification'])
            self.assertEqual(final['orderedFields'], ['e_1', 'n_1', 'n_3', 'nu_4'])
            before = {str(p.relative_to(output)): p.read_bytes() for p in output.rglob('*') if p.is_file()}
            refused = subprocess.run(command, text=True, capture_output=True, timeout=10)
            self.assertEqual(refused.returncode, 2)
            self.assertEqual(before, {str(p.relative_to(output)): p.read_bytes() for p in output.rglob('*') if p.is_file()})


if __name__ == '__main__':
    unittest.main()
