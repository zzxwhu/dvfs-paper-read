## 1. G1：能量预算下最低时延

```latex
\min_{f_C,f_G}T(f_C,f_G)\quad\mathrm{s.t.}\ E(f_C,f_G)\leq E_b
```

T为TTFT(s)或TPOT(s/token)，E为对应阶段J或J/token；两种目标不可混。

§6/Fig11，p10–11

## 2. G2：时延约束下最低能量

```latex
\min_{f_C,f_G}E(f_C,f_G)\quad\mathrm{s.t.}\ T(f_C,f_G)\leq D
```

D是阶段时延目标；memory默认，此式不是完整三维穷举。

§6.1，p10–11
