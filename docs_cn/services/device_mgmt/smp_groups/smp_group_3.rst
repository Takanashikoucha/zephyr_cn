.. _mcumgr_smp_group_3:

Settings
（Config）
Management
Group
##################################

Settings
management
group
（在
原始
MCUmgr
repository
中
known
作为
Configuration
Manager）
define
以下
commands：

.. table::
    :align:
    center

    +----------------+------------------------------+
    |
    ``Command
    ID``
    |
    Command
    description
    |
    +================+==============================+
    |
    ``0``
    |
    Read/write
    setting
    |
    +----------------+------------------------------+
    |
    ``1``
    |
    Delete
    setting
    |
    +----------------+------------------------------+
    |
    ``2``
    |
    Commit
    settings
    |
    +----------------+------------------------------+
    |
    ``3``
    |
    Load/Save
    settings
    |
    +----------------+------------------------------+

注意
Zephyr
version
added
additional
的
commands
和
features
它们
不
被
原始
upstream
version
supported
然而
原始
的
client
functionality
应该
可以
work
用于
read/write
functionality。

Read/write
setting
command
**************************

Read/write
setting
command
allow
update
device
上
的
setting
entry
或
get
device
上
setting
的
current
value。

Read
setting
request
==================

Read
setting
request
header
fields：

.. table::
    :align:
    center
