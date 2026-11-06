## 1. 受deadline约束的能量搜索

```latex
\min_{f_G,f_M}\widehat{P}_i\widehat{T}_i\quad\mathrm{s.t.}\ \alpha_k\widehat{T}_i\leq\delta
```

P W、T s/token、δ s/token；预测最优只在固定CPU和已搜候选集合内成立。

Eq1/Algorithm1，p4/8

## 2. 窗口自适应校正

```latex
\alpha_k=\frac{\sum_{i\in W_k}t_i}{\sum_{i\in W_k}\widehat{t}_i},\quad QoS=\min(r_a/r_d,1)
```

α无量纲；ra/rd为实际/目标tokens/s；QoS不等按时token比例。

Eq14/§5，p8/10
