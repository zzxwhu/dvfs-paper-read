## 1. 控制周期内的时限预算（由Table5整理）

```latex
T_{\rm step}=N_{\rm cycles}/f_{\rm ctrl},\qquad S=T_{\rm period}-T_{\rm step}
```

N_cycles为控制器执行周期数；f_ctrl是控制器时钟Hz，非被控CPU频率；S为剩余控制预算，秒。中断、额外通信若未包括，必须另加。

§5.4，Table5，PDF p23–24；SCMI等共同开销未计入Table5。

## 2. 被控功耗模型（原文Eq1符号整理）

```latex
P_i=\kappa(T_i)[I_{cc,i}V_{dd}+C_{{\rm eff},i}f_iV_{dd}^2]
```

P_i为W；V_dd为V；f_i为Hz；I_cc为漏电相关电流A；C_eff为有效开关电容F；κ是温度相关因子。参数由模型标定而来。

§4.2，PDF p16。
