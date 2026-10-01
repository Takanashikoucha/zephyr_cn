.. _display_api:

显示
#######

Zephyr 中的显示子系统提供与广泛显示设备交互的统一方式。显示 API 是传输无关的：它描述你想让显示设备做什么，而不暴露数据如何在线路上移动。

MIPI 显示总线接口（DBI）
********************************

**MIPI DBI** 规范定义了若干用于连接主机到显示控制器的并行和串行总线。在 Zephyr 中，DBI 支持提供驱动内部用于实现通用 API 的总线级原语，包括命令写入、读取、像素传输、复位及相关操作。

应用不直接使用 DBI 函数。相反，它们调用通用显示 API（例如写入像素），显示驱动在底层处理 DBI 协议。

MIPI-DBI 定义 3 种接口类型：

* 类型 A：Motorola 6800 并行总线
* 类型 B：Intel 8080 并行总线
* 类型 C：SPI 类型串行位总线，有 3 个选项：

  #. 每字节 9 个写入时钟，最后一位是命令/数据选择位
  #. 与上述相同，但每字节 16 个写入时钟
  #. 每字节 8 个写入时钟。命令/数据通过 GPIO 引脚选择

目前，API 不支持每字节 16 个写入时钟的类型 C 控制器（选项 2）。

MIPI 显示串行接口（DSI）
***********************************

**MIPI DSI** 标准是为现代彩色 TFT 面板设计的高速差分串行总线。Zephyr 的 DSI 支持提供驱动在 DSI 链路上实现通用显示 API 所需的原语。

与 DBI 一样，应用从不直接调用 DSI 函数。它们通过使用通用显示 API 保持可移植性，而驱动在内部处理 DSI 事务。

API 参考
*************

通用显示接口
=========================

.. doxygengroup:: display_interface

.. _mipi_dbi_api:

MIPI 显示总线接口（DBI）
===============================

.. doxygengroup:: mipi_dbi_interface

.. _mipi_dsi_api:

MIPI 显示串行接口（DSI）
=================================

.. doxygengroup:: mipi_dsi_interface

Grove LCD 显示
================

.. doxygengroup:: grove_display

BBC micro:bit 显示
=====================

.. doxygengroup:: mb_display

单色字符帧缓冲
===============================

.. doxygengroup:: monochrome_character_framebuffer
