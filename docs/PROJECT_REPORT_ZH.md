# FSPT_AHSS 项目交付报告

**全部230个空间群的 classification 和完整 stacking 已完成，正式接受 v09。** 同一冻结版本整轮运行中，classification 在 **13分3秒**完成，全部 stacking 在 **3小时31分39秒**完成。正式结果位于 [results/space_groups](../results/space_groups)，[230群总表](../results/space_groups/report/space_groups.pdf)、[性能图](../results/space_groups/performance.pdf)及全部生成元关系均已生成。

全230份结果通过完整 witness、精确 Smith 关系、AW-v2 公式约定和源码一致性审查；与未启用这两项可选优化的通用 v07 数学基线逐项比较，所有保存的数学字段完全一致。44个具有非零自由 p+ip 层的群都导出实际存活格基及完整生成元塔，32个存活的 torsion p+ip 情形都保存完整上层 witness。独立四层分类与老板提供的新表逐项比较，920项全部一致。

## 计算对象与独立实现

本轮计算采用三维空间、物理自旋半整数超导费米子、无额外 onsite 对称性、晶体等价后的有效 `omega=0`，符号作用取空间群行列式。计算使用完整的无限仿射空间群，包含平移；保留弱相和原子费米子宇称层。

新程序位于远端 `/home/user/xyren/AllFSPT`，本地 Git 仓库为 `/home/xingyu/FSPT_AHSS`。运行时不加载或包装 SptSet。GAP/HAP、CrystCat 和 Polycyclic 提供群与 resolution 等通用基础设施；cochain comparison maps、精确商群计算、classification 流程、生成元 lift 与 stacking reduction 是本项目的实现。

数学输入包括你提供的 obstruction、stacking 公式，以及合作者构造中用于 torsion p+ip 平方的 calibrated cochain product。后者的通用系数在本项目中重新求值、转换坐标并编译；运行时不导入合作者的计算引擎。旧 SptSet 和外部空间群答案表仅用于事后对比，未参与求解或选择输出。

每个空间群由**一个顺序执行的 GAP 进程**完成：

```text
建立实际仿射群与 resolution
    → classification：cocycles、obstructions、商群与 gauge
    → 非零自由 p+ip 层的实际存活格基及完整 lift
    → 同一 classification 对象上的生成元 stacking 与关系约化
    → 导出结果、关系矩阵、cochain 数据和来源哈希
```

并行发生在不同空间群之间，任务运行在 PBS 计算节点。stacking 直接使用前一步保留的代表元、primitive 和商群坐标，而不是只读取四层抽象群的阶数重新猜 extension。

输出同时保留四个 associated-graded 层和最终 stacking 群。四层的直和通常不是最终答案；最终群由实际生成元关系及整数 Smith 分解得到。回放接口支持这些已标记生成元的整数线性组合，并按照保存的关系计算叠加。

## 公式、实际生成元与正确性检查

完整公式与坐标约定整理在[7页公式说明](../notes/independent_space_group_formulas.pdf)，对应 [LaTeX 源文件](../notes/independent_space_group_formulas.tex)。[FORMULAS.md](FORMULAS.md) 给出代码接口，[VALIDATION.md](VALIDATION.md) 区分公式输入、独立验证和适用范围。

独立负整数测试发现并修复了我们编译器中的一个 Alexander–Whitney transport 转录错误：每条整数边必须从它自己的起点运输。修改的是本项目的公式转录，提供的原始公式没有被改动。当前约定命名为 `normalized-pip-aw-edge-transport-v2`；相关 phase、unary dictionary、整数 gauge 与 C4 primitive 已同步修正。

修正后的完整公式与**未经修改的原始 scalar evaluator**比较：84个合法整数塔全部通过，覆盖原先两个失败例、负整数及 `2^45` 量级的整数；通用 C4 塔的1024个 O5 输入也全部直接对上原 evaluator。坐标字典、整数 cylinder gauge、完整 torsion 平方的局部恒等式另有精确检查。修正后的 SG7、SG81、SG82 和有限 C4 完整 cochain controls 已通过。具体输入、哈希和证明见 [AW 修正说明](AW_TRANSPORT_CORRECTION.md)。

