.. _coredump_device_api:

Coredump
Device
###############

Overview
********

Coredump
device
是
一
个
pseudo-device
driver
有
两
种
类型。
A
COREDUMP_TYPE_MEMCPY
类型
暴露
device
tree
bindings
用于
memory
address/size
values
被
包含
在
任何
dump
中。
并且
driver
暴露
一
个
API
在
runtime
添加/移除
dump
memory
regions。
A
COREDUMP_TYPE_CALLBACK
device
要求
在
memory-regions
array
中
恰好
一
个
entry
带
size
为
0
和
期望
的
size。
Driver
将
静态
分配
期望
size
的
memory
并
提供
一
个
API
注册
一
个
callback
函数
在
dump
发生
时
填充
那
memory。

Configuration
Options
*********************

相关
配置
选项：

* :kconfig:option:`CONFIG_COREDUMP_DEVICE`

API
Reference
*************

.. doxygengroup::
   coredump_device_interface
