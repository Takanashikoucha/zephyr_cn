:orphan:

.. _zephyr_2.5:

Zephyr 2.5.0
#############

我们很高兴地宣布 Zephyr RTOS 2.5.0 版本发布。

本版本的主要增强包括：

* 引入对 SPARC 处理器架构及 LEON 处理器实现的支持。
* 增加线程局部存储（TLS）支持
* 增加对每线程运行时统计的支持
* 增加在 X86 上使用 LLVM 构建的支持
* 增加基于条件变量的新同步机制
* 增加按需分页（demand paging）支持，X86 上提供初步支持。

以下各节按组件提供详细的变更列表。

安全漏洞相关
******************************

本版本修复了以下 CVE：

* CVE-2021-3323：保密期至 2021-04-14
* CVE-2021-3321：保密期至 2021-04-14
* CVE-2021-3320：保密期至 2021-04-14

更详细的信息可在以下地址找到：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

已知问题
************

您可以通过 GitHub 界面列出所有带 `bug 标签
<https://github.com/zephyrproject-rtos/zephyr/issues?q=is%3Aissue+is%3Aopen+label%3Abug>`_
的 issue 来查看当前所有已知问题。

API 变更
***********

* 移除了 SETTINGS_USE_BASE64 支持，因为它已被弃用两个多版本。

* :c:func:`lwm2m_rd_client_start` 函数现在接受一个额外的
  ``flags`` 参数，可用于配置当前 LwM2M 客户端会话，
  例如在当前会话中启用引导（bootstrap）流程。

* LwM2M execute 现在支持参数。execute 回调
  :c:type:`lwm2m_engine_execute_cb_t` 扩展了一个 ``args`` 参数，
  它指向包含参数的 CoAP 负载，以及一个 ``args_len`` 参数
  用于指示 ``args`` 数据的长度。

* 更改了 vcnl4040 dts 绑定中属性 'proximity-trigger' 的默认值。
  将默认值改为与该属性对应的硬件 POR 状态一致。

* :c:func:`clock_control_async_on` 函数现在以 ``callback`` 和
  ``user_data`` 作为参数，而不是使用包含链表节点、回调和用户数据的结构体。

* :c:func:`mqtt_keepalive_time_left` 函数现在在通过把 ``CONFIG_MQTT_KEEPALIVE``
  设置为 0 禁用了保活消息时返回 -1。

* ``CONFIG_LEGACY_TIMEOUT_API`` 模式已被移除。所有内核
  超时使用必须使用新风格的 k_timeout_t 类型，而不是
  已弃用的毫秒计数。

* :c:func:`coap_pending_init` 函数现在接受一个额外的 ``retries``
  参数，可指定可确认消息的最大重传次数。

* ``CONFIG_BT_CTLR_CODED_PHY`` 现在在同时构建蓝牙主机和控制器时
  默认禁用。

* :c:func:`coap_packet_append_payload` 函数现在以指向
  常量缓冲区的指针作为 ``payload`` 参数，而不是指向可写缓冲区的指针。

* :c:func:`coap_packet_init` 函数现在以指向
  常量缓冲区的指针作为 ``token`` 参数，而不是指向可写缓冲区的指针。

* 新增 :ref:`regulator_api` API 以支持控制电源。
  稳压器（regulator）还可以与设备树节点关联，使驱动能够确保
  其访问的设备已上电。对于仅使用 GPIO 的简单稳压器，
  设备树属性 ``supply-gpios`` 被定义为标准方式，
  用于在支持电源控制的节点中标识控制信号。

* :c:type:`fs_file_t` 对象现在必须在使用前
  调用 :c:func:`fs_file_t_init` 进行初始化。

* :c:type:`fs_dir_t` 对象现在必须在使用前
  调用 :c:func:`fs_dir_t_init` 进行初始化。

本版本中弃用的内容
==========================

* Nordic nRF5340 PDK 板已弃用，计划在 2.6.0 中移除。
* ARM Musca-A 板和 SoC 支持已弃用，计划在 2.6.0 中移除。

* DEVICE_INIT 已弃用，建议直接使用 DEVICE_DEFINE。

* DEVICE_AND_API_INIT 已弃用，建议改用 DEVICE_DT_INST_DEFINE 和
  DEVICE_DEFINE。

* 蓝牙

  * :c:func:`bt_set_id_addr` 函数已弃用，请改用
    :c:func:`bt_id_create`，并在调用 :c:func:`bt_enable`
    之前使用。当 ``CONFIG_PRIVACY`` 启用时，
    此情况下应用必须提供一个有效的 IRK。

本版本中移除的 API
===========================

* 蓝牙

  * 已弃用的 BT_LE_SCAN_FILTER_DUPLICATE 定义已移除，
    请改用 BT_LE_SCAN_OPT_FILTER_DUPLICATE。
  * 已弃用的 BT_LE_SCAN_FILTER_WHITELIST 定义已移除，
    请改用 BT_LE_SCAN_OPT_FILTER_WHITELIST。
  * 已弃用的 bt_le_scan_param::filter_dup 参数已移除，
    请改用 bt_le_scan_param::options。
  * 已弃用的 bt_conn_create_le() 函数已移除，
    请改用 bt_conn_le_create()。
  * 已弃用的 bt_conn_create_auto_le() 函数已移除，
    请改用 bt_conn_le_create_auto()。
  * 已弃用的 bt_conn_create_slave_le() 函数已移除，
    请改用 bt_le_adv_start()，并将 bt_le_adv_param::peer
    设置为远端对等设备的地址。
  * 已弃用的 BT_LE_ADV_* 宏已移除，
    请改用 BT_GAP_ADV_* 枚举。
  * 已弃用的 bt_conn_security 函数已移除，
    请改用 bt_conn_set_security。
  * 已弃用的 BT_SECURITY_* 定义 NONE、LOW、MEDIUM、HIGH、FIPS
    已移除，请改用 L0、L1、L2、L3、L4 定义。
  * 已弃用的 BT_HCI_ERR_AUTHENTICATION_FAIL 定义已移除，
    请改用 BT_HCI_ERR_AUTH_FAIL。

* 内核

  * 已弃用的 k_mem_pool API 已完全移除
    （上一个版本中它由 k_heap 支撑，但保持了
    兼容的 API）。现在所有实例化的堆都必须是
    sys_heap/k_heap。请注意，新风格的堆是通用
    分配器，对块对齐/拆分不做同样的保证。
    有此类需求的应用应考虑移植其逻辑，
    或者参考 k_mem_slab 工具。

本版本中的稳定 API 变更
==================================

内核
******

* 增加对每线程运行时统计的支持
* 增加基于条件变量的新同步机制
* 线程局部存储（TLS）

  * 为以下架构引入线程局部存储支持：

    * ARC
    * Arm Cortex-M
    * Arm Cortex-R
    * AArch64
    * RISC-V
    * Sparc
    * x86 和 x86_64
    * Xtensa

  * 这使得用 ``__thread`` 关键字声明的变量
    可以按线程分配，每个线程拥有这些变量的独立副本。
  * 通过 :kconfig:option:`CONFIG_THREAD_LOCAL_STORAGE` 启用。
  * 如果启用了 :kconfig:option:`CONFIG_ERRNO_IN_TLS`
    （与 :kconfig:option:`CONFIG_ERRNO` 一起），
    ``errno`` 可以存储在 TLS 中。
    这使得用户线程无需系统调用即可访问 ``errno`` 的值。

* 内存管理

  * 为物理内存增加了页帧管理，用于跟踪
    每个页帧的状态。
  * 增加了 :c:func:`k_mem_map`，允许应用通过
    匿名内存映射扩大可用的数据空间。
  * 增加了 :c:func:`k_mem_free_get`，返回剩余的
    物理匿名内存量。
  * 分页结构现在必须预分配，因此映射内存时
    无需进行内存分配。由于此原因，
    :c:func:`arch_mem_map` 不再可能失败。

* 按需分页

  * 引入了按需分页框架，以及自定义逐出算法
    和后备存储（backing store）实现的基础设施。
  * 当前整个内核都被固定（pinned），
    剩余的物理内存可用于分页。

架构
*************

* ARC

  * 修复了 ARC HS 在启用一个中断 bank 和快速中断（FIRQ）时的运行
  * 增强了 SMP 支持
  * 改进了 mdb west runner，支持基于 nSIM 的
    仿真配置
  * 改进了 mdb west runner，支持在真实硬件（基于 FPGA）上
    运行基于 nSIM 的配置
  * 增加了介绍 Zephyr 在 ARC 处理器上支持状态的文档页
  * 为基于 nSIM 的配置增加了覆盖率支持
  * ARC 改用上游 OpenOCD
  * 对 ARC MWDT 工具链基础设施的各种小修复/改进

* ARM

  * AARCH32

    * 引入了链式加载（chain-loadable）Zephyr
      固件镜像的功能，用于在系统早期启动时强制
      初始化内部架构状态（Cortex-M）。
    * 将默认的浮点服务模式改为
      共享 FP 寄存器模式。
    * 通过在线程中实现动态惰性 FP 寄存器压栈，
      增强了 Cortex-M 共享 FP 寄存器模式。
    * 增加了对 Cortex-R7 变体的初步支持。
    * 修复了 Cortex-M 系统调用中的内联汇编代码。
    * 增强并修复了 Cortex-M TCS 支持。
    * 在单线程 Cortex-M 构建（CONFIG_MULTITHREADING=n）中，
      切换到 main 之前启用中断。
    * 修复了非 XIP Cortex-M 构建中的向量表重定位。
    * 修复了 Cortex-R 中致命错误异常的异常退出例程。
    * 修复了 ARMv7-R 架构中的中断嵌套。


  * AARCH64

    * 修复了出错时的寄存器打印，并美化了崩溃转储输出
    * 移除了 CONFIG_SWITCH_TO_EL1 符号。默认情况下，
      执行现在在启动时降到 EL1
    * 弃用了从 EL2 引导
    * 改进了启动例程中 EL3 和 EL1 的汇编代码和错误捕获
    * 在页表中启用对 EL0 的支持
    * 修复了向量表对齐
    * 引入了在 NS 模式下引导 Zephyr 的支持
    * 修复了 z_bss_zero 中的对齐错误
    * 增加了 PSCI 驱动
    * 增加了生成镜像头的能力
    * 改进了 MMU 代码和驱动

* RISC-V

  * 增加了对 PMP（物理内存保护）的支持。
    在 Zephyr 中集成 PMP 可以支持用户空间
    （含共享内存）和栈保护特性。

* SPARC

  * 增加了对 SPARC 架构的支持，兼容 SPARC V8
    规范和 SPARC ABI。
  * FPU 在共享和非共享 FP 寄存器模式下均受支持。

* x86

  * 为 Zephyr SDK 启用软浮点支持
  * ``CONFIG_X86_MMU_PAGE_POOL_PAGES`` 已移除，因为分页结构
    现在必须预分配。
  * 物理内存的映射方式已更改：

    * 这使得虚拟地址空间更小，从而需要更小的
      分页结构。
    * 当 :kconfig:option:`CONFIG_ACPI` 未启用时，
      只映射内核镜像。
    * 当 :kconfig:option:`CONFIG_ACPI` 启用时，
      保留之前映射所有物理内存的行为，
      因为带 ACPI 的平台通常不受内存限制，
      可以容纳更大的分页结构。

  * 页错误（page fault）处理器已扩展以支持按需分页。

板级与 SoC 支持
********************

* 增加了对以下 SoC 系列的支持：

  * Cypress PSoC-63
  * Intel Elkhart Lake

* 对其他 SoC 系列做了以下更改：

* ARC 板的变更：

  * 为 ARC QEMU 板增加 icount 支持
  * 为 HSDK 板增加 MWDT 编译器选项
  * 为 HSDK 板的双核配置补全 JTAG 链中缺失的 tap

* 增加了对以下 ARM 板的支持：

  * Cypress CY8CKIT_062_BLE 板

* 增加了对以下 x86 板的支持：

  * Elkhart Lake CRB 板
  * Elkhart Lake CRB 板上的 ACRN 配置
  * Elkhart Lake CRB 板上的 Slim Bootloader 配置

* 增加了对以下 SPARC 板的支持：

  * GR716-MINI LEON3FT 微控制器开发板
  * 面向 GRLIB FPGA 参考设计的通用 LEON3 板配置
  * 用于仿真 LEON3 处理器并运行内核测试的 SPARC QEMU

* 增加了对以下 NXP 板的支持：

  * LPCXpresso55S28
  * MIMXRT1024-EVK

* 增加了对以下 STM32 板和 SoC 的支持：

  * Cortex-M Trace Reference Board V1.2（SEGGER TRB STM32F407）
  * 面向 STM32 的 MikroE Clicker 2
  * STM32F103RCT6 Mini
  * ST Nucleo F303K8
  * ST Nucleo F410RB
  * ST Nucleo H723ZG
  * ST Nucleo L011K4
  * ST Nucleo L031K6
  * ST Nucleo L433RC-P
  * ST STM32L562E-DK Discovery
  * STM32F105xx 和 STM32F103xG SoC 变体
  * STM32G070xx SoC 变体
  * STM32G474xB/C SoC 变体
  * STM32L071xx SoC 变体
  * STM32L151xC 和 STM32L152xC SoC 变体

* 对 STM32 板和 SoC 系列做了以下全局更改：

  * 引脚控制配置现在通过设备树完成，
    在 pinmux.c 文件中配置引脚的现有宏已标记为弃用。
    新的引脚设置得益于 hal_stm32 模块中分发的 .dtsi 文件。
  * 通用 LL 头文件（同样在 hal_stm32 模块中分发）
    现在可用于在驱动中抽象系列引用。
  * 硬件栈保护现在是所有启用 MPU 的板的默认设置
    （SRAM > 64K），F0/G0/L0 系列除外。
  * 新增 West flash STM32CubeProgrammer runner，
    作为 STM32 板刷写的选项（需单独安装）。

