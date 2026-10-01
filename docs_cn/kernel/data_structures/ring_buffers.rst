.. _ring_buffers_v2:

环形缓冲区
############

:dfn:`环形缓冲区（ring buffer）`是一种环形缓冲区，
其内容按先进先出顺序存储。

当应用需要实现数据的异步"流式"拷贝时，
Zephyr 提供了一个 ``struct ring_buf`` 抽象，
用于管理此类数据在共享内存缓冲区中进出的拷贝。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的环形缓冲区（仅受可用 RAM 限制）。
每个环形缓冲区由其内存地址引用。

环形缓冲区具有以下关键特性：

* 一个**数据缓冲区**（字节）。数据缓冲区包含
  已添加到环形缓冲区但尚未移除的原始字节。

* 一个以字节为单位的**数据缓冲区大小**。它决定了
  环形缓冲区可容纳的最大数据量。

环形缓冲区在使用前必须初始化。
这会将其数据缓冲区设置为空。

``struct ring_buf`` 可以放在用户可访问内存的任何位置，
并且必须在使用前用 :c:func:`ring_buf_init` 初始化。
这必须提供一个用户控制的内存区域作为缓冲区本身。
请注意，所传缓冲区大小的单位（字节或字）
会根据环形缓冲区后续的使用方式而变化。
为方便起见，存在将这些步骤合并为单个静态声明的宏。
:c:macro:`RING_BUF_DECLARE` 将以指定的字节数
声明并静态初始化一个环形缓冲区，其中

"字节"数据可以用 :c:func:`ring_buf_put` 拷贝到环形缓冲区，
传入数据指针和字节数。
这些字节将按顺序拷贝到缓冲区中，
尽可能多地放入已分配的缓冲区。
拷贝的字节总数（可能少于提供的数量）将被返回。
同样，:c:func:`ring_buf_get` 将按写入顺序
把字节从环形缓冲区拷贝到用户提供的缓冲区，
并返回传输的字节数。

为避免多次拷贝数据的情况，提供了零拷贝"指针" API。
:c:func:`ring_buf_put_ptr` 返回一个指向环形缓冲区
内部内存的指针，可用于接收字节，
以及可用于写入的连续内部区域大小
（如果区域回绕，它可能小于总空闲空间）。
然后用户可以直接将数据写入该区域（例如通过 DMA），
而无需先将所有字节组装到一个区域中。
完成后，使用 :c:func:`ring_buf_commit` 向缓冲区发出信号，
表示传输已完成，传入实际传输的字节数。
此时可以发起新的传输。
类似地，:c:func:`ring_buf_get_ptr` 返回一个指向
环形缓冲区内部数据的指针，
用户可以从该指针读取而无需逐字拷贝，
:c:func:`ring_buf_consume` 向缓冲区发出
已消费多少字节的信号，并允许新的传输开始。

遗留的 :c:func:`ring_buf_put_claim` / :c:func:`ring_buf_put_finish` 和
:c:func:`ring_buf_get_claim` / :c:func:`ring_buf_get_finish` API 提供
类似功能，但在完成前保留已认领的区域，
会产生额外的代码大小和运行时开销。
这些 API 已弃用，将在未来版本中移除；
新代码应使用上面描述的 ``_ptr`` / ``_commit`` / ``_consume`` 变体。

用户可以用 :c:func:`ring_buf_space_get`（返回空闲字节数）
或测试 :c:func:`ring_buf_is_empty` 谓词，
在不修改环形缓冲区的情况下管理其容量。

最后，存在 :c:func:`ring_buf_reset` 调用，
可立即清空环形缓冲区，
丢弃对已写入缓冲区的任何字节的跟踪。
但它不会修改缓冲区本身的内存内容。


实例化与使用
======================

环形缓冲区实例使用 :c:macro:`RING_BUF_DECLARE()` 声明，
并使用以下函数访问：
:c:func:`ring_buf_put_ptr`、:c:func:`ring_buf_commit`、
:c:func:`ring_buf_get_ptr`、:c:func:`ring_buf_consume`、
:c:func:`ring_buf_put` 和 :c:func:`ring_buf_get`。

数据可以拷贝到环形缓冲区（参见 :c:func:`ring_buf_put`），
或环形缓冲区内存可被用户直接使用。
在后一种情况下，操作分为三个阶段：

1. 访问环形缓冲区的内部缓冲区（:c:func:`ring_buf_put_ptr`）
   获取指向下一个可写入位置的指针，
   以及该位置可用的连续空间量。
#. 由用户写入数据（例如由 DMA 写入缓冲区）。
#. 指示写入所提供缓冲区的数据量（:c:func:`ring_buf_commit`）。
   提交量可以小于或等于 :c:func:`ring_buf_put_ptr` 提供的量。


数据可以通过拷贝从环形缓冲区获取（参见 :c:func:`ring_buf_get`），
或按地址直接访问。
在后一种情况下，操作分为三个阶段：

1. 访问环形缓冲区的内部缓冲区（参见 :c:func:`ring_buf_get_ptr`）
   获取指向下一个可读位置的指针，
   以及该位置可用的连续数据量。
#. 处理数据
#. 向环形缓冲区发出信号，表示数据已被消费（参见 :c:func:`ring_buf_consume`）。
   消费量可以小于或等于 :c:func:`ring_buf_get_ptr` 提供的量。

