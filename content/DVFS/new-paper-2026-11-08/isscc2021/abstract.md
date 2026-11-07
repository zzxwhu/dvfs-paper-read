---
title: ISSCC2021：传感器裕量与PLL、PMIC控制｜双语摘要与导读
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# ISSCC2021：传感器裕量与PLL、PMIC控制｜双语摘要与导读

## 原文摘要翻译

这份会议摘要集正文没有单列Abstract。以下翻译开头概述段，不额外加入分析结论。

本文以7nm FinFET工艺实现了一个高速、低功耗的异构八核CPU复合体。片上传感器针对工艺、电压、温度与老化的裕量进行处理，以改善动态频率和电压缩放中的功耗。工艺传感器结合机器学习确定每颗芯片的工艺电压裕量，服务于智能手机工作电压设置。温度传感器感知运行时局部温度及温度反转，调整DVFS中的温度裕量。老化传感器将单元退化转换成相应老化裕量进行补偿。电压传感器则维持系统面对供电噪声时的稳定性。在传感器辅助下，CPU最高可运行到2.8GHz，并获得13%的功耗改善。它被集成到支持sub-6GHz、上行2.6Gbps及下行4.7Gbps的5G手机SoC中。（PDF第1页首段）

## 英文改写（非原摘要）

**English paraphrase, not the original abstract:** This measured 7nm CPU uses process, temperature, aging and voltage sensing to support DVFS. Offline calibration and firmware connect sensor counts to voltage guardbands, while performance requests and thermal budgets guide operating-point selection. The reported 13% power reduction applies to the stated matched-frequency configuration and does not imply a universal energy benefit.

## 创新点

1. **将工艺、温度与老化的电压裕量分开校准和调整。** 以当前芯片的实际传感信息取代统一采用最坏条件的部分裕量，目标是在要求频率不变时减少过度供电。

2. **工艺传感器不仅模拟组合逻辑延迟。** 在环振结构中加入触发器、数据反相和脉冲发生器，使感测路径包含时序单元，更接近CPU关键路径的构成；用传感计数与所需电压建立多元回归关系。

3. **把传感器电路、固件与现有PLL/PMIC连接成运行流程。** 启动阶段做每颗芯片的校准，运行时约每1ms结合性能需求、热预算与传感器更新OPP。快速供电跌落由V传感器处理，不能只靠毫秒循环。

“用了机器学习”不是说训练了一个神经网络或强化学习器来直接决定所有频率动作。本文的明确机器学习作用是传感器到工作电压的校准建模。

## 一句话

EAS与热预算决定CPU需要哪个性能工作点，片上传感器和固件再修正该工作点所需的电压裕量，PLL与PMIC负责真实执行。

[返回完整图文精读](note.md) · [专题索引](../index.md)
