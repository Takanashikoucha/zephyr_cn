Bluetooth:
Common
Audio
Profile
Shell
#####################################

这
document
describe
如何
运行
Common
Audio
Profile
functionality。

CAP
Acceptor
************

Acceptor
通常
是
resource
constrained
的
device
如
headset、
earbud
或
hearing
aid。
Acceptor
可以
initialize
一
个
Coordinated
Set
Identification
Service
instance
如果
它
与
一
个
或
多
个
其他
CAP
Acceptors
在
一
对
中。

Using
the
CAP
Acceptor
=====================

当
Bluetooth
stack
被
initialized
（:code:`bt
init`）
后
Acceptor
可以
通过
调用
:code:`cap_acceptor
init`
被
registered
它
将
register
CAS
和
CSIS
services
同时
register
callbacks。

.. code-block::
   console


   cap_acceptor
   --help
   cap_acceptor
   -
   Bluetooth
   CAP
   acceptor
   shell
   commands
   Subcommands:
     init
          :Initialize
      the
      service
      and
      register
      callbacks
      [size
      <int>]
                    [rank
      <int>]
      [not
      lockable]
      [sirk
      <data>]
     lock
          :Lock
      the
      set
     release
       :Release
      the
      set
      [force]
     sirk
          :Set
      the
      currently
      used
      SIRK
      <sirk>
     get_info
      :Get
      CSIS
      info
     sirk_rsp
      :Set
      the
      response
      used
      in
      SIRK
      requests
      <accept,
      accept_enc,
      reject,
      oob>

除了
initialize
CAS
和
CSIS
还有
commands
用于
lock
和
release
CSIS
instance
同时
print
和
modify
对
CSIS
的
SIRK
的
access。

Setting
a
new
SIRK
------------------


.. note::

   以下为原文（待翻译）


To stop all the streams that has been started, the :code:`cap_initiator unicast_stop` command can be
used.


.. code-block:: console

   uart:~$ cap_initiator unicast_stop all
   Unicast stop completed

When doing broadcast
--------------------

To start a broadcast as the CAP initiator there are a few steps to be done:

1. Create and configure an extended advertising set with periodic advertising
2. Create and configure a broadcast source
3. Setup extended and periodic advertising data

The following commands will setup a CAP broadcast source using the 16_2_1 preset (defined by BAP):


.. code-block:: console

   bt init
   bap init
   bt adv-create nconn-nscan ext-adv
   bt per-adv-param
   bap preset broadcast 16_2_1
   cap_initiator ac_12
   bt adv-data dev-name discov
   bt per-adv-data
   cap_initiator broadcast_start
   bt adv-start
   bt per-adv on


The broadcast source is created by the :code:`cap_initiator ac_12`, :code:`cap_initiator ac_13`,
and :code:`cap_initiator ac_14` commands, configuring the broadcast source for the defined audio
configurations from BAP. The broadcast source can then be stopped with
:code:`cap_initiator broadcast_stop` or deleted with :code:`cap_initiator broadcast_delete`.

The metadata of the broadcast source can be updated at any time, including when it is already
streaming. To update the metadata the :code:`cap_initiator broadcast_update` command can be used.
The command takes an array of data, and the only requirement (besides having valid data) is that the
streaming context shall be set. For example to set the streaming context to media, the command can
be used as

.. code-block:: console

   cap_initiator broadcast_update 03020400
   CAP Broadcast source updated with new metadata. Update the advertised base via `bt per-adv-data`
   bt per-adv-data

The :code:`bt per-adv-data` command should be used afterwards to update the data is the advertised
BASE. The data must be little-endian, so in the above example the metadata :code:`03020400` is
setting the metadata entry with :code:`03` as the length, :code:`02` as the type (streaming context)
and :code:`0400` as the value :code:`BT_AUDIO_CONTEXT_TYPE_MEDIA`
(which has the numeric value of 0x).

CAP Commander
*************

The Commander will typically be a either co-located with a CAP Initiator or be on a separate
resource-rich mobile device, such as a phone or smartwatch. The Commander can
discover CAP Acceptors's CAS and optional CSIS services. The CSIS service can be read to provide
information about other CAP Acceptors in the same Coordinated Set. The Commander can provide
information about broadcast sources to CAP Acceptors or coordinate capture and rendering information
such as mute or volume states.

Using the CAP Commander
=======================

When the Bluetooth stack has been initialized (:code:`bt init`), the Commander can discover CAS and
the optionally included CSIS instance by calling (:code:`cap_commander discover`).

