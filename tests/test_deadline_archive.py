"""Full 230-record archive integration with a separately audited extension.

All records are disposable fixtures. No processes, signals or cluster work.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import unittest

import test_archive_campaign as campaign_fixture
import test_deadline_evidence as extension_fixture


class DeadlineArchiveTests(unittest.TestCase):
    def setUp(self):
        self.campaign = campaign_fixture.ArchiveCampaignTests()
        self.addCleanup(self.campaign.doCleanups)
        self.campaign.setUp()
        self.extension = extension_fixture.DeadlineEvidenceTests()
        self.addCleanup(self.extension.doCleanups)
        self.extension.setUp()
        c, e = self.campaign, self.extension
        manifest = json.loads((c.run/'campaign.json').read_text())
        manifest['tasks'][218] = e.task.copy()
        campaign_fixture.save(c.run/'campaign.json', manifest)
        shutil.rmtree(c.tasks/'task219')
        campaign_fixture.save(c.tasks/e.ident/'status.json', e.status)
        (c.tasks/e.ident/'metrics.txt').write_bytes(e.metrics)
        (c.tasks/e.ident/'stdout.log').write_bytes(b'SG219 completed under explicit extension\r\n')
        observation = json.loads((c.run/'observation.json').read_text())
        observation['submitted_at'] = min(t['created'] for t in manifest['tasks'])
        for event in observation['history']:
            event['elapsed_seconds'] = event['observed_at']-observation['submitted_at']
        campaign_fixture.save(c.run/'observation.json', observation)
        # Keep this relative so archive replay must honor original_run.
        campaign_fixture.save(c.run/'deadline_extensions.json', dict(
            schema='fspt-deadline-extension-index-v1',
            tasks={e.ident:os.path.relpath(e.ledger, c.run)}))

    def test_complete_archive_preserves_timeout_and_replays_without_original_inputs(self):
        c, e = self.campaign, self.extension
        status_raw = (c.tasks/e.ident/'status.json').read_bytes()
        index_raw = (c.run/'deadline_extensions.json').read_bytes()
        ledger_raw = {str(p.relative_to(e.ledger)):p.read_bytes()
                      for p in e.ledger.rglob('*') if p.is_file()}
        result = c.call()
        self.assertTrue(result['complete'])
        self.assertEqual(result['groups'], 230)
        archived_status = c.output/'tasks'/e.ident/'status.json'
        self.assertEqual(archived_status.read_bytes(), status_raw)
        self.assertEqual(json.loads(status_raw)['status'], 'timeout')
        self.assertEqual((c.tasks/e.ident/'status.json').read_bytes(), status_raw)
        self.assertEqual((c.output/'deadline_extensions.json').read_bytes(), index_raw)
        manifest = json.loads((c.output/'archive.json').read_text())
        archived_ledger = c.output/'deadline_extensions'/e.ledger.name
        self.assertEqual(set(ledger_raw), {str(p.relative_to(archived_ledger))
                                         for p in archived_ledger.rglob('*') if p.is_file()})
        for relative, payload in ledger_raw.items():
            archived_relative = 'deadline_extensions/'+e.ledger.name+'/'+relative
            self.assertEqual((c.output/archived_relative).read_bytes(), payload)
            entry = manifest['files'][archived_relative]
            self.assertEqual(entry['sha256'], hashlib.sha256(payload).hexdigest())
            self.assertEqual(entry['bytes'], len(payload))
            self.assertEqual(entry['original_path'], str(e.ledger/relative))
        performance = json.loads((c.output/'performance.json').read_text())
        self.assertTrue(performance['complete'])
        self.assertEqual(len(performance['deadline_extensions']), 1)
        row = next(x for x in performance['group_measurements'] if x['space_group'] == 219)
        self.assertEqual(row['task_status'], 'timeout')
        self.assertEqual(row['effective_task_status'], 'done_with_audited_deadline_extension')
        self.assertEqual(row['gnu_time']['exit_status'], 0)

        # Every original location is now absent. Re-reading must use only the
        # archive's result/task/ledger bytes and its preserved provenance map.
        for original in (c.run, c.source, c.tasks, e.ledger):
            original.rename(original.with_name(original.name+'.moved'))
            self.assertFalse(original.exists())
        replay = campaign_fixture.module.collect(c.output, c.output/'tasks', allow_partial=False)
        self.assertTrue(replay['complete'])
        self.assertEqual(replay['expected_groups'], 230)
        self.assertEqual(replay['totals'], performance['totals'])
        self.assertEqual(replay['observer'], performance['observer'])
        self.assertEqual(replay['deadline_extensions'][0]['ledger'], str(archived_ledger))
        self.assertEqual(replay['deadline_extensions'][0]['original_worker_status'], 'timeout')
        self.assertTrue(all(c.output in Path(p).parents for p in replay['evidence_sha256']))
        self.assertEqual(archived_status.read_bytes(), status_raw)

    def test_timeout_without_index_is_refused_before_destination_creation(self):
        c, e = self.campaign, self.extension
        (c.run/'deadline_extensions.json').unlink()
        original_status = (c.tasks/e.ident/'status.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'incomplete campaign'):
            c.call()
        self.assertFalse(c.output.exists())
        self.assertFalse(c.output.parent.exists())
        self.assertEqual((c.tasks/e.ident/'status.json').read_bytes(), original_status)


if __name__ == '__main__':
    unittest.main()
