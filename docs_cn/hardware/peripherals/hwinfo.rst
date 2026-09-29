.. _hwinfo_api:

Hardware
Information
####################

Overview
********

HW
Info
API
提供
对
hardware
information
的
访问
如
device
identifiers
和
reset
cause
flags。

Reset
cause
flags
可以
用
来
确定
device
为什么
被
reset；
例如
因为
watchdog
timeout
或
因为
power
cycling。
不同
的
devices
支持
不同
的
flags
子集。
用
:c:func:`hwinfo_get_supported_reset_cause`
获取
该
device
支持
的
flags。

大多数
implementations
是
SoC
特定
的
从
vendor
registers
或
memory
读取
identifiers。
通用
的
:dtcompatible:`zephyr,hwinfo-nvmem`
backend
从
NVMEM
cells
获取
device
ID
并
可选
地
获取
EUI-64
（参考
:ref:`nvmem`）。

Configuration
Options
*********************

相关
配置
选项：

* :kconfig:option:`CONFIG_HWINFO`
* :kconfig:option:`CONFIG_HWINFO_NVMEM`

API
Reference
*************

.. doxygengroup::
   hwinfo_interface
