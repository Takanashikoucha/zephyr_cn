.. _network_monitoring:

监控网络流量
#######################

.. contents::
    :local:
    :depth: 2

能够监控网络流量是很有用的，尤其是在调试连接性问题或在 Zephyr 中开发新的协议支持时。本页介绍如何设置一种捕获网络流量的方式，以便用户能够在远程主机上使用 Wireshark 或类似工具来查看 Zephyr 设备发送或接收的网络数据包。

另请参阅 Zephyr 源码发行版中的 :zephyr:code-sample:`net-capture` 示例应用程序，了解需要启用的配置选项。

主机配置
******************

这里的说明介绍如何设置 Linux 主机来捕获 Zephyr 网络 RX 和 TX 流量。类似的说明在其他操作系统中应该也能适用。

在 Linux 主机上，找到 Zephyr 的 `net-tools`_ 项目，它既可以在 Zephyr 标准安装中的 ``tools/net-tools`` 目录下找到，也可以从其独立的 git 仓库单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

``net-tools`` 项目提供了一个配置文件来设置 IP-to-IP 隧道接口，以便我们可以将监控数据从 Zephyr 传输到主机。

在终端 #1 中，输入：

.. code-block:: console

   ./net-setup.sh -c zeth-tunnel.conf

该脚本将创建以下 IPIP 隧道接口：

.. csv-table::
   :header: "接口名称", "描述"
   :widths: auto

   "``zeth-ip6ip``", "IPv6-over-IPv4 隧道"
   "``zeth-ipip``", "IPv4-over-IPv4 隧道"
   "``zeth-ipip6``", "IPv4-over-IPv6 隧道"
   "``zeth-ip6ip6``", "IPv6-over-IPv6 隧道"

Zephyr 会将捕获的网络数据包发送到这些接口之一。
实际使用哪个接口取决于捕获是如何配置的。
然后你可以使用 Wireshark 来监控正确的网络接口。

在隧道接口创建之后，你可以例如使用 ``net-tools`` 项目中的 ``net-capture.py`` 脚本来打印或保存捕获的网络数据包。``net-capture.py`` 提供了一个 UDP 监听器，它可以将捕获的数据打印到屏幕上，并可选择将数据保存到 pcap 文件。

.. code-block:: console

   $ ./net-capture.py -i zeth-ip6ip -w capture.pcap
   [20210408Z14:33:08.959589] Ether / IP / ICMP 192.0.2.1 > 192.0.2.2 echo-request 0 / Raw
   [20210408Z14:33:08.976178] Ether / IP / ICMP 192.0.2.2 > 192.0.2.1 echo-reply 0 / Raw
   [20210408Z14:33:16.176303] Ether / IPv6 / ICMPv6 Echo Request (id: 0x9feb seq: 0x0)
   [20210408Z14:33:16.195326] Ether / IPv6 / ICMPv6 Echo Reply (id: 0x9feb seq: 0x0)
   [20210408Z14:33:21.194979] Ether / IPv6 / ICMPv6ND_NS / ICMPv6 Neighbor Discovery Option - Source Link-Layer Address 02:00:5e:00:53:3b
   [20210408Z14:33:21.217528] Ether / IPv6 / ICMPv6ND_NA / ICMPv6 Neighbor Discovery Option - Destination Link-Layer Address 00:00:5e:00:53:ff
   [20210408Z14:34:10.245408] Ether / IPv6 / UDP 2001:db8::2:47319 > 2001:db8::1:4242 / Raw
   [20210408Z14:34:10.266542] Ether / IPv6 / UDP 2001:db8::1:4242 > 2001:db8::2:47319 / Raw

``net-capture.py`` 具有以下命令行选项：

.. code-block:: console

   Listen captured network data from Zephyr and save it optionally to pcap file.
   ./net-capture.py \
 	-i | --interface <network interface>
 		Listen this interface for the data
 	[-p | --port <UDP port>]
 		UDP port (default is 4242) where the capture data is received
 	[-q | --quiet]
 		Do not print packet information
 	[-t | --type <L2 type of the data>]
 		Scapy L2 type name of the UDP payload, default is Ether
 	[-w | --write <pcap file name>]
 		Write the received data to file in PCAP format

除了 ``net-capture.py`` 脚本，你还可以例如使用 ``netcat`` 来提供一个 UDP 监听器，以便主机不会向 Zephyr 发送端口不可达（port unreachable）消息：

.. code-block:: console

   nc -l -u 2001:db8:200::2 4242 > /dev/null

上面的 IP 地址是内部隧道端点，可以更改，并且取决于 Zephyr 是如何配置的。Zephyr 会将包含捕获的网络数据包的 UDP 数据包发送到已配置的 IP 隧道，因此我们需要像这样终止网络连接。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools

Zephyr 配置
********************

