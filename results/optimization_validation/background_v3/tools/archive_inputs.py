"""One-time byte-preserving packing of independently checked control campaigns.
The two main 230-group campaigns must be complete. An SG219 development pilot
may retain its original timeout, explicitly separated from completed results.
No numerical source/result or task status is modified.
"""
import argparse, collections, datetime, hashlib, json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
H=lambda raw:hashlib.sha256(raw).hexdigest()
SPECS=[('v1_initial_controls','spinless_full_controls_v1', [1,2,3,6,7,16,19,75,81,84,103,146]),
 ('v1_baseline','spinless_230_v1_20260927T040004Z',list(range(1,231))),
 ('v2_cup0_pilot','spinless_cup0_controls_v2',[1,2,3,6,7,16,19,75,81,84,103,146,219]),
 ('v3_integrated_pilot','spinless_specialized_controls_v3',[3,6,84,86,87,88,219]),
 ('half_regression_v3','half_background_regression_v3',[1,2,6,19,81,103,146]),
 ('half_diagnostic_completion_v3','half_diagnostic_completion_v3',[84,104])]

def completed_attempt(label,task,status):
 assert status['id']==task['id'] and status['command']==task['command']
 assert status['space_group']==task['space_group'] and status['timeout_s']==task['timeout_s']
 if status['status']=='done':
  assert status['exit_code']==0
  return True
 assert label in ('v2_cup0_pilot','v3_integrated_pilot') and task['space_group']==219
 assert status['status']=='timeout' and type(status['exit_code']) is int
 assert status['elapsed_s']>=status['timeout_s']
 return False

