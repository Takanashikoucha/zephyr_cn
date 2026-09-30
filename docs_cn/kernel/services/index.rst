.. _kernel_api:

内核服务
########

Zephyr 内核位于每个 Zephyr 应用的核心。
它提供低开销、高性能的多线程执行环境，
并拥有丰富的可用功能。Zephyr 生态系统的其余部分——
包括设备驱动、网络栈和应用特定代码——
利用内核功能构建完整应用。

内核的可配置特性允许你仅纳入应用所需的功能，
使其非常适合内存有限的系统（低至 2 KB！）
或具有简单多线程需求的系统
（如一组中断处理程序和单个后台任务）。
此类系统的示例包括：嵌入式传感器集线器、环境传感器、
简单 LED 可穿戴设备和商店库存标签。

需要更多内存（50 到 900 KB）、多个通信设备
（如 Wi-Fi 和蓝牙低功耗）和复杂多线程的应用，
也可以使用 Zephyr 内核开发。
此类系统的示例包括：健身可穿戴设备、智能手表和物联网无线网关。

调度、中断和同步
******************

以下页面涵盖与线程调度和同步相关的基本内核服务。

.. toctree::
   :maxdepth: 1

   threads/index
   scheduling/index
   threads/system_threads
   threads/workqueue
   threads/nothread
   interrupts
   polling
   synchronization/semaphores
   synchronization/locks
   synchronization/kpoll
   synchronization/condvars
   synchronization/futex

线程
****

.. toctree::
   :maxdepth: 1

   threads/index

调度
****

.. toctree::
   :maxdepth: 1

   scheduling/index

同步
****

.. toctree::
   :maxdepth: 1

   synchronization/index

内存分配
********

.. toctree::
   :maxdepth: 1

   memory_allocation/index

数据传递
********

.. toctree::
   :maxdepth: 1

   data_passing/index


.. note::

   以下为原文（待翻译）


.. [#f6] Data item size must be a multiple of the data alignment.

.. toctree::
   :maxdepth: 1

   data_passing/queues.rst
   data_passing/fifos.rst
   data_passing/lifos.rst
   data_passing/stacks.rst
   data_passing/message_queues.rst
   data_passing/mailboxes.rst
   data_passing/pipes.rst

.. _kernel_memory_management_api:

Memory Management
*****************

See :ref:`memory_management_api`.

Timing
******

These pages cover timing related services.

.. toctree::
   :maxdepth: 1

   timing/clocks.rst
   timing/timers.rst
   timing/system_timer_drivers.rst

Other
*****

These pages cover other kernel services.

.. toctree::
   :maxdepth: 1

   other/atomic.rst
   other/float.rst
   other/version.rst
   other/assert.rst
   other/fatal.rst
   other/thread_local_storage.rst
