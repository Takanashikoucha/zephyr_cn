.. _zperf:

zperf: Network Traffic Generator
################################

.. contents::
    :local:
    :depth: 2

Overview
********

zperf 为在 Zephyr 中生成 network traffic 的 shell utility。Tool 可用于评估 network bandwidth。

zperf 与 iPerf 2.0.10 及更新版本兼容。要与旧版本兼容（启用 :kconfig:option:`CONFIG_NET_ZPERF_LEGACY_HEADER_COMPAT`。或者（zperf 可讲 iperf3（参见 :ref:`zperf_iperf3`。Build 讲两者之一。

zperf 可在任何 application 中启用（Zephyr 中还有专用 sample。细节参见 :zephyr:code-sample:`zperf sample application <zperf>`。

Sample Usage
************

若 Zephyr 作为 client（iPerf 须以 server mode 执行。例如（UDP 测试须用以下 command line：

.. code-block:: console

   $ iperf -s -l 1K -u -V -B 2001:db8::2

TCP 测试的 command line 如下：

.. code-block:: console

   $ iperf -s -l 1K -V -B 2001:db8::2


在 Zephyr console 中（zperf 可按如下执行：

.. code-block:: console

   zperf udp upload 2001:db8::2 5001 10 1K 1M


TCP 的 zperf command 如下：

.. code-block:: console

   zperf tcp upload 2001:db8::2 5001 10 1K 1M


若 Zephyr 和 host machine 的 IP addresses 在 config file 中指定（zperf 可按如下启动：

.. code-block:: console

   zperf udp upload2 v6 10 1K 1M


若要测试 TCP（如下：

.. code-block:: console

   zperf tcp upload2 v6 10 1K 1M


若 Zephyr 作为 server（UDP 如下设置 download mode：

.. code-block:: console

   zperf udp download 5001


TCP 如下：

.. code-block:: console

   zperf tcp download 5001


host 侧（测试 UDP 时 iPerf 须用以下 command line 执行：

.. code-block:: console

   $ iperf -l 1K -u -V -c 2001:db8::1 -p 5001


测试 TCP 时如下：

.. code-block:: console

   $ iperf -l 1K -V -c 2001:db8::1 -p 5001


若 Zephyr 无法有序接收所有 packets（可用 -b option 限制 iPerf output。

.. _zperf_iperf3:

iperf3
******

带 :kconfig:option:`CONFIG_NET_ZPERF_IPERF3`（zperf 与 iperf3 互操作（而非 iPerf 2。支持为 experimental。zperf API 和 shell commands 不变（且默认 port 变为 5201（iperf3 默认。

Zephyr 作为 server 时（启用要接受的 protocols：

.. code-block:: console

   zperf tcp download
   zperf udp download

iperf3 client 为每个测试选择 TCP 或 UDP（并用一个 port 用于两者（无论哪种均有 TCP control connection。两个 command 因此共享 listening port：各自启用其 protocol（且请求未启用 protocol 的测试被拒绝。Host 上：

.. code-block:: console

   $ iperf3 -c 2001:db8::1
   $ iperf3 -c 2001:db8::1 -u -b 10M

Zephyr 作为 client 时（host 上运行 ``iperf3 -s``（Zephyr console 中：

.. code-block:: console

   zperf tcp upload 2001:db8::2 5201 10 1K
   zperf udp upload 2001:db8::2 5201 10 1K 10M

测试在单个 stream 上运行。Reverse（``-R``）、bidirectional（``--bidir``）和 parallel（``-P``）测试（以及省略测试开始（``-O``）（以 iperf3 为 server 未实现的 option 打印的消息拒绝。一次运行一个测试（且第二个 client 被告知 server 忙。Multicast 和 :kconfig:option:`CONFIG_ZPERF_SESSION_PER_THREAD` 为 iPerf 2 features。

与 iPerf 2 比较时须记住的 points：

