.. _net_offload_interface:

网络流量卸载
==========================

.. contents::
    :local:
    :depth: 2

网络卸载
##################

概述
********

网络卸载 API 提供了一组钩子，设备厂商
可以使用它们为 IP 栈提供替代实现。这意味着
实际的网络连接建立、数据传输等，
是在厂商 HAL 中完成的，而不是在 Zephyr 网络栈中完成。

API 参考
*************

.. doxygengroup:: net_offload

.. _net_socket_offloading:

套接字卸载
#################

概述
********

除了网络卸载 API 之外，Zephyr 还支持在
套接字 API 级别卸载网络功能。采用这种方式，
提供网络栈替代实现、并为其网络设备
暴露套接字 API 的厂商，可以轻松地将其
集成到 Zephyr 中。

关于如何在套接字级别集成网络卸载的示例
实现，参见 :zephyr_file:`drivers/wifi/simplelink/simplelink_sockets.c`。
