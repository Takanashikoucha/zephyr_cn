.. _retained_mem_api:

Retained
Memory
###############

Overview
********

Retained
memory
driver
API
提供
从
memory
areas
read/write
的
方式
其中
memory
的
contents
在
device
被
powered
期间
被
retained
（data
可能
在
low
power
modes
中
丢失）。

Configuration
Options
*********************

相关
配置
选项：

* :kconfig:option:`CONFIG_RETAINED_MEM`
* :kconfig:option:`CONFIG_RETAINED_MEM_INIT_PRIORITY`
* :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE`

Mutex
protection
****************

Retained
memory
drivers
的
Mutex
protection
在
应用
被
编译
带
multithreading
support
时
默认
被
启用。
这
意味着
不同
的
threads
可以
安全
地
调用
retained
memory
functions
而
不
与
其他
concurrent
thread
function
usage
clash
但
意味着
retained
memory
functions
不
能
从
ISRs
使用。
可以
通过
启用
:kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE`
全局
禁用
所有
retained
memory
drivers
的
mutex
protection
—
users
然后
负责
确保
function
calls
不
相互
conflict。

API
Reference
*************

.. doxygengroup::
   retained_mem_interface