* iperf3 server 计数 TCP data 直到 client 在 control connection 上结束测试（这可能晚于最后 data（故其可能报告略少于 client 发送的。iPerf 2 server 计数直到 connection 关闭。
* 对 UDP（server 收到的最后一个之后丢失的 datagrams 在 zperf upload report 中计为 lost（与 iPerf 2 一样。iperf3 本身将其排除。
* iperf3 不报告 reordering（故 upload 不报告 out-of-order packets。
* Server 仅读取每个 UDP datagram 的 header（依赖 ``ZSOCK_MSG_TRUNC`` 了解其完整 length。忽略该 flag 的 socket offload driver 使其计数过少 bytes。
* 测试每端取 control connection 和 data stream（且关闭的 connections 在每个测试后在 TIME_WAIT 中停留一段时间。在 :kconfig:option:`CONFIG_NET_MAX_CONTEXTS` 和 :kconfig:option:`CONFIG_NET_MAX_CONN` 中为它们留出空间（如 sample 的 ``overlay-iperf3.conf`` 所做。

Session Management
******************

若设置 :kconfig:option:`CONFIG_ZPERF_SESSION_PER_THREAD` option（则 user 在启动 upload 时提供 ``-a`` option 可同时执行多个 upload sessions。每个 session 将有自己的 work queue 运行测试。Session test results 在测试完成后也可查看。Sessions 可用 ``-w`` option 启动（其让 worker threads 等待 start signal（使所有 threads 可同时启动。这可防止 zperf shell 因运行在比已启动 session thread 更低 priority 而无法运行的情况。若仅有一个 upload session（``-w`` 其实不需要。

以下 zperf shell commands 可用于 session management：

.. csv-table::
   :header: "zperf shell command", "Description"
   :widths: auto

   "``jobs``", "显示当前活动或已完成的 sessions"
   "``jobs all``", "显示已完成 sessions 的 statistics"
   "``jobs clear``", "清除已完成 session statistics"
   "``jobs start``", "启动所有等待的 sessions"

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

``-w`` option 可按如下延迟 jobs 的启动。

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

zperf 通过 :c:member:`zperf_upload_params.data_loader` 设置 custom data source 支持更高级的 data upload profiling。这允许生成 custom packet contents（而非仅由 ``z`` 字符组成的 constant packet。使用示例为确定从外部 flash memory chip 上传 data 的最大 throughput。

Raw TX Mode
***********

zperf 支持 raw packet transmission mode 以测试 custom L2 frames 或 vendor-specific protocols。此 mode 绕过 UDP/TCP（用 packet sockets 直接发送 raw packets。

要启用 raw TX mode（设置以下 Kconfig options：

.. code-block:: kconfig

   CONFIG_NET_SOCKETS_PACKET=y
   CONFIG_NET_ZPERF_RAW_TX=y

最大 header size 可用 :kconfig:option:`CONFIG_NET_ZPERF_RAW_TX_MAX_HDR_SIZE` 配置（默认：64 bytes）。

使用 raw TX mode 前（须在 network interface 上启用 TX injection mode：

.. code-block:: console

   uart:~$ net iface txinjection 1 on

Raw TX upload command 语法为：

.. code-block:: console

   zperf raw upload [-a] <if_index> <header_hex> [<duration_sec>] [<packet_size>] [<rate_kbps>]

其中：

- ``-a``：可选 async mode flag
- ``if_index``：Network interface index（如 1）
- ``header_hex``：User 提供的 header（hex string（vendor metadata + frame header）
- ``duration_sec``：测试时长（秒）（默认：1）
- ``packet_size``：含 header 的总 packet size（默认：256）
- ``rate_kbps``：目标 rate（Kbps）（支持 K/M suffixes）（默认：10）

发送带 vendor metadata 的 raw 802.11 frames 示例：

.. code-block:: console

   uart:~$ zperf raw upload 1 12345678000400030000000088000000ffffffffffa06960e35215a06960e3521500000000aaaa030000000800 10 1024 50M

Header hex string 包含：

- Vendor metadata（此示例中前 12 bytes）
- 带 LLC/SNAP 的 802.11 QoS Data header

Payload（填充 ``z`` 字符）自动追加以达到指定 packet size。
