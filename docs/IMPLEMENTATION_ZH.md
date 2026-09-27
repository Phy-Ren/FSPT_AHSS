# FSPT_AHSS 的计算流程

当前计算固定三维普通空间群、物理 spin-half、无额外 onsite symmetry，
采用 crystalline equivalence 后的 `s = det`、`omega = 0`。
使用完整的无限仿射空间群，保留平移、weak phases 和 atomic fermion parity。

## 一个空间群，一个连续程序

完整入口是 `scripts/run_group.py --mode full`，实际 GAP 入口为
`gap/run_one.g`。每个空间群在同一个 GAP 进程中依次完成：

1. 构造空间群、有限自由分辨率的所需次数、系数作用和链映射。
2. 计算各层分类，保留 cocycle、obstruction、原像、incoming boundary、
   商群坐标以及生成元的选择。
3. 把整个分类对象直接传给 stacking，补齐生成元的 lift，计算幂关系，
   在共同的下层基底中约化，最后对联合关系矩阵做 Smith 化简。
4. 保存分类、stacking、精确有理数数据、证书、源码摘要和耗时。

并行发生在不同空间群之间。分类阶段和 stacking 阶段不跨进程传递几个
群阶后分别运行。开发时保留 classification-only 入口用于回归检查，
所以开发批次可能重复计算同一空间群的分类。

## 独立实现的边界

新程序不加载 SptSet，不包装其谱序列或 stacking 接口。
GAP/HAP、CrystCat、Polycyclic 提供通用群和分辨率基础设施；本项目独立实现
cochain 适配、比较映射、homotopy 修正、分类流程、商群坐标和 stacking。
交付的公式是数学输入。老板及合作者的空间群结果不会进入计算分支。

局部公式的固定系数表与空间群答案表不同：前者只描述普适 cochain 运算，
没有空间群编号，也不预先指定任何群的幸存层或扩张结果。

## 主要的速度改进

* 一次计算矩阵分解后，复用其坐标映射和原像求解器。
* 用有限分辨率上的高阶 diagonal 计算 primary operation，避免重复展开 bar。
* 使用稀疏项、比较映射和 contraction 缓存，并减少群元素的线性查找。
* 只需要上同调坐标时，直接在目标 Smith 对偶链上计算。
* 把本项目的解析公式编译成精确整数标量运算，保留 lift、carry 和符号约定。
* 已由最终 bosonic 商群证明的关系直接使用 Smith 证书。
* 纯 CF 扩张可由 native Gu--Wen doubling 公式计算，并记录其 lift 重建方法。
* 生产任务不重复做完整的 bar 支撑恒等式检查；这些检查保留在 audit 模式，
  原像方程、闭性、incoming 是否落在 kernel 等必要检查仍执行。

优化版和原算法通过同一组 cochain、同一组坐标和实际空间群作比较。
所有运算使用整数、有理数或有限域，不使用浮点容差判断拓扑分类。

## 如何读结果

`0` 表示无限循环因子，`2,4,8,...` 表示有限循环因子的阶。
classification 的四层是 associated graded；完整 stacking 必须读
`stacking.invariants` 和相应的联合 presentation。

证书会区分实际幂关系、native 关系及其重建方法、只确定抽象群的上层证书。
`fullUpperPhaseWitness = false` 的输出不声称给出了完整 p+ip 相位 witness。
自由 p+ip 商的抽象分裂也不意味着任意原始几何代表都是 primitive survivor。
未解决的 obstruction 或扩张不会输出成平凡群。

## 复现和审计

`run_group.py` 在启动 GAP 前冻结运行源码。生产批次也可统一指定 `--source`
使用同一份不可变快照。运行中修改工作目录不会改变已提交任务的算法。
每个任务在 `runs/tasks/` 中保留 stdout、退出状态、CPU 时间和峰值内存。

`scripts/audit_run.py` 在不读取外部答案的条件下检查层群阶与最终群阶、
自由秩、Smith 整数矩阵恒等式、变换矩阵的 unimodularity，以及源码摘要。
`scripts/collect.py` 汇总整批结果；缺失、未解决和失败的任务分别记录。
