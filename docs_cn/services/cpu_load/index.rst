.. _cpu_load:

CPU load
########

CPU load module 跟踪 CPU 在 idle state 外花费时间的比例。两个
measurement backends 可用（用 ``CPU_LOAD_BACKEND`` Kconfig choice 选择：

Scheduler runtime statistics
   :kconfig:option:`CONFIG_CPU_LOAD_BACKEND_RUNTIME_STATS` 从 scheduler
   每 CPU runtime statistics 推导 load。其跨 architectures 可移植（且支持多个 CPUs。

Architecture idle hooks
   :kconfig:option:`CONFIG_CPU_LOAD_BACKEND_IDLE_HOOK` 用 architecture
   idle hooks 测量 load（其在 CPU 进入 idle 前后被调用。其 overhead 低于
   runtime-statistics backend（且可
   用 :ref:`counter_api` device 获得更高 precision
   （counter path 仅单 CPU）。其在发出 idle
   hooks 的任何 architecture 上可用（:kconfig:option:`CONFIG_ARCH_HAS_CPU_IDLE_HOOKS`）。与 :ref:`thread_analyzer` 相比
   其更准确（因为其也考虑 interrupt context 中花费的时间。
   此 backend 不依赖 tracing subsystem。

Load 用 :c:func:`cpu_load_get 为当前 CPU 或 :c:func:`cpu_load_get_cpu`
为特定 CPU 获取。两者返回 per mille (0...1000) 的 load（且可重置
measurement
window。用 :c:macro:`CPU_LOAD_PERMILLE_TO_PERCENT` 将值转为整 percent。

Load 也可用 logging message 周期性报告。Period 用
:kconfig:option:`CONFIG_CPU_LOAD_LOG_PERIODICALLY` 配置。

示例参见 :zephyr:code-sample:`cpu_freq_on_demand` sample。

Using a counter device
**********************

Idle-hook backend 默认用 :c:func:`k_cycle_get_32`。需更高 precision 时
可启用 :kconfig:option:`CONFIG_CPU_LOAD_USE_COUNTER`（并在
devicetree 中设置 chosen node 用 :ref:`counter_api` device。

.. code-block:: devicetree

   chosen {
     zephyr,cpu-load-counter = &counter_device;
   };
