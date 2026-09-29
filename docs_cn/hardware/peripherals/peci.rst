.. _peci_api:

Platform
Environment
Control
Interface
（PECI）
#############################################

Overview
********
Platform
Environment
Control
Interface
缩写
为
PECI
是
2006
年
随
Intel
Core
2
Duo
Microprocessors
引入
的
thermal
management
standard。
PECI
interface
允许
外部
devices
读取
processor
temperature、
执行
processor
manageability
functions、
并
管理
processor
interface
tuning
和
diagnostics。
PECI
bus
driver
APIs
使
Embedded
Microcontrollers
和
CPUs
之间
的
interaction
成为
可能。

Configuration
Options
*********************

相关
配置
选项：

* :kconfig:option:`CONFIG_PECI`

API
Reference
*************

.. doxygengroup::
   peci_interface
