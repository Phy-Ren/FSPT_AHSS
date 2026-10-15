set -eu
ssh -o BatchMode=yes -o ControlMaster=auto -o ControlPersist=43200 -o ControlPath=/home/user/xyren/.ssh/cm-%r@%h:%p n03 'bash -s' <<'NODE_SCRIPT'
set -eu
export PYTHONDONTWRITEBYTECODE=1 LC_ALL=C LANG=C
/home/user/xyren/AllFSPT_insulator/runtime/bin/python3 /home/user/xyren/AllFSPT_insulator/snapshots/g-preservation-70cc4c24/postprocess_g.py run --node n03 --report /home/user/xyren/AllFSPT_insulator/runs/sgfull-20261015-g-n03-stop-20261015-h24/cancellation.json
NODE_SCRIPT
