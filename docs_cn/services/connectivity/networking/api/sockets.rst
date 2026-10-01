.. _bsd_sockets_interface:

BSD Sockets
###########

.. contents::
    :local:
    :depth: 2

Overview
********

Zephyr 提供 BSD Sockets API（POSIX standard 的一部分）子集的实现。此 API 允许复用现有 programming experience（并将现有简单 networking applications 移植到 Zephyr。

以下是指导 Zephyr BSD Sockets 兼容 API 实现的关键 requirements 和 concepts：

* 开销最小（与其他 Zephyr subsystems 的要求类似。
* 默认 namespaced（以避免与知名 names（如 ``close()``）的 name conflicts（其可能是 libc 或其他 POSIX compatibility libraries 的一部分。若由 :kconfig:option:`CONFIG_POSIX_API` 启用（还将暴露 POSIX 兼容 APIs。

BSD Sockets 兼容 API 用 :kconfig:option:`CONFIG_NET_SOCKETS` config option 启用（并实现以下 operations：``socket()``、``close()``、``recv()``、``recvfrom()``、``send()``、``sendto()``、``connect()``、``bind()``、``listen()``、``accept()``、``fcntl()``（设置 non-blocking mode）、``getsockopt()``、``setsockopt()``、``poll()``、``select()``、``getaddrinfo()``、``getnameinfo()``。

基于上述 namespacing requirements（这些 operations 默认暴露为带 ``zsock_`` prefix 的 functions（如 :c:func:`zsock_socket` 和 :c:func:`zsock_close`。若定义 config option :kconfig:option:`CONFIG_POSIX_API`（所有 functions 还将暴露为无 prefix 的 aliases。这包括 ``close()`` 和 ``fcntl()`` 等 functions（其可能与 libc 或其他库中的 functions（例如 filesystem libraries）冲突。

上述 design requirements 的另一推论为 Zephyr API 尽可能积极采用 POSIX API 的 short-read/short-write property（以最小化复杂性和开销）。POSIX 允许 ``recv()`` 和 ``send()`` 等 calls 实际处理（接收或发送）少于 user 请求的 data（对 ``SOCK_STREAM`` 类型 sockets）。例如（调用 ``recv(sock, 1000, 0)`` 可能返回 100（意味着仅读取 100 bytes（short read）（且 application 需重试 call(s) 以接收剩余 900 bytes。

BSD Sockets API 用 file descriptors 表示 sockets。File descriptors 为小 integers（从零连续分配（在 sockets、files、special devices（如 stdin/stdout）等之间共享。内部有将 file descriptors 映射到 internal object pointers 的 table。即使 POSIX subsystem 其余部分（filesystem、stdin/stdout）未启用（file descriptor table 也由 BSD Sockets API 使用。

Zephyr 支持多种类型的 BSD sockets（以下 table 总结可用的 socket types：

+--------------+-------------+------------------+---------------------------------------------------------------------------+
| Family       | Type        | Protocol         | Description                                                               |
+==============+=============+==================+===========================================================================+
| AF_INET |br| | SOCK_DGRAM  | IPPROTO_UDP      | 若设置 :kconfig:option:`CONFIG_NET_UDP` 则启用。|br|                  |
| AF_INET6     |             |                  | 允许发送和接收 UDP datagrams。                                 |
|              |             +------------------+---------------------------------------------------------------------------+
|              |             | IPPROTO_DTLS_1_x | 若设置 :kconfig:option:`CONFIG_NET_SOCKETS_ENABLE_DTLS` 则启用。|br|  |
|              |             |                  | 允许发送和接收 DTLS datagrams。                                |
|              +-------------+------------------+---------------------------------------------------------------------------+
|              | SOCK_STREAM | IPPROTO_TCP      | 若设置 :kconfig:option:`CONFIG_NET_TCP` 则启用。|br|                  |
|              |             |                  | 允许发送和接收 TCP data stream。                               |
|              |             +------------------+---------------------------------------------------------------------------+
|              |             | IPPROTO_TLS_1_x  | 若设置 :kconfig:option:`CONFIG_NET_SOCKETS_SOCKOPT_TLS` 则启用。|br|  |
|              |             |                  | 允许发送和接收 TLS data stream。                               |
|              +-------------+------------------+---------------------------------------------------------------------------+
|              | SOCK_RAW    | IPPROTO_IP |br|  | 若设置 :kconfig:option:`CONFIG_NET_SOCKETS_INET_RAW` 则启用。|br|     |
|              |             | <proto>          | 允许发送和接收 IPv4/IPv6 datagrams。|br|                      |
|              |             |                  | Packets 由指定的 L4 protocol 过滤。                            |
|              |             |                  | IPPROTO_IP 为接收所有 IP datagrams 的 wildcard protocol。            |
+--------------+-------------+------------------+---------------------------------------------------------------------------+
| AF_PACKET    | SOCK_DGRAM  | ETH_P_ALL |br|   | 若设置 :kconfig:option:`CONFIG_NET_SOCKETS_PACKET_DGRAM` 则启用。|br| |
|              |             | <proto>          | 允许发送和接收无 L2 header 的 packets。|br|                |
|              |             |                  | Packets 由指定的 L3 protocol 过滤。                            |
|              |             |                  | ETH_P_ALL 为接收所有 packets 的 wildcard protocol。                  |
|              +-------------+------------------+---------------------------------------------------------------------------+
|              | SOCK_RAW    | ETH_P_ALL        | 若设置 :kconfig:option:`CONFIG_NET_SOCKETS_PACKET` 则启用。|br|       |
|              |             |                  | 允许发送和接收含 L2 header 的 packets。               |
+--------------+-------------+------------------+---------------------------------------------------------------------------+
| AF_CAN       | SOCK_RAW    | CAN_RAW          | 若设置 :kconfig:option:`CONFIG_NET_SOCKETS_CAN` 则启用。|br|          |
|              |             |                  | 允许发送和接收 CAN packets。                                   |
+--------------+-------------+------------------+---------------------------------------------------------------------------+

