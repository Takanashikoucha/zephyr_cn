.. _twister_script:

测试运行器（Twister）
#####################

Twister 扫描 git 仓库中的一组测试应用并尝试执行它们。默认情况下，它尝试在
board 定义文件中标记为默认（default）的 board 上构建每个测试应用。

默认选项会在定义的一组 board 上构建大多数测试应用，并在所测试的架构或配置
可用的模拟环境中运行。

由于测试执行覆盖范围有限，Twister 不能保证本地更改在完整构建环境中会成功，
但它通过为不同 board 和不同配置构建示例（samples）和测试（tests）执行了足够的
测试，有助于保持完整代码树可构建。

当使用（至少）一个 ``-v`` 选项时，Twister 的控制台输出会显示每个测试应用
的测试是如何运行的（qemu、native_sim 等），或者二进制文件只是被构建。测试的
:ref:`状态 <twister_statuses>` 同样会报告在 ``twister.json`` 和其他报告文件中。
Twister 只构建测试而不运行它的原因有以下几种：

- 测试在其 ``.yaml`` 配置文件中被标记为 ``build_only: true``。
- 测试配置定义了 ``harness``，但你没有安装它或没有配置好。
- 目标设备未连接，无法用于烧录。
- 你或某个更高层的自动化用 ``--build-only`` 调用了 Twister。

要在本地代码树中运行 Twister，请遵循以下步骤：

.. code-block:: console

   $ west twister

.. note::

   本文档中的示例以 ``west twister`` 形式调用 Twister，即 :ref:`west <west>`
   扩展命令，它在所有主机操作系统上的行为相同。以下调用方式是等价的：

   * ``west twister ...``（推荐）。
   * ``python .\scripts\twister ...``（Windows）：直接调用脚本。这需要先设置
     Zephyr 环境（``source zephyr-env.sh`` 或 ``zephyr-env.cmd``）。

   所有形式接受相同的命令行选项。

如果你想在某个或某些特定平台上运行测试，可以使用 ``--platform`` 选项，
它是用于测试的平台过滤器；使用该选项后，测试套件只会在指定的平台上构建/运行。
该选项还支持同一 board 的不同版本，你可以用 ``--platform board@revision``
在特定版本上测试。

Twister 支持的命令行选项列表可以用 ``west twister --help`` 查看。
完整的选项集参见 :ref:`twister_commandline_options`。

以下页面介绍 Twister 的其他主题：

.. toctree::
   :maxdepth: 1

   commandline
   pytest
   twister_statuses
   twister_blackbox

.. _twister_board_configuration:

Board 配置
*************

要为特定 board 构建测试，并在真实硬件或 QEMU 等模拟环境中执行部分测试，
需要一个 board 配置文件。该文件足够通用，也可以用于其他需要 board 清单的任务；
否则，关于 board 及其配置的细节只在构建时可用。

board 元数据文件位于 board 目录中，使用 YAML 标记语言组织。下面的示例展示了一个
包含该特定 board 最佳测试覆盖所需数据的 board：

.. code-block:: yaml

   identifier: frdm_k64f
   name: NXP FRDM-K64F
   type: mcu
   arch: arm
   toolchain:
     - zephyr
     - gnuarmemb
   supported:
     - arduino_gpio
     - arduino_i2c
     - netif:eth
     - adc
     - i2c
     - nvs
     - spi
     - gpio
     - usb_device
     - watchdog
     - can
     - pwm
   testing:
     default: true


identifier:
   一个字符串，与 board 在构建系统中的定义方式相匹配。构建时使用同一个字符串，
   例如调用 ``west build`` 或 ``cmake`` 时：

   .. code-block:: console

      # with west
      west build -b reel_board
      # with cmake
      cmake -DBOARD=reel_board ..

name:
   board 在营销材料中显示的实际名称。
vendor:
   board 供应商。用于 ``vendor_allow`` 和 ``vendor_exclude`` 测试场景过滤器。
tier:
   一个可选整数，指示 board 支持层级。用于报告以及按支持级别对平台分组。
type:
   board 或配置的类型。取值为 ``mcu``、``qemu``、``sim``、``unit`` 或 ``native`` 之一。
simulation:
   用于模拟平台的模拟器，例如 qemu。

   .. code-block:: yaml

       simulation:
         - name: qemu
         - name: armfvp
           exec: FVP_Some_Platform
         - name: custom
           exec: AnotherBinary

   默认情况下，测试使用 simulation 数组中的第一个条目执行。
   可以用 ``--simulation <simulation_name>`` 选择另一个模拟器。
   ``exec`` 属性是可选的。如果设置了它但所需模拟器不可用，测试只会被构建。
   如果未设置它且所需模拟器不可用，测试将无法运行。
   模拟器名称必须与 ``SUPPORTED_EMU_PLATFORMS`` 中的某个元素匹配。
arch:
   board 的架构。
toolchain:
   可以构建该 board 的支持工具链列表。这应与命令行构建时用于
   :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 的值之一匹配。
   Twister 会过滤掉工具链不在此列表中的任何测试实例，除非给出了
   ``--force-toolchain``。该列表说明哪些工具链 *可能* 构建该 board，
   它不选择某一个；参见 :ref:`twister_toolchain_selection`。
preferred_toolchain:
   当没有其他选择时，Twister 应为该平台使用的工具链。
   这对名义上可以用多个工具链构建、但应该用特定一个测试的 board 很有用。
   参见 :ref:`twister_toolchain_selection`。
build_toolchains:
   一个可选的工具链列表，分配给该平台的每个测试都应使用列表中的工具链构建。
   Twister 为列表中的每个工具链创建一个测试实例，每个位于自己的构建目录中，
   而不是为平台选择单一工具链。例如，要在 ``native_sim`` 上同时用 GCC 和
   Clang 构建所有测试：

   .. code-block:: yaml

       build_toolchains:
         - host/gnu
         - host/llvm

   由于这会使构建时间成倍增加，通常最好把它排除在 board 定义之外，
   仅通过 :ref:`Twister 配置文件 <twister_test_config>` 的 ``build_toolchains``
   选项为 CI 启用。参见 :ref:`twister_toolchain_selection`。
ram:
   board 上可用的 RAM（以 KB 指定）。用于匹配测试场景的需求。
   如果未指定，默认为 128KB。
flash:
   board 上可用的 FLASH（以 KB 指定）。用于匹配测试场景的需求。
   如果未指定，默认为 512KB。
sysbuild: [True|False] (default False)
   如果为 true，该平台的默认应用使用 :ref:`sysbuild <sysbuild>` 构建。
twister: [True|False] (default True)
   如果为 false，Twister 完全忽略该平台，从不构建或运行其上的测试。
supported:
   该 board 支持的特性列表。可以指定为单个词的特性，或某个特性类的变体。例如：

   .. code-block:: yaml

         supported:
           - pci

   这表示该 board 支持 PCI。你可以让测试场景只在此类 board 上构建或运行，或者：

   .. code-block:: yaml

         supported:
           - netif:eth
           - sensor:bmi16

   测试场景可以依赖 'eth' 只测试以太网，或依赖 'netif' 在任何具有网络接口的
   board 上运行。

testing:
   与测试相关的关键词，用于为该 board 的特性提供最佳覆盖。

   .. _twister_default_testing_board:

   binaries:
     需要保留用于设备测试的自定义二进制文件列表。
   default: [True|False]:
     这是一个默认 board，它将以最高优先级进行测试，并在不带任何额外参数
     调用简化版 Twister 时被覆盖。
   ignore_tags:
     不要尝试构建（因而也不运行）标记了此列表标签的测试。
   only_tags:
     只在特定平台上执行带有此列表标签的测试。
   timeout_multiplier: <float> (default 1)
     .. _twister_board_timeout_multiplier:

     将每个测试场景的超时时间乘以指定比例。该选项允许只为所需平台调整超时时间。
     对于天然较慢的平台（例如带省电但慢速 CPU 的硬件 board，或能执行指令级
     精确模拟但速度很慢的模拟平台）可能很有用。

   flash_before: [True|False] (default False)
     对于 pytest/shell 测试框架的硬件测试，在打开串口之前先烧录设备。
     这可以防止某些 board（例如烧录过程中会重置的 USB CDC）在烧录期间
     出现串口断开问题。

   renode:
     Renode 模拟器的配置。支持两个键：``uart``，测试框架连接的 UART 外设
     （例如 ``sysbus.uart0``）；以及 ``resc``，用于设置模拟机器的
     Renode 脚本（``.resc``）。

env:
   环境变量列表。Twister 会检查是否设置了所有这些环境变量，否则跳过该平台。
   这允许用户定义一个平台，例如仅在所需软件或硬件存在时才使用它，
   并用这些环境变量将该存在性信号传递给 Twister。

