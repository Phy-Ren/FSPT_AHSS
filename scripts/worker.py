#!/usr/bin/env python3
"""PBS-resident task runner. All numerical jobs execute inside its allocation."""
import argparse
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import time


def atomic_json(path, value):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    tmp.replace(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--queue", default="queue", help="Queue namespace under runs/")
    args = ap.parse_args()
    if not 1 <= args.workers <= 28:
        ap.error("--workers must be in 1..28 for the 28-core PBS templates")
    root = Path(args.root).resolve()
    if not args.queue or Path(args.queue).name != args.queue:
        ap.error("queue must be a single directory name")
    queue = root / "runs" / args.queue
    for name in ("pending", "running", "done"):
        (queue / name).mkdir(parents=True, exist_ok=True)
    active = {}
    stopping = [False]
    def stop(signum, frame):
        stopping[0] = True
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    started = time.time()
    while not stopping[0]:
        slots = args.workers
        config = queue / "config.json"
        if config.exists():
            try:
                slots = min(28, max(1, int(json.loads(config.read_text())["workers"])))
            except (ValueError, KeyError, OSError, TypeError):
                pass
        for path in sorted((queue / "pending").glob("*.json")):
            if len(active) >= slots:
                break
            running = queue / "running" / path.name
            try:
                path.rename(running)
            except FileNotFoundError:
                continue
            task = json.loads(running.read_text())
            ident = path.stem
            outdir = root / "runs" / "tasks" / ident
            outdir.mkdir(parents=True, exist_ok=True)
            log = (outdir / "stdout.log").open("wb")
            env = os.environ.copy()
            env.update({"OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "LC_ALL": "C", "PYTHONUNBUFFERED": "1"})
            env.update(task.get("env", {}))
            command = ["/usr/bin/time", "-v", "-o", str(outdir / "metrics.txt")] + task["command"]
            now = time.time()
            try:
                proc = subprocess.Popen(command, cwd=task.get("cwd", str(root)), env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
                status = dict(task, id=ident, queue=args.queue, hostname=socket.gethostname(), pbs_job=os.environ.get("PBS_JOBID"), pid=proc.pid, started=now, status="running")
                atomic_json(outdir / "status.json", status)
                active[ident] = (proc, log, running, outdir, status)
            except Exception as exc:
                log.close()
                atomic_json(outdir / "status.json", dict(task, id=ident, status="launch_error", reason=str(exc)))
                running.rename(queue / "done" / running.name)
        for ident, entry in list(active.items()):
            proc, log, running, outdir, status = entry
            elapsed = time.time() - status["started"]
            timed_out = elapsed > status.get("timeout_s", 3600)
            if proc.poll() is None and timed_out:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
            if proc.poll() is not None:
                log.close()
                status.update(status="timeout" if timed_out else ("done" if proc.returncode == 0 else "failed"), exit_code=proc.returncode, elapsed_s=elapsed, finished=time.time())
                atomic_json(outdir / "status.json", status)
                running.rename(queue / "done" / running.name)
                del active[ident]
        atomic_json(queue / "worker.json", dict(hostname=socket.gethostname(), pbs_job=os.environ.get("PBS_JOBID"), pid=os.getpid(), started=started, heartbeat=time.time(), slots=slots, active=list(active)))
        if (queue / "STOP").exists() and not active:
            break
        time.sleep(1)
    for proc, log, running, outdir, status in active.values():
        if proc.poll() is None:
            os.killpg(proc.pid, signal.SIGTERM)
        status.update(status="worker_stopped", finished=time.time())
        atomic_json(outdir / "status.json", status)
        log.close()


if __name__ == "__main__":
    main()
