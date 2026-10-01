.. _networking_with_qemu:

Networking with QEMU
####################

.. contents::
    :local:
    :depth: 2

此页面描述如何在 (Linux) host 与运行在 QEMU virtual machine（为 Zephyr
targets（如 qemu_x86 和 qemu_cortex_m3）构建）的 Zephyr application 之间设置虚拟 network。某些 virtual ARM boards（如
qemu_cortex_a53）仅支持单个 UART（此情况下首选 QEMU Ethernet（
细节参见 :ref:`networking_with_eth_qemu`。

此示例中（Zephyr source distribution 的 :zephyr:code-sample:`sockets-echo-server` sample application 在 QEMU 中运行。QEMU instance
通过 serial port 连接到 Linux host（且用 SLIP
在 Zephyr application 和 Linux 间传输 data（通过虚拟
connections 链。

Prerequisites
*************

在 Linux Host 上（找到 Zephyr `net-tools`_ project（其可在 Zephyr standard installation 的 ``tools/net-tools`` directory 下找到（或从自己的 git repository 单独安装：

.. code-block:: console

   sudo apt install -y socat libpcap-dev
   git clone https://github.com/zephyrproject-rtos/net-tools
   cd net-tools
   make

.. note::

   若得到关于 AX_CHECK_COMPILE_FLAG 的 error（在 Debian/Ubuntu 上安装
   ``autoconf-archive`` package。

Basic Setup
***********

以下步骤至少需 4 个 terminal windows：

* Terminal #1 为常规 Zephyr development terminal（Zephyr environment
  已初始化。
* Terminals #2、#3 和 #4 为 net-tools 为当前
  directory 的 terminal windows（``cd net-tools``）

Step 1 - Create helper socket
=============================

启动带 network 模拟的 QEMU 前（应为模拟
创建 Unix socket。

Terminal #2 中输入：

.. code-block:: console

   ./loop-socat.sh

Step 2 - Start TAP device routing daemon
========================================

Terminal #3 中输入：


.. code-block:: console

   sudo ./loop-slip-tap.sh

对需 DNS 的 applications（可能须在此处重启 host 的 DNS server（
如 :ref:`networking_internet` 中所述。

Step 3 - Start app in QEMU
==========================

构建并启动 ``echo_server`` sample application。

Terminal #1 中输入：

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :goals: run
   :compact:

若看到 QEMU 关于 unix:/tmp/slip.sock 的 error（意味着漏了
上述 Step 1。

Step 4 - Run apps on host
=========================

现在 Terminal #4 中（可运行各种 tools 与
QEMU 中运行的 application 通信。

可从 pings 开始：

.. code-block:: console

   ping 192.0.2.1
   ping6 2001:db8::1

可用 netcat ("nc") utility（用 UDP 连接：

.. code-block:: console

   echo foobar | nc -6 -u 2001:db8::1 4242
   foobar

.. code-block:: console

   echo foobar | nc -u 192.0.2.1 4242
   foobar

若 echo_server 编译带 TCP 支持（当前 echo_server sample 默认启用（CONFIG_NET_TCP=y）：

.. code-block:: console

   echo foobar | nc -6 -q2 2001:db8::1 4242
   foobar

.. note::

   用 Ctrl+C 退出。

也可用 telnet command 实现上述。

Step 5 - Stop supporting daemons
================================

完成用 QEMU 的 network testing 后（应停止
初始步骤中启动的任何 daemons 或 helpers（以避免可能的
networking 或 routing problems（如 local
network interfaces 中的 address conflicts。例如（若从
QEMU network testing 切换到用真实 hardware（或要将 host
laptop 恢复正常 Wi-Fi 使用（停止它们。

停止 daemons（在相应 terminal windows 中按 Ctrl+C
（须停止 ``loop-slip-tap.sh`` 和 ``loop-socat.sh`` 两者）。

按 :kbd:`CTRL+A` :kbd:`x` 退出 QEMU。

.. _networking_internet:

Setting up Zephyr and NAT/masquerading on host to access Internet
*****************************************************************

要从 Zephyr application 访问 internet（host 上可能须
额外 setup。此 setup 对在 QEMU 中和在真实 hardware 上运行的
application 通用（假设
development board 连接到 development host。若
board 连接到专用 router（则不需要。