variants:
   从 board 变体（限定符）名称到按变体覆盖项的映射。每个条目本身就是一个
   平台定义，可以为该特定变体覆盖上述任意键，同时从顶层定义继承其余值。

.. _twister_toolchain_selection:

工具链选择
*************

多个选项会影响测试使用哪个工具链构建。它们分为三组：*选择* 工具链的选项、
*过滤* 掉工具链不可用的测试实例的选项，以及将一个测试*倍增* 为多个构建的选项。

Twister 首先通过调用 ``cmake/verify-toolchain.cmake`` 为整个运行确定默认工具链，
它会遵循 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 环境变量。该值会在运行开始时
以 ``Using '<toolchain>' toolchain variant.`` 的形式报告。

对于每个测试场景与平台的组合，随后按以下第一条适用规则选择工具链：

#. 测试场景的 ``integration_toolchains``（如果已设置）。测试为每个列出的
   工具链构建一次。
#. 平台的 ``build_toolchains``（如果已设置），无论是在 board 配置中还是在
   :ref:`Twister 配置文件 <twister_test_config>` 中。测试为每个列出的
   工具链构建一次。
#. 对于 ``posix`` 和 ``unit`` 平台，如果运行默认值是 ``host/llvm`` 则使用
   ``host/llvm``，否则使用 ``host/gnu``。
#. 平台的 ``preferred_toolchain``（如果已设置）。
#. 上面描述的运行默认值；如果无法确定，则使用 ``zephyr``。

注意 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 只改变运行默认值，即本列表中的
最后一项。它不会覆盖平台的 ``preferred_toolchain`` 或 ``build_toolchains``，
也不会覆盖测试场景的 ``integration_toolchains``。

选定工具链后，生成的测试实例仍可能被过滤掉：

* 如果工具链不在平台 ``toolchain`` 支持工具链列表中，该实例会被过滤。
  ``--force-toolchain`` 会禁用此检查并无条件使用所选工具链。
  比较在 ``/`` 之前的部分也成功，因此 ``host/gnu`` 能匹配列出 ``host`` 的平台。
* 测试场景的 ``toolchain_allow`` 和 ``toolchain_exclude`` 选项按所选工具链
  过滤实例。

由于 ``integration_toolchains`` 和 ``build_toolchains`` 会为每个工具链生成一个
测试实例，它们会使构建时间成倍增加。因此 ``build_toolchains`` 通常不出现在
board 配置中，而只在 CI 使用的配置文件中启用。

.. _twister_tests_long_version:

测试
*****

测试通过应用项目目录中存在 ``tests.yaml`` 文件（对 ``sample.yaml`` 和
``testcase.yaml`` 的支持已弃用）来检测。该测试应用配置文件可以在 ``tests:``
部分包含一个或多个条目，每个条目标识一个测试场景（Test Scenario）。

.. _twister_test_project_diagram:

.. figure:: figures/twister_test_project.svg
   :alt: Twister and a Test application project.
   :figclass: align-center

   Twister 与一个测试应用项目。


测试应用配置使用 YAML 语法编写，与示例（sample）共享相同的结构。

测试场景（Test Scenario）是定义在测试场景条目中的一组条件和变量，
在这些条件下，一组测试套件（Test Suite）将被构建并执行。

测试套件（Test Suite）是一组测试用例（Test Case）的集合，旨在用于测试
软件程序以确保其满足某些要求。测试套件中的测试用例彼此相关，
或打算一起执行。

测试场景、测试套件和测试用例名称必须遵循以下基本规则：

#. 测试场景标识符的格式应为不含任何空格或特殊字符的字符串（允许的字符：
   字母数字和 [\_=]），由以点（``.``）分隔的多个部分组成。

#. 每个测试场景标识符应以一个部分名称开头，后跟以点（``.``）分隔的子部分名称。
   例如，覆盖内核中信号量（semaphore）的测试场景应以 ``kernel.semaphore`` 开头。

#. 所有测试场景名称在 Twister 执行范围内必须唯一。

#. 测试套件的完整规范名称为：
   ``<测试应用项目路径>/<测试场景标识符>``

#. 根据测试套件实现的不同，其测试用例标识符由**至少三个部分**组成，
   以点（``.``）分隔：

   * **Ztest 测试**：
     来自对应 ``testcase.yaml`` 文件的测试场景标识符、Ztest 套件名称和
     Ztest 测试名称：
     ``<测试场景标识符>.<Ztest 套件名称>.<Ztest 测试名称>``

   * **独立测试和示例**：
     来自对应 ``tests.yaml`` 文件的测试场景标识符，其中最后一部分表示
     独立测试用例名称，例如：``debug.coredump.logging_backend``。


下面是一个测试配置示例，其中包含本文档中解释的几个选项。


  .. code-block:: yaml

        tests:
          bluetooth.gatt:
            build_only: true
            platform_allow:
              - qemu_cortex_m3
              - qemu_x86
            tags:
              - bluetooth
          bluetooth.gatt.br:
            build_only: true
            extra_args:
              -CONF_FILE="prj_br.conf"
            filter: not CONFIG_DEBUG
            platform_exclude:
              -up_squared
            platform_allow:
              - qemu_cortex_m3 qemu_x86
            tags:
              - bluetooth


带测试的示例（sample）具有相同的结构，并包含与示例及其演示内容相关的
附加信息：

  .. code-block:: yaml

        sample:
          name: hello world
          description: Hello World sample, the simplest Zephyr application
        tests:
          sample.basic.hello_world:
            build_only: true
            tags:
              - tests
            min_ram: 16
          sample.basic.hello_world.singlethread:
            build_only: true
            extra_args: CONF_FILE=prj_single.conf
            filter: not CONFIG_BT
            tags:
              - tests
            min_ram: 16

``tests:`` YAML 字典中的测试场景条目以其测试场景标识符作为键。

测试应用配置中的每个测试场景条目可以定义以下键/值对：

..  _test_config_args:

tags: <标签列表> (required)
    测试场景的一组字符串标签。通常与功能域相关，但可以是任意内容。
    通过命令行调用该脚本时，可以基于标签过滤要运行的测试集。

skip: <True|False> (default False)
    无条件跳过测试场景。例如，可用于已损坏的测试。

slow: <True|False> (default False)
    除非命令行传入了 ``--enable-slow`` 或 ``--enable-slow-only``，
    否则不运行该测试场景。用于耗时的测试场景，这些场景只在特定情况下
    （如每日构建）才运行。这些测试场景仍会被编译。

extra_args: <额外参数列表>
    构建或运行测试场景时传递给构建工具的额外参数。

    使用命名空间，可以将 extra_args 仅应用于某些硬件。
    目前支持架构/平台/模拟器：

    .. code-block:: yaml

        common:
          tags:
           - drivers
           - adc
        tests:
          test:
            depends_on: adc
          test_async:
            extra_args:
              - arch:x86:CONFIG_ADC_ASYNC=y
              - platform:qemu_x86:CONFIG_DEBUG=y
              - platform:mimxrt1060_evk:SHIELD=rk043fn66hs_ctg
              - simulation:qemu:CONFIG_MPU=y

extra_configs: <额外配置列表>
    构建或运行测试场景时与主 prj.conf 合并的额外配置选项。例如：

    .. code-block:: yaml

        common:
          tags:
            - drivers
            - adc
        tests:
          test:
            depends_on: adc
          test_async:
            extra_configs:
              - CONFIG_ADC_ASYNC=y

    使用命名空间，可以将配置仅应用于某些硬件。
    目前同时支持架构和平台：

    .. code-block:: yaml

        common:
          tags:
            - drivers
            - adc
        tests:
          test:
            depends_on: adc
          test_async:
            extra_configs:
              - arch:x86:CONFIG_ADC_ASYNC=y
              - platform:qemu_x86:CONFIG_DEBUG=y


extra_conf_files: <配置文件列表>
    合并到构建中的额外 Kconfig 片段文件，作为通过 ``extra_args`` 传递
    ``CONF_FILE=`` 的替代方案。``common`` 和测试场景的条目会被拼接。
    对于配置文件，优先使用此字段而非 ``extra_args``。

extra_overlay_confs: <覆盖配置文件列表>
    合并到构建中的额外 Kconfig 覆盖片段，作为通过 ``extra_args`` 传递
    ``OVERLAY_CONFIG=`` 的替代方案。``common`` 和测试场景的条目会被拼接。

extra_dtc_overlay_files: <设备树覆盖文件列表>
    应用于构建的额外设备树（devicetree）覆盖文件，作为通过 ``extra_args``
    传递 ``DTC_OVERLAY_FILE=`` 的替代方案。``common`` 和测试场景的条目会被拼接。

