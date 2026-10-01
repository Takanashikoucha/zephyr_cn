.. _mcumgr_smp_group_63:

Zephyr Management Group
#######################

Zephyr management group 定义以下 commands：

.. table::
    :align: center

    +----------------+------------------------------+
    | ``Command ID`` | Command description          |
    +================+==============================+
    | ``0``          | Erase storage                |
    +----------------+------------------------------+

Erase storage command
*********************

Erase storage command 允许清除
device 上的 ``storage_partition`` flash partition（
通常这在切换到新 application build 时使用（若 application 使用
应被清除的
storage（application 相关。

Erase storage request
=====================

Erase storage request header fields：

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``2``  | ``63``       | ``0``          |
    +--------+--------------+----------------+

Command 发送空 CBOR map 作为 data。

Erase storage response
======================

Read setting response header fields：

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``3``  | ``63``       | ``0``          |
    +--------+--------------+----------------+

成功时（command 发送空 CBOR map 作为 data。错误时（CBOR data 取
以下形式：

.. tabs::

   .. group-tab:: SMP version 2

      .. code-block:: none

          {
              (str)"err" : {
                  (str)"group"    : (uint)
                  (str)"rc"       : (uint)
              }
          }

   .. group-tab:: SMP version 1

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

其中：

.. table::
    :align: center

    +------------------+-------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` of the group-based error code. Only      |
    |                  | appears if an error is returned when using SMP version 2.               |
    +------------------+-------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if       |
    |                  | non-zero (error condition) when using SMP version 2.                    |
    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when  |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.         |
    +------------------+-------------------------------------------------------------------------+
