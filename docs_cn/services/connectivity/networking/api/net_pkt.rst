.. _net_pkt_interface:

Packet
Management
#################

.. contents::
    :local:
    :depth:
    2

Overview
********

Network
packets
是
networking
stack
manipulates
的
main
data。
这样
的
data
通过
net_pkt
structure
represented
它
提供
一
个
means
hold
packet、
write
和
read
它
同时
还有
core
hold
重要
information
所需
的
necessary
metadata。
这样
的
object
在
这
个
document
中
被
called
net_pkt。

Data
structure
和
它
周围
的
整个
API
在
:zephyr_file:`include/zephyr/net/net_pkt.h`
中
defined。

Architectural
notes
==================

Stack
内
有
两
个
network
packets
flows
**TX**
用于
transmission
path
和
**RX**
用于
reception
一
个。
在
两
个
paths
中
每个
net_pkt
从
beginning
到
end
被
written
和
read
或
更
specific
地
从
headers
到
payload。

Concurrency
and
Thread
Safety
=============================

``net_pkt``
structure
和
它
的
associated
APIs
**不
是
thread
safe
的**。
Network
stack
rely
on
严格
的
**Exclusive
Ownership**
model。
当
一
个
network
packet
被
created
或
received
时
它
在
任何
给定
time
被
单
个
thread
或
execution
context
owned。

Concurrency
用
以下
primary
patterns
managed：

*
**Ownership
Transfer
via
FIFOs**：
``net_pkt``
的
most
common
的
lifecycle
involved


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
=====================

As said earlier, though net_pkt uses net_buf for its buffer, it
provides its own API to access it. Indeed, a network packet might be
scattered over a chain of net_buf objects, the functions provided by
net_buf are then limited for such case.  Instead, net_pkt provides
functions which hide all the complexity of potential non-contiguous
access.

Data movement into the buffer is made through a cursor maintained
within each net_pkt.  All read/write operations affect this
cursor. Note as well that read or write functions are strict on their
length parameters: if it cannot r/w the given length it will
fail. Length is not interpreted as an upper limit, it is instead the
exact amount of data that must be read or written.

As there are two paths, TX and RX, there are two access modes: write
and overwrite.  This might sound a bit unusual, but is in fact simple
and provides flexibility.

In write mode, whatever is written in the buffer affects the length of
actual data present in the buffer. Buffer length should not be
confused with the buffer size which is a limit any mode cannot pass.
In overwrite mode then, whatever is written must happen on valid data,
and will not affect the buffer length. By default, a newly allocated
net_pkt is on write mode, and its cursor points to the beginning of
its buffer.

Let's see now, step by step, the functions and how they behave
depending on the mode.

When freshly allocated with a buffer of 500 bytes, a net_pkt has 0
length, which means no valid data is in its buffer. One could verify
this by:

.. code-block:: c

    len = net_pkt_get_len(pkt);

Now, let's write 8 bytes:

.. code-block:: c

    net_pkt_write(pkt, data, 8);

The buffer length is now 8 bytes.
There are various helpers to write a byte, or big endian uint16_t, uint32_t.

.. code-block:: c

    net_pkt_write_u8(pkt, &foo);
    net_pkt_write_be16(pkt, &ba);
    net_pkt_write_be32(pkt, &bar);

Logically, net_pkt's length is now 15. But if we try to read at this
point, it will fail because there is nothing to read at the cursor
where we are at in the net_pkt. It is possible, while in write mode,
to read what has been already written by resetting the cursor of the
net_pkt. For instance:

.. code-block:: c

    net_pkt_cursor_init(pkt);
    net_pkt_read(pkt, data, 15);

This will reset the cursor of the pkt to the beginning of the buffer
and then let you read the actual 15 bytes present. The cursor is then
again pointing at the end of the buffer.

To set a large area with the same byte, a memset function is provided:

