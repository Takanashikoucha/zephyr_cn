.. _can_api:

CAN 控制器
##############

.. contents::
    :local:
    :depth: 2

概述
********

控制器局域网（Controller Area Network，CAN）是一种双绞线串行总线，
由 Bosch CAN 规范、Bosch CAN with Flexible Data-Rate（CAN FD）规范
以及 ISO 11898-1:2003 标准定义。
CAN 最广为人知的应用领域是汽车，但它同样用于家庭与工业自动化及其他产品。

.. warning::

   CAN 控制器只有在总线处于空闲（隐性，recessive）状态且至少持续
   11 个隐性位时才能完成初始化。因此必须确保 CAN RX 引脚至少
   在短时间内为高电平。回环（loopback）模式同样需要满足这一条件。

ISO 11898-1:2003 中定义的位定时（bit-timing）如下图所示：

.. image:: timing.svg
   :width: 40%
   :align: center
   :alt: CAN Timing

单个位（bit）被划分为四个段：

* Sync_Seg（同步段）：节点在 Sync_Seg 的边沿进行同步。它始终为 1 个时间量子（time quantum）长。

* Prop_Seg（传播段）：总线的信号传播延迟，以及收发器和节点的其他延迟。

* Phase_Seg1（相位段 1）和 Phase_Seg2（相位段 2）：定义采样点。位信号在 Phase_Seg1 的末尾被采样。

比特率（bit-rate）由单个时间量子的时长以及上述定义的值计算得出：
一个位的长度等于 Sync_Seg、Prop_Seg、Phase_Seg1 和 Phase_Seg2
四者之和乘以单个时间量子的时长；比特率即为单个位长度的倒数。

位信号在采样点被采样。采样点位于 Phase_Seg1 与 Phase_Seg2 之间，
因此是一个需要用户自行选择的参数。CiA 建议将采样点设置在位的 87.5% 处。

重同步跳转宽度（SJW，resynchronization jump width）定义了采样点
可以移动的时间量子数量；当需要重新同步时，采样点就会发生移动。

时序参数（SJW、比特率和采样点，或者比特率、Prop_Seg、
Phase_Seg1 和 Phase_Seg2）最初从设备树（device-tree）中设置，
并可在运行时通过定时 API（timing API）进行修改。

CAN 使用所谓的标识符（identifier）来识别帧，而不是使用地址（address）
来识别节点。标识符可以是 11 位宽（标准帧或基本帧），
在扩展帧（Extended Frame）的情况下为 29 位。
Zephyr CAN API 同时支持标准标识符和扩展标识符。
一个 CAN 帧以显性（dominant）的帧起始位（Start Of Frame）开始，
其后依次是标识符，这一阶段称为仲裁阶段。
在仲裁阶段，允许发生写冲突，
这些冲突通过"显性位覆盖隐性位"这一事实得到解决。
节点会监控总线，一旦发现自身的发送正在被覆盖，
就会中止本次发送。
这实际上使编号较小的标识符优先于编号较大的标识符。

滤波器（filter）用于允许（白名单）特定节点所关心的标识符；
不匹配任何滤波器的标识符将被忽略。
滤波器可以精确匹配，也可以匹配标识符的指定部分，
这种方法称为屏蔽（masking）。
例如，对于标准标识符设置 11 位全 1、对于扩展标识符设置 29 位全 1
的掩码必须完全匹配；掩码中置零的位在匹配标识符时将被忽略。
大多数 CAN 控制器在硬件中只实现了有限数量的滤波器，
滤波器的数量在 Kconfig 中也受到限制，以节省内存。

发送过程中可能发生错误。如果节点检测到错误帧，
它会用一个错误帧（error-frame）部分覆盖当前的帧。
错误帧可以是错误被动（error passive）或错误主动（error active），
具体取决于控制器的状态。
如果控制器处于错误主动状态，它会发送 6 个连续的显性位，
这违反了填充（stuffing）规则，所有节点都能检测到这一违规；
发送方可以立即重发该帧。

完成初始化的节点可以处于以下状态之一：

* 错误主动（Error-active）
* 错误被动（Error-passive）
* 总线关闭（Bus-off）

初始化后，节点处于错误主动状态。在此状态下，
节点被允许发送主动错误帧、应答帧（ACK）和过载帧。
每个节点都有一个接收错误计数器和一个发送错误计数器。
如果接收错误或发送错误计数器中任一个超过 127，
节点将切换到错误被动状态。
在此状态下，节点不再被允许发送错误主动帧。
如果发送错误计数器进一步增加到 255，节点将切换到总线关闭状态。
在此状态下，节点不允许向总线发送任何显性位。
处于总线关闭状态的节点在接收到 128 次"11 个连续隐性位"之后可以恢复。

