.. _http_server_interface:

HTTP Server
###########

.. contents::
    :local:
    :depth: 2

Overview
********

Zephyr 提供 HTTP server library（其允许注册 HTTP services 和与这些 services 关联的 HTTP resources。Server 为每个注册的 service 创建 listening socket（并处理 incoming client connections。可通过 plain TCP socket（HTTP）或 TLS socket（HTTPS）通信。支持 HTTP/1.1（:rfc:`2616`）、HTTP/2（:rfc:`9113`）和 HTTP/3（:rfc:`9114`）protocol 版本。

Server 操作通常对 application 透明（在 background thread 中运行。Application 可用相应 API functions 控制 server activity。

某些 resource types（例如 dynamic resource）提供 resource-specific application callbacks（允许 server 与 application 交互（例如提供 resource content（或处理 request payload）。

当前（支持以下 resource types：

* Static resources - compile-time 定义的 content（runtime 不可修改（:c:enumerator:`HTTP_RESOURCE_TYPE_STATIC`）。

* Static file system resources - filesystem 挂载的路径和 filesystem 可用的 URL 在 build time 固定（但 filesystem 内的 content 可动态更改。这意味着 files 可被 HTTP server 之外的其他代码创建、修改或删除（:c:enumerator:`HTTP_RESOURCE_TYPE_STATIC_FS`）。

* Dynamic resources - runtime 由相应 application callback 提供的 content（:c:enumerator:`HTTP_RESOURCE_TYPE_DYNAMIC`）。

* Websocket resources - 允许与 server 建立 Websocket connections（:c:enumerator:`HTTP_RESOURCE_TYPE_WEBSOCKET`）。

Zephyr 提供演示 HTTP(s) server 操作和各种 resource types 使用的 sample。更多信息参见 :zephyr:code-sample:`sockets-http-server`。

Server Setup
************

需在 application 中启用 HTTP server 功能需一些前提条件。

首先（HTTP server 须用 :kconfig:option:`CONFIG_HTTP_SERVER` Kconfig option 在 application 的 configuration file 中启用：

.. code-block:: cfg
    :caption: ``prj.conf``

    CONFIG_HTTP_SERVER=y

所有 HTTP services 和 HTTP resources 放在专用 linker section 中。Services 的 linker section 本地预定义（然而 application 负责定义与相应 services 关联的 resources 的 linker sections。Resources 的 linker section 名称应以 ``http_resource_desc_`` 为前缀（以 service 名称为后缀。

Resources 的 linker sections 应在 linker file 中定义。例如（对名为 ``my_service`` 的 service（linker section 应定义如下：

.. code-block:: c
    :caption: ``sections-rom.ld``

    #include <zephyr/linker/iterable_sections.h>

    ITERABLE_SECTION_ROM(http_resource_desc_my_service, Z_LINK_ITERABLE_SUBALIGN)

最后（linker file 和 linker section 须用 CMake 添加到您的 application：

.. code-block:: cmake
    :caption: ``CMakeLists.txt``

    zephyr_linker_sources(SECTIONS sections-rom.ld)
    zephyr_linker_section(NAME http_resource_desc_my_service
                          KVMA RAM_REGION GROUP RODATA_REGION)

.. note::

    您须为系统中注册的每个 HTTP service 定义单独的 linker section。

Sample Usage
************

Services
========

Application 须用 :c:macro:`HTTP_SERVICE_DEFINE` macro 定义 HTTP service（或多个 services）（名称与用于 linker section 的名称相同：

.. code-block:: c

    #include <zephyr/net/http/service.h>

    static uint16_t http_service_port = 80;

    HTTP_SERVICE_DEFINE(my_service, "0.0.0.0", &http_service_port, 1, 10, NULL, NULL, NULL);

或者（可用 :c:macro:`HTTPS_SERVICE_DEFINE` 定义 HTTPS service：

