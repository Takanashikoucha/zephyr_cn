.. _ip_stack_overview:

概述
########

.. contents::
    :local:
    :depth: 2

支持的功能
******************

网络 IP 协议栈是模块化的，并可通过构建时配置选项进行高度配置。你可以通过仅启用应用程序所需的网络功能来最小化系统内存消耗。几乎所有功能都可以在不需要时禁用。

* **IPv6**（:rfc:`8200`）受到支持。各种 IPv6 子选项
  可以根据网络需求启用或禁用。

  * 开发者可以设置同时活动的单播和多播 IPv6 地址的数量。
  * 设备的 IPv6 地址可以静态设置，
  也可以使用 SLAAC（无状态地址自动配置，:rfc:`4862`）动态设置。
  * 系统还支持多个 IPv6 前缀，并且最大
    IPv6 前缀计数可以在构建时配置。
  * 如果不需要，IPv6 邻居缓存可以禁用，并且其大小可以
  在构建时配置。
  * IPv6 邻居发现支持（:rfc:`4861`）默认启用。
  * 多播监听器发现 v2 支持（:rfc:`3810`）默认启用。
  * IPv6 头部压缩（6lo）可用于 IEEE 802.15.4 网络的
  IPv6 连接（:rfc:`4944`）。
  * DHCPv6（IPv6 动态主机配置协议）（:rfc:`8415`）客户端
  功能受到支持。
  * IPv6 隐私扩展（:rfc:`8981`）受到支持。

* **IPv4**（:rfc:`791`）受到支持。它不能用于 IEEE 802.15.4，
  因为该网络技术仅支持 IPv6。IPv4 可以用于例如
  以太网、Wi-Fi 和基于蜂窝的网络。

  * 支持 DHCP（动态主机配置协议）客户端和服务器
  （:rfc:`2131`）。
  * IPv4 地址也可以手动配置。默认支持
  静态 IPv4 地址。
  * 支持 IPv4 NAT（网络地址转换）。数据包可以
  通过执行 SNAT 和 DNAT 在接口之间跳转。连接跟踪
  和 iptable 规则用于过滤和跨子网转发数据包。

* **双栈支持。** 网络协议栈允许开发者配置
  系统同时使用 IPv6 和 IPv4。

* **UDP** 用户数据报协议（:rfc:`768`）受到支持。
  开发者可以发送 UDP 数据报（客户端支持）或创建
  监听器以接收发往特定端口的 UDP 数据包（服务器
  支持）。

* **TCP** 传输控制协议（:rfc:`793`）受到支持。应用程序中可以使用服务器
  和客户端两种角色。可供应用程序使用的 TCP 套接字数量
  可以在构建时配置。
  支持对接收数据的选择性确认（:rfc:`2018`）
  （:kconfig:option:`CONFIG_NET_TCP_SACK`）。

* **BSD 套接字 API** 实现了
  :ref:`BSD 套接字兼容 API <bsd_sockets_interface>` 的一个子集的支持。
  同时支持阻塞和非阻塞数据报（UDP）和流（TCP）
  套接字。也支持数据包套接字（``AF_PACKET``）。

* **安全套接字 API** 实验性支持 TLS/DTLS 安全协议和
  套接字 API 的配置选项。实现的安全函数
  由 Mbed TLS 库提供。

* **MQTT** 消息队列遥测传输（ISO/IEC PRF 20922）版本 3.1.1 和 5.0
  受到支持。
  提供了针对 MQTT v3.1.1 和 v5.0 的示例 :zephyr:code-sample:`mqtt-publisher` 客户端应用程序。

* **MQTT-SN** 支持传感器网络 MQTT 版本 1.2。
  提供了示例 :zephyr:code-sample:`mqtt-sn-publisher` 客户端应用程序。

* **CoAP** 受限应用协议（:rfc:`7252`）受到支持。
  同时提供了 :zephyr:code-sample:`coap-client` 和 :zephyr:code-sample:`coap-server` 示例
  应用程序。

* **LwM2M** OMA 轻量级机器对机器协议
  （`LwM2M 规范 1.0.2`_）通过 "Bootstrap"、"Client
  Registration"、"Device Management & Service Enablement" 和 "Information
  Reporting" 接口受到支持。所需的 LwM2M 核心对象已实现，
  以及若干 IPSO 智能对象。启用 Kconfig 选项后，
  （`LwM2M 规范 1.1.1`_）以类似方式受到支持。
  :zephyr:code-sample:`lwm2m-client` 示例将该库作为示例实现。

* **HTTP** 支持超文本传输协议客户端和服务器。
  :ref:`http_client_interface` 库支持 HTTP/1.1（:rfc:`2616`）。
  :ref:`http_server_interface` 库支持 HTTP/1.1（:rfc:`2616`）和
  HTTP/2（:rfc:`9113`）。
  提供了 :zephyr:code-sample:`sockets-http-client` 和
  :zephyr:code-sample:`sockets-http-server` 示例。

* **Websocket**（:rfc:`6455`）客户端受到支持。
  提供了 :zephyr:code-sample:`sockets-websocket-client` 示例。

* **DNS** 域名服务（:rfc:`1035`）客户端功能受到支持。
  应用程序可以使用 DNS API 从 DNS 服务器查询域名信息或 IP
  地址。可以查询 IPv4（A）和 IPv6（AAAA）记录。
  同时支持多播 DNS（mDNS）（:rfc:`6762`）和链路本地多播名称解析
  （LLMNR，:rfc:`4795`）。
  还支持 DNS 服务发现（:rfc:`6763`）。