自由 p+ip 层也已落实为实际代表元：44个相关群保存的是存活整数格的基、在原始 `H^1(G,Z_s)` 中的坐标、可能的 torsion shift，以及 Majorana、CF、phase 各层数据。它们不只是按原始 cohomology 的自由秩补一个形式上的 `Z^r`。其中29群的存活格指数为1，14群为2，SG2为8；SG2的抽象自由部分仍为 `Z^3`，但在保存的原始自由基坐标中，实际存活子格是 `2Z^3`。这也是只给抽象秩不足以回答生成元如何 stacking 的一个例子。详细构造见 [FREE_PIP_LATTICE.md](FREE_PIP_LATTICE.md)。

CF lift 同样保留了所需的 cochain 修正。完整 bar 路径使用原来的 integral comparison-homotopy correction。纯 CF 的 native 路径保存 native seed 和精确重构方法：调用 `AFSReconstructNativeCFLift` 时求解差值的 binary primitive，再加上半整数 phase correction，使 lift 满足实际 bar 方程。native diagonal 与 bar 公式在上同调中一致，并不表示其原生向量逐项相同。该修正在 doubling 时消失，因此这一路径不必为求 stacking 关系而提前展开全部 bar 值；重构方法仍保留在输出中。

这些结果的证据范围是：

- 公式、整数 carries、Smith 分解和 phase 求解使用精确整数或有理数运算。
- 保存的矩阵、商群、生成元与 source digest 可以重新审查；这种文件审查不等于重跑全部 cochain 计算。
- 已记录的定向 controls 检查了 comparison maps 所需 simplices 上的 lift 与 relation gauge 方程。全230群都完成 classification、44群都构造了自由层 witness，**不等于全230群都另做过完整 support audit**。
- calibrated product 的闭项仍是数学输入；有限的局部测试不构成新的完整 coherence 或物理唯一性定理。原 normalized manuscript 的相对、有限群假设没有被数值检查自动扩展。

## 与现有结果的对比

独立230群分类先冻结并保存哈希，然后才读取外部答案。老板的新 `space_group_230_layers.pdf` 与本轮物理约定一致；其230群、每群四层，共 **920项全部匹配**。最终接受结果与原独立冻结、最终结果与 PDF、原冻结与 PDF 三组比较均为920/920。该 PDF 没有给出完整 stacking extension，因此920项一致不能表述为230个完整 stacking 群全部经过外部核对。逐项结果见 [最终分类比较报告](../results/boss_layers/current_reference_comparison.md)；[首次比较记录](../results/boss_layers/reference_comparison.md)保持原样。

历史稿件另有204行非空完整 stacking 答案。与修正后独立结果比较：

最终230群独立完整结果已全部纳入比较；其中26群的历史完整群栏为空，不能填作一致。

| 比较类别 | 数量 |
|---|---:|
| 完整 stacking 群相同 | 179 |
| 完整群不同，且至少一个 graded layer 已不同 | 21 |
| 四个 graded layer 全相同，但 extension 不同 | 4 |
| 历史完整 stacking 栏空白，无法对比 | 26 |

其中21例不能单独归因于 stacking law，因为其 classification 已有变化。剩下4例是真正的同层 extension 差异：

| 空间群 | 历史完整群 | 独立计算的完整群 |
|---|---|---|
| 68，Ccca | `Z₂³ ⊕ Z₄` | `Z₂⁵` |
| 81，P-4 | `Z ⊕ Z₂⁴ ⊕ Z₈³` | `Z ⊕ Z₂² ⊕ Z₄ ⊕ Z₈³` |
| 82，I-4 | `Z ⊕ Z₂⁴ ⊕ Z₈²` | `Z ⊕ Z₂² ⊕ Z₄ ⊕ Z₈²` |
| 101，P4₂cm | `Z₂ ⊕ Z₄` | `Z₂³` |

这里 `⊕` 表示直和，上标表示因子重数。四个历史值均已在原稿及原始完成的 SptSet 日志中确认，不能简单解释成表格转录错误。

