.. _net_pkt_interface:

数据包管理
#################

.. contents::
    :local:
    :depth: 2

概述
********

网络数据包是网络栈操作的主要数据。
这类数据通过 net_pkt 结构体表示，它提供了
保存数据包、读写数据包的手段，以及核心
保存重要信息所需的元数据。本文中，此类对象
称为 net_pkt。

该数据结构及其周围的整个 API 定义在
:zephyr_file:`include/zephyr/net/net_pkt.h` 中。

架构说明
===================

栈内部有两条网络数据包流：**TX** 为
发送路径，**RX** 为接收路径。在两条路径中，
每个 net_pkt 都是从开头读到末尾，
更具体地说，是从头部到有效载荷。

并发与线程安全
=============================

``net_pkt`` 结构体及其关联 API **不是线程安全的**。
网络栈依赖严格的**独占所有权**（Exclusive Ownership）模型。当一个网络
数据包被创建或接收时，它在任一时刻
都只由单个线程或执行上下文拥有。

并发通过以下主要模式进行管理：

*   **通过 FIFO 转移所有权：** ``net_pkt`` 最常见的生命周期涉及
    在相互隔离的执行上下文之间传递它（例如从接收驱动线程
    到 IP 栈）。数据包入队后，发送方即释放其引用并失去访问权。
*   **浅拷贝（``net_pkt_shallow_clone``）：** 如果一个数据包必须被某一层
    保留（例如 TCP 为可能的重传而保留），同时又被
    另一层处理，则使用 ``net_pkt_shallow_clone()`` 创建一个指向
    相同底层只读数据的新包装器（数据缓冲区本身
    通过线程安全的引用计数管理）。
*   **粗粒度协议锁：** 当数据包被有意保存在内存
    队列中时，由更高层子系统锁（例如连接
    互斥锁）保护。

``struct net_pkt`` 中的 ``atomic_ref`` 字段用于
内存生命周期管理（防止 Use-After-Free 问题），
而不是用于并发修改的锁。

内存管理
*****************

分配
==========

所有 net_pkt 对象都来自一个预定义的 net_pkt 结构体池。
该池通过以下方式定义：

.. code-block:: c

    NET_PKT_SLAB_DEFINE(name, count)

不过，很少需要用到它，因为核心
已经提供了两个池，一个用于 TX 路径，一个用于 RX 路径。

分配一个原始 net_pkt 可以通过以下方式完成：

.. code-block:: c

    pkt = net_pkt_alloc(timeout);

然而，就其本质而言，没有缓冲区的原始 net_pkt 毫无用处，
还需要各种元数据信息才能变得有意义。
它至少需要知道要发送所经过的网络接口，
或接收所经过的网络接口。由于这是一个非常常见
的操作，因此存在一个辅助函数：

.. code-block:: c

    pkt = net_pkt_alloc_on_iface(iface, timeout);

存在一个更完整的分配器，可以同时分配
net_pkt 及其缓冲区：

.. code-block:: c

    pkt = net_pkt_alloc_with_buffer(iface, size, family, proto, timeout);

缓冲区如何分配见下文。


缓冲区分配
====================

net_pkt 对象不定义自己的缓冲区，而是使用一个
现成的对象：:c:struct:`net_buf`。（更多信息
参见 :ref:`net_buf_interface`）。不过，它大多
隐藏了此类缓冲区的使用，因为 net_pkt 为缓冲区分配
带来了网络感知，并且如后文所述，
其操作也是如此。

要分配缓冲区，net_pkt 至少需要设置好
其网络接口。这在分配缓冲区时数据包
族（family）未知时也能正常工作。此时可以这样做：

.. code-block:: c

    net_pkt_alloc_buffer(pkt, size, proto, timeout);

其中如果未知，proto 可以为 0（不存在 IPPROTO_UNSPEC）。

如前所述，net_pkt 及其缓冲区可以通过
:c:func:`net_pkt_alloc_with_buffer` 一次性分配。实际上这是
使用最广泛的分配器。

数据包的接口、族和协议
被缓冲区分配用来判断所请求的大小能否
被分配。确实，分配器会利用网络接口
了解 MTU，然后利用族和协议了解头部空间
（如果只指定了这两者）。如果整体
在 MTU 之内，所分配的空间将是所请求大小加上（可能的）
头部空间。如果 MTU 空间不足，所请求
的大小会被缩小，以便可能的头部空间和新大小
能装入 MTU。

