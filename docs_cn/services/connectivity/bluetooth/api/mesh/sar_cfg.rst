.. _bluetooth_mesh_sar_cfg:

Segmentation and reassembly (SAR)
#################################

Segmentation and reassembly (SAR) 提供在 mesh network 中处理较大 upper transport layer messages 的方式（以增强 Bluetooth Mesh throughput。Segmentation and reassembly 机制由 lower transport layer 使用。

Lower transport layer 定义 upper transport layer PDUs 如何被 segmentation 和 reassembly 为多个 Lower Transport PDUs（并将其发送到 peer device 的 lower transport layer。若 Upper Transport PDU 适配（则在单个 Lower Transport PDU 中发送。对于不适配单个 Lower Transport PDU 的较长 packets（lower transport layer 执行 segmentation（将 Upper Transport PDU 分割为多个 segments。

接收 device 上的 lower transport layer 在将其传递到 stack 上层之前将 segments reassembly 为单个 Upper Transport PDU。Segmented message 的 delivery 由接收 node 的 lower transport layer 确认（而 unsegmented message delivery 不确认。然而（适配单个 Lower Transport PDU 的 Upper Transport PDU 也可作为 single-segment segmented message 发送（当需要 lower transport layer 确认时。设置 ``send rel`` flag（参见 :c:struct:`bt_mesh_msg_ctx`）以使用可靠 message transmission 并确认 single-segment segmented messages。

Transport layer 能用其 SAR 机制传输最多 32 segments（最大 message（PDU）size 为 384 octets。要为 Bluetooth Mesh stack 配置 message size（使用以下 Kconfig options：

* :kconfig:option:`CONFIG_BT_MESH_RX_SEG_MAX` 设置 incoming message 中 segments 的最大数。
* :kconfig:option:`CONFIG_BT_MESH_TX_SEG_MAX` 设置 outgoing message 中 segments 的最大数。

Kconfig options :kconfig:option:`CONFIG_BT_MESH_TX_SEG_MSG_COUNT` 和 :kconfig:option:`CONFIG_BT_MESH_RX_SEG_MSG_COUNT` 定义可同时处理多少个 outgoing 和 incoming segmented messages。当向同一 destination 发送多个 segmented messages 时（messages 被 queued 且一次发送一个。

Incoming 和 outgoing segmented messages 共享同一 pool 以分配其 segments。此 pool size 通过 :kconfig:option:`CONFIG_BT_MESH_SEG_BUFS` Kconfig option 配置。Incoming 和 outgoing messages 在 transaction 开始时分配 segments。Outgoing segmented message 在 segments 被 receiver 确认后逐个释放（而 incoming message 在 message 完全接收后首先释放 segments。定义 buffers 大小时请记住此点。

SAR 不对每个 segment 的 access layer payload 施加额外 overhead。

Segmentation and reassembly (SAR) Configuration models
******************************************************

自 Bluetooth Mesh Protocol Specification version 1.1 起（可使用 SAR Configuration models 通过 mesh network 配置 SAR 行为（如 intervals、timers 和 retransmission counters：

* :ref:`bluetooth_mesh_sar_cfg_cli`
* :ref:`bluetooth_mesh_sar_cfg_srv`

无论 node 上是否存在 SAR Configuration Server（以下 SAR 行为均适用。

Segments 的 transmission 由 segment transmission interval 分隔（参见 `SAR Segment Interval Step`_ state。可用于 segmentation and reassembly 的其他可配置 time intervals 和 delays：

* Unicast retransmissions 之间的 interval（参见 states `SAR Unicast Retransmissions Interval Step`_ 和 `SAR Unicast Retransmissions Interval Increment`_）。
* Multicast retransmissions 之间的 interval（参见 `SAR Multicast Retransmissions Interval Step`_ state）。
* Segment reception interval（参见 `SAR Receiver Segment Interval Step`_ state）。
* Acknowledgment delay increment（参见 `SAR Acknowledgment Delay Increment`_ state）。

当标记为 unacknowledged 的最后一个 segment 被传输时（lower transport layer 启动 retransmissions timer。SAR Unicast Retransmissions timer 的初始值取决于 message 的 TTL field 值。若 TTL field 值大于 ``0``（timer 初始值按以下公式设置：

.. math::

   unicast~retransmissions~interval~step + unicast~retransmissions~interval~increment \times (TTL - 1)


若 TTL field 值为 ``0``（timer 初始值设为 unicast retransmissions interval step。

SAR Multicast Retransmissions timer 的初始值设为 multicast retransmissions interval。

当 lower transport layer 接收 message segment 时（启动 SAR Discard timer。Discard timer 指示 lower transport layer 在丢弃 segment 所属的 segmented message 前等待多久。SAR Discard timer 的初始值为 `SAR Discard Timeout`_ state 指示的 discard timeout 值。

SAR Acknowledgment timer 持有在收到 segment 后发送 Segment Acknowledgment message 前的时间。SAR Acknowledgment timer 的初始值用以下公式计算：

.. math::

   min(SegN + 0.5 , acknowledgment~delay~increment) \times segment~reception~interval


``SegN`` field 值标识 Upper Transport PDU 被分割成的 segments 总数。

四个 counters 与 SAR 行为相关：

* 两个 unicast retransmissions counts（参见 `SAR Unicast Retransmissions Count`_ state 和 `SAR Unicast Retransmissions Without Progress Count`_ state）
* Multicast retransmissions count（参见 `SAR Multicast Retransmissions Count`_ state）
* Acknowledgment retransmissions count（参见 `SAR Acknowledgment Retransmissions Count`_ state）

