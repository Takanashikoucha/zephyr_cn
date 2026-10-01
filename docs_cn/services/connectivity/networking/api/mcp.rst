.. _mcp_server_interface:

MCP Server
##########

.. contents::
    :local:
    :depth: 2

Overview
********

`Model Context Protocol`_（MCP）是连接 AI applications 到外部 data sources 和 tools 的 open standard。其定义 MCP clients（AI agents）和 MCP servers（capability providers）之间的 JSON-RPC-based communication protocol。

Zephyr MCP Server library 实现 MCP specification（version 2025-11-25）的 server role。其允许联网的 Zephyr devices 暴露 tools（AI agents 可通过 HTTP 发现和调用。Library 构建于现有 Zephyr subsystems 之上：HTTP server library 用于 transport（JSON library 用于 serialization。

.. note::

   此 library 标记为 :ref:`experimental <api_lifecycle_experimental>`。仅实现带 text responses 的 tool service。额外 features（如更多 content types、session management、SSE streaming、authorization 和其他 services）计划用于未来 releases。

.. _Model Context Protocol: https://modelcontextprotocol.io/specification/2025-11-25

Architecture
************

.. graphviz::
   :caption: MCP Server layered architecture
   :alt: MCP Server layered architecture diagram

   digraph mcp_arch {
       rankdir=TB;
       node [shape=box, style=filled, fillcolor="#e8e8e8", fontname="sans-serif"];
       edge [arrowsize=0.8];

       app [label="Application\n(tool callbacks)", fillcolor="#cce5ff"];
       core [label="MCP Server Core\n(protocol, registries, workers)"];
       json [label="JSON Processing\n(Zephyr JSON library)"];
       transport [label="Transport Layer\n(HTTP / mock)"];

       app -> core [label="register/respond"];
       core -> json [label="serialize/parse"];
       core -> transport [label="send/receive"];
   }

Application
   注册 tools 并实现其 callbacks。Tool 执行结果通过 :c:func:`mcp_server_submit_tool_message` 提交回 core。

MCP Server Core
   实现 MCP protocol state machines。管理 client connections、tool registry、execution tracking（以及可配置的 worker thread pool。Health monitor thread 强制 timeouts（并触发 cancellations。

JSON Processing
   用 Zephyr JSON library 序列化 outgoing responses（并反序列化 incoming JSON-RPC requests。

Transport Layer
   抽象 network protocol。包含的 HTTP transport 使用 Zephyr HTTP server library。Mock transport 可用于 unit testing。

HTTP Transport and Asynchronous Responses
=========================================

Zephyr 的 HTTP server 在单个 thread 中运行（跨所有 connections 一次处理一个 request。Resource callback 须返回后 server 才能处理来自任何 client 的下一个 request。由于 tool 执行可能比阻塞整个 server 可接受的时间更长（MCP HTTP transport 实现 polling-to-SSE fallback：

1. POST request 时（transport 内部轮询 tool response 直到 :kconfig:option:`CONFIG_MCP_HTTP_TIMEOUT_MS`（每 :kconfig:option:`CONFIG_MCP_HTTP_POLL_INTERVAL_MS` 检查一次）。
2. 若此窗口内 response 就绪（其直接作为 ``application/json`` 返回。
3. 若 timeout 过期（transport 切换到 SSE mode：其返回仅含 event ID（无 data）的 ``text/event-stream`` response。这向 client 信号 response 待处理（其应开始用周期性 GET requests 轮询（interval 由 :kconfig:option:`CONFIG_MCP_HTTP_SSE_RETRY_MS` 控制）。
4. Client 然后发送带 ``Last-Event-Id`` header 的周期性 GET requests。若 result 就绪（server 发送 response 并结束 SSE stream。若 result 未就绪（server 再次发送 retry response。

.. note::

   这不是完整 SSE streaming。Mechanism 仅交付无法在初始 HTTP timeout 内完成的 requests 的 deferred responses。Server-initiated notifications 和 streaming tool output 此阶段不支持。

Configuration
*************

用 :kconfig:option:`CONFIG_MCP_SERVER` 启用 library。Transport 通过 :kconfig:option:`CONFIG_MCP_TRANSPORT_HTTP`（默认）或 :kconfig:option:`CONFIG_MCP_TRANSPORT_MOCK`（仅测试）选择。

