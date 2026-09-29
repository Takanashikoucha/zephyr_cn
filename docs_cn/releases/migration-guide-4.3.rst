:orphan:

..
   See
   https://docs.zephyrproject.org/latest/releases/index.html#migration-guides
   获取
   这
   个
   document
   应该
   contain
   什么
   的
   details。

.. _migration_4.3:

Migration
guide
to
Zephyr
v4.3.0
################################

这
个
document
describe
migrating
你
的
application
从
Zephyr
v4.2.0
到
Zephyr
v4.3.0
required
的
changes。

其他
changes
（不
directly
related
to
migrating
applications）
可以
found
在
:ref:`release
notes<zephyr_4.3>`。

.. contents::
    :local:
    :depth:
    2

Build
System
************

Kernel
******

*
:c:func:`device_init`
Earlier
releases
在
device
init
failure
时
return
一
个
positive
+errno
value
因为
一
个
bug。
这
now
被
fixed
用于
return
correct
的
negative
-errno
value。
Applications
它们
为
这
个
issue
implement
了
workarounds
应该
now
update
它们
的
code
accordingly。

Base
Libraries
**************

*
UTF
8
utils
declarations
(:c:func:`utf8_trunc`、
:c:func:`utf8_lcpy`)
被
moved
from
``util.h``
到
separate
的
:zephyr_file:`include/zephyr/sys/util_utf8.h`
file。
