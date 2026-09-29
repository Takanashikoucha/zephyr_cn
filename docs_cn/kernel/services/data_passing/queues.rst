.. _queues:

队列
######

Zephyr 中的队列（Queue）是一种内核对象，实现了传统的队列，允许线程和中断服务程序（ISR）添加和移除任意大小的数据项。队列类似于 FIFO，同时作为 :ref:`k_fifo <fifos_v2>` 和 :ref:`k_lifo <lifos_v2>` 的底层实现。有关用法的更多信息，请参阅 :ref:`k_fifo <fifos_v2>`。

取消等待
*********

一个阻塞等待从队列中获取数据的线程，可以通过另一个线程或 ISR 调用 :c:func:`k_queue_cancel_wait` 来在没有数据项的情况下被释放。在队列上挂起的第一个线程将从其 :c:func:`k_queue_get` 调用中返回，返回值为 ``NULL``，效果与其超时到期完全相同。如果队列是通过 :c:func:`k_poll` 进行等待的，则该调用将返回 ``-EINTR``，且轮询事件处于已取消状态。

该机制也可通过 :c:macro:`k_fifo_cancel_wait` 和 :c:macro:`k_lifo_cancel_wait` 用于基于队列的原语。

配置选项
*********************

相关配置选项：

* 无

API 参考
*************

.. doxygengroup:: queue_apis
