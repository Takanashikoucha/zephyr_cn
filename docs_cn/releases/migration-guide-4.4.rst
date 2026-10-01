:orphan:

..
  参见
  https://docs.zephyrproject.org/latest/releases/index.html#migration-guides
  了解本文档应包含的内容。

.. _migration_4.4:

Zephyr v4.4.0 迁移指南
######################

本文档描述了将应用从 Zephyr v4.3.0 迁移到 Zephyr v4.4.0 所需的更改。

其他更改（与迁移应用无直接关系）可在 :ref:`发布说明<zephyr_4.4>` 中查看。

.. contents::
    :local:
    :depth: 2

通用
******

* 现在所需的最低 Zephyr SDK 版本为 1.0.0。
* 现在所需的最低 Python 版本为 3.12（从 3.10 起）。

构建系统
************

* Zephyr 现在官方默认以 C17（ISO/IEC 9899:2018）作为其最低必需的 C 标准版本。
  如果你的工具链不支持该标准，你需要使用现有的现已弃用的选项之一：
  :kconfig:option:`CONFIG_STD_C99` 或 :kconfig:option:`CONFIG_STD_C11`。
* ``board``/``boards`` 条目中对应新开发板的 ``full_name`` 属性在 board.yml 文件中现在为必需。
* CMake 变量 ``BOARD_QUALIFIERS`` 已与对应的 :kconfig:option:`CONFIG_BOARD_QUALIFIERS` 对齐，
  不再以 ``/`` 为前缀。
  这意味着 ``${BOARD}${BOARD_QUALIFIERS}`` 的任何使用必须更新为包含 ``/``，
  如下所示：``${BOARD}/${BOARD_QUALIFIERS}``。
* ``SNIPPET_ROOT`` 已与其他 Zephyr ``<type>_ROOT`` 设置对齐，默认不包含应用源目录。
  需要在 ``SNIPPET_ROOT`` 中添加应用源目录的示例必须改用 :file:`zephyr/module.yml` 中的
  ``snippet_root = <dir>`` 条目添加应用源目录，
  或手动将文件夹追加到 CMake 变量 ``SNIPPET_ROOT``。
* Shell 自动补全（``west completion``）应重新生成，
  因为开发板目标自动补全现在支持开发板修订版本。

内核
******

* 堆强化（heap hardening）支持已通过添加构建时生成的 ``zephyr/heap_constants.h`` 文件实现，
  该文件现在从 ``kernel.h`` 包含。
  这可能为作为 cmake 库构建的下游应用创建构建竞态条件，
  cmake 可能尝试在头文件生成前构建它们，
  这些可能需要额外的 ``add_dependencies(${lib} zephyr_generated_headers)`` cmake 条目，
  更多细节参见 :github:`106439`。

* ``__pinned_*`` 属性族和
  ``CONFIG_LINKER_USE_PINNED_SECTION`` /
  ``CONFIG_LINKER_GENERIC_SECTIONS_PRESENT_AT_BOOT`` Kconfig 选项已移除（:github:`108773`）。
  内核映像现在始终驻留在物理内存中；
  按需分页仅适用于通过 :c:func:`k_mem_map` 创建的匿名映射
  和通过 :kconfig:option:`CONFIG_LINKER_USE_ONDEMAND_SECTION`
  放置在 ``__ondemand_*`` 链接器段中的符号。

  之前"默认可逐出"的模型，
  其中任何未显式标记为 ``__pinned_*`` 的内核页都可被逐出，
  从结构上从未是安全的：
  给定构建能否存活取决于代码和数据相对于页错误分发路径的意外放置，
  而非任何保证。
  如果你有依赖旧模型且在现有版本上正常工作的应用，
  推荐路径是保持在该版本上，
  理想情况下是 :ref:`长期支持 <release_process_lts>` 版本，
  而非升级。
  迁移到较晚版本很可能改变布局足够多
  （添加代码、重排函数、新编译器）
  使未标记页位于错误分发路径上
  并以难以诊断的方式破坏系统。
  该潜在脆弱性正是该模式被移除而非延续的原因。
  确实升级的应用需要以下更新：

  * 从开发板 defconfig 和 prj.conf 覆盖文件中删除任何
    ``CONFIG_LINKER_USE_PINNED_SECTION=y`` 或
    ``CONFIG_LINKER_GENERIC_SECTIONS_PRESENT_AT_BOOT=n`` 行。

  * 从源代码中删除 ``__pinned_func``、``__pinned_data``、``__pinned_rodata``、
    ``__pinned_bss`` 和 ``__pinned_noinit`` 属性。
    需要按需分页的代码必须改用 ``__ondemand_func`` / ``__ondemand_rodata``；
    贡献者有责任确保此类符号不会从页错误处理器的执行路径到达。

  * 将汇编中 ``PINNED_TEXT``、``PINNED_RODATA``、``PINNED_DATA``、
    ``PINNED_BSS`` 和 ``PINNED_NOINIT`` 的使用
    （作为 ``SECTION_FUNC()`` / ``SECTION_VAR()`` 的段名参数）
    替换为普通的 ``TEXT``、``RODATA``、``DATA``、``BSS`` 和 ``NOINIT`` 别名。

  * 将 ``K_KERNEL_PINNED_STACK_DEFINE``、
    ``K_KERNEL_PINNED_STACK_ARRAY_DEFINE``、
    ``K_KERNEL_PINNED_STACK_ARRAY_DECLARE``、
    ``K_THREAD_PINNED_STACK_DEFINE`` 和
    ``K_THREAD_PINNED_STACK_ARRAY_DEFINE`` 的使用
    重命名为其非 pinned 对应项
    （``K_KERNEL_STACK_DEFINE``、
    ``K_KERNEL_STACK_ARRAY_DEFINE``、``K_KERNEL_STACK_ARRAY_DECLARE``、
    ``K_THREAD_STACK_DEFINE``、``K_THREAD_STACK_ARRAY_DEFINE``）。

  * 提供带有 pinned 段（``pinned_text`` / ``pinned_rodata`` / ``pinned_data`` /
    ``pinned_bss`` / ``pinned_noinit``）的自定义链接器脚本的树外开发板
    应将这些输入段匹配合并回普通的 text / rodata / data / bss / noinit 输出段。

  * 依赖 ``lnkr_pinned_*`` 链接器符号
    或 ``lnkr_is_pinned()`` / ``lnkr_is_region_pinned()`` 的树外代码
    必须删除这些引用。
    对应的 ``app_smem_pinned*.ld`` 包含
    以及 ``scripts/build/gen_app_partitions.py`` 的
    ``--pinoutput`` / ``--pinpartitions`` 选项也已移除。

开发板
******

* OpenOCD runner 现在使用标准的 ``--file`` 和 ``--file-type`` 接口指定 flash 文件，
  与 JLink 等其他 runner 对齐。
  以下更改适用：

  * ``--use-hex``、``--use-elf`` 和 ``--use-bin`` 标志已弃用。
    改用 ``--file-type``：

    * ``--use-elf`` → ``--file-type=elf``
    * ``--use-bin`` → ``--file-type=bin``
    * ``--use-hex`` → ``--file-type=hex``（或省略，因为 hex 是默认值）

  * 现在支持 ``--file`` 选项指定自定义文件路径，类似于 JLink runner。

  * 使用已弃用标志的开发板 cmake 文件将继续工作，但会发出弃用警告。

  * ``--file-type`` 选项现在可以不带 ``--file`` 使用，
    以在构建产物（hex、elf、bin）之间选择。

* native_sim：主机 FUSE 访问：
  现在默认使用 libfusev3 而非 v2。
  但可通过 :kconfig:option:`CONFIG_FUSE_LIBRARY_VERSION` 选择（:github:`104965`）。

* m5stack_fire：删除了 UART2 未使用的 pinctrl 条目，
  并将 UART1 引脚映射从 GPIO32/GPIO33 更新为 GPIO16/GPIO17
  以匹配文档中的 Grove PORT.C 接线。

* Ai-Thinker ``ai_m62_12f`` 和 ``ai_wb2_12f`` 开发板
  已分别重命名为 ``ai_m62_12f_kit`` 和 ``ai_wb2_12f_kit``。

* 编译定义 'XIP_EXTERNAL_FLASH'、'USE_HYPERRAM' 和 'XIP_BOOT_HEADER_XMCD_ENABLE'
  仅在 :zephyr_file:`boards/nxp/mimxrt1180_evk/xip/evkmimxrt1180_flexspi_nor_config.c`
  和 :zephyr_file:`boards/nxp/mimxrt1170_evk/xmcd/xmcd.c` 中使用，
  我们已将其改为各自开发板 CMakeLists.txt 文件中的局部作用域。
  依赖这些定义全局可用的应用可能需要更新（:github:`101322`）。

* Renesas ``ek_ra8t2/r7ka8t2lfecac/cm85`` 已重命名为 ``ek_ra8t2/r7ka8t2lflcac/cm85``。

* NXP 已更改某些树内编译标志的作用域，
  将其可见性限制到仅需要的地方。
  依赖这些标志全局可用的树外应用或开发板
  可能需要将它们添加到自己的 CMakeLists.txt 文件中
  以确保继续正确构建（:github:`100252`）。
  受影响的标志如下：

  * 对于 RT10xx 和 RT11xx 系列，
    编译标志 ``BOARD_FLASH_SIZE`` 最初定义在
    ``boards/nxp/mimxrt10xx_evk/CMakeLists.txt`` 和
    ``boards/nxp/mimxrt11xx_evk/CMakeLists.txt`` 中，
    仅由 HAL 头文件 ``fsl_flexspi_nor_boot.h`` 使用，
    该头文件被 :zephyr_file:`soc/nxp/imxrt/imxrt10xx/soc.c` 和
    :zephyr_file:`soc/nxp/imxrt/imxrt11xx/soc.c` 包含。
    为避免与其他全局标志潜在冲突，
    该宏现在使用
    :zephyr_file:`soc/nxp/imxrt/imxrt10xx/CMakeLists.txt` 和
    :zephyr_file:`soc/nxp/imxrt/imxrt11xx/CMakeLists.txt` 中的
    ``zephyr_library_compile_definitions()`` 在 SoC 层定义。
    此更改已应用于所有 RTxxxx 开发板。

  * 对于 RTxxx 系列，
    编译标志 ``BOARD_FLASH_SIZE`` 最初定义在
    ``boards/nxp/mimxrtxxx_evk/CMakeLists.txt`` 中，
    未在 Zephyr 树中使用，
    因此已从所有 RTxxx 开发板 CMakeLists.txt 文件中删除。

  * 对于 RTxxx 系列，
    编译标志 ``BOOT_HEADER_ENABLE`` 之前定义在
    ``boards/nxp/mimxrtxxx_evk/CMakeLists.txt`` 中
    并在 ``boards/nxp/rtxxx/<boot_header>.c`` 中使用，
    已被 Kconfig 选项替换。
    因此，``zephyr_compile_definitions(BOOT_HEADER_ENABLE=1)`` 行
    已从 RTxxx 开发板 CMakeLists.txt 文件中删除。

  * 从 :zephyr_file:`boards/nxp/rd_rw612_bga/CMakeLists.txt` 中
    删除了编译标志 ``BOOT_HEADER_ENABLE`` 定义，
    因为它未在 Zephyr 树中使用。

  * 最初，编译标志 ``XIP_BOOT_HEADER_ENABLE`` 和 ``XIP_BOOT_HEADER_DCD_ENABLE``
    在 ``boards/nxp/rt1xxx/<boot_header>.c`` 中使用。
    这些标志已转换为 NXP RTxxxx 评估开发板上的 Kconfig 选项，
    允许通过 Kconfig 构建系统而非编译时定义配置 boot-header。
    因此，``zephyr_compile_definitions(XIP_BOOT_HEADER_ENABLE=1)``
    和 ``zephyr_compile_definitions(XIP_BOOT_HEADER_DCD_ENABLE=1)``
    已从 RTxxxx 开发板级 CMakeLists.txt 文件中删除。
    由于这些宏还需由 ``hal_nxp/rt10xx/fsl_flexspi_nor_boot.h`` 和
    ``hal_nxp/rt11xx/fsl_flexspi_nor_boot.h`` 使用，因此它们已使用
    ``zephyr_library_compile_definitions()`` 添加到对应的 SoC 层
    CMakeLists.txt 文件中，以限定其作用域。

