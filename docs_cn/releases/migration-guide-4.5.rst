:orphan:

..
  参见
  https://docs.zephyrproject.org/latest/releases/index.html#migration-guides
  了解此文档应包含的内容。

.. _migration_4.5:

迁移到 Zephyr v4.5.0 的指南（工作草稿）
################################################

此文档描述从 Zephyr v4.4.0 迁移应用到 Zephyr v4.5.0 所需的更改。

任何其他更改（与迁移应用无直接关系）可在 :ref:`发布说明<zephyr_4.5>` 中查看。

.. contents::
    :local:
    :depth: 2

通用
******

* 头文件 :file:`include/zephyr/sys_clock.h` 已弃用，并将在未来版本中移除。
  应改为包含 :file:`include/zephyr/sys/clock.h`。

构建系统
************

* 现在所需的最低 CMake 版本为 3.28.0。Ubuntu 24.04 LTS 软件包仓库中提供 CMake 3.28.3。
  使用提供较旧 CMake 的发行版（例如 Ubuntu 22.04 LTS）的用户，
  可从 `Kitware APT 软件源 <https://apt.kitware.com/>`_ 或通过
  ``pip install cmake`` 获取较新版本。

* 已移除对 C17 之前 C 标准版本的支持（此前已弃用）。
  Kconfig 选项 ``CONFIG_STD_C11``、``CONFIG_STD_C99`` 和 ``CONFIG_STD_C90`` 已移除。
  编译 Zephyr 时应使用 C17 或更高版本。

* :kconfig:option:`CONFIG_LEGACY_GENERATED_INCLUDE_PATH` 已弃用且默认禁用，
  Zephyr 文件的 include 现在必须以 ``zephyr/`` 前缀开头。

* CMake 变量 ``SOC_NAME``、``SOC_SERIES``、``SOC_FAMILY`` 和 ``SOC_V2_DIR`` 已弃用，
  因为它们重复了已有变量；替代变量如下：
  :kconfig:option:`CONFIG_SOC`、:kconfig:option:`CONFIG_SOC_SERIES`、
  :kconfig:option:`CONFIG_SOC_FAMILY` 和 ``SOC_FULL_DIR``。

* ``CONFIG_BUILD_NO_GAP_FILL`` 已移除。间隙填充通过
  :kconfig:option:`CONFIG_BUILD_OUTPUT_HEX_GAP_FILL` 和
  :kconfig:option:`CONFIG_BUILD_OUTPUT_S19_GAP_FILL` 启用，因此只需删除该选项即可。

* :file:`cmake/app/boilerplate.cmake` 已移除。仍直接包含它的应用
  必须改为以 ``find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})``
  开头编写 :file:`CMakeLists.txt`。

* 命名 :file:`<board>_<revision>.conf` 的开发板修订版 Kconfig 片段
  不再被读取。应将其重命名为 :file:`<board>_<revision>_defconfig`。

* ``zephyr_code_relocate(FILES ...)`` 不再展开通配符模式，
  遇到通配符时会失败。应使用 ``file(GLOB ...)`` 展开模式，
  并传入生成的文件列表。

* 自 Zephyr 3.1 起已弃用的 ``ZephyrUnittest`` CMake 软件包已移除，
  且 ``west zephyr-export`` 不再注册它。
  应使用 ``find_package(Zephyr COMPONENTS unittest)``
  代替 ``find_package(ZephyrUnittest)``。

* ``west spdx --init`` 已弃用，并将在 Zephyr 5.0 中移除。
  带 :kconfig:option:`CONFIG_BUILD_OUTPUT_META` 的构建现在会向 CMake 请求
  ``west spdx`` 读取的文件式 API 对象模型，
  因此生成 SBOM 不再需要预先准备构建目录：照常构建，然后运行 ``west spdx``。

* CMake ``flash``、``debug``、``debugserver``、``attach`` 和 ``rtt`` 目标已移除。
  应改用 ``west flash``、``west debug``、``west debugserver``、``west attach``
  和 ``west rtt``。仿真 ``run`` 和 ``debugserver`` 目标不受影响。

* 构建系统变量 ``WEST_DIR`` 不再使用。

* :kconfig:option:`CONFIG_DEPRECATION_TEST` 已弃用，
  因为可用 :kconfig:option:`CONFIG_WARN_DEPRECATED` 代替；
  应将 ``CONFIG_DEPRECATION_TEST=y`` 的行替换为 ``CONFIG_WARN_DEPRECATED=n``。

* 加固工具的数据文件 :file:`scripts/kconfig/hardened.csv` 已由 YAML 数据库替换：
  配置文件位于 :file:`scripts/kconfig/hardening.yaml`，
  每个子系统的 ``hardening.yaml`` 片段位于相关 Kconfig 文件旁边。
  对 CSV 打过补丁的下游分支应将条目迁移到新格式（参见 :ref:`hardening`）；
  树外建议不再需要修补树内文件，
  可改为通过 ``-DHARDENCONFIG_EXTRA_SOURCES=`` 提供。
  注意 ``CONFIG_DEBUG_COREDUMP`` 在 CSV 中曾因语法错误被静默跳过；
  现在实际会被检查，因此 ``hardenconfig`` 可能将其报告为新发现。
  三个 CSV 条目被丢弃而非迁移：``CONFIG_STACK_USAGE``（仅生成构建期
  :file:`.su` 文件且不影响镜像）、``CONFIG_MPU_STACK_GUARD`` 和
  ``CONFIG_BUILTIN_STACK_GUARD``（互斥机制由
  :kconfig:option:`CONFIG_HW_STACK_PROTECTION` 仲裁——
  同时推荐两者会在带栈指针限制寄存器的核心上标记错误的一个；
  启用 :kconfig:option:`CONFIG_HW_STACK_PROTECTION` 仍被推荐，
  可让架构自行选择）。

内核
******

* ``_k_neg_eagain`` 已重命名为 ``_errno_neg_egain``，
  因为 ``errno`` 已从内核迁移到 ``lib/libc/common``。

* :c:func:`k_sem_reset` 不再唤醒等待信号量的轮询等待者。
  轮询等待者保持挂起，直到信号量可用或轮询操作超时。
  依赖 reset 唤醒轮询等待者的应用必须改用显式同步机制。

* ``CONFIG_SMP_BOOT_DELAY`` Kconfig 选项已移除。
  将次级 CPU 的启动延迟到运行期现在通过设备树按 CPU 表达：
  在 ``/cpus`` 下相应 ``cpu`` 节点（通常在开发板覆盖层中）添加
  ``zephyr,deferred-start`` 标志，
  然后像以前一样使用 :c:func:`k_smp_cpu_start` 或 :c:func:`k_smp_cpu_resume`
  稍后启动该 CPU。与被移除的选项跳过所有次级 CPU 不同，
  现在可为每个 CPU 单独选择延迟。
  注意该标志仅对设备树绑定包含 ``cpu.yaml`` 的 cpu 节点生效；
  没有此类绑定的节点无法延迟。

* 当 :kconfig:option:`CONFIG_SCHED_CPU_MASK_PIN_ONLY` 启用时，
  调用 :c:func:`k_thread_cpu_mask_clear`、:c:func:`k_thread_cpu_mask_enable_all`
  或 :c:func:`k_thread_cpu_mask_disable` 现在会触发断言，
  而不是静默产生无效状态。在 PIN_ONLY 模式下使用这些函数的应用
  必须更新为使用 :c:func:`k_thread_cpu_pin`。

* :kconfig:option:`CONFIG_SCHED_CPU_MASK` 不再限制于
  :kconfig:option:`CONFIG_SCHED_SIMPLE`。
  之前选择 ``SCHED_SCALABLE`` 或 ``SCHED_MULTIQ`` 并通过保留
  ``SCHED_SIMPLE`` 来规避亲和性限制的项目，现在可直接使用其首选后端。

* :c:func:`k_sleep` 和 :c:func:`k_usleep` 不再是独立的系统调用。
  它们现在是围绕新 :c:func:`k_sleep_ticks` 系统调用的内联封装，
  以便编译器可以折叠或丢弃其单位转换。
  它们的原型、语义和返回值不变，
  并从 :file:`include/zephyr/kernel.h` 移到新的
  :file:`include/zephyr/sleep.h`，后者被 :file:`kernel.h` 包含。
  调用它们的代码无需更改。
  树外代码若取它们的地址，或依赖 ``K_SYSCALL_K_SLEEP`` /
  ``K_SYSCALL_K_USLEEP`` 符号，需要更新。

* 内存映射函数 :c:func:`arch_mem_map` 和 :c:func:`arch_mem_unmap`
  现在在断言禁用时返回错误码，而不是停止系统。
  若断言启用，当前仍保留大多先前行为（停止系统）。

* 堆加固（heap hardening）默认启用。
  若应用需要旧行为，可显式禁用相关 Kconfig 选项。

* ``k_mem_map`` 和 ``k_mem_unmap`` 已移除。
  使用 :c:func:`sys_cache_invalidate` / :c:func:`sys_cache_flush`
  或架构特定替代方案。

开发板
******

* 树外开发板若直接包含已移动的 SoC 或开发板 DTSI 文件，
  必须更新 include 路径。
  具体移动列表参见各厂商章节。

设备树
******

* ``zephyr,mapped-partition`` 绑定现在要求 ``reg`` 属性，
  以描述分区在父设备中的地址和大小。

* ``fixed-subpartitions`` 属性已移除；
  使用 ``zephyr,mapped-partition`` 子节点表达子分区。

* :kconfig:option:`CONFIG_FLASH_CODE_PARTITION_USING_FIXED_PARTITIONS`
  已移除；代码分区现在通过设备树映射分区表达。

设备驱动与设备树
*****************

.. zephyr-keep-sorted-start re(^\w) ignorecase

ADC
===

* :dtcompatible:`renesas,ra-adc` 已重命名为 :dtcompatible:`renesas,ra-adc12`，
  新增 :dtcompatible:`renesas,ra-adc16` 用于 16 位 ADC。

* :kconfig:option:`CONFIG_ADC_MCUX_SAR_ADC` 已重命名为
  :kconfig:option:`CONFIG_ADC_NXP_SAR_ADC`，
  驱动文件 ``adc_nxp_sar_adc.c`` 已相应更新。

* :dtcompatible:`st,stm32-adc` 和 :dtcompatible:`st,adc-resolutions`
  的 ``zephyr,input-positive`` 和 ``ADC_REF_VDD_1`` 用法已更新。

Audio
=====

* 音频编解码器驱动后端 API 现在使用 :c:struct:`audio_codec_driver_api`
  代替 ``struct audio_codec_api``。
  树外音频编解码器驱动必须重命名其后端 API 结构体定义，
  并将 API 实例切换为 ``DEVICE_API(audio_codec, ...)``。
  参见 :github:`110631` 了解树内驱动如何更新的示例。
  使用 ``audio_codec_...`` API 的应用代码不受影响。

CAN
===

* 已移除 ``CONFIG_CAN_MAX_FILTER``、``CONFIG_CAN_MAX_STD_ID_FILTER``
  和 ``CONFIG_CAN_MAX_EXT_ID_FILTER`` (:github:`100596`)。
  它们由以下驱动特定 Kconfig 符号替换，其中一些默认值已提高
  以满足典型软件需求：

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

* 已将 :dtcompatible:`nxp,flexcan` 和 :dtcompatible:`nxp,flexcan-fd` 的
  Kconfig 选项 ``CONFIG_CAN_MAX_MB`` 替换为每实例的 ``number-of-mb``
  设备树属性 (:github:`99483`)。

* :dtcompatible:`nxp,flexcan` 的 ``clk-source`` 设备树属性如果存在，
  现在会自动在命名输入时钟 ``clksrc0`` 和 ``clksrc1`` 之间选择，
  用作 CAN 协议引擎时钟。

* 已将 NXP LPC 系列 MCAN 驱动 Kconfig 选项 ``CONFIG_CAN_MCUX_MCAN``
  重命名为 :kconfig:option:`CONFIG_CAN_NXP_LPC_MCAN`，
  因为该驱动并非基于 NXP MCUXpresso HAL (:github:`103679`)。

* 为 :dtcompatible:`ti,tcan4x5x` 添加了设备树属性 ``ti,nwkrq-voltage-vio``，
  用于配置 ``nWKRQ`` 引脚使用的电压轨。
  为保持之前驱动默认使用 VIO 的行为，必须设置该属性 (:github:`104182`)。

Clock Control
=============

* 已移除 Nordic Kconfig 选项 ``CONFIG_NRFS_LOCAL_DOMAIN_DVFS_SCALE_DOWN_AFTER_INIT``。
  应改用 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_HSFLL_LOCAL_REQ_LOW_FREQ`。

* :dtcompatible:`nxp,imxrt11xx-arm-pll` 绑定现在使用 ``loop-div``
  和 ``post-div`` 进行 ARM PLL 配置。
  传统 ``clock-mult`` 和 ``clock-div`` 属性仍受支持但已弃用。
  现有 RT11xx 覆盖层应使用映射
  ``loop-div = clock-mult * 2`` 和 ``post-div = clock-div`` 更新。

* SiWx91x 时钟控制已拆分为三个管理器
  （:dtcompatible:`silabs,siwx91x-cmu-aon`、:dtcompatible:`silabs,siwx91x-cmu-ulp`、
  :dtcompatible:`silabs,siwx91x-cmu-hp`）。
  传统 :dtcompatible:`silabs,siwx91x-clock` 绑定和 ``clock0`` 节点已移除。
  树外开发板和覆盖层必须将 ``clocks`` phandle 更新为匹配的 CMU，
  并使用 ``siwx91x-clock.h`` 中更新的 ``SIWX91X_CLK_*`` ID。
  例如，``clocks = <&clock0 SIWX91X_CLK_UART0>;`` 变为
  ``clocks = <&cmu_hp SIWX91X_CLK_UART0>;``。

Clock control nRF 弃用说明
-----------------------------

.. toggle::

   :ref:`clock_control_api` 驱动已为以下 nRF52、nRF53、nRF91 和 nRF54L
   系列设备上的时钟更新：

   * HFCLK
   * LFCLK
   * XO
   * XO24M
   * HFCLK192M
   * HFCLKAUDIO

   要恢复传统驱动实现，将 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF`
   设置为 ``y``。

   要将代码从 Zephyr v4.4.0 迁移到 Zephyr v4.5.0，完成以下步骤：

   1. 在应用特定或开发板特定的设备树覆盖层文件中启用每个应用控制的时钟。

      这会启用相应的时钟驱动。
      例如：

      .. code-block:: dts

         /* 如果要控制 nRF54L XO */
         &xo {
             status = "okay";
         };

         /* 如果要控制 nRF52、nRF53 HFCLK */
         &hfclk {
             status = "okay";
         };

         /* 如果要控制 nRF52、nRF53、nRF91 或 nRF54L LFCLK */
         &lfclk {
             status = "okay";
         };

         /* 如果要控制 HFCLK192M */
         &hfclk192m {
             status = "okay";
         };

         /* 如果要控制 XO24M */
         &xo24m {
             status = "okay";
         };

         /* 如果要控制 HFCLKAUDIO */
         &hfclkaudio {
             status = "okay";
         };

   #. 重命名以下 Kconfig 选项：

      * 将 :kconfig:option:`CONFIG_NRFX_CLOCK_USE_LFRC_CALIBRATION`
        替换为 :kconfig:option:`CONFIG_NRFX_CLOCK_LFCLK_USE_LFRC_CALIBRATION`。
      * 将 :kconfig:option:`CONFIG_NRFX_CLOCK_XO_CALIBRATION`
        替换为 :kconfig:option:`CONFIG_NRFX_CLOCK_XO24M_CALIBRATION`。

   #. 将代码中对 ``clock_control_...`` API 的调用更新为
      新的 :ref:`clock_control_api` API。

