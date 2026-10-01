.. _vlan_interface:

Virtual LAN (VLAN) Support
##########################

.. contents::
    :local:
    :depth: 2

Overview
********

`Virtual LAN <https://wikipedia.org/wiki/Virtual_LAN>`_（VLAN）为 data link layer（OSI layer 2）上分区和隔离的 computer network。对 ethernet network 这指 `IEEE 802.1Q <https://en.wikipedia.org/wiki/IEEE_802.1Q>`_

在 Zephyr 中（每个独立 VLAN 建模为 virtual network interface。这意味着有对应系统中真实物理 ethernet port 的 ethernet network interface。为每个 VLAN 创建 virtual network interface（且此 virtual network interface 连接到 real network interface。这与 Linux 实现 VLANs 的方式类似。*eth0* 为 real network interface（*vlan0* 为运行在 *eth0* 之上的 virtual network interface。

VLAN 支持须通过设置 :kconfig:option:`CONFIG_NET_VLAN` 和 :kconfig:option:`CONFIG_NET_VLAN_COUNT` option 在 compile time 启用（以反映系统中将有多少 network interfaces。例如（若有一个无 VLAN 支持的 network interface（两个有 VLAN 支持的（:kconfig:option:`CONFIG_NET_VLAN_COUNT` option 应设为 3。

即使 VLAN 在 :file:`prj.conf` file 中启用（VLAN 仍需 application 在 runtime 激活。VLAN API 提供 :c:func:`net_eth_vlan_enable` function 以执行此操作。Application 须将 network interface 和期望 VLAN tag 作为 parameter 传给该 function。给定 network interface 的 VLAN tagging 可用 :c:func:`net_eth_vlan_disable` function 禁用。Application 须自行配置 VLAN network interface（如设置 IP address 等。

API 使用示例参见 :zephyr:code-sample:`VLAN sample application <vlan>`。该 sample application 的源代码可在 :zephyr_file:`samples/net/ethernet/vlan` 找到。

Net-shell module 包含 *net vlan add* 和 *net vlan del* commands（可用于启用或禁用给定 network interface 的 VLAN tags。

ethernet VLANs 更多信息参见 `IEEE 802.1Q spec`_。

.. _IEEE 802.1Q spec: https://ieeexplore.ieee.org/document/6991462/

API Reference
*************

.. doxygengroup:: vlan_api
