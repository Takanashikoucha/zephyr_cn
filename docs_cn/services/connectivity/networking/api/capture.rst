.. _net_capture_interface:

网络数据包捕获
######################

.. contents::
    :local:
    :depth: 2

概述
********

``net_capture`` API 允许用户监控 Zephyr 网络接口之一的
网络流量，并将该流量发送到
外部系统进行分析。监控可以
手动使用 ``net-shell`` 设置，也可以使用 ``net_capture`` API 自动设置。

Cooked 模式捕获
*******************

如果捕获已启用并配置，系统将自动捕获
给定网络接口的网络流量。如果希望在
没有网络接口参与的情况下捕获网络数据，则需要使用
cooked 模式捕获 API。

在 cooked 模式捕获中，可以捕获任意网络数据包，
且无需网络接口参与。例如，PPP 中的低层 HDLC
数据包可以被捕获，因为使用
基于普通网络接口的捕获时，HDLC L2 层数据会被剥离。此外，CANBUS 或
Bluetooth 网络数据也可以被捕获，尽管目前
网络协议栈中尚无捕获这些数据的
支持。

cooked 模式捕获的工作方式如下：

* 创建一个 ``any`` 网络接口。它充当一个汇聚点（sink），
  cooked 模式捕获的数据包由 cooked 模式捕获 API 写入该接口。
* 一个 ``cooked`` 虚拟网络接口被附加在该 ``any``
  接口之上。
* 必须使用网络接口配置 API，将 ``cooked`` 接口
  配置为捕获特定 L2 数据包类型。
* 使用 cooked 模式捕获 API 时，调用者必须指定
  所捕获数据的第 2 层协议类型。随后 cooked 模式捕获 API
  就能确定在收到此类 L2 数据包时捕获什么。
* 然后配置网络数据包捕获基础设施，
  将 ``cooked`` 接口标记为被捕获的网络接口。
  通过 ``any`` 接口由 ``cooked`` 接口接收到的
  数据包随后被自动放入捕获 IP 隧道，
  并发送到远程主机进行分析。

例如，在示例捕获应用中，
创建了以下网络接口：

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

在此示例中，``192.0.2.2`` 是
终止该隧道的宿主机的外层端点地址。Zephyr 使用该地址
选择用于隧道的内部接口。在此示例中为接口 3。

接口 2 是运行在接口 1 之上的虚拟接口。
cooked 捕获的数据包由捕获 API 写入汇聚接口 1。
由于接口 2 链接到第一个接口，数据包会
传播到接口 2。``net capture enable 2`` net-shell 命令会使
发送到接口 2 的数据包被写入捕获接口 4，
接口 4 随后封装这些数据包，并通过以太网接口 3 通过隧道
发送到对端。

如果在示例 :zephyr_file:`samples/net/capture/overlay-tunnel.conf` 文件中更改地址，
上述 IP 地址可能会改变。

示例用法
************

参见 :zephyr:code-sample:`net-capture` 示例应用和
:ref:`network_monitoring` 了解详情。


API 参考
*************

.. doxygengroup:: net_capture
