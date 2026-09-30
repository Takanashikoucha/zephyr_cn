.. _bluetooth_le_host:

LE
Host
#######

Bluetooth
Host
实现
所有
的
higher
level
的
protocols
和
profiles
最
重要
的
是
为
applications
提供
high
level
的
API。
以下
diagram
depict
host
的
main
protocol
&
profile
layers。

.. figure::
   img/ble_host_layers.png
   :align:
   center
   :alt:
   Bluetooth
   Host
   protocol
   &
   profile
   layers

   Bluetooth
   Host
   protocol
   &
   profile
   layers。

Host
stack
最
底部
是
一
个
所谓
的
HCI
driver
它
负责
abstract
away
HCI
transport
的
details。
它
提供
基本
的
API
用于
将
data
从
controller
传递
到
host
反之
亦然。

可能
最
重要
的
block
在
HCI
handling
上面
是
Generic
Access
Profile
（GAP）。
GAP
通过
定义
Bluetooth
使用
的
四
个
distinct
的
roles
简化
Bluetooth
LE
access：

*
Connection
oriented
的
roles

   *
   Peripheral
   （e.g.
   a
   smart
   sensor
   often
   with
   a
   limited
   user
   interface）

   *
   Central
   （typically
   a
   mobile
   phone
   or
   a
   PC）

*
Connection
less
的
roles

   *
   Broadcaster
   （sending
   out
   Bluetooth
   LE
   advertisements
   e.g.
   a
   smart
   beacon）

   *
   Observer
   （scanning
   for
   Bluetooth
   LE
   advertisements）

每个
role
带
它
自己
的
build
time
configuration
option：
:kconfig:option:`CONFIG_BT_PERIPHERAL`、
:kconfig:option:`CONFIG_BT_CENTRAL`、
:kconfig:option:`CONFIG_BT_BROADCASTER`
&
:kconfig:option:`CONFIG_BT_OBSERVER`。
Of
the


.. note::

   以下为原文（待翻译）


Terminology
-----------

The definitions are from the Core Specification version 5.4, volume 3, part A
1.4.

.. list-table::
  :header-rows: 1

  * - Term
    - Description

  * - Upper layer
    - Layer above L2CAP, it exchanges data in form of SDUs. It may be an
      application or a higher level protocol.

  * - Lower layer
    - Layer below L2CAP, it exchanges data in form of PDUs (or fragments). It is
      usually the HCI.

  * - Service Data Unit (SDU)
    - Packet of data that L2CAP exchanges with the upper layer.

      This term is relevant only in Enhanced Retransmission mode, Streaming
      mode, Retransmission mode and Flow Control Mode, not in Basic L2CAP mode.

  * - Protocol Data Unit (PDU)
    - Packet of data containing L2CAP data. PDUs always start with Basic L2CAP
      header.

      Types of PDUs for LE: :ref:`B-frames <bluetooth_l2cap_b_frame>` and
      :ref:`K-frames <bluetooth_l2cap_k_frame>`.

      Types of PDUs for BR/EDR: I-frames, S-frames, C-frames and G-frames.

  * - Maximum Transmission Unit (MTU)
    - Maximum size of an SDU that the upper layer is capable of accepting.

  * - Maximum Payload Size (MPS)
    - Maximum payload size that the L2CAP layer is capable of accepting.

      In Basic L2CAP mode, the MTU size is equal to MPS. In credit-based
      channels without segmentation, the MTU is MPS minus 2.

  * - Basic L2CAP header
    - Present at the beginning of each PDU. It contains two fields, the PDU
      length and the Channel Identifier (CID).

PDU Types
---------

.. _bluetooth_l2cap_b_frame:

B-frame: Basic information frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PDU used in Basic L2CAP mode. It contains the payload received from the upper
layer or delivered to the upper layer as its payload.

