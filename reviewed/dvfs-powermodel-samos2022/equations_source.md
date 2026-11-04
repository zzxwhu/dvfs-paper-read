## 1. 固定频点的线性模型与组合（简化记号）

```latex
\widehat P_{d,f}=b_{d,f}+\sum_j w_{d,f,j}\frac{\Delta n_j}{\Delta t},\qquad \widehat P_{\rm sys}=\sum_d\widehat P_{d,f_d}
```

Δn为窗口事件次数，Δt为秒，事件率单位s⁻¹；b为W，w单位J/事件，依特征定义变化；CPU活跃度项在原文Eq4中另有表示。这里为阅读统一式，不代替完整实现。

§3.1，Eq1/4/5，PDF p5–7；数字为教学。

## 2. 非负最小二乘及误差

```latex
\min_{b,w\geq0}\|Xw+b\mathbf{1}-p\|_2^2,\qquad {\rm MAPE}=\frac{100}{N}\sum_k\frac{|\widehat p_k-p_k|}{p_k}
```

X是事件率矩阵，p是测得W；N为样本数。MAPE在p接近零时不稳定；能量误差需先积分再比较，不等于功率MAPE。

§3.3与§5，PDF p8/13–15。
