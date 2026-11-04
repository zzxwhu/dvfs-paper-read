# Runmeter：中英文摘要与章节导读

[论文页面](https://doi.org/10.1016/j.sysarc.2025.103504) · [本笔记所用 PDF](https://www.research-collection.ethz.ch/server/api/core/bitstreams/64d80e13-6f49-46a4-bb66-f8b0bc8e60f6/content) · [DOI](https://doi.org/10.1016/j.sysarc.2025.103504)

整理日期：2026-11-05。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

Runmeter brings frequency-specific, counter-based power models into the Linux kernel. Hybrid sampling, moving observation windows and fixed-point evaluation enable low-cost online estimates. The evaluation separates offline model accuracy, numerical approximation, online error and monitoring overhead. The framework supplies feedback for future control policies rather than demonstrating a complete DVFS policy. This is a reader-written paraphrase.

## 中文摘要改写

本文沿用并扩展按子系统和频率建模的方法，用自动筛选的计数器建立低开销线性功率估计，并提出Runmeter内核监控框架。框架在任务切换和调度tick时采样，聚合为可配置窗口统计，以定点数进行在线求值。Xavier实验分别验证离线模型、定点近似、在线估计和监控成本。它的重要增量是将模型变成可用于运行时控制的反馈基础设施；在线窗口误差明显大于离线整体能量误差，论文也未给出完整DVFS governor的净节能结果。

## 题名怎么理解

**原题：** Data-driven power modeling and monitoring via hardware performance counter tracking

**中文阅读题：** 从离线功率模型走向内核在线监控：精度、定点数和采样窗口

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
| A | 功率估计器 | 把计数器转成W，不自行决定频率。 |
| B | 观察窗口 | 用于汇总特征的时段，可比更新间隔长。 |
| B | 定点数 | 用整数及固定缩放因子表示小数，要检查位宽和溢出。 |
| C | 在线APE | 运行中每个估计窗口的相对绝对误差，与整段积分误差不同。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| 离线全部组合 | 功率MAPE8.6%；能量平均误差2.5% | 不能只展示有利子集 | §5.3，p9 |
| 离线GPU>600MHz子集 | 功率MAPE7.5%；能量平均1.3%、最大3.1% | 受限频率范围 | §5.3，p9 |
| 在线能量窗口APE | 平均约9%；P90约20.8%；最大约29% | CPU内核在线实验，Fig4；不同于离线1.3% | §5.4.2，p9–10 |
| 定点相对浮点 | 平均绝对误差约0.17mW，最大约17mW | 数值实现误差，不是相对真实功率的总误差 | §5.4.1，Fig3，p9–10 |
| 监控开销 | 最坏约7ms/s=0.7% | 密集上下文切换；2.3GHz最坏低于0.2% | §5.4.3，p10 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

把它当你系统的“观测／估计模块”参考最有价值。小型CPU上可以用环形缓冲保存周期、字节进度和活跃时间，用不同频点的整数线性权重估计能量，再由小Q表或回归选档。实际能量传感器与估计都应记录，不能只凭模型预测自证节能。