SG68、101 的区别落在 Majorana 生成元的平方：新计算经过实际 incoming gauges 约化得到 `2B=0`，并非原始平方 cochain 逐点为零。SG81、82 得到 `2P=C1`、`2C1=0`，产生一个独立的 `Z₄` 因子；实际仿射群对 C4 的 retraction，以及有限 C4 的完整计算，提供了额外的直接和一致性检查。这四例的针对性完整验证已经通过；尚未把差异定位为旧程序某一行的错误。详见[四例关系分析](HISTORICAL_STACKING_REVIEW.md)及保存的原始日志。

提供的 Weicheng checkout 中包含有限群 benchmarks 和通用 cochain 公式，**没有可用于全230无限仿射群 stacking 对比的答案表**。这只描述已提供且已检查的材料，不推断未发布结果。与当前三维、`omega=0` 范围一致的有限 C2 结果共有四个标签，实际对应两个不同输入；两项独立全流程计算均给出平凡群，与参考一致。这些小规模 controls 和公式对比，不能替代不存在的230群完整答案对照。参考文件清单、比较约定和结果见 [COMPARISON_WEICHENG.md](COMPARISON_WEICHENG.md)。

## 实测性能与最终配置

以下数值全部来自正式接受的同一轮 `full_closed_cf_v09`，没有按群挑选不同版本的较快结果：

| 项目 | 实测数值 |
|---|---|
| 230个 classification 检查点全部完成，含实际自由层构造 | **783.017秒，即13分3秒** |
| 先完成的229个群已获得完整 stacking | **3657.307秒，即60分57秒** |
| 全230 classification + 完整 stacking 总 elapsed time | **12699.328秒，即3小时31分39秒** |
| 全部任务累计 GAP CPU 时间 | **62963.022秒，即17.490小时** |
| 全部任务 GNU time 进程树 CPU 时间 | **63036.050秒，即17.510小时** |
| 最慢群 SG219：完整 GAP CPU / 单次调用 wall time | **12689.769秒 / 12691.841秒** |
| 全轮最大单任务 peak RSS | **17688448 KiB，即16.869 GiB，SG219** |

classification 耗时不是完整 stacking 耗时；累计 CPU 时间也不是并行运行的总 elapsed time。旧 SptSet 日志及合作者“一晚上”的描述缺少统一硬件和运行配置，因此不据此给出严格加速倍数。原始测量见 [performance.json](../results/space_groups/performance.json)，可携带归档的独立重算见 [portable_performance.json](../results/space_groups/audits/portable_performance.json)。

运行使用5个 PBS worker，每个最多28个并发任务，合计上限140。期间还有其他候选及验证任务共享这些 worker，因此这里是实际部署中的 elapsed time，包含排队、资源竞争及观察间隔，不是独占140核的 benchmark。classification 数值取完整流水线中首次观察到全部230个检查点的时刻，也不是另开一次只算 classification 的测试。

SG219 的实际生成元构造是整轮耗时的主要原因；其余229群在约61分钟时已经完成。增加跨群并发不能继续缩短最后一个顺序 GAP 任务。SG219 的 Majorana B1 lift 和 p+ip phase lift 分别占4288.262及4041.885 CPU秒；后续优化应集中在这些实际 cochain primitive 的求值与缓存，而不是只加节点。最终结果为 `Z₂² ⊕ Z₄`，保存的关系是 `2P1=C1`、`2C1=2C2=2B1=0`。

原四小时上限到来前，三个健康的 SG219 任务获得了明确延期，总预算各为7.5小时，仍受原 PBS 分配约束。冻结数值代码和 GAP 进程保持原样，原始任务状态没有改写。最终接受的 v09 实际在原四小时内完成，原 worker 记录为 `done`、退出码0；完成的监管记录、GNU time 和源码证据仍全部保存并经过严格审查。这个7.5小时预算不是实测耗时，整轮 elapsed time 始终由原 campaign observer 记录。详见[调度与延期证据](SCHEDULING_EXTENSIONS.md)。

