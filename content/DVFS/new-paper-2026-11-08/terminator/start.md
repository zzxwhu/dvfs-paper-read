---
title: Terminator：FPGA执行链与正确性边界｜从零入门
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# Terminator：FPGA执行链与正确性边界｜从零入门

先沿PS→AXI→MMCM看时钟，再沿PS→I2C/PMBus→板上PMIC看电压。读图5时区分不崩溃与算得对；本篇研究故障安全，没有新的节能governor。

## 一句话

PS软件确实可以控制FPGA的时钟资源和板上稳压器，但不能把所有“还能跑”的电压频率组合交给正常控制策略，必须同时保证输出正确性和切换安全。

## 先理解研究问题

### 阅读地图：它怎样回答你的疑问

**English paraphrase (not the original abstract):** The paper builds a software-controlled voltage and frequency framework on an Ultra96-V2 FPGA platform and evaluates reliability boundaries of the SkyNet accelerator. MMCM configuration controls the PL clock, while a board PMIC supplies voltage through a separate control path. Results show that silent output corruption can occur without a hang or crash. The useful lesson for a normal DVFS controller is to restrict legal OPPs and validate both steady states and transitions; the paper is not an energy-saving governor.

按图4看平台整体，图2看调频，图3看调压，再读图5的不同边界。最后看图7及局部实验的指标定义。你会看到DVFS并不是一个悬在CPU外面的“神奇算法”：软件提出状态请求，数字接口配置执行器，实际硬件时钟/电源改变，程序速度与正确性随之受影响。

文中的被控计算对象是PL中的SkyNet加速器，不是PS里的ARM处理器本身。PS承担控制职责。对于你的E902，若E902处于被调电压/时钟域，则需要明确谁在稳定域执行控制代码、谁负责配置PLL/PMIC；不能直接照搬“PS管PL”就假设CPU能在任意停钟或低压状态自救。

### 三个成功层次不能混为一谈

|现象|能说明什么|不能说明什么|
|---|---|---|
|配置寄存器读回正确|软件事务写到了某处|电压已稳定、PLL已锁定、负载已切到新状态|
|程序done或未触发watchdog|没有明显卡住|算术结果或检测输出正确|
|与正常配置输出一致|这组输入下未发现硬件扰动差异|模型语义完全正确，或所有输入/PVT都安全|

静默数据错误SDC指没有通过明显崩溃显露出来的错误结果。合法DVFS设计需要把正确性放进约束，不应只最小化功率或让程序不超时。

## 五步阅读

1. [谁是被控对象与平台](note.md#数据与任务定义)。
2. [跟着输入、操作、输出读方法](note.md#方法主线)。
3. [对齐基线与实验结果](note.md#关键结果)。
4. [检查哪些参数和证据还不够](note.md#局限)。
5. [按复现计划从模型到硬件验证](note.md#我的笔记)。

[返回完整图文精读](note.md) · [专题索引](../index.md)
