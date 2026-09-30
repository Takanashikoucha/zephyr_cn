.. _bsd_sockets_interface:

BSD
Sockets
###########

.. contents::
    :local:
    :depth:
    2

Overview
********

Zephyr
offer
一
个
BSD
Sockets
API
subset
的
implementation
（POSIX
standard
的
一
part）。
这
个
API
允许
reuse
现有
的
programming
experience
并
port
现有
的
简单
networking
applications
到
Zephyr。

以下
是
govern
Zephyr
的
BSD
Sockets
compatible
API
implementation
的
key
requirements
和
concepts：

*
有
minimal
的
overhead
与
其他
Zephyr
subsystems
的
requirement
相似。
*
Default
下
被
namespaced
避免
与
well
known
的
names
如
``close()``
的
name
conflicts
它们
可能
是
libc
或
其他
POSIX
compatibility
libraries
的
part。
如果
被
:kconfig:option:`CONFIG_POSIX_API`
enabled
它
也
将
expose
POSIX
compatible
的
APIs。

BSD
Sockets
compatible
API
用
:kconfig:option:`CONFIG_NET_SOCKETS`
config
option
enabled
并
implement
以下
operations：
``socket()``、
``close()``、
``recv()``、
``recvfrom()``、
``send()``、
``sendto()``、
``connect()``、
``bind()``、
``listen()``、
``accept()``、
``fcntl()``
（用于
set
non
blocking
mode）、
``getsockopt()``、
``setsockopt()``、
``poll()``、
``select()``、
``getaddrinfo()``、
``getnameinfo()``。

根据
上面
的
namespacing
requirements
这些
operations
default
下
被
exposed
作为
带
``zsock_``
prefix
的
functions
例如
:c:func:`zsock_socket`
和
:c:func:`zsock_close`。
如果
config
option
:kconfig:option:`CONFIG_POSIX_API`
被
defined
所有
的
functions
将
也
被
exposed
作为
不带
prefix
的
aliases。
这
包括
functions
如
``close()``
和
``fcntl()``
（它们
可能
conflict


.. note::

   以下为原文（待翻译）

.. note::

   Due to mbed TLS internal data buffering and ``mbedtls_ssl_write()`` function
   requirements, when a non-blocking :c:func:`zsock_send` returns ``EAGAIN``, it is
   expected that the consecutive call to :c:func:`zsock_send` will contain the same
   data as the original call.

Several samples in Zephyr use secure sockets for communication. For a sample use
see e.g. :zephyr:code-sample:`echo-server sample application <sockets-echo-server>` or
:zephyr:code-sample:`HTTP GET sample application <sockets-http-get>`.

Secure Sockets options
======================

Secure sockets offer the following options for socket management:

.. doxygengroup:: secure_sockets_options

Socket offloading
*****************

Zephyr allows to register custom socket implementations (called offloaded
sockets). This allows for seamless integration for devices which provide an
external IP stack and expose socket-like API.

Socket offloading can be enabled with :kconfig:option:`CONFIG_NET_SOCKETS_OFFLOAD`
option. A network driver that wants to register a new socket implementation
should use :c:macro:`NET_SOCKET_OFFLOAD_REGISTER` macro. The macro accepts the
following parameters:

 * ``socket_name``
     An arbitrary name for the socket implementation.

 * ``prio``
     Socket implementation's priority. The higher the priority, the earlier this
     particular implementation will be processed when creating a new socket.
     Lower numeric value indicates higher priority.

 * ``_family``
     Socket family implemented by the offloaded socket. ``AF_UNSPEC`` indicates
     any family.

 * ``_is_supported``
     A filtering function, used to verify whether a particular socket family,
     type and protocol are supported by the offloaded socket implementation.

 * ``_handler``
     A function compatible with :c:func:`socket` API, used to create an
     offloaded socket.

Every offloaded socket implementation should also implement a set of socket
APIs, specified in :c:struct:`socket_op_vtable` struct.