build_only: <True|False> (default False)
    如果为 true，即使测试可以在该平台上运行，Twister 也不会尝试运行它。

    此关键字保留给用于验证某些代码是否确实能构建的测试。
    ``build_only`` 测试不设计为在任何环境中运行，也不应测试任何功能，
    它只验证代码能构建。

    该选项通常用于测试驱动（driver）以及它们在 Zephyr 中被正确启用且
    代码能构建的事实，例如传感器驱动。此类测试不应用于验证驱动的功能。

build_on_all: <True|False> (default False)
    如果为 true，尝试在所有可用平台上构建测试场景。这主要用于 CI 中
    增加覆盖。不要在新测试中使用此标志。

depends_on: <特性列表>
    board 或平台可以声明其支持的特性，该选项只会在提供此特性的
    平台上启用测试。

levels: <级别列表>
    该测试应所属的测试级别。如果存在某级别，该测试可以用命令行选项
    ``--level <level name>`` 选择。

min_ram: <整数>
    该测试构建和运行所需的估计最小 RAM（以 KB 计）。
    会与 board 元数据提供的信息进行比较。

min_flash: <整数>
    该测试构建和运行所需的估计最小 ROM（以 KB 计）。
    会与 board 元数据提供的信息进行比较。

.. _twister_test_case_timeout:

timeout: <秒数>
    运行测试的时长，超时后自动终止测试。
    默认为 60 秒。

arch_allow: <架构列表，例如 x86、arm、arc>
    该测试场景只应运行的架构集合。

arch_exclude: <架构列表，例如 x86、arm、arc>
    该测试场景不应运行的架构集合。

