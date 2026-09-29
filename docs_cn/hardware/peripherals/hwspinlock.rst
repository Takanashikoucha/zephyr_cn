.. _hwspinlock_api:

Hardware
Spinlocks
（HWSPINLOCK）
###############################

Overview
********

HWSPINLOCK
device
是
用
来
保护
system
中
跨
clusters
的
shared
resources
的
peripheral。
每个
HWSPINLOCK
instance
提供
一
个
或
多
个
spinlocks。
API
类似
于
regular
zephyr
spinlocks。

.. doxygengroup::
   spinlock_apis

因为
我们
也
想
保护
spinlock
resource
被
同一
cluster
中
的
多
个
cores
使用，
每个
HWSPINLOCK
device
包含
一
个
regular
zephyr
spinlock
并
用
它
lock
对
HWSPINLOCK
hardware
的
access。

API
Reference
*************

.. doxygengroup::
   hwspinlock_interface
