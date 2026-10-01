.. _debug-probes:

调试探针
############

*调试探针* 是特殊硬件，允许你控制运行在另一块开发板上的 Zephyr 应用的执行。调试探针通常允许读取和写入寄存器和内存，并支持用 GDB 等工具在你的主机工作站上对 Zephyr 应用做断点调试。它们可能也支持其他调试软件和更高级的功能如 :ref:`追踪程序执行 <tracing>`。关于 Zephyr 支持的相关主机软件的细节，见 :ref:`flash-debug-host-tools`。

调试探针通常通过 USB 连接到你的主机工作站；它们有时也可以通过 IP 网络或其他方式访问。它们通常用 JTAG 或 SWD 协议连接到运行 Zephyr 的设备。调试探针是独立的硬件设备或集成在运行 Zephyr 的相同开发板上的电路。

Zephyr 中许多受支持开发板包括一个第二微控制器，充当板载调试探针、USB 到串口适配器，有时还是拖放 flash 编程器。这消除了购买外部调试探针的需要并提供多种调试主机工具选项。

几个硬件厂商有他们自己品牌的板载调试探针实现：NXP 开发板可能用 `OpenSDA <#opensda-onboard-debug-probe>`_、`LPC-Link2 <#lpc-link2-onboard-debug-probe>`_ 或 `MCU-Link <#mcu-link-onboard-debug-probe>`_ 探针，取决于调试探针固件运行的微控制器。ST 开发板有 `ST-LINK 探针 <#stlink-v21-onboard-debug-probe>`_。每个板载调试探针微控制器可以支持一个或多个类型的固件与其各自的调试主机工具通信。例如，一个 OpenSDA 微控制器可以被编程 DAPLink 固件与 pyOCD 或 OpenOCD 调试主机工具通信，或编程 J-Link 固件与 J-Link 调试主机工具通信。


+------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
|| *调试探针和主机工具*             |                                                            主机工具                                                            |
+| *兼容性表*                   +--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                                          |  **J-Link 调试**  |    **OpenOCD**     |      **pyOCD**      |   **NXP S32DS**    | **NXP LinkServer** | **ST-LINK GDB Server** |
+----------------+-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **J-Link 外部**     |           ✓        |          ✓         |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **LPC-Link2 CMSIS-DAP** |                    |                    |                     |                    |         ✓          |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **LPC-Link2 J-Link**    |           ✓        |                    |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **MCU-Link CMSIS-DAP**  |                    |                    |                     |                    |         ✓          |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|  调试探针  +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **MCU-Link J-Link**     |           ✓        |                    |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **NXP S32 调试探针** |                    |                    |                     |          ✓         |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **OpenSDA DAPLink**     |                    |          ✓         |          ✓          |                    |         ✓          |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **OpenSDA J-Link**      |           ✓        |                    |                     |                    |                    |                        |
|                +-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+
|                | **ST-LINK/V2-1**        |           ✓        |          ✓         | *部分 STM32 开发板* |                    |                    |           ✓            |
+----------------+-------------------------+--------------------+--------------------+---------------------+--------------------+--------------------+------------------------+


Zephyr 中一些受支持开发板不包括板载调试探针，因此需要外部调试探针。此外，包括板载调试探针的开发板通常也有 SWD 或 JTAG 接头以启用使用外部调试探针代替。一个原因可能是板载调试探针可能有局限性，如缺乏对高级调试器或高速追踪的支持。你可能需要调整跳线以防止板载调试探针干扰外部调试探针。

.. _nxp-onboard-debug-probes:

NXP 板载调试探针
************************

NXP 开发板可能有几种板载调试探针之一。这些探针包括 :ref:`mcu-link-onboard-debug-probe`、:ref:`lpc-link2-onboard-debug-probe` 和 :ref:`opensda-onboard-debug-probe`。每个探针都实现为评估板上存在的第二微控制器。给定开发板上存在的具体调试探针类型可以基于调试微控制器 SoC 确定：

