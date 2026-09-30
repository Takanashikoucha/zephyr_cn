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


.. note::

   以下为原文（待翻译）

    +------------------+-------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when  |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.         |
    +------------------+-------------------------------------------------------------------------+

Write setting request
=====================

Write setting request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``2``  | ``3``        | ``0``          |
    +--------+--------------+----------------+

CBOR data of request:

.. code-block:: none

    {
        (str)"name"    : (str)
        (str)"val"     : (bstr)
    }

where:

.. table::
    :align: center

    +--------+-------------------------------------+
    | "name" | string of the setting to update/set |
    +--------+-------------------------------------+
    | "val"  | value to set the setting to         |
    +--------+-------------------------------------+

Write setting response
======================

Write setting response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``3``  | ``3``        | ``0``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data if successful. In case of error the CBOR data takes
the form:

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

where:

.. table::
    :align: center

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

Delete setting command
**********************

Delete setting command allows deleting a setting on a device.

Delete setting request
======================

Delete setting request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``2``  | ``3``        | ``1``          |
    +--------+--------------+----------------+

CBOR data of request:

.. code-block:: none

    {
        (str)"name"   : (str)
    }

where:

.. table::
    :align: center

    +--------+---------------------------------+
    | "name" | string of the setting to delete |
    +--------+---------------------------------+

Delete setting response
=======================

Delete setting response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``3``  | ``3``        | ``1``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data if successful. In case of error the CBOR data takes
the form:

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

where:

.. table::
    :align: center

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

Commit settings command
***********************

Commit settings command allows committing all settings that have been set but not yet applied on a
device.

Commit settings request
=======================

Commit settings request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``2``  | ``3``        | ``2``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data.

Commit settings response
========================

Commit settings response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``3``  | ``3``        | ``2``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data if successful. In case of error the CBOR data takes
the form:

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

where:

.. table::
    :align: center

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

Load/Save settings command
**************************

Load/Save settings command allows loading/saving all serialized items from/to persistent storage
on a device.

Load settings request
=====================

Load settings request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``0``  | ``3``        | ``3``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data.

Load settings response
======================

Load settings response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``1``  | ``3``        | ``3``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data if successful. In case of error the CBOR data takes
the form:

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

where:

.. table::
    :align: center

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

Save settings request
=====================

Save settings request header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``2``  | ``3``        | ``3``          |
    +--------+--------------+----------------+

CBOR data of request:

.. code-block:: none

    {
        (str,opt)"name" : (str)
    }

where:

.. table::
    :align: center

    +--------+---------------------------------------------------------------------------------------+
    | "name" | If provided, contains the settings subtree name to save (can also be a single setting |
    |        | name if :kconfig:option:`CONFIG_SETTINGS_SAVE_SINGLE_SUBTREE_WITHOUT_MODIFICATION` is |
    |        | enabled), if not then will save all settings.                                         |
    +--------+---------------------------------------------------------------------------------------+


Save settings response
======================

Save settings response header fields:

.. table::
    :align: center

    +--------+--------------+----------------+
    | ``OP`` | ``Group ID`` | ``Command ID`` |
    +========+==============+================+
    | ``3``  | ``3``        | ``3``          |
    +--------+--------------+----------------+

The command sends an empty CBOR map as data if successful. In case of error the CBOR data takes
the form:

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

where:

.. table::
    :align: center

    +------------------+------------------------------------------------------------------------+
    | "err" -> "group" | :c:enum:`mcumgr_group_t` group of the group-based error code. Only     |
    |                  | appears if an error is returned when using SMP version 2.              |
    +------------------+------------------------------------------------------------------------+
    | "err" -> "rc"    | contains the index of the group-based error code. Only appears if      |
    |                  | non-zero (error condition) when using SMP version 2.                   |
    +------------------+------------------------------------------------------------------------+
    | "rc"             | :c:enum:`mcumgr_err_t` only appears if non-zero (error condition) when |
    |                  | using SMP version 1 or for SMP errors when using SMP version 2.        |
    +------------------+------------------------------------------------------------------------+

Settings access callback
************************

There is a settings access MCUmgr callback available (see :ref:`mcumgr_callbacks` for details on
callbacks) which allows for applications/modules to know when settings management commands are
used and, optionally, block access (for example through the use of a security mechanism). This
callback can be enabled with :kconfig:option:`CONFIG_MCUMGR_GRP_SETTINGS_ACCESS_HOOK`, registered
with the event :c:enumerator:`MGMT_EVT_OP_SETTINGS_MGMT_ACCESS`, whereby the supplied callback data
is :c:struct:`settings_mgmt_access`.
