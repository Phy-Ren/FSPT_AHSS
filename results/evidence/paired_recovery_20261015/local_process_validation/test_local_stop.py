#!/usr/bin/env python3
"""Real LOCAL process-only validation. Never connects to a cluster."""
import ctypes
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time

BASE=Path(__file__).resolve().parent
REPO=Path('/home/xingyu/FSPT_AHSS_insulator')
HELPER=Path('/tmp/stop_owned_u1_campaign.py')
FIXTURE=REPO/'results/spacegroup_campaign_20261015/performance/cluster_d'
CASES=['spacegroup_019_spin_half','spacegroup_019_spinless']

def write(p,v):
    p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(p): return {str(q.relative_to(p)):sha(q) for q in sorted(p.rglob('*')) if q.is_file()}
def module(name,p):
    spec=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
stop=module('stop_owned',HELPER)
# Reap only our synthetic orphan descendants, rather than leave local zombies.
ctypes.CDLL(None).prctl(36,1,0,0,0)
work=Path(tempfile.mkdtemp(prefix='run-',dir=BASE))
snapshot=work/'snapshot';(snapshot/'scripts').mkdir(parents=True)
root=work/'campaign';root.mkdir()
ready=work/'ready.json'
(snapshot/'scripts/classify.py').write_text('''import argparse,os,subprocess,sys,time\nfrom pathlib import Path\np=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--ready');a=p.parse_args()\nsnapshot=Path(__file__).resolve().parents[1]\nenv=dict(os.environ,FAKE_READY=a.ready)\nchild=subprocess.Popen([sys.executable,str(snapshot/'scripts/fake_gap.py'),str(Path(a.output)/'spacegroup_019_spin_half/driver.g')],env=env,start_new_session=True)\nwhile True: time.sleep(1)\n''')
(snapshot/'scripts/fake_gap.py').write_text('''import json,os,signal,subprocess,sys,time\nfrom pathlib import Path\nworker=subprocess.Popen([sys.executable,'-c','import time; time.sleep(1000)'])\ndef end(sig,frame):\n    try: worker.terminate()\n    except ProcessLookupError: pass\n    worker.wait(timeout=2)\n    raise SystemExit(0)\nsignal.signal(signal.SIGTERM,end)\nPath(os.environ['FAKE_READY']).write_text(json.dumps({'gap':os.getpid(),'worker':worker.pid,'runner':os.getppid()}))\nwhile True: time.sleep(1)\n''')
source={'files':manifest(snapshot)}
source['sha256']=hashlib.sha256(json.dumps(source['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
write(root/'source.json',source);write(root/'selection.json',CASES)
command=[sys.executable,str(snapshot/'scripts/fake_gap.py'),str(root/CASES[0]/'driver.g')]
marker='CloseStream(output);;\nPrint("U1_PAIR_CASE_DONE ",U1_INPUT.id,"\\n");;'
driver='U1_ROOT:='+json.dumps(str(snapshot))+';;\n'
for case in CASES:
    driver+='U1_INPUT:=rec(id:='+json.dumps(case)+');;\noutput:=OutputTextFile('+json.dumps(str(root/case/'native.json'))+',false);;\n'+marker+'\n'
started=datetime.now(timezone.utc).isoformat()
for case in CASES:
    d=root/case;d.mkdir()
    shutil.copyfile(FIXTURE/case/'input.json',d/'input.json')
    (d/'driver.g').write_text(driver)
    run=dict(id=case,status='running',pairedSpins=True,batchCaseIDs=CASES,command=command,
             sourceSHA256=source['sha256'],inputSHA256=sha(d/'input.json'),host=socket.gethostname(),startedUTC=started)
    write(d/'run.json',run)
shutil.copyfile(FIXTURE/CASES[0]/'native.json',root/CASES[0]/'native.json')
(root/CASES[0]/'stdout.log').write_text('U1_PAIR_CASE_DONE '+CASES[0]+'\n')
(root/CASES[0]/'stderr.log').write_text('')
wrapper=work/'invoke_helper.py'
wrapper.write_text('''import importlib.util,json,os,signal,sys\nfrom pathlib import Path\nhelper,trace,mode,target=sys.argv[1:5];sys.argv=[helper]+sys.argv[5:]\nspec=importlib.util.spec_from_file_location('owned_stop',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)\nfor name in ('kill','killpg'):\n    original=getattr(m.os,name)\n    def wrapped(pid,sig,original=original,name=name):\n        with open(trace,'a') as out: out.write(json.dumps({'call':name,'pid':pid,'signal':int(sig)})+'\\n')\n        return original(pid,sig)\n    setattr(m.os,name,wrapped)\nif mode=='missing_argv':\n    original=m.scan_owned\n    def scan(uid):\n        rows=original(uid)\n        if int(target) in rows: rows[int(target)]['argv']=[]\n        return rows\n    m.scan_owned=scan\nif mode=='after_freeze_failure':\n    original=m.validate_tree\n    calls=[0]\n    def validate(*a,**k):\n        calls[0]+=1\n        if calls[0]>1: raise RuntimeError('Synthetic post-freeze validation failure')\n        return original(*a,**k)\n    m.validate_tree=validate\nm.main()\n''')
sentinel=subprocess.Popen([sys.executable,'-c','import time; time.sleep(1000)'],start_new_session=True)
runner=subprocess.Popen([sys.executable,str(snapshot/'scripts/classify.py'),'--output',str(root),'--ready',str(ready)],start_new_session=True)
identities={};results=[]
def active(pid):
    p=stop.process(pid);return p is not None and p['state'] not in ('Z','T','t')
def all_live():
    assert all(active(pid) for pid in identities), {pid:stop.process(pid) for pid in identities}
    assert active(sentinel.pid)
def invoke(name,mode='normal',runner_pid=None):
    trace=work/(name+'.signals.jsonl');trace.write_text('')
    out=work/name
    cmd=[sys.executable,str(wrapper),str(HELPER),str(trace),mode,str(identities.get('worker',0)),
         '--root',str(root),'--snapshot',str(snapshot),'--runner-pid',str(runner_pid or runner.pid),
         '--output',str(out),'--replacement','synthetic-local-validation-only']
    # The worker key is stored separately below; wrapper gets its real PID.
    cmd[5]=str(ids['worker'])
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=60)
    (work/(name+'.stdout.log')).write_text(p.stdout);(work/(name+'.stderr.log')).write_text(p.stderr)
    events=[json.loads(line) for line in trace.read_text().splitlines()]
    item=dict(name=name,exitCode=p.returncode,signals=events,output=str(out));results.append(item)
    return p,out,events
try:
    deadline=time.monotonic()+5
    while not ready.is_file() and time.monotonic()<deadline:time.sleep(.02)
    ids=json.loads(ready.read_text());assert ids['runner']==runner.pid
    identities={pid:stop.process(pid) for pid in ids.values()}
    write(work/'initial_processes.json',dict(owned=list(identities.values()),sentinel=stop.process(sentinel.pid)))
    before=manifest(root);write(work/'raw_before.json',before)
    p,out,events=invoke('wrong_runner',runner_pid=sentinel.pid)
    assert p.returncode!=0 and not events and not out.exists();all_live()
    runfile=root/CASES[0]/'run.json';original=runfile.read_bytes();changed=json.loads(original)
    changed['command'].insert(1,'--mismatched-argv');write(runfile,changed)
    p,out,events=invoke('mismatched_child_argv')
    assert p.returncode!=0 and not events and not out.exists();all_live();runfile.write_bytes(original)
    p,out,events=invoke('missing_child_argv',mode='missing_argv')
    assert p.returncode!=0 and not events and not out.exists();all_live()
    p,out,events=invoke('post_freeze_failure',mode='after_freeze_failure')
    assert p.returncode!=0 and events and {e['signal'] for e in events}<={int(signal.SIGSTOP),int(signal.SIGCONT)}
    assert any(e['signal']==signal.SIGCONT for e in events)
    time.sleep(.05);all_live()
    failure=json.loads((out/'validation_failure.json').read_text());assert failure['terminationSignalsSent'] is False
    assert manifest(root)==before
    # The same verifier must reject changed/missing/present library states.
    base=stop.verify_source_runtime(root,snapshot,source);assert base['formulaRuntimeVerified'] and not base['formulaRuntimeVerification']['configured']
    lib=work/'fake_vm.so';lib.write_bytes(b'synthetic library hash fixture only')
    runtime=dict(libraryPath=str(lib),libraryPresent=True,librarySHA256=sha(lib))
    write(root/'formula_runtime.json',runtime)
    assert stop.verify_source_runtime(root,snapshot,source)['formulaRuntimeVerification']['configured']
    lib.write_bytes(b'changed')
    p,out,events=invoke('changed_runtime')
    assert p.returncode!=0 and not events and not out.exists();all_live()
    lib.unlink();runtime.update(libraryPresent=False,librarySHA256=None);write(root/'formula_runtime.json',runtime)
    assert stop.verify_source_runtime(root,snapshot,source)['formulaRuntimeVerified']
    (root/'formula_runtime.json').unlink()
    sourcefile=snapshot/'scripts/fake_gap.py';originalsource=sourcefile.read_bytes();sourcefile.write_bytes(originalsource+b'\n# changed\n')
    p,out,events=invoke('changed_snapshot')
    assert p.returncode!=0 and not events and not out.exists();all_live();sourcefile.write_bytes(originalsource)
    p,out,events=invoke('confirmed_stop')
    assert p.returncode==0,p.stderr
    assert all(e['pid'] in identities for e in events),events
    assert not any(e['pid']==sentinel.pid for e in events)
    assert active(sentinel.pid)
    assert all(stop.process(pid) is None or stop.process(pid)['state']=='Z' for pid in identities)
    assert manifest(root)==before
    report=json.loads((out/'cancellation.json').read_text())
    assert report['allOwnedProcessesStopped'] and report['sourceSnapshotVerified'] and report['formulaRuntimeVerified']
    recover=module('recovery',REPO/'scripts/recover_paired_campaign.py')
    recover.validate_stop_report(report)
    recovered=work/'recovered_subset'
    recovery=recover.preserve_campaign(root,out/'cancellation.json',recovered)
    checked=recover.validate_recovered_case(recovered,CASES[0])
    assert manifest(root)==before
    write(work/'raw_after.json',manifest(root))
    write(work/'recovery_return.json',recovery)
    write(work/'recovered_validation.json',checked)
    summary=dict(status='PASS',localOnly=True,clusterSignalsSent=False,workdir=str(work),helperSHA256=sha(HELPER),
                 tests=results,rawCampaignUnchanged=True,unrelatedSentinelAlive=True,ownedPIDs=ids,sentinelPID=sentinel.pid,
                 sourceSnapshotSHA256=source['sha256'],recoveredCase=CASES[0],retryCase=CASES[1])
    shutil.copyfile(HELPER,work/'tested_stop_helper.py')
    write(work/'validation.json',summary);write(BASE/'latest.json',summary)
    print(json.dumps(summary,indent=2))
finally:
    # Only our explicitly captured synthetic identities may be cleaned up.
    for row in list(identities.values()):
        if row: stop.signal_one(row,signal.SIGCONT);stop.signal_one(row,signal.SIGKILL)
    for p in (runner,sentinel):
        if p.poll() is None:p.kill()
        p.wait(timeout=5)
    while True:
        try:
            pid,_=os.waitpid(-1,os.WNOHANG)
            if not pid:break
        except ChildProcessError:break
