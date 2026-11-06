---
title: "GreenLLM：SLO双环服务：中英文摘要与章节导读"
tags: ["DVFS", "GPU", "CV", "LLM", "E902"]
date: "2026-11-06"
source_sha256: "e78dbad4f73f1e6943ac96cf8e41b20f5f1e7a1254565def76aed97de186f9e5"
---

[论文页面](https://arxiv.org/abs/2508.16449v1) · [本笔记所用 PDF](https://arxiv.org/pdf/2508.16449v1) · [标识符](https://doi.org/10.48550/arXiv.2508.16449)

整理日期：2026-11-06。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

GreenLLM separates prefill and decode energy control for LLM serving. Prompt-length queues and a latency/power optimizer handle prefill. A TPS-based lookup table, hysteresis and a token-latency feedback loop control decode. Tests on an eight-A100 node report GPU energy savings under specified TTFT and TBT targets, with workload-dependent SLO compliance. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究多请求服务端LLM推理，prefill/decode解耦、动态到达率的运行时能效。具体程序包括Qwen3-14B dense、Qwen3-30B MoE，BF16；Alibaba ServeGen chat QPS1/3/5/8/10、Azure2024 code/conversation下采样trace。作者在单DGX-A100节点8×A100-SXM4 40GB/NVLink；Dynamo0.3.1/TensorRT-LLM；NVML SM应用时钟，显存固定；GPU能量，不含全设施上采用prefill长度分队列＋二次延时/三次功率模型约束优化；decode TPS查表粗环＋滞回＋20ms尾延时频率步进细环＋6s表偏置更新。输入为prompt长度/队列待处理项、离线aL²+bL+c时延与P(f)功率模型、过去200ms TPS、近期P95 TBT、SLO余量，输出为prefill队列路由与各worker SM频率；decode频带＋15MHz步进频率；不在线改变模型尺寸。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。按阶段采用不同控制律，且将服务排队、空闲功耗、尾延时反馈组合；可解释的双时间尺度比泛称“智能DVFS”更有实施意义。

## 题名怎么理解

**原题：** GreenLLM: SLO-Aware Dynamic Frequency Scaling for Energy-Efficient LLM Serving

**中文阅读题：** prefill按prompt长度分队列并解能量模型，decode用TPS粗档表与token尾延时细环分别调GPU频率

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
| A | 被控程序 | Qwen3-14B dense、Qwen3-30B MoE，BF16；Alibaba ServeGen chat QPS1/3/5/8/10、Azure2024 code/conversation下采样trace |
| A | 控制策略 | prefill长度分队列＋二次延时/三次功率模型约束优化；decode TPS查表粗环＋滞回＋20ms尾延时频率步进细环＋6s表偏置更新 |
| B | 控制周期 | decode 200ms估TPS、连续3窗口才换bucket；20ms细环；6s更新粗表。prefill按待处理队列调节 |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| GPU总能量降低 | Azure Qwen14B最高34.09% | Azure_conv5，相对defaultNV；其他工况约6.78%–34.09%，非所有34% | Table3，p10 |
| Qwen30B例 | Azure_conv8节能22.51%，TBT通过99.8%→93.8% | 通过率下降6.0个百分点；与摘要“additional violations<3.5%”笼统说法不完全一致 | Table4，p10 |
| 路由单独贡献 | 多工况约1%–3%能量变化 | PrefillSplit消融vsdefaultNV；主要节能还来自阶段调频 | Table3–4，p10 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

适合将“队列长度/阶段＋粗表＋细反馈”迁移到CPU服务应用；E902可用队列积压/剩余期限替代TPS与P95窗口，先简单规则再学习预测。完整LLM服务实验需要GPU内存，E902只适合小负载或作为管理核。