* **网络管理 API。** 应用程序可以使用网络管理 API
  监听由核心网络协议栈生成的管理事件，例如当 IP 地址
  被添加到设备或网络接口启动时。

* **Wi-Fi 管理 API。** 应用程序可以使用 Wi-Fi 管理 API
  管理接口，例如连接 Wi-Fi 网络和扫描
  可用的 Wi-Fi 网络。

* **Wi-Fi 网络管理器 API。** Wi-Fi 网络管理器现在可以
  向 Wi-Fi 协议栈注册自己。然后网络管理器可以
  实现 Wi-Fi 管理 API 并管理 Wi-Fi 接口。

* **多种网络技术。** Zephyr 操作系统可以配置为
  仅通过在 Kconfig 中启用即可同时支持多种网络技术：例如以太网、Wi-Fi 和 802.15.4 支持。注意
  这些技术之间不提供自动 IP 路由功能。应用程序可以根据其需求向所需的
  网络接口发送数据。

* **最小拷贝网络缓冲区管理。** 可以实现最小
  拷贝网络数据路径。这意味着系统在数据
  发送到网络时尝试避免拷贝
  应用程序数据。

* **虚拟局域网支持。** 虚拟局域网（VLAN）允许将物理
  以太网网络划分为逻辑网络。
  有关更多细节，请参阅 :ref:`VLAN 支持 <vlan_interface>`。

* **网络流量分类。** 发送和接收的网络数据包可以
  根据应用程序需求进行优先级划分。
  有关更多细节，请参阅 :ref:`流量分类 <traffic-class-support>`。

* **时间敏感网络。** 同时支持 gPTP（通用精密时间协议）
  和 PTP（精密时间协议，IEEE 1588）。
  有关更多细节，请参阅 :ref:`gPTP 支持 <gptp_interface>` 和 :ref:`PTP 支持 <ptp_interface>`。

* **SNTP** 简单网络时间协议（:rfc:`5905`）客户端受到支持。
  提供了 :zephyr:code-sample:`sntp-client` 示例。

* **SOCKS5** 支持代理版本 5（:rfc:`1928`）。

* **TFTP** 简单文件传输协议（:rfc:`1350`）客户端受到支持。
  提供了 :zephyr:code-sample:`tftp-client` 示例。

* **MIDI2** 支持 MIDI 2.0 网络 UDP 传输。
  提供了 :zephyr:code-sample:`netmidi2` 示例。

* **OCPP** 支持开放充电点协议。
  提供了 :zephyr:code-sample:`ocpp` 示例。

* **Prometheus** 支持指标服务器功能。
  提供了 :zephyr:code-sample:`prometheus`。

* **网络 shell。** 网络 shell 提供了用于确定
  网络状态、启用/禁用功能以及发出 ping
  或 DNS 解析等命令的辅助工具。net-shell 在开发网络软件时很有用。
  有关更多细节，请参阅 :ref:`网络 shell <net_shell>`。

* **zperf** 是 iPerf v2 网络性能和带宽测量工具。
  同时支持客户端和服务器功能。提供了 :zephyr:code-sample:`zperf`
  示例。

此外，Zephyr 操作系统支持以下网络技术（链路层）：

* IEEE 802.15.4
* Bluetooth
* Ethernet, IEEE 802.3
* Wi-Fi, IEEE 802.11
* Cellular / PPP（:rfc:`1661`）
* Thread（提供了 :zephyr:code-sample-category:`openthread` 示例）
* 用于 SocketCAN 的 CAN 总线
* SLIP（串行线路上的 IP）。用于与 QEMU 进行测试。它向
  主机系统（如 Linux）提供以太网接口，测试应用程序
  可以在 Linux 主机中运行并向 Zephyr 操作系统设备发送网络数据。

源码树布局
******************

网络协议栈源代码树组织如下：

:zephyr_file:`subsys/net/`
  各种可选网络协议栈组件如连接管理器、
  数据包过滤代码和主机名处理位于此处。

:zephyr_file:`subsys/net/ip/`
  这是核心网络协议栈代码所在的位置。

:zephyr_file:`subsys/net/l2`
  这是 IP 协议栈第 2 层代码所在的位置。这包括
  以太网、IEEE 802.15.4 和 Wi-Fi 的通用
  支持。

:zephyr_file:`subsys/net/lib/`
  应用层协议（DNS、MQTT 等）和附加协议栈
  组件（BSD 套接字等）。

:zephyr_file:`include/zephyr/net/`
  公共 API 头文件。这些是应用程序需要
  包含以使用 IP 网络功能的头文件。

:zephyr_file:`samples/net/`
  示例网络代码。这是入门
  网络应用程序开发的好参考。

:zephyr_file:`tests/net/`
  测试应用程序。这些应用程序用于验证
  IP 协议栈的功能，但不是示例代码的最佳
  来源（请参见 :zephyr_file:`samples/net/`）。

.. _LwM2M 规范 1.0.2:
   https://www.openmobilealliance.org/release/LightweightM2M/V1_0_2-20180209-A/OMA-TS-LightweightM2M-V1_0_2-20180209-A.pdf

.. _LwM2M 规范 1.1.1:
   https://www.openmobilealliance.org/release/LightweightM2M/V1_1_1-20190617-A/
