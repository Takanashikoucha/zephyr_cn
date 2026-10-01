.. _flash-debug-host-tools:

烧录与调试主机工具
########################

本指南描述你可以在主机工作站上运行的软件工具来烧录和调试 Zephyr 应用。

Zephyr 的 west 工具在其 ``flash``、``debug``、``debugserver`` 和 ``attach`` 命令中内置了对所有这些的支持，前提是你的开发板硬件支持它们且你的 Zephyr 开发板目录的 :file:`board.cmake` 文件正确声明了这种支持。更多细节见 :ref:`west-build-flash-debug`。

.. _runner_blackmagicprobe:

Black Magic Probe
*****************

Black Magic Probe（BMP）是一个开源调试硬件，将 GDB 调试服务器功能集成到固件中。不需要 GDB 服务器程序，因此没有与主机工具等价的程序。

更多细节，包括使用说明和支持目标，见 :ref:`black-magic-probe`。

.. _atmel_sam_ba_bootloader:
.. _runner_bossac:

SAM Boot Assistant（SAM-BA）
***************************

Atmel SAM Boot Assistant（Atmel SAM-BA）允许从 USB 或 UART 主机进行系统内编程（ISP），不需要任何外部编程接口。Zephyr 允许用户用 :ref:`west <west-flashing>` 开发和支持 SAM-BA 的开发板并编程。Zephyr 支持带/不带 ROM bootloader 的设备以及来自 Arduino 和 Adafruit 的两种扩展。完整支持在 Zephyr SDK 0.12.0 中引入。

烧录开发板的典型命令是：

.. code-block:: console

	west flash [ -r bossac ] [ -p /dev/ttyX ] [ --erase ]

.. note::

    默认情况下，用 bossac 烧录只擦除包含烧录应用的 flash 页，其他页保持不变。如果你想烧录时擦除目标的整个 flash，烧录时传递 ``--erase`` 参数。

设备的 flash 配置：

.. tabs::

    .. tab:: 带 ROM bootloader

        这些设备不需要任何特殊配置。构建你的应用后，只运行 ``west flash`` 烧录开发板。

    .. tab:: 不带 ROM bootloader

        对于这些设备，用户应该：

        1. 定义容纳 bootloader 和应用镜像所需的 flash 分区；细节见 :ref:`flash_map_api`。
        2. 有开发板 :file:`.defconfig` 文件将 :kconfig:option:`CONFIG_USE_DT_CODE_PARTITION` Kconfig 选项设置为 ``y`` 以指示构建系统用这些分区做代码重定位。这个选项也可以在 ``prj.conf`` 或任何其他 Kconfig 片段中设置。
        3. 构建并烧录设备上的 SAM-BA bootloader。

    .. tab:: 带兼容 SAM-BA bootloader

        对于这些设备，用户应该：

        1. 定义容纳 bootloader 和应用镜像所需的 flash 分区；细节见 :ref:`flash_map_api`。
        2. 有开发板 :file:`.defconfig` 文件将 :kconfig:option:`CONFIG_BOOTLOADER_BOSSA` Kconfig 选项设置为 ``y``。这将自动选择 :kconfig:option:`CONFIG_USE_DT_CODE_PARTITION` Kconfig 选项它指示构建系统用这些分区做代码重定位。开发板 :file:`.defconfig` 文件应该将 :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_ARDUINO`、:kconfig:option:`CONFIG_BOOTLOADER_BOSSA_ADAFRUIT_UF2` 或 :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_LEGACY` Kconfig 选项设置为 ``y`` 来选择正确的兼容 SAM-BA bootloader 模式。这些选项也可以在 ``prj.conf`` 或任何其他 Kconfig 片段中设置。
        3. 构建并烧录设备上的 SAM-BA bootloader。

.. note::

    :kconfig:option:`CONFIG_BOOTLOADER_BOSSA_LEGACY` Kconfig 选项应该作为最后手段使用。先尝试用不带 ROM bootloader 的设备配置。


