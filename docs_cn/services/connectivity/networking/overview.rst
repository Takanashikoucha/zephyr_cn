.. _ip_stack_overview:

Overview
########

.. contents::
    :local:
    :depth: 2

Supported Features
******************

Networking IP stack 模块化（且通过 build-time
configuration options 高度可配置。可仅启用 application 所需的 network features 以最小化 system memory 消耗。几乎所有 features
在不需要时可禁用。

* **IPv6**（:rfc:`8200`）受支持。各种 IPv6 sub-options
  可根据 networking 需要启用或禁用。

  * Developer 可设置同时活动的 unicast 和 multicast IPv6 addresses 数量。
  * Device 的 IPv6 address 可静态设置（或
    用 SLAAC (Stateless Address Auto Configuration（:rfc:`4862`）动态设置。
  * System 还支持多个 IPv6 prefixes（且最大
    IPv6 prefix count 可在 build time 配置。
  * IPv6 neighbor cache 在不需要时可禁用（且其 size 可
    在 build time 配置。
  * IPv6 neighbor discovery 支持（:rfc:`4861`）默认启用。
  * Multicast Listener Discovery v2 支持（:rfc:`3810`）默认启用。
  * IPv6 header compression (6lo) 可用于 IEEE 802.15.4 networks 的
    IPv6 connectivity（:rfc:`4944`）。
  * DHCPv6 (Dynamic Host Configuration Protocol for IPv6)（:rfc:`8415`）client
    functionality 受支持。
  * IPv6 privacy extension（:rfc:`8981`）受支持。

* **IPv4**（:rfc:`791`）受支持。IEEE 802.15.4 不可用
  此（因为此 network technology 仅支持 IPv6。IPv4 可例如
  用于 Ethernet、Wi-Fi 和 Cellular based networks。

  * DHCP (Dynamic Host Configuration Protocol) client 和 server 受支持
    （:rfc:`2131`）。
  * IPv4 address 也可手动配置。默认支持静态 IPv4 addresses。
  * IPv4 NAT (Network Address Translation) 受支持。Packets 可
    通过执行 SNAT 和 DNAT 在 interfaces 之间 hop。Connection tracking
    和 iptable rules 用于过滤并跨 subnets 转发 packets。

* **Dual stack support。**Networking stack 允许 developer 配置
  system 同时使用 IPv6 和 IPv4。

* **UDP** User Datagram Protocol（:rfc:`768`）受支持。
  Developer 可发送 UDP datagrams（client side support）（或创建
  listener 接收发往特定 port 的 UDP packets（server side
  support）。

* **TCP** Transmission Control Protocol（:rfc:`793`）受支持。Application 中可用 server
  和 client 两种 roles。Application 可用的 TCP sockets
  数量可在 build time 配置。
  对收到的 data 支持 Selective acknowledgment（:rfc:`2018`）
  （:kconfig:option:`CONFIG_NET_TCP_SACK`）。

* **BSD Sockets API** 实现了
  :ref:`BSD sockets compatible API <bsd_sockets_interface>` 子集的支持。
  支持 blocking 和 non-blocking 的 datagram (UDP) 和 stream (TCP)
  sockets。还支持 Packet sockets（``AF_PACKET``）。

* **Secure Sockets API** 对 sockets API 的 TLS/DTLS secure protocols 和
  configuration options 提供 experimental support。实现的 Secure functions
  由 Mbed TLS library 提供。

* **MQTT** Message Queue Telemetry Transport (ISO/IEC PRF 20922) 3.1.1 和 5.0 版本
  受支持。
  为 MQTT v3.1.1 和 v5.0 提供 :zephyr:code-sample:`mqtt-publisher` client application 示例。

* **MQTT-SN** MQTT for Sensor Networks 1.2 版本受支持。
  提供 :zephyr:code-sample:`mqtt-sn-publisher` client application 示例。

* **CoAP** Constrained Application Protocol（:rfc:`7252`）受支持。
  提供 :zephyr:code-sample:`coap-client` 和 :zephyr:code-sample:`coap-server` sample
  applications。

* **LwM2M** OMA Lightweight Machine-to-Machine Protocol
  （`LwM2M specification 1.0.2`_）通过 "Bootstrap"、"Client
  Registration"、"Device Management & Service Enablement" 和 "Information
  Reporting" interfaces 受支持。所需 core LwM2M objects 已实现
  （以及若干 IPSO Smart Objects。（`LwM2M specification 1.1.1`_）
  用 Kconfig option 启用时以类似方式支持。
  :zephyr:code-sample:`lwm2m-client` sample 作为示例实现 library。

* **HTTP** Hypertext Transfer Protocol client 和 server 受支持。
  :ref:`http_client_interface` library 支持 HTTP/1.1（:rfc:`2616`）。
  :ref:`http_server_interface` library 支持 HTTP/1.1（:rfc:`2616`）和
  HTTP/2（:rfc:`9113`）。
  提供 :zephyr:code-sample:`sockets-http-client` 和
  :zephyr:code-sample:`sockets-http-server` samples。

* **Websocket**（:rfc:`6455`）client 受支持。
  提供 :zephyr:code-sample:`sockets-websocket-client` sample。

* **DNS** Domain Name Service（:rfc:`1035`）client functionality 受支持。
  Applications 可用 DNS API 从 DNS server 查询 domain name 信息或 IP
  addresses。可查询 IPv4 (A) 和 IPv6 (AAAA) 两种 records。
  支持 multicast DNS (mDNS)（:rfc:`6762`）和 link-local multicast name resolution
  (LLMNR（:rfc:`4795`）。
  还支持 DNS Service Discovery（:rfc:`6763`）。

* **Network Management API。**Applications 可用 network management API
  监听 core network stack 生成的 management events（例如 IP address
  添加到 device 时（或 network interface 起来时等。

* **Wi-Fi Management API。**Applications 可用 Wi-Fi management API
  管理 interface（例如连接 Wi-Fi network（并
  扫描可用 Wi-Fi networks。

* **Wi-Fi Network Manager API。**Wi-Fi Network Managers 现可
  注册到 Wi-Fi stack。Network Managers 然后可
  实现 Wi-Fi Management API（并管理 Wi-Fi interface。

* **Multiple Network Technologies。**Zephyr OS 可配置为
  同时支持多个 network technologies（仅需在 Kconfig 中
  启用：例如 Ethernet、Wi-Fi 和 802.15.4 支持。注意
  这些 technologies 之间不提供自动 IP routing functionality。Applications 可按需向期望
  network interface 发送 data。

* **Minimal Copy Network Buffer Management。**可拥有
  minimal copy network data path。这意味着 system 尝试在
  发送 application data 到 network 时避免复制。

* **Virtual LAN support。**Virtual LANs (VLANs) 允许将物理
  ethernet networks 划分为 logical networks。
  更多细节参见 :ref:`VLAN support <vlan_interface>`。

* **Network traffic classification。**发送和接收的 network packets 可
  根据 application 需要优先化。
  更多细节参见 :ref:`traffic classification <traffic-class-support>`。

* **Time Sensitive Networking。**gPTP (generalized Precision Time Protocol)
  和 PTP (Precision Time Protocol（IEEE 1588) 均受支持。
  更多细节参见 :ref:`gPTP support <gptp_interface>` 和 :ref:`PTP support <ptp_interface>`。

* **SNTP** Simple Network Time Protocol（:rfc:`5905`）client 受支持。
  提供 :zephyr:code-sample:`sntp-client` sample。

* **SOCKS5** proxy 5 版本（:rfc:`1928`）受支持。

* **TFTP** Trivial File Transfer Protocol（:rfc:`1350`）client 受支持。
  提供 :zephyr:code-sample:`tftp-client` sample。

* **MIDI2** MIDI 2.0 network UDP transport 受支持。
  提供 :zephyr:code-sample:`netmidi2` sample。

* **OCPP** Open Charge Point Protocol 受支持。
  提供 :zephyr:code-sample:`ocpp` sample。

* **Prometheus** Metric Server functionality 受支持。
  提供 :zephyr:code-sample:`prometheus`。

* **Network shell。**Network shell 提供查明
  network status（启用/禁用 features（以及发出如 ping
  或 DNS resolving 等 commands 的 helpers。Net-shell 在开发 network software 时有用。
  更多细节参见 :ref:`network shell <net_shell>`。

* **zperf** 为 iPerf v2 network performance 和 bandwidth 测量 tool。
  支持 client 和 server 两种 functionality。提供 :zephyr:code-sample:`zperf`
  sample。

另外（Zephyr OS 中支持以下 network technologies (link layers)：

* IEEE 802.15.4
* Bluetooth
* Ethernet（IEEE 802.3
* Wi-Fi（IEEE 802.11
* Cellular / PPP（:rfc:`1661`）
* Thread（提供 :zephyr:code-sample-category:`openthread` samples）
* SocketCAN 的 CAN bus
* SLIP (IP over serial line)。用于与 QEMU 测试。其
  向 host system（如 Linux）提供 ethernet interface（且 test applications
  可在 Linux host 中运行（并向 Zephyr OS device 发送 network data。

Source Tree Layout
******************

Networking stack source code tree 组织如下：

:zephyr_file:`subsys/net/`
  各种可选 network stack components（如 connection manager、
  packet filter code 和 hostname handling）位于此处。

:zephyr_file:`subsys/net/ip/`
  Core network stack code 位于此处。

:zephyr_file:`subsys/net/l2`
  IP stack layer 2 code 位于此处。这包括对
  Ethernet、IEEE 802.15.4 和 Wi-Fi 的通用
  support。

:zephyr_file:`subsys/net/lib/`
  Application-level protocols（DNS、MQTT 等）和额外 stack
  components（BSD Sockets 等）。

:zephyr_file:`include/zephyr/net/`
  Public API header files。这些是 applications 须
  包含以使用 IP networking functionality 的 header files。

:zephyr_file:`samples/net/`
  Sample networking code。这是开始
  network application development 的良好 reference。

:zephyr_file:`tests/net/`
  Test applications。这些 applications 用于验证
  IP stack 的 functionality（但非 sample code 的最佳
  source（改用 :zephyr_file:`samples/net/`）。

.. _LwM2M specification 1.0.2:
   https://www.openmobilealliance.org/release/LightweightM2M/V1_0_2-20180209-A/OMA-TS-LightweightM2M-V1_0_2-20180209-A.pdf

.. _LwM2M specification 1.1.1:
   https://www.openmobilealliance.org/release/LightweightM2M/V1_1_1-20190617-A/
