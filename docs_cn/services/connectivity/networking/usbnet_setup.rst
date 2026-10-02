.. _usb_device_networking_setup:

USB 设备网络
#####################

.. contents::
    :local:
    :depth: 2

本页介绍如何在 Linux 主机与运行在支持 USB 的设备上的 Zephyr 应用之间搭建网络。

板卡通过 USB 线缆连接到 Linux 主机，并向主机提供一个以太网接口。Zephyr 源码发行版中的 :zephyr:code-sample:`sockets-echo-server` 应用运行在受支持的板卡上。板卡通过 USB 线缆连接到 Linux 主机，并向主机提供一个以太网接口。

基本设置
***********

要通过新建的以太网接口与 Zephyr 应用通信，需要为 Linux 主机分配 IP 地址并设置路由表。将 USB 线缆从板卡插入 Linux 主机后，``cdc_ether`` 驱动会使用提供的 MAC 地址注册一个新的以太网设备。

您可以在 Linux 主机上运行 dmesg 来检查该网络设备已创建且 MAC 地址已分配。

.. code-block:: console

   cdc_ether 1-2.7:1.0 eth0: register 'cdc_ether' at usb-0000:00:01.2-2.7, CDC Ethernet Device, 00:00:5e:00:53:01

接下来需要按下一节的说明进行设置并分配 IP 地址。

选择 IP 地址
=====================

要与板卡建立网络连接，需要为 Linux 主机上的接口选择 IP 地址。

选择与 Zephyr 应用所在子网相同的地址是有意义的。IP 地址通常在项目配置文件中设置，也可以通过以下命令从 shell 中查看。将串口终端程序（如 puTTY）连接到板卡，并向 Zephyr shell 输入以下命令：

.. code-block:: console

   shell> net iface

   Interface 0xa800e580 (Ethernet)
   ===============================
   Link addr : 00:00:5E:00:53:00
   MTU       : 1500
   IPv6 unicast addresses (max 2):
           fe80::200:5eff:fe00:5300 autoconf preferred infinite
           2001:db8::1 manual preferred infinite
   ...
   IPv4 unicast addresses (max 1):
           192.0.2.1 manual preferred infinite

此命令显示已为板卡分配了一个 IPv4 地址和两个 IPv6 地址。可根据板卡的网络配置使用 IPv4 或 IPv6 建立网络连接。

下一步是为新的 Linux 主机接口分配 IP 地址。在以下步骤中，``enx00005e005301`` 是我 Linux 系统上该接口的名称。

设置 IPv4 地址和路由
================================

.. code-block:: console

   # ip address add dev enx00005e005301 192.0.2.2
   # ip link set enx00005e005301 up
   # ip route add 192.0.2.0/24 dev enx00005e005301

设置 IPv6 地址和路由
================================

.. code-block:: console

   # ip address add dev enx00005e005301 2001:db8::2
   # ip link set enx00005e005301 up
   # ip -6 route add 2001:db8::/64 dev enx00005e005301

测试连接
******************

从主机可以使用以下命令 ping 板卡的 Zephyr IP 地址来测试连接：

.. code-block:: console

   $ ping 192.0.2.1
   PING 192.0.2.1 (192.0.2.1) 56(84) bytes of data.
   64 bytes from 192.0.2.1: icmp_seq=1 ttl=64 time=2.30 ms
   64 bytes from 192.0.2.1: icmp_seq=2 ttl=64 time=1.43 ms
   64 bytes from 192.0.2.1: icmp_seq=3 ttl=64 time=2.45 ms
   ...
