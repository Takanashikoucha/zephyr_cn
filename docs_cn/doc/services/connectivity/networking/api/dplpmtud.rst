.. _net_dplpmtud:

数据报 PLPMTUD API
####################

.. contents::
    :local:
    :depth: 2

概述
****

Zephyr 提供了基于 :rfc:`8899` 的通用**数据报分组层路径 MTU 发现**（DPLPMTUD）实现。它适用于基于 UDP 的传输协议（QUIC、基于 UDP 的 CoAP、自定义协议），这些协议必须在不依赖本地 IP 分片的情况下发现数据报负载可以有多大。

该子系统按以下方式划分职责：

**通用协议栈**（``subsys/net/ip/dplpmtud.c``）

* 每个目的地的搜索状态：已验证的 PLPMTU、探测大小、重试次数、边界
* 在基础 PLPMTU（1200 字节）和路径上限之间进行二分查找
* 与现有 PMTU 目的地缓存的集成（ICMP PTB 输入，已验证的大小输出）
* 当 PMTU 缓存报告的 MTU 低于基础 PLPMTU 时的黑洞处理

**传输层消费者**

* 按照 :c:func:`net_dplpmtud_get_path_probe_size()` 返回的大小构造探测数据报
* 启用不分片（don't fragment）发送探测报文（参见 :ref:`ip_socket_options` 以及 :c:macro:`ZSOCK_IP_DONTFRAG` / :c:macro:`ZSOCK_IPV6_DONTFRAG`）
* 将传输层 ACK/丢包映射到 :c:func:`net_dplpmtud_on_path_probe_acked()` 和 :c:func:`net_dplpmtud_on_path_probe_lost()`

:ref:`QUIC <quic_dplpmtud>` 是树内的第一个消费者。其他传输协议也可以使用相同的 API，而无需重复实现 RFC 8899 状态机。

配置
****

按地址族启用 DPLPMTUD：

* IPv4 使用 :kconfig:option:`CONFIG_NET_IPV4_PMTU` 和 :kconfig:option:`CONFIG_NET_IPV4_PMTU_DPLPMTUD`
* IPv6 使用 :kconfig:option:`CONFIG_NET_IPV6_PMTU` 和 :kconfig:option:`CONFIG_NET_IPV6_PMTU_DPLPMTUD`

两个地址族还都需要 :kconfig:option:`CONFIG_NET_UDP`。只要启用了任一地址族选项，就会选中总选项 :kconfig:option:`CONFIG_NET_PMTU_DPLPMTUD`。

基于 ICMP 的 PMTU 缩减（Packet Too Big）仍可通过 :kconfig:option:`CONFIG_NET_IPV4_PMTU_PTB` 和 :kconfig:option:`CONFIG_NET_IPV6_PMTU_PTB` 使用。DPLPMTUD 在路径允许时主动探测更大的大小，从而与 PTB 形成互补。

同时跟踪的路径数量分别与 :kconfig:option:`CONFIG_NET_IPV4_PMTU_DESTINATION_CACHE_ENTRIES` 和 :kconfig:option:`CONFIG_NET_IPV6_PMTU_DESTINATION_CACHE_ENTRIES` 一致。

使用模型
*********

为每个远程目的地初始化一个 :c:struct:`net_dplpmtud_path`（或者在整个连接生命周期内复用该句柄）：

.. code-block:: c

   struct net_dplpmtud_path path;
   uint16_t max_plpmtu = 1452U; /* transport / peer limit, or 0 if uncapped */
   int mtu;
   int probe;
   int ret;

   ret = net_dplpmtud_init_path(&path, &remote_addr, max_plpmtu);
   if (ret < 0) {
       /* handle error */
   }

   mtu = net_dplpmtud_get_path_mtu(&path);
   if (mtu < 0) {
       mtu = NET_DPLPMTUD_BASE_PLPMTU;
   }

   /* Application data must fit in @a mtu bytes (transport framing excluded). */

探测生命周期：

1. 调用 :c:func:`net_dplpmtud_get_path_probe_size()`。返回值 ``0`` 表示不需要探测。路径必须已经初始化；获取器不会创建缓存条目。
2. 如果 :c:func:`net_dplpmtud_path_probe_in_flight()` 为假，则以该大小构造并发送设置不分片位的探测数据报（使用套接字选项或 :c:func:`zsock_sendmsg()` 中的按数据报控制消息）。
3. 调用 :c:func:`net_dplpmtud_on_path_probe_sent()` 在通用状态机中预留该探测报文，然后发送探测数据报。
4. 如果发送失败，调用 :c:func:`net_dplpmtud_on_path_probe_lost()`，使核心状态和传输层状态保持一致。
5. 在传输层确认时，调用 :c:func:`net_dplpmtud_on_path_probe_acked()` 或 :c:func:`net_dplpmtud_on_path_probe_lost()`。

当传输层得知新的上限时（例如 QUIC 的 ``max_udp_payload_size`` 传输参数），调用 :c:func:`net_dplpmtud_set_path_max_plpmtu()` 更新上限。

如果传输层检测到与 ICMP 无关的黑洞，调用 :c:func:`net_dplpmtud_note_path_blackhole()`。低于基础 PLPMTU 的 PTB 更新会通过 PMTU 缓存自动应用。

API 参考
*********

.. doxygengroup:: net_dplpmtud
