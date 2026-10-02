.. _mcp_server_interface:

MCP 服务器
##########

.. contents::
    :local:
    :depth: 2

概述
********

`模型上下文协议`_（MCP）是一个开放标准，用于将 AI 应用程序连接到外部数据源和工具。它定义了 MCP 客户端（AI 智能体）与 MCP 服务器（能力提供者）之间基于 JSON-RPC 的通信协议。

Zephyr MCP 服务器库实现了 MCP 规范（版本 2025-11-25）的服务器角色。它允许联网的 Zephyr 设备暴露工具，AI 智能体可以通过 HTTP 发现并调用这些工具。该库基于现有 Zephyr 子系统构建：HTTP 服务器库用于传输，JSON 库用于序列化。

.. note::

   此库标记为 :ref:`实验性 <api_lifecycle_experimental>`。仅实现了带文本响应的工具服务。更多功能，如更多内容类型、会话管理、SSE 流式传输、授权和其他服务，将在未来版本中实现。

.. _Model Context Protocol: https://modelcontextprotocol.io/specification/2025-11-25

架构
************

.. graphviz::
   :caption: MCP 服务器分层架构
   :alt: MCP 服务器分层架构图

   digraph mcp_arch {
       rankdir=TB;
       node [shape=box, style=filled, fillcolor="#e8e8e8", fontname="sans-serif"];
       edge [arrowsize=0.8];

       app [label="应用程序\n(工具回调)", fillcolor="#cce5ff"];
       core [label="MCP 服务器核心\n(协议、注册表、工作线程)"];
       json [label="JSON 处理\n(Zephyr JSON 库)"];
       transport [label="传输层\n(HTTP / mock)"];

       app -> core [label="注册/响应"];
       core -> json [label="序列化/解析"];
       core -> transport [label="发送/接收"];
   }

应用程序
   注册工具并实现其回调。工具执行结果通过 :c:func:`mcp_server_submit_tool_message` 提交回核心。

MCP 服务器核心
   实现 MCP 协议状态机。管理客户端连接、工具注册表、执行跟踪和可配置的工作线程池。健康监控线程强制超时并触发取消。

JSON 处理
   使用 Zephyr JSON 库序列化发出的响应，并反序列化传入的 JSON-RPC 请求。

传输层
   抽象网络协议。包含的 HTTP 传输使用 Zephyr HTTP 服务器库。Mock 传输可用于单元测试。

HTTP 传输和异步响应
=========================================

Zephyr 的 HTTP 服务器在单个线程中运行，跨所有连接一次处理一个请求。资源回调必须返回后，服务器才能处理来自任何客户端的下一个请求。由于工具执行可能耗时较长，不适合阻塞整个服务器，MCP HTTP 传输实现了轮询到 SSE 的回退机制：

1. 对于 POST 请求，传输内部轮询工具响应，直到 :kconfig:option:`CONFIG_MCP_HTTP_TIMEOUT_MS`（每 :kconfig:option:`CONFIG_MCP_HTTP_POLL_INTERVAL_MS` 检查一次）。
2. 如果在此窗口内响应就绪，则直接作为 ``application/json`` 返回。
3. 如果超时到期，传输切换到 SSE 模式：返回仅包含事件 ID（无数据）的 ``text/event-stream`` 响应。这向客户端发出信号，表示响应正在等待，客户端应开始使用周期性 GET 请求进行轮询（间隔由 :kconfig:option:`CONFIG_MCP_HTTP_SSE_RETRY_MS` 控制）。
4. 客户端随后发送带有 ``Last-Event-Id`` 头的周期性 GET 请求。如果结果就绪，服务器发送响应并结束 SSE 流。如果结果未就绪，服务器再次发送重试响应。

.. note::

   这不是完整的 SSE 流式传输。该机制仅交付无法在初始 HTTP 超时内完成的请求的延迟响应。服务器主动通知和流式工具输出在此阶段不支持。

配置
*************

使用 :kconfig:option:`CONFIG_MCP_SERVER` 启用该库。传输通过 :kconfig:option:`CONFIG_MCP_TRANSPORT_HTTP`（默认）或 :kconfig:option:`CONFIG_MCP_TRANSPORT_MOCK`（仅用于测试）选择。

最小 ``prj.conf``：

.. code-block:: kconfig

   CONFIG_NETWORKING=y
   CONFIG_NET_TCP=y
   CONFIG_HTTP_SERVER=y
   CONFIG_MCP_SERVER=y
   CONFIG_MCP_TRANSPORT_HTTP=y

关键配置组：

