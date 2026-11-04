## 1. 历史编码与动作（原文§III的符号澄清）

```latex
h_t=G(h_{t-1},s_t),\qquad a_t=\arg\max_a Q(h_t,a),\quad f_t=T[a_t]
```

s_t为当前二维观测；h_t为8维历史状态；a是离散动作编号，无量纲；T为频率表，Hz。原文推理式的max应按选择动作的含义理解为argmax。

§III-A/B，Fig2，PDF p4。

## 2. 即时奖励与TD目标（本篇版本）

```latex
r_t=1-f_t/f_{\max}\ \ (t\leq D),\quad r_t=-5\ \ (t>D),\qquad y_t=r_t+\gamma\max_{a'}Q(h_{t+1},a')
```

r和Q是无量纲学习分数；D是应用期限，秒；γ=0.9。终止样本只取y=r。频率比奖励是能量偏好的代理，不是实测J。

Algorithms1–3与§IV-A，PDF p5–7。
