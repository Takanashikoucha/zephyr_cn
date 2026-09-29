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
