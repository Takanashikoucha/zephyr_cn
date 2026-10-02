.. _mqtt_sn_socket_interface:

MQTT-SN
#######

.. contents::
    :local:
    :depth: 2

概述
********

MQTT-SN 是知名 MQTT 协议的一个变体 - 参见 :ref:`mqtt_socket_interface`。

与 MQTT 不同，MQTT-SN 不需要 TCP 传输，而是设计用于任何基于消息的传输。最初，它主要是为 ZigBee 创建的，但其他如 Bluetooth、UDP 甚至 UART 也可以同样使用。

Zephyr 提供了一个基于 BSD 套接字 API 构建的 MQTT-SN 客户端库。该库可以通过 :kconfig:option:`CONFIG_MQTT_SN_LIB` Kconfig 选项启用，并按客户端进行配置，支持 MQTT-SN 版本 1.2。Zephyr MQTT-SN 实现可用于任何基于消息的传输，但 UDP 支持已内置。

MQTT-SN 客户端需要一个 MQTT-SN 网关来连接。这些网关在 MQTT-SN 和 MQTT 之间进行转换。Eclipse Paho 项目提供了一个 MQTT-SN 网关的实现，但还有其他可用的。
https://www.eclipse.org/paho/index.php?page=components/mqtt-sn-transparent-gateway/index.php

MQTT-SN 规范 v1.2 可在此找到：
https://www.oasis-open.org/committees/download.php/66091/MQTT-SN_spec_v1.2.pdf

使用示例
************

要创建一个 MQTT-SN 客户端，需要定义客户端上下文结构和缓冲区：

.. code-block:: c

   /* MQTT 客户端缓冲区。 */
   static uint8_t rx_buffer[256];
   static uint8_t tx_buffer[256];

   /* MQTT-SN 客户端上下文 */
   static struct mqtt_sn_client client;

应用程序中可以创建多个 MQTT-SN 客户端实例并独立管理。此外，还需要一个传输结构。该库已经附带了一个 UDP 的示例实现。

.. code-block:: c

   /* MQTT 代理地址信息。 */
   static struct mqtt_sn_transport tp;

MQTT-SN 库使用回调通知客户端某些事件。

.. code-block:: c

   static void evt_cb(struct mqtt_sn_client *client,
                      const struct mqtt_sn_evt *evt)
   {
      switch(evt->type) {
      {
         /* 在此处处理事件。 */
      }
   }

有关可能事件的列表，参见 :ref:`mqtt_sn_api_reference`。

客户端上下文结构需要在使用前进行初始化和配置。以下是 UDP 传输的示例配置：

.. code-block:: c

   struct mqtt_sn_data client_id = MQTT_SN_DATA_STRING_LITERAL("ZEPHYR");
   struct net_sockaddr_in gateway = {0};

   uint8_t tx_buf[256];
   uint8_t rx_buf[256];

   mqtt_sn_transport_udp_init(&tp, (struct net_sockaddr*)&gateway, sizeof((gateway)));

   mqtt_sn_client_init(&client, &client_id, &tp.tp, evt_cb, tx_buf, sizeof(tx_buf), rx_buf, sizeof(rx_buf));

配置完成后，必须定义要连接的网关的网络地址。MQTT-SN 协议提供了通过广播或搜索机制发现网关的功能。用户应至少执行以下步骤之一来为库定义网关：

* 调用 :c:func:`mqtt_sn_add_gw` 函数手动定义网关地址。
* 等待 :c:enumerator:`MQTT_SN_EVT_ADVERTISE`。
* 调用 :c:func:`mqtt_sn_search` 函数并等待 :c:enumerator:`MQTT_SN_EVT_GWINFO` 回调。
  确保定期调用 :c:func:`mqtt_sn_input` 函数处理传入消息。

:c:func:`mqtt_sn_search` 函数调用示例：

.. code-block:: c

 	err = mqtt_sn_search(&mqtt_client, 1);
 	k_sleep(K_SECONDS(10));
 	err = mqtt_sn_input(&mqtt_client);
 	__ASSERT(err == 0, "mqtt_sn_search() failed %d", err);

网关地址定义或找到后，MQTT-SN 客户端可以连接到网关。调用 :c:func:`mqtt_sn_connect` 函数，该函数将发送 ``CONNECT`` MQTT-SN 消息。应用程序应定期调用 :c:func:`mqtt_sn_input` 函数处理收到的响应。如果应用程序知道没有收到数据（例如使用 Bluetooth 时），则无需调用 :c:func:`mqtt_sn_input`。注意，如果传输结构包含 :c:func:`poll` 兼容的函数指针，:c:func:`mqtt_sn_input` 是非阻塞函数。
如果连接成功，:c:enumerator:`MQTT_SN_EVT_CONNECTED` 将通过回调函数通知应用程序。

.. code-block:: c

 	err = mqtt_sn_connect(&client, false, true);
 	__ASSERT(err == 0, "mqtt_sn_connect() failed %d", err);

 	while (1) {
 		mqtt_sn_input(&client);
 		if (connected) {
 			mqtt_sn_publish(&client, MQTT_SN_QOS_0, &topic_p, false, &pubdata);
 		}
 		k_sleep(K_MSEC(500));
 	}

在上述代码片段中，网关在发布消息之前已连接。如果连接在 MQTT 层失败或发生超时，连接将被中止并返回错误。

连接建立后，应用程序需要定期调用 :c:func:`mqtt_input` 函数处理传入数据。另一方面，连接维护使用 k_work 项自动完成。
如果收到 MQTT 消息，将调用 MQTT 回调函数并通知相应事件。

通过调用 :c:func:`mqtt_sn_disconnect` 函数可以关闭连接。但是，这对传输没有影响。如果要关闭传输（例如套接字），调用 :c:func:`mqtt_sn_client_deinit`，该函数也会反初始化传输。

Zephyr 提供了使用 MQTT-SN 客户端 API 的示例代码。更多信息参见 :zephyr:code-sample:`mqtt-sn-publisher`。

与标准的不同
****************************

协议的某些部分尚未在库中支持。

* 转发器封装

.. _mqtt_sn_api_reference:

API 参考
*************

.. doxygengroup:: mqtt_sn_socket
