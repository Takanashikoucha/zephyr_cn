.. _task_wdt_api:

Task Watchdog
#############

Overview
********

许多微控制器都带有硬件看门狗定时器外设。它的目的是在发生严重软件故障时触发某个动作（通常是系统复位）。初始化之后，看门狗定时器必须定期被重启（即"喂狗"），以防止其超时。如果软件卡住、无法再喂狗，则纠正性动作会被触发，使系统恢复正常运行。

在多个任务并行运行的实时操作系统中，单个看门狗实例可能已经不够用了，因为它只能用于一个任务。这个基于内核定时器的软件看门狗提供了一种方法来监管多个线程或任务（称为看门狗通道）。

一个已有的硬件看门狗可以作为可选的后备手段，用于处理任务看门狗本身或调度器发生故障的情况。

任务看门狗使用内核定时器作为其后端。如果配置得当，定时器 ISR 在正常运行期间实际上永远不会被调用，因为定时器会在喂狗调用中被持续更新。

目前尚不支持多个任务看门狗实例。相反，任务看门狗 API 可以全局访问，用于添加或删除新通道，而无需在固件中传递上下文或设备指针。

通道最大数量通过 Kconfig 预先定义，应调整为与应用所需的通道数量完全一致。

Configuration Options
*********************

相关配置选项可在 :zephyr_file:`subsys/task_wdt/Kconfig` 中找到。

* :kconfig:option:`CONFIG_TASK_WDT`

* :kconfig:option:`CONFIG_TASK_WDT_CHANNELS`

* :kconfig:option:`CONFIG_TASK_WDT_HW_FALLBACK`

* :kconfig:option:`CONFIG_TASK_WDT_MIN_TIMEOUT`

* :kconfig:option:`CONFIG_TASK_WDT_HW_FALLBACK_DELAY`

API Reference
*************

.. doxygengroup:: task_wdt_api
