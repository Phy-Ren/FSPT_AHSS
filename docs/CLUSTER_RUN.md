# 在 cuhk-cluster3 重新运行全部 230 个空间群

每个空间群在计算节点上的**同一个 GAP 进程**中依次完成 classification、实际生成元的 stacking 和证书导出；不同空间群之间并行。不要在 head 节点直接运行 `run_group.py`。以下示例申请新的五个 PBS allocation，使用四个 `bigmem` 节点和一个 `normal` 节点，每个 worker 最多同时运行 28 个单线程任务。

本页重现已正式接受的 v09 全 230 群归档：源码为 `results/space_groups/source`，调度基准为 `results/space_groups`。统一源码 ID 为 `9c16c0714da16a1ed5dc23b7830701afc01e6d7a37ee6d243f536ee4dc9ecd96`；归档清单 SHA256 为 `60bc072c330c838a10e6a1f663eb6664e1d09e010b5081141dacf609aff33831`。全部 AW-v2 完整 witnesses 和性能证据已通过严格审查。重跑前仍需确认归档已同步到当前目录并通过下方审计；历史 `runs/` 目录、数学结果拼接基准和已释放的 worker 不替代这些文件。`--timings` 只读取既有耗时来安排任务次序，数值程序不会读取旧答案。

本地的 `cuhk-cluster3` alias 进入共享文件 login host；PBS 的 `qsub/qstat` 在内网 `head`。先复用本地已有的 cluster master 进入 login host，再复用其 `/home/user/xyren/.ssh/cm-fspt-head` socket 进入 PBS head。每一级的 `-O check` 失败就停止，恢复该已有 master 后再继续；不要循环创建新 SSH 连接，也不直接 SSH 到计算节点。

```bash
ssh -O check cuhk-cluster3
ssh -o ControlMaster=no -o ProxyCommand=false -t cuhk-cluster3 'bash --noprofile --norc'
```

下面两条在刚进入的 login host 中执行：

```bash
ssh -S /home/user/xyren/.ssh/cm-fspt-head -O check head
ssh -S /home/user/xyren/.ssh/cm-fspt-head -o ControlMaster=no -o ProxyCommand=false \
  -t head 'bash --noprofile --norc'
```

其余代码块全部在上述 **PBS head Bash** 中执行。代码和已接受的归档须已同步到 `/home/user/xyren/AllFSPT`；GAP/HAP 环境沿用仓库中的计算节点配置。

```bash
set -euo pipefail
cd /home/user/xyren/AllFSPT
command -v qsub
command -v qstat
FSPT_PY=/home/apps/anaconda3/bin/python3
export FSPT_RUN_TAG="rerun_$(date -u +%Y%m%dT%H%M%SZ)"
FSPT_RUN="runs/${FSPT_RUN_TAG}"
FSPT_ADMIN="runs/${FSPT_RUN_TAG}_pbs"

test -f results/space_groups/archive.json
test -f results/space_groups/source/gap/run_one.g
"$FSPT_PY" scripts/audit_run.py results/space_groups \
  --require-complete-witnesses \
  --require-formula-convention normalized-pip-aw-edge-transport-v2
```

生成五份新的 PBS 文件和队列目录。下面先检查所有目标路径，任一目录或符号链接已存在就拒绝；请换一个新的 `FSPT_RUN_TAG`，不要删历史目录、清 `STOP`，或复用历史 `running` 队列。输出目录 `FSPT_RUN` 此时保持不存在，稍后由 `submit_campaign.py` 创建。

```bash
"$FSPT_PY" - <<'PY'
import json, os, pathlib, re
root = pathlib.Path.cwd()
tag = os.environ['FSPT_RUN_TAG']
assert re.fullmatch(r'rerun_[0-9]{8}T[0-9]{6}Z', tag)
admin = root/'runs'/(tag+'_pbs')
queues = [tag+'_q'+str(i) for i in range(1, 6)]
targets = [root/'runs'/tag, admin] + [root/'runs'/q for q in queues]
assert all(not p.exists() and not p.is_symlink() for p in targets), 'Namespace already exists'
template = (root/'scripts/campaign_worker.pbs').read_text()
assert '#PBS -q bigmem\n' in template
assert '#PBS -l nodes=1:ppn=28:bigmem\n' in template
assert '#PBS -l walltime=12:00:00\n' in template
admin.mkdir()
for i, queue in enumerate(queues, 1):
    (root/'runs'/queue).mkdir()
    text = template.replace('#PBS -N FSPT_AHSS\n', '#PBS -N FSPT-r%d\n' % i)
    text = text.replace('#PBS -j oe\n', '#PBS -j oe\n'
        '#PBS -v AFS_QUEUE=%s,AFS_WORKERS=28\n'
        '#PBS -o %s\n' % (queue, admin/('worker%d.log' % i)))
    if i == 5:
        text = text.replace('#PBS -q bigmem\n', '#PBS -q normal\n')
        text = text.replace('#PBS -l nodes=1:ppn=28:bigmem\n',
                            '#PBS -l nodes=1:ppn=28\n')
    (admin/('worker%d.pbs' % i)).write_text(text)
(admin/'namespace.json').write_text(json.dumps(dict(tag=tag, queues=queues,
    run=str(root/'runs'/tag), root=str(root)), indent=2)+'\n')
print(admin)
PY

qstat -q
```

