.. _espi_api:

Enhanced
Serial
Peripheral
Interface
（eSPI）
Bus
###############################################

Overview
********

eSPI
（enhanced
serial
peripheral
interface）
是
基于
SPI
的
serial
bus。
它
也
有
four-wire
interface
（receive、
transmit、
clock
和
target
select）
和
三
个
configurations：
single
IO、
dual
IO
和
quad
IO。

技术
进步
包括
更低
的
voltage
signal
levels
（1.8V
vs.
3.3V）、
更少
的
pin
count、
以及
frequency
是
两倍
快
（66MHz
vs.
33MHz）
因为
其
enhancements，
eSPI
被
用
来
替换
LPC
（lower
pin
count）
interface、
SPI、
SMBus
和
sideband
signals。

参考
`eSPI
interface
specification`_
获取
额外
细节。


API
Reference
*************

.. doxygengroup::
   espi_interface

.. _eSPI
   interface
   specification:
   https://downloadmirror.intel.com/27055/327432%20espi_base_specification%20R1-5.pdf
