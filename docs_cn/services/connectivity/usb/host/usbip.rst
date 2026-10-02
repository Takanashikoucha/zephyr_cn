.. _usbip:

USB/IP 协议支持
#######################

概述
********

新的 USB 支持包含对 USB/IP 协议的初步支持。它仍在开发中，目前仅限于支持连接到被导出的主机控制器的单个设备。

USB/IP 使用 TCP/IP。其底层两个互连栈（USB 和网络）都需要大量的内存资源，在选择平台时必须考虑这一点。

在 USB/IP 协议中，服务器导出 USB 设备，客户端导入它们。Zephyr RTOS 中的 USB/IP 支持实现了服务器功能，在运行 Zephyr RTOS 的设备上导出连接到主机控制器的设备。客户端（通常运行 Linux 内核）导入该设备。USB/IP 协议在 `USB/IP 协议文档`_ 中有描述。

要使用 USB/IP 支持，请确保客户端已加载所需的模块。

.. code-block:: console

   modprobe vhci_hcd
   modprobe usbip-core
   modprobe usbip-host

在客户端，还需要 **usbip** 用户工具。它可以通过 Linux 发行版的包管理系统安装，也可以从 Linux 内核源码构建。

日常使用有几个基本命令。要列出已导出的 USB 设备，运行以下命令：

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

要附加一个 busid 为 1-1 的已导出设备：

.. code-block:: console

   $ sudo usbip attach -r 192.0.2.1 -b 1-1

要分离端口 0 上的已导出设备：

.. code-block:: console

   $ sudo usbip detach -p 0

使用 native_sim 的 USB/IP
**********************

在启用 USB/IP 支持的情况下进行开发的首选方法是使用 :zephyr:board:`native_sim <native_sim>`。在真实硬件上的使用目前尚未真正测试过。
USB/IP 需要网络连接，客户端如何设置接口参见 :ref:`networking_with_native_sim`。

构建和运行使用 USB/IP 的示例需要大量配置，可以使用 usbip-native-sim 片段来配置主机和 USB/IP 支持。

.. zephyr-app-commands::
   :zephyr-app: samples/subsys/usb/cdc_acm
   :board: native_sim/native/64
   :gen-args: -DSNIPPET=usbip-native-sim -DEXTRA_DTC_OVERLAY_FILE=app.overlay
   :goals: build

.. _USB/IP 协议文档: https://www.kernel.org/doc/html/latest/usb/usbip_protocol.html
