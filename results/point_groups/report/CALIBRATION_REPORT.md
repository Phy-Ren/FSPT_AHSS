# 两套32有限点群：独立校准及文献差异

本轮从真正的三维有限矩阵点群分别计算两种物理自旋，共64个输入、320个数值格（四个过滤层和完整 stacking 群）。没有把无限空间群的代表行当作点群答案。统一源码为 `8fceb2f5f3bcaa9205c00962cd2c7c78b493a45f583fb090f246e7ce1637f297`；原始结果、任务及64/64独立几何及代数证据审计保存在上一级目录。本报告是归档之后生成的派生文件，不属于 `archive.json` 原始数值 payload。

结论是：**64组全部与提供的旧稿表一致；发表论文有三个群、四格差异。** 因而不能说本轮与发表论文全64一致。两个差异可由保留实际符号作用和 Pin 背景的群收缩独立检验；另一个涉及已知 lower stacking 的非平凡扩张。

- [完整64行四层和全群 CSV](classification_stacking_64.csv)
- [32行、两物理约定全群表](FULL_STACKING_32.md)
- [逐格比较及哈希 JSON](reference_comparison.json)
- [两个奇阶核收缩的有限表/背景证书](odd_kernel_retractions.json)

## 约定与比较范围

| 物理约定 | 内部反幺正符号 | 内部中心扩张 |
|---|---|---|
| crystalline spin-half | `s=w1=det` | `omega=0` |
| crystalline spinless | `s=w1=det` | `omega=w2+w1²`，实际三维表示的 Pin-minus 类 |

`det` 在二元符号记法中为 `(1-det R)/2`。比较键采用物理自旋及几何 HM/Schoenflies 名；`C3i=S6` 仅作名称别名。没有按群序号或抽象有限群同构强配。例如 `Ci` 与 `Cs` 虽同为抽象 `C2`，其几何背景不同；旧稿的 `O/Td` 两表行号还互换，不能按行号拼表。