- LPC55S69: :ref:`mcu-link-onboard-debug-probe`
- LPC4322: :ref:`lpc-link2-onboard-debug-probe`
- MK20: :ref:`opensda-onboard-debug-probe`

例如，:zephyr:board:`frdm_k64f` 开发板有一个 MK20 调试微控制器，所以这个开发板使用 :ref:`opensda-onboard-debug-probe`。

.. _mcu-link-onboard-debug-probe:

MCU-Link 板载调试探针
****************************

MCU-Link 板载调试探针使用 LPC55S69 SoC。这个探针支持以下固件：

- :ref:`mcu-link-cmsis-onboard-debug-probe`（默认固件）
- :ref:`mcu-link-jlink-onboard-debug-probe`

这个探针用 MCU-Link 主机工具编程，这些工具随 :ref:`linkserver-debug-host-tools` 安装。NXP 推荐用 NXP 的 `MCUXpresso Installer`_ 安装 Linkserver 工具。

.. _mcu-link-cmsis-onboard-debug-probe:

MCU-Link CMSIS-DAP 板载调试探针
======================================

这是在 MCU-Link 调试探针上安装的默认固件。CMSIS-DAP 调试探针允许从任何兼容工具链调试，包括 IAR EWARM、Keil MDK、NXP 的 MCUXpresso IDE 和 VS Code 的 MCUXpresso 扩展。除了调试探针功能，MCU-Link 探针还可能提供：

1. SWO trace 端点：这个虚拟设备被 MCUXpresso 用于检索 SWO trace 数据。更多细节见 MCUXpresso IDE 文档。
#. 连接到目标处理器的虚拟 COM（VCOM）端口 / UART 桥
#. USB 到 UART、SPI 和/或 I2C 接口（取决于 MCU-Link 类型/实现）
#. 目标 MCU 的能量测量

这个调试探针与以下调试主机工具兼容：

- :ref:`linkserver-debug-host-tools`

一旦 MCU-Link 主机工具安装完毕，以下是在编程 CMSIS-DAP 固件前所需的步骤：

1. 确保 MCU-Link 工具在你的主机机器上存在。这可以通过安装 :ref:`linkserver-debug-host-tools` 来完成。

#. 通过附加 DFU 跳线然后连接到开发板上的 USB 调试端口将 MCU-Link 微控制器放入 DFU boot 模式。这个跳线也可能被称为 ISP 跳线，将连接到 LPC55S69 上的 ``PIO0_5``。

#. 运行 ``program_CMSIS`` 脚本，在安装的 MCU-Link ``scripts`` 文件夹中找到。

#. 移除 DFU 跳线并电源循环开发板。

.. _mcu-link-jlink-onboard-debug-probe:

MCU-Link JLink 板载调试探针
==================================

这个调试探针固件提供一个 J-Link 兼容的调试接口，以及一个 USB 转串口适配器。它与以下调试主机工具兼容：

- :ref:`jlink-debug-host-tools`

这些探针默认不安装 J-Link 固件，必须更新。一旦 MCU-Link 主机工具安装完毕，以下是在编程 J-Link 固件前所需的步骤：

1. 确保 MCU-Link 工具在你的主机机器上存在。这可以通过安装 :ref:`linkserver-debug-host-tools` 来完成。

#. 通过附加 DFU 跳线然后连接到开发板上的 USB 调试端口将 MCU-Link 微控制器放入 DFU boot 模式。这个跳线也可能被称为 ISP 跳线，将连接到 LPC55S69 上的 ``PIO0_5``。

#. 运行 ``program_JLINK`` 脚本，在安装的 MCU-Link ``scripts`` 文件夹中找到。

#. 移除 DFU 跳线并电源循环开发板。

.. _lpc-link2-onboard-debug-probe:

LPC-LINK2 板载调试探针
*****************************

