Bluetooth:
Classic:
AVRCP
Shell
################################

这
document
describe
如何
用
shell
commands
使用
Bluetooth
Classic
AVRCP
（Audio/Video
Remote
Control
Profile）
functionality。
:code:`avrcp`
command
expose
Controller
（CT）
和
Target
（TG）
两
个
roles
用于
exercise
AVRCP
control
和
browsing
features。

有
两
个
sub
commands：
:code:`avrcp
ct`
和
:code:`avrcp
tg`。
:code:`avrcp
ct`
sub
command
提供
**Controller
（CT）**
functionality
:code:`avrcp
tg`
sub
command
提供
**Target
（TG）**
functionality。

Prerequisites
-------------

在
运行
:code:`avrcp`
shell
之前
确保
你
的
build
启用
了
Bluetooth
Classic
和
shell。
在
AVRCP
control
或
browsing
connections
可以
被
created
之前
必须
先
establish
到
peer
device
的
ACL
BR/EDR
connection
（通常
通过
general
的
:code:`bt`
shell
commands）。

Commands
********

所有
commands
只
能
在
ACL
connection
被
established
之后
使用
除了
:code:`avrcp
ct
register_cb`
和
:code:`avrcp
tg
register_cb`。

:code:`avrcp`
commands：

.. code-block::
   console

   uart:~$
   avrcp
   avrcp
   -
   Bluetooth
   AVRCP
   shell
   commands
   Subcommands:
     connect
                :
      connect
      AVRCP
     disconnect
             :
      disconnect
      AVRCP
     browsing_connect
       :
      connect
      browsing
      AVRCP
     browsing_disconnect
    :
      disconnect
      browsing
      AVRCP
     ct
                     :
      AVRCP
      CT
      shell
      commands
     tg
                     :
      AVRCP
      TG
      shell
      commands

:code:`avrcp
ct`
commands：


.. note::

   以下为原文（待翻译）

        .. group-tab:: Device B (TG - Target)

                .. code-block:: console

                        uart:~$ avrcp tg register_cb
                        AVRCP TG callbacks registered
                        <input `avrcp connect` in CT side>
                        AVRCP TG connected
                        <input `avrcp ct get_caps events` in CT side>
                        AVRCP get capabilities command received: cap_id 0x03 (EVENTS_SUPPORTED)
                        uart:~$ avrcp tg send_get_caps_rsp
                        Get capabilities response sent successfully
                        <input `avrcp ct register_notification 0x01` in CT side>
                        receive register notification request event_id=0x01
                        uart:~$ avrcp tg send_notification_rsp 0x01 interim 0
                        Sent notification rsp event_id=0x01 type=interim
                        <input `avrcp ct play` in CT side>
                        receive passthrough command: op_id=0x44 (PLAY)
                        uart:~$ avrcp tg send_passthrough_rsp op play pressed
                        Passthrough opid=0x44 (STANDARD), state=pressed sent successfully
                        uart:~$ avrcp tg send_passthrough_rsp op play released
                        Passthrough opid=0x44 (STANDARD), state=released sent successfully
                        uart:~$ avrcp tg send_notification_rsp 0x01 changed 1
                        Sent notification rsp event_id=0x01 type=changed
                        <input `avrcp ct get_play_status` in CT side>
                        receive get play status request
                        uart:~$ avrcp tg send_get_play_status_rsp
                        GetPlayStatus rsp sent
                        <input `avrcp ct get_element_attrs` in CT side>
                        AVRCP GetElementAttributes command received
                        uart:~$ avrcp tg send_get_element_attrs_rsp 0
                        Sending standard GetElementAttributes response (7 attrs)
                        GetElementAttributes response sent successfully
                        <input `avrcp ct set_absolute_volume 50` in CT side>
                        AVRCP set_absolute_volume_req: tid=0x06, absolute_volume=0x32
                        uart:~$ avrcp tg send_absolute_volume_rsp 50
                        Set absolute volume response sent successfully
                        <input `avrcp ct pause` in CT side>
                        AVRCP passthrough command received: opid = 0x46
                        uart:~$ avrcp tg send_passthrough_rsp op pause pressed
                        send passthrough response
                        uart:~$ avrcp tg send_passthrough_rsp op pause released
                        send passthrough response

AVRCP Connection
****************

The AVRCP profile supports both control and browsing connections. The control connection
is used for basic remote control functionality, while the browsing connection allows
browsing of media content.

