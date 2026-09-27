# 460 个空间群算例中，p+ip 的 d3、d4 到底做了什么

编号均为国际空间群号 SG1–230。两套约定是：crystalline spin-1/2 对应
internal spinless、`omega=0`；crystalline spinless 对应 internal spin-1/2、
`omega=w2+w1²`。这里的 differential 是 classification 的障碍/等价关系，
不能和 stacking 的第三、第四阶 twister 混为一谈。

## 真正阻止 p+ip decoration 存活的 outgoing 障碍

两套 230 群中，**没有候选在处理允许的低层调整之后被 d3 或 d4 杀掉**。
被排除的候选都在 d2。初次选的低层代表产生非零障碍、后来换代表消掉，
不应计作非零终端 differential。

| 初始障碍非零，但最后可消除 | crystalline spin-1/2 | crystalline spinless |
|---|---|---|
| torsion p+ip 的初始 d3 | 32, 34, 45, 110, 112, 114, 116, 117, 118, 120, 122, 218, 219 | 30 |
| free p+ip 候选的初始 d3 | 8, 84, 86, 88 | 5, 176 |
| free p+ip 候选的初始 d4 | 84 (P4₂/m) | 83 (P4/m) |

最后一行两例的存活自由格均为 `2Z`。并不是说 primitive 的一个 p+ip 已存活。
表中列的是实际记录的非零初始类；不少其它候选因目标群为零或没有二初级部分，
已经可以证明最终 d4 为零，无须计算原始共链。因此不能进一步声称其它所有
原始 d4 共链都恒为零。

## 确实改变 CF classification 的 incoming d3

这里是另一件事：p+ip 层的边界让一个本来看似非平凡的 CF 相成为平凡相。
它没有杀掉一个 H1 p+ip decoration，而是在下层分类中建立等价关系。

- crystalline spin-1/2：这类 incoming d3、d4 都没有非零像。
- crystalline spinless：22 个群各去掉 CF 层的一个 `Z2`；incoming d4 没有非零像。

这 22 群为：

`16, 21, 22, 23, 89, 90, 93, 94, 97, 98, 177, 180, 181, 195, 196, 197, 207, 208, 209, 210, 211, 214`。

| SG | 名称 | SG | 名称 |
|---:|---|---:|---|
| 16 | P222 | 180 | P6222 |
| 21 | C222 | 181 | P6422 |
| 22 | F222 | 195 | P23 |
| 23 | I222 | 196 | F23 |
| 89 | P422 | 197 | I23 |
| 90 | P4212 | 207 | P432 |
| 93 | P4222 | 208 | P4232 |
| 94 | P42212 | 209 | F432 |
| 97 | I422 | 210 | F4132 |
| 98 | I4122 | 211 | I432 |
| 177 | P622 | 214 | I4132 |

它们也是 incoming d2 非零的 52 群的子集。同一个下层边界的实际阶为 4，
同时影响 MC 与 CF 两层；不能只看它的 MC 部分就停止计算。d4 为零经过完整
过滤关系格检查，不能单凭该边界的阶不超过 4 推断。

## 原始证据

- [spin-1/2 诊断](../../results/pip_diagnostics/crystalline_spin_half.json)
- [spin-1/2 三例补证](../../results/pip_diagnostics/crystalline_spin_half_d3_supplement.json)
- [spinless 诊断](../../results/pip_diagnostics/crystalline_spinless.json)
- [stacking 未知项的另一个问题](UPPER_CARRY_SCOPE_ZH.md)

SG84 的初始 d3 来自单独补跑；旧归档缺少该字段，原字节没有被改写。补跑还
补全 SG103、104，并确认原结果及保存的原生共链向量不变。本说明不重新解释
或覆盖任何失败、超时任务。
