.. _message_queues_v2:

消息队列
##############

:dfn:`消息队列`是一种内核对象，实现简单的消息队列，
允许线程和 ISR 异步收发固定大小的数据项。

.. contents::
    :local:
    :depth: 2

概念
********

可以定义任意数量的消息队列（仅受可用 RAM 限制）。
每个消息队列通过其内存地址引用。

消息队列具有以下关键属性：

* 一个**环形缓冲区**，保存已发送但尚未接收的数据项。

* 一个以字节计的**数据项大小**。

* 环形缓冲区中可入队的**最大数量**数据项。

消息队列在使用前必须初始化。
初始化会将环形缓冲区置为空。

线程或 ISR 可以将数据项**发送**到消息队列。
发送线程所指向的数据项会被复制到等待线程（如有）；
否则，如果有可用空间，数据项被复制到消息队列的环形缓冲区。
无论哪种情况，被发送的数据区大小
*必须*等于消息队列的数据项大小。

如果线程在环形缓冲区满时尝试发送数据项，
发送线程可以选择等待空间可用。
环形缓冲区满时，任意数量的发送线程
可以同时等待；当空间可用时，
它被交给等待时间最长的最高优先级发送线程。

线程可以从消息队列**接收**数据项。
数据项被复制到接收线程指定的区域；
接收区大小*必须*等于消息队列的数据项大小。

如果线程在环形缓冲区为空时尝试接收数据项，
接收线程可以选择等待数据项被发送。
环形缓冲区为空时，任意数量的接收线程
可以同时等待；当数据项可用时，
它被交给等待时间最长的最高优先级接收线程。

线程还可以**窥视**消息队列头部的消息，
而不将其从队列中移除。
数据项被复制到接收线程指定的区域；
接收区大小*必须*等于消息队列的数据项大小。

.. note::
    内核允许 ISR 从消息队列接收数据项，
    但如果消息队列为空，ISR 不得尝试等待。

.. note::
    消息队列的环形缓冲区不需要对齐。
    底层实现使用 :c:func:`memcpy`（与对齐无关），
    且不暴露任何内部指针。

实现
**************

定义消息队列
========================

消息队列使用类型为 :c:struct:`k_msgq` 的变量定义。
之后必须通过调用 :c:func:`k_msgq_init` 进行初始化。

以下代码定义并初始化一个空消息队列，
该队列可容纳 10 个项目，每项 12 字节长。

.. code-block:: c

    struct data_item_type {
        uint32_t field1;
	uint32_t field2;
	uint32_t field3;
    };

    char my_msgq_buffer[10 * sizeof(struct data_item_type)];
    struct k_msgq my_msgq;

    k_msgq_init(&my_msgq, my_msgq_buffer, sizeof(struct data_item_type), 10);

或者，可以通过调用以下宏之一
在编译时定义并初始化一个消息队列：

* :c:macro:`K_MSGQ_DEFINE` -- 定义一个公共消息队列。
* :c:macro:`K_MSGQ_DEFINE_STATIC` -- 定义一个私有
  （静态作用域）消息队列。
* :c:macro:`K_MSGQ_DEFINE_TYPE` -- 为给定项类型
  定义一个公共消息队列。
* :c:macro:`K_MSGQ_DEFINE_STATIC_TYPE` -- 为给定项类型
  定义一个私有消息队列。

以下代码与上面代码段的效果相同。注意
该宏同时定义了消息队列及其缓冲区。

.. code-block:: c

    K_MSGQ_DEFINE(my_msgq, sizeof(struct data_item_type), 10, 1);

如果队列项类型在编译时已知，
可以使用 :c:macro:`K_MSGQ_DEFINE_TYPE` 简写。
该宏自动配置队列项大小和对齐：

.. code-block:: c

    K_MSGQ_DEFINE_TYPE(my_msgq, struct data_item_type, 10);

写入消息队列
==========================

通过调用 :c:func:`k_msgq_put` 将数据项添加到消息队列。

以下代码基于上面的示例，使用消息队列
将数据项从生产者线程传递给一个或多个消费者线程。
如果消费者跟不上导致消息队列填满，
生产者线程丢弃所有现有数据，
以便保存较新的数据。注意该 api 会触发重新调度。

.. code-block:: c

    void producer_thread(void)
    {
        struct data_item_type data;

        while (1) {
            /* create data item to send (e.g. measurement, timestamp, ...) */
            data = ...

            /* send data to consumers */
            while (k_msgq_put(&my_msgq, &data, K_NO_WAIT) != 0) {
                /* message queue is full: purge old data & try again */
                k_msgq_purge(&my_msgq);
            }

            /* data item was successfully added to message queue */
        }
    }

从消息队列读取
===========================

通过调用 :c:func:`k_msgq_get` 从消息队列取出数据项。

以下代码基于上面的示例，使用消息队列
处理一个或多个生产者线程生成的数据项。注意
:c:func:`k_msgq_get` 的返回值应当检查，
因为 :c:func:`k_msgq_purge` 可能导致
返回 ``-ENOMSG``。

.. code-block:: c

    void consumer_thread(void)
    {
        struct data_item_type data;

        while (1) {
            /* get a data item */
            k_msgq_get(&my_msgq, &data, K_FOREVER);

            /* process data item */
            ...
        }
    }


窥视消息队列
===========================

通过调用 :c:func:`k_msgq_peek` 从消息队列读取数据项。

以下代码窥视消息队列，读取由一个或多个
生产者线程生成的、位于队列头部的数据项。

.. code-block:: c

    void consumer_thread(void)
    {
        struct data_item_type data;

        while (1) {
            /* read a data item by peeking into the queue */
            k_msgq_peek(&my_msgq, &data);

            /* process data item */
            ...
        }
    }

建议使用
**************

使用消息队列以异步方式
在线程之间传输小型数据项。

.. note::
    如有需要，消息队列可用于传输大型数据项。
    但是，在数据项写入或读取期间中断被锁定，
    这可能会增加中断延迟。由于数据项
    被整体从内存缓冲区复制或复制到内存，
    写入或读取数据项所花费的时间
    随其大小线性增长。因此，
    通常更倾向于通过交换指向数据项的指针
    而非数据项本身来传输大型数据项。

    可以通过使用内核的邮箱对象类型
    实现同步传输。

配置选项
*********************

相关配置选项：

* 无。

API 参考
*************

.. doxygengroup:: msgq_apis
