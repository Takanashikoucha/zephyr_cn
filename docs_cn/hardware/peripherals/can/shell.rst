.. _can_shell:

CAN
Shell
#########

.. contents::
   :local:
   :depth:
   1

Overview
********

CAN
shell
为
:ref:`shell
<shell_api>`
模块
提供
一
个
带
一
组
subcommands
的
``can``
命令。
它
允许
通过
交互式
interface
测试
和
探索
:ref:`can_api`
driver
API
而
不
需要
写
专门
的
应用。
CAN
shell
也
可以
在
现有
应用
中
启用
以
辅助
CAN
issues
的
交互式
debugging。

CAN
shell
提供
对
大多数
CAN
controller
功能
的
访问，
包括
inspection、
configuration、
CAN
frames
的
发送
和
接收、
以及
bus
recovery。

要
启用
CAN
shell，
必须
启用
以下
:ref:`Kconfig
<kconfig>`
选项：

* :kconfig:option:`CONFIG_SHELL`
* :kconfig:option:`CONFIG_CAN`
* :kconfig:option:`CONFIG_CAN_SHELL`

以下
:ref:`Kconfig
<kconfig>`
选项
启用
``can``
命令
的
额外
subcommands
和
功能：

* :kconfig:option:`CONFIG_CAN_FD_MODE`
  启用
  CAN
  FD
  特定
  subcommands
  （例如
  用于
  设置
  CAN
  FD
  data
  phase
  的
  timing）。
* :kconfig:option:`CONFIG_CAN_RX_TIMESTAMP`
  启用
  接收
  的
  CAN
  frames
  的
  timestamps
  打印。
* :kconfig:option:`CONFIG_CAN_STATS`
  启用
  ``can
  show``
  subcommand
  中
  CAN
  controller
  的
  各种
  statistics
  打印。
  这
  依赖
  于
  :kconfig:option:`CONFIG_STATS`
  也
  被
  启用。
* :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE`
  启用
  ``can
  recover``
  subcommand。

例如，
为
:zephyr:board:`frdm_k64f`
构建
:zephyr:code-sample:`hello_world`
sample
启用
CAN
shell
和
CAN
statistics：


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
.. code-block:: console

   uart:~$ can filter add can@0 010
   adding filter with standard (11-bit) CAN ID 0x010, CAN ID mask 0x7ff, data frames 1, RTR frames 0, CAN FD frames 0
   filter ID: 0

The filter ID (0 in the example above) returned is to be used when removing the CAN RX filter.

Received CAN frames matching the added filter(s) are printed to the shell. A few examples are shown below:

.. code-block:: console

   # Dev Flags    ID   Size  Data bytes
   can0  --       010   [8]  01 02 03 04 05 06 07 08
   can0  B-       010  [08]  01 02 03 04 05 06 07 08
   can0  BP       010  [03]  01 aa bb
   can0  --  00000010   [0]
   can0  --       010   [1]  20
   can0  --       010   [8]  remote transmission request

The columns have the following meaning:

* Dev

  * Name of the device receiving the frame.

* Flags

  * ``B``: The frame has the CAN FD Baud Rate Switch (BRS) flag set.
  * ``P``: The frame has the CAN FD Error State Indicator (ESI) flag set. The transmitting node is
    in error-passive state.
  * ``-``: Unset flag.

* ID

  * ``010``: The standard (11-bit) CAN ID of the frame in hexadecimal format, here 10h.
  * ``00000010``: The extended (29-bit) CAN ID of the frame in hexadecimal format, here 10h.

* Size

  * ``[8]``: The number of frame data bytes in decimal format, here a classic CAN frame with 8 data
    bytes.
  * ``[08]``: The number of frame data bytes in decimal format, here a CAN FD frame with 8 data
    bytes.

* Data bytes

  * ``01 02 03 04 05 06 07 08``: The frame data bytes in hexadecimal format, here the numbers from 1
    through 8.
  * ``remote transmission request``: The frame is a Remote Transmission Request (RTR) frame and thus
    carries no data bytes.

.. tip::
   If :kconfig:option:`CONFIG_CAN_RX_TIMESTAMP` is enabled, each line will be prepended with a
   timestamp from the free-running timestamp counter in the CAN controller.

Configured CAN RX filters can be removed again using the ``can filter remove`` subcommand as shown
below. The filter ID is the ID returned by the ``can filter add`` subcommand (0 in the example
below).

.. code-block:: console

   uart:~$ can filter remove can@0 0
   removing filter with ID 0

Another option is to use the ``can dump`` subcommand, which adds standard (11-bit) and extended
(29-bit) CAN filters matching any RX frame, starts the CAN controller, and prints all received CAN
frames to the shell:

.. code-block:: console

   uart:~$ can dump can@0
   dumping CAN RX frames on device can@0, press Ctrl+C to exit

After exiting the ``can dump`` subcommand by pressing Ctrl+C, the added filters are automatically
removed and the CAN controller stopped again.

Sending
*******

CAN frames can be queued for transmission using the ``can send`` subcommand as shown below. The
subcommand accepts a CAN ID in hexadecimal format and optionally a number of data bytes, also
specified in hexadecimal. Refer to the interactive help output for this subcommand for further
details on the supported arguments.

.. code-block:: console

   uart:~$ can send can@0 010 1 2 3 4 5 6 7 8
   enqueuing CAN frame #2 with standard (11-bit) CAN ID 0x010, RTR 0, CAN FD 0, BRS 0, DLC 8
   CAN frame #2 successfully sent

Bus Recovery
************

The ``can recover`` subcommand can be used for initiating manual recovery from a CAN bus-off event
as shown below:

.. code-block:: console

   uart:~$ can recover can@0
   recovering, no timeout

The subcommand accepts an optional bus recovery timeout in milliseconds. If no timeout is specified,
the command will wait indefinitely for the bus recovery to succeed.

.. note::
   The ``recover`` subcommand is only available if :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE`
   is enabled.