.. code-block:: c

    #include <zephyr/net/http/service.h>
    #include <zephyr/net/tls_credentials.h>

    #define HTTP_SERVER_CERTIFICATE_TAG 1

    static uint16_t https_service_port = 443;
    static const sec_tag_t sec_tag_list[] = {
        HTTP_SERVER_CERTIFICATE_TAG,
    };

    HTTPS_SERVICE_DEFINE(my_service, "0.0.0.0", &https_service_port, 1, 10,
                         NULL, NULL, NULL, sec_tag_list, sizeof(sec_tag_list));

Per-service configuration
=========================

HTTP services 支持单独的 service configuration（目前仅包括通过 ``http_service_config`` structure 的 socket 创建。这允许 applications 定制 socket 创建行为（例如设置特定 socket options 或使用 custom socket types。

要使用 custom socket 创建：

.. code-block:: c

    static int my_socket_create(const struct http_service_desc *svc, int af, int proto)
    {
        int fd;

        /* Create socket with custom parameters */
        fd = zsock_socket(af, SOCK_STREAM, proto);
        if (fd < 0) {
            return fd;
        }

        /* Set custom socket options */
        /* Add any other custom socket configuration */

        return fd;
    }

    static const struct http_service_config my_service_config = {
        .socket_create = my_socket_create,
    };

    static uint16_t http_service_port = 80;

    HTTP_SERVICE_DEFINE(my_service, "0.0.0.0", &http_service_port, 1, 10,
                        NULL, NULL, &my_service_config);

Custom socket 创建 function 接收：
- ``svc``：指向 service descriptor 的 pointer
- ``af``：Address family（NET_AF_INET 或 NET_AF_INET6）
- ``proto``：Protocol（NET_IPPROTO_TCP 或 HTTPS 的 NET_IPPROTO_TLS_1_2）

Function 成功时应返回 socket file descriptor（失败时返回负 error code。

若无需 custom configuration（简单将 ``NULL`` 传给 config parameter：

.. code-block:: c

    HTTP_SERVICE_DEFINE(my_service, "0.0.0.0", &http_service_port, 1, 10,
                        NULL, NULL, NULL);

Fallback Resources
==================

定义 HTTP/HTTPS service 时可用 ``_res_fallback`` parameter 指定 fallback resource（若其他 resource 不匹配 URL 则使用。这可例如用于为所有未知 paths 提供 index page（对在前端处理 routing 的 single-page app 有用）或用于 customized 404 response。

.. code-block:: c

    static int default_handler(struct http_client_ctx *client, enum http_transaction_status status,
		       const struct http_request_ctx *request_ctx,
		       struct http_response_ctx *response_ctx, void *user_data)
    {
        static const char response_404[] = "Oops, page not found!";

        if (status == HTTP_SERVER_REQUEST_DATA_FINAL) {
            response_ctx->status = 404;
            response_ctx->body = response_404;
            response_ctx->body_len = sizeof(response_404) - 1;
            response_ctx->final_chunk = true;
        }

        return 0;
    }

    static struct http_resource_detail_dynamic default_detail = {
        .common = {
            .type = HTTP_RESOURCE_TYPE_DYNAMIC,
            .bitmask_of_supported_http_methods = BIT(HTTP_GET),
        },
        .cb = default_handler,
        .user_data = NULL,
    };

    /* Register a fallback resource to handle any unknown path */
    HTTP_SERVICE_DEFINE(my_service, "0.0.0.0", &http_service_port, 1, 10, NULL, &default_detail, NULL);

.. note::

    HTTPS services 依赖于系统中注册的 TLS credentials。如何配置系统中的 TLS credentials 参见 :ref:`sockets_tls_credentials_subsys`。

HTTP(s) service 定义后（可用 :c:macro:`HTTP_RESOURCE_DEFINE` macro 为其注册 resources。

Application 可通过启用 :kconfig:option:`CONFIG_HTTP_SERVER_RESOURCE_WILDCARD` option 启用 resource wildcard 支持。设置此 option 时（可用单个 resource handler 匹配多个 incoming HTTP requests。`fnmatch() <https://pubs.opengroup.org/onlinepubs/9699919799/functions/fnmatch.html>`__ POSIX API function 用于匹配 URL paths 中的 pattern。

