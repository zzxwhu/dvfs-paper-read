---
title: "ATP Per-core DVFS：中英文摘要与章节导读"
tags: ["DVFS", "CPU", "E902"]
date: "2026-11-05"
source_sha256: "dfa8d334c213d29f86436d9000169c02a4681eeb3e839864684c32a925aed4cf"
---

[论文页面](https://doi.org/10.37936/ecti-cit.2025192.258820) · [本笔记所用 PDF](https://ph01.tci-thaijo.org/index.php/ecticit/article/download/258820/174292) · [标识符](https://doi.org/10.37936/ecti-cit.2025192.258820)

整理日期：2026-11-05。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

ATP DVFS adapts an utilization threshold within a profiled range and applies a per-core frequency policy. A Xeon server running KVM and Charm++ workloads provides the evaluation. The method improves energy per instruction relative to Ondemand in the reported workloads, but does not dominate the Performance governor in every case. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究虚拟机中并行通信负载，2/3/4核参与与不同不平衡程度的运行时能效。具体程序包括Charm++ Stream-All-to-All，TRAM（Topological Routing and Aggregation of Messages）；Type1/2/3三种并行配置。作者在物理Xeon E5630四核2.53GHz，CentOS7/KVM；4vCPU虚拟机；psutil/perf-kvm，APC UPS/apcupsd读取能耗；实际供电域独立性未由请求接口自动证明上采用阈值T=45%+U_avg·(85%−45%)；逐核利用率超过T则升最高频，否则降一档；100ms轮询，非神经网络。输入为各核当前频率和利用率、平均利用率、45%/85%经验阈值界，输出为各核频率请求：最高档或下降一个支持频档；没有直接输出电压。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。基于静态阈值扫描得到自适应范围，在较低实现复杂度下改善一部分并行负载的阈值控制。贡献是政策和测评，不是复杂智能算法。

## 题名怎么理解

**原题：** Energy-Efficient Per-Core DVFS for Virtual Machine Management in Cloud Data Centers

**中文阅读题：** 用随平均CPU利用率变化的阈值替代固定阈值，逐核升到最高档或下降一档

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
| A | 被控程序 | Charm++ Stream-All-to-All，TRAM（Topological Routing and Aggregation of Messages）；Type1/2/3三种并行配置 |
| A | 控制策略 | 阈值T=45%+U_avg·(85%−45%)；逐核利用率超过T则升最高频，否则降一档；100ms轮询，非神经网络 |
| B | 控制周期 | 100ms轮询；作者将监测器称Optimizer，控制物理层而负载在VM |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| Type1能量/指令 | ATP79.06，Ondemand84.29，Performance75.74 J/Ginstr | ATP好于Ondemand，但差于Performance | Fig9/§6.2，p8–9 |
| Type2能量/指令 | ATP57.88，Ondemand61.64，Performance57.48 J/Ginstr | 同一负载内比较，不能说ATP全面第一 | §6.2，p9 |
| Type3能量/指令 | ATP44.81，Performance44.92 J/Ginstr | 很小差距无置信区间，不自动显著 | §6.2，p9 |
| 温度 | 平均约低2.5°C | 相对Performance；摄氏百分比非热能收益 | §6.3，p10 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

很适合作为E902简单基线：在固定任务到达与CPU利用率可观测条件下用少量比较和查表控制频率；压缩任务可能持续100%利用率，必须检验是否退化为一直最高档。
