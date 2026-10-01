.. _networking_with_multiple_instances:

Networking with multiple Zephyr instances
#########################################

.. contents::
    :local:
    :depth: 2

此页面描述如何在多个
Zephyr instances 之间设置虚拟 network。Zephyr instances 可在 QEMU
内运行（或可为 native_sim board processes。Linux host 可
用于在这些 systems 之间路由 network traffic。

Prerequisites
*************

在 Linux Host 上（找到 Zephyr `net-tools`_ project（其可在 Zephyr standard installation 的 ``tools/net-tools`` directory 下找到（或从自己的 git repository 单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

Basic Setup
***********

以下步骤需五个 terminal windows：

* Terminal #1 和 #2 为 net-tools 为当前
  directory 的 terminal windows（``cd net-tools``）
* Terminal #3（在其中设置 Linux host 中的 bridging
* Terminal #4 和 #5 为常规 Zephyr development terminal（
  Zephyr environment 已初始化。

由于设置 Zephyr network 有多种方式（以下示例使用
``qemu_x86`` board 和 ``e1000`` Ethernet controller 以及 native_sim board
以简化 setup 说明。需要时可用其他 QEMU boards 和 drivers（
细节参见 :ref:`networking_with_eth_qemu`。也可用
两个或多个 native_sim board Zephyr instances（并将它们连接在一起。


Step 1 - Create configuration files
===================================

启动带 network connectivity 的 QEMU 前（host system 中应为每个
Zephyr instance 创建 network interfaces。创建 network interface 的默认 setup
此处不可用（因为其用于将一个
Zephyr instance 连接到 Linux host。

对 Zephyr instance #1（向 ``net-tools``
project（或某个其他合适 directory）创建名为 ``zephyr1.conf`` 的 file。

.. code-block:: console

   # Configuration file for setting IP addresses for a network interface.
   INTERFACE="$1"
   HWADDR="00:00:5e:00:53:11"
   IPV6_ADDR_1="2001:db8:100::2"
   IPV6_ROUTE_1="2001:db8:100::/64"
   IPV4_ADDR_1="198.51.100.2/24"
   IPV4_ROUTE_1="198.51.100.0/24"
   ip link set dev $INTERFACE up
   ip link set dev $INTERFACE address $HWADDR
   ip -6 address add $IPV6_ADDR_1 dev $INTERFACE nodad
   ip -6 route add $IPV6_ROUTE_1 dev $INTERFACE
   ip address add $IPV4_ADDR_1 dev $INTERFACE
   ip route add $IPV4_ROUTE_1 dev $INTERFACE > /dev/null 2>&1

对 Zephyr instance #2（向 ``net-tools``
project（或某个其他合适 directory）创建名为 ``zephyr2.conf`` 的 file。

.. code-block:: console

   # Configuration file for setting IP addresses for a network interface.
   INTERFACE="$1"
   HWADDR="00:00:5e:00:53:22"
   IPV6_ADDR_1="2001:db8:200::2"
   IPV6_ROUTE_1="2001:db8:200::/64"
   IPV4_ADDR_1="203.0.113.2/24"
   IPV4_ROUTE_1="203.0.113.0/24"
   ip link set dev $INTERFACE up
   ip link set dev $INTERFACE address $HWADDR
   ip -6 address add $IPV6_ADDR_1 dev $INTERFACE nodad
   ip -6 route add $IPV6_ROUTE_1 dev $INTERFACE
   ip address add $IPV4_ADDR_1 dev $INTERFACE
   ip route add $IPV4_ROUTE_1 dev $INTERFACE > /dev/null 2>&1


Step 2 - Create Ethernet interfaces
===================================

以下 ``net-setup.sh`` commands 应在 net-tools
directory（``cd net-tools``）中输入。

Terminal #1 中输入：

.. code-block:: console

   ./net-setup.sh -c zephyr1.conf -i zeth.1

Terminal #2 中输入：

.. code-block:: console

   ./net-setup.sh -c zephyr2.conf -i zeth.2


Step 3 - Setup network bridging
===============================

Terminal #3 中输入：

.. code-block:: console

   sudo brctl addbr zeth-br
   sudo brctl addif zeth-br zeth.1
   sudo brctl addif zeth-br zeth.2
   sudo ifconfig zeth-br up


Step 4 - Start Zephyr instances
===============================

此示例中启动 :zephyr:code-sample:`sockets-echo-server` 和
:zephyr:code-sample:`sockets-echo-client` sample applications。需要时也可用其他 applications。

Terminal #4 中（若使用 QEMU（输入此：

.. code-block:: console

   west build -d build/server -b qemu_x86 -t run \
      samples/net/sockets/echo_server -- \
      -DEXTRA_CONF_FILE=overlay-e1000.conf \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"203.0.113.1\" \
      -DCONFIG_ETH_QEMU_IFACE_NAME=\"zeth.1\" \
      -DCONFIG_NET_QEMU_DEVICE_EXTRA_ARGS=\"mac=00:00:5e:00:53:01\"

或若要用 native_sim board（输入此：

.. code-block:: console

   west build -d build/server -b native_sim \
      samples/net/sockets/echo_server -- \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"203.0.113.1\"
   build/server/zephyr/zephyr.exe --eth-if=zeth.1 --mac-addr=00:00:5e:00:53:01


Terminal #5 中（若使用 QEMU（输入此：

.. code-block:: console

   west build -d build/client -b qemu_x86 -t run \
      samples/net/sockets/echo_client -- \
      -DEXTRA_CONF_FILE=overlay-e1000.conf \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"198.51.100.1\" \
      -DCONFIG_ETH_QEMU_IFACE_NAME=\"zeth.2\" \
      -DCONFIG_NET_QEMU_DEVICE_EXTRA_ARGS=\"mac=00:00:5e:00:53:02\"

或若要用 native_sim board（输入此：

.. code-block:: console

   west build -d build/client -b native_sim \
      samples/net/sockets/echo_client -- \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"198.51.100.1\"
   build/client/zephyr/zephyr.exe --eth-if=zeth.2 --mac-addr=00:00:5e:00:53:02


另外（若 host 中启用 firewall（须允许
``zeth.1``、``zeth.2`` 和 ``zeth-br`` interfaces 间的 traffic。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
