.. _net_dplpmtud:

Datagram PLPMTUD API
####################

.. contents::
    :local:
    :depth: 2

Overview
********

Zephyr 提供基于 :rfc:`8899` 的通用 **Datagram Packetization Layer Path MTU Discovery**（DPLPMTUD）实现。其面向基于 UDP 的 transports（QUIC、CoAP over UDP、custom protocols）（其必须在不依赖本地 IP fragmentation 的情况下发现 datagram payload 可多大。

Subsystem 如下划分职责：

**Generic stack**（``subsys/net/ip/dplpmtud.c``）

* Per-destination search state：validated PLPMTU、probe size、retry count、bounds
* 在 base PLPMTU（1200 bytes）和 path ceiling 之间的 binary search
* 与现有 PMTU destination cache 的集成（ICMP PTB 输入（validated size 输出）
* 当 PMTU cache 报告低于 base PLPMTU 的 MTU 时的 black-hole handling

**Transport consumer**

* 按 :c:func:`net_dplpmtud_get_path_probe_size()` 返回的 size 构建 probe datagrams
* 以 don't fragment 启用发送 probes（参见 :ref:`ip_socket_options` 和 :c:macro:`ZSOCK_IP_DONTFRAG` / :c:macro:`ZSOCK_IPV6_DONTFRAG`）
* 将 transport ACK/loss 映射到 :c:func:`net_dplpmtud_on_path_probe_acked()` 和 :c:func:`net_dplpmtud_on_path_probe_lost()`

:ref:`QUIC <quic_dplpmtud>` 为首个 in-tree consumer。其他 transports 可使用相同 API 而不重复 RFC 8899 state machine。

Configuration
*************

按 address family 启用 DPLPMTUD：

* :kconfig:option:`CONFIG_NET_IPV4_PMTU` 和 :kconfig:option:`CONFIG_NET_IPV4_PMTU_DPLPMTUD` 用于 IPv4
* :kconfig:option:`CONFIG_NET_IPV6_PMTU` 和 :kconfig:option:`CONFIG_NET_IPV6_PMTU_DPLPMTUD` 用于 IPv6

两个 families 均要求 :kconfig:option:`CONFIG_NET_UDP`。Umbrella option :kconfig:option:`CONFIG_NET_PMTU_DPLPMTUD` 在任一 family option 启用时选中。

基于 ICMP 的 PMTU reduction（Packet Too Big）仍通过 :kconfig:option:`CONFIG_NET_IPV4_PMTU_PTB` 和 :kconfig:option:`CONFIG_NET_IPV6_PMTU_PTB` 可用。DPLPMTUD 通过主动探测更大 size（当 path 允许时）补充 PTB。

跟踪的并发 paths 数分别匹配 :kconfig:option:`CONFIG_NET_IPV4_PMTU_DESTINATION_CACHE_ENTRIES` 和 :kconfig:option:`CONFIG_NET_IPV6_PMTU_DESTINATION_CACHE_ENTRIES`。

Usage model
***********

为每个 remote destination 初始化一个 :c:struct:`net_dplpmtud_path`（或为 connection 生命周期复用 handle）：

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

Probe 生命周期：

1. 调用 :c:func:`net_dplpmtud_get_path_probe_size()`。返回值 ``0`` 表示无需 probe。Path 须已初始化；getters 不创建 cache entries。
2. 若 :c:func:`net_dplpmtud_path_probe_in_flight()` 为 false（构建并发送该 size 的 probe datagram（don't fragment 设置（socket option 或 :c:func:`zsock_sendmsg()` 中 per-datagram control message）。
3. 调用 :c:func:`net_dplpmtud_on_path_probe_sent()` 在 generic state machine 中保留 probe（然后传输 probe datagram。
4. 若发送失败（调用 :c:func:`net_dplpmtud_on_path_probe_lost()` 使 core 和 transport state 保持对齐。
5. 在 transport 确认时（调用 :c:func:`net_dplpmtud_on_path_probe_acked()` 或 :c:func:`net_dplpmtud_on_path_probe_lost()`。

当 transport 学到新 ceiling 时（例如 QUIC ``max_udp_payload_size`` transport parameter）更新 :c:func:`net_dplpmtud_set_path_max_plpmtu()`。

若 transport 独立于 ICMP 检测到 black hole（调用 :c:func:`net_dplpmtud_note_path_blackhole()`。低于 base PLPMTU 的 PTB updates 通过 PMTU cache 自动应用。

API Reference
*************

.. doxygengroup:: net_dplpmtud
