# p+ip 上层 carry：哪些量已算出，哪些量仍未确定

这份说明区分**既定公式下的计算结果**与**公式是否已唯一确定物理 stacking**。
两个归档共有 460 行抽象群结果；其中 16 行没有给出具体的上层 carry，
但对全部允许 carry 的整数关系计算均给出同一个抽象群。其余行中保存的
“actual upper witness”表示实际构造、计算了**所选产品公式下**的 cochain
和关系，不能仅凭闭合性将该产品认定为唯一物理 stacking。随后已通过独立
S4 物理结果与自然性校准第一半 26 个、第二半 6 个平方类；其证明与剩余范围
见 [`C4_NATURALITY_CALIBRATION_ZH.md`](C4_NATURALITY_CALIBRATION_ZH.md)。

本报告不修改原归档。独立静态复核程序是
[`report_upper_carry_scope.py`](../../scripts/report_upper_carry_scope.py)，
完整逐群记录是
[`presentation_audit.json`](../../results/upper_carry_scope/presentation_audit.json)。
它校验两个归档全部 460 个结果文件的 SHA-256 和 source ID，只重算小整数
关系矩阵的 Smith 型，不运行 GAP 或 cochain 计算。群名使用公开的纯名称目录 [`space_group_names.json`](../../fspt/data/space_group_names.json)，没有运行时第三方表格依赖。

## 16 个未知 carry 为什么不妨碍抽象群型

令 `H` 为已经算完的 MC、CF、bosonic 下层 stacking 群，`P` 为阶二商中的
p+ip 生成元。给定第一乘积规范确定

\[
 2P=b+u,\qquad u\in F_1H,
\]

其中 `b` 的 MC 投影已知，`F1H` 是 CF 与 bosonic 层生成的子群。
改选 `P+h` 将右边改成 `b+u+2h`，所以相关的代数扩张类由
`b + image(F1H -> H/2H)` 描述。我们枚举这个**完整有限像**，不是只试零
carry，也不是只凭 MC 投影非零作判断。

下表的 `Bi`、`Ci`、`Di` 分别是该行归档中的 MC、CF、bosonic 生成元，
不同群的同名生成元没有跨群同一性的含义。`b` 表示 `2P` 模掉 CF/bos 后的
代表，**不是完整实际关系**。最后一列列出在 `H/2H` 中独立的未知方向；
每个方向只需取 0 或 1。`Z_n` 表示阶 `n` 的循环群。

| SG | 名称 | 下层群 H | 已知 b | 完整抽象群 | 不同扩张类数 | 独立未知方向 |
|---:|---|---|---|---|---:|---|
| 6 | Pm | Z₂⁹ + Z₈² | B1 | Z + Z₂⁹ + Z₈ + Z₁₆ | 32 | D3,C3,C4,C5,C6 |
| 8 | Cm | Z₂⁶ + Z₈ | B1 | Z + Z₂⁶ + Z₁₆ | 8 | D2,C2,C3 |
| 28 | Pma2 | Z₂⁹ + Z₈ | B2 | Z₂⁹ + Z₁₆ | 32 | D2,C2,C3,C4,C5 |
| 30 | Pnc2 | Z₂⁶ | B1 | Z₂⁵ + Z₄ | 8 | D1,C1,C2 |
| 31 | Pmn2₁ | Z₂⁶ + Z₈ | B1 | Z₂⁶ + Z₁₆ | 8 | D1,C2,C3 |
| 32 | Pba2 | Z₂⁶ | B1 | Z₂⁵ + Z₄ | 8 | D1,C1,C2 |
| 34 | Pnn2 | Z₂⁶ | B1 | Z₂⁵ + Z₄ | 8 | D1,C1,C2 |
| 40 | Ama2 | Z₂⁷ + Z₈ | B1 | Z₂⁷ + Z₁₆ | 16 | D1,C2,C3,C4 |
| 41 | Aba2 | Z₂⁵ | B1 | Z₂⁴ + Z₄ | 4 | D1,C1 |
| 43 | Fdd2 | Z₂⁴ | B1 | Z₂³ + Z₄ | 4 | D1,C1 |
| 156 | P3m1 | Z₂⁵ + Z₈ | B1 | Z₂⁵ + Z₁₆ | 8 | D1,C2,C3 |
| 157 | P31m | Z₂⁵ + Z₂₄ | B1 | Z₂⁵ + Z₄₈ | 8 | D1,C2,C3 |
| 160 | R3m | Z₂⁵ + Z₈ | B1 | Z₂⁵ + Z₁₆ | 8 | D1,C2,C3 |
| 174 | P−6 | Z₂² + Z₆ + Z₂₄² | B1 | Z + Z₂² + Z₆ + Z₂₄ + Z₄₈ | 8 | D1,C3,C4 |
| 188 | P−6c2 | Z₂⁴ + Z₈ | B1 | Z₂⁴ + Z₁₆ | 8 | D1,C2,C3 |
| 190 | P−62c | Z₂⁴ + Z₂₄ | B1 | Z₂⁴ + Z₄₈ | 8 | D2,C2,C3 |

