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

.. _migration_4.1:

Migration
guide
to
Zephyr
v4.1.0
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
v4.0.0
到
Zephyr
v4.1.0
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
notes<zephyr_4.1>`。

.. contents::
    :local:
    :depth:
    2

Build
System
************

*
Support
for
build
type
feature
它
在
Zephyr
3.6
中
被
deprecated
被
removed
:ref:`application-file-suffixes`/:ref:`sysbuild_file_suffixes`
replaced
这
个。

*
Sysbuild

   *
   Kconfig
   ``SB_CONFIG_MCUBOOT_MODE_SWAP_WITHOUT_SCRATCH``
   被
   deprecated
   并
   replaced
   with
   ``SB_CONFIG_MCUBOOT_MODE_SWAP_USING_MOVE``
   applications
   应该
   被
   updated
   用于
   select
   这
   个
   new
   symbol
   如果
   它们
   之前
   在
   select
   old
   的
   symbol。

BOSSA
Runner
=============

``bossac``
runner
changed
为
no
longer
在
flashing
时
default
做
full
erase。
要
perform
full
erase
在
executing
``west
flash``
时
pass
``--erase``
option。
