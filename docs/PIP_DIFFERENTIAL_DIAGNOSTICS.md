# 已接受 crystalline spin-1/2 结果的 p+ip 诊断

本报告主体只分析 `results/space_groups/sg1.json`–`sg230.json` 已保存的证据，不运行 GAP，不重算缺失的初始障碍，也不读取合作者答案。对应 **crystalline spin-1/2 = internal spinless**，有效背景为 `omega_eff=0`、`s_eff=w1`；不能据此断言 crystalline spinless / internal spin-1/2 的另一半也没有高阶障碍。

文末的独立补证另列后来控制运行补出的三个字段，不改旧归档和原诊断 JSON。

可复用的导出命令是：

```bash
python3 scripts/analyze_pip_diagnostics.py results/space_groups \
  --output results/pip_diagnostics/crystalline_spin_half.json
```

脚本逐一核对归档中的结果 SHA-256，拒绝混合 convention、source ID 或 formula convention。默认要求完整 230 群；`--allow-partial` 仅用于明确标记缺失群的开发报告。它读取实际已保存字段，遇到不认识的 certificate 会标记未知，不把缺失字段补成零。输出每个 candidate 的 JSON 路径、原始记录、推断所用的字段及每个群的输入哈希。

## 先区分四件事

1. `status="killed", page=3/4` 才是完成允许的低层选择后，真正被对应页障碍杀掉的候选。
2. `d3_initial_coordinates` 是固定初始 Majorana 解时，在 `H^4(G,Z2)` 中的源坐标。它非零，不等于商掉允许的 Majorana 选择后，真正的 `d3` 非零。
3. `d4_raw_coordinates` 是固定低层塔的 `H^5(G,U(1)_s)` 类；实际 `d4` 还要商掉 CF primary image 和 MC secondary image。raw 非零也可能存活。
4. `d4_target=[]` 是整个商目标零；`d4_target=[3]` 等只表示其二初级部分为零。代码对当前二阶源使用后一个充分条件，不应将它写成“整个目标为零”或“完整 O5 cochain 为零”。后续构造完整 phase primitive 仍可能需要非零低层调整。

这些字段的生产语义可在归档源码 [pip.g](../results/space_groups/source/gap/pip.g)、[pip_free.g](../results/space_groups/source/gap/pip_free.g) 和 [pip_stacking.g](../results/space_groups/source/gap/pip_stacking.g) 核对。

## Orientation torsion 候选

230 群中，165 群保存了一个 orientation torsion 候选；另 65 群没有该候选。165 个候选中 133 个在 `d2` 被杀，32 个存活。**保存的结果里没有真正 killed at d3 或 d4 的 torsion 候选。**全部精确群号和字段指针在机器报告的 `cohorts.torsion` 中。

32 个存活群为：

`7, 9, 27, 29, 30, 32, 33, 34, 37, 41, 43, 45, 81, 82, 103, 104, 106, 110, 112, 114, 116, 117, 118, 120, 122, 158, 159, 161, 184, 218, 219, 220`。

其中 13 群的初始 `d3` 源类非零，但由保存的 `majorana_adjustment` 消除：

| SG | `d3_initial_coordinates` | `majorana_adjustment` |
|---|---|---|
| 32 | `[0,0,1,0]` | `[0,0,1,0]` |
| 34 | `[0,1,1,0]` | `[0,1,0,0]` |
| 45 | `[0,0,0,1]` | `[0,0,0,1]` |
| 110 | `[1,0]` | `[1,0]` |
| 112 | `[1,0,1,0,0,1,0,0,0,0,0,0,0,0,0]` | `[0,0,0,0,1,0,0]` |
| 114 | `[1,0,0,0]` | `[1,0,0]` |
| 116 | `[1,1,0,1,0,1,0,0,0,0]` | `[1,0,0,0,1,0]` |
| 117 | `[0,1,0,0,0,0,0,0,0]` | `[0,1,0,0,0]` |
| 118 | `[0,1,0,0,0,0,0,0,0]` | `[0,1,0,0,0]` |
| 120 | `[0,1,0,0,0,0,1,0]` | `[0,1,0,0,1]` |
| 122 | `[1,0,0,0]` | `[0,1,0]` |
| 218 | `[1,0,0,0,0]` | `[1,0,0]` |
| 219 | `[1,1]` | `[0,1,1]` |

每行的路径为 `sgN.json#/pip/torsion/0`。坐标属于该群自己的 native cohomology 基，跨群不能逐分量比较。该调整是 `H^2(G,Z2)` 中改变低层定义塔的选择，不必已经是一个独立存活的最终 MC 相。

