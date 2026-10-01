.. _websocket_interface:

Websocket Client API
####################

.. contents::
    :local:
    :depth: 2

Overview
********

Websocket client library 允许 Zephyr 连接到 Websocket server。Websocket client API 可被 application 直接使用以与 server 建立 Websocket connection（或用作 MQTT 等其他 network protocols 的 transport。

Websocket 工作原理的详细概述参见此 `Websocket Wikipedia article <https://en.wikipedia.org/wiki/WebSocket>`_。

protocol 本身更多信息参见 :rfc:`6455`。

Websocket Transport
*******************

Websocket API 允许其用作 MQTT 等其他 high level protocols 的 transport。Zephyr MQTT client library 可通过启用 :kconfig:option:`CONFIG_MQTT_LIB_WEBSOCKET` 和 :kconfig:option:`CONFIG_WEBSOCKET_CLIENT` Kconfig options 配置为使用 Websocket transport。

首先需创建 socket 并连接到 Websocket server：

.. code-block:: c

    sock = socket(family, SOCK_STREAM, IPPROTO_TCP);
    ...
    ret = connect(sock, addr, addr_len);
    ...

然后创建 Websocket transport socket（如下：

.. code-block:: c

    ws_sock = websocket_connect(sock, &config, timeout, user_data);

然后可用 Websocket socket 发送或接收 data（Websocket client API 将发送或接收的 data 封装到/从 Websocket packet payload。发送和接收 application data 均可用 :c:func:`websocket_xxx()` API 或普通 BSD socket API functions。

.. code-block:: c

    ret = websocket_send_msg(ws_sock, buf_to_send, buf_len,
                             WEBSOCKET_OPCODE_DATA_BINARY, true, true,
			     K_FOREVER);
    ...
    ret = send(ws_sock, buf_to_send, buf_len, 0);

若使用普通 BSD socket functions（当前仅支持 TEXT data。要发送 BINARY data（须使用 :c:func:`websocket_send_msg()`。

完成后（须关闭 Websocket transport socket。User 应在 websocket_disconnect 后处理 tcp socket 的 lifecycle（close/reuse）。

.. code-block:: c

    ret = close(ws_sock);
    or
    ret = websocket_disconnect(ws_sock);


API Reference
*************

.. doxygengroup:: websocket
