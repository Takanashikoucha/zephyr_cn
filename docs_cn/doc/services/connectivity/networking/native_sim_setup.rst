.. _networking_with_native_sim:

使用 native_sim 单板进行网络通信
################################

.. contents::
    :local:
    :depth: 2

使用虚拟/TAP 以太网驱动程序
*********************************

本段介绍如何在（Linux）主机与运行在 :zephyr:board:`native_sim <native_sim>` 单板上的 Zephyr 应用程序之间搭建虚拟网络。

在本示例中，Zephyr 源码发行版中的 :zephyr:code-sample:`sockets-echo-server` 示例应用程序在 native_sim 单板上运行。Zephyr native_sim 单板实例通过一个 tuntap 设备连接到 Linux 主机，该设备在 Linux 中被建模为一个以太网网络接口。

前提条件
=============

在 Linux 主机上，找到 Zephyr 的 `net-tools`_ 项目，它既可以在 Zephyr 标准安装中的 ``tools/net-tools`` 目录下找到，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools


基本设置
===========

对于下面的步骤，你需要三个终端窗口：

* 终端 #1 是当前目录为 net-tools 的终端窗口（``cd net-tools``）
* 终端 #2 是你通常使用的 Zephyr 开发终端，
  已初始化 Zephyr 环境。
* 终端 #3 是连接到正在运行的 Zephyr native_sim
  实例的控制台（可选）。

步骤 1 - 创建以太网接口
----------------------------------

在启动带网络仿真的 native_sim 之前，应先创建一个网络接口。

在终端 #1 中，输入：

.. code-block:: console

   ./net-setup.sh

你可以调整 net-setup.sh 脚本的行为。通过如下方式运行 ``net-setup.sh`` 查看各种选项：

.. code-block:: console

   ./net-setup.sh --help


步骤 2 - 在 native_sim 单板上启动应用程序
--------------------------------------

构建并启动 ``echo_server`` 示例应用程序。

在终端 #2 中，输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: native_sim
   :goals: run
   :compact:


步骤 3 - 连接到控制台（可选）
--------------------------------------

当 Zephyr 实例启动时，控制台窗口应会自动启动，但如果它没有显示出来，你可以手动连接到控制台。native_sim 单板启动时会打印如下字符串：

.. code-block:: console

   UART connected to pseudotty: /dev/pts/5

你可以如下手动连接到它：

.. code-block:: console

   screen /dev/pts/5

使用卸载套接字
***********************

与 `使用虚拟/TAP 以太网驱动程序`_ 相比，主要优势是不需要在主机上设置虚拟网络接口。这意味着不需要提升（root）权限。

步骤 1 - 在 native_sim 单板上启动应用程序
======================================

构建并启动 ``echo_server`` 示例应用程序：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: native_sim
   :gen-args: -DEXTRA_CONF_FILE=overlay-nsos.conf
   :goals: run
   :compact:

步骤 2 - 从 net-tools 运行 echo-client
======================================

在 Linux 主机上，找到 Zephyr 的 `net-tools`_ 项目，它既可以在 Zephyr 标准安装中的 ``tools/net-tools`` 目录下找到，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

.. note::

   使用卸载套接字网络驱动程序的 Native Simulator 与任何使用 BSD
   套接字 API 的其他（Linux）应用程序使用相同的网络接口/命名空间。这意味着 :zephyr:code-sample:`sockets-echo-server` 和
   ``echo-client`` 应用程序将通过 localhost/loopback
   接口（地址 ``127.0.0.1``）进行通信。

要运行 UDP 测试，输入：

.. code-block:: console

   ./echo-client 127.0.0.1

要运行 TCP 测试，输入：

.. code-block:: console

   ./echo-client -t 127.0.0.1

从命令行设置接口名称和 IPv4 参数
************************************************************

默认情况下，native_sim 使用的以太网接口名称由 ``zephyr,native-tap`` devicetree 节点的 ``host-interface`` 属性决定，但也可以使用 ``--eth-if=<interface_name>`` 从命令行设置。

同样适用于 IPv4 地址、网关和子网掩码。可以使用 ``--ipv4-addr=<ip_address>``、``--ipv4-gw=<gateway>`` 和 ``--ipv4-nm=<netmask>`` 从命令行设置它们。

这些选项适用于第一个接口。当定义了多个 ``zephyr,native-tap`` 接口时，每个附加接口都有自己按接口划分的选项，以 devicetree 节点名称作为前缀，例如 ``--<node>_eth-if`` 和 ``--<node>_ipv4-addr``。

注意：配置 :kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_ADDR` 和命令行参数是并行工作的。这意味着如果两者都设置，接口最终可能拥有两个 IP 地址。在大多数情况下，同时只使用其中之一是有意义的。

当应用程序必须以多个实例运行，而为每个实例重新编译会很麻烦时，这会有用。

.. code-block:: console

   ./zephyr.exe --eth-if=zeth2 --ipv4-addr=192.0.2.2 --ipv4-gw=192.0.0.1
   --ipv4-nm=255.255.0.0

.. note::

   这些命令行选项也可以在构建时通过 :kconfig:option:`CONFIG_NATIVE_EXTRA_CMDLINE_ARGS` 配置选项提供。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
