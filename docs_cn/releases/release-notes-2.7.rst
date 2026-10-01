:orphan:

.. _zephyr_2.7:

Zephyr 2.7.0
############

我们很高兴地宣布 Zephyr RTOS 版本 2.7.0（LTS2）的发布。

自 v2.6.0 以来的主要增强功能包括：

* 蓝牙音频、方向查找和 Mesh 改进
* 支持蓝牙广播 PDU 链接
* 新增对 armclang / armlinker 工具链的支持
* 新增对 MWDT C / C++ 工具链的支持
* 更新到 CMSIS v5.8.0（Core v5.5.0、DSP v1.9.0）
* 支持 ARMv8.1-M 上的 M-Profile 向量扩展（MVE）
* 改进了 Newlib 和 C++ 在支持 SMP 的系统上的线程安全性
* IEEE 802.15.4 软件地址过滤
* 新的基于操作的电源管理 API
* USB 设备框架现在包含第 9 章的所有定义和结构体
* 通用系统控制器（``syscon``）驱动和仿真器
* RISC-V 中紧耦合存储器的链接器支持
* LoRa 的额外阻塞 API 调用
* 支持扩展 PCI / PCIe 能力，改进 MIS-X 支持
* 新增对 mDNS / DNS 服务发现中的服务类型枚举（STE）的支持
* 为 West 中的 OpenOCD 新增 Zephyr 线程感知
* EEPROM 现在可以在闪存中仿真
* 新增以太网 MDIO 和以太网通用 PHY 驱动

自 v1.14.0（LTS1）以来的额外主要增强功能包括：

* 内核现在同时支持 32 位和 64 位架构
* 我们新增了对 SOCKS5 代理的支持
* 引入了对 6LoCAN 的支持，这是用于控制区域网络的 6Lo 适配层
* 我们新增了对点对点协议（PPP）的支持
* 我们新增了对 UpdateHub 的支持，这是一个用于设备空中更新的端到端解决方案
* 我们新增了对 ARM Cortex-R 架构的支持
* 在所有架构上规范化了 API
* 扩展了对 ARMv6-M 架构的支持
* 新增对众多新板级和扩展板的支持
* 新增众多新驱动和传感器
* 在 Vega 平台上新增 BLE 支持
* 蓝牙主机协议栈的内存大小改进
* 我们新增了对 64 位 ARMv8-A 架构的初步支持
* 通过第三方 CANopenNode 协议栈支持 CANopen 协议
* 新增 LoRa 支持以及 SX1276 LoRa 调制解调器驱动
* 引入了新的 Zephyr CMake 包
* 新的设备树 API，提供对几乎所有 DT 节点和属性的访问
* 内核超时 API 已全面重构
* 新的 k_heap/sys_heap 分配器，性能得到改进
* Zephyr 现在与 TF-M（Trusted Firmware M）PSA 合规框架集成
* 蓝牙低功耗主机现在支持 LE 广播扩展
* CMSIS-DSP 库现在已包含并集成
* 引入了对虚拟内存管理的初步支持
* 新增蓝牙主机对周期性广播和等时通道的支持
* 新增一个新的 TCP 协议栈，改进网络协议可测试性
* 引入了新的工具链抽象，初步支持 GCC 和 LLVM/Clang
* 改用 C99 整数类型，弃用 Zephyr 整数类型
* 引入了对 SPARC 架构和 LEON 实现的支持
* 新增线程本地存储（TLS）支持
* 新增对每线程运行时统计的支持
* 新增在 X86 上使用 LLVM 构建的支持
* 新增使用条件变量的新同步机制
* 新增对按需分页的支持，X86 上初步支持
* 日志子系统全面重构
* 新增对 64 位 ARCv3 的支持
* 拆分 ARM32 和 ARM64，ARM64 现在是顶层架构
* 新增对 Arm v8.1-m 和 Cortex-M55 的初步支持
* 移除在 2.4 中已弃用的遗留 TCP 协议栈支持
* 跟踪子系统全面重构 / 新增对 Percepio Tracealyzer 的支持
* 设备运行时电源管理（PM）完全重构
* West 中新增自动 SPDX SBOM 生成
* 新增一个独立的 Zephyr 应用示例

以下各节按组件提供详细的变更列表。

安全漏洞相关
******************************

本次发布解决了以下 CVE：

更详细的信息可参见：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2022-24193：截至 2022-09-01 处于保密期
* CVE-2022-24194：截至 2022-09-01 处于保密期
* CVE-2022-24195：截至 2022-09-01 处于保密期

已知问题
************

您可以使用 GitHub 接口列出所有带有 `bug 标签
<https://github.com/zephyrproject-rtos/zephyr/issues?q=is%3Aissue+is%3Aopen+label%3Abug>`_
的 issue，从而检查所有当前已知的问题。

API 变更
***********

* 新增对基于操作的电源管理 API 的支持。

* 新增对 IEEE 802.15.4 软件地址过滤的支持。

* 新增对 LoRa 的额外阻塞 API 调用的支持。

* 新增对扩展 PCI / PCIe 能力的支持。

* 新增对 mDNS / DNS 服务发现中的服务类型枚举（STE）的支持。

* 新增对以太网 MDIO 和以太网通用 PHY 驱动的支持。

本次发布中弃用

* 弃用 xoroshiro128+ PRNG，建议改用 xoshiro128++。

* 弃用 Doxygen 别名 ``@config{}``，建议改用 ``@kconfig{}``。

本次发布中移除的 API

* 移除 Kconfig 选项 ``CONFIG_USB``，引入 Kconfig 选项
  ``CONFIG_USB_DEVICE_DRIVER`` 以启用 USB 设备控制器驱动，
  当选项 ``CONFIG_USB_DEVICE_STACK`` 启用时选中。

============================

本次发布中的稳定 API 变更
==================================

内核
******

* 新增对基于操作的电源管理 API 的支持。

* 新增对 IEEE 802.15.4 软件地址过滤的支持。

* 新增对 LoRa 的额外阻塞 API 调用的支持。

* 新增对扩展 PCI / PCIe 能力的支持。

* 新增对 mDNS / DNS 服务发现中的服务类型枚举（STE）的支持。

* 新增对以太网 MDIO 和以太网通用 PHY 驱动的支持。

架构
*************

* ARC

  * 新增对 ARCv3 64 位 ISA 支持和相应的 HS6x 处理器支持
  * 加固 SMP 支持
  * ARC MWDT 工具链基础设施的各种小修复/改进
  * ARC Kconfig 重构

* ARM

  * AARCH32

    * 在 Cortex-M 中新增空指针解引用检测支持。
    * 新增 Arm v8.1-m 和 Cortex-M55 的初步支持。
    * 新增在 Cortex-M 中线程执行安全调用时对其进行抢占的支持。
    * 新增基于设备树节点信息由链接器生成内存区域的支持（Cortex-M）。
    * 清理了通用 Cortex-M 链接脚本中 SoC 专用内存区域的定义。
    * 新增在 Zephyr 早期启动阶段清除 NXP MPU 区域配置的支持。
    * 在 Cortex-M33 上使用 TF-M 构建非安全应用时，禁止使用 fpu hard ABI。
    * 增强了 Cortex-R 中故障异常的寄存器信息转储。
    * 修复了 Cortex-R 中的虚假中断处理。

  * AARCH64

    * SMP 支持
    * 带页表共享的 MMU 动态映射。
    * 用户空间（非特权）线程支持。
    * 独立的 SMCCC 支持。
    * XIP 支持。
    * ARM64 现在是独立的顶层架构。
    * Cortex-R82 和 Armv8-R AArch64 MPU 支持。
    * 缓存管理支持。
    * 重新设计的引导代码。
    * 完整的 FPU 上下文切换。

* x86

  * 新增 Lakemont SoC 的 SoC 配置。
  * 移除 kconfig ``CONFIG_CPU_MINUTEIA``，因为没有使用该选项的用户。
  * 将 kconfig ``CONFIG_SSE*`` 重命名为 ``CONFIG_X86_SSE*``。
  * 扩展了页表生成脚本，允许在构建期间指定额外的内存映射。
  * x86-32

    * 新增内核映像驻留在虚拟地址空间中的支持，允许通过虚拟地址进行代码执行
      和数据操作。

蓝牙
*********

* 音频

  * 将 ISO 处理与音频处理分离，并将后者移至其自身的目录。
  * 新增音量偏移控制服务和客户端。
  * 新增音频输入控制服务和客户端。
  * 新增音量控制服务和客户端。

* 主机

  * 新增方向查找的基本支持。
  * 新增通过周期性广播进行 CTE 无连接传输和接收的支持。
  * 重构了 HCI 和 ECC 处理实现。
  * 停止在广播数据中自动更新设备名称。
  * 新增记录安全密钥（供空中嗅探器使用）的支持。
  * 修复了一个绑定问题：当对端未使用绑定信息中存储的 IRK 时，
    远程设备移除本地绑定数据后，本地绑定数据未被更新。
  * 在 OTS 中实现了目录列表对象。
  * 新增访问 ``bt_conn_iso`` 对象的函数。
  * 新增可写设备名称的配置选项。
  * 新增最小加密密钥大小的配置选项。
  * 新增作为 SMP 响应方发送按键通知的支持。
  * 新增选项 ``BT_LE_ADV_OPT_FORCE_NAME_IN_AD``，强制设备名称
    出现在广播数据包中，而不是扫描响应中。
  * 在发送通知或指示时新增安全级别检查。
  * 新增通过 RTT 发送 HCI 监控跟踪的能力。
  * 为简化而重构了蓝牙缓冲区配置。更多信息参见
    6483e12a8ac4f495b28279a6b84014f633b0d374 的提交信息。
    但请注意，上述提交信息中有两个拼写错误；

    * ``BT_CTLR_TX_BUFFER`` 应为 ``BT_CTLR_TX_BUFFERS``
    * ``BT_CTLR_TX_BUFFERS_SIZE`` 应为 ``BT_CTLR_TX_BUFFER_SIZE``
  * 新增多身份并发广播的支持。
  * 更改了在设置随机地址前禁用扫描的逻辑。
  * 修复了一个崩溃：ATT 超时发生在已断开的 ATT 通道上。
  * 更改了配对流程：当双方具有相同的公钥时，配对失败。
  * 修复了一个问题：GATT 请求可能使 RX 线程死锁。
  * 修复了一个问题：之前设置的固定密码无法清除。
  * 修复了一个问题："security changed" 和 "pairing failed" 的回调
    并不总是被调用。
  * 更改了配对流程：如果远程设备无法达到所需的安全级别，则尽早失败。
  * 修复了一个问题：GATT 通知和 Write Without Response 可能乱序发送。
  * 更改了 ``bt_l2cap_chan_send`` 的缓冲区所有权。
    应用程序现在必须释放所有返回错误的缓冲区。

* Mesh

  * 新增 CDB 句柄密钥刷新阶段。
  * 新增对 SeqAuth 执行重放检查的能力。
  * 新增在关闭链路时发送 Link Close 消息。
  * 新增用于启用和禁用 Node ID 的 Proxy 回调结构体。
  * 在配置客户端中新增对响应地址的检查。
  * 引入新的确认消息 API。
  * 重新设计了周期性发布定时器和轮询超时调度逻辑。
  * 在 ``cfg_srv`` 中报告已配置的 ``LPNTimeout``。
  * 确保配置输出计数至少为 1。
  * 确保使用好友凭据加密初始好友轮询。
  * 停止在重传时重置 PB ADV 可靠定时器。

* 蓝牙 LE 拆分软件控制器

  * 移除对 nRF5340 PDK 的支持。请改用 nRF5340 DK。
  * 新增方向查找的基本支持。
  * 新增通过周期性广播进行 CTE 无连接传输和接收的支持。
  * 新增在方向查找上下文中进行天线切换的支持。
  * 新增无效的 ACL 数据长度检查。
  * 新增 ISO 适配层的基本支持。
  * 新增广播等时组和流的实验性支持。
  * 新增连接等时组和流的部分实验性支持。
  * 实现了扩展连接创建和取消。
  * 更改策略：忽略来自已连接对端的连接请求。
  * 新增控制流程锁定系统。
  * 为 Nordic nRF53x SoC 系列新增 GPIO PA/LNA 支持。
  * 为 nRF21540 IC 新增 FEM 支持。
  * 新增配置 CTE RX 路径的新无线电 API。

* HCI 驱动

  * 新增对 Espressif ESP32 平台的支持。

板级与 SoC 支持
********************

* 新增对这些 SoC 系列的支持：

  * STM32F205xx
  * STM32G03yxx、STM32G05yxx、STM32G070xx 和 STM32G0byxx
  * STM32G4x1、STM32G4x3 和 STM32G484xE
  * STM32WL55xx
  * Nuvoton npcx7m6fc 和 npcx7m6fc
  * Renesas R-Car Gen3
  * Silicon Labs EFR32FG13P
  * ARM MPS3-AN547
  * ARM FVP-AEMv8A
  * ARM FVP-AEMv8R
  * NXP LS1046A
  * X86 Lakemont

* 移除对这些 SoC 系列的支持：

   * ARM Musca-A

* 在其他 SoC 系列中进行了以下更改：

  * 新增 Cypress PSoC-6 pinctrl 支持。
  * STM32 L4/L5/WB 系列已更新以提供更好的电源管理支持（CONFIG_PM=y）。
  * 在部分 STM32 系列（F2/F4/F7/H7）上新增备份 SRAM
  * 在 STM32 SoC 上将 TRACE_MODE 设置为异步并启用跟踪输出引脚

* ARC 板级的更改：

  * 新增带有 ARCv3 64 位 HS6x 处理器的 nSIM 和 QEMU 仿真板
    （nsim_hs6x 和 qemu_arc_hs6x）
  * 在 qemu_arc_hs 和 qemu_arc_em 板上启用 MPU
  * 在 HSDK 板上新增 cy8c95xx GPIO 扩展器支持

* 新增对这些 ARM 板级的支持：

   * Actinius Icarus
   * Actinius Icarus SoM
   * Laird Connectivity BL654 Sensor Board
   * Laird Connectivity Sentrius BT6x0 Sensor
   * EFR32 Radio BRD4255A Board
   * MPS3-AN547
   * RAK4631
   * Renesas R-Car H3ULCB
   * Ronoth LoDev（基于 AcSIP S76S / STM32L073）
   * nRF9160 Thing Plus
   * ST Nucleo F030R8
   * ST Nucleo G0B1RE
   * ST Nucleo H753ZI
   * ST Nucleo L412RP-P
   * ST Nucleo WL55JC
   * ST STM32G071B Discovery
   * Thingy:53
   * u-blox EVK-BMD-30/35：BMD-300-EVAL、BMD-301-EVAL 和 BMD-350-EVAL
   * u-blox EVK-BMD-330：BMD-330-EVAL
   * u-blox EVK-BMD-34/38：BMD-340-EVAL 和 BMD-341-EVAL
   * u-blox EVK-BMD-34/38：BMD-345-EVAL
   * u-blox EVK-BMD-360：BMD-360-EVAL
   * u-blox EVK-BMD-34/48：BMD-380-EVAL
   * u-blox EVK-ANNA-B11x
   * u-blox EVK NINA-B11x
   * u-blox EVK-NINA-B3
   * u-blox EVK NINA-B40x

* 新增对这些 ARM64 板级的支持：

   * fvp_base_revc_2xaemv8a
   * fvp_baser_aemv8r
   * nxp_ls1046ardb

* 移除对这些 ARM 板级的支持：

   * ARM V2M Musca-A
   * Nordic nRF5340 PDK

* 移除对这些 X86 板级的支持：

   * up_squared_32
   * qemu_x86_coverage
   * minnowboard