`d4` 的存活证据分三类：

| 证据 | 群号 | 保存内容 |
|---|---|---|
| 整个商目标零（23 群） | `7,9,27,29,30,32,33,34,37,41,43,45,81,82,106,110,112,114,116,117,118,120,122` | `d4_target=[]`，分类阶段不计算完整 O5 类 |
| 商目标非零但只有奇数阶（7 群） | `158,159,161,184,218,219,220` | 分别为 `[3,3,3]`, `[3,3]`, `[3]`, `[3,3]`, `[3]`, `[3]`, `[3]`；同样跳过分类阶段的 O5 类求值 |
| 显式计算 O5 后存活（2 群） | `103,104` | raw 坐标分别 `[0,0,0]`, `[0,0]`；商目标分别 `[2,2]`, `[2]` |

这里“跳过”仅指 `AFSClassifyPipTorsion` 的类判定。完整 stacking 阶段仍有实际 phase lift；不能把前一阶段的 shortcut 理解为整个程序未处理 bosonic phase。

## 自由 H1 候选与存活整数子格

44 群有自由 p+ip 层。20 个 unitary 群直接使用 `s=B=C=0` 的通用完整塔，`parityCandidates=[]`，所以没有逐候选的 `d3/d4` 初始记录：

`1,3,4,5,75,76,77,78,79,80,143,144,145,146,168,169,170,171,172,173`。

其余 24 群共保存 55 个非零自由 parity candidate：46 个在 `d2` 被杀，9 个存活，没有记录到 `d3` 或 `d4` 真正杀掉的候选。9 个存活候选属于 `7,8,9,14,81,82,84,86,88`。

其中 SG8、86、88 保存了非零初始 `d3` 源，经 MC choice 消除，分别为：

| SG | H1 坐标 | 初始 `d3` 源 | MC 调整 |
|---|---|---|---|
| 8 | `[1,1]` | `[0,0,1,0]` | `[0,0,1,0]` |
| 86 | `[1,1]` | `[0,1,0,0,0,0]` | `[0,1,0,0,0]` |
| 88 | `[1,1]` | `[0,1,0,0]` | `[0,1,0]` |

**SG84 是已保存数据中最明确的 raw `d4` 非零但实际存活例子。**

- `sg84.json#/pip/free_lattice/parityCandidates/1` 的 `h1Coordinates=[1,1]`。
- `d4_raw_coordinates=[0,1,1,0,0,1,0,0]`，并非零。
- `d4_target=[2,2,2,2]`，不能用无二初级目标的 shortcut。
- certificate 为 `explicit-full-O5-in-E4-quotient`，表示投影到实际 E4 商后为零。
- 后续自由生成元的 `cfIndeterminacyAdjustment=[0,1,0,0,0,0,1,0,0,0,0]`，并保存了完整 phase primitive。这里没有用“raw 非零”来错误杀掉整数层。

SG8、84、86、88 的 `h1BasisOrders=[2,0]`。初试 `[0,1]` 在 `d2` 被杀，而加入 orientation torsion 后的 `[1,1]` 存活。因此自由投影的 primitive parity 仍然保留，`latticeBasis=[[1]]`。这两个候选是**不同的 H1 类**，不是同一类的普通 coboundary gauge；它们有相同的自由投影。若只测 `[0,1]`，就会错误地把存活自由子格缩成 `2Z`。

另一方面，实际自由子格确实缩小的有 15 群：SG2 的 index 为 8、基为 `2I3`；`6,10,11,12,13,15,83,85,87,147,148,174,175,176` 的 index 为 2。抽象自由群的秩仍不变，不能从表中 `Z`/`Z^3` 的符号倒推 primitive candidate 全部存活。

枚举会在同一自由 parity 找到一个存活 torsion shift 后停止。因此 `parityCandidates` 是用于确定自由投影子格的实际已尝试候选，不是所有 H1/2H1 元素的完整列表；未试的其他 torsion shift 不应补成“存活”或“死亡”。

## 已保存 p+ip square 向低层的关系

32 个 surviving torsion 群都保存了完整 `pipGenerator`、`pipRelation` 和 `fullPresentation`。报告从**最终 presentation 的末行**读取

`2 P1 = sum_j a_j G_j`，

