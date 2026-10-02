.. _zperf:

zperf：网络流量生成器
################################

.. contents::
    :local:
    :depth: 2

概述
********

zperf 是一个 shell 工具，允许在 Zephyr 中生成网络流量。
该工具可用于评估网络带宽。

zperf 与 iPerf 2.0.10 及更新版本兼容。要与旧版本兼容，
启用 :kconfig:option:`CONFIG_NET_ZPERF_LEGACY_HEADER_COMPAT`。或者，zperf 可以支持
iperf3，参见 :ref:`zperf_iperf3`。一次构建支持两者之一。

zperf 可以在任何应用程序中启用，Zephyr 中也有一个专门的示例。
详情参见 :zephyr:code-sample:`zperf 示例应用程序 <zperf>`。

示例用法
************

如果 Zephyr 作为客户端，iPerf 必须以服务器模式运行。
例如，UDP 测试必须使用以下命令行：

.. code-block:: console

   $ iperf -s -l 1K -u -V -B 2001:db8::2

TCP 测试的命令行如下：

.. code-block:: console

   $ iperf -s -l 1K -V -B 2001:db8::2


在 Zephyr 控制台中，zperf 可以按如下方式执行：

.. code-block:: console

   zperf udp upload 2001:db8::2 5001 10 1K 1M


TCP 的 zperf 命令如下：

.. code-block:: console

   zperf tcp upload 2001:db8::2 5001 10 1K 1M


如果 Zephyr 和主机的 IP 地址在
配置文件中指定，zperf 可以按如下方式启动：

.. code-block:: console

   zperf udp upload2 v6 10 1K 1M


如果要测试 TCP，则如下：

.. code-block:: console

   zperf tcp upload2 v6 10 1K 1M


如果 Zephyr 作为服务器，UDP 的下载模式设置如下：

.. code-block:: console

   zperf udp download 5001


TCP 则如下：

.. code-block:: console

   zperf tcp download 5001


在主机端，如果测试 UDP，iPerf 必须使用以下
命令行运行：

.. code-block:: console

   $ iperf -l 1K -u -V -c 2001:db8::1 -p 5001


如果测试 TCP，则如下：

.. code-block:: console

   $ iperf -l 1K -V -c 2001:db8::1 -p 5001


如果 Zephyr 无法有序接收所有数据包，
可以使用 -b 选项限制 iPerf 输出。

.. _zperf_iperf3:

iperf3
******

使用 :kconfig:option:`CONFIG_NET_ZPERF_IPERF3`，zperf 与 iperf3 互操作，而不是
与 iPerf 2 互操作。支持是实验性的。zperf API 和 shell 命令保持不变，默认端口变为 5201，
即 iperf3 的默认端口。

当 Zephyr 作为服务器时，启用要接受的协议：

.. code-block:: console

   zperf tcp download
   zperf udp download

iperf3 客户端为每个测试选择 TCP 或 UDP，一个端口用于两者，无论哪种都有 TCP 控制
连接。因此两个命令共享监听端口：各自启用其
协议，请求未启用协议的测试会被拒绝。在主机上：

.. code-block:: console

   $ iperf3 -c 2001:db8::1
   $ iperf3 -c 2001:db8::1 -u -b 10M

当 Zephyr 作为客户端时，在主机上运行 ``iperf3 -s``，在 Zephyr 控制台中：

.. code-block:: console

   zperf tcp upload 2001:db8::2 5201 10 1K
   zperf udp upload 2001:db8::2 5201 10 1K 10M

测试在单个流上运行。反向（``-R``）、双向（``--bidir``）和并行
（``-P``）测试，以及省略测试开始（``-O``），都会以 iperf3
为服务器未实现的选项打印的消息被拒绝。一次运行一个测试，第二个客户端
会被告知服务器忙。多播和
:kconfig:option:`CONFIG_ZPERF_SESSION_PER_THREAD` 是 iPerf 2 的功能。

与 iPerf 2 比较时需要注意的要点：

* iperf3 服务器计数 TCP 数据直到客户端在控制连接上结束测试，
  这可能晚于最后一个数据，因此可能报告略少于客户端发送的数据。
  iPerf 2 服务器计数直到连接关闭。
