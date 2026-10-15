import base64,concurrent.futures,hashlib,json,shlex,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD=Path('/home/xingyu/AllFSPT_reviews/spacegroup_full_catalogue_20261015/accelerated_gate')
source=(OLD/'remote_g_probe.py').read_bytes();recovery=(OLD/'preservation-helper-c26f3de/scripts/recover_paired_campaign.py').read_bytes()
(HERE/'remote_g_probe.py').write_bytes(source)
configs=json.loads((OLD/'probe_config.json').read_text())
def run(c):
 c=dict(c,plannedRecoverySourceBase64=base64.b64encode(recovery).decode(),plannedRecoveryHelperSHA256=hashlib.sha256(recovery).hexdigest())
 code="import base64,sys;sys.dont_write_bytecode=True;sys.argv=['probe',base64.b64decode(%r).decode()];exec(compile(base64.b64decode(%r),'<readonly-ordinary-probe>','exec'))"%(base64.b64encode(json.dumps(c).encode()).decode(),base64.b64encode(source).decode())
 command='/home/user/xyren/AllFSPT_insulator/runtime/bin/python3 -c '+shlex.quote(code)
 nested=['ssh','-n','-o','BatchMode=yes','-o','ControlMaster=auto','-o','ControlPersist=43200','-o','ControlPath=/home/user/xyren/.ssh/cm-%r@%h:%p',c['node'],command]
 r=subprocess.run(['ssh','-o','ControlMaster=no','-o','ProxyCommand=false','-o','BatchMode=yes','cuhk-cluster3','bash -s'],input=shlex.join(nested)+'\n',text=True,capture_output=True,timeout=90)
 p=HERE/(c['node']+'-ordinary-probe.json');p.write_text(r.stdout);p.with_suffix('.stderr.log').write_text(r.stderr)
 if r.returncode:raise RuntimeError(r.stderr)
 x=json.loads(r.stdout);assert x['processPreflight']['valid']
 assert all(q['ordinaryComplete'] and q.get('plannedHelperOrdinaryInspectionPassed') and q['nativeAvailable'] and q['nativeUnchangedAcrossRead'] for q in x['cases']),x['cases']
 print(c['node'],x['sampleUTC'],len(x['cases']),'ordinary cases verified',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:list(e.map(run,configs))
