.. _twister_power_harness:

Power
#####

``power`` 测试框架用于测量和验证电流消耗。它与 pytest 集成，使用硬件电源监控器执行自动化数据收集和分析。

该测试框架执行以下步骤：

1. 通过 ``PowerMonitor`` 抽象接口初始化电源监控设备（例如 ``stm_powershield``）。
#. 为定义的 ``measurement_duration`` 开始电流测量。
#. 收集原始电流波形数据。
#. 使用峰值检测算法，基于电源转换将数据分段为定义的执行阶段。
#. 使用工具函数计算每个阶段的 RMS 电流值。
#. 将计算值与用户定义的期望 RMS 值进行比较。

.. code-block:: yaml

    harness: power
    harness_config:
      fixture: pm_probe
      power_measurements:
        elements_to_trim: 100
        min_peak_distance: 40
        min_peak_height: 0.008
        peak_padding: 40
        measurement_duration: 6
        num_of_transitions: 4
        expected_rms_values: [56.0, 4.0, 1.2, 0.26, 140]
        tolerance_percentage: 20

- **elements_to_trim** – 测量开始时丢弃的样本数，以消除噪声。
- **min_peak_distance** – 检测到的电流峰值之间的最小距离（有助于检测不同的转换）。
- **min_peak_height** – 作为峰值的最低电流阈值（单位：安培）。
- **peak_padding** – 每个检测到的峰值周围扩展的样本数。
- **measurement_duration** – 记录电流数据的总时间（单位：秒）。
- **num_of_transitions** – 测试执行期间被测设备（DUT）中期望的电源状态转换次数。
- **expected_rms_values** – 每个识别出的执行阶段的目标 RMS 值（单位：毫安）。
- **tolerance_percentage** – 允许偏离期望 RMS 值的百分比。
