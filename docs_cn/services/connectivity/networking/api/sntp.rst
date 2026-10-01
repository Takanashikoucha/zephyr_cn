.. _sntp_interface:

Simple Network Time Protocol Library
####################################

.. contents::
    :local:
    :depth: 2

Overview
********

SNTP library 实现 :rfc:`4330`。

SNTP 提供在 computer networks 中同步 clocks 的方式。

Client（:kconfig:option:`CONFIG_SNTP`）从 SNTP server 查询 time。Server（:kconfig:option:`CONFIG_SNTP_SERVER`）在每个启用的 address family 上的 UDP port 123 响应此类 queries。Application 负责设置 system clock（并用 :c:func:`sntp_server_clock_source` 告知 server 其 time 来源。在此之前（server 响应 leap indicator 设为 "clock not synchronized"（stratum 16（使 clients 丢弃其 timestamps。

API Reference
*************

.. doxygengroup:: sntp

.. doxygengroup:: sntp_server
