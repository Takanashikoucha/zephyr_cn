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


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
.. code-block:: c

    #include <zephyr/sys/printk.h>
    #include <zephyr/net/coap_mgmt.h>
    #include <zephyr/net/coap_service.h>

    #define COAP_EVENTS_SET (NET_EVENT_COAP_OBSERVER_ADDED | NET_EVENT_COAP_OBSERVER_REMOVED | \
                             NET_EVENT_COAP_SERVICE_STARTED | NET_EVENT_COAP_SERVICE_STOPPED)

    void coap_event_handler(uint64_t mgmt_event, struct net_if *iface,
                            void *info, size_t info_length, void *user_data)
    {
        switch (mgmt_event) {
        case NET_EVENT_COAP_OBSERVER_ADDED:
            printk("CoAP observer added");
            break;
        case NET_EVENT_COAP_OBSERVER_REMOVED:
            printk("CoAP observer removed");
            break;
        case NET_EVENT_COAP_SERVICE_STARTED:
            if (info != NULL && info_length == sizeof(struct net_event_coap_service)) {
                struct net_event_coap_service *net_event = info;

                printk("CoAP service %s started", net_event->service->name);
            } else {
                printk("CoAP service started");
            }
            break;
        case NET_EVENT_COAP_SERVICE_STOPPED:
            if (info != NULL && info_length == sizeof(struct net_event_coap_service)) {
                struct net_event_coap_service *net_event = info;

                printk("CoAP service %s stopped", net_event->service->name);
            } else {
                printk("CoAP service stopped");
            }
            break;
        }
    }

    NET_MGMT_REGISTER_EVENT_HANDLER(coap_events, COAP_EVENTS_SET, coap_event_handler, NULL);

CoRE Link Format
****************

The :kconfig:option:`CONFIG_COAP_SERVER_WELL_KNOWN_CORE` option enables handling the
``.well-known/core`` GET requests by the server. This allows clients to get a list of hypermedia
links to other resources hosted in that server.

API Reference
*************

.. doxygengroup:: coap_service
.. doxygengroup:: coap_mgmt