* 以下 Nordic SoC Kconfig 已弃用并被替换。如果 Kconfig、CMake 或代码引用了弃用项，
  需要更新：

  * :kconfig:option:`CONFIG_SOC_SERIES_NRF51X` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_NRF51`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF52X` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_NRF52`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF53X` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_NRF53`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF54HX` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_NRF54H`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF54LX` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_NRF54L`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF91X` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_NRF91`
  * :kconfig:option:`CONFIG_SOC_SERIES_NRF92X` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_NRF92`

* 以下 Sifive Freedom SoC Kconfig 已弃用并被替换。如果 Kconfig、CMake 或代码
  引用了弃用项，需要更新：

  * :kconfig:option:`CONFIG_SOC_SERIES_SIFIVE_FREEDOM_FE300` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_FE300`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FE310_G000` 替换为
    :kconfig:option:`CONFIG_SOC_FE310_G000`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FE310_G002` 替换为
    :kconfig:option:`CONFIG_SOC_FE310_G002`
  * :kconfig:option:`CONFIG_SOC_SERIES_SIFIVE_FREEDOM_FU500` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_FU500`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU540` 替换为
    :kconfig:option:`CONFIG_SOC_FU540`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU540_E51` 替换为
    :kconfig:option:`CONFIG_SOC_FU540_E51`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU540_U54` 替换为
    :kconfig:option:`CONFIG_SOC_FU540_U54`
  * :kconfig:option:`CONFIG_SOC_SERIES_SIFIVE_FREEDOM_FU700` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_FU700`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU740` 替换为
    :kconfig:option:`CONFIG_SOC_FU740`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU740_S7` 替换为
    :kconfig:option:`CONFIG_SOC_FU740_S7`
  * :kconfig:option:`CONFIG_SOC_SIFIVE_FREEDOM_FU740_U74` 替换为
    :kconfig:option:`CONFIG_SOC_FU740_U74`

* ITE ``it515xx_evb`` 已重命名为 ``it51xxx_evb``。

* 使用 :kconfig:option:`CONFIG_USE_DT_CODE_PARTITION` 或设置了
  ``zephyr,code-partition`` 选择节点的开发板，现在应使用新的
  :dtcompatible:`zephyr,mapped-partition` 兼容值。该绑定使用设备树单元地址
  获取分区的内存映射地址，而不是手动向上遍历子节点直到找到特定名称的节点再计算地址；
  同时，当使用 :dtcompatible:`zephyr,mapped-partition` 时，也禁止使用
  :kconfig:option:`CONFIG_FLASH_LOAD_OFFSET` 和 :kconfig:option:`CONFIG_FLASH_LOAD_SIZE`，
  因为链接文件现在无需通过 Kconfig 执行数学运算作为中间步骤即可确定 NVM 偏移和大小。
  此外，切换到 :dtcompatible:`zephyr,mapped-partition` 后，在内存映射设备上不再需要
  :dtcompatible:`fixed-subpartitions`，因为这些分区可以原生嵌套，并且在使用设备树
  ``ranges`` 属性时会具有正确的地址和偏移。对于未更新为使用
  :dtcompatible:`zephyr,mapped-partition` 绑定处理 ``zephyr,code-partition``
  选择设备的开发板目标，将设置
  :kconfig:option:`CONFIG_FLASH_CODE_PARTITION_USING_FIXED_PARTITIONS`。
  未来将弃用使用 fixed-partitions 作为选择 ``zephyr,code-partition`` 节点的支持。

* 基于 STM32N6x SoC（:kconfig:option:`CONFIG_SOC_SERIES_STM32N6X`）的开发板或项目，
  现在需要在 Zephyr 应用预期在处理器安全状态中运行时显式启用
  :kconfig:option:`CONFIG_TRUSTED_EXECUTION_SECURE`。或者，如果 Zephyr 应用预期
  在处理器非安全状态中运行，开发板或项目必须显式启用
  :kconfig:option:`CONFIG_TRUSTED_EXECUTION_NON_SECURE`。

* 以下 WCH SoC Kconfig 已重命名。如果 Kconfig、CMake 或代码引用了旧 Kconfig，
  需要更新：

  * ``CONFIG_SOC_SERIES_CH32V00X`` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_QINGKE_V2C`

Device Drivers and Devicetree
****************************

.. zephyr-keep-sorted-start re(^\w) ignorecase

ADC
===

* :dtcompatible:`renesas,ra-adc` 兼容值已替换为 :dtcompatible:`renesas,ra-adc12`。
  使用旧兼容值的应用必须更新其设备树节点。

* 新增了 :dtcompatible:`renesas,ra-adc16` 兼容值。使用 EK-RA2A1 开发板时
  必须使用它，该开发板提供 16 位 ADC 分辨率。

* 将 :kconfig:option:`CONFIG_ADC_MCUX_SAR_ADC` 重命名为
  :kconfig:option:`CONFIG_ADC_NXP_SAR_ADC`。
* 将驱动文件从 ``adc_mcux_sar_adc.c`` 重命名为
  :zephyr_file:`drivers/adc/adc_nxp_sar_adc.c`。
* 使用 SAR ADC 驱动的应用需要更新设备树中的节点，加入
  ``zephyr,input-positive`` 以指定硬件通道。对于当前支持 SAR ADC 的 SoC，
  参考电压应使用 ``ADC_REF_VDD_1`` 而不是 ``ADC_REF_INTERNAL``。
  该驱动更新同时修复了此问题，因此用户还需相应更新设备树中该属性的值。
  (:github:`100978`)

* :dtcompatible:`st,stm32-adc` 不再具有 ``resolutions`` 属性，
  替换为 ``st,adc-resolutions`` 属性。对于修订版 Y 的 STM32H7 器件，
  不再需要替换 14 位和 12 位分辨率值。如果使用了 14 位或 12 位分辨率，
  此更改可能影响功耗。之前使用的是功耗优化值，现在使用的是标准值
  （非功耗优化但精度更高）。其他系列不受影响。

Clock Control
=============

* ``bflb,bl60x-pll``、``bflb,bl61x-root-clk``、``bflb,bl60x-root-clk``、
  ``bflb,bl61x-wifipll``、``bflb,bl70x-root-clk`` 和 ``bflb,bl61x-flash-clk``
  已分别替换为 :dtcompatible:`bflb,flash-clk`、:dtcompatible:`bflb,pll`
  和 :dtcompatible:`bflb,root-clk`。

* :dtcompatible:`infineon,peri-div` 时钟控制绑定已移除 ``resource-type``、
  ``resource-instance`` 和 ``resource-channel`` 属性。这些属性不再被驱动使用，
  相应字段已从驱动内部数据结构中移除。使用该兼容值的树外开发板必须从设备树节点中
  删除这些属性。(:github:`105393`)

Controller Area Network (CAN)
=============================

* 移除了 ``CONFIG_CAN_MAX_FILTER``、``CONFIG_CAN_MAX_STD_ID_FILTER`` 和
  ``CONFIG_CAN_MAX_EXT_ID_FILTER`` (:github:`100596`)。
  它们由以下驱动特定的 Kconfig 符号替换，其中一些默认值已提高以满足典型软件需求：

  * :dtcompatible:`zephyr,can-loopback` 使用
    :kconfig:option:`CONFIG_CAN_LOOPBACK_MAX_FILTERS`
  * :dtcompatible:`adi,max32-can` 使用
    :kconfig:option:`CONFIG_CAN_MAX32_MAX_FILTERS`
  * :dtcompatible:`microchip,mcp2515` 使用
    :kconfig:option:`CONFIG_CAN_MCP2515_MAX_FILTERS`
  * :dtcompatible:`microchip,mcp251xfd` 使用
    :kconfig:option:`CONFIG_CAN_MCP251XFD_MAX_FILTERS`
  * :dtcompatible:`nxp,flexcan` 使用
    :kconfig:option:`CONFIG_CAN_MCUX_FLEXCAN_MAX_FILTERS`
  * :dtcompatible:`zephyr,native-linux-can` 使用
    :kconfig:option:`CONFIG_CAN_NATIVE_LINUX_MAX_FILTERS`
  * :dtcompatible:`renesas,rcar-can` 使用
    :kconfig:option:`CONFIG_CAN_RCAR_MAX_FILTERS`
  * :dtcompatible:`kvaser,pcican` 和 :dtcompatible:`espressif,esp32-twai` 使用
    :kconfig:option:`CONFIG_CAN_SJA1000_MAX_FILTERS`
  * :dtcompatible:`st,stm32-bxcan` 使用
    :kconfig:option:`CONFIG_CAN_STM32_BXCAN_MAX_EXT_ID_FILTERS` 和
    :kconfig:option:`CONFIG_CAN_STM32_BXCAN_MAX_STD_ID_FILTERS`
  * :dtcompatible:`st,stm32-fdcan` 使用
    :kconfig:option:`CONFIG_CAN_STM32_FDCAN_MAX_EXT_ID_FILTERS` 和
    :kconfig:option:`CONFIG_CAN_STM32_FDCAN_MAX_STD_ID_FILTERS`
  * :dtcompatible:`infineon,xmc4xxx-can-node` 使用
    :kconfig:option:`CONFIG_CAN_XMC4XXX_MAX_FILTERS`

* 将 :dtcompatible:`nxp,flexcan` 和 :dtcompatible:`nxp,flexcan-fd` 的
  Kconfig 选项 ``CONFIG_CAN_MAX_MB`` 替换为每个实例的 ``number-of-mb``
  设备树属性 (:github:`99483`)。

* :dtcompatible:`nxp,flexcan` 的 ``clk-source`` 设备树属性如果存在，
  现在会自动在命名输入时钟 ``clksrc0`` 和 ``clksrc1`` 之间选择，
  用作 CAN 协议引擎时钟。

* 将 NXP LPC 系列 MCAN 驱动 Kconfig 选项 ``CONFIG_CAN_MCUX_MCAN`` 重命名为
  :kconfig:option:`CONFIG_CAN_NXP_LPC_MCAN`，因为该驱动并非基于
  NXP MCUXpresso HAL (:github:`103679`)。

* 为 :dtcompatible:`ti,tcan4x5x` 添加了设备树属性 ``ti,nwkrq-voltage-vio``，
  用于配置 ``nWKRQ`` 引脚使用的电压轨。为保持之前驱动默认使用 VIO 的行为，
  必须设置该属性 (:github:`104182`)。

Counter
=======

* 实现 ``get_value_64`` API 的驱动现在需要选择
  :kconfig:option:`CONFIG_COUNTER_SUPPORTS_64BITS_TICKS`，
  应用需要 :kconfig:option:`CONFIG_COUNTER_64BITS_TICKS` 才能启用该 API。
  (:github:`94189`)

* NXP LPTMR 驱动（:dtcompatible:`nxp,lptmr`）已更新，
  修复了错误的预分频器和毛刺滤波器配置：

  * ``prescale-glitch-filter`` 属性的有效范围从 ``[0-16]`` 改为 ``[0-15]``。
    值 ``16`` 对脉冲计数器模式无效，已移除。使用值 ``16`` 的设备树
    必须更新为使用 ``[0-15]`` 范围内的值。

  * 引入了新的布尔属性 ``prescale-glitch-filter-bypass``，
    用于显式控制预分频器/毛刺滤波器旁路。之前，设置
    ``prescale-glitch-filter = <0>`` 会隐式启用旁路模式，存在歧义。

    在 v4.4 及以后，旁路仅由 ``prescale-glitch-filter-bypass`` 是否存在控制。
    如果该属性不存在，则预分频器/毛刺滤波器处于活动状态，
    并应用 ``prescale-glitch-filter``。

  * 明确了预分频器/毛刺滤波器行为：

    * 时间计数器模式：预分频器将时钟除以 ``2^(prescale-glitch-filter + 1)``
    * 脉冲计数器模式：毛刺滤波器在 ``2^prescale-glitch-filter`` 个上升沿后
      识别变化（毛刺滤波不支持值 0）

  * 所有树内设备树节点已更新为使用 ``prescale-glitch-filter-bypass;``
    而不是 ``prescale-glitch-filter = <0>;``。树外开发板应相应更新。

  * 如果同时设置了 ``prescale-glitch-filter-bypass`` 和 ``prescale-glitch-filter``，
    旁路模式优先，``prescale-glitch-filter`` 值被忽略。

  迁移示例：

  .. code-block:: devicetree

     /* 旧（已弃用） */
     lptmr0: counter@40040000 {
         compatible = "nxp,lptmr";
         /* 隐式旁路 */
         prescale-glitch-filter = <0>;
     };

     /* 新（正确） */
     lptmr0: counter@40040000 {
         compatible = "nxp,lptmr";
         /* 显式旁路 */
         prescale-glitch-filter-bypass;
     };

  .. rubric:: 使用 ``prescale-glitch-filter`` 的示例

  .. note::

     ``prescale-glitch-filter-bypass`` 是布尔值。如果存在，则启用旁路。
     如果不存在，则禁用旁路并应用 ``prescale-glitch-filter``。

     在脉冲计数器模式中，``prescale-glitch-filter = <0>`` 不是受支持的毛刺滤波配置。
     如需请求无滤波，请使用 ``prescale-glitch-filter-bypass;``。

  * 时间计数器模式：对计数器时钟分频

    在时间计数器模式中，预分频器除以 ``2^(N + 1)``。

    .. code-block:: devicetree

       /* 除以 2^(0+1) = 2 */
       lptmr0: counter@40040000 {
           compatible = "nxp,lptmr";
           /* 时间计数器模式 */
           timer-mode-sel = <0>;
           clk-source = <1>;
           clock-frequency = <32768>;
           /* /2 */
           prescale-glitch-filter = <0>;
           resolution = <16>;
       };

       /* 除以 2^(3+1) = 16 */
       lptmr1: counter@40041000 {
           compatible = "nxp,lptmr";
           /* 时间计数器模式 */
           timer-mode-sel = <0>;
           clk-source = <1>;
           clock-frequency = <32768>;
           /* /16 */
           prescale-glitch-filter = <3>;
           resolution = <16>;
       };

  * 时间计数器模式：显式旁路（不分频）

    .. code-block:: devicetree

       lptmr0: counter@40040000 {
           compatible = "nxp,lptmr";
           /* 时间计数器模式 */
           timer-mode-sel = <0>;
           clk-source = <1>;
           clock-frequency = <32768>;
           /* 无预分频器 */
           prescale-glitch-filter-bypass;
           resolution = <16>;
       };

  * 脉冲计数器模式：毛刺滤波

    在脉冲计数器模式中，毛刺滤波器在 ``2^N`` 个上升沿后识别变化。
    值 ``0`` 不支持毛刺滤波；如需无滤波，请使用旁路。

    .. code-block:: devicetree

       /* 在 2^2 = 4 个上升沿后识别变化 */
       lptmr0: counter@40040000 {
           compatible = "nxp,lptmr";
           /* 脉冲计数器模式 */
           timer-mode-sel = <1>;
           clk-source = <1>;
           input-pin = <0>;
           prescale-glitch-filter = <2>;
           resolution = <16>;
       };

       /* 无滤波（显式旁路） */
       lptmr1: counter@40041000 {
           compatible = "nxp,lptmr";
           /* 脉冲计数器模式 */
           timer-mode-sel = <1>;
           clk-source = <1>;
           input-pin = <0>;
           prescale-glitch-filter-bypass;
           resolution = <16>;
       };

* NXP i.MX GPT 计数器驱动（:dtcompatible:`nxp,imx-gpt`）
  现在默认为 ``run-mode = "restart"``，而不是之前硬编码的自由运行行为。

  * **之前行为**（Zephyr ≤ 4.3）：GPT 计数器始终运行在自由运行模式
    （``enableFreeRun = true``）。计数器在比较事件时继续计数而不复位。

  * **新行为**（Zephyr ≥ 4.4）：除非显式配置，GPT 计数器默认为重启模式。
    新的 ``run-mode`` 设备树属性控制行为：

    * ``"restart"``（默认）：计数器达到 Compare Channel 1 值时复位为 0
    * ``"free-run"``：计数器继续计数而不复位（之前行为）

  **需要迁移**：使用 GPT 计数器的树外开发板和应用必须在其设备树节点中添加
  ``run-mode = "free-run";`` 以保留之前行为。

  .. code-block:: devicetree

     /* 树外开发板：添加此内容以保留之前行为 */
     gpt2: gpt@400f0000 {
         compatible = "nxp,imx-gpt";
         /* 显式恢复 Zephyr ≤4.3 行为 */
         run-mode = "free-run";
         /* ... 其他属性 ... */
     };

  .. warning::

     驱动使用 Compare Channel 1 实现 Zephyr 计数器报警功能。使用
     ``run-mode = "restart"`` 时，设置报警会导致计数器在报警比较点复位。
     如果应用依赖报警和连续计数，必须使用 ``run-mode = "free-run"``。

  .. note::

     此更改标准化了 NXP 计数器驱动运行模式配置。GPT 现在使用显式设备树属性
     而不是硬编码值，允许按实例自定义。

.. _migration_4.4_devicetree:

Devicetree
==========

* :ref:`dt-bindings` 不再允许为 ``status`` 和 ``#address-cells``、``#size-cells``
  属性指定任何默认值。这些属性的语义在设备树 `Specification
  <https://www.devicetree.org/specifications>`_ 第 2.3.4 节和 `Specification
  <https://www.devicetree.org/specifications>`_ 第 2.3.5 节中定义，
  用户不应尝试用自己的默认值覆盖它们。

  以下绑定语法现在会导致构建错误：

  .. code-block:: yaml

     properties:
       "status":
         default: ...             <---- 任何默认值都是构建错误
       "#address-cells":
         default: ...             <---- 任何默认值都是构建错误
       "#size-cells":
         default: ...             <---- 任何默认值都是构建错误

  如果之前依赖绑定中的默认值，现在必须在设备树源中显式指定值
  以修复这些构建错误。