例如，在一个 MTU 为 1500
字节的以太网网络接口上：

.. code-block:: c

    pkt = net_pkt_alloc_with_buffer(iface, 800, NET_AF_INET4, IPPROTO_UDP, K_FOREVER);

会成功为新的 net_pkt 分配 800 + 20 + 8 字节的缓冲区，
其中：

.. code-block:: c

    pkt = net_pkt_alloc_with_buffer(iface, 1600, NET_AF_INET4, IPPROTO_UDP, K_FOREVER);

会成功分配 1500 字节，其中 20 + 8 字节（IPv4 +
UDP 头部）不会用于有效载荷。

在接收侧，当族和协议未知时：

.. code-block:: c

    pkt = net_pkt_rx_alloc_with_buffer(iface, 800, AF_UNSPEC, 0, K_FOREVER);

会分配 800 字节，不分配额外头部空间。
但：

.. code-block:: c

    pkt = net_pkt_rx_alloc_with_buffer(iface, 1600, AF_UNSPEC, 0, K_FOREVER);

会分配 1514 字节，即 MTU + 以太网头部空间。

可以通过调用 :c:func:`net_pkt_alloc_buffer`
来增加所分配的缓冲区空间，因为它会
考虑现有缓冲区。如果 net_pkt 的族
是有效的，它还会考虑头部空间，
以及 proto 参数。在这种情况下，新分配的缓冲区空间
会追加到现有缓冲区之后，
而不是插入到前面。不过要注意，此类
使用场景相当有限。通常，一开始就应该知道
应该请求多大的空间。


释放
============

每个 net_pkt 都带引用计数。分配时，引用计数
设为 1。引用计数可以通过
:c:func:`net_pkt_ref()` 递增，或
通过 :c:func:`net_pkt_unref()` 递减。当计数降到零时，缓冲区
也被解除引用，net_pkt 自动放回
空闲的 net_pkt_slabs。

如果 net_pkt 释放后仍需要其缓冲区，
需要在调用最后一个 net_pkt_unref 之前
将 net_buf 链上所有对象再引用一次。更多信息
参见 :ref:`net_buf_interface`。


操作
**********

有两种方式访问 net_pkt 缓冲区，
在以下章节中说明：基本读写访问和数据访问，
后者是推荐方式。

读写访问
=====================

如前所述，虽然 net_pkt 使用 net_buf 作为其缓冲区，但它
提供了自己的 API 来访问缓冲区。确实，一个网络数据包可能
散布在一串 net_buf 对象上，net_buf 提供的
函数在此类情况下能力有限。相反，net_pkt 提供了
隐藏所有潜在非连续访问复杂性的函数。

数据移入缓冲区是通过维护在每个
net_pkt 内部的光标完成的。所有读写操作都影响该
光标。还要注意，读或写函数对其
长度参数是严格的：如果无法按给定长度读/写，
就会失败。长度不被解释为上限，
而是必须读取或写入的精确数据量。

由于有两条路径（TX 和 RX），因此有两种访问模式：
写（write）和覆盖（overwrite）。这听起来可能有点
不寻常，但事实上很简单，
并提供了灵活性。

在写模式下，无论写入缓冲区的什么内容，
都会影响缓冲区中实际存在的
数据长度。缓冲区长度不应与缓冲区大小混淆，
后者是任何模式都不能逾越的限制。
而在覆盖模式下，写入必须
发生在有效数据上，
且不会影响缓冲区长度。默认情况下，新分配的
net_pkt 处于写模式，其光标
指向其缓冲区的开头。

现在让我们逐步看看这些函数以及
它们在不同模式下的行为。

当刚分配了一个 500 字节缓冲区的 net_pkt 时，
其长度为 0，
意味着其缓冲区中没有有效数据。可以通过以下方式
验证：

.. code-block:: c

    len = net_pkt_get_len(pkt);

现在，让我们写入 8 字节：

.. code-block:: c

    net_pkt_write(pkt, data, 8);

现在缓冲区长度为 8 字节。
存在各种辅助函数用于写入一个字节，
或大端 uint16_t、uint32_t。

.. code-block:: c

    net_pkt_write_u8(pkt, &foo);
    net_pkt_write_be16(pkt, &ba);
    net_pkt_write_be32(pkt, &bar);

从逻辑上讲，net_pkt 的长度现在为 15。但如果此时
尝试读取，会失败，因为光标
当前位置的 net_pkt 中没有任何可读内容。在写模式下，
可以通过重置
net_pkt 的光标来读取已写入的内容。例如：