要从 QEMU 中运行的自定义 application 用 IPv4 访问 internet（
应通过 DHCP 设置或手动配置 gateway。
对使用 "Settings" facility（启用 config option
:kconfig:option:`CONFIG_NET_CONFIG_SETTINGS`）的 applications（
将 :kconfig:option:`CONFIG_NET_CONFIG_MY_IPV4_GW` option 设为
gateway 的 IP address。对不使用 "Settings" facility 的 apps（在
runtime 调用 :c:func:`net_if_ipv4_set_gw 设置
gateway。
例如：``CONFIG_NET_CONFIG_MY_IPV4_GW="192.0.2.2"``

要从 QEMU 中运行的自定义 application 访问 internet（应为
QEMU 的 source address 设置 NAT
(masquerading)。假设使用 ``192.0.2.1``（且 Zephyr network interface 为 ``zeth``（以下 command 应以 root 运行：

.. code-block:: console

   iptables -t nat -A POSTROUTING -j MASQUERADE -s 192.0.2.1/24
   iptables -I FORWARD 1 -i zeth -j ACCEPT
   iptables -I FORWARD 1 -o zeth -m state --state RELATED,ESTABLISHED -j ACCEPT

另外（host 上应启用 IPv4 forwarding（且可能须
检查其他 firewall (iptables) rules 不干扰 masquerading。
启用 IPv4 forwarding（以下 command 应以 root 运行：

.. code-block:: console

   sysctl -w net.ipv4.ip_forward=1

某些 applications 可能还需 DNS server。若干 Zephyr 提供的
samples 默认假设 host 上
（IP ``192.0.2.2``）有可用 DNS server（其在现代 Linux distributions 中通常至少运行
DNS proxy。用 QEMU 运行时（可能须重启 host 的
DNS（使其能为新建 TAP interface 上的 requests 服务。例如（
在 Debian-based systems 上：

.. code-block:: console

   service dnsmasq restart

依赖 host DNS server 的替代方案为使用
network 中的一个。例如（``8.8.8.8`` 为公开可用 DNS server。可
用 :kconfig:option:`CONFIG_DNS_SERVER1` option 配置。


Network connection between two QEMU VMs
***************************************

与上述 VM-to-Host setup 不同（VM-to-VM setup
自动。对支持此 mode 的 sample
applications（如 echo_server 和 echo_client
samples（须两个 terminal windows（为 Zephyr development 设置。

Terminal #1:
============

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_server
   :host-os: unix
   :board: qemu_x86
   :goals: build
   :build-args: server
   :compact:

这将启动 QEMU（等待来自 client QEMU 的 connection。

Terminal #2:
============

.. zephyr-app-commands::
   :zephyr-app: samples/net/sockets/echo_client
   :host-os: unix
   :board: qemu_x86
   :goals: build
   :build-args: client
   :compact:

这将启动第二个 QEMU instance（应在两者中看到发送和
收到的 data 的 logging。

Running multiple QEMU VMs of the same sample
********************************************

若发现想运行同一 Zephyr
sample application 的多个 instances（且它们无需相互通信（用
``QEMU_INSTANCE`` argument。

手动启动 ``socat`` 和 ``tunslip6``（而非用
``loop-xxx.sh`` scripts）（按需启动的 instances 数量。用
以下作为 guide（替换 MAIN 或 OTHER。

Terminal #1:
============

.. code-block:: console

   socat PTY,link=/tmp/slip.devMAIN UNIX-LISTEN:/tmp/slip.sockMAIN &
   sudo $ZEPHYR_BASE/../tools/net-tools/tunslip6 -t tapMAIN -T -s /tmp/slip.devMAIN 2001:db8::1/64 &
   # Now run Zephyr
   make -Cbuild run QEMU_INSTANCE=MAIN

Terminal #2:
============

.. code-block:: console

   socat PTY,link=/tmp/slip.devOTHER UNIX-LISTEN:/tmp/slip.sockOTHER &
   sudo $ZEPHYR_BASE/../tools/net-tools/tunslip6 -t tapOTHER -T -s /tmp/slip.devOTHER 2001:db8::1/64 &
   make -Cbuild run QEMU_INSTANCE=OTHER

.. _`net-tools`: https://github.com/zephyrproject-rtos/net-tools