示例：

.. code-block:: c

    HTTP_RESOURCE_DEFINE(my_resource, my_service, "/foo*", &resource_detail);

这将匹配所有以 ``foo`` 字符串开头的 URLs。pattern matching syntax 描述参见 `POSIX.2 chapter 2.13 <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_13>`__。

Static resources
================

Static resource content 在 build-time 定义（不可变。以下示例展示如何在 application 中将 gzip 压缩的 webpage 定义为 static resource：

.. code-block:: c

    static const uint8_t index_html_gz[] = {
        #include "index.html.gz.inc"
    };

    struct http_resource_detail_static index_html_gz_resource_detail = {
        .common = {
            .type = HTTP_RESOURCE_TYPE_STATIC,
            .bitmask_of_supported_http_methods = BIT(HTTP_GET),
            .content_encoding = "gzip",
        },
        .static_data = index_html_gz,
        .static_data_len = sizeof(index_html_gz),
    };

    HTTP_RESOURCE_DEFINE(index_html_gz_resource, my_service, "/",
                         &index_html_gz_resource_detail);

Resource content 和 content encoding 为 application-specific。对以上示例（可在 build 期间生成 gzip 压缩的 webpage（将以下代码添加到 application 的 ``CMakeLists.txt`` file：

.. code-block:: cmake
    :caption: ``CMakeLists.txt``

    set(gen_dir ${ZEPHYR_BINARY_DIR}/include/generated/)
    set(source_file_index src/index.html)
    generate_inc_file_for_target(app ${source_file_index} ${gen_dir}/index.html.gz.inc --gzip)

其中 ``src/index.html`` 为要压缩的 webpage 的位置。

Static filesystem resources
===========================

Static filesystem resource content 在 build-time 定义（不可变。注意仅支持 ``GET`` 操作（user 无法向 filesystem 上传 files。以下示例展示如何在 application 中将 path 定义为 static resource：

.. code-block:: c

    struct http_resource_detail_static_fs static_fs_resource_detail = {
        .common = {
            .type                              = HTTP_RESOURCE_TYPE_STATIC_FS,
            .bitmask_of_supported_http_methods = BIT(HTTP_GET),
        },
        .fs_path = "/lfs1/www",
    };

    HTTP_RESOURCE_DEFINE(static_fs_resource, my_service, "*", &static_fs_resource_detail);

/lfs1/www 中的所有 files 对 client 可用。若 file 被 gzipped（file 名称须追加 .gz（例如 index.html.gz）（然后 client 请求 index.html 时 server 交付 index.html.gz（并在 HTTP header 中添加 gzip content-encoding。

Content type 基于 file extension 评估。Server 支持 .html、.js、.css、.jpg、.png 和 .svg。更多 content types 可用 :c:macro:`HTTP_SERVER_CONTENT_TYPE` macro 提供。所有其他 files 以 content type text/html 提供。

.. code-block:: c

    HTTP_SERVER_CONTENT_TYPE(json, "application/json")

从 static filesystem 提供 files 时（response chunk size 可用 :kconfig:option:`CONFIG_HTTP_SERVER_STATIC_FS_RESPONSE_SIZE` Kconfig option 配置。这决定向 clients 传输 file content 时单个 chunks 的 size。

Dynamic resources
=================

对 dynamic resource（注册 resource callback 以在 server 和 application 之间交换 data。

以下示例代码展示如何注册带简单 resource handler 的 dynamic resource（其将收到的 data echo 回 client：

