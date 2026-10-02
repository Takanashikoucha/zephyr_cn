.. _dhcpv6_interface:

DHCPv6
######

.. contents::
    :local:
    :depth: 2

概述
****

IPv6 的动态主机配置协议（DHCP）是一种用于基于 IPv6 的网络的网络管理协议。DHCPv6 服务器为网络中的每台设备动态分配 IPv6 地址和其他网络配置参数，使它们能够与其他 IP 网络进行通信。
有关 DHCPv6 工作原理的详细说明，请参阅这篇
`DHCPv6 维基百科文章 <https://en.wikipedia.org/wiki/DHCPv6>`_。

Zephyr 同时支持 DHCPv6 客户端和服务器功能，包括 :rfc:`8415` 中规定的 IPv6 前缀委派（IA_PD）。

前缀委派
*********

DHCPv6 客户端可以充当*请求路由器*：除了请求非临时地址（IA_NA）之外，还可以通过设置 :c:member:`net_dhcpv6_params.request_prefix` 请求委派的子网前缀（IA_PD）。委派的子网前缀会安装在请求方接口上。

要将节点转变为完整的请求路由器（把前缀再委派给一个或多个下游链路），请在 :c:member:`net_dhcpv6_params.downstream_ifaces` 中列出下游（LAN）接口索引，并将 :c:member:`net_dhcpv6_params.downstream_count` 设置为条目数量。每个下游接口都会从委派的子网前缀中划分出一个独立的 ``/64`` 子网（第 N 个接口获得第 N 个 ``/64``），随后通过路由器通告（Router Advertisement）在该接口上宣告，使下游主机能够使用 SLAAC 自动配置地址。该数组最多可容纳 :kconfig:option:`CONFIG_NET_DHCPV6_MAX_DOWNSTREAM` 个条目；:c:member:`net_dhcpv6_params.downstream_count` 为 0 表示委派的子网前缀仅安装在请求方接口上。这需要 :kconfig:option:`CONFIG_NET_IPV6_ND_RA_TX`（路由器通告发送/路由器角色），并且如果要在上游接口和下游接口之间转发流量，还需要 :kconfig:option:`CONFIG_NET_IPV6_FORWARDING`。

委派的子网前缀长度必须足够短，以便为每个下游接口容纳一个独立的 ``/64`` 子网，也就是说，长度为 ``L`` 的委派子网前缀最多可服务 ``2^(64 - L)`` 个下游链路。因此，恰好为 ``/64`` 的委派只能服务单个链路，而长于 ``/64`` 的委派则完全无法再委派。无法获得独立 ``/64`` 子网的下游接口会被跳过并发出警告。

DHCPv6 服务器（:kconfig:option:`CONFIG_NET_DHCPV6_SERVER`）实现了*委派路由器*角色，从配置的地址池和子网前缀池中分配地址和委派的子网前缀。有关两种角色的完整示例，请参阅 :zephyr:code-sample:`dhcpv6-pd`。

限制
****

该实现有意省略了 RFC 8415 和 RFC 4861 允许简化的若干内容：

* 客户端停止时发送的 Release 报文（:kconfig:option:`CONFIG_NET_DHCPV6_SEND_RELEASE_ON_STOP`）是尽力而为的，只发送一次，不会按照 :rfc:`8415#section-18.2.7` 中所述重传 ``REL_MAX_RC`` 次。未释放的租约会在到期后由服务器回收。

* 未经请求的路由器通告以 :kconfig:option:`CONFIG_NET_IPV6_ND_RA_TX_INTERVAL` 配置的固定间隔发送，而不是在 ``MinRtrAdvInterval`` 和 ``MaxRtrAdvInterval`` 之间以随机间隔发送，并且接口承担路由器角色时也不会发送 ``MAX_INITIAL_RTR_ADVERTISEMENTS`` 次初始突发报文。被请求的通告按照 :rfc:`4861#section-6.2.6` 的要求进行速率限制并随机延迟。

* 服务器通过变更配置池基址的单个字节来分配地址和子网前缀，因此池的大小限制为 :kconfig:option:`CONFIG_NET_DHCPV6_SERVER_MAX_LEASES` 个条目，且 IA_PD 池的子网前缀长度必须按字节对齐。

API 参考
*********

.. doxygengroup:: dhcpv6

.. doxygengroup:: dhcpv6_server
