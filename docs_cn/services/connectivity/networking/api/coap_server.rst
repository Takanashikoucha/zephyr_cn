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

   以下为原文（待翻译）

                                const struct net_sockaddr *addr, socklen_t addr_len,
                                uint16_t age, uint16_t id, const uint8_t *token, uint8_t tkl,
                                bool is_response)
    {
        const struct device *dev = DEVICE_DT_GET(DT_ALIAS(ambient_temp0));
        uint8_t data[CONFIG_COAP_SERVER_MESSAGE_SIZE];
        struct coap_packet response;
        char payload[14];
        struct sensor_value value;
        double temp;
        uint8_t type;

        /* Determine response type */
        type = is_response ? COAP_TYPE_ACK : COAP_TYPE_CON;

        if (!is_response) {
            id = coap_next_id();
        }

        coap_packet_init(&response, data, sizeof(data), COAP_VERSION_1, type, tkl, token,
                         COAP_RESPONSE_CODE_CONTENT, id);

        if (age >= 2U) {
            coap_append_option_int(&response, COAP_OPTION_OBSERVE, age);
        }

        /* Set content format */
        coap_append_option_int(&response, COAP_OPTION_CONTENT_FORMAT,
                               COAP_CONTENT_FORMAT_TEXT_PLAIN);

        /* Get the sensor data */
        sensor_sample_fetch_chan(dev, SENSOR_CHAN_AMBIENT_TEMP);
        sensor_channel_get(dev, SENSOR_CHAN_AMBIENT_TEMP, &value);
        temp = sensor_value_to_double(&value);

        snprintk(payload, sizeof(payload), "%0.2f°C", temp);

        /* Append payload */
        coap_packet_append_payload_marker(&response);
        coap_packet_append_payload(&response, (uint8_t *)payload, strlen(payload));

        return coap_resource_send(resource, &response, addr, addr_len, NULL);
    }

    static int temp_get(struct coap_resource *resource, struct coap_packet *request,
                        struct net_sockaddr *addr, socklen_t addr_len)
    {
        uint8_t token[COAP_TOKEN_MAX_LEN];
        uint16_t id;
        uint8_t tkl;
        int r;

        /* Let the CoAP server parse the request and add/remove observers if needed */
        r = coap_resource_parse_observe(resource, request, addr);

        id = coap_header_get_id(request);
        tkl = coap_header_get_token(request, token);

        return send_temperature(resource, addr, addr_len, r == 0 ? resource->age : 0,
                                id, token, tkl, true);
    }

    static void temp_notify(struct coap_resource *resource, struct coap_observer *observer)
    {
        send_temperature(resource, net_sad(&observer->addr), sizeof(observer->addr), resource->age,
                         0, observer->token, observer->tkl, false);
    }

    static const char * const temp_resource_path[] = { "sensors", "temp1", NULL };
    COAP_RESOURCE_DEFINE(temp_resource, my_service, {
        .path = temp_resource_path,
        .get = temp_get,
        .notify = temp_notify,
    });

    static void notify_observers(struct k_work *work)
    {
        if (sys_slist_is_empty(&temp_resource.observers)) {
            return;
        }

        coap_resource_notify(&temp_resource);
        k_work_reschedule(&temp_work, K_SECONDS(1));
    }

CoAP Events
***********

By enabling :kconfig:option:`CONFIG_NET_MGMT_EVENT` the user can register for CoAP events. The
following example simply prints when an event occurs.

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
