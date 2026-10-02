Bluetooth: Basic Audio Profile: Broadcast Assistant Shell
#########################################################

本文档描述如何运行 BAP Broadcast Assistant 功能。
请注意，在下面的示例中，删除了一些调试行
以使本文档更短并提供更好的概览。

Broadcast Assistant 负责为资源
受限设备卸载扫描，使得扫描不会耗尽电池。Broadcast
Assistant 应支持扫描周期广播，并可选项
支持周期广播同步传输（PAST）协议。

Broadcast Assistant 通常将是手机或笔记本电脑。
Broadcast Assistant 扫描周期广播并传输
信息到服务器。

交互使用 Broadcast Assistant
需要启用
:kconfig:option:`CONFIG_BT_BAP_BROADCAST_ASSISTANT_LOG_LEVEL_DBG`。

当蓝牙协议栈已初始化（:code:`bt init`），
并且已连接设备后，Broadcast Assistant 可通过调用 :code:`bap_broadcast_assistant discover` 在
已连接设备上发现 BASS，
这将开始发现 BASS UUID 并保存句柄，
并订阅所有通知。

.. code-block:: console

   uart:~$ bap_broadcast_assistant --help
   bap_broadcast_assistant - Bluetooth BAP broadcast assistant client shell
                           commands
   Subcommands:
   discover          : Discover BASS on the server
   scan_start        : Start scanning for broadcasters
   scan_stop         : Stop scanning for BISs
   add_src           : Add a source <address: P:XX:XX:XX:XX:XX:XX or
                         R:XX:XX:XX:XX:XX:XX> <adv_sid> <sync_pa> <broadcast_id>
                         [<sync_bis>] [<pa_interval>] [<metadata>]
   add_broadcast_id  : Add a source by broadcast ID <broadcast_id> <sync_pa>
                         [<sync_bis>] [<metadata>]
   add_broadcast_name: Add a source by broadcast name <broadcast_name> <sync_pa>
                         [<sync_bis>] [<metadata>]
   add_pa_sync       : Add a PA sync as a source <sync_pa> <broadcast_id>
                         [bis_index [bis_index [bix_index [...]]]]>
   mod_src           : Set sync <src_id> <sync_pa> [<pa_interval> | "unknown"] [<sync_bis>]
                         [<metadata>]
   broadcast_code    : Send a string-based broadcast code of up to 16 bytes
                         <src_id> <broadcast code>
   rem_src           : Remove a source <src_id>
   read_state        : Remove a source <index>

示例用法
*************

设置
=====

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap init
   uart:~$ bt connect P:xx:xx:xx:xx:xx:xx

已连接时
==============

为服务器开始扫描周期广播：
--------------------------------------------------------

.. note::
   Broadcast Assistant 实际上不会开始扫描周期
   广播，因为该功能在撰写本文时
   尚未实现。

.. code-block:: console

   uart:~$ bap_broadcast_assistant discover
   BASS discover done with 1 recv states
   uart:~$ bap_broadcast_assistant scan_start true
   BASS scan start successful
   Found broadcaster with ID 0x05BD38 and addr R:1E:4D:0A:AA:6E:49 and sid 0x00

使用 add_src 向接收状态添加源：
--------------------------------------------------

.. code-block:: console

   uart:~$ bap_broadcast_assistant add_src P:11:22:33:44:55:66 5 1 1
   BASS recv state: src_id 0, addr P:11:22:33:44:55:66, sid 5, sync_state 1, encrypt_state 000000000000000000000000000000000
       [0]: BIS sync 0, metadata_len 0


使用 add_broadcast_id 向接收状态添加源（推荐）：
--------------------------------------------------------------------------------

.. code-block:: console

   uart:~$ bap_broadcast_assistant add_broadcast_id 0x05BD38 true
   [DEVICE]: R:1E:4D:0A:AA:6E:49, AD evt type 5, RSSI -28 Broadcast Audio Source C:0 S:0 D:0 SR:0 E:1 Prim: LE 1M, Secn: LE 2M, Interval: 0x03c0 (1200000 us), SID: 0x0
   Found BAP broadcast source with address R:1E:4D:0A:AA:6E:49 and ID 0x05BD38
   BASS recv state: src_id 0, addr R:1E:4D:0A:AA:6E:49, sid 0, sync_state 0, encrypt_state 0
         [0]: BIS sync 0x0000, metadata_len 0
   BASS add source successful
   BASS recv state: src_id 0, addr R:1E:4D:0A:AA:6E:49, sid 0, sync_state 2, encrypt_state 0
         [0]: BIS sync 0x0000, metadata_len 0
   BASS recv state: src_id 0, addr R:1E:4D:0A:AA:6E:49, sid 0, sync_state 2, encrypt_state 0
         [0]: BIS sync 0x0000, metadata_len 4
                 Metadata length 2, type 2, data: 0100


修改接收状态：
--------------------------

.. code-block:: console

   uart:~$ bap_broadcast_assistant mod_src 0 true 0x03c0 0x02
   BASS modify source successful
   BASS recv state: src_id 0, addr R:1E:4D:0A:AA:6E:49, sid 0, sync_state 2, encrypt_state 0
         [0]: BIS sync 0x0001, metadata_len 4
                 Metadata length 2, type 2, data: 0100

提供广播码：
---------------------------

.. code-block:: console

   uart:~$ bap_broadcast_assistant broadcast_code 0 secretCode
   Sending broadcast code:
   00000000: 73 65 63 72 65 74 43 6f 64 65 00 00 00 00 00 00 |secretCo de....|
   uart:~$ BASS broadcast code successful
