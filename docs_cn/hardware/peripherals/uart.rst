.. _uart_api:

通用异步收发器（UART）
##################################################

概述
********

Zephyr 提供三种不同的方式来访问 UART 外设。根据所选方法，不同的 API 函数按以下章节使用：

1. :ref:`uart_polling_api`
2. :ref:`uart_interrupt_api`
3. :ref:`uart_async_api` 使用 :ref:`dma_api`

轮询（Polling）是访问 UART 外设最基本的方法。读取函数 :c:func:`uart_poll_in` 是非阻塞函数，当没有有效数据可用时返回一个字符或 ``-1``。写入函数 :c:func:`uart_poll_out` 是阻塞函数，线程会等待直到给定字符被发送。

使用中断驱动 API，可能较慢的通信可以在后台进行，同时线程继续执行其他任务。内核的 :ref:`kernel_data_passing_api` 特性可用于线程与 UART 驱动程序之间通信。

异步 API 允许使用 DMA 在后台读取和写入数据，完全不中断 MCU。然而，其设置比其他方法更复杂。

.. warning::

   中断驱动 API 和异步 API 不应同时用于同一硬件外设，因为两个 API 都需要硬件中断才能正常工作。同时使用两个 API 的回调会导致相互干扰。:kconfig:option:`CONFIG_UART_EXCLUSIVE_API_CALLBACKS` 默认启用，使得任一时刻只有与一个 API 关联的回调处于激活状态。


配置选项
*********************

最重要的是，Kconfig 选项定义是否可以使用轮询 API（默认）、中断驱动 API 或异步 API。仅启用你需要的功能，以最小化内存占用。

相关配置选项：

* :kconfig:option:`CONFIG_SERIAL`
* :kconfig:option:`CONFIG_UART_INTERRUPT_DRIVEN`
* :kconfig:option:`CONFIG_UART_ASYNC_API`
* :kconfig:option:`CONFIG_UART_WIDE_DATA`
* :kconfig:option:`CONFIG_UART_USE_RUNTIME_CONFIGURE`
* :kconfig:option:`CONFIG_UART_LINE_CTRL`
* :kconfig:option:`CONFIG_UART_DRV_CMD`


API 参考
*************

.. doxygengroup:: uart_interface


.. _uart_polling_api:

轮询 API
===========

.. doxygengroup:: uart_polling


.. _uart_interrupt_api:

中断驱动 API
================

.. doxygengroup:: uart_interrupt


.. _uart_async_api:

异步 API
================

.. doxygengroup:: uart_async
