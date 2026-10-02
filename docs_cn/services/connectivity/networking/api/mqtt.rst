.. _mqtt_socket_interface:

MQTT
####

.. contents::
    :local:
    :depth: 2

概述
********

MQTT（消息队列遥测传输）是一种应用层协议，运行在 TCP/IP 协议栈之上。它是一种轻量级的发布/订阅消息传输协议，用于机器对机器通信。有关协议本身的更多信息，参见 https://mqtt.org/。

Zephyr 提供了一个基于 BSD 套接字 API 构建的 MQTT 客户端库。该库可以通过 :kconfig:option:`CONFIG_MQTT_LIB` Kconfig 选项启用，并按客户端进行配置，支持 MQTT 版本 3.1.0、3.1.1 和 5.0。Zephyr MQTT 实现可用于通过 TCP 通信的普通套接字，也可用于通过 TLS 通信的安全套接字。有关 Zephyr 套接字的更多信息，参见 :ref:`bsd_sockets_interface`。

MQTT 客户端需要一个 MQTT 服务器来连接。这样的服务器称为 MQTT 代理（Broker），负责管理客户端订阅并分发客户端发布的消息。有许多 MQTT 代理实现，其中之一是 Eclipse Mosquitto。有关 Eclipse Mosquitto 项目的更多信息，参见 https://mosquitto.org/。

使用示例
************

要创建一个 MQTT 客户端，需要定义客户端上下文结构和缓冲区：

.. code-block:: c

   /* MQTT 客户端缓冲区。 */
   static uint8_t rx_buffer[256];
   static uint8_t tx_buffer[256];

   /* MQTT 客户端上下文 */
   static struct mqtt_client client_ctx;

应用程序中可以创建多个 MQTT 客户端实例并独立管理。此外，还需要一个 MQTT 代理地址信息结构。该结构必须在 MQTT 客户端的整个生命周期中可访问，并可在 MQTT 客户端之间共享：

.. code-block:: c

   /* MQTT 代理地址信息。 */
   static struct net_sockaddr_storage broker;

MQTT 客户端库通过为处理相应事件创建的回调函数向应用程序通知 MQTT 事件：

.. code-block:: c

   void mqtt_evt_handler(struct mqtt_client *client,
                         const struct mqtt_evt *evt)
   {
      switch (evt->type) {
         /* 在此处处理事件。 */
      }
   }

有关可能事件的列表，参见 :ref:`mqtt_api_reference`。

客户端上下文结构需要在使用前进行初始化和配置。以下是 TCP 传输的示例配置：

.. code-block:: c

   mqtt_client_init(&client_ctx);

   /* MQTT 客户端配置 */
   client_ctx.broker = &broker;
   client_ctx.evt_cb = mqtt_evt_handler;
   client_ctx.client_id.utf8 = (uint8_t *)"zephyr_mqtt_client";
   client_ctx.client_id.size = sizeof("zephyr_mqtt_client") - 1;
   client_ctx.password = NULL;
   client_ctx.user_name = NULL;
   client_ctx.protocol_version = MQTT_VERSION_3_1_1;
   client_ctx.transport.type = MQTT_TRANSPORT_NON_SECURE;

   /* MQTT 缓冲区配置 */
   client_ctx.rx_buf = rx_buffer;
   client_ctx.rx_buf_size = sizeof(rx_buffer);
   client_ctx.tx_buf = tx_buffer;
   client_ctx.tx_buf_size = sizeof(tx_buffer);

配置完成后，MQTT 客户端可以连接到 MQTT 代理。调用 ``mqtt_connect`` 函数，该函数将创建适当的套接字、建立 TCP/TLS 连接并发送 ``MQTT CONNECT`` 消息。收到通知后，应用程序应调用 ``mqtt_input`` 函数处理收到的响应。注意，``mqtt_input`` 是非阻塞函数，因此应用程序应使用套接字 ``poll`` 等待响应。如果连接成功，``MQTT_EVT_CONNACK`` 将通过回调函数通知应用程序。

.. code-block:: c

   rc = mqtt_connect(&client_ctx);
   if (rc != 0) {
      return rc;
   }

   fds[0].fd = client_ctx.transport.tcp.sock;
   fds[0].events = ZSOCK_POLLIN;
   poll(fds, 1, 5000);

   mqtt_input(&client_ctx);

   if (!connected) {
      mqtt_abort(&client_ctx);
   }

在上述代码片段中，MQTT 回调函数应在成功连接时设置 ``connected`` 标志。如果连接在 MQTT 层失败或发生超时，连接将被中止，底层套接字关闭。

连接建立后，应用程序需要定期调用 ``mqtt_input`` 和 ``mqtt_live`` 函数来处理传入数据并维护连接。如果收到 MQTT 消息，将调用 MQTT 回调函数并通知相应事件。

通过调用 ``mqtt_disconnect`` 函数可以关闭连接。

Zephyr 提供了使用 MQTT 客户端 API 的示例代码。更多信息参见 :zephyr:code-sample:`mqtt-publisher`。

使用 TLS 的 MQTT
*******************

Zephyr MQTT 库可以通过选择安全传输类型（``MQTT_TRANSPORT_SECURE``）和一些额外配置信息来使用 TLS 传输进行安全通信：

.. code-block:: c

   client_ctx.transport.type = MQTT_TRANSPORT_SECURE;

   struct mqtt_sec_config *tls_config = &client_ctx.transport.tls.config;

   tls_config->peer_verify = TLS_PEER_VERIFY_REQUIRED;
   tls_config->cipher_list = NULL;
   tls_config->sec_tag_list = m_sec_tags;
   tls_config->sec_tag_count = ARRAY_SIZE(m_sec_tags);
   tls_config->hostname = MQTT_BROKER_HOSTNAME;
   tls_config->set_native_tls = true;

在此示例代码中，``m_sec_tags`` 数组持有一组标签，引用 MQTT 库应用于身份验证的 TLS 凭据。我们不指定 ``cipher_list``，以允许使用系统中可用的所有密码套件。我们将 ``hostname`` 字段设置为代理主机名，这是服务器身份验证所必需的。最后，我们通过设置 ``peer_verify`` 字段来强制对等证书验证。

注意，``m_sec_tags`` 数组引用的 TLS 凭据必须先在系统中注册。有关如何操作的更多信息，参见 :ref:`安全套接字文档 <secure_sockets_interface>`。

最后，``set_native_tls`` 可以可选地设置为启用原生 TLS 支持，而不是将 TLS 操作卸载到卸载套接字。

如何使用 TLS 与 MQTT 的示例也存在于 :zephyr:code-sample:`mqtt-publisher` 示例应用程序中。

.. _mqtt_api_reference:

API 参考
*************

.. doxygengroup:: mqtt_socket
