#!/usr/bin/env python3
"""Read only hardware and allocation metadata for this worker's own PBS job."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import platform
import socket
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('--expected-host', required=True)
parser.add_argument('--expected-job', required=True)
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
started = time.monotonic()
host = socket.gethostname()
job = os.environ.get('PBS_JOBID')
if host != args.expected_host or job != args.expected_job:
    raise SystemExit('worker host/PBS job differs from the authorized allocation')
nodefile_name = os.environ.get('PBS_NODEFILE')
if not nodefile_name:
    raise SystemExit('own PBS_NODEFILE is missing')
nodefile = Path(nodefile_name).read_bytes()
allocated = [line.strip() for line in nodefile.decode().splitlines() if line.strip()]
if not allocated or any(name.split('.')[0] != host.split('.')[0] for name in allocated):
    raise SystemExit('PBS nodefile does not describe the expected single-node allocation')
models = set()
with open('/proc/cpuinfo') as stream:
    for line in stream:
        key, separator, value = line.partition(':')
        if separator and key.strip() == 'model name':
            models.add(value.strip())
mem_total_kib = None
with open('/proc/meminfo') as stream:
    for line in stream:
        if line.startswith('MemTotal:'):
            fields = line.split()
            if len(fields) != 3 or fields[2] != 'kB':
                raise SystemExit('unrecognized MemTotal units')
            mem_total_kib = int(fields[1])
            break
if not models or mem_total_kib is None:
    raise SystemExit('required CPU or memory metadata missing')
result = dict(hostname=host, pbs_job=job, recorded_node_time=time.time(),
    cpu_model_names=sorted(models), host_logical_cpu_count=os.cpu_count(),
    own_process_affinity_cpu_count=len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else None,
    host_memtotal_kib=mem_total_kib, host_memtotal_gib=mem_total_kib/1024**2,
    allocation=dict(pbs_nodefile_path=nodefile_name, pbs_nodefile_sha256=hashlib.sha256(nodefile).hexdigest(),
                    nodefile_slots=len(allocated), nodefile_hosts=dict(Counter(allocated))),
    python=dict(executable=sys.executable, version=sys.version),
    uname=dict(platform.uname()._asdict()),
    probe_elapsed_seconds=time.monotonic()-started,
    scope=dict(memtotal='Host total memory from /proc/meminfo; not task RSS or an allocation memory limit.',
               logical_cpus='Host logical CPU count; not the number of allocated PBS slots.',
               slots='Line count of this PBS job\'s own PBS_NODEFILE; allocation evidence.',
               process_inspection='No other process was inspected; only own CPU affinity was read.',
               environment='Only PBS_JOBID and PBS_NODEFILE were read; no full environment was collected.',
               gap_executed=False))
if args.output.exists():
    raise SystemExit('probe output already exists')
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps(result, sort_keys=True))
