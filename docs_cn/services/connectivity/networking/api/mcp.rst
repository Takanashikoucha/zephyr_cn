.. _mcp_server_interface:

MCP
Server
##########

.. contents::
    :local:
    :depth:
    2

Overview
********

`Model
Context
Protocol`_
（MCP）
是
一
个
open
standard
用于
connect
AI
applications
到
external
data
sources
和
tools。
它
define
了
MCP
clients
（AI
agents）
和
MCP
servers
（capability
providers）
之间
的
JSON
RPC
based
的
communication
protocol。

Zephyr
MCP
Server
library
implement
MCP
specification
（version
2025
11
25）
的
server
role。
它
允许
networked
的
Zephyr
devices
expose
tools
AI
agents
可以
通过
HTTP
discover
和
invoke。
Library
build
在
现有
的
Zephyr
subsystems
上：
HTTP
server
library
用于
transport
JSON
library
用于
serialization。

.. note::

   这
   个
   library
   被
   marked
   :ref:`experimental
   <api_lifecycle_experimental>`。
   只
   有
   带
   text
   responses
   的
   tool
   service
   被
   implemented。
   额外
   的
   features
   如
   更多
   的
   content
   types、
   session
   management、
   SSE
   streaming、
   authorization
   和
   其他
   services
   计划
   在
   未来
   releases
   中
   提供。

.. _Model
Context
Protocol:
   https://modelcontextprotocol.io/specification/2025-11-25

Architecture
************

.. graphviz::
   :caption:
   MCP
   Server
   layered
   architecture
   :alt:
   MCP
   Server
   layered
   architecture
   diagram

   digraph
   mcp_arch
   {


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
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

The ``.data`` field accepts a plain text string. The server wraps it into an
MCP-compliant ``"text"`` content item automatically. Maximum length is
:kconfig:option:`CONFIG_MCP_TOOL_RESULT_MAX_LEN`.

Tool Callback Patterns
======================

Blocking
   Short-running tools execute directly in the worker thread and call
   :c:func:`mcp_server_submit_tool_message` before returning. The worker
   stack size is :kconfig:option:`CONFIG_MCP_REQUEST_WORKER_STACK_SIZE`.

Asynchronous
   Long-running tools should spawn a dedicated thread, return immediately
   from the callback, and submit the response later using the provided
   execution token. Periodic pings (``MCP_USR_TOOL_PING``) prevent the
   health monitor from cancelling idle executions.

Cancellation
   When the health monitor or a client requests cancellation, the callback
   is invoked with ``MCP_TOOL_CANCEL_REQUEST``. The tool should stop work
   and submit ``MCP_USR_TOOL_CANCEL_ACK``.

Tool Removal
============

Tools can be removed at runtime with :c:func:`mcp_server_remove_tool`. The
call returns ``-EBUSY`` if the tool is currently executing; retry later.

Limitations
***********

The following MCP features are not yet implemented:

- Resources, prompts, sampling, roots, and session management
- Server-initiated notifications and streaming tool output
- Image and embedded-resource content types (only ``"text"`` is supported)
- Full SSE transport (only deferred response delivery is supported)

Testing
*******

Unit tests are available under :zephyr_file:`tests/net/lib/mcp/`. They use
the mock transport (:kconfig:option:`CONFIG_MCP_TRANSPORT_MOCK`) to exercise
protocol logic without a network stack.

Sample
******

See :zephyr:code-sample:`mcp-server-hello-world` for a working example that
registers multiple tools including GPIO-based LED control.

API Reference
*************

.. doxygengroup:: mcp_server