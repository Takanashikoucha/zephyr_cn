.. _net_offload_interface:

Network Traffic Offloading
==========================

.. contents::
    :local:
    :depth: 2

Network Offloading
##################

Overview
********

Network offloading API 提供 hooks（device vendor 可用其提供 IP stack 的 alternate implementation。这意味着实际的 network connection 创建、data transfer 等在 vendor HAL 中完成（而非 Zephyr network stack。

API Reference
*************

.. doxygengroup:: net_offload

.. _net_socket_offloading:

Socket Offloading
#################

Overview
********

除 network offloading API 外（Zephyr 允许在 socket API 层卸载 networking 功能。用此 approach（提供 networking stack alternate implementation（为其 networking devices 暴露 socket API 的 vendors 可轻松与 Zephyr 集成。

socket 层集成 network offloading 的 sample 实现参见 :zephyr_file:`drivers/wifi/simplelink/simplelink_sockets.c`。