Control Connection
==================

Establish AVRCP control connection:

1. Register callbacks (CT side):

.. code-block:: console

   uart:~$ avrcp ct register_cb
   AVRCP CT callbacks registered

2. Register callbacks (TG side):

.. code-block:: console

   uart:~$ avrcp tg register_cb
   AVRCP TG callbacks registered

3. Connect AVRCP:

.. code-block:: console

   uart:~$ avrcp connect
   AVRCP CT connected
   AVRCP TG connected

4. Disconnect AVRCP:

.. code-block:: console

   uart:~$ avrcp disconnect
   AVRCP CT disconnected
   AVRCP TG disconnected

Browsing Connection
===================

After control connection is established, browsing connection can be initiated:

1. Connect browsing:

.. code-block:: console

   uart:~$ avrcp browsing_connect
   AVRCP browsing connect request sent
   AVRCP CT browsing connected
   AVRCP TG browsing connected

2. Disconnect browsing:

.. code-block:: console

   uart:~$ avrcp browsing_disconnect
   AVRCP browsing disconnect request sent
   AVRCP CT browsing disconnected
   AVRCP TG browsing disconnected

Basic Playback Control
**********************

Control playback from CT side:

.. tabs::

   .. group-tab:: Play Command

      .. code-block:: console

         uart:~$ avrcp ct play
         Passthrough PRESSED command sent successfully: opid=0x44
         Passthrough RELEASED command sent successfully: opid=0x44

   .. group-tab:: Pause Command

      .. code-block:: console

         uart:~$ avrcp ct pause
         Passthrough PRESSED command sent successfully: opid=0x46
         Passthrough RELEASED command sent successfully: opid=0x46

Get Capabilities
****************

Query supported capabilities:

.. tabs::

   .. group-tab:: Company ID

      .. code-block:: console

         uart:~$ avrcp ct get_caps company
         Get capabilities command sent successfully: cap_id=company
         GetCapabilities : status=0x04
         Remote CompanyID = 0x001958

   .. group-tab:: Events Supported

      .. code-block:: console

         uart:~$ avrcp ct get_caps events
         Get capabilities command sent successfully: cap_id=events
         GetCapabilities : status=0x04
         Remote supported EventID = 0x01
         Remote supported EventID = 0x02
         Remote supported EventID = 0x03
         Remote supported EventID = 0x04
         Remote supported EventID = 0x0d

   .. group-tab:: TG Response

      .. code-block:: console

         uart:~$ avrcp tg send_get_caps_rsp
         Sending company ID capability rsp: 0x001958

Media Metadata Operations
*************************

Get Element Attributes
======================

Retrieve metadata for the currently playing media:

.. tabs::

   .. group-tab:: CT Request

      .. code-block:: console

         uart:~$ avrcp ct get_element_attrs
         Requesting element attributes: identifier=0x0000000000000000, num_attrs=0
         AVRCP CT get element attrs command sent
         GetElementAttributes : status=0x04
         AVRCP GetElementAttributes response received, tid=0x00, num_attrs=7
          Attr[0]: ID=0x00000001 (TITLE), charset=0x006a, len=11
            Value: "Test Title"
          Attr[1]: ID=0x00000002 (ARTIST), charset=0x006a, len=11
            Value: "Test Artist"
          Attr[2]: ID=0x00000003 (ALBUM), charset=0x006a, len=10
            Value: "Test Album"
          Attr[3]: ID=0x00000004 (TRACK_NUMBER), charset=0x006a, len=1
            Value: "1"
          Attr[4]: ID=0x00000005 (TOTAL_TRACKS), charset=0x006a, len=2
            Value: "10"
          Attr[5]: ID=0x00000006 (GENRE), charset=0x006a, len=4
            Value: "Rock"
          Attr[6]: ID=0x00000007 (PLAYING_TIME), charset=0x006a, len=6
            Value: "240000"

   .. group-tab:: TG Response

      .. code-block:: console

         uart:~$ avrcp tg send_get_element_attrs_rsp 0
         Sending standard GetElementAttributes response (7 attrs)
         GetElementAttributes response sent successfully

Play Status
===========

Get current playback status:

.. tabs::

   .. group-tab:: CT Request

      .. code-block:: console

         uart:~$ avrcp ct get_play_status
         AVRCP GetPlayStatus
         getplaystatus : status=0x04
         GetPlayStatus: len=180000 ms, pos=30000 ms, status=0x01
          status: PLAYING

   .. group-tab:: TG Response

      .. code-block:: console

         uart:~$ avrcp tg send_get_play_status_rsp
         GetPlayStatus rsp sent

Volume Control
**************

Set absolute volume:

.. tabs::

   .. group-tab:: CT Set Volume

      .. code-block:: console

         uart:~$ avrcp ct set_absolute_volume 50
         set absolute volume absolute_volume=0x32
         AVRCP set absolute volume rsp: tid=0x01, status=0x04, volume=0x32

   .. group-tab:: TG Response

      .. code-block:: console

         uart:~$ avrcp tg send_absolute_volume_rsp 50
         Set absolute volume response sent successfully

Event Notifications
*******************

Register for notifications and handle events:

Register for Volume Change Notification
========================================

.. tabs::

   .. group-tab:: CT Register

      .. code-block:: console

         uart:~$ avrcp ct register_notification 0x0d
         Sent register notification event_id=0x0d
         AVRCP notification rsp: tid=0x02, status=0x04, event_id=0x0d
          Notification type: INTERIM
          VOLUME_CHANGED: absolute_volume=0x0a
         AVRCP notify_changed_cb received: event_id=0x0d
          Notification type: CHANGED
          VOLUME_CHANGED: absolute_volume=0x14

   .. group-tab:: TG Send Notification

      .. code-block:: console

         uart:~$ avrcp tg send_notification_rsp 0x0d interim 10
         Sent notification rsp event_id=0x0d type=interim

         uart:~$ avrcp tg send_notification_rsp 0x0d changed 20
         Sent notification rsp event_id=0x0d type=changed

Browsing Operations
*******************

Set Browsed Player
==================

.. tabs::

   .. group-tab:: CT Request

      .. code-block:: console

         uart:~$ avrcp ct set_browsed_player 1
         AVRCP send set browsed player req
         AVRCP set browsed player success, tid = 0
           UID Counter: 1
           Number of Items: 100
           Charset ID: 0x006A
           Folder Depth: 1
           charset_id  : 0x006A
           Get folder Name (hex)  :
         00000000: 4d 75 73 69 63                                   |Music            |

   .. group-tab:: TG Response

      .. code-block:: console

         uart:~$ avrcp tg send_browsed_player_rsp
         Send set browsed player response, status = 0x04

Get Folder Items
================

.. tabs::

   .. group-tab:: CT Request

      .. code-block:: console

         uart:~$ avrcp ct get_folder_items
         Sent GetFolderItems command
         AVRCP get folder items success, tid = 1
           UID Counter: 1
           Number of Items: 1
         Media Player Item:
           item_len   : 28
           player_id   : 1
           major_type  : 0x01
           sub_type    : 0x00000000
           play_status : 0x00
           charset_id  : 0x006A
           name_len    : 4
           charset_id  : 0x006A
           Name (hex)  :
         00000000: 44:65:6d:6f                                      |Demo

   .. group-tab:: TG Response

      .. code-block:: console

         uart:~$ avrcp tg send_get_folder_items_rsp
         TG: Sent GetFolderItems response

Player Application Settings
***************************

List and get configure player application settings:

List Available Settings
=======================

.. tabs::

   .. group-tab:: CT Request

      .. code-block:: console

         uart:~$ avrcp ct list_app_attrs
         Sent list player app setting attrs
         list player app setting attrs : status=0x04
         attr =0x01 (EQUALIZER)
         attr =0x02 (REPEAT_MODE)

   .. group-tab:: TG Response

      .. code-block:: console

         uart:~$ avrcp tg send_list_player_app_setting_attrs_rsp 2 0x01 0x02
         TG: Sent list player app setting attrs response

Get Current Settings
====================

.. tabs::

   .. group-tab:: CT Request

      .. code-block:: console

         uart:~$ avrcp ct get_app_curr 1 2
         Sent get_curr_player_app_setting_val num=2
         get curr player app setting val : status=0x04
         attr_id :1 val 1
         attr_id :2 val 1

   .. group-tab:: TG Response

      .. code-block:: console

         uart:~$ avrcp tg send_get_curr_player_app_setting_val_rsp 2 0x01 0x01 0x02 0x02
         TG: Send get curr player app setting val rsp (num=2)