典型 flash 布局和配置
--------------------------------------

对于位于 flash 上的 bootloader，设备树分区布局是强制的。对于有 ROM bootloader 的设备，当应用使用存储或其他非应用分区时是强制的。在这个特殊情况下，应该省略 boot 分区且 code_partition 应该从偏移 0 开始。必须总是定义大小避免重叠的分区。

不带 ROM bootloader 的设备的典型 flash 布局是：

.. code-block:: devicetree

	/ {
		chosen {
			zephyr,code-partition = &code_partition;
		};
	};

	&flash0 {
		partitions {
			compatible = "fixed-partitions";
			#address-cells = <1>;
			#size-cells = <1>;

			boot_partition: partition@0 {
				label = "sam-ba";
				reg = <0x00000000 0x2000>;
				read-only;
			};

			code_partition: partition@2000 {
				label = "code";
				reg = <0x2000 0x3a000>;
				read-only;
			};

			/*
			* 最后 16 KiB 为应用保留。
			* 存储分区如果启用将被 FCB/LittleFS/NVS 使用。
			*/
			storage_partition: partition@3c000 {
				label = "storage";
				reg = <0x0003c000 0x00004000>;
			};
		};
	};

带 ROM bootloader 和存储分区的设备的典型 flash 布局是：

.. code-block:: devicetree

	/ {
		chosen {
			zephyr,code-partition = &code_partition;
		};
	};

	&flash0 {
		partitions {
			compatible = "fixed-partitions";
			#address-cells = <1>;
			#size-cells = <1>;

			code_partition: partition@0 {
				label = "code";
				reg = <0x0 0xF0000>;
				read-only;
			};

			/*
			* 最后 64 KiB 为应用保留。
			* 存储分区如果启用将被 FCB/LittleFS/NVS 使用。
			*/
			storage_partition: partition@F0000 {
				label = "storage";
				reg = <0x000F0000 0x00100000>;
			};
		};
	};


启用 SAM-BA runner
----------------------

要指示 Zephyr west 工具使用 SAM-BA bootloader，:file:`board.cmake` 文件必须有 ``include(${ZEPHYR_BASE}/boards/common/bossac.board.cmake)`` 条目。注意 Zephyr 工具接受更多条目来定义多个 runner。默认情况下，第一个将在使用 ``west flash`` 命令时被选择。剩余的选项通过传递 runner 选项可用，例如 ``west flash -r bossac``。


更多实现细节可以在 :ref:`boards` 文档中找到。作为快速参考，见这些开发板文档页面：

  - :zephyr:board:`sam4e_xpro`（ROM bootloader）
  - :zephyr:board:`adafruit_feather_m0_basic_proto`（Adafruit UF2 bootloader）
  - :zephyr:board:`arduino_nano_33_iot`（Arduino bootloader）
  - :zephyr:board:`arduino_nano_33_ble`（Arduino legacy bootloader）

在 Windows Native 启用 BOSSAC [实验性]
------------------------------------------------

Zephyr SDK 的 bossac 当前只支持 Linux 和 macOS。Windows 支持可以通过使用 `BOSSA 官方发布`_ 的 bossac 版本实现。用默认选项安装后，:file:`bossac.exe` 必须被添加到 Windows PATH。可以通过传递 ``--bossac`` 选项使用特定的 bossac 可执行文件，如下：

.. code-block:: console

    west flash -r bossac --bossac="C:\Program Files (x86)\BOSSA\bossac.exe" --bossac-port="COMx"

.. note::

   WSL 当前不受支持。


.. _linkserver-debug-host-tools:
.. _runner_linkserver:

LinkServer 调试主机工具
****************************

