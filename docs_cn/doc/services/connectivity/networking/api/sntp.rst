.. _sntp_interface:

Simple Network Time Protocol 库
####################################

.. contents::
    :local:
    :depth: 2

概述
********

SNTP 库实现了 :rfc:`4330`。

SNTP 提供了一种在计算机网络中同步时钟的方法。

客户端（:kconfig:option:`CONFIG_SNTP`）向 SNTP 服务器查询时间。服务器（:kconfig:option:`CONFIG_SNTP_SERVER`）在 UDP 端口 123 上应答此类查询，覆盖每个已启用的地址族。应用程序负责设置系统时钟，并通过 :c:func:`sntp_server_clock_source` 告知服务器其时间来源。在此之前，服务器会以跳时指示器（leap indicator）设置为"时钟未同步"、stratum 为 16 的方式应答，从而使客户端丢弃其时间戳。

API 参考
*************

.. doxygengroup:: sntp

.. doxygengroup:: sntp_server
