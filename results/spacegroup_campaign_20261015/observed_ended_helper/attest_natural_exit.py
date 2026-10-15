#!/usr/bin/env python3
"""EXTERNAL PROTOTYPE: attest previously captured campaign absence; no signals.

No process is launched, frozen, resumed or terminated. This attests an observed
ended process tree, not execution success. Existing failed records are retained.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import time

EXPECTED_STOP_HELPER = '574ee600775d6daa858cb6b20f97bb60843c126669a576daa82b4723dd467871'
NAMES = ['source.json','selection.json','summary.json','formula_runtime.json','runtime_plan.json','runtime.json']
CASE_NAMES = ['input.json','run.json','result.json','native.json','driver.g','stdout.log','stderr.log']


def sha(raw): return hashlib.sha256(raw).hexdigest()
def read(path): return json.loads(path.read_bytes())
def encoded(x): return (json.dumps(x,indent=2,sort_keys=True)+'\n').encode()
def now(): return datetime.now(timezone.utc).isoformat()
def load_helper(path):
    raw=path.read_bytes()
    if sha(raw)!=EXPECTED_STOP_HELPER: raise ValueError('Unreviewed stop-helper bytes')
    spec=importlib.util.spec_from_file_location('readonly_owned_process_tools',path)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    return helper


def artifacts(root,selection):
    paths=[root/n for n in NAMES]+[root/c/n for c in selection for n in CASE_NAMES]
    out={}
    for p in paths:
        if p.is_symlink(): raise ValueError('Campaign evidence cannot be a symlink')
        if p.exists():
            if not p.is_file(): raise ValueError('Campaign evidence is not a regular file')
            out[str(p.relative_to(root))]=sha(p.read_bytes())
    return out


def attest(root,snapshot,capture_paths,output,helper,pause=0.1):
    root,snapshot,output=map(lambda p:Path(p).resolve(),[root,snapshot,output])
    if output.exists() or output==root or root in output.parents or output==snapshot or snapshot in output.parents:
        raise ValueError('Attestation requires a new directory outside campaign/source')
    if not capture_paths: raise ValueError('At least one prior exact live capture is required')
    source_raw=(root/'source.json').read_bytes();source=json.loads(source_raw)
    selection_raw=(root/'selection.json').read_bytes();selection=json.loads(selection_raw)
    if not isinstance(selection,list) or not selection or len(set(selection))!=len(selection):raise ValueError('Invalid selection')
    if any(not isinstance(c,str) or not c or Path(c).name!=c or c in ('.','..') for c in selection):raise ValueError('Unsafe case ID')
    observer=helper.process(os.getpid())
    observer_fields=('pid','uid','startTicks','argv','executablePath','executableSHA256')
    if (observer is None or observer.get('uid')!=os.getuid()
            or any(k not in observer for k in observer_fields)
            or not observer['argv'] or observer.get('host')!=socket.gethostname()):
        raise ValueError('Cannot capture the exact current attestor identity')
    initial=artifacts(root,selection)
    verification=helper.verify_source_runtime(root,snapshot,source)
    processes={};batches={};evidence={};captured_gaps=set();runner_identity=None
    for i,path in enumerate(map(Path,capture_paths)):
        raw=path.read_bytes();c=json.loads(raw)
        if (c.get('schema')!='u1-live-owned-capture-v1' or c.get('processPreflightPassed') is not True
                or c.get('noSignalsOrLaunches') is not True or c.get('helperSHA256')!=EXPECTED_STOP_HELPER
                or c.get('host')!=socket.gethostname() or c.get('uid')!=os.getuid()
                or c.get('originalCampaignRoot')!=str(root) or c.get('sourceSnapshotPath')!=str(snapshot)
                or c.get('sourceSHA256')!=source['sha256'] or c.get('sourceArtifactSHA256')!=sha(source_raw)
                or c.get('selectionSHA256')!=sha(selection_raw) or c.get('selection')!=selection
                or c.get('sourceSnapshotVerified') is not True or c.get('formulaRuntimeVerified') is not True
                or c.get('verifiedSourceSHA256')!=source['sha256']
                or c.get('formulaRuntimeVerification')!=verification['formulaRuntimeVerification']):
            raise ValueError('Prior live capture does not identify this exact owned campaign')
        stamp=datetime.fromisoformat(c['capturedUTC'])
        if stamp.tzinfo is None or stamp.utcoffset().total_seconds()!=0 or stamp>datetime.now(timezone.utc):
            raise ValueError('Invalid/future live-capture timestamp')
        runner=c['runner']
        if (str(root) not in runner.get('argv',[]) or str(snapshot/'scripts/classify.py') not in runner['argv']
                or runner.get('uid')!=os.getuid() or runner.get('host')!=socket.gethostname()):
            raise ValueError('Prior runner identity does not identify campaign/source')
        rid=(runner['pid'],runner['uid'],runner['startTicks'])
        if runner_identity is not None and runner_identity!=rid:raise ValueError('Captures describe different runners')
        runner_identity=rid
        rows={p['pid']:p for p in c['processes']}
        if len(rows)!=len(c['processes']):raise ValueError('Duplicated prior process PID')
        # Revalidate the historical tree against unchanged saved launch metadata.
        _,gaps,checked_batches=helper.validate_tree(rows,runner,root,source,selection)
        if gaps!=c['gaps'] or checked_batches!=c['batches']:raise ValueError('Prior GAP/batch evidence differs on replay')
        gap_ids={p['pid'] for p in gaps};captured_gaps.update(gap_ids)
        for p in c['processes']:
            if p['uid']!=os.getuid() or p['host']!=socket.gethostname():raise ValueError('Wrong captured process owner/host')
            if not p.get('argv') or not p.get('executablePath') or not p.get('executableSHA256'):
                if p.get('state')!='Z':raise ValueError('Incomplete active captured identity')
                continue
            p=dict(p,role='runner' if p['pid']==runner['pid'] else 'gap' if p['pid'] in gap_ids else 'formula-worker')
            if p['pid'] in processes:
                previous=processes[p['pid']]
                fields=['uid','startTicks','ppid','pgid','argv','executablePath','executableSHA256','role']
                if any(previous[k]!=p[k] for k in fields):raise ValueError('Prior PID identity/argv changed between captures')
            processes[p['pid']]=p
        for b in checked_batches:
            key=tuple(b['caseIDs'])
            if key in batches and batches[key]!=b:raise ValueError('Conflicting captured batch attempt')
            batches[key]=b
        # Dynamic completion logs/run metadata can legitimately change while the
        # original runner is alive. Already written input/driver/native/result
        # bytes and completed run metadata must remain exactly the captured ones.
        for name,h in c['artifactsSHA256'].items():
            immutable=(name in ('source.json','selection.json','formula_runtime.json')
                       or name.endswith(('/input.json','/driver.g','/native.json','/result.json'))
                       or (name.endswith('/run.json') and c['runs'][name.split('/')[0]].get('status')=='complete'))
            if immutable and initial.get(name)!=h:raise ValueError('Previously durable artifact changed: '+name)
        evidence['prior_capture_%02d.json'%i]=raw
    if runner_identity[0] not in processes:raise ValueError('Captured runner has no complete executable identity')

    def absent_scan():
        rows=helper.scan_owned(os.getuid());observed=[];remaining=[]
        current_observer=rows.get(observer['pid'])
        if (current_observer is None or current_observer.get('state')=='Z'
                or any(current_observer.get(k)!=observer[k] for k in observer_fields)):
            raise ValueError('The attestor identity changed during a process census')
        for p in processes.values():
            current=helper.process(p['pid'])
            state='absent' if not helper.same_identity(p,current) else 'zombie' if current['state']=='Z' else 'active'
            observed.append(dict(p,observedState=state))
            if state=='active':remaining.append(p['pid'])
        leftovers=[]
        for row in rows.values():
            # The CLI itself contains --root. Exclude only this exact verified
            # observer, never its parents/children or another matching command.
            if row['pid']==observer['pid']:continue
            if row['state']=='Z':continue
            scoped=any(a==str(root) or a.startswith(str(root)+'/')
                       or a in (str(snapshot/'scripts/classify.py'),str(snapshot/'scripts/formula_worker.py'))
                       for a in row['argv'])
            if scoped or row['pgid'] in captured_gaps:leftovers.append(row)
        if remaining or leftovers:
            raise ValueError('Campaign absence is not established: captured active=%r, scoped/group active=%r'
                             %(remaining,[p['pid'] for p in leftovers]))
        return dict(observedUTC=now(),processes=observed,scannedOwnedProcessCount=len(rows),
                    sameCapturedIdentitiesActive=[],scopedProcessesOrCapturedGroupsActive=[],noSignalsSent=True,
                    excludedNonCampaignObserver=current_observer,
                    observerExclusionRule='Only this exact PID/UID/startTicks/argv/executable identity, rechecked in this census')

    first=absent_scan()
    # Two independent process censuses bracket stable campaign bytes; no wait
    # for an active job is hidden inside this tool.
    time.sleep(pause)
    final=artifacts(root,selection)
    verification=helper.verify_source_runtime(root,snapshot,source)
    second=absent_scan()
    if initial!=final or artifacts(root,selection)!=final:
        raise ValueError('Campaign artifacts changed during absence observation')
    if (root/'source.json').read_bytes()!=source_raw or (root/'selection.json').read_bytes()!=selection_raw:
        raise ValueError('Source/selection changed during observation')
    for i,path in enumerate(map(Path,capture_paths)):
        if path.read_bytes()!=evidence['prior_capture_%02d.json'%i]:raise ValueError('Prior capture changed during observation')
    evidence['absence_observations.json']=encoded(dict(first=first,second=second))
    evidence['source_verification.json']=encoded(verification)
    evidence['artifact_stability.json']=encoded(dict(beforeSHA256=initial,afterSHA256=final,equal=True))
    completed_batches=[dict(b,allOwnedDescendantsStopped=True,remainingOwnedPIDs=[]) for b in batches.values()]
    report=dict(schema='u1-paired-stop-v1',originalCampaignRoot=str(root),sourceSnapshotPath=str(snapshot),
                sourceSHA256=source['sha256'],stoppedObservedUTC=second['observedUTC'],allOwnedProcessesStopped=True,
                processes=second['processes'],uncapturedExitedProcesses=[],batches=completed_batches,artifactsSHA256=final,
                terminationMode='observed-ended-without-signaling',terminationCause='not_inferred',signalsSent=False,
                executionExitStatus='not_inferred_from_process_absence',
                reason='Previously captured exact owned identities are absent or zombie; no scoped processes or captured groups remain. Original execution metadata is unchanged.',
                evidence=[dict(path=n,sha256=sha(raw)) for n,raw in evidence.items()],**verification)
    output.mkdir(parents=True,exist_ok=False)
    for name,raw in evidence.items():(output/name).write_bytes(raw)
    (output/'cancellation.json').write_bytes(encoded(report))
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',required=True,type=Path);p.add_argument('--snapshot',required=True,type=Path)
    p.add_argument('--capture',required=True,action='append',type=Path);p.add_argument('--output',required=True,type=Path)
    p.add_argument('--stop-helper',required=True,type=Path)
    a=p.parse_args();report=attest(a.root,a.snapshot,a.capture,a.output,load_helper(a.stop_helper))
    print(json.dumps(dict(report=str(a.output/'cancellation.json'),observedProcessTreeEnded=True,signalsSent=False,
                         artifactCount=len(report['artifactsSHA256'])),sort_keys=True))
if __name__=='__main__':main()
