.. _bsd_sockets_interface:

BSD Sockets
###########

.. contents::
    :local:
    :depth: 2

概述
********

Zephyr 提供了 BSD Sockets API（POSIX 标准的一部分）子集的实现。该 API 允许复用现有的编程经验，并将现有的简单网络应用程序移植到 Zephyr。

以下是指导 Zephyr 实现 BSD Sockets 兼容 API 的关键需求和概念：

* 开销最小，与其他
  Zephyr 子系统的要求类似。
* 默认使用命名空间，以避免与 ``close()`` 等
  可能属于 libc 或其他 POSIX
  兼容库的知名名称发生冲突。
  如果通过 :kconfig:option:`CONFIG_POSIX_API` 启用，还会
  暴露 POSIX 兼容 API。

BSD Sockets 兼容 API 通过 :kconfig:option:`CONFIG_NET_SOCKETS`
配置选项启用，并实现以下操作：``socket()``、``close()``、
``recv()``、``recvfrom()``、``send()``、``sendto()``、``connect()``、``bind()``、
``listen()``、``accept()``、``fcntl()``（用于设置非阻塞模式）、
``getsockopt()``、``setsockopt()``、``poll()``、``select()``、
``getaddrinfo()``、``getnameinfo()``。

基于上述命名空间要求，这些操作默认
以带 ``zsock_`` 前缀的函数形式暴露，例如
:c:func:`zsock_socket` 和 :c:func:`zsock_close`。如果定义了配置选项
:kconfig:option:`CONFIG_POSIX_API`，所有函数
还会同时以不带前缀的别名形式暴露。这包括
``close()`` 和 ``fcntl()`` 等函数（它们可能与
libc 或其他库中的函数发生冲突，例如与文件系统
库中的函数冲突）。

上述设计要求的另一个推论是，Zephyr
API 在尽可能的时候积极利用 POSIX API 的短读/短写特性
（以最小化复杂性和开销）。POSIX 允许
``recv()`` 和 ``send()`` 等调用实际处理（接收
或发送）的数据少于用户请求的数据量（对于 ``SOCK_STREAM`` 类型
套接字）。例如，调用 ``recv(sock, 1000, 0)`` 可能返回 100，
意味着只读取了 100 字节（短读），应用程序
需要重试调用以接收剩余的 900 字节。

BSD Sockets API 使用文件描述符来表示套接字。文件
描述符是小整数，从零开始依次分配，在
套接字、文件、特殊设备（如 stdin/stdout）等之间共享。内部
有一个将文件描述符映射到内部对象指针的表。
即使未启用其余
POSIX 子系统（文件系统、stdin/stdout），BSD Sockets API 也会使用文件描述符表。

Zephyr 支持多种类型的 BSD 套接字，下表总结了
可用的套接字类型：

