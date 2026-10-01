.. _socket_service_interface:

Socket Services
###############

.. contents::
    :local:
    :depth: 2

Overview
********

Socket service API 可用于安装在 socket 上收到 data 时调用的 handler。API 帮助避免为 application 提供的每个 TCP 或 UDP service 创建专用 thread。相反（创建一个 thread 服务多个 listening sockets（节省 memory（因为此情况下系统中仅需创建一个 thread。

学习如何用 sockets service API 创建简单 BSD socket based server application 参见 :zephyr:code-sample:`sockets-service-echo` sample application。此 sample application 的源代码可在 :zephyr_file:`samples/net/sockets/echo_service` 找到。

API Description
***************

Socket service API 用 :kconfig:option:`CONFIG_NET_SOCKETS_SERVICE` config option 启用（并实现以下 operations：

* :c:macro:`NET_SOCKET_SERVICE_SYNC_DEFINE`

  定义 network socket service。此 socket service 以 extern scope 创建（故可从多个 C source files 使用。

* :c:macro:`NET_SOCKET_SERVICE_SYNC_DEFINE_STATIC`

  定义 static scope 的 network socket service。此 socket service 仅可在一个 C source file 中使用。

* :c:func:`net_socket_service_register`

  为此 service 注册 pollable sockets。User 须在此调用前创建 sockets。

* :c:func:`net_socket_service_unregister`

  移除此 service 的 pollable sockets。User 可在此调用后关闭 sockets。

* :c:type:`net_socket_service_handler_t`

  User 指定的 callback（在 listening socket 上收到 data 时调用。

Application Overview
********************

若启用 socket service API（application 须如下创建 service：

.. code-block:: c

   #define MAX_BUF_LEN 1500
   #define MAX_SERVICES 1

   static void udp_service_handler(struct net_socket_service_event *pev)
   {
	struct pollfd *pfd = &pev->event;
	int client = pfd->fd;
	struct sockaddr_in6 addr;
	socklen_t addrlen = sizeof(addr);

	/* In this example we use one static buffer in order to avoid
	 * having a large stack.
	 */
	static char buf[MAX_BUF_LEN];

	len = recvfrom(client, buf, sizeof(buf), 0,
		       (struct sockaddr *)&addr, &addrlen);
	if (len <= 0) {
		/* Error */
		...
		return;
	}

	/* Do something with the received data. The pev variable contains
	 * user data that was stored in the socket service when it was
	 * registered.
	 */
   }

   NET_SOCKET_SERVICE_SYNC_DEFINE_STATIC(service_udp, udp_service_handler, MAX_SERVICES);

Application 需创建 sockets（然后将其注册到 socket service（之后 socket service thread 将开始对任何 incoming data 调用 callback。

.. code-block:: c

   /* Create one or multiple sockets */

   struct pollfd sockfd_udp[1] = { 0 };
   int sock, ret;

   sock = socket(AF_INET6, SOCK_DGRAM, IPPROTO_UDP);
   if (sock < 0) {
	LOG_ERR("socket: %d", -errno);
	return -errno;
   }

   /* Set possible socket options after creation */
   ...

   /* Then bind the socket to local address */
   if (bind(sock, (struct sockaddr *)addr, sizeof(*addr)) < 0) {
	LOG_ERR("bind: %d", -errno);
	return -errno;
   }

   /* Set the polled sockets */
   sockfd_udp[0].fd = sock;
   sockfd_udp[0].events = POLLIN;

   /* Register UDP socket to service handler */
   ret = net_socket_service_register(&service_udp, sockfd_udp,
				     ARRAY_SIZE(sockfd_udp), NULL);
   if (ret < 0) {
	LOG_ERR("Cannot register socket service handler (%d)", ret);
	return ret;
   }

   /* Application logic happens here. When application is ready to
    * quit, one should unregister the socket service and close the
    * socket.
    */

   (void)net_socket_service_unregister(&service_udp);
   close(sock);

TCP socket 需略不同的 logic（因为须通过为 accepted socket 调用 :c:func:`net_socket_service_register` 将任何 accepted socket 添加到 listening socket。

.. code-block:: c

   struct sockaddr_in6 client_addr;
   socklen_t client_addr_len = sizeof(client_addr);
   struct pollfd sockfd_tcp[1] = { 0 };
   int client;

   /* TCP socket service is created similar way as the UDP one */
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

	/* Register all the sockets to service handler */
	ret = net_socket_service_register(&service_tcp, sockfd_tcp,
					  ARRAY_SIZE(sockfd_tcp), NULL);
	if (ret < 0) {
		LOG_ERR("Cannot register socket service handler (%d)", ret);
		break;
	}
   }

对任何关闭的 TCP client connection（须从 polled socket list 移除关闭的 socket。

.. code-block:: c

   /* If the TCP socket is closed while reading the data in the handler,
    * mark it as non pollable.
    */
   if (sockfd_tcp[0].fd == client) {
	sockfd_tcp[0].fd = -1;

	/* Update the handler so that client connection is
	 * not monitored any more.
	 */
	 (void)net_socket_service_register(&service_tcp, sockfd_tcp,
					   ARRAY_SIZE(sockfd_tcp), NULL);
	 close(client);

	 Log_INF("Connection from %s closed", addr_str);
   }

更完整的示例参见 :zephyr_file:`samples/net/sockets/echo_service/src/main.c` 中 ``echo_service`` sample 源代码。

API Reference
*************

.. doxygengroup:: bsd_socket_service