.. code-block:: c

    static int dyn_handler(struct http_client_ctx *client, enum http_transaction_status status,
                           const struct http_request_ctx *request_ctx,
                           struct http_response_ctx *response_ctx, void *user_data)
    {
    #define MAX_TEMP_PRINT_LEN 32
        static char print_str[MAX_TEMP_PRINT_LEN];
        enum http_method method = client->method;
        static size_t processed;

        __ASSERT_NO_MSG(request_ctx->data != NULL);

        if (status == HTTP_SERVER_TRANSACTION_ABORTED ||
            status == HTTP_SERVER_TRANSACTION_COMPLETE) {
            if (status == HTTP_SERVER_TRANSACTION_ABORTED) {
                LOG_DBG("Transaction aborted after %zd bytes.", processed);
            }
            processed = 0;
            return 0;
        }

        processed += request_ctx->data_len;

        snprintf(print_str, sizeof(print_str), "%s received (%zd bytes)",
                 http_method_str(method), request_ctx->data_len);
        LOG_HEXDUMP_DBG(request_ctx->data, request_ctx->data_len, print_str);

        if (status == HTTP_SERVER_REQUEST_DATA_FINAL) {
            LOG_DBG("All data received (%zd bytes).", processed);
            processed = 0;
        }

        /* Echo data back to client */
        response_ctx->body = request_ctx->data;
        response_ctx->body_len = request_ctx->data_len;
        response_ctx->final_chunk = (status == HTTP_SERVER_REQUEST_DATA_FINAL);

        return 0;
    }

    struct http_resource_detail_dynamic dyn_resource_detail = {
        .common = {
            .type = HTTP_RESOURCE_TYPE_DYNAMIC,
            .bitmask_of_supported_http_methods =
                BIT(HTTP_GET) | BIT(HTTP_POST),
        },
        .cb = dyn_handler,
        .user_data = NULL,
    };

    HTTP_RESOURCE_DEFINE(dyn_resource, my_service, "/dynamic",
                         &dyn_resource_detail);


Resource callback 可能对单个 request 被调用多次（因此 application 应能跟踪收到的 data 进度。

``status`` field 告知 application 从 server 向 application 传递 request payload 的进度。只要 status 报告 :c:enumerator:`HTTP_SERVER_REQUEST_DATA_MORE`（application 应预期在连续 callback calls 中提供更多 data。一旦所有 request payload 传递给 application（server 报告 :c:enumerator:`HTTP_SERVER_REQUEST_DATA_FINAL` status。request 处理期间通信错误时（例如 client 在完整 payload 收到前关闭 connection）（server 报告 :c:enumerator:`HTTP_SERVER_TRANSACTION_ABORTED`。当 response 完全发送到 client 时（server 报告 :c:enumerator:`HTTP_SERVER_TRANSACTION_COMPLETE` status。两个 events 之一指示 request 处理完成（且 application 应重置为 resource 记录的任何 progress（并等待新 request 到来。Server 保证 resource 一次只能被单个 client 访问。

``request_ctx`` parameter 用于向 application 传递 request data：

* ``data`` 和 ``data_len`` fields 向 application 传递 request data。

* ``headers``、``header_count`` 和 ``headers_status`` fields 在启用 :kconfig:option:`CONFIG_HTTP_SERVER_CAPTURE_HEADERS` 时向 application 传递 request headers。这些 fields 仅在 request 的第一个 callback 中填充；细节参见 :ref:`http_server_interface_accessing_request_headers`。

``response_ctx`` field 由 application 用于向 HTTP server 传递 response data：

* ``status`` field 允许 application 发送 HTTP response code。若未填充（response code 默认为 200。

* ``headers`` 和 ``header_count`` fields 可由 application 用于发送任意 HTTP headers。若未填充（默认仅发送 Transfer-Encoding 和 Content-Type。Callback 可在需要时覆盖 Content-Type。

* ``body`` 和 ``body_len`` fields 用于发送 body data。

* ``final_chunk`` field 用于指示 application 无更多 response data 可发送。

Headers 和/或 response codes 仅在首个填充的 ``response_ctx`` 中发送（之后仅允许在后续 callbacks 中进一步 body data。

Server 调用 resource callback 直到其向 application 提供所有 request data（且 application 报告回复中无更多 data 可包含。

Websocket resources
===================