* 在其他板级中进行了以下更改：

  * cy8ckit_062_ble：重构为通过 pinctrl 配置。
  * cy8ckit_062_ble：新增对带中断的 SCB[uart] 的支持。
  * cy8ckit_062_ble：新增对 SCB[spi] 的支持。
  * cy8ckit_062_ble：新增板级修订模式。
  * cy8ckit_062_wifi_bt：重构为通过 pinctrl 配置。
  * cy8ckit_062_wifi_bt：新增对带中断的 SCB[uart] 的支持。
  * lpcxpresso55s16：由于该板级不支持 Trusted Firmware M（TF-M），
    已从 lpcxpresso55s16_ns 重命名为 lpcxpresso55s16。
  * lpcxpresso55s28：由于该板级不支持 Trusted Firmware M（TF-M），
    已移除 lpcxpresso55s28_ns 配置。
  * mimxrt685_evk：新增对八线 SPI 闪存存储、LittleFS、I2S、OS 定时器和
    电源管理的支持。
  * mimxrt1060_evk：新增对 QSPI 闪存存储、LittleFS 和 mcuboot 的支持。
  * mimxrt1064_evk：新增对 mcuboot 的支持。

* 新增对以下扩展板的支持：

  * FTDI VM800C 嵌入式视频引擎板
  * 通用 ST7735R 显示扩展板
  * NXP FRDM-STBC-AGM01
  * Semtech SX1272MB2DAS LoRa 扩展板

驱动与传感器
*******************

* ADC

  * 新增对 TI CC32xx 的支持。
  * 新增对 ITE IT8xxx2 的支持。
  * 在 MCUX ADC16 驱动中新增对 DMA 和硬件触发的支持。
  * 新增 ADC 仿真器。
  * 移动了 ADC 采集时间宏的定义，使得这些宏可以在 dts 文件中使用。

* 蓝牙

  * 移除了 Kconfig 选项 ``CONFIG_BT_CTLR_TO_HOST_UART_DEV_NAME``。
    请改用 :ref:`zephyr,bt-c2h-uart chosen 节点 <devicetree-chosen-nodes>`。

* CAN

  * 新增基于 Bosch M_CAN IP 的 CAN-FD 驱动。该驱动
    目前支持 STM32G4 系列 MCU。对 Microchip
    SAM 和 NXP 芯片的额外支持正在进行中。

  * CAN ISO-TP 子系统已增强，允许填充和固定寻址。

* 时钟控制

  * 在 STM32 系列上，系统时钟配置已从 Kconfig 移至 DTS。
    现有 Kconfig 专用符号（CONFIG_CLOCK_STM32_FOO）的使用现在
    已弃用。
  * 为 Renesas R-Car 平台新增时钟控制驱动

* 控制台

  * 新增 ``UART_CONSOLE_INPUT_EXPIRED`` 和 ``UART_CONSOLE_INPUT_EXPIRED_TIMEOUT``
    Kconfig 选项，用于通知电源管理模块 UART 控制台当前正在使用，
    并禁止其进入低功耗状态。

* 计数器

   * 新增对 ESP32 计数器的支持

* DAC

   * 新增对 Microchip MCP4725 的支持

* 磁盘

  * 在 STM32L4+ 上新增 SDMMC 支持

* 显示

  * 新增对 ST7735R 的支持

* 磁盘

  * 将磁盘驱动（``disk_access_*.c``）移至 ``drivers/disk`` 并根据
    其功能重命名。
  * 修复了 USDHC 驱动中的 CMD6 支持。
  * 修复了 ``sdmmc_spi.c`` 驱动中初始化后时钟频率切换的问题。

* DMA

  * 新增对 STM32G0 和 STM32H7 的支持

* EEPROM

  * 新增对闪存中模拟的 EEPROM 的支持。

* ESPI

  * 新增对 Microchip eSPI SAF 的支持

* 以太网

  * 在 e1000 以太网控制器中新增仿真 PTP 时钟。这允许使用 Qemu
    进行简单的 PTP 时钟测试。
  * 在 mcux 和 gmac 驱动中将 PTP 时钟与 gPTP 支持分离。这允许
    应用在不启用 gPTP 支持的情况下使用 PTP 时钟。
  * 在 mcux 驱动中将时钟控制转换为使用 DEVICE_DT_GET。
  * 更改为允许在 gmac 驱动中更改 MAC 地址。
  * STM32H7 的驱动现在使用特定的内存布局以满足 RAM 访问的
    DMA 约束。

* 闪存

  * flash_write_protection_set() 已弃用，并将在
    Zephyr 2.8 中移除。写/擦除保护管理的责任已
    移至 flash_write() 和 flash_erase() API 调用的驱动特定实现。
    所有树内闪存驱动均已更新，
    并从其 API 表中移除了 protect 实现。
    在弃用期间，调用 flash_write_protection_set() 的用户代码
    将没有效果，但如果 API 表中存在 protect 实现，
    flash_write() 和 flash_erase() 驱动垫片将用对 protect
    实现的调用包装其调用。
    树外驱动必须在弃用期结束移除垫片中的包装之前进行更新。
  * 在 STM32F7 上新增 QSPI 支持。

* GPIO

  * :c:struct:`gpio_dt_spec`：一种新的结构体，使得
    访问 :ref:`设备树 <dt-guide>` 中的 GPIO 配置更加方便。
  * 用于初始化 ``gpio_dt_spec`` 值的新宏：
    :c:macro:`GPIO_DT_SPEC_GET_BY_IDX`、:c:macro:`GPIO_DT_SPEC_GET_BY_IDX_OR`、
    :c:macro:`GPIO_DT_SPEC_GET`、:c:macro:`GPIO_DT_SPEC_GET_OR`、
    :c:macro:`GPIO_DT_SPEC_INST_GET_BY_IDX`、
    :c:macro:`GPIO_DT_SPEC_INST_GET_BY_IDX_OR`、
    :c:macro:`GPIO_DT_SPEC_INST_GET` 和 :c:macro:`GPIO_DT_SPEC_INST_GET_OR`
  * 用于使用 ``gpio_dt_spec`` 值的新辅助函数：
    :c:func:`gpio_pin_configure_dt`、:c:func:`gpio_pin_interrupt_configure_dt`
  * 移除 :c:func:`gpio_pin_configure() 中 ``GPIO_INT_*`` 标志的支持。
    该功能已在 Zephyr 2.2 发布中弃用。中断
    标志现在仅由 :c:func:`gpio_pin_interrupt_configure()`
    函数接受。
  * STM32 GPIO 驱动现在支持使用 PM_DEVICE 和 PM_DEVICE_RUNTIME 进行时钟门控
  * 为 Renesas R-Car 平台新增 GPIO 驱动

* 硬件信息

  * 新增对 Silicon Labs Gecko SoC 的支持

* I2C

  * 新增对 STM32F2 的支持

* I2S

  * 新增对 NXP LPC 设备的支持

* IEEE 802.15.4

  * 修复了 IEEE 802.15.4 L2 驱动中的各种问题。

  * nrf5：

    * 使硬件无线电能力变为运行时配置。
    * 在序列化主机上启用 CSMA-CA。
    * 更改驱动以从 UICR 加载 EUI64。

  * rf2xx：

    * 新增对 tx 模式 direct 的支持。
    * 新增对 tx 模式 CCA 的支持。
    * 新增对启用混杂模式的支持。
    * 新增对启用 PAN 协调器模式的支持。

* 中断控制器

  * 将共享中断控制器配置移至基于设备树。

* LED

  * 新增对 LED GPIO 的支持
  * 为 LED PWM 新增电源管理支持

* LoRa

  * 新增对 SX1272 的支持

* 调制解调器

  * 将 wncm14a2a、quectel-bg9x、hl7800 和 ublox-sara-r4 驱动转换为使用
    新的 DT 设备宏。
  * 更改 GSM 调制解调器以在启动时可选执行出厂复位。
  * 为 GSM 调制解调器新增自动启动支持。
  * 在 BG9X 中新增等待 RDY 而非轮询 AT。
  * 修复了 BG9X 的 PDP 上下文管理。
  * 为 ublox-sara-r4 新增 TLS 卸载支持。
  * 在 ublox-sara-r4 中使复位引脚变为可选。
  * 修复了 hl7800 中的潜在缓冲区溢出。
  * 修复了 64 位平台上的构建错误。
  * 在 PPP 驱动中新增对拨号调制解调器的支持。

* PWM

  * 新增对 STM32F2 和 STM32L1 的支持。
  * 新增对 Silicon Labs Gecko SoC 的支持。

* 传感器

  * 新增对 STM32 内部（CPU）温度传感器的支持。
  * 重构了多个 ST 传感器驱动以使用 gpio_dt_spec 宏和通用
    stmemc 例程，支持多实例，并在设备树中配置 ODR/range
    属性。
  * 新增符合 SBS 1.1 规范的电量计驱动。
  * 新增 MAX17262 电量计驱动。
  * 新增 BMP388 压力传感器驱动。
  * 新增 Atmel SAM QDEC 驱动。
  * 新增 TI FDC2X1X 驱动。
  * 在现有 MPU6050 6 轴运动跟踪驱动中新增对 MPU9250 的支持。
  * 重构了 BME280 温度/压力传感器驱动。
  * 新增 BMI270 IMU 驱动。
  * 新增 Nuvoton 测速仪传感器驱动。
  * 新增 MAX6675 冷端补偿 K 型热电偶到数字转换器。

* 串行

  * 扩展 Cypress PSoC-6 SCB[uart] 驱动以支持中断。
  * 为 Renesas R-Car 平台新增 UART 驱动

* SPI

  * 新增 Cypress PSoC-6 SCB[spi] 驱动。
  * 默认 SPI_SCK 配置现在对所有 STM32 都是下拉，以最小化
    停止模式下的功耗。

* 定时器

  * 新增 x86 APIC TSC_DEADLINE 驱动。
  * 新增对 NXP MCUX OS 定时器的支持。
  * 新增对 Nuvoton NPCX 系统定时器的支持。
  * 为 Renesas R-Car 平台新增 CMT 驱动。

* USB

  * 新增对 STM32H7 的支持
  * 在 usb_dc_nrfx 驱动中新增连接事件延迟

* 看门狗

  * 新增对 TI CC32xx 看门狗的支持。

* WiFi

  * 将 eswifi 和 esp 驱动转换为新的 DT 设备宏

  * esp：

    * 修复了主机名配置。
    * 移除了 POSIX API 依赖。
    * 将卸载驱动从 esp 重命名为 esp_at。
    * 新增 esp32 wifi 驱动支持。

网络
**********

* 802.15.4 L2：

  * 修复了一个 bug，其中 net_pkt 结构体在经过 802.15.4 L2 处理后
    包含无效的 LL 地址指针。
  * 在 802.15.4 L2 中新增可选的目标地址过滤。

* CoAP：

  * 在 :c:struct:`coap_packet` 结构体中新增 ``user_data`` 字段。
  * 修复了乱序通知的处理。
  * 修复了 :c:func:`coap_packet_get_payload` 函数。
  * 将 CoAP 测试套件转换为 ztest API。
  * 改进了 :c:func:`coap_packet_get_payload` 函数以最小化
    RNG 调用次数。
  * 修复了 ``coap_server`` 示例中的重传。
  * 修复了 ``coap_server`` 示例中的观察者移除（在通知
    超时时）。

* DHCPv4：

  * 修复了一个 bug，其中 DHPCv4 库在从服务器获取新网关之前
    移除了静态配置的网关。

* DNS：

  * 修复了一个 bug，其中当从服务器获取多个 IP 地址时，
    使用相同的 IP 地址来填充结果地址信息条目。

* DNS-SD：

  * 新增服务类型枚举支持（``_services._dns_sd._udp.local``）

* HTTP：

  * 将库切换到使用 ``zsock_*`` API，以改进与
    各种 POSIX 配置的兼容性。
  * 修复了一个 bug，其中 ``HTTP_DATA_FINAL`` 通知即使对于
    中间响应片段也会触发。

* IPv6：

  * 多个 IPv6 修复，解决 IPv6Ready 合规测试中的失败。

* LwM2M：

  * 新增对向应用报告通知超时的支持。
  * 修复了一个 bug，其中只有一个活动实例的多实例资源
    在读取时编码不正确。
  * 修复了一个 bug，其中对不可读资源的变化会生成通知。
  * 为 ``lwm2m_rd_client`` 模块的状态变量新增互斥锁保护。
  * 移除 LWM2M_RES_TYPE_U64 类型，因为对于大值
    无法正确编码。
  * 修复了一个 bug，其中大无符号整数在 TLV 中编码不正确。
  * LwM2M 引擎和编码器中 FLOAT 类型处理的多个修复。
  * 修复一个 bug，其中 IPSO 按钮计数器资源在递增时
    未触发通知。
  * 修复了一个 bug，其中注册失败被报告为成功
    给应用。

* 其他：

  * 在 ``big_http_download`` 示例中新增套接字的 RX/TX 超时。
  * 引入 :c:func:`net_pkt_remove_tail` 函数。
    在 :c:struct:`net_pkt` 结构体中新增 IEEE 802.15.4 安全相关标志。
  * 在以太网 L2 中新增桥接支持。
  * 修复了 mDNS 中的一个 bug，其中可能将错误的地址类型
    设置为响应目标。
  * 新增抑制 ICMP 目标不可达错误的选项。
  * 修复了 ``net nbr`` shell 命令中可能的断言。
  * TFTP 库的重大重构。

* MQTT：

  * 新增注册自定义传输类型的选项。
  * 修复了 :c:func:`mqtt_abort 中的一个 bug，其中函数可能在不
    释放锁的情况下返回。

* OpenThread：

  * 将 OpenThread 模块更新到提交 ``9ea34d1e2053b6b2a80e1d46b65a6aee99fc504a``。
    新增多个新的 Kconfig 选项以与新的 OpenThread
    配置保持一致。
  * 在初始化期间新增 OpenThread API 互斥锁保护。
  * 将 OpenThread 线程转换为专用工作队列。
  * 实现缺失的 :c:func:`otPlatAssertFail` 平台函数。
  * 修复了一个 bug，其中 NONE 级别的 OpenThread 日志未处理。
  * 新增禁用 CSL 采样的可能性，当使用时。
  * 修复了一个潜在 bug，其中平台无线电层可能向 OpenThread
    返回无效的错误代码。
  * 重新设计了 OpenThread 协处理器示例中的 UART 配置。

* 套接字：

  * 在 :c:func:`zsock_select` 函数中新增微秒精度。
  * 将 :c:func:`zsock_select` 重构为系统调用。
  * 修复了一个 bug，其中 :c:func:`poll` 事件未正确
    为 socketpair 套接字发出信号。
  * 修复了一个 bug，其中套接字互斥锁可能在新所有者
    初始化后被使用，在 :c:func:`zsock_close` 中释放后。
  * 修复了启用 CAN 套接字后可能的断言。
  * 修复了数据包套接字实现中 IPPROTO_RAW 的使用。

* TCP：

  * 修复了一个 bug，其中 ``unacked_len`` 可能被设置为负值。
  * 修复了 :c:func:`tcp_send_data` 中可能的断言失败。
  * 修复了一个 bug，其中 [FIN, PSH, ACK] 未在
    TCP_FIN_WAIT_2 状态中正确处理。

* TLS：

  * 将 TLS 套接字重构为使用 Zephyr 的安全随机数生成器。
  * 修复了与卸载套接字进行 DTLS 握手期间的忙循环。
  * 修复了非阻塞套接字上 TLS/DTLS 握手期间的忙循环。
  * 在超时的 DTLS 握手中重置 mbed TLS 会话，以允许重试而
    不关闭套接字。
  * 修复了 TLS/DTLS :c:func:`sendmsg` 实现以支持更大的负载。
  * 修复了 TLS/DTLS 套接字的 ``POLLHUP`` 通知。

* WebSocket：

  * 修复了 WebSocket 的 :c:func:`poll` 实现，其与
    卸载套接字一起无法正确工作。
  * 修复了 WebSocket 的 :c:func:`ioctl` 实现，其与
    卸载套接字一起无法正确工作。

USB
***

* 新增一个新头文件，其中应包含所有第 9 章
  （USB 设备框架）的定义和结构体。
* 修订了 USB 设备支持的配置。
  移除 Kconfig 选项 ``CONFIG_USB``，引入 Kconfig 选项
  ``CONFIG_USB_DEVICE_DRIVER`` 以启用 USB 设备控制器驱动，
  当选项 ``CONFIG_USB_DEVICE_STACK`` 启用时选中。