* 对于 UDP，服务器收到的最后一个之后丢失的数据包在 zperf
  上传报告中计为丢失，与 iPerf 2 相同。iperf3 本身将其排除。
* iperf3 不报告乱序，因此上传不报告乱序数据包。
* 服务器只读取每个 UDP 数据报的头部，依赖 ``ZSOCK_MSG_TRUNC`` 了解
  其完整长度。忽略该标志的套接字卸载驱动程序会导致其计数字节过少。
* 测试每端需要一个控制连接和一个数据流，关闭的连接在每个测试后
  会在 TIME_WAIT 中停留一段时间。在
  :kconfig:option:`CONFIG_NET_MAX_CONTEXTS` 和 :kconfig:option:`CONFIG_NET_MAX_CONN` 中为它们留出空间，
  如示例的 ``overlay-iperf3.conf`` 所做。

会话管理
******************

如果设置了 :kconfig:option:`CONFIG_ZPERF_SESSION_PER_THREAD` 选项，则
如果用户在启动上传时提供了 ``-a``
选项，可以同时执行多个上传会话。每个会话将有自己的工作队列
来运行测试。会话测试结果在测试
完成后也可以查看。会话可以用 ``-w`` 选项启动，然后
让工作线程等待启动信号，使所有线程
可以同时启动。这将防止 zperf shell
因为运行在比已启动会话线程更低优先级而无法运行的情况。如果只有一个上传会话，则 ``-w``
其实不需要。

以下 zperf shell 命令可用于会话管理：

.. csv-table::
   :header: "zperf shell 命令", "描述"
   :widths: auto

   "``jobs``", "显示当前活动或已完成的会话"
   "``jobs all``", "显示已完成会话的统计信息"
   "``jobs clear``", "清除已完成会话统计信息"
   "``jobs start``", "启动所有等待的会话"

示例：

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

``-w`` 选项可以按如下方式延迟任务的启动。

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

自定义数据上传
******************

zperf 通过 :c:member:`zperf_upload_params.data_loader` 设置自定义数据
源，支持更高级的数据上传性能分析。这允许
生成自定义数据包内容，而不是发送仅由 ``z`` 字符组成的固定数据包。一个示例用例是
确定从外部闪存
芯片上传数据的最大吞吐量。

原始 TX 模式
***********

zperf 支持原始数据包传输模式，用于测试自定义 L2 帧或
厂商特定协议。此模式绕过 UDP/TCP，使用数据包套接字
直接发送原始数据包。

要启用原始 TX 模式，设置以下 Kconfig 选项：

.. code-block:: kconfig

   CONFIG_NET_SOCKETS_PACKET=y
   CONFIG_NET_ZPERF_RAW_TX=y

最大头部大小可以用
:kconfig:option:`CONFIG_NET_ZPERF_RAW_TX_MAX_HDR_SIZE` 配置（默认：64 字节）。

使用原始 TX 模式之前，必须在网络
接口上启用 TX 注入模式：

.. code-block:: console

   uart:~$ net iface txinjection 1 on

原始 TX 上传命令语法为：

.. code-block:: console

   zperf raw upload [-a] <if_index> <header_hex> [<duration_sec>] [<packet_size>] [<rate_kbps>]

其中：

- ``-a``：可选异步模式标志
- ``if_index``：网络接口索引（例如 1）
- ``header_hex``：用户提供的头部（十六进制字符串（厂商元数据 + 帧头部）
- ``duration_sec``：测试时长（秒）（默认：1）
- ``packet_size``：含头部的总数据包大小（默认：256）
- ``rate_kbps``：目标速率（Kbps），支持 K/M 后缀（默认：10）。``0`` 表示尽可能快发送。

发送带厂商元数据的原始 802.11 帧示例：

.. code-block:: console

   uart:~$ zperf raw upload 1 12345678000400030000000088000000ffffffffffa06960e35215a06960e3521500000000aaaa030000000800 10 1024 50M

头部十六进制字符串包含：

- 厂商元数据（此示例中前 12 字节）
- 带 LLC/SNAP 的 802.11 QoS 数据头部

有效载荷（填充 ``z`` 字符）自动追加以达到
指定数据包大小。
