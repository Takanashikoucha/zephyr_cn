.. _coap_sock_interface:

CoAP
#####

.. contents::
    :local:
    :depth: 2

Overview
********

Constrained Application Protocol（CoAP）是用于 constrained nodes 和 constrained（如低功耗、lossy）networks 的专用 web transfer protocol。其为支持 CoAP features 的 RESTful Web services 提供便利 API。协议本身更多信息参见 :rfc:`7252`。

Zephyr 提供支持 client 和 server roles 的 CoAP library。库可用 :kconfig:option:`CONFIG_COAP` Kconfig option 启用（且可按 user 需求配置。Zephyr CoAP library 用 plain buffers 实现。API 的 users 创建 sockets 以通信（并将 buffer 传递给 library 以解析和其他目的。Library 本身不为 users 创建任何 sockets。

CoAP 之上（Zephyr 支持 LwM2M "Lightweight Machine 2 Machine" protocol（简单、低成本的 remote management 和 service enablement 机制。更多信息参见 :ref:`lwm2m_interface`。

Supported RFCs：

- :rfc:`7252` - The Constrained Application Protocol（CoAP）
- :rfc:`6690` - Constrained RESTful Environments（CoRE）Link Format
- :rfc:`7959` - Block-Wise Transfers in the Constrained Application Protocol（CoAP）
- :rfc:`7641` - Observing Resources in the Constrained Application Protocol（CoAP）
- :rfc:`8613` - Object Security for Constrained RESTful Environments（OSCORE）

.. note:: 这些 RFCs 并非所有部分均支持。Features 按 Zephyr 需求支持。

Zephyr CoAP library 还支持按 :rfc:`8613` 指定的 Object Security for Constrained RESTful Environments（OSCORE）。更多信息参见 :ref:`coap_oscore_interface`。

Sample Usage
************

CoAP Server
===========

.. note::

   有 :ref:`coap_server_interface` subsystem 可用（以下为创建 custom server 实现。

要创建 CoAP server（须定义 server 的 resources。``.well-known/core`` resource 应在所有应包含在 ``.well-known/core`` resource 的 responses 中的其他 resources 之前添加。

.. code-block:: c

    static struct coap_resource resources[] = {
        { .get = well_known_core_get,
          .path = COAP_WELL_KNOWN_CORE_PATH,
        },
        { .get  = sample_get,
          .post = sample_post,
          .del  = sample_del,
          .put  = sample_put,
          .path = sample_path
        },
        { },
    };

Application 从 socket 读取 data（并将 buffer 传递给 CoAP library 以解析 message。若 CoAP message 适当（library 用 buffer 连同上述定义的 resources 调用正确的 callback function 以处理来自 client 的 CoAP request。Callback function 负责按 CoAP request 回复或行动。

.. code-block:: c

    coap_packet_parse(&request, data, data_len, options, opt_num);
    ...
    coap_handle_request(&request, resources, options, opt_num,
                        client_addr, client_addr_len);

若启用 :kconfig:option:`CONFIG_COAP_URI_WILDCARD`（server 可用 MQTT-like wildcard style 接受多个 resources：

- plus symbol 代表 path 中的 single-level wild card；
- hash symbol 代表 path 中的 multi-level wild card。

.. code-block:: c

    static const char * const led_set[] = { "led","+","set", NULL };
    static const char * const btn_get[] = { "button","#", NULL };
    static const char * const no_wc[] = { "test","+1", NULL };

其接受 /led/0/set、led/1234/set、led/any/set、/button/door/1、/test/+1（但对 /led/1、/test/21、/test/1 返回 -ENOENT。

此 option 默认启用（禁用它以避免 resource path 如 '/some_resource/+/#' 的意外行为。

CoAP Client
===========

.. note::

   有 :ref:`coap_client_interface` subsystem 可用（以下为创建 custom client 实现。

若 CoAP client 了解 CoAP server 中的 resources（client 可开始准备 CoAP requests 并等待 responses。若 client 不了解 CoAP server 中的 resources（其可通过 ``.well-known/core`` CoAP message 请求 resources。

.. code-block:: c

    /* Initialize the CoAP message */
    char *path = "test";
    struct coap_packet request;
    uint8_t data[100];
    uint8_t payload[20];

    coap_packet_init(&request, data, sizeof(data),
                     1, COAP_TYPE_CON, 8, coap_next_token(),
                     COAP_METHOD_GET, coap_next_id());

    /* Append options */
    coap_packet_append_option(&request, COAP_OPTION_URI_PATH,
                              path, strlen(path));

    /* Append Payload marker if you are going to add payload */
    coap_packet_append_payload_marker(&request);

    /* Append payload */
    coap_packet_append_payload(&request, (uint8_t *)payload,
                               sizeof(payload) - 1);

    /* send over sockets */

Testing
*******

有多种方式测试 Zephyr CoAP library。

libcoap
=======
libcoap 为 resource constrained 的 devices（如受 computing power、RF range、memory、bandwidth 或 network packet sizes 限制）实现轻量级 application-protocol。Sources 可在 `libcoap <https://github.com/obgm/libcoap>`_ 找到。libcoap 有 script（``examples/etsi_coaptest.sh``）测试 Zephyr 中的 coap-server 功能。

更多细节参见 `net-tools <https://github.com/zephyrproject-rtos/net-tools>`_ project。

:zephyr:code-sample:`coap-server` sample 可按 :ref:`networking_with_qemu` 描述在 QEMU 上构建并执行。

在 host 上用此命令运行 libcoap 实现的 ETSI test cases：

.. code-block:: console

   sudo ./libcoap/examples/etsi_coaptest.sh -i tap0 2001:db8::1

TTCN3
=====
Eclipse 有基于 TTCN3 的 tests 以针对 CoAP 实现运行。

安装 eclipse-titan（并为 titan tools 设置 symbolic links：

.. code-block:: console

    sudo apt-get install eclipse-titan

    cd /usr/share/titan

    sudo ln -s /usr/bin bin
    sudo ln /usr/bin/titanver bin
    sudo ln -s /usr/bin/mctr_cli bin
    sudo ln -s /usr/include/titan include
    sudo ln -s /usr/lib/titan lib

    export TTCN3_DIR=/usr/share/titan

    git clone https://gitlab.eclipse.org/eclipse/titan/titan.misc.git

    cd titan.misc

按此处的说明设置 CoAP test suite：

- https://gitlab.eclipse.org/eclipse/titan/titan.misc
- https://gitlab.eclipse.org/eclipse/titan/titan.misc/-/tree/master/CoAP_Conf

构建完成后（:zephyr:code-sample:`coap-server` sample 可按 :ref:`networking_with_qemu` 描述在 QEMU 上构建并执行。

按您的 setup 在 coap.cfg 文件中更改 client（test suite）和 server（Zephyr coap-server sample）addresses。

用以下命令执行 test cases。

.. code-block:: console

   ttcn3_start coaptests coap.cfg

ttcn3 tests 的示例输出如下。

.. code-block:: console

   Verdict statistics: 0 none (0.00 %), 10 pass (100.00 %), 0 inconc (0.00 %), 0 fail (0.00 %), 0 error (0.00 %).
   Test execution summary: 10 test cases were executed. Overall verdict: pass

API Reference
*************

.. doxygengroup:: coap
