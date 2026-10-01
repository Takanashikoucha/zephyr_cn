.. _coredump_device_api:

核心转储设备
###############

概述
********

核心转储（coredump）设备是一种伪设备驱动，有两种类型。COREDUMP_TYPE_MEMCPY 类型通过设备树绑定（bindings）暴露内存地址/大小值，这些值将被包含在任何转储中；该驱动还提供 API 在运行时添加/移除转储内存区域。COREDUMP_TYPE_CALLBACK 类型要求在 memory-regions 数组中恰好有一个大小（size）为 0 且带有期望大小的条目。驱动会静态分配期望大小的内存，并提供 API 注册一个回调函数，在发生转储时填充该内存。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_COREDUMP_DEVICE`

API 参考
*************

.. doxygengroup:: coredump_device_interface
