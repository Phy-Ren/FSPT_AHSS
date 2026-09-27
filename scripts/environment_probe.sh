#!/bin/bash
set -eu
hostname
date -u
uname -a
/home/apps/anaconda3/bin/python3 -c 'import sys; print(sys.version); import numpy; print("numpy", numpy.__version__)'
/home/user/xyren/software/gap-4.13.1/gap -q -r -b <<'GAP'
Print("GAP ", GAPInfo.Version, "\n");
Print("HAP ", LoadPackage("hap"), "\n");
Print("CrystCat ", LoadPackage("crystcat"), "\n");
Print("Polycyclic ", LoadPackage("polycyclic"), "\n");
Print("JSON ", LoadPackage("json"), "\n");
Print("ENVIRONMENT_OK\n");
QUIT_GAP(0);
GAP
