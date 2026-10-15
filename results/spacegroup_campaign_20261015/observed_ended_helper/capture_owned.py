"""Read-only live ownership capture; never signals or starts campaign processes."""
import base64, datetime, hashlib, json, os, socket, sys, types
from pathlib import Path

def capture(config):
    raw=base64.b64decode(config['helperBase64'])
    assert hashlib.sha256(raw).hexdigest()==config['helperSHA256']
    m=types.ModuleType('captured_readonly_stopper');exec(compile(raw,'<verified-readonly-stopper>','exec'),m.__dict__)
    root=Path(config['root']);snapshot=Path(config['snapshot']);source_raw=(root/'source.json').read_bytes();selection_raw=(root/'selection.json').read_bytes()
    source=json.loads(source_raw);selection=json.loads(selection_raw)
    assert source['sha256']==config['sourceSHA256'] and hashlib.sha256(selection_raw).hexdigest()==config['selectionSHA256']
    node=socket.gethostname();assert node.split('.')[0]==config['node']
    runner=m.process(config['runnerPID'])
    assert runner and runner['uid']==os.getuid() and str(root) in runner['argv'] and str(snapshot/'scripts/classify.py') in runner['argv']
    verified=m.verify_source_runtime(root,snapshot,source)
    rows=m.scan_owned(os.getuid());captured,gaps,batches=m.validate_tree(rows,runner,root,source,selection)
    # Record matches outside the tree too. This does not classify them as owned
    # or signal them; a future absence check must conservatively exclude any.
    matching=[r for r in rows.values() if any(str(root) in a or str(snapshot) in a for a in r['argv'])]
    names=['source.json','selection.json','summary.json','formula_runtime.json','runtime_plan.json','runtime.json']
    paths=[root/name for name in names]
    paths += [root/c/name for c in selection for name in ['input.json','run.json','result.json','native.json','driver.g','stdout.log','stderr.log']]
    before={str(p.relative_to(root)):m.sha(p) for p in paths if p.is_file()}
    runs={c:json.loads((root/c/'run.json').read_bytes()) for c in selection if (root/c/'run.json').is_file()}
    after={str(p.relative_to(root)):m.sha(p) for p in paths if p.is_file()}
    assert (root/'source.json').read_bytes()==source_raw and (root/'selection.json').read_bytes()==selection_raw
    return dict(schema='u1-live-owned-capture-v1',capturedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),host=node,uid=os.getuid(),
                originalCampaignRoot=str(root),sourceSnapshotPath=str(snapshot),source=source,sourceSHA256=source['sha256'],selection=selection,
                sourceArtifactSHA256=hashlib.sha256(source_raw).hexdigest(),selectionSHA256=hashlib.sha256(selection_raw).hexdigest(),
                helperSHA256=config['helperSHA256'],runner=runner,processes=list(captured.values()),gaps=gaps,batches=batches,
                sourceOrCampaignMatchingProcesses=matching,artifactsSHA256=after,artifactsStableDuringCapture=before==after,runs=runs,
                noSignalsOrLaunches=True,processPreflightPassed=True,**verified)
if __name__=='__main__':print(json.dumps(capture(json.loads(sys.argv[1])),sort_keys=True))