.. code-block:: console

   cap_commander --help
   cap_commander - Bluetooth CAP commander shell commands
   Subcommands:
     discover                  :Discover CAS
     cancel                    :CAP commander cancel current procedure
     change_volume             :Change volume on all connections <volume>
     change_volume_mute        :Change volume mute state on all connections <mute>
     change_volume_offset      :Change volume offset per connection <volume_offset
                                [volume_offset [...]]>
     change_microphone_mute    :Change microphone mute state on all connections <mute>
     change_microphone_gain    :Change microphone gain per connection <gain
                                [gain [...]]>
     broadcast_reception_start : Start broadcast reception with source
                                 <address: P:XX:XX:XX:XX:XX:XX or R:XX:XX:XX:XX:XX:XX>
                                 <adv_sid> <broadcast_id>
                                 [<pa_interval>] [<sync_bis>] [<metadata>]
     broadcast_reception_stop  : Stop broadcast reception <src_id [...]>
     distribute_broadcast_code : Distribute broadcast code <src_id [...]> <broadcast_code>


Before being able to perform any stream operation, the device must also perform the
:code:`bap discover` operation to discover the ASEs and PAC records. The :code:`bap init`
command also needs to be called.

When connected
--------------

Discovering CAS and CSIS on a device
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ cap_commander discover
   discovery completed with CSIS


Setting the volume on all connected devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ vcp_vol_ctlr discover
   VCP discover done with 1 VOCS and 1 AICS
   uart:~$ cap_commander change_volume 15
   uart:~$ cap_commander change_volume 15
   Setting volume to 15 on 2 connections
   VCP volume 15, mute 0
   VCP vol_set done
   VCP volume 15, mute 0
   VCP flags 0x01
   VCP vol_set done
   Volume change completed

Setting the volume offset on one or more devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The offsets are set by connection index, so connection index 0 gets the first offset,
and index 1 gets the second offset, etc.:

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ vcp_vol_ctlr discover
   VCP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ bt connect <device B>
   Connected: <device B>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ vcp_vol_ctlr discover
   VCP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ cap_commander change_volume_offset 10
   Setting volume offset on 1 connections
   VOCS inst 0x200140a4 offset 10
   Offset set for inst 0x200140a4
   Volume offset change completed
   uart:~$
   uart:~$ cap_commander change_volume_offset 10 15
   Setting volume offset on 2 connections
   Offset set for inst 0x200140a4
   VOCS inst 0x20014188 offset 15
   Offset set for inst 0x20014188
   Volume offset change completed

Setting the volume mute on all connected devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ vcp_vol_ctlr discover
   VCP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ bt connect <device B>
   Connected: <device B>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ vcp_vol_ctlr discover
   VCP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ cap_commander change_volume_mute 1
   Setting volume mute to 1 on 2 connections
   VCP volume 100, mute 1
   VCP mute done
   VCP volume 100, mute 1
   VCP mute done
   Volume mute change completed
   uart:~$ cap_commander change_volume_mute 0
   Setting volume mute to 0 on 2 connections
   VCP volume 100, mute 0
   VCP unmute done
   VCP volume 100, mute 0
   VCP unmute done
   Volume mute change completed

Setting the microphone mute on all connected devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ micp_mic_ctlr discover
   MICP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ bt connect <device B>
   Connected: <device B>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ micp_mic_ctlr discover
   MICP discover done with 1 VOCS and 1 AICS
   uart:~$
   uart:~$ cap_commander change_microphone_mute 1
   Setting microphone mute to 1 on 2 connections
   MICP microphone 100, mute 1
   MICP mute done
   MICP microphone 100, mute 1
   MICP mute done
   Microphone mute change completed
   uart:~$ cap_commander change_microphone_mute 0
   Setting microphone mute to 0 on 2 connections
   MICP microphone 100, mute 0
   MICP unmute done
   MICP microphone 100, mute 0
   MICP unmute done
   Microphone mute change completed

Setting the microphone gain on one or more devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The gains are set by connection index, so connection index 0 gets the first offset,
and index 1 gets the second offset, etc.:

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ micp_mic_ctlr discover
   MICP discover done with 1 AICS
   uart:~$
   uart:~$ bt connect <device B>
   Connected: <device B>
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ micp_mic_ctlr discover
   MICP discover done with 1 AICS
   uart:~$
   uart:~$ cap_commander change_microphone_gain 10
   Setting microphone gain on 1 connections
   AICS inst 0x200140a4 state gain 10, mute 0, mode 0
   Gain set for inst 0x200140a4
   Microphone gain change completed
   uart:~$
   uart:~$ cap_commander change_microphone_gain 10 15
   Setting microphone gain on 2 connections
   Gain set for inst 0x200140a4
   AICS inst 0x20014188 state gain 15, mute 0, mode 0
   Gain set for inst 0x20014188
   Microphone gain change completed

