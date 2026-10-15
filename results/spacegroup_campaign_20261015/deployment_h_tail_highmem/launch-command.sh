python3 - <<'LAUNCH_HIGHMEM'
import subprocess
p=subprocess.run(['ssh','-o','BatchMode=yes','-o','ControlMaster=no','-o','ControlPath=/home/user/xyren/.ssh/cm-%r@%h:%p','n02','bash -s'],input='export PATH=/home/user/xyren/AllFSPT_insulator/runtime/bin:$PATH\nexport LC_ALL=C LANG=C OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1\nexec /home/user/xyren/AllFSPT_insulator/runtime/bin/python3 /home/user/xyren/AllFSPT_insulator/snapshots/u1_launch_h_tail_highmem_20261015.py\n'.encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
print(p.stdout.decode());print(p.stderr.decode())
raise SystemExit(p.returncode)
LAUNCH_HIGHMEM
