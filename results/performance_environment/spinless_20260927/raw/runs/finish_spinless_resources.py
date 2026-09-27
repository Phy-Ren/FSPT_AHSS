"""Wait for our existing queues to empty, then archive release evidence."""
import json
from pathlib import Path
import subprocess
import sys
import time
ROOT = Path('/home/user/xyren/AllFSPT')
OUT = ROOT/'runs/spinless_resource_finalization.json'
try:
    while True:
        subprocess.run([sys.executable,str(ROOT/'runs/drain_spinless_workers.py')],check=True)
        data=json.loads((ROOT/'runs/spinless_final_release.json').read_bytes())
        if data['complete']:
            break
        time.sleep(60)
    result=subprocess.check_output([sys.executable,str(ROOT/'runs/archive_spinless_environment.py')],universal_newlines=True)
    value=dict(complete=True,finished_epoch=time.time(),archive=json.loads(result))
except BaseException as exc:
    value=dict(complete=False,finished_epoch=time.time(),error=repr(exc))
    raise
finally:
    OUT.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