Counter
=======

* 实现 ``get_value_64`` API 的驱动现在需要选择
  :kconfig:option:`CONFIG_COUNTER_SUPPORTS_64BITS_TICKS`，
  应用需要 :kconfig:option:`CONFIG_COUNTER_64BITS_TICKS` 才能启用该 API。
  (:github:`94189`)

* NXP LPTMR 驱动（:dtcompatible:`nxp,lptmr`）已更新，
  修复了错误的预分频器和毛刺滤波器配置：

  * ``prescale-glitch-filter`` 属性的有效范围从 ``[0-16]`` 改为 ``[0-15]``。
    值 ``16`` 对脉冲计数器模式无效，已移除。
    使用值 ``16`` 的设备树必须更新为使用 ``[0-15]`` 范围内的值。

  * 引入了新的布尔属性 ``prescale-glitch-filter-bypass``，
    用于显式控制预分频器/毛刺滤波器旁路。
    之前，设置 ``prescale-glitch-filter = <0>`` 会隐式启用旁路模式，
    存在歧义。

    在 v4.4 及以后，旁路仅由 ``prescale-glitch-filter-bypass``
    是否存在控制。如果该属性不存在，则预分频器/毛刺滤波器处于活动状态，
    并应用 ``prescale-glitch-filter``。

  * 明确了预分频器/毛刺滤波器行为：

    * 时间计数器模式：预分频器将时钟除以 ``2^(prescale-glitch-filter + 1)``
    * 脉冲计数器模式：毛刺滤波器在 ``2^prescale-glitch-filter`` 个上升沿后
      识别变化（毛刺滤波不支持值 0）

  * 所有树内设备树节点已更新为使用 ``prescale-glitch-filter-bypass;``
    而不是 ``prescale-glitch-filter = <0>;``。
    树外开发板应相应更新。

  * 如果同时设置了 ``prescale-glitch-filter-bypass`` 和
    ``prescale-glitch-filter``，旁路模式优先，
    ``prescale-glitch-filter`` 值被忽略。

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

     在脉冲计数器模式中，``prescale-glitch-filter = <0>``
     不是受支持的毛刺滤波配置。如需请求无滤波，
     请使用 ``prescale-glitch-filter-bypass;``。

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

     驱动使用 Compare Channel 1 实现 Zephyr 计数器报警功能。
     使用 ``run-mode = "restart"`` 时，设置报警会导致计数器
     在报警比较点复位。如果应用依赖报警和连续计数，
     必须使用 ``run-mode = "free-run"``。

  .. note::

     此更改标准化了 NXP 计数器驱动运行模式配置。
     GPT 现在使用显式设备树属性而不是硬编码值，
     允许按实例自定义。

Display
=======

* 对于 ILI9XXX 控制器，设备树中用于面板颜色格式选择的
  ``ILI9XXX_PIXEL_FORMAT_x`` 用法已更新为 ``PANEL_PIXEL_FORMAT_x``。
  树外开发板和扩展板应相应更新。(:github:`99267`)

* 对于 ILI9341 控制器，显示镜像配置已更新，
  以符合示例 ``samples/drivers/display`` 中描述的行为。(:github:`99267`)
  此更改会导致某些显示面板出现镜像问题，
  将在 v4.4.1 发布中提供正式修复。(:github:`106862`)

* ``PIXEL_FORMAT_BGR_565`` 像素格式（及其对应的设备树宏
  ``PANEL_PIXEL_FORMAT_BGR_565``）已重命名为 :c:enumerator:`PIXEL_FORMAT_RGB_565X`
  （及 :c:macro:`PANEL_PIXEL_FORMAT_RGB_565X`），
  以正确反映它是 RGB-565 的字节交换版本，
  而不是交换红蓝通道的格式。(:github:`99276`)
  使用 ``PIXEL_FORMAT_BGR_565`` 表示字节交换 RGB-565 的应用和库
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

Ethernet
========

* 使用 :c:struct:`net_eth_mac_config` 的驱动 MAC 地址配置支持
  已引入以下驱动：

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
  需要启用 :kconfig:option:`CONFIG_NET_CHECKSUM_OFFLOAD`
  才能使用校验和卸载。如果选择了
  :kconfig:option:`CONFIG_NET_CHECKSUM_OFFLOAD_SUPPORTED`，则默认启用。
  (:github:`105051`)

* :dtcompatible:`microchip,lan865x` 的 ``phy-handle`` 属性
  现在必须设置为 phy 节点。

* 已移除 ``CONFIG_NET_DSA_DEPRECATED``。
  兼容值 ``microchip,ksz8463``、``microchip,ksz8794`` 和
  ``microchip,ksz8863`` 的驱动已移除，
  因为它们未迁移到新的 DSA 子系统。(:github:`105926`)

* 当通过 ``ETHERNET_CONFIG_TYPE_MAC_ADDRESS`` 更改 MAC 地址时，
  以太网驱动不再需要自行调用 :c:func:`net_if_set_link_addr`。
  (:github:`105931`)

* 使用 :c:enumerator:`ETHERNET_CONFIG_TYPE_EXTRA_TX_PKT_HEADROOM`
  请求发送包额外头部的以太网和 Wi-Fi 驱动现在必须选择
  :kconfig:option:`CONFIG_NET_L2_ETHERNET_EXTRA_TX_PKT_HEADROOM`。
  (:github:`112924`)

* ``ETHERNET_PTP`` 标志已从 :c:enum:`ethernet_hw_caps` 中移除。
  使用 :c:func:`net_eth_get_ptp_clock` 检查以太网接口是否有 PTP 时钟。
  树外驱动必须从 :c:struct:`ethernet_api` 的 ``get_capabilities``
  实现中移除对这些标志的任何引用。(:github:`112788`)

* 支持 LLDP 的以太网驱动不再需要在初始化时调用
  :c:func:`net_lldp_set_lldpdu`。现在由 :c:func:`ethernet_init` 完成。
  (:github:`114087`)

* :dtcompatible:`infineon,xmc4xxx-ethernet` 和 :dtcompatible:`wch,ethernet`
  节点已与父节点合并。同级 MDIO 节点未移动，
  因此成为这些 ``ethernet`` 节点的子节点。(:github:`114899`)

* ``infineon,xmc4xxx-mdio`` 的属性 ``mdi-port-ctrl``
  已移到父节点（:dtcompatible:`infineon,xmc4xxx-ethernet`）。
  (:github:`114899`)

* 兼容值 ``espressif,esp32-mdio``、``infineon,xmc4xxx-mdio``、
  ``nxp,enet-qos-mdio``、``nxp,s32-gmac-mdio``、``st,stm32-mdio``
  和 ``wch,mdio`` 已替换为 :dtcompatible:`snps,dwmac-mdio`。
  (:github:`114899`)

* NXP ENET-QOS 以太网控制器（:dtcompatible:`nxp,enet-qos`）
  设备树结构已扁平化，以匹配其他类似控制器。
  时钟、中断、``pinctrl-0``、``pinctrl-names``、``phy-handle``
  和 MAC 地址属性现在直接位于父 ``nxp,enet-qos`` 节点上，
  而不是单独的子 MAC 节点。``nxp,enet-qos-mac`` 兼容值
  及其 ``enet_mac`` 节点已移除。
  使用此控制器的树外开发板必须将属性从旧 ``enet_mac`` 节点
  移到 ``enet`` 节点。(:github:`115952`)

* Kconfig 选项 ``CONFIG_ETH_NXP_ENET_QOS_MAC_UNIQUE_MAC_ADDRESS``
  已重命名为 :kconfig:option:`CONFIG_ETH_NXP_ENET_QOS_UNIQUE_MAC_ADDRESS`。
  设置旧名称的配置必须更新为使用新名称。(:github:`115952`)

* Synopsys DesignWare MAC 驱动现在默认过滤多播
  （:kconfig:option:`CONFIG_ETH_DWC_ETHER_MULTICAST_FILTER`），
  因此只接收网络栈已加入地址的多播。
  禁用此选项可像以前一样接收所有多播。(:github:`113235`)

* 带以太网接口的开发板现在应默认启用
  :kconfig:option:`CONFIG_ETH_DRIVER`，
  而不是 :kconfig:option:`CONFIG_NET_L2_ETHERNET`。
  后者现在在前者启用时默认启用。(:github:`117121`)

Flash
=====

* :dtcompatible:`jedec,spi-nand` 现在要求 ``plane-bytes`` 属性，
  该属性指示闪存器件中每个平面的大小。
  对于单平面器件，应将其设置为与 ``size-bytes`` 相同的值。

* :dtcompatible:`st,stm32-nv-flash` 的属性 ``bank2-flash-size``
  已弃用，改为使用 ``reg`` 大小单元确定闪存 bank 大小。
  除移除上述属性外，设备树无需更改。(:github:`114971`)

Fuel Gauge
==========

* 各种燃料表属性枚举和联合体字段已弃用，
  改用带显式单位后缀的新版本。应用和驱动应迁移到带单位后缀的名称。
  例如，``FUEL_GAUGE_CURRENT``（``val.current``）
  替换为 ``FUEL_GAUGE_CURRENT_UA``（``val.current_ua``）。

* 驱动曾不一致地报告完整充放电循环或 ``FUEL_GAUGE_CYCLE_COUNT``
  属性中的“1/100”循环。该属性现在一致地报告完整循环，
  之前报告循环分数（即 ADP5360 和 BQ27Z746）的驱动
  已更新为报告完整循环。依赖旧行为的应用应更新。
  (:github:`112276`)

GPIO
====

* STM32 GPIO 驱动现在在尝试使用 :c:func:`gpio_pin_configure`
  配置处于禁用状态的 GPIO 引脚的上拉/下拉电阻时返回 ``-EINVAL``。
  驱动之前会返回 ``0`` 而实际不尊重这些标志
  （未启用任何 PU/PD 电阻）。遇到此错误的应用
  应从提供给 :c:func:`gpio_pin_configure` 的 ``flags`` 中移除
  :c:macro:`GPIO_PULL_UP` / :c:macro:`GPIO_PULL_DOWN`；
  这将产生与之前相同的行为，因为这些标志实际上被忽略。
  (:github:`104690`)

* 在 STM32F1 系列上，GPIO 输出引脚现在使用 50 MHz 最大速度，
  而不是 10 MHz。(:github:`104690`)

* :dtcompatible:`awinic,aw9523b-gpio` 驱动不再有 ``reset-gpios`` 属性。
  该属性已移到父 :dtcompatible:`awinic,aw9523b` MFD 设备。

Haptics
=======

* ``cirrus,cs40l5x`` 兼容值已替换为特定变体兼容值
  :dtcompatible:`cirrus,cs40l50`、:dtcompatible:`cirrus,cs40l51`、
  :dtcompatible:`cirrus,cs40l52` 和 :dtcompatible:`cirrus,cs40l53`。
  使用旧兼容值的应用必须相应更新其设备树节点。

* :dtcompatible:`ti,drv2605` 的 ``vib-rated-mv`` 和 ``vib-overdrive-mv``
  属性现在默认为器件复位值 1362 mV 和 3075 mV，而不是 3200 mV。
  需要之前驱动级别的开发板必须显式设置它们。

HWSPINLOCK
==========

* ``num-locks`` 设备树属性现在是 hwspinlock 控制器绑定的标准必需属性。
  每个 hwspinlock 控制器节点都必须设置它，
  树外绑定必须删除其自己的 ``num-locks`` ``type`` / ``required`` 声明。

* :c:func:`hw_spin_lock`、:c:func:`hw_spin_trylock` 和 :c:func:`hw_spin_unlock`
  不再接受 ``hwspinlock_ctx_t *`` 参数；
  每锁 Zephyr 自旋锁现在位于驱动配置中。
  ``struct hwspinlock_context``、``hwspinlock_ctx_t``、
  :c:struct:`hwspinlock_dt_spec` 的 ``ctx`` 成员和
  ``HWSPINLOCK_CTX_INITIALIZER`` 已移除。
  :c:func:`hw_spin_lock_dt`、:c:func:`hw_spin_trylock_dt` 和
  :c:func:`hw_spin_unlock_dt` 辅助函数不变。
  因此，所有引用同一硬件自旋锁的 :c:macro:`HWSPINLOCK_DT_SPEC_GET`
  实例现在共享单个 Zephyr 自旋锁，而不是各自拥有自己的。

* 硬件自旋锁驱动现在必须将 :c:struct:`hwspinlock_driver_config`
  嵌入其配置结构体的第一个成员，使用
  :c:macro:`HWSPINLOCK_COMMON_CONFIG_FROM_DT_INST`（或
  :c:macro:`HWSPINLOCK_COMMON_CONFIG_FROM_DT_NODE`）初始化，
  并使用 :c:macro:`HWSPINLOCK_SPINLOCK_ARRAY_DT_INST_DEFINE`（或
  :c:macro:`HWSPINLOCK_SPINLOCK_ARRAY_DT_DEFINE`）声明支持自旋锁数组。
  ``get_max_id`` 驱动操作现在可选：当未实现时，
  :c:func:`hw_spinlock_get_max_id` 默认实现
  返回 ``num-locks`` 设备树属性值减 1。

I2C
===

* 基于 :kconfig:option:`CONFIG_I2C_DW` 的控制器上，
  ``CONFIG_I2C_DW_RW_TIMEOUT_MS`` 选项已替换为
  :kconfig:option:`CONFIG_I2C_TRANSFER_TIMEOUT_MS`，默认 500 ms。

* ITE I2C 控制器 :dtcompatible:`ite,enhance-i2c`、
  :dtcompatible:`ite,it51xxx-i2c` 和 :dtcompatible:`ite,it8xxx2-i2c`
  的传输超时现在使用通用 ``zephyr,transfer-timeout-ms`` 属性，
  而不是 ``transfer-timeout-ms``，默认 500 ms。

