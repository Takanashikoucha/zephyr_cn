.. _ptp_interface:

Precision Time Protocol (PTP)
#############################

.. contents::
    :local:
    :depth: 2

Overview
********

PTP 为在 application layer 实现的 network protocol（用于同步 computer network 中的 clocks。其精度达小于 1 微秒。Stack 支持 `IEEE 1588-2019 standard`_（IEEE Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems）中定义的 protocol 和 procedures。其有多个 profiles（并可实现在 L2（Ethernet）或 L3（UDP/IPv4 或 UDP/IPv6）之上。其精度通过使用 protocol packets 的 hardware timestamping 实现。

Zephyr 的 PTP stack 实现包括以下 items：

* 处理 incoming messages 和 events 的 PTP stack thread
* 与 ptp_clock driver 的集成
* system init 期间执行的 PTP stack 初始化

实现自动创建 PTP Ports（每个 PTP Port 对应唯一 interface）。

Supported features
******************

Stack 实现不支持 standard 中指定的所有 features。下表列出所有支持的 features。

.. csv-table:: Supported features
   :header: Feature, Supported
   :widths: 50,10

    Ordinary Clock, yes
    Boundary Clock, yes
    Transparent Clock,
    Management Node,
    End to end delay mechanism, yes
    Peer to peer delay mechanism, yes (two-step)
    Multicast operation mode, yes
    Hybrid operation mode, yes
    Unicast operation mode,
    Non-volatile storage,
    UDP IPv4 transport protocol, yes
    UDP IPv6 transport protocol, yes
    IEEE 802.3 (Ethernet) transport protocol, yes
    Hardware timestamping, yes
    Software timestamping,
    TIME_RECEIVER_ONLY PTP Instance, yes
    TIME_TRANSMITTER_ONLY PTP Instance,

Network transmission modes
**************************

Network transmission mode 用 ``PTP_NETWORK_MODE`` Kconfig choice 选择：

* Multicast mode（:kconfig:option:`CONFIG_PTP_NETWORK_MODE_MULTICAST`（默认）为 standard PTP mode（所有 PTP messages 发送到默认 multicast addresses。含义为每个 node 接收所有其他 nodes 的 ``Delay_Req`` 和 ``Delay_Resp`` message pairs（从而增加网络上的 traffic 量。通常仅在部署少数 timeReceivers 的小型网络中这不是问题。

* Hybrid mode（:kconfig:option:`CONFIG_PTP_NETWORK_MODE_HYBRID`）仍将 ``Announce``、``Sync`` 和 ``Follow_Up`` messages 发送到默认 multicast addresses（但 timeReceiver 将其 ``Delay_Req`` messages 作为 unicast 直接发送到当前 timeTransmitter 的 protocol address（IP address（或 IEEE 802.3 transport 的 MAC address）（其随后向请求的 timeReceiver 响应 unicast ``Delay_Resp``。这降低网络上的 PTP traffic 水平（在扩展到部署许多 timeReceivers 的更大网络时这可能是因素。Hybrid mode 仅要求 network 支持从 timeTransmitter 到 timeReceivers 的 multicast 传输。此 mode 与 linuxptp 的 ``hybrid_e2e`` option 和 sfptpd 的 ``hybrid`` network mode 兼容；不支持 unicast negotiation。

  若 timeTransmitter 未响应 :kconfig:option:`CONFIG_PTP_HYBRID_FALLBACK_ATTEMPTS` 次连续 unicast ``Delay_Req`` messages（PTP Port 记录 error（回退到 multicast delay measurement（并保持 multicast 直到选择新 timeTransmitter。回退可用 :kconfig:option:`CONFIG_PTP_NETWORK_MODE_HYBRID_NO_FALLBACK` 禁用（此情况下 port 始终继续发送 unicast ``Delay_Req`` messages。

  Hybrid mode 需 End-to-End delay mechanism（:kconfig:option:`CONFIG_PTP_DELAY_MECHANISM_E2E`）（并在所有 transport protocols（UDP IPv4、UDP IPv6 和 IEEE 802.3）上支持。

Supported Management messages
*****************************

基于 IEEE 1588-2019 section 15.5.2.3 的 Table 59（支持以下 management TLVs：