Linkserver 是一个用于启动和管理 NXP 调试探针的 GDB 服务器的工具，还提供命令行目标 flash 编程能力。Linkserver 可以与 `NXP MCUXpresso for Visual Studio Code`_ 实现一起使用，与基于 GNU 工具的自定义调试配置一起使用，或作为持续集成和测试的无头解决方案的部分。LinkServer 可以与 NXP 的 MCU-Link、LPC-Link2、基于 LPC11U35 和基于 OpenSDA 的独立或板载调试探针一起使用。

NXP 推荐用 NXP 的 `MCUXpresso Installer`_ 安装 LinkServer。这个方法也将安装支持以下调试探针的工具，包括 NXP 的 MCU-Link 和 LPCScrypt 工具。

LinkServer 与以下调试探针兼容：

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`mcu-link-cmsis-onboard-debug-probe`
- :ref:`opensda-daplink-onboard-debug-probe`

要用 West 命令使用 LinkServer，安装文件夹应该被添加到 :envvar:`PATH` :ref:`环境变量 <env_vars>`。要添加的默认安装路径是：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

         /usr/local/LinkServer

   .. group-tab:: macOS

      .. code-block:: console

         /Applications/LinkServer_<version>

   .. group-tab:: Windows

      .. code-block:: console

         c:\nxp\LinkServer_<version>

受支持的 west 命令：

1. flash
#. debug
#. debugserver
#. attach

注意：


1. 探针可以用 LinkServer 列出：

.. code-block:: console

   LinkServer probes

2. 当多个调试探针连接到主机时，用 LinkServer west runner 的 ``--probe`` 选项传递探针索引。

.. code-block:: console

   west flash --runner=linkserver --probe=3

3. 设备特定设置可以用 LinkServer 的 west runner 的 '--override' 选项覆盖。可以多次使用。格式由 LinkServer 规定，例如：

.. code-block:: console

   west flash --runner=linkserver --override /device/memory/5/flash-driver=MIMXRT500_SFDP_MXIC_OSPI_S.cfx

4. LinkServer 不在 reset handler 安装隐式断点。如果你想从应用开始单步，你需要手动在 ``main`` 或 reset handler 添加断点。

5. 那个断点，和任何其他 GDB 命令，可以用 ``--gdb-init`` 自动安装，这个 runner 将它附加到 ``west debug`` 和 ``west attach`` 的 GDB 客户端，例如：

   .. code-block:: console

      west debug --runner=linkserver --gdb-init 'b main'

   见 :ref:`gdb-init-runner-option`。

.. _jlink-debug-host-tools:
.. _runner_jlink:

J-Link 调试主机工具
***********************

Segger 为 Linux、macOS 和 Windows 操作系统提供一套调试主机工具：

- J-Link GDB Server: GDB 远程调试
- J-Link Commander: 命令行控制和 flash 编程
- RTT Viewer: RTT 终端输入和输出
- SystemView: 实时事件可视化和记录

这些调试主机工具与以下调试探针兼容：

