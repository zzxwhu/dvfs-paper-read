---
title: "02 两个频档怎样由强化学习选择"
date: "2026-11-07"
tags: [DVFS, E902]
---

[返回五篇实验手册](guide.md) · [论文原文](https://doi.org/10.48550/arXiv.2409.19434) · [所用版本PDF](https://arxiv.org/pdf/2409.19434v3)

**Energy-Efficient Computation with DVFS using Deep Reinforcement Learning for Multi-Task Systems in Edge Computing**  
Xinyi Li, Ti Zhou, Haoyu Wang, Man Lin。arXiv2409.19434v3，2025-05-21，13页；不混用初版摘要。

假设 CPU 正在压缩一张图，几毫秒后又要处理音频。此刻利用率都可能是 100%，但“刚开始处理”和“已经接近最后期限”需要的档位不同。本文研究多个周期任务共享一个频率域时，怎样把历史进度交给一个选频程序。神经网络只负责给候选动作打分，JPEG、排序或 FFT 才是消耗计算时间的被控程序。

## 从观测到实际动作

![Fig2 方法整体流程](images/multitask-drl2024-fig2.png)

[放大原图表](images/multitask-drl2024-fig2.png) · [原文 Fig2，PDF 第 2 页](https://arxiv.org/pdf/2409.19434v3#page=2)。图表来自该论文作者。

一个控制窗口结束，收集上个窗口的运行频率、各核最大/平均利用率、经过的时间，以及应用报告的任务开始/完成标签。用“窗口长度×平均利用率”累加忙碌时间，用墙钟时间累加已经过去多久。两者分开后，模型有机会分辨“整个周期一直在算”和“过去很久但中间多次等待”。标签在运行时获得。任务最终是否超时，要等任务完成后才知道。

作者比较两种编码。TEM 为每个正在运行的任务累加它在各个“频率×负载”格子里的驻留时间，再送入多层感知机。TEGM 把公共频率/负载历史交给 GRU，让它维护压缩过的历史状态，再与任务标签等特征合并。前者容易手算，任务变多时输入维度也会长大。后者增加一次时序网络推理。v3 的 GRU 输入维度 2、隐藏状态 6，多层感知机两个隐藏层各 30 个节点，较大任务集另测 PROL。

![Fig6 内核推理流程](images/multitask-drl2024-fig6.png)

[放大原图表](images/multitask-drl2024-fig6.png) · [原文 Fig6，PDF 第 5 页](https://arxiv.org/pdf/2409.19434v3#page=5)。图表来自该论文作者。

固定同一个状态 s，分别算 Q(s,低档) 和 Q(s,高档)。Q 表示这个动作连同后续决策的预期累计奖励。部署时取分数较大的档。训练时偶尔探索另一个动作，把整回合的状态、动作、下一状态和回报送到用户态。DDQN 用在线网络挑下一动作，用目标网络评价它，随后更新权重并传回内核。控制周期内只做前向计算。

奖励把低频驻留比例和平均利用率结合起来，频率代价以 f³ 归一化。回合末根据任务超时程度减分，超过阈值后回报归零。**reward 是训练信号，瓦和焦耳是评价信号。** 一个以低频为偏好的策略有可能得到好分，同时因为运行过久而增加总能量。Algorithm 3 的超时比书写与叙述需核对，复建时应记录采用的公式及阈值。

## 实验为什么要同时读两张表

![TableVI 随机任务功率](images/multitask-drl2024-tablevi.png)

[放大原图表](images/multitask-drl2024-tablevi.png) · [原文 TableVI，PDF 第 11 页](https://arxiv.org/pdf/2409.19434v3#page=11)。图表来自该论文作者。

Jetson Nano 2GB 实验使用板级 USB 功率计。随机三任务组的平均功率由 2.17700 W 降到 1.84490 W，1−1.84490/2.17700≈15.25%。同页 Table VII 中，85.50% 落在按时完成一栏，10.67% 落在**超过期限 5%** 的一栏。全部超时比例按表为 14.50%。这三个数分别回答平均功率、严重超时、所有超时。若两策略运行时间不同，另需积分能量才能比较 J/任务。

## 怎样复建这一篇

1. **先实现状态记录器。** 用用户态驱动三个重复乘法任务。论文例子相对启动时刻为 0、0.3、0.7 s，各自相对期限为 0.3、0.4、0.5 s。记录 release、start、finish、相对期限。第三个任务的绝对期限是 1.2 s。用这个例子检查超时统计是否误把绝对时刻当运行时长。
2. **无板验证。** 构建任务进度模拟器，每次按选定档位推进剩余工作量，更新标签和驻留时间。高低各跑一遍同一到达序列，检查动作能否改变完成时刻。仅有一条真实运行轨迹时，直接改写轨迹里的频率无法还原另一个动作的结果。
3. **训练并冻结。** 先用两档固定基线和利用率阈值检查环境。再照 Algorithm 1–3 实现编码和终回合奖励，分别训练 TEM 与 TEGM，保存随机种子。原文每轮收集三次，训练 400 轮，按任务组约 1.67–1.89 小时。达到轮数只说明训练结束。留出整组任务及到达序列后再评估。
4. **原平台核验。** 对齐 Jetson Nano、Linux 4.9、应用及功率计边界。分别做原文基线对照和所有策略共用两档的公平对照。计入最大 0.16 ms 的推理开销。保留平均功率、积分能量、按时比例、超时幅度和策略执行时长。论文关联 tinyagent 内核引擎，具体档值、驱动补丁与采样周期需从对应配置核对。

## 摘要改写与复建资料

把任务开始/完成标签和负载历史编码给DDQN，使共享CPU频率能考虑多个任务的软期限。固定任务集相对Ondemand：约7%/3%/4%降低，条件为分别3任务PRO、5任务PRO、8任务PROL；图15称功率，正文又称energy，应保留术语不一致。

This work extends utilization-based learned CPU governors to periodic task sets with multiple deadlines. Task-state labels and temporal encoders feed a Double DQN trained in user space and evaluated in the kernel. Jetson Nano experiments compare recurrent and non-recurrent encodings, including random task sets. Reported savings and deadline violations must be examined together. This is a reader-written paraphrase, not the original abstract.

**代码与复现边界**　论文链接 https://github.com/coladog/tinyagent 为相关内核引擎；未运行本篇多任务代码或确认该仓库某提交即可重现实验。

[完整编号图表索引](../multitask-drl2024/figs_notes.md) · [原四报告中的技术笔记](../multitask-drl2024/paper_notes.md) · [配套核算脚本](https://github.com/zzxwhu/dvfs-paper-read/blob/main/examples/focus-five/check_examples.py)
