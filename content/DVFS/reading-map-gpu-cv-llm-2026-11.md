---
title: "第三批10篇：从CPU DVFS走向GPU、CV和LLM应用"
date: "2026-11-06"
tags: [DVFS, CPU, GPU, CV, LLM, E902]
---

这次允许GPU、CV和LLM作为被控应用，但还没有替你确定最终课题。建议先读[30篇具体比较](comparison-30-papers.md)，再按下面顺序挑论文。每篇都有入门、技术精读、图表索引、双语摘要四份报告；原图、公式、实验边界在技术精读中就地展示。

## 先把“谁控制谁”说清

以小语言模型生成文字为例：**被控程序**是llama.cpp及其中运行的SLM；**执行硬件**是CPU/GPU/内存；**控制器**可只是查表，也可是回归/搜索或DQN；**执行器**是驱动/sysfs/NVML暴露的合法档位。LLM是应用不意味着要用LLM做控制。软件控制真实硬件上运行的程序，也是实际闭环；只有在plant或能量输出来自模型时，才标成模型/仿真证据。

典型数据流：输入图像或prompt → 程序开始执行 → 观测阶段、context、队列和延时 → 控制算法选档 → 驱动调频 → 程序在该档继续执行 → 测量正确性、质量、时延和能量并反馈。

## 推荐阅读顺序

| 次序 | 论文与入门 | 你应掌握的具体知识 | 实验边界 |
| --- | --- | --- | --- |
| 1 | [FUSE入门](fuse2025/ELI5_notes.md) / [精读](fuse2025/paper_notes.md) | 为什么GPU推理也需要CPU；为什么独立governor可能互相拖慢；阶段查表如何实施 | rooted Pixel手机，单请求无排队，整设备Monsoon |
| 2 | [DVFSLM入门](dvfslm2026/ELI5_notes.md) / [精读](dvfslm2026/paper_notes.md) | 预测下一任务需求→约束搜索→窗口校正；XGBoost与最终选频的关系 | Jetson，CPU阈值固定；标定约一天；QoS是吞吐比 |
| 3 | [GPOEO入门](gpoeo2022/ELI5_notes.md) / [精读](gpoeo2022/paper_notes.md) | GPU计数器、周期检测、回归树和局部搜索怎样协作 | RTX3080Ti；训练迭代；探索会造成额外slowdown |
| 4 | [GreenLLM入门](greenllm2025/ELI5_notes.md) / [精读](greenllm2025/paper_notes.md) | prefill与decode为什么需要不同控制器；SLO、排队、滞回、粗细环 | 8×A100节点；GPU能量；部分TBT通过率下降不能漏 |
| 5 | [E4入门](e4-aaai2025/ELI5_notes.md) / [精读](e4-aaai2025/paper_notes.md) | 神经gate决定少做几层，坐标搜索决定每层怎么运行；质量/能量联合比较 | 视频动作识别；早退改变计算量；W轴不等J |
| 6 | [DVFO入门](dvfo2023/ELI5_notes.md) / [精读](dvfo2023/paper_notes.md) | DQN状态/动作/reward，边云卸载和频率协同 | 边缘能量不含云端；动作/比例文字有核对缺口 |
| 7 | [SparseDVFS入门](sparsedvfs2026/ELI5_notes.md) / [精读](sparsedvfs2026/paper_notes.md) | 控制粒度与切换摊销；为什么不能对每个极短算子调一次 | 新预印本；78.17%大数字需原始轨迹复核 |
| 8 | [Zeus入门](zeus-nsdi2023/ELI5_notes.md) / [精读](zeus-nsdi2023/paper_notes.md) | 训练到目标质量的总能量、batch老虎机和功率帽剖析 | 主评估多为真实轨迹回放；不是单次纯锁频 |
| 9 | [Perseus入门](perseus-sosp2024/ELI5_notes.md) / [精读](perseus-sosp2024/paper_notes.md) | 关键路径、DAG、最小割与近似Pareto前沿 | 小规模实体测试与大规模emulation分开 |
| 10 | [LLM刻画v4入门](llm-dvfs-characterization2026/ELI5_notes.md) / [精读](llm-dvfs-characterization2026/paper_notes.md) | 如何设计频率扫描；分类/生成区别；实测与机会估算区别 | 单Blackwell GPU；联合路由87%为推算，不是部署 |

若只想先做CPU毕设，先精读前3篇的“输入输出—公式—最小复建—课题实验”。它们提供了容易缩小的控制框架，不要求E902运行大模型。若转GPU/CV，读E4与SparseDVFS时先保持网络和精度不变，只验证调频，再把早退或稀疏当独立实验变量。

## 三个容易落地的算法层次

1. **查表与保护层。** 各阶段E–T表，输入任务阶段/期限，输出最低能量可行档；非法/不可达状态退安全档。先验证实际频率生效与正确输出。
2. **学习预测层。** 用新输入可知的信息预测下一块/帧/token的执行时间与能量，在小档位集合搜索。训练数据与留出测试分开，用已完成任务校正预测偏差。
3. **动态策略层。** 只有队列/干扰/长期收益使前两层明显不足，才加小Q表、DQN或双时间尺度反馈。控制器推理时间也属于任务预算。

建议实验最低记录：输入哈希、模型/程序版本、质量、合法档位和实际频率、温度、预热、独立运行、开始/结束/命令/生效时间、积分能量、P95/最大时延、违约定义、控制净开销。只用功耗模型时明确写“估计J”，不能用同一模型训练和评分就声称物理节能成立。

## 阅读状态

本批完成全文方法/结果阅读、关键页视觉核对及读者原创分析，没有运行作者代码，没有做GPU/CPU/E902独立复现；每篇复建和课题实验都是待执行建议。完整PDF只本地保留，公开内容为带来源的关键图表裁图和中文解读。
