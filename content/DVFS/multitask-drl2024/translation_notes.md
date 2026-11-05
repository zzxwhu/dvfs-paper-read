---
title: "多任务时序DDQN：中英文摘要与章节导读"
tags: ["DVFS", "CPU", "E902"]
date: "2026-11-05"
source_sha256: "c106cb9bf8b2503b16ccbadf8cc336b506eced4ccf86df1e971ea98f1bb1e548"
---

[论文页面](https://doi.org/10.48550/arXiv.2409.19434) · [本笔记所用 PDF](https://arxiv.org/pdf/2409.19434v3) · [标识符](https://doi.org/10.48550/arXiv.2409.19434)

整理日期：2026-11-05。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

This work extends utilization-based learned CPU governors to periodic task sets with multiple deadlines. Task-state labels and temporal encoders feed a Double DQN trained in user space and evaluated in the kernel. Jetson Nano experiments compare recurrent and non-recurrent encodings, including random task sets. Reported savings and deadline violations must be examined together. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究多核共享频率上的周期软实时任务集，串行/并行与多个期限的运行时能效。具体程序包括3任务：重复乘法；5/8任务：MiBench jpeg、qsort、fft、typeset混合；另随机生成3/4/5/8任务集。作者在NVIDIA Jetson Nano2GB，Linux4.9；Ruideng UM25C USB功率计；内核浮点网络，用户态训练；不是E902实现上采用用户态DDQN＋内核TEGM（GRU+MLP，PRO/PROL）或TEM（MLP，PROM）；对每个候选频率评估Q并取最大；终回合稀疏reward。输入为每任务未开始/执行中/完成标签、开始/完成时间记录、最大/平均利用率、候选频率、累计已用时间与频率-负载驻留时间，输出为两档候选CPU频率的选择；内核不接收完整任务模型，期限用于用户态reward。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。相对已有2023单任务编码，新增多任务状态标签/时间戳和递归编码，并调整软超时奖励；需要较大网络才处理8任务，展示可观测性与容量权衡。

## 题名怎么理解

**原题：** Energy-Efficient Computation with DVFS using Deep Reinforcement Learning for Multi-Task Systems in Edge Computing

**中文阅读题：** 把任务开始/完成标签和负载历史编码给DDQN，使共享CPU频率能考虑多个任务的软期限

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
| A | 被控程序 | 3任务：重复乘法；5/8任务：MiBench jpeg、qsort、fft、typeset混合；另随机生成3/4/5/8任务集 |
| A | 控制策略 | 用户态DDQN＋内核TEGM（GRU+MLP，PRO/PROL）或TEM（MLP，PROM）；对每个候选频率评估Q并取最大；终回合稀疏reward |
| B | 控制周期 | 在governor决策点更新；本文统一采样间隔及两档确切频值当前未定位齐；400训练轮，每轮3次收集 |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| 固定任务集相对Ondemand | 约7%/3%/4%降低 | 分别3任务PRO、5任务PRO、8任务PROL；图15称功率，正文又称energy，应保留术语不一致 | Fig15/§III-E，p9–10 |
| 随机任务集功率 | 2.177→1.8449W（3任务，15.25%） | 不是所有任务均有15.25%；4/5/8任务7.25/8.12/7.26% | TableVI，p11 |
| 推理开销 | 最大0.16ms | 8任务PROL；非旧2023的整数引擎25µs | TableIV，p10 |
| 随机任务超时>5%的比例 | 10.67%/12.57%/4.06%/4.59% | 分别3/4/5/8任务；不能写零违约保证 | TableVII，p11 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

对E902可把多任务标签换成“采集、压缩、发送”阶段或多个待处理块；先实现低维历史统计/小Q表，再考虑GRU。不要为单核小任务复制内核浮点网络。
