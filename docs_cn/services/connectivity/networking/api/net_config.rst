.. _net_config_interface:

Network Configuration Library
#############################

.. contents::
    :local:
    :depth: 2

Overview
********

Network configuration library 在系统 boot 期间基于 user 提供的 Kconfig options 以半自动方式设置 networking devices。

以下 Kconfig options 影响 configuration library 如何设置 system：

.. csv-table:: Kconfig options for network configuration library
   :header: "Option name", "Description"
   :widths: 45 55

   ":kconfig:option:`CONFIG_NET_CONFIG_SETTINGS`", "此 option 控制 network system 是否被配置或初始化。若未设置（则 config library 不用于初始化（且 application 需自行完成所有 network 相关 configuration。若此 option 设置（则 user 可选配置静态 IP addresses 以设置到 system 中第一个 network interface。通常设置静态 IP addresses 仅可用于测试（不应在生产代码中使用。设置静态 IP addresses 的特定 options 参见 config library Kconfig file :zephyr_file:`subsys/net/lib/config/Kconfig`。"
   ":kconfig:option:`CONFIG_NET_CONFIG_AUTO_INIT`", "Device 启动时 networking system 自动配置。"
   ":kconfig:option:`CONFIG_NET_CONFIG_INIT_TIMEOUT`", "其指示等待 networking 就绪和可用的时长。例如（若在此限制内未收到来自 DHCPv4 的 IPv4 address（则 ``net_config_init()`` 调用将在 device 启动期间返回 error。"
   ":kconfig:option:`CONFIG_NET_CONFIG_NEED_IPV4`", "Network application 需 IPv4 支持以正确工作。此 option 确保 network application 正确初始化以使用 IPv4。若 :kconfig:option:`CONFIG_NET_IPV4` 未启用（则设置此 option 将自动启用 IPv4。"
   ":kconfig:option:`CONFIG_NET_CONFIG_NEED_IPV6`", "Network application 需 IPv6 支持以正确工作。此 option 确保 network application 正确初始化以使用 IPv6。若 :kconfig:option:`CONFIG_NET_IPV6` 未启用（则设置此 option 将自动启用 IPv6。"
   ":kconfig:option:`CONFIG_NET_CONFIG_NEED_IPV6_ROUTER`", "若 IPv6 启用（则此 option 指示 network application 需 IPv6 router 存在后才继续。这实际上意味着 application 想在收到 IPv6 router advertisement message 前等待。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV6_ADDR`","分配给默认 network interface 的本地静态 IPv6 address。"
   ":kconfig:option:`CONFIG_NET_CONFIG_PEER_IPV6_ADDR`","Peer 静态 IPv6 address。这主要可用于 application 可连接到预定义 host 的测试 setups。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_ADDR`","分配给默认 network interface 的本地静态 IPv4 address。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_NETMASK`","分配给 IPv4 address 的静态 IPv4 netmask。"
   ":kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_GW`","分配给默认 network interface 的静态 IPv4 gateway address。"
   ":kconfig:option:`CONFIG_NET_CONFIG_PEER_IPV4_ADDR`","Peer 静态 IPv4 address。这主要可用于 application 可连接到预定义 host 的测试 setups。"

Sample usage
************

若设置 :kconfig:option:`CONFIG_NET_CONFIG_AUTO_INIT`（则 configuration library 自动启用并在 device boot 期间运行。此情况下（library 自动调用 ``net_config_init()``（且 application 无需做任何 network configuration。

若想使用 network configuration library 但不自动初始化（可手动调用 ``net_config_init()``。``flags`` parameter 可用于向 library 提供关于 application 在实际 application 启动前希望有何种 functionality 的 hints。

API Reference
*************

.. doxygengroup:: net_config