在本示例中，我们使用 ``native_sim`` 单板。你也可以使用任何支持网络的其他单板。

在终端 #3 中，输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/capture
   :host-os: unix
   :board: native_sim
   :gen-args: -DCONFIG_UART_NATIVE_PTY_AUTOATTACH_DEFAULT_CMD=\""gnome-terminal -- screen %s"\"
   :goals: build
   :compact:

要查看 Zephyr 控制台和 shell，像这样启动 Zephyr 实例：

.. code-block:: console

   build/zephyr/zephyr.exe -attach_uart

也可以使用任何其他应用程序，只需确保启用了合适的
配置选项（参见 ``samples/net/capture/prj.conf`` 文件
中的示例）。

如有需要，网络捕获可以自动配置，但
目前 ``capture`` 示例应用程序并不这样做。用户必须使用
``net-shell`` 来设置并启用监控。

网络数据包监控需要首先进行设置。``net-shell`` 有
``net capture setup`` 命令用于完成此操作。该命令的语法是

.. code-block:: console

   net capture setup <remote-ip-addr> <local-ip-addr> <peer-ip-addr>
        <remote> 是（外部）端点 IP 地址
        <local> 是（内部）本地 IP 地址
        <peer> 是（内部）对等 IP 地址
        本地和对等 IP 地址中可以包含 UDP 端口号（可选）
        例如 198.0.51.2:9000 或 [2001:db8:100::2]:4242

在 Zephyr 控制台中，输入：

.. code-block:: console

   net capture setup 192.0.2.2 2001:db8:200::1 2001:db8:200::2

该命令将创建隧道接口。``192.0.2.2`` 是
隧道终止所在的远程主机。该地址用于选择
隧道接口所附加的本地网络接口。
``2001:db8:200::1`` 指定隧道的本地 IP 地址，
``2001:db8:200::2`` 是捕获的网络
数据包被发送到的对等 IP 地址。UDP 数据包的端口号可以在
setup 命令中像这样给出（针对 IPv6-over-IPv4 隧道）

.. code-block:: console

   net capture setup 192.0.2.2 [2001:db8:200::1]:9999 [2001:db8:200::2]:9998

针对 IPv4-over-IPv4 隧道则像这样

.. code-block:: console

   net capture setup 192.0.2.2 198.51.100.1:9999 198.51.100.2:9998

如果省略端口号，则默认使用 ``4242`` UDP 端口。

当前监控配置可以像这样检查：

.. code-block:: console

   uart:~$ net capture
   Network packet capture disabled
                   Capture  Tunnel
   Device          iface    iface   Local                  Peer
   NET_CAPTURE0    -        1      [2001:db8:200::1]:4242  [2001:db8:200::2]:4242

这将打印当前配置。由于我们尚未启用
监控，因此 ``Capture iface`` 未设置。

然后我们需要像这样启用网络数据包监控：

.. code-block:: console

   net capture enable 2

``2`` 指定我们想要捕获流量的网络接口。在
本示例中，``2`` 是 ``native_sim`` 单板的以太网接口。
注意，在本示例中我们将网络流量发送到我们正在
监控的同一个接口。监控系统会避免捕获已经
捕获过的网络流量，因为这会导致递归。
你可以使用 ``net iface`` 命令查看有哪些可用的网络接口。
注意，你不能从隧道接口捕获流量，因为这会
造成递归循环。
如果配置如此，捕获的网络流量可以发送到其他网络接口。只需在
``net capture setup`` 中正确设置 ``<remote-ip-addr>`` 选项，使 IP 隧道附加到所需的网络
接口即可。
捕获状态可以再次像这样检查：

.. code-block:: console

   uart:~$ net capture
   Network packet capture enabled
                   Capture  Tunnel
   Device          iface    iface   Local                  Peer
   NET_CAPTURE0    2        1      [2001:db8:200::1]:4242  [2001:db8:200::2]:4242

启用监控后，系统会将捕获的（无论是接收
还是发送的）网络数据包发送到隧道接口以进行进一步处理。

监控可以像这样禁用：

.. code-block:: console

   net capture disable

这将关闭当前正在运行的监控。监控设置可以
像这样清除：

.. code-block:: console

   net capture cleanup

配置监控时不必使用 ``net-shell``。
如有需要，应用程序可以调用 :ref:`网络捕获 API <net_capture_interface>` 函数。

Wireshark 配置
***********************

`Wireshark <https://www.wireshark.org/>`_ 工具可以以有用的方式监控
捕获的网络流量。

你可以监控隧道接口或 ``zeth`` 接口。
为了查看 UDP 数据包内部实际捕获的数据，
请参阅 `Wireshark 解封装 UDP`_ 文档中的说明。

.. _Wireshark 解封装 UDP:
   https://osqa-ask.wireshark.org/questions/28138/decoding-ethernet-encapsulated-in-tcp-or-udp/
