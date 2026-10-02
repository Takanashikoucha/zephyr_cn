.. _networking_with_native_sim_eth_bridge:

使用 native_sim 板卡的以太网桥接
#####################################

.. contents::
    :local:
    :depth: 2

本文档描述如何在（Linux）主机与运行在
:zephyr:board:`native_sim <native_sim>` 板卡上的 Zephyr 应用程序之间
设置桥接以太网网络。

此设置在测试可用 :kconfig:option:`CONFIG_NET_ETHERNET_BRIDGE` Kconfig 选项
启用的以太网桥接功能时有用。在此设置中，net-tools
配置创建两个主机网络接口 ``zeth0`` 和 ``zeth1``，
并将它们连接到 Zephyr 的 :zephyr:board:`native_sim <native_sim>` 应用程序。

首先创建主机接口。在此示例中创建两个接口。

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   ./net-setup.sh -c zeth-multiface.conf -i zeth0 -t 2

``-c`` 告知使用哪个配置文件，其中 ``zeth-multiface.conf``
专为在主机中生成多个网络接口定制。
``-i`` 选项告知第一个主机接口名称。``-t`` 告知
创建多少个网络接口。

主机接口的示例输出：

.. code-block:: console

   zeth0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
          inet 192.0.2.2  netmask 255.255.255.255  broadcast 0.0.0.0
          inet6 2001:db8::2  prefixlen 128  scopeid 0x0<global>
          inet6 fe80::200:5eff:fe00:5300  prefixlen 64  scopeid 0x20<link>
          ether 00:00:5e:00:53:00  txqueuelen 1000  (Ethernet)
          RX packets 33  bytes 2408 (2.4 KB)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 49  bytes 4092 (4.0 KB)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   zeth1: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
          inet 198.51.100.1  netmask 255.255.255.255  broadcast 0.0.0.0
          inet6 fe80::200:5eff:fe00:5301  prefixlen 64  scopeid 0x20<link>
          inet6 2001:db8:2::1  prefixlen 128  scopeid 0x0<global>
          ether 00:00:5e:00:53:01  txqueuelen 1000  (Ethernet)
          RX packets 21  bytes 1340 (1.3 KB)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 45  bytes 3916 (3.9 KB)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

然后创建示例并启用以太网桥接支持。在此示例中创建
:zephyr:code-sample:`sockets-echo-server` 示例应用程序。

桥接需要第二个 TAP 接口。创建设备树覆盖文件
:file:`second-iface.overlay`，添加第二个 ``zephyr,native-tap`` 接口：

.. code-block:: devicetree

   / {
       zeth1: zeth1 {
           compatible = "zephyr,native-tap";
           status = "okay";
           zephyr,random-mac-address;
           host-interface = "zeth1";
       };
   };

然后构建并运行应用程序，指向覆盖文件：

.. code-block:: console

   west build -p -b native_sim -d ../build/echo-server \
      samples/net/sockets/echo_server -- \
      -DCONFIG_UART_NATIVE_PTY_AUTOATTACH_DEFAULT_CMD="\"gnome-terminal -- screen %s\"" \
      -DCONFIG_NET_ETHERNET_BRIDGE=y \
      -DCONFIG_NET_ETHERNET_BRIDGE_SHELL=y \
      -DEXTRA_DTC_OVERLAY_FILE=second-iface.overlay \
      -DCONFIG_NET_IF_MAX_IPV6_COUNT=2 \
      -DCONFIG_NET_IF_MAX_IPV4_COUNT=2
   ../build/echo-server/zephyr/zephyr.exe -attach_uart

这将创建并运行启用桥接但尚未配置的
:zephyr:code-sample:`sockets-echo-server`。要配置桥接，
你要么使用桥接 shell，要么直接从应用程序
调用桥接 API。我们使用桥接 shell 设置桥接如下：

.. code-block:: console

   net bridge addif 1 3 2
   net iface up 1

在上述示例中，桥接接口索引为 1，接口 2 和 3 是
链接到主机侧 ``zeth0`` 和 ``zeth1`` 的以太网接口。

Zephyr 侧的网络接口如下：

.. code-block:: console

   net iface
   Hostname: zephyr

   Interface bridge0 (0x8090ebc) (Virtual) [1]
   ==================================
   Virtual name : <enabled>
   No attached network interface.
   Link addr : 3B:DB:31:0F:CC:B6
   MTU       : 1500
   Flags     : NO_AUTO_START
   Device    : BRIDGE_0 (0x8088354)
   Promiscuous mode : disabled
   IPv6 not enabled for this interface.
   IPv4 not enabled for this interface.

   Interface eth0 (0x8090fcc) (Ethernet) [2]
   ===================================
   Link addr : 02:00:5E:00:53:D2
   MTU       : 1500
   Flags     : AUTO_START,IPv4,IPv6
   Device    : zeth0 (0x808837c)
   Promiscuous mode : disabled
   Ethernet capabilities supported:
           TXTIME
           Promiscuous mode
   Ethernet PHY device: <none> (0)
   IPv6 unicast addresses (max 3):
           fe80::5eff:fe00:53d2 autoconf preferred infinite
           2001:db8::1 manual preferred infinite
   IPv6 multicast addresses (max 4):
           ff02::1
           ff02::1:ff00:53d2
           ff02::1:ff00:1
   IPv6 prefixes (max 2):
           <none>
   IPv6 hop limit           : 64
   IPv6 base reachable time : 30000
   IPv6 reachable time      : 18476
   IPv6 retransmit timer    : 0
   IPv4 unicast addresses (max 1):
           192.0.2.1/255.255.255.0 manual preferred infinite
   IPv4 multicast addresses (max 2):
           224.0.0.1
   IPv4 gateway : 0.0.0.0

   Interface eth1 (0x80910dc) (Ethernet) [3]
   ===================================
   Link addr : 02:00:5E:00:53:87
   MTU       : 1500
   Flags     : AUTO_START,IPv4,IPv6
   Device    : zeth1 (0x8088368)
   Promiscuous mode : disabled
   Ethernet capabilities supported:
           TXTIME
           Promiscuous mode
   Ethernet PHY device: <none> (0)
   IPv6 unicast addresses (max 3):
           fe80::5eff:fe00:5387 autoconf preferred infinite
   IPv6 multicast addresses (max 4):
           ff02::1
           ff02::1:ff00:5387
   IPv6 prefixes (max 2):
           <none>
   IPv6 hop limit           : 64
   IPv6 base reachable time : 30000
   IPv6 reachable time      : 25158
   IPv6 retransmit timer    : 0
   IPv4 unicast addresses (max 1):
           <none>
   IPv4 multicast addresses (max 2):
           224.0.0.1
   IPv4 gateway : 0.0.0.0

``net bridge`` 命令将显示桥接的当前状态：

.. code-block:: console

   net bridge
   Bridge Status   Config   Interfaces
   1      up       ok       2 3

``addif`` 命令将以太网接口 2 和 3 添加到桥接接口 1。
``addif`` 命令后，桥接仍禁用，因为桥接接口
默认未启动。``net iface up`` 命令将启用桥接。

如果你在主机侧运行 wireshark 并监控 ``zeth0`` 和 ``zeth1``，
你应该在两个主机接口中看到相同的网络流量。

注意接口索引号不固定，桥接和以太网接口索引
值在你的设置中可能不同。

通过关闭桥接接口可以禁用桥接，
可用 ``delif`` 命令从桥接中移除以太网接口。

.. code-block:: console

   net iface down 1
   net bridge delif 1 2 3
