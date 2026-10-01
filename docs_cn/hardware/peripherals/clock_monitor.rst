.. _clock_monitor_api:

时钟监控
#############

概述
********

时钟监控 API 提供对硬件外设的访问，这些外设在运行时观察时钟信号，
并在其频率漂移超出预期范围或完全停止时上报。该 API 面向功能安全
与诊断用例——检测失效的振荡器、丢失的参考时钟，或关键时钟树上
超出规格的频率漂移。

操作模式
***************

两种模式共享同一个生命周期：用 :c:func:`clock_monitor_configure` 配置，
用 :c:func:`clock_monitor_start` 开始运行，
用 :c:func:`clock_monitor_stop` 结束。

该 API 提供两种操作模式：

``CLOCK_MONITOR_MODE_WINDOW``
   连续阈值检查。硬件将所监控时钟的频率与由
   :c:member:`clock_monitor_window_cfg.expected_hz` 和
   :c:member:`clock_monitor_window_cfg.tolerance_ppm` 派生的可编程高、低边界
   进行比较。阈值穿越事件通过配置时安装的用户回调异步送达。

``CLOCK_MONITOR_MODE_MEASURE``
   每次 :c:func:`clock_monitor_start` 进行一次频率测量，
   结果通过配置时的回调送达（``CLOCK_MONITOR_EVT_MEASURE_DONE``
   事件，外加以赫兹为单位的测量值）。设备在回调执行前会自动回到
   已配置的（停止）状态，因此正常路径下无需调用
   :c:func:`clock_monitor_stop`。要重复测量，可从回调中再次调用
   :c:func:`clock_monitor_start`——:c:func:`clock_monitor_start` 和
   :c:func:`clock_monitor_stop` 都是中断安全的（与从回调中重新武装
   计数器闹钟相同的惯用法）。

对于 MEASURE 模式，API 不提供阻塞式等待：超时由应用自行管理。
通常的做法是：用应用自行选择的超时时间等待由回调给出的信号量，
并在超时路径上调用 :c:func:`clock_monitor_stop` 中止进行中的测量。
另一种方式是用 :c:func:`clock_monitor_get_rate` 轮询最近一次结果——
这也是用户态线程的获取路径，因为用户态线程可能无法安装回调。

事件
******

事件以位掩码形式通过 :c:member:`clock_monitor_event_data.events` 送达：

* ``CLOCK_MONITOR_EVT_FREQ_HIGH`` —— 所监控频率超过上限阈值（WINDOW 模式）。
* ``CLOCK_MONITOR_EVT_FREQ_LOW`` —— 所监控频率低于下限阈值（WINDOW 模式）。
* ``CLOCK_MONITOR_EVT_CLOCK_LOST`` —— 所监控时钟在测量窗口内停止产生边沿（MEASURE 模式硬件故障）。
* ``CLOCK_MONITOR_EVT_MEASURE_DONE`` —— 测量成功完成（MEASURE 模式）；
  :c:member:`clock_monitor_event_data.measured_hz` 保存测量结果。

配置时的回调是唯一的事件送达路径。对于 MEASURE 模式，最近一次已完成的
结果额外可以通过轮询 :c:func:`clock_monitor_get_rate` 获取。
WINDOW 模式的用户态观察者（可能无法安装回调）通过特权态中继接收事件
（例如由回调写入的 :c:struct:`k_msgq` 消息队列）。

配置
*************

时钟监控必须先通过 :c:func:`clock_monitor_configure` 配置才能启动。
配置内容包含操作模式、模式相关参数（预期频率、容差、测量窗口）
以及可选的异步回调。只有在监控器处于停止状态时才能进行配置；
重新配置的方式是用新的模式/参数集再次调用 :c:func:`clock_monitor_configure`——
没有单独的拆除操作。完整返回码列表参见 `API 参考`_ 中的
:c:func:`clock_monitor_configure`。

相关配置选项：

* :kconfig:option:`CONFIG_CLOCK_MONITOR`

API 参考
*************

.. doxygengroup:: clock_monitor_interface
