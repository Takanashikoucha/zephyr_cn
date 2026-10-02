.. _bluetooth_mesh_stat:

Mesh 统计
##############

统计 API 提供对 Bluetooth Mesh 通信的运行时监控。

帧统计
***************

帧统计 API 允许监控通过不同接口接收到的帧数量，以及计划的、成功完成的传输和转发尝试次数。

该 API 帮助用户评估广播器配置参数的效率和设备的扫描能力。所监控的参数数量可通过客户自定义值轻松扩展。

LPN 计时测量
**********************

当启用 :kconfig:option:`CONFIG_BT_MESH_LOW_POWER` 时，统计模块通过对协议事件打时间戳来测量 LPN friendship 计时参数：

* T1：Poll 发送完成
* T2：扫描器启用（ReceiveDelay 已超时）
* T3：收到 Friend 响应或 ReceiveWindow 已超时

根据这些时间戳，该模块以微秒为单位计算实测的 ReceiveDelay（T2 - T1）和 ReceiveWindow（T3 - T2）。应用程序可使用这些值将实际空中计时与已配置的 friendship 参数进行对比评估。

应用程序可以在任何时间读取并重置统计数据。

API 参考
*************

.. doxygengroup:: bt_mesh_stat
