.. _network_configuration_guide:

网络配置指南
###########################

.. contents::
    :local:
    :depth: 2

本文档描述如何根据系统中的可用资源设置各种网络配置选项。

网络缓冲区配置选项
************************************

网络缓冲区配置选项控制我们同时能够发送或接收多少数据。

:kconfig:option:`CONFIG_NET_PKT_RX_COUNT`
  我们同时能够接收的最大网络数据包数量。

:kconfig:option:`CONFIG_NET_PKT_TX_COUNT`
  同时处于待发送状态的最大网络数据包发送数量。

:kconfig:option:`CONFIG_NET_BUF_RX_COUNT`
  为接收数据分配了多少个网络缓冲区。
  每个 net_buf 包含一个小头部和一个固定或可变
  长度的数据缓冲区。当设置了 :kconfig:option:`CONFIG_NET_BUF_FIXED_DATA_SIZE` 时使用 :kconfig:option:`CONFIG_NET_BUF_DATA_SIZE`。
  这是默认设置。缓冲区的默认大小为 128 字节。

  :kconfig:option:`CONFIG_NET_BUF_VARIABLE_DATA_SIZE` 是一个实验性
  设置。在那里，每个 net_buf 的数据部分从内存池中分配，
  可以是我们从网络接收到的数据量。
  当从网络接收到数据时，它被放入 net_buf 数据部分。
  根据设备资源和期望的网络使用情况，用户可以通过设置 :kconfig:option:`CONFIG_NET_BUF_DATA_SIZE` 来调整
  固定缓冲区的大小，并在
  使用可变大小缓冲区时通过设置 :kconfig:option:`CONFIG_NET_PKT_BUF_RX_DATA_POOL_SIZE`
  和 :kconfig:option:`CONFIG_NET_PKT_BUF_TX_DATA_POOL_SIZE` 来调整数据池的大小。

  当使用固定大小的数据缓冲区时，可以通过根据我们接收的网络
  数据类型选择数据部分的大小来调整网络缓冲区的
  内存消耗。如果将数据大小设置为 256，但只接收
  32 字节长的数据包，那么我们对每个数据包都"浪费"了 224 字节，因为我们
  无法利用剩余的数据。不应将数据大小设置得太低，因为
  每个 net_buf 都涉及一些开销。出于这些原因，默认
  网络缓冲区大小被设置为 128 字节。

  可变大小的数据缓冲区特性被标记为实验性，因为它没有
  像固定大小的缓冲区那样经过充分测试。使用可变大小的数据
  缓冲区试图通过分配网络数据所需的最小
  数据量来提高内存利用率。这里的额外开销是
  从内存池动态分配缓冲区时所需的
  时间量。

  例如，在以太网中，最大传输单元（MTU）大小为 1500 字节。
  如果想接收两个完整帧，则应将 net_pkt RX 计数设置为 2，
  将 net_buf RX 计数设置为 (1500 / 128) * 2，即 24。
  如果正在使用 TCP，则这些值需要更高，因为我们可以
  在传递给应用程序之前在内部对数据包进行排队。

:kconfig:option:`CONFIG_NET_BUF_TX_COUNT`
  为发送数据分配了多少个网络缓冲区。这是与
  接收缓冲区计数类似的设置，但用于发送。


连接选项
******************

:kconfig:option:`CONFIG_NET_MAX_CONN`
  该选项指定支持多少个网络连接端点。
  例如，每个 TCP 连接需要一个连接端点。同样
  每个监听 UDP 连接需要一个连接端点。
  此外，各种系统服务如 DHCP 和 DNS 也需要连接端点才能工作。
  网络 shell 命令 **net conn** 可在运行时用于查看
  网络连接信息。

:kconfig:option:`CONFIG_NET_MAX_CONTEXTS`
  要分配的网络上下文数量。每个网络上下文描述一个网络
  5 元组，用于监听或发送网络流量。系统中的每个 BSD 套接字
  使用一个网络上下文。


套接字选项
**************

:kconfig:option:`CONFIG_ZVFS_POLL_MAX`
  支持的 poll() 条目的最大数量。需要根据
  系统中轮询了多少个 BSD 套接字来选择合适的值。

:kconfig:option:`CONFIG_ZVFS_OPEN_MAX`
  打开文件描述符的最大数量，这包括文件、套接字、特殊设备等。
  需要根据系统中创建了多少个 BSD 套接字
  来选择合适的值。

