.. _ipc_service_backend_icbmsg:

ICMsg with dynamically allocated buffers backend
################################################

通过该 backend 传输的数据在共享内存中动态分配的缓冲区中传输。分配是线程安全的，可以从任何上下文进行。该 backend 支持：

* 多个 endpoints。
* No-copy 发送。
* 持有 RX 缓冲区。
* 从中断上下文发送。
* 两级 endpoint 优先级。
* 统计和可选的带利用率报告的 shell 命令
* 最多支持 32 个块。
* 数据缓存支持。
* 低内存占用（约 2 kB 代码）。

Overview
========

对于每个方向，都会保留一个共享内存区域，每个区域被分为两部分。一部分形成一个固定大小缓冲区的池，分配器从池中相邻的缓冲区构建可变大小的缓冲区。另一部分用于由两个消息队列（每个方向各一个）组成的控制路径。存在一个生产者队列，由发送方写入、接收方读取；以及一个消费者队列，由接收方写入、发送方读取。生产者队列包含下一条消息位置（在池内）的信息。消费者队列包含已消费消息位置（在池内）的信息。

数据发送流程如下：

* 发送方从池中分配一个或多个块。
  如果连续块不足，线程上下文会使用参数中提供的超时进行等待，该参数还包括 K_FOREVER 和 K_NO_WAIT。
* 已分配的块被填入数据。
  第一个块的开头有一个 32 位消息头，包含长度、endpoint ID 和自身块索引。
  对于零拷贝情况，这由调用方完成；否则会自动复制。
  在此期间，只要空闲块足够，其他线程就不会以任何方式被阻塞。
  它们可以分配、发送数据和接收数据。
* 带有消息开头的块索引被写入生产者队列。
  endpoint 的优先级信息附加在块索引之后。
  :kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_MAX_ACTIVE_COUNT` 定义了队列中的槽位数量。
  向接收方发送 mailbox 通知。
* 接收方读取生产者队列。优先级更高的消息优先处理。
  它可以根据需要持有数据。
  同样，只要空闲块足够，其他线程就不会被阻塞。
* 当不再需要数据时，接收方将块索引写入消费者队列。
* 发送方通过读取消费者队列并释放缓冲区来执行垃圾回收。
  垃圾回收在发送任何消息之后或没有可用缓冲区时执行。

Configuration
=============

该 backend 通过 Kconfig 和 devicetree 进行配置。

有以下 Kconfig 选项：

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_NUM_EP` - 已注册 endpoint 的最大数量。

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_MAX_ACTIVE_COUNT` - 队列中的槽位数量。

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_DEINIT` - 支持注销和关闭。

:kconfig:option:`CONFIG_IPC_SERVICE_BACKEND_ICBMSG_SHELL` - 支持 shell 命令。

配置该 backend 时，请执行以下操作：

* 如果至少一个 core 在共享内存上使用数据缓存，请设置 ``dcache-alignment`` 值。
  这必须是通信双方失效或写回大小的最大值。
  如果通信双方都不在共享内存上使用数据缓存，则可以跳过。
* 定义两个内存区域，并将它们分配给 instance 的 ``tx-region`` 和 ``rx-region``。
  确保用于数据交换的内存区域是唯一的（不与其他任何区域重叠），并且两个 domains（或 CPUs）都可以访问。
* 使用 ``tx-blocks`` 和 ``rx-blocks`` 为每个区域定义可分配块的数量。
* 定义 MBOX 设备，用于发送通知其他 domain（或 CPU）已写入数据的信号。
  确保其他 domain（或 CPU）能够接收该信号。

.. caution::

    请确保你设置了正确的 ``dcache-alignment`` 值。
    起初，错误的值可能不会表现出任何征兆，这可能会给人一切正常的错误印象。
    不稳定的行为迟早会出现。

如果使用 ``dcache-alignment``，则应仔细选择块数量的配置，以避免内存使用效率低下。
这是因为块按缓存对齐方式对齐，如果块数量不是缓存对齐的倍数，则最后一个块将无法被高效使用。
这是因为块和控制数据都按缓存对齐方式对齐。
例如，如果 ``dcache-alignment`` 为 32，且一个方向使用 1024 字节共享内存。
控制数据将占用 64 字节，剩余 960 字节用于缓冲区。
使用 16 个块将导致每块 32 字节（由于缓存对齐）。
使用 15 个块将导致每块 64 字节（由于缓存对齐），内存利用率要好得多。


参见以下某个 instance 的配置示例：

.. code-block:: devicetree

   reserved-memory {
      tx: memory@20070000 {
         reg = <0x20070000 0x0800>;
      };

      rx: memory@20078000 {
         reg = <0x20078000 0x0800>;
      };
   };

   ipc {
      ipc0: ipc0 {
         compatible = "zephyr,ipc-icbmsg";
         dcache-alignment = <32>;
         tx-region = <&tx>;
         rx-region = <&rx>;
         tx-blocks = <16>;
         rx-blocks = <16>;
         mboxes = <&mbox 0>, <&mbox 1>;
         mbox-names = "tx", "rx";
         status = "okay";
      };
   };


你必须为通信的另一方（domain 或 CPU）提供类似的配置。
交换 MBOX 通道、内存区域（``tx-region`` 和 ``rx-region``）以及块数量（``tx-blocks`` 和 ``rx-blocks``）。

Limitations
===========

* 预期通信双方的字节序（endianness）相同。
* 不支持检测意外的远程重置。

Samples
=======

* :zephyr:code-sample:`ipc_multi_endpoint`

Detailed Protocol Specification
===============================

