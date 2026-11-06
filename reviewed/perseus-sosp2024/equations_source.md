## 1. 受时间约束的能量最小化

```latex
\min_F E(F)\quad\mathrm{s.t.}\ T(F)\leq D
```

F为所有计算的频率向量；E为GPU J/迭代，T与D为s。不是每个算子各自满足同一个D。

Eq5，p6

## 2. 关键割的边际成本（教学整理）

```latex
c_i=E_i(t_i-\tau)-E_i(t_i),\quad C^*=\arg\min_C\sum_{i\in C}c_i
```

τ与t为s，ci为加速τ增加的J；C是关键DAG合法s-t割。

§4.3/Fig6，p7
