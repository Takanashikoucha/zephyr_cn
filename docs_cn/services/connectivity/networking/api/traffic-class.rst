.. _traffic-class-support:

Traffic Classification
#######################

Overview
********

`Traffic classification <https://en.wikipedia.org/wiki/Traffic_classification>`_ 为按各种 parameters 对 computer network traffic 分类的自动化过程。对 Zephyr（用 VLAN priority code point（PCP）对接收和发送的 network packets 分类。VLAN priority 更多信息参见 `IEEE 802.1Q <https://en.wikipedia.org/wiki/IEEE_802.1Q>`_。

默认（Zephyr 中所有 network traffic 平等对待。若需要（可用 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` option 设置 transmit queues 数量。可用 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` option 设置 receive queues 数量。每个 traffic class queue 对应特定 kernel work queue。每个 kernel work queue 有 priority。VLAN priority 按 `IEEE 802.1Q spec`_ chapter I.3、chapter 8.6.6 table 8-4 和 chapter 34.5 table 34-1 中指定的 rules 映射到特定 traffic class。每个 traffic class 进而映射到特定 kernel work queue。Rx 和 Tx 的最大 traffic classes 数为 8。

各种 mappings 如何执行的细节参见 :zephyr_file:`subsys/net/ip/net_tc.c`。

.. _IEEE 802.1Q spec: https://ieeexplore.ieee.org/document/6991462/
