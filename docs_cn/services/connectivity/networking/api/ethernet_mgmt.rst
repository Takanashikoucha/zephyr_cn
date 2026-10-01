.. _ethernet_mgmt_interface:

Ethernet Management
###################

.. contents::
    :local:
    :depth: 2

Overview
********

Ethernet management API 提供管理 Ethernet network interface 低层 status 的 functions。这些 functions 的 caller 可：

* 触发 ``carrier ON`` 或 ``carrier OFF`` management events
* 触发 ``VLAN enabled`` 或 ``VLAN disabled`` management events

通常 ``carrier OFF`` event 由 Ethernet device driver 在注意到 Ethernet cable 断开时生成。``carrier ON`` event 在 Ethernet device driver 注意到 Ethernet cable 重新连接时生成。

当前 VLAN events 由 Ethernet L2 layer 在特定 VLAN tag 启用或禁用时生成。

User application 可在需要于对应 status 变化时行动时监控这些 events。

API Reference
*************

.. doxygengroup:: ethernet_mgmt
