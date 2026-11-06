# E4：视频早退出＋DVFS：中英文摘要与章节导读

[论文页面](https://ojs.aaai.org/index.php/AAAI/article/view/32104) · [本笔记所用 PDF](https://yangece.github.io/papers/conference/AAAI2025-E4.pdf) · [标识符](https://ojs.aaai.org/index.php/AAAI/article/view/32104)

整理日期：2026-11-06。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

E4 combines temporal feature accumulation, attention-based early exits and joint CPU/GPU frequency search for edge video analytics. Neural gates decide how much inference work to execute, while a just-in-time coordinate search profiles frequency schedules. Energy and latency gains must be interpreted alongside recognition quality and the reduced amount of executed work. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究边缘视频动作识别，多帧/多出口DNN推理的运行时能效。具体程序包括EfficientNet-B0、MobileNet-v2特征骨干＋5出口；ActivityNet-v1.3、Mini-Kinetics；ImageNet预训练。作者在Jetson Nano/TX2/Xavier NX/Orin Nano/AGX Orin五设备；Python3.6、nvpmodel；jetson-stats整设备遥测；早退网络另用4×RTX3080离线训练上采用两层LSTM累计特征＋注意力/MLP早退gate；JIT coordinate descent search逐层找CPU-GPU频率；nvpmodel执行，非RL governor。输入为历史与当前帧累计特征、注意力权重、gate置信/退出条件、可用CPU/GPU频档、剖析每层配置能量，输出为DNN退出位置（改变执行量）＋退出前逐层CPU/GPU频率pair；视频类别。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。把时序视频复杂度、退出位置与逐层频率搜索结合；优化空间既有少算几层，也有每层硬件运行档。

## 题名怎么理解

**原题：** E4: Energy-Efficient DNN Inference for Edge Video Analytics via Early Exiting and DVFS

**中文阅读题：** 先通过时序注意力确定视频动作识别所需的退出位置，再用坐标下降为退出前各层选CPU/GPU频率

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
| A | 被控程序 | EfficientNet-B0、MobileNet-v2特征骨干＋5出口；ActivityNet-v1.3、Mini-Kinetics；ImageNet预训练 |
| A | 控制策略 | 两层LSTM累计特征＋注意力/MLP早退gate；JIT coordinate descent search逐层找CPU-GPU频率；nvpmodel执行，非RL governor |
| B | 控制周期 | 按视频帧/网络层动作；频率执行毫秒级，JIT搜索开销需单计；不是逐周期硬实时保证 |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| 主要正文结果 | EfficientNet能量−20%–37%、速度1.3–2.2×；MobileNet−18%–30%、1.4–1.9× | 五Jetson/两数据集，与EENet/zTT/Ring比较；摘要最高2.8×不冒充所有主图结果 | §Performance/Fig3，p5–6 |
| 摘要总体 | 平均节能26%，最高速度2.8× | 联合早退和调频；保留正文分组与精度条件 | 摘要，p1 |
| 能量换算示例 | 约217.98mJ→164.01mJ | Table2 Eff-B0无策略6.3ms/34.6W，单DVFS7.1ms/23.1W；乘积教学换算，约−24.8%，不是新实测 | Table2，p7 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

若选CV应用，建议先CPU小型分类模型固定网络/固定精度做DFS，再加早退作为独立实验变量。E902可尝试小型模型或前处理；Jetson更适合复建完整E4，不能把大平台频率表直接复制到E902。
