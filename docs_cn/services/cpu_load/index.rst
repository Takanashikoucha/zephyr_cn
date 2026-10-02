.. _cpu_load:

CPU 负载
########

CPU 负载模块跟踪 CPU 处于空闲状态之外的时间占比。有两个
测量后端可供选择，通过 ``CPU_LOAD_BACKEND`` Kconfig 选项选择：

调度器运行时间统计
   :kconfig:option:`CONFIG_CPU_LOAD_BACKEND_RUNTIME_STATS` 从调度器的
   每 CPU 运行时间统计信息推导负载。它跨架构可移植并支持多 CPU。

架构空闲钩子
   :kconfig:option:`CONFIG_CPU_LOAD_BACKEND_IDLE_HOOK` 使用架构
   空闲钩子（在 CPU 进入空闲前后被调用）来测量负载。它的开销比
   运行时间统计后端更低，并且可以使用 :ref:`counter_api` 设备获得更高精度
   （计数器路径仅支持单 CPU）。它在任何发出空闲
   钩子的架构上可用（:kconfig:option:`CONFIG_ARCH_HAS_CPU_IDLE_HOOKS`）。与 :ref:`thread_analyzer` 相比，它
   更精确，因为它同时考虑了在中断上下文中花费的时间。该
   后端不依赖跟踪（tracing）子系统。

负载通过 :c:func:`cpu_load_get`（当前 CPU）或 :c:func:`cpu_load_get_cpu`
（特定 CPU）获取。两者都以千分比（per mille，0...1000）返回负载，
并可重置测量窗口。使用 :c:macro:`CPU_LOAD_PERMILLE_TO_PERCENT` 将值转换为整百分比。

负载也可以定期通过日志消息报告。周期通过
:kconfig:option:`CONFIG_CPU_LOAD_LOG_PERIODICALLY` 配置。

示例参见 :zephyr:code-sample:`cpu_freq_on_demand` 示例。

使用计数器设备
**********************

空闲钩子后端默认使用 :c:func:`k_cycle_get_32`。当需要更高精度时，
可以启用 :kconfig:option:`CONFIG_CPU_LOAD_USE_COUNTER` 并在设备树中
设置所选节点，从而使用 :ref:`counter_api` 设备。

.. code-block:: devicetree

   chosen {
     zephyr,cpu-load-counter = &counter_device;
   };