共 176 个不同的 fixed-lower 扩张类，独立重算全部得到各行所列的同一群型。
因此每一行都可以选 `u=0` 写出一个**正确抽象群的展示模型**。
这不等于物理 carry 为零，也不等于已找到保留原下层生成元的变换将真实 carry
归零。事实上，每一行的未知像均非零；只用 `P -> P+h` 通常不能消掉它。
若要求命名生成元的实际相乘结果，仍需上层产品输入或独立校准。
原归档因此保留 `fullUpperPhaseWitness=false`，marked stacking API 拒绝这 16 行。

上述结论以给定第一 p+ip 乘积规范及已经计算的下层群为条件；并不由本表证明
该第一乘积的物理唯一性。自由 p+ip 部分使用已经确定的存活整数格，因自由
阿贝尔商的扩张抽象分裂而贡献 `Z` 因子；这也不等于所有相关 cochain twister 为零。

## 第一半 12 个 CF、5 个 bosonic 非零最终关系说明什么

以下关系来自 crystalline spin-half 归档的**所选校准产品**，并已包括输入/输出
坐标变换、整数层 gauge、下层 incoming gauge 和最终关系约化。
它们不是原始 twister 的逐项列表。

| SG | 保存的最终 2P 关系 | 单独删除 bosonic 坐标是否改变抽象群 | bosonic 差是否属于 2H |
|---:|---|---|---|
| 81 | C1 | 无 bosonic 项 | — |
| 82 | C1 | 无 bosonic 项 | — |
| 112 | C1 + D2 + D6 + D8 | 不变 | 否 |
| 114 | C1 + 2D1 | 不变 | 是 |
| 116 | C1 | 无 bosonic 项 | — |
| 117 | C1 | 无 bosonic 项 | — |
| 118 | C1 + 2D5 | 不变 | 是 |
| 120 | C1 | 无 bosonic 项 | — |
| 122 | C1 + D1 | 不变 | 是 |
| 218 | C1 | 无 bosonic 项 | — |
| 219 | C1 | 无 bosonic 项 | — |
| 220 | C1 + 2D1 | 不变 | 是 |

保持下层关系不变而直接将这 12 行的最终关系改成 `2P=0`，12 行的抽象群都会
改变。这只否定了“随意删掉最终关系”的做法，**没有证明把原始 twister 设零会
得到这个删项结果**。即使某个原始产品项为零，坐标变换和 gauge 也可能产生
非零最终 CF/bosonic 项。

单独删掉五行的最终 bosonic 坐标均不改变抽象群。四行的差在 `2H` 中，
在抽象扩张层面可以改选 `P` 吸收；SG112 的差不在 `2H` 中，虽抽象群型相同，
固定下层标记的扩张类却不同。两种情况都不能反推原始 bosonic twister 为零。

## “实际算了上层关系”的数学输入范围

第一半的 32 个 torsion p+ip 上层关系、第二半另外 7 个上层关系采用了所供
collaborator 代码中的选定通用产品。具体来源是参考 revision
`c2961a2d6` 的 `python/stacking_model/production_gamma4.py` 与
`v1_pair_shared.py`。前者通过固定 universal chain contractor 及选定的两个
小胞腔相位系数 `(+1/8,-1/8)` 定义产品；它自己的开头还注明
“Symmetry is not yet asserted here.”

来源文件 SHA-256 分别为
`8bf3d4f19ebadef5fb80854c17bf817b43ebbab1845b965e2e9923c28e709759` 与
`51f09cbb4fa3bbdec1715991a4efb1223b10bec07ad10a2e0178b6fd205aa447`，
这些哈希仅标识所供数学产品的来源；本说明不再分发第三方源码。
本项目的 [`derive_pip_diagonal.py`](../../tests/derive_pip_diagonal.py)
以该数学产品作为推导阶段的 oracle，编译出 `n=n'=s, omega=0` 的通用对角
公式；生产程序加载独立生成的数据和 GAP 实现，不调用参考引擎或答案表。

已完成的检查证明：转录/坐标运输与该选定公式相符，所得状态满足所检验的
cochain 方程，保存的实际关系与 Smith 展示相符，并通过若干实际 lift 选择
与有限模型控制。**这些检查不构成通用物理 stacking 的唯一性或完整 coherence
证明。**给定手稿的 `05b_pip.tex` 也将第一乘积称为候选，并明确指出闭项不由
微分恒等式固定。有限模型的来源比较另保留 `certified_ko=false` 的范围限制。

因此不能用“已有 460 个数值结果”回答“所有物理 twister 都已知道”。较准确的
说法是：已完成给定数学模型下的两套 230 群计算；16 行的抽象群对所允许的未知
CF/bosonic carry 完全不敏感；使用选定上层产品的行还应说明产品输入及校准范围。
如果撤回这两种上层产品、只保留下层群和 leading MC 数据，第一半全部 32 个
torsion 行都存在非零的代数 carry 歧义像，包括所选模型中 `2P=0` 的 20 行。
但不能据此声称每个代数选项都由自然且 coherent 的物理产品实现。

