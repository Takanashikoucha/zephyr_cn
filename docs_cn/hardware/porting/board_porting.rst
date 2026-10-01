.. _board_porting_guide:

Board 移植指南
###################

要为新的 :term:`board` 添加 Zephyr 支持，你至少需要一个带各种文件的 *board 目录*。
Board 目录中的文件继承对至少一个 SoC 及其所有功能的支持。
因此，Zephyr 还必须支持你的 :term:`SoC`。

.. _hw_model_v2:

过渡到当前硬件模型
****************************************

在 Zephyr 3.6.0 发布后不久，向 Zephyr 引入了新硬件模型。
此新模型彻底改变了 SoCs 和 boards 的命名和定义方式，
并添加了对多年来被识别为重要的功能的支持。
其中包括：

- 支持多核、多架构 AMP（非对称多处理）SoCs
- 支持多 SoC boards
- 支持在 Zephyr 构建系统之外复用 SoC 和 board Kconfig 树
- 支持用 :ref:`sysbuild` 的高级用例
- 移除所有现有任意和不一致的 Kconfig 和文件夹名称使用

此页面上的所有文档都指当前硬件模型。
请参见 Zephyr v3.6.0（或更早）中的文档以获取先前（现已过时）硬件模型的信息。

有关新模型背后理由、开发和概念的更多信息可在 :github:`original issue <51831>`、
:github:`original Pull Request <50305>` 中找到，
对于引入的完整变更集，参见 `hardware model v2 commit`_。

新硬件模型的某些非关键特性、增强和改进仍在开发中。
参见 :github:`hardware model v2 enhancements issue <69546>` 获取完整列表。

从先前硬件模型过渡到当前模型（通常称为 "hardware model v2"）
需要对所有现有 board 和 SoC 定义进行修改。
已决定不为先前模型提供直接向后兼容性，
这使得从先前 Zephyr 版本过渡到包含新模型（v3.7.0 及以后）的用户
如果他们有 out-of-tree board（或 SoC）有两个选项：

#. 将 out-of-tree board 转换到当前硬件模型（推荐）
#. 从 Zephyr v3.6.0 获取 SoC 定义并复制到你的下游仓库
   （确保构建系统可通过 :ref:`zephyr module <modules>` 或 ``SOC_ROOT`` 找到它）。
   这将允许你的 board（在先前硬件模型中定义）继续工作

在将你的 board 从先前硬件模型转换到当前硬件模型时，
我们建议先通读此页以详细了解模型。
然后可以用 `example-application conversion Pull Request`_ 作为移植简单 board 的示例。
此外，提供了 `conversion script`_ 且在许多情况下可靠工作
（尽管多核 SoCs 可能未完全处理）。
最后，`hardware model v2 commit`_ 包含所有现有 boards 从旧模型到当前模型的完整转换，
因此你可以将其用作完整转换参考。

.. _hardware model v2 commit: https://github.com/zephyrproject-rtos/zephyr/commit/8dc3f856229ce083c956aa301c31a23e65bd8cd8
.. _example-application conversion Pull Request: https://github.com/zephyrproject-rtos/example-application/pull/58
.. _conversion script: https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/utils/board_v1_to_v2.py

.. _hw_support_hierarchy:

硬件支持层级
**************************

Zephyr 的硬件支持基于一系列层级抽象。
主要地，每个 :term:`board` 有一个或多个 :term:`SoC`。
每个 SoC 可以可选地归类到 :term:`SoC series`，
后者可以可选地属于 :term:`SoC family`。
每个 SoC 有一个或多个 :term:`CPU cluster`，
每个包含一个或多个特定 :term:`architecture` 的 :term:`CPU core`。

你可以在下图可视化层级：

.. figure:: board/hierarchy.png
   :width: 500px
   :align: center
   :alt: Hardware support Hierarchy

   Hardware 支持层级

下面是本节描述的层级的几个示例，
以每行一个 :term:`board` 及其对应层级条目的形式呈现。
注意 :term:`SoC series` 和 :term:`SoC family` 层级并不总是被使用。

