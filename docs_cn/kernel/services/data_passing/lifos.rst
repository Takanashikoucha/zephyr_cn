.. _lifos_v2:

LIFO
#####

:dfn:`LIFO` 是一种内核对象，实现传统的后进先出（LIFO）队列，允许线程和 ISR 添加和移除任意大小的数据项。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的 LIFO（仅受可用 RAM 限制）。每个 LIFO 通过其内存地址引用。

LIFO 具有以下关键属性：

* 一个**队列**，保存已添加但尚未移除的数据项。队列实现为一个简单的链表。

LIFO 在使用前必须初始化。初始化会将队列置为空。

LIFO 数据项必须按指针要求对齐，因为内核保留数据项中第一个指针大小的字段，用作指向队列中下一个数据项的指针。因此，保存 N 字节应用数据的数据项需要 N+4（或 N+8）字节的内存。如果使用 :c:func:`k_lifo_alloc_put` 添加数据项，则数据项没有对齐或保留空间要求，改为从调用线程的资源池中临时分配额外内存。

.. note::
    LIFO 数据项在所有 LIFO 数据队列中只允许存在单个活跃实例。在数据项从其之前所在队列移除之前，任何试图将其重新添加到队列的操作都将导致未定义行为。

线程或 ISR 可以将数据项**添加**到 LIFO。如果存在等待线程，数据项会直接交给该等待线程；否则数据项被添加到 LIFO 的队列中。可入队的项数没有上限。

线程可以从 LIFO **移除**数据项。如果 LIFO 队列为空，线程可以选择等待数据项被给出。任意数量的线程可以同时等待一个空 LIFO。当数据项被添加时，它会被交给等待时间最长的最高优先级线程。

.. note::
    内核允许 ISR 从 LIFO 移除数据项，但如果 LIFO 为空，ISR 不得尝试等待。

实现
**************

定义 LIFO
==============

LIFO 使用类型为 :c:struct:`k_lifo` 的变量定义。之后必须通过调用 :c:func:`k_lifo_init` 进行初始化。

以下代码定义并初始化一个空 LIFO。

.. code-block:: c

    struct k_lifo my_lifo;

    k_lifo_init(&my_lifo);

或者，可以通过调用 :c:macro:`K_LIFO_DEFINE` 在编译时定义并初始化一个空 LIFO。

以下代码与上面代码段的效果相同。

.. code-block:: c

    K_LIFO_DEFINE(my_lifo);

写入 LIFO
================

通过调用 :c:func:`k_lifo_put` 将数据项添加到 LIFO。

以下代码基于上面的示例，使用 LIFO 向一个或多个消费者线程发送数据。

.. code-block:: c

    struct data_item_t {
        void *LIFO_reserved;   /* 1st word reserved for use by LIFO */
        ...
    };

    struct data_item_t tx data;

    void producer_thread(int unused1, int unused2, int unused3)
    {
        while (1) {
            /* create data item to send */
            tx_data = ...

            /* send data to consumers */
            k_lifo_put(&my_lifo, &tx_data);

            ...
        }
    }

可以使用 :c:func:`k_lifo_alloc_put` 将数据项添加到 LIFO。使用该 API 时，无需在数据项中为内核保留空间，改为在数据项被读取之前，从调用线程的资源池中分配额外内存。

从 LIFO 读取
==================

通过调用 :c:func:`k_lifo_get` 从 LIFO 移除数据项。

以下代码基于上面的示例，使用 LIFO 从生产者线程获取数据项，然后以某种方式处理。

.. code-block:: c

    void consumer_thread(int unused1, int unused2, int unused3)
    {
        struct data_item_t  *rx_data;

        while (1) {
            rx_data = k_lifo_get(&my_lifo, K_FOREVER);

            /* process LIFO data item */
            ...
        }
    }

建议使用
**************

使用 LIFO 以"后进先出"方式异步传输任意大小的数据项。

配置选项
*********************

相关配置选项：

* 无。

API 参考
*************

.. doxygengroup:: lifo_apis
