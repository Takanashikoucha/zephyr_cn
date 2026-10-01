.. _net_core_interface:

Network Core Helpers
####################

.. contents::
    :local:
    :depth: 2

Overview
********

Network subsystem 包含两个用于发送和接收 network data 的 functions。``net_recv_data()`` 通常由 network device driver 使用（当收到的 network data 需被推上 network stack 以进一步处理时。所有 data 通过 network interface 接收（其通常由 device driver 创建。

发送时（可用 ``net_send_data()``。通常 applications 不直接调用此 function（因为有 :ref:`bsd_sockets_interface` API 用于发送和接收 network data。

API Reference
*************

.. doxygengroup:: net_core
