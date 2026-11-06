## 1. 相对能量预测

```latex
\widehat{e}(x,f)=\sum_{k=1}^{K}h_k(x,f)
```

x为参考档特征，f为候选档；输出e是E/Edefault无量纲，不是J；hk为回归树。

§4.3，p6–7

## 2. 目标与性能约束（整理）

```latex
\min_f E(f)T(f)^2\quad\mathrm{or}\quad\min_f E(f),\ T(f)\leq(1+\epsilon)T_0
```

ε为允许slowdown比例；E J、T s；ED²P单位J·s²。

§3.1/§5.4，p3/9
