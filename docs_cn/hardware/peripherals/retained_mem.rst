.. _retained_mem_api:

保留内存
###############

概述
********

保留内存（retained memory）驱动程序 API 提供了一种读写内存区域的方式，这些内存区域的内容在设备通电期间会保留（在低功耗模式下数据可能会丢失）。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_RETAINED_MEM`
* :kconfig:option:`CONFIG_RETAINED_MEM_INIT_PRIORITY`
* :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE`

互斥锁保护
****************

当应用程序以多线程支持编译时，保留内存驱动程序的互斥锁（mutex）保护默认启用。这意味着不同的线程可以安全地调用保留内存函数，而不会与其他并发线程的函数使用发生冲突；但也意味着保留内存函数不能在中断服务程序（ISR）中使用。可以通过启用 :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE` 在所有保留内存驱动程序上全局禁用互斥锁保护——此时用户需自行确保各函数调用之间互不冲突。

API 参考
*************

.. doxygengroup:: retained_mem_interface
