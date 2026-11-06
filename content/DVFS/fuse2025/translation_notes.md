---
title: "FUSE：手机LLM协同频率：中英文摘要与章节导读"
tags: ["DVFS", "GPU", "CV", "LLM", "E902"]
date: "2026-11-06"
source_sha256: "7805115c2cb1bab137a76f2416e1620119ddc741ff5fb09dc942a5f8a9a4fe28"
---

[论文页面](https://arxiv.org/abs/2507.02135v1) · [本笔记所用 PDF](https://arxiv.org/pdf/2507.02135v1) · [标识符](https://doi.org/10.48550/arXiv.2507.02135)

整理日期：2026-11-06。**读者原创中文解读；原图归论文作者／出版方。未运行作者实验，不是独立复现。**

**范围说明：以下英文与中文都是读者改写，不是原文摘要逐字引用，也不是全文翻译。** 原始摘要请打开论文页面或PDF首页。

## English abstract paraphrase

FUSE studies mobile LLM inference under independent CPU, GPU and memory governors. It finds that CPU kernel-submission delays can cause a mutually reinforcing CPU/GPU downclocking cycle. A model-specific offline search chooses CPU/GPU settings for latency or energy objectives and applies them at phase boundaries, while leaving the memory governor at its default setting. This is a reader-written paraphrase, not the original abstract.

## 中文摘要改写

本文研究手机本地GPU卸载的LLM自回归推理，单请求顺序执行的运行时能效。具体程序包括llama.cpp b2202/OpenCL＋CLBlast；TinyLlama1.1B、DS-R1-Distill-Qwen1.5B、Refact1.6B、StableLM2.7B、Phi2 2.7B、Llama2 6.7B，4bit；ShareGPT抽200请求。作者在root/opened Pixel7与7Pro，TensorG2/MaliG710、Android13；Monsoon旁路电池、0.2ms采样，屏幕关闭；测设备功耗上采用基于U形能量曲线的两步离线搜索：先GPU至能量/时延边界，再CPU细调；5种prompt桶＋1种decode配置；相位切换查表，无RL。输入为模型、prompt长度桶、当前prefill/decode通知、离线E/T曲线、用户每token能量预算G1或时延目标G2，输出为CPU/GPU锁定频率pair；memory governor默认；G1最小时延/G2最小能量。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。以受控实验揭示多governor相互作用，提出简单可部署的阶段感知协同控制；复杂神经控制器不是必要条件。

## 题名怎么理解

**原题：** Dissecting the Impact of Mobile DVFS Governors on LLM Inference Performance and Energy Efficiency

**中文阅读题：** 解释手机CPU/GPU独立governor互相降频的恶性循环，再通过离线两步搜索为prefill/decode配置协同频率

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
| A | 被控程序 | llama.cpp b2202/OpenCL＋CLBlast；TinyLlama1.1B、DS-R1-Distill-Qwen1.5B、Refact1.6B、StableLM2.7B、Phi2 2.7B、Llama2 6.7B，4bit；ShareGPT抽200请求 |
| A | 控制策略 | 基于U形能量曲线的两步离线搜索：先GPU至能量/时延边界，再CPU细调；5种prompt桶＋1种decode配置；相位切换查表，无RL |
| B | 控制周期 | 安装/部署时每模型离线搜索；运行时只在prefill/decode边界换表，不是连续在线训练/逐tokenMPC |
| B | 证据边界 | 实测、硬件仿真、功耗模型是不同证据，见平台与结果表。 |

## 原文数字应怎样转述

| 指标 | 原文报告 | 条件／分母／边界 | 证据位置 |
| --- | --- | --- | --- |
| ShareGPT同能量预算G1 | TTFT降低7.0%–16.9%；TPOT降低25.4%–36.8% | TinyLlama/DS-Qwen/StableLM，200请求，近似iso-energy；不是节能百分比 | Fig14/§6.2，p12 |
| ShareGPT同TTFT目标G2 | 总能量/电量代理降低4.2%–14.3% | 三个模型；论文部分以mAh写energy drain，电量转J需电压 | Fig14，p12 |
| 固定长度同阶段时延G2 | prefill每token能量−6.9%、decode−10.3%均值 | 六模型固定长度，不能替代真实trace范围 | Fig13，p12 |

不要省去基线、平台、约束和测量边界。摘要级概述与全文结果不一致时，以明确标注版本的正文实验条件为准。

## 对你课题最有用的一句话

如果有GPU/手机实验权限，适合作为“软控软”的清晰案例：软件策略控制运行推理软件的真实硬件。CPU单平台可借鉴阶段分表与小规模离线搜索；E902只迁移阶段观测/安全OPP，不照搬Android三频域。
