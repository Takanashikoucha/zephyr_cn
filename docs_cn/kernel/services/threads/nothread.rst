.. _nothread:

无线程运行
#########################

某些应用不需要线程支持：

* 引导加载器
* 简单的事件驱动应用
* 旨在演示核心功能的示例

通过将
:kconfig:option:`CONFIG_MULTITHREADING` 设置为 ``n`` 可以禁用
线程支持。由于此配置
对 Zephyr 的功能有重大影响，且测试
有限，因此对在此配置下
预期哪些功能可以正常工作存在条件。

预期可以正常工作的内容
****************************

当
:kconfig:option:`CONFIG_MULTITHREADING` 被禁用时，
以下核心能力应正确运行：

* :ref:`构建系统 <application>`

* 将应用启动到 ``main()`` 的能力

* :ref:`中断管理 <interrupts_v2>`

* 包括 :c:func:`k_uptime_get` 的系统时钟

* 定时器，即 :c:func:`k_timer`

* 非睡眠延迟，例如 :c:func:`k_busy_wait`。

* 睡眠 :c:func:`k_cpu_idle`。

* ``main()`` 之前的驱动程序和子系统初始化，例如 :c:macro:`SYS_INIT`。

* :ref:`kernel_memory_management_api`

* 特定子系统中明确标识的驱动程序，列于下方。

上述预期影响其他特性的选择；例如
:kconfig:option:`CONFIG_SYS_CLOCK_EXISTS` 不能设置为 ``n``。

预期无法正常工作
*******************************

当 :kconfig:option:`CONFIG_MULTITHREADING`
被禁用时无法工作的功能包括内核 API 的大部分：

* :ref:`threads_v2`

* :ref:`scheduling_v2`

* :ref:`workqueues_v2`

* :ref:`polling_v2`

* :ref:`semaphores_v2`

* :ref:`mutexes_v2`

* :ref:`condvar`

* :ref:`kernel_data_passing_api`

.. contents::
    :local:
    :depth: 1

无线程支持时的子系统行为
*****************************************

以下部分列出了在 :kconfig:option:`CONFIG_MULTITHREADING`
被禁用时预期在某种程度上正常工作的驱动程序和功能
子系统。未在此处列出的子系统不应预期
正常工作。

所列子系统中的某些现有驱动程序在
禁用线程时无法工作，但根据其子系统在范围内，
或者可能足够隔离，使得在特定
平台上支持它们影响较小。将
考虑增强以添加对原本未实现
在线程禁用时工作的现有能力的支持。

闪存（Flash）
=====

预期 :ref:`flash_api` 对所有 SoC 闪存外设驱动程序正常工作。总线访问的设备（如串行存储器）可能不受支持。

*支持的驱动程序列表/表格将放在此处*

通用输入输出（GPIO）
====

预期 :ref:`gpio_api` 对所有 SoC GPIO 外设驱动程序正常工作。总线访问的设备（如 GPIO 扩展器）可能不受支持。

*支持的驱动程序列表/表格将放在此处*

通用异步收发器（UART）
====

预期 :ref:`uart_api` 的子集对所有 SoC UART 外设驱动程序正常工作。

* 选择 :kconfig:option:`CONFIG_UART_INTERRUPT_DRIVEN` 的应用
  可能正常工作，取决于驱动程序实现。

* 选择 :kconfig:option:`CONFIG_UART_ASYNC_API` 的应用
  可能正常工作，取决于驱动程序实现。

* 未选择 :kconfig:option:`CONFIG_UART_ASYNC_API`
  或 :kconfig:option:`CONFIG_UART_INTERRUPT_DRIVEN` 的应用预期正常工作。

*支持的驱动程序列表/表格将放在此处，包括
支持哪些 API 选项*
