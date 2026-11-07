---
title: "IC方向DVFS：10篇精选与课题阅读路线"
date: "2026-11-07"
tags: [DVFS, IC, PLL, PMIC, co-design]
---

这份清单面向“数字DVFS控制器＋现有PLL/PMIC”的课题。选入10项不同工作：8篇ISSCC/JSSC，1篇MICRO，以及1篇工程复现价值较高的ControlPULP。ControlPULP复用原31篇中的论文，其余9篇是本专题新选入工作。这里完成的是文献筛选和阅读路线，不表示10篇已全部全文精读或独立复现。

## 先理解这条控制链

软件提供任务需求、截止时间或性能目标；硬件计数器和传感器提供实际运行状态；策略产生目标电压频率工作点；执行控制器协调时钟、电源及完成反馈；监测器检查是否超温、欠压、超时或违反性能要求。论文可能只研究其中一部分，必须确认它覆盖到了哪里。

你的核心工作可以是监控接口、选档策略、安全执行状态机与验证平台。下面涉及片上稳压器、延迟跟踪振荡器或统一闭环的工作，用于理解执行器约束；采用它们的思想时要核对已有IP能否暴露所需控制端口和反馈信号。

## 10篇清单

|编号|工作与渠道|课题关联|阅读优先级|
|---|---|---|---|
|1|EPOCHS-1，JSSC 2026|分布式数字功耗分配＋联合调压调频＋RISC-V SoC|优先：系统架构|
|2|可重构稳压器网络，ISSCC 2025|运行时调整电源域与供电资源的对应关系|其次：多域扩展|
|3|4nm Tri-Gear ARMv9.2 SoC，ISSCC 2024|软件性能请求、硬件DVFS、PMIC及SRAM电源协调|优先：实际控制链|
|4|POWER10电压频率增强，JSSC 2023|负载选频、欠压调节与快速保护|优先：算法与保护分工|
|5|194nW RISC-V IoT SoC，ISSCC 2022|事件优先级、可用能量与性能约束决定控制模式|优先：小型CPU场景|
|6|性能保证的超低功耗MCU供电控制，JSSC 2021|性能反馈决定电压，理解AVS与DVFS的关系|优先：反馈量选择|
|7|24核分布式LDO网络，JSSC 2020|电压反馈、IR压降补偿与电源转换时间|补充：电源动态|
|8|All-Digital Fused PLL-Buck，JSSC 2019|时钟与供电进入统一控制环的经典方案|补充：PLL/电源协同|
|9|ICED，MICRO 2024|编译映射、电源岛、动态吞吐约束协同|其次：co-design方法|
|10|ControlPULP，IJPP 2024|开源控制器、控制固件与FPGA硬件在环|优先：实现与验证|

## 1. EPOCHS-1：数字功率预算如何落到调压调频

**原题：** EPOCHS-1: A 12 nm Highly Heterogeneous Open-Source SoC With Distributed Coin-Based Power Management and Integrated Hybrid Voltage Regulation。

**发表：** JSSC，61卷5期，2276–2294，2026；DOI含2025，对应先行发表时间，正式卷期年份为2026。