Starting and stopping broadcast reception
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ bap_init
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ bap_broadcast_assistant discover
   BASS discover done with 1 recv states
   uart:~$ cap_commander broadcast_reception_start <device B> 0 4
   Starting broadcast reception on 1 connection(s)
   Broadcast reception start completed
   uart:~$ cap_commander broadcast_reception_stop 0
   Stopping broadcast reception on 1 connection(s)
   Broadcast reception stop completed

Distributing the broadcast code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   uart:~$ bt connect <device A>
   Connected: <device A>
   uart:~$ bap_init
   uart:~$ cap_commander discover
   discovery completed with CSIS
   uart:~$ bap_broadcast_assistant discover
   BASS discover done with 1 recv states
   uart:~$ cap_commander broadcast_reception_start <device B> 0 4
   Starting broadcast reception on 1 connection(s)
   Broadcast reception start completed
   uart:~$ cap_commander distribute_broadcast_code 0 "BroadcastCode"
   Distribute broadcast code completed

CAP Handover
************

The handover procedures allow the user to switch between unicast and broadcast streams. Since
broadcast streams are always unidirectional, the procedures will only work for streams with audio
direction from the Initiator to the Acceptor (sink streams).

Using the CAP Handover procedures
=================================

When the Bluetooth stack has been initialized (:code:`bt init`),
one or more remote CAP acceptor devices have been connected,
and audio streams have been set up,
the handover procedures can be used to switch between unicast and broadcast.
Before any of the handover procedures can be used,
the :code:`bap discover`, :code:`cap_initiator discover`
and :code:`bap_broadcast_assistant discover` commands must have been issued and completed.

.. code-block:: console

   cap_handover --help
   cap_handover - Bluetooth CAP handover shell commands
   Subcommands:
     unicast_to_broadcast  : Handover current unicast group to broadcast (unicast
                           group will be deleted) [enc <broadcast_code>] [preset <preset_name>]
     broadcast_to_unicast  : Handover current broadcast source to unicast
                           (broadcast source will be deleted)
                           [conns <count>|all] [preset <preset_name>]



Handover unicast to broadcast
-----------------------------

This command hands over one or more unicast streams from unicast to broadcast.

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap init
   uart:~$ bt connect <addr>

   # Discover necessary services
   uart:~$ bap discover
   uart:~$ cap_initiator discover
   uart:~$ bap_broadcast_assistant discover

   # Setup unicast audio e.g. using the ac_1
   uart:~$ cap_initiator ac_1

   # Create a non-connectable and non-scannable extended advertising set for broadcast
   uart:~$ bt adv-create nconn-nscan ext-adv
   uart:~$ bt per-adv-param

   # Perform the handover and update the advertising data to contain the broadcast ID
   uart:~$ cap_handover unicast_to_broadcast
   uart:~$ bt adv-data dev-name discov
   uart:~$ bt per-adv-data

   # Enable periodic advertising (extended advertising is enabled as part of handover)
   uart:~$ bt per-adv on

Handover broadcast to unicast
-----------------------------

This command hands over one or more unicast streams from broadcast to unicast.

.. code-block:: console

   uart:~$ bt init
   uart:~$ bap init
   uart:~$ bt connect <addr>

   # Discover necessary services
   uart:~$ bap discover
   uart:~$ cap_initiator discover
   uart:~$ bap_broadcast_assistant discover

   # Create a non-connectable and non-scannable extended advertising set for broadcast
   uart:~$ bt adv-create nconn-nscan ext-adv
   uart:~$ bt per-adv-param

   # Setup broadcast audio e.g. using the ac_12
   uart:~$ cap_initiator ac_12
   uart:~$ cap_initiator broadcast_start

   # Set advertising data and enable advertising
   uart:~$ bt adv-data dev-name discov
   uart:~$ bt per-adv-data
   uart:~$ bt per-adv on
   uart:~$ bt adv-start

   # Wait for broadcast sink to self-scan, or use broadcast reception to instruct sink to sync

   # Perform the handover
   uart:~$ cap_handover broadcast_to_unicast

   # Terminate the advertiser (optional)
   uart:~$ bt adv-stop
   uart:~$ bt per-adv off
   uart:~$ bt adv-delete