:kconfig:option:`CONFIG_ZVFS_EVENTFD_MAX`
  ZVFS eventfd 的最大数量。几个网络子系统（例如 HTTP 服务器、
  CoAP 服务器、LwM2M 引擎、PTP、SSH 和套接字服务）会分配一个 eventfd 来唤醒
  其 poll 循环。每个这样的子系统都通过
  ``CONFIG_ZVFS_EVENTFD_ADD_SIZE_*`` 选项声明其需求，实际的 eventfd 数量是
  该选项与所有这些需求之和中较大的一个。仅当
  应用程序自行创建额外的 eventfd 时才显式设置此选项。

:kconfig:option:`CONFIG_NET_SOCKETPAIR_BUFFER_SIZE`
  该选项由 socketpair() 函数使用。它设置了
  内部中间缓冲区的大小（以字节为单位）。这设置了两个 socketpair 端点之间可以传递的
  消息的最大大小。


TLS 选项
***********

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CONTEXTS`
  TLS/DTLS 上下文的最大数量。每个 TLS/DTLS 连接需要一个上下文。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CREDENTIALS`
  该变量设置可以与特定套接字一起使用的
  TLS/DTLS 凭据的最大数量。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CIPHERSUITES`
  每个套接字的 TLS/DTLS 密码套件最大数量。
  该变量设置如果通过套接字选项显式设置，则可以与
  特定套接字一起使用的 TLS/DTLS 密码套件的最大数量。
  默认情况下，系统中可用的所有密码套件
  都可供套接字使用。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_APP_PROTOCOLS`
  支持的应用层协议的最大数量。
  该变量设置可以通过套接字选项显式设置的、
  在 TLS/DTLS 之上支持的应用层
  协议的最大数量。默认情况下，不设置任何支持的应用层协议。

:kconfig:option:`CONFIG_NET_SOCKETS_TLS_MAX_CLIENT_SESSION_COUNT`
  该变量指定存储的 TLS/DTLS 会话的最大数量，
  用于 TLS/DTLS 会话恢复。

:kconfig:option:`CONFIG_TLS_MAX_CREDENTIALS_NUMBER`
   可以注册的 TLS 凭据的最大数量。
   确保该值足够高，以便所有
   证书都能加载到存储中。


IPv4/6 选项
**************

:kconfig:option:`CONFIG_NET_IF_MAX_IPV4_COUNT`
   系统中 IPv4 网络接口的最大数量。
   这指定系统中将有多少个
   启用了 IPv4 的网络接口。
   例如，如果你有两个网络接口，但只有一个
   可以使用 IPv4 地址，则可以将此值设置为 1。
   如果两个网络接口都可以使用 IPv4，则应将设置
   设为 2。

:kconfig:option:`CONFIG_NET_IF_MAX_IPV6_COUNT`
   系统中 IPv6 网络接口的最大数量。
   这是与 IPv4 计数选项类似的设置，但用于 IPv6。


TCP 选项
***********

:kconfig:option:`CONFIG_NET_TCP_TIME_WAIT_DELAY`
  在 TCP *TIME_WAIT* 状态下等待多长时间（以毫秒为单位）。
  为避免一种（低概率）问题，即来自
  前一个连接的延迟数据包被投递到重用
  相同本地/远程端口的下一个连接，
  `RFC 793 <https://www.rfc-editor.org/rfc/rfc793>`_（TCP）建议
  将旧的、已关闭的连接保持在特殊的 *TIME_WAIT* 状态，持续
  2*MSL（最大段生存时间）的时间。该 RFC
  建议使用 2 分钟的 MSL，但指出

  *这是一个工程选择，如果经验表明
  这样做是可取的，则可以更改。*

  对于资源有限的系统，较大的 MSL 可能导致
  资源快速耗尽（以及相关的 DoS 攻击）。与此同时，
  数据包误投递的问题在现代
  TCP 协议栈中在很大程度上通过使用随机的、不重复的端口号和初始
  序列数得到缓解。因此，Zephyr 默认使用低得多的 1500ms 值。值为 0 则完全禁用 *TIME_WAIT* 状态。

:kconfig:option:`CONFIG_NET_TCP_RETRY_COUNT`
  TCP 段重传的最大次数。
  可以使用以下公式来确定一个段将被缓冲等待重传的时间（以 ms 为单位）：

  .. math::

     \sum_{n=0}^{\mathtt{NET\_TCP\_RETRY\_COUNT}} \bigg(1 \ll n\bigg)\times
     \mathtt{NET\_TCP\_INIT\_RETRANSMISSION\_TIMEOUT}

  使用默认值 9，IP 协议栈将尝试
  重传最长 1 分 42 秒。这已尽可能
  接近 `RFC 1122 <https://www.rfc-editor.org/rfc/rfc1122>`_ 推荐的最小值
  （1 分 40 秒）。只有 5 位专门用于重传计数，因此接受的
  值在 0-31 范围内。但强烈建议不要
  低于 9。

  如果发生重传超时，接收回调
  将以 :code:`-ETIMEDOUT` 错误码被调用，并且上下文被解除引用。

