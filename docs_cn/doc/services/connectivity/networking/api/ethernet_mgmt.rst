.. _ethernet_mgmt_interface:

以太网管理
###################

.. contents::
    :local:
    :depth: 2

概述
****

以太网管理 API 提供用于管理以太网网络接口底层状态的函数。这些函数的调用者可以：

* 触发 ``carrier ON`` 或 ``carrier OFF`` 管理事件
* 触发 ``VLAN enabled`` 或 ``VLAN disabled`` 管理事件

通常，当以太网设备驱动程序注意到以太网电缆被断开时，会生成 ``carrier OFF`` 事件。当以太网设备驱动程序注意到以太网电缆重新连接时，会生成 ``carrier ON`` 事件。

目前，当特定的 VLAN 标签被启用或禁用时，VLAN 事件由以太网 L2 层生成。

如果用户应用程序需要在相应状态变化时采取行动，可以监控这些事件。

API 参考
*********

.. doxygengroup:: ethernet_mgmt
