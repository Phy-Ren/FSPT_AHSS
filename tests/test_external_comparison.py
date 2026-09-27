"""Independent-result provenance guards for the external comparison report."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from compare_external_refs import (CURRENT_FORMULA_CONVENTION, audit_computed,
                                   invariant_factors, load_frozen, read_results)


def record(number):
    hashes = {'gap/test-fixture.g': hashlib.sha256(b'fixture').hexdigest()}
    return dict(space_group=number, convention='physical-spin-half-det-sign-omega0',
        formula_convention=CURRENT_FORMULA_CONVENTION, sptset_loaded=False, status='computed',
        pip=dict(status='computed', orders=[], free_rank=0), majorana=[], complex_fermion=[], bosonic=[],
        source_sha256=hashes, source_id=hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest(),
        stacking=dict(status='computed', invariants=[], lower=dict(invariants=[], presentation=[],
            smithRowTransform=[], smithColumnTransform=[], smithDiagonal=[], enumeratedPhaseProducts=0)))


class ExternalComparisonTests(unittest.TestCase):
    def test_isomorphic_cyclic_decompositions_and_free_rank(self):
        self.assertEqual(invariant_factors([0, 2, 3, 4]), [0, 2, 12])
        self.assertEqual(invariant_factors([12, 0, 2]), [0, 2, 12])
        self.assertNotEqual(invariant_factors([2, 2]), invariant_factors([4]))

    def test_final_guard_rejects_partial_or_missing_phase(self):
        audit_computed({1: record(1)}, require_complete=False)
        with self.assertRaisesRegex(ValueError, 'all 230 complete'):
            audit_computed({1: record(1)}, require_complete=True)
        records = {n: record(n) for n in range(1, 231)}
        del records[1]['stacking']
        with self.assertRaisesRegex(ValueError, 'full stacking is missing'):
            audit_computed(records, require_complete=True)

    def test_final_guard_requires_current_convention_and_uniform_source(self):
        records = {n: record(n) for n in range(1, 231)}
        audit_computed(records, require_complete=True)
        records[1]['formula_convention'] = 'obsolete'
        with self.assertRaisesRegex(ValueError, 'formula convention differs'):
            audit_computed(records, require_complete=True)
        records[1] = record(1)
        records[1]['source_sha256']['gap/test-fixture.g'] = hashlib.sha256(b'other').hexdigest()
        records[1]['source_id'] = hashlib.sha256(json.dumps(records[1]['source_sha256'], sort_keys=True).encode()).hexdigest()
        with self.assertRaisesRegex(ValueError, 'one uniform source'):
            audit_computed(records, require_complete=True)

    def test_frozen_manifest_and_every_result_hash_are_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            hashes = {}
            for n in range(1, 231):
                path = root / ('sg%d.json' % n)
                path.write_text(json.dumps(record(n)))
                hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            manifest = dict(groups=230, external_answers_consulted=False, frozen_at=123, result_sha256=hashes)
            mp = root / 'manifest.json'
            mp.write_text(json.dumps(manifest))
            records, loaded, provenance = load_frozen(root)
            self.assertEqual(len(records), 230)
            self.assertEqual(loaded, manifest)
            self.assertEqual(provenance['result_sha256'], hashes)
            self.assertEqual(provenance['manifest_sha256'], hashlib.sha256(mp.read_bytes()).hexdigest())
            target = root / 'sg17.json'
            target.write_text(target.read_text()+'\n')
            with self.assertRaisesRegex(ValueError, 'frozen result hash mismatch: sg17.json'):
                load_frozen(root)

    def test_filename_group_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'sg1.json').write_text(json.dumps(record(2)))
            with self.assertRaisesRegex(ValueError, 'filename/group mismatch'):
                read_results(root)

    def test_checkpoint_source_map_must_come_from_the_identical_audited_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            checkpoint = record(1)
            source = checkpoint['source_id']
            hashes = checkpoint.pop('source_sha256')
            del checkpoint['stacking']
            path = root / 'sg1.json'
            path.write_text(json.dumps(checkpoint))
            original = path.read_bytes()
            with self.assertRaisesRegex(ValueError, 'no verifiable source-file hash map'):
                read_results(root)
            loaded = read_results(root, {source: hashes})
            self.assertEqual(loaded[1]['source_sha256'], hashes)
            self.assertEqual(path.read_bytes(), original)


if __name__ == '__main__':
    unittest.main(verbosity=2)
