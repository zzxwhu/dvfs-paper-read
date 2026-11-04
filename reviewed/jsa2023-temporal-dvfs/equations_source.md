# 公式源代码与对应位置

每组公式与正文同名图片对应。背景和教学模型不冒充作者提出的方法；k/D/Δt 为便于教学而重排的符号。

## eq01-power

```latex
P_{dyn}=\alpha C V^2 f
E=\int_0^{T_{exec}}P(t)\,dt\quad\approx\quad \overline{P}\,T_{exec}
```

## eq02-time

```latex
T_{exec}\approx\frac{N_{cycles}}{f}+T_{wait}
S=D-T_{exec}
```

## eq03-objective

```latex
\min_{\{a_k\}}\ E\qquad\mathrm{subject\ to}\quad T_{exec}\leq D
```

## eq04-state

```latex
s_k=(i_k,u_k,c_k,p_k)
\widehat f_k=\frac{f_k-f_{min}}{f_{max}-f_{min}},\qquad i_k=(\widehat f_k,\ell_{avg,k},\ell_{max,k})
u_k=u_{k-1}+\frac{\Delta t_k\ell_{avg,k}}{D},\qquad c_k=c_{k-1}+\frac{\Delta t_k}{D}
p_k[f_k,b_k]=p_{k-1}[f_k,b_k]+\frac{\Delta t_k}{D}
```

## eq05-action

```latex
a_k^*=\operatorname{argmax}_{a\in A} Q(s_k,a;\theta)
```

## eq06-reward

```latex
r_f=\sum_{f\in F}\left(1-\frac{f^3-f_{min}^3}{f_{max}^3-f_{min}^3}\right)\frac{\tau_f}{D}
r_u=\mathrm{average\ CPU\ utilization\ in\ the\ task\ window}
R=\frac{1}{2}r_f+\frac{1}{2}r_u\qquad (\mathrm{on\ time})
```

## eq07-ddqn

```latex
a^*=\operatorname{argmax}_{a\in A}Q(s_{k+1},a;\theta)
y_k=r_k+\gamma Q(s_{k+1},a^*;\theta^{-})
L(\theta)=\left[y_k-Q(s_k,a_k;\theta)\right]^2
```

## eq08-saving

```latex
\mathrm{energy\ saving}=1-\frac{E_{method}}{E_{baseline}}
\mathrm{miss\ rate}=\frac{N_{late}}{N_{total}}
```

