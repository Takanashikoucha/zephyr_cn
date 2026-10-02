Bluetooth：媒体控制配置文件 Shell
######################################

本文档描述如何通过 Shell 运行媒体控制功能，
既作为客户端也作为服务器。

媒体控制服务器由两部分组成。
有一个媒体播放器（mpl），包含处理媒体的逻辑；
还有一个媒体控制服务（mcs），
作为基于 GATT 的播放器接口。
媒体控制客户端由一部分组成，即基于 GATT 的客户端（mcc）。

媒体控制服务器可以包含对象传输服务（ots），
媒体控制客户端可以包含对象传输客户端（otc）。
当包含这些时，可提供更丰富的功能集。

媒体控制服务器和客户端都只实现通用媒体控制服务（GMCS），
不使用任何底层媒体控制服务。

注意以下示例中，许多情况下已删除调试输出，
长输出可能已被截短，以使示例更简洁清晰。

另外注意本文档未列出所有 Shell 命令，
仅展示其中一些命令的示例。
命令集可以从 mcc Shell 和 mpl Shell 中探索，
输入 :code:`mcc` 或 :code:`mpl` 并按 TAB 即可查看。
每个命令的帮助文本可通过执行 :samp:`mcc {<command>} help`
或 :samp:`mpl {<command>} help` 查看。

概述
********

媒体播放器有一个*名称*和一个*图标*，
允许用户识别该播放器。

媒体播放器的内容结构化为曲目和分组。
媒体播放器有多个分组。
分组包含曲目和其他分组。
（在此实现中，分组仅包含曲目，不包含其他分组。）
曲目可以划分为片段。

活动的播放器会有一个*当前曲目*。
这是当前正在播放的曲目（如果播放器正在播放）。
当前曲目有*标题*、*时长*（以百分之一秒为单位）
和*位置*——播放器在该曲目中的当前位置。

还有*当前分组*（当前曲目所属的分组）、
*父分组*（当前分组的父分组）和*下一曲目*。

媒体播放器处于某种*状态*，
为播放中、暂停、定位或非活动之一。
播放时，以给定的*播放速度*进行播放，
曲目按*播放顺序*播放，
该顺序是*支持的播放顺序*之一。
曲目变更通过*曲目变更*特征的通知来信号。
定位时（快进或快退），
曲目位置按*定位速度*移动。

*支持的助记符*指示播放器通过写入*媒体控制点*
支持哪些操作。
还有一个*搜索控制点*，
允许根据各种条件搜索分组和曲目，
结果在*搜索结果*中返回。

最后，*内容控制 ID* 用于将媒体播放器与音频流关联。

媒体控制客户端（MCP）
**************************

媒体控制客户端用于控制和获取媒体控制服务器的信息。
控制通过写入两个控制点之一或写入其他可写特征来实现。
获取信息通过读取特征或配置服务器发送通知来实现。

使用媒体控制客户端
==============================

使用前，必须通过命令 :code:`mcc init` 初始化媒体控制客户端。

要与对端建立连接，必须使用 :code:`bt` 命令——
先 :code:`bt init` 然后 :code:`bt advertise on`
（如果服务器在广播则使用 :code:`bt connect`）。

当媒体控制客户端连接到媒体控制服务器后，
客户端可以通过命令 :code:`mcc discover_mcs` 发现服务器的通用媒体控制服务。
这将存储服务的句柄，并（可选地，但默认）订阅所有通知。

发现后，媒体控制客户端可以读写特征，
包括媒体控制点和搜索控制点。

使用示例
=============

设置
-----

.. code-block:: console

   uart:~$ bt init
   Bluetooth initialized

   uart:~$ mcc init
   MCC init complete

   uart:~$ bt advertise on
   Advertising started
   Connected: R:F6:58:DC:27:F3:57


连接后
--------------

服务发现（GMCS 和包含的 OTS）：

