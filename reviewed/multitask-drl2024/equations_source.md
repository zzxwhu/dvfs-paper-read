## 1. 候选频率逐个评分

```latex
a_t=\arg\max_{f\in\mathcal{F}}Q_\theta(s_t,f)
```

s为时序编码状态，Q为无量纲预期回报，f为候选动作；推理每档一次。

§II-B，p5–6

## 2. 低频reward项

```latex
r_f=\sum_{f\in\mathcal{F}}x_f\left(1-\frac{f^3-f_{min}^3}{f_{max}^3-f_{min}^3}\right)
```

x_f为驻留时间/T，和为1；不是实测功率，V-f关系和静态功率未显式包含。

Algorithm3，p6
