## 1. 控制时限余量（原文§III-B）

```latex
T_{\rm ctrl}=T_{\rm comp}+T_{\rm comm},\qquad T_{\rm slack}=T_{\rm long}-T_{\rm ctrl}>0
```

T_comp含MPC计算；T_comm含消息、采样与动作传输；T_long=3ms。所有单位s，短周期任务抢占等应在完整预算中体现。

§III-B，PDF p8。

## 2. 峰值链路与实际吞吐（原文整理）

```latex
\Theta=2\alpha f\theta,\qquad 0\leq\alpha\leq1
```

Θ单位bit/s；α为利用率；f是时钟Hz；θ为单向每周期有效位数，2表示双向。理论带宽、RTL利用率与板测物理链路应分开。

§III-A，Fig9，PDF p7。
