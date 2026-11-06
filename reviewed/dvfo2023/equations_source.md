## 1. 状态与动作

```latex
s_t=(\lambda,\eta,p(a),B),\quad a_t=(f_C,f_G,f_M,\xi)
```

λ/η与ξ无量纲，p(a)为特征重要性分布，B为bit/s，频率单位必须统一MHz。

§5.1，p6

## 2. 任务代价与reward（整理）

```latex
C=\eta E+(1-\eta)P_{\max}T,\quad r_t=-C
```

E为边缘J/任务，T为端到端s，Pmax将时间转成能量尺度；云端J不在此E内。

§4.2 Eq4/§5.1 Eq14，p4/6
