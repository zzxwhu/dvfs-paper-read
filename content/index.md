# DVFS论文精读：面向CPU／E902课题

从零理解CPU频率、能量与闭环，再结合原图、公式与实验边界选择自己的实现路线。

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