最终源码 ID 为 `9c16c0714da16a1ed5dc23b7830701afc01e6d7a37ee6d243f536ee4dc9ecd96`；本地及远端当前 `gap/*.g` 与 [正式冻结源码](../results/space_groups/source/gap)逐文件一致。启用 closed-CF lazy evaluation 和 exact half-phase transfer，关闭可选的 mod-two bar comparison map；classification 内的 native mod-two contraction 保持启用。这一选择保留后续 Majorana lift 可复用的 integral cache。优化适用条件与 controls 见 [CLOSED_CF_OPTIMIZATION.md](CLOSED_CF_OPTIMIZATION.md)。

同时启用 mod-two bar comparison 的 v08 也完成了全部230群，所有保存的数学字段与 v09 完全一致。它的完整 elapsed time 为14751.680秒（4小时5分52秒），累计 GAP CPU 为70171.795秒，最大单任务 RSS 为20.063 GiB。在此次共享 worker 的实际部署中，v09 总耗时少2052.352秒（约34分12秒），内存峰值也较低，因此接受 v09。两轮完整证据和选择依据见 [optimization_validation](../results/optimization_validation/README.md)。

通用 v07 的 SG219 原任务曾因90分钟预算超时，随后由同一源码重跑补齐。完整通用数学基线及来源保存在 [optimization_validation](../results/optimization_validation)；这个229+1集合只用于数学比较，不充作不间断整轮 benchmark。它与最终 v09 的230组结果在生成元、phase、gauge、关系矩阵、自由格与 Smith 数据上全部逐项一致；比较仅排除了明确列出的执行时间和来源字段。原始超时与历史记录均保留。

## 复现、结果与叠加入口

在已分配的计算节点中，从远端工作目录运行一个群：

```sh
cd /home/user/xyren/AllFSPT
python3 scripts/run_group.py 81 --mode full --source results/space_groups/source \
  --output runs/example/sg81.json
python3 scripts/stack_result.py results/space_groups/sg81.json \
  --left '{"P1":1}' --right '{"P1":1}'
```

在此 SG81 例子中，两个 `P1` 叠加得到 `C1`，`P1` 的阶为4；这直接展示了层间 extension。

`stack_result.py` 对保存的 marked presentation 做叠加与约化。生成元标签依赖该结果的坐标基，不宜在不同 source 之间直接对应。若要重现指定冻结版本，为 `run_group.py` 指定其 `--source` 路径，以 campaign manifest 中记录的路径为准。

本地 Git 仓库已经建立并保存提交历史，没有发布 GitHub 远端。完整 campaign 使用 `scripts/submit_campaign.py` 冻结源文件并向有效 PBS workers 排队；跨群并行和每个任务的日志、状态、时限都被保留。新的五节点申请、两级持久 SSH 复用、重跑、监控及资源释放见 [CLUSTER_RUN.md](CLUSTER_RUN.md)。默认 `--timeout 27000` 是单个群的调度预算，不是7.5小时实测耗时；实际提交须给排队与清理留出 PBS 时间。

正式归档可以直接重新审查和生成表格，无需再运行 GAP：

```sh
python3 scripts/audit_run.py results/space_groups \
  --require-complete-witnesses \
  --require-formula-convention normalized-pip-aw-edge-transport-v2 --write
python3 scripts/report_results.py results/space_groups \
  --require-full-stacking --require-complete-witnesses \
  --require-formula-convention normalized-pip-aw-edge-transport-v2
python3 scripts/render_table.py results/space_groups \
  --output results/space_groups/report/space_groups.tex --pdf
```

每群 JSON 保存四层群、最终 stacking presentation、Smith 数据、生成元 witness 与来源；[CSV](../results/space_groups/report/independent_results.csv)、[Markdown](../results/space_groups/report/independent_results.md)和6页 PDF 均来自同一正式归档。归档共有1198个原始及清单文件，总计15929682字节（另生成的报告不计入该数字）；清单 SHA-256 为 `60bc072c330c838a10e6a1f663eb6664e1d09e010b5081141dacf609aff33831`。所有归档载荷经本地与远端哈希核对，公式 PDF 和总表经过排版检查。完整字段解释见 [RESULTS_REPORT.md](RESULTS_REPORT.md)。

两轮候选、所有验证任务和监管进程均已结束，五个 PBS allocation 已全部释放。各队列的 `STOP`、空任务队列和调度器核对记录保存在 [final_release.json](../results/performance_environment/final_release.json)，历史任务状态保持原样。
