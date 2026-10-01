.. _networking_with_native_sim:

Networking with native_sim board
################################

.. contents::
    :local:
    :depth: 2

Using virtual/TAP Ethernet driver
*********************************

此段描述如何在 (Linux) host 与运行在 :zephyr:board:`native_sim <native_sim>` board 的 Zephyr application 之间设置虚拟 network。

此示例中（Zephyr source distribution 的 :zephyr:code-sample:`sockets-echo-server` sample application 在 native_sim board 中运行。Zephyr native_sim board instance 通过 Linux 中建模为 Ethernet network interface 的 tuntap device 连接到 Linux host。

Prerequisites
=============

在 Linux Host 上（找到 Zephyr `net-tools`_ project（其可在 Zephyr standard installation 的 ``tools/net-tools`` directory 下找到（或从自己的 git repository 单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools


Basic Setup
===========

以下步骤需三个 terminal windows：

* Terminal #1 为 net-tools 为当前 directory 的 terminal window（``cd net-tools``）
* Terminal #2 为常规 Zephyr development terminal（Zephyr environment 已初始化。
* Terminal #3 为运行中 Zephyr native_sim instance 的 console（可选。

Step 1 - Create Ethernet interface
----------------------------------

启动带 network 模拟的 native_sim 前（应创建 network interface。

Terminal #1 中输入：

.. code-block:: console

   ./net-setup.sh

可调整 net-setup.sh script 的行为。用如下方式运行 ``net-setup.sh`` 查看各种 options：

.. code-block:: console

   ./net-setup.sh --help


Step 2 - Start app in native_sim board
--------------------------------------

构建并启动 ``echo_server`` sample application。

Terminal #2 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: native_sim
   :goals: run
   :compact:


Step 3 - Connect to console (optional)
--------------------------------------

Zephyr instance 启动时 console window 应自动启动（但若未显示（可手动连接到 console。Native_sim board 启动时打印如下 string：

.. code-block:: console

   UART connected to pseudotty: /dev/pts/5

可手动连接：

.. code-block:: console

   screen /dev/pts/5

Using offloaded sockets
***********************

相比 `Using virtual/TAP Ethernet driver`_ 的主要优势为无需在 host machine 上设置虚拟 network interface。这意味着无需 leveraged (root) privileges。

Step 1 - Start app in native_sim board
======================================

构建并启动 ``echo_server`` sample application：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: native_sim
   :gen-args: -DEXTRA_CONF_FILE=overlay-nsos.conf
   :goals: run
   :compact:

Step 2 - run echo-client from net-tools
=======================================

在 Linux Host 上（找到 Zephyr `net-tools`_ project（其可在 Zephyr standard installation 的 ``tools/net-tools`` directory 下找到（或从自己的 git repository 单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

.. note::

   用 offloaded sockets network driver 的 Native Simulator 与任何使用 BSD sockets API 的 (Linux) application 使用相同 network interface/namespace。这意味着 :zephyr:code-sample:`sockets-echo-server` 和 ``echo-client`` applications 将通过 localhost/loopback interface（address ``127.0.0.1``）通信。

运行 UDP test 输入：

.. code-block:: console

   ./echo-client 127.0.0.1

TCP test 输入：

.. code-block:: console

   ./echo-client -t 127.0.0.1

Setting interface name and IPv4 parameters from command line
************************************************************

默认（native_sim 使用的 Ethernet interface name 由 ``zephyr,native-tap`` devicetree node 的 ``host-interface`` property 决定（但也可用 ``--eth-if=<interface_name>`` 从 command line 设置。

相同适用于 IPv4 address、gateway 和 netmask。其可用 ``--ipv4-addr=<ip_address>``、``--ipv4-gw=<gateway>`` 和 ``--ipv4-nm=<netmask>`` 从 command line 设置。

这些 options 应用于第一个 interface。定义多个 ``zephyr,native-tap`` interfaces 时（每个额外 interface 有其自己的 per-interface options（以 devicetree node name 为 prefix（如 ``--<node>_eth-if`` 和 ``--<node>_ipv4-addr``。

注意 configuration :kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_ADDR` 和 command line arguments 并行工作。这意味着若两者均设置（interface 可能最终有两个 IP addresses。大多数情况下（同时仅使用两者之一有意义。

若 application 须运行多个 instances（且为每个 instance 重新编译麻烦（此有用。

.. code-block:: console

   ./zephyr.exe --eth-if=zeth2 --ipv4-addr=192.0.2.2 --ipv4-gw=192.0.0.1
   --ipv4-nm=255.255.0.0

.. note::

   这些 command line options 也可在 build time 通过 :kconfig:option:`CONFIG_NATIVE_EXTRA_CMDLINE_ARGS` configuration option 提供。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