* :dtcompatible:`nxp,sc18im704-i2c` 桥接器不再向 SC18IM704
  发送未移位的目标地址。Zephyr I2C API 向控制
  寄存器传递 7 位地址。

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

* :dtcompatible:`swerv,pic` 现在通过添加供应商前缀变为
  :dtcompatible:`cdns,swerv-pic`。

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
  必须更新移动文件的设备树包含路径。
  将形如 ``#include <nxp/nxp_*.dtsi>`` 的包含
  更新为使用正确的系列子目录。(:github:`101243`)

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
  ``zephyr,system-timer`` 选择属性指定。
  基于 i.MX95 和 MCX-W SoC 的开发板已在 SoC DTSI 中设置此项，
  无需更改。所有其他使用 :kconfig:option:`CONFIG_MCUX_LPTMR_TIMER`
  的开发板必须添加开发板覆盖层：

  .. code-block:: devicetree

     / {
         chosen {
             zephyr,system-timer = &lptmr0;
         };
     };

  在 Kinetis KE1xF 上，启用 :kconfig:option:`CONFIG_PM` 时也需要此覆盖层。

* :dtcompatible:`nxp,imx-flexspi-nor` 兼容节点现在有一个
  :dtcompatible:`soc-nv-flash` 兼容子节点来描述闪存。
  ``nxp,imx-flexspi-nor`` 节点作为闪存控制器
  （重命名为 ``flash-controller@0``），
  ``erase-block-size``、``write-block-size`` 属性以及 ``partitions`` 节点
  移到闪存芯片节点中。树外开发板必须相应更新其设备树。

* ``zephyr,flash`` 选择属性必须指向 :dtcompatible:`soc-nv-flash`
  兼容节点。

  * ``zephyr,flash-controller`` 选择属性必须指向
    :dtcompatible:`nxp,imx-flexspi-nor` 兼容节点。
  * 控制器节点上需要 ``ranges`` 属性。

PWM
===

* :dtcompatible:`microchip,xec-pwm` 的 ``pcrs`` 属性（数组类型）
  已替换为 ``pcr-scr``（int 类型），
  以使用编码 PCR 寄存器索引和位位置宏 (:github:`104570`)。

* 自 Zephyr v3.3.0 起已弃用的 STM32 PWM DT 绑定宏
  ``PWM_STM32_COMPLEMENTARY`` 不再定义。
  应改用 ``STM32_PWM_COMPLEMENTARY``。

* :dtcompatible:`nxp,ctimer-pwm` 现在通过通用
  :ref:`mux <mux_api>` 子系统路由其输入捕获信号。
  ``inputmux-connections`` 属性已移除；
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从定时器节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* :dtcompatible:`nxp,sctimer-pwm` 现在通过通用
  :ref:`mux <mux_api>` 子系统路由其输入捕获信号。
  ``input-channels`` 属性已移除；
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从定时器节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

RTC
===

* 传统基于计数器的 DS3231 驱动已移除，
  完成了 :github:`95221` 引入的弃用。
  使用 :dtcompatible:`maxim,ds3231`、``CONFIG_COUNTER_MAXIM_DS3231``
  或 :file:`<zephyr/drivers/rtc/maxim_ds3231.h>` 的应用
  必须迁移到 RTC 子系统驱动。

  将单个传统 I2C 节点替换为 :dtcompatible:`maxim,ds3231-mfd`
  父节点和 :dtcompatible:`maxim,ds3231-rtc` 子节点。
  将 ``isw-gpios`` 移到 RTC 子节点。

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
  执行对远端 BASS 接收状态的读取。
  用户必须手动调用 :c:func:`bt_bap_broadcast_assistant_read_recv_state`
  读取现有接收状态（如有），然后再执行任何操作。(:github:`91587`)
* :kconfig:option:`CONFIG_BT_AUDIO` 现在依赖 :kconfig:option:`CONFIG_UTF8`。
  启用 :kconfig:option:`CONFIG_BT_AUDIO` 的应用还必须启用
  :kconfig:option:`CONFIG_UTF8`。(:github:`102350`)
* :c:func:`bt_tbs_set_uri_scheme_list` 现在只接受单个字符串值，
  而不是 URI 列表/数组。
  应用需要修改当前输入，例如从 ``{"tel", "skype"}``
  改为 ``"tel,skype"``。(:github:`102724`)
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
  重新编译以使调用 net_mgmt 时 ``sizeof(struct wifi_status)`` 正确。

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
  ``LORAWAN_REGION_*``，以使其与后端无关。
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

* 原生 LoRaWAN 后端
  （:kconfig:option:`CONFIG_LORA_MODULE_BACKEND_NATIVE`）
  现在要求在以下运行期配置 API 被接受之前
  先调用 :c:func:`lorawan_start`：

  * :c:func:`lorawan_set_datarate` 和 :c:func:`lorawan_set_conf_msg_tries`
    如果在启动前调用返回 ``-EPERM``。
  * :c:func:`lorawan_enable_adr`（具有 ``void`` 返回类型）
    如果在启动前调用会记录警告并丢弃调用。

  之前由这些 API 在 :c:func:`lorawan_start` 之前锁存的配置值
  不再保留。在初始化期间调用它们的应用
  必须将调用移到启动之后。它们仍可在成功
  :c:func:`lorawan_join` 之前或之后运行。

  :c:func:`lorawan_set_channels_mask` 不受影响，
  在 :c:func:`lorawan_start` 之后任何时间都可调用，
  因为信道掩码影响 Join-Request 信道选择本身。

  这些顺序要求不适用于 LoRaMac-node 后端
  （:kconfig:option:`CONFIG_LORA_MODULE_BACKEND_LORAMAC_NODE`）。

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
  Read Status Register（RSR）错误处理。
  RSR 处理已在 :c:func:`pl011_err_check` 中实现，
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

* 以下已弃用的 Kconfig 选项已移除：

  * ``CONFIG_MBEDTLS_MD`` -> :kconfig:option:`CONFIG_MBEDTLS_MD_C`
  * ``CONFIG_MBEDTLS_LMS`` -> :kconfig:option:`CONFIG_MBEDTLS_LMS_C`
  * ``CONFIG_MBEDTLS_TLS_VERSION_1_2`` -> :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_TLS1_2`
  * ``CONFIG_MBEDTLS_DTLS`` -> :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_DTLS`
  * ``CONFIG_MBEDTLS_TLS_VERSION_1_3`` -> :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_TLS1_3`
  * ``CONFIG_MBEDTLS_TLS_SESSION_TICKETS`` ->
    :kconfig:option:`CONFIG_MBEDTLS_SSL_SESSION_TICKETS`
  * ``CONFIG_MBEDTLS_CTR_DRBG_ENABLED`` -> :kconfig:option:`CONFIG_MBEDTLS_CTR_DRBG_C`
  * ``CONFIG_MBEDTLS_HMAC_DRBG_ENABLED`` -> :kconfig:option:`CONFIG_MBEDTLS_HMAC_DRBG_C`

  与移除的选项不同，新选项不会自动启用其依赖项。

* :kconfig:option:`CONFIG_MBEDTLS_SSL_EARLY_DATA` 现在为显式 opt-in，
  不再由 :kconfig:option:`CONFIG_MBEDTLS_SSL_TLS1_3_KEY_EXCHANGE_MODE_PSK_ENABLED`
  隐式启用。依赖 TLS 1.3 PSK 早期数据（0-RTT）的树外应用
  或开发板配置现在必须显式启用
  :kconfig:option:`CONFIG_MBEDTLS_SSL_EARLY_DATA`。

* ``CONFIG_PSA_CRYPTO_CLIENT`` 已移除，
  因为它是 :kconfig:option:`CONFIG_PSA_CRYPTO` 的重复。
  如果之前使用它，请改用 :kconfig:option:`CONFIG_PSA_CRYPTO`。
  (:github:`108960`)

* 接口 CMake 库 ``mbedTLS`` 已重命名为 ``mbedtls_iface``。
  前者保留为后者的别名以向后兼容，但将在未来版本中移除。

* Mbed TLS 已更新到版本 4.1.1。
  发布说明可在此处查看
  `here <https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-4.1.1>`_。

* TF-PSA-Crypto 已更新到版本 1.1.1。
  发布说明可在此处查看
  `here <https://github.com/Mbed-TLS/TF-PSA-Crypto/releases/tag/tf-psa-crypto-1.1.1>`_。

Trusted Firmware-M (TF-M)
=========================

* :kconfig:option:`CONFIG_TFM_ZEPHYR_4_0_TO_4_2_COMPATIBILITY`
  已弃用，改用 :kconfig:option:`CONFIG_TFM_ZEPHYR_4_2_COMPATIBILITY`，
  后者更准确地描述了何时需要设置该符号。

* :kconfig:option:`CONFIG_BUILD_WITH_TFM` 不再启用
  :kconfig:option:`CONFIG_MBEDTLS` / :kconfig:option:`CONFIG_PSA_CRYPTO`。
  请确保在构建中按需显式启用它们。(:github:`114762`)

* :kconfig:option:`CONFIG_TFM_PARTITION_CRYPTO` 现在依赖
  :kconfig:option:`CONFIG_PSA_CRYPTO_PROVIDER_TFM`，
  意味着需要启用 :kconfig:option:`CONFIG_PSA_CRYPTO`
  才能启用 TF-M Crypto 分区。(:github:`116318`)

Architectures
*************

* 新增架构原语 ``arch_cpu_irqs_are_enabled()``。
  它返回调用 CPU 的当前中断启用状态而不修改它，
  补充检查已保存 key 的 ``arch_irq_unlocked()``。
  树外架构端口必须提供实现。

* ``CONFIG_XTENSA_MPU_ONLY_SOC_RANGES`` 已移除。
  对于 SoC 或开发板覆盖默认 MPU 区域表，
  请改为在 SoC 或开发板层覆盖 :c:var:`xtensa_mpu_ranges`。

* ``xtensa_soc_mpu_ranges[]`` 和 ``xtensa_soc_mpu_ranges_num`` 已移除。
  如果 SoC 或开发板需要在启动时拥有自己的内存区域，
  请改为覆盖 :c:var:`xtensa_mpu_ranges`。

* ``CONFIG_XTENSA_MPU_DEFAULT_MEM_TYPE`` 已移除，
  因为内存类型现在通过 ``xtensa_mpu_mem_type_ranges[]`` 定义。

* ``CONFIG_XTENSA_BACKTRACE_EXCEPTION_DUMP_HOOK`` 已移除，
  因为回溯现在始终使用 :c:macro:`EXCEPTION_DUMP` 进行输出。

* 使用 :kconfig:option:`CONFIG_XTENSA_BACKTRACE` 的 SoC
  现在预期实现 :c:func:`xtensa_soc_stack_ptr_is_sane`
  和 :c:func:`xtensa_soc_ptr_executable`。

* ARMv7-M MPU 器件类型区域属性 ``REGION_PPB_ATTR``、``REGION_IO_ATTR``
  和 ``REGION_EXTMEM_ATTR`` 现在在所有 ARMv7-M 核心上
  设置 Execute-Never（``XN=1``）。
  从 Device/Strongly-ordered 内存执行在 ARMv7-M 上架构上不可预测，
  因此没有有效用例受影响。在 Cortex-M7 上，XN 属性还防止
  向这些区域的推测性指令获取，这可能导致总线挂起
  或外设空间中的读取副作用（Arm Cortex-M7 TRM，“Speculative accesses -
  Considerations for system design”）；仅内存类型无法阻止它们。
  尽管如此仍从使用这些属性映射的区域执行的树外开发板
  必须定义自定义属性。

* 新的 :kconfig:option:`CONFIG_ARM_MPU_CM7_UNMAPPED_REGION` 选项
  使 Arm MPU 驱动将最低优先级 MPU 区域（区域 0）
  编程为 4GB Strongly-ordered、no-access、Execute-Never 的兜底，
  实现 Arm Cortex-M7 erratum 1013783（SDEN-1068427）的变通方案，
  并防止 Cortex-M7 对未映射地址的推测性访问。
  静态 MPU 区域表显式覆盖固件使用的所有内存的
  Cortex-M7 开发板或 SoC 可以启用它；
  静态区域随后从 MPU 区域 1 开始编程。
  ``mimxrt1180_evk`` 和 ``frdm_imxrt1186`` cm7 目标默认启用它，
  用相同的运行期行为替换其之前手写的 ``UNMAPPED`` MPU 区域表条目。

* ``CONFIG_SSE`` 和 ``CONFIG_SSE_FP_MATH`` 已移除。
  改用 :kconfig:option:`CONFIG_X86_SSE` 和
  :kconfig:option:`CONFIG_X86_SSE_FP_MATH`。

* ``CONFIG_PLATFORM_SPECIFIC_INIT`` 及其 ``z_arm_platform_init()``
  hook 已移除。启用 :kconfig:option:`CONFIG_SOC_RESET_HOOK`
  并将 hook 重命名为 :c:func:`soc_reset_hook`。
  新 hook 在复位路径中稍后运行，在栈指针设置之后，
  并在从 suspend-to-RAM 恢复时跳过。

* RISC-V 特定的 ``CONFIG_EXTRA_EXCEPTION_INFO`` 已移除。
  改用 :kconfig:option:`CONFIG_EXCEPTION_DEBUG`。
  该选项在 Arm 和 SPARC 上不变。

* :c:func:`arch_mem_map` 和 :c:func:`arch_mem_unmap`
  均从返回 ``void`` 更改为 ``int``，
  以便调用者在断言禁用时响应错误码。
  若断言启用，当前仍保留大多先前行为（停止系统）。

Video
=====

* :c:func:`video_import_buffer` 不再通过 ``uint16_t *idx``
  输出参数返回导入的 buffer index，
  而是返回指向导入的 :c:struct:`video_buffer` 的指针，
  失败时为 ``NULL``。这有助于使 index 对应用透明，
  并使 buffer 可从应用访问。

Twister
=======

* 测试通过后发生的 Faults 现在被显式检测并使整个 testsuite 失败；
  如果测试故意产生 fault，对应 test case 必须标记为
  ``ignore_faults: true`` (:github:`116359`)。

内核（补充）
************

* :c:struct:`k_futex` 不再是内核对象，对应的类型
  :c:enumerator:`K_OBJ_FUTEX` 已移除。任何用户可访问的内存
  都可以用作 futex 地址。futex 操作上不再可能发生 -EINVAL 错误。

开发板（补充）
**************

* 在 NXP LPC54xxx 上，``CONFIG_LPC54XXX_SRAM2_CLOCK`` 已被
  ``CONFIG_SOC_SERIES_LPC54XXX_SRAM_CLOCKS`` 替换。旧名称在 LPC54114
  是该系列中唯一 SoC 时适用，那时 CMSIS ``SystemInit()`` 仅启用
  SRAM2。在 LPC546xx 上它启用 SRAM2 和 SRAM3，因此该选项现在
  覆盖的范围超出了其命名的那一个 bank。两者默认为 ``y``。
  分配了旧符号的配置必须更新，否则构建失败。

