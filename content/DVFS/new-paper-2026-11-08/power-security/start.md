---
title: 电源管理安全：可信OPP许可、执行与遥测｜从零入门
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# 电源管理安全：可信OPP许可、执行与遥测｜从零入门

先把性能策略、OPP许可、硬件执行和遥测分开。本文是2024作者稿综述，表中数字来自原始研究；2025期刊扩展仅核身份，不能称已读。合法端点之外还要验证过渡态。

## 一句话

正常DVFS可以让软件提出性能需求，但合法性、实际电源时钟执行和敏感遥测权限应经过可信边界；只保护任务内存、只封锁一个寄存器或只检查“没崩溃”，都不能自动解决全部风险。

## 先理解研究问题

### 给初学者的阅读地图

**English paraphrase (not the original abstract):** This survey treats software-accessible power controls, telemetry, and automatic throttling as shared resources that can cross TEE security boundaries. It organizes prior attacks and countermeasures, separates implemented mechanisms from proposals, and motivates trusted OPP enforcement. The 11-page manuscript is a historical snapshot; it neither evaluates a new controller nor proves current vulnerability of every RISC-V implementation.

TEE可理解为同一机器中的受保护运行区域：即使普通操作系统不可信，敏感应用仍希望得到隔离。这里的难点是它与外部程序可能共用CPU、电源、时钟及热/功率预算。外部软件未必能读敏感内存，却可能通过这些共享资源影响或观察执行。

本文最贴近你的课题的问题是：**软件选出了一个OPP后，谁有权决定它可以执行？** 如果PLL/PMIC可被另一条路径绕开，正确的正常策略并不保证整个系统始终处于合法状态。

### 基础与进阶术语

|术语|含义与课题联系|
|---|---|
|TEE、普通环境RE|受保护环境与其余可能不可信的软件环境；用户稿用RE记后者|
|TCB|保证安全所必须信任的软硬件集合；加入监管器会增加其职责与验证成本|
|故障攻击FIA|通过不合适的电压/时钟导致错误；对应合法OPP、时序与保护问题|
|侧信道SCA|不直接读秘密，而从功率、频率或耗时等相关信号推断；对应遥测与策略可观测性|
|隐蔽通信|两个合作程序利用非正式通道传递信息；与无意泄漏的侧信道不同|
|可信代理|不可信软件提出请求，由较可信固件/硬件验证后执行；“谁选档”和“谁批准”可以分离|
|PVT与老化|工艺、电压、温度和时间变化影响真实安全边界，静态表不一定覆盖全部状态|

## 五步阅读

1. [谁是被控对象与平台](note.md#数据与任务定义)。
2. [跟着输入、操作、输出读方法](note.md#方法主线)。
3. [对齐基线与实验结果](note.md#关键结果)。
4. [检查哪些参数和证据还不够](note.md#局限)。
5. [按复现计划从模型到硬件验证](note.md#我的笔记)。

[返回完整图文精读](note.md) · [专题索引](../index.md)