* 设备树兼容值 ``ilitek,ili9806e-dsi`` 已重命名。
  请改用 :dtcompatible:`ilitek,ili9806e`。

Display
=======

* 对于 ILI9XXX 控制器，设备树中用于面板颜色格式选择的 ``ILI9XXX_PIXEL_FORMAT_x``
  用法已更新为 ``PANEL_PIXEL_FORMAT_x``。树外开发板和扩展板应相应更新。
  (:github:`99267`)

* 对于 ILI9341 控制器，显示镜像配置已更新，
  以符合示例 ``samples/drivers/display`` 中描述的行为。(:github:`99267`)
  此更改会导致某些显示面板出现镜像问题，将在 v4.4.1 发布中提供正式修复。
  (:github:`106862`)

* ``PIXEL_FORMAT_BGR_565`` 像素格式（及其对应的设备树宏
  ``PANEL_PIXEL_FORMAT_BGR_565``）已重命名为 :c:enumerator:`PIXEL_FORMAT_RGB_565X`
  （及 :c:macro:`PANEL_PIXEL_FORMAT_RGB_565X`），
  以正确反映它是 RGB-565 的字节交换版本，而不是交换红蓝通道的格式。
  (:github:`99276`) 使用 ``PIXEL_FORMAT_BGR_565`` 表示字节交换 RGB-565 的应用和库
  必须更新为使用 :c:enumerator:`PIXEL_FORMAT_RGB_565X`。

* Kconfig 选项 ``CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_BGR_565`` 和
  ``CONFIG_ST7789V_BGR565`` 已分别重命名为
  :kconfig:option:`CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_RGB_565X` 和
  :kconfig:option:`CONFIG_ST7789V_RGB565X`。(:github:`99276`)

* ``CONFIG_SSD1327`` 符号已重命名为 :kconfig:option:`CONFIG_SSD1327_5`，
  以同时包含 ``SSD1325``。

* ``solomon,ssd1327fb``、``solomon,ssd1306fb`` 和 ``solomon,ssd1309fb``
  设备树兼容值已分别重命名为 :dtcompatible:`solomon,ssd1327`、
  :dtcompatible:`solomon,ssd1306` 和 :dtcompatible:`solomon,ssd1309`，
  以与其他显示控制器保持一致，并消除与 Zephyr 无关的 ``fb`` 后缀。

* NXP eLCDIF 控制器（:dtcompatible:`nxp,imx-elcdif`）
  现在正确声明支持 :c:macro:`PIXEL_FORMAT_XRGB_8888`，
  而不是 :c:macro:`PIXEL_FORMAT_ARGB_8888`。

* ``waveshare,7inch-dsi-lcd-c`` 设备树兼容值已替换为
  :dtcompatible:`waveshare,dsi2dpi`，``CONFIG_WAVESHARE_7INCH_DSI_LCD_C``
  选项已替换为 :kconfig:option:`CONFIG_WAVESHARE_DSI2DPI`。(:github:`100140`)

* 使用 STM32 LTDC 显示控制器的开发板必须更新其设备树，
  使 :dtcompatible:`st,stm32-ltdc` 节点中的 ``pixel-format`` 为
  :c:macro:`PANEL_PIXEL_FORMAT_RGB_888`。(:github:`99277`)

DMA
===

* 移除了 :kconfig:option:`CONFIG_DMA_MCUX_EDMA_V5` (:github:`100341`)。
  该宏之前用于区分 nxp,version(5) 和 nxp,version(4)。
  现在它支持两个版本的统一维护。
  用户可以将 ``DMA_MCUX_EDMA_V5`` 修改为 ``DMA_MCUX_EDMA_V4``。

EEPROM
======

* 添加了 :c:func:`eeprom_target_read_data()` 和 :c:func:`eeprom_target_write_data()`，
  它们接受偏移量和长度；并为 I2C EEPROM 目标驱动弃用了
  :c:func:`eeprom_target_program()`。

* 更新了 :dtcompatible:`microchip,xec-eeprom` 的 PCR 和 GIRQ 属性，
  使用新宏 (:github:`104591`)。

ESP32-S3
========

* 之前的 ``espressif,esp32-lcd-cam`` 绑定已重构。
  LCD_CAM 外设现在由通用 ``lcd_cam`` 节点表示，
  其功能块拆分为两个独立的子节点：

  * :dtcompatible:`espressif,esp32-lcd-cam-dvp` 兼容节点用于 DVP（相机）输入模块，
    标签为 ``lcd_cam_dvp``。
  * :dtcompatible:`espressif,esp32-lcd-cam-mipi-dbi` 兼容节点用于 LCD 输出模块，
    标签为 ``lcd_cam_disp``。

  原始 :dtcompatible:`espressif,esp32-lcd-cam` 兼容节点保留通用引脚控制、
  时钟和中断属性，而相机特定属性已移入新的 ``lcd_cam_dvp`` 子节点。

  相机相关属性必须从 ``lcd_cam`` 节点移到新的 ``lcd_cam_dvp`` 子节点，
  并且 ``zephyr,camera`` 选择属性应指向 ``lcd_cam_dvp``。