还需区分“任意改变最终 Ext 类”与“只改变通用纯整数 source contractor”。
后者在 `n=n'=s, omega=0` 的 CF 对角上，若差确为仅依赖这些输入的自然闭操作，
只能拉回到 `s^3` 型项，而合法塔有 `dB=s^3`。因此它的 CF 类可以为零；
是否连相应顶层相位差也被 gauge 消去，需要另行证明，不能直接从上面的
代数候选数推出。这一更窄的 normalization 问题仍应与物理校准分开核查。

第一半有 26 个实际保存的 p+ip 塔是有限 `C4` 定向角色的 pullback；其余为
SG `29,41,45,110,120,219`。现在已利用独立发表的 S4 物理结果、唯一非零下层
CF 类及 stacking 自然性固定这 26 个平方类，另覆盖第二半六个背景精确
trivialize 的同类 pullback。此校准并非使用本项目有限结果循环证明自身，
也不推导通用 Γ。第一半六群和第二半 SG29 仍只具有所选产品下的实际关系，
尚未被这个校准论证涵盖。具体输入、逐群角色和 gauge 证书见上面的校准说明。

## 复核命令与证据范围

```sh
python3 scripts/report_upper_carry_scope.py
```

该命令独立枚举 16 行共 176 个 carry 类，检查全体 Smith 型，同时核对第一半
12 个非零最终关系的删项反事实。它不修改任何原始群结果，不把删项反事实作为
新的物理分类，也不重新检查 bar-cochain 方程。

## 非零 p+ip 的完整分组名单

下列按两种物理约定分别计行，同一个 SG 在两个约定中是两次计算。

| 约定 | 含自由 p+ip | 含 torsion p+ip | 二者都有 | 非零 p+ip 并集 | p+ip 为零 |
|---|---:|---:|---:|---:|---:|
| crystalline spin-half | 44 | 32 | 4 | 72 | 158 |
| crystalline spinless | 44 | 23 | 5 | 62 | 168 |
| 共 460 行 | 88 | 55 | 9 | 134 | 326 |

自由 p+ip 不算少，但它与阶二上层关系是两类问题。实际存活整数格的基可以选完整相，
整数倍没有有限阶平方关系，因此抽象群分裂出 `Z` 因子；这不表示原始 twister 为零。

### crystalline spin-half

**仅自由 p+ip（40 群）：** 1 P1；2 P−1；3 P2；4 P21；5 C2；6 Pm；8 Cm；10 P2/m；11 P21/m；12 C2/m；13 P2/c；14 P21/c；15 C2/c；75 P4；76 P41；77 P42；78 P43；79 I4；80 I41；83 P4/m；84 P42/m；85 P4/n；86 P42/n；87 I4/m；88 I41/a；143 P3；144 P31；145 P32；146 R3；147 P−3；148 R−3；168 P6；169 P61；170 P65；171 P62；172 P64；173 P63；174 P−6；175 P6/m；176 P63/m。

**仅 torsion p+ip（28 群）：** 27 Pcc2；29 Pca21；30 Pnc2；32 Pba2；33 Pna21；34 Pnn2；37 Ccc2；41 Aba2；43 Fdd2；45 Iba2；103 P4cc；104 P4nc；106 P42bc；110 I41cd；112 P−42c；114 P−421c；116 P−4c2；117 P−4b2；118 P−4n2；120 I−4c2；122 I−42d；158 P3c1；159 P31c；161 R3c；184 P6cc；218 P−43n；219 F−43c；220 I−43d。

**自由和 torsion 都有（4 群）：** 7 Pc；9 Cc；81 P−4；82 I−4。

### crystalline spinless

**仅自由 p+ip（39 群）：** 1 P1；2 P−1；3 P2；4 P21；5 C2；10 P2/m；11 P21/m；12 C2/m；13 P2/c；14 P21/c；15 C2/c；75 P4；76 P41；77 P42；78 P43；79 I4；80 I41；81 P−4；82 I−4；83 P4/m；84 P42/m；85 P4/n；86 P42/n；87 I4/m；88 I41/a；143 P3；144 P31；145 P32；146 R3；147 P−3；148 R−3；168 P6；169 P61；170 P65；171 P62；172 P64；173 P63；175 P6/m；176 P63/m。

**仅 torsion p+ip（18 群）：** 28 Pma2；29 Pca21；30 Pnc2；31 Pmn21；32 Pba2；33 Pna21；34 Pnn2；40 Ama2；41 Aba2；43 Fdd2；156 P3m1；157 P31m；158 P3c1；159 P31c；160 R3m；161 R3c；188 P−6c2；190 P−62c。

**自由和 torsion 都有（5 群）：** 6 Pm；7 Pc；8 Cm；9 Cc；174 P−6。
