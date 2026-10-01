.. _network_stack_architecture:

Network Stack Architecture
##########################

.. toctree::
   :maxdepth: 1
   :hidden:

   net_pkt_processing_stats.rst

Zephyr network stack 为专为 Zephyr OS 设计的 native network stack。其由 layers 组成（每个 layer 旨在向其他 layers 提供某些 services。Network stack functionality 通过 Kconfig options 高度可配置。

.. contents::
    :local:
    :depth: 2

High level overview of the network stack
****************************************

.. figure:: zephyr_netstack_overview.svg
    :alt: Overview of the network stack architecture
    :figclass: align-center

    Network stack overview

Network stack 分层（由以下 parts 组成：

* **Network Application。**Network application 可用提供的 application-level protocol libraries（或直接访问 :ref:`BSD socket API <bsd_sockets_interface>` 创建 network connection（发送或接收 data（并关闭 connection。Application 还可用 :ref:`network management API <net_mgmt_interface>` 配置 network（并设置相关 parameters（如 network link options（启动 scan（若适用）（监听 network configuration events 等。:ref:`network interface API <net_if_interface>` 可用于为 network interface 设置 IP address（将 network interface down 等。

* **Network Protocols。**这为各种 protocols 提供 implementations（如

  * CoAP、LwM2M 和 MQTT 等 application-level network protocols。
    关于它们的信息参见 :ref:`application protocols chapter <net_protocols>`。
  * IPv6、IPv4、UDP、TCP、ICMPv4 和 ICMPv6 等 core network protocols。
    通过 :ref:`BSD socket API <bsd_sockets_interface>` 访问这些 protocols。

* **Network Interface Abstraction。**这提供所有 network interfaces 共有的 functionality（如将 network interface down 等。系统中可有多个 network interfaces。更多细节参见 :ref:`network interface overview <net_if_interface>`。

* **L2 Network Technologies。**这为向实际 network device 发送和接收 data 提供通用 API。
  更多细节参见 :ref:`L2 overview <net_l2_interface>`。

  这些 network technologies 包括 :ref:`Ethernet <ethernet_interface>`、
  :ref:`IEEE 802.15.4 <ieee802154_interface>`、
  :ref:`Bluetooth <bluetooth_api>`、:ref:`CANBUS <can_api>` 等。

  其中某些 technologies 支持 IPv6 header compression (6Lo)（
  细节参见 :rfc:`6282`。
  例如 IPv4 的 ARP（:rfc:`826`）由
  :ref:`Ethernet component <ethernet_interface>` 完成。

* **Network Device Drivers。**实际 low-level device drivers 处理 network packets 的物理发送或接收。

Network data flow
*****************

Application 通常由一个或多个 :ref:`threads <threads_v2>` 组成（其执行 application 逻辑。使用 :ref:`BSD socket API <bsd_sockets_interface>` 时（将发生以下事情。

.. figure:: zephyr_netstack_overview-rx_sequence.svg
    :alt: Network RX data flow
    :figclass: align-center

    Network RX data flow

Data receiving (RX)
-------------------

1. Network data packet 由 device driver 接收。

2. Device driver 分配足够 network buffers 以存储收到的
   data。Network packet 放入正确 RX queue（由
   :ref:`k_fifo <fifos_v2>` 实现。默认系统中仅有一个 receive queue（但最多可有 8 个 receive queues。
   这些 queues 将以不同 priority 处理 incoming packets。
   更多细节参见 :ref:`traffic-class-support`。Receive queues 还
   作为分离 data processing pipeline (bottom-half) 的方式
   （device driver 在 interrupt context 中运行（且其须尽可能快完成
   processing。

3. Network packet 然后传递给正确 L2 driver。L2 driver
   可检查 packet 是否恰当（并在需要时修改其（例如剥离 L2
   header 和 frame check sequence 等。

4. Packet 由 network interface 处理。若由 :kconfig:option:`CONFIG_NET_STATISTICS` 启用（则收集
   network statistics。

5. Packet 然后传递给 L3 processing。若 packet 基于 IP（
   则 L3 layer 检查 packet 是否为恰当的 IPv6 或 IPv4 packet。

6. Socket handler 然后找到 network packet 所属的活动 socket（并将其放入该 socket 的 queue（以分离
   networking code 和 application。通常 application 在
   userspace context 中运行（且 network stack 在 kernel context 中运行。

7. Application 然后接收 data（并可按需处理。
   Application 应已使用
   :ref:`BSD socket API <bsd_sockets_interface>` 创建接收
   data 的 socket。


.. figure:: zephyr_netstack_overview-tx_sequence.svg
    :alt: Network TX data flow
    :figclass: align-center

    Network TX data flow

Data sending (TX)
-----------------

1. 发送 data 时 application 应使用
   :ref:`BSD socket API <bsd_sockets_interface>`。

2. Application data 被准备发送到 kernel space（然后
   复制到内部 net_buf structures。

3. 根据 socket 类型（在 data 前添加 protocol header。例如（若 socket 为 UDP socket（则构建 UDP header
   并将其放在 data 前。

4. 为 UDP 或 TCP packet 的 network packet 添加 IP header。

5. Network stack 将检查 network interface 是否为 network packet 正确设置（且还将确保在 data 被 queue 待发送前 network interface
   已启用。

6. Network packet 然后被分类并放入正确 transmit
   queue（由 :ref:`k_fifo <fifos_v2>` 实现。默认系统中仅有一个 transmit queue（但最多可有 8
   个 transmit queues。这些 queues 将以不同 priority 处理发送的 packets。更多细节参见 :ref:`traffic-class-support`。
   Transmit packet 分类后（packet 由正确 L2 layer module 检查。L2 module 将对
   data 执行额外检查（且还将为 network packet 创建任何 L2 headers。
   若一切 ok（data 交给 network device driver 发送。

7. Device driver 将 packet 发送到 network。

注意在 TX 和 RX data paths 中（queues
（:ref:`k_fifo's <fifos_v2>`）形成 data 从一个 :ref:`thread <threads_v2>` 传递给另一个的分离点。
这些 :ref:`threads <threads_v2>` 可能在不同 contexts
（:ref:`kernel <kernel_api>` 与 :ref:`userspace <usermode_api>`）中运行（且具不同
:ref:`priorities <scheduling_v2>`。


Network packet processing statistics
************************************

Network processing statistics 信息
参见 :ref:`here <net_pkt_processing_stats>`。
