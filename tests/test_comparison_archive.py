"""Archive legacy evidence as exact bytes without silent replacement."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from archive_comparison_inputs import (BOSS_FILES, FINITE_REFERENCE, LEGACY_GROUPS,
                                       collect_inputs, write_archive)


class ComparisonArchiveTests(unittest.TestCase):
    def test_all_inputs_preserved_including_raw_legacy_line_endings(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            boss, reference, legacy = (root / n for n in ('boss', 'reference', 'legacy'))
            legacy.mkdir()
            for base, relative in [(boss, p) for p in BOSS_FILES]+[(reference, FINITE_REFERENCE)]:
                path = base / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'fixture\r\n')
            originals = {}
            raw = b'original GAP stdout\r\npartial progress\rcompleted\n'
            for number in LEGACY_GROUPS:
                name = 'sg%03d.log' % number
                (legacy / name).write_bytes(raw)
                originals[name] = dict(original='/original/'+name,
                    sha256=hashlib.sha256(raw).hexdigest())
            (legacy / 'manifest.json').write_text(json.dumps(originals))
            pdf, text, finite = (root / n for n in ('sample.pdf', 'sample.txt', 'finite.json'))
            for path in (pdf, text, finite):
                path.write_bytes(b'fixture')
            material, manifest_hash = collect_inputs(boss, reference, legacy, pdf, text, finite)
            out = root / 'archive'
            manifest = write_archive(out, material, {'legacy_manifest_sha256': manifest_hash})
            self.assertEqual(len(manifest['inputs']), 12)
            for number in LEGACY_GROUPS:
                name = 'legacy_sg%03d.txt' % number
                self.assertEqual((out / name).read_bytes(), raw)
                self.assertEqual(manifest['inputs'][name]['original_source_path'],
                                 '/original/sg%03d.log' % number)
            with self.assertRaisesRegex(ValueError, 'destination exists'):
                write_archive(out, material, {})
            (legacy / 'sg068.log').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'legacy source hash mismatch'):
                collect_inputs(boss, reference, legacy, pdf, text, finite)


if __name__ == '__main__':
    unittest.main(verbosity=2)
