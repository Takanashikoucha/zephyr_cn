.. _vlan_interface:

虚拟局域网（VLAN）支持
##########################

.. contents::
    :local:
    :depth: 2

概述
********

`虚拟局域网 <https://wikipedia.org/wiki/Virtual_LAN>`_（VLAN）是
数据链路层（OSI 第 2 层）上划分并隔离的计算机网络。
对于以太网，这指的是
`IEEE 802.1Q <https://en.wikipedia.org/wiki/IEEE_802.1Q>`_。

在 Zephyr 中，每个单独的 VLAN 都被建模为一个虚拟网络接口。
这意味着存在一个对应系统中真实物理以太网端口的以太网网络接口。
为每个 VLAN 创建一个虚拟网络接口，该虚拟网络接口连接到
真实网络接口。这与 Linux 实现 VLAN 的方式类似。
*eth0* 是真实网络接口，*vlan0* 是
运行在 *eth0* 之上的虚拟网络接口。

VLAN 支持必须在编译时通过设置选项
:kconfig:option:`CONFIG_NET_VLAN` 和 :kconfig:option:`CONFIG_NET_VLAN_COUNT` 来启用，后者应反映
系统中将有多少个网络接口。例如，如果有一个
不带 VLAN 支持的网络接口和两个带 VLAN 支持的网络接口，
则 :kconfig:option:`CONFIG_NET_VLAN_COUNT` 选项应设置为 3。

即使 VLAN 已在 :file:`prj.conf` 文件中启用，VLAN 仍需
在运行时由应用激活。VLAN API 提供了一个
:c:func:`net_eth_vlan_enable` 函数来实现这一点。应用需要
将该函数参数设置为网络接口和所需的 VLAN 标签。
可以使用
:c:func:`net_eth_vlan_disable` 函数禁用
特定网络接口的 VLAN 标记。应用需要
自行配置 VLAN 网络接口，例如设置 IP 地址等。

有关 API 用法示例，还请参阅 :zephyr:code-sample:`VLAN 示例应用 <vlan>`。
该示例应用的源代码位于
:zephyr_file:`samples/net/ethernet/vlan`。

net-shell 模块包含 *net vlan add* 和 *net vlan del* 命令，
可用于启用或禁用特定网络接口的 VLAN 标签。

有关以太网 VLAN 的更多信息，请参阅 `IEEE 802.1Q 规范`_。

.. _IEEE 802.1Q 规范: https://ieeexplore.ieee.org/document/6991462/

API 参考
*************

.. doxygengroup:: vlan_api
