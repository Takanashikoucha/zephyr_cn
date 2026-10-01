.. _fifos_v2:

FIFO
#####

:dfn:`FIFO` 是一种内核对象，实现传统的先进先出（FIFO）队列，允许线程和 ISR 添加和移除任意大小的数据项。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的 FIFO（仅受可用 RAM 限制）。每个 FIFO 通过其内存地址引用。

FIFO 具有以下关键属性：

* 一个**队列**，保存已添加但尚未移除的数据项。队列实现为一个简单的链表。

FIFO 在使用前必须初始化。初始化会将队列置为空。

FIFO 数据项必须按指针要求对齐，因为内核保留数据项中第一个指针大小的字段，用作指向队列中下一个数据项的指针。因此，保存 N 字节应用数据的数据项需要 N+4（或 N+8）字节的内存。如果使用 :c:func:`k_fifo_alloc_put` 添加数据项，则数据项没有对齐或保留空间要求，改为从调用线程的资源池中临时分配额外内存。

.. note::
    FIFO 数据项在所有 FIFO 数据队列中只允许存在单个活跃实例。在数据项从其之前所在队列移除之前，任何试图将其重新添加到队列的操作都将导致未定义行为。

线程或 ISR 可以将数据项**添加**到 FIFO。如果存在等待线程，数据项会直接交给该等待线程；否则数据项被添加到 FIFO 的队列中。可入队的项数没有上限。

线程可以从 FIFO **移除**数据项。如果 FIFO 队列为空，线程可以选择等待数据项被给出。任意数量的线程可以同时等待一个空 FIFO。当数据项被添加时，它会被交给等待时间最长的最高优先级线程。

.. note::
    内核允许 ISR 从 FIFO 移除数据项，但如果 FIFO 为空，ISR 不得尝试等待。

如有需要，如果多个数据项被链接成一个单链表，可以在一次操作中向 FIFO **添加多个数据项**。如果多个写者正在向 FIFO 添加一组相关联的数据项，此能力非常有用，因为它可确保每组中的数据项不会与其他数据项交错。一次添加多个数据项比逐个添加效率更高，并且可以保证移除某组中第一个数据项的人无需等待即可移除该组中剩余的数据项。

实现
**************

定义 FIFO
==============

FIFO 使用类型为 :c:struct:`k_fifo` 的变量定义。之后必须通过调用 :c:func:`k_fifo_init` 进行初始化。

以下代码定义并初始化一个空 FIFO。

.. code-block:: c

    struct k_fifo my_fifo;

    k_fifo_init(&my_fifo);

或者，可以通过调用 :c:macro:`K_FIFO_DEFINE` 在编译时定义并初始化一个空 FIFO。

以下代码与上面代码段的效果相同。

.. code-block:: c

    K_FIFO_DEFINE(my_fifo);

写入 FIFO
================

通过调用 :c:func:`k_fifo_put` 将数据项添加到 FIFO。

以下代码基于上面的示例，使用 FIFO 向一个或多个消费者线程发送数据。

.. code-block:: c

    struct data_item_t {
        void *fifo_reserved;   /* 1st word reserved for use by FIFO */
        ...
    };

    struct data_item_t tx_data;

    void producer_thread(int unused1, int unused2, int unused3)
    {
        while (1) {
            /* create data item to send */
            tx_data = ...

            /* send data to consumers */
            k_fifo_put(&my_fifo, &tx_data);

            ...
        }
    }

此外，可以通过调用 :c:func:`k_fifo_put_list` 或 :c:func:`k_fifo_put_slist` 将单链表形式的多个数据项添加到 FIFO。

最后，可以使用 :c:func:`k_fifo_alloc_put` 将数据项添加到 FIFO。使用该 API 时，无需在数据项中为内核保留空间，改为在数据项被读取之前，从调用线程的资源池中分配额外内存。

从 FIFO 读取
==================

通过调用 :c:func:`k_fifo_get` 从 FIFO 移除数据项。

以下代码基于上面的示例，使用 FIFO 从生产者线程获取数据项，然后以某种方式处理。

.. code-block:: c

    void consumer_thread(int unused1, int unused2, int unused3)
    {
        struct data_item_t  *rx_data;

        while (1) {
            rx_data = k_fifo_get(&my_fifo, K_FOREVER);

            /* process FIFO data item */
            ...
        }
    }

建议使用
**************

使用 FIFO 以"先进先出"方式异步传输任意大小的数据项。

配置选项
*********************

相关配置选项：

* 无

API 参考
*************

.. doxygengroup:: fifo_apis
