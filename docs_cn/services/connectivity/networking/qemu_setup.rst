.. _networking_with_qemu:

使用 QEMU 进行网络
####################

.. contents::
    :local:
    :depth: 2

本页介绍如何在（Linux）主机与运行在 QEMU 虚拟机（面向 qemu_x86 和 qemu_cortex_m3 等 Zephyr 目标构建）中的 Zephyr 应用之间搭建虚拟网络。某些虚拟 ARM 板卡（如 qemu_cortex_a53）仅支持单个 UART，此时建议优先使用 QEMU 以太网，详情参见 :ref:`networking_with_eth_qemu`。

在本示例中，Zephyr 源码发行版中的 :zephyr:code-sample:`sockets-echo-server` 示例应用会在 QEMU 中运行。QEMU 实例通过串口连接到 Linux 主机，并使用 SLIP 在 Zephyr 应用与 Linux 之间传输数据（经过一串虚拟连接）。

前提条件
*************

在 Linux 主机上，找到 Zephyr `net-tools`_ 项目。它既可以位于 Zephyr 标准安装目录下的 ``tools/net-tools`` 目录中，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   sudo apt install -y socat libpcap-dev
   git clone https://github.com/zephyrproject-rtos/net-tools
   cd net-tools
   make

.. note::

   如果出现与 AX_CHECK_COMPILE_FLAG 相关的错误，请在 Debian/Ubuntu 上安装 ``autoconf-archive`` 软件包。

基本设置
***********

以下步骤至少需要 4 个终端窗口：

* 终端 #1 是您通常使用的 Zephyr 开发终端，且已初始化 Zephyr 环境。
* 终端 #2、#3 和 #4 是当前目录为 net-tools 的终端窗口（``cd net-tools``）。

步骤 1 - 创建辅助套接字
=============================

在启动带网络模拟的 QEMU 之前，应为模拟创建一个 Unix 套接字。

在终端 #2 中输入：

.. code-block:: console

   ./loop-socat.sh

步骤 2 - 启动 TAP 设备路由守护进程
========================================

在终端 #3 中输入：


.. code-block:: console

   sudo ./loop-slip-tap.sh

对于需要 DNS 的应用，您可能需要在此处按 :ref:`networking_internet` 中的说明重启主机的 DNS 服务器。

步骤 3 - 在 QEMU 中启动应用
=========================

构建并启动 ``echo_server`` 示例应用。

在终端 #1 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

如果您看到 QEMU 报出关于 unix:/tmp/slip.sock 的错误，说明您遗漏了上述步骤 1。

步骤 4 - 在主机上运行应用
=========================

现在在终端 #4 中，您可以运行各种工具来与运行在 QEMU 中的应用通信。

可以从 ping 开始：

.. code-block:: console

   ping 192.0.2.1
   ping6 2001:db8::1

您可以使用 netcat（"nc"）工具，通过 UDP 连接：

.. code-block:: console

   echo foobar | nc -6 -u 2001:db8::1 4242
   foobar

.. code-block:: console

   echo foobar | nc -u 192.0.2.1 4242
   foobar

如果 echo_server 编译时启用了 TCP 支持（当前 echo_server 示例默认启用，CONFIG_NET_TCP=y）：

.. code-block:: console

   echo foobar | nc -6 -q2 2001:db8::1 4242
   foobar

.. note::

   使用 Ctrl+C 退出。

您也可以使用 telnet 命令实现上述功能。

步骤 5 - 停止辅助守护进程
===============================

完成使用 QEMU 的网络测试后，应停止初始步骤中启动的任何守护进程或辅助程序，以避免可能出现的网络或路由问题（例如本地网络接口中的地址冲突）。例如，当您从 QEMU 网络测试切换到使用真实硬件，或者要把主机笔记本恢复为正常 Wi-Fi 使用时，就应停止它们。

要停止守护进程，请在相应终端窗口中按 Ctrl+C（需要同时停止 ``loop-slip-tap.sh`` 和 ``loop-socat.sh``）。

按 :kbd:`CTRL+A` 再按 :kbd:`x` 退出 QEMU。

.. _networking_internet:

配置 Zephyr 以及主机上的 NAT/伪装以访问互联网
*****************************************************************

