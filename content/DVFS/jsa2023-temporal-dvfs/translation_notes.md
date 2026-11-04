---
title: "中英文摘要与章节导读"
tags: ["DVFS", "CPU"]
date: "2026-11-04"
---

> 本页为双语改写概述与阅读导航，不是论文全文翻译。原文：[arXiv:2309.03779v1](https://arxiv.org/abs/2309.03779)。对原始摘要的准确措辞请直接查看 PDF 第 1 页。

## English abstract — reader-written paraphrase

This work develops CPU frequency control for periodic embedded applications with soft deadlines. Utilization-based Linux governors can miss energy-saving opportunities when voltage levels are coarse, CPU cores have uneven activity, or tasks include I/O waiting. The authors summarize execution history through temporal encoding and use Double DQN to choose frequency actions. Training is performed in user space, and quantized inference is deployed in the kernel. Experiments on a Jetson Nano use two custom applications and four MiBench workloads. The reported energy benefits depend on the workload, deadline, and comparison governor. The method is a practical soft-deadline controller; its results do not establish hard real-time guarantees or performance on another CPU.

## 中文对应摘要

本文为具有软截止时间的周期性嵌入式应用设计 CPU 频率控制。电压档位粗、多核忙闲不均和任务中的 I/O 等待，会使基于利用率的 Linux governor 错过节能机会。作者通过时序编码压缩执行历史，再由 Double DQN 选择频率动作。训练在用户态完成，量化推理部署在内核。Jetson Nano 实验覆盖两项自建应用和四项 MiBench 负载。节能收益取决于负载、截止时间以及比较的 governor。本文展示的是一个可实现的软截止时间控制器，实验不能证明硬实时保证或另一种 CPU 上的性能。

## 按问题阅读全文

| 想知道什么 | 原文重点位置 | 读的时候记下什么 |
| --- | --- | --- |
| 为什么需要新策略 | 第 1–3 节及动机实验 | 现有 governor 的具体失效情形，平台有多少电压档 |
| 控制器看什么、输出什么 | 方法章节与图 8、11、12 | 状态、动作、采样时序、截止时间、终端奖励 |
| 历史怎样变成固定输入 | 图 11–12 及编码描述 | 近期信息、累计信息、历史分配；别把时间比例当进度 |
| 智能算法怎样训练 | DDQN、奖励及训练流程 | 在线网络、目标网络、经验、每种截止时间的训练设置 |
| 怎么在真实系统里跑 | 实现章节与图 15 | 用户态训练、内核量化推理、CPUFreq 执行路径 |
| 比普通调频好多少 | 实验章节与图 22–25 | 基线、时限、能量归一化参照及超时分布 |
| 编码是否有必要 | RNN 对照与图 26–31 | 对照网络大小、输入长度、训练开销、收敛差异 |

页码随期刊排版可能改变。本笔记的图号与页码采用 21 页 arXiv v1，不能机械套到期刊 PDF。

## 术语对照

| 英文 | 中文及本论文含义 |
| --- | --- |
| Dynamic Voltage and Frequency Scaling (DVFS) | 动态电压频率调节，通过合法工作点调整 CPU 性能与能耗 |
| governor | 调频策略模块，不是 PLL 本身 |
| workload | CPU 运行的任务与输入，不是控制算法自身 |
| soft deadline | 软截止时间，少量或轻微违约可能被系统接受 |
| slack | 相对截止时间可利用的时间余量，含义需看具体实验定义 |
| temporal encoding | 时序编码，把执行历史压缩成有限规模状态 |
| Double DQN | 双重深度 Q 学习，将动作选择与目标值评估分离 |
| Q value | 某状态采取某动作的预计长期回报 |
| quantized inference | 量化推理；本文用整数路径适配内核约束 |
| energy / power | 能量 / 功率；总能量不能用单一瞬时功率替代 |
| model-free | 不依赖预先给出的精确任务模型，不是无数据或无约束 |

## 读完后应能回答

控制器是否真正改变硬件工作点？候选动作是什么？状态里哪些量来自观测，哪些是累计得到？奖励与真实能量是什么关系？最低能量结果是否伴随截止时间违约？比较对象是否有相同动作集合？如果迁移到单核 RISC-V，哪些输入会失效？

答案与证据分别整理在“论文解析”和“图表详解”；迁移建议与改进设想均需后续实验。
