.. _thread_protocol_interface:

Thread protocol
###############

.. contents::
    :local:
    :depth: 2

Overview
********
Thread 为专为 home automation applications 设计的低功耗 mesh networking technology。其为基于 IPv6 的 standard（在 IEEE 802.15.4 protocol 上使用 6LoWPAN technology。IP connectivity 让您轻松将 Thread mesh network 通过 Thread Border Router 连接到 internet。

Thread specification 提供高 network security。用 Thread 构建的 mesh networks 安全——仅 authenticated devices 可加入 network（且 mesh 内所有 communications 加密。Thread protocol 更多信息可在 `Thread Group website <https://www.threadgroup.org>`_ 找到。

Zephyr 集成名为 OpenThread 的 open source Thread protocol 实现（在 `OpenThread website <https://openthread.io/>`_ 文档化。

Internet connectivity
*********************

连接 mesh network 到 internet 需 Thread Border Router。OpenThread community 提供 Thread Border Router 的 open source 实现。Border Router 设置说明参见 `OpenThread Border Router guide <https://openthread.io/guides/border-router>`_。

Sample usage
************

可尝试用 Zephyr Echo server 和 Echo client samples 使用 OpenThread（其为 OpenThread 提供 out-of-the-box configuration。要在此类 samples 中启用 OpenThread 支持（用 ``overlay-ot.conf`` overlay config file 构建。细节参见 :zephyr:code-sample:`sockets-echo-server` 和 :zephyr:code-sample:`sockets-echo-client` samples。

Zephyr 还提供 :zephyr:code-sample:`openthread-shell`（对测试和调试 Thread 及其底层 IEEE 802.15.4 drivers 有用。

Thread related APIs
*******************

OpenThread Driver API
========================

OpenThread L2 内部使用 Zephyr 的 protocol agnostic IEEE 802.15.4 driver API。此 API 对想支持 OpenThread 的 **driver developers** 有兴趣。

Driver API 为 :ref:`ieee802154_driver_api` subsystem 的一部分（并在那里文档化。

OpenThread L2 Adaptation Layer API
==================================

Zephyr 的 OpenThread L2 platform adaptation layer 将外部 OpenThread stack 与 Zephyr 的 IEEE 802.15.4 protocol agnostic driver API 粘合。此 API 仅对 OpenThread L2 **subsystem contributors** 有兴趣。

OpenThread Platform API
=======================

OpenThread platform API 由 OpenThread stack 定义（并在 Zephyr 中作为 OpenThread module 实现。Applications 可直接使用此实现（或通过 OpenThread L2 adaptation layer 访问。

Using the OpenThread L2 Adaptation Layer API
--------------------------------------------

要通过 OpenThread L2 adaptation layer 使用 OpenThread platform API（将 :kconfig:option:`CONFIG_NET_L2_OPENTHREAD` 和 :kconfig:option:`CONFIG_NETWORKING` Kconfig options 均设为 ``y`` 以启用。Adaptation layer 将使用 :file:`modules/openthread/platform/radio.c` 中找到的 OpenThread radio API 实现。此 setup 中（OpenThread stack 由 adaptation layer 初始化和管理。

Using the OpenThread Platform API Directly
------------------------------------------

也可直接使用 OpenThread platform API（绕过 OpenThread L2 adaptation layer。然而（此 approach 要求您提供与特定 radio driver 兼容的 OpenThread radio API 自己的实现。

要直接使用 OpenThread platform API（将 :kconfig:option:`CONFIG_OPENTHREAD` Kconfig option 设为 ``y``（且**不**设置 :kconfig:option:`CONFIG_NET_L2_OPENTHREAD`。此情况下（须用您的 radio driver 实现 `OpenThread radio API
<https://openthread.io/reference/group/radio-config>`_ 中的以下 functions：

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

此外（须实现 OpenThread radio API（参见 :zephyr_file:`include/zephyr/net/openthread.h`）中的以下 functions 以处理 radio 初始化和 event 处理：

* :c:func:`platformRadioInit`
* :c:func:`platformRadioProcess`

要以此 approach 初始化 OpenThread stack（或在 application 中调用 :c:func:`ot_platform_init` function（或启用 :kconfig:option:`CONFIG_OPENTHREAD_SYS_INIT` Kconfig option 以在 system 启动期间自动初始化 OpenThread。可用 :kconfig:option:`CONFIG_OPENTHREAD_SYS_INIT_PRIORITY` Kconfig option 设置初始化 priority。

.. doxygengroup:: openthread
