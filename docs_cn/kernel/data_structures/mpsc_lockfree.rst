.. _mpsc_lockfree:

多生产者单消费者无锁队列
==============================================

:dfn:`多生产者单消费者无锁队列（MPSC）`是一种无锁侵入式队列，
基于 Dmitry Vyukov 在 `1024cores <https://www.1024cores.net/home/lock-free-algorithms/queues/intrusive-mpsc-node-based-queue>`_
中描述的原子指针交换（atomic pointer swap）实现。


API 参考
*************

.. doxygengroup:: mpsc_lockfree
