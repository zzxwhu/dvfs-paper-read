# DRQN Governor：中英文摘要与章节导读

[论文页面](https://doi.org/10.1109/TNSE.2021.3123280) · [本笔记所用 PDF](https://coladog.github.io/assets/papers/TNSE2021.pdf) · [DOI](https://doi.org/10.1109/TNSE.2021.3123280)

整理日期：2026-11-05。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

A recurrent Q-network uses frequency and CPU-utilization history to choose CPU operating frequencies for application-specific timing targets. Inference runs in the Linux kernel, while training uses collected experience in user space. Experiments evaluate three mixed compute and I/O workloads. Savings depend on deadlines, and the inference cost remains material for smaller processors. This is a reader-written paraphrase.

## 中文摘要改写

传统Linux governor主要根据当前负载阈值调频，难以按特定应用的软截止时间利用执行阶段差异。作者以频率和利用率为观测，用GRU压缩历史、Q网络输出频率动作；内核只执行推理和采样，用户态进行经验回放训练。i5平台上的视觉、转码联网以及FFT与文件写入三类任务显示了依截止期变化的能量收益。方法证明了真实CPU上的学习选频可实现，但4–10ms推理开销、单平台与软时限证据使其不能原样迁移到小型E902。

## 题名怎么理解

**原题：** Deadline-Aware Deep-Recurrent-Q-Network Governor for Smart Energy Saving

**中文阅读题：** 为什么要让CPU选频器记住过去：DRQN及用户态训练

## 章节导读

| 阅读问题 | 先看材料 | 如何接到下一步 |
| --- | --- | --- |
| 为什么要改现有方案 | 问题背景与动机图 | 确定目标、约束和原有不足 |
| 系统观察什么、控制什么 | 输入输出表＋关键架构图 | 确认数据、模型和执行器真实角色 |
| 方法如何得到动作或估计 | 方法段、公式、算法／模型表 | 明确离线训练与在线流程 |
| 收益是否真实且公平 | 结果图表、统计与测量边界 | 核查基线／目标／分母／开销 |
| 能否用于自己的CPU | 局限、复现计划、三项实验 | 把论文假设变成待验证的工程条件 |

## 阅读中英对照

| 级别 | 术语／关键词 | 直觉、严格含义与易混点 |
| --- | --- | --- |
| A | DVFS / DFS | DVFS同时涉及动态电压与频率；只有时钟变化称DFS。电压能否改变取决于实际供电域。 |
| A | Workload | 真正执行应用计算的程序与输入；本文里的控制器是另一个角色。 |
| A | Controller | 根据观测选择动作的软件／硬件，可运行在同一CPU或独立控制核。 |
| A | OPP | Operating Performance Point，经过允许范围验证的电压—频率组合。 |
| A | Power / Energy | 功率W表示此刻消耗快慢；能量J是对时间积分。低功率不必然低能量。 |
| B | Deadline | 作业必须完成的时刻；平均时延、P95与最大时延各有不同用途。 |
| A | Governor | 根据观测作出频率请求的软件策略。 |
| B | GRU | 带门控的循环网络，用固定长度向量概括历史。 |
| B | Q值 | 某状态采取动作的预期累计回报，非功率测量值。 |
| C | 经验回放 | 保存交互样本后重用训练；循环模型还需处理序列状态。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| Benchmark1相对Ondemand | 13%–33%核心能量降低 | 期限4.0–5.0s，10次请求 | §IV-D，Fig9，p9 |
| Benchmark2相对Ondemand | 22%–30%降低 | 期限4.0/4.5s，含转码和蓝牙 | Fig10，p9 |
| Benchmark3相对Ondemand | 7%–28%降低 | 期限4.0/5.0s，FFT与写文件 | Fig11，p9 |
| 单次推理 | 4–10ms | 不是2023后续工作的25µs | 结论，p9 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

最值得迁移的是“执行历史有用”与“离线训练、在线轻推理”的分工。你的被控负载可以是压缩程序，状态历史换成每块进度、周期与忙闲比例。E902上先比较短历史统计量和小Q表，再决定是否需要GRU；不要把i5上的4–10ms叫轻到可以忽略。
