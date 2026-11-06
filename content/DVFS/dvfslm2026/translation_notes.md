---
title: "DVFSLM：token需求预测：中英文摘要与章节导读"
tags: ["DVFS", "GPU", "CV", "LLM", "E902"]
date: "2026-11-06"
source_sha256: "c5198e6a344fb7fafe8727cf707c3851db286138803cb1d61f602da9e21fc447"
---

[论文页面](https://arxiv.org/abs/2609.13153v1) · [本笔记所用 PDF](https://arxiv.org/pdf/2609.13153v1) · [标识符](https://doi.org/10.48550/arXiv.2609.13153)

整理日期：2026-11-06。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

DVFSLM models upcoming SLM token workloads through matrix-operation structure and an offline learned metadata parser. Lightweight latency and power estimators drive a pruned GPU–EMC frequency search, with the CPU fixed at an empirically selected threshold. Window-level feedback corrects latency bias, and energy-per-token results are assessed together with a capped rate-based QoS metric. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究边缘GPU本地小语言模型自回归decode（含dense/MoE）的运行时能效。具体程序包括llama.cpp/llama-cpp-python q4_0；GPT2-small/medium/large/xl、Qwen2.5-0.5B、TinyLLaMA1.1B、OLMoE-1B-7B；主实验生成1024tokens。作者在Jetson AGX Orin与Orin NX；CPU阈值0.6528GHz固定；44/28组GPU–EMC候选；INA3221 200Hz整设备功耗；C++/XGBoost CAPI/pybind11上采用XGBoost矩阵规模→未来HPC元数据parser；线性/频率基函数E/T估计；枚举GPU–EMC候选＋单调剪枝；50token窗口偏差反馈α修正。输入为模型层结构、当前context长度与矩阵维度scale、离线预测HPC、deadline δ=1/目标tokens/s、上窗口测量/估计时延比α，输出为每窗口GPU/EMC频率pair；prefill用高GPU/EMC；CPU保持阈值；无可行解则最高频best-effort。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。把应用可知的未来矩阵工作量接到硬件元数据，再用轻量可解释估计和小空间约束搜索；智能学习在估计器，不在强化学习选频。

## 题名怎么理解

**原题：** DVFS for Small Language Model Inference on Mobile Edge Devices

**中文阅读题：** 从下一token的矩阵计算规模预测硬件元数据，再用轻量功率/延时模型在deadline下搜索GPU与EMC频率

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
| A | 被控程序 | llama.cpp/llama-cpp-python q4_0；GPT2-small/medium/large/xl、Qwen2.5-0.5B、TinyLLaMA1.1B、OLMoE-1B-7B；主实验生成1024tokens |
| A | 控制策略 | XGBoost矩阵规模→未来HPC元数据parser；线性/频率基函数E/T估计；枚举GPU–EMC候选＋单调剪枝；50token窗口偏差反馈α修正 |
| B | 控制周期 | 默认50token一决策窗；剪枝后平均决策0.81ms（原枚举1.73ms）；不是每token都实时采一次CUPTI |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| 每token能量 | 相对RULE最高−12.4%，相对改造Gear最高−8.4% | 模型/期限不同；某些高目标下Gear更省能但QoS差，不能脱约束比较 | Fig8/§5.1，p10 |
| QoS定义与改善 | min(实际tokens/s÷目标tokens/s,1)；原文最高相对改善93.12%/69.14% | 不是百分之多少token按时完成，也不是成功率；不可达目标下仍<100% | Fig9/§5.1，p10 |
| 模型误差/决策 | 功率平均误差2.49%–4.60%、延时2.01%–2.81%；决策0.81ms | 预测误差不是节能；CPU固定＋已剖析模型条件 | §5.2/Fig11，p10–11；§3.3 p8 |
| 一次性剖析成本 | 21.37–27.28小时/模型，0.25–0.33kWh，0.34–0.61GB | 并非零成本部署；须由后续推理节省摊销 | Table3/§5.4，p13 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

最贴近“输入需求预测→合法档约束搜索→实测反馈”的可行毕设链。GPU上可用小SLM；CPU/E902可把矩阵规模换块长/数据复杂度、未来cycles估计，做同结构小回归/小树，动作空间保持小。
