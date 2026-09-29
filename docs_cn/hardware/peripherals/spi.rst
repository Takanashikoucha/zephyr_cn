.. _spi_api:

Serial
Peripheral
Interface
（SPI）
Bus
#####################################

Overview
********

Terminology
============

Zephyr
SPI
API
使用
由
:ref:`coding_guideline_inclusive_language`
选择
的
inclusive
terminology
遵循
`OSHWA
resolution
to
redefine
SPI
signal
names`_：

* 驱动
  clock
  的
  device
  是
  *controller*
  它
  寻址
  的
  devices
  是
  *peripherals*
  （参考
  :c:macro:`SPI_OP_MODE_CONTROLLER`
  和
  :c:macro:`SPI_OP_MODE_PERIPHERAL`）。
* Data
  signals
  从
  每个
  device
  自己
  的
  perspective
  命名：
  *SDO*
  （Serial
  Data
  Out）
  和
  *SDI*
  （Serial
  Data
  In）
  以及
  *CS*
  （Chip
  Select）
  用于
  select
  line。

之前
的
master/slave
和
MOSI/MISO
names
仍
可
用
作为
compatibility
aliases。
它们
自
Zephyr
v4.5
起
被
deprecated
并
将
在
Zephyr
v5.0
中
被
移除。

.. _OSHWA
   resolution
   to
   redefine
   SPI
   signal
   names:
   https://oshwa.org/resources/a-resolution-to-redefine-spi-signal-names/

API
Reference
*************

.. doxygengroup::
   spi_interface
