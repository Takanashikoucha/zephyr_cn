.. _mcumgr_smp_group_10:

Enumeration
Management
Group
#############################

Enumeration
management
group
define
以下
commands：

.. table::
    :align:
    center

    +----------------+-----------------------------+
    |
    ``Command
    ID``
    |
    Command
    description
    |
    +================+=============================+
    |
    ``0``
    |
    Count
    of
    supported
    groups
    |
    +----------------+-----------------------------+
    |
    ``1``
    |
    List
    supported
    groups
    |
    +----------------+-----------------------------+
    |
    ``2``
    |
    Fetch
    single
    group
    ID
    |
    +----------------+-----------------------------+
    |
    ``3``
    |
    Details
    on
    supported
    groups
    |
    +----------------+-----------------------------+

Count
of
supported
groups
command
*********************************

Count
of
supported
groups
returns
device
supported
的
MCUmgr
command
groups
的
total
数量。

Count
of
supported
groups
request
=================================

Read
setting
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
    ``0``
    |
    ``10``
    |
    ``0``
    |
    +--------+--------------+----------------+
