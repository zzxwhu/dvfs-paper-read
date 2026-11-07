---
title: ScalePoM：DVFS、分层供电与LLM映射共同优化｜双语摘要与导读
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# ScalePoM：DVFS、分层供电与LLM映射共同优化｜双语摘要与导读

## 原文摘要翻译

对高能效、高性能大语言模型硬件的需求推动了可扩展Chiplet设计的发展，而这类设计需要仔细进行电源优化与管理。本文提出一种面向LLM应用的Chiplet分层供电协同优化与管理方法。为建模LLM工作负载映射与供电，作者首先建立可扩展Chiplet模拟器，展示不同电源策略对效率有显著影响，需要细致全面的优化。随后，作者开发了面向Chiplet电源管理的协同优化框架ScalePoM。根据给定LLM模型与功耗、性能和面积要求，ScalePoM能够自动探索Chiplet架构和工作负载映射，以优化分层供电。作者通过两种采用不同互连拓扑的扩展LLM Chiplet方案评估该方法，在不同稀疏程度的LLM推理中取得平均45%、最高62%的能量节省。（第1页摘要）

## 英文改写（非原摘要）

**English paraphrase, not the original abstract:** ScalePoM links LLM workload mapping with chiplet architecture and hierarchical power delivery. It searches design choices using performance and power-delivery models, then exploits unequal runtime loads through DVFS. Its reported benefits combine several optimizations and depend on the modeled architectures, constraints, regulator data and baselines.

## 创新点

1. **把供电端损耗纳入架构与映射决策。** 相同核心计算功耗下，稳压器效率、寄生网络、电流分布和供电分组仍会改变输入端能量。只优化MAC或只给核心降频会遗漏这部分。

2. **构建连接LLM任务与分层PDN的探索框架。** 输入模型规模、功率/时延/面积约束及器件特征，联动Chiplet数量、映射、批量和PMIC/PIVR/FIVR组合，输出候选设计和Pareto集合。

3. **利用阶段与负载差异做运行时DVFS。** 分层供电隔离不同组，再降低低负载/非瓶颈组的电压频率。论文说明其应用机会，但没有给足完整在线控制器实现规范。

LLM是被控工作负载，不是训练一个LLM来选频。本文也不是用强化学习替代所有搜索。

## 一句话

先共同决定任务放在哪里、电从哪里来，再根据各域是否处在瓶颈上调整电压频率，评价完成任务的总能量而非只看核心功率。

[返回完整图文精读](note.md) · [专题索引](../index.md)