- :ref:`lpclink2-jlink-onboard-debug-probe`
- :ref:`opensda-jlink-onboard-debug-probe`
- :ref:`mcu-link-jlink-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查你的 SoC 是否列在 `J-Link Supported Devices`_ 中。

下载并安装 `J-Link Software and Documentation Pack`_ 获取 J-Link GDB Server 和 Commander，并安装关联的 USB 设备驱动。RTT Viewer 和 SystemView 可以分开下载，但不是必须的。

注意 J-Link GDB 服务器尚不支持 Zephyr RTOS 感知。

.. _gdb-init-runner-option:

传递额外 GDB 命令
--------------------------

``jlink`` runner 接受 ``--gdb-init``，它向 ``west debug`` 和 ``west attach`` 启动的 GDB 客户端附加一个命令。选项可以多次给出且命令按给定顺序运行，最后的在 runner 发送给 GDB 的所有东西之后且在目标恢复前。由于它们只是附加的，它们不能更改 runner 自己的 connect、load 和 reset 序列。``west flash``、``west reset``、``west rtt`` 和 ``west debugserver`` 不受影响。

例如，要为一个调试会话的持续时间启用 J-Link semihosting：

.. code-block:: console

   west debug -r jlink --gdb-init 'monitor semihosting enable' \
     --gdb-init 'monitor semihosting basedir .'

相同的命令可以通过添加到开发板的 :file:`board.cmake` 成为开发板的默认：

.. code-block:: cmake

   board_runner_args(jlink "--gdb-init=monitor semihosting enable")

注意 ``--gdb-init`` 只到达 GDB 客户端。J-Link GDB server 本身的选项用 ``--tool-opt`` 传递，烧录时运行的 J-Link Commander 命令用 ``--pre-script-cmd`` 传递。

``linkserver``、``openocd`` 和 ``intel_cyclonev`` runner 接受相同的选项。它适用于哪些命令，以及命令在哪里插入，取决于每个 runner。

.. _openocd-debug-host-tools:
.. _runner_openocd:

OpenOCD 调试主机工具
************************

OpenOCD 是一个社区开源项目，为广泛的 SoC 提供 GDB 远程调试和 flash 编程支持。Zephyr SDK 包括一个添加 Zephyr RTOS-awareness 的 fork；否则见 `Getting OpenOCD`_ 获取从官方仓库下载 OpenOCD 的选项。

这些调试主机工具与以下调试探针兼容：

- :ref:`opensda-daplink-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查你的 SoC 是否列在 `OpenOCD Supported Devices`_ 中。

.. note:: 在 Linux 上，openocd 通过 `Zephyr SDK
   <https://github.com/zephyrproject-rtos/sdk-ng/releases>`_ 可用。
   Windows 用户应该用以下步骤安装 openocd：

   - 从这里下载 Windows 的 openocd: `OpenOCD Windows`_
   - 复制 bin 和 share 目录到 ``C:\Program Files\OpenOCD\``
   - 将 ``C:\Program Files\OpenOCD\bin`` 添加到 'PATH' 环境变量

.. _pyocd-debug-host-tools:
.. _runner_pyocd:

pyOCD 调试主机工具
**********************

pyOCD 是来自 Arm 的开源项目，为 Arm Cortex-M SoC 提供 GDB 远程调试和 flash 编程支持。它在 PyPi 上分发并在你完成入门指南中的 :ref:`gs_python_deps` 步骤时安装。pyOCD 包括对 Zephyr RTOS 感知的支持。

这些调试主机工具与以下调试探针兼容：

- :ref:`lpclink2-cmsis-onboard-debug-probe`
- :ref:`mcu-link-cmsis-onboard-debug-probe`
- :ref:`opensda-daplink-onboard-debug-probe`
- :ref:`stlink-v21-onboard-debug-probe`

检查你的 SoC 是否列在 `pyOCD Supported Devices`_ 中。

.. _lauterbach-trace32-debug-host-tools:
.. _runner_trace32:

Lauterbach TRACE32 调试主机工具
***********************************

`Lauterbach TRACE32`_ 是一条微处理器开发工具、调试器和实时追踪器产品线，支持 JTAG、SWD、NEXUS 或多核心架构上的 ETM，包括 Arm Cortex-A/-R/-M、RISC-V、Xtensa 等。Zephyr 允许用户用 :ref:`west <west-flashing>` 开发和支持 Lauterbach TRACE32 的开发板并编程。

runner 由 TRACE32 软件的一个包装器组成，允许 Zephyr 开发板为受支持的不同命令执行自定义启动脚本（Practice Script），包括从 CMake 传递额外参数的能力。由使用这个 runner 的开发板决定定义每个命令执行的操作。

安装 Lauterbach TRACE32 软件
-----------------------------------

从 `Lauterbach TRACE32 download website`_ 下载 Lauterbach TRACE32 软件（需要注册）并遵循 `Lauterbach TRACE32 Installation Guide`_ 中描述的安装步骤。

烧录和调试
----------------------