先查看当前资源和自己已有的 allocation，再执行下一块。此配置不表示当前有五个空闲节点。第 5 个 PBS 文件明确使用 `normal`、`nodes=1:ppn=28`，与此次实际运行的资源类型一致；其主机总内存曾测得约 125.776 GiB，**这不是 PBS 分配内存保证**。硬件读数见[归档说明](../results/performance_environment/README.md)和[原始探测记录](../results/performance_environment/summary.json)。正式 v09 的单任务峰值为 SG219 的 **16.869 GiB**，见[性能归档](../results/space_groups/performance.json)；历史 v07 基准曾测得约 18.502 GiB，应与正式结果区分。调度器按耗时排序，并不按内存做装箱，不能用一个任务的峰值推断整节点并发内存。提交前应结合现场内存资源核对 28 并发配置。

`qsub` 只传 PBS 文件名；队列名字和 worker 数写在文件的 `#PBS -v` 行中。保留每次返回的 PBS job ID；若中途失败，已有 job ID 留在文件里，不要从头重复提交。

```bash
"$FSPT_PY" - <<'PY'
import os, pathlib, subprocess
admin = pathlib.Path('runs')/(os.environ['FSPT_RUN_TAG']+'_pbs')
with (admin/'jobs.tsv').open('x') as out:
    for i in range(1, 6):
        job = subprocess.check_output(['qsub', str(admin/('worker%d.pbs' % i))],
                                      universal_newlines=True).strip()
        assert job and not any(c.isspace() for c in job), 'Unexpected qsub output: '+job
        out.write('%s_q%d\t%s\n' % (os.environ['FSPT_RUN_TAG'], i, job))
        out.flush()
        os.fsync(out.fileno())
        print(job, flush=True)
PY

while IFS=$'\t' read -r FSPT_QUEUE FSPT_JOB; do
  qstat -f "$FSPT_JOB"
done < "$FSPT_ADMIN/jobs.tsv"
```

等待五个 job 都进入 `R` 且生成各自的 `worker.json`。再做下面的只读检查：PBS job ID、实际主机、28 个 slot、空队列以及连续两次增长的 heartbeat 都必须对应本次新 allocation。这里只检查自己的五个 job。计算节点与 head 的时钟可能略有差异，因此同时检查 heartbeat 是否推进。

每个 allocation 为 12 小时；每个任务的 `27000s` 是从该任务真正启动开始的 **7.5 小时上限**。PBS 时钟从 allocation 开始就计时，等待别的节点就绪和任务内部排队都会消耗余量。本例提交门槛另预留 1 小时排队及 30 分钟清理时间，要求每个 allocation 还剩至少 9 小时；这不是对未来排队时长的保证。实际必须满足“任务等待时间 + 任务预算 + 清理时间 < allocation 剩余时间”。不足时不要提交本轮 230 任务。

```bash
"$FSPT_PY" - <<'PY'
import json, os, pathlib, re, subprocess, time
root = pathlib.Path.cwd()
admin = root/'runs'/(os.environ['FSPT_RUN_TAG']+'_pbs')
pairs = [line.split() for line in (admin/'jobs.tsv').read_text().splitlines()]
assert len(pairs) == 5 and len({j for q,j in pairs}) == 5
first = {q:json.loads((root/'runs'/q/'worker.json').read_text()) for q,j in pairs}
time.sleep(2)
def seconds(value):
    h, m, s = map(int, value.split(':'))
    return h*3600+m*60+s
for queue, job in pairs:
    base = root/'runs'/queue
    w = json.loads((base/'worker.json').read_text())
    assert w['pbs_job'] == job and w['slots'] == 28 and not w['active']
    assert w['pid'] == first[queue]['pid'] and w['heartbeat'] > first[queue]['heartbeat']
    assert abs(time.time()-w['heartbeat']) < 120
    assert not (base/'STOP').exists()
    for state in ('pending', 'running', 'done'):
        assert not list((base/state).glob('*.json')), (queue, state)
    text = subprocess.check_output(['qstat', '-f', job], universal_newlines=True)
    fields = dict(re.findall(r'^\s*([\w.]+)\s*=\s*(.*)$', text, re.M))
    assert fields['job_state'] == 'R'
    hosts = {item.split('/')[0].split('.')[0] for item in fields['exec_host'].split('+')}
    assert w['hostname'].split('.')[0] in hosts
    assert 'ppn=28' in fields['Resource_List.nodes']
    remaining = seconds(fields['Resource_List.walltime'])-seconds(fields.get('resources_used.walltime', '00:00:00'))
    assert remaining >= 27000+3600+1800, (queue, 'insufficient remaining allocation', remaining)
    print(queue, job, w['hostname'], 'slots=28', 'remaining_seconds='+str(remaining))
PY
```