.. code-block:: c

    net_pkt_cursor_init(pkt);
    net_pkt_read(pkt, data, 15);

这将把 pkt 的光标重置到缓冲区开头，
然后让你读取实际存在的 15 字节。之后光标
又指向缓冲区的末尾。

要用同一个字节填充一大片区域，提供了 memset 函数：

.. code-block:: c

    net_pkt_memset(pkt, 0, 5);

现在我们的 net_pkt 长度为 20 字节。

模式之间的切换可以通过
:c:func:`net_pkt_set_overwrite` 函数实现。可以
随时来回切换
模式。net_pkt 会被设为覆盖
模式并重置其光标：

.. code-block:: c

    net_pkt_set_overwrite(pkt, true);
    net_pkt_cursor_init(pkt);

现在可以使用相同的操作符，但
将仅限于缓冲区中
已有的数据，即 20 字节。

如果需要知道 net_pkt 中还有多少可用空间，
调用：

.. code-block:: c

    net_pkt_available_buffer(pkt);

或者，如果需要计入头部空间，调用：

.. code-block:: c

    net_pkt_available_payload_buffer(pkt, proto);

如果想把光标放到已知位置，使用函数
:c:func:`net_pkt_skip`。例如，要跳到 IP 头部之后，使用：

.. code-block:: c

    net_pkt_cursor_init(pkt);
    net_pkt_skip(pkt, net_pkt_ip_header_len(pkt));


数据访问
===================

虽然前面展示的 API 相当简单，但它总是
涉及在 net_pkt 缓冲区中来回拷贝数据。在许多场合，
连续访问缓冲区中存储的信息
更为合适，尤其是嵌入了头部的网络数据包。

这些头部大多数时候是已知的一组固定字节。
因此，更自然的做法是拥有一个表示某种
头部类型的结构体。除此之外，如果已知
头部大小出现在缓冲区的连续区域中，
将缓冲区中的实际位置强制转换为该头部类型
会高效得多。
无论是读取还是写入此类头部的字段，
直接访问都能节省内存。

net_pkt 为此附带了一套专用 API，构建在
前述 API 之上。它能够透明地
处理连续和非连续访问两种情况。

有两个宏用于定义数据访问描述符：
:c:macro:`NET_PKT_DATA_ACCESS_DEFINE` 用于
无法判断数据是否位于连续区域的情况，
:c:macro:`NET_PKT_DATA_ACCESS_CONTIGUOUS_DEFINE` 用于
保证数据位于连续区域的情况。

以 IP 和 UDP 为例。IPv4 和 IPv6 头部
总是位于数据包开头，且足够小，
能装进 128 字节的 net_buf（例如，
虽然也可以选 64 字节）。

.. code-block:: c

    NET_PKT_DATA_ACCESS_CONTIGUOUS_DEFINE(ipv4_access, struct net_ipv4_hdr);
    struct net_ipv4_hdr *ipv4_hdr;

    ipv4_hdr = (struct net_ipv4_hdr *)net_pkt_get_data(pkt, &ipv4_access);

struct net_ipv4_hdr 也是如此。对于 UDP 头部，
例如在 IPv6 中，它很可能
不位于连续区域，因此：

.. code-block:: c

    NET_PKT_DATA_ACCESS_DEFINE(udp_access, struct net_udp_hdr);
    struct net_udp_hdr *udp_hdr;

    udp_hdr = (struct net_udp_hdr *)net_pkt_get_data(pkt, &udp_access);

此时，net_pkt 的光标指向
所请求数据的开头。在 RX 路径中，这些头部
只读不改，因此要继续往下处理，光标需要
跳过这些数据。有一个专门的函数用于此：

.. code-block:: c

    net_pkt_acknowledge_data(pkt, &ipv4_access);

然而，在 TX 路径中，头部字段
已被修改。在这种情况下：

.. code-block:: c

    net_pkt_set_data(pkt, &ipv4_access);

如果数据位于连续区域，它会相应地
推进光标。如果不是，它会写入数据
并更新光标。注意 :c:func:`net_pkt_set_data`
在 RX 路径中也可以使用，
但使用 :c:func:`net_pkt_acknowledge_data` 会稍快一些，
因为它完全不关心连续性，
它只是直接通过 :c:func:`net_pkt_skip` 推进光标。


API 参考
*************

.. doxygengroup:: net_pkt