.. code-block:: console

   uart:~$ mcc discover_mcs
   <dbg> bt_mcc.bt_mcc_discover_mcs: start discovery of MCS primary service
   <dbg> bt_mcc.discover_primary_func: [ATTRIBUTE] handle 0x00ae
   <dbg> bt_mcc.discover_primary_func: Primary discovery complete
   <dbg> bt_mcc.discover_primary_func: UUID: 2800
   <dbg> bt_mcc.discover_primary_func: UUID: 8fd7
   <dbg> bt_mcc.discover_primary_func: Start discovery of MCS characteristics
   <dbg> bt_mcc.discover_mcs_char_func: [ATTRIBUTE] handle 0x00b0
   <dbg> bt_mcc.discover_mcs_char_func: Player name, UUID: 8fa0
   <dbg> bt_mcc.discover_mcs_char_func: [ATTRIBUTE] handle 0x00b2
   <dbg> bt_mcc.discover_mcs_char_func: Icon Object, UUID: 8fa1
   <dbg> bt_mcc.discover_mcs_char_func: [ATTRIBUTE] handle 0x00b4
   <dbg> bt_mcc.discover_mcs_char_func: Icon URI, UUID: 8fa2
   <dbg> bt_mcc.discover_mcs_char_func: [ATTRIBUTE] handle 0x00b6
   <dbg> bt_mcc.discover_mcs_char_func: Track Changed, UUID: 8fa3
   <dbg> bt_mcc.discover_mcs_char_func: Subscribing - handle: 0x00b6
   [...]
   <dbg> bt_mcc.discover_mcs_char_func: [ATTRIBUTE] handle 0x00ea
   <dbg> bt_mcc.discover_mcs_char_func: Content Control ID, UUID: 8fb5
   <dbg> bt_mcc.discover_mcs_char_func: Setup complete for MCS
   <dbg> bt_mcc.discover_mcs_char_func: Start discovery of included services
   <dbg> bt_mcc.discover_include_func: [ATTRIBUTE] handle 0x00af
   <dbg> bt_mcc.discover_include_func: Include UUID 1825
   <dbg> bt_mcc.discover_include_func: Discover include complete for MCS: OTS
   <dbg> bt_mcc.discover_include_func: Start discovery of OTS characteristics
   <dbg> bt_mcc.discover_otc_char_func: [ATTRIBUTE] handle 0x009c
   <dbg> bt_mcc.discover_otc_char_func: OTS Features
   [...]
   <dbg> bt_mcc.discover_otc_char_func: [ATTRIBUTE] handle 0x00ac
   <dbg> bt_mcc.discover_otc_char_func: Object Size
   Discovery complete
   <dbg> bt_otc.bt_otc_register: 0
   <dbg> bt_otc.bt_otc_register: L2CAP psm 0x  25 sec_level 1 registered
   <dbg> bt_mcc.discover_otc_char_func: Setup complete for OTS 1 / 1
   uart:~$


读取特征——以播放器和曲目时长为例：

.. code-block:: console

   uart:~$ mcc read_player_name
   Player name: My media player
   4d 79 20 6d 65 64 69 61  20 70 6c 61 79 65 72    |My media  player

   uart:~$ mcc read_track_duration
   Track duration: 6300

注意某些特征的值可能因过长而无法放入 ATT 数据包而被截断。
增大 ATT MTU 可能有帮助：

.. code-block:: console

   uart:~$ mcc read_track_title
   Track title: Interlude #1 (Song for

   uart:~$ gatt exchange-mtu
   Exchange pending
   Exchange successful

   uart:~$ mcc read_track_title
   Track title: Interlude #1 (Song for Alison)

写入特征——以曲目位置为例：

曲目位置是播放器在当前曲目中的"位置"。
读取曲目位置，通过写入来更改，
再次读取以确认。

.. code-block:: console

   uart:~$ mcc read_track_position
   Track Position: 0

   uart:~$ mcc set_track_position 500
   Track Position: 500

   uart:~$ mcc read_track_position
   Track Position: 500


通过控制点控制播放器：

写入控制点允许客户端请求服务器执行播放、暂停、快进、
切换曲目、切换分组等操作。
某些操作（例如跳转到曲目）接受参数。
目前，原始助记符值用作控制点 Shell 命令的输入。
这些助记符值可在 mpl.h 头文件中找到。

