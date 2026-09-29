.. _flash_api:

Flash
#####

Overview
********

**Flash
offset
concept**

用户
API
使用
的
offsets
用
相对
于
flash
memory
beginning
address
的
关系
表达。
这
个
规则
应该
被
应用
到
所有
flash
controller
regular
memory
其
layout
可以
通过
API
获取
pages
的
layout
（参考
:kconfig:option:`CONFIG_FLASH_PAGE_LAYOUT`）。

这
个
规则
的
exception
可以
应用
于
vendor
特定
的
flash
dedicated-purpose
region
（这样
的
region
显然
不
能
被
覆盖
在
获取
pages
layout
的
API
下）。



User
API
Reference
******************
.. doxygengroup::
   flash_interface

Implementation
interface
API
Reference
**************************************
.. doxygengroup::
   flash_internal_interface
