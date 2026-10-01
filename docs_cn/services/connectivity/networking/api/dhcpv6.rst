.. _dhcpv6_interface:

DHCPv6
######

.. contents::
    :local:
    :depth: 2

Overview
********

IPv6 的 Dynamic Host Configuration Protocol（DHCP）是用于基于 IPv6 的 networks 的 network management protocol。DHCPv6 server 动态为网络上每个 device 分配 IPv6 address 和其他 network configuration parameters（使它们能与其他 IP networks 通信。DHCPv6 工作原理的详细概述参见此 `DHCPv6 Wikipedia article <https://en.wikipedia.org/wiki/DHCPv6>`_。

Zephyr 同时支持 DHCPv6 client 和 server 功能（包括按 `RFC 8415 <https://www.rfc-editor.org/rfc/rfc8415>`_ 指定的 IPv6 prefix delegation（IA_PD）。

Prefix delegation
*****************

DHCPv6 client 可充当 *requesting router*：除请求 non-temporary address（IA_NA）外（其可通过设置 :c:member:`net_dhcpv6_params.request_prefix` 请求 delegated prefix（IA_PD）。Delegated prefix 安装在 requesting interface 上。

要将 node 变为完整的 requesting router（将 prefix sub-delegate 到一个或多个 downstream links（在 :c:member:`net_dhcpv6_params.downstream_ifaces` 中列出 downstream（LAN）interface indices（并将 :c:member:`net_dhcpv6_params.downstream_count` 设为 entries 数。每个 downstream interface 被分配从 delegated prefix 划分出的不同 ``/64``（第 N 个 interface 获得第 N 个 ``/64``）（其然后通过 Router Advertisements 在该 interface 上 advertise（允许 downstream hosts 使用 SLAAC 自动配置 addresses。Array 最多持有 :kconfig:option:`CONFIG_NET_DHCPV6_MAX_DOWNSTREAM` entries；:c:member:`net_dhcpv6_params.downstream_count` 为 0 表示 delegated prefix 仅安装在 requesting interface 上。这需要 :kconfig:option:`CONFIG_NET_IPV6_ND_RA_TX`（Router Advertisement transmit / router role）以及（为使 traffic 在 upstream 和 downstream interfaces 之间转发（:kconfig:option:`CONFIG_NET_DHCPV6_FORWARDING`。

Delegation 须足够短以包含为每个 downstream interface 的不同 ``/64``（即（长度 ``L`` 的 delegated prefix 最多可服务 ``2^(64 - L)`` downstream links。恰好 ``/64`` 的 delegation 因此可服务单个 link（长于 ``/64`` 的完全无法 sub-delegate。无法被赋予不同 ``/64`` 的 downstream interfaces 被跳过并带 warning。

DHCPv6 server（:kconfig:option:`CONFIG_NET_DHCPV6_SERVER`）实现 *delegating router* role（从配置的 pools 分配 addresses 和 delegated prefixes。参见 :zephyr:code-sample:`dhcpv6-pd` 作为两个 role 的完整示例。

Limitations
***********

实现有意省略 RFC 8415 和 RFC 4861 允许简化的几件事：

* 客户端停止时发送的 Release（:kconfig:option:`CONFIG_NET_DHCPV6_SEND_RELEASE_ON_STOP`）为 best effort（其传输一次（不按 :rfc:`8415#section-18.2.7` 描述重传 ``REL_MAX_RC`` 次。未释放的 lease 在过期时由 server 回收。

* Unsolicited Router Advertisements 按 :kconfig:option:`CONFIG_NET_IPV6_ND_RA_TX_INTERVAL` 配置的固定 interval 发送（而非 ``MinRtrAdvInterval`` 和 ``MaxRtrAdvInterval`` 之间的随机 interval（且 interface 承担 router role 时不发送 ``MAX_INITIAL_RTR_ADVERTISEMENTS`` 的 initial burst。Solicited advertisements 按 :rfc:`4861#section-6.2.6` 要求被 rate limited 并随机延迟。

* Server 通过变化配置的 pool base 的单个 byte 分配 addresses 和 prefixes（因此 pools 限于 :kconfig:option:`CONFIG_NET_DHCPV6_SERVER_MAX_LEASES` entries（且 IA_PD pool prefix lengths 须 byte aligned。

API Reference
*************

.. doxygengroup:: dhcpv6

.. doxygengroup:: dhcpv6_server
