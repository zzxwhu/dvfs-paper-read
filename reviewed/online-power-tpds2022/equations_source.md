## 1. Double Q更新（Algorithm1的整理）

```latex
a^*=\arg\max_a Q_A(s',a),\quad Q_A(s,a)\leftarrow Q_A(s,a)+\eta[r+\gamma Q_B(s',a^*)-Q_A(s,a)]
```

Q_A/Q_B为两张无量纲价值表；η是学习率，γ是折扣；s为离散IPC/MPO状态。随机选择更新哪张表，另一路对称处理。

Algorithm1、Fig4，PDF p5。

## 2. 选定奖励与真实能量的区别

```latex
r=(c\,{\rm IPC})^3/P,\qquad E=\int P(t)dt
```

P为功率W，c为论文给定缩放常数（c≥10）；IPC为指令/周期。r是训练评分，E才是J。该奖励并非严格的截止期约束。

§3.5，PDF p6。