Websocket resources 注册 application callback（其在 Websocket connection upgrade 发生时调用。Callback 提供与底层 TCP/TLS connection 对应的 socket descriptor。调用后（application 完全控制 socket（即负责完成后释放。

.. code-block:: c

    static int ws_socket;
    static uint8_t ws_recv_buffer[1024];

    int ws_setup(int sock, struct http_request_ctx *request_ctx, void *user_data)
    {
        ws_socket = sock;
        return 0;
    }

    struct http_resource_detail_websocket ws_resource_detail = {
        .common = {
            .type = HTTP_RESOURCE_TYPE_WEBSOCKET,
            /* We need HTTP/1.1 Get method for upgrading */
            .bitmask_of_supported_http_methods = BIT(HTTP_GET),
        },
        .cb = ws_setup,
        .data_buffer = ws_recv_buffer,
        .data_buffer_len = sizeof(ws_recv_buffer),
        .user_data = NULL, /* Fill this for any user specific data */
    };

    HTTP_RESOURCE_DEFINE(ws_resource, my_service, "/", &ws_resource_detail);

上述最小化示例展示如何注册带简单 callback 的 Websocket resource（其仅用于存储提供的 socket descriptor。Websocket connection 的进一步处理为 application-specific（因此超出此 guide 范围。Websocket-based echo service 实现示例参见 :zephyr:code-sample:`sockets-http-server`。

.. _http_server_interface_accessing_request_headers:

Accessing request headers
=========================

Application 可注册对任何特定 HTTP request headers 的兴趣。这些 headers 然后为每个 incoming request 存储（并可在 dynamic resource callback 内访问。

.. important::

   Captured request headers 仅在给定 request 的**第一个 callback** 中传递给 application。同一 request 的任何后续 callback 中 ``request_ctx`` 的 ``headers``、``header_count`` 和 ``headers_status`` fields 被清除（``headers_status`` 变为 :c:enumerator:`HTTP_HEADER_STATUS_NONE`）。Applications 须在第一个 callback 中复制出所需的所有 header values（而非稍后读取。

   注意第一个 callback 可能也可能不带 request body data（这取决于 HTTP method 和 transport framing）。不要以 body data 的存在为条件处理 headers：始终检查 ``headers_status``（并在其非 :c:enumerator:`HTTP_HEADER_STATUS_NONE` 时存储 headers。

此功能须先用 :kconfig:option:`CONFIG_HTTP_SERVER_CAPTURE_HEADERS` Kconfig option 启用。

然后 application 可注册要捕获的 headers（并在 dynamic resource callback 内读取 values。推荐 pattern 为在第一个 callback 中复制出感兴趣的 headers（然后在完整 request body 收到后对其行动：

.. code-block:: c

    HTTP_SERVER_REGISTER_HEADER_CAPTURE(capture_user_agent, "User-Agent");

    static char user_agent[64];

    static int dyn_handler(struct http_client_ctx *client, enum http_transaction_status status,
                           const struct http_request_ctx *request_ctx,
                           struct http_response_ctx *response_ctx, void *user_data)
    {
        /* Request headers are only present in the first callback, so copy out
         * any values needed later before they are gone.
         */
        if (request_ctx->headers_status != HTTP_HEADER_STATUS_NONE) {
            for (size_t i = 0; i < request_ctx->header_count; i++) {
                const struct http_header *hdr = &request_ctx->headers[i];

                LOG_INF("Captured header: '%s: %s'", hdr->name, hdr->value);

                if (strcasecmp(hdr->name, "User-Agent") == 0) {
                    strncpy(user_agent, hdr->value, sizeof(user_agent) - 1);
                }
            }
        }

        /* Process request body data (may be empty in the first callback). */

        if (status == HTTP_SERVER_REQUEST_DATA_FINAL) {
            /* Full request received: act on the body together with the header
             * values stashed above (e.g. user_agent).
             */
        }

        return 0;
    }

API Reference
*************

.. doxygengroup:: http_service
.. doxygengroup:: http_server
