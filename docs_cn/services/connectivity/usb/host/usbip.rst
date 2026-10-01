.. _usbip:

USB/IP protocol support
#######################

Overview
********

新 USB 支持包括对 USB/IP protocol 的 initial support。其仍
在开发中（且当前限于仅支持连接到
被导出 host controller 的一个 device。

USB/IP 用 TCP/IP。两个底层 connectivity stacks（USB 和
networking）均需大量 memory resources（选择
platform 时须考虑。

在 USB/IP protocol 中（server 导出 USB devices（client
导入它们。Zephyr RTOS 中的 USB/IP 支持实现 server functionality（
并导出连接到运行 Zephyr
RTOS 的 device 上 host controller 的 device。
Client（通常运行 Linux kernel）导入此 device。USB/IP protocol 描述在 `USB/IP protocol documentation`_。

要用 USB/IP 支持（确保 client 侧加载所需 modules。

.. code-block:: console

   modprobe vhci_hcd
   modprobe usbip-core
   modprobe usbip-host

在 client 侧（还需 **usbip** user tool。其可
用 Linux distribution 的 package management system 安装（或从 Linux
kernel sources 构建。

日常使用有若干基本 commands。要列出导出的 USB devices（
运行以下 command：

.. code-block:: console

   $ usbip list -r 192.0.2.1
   Exportable USB devices
   ======================
    - 192.0.2.1
           1-1: NordicSemiconductor : unknown product (2fe3:0001)
              : /sys/bus/usb/devices/usb1/1-1
              : Miscellaneous Device / ? / Interface Association (ef/02/01)
              :  0 - Communications / Abstract (modem) / None (02/02/00)
              :  1 - CDC Data / Unused / unknown protocol (0a/00/00)

要附加 busid 为 1-1 的导出 device：

.. code-block:: console

   $ sudo usbip attach -r 192.0.2.1 -b 1-1

要分离 port 0 上的导出 device：

.. code-block:: console

   $ sudo usbip detach -p 0

USB/IP with native_sim
**********************

启用 USB/IP 支持开发的首选方法为使用
:zephyr:board:`native_sim <native_sim>`。在真实 hardware 上的使用尚未经过充分测试。
USB/IP 需 network connection（client 侧如何设置
interface 参见 :ref:`networking_with_native_sim`。

构建并运行带 USB/IP 的 sample 需大量 configuration（
可用 usbip-native-sim snippet 配置 host 和 USB/IP 支持。

.. zephyr-app-commands::
   :zephyr-app: samples/subsys/usb/cdc_acm
   :board: native_sim/native/64
   :gen-args: -DSNIPPET=usbip-native-sim -DEXTRA_DTC_OVERLAY_FILE=app.overlay
   :goals: build

.. _USB/IP protocol documentation: https://www.kernel.org/doc/html/latest/usb/usbip_protocol.html