.. table::

   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   | :term:`board name`                         | :term:`board qualifiers` | :term:`SoC` | :term:`SoC Series` | :term:`SoC family` | CPU core       | :term:`architecture` |
   +============================================+==========================+=============+====================+====================+================+======================+
   | :zephyr:board:`nrf52dk`                    | nrf52832                 | nRF52832    | nRF52              | Nordic nRF         | Arm Cortex-M4  | ARMv7-M              |
   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   | :zephyr:board:`frdm_k64f <frdm_k64f>`      | mk64f12                  | MK64F12     | Kinetis K6x        | NXP Kinetis        | Arm Cortex-M4  | ARMv7-M              |
   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   | :zephyr:board:`rv32m1_vega <rv32m1_vega>`  | openisa_rv32m1/ri5cy     | RV32M1      | (Not used)         | (Not used)         | RI5CY          | RISC-V RV32          |
   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   | :zephyr:board:`nrf5340dk`                  | nrf5340/cpuapp           | nRF5340     | nRF53              | Nordic nRF         | Arm Cortex-M33 | ARMv8-M              |
   |                                            +--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   |                                            | nrf5340/cpunet           | nRF5340     | nRF53              | Nordic nRF         | Arm Cortex-M33 | ARMv8-M              |
   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   | :zephyr:board:`mimx8mp_evk <imx8mp_evk>`   | mimx8ml8/a53             | i.MX8M Plus | i.MX8M             | NXP i.MX           | Arm Cortex-A53 | ARMv8-A              |
   |                                            +--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   |                                            | mimx8ml8/m7              | i.MX8M Plus | i.MX8M             | NXP i.MX           | Arm Cortex-M7  | ARMv7-M              |
   |                                            +--------------------------+-------------+--------------------+--------------------+----------------+----------------------+
   |                                            | mimx8ml8/adsp            | i.MX8M Plus | i.MX8M             | NXP i.MX           | Cadence HIFI4  | Xtensa LX6           |
   +--------------------------------------------+--------------------------+-------------+--------------------+--------------------+----------------+----------------------+

术语的更多细节可在下一节找到。

.. _board_terminology:

Board 术语
*****************

上一节介绍了 Zephyr 分类和实现硬件支持的层级方式。
本节聚焦于硬件支持周围使用的术语，
特别是在定义和处理 boards 和 SoCs 时。

Zephyr 中围绕 board 概念使用的整套术语在下图中描绘，
该图以 :zephyr:board:`bl5340_dvk` board 作为参考。

.. figure:: board/board-terminology.svg
   :width: 500px
   :align: center
   :alt: Board terminology diagram

   Board 术语图

该图显示了用于描述 boards 的不同术语：

- :term:`board name`：``bl5340_dvk``
- 可选的 :term:`board revision`：``1.2.0``
- :term:`board qualifiers`，可选地描述 :term:`SoC`、
  :term:`CPU cluster` 和 :term:`variant`：``nrf5340/cpuapp/ns``
- :term:`board target`，唯一标识上述组合，
  可用于在使用 Zephyr 提供的工具时指定要为其构建的硬件：
  ``bl5340_dvk@1.2.0/nrf5340/cpuapp/ns``

从形式上看，这也可以看作
:samp:`{board name}[@{revision}][/{board qualifiers}]`，
它可以扩展为
:samp:`{board name}[@{revision}][/{SoC}[/{CPU cluster}][/{variant}]]`。

如果 board 只包含一个单核 SoC，那么 board target 中可以省略 SoC。
这意味着如果 board 未定义任何 board qualifiers，
board 名称可作为 board target 使用。
相反，如果 board qualifiers 是 board 定义的一部分，
那么可以通过省略 SoC 但保留对应的前斜杠来省略它：``//``。

继续上面的示例，board :zephyr:board:`bl5340_dvk` 是单 SoC board，
其中 SoC 定义了两个 CPU cluster：``cpuapp`` 和 ``cpunet``。
其中一个 CPU cluster ``cpuapp`` 额外定义了一个非安全 board variant ``ns``。

board qualifiers ``nrf5340/cpuapp/ns`` 可以读作：

- ``nrf5340``：SoC，它是 Nordic nRF5340 双核 SoC
- ``cpuapp``：CPU cluster ``cpuapp``，它由单个 Cortex-M33 CPU core 组成。
  CPU cluster 中的核心数无法从 board qualifiers 确定。
- ``ns``：一个 variant，在此情况下 ``ns`` 是 Zephyr 中常见的 variant 名称，
  表示支持 :ref:`tfm` 的 boards 的非安全构建。

并非所有 SoCs 都定义 CPU cluster 或 variants。
例如像 :zephyr:board:`thingy52` 这样的简单 board
包含一个没有 CPU cluster 和 variants 的单 SoC。
对于 ``thingy52``，board target ``thingy52/nrf52832`` 可以读作：

- ``thingy52``：board 名称。
- ``nrf52832``：board qualifiers，在此情况下与 SoC 相同，
  它是 Nordic nRF52832。

确保你的 SoC 受支持
*******************************

首先确保你的 SoC 受 Zephyr 支持。
如果是，是时候 :ref:`create-your-board-directory` 了。
如果你不知道，试试：

- 查看 :ref:`boards` 中看起来相关的名称，
  并阅读单独的 board 文档以确认。
- 询问你的 SoC vendor

如果你需要添加 SoC、CPU cluster 甚至 architecture 支持，
此页不是正确的页面，但这里有一些一般建议。

Architecture
=============

参见 :ref:`architecture_porting_guide`。

CPU Core
========

