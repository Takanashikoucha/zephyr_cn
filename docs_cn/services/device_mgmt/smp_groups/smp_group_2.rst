.. _mcumgr_smp_group_2:

Statistics
management
#####################

Statistics
management
allow
obtain
Zephyr
的
Statistics
subsystem
gathered
的
data
它
用
:kconfig:option:`CONFIG_STATS`
enabled。

Statistics
management
group
define
commands：

.. table::
    :align:
    center

    +-------------------+-----------------------------------------------+
    |
    ``Command
    ID``
    |
    Command
    description
    |
    +===================+===============================================+
    |
    ``0``
    |
    Group
    data
    |
    +-------------------+-----------------------------------------------+
    |
    ``1``
    |
    List
    groups
    |
    +-------------------+-----------------------------------------------+

Statistics:
group
data
**********************

这
个
command
被
used
用于
obtain
由
name
specified
的
group
的
data。
Name
是
一
个
group
name
它
被
registered
用
:c:macro:`STATS_INIT_AND_REG`
macro
或
:c:func:`stats_init_and_reg`
function
call
在
gather
statistics
的
module
中。

Statistics:
group
data
request
==================================

Statistics
group
data
request
header：

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