.. csv-table:: Supported management message's IDs
   :header: Management_ID, Management_ID name, Allowed actions
   :widths: 10,40,25

    0x0000, NULL_PTP_MANAGEMENT, GET SET COMMAND
    0x0001, CLOCK_DESCRIPTION, GET
    0x0002, USER_DESCRIPTION, GET
    0x0003, SAVE_IN_NON_VOLATILE_STORAGE, -
    0x0004, RESET_NON_VOLATILE_STORAGE, -
    0x0005, INITIALIZE, -
    0x0006, FAULT_LOG, -
    0x0007, FAULT_LOG_RESET, -
    0x2000, DEFAULT_DATA_SET, GET
    0x2001, CURRENT_DATA_SET, GET
    0x2002, PARENT_DATA_SET, GET
    0x2003, TIME_PROPERTIES_DATA_SET, GET
    0x2004, PORT_DATA_SET, GET
    0x2005, PRIORITY1, GET SET
    0x2006, PRIORITY2, GET SET
    0x2007, DOMAIN, GET SET
    0x2008, TIME_RECEIVER_ONLY, GET SET
    0x2009, LOG_ANNOUNCE_INTERVAL, GET SET
    0x200A, ANNOUNCE_RECEIPT_TIMEOUT, GET SET
    0x200B, LOG_SYNC_INTERVAL, GET SET
    0x200C, VERSION_NUMBER, GET SET
    0x200D, ENABLE_PORT, COMMAND
    0x200E, DISABLE_PORT, COMMAND
    0x200F, TIME, GET SET
    0x2010, CLOCK_ACCURACY, GET SET
    0x2011, UTC_PROPERTIES, GET SET
    0x2012, TRACEBILITY_PROPERTIES, GET SET
    0x2013, TIMESCALE_PROPERTIES, GET SET
    0x2014, UNICAST_NEGOTIATION_ENABLE, -
    0x2015, PATH_TRACE_LIST, -
    0x2016, PATH_TRACE_ENABLE, -
    0x2017, GRANDMASTER_CLUSTER_TABLE, -
    0x2018, UNICAST_TIME_TRANSMITTER_TABLE, -
    0x2019, UNICAST_TIME_TRANSMITTER_MAX_TABLE_SIZE, -
    0x201A, ACCEPTABLE_TIME_TRANSMITTER_TABLE, -
    0x201B, ACCEPTABLE_TIME_TRANSMITTER_TABLE_ENABLED, -
    0x201C, ACCEPTABLE_TIME_TRANSMITTER_MAX_TABLE_SIZE, -
    0x201D, ALTERNATE_TIME_TRANSMITTER, -
    0x201E, ALTERNATE_TIME_OFFSET_ENABLE, -
    0x201F, ALTERNATE_TIME_OFFSET_NAME, -
    0x2020, ALTERNATE_TIME_OFFSET_MAX_KEY, -
    0x2021, ALTERNATE_TIME_OFFSET_PROPERTIES, -
    0x3000, EXTERNAL_PORT_CONFIGURATION_ENABLED,
    0x3001, TIME_TRANSMITTER_ONLY, -
    0x3002, HOLDOVER_UPGRADE_ENABLE, -
    0x3003, EXT_PORT_CONFIG_PORT_DATA_SET, -
    0x4000, TRANSPARENT_CLOCK_DEFAULT_DATA_SET, -
    0x4001, TRANSPARENT_CLOCK_PORT_DATA_SET, -
    0x4002, PRIMARY_DOMAIN, -
    0x6000, DELAY_MECHANISM, GET
    0x6001, LOG_MIN_PDELAY_REQ_INTERVAL, GET SET

Timestamping notes
******************

当 RX hardware timestamps 不可用或无效时（synchronization 回退到 receive processing 期间读取 PHC time。这可引入额外 jitter（来自 frame 到达与 PHC 读取之间软件处理 latency（packet path 和 scheduling）。

此行为对无真正 driver-provided RX hardware timestamps 的 L2 AF_PACKET paths 预期。

对 IEEE 802.3 transport（Sync 以 two-step mode 发送（Follow_Up 由 TX timestamp callbacks 生成。若 TX timestamp 缺失或延迟（stack 记录 warning（并跳过该 Sync sequence 的 Follow_Up（然后在后续 intervals 继续正常 Sync transmission（best-effort 行为）。

Peer-to-peer delay measurement 可用 :kconfig:option:`CONFIG_PTP_DELAY_MECHANISM_P2P` 选择。第一个支持的 P2P mode 为 two-step ``Pdelay_Req`` / ``Pdelay_Resp`` / ``Pdelay_Resp_Follow_Up``。One-step ``Pdelay_Resp`` samples 被拒绝并记录以留待后续实现。

Supported hardware
******************

虽然 stack 本身为 hardware 无关（但 Ethernet frame timestamping 支持须在 ethernet drivers 中启用。

支持的 boards：

- :zephyr:board:`nucleo_h563zi`
- :zephyr:board:`nucleo_h743zi`
- :zephyr:board:`nucleo_h745zi_q`
- :zephyr:board:`nucleo_f767zi`
- :zephyr:board:`frdm_mcxn947`
- :zephyr:board:`native_sim`（仅可用于简单测试（因无 hardware clock 能力有限）

Enabling the stack
******************

以下 configuration option 须在 :file:`prj.conf` file 中启用。

- :kconfig:option:`CONFIG_PTP`

Testing
*******

Stack 已用 `Linux ptp4l <https://linuxptp.sourceforge.net/>`_ daemons 非正式测试。其也已用 :zephyr:board:`nucleo_h563zi` 和 :zephyr:board:`frdm_mcxn947` board 对 GPS clock 测试（均带直接 Ethernet 连接和带 PTP-capable switch 在中间。所有测试均用 :zephyr:code-sample:`PTP sample application <ptp>`（带 UDP IPv4、UDP IPv6 和 IEEE 802.3 transport。

以下 table 总结非正式 test matrix：

+--------------------------------+-------------+----------+----------+
|                                | IEEE 802.3  | UDP IPv4 | UDP IPv6 |
+================================+=============+==========+==========+
| ptp4l daemons                  | yes         | yes      | yes      |
+--------------------------------+-------------+----------+----------+
| GPS Clock (direct link)        | yes         | yes      | yes      |
+--------------------------------+-------------+----------+----------+
| PTP-capable switch             | yes         | yes      | yes      |
+--------------------------------+-------------+----------+----------+
| GPS Clock + PTP-capable switch | yes         | yes      | yes      |
+--------------------------------+-------------+----------+----------+

Peer-to-peer delay measurement 已实现并针对 ordinary-clock 使用验证。Boundary-clock operation 预期共享相同 port-level Pdelay machinery（但尚未在 multi-port hardware 上验证。

Zephyr source distribution 中的 :zephyr:code-sample:`PTP sample application <ptp>` 可用于测试。

.. _IEEE 1588-2019 standard:
   https://standards.ieee.org/ieee/1588/6825/

API Reference
*************

.. doxygengroup:: ptp
