.. _dhcpv4_interface:

DHCPv4
######

.. contents::
    :local:
    :depth: 2

Overview
********

Dynamic Host Configuration Protocol（DHCP）是用于 IPv4 networks 的 network management protocol。DHCPv4 server 动态为网络上每个 device 分配 IPv4 address 和其他 network configuration parameters（使它们能与其他 IP networks 通信。DHCP 工作原理的详细概述参见此 `DHCP Wikipedia article <https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol>`_。

注意 Zephyr 同时支持 DHCPv4 client 和 server 功能。

Sample usage
************

参见 :zephyr:code-sample:`dhcpv4-client` sample application 以了解细节。

API Reference
*************

.. doxygengroup:: dhcpv4