Ethernet
========

* 使用 :c:struct:`net_eth_mac_config` 的驱动 MAC 地址配置支持已引入以下驱动：

  * :dtcompatible:`atmel,sam-gmac` 和 :dtcompatible:`atmel,sam0-gmac`
    (:github:`96598`)

    * 移除 ``CONFIG_ETH_SAM_GMAC_MAC_I2C_EEPROM``
    * 移除 ``CONFIG_ETH_SAM_GMAC_MAC_I2C_INT_ADDRESS``
    * 移除 ``CONFIG_ETH_SAM_GMAC_MAC_I2C_INT_ADDRESS_SIZE``
    * 移除 ``mac-eeprom`` 属性

  * :dtcompatible:`litex,liteeth` (:github:`100620`)
  * :dtcompatible:`microchip,lan865x` (:github:`100318`)
  * :dtcompatible:`microchip,lan9250` (:github:`99127`)
  * :dtcompatible:`nxp,enet-mac` (:github:`102775`)
  * :dtcompatible:`sensry,sy1xx-mac` (:github:`100619`)
  * :dtcompatible:`st,stm32n6-ethernet`、:dtcompatible:`st,stm32h7-ethernet`
    和 :dtcompatible:`st,stm32-ethernet` (:github:`102810`, :github:`105090`)
  * :dtcompatible:`virtio,net` (:github:`100106`)
  * :dtcompatible:`vnd,ethernet` (:github:`96598`)
  * :dtcompatible:`wiznet,w5500` (:github:`100919`)
  * :dtcompatible:`snps,designware-ethernet` (:github:`105090`)

  MAC 地址现在应设置为 :dtcompatible:`nvmem-layout` 的子节点。
  参见 :ref:`MAC 地址配置 <mac_address_config>` 的文档。

* 已从 :dtcompatible:`ethernet-phy` 中移除 ``fixed-link`` 属性。
  如需要该功能，请改用新的 :dtcompatible:`ethernet-phy-fixed-link` 兼容值。
  在那里需要使用 ``default-speeds`` 属性指定固定链路参数 (:github:`100454`)。

* :dtcompatible:`microchip,ksz8081` 的 ``reset-gpios`` 属性已重构为低电平有效，
  可能需要在设备树中将引脚设置为 ``GPIO_ACTIVE_LOW`` (:github:`100751`)。

* :kconfig:option:`CONFIG_ETH_INIT_PRIORITY` 现在默认设置为 60。
  :kconfig:option:`CONFIG_PHY_INIT_PRIORITY` 和 :kconfig:option:`CONFIG_MDIO_INIT_PRIORITY`
  现在默认使用 :kconfig:option:`CONFIG_ETH_INIT_PRIORITY` 的值。
  :kconfig:option:`CONFIG_PTP_CLOCK_INIT_PRIORITY` 也是如此，
  但仅在启用 :kconfig:option:`CONFIG_ETH_DRIVER` 时。
  这样优先级基于设备树中的依赖关系。(:github:`104310`)

* 支持校验和卸载的驱动现在需要选择新的 Kconfig 选项
  :kconfig:option:`CONFIG_NET_CHECKSUM_OFFLOAD_SUPPORTED`。
  需要启用 :kconfig:option:`CONFIG_NET_CHECKSUM_OFFLOAD` 才能使用校验和卸载。
  如果选择了 :kconfig:option:`CONFIG_NET_CHECKSUM_OFFLOAD_SUPPORTED`，则默认启用。
  (:github:`105051`)

* :dtcompatible:`microchip,lan865x` 的 ``phy-handle`` 属性现在必须设置为 phy 节点。

* 已移除 ``CONFIG_NET_DSA_DEPRECATED``。兼容值 ``microchip,ksz8463``、
  ``microchip,ksz8794`` 和 ``microchip,ksz8863`` 的驱动已移除，
  因为它们未迁移到新的 DSA 子系统。(:github:`105926`)

* 当通过 ``ETHERNET_CONFIG_TYPE_MAC_ADDRESS`` 更改 MAC 地址时，
  以太网驱动不再需要自行调用 :c:func:`net_if_set_link_addr`。
  (:github:`105931`)

File System
===========

* 如果设备树中存在任何启用的带 ``automount`` 属性的
  :dtcompatible:`zephyr,fstab,fatfs`，则
  :kconfig:option:`CONFIG_FS_FATFS_FSTAB_AUTOMOUNT` 现在默认启用。
  不希望此行为的应用需要显式禁用该选项。(:github:`103139`)

* NVS 和 ZMS 已迁移到新的 Key-Value Storage Systems（KVSS）子系统；
  迁移影响 NVS 和 ZMS 接口头文件路径，已从 ``zephyr/fs/`` 移到 ``zephyr/kvss/``。
  NVS 和 ZMS 的 Kconfig 选项已从“File Systems”菜单移到“Key-Value Storage Systems”菜单，
  未影响任何 Kconfig。(:github:`103244`)

GPIO
====

* LiteX GPIO 驱动 :dtcompatible:`litex,gpio` 已重构以支持更改方向。
  驱动现在使用 reg-names 属性检测 GPIO 控制器支持的模式。
  已移除设备树属性 ``port-is-output``。
  reg-names 现在直接取自 LiteX。(:github:`99329`)

* :dtcompatible:`renesas,rz-gpio` 的 ``irqs`` 属性已重构，
  用于将引脚显式映射到中断 phandle，而不是中断索引 (:github:`101256`)。

  .. code-block:: devicetree

     /* 旧（Zephyr ≤ 4.3） */
     &gpio16 {
         /* 将 port16 pin3 映射到 tint7 */
         irqs = <3 7>;
     };

     /* 新（Zephyr ≥ 4.4） */
     &tint7 {
         status = "okay";
     };

     &gpio16 {
         /* 将 port16 pin3 映射到 tint7 */
         irqs = <&tint7 3>;
     };

Infineon
========

* Infineon 驱动文件名已重命名，移除名称中的 ``cat1``，
  以支持跨多个器件类别复用。以下驱动已重命名 (:github:`99174`)：

  * ``adc_ifx_cat1.c`` → ``adc_ifx.c``
  * ``clock_control_ifx_cat1.c`` → ``clock_control_ifx.c``
  * ``counter_ifx_cat1.c`` → ``counter_ifx.c``
  * ``dma_ifx_cat1.c`` → ``dma_ifx.c``
  * ``dma_ifx_cat1_pdl.c`` → ``dma_ifx_pdl.c``
  * ``flash_ifx_cat1.c`` → ``flash_ifx.c``
  * ``flash_ifx_cat1_qspi.c`` → ``flash_ifx_qspi.c``
  * ``flash_ifx_cat1_qspi_mtb_hal.c`` → ``flash_ifx_qspi_mtb_hal.c``
  * ``gpio_ifx_cat1.c`` → ``gpio_ifx.c``
  * ``i2c_ifx_cat1.c`` → ``i2c_ifx.c``
  * ``i2c_ifx_cat1_pdl.c`` → ``i2c_ifx_pdl.c``
  * ``mbox_ifx_cat1.c`` → ``mbox_ifx.c``
  * ``pinctrl_ifx_cat1.c`` → ``pinctrl_ifx.c``
  * ``rtc_ifx_cat1.c`` → ``rtc_ifx.c``
  * ``ifx_cat1_sdio.c`` → ``ifx_sdio.c``
  * ``sdio_ifx_cat1_pdl.c`` → ``sdio_ifx_pdl.c``
  * ``serial_ifx_cat1_uart.c`` → ``serial_ifx_uart.c``
  * ``spi_ifx_cat1.c`` → ``spi_ifx.c``
  * ``spi_ifx_cat1_pdl.c`` → ``spi_ifx_pdl.c``
  * ``uart_ifx_cat1.c`` → ``uart_ifx.c``
  * ``uart_ifx_cat1_pdl.c`` → ``uart_ifx_pdl.c``
  * ``wdt_ifx_cat1.c`` → ``wdt_ifx.c``

  相应的 Kconfig 符号和绑定文件也已更新：

  * ``CONFIG_*_INFINEON_CAT1`` → ``CONFIG_*_INFINEON``
  * ``compatible: "infineon,cat1-adc"`` → ``compatible: "infineon,adc"``

* Infineon 蓝牙 HCI UART 驱动（:kconfig:option:`CONFIG_BT_HCI_UART_INFINEON`）
  兼容值 :dtcompatible:`infineon,bt-hci-uart` 现在显式限定于使用 HCI UART 传输的
  AIROC 连接芯片。(:github:`103871`)

  相应的 Kconfig 符号和设备树兼容值也已更新：

  * ``CONFIG_BT_CYW43XX`` → :kconfig:option:`CONFIG_BT_HCI_UART_INFINEON`
  * ``dtcompatible: "infineon,cyw43xxx-bt-hci"`` → ``dtcompatible: "infineon,bt-hci-uart"``

Input
=====

* CST816S 输入驱动已泛化以支持 CST8xx 系列。
  驱动和 Kconfig 文件已重命名 (:github:`105348`)

  * ``input_cst816s.c`` → ``input_cst8xx.c``
  * ``Kconfig.cst816s`` → ``Kconfig.cst8xx``

  相应的设备树兼容值已更新：

  * ``hynitron,cst816s`` → :dtcompatible:`hynitron,cst8xx`

  相应的 Kconfig 也已更新：

  * ``CONFIG_INPUT_CST816S`` → :kconfig:option:`CONFIG_INPUT_CST8XX`
  * ``CONFIG_INPUT_CST816S_PERIOD`` → :kconfig:option:`CONFIG_INPUT_CST8XX_PERIOD`
  * ``CONFIG_INPUT_CST816S_INTERRUPT`` → :kconfig:option:`CONFIG_INPUT_CST8XX_INTERRUPT`
  * ``CONFIG_INPUT_CST816S_EV_DEVICE`` → :kconfig:option:`CONFIG_INPUT_CST8XX_EV_DEVICE`

  dt-binding 宏前缀也已从 ``CST816S_*`` 更新为 ``CST8XX_*``。

Interrupt Controller
===================

* :dtcompatible:`swerv,pic` 现在通过添加供应商前缀变为 :dtcompatible:`cdns,swerv-pic`。

Keyboard matrix
==============

* 通用键盘矩阵设备树绑定已更新，轮询周期属性改用微秒而不是毫秒。

  以下属性已重命名并更改单位：

  * ``poll-period-ms`` -> ``poll-period-us``
  * ``stable-poll-period-ms`` -> ``stable-poll-period-us``

  使用这些属性的应用必须：

  * 用新属性名替换旧属性名，并且
  * 将值从毫秒转换为微秒。例如，之前表示 10 ms 的值 ``10``
    现在必须写为 ``10000`` 以表示 10,000 µs。

MDIO
====

* 已移除 ``mdio_bus_enable()`` 和 ``mdio_bus_disable()`` 函数。
  MDIO 总线启用/禁用现在由 MDIO 驱动内部处理。(:github:`99690`)

* MDIO 驱动区域已集成到以太网驱动区域。
  驱动已从 ``drivers/mdio/`` 移到 :zephyr_file:`drivers/ethernet/mdio/`。
  设备树绑定已从 ``dts/bindings/mdio/`` 移到
  :zephyr_file:`dts/bindings/ethernet/mdio/`。(:github:`103944`)

MEMC
====

* :dtcompatible:`st,stm32-xspi-psram` 和 :dtcompatible:`st,stm32-ospi-psram`
  兼容节点现在需要包含 ``st,refresh`` 属性，
  以内存时钟周期数指定 PSRAM 刷新率。(:github:`102735`)
  驱动中硬编码的默认值 320（:dtcompatible:`st,stm32-xspi-psram`）
  和 129（:dtcompatible:`st,stm32-ospi-psram`）已移除。