The function registered for socket creation should allocate a new file
descriptor using :c:func:`zvfs_reserve_fd` function. Any additional actions,
specific to the creation of a particular offloaded socket implementation,
should take place after the file descriptor is allocated. As a final step,
if the offloaded socket was created successfully, the file descriptor should
be finalized with :c:func:`zvfs_finalize_typed_fd`, or :c:func:`zvfs_finalize_fd`
functions. The finalize function allows to register a
:c:struct:`socket_op_vtable` structure implementing socket APIs for an
offloaded socket along with an optional socket context data pointer.

Finally, when an offloaded network interface is initialized, it should indicate
that the interface is offloaded with :c:func:`net_if_socket_offload_set`
function. The function registers the function used to create an offloaded socket
(the same as the one provided in :c:macro:`NET_SOCKET_OFFLOAD_REGISTER`) at the
network interface.

Offloaded socket creation
=========================

When application creates a new socket with :c:func:`socket` function, the
network stack iterates over all registered socket implementations (native and
offloaded). Higher priority socket implementations are processed first.
For each registered socket implementation, an address family is verified, and if
it matches (or the socket was registered as ``AF_UNSPEC``), the corresponding
``_is_supported`` function is called to verify the remaining socket parameters.
The first implementation that fulfills the socket requirements (i. e.
``_is_supported`` returns true) will create a new socket with its ``_handler``
function.

The above indicates the importance of the socket priority. If multiple socket
implementations support the same set of socket family/type/protocol, the first
implementation processed by the system will create a socket. Therefore it's
important to give the highest priority to the implementation that should be the
system default.

The socket priority for native socket implementation is configured with Kconfig.
Use :kconfig:option:`CONFIG_NET_SOCKETS_TLS_PRIORITY` to set the priority for
the native TLS sockets.
Use :kconfig:option:`CONFIG_NET_SOCKETS_PRIORITY_DEFAULT` to set the priority
for the remaining native sockets.

Dealing with multiple offloaded interfaces
==========================================

As the :c:func:`socket` function does not allow to specify which network
interface should be used by a socket, it's not possible to choose a specific
implementation in case multiple offloaded socket implementations, supporting the
same type of sockets, are available. The same problem arises when both native
and offloaded sockets are available in the system.

To address this problem, a special socket implementation (called socket
dispatcher) was introduced. The sole reason for this module is to postpone the
socket creation for until the first operation on a socket is performed. This
leaves an opening to use ``SO_BINDTODEVICE`` socket option, to bind a socket to
a particular network interface (and thus offloaded socket implementation).
The socket dispatcher can be enabled with :kconfig:option:`CONFIG_NET_SOCKETS_OFFLOAD_DISPATCHER`
Kconfig option.

When enabled, the application can specify the network interface to use with
:c:func:`setsockopt` function:

.. code-block:: c

   /* A "dispatcher" socket is created */
   sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

   struct ifreq ifreq = {
      .ifr_name = "SimpleLink"
   };

   /* The socket is "dispatched" to a particular network interface
    * (offloaded or not).
    */
   setsockopt(sock, SOL_SOCKET, SO_BINDTODEVICE, &ifreq, sizeof(ifreq));

Similarly, if TLS is supported by both native and offloaded sockets,
``TLS_NATIVE`` socket option can be used to indicate that a native TLS socket
should be created. The underlying socket can then be bound to a particular
network interface:

.. code-block:: c

   /* A "dispatcher" socket is created */
   sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TLS_1_2);

   int tls_native = 1;

   /* The socket is "dispatched" to a native TLS socket implmeentation.
    * The underlying socket is a "dispatcher" socket now.
    */
   setsockopt(sock, SOL_TLS, TLS_NATIVE, &tls_native, sizeof(tls_native));

   struct ifreq ifreq = {
      .ifr_name = "SimpleLink"
   };

   /* The underlying socket is "dispatched" to a particular network interface
    * (offloaded or not).
    */
   setsockopt(sock, SOL_SOCKET, SO_BINDTODEVICE, &ifreq, sizeof(ifreq));

In case no ``SO_BINDTODEVICE`` socket option is used on a socket, the socket
will be dispatched according to the default priority and filtering rules on a
first socket API call.

API Reference
*************

BSD Sockets
===========

.. doxygengroup:: bsd_sockets

TLS Credentials
===============

.. doxygengroup:: tls_credentials
