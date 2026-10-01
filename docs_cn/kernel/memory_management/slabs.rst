.. _memory_slabs_v2:

内存块（Slabs）
############

:dfn:`内存块（memory slab）` 是一种内核对象，允许从指定的内存区域动态分配内存块。
内存块中的所有内存块都具有单一的固定大小，
从而可以高效地进行分配和释放，
并避免内存碎片化问题。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的内存块（仅受可用 RAM 限制）。每个
内存块通过其内存地址来引用。

内存块具有以下关键属性：

* 每个内存块的**块大小**，以字节为单位。
  在 32 位平台上必须至少为 4N 字节，在 64 位平台上
  必须至少为 8N 字节，其中 N 大于 0。

* 可用于分配的**块数量**。
  必须大于零。

* 为内存块的块提供内存的**缓冲区**。
  长度必须至少为"块大小"乘以"块数量"字节。

内存块的缓冲区必须对齐到 N 字节边界，其中 N 是
2 的幂。N 在 32 位平台上必须至少为 4，在 64 位
平台上必须至少为 8。为确保缓冲区中的所有内存块都
以相同方式对齐到该边界，块大小也必须是 N 的倍数。

内存块在使用前必须初始化。这会将所有
块标记为未使用。

需要使用内存块的线程只需从内存块中分配即可。当线程
用完一个内存块时，
必须将该块释放回内存块，以便该块可以被重用。

如果所有块当前都在使用中，线程可以选择
等待其中一个变为可用。
任意数量的线程可以同时等待一个空的内存块；
当一个内存块变为可用时，它会被分配给
等待时间最长的最高优先级线程。

如有需要，可以定义多个内存块。这
允许一个内存块具有较小的块，而其他内存块
具有较大尺寸的块。或者，可以使用内存池对象。

内部工作原理
==================

内存块的缓冲区是一个固定大小块的数组，
块与块之间没有浪费的空间。

内存块使用链表来跟踪未分配的块。
32 位平台使用每个未使用块的前 4 字节来提供
必要的链接，而 64 位平台使用每个
未使用块的前 8 字节。

实现
**************

定义内存块
=====================

内存块使用 :c:type:`k_mem_slab` 类型的变量来定义。
然后必须通过调用 :c:func:`k_mem_slab_init` 进行初始化。

以下代码定义并初始化一个具有 6 个
400 字节长块的内存块，每个块都对齐到 8 字节边界。

.. code-block:: c

    struct k_mem_slab my_slab;
    char __aligned(8) my_slab_buffer[6 * 400];

    k_mem_slab_init(&my_slab, my_slab_buffer, 400, 6);

或者，内存块可以通过调用 :c:macro:`K_MEM_SLAB_DEFINE`
在编译时定义并初始化。

以下代码与上面的代码段效果相同。注意
该宏同时定义了内存块及其缓冲区。

.. code-block:: c

    K_MEM_SLAB_DEFINE(my_slab, 400, 6, 8);

类似地，你可以在私有作用域中定义内存块：

.. code-block:: c

    K_MEM_SLAB_DEFINE_STATIC(my_slab, 400, 6, 8);

分配内存块
=========================

内存块通过调用 :c:func:`k_mem_slab_alloc` 来分配。

以下代码基于上面的示例，最多等待 100 毫秒
直到一个内存块变为可用，然后用零填充它。
如果未能获取到合适的块，则打印一条警告。

.. code-block:: c

    char *block_ptr;

    if (k_mem_slab_alloc(&my_slab, (void **)&block_ptr, K_MSEC(100)) == 0) {
        memset(block_ptr, 0, 400);
	...
    } else {
        printf("Memory allocation time-out");
    }

释放内存块
========================

内存块通过调用 :c:func:`k_mem_slab_free` 来释放。

以下代码基于上面的示例，分配一个内存块，
然后在不再需要时将其释放。

.. code-block:: c

    char *block_ptr;

    k_mem_slab_alloc(&my_slab, (void **)&block_ptr, K_FOREVER);
    ... /* use memory block pointed at by block_ptr */
    k_mem_slab_free(&my_slab, (void *)block_ptr);

查询内存块使用情况
===================

内存块的当前使用率可以在运行时查询。
:c:func:`k_mem_slab_num_used_get` 返回当前
已分配的块数量，:c:func:`k_mem_slab_num_free_get` 返回仍
可用的块数量。当 :kconfig:option:`CONFIG_MEM_SLAB_TRACE_MAX_UTILIZATION`
启用时，:c:func:`k_mem_slab_max_used_get` 报告同时
分配的高峰块数量，
:c:func:`k_mem_slab_runtime_stats_get` 在一个
:c:struct:`sys_memory_stats` 结构中一起返回这些数据。

建议用途
**************

使用内存块以固定大小的块来分配和释放内存。

在从一个线程向另一个线程发送大量数据时
使用内存块的块，以避免不必要的数据复制。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_MEM_SLAB_TRACE_MAX_UTILIZATION`

API 参考
*************

.. doxygengroup:: mem_slab_apis
