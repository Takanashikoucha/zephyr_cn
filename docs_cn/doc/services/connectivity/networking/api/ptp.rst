.. _ptp_interface:

Precision Time Protocol (PTP)
#############################

.. contents::
    :local:
    :depth: 2

概述
********

PTP 是实现在应用层的网络协议，用于同步计算机网络中的时钟。其精度可达微秒以下。
该协议栈支持 `IEEE 1588-2019 标准`_（面向网络测量与控制系统的精密时钟同步协议 IEEE 标准）中定义的协议和流程。
它有多种配置（profile），可以实现在 L2（以太网）或 L3（UDP/IPv4 或 UDP/IPv6）之上。
其精度通过使用协议数据包的硬件时间戳来实现。

Zephyr 的 PTP 协议栈实现包含以下内容：

* 处理传入消息和事件的 PTP 协议栈线程
* 与 ptp_clock 驱动的集成
* 在系统初始化期间执行的 PTP 协议栈初始化

该实现会自动创建 PTP 端口（每个 PTP 端口对应一个唯一的接口）。

支持的特性
******************

协议栈实现并不支持标准中规定的全部特性。
下表列出了所有支持的特性。

.. csv-table:: 支持的特性
   :header: 特性, 是否支持
   :widths: 50,10

   普通时钟（Ordinary Clock）, 支持
   边界时钟（Boundary Clock）, 支持
   透明时钟（Transparent Clock）,
   管理节点（Management Node）,
   端到端（End to end）延迟机制, 支持
   对等（Peer to peer）延迟机制, 支持（两步式）
   多播（Multicast）工作模式, 支持
   混合（Hybrid）工作模式, 支持
   单播（Unicast）工作模式,
   非易失性存储,
   UDP IPv4 传输协议, 支持
   UDP IPv6 传输协议, 支持
   IEEE 802.3（以太网）传输协议, 支持
   硬件时间戳, 支持
   软件时间戳,
   TIME_RECEIVER_ONLY PTP 实例, 支持
   TIME_TRANSMITTER_ONLY PTP 实例,

网络传输模式
**************************

网络传输模式通过 ``PTP_NETWORK_MODE``
Kconfig 选择项来选定：

* 多播模式（:kconfig:option:`CONFIG_PTP_NETWORK_MODE_MULTICAST`，
  默认值）是标准 PTP 模式，所有 PTP 消息都发送到默认的多播地址。其含义是
  每个节点都会收到所有其他节点的 ``Delay_Req`` 和 ``Delay_Resp`` 消息对，从而
  增加了网络上的流量。在仅部署少量 timeReceiver 的小型网络上，这通常
  不是问题。

* 混合模式（:kconfig:option:`CONFIG_PTP_NETWORK_MODE_HYBRID`）仍然将
  ``Announce``、``Sync`` 和 ``Follow_Up`` 消息发送到默认的多播
  地址，但 timeReceiver 将其 ``Delay_Req`` 消息以单播方式
  直接发送到当前 timeTransmitter 的协议地址（IP 地址，或
  IEEE 802.3 传输的 MAC 地址），后者再以单播 ``Delay_Resp``
  响应发起请求的 timeReceiver。这减少了网络上 PTP 流量的
  水平，在扩展到部署大量 timeReceiver 的更大网络时，这可能是一个
  因素。混合模式仅要求网络支持从 timeTransmitter 到
  timeReceiver 的多播传输。该模式与 linuxptp 的 ``hybrid_e2e`` 选项
  以及 sfptpd 的 ``hybrid`` 网络模式兼容；不支持单播协商。

  如果 timeTransmitter 未能应答
  :kconfig:option:`CONFIG_PTP_HYBRID_FALLBACK_ATTEMPTS` 次连续的单播
  ``Delay_Req`` 消息，PTP 端口会记录一条错误，回退到多播
  延迟测量，并保持多播状态直到选出新的 timeTransmitter。
  该回退可以通过
  :kconfig:option:`CONFIG_PTP_NETWORK_MODE_HYBRID_NO_FALLBACK` 禁用，此时
  端口将始终继续发送单播 ``Delay_Req`` 消息。

  混合模式需要端到端延迟机制
  （:kconfig:option:`CONFIG_PTP_DELAY_MECHANISM_E2E`），并支持所有
  传输协议（UDP IPv4、UDP IPv6 和 IEEE 802.3）。

