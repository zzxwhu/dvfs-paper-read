## 1. SLO窗口能量

```latex
E(f)=P(f)\frac{f_{\mathrm{ref}}}{f}T_{\mathrm{ref}}+P_{\mathrm{idle}}\left(D-\frac{f_{\mathrm{ref}}}{f}T_{\mathrm{ref}}\right)
```

频率同单位，Tref/D为s，功率W，E为J；只在busy≤D可行时用。

Eq5–12，p6

## 2. 尾延时控制误差

```latex
m_t=\frac{\mathrm{P95}(TBT)}{100\,\mathrm{ms}}
```

m无量纲；m>1升频，m<0.65降频，中间死区保持；不等PID积分。

Eq13/§3.3，p7
