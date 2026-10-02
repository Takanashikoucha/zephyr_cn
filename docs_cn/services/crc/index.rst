.. _crc:

CRC
###

概述
********

CRC 子系统提供多种循环冗余校验（Cyclic Redundancy Check）算法的软件实现，用于数据完整性验证。
CRC 常用于检测存储和通信系统中数据的意外变更。

该子系统提供了一整套 CRC 算法，包括 CRC-4、CRC-7、CRC-8、CRC-16、
CRC-24 和 CRC-32 的各种变体，并在可用时提供可选的硬件加速支持。

.. note::
   本库与 :ref:`CRC 硬件驱动 API <crc_api>` 不同，后者提供访问硬件 CRC 加速外设的接口。

   当硬件 CRC 单元可用且设备树（Devicetree）的 ``/chosen`` 节点中已设置 ``zephyr,crc``
   属性时，库函数将默认使用硬件加速以提升性能（可通过将
   :kconfig:option:`CONFIG_CRC_HW_HANDLER` 设置为 ``n`` 来禁用）。

用法
=====

要计算 CRC，请包含相应头文件并调用所需函数：

.. code-block:: c

   #include <zephyr/sys/crc.h>

   uint8_t data[] = {0x01, 0x02, 0x03, 0x04};
   uint32_t checksum = crc32_ieee(data, sizeof(data));

对于分块处理的流式数据，请使用 "update" 变体函数：

.. code-block:: c

   uint32_t crc = 0;
   crc = crc32_ieee_update(crc, chunk1, len1);
   crc = crc32_ieee_update(crc, chunk2, len2);
   /* Final CRC value is in 'crc' */

通用 :c:func:`crc_by_type` 函数提供统一接口，可在运行时选择 CRC 算法。

配置
*************

相关配置选项：

* :kconfig:option:`CONFIG_CRC` - 启用 CRC 支持
* :kconfig:option:`CONFIG_CRC_HW_HANDLER` - 启用硬件 CRC 加速
* :kconfig:option:`CONFIG_CRC_SHELL` - 启用 CRC shell 命令
* :kconfig:option-regex:`CONFIG_CRC[0-9].*` - 启用特定 CRC
  算法的软件实现

API 参考
*************

.. doxygengroup:: crc