CPU core 支持文件放在 :zephyr_file:`arch` 下的 ``core`` 子目录中，
例如 :zephyr_file:`arch/x86/core`。

参见 :ref:`gs_toolchain` 了解 Zephyr 支持的工具链（编译器、链接器等）信息。
如果你需要支持新工具链，:ref:`build_overview` 是开始学习构建系统的好地方。
如果你正在寻求建议或希望协作支持工具链，请联系社区。

SoC
===

Zephyr SoC 支持文件位于 :zephyr_file:`soc` 的特定于架构的子目录中。
它们通常按 SoC family 分组。

在为已经有 SoC 支持的 vendor 添加新的 SoC family 或 series 时，
请尝试将通用功能提取到共享文件中以避免重复。
如果你的 vendor 还没有支持，你可以在新目录 ``zephyr/soc/<VENDOR>/<YOUR-SOC>`` 中添加它；
请使用自解释的目录名称。

.. _create-your-board-directory:

创建你的 board 目录
***************************

一旦你找到使用你的 SoC 的现有 board，
你通常可以通过复制/粘贴其 board 目录并修改其内容以适配你的硬件来开始。

你需要为你的 board 赋予一个唯一的名称。
运行 ``west boards`` 查看已被占用的名称列表，然后选择一个新的名称。
假设你的 board 叫做 ``plank``（请实际上不要使用该名称）。

从创建 board 目录 ``zephyr/boards/<VENDOR>/plank`` 开始，
其中 ``<VENDOR>`` 是你的 vendor 子目录。
（你不必将 board 目录放在 zephyr 仓库中，但这是开始的最简单方式。
参见 :ref:`custom_board_definition` 了解如何将你的 board 目录
移到单独仓库的文档。）

.. note::
   如果要将你的 board 贡献给 Zephyr，``<VENDOR>`` 子目录是强制要求的，
   但如果你的 board 放在本地仓库中，
   则允许 ``<your-repo>/boards`` 下的任何文件夹结构。
   如果 vendor 在 :zephyr_file:`dts/bindings/vendor-prefixes.txt`
   的列表中有定义，则必须使用该 vendor 前缀作为 ``<VENDOR>``。
   如果 vendor 未定义，可以使用 ``others`` 作为 vendor 前缀。

.. note::

   board 目录名称不必与 board 名称匹配。
   甚至可以在一个目录中定义多个 boards。

你的 board 目录应该如下所示：

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.yml
   ├── board.cmake
   ├── CMakeLists.txt
   ├── doc
   │   ├── plank.webp
   │   └── index.rst
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   ├── plank_<qualifiers>_defconfig
   ├── plank_<qualifiers>.dts
   └── plank_<qualifiers>.yaml

当然，用你的 board 名称替换 ``plank``。

强制文件是：

#. :file:`board.yml`：描述 boards 高层元数据的 YAML 文件，
   例如 boards 名称、它们的 SoCs 和 variants。
   多核 SoCs 的 CPU cluster 不在此文件中描述，
   因为它们继承自 SoC 的 YAML 描述。

#. :file:`plank_<qualifiers>.dts`：以 :ref:`devicetree <dt-guide>`
   格式的硬件描述。
   这声明你的 SoC、连接器和任何其他硬件组件，
   例如 LED、按钮、传感器或通信外设（USB、蓝牙控制器等）。

#. :file:`Kconfig.plank`：选择 SoC 以及其他 board 和 SoC 相关设置的
   基础软件配置。
   不得选择 board 和 SoC 树之外的 Kconfig 设置。
   要选择通用 Zephyr Kconfig 设置，必须使用 :file:`Kconfig` 文件。

可选文件是：

- :file:`Kconfig`、:file:`Kconfig.defconfig`：以 :ref:`kconfig` 格式的
  软件配置。
  这为软件功能和外设驱动程序提供默认设置。
- :file:`plank_defconfig` 和 :file:`plank_<qualifiers>_defconfig`：
  以 Kconfig ``.conf`` 格式的软件配置。
- :file:`board.cmake`：用于 :ref:`flash-and-debug-support`
- :file:`CMakeLists.txt`：如果你需要向构建中添加额外的源文件。
- :file:`doc/index.rst`、:file:`doc/plank.webp`：你的 board 的文档和一张图片。
  只有当你 :ref:`contributing-your-board` 给 Zephyr 时才需要它。
- :file:`plank_<qualifiers>.yaml`：包含 :ref:`twister_script` 使用的
  杂项元数据的 YAML 文件。

形式为 ``<soc>/<cpucluster>/<variant>`` 的 board qualifiers
会被规范化，使得在用于文件名时 ``/`` 被替换为 ``_``，
例如：``soc1/foo`` 在用于文件名时变为 ``soc1_foo``。

.. _board_description:

编写你的 board YAML
*********************

board YAML 文件在高层描述 board。
这包括 SoC、board variants 和 board revisions。

