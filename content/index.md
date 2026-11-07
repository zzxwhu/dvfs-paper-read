---
title: "DVFS论文精读：IC控制器、PLL／PMIC与软硬件协同"
date: "2026-11-06"
---

[初学者优先：用Jiang2020看懂DVFS完整执行流程（含原图）](DVFS/jiang2020-beginner/guide.md)

[IC方向新精选10篇：ISSCC／JSSC、数字控制器与co-design](DVFS/ic-codesign-selected-10.md)

当前课题主线：数字DVFS控制器调用现有PLL/PMIC，优先阅读IC领域论文。下方保留此前CPU/GPU应用文献作为背景。

从零理解CPU/GPU频率、能量与闭环，再结合CV/LLM等应用的原图、公式与实验边界选择实现路线；保留CPU/E902迁移分析。

[五篇重点精读与复现实验手册：从软件选档到 E902 执行](DVFS/focus-five/guide.md)

## 新增第三批：GPU、CV、LLM应用与30篇比较

[30篇：算法、负载、程序、平台、结果](DVFS/comparison-30-papers.md) · [CSV](DVFS/data/dvfs-30.csv) · [新10篇阅读路线](DVFS/reading-map-gpu-cv-llm-2026-11.md)

三批30篇，加独立旧JSA2023共31篇。GPU/CV/LLM现可作为应用候选，最终课题尚未确定；全部为原文阅读与分析，未独立复现。

| 新增论文 | 从零入门 | 图文精读 | 图表索引 | 双语摘要 |
| --- | --- | --- | --- | --- |
| Zeus：训练能量优化 | [入门](DVFS/zeus-nsdi2023/ELI5_notes.md) | [精读](DVFS/zeus-nsdi2023/paper_notes.md) | [图表](DVFS/zeus-nsdi2023/figs_notes.md) | [摘要](DVFS/zeus-nsdi2023/translation_notes.md) |
| Perseus：训练流水线频率调度 | [入门](DVFS/perseus-sosp2024/ELI5_notes.md) | [精读](DVFS/perseus-sosp2024/paper_notes.md) | [图表](DVFS/perseus-sosp2024/figs_notes.md) | [摘要](DVFS/perseus-sosp2024/translation_notes.md) |
| GPOEO：预测＋局部搜索 | [入门](DVFS/gpoeo2022/ELI5_notes.md) | [精读](DVFS/gpoeo2022/paper_notes.md) | [图表](DVFS/gpoeo2022/figs_notes.md) | [摘要](DVFS/gpoeo2022/translation_notes.md) |
| DVFO：边云协同推理 | [入门](DVFS/dvfo2023/ELI5_notes.md) | [精读](DVFS/dvfo2023/paper_notes.md) | [图表](DVFS/dvfo2023/figs_notes.md) | [摘要](DVFS/dvfo2023/translation_notes.md) |
| E4：视频早退出＋DVFS | [入门](DVFS/e4-aaai2025/ELI5_notes.md) | [精读](DVFS/e4-aaai2025/paper_notes.md) | [图表](DVFS/e4-aaai2025/figs_notes.md) | [摘要](DVFS/e4-aaai2025/translation_notes.md) |
| SparseDVFS：稀疏感知分块 | [入门](DVFS/sparsedvfs2026/ELI5_notes.md) | [精读](DVFS/sparsedvfs2026/paper_notes.md) | [图表](DVFS/sparsedvfs2026/figs_notes.md) | [摘要](DVFS/sparsedvfs2026/translation_notes.md) |
| FUSE：手机LLM协同频率 | [入门](DVFS/fuse2025/ELI5_notes.md) | [精读](DVFS/fuse2025/paper_notes.md) | [图表](DVFS/fuse2025/figs_notes.md) | [摘要](DVFS/fuse2025/translation_notes.md) |
| GreenLLM：SLO双环服务 | [入门](DVFS/greenllm2025/ELI5_notes.md) | [精读](DVFS/greenllm2025/paper_notes.md) | [图表](DVFS/greenllm2025/figs_notes.md) | [摘要](DVFS/greenllm2025/translation_notes.md) |
| DVFSLM：token需求预测 | [入门](DVFS/dvfslm2026/ELI5_notes.md) | [精读](DVFS/dvfslm2026/paper_notes.md) | [图表](DVFS/dvfslm2026/figs_notes.md) | [摘要](DVFS/dvfslm2026/translation_notes.md) |
| LLM能量–性能刻画v4 | [入门](DVFS/llm-dvfs-characterization2026/ELI5_notes.md) | [精读](DVFS/llm-dvfs-characterization2026/paper_notes.md) | [图表](DVFS/llm-dvfs-characterization2026/figs_notes.md) | [摘要](DVFS/llm-dvfs-characterization2026/translation_notes.md) |

