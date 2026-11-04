## 1. 移动窗口与固定频点功率（§4整理）

```latex
S_j(t)=\sum_{k\in W(t)}\Delta n_{j,k},\qquad \widehat P(t)=L_f+\frac{1}{T'}\sum_j w_{f,j}S_j(t)
```

W(t)为最近采样组成的窗口；S为事件总数；T′为窗口秒数；L_f为常数功率W；w单位J/事件。固定频点公式要随实际状态切换；图示仅为单核简化。

§4.1–4.2，Eq4，PDF p7。

## 2. 固定点权重与整体能量误差

```latex
w_q=\operatorname{round}(2^{29}w),\qquad \epsilon_E=\frac{|\sum_k\widehat P_k\Delta t_k-\sum_kP_k\Delta t_k|}{\sum_kP_k\Delta t_k}
```

w_q为整数编码；解码为w_q/2^29。ε_E无量纲；分窗口APE与整段能量误差的汇总顺序不同。

§5.3–5.4，PDF p9–10。
