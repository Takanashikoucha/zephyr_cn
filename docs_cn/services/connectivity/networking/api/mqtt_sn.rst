.. _mqtt_sn_socket_interface:

MQTT-SN
#######

.. contents::
    :local:
    :depth: 2

Overview
********

MQTT-SN 为知名 MQTT protocol 的 variant - 参见 :ref:`mqtt_socket_interface`。

与 MQTT 不同（MQTT-SN 不需要 TCP transport（而是设计用于任何 message-based transport。最初其主要为 ZigBee 创建（但其他如 Bluetooth、UDP 甚至 UART 也可同样使用。

Zephyr 提供构建于 BSD sockets API 之上的 MQTT-SN client library。Library 可用 :kconfig:option:`CONFIG_MQTT_SN_LIB` Kconfig option 启用（且可按 per-client 配置（支持 MQTT-SN version 1.2。Zephyr MQTT-SN 实现可用于任何 message-based transport（但 UDP 支持已内置。

MQTT-SN clients 需要连接 MQTT-SN gateway。这些 gateways 在 MQTT-SN 和 MQTT 之间转换。Eclipse Paho project 提供 MQTT-SN gateway 的实现（但其他也可用。https://www.eclipse.org/paho/index.php?page=components/mqtt-sn-transparent-gateway/index.php

MQTT-SN spec v1.2 可在此找到：https://www.oasis-open.org/committees/download.php/66091/MQTT-SN_spec_v1.2.pdf

Sample usage
************

要创建 MQTT-SN client（须定义 client context structure 和 buffers：

.. code-block:: c

   /* Buffers for MQTT client. */
   static uint8_t rx_buffer[256];
   static uint8_t tx_buffer[256];

   /* MQTT-SN client context */
   static struct mqtt_sn_client client;

Application 中可创建多个 MQTT-SN client instances（并独立管理。此外（还需要 transport 的 structure。Library 已附带 UDP 的示例实现。

.. code-block:: c

   /* MQTT Broker address information. */
   static struct mqtt_sn_transport tp;

MQTT-SN library 用 callback 通知 clients 某些 events。

.. code-block:: c

   static void evt_cb(struct mqtt_sn_client *client,
                      const struct mqtt_sn_evt *evt)
   {
      switch(evt->type) {
      {
         /* Handle events here. */
      }
   }

可能 events 的列表参见 :ref:`mqtt_sn_api_reference`。

Client context structure 须在使用前初始化并设置。UDP transport 的示例 configuration 如下：

.. code-block:: c

   struct mqtt_sn_data client_id = MQTT_SN_DATA_STRING_LITERAL("ZEPHYR");
   struct net_sockaddr_in gateway = {0};

   uint8_t tx_buf[256];
   uint8_t rx_buf[256];

   mqtt_sn_transport_udp_init(&tp, (struct net_sockaddr*)&gateway, sizeof((gateway)));

   mqtt_sn_client_init(&client, &client_id, &tp.tp, evt_cb, tx_buf, sizeof(tx_buf), rx_buf, sizeof(rx_buf));

Configuration 设置后（须定义要连接的 gateway 的 network address。MQTT-SN protocol 提供通过 advertisement 或 search mechanism 发现 gateways 的功能。User 应至少执行以下步骤之一以定义 library 的 Gateway：

* 调用 :c:func:`mqtt_sn_add_gw` function 手动定义 Gateway address。
* 等待 :c:enumerator:`MQTT_SN_EVT_ADVERTISE`。
* 调用 :c:func:`mqtt_sn_search` function（并等待 :c:enumerator:`MQTT_SN_EVT_GWINFO` callback。确保周期性调用 :c:func:`mqtt_sn_input` function 以处理 incoming messages。

:c:func:`mqtt_sn_search` function 调用示例：

.. code-block:: c

	err = mqtt_sn_search(&mqtt_client, 1);
	k_sleep(K_SECONDS(10));
	err = mqtt_sn_input(&mqtt_client);
	__ASSERT(err == 0, "mqtt_sn_search() failed %d", err);

Gateway address 定义或找到后（MQTT-SN client 可连接 gateway。调用 :c:func:`mqtt_sn_connect` function（其发送 ``CONNECT`` MQTT-SN message。Application 应周期性调用 :c:func:`mqtt_sn_input` function 以处理收到的 response。若 application 知道未收到 data（例如使用 Bluetooth 时）（无需调用 :c:func:`mqtt_sn_input`。注意 :c:func:`mqtt_sn_input` 为非阻塞 function（若 transport struct 包含 :c:func:`poll` compatible function pointer。若 connection 成功（:c:enumerator:`MQTT_SN_EVT_CONNECTED` 通过 callback function 通知 application。

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

上述代码片段中（gateway 在 publish messages 前连接。若 connection 在 MQTT 层失败或发生 timeout（connection 被中止（并返回 error。

Connection 建立后（application 需周期性调用 :c:func:`mqtt_input` function 以处理 incoming data。另一方面（connection upkeep 用 k_work item 自动完成。若收到 MQTT message（MQTT callback function 被调用（并通知适当 event。

Connection 可调用 :c:func:`mqtt_sn_disconnect` function 关闭。但这对 transport 无影响。若要关闭 transport（例如 socket（调用 :c:func:`mqtt_sn_client_deinit`（其也 deinit transport。

Zephyr 提供利用 MQTT-SN client API 的 sample code。更多信息参见 :zephyr:code-sample:`mqtt-sn-publisher`。

Deviations from the standard
****************************

Protocol 的某些部分尚未在 library 中支持。

* Forwarder Encapsulation

.. _mqtt_sn_api_reference:

API Reference
*************

.. doxygengroup:: mqtt_sn_socket
