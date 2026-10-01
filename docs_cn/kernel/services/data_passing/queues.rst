.. _queues:

队列
######

Zephyr 中的队列是一种内核对象，用于实现传统的队列，允许线程和 ISR 添加和移除任意大小的数据项。队列类似于 FIFO，同时作为 :ref:`k_fifo <fifos_v2>` 和 :ref:`k_lifo <lifos_v2>` 的底层实现。有关更多使用信息，参见 :ref:`k_fifo <fifos_v2>`。

取消等待
*****************

一个正在阻塞等待从队列中取出数据项的线程，可以不经由任何数据项就被释放：从另一个线程或 ISR 调用 :c:func:`k_queue_cancel_wait` 即可实现。第一个在该队列上挂起的线程将从其 :c:func:`k_queue_get` 调用中返回一个 ``NULL`` 值，效果与其超时到期完全相同。如果该队列是通过 :c:func:`k_poll` 进行等待的，则该调用会返回 ``-EINTR``，且对应的 poll 事件处于被取消的状态。

此机制也可通过 :c:macro:`k_fifo_cancel_wait` 和 :c:macro:`k_lifo_cancel_wait` 用于基于队列的原语。

配置选项
*********************

相关配置选项：

* 无

API 参考
*************

.. doxygengroup:: queue_apis