要从 Zephyr 应用访问互联网，可能需要在主机上做一些额外设置。对于运行在 QEMU 中和运行在真实硬件上的应用，此设置是通用的，前提是开发板已连接到开发主机。如果板卡连接到专用路由器，则不需要此设置。

要从 Zephyr 应用使用 IPv4 访问互联网，应通过 DHCP 设置或手动配置网关。对于使用“设置”机制（启用配置选项 :kconfig:option:`CONFIG_NET_CONFIG_SETTINGS`）的应用，将 :kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_GW` 选项设置为网关的 IP 地址。对于不使用“设置”机制的应用，在运行时调用 :c:func:`net_if_ipv4_set_gw` 来设置网关。例如：``CONFIG_NET_CONFIG_MY_IPV4_GW="192.0.2.2"``

要从运行在 QEMU 中的自定义应用访问互联网，应为 QEMU 的源地址设置 NAT（伪装）。假设使用 ``192.0.2.1``，且 Zephyr 网络接口为 ``zeth``，则以下命令应以 root 身份运行：

.. code-block:: console

   iptables -t nat -A POSTROUTING -j MASQUERADE -s 192.0.2.1/24
   iptables -I FORWARD 1 -i zeth -j ACCEPT
   iptables -I FORWARD 1 -o zeth -m state --state RELATED,ESTABLISHED -j ACCEPT

此外，应在主机上启用 IPv4 转发，并且您可能需要检查其他防火墙（iptables）规则是否会干扰伪装。要启用 IPv4 转发，以下命令应以 root 身份运行：

.. code-block:: console

   sysctl -w net.ipv4.ip_forward=1

某些应用可能还需要 DNS 服务器。许多 Zephyr 提供的示例默认假设主机上（IP 为 ``192.0.2.2``）有可用的 DNS 服务器；在现代 Linux 发行版中，主机通常至少运行一个 DNS 代理。使用 QEMU 运行时，可能需要重启主机的 DNS 服务，使其能够为新建 TAP 接口上的请求提供服务。例如，在基于 Debian 的系统上：

.. code-block:: console

   service dnsmasq restart

依赖主机 DNS 服务器的替代方案是使用网络中的一个 DNS 服务器。例如，``8.8.8.8`` 是一个公开可用的 DNS 服务器。您可以使用 :kconfig:option:`CONFIG_DNS_SERVER1` 选项来配置它。


两个 QEMU 虚拟机之间的网络连接
***************************************

与上述虚拟机到主机的设置不同，虚拟机到虚拟机的设置是自动完成的。对于支持此模式的示例应用（如 echo_server 和 echo_client 示例），您需要两个为 Zephyr 开发设置好的终端窗口。

终端 #1：
============

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :goals: build
   :build-args: server
   :compact:

这将启动 QEMU，等待来自客户端 QEMU 的连接。

终端 #2：
============

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :host-os: unix
   :board: qemu_x86
   :goals: build
   :build-args: client
   :compact:

这将启动第二个 QEMU 实例，您应能在两边看到发送和接收数据的日志。

运行同一示例的多个 QEMU 虚拟机
********************************************

如果您想运行同一 Zephyr 示例应用的多个实例，且它们之间不需要相互通信，请使用 ``QEMU_INSTANCE`` 参数。

手动启动 ``socat`` 和 ``tunslip6``（而不是使用 ``loop-xxx.sh`` 脚本），数量按您的需要而定。以下命令供参考，请将 MAIN 或 OTHER 替换为您自己的标识。

终端 #1：
============

.. code-block:: console

   socat PTY,link=/tmp/slip.devMAIN UNIX-LISTEN:/tmp/slip.sockMAIN &
   sudo $ZEPHYR_BASE/../tools/net-tools/tunslip6 -t tapMAIN -T -s /tmp/slip.devMAIN 2001:db8::1/64 &
   # Now run Zephyr
   make -Cbuild run QEMU_INSTANCE=MAIN

终端 #2：
============

.. code-block:: console

   socat PTY,link=/tmp/slip.devOTHER UNIX-LISTEN:/tmp/slip.sockOTHER &
   sudo $ZEPHYR_BASE/../tools/net-tools/tunslip6 -t tapOTHER -T -s /tmp/slip.devOTHER 2001:db8::1/64 &
   make -Cbuild run QEMU_INSTANCE=OTHER

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
