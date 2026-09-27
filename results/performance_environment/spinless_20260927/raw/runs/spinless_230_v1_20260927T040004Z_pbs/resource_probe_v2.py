import json,socket,subprocess,time
from pathlib import Path
host=socket.gethostname();info={}
for line in Path('/proc/meminfo').read_text().splitlines():
 key,val=line.split(':',1)
 if key in ('MemTotal','MemAvailable','SwapTotal','SwapFree'):info[key]=int(val.split()[0])
import os
rows={};ticks=os.sysconf('SC_CLK_TCK');page_kib=os.sysconf('SC_PAGE_SIZE')/1024;uptime=float(Path('/proc/uptime').read_text().split()[0])
for path in Path('/proc').iterdir():
 if not path.name.isdigit():continue
 try:
  line=(path/'stat').read_text();end=line.rindex(')');stat=line[end+2:].split();age=max(.01,uptime-int(stat[19])/ticks)
  rows[int(path.name)]=dict(pid=int(path.name),parent=int(stat[1]),cpu=100*(int(stat[11])+int(stat[12]))/ticks/age,rss_kib=int(stat[21])*page_kib,name=line[line.index('(')+1:end])
 except (OSError,ValueError,IndexError):pass
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
