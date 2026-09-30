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


.. note::

   以下为原文（待翻译）

    |                  | appears if an error is returned when using SMP version 2.               |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if       |
    |                  | non-zero (error condition) when using SMP version 2.                    |
    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when  |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.         |
    +------------------+-------------------------------------------------------------------------+

Statistics: list of groups
**************************

The command is used to obtain list of groups of statistics that are gathered
on a device. This is a list of names as given to groups with
:c:macro:`STATS_INIT_AND_REG` macro or :c:func:`stats_init_and_reg` function
calls, within module that gathers the statistics; this means that this command
may be considered optional as it is known during compilation what groups will
be included into build and listing them is not needed prior to issuing a query.

Statistics: list of groups request
==================================

Statistics group list request header:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``0``  | ``2``        |  ``1``         |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data.

Statistics: list of groups response
===================================

Statistics group list request header:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``1``  | ``2``        |  ``1``         |
    +--------+--------------+----------------+

CBOR data of successful response:

.. code-block:: none

    {
        (str)"stat_list" :  [
            (str)<stat_group_name>, ...
        ]
    }

In case of error the CBOR data takes the form:


.. tabs::

   .. group-tab:: SMP version 2

      .. code-block:: none

          {
              (str)"err" : {
                  (str)"group"    : (uint)
                  (str)"rc"       : (uint)
              }
          }

   .. group-tab:: SMP version 1 (and non-group SMP version 2)

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

where:

.. table::
    :align: center

    +------------------+-------------------------------------------------------------------------+
    | "stat_list"      | array of strings representing group names; this array may be empty if   |
    |                  | there are no groups.                                                    |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` group of the group-based error code. Only      |
    |                  | appears if an error is returned when using SMP version 2.               |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if       |
    |                  | non-zero (error condition) when using SMP version 2.                    |
    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when  |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.         |
    +------------------+-------------------------------------------------------------------------+
