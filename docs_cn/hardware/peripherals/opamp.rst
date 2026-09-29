.. _opamp_api:

Operational
Amplifier
（OPAMP）
#############################

Overview
********

Operational
amplifier
是
一
个
analog
device
它
放大
differential
input
signals
（inverting
和
non-inverting
input
之间
的
difference）
给出
resulting
output
voltage。


Configuration
*************

当
OPAMP
被
启用
时
应该
用
devicetree
提供
初始
configuration。
OPAMP
gain
可以
在
runtime
调整。

相关
配置
选项：

* :kconfig:option:`CONFIG_OPAMP`

API
Reference
*************

.. doxygengroup::
   opamp_interface
