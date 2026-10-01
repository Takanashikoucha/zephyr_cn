.. _timing_noise_policy:

Timing Noise CPU Frequency Scaling Policy
#########################################

Overview
########

Timing noise policy 为周期性
选择随机 performance state (P-state) 的 CPU frequency scaling policy。其意图为通过
jitter CPU clock 注入 timing
variability（这可扰乱假设稳定 frequency 的 naive cycle-count
或 wall-clock 测量。

此为 randomized P-state policy。其非通用 side-channel
countermeasure。

Primary Mitigation
##################

经 side-channel 泄漏审查的 constant-time 和 constant-flow 实现
仍为对抗 timing 攻击的主要 mitigation。
此 policy 不替代这些 practices。至多（其可能使
特定类测量复杂化。

Attacker Model
##############

此 policy 考虑以下 adversary：

* 通过 cycle counters、wall-clock timers 或
  类似 software-visible timestamps 观察相对执行时间
* 依赖稳定 CPU frequency（使指令
  count 或 data-dependent paths 的小差异在 trials 间仍可区分

Randomized P-state 选择不击败此类攻击。给定足够
samples（attacker 常可平均掉 noise。Policy 仅
使这些测量更不便且更不可重复。

Use Cases
#########

当 application 想在已健全的 software 之上添加额外 timing
variability 作为次要层时（此 policy 可能有用。应
将其视为扰乱某些 analyses 的方式（而非
本身的安全 solution。

其不适合：

* 需确定性执行时间的 Hard real-time systems
* timing 可预测性为 safety case 一部分的 Safety-related systems
* 不能容忍意外慢 P-states 的 Latency-sensitive workloads
* 严格 power-budget designs（因为频繁 P-state 变更可能增加
  平均 power 消耗

Configuration
#############

启用 CPU frequency subsystem 并选择 timing noise policy：

.. code-block:: kconfig

   CONFIG_CPU_FREQ=y
   CONFIG_CPU_FREQ_POLICY_TIMING_NOISE=y

Policy 用标准 CPU frequency subsystem update interval（
配置为：

.. code-block:: kconfig

   CONFIG_CPU_FREQ_INTERVAL_MS=<interval>

更小 update intervals 增加 timing variability（但也增加
frequency transitions 数量。

Random Number Generation
########################

Policy 用 :c:func:`sys_rand32_get()` 选择 performance states。
选择 ``CONFIG_CPU_FREQ_POLICY_TIMING_NOISE`` 在有 hardware entropy source 的
platforms 上启用 entropy driver。有 TRNG 时首选
通过该 driver 路由 random draws：

.. code-block:: kconfig

   CONFIG_ENTROPY_DEVICE_RANDOM_GENERATOR=y

Limitations
###########

* 不消除 timing side channels
* 不能补偿根本不安全的 software
* 可能降低整体 system performance
* 可能因频繁 performance state 变更增加 power 消耗
* 对坚定或充分 instrumented 的 attacker 不提供任何保证

timing noise policy 示例参见
:zephyr:code-sample:`cpu_freq_timing_noise` sample。
