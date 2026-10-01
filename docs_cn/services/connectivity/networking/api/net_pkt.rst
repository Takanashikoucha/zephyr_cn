.. _net_pkt_interface:

Packet Management
#################

.. contents::
    :local:
    :depth: 2

Overview
********

Network packets 是 networking stack 操纵的主要 data。此类 data 通过 net_pkt structure 表示（其提供持有 packet、读写 packet 以及 core 持有重要信息所需 metadata 的手段。此类对象在此文档中称为 net_pkt。

Data structure 及其周围的整个 API 在 :zephyr_file:`include/zephyr/net/net_pkt.h` 中定义。

Architectural notes
===================

Stack 中有两个 network packets flows：**TX** 用于 transmission path（**RX** 用于 reception path。两个 paths 中（每个 net_pkt 从开头到末尾（更具体地从头 headers 到 payload）写入和读取。

Concurrency and Thread Safety
=============================

``net_pkt`` structure 及其关联 APIs **非 thread-safe**。Network stack 依赖严格的 **Exclusive Ownership** 模型。Network packet 创建或接收时（其在任何给定时间由单个 thread 或 execution context 拥有。

Concurrency 用以下主要 patterns 管理：

*   **Ownership Transfer via FIFOs**：``net_pkt`` 最常见的生命周期涉及在隔离的 execution contexts（如从 RX driver thread 到 IP stack）之间传递。Packet 入队后（sender 释放其引用（并失去访问。
*   **Shallow Cloning（``net_pkt_shallow_clone``）**：若 packet 须由一个 layer（如 TCP 以潜在 retransmission）保留（同时被另一个处理（用 ``net_pkt_shallow_clone()`` 创建指向相同底层 read-only data 的新 wrapper（data buffers 本身为 thread-safely reference counted）。
*   **Coarse-Grained Protocol Locks**：当 packets 有意保持在 memory queues 中（其由更高层 subsystem locks（如 connection mutexes）保护。

``struct net_pkt`` 中的 ``atomic_ref`` field 用于 memory lifecycle 管理（防止 Use-After-Free 条件）（而非并发 mutation 的 lock。

Memory management
*****************

Allocation
==========

所有 net_pkt objects 来自预定义的 struct net_pkt pool。此类 pool 通过

.. code-block:: c

    NET_PKT_SLAB_DEFINE(name, count)

定义。然而（很少须使用它（因为 core 已提供两个 pools（一个用于 TX path（一个用于 RX path。

Raw net_pkt 的分配可通过：

.. code-block:: c

    pkt = net_pkt_alloc(timeout);

然而（按其性质（raw net_pkt 无 buffer 无用（且需各种 metadata 信息才相关。其至少须获得其意在发送通过或接收通过的 network interface。由于这是非常常见的操作（有 helper：

.. code-block:: c

    pkt = net_pkt_alloc_on_iface(iface, timeout);

存在更完整的 allocator（net_pkt 和其 buffer 可同时分配：

.. code-block:: c

    pkt = net_pkt_alloc_with_buffer(iface, size, family, proto, timeout);

buffer 如何分配参见下文。


Buffer allocation
=================

Net_pkt 对象不定义自己的 buffer（而是用现有对象：:c:struct:`net_buf`（更多信息参见 :ref:`net_buf_interface`。然而（其大多隐藏此类 buffer 的使用（因为 net_pkt 为 buffer allocation 带来 network awareness（且如后文所述（其 operation 也是。

要分配 buffer（net_pkt 须至少设置其 network interface。这在 buffer allocation 时 packet 的 family 未知时有效。此时可：

.. code-block:: c

    net_pkt_alloc_buffer(pkt, size, proto, timeout);

其中 proto 若未知可为 0（无 IPPROTO_UNSPEC）。

如前所述（net_pkt 和其 buffer 可通过 :c:func:`net_pkt_alloc_with_buffer` 同时分配。其实际上是最广泛使用的 allocator。

Packet 的 network interface、family 和 protocol 由 buffer allocation 用于确定请求的 size 是否可分配。实际上（allocator 用 network interface 了解 MTU（然后用 family 和 protocol 了解 headers space（若仅指定此 2 个）。若整体在 MTU 内（分配的 space 为请求的 size 加上（可能的）headers space。若 MTU space 不足（请求的 size 缩小以使可能的 headers space 和新 size 在 MTU 内。

