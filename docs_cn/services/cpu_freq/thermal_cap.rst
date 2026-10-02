.. _cpu_freq_thermal_cap:

CPU 频率温度上限
#########################

CPU 频率温度上限是 CPU 频率调节
子系统的可选约束层。当前生效的策略选择所请求的 P-state，而温度上限在
配置的温度触发点生效时限制所允许的最高性能 P-state。

这将性能需求与热缓解分离开来：

* CPU 频率策略根据自身的指标和
  阈值选择所请求的 P-state。
* 温度上限将该请求钳制（clamp）到当前温度
  允许的最高性能 P-state。

钳制之后，得到的 P-state 被传递给 SoC P-state 驱动程序。

设备树
**********

通过添加 :dtcompatible:`zephyr,cpu-freq-thermal-cap` 节点并启用
:kconfig:option:`CONFIG_CPU_FREQ_THERMAL_CAP` 来启用温度上限。

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

当 ``trip_0`` 生效时，CPU 频率请求被钳制到 ``pstate_1`` 或更低。
当 ``trip_1`` 生效时，请求被钳制到 ``pstate_2`` 或更低。上限并不
强制 CPU 运行在该 P-state；策略对较低性能 P-state 的请求
保持不变。

温度上限约束使用 CPU 频率 P-state 索引顺序。索引较低的 P-state
性能更高，索引较高的 P-state 性能更低且限制更严格。
每个 ``cap-pstate`` 必须通过 phandle 引用该有序表中的一个 P-state。

运行时行为
****************

温度采样在一个可延迟的工作项（delayable work item）中完成，因为传感器驱动程序可能使用
阻塞操作。CPU 频率定时器在应用
策略结果时只读取缓存的上限值。

如果温度采样反复失败，上限将应用最低性能
P-state（表中索引最高者）作为故障安全（fail-safe）约束。