详细配置，例如硬件描述和配置，在 devicetree 和 Kconfig 中完成。

board YAML 文件的骨架是：

.. code-block:: yaml

   board:
     name: <board-name>
     full_name: <board-full-name>
     vendor: <board-vendor>
     revision:
       format: <major.minor.patch|letter|number|custom>
       default: <default-revision-value>
       exact: <true|false>
       revisions:
       - name: <revA>
       - name: <revB>
         ...
     socs:
     - name: <soc-1>
       variants:
       - name: <variant-1>
       - name: <variant-2>
         variants:
         - name: <sub-variant-2-1>
           ...
     - name: <soc-2>
       ...

可以在 board 文件夹中放置多个 boards。
如果多个 boards 放在同一 board 文件夹中，
则 :file:`board.yml` 文件必须以列表形式描述它们，如下所示：

.. code-block:: yaml

   boards:
   - name: <board-name-1>
     vendor: <board-vendor>
     full_name: <board-full-name>
     ...
   - name: <board-name-2>
     vendor: <board-vendor>
     full_name: <board-full-name>
     ...
   ...


.. _default_board_configuration:

编写你的 devicetree
*********************

devicetree 文件 :file:`boards/<vendor>/plank/plank_<qualifiers>.dts`
以 Devicetree Source (DTS) 格式描述你的 board 硬件
（照例，将 ``plank`` 改为你的 board 名称）。
如果你是 devicetree 新手，参见 :ref:`devicetree-intro`。

通常，:file:`plank_<qualifiers>.dts` 应该如下所示：

.. code-block:: devicetree

   /dts-v1/;
   #include <your_soc_vendor/your_soc.dtsi>

   / {
           model = "A human readable name";
           compatible = "yourcompany,plank";

           chosen {
                   zephyr,console = &your_uart_console;
                   zephyr,sram = &your_memory_node;
                   /* other chosen settings  for your hardware */
           };

           /*
            * Your board-specific hardware: buttons, LEDs, sensors, etc.
            */

           leds {
                   compatible = "gpio-leds";
                   led0: led_0 {
                           gpios = </* GPIO your LED is hooked up to */>;
                           label = "LED 0";
                   };
                   /* ... other LEDs ... */
           };

           buttons {
                   compatible = "gpio-keys";
                   /* ... your button definitions ... */
           };

           /* These aliases are provided for compatibility with samples */
           aliases {
                   led0 = &led0; /* now you support the blinky sample! */
                   /* other aliases go here */
           };
   };

   &some_peripheral_you_want_to_enable { /* like a GPIO or SPI controller */
           status = "okay";
   };

   &another_peripheral_you_want {
           status = "okay";
   };

在 board 只包含单个 SoC 且没有任何 board variants 的情况下，
dts 文件可以命名为 :file:`<plank>.dts`，
但由于如果向 board 添加了 variant 或其他 SoC 该文件会静默地不被使用，
因此不推荐这样做。

如果你赶时间，简单硬件通常可以通过复制/粘贴加试错来支持。
如果你想了解细节，需要阅读其余的 devicetree 文档和 devicetree 规范。

.. _dt_k6x_example:

示例：FRDM-K64F 和 Hexiwear K64
===================================

.. Give the filenames instead of the full paths below, as it's easier to read.
   The cramped 'foo.dts<path>' style avoids extra spaces before commas.

本节包含与编写你的 board devicetree 相关的具体示例。

FRDM-K64F 和 Hexiwear K64 board 的 devicetree 分别定义在
:zephyr_file:`frdm_k64fs.dts <boards/nxp/frdm_k64f/frdm_k64f.dts>` 和
:zephyr_file:`hexiwear_k64.dts <boards/mikroe/hexiwear/hexiwear_mk64f12.dts>` 中。
两个 boards 都有来自同一 Kinetis SoC family K6X 的 NXP SoCs。

K6X 的通用 devicetree 定义存储在
:zephyr_file:`nxp_k6x.dtsi <dts/arm/nxp/kinetis/k6x/nxp_k6x.dtsi>` 中，
它被两个 board 的 :file:`.dts` 文件包含。
:zephyr_file:`nxp_k6x.dtsi<dts/arm/nxp/kinetis/k6x/nxp_k6x.dtsi>`
反过来包含 :zephyr_file:`armv7-m.dtsi<dts/arm/armv7-m.dtsi>`，
后者有 Arm v7-M cores 的通用定义。

由于 :zephyr_file:`nxp_k6x.dtsi<dts/arm/nxp/kinetis/k6x/nxp_k6x.dtsi>`
旨在跨基于 K6X 的 boards 通用化，
它使用 ``status`` 属性默认禁用许多设备。
例如，有一个 CAN 控制器定义如下（跳过不重要的部分）：

.. code-block:: devicetree

   can0: can@40024000 {
        ...
        status = "disabled";
        ...
   };

