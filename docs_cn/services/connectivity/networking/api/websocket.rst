.. _websocket_interface:

Websocket 客户端 API
####################

.. contents::
    :local:
    :depth: 2

概述
********

Websocket 客户端库允许 Zephyr 连接到 Websocket 服务器。
Websocket 客户端 API 可以由应用直接使用，
用于与服务器建立 Websocket 连接，
也可以作为 MQTT 等其他网络协议的传输层。

有关 Websocket 工作原理的详细概述，请参阅
这篇
`Websocket Wikipedia 文章 <https://en.wikipedia.org/wiki/WebSocket>`_。

有关协议本身的更多信息，请参阅 :rfc:`6455`。

Websocket 传输
*******************

Websocket API 允许其作为 MQTT 等其他高层协议的传输层。
Zephyr MQTT 客户端库可通过启用
:kconfig:option:`CONFIG_MQTT_LIB_WEBSOCKET` 和
:kconfig:option:`CONFIG_WEBSOCKET_CLIENT` Kconfig 选项
配置为使用 Websocket 传输。

首先需要创建一个套接字并连接到 Websocket 服务器：

.. code-block:: c

    sock = socket(family, SOCK_STREAM, IPPROTO_TCP);
    ...
    ret = connect(sock, addr, addr_len);
    ...

然后按以下方式创建 Websocket 传输套接字：

.. code-block:: c

    ws_sock = websocket_connect(sock, &config, timeout, user_data);

之后可以使用 Websocket 套接字发送或接收数据，
Websocket 客户端 API 会将发送或接收的数据封装到
Websocket 数据包有效载荷中，或从中解出。
发送和接收应用数据时，既可以使用
:c:func:`websocket_xxx()` API，也可以使用常规
BSD 套接字 API 函数。

.. code-block:: c

    ret = websocket_send_msg(ws_sock, buf_to_send, buf_len,
                             WEBSOCKET_OPCODE_DATA_BINARY, true, true,
			     K_FOREVER);
    ...
    ret = send(ws_sock, buf_to_send, buf_len, 0);

如果使用常规 BSD 套接字函数，则目前仅支持
TEXT 数据。要发送 BINARY 数据，必须使用
:c:func:`websocket_send_msg()`。

完成后，必须关闭 Websocket 传输套接字。用户应在
websocket_disconnect 之后自行处理
tcp 套接字的生命周期（关闭/复用）。

.. code-block:: c

    ret = close(ws_sock);
    or
    ret = websocket_disconnect(ws_sock);


API 参考
*************

.. doxygengroup:: websocket
