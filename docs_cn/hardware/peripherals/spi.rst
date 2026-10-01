.. _spi_api:

串行外设接口（SPI）总线
#####################################

概述
********

术语
===========

Zephyr SPI API 使用 :ref:`coding_guideline_inclusive_language` 选择的包容性术语，遵循 `OSHWA 重新定义 SPI 信号名称的决议`_：

* 驱动时钟的设备是*控制器*，它寻址的设备是*外设*（参见 :c:macro:`SPI_OP_MODE_CONTROLLER` 和 :c:macro:`SPI_OP_MODE_PERIPHERAL`）。
* 数据信号从每个设备自身视角命名：*SDO*（串行数据输出）和 *SDI*（串行数据输入），选择线用 *CS*（片选）。

前主/从和 MOSI/MISO 名称仍可作为兼容性别名使用。它们自 Zephyr v4.5 起弃用，将在 Zephyr v5.0 中移除。

.. _OSHWA resolution to redefine SPI signal names:
    https://oshwa.org/resources/a-resolution-to-redefine-spi-signal-names/

API 参考
*************

.. doxygengroup:: spi_interface