+--------------+-------------+------------------+---------------------------------------------------------------------------+
| 地址族       | 类型        | 协议             | 说明                                                                       |
+==============+=============+==================+===========================================================================+
| AF_INET |br| | SOCK_DGRAM  | IPPROTO_UDP      | 若设置了 :kconfig:option:`CONFIG_NET_UDP` 则启用。 |br|                  |
| AF_INET6     |             |                  | 允许发送和接收 UDP 数据报。                                 |
|              |             +------------------+---------------------------------------------------------------------------+
|              |             | IPPROTO_DTLS_1_x | 若设置了 :kconfig:option:`CONFIG_NET_SOCKETS_ENABLE_DTLS` 则启用。 |br|  |
|              |             |                  | 允许发送和接收 DTLS 数据报。                                |
|              +-------------+------------------+---------------------------------------------------------------------------+
|              | SOCK_STREAM | IPPROTO_TCP      | 若设置了 :kconfig:option:`CONFIG_NET_TCP` 则启用。 |br|                  |
|              |             |                  | 允许发送和接收 TCP 数据流。                               |
|              |             +------------------+---------------------------------------------------------------------------+
|              |             | IPPROTO_TLS_1_x  | 若设置了 :kconfig:option:`CONFIG_NET_SOCKETS_SOCKOPT_TLS` 则启用。 |br|  |
|              |             |                  | 允许发送和接收 TLS 数据流。                               |
|              +-------------+------------------+---------------------------------------------------------------------------+
|              | SOCK_RAW    | IPPROTO_IP |br|  | 若设置了 :kconfig:option:`CONFIG_NET_SOCKETS_INET_RAW` 则启用。 |br|     |
|              |             | <proto>          | 允许发送和接收 IPv4/IPv6 数据报。 |br|                      |
|              |             |                  | 数据包按指定的 L4 协议过滤。                            |
|              |             |                  | IPPROTO_IP 是接收所有 IP 数据报的通配协议。            |
+--------------+-------------+------------------+---------------------------------------------------------------------------+
| AF_PACKET    | SOCK_DGRAM  | ETH_P_ALL |br|   | 若设置了 :kconfig:option:`CONFIG_NET_SOCKETS_PACKET_DGRAM` 则启用。 |br| |
|              |             | <proto>          | 允许发送和接收不带 L2 头的数据包。 |br|                |
|              |             |                  | 数据包按指定的 L3 协议过滤。                            |
|              |             |                  | ETH_P_ALL 是接收所有数据包通配协议。                  |
|              +-------------+------------------+---------------------------------------------------------------------------+
|              | SOCK_RAW    | ETH_P_ALL        | 若设置了 :kconfig:option:`CONFIG_NET_SOCKETS_PACKET` 则启用。 |br|       |
|              |             |                  | 允许发送和接收包含 L2 头的数据包。               |
+--------------+-------------+------------------+---------------------------------------------------------------------------+
| AF_CAN       | SOCK_RAW    | CAN_RAW          | 若设置了 :kconfig:option:`CONFIG_NET_SOCKETS_CAN` 则启用。 |br|          |
|              |             |                  | 允许发送和接收 CAN 数据包。                                   |
+--------------+-------------+------------------+---------------------------------------------------------------------------+

参见 :zephyr:code-sample:`sockets-echo-server` 和 :zephyr:code-sample:`sockets-echo-client`
示例应用，了解如何创建简单的基于 BSD 套接字的服务器或客户端
应用。

.. _ip_socket_options:

IPv4 和 IPv6 套接字选项
****************************

Zephyr 通过 :c:func:`zsock_setsockopt` 和
:c:func:`zsock_getsockopt` 在 ``NET_IPPROTO_IP``（IPv4）和 ``NET_IPPROTO_IPV6``
（IPv6）协议级别上支持 IP 层套接字选项。选项的可用性可能取决于
Kconfig 设置和套接字地址族。

IPv4 选项
============

.. doxygengroup:: ipv4_socket_options

IPv6 选项
============

.. doxygengroup:: ipv6_socket_options

:c:macro:`ZSOCK_IP_DONTFRAG` 和 :c:macro:`ZSOCK_IPV6_DONTFRAG` 选项
由 QUIC 协议栈在 DPLPMTUD 探测期间内部使用（参见 :ref:`quic_dplpmtud`）。

.. _secure_sockets_interface:

安全套接字
******************************

Zephyr 提供了标准 POSIX 套接字 API 的扩展，允许创建
并配置采用 TLS 协议类型的套接字，从而简化安全
通信。实现中的安全功能由
Mbed TLS 库提供。安全套接字实现允许在标准套接字调用中使用 TLS 和 DTLS
两种协议。支持的secure 协议版本参见 :c:enum:`net_ip_protocol_secure` 类型。

要启用安全套接字，请设置 :kconfig:option:`CONFIG_NET_SOCKETS_SOCKOPT_TLS`
选项。要启用 DTLS 支持，请使用 :kconfig:option:`CONFIG_NET_SOCKETS_ENABLE_DTLS`
选项。

.. _sockets_tls_credentials_subsys:

TLS 凭据子系统
=========================

TLS 凭据必须先注册到系统中，然后才能与
安全套接字一起使用。更多信息参见 :c:func:`tls_credential_add`。

当某个 TLS 凭据注册到系统中时，它会被分配一个
类型为 :c:type:`sec_tag_t` 的数值，称为标签（tag）。该值可以
稍后用于在通过套接字选项配置安全套接字时
引用该凭据。

