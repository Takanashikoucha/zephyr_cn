:orphan:

.. _nordic_segger:

Nordic nRF5x Segger J-Link
##########################

概览
********

所有 Nordic nRF5x 开发套件、预览开发套件和 Dongle 都配备一个调试 IC（Atmel ATSAM3U2C），提供以下功能：

* Segger J-Link 固件和桌面工具
* nRF5x IC 的 SWD 调试
* 拖放镜像烧录的大容量存储设备
* 桥接到 nRF5x UART 外设的 USB CDC ACM 串口
* Segger RTT 控制台
* Segger Ozone 调试器

Segger J-Link 软件安装
***********************************

要安装 J-Link 软件和文档包，遵循以下步骤：

#. 从 `J-Link Software and documentation pack`_ 网站下载适当的包
#. 取决于你的平台，安装包或运行安装器
#. 当连接一个 J-Link 使能的开发板如 nRF5x DK、PDK 或 dongle 时，对应 USB 大容量存储设备的驱动器和一个串口应该出现

nRF5x 命令行工具安装
*************************************

nRF5x 命令行工具允许你从命令行控制你的 nRF5x 设备，包括重置它、擦除或编程 flash 内存等。

要安装它们，访问 `nRF5x Command-Line Tools`_ 并选择你的操作系统。

安装后，确保 ``nrfjprog`` 在你的可执行路径某处以能够从任何地方调用它。

.. _nordic_segger_flashing:

烧录
********

在遵循安装 Segger J-Link 软件和 nRF5x 命令行工具的说明后，要用编译的 Zephyr 镜像编程 flash，遵循以下步骤：

* 将 micro-USB 线连接到 nRF5x 开发板和你的电脑
* 擦除 nRF5x IC 中的 flash 内存：

.. code-block:: console

   nrfjprog --eraseall -f nrf5<x>

其中 ``<x>`` 是 1 用于 nRF51 基于的开发板或 2 用于 nRF52 基于的开发板

* 从你选择的示例文件夹烧录 Zephyr 镜像：

.. code-block:: console

   nrfjprog --program outdir/<board>/zephyr.hex -f nrf5<x>

其中：``<board>`` 是你在构建时 BOARD 指令中使用的开发板名称（例如 nrf52dk/nrf52832）且 ``<x>`` 是 1 用于 nRF51 基于的开发板或 2 用于 nRF52 基于的开发板

* 重置并启动 Zephyr：

.. code-block:: console

   nrfjprog --reset -f nrf5<x>

其中 ``<x>`` 是 1 用于 nRF51 基于的开发板或 2 用于 nRF52 基于的开发板

USB CDC ACM 串口设置
*****************************

**重要注意**：nRF5x 开发板上的 Segger J-Link 固件的一个问题可能导致某些机器上 USB CDC ACM 串口的数据丢失和/或损坏。要绕过这在你的开发板上禁用大容量存储设备如 :ref:`nordic_segger_msd` 中描述的。

Windows
=======

串口将出现为 ``COMxx``。只需要检查设备管理器中的 "Ports (COM & LPT)" 章节。

GNU/Linux
=========

串口将出现为 ``/dev/ttyACMx``。默认情况下端口不对所有用户可访问。键入下面的命令将你的用户添加到 dialout 组以给它串口访问权限。注意这需要重新登录才生效。

.. code-block:: bash

   sudo usermod -a -G dialout `whoami`

较新版本的 ModemManager 会向 TTY 类设备发送 AT 命令（见 `ModemManager 向 TTY 类设备发送 AT 命令`_），这包括 Nordic 开发套件。这将阻止你使用串口几秒，并可能使你的应用行为异常（如果它从 UART 读取数据）。运行你的应用前，你可能想通过运行以下命令临时禁用 ModemManager：

.. code-block:: bash

   systemctl stop ModemManager.service
   systemctl disable ModemManager.service

你也可以通过 `编辑 udev 规则将 Segger 设备加入黑名单`_ 使 ModemManager 忽略它们，运行：

.. code-block:: bash

   sudo sh -c 'echo "ATTRS{idVendor}==\"1366\", ENV{ID_MM_DEVICE_IGNORE}=\"1\" " \
     >> /etc/udev/rules.d/99-segger-modemmanager-blocklist.rules'
   sudo service udev restart

此问题的修复预计在 ModemManager 1.8 和 Segger IMCU 的新固件中。

Apple macOS（OS X）
==================

串口将出现为 ``/dev/tty.usbmodemXXXX``。

.. _nordic_segger_msd:

禁用大容量存储设备功能
***********************************************

