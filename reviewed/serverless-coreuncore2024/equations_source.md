## 1. 比例余量反馈

```latex
S_k=\sum_{i\leq k}(t_i^{budget}-t_i^{actual}),\qquad u_k=K_p(S)S_{k-1}
```

时间均s，S正为剩余余量，Kp无量纲且分段自适应；不是包含积分/微分项的PID。

§5.1–5.2，p5–6

## 2. 可行频点优化

```latex
\min_{F_c,F_u}\widehat P(F_c,F_u)\quad\mathrm{s.t.}\quad\widehat L=\frac{W_c}{F_c}+\frac{W_u}{F_u}+\frac{W_d}{F_d}\leq t^{budget}
```

W为域工作周期，F为Hz，L为s，P为W；预测可行不等于实际必然满足。

Eq3/§5.2，p6–7
