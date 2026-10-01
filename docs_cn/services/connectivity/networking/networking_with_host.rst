.. _networking_with_host:

Networking with the host system
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

开发 networking software 时（通常须连接并与 host system（如 Linux desktop computer）交换 data。
取决于开发所用 board（以下 options 可能：

* QEMU 用 SLIP (Serial Line Internet Protocol)。

  * 这里 IP packets 在 Zephyr 和 host system 间通过 serial
    port 交换。此为传输 data 的 legacy 方式。其也相当慢（故
    仅在必要时使用。细节参见 :ref:`networking_with_qemu`。

* QEMU 用内置 Ethernet driver。

  * 这里 IP packets 在 Zephyr 和 host system 间通过 QEMU 的
    内置 Ethernet driver 交换。并非所有 QEMU boards 支持内置 Ethernet（故
    某些情况下（可能须用 SLIP method 进行 host connectivity。
    细节参见 :ref:`networking_with_eth_qemu`。

* QEMU 用 SLIRP (Qemu User Networking)。

  * QEMU User Networking 用 "slirp" 实现（其在 QEMU 内提供完整 TCP/IP
    stack（并用该 stack 实现虚拟 NAT'd network。由于
    此支持内置于 QEMU（其可用于任何 model（且无需 host machine 上的
    admin privileges（不同于 TAP。然而（其有若干
    limitations（包括 performance（使其对实际
    目的价值较低。细节参见 :ref:`networking_with_user_qemu`。

* Arm FVP (User Mode Networking)。

  * User mode networking 模拟内置 IP router 和 DHCP server（并
    在 guest 和 host 之间路由 TCP 和 UDP traffic。其用 host 的 user mode
    socket layer 与其他 hosts 通信。这允许
    使用大量 IP network services（无需
    administrative privileges（或无需在 model 运行的 host 上安装单独 driver。细节参见 :ref:`networking_with_armfvp`。

* native_sim board。

  * Zephyr instance 可作为 host
    system 中的 user space process 执行。这是调试 Zephyr system 最方便的方式（因为
    可直接将 host debugger 附加到运行中的 Zephyr instance。这
    要求 Zephyr 中有与 host system 接口的 adaptation driver。两个可能的 network drivers 可用于此
    目的（TAP 虚拟 Ethernet driver 和 offloaded sockets driver。
    细节参见 :ref:`networking_with_native_sim`。

* USB device networking。

  * 这里（Zephyr instance 在真实 board 上运行（且与
    host system 的 connectivity 通过 USB 完成。
    细节参见 :ref:`usb_device_networking_setup`。

* 将多个 Zephyr instances 连接在一起。

  * 若有多个 Zephyr instances（QEMU 或 native_sim 的（且
    想在它们之间创建 connection（参见
    :ref:`networking_with_multiple_instances` 了解细节。

* 模拟两个 QEMU 间的 IEEE 802.15.4 network。

  * 这里（两个 Zephyr instances 运行（且它们之间在 UART 上
    运行 IEEE 802.15.4 link layer。
    细节参见 :ref:`networking_with_ieee802154_qemu`。

* 用 native_sim 模拟 Ethernet bridge network。

  * 这里（一个 Zephyr instance 运行（通过 :kconfig:option:`CONFIG_NET_ETHERNET_BRIDGE` Kconfig option 启用 Ethernet bridge。存在
    两个 host network interfaces ``zeth0`` 和 ``zeth1``（且 network
    packets 在两个 interfaces 之间 bridged。
    细节参见 :ref:`networking_with_native_sim_eth_bridge`。