例如（在 MTU 为 1500 bytes 的 Ethernet network interface 上：

.. code-block:: c

    pkt = net_pkt_alloc_with_buffer(iface, 800, NET_AF_INET4, IPPROTO_UDP, K_FOREVER);

将成功为新 net_pkt 分配 800 + 20 + 8 bytes 的 buffer（其中：

.. code-block:: c

    pkt = net_pkt_alloc_with_buffer(iface, 1600, NET_AF_INET4, IPPROTO_UDP, K_FOREVER);

将成功分配 1500 bytes（其中 20 + 8 bytes（IPv4 + UDP headers）不用于 payload。

接收侧（当 family 和 protocol 未知时：

.. code-block:: c

    pkt = net_pkt_rx_alloc_with_buffer(iface, 800, AF_UNSPEC, 0, K_FOREVER);

将分配 800 bytes（无额外 header space。但：

.. code-block:: c

    pkt = net_pkt_rx_alloc_with_buffer(iface, 1600, AF_UNSPEC, 0, K_FOREVER);

将分配 1514 bytes（MTU + Ethernet header space。

可调用 :c:func:`net_pkt_alloc_buffer` 增加分配的 buffer space 量（其将考虑现有 buffer。若 net_pkt 的 family 为有效值（以及 proto parameter（其也将考虑 header space。此情况下（新分配的 buffer space 追加到现有 buffer 后（而非插入前面。注意此类 use case 相当有限。通常（一开始就应知道应请求多少 size。


Deallocation
============

每个 net_pkt 为 reference counted。分配时（reference 设为 1。Reference count 可用 :c:func:`net_pkt_ref()` 递增（或 :c:func:`net_pkt_unref()` 递减。当 count 降到 zero（buffer 也被 un-referenced（且 net_pkt 自动放回 free net_pkt_slabs。

若 net_pkt deallocation 后仍需要其 buffer（须在调用最后一个 net_pkt_unref 前再次引用所有 net_buf 链。更多信息参见 :ref:`net_buf_interface`。


Operations
**********

有两种方式访问 net_pkt buffer（以下 section 解释：basic read/write access 和 data access（后者为推荐方式。

Read and Write access
=====================

如前所述（虽然 net_pkt 用 net_buf 作为其 buffer（其提供自己的 API 以访问。实际上（network packet 可能散布在 net_buf objects 链上（net_buf 提供的 functions 对此情况有限。相反（net_pkt 提供隐藏潜在 non-contiguous 访问所有复杂性的 functions。

Data 移入 buffer 通过每个 net_pkt 内维护的 cursor 完成。所有 read/write operations 影响此 cursor。注意 read 或 write functions 对其 length parameters 严格：若无法 r/w 给定 length（其将失败。Length 不解释为上限（而是必须读取或写入的精确 data 量。

由于有两个 paths（TX 和 RX（有两个 access modes：write 和 overwrite。这可能听起来有点不寻常（但实际简单（并提供灵活性。

Write mode 中（写入 buffer 的无论什么影响 buffer 中实际 data 的长度。Buffer length 不应与 buffer size 混淆（后者为任何 mode 不可逾越的限制。Overwrite mode 中（写入的无论什么须发生在有效 data 上（且不影响 buffer length。默认（新分配的 net_pkt 处于 write mode（且其 cursor 指向其 buffer 的开头。

现在逐步看 functions 及其如何根据 mode 行为。

新分配带 500 bytes buffer 时（net_pkt 长度为 0（意味着其 buffer 中无有效 data。可验证：

.. code-block:: c

    len = net_pkt_get_len(pkt);

现在（写入 8 bytes：

.. code-block:: c

    net_pkt_write(pkt, data, 8);

Buffer length 现在为 8 bytes。有各种 helpers 以写入 byte（或 big endian uint16_t、uint32_t。

.. code-block:: c

    net_pkt_write_u8(pkt, &foo);
    net_pkt_write_be16(pkt, &ba);
    net_pkt_write_be32(pkt, &bar);