你可以在这篇 `CAN Wikipedia 文章 <https://en.wikipedia.org/wiki/CAN_bus>`_
中阅读更多关于 CAN 总线的信息。

Zephyr 支持以下 CAN 特性：

* 标准与扩展标识符
* 带屏蔽（masking）的滤波器
* 回环（Loopback）与静默（Silent）模式
* 远程请求（Remote Request）

发送
*******

以下代码片段展示了如何发送数据。

这个基本示例发送一个标识符为 0x123 的标准帧，
并携带 8 字节数据。如本例所示，将 NULL 作为回调传入时，
发送函数会阻塞，直到帧被发送并至少被另一个节点确认，
或者发生错误为止。超时仅对获取邮箱（mailbox）生效；
一旦分配到发送邮箱，发送就无法取消。

.. code-block:: C

  struct can_frame frame = {
          .flags = 0,
          .id = 0x123,
          .dlc = 8,
          .data = {1,2,3,4,5,6,7,8}
  };
  const struct device *const can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));
  int ret;

  ret = can_send(can_dev, &frame, K_MSEC(100), NULL, NULL);
  if (ret != 0) {
          LOG_ERR("Sending failed [%d]", ret);
  }


此示例展示了如何发送一个扩展标识符为 0x1234567、
携带 2 字节数据的帧。所提供的回调会在消息发送完成
或发生错误时被调用。向超时参数传入 :c:macro:`K_FOREVER`
会使函数阻塞，直到为该帧分配到一个发送邮箱或发生错误为止；
它不会像上面的示例那样阻塞到消息真正发送完成。

.. code-block:: C

  void tx_callback(const struct device *dev, int error, void *user_data)
  {
          char *sender = (char *)user_data;

          if (error != 0) {
                  LOG_ERR("Sending failed [%d]\nSender: %s\n", error, sender);
          }
  }

  int send_function(const struct device *can_dev)
  {
          struct can_frame frame = {
                  .flags = CAN_FRAME_IDE,
                  .id = 0x1234567,
                  .dlc = 2
          };

          frame.data[0] = 1;
          frame.data[1] = 2;

          return can_send(can_dev, &frame, K_FOREVER, tx_callback, "Sender 1");
  }

接收
*********

只有匹配某个滤波器的帧才会被接收。
以下代码片段展示了如何通过添加滤波器来接收帧。

下面是一个用于 :c:func:`can_add_rx_filter` 的接收回调示例，
其用户数据（user data）参数在添加滤波器时传入。

.. code-block:: C

  void rx_callback_function(const struct device *dev, struct can_frame *frame, void *user_data)
  {
          ... do something with the frame ...
  }

以下片段展示了如何添加一个带回调函数的滤波器。
这是接收消息最高效、但也是最关键（最需谨慎）的方式：
回调函数从中断上下文中被调用，
这意味着回调函数应尽可能短，且不得阻塞。
不允许从用户空间（userspace）上下文添加回调函数。

此示例中的滤波器被配置为精确匹配标识符 0x123。

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

下面给出 :c:func:`can_add_rx_filter_msgq` 的示例。
使用这个函数可以同步地接收帧，并且可以从用户空间上下文调用。
消息队列的大小应尽可能大，以匹配预期的积压（backlog）。

此示例中的滤波器被配置为精确匹配扩展标识符 0x1234567。

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

:c:func:`can_remove_rx_filter` 用于移除指定的滤波器。

.. code-block:: C

  can_remove_rx_filter(can_dev, filter_id);

设置比特率
*******************

比特率和采样点最初在运行时设置。
若要从应用中修改它们，可以使用 :c:func:`can_set_timing` API；
:c:func:`can_calc_timing` 函数可以根据比特率和以千分比表示的
采样点计算出定时参数。以下示例将比特率设置为 250k baud，
采样点设置为 87.5%。

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

对于支持 CAN FD 的控制器，存在类似的 API，
用于计算和设置数据阶段的定时参数。
参见 :c:func:`can_set_timing_data` 和 :c:func:`can_calc_timing_data`。

SocketCAN
*********

Zephyr 额外支持 SocketCAN，它是 Zephyr CAN API 的一种 BSD socket 实现。
SocketCAN 将广为人知的 BSD Socket API 的便利性带入了
控制器局域网（CAN）。它与 Linux 的 SocketCAN 实现兼容，
许多其他高层 CAN 项目正是构建在其之上。
需要注意的是，帧会被路由到网络栈，而不是直接传递，
这会带来一些计算和内存开销。

示例
*******

我们提供了两个可直接构建的示例，用于演示 Zephyr CAN API 的使用：
:zephyr:code-sample:`Zephyr CAN 计数器示例 <can-counter>` 和
:zephyr:code-sample:`SocketCAN 示例 <socket-can>`。


CAN 控制器 API 参考
****************************

.. doxygengroup:: can_controller

.. doxygengroup:: can_fake