## 新增第二批：20篇具体对比

[20篇：具体算法、被控负载、执行程序、平台、结果](DVFS/comparison-20-papers.md) · [CSV](DVFS/data/dvfs-20.csv)

两批共20篇，加原有独立JSA2023共21篇全文笔记。

| 新增论文 | 从零入门 | 图文精读 | 图表索引 | 双语摘要 |
| --- | --- | --- | --- | --- |
| Ondemand原始设计 | [入门](DVFS/ondemand2006/ELI5_notes.md) | [精读](DVFS/ondemand2006/paper_notes.md) | [图表](DVFS/ondemand2006/figs_notes.md) | [摘要](DVFS/ondemand2006/translation_notes.md) |
| ULP MCU DVFS | [入门](DVFS/ulp-dvfs2024/ELI5_notes.md) | [精读](DVFS/ulp-dvfs2024/paper_notes.md) | [图表](DVFS/ulp-dvfs2024/figs_notes.md) | [摘要](DVFS/ulp-dvfs2024/translation_notes.md) |
| RP2040阶段DVFS | [入门](DVFS/embedded-apps2025/ELI5_notes.md) | [精读](DVFS/embedded-apps2025/paper_notes.md) | [图表](DVFS/embedded-apps2025/figs_notes.md) | [摘要](DVFS/embedded-apps2025/translation_notes.md) |
| ATP Per-core DVFS | [入门](DVFS/percore-dvfs2025/ELI5_notes.md) | [精读](DVFS/percore-dvfs2025/paper_notes.md) | [图表](DVFS/percore-dvfs2025/figs_notes.md) | [摘要](DVFS/percore-dvfs2025/translation_notes.md) |
| WLC＋MLR RTM | [入门](DVFS/lowcomplex-rtm2020/ELI5_notes.md) | [精读](DVFS/lowcomplex-rtm2020/paper_notes.md) | [图表](DVFS/lowcomplex-rtm2020/figs_notes.md) | [摘要](DVFS/lowcomplex-rtm2020/translation_notes.md) |
| GreenDVFS | [入门](DVFS/greendvfs2024/ELI5_notes.md) | [精读](DVFS/greendvfs2024/paper_notes.md) | [图表](DVFS/greendvfs2024/figs_notes.md) | [摘要](DVFS/greendvfs2024/translation_notes.md) |
| 多任务时序DDQN | [入门](DVFS/multitask-drl2024/ELI5_notes.md) | [精读](DVFS/multitask-drl2024/paper_notes.md) | [图表](DVFS/multitask-drl2024/figs_notes.md) | [摘要](DVFS/multitask-drl2024/translation_notes.md) |
| 2QoSM表格Q | [入门](DVFS/2qosm2022/ELI5_notes.md) | [精读](DVFS/2qosm2022/paper_notes.md) | [图表](DVFS/2qosm2022/figs_notes.md) | [摘要](DVFS/2qosm2022/translation_notes.md) |
| 数字分频＋DVFS | [入门](DVFS/divider-dvfs2023/ELI5_notes.md) | [精读](DVFS/divider-dvfs2023/paper_notes.md) | [图表](DVFS/divider-dvfs2023/figs_notes.md) | [摘要](DVFS/divider-dvfs2023/translation_notes.md) |
| Ωkypous | [入门](DVFS/serverless-coreuncore2024/ELI5_notes.md) | [精读](DVFS/serverless-coreuncore2024/paper_notes.md) | [图表](DVFS/serverless-coreuncore2024/figs_notes.md) | [摘要](DVFS/serverless-coreuncore2024/translation_notes.md) |

## 新增十篇：先读路线图

[十篇对比、推荐读序与CPU/E902设计建议](DVFS/reading-map-2026-11.md)

本批选取2001—2025年的互补工作，不是“最新发表十篇”。每篇有四份笔记，英文与中文摘要均标明读者改写。所有课题实验是待验证建议，没有伪称已复现。