将 :ref:`环境变量 <env_vars>` :envvar:`T32_DIR` 设置为 TRACE32 系统目录。然后执行 ``west flash`` 或 ``west debug`` 命令来烧录或调试 Zephyr 应用，如 :ref:`west-build-flash-debug` 中详细描述的那样。``debug`` 命令启动 TRACE32 GUI 允许调试 Zephyr 应用，而 ``flash`` 命令隐藏 GUI 并在后台执行所有操作。

默认情况下，``t32`` runner 将用位于 TRACE32 系统目录中名为 ``config.t32`` 的默认配置文件启动 TRACE32。要使用不同的配置文件，向 runner 提供参数 ``--config CONFIG``，例如：

.. code-block:: console

	west flash --config myconfig.t32

更多选项，运行 ``west flash --context -r t32`` 打印用法。

Zephyr RTOS 感知
---------------------

要启用 Zephyr RTOS 感知，遵循 `Lauterbach TRACE32 Zephyr OS Awareness Manual`_ 中描述的步骤。

.. _nxp-s32-debug-host-tools:
.. _runner_nxp_s32dbg:

NXP S32 调试探针主机工具
******************************

:ref:`nxp-s32-debug-probe` 设计用于与 `NXP S32 Design Studio for S32 Platform`_ 配合工作。

下载（需要注册）NXP S32 Design Studio for S32 Platform 并遵循 `S32 Design Studio for S32 Platform Installation User Guide`_ 获取需要的调试主机工具和关联的 USB 设备驱动。

注意 NXP S32 GDB 服务器的 Zephyr RTOS 感知支持取决于目标设备。咨询产品发布说明获取更多信息。

受支持的 west 命令：

1. debug
#. debugserver
#. attach

基本使用
-----------

开始前，将 NXP S32 Design Studio 安装目录添加到系统 :ref:`PATH 环境变量 <env_vars>`。或者，它可以在每次调用时通过 ``--s32ds-path`` 传递给 runner 如下所示：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

         west debug --s32ds-path=/opt/NXP/S32DS.3.6

   .. group-tab:: Windows

      .. code-block:: console

         west debug --s32ds-path=C:\NXP\S32DS.3.6

如果多个 S32 调试探针通过 USB 连接到主机，runner 将要求用户在继续前通过命令行提示选择一个。探针的连接字符串也可以在调用 runner 时通过 ``--dev-id=<connection-string>`` 指定。咨询 NXP S32 调试探针用户手册获取如何构造连接字符串的细节。例如，如果使用序列 ID ``00:04:9f:00:ca:fe`` 的探针：

.. code-block:: console

   west debug --dev-id='s32dbg:00:04:9f:00:ca:fe'

可以通过 ``--tool-opt`` 向调试主机工具传递额外选项。执行 ``debug`` 或 ``attach`` 命令时，工具选项只传递给 GDB 客户端。执行 ``debugserver`` 时，工具选项传递给 GDB 服务器。例如，要将 Zephyr 应用加载到 SRAM 并之后分离调试会话：

.. code-block:: console

   west debug --tool-opt='--batch'

要求
--------------

- **S32 Design Studio 版本**：3.6.0 或更新。
- **S32DebugProbe OS（固件）**：1.1.0 或更新。

S32 Debug Probe OS 升级程序
------------------------------------

参考 `S32 Debug Probe User Guide`_ 中的 "Reprogramming S32 Debug Probe Firmware Images" 章节升级 S32DebugProbe 的 OS。

.. _runner_probe_rs:

probe-rs 调试主机工具
*************************

probe-rs 是一个用 Rust 编写的开源嵌入式工具包。它为各种调试探针提供开箱即用的支持，包括 CMSIS-DAP、ST-Link、SEGGER J-Link、FTDI 和 ESP32 设备上的内置 USB-JTAG 接口。

更多设置细节检查 `probe-rs Installation`_。