.. code-block:: c

    net_pkt_memset(pkt, 0, 5);

Our net_pkt has now a length of 20 bytes.

Switching between modes can be achieved via
:c:func:`net_pkt_set_overwrite` function. It is possible to switch
mode back and forth at any time.  The net_pkt will be set to overwrite
and its cursor reset:

.. code-block:: c

    net_pkt_set_overwrite(pkt, true);
    net_pkt_cursor_init(pkt);

Now the same operators can be used, but it will be limited to the
existing data in the buffer, i.e. 20 bytes.

If it is necessary to know how much space is available in the net_pkt
call:

.. code-block:: c

    net_pkt_available_buffer(pkt);

Or, if headers space needs to be accounted for, call:

.. code-block:: c

    net_pkt_available_payload_buffer(pkt, proto);

If you want to place the cursor at a known position use the function
:c:func:`net_pkt_skip`.  For example, to go after the IP header, use:

.. code-block:: c

    net_pkt_cursor_init(pkt);
    net_pkt_skip(pkt, net_pkt_ip_header_len(pkt));


Data access
===========

Though the API shown previously is rather simple, it involves always
copying things to and from the net_pkt buffer. In many occasions, it
is more relevant to access the information stored in the buffer
contiguously, especially with network packets which embed headers.

These headers are, most of the time, a known fixed set of bytes. It is
then more natural to have a structure representing a certain type of
header.  In addition to this, if it is known the header size appears
in a contiguous area of the buffer, it will be way more efficient to
cast the actual position in the buffer to the type of header. Either
for reading or writing the fields of such header, accessing it
directly will save memory.

Net pkt comes with a dedicated API for this, built on top of the
previously described API. It is able to handle both contiguous and
non-contiguous access transparently.

There are two macros used to define a data access descriptor:
:c:macro:`NET_PKT_DATA_ACCESS_DEFINE` when it is not possible to
tell if the data will be in a contiguous area, and
:c:macro:`NET_PKT_DATA_ACCESS_CONTIGUOUS_DEFINE` when
it is guaranteed the data is in a contiguous area.

Let's take the example of IP and UDP. Both IPv4 and IPv6 headers are
always found at the beginning of the packet and are small enough to
fit in a net_buf of 128 bytes (for instance, though 64 bytes could be
chosen).

.. code-block:: c

    NET_PKT_DATA_ACCESS_CONTIGUOUS_DEFINE(ipv4_access, struct net_ipv4_hdr);
    struct net_ipv4_hdr *ipv4_hdr;

    ipv4_hdr = (struct net_ipv4_hdr *)net_pkt_get_data(pkt, &ipv4_access);

It would be the same for struct net_ipv4_hdr. For a UDP header it
is likely not to be in a contiguous area in IPv6
for instance so:

.. code-block:: c

    NET_PKT_DATA_ACCESS_DEFINE(udp_access, struct net_udp_hdr);
    struct net_udp_hdr *udp_hdr;

    udp_hdr = (struct net_udp_hdr *)net_pkt_get_data(pkt, &udp_access);

At this point, the cursor of the net_pkt points at the beginning of
the requested data. On the RX path, these headers will be read but not
modified so to proceed further the cursor needs to advance past the
data. There is a function dedicated for this:

.. code-block:: c

    net_pkt_acknowledge_data(pkt, &ipv4_access);

On the TX path, however, the header fields have been modified. In such
a case:

.. code-block:: c

    net_pkt_set_data(pkt, &ipv4_access);

If the data are in a contiguous area, it will advance the cursor
relevantly. If not, it will write the data and the cursor will be
updated. Note that :c:func:`net_pkt_set_data` could be used in the RX
path as well, but it is slightly faster to use
:c:func:`net_pkt_acknowledge_data` as this one does not care about
contiguity at all, it just advances the cursor via
:c:func:`net_pkt_skip` directly.


API Reference
*************

.. doxygengroup:: net_pkt