LPC-LINK2 板载调试探针使用 LPC4322 SoC。这个探针支持以下固件：

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`lpclink2-jlink-onboard-debug-probe`
- :ref:`lpclink2-daplink-onboard-debug-probe`（默认固件）

这个探针用 LPCScrypt 主机工具编程，这些工具随 :ref:`linkserver-debug-host-tools` 安装。NXP 推荐用 NXP 的 `MCUXpresso Installer`_ 安装 Linkserver 工具。

.. _lpclink2-cmsis-onboard-debug-probe:

LPC-LINK2 CMSIS DAP 板载调试探针
=======================================

CMSIS-DAP 调试探针允许从任何兼容工具链调试，包括 IAR EWARM、Keil MDK，以及 NXP 的 MCUXpresso IDE 和 VS Code 的 MCUXpresso 扩展。除了提供调试探针功能，LPC-Link2 探针还提供：

1. SWO trace 端点：这个虚拟设备被 MCUXpresso 用于检索 SWO trace 数据。更多细节见 MCUXpresso IDE 文档。
2. 连接到目标处理器的虚拟 COM（VCOM）端口 / UART 桥
3. 提供与 I2C 和 SPI 外设设备通信的 LPCSIO 桥

这个调试探针固件与以下调试主机工具兼容：

- :ref:`linkserver-debug-host-tools`

探针可以用以下步骤更新以使用 CMSIS-DAP 固件：

1. 确保 LPCScrypt 工具在你的主机机器上存在。这可以通过安装 :ref:`linkserver-debug-host-tools` 做到。

#. 通过附加 DFU 跳线然后连接到开发板上的 USB 调试端口将 LPC-Link2 微控制器放入 DFU boot 模式。这个跳线连接到 LPC4322 SoC 上的 ``P2_6``。

#. 运行 ``program_CMSIS`` 脚本，在安装的 LPCScrypt ``scripts`` 文件夹中找到。

#. 移除 DFU 跳线并电源循环开发板。

.. _lpclink2-jlink-onboard-debug-probe:

LPC-Link2 J-Link 板载调试探针
====================================

.. note:: 在一些开发板上，J-Link 探针固件将不再通过 USB 调试端口给开发板供电。在这些开发板上，编程这个固件时必须使用替代方法给开发板供电。

这个调试探针固件提供一个 J-Link 兼容的调试接口，以及一个 USB 转串口适配器。它与以下调试主机工具兼容：

- :ref:`jlink-debug-host-tools`

探针可以用以下步骤更新以使用 J-Link 固件：

.. note:: 通过访问 `Firmware for LPCXpresso`_ 验证固件支持你的开发板

1. 确保 LPCScrypt 工具在你的主机机器上存在。这可以通过安装 :ref:`linkserver-debug-host-tools` 做到。

#. 通过附加 DFU 跳线然后连接到开发板上的 USB 调试端口将 LPC-Link2 微控制器放入 DFU boot 模式。这个跳线连接到 LPC4322 SoC 上的 ``P2_6``。

#. 运行 ``program_JLINK`` 脚本，在安装的 LPCScrypt ``scripts`` 文件夹中找到。

#. 移除 DFU 跳线并电源循环开发板。

.. _lpclink2-daplink-onboard-debug-probe:

LPC-Link2 DAPLink 板载调试探针
=====================================

LPC-Link2 DAPLink 固件是 LPC-Link2 基于开发板上预装的默认固件，但不是推荐的固件。用户应该用上面提供的说明更新到 :ref:`lpclink2-cmsis-onboard-debug-probe` 固件。关于编程 DAPLink 固件的细节，见 `NXP AN13206`_。

.. _opensda-onboard-debug-probe:

OpenSDA 板载调试探针
***************************

OpenSDA 板载调试探针基于 NXP MK20 SoC。它具有拖放编程支持，并支持以下调试固件：

- :ref:`opensda-daplink-onboard-debug-probe`（默认固件）
- :ref:`opensda-jlink-onboard-debug-probe`

.. _opensda-daplink-onboard-debug-probe:

