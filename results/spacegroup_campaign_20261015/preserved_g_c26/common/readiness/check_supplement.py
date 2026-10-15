"""Supplemental read-only cleanup readiness; no signals and no final460 claim."""
import datetime,hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
GATE=Path('/home/xingyu/AllFSPT_reviews/spacegroup_full_catalogue_20261015/accelerated_gate')
CAP=Path('/home/xingyu/AllFSPT_reviews/spacegroup_full_d_monitor_20261015/g_readiness_20261015T165242Z')
spec=importlib.util.spec_from_file_location('prior_readonly_gate',GATE/'check_readiness.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_bytes())
config=read(Path('/home/xingyu/AllFSPT_reviews/g_preservation_prepared_20261015/prepared_config.json'))
expected=config['helperSnapshot']['files']
assert {str(p.relative_to(g.HELPER)):dict(sha256=sha(p),bytes=p.stat().st_size) for p in g.HELPER.rglob('*') if p.is_file()}==expected
plan=read(g.HPLAN);replacement=set(plan['candidateCases']);tail=set(plan['excludedTailCases'])
assert len(replacement)==24 and len(tail)==4 and not replacement&tail
parents=[g.validate_parent(g.parent_entry('sgfull-20261015-h-remaining-'+n,plan['assignments'][n],'Accepted H24 '+n)) for n in ('n02','n03')]
assert all(p['state']=='validated' for p in parents)
assert set(k for p in parents for k in p['cases'])==replacement
now=datetime.datetime.now(datetime.timezone.utc);nodes=[];failed={};all_required=set();active=set()
for node in ('n02','n03'):
 cp=CAP/(node+'-capture-20261015T165242Z.json');p=read(cp);op=HERE/(node+'-ordinary-probe.json');o=read(op);cfg=config['nodes'][node]
 assert p['schema']=='u1-live-owned-capture-v1' and p['noSignalsOrLaunches'] and p['processPreflightPassed'] and p['artifactsStableDuringCapture']
 assert p['helperSHA256']=='574ee600775d6daa858cb6b20f97bb60843c126669a576daa82b4723dd467871'
 assert p['sourceSHA256']==cfg['sourceSHA256']==p['verifiedSourceSHA256'] and p['sourceSnapshotVerified'] and p['formulaRuntimeVerified']
 assert p['selectionSHA256']==cfg['selectionSHA256'] and p['originalCampaignRoot']==cfg['root']
 assert p['formulaRuntimeVerification']['librarySHA256']=='0c026ca103e9ba8b674c006d6042ca23bfe526ca62b4e96b3c1b79c4d318dec2'
 owned={r['pid']:r for r in p['processes']};matches=p['sourceOrCampaignMatchingProcesses']
 assert all(r['pid'] in owned and r==owned[r['pid']] for r in matches)
 assert {r['pid'] for r in p['gaps']}=={b['gapPID'] for b in p['batches']}
 active_here=[k for b in p['batches'] for k in b['caseIDs']]
 assert len(active_here)==len(set(active_here)) and set(active_here)<=replacement and not set(active_here)&tail
 assert o['processPreflight']['valid'] and o['processPreflight']['noSignalsSent'] and o['noSignalsOrLaunches']
 assert o['processPreflight']['runner']==p['runner']
 assert o['selectionSHA256']==cfg['selectionSHA256'] and o['source']['sha256']==cfg['sourceSHA256']
 assert o['sourceRuntimeVerification']['sourceSnapshotVerified'] and o['sourceRuntimeVerification']['formulaRuntimeVerified']
 assert o['plannedRecoveryHelperSHA256']==expected['scripts/recover_paired_campaign.py']['sha256']
 required=set(cfg['requiredCases']);assert {r['id'] for r in o['cases']}==required
 assert set(p['selection'])-required <= replacement|tail
 for r in o['cases']:
  case=r['id'];assert r['ordinaryComplete'] and r['plannedHelperOrdinaryInspectionPassed'] and r['nativeAvailable'] and r['nativeUnchangedAcrossRead']
  run=r['originalRun'];assert run['status']=='complete' and type(run['exitCode']) is int and run['exitCode']==0
  for name,key in [('input.json','inputSHA256'),('native.json','nativeSHA256')]:
   assert r['hashes'][name]==cfg['requiredHashes'][case][key]==p['artifactsSHA256'][case+'/'+name]
  assert r['resultSHA256']==p['artifactsSHA256'][case+'/result.json']
  assert r['hashes']['input.json']==sha(g.REPO/'insulator_catalog/generated'/(case+'.json'))
  assert p['runs'][case]==run
 for case,run in p['runs'].items():
  if run['status']=='failed':
   assert type(run['exitCode']) is int and run['exitCode']!=0 and case not in required
   failed[case]=dict(node=node,exitCode=run['exitCode'],runSHA256=p['artifactsSHA256'][case+'/run.json'])
 for case in set(p['selection'])&tail:
  assert case in failed and case not in active_here
 age=(now-datetime.datetime.fromisoformat(p['capturedUTC'])).total_seconds();ordinary_age=(now-datetime.datetime.fromisoformat(o['sampleUTC'])).total_seconds()
 nodes.append(dict(node=node,capture=str(cp),captureSHA256=sha(cp),captureUTC=p['capturedUTC'],ageSeconds=age,fresh=0<=age<=300,
                   ordinaryProbe=str(op),ordinaryProbeSHA256=sha(op),ordinaryProbeUTC=o['sampleUTC'],ordinaryProbeAgeSeconds=ordinary_age,
                   ordinaryProbeFresh=0<=ordinary_age<=300,runner=p['runner'],requiredOrdinaryCount=len(required),requiredCases=sorted(required),
                   activeBatches=p['batches'],activeCaseIDs=active_here,allActiveCasesCoveredByAcceptedH24=True,
                   originalRequiredBytesEqualPrelaunchAndFreshProbe=True,noSourceOrRootMatchesOutsideValidatedTree=True))
 all_required|=required;active.update(active_here)
assert len(all_required)==88 and tail<=set(failed) and not all_required&replacement and not all_required&tail
result=dict(schema='u1-g-active-coverage-cleanup-supplement-v1',sampleUTC=now.isoformat(),priorLedgerUnchanged=True,authorizesSignals=False,
            readyForRootStopReview=all(n['fresh'] and n['ordinaryProbeFresh'] for n in nodes),acceptedH24=True,acceptedHParents=parents,
            requiredG88OrdinaryVerified=True,originalFailedTailCases=sorted(tail),allFailedGRecords=failed,activeGCaseIDs=sorted(active),
            everyActiveGCaseCoveredByAcceptedH24=True,nodes=nodes,configSHA256=sha(Path('/home/xingyu/AllFSPT_reviews/g_preservation_prepared_20261015/prepared_config.json')),
            helperTreeSHA256=config['helperSnapshot']['treeSHA256'],scriptSHA256=sha(Path(__file__)),
            condition='Root may review redundant live G cleanup only while observations are fresh and must repeat exact live identity and active-batch coverage before stopping. Final460 still requires accepted tail4; this record does not claim them.')
out=HERE/'readiness.json';assert not out.exists();out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:result[k] for k in ('readyForRootStopReview','acceptedH24','requiredG88OrdinaryVerified','originalFailedTailCases','activeGCaseIDs','authorizesSignals')},sort_keys=True))
