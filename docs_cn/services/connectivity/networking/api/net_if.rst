.. _net_if_interface:

Network Interface
#################

.. contents::
    :local:
    :depth: 2

Overview
********

Network interface 是将 network device drivers 和 network stack 上层联系在一起的 nexus。所有发送和接收的 data 通过 network interface 传输。Network interfaces 无法在 runtime 创建。专用 linker section 将包含关于它们的信息（且该 section 在 linking 时填充。

Network interfaces 由 ``NET_DEVICE_INIT()`` macro 创建。对 Ethernet network（应改用名为 ``ETH_NET_DEVICE_INIT()`` 的 macro（其若启用 :kconfig:option:`CONFIG_NET_VLAN` 将自动创建 VLAN interfaces。这些 macros 通常用于 network device driver 源代码中。

Network interface 可调用 ``net_if_up()`` 开启（调用 ``net_if_down()`` 关闭。Device 上电时（network interface 默认也开启。

Network interfaces 可用 ``struct net_if *`` pointer 或 network interface index 引用。Network interface 可调用 ``net_if_get_by_index()`` 从其 index 解析（调用 ``net_if_get_by_iface()`` 从 interface pointer 解析。

.. _net_if_interface_ip_management:

Network devices 的 IP address 须设置以使它们可连接。在典型动态 network 环境中（IP addresses 自动由例如 DHCPv4 设置。然而若需要（application 可手动设置 device 的 IP address。执行此操作的 functions（如 ``net_if_ipv4_addr_add()``）参见以下 API 文档。

``net_if_get_default()`` 返回*默认* network interface。此默认 interface 的含义可通过 :kconfig:option:`CONFIG_NET_DEFAULT_IF_FIRST` 和 :kconfig:option:`CONFIG_NET_DEFAULT_IF_ETHERNET` 等 options 配置。选择默认 network interface 的可用 options 参见 Kconfig file :zephyr_file:`subsys/net/ip/Kconfig`。

传输和接收的 network packets 可用 network packet priority 分类。这通常在 Ethernet networks 中使用 virtual LANs（VLANs）时执行。高优先级 packets 可比低优先级 packets 更早发送或接收。Traffic class setup 可用 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` 和 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` options 配置。

若启用 :kconfig:option:`CONFIG_NET_PROMISCUOUS_MODE`（且底层 network technology 支持 promiscuous mode（则可能接收 network device driver 能接收的所有 network packets。更多细节参见 :ref:`promiscuous_interface` API。

.. _net_if_interface_state_management:

Network interface state management
**********************************

Zephyr 区分两种 interface states：administrative state 和 operational state（如 RFC 2863 所述。Administrative state 指示 interface 是否开启或关闭。此 state 由 :c:enumerator:`NET_IF_UP` flag 表示（并由 application 控制。其可调用 :c:func:`net_if_up` 或 :c:func:`net_if_down` functions 更改。Network drivers 或 L2 implementations 不应自行更改 administrative state。

然而将 interface 启动不总意味着 interface 准备好传输 packets。因此（实现了表示 interface 内部 status 的 operational state。Operational state 在以下任一条件发生时更新：

  * Application 启动/关闭 interface（administrative state 变化）。
  * Driver/L2 通知 interface PHY status 已变化。
  * Driver/L2 通知 interface 已加入/离开 network。

PHY status 由 :c:enumerator:`NET_IF_LOWER_UP` flag 表示（并可用 :c:func:`net_if_carrier_on` 和 :c:func:`net_if_carrier_off` 更改。默认（flag 在新初始化的 interface 上设置。更改 carrier state 的 event 示例为 Ethernet cable 插入或拔出。

Network association status 由 :c:enumerator:`NET_IF_DORMANT` flag 表示（并可用 :c:func:`net_if_dormant_on` 和 :c:func:`net_if_dormant_off` 更改。默认（flag 在新初始化的 interface 上清除。更改 dormant state 的 event 示例为 Wi-Fi driver 成功连接到 access point。此场景中（driver 应在初始化期间将 dormant state 设为 ON（且一旦检测到已连接到 Wi-Fi network（dormant state 应设为 OFF。

Interface 的 operational state 按如下更新：

  * ``!net_if_is_admin_up()``

    Interface 处于 :c:enumerator:`NET_IF_OPER_DOWN`。

  * ``net_if_is_admin_up() && !net_if_is_carrier_ok()``

    Interface 处于 :c:enumerator:`NET_IF_OPER_DOWN` 或（若 interface 为 stacked（virtual）（:c:enumerator:`NET_IF_OPER_LOWERLAYERDOWN`。

  * ``net_if_is_admin_up() && net_if_is_carrier_ok() && net_if_is_dormant()``

    Interface 处于 :c:enumerator:`NET_IF_OPER_DORMANT`。

  * ``net_if_is_admin_up() && net_if_is_carrier_ok() && !net_if_is_dormant()``

    Interface 处于 :c:enumerator:`NET_IF_OPER_UP`。

仅当 interface 进入 :c:enumerator:`NET_IF_OPER_UP` state 后（interface 上设置 :c:enumerator:`NET_IF_RUNNING` flag（指示 interface 准备好供 application 使用。

API Reference
*************

.. doxygengroup:: net_if
