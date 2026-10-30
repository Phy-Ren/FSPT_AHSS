"""Subset acceptance validates whole recovered parents without rewriting ledgers."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from insulator.notation import legacy_metadata_view

from scripts.collect_expansion import selection_plan_requests
from scripts.extend_e8_3p1 import extend_run, source_manifest
from scripts.recover_paired_campaign import encoded, parse, sha
import test_paired_recovery as recovery_fixtures

FIXTURES, FIRST, SECOND, ROOT = (recovery_fixtures.FIXTURES, recovery_fixtures.FIRST,
                                 recovery_fixtures.SECOND, recovery_fixtures.ROOT)


class CollectorSelectionPlan(unittest.TestCase):
    def setUp(self):
        # Use the real saved SG19 native records and original paired driver,
        # with the same explicit synthetic stopped-process evidence used by
        # the recovery suite. Both completed marker lines are restored here.
        self.fixture = recovery_fixtures.PairedRecovery(methodName='runTest')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.base = self.fixture.base
        shutil.copy2(FIXTURES / SECOND / 'native.json', self.fixture.campaign / SECOND / 'native.json')
        shutil.copy2(FIXTURES / FIRST / 'stdout.log', self.fixture.campaign / FIRST / 'stdout.log')
        self.fixture.refresh()
        self.ci, ledger = self.fixture.preserve()
        self.assertEqual(set(ledger['recoveredCases']), {FIRST, SECOND})
        self.e8 = self.base / 'e8'
        self.e8.mkdir()
        source = source_manifest(include_recovery=True)
        (self.e8 / 'source.json').write_bytes(encoded(source))
        (self.e8 / 'selection.json').write_bytes(encoded([FIRST, SECOND]))
        for case in (FIRST, SECOND):
            extend_run(self.ci / case / 'result.json', self.e8, source, allow_recovered=True)
        self.plan = self.base / 'plan.json'
        self.entries = [{'kind': 'ci', 'root': self.ci.name, 'cases': [FIRST]},
                        {'kind': 'e8', 'root': self.e8.name, 'cases': [FIRST]}]

    def collect(self, entries=None, allow=True, label='collected'):
        self.plan.write_bytes(encoded(self.entries if entries is None else entries))
        output = self.base / label
        command = [sys.executable, str(ROOT / 'scripts/collect_expansion.py'),
                   '--selection-plan', str(self.plan), '--output', str(output)]
        if allow:
            command += ['--allow-recovered']
        result = subprocess.run(command, text=True, capture_output=True)
        return result, output

    @staticmethod
    def tree_bytes(root):
        return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}

    def test_one_of_two_recovered_cases_preserves_full_parent_and_records_subset(self):
        before = {str(p): self.tree_bytes(p) for p in (self.fixture.campaign, self.fixture.stop, self.ci, self.e8)}
        result, output = self.collect()
        self.assertEqual(result.returncode, 0, result.stderr)
        for path, expected in before.items():
            self.assertEqual(self.tree_bytes(Path(path)), expected)
        target = output / '3p1d/space_groups'
        self.assertEqual(parse((target / 'ci_results.json').read_bytes()),
                         legacy_metadata_view([parse((self.ci / FIRST / 'result.json').read_bytes())]))
        self.assertEqual(parse((target / 'results.json').read_bytes()),
                         legacy_metadata_view([parse((self.e8 / FIRST / 'result.json').read_bytes())]))
        provenance = parse((target / 'provenance.json').read_bytes())
        self.assertEqual(len(provenance), 2)
        for item in provenance:
            self.assertEqual(item['selection'], [FIRST, SECOND])
            self.assertEqual(item['originalSelection'], [FIRST, SECOND])
            self.assertEqual(item['originalSelectionSHA256'], item['selectionSHA256'])
            self.assertEqual(item['requestedSubset'], [FIRST])
            self.assertEqual(item['acceptedSelection'], [FIRST])
            self.assertEqual(set(item['resultHashes']), {FIRST})
            self.assertEqual(item['fullParentValidation'], {'allSelectedParentCasesPassed': True, 'caseCount': 2})
            self.assertEqual(item['selectionPlan']['SHA256'], sha(self.plan.read_bytes()))
        validation = parse((target / 'validation.json').read_bytes())
        self.assertEqual(validation['selectedCases'], [FIRST])
        self.assertEqual(len(validation['checks']), 2)
        self.assertTrue(all(item['id'] == FIRST for item in validation['checks']))

    def test_recovered_selection_still_requires_explicit_opt_in(self):
        result, output = self.collect(allow=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('allow-recovered', result.stderr)
        self.assertFalse(output.exists())

    def test_missing_cases_and_duplicate_requests_rejected(self):
        variants = [self.entries + [self.entries[0]],
                    [dict(self.entries[0], cases=['spacegroup_999_spinless']), self.entries[1]],
                    [dict(self.entries[0], cases=[FIRST, FIRST]), self.entries[1]]]
        for index, entries in enumerate(variants):
            with self.subTest(index=index):
                result, output = self.collect(entries, label='invalid-' + str(index))
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())

    def test_plan_schema_and_paths_are_strict(self):
        entries = [[], {}, [{'kind': 'wrong', 'root': self.ci.name, 'cases': [FIRST]}],
                   [{'kind': 'ci', 'root': '', 'cases': [FIRST]}],
                   [{'kind': 'ci', 'root': 'does-not-exist', 'cases': [FIRST]}],
                   [{'kind': 'ci', 'root': self.ci.name, 'cases': []}],
                   [{'kind': 'ci', 'root': self.ci.name, 'cases': ['../' + FIRST]}],
                   [{'kind': 'ci', 'root': self.ci.name, 'cases': [FIRST], 'typo': True}]]
        for index, value in enumerate(entries):
            self.plan.write_bytes(encoded(value))
            with self.subTest(index=index), self.assertRaises(ValueError):
                selection_plan_requests(self.plan)

    def test_unselected_corrupt_parent_case_is_not_bypassed(self):
        (self.ci / SECOND / 'native.json').write_text('{}\n')
        result, output = self.collect()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())

    def test_same_case_e8_from_different_exact_ci_parent_is_rejected(self):
        other = self.base / 'ordinary_e8'
        other.mkdir()
        source = source_manifest()
        (other / 'source.json').write_bytes(encoded(source))
        (other / 'selection.json').write_bytes(encoded([FIRST]))
        extend_run(FIXTURES / FIRST / 'result.json', other, source)
        entries = [self.entries[0], {'kind': 'e8', 'root': other.name, 'cases': [FIRST]}]
        result, output = self.collect(entries)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('different exact CI artifact', result.stderr)
        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