检查你的 SoC 是否列在 `probe-rs Supported Devices`_ 中。

.. _runner_rfp:

Renesas Flash Programmer（RFP）主机工具
*****************************************

Renesas 提供 `Renesas Flash Programmer`_ 作为 Renesas 开发板的官方编程工具，使用 Renesas 标准 boot 固件。它以 GUI 和 CLI 形式可用。

对于配置了 ``rfp`` west runner 的开发板，RFP CLI 可以轻松使用来烧录 Zephyr。

受支持的 west 命令：

1. flash

下载后，如果 ``rfp-cli`` 没有放在你系统 PATH 的某处，你可以在烧录时向 ``rfp-cli`` 传递位置：

.. code-block:: console

   west flash --rfp-cli ~/Downloads/RFP_CLI_Linux_V31800_x64/linux-x64/rfp-cli

.. _stm32cubeclt-host-tools:
.. _runner_stlink_gdbserver:

STM32CubeCLT 烧录与调试主机工具
*************************************

STMicroelectronics 提供 `STM32CubeCLT`_ 作为兼容 Linux®、macOS® 和 Windows® 的官方一体工具集，允许在第三方开发环境中使用 STMicroelectronics 专有工具。

它特别提供一个 GDB 调试服务器（*ST-LINK GDB Server*），可以用板载或外部 ST-LINK 调试探针调试 STM32 开发板上的应用。

它与以下调试探针兼容：

- :ref:`stlink-v21-onboard-debug-probe`
- 独立 `ST-LINK-V2`_、`ST-LINK-V3`_ 和 `STLINK-V3PWR`_ 探针

安装 STM32CubeCLT
--------------------

获取 ST-LINK GDB Server 的最简单方式是从 STMicroelectronics 网站安装 `STM32CubeCLT`_。需要一个有效的邮件地址来接收下载链接。

基本使用
-----------

ST-Link GDB Server 可以通过 ``west attach``、``west debug`` 或 ``west debugserver`` 命令使用来调试 Zephyr 应用。

.. code-block:: console

   west debug --runner stlink_gdbserver

.. note::

   `STM32CubeCLT`_ 安装中包含的 `STM32CubeProgrammer`_ 版本也可以用来烧录应用。要做这，应该用专用的 :ref:`STM32CubeProgrammer runner <runner_stm32cubeprogrammer>` 替代 ``stlink_gdbserver``，如下示例中做的：

   .. code-block:: console

      west flash --runner stm32cubeprogrammer

.. _stm32cubeprog-flash-host-tools:
.. _runner_stm32cubeprogrammer:

STM32CubeProgrammer 烧录主机工具
************************************

STMicroelectronics 提供 `STM32CubeProgrammer`_（STM32CubeProg）作为 STM32 开发板在 Linux®、macOS® 和 Windows® 操作系统上的官方编程工具。

它提供一个易用和高效的环境用于通过调试接口（JTAG 和 SWD）和 bootloader 接口（UART 和 USB DFU、I2C、SPI 和 CAN）读取、写入和验证设备内存。

它提供广泛的功能用于编程 STM32 内部内存（如 flash、RAM 和 OTP）以及外部内存。

它还允许选项编程和上传、编程内容验证、以及通过脚本的编程自动化。

它以 GUI（图形用户接口）和 CLI（命令行接口）版本提供。

它与以下调试探针兼容：

- :ref:`stlink-v21-onboard-debug-probe`
- :ref:`jlink-external-debug-probe`
- 独立 `ST-LINK-V2`_、`ST-LINK-V3`_ 和 `STLINK-V3PWR`_ 探针

安装 STM32CubeProgrammer
---------------------------

获取 `STM32CubeProgrammer`_ 的最简单方式是从 STMicroelectronics 网站下载。需要一个有效的邮件地址来接收下载链接。

或者，它可以作为 `STM32CubeCLT`_ 一体多 OS 命令行工具集的部分安装，该工具集还包括 GDB 调试器客户端和服务器。

