.. _pressure_policy:

基于压力的 CPU 频率调节策略
###########################################

压力策略评估就绪队列（ready queue）的当前压力，
以指导系统 P-state 转换。

线程压力由以下公式计算：

.. math::

   P_{sys} = \frac{\sum_{t \in R} (P_{min} - prio_t + 1)}
                   {\sum_{t \in T} (P_{min} - prio_t + 1)} \times 100

其中

- :math:`R` 是可运行（已入队）线程的集合
- :math:`T` 是用于压力计算的所有线程的集合
- :math:`w_t = P_{min} - \text{prio}_t + 1` 是线程 :math:`t` 的权重
- :math:`P_{min}` 是配置的最小优先级（数值上为最大值）

该公式产生一个 0 到 100 之间的归一化系统压力值，
然后用于选择由 SoC 或 overlay 文件定义的合适 P-state。

一旦计算出归一化系统压力，它就被当作系统的"负载"处理，
然后策略会遍历 SoC 可用的 P-state，选择第一个归一化压力
大于或等于其定义阈值的 P-state。

如果没有 P-state 匹配（即归一化压力低于所有阈值），该策略将选择
soc_pstates 数组中的最后一个 P-state（最低性能状态）。

用户可以通过调整
:kconfig:option:`CONFIG_CPU_FREQ_POLICY_PRESSURE_LOWEST_PRIO` 选项来调节该策略的响应性，
该选项应设置为系统中最低优先级线程的优先级（数值上为最大数字）。压力
策略将忽略优先级低于该选项的线程，并且由于上述公式，会改变
高优先级线程运行时的感知影响。

压力策略的示例参见 :zephyr:code-sample:`cpu_freq_pressure` 示例。

该策略尝试主动评估已入队的任务，并在其执行时间之前
提前调整时钟频率，但该策略不保证线程达到其截止时间的性能
或确定性，也不保证避免饥饿（starvation）。

注意 :kconfig:option:`CONFIG_CPU_FREQ_POLICY_PRESSURE_LOWEST_PRIO` 包含 :kconfig:option:`CONFIG_TRACING`
会引入上下文切换的开销。