| 论文 | 从零入门 | 图文精读 | 原图表索引 | 双语摘要 |
| --- | --- | --- | --- | --- |
| CPN-DVFS（2018） | [入门](DVFS/cpn-dvfs-sensors2018/ELI5_notes.md) | [精读](DVFS/cpn-dvfs-sensors2018/paper_notes.md) | [图表](DVFS/cpn-dvfs-sensors2018/figs_notes.md) | [摘要](DVFS/cpn-dvfs-sensors2018/translation_notes.md) |
| RT-DVS（2001） | [入门](DVFS/rtdvs-sosp2001/ELI5_notes.md) | [精读](DVFS/rtdvs-sosp2001/paper_notes.md) | [图表](DVFS/rtdvs-sosp2001/figs_notes.md) | [摘要](DVFS/rtdvs-sosp2001/translation_notes.md) |
| DRQN Governor（2022） | [入门](DVFS/drqn-tnse2022/ELI5_notes.md) | [精读](DVFS/drqn-tnse2022/paper_notes.md) | [图表](DVFS/drqn-tnse2022/figs_notes.md) | [摘要](DVFS/drqn-tnse2022/translation_notes.md) |
| Online Power / Double Q（2022） | [入门](DVFS/online-power-tpds2022/ELI5_notes.md) | [精读](DVFS/online-power-tpds2022/paper_notes.md) | [图表](DVFS/online-power-tpds2022/figs_notes.md) | [摘要](DVFS/online-power-tpds2022/translation_notes.md) |
| DVFS功率模型 / SAMOS（2022） | [入门](DVFS/dvfs-powermodel-samos2022/ELI5_notes.md) | [精读](DVFS/dvfs-powermodel-samos2022/paper_notes.md) | [图表](DVFS/dvfs-powermodel-samos2022/figs_notes.md) | [摘要](DVFS/dvfs-powermodel-samos2022/translation_notes.md) |
| Runmeter（2025） | [入门](DVFS/runmeter-jsa2025/ELI5_notes.md) | [精读](DVFS/runmeter-jsa2025/paper_notes.md) | [图表](DVFS/runmeter-jsa2025/figs_notes.md) | [摘要](DVFS/runmeter-jsa2025/translation_notes.md) |
| JOSS（2023） | [入门](DVFS/joss2023/ELI5_notes.md) | [精读](DVFS/joss2023/paper_notes.md) | [图表](DVFS/joss2023/figs_notes.md) | [摘要](DVFS/joss2023/translation_notes.md) |
| ControlPULP（2024） | [入门](DVFS/controlpulp2024/ELI5_notes.md) | [精读](DVFS/controlpulp2024/paper_notes.md) | [图表](DVFS/controlpulp2024/figs_notes.md) | [摘要](DVFS/controlpulp2024/translation_notes.md) |
| SCMI端到端时延（2024） | [入门](DVFS/scmi-interfaces2024/ELI5_notes.md) | [精读](DVFS/scmi-interfaces2024/paper_notes.md) | [图表](DVFS/scmi-interfaces2024/figs_notes.md) | [摘要](DVFS/scmi-interfaces2024/translation_notes.md) |
| ControlPULPlet（2025） | [入门](DVFS/controlpulplet2025/ELI5_notes.md) | [精读](DVFS/controlpulplet2025/paper_notes.md) | [图表](DVFS/controlpulplet2025/figs_notes.md) | [摘要](DVFS/controlpulplet2025/translation_notes.md) |

## 已有JSA2023：时序编码与强化学习CPU DVFS

[从零入门](DVFS/jsa2023-temporal-dvfs/ELI5_notes.md) · [图文技术精读](DVFS/jsa2023-temporal-dvfs/paper_notes.md) · [图表索引](DVFS/jsa2023-temporal-dvfs/figs_notes.md) · [双语摘要](DVFS/jsa2023-temporal-dvfs/translation_notes.md)

这篇不重复计入新增十篇。学习控制器、功耗估计器与硬件接口是不同模块；真实硬件、RTL、HIL与模型能量的证据也必须分开。

## 原文、材料与生成规范

每篇顶部提供论文页面、分析版本PDF与DOI；图下给原图号与PDF页码。代码／原始数据／勘误的未核实项逐篇说明。原PDF不在公开仓库再分发；图归原作者与出版方，中文分析与教学算例为本项目整理。

[日报与历史筛选站](https://zzxwhu.github.io/dvfs-paper-daily/)用于发现候选，摘要卡不代替完整精读。
