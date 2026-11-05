## 1. 表格Q更新

```latex
Q(s,a)\leftarrow(1-\alpha)Q(s,a)+\alpha[r+\gamma\max_{a\prime}Q(s\prime,a\prime)]
```

α学习率、γ折扣均无量纲；状态/动作必须离散；不是神经网络反向传播。

Eq4，p7

## 2. 归一化功率/误差奖励

```latex
r=2-\left(P/P_{max}+e/e_{max}\right)
```

P为W，e为任务误差；归一化后无量纲。压缩项目不使用物理路径误差。

Table4，p13
