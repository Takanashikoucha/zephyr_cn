.. _thread_protocol_interface:

Thread 协议
###############

.. contents::
    :local:
    :depth: 2

概述
********

Thread 是一种低功耗网状网络技术，专为家庭自动化应用设计。它是一个基于 IPv6 的标准，
在 IEEE 802.15.4 协议之上使用 6LoWPAN 技术。借助 IP 连接，你可以轻松地将 Thread
网状网络通过 Thread 边界路由器（Thread Border Router）连接到互联网。

Thread 规范提供了高网络安全性。使用 Thread 构建的网状网络是安全的——只有经过认证
的设备才能加入网络，且网状网络内的所有通信均经过加密。有关 Thread 协议的更多信息，
请参阅 `Thread Group 网站 <https://www.threadgroup.org>`_。

Zephyr 集成了一个名为 OpenThread 的开源 Thread 协议实现，其文档见
`OpenThread 网站 <https://openthread.io/>`_。

互联网连接
*********************

连接网状网络到互联网需要一个 Thread 边界路由器。OpenThread 社区提供了一个
开源的 Thread 边界路由器实现。有关如何设置边界路由器的说明，请参阅
`OpenThread 边界路由器指南 <https://openthread.io/guides/border-router>`_。

示例用法
************

你可以尝试在 Zephyr 的 Echo 服务器和 Echo 客户端示例中使用 OpenThread，这些示例
为 OpenThread 提供了开箱即用的配置。要在这些示例中启用 OpenThread 支持，
请使用 ``overlay-ot.conf`` overlay 配置文件进行构建。详细信息请参阅
:zephyr:code-sample:`sockets-echo-server` 和 :zephyr:code-sample:`sockets-echo-client`
示例。

Zephyr 还提供了 :zephyr:code-sample:`openthread-shell`，对于测试和调试 Thread
及其底层 IEEE 802.15.4 驱动非常有用。

Thread 相关 API
*******************

OpenThread 驱动 API
========================

OpenThread L2 内部使用 Zephyr 的协议无关（protocol agnostic）的
IEEE 802.15.4 驱动 API。该 API 面向希望支持 OpenThread 的 **驱动开发者**。

该驱动 API 是 :ref:`ieee802154_driver_api` 子系统的一部分，文档见该处。

OpenThread L2 适配层 API
==================================

Zephyr 的 OpenThread L2 平台适配层将外部 OpenThread 协议栈与 Zephyr 的
协议无关的 IEEE 802.15.4 驱动 API 粘合在一起。该 API 仅面向
OpenThread L2 **子系统贡献者**。

OpenThread 平台 API
=======================

OpenThread 平台 API 由 OpenThread 协议栈定义，并在 Zephyr 中作为一个
OpenThread 模块实现。应用可以直接使用该实现，也可以通过 OpenThread L2
适配层访问它。

通过 OpenThread L2 适配层使用
--------------------------------------------

要通过 OpenThread L2 适配层使用 OpenThread 平台 API，请将
:kconfig:option:`CONFIG_NET_L2_OPENTHREAD` 和 :kconfig:option:`CONFIG_NETWORKING`
两个 Kconfig 选项均设置为 ``y``。适配层将使用位于
:file:`modules/openthread/platform/radio.c` 中的 OpenThread 无线电（radio）API
实现。在此配置下，OpenThread 协议栈由适配层初始化和管理。

直接使用 OpenThread 平台 API
------------------------------------------

你也可以直接使用 OpenThread 平台 API，绕过 OpenThread L2 适配层。
但这种方式要求你自己提供一个与特定无线电驱动兼容的 OpenThread
无线电 API 实现。

要直接使用 OpenThread 平台 API，请将 :kconfig:option:`CONFIG_OPENTHREAD`
Kconfig 选项设置为 ``y``，且 **不要** 设置 :kconfig:option:`CONFIG_NET_L2_OPENTHREAD`。
在这种情况下，你必须使用自己的无线电驱动实现
`OpenThread 无线电 API <https://openthread.io/reference/group/radio-config>`_
中的以下函数：

* ``otPlatRadioGetPromiscuous``
* ``otPlatRadioGetCcaEnergyDetectThreshold``
* ``otPlatRadioGetTransmitPower``
* ``otPlatRadioGetIeeeEui64``
* ``otPlatRadioSetPromiscuous``
* ``otPlatRadioGetCaps``
* ``otPlatRadioGetTransmitBuffer``
* ``otPlatRadioSetPanId``
* ``otPlatRadioEnable``
* ``otPlatRadioDisable``
* ``otPlatRadioReceive``
* ``otPlatRadioGetRssi``
* ``otPlatRadioGetReceiveSensitivity``
* ``otPlatRadioEnergyScan``
* ``otPlatRadioSetExtendedAddress``
* ``otPlatRadioSetShortAddress``
* ``otPlatRadioAddSrcMatchExtEntry``
* ``otPlatRadioTransmit``
* ``otPlatRadioClearSrcMatchShortEntries``
* ``otPlatRadioClearSrcMatchExtEntries``
* ``otPlatRadioEnableSrcMatch``
* ``otPlatRadioAddSrcMatchShortEntry``
* ``otPlatRadioClearSrcMatchShortEntry``
* ``otPlatRadioClearSrcMatchExtEntry``

此外，你还必须实现 OpenThread 无线电 API 中的以下函数（见
:zephyr_file:`include/zephyr/net/openthread.h`），以处理无线电初始化和事件处理：

* :c:func:`platformRadioInit`
* :c:func:`platformRadioProcess`

要在此方式下初始化 OpenThread 协议栈，可以在应用
中调用 :c:func:`ot_platform_init` 函数，或者启用
:kconfig:option:`CONFIG_OPENTHREAD_SYS_INIT` Kconfig 选项，
在系统启动时自动初始化 OpenThread。可以使用
:kconfig:option:`CONFIG_OPENTHREAD_SYS_INIT_PRIORITY` Kconfig
选项设置初始化优先级。

.. doxygengroup:: openthread
