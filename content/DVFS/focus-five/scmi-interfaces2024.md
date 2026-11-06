---
title: "05 软件已经写了寄存器，频率何时才生效"
date: "2026-11-07"
tags: [DVFS, E902]
---

[返回五篇实验手册](guide.md) · [论文原文](https://www.mdpi.com/1996-1073/17/22/5778) · [所用版本PDF](https://www.research-collection.ethz.ch/server/api/core/bitstreams/5fab7af7-3ebf-4ae4-93bb-9fea8875e6e3/content)

**Performance Characterization of Hardware/Software Communication Interfaces in End-to-End Power Management Solutions of High-Performance Computing Processors**  
Antonio del Vecchio, Alessandro Ottaviano, Giovanni Bambini, Andrea Acquaviva, Andrea Bartolini。ETH仓储正式版，含1页封面共16页；本文所有PDF页码比正文印刷页多1。

你工程里的 CPU 写完 FBDIV，运行速度究竟从哪一刻开始改变？这篇研究把注意力放在选频之后。上层已经知道想要哪个性能档。它仍要跨过驱动、消息传输、底层固件和周期性控制任务，才可能使被控对象真正换档。一个算法即使总能选对档，若档位晚于计算阶段结束才生效，收益也会消失。

![Fig1 真实部件与HIL映射](images/scmi-interfaces2024-fig1.png)

[放大原图表](images/scmi-interfaces2024-fig1.png) · [原文 Fig1，PDF 第 6 页](https://www.research-collection.ethz.ch/server/api/core/bitstreams/5fab7af7-3ebf-4ae4-93bb-9fea8875e6e3/content#page=6)。图表来自该论文作者。

## 跟踪一次请求

Linux 高层决定新的性能等级，通过 CPUFreq/SCMI 驱动发送 perf_level_set 消息。邮箱保存消息，用中断通知底层。底层中断服务先接收并转交，固件解码任务再处理请求。默认电源控制固件按 500 µs 周期读取目标，实际应用还要等后续调度。**消息到达、消息应答、频率生效是三个时刻。** 把它们存成一个 ready 位，会让实验无法定位慢在哪里。

![Fig2 SCMI调用时序](images/scmi-interfaces2024-fig2.png)

[放大原图表](images/scmi-interfaces2024-fig2.png) · [原文 Fig2，PDF 第 7 页](https://www.research-collection.ethz.ch/server/api/core/bitstreams/5fab7af7-3ebf-4ae4-93bb-9fea8875e6e3/content#page=7)。图表来自该论文作者。

优化有两处。第一处改变“何时发现需要调频”，由阶段事件触发上层，减少等待下次轮询的时间。第二处改变“底层怎样应用请求”，对符合条件的降频提供快速通路。升频仍受功率、温度、电压等条件约束。论文用合成的计算密集与访存密集阶段区分需求。前者更依赖计算频率，后者部分时间花在等待数据，才有机会用低频换能量。

## 两个实验各测什么

![Table1 通信与解码统计](images/scmi-interfaces2024-table1.png)

[放大原图表](images/scmi-interfaces2024-table1.png) · [原文 Table1，PDF 第 10 页](https://www.research-collection.ethz.ch/server/api/core/bitstreams/5fab7af7-3ebf-4ae4-93bb-9fea8875e6e3/content#page=10)。图表来自该论文作者。

通信实验让高层以 1 秒间隔发送无拥塞请求，并另做 1000 次固件解码测量。T1 平均 70.5 µs 是 Linux 发送段。固件解码 263 个周期，20 MHz 的一个周期是 0.05 µs，相乘为 13.15 µs。两数都不能单独当作从负载变化到时钟改变的时间。周期换算时必须用运行固件的时钟。

![Table2 应用性能改善](images/scmi-interfaces2024-table2.png)

[放大原图表](images/scmi-interfaces2024-table2.png) · [原文 Table2，PDF 第 12 页](https://www.research-collection.ethz.ch/server/api/core/bitstreams/5fab7af7-3ebf-4ae4-93bb-9fea8875e6e3/content#page=12)。图表来自该论文作者。

控制质量实验使用 500 个各 20 ms 的阶段，基准模型时间 10 s。按周期发现负载时平均控制延迟为 2.20 ms，改事件发现为 1.35 ms，进一步优化底层后为 0.77 ms。对一个 20 ms 阶段，2.20 ms 已占 11%，0.77 ms 占 3.85%。这两个比例是等待占阶段长度的换算，不能直接当作应用加速比。优化降频 114 µs，升频约 1.42 ms。Table 2 的应用加速 2.89% 属于模型应用及指定基线。论文为时间尺度匹配让仿真相对控制器放慢 25 倍，并加入 1.7 ms 人工转发延迟。复建必须把模型时间与主机墙钟分开。

## 怎样复建这一篇

1. **先写离散事件实验。** 生成带起止时间的计算/访存阶段，让上层分别按固定周期和阶段事件产生相同目标档序列。底层设置邮箱、解码、周期应用三个事件。固定随机种子和阶段序列，分别只改上层触发、只改底层降频通路，再两处一起改。
2. **每条命令保存五个时间戳。** 负载变化、上层请求、底层接收、底层应答、实际频率变化。最后一个减第一个得到端到端 CD。把请求恰好安排在底层轮询前后各一次，检查延迟分布能否反映等待一个周期的差别。给升频、降频分别做直方图。
3. **原平台复建。** ZCU102 上 A53/Linux 跑上层，FPGA 上的 ControlPULP 跑底层固件，被控处理器及功耗/热行为用模型提供。若只有 PC，可重建事件时序与比较方向；若要复现微秒级固件数字，需要同硬件、时钟、软件版本、优先级和时间尺度映射。
4. **接到你的 E902。** 先令接口只有 request、accepted、applied 和 error 四种观察量。用固定参考时钟测请求至生效，避免用正在变频的时钟给自己计时。仿真加入 PLL 失锁、PMIC 忙、写成功但电压未稳三种情形。验证成功条件是动作按顺序生效、任务输出正确、超时后回安全档。此处为毕业设计的简化路径，完整 SCMI 协议属于原论文平台。

## 摘要改写与复建资料

把“写入新频率”拆成Linux发请求、邮箱传输、固件解码、控制任务计算和执行器生效。。Linux发送T1：均值70.5µs，条件为HLC1.2GHz；非完整控制延迟。

The study measures the path from Linux frequency requests to a firmware power controller through SCMI. Hardware-in-the-loop experiments separate communication latency from control-policy delay and evaluate periodic, event-driven and optimized low-level policies. Fast application of safe frequency decreases reduces delay, whereas increases remain constrained. The plant and energy effects are emulated. This is a reader-written paraphrase.

**代码与复现边界**　论文依托[ControlPULP平台](https://github.com/pulp-platform/control-pulp)；本篇完整Linux补丁、实验脚本与对应commit当前未全部核验，不假定基础仓库包含所有扩展。

[完整编号图表索引](../scmi-interfaces2024/figs_notes.md) · [原四报告中的技术笔记](../scmi-interfaces2024/paper_notes.md) · [配套核算脚本](https://github.com/zzxwhu/dvfs-paper-read/blob/main/examples/focus-five/check_examples.py)
