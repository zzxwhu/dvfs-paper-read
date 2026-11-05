---
title: "20篇DVFS论文具体对比：算法、负载、程序、平台与结果"
date: "2026-11-05"
tags: [DVFS, CPU, E902]
---

这里比较上一批10篇与本轮新增10篇，**恰好20篇**。另有早先JSA2023时序编码笔记，保留在站内但不混入20篇计数。整理时间2026-11-05；论文覆盖基础与近期工程工作，不宣称“最新20篇”或系统综述。

[下载完整CSV对比表](data/dvfs-20.csv) · [结构化JSON](data/dvfs-20.json) · [上一批路线图](reading-map-2026-11.md)

**先分清四个角色：** 控制算法是“怎样决定动作”；负载是“CPU要处理哪类工作”；具体程序是“真正执行哪个软件”；平台决定“动作能否真实生效、能量怎样得到”。软件程序运行在物理CPU上，可通过驱动改变CPU频率；模型闭环则只能证明模型条件下的效果。以下所有复现建议尚未执行。

**结果不能直接按百分比排冠军。** 核心/芯片/整板能量、平均功率、IPS/W、预测误差、控制延迟和面积是不同量；每行保留对应分母。未找到具体程序名称就明说，绝不从benchmark套件中猜补。移动端/服务器的节能率不预测E902收益。

手机可横向滑动表格；单击论文名称进入含原图表、公式、输入输出和实验审查的笔记。

## 第1批：10篇逐项比较