NXP
===

* NXP DTSI 文件已移到 ``dts/arm/nxp`` 下的特定系列子目录中，
  以提高可维护性和可发现性，并与 ``soc/nxp`` 下的结构匹配。
  必须更新移动文件的设备树包含路径。将形如
  ``#include <nxp/nxp_*.dtsi>`` 的包含更新为使用正确的系列子目录。
  (:github:`101243`)

  示例：

  .. code-block:: dts

     /* 之前 */
     #include <nxp/nxp_rt1060.dtsi>

     /* 之后 */
     #include <nxp/imxrt/nxp_rt1060.dtsi>

  此更改仅适用于从 ``dts/arm/nxp`` 移动的 NXP ARM SoC 包含文件。
  不要更改位于其他位置（例如 ``dts/arm64/nxp`` 下）的 DTSI 文件的包含。

  要定位受影响的包含，可以搜索旧的包含前缀：

  .. code-block:: console

     git grep "#include <nxp/nxp_" -- '*.dtsi' '*.dts' '*.overlay'

* 用作系统定时器的 :dtcompatible:`nxp,lptmr` 节点现在必须通过
  ``zephyr,system-timer`` 选择属性指定。基于 i.MX95 和 MCX-W SoC 的开发板
  已在 SoC DTSI 中设置此项，无需更改。所有其他使用
  :kconfig:option:`CONFIG_MCUX_LPTMR_TIMER` 的开发板必须添加开发板覆盖层：

  .. code-block:: devicetree

     / {
         chosen {
             zephyr,system-timer = &lptmr0;
         };
     };

  在 Kinetis KE1xF 上，启用 :kconfig:option:`CONFIG_PM` 时也需要此覆盖层。

* :dtcompatible:`nxp,imx-flexspi-nor` 兼容节点现在有一个
  :dtcompatible:`soc-nv-flash` 兼容子节点来描述闪存。
  ``nxp,imx-flexspi-nor`` 节点作为闪存控制器（重命名为 ``flash-controller@0``），
  ``erase-block-size``、``write-block-size`` 属性以及 ``partitions`` 节点
  移到闪存芯片节点中。树外开发板必须相应更新其设备树。

* ``zephyr,flash`` 选择属性必须指向 :dtcompatible:`soc-nv-flash` 兼容节点。

  * ``zephyr,flash-controller`` 选择属性必须指向
    :dtcompatible:`nxp,imx-flexspi-nor` 兼容节点。
  * 控制器节点上需要 ``ranges`` 属性。

QSPI
====

* 配置了 ``dual-flash`` 属性的 :dtcompatible:`st,stm32-qspi` 兼容节点
  现在还需要包含 ``ssht-enable`` 属性以重新启用采样移位。
  采样移位现在可配置，默认禁用。(:github:`98999`)

Radio
=====

* 为与 ``radio-`` 前缀保持一致，以下设备树绑定已重命名：

  * :dtcompatible:`generic-fem-two-ctrl-pins` 现在为 :dtcompatible:`radio-fem-two-ctrl-pins`
  * :dtcompatible:`gpio-radio-coex` 现在为 :dtcompatible:`radio-gpio-coex`

* 引入了新的 :dtcompatible:`radio.yaml` 基础绑定，用于通用无线电硬件能力。
  为保持一致，``tx-high-power-supported`` 属性已重命名为
  ``radio-tx-high-power-supported``。

* 使用旧兼容值字符串的设备树和覆盖层必须更新为使用新名称。

SD Host Controller
==================

* 根据 `SD Host Controller Specification
  <https://www.sdcard.org/downloads/pls/pdf/?p=PartA2_SD%20Host_Controller_Simplified_Specification_Ver4.20.jpg>`_，
  已将额外字段 ``bus_4_bit_support``、``hs200_support`` 和 ``hs400_support``
  从 :c:struct:`sdhc_host_caps` 移到 :c:struct:`sdhc_host_props`。
  (:github:`91701`)

Shell
=====

* :c:func:`shell_set_bypass` 现在要求传递用户数据指针。
  相应地，:c:type:`shell_bypass_cb_t` 现在有一个用户数据参数。
  (:github:`100311`)

Stepper
=======

* 对于 :dtcompatible:`adi,tmc2209`，属性 ``msx-gpios`` 现在替换为
  ``m0-gpios`` 和 ``m1-gpios``，以与其他 step/dir 步进器驱动保持一致。

* 多个 API 函数已重命名：

  * ``stepper_move_by`` 改为 :c:func:`stepper_ctrl_move_by`。
  * ``stepper_move_to`` 改为 :c:func:`stepper_ctrl_move_to`。
  * ``stepper_is_moving`` 改为 :c:func:`stepper_ctrl_is_moving`。
  * ``stepper_run`` 改为 :c:func:`stepper_ctrl_run`。
  * ``stepper_stop`` 改为 :c:func:`stepper_ctrl_stop`。
  * ``stepper_set_reference_position`` 改为 :c:func:`stepper_ctrl_set_reference_position`。
  * ``stepper_get_actual_position`` 改为 :c:func:`stepper_ctrl_get_actual_position`。
  * ``stepper_set_microstep_interval`` 改为 :c:func:`stepper_ctrl_set_microstep_interval`。

* 以下事件已从 :c:enum:`stepper_event` 移到 :c:enum:`stepper_ctrl_event`：

  * ``STEPPER_EVENT_STEPS_COMPLETED`` 改为 ``STEPPER_CTRL_EVENT_STEPS_COMPLETED``。
  * ``STEPPER_EVENT_LEFT_END_STOP_DETECTED`` 改为
    ``STEPPER_CTRL_EVENT_LEFT_END_STOP_DETECTED``。
  * ``STEPPER_EVENT_RIGHT_END_STOP_DETECTED`` 改为
    ``STEPPER_CTRL_EVENT_RIGHT_END_STOP_DETECTED``。
  * ``STEPPER_EVENT_STOPPED`` 改为 ``STEPPER_CTRL_EVENT_STOPPED``。

* 已从所有 step-dir 步进器硬件驱动器件（:dtcompatible:`adi,tmc2209`、
  :dtcompatible:`ti,drv84xx` 和 :dtcompatible:`allegro,a4979`）的绑定中移除
  ``step-gpios``、``dir-gpios``、``invert-direction`` 和 ``counter`` 属性，
  并移到新的通用步进器运动控制器绑定 :dtcompatible:`zephyr,gpio-step-dir-stepper-ctrl`。

* 现在必须通过 :dtcompatible:`zephyr,gpio-step-dir-stepper-ctrl` 器件执行运动控制，
  该器件通过 ``stepper-driver`` 属性引用步进器硬件驱动设备树节点。
  应用必须更新其设备树以添加运动控制器节点，并使用 ``stepper_ctrl_*`` API，
  而不是直接在步进器硬件驱动器件上调用运动控制函数。

* 已从 H 桥步进器控制器中移除步进器硬件驱动特定 API：

  * :dtcompatible:`zephyr,h-bridge-stepper` 重命名为
    :dtcompatible:`zephyr,h-bridge-stepper-ctrl`，
    以反映它是步进器运动控制器绑定，而不是步进器硬件驱动绑定。

  * :c:func:`stepper_enable`、:c:func:`stepper_disable`、
    :c:func:`stepper_set_micro_step_res` 和 :c:func:`stepper_get_micro_step_res`
    API 函数不再可用于 :dtcompatible:`zephyr,h-bridge-stepper-ctrl` 兼容器件。

  * 已从 :dtcompatible:`zephyr,h-bridge-stepper-ctrl` 中移除 ``en-gpios`` 属性。

  * :dtcompatible:`zephyr,h-bridge-stepper-ctrl` 中的 ``micro-step-res`` 属性
    已替换为 ``lut-step-gap``，以更好地反映 H 桥控制机制，
    该机制使用查找表插值而不是硬件微步进。

  使用 H 桥步进器控制器的应用必须：

  1. 移除 H 桥控制器器件上对步进器硬件驱动特定 API 的调用
  2. 更新设备树以使用 ``lut-step-gap`` 而不是 ``micro-step-res``
  3. 如果存在，移除 ``en-gpios`` 属性

* :dtcompatible:`adi,tmc50xx` 和 :dtcompatible:`adi,tmc51xx` 器件现在建模为 MFD。

* 已移除用于生成 :kconfig:option:`CONFIG_STEPPER_*_GENERATE_ISR_SAFE_EVENTS` 和
  :kconfig:option:`CONFIG_STEPPER_*_EVENT_QUEUE_LEN` 符号的
  Kconfig.stepper_event_template 模板。

* :kconfig:option:`CONFIG_STEPPER_STEP_DIR_GENERATE_ISR_SAFE_EVENTS`
  替换为 :kconfig:option:`CONFIG_STEPPER_CTRL_ISR_SAFE_EVENTS`

* :kconfig:option:`CONFIG_STEPPER_STEP_DIR_EVENT_QUEUE_LEN`
  替换为 :kconfig:option:`CONFIG_STEPPER_CTRL_EVENT_QUEUE_LEN`

* :kconfig:option:`CONFIG_STEPPER_CTRL_ISR_SAFE_EVENTS` 现在默认启用

STM32
=====

* STM32 电源配置现在使用设备树属性执行。
  引入了新绑定 :dtcompatible:`st,stm32h7-pwr`、:dtcompatible:`st,stm32h7rs-pwr`
  和 :dtcompatible:`st,stm32-dualreg-pwr`，
  并移除了所有与电源配置相关的 Kconfig 符号：

  * ``CONFIG_POWER_SUPPLY_LDO``

  * ``CONFIG_POWER_SUPPLY_DIRECT_SMPS``

  * ``CONFIG_POWER_SUPPLY_SMPS_1V8_SUPPLIES_LDO``

  * ``CONFIG_POWER_SUPPLY_SMPS_2V5_SUPPLIES_LDO``

  * ``CONFIG_POWER_SUPPLY_SMPS_1V8_SUPPLIES_EXT_AND_LDO``

  * ``CONFIG_POWER_SUPPLY_SMPS_2V5_SUPPLIES_EXT_AND_LDO``

  * ``CONFIG_POWER_SUPPLY_SMPS_1V8_SUPPLIES_EXT``

  * ``CONFIG_POWER_SUPPLY_SMPS_2V5_SUPPLIES_EXT``

  * ``CONFIG_POWER_SUPPLY_EXTERNAL_SOURCE``

* ST 特定选择属性 ``/chosen/zephyr,ccm`` 替换为 ``/chosen/zephyr,dtcm``。
  属性宏 ``__ccm_data_section``、``__ccm_bss_section`` 和 ``__ccm_noinit_section``
  已弃用，但为向后兼容而保留；**它们将在 Zephyr 4.5 中移除**。
  应改用通用 ``__dtcm_{data,bss,noinit}_section`` 宏。(:github:`100590`)

* STM32 平台现在使用默认 MCUboot 运行模式 ``swap using offset``
  （:kconfig:option:`SB_CONFIG_MCUBOOT_MODE_SWAP_USING_OFFSET`）。
  为支持此引导加载程序模式，需要对开发板设备树进行一些更改。
  多个开发板已支持此模式（参见 :github:`100385`）。
  之前的 ``swap using move`` 模式仍可在 sysbuild 中通过启用
  :kconfig:option:`SB_CONFIG_MCUBOOT_MODE_SWAP_USING_MOVE` 选择。

