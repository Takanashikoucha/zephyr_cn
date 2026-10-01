.. _network_configuration_guide:

Network Configuration Guide
###########################

.. contents::
    :local:
    :depth: 2

此文档描述如何根据系统中可用 resources 设置各种 network configuration options。

Network Buffer Configuration Options
************************************

Network buffer configuration options 控制我们可同时发送或接收多少 data。

:kconfig:option:`CONFIG_NET_PKT_RX_COUNT`
  可同时接收的 network packets 最大数量。

:kconfig:option:`CONFIG_NET_PKT_TX_COUNT`
  同时 pending 的 network packet sends 最大数量。

:kconfig:option:`CONFIG_NET_BUF_RX_COUNT`
  为接收 data 分配多少 network buffers。
  每个 net_buf 包含小 header（以及固定或可变 length 的 data buffer。:kconfig:option:`CONFIG_NET_BUF_DATA_SIZE` 在设置 :kconfig:option:`CONFIG_NET_BUF_FIXED_DATA_SIZE` 时使用。此为默认设置。Buffer 默认 size 为 128 bytes。

  :kconfig:option:`CONFIG_NET_BUF_VARIABLE_DATA_SIZE` 为 experimental 设置。那里每个 net_buf data portion 从 memory pool 分配（可为从 network 收到的 data 数量。从 network 收到 data 时（其放入 net_buf data portion。根据 device resources 和期望 network usage（user 可通过设置 :kconfig:option:`CONFIG_NET_BUF_DATA_SIZE` 调整固定 buffer 的 size（若使用可变 size buffers（可通过设置 :kconfig:option:`CONFIG_NET_PKT_BUF_RX_DATA_POOL_SIZE` 和 :kconfig:option:`CONFIG_NET_PKT_BUF_TX_DATA_POOL_SIZE` 调整 data pool size。

  使用固定 size data buffers 时（network buffers 的 memory 消耗可通过根据接收的 network data 类型选择 data 部分 size 调整。若将 data size 设为 256（但仅接收 32 bytes 长的 packets（则为每个 packet "浪费" 224 bytes（因为无法利用剩余 data。不应将 data size 设得太低（因为每个 net_buf 涉及某些 overhead。出于这些原因（默认 network buffer size 设为 128 bytes。

  可变 size data buffer feature 标记为 experimental（因为其未像固定 size buffers 那样接受大量测试。使用可变 size data buffers 尝试通过仅分配 network data 所需最小 data 量改善 memory 利用率。这里的额外成本为从 memory pool 动态分配 buffer 所需时间。

  例如（Ethernet 中 maximum transmission unit (MTU) size 为 1500 bytes。若要接收两个完整 frames（net_pkt RX count 应设为 2（且 net_buf RX count 为 (1500 / 128) * 2（即 24。若使用 TCP（这些值须更高（因为可在交付给 application 前内部 queue packets。

:kconfig:option:`CONFIG_NET_BUF_TX_COUNT`
  为发送 data 分配多少 network buffers。此为类似接收 buffer count 但用于发送的设置。


Connection Options
******************

:kconfig:option:`CONFIG_NET_MAX_CONN`
  此 option 告知支持多少 network connection endpoints。
  例如每个 TCP connection 需一个 connection endpoint。类似地（每个 listening UDP connection 需一个 connection endpoint。
  DHCP 和 DNS 等各种 system services 也需 connection endpoints 工作。
  Network shell command **net conn** 可在 runtime 查看 network connection 信息。

:kconfig:option:`CONFIG_NET_MAX_CONTEXTS`
  分配多少 network contexts。每个 network context 描述 listening 或发送 network traffic 时使用的 network 5-tuple。系统中每个 BSD socket 使用一个 network context。


Socket Options
**************

:kconfig:option:`CONFIG_ZVFS_POLL_MAX`
  支持的 poll() entries 最大数量。须根据系统中 poll 多少 BSD sockets 选择合适值。

:kconfig:option:`CONFIG_ZVFS_OPEN_MAX`
  打开 file descriptors 最大数量（包括 files、sockets、special devices 等。须根据系统中创建多少 BSD sockets 选择合适值。