如果你系统上有 STM32CubeIDE 安装，那么 STM32CubeProg 已经存在。

基本使用
-----------

`STM32CubeProgrammer`_ 设置为 Zephyr 支持的所有活跃 STM32 开发板的默认 west runner。它可以通过 ``west flash`` 命令使用来烧录 Zephyr 应用。

.. code-block:: console

   west flash --runner stm32cubeprogrammer

高级使用通过 GUI 或 CLI，检查 `STM32CubeProgrammer User Manual`_。

.. _runner_xsdb:

XSDB 烧录与调试主机工具
*****************************

AMD XSDB 工具（Xilinx Software Command-line Tool for Debug）是用于编程和调试许多 AMD adaptive SoC 和 FPGA 平台的命令行工具。它 **不** 包括在 Zephyr SDK 中：安装 `AMD Vitis`_（或你平台的等价 AMD 工具链分发）并确保 ``xsdb`` 可执行文件在你系统 :ref:`PATH <env_vars>` 上。

选择 ``xsdb`` west runner 的开发板通常在开发板定义旁边附带开发板特定的 ``support/xsdb.cfg``。见你开发板的文档获取需要的 boot 制品（PDI、bitstream、FSBL 等）。

受支持的 west 命令包括 ``flash``、``debug`` 和 ``debugserver``。

对于这个 runner，``west debug`` 和 ``west debugserver`` 都启动相同的本地 XSDB 交互会话。与基于 GDB 的 runner 不同（那里 ``debugserver`` 为 IDE 启动一个远程 stub），xsdb runner 总是直接启动 XSDB，通过开发板 ``xsdb.cfg`` 加载应用，并停留在 XSDB 提示符处。

.. code-block:: console

   west flash --runner xsdb

   west debug --runner xsdb

   west debugserver --runner xsdb

.. note::

   这与本章其他专有主机工具（例如 :ref:`J-Link <jlink-debug-host-tools>` 或 :ref:`STM32CubeCLT <stm32cubeclt-host-tools>`）是相同类的依赖：Zephyr 通过 west runner 与工具集成；获取和许可工具链是用户的责任。

.. _runner_uf2:

UF2 上传器
************

uf2 runner 支持用 UF2（USB Flashing Format）烧录某些开发板。UF2（USB 烧录格式）是一个用户友好的文件格式，设计用于通过 USB 大容量存储设备拖放编程。

它依赖目标设备进入一个特殊的 bootloader 模式，在该模式下它向主机呈现为 USB 大容量存储设备。进入这个模式后，应用镜像可以通过将 ``.uf2`` 文件复制到挂载的卷上传。

.. code-block:: console

   west flash --runner uf2

如果 UF2 卷不自动检测，你可能需要用 ``--device`` 选项手动指定挂载点：

关于 UF2 格式及其工具的更多信息，见 `USB Flashing Format（UF2）`_。

.. _runner_rtkprog:

Realtek 备用 Flash 编程器（rtkprog）
********************************************

``rtkprog`` 是用 UART 烧录 Realtek Bee 家族 SoC 所需协议的开源实现。

.. code-block:: console

   west flash --runner rtkprog

.. _rtkprog 源代码:
   https://github.com/a-labs-io/rtkprog
.. _rtkprog Python 包:
   https://pypi.org/p/rtkprog


.. _runner_mpcli:

Realtek Bee Flash 编程器（MPCli）主机工具
***********************************************

Realtek 提供 `Realtek Flash Programmer（MPCli）`_ 作为 Bee 系列的官方编程工具，支持 Linux、macOS 和 Windows 操作系统。MPCli 通过 UART 接口启用系统内编程（ISP），消除对外部编程硬件的需要。在大多数官方 Bee 系列评估开发板上，包括内置的 UART 到 USB 转换器用于开箱即用的编程和日志。

