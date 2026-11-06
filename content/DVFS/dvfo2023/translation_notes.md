---
title: "DVFO：边云协同推理：中英文摘要与章节导读"
tags: ["DVFS", "GPU", "CV", "LLM", "E902"]
date: "2026-11-06"
source_sha256: "1a9e48c7242d3cdcea3a51bf6b487299c69948f449d272d0dcd082026602e2a6"
---

[论文页面](https://arxiv.org/abs/2306.01811v3) · [本笔记所用 PDF](https://arxiv.org/pdf/2306.01811v3) · [标识符](https://doi.org/10.48550/arXiv.2306.01811)

整理日期：2026-11-06。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

DVFO jointly controls edge frequencies and partial feature offloading for collaborative DNN inference. Spatial–channel attention keeps important features local and quantizes less important features for remote execution. A concurrent DQN reduces blocking decision overhead. Reported energy is measured on the edge device and should not be confused with combined edge-and-cloud energy. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究边缘–云协同CV分类推理，网络带宽变化的运行时能效。具体程序包括主实验EfficientNet-B0与ViT-B16，CIFAR100/ImageNet2012；扩展ResNet18、Inception-v3、MobileNet-v2、MaxViT。作者在Jetson Nano/TX2/Xavier NX（默认NX）；云RTX3080＋Xeon6226R；PyTorch、nvpmodel、jetson-stats边缘设备遥测；云端能量未计入边缘ETI上采用离线训练、在线推理的concurrent DQN：prioritized replay＋ε-greedy；thinking-while-moving减少决策阻塞；SCAM选择特征＋INT8量化＋加权融合。输入为η能量/时延权重、融合权重λ、SCAM特征重要性分布、当前带宽B；历史reward/replay用于训练，输出为CPU/GPU/内存频率三元组＋特征分配比例ξ；另由SCAM确定重要特征和加权融合输出。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。同时处理应用特征、卸载动作和异构频域，突出决策延迟与任务执行重叠。智能控制器是DQN，CV网络是被控负载，两者角色独立。

## 题名怎么理解

**原题：** DVFO: Learning-Based DVFS for Energy-Efficient Edge-Cloud Collaborative Inference

**中文阅读题：** 用并发DQN联合选择边缘CPU/GPU/内存频率与特征卸载比例，结合注意力和量化降低边缘推理成本

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
| A | 被控程序 | 主实验EfficientNet-B0与ViT-B16，CIFAR100/ImageNet2012；扩展ResNet18、Inception-v3、MobileNet-v2、MaxViT |
| A | 控制策略 | 离线训练、在线推理的concurrent DQN：prioritized replay＋ε-greedy；thinking-while-moving减少决策阻塞；SCAM选择特征＋INT8量化＋加权融合 |
| B | 控制周期 | 以推理任务为动作边界；策略推理与正在执行的动作并发，不是CPU利用率固定周期阈值 |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| 主推理能量降低 | 18.4%/31.2%/39.7%/43.4% | 分别相对DRLDO/AppealNet/Cloud-only/Edge-only；NX、5Mbps、两模型×两数据集平均，边缘能量 | §6.3/Fig8，p9 |
| 端到端时延降低 | 28.6%–59.1% | 相对上述不同基线；不是纯DVFS消融收益 | Fig8，p9 |
| 准确率边界 | §6.3称相对Edge-only损失within2%；融合例0.68/0.56个百分点 | 摘要within1%与主实验within2%不能合并；Table4只比较融合实现 | Fig9/Table4，p10/12 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

若选CV且有Jetson与云GPU，可做联合卸载；若只有CPU，先缩成“本地CPU推理＋离散频率”并保留质量约束。E902不能默认接DQN或跑ViT；可迁移“状态—动作—reward表”和异步控制开销测量。