只有上述检查全通过后提交。使用归档源码保持统一版本；长任务按已接受基准的耗时优先启动。提交后立即启动 head 上的轻量 observer，它只读取结果文件，不运行 GAP。

```bash
"$FSPT_PY" scripts/submit_campaign.py --run "$FSPT_RUN" \
  --queues "${FSPT_RUN_TAG}_q1" "${FSPT_RUN_TAG}_q2" "${FSPT_RUN_TAG}_q3" \
           "${FSPT_RUN_TAG}_q4" "${FSPT_RUN_TAG}_q5" \
  --groups 1-230 --mode full --timeout 27000 \
  --source results/space_groups/source --timings results/space_groups

nohup "$FSPT_PY" scripts/watch_campaign.py "$FSPT_RUN" --interval 10 \
  >> "$FSPT_ADMIN/observer.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$FSPT_ADMIN/observer.pid"
```

保留 `campaign.json`、`observation.json`、observer 日志和 `runs/tasks/`。如果 observer 被中断，重新连接仍复用 SSH master，恢复本次 `FSPT_RUN_TAG`、`FSPT_RUN`、`FSPT_ADMIN` 和 `FSPT_PY` 变量，然后使用下面的命令；不要删 observation 重新计时。脚本用文件锁拒绝同时运行两个 observer。

```bash
nohup "$FSPT_PY" scripts/watch_campaign.py "$FSPT_RUN" --interval 10 --resume \
  >> "$FSPT_ADMIN/observer.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$FSPT_ADMIN/observer.pid"
```

日常检查可用 `scripts/monitor.py --queue "${FSPT_RUN_TAG}_q1" --prefix "$FSPT_RUN_TAG"`，其余四队列同理，并查看这些 job 的 `qstat -f`。单任务日志中的 `AFS_STAGE` 是阶段入口，不能据一个长阶段推算完成百分比。若任务失败或 allocation 到期，保留原状态及日志，在新的 namespace 重试；不要改写 timeout/failed 为成功。

等全部 230 个 full 结果及 task 状态落盘后，严格核对，并生成本轮性能报告。报告含排队和观察延迟，不把 7.5 小时预算当成实际耗时。

```bash
"$FSPT_PY" scripts/audit_run.py "$FSPT_RUN" --write \
  --require-complete-witnesses \
  --require-formula-convention normalized-pip-aw-edge-transport-v2
"$FSPT_PY" scripts/collect_performance.py "$FSPT_RUN" \
  --tasks-root runs/tasks --output "$FSPT_RUN/performance.json"
```

最后确认本轮所有 worker 都已没有 active、pending 或 running 任务，再在**本轮自己的五个队列**放置 `STOP`。worker 会正常退出，PBS allocation 随之释放。不要清除任何历史 `STOP`，也不要为了重用旧队列改写其状态。

```bash
"$FSPT_PY" - <<'PY'
import json, os, pathlib
root = pathlib.Path.cwd()
admin = root/'runs'/(os.environ['FSPT_RUN_TAG']+'_pbs')
pairs = [line.split() for line in (admin/'jobs.tsv').read_text().splitlines()]
for queue, job in pairs:
    base = root/'runs'/queue
    w = json.loads((base/'worker.json').read_text())
    assert w['pbs_job'] == job and not w['active']
    assert not list((base/'pending').glob('*.json'))
    assert not list((base/'running').glob('*.json'))
for queue, job in pairs:
    (root/'runs'/queue/'STOP').touch(exist_ok=False)
    print('draining', queue, job)
PY

while IFS=$'\t' read -r FSPT_QUEUE FSPT_JOB; do
  qstat -f "$FSPT_JOB" || true
done < "$FSPT_ADMIN/jobs.tsv"
```

稍后再次核对这些确切 job ID：`job_state = C` 或 PBS 已不再保留该 job 表示已结束；仍为 `R` 时检查自己的 worker 日志，不把一次查询失败当作已释放。此次重跑结果留在新的 `runs/` 目录，不覆盖正式的 `results/space_groups` 或原独立分类冻结。
