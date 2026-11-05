---
title: "Ωkypous：中英文摘要与章节导读"
tags: ["DVFS", "CPU", "E902"]
date: "2026-11-05"
source_sha256: "104c8cbec7a5724c75de48a7248ebb611600584cc4653b9618e27fc1fcd26ddb"
---

[论文页面](https://doi.org/10.48550/arXiv.2407.18386) · [本笔记所用 PDF](https://arxiv.org/pdf/2407.18386v3) · [标识符](https://doi.org/10.48550/arXiv.2407.18386)

整理日期：2026-11-05。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

Omega-kypous coordinates core and uncore scaling for serverless workflows. A grey-box latency model and an adaptive proportional controller redistribute timing slack between functions. Measurements on Xeon servers combine real functions with invocation patterns derived from Azure traces. Lower average power is reported with nonzero SLO violations and millisecond-scale control overhead. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究具有顺序/分叉/汇合的serverless函数工作流，SLO与调用率变化的运行时能效。具体程序包括SeBS九种函数构成160条工作流；正文点名video-processing、graph-bfs、dynamic-html；Azure调用轨迹驱动（并非直接在Azure上实测）。作者在两台Intel Xeon E5-2658A服务器，4个10vCPU/16GB VM，各VM分socket；OpenWhisk/Kubernetes/MinIO；acpi-cpufreq与MSR0x620；RAPL20ms采样上采用关键路径/比例预算＋自适应比例反馈u=Kp(S)S＋PMC灰盒延迟模型＋二次功率回归；Pareto可行集选最低功率Core/Uncore组合；共享域冲突协调。输入为工作流拓扑、端到端SLO、历史执行余量、函数输入对应PMC向量、共享频域请求，输出为下个函数延迟预算、Core频率与Uncore频率请求；不直接改变应用功能。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。把跨函数时间余量反馈、Core/Uncore联合动作、少样本灰盒预测与共享域协调结合；反馈是自适应比例控制，不是DDQN或标准PID。

## 题名怎么理解

**原题：** Leveraging Core and Uncore Frequency Scaling for Power-Efficient Serverless Workflows

**中文阅读题：** 先分配工作流时间预算，再用余量比例反馈与灰盒模型联合选择CPU核心和uncore频率

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
| A | 被控程序 | SeBS九种函数构成160条工作流；正文点名video-processing、graph-bfs、dynamic-html；Azure调用轨迹驱动（并非直接在Azure上实测） |
| A | 控制策略 | 关键路径/比例预算＋自适应比例反馈u=Kp(S)S＋PMC灰盒延迟模型＋二次功率回归；Pareto可行集选最低功率Core/Uncore组合；共享域冲突协调 |
| B | 控制周期 | 函数执行前后事件触发；Core系统调用30–70µs，Uncore切换1–3ms；预处理3–15ms、预测2–5ms、远端协调10–20ms |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| 相对Performance/Ondemand功率 | 约降低44%/25% | 160条工作流，代价为非零违约；不等于CPU压缩能量收益 | Fig11–12/§6.2.1，p9–10 |
| 相对EcoFaaS功率 | 约降低16.4% | Ωkypous违约1.8%，EcoFaaS1.3%；不是相同违约率下比较 | §6.2.2，p10 |
| 相对DVFaaS功率 | 约降低22% | DVFaaS违约2.8%，各控制器服务质量并非完全相同 | Fig12，p10 |
| 少样本预测 | 5次调用内MAPE<4% | 函数leave-one-out设置；不是所有未知输入误差上界 | Fig10，p8 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

可把工作流函数换成采集→压缩→发送，用前一阶段余量调下一阶段预算；E902只保留一个合法频率动作。学习灰盒模型的可解释分解，确认开销低于阶段时长，再考虑智能增强。