由 board 的 :file:`.dts` 或应用程序 overlay 文件来决定
是否通过设置 ``status = "okay"`` 来启用这些设备。
board 的 :file:`.dts` 文件还负责设备的任何 board 特定配置，
例如添加板载传感器、LED、按钮等的节点。

例如，FRDM-K64（但 Hexiwear K64 不）的 :file:`.dts`
启用 CAN 控制器并设置总线速度：

.. code-block:: devicetree

   &can0 {
        status = "okay";
   };

``&can0 { ... };`` 语法在标签为 ``can0`` 的节点上添加/覆盖属性，
即 :file:`.dtsi` 文件中定义的 ``can@40024000`` 节点。

board 特定定制的其他示例是将 ``aliases`` 和 ``chosen`` 中的属性
指向正确的节点（参见 :ref:`dt-alias-chosen`），
以及进行 GPIO/pinmux 分配。

.. _board_kconfig_files:

编写 Kconfig 文件
*******************

Zephyr 使用 Kconfig 语言配置软件功能。
你的 board 需要提供一些 Kconfig 设置，
然后才能为它编译 Zephyr 应用程序。

设置 Kconfig 配置值在 :ref:`setting_configuration_values` 中详细记录。

board 目录中有一个强制 Kconfig 文件，
对于名为 ``plank`` 的 board 还有几个可选文件：

.. code-block:: none

   boards/<vendor>/plank
   ├── Kconfig
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   └── plank_<qualifiers>_defconfig

:file:`Kconfig.plank`
  一个共享 Kconfig 文件，可以在 Zephyr Kconfig 和 sysbuild
  Kconfig 树中都被 source。

  此文件在 Kconfig 树中选择 SoC 以及潜在的其他 SoC 相关
  Kconfig 设置。
  此文件不得选择可复用 Kconfig board 和 SoC 树之外的任何内容。

  :file:`Kconfig.plank` 可能如下所示：

  .. code-block:: kconfig

     config BOARD_PLANK
             select SOC_SOC1

  Kconfig 符号 :samp:`BOARD_{board}` 和
  :samp:`BOARD_{normalized_board_target}` 由构建系统构造，
  因此上述代码片段中不应定义类型。

:file:`Kconfig`
  由 :zephyr_file:`boards/Kconfig` 包含。

  此文件可以添加特定于当前 board 的 Kconfig 设置。

  并非所有 boards 都有 :file:`Kconfig` 文件。

  board 特定设置应该是定义一个自定义设置，通常带有 prompt，如下所示：

  .. code-block:: kconfig

     config BOARD_FEATURE
             bool "Board specific feature"

  如果设置名称与 Zephyr 中现有的 Kconfig 设置相同，
  并且只修改该设置的默认值，
  则应改用 :file:`Kconfig.defconfig`。

:file:`Kconfig.defconfig`
  Kconfig 选项的 board 特定默认值。

  并非所有 boards 都有 :file:`Kconfig.defconfig` 文件。

  整个文件应位于 ``if BOARD_PLANK`` / ``endif`` 行对内部，如下所示：

  .. code-block:: kconfig

     if BOARD_PLANK

     config FOO
             default y

     if NETWORKING

     config SOC_ETHERNET_DRIVER
             default y

     endif # NETWORKING

     endif # BOARD_PLANK

:file:`plank_<qualifiers>_defconfig`（或在有限情况下 :file:`plank_defconfig`）
  一个 Kconfig fragment，每当为你的 board 编译应用程序时
  原样合并到最终构建目录的 :file:`.config` 中。

  :file:`plank_defconfig` 只能用于没有 qualifiers、没有 variants 且
  存在单个 SoC 的 boards，
  尽管由于如果在上游 Zephyr 的 board 中添加了新 SoC 或 board variant/qualifier，
  samples/tests 或下游使用会突然中断而无警告，
  因此不推荐这种命名风格。

.. note::
   多个文件不会被合并，文件之间也没有回退机制，
   这意味着如果有一个 board 有 2 个不同的 SoCs 且每个有 2 个 board variants，
   :file:`plank_defconfig` 文件对于第一个 qualifier 和 variant 将完全不被使用，
   将使用 :file:`plank_<soc1>_<variant1>_defconfig`，
   它不会包含其他文件。

   ``_defconfig`` 应包含你的 UART、console 等的强制设置。
   结果是特定于架构的，但通常看起来如下所示：

   .. code-block:: cfg

      CONFIG_GPIO=y
      CONFIG_CONSOLE=y
      CONFIG_UART_CONSOLE=y
      CONFIG_SERIAL=y

:file:`plank_x_y_z_defconfig` / :file:`plank_<qualifiers>_x_y_z_defconfig`
  一个 Kconfig fragment，每当为你的 board revision ``x.y.z``
  编译应用程序时原样合并到最终构建目录的 :file:`.config` 中。

构建、测试和修复
********************

