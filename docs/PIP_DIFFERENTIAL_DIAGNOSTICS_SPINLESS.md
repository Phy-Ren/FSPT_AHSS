# Crystalline spinless 第二半 p+ip 诊断：完整230群

本报告分析 **crystalline spinless = internal spin-1/2**，有效背景为
`omega_eff=w2+w1 cup w1`、`s_eff=w1`。计算对象是包含平移、螺旋和滑移等完整仿射操作的无限空间群。
它与第一半 `omega_eff=0` 的报告分开，不能合并两种约定的群号或统计。

**这是完整 230 群的正式归档诊断。**输入为
[results/space_groups_spinless](../results/space_groups_spinless)，原运行 `runs/spinless_230_v3`。
唯一数值 source ID 为 `73e7bae91a1c02156431ddc1c072c06d32517e287b5aa6314203f416cff1b252`，
formula convention 为 `normalized-pip-aw-edge-transport-v2`。
归档 SHA-256 为 `1c2148ca95fd5245ec5a490665f784229a629e2c8745b6838c17262ba7e3aa72`。
全部 230 群通过严格物理背景、lower 关系、H0 商、过滤格与 upper Ext 范围审核；
v1 与优化后的 v3 全230数学字段及 native witnesses 逐项一致。

机器证据为 [crystalline_spinless.json](../results/pip_diagnostics/crystalline_spinless.json)，
记录230个输入文件的 SHA-256、全部246个实际候选、原始字段和 JSON pointer。
[提取检查](../results/pip_diagnostics/crystalline_spinless_checks.json)
保存诊断/解析脚本哈希，逐一复核230个结果及归档全部 1193 个 payload 文件的哈希。
此前215群快照 [partial_v1](../results/pip_diagnostics/crystalline_spinless_partial_v1.json)
及其 [checks](../results/pip_diagnostics/crystalline_spinless_partial_v1_checks.json) 原样保留，明确是历史部分结果。
本次提取没有运行 GAP、重新求值 cochain、读取参考答案或混入其他源码版本。

## 如何理解“d3/d4 非零”

这里分开报告四种证据：

1. `status="killed", page=3/4` 才是允许低层选择后，真正由该页杀掉的候选。
2. `d3_initial_coordinates` 非零仅表示初始 Majorana 解对应的源类非零；
   `majorana_adjustment` 可以消去它。这不等于最终 d3 非零。
3. `d4_raw_coordinates` 是固定低层塔的 `H^5(G,U(1)_s)` 类。
   真正 d4 还要投影到允许 CF primary 和 MC secondary 调整后的商；
   raw 非零、`d4_projected_coordinates=0` 仍然存活。
4. `d4_target=[]` 是整个商目标零；非空奇数阶目标仅表示没有二初级部分。
   分类阶段使用该障碍只有二初级值的已证界（自由候选可用16倍周期）推出其像零；
   这不等于 O5 cochain 恒零，也不等于后续 phase lift 不需修正。

H1 候选的 outgoing differential 与下文 H0 incoming quotient 是两个不同位置的映射。
不能把“H1 没有被 d3 杀掉”写成“所有与 p+ip 有关的 d3 都为零”。

## 完整归档的实际候选结局

| 候选类型 | 保存的实际候选数 | killed d2 | killed d3 | killed d4 | 存活 |
|---|---:|---:|---:|---:|---:|
| Orientation torsion | 165 | 142 | 0 | 0 | 23 |
| 带非零自由投影的 H1 候选 | 81 | 51 | 0 | 0 | 30 |

**完整230群没有真正 killed at d3 或 d4 的已保存候选。**
这一结论覆盖实际搜索记录，不将未尝试的 H1 代表计入结局。实际搜索会在确定一个自由投影的存活塔后停止某些分支。

23 个 torsion 存活群为：

`6, 7, 8, 9, 28, 29, 30, 31, 32, 33, 34, 40, 41, 43, 156, 157, 158, 159, 160, 161, 174, 188, 190`。

初始 d3 源非零但已消除的全部已保存实例为：

| SG | 候选路径 | H1 坐标 | 初始 d3 源 | MC choice 调整 |
|---|---|---|---|---|
| 30 | `/pip/torsion/0` | orientation torsion | `[0,0,1,0]` | `[0,0,0,1]` |
| 5 | `/pip/free_lattice/parityCandidates/0` | `[1]` | `[0,0,1,0]` | `[0,0,1,0]` |
| 176 | `/pip/free_lattice/parityCandidates/0` | `[0,1]` | `[0,1,0,0]` | `[0,1,0]` |

坐标属于各群自己的 cohomology 基；它们是允许的定义塔选择，不必独立构成最终存活的 MC 相。
全部 53 个到达 d4 的候选都保存了初始 d3 坐标；正式第二半没有旧第一半显式 d4 分支的“初始 d3 遗失”问题。

**SG83 的自由候选给出 raw d4 非零但存活的明确反例。**
`sg83.json#/pip/free_lattice/parityCandidates/2` 保存：

