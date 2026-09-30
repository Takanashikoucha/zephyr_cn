.. _bluetooth_shell:

Shell
#####

Bluetooth
Shell
是
基于
:ref:`shell_api`
module
的
application。
它
offer
一
组
commands
旨在
轻松
与
Bluetooth
stack
交互。

关于
特定
的
Bluetooth
functionality
也
参考
以下
shell
documentation

.. toctree::
   :maxdepth:
   1

   shell/audio/bap.rst
   shell/audio/bap_broadcast_assistant.rst
   shell/audio/bap_scan_delegator.rst
   shell/audio/cap.rst
   shell/audio/ccp.rst
   shell/audio/csip.rst
   shell/audio/gmap.rst
   shell/audio/mcp.rst
   shell/audio/tbs.rst
   shell/audio/tmap.rst
   shell/audio/pbp.rst
   shell/classic/a2dp.rst
   shell/classic/avrcp.rst
   shell/classic/goep.rst
   shell/classic/hfp.rst
   shell/classic/l2cap.rst
   shell/classic/map.rst
   shell/classic/pbap.rst
   shell/classic/spp.rst
   shell/host/gap.rst
   shell/host/gatt.rst
   shell/host/iso.rst
   shell/host/l2cap.rst

Bluetooth
Shell
Setup
and
Usage
*******************************


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
* List the available modules and their current logging level

.. code-block:: console

        uart:~$ log status

* Disable logging for *bt_hci_core*

.. code-block:: console

        uart:~$ log disable bt_hci_core

* Enable error logs for *bt_att* and *bt_smp*

.. code-block:: console

        uart:~$ log enable err bt_att bt_smp

* Disable logging for all modules

.. code-block:: console

        uart:~$ log disable

* Enable warning logs for all modules

.. code-block:: console

        uart:~$ log enable wrn