import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'point_marked_comparison', ROOT/'scripts/compare_point_group_marked_controls.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PointMarkedControls(unittest.TestCase):
    def test_archived_controls(self):
        archive = ROOT/'results/optimization_validation/point_group_backend/marked_audit'
        actual = MODULE.compare(ROOT/'results/point_groups', archive/'run', archive/'tasks')
        expected = json.loads((archive/'comparison.json').read_bytes())
        self.assertEqual(actual, expected)

    def test_native_witness_difference_not_ignored(self):
        with self.assertRaisesRegex(AssertionError, 'Unexplained'):
            MODULE.reason('/stacking/lower/generators/1/lift/phase4/0/0', 0, 1)

    def test_stage_names_not_ignored(self):
        with self.assertRaisesRegex(AssertionError, 'Unexplained'):
            MODULE.reason('/stage_timings/0/stage', 'backend', 'classification')

    def test_audit_flag_cannot_regress(self):
        with self.assertRaisesRegex(AssertionError, 'demonstrated'):
            MODULE.reason('/stacking/lower/witnesses/1/checkedComparisonSupport', True, False)


if __name__ == '__main__':
    unittest.main()
