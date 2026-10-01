.. _cpu_freq_thermal_cap:

CPU Frequency Thermal Cap
#########################

CPU frequency thermal cap 为 CPU Frequency Scaling
subsystem 的可选 constraint layer。Active policy 选择请求的 P-state（且当配置的
temperature trip points active 时 thermal cap 限制
允许的最高 performance P-state。

这将 performance demand 和 thermal mitigation 分开：

* CPU frequency policy 按其自己的 metrics 和
  thresholds 选择请求的 P-state。
* Thermal cap 将该 request clamp 到当前
  temperature 允许的最高 performance P-state。

Clamping 后（结果 P-state 被传递给 SoC P-state driver。

Devicetree
**********

添加 :dtcompatible:`zephyr,cpu-freq-thermal-cap` node 并启用
:kconfig:option:`CONFIG_CPU_FREQ_THERMAL_CAP` 启用 thermal cap。

示例：

.. code-block:: devicetree

   cpu_freq_thermal_cap: cpu_freq_thermal_cap {
           compatible = "zephyr,cpu-freq-thermal-cap";
           sensor = <&temp0>;
           sensor-channel = "die-temp";
           polling-delay-ms = <1000>;
           trip-active-polling-delay-ms = <100>;

           trip_0 {
                   temperature-millicelsius = <85000>;
                   hysteresis-millicelsius = <5000>;
                   cap-pstate = <&pstate_1>;
           };

           trip_1 {
                   temperature-millicelsius = <95000>;
                   hysteresis-millicelsius = <3000>;
                   cap-pstate = <&pstate_2>;
           };
   };

``trip_0`` active 时（CPU frequency requests 被 cap 到 ``pstate_1`` 或更低。
``trip_1`` active 时（requests 被 cap 到 ``pstate_2`` 或更低。Cap 不
强制 CPU 在该 P-state 运行；对更低 performance P-state 的 policy request
保持不变。

Thermal cap constraints 用 CPU frequency P-state index 顺序。更低 index P-states
为更高 performance（更高 index P-states
为更低 performance 且更 restrictive。
每个 ``cap-pstate`` 须用 phandle 引用该有序 table 中的 P-state。

Runtime behavior
****************

Temperature sampling 从 delayable work item 执行（因为 sensor drivers 可能用
blocking operations。CPU frequency timer 在应用
policy result 时仅读取 cached cap。

若 temperature sampling 反复失败（cap 应用最低 performance
P-state（table 中最高 index）作为 fail-safe constraint。
