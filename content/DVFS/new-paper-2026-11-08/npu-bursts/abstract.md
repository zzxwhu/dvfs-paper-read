---
title: NPU融合功率尖峰：负载塑形与DVFS保护｜双语摘要与导读
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# NPU融合功率尖峰：负载塑形与DVFS保护｜双语摘要与导读

## 原文摘要翻译

移动设备越来越依赖实时NPU推理来运行相机和感知负载。然而，在低电压条件下，单次推理可能在供电网络中造成瞬态电压跌落，迫使PMIC启动动态电压频率调节，并增加时延。本文在一款商业手机上测量了这一现象。作者表明，移动NPU编译器中激进的算子融合能够形成大型整体式超层，集中执行这些超层会产生很高的峰值电流。尖峰会使DVFS开始介入的电压上移，缩小低电压运行裕量。作者还评估了一种实用的黑盒缓解方法：由测量引导，在编译前改写计算图；部署版本在选定的峰均比热点处插入屏障，阻止供应商NPU编译器进行有害的超层合并。在Snapdragon 8 Gen 3上使用MobileNetV4、768×768输入和ImageNet-1k时，峰值电流从3.12A降至1.94A，时延开销为3.76%；方法在更低电压区间仍保持稳定时延，并使推算得到的DVFS裕量变化约173mV。（第1页摘要）

## 英文改写（非原摘要）

**English paraphrase (not the original abstract):** This measurement study links aggressive operator fusion on a commercial mobile NPU to peak-current bursts and low-voltage protection behavior. An offline, PAPR-guided graph rewrite inserts jointly compilable Q–DQ barriers to reshape execution. Peak-current reduction comes with latency, energy, and quantization tradeoffs; the inferred voltage margin is an exploratory estimate rather than a transferable hardware law.

## 创新点

1. **把编译器融合与供电瞬态联系起来。** 融合通常为了少搬数据、提高速度；本文关注其集中计算是否造成电流尖峰，以及尖峰如何使低压保护更早介入。
2. **用测量引导少量图边界改写。** 先筛选能编译运行的边，再根据电流热点排序，逐个检查屏障组合，避免对全部层粗暴拆分。
3. **与厂商限频配置直接比较。** 把拆分和限频分开及组合实验，展示峰值、时延、能量并非同一目标，也展示低峰均比模型可能不值得改写。

这是一种负载塑形方法，与DVFS保护发生直接联系，但没有重新设计PMIC、PLL，也没有实现新的在线OPP选档算法。其价值在于补上“程序怎样制造供电压力”这一环。

## 一句话

先找编译融合后最容易制造电流尖峰的执行区间，再在少量可行边插入不能被优化掉的屏障，使负载不那么集中，从而减少低输入电压下既有保护导致的性能恶化。

[返回完整图文精读](note.md) · [专题索引](../index.md)
