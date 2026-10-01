.. _mqtt_socket_interface:

MQTT
####

.. contents::
    :local:
    :depth: 2

Overview
********

MQTT（Message Queuing Telemetry Transport）是运行于 TCP/IP stack 之上的 application layer protocol。其为 machine-to-machine 通信的轻量级 publish/subscribe messaging transport。协议本身更多信息参见 https://mqtt.org/。

Zephyr 提供构建于 BSD sockets API 之上的 MQTT client library。Library 可用 :kconfig:option:`CONFIG_MQTT_LIB` Kconfig option 启用（且可按 per-client 配置（支持 MQTT versions 3.1.0、3.1.1 和 5.0。Zephyr MQTT 实现可用于通过 TCP 通信的 plain sockets（或通过 TLS 通信的 secure sockets。Zephyr sockets 更多信息参见 :ref:`bsd_sockets_interface`。

MQTT clients 需要连接 MQTT server。此类 server 称为 MQTT Broker（负责管理 client subscriptions（并分发 clients 发布的 messages。有许多 MQTT brokers 实现（其中之一为 Eclipse Mosquitto。Eclipse Mosquitto project 更多信息参见 https://mosquitto.org/。

Sample usage
************

要创建 MQTT client（须定义 client context structure 和 buffers：

.. code-block:: c

   /* Buffers for MQTT client. */
   static uint8_t rx_buffer[256];
   static uint8_t tx_buffer[256];

   /* MQTT client context */
   static struct mqtt_client client_ctx;

Application 中可创建多个 MQTT client instances（并独立管理。此外（还需要 MQTT Broker address information 的 structure。此 structure 须在 MQTT client 的整个 lifespan 中可访问（且可在 MQTT clients 之间共享：

.. code-block:: c

   /* MQTT Broker address information. */
   static struct net_sockaddr_storage broker;

MQTT client library 通过为处理相应 events 创建的 callback function 向 application 通知 MQTT events：

.. code-block:: c

   void mqtt_evt_handler(struct mqtt_client *client,
                         const struct mqtt_evt *evt)
   {
      switch (evt->type) {
         /* Handle events here. */
      }
   }

可能 events 的列表参见 :ref:`mqtt_api_reference`。

Client context structure 须在使用前初始化并设置。TCP transport 的示例 configuration 如下：

.. code-block:: c

   mqtt_client_init(&client_ctx);

   /* MQTT client configuration */
   client_ctx.broker = &broker;
   client_ctx.evt_cb = mqtt_evt_handler;
   client_ctx.client_id.utf8 = (uint8_t *)"zephyr_mqtt_client";
   client_ctx.client_id.size = sizeof("zephyr_mqtt_client") - 1;
   client_ctx.password = NULL;
   client_ctx.user_name = NULL;
   client_ctx.protocol_version = MQTT_VERSION_3_1_1;
   client_ctx.transport.type = MQTT_TRANSPORT_NON_SECURE;

   /* MQTT buffers configuration */
   client_ctx.rx_buf = rx_buffer;
   client_ctx.rx_buf_size = sizeof(rx_buffer);
   client_ctx.tx_buf = tx_buffer;
   client_ctx.tx_buf_size = sizeof(tx_buffer);

Configuration 设置后（MQTT client 可连接 MQTT broker。调用 ``mqtt_connect`` function（其创建适当的 socket（建立 TCP/TLS connection（并发送 ``MQTT CONNECT`` message。被通知时（application 应调用 ``mqtt_input`` function 以处理收到的 response。注意 ``mqtt_input`` 为非阻塞 function（因此 application 应使用 socket ``poll`` 等待 response。若 connection 成功（``MQTT_EVT_CONNACK`` 通过 callback function 通知 application。

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

上述代码片段中（MQTT callback function 应在成功连接时设置 ``connected`` flag。若 connection 在 MQTT 层失败或发生 timeout（connection 被中止（且底层 socket 关闭。

Connection 建立后（application 需周期性调用 ``mqtt_input`` 和 ``mqtt_live`` functions 以处理 incoming data（并维护 connection。若收到 MQTT message（MQTT callback function 被调用（并通知适当 event。

Connection 可调用 ``mqtt_disconnect`` function 关闭。

Zephyr 提供利用 MQTT client API 的 sample code。更多信息参见 :zephyr:code-sample:`mqtt-publisher`。

Using MQTT with TLS
*******************

Zephyr MQTT library 可通过选择 secure transport type（``MQTT_TRANSPORT_SECURE``）和一些额外 configuration information 用于 TLS transport 以进行安全通信：

.. code-block:: c

   client_ctx.transport.type = MQTT_TRANSPORT_SECURE;

   struct mqtt_sec_config *tls_config = &client_ctx.transport.tls.config;

   tls_config->peer_verify = TLS_PEER_VERIFY_REQUIRED;
   tls_config->cipher_list = NULL;
   tls_config->sec_tag_list = m_sec_tags;
   tls_config->sec_tag_count = ARRAY_SIZE(m_sec_tags);
   tls_config->hostname = MQTT_BROKER_HOSTNAME;
   tls_config->set_native_tls = true;

此 sample code 中（``m_sec_tags`` array 持有 tags 列表（引用 MQTT library 应用于 authentication 的 TLS credentials。不指定 ``cipher_list``（以允许使用系统中可用的所有 cipher suites。将 ``hostname`` field 设为 broker hostname（其是 server authentication 所必需的。最后（通过设置 ``peer_verify`` field 强制 peer certificate 验证。

注意 ``m_sec_tags`` array 引用的 TLS credentials 须先在系统中注册。如何做的更多信息参见 :ref:`secure sockets documentation <secure_sockets_interface>`。

最后（``set_native_tls`` 可选设置以启用 native TLS 支持（而非将 TLS operations 卸载到 offloaded socket。

如何使用 TLS 与 MQTT 的示例也在 :zephyr:code-sample:`mqtt-publisher` sample application 中。

.. _mqtt_api_reference:

API Reference
*************

.. doxygengroup:: mqtt_socket
