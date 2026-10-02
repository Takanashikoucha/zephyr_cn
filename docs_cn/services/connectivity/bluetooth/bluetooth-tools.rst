.. _bluetooth-tools:

工具
#####

本页列出并描述可用于协助蓝牙协议栈或应用开发过程中的工具，以帮助、简化和加速开发过程。

.. contents::
    :local:
    :depth: 2

.. _bluetooth-mobile-apps:

移动应用
*******************

利用现有的移动应用与运行 Zephyr 的硬件交互通常非常有用，可以测试功能而无需编写任何额外代码或需要额外硬件。

推荐用于与 Zephyr 交互的移动应用：

* Android：

  * `nRF Connect for Android`_
  * `nRF Mesh for Android`_
  * `LightBlue for Android`_

* iOS：

  * `nRF Connect for iOS`_
  * `nRF Mesh for iOS`_
  * `LightBlue for iOS`_

.. _bluetooth_bluez:

在 Zephyr 中使用 BlueZ
***********************

Linux 蓝牙协议栈 BlueZ 附带一组非常有用的工具，可用于调试和交互 Zephyr 的蓝牙 Host 和
Controller。为了受益于这些工具，你需要确保运行的是较新版本的 Linux 内核和 BlueZ：

* Linux 内核 4.10+
* BlueZ 4.45+

此外，某些 BlueZ 工具可能默认未包含在你的 Linux 发行版中。如果你需要从头构建 BlueZ 以更新到
较新版本或获取其所有工具，可以遵循以下步骤：

.. code-block:: console

   git clone git://git.kernel.org/pub/scm/bluetooth/bluez.git
   cd bluez
   ./bootstrap-configure --disable-android --disable-midi
   make

然后你可以在
:file:`tools/` 文件夹中找到 :file:`btattach`、:file:`btmgt` 和 :file:`btproxy`，
在 :file:`monitor/` 文件夹中找到 :file:`btmon`。

你需要启用 BlueZ 的实验特性，以便访问其
最新的蓝牙功能。通过编辑文件
:file:`/lib/systemd/system/bluetooth.service`
并确保在守护进程的启动行中包含 :literal:`-E` 选项来实现：

.. code-block:: console

   ExecStart=/usr/libexec/bluetooth/bluetoothd -E

最后，重新加载并重启守护进程：

.. code-block:: console

   sudo systemctl daemon-reload
   sudo systemctl restart bluetooth

.. _bluetooth_qemu_native:

在 QEMU 或 native_sim 上运行
*****************************

可以使用 :ref:`QEMU
模拟器<application_run_qemu>` 或 :zephyr:board:`native_sim <native_sim>` 运行蓝牙应用。

无论哪种情况，都需要从
主机操作系统（Linux）向模拟器导出一个蓝牙控制器。为此，你需要一些
:ref:`bluetooth_bluez` 一节中描述的工具。

使用主机系统的蓝牙控制器
==========================================

主机操作系统的蓝牙控制器按以下方式连接：

* 通过 UNIX 套接字连接到第二个 QEMU 串口。该套接字借助
  QEMU 选项 :literal:`-serial unix:/tmp/bt-server-bredr` 使用。
  每当应用启用了蓝牙支持时，该选项会通过 :makevar:`QEMU_EXTRA_FLAGS`
  自动传递给 QEMU。
* 通过传递给 native_sim 可执行文件的命令行选项 ``--bt-dev=hci0``
  连接到 :ref:`native_sim 的 BT User Channel 驱动 <nsim_bt_host_cont>`

在主机侧，BlueZ 允许你通过所谓的用户信道导出其蓝牙控制器
供 QEMU 和 :zephyr:board:`native_sim <native_sim>` 使用。

.. note::
   仅在使用 QEMU 时需要运行 ``btproxy``。native_sim 自动处理
   UNIX 套接字代理

如果你使用 QEMU，为了让 Controller 可用，你需要
使用 ``btproxy`` 额外执行一步：

#. 确保蓝牙控制器已关闭

#. 使用 btproxy 工具打开监听 UNIX 套接字，类型：

   .. code-block:: console

      sudo tools/btproxy -u -i 0
      Listening on /tmp/bt-server-bredr

   你可能需要将 :literal:`-i 0` 替换为你希望代理的
   Controller 的索引。

   如果在运行 QEMU 时看到 ``Received unknown host packet type 0x00``，则
   在 ``btproxy`` 命令行中添加 :literal:`-z` 以忽略启动时传输的任何空字节。

硬件连接并准备就绪后，你就可以继续
构建和运行示例：

* 选择 :literal:`samples/bluetooth` 中的一个蓝牙示例应用。