支持的管理消息
*****************************

基于 IEEE 1588-2019 第 15.5.2.3 节的表 59，支持以下管理 TLV：

.. csv-table:: 支持的管理消息 ID
   :header: Management_ID, Management_ID 名称, 允许的操作
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

时间戳说明
******************

当 RX 硬件时间戳不可用或无效时，同步会
回退为在接收处理期间读取 PHC 时间。这可能会
在帧到达与 PHC 读取之间引入额外的抖动（来自软件处理延迟（数据包路径和调度））。

对于没有真正由驱动提供的
RX 硬件时间戳的 L2 AF_PACKET 路径，这是预期行为。

对于 IEEE 802.3 传输，Sync 以两步模式发送，Follow_Up
由 TX 时间戳回调生成。如果 TX 时间戳缺失或延迟，
协议栈会记录一条警告，并跳过该 Sync 序列的 Follow_Up，然后
在后续间隔继续正常的 Sync 传输（尽力而为
行为）。

对等（Peer-to-peer）延迟测量可以通过
:kconfig:option:`CONFIG_PTP_DELAY_MECHANISM_P2P` 选定。第一个支持的 P2P 模式
是两步式 ``Pdelay_Req`` / ``Pdelay_Resp`` /
``Pdelay_Resp_Follow_Up``。一步式 ``Pdelay_Resp`` 采样会被拒绝并
记录日志，留待后续实现。

支持的硬件
******************

尽管协议栈本身与硬件无关，但以太网帧时间戳
支持必须在以太网驱动中启用。

支持的板卡：

- :zephyr:board:`nucleo_h563zi`
- :zephyr:board:`nucleo_h743zi`
- :zephyr:board:`nucleo_h745zi_q`
- :zephyr:board:`nucleo_f767zi`
- :zephyr:board:`frdm_mcxn947`
- :zephyr:board:`native_sim`（仅可用于简单测试，由于缺乏硬件时钟
  而能力有限）

启用协议栈
******************

以下配置选项必须在 :file:`prj.conf` 文件中启用。

- :kconfig:option:`CONFIG_PTP`

测试
*******

该协议栈曾使用
`Linux ptp4l <https://linuxptp.sourceforge.net/>`_ 守护进程进行过非正式测试。它还在
:zephyr:board:`nucleo_h563zi` 和 :zephyr:board:`frdm_mcxn947` 板卡上
对照 GPS 时钟进行了测试，两者都分别采用了直接以太网连接和
中间接入支持 PTP 的交换机。所有测试均使用
:zephyr:code-sample:`PTP 示例应用 <ptp>` 执行，采用 UDP IPv4、UDP IPv6 以及
IEEE 802.3 传输。

下表总结了非正式测试矩阵：

+--------------------------------+-------------+----------+----------+
|                                | IEEE 802.3  | UDP IPv4 | UDP IPv6 |
+================================+=============+==========+==========+
| ptp4l 守护进程                  | 支持         | 支持      | 支持      |
+--------------------------------+-------------+----------+----------+
| GPS 时钟（直连）        | 支持         | 支持      | 支持      |
+--------------------------------+-------------+----------+----------+
| 支持 PTP 的交换机             | 支持         | 支持      | 支持      |
+--------------------------------+-------------+----------+----------+
| GPS 时钟 + 支持 PTP 的交换机 | 支持         | 支持      | 支持      |
+--------------------------------+-------------+----------+----------+

对等（Peer-to-peer）延迟测量已为普通时钟
用途实现并验证。边界时钟（Boundary-clock）运行预计
共享相同的端口级 Pdelay 机制，但尚未在多端口硬件上
验证。

Zephyr 源码发行版中的 :zephyr:code-sample:`PTP 示例应用 <ptp>`
可用于测试。

.. _IEEE 1588-2019 标准:
   https://standards.ieee.org/ieee/1588/6825/

API 参考
*************

.. doxygengroup:: ptp