逻辑上（net_pkt 的长度现在为 15。但若此时尝试读取（将失败（因为 net_pkt 中 cursor 所在处无内容可读。Write mode 中（可通过重置 net_pkt 的 cursor 读取已写入的。例如：

.. code-block:: c

    net_pkt_cursor_init(pkt);
    net_pkt_read(pkt, data, 15);

这将重置 pkt 的 cursor 到 buffer 开头（然后允许读取实际存在的 15 bytes。Cursor 然后再次指向 buffer 末尾。

要用相同 byte 设置大区域（提供 memset function：

.. code-block:: c

    net_pkt_memset(pkt, 0, 5);

我们的 net_pkt 现在长度为 20 bytes。

Modes 间切换可用 :c:func:`net_pkt_set_overwrite` function 实现。可随时来回切换 mode。Net_pkt 设为 overwrite（且其 cursor 重置：

.. code-block:: c

    net_pkt_set_overwrite(pkt, true);
    net_pkt_cursor_init(pkt);

现在可用相同 operators（但限于 buffer 中现有 data（即 20 bytes。

若需了解 net_pkt 中可用多少 space（调用：

.. code-block:: c

    net_pkt_available_buffer(pkt);

或者（若需考虑 headers space（调用：

.. code-block:: c

    net_pkt_available_payload_buffer(pkt, proto);

若想将 cursor 置于已知位置（用 :c:func:`net_pkt_skip` function。例如（要移到 IP header 之后（用：

.. code-block:: c

    net_pkt_cursor_init(pkt);
    net_pkt_skip(pkt, net_pkt_ip_header_len(pkt));


Data access
===========

虽然前述 API 相当简单（其总涉及将 things 复制到 net_pkt buffer 和从中复制。许多场合（连续访问存储在 buffer 中的信息更相关（尤其是嵌入 headers 的 network packets。

这些 headers 大多数时候为已知固定 bytes 集。此时更自然有代表特定 header 类型的 structure。此外（若已知 header size 出现在 buffer 的连续区域（将 buffer 中实际位置 cast 为 header 类型将高效得多。无论读取还是写入此类 header 的 fields（直接访问节省 memory。

Net pkt 带专用于此的 API（构建于前述 API 之上。其能透明处理连续和 non-contiguous 访问两者。

有两个 macros 用于定义 data access descriptor：无法判断 data 是否在连续区域时用 :c:macro:`NET_PKT_DATA_ACCESS_DEFINE`（保证 data 在连续区域时用 :c:macro:`NET_PKT_DATA_ACCESS_CONTIGUOUS_DEFINE`。

以 IP 和 UDP 为例。IPv4 和 IPv6 headers 总在 packet 开头（且足够小以放入 128 bytes 的 net_buf（例如（虽然可选 64 bytes。

.. code-block:: c

    NET_PKT_DATA_ACCESS_CONTIGUOUS_DEFINE(ipv4_access, struct net_ipv4_hdr);
    struct net_ipv4_hdr *ipv4_hdr;

    ipv4_hdr = (struct net_ipv4_hdr *)net_pkt_get_data(pkt, &ipv4_access);

对 struct net_ipv4_hdr 相同。对 UDP header（在 IPv6 中很可能不在连续区域（因此：

.. code-block:: c

    NET_PKT_DATA_ACCESS_DEFINE(udp_access, struct net_udp_hdr);
    struct net_udp_hdr *udp_hdr;

    udp_hdr = (struct net_udp_hdr *)net_pkt_get_data(pkt, &udp_access);

此时（net_pkt 的 cursor 指向请求 data 的开头。RX path 中（这些 headers 读取但不修改（因此要继续（cursor 须推进过 data。有专用 function：

.. code-block:: c

    net_pkt_acknowledge_data(pkt, &ipv4_access);

然而（TX path 中（header fields 已修改。此情况下：

.. code-block:: c

    net_pkt_set_data(pkt, &ipv4_access);

若 data 在连续区域（将相应推进 cursor。若不在（将写入 data（且 cursor 更新。注意 :c:func:`net_pkt_set_data` 也可用于 RX path（但用 :c:func:`net_pkt_acknowledge_data` 略快（其完全不考虑 contiguity（仅通过 :c:func:`net_pkt_skip` 直接推进 cursor。


API Reference
*************

.. doxygengroup:: net_pkt