- `h1Coordinates=[0,2]`；
- `d4_raw_coordinates=[0,0,0,0,1,1,0,0,0,0,1,0,1]`；
- `d4_target=[2,2,2,2,2,2,2,2]`，不能使用无二初级目标的 shortcut；
- `d4_projected_coordinates=[0,0,0,0,0,0,0,0]`，certificate 为 `explicit-full-O5-in-E4-quotient`；
- 实际自由生成元后续的 `cfIndeterminacyAdjustment=[0,1,0,0,1,0,1,1,1,0,0,0,0,0,0]`，
  且 `fullFreePhaseWitness=true`。

其自由存活格为 `2Z`，不是 primitive 候选 `[0,1]` 的存活；`[0,1]` 和 torsion-shifted `[1,1]` 均在 d2 被杀。

## d4 目标 shortcut 与实际求值

| 类别 | torsion 群 | free 候选所在群 |
|---|---|---|
| 整个 d4 商目标为零 | `7, 9, 29, 33, 174` | `7, 9, 14, 82, 88, 174, 176` |
| 非零商目标仅奇数阶 | `158, 159, 161` | 无 |
| 显式求值，raw 类零 | `6, 8, 28, 30, 31, 32, 34, 40, 41, 43, 156, 157, 160, 188, 190` | `3, 5, 6, 8, 10, 11, 12, 13, 15, 75, 77, 79, 80, 81, 84, 85, 86, 87, 168, 171, 172, 175` |
| 显式求值，raw 类非零但投影零 | 无 | `83` |

奇数阶目标在 SG158、159、161 分别为 `[3,3,3]`、`[3,3]`、`[3]`。
shortcut 共 15 个候选，没有保存分类阶段初始 raw H5 坐标；不从后续调整过的 phase 塔倒推它们。
到达 d4 的其余 38 个候选显式求值，37 个 raw 类零，1 个 raw 类非零但可消。

## 自由整数层：模16与实际子格

完整230个结果中有44群含自由 p+ip 层，都保存了完整自由 phase witness。
其中 27 群使用非零背景的 `certifiedIntegerPeriod=16`；另 17 群的实际内部背景为零或已显式平凡化，使用原模2构造。
模16是严格通用周期/覆盖证书，不是把 n 除以2，也不意味着每个输出生成元都是16倍。
本次正式结果没有最终生成元落回严格通用16倍塔；各实际生成元均有更小的已构造存活代表。

23 个群的自由格 index 大于1：

`2, 3, 10, 12, 13, 15, 75, 77, 79, 81, 82, 83, 84, 85, 86, 87, 88, 147, 148, 168, 171, 172, 175`。

SG2 的格为 `2I3`，index=8；其余22个均为 `2Z`，index=2。
其余21个自由格 index=1。表中的抽象 `Z`/`Z^3` 不记录这项 primitive-index 差别。

11 个群由通用零背景完整塔直接构造，没有逐候选记录：
`1, 4, 76, 78, 143, 144, 145, 146, 169, 170, 173`。
另33群保存上述81个实际候选。
完整实际尝试列表未出现“相同模16自由投影，改变 torsion H1 坐标后由 killed 变为 survives”的已保存实例；
这只描述实际尝试列表，不是证明 torsion shift 普遍无效。
尤其自由坐标1、2、4、8不能按奇偶性混成同一个候选。

## H0 incoming：实际 cyclic quotient 的分层作用

unitary 时存在 `H^0(G,Z_s)=Z`。程序在完整 lower MC/CF/bosonic stacking 群 H 中构造
actual incoming state X，随后取 `H/<X>`，并从整数关系格的饱和交重新计算每层 graded。
这里的最终 classification 已使用商后 graded；不能只从 MC 行删一个 Z2 而保留旧 CF/bosonic 行。

X 的正生成元 normalization 是给定的 unary 输入：MC 为 `n0*omega`，CF 为
`floor(n0/2)*(omega cup1 omega)`，故 n0=1 时 `a=omega,c=0`。repo→CA 字典只改变 phase。
这不是从固定CF后的闭合方程或平方校准推导出所有CF选择均等价；负倍数由实际CA群逆定义。
构造和输入范围见 [背景公式说明](CRYSTALLINE_SPINLESS_BACKGROUND.md)。

52群保存非零 actual incoming quotient：30群 X 的阶为2，22群为4。
所有52群的 incoming d2 像阶均为2；其中22群在 d2 核 `2Z` 上还有非零 d3 像，阶也为2。
完整230群的 incoming d4 像均平凡。
其余178群中，165群因非平凡 sign 而 `H^0(G,Z_s)=0`；13群的物理背景已在完整 affine 群上显式平凡化。
因此65个 unitary 空间群均已覆盖。

incoming d2 非零的52群：

`3, 5, 16, 17, 18, 20, 21, 22, 23, 24, 75, 77, 79, 80, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 149, 150, 151, 152, 153, 154, 155, 168, 171, 172, 177, 178, 179, 180, 181, 182, 195, 196, 197, 199, 207, 208, 209, 210, 211, 212, 213, 214`。

incoming d3 非零的22群：