* 对于 STM32F2x/F4x/F7x，不同的 PLL 绑定（:dtcompatible:`st,stm32f2-pll-clock`、
  :dtcompatible:`st,stm32f4-pll-clock`、:dtcompatible:`st,stm32f4-plli2s-clock`、
  :dtcompatible:`st,stm32f411-plli2s-clock`、:dtcompatible:`st,stm32f7-pll-clock`
  和 :dtcompatible:`st,stm32fx-pllsai-clock`）已合并为单一的
  :dtcompatible:`st,stm32fx-pll-clock`。此合并带来一些更改，
  特别是 ``div-divq`` 和 ``div-divr`` 属性已分别重命名为
  ``post-div-q`` 和 ``post-div-r``。此外，当适用于 SoC 时，
  如果使用相应的 ``div-q`` 或 ``div-r`` 属性，则需要定义这些属性。

* 对于 STM32L4x，:dtcompatible:`st,stm32l4-pllsai-clock` 绑定
  已替换为现有的 :dtcompatible:`st,stm32l4-pll-clock`。
  此替换带来 ``div-divr`` 属性重命名为 ``post-div-r``。

* STM32 平台中 :zephyr_file:`drivers/ethernet/eth_stm32_hal_common.c`
  的 MAC 地址生成现在在使用以下属性之一于 MAC 设备树节点时使用
  :c:struct:`net_eth_mac_config`：

  * ``zephyr,random-mac-address``（a）
  * ``local-mac-address``（b）
  * ``nvmem-cells``（c）（新）

  这会导致使用（a）或（b）属性的实现出现向后兼容性问题。
  之前使用这些属性的 DT 实现将 ST OUI 的前 3 个 MSB
  与 MAC 地址后 3 个 LSB 的随机（a）或显式（b）位混合。
  现在，MAC 地址完全随机（a），或完全或部分写在设备树中（b）。

  新实现（c）允许引用存储在非易失性存储器中的 MAC 地址。
  例如：管理 STM32N6x 平台上 :abbr:`OTP(One Time Programmable)` 熔丝的 BSEC 外设。
  更多细节参见 :c:func:`net_eth_mac_load`。

  当 MAC 节点中未指定这些属性中的任何一个时，使用传统实现。
  (:github:`102810`)

  .. note:: 此更改使 STM32 平台的行为与 Zephyr 通用行为一致。
            之前的实现未达产品就绪状态，因此不应造成太大麻烦。

* 已移除 Kconfig 选项 ``CONFIG_SPI_STM32_USE_HW_SS``。
  SPI 操作模式现在基于设备树配置自动选择：具有 ``cs-gpios``
  或新 ``st,soft-nss`` 属性之一的实例以“Soft NSS”模式运行，
  而所有其他实例以“Hard NSS”模式运行。

* 为确保 SPI 在任何频率下都能工作，所有 SPI 引脚现在默认配置为
  ``very-high-speed`` 摆率。这可能导致功耗增加。
  可以在开发板 dts 或覆盖层中覆盖摆率值为更慢的速度，
  以降低功耗。

* :kconfig:option:`CONFIG_NUM_IRQS` 现在基于活动（``status = "okay";``）器件
  使用新的 ``dt_highest_controller_irq_number`` Kconfig 预处理器函数自动计算。
  注册自定义 ISR（使用 :c:macro:`IRQ_CONNECT()`）的应用可能因
  :kconfig:option:`CONFIG_NUM_IRQS` 值较低而遇到如下构建失败：

  .. code-block::

     gen_isr_tables.py: error: IRQ 114 (offset=0) exceeds the maximum of 106

  显式将 :kconfig:option:`CONFIG_NUM_IRQS` 设置为适当值以解决这些问题。
  （:ref:`以下文档页 <setting_configuration_values>` 解释了如何操作）

Timer
=====

* 通过兼容宏 ``z_cms_lptim_hook_on_lpm_entry`` 和 ``z_cms_lptim_hook_on_lpm_exit``
  实现传统 Cortex-M SysTick 低功耗伴随接口的树外 SoC 或平台代码
  应迁移到 :zephyr_file:`include/zephyr/drivers/timer/system_timer_lpm.h` 中的
  :c:func:`z_sys_clock_lpm_enter` 和 :c:func:`z_sys_clock_lpm_exit`。
  :zephyr_file:`drivers/timer/cortex_m_systick.h` 中的兼容垫片
  在 Zephyr 4.4.0 中已弃用，目前计划在 Zephyr 4.6.0 中移除。
  传统 Kconfig 选项：
  :kconfig:option:`CONFIG_CORTEX_M_SYSTICK_LPM_TIMER_NONE`、
  :kconfig:option:`CONFIG_CORTEX_M_SYSTICK_LPM_TIMER_COUNTER`、
  :kconfig:option:`CONFIG_CORTEX_M_SYSTICK_LPM_TIMER_HOOKS` 和
  :kconfig:option:`CONFIG_CORTEX_M_SYSTICK_RESET_BY_LPM` 也已弃用。
  选择属性 ``/chosen/zephyr,cortex-m-idle-timer`` 已弃用，
  改用 ``/chosen/zephyr,system-timer-companion``。
  迁移到 :kconfig:option:`CONFIG_SYSTEM_TIMER_LPM_COMPANION_NONE`、
  :kconfig:option:`CONFIG_SYSTEM_TIMER_LPM_COMPANION_COUNTER`、
  :kconfig:option:`CONFIG_SYSTEM_TIMER_LPM_COMPANION_HOOKS` 和
  :kconfig:option:`CONFIG_SYSTEM_TIMER_RESET_BY_LPM`。

* :dtcompatible:`renesas,rza2m-ostm` 名称已替换为
  :dtcompatible:`renesas,rza2m-ostm-timer`。
  选择 :kconfig:option:`DT_HAS_RENESAS_RZA2M_OSTM_ENABLED`
  已替换为 :kconfig:option:`DT_HAS_RENESAS_RZA2M_OSTM_TIMER_ENABLED`
  (:github:`100934`)

USB
===

* :dtcompatible:`maxim,max3421e_spi` 已重命名为 :dtcompatible:`maxim,max3421e-spi`。
* USB 控制传输缓冲区分配已从 UDC 移到 USB device_next。
  树外 UDC 驱动必须重构。(:github:`103493`)

* UVC 器件应用 API 已修改：

  * ``uvc_set_video_dev`` 已重命名为 :c:func:`uvc_device_init`
  * ``uvc_add_format`` 已重命名为 :c:func:`uvc_device_add_format`
  * 引入了 :c:func:`uvc_device_enable`
  * 引入了 :c:func:`uvc_device_shutdown`

USB-C
=====

* 已从 :c:struct:`tcpc_driver_api` 结构中移除 ``alert_handler_cb`` 字段，
  因为它未使用且与通过 :c:func:`tcpc_set_alert_handler_cb` 注册的回调冗余。

Video
=====

* ``CONFIG_VIDEO_HIMAX_HM01B0`` 已重命名为 :kconfig:option:`CONFIG_VIDEO_HM01B0`。
* ``CONFIG_VIDEO_OV7670`` 现已移除，替换为
  :kconfig:option:`CONFIG_VIDEO_OV767X`。这允许同时支持 OV7670
  和 OV7675。
* :kconfig:option:`CONFIG_VIDEO_BUFFER_POOL_SZ_MAX` 替换为
  :kconfig:option:`CONFIG_VIDEO_BUFFER_POOL_HEAP_SIZE`，
  表示为整个视频缓冲区池分配的字节大小。

* :dtcompatible:`ovti,ov2640` 复位引脚处理已修正，
  导致与之前相比活动电平反转，以匹配传感器期望的活动电平。

* 为与数据保持一致，以下像素格式已重命名 (:github:`105522`)：

  * :c:macro:`VIDEO_PIX_FMT_ARGB32`（与 :c:macro:`VIDEO_PIX_FMT_BGRA32` 交换）
  * :c:macro:`VIDEO_PIX_FMT_BGRA32`（与 :c:macro:`VIDEO_PIX_FMT_ARGB32` 交换）
  * :c:macro:`VIDEO_PIX_FMT_RGBA32`（未更改）
  * :c:macro:`VIDEO_PIX_FMT_ABGR32`（未更改）
  * :c:macro:`VIDEO_PIX_FMT_XRGB32`（未更改）
  * :c:macro:`VIDEO_PIX_FMT_XBGR32`（新引入）
  * :c:macro:`VIDEO_PIX_FMT_BGRX32`（新引入）
  * :c:macro:`VIDEO_PIX_FMT_RGBX32`（新引入）

Watchdog
========

* 已澄清 :kconfig:option:`CONFIG_WDT_DISABLE_AT_BOOT` 的语义：
  当 ``CONFIG_WDT_DISABLE_AT_BOOT=n`` 时期望的行为
  之前不明确且在各驱动中实现不一致，现在已在
  :kconfig:option:`CONFIG_WDT_DISABLE_AT_BOOT` 的描述中明确记录
  （更多细节参见该描述）。

  所有树内看门狗驱动已更新以遵循现在已记录的语义。

  特别是，``CONFIG_WDT_DISABLE_AT_BOOT=n`` 不再能用于
  “自动”在启动时启用看门狗。依赖此行为的用户必须更新其应用
  以显式配置看门狗，如 :zephyr:code-sample:`watchdog` 中所做。
  已移除与此错误用法相关的以下 Kconfig 选项：

  * ``CONFIG_IWDG_STM32_INITIAL_TIMEOUT``
  * ``CONFIG_WDT_RPI_PICO_INITIAL_TIMEOUT``
  * ``CONFIG_WDT_CC13XX_CC26XX_INITIAL_TIMEOUT``
  * ``CONFIG_WDT_CC23X0_INITIAL_TIMEOUT``
  * ``CONFIG_WDT_CC32XX_INITIAL_TIMEOUT``

* 更新了 :dtcompatible:`microchip,xec-watchdog` 的 PCR 和 GIRQ 属性，
  使用新宏 (:github:`105668`)。

.. zephyr-keep-sorted-stop

Bluetooth
*********

Bluetooth Host
=============

* :kconfig:option:`CONFIG_BT_SIGNING` 已弃用。
* :c:macro:`BT_GATT_CHRC_AUTH` 已弃用。
* :c:member:`bt_conn_le_info.interval` 已弃用。
  请改用 :c:member:`bt_conn_le_info.interval_us`。
  注意单位已更改：``interval`` 以 1.25 毫秒为单位，
  而 ``interval_us`` 以微秒为单位。
* 根据蓝牙核心规范 v6.2，使用密码输入方法的传统蓝牙 LE 配对
  不再提供经过身份验证（MITM）保护。
  使用此方法生成并存储的绑定在从持久存储加载时
  将降级为未经验证，导致较低的安全级别。
* 蓝牙主机不再依赖 :c:func:`k_poll`，因此不再选择
  :kconfig:option:`CONFIG_POLL`。如果应用代码本身依赖此项，
  需要在配置中显式启用 :kconfig:option:`CONFIG_POLL`。
* 将 :kconfig:option:`CONFIG_DEVICE_NAME_GATT_WRITABLE_NONE` 的任何用法
  替换为 :kconfig:option:`CONFIG_BT_DEVICE_NAME_GATT_WRITABLE_NONE`。
* 将 :kconfig:option:`CONFIG_DEVICE_NAME_GATT_WRITABLE_ENCRYPT` 的任何用法
  替换为 :kconfig:option:`CONFIG_BT_DEVICE_NAME_GATT_WRITABLE_ENCRYPT`。
* 将 :kconfig:option:`CONFIG_DEVICE_NAME_GATT_WRITABLE_AUTHEN` 的任何用法
  替换为 :kconfig:option:`CONFIG_BT_DEVICE_NAME_GATT_WRITABLE_AUTHEN`。
