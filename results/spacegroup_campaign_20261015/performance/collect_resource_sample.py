"""Read-only n02 smoke-process sampling through existing persistent SSH masters."""
import json,shlex,subprocess
from pathlib import Path
node_code=r'''import os,json,time,datetime
from pathlib import Path
allp={}; hz=os.sysconf('SC_CLK_TCK'); uptime=float(Path('/proc/uptime').read_text().split()[0])
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace'); stat=(p/'stat').read_text().split(); status=dict(line.split(':',1) for line in (p/'status').read_text().splitlines() if ':' in line)
  allp[int(p.name)]={'pid':int(p.name),'ppid':int(stat[3]),'cpuSeconds':(int(stat[13])+int(stat[14]))/hz,'elapsedSeconds':round(uptime-int(stat[21])/hz,2),'rss':status.get('VmRSS','').strip(),'peakRSS':status.get('VmHWM','').strip(),'command':cmd}
 except (OSError,ValueError):continue
wanted={pid for pid,p in allp.items() if any(run in p['command'] for run in ['/sgfull-20261015-c-smoke/','/sgfull-20261015-d-smoke/']) and 'driver.g' in p['command'] and 'python3 -c' not in p['command']}
for _ in range(3):wanted.update(pid for pid,p in allp.items() if p['ppid'] in wanted)
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'host':os.uname().nodename,'loadavg':Path('/proc/loadavg').read_text().strip(),'processes':[allp[p] for p in sorted(wanted)]},indent=2))
'''
node_command='python3 -c '+shlex.quote('exec(bytes.fromhex("'+node_code.encode().hex()+'").decode())')
args=['ssh','-n','-o','BatchMode=yes','-o','ControlMaster=auto','-o','ControlPersist=43200','-o','ControlPath=/home/user/xyren/.ssh/cm-%r@%h:%p','n02',node_command]
remote=' '.join(shlex.quote(s) for s in args)+'\n'
raw=subprocess.run(['ssh','cuhk-cluster3','bash -s'],input=remote,text=True,capture_output=True,check=True).stdout
row=json.loads(raw)
with (Path(__file__).resolve().parent / 'cluster_cd_resources.jsonl').open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n')
print(json.dumps(row,indent=2))
