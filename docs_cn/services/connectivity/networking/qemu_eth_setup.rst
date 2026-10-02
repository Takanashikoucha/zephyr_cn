.. _networking_with_eth_qemu:

使用 QEMU 以太网进行网络
#############################

.. contents::
    :local:
    :depth: 2

本页介绍如何在（Linux）主机与运行在 QEMU 中的 Zephyr 应用之间搭建虚拟网络。

在本示例中，Zephyr 源码发行版中的 :zephyr:code-sample:`sockets-echo-server` 示例应用会在 QEMU 中运行。Zephyr 实例通过一个在 Linux 中被建模为以太网网络接口的 tuntap 设备连接到 Linux 主机。

前提条件
*************

在 Linux 主机上，找到 Zephyr `net-tools`_ 项目。它既可以位于 Zephyr 标准安装目录下的 ``tools/net-tools`` 目录中，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools


基本设置
***********

以下步骤需要两个终端窗口：

* 终端 #1 是当前目录为 net-tools 的终端窗口（``cd net-tools``）。
* 终端 #2 是您通常使用的 Zephyr 开发终端，且已初始化 Zephyr 环境。

配置 Zephyr 实例时，必须选择用于 QEMU 连接的正确以太网驱动：

* 对于 ``qemu_x86``，选择 ``Intel(R) PRO/1000 Gigabit Ethernet driver`` 以太网驱动。该驱动在 Zephyr 源码树中称为 ``e1000``。
* 对于 ``qemu_cortex_m3``，选择 ``TI Stellaris MCU family ethernet driver`` 以太网驱动。该驱动在 Zephyr 源码树中称为 ``stellaris``。
* 对于 ``mps2_an385``，选择 ``SMSC911x/9220 Ethernet driver`` 以太网驱动。该驱动在 Zephyr 源码树中称为 ``smsc911x``。
* 对于 ``qemu_cortex_a53``，默认选择 ``Intel(R) PRO/1000 Gigabit Ethernet driver`` 以太网驱动。
* 此外，:zephyr:code-sample:`sockets-echo-server` 示例包含用于 ``qemu_x86_64`` 上 VIRTIO 网络设备的 overlay 文件。

步骤 1 - 创建以太网接口
==================================

在启动带网络连接功能的 QEMU 之前，应在主机系统中创建一个网络接口。

在终端 #1 中输入：

.. code-block:: console

   ./net-setup.sh

您可以调整 ``net-setup.sh`` 脚本的行为。按如下方式运行 ``net-setup.sh`` 即可查看各种选项：

.. code-block:: console

   ./net-setup.sh --help


步骤 2 - 在 QEMU 板卡上启动应用
================================

构建并启动 :zephyr:code-sample:`sockets-echo-server` 示例应用。本示例使用 qemu_x86 板卡。

在终端 #2 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :gen-args: -DEXTRA_CONF_FILE=overlay-e1000.conf
   :goals: run
   :compact:

或者，如果您决定在 qemu_x86_64 上使用 VIRTIO 网络设备：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86_64
   :gen-args: -DDTC_OVERLAY_FILE=virtnet.overlay -DEXTRA_CONF_FILE=overlay-virtnet.conf
   :goals: run
   :compact:

按 :kbd:`CTRL+A` 再按 :kbd:`x` 退出 QEMU。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
