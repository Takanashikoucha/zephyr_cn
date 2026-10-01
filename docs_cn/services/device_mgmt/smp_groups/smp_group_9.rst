.. _mcumgr_smp_group_9:

Shell management
################

Shell management 允许通过 SMP
protocol 向 shell subsystem 传递
commands。

Shell management group 定义以下 commands：

.. table::
    :align: center

    +-------------------+-----------------------------------------------+
    | ``Command ID``    | Command description                           |
    +===================+===============================================+
    | ``0``             | Shell command line execute                    |
    +-------------------+-----------------------------------------------+

Shell command line execute
**************************

Command 允许以类似输入到
shell 的方式执行 command line（但 request 和
response 均通过 SMP 传输。

Shell command line execute request
==================================

Execute command request header：

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``2``  | ``9``        |  ``0``         |
    +--------+--------------+----------------+

Request 的 CBOR data：

.. code-block:: none

    {
        (str)"argv"     : [
            (str)<cmd>
            (str,opt)<arg>
            ...
        ]
    }

其中：

.. table::
    :align: center

    +-----------------------+---------------------------------------------------+
    | "argv"                | array consisting of strings representing command  |
    |                       | and its arguments.                                |
    +-----------------------+---------------------------------------------------+
    | <cmd>                 | command to be executed.                           |
    +-----------------------+---------------------------------------------------+
    | <arg>                 | optional arguments to command.                    |
    +-----------------------+---------------------------------------------------+

Shell command line execute response
===================================

Command line execute response header fields：

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``3``  | ``9``        |  ``0``         |
    +--------+--------------+----------------+

成功 response 的 CBOR data：

.. code-block:: none

    {
        (str)"o"            : (str)
        (str)"ret"          : (int)
    }

错误时（CBOR data 取
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

   .. group-tab:: SMP version 1 (and non-group SMP version 2)

      .. code-block:: none

          {
              (str)"rc"       : (int)
          }

其中：

.. table::
    :align: center

    +------------------+-------------------------------------------------------------------------+
    | "o"              | command output.                                                         |
    +------------------+-------------------------------------------------------------------------+
    | "ret"            | return code from shell command execution.                               |
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

.. note::
    在 Zephyr 较旧版本中（"rc" 同时用于
    mcumgr status code
    和 shell command execution return code（此 legacy behaviour 可
    通过启用 :kconfig:option:`CONFIG_MCUMGR_GRP_SHELL_LEGACY_RC_RETURN_CODE`
    恢复
