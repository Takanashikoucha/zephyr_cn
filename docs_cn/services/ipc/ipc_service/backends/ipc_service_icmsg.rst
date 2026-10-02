.. _ipc_service_backend_icmsg:

ICMsg backend
#############

核间消息 backend（ICMsg）是比功能较重的 RPMsg static vrings backend 更轻量的替代方案。它以较小的内存占用提供了最小的功能集。ICMsg backend 构建在 :ref:`spsc_pbuf` 之上。

Overview
========

ICMsg backend 使用共享内存和 MBOX 设备来交换数据。
共享内存用于存储数据，MBOX 设备用于发出数据已写入的信号。

该 backend 支持在单个 instance 上注册单个 endpoint。如果应用需要多个通信通道，你必须定义多个 instances，每个 instance 拥有自己的专用 endpoint。

Configuration
=============

该 backend 通过 Kconfig 和 devicetree 进行配置。
配置该 backend 时，请执行以下操作：

* 如果至少一个 core 在共享内存上使用数据缓存，请设置 ``dcache-alignment`` 值。
  这必须是通信双方失效或写回大小的最大值。
  如果通信双方都不在共享内存上使用数据缓存，则可以跳过。
* 定义两个内存区域，并将它们分配给 instance 的 ``tx-region`` 和 ``rx-region``。
  确保用于数据交换的内存区域是唯一的（不与其他任何区域重叠），并且两个 domains（或 CPUs）都可以访问。
* 定义用于发送信号以通知其他 domain（或 CPU）数据已写入的 MBOX 设备。
  确保其他 domain（或 CPU）能够接收该信号。

.. caution::

    请确保你设置了正确的 ``dcache-alignment`` 值。
    起初，错误的值可能不会表现出任何征兆，这可能会给人一切正常的错误印象。
    不稳定的行为迟早会出现。

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
            compatible = "zephyr,ipc-icmsg";
            dcache-alignment = <32>;
            tx-region = <&tx>;
            rx-region = <&rx>;
            mboxes = <&mbox 0>, <&mbox 1>;
            mbox-names = "tx", "rx";
            status = "okay";
         };
      };
   };


你必须为通信的另一方（domain 或 CPU）提供类似的配置，但你必须交换 MBOX 通道和内存区域（``tx-region`` 和 ``rx-region``）。

Bonding
=======

当 endpoint 被注册时，每个通过 IPC instance 连接的 domain（或 CPU）上会发生以下情况：

1. 该 domain（或 CPU）将一个 magic number 写入其共享内存的 ``tx-region``。
#. 然后它向另一个 domain 或 CPU 发送信号，通知数据已写入。
   向另一个 domain 或 CPU 发送信号的操作会带超时重复执行。
#. 当收到来自另一个 domain 或 CPU 的信号时，从 ``rx-region`` 读取 magic number。
   如果正确，bonding 过程完成，backend 通过调用 :c:member:`ipc_service_cb.bound` 回调通知应用。

Samples
=======

 - :zephyr:code-sample:`ipc-icmsg`

Detailed Protocol Specification
===============================

ICMsg 使用两个共享内存区域和两个 MBOX 通道。
区域和通道对用于单向传输消息。
另一对是对称的，用于相反方向传输消息。
因此，下面的规范专注于这样的一对。
另一对是相同的。

ICMsg 每个 instance 只提供单个 endpoint。

Shared Memory Region Organization
---------------------------------

如果启用了数据缓存，提供给 ICMsg 的共享内存区域必须按缓存要求对齐。
如果未启用缓存，所需的对齐值为 4 字节。

共享内存区域完全由单个 FIFO 使用。
它包含读写索引，后跟数据缓冲区。
详细结构包含在以下表格中：

.. list-table::
   :header-rows: 1

   * - 字段名
     - 大小（字节）
     - 字节序
     - 描述
   * - ``rd_idx``
     - 4
     - little‑endian
     - ``data`` 字段中第一个传入字节的索引。
   * - ``padding``
     - 取决于缓存对齐
     - n/a
     - 为将 ``wr_idx`` 对齐到缓存对齐而添加的填充。
   * - ``wr_idx``
     - 4
     - little‑endian
     - ``data`` 字段中最后一个传入字节之后字节的索引。
   * - ``data``
     - 从当前位置到区域末尾的所有内容
     - n/a
     - 包含实际待传输字节的循环缓冲区。

这是一个带有循环缓冲区的常规 FIFO：

* 索引（``rd_idx`` 和 ``wr_idx``）在到达 ``data`` 缓冲区末尾时回绕。
* 如果 ``rd_idx == wr_idx``，则 FIFO 为空。
* FIFO 的容量比 ``data`` 缓冲区长度少一个字节。

Packets
-------

数据包通过上面章节中描述的 FIFO 发送。
如果一个数据包出现在 FIFO 缓冲区末尾，它可以发生回绕。

以下是数据包结构：

.. list-table::
   :header-rows: 1

   * - 字段名
     - 大小（字节）
     - 字节序
     - 描述
   * - ``len``
     - 2
     - big‑endian
     - ``data`` 字段的长度。
   * - ``reserved``
     - 2
     - n/a
     - 保留供将来使用。
       对于当前协议版本，它必须为 0。
   * - ``data``
     - ``len``
     - n/a
     - 数据包数据。
   * - ``padding``
     - 0‑3
     - n/a
     - 添加填充以将数据包总大小对齐到 4 字节。

数据包发送流程如下：

#. 检查数据包是否能放入缓冲区。
#. 从 ``wr_idx`` 开始将数据包写入 ``data`` FIFO 缓冲区。
   如需要则进行回绕。
#. 写入 ``wr_idx`` 的新值。
#. 通过 MBOX 通道通知接收方。

Initialization
--------------

初始化序列如下：

#. 将 ``wr_idx`` 和 ``rd_idx`` 设置为零。
#. 向 FIFO 推送一个包含 magic data 的单个数据包：``45 6d 31 6c 31 4b 30 72 6e 33 6c 69 34``。
   此时尚不使用 MBOX。
#. 初始化 MBOX。
#. 使用某个时间间隔（例如 1 ms）重复通过 MBOX 通道发送通知。
#. 等待包含 magic data 的传入数据包。
   它将通过另一对（共享内存区域和 MBOX）到达。
#. 停止重复 MBOX 通知。

在此之后，ICMsg 完成绑定，并准备好传输数据包。
