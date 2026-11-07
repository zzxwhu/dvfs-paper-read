---
title: "01 从一次 CRC32 读懂电压、频率与能量"
date: "2026-11-07"
tags: [DVFS, E902]
---

[返回五篇实验手册](guide.md) · [论文原文](https://doi.org/10.3390/electronics13050826) · [所用版本PDF](https://mdpi-res.com/d_attachment/electronics/electronics-13-00826/article_deploy/electronics-13-00826.pdf)

**Dynamic Voltage and Frequency Scaling as a Method for Reducing Energy Consumption in Ultra-Low-Power Embedded Systems**  
Josip Zidar, Tomislav Matić, Ivan Aleksi, Željko Hocenski。MDPI正式版18页，DOI 10.3390/electronics13050826。

> 方法详解第二版。阅读顺序为“任务→测量→建表→选档→执行→验证”。文中的“原文”指本文所用 PDF；“教学推导”和“建议实验”是为了帮助复建而补充的分析，不是作者已经做过的实验。

## 1. 这篇究竟控制什么

设想一块单片机收到26字节数据，需要计算 CRC32。**被控负载**就是这段计算，**控制量**是运行它的处理器工作频率以及相应供电电压。CRC32代码和正确答案不因为选档而改变，改变的是执行速度、供电电流和完成这次计算所消耗的能量。

本文使用 STM32L0、Cortex-M0+，测试 FFT32、FFT128、CRC32、MD5、SHA256。FFT输入随机生成，后三种算法输入是26字母字符串。这里的“算法”主要指被运行的计算程序；选档策略本身是任务分类与模式选择，没有训练神经网络。这是理解你课题的第一步：**被控程序、预测模型、选档规则是三个独立组件**。原文依据为§3.1–3.2，PDF第5–8页。

| 组件 | 这篇论文中的实际含义 | 对应你的工程 |
| --- | --- | --- |
| 任务输入 | FFT采样序列或26字节字符串 | CPU能执行的块处理程序，具体应用待定 |
| 策略输入 | 任务触发事件和任务类别 | 任务ID、输入大小、期限类别 |
| 策略内部数据 | 不同工作档的时间、能量与性能效率 | 离线标定表 |
| 策略输出 | 高性能、省电、能量效率三种模式 | 合法档位编号 |
| 执行器 | MCU时钟配置；电压配档方案 | CPUFreq驱动，或PLL/电源控制接口 |
| 验证反馈 | 电流、电压、执行时间、输出正确性 | 日志与测量设备 |

原文展示了测量、配档模型和程序框架。它没有给出你可以直接复制的“在线误差学习器＋PMIC完整闭环”。读到Algorithm 5时应把它当作任务模式调度框架，而不是已经解决所有硬件切换细节的产品。

## 2. 为什么最低频率不一定最省电

先区分三个物理量。电流 $I$ 的单位是A，功率 $P=VI$ 的单位是W，能量 $E$ 的单位是J。功率是每秒消耗多少能量，任务能量则累计整个运行过程。

$$
E_{\mathrm{task}}=\int_{t_s}^{t_e}V(t)I(t)\,dt
\approx \bar V\bar I T.
$$

$t_s,t_e$是任务起止时刻，$T=t_e-t_s$。最后一个近似适用于稳定工作点及恰当的平均测量；若电压、电流同时明显变化，应使用功率采样积分，不能随意把两个平均值相乘。

**教学推导。** 用简化模型 $P=P_0+kV^2f$、$T=C/f$ 理解趋势，可得

$$
E=\frac{P_0C}{f}+kV^2C.
$$

$P_0$代表这段时间持续存在的背景功率，$C$为任务需要的等效周期数，$k$为与活动程度有关的系数。固定电压时，降频会拉长背景耗电时间；降低电压又能减少动态能量。两者竞争可能形成中间最优点。此式用于解释，原表中执行时间并不严格按 $1/f$ 缩放，原文还讨论了8MHz时钟配置造成的异常，不能用这条理想式替代测量。

这也回答“程序怎样被DVFS改变速度”。程序运行在实际处理器上，处理器每秒执行的时钟周期数改变，程序完成时间就可能变化。访存等待、外设等待和操作系统调度不一定随CPU频率等比例变化，需要按实际程序测量。

## 3. 离线阶段：把一次任务变成一行标定数据

![Fig3 电流测量连接](images/ulp-dvfs2024-fig3.png)

[放大原图表](images/ulp-dvfs2024-fig3.png) · [原文 Fig3，PDF 第 6 页](https://mdpi-res.com/d_attachment/electronics/electronics-13-00826/article_deploy/electronics-13-00826.pdf#page=6)。图表来自该论文作者。

读Fig.3时沿电源路径看，先确定仪器测的是哪条供电支路，再找处理器与测量设备的连接。这张图解释测量边界，没有展示一个训练好的选频网络。原平台采用Keysight 34465A电表与GW INSTEK PSB-1400L可编程电源，开发环境是STM32CubeIDE。仪器最高读取速率不等于本次实验实际使用的采样速率，应在复现记录中分开填写。

原文Table 1先固定3.3V，扫描八个频率，报告100次测量的平均电流和执行时间。你复建时，每条原始记录至少应保留如下字段，而不能只留最终平均值。

```text
run_id, task_name, input_hash, input_bytes,
requested_frequency, observed_frequency, voltage,
start_time, finish_time, current_or_power_samples,
output_checksum, clock_source, compiler_flags, temperature
```

一次测量的顺序是：校验输入→进入目标档并等待稳定→发出任务开始标记→执行计算→发出结束标记→验证输出→对同一窗口积分。调试器暂停、串口打印、数据装载是否计入窗口必须固定；否则测到的是不同问题。

**一个可按原表重算的例子。** Table 1的CRC32在2097kHz下，固定电压3.3V，平均电流0.51297mA，时间2.93ms。因此

$$
E\approx3.3\times0.51297\times2.93=4.960\ \mu\mathrm{J}.
$$

单位换算是 $\mathrm V\times\mathrm{mA}\times\mathrm{ms}=\mu\mathrm J$。这与Table 2的4.96µJ一致。此计算验证了单位与表格口径，没有独立验证仪器准确性。

## 4. 电压曲线怎样得到，又不能证明什么

原文Eq.(2)采用两个端点 $f_1=0.131$MHz、$V_1=1.8$V和 $f_2=16$MHz、$V_2=3.3$V，拟合

$$
V(f)=A\exp(f/B),\qquad
B=\frac{f_2-f_1}{\ln(V_2/V_1)},\quad
A=V_1\exp(-f_1/B).
$$

得到 $A=1.791011$V、$B=26.1804846$MHz。注意指数必须无量纲，所以这里的 $f$ 输入MHz；把2097kHz直接当成2097代入会完全算错。2.097MHz代入得到约1.94V。该推导解释作者模型的来源，不需要把“Excel回归”当成不可理解的步骤。

**两点拟合只确定一条曲线，不会自动确定芯片的安全工作边界。** 换成E902或FPGA，必须重新获得器件允许的电压范围、时序裕量和供电轨限制。STM32的这条曲线不能变成你的PMIC目标电压公式。Table 3给出的是本文配档条件下计算的能量，原文尚不足以复建一个包含全部转换损耗、失锁和电压稳定过程的动态电源系统。

![Table3 DVFS计算能量表](images/ulp-dvfs2024-table3.png)

[放大原图表](images/ulp-dvfs2024-table3.png) · [原文 Table3，PDF 第 13 页](https://mdpi-res.com/d_attachment/electronics/electronics-13-00826/article_deploy/electronics-13-00826.pdf#page=13)。图表来自该论文作者。

按Table 3读CRC32列：131kHz为9.17µJ，2097kHz为2.83µJ，16MHz为4.61µJ。能量最低在中间档。复核同一行，$1.94\times0.49866\times2.93\approx2.835$µJ，与表中2.83的差别来自表项取整。保持精度时应使用未舍入原始数据。

## 5. 在线阶段：怎样把表变成一次真实决策

原文Algorithm 5的逻辑可用下面的语义等价伪代码理解。它按不同条件依次检查三类负载，**不是并发任务调度器**。

```python
set_mode(POWER_SAVING)
while True:
    if critical_task_arrives():
        set_mode(HIGH_PERFORMANCE)
        execute_critical_task()
        set_mode(POWER_SAVING)
    if light_task_arrives():
        execute_light_task()  # 当前保持省电模式
    if energy_task_arrives():
        set_mode(ENERGY_EFFICIENT)
        execute_energy_task()
        set_mode(POWER_SAVING)
```

严格时间要求选高性能，有柔性期限的任务选能量效率模式，轻负载留在省电模式。原文没有在每次任务开始前训练或重新拟合模型，也没有展示对每个实时任务在线求一个连续电压值。**学习发生在哪里？这篇并没有学习阶段，价值在于建立可被智能算法替代的测量与决策基线。**

**面向你课题的扩展。** 如果任务有明确期限 $D$，把模式选择细化为有限档约束搜索。

$$
a^*=\arg\min_{a\in\mathcal F}\bigl(\widehat E_a+E_{\mathrm{switch},a}\bigr),
\quad
\mathcal F=\{a:\widehat T_a+T_{\mathrm{ctrl}}+T_{\mathrm{switch},a}\le D_{\mathrm{remain}}\}.
$$

$a$是档位编号；帽号表示预测或表中估计；$T_{\mathrm{ctrl}}$是策略计算时间；转换时间取决于当前档与目标档；$D_{\mathrm{remain}}$是此刻剩余预算。注意把整任务原始期限当作剩余预算，会忽略排队和已执行时间。这条搜索是本文标定思路的扩展，不冒充作者原算法。

以原表CRC32时间与能量作静态输入，再加**教学假设**控制加切换共0.20ms、暂不加入转换能量，能得到一条可手算的决策轨迹。

| 档位MHz | 时间ms（Table 1） | 能量µJ（Table 3） | 加开销后的ms | 剩余期限3ms是否可行 |
| --- | ---: | ---: | ---: | --- |
| 1.048 | 6.04 | 2.95 | 6.24 | 否 |
| 2.097 | 2.93 | 2.83 | 3.13 | 否 |
| 4.194 | 1.44 | 2.95 | 1.64 | 是 |
| 8.000 | 0.75 | 3.72 | 0.95 | 是 |
| 16.000 | 0.37 | 4.61 | 0.57 | 是 |

所以3ms期限选4.194MHz，而非能量最小的2.097MHz；4ms期限可选2.097MHz；0.5ms期限没有可行档。无解时返回“期限不可达＋最快安全档”，不能输出一个伪装满足期限的档位。这样你的控制算法才有清晰、可检查的输入输出。

## 6. 档位怎样交给PLL和PMIC

对软件模型，`apply(a)`意味着用标定的时间和能量推进目标系统的时间轴；不能在普通Python里`time.sleep()`后声称已经给CPU降压。对真实MCU或E902，`apply(a)`必须进入受控的硬件转换流程。一般升性能需要先保证足够的供电电压再升频，降性能先降频再降压；实际顺序、稳定条件、超时处理以器件资料为准。

建议接口返回 `accepted`、`applied`、`error` 三种状态，以及实际档位与生效时间。`accepted`只表示收到了请求。算法预算应把等待`applied`的时间算进去。FPGA上的PLL/IP可以生成合法时钟，但并不等于板上电压可任意改变，固定电压的验证应标成DFS。

## 7. 实验结果的两个百分比为什么不同

![Table4 同频DFS对DVFS节能率](images/ulp-dvfs2024-table4.png)

[放大原图表](images/ulp-dvfs2024-table4.png) · [原文 Table4，PDF 第 13 页](https://mdpi-res.com/d_attachment/electronics/electronics-13-00826/article_deploy/electronics-13-00826.pdf#page=13)。图表来自该论文作者。

Table 4沿频率逐行比较“同一任务、同一频率、不同电压方案”。2097kHz行的42.84%是DVFS对固定3.3V的DFS。另一方面 $1-2.83/4.61\approx38.61\%$ 比较的是DVFS中间档对最高档。基线变了，问题也变了。用已舍入的4.96和2.83重算第一种比较约为42.94%，不要为了匹配42.84%改造原始表值。

原文§3.4把不同算法在15种工作点下的能量做统计比较。这能说明算法耗能分布有区别，却不能直接证明某个在线DVFS控制器在新任务流上的收益显著。100次重复和15个工作点也不是同一种样本单位。你的论文应保留独立运行数据，在同一任务输入上配对比较策略，报告置信区间与失败次数。

## 8. 分三层复建，怎样判断做到哪一步

| 层级 | 实际工作 | 通过标准 | 不能声称 |
| --- | --- | --- | --- |
| 表级核算 | 重算E、V(f)、两种节能率和带期限选档 | 单位正确，无解有标记，结果与原表精度相容 | 已测得真实节能 |
| 软件闭环 | 不同块长与任务类型，使用逐档标定环境 | 动作改变后续时间，留出输入上统计能量和超时 | 模型焦耳等于E902实测焦耳 |
| 板级验证 | 同工作程序、实际频率与供电测量 | 输出正确、时钟生效、积分窗一致、转换代价计入 | 不同芯片必有同一最佳频率 |

建议首先只实现CRC32，验证输出与原始表口径，再加入一个长任务。每种输入以随机顺序重复不同档位，控制温度漂移，固定编译选项和程序版本。比较最高固定档、最低固定档、表中最省能档、带期限搜索四种策略。扫描期限从宽松到不可达，画“能量—超时率”曲线。若没有独立可调电源，先完成DFS并明确记录这一边界。

**值得改进的部分。** P0是把任务种类和数据大小纳入表，避免只标定26字节后外推所有输入。P1是增加小回归模型预测新输入的时间/能量，并和查表公平比较。P1还应比较是否计入转换成本，因为微秒级短任务可能没有足够收益覆盖切换。成功标准不是单个百分比，而是在相同期限、相同正确输出下净能量下降且超时风险可接受。

## 9. 读完应能回答的三个问题

为什么2.097MHz在静态表里最省能，却可能不是3ms期限下的选择？为什么给程序换频率能改变运行时间，却不应该改变CRC答案？为什么用STM32两点拟合的电压曲线不能直接驱动你的FPGA供电轨？能用上面的数据和接口回答，就掌握了后面四篇所依赖的DVFS基本闭环。


## 双语摘要改写与原文入口

**中文改写**　本文研究单核MCU计算内核；不同计算量与软/严格时限类别的运行时能效。具体程序包括32点/128点FFT、CRC32、MD5、SHA256（Algorithm1–4）。作者在STM32L0 ARM Cortex-M0+，STM32CubeIDE；Keysight34465A电流测量、GW INSTEK PSB-1400L供电；引用数据表为STM32L010K8，正文未把具体开发板型号写齐上采用离线频点扫描＋两端点指数V–f拟合；Algorithm5按事件/任务类别选择高性能、最低功耗或能量效率模式；没有训练神经网络。输入为应用事件、预先分类的时限需求、测得的I/T和频率表，输出为工作模式/频率，以及指数拟合所得供电目标；完整在线DC–DC切换闭环未展示。主要结果应与下方基线、性能约束和测量范围一起阅读，不能只摘最高百分比。贡献是低成本MCU操作级能量表、经验V–f曲线和按任务要求选模式的工程组织。它适合你建立基线；不是新的强化学习算法。

**English paraphrase**　This study characterizes FFT and hashing operations on an ultra-low-power Cortex-M0+ MCU. It compares fixed-voltage frequency scaling with voltage-frequency settings obtained from an exponential fit, and sketches task-specific operating modes. Its value is a measurement-oriented baseline rather than a learned online governor. This is a reader-written paraphrase, not the original abstract.

**代码与复现边界**　当前材料中尚未定位齐完整控制器源码、实验脚本和原始重复数据；这不表示这些材料不存在。

[完整编号图表索引](../ulp-dvfs2024/figs_notes.md) · [原四报告中的技术笔记](../ulp-dvfs2024/paper_notes.md) · [原表核算脚本](https://github.com/zzxwhu/dvfs-paper-read/blob/main/examples/focus-five/check_examples.py) · [方法逐步演示脚本](https://github.com/zzxwhu/dvfs-paper-read/blob/main/examples/focus-five/method_walkthrough.py)