`16, 21, 22, 23, 89, 90, 93, 94, 97, 98, 177, 180, 181, 195, 196, 197, 207, 208, 209, 210, 211, 214`。

每层像的阶通过商前/商后该层群阶比求出；三项乘积必须等于 actual X 的阶。
这是完整 cyclic quotient 的**过滤像证书**，不是重新求值未经低层 gauge 修正的裸 `Sq1(omega)` 或 Pontryagin 类。
H0 的原始 d3/d4 代表坐标未保存，本报告不重建。
对阶2的X，最终源核为 `2Z`；对阶4的X，源核为 `4Z`。
无非零 incoming d4 不等于所有 phase correction 为零。

对 unitary 空间群的定向 rank3 实表示，`P(w2)=rho4(p1)`，有限 holonomy 使 `p1` 为 torsion。
因此 `-P/4` 在 U(1) cohomology 中 exact，再加已给出的 eta gauge 可得 `4X=0`。
这解释本次 X 阶只出现2或4，却**不能单独推出 incoming d4=0**：若2X的CF在相应商中exact，
它仍可能留下阶2的bosonic类。这里 d4=0 由实际过滤交证书给出。
canonical X、2X、4X 的 leading coordinates 不能当作每页未经 gauge 修正的固定代表；
若2X的CF被消掉，下一页要读取实际 gauge-corrected 2X，不能直接代成4X。

例如 SG16：商前 lower 为 `Z2^12 x Z4`，商掉阶4的X后成为 `Z2^12`。
其 MC graded 从 `Z2` 变为0，CF 从 `Z2^8` 变为 `Z2^7`，bosonic 保持 `Z2^5`。
同一个 incoming 元素同时移除 MC 和 CF 的因素，不能用“先在MC非零”忽略后续过滤作用。

## Upper stacking：抽象群唯一与实际 marked witness

23个 torsion 存活群分为两种证据强度。

**7群保存完整实际 upper phase 和最终 marked square：**
`7, 9, 29, 33, 158, 159, 161`。
它们在各自已选低层 lift 基中的末行均为 `2P1=0`。
这只是经过整数 gauge 和低层 reduction 后的最终关系；中间 CF/phase cochain 可以非零，不能据此宣布裸 twister 恒零。

**16群只固定 leading MC square，尚未构造完整实际 upper phase/marked square：**
`6, 8, 28, 30, 31, 32, 34, 40, 41, 43, 156, 157, 160, 174, 188, 190`。
这些群保存 `fullUpperPhaseWitness=false`，
`unknownCarries=["complex-fermion","bosonic"]`，以及完整允许的仿射 Ext family。
程序保留全部未知 CF/bosonic carry，通过已保存 lower 群和允许 relation coset 的 height 分层，
证明每个允许值给出同一个抽象群；因此 abstract stacking status 为 computed。
这是抽象同构型的证书，**不是把未知 carry 设为零、不是唯一扩张类的证书，也不是已完成 upper 共链构造**。

在这16群中，leading MC 分量均非零，关系为移去整数 `2s` 后 `2P` 的 MC 类等于 `[omega]`。
但“MC先非零”本身不推出CF/bosonic修正不影响同构型。
本次之所以能固定抽象群，依靠的是每个群完整允许 Ext family 只有一个 `invariantOptions`，而不是只看leadingMC。
完整230群没有多种抽象同构型的 unresolved family；16群的结论均是在给定第一整数层乘积 normalization 下，对整个允许 fiber 的同构型证明。

机器摘要 `square_nonzero_components.complex_fermion=[]` 和 `bosonic=[]`
仅表示**没有记录到已知的非零分量**：对于上面16群它们未知，绝非16个零结论。
实际完整关系仅有上述7群；其余没有 torsion 候选的行也不提供额外 zero-twister 证据。
自由生成元没有有限 quotient-order square 关系，抽象自由因子不能反映其所有逐项 cochain product。

## 论文与复现范围

论文第二半独立表含完整230×5个数值格，使用商后 graded 和上述抽象 stacking 类型。
正文明确列出16个没有实际 upper phase/marked square 的群，caption 保留同一限定；
第一半 omega_eff=0 的1150个数值格不作改动。两套物理约定的 JSON 和表格证据分开保存。

完整诊断可由正式归档重复提取：

```bash
python3 scripts/analyze_pip_diagnostics.py results/space_groups_spinless \
  --output results/pip_diagnostics/crystalline_spinless.json
```

脚本默认拒绝不完整230组、混合 source/convention 和不匹配的归档结果哈希。
历史 partial_v1 保留其215群范围；第一半的独立 raw-d3 补证见
[第一半诊断附录](PIP_DIFFERENTIAL_DIAGNOSTICS.md)，没有覆盖旧230结果的 bytes。

论文源已推送 [Overleaf](https://www.overleaf.com/project/68777f2bb9ff9a66a0cbc509)，
commit `c2db7a751ef9970debb47ed83189af6499cc2b1c`，远端 master 已核对一致。
[表格/编译/推送证据](validation_runs/overleaf_spinless_update.json) 保存两套2300格检查、
第一半未变哈希、新表与输入哈希、58页编译和视觉检查记录。
