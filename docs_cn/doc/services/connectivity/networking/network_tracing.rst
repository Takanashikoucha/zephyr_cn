.. _network_tracing:

网络跟踪
###############

.. contents::
    :local:
    :depth: 2

用户可以为网络核心协议栈和套接字 API 调用启用跟踪。

:kconfig:option:`CONFIG_TRACING_NET_CORE` 选项用于控制核心网络协议栈的跟踪。如果跟踪和网络功能均已启用，该选项默认开启。系统会开始收集收包和发包的调用结果，即网络数据包是否成功发送或接收。同时还会收集数据包发送或接收的耗时，即投递该网络数据包花了多长时间，以及所使用的网络接口、优先级和流量类别。

:kconfig:option:`CONFIG_TRACING_NET_SOCKETS` 选项可用于跟踪系统中的 BSD 套接字调用使用情况。如果跟踪和 BSD 套接字 API 支持均已启用，该选项会开启。系统会开始收集发起了哪些 BSD 套接字 API 调用，以及这些 API 调用使用了哪些参数、返回了什么。

有关如何使用跟踪服务，请参阅 :ref:`跟踪文档 <tracing>`。
