"""Offline recovery never infers successful process exits or changes raw runs."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest

from scripts.collect_expansion import load_campaign
from scripts.extend_e8_3p1 import extend_run, source_manifest
from scripts.recover_paired_campaign import (encoded, parse, preserve_campaign,
    sha, validate_preserved_ordinary_case, validate_recovered_case, validate_stop_report)
from insulator.e8_spacegroup import extend_spacegroup_classification

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'results/spacegroup_campaign_20261015/performance/cluster_d'
FIRST, SECOND = 'spacegroup_019_spin_half', 'spacegroup_019_spinless'
SINGLE = 'spacegroup_010_spin_half'


class PairedRecovery(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='u1-recovery-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.campaign, self.stop = self.base / 'original', self.base / 'stop'
        self.campaign.mkdir()
        self.stop.mkdir()
        shutil.copy2(FIXTURES / 'source.json', self.campaign / 'source.json')
        (self.campaign / 'selection.json').write_bytes(encoded([FIRST, SECOND]))
        for case in (FIRST, SECOND):
            shutil.copytree(FIXTURES / case, self.campaign / case)
            path = self.campaign / case / 'run.json'
            run = parse(path.read_bytes())
            self.original_completed = deepcopy(run)
            for key in ('exitCode', 'batchExitCode', 'elapsedSeconds', 'batchElapsedSeconds'):
                run.pop(key, None)
            run['status'] = 'running'
            path.write_bytes(encoded(run))
            (self.campaign / case / 'result.json').unlink()
        (self.campaign / SECOND / 'native.json').unlink()
        log = self.campaign / FIRST / 'stdout.log'
        log.write_bytes(log.read_bytes().replace(('U1_PAIR_CASE_DONE ' + SECOND + '\n').encode(), b''))
        run = parse((self.campaign / FIRST / 'run.json').read_bytes())
        self.remote = str(Path(run['command'][-1]).parents[1])
        self.snapshot = '/home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-c'
        executable = '/captured/gap-binary'
        process = dict(host=run['host'], uid=1000, pgid=100, startTicks=12345,
                       executablePath=executable, executableSHA256='a' * 64,
                       observedState='absent')
        runner = dict(process, pid=100, ppid=1, role='runner',
                      argv=['python3', self.snapshot + '/scripts/classify.py', '--output', self.remote])
        gap = dict(process, pid=101, ppid=100, pgid=101, startTicks=12346, role='gap',
                   argv=[executable, '-l', '/original/gap/root'] + run['command'][1:])
        worker = dict(process, pid=102, ppid=101, pgid=102, startTicks=12347, role='formula-worker',
                      argv=['python3', self.snapshot + '/scripts/formula_worker.py'])
        self.report = dict(schema='u1-paired-stop-v1', originalCampaignRoot=self.remote,
            sourceSnapshotPath=self.snapshot, sourceSHA256=run['sourceSHA256'],
            sourceSnapshotVerified=True, verifiedSourceSHA256=run['sourceSHA256'],
            stoppedObservedUTC='2026-10-15T15:00:00+00:00', allOwnedProcessesStopped=True,
            processes=[runner, gap, worker],
            batches=[dict(caseIDs=[FIRST, SECOND], host=run['host'], gapPID=101, runnerPID=100,
                          launchedCommand=run['command'], launcherPath=run['command'][0],
                          launcherSHA256='b' * 64, allOwnedDescendantsStopped=True, remainingOwnedPIDs=[])],
            evidence=[dict(path='processes_before.json', sha256=''), dict(path='processes_after.json', sha256='')])
        for item in self.report['evidence']:
            raw = encoded({'syntheticTestFixture': True, 'processes': self.report['processes']})
            (self.stop / item['path']).write_bytes(raw)
            item['sha256'] = sha(raw)
        self.refresh()

    def refresh(self):
        self.report['artifactsSHA256'] = {
            str(path.relative_to(self.campaign)): sha(path.read_bytes())
            for path in self.campaign.rglob('*') if path.is_file()}
        self.report_path = self.stop / 'cancellation.json'
        self.report_path.write_bytes(encoded(self.report))

    def preserve(self, name='subset'):
        output = self.base / name
        return output, preserve_campaign(self.campaign, self.report_path, output)

    def add_ordinary_singleton(self):
        """Real saved scientific data with explicitly synthetic execution paths."""
        tag = 'sgfull-20261015-g-n08'
        archive_path = ROOT / 'results/spacegroup_campaign_20261015/completed_g/archives' / (tag + '-evidence.tar.gz')
        directory = self.campaign / SINGLE
        directory.mkdir()
        with tarfile.open(archive_path) as archive:
            for name in ('input.json', 'native.json', 'driver.g', 'stdout.log', 'stderr.log'):
                (directory / name).write_bytes(archive.extractfile(tag + '/' + SINGLE + '/' + name).read())
        data = parse((directory / 'input.json').read_bytes())
        native = parse((directory / 'native.json').read_bytes())
        run = parse((FIXTURES / FIRST / 'run.json').read_bytes())
        for name in list(run):
            if name.startswith('batch') or name == 'pairedSpins':
                del run[name]
        run.update(id=SINGLE, inputSHA256=sha((directory / 'input.json').read_bytes()))
        run['command'][-1] = self.remote + '/' + SINGLE + '/driver.g'
        driver = ('U1_ROOT:=' + json.dumps(self.snapshot) + ';;\n'
                  'Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n'
                  'output:=OutputTextFile(' + json.dumps(self.remote + '/' + SINGLE + '/native.json') + ',false);;\n'
                  'PrintTo(output,U1JSON(result),"\\n");;\nCloseStream(output);;\nQUIT;\n')
        (directory / 'driver.g').write_text(driver)
        (directory / 'run.json').write_bytes(encoded(run))
        (directory / 'result.json').write_bytes(encoded({'input': data, 'classification': native, 'run': run}))
        (self.campaign / 'selection.json').write_bytes(encoded([FIRST, SECOND, SINGLE]))
        self.refresh()
        return directory

    def test_complete_first_case_recovered_and_incomplete_second_queued(self):
        before = {str(p.relative_to(self.campaign)): p.read_bytes() for p in self.campaign.rglob('*') if p.is_file()}
        output, ledger = self.preserve()
        self.assertEqual(ledger['recoveredCases'], [FIRST])
        self.assertEqual(ledger['retryCases'], [SECOND])
        self.assertEqual(validate_recovered_case(output, FIRST)['nativeChainIdentitiesVerified'], True)
        run = parse((output / FIRST / 'run.json').read_bytes())
        self.assertEqual(run['status'], 'recovered_complete')
        for field in ('exitCode', 'batchExitCode', 'elapsedSeconds', 'startedUTC'):
            self.assertNotIn(field, run)
        self.assertEqual((output / FIRST / 'native.json').read_bytes(), before[FIRST + '/native.json'])
        self.assertEqual((output / '_recovery/original_runs' / FIRST / 'run.json').read_bytes(), before[FIRST + '/run.json'])
        after = {str(p.relative_to(self.campaign)): p.read_bytes() for p in self.campaign.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertFalse((output / SECOND).exists())
        with self.assertRaises(ValueError):
            preserve_campaign(self.campaign, self.report_path, output)

    def test_defaults_reject_and_explicit_e8_collector_pipeline_accepts(self):
        output, _ = self.preserve()
        with self.assertRaisesRegex(ValueError, 'allow-recovered'):
            load_campaign(output, 'ci')
        records, checks, _ = load_campaign(output, 'ci', allow_recovered=True)
        result = records[FIRST]['record']
        self.assertTrue(checks[0]['explicitRecoveryAcceptance']['capturedProcessTreeStopped'])
        with self.assertRaises(ValueError):
            extend_spacegroup_classification(result)
        extended = self.base / 'e8'
        extended.mkdir()
        source = source_manifest(include_recovery=True)
        (extended / 'source.json').write_bytes(encoded(source))
        (extended / 'selection.json').write_bytes(encoded([FIRST]))
        with self.assertRaisesRegex(ValueError, 'allow-recovered'):
            extend_run(output / FIRST / 'result.json', extended, source)
        extend_run(output / FIRST / 'result.json', extended, source, allow_recovered=True)
        self.assertEqual((extended / FIRST / 'ci_result.json').read_bytes(), (output / FIRST / 'result.json').read_bytes())
        with self.assertRaises(ValueError):
            load_campaign(extended, 'e8')
        collected = self.base / 'collection'
        subprocess.run([sys.executable, str(ROOT / 'scripts/collect_expansion.py'),
                        '--ci-root', str(output), '--e8-root', str(extended),
                        '--allow-recovered', '--output', str(collected)],
                       check=True, stdout=subprocess.DEVNULL)
        self.assertTrue(parse((collected / 'collection.json').read_bytes())['accepted'])
        altered = deepcopy(result)
        altered['classification']['scope'] += ' altered'
        with self.assertRaisesRegex(ValueError, 'exact CI result'):
            extend_spacegroup_classification(altered, recovery_root=output)

    def test_ordinary_complete_case_preserves_original_exit_metadata(self):
        directory = self.campaign / FIRST
        for name in ('run.json', 'result.json'):
            shutil.copy2(FIXTURES / FIRST / name, directory / name)
        self.report['batches'] = []  # No live GAP identity is needed for an already completed result.
        self.refresh()
        output, ledger = self.preserve()
        self.assertEqual(ledger['ordinaryCompleteCases'], [FIRST])
        self.assertEqual(ledger['recoveredCases'], [])
        for name in ('run.json', 'result.json'):
            self.assertEqual((directory / name).read_bytes(), (output / FIRST / name).read_bytes())
        load_campaign(output, 'ci')

    def test_mixed_ordinary_singleton_and_paired_recovery_revalidate_portably(self):
        directory = self.add_ordinary_singleton()
        before = {str(p.relative_to(self.campaign)): p.read_bytes() for p in self.campaign.rglob('*') if p.is_file()}
        output, ledger = self.preserve('mixed')
        self.assertEqual(ledger['ordinaryCompleteCases'], [SINGLE])
        self.assertEqual(ledger['recoveredCases'], [FIRST])
        self.assertEqual(ledger['retryCases'], [SECOND])
        for name in ('input.json', 'native.json', 'driver.g', 'run.json', 'result.json', 'stdout.log', 'stderr.log'):
            self.assertEqual((output / SINGLE / name).read_bytes(), before[SINGLE + '/' + name])
        self.assertEqual(before, {str(p.relative_to(self.campaign)): p.read_bytes() for p in self.campaign.rglob('*') if p.is_file()})
        self.campaign.rename(self.base / 'original-unavailable')
        self.assertTrue(validate_preserved_ordinary_case(output, SINGLE)['originalExitMetadataPreserved'])
        self.assertTrue(validate_recovered_case(output, FIRST)['capturedProcessTreeStopped'])
        records, _, _ = load_campaign(output, 'ci', allow_recovered=True)
        self.assertEqual(set(records), {FIRST, SINGLE})
        with self.assertRaises(ValueError):
            validate_recovered_case(output, SINGLE)
        with self.assertRaises(ValueError):
            validate_preserved_ordinary_case(output, FIRST)
        (output / SINGLE / 'stdout.log').write_bytes(b'changed original log')
        with self.assertRaises(ValueError):
            validate_preserved_ordinary_case(output, SINGLE)

    def test_singleton_rejects_incomplete_failed_misleading_and_unbound_evidence(self):
        directory = self.add_ordinary_singleton()
        originals = {name: (directory / name).read_bytes() for name in ('run.json', 'result.json', 'driver.g')}
        kinds = ['incomplete', 'failed', 'boolean_exit', 'batch_field', 'paired_false_batch',
                 'paired_flag', 'wrong_driver', 'wrong_source', 'wrong_native', 'extra_native',
                 'marker_in_driver', 'mismatched_result', 'missing_stderr']
        stderr = (directory / 'stderr.log').read_bytes()
        for kind in kinds:
            with self.subTest(kind=kind):
                for name, raw in originals.items():
                    (directory / name).write_bytes(raw)
                (directory / 'stderr.log').write_bytes(stderr)
                run = parse(originals['run.json'])
                result = parse(originals['result.json'])
                driver = originals['driver.g'].decode()
                if kind == 'incomplete':
                    run['status'] = 'running'
                    run.pop('exitCode')
                elif kind == 'failed': run['exitCode'] = 1
                elif kind == 'boolean_exit': run['exitCode'] = False
                elif kind == 'batch_field': run['batchCaseIDs'] = [SINGLE]
                elif kind == 'paired_false_batch': run.update(pairedSpins=False, batchCaseIDs=[SINGLE])
                elif kind == 'paired_flag': run['pairedSpins'] = 1
                elif kind == 'wrong_driver': run['command'][-1] += '.wrong'
                elif kind == 'wrong_source': driver = driver.replace(self.snapshot, self.snapshot + '-wrong')
                elif kind == 'wrong_native': driver = driver.replace('/' + SINGLE + '/native.json', '/' + FIRST + '/native.json')
                elif kind == 'extra_native': driver += 'output:=OutputTextFile("/extra/native.json",false);;\n'
                elif kind == 'marker_in_driver': driver += 'Print("U1_PAIR_CASE_DONE ");;\n'
                elif kind == 'missing_stderr': (directory / 'stderr.log').unlink()
                result['run'] = run
                if kind == 'mismatched_result': result['classification']['freeRank'] += 1
                (directory / 'run.json').write_bytes(encoded(run))
                (directory / 'result.json').write_bytes(encoded(result))
                (directory / 'driver.g').write_text(driver)
                self.refresh()
                _, ledger = self.preserve('single-rejected-' + kind)
                self.assertNotIn(SINGLE, ledger['preservedCases'])
                self.assertIn(SINGLE, ledger['retryCases'])
                self.assertEqual(ledger['recoveredCases'], [FIRST])

    def test_missing_process_identity_or_stop_evidence_rejected(self):
        for field in ('pid', 'ppid', 'pgid', 'uid', 'startTicks', 'argv', 'executablePath', 'executableSHA256', 'host'):
            report = deepcopy(self.report)
            del report['processes'][1][field]
            with self.subTest(field=field), self.assertRaises((ValueError, KeyError, TypeError)):
                validate_stop_report(report)
        changes = [('allOwnedProcessesStopped', False), ('evidence', []), ('sourceSnapshotPath', None), ('sourceSnapshotVerified', False), ('verifiedSourceSHA256', '0' * 64)]
        for field, value in changes:
            report = deepcopy(self.report)
            report[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_stop_report(report)
        for change in ('active', 'wrong_argv', 'wrong_parent', 'remaining'):
            report = deepcopy(self.report)
            if change == 'active': report['processes'][1]['observedState'] = 'active'
            elif change == 'wrong_argv': report['processes'][1]['argv'][-1] += '.wrong'
            elif change == 'wrong_parent': report['processes'][1]['ppid'] = 999
            else: report['batches'][0]['remainingOwnedPIDs'] = [102]
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_stop_report(report)

    def test_missing_marker_partial_native_and_bad_certificates_are_not_recovered(self):
        native_path = self.campaign / FIRST / 'native.json'
        original = native_path.read_bytes()
        variants = [('truncated', None), ('chain', False), ('count', 0), ('smith', [3]), ('filling', 999), ('root', '1/0')]
        for index, (kind, value) in enumerate(variants):
            changed = parse(original)
            if kind == 'chain': changed['nativeChainIdentitiesVerified'] = value
            elif kind == 'count': changed['nativeCompletionChecks'] = value
            elif kind == 'smith': changed['torsion'] = value
            elif kind == 'filling': changed['spaceGroupFilling']['fillingStep'] = value
            elif kind == 'root': changed['generators'][0]['nativePhase'][0] = value
            native_path.write_bytes(b'{"incomplete":' if kind == 'truncated' else encoded(changed))
            self.refresh()
            _, ledger = self.preserve('rejected-' + str(index))
            self.assertEqual(ledger['preservedCases'], [])
            self.assertIn(FIRST, ledger['retryCases'])
        native_path.write_bytes(original)
        log = self.campaign / FIRST / 'stdout.log'
        log.write_bytes(log.read_bytes().replace(('U1_PAIR_CASE_DONE ' + FIRST).encode(), b'not a completion marker'))
        self.refresh()
        _, ledger = self.preserve('missing-marker')
        self.assertEqual(ledger['preservedCases'], [])

    def test_wrong_context_hashes_and_post_recovery_mutation_rejected(self):
        self.report['sourceSnapshotPath'] += '-wrong'
        self.report['processes'][0]['argv'][1] = self.report['sourceSnapshotPath'] + '/scripts/classify.py'
        self.refresh()
        _, ledger = self.preserve('wrong-source')
        self.assertEqual(ledger['preservedCases'], [])
        self.report['sourceSnapshotPath'] = self.snapshot
        self.report['processes'][0]['argv'][1] = self.snapshot + '/scripts/classify.py'
        self.refresh()
        output, _ = self.preserve()
        run = parse((output / FIRST / 'run.json').read_bytes())
        run['exitCode'] = 0
        (output / FIRST / 'run.json').write_bytes(encoded(run))
        with self.assertRaises(ValueError):
            validate_recovered_case(output, FIRST)
        (self.stop / 'processes_after.json').write_text('changed')
        with self.assertRaises(ValueError):
            self.preserve('changed-evidence')


if __name__ == '__main__':
    unittest.main()