由于 Segger 的 J-Link 固件中的一个已知问题，取决于你的操作系统和版本，如果你用大于 64 字节的包使用 USB CDC ACM 串口你可能遇到数据损坏或丢失。这在 GNU/Linux 和 macOS（OS X）上都被观察到。

要避免此问题，你只需打开以下程序来禁用大容量存储设备：

* 在 GNU/Linux 或 macOS（OS X）从终端打开 JLinkExe
* 在 Microsoft Windows 打开 "JLink Commander" 应用

然后键入以下：

.. code-block:: bat

   MSDDisable

最后拔掉并重新插入开发板。大容量存储设备将不再出现且你现在应该能在虚拟串口上发送长包。来自 Segger 的更多信息可以在 `Segger SAM3U Wiki`_ 中找到。

RTT 控制台
***********

Segger 的 J-Link 支持 `Real-Time Tracing (RTT)`_，一种允许在目标（nRF5x 开发板）和开发电脑之间建立终端连接（输入和输出）的技术用于日志和输入。Zephyr 支持 nRF5x 目标上的 RTT，如果 UART（通过 USB CDC ACM）已经被用于不同于日志的目的（如 hci_uart 应用中的 HCI 流量），这可能非常有用。要用 RTT，你首先需要通过在 ``.conf`` 文件中添加以下行来启用它：

.. code-block:: cfg

   CONFIG_USE_SEGGER_RTT=y
   CONFIG_RTT_CONSOLE=y

.. warning::

   还有一个 ``HAS_SEGGER_RTT`` 符号指示平台支持 SEGGER J-Link RTT。这个符号由 SoC Kconfig 文件自动设置。不要把它与 ``USE_SEGGER_RTT`` 混淆。

   ``USE_SEGGER_RTT`` 依赖于 ``HAS_SEGGER_RTT``。

如果你得不到 RTT 输出你可能需要禁用其他与 RTT 控制台冲突的控制台如果它们在特定示例或应用中被默认启用。例如，要禁用 UART 控制台，在你的 ``.conf`` 文件中添加这个：

.. code-block:: cfg

   CONFIG_UART_CONSOLE=n

一旦编译并烧录启用 RTT 后，你可以通过以下操作显示 RTT 控制台消息：

Windows
=======

* 打开 "J-Link RTT Viewer" 应用
* 选择以下选项：

  * Connection: USB
  * Target Device: 从列表选择你的 IC
  * Target Interface and Speed: SWD, 4000 KHz
  * RTT Control Block: Auto Detection

GNU/Linux 和 macOS（OS X）
==========================

* 从终端打开 ``JLinkRTTLogger``
* 选择以下选项：

  * Device Name: 用你的 IC 的完全限定设备名
  * Target Interface: SWD
  * Interface Speed: 4000 KHz
  * RTT Control Block address: 自动检测
  * RTT Channel name or index: 0
  * Output file: 文件名或 ``/dev/stdout`` 直接在终端显示

Python 查看器
=============

Python RTT 查看器工具可以在 `pyrtt-viewer`_ GitHub 仓库中找到。

Segger Ozone
************

Segger J-Link 与 `Segger Ozone`_ 兼容，一个可以从这里获取的可视化调试器：

* `Segger Ozone Download`_

下载后你可以安装并配置它如下：

* Target Device: 从列表选择你的 IC
* Target Interface: SWD
* Target Interface Speed: 4 MHz
* Host Interface: USB

配置后，你可以用 File->Open 菜单打开 ``zephyr.elf`` 文件你可以在构建文件夹中找到的那个。

参考
**********

.. target-notes::

.. _nRF5x Command-Line Tools:
   https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Command-Line-Tools

.. _Segger SAM3U Wiki:
   https://wiki.segger.com/J-Link-OB_SAM3U
.. _Real-Time Tracing (RTT):
   https://www.segger.com/jlink-rtt.html
.. _pyrtt-viewer:
   https://github.com/thomasstenersen/pyrtt-viewer
.. _Segger Ozone:
   https://www.segger.com/ozone.html
.. _Segger Ozone Download:
   https://www.segger.com/downloads/jlink#Ozone

.. _ModemManager send AT commands to TTY-like devices:
   https://bugs.freedesktop.org/show_bug.cgi?id=85007
.. _blocklist Segger devices by editing udev rules:
   http://www.at91.com/linux4sam/bin/view/Linux4SAM/SoftwareTools#Device_or_resource_busy_dev_ttyA

.. _J-Link Software and documentation pack:
   https://www.segger.com/jlink-software.html
