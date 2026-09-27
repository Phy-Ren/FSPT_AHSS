# 用独立 S4 物理结果校准 C4 pullback 平方

这项论证将第一半 26 个、第二半 6 个实际保存的上层平方，从“依赖所选通用
Γ 产品的结果”收紧为“可由独立有限物理结果与自然性固定的平方类”。它不推导
一般 p+ip→CF 或 p+ip→bosonic twister，也不改原归档。

这里 `S4` 是 Schoenflies 的四重旋转反射，HM 为 `−4`，抽象群是 `C4`；
不是四字母置换群。物理约定是 crystalline spin-half，对应内部定向反转
生成元的 `C4`、`s` 非平凡、`omega=0`。

## 独立物理输入与非循环性

所供 [Phys. Rev. X 15, 031029 (2025)](https://doi.org/10.1103/PhysRevX.15.031029)
Table I（PDF 第 4 页）给出该 crystalline spin-half S4 全群为 `Z4`。
其 §III B（第 11–13 页）用实空间 block/bubble 构造说明 p+ip 双层与非平凡
0D 复费米子态的关系，独立于本项目所选 Γ 程序。Table III（第 51 页）右侧
internal-spinless panel 给出对应 AHSS 四层 `(P,MC,CF,Bos)=(Z2,0,Z2,0)`。
所审 PDF 的 SHA-256 为
`eda983b3c093877d7b6d34da1092ae8c8c5dc272746e6f4eaf28f35a7438c692`。
这里实空间 block 过滤与 AHSS 过滤并未逐列等同；只用 Table I/物理论证提供
全群输入，用 Table III 及独立的已知下层计算识别唯一 CF 子群。

先完成、冻结后对照的有限输入
[`half_pg10.json`](../../results/point_groups/half_pg10.json)
也给出下层只有一个 `C1`，关系 `2C1=0`，所选候选产品的平方为 `2P=C1`。
它的作用是确认候选平方代表哪个**已知下层类**，不是用自身输出证明物理
全群应为 `Z4`。两种证据的角色必须分开。

## 为什么这足够固定拉回关系

在该通用有限模型中，下层 `H=Z2` 只有一个非零 CF 元 `C`，没有额外 MC 或
bosonic 类。由独立物理全群 `Z4` 可知，任一投到非零 p+ip 商的物理态 `Q`
都满足 `2Q=C`。改选 `Q+C` 也不改变其平方，因为 `2C=0`。因此不需要指定
一般通用产品，就已经固定这个有限模型上的平方类。

对归档中的每个相关空间群，已有实际群同态 `t:G→C4`，并且 `t mod2=s`。
保存的 p+ip 塔就是同一有限完整塔沿 `t` 的拉回：`B,C,nu` 均来自固定的
有限 cochain 表。群上诱导的 stacking 遵从自然性，故

\[
  2\,t^*Q=t^*(2Q)=t^*C.
\]

生产程序的候选平方也严格拉回同一个有限候选平方。这一步可从公式检查：
`AFSStackPipSquare` 使用局部 cup/高 cup、整数 carry、固定坐标变换和整数
gauge，全部与群同态拉回交换。有限候选平方是闭合的、CF 类非零，因此在
唯一的下层 `Z2` 中必等于 `C`。随后空间群自己的下层 gauge reduction 仅
将 `t^*C` 改写成归档的命名生成元坐标。

这证明的是平方的下层群元素，不是候选 Γ 函数等于唯一物理 cochain 函数。
后者可以相差 gauge、坐标选取或其他在此拉回平方上不可见的项。若改选空间群
上层 lift，平方只改变 `2h`；因而同一证据也固定抽象扩张类。

## 归档证书与第二半的背景 gauge

静态程序
[`audit_c4_pullback_calibration.py`](../../scripts/audit_c4_pullback_calibration.py)
读取两个 230 群归档及已经冻结的有限 `−4` 行。它检查保存的 `t` 模二等于
定向、其保存的整数微分为 4 的倍数，以及拉回构造标记；三处归档中
`pip_stacking.g`、`pip_c4_data.g`、`pip_coordinates.g`、`pip_diagonal_data.g`
四个文件的完整冻结字节哈希均相同。它不重新构造分辨率或计算 bar cochain。
`n` 属于 signed integer coefficients，`t` 属于普通整数模四 coefficients，
所以检查两者的**模二**方向数据，不能强求其 native 整数向量逐项相等。

第二半的六行还保存了原 Pin-minus 背景的精确 trivialization。程序用保存的
native differential matrix 逐项验证 `delta lambda=omega`；完整 bar primitive
的 reconstruction recipe 包含 comparison homotopy。改变 fermion extension
的 section 给出物理背景等价，故可在已保存的 `omega=0` gauge 中应用同一
`C4` 校准。这里没有声称已经把所有生成元 cochain 展开回原始 Pin-minus
坐标；经校准的关系正是在归档使用的零背景 gauge 中。

详细逐群证据在
[`c4_naturality_calibration.json`](../../results/upper_carry_scope/c4_naturality_calibration.json)。
论证仍采用本项目的 crystalline equivalence、已知下层识别和物理 stacking
自然性；不把一次数值闭合检查当作这些物理原则的推导。

## 精确适用名单与剩余范围

第一半 26 群：
`7,9,27,30,32,33,34,37,43,81,82,103,104,106,112,114,116,117,118,122,158,159,161,184,218,220`。

第二半六群：`7,9,33,158,159,161`。这六群的原背景均已精确 trivialize；
其归档最终平方为零，含义是 `t^*C` 在这些空间群的下层商中为零，不是原始
通用 twister 为零。

仍未由此校准的第一半六群是
`29 Pca2_1, 41 Aba2, 45 Iba2, 110 I4_1cd, 120 I−4c2, 219 F−43c`；
第二半还有 `29 Pca2_1`。它们保留所选 Γ 产品下实际计算的关系；本证书未将
其提升为独立物理校准。未来其他有限模型、自然性关系或直接物理论证可能
进一步固定它们，不能说它们原则上一定需要完整通用 twister。

第二半另有 16 行从完整 carry fiber 得到唯一抽象群而未给出 marked 平方，
其结论与本项 `C4` 校准分开；见
[`UPPER_CARRY_SCOPE_ZH.md`](UPPER_CARRY_SCOPE_ZH.md)。
