"""Read-only current G evidence and stop-helper preflight. Never call main/freeze."""
import datetime
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import socket
import sys
import types

BASE = Path('/home/user/xyren/AllFSPT_insulator')
H = BASE / 'snapshots/sgfull-20261015-h'
G = BASE / 'snapshots/sgfull-20261015-g'
sys.path.insert(0,str(H))
from scripts.recover_paired_campaign import parse, scientific_checks


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def probe(config):
    node = socket.gethostname().split('.')[0]
    assert node == config['node']
    root = Path(config['root'])
    source_raw = (root/'source.json').read_bytes()
    selection_raw = (root/'selection.json').read_bytes()
    source,selection = parse(source_raw),parse(selection_raw)
    assert source['sha256'] == config['sourceSHA256']
    assert digest(selection_raw) == config['selectionSHA256']
    helper = H/'scripts/stop_owned_campaign.py'
    assert digest(helper.read_bytes()) == config['stopHelperSHA256']
    spec=importlib.util.spec_from_file_location('readonly_stop_helper',helper)
    stopper=importlib.util.module_from_spec(spec);spec.loader.exec_module(stopper)
    verification=stopper.verify_source_runtime(root,G,source)
    planned_raw=base64.b64decode(config['plannedRecoverySourceBase64'])
    assert digest(planned_raw)==config['plannedRecoveryHelperSHA256']
    planned=types.ModuleType('readonly_planned_recovery')
    planned.__file__=str(H/'scripts/recover_paired_campaign.py')
    exec(compile(planned_raw,planned.__file__,'exec'),planned.__dict__)
    runner=stopper.process(config['runnerPID'])
    tree_status={'readOnly':True,'noSignalsSent':True}
    batches=[]
    try:
        assert runner is not None and runner['uid']==os.getuid()
        assert str(root) in runner['argv'] and str(G/'scripts/classify.py') in runner['argv']
        captured,gaps,batches=stopper.validate_tree(stopper.scan_owned(runner['uid']),runner,root,source,selection)
        tree_status.update(valid=True,runner=runner,activeGapPIDs=[r['pid'] for r in gaps],
                           batches=batches,ownedProcesses=list(captured.values()))
    except (AssertionError,KeyError,ValueError,RuntimeError,OSError) as error:
        tree_status.update(valid=False,runner=runner,error=type(error).__name__+': '+str(error))
    live_batches={case:batch for batch in batches for case in batch['caseIDs']}
    records=[]
    for case in config['cases']:
        record={'id':case,'root':str(root),'nativeAvailable':False,'ordinaryComplete':False,
                'potentialPairedRecovery':False,'currentPreservationHelperSupportsCase':False}
        try:
            folder=root/case
            raw={name:(folder/name).read_bytes() for name in ['input.json','run.json','native.json','driver.g']}
            data,run,native=(parse(raw[name]) for name in ['input.json','run.json','native.json'])
            assert data['id']==run['id']==case and case in selection
            assert raw['input.json']==(H/'insulator_catalog/generated'/(case+'.json')).read_bytes()
            assert run['inputSHA256']==digest(raw['input.json']) and run['sourceSHA256']==source['sha256']
            checks=scientific_checks(native,data)
            record.update(nativeAvailable=True,runStatus=run['status'],scientificChecks=checks,
                          hashes={name:digest(value) for name,value in raw.items()},pairedSpins=run.get('pairedSpins',False),
                          originalRun=run)
            if run.get('status')=='complete' and run.get('exitCode')==0:
                result_raw=(folder/'result.json').read_bytes();result=parse(result_raw)
                assert result['run']==run and result['input']==data and result['classification']==native
                record.update(ordinaryComplete=True,resultSHA256=digest(result_raw))
                inspected=planned._inspect_case(lambda name:(root/name).read_bytes(),
                    {'originalCampaignRoot':str(root),'sourceSnapshotPath':str(G)}, {},source,selection,case)
                assert inspected['kind']=='ordinary_complete'
                record['plannedHelperOrdinaryInspectionPassed']=True
            pair=run.get('batchCaseIDs')
            if run.get('pairedSpins') is True:
                assert isinstance(pair,list) and len(pair)==2 and case in pair and len(set(pair))==2 and set(pair)<=set(selection)
                driver=raw['driver.g'].decode()
                assert raw['driver.g']==(root/pair[0]/'driver.g').read_bytes()
                assert run['command'][-1]==str(root/pair[0]/'driver.g')
                match=re.search(r'^U1_ROOT:=("(?:[^"\\]|\\.)*");;',driver)
                assert match and json.loads(match.group(1))==str(G)
                assert driver.count('CloseStream(output);;\nPrint("U1_PAIR_CASE_DONE ",U1_INPUT.id,"\\n");;')==2
                stdout=(root/pair[0]/'stdout.log').read_bytes()
                marker=('U1_PAIR_CASE_DONE '+case).encode()
                marker_count=sum(line in (marker+b'\n',marker+b'\r\n') for line in stdout.splitlines(keepends=True))
                assert marker_count==1
                record.update(pair=pair,markerCount=marker_count,stdoutSHA256=digest(stdout),
                              currentPreservationHelperSupportsCase=record['ordinaryComplete'])
                if not record['ordinaryComplete']:
                    assert not (folder/'result.json').exists()
                    batch=live_batches[case]
                    assert batch['caseIDs']==pair and batch['host']==run['host'] and batch['launchedCommand']==run['command']
                    record.update(potentialPairedRecovery=True,currentPreservationHelperSupportsCase=True,
                                  recoveryRequiresFutureConfirmedStopReport=True,capturedGapPID=batch['gapPID'])
            else:
                record['preservationHelperIssue']='_inspect_case rejects non-paired metadata before ordinary_complete branch'
                assert record['ordinaryComplete'],'Unpaired incomplete case has no existing recovery path'
            assert (folder/'native.json').read_bytes()==raw['native.json']
            record['nativeUnchangedAcrossRead']=True
            record['plannedPreservationHelperSupportsCase']=record['ordinaryComplete'] or record['potentialPairedRecovery']
        except (AssertionError,KeyError,ValueError,RuntimeError,OSError,TypeError) as error:
            record.update(validationError=type(error).__name__+': '+str(error),nativeAvailable=False)
        records.append(record)
    assert (root/'source.json').read_bytes()==source_raw and (root/'selection.json').read_bytes()==selection_raw
    return {'schema':'u1-readonly-G-complement-evidence-v1','sampleUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'node':node,'root':str(root),'selection':selection,'selectionSHA256':digest(selection_raw),
            'source':source,'sourceRuntimeVerification':verification,'stopHelperSHA256':digest(helper.read_bytes()),
            'recoveryHelperSHA256':digest((H/'scripts/recover_paired_campaign.py').read_bytes()),
            'plannedRecoveryHelperSHA256':config['plannedRecoveryHelperSHA256'],
            'processPreflight':tree_status,'cases':records,'noSignalsOrLaunches':True}


if __name__=='__main__':
    print(json.dumps(probe(json.loads(sys.argv[1])),sort_keys=True))