引用的完整发表答案是 Jian-Hao Zhang、Shang-Qiang Ning、Yang Qi、Zheng-Cheng Gu，*Construction and Classification of Crystalline Topological Superconductor and Insulators in Three-Dimensional Interacting Fermion Systems*，**Physical Review X 15(3), 031029 (2025)**，发表于2025-07-28，[DOI:10.1103/PhysRevX.15.031029](https://link.aps.org/doi/10.1103/PhysRevX.15.031029)。Table III（PDF第51页）右栏 internal spinless 对应 crystalline spin-half，左栏反之；这里逐列比较的是它的 AHSS 层。Table I（PDF第4页）采用 real-space block 过滤，不能把其三列逐项当作本程序四列，不过完整群可以比较。

提供的 PDF SHA256 为 `eda983b3c093877d7b6d34da1092ae8c8c5dc272746e6f4eaf28f35a7438c692`。元数据和数值转录来自本地提供文件，没有外部抓取或执行参考分类代码。完整参考在读取新64结果之前冻结；冻结清单 SHA256 为 `82428dbd5da4a95b387590804b4ea513cc2329bda5fa13991d1d927329468400`。第三方 PDF、原稿和原始旧日志私下保留，未复制到本公开报告目录。

## 完整比较

| 参考 | crystalline spin-half | crystalline spinless | 范围 |
|---|---:|---:|---|
| PRX Table III | 160/160格一致 | 156/160格一致 | 全64四层及全群 |
| 提供的旧 manuscript 表 | 160/160格一致 | 160/160格一致 | 全64四层及全群；历史稿，并非统一源码运行证书 |
| 预冻结旧日志保存值 | 156/156次观察一致 | 117/117次观察一致 | 去重后分别155、114格；缺失不填补，重复/人工恢复记录分开 |
| Weicheng有限C2记录 | 4/4标签一致 | 4/4标签一致 | 仅4个不同物理输入的full值，不是32×2四层表 |

最后一行的八个标签重复描述四种 `(s,omega)` 的有限 `C2` 模型；应计四个输入，不能增加为八个独立校准。对应本轮的 `C2/Cs × 两自旋`。提供的老板材料是 affine230第一约定四层项目，没有找到独立有限32×2答案；Weicheng当前提供的checkout同样没有完整32×2表。

PRX的四层合计为255/256格一致，full为61/64格一致。全部差异都在 **crystalline spinless / internal spin-half**：

| 点群（HM） | 项目 | PRX Table III | 本次独立结果 | 旧稿 |
|---|---|---|---|---|
| S4 (`-4`) | full | `Z2 × Z2` | `Z4` | `Z4` |
| D3d (`-3m`) | full | `Z2 × Z2 × Z2` | `Z8` | `Z8` |
| C3h (`-6`) | p+ip层 | `0` | `Z2` | `Z2` |
| C3h (`-6`) | full | `Z8` | `Z16` | `Z16` |

这不是 Table I 到 Table III 的孤立转录错误：Table I 的 crystalline spinless full 也分别给上述旧值。旧稿全文原先只提及 S4 的文献差异，没有完整解释另外两例。旧 `C3h/C3v` 说明记录其表格修改来自用户物理判断，当时自动程序在 p+ip d4 上报错；不能把该修改算作一次独立完成的数值运行。

旧日志也不是一个无冲突真值表。冻结的主日志/恢复记录有上述273次一致观察，但另外两个 C4v 实验采用不同历史版本，下层 full 分别为 `Z2²×Z4` 与 `Z2⁴`，前者与本次不同、后者相同；两条都保留，没有选择性删除。读取新64之后，又在旧 package 的另一 jobs 目录找到 D3d 完整日志，五格均同（总群 `Z8`），这被明确记为**事后发现的历史补证**，没有加进预冻结总数。

## C3h：mirror retract 排除旧 Z8

实际点群 `C3h=C3×Cs` 存在到 mirror `Cs` 的商与截面。证书从已归档有限乘法表找出 normal `C3`，构造 `q:G→H`、`j:H→G`，逐一验证所有乘法及 `qj=id`；它同时验证符号严格匹配，并解出规范共链 `lambda`：

```
omega_G(g,h) + omega_H(qg,qh) = lambda(g)+lambda(h)+lambda(gh) mod2.
```

在实际费米子中心扩张上定义

```
Q(a,g)=(a+lambda(g),qg),
J(a,h)=(a+lambda(jh),jh).
```

两者是带符号的群同态，且 `QJ=id` 严格成立；所以完整 stacking 的自然 pullback `q*` 为分裂单射，而不只是抽象群名相同。PRX本身给 crystalline spinless mirror `Cs` 的群为 `Z16`，因此 C3h 必须容纳一个 `Z16`，无法是 `Z8`。mirror的非零 p+ip leading 类也在拉回后保持非零，因为 `q*s=s`，从而指出旧表缺失的 p+ip 层。

这项收缩证书单独证明的是注入/下界；“完整群恰为 Z16”还使用本次完整四层计算。它没有构造未知的实际 upper marked square。本例是整个允许 upper-extension fiber 抽象同型唯一的三例有限点群之一。

## D3d：C2h retract 排除三个独立 Z2

实际 `D3d=S3×Ci` 的 normal `C3` 商为 `C2h`，并有 Sylow2 截面。相同证书验证实际乘法、符号和 Pin 背景的规范等价，而非只使用抽象 `S3×C2` 的名称。

PRX自身给 crystalline spinless `C2h` 为 `Z8`；分裂注入要求 D3d 也有阶8元素，故不能是所有元素阶至多2的 `Z2³`。本次三层各一个 `Z2`、没有 p+ip，保存的生成元依次为 bosonic `D`、CF `C`、MC `B`，其实际关系是

```
2D=0,  2C=D,  2B=D+C.
```

因此 `B` 的阶为8。这是已知 lower 共链公式的扩张；**与未知 p+ip→CF/bosonic twister 无关**。收缩与论文已知 C2h 给出的独立阶数约束也支持非平凡 lower 扩张。

## S4：已知 lower MC→bosonic 扩张

这里的 `S4` 指四重旋转反演点群（HM `-4`，抽象 `C4`），不是四字母对称群。crystalline spinless 的 p+ip 已在 d2 被阻碍，CF最终为零。实际 lower 群仅有 bosonic `D` 和 MC `B`：

```
2D=0,  2B=D.
```

保存的关系矩阵（生成元顺序 `D,B`）为 `[[2,0],[-1,2]]`，Smith群为 `Z4`。换 MC lift 为 `B+aD` 不改变 `2B`，因为 `2D=0`；故这种扩张不能用代表规范变更抹掉。CF为零也不阻止 MC直接扩张到bosonic。

PRX §III B.4（PDF第12页）给出 crystalline spinless 两个 real-space root 后直接总结 `Z2²`。同节之后对**另一物理自旋**的 p+ip→0D 扩张做了详细推导（第12–13页），这段不能当作本例 MC→bosonic 的证明。提供的旧 debug 笔记早已记录三条计算路径均给本例 `2MC=Bos`、`Z4`；旧 `notes.md` 的 `Z2²` 标注则来自外部文献，后续笔记明确指出它不是旧程序算出的结果。

另一次加强控制关闭 compiled CA、mod2 contraction、mod2 bar、closed-CF half-phase 与 projected cup0 优化，使用完整 bar 模型，穷举所有非退化元组上的平坦性、ordered generator products、literal squares 和 reduction gauge 等式：degree2/3/4/5 分别18、270、810、1458项通过，仍得到 `2B=D, 2D=0`，保存的 lower witnesses 与正式结果相同。S4、D3d、C3h 三例也分别开启实际 comparison-support 检查，原始数学字段/native witnesses 全同，只增加核验标志及计时。证据见 [marked audit comparison](../../optimization_validation/point_group_backend/marked_audit/comparison.json)，SHA256 `3a49426ce7b5a7f9000976f1a3313589d49918f21c15d6b2faf10c9c5299b2c5`。这些控制仍不把 C3h 的未知 upper carry 变为 actual witness。

因此这里应保留“新程序给出有标记证书的非平凡 lower 扩张、与发表的 real-space full 结论不同”的准确结论。历史代码一致不是独立物理证明；单靠本轮表格吻合也不能判定论文具体哪一步遗漏。它确实不涉及本项目尚未知的 p+ip 高层 twister。

## 数学边界

本轮64个 **abstract** full群都确定。crystalline spinless 的 **Cs、C3v、C3h** 三个有限输入尚无 actual upper phase/marked square，采用给定第一整数层乘积 normalization 下整个允许的扩张类集合 的同构型唯一性；不能由表格数值一致推出这些实际 carries 已知或为零。其余条目的保存证书范围以原始 JSON 为准。

这与先前空间群的16例是不同的索引集合。旧460个空间群 JSON 没有被本次校准改写；其 H1 outgoing d3/d4、H0 incoming identification 和高层 product 物理选择仍需按各自已保存的范围表述。特别是“某CF类被 H0 incoming d3 等同为零”不等于“p+ip H1候选在 outgoing d3 被阻碍”。

第一约定的真实 `S4`/`C4` 物理校准及其对26+6空间群自然性的适用范围另见 [C4自然性校准说明](../../../docs/case_reports/C4_NATURALITY_CALIBRATION_ZH.md)。这不应与上述 crystalline spinless 的 S4 lower 差异混淆。