* 在 RP2040 和 RP2350 上，``vreg`` 节点（:dtcompatible:`raspberrypi,core-supply-regulator`）
  现在默认为 ``disabled`` 而不是 ``okay``。需要此稳压器的树外开发板
  必须在 ``&vreg`` 节点上设置 ``status = "okay"``。

  在 RP2040 上，``regulator-always-on`` 和 ``regulator-allowed-modes =
  <REGULATOR_RPI_PICO_MODE_NORMAL>`` 属性现在在 SoC dtsi 中默认设置。
  之前显式设置它们的开发板可以删除这些行。(:github:`114751`)

* 在 RP2350（rpi_pico 系列）上，``hazard3`` 和 ``m33`` cpucluster 限定符
  已弃用，改用 ``hazard3_0`` 和 ``m33_0``，后者显式标识该 cluster 为 CPU0
  并为双核支持铺平道路。所有树内 RP2350 开发板已迁移到新限定符
  （例如 ``rpi_pico2/rp2350a/m33`` 到 ``rpi_pico2/rp2350a/m33_0``）。
  使用裸 ``hazard3``/``m33`` 限定符的树外开发板应重命名其开发板文件、
  ``board.yml`` 中的 ``cpucluster:`` 条目和 Kconfig select 行，
  改用 ``SOC_RP2350[AB]_HAZARD3_0``/``SOC_RP2350[AB]_M33_0``。
  ``soc.yml`` 中裸的 ``hazard3``/``m33`` 条目和对应的
  ``SOC_RP2350[AB]_HAZARD3``/``_M33`` Kconfig 符号已弃用，
  并将在未来版本中移除。

* :zephyr:board:`rak4631` 现在支持 WisBlock 生态系统。
  需要 WisBlock Base Board 扩展板（例如 :ref:`rakwireless_rak19007`）
  才能暴露传感器和 IO 插槽：

  .. code-block:: shell

     west build -b rak4631/nrf52840 --shield rakwireless_rak19007

* Kconfig 选项 :kconfig:option:`CONFIG_SRAM_SIZE` 和
  :kconfig:option:`CONFIG_SRAM_BASE_ADDRESS` 已弃用，开发板应改为使用
  设备树 ``zephyr.sram`` chosen 节点来指定将使用的 RAM 节点
  （其值填充了 Kconfig 值）。如果手动调整了任一选项，
  将导致 :kconfig:option:`CONFIG_SRAM_DEPRECATED_KCONFIG_SET` 被设置，
  表示此弃用。

* 内部 Nordic SoC 平台 Kconfig 符号 ``NRF_PLATFORM_HALTIUM``
  和 ``NRF_PLATFORM_LUMOS`` 不再被树内代码使用，树内代码现在
  依赖显式的 :kconfig:option:`CONFIG_SOC_SERIES_NRF54H`、
  :kconfig:option:`CONFIG_SOC_SERIES_NRF92`、
  :kconfig:option:`CONFIG_SOC_SERIES_NRF54L` 和
  :kconfig:option:`CONFIG_SOC_SERIES_NRF71` 检查。
  两个符号保留为弃用 stub，当选择了相应的 SoC 系列且
  启用了 :kconfig:option:`CONFIG_NRF_PLATFORM_DEPRECATED_SYMBOLS` 时
  默认为 ``y``，因此现有的 ``CONFIG_NRF_PLATFORM_*=y`` 行和
  ``depends on NRF_PLATFORM_*`` 子句仍会构建并带有 Kconfig 弃用警告。
  使用这些符号的树外 Kconfig、CMake 和代码应更新：

  * 将 ``CONFIG_NRF_PLATFORM_HALTIUM`` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_NRF54H` 或
    :kconfig:option:`CONFIG_SOC_SERIES_NRF92`。
  * 将 ``CONFIG_NRF_PLATFORM_LUMOS`` 替换为
    :kconfig:option:`CONFIG_SOC_SERIES_NRF54L` 或
    :kconfig:option:`CONFIG_SOC_SERIES_NRF71`。

* Aesc Silicon ``elemrv`` 开发板已重命名为 ``elemrv_flask_n``。

* Nordic sysbuild Kconfig 选项 ``SB_CONFIG_NRF_HALTIUM_GENERATE_UICR``
  已重命名为 :kconfig:option:`SB_CONFIG_NRF_GENERATE_UICR`。
  更新 sysbuild 配置以使用新名称。

* Nordic SoC 头文件 :file:`<haltium_power.h>` 和 :file:`<haltium_pm_s2ram.h>`
  已分别重命名为 :file:`<soc_power.h>` 和 :file:`<soc_pm_s2ram.h>`。
  旧名称下的转发头文件仍可用，并发出 ``#warning``
  指向新的 include 路径。包含旧路径的树外代码应更新：

  * 将 ``#include <haltium_power.h>`` 替换为 ``#include <soc_power.h>``。
  * 将 ``#include <haltium_pm_s2ram.h>`` 替换为 ``#include <soc_pm_s2ram.h>``。

* 基于 STM32H7RS 的开发板（stm32h7s78_dk 和 nucleo_h7s3l8）
  的系统时钟已提高到 600 MHz。这通过提高 PLL1 频率
  到 300 MHz 实现，这也影响总线和内核时钟，
  导致略高的频率。

* :kconfig:option:`CONFIG_GPIO` 不再在大多数 STM32 开发板上默认启用。
  （带 GPIO hogs 的开发板保持启用，因为 hogs 需要 GPIO 才能工作）。
  依赖 ``CONFIG_GPIO=y`` 为默认值的应用需要显式启用该选项。
  (:github:`109468`)

* 使用 UF2 镜像并迁移到 :dtcompatible:`zephyr,mapped-partition` 的开发板
  应在其 defconfig 中启用 HEX 输出（:kconfig:option:`CONFIG_BUILD_OUTPUT_HEX`），
  因为 UF2 镜像生成不再依赖 :kconfig:option:`CONFIG_FLASH_LOAD_OFFSET`
  从 BIN 输出确定代码地址。HEX 到 UF2 现在是默认（而不是 BIN）。
  (:github:`107944`)

* Ezurio bl54l15u_dvk 已移除。bl54l15_dvk 仍可用，
  支持模块的 bl54l15 和 bl54l15u 变体，功能相同。
  使用 bl54l15u_dvk 的开发板应迁移到
  bl54l15_dvk/nrf54l15/cpuapp 或 bl54l15_dvk/nrf54l15/cpuflpr（视情况而定）。

* 开发板 stm32h573i_dk 和 b_u585i_iot02a 的默认 MCUboot 签名类型
  已从 RSA-3072 更改为 EC-P256。这影响在 TF-M 中启用了 MCUboot
  （:kconfig:option:`CONFIG_TFM_BL2`）的构建。如果希望继续使用 RSA-3072，
  需要将 :kconfig:option:`CONFIG_TFM_MCUBOOT_SIGNATURE_TYPE` 设置为 ``"RSA-3072"``。
  否则，请确保拥有所用签名类型的自己的签名密钥。

* modules/hal_silabs/gecko 下的所有 Kconfig 已从 ``SOC_GECKO_*``
  重命名为 ``SILABS_GECKO_*``。相应地调整您的开发板。

* 所有 Silabs Series 0 和 Series 1 开发板的时钟配置
  现在需要在设备树中指定。Kconfig ``CONFIG_SOC_GECKO_HAS_HFRCO_FREQRANGE``
  和 ``CONFIG_CMU_*`` 已移除。参见 :github:`111754` 了解如何调整开发板的示例。

* 在 nRF54LM20 DK 上，``nrf7002eb2`` 扩展板（及其 ``nrf7002eb2_nrf7001`` 和
  ``nrf7002eb2_nrf7000`` 变体）不再重定向应用控制台。
  之前它禁用了 UART20 并将控制台（shell、mcumgr 和 Bluetooth monitor）
  重路由到 UART30，以解决仅存在于预生产套件上（而非生产 nRF54LM20 DK 上）
  的引脚冲突。控制台现在保持在 UART20（VCOM1）上，
  与标准开发板行为一致，``button3``/``sw3`` 不再被删除。
  在 nRF54LM20 DK 上使用该扩展板的现有用户
  必须将串行终端从 VCOM0 移回 VCOM1。nRF54L15 DK 不受影响：
  其扩展头确实与 UART20 冲突，因此保持将控制台重路由到 UART30。

* mimxrt1180_evk Kconfig 选项 ``NXP_BOARD_SPECIFIC_MPU_SETTINGS``
  已重命名为 :kconfig:option:`CONFIG_BOARD_NXP_SPECIFIC_MPU_SETTINGS`，
  与其他 NXP 开发板选项和 frdm_imxrt1186 使用的 ``BOARD_NXP_*`` 命名一致。
  设置 ``CONFIG_NXP_BOARD_SPECIFIC_MPU_SETTINGS`` 的配置
  必须更新为新名称。

* 支持通过 TF-M 进行固件更新的开发板现在必须选择
  :kconfig:option:`CONFIG_TFM_PARTITION_FIRMWARE_UPDATE_SUPPORTED`。

* 从基于 STM32 的开发板中移除了 :kconfig:option:`CONFIG_SPI_STM32_INTERRUPT`
  的默认激活。选择中断驱动与轮询 SPI 传输是应用关注点，
  不是开发板关注点。在受影响的开发板上依赖中断驱动 SPI
  （例如使用 :c:func:`spi_transceive_signal` 或 :c:func:`spi_transceive_cb`
  而不使用 DMA）的应用现在必须在自己的配置中显式启用
  :kconfig:option:`CONFIG_SPI_STM32_INTERRUPT`。(:github:`116218`)

* 以下在 v4.3 或更早版本中弃用的开发板名称别名已移除
  (:github:`116657`, :github:`116750`)。
  改为构建该别名原本重定向到的开发板目标：

  * ``arduino_uno_r4_minima`` → ``arduino_uno_r4@minima``
  * ``arduino_uno_r4_wifi`` → ``arduino_uno_r4@wifi``
  * ``esp32c6_devkitc`` → ``esp32c6_devkitc/esp32c6/hpcore``
  * ``esp32_devkitc_wroom/esp32/procpu`` 和 ``esp32_devkitc_wrover/esp32/procpu`` →
    ``esp32_devkitc/esp32/procpu``
  * ``esp32_devkitc_wroom/esp32/appcpu`` 和 ``esp32_devkitc_wrover/esp32/appcpu`` →
    ``esp32_devkitc/esp32/appcpu``
  * ``neorv32`` → ``neorv32/neorv32/up5kdemo``
  * ``panb511evb`` → ``panb611evb``
  * ``raytac_an54l15q_db/nrf54l15/cpuapp`` → ``raytac_an54lq_db_15/nrf54l15/cpuapp``
  * ``scobc_module1`` → ``scobc_a1``
  * ``xiao_esp32c6`` → ``xiao_esp32c6/esp32c6/hpcore``

* Nordic nRF52 Kconfig 选项 ``CONFIG_GPIO_AS_PINRESET`` 已移除。
  改为在 ``&uicr`` 设备树节点上设置 ``gpio-as-nreset`` 属性。

* Nordic Kconfig 选项 ``CONFIG_SOC_DCDC_NRF52X``、``CONFIG_SOC_DCDC_NRF52X_HV``、
  ``CONFIG_SOC_DCDC_NRF53X_APP``、``CONFIG_SOC_DCDC_NRF53X_NET`` 和
  ``CONFIG_SOC_DCDC_NRF53X_HV`` 已移除。改为在设备树中配置稳压器：
  在 ``&reg1``/``&vregmain``/``&vregradio`` 上设置
  ``regulator-initial-mode = <NRF5X_REG_MODE_DCDC>``，
  在 ``&reg0``/``&vregh`` 上设置 ``status = "okay"``。

* Nordic nRF53 Kconfig 选项 ``CONFIG_BOARD_ENABLE_CPUNET`` 已移除。
  改用 :kconfig:option:`CONFIG_SOC_NRF53_CPUNET_ENABLE`。

* ``esp_threadbr_ethernet`` 扩展板已移除。现有用户应
  构建 ``esp_threadbr/esp32s3/procpu/ethernet``，
  而不是将 ``esp_threadbr/esp32s3/procpu`` 与 ``SHIELD=esp_threadbr_ethernet`` 组合。
  连同扩展板一起，``esp_threadbr`` 子开发板连接器描述已移除，
  因此 ``espressif,esp-threadbr-header`` 绑定、``esp_threadbr_header``
  GPIO nexus 节点以及 ``esp_threadbr_spi`` 和 ``esp_threadbr_i2c``
  设备树标签已消失。使用它们的树外覆盖层
  必须直接引用 SoC 节点（``&spi2``、``&i2c0``、``&gpio0``、``&gpio1``）。
  (:github:`116956`)

* STM32MP15 Cortex-M4 SoC Kconfig 符号 ``SOC_STM32MP15_M4``
  已重命名为 :kconfig:option:`CONFIG_SOC_STM32MP157CXX_M4`。
  选择了 ``SOC_STM32MP15_M4`` 的树外 STM32MP15 开发板
  必须改为选择 :kconfig:option:`CONFIG_SOC_STM32MP157CXX_M4`。
  (:github:`118151`)

* 在 Arduino UNO R4 WiFi 上，``zephyr,console`` 和 ``zephyr,shell-uart``
  现在默认指向 SCI9，板载 ESP32-S3 将其桥接到 USB-C 连接器
  作为 USB CDC ACM 端口，而不是 D0/D1 头引脚上的 SCI2。
  控制台输出现在可在用于烧录开发板的同一端口上查看，
  无需外部 USB-串口适配器。依赖控制台在 D0/D1 上的应用
  可在应用覆盖层中重新选择：

  .. code-block:: devicetree

     / {
         chosen {
             zephyr,console = &uart2;
             zephyr,shell-uart = &uart2;
         };
     };

  Arduino UNO R4 Minima 不受影响。(:github:`118433`)

* Espressif 的按模块设备树 include 文件及其 SoC Kconfig 符号已移除。
  模块或 SIP 部件号描述开发板携带多少闪存和 PSRAM，
  这是开发板的属性而非 SoC 的属性，因此两者现在都由开发板自身声明。

  每个 ``espressif/<soc>/<soc>_<module>.dtsi`` 文件
  被每个 SoC 的单个 ``espressif/<soc>/<soc>.dtsi`` 替换。
  对应的隐藏 Kconfig 符号（如 ``SOC_ESP32S3_WROOM_N8`` 和
  ``SOC_ESP32_WROVER_E_N16R8``）被纯 SoC 符号替换，
  如 :kconfig:option:`CONFIG_SOC_ESP32S3`。
  ``SOC_PART_NUMBER`` 现在报告 SoC 而不是模块。

  树外 Espressif 开发板必须更新，在更新前构建失败：

  * Include 纯 SoC dtsi 而不是模块的。
  * 在 ``Kconfig.<board>`` 中选择纯 SoC 符号。
  * 在开发板 dts 中描述闪存，同时给出 ``reg`` 和匹配的 ``ranges``，
    因为 SoC dtsi 不再设置两者。

    .. code-block:: devicetree

       &flash0 {
           reg = <0x0 DT_SIZE_M(8)>;
           ranges = <0x0 0x0 DT_SIZE_M(8)>;
       };

  * 在带有 PSRAM 的开发板上以同样方式描述 PSRAM：

    .. code-block:: devicetree

       &psram0 {
           size = <DT_SIZE_M(2)>;
       };

  在双核 ESP32 上，``espressif/esp32/esp32_appcpu.dtsi``
  也不再设置闪存，因此 APPCPU 开发板 dts
  必须声明与其 PROCPU 对应部分相同的闪存。

* 在 NXP S32K148 上，ENET 节点 ``enet``（:dtcompatible:`nxp,enet`）、
  ``enet_mac``（:dtcompatible:`nxp,enet-mac`）、``enet_mdio``
  （:dtcompatible:`nxp,enet-mdio`）和 ``enet_ptp_clock``
  （:dtcompatible:`nxp,enet-ptp-clock`）现在默认为 ``disabled``
  而不是 ``okay``。使用以太网的树外开发板必须在这些节点上
  设置 ``status = "okay"``。

* ``mimxrt1170_evk`` 和 ``mimxrt1160_evk`` cm7 目标以及 ``frdm_imxrt1152``
  现在提供静态 Arm MPU 区域表并默认启用
  :kconfig:option:`CONFIG_ARM_MPU_CM7_UNMAPPED_REGION`。
  因此 MPU 不再回退到 ``PRIVDEFENA`` 背景映射，
  该表之外的地址不再可访问。该表覆盖 ITCM、DTCM、
  双核开发板上与 CM4 共享的 OCRAM 镜像区域、
  支撑 ``zephyr,sram`` chosen 节点的 RAM、FlexSPI NOR 窗口
  和外设孔径，但不覆盖剩余的片上 bank：
  ``mimxrt1170_evk`` 和 ``frdm_imxrt1152`` 上的 ``ocram1`` 和 ``ocram2``，
  以及 ``mimxrt1160_evk`` 上的 ``ocram_combined``。

  将这些 bank 中放置数据的应用必须使用 ``zephyr,memory-attr`` 节点
  显式声明它，该节点随后获得自己的 MPU 区域，
  如树内 :file:`samples/subsys/ipc` 示例对其与 CM4 共享的内存所做的那样。
  将 :kconfig:option:`CONFIG_ARM_MPU_CM7_UNMAPPED_REGION` 设置为 ``n``
  可恢复之前行为。

* Silabs Kconfig 选项 ``CONFIG_SOC_SILABS_IMAGE_PROPERTIES``
  已重命名为 :kconfig:option:`CONFIG_SOC_VENDOR_SILABS_IMAGE_PROPERTIES`。

* Silabs Kconfig 选项 ``CONFIG_SOC_SILABS_PM_LOW_INTERRUPT_LATENCY``
  已重命名为 :kconfig:option:`CONFIG_SOC_VENDOR_SILABS_PM_LOW_INTERRUPT_LATENCY`。

* stm32h573i_dk 和 stm32h5f5j_dk disco 套件现在采用 mspi 控制器模型。
  这是迁移到 mspi stm32 支持的下一步。对于两个开发板，
  将 xspi 节点声明为 ``st,stm32-xspi-controller`` 兼容。
  一旦所有目标开发板更改完毕，stm32h5 设备 DTS 将更新。

* stm32l562e disco 套件现在采用 mspi 控制器模型。
  这是迁移到 mspi stm32 支持的下一步。
  对于该开发板，将 ospi 节点声明为 ``st,stm32-ospi-controller`` 兼容。
  一旦所有目标开发板更改完毕，stm32l5 设备 DTS 将更新。

设备驱动与设备树
*****************

.. 仅在此处放置所有设备驱动通用的内容。特定于一个驱动子系统的
   内容放入其自己的子章节，如下。

* :c:macro:`DEVICE_API` 宏现在对于声明任何上游驱动类的
  设备驱动 API 实例都是必需的，包括树外驱动。
  :c:macro:`DEVICE_API_GET` 现在断言 API 属于请求的类，
  这要求实例位于该类的可迭代 section 中。
  将上游 API 作为其第一个成员嵌入的树外驱动类
  还必须使用 :c:macro:`DEVICE_API_EXTENDS` 声明这种关系，
  以便父类的 :c:macro:`DEVICE_API_GET`
  在实现了子 API 的设备上成功。参见 :ref:`device_driver_api` 了解详情。

ADC
===

* :dtcompatible:`microchip,xec-adc` 的 ``girqs`` 和 ``pcrs`` 属性
  （数组类型）已被编码的 ``girqs``（使用 ``MCHP_XEC_ECIA_GIRQ_ENC`` 宏）
  和 ``pcr-scr``（int 类型）替换，用于编码的 PCR 寄存器索引和位位置
  (:github:`105658`)。

* :kconfig:option:`CONFIG_LPADC_DO_OFFSET_CALIBRATION` 选项
  现在仅在启用 :kconfig:option:`CONFIG_ADC_MCUX_LPADC` 时有意义，
  其 ``default y`` 现在限定于该条件。
  树内开发板不再在其 defconfig 中显式启用它，
  因为默认值已覆盖它们。

* ``CONFIG_LPADC_CHANNEL_COUNT`` Kconfig 选项已移除。
  NXP LPADC 驱动现在将硬件命令槽视为逻辑 ADC 通道，
  从设备树中为该实例声明的 ``channel`` 子节点
  推导每个实例的逻辑通道数，因此未使用的命令槽
  不再消耗 RAM。通过降低 Kconfig 选项来节省 RAM 的应用
  应直接删除它。未声明 ``channel`` 节点的实例
  保持完整的硬件容量可用，因此仅通过
  :c:func:`adc_channel_setup` 在运行时配置通道的应用不受影响；
  混合使用两者的应用必须在设备树中声明
  其在运行时设置的最高的通道标识符。
  声明超出 SoC 实现的 ``CMD`` 寄存器数量的通道标识符
  现在是构建错误而不是运行时 HAL 断言，
  且 :c:func:`adc_read` 现在以 ``-EINVAL`` 拒绝
  空的通道掩码或选择超出该限制的通道，
  而不是静默忽略 (:github:`116995`)。

Analog Devices
=============

* :kconfig:option:`CONFIG_NUM_IRQS` 现在对所有 MAX32 SoC
  从设备树自动计算，基于活动（``status = "okay";``）设备，
  使用 ``dt_highest_controller_irq_number`` Kconfig 预处理器函数。
  硬编码的每 SoC 值已移除，生成的 IRQ 表
  通常比之前小得多。使用 :c:macro:`IRQ_CONNECT()`
  注册自定义 ISR 的应用可能遇到如下构建失败，
  因为 :kconfig:option:`CONFIG_NUM_IRQS` 值较低：

  .. code-block::

    gen_isr_tables.py: error: IRQ 88 (offset=0) exceeds the maximum of 54

  显式将 :kconfig:option:`CONFIG_NUM_IRQS` 设置为适当值
  以解决这些问题。(:ref:`以下文档页面 <setting_configuration_values>` 解释如何操作)

  使用 :c:func:`irq_connect_dynamic` 在运行时安装 ISR 的应用
  不受此构建时检查覆盖，必须手动审查。

Audio Codec
===========

* 音频编解码器驱动后端 API 现在使用 :c:struct:`audio_codec_driver_api`
  而不是 ``struct audio_codec_api``。

  树外音频编解码器驱动必须重命名其后端 API 结构体定义，
  并将 API 实例切换为 ``DEVICE_API(audio_codec, ...)``。
  参见 :github:`110631` 了解树内驱动如何更新的示例。
  使用 ``audio_codec_...`` API 的应用代码不受影响。

Clock Control
=============

* 已移除 Nordic Kconfig 选项 ``CONFIG_NRFS_LOCAL_DOMAIN_DVFS_SCALE_DOWN_AFTER_INIT``。
  应改用 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_HSFLL_LOCAL_REQ_LOW_FREQ`。

