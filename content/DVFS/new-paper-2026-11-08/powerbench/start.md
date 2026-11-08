---
title: PowerBench：测量、扫档与有约束的OPP选择｜从零入门
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# PowerBench：测量、扫档与有约束的OPP选择｜从零入门

先固定程序、输入与测量窗口，再扫合法OPP。按prefill/decode读核心与总线热图，按速度约束从Pareto前沿选点。39.7%是单项实测，53.2%是组合配置推算；本文没有新在线智能调档器。

## 一句话

先固定真实推理任务，测出每个执行阶段在不同合法配置下的时延与能量，再找性能合格的省能工作点；本文提供这套表征证据，而PLL/PMIC的底层执行协议仍由平台承担。

## 先理解研究问题

### 阅读地图：这篇论文最能回答你什么

先读“方法主线”的计量和扫档，再看图14的二维工作点与图15的Pareto前沿，最后看图16和表9。你会知道哪些数据足以支撑一个选档器，也能看到从一张实验表到实际硬件闭环还差哪些模块。

**English paraphrase (not the original abstract):** PowerBench characterizes mobile LLM execution across frameworks and heterogeneous backends using standardized timing, energy attribution, and hardware microbenchmarks. Configuration sweeps reveal phase-dependent bottlenecks and coordination costs. Measured CPU-frequency savings and estimated end-to-end savings are distinct results; the work does not implement a new online DVFS controller or expose a complete PLL/PMIC transition protocol.

直观地说，NPU像一条适合大批量生产的流水线。一次送入大量工作时很高效；如果每次只做一个很小的操作，却需要不断由CPU发命令、等待并同步，生产线的高峰值能力就未必能转成真实任务速度。这只是帮助理解的类比，是否发生要由实际算子和调用测量证明。

论文的研究空白是：只看CPU/GPU/NPU的峰值TOPS、模型总吞吐或整机功率，会掩盖框架实现、数据搬运、CPU辅助和NPU电源状态之间的耦合。因此它同时回答两个层次的问题：哪个后端适合哪一阶段，以及在已选后端上有哪些省能配置。

### 术语按三个层次掌握

|层次|术语|含义与本篇用途|
|---|---|---|
|A：先看懂任务|prefill，提示处理|并行处理输入token、建立上下文缓存，通常有较大的矩阵乘法|
|A|decode，逐词生成|依次生成token，每一步依赖前一步；小矩阵向量运算和访存占比可能更高|
|A|吞吐、能量、功率|tokens/s表示快慢；J或µJ/token表示完成工作耗多少能量；W表示瞬时或平均耗能速率|
|B：理解实验|GEMM/GEMV|矩阵乘矩阵/矩阵乘向量，决定同一硬件是否有足够并行工作|
|B|PMIC zone、累计能量计数|平台按供电区域提供的能量遥测；读两次做差获得测量窗口能量|
|B|vcorner|供应商定义的性能/电压等级；名称本身不是伏特值，也不等于实际测得频率|
|C：形成策略|Pareto前沿|找不到另一个同时更快且不更耗能、或更省能且不更慢的已测配置集合|
|C|OPP|运行工作点，通常包含合法电压频率组合；还可能受温度、共享电源域和固件限制|
|C|RPC轮询、睡眠延迟|CPU/NPU协作与电源状态参数；与DVFS有关联，但不是同一种控制动作|

## 五步阅读

1. [谁是被控对象与平台](note.md#数据与任务定义)。
2. [跟着输入、操作、输出读方法](note.md#方法主线)。
3. [对齐基线与实验结果](note.md#关键结果)。
4. [检查哪些参数和证据还不够](note.md#局限)。
5. [按复现计划从模型到硬件验证](note.md#我的笔记)。

[返回完整图文精读](note.md) · [专题索引](../index.md)
