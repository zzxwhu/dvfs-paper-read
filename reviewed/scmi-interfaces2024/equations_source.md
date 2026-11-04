## 1. 通信延迟与控制延迟不是同一量（定义整理）

```latex
T_{\rm msg}=T_1+T_2+T_3,\qquad T_{\rm CD}=t_{\rm frequency\ effective}-t_{\rm phase\ change}
```

全部为秒；T1发送，T2包含平台与Linux等待，T3返回。CD还包括检测、排队、周期与动作应用；T_msg返回完成也不一定是工作负载开始变速的同一时刻。

§3.2、Table1及§4.2，PDF p8/10–12。

## 2. 控制改善的正确分母（读者算例）

```latex
\Delta T\%=100\,(T_{\rm base}-T_{\rm new})/T_{\rm base}
```

该式是耗时减少百分比；若用speedup=T_base/T_new−1，定义不同，小差异时才近似相等。论文Table2使用自身speedup口径，应保留表述。

Fig4、Table2与讨论；算例为读者补充。
