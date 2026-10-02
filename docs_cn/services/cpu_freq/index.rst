.. _cpu_freq:

CPU 频率调节
#####################

.. toctree::
   :maxdepth: 1

   policies/index.rst
   thermal_cap.rst

概述
********

Zephyr 中的 CPU 频率调节（CPU Frequency Scaling）子系统为 SoC 提供了一个框架，使其能够根据
被监控的指标（metric）和性能状态（P-state）策略算法动态调整
处理器频率。

设计目标
************

CPU 频率调节子系统旨在提供一个框架，使任意策略算法
都能与任意 P-state 驱动程序协同工作，并允许每个策略使用一个或多个
指标来确定最佳 CPU 频率。该子系统应当足够灵活，以便 SoC 厂商
可以自定义 P-state、阈值和指标。

P-state 策略
****************

P-state 策略是一种算法，根据所消费的指标和每个 P-state 定义的阈值
来确定 CPU 的最佳 P-state。一个策略可以消费一个或多个
指标，根据系统的期望统计信息来确定最佳 CPU 频率。

标准策略列表参见 :ref:`policies <cpu_freq_policies>`。

指标
*******

P-state 策略应包含一个或多个作为决策依据的指标。指标的例子可以
包括 CPU 负载百分比、SoC 温度等。

一个正在使用中的指标示例，参见 :ref:`on_demand <on_demand_policy>` 策略。

温度上限
***********

可选的 :ref:`cpu_freq_thermal_cap` 根据温度触发点（trip point）限制
当前生效策略所允许的最高性能 P-state。它是一个约束层，而不是 P-state 策略，
用于减少过多的热量产生并保护 SoC 免受热应力影响。

P-state 驱动程序
***************

支持 CPU 频率调节子系统的 SoC 必须实现一个 P-state 驱动程序，其中实现
:c:func:`cpu_freq_pstate_set`，在调用时将传入的 ``p_state`` 应用到
CPU。

SoC 还必须在设备树（devicetree）中提供可用的 P-state，即拥有一个
:dtcompatible:`zephyr,pstate` 兼容节点。SoC 还可以定义自己的 P-state 绑定（binding），
它扩展 :dtcompatible:`zephyr,pstate` 以包含额外的属性，这些属性可被
SoC 的 P-state 驱动程序使用。

使用注意事项
********************

CPU 频率调节子系统被设计为在 UP 和 SMP 系统上都能工作。在 SMP 系统上，
默认假设每个 CPU 都以相同的速率运行时钟。因此，如果一个 CPU
经历了 P-state 转换，那么所有其他 CPU 也会经历相同的 P-state 转换。
SoC 可以通过启用 :kconfig:option:`CONFIG_CPU_FREQ_PER_CPU_SCALING`
配置选项来覆盖此行为，允许每个 CPU 独立运行时钟。

支持 CPU 频率调节的 SoC 必须遵守 Zephyr 的要求，即系统定时器
频率在整个程序生命周期内保持稳定。更多信息参见 :ref:`Kernel Timing <kernel_timing>`。

CPU 频率调节子系统作为 ``k_timer`` 的处理函数运行，这意味着它运行
在中断上下文（IRQ）中。SoC 的 P-state 驱动程序必须确保其对
:c:func:`cpu_freq_pstate_set` 的实现是中断上下文安全的。如果 P-state 转换
无法在 IRQ 上下文中合理地完成，建议 SoC 的 P-state 驱动程序
将其任务实现为一个工作队列（workqueue）项。
