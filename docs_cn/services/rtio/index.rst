.. _rtio:

实时 I/O（RTIO）
####################

.. contents::
  :local:
  :depth: 2

.. image:: rings.png
  :width: 800
  :alt: 提交和完成环形队列

RTIO 提供了一个用于事件驱动 I/O 的异步操作链框架。本节介绍 RTIO API、队列、执行器、iodev 以及与外设设备的常见使用模式。

RTIO 在操作和 API 方面大量借鉴了 Linux 的 io_uring，因为该 API 与硬件传输队列和描述符（如 DMA 传输列表）非常匹配。

问题
*******

如今，希望执行复杂 DMA 或中断驱动操作的应用在 Zephyr 中需要直接了解硬件及其工作方式。DMA API 并不了解其他 Zephyr 设备以及它们之间的关系。

这意味着执行复杂的音频、视频或传感器流需要直接的硬件知识，或者在 DMA 控制器之上使用泄漏的抽象。两者都不是理想的。

要启用异步操作，尤其是使用 DMA 时，需要描述要做什么，而不是通过 C 和回调进行直接操作。要启用带优先级的通道和传输序列等 DMA 功能，需要的不仅仅是简单的描述符列表。

使用 DMA 和/或中断驱动的 I/O 不应决定调用是否阻塞。

灵感来源：介绍 io_uring
*********************************

最好不要重新发明轮子（在本例中是环形队列），而 io_uring 作为 Linux 内核的 API 提供了一个成功的模型。在 io_uring 中，有两个无锁环形队列作为内核与用户态应用之间共享的队列。一个队列用于可链接并刷新以创建并发顺序请求的提交项。另一个队列用于完成队列事件。实际上只需要一个系统调用即可执行许多操作，即 io_uring_submit 调用。当给定要等待的操作数量时，该调用可能会阻塞调用者。

该模型很好地映射到 DMA 和中断驱动的传输。以异步方式执行一系列操作的请求与硬件通常使用中断驱动状态机的工作方式直接相关，可能涉及多个外设 IP，如总线控制器和 DMA 控制器。

提交队列
****************

提交队列（sq）是对要在并发链中执行的操作的描述。

例如，想象一个典型的 SPI 传输，你希望写入一个寄存器地址，然后从中读取。因此，操作序列可能是……

    1. 片选
    2. 时钟使能
    3. 将寄存器地址写入 SPI 发送寄存器
    4. 从 SPI 接收寄存器读取到缓冲区
    5. 禁用时钟
    6. 禁用片选

如果该操作链中的任何操作失败，就放弃。其中一些操作可以体现在设备抽象中，该抽象理解读取或写入隐式意味着设置时钟和片选。请求的事务性质也需要以某种方式体现。上述操作中，也许读取可以使用 DMA 完成，因为数据量足够大而有意义。这需要理解如何设置该设备的特定 DMA 来完成此操作。

上述操作序列在 RTIO 中体现为提交队列项（sqe）链。链式通过将 sqe 中的位标志置位来完成，表示下一个 sqe 必须等待当前 sqe。

由于片选和时钟是特定 SPI 控制器和总线上设备的共同点，它体现在 RTIO 所称的 iodev 中。

针对同一 iodev 的多个操作会尽快按提供的顺序执行。如果两个操作链在不同点使用同一设备，一个链可能需要等待另一个链完成。

完成队列
****************

为了知道何时 sqe 已完成，存在一个完成队列（cq），其中包含完成队列事件（cqe）。sqe 完成后会导致一个 cqe 被推入 cq。cqe 的顺序可能与 sqe 的顺序不同。然而，sqe 链会确保顺序和失败级联。

其他潜在方案也是可能的，但完成队列是 io_uring 和其他类似操作系统 API 中成熟的理念。

执行器
********

RTIO 执行器是一个低开销的并发 I/O 任务调度器。它确保某些请求标志提供预期行为。它接收一个提交列表并按顺序处理。各种标志允许改变提交的处理方式。形成顺序提交链、事务性提交集合或创建多发射（持续产生）请求的标志都是可能的！

I/O 设备
*********

将提交队列项（sqe）转换为完成队列事件（cqe）是实现 iodev（I/O 设备）API 的对象的工作。该 API 以 iodev submit API 调用的形式接受请求。I/O 设备的工作是处理其内部提交队列并将其转换为完成。从本质上讲，每个 I/O 设备都可以被视为一个独立的事件驱动 actor 对象，它接受永不停止的类 I/O 请求队列。iodev 如何完成此工作取决于 iodev 的作者，也许整个操作队列可以转换为一组 DMA 传输描述符，这意味着硬件完成了几乎全部实际工作。

