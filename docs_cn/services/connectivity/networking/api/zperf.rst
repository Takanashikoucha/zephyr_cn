.. _zperf:

zperf:
Network
Traffic
Generator
################################

.. contents::
    :local:
    :depth:
    2

Overview
********

zperf
是
一
个
shell
utility
它
允许
在
Zephyr
中
generate
network
traffic。
该
tool
可
被
used
用于
evaluate
network
bandwidth。

zperf
与
iPerf
2.0.10
及
更新
版本
compatible。
要
与
较
old
版本
compatible
enable
:kconfig:option:`CONFIG_NET_ZPERF_LEGACY_HEADER_COMPAT`。
或者
zperf
可以
speak
iperf3
参考
:ref:`zperf_iperf3`。
一
个
build
speak
两
个
中
的
一
个。

zperf
可以
在
任何
application
中
被
enabled
Zephyr
中
也
有
一
个
dedicated
的
sample。
参考
:zephyr:code-sample:`zperf
sample
application
<zperf>`
获取
details。

Sample
Usage
************

如果
Zephyr
作为
client
iPerf
必须
被
executed
在
server
mode。
例如
以下
command
line
必须
被
used
用于
UDP
testing：

.. code-block::
   console

   $
   iperf
   -s
   -l
   1K
   -u
   -V
   -B
   2001:db8::2

对于
TCP
testing
command
line
将
看起来
如
这
个：

.. code-block::
   console

   $
   iperf
   -s
   -l
   1K
   -V
   -B
   2001:db8::2


在
Zephyr
console
中
zperf
可以
被
executed
如
下：


.. note::

   以下为原文（待翻译）


   "``jobs``", "Show currently active or finished sessions"
   "``jobs all``", "Show statistics of finished sessions"
   "``jobs clear``", "Clear finished session statistics"
   "``jobs start``", "Start all the waiting sessions"

Example:

.. code-block:: console

   uart:~$ zperf udp upload -a -t 5 192.0.2.2 5001 10 1K 1M
   Remote port is 5001
   Connecting to 192.0.2.2
   Duration:       10.00 s
   Packet size:    1000 bytes
   Rate:           1000 kbps
   Starting...
   Rate:           1.00 Mbps
   Packet duration 7 ms

   uart:~$ zperf jobs all
   No sessions sessions found
   uart:~$ zperf jobs
              Thread    Remaining
   Id  Proto  Priority  time (sec)
   [1] UDP    5            4

   Active sessions have not yet finished
   -
   Upload completed!
   Statistics:             server  (client)
   Duration:               30.01 s (30.01 s)
   Num packets:            3799    (3799)
   Num packets out order:  0
   Num packets lost:       0
   Jitter:                 63 us
   Rate:                   1.01 Mbps       (1.01 Mbps)
   Thread priority:        5
   Protocol:               UDP
   Session id:             1

   uart:~$ zperf jobs all
   -
   Upload completed!
   Statistics:             server  (client)
   Duration:               30.01 s (30.01 s)
   Num packets:            3799    (3799)
   Num packets out order:  0
   Num packets lost:       0
   Jitter:                 63 us
   Rate:                   1.01 Mbps       (1.01 Mbps)
   Thread priority:        5
   Protocol:               UDP
   Session id:             1
   Total 1 sessions done

   uart:~$ zperf jobs clear
   Cleared data from 1 sessions

   uart:~$ zperf jobs
   No active upload sessions
   No finished sessions found

The ``-w`` option can be used like this to delay the startup of the jobs.

.. code-block:: console

   uart:~$ zperf tcp upload -a -t 6 -w 192.0.2.2 5001 10 1K
   Remote port is 5001
   Connecting to 192.0.2.2
   Duration:       10.00 s
   Packet size:    1000 bytes
   Rate:           10 kbps
   Waiting "zperf jobs start" command.
   [01:06:51.392,288] <inf> net_zperf: [0] TCP waiting for start

   uart:~$ zperf udp upload -a -t 6 -w 192.0.2.2 5001 10 1K 10M
   Remote port is 5001
   Connecting to 192.0.2.2
   Duration:       10.00 s
   Packet size:    1000 bytes
   Rate:           10000 kbps
   Waiting "zperf jobs start" command.
   Rate:           10.00 Mbps
   Packet duration 781 us
   [01:06:58.064,552] <inf> net_zperf: [0] UDP waiting for start

   uart:~$ zperf jobs start
   -
   Upload completed!
   -
   Upload completed!

   # Note that the output may be garbled as two threads printed
   # output at the same time. Just print out the fresh listing
   # like this.

   uart:~$ zperf jobs all
   -
   Upload completed!
   Statistics:             server  (client)
   Duration:               9.99 s  (10.00 s)
   Num packets:            11429   (11429)
   Num packets out order:  0
   Num packets lost:       0
   Jitter:                 164 us
   Rate:                   9.14 Mbps       (9.14 Mbps)
   Thread priority:        6
   Protocol:               UDP
   Session id:             0
   -
   Upload completed!
   Duration:               10.00 s
   Num packets:            15487
   Num errors:             0 (retry or fail)
   Rate:                   12.38 Mbps
   Thread priority:        6
   Protocol:               TCP
   Session id:             0
   Total 2 sessions done

Custom Data Upload
******************

zperf supports more advanced data upload profiling by setting a custom data
source through :c:member:`zperf_upload_params.data_loader`. This enables the
generation of custom packet contents instead of sending a constant packet
consisting solely of the ``z`` character. An example use case would be
determining the maximum throughput of uploading data from an external flash
memory chip.

Raw TX Mode
***********

zperf supports raw packet transmission mode for testing custom L2 frames or
vendor-specific protocols. This mode bypasses UDP/TCP and sends raw packets
directly using packet sockets.

To enable raw TX mode, set the following Kconfig options:

.. code-block:: kconfig

   CONFIG_NET_SOCKETS_PACKET=y
   CONFIG_NET_ZPERF_RAW_TX=y

The maximum header size can be configured with
:kconfig:option:`CONFIG_NET_ZPERF_RAW_TX_MAX_HDR_SIZE` (default: 64 bytes).

Before using raw TX mode, TX injection mode must be enabled on the network
interface:

.. code-block:: console

   uart:~$ net iface txinjection 1 on

The raw TX upload command syntax is:

.. code-block:: console

   zperf raw upload [-a] <if_index> <header_hex> [<duration_sec>] [<packet_size>] [<rate_kbps>]

Where:

- ``-a``: Optional async mode flag
- ``if_index``: Network interface index (e.g., 1)
- ``header_hex``: User-provided header as hex string (vendor metadata + frame header)
- ``duration_sec``: Test duration in seconds (default: 1)
- ``packet_size``: Total packet size including header (default: 256)
- ``rate_kbps``: Target rate in Kbps, supports K/M suffixes (default: 10)

Example for sending raw 802.11 frames with vendor metadata:

.. code-block:: console

   uart:~$ zperf raw upload 1 12345678000400030000000088000000ffffffffffa06960e35215a06960e3521500000000aaaa030000000800 10 1024 50M

The header hex string contains:

- Vendor metadata (first 12 bytes in this example)
- 802.11 QoS Data header with LLC/SNAP

The payload (filled with ``z`` characters) is automatically appended to reach
the specified packet size.
