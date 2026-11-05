# Ondemand原始设计：中英文摘要与章节导读

[论文页面](https://www.kernel.org/doc/ols/2006/) · [本笔记所用 PDF](https://www.kernel.org/doc/ols/2006/ols2006v2-pages-223-238.pdf) · [标识符](https://www.kernel.org/doc/ols/2006/)

整理日期：2026-11-05。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

This paper describes the original Ondemand governor, its evolution, and frequency coordination in Linux. An SSL web-server workload on a multiprocessor Xeon system illustrates the power-performance tradeoff. The design is deliberately simple and reactive, and its historical parameters and experimental variants should not be treated as current Linux defaults. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究多处理器SSL Web服务，客户连接数由负载机递增的运行时能效。具体程序包括标准SSL Web server/client测试；当前材料未明确到可唯一复建的服务软件版本，不擅自补成Apache/Nginx。作者在4-socket Xeon MP，双核/HT共16逻辑CPU，8GB；Linux2.6时期cpufreq；12V CPU供电支路电流，CR5410S霍尔传感器＋PMD-1208LS USB采集上采用内核定时采样忙闲比：原版超过上阈值升MAX，低于下阈值逐步降；后续直接选可保持约80%忙碌的最低频率，共享域取最高核需求。输入为采样窗口CPU忙闲时间、up/down阈值、频率转换延迟、共享依赖CPU集合，输出为CPUFreq驱动目标频率请求；驱动/硬件匹配电压，不是governor直接写任意电压。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。把轻量忙闲调频放入内核，利用快速P-state切换与多CPU依赖协调；这是一篇理解基线与软件执行路径的原始工程文献，不因年份旧而省略。

## 题名怎么理解

**原题：** The Ondemand Governor: Past, Present, and Future

**中文阅读题：** 用CPU忙闲比触发升频，并由内核与驱动协调共享频域，是后续智能算法必须面对的基线

## 章节导读

| 阅读问题 | 先看材料 | 如何接到下一步 |
| --- | --- | --- |
| 为什么要改现有方案 | 问题背景与动机图 | 确定目标、约束和原有不足 |
| 系统观察什么、控制什么 | 输入输出表＋关键架构图 | 确认数据、模型和执行器真实角色 |
| 方法如何得到动作或估计 | 方法段、公式、算法／模型表 | 明确离线训练与在线流程 |
| 收益是否真实且公平 | 结果图表、统计与测量边界 | 核查基线／目标／分母／开销 |
| 能否用于自己的CPU | 局限、复现计划、三项实验 | 把论文假设变成待验证的工程条件 |

## 阅读中英对照

| 级别 | 术语／关键词 | 直觉、严格含义与易混点 |
| --- | --- | --- |
| A | DVFS / DFS | DVFS同时涉及动态电压与频率；只有时钟变化称DFS。电压能否改变取决于实际供电域。 |
| A | Workload | 真正执行应用计算的程序与输入；本文里的控制器是另一个角色。 |
| A | Controller | 根据观测选择动作的软件／硬件，可运行在同一CPU或独立控制核。 |
| A | OPP | Operating Performance Point，经过允许范围验证的电压—频率组合。 |
| A | Power / Energy | 功率W表示此刻消耗快慢；能量J是对时间积分。低功率不必然低能量。 |
| B | Deadline | 作业必须完成的时刻；平均时延、P95与最大时延各有不同用途。 |
| A | 被控程序 | 标准SSL Web server/client测试；当前材料未明确到可唯一复建的服务软件版本，不擅自补成Apache/Nginx |
| A | 控制策略 | 内核定时采样忙闲比：原版超过上阈值升MAX，低于下阈值逐步降；后续直接选可保持约80%忙碌的最低频率，共享域取最高核需求 |
| B | 控制周期 | 采样受HZ和P-state切换延迟影响；文中示例110000µs/up_threshold80，参数是历史示例非当前Linux建议 |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| Performance与Powersave功率差 | 约10% | 16逻辑CPU服务器SSL负载；CPU12V支路，不是任意整机能量节省 | §6.3，PDF p10–12 |
| 动态策略性能 | 相对静态低频退化更小 | 原文描述dynamic性能损失barely visible；不从曲线虚构统一精确节能率 | Fig4–5，p12 |
| 测量变化 | 约1W run-to-run | 作者因此展示原始曲线未额外平均；不是置信区间 | §6.2，p10 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

E902可实现一个忙闲比阈值控制器作最低复杂度对照，再验证进度/余量特征是否真正改善；无Linux时用裸机计时与安全寄存器接口替代CPUFreq。
