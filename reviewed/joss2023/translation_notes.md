# JOSS：中英文摘要与章节导读

[论文页面](https://arxiv.org/abs/2306.04615) · [本笔记所用 PDF](https://arxiv.org/pdf/2306.04615v1) · [DOI](https://doi.org/10.48550/arXiv.2306.04615)

整理日期：2026-11-05。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

JOSS jointly chooses core type, parallelism, CPU frequency and memory frequency for task-based programs. Platform models and short runtime calibration predict latency and energy; a scheduler searches configurations and coordinates shared domains. The experiments emphasize CPU-plus-memory energy rather than CPU energy alone. Model error and shared-resource heuristics limit strict timing claims. This is a reader-written paraphrase.

## 中文摘要改写

JOSS把任务映射与CPU／内存频率选择联合起来。它通过平台离线回归和运行时两档采样，预测每类任务的执行时间及CPU、内存功耗，搜索满足能量或相对性能目标的配置；再处理共享频域的并发冲突及短任务切换成本。Jetson TX2实验显示，只优化CPU能量可能增加内存驻留能量。该方法有助于建立“总能量而非单轨功率”的选频观念，但多核异构调度和内存DVFS并不是E902现成具备的条件。

## 题名怎么理解

**原题：** JOSS: Joint Exploration of CPU-Memory DVFS and Task Scheduling for Energy Efficiency

**中文阅读题：** 别只盯CPU功耗：同时预测任务时间、CPU能量与内存能量

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
| A | 总能量 | 这里主要指CPU轨＋内存轨，不自动包括整板所有外设。 |
| B | Memory-boundness | 等待访存对运行时间的影响，本文由模型估计。 |
| B | Moldable任务 | 同类任务可选择使用不同核数执行。 |
| C | 最陡下降 | 邻域内逐步找更低预测能量；一般不保证全局最优。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| 相对GRWS总能量 | JOSS降低40.7%；STEER降低19.5% | Fig8统一归一化到GRWS，含CPU＋内存 | §7.1，p8–9 |
| 论文所谓额外收益 | 作者称相对STEER额外21.2% | 40.7−19.5=21.2个百分点；分母不同，不能直接当相对比值 | §7.1，Fig8 |
| 不控制内存频率 | 相对GRWS降低24.8% | 仍考虑内存能量，证明目标边界重要 | §7.1，p8 |
| 平均模型分数 | 时间97%、CPU功率90%、内存功率80% | 按1−相对绝对误差定义，不是三种分类正确率 | §7.3，Fig10，p9 |
| 运行时采样 | 约0.8%总时间 | 每kernel重复出现的测试场景 | §5.1，p5 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

你最应借鉴免PMC的两档标定、把非CPU固定功耗加入目标、用小查表替代复杂在线搜索。E902先只调CPU，测量SRAM/外设和板级功耗的边界；不要为了照搬四旋钮引入不存在的内存调压接口。