取消
************

取消已排队的操作是可能的，但不保证成功。如果 SQE 尚未开始，调用 :c:func:`rtio_sqe_cancel` 很可能移除该 SQE 且永不执行它。然而，如果 SQE 已经开始运行，取消请求将被忽略。

内存池
************

在某些情况下，读取请求可能不知道将产生多少数据。或者，读取器可能正在处理来自多个 I/O 设备的数据，而数据频率不可预测。在这些情况下，将内存绑定到在途读取请求可能是浪费的。相反，使用内存池时，读取目标内存由 iodev 从与读取关联的 RTIO 上下文关联的内存池分配。要创建这样的 RTIO 上下文，可以使用 :c:macro:`RTIO_DEFINE_WITH_MEMPOOL`。它允许创建具有专用“内存块”池的 RTIO 上下文，该池可被 iodev 消耗。下面是设置带有内存池的 RTIO 上下文的代码片段。内存池有 128 个块，每个块大小为 16 字节，数据按 4 字节对齐。

.. code-block:: C

  #include <zephyr/rtio/rtio.h>

  #define SQ_SIZE       4
  #define CQ_SIZE       4
  #define MEM_BLK_COUNT 128
  #define MEM_BLK_SIZE  16
  #define MEM_BLK_ALIGN 4

  RTIO_DEFINE_WITH_MEMPOOL(rtio_context,
      SQ_SIZE, CQ_SIZE, MEM_BLK_COUNT, MEM_BLK_SIZE, MEM_BLK_ALIGN);

当需要读取时，调用者只需将调用 :c:func:`rtio_sqe_prep_read`（接受缓冲区指针和长度）替换为调用 :c:func:`rtio_sqe_prep_read_with_pool`。iodev 只需要一个小的更改即可同时支持预分配的数据缓冲区和内存池。当读取就绪时，iodev 不应直接从 :c:struct:`rtio_iodev_sqe` 获取缓冲区，而应通过调用 :c:func:`rtio_sqe_rx_buf` 获取缓冲区和计数，如下所示：

.. code-block:: C

  uint8_t *buf;
  uint32_t buf_len;
  int rc = rtio_sqe_rx_buff(iodev_sqe, MIN_BUF_LEN, DESIRED_BUF_LEN, &buf, &buf_len);

  if (rc != 0) {
    LOG_ERR("Failed to get buffer of at least %u bytes", MIN_BUF_LEN);
    return;
  }

最后，消费者可以通过 :c:func:`rtio_cqe_get_mempool_buffer` 访问分配的缓冲区。

.. code-block:: C

  uint8_t *buf;
  uint32_t buf_len;
  int rc = rtio_cqe_get_mempool_buffer(&rtio_context, &cqe, &buf, &buf_len);

  if (rc != 0) {
    LOG_ERR("Failed to get mempool buffer");
    return rc;
  }

  /* Release the cqe events (note that the buffer is not released yet */
  rtio_cqe_release_all(&rtio_context);

  /* Do something with the memory */

  /* Release the mempool buffer */
  rtio_release_buffer(&rtio_context, buf);

何时使用
***********

RTIO 在并发或批处理类 I/O 流有用的情况下很有用。

从驱动程序/硬件的角度来看，该 API 支持 I/O 请求的批处理，可能以最优方式。例如，对同一 SPI 外设的许多请求可能完全转换为硬件命令队列或 DMA 传输描述符。这意味着硬件可能比以往任何时候都能做更多。

每个 RTIO 上下文和 iodev 都有一定的成本。该成本可以与为每个并发 I/O 操作使用线程或为每个外设使用自定义队列和线程进行比较。RTIO 的成本远低于后者。

支持的总线
***************

要检查你的总线是否原生支持 RTIO，可以检查驱动程序 API 实现：如果驱动程序实现了总线 API 的 ``iodev_submit`` 函数，则支持 RTIO。如果驱动程序不支持 RTIO API，它会将 submit 函数设置为 ``i2c_iodev_submit_fallback``。

I2C 总线有一个默认实现，允许应用利用 RTIO 工作队列，而厂商实现 submit 函数。使用此队列，任何未实现 ``iodev_submit`` 函数的 I2C 总线驱动程序都会回退到执行阻塞 I2C 事务的工作项。要更改池大小，请为 :kconfig:option:`CONFIG_RTIO_WORKQ_POOL_ITEMS` 设置不同的值。

API 参考
*************

.. doxygengroup:: rtio