* 将 :kconfig:option:`CONFIG_DEVICE_APPEARANCE_GATT_WRITABLE_AUTHEN` 的任何用法
  替换为 :kconfig:option:`CONFIG_BT_DEVICE_APPEARANCE_GATT_WRITABLE_AUTHEN`。
* 已从 :c:struct:`bt_iso_chan` 中移除 ``required_sec_level`` 字段。
  需要为 CIS 连接设置安全性的应用应在调用
  :c:func:`bt_iso_chan_connect` 之前在 ACL 连接上调用
  :c:func:`bt_conn_set_security`。
* 已从 :c:struct:`bt_iso_server` 中移除 ``sec_level`` 字段。

Bluetooth Audio
==============

* :c:func:`bt_bap_broadcast_assistant_discover` 现在不再在流程末尾
  执行对远端 BASS 接收状态的读取。用户必须手动调用
  :c:func:`bt_bap_broadcast_assistant_read_recv_state`
  读取现有接收状态（如有），然后再执行任何操作。(:github:`91587`)
* :kconfig:option:`CONFIG_BT_AUDIO` 现在依赖 :kconfig:option:`CONFIG_UTF8`。
  启用 :kconfig:option:`CONFIG_BT_AUDIO` 的应用还必须启用
  :kconfig:option:`CONFIG_UTF8`。(:github:`102350`)
* :c:func:`bt_tbs_set_uri_scheme_list` 现在只接受单个字符串值，
  而不是 URI 列表/数组。应用需要修改当前输入，
  例如从 ``{"tel", "skype"}`` 改为 ``"tel,skype"``。(:github:`102724`)
* 已移除 ``CONFIG_BT_TBS_SUPPORTED_FEATURES``。
  应用应使用已定义的宏 :c:macro:`BT_TBS_FEATURE_HOLD` 和
  :c:macro:`BT_TBS_FEATURE_JOIN` 设置其支持的特性。(:github:`102666`)
* :c:func:`bt_bap_unicast_server_foreach_ep` 和 :c:func:`bt_has_preset_foreach`
  现在可能返回错误，如果迭代提前停止或提供了无效参数。(:github:`105462`)
* :c:func:`bt_bap_unicast_server_foreach_ep`、
  :c:func:`bt_bap_unicast_group_foreach_stream`、
  :c:func:`bt_bap_broadcast_source_foreach_stream`、
  :c:func:`bt_cap_unicast_group_foreach_stream`、
  :c:func:`bt_cap_initiator_broadcast_foreach_stream`
  和 :c:func:`bt_has_preset_foreach` 的回调现在返回 ``true``
  以继续迭代，返回 ``false`` 以停止迭代。
  这些函数的任何回调都需要更新以反映新的返回类型和值。
  (:github:`105462`)

Bluetooth Mesh
=============

* :kconfig:option:`CONFIG_BT_MESH_MODEL_VND_MSG_CID_FORCE` 已弃用。
  启用它不再对消息处理性能有任何影响。

Bluetooth HCI
============

* 使用 :c:macro:`BT_HCI_LE_SUPERVISION_TIMEOUT_MIN` 和
  :c:macro:`BT_HCI_LE_SUPERVISION_TIMEOUT_MAX` 而不是
  :c:macro:`BT_HCI_LE_SUPERVISON_TIMEOUT_MIN` 和
  :c:macro:`BT_HCI_LE_SUPERVISON_TIMEOUT_MAX`，
  因为后者因拼写错误已弃用。

Networking
**********

Wi-Fi
=====

* :c:struct:`wifi_channel_info` 增加了用于 set-channel 的 ``band`` 字段。
  对于 2.4 GHz（频道 1–14）和 5 GHz（36–165），行为向后兼容：
  省略或将 ``band`` 保留为 :c:macro:`WIFI_FREQ_BAND_UNKNOWN`，
  驱动将推断频段。对于 6 GHz，将 ``band`` 设置为
  :c:macro:`WIFI_FREQ_BAND_6_GHZ`（频道号与 2.4 GHz 的 1–14 重叠）。
  重新编译以使调用 net_mgmt 时 ``sizeof(struct wifi_channel_info)`` 正确。

* WPA3 通过选择 ``WIFI_NM_WPA_SUPPLICANT_WPA3_IMPLEMENTATION``
  配置（Internal、External 或 None）。
  将 ``prj.conf`` 中任何 ``CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3=y`` 行
  替换为 ``CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3_IMPLEMENTATION_INT=y``
  （或根据需要替换为 ``_EXT`` / ``_NONE``）。
  :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3`
  现在无提示，仅在选择 Internal 时选中；不要直接赋值。
  在 C 代码中，优先使用 :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_WPA3_COMMON`
  检测内部或外部 WPA3。

* 在以下文件中找到的网络 API

  * :zephyr_file:`include/zephyr/net/net_ip.h`
  * :zephyr_file:`include/zephyr/net/socket.h`

  以及 ``subsys/net`` 等相关代码已命名空间化。
  这意味着网络 API 名称添加了 ``net_``、``NET_`` 或 ``ZSOCK_`` 前缀。
  这样做是为了避免与可能定义相同符号的 POSIX 或 libc 的循环依赖。
  创建了兼容头文件 :zephyr_file:`include/zephyr/net/net_compat.h`，
  提供旧符号，允许用户继续使用旧符号。
  外部网络应用可继续使用 POSIX 定义的网络符号，
  并包含相关 POSIX 头文件（如 ``sys/socket.h``）获取 POSIX 符号，
  因为 Zephyr 网络头文件不再包含它们。
  如果应用或 Zephyr 内部代码无法使用 POSIX API，
  则需要在调用网络 API 的代码中添加相关网络 API 前缀。

* :c:type:`net_icmp_handler_t` 的返回类型已从 ``int`` 更改为
  :c:enum:`net_verdict`。(:github:`104815`)

* HTTP 服务器事务状态枚举已从 ``http_data_status`` 重命名为
  ``http_transaction_status``，以更好地反映其用途。
  枚举值也已重命名如下：

  - ``HTTP_SERVER_DATA_ABORTED`` → ``HTTP_SERVER_TRANSACTION_ABORTED``
  - ``HTTP_SERVER_DATA_MORE`` → ``HTTP_SERVER_REQUEST_DATA_MORE``
  - ``HTTP_SERVER_DATA_FINAL`` → ``HTTP_SERVER_REQUEST_DATA_FINAL``

  动态资源的手动回调类型已相应更新，以使用新枚举及其重命名值。
  使用动态 HTTP 资源的应用必须更新其手动回调以使用新枚举
  并处理重命名值。

* HTTP 服务器现在在响应完全发送到客户端时
  为动态资源报告 ``HTTP_SERVER_TRANSACTION_COMPLETE`` 状态。
  应用现在还应在手动回调中处理此状态，
  以在成功响应传输后正确重置资源状态。

* 创建安全套接字时传递给 :c:func:`zsock_socket` 的协议版本
  现在强制作为 TLS 会话使用的最低 TLS 版本。

* 已从 :kconfig:option:`NET_SOCKETS_SOCKOPT_TLS` 中移除
  加密 Kconfig 的自动选择，因为它们强烈依赖最终应用的需求。
  因此，必须显式选择期望的 TLS 协议版本和密码套件。
  可用的 :kconfig:option-regex:`CONFIG_MBEDTLS_CIPHERSUITE_TLS_.*`
  Kconfig 助手可用于自动启用给定密码套件的所有依赖项，
  可按需按相同模式添加更多。

CoAP
====

* CoAP ``.well-known/core`` 响应的资源相关元数据
  现在使用专用的 :c:member:`coap_resource.metadata` 指针配置，
  而不是 :c:member:`coap_resource.user_data`，
  后者应保留供应用专用使用。
  实现 CoAP ``.well-known/core`` 处理的应用应更新为使用新指针。

