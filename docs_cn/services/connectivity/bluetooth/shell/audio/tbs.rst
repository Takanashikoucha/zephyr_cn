Bluetooth：电话承载服务 Shell
#########################################

本文档描述如何运行呼叫控制功能，
既作为客户端也作为（电话承载服务（TBS））服务器。
注意以下示例中删除了部分调试输出行，
以使内容更简洁并便于总览。

电话承载服务客户端
*******************************

电话承载服务客户端通常存在于资源受限的设备上，
例如耳机，但也可能存在于手机或笔记本电脑上。
呼叫控制客户端因此也通常是广播方。
客户端可以使用呼叫控制点控制服务器上呼叫的状态。

必须启用 :kconfig:option:`CONFIG_BT_TBS_CLIENT_LOG_LEVEL_DBG`
才能交互式使用客户端。

使用电话承载服务客户端
=========================================

当蓝牙协议栈已初始化（:code:`bt init`）
且已连接一个设备后，
电话承载服务客户端可以通过调用 :code:`tbs_client discover`
发现已连接设备上的 TBS，
这将启动对 TBS UUID 的发现并存储句柄，
可选地订阅所有通知（默认订阅所有）。

由于服务器可能有多个 TBS 实例，
大多数 tbs_client 命令将接受一个索引（从 0 开始）作为输入。
合并呼叫至少需要 2 个呼叫 ID，
且所有呼叫索引应在同一个 TBS 实例上。

服务器还会有一个 GTBS 实例，
它是服务器上所有电话承载的抽象层。
如果服务器同时具有 GTBS 和 TBS，
当 :code:`BT_TBS_CLIENT_GTBS` 启用时，
客户端可以订阅并在发送请求时使用其中任何一个。

.. code-block:: console

   tbs_client --help
   tbs_client - Bluetooth TBS_CLIENT shell commands
   Subcommands:
      discover                       :Discover TBS [subscribe]
      set_signal_reporting_interval  :Set the signal reporting interval
                                       [<{instance_index, gtbs}>] <interval>
      originate                      :Originate a call [<{instance_index, gtbs}>]
                                       <uri>
      terminate                      :terminate a call [<{instance_index, gtbs}>]
                                       <id>
      accept                         :Accept a call [<{instance_index, gtbs}>] <id>
      hold                           :Place a call on hold [<{instance_index,
                                       gtbs}>] <id>
      retrieve                       :Retrieve a held call [<{instance_index,
                                       gtbs}>] <id>
      read_provider_name             :Read the bearer name [<{instance_index,
                                       gtbs}>]
      read_bearer_uci                :Read the bearer UCI [<{instance_index, gtbs}>]
      read_technology                :Read the bearer technology [<{instance_index,
                                       gtbs}>]
      read_uri_list                  :Read the bearer's supported URI list
                                       [<{instance_index, gtbs}>]
      read_signal_strength           :Read the bearer signal strength
                                       [<{instance_index, gtbs}>]
      read_signal_interval           :Read the bearer signal strength reporting
                                       interval [<{instance_index, gtbs}>]
      read_current_calls             :Read the current calls [<{instance_index,
                                       gtbs}>]
      read_ccid                      :Read the CCID [<{instance_index, gtbs}>]
      read_status_flags              :Read the in feature and status value
                                       [<{instance_index, gtbs}>]
      read_uri                       :Read the incoming call target URI
                                       [<{instance_index, gtbs}>]
      read_call_state                :Read the call state [<{instance_index, gtbs}>]
      read_remote_uri                :Read the incoming remote URI
                                       [<{instance_index, gtbs}>]
      read_friendly_name             :Read the friendly name of an incoming call
                                       [<{instance_index, gtbs}>]
      read_optional_opcodes          :Read the optional opcodes [<{instance_index,
                                       gtbs}>]


在以下示例中，除非另有说明，忽略来自 GTBS 的通知。

使用示例
=============

设置
-----

.. code-block:: console

   uart:~$ bt init
   uart:~$ bt advertise on
   Advertising started

连接后
--------------

拨打呼叫：

.. code-block:: console

   uart:~$ tbs_client discover
   <dbg> bt_tbs_client.primary_discover_func: Discover complete, found 1 instances (GTBS found)
   <dbg> bt_tbs_client.discover_func: Setup complete for 1 / 1 TBS
   <dbg> bt_tbs_client.discover_func: Setup complete GTBS
   uart:~$ tbs_client originate 0 tel:123
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the dialing state with URI tel:123
   <dbg> bt_tbs_client.call_cp_notify_handler: Status: success for the originate opcode for call 0x00
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the alerting state with URI tel:123
   <call answered by peer device, and status notified by TBS server>
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the active state with URI tel:123

在 GTBS 上拨打呼叫：

