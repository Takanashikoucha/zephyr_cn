.. _reset_api:

Reset
Controller
################

Overview
********

Reset
controllers
是
控制
向
多
个
peripherals
的
reset
signals
的
units。
Reset
controller
API
允许
peripheral
drivers
请求
对
它们
的
reset
input
signals
的
control
包括
assert、
deassert
和
toggle
那些
signals
的
能力。
此外
reset
input
signal
的
reset
status
可以
被
check。

主要
地
line_assert
和
line_deassert
API
functions
是
optional
的
因为
在
大多数
情况
下
我们
想
toggle
reset
signals。

Configuration
Options
*********************

相关
配置
选项：

* :kconfig:option:`CONFIG_RESET`

API
Reference
*************

.. doxygengroup::
   reset_controller_interface
