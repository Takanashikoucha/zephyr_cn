.. _networking_with_host:

与主机系统进行网络通信
###############################

.. toctree::
   :maxdepth: 1
   :hidden:

   native_sim_setup.rst
   qemu_eth_setup.rst
   qemu_setup.rst
   usbnet_setup.rst
   qemu_user_setup.rst
   networking_with_multiple_instances.rst
   eth_bridge_native_sim_setup.rst
   qemu_802154_setup.rst
   armfvp_user_networking_setup.rst

在开发网络软件时，通常需要像连接 Linux 桌面计算机这样的主机系统，并与之交换数据。
根据开发所用的单板，有以下几种可能的方案：

* 使用 SLIP（串行线路互联网协议）的 QEMU。

  * 这里 IP 数据包通过串口在 Zephyr 和主机系统之间交换。这是传输数据的传统方式。由于速度相当慢，因此仅在有必要时使用。详情请参见 :ref:`networking_with_qemu`。

* 使用内置以太网驱动程序的 QEMU。

  * 这里 IP 数据包通过 QEMU 的内置以太网驱动程序在 Zephyr 和主机系统之间交换。并非所有 QEMU 单板都支持内置以太网，因此在某些情况下，你可能需要使用 SLIP 方式来实现与主机的连接。详情请参见 :ref:`networking_with_eth_qemu`。

* 使用 SLIRP（Qemu 用户网络）的 QEMU。

  * QEMU 用户网络使用 "slirp" 实现，它在 QEMU 内部提供一个完整的 TCP/IP 协议栈，并利用该协议栈实现一个虚拟 NAT 网络。由于此支持内置于 QEMU 中，它可以用于任何模型，并且与 TAP 不同，在主机上不需要管理员权限。然而，它存在若干限制，包括性能方面的不足，这使其在实际用途中的价值较低。详情请参见 :ref:`networking_with_user_qemu`。

* Arm FVP（用户模式网络）。

  * 用户模式网络模拟一个内置 IP 路由器和 DHCP 服务器，并在客户机与主机之间路由 TCP 和 UDP 流量。它使用主机的用户模式套接字层与其他主机通信。这使得无需管理员权限，也无需在运行该模型的主机上安装单独的驱动程序，就可以使用大量 IP 网络服务。详情请参见 :ref:`networking_with_armfvp`。

* native_sim 单板。

  * Zephyr 实例可以作为主机系统中的用户空间进程来运行。这是调试 Zephyr 系统最便捷的方式，因为可以直接将主机调试器附加到正在运行的 Zephyr 实例上。这要求 Zephyr 中存在一个适配驱动程序，用于与主机系统交互。可以使用两种网络驱动程序来实现此目的：TAP 虚拟以太网驱动程序和卸载（offloaded）套接字驱动程序。详情请参见 :ref:`networking_with_native_sim`。

* USB 设备网络。

  * 这里，Zephyr 实例运行在真实单板上，与主机系统的连接通过 USB 完成。
  详情请参见 :ref:`usb_device_networking_setup`。

* 将多个 Zephyr 实例连接在一起。

  * 如果你有多个 Zephyr 实例（无论是 QEMU 还是 native_sim），并希望在其之间建立连接，详情请参见 :ref:`networking_with_multiple_instances`。

* 在两个 QEMU 之间仿真 IEEE 802.15.4 网络。

  * 这里，两个 Zephyr 实例正在运行，它们之间通过 UART 运行 IEEE 802.15.4 链路层。
  详情请参见 :ref:`networking_with_ieee802154_qemu`。

* 使用 native_sim 仿真以太网桥接网络。

  * 这里，一个 Zephyr 实例正在运行，并通过 :kconfig:option:`CONFIG_NET_ETHERNET_BRIDGE` Kconfig 选项启用了以太网桥接。存在两个主机网络接口 ``zeth0`` 和 ``zeth1``，网络数据包在这两个接口之间进行桥接。
  详情请参见 :ref:`networking_with_native_sim_eth_bridge`。