:kconfig:option:`CONFIG_ZVFS_EVENTFD_MAX`
  ZVFS eventfds 最大数量。若干 networking subsystems（例如 HTTP server、CoAP server、LwM2M engine、PTP、SSH 和 socket service）分配 eventfd 唤醒其 poll loop。每个此类 subsystem 通过 ``CONFIG_ZVFS_EVENTFD_ADD_SIZE_*`` option 声明其 requirement（且实际 eventfd count 为此 option 与所有那些 requirements 之和中较大者。仅当 application 自行创建额外 eventfds 时显式设置此 option。

:kconfig:option:`CONFIG_NET_SOCKETPAIR_BUFFER_SIZE`
  此 option 由 socketpair() function 使用。其设置内部 intermediate buffer 的 size（bytes。这设置两个 socketpair endpoints 间可传递的 messages 最大 size 的限制。


TLS Options
***********

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CONTEXTS`
  TLS/DTLS contexts 最大数量。每个 TLS/DTLS connection 需一个 context。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CREDENTIALS`
  此 variable 设置特定 socket 可使用的 TLS/DTLS credentials 最大数量。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CIPHERSUITES`
  每 socket 的 TLS/DTLS ciphersuites 最大数量。
  此 variable 设置特定 socket 可使用的 TLS/DTLS ciphersuites 最大数量（若由 socket option 显式设置。
  默认（系统中可用的所有 ciphersuites 均可用于 socket。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_APP_PROTOCOLS`
  支持的 application layer protocols 最大数量。
  此 variable 设置可通过 socket option 显式设置的 TLS/DTLS 上支持的 application layer protocols 最大数量。
  默认（未设置支持的 application layer protocol。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CLIENT_SESSION_COUNT`
  此 variable 指定用于 TLS/DTLS session resumption 的存储 TLS/DTLS sessions 最大数量。

:kconfig:option:`CONFIG_TLS_MAX_CREDENTIALS_NUMBER`
   可注册的 TLS credentials 最大数量。
   确保此值足够高（使所有 certificates 可加载到 store。


IPv4/6 Options
**************

:kconfig:option:`CONFIG_NET_IF_MAX_IPV4_COUNT`
   系统中 IPv4 network interfaces 最大数量。
   这告知系统中将有多少 network interfaces 启用 IPv4。
   例如若有两个 network interfaces（但仅其中一个可用 IPv4 addresses（此值可设为 1。
   若两个 network interface 均可用 IPv4（设置应设为 2。

:kconfig:option:`CONFIG_NET_IF_MAX_IPV6_COUNT`
   系统中 IPv6 network interfaces 最大数量。
   此为类似 IPv4 count option 但用于 IPv6 的设置。


TCP Options
***********

:kconfig:option:`CONFIG_NET_TCP_TIME_WAIT_DELAY`
  在 TCP *TIME_WAIT* state 等待多久（毫秒。
  为避免（低概率）问题（前一 connection 的 delayed packets 被交付给重用相同 local/remote ports 的下一 connection（
  `RFC 793 <https://www.rfc-editor.org/rfc/rfc793>`_（TCP）建议将旧的、已关闭的 connection 保持在特殊 *TIME_WAIT* state 持续 2*MSL (Maximum Segment Lifetime)。RFC
  建议使用 2 分钟的 MSL（但注明

  *This is an engineering choice, and may be changed if experience indicates
  it is desirable to do so.*

  对低 resource systems（大 MSL 可能导致快速 resource 耗尽（及相关 DoS attacks。同时（packet misdelivery 问题在现代
  TCP stacks 中通过使用随机、非重复的 port numbers 和 initial sequence numbers 在很大程度上缓解。因此（Zephyr 默认使用低得多的 1500ms 值。值 0 完全禁用 *TIME_WAIT* state。

