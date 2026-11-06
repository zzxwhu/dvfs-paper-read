---
title: "04 把下一批 token 的需求变成一个可执行的频率请求"
date: "2026-11-07"
tags: [DVFS, E902]
---

[返回五篇实验手册](guide.md) · [论文原文](https://arxiv.org/abs/2609.13153v1) · [所用版本PDF](https://arxiv.org/pdf/2609.13153v1)

**DVFS for Small Language Model Inference on Mobile Edge Devices**  
Jiesong Chen, Lixiang Han, Jiani Cao, Zhaoxi Yue, Zhenjiang Li。arXiv2609.13153v1，16页；首页版本标2026-07-08，与编号月份不同，按所用PDF记录，不自行改日期。

一个字还没生成，下一步工作量从哪里来？SLM 每多生成一个 token，上下文会增长。模型的层数、隐藏维度和当前上下文长度，在运行下一步以前就已知。作者用这些信息描述下一步涉及的矩阵尺寸。读取“下一步运行完才产生的计数器”会把答案提前泄漏给控制器。

![Fig3 系统架构](images/dvfslm2026-fig3.png)

[放大原图表](images/dvfslm2026-fig3.png) · [原文 Fig3，PDF 第 4 页](https://arxiv.org/pdf/2609.13153v1#page=4)。图表来自该论文作者。

## 把系统拆成三个可单独检查的计算

**第一步，预测负载特征。** 离线执行不同上下文和配置，采硬件性能计数器，比如访存活动。用矩阵运算规模训练 XGBoost，让它把决策时已知的信息映射为预计的硬件特征。运行时查询模型，省去对尚未执行的任务读计数器这件做不到的事。

**第二步，把特征变成时间和能量。** 对每个候选 GPU、EMC（内存控制器）频率组合，预测每 token 平均功率与时延。论文把频率的三次项用于刻画功率变化，把频率倒数用于刻画延时变化，然后用剖析数据拟合参数。CPU 先扫出继续升频收益很小的阈值，实验采用 0.6528 GHz。这样 AGX Orin 每次只比较 44 组 GPU/EMC，Orin NX 比较 28 组。预测能量等于预测功率乘预测时间。

![Algorithm1 剪枝搜索](images/dvfslm2026-algorithm1.png)

[放大原图表](images/dvfslm2026-algorithm1.png) · [原文 Algorithm1，PDF 第 8 页](https://arxiv.org/pdf/2609.13153v1#page=8)。图表来自该论文作者。

**第三步，先筛时限，再选能量。** 用户要求 20 token/s，单 token 预算就是 50 ms。教学例中，A 档预测 45 ms、6 W，B 档 36 ms、8 W。起初两者都可行，A 的 270 mJ 小于 B 的 288 mJ。若上一窗口实际总时间比预测多 20%，给下一窗口乘 1.2 的校正因子后，A 是 54 ms，B 是 43.2 ms，应选 B。若没有任何可行档就转入尽力而为模式，并记录一次不可行。程序默认每 50 token 选一次，prefill 则优先用高 GPU/EMC 频率。论文按 EMC 分组剪枝以减少搜索时间，初版建议保留穷举版，逐窗口比较剪枝结果与穷举解。

## 原文结果的两个分母

![Fig8 Fig8＋Fig9：能量与QoS成对阅读](images/dvfslm2026-fig8.png)

[放大原图表](images/dvfslm2026-fig8.png) · [原文 Fig8，PDF 第 10 页](https://arxiv.org/pdf/2609.13153v1#page=10)。图表来自该论文作者。

左侧读能量，右侧读相同模型、相同目标速率的 QoS。其定义为 min(实际速率/目标速率, 1)。例如 40 对 80 token/s 得 50%，即平均生成速率只达到目标一半。它无法告诉你有多少 token 超过各自期限。作者测得相对内置规则每 token 能量最高降低 12.4%，相对改造的 GearDVFS 最高降低 8.4%。在部分紧期限工况，Gear 耗能更低的同时 QoS 也更差。复建时应把两个指标画成同一张散点图。

![Table3 离线profiling成本](images/dvfslm2026-table3.png)

[放大原图表](images/dvfslm2026-table3.png) · [原文 Table3，PDF 第 13 页](https://arxiv.org/pdf/2609.13153v1#page=13)。图表来自该论文作者。

## 怎样复建这一篇

1. **离线数据。** 固定设备、量化方式和模型。主要负载含 GPT2-large、Qwen2.5-0.5B、TinyLLaMA，另有 MoE。每次保存 context、矩阵规模、HPC、实际频率组合、时间和平均功率。按上下文区间和完整运行分割训练/测试，避免相邻 token 随机拆分让误差虚低。保存估计器的平均误差以及最危险的延时低估。
2. **无硬件验证。** 先用查表实现精确枚举，再替换预测器。单独测试截止时间刚好相等、全部不可行、α突然上升、某个 EMC 档预测不再单调四种情况。若剪枝解和穷举解不一致，先退回穷举定位。验证 α 所用的全部样本均来自已经结束的窗口。
3. **原设备复建。** 两种 Orin、llama.cpp q4_0、Perf/CUPTI 离线剖析、INA3221 以 200 Hz 采样。主实验生成 1024 个 token，每组 5 次，报告均值与 95% t 区间。比较相同硬件与动作集下的 RULE、加入 deadline reward 并训练后冻结的 Gear、DVFSLM。另测不同窗口、控制开销、并发干扰和不可达目标。
4. **算回成本。** Table 3 给出 GPT2-large 单模型标定 27.28 小时、0.33 kWh。教学换算为约 1188 kJ；若每个 token 实际净省 0.05 J，约需 2376 万个 token 才摊平这笔标定电能。0.05 J 是示例假设。迁移到 E902 可以换成“下一块输入的字节数→预测周期→枚举合法档”，保留同一套验证方法，重新测每档数据。

## 摘要改写与复建资料

从下一token的矩阵计算规模预测硬件元数据，再用轻量功率/延时模型在deadline下搜索GPU与EMC频率。每token能量：相对RULE最高−12.4%，相对改造Gear最高−8.4%，条件为模型/期限不同；某些高目标下Gear更省能但QoS差，不能脱约束比较。

DVFSLM models upcoming SLM token workloads through matrix-operation structure and an offline learned metadata parser. Lightweight latency and power estimators drive a pruned GPU–EMC frequency search, with the CPU fixed at an empirically selected threshold. Window-level feedback corrects latency bias, and energy-per-token results are assessed together with a capped rate-based QoS metric. This is a reader-written paraphrase, not the original abstract.

**代码与复现边界**　当前材料中尚未定位齐完整控制器源码、实验脚本和原始重复数据；这不表示这些材料不存在。

[完整编号图表索引](../dvfslm2026/figs_notes.md) · [原四报告中的技术笔记](../dvfslm2026/paper_notes.md) · [配套核算脚本](https://github.com/zzxwhu/dvfs-paper-read/blob/main/examples/focus-five/check_examples.py)