.. code-block:: console

   uart:~$ tbs_client originate 0 tel:123
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the dialing state with URI tel:123
   <dbg> bt_tbs_client.call_cp_notify_handler: Status: success for the originate opcode for call 0x00
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the alerting state with URI tel:123
   <call answered by peer device, and status notified by TBS server>
   <dbg> bt_tbs_client.notify_handler: Index 0
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x01 is in the active state with URI tel:123

在拨打呼叫之前必须设置 outgoing 主叫 ID。

接听来自对端设备的来电：

.. code-block:: console

   <dbg> bt_tbs_client.incoming_uri_notify_handler: tel:123
   <dbg> bt_tbs_client.in_call_notify_handler: tel:456
   <dbg> bt_tbs_client.friendly_name_notify_handler: Peter
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x05 is in the incoming state with URI tel:456
   uart:~$ tbs_client accept 0 5
   <dbg> bt_tbs_client.call_cp_callback_handler: Status: success for the accept opcode for call 0x05
   <dbg> bt_tbs_client.current_calls_notify_handler: Call 0x05 is in the active state with URI tel


结束呼叫：

.. code-block:: console

   uart:~$ tbs_client terminate 0 5
   <dbg> bt_tbs_client.termination_reason_notify_handler: ID 0x05, reason 0x06
   <dbg> bt_tbs_client.call_cp_notify_handler: Status: success for the terminate opcode for call 0x05
   <dbg> bt_tbs_client.current_calls_notify_handler:

电话承载服务（TBS）
******************************
电话承载服务是一种通常驻留在能够发起呼叫的设备上的服务，
包括来自 Skype 等应用程序的呼叫，例如（智能）手机和 PC。

必须启用 :kconfig:option:`CONFIG_BT_TBS_LOG_LEVEL_DBG`
才能交互式使用 TBS 服务器。

使用电话承载服务
==================================
TBS 可以本地控制，也可以由远程设备控制（在呼叫过程中）。
例如，远程设备可以向具有 TBS 服务器的设备发起呼叫，
或者 TBS 服务器可以向远程设备发起呼叫，而无需 TBS_CLIENT 客户端。
TBS 实现能够完全控制任何呼叫。
对于可以接受 :code:`<instance_index>` 的命令，
省略索引时默认为 GTBS 承载。

.. code-block:: console

   tbs --help
   tbs - Bluetooth TBS shell commands
   Subcommands:
      init                        :Initialize TBS
      authorize                   :Authorize the current connection
      accept                      :Accept call <call_index>
      terminate                   :Terminate call <call_index>
      hold                        :Hold call <call_index>
      retrieve                    :Retrieve call <call_index>
      originate                   :Originate call [<instance_index>] <uri>
      join                        :Join calls <id> <id> [<id> [<id> [...]]]
      incoming                    :Simulate incoming remote call [<{instance_index,
                                    gtbs}>] <local_uri> <remote_uri>
                                    <remote_friendly_name>
      remote_answer               :Simulate remote answer outgoing call <call_index>
      remote_retrieve             :Simulate remote retrieve <call_index>
      remote_terminate            :Simulate remote terminate <call_index>
      remote_hold                 :Simulate remote hold <call_index>
      set_bearer_provider_name    :Set the bearer provider name [<{instance_index,
                                    gtbs}>] <name>
      set_bearer_technology       :Set the bearer technology [<{instance_index,
                                    gtbs}>] <technology>
      set_bearer_signal_strength  :Set the bearer signal strength [<{instance_index,
                                    gtbs}>] <strength>
      set_status_flags            :Set the bearer feature and status value
                                    [<{instance_index, gtbs}>] <feature_and_status>
      set_uri_scheme              :Set the URI prefix list <bearer_idx> <uri1[,uri2[,uri3[,...]]]>
      print_calls                 :Output all calls in the debug log

使用示例
=============

设置
-----

.. code-block:: console

   uart:~$ bt init
   uart:~$ bt connect P:xx:xx:xx:xx:xx:xx

连接后
--------------

接听对端设备由客户端发起的呼叫：

.. code-block:: console

   <dbg> bt_tbs.write_call_cp: Index 0: Processing the originate opcode
   <dbg> bt_tbs.originate_call: New call with call index 1
   <dbg> bt_tbs.write_call_cp: Index 0: Processed the originate opcode with status success for call index 1
   uart:~$ tbs remote_answer 1
   TBS succeeded for call_id: 1

来自对端设备的来电，由客户端接听：

.. code-block:: console

   uart:~$ tbs incoming 0 tel:123 tel:456 Peter
   TBS succeeded for call_id: 4
   <dbg> bt_tbs.bt_tbs_remote_incoming: New call with call index 4
   <dbg> bt_tbs.write_call_cp: Index 0: Processed the accept opcode with status success for call index 4
