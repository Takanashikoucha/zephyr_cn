.. _network_stack_architecture:

网络协议栈架构
##########################

.. toctree::
   :maxdepth: 1
   :hidden:

   net_pkt_processing_stats.rst

Zephyr 网络协议栈是一个专为 Zephyr 操作系统设计的原生网络协议栈。它由若干层组成，每一层旨在为其他层提供特定的服务。网络协议栈的功能可以通过 Kconfig 选项进行高度配置。

.. contents::
    :local:
    :depth: 2

网络协议栈的高层概述
****************************************

.. figure:: zephyr_netstack_overview.svg
    :alt: 网络协议栈架构概述
    :figclass: align-center

    网络协议栈概述

网络协议栈是分层的，由以下部分组成：

* **网络应用程序。** 网络应用程序既可以使用所提供的应用层协议库，也可以直接访问 :ref:`BSD 套接字 API <bsd_sockets_interface>` 来创建网络连接、发送或接收数据、关闭连接。应用程序还可以使用 :ref:`网络管理 API <net_mgmt_interface>` 来配置网络并设置相关参数，例如网络链路选项、启动扫描（如适用）、监听网络配置事件等。:ref:`网络接口 API <net_if_interface>` 可用于为网络接口设置 IP 地址、将网络接口置为 down 状态等。

* **网络协议。** 这为各种协议提供实现，例如

  * 应用层网络协议，如 CoAP、LwM2M 和 MQTT。
    有关它们的信息，请参阅 :ref:`应用协议章节 <net_protocols>`。
  * 核心网络协议，如 IPv6、IPv4、UDP、TCP、ICMPv4 和 ICMPv6。
    你通过 :ref:`BSD 套接字 API <bsd_sockets_interface>` 访问这些协议。

* **网络接口抽象。** 这提供所有网络接口共有的功能，例如将网络接口置为 down 状态等。系统中可以有多个网络接口。有关更多细节，请参阅 :ref:`网络接口概述 <net_if_interface>`。

* **L2 网络技术。** 这为向实际网络设备发送和接收数据提供通用 API。
  有关更多细节，请参阅 :ref:`L2 概述 <net_l2_interface>`。

  这些网络技术包括 :ref:`以太网 <ethernet_interface>`、
  :ref:`IEEE 802.15.4 <ieee802154_interface>`、
  :ref:`蓝牙 <bluetooth_api>`、:ref:`CAN 总线 <can_api>` 等。

  其中一些技术支持 IPv6 头部压缩（6Lo），
  详情请参见 :rfc:`6282`。
  例如，IPv4 的 ARP（:rfc:`826`）由
  :ref:`以太网组件 <ethernet_interface>` 完成。

* **网络设备驱动程序。** 实际的底层设备驱动程序负责网络数据包的物理发送或接收。

网络数据流
*****************

应用程序通常由一个或多个 :ref:`线程 <threads_v2>` 组成，这些线程执行应用程序逻辑。使用
:ref:`BSD 套接字 API <bsd_sockets_interface>` 时，将发生以下事情。

.. figure:: zephyr_netstack_overview-rx_sequence.svg
    :alt: 网络 RX 数据流
    :figclass: align-center

    网络 RX 数据流

数据接收（RX）
-------------------

1. 网络设备驱动程序接收一个网络数据包。

2. 设备驱动程序分配足够的网络缓冲区来存储接收到的
   数据。网络数据包被放入正确的 RX 队列（由
   :ref:`k_fifo <fifos_v2>` 实现）。默认情况下系统中只有一个接收队列，
   但最多可以有 8 个接收队列。
   这些队列将以不同的优先级处理传入的数据包。
   有关更多细节，请参阅 :ref:`traffic-class-support`。接收队列还
   起到分离数据处理流水线（bottom-half）的作用，
   因为设备驱动程序运行在中断上下文中，必须尽可能快地完成其
   处理。

3. 然后网络数据包被传递给正确的 L2 驱动程序。L2 驱动程序
   可以检查数据包是否合法，并在需要时对其进行修改，例如剥离 L2
   头部和帧校验序列（frame check sequence）等。

4. 数据包由网络接口处理。如果启用了 :kconfig:option:`CONFIG_NET_STATISTICS`，
   则收集网络统计信息。

5. 然后数据包被传递给 L3 处理。如果数据包基于 IP，
   则 L3 层检查该数据包是否是合法的 IPv6 或 IPv4 数据包。

6. 套接字句柄随后找到该网络数据包所属的活动套接字，
   并将其放入该套接字的队列中，以便将
   网络代码与应用程序隔离。通常应用程序运行在
   用户空间上下文中，而网络协议栈运行在内核上下文中。

7. 然后应用程序接收数据，并按需对其进行处理。
   应用程序应已使用
   :ref:`BSD 套接字 API <bsd_sockets_interface>` 创建一个
   将接收数据的套接字。


.. figure:: zephyr_netstack_overview-tx_sequence.svg
    :alt: 网络 TX 数据流
    :figclass: align-center

    网络 TX 数据流

数据发送（TX）
-----------------

1. 应用程序在发送数据时应使用
   :ref:`BSD 套接字 API <bsd_sockets_interface>`。

2. 应用程序数据被准备发送到内核空间，然后
   复制到内部 net_buf 结构中。

3. 根据套接字类型，在数据前面添加一个协议头部。例如，如果套接字是 UDP 套接字，则构造一个 UDP 头部
   并将其放在数据前面。

4. 为 UDP 或 TCP 数据包的网络数据包添加 IP 头部。

5. 网络协议栈检查网络接口是否已针对该网络数据包正确设置，
   并且还会确保在数据入队待发送之前网络接口
   已启用。

6. 然后网络数据包被分类并放入正确的发送
   队列（由 :ref:`k_fifo <fifos_v2>` 实现）。默认情况下系统中只有一个
   发送队列，但最多可以有 8 个
   发送队列。这些队列将以不同的优先级处理
   发送的数据包。有关更多细节，请参阅 :ref:`traffic-class-support`。
   在发送数据包分类之后，数据包由
   正确的 L2 层模块检查。L2 模块将
   对数据进行额外检查，还会为网络数据包创建任何 L2 头部。
   如果一切正常，数据被交给网络设备驱动程序
   发送出去。

7. 设备驱动程序将数据包发送到网络。

注意：在 TX 和 RX 两条数据路径中，队列
（:ref:`k_fifo <fifos_v2>`）构成了分离点，数据在此从一个
:ref:`线程 <threads_v2>` 传递到另一个线程。
这些 :ref:`线程 <threads_v2>` 可能运行在不同的上下文中
（:ref:`内核 <kernel_api>` 与 :ref:`用户空间 <usermode_api>`），并具有不同的
:ref:`优先级 <scheduling_v2>`。


网络数据包处理统计
************************************

有关网络处理统计的信息
请参阅 :ref:`此处 <net_pkt_processing_stats>`。
