.. _latmon:

Latmon Network Service
######################

.. contents::
    :local:
    :depth: 2

Overview
********

提供基于 network 的 latency monitoring 所需的功能（包括 socket 管理、client-server 通信（以及与被测系统（SUT）上运行的 Latmus service 的数据交换。

Latmon network service 负责建立并管理 Latmon application（运行在基于 Zephyr 的 board 上）与 Latmus service（运行在 SUT 上）之间的 network 通信。

其用 TCP sockets 进行可靠通信（用 UDP sockets 广播 Latmon device 的 IP address。

API Reference
*************

.. doxygengroup:: latmon

Features
********

- **Socket Management**：创建并管理用于通信的 TCP 和 UDP sockets。
- **Client-Server Communication**：处理来自 Latmus service 的 incoming connections。
- **Data Exchange**：向 Latmus service 发送 latency metrics 和 histogram data。
- **IP Address Broadcasting**：广播 Latmon device 的 IP address 以方便 Latmus service 发现。
- **Thread-Safe Design**：使用 Zephyr 的 kernel primitives（如 message queues 和 semaphores）进行同步。

Workflow
********

Socket Creation
===============

调用 :c:func:`net_latmon_get_socket()` function 创建并配置与 Latmus service 通信的 TCP socket。可指定 connection address 作为参数以将 socket 绑定到特定 interface 和 port。

Connection Handling
===================

:c:func:`net_latmon_connect()` function 等待来自 Latmus service 的 connection。若在 timeout period 内未收到 connection（service 用 UDP 广播其 IP address（并返回 ``-EAGAIN``。若 broadcast request 无法发送（function 返回 ``-1``（且 client 应退出。

Monitoring Start
================

一旦 connection 建立（调用 :c:func:`net_latmon_start()` function 启动 monitoring process。此 function 用 callback 计算 latency deltas（并将 data 发送到 Latmus service。

Monitoring Status
=================

:c:func:`net_latmon_running()` function 可用于检查 monitoring process 是否 active。

Thread Management
=================

Service 用 Zephyr threads 处理 incoming connections（并管理 monitoring process。

Enabling the Latmon Service
***************************

以下 configuration option 须在 :file:`prj.conf` 文件中启用。

- :kconfig:option:`CONFIG_NET_LATMON`

以下 options 可配置以定制 Latmon service：

- :kconfig:option:`CONFIG_NET_LATMON_PORT` - Latmon service 的 port 号。
- :kconfig:option:`CONFIG_NET_LATMON_XFER_THREAD_STACK_SIZE`
- :kconfig:option:`CONFIG_NET_LATMON_XFER_THREAD_PRIORITY`
- :kconfig:option:`CONFIG_NET_LATMON_THREAD_STACK_SIZE`
- :kconfig:option:`CONFIG_NET_LATMON_THREAD_PRIORITY`
- :kconfig:option:`CONFIG_NET_LATMON_MONITOR_THREAD_STACK_SIZE`
- :kconfig:option:`CONFIG_NET_LATMON_MONITOR_THREAD_PRIORITY`

Example Usage
*************

.. code-block:: c

    #include <zephyr/net/latmon.h>
    #include <zephyr/net/socket.h>

    void main(void)
    {
        struct in_addr ip;
        int server_socket, client_socket;

        /* Create and configure the server socket */
        server_socket = net_latmon_get_socket(NULL);

        while (1) {
            /* Wait for a connection from the Latmus service */
            client_socket = net_latmon_connect(server_socket, &ip);
            if (client_socket < 0) {
                if (client_socket == -EAGAIN) {
                    continue;
                }
                goto out;
            }

            /* Start the latency monitoring process */
            net_latmon_start(client_socket, measure_latency_cycles);
        }
    out:
        close(server_socket);
    }
