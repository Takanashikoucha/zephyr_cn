.. _net_capture_interface:

Network Packet Capture
######################

.. contents::
    :local:
    :depth: 2

Overview
********

``net_capture`` API 允许用户监控 Zephyr network interfaces 之一的 network traffic 并将该 traffic 发送到 external system 以分析。Monitoring 可手动使用 ``net-shell`` 设置或自动使用 ``net_capture`` API。

Cooked Mode Capture
*******************

若 capturing 已启用并配置（系统将自动捕获给定 network interface 的 network traffic。若想在无 network interface 参与时捕获 network data（则需使用 cooked mode capture API。

Cooked mode capture 中（可捕获任意 network packets（且无需 network interface 参与。例如（PPP 中低层 HDLC packets 可被捕获（因为使用正常 network interface based capture 时 HDLC L2 layer data 被剥离。也可捕获 CANBUS 或 Bluetooth network data（尽管目前 network stack 中无支持捕获它们的。

Cooked mode capture 如此工作：

* 创建 ``any`` network interface。它作为 sink（cooked mode 捕获的 packets 由 cooked mode capture API 写入。
* 在此 ``any`` interface 上附加 ``cooked`` virtual network interface。
* 须用 network interface configuration API 配置 ``cooked`` interface 以捕获特定 L2 packet 类型。
* 使用 cooked mode capture API 时（caller 须指定捕获 data 的 layer 2 protocol 类型。Cooked mode capture API 然后能确定收到此类 L2 packet 时捕获什么。
* 然后设置 network packet capturing infrastructure（使 ``cooked`` interface 标记为 captured network interface。通过 ``any`` interface 由 ``cooked`` interface 收到的 packets 然后自动放到 capture IP tunnel 并发送到 remote host 以分析。

例如（在 sample capture application 中（创建这些 network interfaces：

.. code-block:: c

	Interface any (0x808ab3c) (Dummy) [1]
	================================
	Virtual interfaces attached to this : 2
	Device    : NET_ANY (0x80849a4)

	Interface cooked (0x808ac94) (Virtual) [2]
	==================================
	Virtual name : Cooked mode capture
	Attached  : 1 (Dummy / 0x808ab3c)
	Device    : NET_COOKED (0x808497c)

	Interface eth0 (0x808adec) (Ethernet) [3]
	===================================
	Virtual interfaces attached to this : 4
	Device    : zeth0 (0x80849b8)
	IPv6 unicast addresses (max 4):
	     fe80::5eff:fe00:53e6 autoconf preferred infinite
	     2001:db8::1 manual preferred infinite
	IPv4 unicast addresses (max 2):
	     192.0.2.1/255.255.255.0 overridable preferred infinite

	Interface net0 (0x808af44) (Virtual) [4]
	==================================
	Virtual name : Capture tunnel
	Attached  : 3 (Ethernet / 0x808adec)
	Device    : IP_TUNNEL0 (0x8084990)
	IPv6 unicast addresses (max 4):
	     2001:db8:200::1 manual preferred infinite
	     fe80::efed:6dff:fef2:b1df autoconf preferred infinite
	     fe80::56da:1eff:fe5e:bc02 autoconf preferred infinite

此示例中（``192.0.2.2`` 为终止 tunnel 的 host 的 outer end point 的 address。Zephyr 用此 address 选择用于 tunnel 的 internal interface。此示例中为 interface 3。

Interface 2 为运行在 interface 1 之上的 virtual interface。Cooked 捕获的 packets 由 capture API 写入 sink interface 1。Packets 传播到 interface 2（因其链接到第一个 interface。``net capture enable 2`` net-shell 命令将使发送到 interface 2 的 packets 写入 capture interface 4（其然后 capsulates packets 并通过 Ethernet interface 3 通过 tunnel 发送到 peer。

若在 sample :zephyr_file:`samples/net/capture/overlay-tunnel.conf` 文件中更改 addresses（上述 IP addresses 可能改变。

Sample usage
************

参见 :zephyr:code-sample:`net-capture` sample application 和 :ref:`network_monitoring` 以了解细节。


API Reference
*************

.. doxygengroup:: net_capture
