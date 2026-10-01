.. _crc:

CRC
###

Overview
********

CRC subsystem 为各种 Cyclic Redundancy Check algorithms
提供 software 实现（用于 data integrity 验证。
CRCs 常用于检测存储和 communication systems 中 data 的意外变更。

Subsystem 提供全面的 CRC algorithms 集合（包括 CRC-4、CRC-7、CRC-8、CRC-16、
CRC-24 和 CRC-32 variants（且可用时提供可选 hardware 加速支持。

.. note::
   此 library 区别于 :ref:`CRC hardware driver API <crc_api>`（其提供
   硬件 CRC 加速 peripherals 的
   interface。

   当有硬件 CRC unit 且 Devicetree 的
   ``/chosen`` node 中已设置 ``zephyr,crc`` property 时（library functions 默认
   用硬件
   加速以获得更好 performance（可设置
   :kconfig:option:`CONFIG_CRC_HW_HANDLER` 为 ``n`` 禁用）。

Usage
=====

要计算 CRC（包含适当 header 并调用期望 function：

.. code-block:: c

   #include <zephyr/sys/crc.h>

   uint8_t data[] = {0x01, 0x02, 0x03, 0x04};
   uint32_t checksum = crc32_ieee(data, sizeof(data));

对分块处理的 streaming data（用 "update" variants：

.. code-block:: c

   uint32_t crc = 0;
   crc = crc32_ieee_update(crc, chunk1, len1);
   crc = crc32_ieee_update(crc, chunk2, len2);
   /* Final CRC value is in 'crc' */

通用 :c:func:`crc_by_type` function 提供在
runtime 选择 CRC algorithm 的统一 interface。

Configuration
*************

相关 configuration options：

* :kconfig:option:`CONFIG_CRC` - 启用 CRC 支持
* :kconfig:option:`CONFIG_CRC_HW_HANDLER` - 启用硬件 CRC 加速
* :kconfig:option:`CONFIG_CRC_SHELL` - 启用 CRC shell commands
* :kconfig:option-regex:`CONFIG_CRC[0-9].*` - 启用特定 CRC
  algorithms 的 software 实现

API Reference
*************

.. doxygengroup:: crc