* :dtcompatible:`nxp,imxrt11xx-arm-pll` 绑定现在使用 ``loop-div``
  和 ``post-div`` 进行 ARM PLL 配置。
  传统 ``clock-mult`` 和 ``clock-div`` 属性仍受支持但已弃用。
  现有 RT11xx 覆盖层应使用映射
  ``loop-div = clock-mult * 2`` 和 ``post-div = clock-div`` 更新。

* SiWx91x 时钟控制已拆分为三个管理器
  （:dtcompatible:`silabs,siwx91x-cmu-aon`、:dtcompatible:`silabs,siwx91x-cmu-ulp`、
  :dtcompatible:`silabs,siwx91x-cmu-hp`）。
  传统 :dtcompatible:`silabs,siwx91x-clock` 绑定和 ``clock0`` 节点已移除。
  树外开发板和覆盖层必须将 ``clocks`` phandle 更新为匹配的 CMU，
  并使用 ``siwx91x-clock.h`` 中更新的 ``SIWX91X_CLK_*`` ID。
  例如，``clocks = <&clock0 SIWX91X_CLK_UART0>;`` 变为
  ``clocks = <&cmu_hp SIWX91X_CLK_UART0>;``。

Clock control nRF 弃用说明
-----------------------------

.. toggle::

   :ref:`clock_control_api` 驱动已为以下 nRF52、nRF53、nRF91 和 nRF54L
   系列设备上的时钟更新：

   * HFCLK
   * LFCLK
   * XO
   * XO24M
   * HFCLK192M
   * HFCLKAUDIO

   要恢复传统驱动实现，将 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF`
   设置为 ``y``。

   要将代码从 Zephyr v4.4.0 迁移到 Zephyr v4.5.0，完成以下步骤：

   1. 在应用特定或开发板特定的设备树覆盖层文件中启用每个应用控制的时钟。

      这会启用相应的时钟驱动。
      例如：

      .. code-block:: dts

         /* 如果要控制 nRF54L XO */
         &xo {
             status = "okay";
         };

         /* 如果要控制 nRF52、nRF53 HFCLK */
         &hfclk {
             status = "okay";
         };

         /* 如果要控制 nRF52、nRF53、nRF91 或 nRF54L LFCLK */
         &lfclk {
             status = "okay";
         };

         /* 如果要控制 HFCLK192M */
         &hfclk192m {
             status = "okay";
         };

         /* 如果要控制 XO24M */
         &xo24m {
             status = "okay";
         };

         /* 如果要控制 HFCLKAUDIO */
         &hfclkaudio {
             status = "okay";
         };

   #. 重命名以下 Kconfig 选项：

      * 将 :kconfig:option:`CONFIG_NRFX_CLOCK_USE_LFRC_CALIBRATION`
        替换为 :kconfig:option:`CONFIG_NRFX_CLOCK_LFCLK_USE_LFRC_CALIBRATION`。
      * 将 :kconfig:option:`CONFIG_NRFX_CLOCK_LF_CAL_ENABLED`
        替换为 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_K32SRC_RC_CALIBRATION`。

   #. 将以下 Kconfig 选项移到 ``nordic,nrf-clock-lfclk`` 设备树节点：

      * 将 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_K32SRC_FREQUENCY`
        替换为 ``k32src-frequency`` 属性。
      * 将 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_SOURCE` choice
        替换为 ``k32src`` 枚举属性。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_RC` 和
        :kconfig:option:`NRFX_CLOCK_LF_SRC_RC` 替换为 ``k32src = "rc"``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_XTAL` 和
        :kconfig:option:`NRFX_CLOCK_LF_SRC_XTAL` 替换为 ``k32src = "xtal"``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_SYNTH` 和
        :kconfig:option:`NRFX_CLOCK_LF_SRC_SYNTH` 替换为 ``k32src = "synth"``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_EXT_LOW_SWING` 和
        :kconfig:option:`NRFX_CLOCK_LF_SRC_LOW_SWING` 替换为 ``k32src = "ext_low_swing"``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_EXT_FULL_SWING` 和
        :kconfig:option:`NRFX_CLOCK_LF_SRC_FULL_SWING` 替换为 ``k32src = "ext_full_swing"``。
      * 将 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_ACCURACY_PPM` choice
        替换为 ``k32src-accuracy-ppm`` 枚举属性。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_500PPM`
        替换为 ``k32src-accuracy-ppm = <500>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_250PPM`
        替换为 ``k32src-accuracy-ppm = <250>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_150PPM`
        替换为 ``k32src-accuracy-ppm = <150>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_100PPM`
        替换为 ``k32src-accuracy-ppm = <100>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_75PPM`
        替换为 ``k32src-accuracy-ppm = <75>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_50PPM`
        替换为 ``k32src-accuracy-ppm = <50>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_30PPM`
        替换为 ``k32src-accuracy-ppm = <30>``。
      * 将 :kconfig:option:`CLOCK_CONTROL_NRF_K32SRC_20PPM`
        替换为 ``k32src-accuracy-ppm = <20>``。
      * 将 :kconfig:option:`CONFIG_NRFX_CLOCK_LFXO_TWO_STAGE_ENABLED`
        替换为 ``k32src = "xtal"`` 或 ``k32src = "ext_low_swing"``
        或 ``k32src = "ext_full_swing"``。

   #. 更新应用以使用新的时钟控制 API。

      更新 API 调用时使用以下映射：

      * ``mgr`` 是为 ``nordic,nrf-clock`` 创建的 on-off 管理器，
        使用 ``z_nrf_clock_control_get_onoff`` 获取。
      * ``dev`` 是与 ``nordic,nrf-clock`` 兼容的设备。
      * ``sys`` 是 ``nordic,nrf-clock`` 的子系统。
        新的时钟实现不使用它。
      * ``new_dev`` 是对应于之前使用的 ``sys`` 值的设备。
        它必须与以下节点之一兼容：

        * ``nordic,nrf-clock-lfclk``
        * ``nordic,nrf-clock-hfclk``
        * ``nordic,nrf-clock-xo``
        * ``nordic,nrf-clock-hfclk192m``
        * ``nordic,nrf-clock-xo24m``
        * ``nordic,nrf-clock-hfclkaudio``

      以下示例展示了已弃用的 API 用法和对应的新 API 用法：

      .. code-block:: c

         // 旧 API 用法（已弃用）
         z_nrf_clock_calibration_init(&mgrs);    //1
         onoff_release(mgr)                      //2
         onoff_request(mgr, &cli);               //3
         onoff_cancel_or_release(mgr, &cli);     //4
         clock_control_on(dev,sys)               //5
         clock_control_off(dev,sys)              //6
         clock_control_async_on(dev,sys)         //7
         clock_control_get_status(dev,sys)       //8
         z_nrf_clock_control_get_onoff(sys)      //9

         // 新 API 用法
         z_nrf_clock_calibration_init();                             //1
         nrf_clock_control_release(new_dev, NULL);                   //2
         nrf_clock_control_request(new_dev, NULL, &cli);             //3
         nrf_clock_control_cancel_or_release(new_dev, NULL, &cli);   //4
         clock_control_on(new_dev, NULL)                             //5
         clock_control_off(new_dev, NULL)                            //6
         clock_control_async_on(new_dev, NULL)                       //7
         clock_control_get_status(new_dev, NULL)                     //8
         // 移除所有 z_nrf_clock_control_get_onoff 的使用             //9

Comparator
==========

* 已移除带 ``nxp,`` 前缀的已弃用 :dtcompatible:`nxp,kinetis-acmp` 属性：
  改用 ``enable-pin-out``、``use-unfiltered-output``、``enable-high-speed-mode``、
  ``filter-enable-sample``、``filter-count``、``filter-period``
  和 ``enable-window-mode``。

Controller Area Network (CAN)
=============================

* NXP SJA1000（``can_sja1000.h``）和 Bosch M_CAN（``can_mcan.h``）
  CAN 控制器驱动后端的头文件已转换为库特定 include。
  基于这些后端的树外驱动需要相应更新其 include 指令。

* Bosch M_CAN 驱动现在仅使用 RX FIFO0 处理接收的 CAN 帧，
  确保这些帧按在总线上接收的顺序处理。
  树外用户可能希望更新任何 ``bosch,mram-cfg`` 设备树属性覆盖，
  将所有 FIFO 元素分配给 RX FIFO0。

* 已弃用的 ``bus-speed`` 和 ``bus-speed-data`` CAN 控制器设备树属性已移除。
  改用 ``bitrate`` 和 ``bitrate-data``。

* CAN 控制器驱动 ops 不再包含 ``can_set_state_change_callback_t``
  函数指针，因为添加/移除回调现在通过通用的
  :c:func:`can_add_state_change_callback` 和
  :c:func:`can_remove_state_change_callback` API 函数处理。
  树外驱动可以完全删除该驱动 op，或根据需要
  替换为 ``can_state_change_callbacks_enabled_t``。
  驱动现在必须使用 :c:func:`can_fire_state_change_callbacks`
  触发 CAN 控制器状态变化回调 (:github:`117889`)。

* CAN 总线网络驱动（:kconfig:option:`CONFIG_NET_CANBUS`）
  现在为每个使用 :c:macro:`CAN_DEVICE_DT_DEFINE` 或
  :c:macro:`CAN_DEVICE_DT_INST_DEFINE` 定义的 CAN 控制器设备
  定义一个网络接口，而不是为 ``zephyr,canbus`` chosen 节点定义一个。

Counter
=======

* :dtcompatible:`nxp,lpc-ctimer` 现在通过通用
  :ref:`mux <mux_api>` 子系统路由其输入捕获信号。
  ``inputmux-connections`` 属性已移除；
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从定时器节点的 ``mux-states`` 属性引用它。
  cell 布局不变，因此现有的
  ``inputmux-connections = <&inputmux0 0 0x06000024>;``
  变为 ``mux-states = <&inputmux0 0 0x06000024>;`` (:github:`112088`)

* :dtcompatible:`nxp,lptmr` 的 ``prescaler`` 属性已移除。
  改用 ``prescale-glitch-filter`` 和 ``prescale-glitch-filter-bypass``。
  新属性是指数而不是除数：预分频器除以 ``2^(prescale-glitch-filter + 1)``。

* :dtcompatible:`adi,max32-rtc-counter` 和 :dtcompatible:`adi,max32-wut`
  现在使用共享的 ``clk_32k`` 节点选择 32 kHz 时钟源。
  时钟源现在通过 ``clk_32k`` 节点的 ``clocks`` 属性配置，
  而不是每个外设节点中的 ``clock-source`` 属性 (:github:`117709`)。

Devicetree
==========

* 使用负数字面量（例如 ``<(-1)>``）的 ``int`` 和 ``array`` 类型
  设备树属性现在展开为负值，而不是之前使用的补码无符号值。
  依赖旧无符号表示的代码（例如无符号比较或
  ``BUILD_ASSERT(DT_PROP(node, foo) > 0, ...)`` 检查）
  必须更新为使用有符号类型或有符号感知检查 (:github:`107271`)。

* ``zephyr,memory-region-mpu`` 属性已移除。
  改用 ``zephyr,memory-attr``。它接受整数位掩码，而不是字符串：

  .. code-block:: none

     "RAM"         -> <DT_MEM_ARM_MPU_RAM>
     "RAM_NOCACHE" -> <DT_MEM_ARM_MPU_RAM_NOCACHE>
     "FLASH"       -> <DT_MEM_ARM_MPU_FLASH>
     "PPB"         -> <DT_MEM_ARM_MPU_PPB>
     "IO"          -> <DT_MEM_ARM_MPU_IO>
     "EXTMEM"      -> <DT_MEM_ARM_MPU_EXTMEM>

Digital Microphone
==================

* DMIC 驱动后端 API 现在使用 :c:struct:`dmic_driver_api`
  而不是 ``struct _dmic_ops``。

  树外 DMIC 驱动必须重命名其后端 API 结构体定义，
  并将 API 实例切换为 ``DEVICE_API(dmic, ...)``。
  参见 :github:`107695` 了解树内驱动如何更新的示例。
  使用 :c:func:`dmic_configure`、:c:func:`dmic_trigger` 和
  :c:func:`dmic_read` 的应用代码不受影响。

Disk
====

* :kconfig:option:`CONFIG_NVME_REQUEST_TIMEOUT` 现在以秒为单位
  记录并限定范围。NVMe 请求超时路径之前将该值与
  :c:func:`k_uptime_get_32` 毫秒比较而不转换，
  因此默认值 ``5`` 在约 5 ms 后过期而不是 5 秒。
  驱动现在在调度和过期检查前使用 ``MSEC_PER_SEC`` 转换。
  如果应用依赖之前短超时行为，审查任何非默认设置。
  (:github:`117809`)

Display
=======

* SDL 显示像素格式选择的 Kconfig 选项
  ``CONFIG_SDL_DISPLAY_DEFAULT_PIXEL_FORMAT_*``
  已移除，改为在 SDL 伪设备节点上直接使用
  :zephyr_file:`include/zephyr/dt-bindings/display/panel.h`
  中的 PANEL_PIXEL_FORMAT_* 宏在设备树中设置 pixel-format 属性。
  (:github:`104099`)

* LVGL ``CONFIG_LV_Z_COLOR_24_BGR_TO_RGB`` Kconfig 选项已移除。
  LVGL 的 RGB888 色彩格式在内存中以蓝、绿、红顺序存储字节，
  与 :c:enumerator:`PIXEL_FORMAT_RGB_888` 的内存布局匹配，
  因此对于报告该格式显示的不再进行通道交换。
  其帧缓冲反而期望红、绿、蓝字节顺序的显示
  现在必须报告 :c:enumerator:`PIXEL_FORMAT_BGR_888`，
  对于该格式 LVGL 胶水层自动执行红/蓝通道交换。

* LVGL 现在直接以 ``RGB565_SWAPPED`` 色彩格式渲染
  报告 :c:enumerator:`PIXEL_FORMAT_RGB_565X` 的显示，
  因此这些显示不再需要 :kconfig:option:`CONFIG_LV_COLOR_16_SWAP`，
  且不得与该像素格式一起启用，否则缓冲
  会被字节交换两次。``t_deck``、``m5stack_core2`` 和 ``wio_terminal``
  开发板不再默认启用该选项。

* 用于 ST7305 和 ST7306 显示的 Kconfig 选项
  ``CONFIG_ST730X_POWERMODE_LOW`` 已移除，
  改为在设备节点上切换 low-power-mode 属性。

* ST7567 显示驱动的 ``set_contrast`` 函数现在期望
  0-255 范围的对比度值，而不是 0-63。
  驱动现在将值缩放到控制器期望的 6 位范围。
  ``CONFIG_ST7567_DEFAULT_CONTRAST`` Kconfig 选项
  已更新以反映新范围。(:github:`112528`)

* :dtcompatible:`raspberrypi,bcm2711-framebuffer` 现在需要
  ``pixel-format`` 属性，并获得可选的 ``red-blue-swap`` 布尔值
  以指示面板期望 BGR 通道顺序。
  依赖固件协商像素顺序来纠正交换通道的开发板
  还必须设置 ``red-blue-swap``。(:github:`115633`)

* ``chipone,co5300`` MIPI DSI 显示驱动不再维护
  内部 shadow framebuffer，``pitch-align``、``addr-align`` 和
  ``ext-ram`` 设备树属性已从 :dtcompatible:`chipone,co5300`
  绑定中移除。之前依赖这些属性来满足显示控制器对齐要求的开发板
  应改为启用 :kconfig:option:`CONFIG_LV_Z_AREA_X_ALIGNMENT_WIDTH`
  和 :kconfig:option:`CONFIG_LV_Z_AREA_Y_ALIGNMENT_WIDTH`（LVGL），
  使失效区域在到达驱动之前四舍五入到所需边界。
  (:github:`117765`)

DMA
===

* :dtcompatible:`silabs,siwx91x-dma` 已重命名为 :dtcompatible:`silabs,udma`。
  Kconfig 选项也已重命名以与该新名称对齐
  （``DMA_SILABS_SIWX91X`` 改为 ``DMA_SILABS_SIWX91X_UDMA``，
  ``DMA_SILABS_SIWX91X_SG_BUFFER_COUNT`` 改为
  ``DMA_SILABS_SIWX91X_UDMA_DESCR_COUNT``）

* 为与其他驱动对齐，``GPDMA_SILABS_SIWX91X_DESCRIPTOR_COUNT``
  已重命名为 ``DMA_SILABS_SIWX91X_GPDMA_DESCR_COUNT``。

ESPI
====

* ECUSTOM_HOST_SUBS_INTERRUPT_EN 已弃用，
  改用允许对单个 eSPI 硬件中断进行细粒度启用/禁用控制的新 API。
  这替换了当前与 CONFIG_ESPI_PERIPHERAL_CUSTOM_OPCODE
  和所有 eSPI 驱动中单个 eSPI ACPI HW block 实例紧密耦合的
  全有或全无方法。将在下一个 Zephyr 版本中完全移除
  以留出迁移时间。

* Microchip XEC eSPI v2 驱动（:dtcompatible:`microchip,xec-espi-v2`）
  已从 MEC172x 移植以同时支持 MEC174x、MEC175x 和 MEC165xB。
  这需要若干影响使用该绑定的树外开发板的设备树更改
  (:github:`109519`)：

  * ``pcrs`` 属性已被 ``pcr-scr`` 替换，后者现在是
    单个整数，使用 ``MCHP_XEC_SCR_ENCODE(reg, bit)``
    辅助宏编码，而不是 ``<reg bit>`` cell 对。
    将现有覆盖层从 ``pcrs = <2 19>;`` 更新为
    ``pcr-scr = <MCHP_XEC_SCR_ENCODE(2, 19)>;``。

  * 仅在 MEC174x/5x/165xB 上，``girqs`` cell 现在是
    由 ``MCHP_XEC_ECIA_GIRQ_ENC(reg, bit)`` 生成的
    每个条目单个整数，而不是 ``<reg bit>`` 对。
    MEC172x 继续使用现有的 ``MCHP_XEC_ECIA(...)`` 形式。

  * eSPI 控制器节点上可用两个新的可选属性，
    用于地址空间超过 32 位的主机：
    ``host-memmap-addr-high``（内存映射逻辑设备的主机地址位 [47:32]）
    和 ``sram-bar-addr-high``（两个 SRAM BAR 的主机地址位 [47:32]）。

  * eSPI 控制器及其 host-device 子节点的 ``interrupt-names``
    已为一致性重命名。相应更新覆盖层：

    * 控制器：``rst`` → ``erst``；``vwct_0_6`` / ``vwct_7_10`` →
      ``ht_vw_bank0`` / ``ht_vw_bank1``。
      必须在 ``interrupts`` 数组中添加两个对应的中断
      （``ht_vw_bank0`` / ``ht_vw_bank1``）。
    * KBC 子节点：``kbc_obe`` / ``kbc_ibf`` → ``obe`` / ``ibf``。
    * ACPI EC 子节点：``acpi_ibf`` / ``acpi_obe`` → ``ibf`` / ``obe``。

  * 在 MEC5 SoC DTSI（MEC174x/5x/165xB）中，
    eSPI 控制器的每个 host-device 子节点
    （mailbox、KBC、ACPI EC、ACPI PM1、port92、glue、EMI、BIOS debug port 等）
    现在声明 :dtcompatible:`microchip,xec-espi-host-dev`
    所需的 ``ldn``（逻辑设备号）属性。
    为这些 SoC 覆盖或添加 host-device 子节点的树外开发板
    必须在每个节点上设置 ``ldn``。

Ethernet
========

* WIZnet 以太网驱动现在共享一组 Kconfig 选项。
  将 ``CONFIG_ETH_W5500_*``、``CONFIG_ETH_W6100_*``
  和 ``CONFIG_ETH_W6300_*`` 替换为匹配的 ``CONFIG_ETH_WIZNET_*`` 选项。

* ``ETHERNET_CONFIG_TYPE_T1S_PARAM`` 和相关
  ``NET_REQUEST_ETHERNET_SET_T1S_PARAM`` 已移除。
  应改用 :c:func:`phy_set_plca_cfg` 连同
  :c:func:`net_eth_get_phy` 来设置这些参数 (:github:`108136`)。

* 在 :c:struct:`ethernet_api` 实现的函数中
  添加了一个指向 :c:struct:`net_if` 的额外参数。
  该 API 不直接暴露给应用，因此只需更新树外驱动。
  (:github:`106086`)

* :dtcompatible:`nxp,enet-mac` 的 ``pinctrl-0``
  和 ``pinctrl-names`` 设备树属性需要从 MAC 节点
  移到父以太网控制器节点。(:github:`107352`)

* NuMaker 以太网驱动已连同 ``CONFIG_ETH_NUMAKER`` 一起移除。
  NuMaker EMAC 现在由 :kconfig:option:`CONFIG_ETH_NUMAKER_DWC_ETHER_1000`
  驱动，即通用的 Synopsys DesignWare MAC 驱动，
  需要在设备树中有 MDIO 控制器和 PHY。
  树外开发板必须在其 pinctrl 状态中启用带有 MDC 和 MDIO 引脚的
  ``mdio`` 节点，向其添加 PHY，并用 ``phy-handle``
  将 ``emac`` 节点指向它。
  :dtcompatible:`nuvoton,numaker-ethernet` 的 ``phy-addr`` 属性已移除。

* :c:struct:`dsa_api` 的 ``port_generate_random_mac`` 已移除。
  此外，:c:struct:`dsa_port_config` 现在使用
  :c:struct:`net_eth_mac_config` 设置 MAC 地址。
  :c:struct:`dsa_port_config` 的 ``mac_addr`` 和
  ``use_random_mac_addr`` 成员已移除。
  树外 DSA 驱动必须更新其端口配置代码以使用新的 API 和结构体。
  (:github:`108952`)

* Kconfig 选项 ``CONFIG_ETH_NATIVE_TAP_PTP_CLOCK``
  已被 :kconfig:option:`CONFIG_PTP_CLOCK_NATIVE` 替换。
  为 native_sim PTP 时钟驱动添加了新的兼容项
  :dtcompatible:`zephyr,native-ptp-clock`。
  当存在 :dtcompatible:`zephyr,native-ptp-clock` 兼容项时
  :kconfig:option:`CONFIG_PTP_CLOCK_NATIVE` 默认启用。

* native_sim TAP 以太网驱动现在从设备树实例化，
  使用 :dtcompatible:`zephyr,native-tap` 兼容项。
  每个接口由设备树节点定义，而不是
  ``CONFIG_ETH_NATIVE_TAP_INTERFACE_COUNT`` Kconfig 选项，
  后者已移除。通过添加多个节点创建多个接口。
  以下 Kconfig 选项已移除并由设备树属性替换：

  * ``CONFIG_ETH_NATIVE_TAP_DRV_NAME`` → ``host-interface`` 属性。
  * ``CONFIG_ETH_NATIVE_TAP_MAC_ADDR`` → ``local-mac-address`` 属性。
  * ``CONFIG_ETH_NATIVE_TAP_RANDOM_MAC`` → ``zephyr,random-mac-address`` 属性。

  ``--eth-if``、``--mac-addr``、``--ipv4-addr``、``--ipv4-gw``
  和 ``--ipv4-nm`` 命令行选项仍受支持并应用于第一个接口。
  为其余接口添加了名为 ``<node>_eth-if``、``<node>_mac-addr``
  等按接口变体。

* :c:struct:`dsa_api` 的 ``port_phylink_change`` 现在是可选的。
  DSA 驱动不再需要在 PHY 链路变化时调用
  :c:func:`net_eth_carrier_on` 或 :c:func:`net_eth_carrier_off`，
  这现在由 DSA 核心处理。
  ``port_phylink_change`` 的 ``void *user_data`` 参数
  已更改为 ``const struct device *dev``，
  因此不再需要强制转换以获取设备指针。
  树外 DSA 驱动必须更新其 ``port_phylink_change`` 回调
  以匹配新的 API，并可从中删除对
  :c:func:`net_eth_carrier_on` 或 :c:func:`net_eth_carrier_off`
  的任何调用。(:github:`109671`)

* 以太网接口的 MAC 地址现在在使用
  :c:func:`net_if_up` 启动接口时检查有效性。
  如果 MAC 地址无效，接口将启动失败并记录错误。
  此检查在调用 :c:struct:`ethernet_api` 的 ``start`` 函数之前执行。
  这也适用于 native wifi 驱动。(:github:`110435`)

* Xilinx GEM 以太网驱动（:dtcompatible:`xlnx,gem`）
  已切换到使用当前的 MDIO 和 PHY 设施，
  将驱动实现拆分为独立的 MDIO 和以太网 MAC 驱动。
  驱动的自定义 PHY 管理代码已移除。
  被移除的自定义代码支持的以太网 PHY 类型，
  Marvell Alaska GBit PHY 系列和 TI TLK105/DP83822 100 MBit PHY
  均由标准（:dtcompatible:`ethernet-phy`）驱动覆盖。
  模拟 Xilinx GEM 的 QEMU 目标已相应更新，
  Zynq-7000 和 ZynqMP / UltraScale+ SoC 系列的设备树也已更新。
  (:github:`87313`)

* 使用 :c:enumerator:`ETHERNET_CONFIG_TYPE_EXTRA_TX_PKT_HEADROOM`
  请求额外发送包头空间的以太网和 Wi-Fi 驱动
  现在必须选择 :kconfig:option:`CONFIG_NET_L2_ETHERNET_EXTRA_TX_PKT_HEADROOM`。
  (:github:`112924`)

* ``ETHERNET_PTP`` 标志已从 :c:enum:`ethernet_hw_caps` 移除。
  使用 :c:func:`net_eth_get_ptp_clock`
  检查以太网接口是否有 PTP 时钟。
  树外驱动必须从其 :c:struct:`ethernet_api`
  ``get_capabilities`` 实现中移除对这些标志的任何引用。
  (:github:`112788`)

* 支持 LLDP 的以太网驱动不再需要在初始化时调用
  :c:func:`net_lldp_set_lldpdu`。
  这现在由 :c:func:`ethernet_init` 完成。(:github:`114087`)

* :dtcompatible:`infineon,xmc4xxx-ethernet` 和
  :dtcompatible:`wch,ethernet` 节点已与其父节点合并。
  兄弟 MDIO 节点不移动，因此成为这些 ``ethernet`` 节点的子节点。
  (:github:`114899`)

* ``infineon,xmc4xxx-mdio`` 的 ``mdi-port-ctrl`` 属性
  已移到父节点（:dtcompatible:`infineon,xmc4xxx-ethernet`）。
  (:github:`114899`)

* 兼容项 ``espressif,esp32-mdio``、``infineon,xmc4xxx-mdio``、
  ``nxp,enet-qos-mdio``、``nxp,s32-gmac-mdio``、``st,stm32-mdio``
  和 ``wch,mdio`` 已被 :dtcompatible:`snps,dwmac-mdio` 替换。
  (:github:`114899`)

* NXP ENET-QOS 以太网控制器（:dtcompatible:`nxp,enet-qos`）
  设备树结构已扁平化以匹配其他类似控制器。
  clocks、interrupts、``pinctrl-0``、``pinctrl-names``、
  ``phy-handle`` 和 MAC 地址属性现在直接位于
  父 ``nxp,enet-qos`` 节点上，而不是单独的子 MAC 节点。
  ``nxp,enet-qos-mac`` 兼容项及其 ``enet_mac`` 节点已移除。
  使用此控制器的树外开发板必须将属性从旧的
  ``enet_mac`` 节点上移到 ``enet`` 节点。(:github:`115952`)

* Kconfig 选项 ``CONFIG_ETH_NXP_ENET_QOS_MAC_UNIQUE_MAC_ADDRESS``
  已重命名为 :kconfig:option:`CONFIG_ETH_NXP_ENET_QOS_UNIQUE_MAC_ADDRESS`。
  设置旧名称的配置必须更新为使用新名称。(:github:`115952`)

* Synopsys DesignWare MAC 驱动现在默认过滤多播
  （:kconfig:option:`CONFIG_ETH_DWC_ETHER_MULTICAST_FILTER`），
  因此仅接收网络栈已加入的地址的多播。
  禁用该选项以如前接收所有多播。(:github:`113235`)

* 带以太网接口的开发板现在应默认启用
  :kconfig:option:`CONFIG_ETH_DRIVER`，
  而不是 :kconfig:option:`CONFIG_NET_L2_ETHERNET`。
  后者现在在前者启用时默认启用。(:github:`117121`)

Flash
=====

* :dtcompatible:`jedec,spi-nand` 现在需要 ``plane-bytes`` 属性，
  指示闪存设备中每个 plane 的大小。
  对于单 plane 设备，这应设置为与 ``size-bytes`` 相同的值。

* :dtcompatible:`st,stm32-nv-flash` 的 ``bank2-flash-size``
  属性已弃用，改用使用 ``reg`` size cell 确定闪存 bank 大小的
  新机制。除移除上述属性外，设备树无需更改。
  (:github:`114971`)

Fuel Gauge
==========

* 各种燃料表属性枚举和 union 字段已弃用，
  改用带显式单位后缀的新版本。
  应用和驱动应迁移到带单位后缀的名称。
  例如，``FUEL_GAUGE_CURRENT``（``val.current``）
  被 ``FUEL_GAUGE_CURRENT_UA``（``val.current_ua``）替换。

* 驱动一直不一致地报告 ``FUEL_GAUGE_CYCLE_COUNT`` 属性中的
  完整充电/放电循环或循环的"1/100"。
  该属性现在一致地报告完整循环，
  之前报告循环分数（即 ADP5360 和 BQ27Z746）的驱动
  已更新为报告完整循环。
  依赖旧行为的应用应更新。(:github:`112276`)

GPIO
====

* STM32 GPIO 驱动现在在尝试使用
  :c:func:`gpio_pin_configure` 在禁用状态下
  配置带上拉/下拉电阻的 GPIO 引脚时返回 ``-EINVAL``。
  驱动之前返回 ``0`` 而未实际尊重这些标志
  （未启用 PU/PD 电阻）。遇到此错误的应用
  应从提供给 :c:func:`gpio_pin_configure` 的 ``flags`` 中
  移除 :c:macro:`GPIO_PULL_UP`/ :c:macro:`GPIO_PULL_DOWN`；
  这将产生与之前相同的行为，因为这些标志实际上被忽略。
  (:github:`104690`)

* 在 STM32F1 系列上，GPIO 输出引脚现在使用 50 MHz 最大速度
  而不是 10 MHz。(:github:`104690`)

* :dtcompatible:`awinic,aw9523b-gpio` 驱动不再有 ``reset-gpios`` 属性。
  这已移到父 :dtcompatible:`awinic,aw9523b` MFD 设备。

Haptics
=======

* ``cirrus,cs40l5x`` 兼容项已被变体特定兼容项替换：
  :dtcompatible:`cirrus,cs40l50`、:dtcompatible:`cirrus,cs40l51`、
  :dtcompatible:`cirrus,cs40l52` 和 :dtcompatible:`cirrus,cs40l53`。
  使用旧兼容项的应用必须相应更新其设备树节点。

* :dtcompatible:`ti,drv2605` 的 ``vib-rated-mv`` 和
  ``vib-overdrive-mv`` 属性现在默认为设备复位值
  1362 mV 和 3075 mV，而不是 3200 mV。
  需要之前驱动级别的开发板必须显式设置它们。

HWSPINLOCK
==========

* ``num-locks`` DeviceTree 属性现在是 hwspinlock
  控制器绑定的标准必需属性。
  每个 hwspinlock 控制器节点必须设置它，
  树外绑定必须删除其自身的 ``num-locks``
  ``type``/``required`` 声明。

* :c:func:`hw_spin_lock`、:c:func:`hw_spin_trylock`
  和 :c:func:`hw_spin_unlock` 不再接受
  ``hwspinlock_ctx_t *`` 参数；
  每锁 Zephyr 自旋锁现在位于驱动配置中。
  ``struct hwspinlock_context``、``hwspinlock_ctx_t``、
  :c:struct:`hwspinlock_dt_spec` 的 ``ctx`` 成员
  和 ``HWSPINLOCK_CTX_INITIALIZER`` 已移除。
  :c:func:`hw_spin_lock_dt`、:c:func:`hw_spin_trylock_dt`
  和 :c:func:`hw_spin_unlock_dt` 辅助函数不变。
  因此，所有引用同一硬件自旋锁的
  :c:macro:`HWSPINLOCK_DT_SPEC_GET` 实例
  现在共享单个 Zephyr 自旋锁，而不是各自拥有一个。

* 硬件自旋锁驱动现在必须将 :c:struct:`hwspinlock_driver_config`
  嵌入其配置结构体的第一个成员，
  使用 :c:macro:`HWSPINLOCK_COMMON_CONFIG_FROM_DT_INST`
  （或 :c:macro:`HWSPINLOCK_COMMON_CONFIG_FROM_DT_NODE`）初始化，
  并使用 :c:macro:`HWSPINLOCK_SPINLOCK_ARRAY_DECLARE`
  声明支撑自旋锁数组。

MHU
===

* FSP MHU 驱动的设备树绑定已更新：

  * ``channel`` 属性已重命名为 ``unit``，
    且现在是必需的。
  * ``tx-mask`` 和 ``rx-mask`` 属性已合并为
    单个 ``channel-mask`` 属性。
  * 不再需要 ``shared-memory`` 属性；
    共享内存改由名为 ``mhu_shmem`` 的
    单个 ``zephyr,memory-region`` 节点提供，
    该节点替换了按单元的 ``mmio-sram`` 节点，
    并使链接器为 FSP MHU 驱动发出 ``__mhu_shmem_start``。
    没有此内存区域的开发板将因对该符号的
    未定义引用而链接失败。

  例如：

  .. code-block:: devicetree

     /* 之前 */
     mhu3_shm: memory@62f01018 {
             compatible = "mmio-sram";
             reg = <0x62f01018 0x8>;
     };

     mbox3: mhu@40400060 {
             channel = <3>;
             tx-mask = <0x00000002>;
             rx-mask = <0x00000001>;
             shared-memory = <&mhu3_shm>;
     };

     /* 之后 */
     mhu_shmem: memory-region@62f01000 {
             compatible = "zephyr,memory-region";
             reg = <0x62f01000 0x1000>;
             zephyr,memory-region = "mhu_shmem";
     };

     mbox3: mhu@40400060 {
             unit = <3>;
             channel-mask = <0x1>;
     };

MSPI
====

* MSPI 设备绑定文件名现在使用 ``(vendor,)device-mspi.yaml``
  用于 MSPI 特定变体，而设备树 ``compatible`` 字符串
  描述设备本身而不是编码 MSPI 总线。
  建议开发板、扩展板、示例、测试和树外设备树覆盖层
  按如下方式更新 MSPI 子节点兼容项：

  * ``jedec,mspi-nor`` -> ``jedec,nor``
  * ``mspi-atxp032`` -> ``atxp032``
  * ``mspi-is25xX0xx`` -> ``is25xX0xx``
  * ``mspi-aps6404l`` -> ``aps6404l``
  * ``mspi-aps-z8`` -> ``aps-z8``
  * ``zephyr,mspi-emul-device`` -> ``zephyr,emul-device-mspi``
  * ``zephyr,mspi-emul-flash`` -> ``zephyr,emul-flash``

  建议树外 MSPI 设备驱动同样更新
  ``DT_DRV_COMPAT`` 和生成的设备树 Kconfig 符号引用
  为新兼容项名称。如果驱动、示例或测试
  必须确保其中一个通用兼容项在 MSPI 总线上实例化，
  添加显式 MSPI 总线检查，例如 Kconfig 中的
  ``dt_compat_on_bus`` 或测试元数据中的
  ``dt_compat_on_bus`` 过滤器。

* MSPI 内存映射功能已从 "XIP" 重命名为 "MEMMAP"，
  因为 XIP（:kconfig:option:`CONFIG_XIP`）
  是 Zephyr 中的软件配置概念，
  而 MSPI 功能仅内存映射设备，
  可用于数据访问以及代码执行 (:github:`104657`)。
  MSPI API 是实验性的，因此不提供弃用别名。
  树外用户必须更新：

  * ``CONFIG_MSPI_XIP`` -> :kconfig:option:`CONFIG_MSPI_MEMMAP`
  * ``CONFIG_FLASH_MSPI_XIP_READ`` -> :kconfig:option:`CONFIG_FLASH_MSPI_MEMMAP_READ`
  * ``struct mspi_xip_cfg`` -> ``struct mspi_memmap_cfg``
  * ``enum mspi_xip_permit`` -> ``enum mspi_memmap_permit``
    及其值 ``MSPI_XIP_READ_WRITE``/``MSPI_XIP_READ_ONLY`` ->
    ``MSPI_MEMMAP_READ_WRITE``/``MSPI_MEMMAP_READ_ONLY``
  * ``mspi_xip_config`` -> :c:func:`mspi_memmap_config`
    和 ``xip_config`` 驱动 API 条目 -> ``memmap_config``
  * ``MSPI_XIP_CONFIG_DT``/``MSPI_XIP_CONFIG_DT_INST``/``MSPI_XIP_CONFIG_DT_NO_CHECK``
    -> ``MSPI_MEMMAP_CONFIG_DT``/``MSPI_MEMMAP_CONFIG_DT_INST``/``MSPI_MEMMAP_CONFIG_DT_NO_CHECK``
  * ``MSPI_XIP_CFG_STRUCT_DECLARE``/``MSPI_XIP_BASE_ADDR_DECLARE``/``MSPI_XIP_BASE_ADDR_INIT``
    -> ``MSPI_MEMMAP_CFG_STRUCT_DECLARE``/``MSPI_MEMMAP_BASE_ADDR_DECLARE``/``MSPI_MEMMAP_BASE_ADDR_INIT``
  * 设备树属性 ``xip-config`` -> MSPI 设备节点上的 ``memmap-config``

Nordic
======

* :dtcompatible:`nordic,owned-memory` 和
  :dtcompatible:`nordic,owned-partitions` 的
  ``owner-id``、``perm-read``、``perm-write``、``perm-execute``、
  ``perm-secure`` 和 ``non-secure-callable`` 属性已移除。
  改用 ``nordic,access``，例如
  ``<NRF_OWNER_ID_APPLICATION NRF_PERM_RW>``。
  所有者不再隐式：省略的 ``owner-id``
  过去意味着正在编译的域，因此现在必须显式命名。

NXP
===

* :kconfig:option:`CONFIG_MCUX_LPTMR_TIMER`
  不再基于 ``/chosen/zephyr,system-timer`` chosen 节点
  与 :dtcompatible:`nxp,lptmr` 兼容而默认为 ``y``。
  依赖 LPTMR 作为系统定时器的树外 SoC 和开发板
  现在必须在其 ``Kconfig.defconfig`` 中显式默认该符号
  （例如 ``default y if PM``）。

* 启用 :kconfig:option:`CONFIG_PM` 时，Kinetis KE1xF
  不再需要开发板覆盖层来指定系统定时器。
  SoC DTSI 现在设置 ``zephyr,system-timer`` chosen 属性，
  因此添加了 Zephyr 4.4 迁移指南中描述的覆盖层的开发板
  可以删除它。

* NXP LPC DTSI 文件已从扁平目录 ``dts/arm/nxp/lpc/``
  重新组织为按系列的子目录。
  直接 include 这些文件的树外开发板必须更新其 include。

  新的子目录布局为：

  ========================  ========================================
  LPC series                New location
  ========================  ========================================
  LPC11U6x                  ``dts/arm/nxp/lpc/lpc11u6x/``
  LPC51U68                  ``dts/arm/nxp/lpc/lpc51u68/``
  LPC54xxx                  ``dts/arm/nxp/lpc/lpc54xxx/``
  LPC55xxx                  ``dts/arm/nxp/lpc/lpc55xxx/``
  LPC84x                    ``dts/arm/nxp/lpc/lpc84x/``
  ========================  ========================================

  示例：

  .. code-block:: dts

    /* 之前 */
    #include <nxp/lpc/nxp_lpc55S6x.dtsi>

    /* 之后 */
    #include <nxp/lpc/lpc55xxx/nxp_lpc55S6x.dtsi>

* NXP Kinetis DTSI 文件已从扁平目录 ``dts/arm/nxp/kinetis/``
  重新组织为按系列的子目录。
  直接 include 这些文件的树外开发板必须更新其 include。

  新的子目录布局为：

  ========================  ========================================
  Kinetis series            New location
  ========================  ========================================
  K2X                       ``dts/arm/nxp/kinetis/k2x/``
  K32Lx                     ``dts/arm/nxp/kinetis/k32lx/``
  K6X                       ``dts/arm/nxp/kinetis/k6x/``
  K8X                       ``dts/arm/nxp/kinetis/k8x/``
  KE1xF                     ``dts/arm/nxp/kinetis/ke1xf/``
  KE1xZ                     ``dts/arm/nxp/kinetis/ke1xz/``
  KL2X                      ``dts/arm/nxp/kinetis/kl2x/``
  KV5X                      ``dts/arm/nxp/kinetis/kv5x/``
  KWX                       ``dts/arm/nxp/kinetis/kwx/``
  ========================  ========================================

  示例：

  .. code-block:: dts

    /* 之前 */
    #include <nxp/kinetis/nxp_k66.dtsi>

    /* 之后 */
    #include <nxp/kinetis/k6x/nxp_k66.dtsi>

* NXP MCX DTSI 文件已从扁平目录 ``dts/arm/nxp/mcx/``
  重新组织为按系列的子目录。
  直接 include 这些文件的树外开发板必须更新其 include。

  新的子目录布局为：

  ========================  ========================================
  MCX series                New location
  ========================  ========================================
  MCXA                      ``dts/arm/nxp/mcx/mcxa/``
  MCXC                      ``dts/arm/nxp/mcx/mcxc/``
  MCXE                      ``dts/arm/nxp/mcx/mcxe/``
  MCXL                      ``dts/arm/nxp/mcx/mcxl/``
  MCXN                      ``dts/arm/nxp/mcx/mcxn/``
  MCXW                      ``dts/arm/nxp/mcx/mcxw/``
  ========================  ========================================

  示例：

  .. code-block:: dts

    /* 之前 */
    #include <nxp/mcx/nxp_mcxc242.dtsi>

    /* 之后 */
    #include <nxp/mcx/mcxc/nxp_mcxc242.dtsi>

* NXP MCXN 系列获得了为 mcxn547、mcxn947 和 mcxn236
  准备的专用按部件 composer DTSI 文件
  （``nxp_mcxn547.dtsi``、``nxp_mcxn947.dtsi``
  和 ``nxp_mcxn236.dtsi``），与本次发布新增的
  mcxn546、mcxn946 和 mcxn235 phantom 部件并列。
  这些文件中的每一个仅 include 现有的系列文件
  （分别为 ``nxp_mcxn54x.dtsi``、``nxp_mcxn94x.dtsi``
  和 ``nxp_mcxn23x.dtsi``）而无覆盖，
  且 mcxn547、mcxn947 和 mcxn236 的树内开发板
  现在 include 新的按部件文件。
  系列文件本身不变，直接 include 时仍可用，
  因此这不是必需的迁移，
  但这些三个部件的树外开发板
  可能希望切换到新的按部件文件
  以与系列其余部分保持一致。

  示例：

  .. code-block:: dts

    /* 之前 */
    #include <nxp/mcx/mcxn/nxp_mcxn94x.dtsi>

    /* 之后 */
    #include <nxp/mcx/mcxn/nxp_mcxn947.dtsi>

* NXP i.MX RT DTSI 文件已从扁平目录 ``dts/arm/nxp/imxrt/``
  重新组织为按系列的子目录。
  直接 include 这些文件的树外开发板必须更新其 include。

  新的子目录布局为：

  ========================  ========================================
  i.MX RT series            New location
  ========================  ========================================
  RT10xx                    ``dts/arm/nxp/imxrt/imxrt10xx/``
  RT11xx                    ``dts/arm/nxp/imxrt/imxrt11xx/``
  RT5xx                     ``dts/arm/nxp/imxrt/imxrt5xx/``
  RT6xx                     ``dts/arm/nxp/imxrt/imxrt6xx/``
  RT7xx                     ``dts/arm/nxp/imxrt/imxrt7xx/``
  RT118x                    ``dts/arm/nxp/imxrt/imxrt118x/``
  ========================  ========================================

  示例：

  .. code-block:: dts

    /* 之前 */
    #include <nxp/imxrt/nxp_rt1060.dtsi>

    /* 之后 */
    #include <nxp/imxrt/imxrt10xx/nxp_rt1060.dtsi>

* i.MX RT118x 开发板现在 include 单个按部件-core composer 文件
  ``nxp_rt118<part>_cm<core>.dtsi``，
  而不是系列-core 文件加单独的部件覆盖层。
  树外开发板必须相应更新其设备树 include (:github:`110228`)。

  之前需要系列文件加部件覆盖层的部件示例：

  .. code-block:: dts

    /* 之前 */
    #include <nxp/imxrt/nxp_rt118x_cm7.dtsi>
    #include <nxp/imxrt/nxp_rt1186.dtsi>

    /* 之后 */
    #include <nxp/imxrt/imxrt118x/nxp_rt1186_cm7.dtsi>

* i.MX RT7xx 开发板现在 include 单个按部件-core composer 文件
  ``nxp_<part>_<core>.dtsi``，而不是系列-core 文件。
  树外开发板必须相应更新其设备树 include。

  之前需要系列文件的部件示例：

  .. code-block:: dts

    /* 之前 */
    #include <nxp/imxrt/imxrt7xx/nxp_rt7xx_cm33_cpu0.dtsi>

    /* 之后 */
    #include <nxp/imxrt/imxrt7xx/nxp_rt798s_cm33_cpu0.dtsi>

* NXP SoC 引脚控制头文件位于 ``hal_nxp`` 的 ``dts/nxp/`` 树下，
  已重新组织以镜像 ``dts/arm/nxp/<family>/<series>/`` 布局：
  每个 SoC ``*-pinctrl.h`` / ``*-pinctrl.dtsi`` 文件
  移入 ``pinctrl/`` 子目录。
  直接 include 这些 SoC 引脚控制头文件的树外开发板
  必须更新其 include。

  按系列组织的系列（i.MX RT、Kinetis、LPC、MCX）
  将其头文件放在 ``<family>/<series>/pinctrl/``；
  扁平的系列（i.MX、S32、RW）
  将其头文件放在系列级的 ``<family>/pinctrl/`` 目录中。
  Kinetis 额外为之前没有的部件添加新的系列目录
  （``k0x``、``km3x``、``kv3x``）。
  此外，之前的 ``nxp_imx`` 目录已拆分：
  ``nxp_imx/rt/`` 成为 ``imxrt/`` 系列，
  其余 i.MX 应用处理器成为扁平的 ``imx/`` 系列。

  示例：

  .. code-block:: dts

    /* 之前 */
    #include <nxp/nxp_imx/rt/mimxrt1151dvm8b-pinctrl.dtsi>
    #include <nxp/nxp_imx/mimx8ml8dvnlz-pinctrl.dtsi>
    #include <nxp/kinetis/MK64FN1M0VLL12-pinctrl.h>

    /* 之后 */
    #include <nxp/imxrt/imxrt11xx/pinctrl/mimxrt1151dvm8b-pinctrl.dtsi>
    #include <nxp/imx/pinctrl/mimx8ml8dvnlz-pinctrl.dtsi>
    #include <nxp/kinetis/k6x/pinctrl/MK64FN1M0VLL12-pinctrl.h>

PWM
===

* :dtcompatible:`microchip,xec-pwm` 的 ``pcrs`` 属性
  （数组类型）已被 ``pcr-scr``（int 类型）替换，
  使用编码的 PCR 寄存器索引和位位置宏
  (:github:`104570`)。

* 自 Zephyr v3.3.0 起已弃用的 STM32 PWM DT 绑定宏
  ``PWM_STM32_COMPLEMENTARY`` 不再定义。
  应改用 ``STM32_PWM_COMPLEMENTARY``。

* :dtcompatible:`nxp,ctimer-pwm` 现在通过通用
  :ref:`mux <mux_api>` 子系统路由其输入捕获信号。
  ``inputmux-connections`` 属性已移除；
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从定时器节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* :dtcompatible:`nxp,sctimer-pwm` 现在通过通用
  :ref:`mux <mux_api>` 子系统路由其输入捕获信号。
  ``input-capture-connections`` 属性已移除；
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从定时器节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 STM32 上，PWM 驱动的 ``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`st,stm32-inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP Kinetis 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP S32 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 Microchip XEC 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`microchip,xec-inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 Analog Devices MAX32 上，``input-capture`` 和
  ``input-capture-connections`` 设备树属性已移除。
  输入捕获现在通过通用 :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`adi,max32-inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 Silicon Labs SiWx 上，``input-capture`` 和
  ``input-capture-connections`` 设备树属性已移除。
  输入捕获现在通过通用 :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`silabs,siwx-inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 Espressif 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`espressif,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 Infineon 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`infineon,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 TI 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`ti,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 WCH 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`wch,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 ITE 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`ite,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 Bouffalo 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`bouffalo,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 Renesas 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`renesas,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 Sifive 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`sifive,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 Nordic 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nordic,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP S32K3 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP S32G 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP S32N 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP S32Z 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP i.MX 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP i.MX RT 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP Kinetis 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP LPC 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP MCX 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP RW 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP S32 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP i.MX 8M 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP i.MX 8Q 上，``input-capture`` 和 ``input-capture-connections``
  设备树属性已移除。输入捕获现在通过通用
  :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP i.MX 8M Plus 上，``input-capture`` 和
  ``input-capture-connections`` 设备树属性已移除。
  输入捕获现在通过通用 :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP i.MX 8Q Plus 上，``input-capture`` 和
  ``input-capture-connections`` 设备树属性已移除。
  输入捕获现在通过通用 :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP i.MX 8QM 上，``input-capture`` 和
  ``input-capture-connections`` 设备树属性已移除。
  输入捕获现在通过通用 :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP i.MX 8QXP 上，``input-capture`` 和
  ``input-capture-connections`` 设备树属性已移除。
  输入捕获现在通过通用 :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)

* 在 NXP i.MX 8QM Plus 上，``input-capture`` 和
  ``input-capture-connections`` 设备树属性已移除。
  输入捕获现在通过通用 :ref:`mux <mux_api>` 子系统路由。
  使用 INPUTMUX 控制器节点（:dtcompatible:`nxp,inputmux`）
  描述路由，并从 PWM 节点的 ``mux-states`` 属性引用它。
  (:github:`112088`)