可扩展性
   :kconfig:option:`CONFIG_MCP_MAX_CLIENTS`、
   :kconfig:option:`CONFIG_MCP_MAX_CLIENT_REQUESTS`、
   :kconfig:option:`CONFIG_MCP_MAX_TOOLS`、
   :kconfig:option:`CONFIG_MCP_REQUEST_WORKERS`

超时
   :kconfig:option:`CONFIG_MCP_TOOL_EXEC_TIMEOUT_MS`、
   :kconfig:option:`CONFIG_MCP_TOOL_IDLE_TIMEOUT_MS`、
   :kconfig:option:`CONFIG_MCP_TOOL_CANCEL_TIMEOUT_MS`、
   :kconfig:option:`CONFIG_MCP_CLIENT_TIMEOUT_MS`
   :kconfig:option:`CONFIG_MCP_HTTP_TIMEOUT_MS`

内存分配
   :kconfig:option:`CONFIG_MCP_ALLOC_SLAB`（默认）使用预分配 slab 提供确定性、无碎片的分配。
   :kconfig:option:`CONFIG_MCP_ALLOC_HEAP` 使用 ``k_malloc``/``k_free`` 按需分配，代价是可能的碎片化。

使用
*****

服务器设置
============

.. code-block:: c

   #include <zephyr/net/mcp/mcp_server.h>
   #include <zephyr/net/mcp/mcp_server_http.h>

   static mcp_server_ctx_t server;

   int main(void)
   {
       server = mcp_server_init();
       mcp_server_http_init(server);

       /* 在此处注册工具 */

       mcp_server_start(server);
       mcp_server_http_start(server);
       return 0;
   }

工具注册
=================

.. code-block:: c

   static int my_tool_cb(enum mcp_tool_event_type event,
                         const char *arguments,
                         const char *execution_token)
   {
       if (event == MCP_TOOL_CANCEL_REQUEST) {
           struct mcp_tool_message ack = {
               .type = MCP_USR_TOOL_CANCEL_ACK,
           };

           mcp_server_submit_tool_message(server, &ack, execution_token);

           /* 在此处处理取消 */
       }

       struct mcp_tool_message resp = {
           .type = MCP_USR_TOOL_RESPONSE,
           .data = "Tool execution result",
           .length = strlen("Tool execution result"),
           .is_error = false,
       };
       return mcp_server_submit_tool_message(server, &resp, execution_token);
   }

   static const struct mcp_tool_record my_tool = {
       .metadata = {
           .name = "my_tool",
           .input_schema = "{\"type\":\"object\",\"properties\":{}}",
       },
       .callback = my_tool_cb,
   };

   mcp_server_add_tool(server, &my_tool);

``.data`` 字段接受纯文本字符串。服务器会自动将其包装为符合 MCP 规范的 ``"text"`` 内容项。最大长度为 :kconfig:option:`CONFIG_MCP_TOOL_RESULT_MAX_LEN`。

工具回调模式
=====================

阻塞式
   短运行工具直接在工作线程中执行，并在返回前调用 :c:func:`mcp_server_submit_tool_message`。工作线程栈大小为 :kconfig:option:`CONFIG_MCP_REQUEST_WORKER_STACK_SIZE`。

异步式
   长运行工具应生成专用线程，立即从回调返回，并稍后使用提供的执行令牌提交响应。周期性 ping（``MCP_USR_TOOL_PING``）防止健康监控线程取消空闲执行。

取消
   当健康监控线程或客户端请求取消时，回调以 ``MCP_TOOL_CANCEL_REQUEST`` 调用。工具应停止工作并提交 ``MCP_USR_TOOL_CANCEL_ACK``。

工具移除
============

工具可以在运行时使用 :c:func:`mcp_server_remove_tool` 移除。如果工具当前正在执行，调用返回 ``-EBUSY``；稍后重试。

局限性
***********

以下 MCP 功能尚未实现：

- 资源、提示词、采样、根和会话管理
- 服务器主动通知和流式工具输出
- 图像和嵌入资源内容类型（仅支持 ``"text"``）
- 完整 SSE 传输（仅支持延迟响应交付）

测试
*******

单元测试位于 :zephyr_file:`tests/net/lib/mcp/` 下。它们使用 mock 传输（:kconfig:option:`CONFIG_MCP_TRANSPORT_MOCK`）在无网络栈的情况下测试协议逻辑。

示例
******

参见 :zephyr:code-sample:`mcp-server-hello-world`，这是一个可工作的示例，注册了多个工具，包括基于 GPIO 的 LED 控制。

API 参考
*************

.. doxygengroup:: mcp_server