* 对其他板做了以下更改：

  * CY8CKIT_062_WIFI_BT_M0：已重命名为 CY8CKIT_062_WIFI_BT。
  * CY8CKIT_062_WIFI_BT_M4：已并入 CY8CKIT_062_WIFI_BT。
  * CY8CKIT_062_WIFI_BT：现在 M0+/M4 位于同一块公共板上。
  * nRF5340 DK：在为非安全域构建 Zephyr 时，
    默认选择 TF-M 作为安全处理元件（SPE）。
  * SAM4E_XPRO：增加了对 SAM-BA ROM 引导程序的支持。
  * SAM4S_XPLAINED：增加了对 SAM-BA ROM 引导程序的支持。
  * 扩展 LPCXpresso55S69 以支持双核。
  * 增强 MIMXRT1064-EVK 以支持 QSPI flash 存储和 LittleFS。
  * 更新 MIMXRT685-EVK 以提高核心时钟频率。
  * 更新 NXP i.MX RT、Kinetis 和 LPC 板，默认启用
    硬件栈保护。
  * 修复了 NXP i.MX RT 板上的 Segger RTT 和 SystemView 支持。
  * ``qemu_x86_tiny`` 默认开启按需分页。
  * 更新 zefi.py 在构建 Zephyr 时使用交叉编译器。
  * 为 ``qemu_x86_64`` 启用代码覆盖率报告。
  * 移除了对旧版 APIC 定时器驱动的支持。
  * 为 x86 SoC 增加通用内存链接脚本。
  * 启用在 x86 SoC 中保留第一个兆字节的配置。

* 增加了对以下扩展板（shield）的支持：

  * Inventek es-WIFI 扩展板
  * Sharp 内存显示屏通用扩展板

驱动与传感器
*******************

* ADC

  * 增加对 STM32G0 系列 ADC 的支持。
  * 引入 ``adc_sequence_options::user_data`` 字段。

* CAN

  * 我们重构了配置 API。
    用户现在可以手动指定时序（定义 prop 段、
    phase 段 1、phase 段 2 和预分频器），
    或使用新引入的算法从比特率和采样点
    计算最优时序值。比特率和采样点
    也可以在设备树中指定。
    现在可以在运行时更改时序值。

  * 由于未定义行为，我们重构了 zcan_frame 结构体。
    std_id（11 位）和 ext_id（29 位）合并为
    单个 id 字段（29 位）。两个 ID 的联合体已移除。

  * 我们使 CAN 总线 API 兼容 CAN-FD。
    zcan_frame 的数据字段现在可以大于 8 字节。
    引入了一个标志用于将 zcan_frame 标记为 CAN-FD 帧。
    引入了一个标志用于在 CAN-FD 帧中启用比特率切换。
    配置 API 支持为 CAN-FD 数据相位
    提供额外的时序参数。

  * 驱动已转换为使用新的 DEVICE_DT_* 宏。

* 时钟控制

  * 增加了 NXP LPC 驱动。

* DAC

  * STM32：启用 G0 和 H7 系列支持。
  * 增加了 TI DACx3608 驱动。

* DMA

  * 从 STM32 DMAMUX 驱动初始化中移除了 kmalloc。

* EEPROM

  * 将 EEPROM API 标记为稳定。
  * 增加对 AT24Cxx 设备的支持。

* 以太网

  * 增加了对分布式交换架构（DSA）设备的支持。
    目前只有 ip_k66f 板支持 DSA。
  * 增加了对 w5500 以太网控制器的支持。
  * 重构 NXP MCUX 驱动以使用 DT_INST_FOREACH。

* Flash

  * CONFIG_NORDIC_QSPI_NOR_QE_BIT 已移除。
    应改用 quad-enable-requirements 设备树属性。
  * 在启用 MPU 的 STM32 板上，MPU_ALLOW_FLASH_WRITE
    现在是默认开启的。
  * 为 STM32H7 和 STM32L1 SoC 系列增加驱动。
  * 为 STM32 家族增加 QSPI NOR Flash 控制器支持。
  * 增加了 NXP LPC 旧版 flash 驱动。
  * 为 i.MX RT SoC 增加了 NXP FlexSPI flash 驱动。
  * 在 nRF QSPI NOR flash 驱动（nrf_qspi_nor）中
    增加了对 nRF53 系列 SoC 的支持。

* GPIO

  * 增加了 Cypress PSoC-6 驱动。
  * 增加了 Atmel SAM4L 驱动。

* 硬件信息

  * 增加了 Cypress PSoC-6 驱动。

* I2C

  * 为 lmx6x、it8xxx2 和 npcx7 平台增加驱动支持。
  * 增加了 Atmel SAM4L TWIM 驱动。
  * 在 microchip i2c 驱动中增加 I2C 从机支持。
  * 撤销 2.4 中将 I2C eeprom 从机驱动降级为
    测试的决定。它现在又是驱动了。

* I2S

* IEEE 802.15.4

  * nRF：

    * 为 nRF5340 增加 IEEE 802.15.4 支持。
    * 增加对接收失败通知的支持。

  * cc13xx/cc26xx：

    * 增加多协议无线电支持。
    * 增加 sub-ghz 支持。
    * 增加 raw 模式支持。

* 中断控制器

  * 增加了 Cypress PSoC-6 Cortex-M0+ 中断多路复用器驱动。

* memc

  * 为 STM32 家族增加 FMC/SDRAM 内存控制器

* 调制解调器（Modem）

  * 改进了 modem 接口 API 中带硬件流控的 RX。
  * 改进了命令处理器中从接口读取。
  * 修复了等待 cmd 应答时的竞争条件。
  * 增加对 Quectel bg95 modem 的支持。
  * 将 modem 命令结构体常量化以减少 RAM 占用。

  * hl7800：

    * 修复缓冲区处理问题。
    * 修复 DNS 地址设置。
    * 修复固件更新中的文件打开。
    * 修复套接字无法关闭的情况。

  * sara-r4：

    * 为 @ 提示符增加合理性超时。
    * 修复 sendto 之后的冗余等待。
    * 改进 offload_sendmsg() 支持。
    * 增加配置 RSSI 工作的 Kconfig。
    * 增加在发送数据时捕获 @ 的直接 CMD。
    * 清理 send_socket_data() 的信号量处理。

  * bg96：

    * 修复 UDP 包管理。

  * GSM：

    * 增加启动/停止 API 支持，使应用可以在需要时
      关闭 GSM/PPP modem 以省电。
    * 避免在 PPP 中为每个字节包装多路复用头。
    * 增加在网络断开时移除 PPP IPv4 ipcp 地址的支持。

* PECI

* Pinmux

  * STM32 pinmux 驱动已重构，允许使用
    设备树定义配置引脚。之前的 C 宏现在已弃用。

* PWM

  * 在 pwm_nrf5_sw 驱动中增加基于 RTC
    生成 PWM 信号的支持。
  * 增加用于捕获 PWM 脉冲宽度和周期的可选 API。
  * 为 NXP Kinetis 脉冲宽度定时器（PWT）
    增加 PWM 捕获驱动。
  * 移除了 DesignWare 和 PCA9685 控制器驱动。

* 传感器

  * 修复了 MAX17055 驱动中电流到毫安的转换。
  * 为 FXOS8700、IIS2DLPC 和 IIS2ICLX
    驱动增加多实例支持。
  * 增加了 Invensense ICM42605 驱动。
  * 增加了 NXP MCUX ACMP 驱动。
  * 修复了 FXAS21002 驱动中的陀螺仪单位。
  * 修复了 DPS310 驱动中的压力和温度寄存器。
  * 为 BMI160 驱动增加 I2C 支持。
  * 增加了 IIS2ICLX 驱动。
  * 将 ST 传感器驱动与 stmemsc HAL i/f v1.03 对齐。
  * 修复了 IIS2MDC 驱动中的温度单位。
  * 为 Bosch BMI160 加速度计增加仿真器。
  * 为 LIS2MDL 驱动增加设备电源管理支持。

* 串口

  * 为 STM32 家族增加 ASYNC API 支持。

* SPI

  * 增强 NXP MCUX Flexcomm 驱动以支持 DMA。

* 定时器

* USB

  * 重构 nrfx 驱动以使用 mem_slab 管理事件元素，
    并使用静态内存管理 OUT 端点。
  * 修复 nrfx 驱动的 ZLP 处理。
  * 为 STM32F105xx 器件增加 USB Device 模式支持。

* 视频

* 看门狗

  * 增加了 NXP i.MX RT 驱动。

* WiFi

  * eswifi：

    * 增加 uart 总线接口。这启用了所有运行
      IWIN AT 命令固件的 Inventek 模块。

  * esp：

    * 修复 esp_socket 操作的线程安全访问。
    * 修复为每个 RX 包调度独立工作线程的问题。
    * 修复只初始化一次套接字工作结构体的问题。
    * 重构 +IPD 和 +CIPRECVDATA 处理。
    * 发送数据时不再锁定调度器。
    * 增加 DHCP/静态 IP 支持。
    * 增加使用 DNS 服务器的支持。
    * 增强 CWMODE 支持。
    * 增加配置主机名的支持。
    * 增加 power-gpios 支持以启用 ESP 模块。
    * 增加 +IPD 中 32 位长度的支持。
    * 增加在初次通信后重新配置 UART 波特率的支持。
    * 通过关闭流式套接字改进包分配失败处理。

网络
**********

* CoAP：

  * 按 RFC6690 修复发现响应的格式。
  * 随机化初始 ACK 超时。
  * 重构待处理重传逻辑。
  * 修复长选项编码。

* DHCPv4：

  * 为 DHCPv4 增加 start/bound/stop 网络管理事件。
  * 修复多网络接口的超时调度。
  * 修复进入 bound 状态时的超时。
  * 修复发送失败时的无效超时。
  * 修复超时中的边界检查。
  * 修复字节序（endian）问题。
  * 为消息间隔增加随机化。
  * 将消息间隔限制在最大 64 秒。

* DNS：

  * 增加在 DNS 禁用时解析字面 IP 地址的支持。
  * 增加对 DNS 服务发现（dns-sd）的支持。
  * 修复 getaddrinfo() 以遵循套接字类型提示。

* HTTP：

  * 为 HTTP 客户端 API 增加分块（chunked）编码正文支持。

* IPv6：

  * 调整 IPv6 DAD 和 RS 超时处理。
  * 修复多个字节序问题。
  * 修复对 IPv6 地址的非对齐访问。

* LwM2M：

  * 增加维度发现支持。
  * 实现引导（bootstrap）发现。
  * 修复基于 pending/reply 的消息查找。
  * 重构 bootstrap DELETE 操作。
  * 增加路径生成宏。
  * 增加在网络出错时通知应用的方式。
  * 增加向应用通知套接字错误的回调。
  * 在生命周期变化时发送注册更新。
  * 修复 URI 解析错误情况下的 PULL 固件更新。
  * 修复分离响应处理。
  * 通知序列号从 0 开始。
  * 更高效地打包 TLV 整数。
  * 改进令牌生成。
  * 修复 bootstrap 使其变为可选。

* 其他：

  * 允许用户选择抢占式或协作式 RX/TX 线程。
  * 重构 RX 和 TX 线程优先级。
  * 仅在启用自动启动时才启动网络日志后端。
  * 增加应用同时使用 UDP/TCP 和 raw 套接字的支持。
  * 为蓝牙 IPSP 连接启用请求节点组播组注册。
  * 增加 net_buf_remove API 以操作网络缓冲区末尾的数据。
  * 为 syslog-net 增加检查，确保不设置为
    立即日志模式，因为网络日志与其不兼容。
  * 实现 SO_RCVTIMEO 套接字接收超时选项。
  * 增加在链路地址变化时更新唯一主机名的支持。
  * 为 IPv6、CAN 和 packet 套接字的 bind 调用增加加锁。
  * 增加网络管理事件监视支持。

* MQTT：

  * 在通过 MQTT_EVT_DISCONNECT 事件通知应用之前
    重置客户端状态。

* OpenThread：

  * 增加对 RCP（Radio Co-Processor）模式的支持。
  * 使无线电工作队列栈大小可配置。
  * 增加加入线程的组播地址，这些地址被添加到 Zephyr。
  * 增加 SRP Kconfig 选项。
  * 启用 CSL 和 TREL 配置选项。
  * 增加启用软件 CSMA 退避的选项。
  * 增加配置平台信息的支持。
  * 增加用于更改 Zephyr 中值的 Kconfig。
  * 移除平台配置中未使用的定义。

* 示例：

  * 增加 TagoIO IoT Cloud HTTP post 示例。
  * 修复 MQTT Docker 测试中的返回码。
  * 增加在 zperf 示例中允许 DHCPv4 或手动设置地址的支持。
  * 在 coap-server 中使用 IPv4 而非 IPv6 以支持基于 Docker 的测试。
  * 为 dumb_http_server_mt 示例增加连接管理器支持。
  * 为 dumb_http_server_mt 示例增加大文件支持。
  * 增加让 gptp 示例运行 X 秒的支持，以支持基于 Docker 的测试。
  * 为 http_client 示例增加基于 Docker 的测试。
  * 重构 civetweb 示例的代码结构并减少 RAM 占用。
  * 为 gsm_modem 示例增加 suspend/resume shell 命令。
  * 为网络日志示例增加基于 Docker 的测试支持。

