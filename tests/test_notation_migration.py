"""Independent regression against the actual pre-migration implementation."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from insulator import api as U
from insulator.notation import migrate_legacy_input, migrate_legacy_request
from insulator.worker import evaluate

ROOT = Path(__file__).resolve().parents[1]


class CharacterMigrationTests(unittest.TestCase):
    def test_actual_pre_migration_outputs_all_dimensions_and_characters(self):
        fixture = json.loads((ROOT / 'tests/fixtures/notation_legacy_45c37e9.json').read_text())
        self.assertEqual(fixture['reference_commit'], '45c37e9')
        self.assertEqual(len(fixture['cases']), 60)
        for case in fixture['cases']:
            old = case['request']
            before = deepcopy(old)
            canonical = migrate_legacy_request(old)
            with self.subTest(d=old['dimension'], op=old['op'], characters=case['characters']):
                self.assertEqual(evaluate(canonical), case['expected'])
                explicit = dict(old, schema_version=1, notation='legacy-charge-rho')
                self.assertEqual(evaluate(explicit), case['expected'])
                self.assertEqual(old, before)

    def test_api_circle_character_is_derived_and_legacy_keyword_is_not_reinterpreted(self):
        for sbit in (0, 1):
            for rbit in (0, 1):
                s, r = [0, sbit, 0], [0, rbit, 0]
                rho = [a ^ b for a, b in zip(r, s)]
                omega = U.Cochain(2, 2, {}, rho)
                sc, rc = U.char(2, s).ret(s), U.char(2, r).ret(r)
                sym = U.Symmetry(omega2_real=omega, s1=sc, r1=rc)
                self.assertEqual(sym.rho1.tw, tuple(rho))
                self.assertEqual(sym.r1.tw, tuple(r))
                self.assertEqual(U.Symmetry.from_legacy(omega, sc, rc).rho1.tw, tuple(rho))
                with self.assertRaises(TypeError):
                    U.Symmetry(omega2_real=omega, s1=sc, rho1=rc)

    def test_charge_and_circle_differentials_differ_under_ordinary_time_reversal(self):
        request = dict(schema_version=2, op='differential', dimension=2,
                       simplex_dimension=1, degree=0, s=[0, 1], r=[0, 0],
                       cochain={'0': '1', '1': '1'}, **{'return': 'top'})
        self.assertEqual(evaluate(dict(request, coefficient='r')), '0')
        self.assertEqual(evaluate(dict(request, coefficient='rho')), '-2')
        self.assertEqual(evaluate(dict(request, coefficient='rho', rho=[0, 1])), '-2')
        for bad in (dict(request, rho=[0, 0]), dict(request, r=[0, True]),
                    dict(request, schema_version=1), dict(request, schema_version=3),
                    dict(request, schema_version=2.0), dict(request, schema_version=True)):
            with self.assertRaises(ValueError):
                evaluate(bad)
        unversioned = dict(request, coefficient='rho')
        del unversioned['schema_version']
        self.assertEqual(evaluate(unversioned), '-2')
        legacy = dict(request)
        del legacy['schema_version']; legacy['rho'] = legacy.pop('r')
        with self.assertRaises(ValueError):
            evaluate(legacy)
        with self.assertRaises(ValueError):
            migrate_legacy_request(dict(legacy, notation='rho-is-circle'))
        with self.assertRaises(ValueError):
            migrate_legacy_request(dict(legacy, circle_action=[0, 0]))
        for operation in ('ping', 'batch', 'cache_info', 'cache_clear'):
            for version in (3, 2.0, True):
                with self.assertRaises(ValueError):
                    evaluate(dict(op=operation, requests=[], schema_version=version))

    def test_explicit_file_migration_preserves_input_and_rejects_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            old = Path(directory) / 'legacy.json'; new = Path(directory) / 'canonical.json'
            old.write_text(json.dumps({'s': [0, 1], 'rho': [0, 0], 'circle_action': [0, 1]}))
            digest = hashlib.sha256(old.read_bytes()).hexdigest()
            command = [sys.executable, str(ROOT / 'scripts/migrate_symmetry_input.py'), str(old), str(new)]
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(json.loads(new.read_text())['rho'], [0, 1])
            self.assertEqual(json.loads(new.read_text())['r'], [0, 0])
            self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(), digest)
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertNotEqual(subprocess.run(command[:-1] + [str(old)], capture_output=True).returncode, 0)
        with self.assertRaises(ValueError):
            migrate_legacy_input({'s': [0], 'rho': [0], 'notation': 'unknown'})

    @unittest.skipUnless(shutil.which('gap'), 'GAP and HAP are required')
    def test_gap_context_distinguishes_time_reversal_from_effective_mirror(self):
        script = r'''
OnBreak:=function() Where(12);QUIT_GAP(1);end;;
U1_ROOT:="@ROOT@";;Read(Concatenation(U1_ROOT,"/gap/load.g"));
for rb in [0,1] do
 data:=rec(schema_version:=2,multiplication:=[[0,1],[1,0]],identity_index:=0,
   s:=[0,1],r:=[0,rb],rho:=[0,(1+rb) mod 2],omega:=[["0","0"],["0","0"]]);;
 c:=U1FiniteContext(data,4);;g:=First(Elements(c.G),x->x<>Identity(c.G));;
 if c.r(g)<>rb or c.rho(g)<>(1+rb) mod 2 then Error("Character meaning changed");fi;
 if U1CoefficientAction(c,"Zr",g)<>(-1)^rb then Error("Charge action changed");fi;
 if U1CoefficientAction(c,"Zt",g)<>(-1)^(1+rb) then Error("Circle action changed");fi;
od;
Print("TIME_REVERSAL_AND_MIRROR_DISTINCT\n");QUIT_GAP(0);
'''.replace('@ROOT@', str(ROOT))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'characters.g'; path.write_text(script)
            result = subprocess.run(['gap', '-q', '-b', str(path)], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('TIME_REVERSAL_AND_MIRROR_DISTINCT', result.stdout)


if __name__ == '__main__':
    unittest.main()