下载 MPCli 的归档后，解压它并选择与你操作系统兼容的版本。然后，将包含 ``mpcli`` 可执行文件的目录添加到你系统 :ref:`PATH 环境变量 <env_vars>`。

开始前，确保你的开发板处于下载模式。请参考开发板文档在：`Realtek Supported Boards`_

.. code-block:: console

   west flash [--runner mpcli] --port /dev/ttyX


.. _iar-debug-host-tools:
.. _runner_iar:

IAR EW 与 C-Spy 主机工具
*************************

IAR 提供 Embedded Workbench 和 CSpyBat 用于调试和烧录。iar runner 适用于 EWARM 10.10 或更新版本。

.. _AMD Vitis:
   https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vitis.html

.. _J-Link Software and Documentation Pack:
   https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack

.. _J-Link Supported Devices:
   https://www.segger.com/downloads/supported-devices.php

.. _Getting OpenOCD:
   https://openocd.org/pages/getting-openocd.html

.. _OpenOCD Supported Devices:
   https://github.com/zephyrproject-rtos/openocd/tree/latest/tcl/target

.. _pyOCD Supported Devices:
   https://github.com/pyocd/pyOCD/tree/main/pyocd/target/builtin

.. _OpenOCD Windows:
   https://gnutoolchains.com/arm-eabi/openocd/

.. _Lauterbach TRACE32:
   https://www.lauterbach.com/

.. _Lauterbach TRACE32 download website:
   https://www.lauterbach.com/download_trace32.html

.. _Lauterbach TRACE32 Installation Guide:
   https://www2.lauterbach.com/pdf/installation.pdf

.. _Lauterbach TRACE32 Zephyr OS Awareness Manual:
   https://www2.lauterbach.com/pdf/rtos_zephyr.pdf

.. _BOSSA 官方发布:
   https://github.com/shumatech/BOSSA/releases

.. _NXP MCUXpresso for Visual Studio Code:
   https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-for-visual-studio-code:MCUXPRESSO-VSC

.. _MCUXpresso Installer:
   https://mcuxpresso.nxp.com/mcux-vscode/latest/html/MCUXpresso-Installer.html

.. _NXP S32 Design Studio for S32 Platform:
   https://www.nxp.com/design/software/development-software/s32-design-studio-ide/s32-design-studio-for-s32-platform:S32DS-S32PLATFORM

.. _Renesas Flash Programmer:
   https://www.renesas.com/en/software-tool/renesas-flash-programmer-programming-gui

.. _S32 Design Studio for S32 Platform Installation User Guide:
   https://www.nxp.com/webapp/Download?colCode=S32DSIG

.. _S32 Debug Probe User Guide:
   https://www.nxp.com/docs/en/user-guide/S32DBGUG.pdf

.. _probe-rs Installation:
   https://probe.rs/docs/getting-started/installation/

.. _probe-rs Supported Devices:
   https://probe.rs/targets/

.. _STM32CubeCLT:
   https://www.st.com/en/development-tools/stm32cubeclt.html

.. _STM32CubeProgrammer:
   https://www.st.com/en/development-tools/stm32cubeprog.html

.. _STM32CubeProgrammer User Manual:
   https://www.st.com/resource/en/user_manual/um2237-stm32cubeprogrammer-software-description-stmicroelectronics.pdf

.. _ST-LINK-V2:
   https://www.st.com/en/development-tools/st-link-v2.html

.. _ST-LINK-V3:
   https://www.st.com/en/development-tools/stlink-v3set.html

.. _STLINK-V3PWR:
   https://www.st.com/en/development-tools/stlink-v3pwr.html

.. _USB Flashing Format（UF2）:
   https://github.com/microsoft/uf2

.. _Realtek Flash Programmer（MPCli）:
   https://docs.realmcu.com/tools/mpcli_tool/en/latest/mpcli/text_en/README.html

.. _Realtek Supported Boards:
   https://docs.zephyrproject.org/latest/boards/realtek/index.html
