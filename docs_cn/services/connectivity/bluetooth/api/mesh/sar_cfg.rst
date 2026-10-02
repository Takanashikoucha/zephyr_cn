.. _bluetooth_mesh_sar_cfg:

分段与重组（SAR）
#################################

分段与重组（SAR）提供了一种在 mesh 网络中处理较大上层传输层消息的方式，其目的是提升 Bluetooth Mesh 的吞吐量。分段与重组机制由较低传输层使用。

较低传输层定义了如何将上层传输层 PDU 分段并重组为多个 Lower Transport PDU，并将其发送到对等设备的较低传输层。如果 Upper Transport PDU 能够容纳，则在一个 Lower Transport PDU 中发送。对于无法容纳在单个 Lower Transport PDU 中的较长报文，较低传输层执行分段，将 Upper Transport PDU 拆分为多个分段。

接收设备上的较低传输层在将报文向上传递到协议栈之前，会将各分段重组为单个 Upper Transport PDU。分段消息的投递由接收节点的较低传输层进行确认，而未分段消息的投递则不进行确认。不过，能够容纳在单个 Lower Transport PDU 中的 Upper Transport PDU 也可以作为单分段的分段消息发送，此时需要较低传输层进行确认。设置 ``send rel`` 标志（参见 :c:struct:`bt_mesh_msg_ctx`）以使用可靠消息传输，并对单分段的分段消息进行确认。

传输层能够使用其 SAR 机制传输多达 32 个分段，最大消息（PDU）大小为 384 字节。要为 Bluetooth Mesh 协议栈配置消息大小，请使用以下 Kconfig 选项：

* :kconfig:option:`CONFIG_BT_MESH_RX_SEG_MAX` 用于设置接收消息中的最大分段数。
* :kconfig:option:`CONFIG_BT_MESH_TX_SEG_MAX` 用于设置发送消息中的最大分段数。

Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_TX_SEG_MSG_COUNT` 和 :kconfig:option:`CONFIG_BT_MESH_RX_SEG_MSG_COUNT` 定义了可以同时处理多少条发送和接收的分段消息。当向同一目的地发送多条分段消息时，这些消息会被排队并逐条发送。

接收和发送的分段消息共享同一个用于分配其分段的池。该池的大小通过 :kconfig:option:`CONFIG_BT_MESH_SEG_BUFS` Kconfig 选项配置。接收和发送消息都在事务开始时分配分段。发送的分段消息在其分段被接收方确认后逐个释放这些分段，而接收消息则在该消息完全接收后首先释放这些分段。在定义缓冲区大小时请牢记这一点。

SAR 不会为每个分段在访问层负载上增加额外开销。

分段与重组（SAR）配置模型
******************************************************

从 Bluetooth Mesh 协议规范 1.1 版本开始，可以通过 SAR 配置模型在 mesh 网络上配置 SAR 行为，例如间隔、定时器和重传计数器：

* :ref:`bluetooth_mesh_sar_cfg_cli`
* :ref:`bluetooth_mesh_sar_cfg_srv`

无论节点上是否存在 SAR 配置服务器，以下 SAR 行为均适用。

分段的传输之间以分段传输间隔分隔（参见 `SAR Segment Interval Step`_ 状态）。可用于分段与重组的其他可配置时间间隔和延迟包括：

* 单播重传之间的间隔（参见状态 `SAR Unicast Retransmissions Interval Step`_ 和 `SAR Unicast Retransmissions Interval Increment`_）。
* 组播重传之间的间隔（参见 `SAR Multicast Retransmissions Interval Step`_ 状态）。
* 分段接收间隔（参见 `SAR Receiver Segment Interval Step`_ 状态）。
* 确认延迟增量（参见 `SAR Acknowledgment Delay Increment`_ 状态）。

当最后一个被标记为未确认的分段被传输时，较低传输层启动一个重传定时器。SAR 单播重传定时器的初始值取决于该消息 TTL 字段的值。如果 TTL 字段值大于 ``0``，则定时器的初始值按以下公式设置：

.. math::

   unicast~retransmissions~interval~step + unicast~retransmissions~interval~increment \times (TTL - 1)


如果 TTL 字段值为 ``0``，定时器的初始值被设置为单播重传间隔步长。

SAR 组播重传定时器的初始值被设置为组播重传间隔。

当较低传输层收到一个消息分段时，它启动一个 SAR 丢弃定时器。丢弃定时器表示较低传输层在丢弃该分段所属的分段消息之前等待多长时间。SAR 丢弃定时器的初始值是由 `SAR Discard Timeout`_ 状态指示的丢弃超时值。

SAR 确认定时器保存的是在收到一个分段后、发送 Segment Acknowledgment 消息之前的时间。SAR 确认定时器的初始值使用以下公式计算：

.. math::

   min(SegN + 0.5 , acknowledgment~delay~increment) \times segment~reception~interval


``SegN`` 字段的值标识该 Upper Transport PDU 被分段的总段数。

有四个计数器与 SAR 行为相关：

* 两个单播重传计数（参见 `SAR Unicast Retransmissions Count`_ 状态和 `SAR Unicast Retransmissions Without Progress Count`_ 状态）
* 组播重传计数（参见 `SAR Multicast Retransmissions Count`_ 状态）
* 确认重传计数（参见 `SAR Acknowledgment Retransmissions Count`_ 状态）

如果传输中的分段数高于 `SAR Segments Threshold`_ 状态的值，则 Segment Acknowledgment 消息会使用 `SAR Acknowledgment Retransmissions Count`_ 状态的值进行重传。

.. _bt_mesh_sar_cfg_states:

SAR 状态
**********

有两个与分段与重组相关的状态：

* SAR 发射器状态
* SAR 接收器状态

SAR 发射器状态是一个复合状态，用于控制分段消息传输的数量和时序。它包括以下状态：

* SAR Segment Interval Step
* SAR Unicast Retransmissions Count
* SAR Unicast Retransmissions Without Progress Count
* SAR Unicast Retransmissions Interval Step
* SAR Unicast Retransmissions Interval Increment
* SAR Multicast Retransmissions Count
* SAR Multicast Retransmissions Interval Step

SAR 接收器状态是一个复合状态，用于控制 Segment Acknowledgment 传输的数量和时序，以及分段消息重组的丢弃。它包括以下状态：

* SAR Segments Threshold
* SAR Discard Timeout
* SAR Acknowledgment Delay Increment
* SAR Acknowledgment Retransmissions Count
* SAR Receiver Segment Interval Step

SAR Segment Interval Step
=========================

SAR Segment Interval Step 状态保存一个值，用于控制分段消息各分段传输之间的间隔。该间隔以毫秒为单位测量。

使用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_SEG_INT_STEP` Kconfig 选项设置默认值。分段传输间隔随后使用以下公式计算：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_SEG\_INT\_STEP} + 1) \times 10~\text{ms}