:kconfig:option:`CONFIG_NET_TCP_MAX_SEND_WINDOW_SIZE`
  要使用的最大发送窗口大小。
  该值影响 TCP 如何选择最大发送窗口
  大小。默认值 0 让 TCP 协议栈根据系统中配置的
  网络缓冲区数量来选择该值。注意，如果系统中
  有多个活动的 TCP 连接，
  则此值可能需要微调（降低），否则多个
  TCP 连接很容易耗尽用于已排队 TX 数据的 net_buf 池。

:kconfig:option:`CONFIG_NET_TCP_MAX_RECV_WINDOW_SIZE`
  要使用的最大接收窗口大小。
  该值定义了最大 TCP 接收窗口大小。增大
  该值可以提高连接吞吐量，但需要系统中
  有更多可用的接收缓冲区才能高效运行。
  默认值 0 让 TCP 协议栈根据系统中配置的
  网络缓冲区数量来选择该值。

:kconfig:option:`CONFIG_NET_TCP_RECV_QUEUE_TIMEOUT`
  接收数据排队多长时间（以 ms 为单位）。
  如果我们接收到乱序的 TCP 数据，我们会对其进行排队。该值告诉
  如果我们未能将数据传递给应用程序，数据在被丢弃前
  保留多长时间。如果设置为 0，则不启用接收
  排队。该值以毫秒为单位。

  注意，在当前版本中我们只按顺序排队数据，即
  队列中不应有空洞。例如，如果我们接收到
  SEQ 5、4、3、6 并在等待 SEQ 2，则段 3、4、5、6 中的数据
  被排队（按此顺序），然后当我们接收到
  SEQ 2 时将其交给应用程序。但如果我们接收到 SEQ 5、4、3、7，则 SEQ 7 被丢弃，
  因为该列表将不按顺序排列，因为缺少数字 6。


流量类别选项
*********************

在接收或发送网络数据时，可以配置多个流量类别（队列）。每个流量类别队列实现为一个
具有不同优先级的线程。这意味着可以将较高优先级的网络数据包
放入较高优先级的网络队列中，以便更快或更慢地
发送或接收它。由于线程调度延迟，实际上
发送数据包最快的方式是不使用专用流量类别线程
直接发送数据包。这就是为什么默认
在未启用用户空间时 :kconfig:option:`CONFIG_NET_TC_TX_COUNT` 选项被设置为 0。如果启用了用户空间，则最小 TX 流量类别
计数为 1。原因是
用户空间应用程序没有足够的权限直接
投递消息。

在接收侧，建议至少有一个接收流量
类别队列。原因是通常网络设备驱动程序在
接收到数据包时运行在 IRQ 上下文中，在这种情况下，它不应尝试
直接将网络数据包投递到上层，而应将
数据包放入流量类别队列。如果网络设备驱动程序在
获取数据包时未运行在 IRQ 上下文中，则 RX 流量类别
选项 :kconfig:option:`CONFIG_NET_TC_RX_COUNT` 可以设置为 0。


栈大小选项
******************

在启用了网络的系统中，有若干个网络专用线程。
某些线程可能依赖于一个可用于
启用或禁用某项功能的配置选项。每个线程栈大小都经过优化，
以允许正常的网络操作。

网络管理 API 默认使用一个专用线程。该线程
负责在启用了 :kconfig:option:`CONFIG_NET_MGMT` 和
:kconfig:option:`CONFIG_NET_MGMT_EVENT` 选项时，将网络管理事件投递到系统中设置的
事件监听器。
如果选项已启用，用户能够注册一个回调函数，
net_mgmt 线程会为每个网络管理事件调用它。
默认情况下，net_mgmt 事件线程栈大小相当小。
其想法是回调函数只做最少的事情，以便新
事件能够尽可能快地投递到监听器且不会丢失。
net_mgmt 事件线程栈大小由
:kconfig:option:`CONFIG_NET_MGMT_EVENT_QUEUE_SIZE` 选项控制。建议
不要在回调函数中执行任何阻塞操作。

可以从内核 shell 通过 **kernel threads** 命令
监控网络线程栈利用率。