再按 `stacking.lower.generators[j].layer` 分组：0 为 bosonic，1 为 CF，2 为 MC。`pipRelation.lowerCoordinates` 只写 bosonic+CF 的前缀；省略的 MC 零项由完整 presentation 的实际零列交叉核对，不能仅凭短数组猜测。

所有 32 个已选标记 square 的最终 MC 坐标均为零。CF 坐标非零的 12 群及剩余 bosonic 坐标如下；没有列出的 20 群最终关系是 `2P1=0`：

| SG | CF 部分 | 同一标记基中的 bosonic 部分 |
|---|---|---|
| 81,82 | `C1` | 0 |
| 112 | `C1` | `D2+D6+D8` |
| 114 | `C1` | `2D1` |
| 116,117 | `C1` | 0 |
| 118 | `C1` | `2D5` |
| 120 | `C1` | 0 |
| 122 | `C1` | `D1` |
| 218,219 | `C1` | 0 |
| 220 | `C1` | `2D1` |

各群的 `C1/Dj` 是自己结果里的实际 lift，不能跨群认作同一个 cochain。bosonic 分量依赖选定的 CF lift；这不是三个独立的、无条件规范不变的投影。特别是 `2D1` 在其相应四阶 bosonic 因子中非零。

这里统计的是完成整数层 gauge 消除、低层 coboundary/incoming reduction 后的**最终关系**，不是原始二元 stacking law 的三个独立 twister。存档没有为任意两个整数 decoration 保存逐项 MC/CF/bosonic twister 求值，也没有保存“人为关掉某项”后的对照。由某个先出现的低层分量非零，不能推出更低层相位修正不影响 stacking；最终坐标为零也不能证明中间 correction 恒为零。

实际 phase lift 已显示其区别：generic orientation 塔的 SG45、120、219 使用了非零 CF indeterminacy adjustment；自由塔的 SG8、84 也如此。SG219 的分类 `d4_target=[3]` 虽无二初级部分，仍需要该 CF 调整来构造完整平坦 phase 塔。另 26 个 orientation lift 使用独立的 universal C4 pullback；它们的空 adjustment 数组表示这条构造路线没有使用 generic solve 的坐标，不能反推先前 AHSS 定义塔的初始障碍为零。

## 无法从旧存档倒推的项目

- torsion SG103、104 和 free SG84 在显式 `d4` 分支没有保存 `d3_initial_coordinates`；旧函数复用了局部变量 `co`。保存了 MC 调整向量，但本报告不重建丢失的初始向量。
- 30 个 torsion shortcut 及 8 个 free shortcut 没有保存分类阶段初始 `H^5` raw 类。之后的完整 lift 可能改用 universal C4 或调整过的低层塔，不能把那份 phase 代表反认为原始类。
- generic 完整 phase lift 的 export 保存最终 MC/CF 调整和 phase primitive，却未保存调整前、重新选 MC 后的每一份 `H^5` 类。只能报告实际调整，不能逐阶段恢复缺失类。
- unitary 自由塔通过恒等式存活，没有逐 candidate 初始数据；未到达某一页的候选也没有该页数据。
- 源 JSON 保存 native vectors 和比较同伦重建方法，并非全 bar cochain 真值表。本报告不重新执行 comparison-support cochain 检查；`checkedComparisonSupport=false` 原样保留。
- 未保存通用二元 twister 的逐项对照；本报告给出的是实际最终平方关系，不能以此宣布某个未知 twister 普遍无效。

新的另一 spin 约定结果可以再次运行相同脚本，但应输出到另一 JSON，并分别报告 convention。若新生产代码保存更完整的初始字段，可补充相应解析，不能让旧记录的缺项自动变成零。


## 第二 spin 约定的解析接口（等待正式归档）

脚本 schema 2 已支持 `physical-spinless-det-sign-Pin-minus`，但本节不填开发
run 的统计值，也不改变上面已接受第一半的结论。对正式第二半应另写输出文件。

- `h0_incoming` 读取实际 `H/<X>` 的完整整数格证书和商前、商后的 graded。
  三层阶数比依次给出 H0 的 `d2/d3/d4` incoming image 的阶，同时保存该页
  输入整数生成元相对于原 H0 的倍数。三项乘积必须等于 actual X 的阶。
  这是已证实 cyclic quotient 的过滤像，不是重新求值未经 gauge 调整的
  原始 `Sq1(omega)` 或 Pontryagin cochain。未保存的 raw d3/d4 坐标仍明确
  标为缺失。商后的 graded 必须与最终 classification 相符，否则拒绝报告。
