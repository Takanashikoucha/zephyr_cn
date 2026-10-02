.. _traffic-class-support:

流量分类
#######################

概述
********

`流量分类 <https://en.wikipedia.org/wiki/Traffic_classification>`_
是一个自动化过程，根据各种参数对计算机网络流量进行分类。对于 Zephyr，
使用 VLAN 优先级码点（PCP）对接收和发送的网络数据包进行分类。
有关 VLAN 优先级的更多信息，请参阅 `IEEE 802.1Q <https://en.wikipedia.org/wiki/IEEE_802.1Q>`_。

默认情况下，Zephyr 中所有网络流量被视为平等。如有需要，
可以使用选项 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` 设置发送队列的数量。
选项 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 可用于设置
接收队列的数量。每个流量类别队列对应一个
特定的内核工作队列（kernel work queue）。每个内核工作队列都有一个优先级。
VLAN 优先级根据 `IEEE 802.1Q 规范`_ 第 I.3 章、第 8.6.6 节表 8-4
以及第 34.5 节表 34-1 中指定的规则，映射到某个流量类别。
每个流量类别又映射到某个内核工作队列。
Rx 和 Tx 的流量类别最大数量均为 8。

有关各种映射如何完成的详细信息，请参阅 :zephyr_file:`subsys/net/ip/net_tc.c`。

.. _IEEE 802.1Q 规范: https://ieeexplore.ieee.org/document/6991462/