现在是时候构建和测试你想在你的 board 上运行的应用程序，
直到你满意为止。

例如：

.. code-block:: console

   west build -b plank samples/hello_world
   west flash

有关 ``west flash`` 如何工作，参见下面的 :ref:`flash-and-debug-support`。
你也可以只用你偏好的任何其他工具刷写 :file:`build/zephyr/zephyr.elf`、
:file:`zephyr.hex` 或 :file:`zephyr.bin`。

在将 board 提交到上游之前，
验证你添加的每个 board target 都能使用仅来自主线 Zephyr 仓库
及其模块的代码通过项目的最小开源测试套件。
该套件目前由以下组成：

- :file:`samples/philosophers`
- :file:`tests/kernel`

例如，为 board target 构建套件：

.. code-block:: console

   west twister -p plank -T samples/philosophers -T tests/kernel

对于有多个 SoCs、CPU cluster、variants 或 revisions 的 boards，
为每个新 board target 重复测试套件。
还建议进行 :zephyr:code-sample:`hello_world` 构建作为快速冒烟检查，
例如：

.. code-block:: console

   west build -p always -b plank/soc1/foo samples/hello_world
   west build -p always -b plank@1.0.0/soc1/foo samples/hello_world

如果 board target 需要，请使用 :ref:`sysbuild`。
当使用 board 测试元数据，例如 board target YAML 文件中的
``testing: only_tags`` 时，
确保该 target 在本地测试或 CI 中仍对照最小测试套件进行验证。

.. _porting-general-recommendations:

一般建议
***********************

为了一致性以及让用户更容易构建保持 board 无关的应用程序，
在移植你打算贡献给 Zephyr 的 board 时，请遵循以下准则：

在 Devicetree 中启用有价值的组件
  有价值的板载组件（LED、按钮、传感器、板载
  USB/Ethernet/BLE/Wi-Fi 等）的 Devicetree 节点必须**默认启用**
  并具有正确的引脚控制和驱动程序配置，
  以便它们开箱即用。

默认禁用子系统（Kconfig）
  不要在 board defconfig 中启用子系统，
  除非它们是基本 board 操作严格必需的，
  或者在这些建议中明确列为例外。

配置系统时钟和 tick 源
  设置一个可工作的系统时钟和 tick 源。

提供默认 console
  使用 ``zephyr,console`` chosen 节点指向用于 console 输出的
  UART 控制器。

  具有内置调试或 USB-to-UART 适配器的 boards
  应将 console 设置为连接到该适配器的 UART 控制器。

  没有任何调试适配器的纯 USB boards
  必须包含通用 USB CDC-ACM
  :zephyr_file:`Kconfig <boards/common/usb/Kconfig.cdc_acm_serial.defconfig>` 和
  :zephyr_file:`DTS <boards/common/usb/cdc_acm_serial.dtsi>` fragment
  以启用 CDC-ACM UART 作为日志和 shell 的默认后端。

添加 :ref:`shield interface <shield-interfaces>` 定义
  对于暴露标准扩展连接器的 boards，添加连接器节点和引脚复用。
  仅启用预期/标准连接器功能所需的外设。

配置引脚和外设实例
  将外设映射到正确的引脚（例如 SPI 在 Arduino SPI 引脚上），
  并提供支持 board 功能的默认 pinmux 条目。

启用网络接口
  如果存在网络硬件，为每种支持的技术配置默认接口，
  以便网络 samples 开箱即用。

启用 GPIO 控制器
  应启用所有连接到板载组件或扩展连接器的 GPIO 端口。

启用 MPU 和栈保护
  建议在有 MPU 时启用它（除非内存资源过于有限）。
  当启用 MPU 时，建议还启用硬件栈保护
  （:kconfig:option:`CONFIG_HW_STACK_PROTECTION`）
  以便通过允许内核检测栈溢出来简化调试。

.. _flash-and-debug-support:

Flash 和调试支持
***********************

Zephyr 通过 west 扩展命令支持 :ref:`west-build-flash-debug`。

要为你的 board 添加 ``west flash`` 和 ``west debug`` 支持，
你需要在 board 目录中创建一个 :file:`board.cmake` 文件。
此文件的作用是为你的 board 配置一个 "runner"。
（要让 ``west build`` 支持你的 board，不需要做特别的事情。）

"Runners" 是 Zephyr 特定的 Python 类，
它们封装 :ref:`flash and debug host tools <flash-debug-host-tools>`
并与 west 和 zephyr 构建系统集成以支持 ``west flash`` 和相关命令。
每个 runner 支持刷写、调试或两者兼有。
你需要在 :file:`board.cmake` 中配置这些 Python 脚本的参数
以支持这些命令，如下面的示例 :file:`board.cmake` 所示：

