.. _coap_client_interface:

CoAP 客户端
###########

.. contents::
    :local:
    :depth: 2

概述
********

CoAP 客户端库允许应用发送 CoAP 请求并解析 CoAP 响应。
该库可通过 :kconfig:option:`CONFIG_COAP_CLIENT` Kconfig 选项启用。
应用通过请求中提供给 API 的回调获知
响应。CoAP 客户端负责处理通过套接字的通信。
由于 CoAP 客户端不创建其使用的套接字，
应用负责创建套接字。支持
普通 UDP 或 DTLS 套接字。

基于 TCP 的 CoAP
================

基于可靠传输（TCP/TLS）的 CoAP 也按 :rfc:`8323` 规范受支持。
通过 :kconfig:option:`CONFIG_COAP_CLIENT_TCP` 启用。TCP 客户端在内部
管理连接建立、CSM（Capabilities and Settings Message，能力与设置消息）交换，以及信令
（Ping/Pong、Release、Abort）。与 UDP 客户端不同，
应用不创建套接字——而是调用 :c:func:`coap_client_tcp_connect` 并传入服务器
地址。参见 :zephyr:code-sample:`coap-client-tcp` 了解使用示例。

示例用法
************

以下是 CoAP 客户端初始化和请求发送的示例：

.. code-block:: c

    static struct coap_client client;
    struct coap_client_request req = { 0 };

    coap_client_init(&client, NULL);

    req.method = COAP_METHOD_GET;
    req.confirmable = true;
    strcpy(req.path, "test");
    req.fmt = COAP_CONTENT_FORMAT_TEXT_PLAIN;
    req.cb = response_cb;
    req.payload = NULL;
    req.len = 0;

    /* Sock is a file descriptor referencing a socket, address is the net_sockaddr struct for the
     * destination address of the request or NULL if the socket is already connected.
     */
    ret = coap_client_req(&client, sock, &address, &req, -1);

在发送任何请求之前，必须先初始化 CoAP 客户端。
初始化后，应用即可发送 CoAP 请求并等待响应。
目前单个 CoAP 客户端一次只能发送一个请求。可以
存在多个 CoAP 客户端。

在以下情况下会调用请求中提供的回调：

- 存在该请求的响应
- 请求因某种原因失败

回调包含一个标志 ``last_block``，指示响应中
是否还有更多数据到来，
意味着当前响应是分块传输的一部分。当
``last_block`` 被设为 true 时，响应已完成，客户端在
从回调返回后即可处理下一个请求。

如果服务器响应了请求，库会通过请求结构
中注册的响应回调，将响应提供给
应用。由于响应可能是分块传输，且客户端
每收到一个块就调用一次回调，
应用应当能够处理所有块，才能完整处理该响应。

在分块传输期间，客户端会按 :rfc:`7959` 的要求比较
所收到各块的 ETag 选项。当资源表示
在传输中途发生变化时，
传输会被中止，回调以 ``result_code`` 设为 ``-EBADMSG`` 被调用。
比 RFC 的最低要求（仅规定比较服务器提供的 ETag）
更严格：当 ETag 选项
在块之间出现或消失时，传输同样会被中止，
因为带 ETag 与不带 ETag 的块混合在一起无法验证。应用应当
丢弃已接收的部分数据，并可以重试该请求。

以下是一个非常简单的响应处理函数示例：

.. code-block:: c

    void response_cb(const struct coap_client_response_data *data, void *user_data)
    {
        if (data->result_code >= 0) {
 	        LOG_INF("CoAP response from server %d", data->result_code);
                if (data->last_block) {
                        LOG_INF("Last packet received");
                }
        } else {
                LOG_ERR("Error in sending request %d", data->result_code);
        }
    }

应用还可以向请求中添加 CoAP 选项。以下是
应用向初始请求添加 Block2 选项的示例，
以向服务器建议一个最大块大小，
用于预期大到需要分块传输的资源（参见
:rfc:`7959` Figure 3: Block-Wise GET with Early Negotiation）。

.. code-block:: c

    static struct coap_client client;
    struct coap_client_request req = { 0 };

    coap_client_init(&client, NULL);

    req.method = COAP_METHOD_GET;
    req.confirmable = true;
    strcpy(req.path, "test");
    req.fmt = COAP_CONTENT_FORMAT_TEXT_PLAIN;
    req.cb = response_cb;
    req.options[0] = coap_client_option_initial_block2();
    req.num_options = 1;
    req.payload = NULL;
    req.len = 0;

    ret = coap_client_req(&client, sock, &address, &req, -1);

可选地，应用可以注册一个负载（payload）回调，
而不用为 CoAP 上传提供负载指针。
在这种情况下，CoAP 客户端库会在
准备 PUT/POST 请求时调用该回调，
使应用可以分块提供负载，
而无需提供一个包含整个负载的
单个连续缓冲区。一个提供
Lorem Ipsum 字符串内容的示例回调
可以如下：

.. code-block:: c

    static int lorem_ipsum_cb(size_t offset, const uint8_t **payload, size_t *len,
                              bool *last_block, void *user_data)
    {
        size_t data_left;

        if (offset > LOREM_IPSUM_STRLEN) {
            return -EINVAL;
        }

        *payload = LOREM_IPSUM + offset;

        data_left = LOREM_IPSUM_STRLEN - offset;
        if (data_left <= *len) {
            *len = data_left;
            *last_block = true;
        } else {
            *last_block = false;
        }

        return 0;
    }

该回调可以代替负载指针
注册用于 PUT/POST 请求：

.. code-block:: c

    struct coap_client_request req = { 0 };

    req.method = COAP_METHOD_PUT;
    req.confirmable = true;
    strcpy(req.path, "lorem-ipsum");
    req.fmt = COAP_CONTENT_FORMAT_TEXT_PLAIN;
    req.cb = response_cb;
    req.payload_cb = lorem_ipsum_cb,

    ret = coap_client_req(&client, sock, &address, &req, -1);


API 参考
*************

.. doxygengroup:: coap_client

.. doxygengroup:: coap_client_tcp
