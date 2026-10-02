.. _socket_service_interface:

套接字服务
###############

.. contents::
    :local:
    :depth: 2

概述
********

套接字服务 API 可用于安装一个处理程序，当套接字上收到数据时会被调用。该 API 有助于避免为应用程序提供的每个 TCP 或 UDP 服务创建专用线程。相反，创建一个线程来为多个监听套接字提供数据服务，从而节省内存，因为在这种情况下系统中只需要创建一个线程。

参见 :zephyr:code-sample:`sockets-service-echo` 示例应用，了解
如何使用套接字服务 API 创建一个简单的基于 BSD 套接字的服务器应用。
该示例应用的源代码可在以下位置找到：
:zephyr_file:`samples/net/sockets/echo_service`。

API 说明
***************

套接字服务 API 通过 :kconfig:option:`CONFIG_NET_SOCKETS_SERVICE`
配置选项启用，并实现以下操作：

* :c:macro:`NET_SOCKET_SERVICE_SYNC_DEFINE`

  定义一个网络套接字服务。该套接字服务以 extern
  作用域创建，因此可以从多个 C 源文件中使用。

* :c:macro:`NET_SOCKET_SERVICE_SYNC_DEFINE_STATIC`

  定义一个静态作用域的网络套接字服务。该套接字服务只能
  在一个 C 源文件内使用。

* :c:func:`net_socket_service_register`

  为该服务注册可轮询的套接字。用户必须
  在此调用之前创建套接字。

* :c:func:`net_socket_service_unregister`

  移除该服务的可轮询套接字。用户可以在
  此调用之后关闭套接字。

* :c:type:`net_socket_service_handler_t`

  用户指定的回调，当监听套接字上收到数据时
  会被调用。

应用说明
********************

如果启用了套接字服务 API，应用程序必须像
这样创建服务：

.. code-block:: c

   #define MAX_BUF_LEN 1500
   #define MAX_SERVICES 1

   static void udp_service_handler(struct net_socket_service_event *pev)
   {
   	struct pollfd *pfd = &pev->event;
   	int client = pfd->fd;
   	struct sockaddr_in6 addr;
   	socklen_t addrlen = sizeof(addr);

   	/* 本示例中我们使用一个静态缓冲区，以避免
   	 * 过大的栈。
   	 */
   	static char buf[MAX_BUF_LEN];

   	len = recvfrom(client, buf, sizeof(buf), 0,
   		       (struct sockaddr *)&addr, &addrlen);
   	if (len <= 0) {
   		/* 错误 */
   		...
   		return;
   	}

   	/* 对接收到的数据做处理。pev 变量包含
   	 * 注册套接字服务时存储在该套接字服务中的
   	 * 用户数据。
   	 */
   }

   NET_SOCKET_SERVICE_SYNC_DEFINE_STATIC(service_udp, udp_service_handler, MAX_SERVICES);

应用程序需要创建套接字，然后将它们注册到套接字
服务，之后套接字服务线程将开始为任何传入数据
调用回调。

.. code-block:: c

   /* 创建一个或多个套接字 */

   struct pollfd sockfd_udp[1] = { 0 };
   int sock, ret;

   sock = socket(AF_INET6, SOCK_DGRAM, IPPROTO_UDP);
   if (sock < 0) {
   	LOG_ERR("socket: %d", -errno);
   	return -errno;
   }

   /* 创建后设置可能的套接字选项 */
   ...

   /* 然后将套接字绑定到本地地址 */
   if (bind(sock, (struct sockaddr *)addr, sizeof(*addr)) < 0) {
   	LOG_ERR("bind: %d", -errno);
   	return -errno;
   }

   /* 设置被轮询的套接字 */
   sockfd_udp[0].fd = sock;
   sockfd_udp[0].events = POLLIN;

   /* 将 UDP 套接字注册到服务处理程序 */
   ret = net_socket_service_register(&service_udp, sockfd_udp,
   				     ARRAY_SIZE(sockfd_udp), NULL);
   if (ret < 0) {
   	LOG_ERR("Cannot register socket service handler (%d)", ret);
   	return ret;
   }

   /* 应用逻辑在此处。当应用准备
    * 退出时，应注销套接字服务并关闭
    * 套接字。
    */

   (void)net_socket_service_unregister(&service_udp);
   close(sock);

TCP 套接字需要略有不同的逻辑，因为我们需要通过调用
:c:func:`net_socket_service_register` 将任何
已接受的套接字添加到监听套接字。

.. code-block:: c

   struct sockaddr_in6 client_addr;
   socklen_t client_addr_len = sizeof(client_addr);
   struct pollfd sockfd_tcp[1] = { 0 };
   int client;

   /* TCP 套接字服务的创建方式与 UDP 类似 */
   sock = socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP);
   if (sock < 0) {
   	LOG_ERR("socket: %d", -errno);
   	return -errno;
   }

   if (bind(sock, (struct sockaddr *)addr, sizeof(*addr)) < 0) {
   	LOG_ERR("bind: %d", -errno);
   	return -errno;
   }

   if (listen(sock, 5) < 0) {
   	LOG_ERR("listen: %d", -errno);
   	return -errno;
   }

   while (1) {
   	client = accept(tcp_sock, (struct sockaddr *)&client_addr,
   			&client_addr_len);
   	if (client < 0) {
   		LOG_ERR("accept: %d", -errno);
   		continue;
   	}

   	inet_ntop(client_addr.sin6_family, &client_addr.sin6_addr,
   		  addr_str, sizeof(addr_str));
   	LOG_INF("Connection from %s (%d)", addr_str, client);

   	sockfd_tcp[0].fd = client;
   	sockfd_tcp[0].events = POLLIN;

   	/* 将所有套接字注册到服务处理程序 */
   	ret = net_socket_service_register(&service_tcp, sockfd_tcp,
   					  ARRAY_SIZE(sockfd_tcp), NULL);
   	if (ret < 0) {
   		LOG_ERR("Cannot register socket service handler (%d)", ret);
   		break;
   	}
   }

对于任何已关闭的 TCP 客户端连接，我们需要将已关闭的
套接字从被轮询的套接字列表中移除。

.. code-block:: c

   /* 如果在处理程序中读取数据时 TCP 套接字被关闭，
    * 将其标记为不可轮询。
    */
   if (sockfd_tcp[0].fd == client) {
   	sockfd_tcp[0].fd = -1;

   	/* 更新处理程序，使客户端连接
   	 * 不再被监控。
   	 */
   	 (void)net_socket_service_register(&service_tcp, sockfd_tcp,
   					   ARRAY_SIZE(sockfd_tcp), NULL);
   	 close(client);

   	 LOG_INF("Connection from %s closed", addr_str);
   }

更完整的示例请参见 ``echo_service`` 示例源代码中的
:zephyr_file:`samples/net/sockets/echo_service/src/main.c`。

API 参考
*************

.. doxygengroup:: bsd_socket_service
