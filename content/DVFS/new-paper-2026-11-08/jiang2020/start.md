---
title: Jiang2020：离线扫档与每帧DVFS执行流程｜从零入门
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# Jiang2020：离线扫档与每帧DVFS执行流程｜从零入门

先区分离线选活动点与在线活动/空闲切换。按图8走一帧：完成事件触发降频，余量足够才降压，下一帧前恢复。实际平台ZCU104，38%能效提升不是38%能量下降，UEE表值待澄清。

## 一句话

先用真实程序遍历V/f建立表，再根据帧周期选择活动工作点；运行时在任务完成后进入低频空闲，有足够时间才降压，并在下一帧前恢复，而不是每次运行都重新遍历所有档位。

## 先理解研究问题

### 先回答你一直追问的“什么时候调、凭什么调”

**English paraphrase (not the original abstract):** The paper integrates software-accessible FPGA clock and power controls with the SkyNet detector, characterizes voltage–frequency operating points, and evaluates both per-frame efficiency and fixed-rate operation. The runtime policy alternates between an offline-selected active point and an idle state, applying voltage scaling only when sufficient slack exists. Results require careful separation of PL power, system energy, quality tolerance, and cross-platform baselines.

这里有两件不同的工作：**离线选择活动工作点**，以及**在线按每帧状态切换**。前者可在运行前完成；后者在程序实际运行过程中反复发生。因此“活动档预先确定”与“运行时有动态调节”完全可以同时成立。

论文的负载是目标检测加速器。它由真实电路在真实FPGA上处理图像，不是虚拟程序速度的动画；控制代码在PS的A53/Linux运行。你若改成CPU程序，真实程序同样可受真实CPU工作点影响，但需要平台允许控制对应时钟和电源。

### 两种应用目标为什么选出的档位不同

|应用情形|目标|关键约束|为什么不能只找最低功率|
|---|---|---|---|
|有事件才处理一帧|尽量少用能量完成这帧|结果质量与任务完成|频率太低会让PS和其他模块持续耗能更久|
|相机固定产生帧|最小化整个帧周期平均功率|必须在下一帧前完成及恢复|需要同时计算活动、空闲和调档成本|

降低瞬时功率不一定降低任务总能量；最快完成也不一定最低平均功率。要把目标写清楚，才能判断一个工作点是好还是坏。

### 最少术语

|层次|术语|直观和严格含义|
|---|---|---|
|A|PS/PL|PS是片上处理器系统，运行控制软件；PL是可编程逻辑，本篇负载在PL|
|A|频率、电压、OPP|频率影响单位时间可推进的时钟周期；电压影响功耗和延迟；OPP是被允许的电压频率组合|
|A|功率W、能量J|W表示耗能速率，J表示累计消耗；相同功率下运行更久，能量更高|
|B|MMCM|FPGA专用时钟管理资源，配置后产生工作时钟；不是普通RTL实现的模拟PLL|
|B|PMIC/PMBus|前者实际转换与调节供电，后者是控制/监测协议，经I²C兼容链路访问|
|B|FPS/FPJ|每秒处理帧数/每焦耳处理帧数，分别表示速度和能效|
|C|空闲余量|帧周期减去活动与切换后剩余的时间，决定是否有足够时间降压及恢复|
|C|质量边界|当前数据集的IoU何时变化；不等于所有输入、所有电路内部状态均无错误|

阅读顺序：图1确定控制与负载位置，图3/6了解执行器，图8跟一帧走完，最后读能量/质量曲面和表2。

## 五步阅读

1. [谁是被控对象与平台](note.md#数据与任务定义)。
2. [跟着输入、操作、输出读方法](note.md#方法主线)。
3. [对齐基线与实验结果](note.md#关键结果)。
4. [检查哪些参数和证据还不够](note.md#局限)。
5. [按复现计划从模型到硬件验证](note.md#我的笔记)。

[返回完整图文精读](note.md) · [专题索引](../index.md)