OpenSDA DAPLink 板载调试探针
===================================

这个调试探针固件与以下调试主机工具兼容：

- :ref:`pyocd-debug-host-tools`
- :ref:`openocd-debug-host-tools`
- :ref:`linkserver-debug-host-tools`

这个探针通过用 DAPLink 固件编程 OpenSDA 微控制器实现。NXP 提供 `OpenSDA DAPLink Board-Specific Firmwares`_。

在编程固件前安装调试主机工具。

与所有 OpenSDA 调试探针一样，编程固件的步骤是：

1. 通过在你给开发板供电时按住重置按钮将 OpenSDA 微控制器放入 bootloader 模式。注意在这个上下文中 "bootloader 模式" 适用于 OpenSDA 微控制器本身，而不是你 Zephyr 应用的目标微控制器。

#. 给你开发板供电后，释放重置按钮。一个叫 **BOOTLOADER** 或 **MAINTENANCE** 的 USB 大容量存储设备将枚举。如果枚举的设备名为 **BOOTLOADER**，请先用 `DAPLink Bootloader Update`_ 的说明将 bootloader 更新到最新版本。

#. 将 OpenSDA 固件二进制文件复制到 USB 大容量存储设备。

#. 电源循环开发板，这次不按住重置按钮。你应该看到三个 USB 设备枚举：一个 CDC 设备（串口）、一个 HID 设备（调试端口）和一个大容量存储设备（拖放 flash 编程）。

.. _opensda-jlink-onboard-debug-probe:

OpenSDA J-Link 板载调试探针
==================================

这个调试探针与以下调试主机工具兼容：

- :ref:`jlink-debug-host-tools`

这个探针通过用 J-Link 固件编程 OpenSDA 微控制器实现。Segger 提供 `OpenSDA J-Link Generic Firmwares`_ 和 `OpenSDA J-Link Board-Specific Firmwares`_，后者在可用时通常推荐。开发板特定固件对 i.MX RT 开发板支持其外部 flash 内存是必需的，而通用固件与所有 Kinetis 开发板兼容。

在编程固件前安装调试主机工具。

与所有 OpenSDA 调试探针一样，编程固件的步骤是：

1. 通过在你将 USB 插入开发板的 USB 调试端口时按住重置按钮将 OpenSDA 微控制器放入 bootloader 模式。注意在这个上下文中 "bootloader 模式" 适用于 OpenSDA 微控制器本身，而不是你 Zephyr 应用的目标微控制器。

#. 给你开发板供电后，释放重置按钮。一个叫 **BOOTLOADER** 或 **MAINTENANCE** 的 USB 大容量存储设备将枚举。如果枚举的设备名为 **BOOTLOADER**，请先用 `DAPLink Bootloader Update`_ 的说明将 bootloader 更新到最新版本。

#. 将 OpenSDA 固件二进制文件复制到 USB 大容量存储设备。

#. 电源循环开发板，这次不按住重置按钮。你应该看到两个 USB 设备枚举：一个 CDC 设备（串口）和一个厂商特定设备（调试端口）。

.. _jlink-external-debug-probe:

J-Link 外部调试探针
***************************

`Segger J-Link`_ 是一个外部调试探针家族，包括 J-Link EDU、J-Link PLUS、J-Link ULTRA+ 和 J-Link PRO，支持来自不同硬件架构和厂商的大量设备。

这个调试探针与以下调试主机工具兼容：

- :ref:`jlink-debug-host-tools`
- :ref:`openocd-debug-host-tools`

在编程固件前安装调试主机工具。

.. _stlink-v21-onboard-debug-probe:

ST-LINK/V2-1 板载调试探针
********************************

ST-LINK/V2-1 是内置在所有 Nucleo 和 Discovery 开发板中的串口和调试适配器。它提供你的电脑（或其他 USB 主机）和嵌入式目标处理器之间的桥，可用于调试、flash 编程和串口通信，全部通过一根简单的 USB 线。

