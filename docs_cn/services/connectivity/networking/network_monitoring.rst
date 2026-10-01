.. _network_monitoring:

Monitor Network Traffic
#######################

.. contents::
    :local:
    :depth: 2

能够监控 network traffic 很有用（尤其在
调试 connectivity issues 或在
Zephyr 中开发新 protocol support 时。此页面描述如何设置捕获 network traffic 的方式（
使 user 能在 remote host 上用 Wireshark 或类似 tool 查看
Zephyr device 发送或接收的 network packets。

参见 Zephyr source distribution 的 :zephyr:code-sample:`net-capture` sample application 了解须启用的 configuration options。

Host Configuration
******************

这里的说明描述如何设置 Linux host 以捕获 Zephyr
network RX 和 TX traffic。类似说明在其他
operating systems 中也应工作。

在 Linux Host 上（找到 Zephyr `net-tools`_ project（其可在 Zephyr standard installation 的 ``tools/net-tools`` directory 下找到（或从自己的 git repository 单独安装：

.. code-block:: console

   git clone https://github.com/zephyrproject-rtos/net-tools

``net-tools`` project 提供 configure file 以设置 IP-to-IP tunnel
interface（使我们可以从 Zephyr 向 host 传输 monitoring data。

Terminal #1 中输入：

.. code-block:: console

   ./net-setup.sh -c zeth-tunnel.conf

此 script 将创建以下 IPIP tunnel interfaces：

.. csv-table::
   :header: "Interface name", "Description"
   :widths: auto

   "``zeth-ip6ip``", "IPv6-over-IPv4 tunnel"
   "``zeth-ipip``", "IPv4-over-IPv4 tunnel"
   "``zeth-ipip6``", "IPv4-over-IPv6 tunnel"
   "``zeth-ip6ip6``", "IPv6-over-IPv6 tunnel"

Zephyr 将捕获的 network packets 发送到这些 interfaces 之一。
实际 interface 取决于 capturing 如何配置。
然后可用 Wireshark 监控正确的 network interface。

Tunneling interfaces 创建后（例如可用 ``net-tools`` project 的 ``net-capture.py`` script 打印或保存
捕获的 network packets。``net-capture.py`` 提供 UDP listener（
其可将捕获的 data 打印到 screen（并可选地
将 data 保存到 pcap file。

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

``net-capture.py`` 有以下 command line options：

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

而非 ``net-capture.py`` script（例如可用 ``netcat``
提供 UDP listener（使 host 不向 Zephyr 发送 port unreachable
message：

.. code-block:: console

   nc -l -u 2001:db8:200::2 4242 > /dev/null

上述 IP address 为 inner tunnel endpoint（可更改（
且取决于 Zephyr 如何配置。Zephyr 将包含捕获 network packets 的 UDP packets
发送到配置的 IP tunnel（故须如此终止 network connection。

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools

Zephyr Configuration
********************

此示例中（使用 ``native_sim`` board。也可用任何支持 networking 的其他 board。

Terminal #3 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/capture
   :host-os: unix
   :board: native_sim
   :gen-args: -DCONFIG_UART_NATIVE_PTY_AUTOATTACH_DEFAULT_CMD=\""gnome-terminal -- screen %s"\"
   :goals: build
   :compact:

要查看 Zephyr console 和 shell（如下启动 Zephyr instance：

.. code-block:: console

   build/zephyr/zephyr.exe -attach_uart

也可用任何其他 application（仅确保启用了合适
configuration options（示例参见 ``samples/net/capture/prj.conf`` file）。

Network capture 需要时可自动配置（但
当前 ``capture`` sample application 不这样做。User 须用
``net-shell`` 设置并启用 monitoring。

Network packet monitoring 须先设置。``net-shell`` 有
``net capture setup`` command 用于此。Command 语法为

.. code-block:: console

   net capture setup <remote-ip-addr> <local-ip-addr> <peer-ip-addr>
        <remote> is the (outer) endpoint IP address
        <local> is the (inner) local IP address
        <peer> is the (inner) peer IP address
        Local and Peer IP addresses can have UDP port number in them (optional)
        like 198.0.51.2:9000 or [2001:db8:100::2]:4242

Zephyr console 中输入：

.. code-block:: console

   net capture setup 192.0.2.2 2001:db8:200::1 2001:db8:200::2

此 command 将创建 tunneling interface。``192.0.2.2`` 为
终止 tunnel 的 remote host。该 address 用于选择
tunneling interface 附加到的 local network interface。
``2001:db8:200::1`` 告知 tunnel 的 local IP address（
``2001:db8:200::2`` 为发送捕获 network
packets 的 peer IP address。UDP packet 的 port numbers 可如此在
setup command 中给出（对 IPv6-over-IPv4 tunnel

.. code-block:: console

   net capture setup 192.0.2.2 [2001:db8:200::1]:9999 [2001:db8:200::2]:9998

对 IPv4-over-IPv4 tunnel

.. code-block:: console

   net capture setup 192.0.2.2 198.51.100.1:9999 198.51.100.2:9998

若省略 port number（则默认使用 ``4242`` UDP port。

当前 monitoring configuration 可如此检查：

.. code-block:: console

   uart:~$ net capture
   Network packet capture disabled
                   Capture  Tunnel
   Device          iface    iface   Local                  Peer
   NET_CAPTURE0    -        1      [2001:db8:200::1]:4242  [2001:db8:200::2]:4242

其将打印当前 configuration。由于尚未启用
monitoring（``Capture iface`` 未设置。

然后须如下启用 network packet monitoring：

.. code-block:: console

   net capture enable 2

``2`` 告知要捕获 traffic 的 network interface。
此示例中（``2`` 为 ``native_sim`` board Ethernet interface。
注意此示例中我们将 network traffic 发送到正在
监控的同一 interface。Monitoring system 避免捕获已
捕获的 network traffic（否则将导致递归。
可用 ``net iface`` command 查看可用哪些 network interfaces。
注意不能从 tunnel interface 捕获 traffic（否则
将导致递归 loop。
若配置（捕获的 network traffic 可发送到其他 network interface。
仅在 ``net capture setup`` 中正确设置 ``<remote-ip-addr>`` option（使 IP tunnel 附加到期望 network
interface 即可。
Capture status 可再次如此检查：

.. code-block:: console

   uart:~$ net capture
   Network packet capture enabled
                   Capture  Tunnel
   Device          iface    iface   Local                  Peer
   NET_CAPTURE0    2        1      [2001:db8:200::1]:4242  [2001:db8:200::2]:4242

启用 monitoring 后（系统将发送捕获的（接收
或发送的）network packets 到 tunnel interface 以进一步处理。

Monitoring 可如此禁用：

.. code-block:: console

   net capture disable

其将关闭当前运行的 monitoring。Monitoring setup 可
如此清除：

.. code-block:: console

   net capture cleanup

配置 monitoring 不必使用 ``net-shell``。
若需要（application 可调用
:ref:`network capture API <net_capture_interface>` functions。

Wireshark Configuration
***********************

`Wireshark <https://www.wireshark.org/>`_ tool 可用于以有用方式监控
捕获的 network traffic。

可监控 tunnel interfaces 或 ``zeth`` interface。
要在 UDP packet 内查看实际捕获的 data（
参见 `Wireshark decapsulate UDP`_ 文档了解说明。

.. _Wireshark decapsulate UDP:
   https://osqa-ask.wireshark.org/questions/28138/decoding-ethernet-encapsulated-in-tcp-or-udp/