* 已移除 ``COAP_RESPONSE_CODE_OK`` 2.00 响应码定义，
  因为它不是有效响应码——未在 :rfc:`7252` 中定义，
  也未在 IANA 注册表中分配
  (https://www.iana.org/assignments/core-parameters/core-parameters.xhtml#response-codes)。

Modem
*****

Modem HL78XX
============

* 与 HL78XX 启动时序相关的 Kconfig 选项已在
  :kconfig:option:`CONFIG_MODEM_HL78XX_DEV_*` 中重命名如下：

  - ``MODEM_HL78XX_DEV_POWER_PULSE_DURATION`` →
    ``MODEM_HL78XX_DEV_POWER_PULSE_DURATION_MS``
  - ``MODEM_HL78XX_DEV_RESET_PULSE_DURATION`` →
    ``MODEM_HL78XX_DEV_RESET_PULSE_DURATION_MS``
  - ``MODEM_HL78XX_DEV_STARTUP_TIME`` →
    ``MODEM_HL78XX_DEV_STARTUP_TIME_MS``
  - ``MODEM_HL78XX_DEV_SHUTDOWN_TIME`` →
    ``MODEM_HL78XX_DEV_SHUTDOWN_TIME_MS``

* 默认启动时序已从 1000 ms 更改为 120 ms，
  以提高所有支持开发板上的初始化可靠性。

  依赖之前默认值的应用必须更新其配置。

LoRaWAN
*******

* LoRaWAN 区域 Kconfig 符号已从 ``LORAMAC_REGION_*`` 重命名为
  ``LORAWAN_REGION_*`，以使其与后端无关。
  使用以下任何符号的应用必须更新其配置文件：

  * ``CONFIG_LORAMAC_REGION_AS923`` → :kconfig:option:`CONFIG_LORAWAN_REGION_AS923`
  * ``CONFIG_LORAMAC_REGION_AU915`` → :kconfig:option:`CONFIG_LORAWAN_REGION_AU915`
  * ``CONFIG_LORAMAC_REGION_CN470`` → :kconfig:option:`CONFIG_LORAWAN_REGION_CN470`
  * ``CONFIG_LORAMAC_REGION_CN779`` → :kconfig:option:`CONFIG_LORAWAN_REGION_CN779`
  * ``CONFIG_LORAMAC_REGION_EU433`` → :kconfig:option:`CONFIG_LORAWAN_REGION_EU433`
  * ``CONFIG_LORAMAC_REGION_EU868`` → :kconfig:option:`CONFIG_LORAWAN_REGION_EU868`
  * ``CONFIG_LORAMAC_REGION_KR920`` → :kconfig:option:`CONFIG_LORAWAN_REGION_KR920`
  * ``CONFIG_LORAMAC_REGION_IN865`` → :kconfig:option:`CONFIG_LORAWAN_REGION_IN865`
  * ``CONFIG_LORAMAC_REGION_US915`` → :kconfig:option:`CONFIG_LORAWAN_REGION_US915`
  * ``CONFIG_LORAMAC_REGION_RU864`` → :kconfig:option:`CONFIG_LORAWAN_REGION_RU864`

Other subsystems
****************

CFB
===

* 更改为使用有符号值表示坐标。
  因此，:c:func:`cfb_print`、:c:func:`cfb_invert_area`
  和 :c:struct:`cfb_position` 定义已更改。

* DAP 子系统的初始化和配置已更改。
  请查看 :zephyr:code-sample:`cmsis-dap` 示例，
  了解如何使用 USB 后端初始化 Zephyr DAP Link。

* Cache

  * 使用 :kconfig:option:`CONFIG_CACHE_HAS_MIRRORED_MEMORY_REGIONS`
    而不是 :kconfig:option:`CONFIG_CACHE_DOUBLEMAP`，
    因为前者更能描述该功能。

Flash
=====

* 之前弃用的 ``CONFIG_FLASH_AREA_CHECK_INTEGRITY_MBEDTLS``
  现已移除。

* 由于现在加密库后端没有替代方案，
  ``CONFIG_FLASH_AREA_CHECK_INTEGRITY_PSA`` 也已移除。

* 闪存 shell 命令 ``flash erase`` 和 ``flash write``
  现在要求显式器件参数。这避免了意外损坏器件的程序闪存。

Flash map
=========

* 以下 :zephyr_file:`include/zephyr/storage/flash_map.h` 宏
  已弃用并替换：

  +-----------------------------------------+-----------------------------------+
  | 弃用宏                                  | 替换宏                            |
  +=========================================+===================================+
  | :c:macro:`FIXED_PARTITION_EXISTS`       | :c:macro:`PARTITION_EXISTS`       |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_ID`           | :c:macro:`PARTITION_ID`           |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_OFFSET`       | :c:macro:`PARTITION_OFFSET`       |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_ADDRESS`      | :c:macro:`PARTITION_ADDRESS`      |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_NODE_ADDRESS` | :c:macro:`PARTITION_NODE_ADDRESS` |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_NODE_OFFSET`  | :c:macro:`PARTITION_NODE_OFFSET`  |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_SIZE`         | :c:macro:`PARTITION_SIZE`         |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_NODE_SIZE`    | :c:macro:`PARTITION_NODE_SIZE`    |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_DEVICE`       | :c:macro:`PARTITION_DEVICE`       |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_NODE_DEVICE`  | :c:macro:`PARTITION_NODE_DEVICE`  |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_MTD`          | :c:macro:`PARTITION_MTD`          |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_NODE_MTD`     | :c:macro:`PARTITION_NODE_MTD`     |
  +-----------------------------------------+-----------------------------------+
  | :c:macro:`FIXED_PARTITION_BY_NODE`      | :c:macro:`PARTITION_BY_NODE`      |
  +-----------------------------------------+-----------------------------------+

  这些新宏还添加了对 :dtcompatible:`zephyr,mapped-partition` 绑定的支持。

JWT
===

* 之前弃用的 ``CONFIG_JWT_SIGN_RSA_LEGACY`` 已移除。
  此移除发生在通常的 2 个发布周期的弃用期之前，
  因为已达成一致（参见 :github:`97660`）Mbed TLS 是外部模块，
  因此正常弃用规则在此情况下不适用。

Libsbc
======

* Libsbc（sbc.c 和 sbc.h）已移到蓝牙子系统中。
  sbc.h 现在位于 include/zephyr/bluetooth 中。

Management
==========

* hawkBit

  * 已移除弃用的 Kconfig 选项 ``CONFIG_HAWKBIT_DDI_NO_SECURITY``。
    (:github:`105150`)

* MCUmgr

  * 如果使用 :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_UART`，
    则现在还必须选择 :kconfig:option:`CONFIG_UART_MCUMGR`，
    这已从 ``select`` 更改为 ``depends on``。

Random
======

* ``CONFIG_CSPRNG_AVAILABLE`` 已重命名为
  :kconfig:option:`CONFIG_ENTROPY_NODE_ENABLED`。

Tracing
=======

* CTF：在 CTF 元数据事件头中将 uint8_t id 更改为 uint16_t id。
  这将事件 ID 使用的空间加倍，但允许 65,535 个事件而不是 255 个。

  通过此更改，具有 8 位 ID 的现有 CTF 跟踪将不兼容。

Serial
======

* pl011 UART 驱动：从 :c:func:`pl011_poll_in` 中移除
  Read Status Register（RSR）错误处理。RSR 处理已在
  :c:func:`pl011_err_check` 中实现，
  这是检测和报告接收错误条件的适当位置。(:github:`101715`)

Settings
========

* ``CONFIG_SETTINGS_TFM_ITS`` 已重命名为
  :kconfig:option:`CONFIG_SETTINGS_TFM_PSA`。

Modules
*******

HostAP
======

* Kconfig :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO_MBEDTLS_PSA`
  现在默认启用。

Mbed TLS
========

* Mbed TLS 已升级到版本 4.1.0。从现在开始，此仓库仅包含 TLS
  和 X.509，而加密支持已移到 TF-PSA-Crypto。
  为后者引入了新的 west 模块，基于上游发布 1.1.0。
  TF-M 继续使用 Mbed TLS 3.6.5 构建。
  从加密角度看，此更改引入了许多变化，
  因此强烈建议查看官方 `Mbed TLS 3.x 到 TF-PSA-Crypto 1.x 迁移指南
  <https://github.com/Mbed-TLS/TF-PSA-Crypto/blob/development/docs/1.0-migration-guide.md>`_。

* ``CONFIG_MBEDTLS_ENTROPY_POLL_ZEPHYR`` 已重命名为
  :kconfig:option:`CONFIG_MBEDTLS_PSA_DRIVER_GET_ENTROPY`。

* ``CONFIG_MBEDTLS_PEM_CERTIFICATE_FORMAT`` 已替换为其过去用于启用的
  底层选项：:kconfig:option:`CONFIG_MBEDTLS_PEM_PARSE_C`、
  :kconfig:option:`CONFIG_MBEDTLS_PEM_WRITE_C` 和
  :kconfig:option:`CONFIG_MBEDTLS_BASE64_C`。

* ``CONFIG_MBEDTLS_SERVER_NAME_INDICATION`` 已重命名为
  :kconfig:option:`CONFIG_MBEDTLS_SSL_SERVER_NAME_INDICATION`。

* ``CONFIG_MBEDTLS_TEST`` 已重命名为 :kconfig:option:`CONFIG_MBEDTLS_DEBUG_C`。

* 以下 PSA 相关 Kconfig 符号已移除，
  因为它们不再被 TF-PSA-Crypto 支持：

  * ``CONFIG_PSA_WANT_KEY_TYPE_DES``
  * ``CONFIG_PSA_WANT_ECC_SECP_R1_192``
  * ``CONFIG_PSA_WANT_ECC_SECP_K1_192``
  * ``CONFIG_PSA_WANT_ECC_SECP_R1_224``

* 以下 Mbed TLS Kconfig 符号已移除：

  * ``CONFIG_CUSTOM_MBEDTLS_CFG_FILE``
  * ``CONFIG_MBEDTLS_CHACHAPOLY_AEAD_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_AES_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_CAMELLIA_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_CCM_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_CHACHA20_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_DES_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_GCM_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_MODE_CBC_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_MODE_CTR_ENABLED``
  * ``CONFIG_MBEDTLS_CIPHER_MODE_XTS_ENABLED``
  * ``CONFIG_MBEDTLS_CMAC``
  * ``CONFIG_MBEDTLS_DHM_C``
  * ``CONFIG_MBEDTLS_ECDH_C``
  * ``CONFIG_MBEDTLS_ECDSA_C``
  * ``CONFIG_MBEDTLS_ECDSA_DETERMINISTIC``
  * ``CONFIG_MBEDTLS_ECJPAKE_C``
  * ``CONFIG_MBEDTLS_ECP_ALL_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_C``
  * ``CONFIG_MBEDTLS_ECP_DP_BP256R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_BP384R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_BP512R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_CURVE25519_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_CURVE448_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP192K1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP192R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP224K1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP224R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP256K1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP256R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP384R1_ENABLED``
  * ``CONFIG_MBEDTLS_ECP_DP_SECP521R1_ENABLED``
  * ``CONFIG_MBEDTLS_GENPRIME_ENABLED``
  * ``CONFIG_MBEDTLS_HKDF_C``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_DHE_PSK_ENABLED``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_DHE_RSA_ENABLED``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_RSA_ENABLED``
  * ``CONFIG_MBEDTLS_KEY_EXCHANGE_RSA_PSK_ENABLED``
  * ``CONFIG_MBEDTLS_MD5``
  * ``CONFIG_MBEDTLS_PKCS1_V15``
  * ``CONFIG_MBEDTLS_PKCS1_V21``
  * ``CONFIG_MBEDTLS_POLY1305``
  * ``CONFIG_MBEDTLS_RSA_C``
  * ``CONFIG_MBEDTLS_SHA1``
  * ``CONFIG_MBEDTLS_SHA224``
  * ``CONFIG_MBEDTLS_SHA256``
  * ``CONFIG_MBEDTLS_SHA384``
  * ``CONFIG_MBEDTLS_SHA512``
  * ``CONFIG_MBEDTLS_USE_PSA_CRYPTO``

OpenThread
==========

* 以下 Kconfig 选项已重命名：

  * ``CONFIG_OPENTHREAD_MBEDTLS_CHOICE`` 改为
    :kconfig:option:`CONFIG_OPENTHREAD_SECURITY_DEFAULT_CONFIG`
  * ``CONFIG_CUSTOM_OPENTHREAD_SECURITY`` 改为
    :kconfig:option:`CONFIG_OPENTHREAD_SECURITY_CUSTOM_CONFIG`

* :kconfig:option:`CONFIG_OPENTHREAD_CRYPTO_PSA` 不再依赖
  :kconfig:option:`CONFIG_PSA_CRYPTO_CLIENT`，
  而是选择 :kconfig:option:`CONFIG_PSA_CRYPTO`。

* 在没有 TF-M 的构建中，如果设置了
  :kconfig:option:`CONFIG_OPENTHREAD_SECURITY_DEFAULT_CONFIG` 和
  :kconfig:option:`CONFIG_OPENTHREAD_CRYPTO_PSA`，
  则现在自动隐含 :kconfig:option:`CONFIG_SECURE_STORAGE`。
  这保证 PSA ITS 实现可用，
  并要求配置 Secure Storage（Settings、ZMS 或自定义）后端。

* :kconfig:option:`CONFIG_OPENTHREAD_CRYPTO_PSA` 现在默认启用。

* 随着 Mbed TLS 升级到版本 4.1.0，传统加密支持
  在 Zephyr 中不再可用。因此已移除
  ``CONFIG_OPENTHREAD_CRYPTO_LEGACY_MBEDTLS_CONFIG``。
  :kconfig:option:`CONFIG_OPENTHREAD_CRYPTO_PSA_CONFIG`
  已经是加密支持的默认选择，现在是唯一支持的加密选项。

Trusted Firmware-M
==================

* ``SECURE_UART1`` TF-M 定义现在由 Zephyr 的
  :kconfig:option:`CONFIG_TFM_SECURE_UART` 控制。
  此选项将覆盖之前 TF-M 仓库中指定的任何平台值。

Architectures
*************

* 将该功能与缓存相关，因此移到缓存下，
  将 ``CONFIG_ARCH_HAS_COHERENCE`` 重命名为
  :kconfig:option:`CONFIG_CACHE_CAN_SAY_MEM_COHERENCE`。

  * 使用 :c:func:`sys_cache_is_mem_coherent`
    而不是 :c:func:`arch_mem_coherent`。

* :kconfig:option:`CONFIG_RISCV` 现在要求设备树中存在
  :dtcompatible:`riscv`。

* :dtcompatible:`riscv` 的 ``riscv,isa-base`` 和
  ``riscv,isa-extensions`` 设备树属性现在用于设置
  Base Integer Instruction Set 和 RISC-V 扩展。
  它们不再由 SoC 设置。设备树属性 ``riscv,isa``
  已弃用，改用两个新属性。(:github:`97540`)

  * ``CONFIG_SOC_CV64A6_IMAFDC`` 和 ``CONFIG_SOC_CV64A6_IMAC``
    现在合并为 :kconfig:option:`CONFIG_SOC_CV64A6`，
    因为 RISC-V 扩展现在由设备树设置。

  * :kconfig:option:`CONFIG_SOC_SERIES_AE350` 的以下选项
    已移除，因为它们现在可以通过设备树设置：

  * ``CONFIG_RV32I_CPU``
  * ``CONFIG_RV32E_CPU``
  * ``CONFIG_RV64I_CPU``
  * ``CONFIG_NO_FPU``
  * ``CONFIG_SINGLE_PRECISION_FPU``
  * ``CONFIG_DOUBLE_PRECISION_FPU``