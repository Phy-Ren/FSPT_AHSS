"""Replay all local equations and bind the derived incoming phase to GAP."""
import json
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from derive_pip_incoming_background import derive


class IncomingBackgroundFormulaTests(unittest.TestCase):
    def test_complete_universal_derivation_and_runtime_coefficients(self):
        result=derive()
        text=(ROOT/'gap/pip_incoming_background.g').read_text()
        array=re.search(r'values:=(\[.*?\]);',text,re.S)
        self.assertIsNotNone(array)
        self.assertEqual(json.loads(array.group(1)),result['numerators'])
        self.assertEqual(result['checks']['closed_omega_five_simplices'],1024)
        self.assertEqual(result['checks']['square_equations'],64)
        self.assertEqual(result['checks']['residual_normalized_half_phase_dimension'],4)
        self.assertEqual(result['checks']['exact_half_phase_dimension'],3)
        self.assertEqual(result['quadruple_gauge3_binary'],[0,0,1,0,0,0,0,0])


if __name__=='__main__':
    unittest.main(verbosity=2)