* TCP：

  * 新的 TCP 协议栈默认启用。旧版 TCP 协议栈已弃用，
    但仍可用，并计划在下一个 2.6 版本中移除。
  * 增加对队列接收的乱序 TCP 数据的支持。
  * 增加在 TCP 握手未完成时终止连接的支持。
  * 增强接收 TCP RST 包的处理。
  * 修复来自 Windows 10 的 TCP 连接。

* TLS：

  * 默认使用最大分片长度（MFL）扩展。
  * 为 TLS 增加 ALPN 扩展选项。
  * 修复套接字分配失败时的 TLS 上下文泄漏。

蓝牙
*********

* 主机

  * 当启用了隐私且要向启用了隐私的对等设备
    广播时，现在必须设置 BT_LE_ADV_OPT_DIR_ADDR_RPA 选项，
    与未启用隐私时相同。

* Mesh

  * ``bt_mesh_cfg_srv`` 结构体已弃用，
    建议改用独立的 Heartbeat API
    以及用于默认状态值的 Kconfig 条目。


* BLE 拆分软件控制器

* HCI 驱动

USB
***

* USB 同步传输

  * 修复 usb_transfer_sync() 中可能的死锁。
  * 增加检查，防止在同一端点上已有传输进行时
    启动新的传输。

* USB DFU 类

  * 使 USB DFU 类兼容没有二级镜像槽的目标配置。
  * 支持在单应用槽模式下于 MCUBoot 中使用 USB DFU。
  * 为 DFU 模式增加单独的 PID，以避免主机 OS
    在切换到 DFU 模式时缓存其余描述符
    导致的问题。
  * 为 appDETACH 状态增加定时器，并修订描述符处理
    以满足规范要求。

* USB HID 类

  * 重构挂起和恢复事件之后的传输处理。

* 示例

  * 重构 MSC 示例中的磁盘和文件系统配置。
    MSC 示例可以构建为不带文件系统，
    或使用两种受支持文件系统（LittleFS 或 FATFS）之一。
    磁盘子系统可以基于 flash 或 RAM。

构建与基础设施
************************

* 改进了对额外工具链的支持：

* 设备树

  * 移除了通过 ``CONFIG_LEGACY_DEVICETREE_MACROS``
    支持旧版设备树宏的功能。所有基于设备树的代码
    都应使用 Zephyr 2.3 中引入并记录在 :ref:`dt-from-c`
    中的新设备树 API。关于 flash 分区的信息
    已移至 :ref:`flash_map_api`。
  * 现在可以在构建时解析与设备树中定义的设备
    关联的设备指针，通过 ``DEVICE_DT_GET``。
    参见 :ref:`dt-get-device`。
  * 通过新宏增强了枚举属性值的支持：

    - :c:macro:`DT_ENUM_IDX_OR`
    - :c:macro:`DT_ENUM_TOKEN`
    - :c:macro:`DT_ENUM_UPPER_TOKEN`

  * 新的硬件相关宏：

    - :c:macro:`DT_GPIO_CTLR_BY_IDX`
    - :c:macro:`DT_GPIO_CTLR`
    - :c:macro:`DT_MTD_FROM_FIXED_PARTITION`

  * 其他新的节点相关宏：

    - :c:macro:`DT_GPARENT`
    - :c:macro:`DT_INVALID_NODE`
    - :c:macro:`DT_NODE_PATH`
    - :c:macro:`DT_SAME_NODE`

  * 属性访问宏变更：

    - :c:macro:`DT_PROP_BY_PHANDLE_IDX_OR`：新宏
    - :c:macro:`DT_PROP_HAS_IDX` 现在展开为字面量 0 或 1，
      而不是求值为 0 或 1 的表达式

  * 节点之间的依赖现在通过新宏暴露：

    - :c:macro:`DT_DEP_ORD`、:c:macro:`DT_INST_DEP_ORD`
    - :c:macro:`DT_REQUIRES_DEP_ORDS`、:c:macro:`DT_INST_REQUIRES_DEP_ORDS`
    - :c:macro:`DT_SUPPORTS_DEP_ORDS`、:c:macro:`DT_INST_SUPPORTS_DEP_ORDS`

* West

  * 改进 bossac runner。它现在支持 Atmel MCU 的原生
    ROM 引导程序以及类似 Arduino 和 Adafruit UF2 的
    扩展 SAM-BA 引导程序。支持的设备
    取决于 Zephyr SDK 内部或用户路径中的 bossac 版本。
    推荐的 Zephyr SDK 版本为 0.12.0 或更新。

库/子系统
**********************

* 文件系统

  * API

    * 增加 :c:func:`fs_file_t_init` 函数用于初始化
      :c:type:`fs_file_t` 对象。

    * 增加 :c:func:`fs_dir_t_init` 函数用于初始化
      :c:type:`fs_dir_t` 对象。

  * ``CONFIG_FS_LITTLEFS_FC_MEM_POOL`` 已弃用，
    应替换为 :kconfig:option:`CONFIG_FS_LITTLEFS_FC_HEAP_SIZE`。

* 管理

  * MCUmgr

    * 增加对擦除值非 0xff 的 flash 设备的支持。
    * 增加可选校验，通过
      :kconfig:option:`CONFIG_IMG_MGMT_REJECT_DIRECT_XIP_MISMATCHED_SLOT`
      启用，用于校验上传的 Direct-XIP 二进制文件，
      将拒绝任何无法从所提供上传槽
      基地址启动的二进制文件。

  * updatehub

    * 在 UpdateHub 示例中增加对 Network Manager
      和接口 overlay 的支持。以太网是默认的接口配置，
      overlay 可用于更改默认配置
    * 增加 WIFI overlay
    * 增加 MODEM overlay
    * 增加 IEEE 802.15.4 overlay [实验性]
    * 增加 BLE IPSP overlay [实验性]
    * 增加 OpenThread overlay [实验性]。

* 设置（Settings）

* 随机数

* POSIX 子系统

* 电源管理

  * 使用一致的命名约定，采用 **pm_** 命名空间。
  * 全面改造电源状态。新的状态 :c:enum:`pm_state`
    更有意义，且与 ACPI 类似。
  * 将驻留（residency）信息和受支持的电源状态
    移至设备树，并移除相关的 Kconfig 选项。
  * 新的电源状态变更通知 API :c:struct:`pm_notifier`
  * 清理构建选项。

* LVGL

  * 库已更新至小版本 v7.6.1

* 存储

  * flash_map：增加 API 用于获取 flash_area 中
    擦除字节的值，参见 ``flash_area_erased_val()``。

* DFU

  * boot：使用 MCUBoot 的 bootutil_public 库重构，
    允许使用 MCUboot 代码库已提供的 API 实现，
    并移除 zephyr 自己的实现。

* 加密

  * mbedTLS 更新至 2.16.9

HAL
****

* HAL 现在从主树移出，作为外部模块
  存在于各自独立的仓库中。

MCUBoot
*******

* bootloader

  * 增加对硬件级故障注入和时序攻击的加固，
    参见 ``CONFIG_BOOT_FIH_PROFILE_HIGH`` 及类似的 kconfig 选项。
  * 引入抽象加密原语以简化移植。
  * 增加 ram-load 升级模式（尚未在 zephyr-rtos 中启用）。
  * 将 single-image 模式重命名为 single-slot 模式，
    参见 ``CONFIG_SINGLE_APPLICATION_SLOT``。
  * 增加补丁，在链式加载前为 Cortex M7 关闭 cache。
  * 修复 swap-move 模式中的引导。
  * 修复一个问题：如果主镜像经过填充（padding），
    被中断的 swap-move 操作可能导致设备变砖。
  * 修复一个问题：硬件栈保护在链式加载的应用
    早期初始化期间会捕获该应用。
  * 在引导前增加对 Cortex SPLIM 寄存器的复位。
  * 修复一个问题：如果 CONF_FILE 包含多个文件路径
    而非单个文件路径时出现的构建问题。
  * 在 nRF 设备上增加看门狗喂狗。
    参见 ``CONFIG_BOOT_WATCHDOG_FEED`` 选项。
  * 移除了 flash_area_read_is_empty() 移植实现函数。
  * 仅在用户选择时才初始化 ARM 核心配置，
    参见 ``CONFIG_MCUBOOT_CLEANUP_ARM_CORE``。
  * 允许串行恢复协议中镜像内的最后一个数据块
    非对齐。
  * Kconfig：仅允许 xip-mode 使用 xip-revert。
  * ext: tinycrypt：将 ctr 模式更新为 stream。
  * 使用最小 CBPRINTF 实现。
  * 默认将日志配置为 LOG_MINIMAL。
  * boot：在引导前清理 NXP MPU 配置。
  * 修复 nokogiri<=1.11.0.rc4 漏洞。
  * bootutil_public 库已抽取为 MCUboot 和
    DFU 应用共用的代码（公共 API），
    参见 ``CONFIG_MCUBOOT_BOOTUTIL_LIB``

* imgtool

  * 在 verify 期间打印镜像摘要。
  * 增加对 hex 文件也设置 confirm 标志的可能性。
  * 使用 --confirm 隐含 --pad。
  * 修复 'custom_tlvs' 参数处理。
  * 增加将固定 ROM 地址写入镜像头的支持。
  * 修复带保护 TLV 的校验。


Trusted-Firmware-M
******************

* 将 Trusted-Firmware-M 模块与上游 v1.2.0 发布同步。

文档
*************

测试与示例
*****************

  * 增加了一个示例，演示如何使用 ADC 驱动 API。
  * Sanitycheck 脚本已重命名为 twister

Issue 相关条目
*******************