以下 TLS 凭据类型可以注册到系统中：

- ``TLS_CREDENTIAL_CA_CERTIFICATE``
- ``TLS_CREDENTIAL_PUBLIC_CERTIFICATE``
- ``TLS_CREDENTIAL_PRIVATE_KEY``
- ``TLS_CREDENTIAL_PSK``
- ``TLS_CREDENTIAL_PSK_ID``

CA 证书（提供在 ``ca_certificate``
数组中）的注册示例如下：

.. code-block:: c

   ret = tls_credential_add(CA_CERTIFICATE_TAG, TLS_CREDENTIAL_CA_CERTIFICATE,
                           ca_certificate, sizeof(ca_certificate));

默认支持 DER 格式的证书。PEM 支持可以在
Mbed TLS 设置中启用。

安全套接字创建
=====================

可以通过指定安全协议类型来创建安全套接字，例如：

.. code-block:: c

   sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TLS_1_2);

创建安全套接字时指定的协议版本表示
用于 TLS 会话的最低 TLS 版本。

创建之后，可以通过套接字选项进行配置。例如，
可以设置 CA 证书和主机名：

.. code-block:: c

   sec_tag_t sec_tag_opt[] = {
           CA_CERTIFICATE_TAG,
   };

   ret = setsockopt(sock, SOL_TLS, TLS_SEC_TAG_LIST,
                    sec_tag_opt, sizeof(sec_tag_opt));

.. code-block:: c

   char host[] = "google.com";

   ret = setsockopt(sock, SOL_TLS, TLS_HOSTNAME, host, sizeof(host));

配置完成后，该套接字可以像普通 TCP 套接字一样使用。

.. note::

   由于 mbed TLS 内部数据缓冲以及 ``mbedtls_ssl_write()`` 函数
   的要求，当非阻塞 :c:func:`zsock_send` 返回 ``EAGAIN`` 时，
   预期对 :c:func:`zsock_send` 的后续调用将包含
   与原始调用相同的数据。

Zephyr 中的多个示例使用安全套接字进行通信。示例用法
参见例如 :zephyr:code-sample:`echo-server 示例应用 <sockets-echo-server>` 或
:zephyr:code-sample:`HTTP GET 示例应用 <sockets-http-get>`。

安全套接字选项
====================

安全套接字提供以下选项用于套接字管理：

.. doxygengroup:: secure_sockets_options

套接字卸载
*****************

Zephyr 允许注册自定义套接字实现（称为卸载
套接字）。这使得能够无缝集成那些提供
外部 IP 协议栈并暴露类套接字 API 的设备。

套接字卸载可以通过 :kconfig:option:`CONFIG_NET_SOCKETS_OFFLOAD`
选项启用。希望注册新套接字实现的
网络驱动应使用 :c:macro:`NET_SOCKET_OFFLOAD_REGISTER` 宏。该宏接受
以下参数：

 * ``socket_name``
     套接字实现的任意名称。

 * ``prio``
     套接字实现的优先级。优先级越高，创建新套接字时
     该特定实现就越早被处理。
     数值越小表示优先级越高。

 * ``_family``
     卸载套接字实现的套接字地址族。``AF_UNSPEC`` 表示
     任意地址族。

 * ``_is_supported``
     过滤函数，用于验证特定的套接字地址族、
     类型和协议是否受卸载套接字实现支持。

 * ``_handler``
     与 :c:func:`socket` API 兼容的函数，用于创建
     卸载套接字。

每个卸载套接字实现还应实现一组套接字
API，指定在 :c:struct:`socket_op_vtable` 结构体中。

用于创建套接字的注册函数应使用 :c:func:`zvfs_reserve_fd` 函数
分配一个新的文件
描述符。创建特定卸载套接字实现所特有的任何其他操作，
都应在文件描述符分配之后进行。最后，
如果卸载套接字创建成功，文件描述符应
通过 :c:func:`zvfs_finalize_typed_fd` 或 :c:func:`zvfs_finalize_fd`
函数完成。finalize 函数允许注册一个
实现卸载套接字套接字 API 的
:c:struct:`socket_op_vtable` 结构体，以及可选的套接字上下文数据指针。

