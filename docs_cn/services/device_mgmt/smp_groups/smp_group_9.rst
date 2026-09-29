.. _mcumgr_smp_group_9:

Shell
management
################

Shell
management
allow
通过
SMP
protocol
pass
commands
到
shell
subsystem。

Shell
management
group
define
以下
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
    Shell
    command
    line
    execute
    |
    +-------------------+-----------------------------------------------+

Shell
command
line
execute
**************************

这
个
command
allow
execute
command
line
以
类似
typing
到
shell
的
方式
但
request
和
response
都
通过
SMP
transported。

Shell
command
line
execute
request
==================================

Execute
command
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
    |
    ``2``
    |
    ``9``
    |
    ``0``
    |
    +--------+--------------+----------------+

Request
的
CBOR
data：