[DOI与原文入口](https://doi.org/10.1109/JSSC.2025.3602386) · [作者机构公开PDF](https://bioee.ee.columbia.edu/wp-content/uploads/2025/10/EPOCHS-1_A_12_nm_Highly_Heterogeneous_Open-Source_SoC_With_Distributed_Coin-Based_Power_Management_and_Integrated_Hybrid_Voltage_Regulation.pdf)

**为什么选：** 它把数字功率预算的分配与电压频率执行放到同一颗异构SoC中研究。阅读时要沿着“功率预算如何表示→各域怎样取得预算→预算怎样映射到目标性能→电源和时钟怎样响应”逐层追踪。这些问题与你设计控制器的边界直接相关。

**需要核对的方法：** coin如何产生、转移和回收；控制节点输入什么局部状态；如何避免预算超发；统一调压调频中电压和时钟分别由谁闭环调节。不能把coin直接理解为电压档位。

**实验边界：** 摘要报告联合方法相对集中式功耗管理基线最高1.57倍加速；必须在全文定位相应负载、预算与比较配置，不能写成通用57%节能。全文已找到，详细方法和图表仍需逐页核对。

**关联版本：** ISSCC2024的12nm RISC-V异构SoC，以及VLSI2024的400ns混合DVFS架构属于这条研究线的关联材料，本清单不另计数量。后者的400ns来自专门集成的供电结构，不能直接当作板外PMIC接口的等待时间。

## 2. 可重构电源网络：控制输出还能包括电源域连接

**原题：** A Dynamically Reconfigurable Digital-Integrated Voltage-Regulator Fabric for Energy-Efficient DVFS in Multi-Domain SoCs。

**发表：** ISSCC 2025，论文8.3。[DOI](https://doi.org/10.1109/ISSCC49661.2025.10904508) · [出版社摘要](https://ieeexplore.ieee.org/document/10904508)

**为什么选：** 多个电源域共享上游Buck时，组内最高电压需求会约束公共电源轨。该工作研究运行中改变域分组与供电拓扑，说明控制动作不一定只有改一个电压编码。

**方法问题：** 什么状态触发重分组；怎样检查稳压器电流上限；切换连接前后如何保持供电；重配置代价怎样影响净节能。以上是全文阅读问题，目前核对到出版社摘要和官方议程，尚未取得完整论文。

**对课题的取舍：** 适合未来多电源域扩展；单CPU、单PMIC电源轨的初版控制器优先实现可靠的OPP切换。不能把稳压器网络架构等同于一个I²C软件接口。

## 3. MediaTek移动SoC：软件请求与硬件执行的分工

**原题：** A 4nm 3.4GHz Tri-Gear Fully Out-of-Order ARMv9.2 CPU Subsystem-Based 5G Mobile SoC。

**发表：** ISSCC 2024，论文2.1。[DOI](https://doi.org/10.1109/ISSCC49657.2024.10454494) · [会议官方议程](https://www.isscc.org/s/ISSCC2024AdvanceProgram-Final.pdf)

**为什么选：** 是CPU应用场景中硬件DVFS、电源控制及存储器供电配合的实例。后续重点核对软件性能目标、频率环、高带宽电压控制器和PMIC之间的完整路径。

**容易误解的地方：** 论文涉及FLL，不能擅自改称PLL。运行频率满足CPU逻辑要求，也必须同时满足SRAM电源要求；不同电源轨之间的约束会影响执行器状态机。

**材料状态：** 题名、DOI和会议信息已核对；已发现公开流传的全文线索，正式或作者可获取全文及方法细节仍待确认。当前不据此写精确节能结论。

## 4. POWER10：慢速优化与快速保护配合

**原题：** Deterministic Frequency and Voltage Enhancements on the POWER10 Processor。

**发表：** JSSC 2023，58卷1期，102–110。[DOI](https://doi.org/10.1109/JSSC.2022.3225378) · [IBM作者机构介绍](https://research.ibm.com/publications/deterministic-frequency-and-voltage-enhancements-on-the-power10-processor)

**为什么选：** 工作负载优化选频算法与数字电压跌落传感器、核心节流及欠压控制共同工作。它有助于理解：优化器负责争取性能或节能，快速保护路径负责应对供电瞬态，两者时间尺度可以不同。

**方法问题：** 选频算法用哪些运行状态；电压环如何抵消负载线和噪声影响；保护触发后频率如何恢复。作者机构摘要报告最高15%频率提升和10%核心电压降低，不能相乘推算论文没有报告的总节能率。

**材料状态：** 元数据和机构摘要核实，全文尚待取得。ISSCC2022会议版作为关联版本，不另计一篇。

## 5. 194nW IoT SoC：事件如何触发DVFS

**原题：** A 194nW Energy-Performance-Aware IoT SoC Employing a 5.2nW 92.6% Peak Efficiency Power Management Unit for System Performance Scaling, Fast DVFS and Energy Minimization。

**发表：** ISSCC 2022，论文13.8。[DOI](https://doi.org/10.1109/ISSCC42614.2022.9731758) · [政府机构公开全文](https://www.osti.gov/servlets/purl/1860366)

**为什么选：** 采用32位RISC-V MCU，讨论事件驱动快速DVFS、能量感知和最低能耗点跟踪，比高端GPU更适合帮助理解小型CPU控制场景。

**已定位的控制输入：** MCU监测I/O接口并编码事件优先级；输入电压监测反映可用能量；最低能耗点跟踪提供另一组参考设置。模式控制器结合这些条件决定控制方式，后接Buck和时钟电路。

**方法问题：** 三种模式优先关系是什么；事件到来和能源不足冲突时怎样处理；电压和时钟怎样跟随；最低能耗点搜索开销多大。论文报告的194nW与5.2nW分别有系统和PMU的条件，不能当作你的CPU目标功耗。

**材料状态：** 已找到全文及控制架构段落，图表和全部实验尚未完成逐项精读。

## 6. 性能保证的MCU供电控制：输入也可以是性能反馈

**原题：** A Supply Voltage Control Method for Performance Guaranteed Ultra-Low-Power Microcontroller。

**发表：** JSSC 2021，56卷2期，601–611。[DOI](https://doi.org/10.1109/JSSC.2020.3023001) · [作者Arm技术说明](https://developer.arm.com/community/arm-research/b/articles/posts/m0n0-the-devil-is-in-the-details)

**为什么选：** 讨论在保证性能的前提下控制供电，适合回答“为什么某一频率必须配某个电压”“怎么知道电压已经够用”。它提供性能跟踪和自适应电压控制的参考，不能仅凭题名当作工作负载学习型DVFS算法。

**方法问题：** 反馈监测器和实际CPU关键路径有什么对应关系；如何校准工艺温度误差；性能目标如何转换成电源控制量；稳定性和安全裕量怎样保证。

**对课题的取舍：** 若现有平台没有延迟或性能监测电路，第一版可采用预先表征的安全OPP表。复现该文闭环则需要相应监测器及可调供电。当前核对元数据和作者说明，期刊全文尚待取得。

## 7. 分布式LDO：写入目标电压之后发生什么

**原题：** Distributed Network of LDO Microregulators Providing Submicrosecond DVFS and IR Drop Compensation for a 24-Core Microprocessor in 14-nm SOI CMOS。

**发表：** JSSC 2020，55卷3期，731–743。[DOI](https://doi.org/10.1109/JSSC.2019.2956413) · [IBM作者机构摘要](https://research.ibm.com/publications/distributed-network-of-ldo-microregulators-providing-submicrosecond-dvfs-and-ir-drop-compensation-for-a-24-core-microprocessor-in-14-nm-soi-cmos)

**为什么选：** 可编程参考电压、分布式电压采样和局部稳压器构成执行闭环。它说明目标电压、供电网络各处的实际电压和CPU安全电压不能简单等同。

**已核实的机制：** 全局控制器比较电源网格电压与参考，发送2位上调/下调码；局部微稳压器响应并补偿压降。转换速度与局部电路有关。

**对课题的取舍：** 主要学习电压到位判据、转换延迟与瞬态约束。它是片上电源电路参考，不要求你重做LDO。当前全文待取得，不能把其亚微秒行为套用到板外PMIC。

## 8. PLL-Buck统一控制：理解更紧密的协同

**原题：** An All-Digital Fused PLL-Buck Architecture for 82% Average Vdd-Margin Reduction in a 0.6-to-1.0-V Cortex-M0 Processor。

**发表：** JSSC 2019，54卷11期，3215–3225。[DOI](https://doi.org/10.1109/JSSC.2019.2936968) · [作者公开会议版](https://psylab.ece.gatech.edu/files/2023/12/unicap_buck_isscc.pdf)

**为什么保留较早论文：** PLL与Buck的联合闭环直接对应你的两个执行模块，适合作为结构原理参考。它超出了常规“软件选OPP、分别下发命令”的协同程度。

**方法问题：** 电压如何进入频率控制环；负载突变时怎样保持时序裕量；周期数怎样补偿；什么时候调电压，什么时候调整时钟。题名中的82%是电压裕量降低，不能写成CPU能量降低82%。

**移植约束：** 该结构需要修改或耦合环路，通常无法仅靠已有PLL/PMIC黑盒接口完整复现。作者公开入口是会议版，期刊全文待取得，两个版本必须分别标明。

## 9. ICED：co-design具体协同了什么

**原题：** ICED: An Integrated CGRA Framework Enabling DVFS-Aware Acceleration。

**发表：** MICRO 2024，1338–1352。[DOI](https://doi.org/10.1109/MICRO61859.2024.00099) · [作者公开PDF](https://www.comp.nus.edu.sg/~tulika/MICRO24.pdf) · [作者复现材料](https://zenodo.org/records/13858430)

**为什么选：** 硬件提供可独立调压调频的电源岛，编译和映射工具决定任务如何占用这些资源；运行时瓶颈变化进一步影响频率需求。这是明确的软硬件协同设计例子。

**方法问题：** 编译期知道哪些计算依赖；运行时测量什么吞吐量；如何识别不限制总吞吐的内核；电源岛粒度如何影响调度自由度和硬件开销。

**实验边界：** 不能根据论文中出现LDO/PLL框图就断言已制造相应芯片；需全文核对仿真、综合、功耗模型和代码范围。作者artifact提供复现入口，尚未运行。它属于体系结构顶会，渠道名称如实标注。

## 10. ControlPULP：最适合拿来研究控制器实现的一篇

**原题：** ControlPULP: A RISC-V On-Chip Parallel Power Controller for Many-Core HPC Processors with FPGA-Based Hardware-In-The-Loop Power and Thermal Emulation。

**发表：** International Journal of Parallel Programming 2024，52卷，93–123。[DOI](https://doi.org/10.1007/s10766-024-00761-4) · [机构论文入口](https://www.research-collection.ethz.ch/entities/publication/3a7b0b8c-0381-441e-b1b4-4a3502ffdd8a) · [硬件](https://github.com/pulp-platform/control-pulp) · [控制固件](https://github.com/pulp-platform/control_pulp_pcf)

**为什么选：** 有可编程控制器、实时控制固件和FPGA闭环验证框架，对“数字控制器＋现有执行器”有工程参考价值。它复用原论文库中的工作，不属于IC顶刊顶会，选择理由是实现开放。

**方法问题：** 采样、控制计算和执行如何调度；控制固件与硬件加速器怎样分工；中断和DMA怎样影响控制周期；如何用处理器功耗温度模型构成被控对象。

**验证边界：** FPGA上真实运行的是控制器；目标多核处理器的功耗温度响应采用模型进行硬件在环评估。不能把该结果称作目标72核芯片真实电源轨的DVFS测量。

## 给当前课题的阅读顺序和统一摘录表

先看 **5→10→3**，弄清事件触发、控制固件和硬件执行；再看 **4→6→1**，学习策略、反馈和多域管理；最后看 **8→7→2→9**，理解联合环路、执行器动态和更复杂的co-design。

每篇全文笔记统一回答：

1. 输入：软件任务要求、性能计数器、电压、温度或电流分别由谁提供，单位和采样周期是什么？
2. 决策：阈值、查表、控制器、优化或学习算法具体怎样计算目标？触发条件在哪里？
3. 输出：目标频率、电压编码、分频值、功率预算还是电源域连接？
4. 执行：谁写寄存器，谁等待电源稳定、时钟锁定，失败时如何处理？
5. 协同：哪些步骤在软件、固件或RTL中，为什么这样划分？
6. 验证：算法模型、RTL仿真、FPGA硬件在环、芯片测量分别验证了哪些主张？
7. 实验：程序、输入数据、基线、时延约束、控制和切换开销、净能量收益是否齐全？
8. 迁移：现有E902、PLL、PMIC需要增加哪些监测/握手端口；哪些结果依赖专用电路而不能直接复用？

这10篇形成选文集合；逐图逐表、公式推导和复现步骤需在全文精读中继续补齐，不以本筛选页代替完整笔记。