发送播放命令（助记符 "1"）、跳转到第三首曲目的命令
（助记符 "52"）和暂停命令（助记符 "2"）：

.. code-block:: console

   uart:~$ mcc set_cp 1
   Media State: 1
   Operation: 1, result: 1
   Operation: 1, param: 0

   uart:~$ mcc set_cp 52 3
   Track changed
   Track title: Interlude #3 (Levanto Seventy)
   Track duration: 7800
   Track Position: 0
   Current Track Object ID: 0x000000000104
   Next Track Object ID: 0x000000000105
   Operation: 52, result: 1
   Operation: 52, param: 3

   uart:~$ mcc set_cp 2
   Media State: 2
   Operation: 2, result: 1
   Operation: 2, param: 0



使用包含的对象传输客户端
-----------------------------------------

当客户端和服务器都支持对象传输时，
可获取更大的一组特征。
这些包括各种曲目和分组对象的对象 ID。
这些 ID 可用于从服务器的对象传输服务中
选择并下载对应的对象。

读取当前分组对象的对象 ID：

.. code-block:: console

   uart:~$ mcc read_current_group_obj_id
   Current Group Object ID: 0x000000000107


选择具有该 ID 的对象：

.. code-block:: console

   uart:~$ mcc ots_select 0x107
   Selecting object succeeded


读取对象的元数据：

.. code-block:: console

   uart:~$ mcc ots_read_metadata
   Reading object metadata succeeded
   <inf> bt_mcc: Object's meta data:
   <inf> bt_mcc:        Current size    :35
   <inf> bt_otc: --- Displaying 1 metadata records ---
   <inf> bt_otc: Object ID: 0x000000000107
   <inf> bt_otc: Object name: Joe Pass - Guitar Inte
   <inf> bt_otc: Object Current Size: 35
   <inf> bt_otc: Object Allocate Size: 35
   <inf> bt_otc: Type: Group Obj Type
   <inf> bt_otc: Properties:0x4
   <inf> bt_otc:  - read permitted


读取对象本身：

接收到的对象是一个分组对象。
它由一系列记录组成，每条记录包含一个类型（曲目或分组）
和一个对象 ID。

.. code-block:: console

   uart:~$ mcc ots_read_current_group_object
   <dbg> bt_mcc.on_group_content: Object type: 0, object  ID: 0x000000000102
   <dbg> bt_mcc.on_group_content: Object type: 0, object  ID: 0x000000000103
   <dbg> bt_mcc.on_group_content: Object type: 0, object  ID: 0x000000000104
   <dbg> bt_mcc.on_group_content: Object type: 0, object  ID: 0x000000000105
   <dbg> bt_mcc.on_group_content: Object type: 0, object  ID: 0x000000000106


搜索
------

搜索控制点接受一系列搜索控制项作为输入，
每项由长度、类型（例如曲目名称或艺术家名称）
和参数（要搜索的曲目名称或艺术家名称）组成。
如果结果成功，搜索结果存储在对象传输服务的一个对象中。
搜索结果 ID 对象的 ID 可以从搜索结果对象 ID 特征读取。
然后可以像上述当前分组对象一样下载搜索结果对象。
（注意在搜索执行之前，搜索结果对象 ID 为空。）

此实现具有功能完备的搜索功能接口
和服务器端搜索控制点参数解析。
但**实际搜索是模拟的**，
无论搜索什么，都返回相同的结果。

有两个搜索命令，一个（:code:`mcc set_scp_raw`）
允许将搜索控制点参数（搜索控制项序列）
作为字符串输入。
另一个（:code:`mcc set_scp_ioptest`）
执行预设的 IOP 测试搜索，
以 IOP 搜索控制点测试的轮次号作为参数。

搜索之前，搜索结果对象 ID 为空

.. code-block:: console

   uart:~$ mcc read_search_results_obj_id
   Search Results Object ID: 0x000000000000
   <dbg> bt_mcc.mcc_read_search_results_obj_id_cb: Zero-length Search Results Object ID

运行对应 IOP 测试第四轮的搜索：

