.. _networking_with_native_sim_eth_bridge:

Ethernet bridge with native_sim board
#####################################

.. contents::
    :local:
    :depth: 2

此文档描述如何在 (Linux) host 与运行在 :zephyr:board:`native_sim <native_sim>` board 的 Zephyr application 之间设置 bridged Ethernet network。

此 setup 在测试可用 :kconfig:option:`CONFIG_NET_ETHERNET_BRIDGE` Kconfig option 启用的 Ethernet bridging feature 时有用。此 setup 中（net-tools configuration 创建两个 host network interfaces ``zeth0`` 和 ``zeth1``（并将其连接到 Zephyr 的 :zephyr:board:`native_sim <native_sim>` application。

首先创建 host interfaces。此示例中创建两个 interfaces。

.. code-block:: console

   cd $ZEPHYR_BASE/../tools/net-tools
   ./net-setup.sh -c zeth-multiface.conf -i zeth0 -t 2

``-c`` 告知使用哪个 configuration file（``zeth-multiface.conf`` 专为在 host 中生成多个 network interfaces 定制。``-i`` option 告知第一个 host interface name。``-t`` 告知创建多少个 network interfaces。

Host interfaces 示例 output：

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

然后创建 sample 并启用 Ethernet bridging 支持。此示例中创建 :zephyr:code-sample:`sockets-echo-server` sample application。

Bridging 需第二个 TAP interface。创建 devicetree overlay file :file:`second-iface.overlay` 以添加第二个 ``zephyr,native-tap`` interface：

.. code-block:: devicetree

   / {
       zeth1: zeth1 {
           compatible = "zephyr,native-tap";
           status = "okay";
           zephyr,random-mac-address;
           host-interface = "zeth1";
       };
   };

然后构建并运行 application（指向 overlay：

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

这将创建并运行启用 bridging（但尚未配置）的 :zephyr:code-sample:`sockets-echo-server`。要配置 bridging（须用 bridge shell 或直接从 application 调用 bridging API。此示例用 bridge shell 设置 bridging：

.. code-block:: console

   net bridge addif 1 3 2
   net iface up 1

上述示例中（bridge interface index 为 1（interfaces 2 和 3 为链接到 host 侧 ``zeth0`` 和 ``zeth1`` 的 Ethernet interfaces。

Zephyr 侧的 network interfaces 如下：

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

``net bridge`` command 将显示 bridging 当前状态：

.. code-block:: console

   net bridge
   Bridge Status   Config   Interfaces
   1      up       ok       2 3

``addif`` command 将 Ethernet interfaces 2 和 3 添加到 bridge interface 1。``addif`` command 后（bridging 仍禁用（因为 bridge interface 默认未 up。``net iface up`` command 将启用 bridging。

若 host 侧运行 wireshark（并监控 ``zeth0`` 和 ``zeth1``（应在两个 host interfaces 中看到相同的 network traffic。

注意 interface index numbers 不固定（bridge 和 Ethernet interface index values 在您的 setup 中可能不同。

Bridge interface down 可禁用 bridging（且可用 ``delif`` command 从 bridge 移除 Ethernet interfaces。

.. code-block:: console

   net iface down 1
   net bridge delif 1 2 3