学习如何创建简单 server 或 client BSD socket based application 参见 :zephyr:code-sample:`sockets-echo-server` 和 :zephyr:code-sample:`sockets-echo-client` sample applications。

.. _ip_socket_options:

IPv4 and IPv6 socket options
****************************

Zephyr 通过 :c:func:`zsock_setsockopt` 和 :c:func:`zsock_getsockopt` 在 ``NET_IPPROTO_IP``（IPv4）和 ``NET_IPPROTO_IPV6``（IPv6）protocol 层支持 IP-level socket options。Option 可用性可能取决于 Kconfig 设置和 socket address family。

IPv4 options
============

.. doxygengroup:: ipv4_socket_options

IPv6 options
============

.. doxygengroup:: ipv6_socket_options

:c:macro:`ZSOCK_IP_DONTFRAG` 和 :c:macro:`ZSOCK_IPV6_DONTFRAG` options 由 QUIC stack 在 DPLPMTUD probing 期间内部使用（参见 :ref:`quic_dplpmtud`）。

.. _secure_sockets_interface:

Secure Sockets
**************

Zephyr 提供 standard POSIX socket API 的扩展（允许创建和配置带 TLS protocol types 的 sockets（促进 secure 通信。实现的 secure functions 由 Mbed TLS library 提供。Secure sockets 实现允许用 standard socket calls 使用 TLS 和 DTLS 两种 protocols。支持的 secure protocol versions 参见 :c:enum:`net_ip_protocol_secure` type。

要启用 secure sockets（设置 :kconfig:option:`CONFIG_NET_SOCKETS_SOCKOPT_TLS` option。要启用 DTLS 支持（用 :kconfig:option:`CONFIG_NET_SOCKETS_ENABLE_DTLS` option。

.. _sockets_tls_credentials_subsys:

TLS credentials subsystem
=========================

TLS credentials 须在使用 secure sockets 前在系统中注册。更多信息参见 :c:func:`tls_credential_add`。

当特定 TLS credential 在系统中注册时（其被分配 :c:type:`sec_tag_t` 类型的数值（称为 tag。此值之后可在 secure socket configuration 中用 socket options 引用 credential。

以下 TLS credential types 可在系统中注册：

- ``TLS_CREDENTIAL_CA_CERTIFICATE``
- ``TLS_CREDENTIAL_PUBLIC_CERTIFICATE``
- ``TLS_CREDENTIAL_PRIVATE_KEY``
- ``TLS_CREDENTIAL_PSK``
- ``TLS_CREDENTIAL_PSK_ID``

CA certificate（在 ``ca_certificate`` array 中提供）的注册示例如下：

.. code-block:: c

   ret = tls_credential_add(CA_CERTIFICATE_TAG, TLS_CREDENTIAL_CA_CERTIFICATE,
                            ca_certificate, sizeof(ca_certificate));

默认支持 DER 格式的 certificates。PEM 支持可在 Mbed TLS 设置中启用。

Secure Socket Creation
======================

可通过指定 secure protocol type 创建 secure socket（例如：

.. code-block:: c

   sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TLS_1_2);

创建 secure socket 时指定的 protocol version 指示 TLS session 使用的最低 TLS version。

创建后（可用 socket options 配置。例如（可设置 CA certificate 和 hostname：

.. code-block:: c

   sec_tag_t sec_tag_opt[] = {
           CA_CERTIFICATE_TAG,
   };

   ret = setsockopt(sock, SOL_TLS, TLS_SEC_TAG_LIST,
                    sec_tag_opt, sizeof(sec_tag_opt));

.. code-block:: c

   char host[] = "google.com";

   ret = setsockopt(sock, SOL_TLS, TLS_HOSTNAME, host, sizeof(host));

配置后（socket 可像普通 TCP socket 一样使用。

.. note::

   由于 mbed TLS 内部 data buffering 和 ``mbedtls_ssl_write()`` function 要求（当 non-blocking :c:func:`zsock_send` 返回 ``EAGAIN`` 时（预期对 :c:func:`zsock_send` 的连续调用包含与原始调用相同的 data。