| 论文/原文 | 具体控制算法 | 被控负载类型 | 具体被控程序 | 平台/证据 | 结果与适用范围 |
| --- | --- | --- | --- | --- | --- |
| [RT-DVS，2001](rtdvs-sosp2001/paper_notes.md) · [原文](https://doi.org/10.1145/378239.378245) | 静态EDF/RM＋cycle-conserving余量回收＋look-ahead EDF；输入周期/WCET与完成事件，输出合法OPP | 单CPU周期实时计算任务 | 5个周期性任务使用90%WCET；随机周期/WCET任务集仿真。mpg123/内核编译为平台性能校验，不能误写为全部主任务源码 | HP N3350/AMD K6-2+ PowerNow!，Linux2.2.16；真实整机电测＋独立任务集仿真 | 原型约20%–40%整机功率/能量改善，特定5任务；变压约0.4ms、仅变频41µs；见Fig16/§4。 |
| [CPN-DVFS，2018](cpn-dvfs-sensors2018/paper_notes.md) · [原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6163884/) | CPN竞争层最近原型＋输出频率映射；离线训练，在线特征推理；共享频域取各核建议最大值 | 单核/多核CPU计算与访存混合 | MiBench/ParMiBench；gzip_b、gzip、gunzip等，含同构与混合并发压缩 | Creator PXA270/Linux2.6.25＋MAXIM1586B/DAQ；Jetson Tegra K1四A15 | 对Performance，单核CPN70能量降低4.88%–42.63%，CPN90为0.54%–20.93%；70/90允许不同性能损失，非同QoS统一排名。 |
| [DRQN Governor，2022](drqn-tnse2022/paper_notes.md) · [原文](https://doi.org/10.1109/TNSE.2021.3123280) | GRU状态8＋Q网络8–16–15；频率/利用率历史→15档动作；100ms采样，用户态训练/内核推理 | 软实时混合计算/I/O应用 | 相机/ResNet50/存储；MP3→WAV＋蓝牙；FFT＋4KB文件写入 | Intel i5-7200U/Linux5.4.45，400–2500MHz/Turbo关闭；RAPL核心能量 | 对Ondemand三类核心能量分别约13%–33%、22%–30%、7%–28%，依期限；推理4–10ms，非2023版本25µs。 |
| [Double-Q OPM，2022](online-power-tpds2022/paper_notes.md) · [原文](https://doi.org/10.1109/TPDS.2021.3092270) | 两张Q表；IPC/MPO离散状态→RAPL功率帽＋uncore频率；3s窗口，reward=(c·IPC)^3/W | 多核MPI/HPC与学习程序 | NAS8项训练；未见11项：AMG、CoMD、miniFE、miniQMC、HPCCG、Nekbone、miniAMR、LULESH、Sweep3D、LeNet5、Keras-CNN | CascadeLake4×40核共160；Haswell16×12核共192；Ubuntu16.04/Linux4.15/RAPL/msr-safe | 11项未见程序平均芯片能量降低约12%、平均慢化<3%；基线TDP功率帽＋Ondemand＋默认uncore；不保证每程序<3%。 |
| [SAMOS功耗模型，2022](dvfs-powermodel-samos2022/paper_notes.md) · [原文](https://arxiv.org/abs/2305.06782) | 按频点选择兼容PMC＋NNLS非负线性回归；输出功率估计，未实现新的闭环选频策略 | CPU/GPU功率建模工作负载 | Rodinia3.1的17个OpenMP＋5个CPU合成压力内核、10个CUDA程序；当前记录未逐一列齐17个名称，不从套件目录猜补 | Jetson AGX Xavier，INA3221，100ms采样；离线标定模型 | 全组合能量误差2.5%；GPU>600MHz子集平均1.3%，不是节能率；没有可直接横比的governor收益。 |
| [Runmeter，2025](runmeter-jsa2025/paper_notes.md) · [原文](https://doi.org/10.1016/j.sysarc.2025.103504) | 分频点PMC/NNLS功率模型＋内核定点移动窗口；输出估计功率/能量，非完整DVFS governor | Linux任务/核心在线功率监控 | Rodinia/OpenMP/CUDA及合成内核；任务切出/tick采样；具体套件配置需配套代码核对 | Jetson AGX Xavier/Linux4.9.253，INA3221；10Hz监控；64位定点29小数位 | 在线窗口能量APE均值约9%、P90约20.8%；最坏监控时间开销0.7%。离线1.3%不可冒充在线误差或节能率。 |
| [JOSS，2023](joss2023/paper_notes.md) · [原文](https://arxiv.org/abs/2306.04615) | 两频点标定memory-boundness＋回归时间/功率模型＋四角/最陡下降搜索；联合核类型/核数/CPU/内存频率 | 异构多核task-DAG与多种粒度 | Heat Diffusion、Dot Product、Fibonacci、Darknet VGG16、Biomarker Infection、Alya、Sparse LU、Matrix Multiplication、Matrix Copy、Stencil | Jetson TX2，2Denver＋4A57/Linux4.9.253；INA3221 CPU＋内存轨，5ms采样 | 相对GRWS CPU＋内存能量降低40.7%；STEER同基线19.5%，差21.2个百分点；相对速度目标非绝对硬期限。 |
| [ControlPULP，2024](controlpulp2024/paper_notes.md) · [原文](https://arxiv.org/abs/2306.09501) | 可编程功率分配/封顶＋PID温控＋频率/电压协调；PFCT500µs/PVCT125µs；多核并行固件 | HPC CPU被控功耗/热模型 | 72核案例的合成负载轨迹；ZCU102 PS上的C/pthread plant模型；非72核实体运行应用电测 | CV32E40P管理核＋8核集群/DMA；ZCU102 FPGA，FreeRTOS，硬件在环 | 主控制步67330→13641周期（4.9倍固件加速），不是应用/节能4.9倍。9核HIL案例与72核计算案例需分开；分析arXiv v2。 |
| [SCMI接口优化，2024](scmi-interfaces2024/paper_notes.md) · [原文](https://www.mdpi.com/1996-1073/17/22/5778) | Linux CPUFreq/SCMI→邮箱/中断/FreeRTOS PCF；事件触发＋安全降频快速通路；不是新学习算法 | HIL模型中的计算/访存阶段切换 | 500个20ms合成计算/访存阶段、SCMI请求序列；不对应已公开命名的CPU应用基准 | ZCU102：A53/Linux高层＋FPGA ControlPULP低层，模型CPU/能量；时间尺度映射 | T1发送70.5µs；优化降频114µs、升频约1.42ms，整体CD均值0.77ms；模型应用加速2.89%，不是通用实测节能率。 |
| [ControlPULPlet，2025](controlpulplet2025/paper_notes.md) · [原文](https://arxiv.org/abs/2410.15985) | 案例用MPC（horizon2、5次迭代）＋快速中断/周期DMA/D2D；控制核输出DVFS动作 | 9/36PE功率/热控制模型；另有硅片通信实验 | MPC固件、500个8B PVT寄存器事务与链路测试；不是已命名压缩/CV/LLM应用基准 | 500MHz RTL控制案例；TSMC65nm Kairos硅片290MHz/30mW、双QFN64 PCB；两证据分开 | CRD128通信附加总时长<0.05%，因MPC计算占>99%；非通信本身耗时0.05%或节能率。宽链路51.2Gbit/s非窄PCB实测。 |

## 第2批：10篇逐项比较

| 论文/原文 | 具体控制算法 | 被控负载类型 | 具体被控程序 | 平台/证据 | 结果与适用范围 |
| --- | --- | --- | --- | --- | --- |
| [Ondemand原始设计，2006](ondemand2006/paper_notes.md) · [原文](https://www.kernel.org/doc/ols/2006/) | 内核定时采样忙闲比：原版超过上阈值升MAX，低于下阈值逐步降；后续直接选可保持约80%忙碌的最低频率，共享域取最高核需求 | 多处理器SSL Web服务，客户连接数由负载机递增 | 标准SSL Web server/client测试；当前材料未明确到可唯一复建的服务软件版本，不擅自补成Apache/Nginx | 4-socket Xeon MP，双核/HT共16逻辑CPU，8GB；Linux2.6时期cpufreq；12V CPU供电支路电流，CR5410S霍尔传感器＋PMD-1208LS USB采集 | Performance与Powersave功率差：约10%（16逻辑CPU服务器SSL负载；CPU12V支路，不是任意整机能量节省；§6.3，PDF p10–12）；动态策略性能：相对静态低频退化更小（原文描述dynamic性能损失barely visible；不从曲线虚构统一精确节能率；Fig4–5，p12）；测量变化：约1W run-to-run（作者因此展示原始曲线未额外平均；不是置信区间；§6.2，p10） |
| [ULP MCU DVFS，2024](ulp-dvfs2024/paper_notes.md) · [原文](https://doi.org/10.3390/electronics13050826) | 离线频点扫描＋两端点指数V–f拟合；Algorithm5按事件/任务类别选择高性能、最低功耗或能量效率模式；没有训练神经网络 | 单核MCU计算内核；不同计算量与软/严格时限类别 | 32点/128点FFT、CRC32、MD5、SHA256（Algorithm1–4） | STM32L0 ARM Cortex-M0+，STM32CubeIDE；Keysight34465A电流测量、GW INSTEK PSB-1400L供电；引用数据表为STM32L010K8，正文未把具体开发板型号写齐 | 同频点DVFS相对3.3V DFS能量：降低27.74%–47.74%（Table4各频率比较；不是相对最优DFS点统一降低47.74%；Table4，PDF p13）；最低计算能量点：2.097MHz，约1.94V（本文8档/5程序与拟合曲线内；不是任意MCU最优点；Table3/6，p13–14）；FFT128示例：2285.48µJ（2.097MHz下Table3；相同程序单位需统一；Table3，p13） |
| [RP2040阶段DVFS，2025](embedded-apps2025/paper_notes.md) · [原文](https://doi.org/10.3390/technologies13020082) | 离线阶段能量/时延表＋固定周期预算：固定时长采集/通信走Slow，计算选能满足剩余期限的最低电压可行档，余时睡眠；确定性规则，无训练模型 | 周期性IoT声音采集→数字信号处理→无线发送→睡眠 | 4000点FFT、4000点自相关、50-tap FIR；4kHz采集4000样点；经ESP-01发送19字节标志/时间等 | RP2040双Cortex-M0+（264KB SRAM）＋PDM MEMS麦克风＋ESP-01；裸机；Nordic PPK2 100ksps，3.3V板级供电，GPIO四位标记阶段；ATmega328p补充泄漏实验 | 20s周期完整能量：2.947J/周期（Medium Optimized；High4.409J，Medium3.594J，High Optimized3.104J；Table10–11，p15）；30s周期完整能量：2.884J/周期（Low Optimized；High4.503J，Medium3.676J，Low3.145J；Table12–13，p16）；作者概括收益：最高约33%/36%（分别20s/30s、相对未优化高档；不是相对每一种基线均省36%；§4.1，p15–16） |
| [ATP Per-core DVFS，2025](percore-dvfs2025/paper_notes.md) · [原文](https://doi.org/10.37936/ecti-cit.2025192.258820) | 阈值T=45%+U_avg·(85%−45%)；逐核利用率超过T则升最高频，否则降一档；100ms轮询，非神经网络 | 虚拟机中并行通信负载，2/3/4核参与与不同不平衡程度 | Charm++ Stream-All-to-All，TRAM（Topological Routing and Aggregation of Messages）；Type1/2/3三种并行配置 | 物理Xeon E5630四核2.53GHz，CentOS7/KVM；4vCPU虚拟机；psutil/perf-kvm，APC UPS/apcupsd读取能耗；实际供电域独立性未由请求接口自动证明 | Type1能量/指令：ATP79.06，Ondemand84.29，Performance75.74 J/Ginstr（ATP好于Ondemand，但差于Performance；Fig9/§6.2，p8–9）；Type2能量/指令：ATP57.88，Ondemand61.64，Performance57.48 J/Ginstr（同一负载内比较，不能说ATP全面第一；§6.2，p9）；Type3能量/指令：ATP44.81，Performance44.92 J/Ginstr（很小差距无置信区间，不自动显著；§6.2，p9） |
| [WLC＋MLR RTM，2020](lowcomplex-rtm2020/paper_notes.md) · [原文](https://doi.org/10.3390/jlpea10030025) | WLC四类阈值分类＋查表任务映射/cluster DVFS；可选MLR在缩小空间中建模IPC并最大化IPS/W；每500ms重新分类 | CPU密集、访存密集、混合与低活动并发多线程程序 | mthreads整数/64MB随机内存混合合成负载；PARSEC bodytrack、ferret、fluidanimate、canneal、freqmine、streamcluster，单个及多程序组合 | ODROID-XU3 Exynos5422，4×A15＋4×A7、Ubuntu14.04与片上电流传感器；Intel Sandybridge Core i7，Ubuntu/Likwid/RAPL并用分流电阻初步交叉验证 | XU3 WLC-only：IPS/W改善约24%–127%（相对Ondemand，特定单/多程序场景；Fig10/Table10，p19）；XU3 WLC＋MLR：Fluidanimate139%；两不同类128.42%（是IPS/W相对改善，不是能量减少139%；Table10，p19）；Intel平台WLC＋MLR：IPS/W约20%–40%改善（同平台Ondemand，所有核分配给应用；Fig12，p20） |
| [GreenDVFS，2024](greendvfs2024/paper_notes.md) · [原文](https://doi.org/10.1109/CCGrid59990.2024.00039) | 离线加权效用最大化选“负载等级—频率”对；LSTM早期序列分类；在线概率加权频率f=Σp_i f_i；不是强化学习 | 虚拟机中的数据库/缓存/搜索服务，请求强度变化 | CloudSuite Data Serving（YCSB+Cassandra）、Redis benchmark、CloudSuite Web Search（Nutch） | HPE ProLiant DL380 Gen11，2×Xeon Gold6448Y，256GB DDR5；Ubuntu23.04/Linux6.2，KVM/QEMU/libvirt；perf/turbostat等监测package功率并积分能量 | 已知负载能量改善：WS4.6%、Redis6.5%、Data Serving18.3%（相对论文intel governor；package能量；不同应用分别报告；TableV，p10）；已知负载性能改善：0.9%、1.3%、1.3%（与上行同三应用和基线，不是所有负载无退化证明；TableV，p10）；分类准确率：94.1%、97.7%、90.0%（分别DS/Redis/WS，不是节能率；TableIV，p7） |
| [多任务时序DDQN，2024](multitask-drl2024/paper_notes.md) · [原文](https://doi.org/10.48550/arXiv.2409.19434) | 用户态DDQN＋内核TEGM（GRU+MLP，PRO/PROL）或TEM（MLP，PROM）；对每个候选频率评估Q并取最大；终回合稀疏reward | 多核共享频率上的周期软实时任务集，串行/并行与多个期限 | 3任务：重复乘法；5/8任务：MiBench jpeg、qsort、fft、typeset混合；另随机生成3/4/5/8任务集 | NVIDIA Jetson Nano2GB，Linux4.9；Ruideng UM25C USB功率计；内核浮点网络，用户态训练；不是E902实现 | 固定任务集相对Ondemand：约7%/3%/4%降低（分别3任务PRO、5任务PRO、8任务PROL；图15称功率，正文又称energy，应保留术语不一致；Fig15/§III-E，p9–10）；随机任务集功率：2.177→1.8449W（3任务，15.25%）（不是所有任务均有15.25%；4/5/8任务7.25/8.12/7.26%；TableVI，p11）；推理开销：最大0.16ms（8任务PROL；非旧2023的整数引擎25µs；TableIV，p10） |
| [2QoSM表格Q，2022](2qosm2022/paper_notes.md) · [原文](https://doi.org/10.3390/jlpea12020029) | C/GSL实现表格Q-learning，状态离散化，0.9概率选最大Q/0.1探索；10ms线程更新；七种reward对照，HAL映射至CPU性能状态 | 导航/路径规划CPU软件，计算量、访存与重规划需求变化；本文CPU控制不是电机控制算法 | Anytime Dynamic A*（ADA*）路径规划、地图与轨迹规划线程；低层PID/里程计由另一Arduino承担，不是用户课题要实现的内容 | ODROID-XU4 Exynos5422，4×A15/4×A7、2GB，Ubuntu18.04/Linux4.14.5-92；cluster级DVFS；ArduinoROMEO/ATmega328P独立处理低层动作 | power-only策略：平均功率降低42.6% vs Ondemand（2.98W；相对situation-aware降低10.2%，但误差更大；Fig8/§5.4，p15）；power＋error策略：功率−38.7%、误差−4.6% vs Ondemand（同一reward可同时转述这两项；不是42.6%与6.1%同时获得；§5.4，p15）；error-only策略：误差改善6.1% vs Ondemand（属于另一策略；不能合并最高功率收益；§5.4，p15） |
| [数字分频＋DVFS，2023](divider-dvfs2023/paper_notes.md) · [原文](https://doi.org/10.3390/electronics12020407) | 改进CRIT访存关键路径计数＋512–4096周期密集采样；25µs移动平均/稳定判定；快DFS分频与≥100µs慢DVFS双层规则 | 乱序CPU上短突发与持续访存密集阶段 | SPEC CPU2017 traces，例605.mcf、619.lbm、xalancbmk等；非实际板卡上直接运行SPEC测试 | ChampSim修改L2 MSHR与频率时序、McPAT功耗模型；2.5GHz乱序CPU模型，8个DVFS×8个分频配置（64有效频级）；另用Design Compiler估面积 | 模型平均能量降低：16.26%（Table4）（相对无DVFS；摘要写16.36%，版本内不一致；Table4，p12）；模型平均性能损失：2.04%（CRIT1.88%；容限10%是阈值设计设置，非所有应用实证硬上界；Table4/Fig8，p12–13）；ED²P能效改善：13.57%（CRIT6.79%；不是额外节能13.57%；Table4，p12） |
| [Ωkypous，2024](serverless-coreuncore2024/paper_notes.md) · [原文](https://doi.org/10.48550/arXiv.2407.18386) | 关键路径/比例预算＋自适应比例反馈u=Kp(S)S＋PMC灰盒延迟模型＋二次功率回归；Pareto可行集选最低功率Core/Uncore组合；共享域冲突协调 | 具有顺序/分叉/汇合的serverless函数工作流，SLO与调用率变化 | SeBS九种函数构成160条工作流；正文点名video-processing、graph-bfs、dynamic-html；Azure调用轨迹驱动（并非直接在Azure上实测） | 两台Intel Xeon E5-2658A服务器，4个10vCPU/16GB VM，各VM分socket；OpenWhisk/Kubernetes/MinIO；acpi-cpufreq与MSR0x620；RAPL20ms采样 | 相对Performance/Ondemand功率：约降低44%/25%（160条工作流，代价为非零违约；不等于CPU压缩能量收益；Fig11–12/§6.2.1，p9–10）；相对EcoFaaS功率：约降低16.4%（Ωkypous违约1.8%，EcoFaaS1.3%；不是相同违约率下比较；§6.2.2，p10）；相对DVFaaS功率：约降低22%（DVFaaS违约2.8%，各控制器服务质量并非完全相同；Fig12，p10） |

## 按算法选择，哪些值得你先做

| 类别 | 对应论文 | 需要的输入/资源 | 对E902的实际含义 |
| --- | --- | --- | --- |
| 阈值、规则与查表 | Ondemand、ATP、ULP、RP2040 | 忙闲计时或任务阶段、合法频档、离线E–T表 | 先做基线，容易核对动作；不要跳过真实程序与计时接口 |
| 可调度性与余量回收 | RT-DVS、Ωkypous的余量反馈 | 最坏执行需求或可用预测、期限、完成事件 | 分清已证明上界与经验预测，后者不能叫硬实时保证 |
| 分类/回归/原型 | CPN、WLC＋MLR、GreenDVFS、JOSS | 需求特征、离线数据与模型；一些方法依赖PMC/异构核 | 优先小树/原型/回归，先证明增加状态能分辨压缩复杂度 |
| 表格强化学习 | Double-Q OPM、2QoSM | 离散状态/动作、训练环境、reward与探索保护 | 适合小动作空间；把服务器uncore/机器人误差替换成真实可观测量 |
| 深度时序强化学习 | DRQN、多任务DDQN | 历史状态、训练、网络存储与推理预算 | 不混用GRU维度、推理耗时；先做无历史/小表对照，再决定是否值得 |
| 功耗反馈支撑 | SAMOS、Runmeter | 计数器、功耗真值标定、模型校准 | 输出估计功率，不是下一频率；不可用同模型自证最终节能 |
| 硬件/固件路径 | 数字分频、ControlPULP、SCMI、ControlPULPlet | 安全时钟接口、握手、中断、总线/PMIC | 快DFS与慢调压分开，测请求到生效全路径；硅片/RTL/HIL证据分层 |

## 给当前课题的可实行组合（建议，未定题/未上板）

**被控程序：** 首选验证LZ4或heatshrink日志分块压缩是否适合你的RAM与工具链；CRC32/SHA256可作最小功能核。压缩仍是候选，不假定CV或LLM已定，不涉及电机。

**第一层基线：** 借ULP/RP2040的阶段E–T表，加入Ondemand式忙闲阈值和RT-DVS式余量保护。采集/接收、压缩、发送、空闲分开计能量，确认最低频率不一定最省能。

**智能增量：** 借CPN/GreenDVFS的“估需求→选档”，用块长度、已处理字节、历史cycles/byte、队列和剩余时间做小树/原型表；需要多步决策时再比较小Q/Double-Q。只有简单模型确实失败且推理预算允许时，才上时序网络。

**软硬执行：** 先以E902为被控CPU跑真实程序并实现合法DFS，或明确以E902为控制核、另一个对象为plant；角色不能含混。连接PMIC和安全OPP后才称真实DVFS。模型能量、RTL估计与外部实测单独标注。

**统一实验：** 所有策略同输入、同合法频档、同任务期限、同电测边界；保存每块正确性、J/块、P95/最大延迟、违约率、控制/采样/切换开销及失败输入。没有理由提前承诺节能20%或零违约。

## 本轮重点纠正的数字误读

- 多任务DDQN使用GRU状态6，TNSE2022前序为8；本篇0.16ms、前序4–10ms与旧2023量化版本耗时属于不同系统。
- 多任务随机集有超过5%超时组，不能把低功率结果与“全任务满足deadline”捆绑。
- WLC＋MLR的139%是IPS/W提升，绝不是节能139%。
- ATP在Type1的79.06 J/Ginstr仍高于Performance75.74，优点要连同温度和基线描述。
- 2QoSM最佳功率/误差来自不同reward，42.6%是平均功率降低，不是两项最高收益同时成立。
- 数字分频论文摘要16.36%与Table4的16.26%矛盾；本表采用可核对Table4并披露冲突。
- Ωkypous的约16%功率降低主要相对EcoFaaS，服务质量存在差异；不是任意CPU任务节能率。

[额外已有JSA2023笔记](jsa2023-temporal-dvfs/paper_notes.md)可与两篇时序强化学习工作连读，但不计入本页20篇。