* 增强了设备协议栈、类和示例中控制请求的验证。
* 新增存储备用接口设置的支持。
* 在所有支持 USB 的板级上新增 ``zephyr_udc0`` nodelabel，以允许
  构建通用 USB 设备支持示例。
* 重新设计了 CDC ACM 类中的描述符、配置和数据定义宏。
* 更改了 CDC ACM UART 实现以从设备树获取配置。
  通过此更改，许多 ``CONFIG_*_ON_DEV_NAME`` 选项已被移除，
  应用已修订。更多信息参见 :ref:`usb_device_cdc_acm`。

构建基础设施
************************

* 设备树 API

  * 新的"for-each"宏，其工作方式类似于现有 API，但接受
    可变数量的参数：:c:macro:`DT_FOREACH_CHILD_VARGS`、
    :c:macro:`DT_FOREACH_CHILD_STATUS_OKAY_VARGS`、
    :c:macro:`DT_FOREACH_PROP_ELEM_VARGS`、
    :c:macro:`DT_INST_FOREACH_CHILD_VARGS`、
    :c:macro:`DT_INST_FOREACH_STATUS_OKAY_VARGS`、
    :c:macro:`DT_INST_FOREACH_PROP_ELEM_VARGS`

  * 其他新的"for-each"宏：:c:macro:`DT_FOREACH_STATUS_OKAY`、
    :c:macro:`DT_FOREACH_STATUS_OKAY_VARGS`

  * 用于将字符串转换为 C 令的新宏：:c:macro:`DT_STRING_TOKEN`、
    :c:macro:`DT_STRING_UPPER_TOKEN`

  * 新的 :ref:`devicetree-pinctrl-api` 辅助宏

* 设备树工具

  * 当在搜索绑定时发现无效 YAML 文件时，现在会生成错误。
    更多信息参见 :ref:`dt-where-bindings-are-located`。

  * 以 ``.yml`` 结尾的文件名现在在搜索绑定时被视为 YAML 文件。

  * 当使用无效的节点名称时，现在会生成错误。例如，
    节点名称 ``node?`` 现在会生成一条以 ``node?: Bad
    character '?' in node name`` 结尾的错误消息。
    有效的节点名称在设备树规范 v0.3 的"2.2.2 Node Names"中有文档说明。

  * 当 :ref:`compatible 属性
    <dt-important-props>` 使用 ``vendor,device`` 格式且使用未知的
    供应商前缀时，现在会生成警告。此警告不适用于根节点。

    已知的供应商前缀定义在
    :file:`dts/bindings/vendor-prefixes.txt` 文件中，这些文件可能出现在
    :ref:`DTS_ROOT <dts_root>` 中的任何目录。

    这些警告可以通过 edtlib Python API 升级为错误；
    Zephyr 的 CI 现在会生成此类错误。

* 设备树绑定

  * 各种绑定在其 :ref:`compatible
    <dt-important-props>` 属性中具有错误的供应商前缀；
    以下更改已做出以修复这些。

    .. list-table::
       :header-rows: 1

       - * 旧 compatible
         * 新 compatible
       - * ``nios,i2c``
         * :dtcompatible:`altr,nios2-i2c`
       - * ``cadence,tensilica-xtensa-lx4``
         * :dtcompatible:`cdns,tensilica-xtensa-lx4`
       - * ``cadence,tensilica-xtensa-lx6``
         * :dtcompatible:`cdns,tensilica-xtensa-lx6`
       - * ``colorway,lpd8803``
         * :dtcompatible:`greeled,lpd8803`
       - * ``colorway,lpd8806``
         * :dtcompatible:`greeled,lpd8806`
       - * ``grove,light``
         * :dtcompatible:`seeed,grove-light`
       - * ``grove,temperature``
         * :dtcompatible:`seeed,grove-temperature`
       - * ``max,max30101``
         * :dtcompatible:`maxim,max30101`
       - * ``ublox,sara-r4``
         * :dtcompatible:`u-blox,sara-r4`
       - * ``xtensa,core-intc``
         * :dtcompatible:`cdns,xtensa-core-intc`
       - * ``vexriscv,intc0``
         * :dtcompatible:`vexriscv-intc0`

    树外用户需要更新他们的
    设备树。

    您可以通过在节点的 compatible 属性中包含新旧值
    来用一个设备树支持多个版本的 Zephyr，
    如下面的 LPD8803 示例::

        my-led-strip@0 {
                compatible = "colorway,lpd8803", "greeled,lpd8803";
                ...
        };

  * 按字母顺序排列的其他新绑定：:dtcompatible:`andestech,atcgpio100`、
    :dtcompatible:`arm,gic-v3-its`、:dtcompatible:`atmel,sam0-gmac`、
    :dtcompatible:`atmel,sam0-pinctrl`、:dtcompatible:`atmel,sam-dac`、
    :dtcompatible:`atmel,sam-mdio`、:dtcompatible:`atmel,sam-usbc`、
    :dtcompatible:`cdns,tensilica-xtensa-lx7`、
    :dtcompatible:`espressif,esp32c3-uart`、
    :dtcompatible:`espressif,esp32-intc`、
    :dtcompatible:`espressif,esp32s2-uart`、:dtcompatible:`ethernet-phy`、
    :dtcompatible:`fcs,fxl6408`、:dtcompatible:`ilitek,ili9341`、
    :dtcompatible:`ite,it8xxx2-bbram`、:dtcompatible:`ite,it8xxx2-kscan`、
    :dtcompatible:`ite,it8xxx2-pinctrl-conf`、:dtcompatible:`ite,it8xxx2-pwm`、
    :dtcompatible:`ite,it8xxx2-pwmprs`、:dtcompatible:`ite,it8xxx2-watchdog`、
    :dtcompatible:`lm75`、:dtcompatible:`lm77`、:dtcompatible:`meas,ms5607`、
    :dtcompatible:`microchip,ksz8863`、:dtcompatible:`microchip,mcp7940n`、
    :dtcompatible:`microchip,xec-adc-v2`、:dtcompatible:`microchip,xec-ecia`、
    :dtcompatible:`microchip,xec-ecia-girq`、
    :dtcompatible:`microchip,xec-gpio-v2`、
    :dtcompatible:`microchip,xec-i2c-v2`、:dtcompatible:`microchip,xec-pcr`、
    :dtcompatible:`microchip,xec-uart`、:dtcompatible:`nuvoton,npcx-bbram`、
    :dtcompatible:`nuvoton,npcx-booter-variant`、
    :dtcompatible:`nuvoton,npcx-ps2-channel`、
    :dtcompatible:`nuvoton,npcx-ps2-ctrl`、:dtcompatible:`nuvoton,npcx-soc-id`、
    :dtcompatible:`nxp,imx-ccm-rev2`、:dtcompatible:`nxp,lpc-ctimer`、
    :dtcompatible:`nxp,lpc-uid`、:dtcompatible:`nxp,mcux-usbd`、
    :dtcompatible:`nxp,sctimer-pwm`、:dtcompatible:`ovti,ov2640`、
    :dtcompatible:`renesas,rcar-can`、:dtcompatible:`renesas,rcar-i2c`、
    :dtcompatible:`reserved-memory`、:dtcompatible:`riscv,sifive-e24`、
    :dtcompatible:`sensirion,sgp40`、:dtcompatible:`sensirion,sht4x`、
    :dtcompatible:`sensirion,shtcx`、:dtcompatible:`silabs,si7055`、
    :dtcompatible:`silabs,si7210`、:dtcompatible:`snps,creg-gpio`、
    :dtcompatible:`st,i3g4250d`、:dtcompatible:`st,stm32-aes`、
    :dtcompatible:`st,stm32-dma`、:dtcompatible:`st,stm32-dma-v2bis`、
    :dtcompatible:`st,stm32-hsem-mailbox`、:dtcompatible:`st,stm32-nv-flash`、
    :dtcompatible:`st,stm32-spi-subghz`、
    :dtcompatible:`st,stm32u5-flash-controller`、
    :dtcompatible:`st,stm32u5-msi-clock`、:dtcompatible:`st,stm32u5-pll-clock`、
    :dtcompatible:`st,stm32u5-rcc`、:dtcompatible:`st,stm32wl-hse-clock`、
    :dtcompatible:`st,stm32wl-subghz-radio`、:dtcompatible:`st,stmpe1600`、
    :dtcompatible:`syscon`、:dtcompatible:`telink,b91`、
    :dtcompatible:`telink,b91-flash-controller`、
    :dtcompatible:`telink,b91-gpio`、:dtcompatible:`telink,b91-i2c`、
    :dtcompatible:`telink,b91-pinmux`、:dtcompatible:`telink,b91-power`、
    :dtcompatible:`telink,b91-pwm`、:dtcompatible:`telink,b91-spi`、
    :dtcompatible:`telink,b91-trng`、:dtcompatible:`telink,b91-uart`、
    :dtcompatible:`telink,b91-zb`、:dtcompatible:`ti,hdc2010`、
    :dtcompatible:`ti,hdc2021`、:dtcompatible:`ti,hdc2022`、
    :dtcompatible:`ti,hdc2080`、:dtcompatible:`ti,hdc20xx`、
    :dtcompatible:`ti,ina219`、:dtcompatible:`ti,ina23x`、
    :dtcompatible:`ti,tca9538`、:dtcompatible:`ti,tca9546a`、
    :dtcompatible:`ti,tlc59108`、
    :dtcompatible:`xlnx,gem`、:dtcompatible:`zephyr,bbram-emul`、
    :dtcompatible:`zephyr,cdc-acm-uart`、:dtcompatible:`zephyr,gsm-ppp`、
    :dtcompatible:`zephyr,native-posix-udc`

* West（扩展）

    * openocd runner：Zephyr 线程感知现在在 GDB 中默认可用
      对于在 :ref:`kconfig` 中将 :kconfig:option:`CONFIG_DEBUG_THREAD_INFO` 设置为 ``y`` 的应用构建。
      这适用于 ``west debug``、``west debugserver``、
      和 ``west attach``。必须在主机系统上安装
      0.11.0 之后的 OpenOCD 版本。

库 / 子系统
**********************

* 磁盘


* 管理


* CMSIS 子系统


* 电源管理

  * 用于设置/清除/检查设备从电源管理
    角度是否忙乱的 API 已移至 PM 子系统。其命名和签名
    也已调整以遵循通用约定。您可以在下面找到
    等价列表。

    * ``device_busy_set`` -> ``pm_device_busy_set``
    * ``device_busy_clear`` -> ``pm_device_busy_clear``
    * ``device_busy_check`` -> ``pm_device_is_busy``
    * ``device_any_busy_check`` -> ``pm_device_is_any_busy``

  * 设备电源管理回调（``pm_device_control_callback_t``）已
    大幅简化以基于*操作*工作，导致更简单和
    更自然的实现。这一原则也被其他操作系统使用，例如
    Linux 内核。因此，回调参数列表已减少
    到设备实例和一个操作（例如 ``PM_DEVICE_ACTION_RESUME``）。
    其他改进包括指定错误代码、移除一些
    未使用/不清晰的状态，或保证，例如避免在设备
    已处于正确状态时为其调用挂起/恢复。所有这些更改
    一起使得简化多个设备电源管理回调
    实现成为可能。

  * 引入新的 API 以允许能够唤醒系统的设备
    注册自己为唤醒源。这允许应用
    选择唤醒系统的最合适方式当它
    挂起时。标记为唤醒源的设备在系统
    空闲时不会被内核挂起。可以直接在设备树中声明设备唤醒能力，如下面的示例::

        &gpio0 {
                compatible = "zephyr,gpio-emul";
                gpio-controller;
                wakeup-source;
        };

    * 移除 ``PM_DEVICE_STATE_FORCE_SUSPEND`` 设备电源状态，因为
      它是一个操作而不是状态。

    * 移除 ``PM_DEVICE_STATE_RESUMING`` 和 ``PM_DEVICE_STATE_SUSPENDING``。
      它们是过渡状态，仅用于设备运行时。现在
      子系统使用设备标志来跟踪过渡。

    * 将约束 API 实现为弱符号，以便应用或平台
      可以覆盖它们。平台可以有自己的方式
      在其驱动中设置/释放约束，这些驱动不是
      Zephyr 代码库的一部分。

* 日志

* MODBUS

  * 更改服务器处理程序以将事务和协议标识符
    复制到响应头。

* 随机

  * xoroshiro128+ PRNG 已弃用，建议改用 xoshiro128++

* Shell


* 存储


* 任务看门狗


* 跟踪

* 调试

* OS

HAL
****

* HAL 现在已从主树移出作为外部模块，并位于
  其自身的独立仓库中。

Trusted Firmware-m
******************

* 将 psa_level_1 示例重命名为 psa_crypto。扩展了示例代码中 PSA Cryptography
  1.0 API 的使用，以展示额外的加密功能。
* 新增一个新示例以展示 PSA Protecter Storage 服务。

文档
*************

* Kconfig 选项现在需要使用 ``:kconfig:option:`` Sphinx 角色引用。
  在此更改之前，``:option:`` 用于此目的。
* Doxygen 别名 ``@config{}`` 已弃用，建议改用 ``@kconfig{}``。

测试与示例
*****************

Issue 相关条目
*******************

