#!/usr/bin/env python3
"""Run GAP and require a positive completion marker (GAP may exit 0 on errors)."""
import argparse
from pathlib import Path
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--sentinel", required=True)
ap.add_argument("file")
a = ap.parse_args()
cmd = ["/home/user/xyren/software/gap-4.13.1/gap", "-q", "-r", "-b", "-T", a.file]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
found = False
error = False
for line in proc.stdout:
    sys.stdout.write(line)
    sys.stdout.flush()
    found = found or a.sentinel in line
    error = error or line.startswith("Error,") or line.startswith("Syntax error:")
code = proc.wait()
if code or not found or error:
    print("GAP_NOT_ACCEPTED exit=%s sentinel=%s error=%s" % (code, found, error), flush=True)
    sys.exit(code or 1)
