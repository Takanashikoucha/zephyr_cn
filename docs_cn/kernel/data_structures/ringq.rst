.. _fixed_size_ringq_api:

sys_ringq 数据结构
########################

.. contents::
  :local:
  :depth: 2

概述
********

环形队列（或环形缓冲区）是一种数据结构，它将单个固定大小的缓冲区
当作首尾相连来使用。这种结构特别
适合以有序方式缓冲条目。

当需要解耦离散数据大小的生产者和消费者，
而无需担心部分读取或变长负载时，就会使用 ringq。
这一区别将其与 :ref:`ring_buffer <ring_buffers_v2>` 数据结构区分开来，
后者是字节的流式数据结构。

并发
=============

sys_ringq API 不提供任何并发控制。根据使用情况，
应用应使用适当的同步机制（例如互斥锁、
信号量）保护 sys_ringq 结构体，
以确保从多个线程访问时的线程安全。

实例化与使用
*********************

``sys_ringq`` 可以用
``SYS_RINGQ_DEFINE(name, item_size, item_capacity)``
宏声明，也可以在运行时用
``sys_ringq_init(struct sys_ringq *ringq, uint8_t *data, size_t data_size, size_t item_size);`` 函数初始化。

.. code-block:: c

   SYS_RINGQ_DEFINE(my_ringq, item_size, item_capacity);
   /* equivalent to */

   static struct sys_ringq my_ringq;
   static uint8_t buffer[item_size * item_capacity];
   void init_fn (void) {
      sys_ringq_init(&my_ringq, buffer, sizeof(buffer), item_size);
      ....
   }

``sys_ringq`` 初始化后，可以用 ``sys_ringq_put()``
函数向 ringq 添加条目，用 ``sys_ringq_get()``
函数移除条目。ringq 保持条目的
顺序，并确保底层数据缓冲区的正确边界检查。

.. code-block:: c

    struct my_item item_to_add = { ... };
    struct my_item item_removed;

    /* Add an item to the queue */
    if (sys_ringq_put(&my_ringq, &item_to_add) == 0) {
        // Item added successfully
    } else {
        // ringq is full
    }

    /* Remove an item from the queue */
    if (sys_ringq_get(&my_ringq, &item_removed) == 0) {
        // Item removed successfully
    } else {
        // ringq is empty
    }

除标准数据操作（sys_ringq_put() 和 sys_ringq_get()）外，sys_ringq API 提供一组
用于管理和检查数据结构状态的
实用函数。

* sys_ringq_capacity() – 返回 sys_ringq 的总容量（以可容纳的条目数计）。
* sys_ringq_empty() – 如果 sys_ringq 不包含任何条目则返回 true。
* sys_ringq_full() – 如果 sys_ringq 无法再接受更多条目则返回 true。
* sys_ringq_space() – 返回剩余的空闲槽位数。
* sys_ringq_size() – 返回当前存储的条目数。
* sys_ringq_reset() – 将 sys_ringq 重置为空状态。

API 参考
*************
.. doxygengroup:: sys_ringq_apis