此命令和参数生成的搜索控制点参数
有一个搜索控制项。
长度字段（第一字节）为 16（0x10）。
（长度字段本身的长度不包含在内。）
类型字段（第二字节）为 0x04（搜索分组名称）。
参数（要搜索的分组名称）为 "TSPX_Group_Name"。

.. code-block:: console

   uart:~$ mcc set_scp_ioptest 4
   Search string:
   00000000: 10 04 54 53 50 58 5f 47  72 6f 75 70 5f 4e 61 6d |..TSPX_G roup_Nam|
   00000010: 65                                               |e                |
   Search control point notification result code: 1
   Search Results Object ID: 0x000000000107
   Search Control Point set

成功搜索后，搜索结果对象 ID 有值：

.. code-block:: console

   uart:~$ mcc read_search_results_obj_id
   Search Results Object ID: 0x000000000107


媒体控制服务（MCS）
***************************

媒体控制服务（mcs）和关联的媒体播放器（mpl）
通常驻留在能够提供和分发媒体内容的设备上，
如 PC 和智能手机。

如上所述，媒体播放器（mpl）拥有播放器逻辑，
而媒体控制服务（mcs）拥有基于 GATT 的接口。
这种分离使得媒体播放器也可以在没有
基于 GATT 的接口的情况下使用。

使用媒体控制服务和媒体播放器
====================================================

媒体控制服务和媒体播放器通常由媒体控制客户端远程控制。

使用前，必须通过命令 :code:`mpl init` 初始化媒体控制客户端。

与客户端一样，使用 :code:`bt` 命令进行连接——
先 :code:`bt init` 然后 :code:`bt connect <address> <address type>`
（如果服务器在广播则使用 :code:`bt advertise on`）。

使用示例
=============

设置
-----

.. code-block:: console

   uart:~$ bt init
   Bluetooth initialized

   uart:~$ mpl init
   [Large amounts of debug output]

   uart:~$ bt connect R:F9:33:3B:67:D2:A7
   Connection pending
   Connected: R:F9:33:3B:67:D2:A7


连接后
--------------

控制从客户端进行。

服务器会输出与客户端执行的各种操作相关的调试信息。

示例：客户端发送"下一曲目"命令时服务器的调试输出：

.. code-block:: console

   [00:13:29.932,373] <dbg> bt_mcs.control_point_write: Opcode: 49
   [00:13:29.932,403] <dbg> bt_mpl.mpl_operation_set: opcode: 49, param: 536880068
   [00:13:29.932,403] <dbg> bt_mpl.paused_state_operation_handler: Operation opcode: 49
   [00:13:29.932,495] <dbg> bt_mpl.do_next_track: Track ID before: 0x000000000104
   [00:13:29.932,586] <dbg> bt_mpl.do_next_track: Track ID after: 0x000000000105
   [00:13:29.932,617] <dbg> bt_mcs.mpl_track_changed_cb: Notifying track change
   [00:13:29.932,708] <dbg> bt_mcs.mpl_track_title_cb: Notifying track title: Interlude #4 (Vesper Dreams)
   [00:13:29.932,800] <dbg> bt_mcs.mpl_track_duration_cb: Notifying track duration: 13500
   [00:13:29.932,861] <dbg> bt_mcs.mpl_track_position_cb: Notifying track position: 0
   [00:13:29.933,044] <dbg> bt_mcs.mpl_current_track_id_cb: Notifying current track ID: 0x000000000105
   [00:13:29.933,258] <dbg> bt_mcs.mpl_next_track_id_cb: Notifying next track ID: 0x000000000106
   [00:13:29.933,380] <dbg> bt_mcs.mpl_operation_cb: Notifying control point - opcode: 49, result: 1


某些服务器命令可用。这些命令强制发送各种特征的通知，
用于测试客户端是否接收通知。
由这些测试命令触发的通知中发送的值
与媒体播放器无关，
因此不对应特征的实际值，
也不对应媒体播放器的实际状态。

示例：强制（伪造值）发送曲目时长通知：

.. code-block:: console

   uart:~$ mpl duration_changed_cb
   [00:15:17.491,058] <dbg> bt_mcs.mpl_track_duration_cb: Notifying track duration: 12000
