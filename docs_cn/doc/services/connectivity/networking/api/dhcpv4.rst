.. _dhcpv4_interface:

DHCPv4
######

.. contents::
    :local:
    :depth: 2

概述
****

动态主机配置协议（DHCP）是一种用于 IPv4 网络的网络管理协议。DHCPv4 服务器为网络中的每台设备动态分配 IPv4 地址和其他网络配置参数，使它们能够与其他 IP 网络进行通信。
有关 DHCP 工作原理的详细说明，请参阅这篇
`DHCP 维基百科文章 <https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol>`_。

请注意，Zephyr 同时支持 DHCPv4 客户端和服务器功能。

示例用法
********

有关详细信息，请参阅 :zephyr:code-sample:`dhcpv4-client` 示例应用程序。

API 参考
*********

.. doxygengroup:: dhcpv4
