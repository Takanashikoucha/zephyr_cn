.. _coap_sock_interface:

CoAP
#####

.. contents::
    :local:
    :depth: 2

概述
********

Constrained Application Protocol（CoAP，受限应用协议）
是一种专用的 Web 传输协议，
用于受限节点和受限（例如低功耗、
有损）网络。它为支持 CoAP 特性的
RESTful Web 服务提供了便捷的 API。
有关协议本身的更多信息，参见 :rfc:`7252`。

Zephyr 提供了一个 CoAP 库，支持客户端和服务器角色。
该库可通过 :kconfig:option:`CONFIG_COAP` Kconfig 选项启用，
并可按用户需求进行配置。Zephyr CoAP 库
使用普通缓冲区实现。API 的使用者创建
用于通信的套接字，并将缓冲区
传递给库进行解析等用途。
库本身不会为用户创建任何套接字。

在 CoAP 之上，Zephyr 还支持 LwM2M（"Lightweight Machine 2 Machine"，
轻量级机器对机器）协议，
一种简单、低成本的远程管理与服务使能机制。
更多信息参见 :ref:`lwm2m_interface`。

支持的 RFC：

- :rfc:`7252` - The Constrained Application Protocol (CoAP)
- :rfc:`6690` - Constrained RESTful Environments (CoRE) Link Format
- :rfc:`7959` - Block-Wise Transfers in the Constrained Application Protocol (CoAP)
- :rfc:`7641` - Observing Resources in the Constrained Application Protocol (CoAP)
- :rfc:`8613` - Object Security for Constrained RESTful Environments (OSCORE)

.. note:: 这些 RFC 并非所有部分都受支持。特性按 Zephyr 的需求支持。

Zephyr CoAP 库还支持 Object Security for Constrained RESTful
Environments（OSCORE），规范见 :rfc:`8613`。
更多信息参见 :ref:`coap_oscore_interface`。

示例用法
************

CoAP 服务器
===========

.. note::

    有 :ref:`coap_server_interface` 子系统可用，
    以下内容为创建自定义
    服务器实现。

要创建 CoAP 服务器，需要先定义
服务器的资源。``.well-known/core`` 资源
应在所有应包含在 ``.well-known/core``
资源响应中的其他资源之前添加。

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

应用从套接字读取数据，并将缓冲区
传递给 CoAP 库以解析消息。
如果 CoAP 消息格式正确，库会
使用该缓冲区连同上述定义的资源，
调用正确的回调函数
来处理来自客户端的 CoAP 请求。
由回调函数负责
按 CoAP 请求进行回复或执行相应操作。

.. code-block:: c

    coap_packet_parse(&request, data, data_len, options, opt_num);
    ...
    coap_handle_request(&request, resources, options, opt_num,
                        client_addr, client_addr_len);

如果启用了 :kconfig:option:`CONFIG_COAP_URI_WILDCARD`，
服务器可使用类 MQTT 通配符风格
接受多个资源：

- 加号（plus）符号代表路径中的单级通配符；
- 井号（hash）符号代表路径中的多级通配符。

.. code-block:: c

    static const char * const led_set[] = { "led","+","set", NULL };
    static const char * const btn_get[] = { "button","#", NULL };
    static const char * const no_wc[] = { "test","+1", NULL };

它接受 /led/0/set、led/1234/set、led/any/set、/button/door/1、/test/+1，
但对 /led/1、/test/21、/test/1 返回 -ENOENT。

该选项默认启用。如需避免
类似 '/some_resource/+/#' 的资源路径
带来的意外行为，可将其禁用。

CoAP 客户端
===========

.. note::

    有 :ref:`coap_client_interface` 子系统可用，
    以下内容为创建自定义
    客户端实现。

如果 CoAP 客户端了解 CoAP 服务器中的资源，
客户端即可开始
准备 CoAP 请求并等待响应。
如果客户端不了解
CoAP 服务器中的资源，
它可以通过
``.well-known/core`` CoAP 消息请求资源。

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

测试
*******

测试 Zephyr CoAP 库有多种方式。

libcoap
=======
libcoap 为资源受限的设备（例如受
计算能力、射频范围、内存、带宽
或网络数据包大小限制）实现了一种
轻量级应用协议。源码可在 `libcoap <https://github.com/obgm/libcoap>`_ 找到。
libcoap 有一个脚本（``examples/etsi_coaptest.sh``）
用于测试 Zephyr 中的 coap-server 功能。

更多细节参见 `net-tools <https://github.com/zephyrproject-rtos/net-tools>`_ 项目。

:zephyr:code-sample:`coap-server` 示例可按
:ref:`networking_with_qemu` 的描述
在 QEMU 上构建并运行。

在主机上使用以下命令
运行 libcoap 实现的
ETSI 测试用例：

.. code-block:: console

   sudo ./libcoap/examples/etsi_coaptest.sh -i tap0 2001:db8::1

TTCN3
=====
Eclipse 提供了基于 TTCN3 的测试，
可用于针对 CoAP 实现运行。

安装 eclipse-titan，并为 titan 工具设置符号链接

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

按照以下来源的说明设置 CoAP 测试套件：

- https://gitlab.eclipse.org/eclipse/titan/titan.misc
- https://gitlab.eclipse.org/eclipse/titan/titan.misc/-/tree/master/CoAP_Conf

构建完成后，:zephyr:code-sample:`coap-server` 示例即可按
:ref:`networking_with_qemu` 的描述
在 QEMU 上构建并运行。

按您的环境，
在 coap.cfg 文件中更改客户端（测试套件）
和服务器（Zephyr coap-server 示例）的地址。

使用以下命令执行测试用例。

.. code-block:: console

   ttcn3_start coaptests coap.cfg

ttcn3 测试的示例输出如下。

.. code-block:: console

   Verdict statistics: 0 none (0.00 %), 10 pass (100.00 %), 0 inconc (0.00 %), 0 fail (0.00 %), 0 error (0.00 %).
   Test execution summary: 10 test cases were executed. Overall verdict: pass

API 参考
*************

.. doxygengroup:: coap
