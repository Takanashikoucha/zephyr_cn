.. _networking_with_ieee802154_qemu:

Networking with QEMU and IEEE 802.15.4
######################################

.. contents::
    :local:
    :depth: 2

此页面描述如何在两个通过 UART 连接并运行 IEEE 802.15.4 link layer
的 QEMU 之间设置虚拟 network。注意这仅在 Linux host 中工作。

Basic Setup
***********

以下步骤需两个 terminal windows：

* Terminal #1 为 ``echo-server`` Zephyr sample application 的 terminal window。
* Terminal #2 为 ``echo-client`` Zephyr sample application 的 terminal window。

若要捕获传输的 network data（须编译
``tools/net-tools`` directory 中的 ``monitor_15_4`` program。

打开 terminal window 并输入：

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   make monitor_15_4


Step 1 - Compile and start echo-server
======================================

Terminal #1 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :build-dir: server
   :gen-args: -DEXTRA_CONF_FILE=overlay-qemu_802154.conf
   :goals: server
   :compact:

若要捕获两个 QEMU 间的 network traffic（输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :build-dir: server
   :gen-args: -G'Unix Makefiles' -DEXTRA_CONF_FILE=overlay-qemu_802154.conf -DPCAP=capture.pcap
   :goals: server
   :compact:

注意若 command line 中设置 packet capture
option（``server`` target 须用 ``make``。``build/server/capture.pcap`` file 将包含
传输的 data。

Step 2 - Compile and start echo-client
======================================

Terminal #2 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :host-os: unix
   :board: qemu_x86
   :build-dir: client
   :gen-args: -DEXTRA_CONF_FILE=overlay-qemu_802154.conf
   :goals: client
   :compact:

应看到 data 在两个 QEMU 间传递。
按 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。