自上一个 2.4.0 标记版本以来，处理了以下 GitHub issue：
* :github:`31339` - nsim_em: running tests/ztest/error_hook/ failed
* :github:`31338` - mimxrt1050_evk: running tests/kernel/fpu_sharing/float_disable/ failed
* :github:`31333` - adding a periodic k_timer causes k_msleep to never return in tests/kernel/context
* :github:`31330` - Getting started guide outdated: Step 4 - Install a toolchain
* :github:`31327` - ci compliance failures due to intel_adsp_cavs25 sample
* :github:`31316` - Issue in UDP management for BG96
* :github:`31308` - Cannot set static address when using hci_usb or hci_uart on nRF5340 attached to Linux Host
* :github:`31301` - intel_adsp_cavs15: 运行 内核 testcases 失败
* :github:`31289` - Problems building grub2 bootloader for Zephyr
* :github:`31285` - LOG resulting in incorrect output
* :github:`31282` - Kernel: Poll: Code Suspected Logic Problem
* :github:`31272` - CANOpen Sample compilation fails
* :github:`31262` - tests/kernel/threads/tls/kernel.threads.tls.userspace failing
* :github:`31259` - uart.h: Clarification required on uart_irq_tx_ready uart_irq_rx_ready
* :github:`31258` - watch dog (WWDT) timeout calculation for STM32 handles biggest timeout and rollover wrong
* :github:`31235` - Cortex-M: vector table relocation is incorrect with XIP=n
* :github:`31234` - twister: 增加 choice 用于 测试 排序 进入 subsets
* :github:`31226` - tests/drivers/dma/loop_transfer  不 使用 ztest
* :github:`31219` - newlib printk float formatting not working
* :github:`31207` - Non-existent event in asynchronous UART API
* :github:`31206` - coap.c : encoding of options with lengths larger than 268 is not proper
* :github:`31203` - fatal error: setjmp.h: No such file or directory
* :github:`31194` - twister: using unsupported fixture without defined harness causes an infinite loop during on-target test execution
* :github:`31168` - Wrong linker option syntax for printf and scanf with float support
* :github:`31158` - Ethernet (ENC424J600) with dumb_http_server_mt demo does not work
* :github:`31153` - twister 构建 的 samples/audio/sof/sample.audio.sof 失败 在...上 最多 平台
* :github:`31145` - Litex-vexriscv address misaligned with dumb_http_server example
* :github:`31143` - samples: audio: sof: compilation issue, include file not found.
* :github:`31137` - Seems like the rule ".99 tag to signify major work started, minor+1 started " not used anymore ?
* :github:`31134` - LittleFS: Error Resizing the External QSPI NOR Flash in nRF52840dk
* :github:`31114` - Bluetooth: Which coding (S2 vs S8) is used during advertising on Coded PHY?
* :github:`31100` - Recvfrom 不 returning -1 如果 UDP 和 len  太 小 用于 包
* :github:`31091` - usb: usb_transfer_sync deadlocks on disconnect/cancel transfer
* :github:`31086` - bluetooth: Resume peripheral's advertising after disconnection when using new bt_le_ext_adv_* API
* :github:`31085` - networking / openthread: ipv6 mesh-local all-nodes multicast (ff03::1) packets are dropped by zephyr ipv6 stack
* :github:`31079` - Receiving extended scans on an Adafruit nRF 52840
* :github:`31071` - board: arm: SiliconLabs: add support to development kit efm32pg_stk3401a
* :github:`31069` - net: buf: 移除 数据 从 结束 的 缓冲区
* :github:`31067` - usb: cdc_acm: compilation error without UART
* :github:`31055` - nordic: west 刷写 不 longer 支持 更改 ``CONFIG_GPIO_PINRESET`` 当...时 刷写
* :github:`31053` - LwM2M FOTA pull not working with modem (offloaded socket) driver using UART
* :github:`31044` - sample.bluetooth.peripheral_hr 构建 失败 在...上 rv32m1_vega_ri5cy
* :github:`31110` - 如何  我 overwrite west 构建 在...中 命令
* :github:`31028` - Cannot READ_BIT(RCC->CR, RCC_CR_PLL1RDY) on STM32H743 based board
* :github:`31027` - Google tests run twice
* :github:`31020` - CI build failed on intel_adsp_cavs18 when submitted a PR
* :github:`31019` - Bluetooth: Mesh: Thread competition leads to failure to open or close the scanning.
* :github:`31018` - up_squared: tests/kernel/pipe/pipe_api failed.
* :github:`31014` - Incorrect timing calculation in can_mcux_flexcan
* :github:`31008` - error: initializer element is not constant .attr = K_MEM_PARTITION_P_RX_U_RX
* :github:`30999` - updatehub with openthread build update pkg failed
* :github:`30997` - samples: net: sockets: echo_client: posix tls example
* :github:`30989` - driver : STM32 Ethernet : Pin definition for PH6
* :github:`30979` - up_squared_adsp: Twister can not capture testcases log correctly
* :github:`30972` - USB: SET_ADDRESS logic error
* :github:`30964` - Sleep calls are off on qemu_x86
* :github:`30961` - esp32 损坏 由 devicetree 设备 更新
* :github:`30955` - Bluetooth: userchan: k_sem_take failed with err -11
* :github:`30938` - samples/net/dhcpv4_client  不 工作 带 sam_e70_xplained
* :github:`30935` - 测试 net: 套接字 tcp: 增加  tls 测试
* :github:`30921` - west 刷写 失败 带  open ocd 错误
* :github:`30918` - up_squared:  tests/kernel/mem_protect/mem_protect failed.
* :github:`30893` - Remove LEGACY_TIMEOUT_API
* :github:`30872` - Convert Intel GNA driver to devicetree
* :github:`30871` - 警告 compound assignment 带 'volatile'-qualified 离开 operand  已弃用 当...时 构建 带 C++20
* :github:`30870` - Convert Intel DMIC to devicetree
* :github:`30869` - Convert designware PWM driver to devicetree
* :github:`30862` - Nordic system timer driver incompatible with LEGACY_TIMEOUT_API
* :github:`30860` - legacy timeout ticks mishandled
* :github:`30857` - SDRAM 不 工作 在...上 STM32H747I-DISCO
* :github:`30850` - iotdk: couldn't flash image into iotdk board using west flash.
* :github:`30846` - devicetree: unspecified phandle-array elements cause errors
* :github:`30822` - designator 排序 用于 field 'zcan_filter::rtr'  不 匹配 声明 排序 在...中 'const zcan_filter'
* :github:`30819` - twister: --generate-hardware-map crashes and deletes map
* :github:`30810` - 测试 内核 kernel.threads.armv8m_mpu_stack_guard 失败 在...上 nrf9160dk
* :github:`30809` - 新 testcase  失败 在...之后 3f134877 在...上 mec1501modular_assy6885
* :github:`30808` - Blueooth: Controller Response COMMAND DISALLOWED
* :github:`30805` - 构建 错误 在 tests/kernel/queue 在...中 mec15xxevb_assy6853(qemu) 平台
* :github:`30800` - STM32 usb clock from PLLSAI1
* :github:`30792` - Cannot build network echo_server for nucleo_f767zi
* :github:`30752` - ARC: passed tests marked as failed when running sanitycheck on nsim_* platforms
* :github:`30750` - Convert i2s_cavs to devicetree
* :github:`30736` - Deadlock with usb_transfer_sync()
* :github:`30730` - tests: nrf: Tests in tests/drivers/timer/nrf_rtc_timer are flaky
* :github:`30723` - libc: malloc() returns unaligned pointer, causes CPU exception
* :github:`30713` - doc: "Variable ZEPHYR_TOOLCHAIN_VARIANT is not defined"
* :github:`30712` - "make zephyr_generated_headers" regressed again - ";" separator for Z_CFLAGS instead of spaces
* :github:`30705` - STM32 PWM 驱动 生成 信号 带 错误 frequency 在...上 STM32G4
* :github:`30702` - shell 模块 损坏 在...上 LiteX/VexRiscv 在...之后 发布 zephyr-v2.1.0
* :github:`30698` - OpenThread Kconfigs should more closely follow Zephyr Kconfig recommendations
* :github:`30688` - Using openthread based  lwm2m_client cannot ping the external network address unless reset once
* :github:`30686` - getaddrinfo()  不 respect 套接字 类型
* :github:`30685` - reel_board: tests/kernel/fatal/exception/ failure
* :github:`30683` - intel_adsp_cavs15:running tests/kernel/sched/schedule_api failed
* :github:`30679` - puncover  worst-case stack analysis does not work
* :github:`30673` - cmake: zephyr_module.cmake included before ZEPHYR_EXTRA_MODULES is evaluated
* :github:`30663` - Support for TI's TMP117 Temperature Sensor.
* :github:`30657` - BT Mesh: Friendship ends if LPN publishes to a VA it is subscribed to
* :github:`30651` - sanitycheck samples/video/capture/sample.video.capture fails to build on mimxrt1064_evk
* :github:`30649` - Trouble with gpio callback on frdm k64f
* :github:`30638` - nrf pwm broken
* :github:`30636` - TCP stack locks irq's for too long
* :github:`30634` - frdm_kw41z: Current master fails compilation in drivers/pwm/pwm_mcux_tpm.c
* :github:`30624` - BLE : ATT Timeout occurred during multilink central connection
* :github:`30591` - build RAM usage printout uses prebuilt and not final binary
* :github:`30582` - Doxygen doesn't catch 错误 在...中 参数 名称 在...中 callback 函数   @typedef'd
* :github:`30574` - up_squared: tests/kernel/semaphore/semaphore failed.
* :github:`30573` - up_squared: slowdown on test execution and timing out on multiple tests
* :github:`30566` - flashing issue with ST Nucleo board H745ZI-Q
* :github:`30557` - i2c slave driver removed
* :github:`30554` - tests/kernel/fatal/exception/sentinel 测试  失败 用于 various nrf 平台
* :github:`30553` - kconfig.py 退出 带 错误 当...时 使用 multiple shields
* :github:`30548` - reel_board: tests/net/ieee802154/l2/ build failure
* :github:`30547` - reel_board: tests/net/ieee802154/fragment/ build failure
* :github:`30546` - LwM2M 执行 参数 currently 不 支持
* :github:`30541` - l2m2m: writing to resources with pre_write callback fails
* :github:`30531` - 当...时 使用 ccache, compiler identity 存储 在...中 ToolchainCapabilityDatabase  总是  相同
* :github:`30526` - 测试 驱动 定时器 测试 从 drivers.timer.nrf_rtc_timer.basic 失败 在...上 所有 nrf 平台
* :github:`30517` - Interrupt nesting is broken on ARMv7-R / LR_svc corrupted.
* :github:`30514` - reel_board: tests/benchmarks/sys_kernel/ fails
* :github:`30513` - reel_board: tests/benchmarks/latency_measure/ fails
* :github:`30509` - k_timer_remaining_get returns 不正确 值 在...上 长 定时器
* :github:`30507` - nrf52_bsim 失败 在...上 一些 测试 在...之后 merging 29810
* :github:`30488` - Bluetooth: controller: swi.h should use CONFIG_SOC_NRF5340_CPUNET define
* :github:`30486` - updatehub demo for nrf52840dk
* :github:`30483` - Sanitycheck: When platform is nsim_hs_smp, process "west flash"  become defunct, the grandchild "cld" process can't be killed
* :github:`30480` - Bluetooth: Controller: Advertising can only be started 2^16 times
* :github:`30477` - frdm_k64f: testcase  samples/subsys/canbus/canopen/ failed to be ran
* :github:`30476` - frdm_k64f: testcase samples/net/cloud/tagoio_http_post/ failed to be ran
* :github:`30475` - frdm_k64f: testcase tests/kernel/fatal/exception/ failed to be ran
* :github:`30473` - mimxrt1050_evk: testcase tests/kernel/fatal/exception/ failed to be ran
* :github:`30472` - sam_e70_xplained: the samples/net/civetweb/http_server/. waits for interface unitl timeout
* :github:`30470` - sam_e70_xplained: tesecase tests/subsys/log_core failed to run
* :github:`30468` - mesh: cfg_svr.c app_key_del passes an incorrect parameter
* :github:`30467` - replace device define macros with devicetree-based macro
* :github:`30446` - fxas21002 gyroscope reading is in deg/s
* :github:`30435` - NRFX_CLOCK_EVT_HFCLKAUDIO_STARTED not handled in clock_control_nrf.c
* :github:`30434` - 内存 map 执行 测试 case 失败 当...时 代码 coverage 启用 在...中 x86_64 平台
* :github:`30433` - zephyr client automatic joiner failed on nRF52840dk
* :github:`30432` - 不 网络 接口  查找 当...时 运行 socketcan sample
* :github:`30426` - Enforce all checkpatch warnings and move to 100 characters per line
* :github:`30423` - Devicetree: Child node of node on SPI bus itself needs reg property - Bug?
* :github:`30418` - Logging: Using asserts with LOG in high pri ISR context blocks output
* :github:`30408` - tests/kernel/sched/schedule_api is failing after 0875740 on m2gl025_miv
* :github:`30397` - tests:latency_measure is not counting semaphore results on the ARM boards
* :github:`30394` - TLS tests failing with sanitycheck (under load)
* :github:`30393` - kernel.threads.tls.userspace fails with SDK 0.12.0-beta on ARM Cortex-M
* :github:`30386` - 构建 confirmed images  不 工作
* :github:`30384` - Scheduler doesn't activate sleeping threads on native_posix
* :github:`30380` - 改进  使用 的 CONFIG_KERNEL_COHERENCE
* :github:`30378` - Bluetooth: controller: tx buffer overflow error
* :github:`30364` - TCP2  不 实现 queing 用于 incoming 包
* :github:`30362` - adc_read_async callback parameters are dereferenced pointers, making use of CONTAINER_OF impossible
* :github:`30360` - reproducible qemu_x86_64 SMP failures
* :github:`30356` - DAC header file not included in stm32 soc.h
* :github:`30354` - Regression with 'local-mac-address' enet DTS property parsing (on i.MX K6x)
* :github:`30349` - Memory protection unit fault when running socket CAN program
* :github:`30344` - Bluetooth: host: Add support for multiple advertising sets for legacy advertising
* :github:`30338` - BT Mesh LPN max. poll timeout calculated incorrectly
* :github:`30330` - tests/subsys/usb/bos/usb.bos fails with native_posix and llvm/clang
* :github:`30328` - Openthread 构建 问题 带 clang/llvm
* :github:`30322` - tests: benchmarks: latency_measure: timing measurement values are all 0
* :github:`30316` - updatehub with openthread
* :github:`30315` - Build failure: zephyr/include/generated/devicetree_unfixed.h:627:29: error: 'DT_N_S_leds_S_led_0_P_gpios_IDX_0_PH_P_label' undeclared
* :github:`30308` - 增加 可选 user 数据 field 到 设备 structure
* :github:`30307` - up_squared:  tests/kernel/device/ failed.
* :github:`30306` - up_squared: tests/kernel/mem_protect/userspace failed.
* :github:`30305` - up_squared:  tests/kernel/mem_protect/mem_protect failed.
* :github:`30304` - NRF52832 consumption too high 220uA
* :github:`30298` - regression/change in master: formatting floats and doubles
* :github:`30276` - Sanitycheck: can't find mdb.pid
* :github:`30275` - up_squared: tests/kernel/common failed (timeout error)
* :github:`30261` - 文件 不 longer 在 这 location
* :github:`30257` - 测试 内核 测试 kernel.common.stack_protection_arm_fpu_sharing.fatal 失败 在...上 nrf52 平台
* :github:`30253` - 测试 内核 测试 kernel.memory_protection.gap_filling 失败 在...上 nrf5340dk_nrf5340_cpuapp
* :github:`30372` - WEST Support clean build
* :github:`30373` - out of tree （board soc doc subsystem ...)
* :github:`30240` - Bluetooth: Mesh: PTS Test failed in friend node
* :github:`30235` - MbedTLS X509 certificate not parsing
* :github:`30232` - CMake 3.19 doesn't work with Zephyr (tracking issue w/upstream CMake)
* :github:`30230` - printk and power management incompatibility
* :github:`30229` - BinaryHandler  不 pid 文件
* :github:`30224` - stm32f4_disco: User button press is inverted
* :github:`30222` - boards: arm: nucleo_wb55rg: fails to build basic samples
* :github:`30219` - drivers: gpio: gpio_cc13xx_cc26xx: Add drive strength configurability
* :github:`30213` - usb: tests: Test usb.device.usb.device.usb_disable fails on nrf52840dk_nrf52840
* :github:`30211` - spi nor sfdp runtime: nph offset
* :github:`30207` - Mesh_demo 带  nRF52840 不 工作
* :github:`30205` - 缺失 错误 检查 的 函数 i2c_write_read() 和 dac_write_value()
* :github:`30194` - qemu_x86 crashes when printing floating point.
* :github:`30193` - reel_board: running tests/subsys/power/power_mgmt_soc failed
* :github:`30191` - 缺失 检查 的 return 值 的 settings_runtime_set()
* :github:`30189` - 缺失 错误 检查 的 函数 sensor_trigger_set()
* :github:`30187` - usb: stm32: MCU fall in deadlock when calling sleep API during USB transfer
* :github:`30183` - undefined reference to ``ring_buf_item_put``
* :github:`30179` - out of tree （board soc doc subsystem ...）
* :github:`30178` - Is there any plan to support NXP RT600 HIFI4 DSP in the zephyr project?
* :github:`30173` - OpenThread SED cannot join the network after "Update nRF5 ieee802154 driver to v1.9"
* :github:`30157` - SW based BLE Link Layer Random Advertise delay not as expected
* :github:`30153` - BSD recv() can not received huge package(may be 100kB) sustain .
* :github:`30148` - STM32G474: 写入 到 刷写 Bank 2 地址 0x08040000  不 工作 在...中 256K 刷写 版本
* :github:`30141` - qemu_x86 unexpected thread behavior
* :github:`30137` - TCP2: Handling of RST flag from server makes poll() call unable to return indefinitely
* :github:`30135` - LWM2M: 固件 URI 写入  不 工作 anymore
* :github:`30134` - 测试 驱动 uart: 测试 从 tests/drivers/uart/uart_mix_fifo_poll 失败 在...上 nrf 平台
* :github:`30133` - sensor: 驱动 lis2dh 中断 定义
* :github:`30130` - nrf_radio_power_set() should use bool
* :github:`30129` - TCP2 发送 测试
* :github:`30126` - xtensa-asm2-util.s hard coding
* :github:`30120` - sanitycheck fails for tests/bluetooth/init/bluetooth.init.test_ctlr_per_sync
* :github:`30117` - Cannot compile Zephyr project with standard macros INT8_C, UINT8_C, UINT16_C
* :github:`30106` - Refactor zcan_frame.
* :github:`30100` - twister test case selection numbers don't make any sense
* :github:`30099` - sanitycheck --build-only gets stuck
* :github:`30098` - > 非常 少数  甚至 测试 带 CONFIG_NO_OPTIMIZATIONS. 什么   general consensus about 这
* :github:`30094` - 测试 内核 fpu_sharing: 测试 在...中 tests/kernel/fpu_sharing 失败 在...上 nrf 平台
* :github:`30075` - dfu: mcuboot: fail to build with CONFIG_BOOTLOADER_MCUBOOT=n and CONFIG_IMG_MANAGER=y
* :github:`30072` - tests/net/socket/socketpair appears to mis-use work queue APIs
* :github:`30066` - CI test build with RAM overflow
* :github:`30057` - LLVM built application crash
* :github:`30037` - Documentation: Fix getting started guide for macOS around homebrew install
* :github:`30031` - stm32f4 usb - bulk in endpoint does not work
* :github:`30029` - samples: net: cloud: tagoio_http_post: Undefined initialization levels used.
* :github:`30028` - sam_e70_xplained: MPU fault with CONFIG_NO_OPTIMIZATIONS=y
* :github:`30027` - sanitycheck failures on ``tests/bluetooth/init/bluetooth.init.test_ctlr_peripheral_ext``
* :github:`30022` -  mailbox message.info 在...中  receiver 线程  不 更新
* :github:`30014` - STM32F411RE PWM support
* :github:`30010` - util or toolchain: functions for reversing bits
* :github:`29999` - nrf52840 Slave 模式  不 支持 在...上 SPI_0
* :github:`29997` - format specifies 类型 'unsigned 短 但  参数  类型 'int' 错误 在...中 网络 栈
* :github:`29995` - Bluetooth: l2cap: L2CAP/LE/REJ/BI-02-C test failure
* :github:`29994` - High bluetooth ISR latency with CONFIG_BT_MAX_CONN=2
* :github:`29992` - dma tests fail with stm32wb55 and stm32l476  nucleo boards
* :github:`29991` - Watchdog Example not working as expected on a Nordic chip
* :github:`29977` - nrf9160: use 32Mhz HFCLK
* :github:`29969` - sanitycheck fails on tests/benchmarks/latency_measure/benchmark.kernel.latency
* :github:`29968` - sanitycheck 失败  数量 的 bluetooth 测试 在...上 NRF
* :github:`29967` - sanitycheck 失败 到 构建 samples/bluetooth/peripheral_hr/sample.bluetooth.peripheral_hr_rv32m1_vega_ri5cy
* :github:`29964` - net: lwm2m: Correctly Support Bootstrap-Delete Operation
* :github:`29963` - RFC: dfu/boot/mcuboot: consider usage of boootloader/mcuboot code
* :github:`29961` - 增加 i2c 驱动 测试 用于 microchip evaluation 板
* :github:`29960` - Checkpatch compliance errors do not fail CI
* :github:`29958` - mcuboot 挂起 当...时 CONFIG_BOOT_SERIAL_DETECT_PORT 值 不 查找
* :github:`29957` - BLE Notifications limited to 1 per connection event on Zephyr v2.4.0 Central
* :github:`29954` - intel_adsp_cavs18 失败 带 堆 错误 在...上 当前 Zephyr
* :github:`29953` - 增加  sofproject as  模块
* :github:`29951` - ieee802154: cc13xx_cc26xx: raw mode support
* :github:`29945` - 缺失 错误 检查 的 函数 sensor_sample_fetch() 和 sensor_channel_get()
* :github:`29943` - 缺失 错误 检查 的 函数 isotp_send()
* :github:`29937` - XCC Build offsets.c ：FAILED
* :github:`29936` - XCC Build isr_tables.c fail
* :github:`29925` - pinctrl 错误 用于 disco_l475_iot1 板
* :github:`29921` - USB DFU with nrf52840dk (PCA10056)
* :github:`29916` - ARC: tests fail on nsim_hs with one register bank
* :github:`29913` - Question : Bluetooth mesh using long range
* :github:`29908` - devicetree: 允许 所有 GPIO flags 到  使用 由 devicetree
* :github:`29896` - 新 documentation 构建 警告
* :github:`29891` - mcumgr image upload (with smp_svr) does not work over serial/shell on the nrf52840dk
* :github:`29884` - x_nucleo_iks01a2 device tree overlay issue with stm32mp157c_dk2 board
* :github:`29883` - drivers: ieee802154: cc13xx_cc26xx: use multi-protocol radio patch
* :github:`29879` - samples/net/gptp compile failed on frdm_k64f board in origin/master (work well in origin/v2.4-branch)
* :github:`29877` - WS2812 SPI LED strip driver produces bad SPI data
* :github:`29869` - 缺失 错误 检查 的 函数 entropy_get_entropy()
* :github:`29868` - Bluetooth: Mesh: DST not checked on send
* :github:`29858` - [v1.14, v2.4] Bluetooth: Mesh: RPL cleared on LPN disconnect
* :github:`29855` - Bluetooth: Mesh: TTL max not checked on send
* :github:`29853` - multiple PRs fail doc checks
* :github:`29842` - 'imgtool' absent in requirements.txt
* :github:`29833` - Test DT_INST_PROP_HAS_IDX() inside the macros for multi instances
* :github:`29831` - 刷写 支持 用于 stm32h7 SoC
* :github:`29829` - On-PR CI needs 到 构建  subset 的 测试 用于  subset 的 平台 regardless 的  scope 的  PR 更改
* :github:`29826` - SNTP doesn't work on v2.4.0 on eswifi
* :github:`29822` - Redundant 错误 检查 的 函数 usb_set_config() 在...中 subsys/usb/class/usb_dfu.c
* :github:`29809` - gen_isr_tables.py  不 检查   IRQ 数量  在...中 bounds
* :github:`29805` - SimpleLink  不 编译 (simplelink_sockets.c)
* :github:`29796` - Zephyr API for writing to flash for STM32G474 doesn't work as expected
* :github:`29793` - Ninja 生成 错误 当...时 设置 PCAP 选项 在...中 west
* :github:`29791` - spi stm32 dma: spi
* :github:`29790` -  zephyr-app-commands 宏  不 honor :generator: 选项
* :github:`29782` - smp_svr: 刷写 zephyr.signed.bin  不 seem 到 工作 在...上 nrf52840dk
* :github:`29780` - nRF SDK hci_usb sample disconnects after 40 seconds with extended connection via coded PHY
* :github:`29776` - Check vector number and pointer to ISR in "_isr_wrapper" routine for aarch64
* :github:`29775` - TCP socket stream
* :github:`29773` - sam_e70_xplained: running samples/net/sockets/civetweb/ failed
* :github:`29772` - sam_e70_xplained:running testcase tests/subsys/logging/log_core failed
* :github:`29771` - samples: net: sockets: tcp: tcp2 server not accepting with ipv6 bsd sockets
* :github:`29769` - mimxrt1050_evk: 构建 错误 在 tests/subsys/usb/device/
* :github:`29762` - nRF53 Network core cannot start LFClk when using empty_app_core
* :github:`29758` - edtlib not reporting proper matching_compat for led nodes (and other children nodes)
* :github:`29740` - OTA 使用 线程
* :github:`29737` - up_squared: tests/subsys/power/power_mgmt failed.
* :github:`29733` - SAM0 will wake up with interrupted execution after deep sleep
* :github:`29732` - issue with ST Nucleo H743ZI2
* :github:`29730` - drivers/pcie: 在...中 内核 模式 pcie_conf_read 崩溃 当...时 使用 带 newlib
* :github:`29722` - West 刷写  不 able 到 刷写 带 openocd
* :github:`29721` - drivers/sensor/lsm6dsl: assertion/UB during interrupt handling
* :github:`29720` - samples/display/lvgl/sample.gui.lvgl 失败 到 构建 在...上 几个 板
* :github:`29716` - Dependency between userspace and memory protection features
* :github:`29713` - nRF5340 - duplicate unit-address
* :github:`29711` - 增加 BSD 套接字 选项 SO_RCVTIMEO
* :github:`29710` - 驱动 usb_dc_mcux_ehci: 驱动 损坏 构建 错误 在 所有 USB 测试 和 samples
* :github:`29707` - xtensa  xt-xcc -Wno-unused-but-set-variable  not work
* :github:`29706` - xtensa xt-xcc inline warning
* :github:`29705` - reel_board: tests/kernel/sched/schedule_api/ fails on multiple boards
* :github:`29704` - [Coverity CID :215255] Dereference before null check in tests/subsys/fs/fs_api/src/test_fs.c
* :github:`29703` - [Coverity CID :215261] Explicit null dereferenced in subsys/emul/emul_bmi160.c
* :github:`29702` - [Coverity CID :215232] Dereference after null check in subsys/emul/emul_bmi160.c
* :github:`29701` - [Coverity CID :215226] Logically dead code in soc/xtensa/intel_adsp/common/bootloader/boot_loader.c
* :github:`29700` - [Coverity CID :215253] Unintentional integer overflow in drivers/timer/stm32_lptim_timer.c
* :github:`29699` - [Coverity CID :215249] Unused value in drivers/modem/ublox-sara-r4.c
* :github:`29698` - [Coverity CID :215248] Dereference after null check in drivers/modem/hl7800.c
* :github:`29697` - [Coverity CID :215243] Unintentional integer overflow in drivers/timer/stm32_lptim_timer.c
* :github:`29696` - [Coverity CID :215241] Buffer not null terminated in drivers/modem/hl7800.c
* :github:`29695` - [Coverity CID :215235] Dereference after null check in drivers/modem/hl7800.c
* :github:`29694` - [Coverity CID :215233] Logically dead code in drivers/modem/hl7800.c
* :github:`29693` - [Coverity CID :215224] Parse warning in drivers/modem/hl7800.c
* :github:`29692` - [Coverity CID :215221] Unchecked return value in drivers/regulator/regulator_fixed.c
* :github:`29690` - NUCLEO-H745ZI-Q + OpenOCD - connect under reset
* :github:`29684` -  不 创建 multiple BLE IPSP 连接 到  相同 host
* :github:`29683` - BLE IPSP sample doesn't work on raspberry pi 4 with nrf52840_mdk board
* :github:`29681` - 增加 NUCLEO-H723ZG 板 支持
* :github:`29677` - stm32h747i_disco add ethernet support
* :github:`29675` - Remove pinmux dependency on STM32 boards
* :github:`29667` - RTT 跟踪  不 工作 使用 NXP mimxrt1064_evk
* :github:`29657` - enc28j60 on nRF52840 stalls during enc28j60_init_buffers in zephyr 2.4.0
* :github:`29654` - k_heap APIs  不 测试
* :github:`29649` - net: context: 增加 net_context API 到 检查 如果  移植  bound
* :github:`29639` - Bluetooth: host: Security procedure failure can terminate GATT client request
* :github:`29637` - 5g is microwave and 4LTE is radio or static?
* :github:`29636` - Bluetooth: Controller: Connection Parameter Update indication timeout
* :github:`29634` - 构建 错误 (Bluetooth: Mesh: 拆分 prov.c 进入 两个 分离 模块 #28457)
* :github:`29632` - GPIO interrupt support for IO expander
* :github:`29631` - 内核 提供 对齐 variant 的 k_heap_alloc
* :github:`29629` - Creating a k_thread as runtime instantiated kernel object using k_malloc causes general protection fault
* :github:`29616` - Lorawan subsystem stack: missing MLE_JOIN parameter set
* :github:`29611` - usb/class/dfu: void wait_for_usb_dfu() terminates before DFU operation is completed
* :github:`29608` - question: create runtime instantiated kernel objects in kernel mode
* :github:`29594` - x86_64: RBX being clobbered in the idle thread
* :github:`29590` - ARM: FPU: using Unshared FP Services mode can still result in corrupted floating point registers
* :github:`29589` - Creating a k_thread and k_sem as runtime instantiated kernel object causes general protection fault
* :github:`29574` - question: about CONFIG_NET_BUF_POOL_USAGE
* :github:`29567` - Using openthread based echo_client and lwm2m_client cannot ping the external network address
* :github:`29549` - doc: Zephyr module feature ``depends`` not documented.
* :github:`29544` - Bluetooth: Mesh: Friend node unable relay message for lpn
* :github:`29541` - CONFIG_THREAD_LOCAL_STORAGE=y 构建 失败 带 ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb
* :github:`29538` - eswifi recvfrom() not properly implemented on disco_l475_iot1
* :github:`29534` - reel_board:running tests/kernel/workq/work_queue_api/ failed
* :github:`29533` - mec15xxevb_assy6853:running testcase tests/kernel/workq/work_queue_api/ failed.
* :github:`29532` - mec15xxevb_assy6853:running testcase tests/portability/cmsis_rtos_v2/ failed.
* :github:`29530` - display: nrf52840: adafruit_2_8_tft_touch_v2 shield not working with nrf-spim driver
* :github:`29519` - 内核 提供 对齐 variants 用于 allocators
* :github:`29518` - sleep 在...中 qemu 到 短
* :github:`29499` - x86 线程 栈 guards persist 在...之后 线程 退出
* :github:`29497` - 警告 在...中 CR2
* :github:`29491` - usb: web USB sample fails Chapter9 USB3CV tests.
* :github:`29478` - fs: fs_open can corrupt fs_open_t object given via zfp parameter
* :github:`29468` - usb: ZEPHYR FATAL ERROR when running USB test for Nordic.
* :github:`29467` - nrf_qspi_nor.c 不正确 值 使用 用于 检查 启动 的 RAM 地址 space
* :github:`29446` - pwm: stm32: output signal delayed
* :github:`29444` - Network deadlock
* :github:`29442` - 构建 失败 w/sanitycheck 用于 samples/bluetooth/hci_usb_h4/sample.bluetooth.hci_usb_h4
* :github:`29440` - Missing hw-flow-control; in hci_uart overlay files
* :github:`29435` - SDCard via SD/SDIO/MMC interfaces
* :github:`29430` - up_squared_adsp: Sanitycheck  不 运行 测试 case 在...上 Up_Squared_ADSP 板
* :github:`29429` - net: dns: enable dns service discovery for mdns service
* :github:`29418` - ieee802154: cc13xx_cc26xx: bug in rf driver library
* :github:`29412` - sanitycheck: skipped tests marked as failed due to the reason SKIPPED (SRAM overflow)
* :github:`29398` - ICMPv6 错误 发送 带 不正确 链接 layer 地址
* :github:`29386` - unexpected behavior when doing syscall with 7 or more arguments
* :github:`29382` - 移除 内存 domain restriction 在...上 系统 RAM 用于 内存 划分 在...上 MMU 设备
* :github:`29376` - sanitycheck: "TypeError: 'NoneType' object is not iterable"
* :github:`29373` - Some altera DTS bindings have the wrong vendor prefix
* :github:`29368` - STM32: non F1 -pinctrl.dtsi generation files: Limit mode to variants
* :github:`29367` - usb: drivers: add USB support for UP squared
* :github:`29364` - cdc_acm_composite fails USB3CV test for Nordic platform.
* :github:`29363` - shell: inability to print 64-bit integers with newlib support
* :github:`29357` - RFC: API Change: Bluetooth: Update indication callback parameters
* :github:`29347` - Network deadlock because of mutex locking order
* :github:`29346` - west boards doesn't display the arcitecture.
* :github:`29330` - mec15xxevb_assy6853:running samples/boards/mec15xxevb_assy6853/power_management Sleep entry latency is higher than expected
* :github:`29329` - 测试 kernel.workqueue.api 测试 失败 在...上 multiple 平台
* :github:`29328` - mec15xxevb_assy6853:running tests/kernel/workq/work_queue_api/ failed
* :github:`29327` - mec15xxevb_assy6853:region ``SRAM`` overflowed during build
* :github:`29319` - up_squared:  tests/kernel/timer/timer_api failed.
* :github:`29317` - mimxrt1015: kernel_threads_sched: application meet size issue
* :github:`29315` - twr_kv58f220m: 所有 application 构建 失败
* :github:`29312` - [RFC] [BOSSA] Improve offset parameter
* :github:`29310` - ble central Repeat read and write to three peripherals error USAGE FAULT
* :github:`29309` - ADC1 doesn't read correctly on STM32F7
* :github:`29308` - GPIO bit banging i2c init before gpio clock init in stm32f401 plantform,cause same gpio can't work.
* :github:`29307` - samples/bluetooth/mesh-demo unable to send vendor button message
* :github:`29300` - K_THREAD_DEFINE() uses const in a wrong way
* :github:`29298` - xlnx_psttc_timer driver has an imprecise z_clock_set_timeout() implementation
* :github:`29287` - spi: SPI_LOCK_ON does not hold the lock for multiple spi_transceive until spi_release
* :github:`29284` - compilation issues for MinnowBoard/ UpSquared on documentation examples
* :github:`29283` - quickfeather 不 listed 在...中 板
* :github:`29274` - Can't get Coded PHY type(S2 or S8)
* :github:`29272` - nordic qspi: readoc / writeoc selection may not work
* :github:`29263` - tests/kernel/mem_protect/obj_validation 失败 构建 在...上 一些 板 在...之后 最近 更改
* :github:`29261` - 板 musca_b1: post 构建 actions 带 TF-M  不  done 在...中 正确 排序
* :github:`29259` - sanitycheck: sanitycheck defines test expected to fail as FAILED
* :github:`29258` - net: Unable to establish TCP connections from Windows hosts
* :github:`29257` - Race condition in k_queue_append and k_queue_alloc_append
* :github:`29248` - 板 nrf52840_mdk: 支持 用于 qspi 刷写 缺失
* :github:`29244` - k_thread_resume can cause k_sem_take with K_FOREVER to return -EAGAIN and crash
* :github:`29239` - i2c: mcux driver does not prevent simultaneous transactions
* :github:`29235` - Endless build loop after adding pinctrl dtsi
* :github:`29223` - BLE one central connect multiple peripherals
* :github:`29220` - ARC: tickless idle exit code destroy exception status
* :github:`29202` - core kernel depends on minimal libc ``z_prf()``
* :github:`29195` - west fails with custom manifest
* :github:`29194` - Sanitycheck block after passing some test
* :github:`29183` - DHCPv4 retransmission interval gets too large
* :github:`29175` - x86 失败 所有 测试 如果 CONFIG_X86_KPTI  禁用
* :github:`29173` - uart_nrfx_uart fails uart_async_api_test
* :github:`29166` - sanitycheck ``--test-only --device-testing --hardware-map`` shouldn't run tests on all boards from ``--build-only``
* :github:`29165` - shell_print doesn't support anymore %llx when used with newlib
* :github:`29164` - net: accept() doesn't return an immediately usable descriptor
* :github:`29162` - Data Access Violation when LOG_* is called on ISR context
* :github:`29155` - CAN BUS support on Atmel V71
* :github:`29150` - CONFIG_BT_SETTINGS_CCC_LAZY_LOADING never loads CCC
* :github:`29148` - MPU: twr_ke18f: many kernel application fails when allocate dynamic MPU region
* :github:`29146` - canisotp: mimxrt1064_evk: no DT_CHOSEN_ZEPHYR_CAN_PRIMARY_LABEL defined cause tests failure
* :github:`29145` - net: frdmk64f many net related applications meet hardfault, hal driver assert
* :github:`29139` - tests/kernel/fatal/exception 失败 在...上 nsim_sem_mpu_stack_guard 板
* :github:`29120` - STM32: Few issues on pinctrl generation script
* :github:`29113` - 构建 失败 带 OSPD
* :github:`29111` - Atmel SAM V71 UART_0 fail
* :github:`29109` - HAL STM32 Missing ETH pin control configurations in DT files
* :github:`29101` - Bluetooth: assertion fail with basic repeated extended advertisement API
* :github:`29099` - net: dns: dns-sd: support for dns service discovery
* :github:`29098` - ATT timeout worker not canceled by destroy, and may operate on disposed object
* :github:`29095` - zefi.py has incorrect assertions
* :github:`29092` - tests/drivers/uart/uart_async_api 失败 在...上 nrf52840dk_nrf52840 和 额外 平台
* :github:`29089` - doc: boards: cc1352r_sensortag: fix minor rst issue
* :github:`29083` - Bluetooth: Host: Inconsistent permission value during discovery procedure
* :github:`29078` - nRF52840 doesn't start legacy advertisment after extended advertisment
* :github:`29074` - #27901 breaks mikroe_* shields overlay
* :github:`29070` - NXP LPC GPIO driver masked set does not use the mask
* :github:`29068` - 选择 zephyr,code-partition  不 effect 在...上 ELF 链接 启动 地址
* :github:`29066` - kernel: k_sleep doesn't handle relative or absolute timeouts >INT_MAX
* :github:`29062` - samples/bluetooth/peripheral_hr/sample.bluetooth.peripheral_hr_rv32m1_vega_ri5cy 失败 到 构建 在...上 rv32m1_vega_ri5cy
* :github:`29059` - HAL: mchp: Missing PCR ids to control PM for certain HW blocks
* :github:`29056` - tests/bluetooth/init/bluetooth.init.test_ctlr_dbg 失败 到 构建 在...上 nrf51dk_nrf51422
* :github:`29050` - Ugrade lvgl library
* :github:`29048` - 移除 pwr-gpio 的 rt1052 从 devicetree  cause 构建 错误
* :github:`29047` - 板 nucleo_stm32g474re  不 构建
* :github:`29043` - dirvers: eth_stm32_hal: 不 中断  生成 在...上  MII 接口
* :github:`29042` - CONFIG_SHELL_HELP=n 失败 到 编译
* :github:`29034` - 错误 在...中 samples/subsys/usb/cdc_acm
* :github:`29025` - [Coverity CID :214882] Argument cannot be negative in tests/posix/eventfd/src/main.c
* :github:`29024` - [Coverity CID :214878] Argument cannot be negative in tests/posix/eventfd/src/main.c
* :github:`29023` - [Coverity CID :214877] Argument cannot be negative in tests/posix/eventfd/src/main.c
* :github:`29022` - [Coverity CID :214876] Argument cannot be negative in tests/posix/eventfd/src/main.c
* :github:`29021` - [Coverity CID :214874] Argument cannot be negative in tests/posix/eventfd/src/main.c
* :github:`29020` - [Coverity CID :214873] Argument cannot be negative in tests/posix/eventfd/src/main.c
* :github:`29019` - [Coverity CID :214871] Side effect in assertion in tests/kernel/sched/preempt/src/main.c
* :github:`29018` - [Coverity CID :214881] Unchecked return value in subsys/mgmt/ec_host_cmd/ec_host_cmd_handler.c
* :github:`29017` - [Coverity CID :214879] Explicit null dereferenced in subsys/emul/spi/emul_bmi160.c
* :github:`29016` - [Coverity CID :214875] Dereference after null check in subsys/emul/spi/emul_bmi160.c
* :github:`29015` - [Coverity CID :214880] Out-of-bounds access in subsys/net/ip/tcp2.c
* :github:`29014` - [Coverity CID :214872] Bad bit shift operation in drivers/ethernet/eth_w5500.c
* :github:`29008` - BLE Connection fails to establish between two nRF52840-USB Dongles with Zephyr controller
* :github:`29007` - OOT manifest+module discovery/builds fail
* :github:`29003` - memory corruption in pkt_alloc
* :github:`28999` - STM32: Transition to device tree based pinctrl configuration
* :github:`28990` - Docs: Dead links to sample source directories
* :github:`28979` - Automatic reviewer assignment for PR does not seem to work anymore
* :github:`28976` - sanitycheck 失败 所有 测试 用于 nsim_em7d_v22
* :github:`28970` - clarify thread life-cycle documentation
* :github:`28956` - API-less devices aren't findable
* :github:`28955` - undesired 内核 调试 日志
* :github:`28953` - winc1500 driver blocks on listen
* :github:`28948` - hci_usb: ACL transfer not restarted after USB Suspend - Resume
* :github:`28942` - ARC: nsim_hs_smp: huge zephyr.hex file generated on build
* :github:`28941` - Civetweb: create separate directory
* :github:`28938` - EFR32BGx Bluetooth Support
* :github:`28935` - 支持 代码 coverage 在...中 unit 测试
* :github:`28934` - pinmux: stm32: port remaining pinctrl DT serial definitions for STM32 based boards
* :github:`28933` - mcuboot: Brick when using BOOT_SWAP_USING_MOVE and reset happens during images swap
* :github:`28925` - west failed due to empty value in self.path
* :github:`28921` - MCUboot / smp_svr sample broken in 2.4.0
* :github:`28916` - net_if_down doesn't clear address
* :github:`28912` - 不正确 宏  使用 到 init  sflist
* :github:`28908` -  相同 缓冲区  shared 由  2 Ethernet controllers 在...中  eth_mcux 驱动
* :github:`28898` - lwm2m_client can't start if mcuboot is enabled
* :github:`28897` - SPI does not work for STM32 min dev board
* :github:`28893` - Double-dot in path's may cause problems with gcc under Windows
* :github:`28887` - Bluetooth encryption request overrides ongoing phy update
* :github:`28881` - tests/kernel/mem_protect/sys_sem: qemu_x86_64 intermittent failure
* :github:`28876` - -p doesn't run a pristine build
* :github:`28872` - Support ESP32 as Bluetooth controller
* :github:`28870` - Peripheral initiated connection parameter update is ignored
* :github:`28867` - ARM Cortex-M4: Semaphores could not be used in ISRs with priority 0?
* :github:`28865` - Doc: Generate documentation using dts bindings
* :github:`28854` - ``CONFIG_STACK_POINTER_RANDOM`` may be undefined
* :github:`28847` - code_relocation sample does not work on windows
* :github:`28844` - Double quote prepended when exporting CMAKE compile option using zephyr_get_compile_options_for_lang()
* :github:`28833` - STM32: SPI DMA Driver - HW CS handling not compatible with spi_nor (Winbond W25Q)
* :github:`28826` - nRF QSPI flash driver broken for GD25Q16
* :github:`28822` - Improve STM32 LL HAL usage
* :github:`28809` - 启用 bt_gatt_notify() 到 overwrite notified 值 在...之前 发送 相当 than 队列 值
* :github:`28794` - RFC: API Change: k_work
* :github:`28791` - STM32: Clock recovery system (CRS) support
* :github:`28787` - lwm2m-client sample can't be build with openthread and DTLS
* :github:`28785` - shell 它   可能 到 get list 的 命令 没有 pressing tab
* :github:`28777` - 内存 pool 问题
* :github:`28775` - 更新 到 TFM v1.2 发布
* :github:`28774` - 构建 失败 几个 bluetooth samples 失败 到 构建 在...上 nrf51dk_nrf51422
* :github:`28773` - Lower Link Layer code use upper link layer function have " undefined reference to"
* :github:`28758` - ASSERTION FAIL [conn->in_retransmission == 1] with civetweb sample application
* :github:`28745` - 缺陷 在...中 drivers/modem/hl7800.c
* :github:`28739` - Bluetooth: Mesh: onoff_level_lighting_vnd sample fails provisioning
* :github:`28735` - NULL pointer access in zsock_getsockname_ctx with TCP2
* :github:`28723` - Does not respect python virtualenv
* :github:`28722` - Bluetooth: provide ``struct bt_conn`` to ccc_changed callback
* :github:`28714` - Bluetooth: PTS upper tester: GAP/CONN/NCON/BV-02-C Fails because of usage of NRPA
* :github:`28709` - phandle-array doesn't allow array of just phandles
* :github:`28706` - west build -p auto -b nrf52840dk_nrf52840 error: HAS_SEGGER_RTT
* :github:`28701` - ASSERTION FAIL [!radio_is_ready()]
* :github:`28699` - Bluetooth: controller: Speed up disconnect process when slave latency is used
* :github:`28694` - k_wakeup follwed by k_thread_resume call causes system freeze
* :github:`28693` - FCB support for non-0xFF flash erase values
* :github:`28691` - tests: arch: arm: arm_thread_swap: fails with bus fault
* :github:`28688` - Bluetooth: provide ``struct bt_gatt_indicate_params`` to ``bt_gatt_indicate_func_t``
* :github:`28670` - drivers: flash: bluetooth: stm32wb: attempt to erase internal flash before enabling Bluetooth cause fatal error
* :github:`28664` - 决定 whether 到 启用 HW_STACK_PROTECTION 由 默认
* :github:`28650` - GCC-10.2 link issue w/g++ on aarch64
* :github:`28629` - 测试 内核 common: 和 common.misra  失败 在...上 nrf52840dk
* :github:`28620` - 6LowPAN ipsp: ping host -> µc failes, ping µc -> host works. after that: ping host -> µc works
* :github:`28613` - cannot set GDB watchpoints on QEMU x86 with icount enabled
* :github:`28590` - up_squared_adsp:running tests/kernel/smp/ failed
* :github:`28589` - up_squared_adsp:running tests/kernel/workq/work_queue/ failed
* :github:`28587` - Data corruption while serving large files via HTTP with TCP2
* :github:`28556` - mec15xxevb_assy6853:running tests/kernel/sched/schedule_api/ failed
* :github:`28547` - up_squared: tests/subsys/debug/coredump failed using twister command.
* :github:`28544` - Null pointer dereference in ll_adv_aux_ad_data_set
* :github:`28533` - soc: ti_simplelink: cc13xx-cc26xx: kconfig for subghz 802.15.4
* :github:`28509` - series-push-hook.sh: Don't parse then-master-to-latest-master commits after rebase to lastest
* :github:`28504` - dfu: dfu 库  失败 到 编译 在...上 redefined 函数 在...期间 构建 MCUBoot
* :github:`28502` - USB DFU class: support MCUBoot CONFIG_SINGLE_APPLICATION_SLOT
* :github:`28493` - Sanitycheck on ARC em_starterkit_em7d has many tests timeout
* :github:`28483` - Fix nanosleep(2) for sub-microsecond durations
* :github:`28473` - Mcuboot fails to compile when using single image and usb dfu
* :github:`28469` - Unable to capture adc signal at 8ksps when using nrf52840dk board.
* :github:`28462` - SHIELD 不 handled 正确 在...中 CMake 当...时 使用 custom 板
* :github:`28461` - ``HCI_CMD_TIMEOUT`` when setting ext adv data in the hci_usb project
* :github:`28456` - TOOLCHAIN_LD_FLAGS setting of -mabi/-march aren't propagated to linker invocation on RISC-V
* :github:`28442` - How handle IRQ_CONNECT const requirement?
* :github:`28406` - Condition variables
* :github:`28383` - bq274xx sample  不 工作
* :github:`28363` - ssd16xx: off-by-one with non-multiple-of-eight heights
* :github:`28355` - Document limitations of net_buf queuing functions
* :github:`28309` - Sample/subsys/fs/littlefs with board=nucleo_f429zi  don't work
* :github:`28299` - net: lwm2m: Improve token handling
* :github:`28298` - Deep sleep(system off) is not working with LVGL and display driver
* :github:`28296` - test_essential_thread_abort: lpcxpresso55s16_ns test failure
* :github:`28278` - PWM silently fails when changing output frequency on stm32
* :github:`28220` - flash: revise API to remove block restrictions on write operations
* :github:`28177` - gPTP gptp_priority_vector struct field ordering is wrong
* :github:`28176` - [Coverity CID :214217] Out-of-bounds access in tests/kernel/mem_protect/mem_map/src/main.c
* :github:`28175` - [Coverity CID :214214] Uninitialized pointer read in tests/benchmarks/data_structure_perf/rbtree_perf/src/rbtree_perf.c
* :github:`28170` - [Coverity CID :214222] Unrecoverable parse warning in include/ec_host_cmd.h
* :github:`28168` - [Coverity CID :214218] Unused value in subsys/mgmt/osdp/src/osdp.c
* :github:`28159` - [Coverity CID :214216] Logically dead code in drivers/pwm/pwm_stm32.c
* :github:`28155` - sam_e70_xplained:running samples/net/sockets/civetweb/ failed
* :github:`28124` - Linking external lib against POSIX API
* :github:`28117` - CoAP/LWM2M: Clean Packet Retransmission Concept
* :github:`28113` - Embed precise Zephyr version & platform name in sanitycheck output .xml
* :github:`28094` - samples: 驱动 spi_flash_at45: 不 工作 用于 板 没有 internal 刷写 驱动
* :github:`28092` - Make SPI speed of SDHC card configurable
* :github:`28014` - tests: kernel: mem_protect: sys_sem: failed when CONFIG_FPU is activated
* :github:`27999` - 增加 QSPI 测试 用于 microchip mec1521 板 驱动  在...中 zephyr/drivers/spi, 到  测试 在...上 mec15xxevb_assy6853
* :github:`27997` - 错误 在...中 copy paste lengthy 脚本 进入 shell 控制台
* :github:`27981` - Low UART utilization for hci_uart
* :github:`27957` - 刷写 签名 binaries: key 路径 和 版本
* :github:`27914` - frdm_k64f async uart api
* :github:`27892` - [v2.1.x] lib: updatehub: Improve download on slow networks and security fix
* :github:`27890` - [v2.2.x] lib: updatehub: Improve download on slow networks and security fix
* :github:`27881` - Zephyr requirements.txt fails to install on Python 3.9rc1
* :github:`27879` - Make i2c_slave callbacks public in the documentation
* :github:`27856` - Support per thread runtime statistics
* :github:`27846` - Weird ADC outliers on nrf52
* :github:`27841` - samples: disk: unable to access sd card
* :github:`27829` - sys_mutex and futex missing documentation
* :github:`27809` - Cannot enable MPU for nucleo_l552ze_q_ns
* :github:`27785` - memory domain arch implementation not correct with respect to SMP on ARC
* :github:`27716` - Bluetooth: Mesh: Devices relay their own messages (even with relay disabled!)
* :github:`27677` - RFC: Get rid of shell UART device selection in Kconfig
* :github:`27672` - [v2.2] BLE Transaction Collision
* :github:`27633` - arm64 SMP
* :github:`27628` - stm32: i2c bus failure when using USB
* :github:`27622` - Power management for modems using PPP
* :github:`27600` - JSON Api refuse to decode null value
* :github:`27596` - 日志记录 backend inconsistency 带 控制台 和 shell
* :github:`27583` - sanitycheck  不 失败 在...上 SRAM overflow, 增加 选项 到 创建 它 失败 在...上 那些 cases.
* :github:`27574` - mec15xxevb_assy6853:arch.arm.arch.arm.no.multithreading 失败 到 运行
* :github:`27573` - coverage: When enable coverage, some testcases need more time
* :github:`27570` - up_squared:logging.add.logging.add.async failed
* :github:`27561` - 驱动 gpio: pca9555 : 增加 GPIO 驱动 启用 中断 支持
* :github:`27559` - 如何 到 使用 stm32cubeIDE 到 构建 和 调试
* :github:`27525` - Including STM32Cube's USB PD support to Zephyr
* :github:`27510` - [v1.14] Bluetooth: controller: Fix uninit conn context after invalid channel map
* :github:`27506` - driver: peci: mchp: Ping command is failing due to improper tx wait timeout.
* :github:`27490` - arch/common/isr_tables.c compilation fails with CONFIG_NUM_IRQS=0
* :github:`27487` - storage/stream:  使用 仅 刷写 驱动 public API
* :github:`27468` - BT Host: Periodic Advertisement delayed receive
* :github:`27467` - BT Host: Periodic Advertiser List
* :github:`27466` - BT Host: Periodic Advertisement Sync Transfer (PAST)
* :github:`27457` - Add support for Nordic nrfx PDM driver for Nordic Thingy52
* :github:`27423` - RFC: API change: clock_control: Change parameters of clock_control_async_on
* :github:`27417` - CivetWeb Enable WebSocket
* :github:`27396` - samples/subsys/logging/logger timeout when sanitycheck enable coverage, it needs a filter
* :github:`27369` - spi: stm32: dma: rx transfer error when spi_write called
* :github:`27367` - Sprintf -  error while sending data to SD card
* :github:`27350` - ADC: adc shell failure when mismatch with dts device label
* :github:`27332` - [v2.3.x] lib: updatehub: Improve download on slow networks and security fix
* :github:`27299` - espi: xec: Whenever eSPI host indicates we are entering DnX mode, notification doesn't reach application
* :github:`27279` - CMSIS RTOS v1 Signals Implementation Issue
* :github:`27231` - Sending data to .csv file on SD card - ERROR CS control inhibited (no GPIO device)
* :github:`27195` - Sanitycheck: BinaryHandler can't kill children processes
* :github:`27176` - [v1.14] Restore socket descriptor permission management
* :github:`27174` - TCP Server don't get the right data from the client
* :github:`27146` - [Coverity CID :211510] Unchecked return value in lib/posix/semaphore.c
* :github:`27122` - 实现 watchdog 驱动 用于 mimxrt1050_evk
* :github:`27068` - ESP-IDF Bootloader bootloop
* :github:`27055` - BlueZ 带 ESP32 板 支持 或 不
* :github:`27047` - zefi.py assumes host GCC is x86
* :github:`27031` - Zephyr OpenThread Simulation
* :github:`27020` - civetweb issues
* :github:`27006` - unsynchronized newlib uintptr_t and PRIxPTR definition on xtensa
* :github:`26987` - [Coverity CID :211475] Unintended sign extension in drivers/sensor/wsen_itds/itds.c
* :github:`26975` - Control never returns from stm32_i2c_msg_write(), when SCL is pulled low permanently (hardware fault occurs)
* :github:`26961` - occasional sanitycheck failures in samples/subsys/settings
* :github:`26949` - sanitycheck gets overwhelmed by console output
* :github:`26912` - arm: cortex_r: config_userspace: hang during early power-up
* :github:`26873` - WIFI_ESP: sockets left opened after unexpected reset of ESP
* :github:`26829` - GSM modem example on stm32f103 bluepill
* :github:`26819` - drivers: modem: SARA modem driver leaks sockets
* :github:`26807` - Bluetooth HCI USB sample is not working
* :github:`26799` - Introduce p99
* :github:`26794` - arc: smp: different sanitycheck results of ARC hsdk's 2 cores and 4 cores configuration
* :github:`26732` - Advertise only on single bluetooth channel
* :github:`26722` - uarte_nrfx_poll_out() in NRF UARTE driver does not work with hardware flow control
* :github:`26665` - 实现 复位 用于 ARC development 板
* :github:`26656` - SAM0 USB transfer slot leak
* :github:`26637` - 如何 到 识别 sensor 设备
* :github:`26584` - Multicast emission  仅 可能 用于 ipv4 启动 带 224.
* :github:`26533` - 支持 newlib 用于 Aarch64 架构
* :github:`26522` - Reported "Supported shields" list includes boards
* :github:`26515` - timers: platforms using cortex_m_systick does not enter indefinite wait on SLOPPY_IDLE
* :github:`26500` - sanitycheck reports failing tests with test_slice_scheduling()
* :github:`26488` - Bluetooth: Connection failure using frdm_kw41z shield
* :github:`26486` - possible SMP race with k_thread_join()
* :github:`26477` - GPIO sim driver
* :github:`26443` - sanitycheck shall generate results and detailed information about tests and environment in json format.
* :github:`26409` - Clearing of previously initialized data during IPv6 interface init causes infinite loop, memory corruption in timer ISR
* :github:`26383` - OpenThread NCP radio-only
* :github:`26372` - qspi 驱动  不 工作 如果 multithreading  禁用
* :github:`26330` - tcp: low bulk receive performance due to window handling
* :github:`26315` - ieee802154: cc13xx_cc26xx: sub_ghz support
* :github:`26312` - drivers: ieee802154: cc13xx_cc26xx: adopt hal/ti rf driverlib
* :github:`26275` - USB MSC 失败 命令 设置 测试 从 USB3CV.
* :github:`26272` - Cannot use alternative simulation runner with sanitycheck
* :github:`26227` - icount support for qemu_arc_{em,hs}
* :github:`26225` - x86_64 doesn't seem to be handling spurious interrupts properly
* :github:`26219` - sys/util: add support for mapping lists with per-element terminal symbols
* :github:`26172` - Zephyr Master/Slave not conforming with Core Spec. 5.2 connection policies
* :github:`26163` - qemu_arc_{em,hs} keeps failing in CI on tests/kernel/lifo/lifo_usage
* :github:`26142` - cmake warning: "Policy CMP0077 is not set"
* :github:`26084` - 2.4 Release Checklist
* :github:`26072` - refactor struct device to reduce RAM demands
* :github:`26051` - shell: uart: Allow a change in the shell initalisation to let routing it through USB UART
* :github:`26050` - devicetree: provide access to node ordinal
* :github:`26026` - RFC: drivers: pwm: add functions for capturing pwm pulse width and period
* :github:`25956` - Including 头文件 文件 从 模块 进入 app
* :github:`25927` - ARM: Core Stack Improvements/Bug fixes for 2.4 release
* :github:`25918` - qemu_nios2 崩溃 当...时 启用 icount
* :github:`25832` - [test][kernel][lpcxpresso55s69_ns] kernel cases meet ESF could not be retrieved successfully
* :github:`25604` - USB: enable/disable a class driver at runtime
* :github:`25600` - wifi_eswifi: Unable to start TCP/UDP client
* :github:`25592` - Remove checks on board undocumented DT strings
* :github:`25597` - west 签名 失败 到 查找 头文件 大小 或 padding
* :github:`25508` - tests: add additonal power management tests
* :github:`25507` - up_squared:tests/portability/cmsis_rtos_v2 failed.
* :github:`25482` - outdated recommendations for SYS_CLOCK_TICKS_PER_SEC
* :github:`25466` - 日志 构建 错误  不 helpful
* :github:`25434` - nRF5340 Bluetooth peripheral_hr sample high power consumption
* :github:`25413` - soc: ti_simplelink: kconfig: ble: placeholder for hal_ti
* :github:`25409` - Inconsistent naming of Kconfig options related to stack sizes of various Zephyr components
* :github:`25395` - Websocket Server API
* :github:`25379` - Bluetooth mesh example not working
* :github:`25314` - Bluetooth: controller: legacy: Backport conformance test related changes
* :github:`25302` - lwm2m client sample bootstrap server support
* :github:`25182` - Raspberry Pi 4B Support
* :github:`25173` - k_sem_give(struct k_sem \*sem) should report failure when the semaphore is full
* :github:`25164` - Remove ``default:`` functionality from devicetree bindings
* :github:`25015` - Bluetooth Isochronous Channels Support
* :github:`25010` - disco_l475_iot1 don't confirm MCUBoot slot-1 image
* :github:`24803` - ADC 驱动 测试 挂起 在...上 atsame54_xpro
* :github:`24652` - sanitycheck doesn't keep my cores busy
* :github:`24453` - docs: 允许 到 使用  exact 当前 zephyr 版本 数量 在...中 place 的 最新 在...中 documentation URLs
* :github:`24358` - deprecate and remove old k_mem_pool / sys_mem_pool APIs
* :github:`24338` - UICR & FICR missing from nRF52* devicetree files
* :github:`24211` - [v2.2.x] lib: updatehub: Not working on Zephyr 2.x
* :github:`23917` - Kconfig: 问题 带 使用 backslash-escapes 在...中 默认 值 的 "string" 选项
* :github:`23874` - 测试 case 到 检查 registers 数据
* :github:`23866` - sample hci_usb fails with zephyr 2.2.0 (worked with zephyr 2.1.0)
* :github:`23729` - hifive1_revb 失败 到 工作 带 samples/subsys/console/getline
* :github:`23314` - Bluetooth: controller: Use defines for 625 us and 1250 us
* :github:`23302` - Poor TCP performance
* :github:`23212` - ARC: SMP: Enable use of ARConnect Inter-core Debug Unit
* :github:`23210` - mimxrt1050_evk:tests/net/iface failed with v1.14 branch.
* :github:`23063` - CMSIS v2 osThreadJoin  不 工作 如果 线程 退出 带 osThreadExit
* :github:`23062` - thread_num / thread_num_dynamic are never decremented in CMSIS v2 thread.c
* :github:`22942` - Missing TX power options for nRF52833
* :github:`22771` - z_x86_check_stack_bounds() doesn't work right for nested IRQs on x86-64
* :github:`22703` - 实现 ADC 驱动 用于 lpcxpresso55s69
* :github:`22411` - AArch64 / Cortex-A port improvements / TODO
* :github:`22333` - 驱动  检查 bus-timing 值 在 compile-time
* :github:`22247` - Discussion: Supporting the Arduino ecosystem
* :github:`22198` - BMA280 Sample Code
* :github:`22185` - 增加 线程 Local 存储 (TLS) 支持
* :github:`22060` - 构建 失败 带 gcc-arm-none-eabi-9-2019-q4-major
* :github:`21991` - 内存 domain locking  不  entirely 正确
* :github:`21495` - x86_64: interrupt stack overflows are not caught
* :github:`21462` - x86_64 exceptions are not safely preemptible, and stack overflows are not caught
* :github:`21273` - devicetree: 改进 支持 用于 enum 值
* :github:`21238` - Improve Zephyr HCI VS extension detection
* :github:`21216` - Ztest "1cpu" cases don't retarget interrupts on x86_64
* :github:`21179` - Reduce RAM consumption for civetweb HTTP sample
* :github:`20980` - ESP32 刷写 错误 带 segment 计数 错误 使用 esptool.py 从 esp-idf
* :github:`20925` - tests/kernel/fp_sharing/float_disable crashes on qemu_x86 with CONFIG_KPTI=n
* :github:`20821` - Do USE\_\(DT\_\)CODE\_PARTITION and FLASH_LOAD_OFFSET/SIZE need to be user-configurable?
* :github:`20792` - sys_pm: fragility in residency policy
* :github:`20775` - sys_pm_ctrl: fragility in managing state control
* :github:`20686` - tests/kernel/fp_sharing/float_disable 失败 当...时 代码 coverage  启用 在...上 qemu_x86.
* :github:`20518` - [Coverity CID :205647]Memory - illegal accesses in /tests/arch/x86/info/src/memmap.c
* :github:`20337` - sifive_gpio: gpio_basic_api test fails
* :github:`20262` - dt-binding 用于 定时器
* :github:`20118` - Zephyr BLE stack to work on the CC2650 Launchpad
* :github:`19850` - Bluetooth: Mesh: Modular settings handling
* :github:`19530` - 增强 sanitycheck/CI 用于 分离 构建 phase 从 测试
* :github:`19523` - Can't build fade-led example for any Nordic board
* :github:`19511` - net: TCP: echo server blocks after a packet with zero TCP options
* :github:`19497` - log subsystem APIs need to be clearly namespaced as public or private
* :github:`19467` - 错误 构建 samples 带 PWM
* :github:`19448` - devicetree: 支持 禁用 设备
* :github:`19435` - how to change uart tx rx pins in zephyr
* :github:`19380` - Potential bugs re. 'static inline' and static variables
* :github:`19244` - BLE throughput of DFU by Mcumgr is too slow
* :github:`19138` - zassert prints to UART even when RTT is selected
* :github:`19100` - LwM2M sample with DTLS: does not connect
* :github:`19003` - bluetooth : Mesh: adv thread can be replace by other methods.
* :github:`18927` - settings: deprecate base64 encoding
* :github:`18778` - soc: arm: nordic_nrf: Defining DT\_..._DEV_NAME
* :github:`18728` - sam_e70_xplained:tests/subsys/logging/log_core failed.
* :github:`18608` - PCA9685 PWM 驱动  损坏
* :github:`18607` - DesignWare PWM 驱动  损坏
* :github:`18601` - LwM2M client sample: an overlay for OpenThread support
* :github:`18551` - address-of-temporary idiom not allowed in C++
* :github:`18529` - fs/fcb: consider backport of mynewt fixes
* :github:`18276` - irq_connect_dynamic()  不 测试 在...上 所有 arches
* :github:`17893` - dynamic 线程 don't 工作 在...上 x86 在...中 一些 配置
* :github:`17787` - openocd unable to flash hello_world to cc26x2r1_launchxl
* :github:`17743` - cross 编译 用于 RISCV32 失败 as compiler flags  不 supplied 由 板 但   在...中 target.cmake
* :github:`17645` - VSCode debugging Zephyr application
* :github:`17545` - Licensing and reference to public domain material
* :github:`17300` - [Zephyr v1.14.0] mcumgr: stm32: Strange Build warnings when counter is enabled
* :github:`17023` - userspace: thread indexes are not released when dynamic threads lose all references
* :github:`17014` - reentrancy protection in counter drivers?
* :github:`16766` - net: net_pkt_copy don't work as expected when data was pulled from destination
* :github:`16544` - drivers: spi: spi_mcux_lpspi: inconsistent chip select behaviour
* :github:`16438` - fs/FCB fs/NVS : requires unaligned flash read-out length capabilities,
* :github:`16237` - disco_l475_iot1: samples/bluetooth/ipsp ko since 3151d26
* :github:`16195` - k_uptime_delta(): Defective by design
* :github:`15944` - stm32: 新 驱动 用于 FMC/FSMC
* :github:`15713` - MCUMGR_LOG 构建 错误
* :github:`15570` - Unbonded peripheral gets 'Tx Buffer Overflow' when erasing bond on master
* :github:`15372` - logging can't dump exceptions without losing data with CONFIG_LOG_PRINTK
* :github:`14591` - Infineon Tricore architecture support
* :github:`14571` - TCP: sending lots of data deadlocks with slow peer
* :github:`14300` - Bluetooth connection using central and peripheral samples in nrf52840
* :github:`13955` - stm32: Implement async uart api
* :github:`13591` - tests/blutooth/tester: ASSERTION FAIL due to Recursive spinlock when running bt tester on qemu-cortex-m3
* :github:`13396` - Cannot connect to Galaxy S8 via BLE
* :github:`13244` - 如何 到 加密 advertise 包 带 zephyr 和 nrf52832 ？
* :github:`12368` - File descriptors: Compile fails with non-POSIX out-of-tree libc
* :github:`12353` - intel_s1000: SPI 刷写 Erase 命令 doesn't 工作 当...时 引导 从 刷写
* :github:`12239` - BLE400 / nRF51822 (nRF51) PWM clock too low (servo-motor example)
* :github:`12150` - Power management on nRF52 boards
* :github:`11912` - net: SimpleLink: Create real cross-platform port
* :github:`11770` - Multiprotocol feature for BLE/Thread
* :github:`10904` - Requirements 用于 驱动 设备 generation 使用 设备 tree
* :github:`10857` - 迁移 从 CMSIS-Core 到 DeviceTree results 在...中 loss 的 类型 信息
* :github:`10460` - Bluetooth: settings: No space to store CCC config after successful pairing
* :github:`10158` -  支持 用于 probot 带 Zephyr
* :github:`10022` - Porting Modbus Library: Need some guidance
* :github:`9944` - 套接字 Connect doesn't 发送 新 SYN 在...中 case  第一 连接 attempt 失败
* :github:`9883` - DTS processing generates unit_address_vs_reg warning on entries with 'reg'
* :github:`9875` - Bluetooth: Host LE Extended Advertising
* :github:`9783` - LwM2M: Cannot create object instance without specifying instance number
* :github:`9509` - Unable to upload firmware over serial with mcumgr
* :github:`9406` - Generate DTS 'compatible' based compilation flags
* :github:`9403` -  支持 C++ standard 库
* :github:`9087` - 驱动 CAN 接口   compatible 带 CAN-FD 接口
* :github:`8499` - Device Tree support overhaul
* :github:`8393` - ``CONFIG_MULTITHREADING=n`` builds call ``main()`` with interrupts locked
* :github:`8008` - net: Sockets (and likely net_context's) should not be closed behind application's back
* :github:`7939` - Connections to TI CC254x break after conn_update
* :github:`7404` - arch: arm: MSP initialization during early boot
* :github:`7331` - Precise time sync through BLE mesh.
* :github:`6857` - need to improve filtering and coverage in sanitycheck
* :github:`6818` - Question: Is  Lightweight OpenMP implementation supported in Zephyr? Or any plan?
* :github:`6648` - Trusted Execution Framework: practical use-cases (high-level overview)
* :github:`6199` - STM32: document dts porting rules
* :github:`6040` - 实现 刷写 驱动 用于 LPC54114
* :github:`5626` - 构建 samples 失败
* :github:`4420` - net: tcp: RST handling is weak
* :github:`3675` - LE Adv. Ext.: Extended Scan with PHY selection for non-conn non-scan un-directed without aux packets
* :github:`3674` - LE Adv. Ext.: Non-Connectable and Non-Scannable Undirected without auxiliary packet
* :github:`3893` - Enhance k_stack_push() to check k_stack->top to avoid corruption
* :github:`3719` - Multiple 控制台 支持
* :github:`3441` - IP stack: No TCP send window handling
* :github:`3102` - Make newlib libc the default c library
* :github:`2247` - LE Controller: 更改 hal/ 进入  设置 的 驱动
