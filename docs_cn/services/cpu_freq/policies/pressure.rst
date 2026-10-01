.. _pressure_policy:

Pressure based CPU Frequency Scaling Policy
###########################################

Pressure policy 评估 ready queue 的当前 pressure 以
通知 system
P-state transitions。

Thread pressure 由以下公式计算：

.. math::

   P_{sys} = \frac{\sum_{t \in R} (P_{min} - prio_t + 1)}
                   {\sum_{t \in T} (P_{min} - prio_t + 1)} \times 100

其中

- :math:`R` 为 runnable (queued) threads 集合
- :math:`T` 为用于 pressure 考虑的所有 threads 集合
- :math:`w_t = P_{min} - \text{prio}_t + 1` 为 thread :math:`t` 的 weight
- :math:`P_{min}` 为考虑的配置最小 priority（数值上最大值）

这产生 0 到 100 间的 normalized system pressure（然后用于
按 SoC 或 overlay file 定义选择适当
P-state。

计算 normalized system pressure 后（其被视为 system 'load'（
然后 policy 遍历 SoC 的可用 P-states（并选择第一个
normalized pressure 大于或等于定义 threshold 的 P-state。

若无 P-state 匹配（即 normalized pressure 低于所有 thresholds）（policy 将选择
soc_pstates array 中最后一个 P-state（最低 performance state。

User 可通过调整
:kconfig:option:`CONFIG_CPU_FREQ_POLICY_PRESSURE_LOWEST_PRIO` option 调整此 policy 的
responsiveness（其应设为
system 中最低 priority thread 的 priority（数值上为最大数字）。Pressure
policy 将忽略低于此 option 的 threads（且由于上述公式（将改变
高 priority thread 运行的感知影响。

pressure policy 示例参见 :zephyr:code-sample:`cpu_freq_pressure` sample。

此 policy 尝试主动评估 queued tasks（并在其执行时间前调整 clock
frequency（尽管此 policy 对 threads 达成其 deadlines 并避免
starvation 的 performance 或 determinism 不作任何保证。

注意 :kconfig:option:`CONFIG_CPU_FREQ_POLICY_PRESSURE_LOWEST_PRIO` 包含 :kconfig:option:`CONFIG_TRACING`
引入 context switching 的 overhead。