最后，当卸载网络接口初始化时，应通过
:c:func:`net_if_socket_offload_set`
函数指示该接口是卸载的。该函数在网络接口上
注册用于创建卸载套接字的函数
（与 :c:macro:`NET_SOCKET_OFFLOAD_REGISTER` 中提供的函数相同）。

卸载套接字创建
=========================

当应用程序使用 :c:func:`socket` 函数创建新套接字时，
网络协议栈会遍历所有已注册的套接字实现（原生和
卸载）。优先级较高的套接字实现先被处理。
对于每个已注册的套接字实现，都会验证地址族，如果
匹配（或套接字注册为 ``AF_UNSPEC``），则调用相应的
``_is_supported`` 函数验证其余套接字参数。
第一个满足套接字要求的实现（即
``_is_supported`` 返回 true）将通过其 ``_handler``
函数创建新套接字。

上述说明了套接字优先级的重要性。如果多个套接字
实现支持相同的套接字地址族/类型/协议集合，系统
处理的第一个实现将创建套接字。因此，
应将最高优先级分配给应作为
系统默认的实现。

原生套接字实现的套接字优先级通过 Kconfig 配置。
使用 :kconfig:option:`CONFIG_NET_SOCKETS_TLS_PRIORITY` 设置
原生 TLS 套接字的优先级。
使用 :kconfig:option:`CONFIG_NET_SOCKETS_PRIORITY_DEFAULT` 设置
其余原生套接字的优先级。

处理多个卸载接口
==========================================

由于 :c:func:`socket` 函数不允许指定套接字
应使用哪个网络
接口，因此在存在多个支持
相同类型套接字的卸载套接字实现时，无法选择特定
的实现。当系统中同时存在原生
和卸载套接字时也会出现同样的问题。

为解决该问题，引入了一个特殊的套接字实现（称为套接字
调度器）。该模块的唯一目的是将
套接字创建推迟到对套接字执行第一个操作时。这
留下了一个口子，可以使用 ``SO_BINDTODEVICE`` 套接字选项，将套接字绑定到
特定网络接口（从而绑定到卸载套接字实现）。
套接字调度器可以通过 :kconfig:option:`CONFIG_NET_SOCKETS_OFFLOAD_DISPATCHER`
Kconfig 选项启用。

启用后，应用程序可以通过
:c:func:`setsockopt` 函数指定要使用的网络接口：

.. code-block:: c

   /* 创建一个"调度器"套接字 */
   sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

   struct ifreq ifreq = {
      .ifr_name = "SimpleLink"
   };

   /* 套接字被"调度"到特定网络接口
    *（卸载或非卸载）。
    */
   setsockopt(sock, SOL_SOCKET, SO_BINDTODEVICE, &ifreq, sizeof(ifreq));

类似地，如果 TLS 同时受原生和卸载套接字支持，
``TLS_NATIVE`` 套接字选项可用于指示应创建原生 TLS 套接字。
底层套接字随后可以绑定到特定
网络接口：

.. code-block:: c

   /* 创建一个"调度器"套接字 */
   sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TLS_1_2);

   int tls_native = 1;

   /* 套接字被"调度"到原生 TLS 套接字实现。
    * 底层套接字现在是一个"调度器"套接字。
    */
   setsockopt(sock, SOL_TLS, TLS_NATIVE, &tls_native, sizeof(tls_native));

   struct ifreq ifreq = {
      .ifr_name = "SimpleLink"
   };

   /* 底层套接字被"调度"到特定网络接口
    *（卸载或非卸载）。
    */
   setsockopt(sock, SOL_SOCKET, SO_BINDTODEVICE, &ifreq, sizeof(ifreq));

如果套接字上未使用 ``SO_BINDTODEVICE`` 套接字选项，
该套接字将在第一次套接字 API 调用时
根据默认优先级和过滤规则进行调度。

API 参考
*************

BSD Sockets
============

.. doxygengroup:: bsd_sockets

TLS 凭据
================

.. doxygengroup:: tls_credentials
