import json,os,signal,subprocess,sys,time
from pathlib import Path
worker=subprocess.Popen([sys.executable,'-c','import time; time.sleep(1000)'])
def end(sig,frame):
    try: worker.terminate()
    except ProcessLookupError: pass
    worker.wait(timeout=2)
    raise SystemExit(0)
signal.signal(signal.SIGTERM,end)
Path(os.environ['FAKE_READY']).write_text(json.dumps({'gap':os.getpid(),'worker':worker.pid,'runner':os.getppid()}))
while True: time.sleep(1)