它与以下主机调试工具兼容：

- :ref:`openocd-debug-host-tools`
- :ref:`jlink-debug-host-tools`
- :ref:`stm32cubeclt-host-tools`

对于一些 STM32 基于的开发板，它还与以下兼容：

- :ref:`pyocd-debug-host-tools`

虽然它开箱即可与 OpenOCD 配合使用，但需要烧录特定固件才能与 J-Link 配合使用。为此，SEGGER 提供了一个固件，可将 Nucleo 和 Discovery 开发板上的板载 ST-LINK/V2-1 升级为 J-Link。这个固件使 ST-LINK/V2-1 与 J-LinkOB 兼容，允许用户利用大多数 J-Link 功能如超快速 flash 下载和调试速度或免费使用的 GDBServer。

更多关于将 ST-LINK/V2-1 升级到 JLink 或恢复 ST-Link/V2-1 固件的信息请访问：`Segger over ST-Link`_

用 ST-Link 烧录和调试
============================

.. tabs::

    .. tab:: 使用 OpenOCD

        OpenOCD 在 ST-Link 上默认可用并配置为默认烧录和调试工具。烧录和调试可以如下做：

          .. zephyr-app-commands::
             :zephyr-app: samples/hello_world
             :goals: flash

          .. zephyr-app-commands::
             :zephyr-app: samples/hello_world
             :goals: debug

    .. tab:: _`使用 Segger J-Link`

        一旦 ST-Link 烧录了 SEGGER 固件且 J-Link GDB 服务器已在你的主机电脑上安装，你可以如下烧录和调试：

        用 CMake 的 ``-DBOARD_FLASH_RUNNER=jlink`` 将默认 OpenOCD runner 更改为 J-Link。或者，你可以在应用 ``CMakeList.txt`` 文件中添加以下行。

          .. code-block:: cmake

             set(BOARD_FLASH_RUNNER jlink)

        如果你用 West（Zephyr 的 meta 工具），你可以用 ``--runner``（或 ``-r``）选项修改默认 runner。

          .. code-block:: console

             west flash --runner jlink

        要附加调试器到你的开发板并用 ``jlink`` 打开调试控制台，运行：

          .. code-block:: console

             west debug --runner jlink

        更多关于 West 和可用选项的信息，见 :ref:`west`。

        如果你将 Zephyr 应用配置为使用 `Segger RTT`_ 控制台，打开 telnet：

          .. code-block:: console

             $ telnet localhost 19021
             Trying ::1...
             Trying 127.0.0.1...
             Connected to localhost.
             Escape character is '^]'.
             SEGGER J-Link V6.30f - Real time terminal output
             J-Link STLink V21 compiled Jun 26 2017 10:35:16 V1.0, SN=773895351
             Process: JLinkGDBServerCLExe
             Zephyr Shell, Zephyr version: 1.12.99
             Type 'help' for a list of available commands
             shell>

        如果你得不到 RTT 输出你可能需要禁用其他与 RTT 控制台冲突的控制台如果它们在特定示例或应用中被默认启用，例如用 menuconfig 禁用 UART_CONSOLE

.. _stlink-adapter-firmware-update:

更新或恢复 ST-Link 固件
======================================

ST-Link 固件可以用 `STM32CubeProgrammer Tool`_ 更新。通常在遇到烧录问题时有用，例如使用 twister 的 device-testing 选项时。

安装后，你可以用以下命令更新已连接开发板的 ST-Link 固件：

  .. code-block:: console

     s java -jar ~/STMicroelectronics/STM32Cube/STM32CubeProgrammer/Drivers/FirmwareUpgrade/STLinkUpgrade.jar -sn <board_uid>

其中 board_uid 可以用 twister 的 generate-hardware-map 选项获取。更多关于 twister 和可用选项的信息，见 :ref:`twister_script`。

OpenOCD 弃用 HLA ST-Link 接口
========================================

