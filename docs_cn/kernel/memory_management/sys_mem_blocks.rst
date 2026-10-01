.. _sys_mem_blocks:

内存块分配器
#######################

内存块分配器允许从指定的内存区域动态分配内存块，其中：

* 所有内存块都具有单一的固定大小。

* 可以同时分配或释放多个块。

* 一起分配的一组块可能不是连续的。
  这对于散列-聚集（scatter-gather）DMA 传输等操作非常有用。

* 已分配块的管理信息记录在关联缓冲区之外
  （与内存块 slab 不同）。这使得缓冲区可以驻留在
  可以断电以节省能量的内存区域中。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的内存块分配器（仅受
可用 RAM 限制）。每个分配器通过其内存地址来引用。

内存块分配器具有以下关键属性：

* 每个内存块的**块大小**，以字节为单位。
  必须至少为 4N 字节，其中 N 大于 0。

* 可用于分配的**块数量**。
  必须大于零。

* 提供后备存储的**缓冲区**，内存块
  分配器将从中分配块。
  长度必须至少为"块大小"乘以"块数量"字节。

* 用于跟踪哪些块已被分配的**块位图**。

缓冲区必须对齐到 N 字节边界，其中 N 是大于 2 的
2 的幂（即 4、8、16、...）。为确保缓冲区中的所有
内存块都以相同方式对齐到该边界，块大小
也必须是 N 的倍数。

由于使用了内部管理结构及其创建过程，
每个内存块分配器都必须在编译时声明和定义。

内部工作原理
==================

与每个分配器关联的缓冲区是一个固定大小块的数组，
块与块之间没有浪费的空间。

内存块分配器使用位图来跟踪未分配的块。

内存块分配器
***********************

内部，内存块分配器使用位图来跟踪
哪些块已被分配。每个分配器利用
``sys_bitarray`` 接口，从
后备缓冲区中逐个获取内存块，
直到达到请求的块数量。
关于分配器的所有元数据都存储在后备
缓冲区之外。这使得后备缓冲区的内存区域
可以断电以节省能量，因为分配器代码从不
访问缓冲区的内容。

多内存块分配器组
***********************************

多内存块分配器组的工具函数用于
方便地管理一组分配器。可以
编写一个自定义函数来选择该组管理的
哪个分配器应用于块分配。

分配器组应在运行时通过
:c:func:`sys_multi_mem_blocks_init` 进行初始化。然后每个分配器
可以通过 :c:func:`sys_multi_mem_blocks_add_allocator`
添加。

要从组中分配内存块，
调用 :c:func:`sys_multi_mem_blocks_alloc`，
传入一个不透明的"配置"参数。
该参数直接传递给
分配器选择函数，以便选择适当的
分配器。选择分配器后，内存块
通过 :c:func:`sys_mem_blocks_alloc`
分配。

已分配的内存块可以通过
:c:func:`sys_multi_mem_blocks_free` 释放。
调用者无需
传入配置参数。分配器代码将
传入的内存地址进行匹配，
以找到正确的分配器，
然后通过 :c:func:`sys_mem_blocks_free`
释放内存块。

使用
*****

定义内存块分配器
==================================

内存块分配器使用 :c:type:`sys_mem_blocks_t`
类型的变量来定义。需要通过
调用 :c:macro:`SYS_MEM_BLOCKS_DEFINE`
在编译时定义和初始化。

以下代码定义并初始化一个内存块分配器，
该分配器具有 4 个 64 字节长的块，
每个块都对齐到 4 字节边界：

.. code-block:: c

   SYS_MEM_BLOCKS_DEFINE(allocator, 64, 4, 4);

类似地，你可以在私有作用域中定义内存块分配器：

.. code-block:: c

   SYS_MEM_BLOCKS_DEFINE_STATIC(static_allocator, 64, 4, 4);

还可以向分配器提供一个预定义的缓冲区，
其中缓冲区可以单独放置。
注意缓冲区**必须**在定义时
指定其对齐方式。

.. code-block:: c

   uint8_t __aligned(4) backing_buffer[64 * 4];
   SYS_MEM_BLOCKS_DEFINE_WITH_EXT_BUF(allocator, 64, 4, backing_buffer);

分配内存块
========================

内存块可以通过调用 :c:func:`sys_mem_blocks_alloc` 来分配。

.. code-block:: c

   int ret;
   uintptr_t blocks[2];

   ret = sys_mem_blocks_alloc(allocator, 2, blocks);

如果 ``ret == 0``，数组 ``blocks`` 将包含一个
内存地址数组，指向已分配的块。

释放内存块
========================

内存块通过调用 :c:func:`sys_mem_blocks_free` 来释放。

以下代码基于上面的示例，该示例分配了 2 个内存块，
然后在不再需要时将其释放。

.. code-block:: c

   int ret;
   uintptr_t blocks[2];

   ret = sys_mem_blocks_alloc(allocator, 2, blocks);
   ... /* perform some operations on the allocated memory blocks */
   ret = sys_mem_blocks_free(allocator, 2, blocks);

使用多内存块分配器组
=========================================

以下代码演示如何初始化一个分配器组：

.. code-block:: c

   sys_mem_blocks_t *choice_fn(struct sys_multi_mem_blocks *group, void *cfg)
   {
       ... /* choose which allocator in the group to use based on cfg */
   }

   SYS_MEM_BLOCKS_DEFINE(allocator0, 64, 4, 4);
   SYS_MEM_BLOCKS_DEFINE(allocator1, 64, 4, 4);

   static sys_multi_mem_blocks_t alloc_group;

   sys_multi_mem_blocks_init(&alloc_group, choice_fn);
   sys_multi_mem_blocks_add_allocator(&alloc_group, &allocator0);
   sys_multi_mem_blocks_add_allocator(&alloc_group, &allocator1);

要从组中分配和释放内存块：

.. code-block:: c

   int ret;
   uintptr_t blocks[1];
   size_t blk_size;

   ret = sys_multi_mem_blocks_alloc(&alloc_group, UINT_TO_POINTER(0),
                                    1, blocks, &blk_size);

   ret = sys_multi_mem_blocks_free(&alloc_group, 1, blocks);

API 参考
*************

.. doxygengroup:: mem_blocks_apis
