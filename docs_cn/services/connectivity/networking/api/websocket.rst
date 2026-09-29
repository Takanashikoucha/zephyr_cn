.. _websocket_interface:

Websocket
Client
API
####################

.. contents::
    :local:
    :depth:
    2

Overview
********

Websocket
client
library
允许
Zephyr
connect
到
Websocket
server。
Websocket
client
API
可以
被
application
直接
used
用于
establish
到
server
的
Websocket
connection
或
它
可以
被
used
作为
其他
network
protocols
如
MQTT
的
transport。

参考
这
个
`Websocket
Wikipedia
article
<https://en.wikipedia.org/wiki/WebSocket>`_
获取
关于
Websocket
如何
work
的
detailed
overview。

关于
protocol
本身
的
更多
information
参考
:rfc:`6455`。

Websocket
Transport
*******************

Websocket
API
允许
它
被
used
作为
其他
high
level
protocols
如
MQTT
的
transport。
Zephyr
MQTT
client
library
可
被
configured
use
Websocket
transport
通过
enable
:kconfig:option:`CONFIG_MQTT_LIB_WEBSOCKET`
和
:kconfig:option:`CONFIG_WEBSOCKET_CLIENT`
Kconfig
options。

首先
需要
create
并
connect
一
个
socket
到
Websocket
server：

.. code-block::
   c

   sock
   =
   socket(family,
   SOCK_STREAM,
   IPPROTO_TCP);
   ...
   ret
   =
   connect(sock,
   addr,
   addr_len);
   ...
