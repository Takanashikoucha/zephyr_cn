.. _net_config_interface:

网络配置库
#############################

.. contents::
    :local:
    :depth: 2

概述
********

网络配置库在系统启动期间基于用户提供的 Kconfig 选项以半自动方式设置网络设备。

以下 Kconfig 选项影响配置库如何设置系统：

.. csv-table:: 网络配置库的 Kconfig 选项
   :header: "选项名称", "描述"
   :widths: 45 55

   ":kconfig:option:`CONFIG_NET_CONFIG_SETTINGS`", "此选项控制网络系统是否被配置或初始化。如果未设置，则配置库不用于初始化，应用程序需要自行完成所有网络相关配置。如果此选项已设置，则用户可以可选地配置静态 IP 地址，将其设置到系统中的第一个网络接口。通常，设置静态 IP 地址仅可用于测试，不应在生产代码中使用。有关设置静态 IP 地址的具体选项，参见配置库 Kconfig 文件 :zephyr_file:`subsys/net/lib/config/Kconfig`。"
   ":kconfig:option:`CONFIG_NET_CONFIG_AUTO_INIT`", "设备启动时，网络系统自动配置。"
   ":kconfig:option:`CONFIG_NET_CONFIG_INIT_TIMEOUT`", "此选项指示等待网络就绪和可用的时长。例如，如果在此限制内未收到来自 DHCPv4 的 IPv4 地址，则 ``net_config_init()`` 调用将在设备启动期间返回错误。"
   ":kconfig:option:`CONFIG_NET_CONFIG_NEED_IPV4`", "网络应用程序需要 IPv4 支持才能正常工作。此选项确保网络应用程序正确初始化以使用 IPv4。
   如果 :kconfig:option:`CONFIG_NET_IPV4` 未启用，则设置此选项将自动启用 IPv4。"
   ":kconfig:option:`CONFIG_NET_CONFIG_NEED_IPV6`", "网络应用程序需要 IPv6 支持才能正常工作。此选项确保网络应用程序正确初始化以使用 IPv6。
   如果 :kconfig:option:`CONFIG_NET_IPV6` 未启用，则设置此选项将自动启用 IPv6。"
   ":kconfig:option:`CONFIG_NET_CONFIG_NEED_IPV6_ROUTER`", "如果 IPv6 已启用，则此选项指示网络应用程序需要 IPv6 路由器存在后才继续。这实际上意味着应用程序想在收到 IPv6 路由器通告消息前等待。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV6_ADDR`","分配给默认网络接口的本地静态 IPv6 地址。"
   ":kconfig:option:`CONFIG_NET_CONFIG_PEER_IPV6_ADDR`","对端静态 IPv6 地址。这主要可用于应用程序可以连接到预定义主机的测试环境。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_ADDR`","分配给默认网络接口的本地静态 IPv4 地址。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_NETMASK`","分配给 IPv4 地址的静态 IPv4 子网掩码。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_GW`","分配给默认网络接口的静态 IPv4 网关地址。"
   ":kconfig:option:`CONFIG_NET_CONFIG_PEER_IPV4_ADDR`","对端静态 IPv4 地址。这主要可用于应用程序可以连接到预定义主机的测试环境。"

SNTP 时钟初始化
*************************

如果设置了 :kconfig:option:`CONFIG_NET_CONFIG_CLOCK_SNTP_INIT`，
库还会从 SNTP 服务器初始化系统时钟，
并可选地通过 :kconfig:option:`CONFIG_NET_CONFIG_SNTP_INIT_RESYNC` 保持同步。

要查询的服务器按以下顺序查找：

1. 运行时用 :c:func:`net_config_sntp_set_server` 设置的服务器。
   这需要 :kconfig:option:`CONFIG_NET_CONFIG_SNTP_INIT_SERVER_RUNTIME`，
   适用于仅在运行时才得知使用哪个时间服务器的应用程序，
   例如在预配之后。
2. 通过 DHCPv4 NTP 服务器选项收到的服务器，
   如果设置了 :kconfig:option:`CONFIG_NET_CONFIG_SNTP_INIT_SERVER_USE_DHCPV4_OPTION`。
3. :kconfig:option:`CONFIG_NET_CONFIG_SNTP_INIT_SERVER`，
   如果设置了 :kconfig:option:`CONFIG_NET_CONFIG_CLOCK_SNTP_INIT`
   但未启用 :kconfig:option:`CONFIG_NET_CONFIG_SNTP_INIT_SERVER_RUNTIME`
   或 :kconfig:option:`CONFIG_NET_CONFIG_SNTP_INIT_SERVER_USE_DHCPV4_OPTION`，
   则必须设置此项。

使用示例
************

如果设置了 :kconfig:option:`CONFIG_NET_CONFIG_AUTO_INIT`，则配置库自动启用并在设备启动期间运行。在这种情况下，库将自动调用 ``net_config_init()``，应用程序无需进行任何网络配置。

如果想使用网络配置库但不进行自动初始化，可以手动调用 ``net_config_init()``。``flags`` 参数可用于向库提供有关应用程序在实际启动前希望具备何种功能的提示。

API 参考
*************

.. doxygengroup:: net_config