def pack(output):
 if not __debug__:raise ValueError('Run without Python -O')
 if output.exists() or output.is_symlink():raise ValueError('preserve existing destination')
 # This is a control archive, not a new production acceptance decision.
 accepted=ROOT/'results/space_groups_spinless'
 if not (accepted/'archive.json').is_file():raise ValueError('accepted complete v3 archive is not available')
 archive=json.loads((accepted/'archive.json').read_bytes())
 assert archive['groups']==list(range(1,231))
 for rel,entry in archive['files'].items():
  assert H((accepted/rel).read_bytes())==entry['sha256'],('accepted archive payload hash',rel)
 cache=json.loads((ROOT/'runs/background_validation_monitor/state.json').read_bytes())
 materials={};entries={};runs={};sources={}
 def add(path,dst):
  raw=path.read_bytes();entry={'original_path':str(path.resolve()),'archive_path':dst,'sha256':H(raw),'bytes':len(raw)}
  if dst in materials:
   assert materials[dst]==raw
   return raw
  materials[dst]=raw;entries[dst]=entry;return raw
 for label,name,expected in SPECS:
  run=ROOT/'runs'/name
  found={int(p.stem[2:]) for p in run.glob('sg*.json') if '.raw.' not in p.name}
  assert found<=set(expected),(name,'unexpected result')
  prefix='runs/'+label+'/'
  campaign=json.loads(add(run/'campaign.json',prefix+'campaign.json'))
  assert sorted(campaign['groups'])==expected and campaign['mode']=='full'
  assert sorted(t['space_group'] for t in campaign['tasks'])==expected
  assert len({t['id'] for t in campaign['tasks']})==len(expected)
  source=ROOT/Path(campaign['source_snapshot']).relative_to('/home/user/xyren/AllFSPT')
  sourceid=campaign['source_id']; hashes={str(p.relative_to(source)):H(p.read_bytes()) for p in (source/'gap').glob('*.g')}
  assert hashes==campaign['source_sha256'] and H(json.dumps(hashes,sort_keys=True).encode())==sourceid
  for rel in sorted(hashes):add(source/rel,'sources/'+sourceid+'/'+rel)
  sources[sourceid]={'source_sha256':hashes,'archive_path':'sources/'+sourceid,'original_path':campaign['source_snapshot']}
  completed=[];attempts=[]
  for task in campaign['tasks']:
   ident=task['id'];assert Path(ident).name==ident
   root=ROOT/'runs/tasks'/ident
   st=json.loads(add(root/'status.json',prefix+'tasks/'+ident+'/status.json'))
   success=completed_attempt(label,task,st)
   attempts.append({'space_group':task['space_group'],'task_id':ident,
      'raw_status':st['status'],'raw_exit_code':st['exit_code'],'original_timeout_s':task['timeout_s'],
      'complete_success':success,'source_id':sourceid})
   if success:completed.append(task['space_group'])
   for original,stored in [('metrics.txt','metrics.txt'),('stdout.log','stdout.txt')]:
    add(root/original,prefix+'tasks/'+ident+'/'+stored)
  completed.sort();assert set(completed)<=found,(name,'successful task missing result')
  for sg in set(expected)-set(completed):
   filename='sg%d.json'%sg
   # A late or partial artifact is retained as failed-attempt evidence, never
   # exposed as a successfully completed sg*.json comparison input.
   if (run/filename).is_file():add(run/filename,prefix+'failed_attempts/'+filename)
   if (run/'classification'/filename).is_file():
    add(run/'classification'/filename,prefix+'failed_attempts/classification/'+filename)
  records=[]
  for sg in completed:
   filename='sg%d.json'%sg; raw=add(run/filename,prefix+filename);d=json.loads(raw)
   assert d['space_group']==sg and d['source_id']==sourceid and d['source_sha256']==hashes
   assert H(raw) in cache['audits'],(name,sg,'not incrementally audited')
   check=json.loads(add(run/'classification'/filename,prefix+'classification/'+filename))
   assert check['space_group']==sg and check['source_id']==sourceid
   for key in ('pip','majorana','complex_fermion','bosonic','ranks','resolution_dimensions','cpu_ms'):
    assert check[key]==d[key],(name,sg,'checkpoint',key)
   records.append({'space_group':sg,'result_sha256':H(raw),'audit':cache['audits'][H(raw)]['result']})
  if (run/'observation.json').is_file():
   add(run/'observation.json',prefix+'observation.json')
  runs[label]={'original_run':str(run.resolve()),'groups':completed,'intended_groups':expected,
     'incomplete_groups':sorted(set(expected)-set(completed)),'task_attempts':attempts,
     'source_id':sourceid,'source_archive':'sources/'+sourceid,
     'actual_audit_kinds':dict(collections.Counter(r['audit']['kind'] for r in records)),
     'per_group_audits':records,'original_export_scope':'legacy native background matrices absent' if label=='v1_initial_controls' else 'strict background or accepted half witnesses'}
  if runs[label]['incomplete_groups']:
   assert runs[label]['incomplete_groups']==[219]
   if label=='v3_integrated_pilot':
    assert sourceid==archive['source_id'] and campaign['crystalline_spin']=='spinless'
    runs[label]['separate_same_source_evidence']={
       'path':'../../space_groups_spinless/sg219.json',
       'sha256':archive['files']['sg219.json']['sha256'],
       'scope':'Formal v3 same-source full result; not a completed pilot result or a replacement of its timeout history.'}
   else:
    runs[label]['supplementary_evidence_scope']='Direct native bilinear controls and the complete v1-versus-integrated-v3 comparison support the optimization. They do not constitute a completed isolated cup0-pilot SG219 result.'
 # Preserve exact incremental mathematical audit decisions and historical tool hashes.
 add(ROOT/'runs/background_validation_monitor/state.json','incremental_audit_history.json')
 add(Path(__file__),'tools/archive_inputs.py')
 for path in entries.values():
  assert H(Path(path['original_path']).read_bytes())==path['sha256'],('changed during preparation',path['original_path'])
 manifest={'schema':'fspt-background-v3-validation-input-archive-v1','archived_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'runs':runs,'sources':sources,'files':entries,
   'accepted_v3_archive':{'path':'../../space_groups_spinless','source_id':archive['source_id'],'archive_sha256':H((accepted/'archive.json').read_bytes())},
   'scope':{'input_bytes_modified':False,'reference_answers_read':False,
      'all_expected_control_inputs_complete':all(not r['incomplete_groups'] for r in runs.values()),
      'all_declared_control_attempts_terminal':True,'main_v1_and_v3_campaigns_complete_230':True,
      'development_timeout_policy':'Only original-budget SG219 timeouts in auxiliary cup0/integrated pilots are retained; original raw statuses/exit codes/logs remain unchanged. The formal v3 result is never copied into a pilot result path.',
      'production_archive_independently_accepted':True,'all_mathematical_results_incrementally_audited_by_exact_sha256':True,
      'literal_comparison_reports':'Generated separately in comparisons/ with each metadata/export exception enumerated; input archive does not by itself assert mathematical equality.',
      'abstract_upper_certificates_are_not_actual_marked_witnesses':True,'benchmark_claim':'Control task logs are provenance; small pilots are not an independent whole-campaign benchmark.'}}
 output.parent.mkdir(parents=True,exist_ok=True);output.mkdir()
 try:
  for rel,raw in materials.items():
   target=output/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
   assert H(target.read_bytes())==entries[rel]['sha256']
  (output/'archive.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
 except BaseException:
  shutil.rmtree(output);raise
 return {'files':len(materials)+1,'bytes':sum(len(x) for x in materials.values())+(output/'archive.json').stat().st_size,
    'archive_sha256':H((output/'archive.json').read_bytes()),'output':str(output)}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 print(json.dumps(pack(a.output),sort_keys=True))