* 要在 QEMU 中运行蓝牙应用，类型：

  .. zephyr-app-commands::
     :zephyr-app: samples/bluetooth/<sample>
     :host-os: unix
     :board: qemu_x86
     :goals: run
     :compact

  现在运行 QEMU 会建立与
  :literal:`bt-server-bredr` UNIX 套接字的第二个串口连接，
  使应用能够访问蓝牙控制器。

* 要在 :zephyr:board:`native_sim <native_sim>` 中运行蓝牙应用，先构建它：

  .. zephyr-app-commands::
     :zephyr-app: samples/bluetooth/<sample>
     :host-os: unix
     :board: native_sim
     :goals: build
     :compact

  然后运行::

     $ sudo ./build/zephyr/zephyr.exe --bt-dev=hci0

使用基于 Zephyr 的蓝牙控制器
=========================================

根据你可用的硬件，构建单模、基于 Zephyr 的蓝牙控制器时
可以在两种传输之间选择：

* UART：使用 :zephyr:code-sample:`bluetooth_hci_uart` 示例并遵循
  :ref:`bluetooth-hci-uart-qemu-posix` 中的说明。
* USB：使用 :zephyr:code-sample:`bluetooth_hci_usb` 示例，然后
  将其视为主机系统的蓝牙控制器（见上一节）

.. _bluetooth-hci-tracing:

HCI 跟踪
===========

当在连接到外部控制器的计算机上运行 Host 时，
能够以 :ref:`bluetooth-hci` 日志的格式查看两者之间交换的完整日志
会非常有用的。
为了查看这些日志，你可以使用 BlueZ 内置的 ``btmon`` 工具：

.. code-block:: console

   $ btmon

输出如下::

   = New Index: 00:00:00:00:00:00 (Primary,Virtual,Control)                     0.274200
   = Open Index: 00:00:00:00:00:00                                              0.274500
   < HCI Command: Reset (0x03|0x0003) plen 0                                 #1 0.274600
   > HCI Event: Command Complete (0x0e) plen 4                               #2 0.274700
         Reset (0x03|0x0003) ncmd 1
         Status: Success (0x00)
   < HCI Command: Read Local Supported Features (0x04|0x0003) plen 0         #3 0.274800
   > HCI Event: Command Complete (0x0e) plen 12                              #4 0.274900
         Read Local Supported Features (0x04|0x0003) ncmd 1
         Status: Success (0x00)
         Features: 0x00 0x00 0x00 0x00 0x60 0x00 0x00 0x00
            BR/EDR Not Supported
            LE Supported (Controller)

.. _bluetooth-embedded-hci-tracing:

嵌入式 HCI 跟踪
--------------------

当在真实的集成电路中同时运行 Host 和 Controller 时，
默认情况下你只能在控制台上看到普通日志消息，
没有访问 Host 与 Controller 之间 HCI 流量的方式。
然而，有一种特殊的蓝牙日志模式，将控制台转换为使用二进制
协议，该协议交替包含普通日志消息和 HCI 流量。

在构建应用之前，设置以下 Kconfig 选项以启用该协议：

.. code-block:: cfg

   CONFIG_BT_DEBUG_MONITOR_UART=y
   CONFIG_UART_CONSOLE=n

- 设置 :kconfig:option:`CONFIG_BT_DEBUG_MONITOR_UART` 会激活格式化
- 清除 :kconfig:option:`CONFIG_UART_CONSOLE` 会使 UART 无法用于
  系统控制台。例如用于 ``printk`` 和 :kconfig:option:`boot banner
  <CONFIG_BOOT_BANNER>`

可选地，在监视 UART 驱动支持中断 API 的板子上，
设置 :kconfig:option:`CONFIG_BT_DEBUG_MONITOR_UART_INTERRUPT_DRIVEN`
会排队完整的监视记录，并从 UART 中断处理程序传输它们，
而不是在传输每个字节时阻塞。不适合缓冲区的记录
会被丢弃并在下一个监视记录中报告。缓冲区
大小可通过
:kconfig:option:`CONFIG_BT_DEBUG_MONITOR_UART_BUFFER_SIZE` 调整。

要解码现在将发送到控制台 UART 的二进制协议，
你需要使用 :ref:`BlueZ <bluetooth_bluez>` 的 btmon 工具：

.. code-block:: console

   $ btmon --tty <console TTY> --tty-speed 115200

如果 UART 不可用（或你仍然想要非二进制日志），
可以改为设置
:kconfig:option:`CONFIG_BT_DEBUG_MONITOR_RTT`，这将使用 Segger
RTT。例如，如果尝试通过 S/N 683578642 连接到 nRF52840DK：

.. code-block:: console

   $ btmon --jlink nRF52840_xxAA,683578642

.. _bluetooth_virtual_posix:

在虚拟控制器和 native_sim 上运行
**********************************************

蓝牙物理控制器的替代方案是使用虚拟
控制器。该控制器可以通过 HCI TCP 服务器连接。
该 TCP 服务器必须支持 HCI H4 协议。与物理控制器
变体相比，虚拟控制器允许在没有物理蓝牙控制器的情况下测试运行在 native
板子上的 Zephyr 应用。

虚拟控制器的主要用例是在
无需蓝牙硬件的情况下进行蓝牙连接测试。这使得能够使用
外部应用（如蓝牙网关或移动应用）自动化蓝牙集成测试。

为了演示此功能，给出了一个与虚拟控制器交互的示例。
为此，使用 Google 的实验性 python 模块 `Bumble`_，因为它允许创建
TCP 蓝牙虚拟控制器并与 Zephyr 蓝牙 host 连接。要安装
bumble，请遵循 `Bumble Getting Started Guide`_。

.. note::
   如果你的 Zephyr 应用需要使用 HCI LE Set extended 命令，请安装
   Bumble 的 ``controller-extended-advertising`` 分支。

Android 模拟器
=================

你可以通过将蓝牙 Zephyr 应用
连接到 `Android Emulator`_ 来测试虚拟控制器。

要将你的应用连接到 Android 模拟器，请遵循以下步骤：

    #. 构建你的 Zephyr 应用并禁用 HCI ACL 流
       控制（即 ``CONFIG_BT_HCI_ACL_FLOW_CONTROL=n``），因为
       android 的虚拟控制器目前不支持它。

    #. 安装 Android 模拟器版本 >= 33.1.4.0。最简单的方式是安装
       最新版本的 `Android Studio Preview`_。

    #. 使用 `Android Device Manager`_ 创建一个新的 Android 虚拟设备（AVD）。AVD 应至少使用 SDK API 34。

    #. 通过终端按以下方式运行 Android 模拟器：

       ``emulator avd YOUR_AVD -packet-streamer-endpoint default``

    #. 使用 `Bumble`_ 实用工具 ``hci-bridge`` 在 Zephyr 应用和
       Android 模拟器的虚拟控制器之间创建蓝牙桥接。

       ``bumble-hci-bridge tcp-server:_:1234 android-netsim``

       该命令将在本地主机 IP 地址 ``127.0.0.1``
       和端口号 ``1234`` 上创建 TCP 服务器桥接。

    #. 运行 Zephyr 应用并连接到上一步创建的 TCP 服务器。

       ``./zephyr.exe --bt-dev=127.0.0.1:1234``

遵循这些步骤后，Zephyr 应用将通过
使用 Bumble 桥接的虚拟蓝牙控制器对 Android 模拟器可用。
你可以打开 AVD 中的蓝牙设置并扫描你的 Zephyr 应用设备来验证
Zephyr 应用能否通过蓝牙通信。为此，你可以构建蓝牙
peripheral 示例，如 :zephyr:code-sample:`ble_peripheral_hr` 或
:zephyr:code-sample:`ble_peripheral_dis`。

.. _bluetooth_ctlr_bluez:

使用 BlueZ 的基于 Zephyr 的控制器
*****************************************

如果你想使用 BlueZ 的蓝牙
Host 测试由 Zephyr 驱动的蓝牙 Controller，
你需要 :ref:`bluetooth_bluez` 一节中描述的几件工具。
安装工具后，你就可以使用它们与你的
基于 Zephyr 的控制器交互：

   .. code-block:: console

      sudo tools/btmgmt --index 0
      [hci0]# auto-power
      [hci0]# find -l

你可能需要将 :literal:`--index 0` 替换为你希望管理的
Controller 的索引。
关于 :file:`btmgmt` 的更多信息可在其手册页中找到。


.. _nRF Connect for Android: https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=en
.. _nRF Connect for iOS: https://itunes.apple.com/us/app/nrf-connect/id1054362403
.. _LightBlue for Android: https://play.google.com/store/apps/details?id=com.punchthrough.lightblueexplorer&hl=en_US
.. _LightBlue for iOS: https://itunes.apple.com/us/app/lightblue-explorer/id557428110
.. _nRF Mesh for Android: https://play.google.com/store/apps/details?id=no.nordicsemi.android.nrfmeshprovisioner&hl=en
.. _nRF Mesh for iOS: https://itunes.apple.com/us/app/nrf-mesh/id1380726771
.. _Bumble: https://github.com/google/bumble
.. _Bumble Getting Started Guide: https://google.github.io/bumble/getting_started.html
.. _Android Emulator: https://developer.android.com/studio/run/emulator
.. _Android Device Manager: https://developer.android.com/studio/run/managing-avds
.. _Android Studio Preview: https://developer.android.com/studio/preview
