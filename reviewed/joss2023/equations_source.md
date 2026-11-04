## 1. 总能量选配置（对方法的紧凑整理）

```latex
\widehat E(c)=[\widehat P_C(c)+\widehat P_M(c)]\widehat T(c),\quad c=(TC,NC,f_C,f_M)
```

P_C/P_M为W，T为s，E为J；TC为核类型，NC为核数，频率Hz。依赖功率／时间模型准确、共享空闲功耗分摊合理。

§4–5，PDF p4–6；数字为读者算例。

## 2. 计算项缩放与预测准确率

```latex
T_C'=T(1-MB)f_C/f_C',\qquad A=1-|y-\widehat y|/y
```

MB无量纲，描述原始运行中等待占比；T_C′为新CPU频率下计算时间。A是本文用的相对误差反向分数，不是分类准确率。完整等待模型还包含内存频率，不能删掉。

Eq1、§7.3，PDF p4/9。
