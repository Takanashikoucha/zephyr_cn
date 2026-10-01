.. _hwinfo_api:

硬件信息
####################

概述
********

硬件信息 API 提供对硬件信息（如设备标识符和复位原因标志）的访问。

复位原因标志可用于确定设备为何被复位；例如由于看门狗超时或电源循环。不同设备支持不同的标志子集。使用 :c:func:`hwinfo_get_supported_reset_cause` 获取该设备支持的标志。

大多数实现是 SoC 特定的，从厂商寄存器或内存读取标识符。通用 :dtcompatible:`zephyr,hwinfo-nvmem` 后端从 NVMEM 单元获取设备 ID，以及可选的 EUI-64（参见 :ref:`nvmem`）。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_HWINFO`
* :kconfig:option:`CONFIG_HWINFO_NVMEM`

API 参考
*************

.. doxygengroup:: hwinfo_interface
