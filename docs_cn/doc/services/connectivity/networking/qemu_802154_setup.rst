.. _networking_with_ieee802154_qemu:

使用 QEMU 与 IEEE 802.15.4 进行网络通信
######################################

.. contents::
    :local:
    :depth: 2

本页介绍如何在两个通过 UART 连接在一起的 QEMU 之间搭建虚拟网络，它们之间运行 IEEE 802.15.4 链路层。注意：这仅在 Linux 主机上有效。

基本设置
***********

对于下面的步骤，你需要两个终端窗口：

* 终端 #1 是运行 ``echo-server`` Zephyr 示例应用程序的终端窗口。
* 终端 #2 是运行 ``echo-client`` Zephyr 示例应用程序的终端窗口。

如果你想捕获传输的网络数据，必须编译 ``tools/net-tools`` 目录中的 ``monitor_15_4`` 程序。

打开一个终端窗口并输入：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   make monitor_15_4


步骤 1 - 编译并启动 echo-server
======================================

在终端 #1 中，输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :build-dir: server
   :gen-args: -DEXTRA_CONF_FILE=overlay-qemu_802154.conf
   :goals: server
   :compact:

如果你想捕获两个 QEMU 之间的网络流量，输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :build-dir: server
   :gen-args: -G'Unix Makefiles' -DEXTRA_CONF_FILE=overlay-qemu_802154.conf -DPCAP=capture.pcap
   :goals: server
   :compact:

注意：如果命令行中设置了数据包捕获选项，则必须使用 ``make`` 来构建 ``server`` 目标。``build/server/capture.pcap`` 文件将包含所传输的数据。

步骤 2 - 编译并启动 echo-client
======================================

在终端 #2 中，输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :host-os: unix
   :board: qemu_x86
   :build-dir: client
   :gen-args: -DEXTRA_CONF_FILE=overlay-qemu_802154.conf
   :goals: client
   :compact:

你应该能看到数据在两个 QEMU 之间传递。
按 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。
