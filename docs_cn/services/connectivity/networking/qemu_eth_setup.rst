.. _networking_with_eth_qemu:

Networking with QEMU Ethernet
#############################

.. contents::
    :local:
    :depth: 2

此页面描述如何在 (Linux) host 与运行在 QEMU 的 Zephyr application 之间设置虚拟 network。

此示例中（Zephyr source distribution 的 :zephyr:code-sample:`sockets-echo-server` sample application 在 QEMU 中运行。Zephyr instance
通过 Linux 中建模为
Ethernet network interface 的 tuntap device 连接到 Linux host。

Prerequisites
*************

在 Linux Host 上（找到 Zephyr `net-tools`_ project（其可在 Zephyr standard installation 的 ``tools/net-tools`` directory 下找到（或从自己的 git repository 单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools


Basic Setup
***********

以下步骤需两个 terminal windows：

* Terminal #1 为 net-tools 为当前
  directory 的 terminal window（``cd net-tools``）
* Terminal #2 为常规 Zephyr development terminal（
  Zephyr environment 已初始化。

配置 Zephyr instance 时（须为 QEMU connectivity 选择正确 Ethernet
driver：

* 对 ``qemu_x86``（选择 ``Intel(R) PRO/1000 Gigabit Ethernet driver``
  Ethernet driver。Driver 在 Zephyr source tree 中名为 ``e1000``。
* 对 ``qemu_cortex_m3``（选择 ``TI Stellaris MCU family ethernet driver``
  Ethernet driver。Driver 在 Zephyr source tree 中名为 ``stellaris``。
* 对 ``mps2_an385``（选择 ``SMSC911x/9220 Ethernet driver`` Ethernet driver。
  Driver 在 Zephyr source tree 中名为 ``smsc911x``。
* 对 ``qemu_cortex_a53``（默认选择 ``Intel(R) PRO/1000 Gigabit Ethernet driver``
  Ethernet driver。
* 另外（:zephyr:code-sample:`sockets-echo-server` sample 包含
  ``qemu_x86_64`` 上 VIRTIO Network device 的
  overlay files。

Step 1 - Create Ethernet interface
==================================

启动带 network connectivity 的 QEMU 前（host system 中
应创建 network interface。

Terminal #1 中输入：

.. code-block:: console

   ./net-setup.sh

可调整 ``net-setup.sh`` script 的行为。用如下方式运行 ``net-setup.sh`` 查看各种 options：

.. code-block:: console

   ./net-setup.sh --help


Step 2 - Start app in QEMU board
================================

构建并启动 :zephyr:code-sample:`sockets-echo-server` sample application。
此示例中（使用 qemu_x86 board。

Terminal #2 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :gen-args: -DEXTRA_CONF_FILE=overlay-e1000.conf
   :goals: run
   :compact:

或者（若决定在 qemu_x86_64 上使用 VIRTIO Network device：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86_64
   :gen-args: -DDTC_OVERLAY_FILE=virtnet.overlay -DEXTRA_CONF_FILE=overlay-virtnet.conf
   :goals: run
   :compact:

按 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