:kconfig:option:`CONFIG_NET_TCP_RETRY_COUNT`
  TCP segment retransmissions 最大数量。
  以下公式可用于确定 segment 被 buffer 等待 retransmission 的时间（ms）：

  .. math::

     \sum_{n=0}^{\mathtt{NET\_TCP\_RETRY\_COUNT}} \bigg(1 \ll n\bigg)\times
     \mathtt{NET\_TCP\_INIT\_RETRANSMISSION\_TIMEOUT}

  默认值 9（IP stack 将尝试 retransmit 最多 1:42 分钟。这尽可能接近
  `RFC 1122 <https://www.rfc-editor.org/rfc/rfc1122>`_ 推荐的最小值（1:40 分钟。
  仅 5 bits 专用于 retransmission count（故接受值在 0-31 范围。但强烈建议不低于 9。

  若发生 retransmission timeout（receive callback 以 :code:`-ETIMEDOUT` error code 调用（且 context 被 dereference。

:kconfig:option:`CONFIG_NET_TCP_MAX_SEND_WINDOW_SIZE`
  使用的 maximum sending window size。
  此值影响 TCP 如何选择 maximum sending window size。默认值 0 让 TCP stack 根据系统中配置的 network buffers 数量选择值。注意若系统中有多个活动 TCP connections（此值可能需要微调（降低）（否则多个
  TCP connections 可轻松耗尽 queued TX data 的 net_buf pool。

:kconfig:option:`CONFIG_NET_TCP_MAX_RECV_WINDOW_SIZE`
  使用的 maximum receive window size。
  此值定义 maximum TCP receive window size。增大
  此值可改善 connection throughput（但需系统中更多
  receive buffers 可用以高效运行。
  默认值 0 让 TCP stack 根据系统中配置的 network buffers 数量选择值。

:kconfig:option:`CONFIG_NET_TCP_RECV_QUEUE_TIMEOUT`
  queue 收到的 data 多久（ms。
  若收到 out-of-order TCP data（queue 其。此值告知
  在未能将 data 传递给 application 时 data 保留多久后丢弃。若设为 0（则不启用 receive
  queueing。值以毫秒为单位。

  注意当前版本仅顺序 queue data 即，
  queue 中不应有 holes。例如（若收到
  SEQs 5,4,3,6（且等待 SEQ 2（segments 3,4,5,6 中的 data 被 queue（按此顺序）（且收到
  SEQ 2 时交付给 application。但若收到 SEQs 5,4,3,7（则 SEQ 7 被丢弃
  因为列表将不连续（缺 6。


Traffic Class Options
*********************

接收或发送 network data 时可配置多个 traffic classes (queues)。每个 traffic class queue 实现为具有不同 priority 的 thread。这意味着可将较高 priority 的 network packet 放入较高 priority 的 network queue 以更快或更慢地发送或接收。由于 thread scheduling latencies（实践中发送 packet 最快的方式为不使用专用 traffic class thread 直接发送 packet。这就是为何用户空间未启用时默认 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` option 设为 0。若用户空间启用（最小 TX traffic class count 为 1。原因为用户空间 application 权限不足以直接交付 message。

接收侧（建议至少有一个接收 traffic class queue。原因为通常 network device driver 在 IRQ context 中运行（收到 packet 时（此时不应尝试直接将 network packet 交付给 upper layers（而应将 packet 放入 traffic class queue。若 network device driver 收到 packet 时不在 IRQ context 中运行（RX traffic class option :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 可设为 0。


Stack Size Options
******************

Network enabled 系统中有若干 network 特定 threads。
某些 threads 可能依赖可用于启用或禁用 feature 的 configure option。每个 thread stack size 已优化以允许常规 network operations。

Network management API 默认使用专用 thread。Thread
负责在启用 :kconfig:option:`CONFIG_NET_MGMT` 和
:kconfig:option:`CONFIG_NET_MGMT_EVENT` options 时将 network management events 交付给系统中设置的 event listeners。
若 options 启用（user 可注册 net_mgmt thread 为每个 network management event 调用的 callback function。
默认 net_mgmt event thread stack size 相当小。
思路为 callback function 做最少的事（使新
events 尽可能快交付给 listeners 且不丢失。
Net_mgmt event thread stack size 由
:kconfig:option:`CONFIG_NET_MGMT_EVENT_QUEUE_SIZE` option 控制。建议
不要在 callback function 中执行任何 blocking operations。

Network thread stack 利用率可用 kernel shell 的 **kernel threads** command 监控。
