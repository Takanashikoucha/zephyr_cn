.. _mcumgr_smp_group_63:

Zephyr
Management
Group
#######################

Zephyr
management
group
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
    Erase
    storage
    |
    +----------------+------------------------------+

Erase
storage
command
*********************

Erase
storage
command
allow
clear
device
上
的
``storage_partition``
flash
partition
通常
这
被
used
当
switch
到
新
的
application
build
时
如果
application
use
应该
被
cleared
的
storage
（application
dependent）。

Erase
storage
request
====================

Erase
storage
request
header
fields：

.. table::
    :align:
    center

    +--------+--------------+----------------+
    |
    ``OP``
    |
    ``Group
    ID``
    |
    ``Command
    ID``
    |
    +========+==============+================+
    |
    ``2``
    |
    ``63``
    |
    ``0``
    |
    +--------+--------------+----------------+

这
个
command
sends
一
个
empty
的
CBOR
map
作为
data。

Erase
storage
response
