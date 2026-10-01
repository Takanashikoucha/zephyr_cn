.. _network_tracing:

Network Tracing
###############

.. contents::
    :local:
    :depth: 2

User 可启用 network core stack 和 socket API calls tracing。

:kconfig:option:`CONFIG_TRACING_NET_CORE` option 控制 core network
stack tracing。此 option 在启用 tracing 和 networking 时默认启用。系统将开始收集接收和发送 call
verdicts 即，network packet 是否成功发送或接收。
其还将收集 packet 发送或接收 timings 即，交付
network packet 耗时多久（以及所用
network interface、priority
和 traffic class。

:kconfig:option:`CONFIG_TRACING_NET_SOCKETS` option 可用于跟踪
系统中 BSD socket call 使用。在启用 tracing 和 BSD socket
API 支持时启用。系统将开始收集进行了哪些 BSD socket
API calls（以及 API calls 使用并返回哪些 parameters。

如何使用 tracing
service 参见 :ref:`tracing documentation <tracing>`。
