.. _usb_device_networking_setup:

USB Device Networking
#####################

.. contents::
    :local:
    :depth: 2

此页面描述如何在 Linux host
与运行在 USB supported devices 的 Zephyr application 之间设置 networking。

Board 用 USB cable 连接到 Linux host（并向 host 提供 Ethernet interface。
Zephyr source
distribution 的 :zephyr:code-sample:`sockets-echo-server` application 在 supported board 上运行。Board 用
USB cable 连接到
Linux host（并向 host 提供 Ethernet interface。

Basic Setup
***********

要通过新建 Ethernet
interface 与 Zephyr application 通信（须为
Linux host 分配 IP addresses 并设置 routing table。
将 USB cable 从 board 插入 Linux host 后（
``cdc_ether`` driver 用提供的 MAC
address 注册新 Ethernet device。

可从 Linux host 运行 dmesg 检查 network device 已创建且 MAC address 已分配。

.. code-block:: console

   cdc_ether 1-2.7:1.0 eth0: register 'cdc_ether' at usb-0000:00:01.2-2.7, CDC Ethernet Device, 00:00:5e:00:53:01

须设置并分配 IP addresses（如下
节所述。

Choosing IP addresses
=====================

要建立到 board 的 network connection（须为
Linux host 上的 interface 选择 IP address。

选择 Zephyr
application 中所在 subnet 的地址有意义。IP addresses 通常在 project configuration files 中设置（
且也可用以下 commands 从 shell 检查。将
serial console program（如 puTTY）连接到 board（并向 Zephyr shell 输入此
command：

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

此 command 显示已为 board 分配一个 IPv4 address 和两个 IPv6 addresses。可根据
board network configuration 用 IPv4 或 IPv6 进行
network connection。

下一步为向新 Linux host interface 分配 IP addresses（
以下步骤中 ``enx00005e005301`` 为我
Linux system 上 interface 的名称。

Setting IPv4 address and routing
================================

.. code-block:: console

   # ip address add dev enx00005e005301 192.0.2.2
   # ip link set enx00005e005301 up
   # ip route add 192.0.2.0/24 dev enx00005e005301

Setting IPv6 address and routing
================================

.. code-block:: console

   # ip address add dev enx00005e005301 2001:db8::2
   # ip link set enx00005e005301 up
   # ip -6 route add 2001:db8::/64 dev enx00005e005301

Testing connection
******************

从 host 可用以下命令 ping board 的 Zephyr IP address 测试
connection：

.. code-block:: console

   $ ping 192.0.2.1
   PING 192.0.2.1 (192.0.2.1) 56(84) bytes of data.
   64 bytes from 192.0.2.1: icmp_seq=1 ttl=64 time=2.30 ms
   64 bytes from 192.0.2.1: icmp_seq=2 ttl=64 time=1.43 ms
   64 bytes from 192.0.2.1: icmp_seq=3 ttl=64 time=2.45 ms
   ...
