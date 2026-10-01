.. _http_client_interface:

HTTP Client
###########

.. contents::
    :local:
    :depth: 2

Overview
********

HTTP client library 允许您发送 HTTP requests 并解析 HTTP responses。Library 通过 sockets API 通信（但不自行创建 sockets。其可用 :kconfig:option:`CONFIG_HTTP_CLIENT` Kconfig option 启用。

Application 须负责创建 socket 并将其传递给 library。因此（根据 application 的需求（library 可通过 plain TCP socket（HTTP）或 TLS socket（HTTPS）通信。

Sample Usage
************

HTTP client library 的 API 有单个 function。

以下是正确创建的 request structure 的示例：

.. code-block:: c

    struct http_request req = { 0 };
    static uint8_t recv_buf[512];

    req.method = HTTP_GET;
    req.url = "/";
    req.host = "localhost";
    req.protocol = "HTTP/1.1";
    req.response = response_cb;
    req.recv_buf = recv_buf;
    req.recv_buf_len = sizeof(recv_buf);

    /* sock is a file descriptor referencing a socket that has been connected
     * to the HTTP server.
     */
    ret = http_client_req(sock, &req, 5000, NULL);

若 server 响应 request（library 通过 request structure 中注册的 response callback 将 response 提供给 application。由于 library 可分块提供 response（application 须能处理这些。

连同包含 response data 的 structure（callback function 还提供关于 library 是否预期收到更多 data 的信息。

以下是非常简单的 response handling function 的示例：

.. code-block:: c

    static int response_cb(struct http_response *rsp,
                           enum http_final_call final_data,
                           void *user_data)
    {
        if (final_data == HTTP_DATA_MORE) {
            LOG_INF("Partial data received (%zd bytes)", rsp->data_len);
        } else if (final_data == HTTP_DATA_FINAL) {
            LOG_INF("All the data received (%zd bytes)", rsp->data_len);
        }

        LOG_INF("Response status %s", rsp->http_status);

        return 0;
    }

library 使用的更多信息参见 :zephyr:code-sample:`HTTP client sample application <sockets-http-client>`。

API Reference
*************

.. doxygengroup:: http_client
