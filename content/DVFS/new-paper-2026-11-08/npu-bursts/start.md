---
title: NPU融合功率尖峰：负载塑形与DVFS保护｜从零入门
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# NPU融合功率尖峰：负载塑形与DVFS保护｜从零入门

先看PMIC输入侧测点，再读PAPR热点与联合可编译选边。QDQ是融合屏障而非剪枝；峰值低37.8%时能量反增2.6%。它塑形负载以减轻现有DVFS保护，不重新设计PLL/PMIC。

## 一句话

先找编译融合后最容易制造电流尖峰的执行区间，再在少量可行边插入不能被优化掉的屏障，使负载不那么集中，从而减少低输入电压下既有保护导致的性能恶化。

## 先理解研究问题

### 先区分三个常被混用的目标

**English paraphrase (not the original abstract):** This measurement study links aggressive operator fusion on a commercial mobile NPU to peak-current bursts and low-voltage protection behavior. An offline, PAPR-guided graph rewrite inserts jointly compilable Q–DQ barriers to reshape execution. Peak-current reduction comes with latency, energy, and quantization tradeoffs; the inferred voltage margin is an exploratory estimate rather than a transferable hardware law.

降低峰值电流，为的是减轻瞬态供电压力；降低每次推理能量，为的是少耗电；提高吞吐，为的是更快完成任务。三者可以冲突。本文最醒目的数字是**峰值下降37.8%**，不是能量下降37.8%。主配置的能量反而增加约2.6%。

图1的假说链是：激进融合→计算与存储流量集中→瞬态电流尖峰→PDN压降→低压保护→时延上升。作者提供测量和拆分前后对照，但商业芯片内部是黑盒，不能把每个中间环节都当作已直接观测。

### 从零需要的术语

|层次|术语|在本文中的准确含义|
|---|---|---|
|A|算子融合、超层|编译器把连续操作合成较大执行单元，减少中间存取和调用；大单元可能集中负载|
|A|PDN|从电源到负载的供电网络，包含路径阻抗和储能/稳压环节；不是理想无损导线|
|A|峰值、平均值、能量|峰值是瞬间最大电流；平均功率是时间平均；能量是功率积分，量纲不同|
|B|PAPR|峰均比；本文用瞬时电流除以整次推理平均电流作代理指标，无量纲|
|B|Q–DQ|量化再反量化，作为阻止进一步融合的屏障；会有数值误差，不是删除权重|
|B|SOC与SoC|SOC常指电池荷电状态百分比；SoC也常指系统芯片。本文须看上下文，不能混成CPU利用率|
|C|保护起始电压|外部供电逐步降低时开始出现保护性节流的输入电压；不是直接读出的NPU核心最低Vdd|
|C|联合编译可行|所有已选屏障一起插入后，图导出、供应商编译、目标执行均成功；单边可行不足以保证组合可行|

阅读顺序建议：先看测量位置图3，再读算法1与波形图5，最后把表1、表4和图6放在一起。这样能同时看到方法、收益与代价。

## 五步阅读

1. [谁是被控对象与平台](note.md#数据与任务定义)。
2. [跟着输入、操作、输出读方法](note.md#方法主线)。
3. [对齐基线与实验结果](note.md#关键结果)。
4. [检查哪些参数和证据还不够](note.md#局限)。
5. [按复现计划从模型到硬件验证](note.md#我的笔记)。

[返回完整图文精读](note.md) · [专题索引](../index.md)