* :github:`39443` -  更多 inclusive
* :github:`39419` - STM32WL55 not found st/wl/stm32wl55jcix-pinctrl.dtsi
* :github:`39413` - 警告 当...时 使用 newlibc 和 线程
* :github:`39409` - runners: canopen: program download fails with slow flash access and/or congested CAN nets
* :github:`39389` - http_get, big_http_download samples fails to build
* :github:`39388` - GSM Modem sample fails to build
* :github:`39378` - Garbage IQ 数据 Reports  生成 如果 一些 检查 在...中 hci_df_prepare_connectionless_iq_report 失败
* :github:`39294` - noticing stm32 clock domain naming changes
* :github:`39291` - Bluetooth: Periodic advertising
* :github:`39284` - mdns + dns_sd: fix regression that breaks ptr queries
* :github:`39281` - Undefined references to k_thread_abort related tracing routines
* :github:`39270` - example-application CI build fails
* :github:`39263` - Bluetooth: controller: DF: wrong handling of max_cte_count
* :github:`39260` - [backport v2.7-branch] backport of #38292 failed
* :github:`39240` - ARC Kconfig allows so select IRQ configuration which isn't supported in SW
* :github:`39206` - lwm2m: send_attempts field does not seem to be used?
* :github:`39205` - drivers: wifi: esp_at: cannot connect to open (unsecure) WiFi networks
* :github:`39195` - USB: netusb: example echo_server not working as expected
* :github:`39190` - tests/subsys/logging/log_core_additional/logging.add.log2 fails
* :github:`39188` - tests/bluetooth/mesh/bluetooth.mesh.ext_adv fails
* :github:`39185` - tests/subsys/logging/log_core_additional/logging.add.user 失败 在...上 几个 平台
* :github:`39180` - samples/subsys/mgmt/osdp/peripheral_device & samples/subsys/mgmt/osdp/control_panel fail to build
* :github:`39170` - Can not run correctly on NXP MIMXRT1061 CVL5A.
* :github:`39135` - samples/compression/lz4 build failed (lz4.h: No such file or directory)
* :github:`39132` - subsys/net/ip/tcp2: 缺失 feature 到 减少 接收 Window 大小 发送 在...中  ACK messge
* :github:`39123` - ztest: 损坏 在...上 NRF52840 平台
* :github:`39115` - sensor: fdc2x1x: 警告 和 compilation 错误 当...时 PM_DEVICE  使用
* :github:`39086` - CMake warning during build - depracated roule CMP0079
* :github:`39085` - Ordering of device_map() breaks PCIe config space mapping on ARM64
* :github:`39075` - IPv6 地址 不 设置 在...上 loopback 接口
* :github:`39051` - Zephyr was unable to find the toolchain. Is the environment misconfigured?
* :github:`39036` - Multicast packet forwarding not working for the coap_server sample and Openthread
* :github:`39022` - [backport v2.7-branch] backport of #38834 failed
* :github:`39011` - Bluetooth: Mesh: Model extensions walk stops before last model
* :github:`39009` - Nordic PWM causing lock up due to infinte loop
* :github:`39008` - tests: logging.add.user: build failure on STM32H7 targets
* :github:`38999` - [backport v2.7-branch] backport of #38407 failed
* :github:`38996` - There  不 way 到 离开  ipv6 multicast 分组
* :github:`38994` - ARP: Replies are sent to multicast MAC address rather than senders MAC address.
* :github:`38970` - LWM2M Client Sample with DTLS enabled fail to connect
* :github:`38966` - Please add STM32F412VX
* :github:`38961` - tests: kernel: sched: schedule_api: instable on disco_l475_iot1
* :github:`38959` - ITE RISCV I2C driver returning positive values for error instead of negative values
* :github:`38943` - west: update hal_espressif failure
* :github:`38938` - Bluetooth tester application should be able return L2CAP ECFC credits on demand
* :github:`38930` - Low Power mode not functional on nucleo_l073rz
* :github:`38924` - twister: cmake: Misleading error in Twister when sdk-zephyr 0.13.1 not used
* :github:`38904` - [backport v2.7-branch] backport of #38860 failed
* :github:`38902` - i2c_nrfx_twim: 错误 0x0BAE0002 如果 sensor  设置 在...中 trigger 模式 和 复位 带 nrf 设备
* :github:`38899` - There  不 有效 日期 设置 函数 在...中  RTC 驱动 的  LL 库 的 STM32
* :github:`38893` - g0b1re + spi_flash_at45 + flash_shell: First write always fails with ``CONFIG_PM_DEVICE``
* :github:`38886` - devicetree/memory.h probably should not exist as-is
* :github:`38877` - Running the zephyr elf natively on an arm a53 machine (ThunderX2) with KVM emulation
* :github:`38870` - stm32f1: Button callback not fired
* :github:`38853` - Bluetooth: host: bt_unpair failed because function [bt_conn_set_state] wont work as expected
* :github:`38849` - drivers: i2c: nrf: i2c error with burst write
* :github:`38829` - net_buf issue leads to unwanted elem free
* :github:`38826` - tests/lib/cmsis_dsp: malloc failed on 128K SRAM targets
* :github:`38818` - 驱动 display display_st7789v.c 构建 错误
* :github:`38815` - kernel/mem_domain: Remove dead case in check_add_partition()
* :github:`38807` - stm32: 缺失 头文件 在...中 power.c 文件
* :github:`38804` - tests\kernel\threads\thread_stack 测试 失败 带 ARC
* :github:`38799` - BLE central_ht only receives 7 notifications
* :github:`38796` - 失败 构建  zephyr\tests\subsys\cpp\libcxx project
* :github:`38791` - Example code_relocation not compiling.
* :github:`38790` - SD FatFS Sample Build Failure
* :github:`38784` - stm32: pm: Debug mode not functional on G0
* :github:`38782` - CONFIG_BT_CTLR_DATA_LENGTH_MAX=250 causes pairing compatibility issues with many devices
* :github:`38769` - mqtt: the size of a mqtt payload is limited
* :github:`38765` - samples: create an OLED example
* :github:`38764` - CBPRINTF_FP_SUPPORT  不 工作 在...之后 NEWLIB_LIBC 启用
* :github:`38761` - Does zephyr_library_property defines -DTRUE in command-line?
* :github:`38756` - Twister: missing testcases with error in report
* :github:`38745` - Bluetooth 当...时 配置 用于 扩展 advertising  不 limit advertisement 包 大小 如果  non-extended avertisement  使用
* :github:`38737` - drivers: syscon: missing implementation
* :github:`38735` - nucleo_wb55rg: Flash space left to M0 binary is not sufficient anymore
* :github:`38731` - test-ci: ptp_clock_test :  test failure on frdm_k64f platform
* :github:`38727` - [RFC] Add hal_gigadevice to support GigaDevice SoC Vendor
* :github:`38716` - modem: HL7800: does not work with IPv6
* :github:`38702` - Coap server not properly removing observers
* :github:`38701` - Observable resource of coap server seems to not support a restart of an observer
* :github:`38700` - Observable resource of coap server seems to not support 2 observers simultaneously
* :github:`38698` - stm32f4_disco: Socket CAN sample not working
* :github:`38697` - The coap_server sample is missing the actual send in the retransmit routine
* :github:`38694` - Disabling NET_CONFIG_AUTO_INIT does not require calling net_config_init() manually in application as mentioned in Zephyr Network Configuration Library documentation
* :github:`38692` - samples/tfm_integration: Compilation fails ("unexpected keyword argument 'rom_fixed'")
* :github:`38691` - MPU fault with mcumgr bluetooth FOTA started whilst existing FOTA is in progress
* :github:`38690` - Wrong initialisation priority on different display drivers (eg. ST7735r) cause exception when using lvgl.
* :github:`38688` - bt_gatt_unsubscribe does not remove subscription from internal list/returning BT_GATT_ITER_STOP causes bt_gatt_subscribe to return -ENOMEM / -12
* :github:`38675` - DTS binding create devicetree_unfixed.h build error at v2.7.0
* :github:`38673` - DNS-SD library does not support ``_services._dns-sd._udp.local`` meta-query for service enumeration
* :github:`38668` -  ESP32‘s I2S
* :github:`38667` - ST LSM6DSO polling mode does not work on nRF52dk_nrf52832
* :github:`38655` - 失败 测试 用于 Regulator API
* :github:`38653` - drivers: modem: gsm_ppp: Add support for Quectel modems
* :github:`38646` - SIMD Rounding bug while running Assembly addps instruction on Zephyr
* :github:`38641` - Arm v8-M '_ns' renaming was applied inconsistently
* :github:`38635` - USDHC driver broken on RT10XX after 387e6a676f86c00d1f9ef018e4b2480e0bcad3c8 commit
* :github:`38622` - subsys/usb: CONFIG_USB_DEVICE_STACK resulted in 10kb increase in firmware size
* :github:`38621` - Drivers: spi: stm32: Transceive lock forever
* :github:`38620` - STM32 uart driver prevent system to go to deep sleep
* :github:`38617` - HL7800 PSM not working as intended
* :github:`38613` - BLE 连接 参数 更新 带 inconsistent 值
* :github:`38612` - 故障 带 assertions 启用 prevents detailed output 因为 的 ISR() assertion 检查 在...中 shell 函数
* :github:`38602` - modem gsm
* :github:`38601` - nucleo_f103rb: samples/posix/eventfd/ failed since "retargetable locking" addition
* :github:`38593` - using RTT console to print along with newlib C library in Zephyr
* :github:`38591` - nucleo_f091rc: Linking issue since "align __data_ram/rom_start/end linker" (65a2de84a9d5c535167951bf1cf610c4f7967ea5)
* :github:`38586` - olimexino_stm32: "no DEVICE_HANDLE_ENDS inserted" builld issue (samples/subsys/usb/audio/headphones_microphone)
* :github:`38581` - tests-ci : kernel: scheduler: multiq test failed
* :github:`38582` - tests-ci : kernel: scheduler:  test failed
* :github:`38578` - STM32L0X ADC hangs
* :github:`38572` - 构建 带 macOS SDK  失败
* :github:`38571` - bug: drivers: ethernet: build as static library breaks frdm_k64f gptp sample application
* :github:`38563` - ISO broadcast cannot send with callback if CONFIG_BT_CONN=n
* :github:`38560` - log v2 with 64-bit integers and threads causes invalid 64-bit value output
* :github:`38559` - shell 日志 backend  挂起 在...上 qemu_x86_64
* :github:`38558` - CMake warning: CMP0079
* :github:`38554` - tests-ci : kernel: scheduler:  test failed
* :github:`38552` - stm32: g0b1: garbage output in log and suspected hard fault when configuring modem
* :github:`38536` - samples: tests: display: Sample for display.ft800 causes end in timeout
* :github:`38535` - 驱动 modem: bg9x: Kconfig 值 编译 进入 ``autoconf.h`` 甚至 如果 它 isn't  使用
* :github:`38534` - lwm2m: 增加 API 到 检查 observation 状态 的 resource/object
* :github:`38532` - samples: audio: tests: Twister fails on samples/drivers/audio/dmic
* :github:`38527` - lwm2m: re-register instead of removing observer on COAP reset answer to notification
* :github:`38520` - Bluetooth:Host:Scan: "bt_le_per_adv_list_add" function doesn't work
* :github:`38519` - stm32: g0b1re: Log/Shell subsys with serial uart buggy after #38432
* :github:`38516` - subsys: net: ip: packet_socket: always returning of NET_CONTINUE caused access to unreferred pkt and causing a crash/segmentation fault
* :github:`38514` - mqtt azure sample failing with net_tcp "is waiting on connect semaphore"
* :github:`38512` - stm32f7: CAN: STM32F645VE CAN signal seems upside down.
* :github:`38500` - tests/kernel/device/kernel.device.pm 失败 到 构建 在...上 TI 平台
* :github:`38498` - net: ipv6: nbr_lock not initialized with CONFIG_NET_IPV6_ND=n
* :github:`38480` - Improve samples documentation
* :github:`38479` - "west 刷写 命令 退出 带 错误
* :github:`38477` - json: JSON Library Orphaned, Request to Become a Maintainer
* :github:`38474` - command exited with status 63: nrfjprog --ids
* :github:`38463` - check_compliance gives very many Kconfig warnings
* :github:`38452` - Some STM32 series require CONFIG_PM_DEVICE if CONFIG_PM=y
* :github:`38442` - test-ci:  twr_ke18f: 所有  驱动 测试 失败 带 BUS 故障
* :github:`38438` - test-ci: test_flash_map:twr_ke18f: test failure
* :github:`38437` - stm32: g0b1re: Serial UART timing issue after MCU entered deep sleep
* :github:`38433` - gpio_pin_set not working on STM32 with CONFIG_PM_DEVICE_RUNTIME
* :github:`38428` - http_client response callback always reports final_data == HTTP_DATA_FINAL
* :github:`38427` - mimxrt1050_evk 和 mimxrt1020_evk 板 失败 到 引导 一些 sample applications
* :github:`38421` - HardFault regression detected on Cortex-M0+ following Cortex-R introduction
* :github:`38418` - twister: Remove toolchain-depandat filter for native_posix
* :github:`38417` - 增加 支持 用于 WeAct-F401CC 板
* :github:`38414` - Build of http client fails if CONFIG_POSIX_API=y
* :github:`38405` - samples/philosophers/sample.kernel.philosopher.stacks fails on xtensa
* :github:`38403` - Cleanup ``No SOURCES given to Zephyr library`` warnings
* :github:`38402` - module: MCUboot module missing fixes available upstream
* :github:`38401` - 构建 失败 due 到  proxy 错误 由 launchpadlibrarian
* :github:`38400` - mec15xxevb_assy6853: arm_ramfunc and arm_sw_vector_relay tests timeout after the build
* :github:`38398` - DT_N_INST error for TMP116 sample
* :github:`38396` - RISC-V privilege SoC initialisation code skips the __reset vector
* :github:`38382` - stm32 uart finishes Tx before going to PM
* :github:`38365` - 驱动 gsm_ppp: gsm_ppp_stop 失败 到 lock tx_sem 在...之后 一些 时间
* :github:`38362` - soc: ti cc13x2-cc26x2: PM standby + radio interaction regression
* :github:`38354` - stm32: stm32f10x JTAG realated gpio repmap didn't works
* :github:`38351` - Custom radio protocol
* :github:`38349` - XCC compilation fails on Intel cAVS platforms
* :github:`38348` - Bluetooth: Switch to inclusive terminology from the 5.3 specification
* :github:`38340` - Bluetooth:DirectionFinding: Disabling the MPU causes some compilation errors
* :github:`38332` - stm32g0: power hooks should be define as weak
* :github:`38323` -  不 生成 代码 coverage report 由 运行 samples/subsys/tracing
* :github:`38316` - Synchronize multiple DF TX devices in the DF Connectionless RX Example "Periodic Advertising list"
* :github:`38309` - ARC context switch to interrupted thread busted with CONFIG_ARC_FIRQ=y and CONFIG_NUM_IRQ_PRIO_LEVELS=1
* :github:`38303` -  当前 BabbleSim 测试 构建 系统 based 在...上 bash 脚本 hides 警告
* :github:`38290` - net_buf_add_mem() hard-faults when adding buffer from external SDRAM
* :github:`38279` - Bluetooth: Controller: assert LL_ASSERT(!radio_is_ready()) in lll_conn.c
* :github:`38277` - SoC stm32h7: 失败 到 引导 带 LDO power supply, 如果 SoC  SMPS 支持
* :github:`38276` - LwM2M: RD Client: Wrong state if registration fails
* :github:`38273` - Support UART4 on STM32F303Xe
* :github:`38272` - "west 刷写 停止 工作
* :github:`38271` - Expose emulator_get_binding function
* :github:`38264` - Modbus over RS485 on samd21g18a re-gpios turning on 1 byte too early
* :github:`38259` - subsys/shell: ``[JJ`` escape codes in logs after disabling colors
* :github:`38258` - newlib: first malloc call may fail on Xtensa depending on image size
* :github:`38246` - samples: drivers: flash_shell: fails on arduino_due due to compilation issue
* :github:`38245` - board: bl654_usb project: samples/basic/blinky does not blink LED
* :github:`38240` - Connected ISO does not disconnect gracefully
* :github:`38237` - [backport v2.6-branch] backport of #37479 failed
* :github:`38235` - Please add stm32h723Xe.dtsi to dts/arm/st/h7/
* :github:`38234` - Newlib retargetable lock init fails on qemu_xtensa
* :github:`38233` - 构建 newlib 函数 读取 和 写入 失败 当...时 启用 userspace
* :github:`38219` - kernel: Z_MEM_SLAB_INITIALIZER MACRO not compatible with C++
* :github:`38216` - nxp_adsp_imx8 失败 到 构建  数量 的 测试
* :github:`38214` - xtensa 构建 失败 在...中 CI due 到 运行 出 的 ram 到 链接
* :github:`38207` - Use of unaligned noinit data hangs qemu_arc_hs
* :github:`38202` - mbedtls and littlefs on a STM32L4
* :github:`38197` - Invalid NULL check for ``iso`` in bt_iso_connected
* :github:`38196` - net nbr 命令  崩溃
* :github:`38191` - Unable to connect multiple MQTT clients
* :github:`38186` - i.MX RT10xx 板 失败 到 初始化 当...时 Ethernet  启用
* :github:`38181` - tests/drivers/uart/uart_basic_api/drivers.uart.cdc_acm 失败 到 构建
* :github:`38177` - LORA Module crashes SHT3XD sensor.
* :github:`38173` - STM32WB: Low power modes entry blocked by C2 when CONFIG_BLE=n
* :github:`38172` - modem_context_sprint_ip_addr returns pointer to stack array
* :github:`38170` - Shell argument in second position containing a question mark is ignored
* :github:`38168` - aarch32: flags value collision between base IRQ layer and GIC interrupt controller driver
* :github:`38162` - Upgrade to 2.6 GPIO device_get_binding("GPIO_0") now returns null
* :github:`38154` - Error building example i2c_fujitsu_fram
* :github:`38153` - Zephyr Native POSIX select() implementation too frequent wakeup on pure timeout based use
* :github:`38145` - [backport v2.6-branch] backport of #37787 failed
* :github:`38144` - [backport v2.6-branch] backport of #37787 failed
* :github:`38141` - Wrong output from printk() with CONFIG_CBPRINTF_NANO=y
* :github:`38138` - [Coverity CID: 239554] Out-of-bounds read in /zephyr/include/generated/syscalls/log_msg2.h (Generated Code)
* :github:`38137` - [Coverity CID: 239555] Unchecked return value in subsys/mgmt/hawkbit/hawkbit.c
* :github:`38136` - [Coverity CID: 239557] Out-of-bounds read in /zephyr/include/generated/syscalls/kernel.h (Generated Code)
* :github:`38135` - [Coverity CID: 239560] Out-of-bounds access in subsys/modbus/modbus_core.c
* :github:`38134` - [Coverity CID: 239563] Logically dead code in subsys/bluetooth/host/id.c
* :github:`38133` - [Coverity CID: 239564] Side effect in assertion in subsys/bluetooth/controller/ll_sw/nordic/lll/lll.c
* :github:`38132` - [Coverity CID: 239565] Unchecked return value in drivers/sensor/adxl372/adxl372_trigger.c
* :github:`38131` - [Coverity CID: 239568] Out-of-bounds access in subsys/modbus/modbus_core.c
* :github:`38130` - [Coverity CID: 239569] Out-of-bounds access in subsys/bluetooth/host/id.c
* :github:`38129` - [Coverity CID: 239572] Out-of-bounds read in /zephyr/include/generated/syscalls/kernel.h (Generated Code)
* :github:`38127` - [Coverity CID: 239579] Logically dead code in drivers/flash/nrf_qspi_nor.c
* :github:`38126` - [Coverity CID: 239581] Out-of-bounds access in subsys/modbus/modbus_core.c
* :github:`38125` - [Coverity CID: 239582] Unchecked return value in drivers/display/ssd1306.c
* :github:`38124` - [Coverity CID: 239583] Side effect in assertion in subsys/bluetooth/controller/ll_sw/nordic/lll/lll.c
* :github:`38123` - [Coverity CID: 239584] Improper use of negative value in subsys/logging/log_msg2.c
* :github:`38122` - [Coverity CID: 239585] Side effect in assertion in subsys/bluetooth/controller/ll_sw/nordic/lll/lll.c
* :github:`38121` - [Coverity CID: 239586] Side effect in assertion in subsys/bluetooth/controller/ll_sw/nordic/lll/lll.c
* :github:`38120` - [Coverity CID: 239588] Unchecked return value in subsys/bluetooth/host/id.c
* :github:`38119` - [Coverity CID: 239592] Dereference before null check in subsys/ipc/rpmsg_multi_instance/rpmsg_multi_instance.c
* :github:`38118` - [Coverity CID: 239597] Explicit null dereferenced in tests/net/context/src/main.c
* :github:`38117` - [Coverity CID: 239598] Unchecked return value in drivers/sensor/adxl362/adxl362_trigger.c
* :github:`38116` - [Coverity CID: 239601] Untrusted loop bound in subsys/bluetooth/host/sdp.c
* :github:`38115` - [Coverity CID: 239605] Logically dead code in drivers/flash/nrf_qspi_nor.c
* :github:`38114` - [Coverity CID: 239607] Missing break in switch in subsys/usb/class/dfu/usb_dfu.c
* :github:`38113` - [Coverity CID: 239609] Out-of-bounds access in subsys/random/rand32_ctr_drbg.c
* :github:`38112` - [Coverity CID: 239612] Out-of-bounds read in /zephyr/include/generated/syscalls/log_ctrl.h (Generated Code)
* :github:`38111` - [Coverity CID: 239615] Out-of-bounds access in subsys/net/lib/sockets/sockets_tls.c
* :github:`38110` - [Coverity CID: 239619] Out-of-bounds access in subsys/net/lib/sockets/sockets_tls.c
* :github:`38109` - [Coverity CID: 239623] Out-of-bounds access in subsys/net/lib/sockets/sockets_tls.c
* :github:`38108` - nxp: usb driver build failure due to d92d1f162af3ba24963f1026fc0a304f1a44d1f3
* :github:`38104` - kheap buffer own section attribute causing memory overflow in ESP32
* :github:`38101` - bt_le_adv_update_data() assertion fail
* :github:`38093` - preempt_cnt 不 复位 在...中 每个 测试 case 在...中 tests/lib/ringbuffer/libraries.data_structures
* :github:`38090` - LPS22HH: int32_t overflow in pressure calculations
* :github:`38082` - Hawkbit (http request) and MQTT can't seem to work together
* :github:`38078` - RT6XX I2S test fails after d92d1f162af3ba24963f1026fc0a304f1a44d1f3
* :github:`38069` - stm32h747i_disco M4 not working following merge of 9fa5437447712eece9c88e728ac05ac10fb01c4a
* :github:`38065` - Bluetooth: Direction 查找 Compiler 警告 当...时 included 在...中 其他 头文件 文件
* :github:`38059` - automount configuration in nrf52840dk_nrf52840.overlay causes error: mount point already exists!! in subsys/fs/littlefs sample
* :github:`38054` - Bluetooth: host: Local Host terminated but send host number of completed Packed
* :github:`38047` - twister: The --board-root parameter doesn't appear to work
* :github:`38046` - twister: The --device-serial only works at 115200 baud
* :github:`38044` - tests: newlib: Scenarios from tests/lib/newlib/thread_safety fail on nrf9160dk_nrf9160_ns
* :github:`38031` - STM32WB - Problem with data reception on LPUART when PM and LPTIM are enabled
* :github:`38026` - 板 bl654_usb:  不 支持 samples/bluetooth/hci_uart
* :github:`38022` - thread: k_float_enable() API can't build on x86_64 platforms, fix that API and macro documentation
* :github:`38019` - nsim_sem_mpu_stack_guard board can't run
* :github:`38017` - [Coverity CID: 237063] Untrusted value as argument in tests/net/lib/coap/src/main.c
* :github:`38016` - [Coverity CID: 238375] Uninitialized pointer read in subsys/bluetooth/mesh/shell.c
* :github:`38015` - [Coverity CID: 237072] Uninitialized pointer read in subsys/bluetooth/controller/ll_sw/ull_adv_aux.c
* :github:`38014` - [Coverity CID: 237071] Unexpected control flow in subsys/bluetooth/host/keys.c
* :github:`38013` - [Coverity CID: 237070] Unchecked return value in subsys/bluetooth/shell/gatt.c
* :github:`38012` - [Coverity CID: 236654] Unchecked return value in subsys/bluetooth/host/gatt.c
* :github:`38011` - [Coverity CID: 236653] Unchecked return value in drivers/sensor/bmi160/bmi160_trigger.c
* :github:`38010` - [Coverity CID: 236652] Unchecked return value in drivers/sensor/fxas21002/fxas21002_trigger.c
* :github:`38009` - [Coverity CID: 236651] Unchecked return value in drivers/sensor/bmg160/bmg160_trigger.c
* :github:`38008` - [Coverity CID: 236650] Unchecked return value in drivers/sensor/fxos8700/fxos8700_trigger.c
* :github:`38007` - [Coverity CID: 236649] Unchecked return value in drivers/sensor/adt7420/adt7420_trigger.c
* :github:`38006` - [Coverity CID: 236648] Unchecked return value in drivers/sensor/sx9500/sx9500_trigger.c
* :github:`38005` - [Coverity CID: 236647] Unchecked return value in drivers/sensor/bmp388/bmp388_trigger.c
* :github:`38004` - [Coverity CID: 238360] Result is not floating-point in drivers/sensor/sgp40/sgp40.c
* :github:`38003` - [Coverity CID: 238343] Result is not floating-point in drivers/sensor/sgp40/sgp40.c
* :github:`38002` - [Coverity CID: 237060] Out-of-bounds access in subsys/bluetooth/host/gatt.c
* :github:`38001` - [Coverity CID: 238371] Negative array index read in tests/lib/cbprintf_package/src/test.inc
* :github:`38000` - [Coverity CID: 238347] Negative array index read in tests/lib/cbprintf_package/src/test.inc
* :github:`37999` - [Coverity CID: 238383] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37998` - [Coverity CID: 238381] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37997` - [Coverity CID: 238380] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37996` - [Coverity CID: 238379] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37995` - [Coverity CID: 238378] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37994` - [Coverity CID: 238377] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37993` - [Coverity CID: 238376] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37992` - [Coverity CID: 238374] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37991` - [Coverity CID: 238373] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37990` - [Coverity CID: 238372] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37989` - [Coverity CID: 238370] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37988` - [Coverity CID: 238369] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37987` - [Coverity CID: 238368] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37986` - [Coverity CID: 238367] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37985` - [Coverity CID: 238366] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37984` - [Coverity CID: 238364] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37983` - [Coverity CID: 238363] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37982` - [Coverity CID: 238362] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37981` - [Coverity CID: 238361] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37980` - [Coverity CID: 238359] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37979` - [Coverity CID: 238358] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37978` - [Coverity CID: 238357] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37977` - [Coverity CID: 238356] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37976` - [Coverity CID: 238355] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37975` - [Coverity CID: 238354] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37974` - [Coverity CID: 238353] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37973` - [Coverity CID: 238352] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37972` - [Coverity CID: 238351] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37971` - [Coverity CID: 238350] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37970` - [Coverity CID: 238349] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37969` - [Coverity CID: 238348] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37968` - [Coverity CID: 238346] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37967` - [Coverity CID: 238345] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37966` - [Coverity CID: 238344] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37965` - [Coverity CID: 238342] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37964` - [Coverity CID: 238341] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37963` - [Coverity CID: 238340] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37962` - [Coverity CID: 238339] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37961` - [Coverity CID: 238337] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37960` - [Coverity CID: 238336] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37959` - [Coverity CID: 238335] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37958` - [Coverity CID: 238334] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37957` - [Coverity CID: 238333] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37956` - [Coverity CID: 238332] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37955` - [Coverity CID: 238331] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37954` - [Coverity CID: 238330] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37953` - [Coverity CID: 238328] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37952` - [Coverity CID: 238327] Logically dead code in tests/bluetooth/tester/src/mesh.c
* :github:`37951` - [Coverity CID: 238365] Logical vs. bitwise operator in drivers/i2s/i2s_nrfx.c
* :github:`37950` - [Coverity CID: 237067] Division or modulo by zero in tests/benchmarks/latency_measure/src/heap_malloc_free.c
* :github:`37949` - [Coverity CID: 238382] Dereference before null check in subsys/bluetooth/mesh/cfg_cli.c
* :github:`37948` - [Coverity CID: 238338] Dereference before null check in subsys/bluetooth/mesh/cfg_cli.c
* :github:`37947` - [Coverity CID: 237069] Dereference before null check in subsys/bluetooth/host/att.c
* :github:`37946` - [Coverity CID: 237066] Calling risky function in tests/lib/c_lib/src/main.c
* :github:`37945` - [Coverity CID: 237064] Calling risky function in tests/lib/c_lib/src/main.c
* :github:`37944` - [Coverity CID: 237062] Calling risky function in tests/lib/c_lib/src/main.c
* :github:`37940` - Unconsistent UART ASYNC API
* :github:`37927` - tests-ci: net-lib: test/net/lib : build missing drivers__net and application has no console output
* :github:`37916` - [Coverity CID :219656] Uninitialized scalar variable in file /tests/kernel/threads/thread_stack/src/main.c
* :github:`37915` - led_pwm driver not generating correct linker symbol
* :github:`37896` - samples: bluetooth: mesh: build failed for native posix
* :github:`37876` - Execution of twister in makefile environment
* :github:`37865` - nRF Battery measurement issue
* :github:`37861` - tests/lib/ringbuffer 失败 在...上 ARC 板
* :github:`37856` - tests: arm: uninitialized FPSCR
* :github:`37852` - RISC-V machine timer time-keeping question
* :github:`37850` - 提供 宏 用于 switching off Zephyr 内核 版本
* :github:`37842` - TCP2 statemachine gets stuck in TCP_FIN_WAIT_2 state
* :github:`37839` - SX1272 LoRa 驱动  损坏 和 失败 到 构建
* :github:`37838` - cmake 3.20 不 支持 尚未 由 最近 Ubuntu
* :github:`37830` - intel_adsp_cavs15: run queue testcases failed on ADSP
* :github:`37827` - stm32h747i_disco M4 not working, if use large size(>1KB) global array
* :github:`37821` - pm: ``pm_device_request`` incorrectly returns errors
* :github:`37797` - Merge vendor-prefixes.txt from all modules with build.settings.dts_root in zephyr/module.yml
* :github:`37790` - Bluetooth: host: Confusion about periodic advertising interval
* :github:`37786` - Example for tca9546a multiplexor driver
* :github:`37784` - MPU6050 accel and gyro values swapped
* :github:`37781` - nucleo_l496zg lpuart1 驱动 不 工作
* :github:`37779` - adc sam0 interrupt mapping, RESRDY maps to second interrupt in samd5x.dtsi
* :github:`37772` - samples: subsys: usb: mass: Use &flash0 storage_partition for USB mass storage
* :github:`37768` - tests/lib/ringbuffer/libraries.data_structures 失败 到 构建 在...上 数量 的 平台 due 到 CONFIG_SYS_CLOCK_TICKS_PER_SEC=100000
* :github:`37765` - cmake: multiple ``No SOURCES given to Zephyr library:`` warnings
* :github:`37746` - qemu_x86_64 fails samples/hello_world/sample.basic.helloworld.uefi in CI
* :github:`37735` - Unsigned types are incorrectly serialized when TLV format is used in LWM2M response
* :github:`37734` - xtensa xcc build spi_nor.c fail
* :github:`37720` - net: dtls: received close_notify alerts are not properly handled by DTLS client sockets
* :github:`37718` - Incompatible (u)intptr_t type and PRIxPTR definitions
* :github:`37709` - x86 PCIe ECAM does not work as expected
* :github:`37701` - stm32:  conflicts with uart serial DMA
* :github:`37696` - Modbus TCP: wrong transaction id in response
* :github:`37694` - Update CMSIS-DSP version to 1.9.0 (CMSIS 5.8.0)
* :github:`37693` - Update CMSIS-Core version to 5.5.0 (CMSIS 5.8.0)
* :github:`37691` - samples/subsys/canbus/isotp/sample.subsys.canbus.isotp 失败 到 构建 在...上 mimxrt1170_evk_cm7
* :github:`37687` - Support MVE on ARMv8.1-M
* :github:`37684` - Add State Machine Framework to Zephyr
* :github:`37676` - tests/kernel/device/kernel.device.pm (and tests/subsys/pm/power_mgmt/subsys.pm.device_pm) fails to build on mec172xevb_assy6906 & mec1501modular_assy6885
* :github:`37675` - tests/kernel/device/kernel.device.pm fails on bt510/bt6x0
* :github:`37672` - 板 qemu_x86  不 longer 工作 带 shell
* :github:`37665` - 文件 系统 错误 类型 用于 ssize_t 在...中 fs.h 用于 CONFIG_ARCH_POSIX
* :github:`37660` - Changing zephyr,console requires a clean build
* :github:`37658` - samples: boards/stm32/backup_sram : needs backup sram enabled in DT to properly display memory region
* :github:`37652` - bluetooth: tests/bluetooth/bsim_bt/bsim_test_advx reported success but still reported failed.
* :github:`37637` - Infinite configuring loop for samples\drivers\led_ws2812 sample
* :github:`37619` - RT6xx TRNG reports error on first request after reset
* :github:`37611` - Bluetooth: host: Implement L2CAP ecred reconfiguration request as initiator
* :github:`37610` - subsys/mgmt/hawkbit: Unable to parse json if the payload is split into 2 packets
* :github:`37600` - Invalidate TLB after ptables swap
* :github:`37597` - samples: bluetooth: scan_adv
* :github:`37586` - get_maintainer.py  损坏
* :github:`37581` - Bluetooth: controller: radio: Change CTE configuration method
* :github:`37579` - PWM: Issue compiling project when CONFIG_PWM and CONFIG_PWM_SAM is used with SAME70
* :github:`37571` - Bluetooth: Extended advertising assertion
* :github:`37556` - Schedule or timeline of LE audio in zephyr
* :github:`37547` - Bluetooth: Direction 查找 通道 index 的 接收 CTE 包  不正确
* :github:`37544` - 更改 划分 名称 使用 .overlay
* :github:`37543` - Using STM32Cube HAL function results in linker error
* :github:`37536` - _pm_devices() skips  非常 第一 设备 在...中  list 和 挂起  不 called.
* :github:`37530` - arc smp build failed with mwdt toolchain.
* :github:`37527` - Replace mqtt-azure example with azure-sdk-for-c
* :github:`37526` - ehl_crb: edac 测试  失败
* :github:`37520` - Is zephyr can run syscall or extrenal program
* :github:`37519` - friend.c:unseg_app_sdu_decrypt causes assert: net_buf_simple_tailfroom(buf) >= len when payload + opcode is 10 or 11 bytes long
* :github:`37515` - 驱动 flash_sam: Random 失败 当...时 写入 大 amount 的 数据 到 刷写
* :github:`37502` - OPENTHREAD_CUSTOM_PARAMETERS  不 seem 到 工作
* :github:`37495` - mcuboot: Booting an image flashed on top of a Hawkbit updated ones results in hard fault
* :github:`37491` - wrong documentation format on DMA peripheral API reference
* :github:`37482` - 'cmd.exe' is not recognized as an internal or external command, operable program or batch file.
* :github:`37475` - twister: wrong test statuses in json report
* :github:`37472` - Corrupted timeout on poll for offloaded sockets
* :github:`37467` - Bluetooth: host: Incorrect advertiser timeout handling when using Limited Discoverable flag
* :github:`37465` - samples/bluetooth/iso_receive fails on nrf5340dk target
* :github:`37462` - Bluetooth: Advertising becomes scannable even if BT_LE_ADV_OPT_FORCE_NAME_IN_AD is set
* :github:`37461` - Schedule of LE audio in zephyr
* :github:`37460` - tests/kernel/sched/schedule_api/kernel.scheduler and tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout failed on nsim_hs_smp board
* :github:`37456` - script: Unaccounted size in ram/rom reports
* :github:`37454` - Sensor driver: sht4x, sgp40, invalid include path
* :github:`37446` - Sensor driver: ST LPS22HH undeclared functions and variables
* :github:`37444` - MSI-X: wrong register referenced in map_msix_table()
* :github:`37441` - Native POSIX Flash Storage Does not Support Multiple Instances
* :github:`37436` - Delayed startup due to printing over not ready console
* :github:`37412` - IQ samples are not correct during the "reference period" of CTE signal
* :github:`37409` - Allow dual controller on usb
* :github:`37406` - ISO disconnect complete event doesn't reach the application
* :github:`37400` - esp32 build
* :github:`37396` - DHCP issue with events not triggering on network with microsoft windows DHCP server
* :github:`37395` - stm32h747i_disco 板 M4 核心 不 工作
* :github:`37391` - Bluetooth: 4 Bits of IQ Samples Are Removed (Direction Finding Based on CTE)
* :github:`37386` - bt_vcs_register() enhancement for setting default volume and step
* :github:`37379` - 驱动 adc 用于 stm32h7 depends 在...上  版本 用于 oversampling
* :github:`37376` - samples/subsys/usb/dfu/sample.usb.dfu fails on teensy41/teensy40
* :github:`37375` - tests/drivers/adc/adc_api/drivers.adc 失败 到 构建 在...上 nucleo_h753zi
* :github:`37371` - logging.log2_api_deferred_64b_timestamp 测试 失败 运行 在...上 几个 qemu 平台
* :github:`37367` - Bluetooth: Host: Support setting long advertising data
* :github:`37365` - STM32 :DTCM: incorrect buffer size utilization
* :github:`37346` - STM32WL LoRa 增加  当前 在...中 "suspend_to_idle" 状态
* :github:`37338` - west flash to teensy 41 fail, use blinky with west build
* :github:`37332` - Increased power consumption for STM32WB55 with enabled PM and Bluetooth
* :github:`37327` - subsys/mgmt/hawkbit: hawkbit 运行  中断  运行 instance
* :github:`37319` - West 0.11.0 fails in Zephyr doc build under other manifest repo & renamed Zephyr fork
* :github:`37309` - ARC: add MPU v6 (and others) support
* :github:`37307` - Use XOSHIRO random number generator on NXP i.MX RT platform
* :github:`37306` - revert commit with bogus commit message
* :github:`37305` - Bluetooth Direction Finding Support of "AoA RX 1us"
* :github:`37304` - k_timer_status_sync can lock forever on qemu_x86_64
* :github:`37303` - tests: drivers: i2s: drivers.i2s.speed scenario fails on nrf platforms
* :github:`37294` - RTT logs not found with default west debug invocation on jlink runner
* :github:`37293` - Native POSIX MAC addresses are not random and are duplicate between multiple instances
* :github:`37272` - subsys/mgmt/hawkbit: Falsely 确定   更新  安装 successfully
* :github:`37270` - stm32l4 System Power Management issue
* :github:`37264` - tests-ci : can: isotp: implemmentation test  report FATAL ERROR when do not connect can loopback test pins
* :github:`37265` - tests-ci : kernel: scheduler: multiq test failed
* :github:`37266` - tests-ci : kernel: memory_protection: userspace test Timeout
* :github:`37267` - tests-ci : kernel: threads: apis test Timeout
* :github:`37263` - lib: timeutil: conversion becomes less accurate as time progresses
* :github:`37260` - STM32WL does not support HSE as RCC source and HSEDiv
* :github:`37258` - symmetric multiprocessing failed in user mode
* :github:`37254` - Run Coverity / Generate GitHub Issues
* :github:`37253` - west 刷写  失败 带 openocd 用于 在...上 macOS
* :github:`37236` - ESP32  不 启动 当...时 CONFIG_ASSERT=y  启用
* :github:`37231` - BME280 faulty measurement after power cycle
* :github:`37228` - Bluetooth SMP does not complete pairing
* :github:`37226` - PM: soc: Leftover in conversion of PM hooks to __weak
* :github:`37225` - subsys/mgmt/hawkbit & sample: Bugs/improvements
* :github:`37222` - k_queue data corruption, override user data after reserved heading word
* :github:`37221` - nRF5340: SPIM4 invalid clock frequency selection
* :github:`37213` - ESP32: can't write to SD card over SPI (CRC error)
* :github:`37207` - drivers: serial: convert uart_altera_jtag_hal to use devicetree
* :github:`37206` - counter: stm32: Missing implementation of set_top_value
* :github:`37205` - openocd: 配置 线程 awareness 由 默认
* :github:`37202` - esp32c3 构建 错误
* :github:`37189` - Bug "Key 'name', 'cmake-ext' and 'kconfig-ext' were not defined" when build a zephyr application
* :github:`37188` - Get an error  of "Illegal load of EXC_RETURN into PC" when print log in IO interrupt callback
* :github:`37182` - cmsis_v1 osSignalWait doesn't clear the signals properly when any signal mask is set
* :github:`37180` - Led driver PCA9633 does nok take chip out from sleep
* :github:`37175` - nucleo-f756zg: rtos aware debugging not working
* :github:`37174` - Zephyr's .git directory is 409 MiB, can it be squashed?
* :github:`37173` - drivers: clock_control: stm32: AHB prescaler usable for almost all stm32 series
* :github:`37170` - LwM2M lwm2m_rd_client_stop() not working when called during bootstrapping/registration
* :github:`37160` - [Moved] Bootloader should provide the version of zephyr, mcuboot and a user defined version to the application
* :github:`37159` - osThreadTerminate does not decrease the instances counter
* :github:`37153` - USB serial number is not unique for STM32 devices
* :github:`37145` - sys: ring_buffer: ring_buf_peek() and ring_buf_size_get()
* :github:`37140` - Twister: Cmake error wrongly counted in the report
* :github:`37135` - 扩展  HWINFO API 到 提供 变量 长度 unique ID
* :github:`37134` - 增加 支持 用于  Raspberry Pi 计算 模块 4
* :github:`37132` - Assert 在...上 启用 套接字 CAN
* :github:`37120` - Documentation 在...上 模块
* :github:`37119` - 测试 内核 测试 hardfault 在...上 nucleo_l073rz
* :github:`37115` - tests/bluetooth/shell 失败 到 构建 在...上  lot 的 平台
* :github:`37109` - Zephyr POSIX layer uses swapping with an interrupt lock held
* :github:`37105` - mcumgr: BUS FAULT when starting dfu with mcumgr CLI
* :github:`37104` - tests-ci : kernel: scheduler: multiq test failed
* :github:`37075` - PlatformIO: i cannot use the Wifi Shield ESP8266 to build the sample wifi project with the Nucleo F429ZI
* :github:`37070` - NXP mcux ADC16 reading 65535
* :github:`37057` - PWM-blinky for Silabs MCU
* :github:`37038` - stm32f4 - DMA tx interrupt doesn't trigger
* :github:`37032` - 记录 API reference 缺失 在...中 时钟 的 zephyr 记录
* :github:`37029` - drivers: sensor: sensor_value_to_double requieres non const sensor_value pointer
* :github:`37028` - ipv6 multicast addresses vanish after iface down/up sequence
* :github:`37024` - 编译 错误 如果 我们 仅 使用 VCS 没有 VOCS 和 AICS
* :github:`37023` - zephyr_prebuilt.elf and zephyr.elf has inconsistent symbol address in RISC-V platform
* :github:`37007` - 问题 带 出 的 tree 驱动
* :github:`37006` - tests: kernel: mem_protect: stack_random: enable qemu_riscv32
* :github:`36998` - TF-M: does not allow PSA Connect to proceed with IRQs locked
* :github:`36990` - Memory misalignment ARM Cortex-M33
* :github:`36971` - ESP32: wifi station sample does not get IP address by DHCP4
* :github:`36967` - Bluetooth: public API to query controller public address
* :github:`36959` - Direction 查找 - CTE 传输 在...中 connectionless 模式  错误 长度
* :github:`36953` - <err> lorawan: MlmeConfirm failed : Tx timeout
* :github:`36948` - Cluttering 的 日志 在...上 USB 控制台 在...中 Zephyr 当...时 CDC shell  启用
* :github:`36947` - Tensorflow: Dedicated tflite-micro repository
* :github:`36929` - Failure to build OpenThread LwM2M client on nrf52840dk
* :github:`36928` - Disconnecting ISO mid-send giver error in hci_num_completed_packets
* :github:`36927` - LWM2M: Writing to Write-Only resource causes notification
* :github:`36926` - samples/boards/nrf/system_off wouldn't compile on Particle Xenon board
* :github:`36924` - embARC Machine Learning Inference Library from Synopsys
* :github:`36917` - Runtime device PM is broken on STM32
* :github:`36909` - shell 日志 命令 崩溃  系统 如果 CONFIG_SHELL_LOG_BACKEND  不 defined
* :github:`36896` - tests: net: select: still failing occasionally due to FUZZ
* :github:`36891` - Significant TCP perfomance regression
* :github:`36889` - string.h / strcasestr() + strtok()
* :github:`36885` - Update ISO API to better support TWS
* :github:`36882` - MCUMGR: fs upload fail for first time file upload
* :github:`36873` - USB AUDIO Byte alignment issues
* :github:`36869` - Direction Finding Connectionless porting to nrf52811
* :github:`36866` - CONFIG_NO_OPTIMIZATIONS=y MPU fault on Zephyr 2.6
* :github:`36865` - k_work_q seems to check uninitialized flag on start
* :github:`36859` - Possible Advertising PDU Corruption if bt_enable called in SYS_INIT function
* :github:`36858` - Static object constructors execute twice on the NATIVE_POSIX target
* :github:`36857` - i2c_samd0.c burst write not compatible with ssd1306.c
* :github:`36851` - FS logging backend assumes littlefs
* :github:`36823` - Build excludes paths to standard C++ headers when using GNUARMEMB toolchain variant
* :github:`36819` - qemu_leon3 samples/subsys/portability/cmsis_rtos_v2 samples failing
* :github:`36814` - 错误 format 类型 用于 uint32_t
* :github:`36811` - Clarify ``Z_`` APIs naming conventions and intended scope
* :github:`36802` - MCUboot doesn't work with encrypted images on external flash
* :github:`36796` - Build failure: samples/net/civetweb/http_server using target stm32h735g_disco
* :github:`36794` - 构建 失败 tests/drivers/adc 使用 stm32l562e_dk
* :github:`36790` - sys: ring_buffer: correct space calculation when tail is less than head
* :github:`36789` - [ESP32] samples blinky / gpio / custom board
* :github:`36783` - drivers: modem: hl7800 gpio init failed with interrupt flags
* :github:`36782` - drivers: serial: nrfx: Enforced pull-ups on RXD and CTS conflict on many custom boards
* :github:`36781` - source_periph incorrectly set in dma_stm32
* :github:`36778` - firmware update using mcumgr displays information for only slot 0 and not slot 1.
* :github:`36770` - doc：Missing description for deadline scheduling
* :github:`36769` - Zephyr assumes Interrupt Line config space register is RW, while ACRN hardwired it to 0.
* :github:`36767` - tests-ci :arch.arm.irq_advanced_features.arm_irq_target_state : test failed
* :github:`36768` - tests-ci :coredump.logging_backend : test failed
* :github:`36765` - [PCI] ACRN sets Interrupt Line config space register to 0 and ReadOnly.
* :github:`36764` - Bluetooth Require paired after disconnected work with iphone
* :github:`36755` - NTP client 故障 模块 当...时 它 失败
* :github:`36748` - Zephyr IP Stack Leaks when using PROMISCUOUS socket along with POSIX sockets based implementation.
* :github:`36747` - 增加 板 支持 用于 STEVAL-STWINKT1B
* :github:`36745` - Zephyr IP Stack Limited to 1514 bytes on the wire - no ICMPs beyond this limit
* :github:`36739` - coap_packet_get_payload() returns  错误 大小
* :github:`36737` - Cortex M23: "swap_helper.S:223: Error: invalid offset, value too big (0x0000009C)"
* :github:`36736` - kernel: SMP global lock (and therefore irq_lock) works incorrectly on SMP platforms
* :github:`36718` - st_ble_sensor sample references wrong attribute
* :github:`36716` - zephyr - ADC - ATSAMD21G18A
* :github:`36713` - nrf5 ieee802154 驱动  不 编译 和 损坏 CI
* :github:`36711` - Enable "template repository" for zephyrproject-rtos/example-application
* :github:`36696` - Json on native_posix_64 board
* :github:`36695` - net: ieee802154: cc13xx_26xx: Sub-GHz RF power saving
* :github:`36692` - Release Notes for 2.6.0 not useful (BLE API changes)
* :github:`36679` - Bluetooth - notifications not sending (bonded, CONFIG_BT_MAX_CONN=4, after disconnection then reconnection)
* :github:`36678` - Zephyr Throws 异常 用于 shell 日志 状态 命令 当...时 Telnet  shell backend 和 日志  UART backend
* :github:`36668` - LittleFS example overwrite falsh memory
* :github:`36667` - logger: Filesystem backend doesn't work except for first time boot
* :github:`36665` - l2cap cids mixed up in request
* :github:`36661` - xtensa xcc does not support "-Warray-bounds"
* :github:`36659` - samples/net/sockets 小 缺陷
* :github:`36655` - twister:  sometimes the twister fails because the error ``configparser.NoSectionError: No section: 'manifest'``
* :github:`36652` - deadlock in pthread implementation on SMP platforms
* :github:`36646` - sample.shell.shell_module.minimal_rtt 失败 到 构建 在...上 mimxrt1170_evk_cm4/mimxrt1170_evk_cm7
* :github:`36644` - Toolchain C++ 头文件   included 当...时 libstdc++  不 选择
* :github:`36631` - Turn on GPIO from DTS
* :github:`36625` - compilation fails while building samples/net/openthread/coprocessor for Arduino nano 33 ble
* :github:`36613` - LoRaWAN - Provide method to register a callback for received data
* :github:`36609` - could not mount fatfs on efm32pg_stk3402a
* :github:`36608` - Unable to compile USB console example with uart_mux
* :github:`36606` - Regression in udp socket performance from zephyr v2.3.0 to v2.6.0
* :github:`36600` - Bluetooth: Peripheral: Bond 问题 当...时 使用 保护 连接
* :github:`36598` - Lora driver TX done wait/synchronous call
* :github:`36593` - Failing IPv6 Ready compliance (RFC 2460)
* :github:`36590` - NVS sector size above 65535 not supported
* :github:`36578` - net: ip: Assertion fails when tcp_send_data() with zero length packet
* :github:`36575` - Modbus RTU Client on ESP32
* :github:`36572` - kernel: Negative mutex lock_count value
* :github:`36570` - 使用  custom role 用于 Kconfig 配置 选项
* :github:`36569` - '.. only:' is not working as expected in documentation
* :github:`36568` - net: lib: sockets: Assertion fails when zsock_close()
* :github:`36565` - ehl_crb: Only boot banner is printed but not the test related details for multiple tests due to PR #36191 is not backported to v2.6.0 release
* :github:`36553` - LoRaWAN Sample: join accept but "Join failed"
* :github:`36552` - Bluetooth v2.6.0 connectable advertising leak/loss
* :github:`36540` - LoRaWAN otaa.app_key belongs to mib_req.Param.AppKey
* :github:`36524` - HSE clock doesn't initialize and blinky doesn't run on custom board when moving from zephyr v2.3.0 to v2.6.0
* :github:`36520` - tests/kernel/timer/timer_api/kernel.timer.tickless 失败 到 构建 在...上 npcx9m6f_evb
* :github:`36500` - espressif: cannot install toolchain on Darwin-arm64
* :github:`36496` - bluetooth: 仅  第一 扩展 Advertising Report 带 数据 状态 "incomplete, 更多 数据 到 come"  issued
* :github:`36495` - dtc 生成 缺失 #address-cells 在...中 中断 provider 警告
* :github:`36486` - LOG2 - self referential macro
* :github:`36467` - runner mdb-hw not work with arc hsdk board
* :github:`36466` - tests/kernel/mem_protect/mem_protect failed with arcmwdt toolchain
* :github:`36465` - samples/compression/lz4 failed with arcmwdt toolchian
* :github:`36462` - [bluetooth stack][limited_discoverable_advertising timeout] Some problems about the lim_adv_timeout
* :github:`36448` - samples: subsys: fs: fat_fs: adafruit_2_8_tft_touch_v2: buildkite compilation failed when no i2c defined
* :github:`36447` - net: socket: socketpair: Poll call resetting all events
* :github:`36435` - RFC: API Change: Mesh: Add return value for opcode callback
* :github:`36427` - test: kernel.common.nano32: zephyr-v2.6.0-286-g46029914a7ac: mimxrt1060_evk: test fails
* :github:`36419` - test-ci: net.ethernet_mgmt: zephyr-v2.6.0-286-g46029914a7ac: frdm_k64f: test fails
* :github:`36418` - test-ci: net.socket.tls: zephyr-v2.6.0-286-g46029914a7ac: frdm_k64f: test fail
* :github:`36417` - tests-ci :coredump.logging_backend : zephyr-v2.6.0-286-g46029914a7ac: lpcxpresso55s28: test failed
* :github:`36416` - tests-ci :arch.arm.irq_advanced_features.arm_irq_target_state : zephyr-v2.6.0-286-g46029914a7ac: lpcxpresso55s28: test failed
* :github:`36414` - ESP32 带 samples/net/wifi gives: net_if: There  不 网络 接口 到 工作 带
* :github:`36412` - Blinky on ESP32: Unsupported board: led0 devicetree alias is not defined"
* :github:`36410` - board: cc1352r_sensortag: add dts entry for hdc2080
* :github:`36408` - ARM_MPU on boards ``stm32_min_dev_*`` without MPU enabled
* :github:`36398` - [Video API] Erroneous function pointer validation
* :github:`36390` - net: ip: Negative TCP unacked_len value
* :github:`36388` - ARM: Architecture Level user guide
* :github:`36382` - segfault when hardware isn't emulated
* :github:`36381` - Bluetooth ASSERTION FAIL [evdone] Zephyr v2.6.0
* :github:`36380` - missing auto-dependency on CONFIG_EMUL
* :github:`36357` - tests: samples: watchdog: sample.subsys.task_wdt fails on nrf platforms
* :github:`36356` - 网络 失败 到 传输 STM32H747DISC0 板 zephyr v2.6.0
* :github:`36351` - nRF: 我们  不 总是 guarantee  SystemInit  inlined
* :github:`36347` - Zephyr Wifi IoT device - whats a good board to start with?
* :github:`36344` - Zephyr 2.6.0 st_ble_sensor sample is broken when compiled for nucleo_wb55rg
* :github:`36339` - samples/subsys/logging/dictionary doesn't build under MS Windows environment
* :github:`36329` - 支持 用于 CC3120 WiFi 模块
* :github:`36324` - add project groups to upsteam west manifest
* :github:`36323` - Don't set TFM_CMAKE_BUILD_TYPE_DEBUG by default on LPC55S69-NS if DEBUG_OPTIMIZATIONS
* :github:`36319` - Help: Asking for Help Tips page gets 404 error
* :github:`36318` - [Coverity CID: 236600] Unused value in drivers/ieee802154/ieee802154_nrf5.c
* :github:`36317` - [Coverity CID: 236599] Unused value in drivers/ieee802154/ieee802154_nrf5.c
* :github:`36316` - [Coverity CID: 236597] Unused value in drivers/ieee802154/ieee802154_nrf5.c
* :github:`36315` - [Coverity CID: 236604] Untrusted value as argument in subsys/net/lib/lwm2m/lwm2m_engine.c
* :github:`36314` - [Coverity CID: 236610] Uninitialized pointer read in subsys/bluetooth/mesh/proxy.c
* :github:`36313` - [Coverity CID: 236602] Unchecked return value in drivers/modem/gsm_ppp.c
* :github:`36312` - [Coverity CID: 236608] Out-of-bounds access in subsys/bluetooth/audio/mics_client.c
* :github:`36311` - [Coverity CID: 236598] Out-of-bounds access in subsys/bluetooth/audio/mics_client.c
* :github:`36310` - [Coverity CID: 236607] Missing break in switch in drivers/ieee802154/ieee802154_nrf5.c
* :github:`36309` - [Coverity CID: 236606] Missing break in switch in drivers/ieee802154/ieee802154_nrf5.c
* :github:`36308` - [Coverity CID: 236601] Missing break in switch in drivers/ieee802154/ieee802154_nrf5.c
* :github:`36307` - [Coverity CID: 236605] Logically dead code in subsys/bluetooth/audio/mics.c
* :github:`36306` - [Coverity CID: 236596] Logically dead code in subsys/bluetooth/audio/mics.c
* :github:`36305` - [Coverity CID: 236595] Logically dead code in samples/drivers/eeprom/src/main.c
* :github:`36304` - [Coverity CID: 236609] Explicit null dereferenced in subsys/bluetooth/audio/mics_client.c
* :github:`36303` - [Coverity CID: 236603] Dereference after null check in subsys/bluetooth/audio/vcs_client.c
* :github:`36301` - soc: cypress: Port Zephyr to Cypress CYW43907
* :github:`36298` - TF-M integration: add a brief user guide
* :github:`36291` - ADC 和 math 库 函数 使用 用于 stm32l496
* :github:`36289` - eswifi gets a deadlock on b_l4s5i_iot01a target
* :github:`36282` - Overwrite 模式 用于 RTT 日志记录
* :github:`36278` - ARM: Cortex-M: SysTick priority  不 初始化 如果  SysTick  不 使用
* :github:`36276` - NULL pointer access in check_used_port()
* :github:`36270` - TF-M: introduce uniformity in Non-Secure target names
* :github:`36267` - net: ieee802154: software address filtering
* :github:`36263` - up_squared: kernel.memory_protection.mem_map.x86_64 failed.
* :github:`36256` - SPI4 & 3 MISO not working on nRF5340
* :github:`36255` - tests/subsys/logging/log_core 失败 在...上 hsdk 板
* :github:`36254` - Zephyr shell subsystem 不 工作 带 ARC 硬件 板
* :github:`36250` - tests/subsys/cpp/cxx - doesn't compile on native_posix when CONFIG_EXCEPTIONS=y
* :github:`36247` - samples: usb: testusb: Problems with using with cdc-acm
* :github:`36242` - Zephyr Upstream + sdk-nrf BLE NUS SHELL LOG/CBPRINTF build problem.
* :github:`36238` - net_if.c: possible mutex deadlock
* :github:`36237` - fs_open returns 0 on existing file with FS_O_CREATE | FS_O_WRITE
* :github:`36197` - BOSSA flashing on Arduino Nano 33 BLE (NRF52840)
* :github:`36185` - CMP0116 related warnings
* :github:`36172` - net: ieee802154: LL src/dst address is lost from received net_pkt (when using 6LO)
* :github:`36163` - nvs 不 longer 支持  使用 的 id=0xffff
* :github:`36131` - Occasionally unable to scan for extended advertisements when connected
* :github:`36117` - toolchain: The added abstraction for llvm, breaks builds with off-tree llvm based toolchains
* :github:`36107` - ehl_crb: Multiple 测试  失败 和 板  不 引导 上
* :github:`36101` - tfm related build rebuild even if nothing changes
* :github:`36100` - pb_gatt buf_send does not call callback
* :github:`36095` - drivers: pwm: sam: compilation failure for sam_v71b_xult
* :github:`36094` - BLE wrong connections intervals on multible connections
* :github:`36093` - Fix dt_compat_enabled_with_label behavior (or usage)
* :github:`36089` - intel_adsp_cavs25: support more than 2 DSP cores
* :github:`36088` - intel_adsp_cavs25: 次 引导 失败 在...中 arch_start_cpu()
* :github:`36084` - Arduino Nano 33 BLE: USB gets disconnected after flashing
* :github:`36078` - coredump.logging_backend: lpcxpresso55s28: test failure assertion fail
* :github:`36077` - net: lib: coap: Impossible to get socket info from incoming packet
* :github:`36075` - 驱动  stm32fd: can2  不 工作
* :github:`36074` - LoRaWAN: sx126x: infinite loop on CRC error
* :github:`36061` - Undefined reference to ``z_priq_rb_lessthan(rbnode*, rbnode*)`` when using k_timer_start in cpp file.
* :github:`36057` - Zephyr shell 控制台 和 日志记录 Targeting 隔离 不同 设备 接口
* :github:`36048` - Cannot establish ISO CIS connection properly after ACL disconnected several times
* :github:`36038` - iotdk: the testcase samples/modules/nanopb can't build
* :github:`36037` - bt_init returning success when Bluetooth initialization does not get finalized.
* :github:`36035` - struct devices should be allocated in ROM, not RAM
* :github:`36033` - Mere warnings slow down incremental documentation build from seconds to minutes
* :github:`36030` - West warnings (and others?) are ignored when building documentation
* :github:`36028` - More Description in Example Documentation
* :github:`36026` - wolfssl / wolfcrypt
* :github:`36022` - Wrong channel index in connectionless IQ samples report
* :github:`36014` - stm32g050: Missing closing parenthesis for soc prototype
* :github:`36013` - arm: qemu: run cmsis-dsp tests on the qemu target with FPU
* :github:`35999` - Unexpected Bluetooth disconnection and removal of bond
* :github:`35992` - stm32f303k8 device tree missing DACs
* :github:`35986` - POSIX: multiple definition of posix_types
* :github:`35983` - [backport v1.14-branch] backport of #35935 failed
* :github:`35978` - ESP32 SPI send data hangup
* :github:`35972` - C++ 异常  不 工作 当...时 构建 带 GNU Arm Embedded
* :github:`35971` - ehl_crb: test_nop  is failing under tests/kernel/common/
* :github:`35970` - up_squared: samples/boards/up_squared/gpio_counter/ is failing
* :github:`35964` - shell_uart hangs when putting UART into PM_LOW_POWER_STATE / PM_DEVICE_STATE_LOW_POWER
* :github:`35962` - 驱动 使用 已弃用 Kconfigs
* :github:`35955` - Bluetooth: Controller: 回归问题 在...中 连接 设置
* :github:`35949` - can: mcan: sjw-data devicetree configuration is not written correctly
* :github:`35945` - SPI4 在...上 nRF5340 不 工作 当...时 使用 k_sleep() 在...中 主
* :github:`35941` - subsys: tracing: sysview: No SEGGER_SYSVIEW.h in path
* :github:`35939` - enc424j600 driver unusable/broken on stm32l552
* :github:`35931` - Bluetooth: controller: Assertion in ull_master.c
* :github:`35930` - nRF Dongle as BLE Central Unstable Connectivity at Long-ish Range
* :github:`35926` - Shell tab-completion with more than two levels of nested dynamic commands fails
* :github:`35916` - drivers: TI cc13xx_cc26xx: build error when PM is enabled (serial, entropy, spi, i2c modules)
* :github:`35908` - 停止 DHCP 带 网络 接口 goes 下 离开 networking 状态 在...中  损坏 状态
* :github:`35897` - Bluetooth: PTS Tester on native posix
* :github:`35890` - Build system ignores explicit ZephyrBuildConfiguration_ROOT variable
* :github:`35880` - PSA tests run indefinitely when CONFIG_TFM_IPC=y
* :github:`35870` - Build failure with gcc 11.x on native_posix
* :github:`35857` - intel_adsp_cavs15: run msgq testcases failed on ADSP
* :github:`35856` - intel_adsp_cavs15: run semaphore testcases failed on ADSP
* :github:`35850` - the sample kernel/metairq_dispatch fails on nucleo_g474re
* :github:`35835` - ADC 支持 用于 STM32l496_disco 板
* :github:`35809` - sample: USB audio samples are not working on STM32
* :github:`35793` - kernel.scheduler.multiq: Failed since #35276 ("cooperative scheduling only" special cases removal)
* :github:`35789` - sockets_tls: receiving data on offloaded socket before handshake causes pollin | pollerr and failed recvfrom (SARA-R4)
* :github:`35721` - Atmel sam0 Async and/or DMA may not work
* :github:`35720` - tests:kernel timer fails on test_sleep_abs with TICKLESS_KERNEL and PM on nucleo_wb55rg
* :github:`35718` - Excessive 错误 消息 从 filesystem 接口
* :github:`35711` - net: sockets: dtls: handshake not reset as it ought to be
* :github:`35707` - AssertionError: zephyr/tests/kernel/common test case is failing with gcc-11 (Yocto)
* :github:`35703` - posix_apis: fails at test_posix_realtime for mimxrt1024_evk
* :github:`35681` - Unable to get output for samples/subsys/logging/logger and samples/philosophers
* :github:`35668` - The channel selection of auxiliary advertisments in extended advertisments
* :github:`35663` - STM32H7: Support memory protection unit(MPU) to enable shared memory
* :github:`35658` - arch.interrupt.arm.irq_vector_table.arm_irq_vector_table: MPU FAULT Halting system for mximxrt685_evk_cm33
* :github:`35656` - arch.interrupt.arm.arm_interrupt: hangs on mimxrt685_evk_cm33
* :github:`35581` - stm32 SPI problems with DMA and INTR set-up
* :github:`35550` - nRF91: DPS310 I2C driver not working
* :github:`35532` - SSL Handshake error with modified http(s) client example
* :github:`35529` - STM32: STM32H7 ADC calibration must be performed on startup
* :github:`35429` - subsys: settings: Encryption
* :github:`35377` - add creg_gpio driver for ARC HSDK board
* :github:`35354` - Adding support for measurement of Ultraviolet(UV) Light.
* :github:`35293` - Sporadic 引导 失败
* :github:`35256` - DOC:  DATA PASSING TABLE MISSING THE OBJECT QUEUES
* :github:`35250` - Twister is not reading the serial line output completely
* :github:`35244` - twister: build failure for native_posix with GNU binutils 2.35
* :github:`35238` - ieee802.15.4 support for stm32wb55
* :github:`35229` - twister log mixing between tests
* :github:`35190` - echo_server sample non-functional rails all CPUs on native_posix_64 board build
* :github:`35055` - STM32L432KC Nucleo Reference board SWD problem after programming with Zephyr
* :github:`34917` - arch.interrupt.arm| arch.interrupt.extra_exception_info: lpcxpresso55s28 series: test failure
* :github:`34913` - ModuleNotFoundError: No module named 'elftools'
* :github:`34879` - mec15xxevb_assy6853: 2 GPIO test failures
* :github:`34855` - FANSTEL BT840X
* :github:`34832` - Coding Guideline - MISRA rule 14.4 not applied properly
* :github:`34829` - Bluetooth: ISO: Don't attempt to remove the ISO data path of a disconnected ISO channel
* :github:`34767` - C++ 支持 在...上 ESP 板
* :github:`34760` - Hawkbit 不 downloading 大 文件
* :github:`34659` - Bluetooth: HCI cmd response timeout
* :github:`34571` - Twister mark successfully passed tests as failed
* :github:`34557` - upgrade fatfs to 0.14b
* :github:`34554` - 设置 FS: Duplicate 查找  extremely 慢 当...时 dealing 带 larger 数量 的 设置 entries
* :github:`34544` - lib: gui: lvgl: buffer overflow bug on misconfiguration
* :github:`34543` - STM32F1 失败 到 编译 带 CONFIG_UART_ASYNC_API
* :github:`34392` - [backport v2.5-branch] backport of #34237 failed
* :github:`34391` - [backport v1.14-branch] backport of #34237 failed
* :github:`34390` - i2s: bitrate is wrongly configured on STM32
* :github:`34372` - CPU Lockups when using own Log Backend
* :github:`34354` - Please investigate adding DMA support to STM32 I2C!
* :github:`34324` - RTT  不 工作 在...上 STM32
* :github:`34315` - BMI270 配置 文件 发送 到 I2C seems 到  不 handling  最后一个 part 的  配置 properly.
* :github:`34305` - Shell [modem send] command causes shell to hang after about 10 seconds, Sara R4 - Particle Boron
* :github:`34282` - HAL Module Request: hal_telink
* :github:`34273` - mqtt_publisher: Unable to connect properly on EC21 modem with bg9x driver
* :github:`34269` - LOG_MODE_MINIMAL BUILD error
* :github:`34268` - Bluetooth: Mesh: Sample is stuck in init process on disco_l475_iot
* :github:`34259` - 问题 运行 代码 带 内存 domain
* :github:`34239` - Call settings_save_one in the system work queue, which will cause real-time performance degradation.
* :github:`34236` - External source code integration request: Raspberry Pi Pico SDK
* :github:`34231` - uzlib (decompression library)
* :github:`34226` - Compile error when building civetweb http_server sample for posix_native
* :github:`34222` - Commit related to null pointer exception detection causing UART issues
* :github:`34218` - Civetweb server crashing when trying to access invalid resource
* :github:`34204` - nvs_write: 坏 记录 return 值
* :github:`34192` - Sensor BME680: Add support for SPI operation
* :github:`34134` - USB  不 工作 如果 bootloader badly 使用  设备 在...之前
* :github:`34131` - TFTP client ignores incoming data packets
* :github:`34121` - Unable to generate pdf according to the documentation steps on windows
* :github:`34105` - Convert tests/kernel/workq to new kwork API
* :github:`34049` - Nordic nrf9160 switching between drivers and peripherals
* :github:`34015` - cfb sample 设备 不 查找 用于 esp32 当...时 SSD1306  启用
* :github:`33994` - kscan_ft5336 doesn't provide proper up/down information when polling, and hogs resources in interrupt mode
* :github:`33960` - Zephyr for Briey SoC
* :github:`33937` - [backport v1.14-branch] backport of #26712 failed
* :github:`33932` - [backport v1.14-branch] backport of #26083 failed
* :github:`33910` - sam_v71_xult -> I2C_1 hang during scanning i2c devices
* :github:`33901` - 测试 中断 irq_enable() 和 irq_disable()  不 工作 带 direct 和 regular 中断 在...上 x86
* :github:`33895` - Device tree: STM32L412 and STM32L422 are missing nodes
* :github:`33883` - [backport v2.5-branch] backport of #33340 failed
* :github:`33876` - Lora sender sample build error for esp32
* :github:`33873` - arm_arch_timer: Too many clock announcements with CONFIG_TICKLESS_KERNEL=n on SMP
* :github:`33862` - [backport v2.5-branch] backport of #33771 failed
* :github:`33753` - LVGL output doesn't match the LVGL TFT simulator for gauge widget
* :github:`33652` - 监视  BLE 连接
* :github:`33573` - JSON_OBJ_DESCR_ARRAY_ARRAY is dangerously broken
* :github:`33554` - Request to add OM13056 board (LPC1500 family or specifically SoC LPC1519) support to Zephyr
* :github:`33544` - ehl_crb: portability.posix.common.posix_realtime failed.
* :github:`33485` - Issue with DMA transfers outside of the Zephyr DMA driver on STM32F767
* :github:`33483` - TIMESLICE and PM interaction and expected behavior
* :github:`33449` - 移除 已弃用 items 在...中 2.7
* :github:`33440` - lsm6dso sensor driver not working on nRF5340
* :github:`33435` - armclang / armlinker
* :github:`33337` - twister: Find and fix all "dead" samples/tests
* :github:`33275` - ehl_crb: samples/subsys/shell/shell_module  不 工作
* :github:`33265` - Power Management Overhaul
* :github:`33192` - LoRaWAN - Application 失败 到 启动 如果 模块  不 powered
* :github:`33113` - 改进 代码 coverage 用于 新 feature 或 代码 更改 在...中 内核
* :github:`33104` - 更新 Zephyr 到 fix 工作 队列 问题
* :github:`33099` - ppp: termination 包 不 发送
* :github:`33052` - [Coverity CID :219624] Untrusted loop bound in subsys/bluetooth/host/sdp.c
* :github:`33041` - [Coverity CID :219645] Untrusted loop bound in subsys/bluetooth/host/sdp.c
* :github:`33016` - spi_nor: CONFIG_SPI_NOR_SFDP_RUNTIME leaves flash in Standby after spi_nor_configure()
* :github:`33015` - spi_nor driver: SPI_NOR_IDLE_IN_DPD breaks SPI_NOR_SFDP_RUNTIME
* :github:`32997` - Improve documentation search experience
* :github:`32990` - FS/littlefs: 它  可能 到 写入 到 已经 删除 文件
* :github:`32984` - West: openocd runner: Don't let debug mode on by default
* :github:`32875` - Benchmarking Zephyr vs. RIOT-OS
* :github:`32836` - Remaining integration failures on intel_adsp_cavs15
* :github:`32822` - Code doesn't compile after changing the PWM pin on example "blinky_pwm" on NRF52
* :github:`32803` - Extend mcux uart drivers to support async API
* :github:`32789` - USB DFU support w/o MPU support
* :github:`32733` - RS-485 support
* :github:`32669` - [Bluetooth] sample code for Periodic Advertising Sync Transfer
* :github:`32603` - acrn_ehl_crb: test case of arch.interrupt.prevent_interruption failed
* :github:`32564` - net_buf reference 计数 不 保护
* :github:`32545` - 它 seems  CONFIG_IMG_MGMT_VERBOSE_ERR  不 工作
* :github:`32531` - get_maintainer.py cannot parse MAINTAINERS.yml
* :github:`32293` - Zephyr 2.6 Release Checklist
* :github:`32289` - USDHC: 失败 在...之后 复位
* :github:`32282` - x86 ACPI images are much too large
* :github:`32261` - 问题 带 CONFIG_STACK_SENTINEL
* :github:`32133` - 当前 atomics  subtly 损坏 在...上 AArch64 due 到 内存 排序
* :github:`32111` - Zephyr build fail with LLVM on Windows
* :github:`32035` - Bluetooth: application notification when MTU updated
* :github:`31993` - Add west extension to parse yml file
* :github:`31985` - riscv: Long execution time when TICKLESS_KERNEL=y
* :github:`31943` - drivers: flash: stm32: harmonization of flash erase implementation across STM32 series
* :github:`31739` - Convert CoAP unit tests to use ztest API
* :github:`31593` - civetweb hangs when there are no free filedescriptors
* :github:`31499` - lwm2m : Add visibility into observer notification success/fail
* :github:`31475` - TCP keepalive
* :github:`31473` - Failed phy request not retried and may prevent DLE procedure during auto-initiation
* :github:`31447` - MQTT idling gets disconnected when using TCP2
* :github:`31290` - dts: arm: st: standardize pwm default property st,prescaler to 0
* :github:`31253` - lis3dh 驱动 支持  confusing
* :github:`31162` - Mapping between existing and new system power management states
* :github:`31107` - libc: minimal: add qsort routine
* :github:`31043` - Infinite loop in modem cmd_handler_process
* :github:`30921` - west 刷写 失败 带  open ocd 错误
* :github:`30861` - drivers: uart: increase timeout precision in uart_rx_enable
* :github:`30635` - cpu_stats: Change from printk to ``LOG_*``
* :github:`30429` - Thread Border Router with NRC/RCP sample and nrf52840dk not starting
* :github:`30367` - TCP2  不 发送 我们的 MSS 到 peer
* :github:`30245` - Bluetooth: controller: event scheduling pipeline preemption by short schedule
* :github:`30244` - Bluetooth: controller: Extended scan window time reservation prevents auxiliary channel reception
* :github:`30243` - Bluetooth: controller: IRK resolution in extended scanning breaks auxiliary PDU reception
* :github:`30236` - Main thread sometimes looping forever before user application is reached when using UDP and IPv6 on Nucleo F767ZI
* :github:`30209` - TCP2 : How to add MSS option on sending [SYN, ACK] to client?
* :github:`30066` - CI test build with RAM overflow
* :github:`30026` -  不 创建 multiple BLE IPSP 连接 到  相同 host
* :github:`29545` - samples: tfm_integration: tfm_ipc: No module named 'cryptography.hazmat.primitives.asymmetric.ed25519'
* :github:`29535` - riscv: stack objects are mis-aligned
* :github:`29520` - 创建 k_current_get() 工作 没有  系统 call
* :github:`29397` - 构建 所有 测试 的 模块 mcuboot
* :github:`28872` - Support ESP32 as Bluetooth controller
* :github:`28819` - memory order and consistency promises for Zephyr atomic API?
* :github:`28729` - ARM: Core Stack Improvements/Bug fixes for 2.6 release
* :github:`28716` - 2.5 Release Checklist
* :github:`28312` - Add option to enable ART Accelerator on STM32 FLASH controller
* :github:`27992` - stm32f7: usb: Bursting HID Get and Set report requests leads to unresponding Control endpoint.
* :github:`27525` - Including STM32Cube's USB PD support to Zephyr
* :github:`27415` - 决定 如果 我们 保持  single 线程 支持 (CONFIG_MULTITHREADING=n) 在...中 Zephyr
* :github:`27176` - [v1.14] Restore socket descriptor permission management
* :github:`27015` - Add custom transport support for MQTT
* :github:`26981` - Problem with PPP + GSM MUX with SIMCOM7600E
* :github:`26585` - IPv4 multicast datagrams can't be received for mimxrt1064_evk board (missing ethernet API)
* :github:`26256` - NRF51822 BLE Micro module: hangs on k_msleep() (RTC counter not working)
* :github:`26136` - CMake Error in Windows Environment
* :github:`26051` - shell: uart: Allow a change in the shell initalisation to let routing it through USB UART
* :github:`25832` - [test][kernel][lpcxpresso55s69_ns] kernel cases meet ESF could not be retrieved successfully
* :github:`25182` - Raspberry Pi 4B Support
* :github:`25015` - Bluetooth Isochronous Channels Support
* :github:`24854` - docs: 使用 third-party 库 不 well 记录 在...中 内存 划分 docs
* :github:`24733` - Misconfigured environment
* :github:`24200` - USB GET_INTERFACE response always 0, even when an alternate setting is used
* :github:`24051` - double to sensor_val
* :github:`23745` - 对齐 PS/2 handlers 带  handlers 查找 在...中 其他 驱动
* :github:`23723` - Poor sinf/cosf performance compared to the Segger math libraries
* :github:`23349` - Question: 如何 到 增加 external SoC 板 DTS, 驱动 和 libs?
* :github:`22731` - Improve docker CI documentation
* :github:`22705` - 实现 counter 驱动 用于 lpcxpresso55s69
* :github:`22702` - 实现 I2S 驱动 用于 lpcxpresso55s69
* :github:`22455` - How to assign USB endpoint address manually in stm32f4_disco for CDC ACM class driver
* :github:`22210` - Bluetooth -  bt_gatt_get_value_attr_by_uuid
* :github:`22131` - ARM Cortex_R: CONFIG_USERSPACE: external interrupts are disabled during system calls
* :github:`21869` - IPv6 neighbors get added too eagerly
* :github:`21648` - 改进 documentation 在...上 meta-IRQ 线程
* :github:`21519` - RFC: libc: thread-safe newlib
* :github:`21339` - Expired IPv6 router causes an infinite loop
* :github:`21293` - 增加 timeout  I2C read/write 函数 用于  stm32 移植
* :github:`21205` - get_device_list only available if power management invoked
* :github:`21167` - libraries.libc.newlib 测试 失败
* :github:`20576` - DTS overlay files must include full path name
* :github:`20409` - USB: Create webusb shell
* :github:`20236` - usb: api: Cleanup of current inclusion path for USB
* :github:`20171` - support external spi nor flash on mimxrt1060-evk
* :github:`19882` - 增加 支持 用于 multiple 通道 sampling 到 STM32 ADC 驱动
* :github:`19328` - Logger could block in thread at certain log message pool usage
* :github:`18960` - [Coverity CID :203908]Error handling issues in /lib/libc/newlib/libc-hooks.c
* :github:`18896` - Concurrent Multi-Protocol Support NRF52840
* :github:`18850` - Bluetooth: controller: Advertiser following directed advertiser will have corrupt data
* :github:`18386` - [Coverity CID :203443]Memory - corruptions in /subsys/bluetooth/host/rfcomm.c
* :github:`18351` - logging: 32 bit float values don't work.
* :github:`18316` - Support for unregistering bt_conn callbacks
* :github:`18042` - Only corporate members can join the slack channel
* :github:`17748` - stm32: clock-control: Remove usage of SystemCoreClock
* :github:`17692` - Proper way for joining a multicast group (NRF52840/OpenThread)
* :github:`17375` - Add VREF, TEMPSENSOR, VBAT internal channels to the stm32 adc driver
* :github:`17021` - revise concurrency control in kernel/userspace.c
* :github:`16761` - nrf52840 usb driver with openthread
* :github:`16671` - ideas 用于 未来 的  设置
* :github:`16231` - 增加 CONFIG_UART_DYNAMIC_SETTINGS 选项
* :github:`15841` - Support AT86RF233
* :github:`15793` - Unable to load binaries into iotdk
* :github:`15676` - Support instrumentation for time spent in various power states
* :github:`15555` - Counter Docs Missing Callback Context Note
* :github:`14308` - Better integration between system and device power modes.
* :github:`12405` - add test to catch issues fixed in PR  #12384
* :github:`11773` - Add Bluetooth support for Silicon Labs EFR32MG12
* :github:`11702` - 增加 支持 用于 nrfx i2s 驱动
* :github:`11519` - 增加 在 最少 构建 测试 用于 cc1200
* :github:`11193` - ARM V8M Trusted Execution Environments and Zephyr
* :github:`11028` - CONFIG_LOAPIC_SPURIOUS_VECTOR 不  测试
* :github:`11000` - USB 2.0 high-speed support in Zephyr
* :github:`10930` - Extending string formatting function
* :github:`10676` - Feature Required: DFU over Thread network
* :github:`10378` - watchdog: Limitation with the current watchdog API for Nordic devices
* :github:`10324` - 发布 PDF 带  发布 doc 构建
* :github:`10198` - Add support for FRDM-STBC-AGM01 sensor shield
* :github:`8876` - Adapt net/l2/ieee802154 subsystem to new shell subsystem
* :github:`8275` - when zephyr can support popular IDE develop?
* :github:`7001` - ST Sensors: Driver factorization
* :github:`6777` - Add copyright handling to contributing doc
* :github:`6657` - Question:  Bluetooth avrcp 支持 在...中 Zephyr? 或 任何 计划
* :github:`6493` - need APIs for ranged random number generation
* :github:`6450` - 几个 设备 的 相同 类型 在...上 相同 bus - 如何 到 地址
* :github:`6117` - Make sanitycheck aware of DTS and HW support
* :github:`4911` - Filesystem support for qemu
* :github:`1392` - No module named 'elftools'
* :github:`3886` - Add mutual authentication to net/crypto examples
* :github:`3885` - Add real entropy to crypto-based net samples
* :github:`3884` - Improve the TLS and DTLS examples to use best practices on security
* :github:`3879` - k_thread_abort vs k_thread->fn_abort()
* :github:`3677` - Implement HCI Zephyr extensions
* :github:`3199` - xtensa: simplify linker scripts
* :github:`2811` - Investigate having timeout code track tick deadlines instead of deltas
* :github:`2619` - Define APIs for hashing/ Message Authentication
* :github:`2248` - Split LE Controller: style fixes