若 transmission 中 segments 数高于 `SAR Segments Threshold`_ state 值（Segment Acknowledgment messages 用 `SAR Acknowledgment Retransmissions Count`_ state 值 retransmit。

.. _bt_mesh_sar_cfg_states:

SAR states
**********

有两个与 segmentation and reassembly 相关的定义 states：

* SAR Transmitter state
* SAR Receiver state

SAR Transmitter state 是控制 segmented messages transmission 的数量和时序的 composite state。它包括以下 states：

* SAR Segment Interval Step
* SAR Unicast Retransmissions Count
* SAR Unicast Retransmissions Without Progress Count
* SAR Unicast Retransmissions Interval Step
* SAR Unicast Retransmissions Interval Increment
* SAR Multicast Retransmissions Count
* SAR Multicast Retransmissions Interval Step

SAR Receiver state 是控制 Segment Acknowledgment transmissions 的数量和时序以及 segmented message reassembly 丢弃的 composite state。它包括以下 states：

* SAR Segments Threshold
* SAR Discard Timeout
* SAR Acknowledgment Delay Increment
* SAR Acknowledgment Retransmissions Count
* SAR Receiver Segment Interval Step

SAR Segment Interval Step
=========================

SAR Segment Interval Step state 持有控制 segmented message 的 segments transmission 之间 interval 的值。Interval 以毫秒测量。

用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_SEG_INT_STEP` Kconfig option 设置默认值。Segment transmission interval 然后用以下公式计算：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_SEG\_INT\_STEP} + 1) \times 10~\text{ms}


SAR Unicast Retransmissions Count
=================================

SAR Unicast Retransmissions Count 持有定义向 unicast destination 的 segmented message 最大 retransmissions 数的值。用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_COUNT` Kconfig option 设置此 state 的默认值。

SAR Unicast Retransmissions Without Progress Count
==================================================

此 state 持有定义向 unicast address 的 segmented message 最大 retransmissions 数的值（若在 timeout 期间未收到 acknowledgment 或收到已确认 segments 的 acknowledgment 则发送。用 Kconfig option :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_WITHOUT_PROG_COUNT` 设置最大 retransmissions 数。

SAR Unicast Retransmissions Interval Step
=========================================

此 state 的值控制用于延迟向 unicast address 的 unacknowledged segments retransmissions 的 interval step。Interval step 以毫秒测量。

用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_STEP` Kconfig option 设置默认值。此值然后用以下公式计算 interval step：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_UNICAST\_RETRANS\_INT\_STEP} + 1) \times 25~\text{ms}


SAR Unicast Retransmissions Interval Increment
==============================================

SAR Unicast Retransmissions Interval Increment 持有控制用于延迟向 unicast address 的 unacknowledged segments retransmissions 的 interval increment 的值。Increment 以毫秒测量。

用 Kconfig option :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_INC` 设置默认值。Kconfig option 值用以下公式计算 increment：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_UNICAST\_RETRANS\_INT\_INC} + 1) \times 25~\text{ms}


SAR Multicast Retransmissions Count
===================================

此 state 持有控制向 multicast address 的 segmented message 总 retransmissions 数的值。用 Kconfig option :kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_COUNT` 设置总 retransmissions 数。

SAR Multicast Retransmissions Interval Step
===========================================

此 state 持有控制向 multicast address 的 segmented message 所有 segments retransmissions 之间 interval 的值。Interval 以毫秒测量。

用 Kconfig option :kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_INT` 设置用以下公式计算 interval 的默认值：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_MULTICAST\_RETRANS\_INT} + 1) \times 25~\text{ms}


SAR Discard Timeout
===================

此 state 的值定义 lower transport layer 在收到 segmented message 的 segments 后丢弃该 segmented message 前等待的秒数。用 Kconfig option :kconfig:option:`CONFIG_BT_MESH_SAR_RX_DISCARD_TIMEOUT` 设置默认值。Discard timeout 用以下公式计算：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_RX\_DISCARD\_TIMEOUT} + 1) \times 5~\text{seconds}


SAR Acknowledgment Delay Increment
==================================

此 state 持有控制收到新 segment 后延迟 acknowledgment message transmission 的 interval 的 delay increment 的值。Increment 以 segments 测量。

用 Kconfig option :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_DELAY_INC` 设置默认值。Increment 值计算为 :math:`\verb|CONFIG_BT_MESH_SAR_RX_ACK_DELAY_INC| + 1.5`。

SAR Segments Threshold
======================

SAR Segments Threshold state 持有定义 acknowledgment retransmissions 的 segmented message segments 数阈值。用 Kconfig option :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_THRESHOLD` 设置阈值。

当 segmented message 的 segments 数高于此阈值时（stack 将额外 retransmit 每个 acknowledgment message :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT` 值给出的次数。

SAR Acknowledgment Retransmissions Count
========================================

SAR Acknowledgment Retransmissions Count state 控制 lower transport layer 发送的 Segment Acknowledgment messages 的 retransmissions 数。它给出当 segmented message 中 segments size 高于 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_THRESHOLD` 值时 stack 将额外发送的 acknowledgment message 总 retransmissions 数。

用 Kconfig option :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT` 设置此 state 的默认值。Segment Acknowledgment message 的最大 transmission 数为 :math:`\verb|CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT| + 1`。

SAR Receiver Segment Interval Step
==================================

SAR Receiver Segment Interval Step 定义用于收到新 segment 后延迟 acknowledgment message transmission 的 segments reception interval step。Interval 以毫秒测量。

用 Kconfig option :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_INT_STEP` 设置默认值并用以下公式计算 interval：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_RX\_SEG\_INT\_STEP} + 1) \times 10~\text{ms}
