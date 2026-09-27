"""Drain only empty queues in this run; retain scheduler confirmation evidence."""
import json
from pathlib import Path
import re
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path('/home/user/xyren/AllFSPT')
LEDGER = ROOT/'runs/spinless_final_release.json'
PAIRS = [('spinless_dev_20260927T033520Z','115921.head.local')]+[
    ('spinless_230_v1_20260927T040004Z_q%d'%n,'%d.head.local'%(115920+n))
    for n in range(2,6)]
SSH = ['ssh','-o','ControlMaster=no','-o',
       'ControlPath=/home/user/xyren/.ssh/cm-fspt-head',
       '-o','ProxyCommand=false','head']

def query(arguments):
    p = subprocess.run(SSH+arguments, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,universal_newlines=True,timeout=25)
    return dict(epoch=time.time(),arguments=arguments,exit_code=p.returncode,
                stdout=p.stdout,stderr=p.stderr)

def save(data):
    data['complete'] = all(x['released'] for x in data['releases'])
    data['updated_at_utc'] = datetime.now(timezone.utc).isoformat()
    tmp = LEDGER.with_suffix('.tmp')
    tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    tmp.replace(LEDGER)

def main():
    if LEDGER.exists():
        data = json.loads(LEDGER.read_bytes())
    else:
        data = dict(schema='fspt-spinless-worker-release-v1',complete=False,
            releases=[dict(queue=q,pbs_job=j,stopped=False,released=False,
                           scheduler_observations=[]) for q,j in PAIRS])
    assert [(x['queue'],x['pbs_job']) for x in data['releases']] == PAIRS
    for row in data['releases']:
        if row['released']:
            continue
        base = ROOT/'runs'/row['queue']
        worker = json.loads((base/'worker.json').read_bytes())
        assert worker['pbs_job'] == row['pbs_job']
        pending = list((base/'pending').glob('*.json'))
        running = list((base/'running').glob('*.json'))
        if not row['stopped']:
            if worker['active'] or pending or running:
                print(row['pbs_job'],'working',len(worker['active']))
                continue
            assert abs(time.time()-worker['heartbeat']) < 180
            before = query(['qstat','-f',row['pbs_job']])
            fields = dict(re.findall(r'^\s*([\w.]+)\s*=\s*(.*)$',before['stdout'],re.M))
            assert before['exit_code'] == 0 and fields.get('job_state') == 'R', before
            assert fields['exec_host'].split('/')[0].split('.')[0] == worker['hostname'].split('.')[0]
            assert not (base/'STOP').exists()
            for descriptor in (base/'done').glob('*.json'):
                status = json.loads((ROOT/'runs/tasks'/descriptor.stem/'status.json').read_bytes())
                assert status['status'] not in ('pending','running')
            # All submitters are finished. Recheck emptiness immediately before STOP.
            current = json.loads((base/'worker.json').read_bytes())
            assert current['pid'] == worker['pid'] and not current['active']
            assert not list((base/'pending').glob('*.json'))
            assert not list((base/'running').glob('*.json'))
            (base/'STOP').open('x').close()
            row.update(stopped=True,stop_epoch=time.time(),worker_before_stop=current,
                       scheduler_before_stop=before)
            save(data)
            print(row['pbs_job'],'STOP written to its empty queue')
            continue
        assert (base/'STOP').is_file() and not worker['active'] and not pending and not running
        observation = query(['qstat','-f',row['pbs_job']])
        fields = dict(re.findall(r'^\s*([\w.]+)\s*=\s*(.*)$',observation['stdout'],re.M))
        row['scheduler_observations'].append(observation)
        if observation['exit_code'] == 0 and fields.get('job_state') == 'C':
            row.update(released=True,release_evidence='exact PBS job state C',worker_after_stop=worker)
        elif observation['exit_code'] != 0:
            overview = query(['qstat'])
            assert overview['exit_code'] == 0, overview
            # qstat can truncate the server suffix in its compact display.
            # The scheduler-local numerical job identifier must also be absent.
            present = set(re.findall(r'^\s*(\d+)\.',overview['stdout'],re.M))
            assert row['pbs_job'].split('.')[0] not in present, 'failed detail lookup despite a listed job number'
            checks = row.setdefault('successful_absence_checks',[])
            checks.append(overview)
            if len(checks) >= 2 and checks[-1]['epoch']-checks[0]['epoch'] >= 15:
                row.update(released=True,release_evidence='two successful scheduler listings omit exact stopped job',
                           worker_after_stop=worker)
        save(data)
        print(row['pbs_job'],'released' if row['released'] else 'waiting for scheduler confirmation')
    save(data)
    print('complete',data['complete'])

if __name__ == '__main__':
    main()
