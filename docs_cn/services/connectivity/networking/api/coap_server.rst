.. _coap_server_interface:

CoAP
server
###########

.. contents::
    :local:
    :depth:
    2

Overview
********

Zephyr
带
一
个
batteries
included
的
CoAP
server
它
use
services
listen
CoAP
requests。
CoAP
services
handle
通过
sockets
的
communication
并
将
requests
pass
到
registered
的
CoAP
resources。

Setup
*****

需要
某些
configuration
确保
services
可
用
CoAP
server
started。
:kconfig:option:`CONFIG_COAP_SERVER`
option
应该
在
你
的
project
中
被
enabled：

.. code-block::
   cfg
   :caption:
   ``prj.conf``

   CONFIG_COAP_SERVER=y

所有
services
被
added
到
一
个
predefined
的
linker
section
所有
resources
为
每个
service
也
get
它们
各自
的
linker
sections。
如果
你
有
一
个
service
``my_service``
它
必须
被
prefixed
with
``coap_resource_``
并
added
到
一
个
linker
file：

.. code-block::
   c
   :caption:
   ``sections-ram.ld``

   #include
   <zephyr/linker/iterable_sections.h>

   ITERABLE_SECTION_RAM(coap_resource_my_service,
   Z_LINK_ITERABLE_SUBALIGN)

用
CMake
将
这
个
linker
file
added
到
你
的
application：