并发
============

环形缓冲区 API 不提供任何内部并发控制。
根据使用情况（特别是并发读者/写者数量），
应用可能需要用互斥锁保护环形缓冲区和/或使用信号量
通知消费者有数据可读。

运行在单独执行上下文中的单个生产者和单个消费者
（例如两个线程，或一个线程和一个 ISR）
可以并发使用同一个环形缓冲区而无需额外加锁。
生产者一侧只更新 ``put`` 索引，消费者一侧只更新 ``get`` 索引，
因此两侧永远不会写入相同的字段。
这对拷贝 API（:c:func:`ring_buf_put` / :c:func:`ring_buf_get`）
和零拷贝"认领" API（:c:func:`ring_buf_put_claim` /
:c:func:`ring_buf_put_finish` 和 :c:func:`ring_buf_get_claim` /
:c:func:`ring_buf_get_finish`）都成立。

当生产者和消费者运行在不同 CPU（SMP）上时，
应用仍须确保数据写入在发布它们的索引更新之前可见。
实际上，当生产者和消费者使用内核同步原语进行协调时
（例如生产者发出信号、消费者等待的 :c:struct:`k_sem`），
这会免费发生，因为这些原语包含了必要的内存屏障。

任何具有多个并发生产者或多个并发消费者的用例，
都必须从外部序列化这些访问
（例如使用互斥锁或禁用抢占）。

内部操作
==================

通过环形缓冲区流式传输的数据总是写入缓冲区中的下一个字节，
到达末尾后回绕到第一个元素，从而形成"环形"结构。
内部地，``struct ring_buf`` 包含其自身的缓冲区指针和大小，
以及一组表示下一次读和写操作可能发生的"头"和"尾"索引。

这个边界对使用普通 put/get API 的用户是不可见的，
但对"认领" API 却构成障碍，
因为显然无法返回跨越缓冲区末尾的连续区域。
这可能令应用代码感到意外，
并在传输需要发生在缓冲区末尾附近时产生性能假象，
因为此类传输所需的 claim/finish 调用次数需要翻倍。


实现
**************

定义环形缓冲区
====================

环形缓冲区使用 :c:struct:`ring_buf` 类型的变量定义。
然后必须通过调用 :c:func:`ring_buf_init` 初始化。

环形缓冲区可以在文件作用域使用宏在编译时定义并初始化。
该宏定义环形缓冲区本身及其数据缓冲区。

以下代码定义了一个环形缓冲区：

.. code-block:: c

    #define MY_RING_BUF_BYTES 93
    RING_BUF_DECLARE(my_ring_buf, MY_RING_BUF_BYTES);

入队数据
================

通过调用 :c:func:`ring_buf_put` 将字节拷贝到环形缓冲区。

.. code-block:: c

    uint8_t my_data[MY_RING_BUF_BYTES];
    uint32_t ret;

    ret = ring_buf_put(&ring_buf, my_data, MY_RING_BUF_BYTES);
    if (ret != MY_RING_BUF_BYTES) {
        /* not enough room, partial copy. */
	...
    }

通过直接访问环形缓冲区的内存，也可以向环形缓冲区添加数据。
例如：

.. code-block:: c

    uint32_t size;
    uint32_t rx_size;
    uint8_t *data;

    /* Get pointer to writable area within the ring buffer memory. */
    size = ring_buf_put_ptr(&ring_buf, &data, 0);

    /* Work directly on a ring buffer memory. */
    rx_size = uart_rx(data, size);

    /* Indicate amount of valid data. rx_size must be equal or less than size. */
    ring_buf_commit(&ring_buf, rx_size);


获取数据
================

通过调用 :c:func:`ring_buf_get` 将数据字节从环形缓冲区拷贝出来。
例如：

.. code-block:: c

    uint8_t my_data[MY_DATA_BYTES];
    size_t  ret;

    ret = ring_buf_get(&ring_buf, my_data, sizeof(my_data));
    if (ret != sizeof(my_data)) {
        /* Fewer bytes copied. */
    } else {
        /* Requested amount of bytes retrieved. */
        ...
    }

通过对环形缓冲区内存的直接操作，也可以从环形缓冲区获取数据。
例如：

.. code-block:: c

    uint32_t size;
    uint32_t proc_size;
    uint8_t *data;

    /* Get pointer to readable data within the ring buffer memory. */
    size = ring_buf_get_ptr(&ring_buf, &data, 0);

    /* Work directly on a ring buffer memory. */
    proc_size = process(data, size);

    /* Indicate amount of data that has been consumed. proc_size must be equal
     * or less than size.
     */
    ring_buf_consume(&ring_buf, proc_size);

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_RING_BUFFER`：恢复已弃用的遗留环形缓冲区 API
  （claim/finish 和固定大小条目 API）。环形缓冲区本身是纯头文件实现
  且始终可用，因此正常使用不需要此选项。
* :kconfig:option:`CONFIG_RING_BUFFER_LARGE`：将最大缓冲区大小
  从 32KB 增加到 1GB。

API 参考
*************

:zephyr_file:`include/zephyr/sys/ring_buffer.h` 提供以下环形缓冲区 API：

.. doxygengroup:: ring_buffer_apis
