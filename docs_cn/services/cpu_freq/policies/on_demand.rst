.. _on_demand_policy:

On-Demand CPU Frequency Scaling Policy
######################################

On-Demand policy 用
:ref:`CPU Load <cpu_load>` 评估当前 CPU load（并将其与
SoC P-state definition 定义的 trigger threshold 比较。

On-Demand policy 将遍历定义的 P-states（并选择第一个
CPU load 大于或等于定义 threshold 的 P-state。

若无 P-state 匹配（即 CPU load 低于所有 thresholds）（policy 将选择
soc_pstates array 中最后一个 P-state（最低 performance state。这是
policy 固有的：P-states 须在 devicetree 中按递减 threshold 顺序定义（且
最后一个 P-state 用于低于所有 thresholds 的 loads。

on-demand policy 示例参见 :zephyr:code-sample:`cpu_freq_on_demand` sample。

此 policy 为 reactive。仅在观察到 system load 变化后才发生 frequency 调整（
故其不能预见突然高 loads。Policy 无 task deadlines 概念（
不应视为 real-time policy。
