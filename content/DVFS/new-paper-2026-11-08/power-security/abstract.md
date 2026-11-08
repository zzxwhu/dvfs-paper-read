---
title: 电源管理安全：可信OPP许可、执行与遥测｜双语摘要与导读
date: 2026-11-08
tags: [DVFS, reading-guide]
---
# 电源管理安全：可信OPP许可、执行与遥测｜双语摘要与导读

## 原文摘要翻译

过去几年，多个研究团队提出了创新的可信执行环境硬件设计，试图保护应用免受可能被攻陷的特权软件（包括内核）影响。自2017年Tang等人引入一种利用能量管理机制的软件触发硬件攻击以来，这类攻击旨在绕过TEE安全保证、暴露密码密钥等敏感信息，并在近年不断增加。然而，现有RISC-V TEE架构尚未将其纳入威胁模型。Arm TrustZone和Intel SGX等专有实现包含应对措施，但这些措施不利于长期使用，也会限制能量管理机制能力。本文提供此类攻击的综合知识综述，并评估文献中的防护措施。分析指出假定威胁模型与实际威胁之间存在明显安全缺口，现代SoC中这些威胁甚至能够破坏TEE的安全保证。作者呼吁下一代RISC-V TEE将其纳入威胁模型，并希望推动进一步研究。（用户第1页摘要，保留作者稿时点与判断，不作为2026所有平台现状）

## 英文改写（非原摘要）

**English paraphrase (not the original abstract):** This survey treats software-accessible power controls, telemetry, and automatic throttling as shared resources that can cross TEE security boundaries. It organizes prior attacks and countermeasures, separates implemented mechanisms from proposals, and motivates trusted OPP enforcement. The 11-page manuscript is a historical snapshot; it neither evaluates a new controller nor proves current vulnerability of every RISC-V implementation.

## 创新点

1. **把共享电源管理当作跨安全边界的资源。** 保护内存和权限并不自动阻止不可信软件改变共享电压、时钟或观测能量活动。
2. **将故障、侧信道与隐蔽通信放入同一框架。** 同一套DVFS和遥测资源可通过不同路径影响完整性或泄漏信息，不能只防一种异常。
3. **比较防护的作用位置与代价。** 关闭接口、可信监管、动态安全边界、资源隔离和软件加固各自覆盖不同风险；本文没有声称一个无代价万能方案。

这属于综述的分类和研究议程贡献，没有提出并流片一个新DVFS控制器；所汇总的面积、延迟、功率与成功率均应归原始研究。

## 一句话

正常DVFS可以让软件提出性能需求，但合法性、实际电源时钟执行和敏感遥测权限应经过可信边界；只保护任务内存、只封锁一个寄存器或只检查“没崩溃”，都不能自动解决全部风险。

[返回完整图文精读](note.md) · [专题索引](../index.md)
