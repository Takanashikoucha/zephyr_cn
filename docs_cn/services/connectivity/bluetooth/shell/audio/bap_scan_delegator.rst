Bluetooth: Basic Audio Profile: Scan Delegator Shell
####################################################

本文档描述如何运行 Scan Delegator 功能，请注意
在下面的示例中，删除了一些调试行
以使本文档更短并提供更好的概览。

Scan Delegator 可选项支持周期广播
同步传输（PAST）协议。

Scan Delegator 服务器通常驻留在具有输入或
输出的设备上。

交互使用
Scan Delegator 需要启用
:kconfig:option:`CONFIG_BT_BAP_SCAN_DELEGATOR_LOG_LEVEL_DBG`。

Scan Delegator 目前只能设置接收状态的同步状态，
但尚未实际支持与周期广播的同步。

.. code-block:: console

   bap_scan_delegator --help
   bap_scan_delegator - Bluetooth BAP Scan Delegator shell commands
   Subcommands:
     init                : Initialize the service and register callbacks
     set_past_pref       : Set PAST preference <true || false>
     sync_pa             : Sync to PA <src_id>
     term_pa             : Terminate PA sync <src_id>
     add_src             : Add a PA as source <addr> <sid> <broadcast_id>
                           <enc_state> [bis_sync [metadata]]
     add_src_by_pa_sync  : Add a PA as source <broadcast_id> <enc_state> [bis_sync
                           [metadata]]
     mod_src             : Modify source <src_id> <broadcast_id> <enc_state>
                           [bis_sync [metadata]]
     rem_src             : Remove source <src_id>
     synced              : Set server scan state <src_id> <bis_syncs>




示例用法
*************

设置
=====

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap_scan_delegator init
   uart:~$ bt advertise on
   Advertising started

添加源
==============

.. code-block:: console

   uart:~$ bap_scan_delegator add_src P:11:22:33:44:55:66 0 1234 0
   Receive state with ID 0 updated

从 PA 同步添加源
==============================

.. code-block:: console

   uart:~$ bt scan on
   Found broadcaster with ID 0x681A22 and addr R:2C:44:05:82:EB:82 and sid 0x00 (looking for 0x1000000)
   uart:~$ bt scan off
   uart:~$ bt per-adv-sync-create R:2C:44:05:82:EB:82 0
   PA 0x2003e9b0 synced
   uart:~$ bap_scan_delegator add_src_by_pa_sync 0x681A22 0
   Receive state with ID 0 updated

已连接时
==============

为源设置同步状态：

.. code-block:: console

   uart:~$ bap_scan_delegator synced 0 1 3 0
