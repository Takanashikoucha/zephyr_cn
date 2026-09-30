.. _can_api:

CAN
Controller
##############

.. contents::
   :local:
   :depth:
   2

Overview
********

Controller
Area
Network
是
一
个
两
线
serial
bus
由
Bosch
CAN
Specification、
Bosch
CAN
with
Flexible
Data-Rate
specification
和
ISO
11898-1:2003
标准
指定。
CAN
主要
以
其
在
automotive
domain
中
的
应用
著称。
然而，
它
也
用
于
home
和
industrial
automation
以及
其他
products。

.. warning::

   CAN
   controllers
   只
   能
   在
   bus
   处于
   idle
   （recessive）
   state
   至少
   11
   recessive
   bits
   时
   初始化。
   因此
   你
   必须
   确保
   CAN
   RX
   是
   high，
   至少
   短暂
   时间。
   这
   对
   loopback
   mode
   也
   是
   必需
   的。

ISO
11898-1:2003
中
定义
的
bit-timing
看起来
像
以下
这样：

.. image::
   timing.svg
   :width:
   40%
   :align:
   center
   :alt:
   CAN
   Timing

一
个
单一
bit
被
分成
四
个
segments。

* Sync_Seg:
  nodes
  在
  Sync_Seg
  的
  edge
  同步。
  它
  始终
  是
  一
  个
  time
  quantum
  长度。

* Prop_Seg:
  bus
  的
  信号
  propagation
  delay
  和
  transceiver
  和
  node
  的
  其他
  delays。

* Phase_Seg1
  和
  Phase_Seg2
  :
  定义
  采样
  点。
  Bit
  在
  Phase_Seg1
  的
  末尾
  被
  采样。


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
.. code-block:: C

  void rx_callback_function(const struct device *dev, struct can_frame *frame, void *user_data)
  {
          ... do something with the frame ...
  }

The following snippet shows how to add a filter with a callback function.
It is the most efficient but also the most critical way to receive messages.
The callback function is called from an interrupt context, which means that the
callback function should be as short as possible and must not block.
Adding callback functions is not allowed from userspace context.

The filter for this example is configured to match the identifier 0x123 exactly.

.. code-block:: C

  const struct can_filter my_filter = {
          .flags = 0U,
          .id = 0x123,
          .mask = CAN_STD_ID_MASK
  };
  int filter_id;
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));

  filter_id = can_add_rx_filter(can_dev, rx_callback_function, callback_arg, &my_filter);
  if (filter_id < 0) {
    LOG_ERR("Unable to add rx filter [%d]", filter_id);
  }

Here an example for :c:func:`can_add_rx_filter_msgq` is shown. With this
function, it is possible to receive frames synchronously. This function can be
called from userspace context.  The size of the message queue should be as big
as the expected backlog.

The filter for this example is configured to match the extended identifier
0x1234567 exactly.

.. code-block:: C

  const struct can_filter my_filter = {
          .flags = CAN_FILTER_IDE,
          .id = 0x1234567,
          .mask = CAN_EXT_ID_MASK
  };
  CAN_MSGQ_DEFINE(my_can_msgq, 2);
  struct can_frame rx_frame;
  int filter_id;
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));

  filter_id = can_add_rx_filter_msgq(can_dev, &my_can_msgq, &my_filter);
  if (filter_id < 0) {
    LOG_ERR("Unable to add rx msgq [%d]", filter_id);
    return;
  }

  while (true) {
    k_msgq_get(&my_can_msgq, &rx_frame, K_FOREVER);
    ... do something with the frame ...
  }

:c:func:`can_remove_rx_filter` removes the given filter.

.. code-block:: C

  can_remove_rx_filter(can_dev, filter_id);

Setting the bitrate
*******************

The bitrate and sampling point is initially set at runtime. To change it from
the application, one can use the :c:func:`can_set_timing` API. The :c:func:`can_calc_timing`
function can calculate timing from a bitrate and sampling point in permille.
The following example sets the bitrate to 250k baud with the sampling point at
87.5%.

.. code-block:: C

  struct can_timing timing;
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));
  int ret;

  ret = can_calc_timing(can_dev, &timing, 250000, 875);
  if (ret > 0) {
    LOG_INF("Sample-Point error: %d", ret);
  }

  if (ret < 0) {
    LOG_ERR("Failed to calc a valid timing");
    return;
  }

  ret = can_stop(can_dev);
  if (ret != 0) {
    LOG_ERR("Failed to stop CAN controller");
  }

  ret = can_set_timing(can_dev, &timing);
  if (ret != 0) {
    LOG_ERR("Failed to set timing");
  }

  ret = can_start(can_dev);
  if (ret != 0) {
    LOG_ERR("Failed to start CAN controller");
  }

A similar API exists for calculating and setting the timing for the data phase for CAN FD capable
controllers. See :c:func:`can_set_timing_data` and :c:func:`can_calc_timing_data`.

SocketCAN
*********

Zephyr additionally supports SocketCAN, a BSD socket implementation of the
Zephyr CAN API.
SocketCAN brings the convenience of the well-known BSD Socket API to
Controller Area Networks. It is compatible with the Linux SocketCAN
implementation, where many other high-level CAN projects build on top.
Note that frames are routed to the network stack instead of passed directly,
which adds some computation and memory overhead.

Samples
*******

We have two ready-to-build samples demonstrating use of the Zephyr CAN API:
:zephyr:code-sample:`Zephyr CAN counter sample <can-counter>` and
:zephyr:code-sample:`SocketCAN sample <socket-can>`.


CAN Controller API Reference
****************************

.. doxygengroup:: can_controller

.. doxygengroup:: can_fake