.. image:: img/l2cap_b_frame.drawio.svg
  :align: center
  :width: 45%
  :alt: Representation of a B-frame PDU. The PDU is split into two rectangles,
        the first one being the L2CAP header, its size is 4 octets and its made
        of the PDU length and the channel ID. The second rectangle represents
        the information payload and its size is less or equal to MPS.

.. _bluetooth_l2cap_k_frame:

K-frame: Credit-based frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^

PDU used in LE Credit Based Flow Control mode and Enhanced Credit Based Flow
Control mode. It contains a SDU segment and additional protocol information.

.. image:: img/l2cap_k_frame_1.drawio.svg
  :width: 45%
  :alt: Representation of a starting K-frame PDU. The PDU is split into three
        rectangles, the first one being the L2CAP header, its size is 4 octets
        and its made of the PDU length and the channel ID. The second rectangle
        represents the L2CAP SDU length, its size is 2 octets. The third
        rectangle represents the information payload and its size is less or
        equal to MPS minus 2 octets. The information payload contains the L2CAP
        SDU.

.. image:: img/l2cap_k_frame.drawio.svg
  :align: right
  :width: 45%
  :alt: Representation of K-frames PDUs after the starting one. The PDU is split
        into two rectangles, the first one being the L2CAP header, its size is 4
        octets and its made of the PDU length and the channel ID. The second
        rectangle represents the information payload and its size is less or
        equal to MPS. The information payload contains the L2CAP SDU.

Relevant Kconfig
----------------

.. list-table::
  :header-rows: 1

  * - Kconfig symbol
    - Description

  * - :kconfig:option:`CONFIG_BT_BUF_ACL_RX_SIZE`
    - Represents the MPS

  * - :kconfig:option:`CONFIG_BT_L2CAP_TX_MTU`
    - Represents the L2CAP MTU

  * - :kconfig:option:`CONFIG_BT_L2CAP_DYNAMIC_CHANNEL`
    - Enables LE Credit Based Flow Control and thus the stack may use
      :ref:`K-frame <bluetooth_l2cap_k_frame>` PDUs

GATT
====

The Generic Attribute Profile is the most common means of communication
over LE connections. A more detailed description of this layer and the
API reference can be found in the
:ref:`GATT API reference section <bt_gatt>`.

ATT timeout
-----------

If the peer device does not respond to an ATT request (such as read or write)
within the ATT timeout, the host will automatically initiate a disconnect. This
simplifies error handling by reducing rare failure conditions to a common
disconnection, allowing developers to manage unexpected disconnects without
special cases for ATT timeouts.

.. image:: img/att_timeout.svg
  :align: center
  :alt: ATT timeout

Mesh
====

Mesh is a little bit special when it comes to the needed GAP roles. By
default, mesh requires both observer and broadcaster role to be enabled.
If the optional GATT Proxy feature is desired, then peripheral role
should also be enabled.

The API reference for mesh can be found in the
:ref:`Mesh API reference section <bluetooth_mesh>`.

LE Audio
========
The LE audio is a set of profiles and services that utilizes GATT and
Isochronous Channel to provide audio over Bluetooth Low Energy.
The architecture and API references can be found in
:ref:`Bluetooth Audio Architecture <bluetooth_le_audio_arch>`.


.. _bluetooth-persistent-storage:

Persistent storage
==================

The Bluetooth host stack uses the settings subsystem to implement
persistent storage to flash. This requires the presence of a flash
driver and a designated "storage" partition on flash. A typical set of
configuration options needed will look something like the following:

  .. code-block:: cfg

    CONFIG_BT_SETTINGS=y
    CONFIG_FLASH=y
    CONFIG_FLASH_PAGE_LAYOUT=y
    CONFIG_FLASH_MAP=y
    CONFIG_NVS=y
    CONFIG_SETTINGS=y

Once enabled, it is the responsibility of the application to call
settings_load() after having initialized Bluetooth (using the
:c:func:`bt_enable` API).
