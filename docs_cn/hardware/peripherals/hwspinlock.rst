.. _hwspinlock_api:

硬件自旋锁（HWSPINLOCK）
###############################

概述
********

HWSPINLOCK 设备是一种用于保护系统中跨集群共享资源的外设。
每个 HWSPINLOCK 实例提供一个或多个自旋锁，其 API 与 Zephyr 常规自旋锁类似。

.. doxygengroup:: spinlock_apis

由于我们希望保护自旋锁资源被同一集群中的多个内核使用，
每个 HWSPINLOCK 设备都包含一个 Zephyr 常规自旋锁，并用它锁定对 HWSPINLOCK 硬件的访问。

API 参考
*************

.. doxygengroup:: hwspinlock_interface
