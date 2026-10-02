.. _net_if_interface:

网络接口
#################

.. contents::
    :local:
    :depth: 2

概述
********

网络接口是将网络设备驱动程序和网络协议栈上层联系在一起的枢纽。所有发送和接收的数据都通过网络接口传输。网络接口无法在运行时创建。一个特殊的链接器节将包含关于它们的信息，该节在链接时填充。

网络接口由 ``NET_DEVICE_INIT()`` 宏创建。对于以太网，应改用名为 ``ETH_NET_DEVICE_INIT()`` 的宏，因为它会在启用 :kconfig:option:`CONFIG_NET_VLAN` 时自动创建 VLAN 接口。这些宏通常用于网络设备驱动程序源代码中。

通过调用 ``net_if_up()`` 可以打开网络接口，通过调用 ``net_if_down()`` 可以关闭。当设备上电时，网络接口默认也会打开。

网络接口可以通过 ``struct net_if *`` 指针或网络接口索引来引用。通过调用 ``net_if_get_by_index()`` 可以从索引解析网络接口，通过调用 ``net_if_get_by_iface()`` 可以从接口指针解析。

.. _net_if_interface_ip_management:

必须为网络设备设置 IP 地址才能使其可连接。在典型的动态网络环境中，IP 地址例如由 DHCPv4 自动设置。但是，如果需要，应用程序可以手动设置设备的 IP 地址。有关执行此操作的函数（如 ``net_if_ipv4_addr_add()``），参见以下 API 文档。

``net_if_get_default()`` 返回*默认*网络接口。此默认接口的含义可以通过 :kconfig:option:`CONFIG_NET_DEFAULT_IF_FIRST` 和 :kconfig:option:`CONFIG_NET_DEFAULT_IF_ETHERNET` 等选项进行配置。有关选择默认网络接口的可用选项，参见 Kconfig 文件 :zephyr_file:`subsys/net/ip/Kconfig`。

发送和接收的网络数据包可以通过网络数据包优先级进行分类。这通常在使用虚拟局域网（VLAN）的以太网中执行。高优先级数据包可以比低优先级数据包更早发送或接收。流量类设置可以通过 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` 和 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 选项进行配置。

如果启用了 :kconfig:option:`CONFIG_NET_PROMISCUOUS_MODE` 并且底层网络技术支持混杂模式，则可以接收网络设备驱动程序能够接收的所有网络数据包。更多细节参见 :ref:`promiscuous_interface` API。

.. _net_if_interface_state_management:

网络接口状态管理
**********************************

Zephyr 区分两种接口状态：管理状态和操作状态，如 RFC 2863 所述。管理状态指示接口是否打开或关闭。此状态由 :c:enumerator:`NET_IF_UP` 标志表示，并由应用程序控制。可以通过调用 :c:func:`net_if_up` 或 :c:func:`net_if_down` 函数来更改。网络驱动程序或 L2 实现不应自行更改管理状态。

然而，将接口启动并不总是意味着接口已准备好发送数据包。因此，实现了表示接口内部状态的操作状态。操作状态在以下任一条件发生时更新：

  * 应用程序启动/关闭接口（管理状态变化）。
  * 驱动程序/L2 通知接口 PHY 状态已变化。
  * 驱动程序/L2 通知接口已加入/离开网络。

PHY 状态由 :c:enumerator:`NET_IF_LOWER_UP` 标志表示，并可用 :c:func:`net_if_carrier_on` 和 :c:func:`net_if_carrier_off` 更改。默认情况下，该标志在新初始化的接口上设置。更改载波状态的事件示例为以太网电缆插入或拔出。

网络关联状态由 :c:enumerator:`NET_IF_DORMANT` 标志表示，并可用 :c:func:`net_if_dormant_on` 和 :c:func:`net_if_dormant_off` 更改。默认情况下，该标志在新初始化的接口上清除。更改休眠状态的事件示例为 Wi-Fi 驱动程序成功连接到接入点。在此场景中，驱动程序应在初始化期间将休眠状态设置为 ON，一旦检测到已连接到 Wi-Fi 网络，休眠状态应设置为 OFF。

接口的操作状态按如下方式更新：

  * ``!net_if_is_admin_up()``

    接口处于 :c:enumerator:`NET_IF_OPER_DOWN`。

  * ``net_if_is_admin_up() && !net_if_is_carrier_ok()``

    接口处于 :c:enumerator:`NET_IF_OPER_DOWN`，或者如果接口是堆叠的（虚拟的），则处于 :c:enumerator:`NET_IF_OPER_LOWERLAYERDOWN`。

  * ``net_if_is_admin_up() && net_if_is_carrier_ok() && net_if_is_dormant()``

    接口处于 :c:enumerator:`NET_IF_OPER_DORMANT`。

  * ``net_if_is_admin_up() && net_if_is_carrier_ok() && !net_if_is_dormant()``

    接口处于 :c:enumerator:`NET_IF_OPER_UP`。

只有当接口进入 :c:enumerator:`NET_IF_OPER_UP` 状态后，接口上才设置 :c:enumerator:`NET_IF_RUNNING` 标志，表示接口已准备好供应用程序使用。

API 参考
*************

.. doxygengroup:: net_if