ICBMsg 协议使用动态分配的共享内存块来传输消息。

Shared Memory Organization
--------------------------

ICBMsg 使用两个共享内存区域：``rx-region`` 用于接收消息，``tx-region`` 用于传输消息。
这些区域不需要彼此相邻、按特定顺序放置或大小相同。
这些区域在每个 core 上是互换的。

每个共享内存区域被分为以下两部分：

* **控制区** - 由生产者和消费者队列保留的区域。
* **块区** - 包含承载消息内容的可分配块的区域。
  该区域被分为大小相等、按缓存边界对齐的块。

每个区域的位置经过计算，以满足缓存边界要求并实现区域的最优使用。
使用以下算法进行计算：

输入：

* ``region_begin``、``region_end`` - 区域的边界。
* ``local_blocks`` - 该区域中的块数。
* ``remote_blocks`` - 相对区域中的块数。
* ``alignment`` - 内存缓存对齐值。

算法：

#. 将区域边界对齐到缓存：

   * ``region_begin_aligned = ROUND_UP(region_begin, alignment)``
   * ``region_end_aligned = ROUND_DOWN(region_end, alignment)``
   * ``region_size_aligned = region_end_aligned - region_begin_aligned``

#. 计算控制区所需的最小大小：

   * 每个队列有 :kconfig:option:`IPC_SERVICE_BACKEND_ICBMSG_MAX_ACTIVE_COUNT` 字节和 8 字节队列头。
   * 通常每个方向的控制数据占用不到 64 字节。

#. 计算块区的可用大小。注意，由于块对齐，实际大小可能更小：

   ``blocks_area_available_size = region_size_aligned - control_area``

#. 计算单个块的大小：

   ``block_size = ROUND_DOWN(blocks_area_available_size / local_blocks, alignment)``

#. 计算块区的实际大小：

   ``blocks_area_size = block_size * local_blocks``

#. 计算块区的起始地址：

   ``blocks_area_begin = region_end_aligned - blocks_area_size``

结果：

* ``region_begin_aligned`` - ICMsg 区域的起始位置。
* ``blocks_area_begin`` - ICMsg 区域的结束位置和块区的起始位置。
* ``block_size`` - 单个块的大小。
* ``region_end_aligned`` - 块区的结束位置。

.. image:: icbmsg_memory.svg
   :align: center

|

Message Transfer
----------------

ICBMsg 使用以下两种类型的消息：

* **控制消息** - 如绑定或解绑之类的消息。
* **数据消息** - 承载实际用户数据的消息。

它们服务于不同的目的，但其生命周期和流程相同。
以下步骤描述了该流程：

#. 发送方想要发送一条包含 ``K`` 字节的消息。
#. 发送方从其 ``tx-region`` 块区中保留能够容纳至少 ``K + 4`` 字节的块。
   额外的 ``+ 4`` 字节保留给头部。
   块必须是连续的（一个接一个）。
   发送方负责块分配管理。
   如果没有可用块，则线程上下文可能阻塞，而中断上下文将返回错误。
#. 发送方填充头部。
#. 发送方用其数据填充块的剩余部分。
   未使用的空间被忽略。
#. 发送方将消息写入生产者队列并发送 mailbox 信号。
#. 接收方在 mailbox 中断上下文中执行 mailbox 回调并读取生产者队列。
#. 接收方读取块索引并在其 ``rx-region`` 中定位消息。
#. 接收方读取 endpoint 和消息长度并处理该消息。
#. 接收方通过将其块索引写入消费者队列来消费该消息。
   不发送 mailbox 信号。
#. 发送方在每次发送之后或发送失败时检查消费者队列。
   消息从消费者队列中读取并释放回池中。

.. image:: icbmsg_message.svg
   :align: center

|

Binding Instances
-----------------

当 backend instance 被打开时，它会发送一条包含 64 位 magic number 的 bound 消息。
Mailbox 回调被启用，instance 等待 bound 消息。
在收到 bound 消息后，instance 与远程 instance 绑定，然后可以注册 endpoints。

Binding Endpoint
----------------

endpoint 绑定消息包含 endpoint 名称的 SHA 和 endpoint ID，后者是 endpoint 数据所在本地数组中的索引。

有两种可能的场景：

* 远程 instance 在该 endpoint 注册之前发送了该 endpoint 的绑定消息。
* 该 endpoint 在收到远程 instance 的绑定消息之前被注册。

当收到绑定消息时，SHA 与 endpoint 数据数组中存储的 SHA 进行比较。
如果找到匹配，则意味着该 endpoint 已被本地 instance 注册。
endpoint ID 存储在 endpoint 数据中，并调用 bound 回调。
如果未找到匹配，则找到空槽位，并将 endpoint ID 和 SHA 存储在可用槽位中。

当 endpoint 被注册时，计算名称的 SHA 并与 endpoint 数据数组中存储的 SHA 进行比较。
如果找到匹配，则意味着该 endpoint 的远程绑定消息已收到。
在这种情况下，向远程 instance 发送绑定消息并调用 bound 回调。
如果未找到匹配，则找到空槽位，并将 endpoint ID 和 SHA 存储在可用槽位中。
向远程 instance 发送绑定消息，但 endpoints 尚未绑定。

稍后，远程 endpoint ID 用于数据消息以标识该 endpoint。

Unbinding Endpoint
------------------

当 endpoint 被注销时，会发送一条 unbinding 控制消息。
该 endpoint 从 endpoint 数据数组中移除。
当收到 unbinding 消息时，endpoint 槽位被标记为空，并调用 unbinding 回调。
