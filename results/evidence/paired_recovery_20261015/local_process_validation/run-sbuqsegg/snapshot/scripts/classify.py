import argparse,os,subprocess,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--ready');a=p.parse_args()
snapshot=Path(__file__).resolve().parents[1]
env=dict(os.environ,FAKE_READY=a.ready)
child=subprocess.Popen([sys.executable,str(snapshot/'scripts/fake_gap.py'),str(Path(a.output)/'spacegroup_019_spin_half/driver.g')],env=env,start_new_session=True)
while True: time.sleep(1)
