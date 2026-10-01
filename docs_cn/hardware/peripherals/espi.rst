.. _espi_api:

增强串行外设接口（eSPI）总线
###############################################

概述
********

eSPI（增强串行外设接口）是基于 SPI 的串行总线。它具有四线接口（接收、发送、时钟和目标选择）以及三种配置：单 IO、双 IO 和四 IO。

技术改进包括更低的电压信号电平（1.8V 对比 3.3V）、更少的引脚数量，以及频率提升一倍（66MHz 对比 33MHz）。由于这些增强特性，eSPI 被用于替代 LPC（较少引脚计数）接口、SPI、SMBus 和边带信号。

参见 `eSPI 接口规范`_ 获取更多细节。


API 参考
*************

.. doxygengroup:: espi_interface

.. _eSPI interface specification:
    https://downloadmirror.intel.com/27055/327432%20espi_base_specification%20R1-5.pdf