OpenOCD 在 2024 年 1 月弃用了 ST-Link 固件使用的遗留 HLA 接口，转而采用通用 DAP 接口（见 `OpenOCD deprecates ST-Link HLA Interface`_）。DAP 接口自 2015 年起（从版本 v2j24）被 ST-Link 固件支持。

由于 OpenOCD 弃用，使用较新版本的 OpenOCD 工具（release tag v0.12.0 之后）的用户，在 ST-Link 适配器搭载 v2j24 之前版本固件时，可能遇到通信问题。在这种情况下，推荐更新 ST-Link 固件（参见 `ST-LINK firmware update <#_stlink-adapter-firmware-update>`_）。如果不可能更新固件，你仍然可以通过修改其 OpenOCD 配置脚本替换（如果适用）以下 2 行来使用旧的 HLA 接口：

  .. code-block::

    source [find interface/stlink-dap.cfg]
    transport select dapdirect_swd

用以下 2 行：

  .. code-block::

    source [find interface/stlink-hla.cfg]
    transport select hla_swd

.. _nxp-s32-debug-probe:

NXP S32 调试探针
*******************

`NXP S32 Debug Probe`_ 通过标准调试端口启用 NXP S32 目标系统调试，可通过 USB 连接到开发者工作站，或通过以太网远程连接。

NXP S32 调试探针设计用于与 NXP S32 Design Studio（S32DS）和 NXP 汽车微控制器和处理器配合工作。在编程固件前按 :ref:`nxp-s32-debug-host-tools` 中指示的调试主机工具安装。

.. _black-magic-probe:

Black Magic Probe
*****************

Black Magic Probe 是用于调试的开源硬件，设计用于与 `Black Magic Debug`_ 固件一起使用。固件整合 GDB Server 使你可以从 ``gdb`` 直接连接到目标设备。

一些基于 STM32F103 的开发板可以运行 `Black Magic Debug`_ 固件。见 `Black Magic Debug supported hardware`_。

.. _LPCScrypt:
   https://www.nxp.com/lpcscrypt

.. _Firmware for LPCXpresso:
   https://www.segger.com/products/debug-probes/j-link/models/other-j-links/lpcxpresso-on-board/

.. _OpenSDA DAPLink Board-Specific Firmwares:
   https://www.nxp.com/opensda

.. _OpenSDA J-Link Generic Firmwares:
   https://www.segger.com/downloads/jlink/#JLinkOpenSDAGenericFirmwares

.. _OpenSDA J-Link Board-Specific Firmwares:
   https://www.segger.com/downloads/jlink/#JLinkOpenSDABoardSpecificFirmwares

.. _Segger J-Link:
   https://www.segger.com/products/debug-probes/j-link/

.. _Segger over ST-Link:
   https://www.segger.com/products/debug-probes/j-link/models/other-j-links/st-link-on-board/

.. _Segger RTT:
    https://www.segger.com/jlink-rtt.html

.. _STM32CubeProgrammer Tool:
    https://www.st.com/en/development-tools/stm32cubeprog.html

.. _OpenOCD deprecates ST-Link HLA Interface:
    https://sourceforge.net/p/openocd/code/ci/34ec5536c0ba3315bc5a841244bbf70141ccfbb4

.. _MCUXpresso Installer:
	https://www.nxp.com/lgfiles/updates/mcuxpresso/MCUXpressoInstaller.exe

.. _NXP S32 Debug Probe:
   https://www.nxp.com/design/software/automotive-software-and-tools/s32-debug-probe:S32-DP

.. _NXP AN13206:
   https://www.nxp.com/docs/en/application-note/AN13206.pdf

.. _DAPLink Bootloader Update:
   https://os.mbed.com/blog/entry/DAPLink-bootloader-update/

.. _Black Magic Debug:
   https://black-magic.org/index.html

.. _Black Magic Debug supported hardware:
   https://black-magic.org/index.html#other-hardware-supported-by-black-magic-debug