toolchain_allow: <工具链变体列表>
    该测试场景只应运行的工具链变体集合。
    工具链是运行时配置的工具链（参见
    :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`）。用其他任何工具链构建的
    平台会被过滤掉。

toolchain_exclude: <工具链变体列表>
    该测试场景不应运行的工具链变体集合。

vendor_allow: <供应商列表>
    该测试场景只应运行的平台供应商集合。
    供应商作为 board 定义的一部分定义。与此供应商关联的 board 会被包含，
    其他 board（包括没有供应商的）会被排除。

vendor_exclude: <供应商列表>
    该测试场景不应运行的平台供应商集合。
    供应商作为 board 的一部分定义。与此供应商关联的 board 会被排除。

platform_allow: <平台列表>
    该测试场景只应运行的平台集合。不要出于时间或资源限制
    在 CI 中用此选项限制测试或构建；该选项只应在测试或示例
    只能在允许的平台（且无其他平台）上运行时使用。

integration_platforms: <平台/boards 的 YML 列表>
    当 Twister 以 ``--integration`` 选项调用时，该选项将范围限制到
    列出的平台。如果目的是出于时间或资源限制缩小范围，
    应使用此选项而非 platform_allow。

integration_toolchains: <工具链变体的 YML 列表>
    该选项将范围扩展到所有列出的工具链变体，在需要时增加另一个
    测试维度。默认情况下，测试配置基于环境中配置的工具链生成：

    test scenario -> platforms1 -> toolchain1
    test scenario -> platforms2 -> toolchain1


    当平台支持多个在 Twister 运行期间可用的工具链时，
    可以扩展测试配置以包含每个工具链的额外测试。例如，如果平台支持
    工具链 ``toolchain1`` 和 ``toolchain2``，且测试场景包含：

    .. code-block:: yaml

      integration_toolchains:
        - toolchain1
        - toolchain2

    则生成以下配置：

    test scenario -> platforms1 -> toolchain1
    test scenario -> platforms1 -> toolchain2
    test scenario -> platforms2 -> toolchain1
    test scenario -> platforms2 -> toolchain2


    .. note::

      此功能始终会被评估，不限于 ``--integration`` 选项。

    该选项优先于平台的 ``build_toolchains``。若要为平台上每个测试（而非
    每个测试场景）扩展工具链范围，请使用 ``build_toolchains``。
    参见 :ref:`twister_toolchain_selection`。

platform_exclude: <平台列表>
    该测试场景不应运行的平台集合。

platform_type: <平台类型列表>
    将该测试场景限制为给定类型的平台。平台的类型通过其 board 元数据中的
    ``type:`` 键声明。支持的值是 ``mcu``、``qemu``、``sim``、``unit`` 和
    ``native``。类型不在此列表中的平台会被过滤掉。

simulation_exclude: <模拟器列表>
    该测试场景不应运行的模拟器集合。支持的值是 ``qemu``、``simics``、
    ``xt-sim``、``renode``、``nsim``、``mdb-nsim``、``tsim``、``armfvp``、
    ``native`` 和 ``custom``。

extra_sections: <额外二进制段列表>
    计算大小时，如果 Twister 在 Zephyr 二进制文件中发现额外的、
    未预期的段，除非它们在此处命名，否则会报告错误。
    这些段不会包含在大小计算中。

sysbuild: <True|False> (default False)
    使用 sysbuild 基础设施构建项目。只有主项目生成的设备树和
    Kconfig 会用于过滤测试。
    设备测试必须使用硬件映射，或用 west flash 将镜像加载到目标上。
    west flash 的 ``--erase`` 选项与此选项不兼容。使用不支持的选项
    会导致需要 sysbuild 支持的测试被跳过。

harness: <字符串>
    ``testcase.yaml`` 文件中的 harness 关键字标识成功运行测试所需的
    Twister 测试框架（harness）。测试框架是 Twister 的功能，由 Twister 实现；
    某些测试框架被定义为占位符，尚无实现。

    测试框架可以看作 Twister 中需要实现的处理器，用于评估测试是否通过
    判据。例如，键盘测试框架设置在需要键盘交互才能判断测试通过或失败的
    测试上，然而 Twister 目前缺少该测试框架的实现。

    支持的测试框架：

    - ztest
    - test
    - console
    - pytest
    - gtest
    - robot
    - ctest
    - shell
    - power
    - display_capture
    - script
    - bsim

    更多信息参见 :ref:`twister_harnesses`。

platform_key: <平台属性列表>
    通常，测试只需构建并运行一次即可算作通过。设想一个依赖平台架构的
    代码库，在每个架构的单个平台上通过测试即足以判定测试和代码通过。
    platform_key 属性使这成为可能。

    例如，以 (arch, simulation) 作为键，确保测试在每个架构和模拟器上
    运行一次（这是最常见的情况）：

    .. code-block:: yaml

      platform_key:
        - arch
        - simulation

    添加 platform（board）属性以包含 soc 名称、soc 系列，以及实现
    每个外设接口的 IP 块集合，可以实现其他有趣的用途。例如，
    这可以使得为每个唯一 IP 块构建并运行 SPI 测试各一次。

harness_config: <测试框架配置选项>
    用于选择 board 和/或处理通用 Console（配合正则匹配）的额外测试框架
    配置选项。Config 可以声明其支持的特性。该选项使测试只会在满足
    此外部依赖的平台上运行。


    fixture: <字符串或列表>
        指定测试场景对外部设备（例如传感器）的依赖，并标识满足此依赖的
        设置。它依赖于特定测试设置和 board 选择逻辑，基于 ``fixture``
        关键字从多个满足依赖的 board 中选出特定 board（在自动化设置中）。
        一些示例 fixture 名称：i2c_hts221、i2c_bme280、i2c_FRAM、
        ble_fw 和 gpio_loop。

    ztest_suite_repeat: <int> (default 1)
        此参数指定整个测试套件应重复的次数。

    ztest_test_repeat: <int> (default 1)
        此参数指定测试套件中每个单独测试应重复的次数。

    ztest_test_shuffle: <True|False> (default False)
        此参数指示测试套件中测试的顺序是否应打乱。
        设置为 ``true`` 时，测试将以随机顺序执行。



    下面是一个包含 robot 测试框架 harness_config 选项的 yaml 文件示例。

    .. code-block:: yaml

        tests:
          robot.example:
            harness: robot
            harness_config:
              robot_testsuite: [robot file path]

    可以使用列表指定多个测试套件。

    .. code-block:: yaml

        tests:
          robot.example:
            harness: robot
            harness_config:
              robot_testsuite:
                - [robot file path 1]
                - [robot file path 2]
                - [robot file path n]

    可以向 robotframework 传递一个或多个选项。

    .. code-block:: yaml

        tests:
          robot.example:
            harness: robot
            harness_config:
              robot_testsuite: [robot file path]
              robot_option:
                - --exclude tag
                - --stop-on-error

filter: <表达式>
    通过评估表达式过滤测试场景是否应运行，表达式针对包含以下值的环境：

    .. code-block:: none

            { ARCH : <architecture>,
              PLATFORM : <platform>,
              <all CONFIG_* key/value pairs in the test's generated defconfig>,
              *<env>: any environment variable available
            }

    Twister 会先评估表达式，判断能否执行"受限"的 cmake 调用，
    即使用 package_helper cmake 脚本。

    存在 "dt_*" 条目表示需要设备树（devicetree）。
    不同可用 DT 表达式的详细描述参见 :ref:`twister_dt_filter_expressions`。

    存在 "CONFIG*" 条目表示需要 kconfig。
    如果表达式中没有其他类型的条目，可以在不创建完整构建系统的情况下
    完成过滤。如果存在其他类型的条目，则必须执行完整的 cmake。

    表达式语言的语法规则如下：

    .. code-block:: antlr

        expression : expression 'and' expression
                   | expression 'or' expression
                   | 'not' expression
                   | '(' expression ')'
                   | symbol '==' constant
                   | symbol '!=' constant
                   | symbol '<' NUMBER
                   | symbol '>' NUMBER
                   | symbol '>=' NUMBER
                   | symbol '<=' NUMBER
                   | symbol 'in' list
                   | symbol ':' STRING
                   | symbol
                   ;

        list : '[' list_contents ']';

        list_contents : constant (',' constant)*;

        constant : NUMBER | STRING;

    对于 ``expression ::= symbol`` 的情况，如果符号被定义为非空字符串，
    则求值为 ``true``。

    运算符优先级，从最低到最高：

       * or（左结合）
       * and（左结合）
       * not（右结合）
       * 所有比较运算符（非结合）

    ``arch_allow``、``arch_exclude``、``platform_allow``、``platform_exclude``
    都是这些表达式的语法糖。例如：

    .. code-block:: none

        arch_exclude = x86 arc

    等同于：

    .. code-block:: none

        filter = not ARCH in ["x86", "arc"]

    ``:`` 运算符将字符串参数编译为正则表达式，然后仅当符号在环境中的值
    匹配时返回 true 值。例如，如果 ``CONFIG_SOC="stm32f107xc"``，则：

    .. code-block:: none

        filter = CONFIG_SOC : "stm.*"

    会匹配它。

required_snippets: <所需片段列表>
    :ref:`片段（Snippets） <snippets>` 在需要它们的 Twister 测试场景中得到支持。
    与普通应用一样，Twister 支持使用基础 zephyr 片段目录和测试应用目录
    来查找片段。列出的片段会过滤支持的测试（片段必须与 board 兼容，
    测试才能在其上运行，它们不是可选的）。

    下面是一个包含 2 个所需片段的 yaml 文件示例。

    .. code-block:: yaml

        tests:
          snippet.example:
            required_snippets:
              - cdc-acm-console
              - user-snippet-example

.. _required_applications:

required_applications: <所需应用列表> (default empty)
    指定当前测试运行前必须构建的一组测试应用。
    它实现了测试场景之间已构建应用的共享，允许测试访问其他应用的构建产物。

    每个所需应用条目支持：

    - ``application``：测试场景标识符（必需）
    - ``name``：``application`` 的弃用别名（为向后兼容仍接受，
      但新配置中应使用 ``application``）
    - ``platform``：目标平台（可选，默认为当前测试的平台）
    - ``path``：Twister 应查找应用的目录路径（可选）。可以是绝对路径，
      也可以是相对于包含该测试 YAML 文件的目录的路径。环境变量和
      Zephyr 模块目录变量会被展开（参见 :ref:`twister_module_dir_vars`）。
      如果未指定，Twister 在与引用该测试的 YAML 文件相同的目录中查找。

    所需应用由 Twister 自动发现并构建。
    如果所需应用尚未加载，Twister 会在 ``path`` 指定的目录中查找它，
    或者如果未设置 ``path``，则在与引用该测试的 YAML 文件相同的目录中查找。
    当复用构建目录（例如使用 ``--no-clean``）时，
    Twister 可以在当前构建目录中找到所需应用。

    工作原理：

    - Twister 先构建所需应用
    - 主测试应用等待所需应用完成
    - 所需应用的构建目录可供测试框架使用
    - 对于 pytest 测试框架，构建目录通过 ``--required-build`` 参数传递，
      并可通过 ``required_build_dirs`` fixture 访问

    与 ``build: false`` 结合使用时，当前测试场景完全跳过自身的构建步骤，
    并使用第一个所需应用的构建产物作为其镜像。这对于纯粹作为
    在别处构建的镜像的测试框架的场景很有用。

    配置示例：

    .. code-block:: yaml

        tests:
          # Requires two applications, second one from a different path and with a fixed platform
          sample.required_app_demo:
            harness: pytest
            required_applications:
              - application: sample.shared_app
              - application: other.app
                path: ../other_app
                platform: native_sim
          # No self build, use the first required application as the test image
          sample.no_self_build:
            build: false
            harness: pytest
            required_applications:
              - application: sample.basic.helloworld
                path: $ZEPHYR_BASE/samples/hello_world
          sample.shared_app:
            build_only: true

    限制：

    - 不支持与 ``--runtime-artifact-cleanup`` 一起使用，因为所需应用的
      构建产物必须保留供主测试应用使用。
    - 不支持与 ``--subset`` 一起使用：所需应用和依赖它的测试
      可能被分配到不同的子集，导致测试执行时构建产物不可用。

build: <True|False> (default True)
    如果为 false，测试场景跳过自身的构建步骤，并使用
    ``required_applications`` 中第一个条目的构建产物作为其镜像。
    这对于纯粹作为由其他场景构建的镜像的测试框架的场景很有用。

    约束：

    - ``required_applications`` 必须非空。
    - 支持的测试框架：基于 pytest 的（例如 ``pytest``、``shell``）和 ``bsim``。
    - 不支持 QEMU 平台。

expect_reboot: <True|False> (default False)
    通知 Twister 该测试场景在运行期间预期会重启。
    启用后，Twister 会抑制关于测试套件或测试用例意外多次运行的警告。

modules: <模块名称列表>
    仅当工作区中存在所有列出的 :ref:`模块 <modules>` 时，
    才构建并运行该测试场景。需要不可用模块的场景会被过滤掉。

type: <字符串> (default integration)
    场景的测试类型。对于为 :ref:`unit_testing board <unit_testing_board>` 构建
    并在主机上运行（无需完整 Zephyr 构建系统）的单元测试，
    设置为 ``unit``。

testcases: <测试用例名称列表>
    显式声明构成该场景的测试用例名称列表。
    这通常自动检测（例如来自 ztest 源码），
    只需为无法内省（introspect）的测试框架设置。

ignore_faults: <True|False> (default False)
    如果测试运行期间在输出中检测到故障（fault），
    不要将该测试场景标记为失败。

ignore_qemu_crash: <True|False> (default False)
    如果测试运行期间 QEMU 崩溃，不要将该测试场景标记为失败。

实际运行的测试场景集合取决于测试场景文件中的指令和命令行传入的选项。
如果存在任何疑问，使用 ``-v`` 运行或检查 :ref:`测试计划 <twister_output>`
（:file:`testplan.json`）有助于显示为什么特定测试场景被过滤掉。

要从文件加载参数，在文件名前添加 ``+``，例如 ``+file_name``。
文件内容必须是一个或多个以换行符（而非空格）分隔的有效参数。

大多数日常用户不带任何参数运行。

.. _twister_module_dir_vars:

使用模块目录变量展开路径
===============================================

测试场景文件中的路径选项（例如 ``required_applications``、
``harness_config: pytest_root``）在使用前会被展开。除环境变量外，
Twister 还会展开 Zephyr 模块目录变量，它们镜像为每个模块定义的 CMake 变量：

* ``ZEPHYR_<MODULE>_MODULE_DIR`` - 模块根目录的绝对路径。
* ``ZEPHYR_<MODULE>_MODULE_NAME`` - 模块名称。

``<MODULE>`` 会被大写化，非字母数字字符替换为 ``_``，
与 CMake 的做法完全一致（例如 ``hal_nordic`` 模块对应
``$ZEPHYR_HAL_NORDIC_MODULE_DIR``）。未知引用保持原样。

管理测试超时
=====================

有多个参数在不同层级控制测试超时：

* 每个测试场景中的 ``timeout`` 选项。更多详情参见
  :ref:`此处 <twister_test_case_timeout>`。
* board 配置中的 ``timeout_multiplier`` 选项。
  更多详情参见 :ref:`此处 <twister_board_timeout_multiplier>`。
* ``--timeout-multiplier`` Twister 选项，可用于调整特定 Twister 运行中的超时时间。
  对于模拟平台可能很有用，因为模拟时间可能取决于主机速度 & 负载，
  或者我们可能选择不同的模拟方法（例如周期精确但更慢的方法）等。

测试场景的整体超时是这三个参数的乘积。

.. _twister_dt_filter_expressions:

设备树过滤表达式
================================

以 "dt_*" 开头的表达式用于在选择测试场景时基于特定设备树属性
（如 compatibles、aliases、节点标签、节点属性、chosen 节点等）
过滤 board。

.. note::

   这些表达式的源代码位于
   :zephyr_file:`scripts/pylib/twister/expr_parser.py`。

表达式
---------

``dt_compat_enabled(compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查具有指定 compatible 字符串（``compat``）的任意 DT 节点是否已启用。

**参数：**
   - ``compat``：要匹配的 compatible 字符串。

``dt_alias_exists(alias)``
~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查具有指定别名的任意 DT 节点是否存在且已启用。

**参数：**
   - ``alias``：要匹配的别名（定义在 ``aliases`` 节点中）。

``dt_enabled_alias_with_parent_compat(alias, compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查 DT 中是否存在一个已启用的别名节点，其父节点具有指定的 compatible 字符串。
   对于像 ``gpio-leds`` 子节点这类可能没有自身 compatible 的节点很有用。

**参数：**
   - ``alias``：要匹配的别名（定义在 ``aliases`` 节点中）。
   - ``compat``：要匹配的父节点 compatible 字符串。

``dt_label_with_parent_compat_enabled(label, compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查具有指定标签的 DT 节点是否存在、已启用，且其父节点具有
   指定的 compatible 字符串。

**参数：**
   - ``label``：要匹配的节点标签。
   - ``compat``：要匹配的父节点 compatible 字符串。

``dt_label_compat_enabled(label, compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查具有指定标签的 DT 节点是否存在、已启用，且具有
   指定的 compatible 字符串。

**参数：**
   - ``label``：要匹配的节点标签。
   - ``compat``：要匹配的节点 compatible 字符串。

``dt_chosen_enabled(chosen)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查具有指定名称的 DT chosen 属性是否存在，且分配给它的节点已启用。

**参数：**
   - ``chosen``：chosen 属性的名称。

``dt_nodelabel_enabled(label)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查具有指定标签的 DT 节点是否存在且已启用。

**参数：**
   - ``label``：要匹配的节点标签。

``dt_nodelabel_prop_enabled(label, prop)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查具有指定标签的 DT 节点是否存在、已启用，且具有指定属性
   且其值非空。

**参数：**
   - ``label``：要匹配的节点标签。
   - ``prop``：要检查的节点属性。

``dt_node_has_prop(node_id, prop)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**用途：**
   检查 DT 节点（通过别名或路径指定）是否具有指定属性，
   无论其状态如何。对于没有 status 的节点（如 ``zephyr,user`` 节点）很有用。

**参数：**
   - ``node_id``：要匹配的节点别名（定义在 ``aliases`` 节点中）或节点路径。
   - ``prop``：要检查的节点属性。

用法
-----

这些表达式用于 Twister 的测试场景过滤逻辑中，以选择匹配特定 DT 条件的 board。
例如：

.. code-block:: yaml

   tests:
     - test: my_test
       filter: dt_compat_enabled("my-compat-string")

测试场景 ``my_test`` 只会在具有 ``my-compat-string`` 的 DT 节点已启用的
board 上构建。

.. _twister_harnesses:

测试框架（Harnesses）
*********

*测试框架（harness）* 是 Twister 用于运行测试并判断其通过或失败的机制。
在测试镜像构建并在其目标（真实硬件、模拟器或主机）上启动后，
测试框架驱动与运行中镜像的交互——提供输入、捕获输出，或将执行权
交给外部测试运行器——并解释结果以为每个测试用例分配
:ref:`状态 <twister_statuses>`。

测试场景通过其 ``tests.yaml`` 中的 ``harness:`` 条目选择测试框架，
并通过 ``harness_config`` 调整其行为。未指定测试框架时，
使用默认的 ``test`` 测试框架。不同测试框架服务于不同需求：
有些将设备控制台输出与预期模式进行匹配解析，
而有些则将执行委托给外部框架，例如 pytest、Robot Framework 或 ctest。
下面链接的页面描述每个支持的测试框架及其 ``harness_config`` 选项。

``ztest``、``gtest`` 和 ``console`` 测试框架基于解析输出并匹配特定短语。
``ztest`` 和 ``gtest`` 测试框架查找这些框架中定义的通过/失败/其他帧。

一些广泛使用但尚不支持的测试框架：

- keyboard
- net
- bluetooth

下面是一个包含几个 harness_config 选项的 yaml 文件示例。

.. code-block:: yaml

      sample:
        name: HTS221 Temperature and Humidity Monitor
      common:
        tags:
          - sensor
        harness: console
        harness_config:
          type: multi_line
          ordered: false
          regex:
            - "Temperature:(.*)C"
            - "Relative Humidity:(.*)%"
          fixture: i2c_hts221
      tests:
        test:
          tags:
            - sensors
          depends_on: i2c

.. toctree::
   :maxdepth: 1

   harness/ctest
   harness/gtest
   harness/pytest
   harness/console
   harness/robot
   harness/power
   harness/display_capture
   harness/script
   harness/bsim
   harness/shell


.. _twister_sidecars:

Sidecars（伴随进程）
********

有些测试需要在一次运行期间存在一个主机端资源：
与模拟来宾（guest）通信的守护进程、主机稍后读回的共享内存区域，
或来宾附加的网络接口。*sidecar（伴随进程）* 对这一模式建模。
它通过测试场景 :file:`tests.yaml` 中的 ``sidecar:`` 条目选择，
与测试框架正交：测试框架解释来宾的输出，
而 sidecar 在运行周围配置主机端。
因此，任何测试框架（示例用 ``console``、测试用 ``ztest`` 等）
都可以与任何 sidecar 配对。

.. code-block:: yaml

   tests:
     some.test:
       harness: ztest
       sidecar: <name>

sidecar 有一个简短的生命周期，由 Twister 为每个测试实例驱动：

#. **configure（配置）** -- 在任何资源被配置之前，sidecar 从实例及其
   ``sidecar_config`` 块中读取所需内容。
#. **host check（主机检查）** -- 在测试计划阶段，sidecar 报告主机
   是否提供了所需条件（例如，所需守护进程二进制文件已安装）。
   如果没有，测试*仅构建*而不执行，
   与模拟器未安装的平台完全相同。
#. **setup（设置）** -- 在处理器运行测试镜像之前调用；
   它启动主机资源（启动守护进程、创建接口等）。
   如果主机端仍不可用——例如启动资源需要当前不存在的权限——
   setup 会报告这一点，Twister *跳过*执行而非使测试失败。
#. **teardown（拆除）** -- 在处理器返回后调用，位于 ``finally`` 块中，
   因此即使测试失败或超时它也总会运行。它释放资源，
   也可以收集来宾留下的数据（例如将共享内存区域读回构建目录）。

由于资源配置与输出处理解耦，Twister 还可以将 sidecar 附加到实例本身，
无需测试主动选择——例如将覆盖率数据从没有其他主机传输通道的来宾路由出去。

每个 sidecar 在其以 sidecar 命名的 ``sidecar_config`` 块下定义自己的配置键。
按 sidecar 名称命名空间使每个 sidecar 的键相互隔离，
因此只有与场景 ``sidecar:`` 值匹配的被消费。例如，``virtiofs`` sidecar
通过以下方式共享一个从模板播种的主机目录：

.. code-block:: yaml

   tests:
     some.test:
       harness: console
       sidecar: virtiofs
       sidecar_config:
         virtiofs:
           shared: shared


选择平台范围
************************

Twister 的关键特性之一是能够决定给定测试场景应在哪些平台上运行。
这一行为源于 Twister 作为 Zephyr CI 的测试运行器开发而来。
面对数百个可用平台和数千个测试，测试工具应能调整范围，
选择/过滤掉相关与不相关的内容。

Twister 总是基于命令行参数和 :ref:`测试配置 <test_config_args>`
为给定测试准备一个初始平台范围列表。然后，不满足配置 yaml 中
所需条件（例如最小 RAM）的平台会从范围中过滤掉。
使用 ``--force-platform`` 可以覆盖由测试配置文件中
``platform_allow``、``platform_exclude``、``arch_allow`` 和
``arch_exclude`` 键引起的过滤。

命令行参数按以下方式定义初始范围：

* ``-p/--platform <platform_name>``（可多次使用）：仅使用该参数传入的平台；
* ``-l/--all``：所有可用平台；
* ``-G/--integration``：给定测试配置文件中 ``integration_platforms``
  列表中的所有平台。如果测试没有 ``integration_platforms``，
  将发生*"范围推定（scope presumption）"*；
* 无范围参数：将发生*"范围推定"*。

*"范围推定"*：使用 Twister :ref:`默认平台 <twister_default_testing_board>`
列表作为初始列表。如果过滤后没有任何剩余，
则使用 ``platform_allow`` 列表作为初始范围。

以集成模式运行
***************************

此模式用于持续集成（CI）和其他用于向开发人员提供更改快速反馈的
自动化环境。该模式可通过 Twister 的 ``--integration`` 选项激活，
如适用，将构建和测试范围缩小到测试配置文件（``tests.yaml``）中
integration 关键字下定义的平台。


在自定义模拟器上运行测试
********************************

除已支持的 QEMU 和其他模拟环境外，Twister 还支持运行任何在
board 的 :file:`board.cmake` 中定义的树外（out-of-tree）自定义模拟器。
要使用这种类型的模拟，向 :file:`custom_board/custom_board.yaml`
添加以下属性：

.. code-block:: yaml

   simulation:
     - name: custom
       exec: <name_of_emu_binary>

这告诉 Twister 该 board 使用名为 ``<name_of_emu_binary>`` 的自定义模拟器，
请确保该二进制文件存在于 PATH 中。

然后，在 :file:`custom_board/board.cmake` 中，将支持的模拟平台设置为 ``custom``：

.. code-block:: cmake

   set(SUPPORTED_EMU_PLATFORMS custom)

最后，在 :file:`custom_board/board.cmake` 中实现 ``run_custom`` 目标。
它应该类似于这样：

.. code-block:: cmake

   add_custom_target(run_custom
     COMMAND
     <name_of_emu_binary to invoke during 'run'>
     <any args to be passed to the command, i.e. ${BOARD}, ${APPLICATION_BINARY_DIR}/zephyr/zephyr.elf>
     WORKING_DIRECTORY ${APPLICATION_BINARY_DIR}
     DEPENDS ${logical_target_for_zephyr_elf}
     USES_TERMINAL
     )


以随机顺序运行测试
*****************************
启用 ZTEST 框架的 :kconfig:option:`CONFIG_ZTEST_SHUFFLE` 配置选项，
即可按随机顺序运行测试。这有助于识别测试用例之间的依赖关系。
对于 native_sim 平台，可以通过向 Twister 提供 ``--seed=value`` 参数
为随机数生成器提供种子。更多详情参见
:ref:`打乱测试顺序 <ztest_shuffle>`。


在硬件上运行测试
*************************

除能在 QEMU 和其他模拟环境中运行测试外，
Twister 还支持在真实设备上运行大多数测试，并为每次运行生成报告，
包含详细的 FAIL/PASS 结果。


在单个设备上执行测试
==================================

要在单个已连接设备上使用此功能，使用以下新选项运行 Twister：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

 	      west twister --device-testing --device-serial /dev/ttyACM0 \
 	      --device-serial-baud 115200 -p frdm_k64f  -T tests/kernel

   .. group-tab:: Windows

      .. code-block:: bat

 	      west twister --device-testing --device-serial COM1 \
 	      --device-serial-baud 115200 -p frdm_k64f  -T tests/kernel

``--device-serial`` 选项表示 board 连接的串行设备。
运行 Twister 的用户需要能访问它。每次只能在一个 board 上运行，
通过 ``--platform`` 选项指定。如果平台支持多个串口，
可以多次提供 ``--device-serial``，它会被传递给 pytest 测试框架。
或者你可以使用硬件映射，更多详情参见
:ref:`多核测试 <twister_multi_core_testing>`。

``--device-serial-baud`` 选项仅在你的设备不以 115200 波特率运行时才需要。

要支持没有物理串口的设备，使用 ``--device-serial-pty`` 选项。
在此情况下，日志消息例如通过脚本捕获。此时你可以用以下选项运行 Twister：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west twister --device-testing --device-serial-pty "script.py" \
         -p intel_adsp/cavs25 -T tests/kernel

   .. group-tab:: Windows

      .. note::

         Not supported on Windows OS

该脚本由用户定义，负责传递 Twister 可用于判断测试执行状态的消息。

``--device-flash-timeout`` 选项允许为设备烧录操作设置显式超时，
例如当设备烧录耗时显著较长时。

``--device-flash-with-test`` 选项表示在该平台上烧录操作
也会执行一个测试场景，因此烧录超时会增加一个测试场景超时。

在多个设备上执行测试
===================================

要在连接到主机 PC 的多个设备上构建并执行测试，
需要创建一个硬件映射（hardware map），包含所有已连接设备及其
详细信息，如串行设备、波特率及其 ID（如果可用）。
运行以下命令生成硬件映射：

.. code-block:: console

   $ west twister --generate-hardware-map map.yml

生成的硬件映射文件（map.yml）将包含已连接设备列表，例如：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: unknown
           product: DAPLink CMSIS-DAP
           runner: pyocd
           serial: /dev/cu.usbmodem146114202
         - connected: true
           id: "000683759358"
           platform: unknown
           product: J-Link
           runner: unknown
           serial: /dev/cu.usbmodem0006837593581

   .. group-tab:: Windows

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: unknown
           product: unknown
           runner: unknown
           serial: COM1
         - connected: true
           id: "000683759358"
           platform: unknown
           product: unknown
           runner: unknown
           serial: COM2


任何标记为 ``unknown`` 的选项都需要修改并设置为正确值。
在上面的示例中，平台名称、产品和 runner 需要替换为
与已连接硬件对应的正确值。在此示例中我们使用一个 reel_board
和一个 nrf52840dk/nrf52840：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: reel_board
           product: DAPLink CMSIS-DAP
           runner: pyocd
           serial: /dev/cu.usbmodem146114202
           baud: 9600
         - connected: true
           id: "000683759358"
           platform: nrf52840dk/nrf52840
           product: J-Link
           runner: nrfjprog
           serial: /dev/cu.usbmodem0006837593581
           baud: 9600

   .. group-tab:: Windows

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: reel_board
           product: DAPLink CMSIS-DAP
           runner: pyocd
           serial: COM1
           baud: 9600
         - connected: true
           id: "000683759358"
           platform: nrf52840dk/nrf52840
           product: J-Link
           runner: nrfjprog
           serial: COM2
           baud: 9600

baud 条目仅在不以 115200 波特率运行时才需要。

如果映射文件已存在，则添加新条目并更新现有条目。
这样你可以使用一个单一的主硬件映射，并在每次运行时更新它，
以获取正确的串行设备和设备状态。

硬件映射就绪后，可以通过指向该映射运行任何测试：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west twister --device-testing --hardware-map map.yml -T samples/hello_world/

   .. group-tab:: Windows

      .. code-block:: bat

         west twister --device-testing --hardware-map map.yml -T samples\hello_world

上述命令将使 Twister 为硬件映射中定义的平台构建测试，
随后在这些平台上烧录并运行测试。

.. note::

  目前只有支持 pyocd、nrfjprog、jlink、openocd 或 dediprog 的 board
  才支持硬件映射特性。需要其他 runner 烧录 Zephyr 二进制的 board
  仍在开发中。

硬件映射允许将 ``--device-flash-timeout`` 和 ``--device-flash-with-test``
命令行选项分别设置为 ``flash-timeout`` 和 ``flash-with-test`` 字段。
这些硬件映射值会覆盖特定平台的命令行选项。

``--device-serial-pty`` 提供的串行 PTY 支持也可以用于硬件映射：

.. code-block:: yaml

   - connected: true
     id: None
     platform: intel_adsp/cavs25
     product: None
     runner: intel_adsp
     serial_pty: path/to/script.py
     runner_params:
       - --remote-host=remote_host_ip_addr
       - --key=/path/to/key.pem


runner_params 字段表示你想传递给 west runner 的参数。
对于某些 board，west runner 需要一些额外参数才能工作。
它等价于以下 west 和 Twister 命令。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west flash --remote-host remote_host_ip_addr --key /path/to/key.pem

         west twister -p intel_adsp/cavs25 --device-testing --device-serial-pty script.py
         --west-flash="--remote-host=remote_host_ip_addr,--key=/path/to/key.pem"

   .. group-tab:: Windows

      .. note::

         Not supported on Windows OS

.. note::

  对于串行 PTY，"--generate-hardware-map" 选项无法扫描它并
  自动生成正确的硬件映射。你不得不根据上面的示例手动编辑它。
  这是因为 PTY 的串口不固定，在运行时由系统分配。

如果 west 不可用或不知道如何烧录你的系统，
可以使用 ``flash-command`` 标志指定自定义烧录命令。
该脚本以 ``--build-dir``（当前构建的路径）以及
``--board-id`` 标志（在硬件映射中有多个设备时用于标识特定设备）调用。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west twister -p npcx9m6f_evb --device-testing --device-serial /dev/ttyACM0
         --flash-command './custom_flash_script.py,--flag,"complex, argument"'

   .. group-tab:: Windows

      .. note::

         west twister -p npcx9m6f_evb --device-testing
         --device-serial COM1
         --flash-command 'custom_flash_script.py,--flag,"complex, argument"'

结果将调用 ``./custom_flash_script.py
--build-dir <build directory> --board-id <board identification>
--flag "complex, argument"``。

.. _twister_fixtures:

Fixtures（夹具）
--------

有些测试需要额外的设置或特定于测试的特殊接线。
没有此设置或测试夹具（fixture）运行测试可能会失败。
测试场景可以指定其所需的 fixture，然后可以通过命令行
或使用硬件映射文件将其与 board 的硬件能力及其支持的 fixture 匹配。

fixture 在硬件映射文件中定义为列表：

.. code-block:: yaml

      - connected: true
        fixtures:
          - gpio_loopback
        id: "0240000026334e450015400f5e0e000b4eb1000097969900"
        platform: frdm_k64f
        product: DAPLink CMSIS-DAP
        runner: pyocd
        serial: /dev/ttyACM9

使用 ``--device-testing`` 运行 ``twister`` 时，硬件映射文件中
配置的 fixture 将与请求相同 fixture 的测试场景匹配，
这些测试将在提供该 fixture 的 board 上执行。

要为依赖 fixture 的测试保留一个 board，将 ``run_with_fixture_only``
设置为 ``true``。Twister 只为请求匹配 fixture 的测试场景选择该 board；
它不会为没有 fixture 需求的场景选择该 board。

.. code-block:: yaml

      - connected: true
        fixtures:
          - gpio_loopback
        run_with_fixture_only: true
        id: 0240000026334e450015400f5e0e000b4eb1000097969900
        platform: frdm_k64f

.. figure:: figures/fixtures.svg
   :figclass: align-center

fixture 也可以通过 Twister 命令选项 ``--fixture`` 提供，
该选项可多次使用，所有给定的 fixture 会作为列表追加。
给定的 fixture 会被分配给所有 board，这意味着当前 Twister 命令
设置的所有 board 都可以运行请求相同 fixture 的测试场景。

某些 fixture 允许追加配置字符串，与 fixture 名称之间用 ``:`` 分隔。
只有 fixture 名称会与测试场景请求的 fixture 匹配。

Notes（备注）
-----

在硬件映射文件中为 board 描述添加额外信息可能很有用。
使用 ``notes`` 关键字来实现。例如：

.. code-block:: yaml

    - connected: false
      fixtures:
        - gpio_loopback
      id: "000683290670"
      notes: An nrf5340dk/nrf5340 is detected as an nrf52840dk/nrf52840 with no serial
        port, and three serial ports with an unknown platform.  The board id of the serial
        ports is not the same as the board id of the development kit.  If you regenerate
        this file you will need to update serial to reference the third port, and platform
        to nrf5340dk/nrf5340/cpuapp or another supported board target.
      platform: nrf52840dk/nrf52840
      product: J-Link
      runner: jlink
      serial: null

覆盖 board 标识符
---------------------------

（重新）生成硬件映射文件时，其中将包含一个 ``id`` 关键字，
作为烧录时 ``--board-id`` 的参数。在某些情况下，检测到的 ID
不是应使用的正确 ID，例如使用外部 J-Link 探针时。
``probe_id`` 关键字为此目的覆盖 ``id`` 关键字。例如：

.. code-block:: yaml

    - connected: false
      id: "0229000005d9ebc600000000000000000000000097969905"
      platform: mimxrt1060_evk
      probe_id: "000609301751"
      product: DAPLink CMSIS-DAP
      runner: jlink
      serial: null

使用单个 board 支持多个变体
----------------------------------------

  ``platform`` 属性可以是名称列表，或名称之间以空格分隔的字符串。
  这允许在同一物理 board 上为不同平台变体运行测试，
  而无需为每个变体重新配置硬件映射文件。例如：

.. code-block:: yaml

    - connected: true
      id: "001234567890"
      platform:
      - nrf5340dk/nrf5340/cpuapp
      - nrf5340dk/nrf5340/cpuapp/ns
      product: J-Link
      runner: nrfjprog
      serial: /dev/ttyACM1

.. _twister_multi_core_testing:

多核测试支持
--------------------------

Twister 支持测试多核应用，其中不同核心使用独立的 UART 接口。
此功能仅与 pytest 测试框架（``harness: pytest``）配合工作。
生成的硬件映射应为同一物理设备包含多个条目，
每个条目代表一个不同的核心连接。例如：

.. code-block:: yaml

    - connected: true
      id: "001234567890"
      serial: /dev/ttyACM0
    - connected: true
      id: "001234567890"
      platform:
      - nrf54l15dk/nrf54l15/cpuapp
      product: J-Link
      runner: nrfutil
      serial: /dev/ttyACM1

两个实例共享相同的设备 ID，但具有不同的串口，
允许测试同时与多个核心交互。每个连接独立处理，
使用独立的日志文件。

.. _twister_multi_duts_testing:

多 DUT 测试支持
--------------------------

Twister 支持需要多个设备的测试场景。
此功能仅与 pytest 测试框架（``harness: pytest``）配合工作。
支持硬件和 ``native_sim`` 执行环境。

要声明测试需要额外设备，在测试 YAML 文件的
``harness_config`` 下添加 ``required_devices``。
列表中的每个条目描述一个额外 DUT。空条目 ``{}``
保留一个与主 DUT 具有相同平台和应用的第二设备。
所有可用选项参见 :ref:`required_devices <required_devices>`。

测试配置示例：

.. code-block:: yaml

    tests:
      multidut.basic:
        harness: pytest
        harness_config:
          required_devices:
            - {}

硬件映射必须为每个所需设备至少包含一个条目。
每个条目需要一个匹配的平台和一个串行连接：

.. code-block:: yaml

    - connected: true
      id: "01"
      platform: nrf52840dk/nrf52840
      serial: /dev/ttyACM0
    - connected: true
      id: "02"
      platform: nrf52840dk/nrf52840
      serial: /dev/ttyACM1

在硬件上运行测试：

.. code-block:: console

    $ west twister -vv -ll debug -T tests/subsys/testsuite/multidut \
      --device-testing --hardware-map map.yaml

在 ``native_sim`` 上运行测试（无需硬件映射）：

.. code-block:: console

    $ west twister -vv -ll debug -T tests/subsys/testsuite/multidut -p native_sim

Twister 保留所有所需设备（如果使用 ``native_sim`` 则创建占位条目），
然后将它们连同所有必要信息（平台、串行连接、待烧录的构建产物等）
传递给 pytest，使测试可以与所有设备交互。

多 DUT 测试示例位于
:zephyr_file:`tests/subsys/testsuite/multidut`。

Quarantine（隔离区）
------------

Twister 允许用户提供配置文件，定义要放入隔离区的测试或平台列表。
此类测试将被跳过，并在输出报告中相应标记。
此功能在运行较大测试套件时特别有用，
其中一个测试的失败可能影响其他测试的执行
（例如将物理 board 置于损坏状态）。

要使用隔离区功能，需要在 Twister 调用中添加参数
``--quarantine-list <PATH_TO_QUARANTINE_YAML>``。
可以使用多个隔离区文件。
还可以通过在上述参数中添加 ``--quarantine-verify``
验证隔离区列表上测试的当前状态。这会使 Twister 跳过
不在给定列表上的所有测试。

隔离区 yaml 是一组字典序列。每个字典必须至少包含
以下键之一：``scenarios``、``platforms``、``architectures``
或 ``simulations``。允许这些条目的组合。
可选的 ``comment`` 条目可用于提供更多细节
（例如指向已报告问题的链接）。这些注释也会
被添加到输出报告中。

当隔离一类测试或单个测试套件中的多个场景，
或在子系统内处理多个问题时，可以使用正则表达式，
例如 **kernel.*** 将隔离所有内核测试。

隔离区 yaml 条目示例：

.. code-block:: yaml

    - scenarios:
        - sample.basic.helloworld
      comment: "Link to the issue: https://github.com/zephyrproject-rtos/zephyr/pull/33287"

    - scenarios:
        - kernel.common
        - kernel.common.(misra|tls)
        - kernel.common.nano64
      platforms:
        - .*_cortex_.*
        - native_sim

    - platforms:
        - qemu_x86
      comment: "filter out qemu_x86"

    - architectures:
        - riscv

    - simulations:
        - armfvp

.. _twister_output:

测试输出与报告
***********************

默认情况下，Twister 将所有输出写入在当前工作目录中创建的
:file:`twister-out` 目录。使用 ``-O``/``--outdir`` 选择其他位置。
每次运行时该目录会被清理，除非给出 ``--no-clean``；
``--clobber-output`` 控制清理的具体行为。

顶层报告
=================

以下文件写入输出目录的根目录：

:file:`twister.json`
    主要的机器可读报告。它包含每个所选测试套件和测试用例的条目，
    包括其 :ref:`状态 <twister_statuses>`、目标平台、执行时间、
    内存占用、任何 :ref:`记录的数据 <twister_console_harness>`，
    以及运行所用的环境和选项。

:file:`testplan.json`
    解析后的测试计划：Twister 考虑的每个测试实例
    （测试场景 × 平台），包括被过滤掉的及其原因。
    这是用于理解给定场景为何运行或未运行的文件。
    可以配合 ``--load-tests`` 重用以重放相同的选择。

:file:`twister.xml`
    适用于 CI 系统的 JUnit XML 摘要。

:file:`twister_report.xml`
    包含所有测试用例（不仅是摘要）的 JUnit XML 报告。

:file:`twister_suite_report.xml`
    按测试套件分组的 JUnit XML 报告。

:file:`twister.log`
    整个运行的人类可读日志。

:file:`twister_footprint.json`
    ROM/RAM 占用报告。仅在使用 ``--footprint-report`` 时生成。

报告基名（``twister``）可以用 ``--report-name`` 更改，
``--report-suffix`` 为所有生成的文件名追加后缀
（例如版本号或 commit ID）。使用 ``-o``/``--report-dir``
将报告写入输出目录以外的目录，使用 ``--platform-reports``
额外输出按平台的 :file:`<platform>.json` 和 :file:`<platform>.xml`。
``--report-summary`` 在不重新构建的情况下打印最近一次运行的失败摘要。

按测试的产物
==================

每个测试实例在输出目录下有自己的构建目录，
以平台和测试命名：
:file:`twister-out/<platform>/<test path>/<scenario>/`。
除常规 Zephyr 构建产物（例如 :file:`zephyr/zephyr.elf`）外，
可能还包含：

:file:`build.log`
    该实例构建的输出。

:file:`handler.log`
    运行测试时从设备或模拟器捕获的控制台输出。

:file:`twister_harness.log`
    基于 pytest 的测试框架（例如 ``pytest`` 和 ``shell``）生成的日志。

:file:`recording.csv`
    配置了 :ref:`console 测试框架 <twister_console_harness>`
    的 ``record`` 选项捕获的数据字段。

.. _twister_console_monitor:

实时运行监控
*******************

对于长时间运行，从滚动的控制台输出很难判断 Twister 实际在做什么：
哪些已排队、每个作业当前在构建或运行什么、哪些测试已经失败及原因。
``--console-monitor`` 选项在运行期间用终端中的实时全屏仪表盘
替换常规输出：

.. code-block:: console

   $ west twister -T tests/kernel --console-monitor

仪表盘显示总体进度（含通过/失败/错误/过滤分解）和预计完成时间、
当前*进行中*的测试实例集及其各自所处的流水线阶段（``cmake``、
``build``、``run`` 等），以及计划中所有测试实例（含静态过滤的）
的可滚动表格。与此同时，常规日志输出写入 :file:`twister.log`。

导航：:kbd:`Tab` 循环切换表格过滤器
（all/active/failures/passed/queued/filtered），:kbd:`f` 直接跳转到
失败视图，:kbd:`/` 对实例名称和失败原因启动增量文本搜索
（:kbd:`Esc` 清除）。用方向键或 :kbd:`j`/:kbd:`k` 移动选择，
按 :kbd:`Enter` 打开某实例的详情视图：其流水线阶段时间线、
失败测试用例列表及其原因、其日志文件尾部
（:kbd:`l` 在可用日志间切换，:kbd:`j`/:kbd:`k` 或方向键滚动，
:kbd:`g`/:kbd:`G` 跳转到顶部/底部，视图在固定于底部时跟随新输出）
——在其余运行继续时检查失败尤其有用。

运行结束时仪表盘保持显示，以便检查失败；
按 :kbd:`q` 离开，之后报告被写入，Twister 按常规退出。
运行仍在进行时按 :kbd:`q` 会提前离开仪表盘并恢复常规控制台输出。
该选项需要交互式终端，否则被忽略（例如在 CI 中）。

监控器观察运行而不影响它：监控事件尽力交付，
宁可丢弃也绝不延迟构建/运行流水线。

.. _twister_test_config:

Twister 配置文件
**************************

Twister 配置文件（``test_config.yaml``，通过 ``--test-config`` 传入）
可用于自定义 Twister 的各个方面以及默认启用的选项和特性。
这允许根据环境调整过滤能力，并在针对不同平台集时
便于调整和改进覆盖范围。

.. note::

   此文件（通过 ``--test-config`` 选择）配置整个 Twister 运行。
   它与 ``tests.yaml`` 中按应用的测试配置不同，
   后者描述单个 :ref:`测试场景 <twister_tests_long_version>`。

Twister 配置文件还为测试级别（test levels）提供支持，并能够
将特定测试分配到一个或多个级别。然后使用 Twister 的命令行选项
可以选择某个级别并只执行包含在该级别中的测试。

此外，配置文件允许定义级别依赖关系，并在测试本身
尚未具有此信息时额外将测试包含到特定级别中。

在配置文件中，你可以使用正则表达式包含完整组件，
并指定从同一文件导入哪个测试级别，使级别管理更简单。

为帮助在上游 CI 基础设施之外进行测试，
配置文件中提供额外选项，可托管在本地。目前可用的选项有：

- 忽略 board 定义中定义的默认平台的能力
  （这些主要是用于在上游 CI 中运行测试的模拟平台）
- 指定你自己的默认平台列表以覆盖上游定义的选项。
- 覆盖某些测试场景中使用的 ``build_on_all`` 选项的能力。
  这将把测试或示例当作其他普通测试一样处理，
  仅为你在配置文件或命令行中指定的默认平台构建。
- 忽略 Twister 中在某些默认平台不在范围内时扩展平台覆盖的逻辑。


平台配置
=====================

以下选项控制 Twister 中的平台过滤：

- ``override_default_platforms``：覆盖平台在 board 配置中设置的
  default 键，改为使用配置文件中提供的平台列表作为默认平台列表。
  该选项默认为 False。
- ``increased_platform_scope``：该选项默认为 True，
  禁用后，Twister 不会自动增加平台覆盖，
  只会在指定平台上构建和运行测试。
- ``default_platforms``：要添加的额外默认平台列表。
  该列表可用于替换现有默认平台或扩展它，
  取决于 ``override_default_platforms`` 的值。
- ``build_toolchains``：从平台名称到工具链列表的映射，
  分配给该平台的每个测试都应使用列表中的工具链构建。
  Twister 为每个工具链创建一个测试实例，每个位于自己的构建目录中。
  这设置或覆盖 board 定义中的 ``build_toolchains`` 选项；
  空列表禁用请求多工具链构建的平台的此类构建。
  由于这会使构建时间成倍增加，通常只在 CI 使用的配置文件中启用
  （``tests/test_config_ci.yaml``），使本地运行保持每个测试只构建一次。
  参见 :ref:`twister_toolchain_selection`。

平台配置示例：

.. code-block:: yaml

	platforms:
	  override_default_platforms: true
	  increased_platform_scope: false
	  default_platforms:
	    - qemu_x86
	  build_toolchains:
	    native_sim:
	      - host/gnu
	      - host/llvm


测试级别配置
========================

测试配置允许定义测试级别、级别依赖关系，
并在测试本身尚未具有此信息时额外将测试包含到特定测试级别中。

在配置文件中，你可以使用正则表达式包含完整组件，
并指定从同一文件导入哪个测试级别，使级别管理简单化。

测试级别配置示例：

.. code-block:: yaml

	levels:
	  - name: my-test-level
	    description: >
	      my custom test level
	    adds:
	      - kernel.threads.*
	      - kernel.timer.behavior
	      - arch.interrupt
	      - boards.*


组合配置
=====================

要混合平台配置和级别配置，可以参照以下示例：

平台加级别配置示例：

.. code-block:: yaml

	platforms:
	  override_default_platforms: true
	  default_platforms:
	    - frdm_k64f
	levels:
	  - name: smoke
	    description: >
	        A plan to be used verifying basic zephyr features.
	  - name: unit
	    description: >
	        A plan to be used verifying unit test.
	  - name: integration
	    description: >
	        A plan to be used verifying integration.
	  - name: acceptance
	    description: >
	        A plan to be used verifying acceptance.
	  - name: system
	    description: >
	        A plan to be used verifying system.
	  - name: regression
	    description: >
	        A plan to be used verifying regression.


要使用上述 test_config.yaml 文件运行，
只有给定测试级别的 default_platforms 上的测试场景会运行。

.. code-block:: console

   $ west twister --test-config=<path to>/test_config.yaml -T tests --level="smoke"
