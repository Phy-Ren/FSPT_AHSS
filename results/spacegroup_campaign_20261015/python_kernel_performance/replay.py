import json,sys,time,hashlib
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from insulator.worker import _evaluate
requests=[json.loads(x) for x in Path(sys.argv[2]).read_text().splitlines()]
if len(sys.argv)>4: requests=requests[:int(sys.argv[4])]
results=[]
start=time.process_time(); wall=time.perf_counter()
for request in requests:
 try: results.append({"ok":True,"result":_evaluate(request)})
 except Exception as e: results.append({"ok":False,"error":type(e).__name__+": "+str(e)})
report={"requests":len(requests),"cpu_seconds":time.process_time()-start,"wall_seconds":time.perf_counter()-wall,"results":results}
Path(sys.argv[3]).write_text(json.dumps(report,sort_keys=True))
print({k:v for k,v in report.items() if k!="results"})
print("digest",hashlib.sha256(json.dumps(results,sort_keys=True).encode()).hexdigest())
