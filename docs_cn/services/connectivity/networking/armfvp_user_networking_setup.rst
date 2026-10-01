.. _networking_with_armfvp:

Networking with Arm FVP User Mode
#################################

.. contents::
    :local:
    :depth: 2

此页面旨在作为对使用 Arm FVP user mode networking 与 Zephyr 感兴趣者的起点。

Introduction
*************

User mode networking 模拟内置 IP router 和 DHCP server（并在 guest 和 host 之间路由 TCP 和 UDP traffic。其用 host 的 user mode socket layer 与其他 hosts 通信。这允许使用大量 IP network services（无需 administrative privileges（或无需在安装 model 运行的 host 上安装单独 driver。

默认（Arm FVP 使用 ``172.20.51.0/24`` network（并在 ``172.20.51.254`` 运行 gateway。此 gateway 还作为 GOS 的 DHCP server（允许其自动分配 IP address ``172.20.51.1``。

Arm FVP user mode networking 更多细节可从 https://developer.arm.com/documentation/100964/latest/Introduction-to-Fast-Models/User-mode-networking 获取。

Using Arm FVP User Mode Networking with Zephyr
***********************************************

Arm FVP user mode networking 可在任何 applications 中启用（且无需在 host system 上任何 configurations。此 feature 已在 DHCPv4 client sample 中启用。参见 :zephyr:code-sample:`dhcpv4-client` sample application。

Limitations
*************

* 可用 TCP 和 UDP over IP（但不可用 ICMP（ping）。
* User mode networking 不支持将 host 上的 UDP ports 转发到 model。
* 仅可在 private network 内使用 DHCP。
* 仅可通过将 host 上的 TCP ports 映射到 model 建立 inward connections。这对用 NAT 提供 host connectivity 的所有 implementations 通用。
* 需 privileged source ports 的 operations（例如默认配置下的 NFS）不工作。
* 若 setup 失败（或 parameter 语法不正确（无 error 报告。
