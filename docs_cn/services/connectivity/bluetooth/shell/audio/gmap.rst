Bluetooth：游戏音频配置文件 Shell
#####################################

本文档描述如何运行游戏音频配置文件 Shell 功能。
与大多数其他底层配置文件不同，GMAP 是一个在所有设备上都存在并拥有服务（GMAS）的配置文件。
因此发起方和接受方（或中央设备和外围设备）都应该对远程设备的 GMAS 进行发现，
以查看它们支持哪些 GMAP 角色和功能。

使用 GMAP Shell
********************

当蓝牙协议栈已初始化（:code:`bt init`）后，
可以通过调用 :code:`gmap init` 来注册 GMAS。
强烈建议通过 :code:`bap init` 启用 BAP。

.. code-block:: console

   uart:~$ gmap --help
   gmap - Bluetooth GMAP shell commands
   Subcommands:
     init      : [none]
     set_role  : [ugt | ugg | bgr | bgs]
     discover  : [none]
     ac_1      : Unicast audio configuration 1
     ac_2      : Unicast audio configuration 2
     ac_3      : Unicast audio configuration 3
     ac_4      : Unicast audio configuration 4
     ac_5      : Unicast audio configuration 5
     ac_6_i    : Unicast audio configuration 6(i)
     ac_6_ii   : Unicast audio configuration 6(ii)
     ac_7_ii   : Unicast audio configuration 7(ii)
     ac_8_i    : Unicast audio configuration 8(i)
     ac_8_ii   : Unicast audio configuration 8(ii)
     ac_11_i   : Unicast audio configuration 11(i)
     ac_11_ii  : Unicast audio configuration 11(ii)
     ac_12     : Broadcast audio configuration 12
     ac_13     : Broadcast audio configuration 13
     ac_14     : Broadcast audio configuration 14

:code:`set_role` 命令可用于在运行时更改角色，前提是设备支持该角色
（GMAP 角色取决于某些 BAP 配置）。

具有 GMAP UGT 角色的中央设备示例
**********************************

连接并使用音频配置（AC）3 建立游戏音频流
（省略了部分日志以增强可读性）：

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap init
   uart:~$ gmap init
   uart:~$ bt connect <address>
   uart:~$ gatt exchange-mtu
   uart:~$ bap discover
   Discover complete: err 0
   uart:~$ cap_initiator discover
   discovery completed with CSIS
   uart:~$ gmap discover
   gmap discovered for conn 0x2001c7d8:
        role 0x0f
        ugg_feat 0x07
        ugt_feat 0x6f
        bgs_feat 0x01
        bgr_feat 0x03
   uart:~$ bap preset sink 32_2_gr
   uart:~$ bap preset source 32_2_gs
   uart:~$ gmap ac_3
   Starting 2 streams for AC_3
   stream 0x20020060 config operation rsp_code 0 reason 0
   stream 0x200204d0 config operation rsp_code 0 reason 0
   stream 0x200204d0 qos operation rsp_code 0 reason 0
   stream 0x20020060 qos operation rsp_code 0 reason 0
   Stream 0x20020060 enabled
   stream 0x200204d0 enable operation rsp_code 0 reason 0
   Stream 0x200204d0 enabled
   stream 0x20020060 enable operation rsp_code 0 reason 0
   Stream 0x20020060 started
   stream 0x200204d0 start operation rsp_code 0 reason 0
   Stream 0x200204d0 started
   Unicast start completed
   uart:~$ bap start_sine
   Started transmitting on default_stream 0x20020060
   [0]: stream 0x20020060 : TX LC3: 80 (seq_num 24800)
