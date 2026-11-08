---
title: PowerBench：测量、扫档与有约束的OPP选择｜双语摘要与导读
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# PowerBench：测量、扫档与有约束的OPP选择｜双语摘要与导读

## 原文摘要翻译

在移动设备上部署大语言模型能够增强隐私并降低时延，但硬件效率不足严重限制了这一过程。作者提出一项全面的移动端LLM推理跨层测量研究，覆盖五种主流框架（例如llama.cpp和GENIE）以及CPU、GPU、NPU三类硬件后端。为开展分析，作者开发了细粒度剖析工具PowerBench，用于测量LLM吞吐，并提供移动LLM推理的后端能量归因，超越传统设备级测量。作者还通过硬件微基准表征移动CPU、GPU和NPU的存储系统性能与计算能力。研究得到三项主要认识：第一，由框架造成的性能差距在NPU上被显著放大，可达10倍，原因包括卸载策略、不能充分利用硬件的算子以及激活量化策略不同。第二，推理存在明显的阶段差异：NPU擅长计算受限的提示处理，而CPU在访存受限的逐词生成阶段优于其他后端。这源于NPU偏好大型固定形状负载，与生成阶段的小算子及动态特征相冲突。第三，分后端剖析发现了先前研究遗漏的调度优化空间。欠佳的线程配置、不协调的NPU睡眠延迟和CPU轮询间隔会造成不必要的能量消耗。例如，仅调整CPU频率就能使能量消耗最高下降39.7%。利用这些发现，作者估算，一套面向能量的配置能够在三个数据集的NPU后端上将能量消耗最高降低53.2%，表明移动端LLM部署仍有较大的效率提升潜力。（第1页摘要）

## 英文改写（非原摘要）

**English paraphrase (not the original abstract):** PowerBench characterizes mobile LLM execution across frameworks and heterogeneous backends using standardized timing, energy attribution, and hardware microbenchmarks. Configuration sweeps reveal phase-dependent bottlenecks and coordination costs. Measured CPU-frequency savings and estimated end-to-end savings are distinct results; the work does not implement a new online DVFS controller or expose a complete PLL/PMIC transition protocol.

## 创新点

1. **将“谁在耗能”纳入同一评测体系。** 在相同推理窗口内测量SoC、CPU、GPU和NPU能量，比仅比较tokens/s或整机电池下降量更容易找到协调问题。它依赖平台已有遥测接口，贡献主要是统一的剖析基础设施和实验组织。
2. **将框架行为与硬件极限联系起来。** 除真实模型外，还测算子、调用、缓存和带宽，使“高峰值算力为什么没有带来高吞吐”得到可检查的机制解释。
3. **用实测配置空间展示调度和DVFS余量。** 作者分别扫描频率、NPU核心/总线工作角及轮询/睡眠配置，展示吞吐与能量的取舍。论文没有提出并部署一套新的强化学习调档器。

这里的LLM是被控程序的工作负载；PowerBench是测量工具。二者均不能直接等同于你要设计的数字DVFS控制器。

## 一句话

先固定真实推理任务，测出每个执行阶段在不同合法配置下的时延与能量，再找性能合格的省能工作点；本文提供这套表征证据，而PLL/PMIC的底层执行协议仍由平台承担。

[返回完整图文精读](note.md) · [专题索引](../index.md)
