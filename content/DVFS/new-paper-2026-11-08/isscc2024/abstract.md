---
title: ISSCC2024：硬件电压闭环与PMIC、SRAM协调｜双语摘要与导读
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# ISSCC2024：硬件电压闭环与PMIC、SRAM协调｜双语摘要与导读

## 原文摘要翻译

用户提供的会议摘要集正文没有单列Abstract。以下忠实翻译开头概述段，不把后文判断补写成作者摘要。

面向下一代旗舰智能手机，本文介绍一种新的三档CPU子系统。已有研究发表过三档CPU子系统，而本工作介绍的三个档次均使用乱序执行CPU。在4nm CMOS工艺中，四个高能效核心配合三个均衡性能核心和一个高性能核心。通过改进前作的DVFS控制机制，实现了完全由硬件承担的DVFS控制。借助面向SRAM供电的自动双轨均衡器，以及面向核心供电的新高带宽电压控制器，消除了供电顺序对软件的依赖。更快的响应和PMIC节能工作模式带来功耗收益。高频访问的一级缓存采用全CMOS单轨存储阵列，减少功耗；降低标准单元中间金属层电阻与电容的版图技术提升了最高时钟频率。芯片照片见图2.1.7，单线程功耗与性能对照见图2.1.1。（PDF第1页开头）

## 英文改写（非原摘要）

**English abstract paraphrase, not the original abstract:** This measured 4nm mobile SoC moves adaptive voltage control into hardware. A high-bandwidth voltage controller coordinates PMIC updates with a ring-oscillator-based frequency loop, while automatic rail selection protects SRAM supply requirements. The reported voltage and power benefits depend on the evaluated workloads and combined chip-level improvements.

## 创新点

1. **将前作的软件自适应电压调整移入HBVC硬件环。** 它接收目标频率、当前频率和环振编码，计算电压调整量，直接通过专用SPI通知PMIC。它解决的是目标频率已给定后怎样快速、稳定地找到供电电压。（第1页）

2. **双轨均衡器DREQ自动保证SRAM供电。** 比较CPU电压与SRAM最低供电轨，选择较高者并加入迟滞，减少软件排序和专用LDO资源。（图2.1.5）

3. **把PMIC降压方式纳入系统共同优化。** 取消主动放电，让负载自然消耗电荷，减少降压阶段的浪费；这要求时钟和供电控制能配合该响应方式。（图2.1.6）

论文还包含乱序微架构、缓存阵列和标准单元改进。它们共同贡献最终整机收益，因此不能把全文节能数字都归因于上述控制器。

## 一句话

软件提出“CPU需要跑多快”，硬件电压环和频率环协同实现该目标，存储电源选择电路与PMIC工作模式负责使这一过程更安全、更省电。

[返回完整图文精读](note.md) · [专题索引](../index.md)
