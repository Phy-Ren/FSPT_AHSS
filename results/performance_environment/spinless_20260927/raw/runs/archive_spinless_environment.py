"""One-off archive of this campaign's allocations and resource observations."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('/home/user/xyren/AllFSPT')
OUT = ROOT/'results/performance_environment/spinless_20260927'
ADMIN = ROOT/'runs/spinless_230_v1_20260927T040004Z_pbs'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    if OUT.exists():
        raise ValueError('Preserve the existing environment archive')
    release_path = ROOT/'runs/spinless_final_release.json'
    release = json.loads(release_path.read_bytes())
    expected = {'115921.head.local','115922.head.local','115923.head.local',
                '115924.head.local','115925.head.local'}
    assert release['complete'] is True
    assert {x['pbs_job'] for x in release['releases']} == expected
    assert all(x['released'] is True for x in release['releases'])
    allocation = json.loads((ROOT/'runs/spinless_production_allocation.json').read_bytes())
    scheduler_logs = [ROOT/'runs/spinless_dev_20260927T033520Z.pbs.log'] + [
        ADMIN/('worker%d.log' % i) for i in range(2, 6)]
    scheduler_log_availability = [dict(original_path=str(p), available=p.is_file())
                                  for p in scheduler_logs]
    paths = [ROOT/'runs/spinless_production_allocation.json',
             ROOT/'runs/spinless_development_allocation.json', release_path,
             ROOT/'runs/spinless_dev_20260927T033520Z.pbs',
             ROOT/'runs/drain_spinless_workers.py',
             ROOT/'runs/finish_spinless_resources.py', Path(__file__).resolve()]
    paths += list((ROOT/'runs/spinless_230_v3').glob('resource_probes*.json'))
    paths += [p for p in scheduler_logs if p.is_file()]
    paths += [p for p in ADMIN.iterdir() if p.name.startswith('worker')
              or p.name in ('jobs.jsonl','namespace.json','resource_probe.py','resource_probe_v2.py')]
    observations = []
    for queue in allocation['queues']:
        base = ROOT/'runs'/queue
        worker = json.loads((base/'worker.json').read_bytes())
        assert worker['pbs_job'] in expected and not worker['active']
        assert not list((base/'pending').glob('*.json'))
        assert not list((base/'running').glob('*.json'))
        assert (base/'STOP').is_file()
        paths += [base/'worker.json', base/'STOP']
        for descriptor in sorted((base/'done').glob('*spinless*resource*.json')):
            task = ROOT/'runs/tasks'/descriptor.stem
            status = json.loads((task/'status.json').read_bytes())
            assert status['queue'] == queue and status['pbs_job'] == worker['pbs_job']
            assert status['status'] in ('done','failed')
            paths += [descriptor, task/'status.json', task/'stdout.log', task/'metrics.txt']
            row = dict(task_id=descriptor.stem, queue=queue, pbs_job=worker['pbs_job'],
                       status=status['status'], exit_code=status['exit_code'])
            if status['status'] == 'done':
                data = json.loads((task/'stdout.log').read_bytes())
                numerical = [x for x in data['tasks'] if x.get('space_group') is not None]
                row.update(host=data['host'], memory_kib=data['memory_kib'],
                    observed_at_epoch=data['epoch'], numerical_tasks=len(numerical),
                    process_tree_rss_kib=sum(x['rss_kib'] for x in numerical),
                    process_tree_cpu_percent=sum(x['cpu'] for x in numerical))
            observations.append(row)
    material, files = {}, {}
    for path in sorted(set(paths)):
        raw = path.read_bytes()
        target = 'raw/'+str(path.relative_to(ROOT))
        if target.endswith('/stdout.log'):
            target = target[:-len('stdout.log')]+'stdout.txt'
        material[target] = raw
        files[target] = dict(original_path=str(path), sha256=sha(raw), bytes=len(raw))
    summary = dict(schema='fspt-spinless-environment-archive-v1',
        generated_at=datetime.now(timezone.utc).isoformat(), files=files,
        probes=observations, complete_release=True,
        scheduler_log_availability=scheduler_log_availability,
        scope='Resource snapshots and allocation release evidence; not a numerical-correctness or exclusive-node benchmark.')
    material['archive.json'] = (json.dumps(summary,indent=2,sort_keys=True)+'\n').encode()
    material['README.md'] = b'''# Spinless campaign compute environment

These are exact allocation, resource-probe and release records for the five
PBS workers used by the spinless baseline, optimization controls and accepted
campaign. Both conventions' small regression controls shared the workers.
Per-campaign timings and maximum single-task RSS are recorded separately in
their own campaign archives; these observations are not exclusive-node tests.

The initial five resource probes failed because this older system's ps does
not support the requested etimes field. Their original failures are retained.
They are monitoring failures, not failed space-group computations. Subsequent
probes use /proc and are preserved with the corrected probe source.

Scheduler stdout files are included only when actually available. Availability
is listed explicitly in archive.json. Some completed PBS jobs report a failed
stdout transfer because the old compute-node SSH client rejects options in the
account's SSH configuration; the exact scheduler diagnostics remain in the
release record. Missing scheduler stdout is not reconstructed. Numerical task
stdout, exit status and timing files are written independently to shared storage
and are archived separately with the numerical campaigns.

The summary excludes the short monitoring process itself from numerical task
counts. Summed process-tree RSS can double-count shared pages and is not actual
physical memory consumption. CPU percentages average over each process's age;
they are not instantaneous samples. MemTotal is installed host RAM. Missing
MemAvailable on these older kernels is not interpreted as zero or reconstructed.

All original files have SHA-256 entries in archive.json. stdout.log is retained
byte-for-byte under the name stdout.txt. The release record binds each STOP to
its original worker, queue and exact PBS job; no other user's job is modified.
'''
    for relative, raw in material.items():
        path = OUT/relative
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(raw)
        assert sha(path.read_bytes()) == sha(raw)
    print(json.dumps(dict(output=str(OUT), files=len(material), probes=len(observations),
                          archive_sha256=sha(material['archive.json']))))

if __name__ == '__main__':
    main()
