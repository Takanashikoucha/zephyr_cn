.. _net_pkt_processing_stats:

Network Packet Processing Statistics
####################################

.. contents::
    :local:
    :depth: 2

此页面描述如何获取 network stack 内部 network packet processing statistics 的信息。

Network stack 包含基础设施以查明 network packet processing 在发送或接收 path 中耗时多久。有两个 Kconfig options 控制此。对 transmit (TX) path（option 名为 :kconfig:option:`CONFIG_NET_PKT_TXTIME_STATS`（对 receive (RX) path（option 名为 :kconfig:option:`CONFIG_NET_PKT_RXTIME_STATS`。注意对 TX（收集所有类型 network packet statistics。对 RX（仅收集 UDP、TCP 或 raw packet type 的 network packet statistics。

启用这些 options 后（:ref:`net stats <net_shell>` network shell command 将显示此信息：

.. code-block:: console

   Avg TX net_pkt (11484) time 67 us
   Avg RX net_pkt (11474) time 43 us

.. note::

   上述及下方 values 来自 emulated qemu_x86 board 和 UDP traffic

TX time 告知 network packet 从其创建到发送到 network 耗时多久。RX time 告知从其创建到传递给 application 的时间。Values 以微秒为单位。若系统中定义了多个 transmit 或 receive queues（statistics 将按 traffic class 收集。这些由 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` 和 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` options 控制。

若启用 :kconfig:option:`CONFIG_NET_PKT_TXTIME_STATS_DETAIL` 或 :kconfig:option:`CONFIG_NET_PKT_RXTIME_STATS_DETAIL` options（则 network packet 遍历 IP stack 时收集 TX 或 RX network packets 的额外信息。

启用这些 options 后（:ref:`net stats <net_shell>` 将显示此信息：

.. code-block:: console

   Avg TX net_pkt (18902) time 63 us    [0->22->15->23=60 us]
   Avg RX net_pkt (18892) time 42 us    [0->9->6->11->13=39 us]

括号中的 numbers 包含 network packet 从前一 state 到下一 state 耗时多少微秒的信息。

上述 TX 示例中（values 为 **18902** packets 的平均值（包含此信息：

* Packet 由 application 创建（故 time 为 **0**。
* Packet 即将放入 transmit queue。从 network packet 创建到此 state 耗时（此示例中为 **22** 微秒。
* 正确的 TX thread 被调用（且 packet 从 transmit queue 读取。从前一 state 耗时 **15** 微秒。
* Network packet 刚发送（且 network stack 即将释放 network packet。从前一 state 耗时 **23** 微秒。
* 总共平均耗时 **60** 微秒使 network packet 发送完成。值 **63** 也告知相同信息（但以不同方式计算（故因舍入误差有轻微差异。

上述 RX 示例中（values 为 **18892** packets 的平均值（包含此信息：

* Packet 由 network device driver 创建（故 time 为 **0**。
* Packet 即将放入 receive queue。从 network packet 创建到此 state 耗时（此示例中为 **9** 微秒。
* 正确的 RX thread 被调用（且 packet 从 receive queue 读取。从前一 state 耗时 **6** 微秒。
* Network packet 然后被处理并放入正确 socket queue。从前一 state 耗时 **11** 微秒。
* 最后一个值告知从那里到 application 耗时多久。这里
  值为 **13** 微秒。
* 总共平均耗时 **39** 微秒使 network packet 发送完成。值 **42** 也告知相同信息（但以不同方式计算（故因舍入误差有轻微差异。
