import json,socket,subprocess,time
from pathlib import Path
host=socket.gethostname();info={}
for line in Path('/proc/meminfo').read_text().splitlines():
 key,val=line.split(':',1)
 if key in ('MemTotal','MemAvailable','SwapTotal','SwapFree'):info[key]=int(val.split()[0])
rows={}
for line in subprocess.check_output(['ps','-eo','pid,ppid,pcpu,rss,etimes,comm','--no-headers'],universal_newlines=True).splitlines():
 parts=line.split(None,5)
 if len(parts)==6: rows[int(parts[0])]=dict(pid=int(parts[0]),parent=int(parts[1]),cpu=float(parts[2]),rss_kib=int(parts[3]),elapsed=int(parts[4]),name=parts[5])
tasks=[]
for path in Path('runs/tasks').glob('*/status.json'):
 d=json.loads(path.read_text())
 if d.get('status')!='running' or d.get('hostname')!=host:continue
 pid=d['pid'];procs=[]
 for row in rows.values():
  current=row['pid'];seen=set()
  while current in rows and current not in seen:
   if current==pid:procs.append(row);break
   seen.add(current);current=rows[current]['parent']
 tasks.append(dict(id=d['id'],space_group=d.get('space_group'),cpu=sum(x['cpu'] for x in procs),rss_kib=sum(x['rss_kib'] for x in procs),elapsed=time.time()-d['started']))
print(json.dumps(dict(host=host,epoch=time.time(),memory_kib=info,task_count=len(tasks),tasks=sorted(tasks,key=lambda x:-x['rss_kib'])),indent=2))
