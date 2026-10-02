.. _latmon:

Latmon 网络服务
######################

.. contents::
    :local:
    :depth: 2

概述
********

提供基于网络的延迟监控所需的功能，包括套接字管理、客户端-服务器通信，以及与被测系统（SUT）上运行的 Latmus 服务的数据交换。

Latmon 网络服务负责建立并管理 Latmon 应用（运行在基于 Zephyr 的板卡上）与 Latmus 服务（运行在 SUT 上）之间的网络通信。

它使用 TCP 套接字进行可靠通信，并使用 UDP 套接字广播 Latmon 设备的 IP 地址。

API 参考
*************

.. doxygengroup:: latmon

功能
********

- **套接字管理**：创建并管理用于通信的 TCP 和 UDP 套接字。
- **客户端-服务器通信**：处理来自 Latmus 服务的传入连接。
- **数据交换**：向 Latmus 服务发送延迟指标和直方图数据。
- **IP 地址广播**：广播 Latmon 设备的 IP 地址，以便 Latmus 服务发现该设备。
- **线程安全设计**：使用 Zephyr 的内核原语（如消息队列和信号量）进行同步。

工作流程
********

套接字创建
==============

调用 :c:func:`net_latmon_get_socket()` 函数创建并配置用于与 Latmus 服务通信的 TCP 套接字。可以指定连接地址作为参数，将套接字绑定到特定接口和端口。

连接处理
===================

:c:func:`net_latmon_connect()` 函数等待来自 Latmus 服务的连接。如果在超时时间内未收到连接，该服务将使用 UDP 广播其 IP 地址并返回 ``-EAGAIN``。如果广播请求无法发送，该函数返回 ``-1``，客户端应退出。

监控启动
================

一旦连接建立，调用 :c:func:`net_latmon_start()` 函数启动监控流程。该函数使用回调计算延迟差值，并将数据发送到 Latmus 服务。

监控状态
=================

:c:func:`net_latmon_running()` 函数可用于检查监控流程是否正在运行。

线程管理
==================

该服务使用 Zephyr 线程处理传入连接并管理监控流程。

启用 Latmon 服务
***************************

以下配置选项必须在 :file:`prj.conf` 文件中启用。

- :kconfig:option:`CONFIG_NET_LATMON`

以下选项可配置以定制 Latmon 服务：

- :kconfig:option:`CONFIG_NET_LATMON_PORT` - Latmon 服务的端口号。
- :kconfig:option:`CONFIG_NET_LATMON_XFER_THREAD_STACK_SIZE`
- :kconfig:option:`CONFIG_NET_LATMON_XFER_THREAD_PRIORITY`
- :kconfig:option:`CONFIG_NET_LATMON_THREAD_STACK_SIZE`
- :kconfig:option:`CONFIG_NET_LATMON_THREAD_PRIORITY`
- :kconfig:option:`CONFIG_NET_LATMON_MONITOR_THREAD_STACK_SIZE`
- :kconfig:option:`CONFIG_NET_LATMON_MONITOR_THREAD_PRIORITY`

使用示例
*************

.. code-block:: c

    #include <zephyr/net/latmon.h>
    #include <zephyr/net/socket.h>

    void main(void)
    {
        struct in_addr ip;
        int server_socket, client_socket;

        /* 创建并配置服务器套接字 */
        server_socket = net_latmon_get_socket(NULL);

        while (1) {
            /* 等待来自 Latmus 服务的连接 */
            client_socket = net_latmon_connect(server_socket, &ip);
            if (client_socket < 0) {
                if (client_socket == -EAGAIN) {
                    continue;
                }
                goto out;
            }

            /* 启动延迟监控流程 */
            net_latmon_start(client_socket, measure_latency_cycles);
        }
    out:
        close(server_socket);
    }
