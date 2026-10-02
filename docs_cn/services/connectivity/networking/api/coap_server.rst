.. _coap_server_interface:

CoAP 服务器
###########

.. contents::
    :local:
    :depth: 2

概述
********

Zephyr 自带一个功能完备（batteries-included）的 CoAP 服务器，
它通过服务（service）监听 CoAP
请求。CoAP 服务负责处理通过套接字的通信，
并将请求传递给已注册的
CoAP 资源。

设置
*****

需要进行一些配置，以确保服务
能够通过 CoAP 服务器启动。
项目中应启用 :kconfig:option:`CONFIG_COAP_SERVER` 选项：

.. code-block:: cfg
    :caption: ``prj.conf``

    CONFIG_COAP_SERVER=y

所有服务都被添加到预定义的连接器（linker）段中，
每个服务的所有资源也会
获得各自的连接器段。
如果您有一个服务 ``my_service``，
它必须以 ``coap_resource_`` 为前缀，
并添加到连接器文件中：

.. code-block:: c
    :caption: ``sections-ram.ld``

    #include <zephyr/linker/iterable_sections.h>

    ITERABLE_SECTION_RAM(coap_resource_my_service, Z_LINK_ITERABLE_SUBALIGN)

使用 CMake 将该连接器文件
添加到您的应用中：

.. code-block:: cmake
    :caption: ``CMakeLists.txt``

    # Support LD linker template
    zephyr_linker_sources(DATA_SECTIONS sections-ram.ld)

    # Support CMake linker generator
    zephyr_iterable_section(NAME coap_resource_my_service
                            GROUP DATA_REGION ${XIP_ALIGN_WITH_INPUT})

现在，您可以将服务
定义为应用的一部分：

.. code-block:: c

    #include <zephyr/net/coap_service.h>

    static const uint16_t my_service_port = 5683;

    COAP_SERVICE_DEFINE(my_service, "0.0.0.0", &my_service_port, COAP_SERVICE_AUTOSTART);

.. note::

    使用 ``COAP_SERVICE_AUTOSTART`` 标志定义的服务
    会随 CoAP
    服务器线程一起启动。服务
    可分别使用 ``coap_service_start`` 和
    ``coap_service_stop`` 手动启动和停止。

示例用法
************

以下是注册到服务的 CoAP 资源示例：

.. code-block:: c

    #include <zephyr/net/coap_service.h>

    static int my_get(struct coap_resource *resource, struct coap_packet *request,
                      struct net_sockaddr *addr, socklen_t addr_len)
    {
        static const char *msg = "Hello, world!";
        uint8_t data[CONFIG_COAP_SERVER_MESSAGE_SIZE];
        struct coap_packet response;
        uint16_t id;
        uint8_t token[COAP_TOKEN_MAX_LEN];
        uint8_t tkl, type;

        type = coap_header_get_type(request);
        id = coap_header_get_id(request);
        tkl = coap_header_get_token(request, token);

        /* Determine response type */
        type = (type == COAP_TYPE_CON) ? COAP_TYPE_ACK : COAP_TYPE_NON_CON;

        coap_packet_init(&response, data, sizeof(data), COAP_VERSION_1, type, tkl, token,
                         COAP_RESPONSE_CODE_CONTENT, id);

        /* Set content format */
        coap_append_option_int(&response, COAP_OPTION_CONTENT_FORMAT,
                               COAP_CONTENT_FORMAT_TEXT_PLAIN);

        /* Append payload */
        coap_packet_append_payload_marker(&response);
        coap_packet_append_payload(&response, (uint8_t *)msg, strlen(msg));

        /* Send to response back to the client */
        return coap_resource_send(resource, &response, addr, addr_len, NULL);
    }

    static int my_put(struct coap_resource *resource, struct coap_packet *request,
                      struct net_sockaddr *addr, socklen_t addr_len)
    {
        /* ... Handle the incoming request ... */

        /* Return a CoAP response code as a shortcut for an empty ACK message */
        return COAP_RESPONSE_CODE_CHANGED;
    }

    static const char * const my_resource_path[] = { "test", NULL };
    COAP_RESOURCE_DEFINE(my_resource, my_service, {
        .path = my_resource_path,
        .get = my_get,
        .put = my_put,
    });

.. note::

    如上述示例所示，CoAP 资源处理函数
    可以返回响应码，
    让服务器以空 ACK 响应进行回复。

可观察（Observable）资源
********************

CoAP 服务器提供解析 observe（观察）请求的逻辑，
并使用 CoAP 服务的运行时数据
存储这些请求。
一个使用温度传感器的
示例可以如下：

.. code-block:: c

    #include <zephyr/kernel.h>
    #include <zephyr/drivers/sensor.h>
    #include <zephyr/net/coap_service.h>

    static void notify_observers(struct k_work *work);
    K_WORK_DELAYABLE_DEFINE(temp_work, notify_observers);

    static int send_temperature(struct coap_resource *resource,
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

CoAP 事件
***********

启用 :kconfig:option:`CONFIG_NET_MGMT_EVENT` 后，
用户可以注册 CoAP 事件。
以下示例仅在事件发生时打印信息。

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

CoRE 链接格式
****************

:kconfig:option:`CONFIG_COAP_SERVER_WELL_KNOWN_CORE` 选项
启用服务器对
``.well-known/core`` GET 请求的处理。
这允许客户端获取指向该服务器上
托管的其他资源的超媒体（hypermedia）链接列表。

API 参考
*************

.. doxygengroup:: coap_service
.. doxygengroup:: coap_mgmt
