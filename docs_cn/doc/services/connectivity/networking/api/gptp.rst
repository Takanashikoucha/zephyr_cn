.. _gptp_interface:

通用精密时间协议（gPTP）
######################################

.. contents::
    :local:
    :depth: 2

概述
****

该 gPTP 协议栈支持 `IEEE 802.1AS-2011 标准`_ 中定义的协议和流程
（桥接局域网中时间敏感应用的定时与同步）。

支持的功能
*************

该协议栈处理 `IEEE 802.1AS-2011 标准`_ 中定义的通信和状态机。支持标准附录 A 中定义的全双工点对点链路端点的强制性要求。

原则上，该协议栈能够处理多个网络接口（在标准中也定义为"端口"）上的通信，从而充当 802.1AS 桥。但是，这种工作模式尚未在 Zephyr 操作系统上得到验证。

该协议栈还可以作为静态配置的时间接收器，运行在遵循 IEEE 802.1AS 汽车配置文件的网络上（该网络不交换 Announce 报文）。有关详细信息，请参阅下文中的 `静态 timeReceiver 运行`_。

支持的硬件
**********

虽然协议栈本身与硬件无关，但必须在以太网驱动程序中启用以太网帧时间戳支持。

支持的板卡：

- :zephyr:board:`frdm_k64f`
- :zephyr:board:`nucleo_h743zi`
- :zephyr:board:`nucleo_h745zi_q`
- :zephyr:board:`nucleo_f767zi`
- :zephyr:board:`sam_e70_xplained`
- :zephyr:board:`native_sim`（仅可用于简单测试，由于缺少硬件时钟，能力有限）
- :zephyr:board:`qemu_x86`（模拟实现，由于缺少硬件时钟，能力有限）

启用协议栈
**********

以下配置选项必须在 :file:`prj.conf` 文件中启用。

- :kconfig:option:`CONFIG_NET_GPTP`

静态 timeReceiver 运行
*****************************

按照 IEEE 802.1AS 汽车配置文件（AVnu《Automotive Ethernet AVB 功能与互操作性规范》）构建的网络使用静态端口角色，而不是最佳主时钟算法（BMCA）。此类网络上的桥会发送 Sync 和 Follow_Up 报文，但不发送 Announce 报文，并且不要求其 timeTransmitter 端口响应 Pdelay 请求。默认协议栈无法与这样的桥同步：如果没有收到 Announce 报文，端口永远不会进入时间接收器（"从设备"）角色。

启用 :kconfig:option:`CONFIG_NET_GPTP_STATIC_TIME_RECEIVER` 会将节点配置为静态配置的时间接收器：BMCA 和所有 Announce 处理都被旁路，每个端口都被固定为时间接收器角色，asCapable 被强制置位，使同步不依赖于 Pdelay 测量，本地时钟仅从收到的 Sync 和 Follow_Up 报文进行驯服。该节点永远不会成为主时钟（grandmaster），也永远不会发送 Sync 或 Announce 报文，即使设置了 :kconfig:option:`CONFIG_NET_GPTP_GM_CAPABLE` 也是如此。这对应于 linuxptp ptp4l 的汽车时间接收器配置（BMCA "noop"、clientOnly、inhibit_announce、asCapable "true"、ignore_source_id）。以这种方式禁用 BMCA 的标准对应项是 IEEE 802.1AS-2020 的外部端口配置（第 10.3.14 节，源自 IEEE 1588-2019 第 17.6.2 节）。

应用程序接口
**********************

标准第 9 节中定义了以下应用程序接口：

- ``ClockSourceTime`` 接口（:c:func:`gptp_clk_src_time_invoke`）
- ``ClockTargetPhaseDiscontinuity`` 接口（:c:func:`gptp_register_phase_dis_cb`）
- ``ClockTargetEventCapture`` 接口（:c:func:`gptp_event_capture`）

测试
******

该协议栈曾使用 `OpenAVnu gPTP <https://github.com/AVnu/gptp>`_ 和 `Linux ptp4l <https://linuxptp.sourceforge.net/>`_ 守护进程进行过非正式测试。
Zephyr 源代码发行版中的 :zephyr:code-sample:`gPTP 示例应用程序 <gptp>` 可用于测试。

.. _IEEE 802.1AS-2011 standard:
   https://standards.ieee.org/findstds/standard/802.1AS-2011.html

API 参考
*********

.. doxygengroup:: gptp
