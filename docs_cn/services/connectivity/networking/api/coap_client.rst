.. _coap_client_interface:

CoAP client
###########

.. contents::
    :local:
    :depth: 2

Overview
********

CoAP client library 允许 application 发送 CoAP requests 并解析 CoAP responses。库可用 :kconfig:option:`CONFIG_COAP_CLIENT` Kconfig option 启用。Application 通过请求中提供给 API 的 callback 获知 response。CoAP client 处理通过 sockets 的通信。由于 CoAP client 不创建其使用的 socket（application 负责创建 socket。支持 Plain UDP 或 DTLS sockets。

CoAP over TCP
=============

CoAP over reliable transports（TCP/TLS）也按 :rfc:`8323` 规格支持。用 :kconfig:option:`CONFIG_COAP_CLIENT_TCP` 启用。TCP client 内部管理 connection setup、CSM（Capabilities and Settings Message）exchange 和 signaling（Ping/Pong、Release、Abort）。与 UDP client 不同（application 不创建 socket — 而是调用 :c:func:`coap_client_tcp_connect` 以 server address。参见 :zephyr:code-sample:`coap-client-tcp` 作为使用示例。

Sample Usage
************

以下是 CoAP client 初始化和 request 发送的示例：

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

在发送任何 requests 之前（CoAP client 需初始化。初始化后（application 可发送 CoAP request 并等待 response。目前单个 CoAP client 一次仅可发送一个 request。可有多个 CoAP clients。

Callback 在以下情况被调用：

- 有 request 的 response
- Request 因某些原因失败

Callback 包含 flag ``last_block``（其指示 response 中是否还有更多 data 到来（意味着当前 response 为 blockwise transfer 的一部分。当 ``last_block`` 设为 true 时（response 完成（且 client 在从 callback 返回后为下一个 request 就绪。

若 server 响应 request（library 通过 request 结构中注册的 response callback 将 response 提供给 application。由于 response 可为 blockwise transfer 且 client 每个 block 调用一次 callback（application 应能处理所有 blocks 以处理 response。

Blockwise transfer 期间（client 按 :rfc:`7959` 要求比较收到的 blocks 的 ETag option。当 resource representation 在 transfer 中途变化时（transfer 被中止（且 callback 以 ``result_code`` 设为 ``-EBADMSG`` 调用。比 RFC 最低要求（其仅规定比较 server 提供的 ETags）更严格（当 ETag option 在 blocks 之间出现或消失时 transfer 也被中止（因为此类 tagged 和 untagged blocks 的混合无法验证。Application 应丢弃收到的部分 data 并可重试 request。

以下是非常简单 response handling function 的示例：

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

Application 也可向 request 添加 CoAP options。以下是 application 向 initial request 添加 Block2 option 的示例（以向 server 建议预期需 blockwise transfer 的 resource 的最大 block size（参见 :rfc:`7959` Figure 3: Block-Wise GET with Early Negotiation）。

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

可选地（application 可注册 payload callback 代替为 CoAP upload 提供 payload pointer。此类情况下（CoAP client library 在准备 PUT/POST request 时调用此 callback（使 application 可分块提供 payload（而无需提供包含整个 payload 的单个 contiguous buffer。提供 Lorem Ipsum string 内容的示例 callback 可如下：

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

Callback 然后可代替 payload pointer 注册用于 PUT/POST request：

.. code-block:: c

    struct coap_client_request req = { 0 };

    req.method = COAP_METHOD_PUT;
    req.confirmable = true;
    strcpy(req.path, "lorem-ipsum");
    req.fmt = COAP_CONTENT_FORMAT_TEXT_PLAIN;
    req.cb = response_cb;
    req.payload_cb = lorem_ipsum_cb,

    ret = coap_client_req(&client, sock, &address, &req, -1);


API Reference
*************

.. doxygengroup:: coap_client

.. doxygengroup:: coap_client_tcp