.. code-block:: cmake

   board_runner_args(jlink "--device=nrf52" "--speed=4000")
   board_runner_args(pyocd "--target=nrf52" "--frequency=4000000")

   include(${ZEPHYR_BASE}/boards/common/nrfutil.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/nrfjprog.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
   include(${ZEPHYR_BASE}/boards/common/pyocd.board.cmake)

此示例配置了 ``nrfutil``、``nrfjprog``、``jlink`` 和 ``pyocd`` runners。

.. warning::

   Runners 通常有与其封装的工具匹配的名称，
   因此 ``jlink`` runner 封装 Segger 的 J-Link 工具，等等。
   但 runner 命令行选项如 ``--speed`` 等是特定于 Python 脚本的。

.. note::

   如果工具支持多个操作系统，
   runners 和 board 配置应在创建时不针对单个操作系统，
   也不应依赖特殊的系统设置/配置。
   例如：不要假设用户具有先验知识/配置或
   （如果使用 Linux）安装了特殊 udev 规则，
   不要假设所有平台都有特定的 ``/dev/X`` 设备，
   因为这与 Windows 或 macOS 不兼容，
   并允许覆盖所选设备，
   以便可以将多个 boards 连接到单个系统
   并按用户选择进行刷写/调试。

有关更多细节：

- 运行 ``west flash --context`` 查看支持刷写的可用 runners 列表，
  运行 ``west flash --context -r <RUNNER>`` 查看
  单个 runner 的特定可用选项。
- 运行 ``west debug --context`` 和 ``west debug --context <RUNNER>``
  获取支持调试的 runners 的相同输出。
- 运行 ``west flash --help`` 和 ``west debug --help``
  获取刷写和调试的顶层选项。
- 参见 :ref:`west-runner` 了解 Python API。
- 查找与你自己的 board 类似的 boards 的 :file:`board.cmake` 文件
  以获取更多示例。

要查看 ``west flash`` 或 ``west debug`` 命令具体在做什么，
以详细模式运行它：

.. code-block:: sh

   west --verbose flash
   west --verbose debug

详细模式打印 runner 使用的任何 host 工具命令。

:file:`board.cmake` 中 ``include()`` 调用的顺序很重要。
第一个 ``include`` 设置默认 runner（如果尚未设置）。
例如，首先包含 ``nrfjprog.board.cmake``
意味着 ``nrfjprog`` 是该 board 的默认 flash runner。
由于 ``nrfjprog`` 不支持调试，``jlink`` 是默认调试 runner。

.. _porting_board_revisions:

多个 board revisions
************************

参见 :ref:`application_board_version` 了解从用户角度
此功能的基础知识。

Board revisions 在 :file:`board.yml` 的 ``revision`` 条目中描述。

.. code-block:: yaml

   board:
     revision:
       format: <major.minor.patch|letter|number|custom>
       default: <default-revision-value>
       exact: <true|false>
       revisions:
       - name: <revA>
       - name: <revB>

Zephyr 原生支持以下 revision 格式：

- ``major.minor.patch``：匹配三位 revision，例如 ``1.2.3``。
- ``number``：匹配整数 revisions
- ``letter``：仅匹配从 ``A`` 到 ``Z`` 的单个字母 revisions

.. _board_fuzzy_revision_matching:

模糊 revision 匹配
=======================

模糊 revision 匹配默认启用。

如果用户选择可用 revisions 之间的一个 revision，
将使用不大于用户选择的最接近的 revision 号。
例如，如果 board ``plank`` 定义了 revisions ``0.5.0`` 和 ``1.5.0``
且用户为 ``plank@0.7.0`` 构建，
构建系统将针对 revision ``0.5.0``。

构建系统将在 CMake 配置时打印此内容：

.. code-block:: console

   -- Board: plank, Revision: 0.7.0 (Active: 0.5.0)

这允许你只为引入不兼容更改的 board revision 号
创建 revision 配置文件。

类似地，对于 ``letter`` revision 格式，
如果定义了 revisions ``A``、``D`` 和 ``F``
且用户为 ``plank@E`` 构建，构建系统将针对 revision ``D``。

精确 revision 匹配
=======================

当 :file:`board.yml` 的 revision 部分中指定 ``exact: true`` 时，
启用精确 revision 匹配。

当定义 exact 时，在上述示例中为 ``plank@0.7.0`` 构建
将导致以下错误消息：

.. code-block:: console

   Board revision `0.7.0` not found.  Please specify a valid board revision.

Board revision 配置调整
=======================================

当用户为 board ``plank@<revision>`` 构建时，
可以对该 board 的常规配置进行调整。

如 :ref:`default_board_configuration` 和
:ref:`board_kconfig_files` 节所述，
board 默认配置由文件 :file:`<board>.dts` / :file:`<board>_<qualifiers>.dts`
和 :file:`<board>_defconfig` / :file:`<board>_<qualifiers>_defconfig` 创建。
当为特定 board revision 构建时，
上述文件用作起点，此外将使用以下 board 文件：

- :file:`<board>_<qualifiers>_<revision>_defconfig`：
  特定 revision defconfig，
  仅用于由 ``<board>_<qualifiers>`` 标识的 board 和 SOC / variants。

- :file:`<board>_<qualifiers>_<revision>.overlay`：
  特定 revision dts overlay，
  仅用于由 ``<board>_<qualifiers>`` 标识的 board 和 SOC / variants。

这种拆分允许有多个 SoCs、多核 SoCs 或 variants 的 boards
将适用于所有 SoCs 和 variants 的通用 revision 调整
放在单个文件中，
同时仍提供将 SoC 或 variant 特定调整
放在专用 revision 文件中的能力。

使用前面章节中的 ``plank`` board，
我们可以有以下 revision 调整：

.. code-block:: none

   boards/zephyr/plank
   ├── plank_soc1_foo_1_5_0.overlay   # DTS overlay for plank board when building for soc1 variant foo on revision 1.5.0
   └── plank_soc1_foo_1_5_0_defconfig # Kconfig adjustment for plank board when building for soc1 variant foo on revision 1.5.0

自定义 revision.cmake 文件
***************************

某些 boards 可能不使用 Zephyr 原生支持的 board revisions。
例如字符串 revisions。

Zephyr 不支持字符串 revisions 的原因之一是
字符串可以有许多形式，
并且并不总是清楚给定的字符串只是字符串，
例如 ``blue``、``green``、``red`` 等，
还是提供可以匹配更高或更低 revisions 的顺序，
例如 ``alpha``、``beta``、``gamma``。

由于字符串的可能性数量巨大，
包括内部进行正则表达式匹配的可能性，
那么字符串 revisions 必须使用 ``custom`` revision 类型完成。

要向构建系统指示使用 ``custom`` revisions，
:file:`board.yml` 的 ``revision`` 部分中的 format 字段必须写为：

.. code-block:: yaml

   board:
     revision:
       format: custom

当使用 custom revisions 时，
必须在 board 目录中创建 :file:`revision.cmake`。

:file:`revision.cmake` 将在为 board 构建时被构建系统包含，
验证用户指定的 revision 是该文件的责任。

:makevar:`BOARD_REVISION` 变量保存用户指定的 revision 值。

要向构建系统发出信号应使用不同于用户指定的 revision，
:file:`revision.cmake` 可以将 CMake 变量
:cmake:variable:`ACTIVE_BOARD_REVISION` 设置为要替代使用的 revision。
对应的 Kconfig 文件和 devicetree overlays 必须命名为
:file:`<board>_<ACTIVE_BOARD_REVISION>_defconfig` 和
:file:`<board>_<ACTIVE_BOARD_REVISION>.overlay`。

.. _contributing-your-board:

贡献你的 board
***********************

如果你想将你的 board 贡献给 Zephyr，首先——谢谢！

还有一些额外的事情你需要做：

#. 确保你已遵循所有 :ref:`porting-general-recommendations`。
   它们是包含在 Zephyr 中的 boards 的要求。

#. 使用模板文件 :zephyr_file:`doc/templates/board.tmpl`
   为你的 board 添加文档。
   参见 :ref:`zephyr_doc` 了解如何在提交
   pull request 之前构建你的文档的信息。

#. 准备一个添加你的 board 的 pull request，
   遵循 :ref:`contribute_guidelines`。

.. _extend-board:

Board 扩展
****************

Zephyr 中的 board 硬件模型允许你用新的 board variants
扩展现有 board。
这样的 board 扩展可以在你的自定义仓库中完成，
从而在 Zephyr 仓库之外。

用额外的 variant 扩展现有 board
允许你调整现有 board，
从而在构建期间选择为现有的、未修改的 board 构建，
或为新的 variant 构建。

要扩展现有 board，首先在你的扩展 board 中
创建一个 :file:`board.yml`。
确保使用 :ref:`create-your-board-directory` 中描述的目录结构。

扩展示 board 的 board YAML 文件骨架是：

.. code-block:: yaml

   board:
     extend: <existing-board-name>
     variants:
       - name: <new-variant>
         qualifier: <existing-qualifier>

当扩展示 board 时，你的 board 目录应如下所示：

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.yml
   ├── plank_<new-qualifiers>_defconfig
   └── plank_<new-qualifiers>.dts

用你扩展的 board 的真实名称替换 ``plank``。

在某些情况下，你可能还想调整额外设置，
例如 :file:`Kconfig.defconfig` 或 :file:`Kconfig.{board}`。
因此扩展示 board 时也可以额外提供以下内容。

.. code-block:: none

   boards/<VENDOR>/plank
   ├── board.cmake
   ├── Kconfig
   ├── Kconfig.plank
   ├── Kconfig.defconfig
   └── plank_<new-qualifiers>.yaml
