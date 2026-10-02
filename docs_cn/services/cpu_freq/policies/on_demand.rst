.. _on_demand_policy:

按需（On-Demand）CPU 频率调节策略
######################################

按需策略使用 :ref:`CPU Load <cpu_load>` 评估当前 CPU 负载，
并将其与 SoC P-state 定义中定义的触发阈值进行比较。

按需策略会遍历已定义的 P-state，并选择第一个 CPU 负载
大于或等于其定义阈值的 P-state。

如果没有 P-state 匹配（即 CPU 负载低于所有阈值），该策略将选择
soc_pstates 数组中的最后一个 P-state（最低性能状态）。这是该策略的固有特性：
P-state 必须在设备树中按阈值递减顺序定义，最后一个
P-state 将用于低于所有阈值的负载。

按需策略的示例参见 :zephyr:code-sample:`cpu_freq_on_demand` 示例。

该策略是被动的。频率调整只会在观察到系统负载变化
之后发生，因此它无法预判突发的重载。该策略没有任务截止时间的概念，
不应被视为实时策略。
