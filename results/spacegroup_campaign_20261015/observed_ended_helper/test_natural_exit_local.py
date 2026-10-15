#!/usr/bin/env python3
"""Bounded LOCAL natural-exit proof, with every attestation signal API trapped."""
import base64,ctypes,hashlib,importlib.util,json,os,shutil,socket,subprocess,sys,tempfile,time
from pathlib import Path
from unittest import mock
BASE=Path(__file__).resolve().parent
REPO=Path('/home/xingyu/FSPT_AHSS_insulator')
HELPER=REPO/'scripts/stop_owned_campaign.py'
PRESERVE=Path('/home/xingyu/AllFSPT_reviews/spacegroup_full_catalogue_20261015/accelerated_gate/preservation-helper-c26f3de')
sys.dont_write_bytecode=True;sys.path.insert(0,str(PRESERVE))
from scripts import recover_paired_campaign as recovery

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
att=load('attestation',BASE/'attest_natural_exit.py');capture=load('live_capture',BASE/'capture_owned.py')
stop=att.load_helper(HELPER)
def write(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hashes(p):return {str(q.relative_to(p)):sha(q) for q in sorted(p.rglob('*')) if q.is_file()}
ctypes.CDLL(None).prctl(36,1,0,0,0)
work=Path(tempfile.mkdtemp(prefix='local-natural-',dir=BASE));snapshot=work/'snapshot';(snapshot/'scripts').mkdir(parents=True)
root=work/'campaign';root.mkdir();finish=work/'allow_natural_exit';ready=work/'ready';ready.mkdir()
cases=['spacegroup_019_spin_half','spacegroup_019_spinless','spacegroup_226_spin_half']
(snapshot/'scripts/formula_worker.py').write_text('''import sys,time
from pathlib import Path
while not Path(sys.argv[1]).is_file():time.sleep(.02)
''')
(snapshot/'scripts/fake_gap.py').write_text('''import json,os,subprocess,sys,time
from pathlib import Path
snapshot=Path(__file__).resolve().parents[1];driver=Path(sys.argv[-1]);finish=os.environ['LOCAL_FINISH']
w=subprocess.Popen([sys.executable,str(snapshot/'scripts/formula_worker.py'),finish])
(Path(os.environ['LOCAL_READY'])/driver.parent.name).write_text(json.dumps({'gap':os.getpid(),'worker':w.pid,'runner':os.getppid()}))
w.wait();sys.exit(1)
''')
(snapshot/'scripts/classify.py').write_text('''import argparse,json,os,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--finish');p.add_argument('--ready');a=p.parse_args()
snapshot=Path(__file__).resolve().parents[1];root=Path(a.output)
children=[]
for case in ['spacegroup_019_spin_half','spacegroup_226_spin_half']:
 children.append(subprocess.Popen([sys.executable,str(snapshot/'scripts/fake_gap.py'),str(root/case/'driver.g')],env=dict(os.environ,LOCAL_FINISH=a.finish,LOCAL_READY=a.ready),start_new_session=True))
for child in children:child.wait()
for case in ['spacegroup_019_spin_half','spacegroup_019_spinless','spacegroup_226_spin_half']:
 d=root/case;r=json.loads((d/'run.json').read_text());r.update(status='failed',exitCode=1)
 if case!='spacegroup_226_spin_half':r['batchExitCode']=1
 if case=='spacegroup_019_spin_half':
  r.update(status='complete',exitCode=0)
  (d/'result.json').write_text(json.dumps(dict(input=json.loads((d/'input.json').read_text()),classification=json.loads((d/'native.json').read_text()),run=r),indent=2,sort_keys=True)+'\\n')
 (d/'run.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\\n')
(root/'summary.json').write_text(json.dumps({'failed':True,'exitCode':1})+'\\n')
sys.exit(1)
''')
source={'files':hashes(snapshot)};source['sha256']=hashlib.sha256(json.dumps(source['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
write(root/'source.json',source);write(root/'selection.json',cases)
fixture=REPO/'results/spacegroup_campaign_20261015/performance/cluster_d'
for i,case in enumerate(cases):
 d=root/case;d.mkdir();data=json.loads((fixture/(case if i<2 else cases[0])/'input.json').read_text());data['id']=case
 # Preserve insertion order exactly between the driver and JSON input.
 (d/'input.json').write_text(json.dumps(data,indent=2)+'\n')
 command=[sys.executable,str(snapshot/'scripts/fake_gap.py'),str(root/(cases[0] if i<2 else case)/'driver.g')]
 run=dict(id=case,status='running',command=command,host=socket.gethostname(),sourceSHA256=source['sha256'],inputSHA256=sha(d/'input.json'),startedUTC='2026-10-15T00:00:00+00:00')
 if i<2:run.update(pairedSpins=True,batchCaseIDs=cases[:2])
 write(d/'run.json',run)
 (d/'stdout.log').write_text('');(d/'stderr.log').write_text('')
 if i!=1:shutil.copyfile(fixture/cases[0]/'native.json',d/'native.json')
pair='U1_ROOT:='+json.dumps(str(snapshot))+';;\n'
for case in cases[:2]:
 data=json.loads((root/case/'input.json').read_text())
 pair+='U1_INPUT:='+stop.gap_literal(data)+';;\noutput:=OutputTextFile('+json.dumps(str(root/case/'native.json'))+',false);;\nCloseStream(output);;\nPrint("U1_PAIR_CASE_DONE ",U1_INPUT.id,"\\n");;\n'
for case in cases[:2]:(root/case/'driver.g').write_text(pair)
data=json.loads((root/cases[2]/'input.json').read_text())
(root/cases[2]/'driver.g').write_text('U1_ROOT:='+json.dumps(str(snapshot))+';;\nU1_INPUT:='+stop.gap_literal(data)+';;\noutput:=OutputTextFile('+json.dumps(str(root/cases[2]/'native.json'))+',false);;\nCloseStream(output);;\n')
(root/cases[0]/'stdout.log').write_text('U1_PAIR_CASE_DONE '+cases[0]+'\n')
worker_done=work/'sentinel_exit';sentinel=subprocess.Popen([sys.executable,str(snapshot/'scripts/formula_worker.py'),str(worker_done)])
# Initially the sentinel uses the same source path intentionally; once live
# capture is complete, use it as a scoped-leftover rejection control.
runner=subprocess.Popen([sys.executable,str(snapshot/'scripts/classify.py'),'--output',str(root),'--finish',str(finish),'--ready',str(ready)],stdout=(work/'runner.stdout.log').open('w'),stderr=(work/'runner.stderr.log').open('w'),start_new_session=True)
results=[];capture_path=work/'live_capture.json';extra=[]
trap=work/'signal_trap';trap.mkdir()
(trap/'sitecustomize.py').write_text('''import json,os
from pathlib import Path
def forbidden(pid,sig):
 with open(os.environ['SIGNAL_TRACE'],'a') as f:f.write(json.dumps({'pid':pid,'signal':int(sig)})+'\\n')
 raise AssertionError('Attestation CLI attempted a signal')
os.kill=forbidden;os.killpg=forbidden
''')
def invoke_cli(name,should_pass):
 out=work/name;trace=work/(name+'.signals.jsonl');trace.write_text('')
 command=[sys.executable,str(BASE/'attest_natural_exit.py'),'--root',str(root),'--snapshot',str(snapshot),
          '--capture',str(capture_path),'--stop-helper',str(HELPER),'--output',str(out)]
 env=dict(os.environ,PYTHONPATH=str(trap),PYTHONDONTWRITEBYTECODE='1',SIGNAL_TRACE=str(trace))
 process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env)
 stdout,stderr=process.communicate(timeout=30)
 (work/(name+'.stdout.log')).write_text(stdout);(work/(name+'.stderr.log')).write_text(stderr)
 assert trace.read_text()=='',trace.read_text()
 assert (process.returncode==0)==should_pass,(name,process.returncode,stderr)
 if should_pass:
  response=json.loads(stdout);assert response['observedProcessTreeEnded'] is True and response['signalsSent'] is False
  report=json.loads((out/'cancellation.json').read_text())
  observation=json.loads((out/'absence_observations.json').read_text())
  for scan in observation.values():
   observer=scan['excludedNonCampaignObserver']
   assert observer['pid']==process.pid and str(root) in observer['argv'] and str(BASE/'attest_natural_exit.py') in observer['argv']
 else:
  assert not out.exists();report=None
 results.append(dict(name=name,passed=True,realCLISubprocess=True,exitCode=process.returncode,signalsAttempted=0,output=str(out)))
 return report
def invoke(name,should_pass=False,capture_file=None):
 out=work/name
 with mock.patch.object(stop.os,'kill',side_effect=AssertionError('Signal forbidden')) as kill, mock.patch.object(stop.os,'killpg',side_effect=AssertionError('Group signal forbidden')) as killpg:
  try:r=att.attest(root,snapshot,[capture_file or capture_path],out,stop,pause=.02)
  except (ValueError,RuntimeError) as e:
   if should_pass:raise
   assert not out.exists();r={'rejected':True,'reason':str(e)}
  else:
   assert should_pass,'Unexpected success: '+name
  kill.assert_not_called();killpg.assert_not_called()
 results.append(dict(name=name,signalsAttempted=0,passed=True,output=str(out),**({'rejection':r['reason']} if not should_pass else {})))
 return r
try:
 deadline=time.monotonic()+5
 while len(list(ready.iterdir()))<2 and time.monotonic()<deadline:time.sleep(.02)
 assert len(list(ready.iterdir()))==2
 config=dict(root=str(root),snapshot=str(snapshot),runnerPID=runner.pid,node=socket.gethostname().split('.')[0],sourceSHA256=source['sha256'],selectionSHA256=sha(root/'selection.json'),helperBase64=base64.b64encode(HELPER.read_bytes()).decode(),helperSHA256=sha(HELPER))
 c=capture.capture(config);write(capture_path,c)
 invoke('live_runner_rejected')
 invoke_cli('real_cli_live_runner_rejected',False)
 # This changes only a test-owned synchronization file, never a campaign file.
 finish.write_text('allow synthetic processes to end normally\n');assert runner.wait(timeout=5)==1
 invoke('scoped_orphan_worker_rejected')
 invoke_cli('real_cli_scoped_child_rejected',False)
 worker_done.write_text('allow synthetic sentinel to exit\n');assert sentinel.wait(timeout=5)==0
 ended=hashes(root)
 for name,path,change in [('source_changed',snapshot/'scripts/fake_gap.py',lambda b:b+b'\n# changed\n'),
                          ('durable_input_changed',root/cases[0]/'input.json',lambda b:b+b' '),
                          ('durable_native_changed',root/cases[0]/'native.json',lambda b:b+b' ')]:
  raw=path.read_bytes();path.write_bytes(change(raw))
  try:invoke(name)
  finally:path.write_bytes(raw)
 bad=dict(c,uid=c['uid']+1);badpath=work/'wrong_owner_capture.json';write(badpath,bad);invoke('wrong_prior_owner_rejected',capture_file=badpath)
 runtime=root/'formula_runtime.json';write(runtime,dict(libraryPath=str(work/'absent_vm.so'),libraryPresent=False,librarySHA256=None))
 try:invoke('new_runtime_manifest_rejected')
 finally:runtime.unlink()
 # Mock a late same-source process discovered only by the second census.
 original_scan=stop.scan_owned;calls=[0]
 def changed_observer(uid):
  rows=original_scan(uid);rows[os.getpid()]['argv']=rows[os.getpid()]['argv']+['--changed']
  return rows
 with mock.patch.object(stop,'scan_owned',side_effect=changed_observer):invoke('observer_argv_change_rejected')
 def late(uid):
  rows=original_scan(uid);calls[0]+=1
  if calls[0]>=2:
   rows[987654]=dict(c['runner'],pid=987654,pgid=987654,argv=[sys.executable,str(snapshot/'scripts/formula_worker.py')],state='R')
  return rows
 with mock.patch.object(stop,'scan_owned',side_effect=late):invoke('late_worker_second_scan_rejected')
 original_stdout=(root/cases[0]/'stdout.log').read_bytes();calls[0]=0
 def mutate_during_scan(uid):
  rows=original_scan(uid);calls[0]+=1
  if calls[0]>=2:(root/cases[0]/'stdout.log').write_bytes(original_stdout+b'late write\n')
  return rows
 try:
  with mock.patch.object(stop,'scan_owned',side_effect=mutate_during_scan):invoke('post_exit_artifact_race_rejected')
 finally:(root/cases[0]/'stdout.log').write_bytes(original_stdout)
 report=invoke('attested_natural_exit',should_pass=True)
 assert report['signalsSent'] is False and report['terminationCause']=='not_inferred'
 recovery.validate_stop_report(report)
 report=invoke_cli('real_cli_observed_ended',True)
 recovery.validate_stop_report(report)
 out=work/'preserved';ledger=recovery.preserve_campaign(root,work/'real_cli_observed_ended/cancellation.json',out)
 assert ledger['ordinaryCompleteCases']==[cases[0]] and ledger['recoveredCases']==[]
 assert set(ledger['retryCases'])==set(cases[1:])
 recovery.validate_preserved_ordinary_case(out,cases[0])
 original=json.loads((root/cases[0]/'run.json').read_text());preserved=json.loads((out/cases[0]/'run.json').read_text())
 assert original==preserved and preserved['exitCode']==0 and preserved['batchExitCode']==1
 assert hashes(root)==ended
 result=dict(status='PASS',localOnly=True,clusterContact=False,productionSignals=False,testChecks=results,helperSHA256=sha(HELPER),attestorSHA256=sha(BASE/'attest_natural_exit.py'),captureSHA256=sha(capture_path),
             preservedOriginalPerCaseStatus=True,actualFailedBatchExitRetained=True,incompleteSingletonNotRecovered=True,originalArtifactsUnchanged=True,preservationHelperSHA256=sha(PRESERVE/'scripts/recover_paired_campaign.py'),workdir=str(work))
 write(work/'result.json',result);write(BASE/'local_test_result.json',result);print(json.dumps(result,indent=2))
finally:
 # All synthetic jobs normally end through the file protocol; no kill fallback.
 finish.write_text('cleanup natural exit\n');worker_done.write_text('cleanup natural exit\n')
 runner.wait(timeout=5);sentinel.wait(timeout=5)
 while True:
  try:
   pid,_=os.waitpid(-1,os.WNOHANG)
   if not pid:break
  except ChildProcessError:break
