.. _net_stats_interface:

Network Statistics
##################

.. contents::
    :local:
    :depth: 2

Overview
********

若设置 :kconfig:option:`CONFIG_NET_STATISTICS`（则收集 network statistics。IPv4 或 IPv6 的 individual component statistics 可在不需要时关闭。细节参见 :zephyr_file:`subsys/net/ip/Kconfig.stats` file 中的各种 options。

默认（system 按 network interface 收集 network statistics。这可由 :kconfig:option:`CONFIG_NET_STATISTICS_PER_INTERFACE` option 控制。

若 application 想收集 statistics 以进一步处理（可设置 :kconfig:option:`CONFIG_NET_STATISTICS_USER_API` option。用 network management interface API 执行此操作。细节参见 :ref:`net_mgmt_interface`。

可设置 :kconfig:option:`CONFIG_NET_STATISTICS_ETHERNET` option 以收集 generic Ethernet statistics。若设置 :kconfig:option:`CONFIG_NET_STATISTICS_ETHERNET_VENDOR` option（则 Ethernet device driver 可收集 Ethernet device specific statistics。这些 statistics 然后可传输到 application 以处理。

若设置 :kconfig:option:`CONFIG_NET_SHELL` option（则 network shell 可用 ``net stats`` command 显示 statistics 信息。

API Reference
*************

.. doxygengroup:: net_stats
