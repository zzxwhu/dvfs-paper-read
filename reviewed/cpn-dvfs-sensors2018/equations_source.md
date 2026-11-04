## 1. 最近原型推理（对§3步骤的数学整理）

```latex
j^*=\arg\min_j\|\widetilde{x}-w_j\|_2,\qquad \widehat f=\pi_{j^*}
```

x̃为归一化特征，无量纲；w_j是第j个原型；π_j是关联频率输出，Hz或归一化值；j*是节点编号。各维必须按同一训练尺度归一化。

§3，Fig2–3，PDF p5–7。

## 2. 原文性能分数与EDP

```latex
S(f)=1-\frac{T_f-T_{\max}}{T_{\max}},\qquad {\rm EDP}=E\,T_f
```

T_max指最大频率下的执行时间而非最长执行时间，s；T_f为当前频率时间，s；S无量纲；EDP为J·s。S不是T_max/T_f。

Eq6，PDF p8；EDP讨论§6，p15。
