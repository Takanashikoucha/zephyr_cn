.. _cpu_freq:

CPU Frequency Scaling
#####################

.. toctree::
   :maxdepth: 1

   policies/index.rst
   thermal_cap.rst

Overview
********

Zephyr 中的 CPU Frequency Scaling subsystem 提供框架供 SoC 根据
monitored metric 和 performance state (P-state) policy
algorithm 动态调整
processor frequency。

Design Goals
************

CPU Frequency Scaling subsystem 旨在提供允许任何 policy algorithm
与任何 P-state driver 一起工作的框架（且允许每个 policy
使用一个或多个 metrics
确定最优 CPU frequency。Subsystem 应足够灵活（允许 SoC vendors
定义自定义 P-states、thresholds 和 metrics。

P-state Policies
****************

P-state policy 为基于其消费的 metrics 和每 P-state 定义的
thresholds 确定 CPU 最优 P-state 的 algorithm。Policy 可消费一个或多个
metrics 基于 system 的期望 statistics 确定最优 CPU frequency。

标准 policies 列表参见 :ref:`policies <cpu_freq_policies>`。

Metrics
*******

P-state policy 应包含一个或多个 metrics 作为决策基础。Metrics 的示例可
包括 percent CPU load、SoC temperature 等。

metric 使用示例参见 :ref:`on_demand <on_demand_policy>` policy。

Thermal Cap
***********

可选的 :ref:`cpu_freq_thermal_cap` 基于 temperature trip points
约束 active policy 允许的最高 performance P-state。其为 constraint layer（非 P-state policy（
用于减少 excess heat 生成（并保护 SoC 免受 thermal stress。

P-state Drivers
***************

支持 CPU Frequency Scaling subsystem 的 SoC 须实现实现
:c:func:`cpu_freq_pstate_set 的 P-state driver（其
调用时将传入的 ``p_state`` 应用到
CPU。

SoC 还须用
:dtcompatible:`zephyr,pstate` compatible node 在 devicetree 中提供可用
P-states。SoC 还可定义自己的 P-state binding（
其扩展 :dtcompatible:`zephyr,pstate` 以包含 SoC 的 P-state driver 可能使用的
额外 properties。

Usage considerations
********************

CPU Frequency Scaling subsystem 设计为在 UP 和 SMP system 上工作。在 SMP systems 上（
默认假设各 CPUs 以相同 rate 时钟。因此（若一个 CPU
经历 P-state transition（则所有其他 CPUs 也经历相同 P-state transition。
SoC 可启用 :kconfig:option:`CONFIG_CPU_FREQ_PER_CPU_SCALING`
configuration option 覆盖此（以允许各 CPU 独立时钟。

支持 CPU Frequency Scaling 的 SoC 须遵守 Zephyr 的 system timer
frequency 在 program 生命周期内保持稳定的要求。更多
信息参见 :ref:`Kernel Timing <kernel_timing>`。

CPU Frequency Scaling subsystem 作为 ``k_timer`` 的 handler function 运行（意味着其
在 interrupt context (IRQ) 中运行。SoC P-state driver 须确保其
:c:func:`cpu_freq_pstate_set 实现 IRQ context safe。若 P-state transition
不能在 IRQ context 中合理完成（建议 SoC 的 P-state driver
将其 task 实现为 workqueue item。
