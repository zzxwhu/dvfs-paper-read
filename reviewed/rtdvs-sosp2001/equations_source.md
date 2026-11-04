## 1. EDF 的选频条件（原文 §2.3 的符号重排）

```latex
\sum_i C_i/P_i\ \leq\ a,\qquad a=f/f_{\max},\quad C_i(a)=C_i/a
```

C_i：最大频率下的最坏执行时间，秒；P_i：周期／相对期限，秒；a：无量纲，0<a≤1；f：Hz。前提是执行时间近似与频率成反比，且独立周期任务满足 EDF 模型。

§2.2–2.3，PDF p3–4；例子是读者补充。

## 2. 整周期能量（读者补充，用于纠正只比较活动功率）

```latex
E_{\rm period}=E_{\rm run}+E_{\rm switch}+P_{\rm idle}(P-T_{\rm run})
```

E：J；P_idle：W；P 和 T_run：s。这里 P 代表任务周期，不是功率。必须把切换停顿和空闲状态的能量归属统一。

由 §3–4 的能量边界整理，不是论文编号公式。
