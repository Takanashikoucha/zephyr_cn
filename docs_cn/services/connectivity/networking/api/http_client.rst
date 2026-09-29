.. _http_client_interface:

HTTP
Client
###########

.. contents::
    :local:
    :depth:
    2

Overview
********

HTTP
client
library
允许
你
send
HTTP
requests
并
parse
HTTP
responses。
Library
通过
sockets
API
communicate
但
它
不
自己
create
sockets。
它
可
用
:kconfig:option:`CONFIG_HTTP_CLIENT`
Kconfig
option
enable。

Application
必须
负责
create
一
个
socket
并
pass
它
到
library。
因此
根据
application
的
needs
library
可以
通过
plain
TCP
socket
（HTTP）
或
TLS
socket
（HTTPS）
communicate。

Sample
Usage
************

HTTP
client
library
的
API
有
单
个
function。

以下
是
正确
created
的
request
structure
的
一
个
example：

.. code-block::
   c

   struct
   http_request
   req
   =
   {
   0
   };
   static
   uint8_t
   recv_buf[512];

   req.method
   =
   HTTP_GET;
   req.url
   =
   "/";
   req.host
   =
   "localhost";
   req.protocol
   =
   "HTTP/1.1";
   req.response
   =
   response_cb;
   req.recv_buf
   =
   recv_buf;
   req.recv_buf_len
   =
   sizeof(recv_buf);
