---
title: "Zeus：训练能量优化：中英文摘要与章节导读"
tags: ["DVFS", "GPU", "CV", "LLM", "E902"]
date: "2026-11-06"
source_sha256: "90bdc9e84d3189b2573f7218e47e8d244233865b064bc9a2a5fc2506102516a4"
---

[论文页面](https://www.usenix.org/conference/nsdi23/presentation/you) · [本笔记所用 PDF](https://www.usenix.org/system/files/nsdi23-you.pdf) · [标识符](https://www.usenix.org/conference/nsdi23/presentation/you)

整理日期：2026-11-06。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

Zeus optimizes recurring DNN training jobs using a batch-size bandit and an online power-limit profiler. It accounts for stochastic convergence rather than equating throughput with time to accuracy. GPU measurements support a trace-replay evaluation and a separate end-to-end drift experiment. Savings depend on the training accuracy target and the energy–time preference. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究反复提交、需要达到目标质量的GPU DNN训练/微调的运行时能效。具体程序包括DeepSpeech2/LibriSpeech；BERT/SQuAD与Sentiment140；ResNet50/ImageNet；ShuffleNet-v2/CIFAR100；NeuMF/MovieLens1M。作者在默认V100 PCIe32GB；另A40、RTX6000、P100；PyTorch ZeusDataLoader＋NVML GPU遥测与功率帽。多数优化评估由真实训练/功率轨迹回放；漂移另有端到端训练上采用高斯Thompson Sampling多臂老虎机选batch size；两轮剪枝/代价早停；固定batch时JIT剖析选GPU功率上限；近期窗口适应漂移。输入为用户权重η、目标accuracy/F1/WER/NDCG、候选batch、每次达到目标的epochs/时间/能量、各功率帽吞吐与功率，输出为下次训练的batch size b；本次GPU功率上限p；超代价时中止并换batch。不是直接写任意电压。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。将time/energy-to-accuracy、随机收敛与反复训练的探索成本统一起来；智能模块是低维概率老虎机，不是CNN控制器。

## 题名怎么理解

**原题：** Zeus: Understanding and Optimizing GPU Energy Consumption of DNN Training

**中文阅读题：** 把反复训练任务的batch size视为老虎机动作，用在线功率剖析寻找功率上限，优化达到目标精度的总能量与总时间

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
| A | 被控程序 | DeepSpeech2/LibriSpeech；BERT/SQuAD与Sentiment140；ResNet50/ImageNet；ShuffleNet-v2/CIFAR100；NeuMF/MovieLens1M |
| A | 控制策略 | 高斯Thompson Sampling多臂老虎机选batch size；两轮剪枝/代价早停；固定batch时JIT剖析选GPU功率上限；近期窗口适应漂移 |
| B | 控制周期 | batch在训练任务再次提交时选择；power cap在迭代边界切换采样，每个帽约5秒；无统一20ms频率环 |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| 达到目标的GPU能量降低 | 15.3%–75.8% | 相对默认batch＋最大功率帽；Fig6取最后5次recurrences；主要是轨迹回放结果 | §6.1–6.2/Fig6，p10–11 |
| 训练时间代价 | 最多缩短60.1%，部分增加12.8% | 不同负载的能量—时间折中；不是所有负载同时提速 | §6.2，p11 |
| 探索代价 | Grid Search最坏累计regret为Zeus的72倍 | 相同recurrence任务设置；regret单位J，不是节能72倍 | Fig7–8，p11 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

若你选择GPU训练，这是完整应用方向；先小模型重复训练即可。CPU/E902可借鉴“重复作业＋低维离散动作＋探索预算”，动作换为合法OPP、保持任务输出一致；E902不直接照搬大模型batch和GPU功率帽。
