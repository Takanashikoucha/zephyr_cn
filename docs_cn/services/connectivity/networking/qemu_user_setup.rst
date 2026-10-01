.. _networking_with_user_qemu:

Networking with QEMU User
#############################

.. contents::
    :local:
    :depth: 2

此页面旨在作为对使用 QEMU SLIRP 与 Zephyr 感兴趣者的起点。

Introduction
*************

SLIRP 为在
QEMU 内提供完整 TCP/IP stack 的 network backend（并用该 stack 实现虚拟 NAT'd network。由于
对 host 无 dependencies（SLIRP 设置简单。

默认（QEMU 使用 ``10.0.2.X/24`` network（并在
``10.0.2.2`` 运行 gateway。所有发往 host network 的 traffic 须
通过此 gateway（其根据 QEMU command line
parameters 过滤 packets。此 gateway 还作为所有 GOS 的 DHCP server（
允许其自动分配从
``10.0.2.15`` 开始的 IP address。

User Networking 更多细节可从 https://wiki.qemu.org/Documentation/Networking#User_Networking_.28SLIRP.29 获取。

Using SLIRP with Zephyr
************************

要用 SLIRP 与 Zephyr（user 须设置 Kconfig option
以启用 User Networking。

.. code-block:: cfg

   CONFIG_NET_QEMU_USER=y

启用此 configuration option 后（所有 QEMU launches 将使用 SLIRP。
默认配置中（Zephyr 仅启用 User Networking（且
不向其传递任何 arguments。这意味着 Guest 仅能
与 QEMU gateway 通信（且发往 host machine 的任何 data
将被 QEMU 丢弃。

通常（QEMU User Networking 可接受大量 arguments（包括，

* 关于 host/guest port forwarding 的信息。须提供
  以在 guest 和 host 之间创建 communication channel。
* 关于使用 network 的信息。若 user
  不想用默认 ``10.0.2.X`` network（此可能有价值。
* 告知 QEMU 在 user-defined IP address 启动 DHCP server。
* ID 和其他信息。

由于此信息随每个 use case 变化（难以想出
适用于所有的好 defaults。因此（Zephyr Implementation
将此 offload 给 user（并期望其根据 requirements 提供
arguments。为此（有 user 可填充的 Kconfig string。

.. code-block:: cfg

   CONFIG_NET_QEMU_USER_EXTRA_ARGS="net=192.168.0.0/24,hostfwd=tcp::8080-:8080"

此 option 原样追加到 QEMU command line。因此（此
command line 的任何问题仅由 QEMU 报告。此特定
example 将做，

* 使 QEMU 用 ``192.168.0.0/24`` network 替代默认。
* 启用将从 host port 8080 收到的任何 TCP data 转发到 guest
  port 8080（反之亦然。

Limitations
*************

若 user 除从 guest 访问 web page 的能力外无特定 networking requirements（user networking (slirp) 是
好选择。然而（其有若干 limitations

* Overhead 大（故 performance 差。
* Guest 无法从 host 或 external network 直接访问。
* 通常（ICMP traffic 不工作（故 guest 内不能用 ping）。
* 由于 port mappings 须在启动 qemu 前定义（使用
  动态生成 ports 的 clients 无法与 external network 通信。
* SLIRP 实现有 bug（其过滤 guest 的所有 IPv6 packets
  。细节参见 https://bugs.launchpad.net/qemu/+bug/1724590。
  因此（IPv6 在 User Networking 中不工作。