最小 ``prj.conf``：

.. code-block:: kconfig

   CONFIG_NETWORKING=y
   CONFIG_NET_TCP=y
   CONFIG_HTTP_SERVER=y
   CONFIG_MCP_SERVER=y
   CONFIG_MCP_TRANSPORT_HTTP=y

关键 configuration groups：

Scalability
   :kconfig:option:`CONFIG_MCP_MAX_CLIENTS`、
   :kconfig:option:`CONFIG_MCP_MAX_CLIENT_REQUESTS`、
   :kconfig:option:`CONFIG_MCP_MAX_TOOLS`、
   :kconfig:option:`CONFIG_MCP_REQUEST_WORKERS`

Timeouts
   :kconfig:option:`CONFIG_MCP_TOOL_EXEC_TIMEOUT_MS`、
   :kconfig:option:`CONFIG_MCP_TOOL_IDLE_TIMEOUT_MS`、
   :kconfig:option:`CONFIG_MCP_TOOL_CANCEL_TIMEOUT_MS`、
   :kconfig:option:`CONFIG_MCP_CLIENT_TIMEOUT_MS`
   :kconfig:option:`CONFIG_MCP_HTTP_TIMEOUT_MS`

Memory allocation
   :kconfig:option:`CONFIG_MCP_ALLOC_SLAB`（默认）用预分配 slabs 提供确定性、无碎片 allocation。
   :kconfig:option:`CONFIG_MCP_ALLOC_HEAP` 用 ``k_malloc``/``k_free`` 按需 allocation（代价为可能碎片化。

Usage
*****

Server Setup
============

.. code-block:: c

   #include <zephyr/net/mcp/mcp_server.h>
   #include <zephyr/net/mcp/mcp_server_http.h>

   static mcp_server_ctx_t server;

   int main(void)
   {
       server = mcp_server_init();
       mcp_server_http_init(server);

       /* Register tools here */

       mcp_server_start(server);
       mcp_server_http_start(server);
       return 0;
   }

Tool Registration
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

           /* Handle cancellation here */
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

``.data`` field 接受 plain text string。Server 自动将其包装为 MCP-compliant 的 ``"text"`` content item。最大长度为 :kconfig:option:`CONFIG_MCP_TOOL_RESULT_MAX_LEN`。

Tool Callback Patterns
======================

Blocking
   短运行 tools 直接在 worker thread 中执行（并在返回前调用 :c:func:`mcp_server_submit_tool_message`。Worker stack size 为 :kconfig:option:`CONFIG_MCP_REQUEST_WORKER_STACK_SIZE`。

Asynchronous
   长运行 tools 应生成专用 thread（立即从 callback 返回（并稍后用提供的 execution token 提交 response。周期性 pings（``MCP_USR_TOOL_PING``）防止 health monitor 取消 idle executions。

Cancellation
   当 health monitor 或 client 请求取消时（callback 以 ``MCP_TOOL_CANCEL_REQUEST`` 调用。Tool 应停止工作（并提交 ``MCP_USR_TOOL_CANCEL_ACK``。

Tool Removal
============

Tools 可用 :c:func:`mcp_server_remove_tool` 在 runtime 移除。若 tool 当前正在执行（调用返回 ``-EBUSY``；稍后重试。

Limitations
***********

以下 MCP features 尚未实现：

- Resources、prompts、sampling、roots 和 session management
- Server-initiated notifications 和 streaming tool output
- Image 和 embedded-resource content types（仅支持 ``"text"``）
- 完整 SSE transport（仅支持 deferred response 交付）

Testing
*******

Unit tests 可在 :zephyr_file:`tests/net/lib/mcp/` 下找到。其用 mock transport（:kconfig:option:`CONFIG_MCP_TRANSPORT_MOCK`）在无 network stack 的情况下演练 protocol logic。

Sample
******

工作示例参见 :zephyr:code-sample:`mcp-server-hello-world`（其注册多个 tools（包括基于 GPIO 的 LED 控制。

API Reference
*************

.. doxygengroup:: mcp_server