- 非零背景的自由层使用已保存 `certifiedIntegerPeriod=16`，区分自由坐标
  1、2、4、8 的实际候选和严格 16 倍通用塔。脚本按模16的自由投影比较
  torsion shift，不再把所有奇数候选误并成同一个 parity。仍不会把未尝试的
  torsion shift 补成存活。零背景继续使用原模2解释。
- `upper_extension_family` 原样保留允许的完整仿射 Ext family、所有可能的
  抽象群、height 证书，以及 CF/bosonic unknown carries。唯一抽象群并不代表
  已构造唯一 upper phase，也不代表未知 carries 为零。`square` 仅在实际保存
  完整标记关系时给出低层坐标；仅有 leading MC square 时不填 CF/bosonic 零项。
- 完整 classification 但只有多种 upper group 可能性的记录可作为
  `stacking_status="unresolved"` 的证据报告；它们另列于
  `upper_extension_ambiguous_isotype`，不伪装成已完成 stacking。
  无此完整 Ext family 证书的失败/未完成记录仍被拒绝。

`tests/test_pip_diagnostics.py` 的五个控制检查三层 incoming、错误的商后 graded、
未知 carry 的保留、完整但异型不唯一的 family、模16候选的区分和失败记录拒绝。
重新读取原第一半230群后，旧版全部 candidate 记录和原有 cohort 逐项完全一致。


## 独立补证：旧第一半缺失的三个初始 d3 字段

本附录使用后来完成的三个 **同一第一半物理约定** 控制运行补齐缺失字段，
不覆盖 `results/space_groups` 的230个已接受 JSON，也不重写
`results/pip_diagnostics/crystalline_spin_half.json` 的历史 cohort。
原文“旧存档未保存这些坐标”仍成立；下面的向量来自新执行，不能描述为从旧文件读出或倒推。

新控制采用源码 `73e7bae91a1c02156431ddc1c072c06d32517e287b5aa6314203f416cff1b252`，
物理约定仍是 `physical-spin-half-det-sign-omega0`；同一源码支持两种spin选择，
**不能因source相同把这些控制混进第二半统计**。旧接受源码为
`9c16c0714da16a1ed5dc23b7830701afc01e6d7a37ee6d243f536ee4dc9ecd96`。

[独立补证 JSON](../results/pip_diagnostics/crystalline_spin_half_d3_supplement.json)
记录新旧完整文件哈希、实际原始路径、候选pointer和原始字段副本。
SG84/104 的[旧字段逐项比较](validation_runs/background_literal_regressions/half_diagnostics_vs_accepted_complete.json)
以及包含SG103的[七群回归比较](validation_runs/background_literal_regressions/half_v3_vs_accepted_complete.json)
均通过；原有全部数学字段和 native witnesses 逐项相等。只排除了明确列出的运行时间/源码位置等metadata，
对新增的初始d3和projected d4则单列为 added evidence：不存在旧向量可供逐项比较。
本附录还重新核对了原230结果的归档哈希，均未改变。

| SG | 新控制中的候选路径 | 新保存的初始 d3 | 原有 MC 调整 | 新保存的 projected d4 |
|---|---|---|---|---|
| 103 | `/pip/torsion/0` | `[0,0,0,0,0,0]` | `[0,0,0,0,0]` | `[0,0]` |
| 104 | `/pip/torsion/0` | `[0,0,0,0]` | `[0,0,0]` | `[0]` |
| 84 | `/pip/free_lattice/parityCandidates/1`，H1=`[1,1]` | `[0,1,1,0,0,0,0,0,1,0,0,0,0,0,0]` | `[0,1,0,0,1,0,0]` | `[0,0,0,0]` |

SG103的输入位于 `runs/half_background_regression_v3/sg103.json`；
SG84和104位于 `runs/half_diagnostic_completion_v3/sg84.json`、`sg104.json`。
所有字段都属于各自运行的已保存基，不能跨群逐分量比较。

因此SG84同时具有两项可消的原始障碍：初始d3非零，经MC choice调整后可解；
其原已保存的 raw d4=`[0,1,1,0,0,1,0,0]`也非零，但在允许低层选择后的E4商中为零。
其最终完整 phase、CF调整和 stacking关系均与旧接受结果逐项相同。

综合旧档与本附录，第一半自由候选的“初始d3非零但可消”实例为SG8、84、86、88；
orientation torsion 的13个此类群保持不变。SG103、104新补出的初始d3均零。
这三个控制没有新增真正的d3/d4 kill，也没有改变任何classification或stacking表格数值。