SAR Unicast Retransmissions Count
=================================

SAR Unicast Retransmissions Count 保存一个值，用于定义向单播目的地重传分段消息的最大次数。使用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_COUNT` Kconfig 选项为该状态设置默认值。

SAR Unicast Retransmissions Without Progress Count
==================================================

该状态保存一个值，用于定义向单播地址重传分段消息的最大次数：如果在超时期间未收到任何确认，或者收到了包含已确认分段的确认，则会发送该次数的重传。使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_WITHOUT_PROG_COUNT` 设置最大重传次数。

SAR Unicast Retransmissions Interval Step
========================================

该状态的值控制用于延迟向单播地址重传未确认分段所使用的间隔步长。该间隔步长以毫秒为单位测量。

使用 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_STEP` Kconfig 选项设置默认值。该值随后用于使用以下公式计算间隔步长：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_UNICAST\_RETRANS\_INT\_STEP} + 1) \times 25~\text{ms}


SAR Unicast Retransmissions Interval Increment
=============================================

SAR Unicast Retransmissions Interval Increment 保存一个值，用于控制用于延迟向单播地址重传未确认分段所使用的间隔增量。该增量以毫秒为单位测量。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_INC` 设置默认值。Kconfig 选项值用于使用以下公式计算增量：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_UNICAST\_RETRANS\_INT\_INC} + 1) \times 25~\text{ms}


SAR Multicast Retransmissions Count
===================================

该状态保存一个值，用于控制向组播地址重传分段消息的总次数。使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_COUNT` 设置总重传次数。

SAR Multicast Retransmissions Interval Step
==========================================

该状态保存一个值，用于控制向组播地址重传分段消息中所有分段之间的间隔。该间隔以毫秒为单位测量。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_INT` 设置默认值，该值用于使用以下公式计算间隔：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_TX\_MULTICAST\_RETRANS\_INT} + 1) \times 25~\text{ms}


SAR Discard Timeout
==================

该状态的值定义了较低传输层在收到分段消息的分段后、丢弃该分段消息之前等待的时间（以秒为单位）。使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_DISCARD_TIMEOUT` 设置默认值。丢弃超时将使用以下公式计算：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_RX\_DISCARD\_TIMEOUT} + 1) \times 5~\text{seconds}


SAR Acknowledgment Delay Increment
=================================

该状态保存一个值，用于控制在收到新分段后延迟发送确认消息所使用间隔的延迟增量。该增量以分段数为单位测量。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_DELAY_INC` 设置默认值。增量值计算为 :math:`\verb|CONFIG_BT_MESH_SAR_RX_ACK_DELAY_INC| + 1.5`。

SAR Segments Threshold
=====================

SAR Segments Threshold 状态保存一个值，用于定义确认重传的分段数阈值。使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_THRESHOLD` 设置该阈值。

当分段消息的分段数超过该阈值时，协议栈将额外将每条确认消息重传 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT` 值所给定的次数。

SAR Acknowledgment Retransmissions Count
=======================================

SAR Acknowledgment Retransmissions Count 状态控制较低传输层发送的 Segment Acknowledgment 消息的重传次数。它给出当分段消息中分段的大小超过 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_THRESHOLD` 值时，协议栈将额外发送的确认消息总重传次数。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT` 为该状态设置默认值。Segment Acknowledgment 消息的最大传输次数为 :math:`\verb|CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT| + 1`。

SAR Receiver Segment Interval Step
=================================

SAR Receiver Segment Interval Step 定义了用于在收到新分段后延迟发送确认消息的分段接收间隔步长。该间隔以毫秒为单位测量。

使用 Kconfig 选项 :kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_INT_STEP` 设置默认值，并使用以下公式计算间隔：

.. math::

   (\mathtt{CONFIG\_BT\_MESH\_SAR\_RX\_SEG\_INT\_STEP} + 1) \times 10~\text{ms}