Zephyr 中若干 samples 用 secure sockets 通信。sample 使用例如参见 :zephyr:code-sample:`echo-server sample application <sockets-echo-server>` 或 :zephyr:code-sample:`HTTP GET sample application <sockets-http-get>`。

Secure Sockets options
======================

Secure sockets 为 socket management 提供以下 options：

.. doxygengroup:: secure_sockets_options

Socket offloading
*****************

Zephyr 允许注册 custom socket implementations（称为 offloaded sockets）。这允许无缝集成提供外部 IP stack（并暴露 socket-like API 的 devices。

Socket offloading 可用 :kconfig:option:`CONFIG_NET_SOCKETS_OFFLOAD` option 启用。想注册新 socket implementation 的 network driver 应使用 :c:macro:`NET_SOCKET_OFFLOAD_REGISTER` macro。Macro 接受以下 parameters：

 * ``socket_name``
     Socket implementation 的任意 name。

 * ``prio``
     Socket implementation 的 priority。Priority 越高（创建新 socket 时此特定 implementation 越早被处理。数值越小表示 priority 越高。

 * ``_family``
     Offloaded socket 实现的 socket family。``AF_UNSPEC`` 指示任何 family。

 * ``_is_supported``
     过滤 function（用于验证特定 socket family、type 和 protocol 是否由 offloaded socket implementation 支持。

 * ``_handler``
     与 :c:func:`socket` API 兼容的 function（用于创建 offloaded socket。

每个 offloaded socket implementation 还应实现 :c:struct:`socket_op_vtable` struct 中指定的 socket APIs 集。

为 socket 创建注册的 function 应用 :c:func:`zvfs_reserve_fd` function 分配新 file descriptor。特定于特定 offloaded socket implementation 创建的任何额外 actions 应在 file descriptor 分配后执行。最后（若 offloaded socket 成功创建（file descriptor 应用 :c:func:`zvfs_finalize_typed_fd` 或 :c:func:`zvfs_finalize_fd` functions 完成。Finalize function 允许为 offloaded socket 注册实现 socket APIs 的 :c:struct:`socket_op_vtable` structure（以及可选的 socket context data pointer。

最后（当 offloaded network interface 初始化时（其应用 :c:func:`net_if_socket_offload_set` function 指示 interface 为 offloaded。Function 在 network interface 上注册用于创建 offloaded socket 的 function（与 :c:macro:`NET_SOCKET_OFFLOAD_REGISTER` 中提供的相同）。

Offloaded socket creation
=========================

当 application 用 :c:func:`socket` function 创建新 socket 时（network stack 遍历所有注册的 socket implementations（native 和 offloaded）。高 priority socket implementations 先处理。对每个注册的 socket implementation（验证 address family（若匹配（或 socket 注册为 ``AF_UNSPEC``）（调用对应 ``_is_supported`` function 验证剩余 socket parameters。第一个满足 socket requirements（即 ``_is_supported`` 返回 true）的 implementation 用其 ``_handler`` function 创建新 socket。

上述表明 socket priority 的重要性。若多个 socket implementations 支持相同 socket family/type/protocol 集（系统处理的第一个 implementation 将创建 socket。因此（应为应作为系统默认的 implementation 赋予最高 priority 很重要。

Native socket implementation 的 socket priority 用 Kconfig 配置。用 :kconfig:option:`CONFIG_NET_SOCKETS_TLS_PRIORITY` 设置 native TLS sockets 的 priority。用 :kconfig:option:`CONFIG_NET_SOCKETS_PRIORITY_DEFAULT` 设置其余 native sockets 的 priority。

Dealing with multiple offloaded interfaces
==========================================

由于 :c:func:`socket` function 不允许指定 socket 应使用哪个 network interface（多个支持相同类型 sockets 的 offloaded socket implementations 可用时无法选择特定 implementation。系统中 native 和 offloaded sockets 均可用时出现相同问题。

为解决此问题（引入特殊 socket implementation（称为 socket dispatcher。此模块的唯一目的为推迟 socket 创建直到对 socket 执行第一个 operation。这为使用 ``SO_BINDTODEVICE`` socket option 留出空间（将 socket 绑定到特定 network interface（从而 offloaded socket implementation）。Socket dispatcher 可用 :kconfig:option:`CONFIG_NET_SOCKETS_OFFLOAD_DISPATCHER` Kconfig option 启用。

启用后（application 可用 :c:func:`setsockopt` function 指定要使用的 network interface：

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

类似地（若 native 和 offloaded sockets 均支持 TLS（可用 ``TLS_NATIVE`` socket option 指示应创建 native TLS socket。底层 socket 然后可绑定到特定 network interface：

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

若 socket 上未使用 ``SO_BINDTODEVICE`` socket option（socket 将在第一个 socket API call 时按默认 priority 和 filtering rules 调度。

API Reference
*************

BSD Sockets
===========

.. doxygengroup:: bsd_sockets

TLS Credentials
===============

.. doxygengroup:: tls_credentials
