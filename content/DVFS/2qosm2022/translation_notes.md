---
title: "2QoSM表格Q：中英文摘要与章节导读"
tags: ["DVFS", "CPU", "E902"]
date: "2026-11-05"
source_sha256: "ea84698ad20b912cd69b4bd75fdc098fcfb783c587005ac8fcaad5121a106dcb"
---

[论文页面](https://doi.org/10.3390/jlpea12020029) · [本笔记所用 PDF](https://mdpi-res.com/d_attachment/jlpea/jlpea-12-00029/article_deploy/jlpea-12-00029.pdf) · [标识符](https://doi.org/10.3390/jlpea12020029)

整理日期：2026-11-05。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

2QoSM integrates tabular Q-learning with compute-aware applications and a hardware abstraction layer. A navigation application on an ODROID-XU4 supplies application metrics to the CPU power manager. Different reward functions emphasize power, path error, or replanning. The strongest power and error improvements belong to different policies and must not be combined. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究导航/路径规划CPU软件，计算量、访存与重规划需求变化；本文CPU控制不是电机控制算法的运行时能效。具体程序包括Anytime Dynamic A*（ADA*）路径规划、地图与轨迹规划线程；低层PID/里程计由另一Arduino承担，不是用户课题要实现的内容。作者在ODROID-XU4 Exynos5422，4×A15/4×A7、2GB，Ubuntu18.04/Linux4.14.5-92；cluster级DVFS；ArduinoROMEO/ATmega328P独立处理低层动作上采用C/GSL实现表格Q-learning，状态离散化，0.9概率选最大Q/0.1探索；10ms线程更新；七种reward对照，HAL映射至CPU性能状态。输入为路径误差、功率、重规划标志、通信校验错误、地图更新等离散状态；不只CPU利用率，输出为HAL定义的离散CPU性能状态（每状态5个动作Q条目）；具体频率映射需实现确认，线程迁核未作为本实验动作。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。用可替换软件抽象把应用性能指标、Q-learning与HAL组合，并系统展示七种reward如何改变策略。学习器本身是经典表格Q，研究价值在状态/奖励/架构取舍。

## 题名怎么理解

**原题：** Low-Overhead Reinforcement Learning-Based Power Management Using 2QoSM

**中文阅读题：** 用小Q表控制CPU性能状态，并用七种奖励展示省功率与服务质量的取舍

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
| A | 被控程序 | Anytime Dynamic A*（ADA*）路径规划、地图与轨迹规划线程；低层PID/里程计由另一Arduino承担，不是用户课题要实现的内容 |
| A | 控制策略 | C/GSL实现表格Q-learning，状态离散化，0.9概率选最大Q/0.1探索；10ms线程更新；七种reward对照，HAL映射至CPU性能状态 |
| B | 控制周期 | 用户态QoSM独立线程，10ms hrtimer周期；各reward先600s训练，每次试验从同训练矩阵起步，试验中仍可更新 |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| power-only策略 | 平均功率降低42.6% vs Ondemand | 2.98W；相对situation-aware降低10.2%，但误差更大 | Fig8/§5.4，p15 |
| power＋error策略 | 功率−38.7%、误差−4.6% vs Ondemand | 同一reward可同时转述这两项；不是42.6%与6.1%同时获得 | §5.4，p15 |
| error-only策略 | 误差改善6.1% vs Ondemand | 属于另一策略；不能合并最高功率收益 | §5.4，p15 |
| Q表存储 | 64KB | 1600×5×8B，尚不含程序/栈/其他状态 | §5.2/Table2，p10–11 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

只借鉴CPU资源管理：用块进度/余量/历史成本作小Q表状态，动作是合法频档；任务正确性不应被当作可交易reward，出错必须失败。无需任何电机知识。
