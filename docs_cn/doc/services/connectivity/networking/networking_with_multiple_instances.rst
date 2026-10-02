.. _networking_with_multiple_instances:

使用多个 Zephyr 实例进行网络通信
#########################################

.. contents::
    :local:
    :depth: 2

本页介绍如何在多个 Zephyr 实例之间搭建虚拟网络。Zephyr 实例可以运行在 QEMU 内部，也可以是 native_sim 单板进程。Linux 主机可用于在这些系统之间路由网络流量。

前提条件
*************

在 Linux 主机上，找到 Zephyr 的 `net-tools`_ 项目，它既可以在 Zephyr 标准安装中的 ``tools/net-tools`` 目录下找到，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

基本设置
***********

对于下面的步骤，你需要五个终端窗口：

* 终端 #1 和 #2 是当前目录为 net-tools 的终端窗口（``cd net-tools``）
* 终端 #3，用于在 Linux 主机上设置桥接
* 终端 #4 和 #5 是你通常使用的 Zephyr 开发终端，
  已初始化 Zephyr 环境。

由于设置 Zephyr 网络的方式有多种，下面的示例使用带 ``e1000`` 以太网控制器的 ``qemu_x86`` 单板和 native_sim 单板来简化设置说明。如有需要，你可以使用其他 QEMU 单板和驱动程序，详情请参见 :ref:`networking_with_eth_qemu`。你也可以使用两个或更多 native_sim 单板 Zephyr 实例并将它们连接在一起。


步骤 1 - 创建配置文件
===================================

在启动带网络连接的 QEMU 之前，应在主机系统中为每个
Zephyr 实例创建网络接口。这里不能使用创建网络接口的默认设置，因为那是用于将一个
Zephyr 实例连接到 Linux 主机的。

对于 Zephyr 实例 #1，在 ``net-tools``
项目中（或某个其他合适的目录中）创建名为 ``zephyr1.conf`` 的文件。

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

对于 Zephyr 实例 #2，在 ``net-tools``
项目中（或某个其他合适的目录中）创建名为 ``zephyr2.conf`` 的文件。

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


步骤 2 - 创建以太网接口
===================================

下面的 ``net-setup.sh`` 命令应在 net-tools
目录（``cd net-tools``）中输入。

在终端 #1 中，输入：

.. code-block:: console

   ./net-setup.sh -c zephyr1.conf -i zeth.1

在终端 #2 中，输入：

.. code-block:: console

   ./net-setup.sh -c zephyr2.conf -i zeth.2


步骤 3 - 设置网络桥接
===============================

在终端 #3 中，输入：

.. code-block:: console

   sudo brctl addbr zeth-br
   sudo brctl addif zeth-br zeth.1
   sudo brctl addif zeth-br zeth.2
   sudo ifconfig zeth-br up


步骤 4 - 启动 Zephyr 实例
===============================

在本示例中，我们启动 :zephyr:code-sample:`sockets-echo-server` 和
:zephyr:code-sample:`sockets-echo-client` 示例应用程序。如有需要，你也可以使用其他应用程序。

在终端 #4 中，如果你使用 QEMU，输入以下内容：

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

或者如果你想使用 native_sim 单板，输入以下内容：

.. code-block:: console

   west build -d build/server -b native_sim \
      samples/net/sockets/echo_server -- \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"203.0.113.1\"
   build/server/zephyr/zephyr.exe --eth-if=zeth.1 --mac-addr=00:00:5e:00:53:01


在终端 #5 中，如果你使用 QEMU，输入以下内容：

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

或者如果你想使用 native_sim 单板，输入以下内容：

.. code-block:: console

   west build -d build/client -b native_sim \
      samples/net/sockets/echo_client -- \
      -DCONFIG_NET_CONFIG_MY_IPV4_ADDR=\"203.0.113.1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV4_ADDR=\"198.51.100.1\" \
      -DCONFIG_NET_CONFIG_MY_IPV6_ADDR=\"2001:db8:200::1\" \
      -DCONFIG_NET_CONFIG_PEER_IPV6_ADDR=\"2001:db8:100::1\" \
      -DCONFIG_NET_CONFIG_MY_IPV4_GW=\"198.51.100.1\"
   build/client/zephyr/zephyr.exe --eth-if=zeth.2 --mac-addr=00:00:5e:00:53:02


另外，如果主机上启用了防火墙，你需要允许
``zeth.1``、``zeth.2`` 和 ``zeth-br`` 接口之间的流量。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
