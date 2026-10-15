import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('downloader', HERE / 'download_completed.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
EVIDENCE = m.REPO / 'results/spacegroup_campaign_20261015/completed_g'


class DownloadTests(unittest.TestCase):
    def test_offline_actual_archive_and_frozen_replay(self):
        tag = 'sgfull-20261015-g-n08'
        raw = (EVIDENCE / 'nodes/n08/finalization.json').read_bytes()
        original_run = subprocess.run
        def run(argv, **kw):
            if argv[0] == 'ssh':
                with (EVIDENCE / 'archives' / (tag + '-evidence.tar.gz')).open('rb') as source:
                    shutil.copyfileobj(source, kw['stdout'])
                return subprocess.CompletedProcess(argv, 0, stderr=b'')
            return original_run(argv, **kw)
        with tempfile.TemporaryDirectory() as temp, patch.object(m, 'DOWNLOAD', Path(temp)), \
                patch.object(m, 'remote_reports', return_value={tag: raw}), patch.object(m.subprocess, 'run', side_effect=run):
            proof = m.download_one(tag, raw)
            self.assertTrue(proof['frozenCollectorExactReplay'])
            self.assertEqual(proof['acceptedCount'], 85)
            target = Path(proof['localExtractedPath'])
            self.assertEqual((target / 'finalization.json').read_bytes(), raw)
            self.assertEqual(m.verify_existing(target, raw), proof)

    def test_archive_rejects_traversal_links_duplicates_and_unexpected_root(self):
        for name, link, duplicate in [('../bad', False, False), ('/bad', False, False),
                                      ('good/a', True, False), ('good/a', False, True), ('other/a', False, False)]:
            data = io.BytesIO()
            with tarfile.open(fileobj=data, mode='w') as archive:
                info = tarfile.TarInfo(name)
                if link:
                    info.type = tarfile.SYMTYPE
                    info.linkname = '/etc/passwd'
                archive.addfile(info)
                if duplicate:
                    archive.addfile(info)
            data.seek(0)
            with tarfile.open(fileobj=data) as archive, self.assertRaises(ValueError):
                m.safe_members(archive, {'good'})

    def test_incomplete_report_rejected_before_download(self):
        with patch.object(m.subprocess, 'run') as run:
            with self.assertRaises(ValueError):
                m.download_one('case', json.dumps({'tag':'case', 'state':'waiting'}).encode())
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
