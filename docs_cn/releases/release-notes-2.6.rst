:orphan:

.. _zephyr_2.6:

Zephyr 2.6.0
############

我们很高兴地宣布 Zephyr RTOS 版本 2.6.0 的发布。

本次发布的主要增强功能包括：

* 日志子系统全面重构
* 新增 64 位 ARCv3 支持
* 拆分 ARM32 和 ARM64，ARM64 现在是顶层架构
* 新增 Arm v8.1-m 和 Cortex-M55 的初步支持
* 移除在 2.4 中已弃用的遗留 TCP 协议栈支持
* 跟踪子系统全面重构，包括跟踪点的扩展以及对 Percepio Tracealyzer 的新增支持
* 设备运行时电源管理（PM），即原来的 IDLE 运行时，已完全重构
* 新增一个独立的 Zephyr 应用示例，位于其自身的 Git 仓库中：
  https://github.com/zephyrproject-rtos/example-application

以下各节按组件提供详细的变更列表。

安全漏洞相关
******************************

本次发布解决了以下 CVE：

更详细的信息可参见：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2021-3581：截至 2021-09-04 处于保密期

已知问题
************

您可以使用 GitHub 接口列出所有带有 `bug 标签
<https://github.com/zephyrproject-rtos/zephyr/issues?q=is%3Aissue+is%3Aopen+label%3Abug>`_
的 issue，从而检查所有当前已知的问题。

API 变更
***********

* 驱动 API 现在在可选函数未实现时返回 ``-ENOSYS``。
  如果硬件不支持该功能，则返回 ``-ENOTSUP``。
  此前两种失败模式均返回 ``-ENOTSUP``，这意味着此变更
  可能需要修改仅测试该值的现有代码。

* :c:func:`wait_for_usb_dfu` 函数现在接受 ``k_timeout_t`` 参数，
  而不再使用 ``CONFIG_USB_DFU_WAIT_DELAY_MS`` 宏。

* 在 :c:struct:`bt_iso_chan_ops` 的 :c:func:`disconnected` 回调中新增了断开连接原因。

* 对齐 :c:func:bt_l2cap_chan_send 和
  :c:func:`bt_iso_chan_send` 的错误处理，使得发生错误时缓冲区不再解除引用。

* 在 LwM2M 库 API 中新增了 :c:func:`lwm2m_engine_delete_obj_inst` 函数。

本次发布中弃用

* :c:macro:`DT_CLOCKS_LABEL_BY_IDX`、:c:macro:`DT_CLOCKS_LABEL_BY_NAME`、
  :c:macro:`DT_CLOCKS_LABEL`、:c:macro:`DT_INST_CLOCKS_LABEL_BY_IDX`、
  :c:macro:`DT_INST_CLOCKS_LABEL_BY_NAME` 以及
  :c:macro:`DT_INST_CLOCKS_LABEL` 已弃用，建议改用
  :c:macro:`DT_CLOCKS_CTLR` 及其变体。

* :c:macro:`DT_PWMS_LABEL_BY_IDX`、:c:macro:`DT_PWMS_LABEL_BY_NAME`、
  :c:macro:`DT_PWMS_LABEL`、:c:macro:`DT_INST_PWMS_LABEL_BY_IDX`、
  :c:macro:`DT_INST_PWMS_LABEL_BY_NAME` 以及
  :c:macro:`DT_INST_PWMS_LABEL` 已弃用，建议改用
  :c:macro:`DT_PWMS_CTLR` 及其变体。

* :c:macro:`DT_IO_CHANNELS_LABEL_BY_IDX`、
  :c:macro:`DT_IO_CHANNELS_LABEL_BY_NAME`、
  :c:macro:`DT_IO_CHANNELS_LABEL`、
  :c:macro:`DT_INST_IO_CHANNELS_LABEL_BY_IDX`、
  :c:macro:`DT_INST_IO_CHANNELS_LABEL_BY_NAME` 以及
  :c:macro:`DT_INST_IO_CHANNELS_LABEL` 已弃用，建议改用
  :c:macro:`DT_IO_CHANNELS_CTLR` 及其变体。

* :c:macro:`DT_DMAS_LABEL_BY_IDX`、
  :c:macro:`DT_DMAS_LABEL_BY_NAME`、
  :c:macro:`DT_INST_DMAS_LABEL_BY_IDX` 以及
  :c:macro:`DT_INST_DMAS_LABEL_BY_NAME` 已弃用，建议改用
  :c:macro:`DT_DMAS_CTLR` 及其变体。

* ``<include/usb/class/usb_hid.h>`` 中的 USB HID 专用宏已弃用，
  建议改用 ``<include/usb/class/hid.h>`` 中定义的新通用 HID 宏。

* USB HID Kconfig 选项 USB_HID_PROTOCOL_CODE 已弃用。
  USB_HID_PROTOCOL_CODE 不允许为特定 HID 设备设置引导协议代码。
  可以改用 USB HID API 函数 usb_hid_set_proto_code()。

* USB HID 类 API 通过移除 get_protocol/set_protocol 和
  get_idle/set_idle 回调进行了更改。这些回调是冗余的，或者
  不提供任何附加价值，并导致了 HID 类 API 的错误使用。

* ``CONFIG_OPENOCD_SUPPORT`` Kconfig 选项已弃用，建议改用
  ``CONFIG_DEBUG_THREAD_INFO``。

* 磁盘 API 头文件 ``<include/disk/disk_access.h>`` 已弃用，
  建议改用 ``<include/storage/disk_access.h>``。

* :c:func:`flash_write_protection_set()`。

* ``CONFIG_NET_CONTEXT_TIMESTAMP`` 已被移除，因为它只能与发送的数据一起工作。
  相同的功能可以通过设置 ``CONFIG_NET_PKT_RXTIME_STATS`` 和
  ``CONFIG_NET_PKT_TXTIME_STATS`` 选项来实现。
  这些选项还能够更精确地计算 RX 和 TX 时间。
  这意味着对 SO_TIMESTAMPING 套接字选项的支持也已被移除，
  因为它被已移除的配置选项所使用。

* 设备电源管理（PM）API 和数据结构已从 ``device_pm_*`` 重命名为
  ``pm_device_*``，因为它们不是设备 API，而是 PM 子系统 API。
  枚举和定义也适用同样的规则，它们现在遵循 ``PM_DEVICE_*`` 约定。
  其他一些 API 调用，如 ``device_set_power_state`` 和
  ``device_get_power_state``，已重命名为 ``pm_device_state_set`` 和
  ``pm_device_state_get``，以与其他设备 PM API 的命名保持一致。

* 运行时设备电源管理（PM）API 现在默认是同步的，
  异步 API 带有 **_async** 后缀。此变更使 API 与 Zephyr 中使用的约定保持一致。
  受影响的 API 是 ``pm_device_put`` 和 ``pm_device_get``。

* 以下与内核工作队列 API 相关的函数、宏和结构体：

  * :c:func:`k_work_pending()` 替换为 :c:func:`k_work_is_pending()`
  * :c:func:`k_work_q_start()` 替换为 :c:func:`k_work_queue_start()`
  * :c:struct:`k_delayed_work` 替换为 :c:struct:`k_work_delayable`
  * :c:func:`k_delayed_work_init()` 替换为
    :c:func:`k_work_init_delayable`
  * :c:func:`k_delayed_work_submit_to_queue()` 替换为
    :c:func:`k_work_schedule_for_queue()` 或
    :c:func:`k_work_reschedule_for_queue()`
  * :c:func:`k_delayed_work_submit()` 替换为 :c:func:`k_work_schedule()`
    或 :c:func:`k_work_reschedule()`
  * :c:func:`k_delayed_work_pending()` 替换为
    :c:func:`k_work_delayable_is_pending()`
  * :c:func:`k_delayed_work_cancel()` 替换为
    :c:func:`k_work_cancel_delayable()`
  * :c:func:`k_delayed_work_remaining_get()` 替换为
    :c:func:`k_work_delayable_remaining_get()`
  * :c:func:`k_delayed_work_expires_ticks()` 替换为
    :c:func:`k_work_delayable_expires_get()`
  * :c:func:`k_delayed_work_remaining_ticks()` 替换为
    :c:func:`k_work_delayable_remaining_get()`
  * :c:macro:`K_DELAYED_WORK_DEFINE` 替换为
    :c:macro:`K_WORK_DELAYABLE_DEFINE`

==========================

本次发布中移除的 API

* 移除对旧版 zephyr 整数 typedef（u8_t、u16_t 等）的支持。

* 移除对 k_mem_domain_destroy 和 k_mem_domain_remove_thread 的支持

* 移除对 counter_read 和 counter_get_max_relative_alarm 的支持

* 移除对 device_list_get 的支持

============================

本次发布中的稳定 API 变更
==================================

内核
******

* 新增 :c:func:`k_mem_unmap()`，使得通过 :c:func:`k_mem_map()` 映射的匿名内存
  可以解除映射并回收虚拟地址。

* 新增收集更多按需分页统计信息的能力，包括驱逐算法和后备存储的执行时间直方图。

架构
*************

* ARC

  * 新增 ARCv3 64 位 ISA 支持和相应的 HS6x 处理器支持
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

* CoAP：

  * 修复 coap_find_options() 在选项为空时返回 0。

* DHCPv4：

  * 修复了 DHCPv4 对网络事件管理选项的依赖。

* DNS：

  * 为 DNS 库新增锁以防止并发访问。
  * 在 DNS 中重新调度查询超时处理程序时新增 10ms 延迟。

* 以太网：

  * 修复了以太网驱动中的各种问题。

* IPv4：

  * 修复了 IPv4 地址配置中的各种问题。

* IPv6：

  * 修复了 IPv6 地址配置中的各种问题。

* LwM2M：

  * 新增对 LwM2M 对象的支持。

* MGMT：

  * 新增对 MGMT 命令的支持。

* 套接字：

  * 修复了套接字 API 中的各种问题。

* 跟踪：

  * 修复了跟踪中的各种问题。

构建基础设施
**************

* 新增对 CMake 3.21 的支持。

* 新增对 Ninja 1.10 的支持。

* 新增对 Python 3.10 的支持。

* 新增对 west 0.13 的支持。

Kconfig
**********

* 新增 ``CONFIG_PM_DEVICE`` 选项，用于启用设备电源管理。

* 新增 ``CONFIG_PM_DEVICE_RUNTIME`` 选项，用于启用设备运行时电源管理。

库
***

* 新增对 zvfs 文件系统的支持。

* 新增对 LittleFS 文件系统的支持。

HAL
***

* 新增对 Nordic nRF53 系列 HAL 的支持。

* 新增对 NXP MCUX 系列 HAL 的支持。

MCUBoot
*******

* 新增对 MCUBoot 1.7.0 的支持。

Trusted-Firmware-M
******************

* 新增对 Trusted-Firmware-M 2.0 的支持。

文档
****

* 新增对 Zephyr 文档的更新。

测试与示例
**********

* 为每个 ztest 测试用例提供测试执行时间。

* 新增并完善了一些测试用例，其中大部分是负面测试用例，
  以提高测试代码覆盖率：

   * x86 的常规/直接中断和从 ISR 卸载任务的测试用例。
   * SMP 的测试用例，并为现有的信号量、条件变量等测试启用了 SMP。
   * 内存保护、用户空间和内存堆的测试用例。
   * 数据结构（包括栈、队列、环形缓冲区和 rbtree）的测试用例。
   * IPC（包括管道、轮询、邮箱、消息队列）的测试用例。
   * 同步（包括互斥锁、信号量、原子操作）的测试用例。
   * 调度和线程的测试用例。
   * arch_nop() 和 errno 的测试用例。
   * libc 和 posix API 的测试用例。
   * 日志和传感器子系统的测试用例。

Issue 相关条目
*******************
These GitHub issues were addressed since the previous 2.5.0 tagged
release:

* :github:`35962` - 驱动 使用 已弃用 Kconfigs
* :github:`35955` - Bluetooth: Controller: 回归问题 在...中 连接 设置
* :github:`35949` - can: mcan: sjw-data devicetree configuration is not written correctly
* :github:`35941` - subsys: tracing: sysview: No SEGGER_SYSVIEW.h in path
* :github:`35926` - Shell tab-completion with more than two levels of nested dynamic commands fails
* :github:`35924` - Help with Configuring Custom GPIO Pins
* :github:`35916` - drivers: TI cc13xx_cc26xx: build error when PM is enabled (serial, entropy, spi, i2c modules)
* :github:`35911` - shield sample sensorhub does not produce and meaningful data
* :github:`35910` - LIS2MDL reporting wrong temperature
* :github:`35896` - frdm_k64f: 构建 失败 缺失 dt-bindings/clock/kinetis_sim.h: 不 such 文件 或 directory
* :github:`35890` - Build system ignores explicit ZephyrBuildConfiguration_ROOT variable
* :github:`35882` - Fixed width documentation makes DT bindings docs unreadable
* :github:`35876` - Bluetooth: host: CCC store not correctly handled for multiple connections
* :github:`35871` - LPS22HH sensor reporting wrong pressure data
* :github:`35840` - Bluetooth: host: L2CAP enhanced connection request conformance test issues
* :github:`35838` - Bluetooth: ISO: BIG termination doesn't fully unref the connection
* :github:`35826` - LORAWAN Compatibility with nrf52832 and sx1262
* :github:`35813` - Zephyr Native Posix Build Uses Linux Build Machine Headers out of Sandbox
* :github:`35812` - ESP32 Factory app partition is not bootable
* :github:`35781` - Missing response parameter for HCI_LE_Set_Connectionless_IQ_Sampling_Enable HCI command
* :github:`35772` - 支持 C++ 异常 在...上 NIOS2
* :github:`35764` - 测试 内核 线程 不 multithreading: 失败 带 CONFIG_STACK_SENTINEL=y
* :github:`35762` - SAMPLES: shell_module gives no console output on qemu_leon3
* :github:`35756` - ESP32 Ethernet Support
* :github:`35737` - 驱动  mcan: sjw 不 初始化 当...时 CAN_FD_MODE  启用
* :github:`35714` - samples: subsys: testusb: I want to know how to test in window10.
* :github:`35713` - tests: kernel.scheduler.multiq: test_k_thread_suspend_init_null failure
* :github:`35694` - No console output from NIOS2 Max10
* :github:`35693` - gpio_mcux_lpc.c uses devicetree instance numbers incorrectly
* :github:`35686` - Bluetooth: Crash in bt_gatt_dm_attr_chrc_val when BLE device is disconnected during discovery process
* :github:`35681` - Unable to get ouput for samples/subsys/logging/logger and samples/philosophers
* :github:`35677` - samples/subsys/console/getchar and samples/subsys/console/getline build breaks for arduino_nano_33_ble
* :github:`35655` - Arm64: Assertion failed when CONFIG_MP_CPUS >= 3.
* :github:`35653` - ARC MWDT toolchain put 启动 和 复位 在 不同 地址
* :github:`35633` - 出 的 bound 读取 Multiple Coverity sightings 在...中 生成 代码
* :github:`35631` - [Coverity CID: 205610] Out-of-bounds read in /zephyr/include/generated/syscalls/kernel.h (Generated Code)
* :github:`35630` - [Coverity CID: 205657] Out-of-bounds read in /zephyr/include/generated/syscalls/sample_driver.h (Generated Code)
* :github:`35629` - [Coverity CID: 207968] Out-of-bounds read in /zephyr/include/generated/syscalls/counter.h (Generated Code)
* :github:`35628` - [Coverity CID: 207976] Out-of-bounds read in /zephyr/include/generated/syscalls/counter.h (Generated Code)
* :github:`35627` - [Coverity CID: 208195] Out-of-bounds read in /zephyr/include/generated/syscalls/gpio.h (Generated Code)
* :github:`35626` - [Coverity CID: 210588] Out-of-bounds read in /zephyr/include/generated/syscalls/dac.h (Generated Code)
* :github:`35625` - [Coverity CID: 211042] Out-of-bounds read in /zephyr/include/generated/syscalls/socket.h (Generated Code)
* :github:`35624` - [Coverity CID: 214226] Out-of-bounds read in /zephyr/include/generated/syscalls/uart.h (Generated Code)
* :github:`35623` - [Coverity CID: 215223] Out-of-bounds read in /zephyr/include/generated/syscalls/net_ip.h (Generated Code)
* :github:`35622` - [Coverity CID: 215238] Out-of-bounds read in /zephyr/include/generated/syscalls/net_ip.h (Generated Code)
* :github:`35621` - [Coverity CID: 219477] Out-of-bounds read in /zephyr/include/generated/syscalls/pwm.h (Generated Code)
* :github:`35620` - [Coverity CID: 219482] Out-of-bounds read in /zephyr/include/generated/syscalls/pwm.h (Generated Code)
* :github:`35619` - [Coverity CID: 219496] Out-of-bounds read in /zephyr/include/generated/syscalls/ztest_error_hook.h (Generated Code)
* :github:`35618` - [Coverity CID: 219506] Out-of-bounds read in /zephyr/include/generated/syscalls/log_ctrl.h (Generated Code)
* :github:`35617` - [Coverity CID: 219568] Out-of-bounds read in /zephyr/include/generated/syscalls/net_if.h (Generated Code)
* :github:`35616` - [Coverity CID: 219586] Out-of-bounds read in /zephyr/include/generated/syscalls/net_if.h (Generated Code)
* :github:`35615` - [Coverity CID: 219648] Uninitialized scalar variable in /zephyr/include/generated/syscalls/test_syscalls.h (Generated Code)
* :github:`35614` - [Coverity CID: 219725] Out-of-bounds read in /zephyr/include/generated/syscalls/kernel.h (Generated Code)
* :github:`35613` - [Coverity CID: 225900] Out-of-bounds access in tests/net/lib/dns_addremove/src/main.c
* :github:`35612` - [Coverity CID: 229325] Out-of-bounds read in /zephyr/include/generated/syscalls/log_msg2.h (Generated Code)
* :github:`35611` - [Coverity CID: 230223] Out-of-bounds read in /zephyr/include/generated/syscalls/log_msg2.h (Generated Code)
* :github:`35610` - [Coverity CID: 232755] Out-of-bounds read in /zephyr/include/generated/syscalls/log_ctrl.h (Generated Code)
* :github:`35609` - [Coverity CID: 235917] Out-of-bounds read in /zephyr/include/generated/syscalls/log_msg2.h (Generated Code)
* :github:`35608` - [Coverity CID: 235923] Out-of-bounds read in /zephyr/include/generated/syscalls/log_msg2.h (Generated Code)
* :github:`35607` - [Coverity CID: 235933] Out-of-bounds read in /zephyr/include/generated/syscalls/gpio.h (Generated Code)
* :github:`35606` - [Coverity CID: 235951] Out-of-bounds read in /zephyr/include/generated/syscalls/log_ctrl.h (Generated Code)
* :github:`35605` - [Coverity CID: 236005] Out-of-bounds read in /zephyr/include/generated/syscalls/log_ctrl.h (Generated Code)
* :github:`35604` - [Coverity CID: 236129] Unused value in drivers/adc/adc_lmp90xxx.c
* :github:`35603` - [Coverity CID: 236130] Wrong sizeof argument in drivers/adc/adc_lmp90xxx.c
* :github:`35596` - Bluetooth: Cannot connect if extended advertising is enabled in ``prj.conf``
* :github:`35586` - Timer based example on docu using nrf52-dk compile error.
* :github:`35580` - 故障 当...时 日志记录
* :github:`35569` - tests/lib/mem_alloc failed with arcmwdt toolchain
* :github:`35567` - some mwdt compiler options can't be recognized by zephyr_cc_option
* :github:`35561` - Issue with fat_fs example on nucleo_f767zi
* :github:`35553` - all menuconfig interfaces contain sound open firmware/SOF text
* :github:`35543` - samples: subsys: display: lvgl: is run on nucleo_f429zi and nucleo_f746zg but should be skipped
* :github:`35541` - sockets_tls: when using dtls with sara-r4 modem, handshake hangs if no reply
* :github:`35540` - tests: ztest: error_hook: fails on nucleo_g071rb and nucleo_l073rz
* :github:`35539` - 测试 驱动 spi: spi_loopback: 测试 失败 自...以来 #34731  merged
* :github:`35524` - tests: samples: led: LED PWM sample fails on nrf platforms
* :github:`35522` - doc: Current section is not shown in the side pane nor the page top cookie
* :github:`35512` - OpenThread can't find TRNG driver on nRF5340
* :github:`35509` - 测试 定时器 Unstable 测试 使用 定时器 在 nrf 平台
* :github:`35489` - samples: net: gsm_modem: build fails if CONFIG_GSM_MUX=y
* :github:`35480` - pm: device_runtime: ``pm_device_request`` can block forever
* :github:`35479` - 地址  不  known 内核 object 异常 带 arcmwdt toolchain
* :github:`35476` - bluetooth: controller assertion when scanning with multiple active connections
* :github:`35474` - The dma-stm32 driver don't build for STM32F0 MCUs
* :github:`35444` - drivers: sensor: sbs-gauge: The sbs-gauge cannot be read from sensor shell
* :github:`35401` - Enabling POSIX_API leads to SSL handshake error
* :github:`35395` - STM32F4: Infinite reboot loop due to Ethernet initialization
* :github:`35390` - net.socket.tls.tls_ext: frdm_k64f test failure
* :github:`35383` - Can't setup ISO Broadcast Demo on nrf53dk
* :github:`35380` - sys: timeutil: inconsistent types for local times
* :github:`35363` - bt_gatt_discover() retunrs incorrect handle (offset by -1)
* :github:`35360` - Power consumption nRF52
* :github:`35352` - [Coverity CID: 215376] Out-of-bounds access in drivers/sensor/lis2dh/lis2dh_trigger.c
* :github:`35351` - [Coverity CID: 219472] Unrecoverable parse warning in tests/kernel/mem_protect/mem_protect/src/mem_domain.c
* :github:`35350` - [Coverity CID: 236055] Out-of-bounds access in subsys/modbus/modbus_core.c
* :github:`35349` - [Coverity CID: 236057] Unrecoverable parse warning in tests/kernel/mem_protect/mem_protect/src/mem_domain.c
* :github:`35348` - [Coverity CID: 236060] Out-of-bounds access in subsys/net/l2/ppp/ppp_l2.c
* :github:`35347` - [Coverity CID: 236064] Dereference null return value in subsys/bluetooth/controller/ll_sw/ull.c
* :github:`35346` - [Coverity CID: 236069] Out-of-bounds access in tests/lib/c_lib/src/main.c
* :github:`35345` - [Coverity CID: 236074] Out-of-bounds access in tests/lib/c_lib/src/main.c
* :github:`35344` - [Coverity CID: 236075] Out-of-bounds access in subsys/bluetooth/controller/hci/hci.c
* :github:`35343` - [Coverity CID: 236079] Untrusted divisor in subsys/bluetooth/controller/hci/hci.c
* :github:`35342` - [Coverity CID: 236085] Dereference after null check in samples/userspace/prod_consumer/src/app_a.c
* :github:`35341` - twister: Hardware map creation is buggy (+ inaccurate docs)
* :github:`35338` - USB: ethernet CDC ECM/EEM support is broken
* :github:`35336` - tests: samples: power: samples/subsys/pm/device_pm/sample.power.ospm.dev_idle_pm fails on nrf52 platforms
* :github:`35329` - samples: gsm_modem: Compilation failed, likely related to logging changes
* :github:`35327` - Sensor Code for CC3220sf
* :github:`35325` - shell 内核 重启 echo  abruptly 终止
* :github:`35321` - Improve STM32: Serial Driver,Handle uart mode per instance
* :github:`35307` - ARM64 system calls are entered with interrupts masked
* :github:`35305` - 链接 排序 当...时 使用 两者 TF-M 和 Mbed TLS
* :github:`35299` - PM 挂起 IPC 消息 sporadically 不  传递
* :github:`35297` - STM32 SPI - wrong behavior after PR 34731
* :github:`35286` - 新 日志记录 损坏 eclipse
* :github:`35278` - LittleFs Sample will not build for qemu_riscv64 sample target
* :github:`35263` - device_pm_control_nop  使用 在...中 dac_mcp4725.c
* :github:`35242` - intel_adsp_cavs15: run kernel common testcases failed on ADSP
* :github:`35241` - intel_adsp_cavs15: run interrupt testcases failed on ADSP
* :github:`35236` - 测试 doc: 记录 generation 进程 FAILS 带 有效 模块 ``samples:``
* :github:`35223` - Coverity [CID 221772]: Wrong operator used in logging subsystem, multiple violations
* :github:`35220` - tests: dma: memory-to-memory transfer fails on stm32f746zg nucleo board
* :github:`35219` - tests: driver: dma test case loop_transfer fails on stm32 with dmamux
* :github:`35215` - tests/kernel/msgq/msgq_usage 失败 在...上 hsdk 板
* :github:`35209` - tests/kernel/mem_heap/mheap_api_concept 失败 在...上 hsdk 板
* :github:`35204` - PPI channel assignment for Bluetooth controller is incorrect for nRF52805
* :github:`35202` - smp atomic_t global_lock  从不  cleared 当...时  线程 oops 带 global_lock  设置
* :github:`35200` - tests/kernel/smp 失败 在...上 hsdk 板
* :github:`35199` - Queues: there is no documentation about queue's implementation.
* :github:`35198` - subsys.pm.device_pm: frdm_k64f leave idel fails
* :github:`35197` - Zephyr Project Development with 2 Ethernet Interfaces Supported (eth0, and eth1)
* :github:`35195` - doc, coding guidelines: broken CERT-C links
* :github:`35191` - GIT Checkout of Master Branch is 2.6.0rc1 versus west update as 2.5.99
* :github:`35189` - Coding Guidelines: Resolve the issues under Rule 21.2
* :github:`35187` - 版本 selection 不 工作
* :github:`35176` - strtol crashes
* :github:`35175` - quectel-bg9x crashes in modem_rssi_query_work
* :github:`35169` - esp32:    uart_poll_in never ready for UART2 only
* :github:`35163` - [Coverity CID: 236009] Wrong sizeof argument in tests/lib/cbprintf_package/src/test.inc
* :github:`35162` - [Coverity CID: 235972] Wrong sizeof argument in tests/lib/cbprintf_package/src/test.inc
* :github:`35161` - [Coverity CID: 235962] Unused value in tests/kernel/mem_protect/mem_map/src/main.c
* :github:`35160` - [Coverity CID: 235930] Unused value in kernel/mmu.c
* :github:`35159` - [Coverity CID: 232698] Uninitialized scalar variable in samples/net/sockets/txtime/src/main.c
* :github:`35158` - [Coverity CID: 224630] Uninitialized scalar variable in subsys/net/ip/igmp.c
* :github:`35157` - [Coverity CID: 221380] Uninitialized scalar variable in subsys/bluetooth/controller/ll_sw/ull_iso.c
* :github:`35156` - [Coverity CID: 235979] Unchecked return value in drivers/sensor/iis2mdc/iis2mdc_trigger.c
* :github:`35155` - [Coverity CID: 235677] Unchecked return value in drivers/gpio/gpio_cy8c95xx.c
* :github:`35154` - [Coverity CID: 233524] Unchecked return value in include/drivers/dma.h
* :github:`35153` - [Coverity CID: 236006] Structurally dead code in tests/subsys/logging/log_api/src/test.inc
* :github:`35152` - [Coverity CID: 235986] Structurally dead code in tests/subsys/logging/log_api/src/test.inc
* :github:`35151` - [Coverity CID: 235943] Reliance on integer endianness in include/sys/cbprintf_cxx.h
* :github:`35150` - [Coverity CID: 225136] Out-of-bounds write in tests/kernel/sched/deadline/src/main.c
* :github:`35149` - [Coverity CID: 234410] Out-of-bounds read in tests/kernel/sched/preempt/src/main.c
* :github:`35148` - [Coverity CID: 236015] Out-of-bounds access in tests/subsys/logging/log_api/src/mock_backend.c
* :github:`35147` - [Coverity CID: 236012] Out-of-bounds access in subsys/bluetooth/audio/vcs_client.c
* :github:`35146` - [Coverity CID: 235994] Out-of-bounds access in tests/kernel/interrupt/src/interrupt_offload.c
* :github:`35145` - [Coverity CID: 235984] Out-of-bounds access in include/sys/cbprintf_cxx.h
* :github:`35144` - [Coverity CID: 235944] Out-of-bounds access in subsys/bluetooth/audio/vcs_client.c
* :github:`35143` - [Coverity CID: 235921] Out-of-bounds access in include/sys/cbprintf_cxx.h
* :github:`35142` - [Coverity CID: 235914] Out-of-bounds access in subsys/bluetooth/audio/vcs.c
* :github:`35141` - [Coverity CID: 235913] Out-of-bounds access in subsys/bluetooth/audio/vcs.c
* :github:`35140` - [Coverity CID: 231072] Out-of-bounds access in tests/kernel/sched/preempt/src/main.c
* :github:`35139` - [Coverity CID: 229646] Out-of-bounds access in subsys/bluetooth/audio/vocs.c
* :github:`35138` - [Coverity CID: 229545] Out-of-bounds access in tests/subsys/canbus/isotp/conformance/src/main.c
* :github:`35137` - [Coverity CID: 225993] Out-of-bounds access in tests/subsys/canbus/isotp/conformance/src/main.c
* :github:`35136` - [Coverity CID: 235916] Operands don't affect result in drivers/adc/adc_stm32.c
* :github:`35135` - [Coverity CID: 235911] Negative array index write in tests/subsys/logging/log_api/src/mock_backend.c
* :github:`35134` - [Coverity CID: 222151] Negative array index write in tests/subsys/logging/log_msg2/src/main.c
* :github:`35133` - [Coverity CID: 232501] Missing varargs init or cleanup in subsys/logging/log_msg2.c
* :github:`35132` - [Coverity CID: 236003] Logically dead code in subsys/bluetooth/audio/vcs.c
* :github:`35131` - [Coverity CID: 235998] Logically dead code in subsys/bluetooth/audio/vcs.c
* :github:`35130` - [Coverity CID: 235997] Logically dead code in drivers/adc/adc_stm32.c
* :github:`35129` - [Coverity CID: 235990] Logically dead code in subsys/bluetooth/audio/vcs.c
* :github:`35128` - [Coverity CID: 235970] Logically dead code in subsys/bluetooth/audio/vcs.c
* :github:`35127` - [Coverity CID: 235965] Logically dead code in tests/subsys/logging/log_api/src/test.inc
* :github:`35126` - [Coverity CID: 235961] Logically dead code in tests/subsys/logging/log_api/src/test.inc
* :github:`35125` - [Coverity CID: 235956] Logically dead code in subsys/bluetooth/audio/vcs.c
* :github:`35124` - [Coverity CID: 235955] Logically dead code in subsys/bluetooth/audio/vcs.c
* :github:`35123` - [Coverity CID: 235954] Logically dead code in subsys/bluetooth/audio/vcs.c
* :github:`35122` - [Coverity CID: 235952] Logically dead code in subsys/bluetooth/audio/vcs.c
* :github:`35121` - [Coverity CID: 235950] Logically dead code in subsys/bluetooth/audio/vcs.c
* :github:`35120` - [Coverity CID: 235934] Logically dead code in subsys/bluetooth/audio/vcs.c
* :github:`35119` - [Coverity CID: 235932] Logically dead code in samples/sensor/adxl372/src/main.c
* :github:`35118` - [Coverity CID: 235919] Logically dead code in samples/sensor/bmg160/src/main.c
* :github:`35117` - [Coverity CID: 235945] Incorrect sizeof expression in include/sys/cbprintf_cxx.h
* :github:`35116` - [Coverity CID: 235987] Incompatible cast in include/sys/cbprintf_cxx.h
* :github:`35115` - [Coverity CID: 236000] Improper use of negative value in tests/lib/cbprintf_package/src/test.inc
* :github:`35114` - [Coverity CID: 221976] Division or modulo by zero in tests/drivers/can/timing/src/main.c
* :github:`35113` - [Coverity CID: 235985] Dereference before null check in subsys/bluetooth/audio/vcs_client.c
* :github:`35112` - [Coverity CID: 235983] Dereference after null check in samples/sensor/max17262/src/main.c
* :github:`35111` - [Coverity CID: 234630] Dereference after null check in tests/net/dhcpv4/src/main.c
* :github:`35110` - [Coverity CID: 220616] Arguments in wrong order in tests/subsys/canbus/isotp/conformance/src/main.c
* :github:`35108` - tests: drivers: pwm: pwm_api: failed on nucleo_f207zg
* :github:`35107` - Atmel SAM E70 / Cortex-M7 fails to boot if CONFIG_NOCACHE_MEMORY=y
* :github:`35104` - arch.interrupt.gen_isr_table.arm_mainline: fails on lpcxpresso55s16_ns
* :github:`35102` - testing.ztest.error_hook: fails on lpcxpresso55s16_ns
* :github:`35100` - libraries.libc.sprintf_new: fails on lpcxpresso55s16_ns and lpcxpresso55s69_ns
* :github:`35099` - benchmark.kernel.application.fp.arm: Illegal load of EXC_RETURN into PC on lpcxpresso55s16_ns and lpcxpresso55s69_ns
* :github:`35097` - arch.interrupt: fails on NXP Cortex-M0+ platforms
* :github:`35091` - enc424j600  不 工作
* :github:`35089` - stm32h7: systematic 崩溃 在 每个 第二 引导 带 NETWORKING=y
* :github:`35083` - dts: stm32mp1: SPI2 mixup with SAI2, SPI3 mixup with SAI3
* :github:`35082` - intel_adsp_cavs15: 所有  testcases 运行 失败 在...上 ADSP
* :github:`35079` - acrn_ehl_crb: 构建 警告 用于 旧 APIC_TIMER 配置
* :github:`35076` - acrn_ehl_crb does not work with CPUs >1
* :github:`35075` - .west/config west.yml and zephyr versioning during project development
* :github:`35073` - timer: cortex_m_systick: uptime drifting in tickless mode
* :github:`35060` - tests/kernel/common: test_nop failed on ARMV7_M_ARMV8_M_MAINLINE
* :github:`35058` - Bluetooth: deadlock when canceling db_hash.work from settings commit handler
* :github:`35051` - CONFIG_LOG2 fails for floating point output with warning and bad output
* :github:`35048` - mcuboot 带 启用 serial recovery  不 编译
* :github:`35046` - 跟踪 shows k_busy_wait()  执行 非常 often 在...上 nRF 平台
* :github:`35043` - NXP: Build error : ModuleNotFoundError: No module named 'elftools'
* :github:`35041` - Crash in net-shell when invoking "net dns" command
* :github:`35036` - STM32: Wrong uart_event_tx len calculation
* :github:`35033` - samples/boards: stm32 pm blinky fails when run with twister
* :github:`35028` - frdm_k64f: 失败 到 运行 tests/subsys/pm/power_mgmt/
* :github:`35027` - frdm_k64f: failed to run testcase tests/drivers/adc/adc_emul/
* :github:`35026` - sam_e70b_xplained: failed to run testcases tests/drivers/adc/adc_emul/
* :github:`35013` - Bluetooth: Controller: Out-of-Bound ULL context access during connection completion
* :github:`34999` - 使用 BT_ISO bluetooth hci_usb sample, 和 启用 但 仍然 shows 不 命令 支持
* :github:`34989` - Implement arch_page_phys_get() for ARM64
* :github:`34979` - MIMRT685-EVK 板 page  损坏 链接
* :github:`34978` - misleading root folder size in footprint reports
* :github:`34969` - Documentation still mentions deprecated macro DT_INST_FOREACH_STATUS_OKAY
* :github:`34964` - net regression: Connection to Zephyr server non-deterministically leads to client timeout, ENOTCONN on server side
* :github:`34962` - tfm: cmake: Toolchain not being passed into psa-arch-tests
* :github:`34950` - xtensa arch  源码 代码 版本  太 旧
* :github:`34948` - SoF module is not pointing at Zehpyr repo
* :github:`34935` - LwM2M: Block transfer with TLV format does not work
* :github:`34932` - drvers/flash/nrf_qspi_nor: high power consumption on nrf52840
* :github:`34931` - dns resolve timeout leads to CPU memory access violation error
* :github:`34925` - tests/lib/cbprintf_package 失败 到 构建
* :github:`34923` - net.socket.get_addr_info: frdm_k64f test fails
* :github:`34917` - arch.interrupt.arm| arch.interrupt.extra_exception_info: lpcxpresso55s28 series: test failure
* :github:`34915` - arch.interrupt.gen_isr_table.arm_mainline:lpcxpresso55s16_ns/lpcxpresso55s28: 中断 57  不 工作
* :github:`34911` - tests/kernel/mem_protect/mem_protect: frdm_k82f/frdm_k64f unexpected fatal error
* :github:`34909` - dma_loopback:lpcxpresso55s28_ns 驱动 测试 失败
* :github:`34904` - uart_mcux_lpuart: 启用 驱动 到 工作 带 ``CONFIG_MULTITHREADING=n``
* :github:`34903` - doc: Target 名称  错误 用于 rcar_h3ulcb 板
* :github:`34891` - mcumgr timeout due to smp_shell_process stalling
* :github:`34880` - Convert SoF Module to new kwork API
* :github:`34865` - CONFIG_NET_SOCKETS_PACKET interferes with other network traffic (gptp, IP)
* :github:`34862` - CAN ISO-TP implementation not using local work queue
* :github:`34852` - Some bluetooth advertising packages never get transmitted over-air (Bluetooth Mesh application)
* :github:`34844` - qemu_cortex_a53_smp:  tests/ztest/error_hook failed after enabling the FPU context switching support
* :github:`34840` - CONFIG_MULTITHREADING=n  不 测试 在...上 硬件 平台
* :github:`34838` - tests/subsys/logging/log_msg2 failes on qemu_cortex_a53
* :github:`34837` - Unstable multi connections between NRF52840
* :github:`34827` - tests: power management: test_power_state_trans fails on nrf boards
* :github:`34796` - x86 jlink runner fails on M1 macs
* :github:`34794` - LIS2DH Hard Fault when INT2 is not defined
* :github:`34788` - APIC 定时器  不 支持 SMP
* :github:`34777` - semaphore and condvar_api tests fails after ARM64 FPU context switch commit on qemu_cortex_a53_smp
* :github:`34772` - Mixed usage of signed/unsigned integer by the logging subsystem
* :github:`34757` - west update: Default behavior should fetch only --depth 1
* :github:`34753` - Building and Debugging Zephyr for Native Platform on Linux using VSCode and/or QtCreator
* :github:`34748` - Native posix: Segmentation fault in case of allocations without explicit heap assignment
* :github:`34739` - tests/arch/arm/arm_no_multithreading/arch.arm.no_multithreading 失败 到 构建 在...上  数量 的 平台
* :github:`34734` - Can handler doesn't compile with CONFIG_USERSPACE
* :github:`34722` - nvs: possibility of losing data
* :github:`34716` - 刷写 spi_nor: 构建 失败 当...时 CONFIG_SPI_NOR_SFDP_RUNTIME  启用
* :github:`34696` - Unable to select LOG_DICTIONARY_SUPPORT when TEST_LOGGING_DEFAULTS=y
* :github:`34690` - net: process_rx_packet() work handler violates requirements of Workqueue Threads implementation
* :github:`34687` - intel_adsp_cavs15: run tests/kernel/semaphore/semaphore/ failed on ADSP
* :github:`34683` - MCUboot not confirm image when using 'west flash'
* :github:`34672` - stm32h7: issue with CONFIG_UART_ASYNC_API=y
* :github:`34670` - smp_svr sample 配置 用于 serial 移植 带 shell management 启用  不 工作
* :github:`34669` - uart_read_fifo() reads only 2 chars on nucleo STM32L43KC and nRF52840-DK
* :github:`34668` - i2c_ite_it8xxx2.c fails to build - possibly related to device_pm_control_nop changes
* :github:`34667` - posix_apis:mimxrt685_evk_cm33 timeout in test_posix_realtime
* :github:`34662` - many udp networking cases fail on nxp platforms
* :github:`34658` - TF-M integration samples do not work with GNU ARM Embedded having GCC v10.x.x
* :github:`34656` - STM32 ADC - 读取 的 multiple 通道 在...中  排序
* :github:`34644` - CAN - Bus Driver Sample
* :github:`34635` - BME280 构建 错误
* :github:`34633` - STM32: Mass conversion of boards to dts based clock control configuration
* :github:`34624` - Coding guidelines 15.7 PR causes tests failures
* :github:`34605` - flash_stm32h7x.c 失败 到 构建
* :github:`34601` - sample: bluetooth: beacon: USAGE FAULT after few seconds on board b_l4s5i_iot01a
* :github:`34597` - Mismatch between ``ot ping`` and ``net ping``
* :github:`34593` - Using hci_usb with Bluez 5.55 or 5.58
* :github:`34585` - mec15xxevb_assy6853: test_timeout_order in tests/kernel/common assertion failed
* :github:`34584` - 内核 workqueue 线程  occasionally 不 invoked 当...时 内核  运行 在...中 cooperative 模式 仅
* :github:`34583` - twister failing: fails platform native_posix, test lib/cmsis_dsp/filtering
* :github:`34581` - Unable to work with SX1276 Lora module.
* :github:`34570` - IPC samples running secure but configured nonsecure (AN521)
* :github:`34568` - Compilation error with zephyr 2.3.0
* :github:`34563` - net: lib: sockets: Unable to select() file descriptors with number >= 32
* :github:`34558` - Compilation error with Log v2 and CONFIG_LOG_PRINTK
* :github:`34541` - per-adv-sync-create doesn't work on nRF52840, ./tests/bluetooth/shell/
* :github:`34538` - STM32 temperature sensor
* :github:`34534` - west 签名 回归问题 当...时 HEX 文件 不 exists
* :github:`34527` - Cpp compiling error: expected primary-expression before 'char'.    _Generic macros problem
* :github:`34526` - 日志记录 测试 失败 到 构建 在...上  数量 的 平台
* :github:`34515` - samples: net: syslog_net: hard fault when running on frdm_k64f
* :github:`34505` - mimxrt1050_evk:failed to run testcases tests/net
* :github:`34503` - up_squared and ehl_crb: test fails from timeout in application_development.cpp.libcxx.exceptions
* :github:`34500` - thingy52 lis2dh12 sensor values too large
* :github:`34495` - logger: Logger API cannot be compiled with C++
* :github:`34492` - 日志记录 仍然 损坏 带 SOF
* :github:`34482` - net_tunnel_virtual:frdm_k64f: 构建 失败
* :github:`34474` - MPS2-AN385 SRAM does not match what the documentation page says
* :github:`34473` - Add Requirements repository with infrastructure and placeholder requirements
* :github:`34469` - nrf53: nrf5340dk_nrf5340_cpunet not executing.
* :github:`34463` - LwM2M bootstrap DELETE operation not working
* :github:`34462` - samples: net: 套接字 包 reception 停止 工作 在...之后  在...期间
* :github:`34461` - Unable to use PWM pins with STM Nucleo H743ZI
* :github:`34443` - Document font display is incomplete
* :github:`34439` - 日志记录 subsystem causes 构建 到 失败 带 LLVM
* :github:`34434` - subsys: testsuite: ztest framework breaks if run in cooperative mode only
* :github:`34426` - RFC: API Change: USB HID remove get_protocol/set_protocol/get_idle/set_idle callbacks
* :github:`34423` - twister 构建 问题 带 arm64
* :github:`34419` - significant 构建 时间 增加 带 新 日志记录 subsystem
* :github:`34416` - 配置 HAS_DTS  不 函数 preventing 编译 用于 vendors 没有 设备 tree
* :github:`34409` - mDNS response on link local when using DHCPv4 and AutoIP/Static IP
* :github:`34403` - Logging disable function causes Zephyr hard lockup
* :github:`34402` - spi: spi_nrfx_spim: wrong clock frequency selected
* :github:`34397` - Update getting started docs to reflect gdb python requirements
* :github:`34387` - 错误 消息 在...中 include/linker/kobject-text.ld  unclear
* :github:`34382` - fs/nvs: 如果 closing ATE  到 高 offset NVS iterates 上 到  结束 的 刷写
* :github:`34372` - CPU Lockups when using own Log Backend
* :github:`34369` - Driver esp for wifi got a dead lock.
* :github:`34368` - Cmake's Python path breaks after using west build --pristine
* :github:`34363` - k_work: incorrect return values for synchronous cancel
* :github:`34355` - LittleFS sample code catch an "undefined symbol 'ITCM_ADDR' referenced in expression" in linker step
* :github:`34345` - samples/net/civetweb/websocket_server 失败 到 构建
* :github:`34342` - No output on SWO pin (STM32L4)
* :github:`34341` - SWO logging and DWT timing collision
* :github:`34329` - lwm2m: pmin and pmax attributes should be optional
* :github:`34325` - hal: microchip: Missing Wake bit definitions
* :github:`34309` - unable to connect to azure iot hub via mqtt protocol
* :github:`34308` - SPI transceive function only transmitting first tx_buffer on Sifive's MCU
* :github:`34304` - intel_adsp_cavs15: run tests/kernel/queue/ failed on ADSP
* :github:`34295` - TensorFlow Lite Micro Module
* :github:`34280` - 增加 USB 到 LPCXpresso55S69 板
* :github:`34275` - drivers: led_pwm: Improper label assignment
* :github:`34272` - twister: Add memory footprint info to json report
* :github:`34270` - NVS 读取 在...之后 consecutive 重启
* :github:`34265` - BME280 Pressure calculation
* :github:`34264` - CI: twister: Add  merged report from all sub-builds to buildkite build artifacts
* :github:`34262` - Unable to find detailed documentation on pinmux driver development
* :github:`34249` - Unable to initialize on STM32F103RE + Quectel EC21 using BG9x driver
* :github:`34246` - LoRa 驱动 发送 opcode 的 命令 没有 参数
* :github:`34234` - UART NS16550 Underflow Issue During Clearing Port
* :github:`34233` - OpenThread 构建 问题
* :github:`34231` - uzlib (decompression library)
* :github:`34229` - C++ Exception Support in qemu_riscv32 emulation
* :github:`34225` - BBC micro:bit v1.5 LSM303AGR-ACCEL
* :github:`34216` - 使用 nrfx_gpiote 库 带 spi(nrf52840)
* :github:`34214` - codes reference weak variable are optimized out
* :github:`34209` - BLE Mesh Provisioning generates value 0 outside of Specification for Blink, Beep, or Vibrate
* :github:`34206` - Question: Is zephyrproject actively maintaining the windows-curses sub-project?
* :github:`34202` - MPU Fault when running central coded bluetooth and ENC28J60 dhcpv4_client
* :github:`34201` - Fatal error when perform "bt phy-update" if there is not any connections at ./tests/bluetooth/shell
* :github:`34197` - samples: telnet: Tab completion not working in telnet shell
* :github:`34196` - st_lis2mdl: LSM303AGR-MAGN not detected
* :github:`34190` - Newbie: Simple C++ List App Builds for QEMU but not Native Posix Emulation
* :github:`34184` - video samples 失败 到 构建
* :github:`34178` - apds9960 sensor sample does not build on STM32
* :github:`34165` - SNTP 失败 到 close  使用 套接字
* :github:`34154` - AArch64 PR reviews and merges are lagging behind
* :github:`34152` - intel_adsp_cavs15: run tests/kernel/smp/ failed on ADSP
* :github:`34149` - 无效 链接 在...中 Zephyr 记录 到 ACRN page
* :github:`34145` - Convert NXP kinetis boards to have pindata in devicetree
* :github:`34134` - USB  不 工作 如果 bootloader badly 使用  设备 在...之前
* :github:`34117` - ehl_crb: tests/kernel/context tests failed
* :github:`34116` - mec15xxevb_assy6853: tests/kernel/mutex/sys_mutex/
* :github:`34107` - Convert tests/benchmarks/mbedtls/src/benchmark.c to new kwork API
* :github:`34106` - Convert tests/kernel/pending/src/main.c to new kwork API
* :github:`34104` - Convert tests/benchmarks/footprints/src/workq.c to new kwork API
* :github:`34103` - Convert drivers/console/uart_mux.c to new kwork API
* :github:`34102` - Convert drivers/serial/uart_sam0.c to new kwork API
* :github:`34101` - Convert subsys/mgmt to new kwork API
* :github:`34100` - Convert subsys/shell/shell_telnet to new kwork API
* :github:`34099` - Convert subsys/tracing/cpu_stats.c to new kwork API
* :github:`34098` - Convert samples/drivers/led_sx1509b_intensity to new kwork API
* :github:`34097` - Convert samples/boards/reel_board/mesh_badge to new kwork API
* :github:`34096` - Convert samples nrf clock_skew to new kwork API
* :github:`34095` - Convert CAN to new kwork API
* :github:`34094` - Convert ubsys/ipc/rpmsg_service/rpmsg_backend.c to new kwork API
* :github:`34093` - Convert bluetooth to new kwork API
* :github:`34092` - Convert usb to new kwork API
* :github:`34091` - Convert uart_stm32.c to new kwork API
* :github:`34090` - Convert video_sw_generator.c to new kwork API
* :github:`34082` - Bullets  损坏 在...中 documentation
* :github:`34076` - Unrecognized characters generated during document construction
* :github:`34068` - DOC BUILD FAIL
* :github:`34046` - 失败 到 构建 arm64 架构 related 板
* :github:`34045` - samples: subsys: mgmt: smp_srv: UDP sample does not boot on frdm_k64f
* :github:`34026` - RISCV32 QEMU illegal instruction exception / floating point support
* :github:`34023` - test_prevent_interruption  错误 数据 类型 用于 key
* :github:`34014` - Toolchain 编译 错误 的 RISC-V(rv32m1-vega 板
* :github:`34011` - NRF52840 DTS questions
* :github:`34010` - [Coverity CID: 220531] Copy into fixed size buffer in tests/net/socket/misc/src/main.c
* :github:`34009` - [Coverity CID: 220532] Unrecoverable parse warning in subsys/bluetooth/controller/ll_sw/ull_peripheral_iso.c
* :github:`34008` - [Coverity CID: 220533] Improper use of negative value in tests/net/socket/misc/src/main.c
* :github:`34007` - [Coverity CID: 220534] Out-of-bounds access in tests/arch/arm/arm_no_multithreading/src/main.c
* :github:`34006` - [Coverity CID: 220535] Dereference before null check in subsys/net/l2/virtual/virtual.c
* :github:`34005` - [Coverity CID: 220536] Pointer to local outside scope in subsys/net/lib/lwm2m/lwm2m_engine.c
* :github:`34004` - [Coverity CID: 220537] Uninitialized pointer read in tests/net/virtual/src/main.c
* :github:`34003` - [Coverity CID: 220538] Logically dead code in subsys/net/l2/virtual/virtual.c
* :github:`34002` - [Coverity CID: 220539] Improper use of negative value in tests/net/socket/misc/src/main.c
* :github:`34001` - [Coverity CID: 220540] Uninitialized scalar variable in samples/drivers/flash_shell/src/main.c
* :github:`34000` - [Coverity CID: 220541] Dereference before null check in subsys/net/lib/capture/capture.c
* :github:`33986` - TCP stack doesn't handle data received in FIN_WAIT_1
* :github:`33983` - example-application 模块 增加 trivial 驱动
* :github:`33981` - example-application 模块 增加 板 zxa_board_stub
* :github:`33978` - MCP2515 wrong BRP value
* :github:`33977` - Question: How best to contribute drivers upstream?
* :github:`33974` - The stm32wb55rc MCU does not operate on zephyr
* :github:`33969` - Hardfault error caused by ARM Cortex m0 non-4-byte alignment
* :github:`33968` - ESP32 移植 GSM 模块 编译 错误
* :github:`33967` - The printed total size differs from calculated from .json
* :github:`33966` - STM32: I-cache & D-cache
* :github:`33965` - example-application module: add trivial project
* :github:`33956` - 测试 内核 fpu: 几个 测试 related 到 fpu 失败 在...上 nrf5340dk_nrf5340_cpuappns
* :github:`33954` - I2C scan 在...中 UART shell  不 检测 任何 I2C 设备 在...上 ESP32
* :github:`33951` - periodic_adv not working with nRF5340 DK
* :github:`33950` - periodic_adv not working with nRF5340 DK
* :github:`33929` - subsys: logging: Sample app doesn't build if using Werror and logging with latest SDK
* :github:`33925` - Rework hl7800 驱动 到 使用 新 工作 队列 APIs
* :github:`33923` - GSM modem automatic operation selection mode problems
* :github:`33911` - test:twr_ke18f: tests/kernel/sched/schedule_api - kernel_threads_sched_userspace cases meet out our space
* :github:`33904` - having 问题 编译  shell program 和 它  缺陷 可能
* :github:`33898` - intel_adsp_cavs15: running testcases failed tests/kernel/workq/work on adsp
* :github:`33897` - Bluetooth: extended advertising can't restart after connection
* :github:`33896` - Device tree: STM32L4 defines can1 node for chips which do not support CAN peripheral
* :github:`33895` - Device tree: STM32L412 and STM32L422 are missing nodes
* :github:`33890` - Continuous Integration check patch false warnings
* :github:`33884` - CORTEX_M_DEBUG_NULL_POINTER_EXCEPTION_DETECTION_NONE  way 太 长
* :github:`33874` - twister: Add skip as error feature
* :github:`33868` - Bluetooth: controller: connectable advertisement disable race condition
* :github:`33866` - uart: TX_DONE occurs before transmission is complete.
* :github:`33860` - DEPRECATED, a replacement suggestion should be found somewhere
* :github:`33858` - tests: ztest: test trigger_fault_access from tests/ztest/error_hook fails on em_starterkit_em7d_v22
* :github:`33857` - atomic xtensa  build fail
* :github:`33843` - ESP32 example does not connect to WiFi
* :github:`33840` - [Coverity CID: 220301] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33839` - [Coverity CID: 220302] Uninitialized scalar variable in subsys/net/lib/lwm2m/lwm2m_rw_link_format.c
* :github:`33838` - [Coverity CID: 220304] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33837` - [Coverity CID: 220305] Logically dead code in drivers/gpio/gpio_nrfx.c
* :github:`33836` - [Coverity CID: 220306] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33835` - [Coverity CID: 220309] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33834` - [Coverity CID: 220310] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33833` - [Coverity CID: 220311] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33832` - [Coverity CID: 220312] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33831` - [Coverity CID: 220313] Logically dead code in subsys/bluetooth/services/ots/ots_obj_manager.c
* :github:`33830` - [Coverity CID: 220314] Untrusted value as argument in subsys/bluetooth/services/ots/ots_dir_list.c
* :github:`33829` - [Coverity CID: 220315] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33828` - [Coverity CID: 220316] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33827` - [Coverity CID: 220317] Unchecked return value in tests/kernel/pipe/pipe_api/src/test_pipe_contexts.c
* :github:`33826` - [Coverity CID: 220318] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33825` - [Coverity CID: 220319] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33824` - [Coverity CID: 220320] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33823` - [Coverity CID: 220321] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33822` - [Coverity CID: 220413] Explicit null dereferenced in tests/lib/sprintf/src/main.c
* :github:`33821` - [Coverity CID: 220414] Unused value in tests/subsys/logging/log_backend_fs/src/log_fs_test.c
* :github:`33820` - [Coverity CID: 220415] Uninitialized scalar variable in tests/posix/common/src/pthread.c
* :github:`33819` - [Coverity CID: 220417] Out-of-bounds access in subsys/modbus/modbus_core.c
* :github:`33818` - [Coverity CID: 220418] Destination buffer too small in subsys/modbus/modbus_raw.c
* :github:`33817` - [Coverity CID: 220419] Unchecked return value in subsys/bluetooth/host/gatt.c
* :github:`33816` - [Coverity CID: 220420] Out-of-bounds access in tests/subsys/modbus/src/test_modbus_raw.c
* :github:`33815` - [Coverity CID: 220421] Incorrect sizeof expression in tests/lib/cbprintf_package/src/main.c
* :github:`33814` - [Coverity CID: 220422] Extra argument to printf format specifier in tests/lib/sprintf/src/main.c
* :github:`33813` - [Coverity CID: 220423] Out-of-bounds access in subsys/net/l2/ppp/ppp_l2.c
* :github:`33812` - [Coverity CID: 220424] Out-of-bounds access in drivers/watchdog/wdt_mcux_imx_wdog.c
* :github:`33811` - [Coverity CID: 220425] Destination buffer too small in tests/subsys/modbus/src/test_modbus_raw.c
* :github:`33810` - [Coverity CID: 220426] Out-of-bounds access in tests/lib/c_lib/src/main.c
* :github:`33809` - [Coverity CID: 220427] Unchecked return value in tests/posix/common/src/pthread.c
* :github:`33808` - [Coverity CID: 220428] Out-of-bounds access in subsys/bluetooth/audio/vocs.c
* :github:`33807` - [Coverity CID: 220429] Out-of-bounds access in subsys/net/l2/ppp/ppp_l2.c
* :github:`33806` - [Coverity CID: 220430] Operands don't affect result in tests/lib/c_lib/src/main.c
* :github:`33805` - [Coverity CID: 220431] Extra argument to printf format specifier in tests/lib/sprintf/src/main.c
* :github:`33804` - [Coverity CID: 220432] Out-of-bounds access in subsys/net/l2/ethernet/ethernet.c
* :github:`33803` - [Coverity CID: 220433] Printf arg count mismatch in tests/lib/sprintf/src/main.c
* :github:`33802` - [Coverity CID: 220434] Resource leak in tests/lib/mem_alloc/src/main.c
* :github:`33801` - [Coverity CID: 220435] Extra argument to printf format specifier in tests/lib/sprintf/src/main.c
* :github:`33800` - [Coverity CID: 220436] Explicit null dereferenced in tests/lib/sprintf/src/main.c
* :github:`33799` - [Coverity CID: 220437] Wrong size argument in tests/lib/mem_alloc/src/main.c
* :github:`33798` - [Coverity CID: 220438] Out-of-bounds access in subsys/bluetooth/audio/vocs_client.c
* :github:`33797` - [Coverity CID: 220439] Destination buffer too small in tests/subsys/modbus/src/test_modbus_raw.c
* :github:`33796` - [Coverity CID: 220440] Out-of-bounds access in tests/subsys/modbus/src/test_modbus_raw.c
* :github:`33795` - [Coverity CID: 220441] Untrusted loop bound in subsys/modbus/modbus_client.c
* :github:`33794` - [Coverity CID: 220442] Pointless string comparison in tests/lib/c_lib/src/main.c
* :github:`33793` - [Coverity CID: 220443] Out-of-bounds access in tests/subsys/modbus/src/test_modbus_raw.c
* :github:`33792` - [Coverity CID: 220444] Out-of-bounds access in subsys/modbus/modbus_raw.c
* :github:`33791` - [Coverity CID: 220445] Unchecked return value in subsys/logging/log_backend_fs.c
* :github:`33790` - [Coverity CID: 220446] Printf arg count mismatch in tests/lib/sprintf/src/main.c
* :github:`33789` - [Coverity CID: 220447] Out-of-bounds access in subsys/modbus/modbus_raw.c
* :github:`33788` - [Coverity CID: 220448] Out-of-bounds access in tests/subsys/modbus/src/test_modbus_raw.c
* :github:`33787` - [Coverity CID: 220449] Unused value in tests/subsys/logging/log_backend_fs/src/log_fs_test.c
* :github:`33786` - [Coverity CID: 220450] Untrusted loop bound in subsys/modbus/modbus_client.c
* :github:`33785` - [Coverity CID: 220451] Resource leak in tests/lib/mem_alloc/src/main.c
* :github:`33784` - [Coverity CID: 220452] Out-of-bounds access in subsys/net/l2/ethernet/ethernet.c
* :github:`33783` - [Coverity CID: 220453] Extra argument to printf format specifier in tests/lib/sprintf/src/main.c
* :github:`33768` - Rpmsg initialisation on nRF53 may fail
* :github:`33765` - Regular loss of a few connection intervals
* :github:`33761` - Documentation: K_WORK_DEFINE usage is not shown in workqueue doc
* :github:`33754` - xtensa sys 定时器 中断 缺陷
* :github:`33745` - ``west attach`` silently downgrades to ``debugserver`` for openocd runner
* :github:`33729` - flash_write() in STM32L0 MCU throws hard fault
* :github:`33727` - mec15xxevb_assy6853: multiple tests failed due to assertion failure at kernel/sched.c:841
* :github:`33726` - test:mimxrt1010_evk:  tests/kernel/sched/schedule_api - kernel_threads_sched_userspace cases meet out our space
* :github:`33721` - STM32 serial 驱动 配置 API doesn't 设置 正确 datalength 当...时 甚至 或 odd parity  使用
* :github:`33712` - kernel/poll: 不 错误 happened 当...时 mutil-threads poll  相同 event 在  相同 时间
* :github:`33702` - cfb sample 构建 错误 用于 esp32 当...时 SSD1306  启用
* :github:`33697` - dts:dt-bindings No OCTOSPIM dt-bindings available for stm32h723
* :github:`33693` - cmake -E env: unknown option '-Wno-unique_unit_address_if_enabled'
* :github:`33667` - 测试 内核 定时器 测试 timeout_abs 从 tests/kernel/timer/timer_api 挂起 causing 测试 scenarios 到 失败
* :github:`33665` - 测试 内核 timer_api 失败 带 hard 故障 在...中 CONFIG_TICKLESS_KERNEL
* :github:`33662` - Make twister dig deeper in directory structure to find additional .yaml files
* :github:`33658` - Question: How is NUM_IRQS determined for example for STM32F401xC
* :github:`33655` - 增加 支持 用于 板 Nucleo-L412RB-P
* :github:`33646` - Expose net_ipv4_create, net_ipv6_create, and net_udp_create in standard header
* :github:`33645` - Random MAC after RESET - NRF52832
* :github:`33641` - API Meeting Minutes
* :github:`33635` - subsys/ipc/openamp sample 在...上 QEMU 不 工作 当...时 调试
* :github:`33633` - NXP imx rt1064 evk: Application does not boot when flash/flexSPI driver is enabled
* :github:`33629` - 测试 subsys: 日志记录 测试 从 /tests/subsys/logging/log_backend_fs 失败 在...上 nrf52840dk
* :github:`33625` - NVS: replace dev_name parameter by device reference in nvs_init()
* :github:`33612` - Add support to get adv address of a per_adv_sync object and lookup per_adv_sync object from adv address
* :github:`33610` - ARC: add ARCv3 HS6x support
* :github:`33609` - Question about memory usage of the binary zephyr.exe
* :github:`33600` - Master  损坏 在 build-time 当...时 SRAM  mapped 在  高 地址
* :github:`33593` - acrn_ehl_crb: general tests and samples execution slowdown
* :github:`33591` - wordlist (kobject hash)  不 生成 correctly 当...时 使用 高 地址 用于 SRAM 在...上 64-bit 平台
* :github:`33590` - nrf: 调试 任何 测试 失败 当...时 CORTEX_M_DEBUG_NULL_POINTER_EXCEPTION_DETECTION_DWT  启用
* :github:`33589` - SSD1306 driver no longer works for I2C displays
* :github:`33583` - nRF SPI CS control: CS set / release delay is longer than configured
* :github:`33572` -  <err> esp_event: SYSTEM_EVENT_STA_DISCONNECTED for wifi sample for esp32 board
* :github:`33568` - 测试 tests/arch/x86/info 失败 用于 ehl_crb
* :github:`33567` - sof: framework is redefnining MAX, MIN to version with limited capabilities
* :github:`33559` - pin 设置 错误 在...上 frdm_kl25z 板
* :github:`33558` - qemu_cortex_a53_smp 和 qemu_x86_64 失败 在...中 tests/kernel/condvar/condvar 在...期间 启用 用于 SMP
* :github:`33557` - there  不 网络 接口 到 工作 带 用于 wifi sample 用于 esp32 板
* :github:`33551` - tests: SMP: Two threads synchronize failed using mutex or semaphore while both doing irq_lock()
* :github:`33549` - xt-xcc unknown field 'obj' specified in initializer
* :github:`33548` - xt-xcc  不 支持 已弃用 attribute
* :github:`33545` - ehl_crb: tests/arch/x86/info failed.
* :github:`33544` - ehl_crb: portability.posix.common.posix_realtime failed.
* :github:`33543` - ehl_crb: tests/subsys/edac/ibecc failed.
* :github:`33542` - reel_board: samples/subsys/usb/hid/ timeout failure
* :github:`33539` - ehl_crb: tests/kernel/mem_heap/mheap_api_concept failed.
* :github:`33529` - adafruit_feather_nrf52840 dts not setting I2C controller compat (was: SSD1306 DTS properties not being generated in devicetree_unfixed.h)
* :github:`33526` - boards:  Optimal way to have customized dts for my project.
* :github:`33525` - ST Nucleo G071RB board support issue
* :github:`33524` - minor: kswap.h is included twice in kernel/init.c
* :github:`33523` - Bossac runner flashes at an incorrect offset
* :github:`33516` - 套接字 tcp application 崩溃 当...时 there  不 更多 net 缓冲区 在...中 case 的 reception
* :github:`33515` - arm64/mmu: Are you sure it's OK to use atomic_cas before the MMU is initialized?
* :github:`33512` - 构建 构建 target  总是 out-of-date
* :github:`33509` - samples: tests: watchdog: samples/subsys/task_wdt breaks nrf platforms performace
* :github:`33505` - WS2812 SPI LED driver with DMA on nrf52 bad SPI data
* :github:`33498` - west: Question on ``west flash --hex-file`` behavior with build.dir-fmt
* :github:`33491` - fwrite() 函数  cause  program 到 崩溃 当...时 错误 参数 passed
* :github:`33488` - Ring buffer makes it hard to discard items
* :github:`33479` - disk_access_spi_sdhc: Missing stop/end bit
* :github:`33475` - Need to add device node for UART10 in dts/arm/st/h7/stm32h723.dtsi
* :github:`33464` - SYS_INIT initialize priority "2-9" ordering error
* :github:`33459` - 拆分 zero 异常  不 启用 在...中 ARC
* :github:`33457` - Fail to build ARC zephyr with MetaWare toolchain
* :github:`33456` - lorawan: unconfirmed 消息 离开 栈 在...中 busy 状态
* :github:`33426` -  少数 失败 带 CONFIG_HCI_ACL_DATA_SIZE 在...中 nightly 构建
* :github:`33424` - 测试 ztest: 测试 从 tests/ztest/error_hook 失败 在...上 nrf5340dk_nrf5340_cpuappns
* :github:`33423` - tests: portability: tests/portability/cmsis_rtos_v2 fails on nrf5340dk_nrf5340_cpuappns
* :github:`33422` - samples/subsys/usb/dfu/sample.usb.dfu 失败 在...上 multiple 平台 在...中 daily 构建
* :github:`33421` - Add BT_LE_FEAT_BIT_PER_ADV checks for periodic advertising commands
* :github:`33403` - trigger_fault_divide_zero test case didn't run divide instruction
* :github:`33381` - West 调试  不 工作 带 Bluetooth shell 和 nRF52840 DK
* :github:`33378` - Extended advertising switch on / switch off loop impossible
* :github:`33374` - 网络 接口 routines  不 线程 safe
* :github:`33371` - mec15xxevb_assy6853: tests/drivers/gpio/gpio_basic_api/ failed
* :github:`33365` - Add STM32H7 Series USB Device Support
* :github:`33363` - Properly indicate ISR number in SystemView
* :github:`33356` - 使用 AT HOST 失败 构建
* :github:`33353` - 工作 k_work_schedule 从 运行 工作 item  不 计划
* :github:`33352` - Arduino Nano 33 BLE sense constantly resetting.
* :github:`33351` - uart peripheral outputs 7 bits when configured in 8 bits + parity on stm32
* :github:`33348` - ip/dhcpv4  不 thread-safe 在...中 SMP/preemptive 线程 配置
* :github:`33342` - disco_l475_iot1: Multiple definitions of z_timer_cycle_get_32, etc.
* :github:`33339` - API/functions to get remaining free heap size
* :github:`33330` - Poll on DTLS socket returns -EAGAIN if bind & receive any data.
* :github:`33326` - The gpio-map for adafruit_feather_stm32f405 looks like it contains conflicts
* :github:`33324` - Using bluetooth hci_usb sample, and set periodic adv enable, but bluez still shows no command supported
* :github:`33322` - Questions on ztest : 1) Can twister/ztests run on windows? 2) Project structure
* :github:`33319` - Kernel doesn't validate lock state on swap
* :github:`33318` - [Coverity CID: 219722] Resource leak in tests/lib/mem_alloc/src/main.c
* :github:`33317` - [Coverity CID: 219727] Improper use of negative value in tests/lib/cbprintf_package/src/main.c
* :github:`33316` - [Coverity CID: 219724] Side effect in assertion in tests/kernel/queue/src/test_queue_contexts.c
* :github:`33315` - [Coverity CID: 219723] Side effect in assertion in tests/kernel/queue/src/test_queue_contexts.c
* :github:`33314` - [Coverity CID: 219726] Side effect in assertion in tests/kernel/lifo/lifo_usage/src/main.c
* :github:`33313` - [Coverity CID: 219728] Untrusted array index read in subsys/bluetooth/host/iso.c
* :github:`33312` - [Coverity CID: 219721] Untrusted array index read in subsys/bluetooth/host/iso.c
* :github:`33311` - [Coverity CID: 219729] Logically dead code in lib/os/cbprintf_packaged.c
* :github:`33303` - __ASSERT does not display message or register info in v2.5.0
* :github:`33291` - 使用 两者 NET_SOCKETS_SOCKOPT_TLS 和 POSIX_API 失败 构建
* :github:`33280` - drivers: serial: nrf uarte: The application receives one more byte that was received over UART
* :github:`33273` - The z_smp_reacquire_global_lock() internal API is not used any where inside zephyr code base
* :github:`33269` - ILI9341 (ILI9XXX) set orientation function fails to update the display area correctly
* :github:`33265` - Power Management Overhaul
* :github:`33261` - gatt_notify 太 慢 在...上 Broadcast
* :github:`33253` - STM32G4 with USB-C PD: Some pins cannot be used as input by default
* :github:`33239` - lib/rbtree: Remove dead case in rb_remove()
* :github:`33238` - 测试 驱动 pwm API 失败 在...上 许多 板
* :github:`33233` - uart9 missing from <st/h7/stm32h7.dtsi>
* :github:`33218` - Incorrect documentation CONFIG_LOG_STRDUP_MAX_STRING
* :github:`33213` - Configuring a project with a sub-project (e.g. nRF5340) and an overlay causes an infinite configuring loop
* :github:`33212` - GUI configuration system (ninja menuconfig) exists with an error when the windows key is pressed
* :github:`33208` - cbprintf: Package size calculation is using best case alignment
* :github:`33207` - twister: 增加 选项 到 加载 list 带 quarantined 测试
* :github:`33203` - Bluetooth: host: ISO: Missing terminate reason in ISO disconnected callback
* :github:`33200` - USB CDC ACM sample application fails to compile
* :github:`33196` - I2C doesn't work on STM32F103RE
* :github:`33185` - TCP traffic with IPSP sample not working on 96Boards Nitrogen
* :github:`33176` - 测试 内核 Multiple 测试 cases 从 tests/kernel/workq/work_queue  失败
* :github:`33173` - tests/kernel/workq/work_queue fails on sam_e70_xplained
* :github:`33171` - Create Renesas HAL
* :github:`33169` - STM32 SPI Driver - Transmit (MOSI) Only - Infinite Loop on Tranceive
* :github:`33168` - CONFIG_HEAP_MEM_POOL_SIZE=64 doesn't work
* :github:`33164` - Newlib has no synchronization
* :github:`33153` - west flash cannot find OpenOCD
* :github:`33149` - subsys: canbus: canopen EDSEditor / libedssharp version that works with Zephyr's CANopenNode
* :github:`33147` - 不 able 到 构建 blinky 或 设置 toolchain 到 zephyr
* :github:`33142` - fs_mount 用于 FAT FS  不 distingush between 不 文件 系统 和 其他 错误
* :github:`33140` - STM32H7: Bus 故障 当...时 读取 损坏 刷写 sectors
* :github:`33138` - invalid west cmake diagnostics when using board alias
* :github:`33137` - Enabling DHCP without NET_MGMT shouldn't be allowed
* :github:`33127` - Improve documentation user experience
* :github:`33122` - Device-level Cache API
* :github:`33120` - iotdk: running testcase tests/kernel/mbox/mbox_api/ failed
* :github:`33114` - tests: mbox_api: testcase test_mbox_data_get_null has some bugs.
* :github:`33104` - 更新 Zephyr 到 fix 工作 队列 问题
* :github:`33101` - DNS resolver misbehaves if receiving response too late
* :github:`33100` - tcp2 不 工作 带 ppp
* :github:`33097` - Coverity ID links in associated GitHub issues are broken
* :github:`33096` - [Coverity CID :215373] Unchecked return value in subsys/net/lib/lwm2m/lwm2m_rd_client.c
* :github:`33095` - [Coverity CID :215379] Out-of-bounds write in subsys/mgmt/osdp/src/osdp_cp.c
* :github:`33094` - [Coverity CID :215381] Resource leak in samples/net/mdns_responder/src/service.c
* :github:`33093` - [Coverity CID :215391] Unchecked return value from library in samples/net/mdns_responder/src/service.c
* :github:`33092` - [Coverity CID :215392] Logically dead code in subsys/mgmt/osdp/src/osdp_cp.c
* :github:`33091` - [Coverity CID :219474] Logically dead code in subsys/bluetooth/controller/ll_sw/ull_scan.c
* :github:`33090` - [Coverity CID :219476] Dereference after null check in subsys/bluetooth/controller/ll_sw/ull_conn.c
* :github:`33089` - [Coverity CID :219556] Self assignment in drivers/espi/host_subs_npcx.c
* :github:`33088` - [Coverity CID :219558] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33087` - [Coverity CID :219559] Out-of-bounds access in tests/arch/arm/arm_interrupt/src/arm_interrupt.c
* :github:`33086` - [Coverity CID :219561] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33085` - [Coverity CID :219562] Out-of-bounds access in tests/bluetooth/tester/src/gatt.c
* :github:`33084` - [Coverity CID :219563] Dereference after null check in arch/x86/core/multiboot.c
* :github:`33083` - [Coverity CID :219564] Untrusted value as argument in subsys/net/lib/lwm2m/lwm2m_engine.c
* :github:`33082` - [Coverity CID :219566] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33081` - [Coverity CID :219572] Untrusted value as argument in tests/net/lib/coap/src/main.c
* :github:`33080` - [Coverity CID :219573] Untrusted value as argument in samples/net/sockets/coap_client/src/coap-client.c
* :github:`33079` - [Coverity CID :219574] Side effect in assertion in tests/subsys/edac/ibecc/src/ibecc.c
* :github:`33078` - [Coverity CID :219576] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33077` - [Coverity CID :219579] Out-of-bounds read in drivers/ipm/ipm_nrfx_ipc.c
* :github:`33076` - [Coverity CID :219583] Operands don't affect result in drivers/clock_control/clock_control_npcx.c
* :github:`33075` - [Coverity CID :219588] Out-of-bounds access in tests/bluetooth/tester/src/gatt.c
* :github:`33074` - [Coverity CID :219590] Unchecked return value in subsys/bluetooth/mesh/proxy.c
* :github:`33073` - [Coverity CID :219591] Untrusted divisor in drivers/sensor/bme680/bme680.c
* :github:`33072` - [Coverity CID :219593] Logically dead code in tests/arch/x86/pagetables/src/main.c
* :github:`33071` - [Coverity CID :219595] Dereference before null check in subsys/net/ip/net_context.c
* :github:`33070` - [Coverity CID :219596] Out-of-bounds read in tests/kernel/interrupt/src/dynamic_isr.c
* :github:`33069` - [Coverity CID :219597] Untrusted value as argument in tests/net/lib/coap/src/main.c
* :github:`33068` - [Coverity CID :219598] Out-of-bounds access in tests/bluetooth/tester/src/gatt.c
* :github:`33067` - [Coverity CID :219600] Unchecked return value in drivers/watchdog/wdt_wwdg_stm32.c
* :github:`33066` - [Coverity CID :219601] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33065` - [Coverity CID :219603] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33064` - [Coverity CID :219608] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33063` - [Coverity CID :219609] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33062` - [Coverity CID :219610] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33061` - [Coverity CID :219611] Dereference after null check in subsys/net/ip/tcp2.c
* :github:`33060` - [Coverity CID :219613] Uninitialized scalar variable in lib/cmsis_rtos_v1/cmsis_signal.c
* :github:`33059` - [Coverity CID :219615] Out-of-bounds access in tests/arch/arm/arm_irq_advanced_features/src/arm_zero_latency_irqs.c
* :github:`33058` - [Coverity CID :219616] Untrusted value as argument in subsys/net/lib/coap/coap_link_format.c
* :github:`33057` - [Coverity CID :219619] Untrusted divisor in subsys/bluetooth/controller/hci/hci.c
* :github:`33056` - [Coverity CID :219620] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33055` - [Coverity CID :219621] Uninitialized scalar variable in tests/net/socket/getaddrinfo/src/main.c
* :github:`33054` - [Coverity CID :219622] Untrusted value as argument in subsys/net/lib/coap/coap.c
* :github:`33053` - [Coverity CID :219623] Out-of-bounds read in drivers/ipm/ipm_nrfx_ipc.c
* :github:`33051` - [Coverity CID :219625] Unchecked return value in subsys/bluetooth/mesh/proxy.c
* :github:`33050` - [Coverity CID :219628] Untrusted value as argument in subsys/net/lib/lwm2m/lwm2m_engine.c
* :github:`33049` - [Coverity CID :219629] Operands don't affect result in drivers/clock_control/clock_control_npcx.c
* :github:`33048` - [Coverity CID :219631] Out-of-bounds read in drivers/espi/espi_npcx.c
* :github:`33047` - [Coverity CID :219634] Out-of-bounds access in tests/net/lib/dns_addremove/src/main.c
* :github:`33046` - [Coverity CID :219636] Untrusted value as argument in subsys/net/lib/lwm2m/lwm2m_engine.c
* :github:`33045` - [Coverity CID :219637] Untrusted value as argument in tests/net/lib/coap/src/main.c
* :github:`33044` - [Coverity CID :219638] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33043` - [Coverity CID :219641] Out-of-bounds access in tests/bluetooth/tester/src/gatt.c
* :github:`33042` - [Coverity CID :219644] Side effect in assertion in tests/subsys/edac/ibecc/src/ibecc.c
* :github:`33040` - [Coverity CID :219646] Untrusted value as argument in subsys/net/lib/coap/coap.c
* :github:`33039` - [Coverity CID :219647] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33038` - [Coverity CID :219649] Operands don't affect result in kernel/sem.c
* :github:`33037` - [Coverity CID :219650] Out-of-bounds access in samples/bluetooth/central_ht/src/main.c
* :github:`33036` - [Coverity CID :219651] Logically dead code in subsys/bluetooth/mesh/net.c
* :github:`33035` - [Coverity CID :219652] Unchecked return value in drivers/gpio/gpio_stm32.c
* :github:`33034` - [Coverity CID :219653] Unchecked return value in drivers/modem/hl7800.c
* :github:`33033` - [Coverity CID :219654] Out-of-bounds access in tests/net/lib/dns_addremove/src/main.c
* :github:`33032` - [Coverity CID :219656] Uninitialized scalar variable in tests/kernel/threads/thread_stack/src/main.c
* :github:`33031` - [Coverity CID :219658] Untrusted value as argument in samples/net/sockets/coap_client/src/coap-client.c
* :github:`33030` - [Coverity CID :219659] Side effect in assertion in tests/subsys/edac/ibecc/src/ibecc.c
* :github:`33029` - [Coverity CID :219660] Untrusted divisor in drivers/sensor/bme680/bme680.c
* :github:`33028` - [Coverity CID :219661] Unchecked return value in subsys/bluetooth/host/gatt.c
* :github:`33027` - [Coverity CID :219662] Inequality comparison against NULL in lib/os/cbprintf_packaged.c
* :github:`33026` - [Coverity CID :219666] Out-of-bounds access in tests/bluetooth/tester/src/gatt.c
* :github:`33025` - [Coverity CID :219667] Untrusted value as argument in tests/net/lib/coap/src/main.c
* :github:`33024` - [Coverity CID :219668] Dereference after null check in drivers/espi/host_subs_npcx.c
* :github:`33023` - [Coverity CID :219669] Untrusted value as argument in subsys/mgmt/updatehub/updatehub.c
* :github:`33022` - [Coverity CID :219672] Untrusted value as argument in samples/net/sockets/coap_server/src/coap-server.c
* :github:`33021` - [Coverity CID :219673] Untrusted value as argument in samples/net/sockets/coap_client/src/coap-client.c
* :github:`33020` - [Coverity CID :219675] Macro compares unsigned to 0 in kernel/include/mmu.h
* :github:`33019` - [Coverity CID :219676] Unchecked return value in drivers/modem/wncm14a2a.c
* :github:`33018` - [Coverity CID :219677] Logically dead code in drivers/timer/npcx_itim_timer.c
* :github:`33009` - 内核 k_heap 失败 在...上 小 堆
* :github:`33001` - stm32: window watchdog (wwdg): setup of prescaler not valid for newer series
* :github:`33000` - stm32: window watchdog (wwdg): invalid interrupts priority for CM0 Series Socs
* :github:`32996` - SPI speed when using SDHC via SPI in Zephyr
* :github:`32994` - Question: Possible simplification in mutex.h?
* :github:`32975` - 在...处   少数 include/ 头文件 live
* :github:`32969` - Wrong board target in microbit v2 documentation
* :github:`32966` - frdm_k64f: Run some testcases timeout failed by using twister
* :github:`32963` - USB 设备  不 支持 由 qemu_x86 平台
* :github:`32961` - [Coverity CID :219478] Unchecked return value in subsys/bluetooth/controller/ll_sw/ull_filter.c
* :github:`32960` - [Coverity CID :219479] Out-of-bounds access in subsys/net/l2/bluetooth/bluetooth.c
* :github:`32959` - [Coverity CID :219480] Out-of-bounds read in lib/os/cbprintf_nano.c
* :github:`32958` - [Coverity CID :219481] Out-of-bounds access in subsys/bluetooth/controller/ll_sw/nordic/lll/lll_adv_aux.c
* :github:`32957` - [Coverity CID :219483] Improper use of negative value in tests/drivers/timer/nrf_rtc_timer/src/main.c
* :github:`32956` - [Coverity CID :219484] Out-of-bounds access in tests/drivers/timer/nrf_rtc_timer/src/main.c
* :github:`32955` - [Coverity CID :219485] Logically dead code in subsys/bluetooth/controller/ll_sw/ull.c
* :github:`32954` - [Coverity CID :219486] Unrecoverable parse warning in tests/kernel/mem_protect/mem_protect/src/mem_domain.c
* :github:`32953` - [Coverity CID :219487] Resource leak in tests/net/socket/getaddrinfo/src/main.c
* :github:`32952` - [Coverity CID :219488] Unrecoverable parse warning in tests/kernel/mem_protect/mem_protect/src/mem_domain.c
* :github:`32951` - [Coverity CID :219489] Structurally dead code in tests/drivers/dma/loop_transfer/src/test_dma_loop.c
* :github:`32950` - [Coverity CID :219490] Unsigned compared against 0 in drivers/wifi/esp/esp.c
* :github:`32949` - [Coverity CID :219491] Resource leak in tests/net/socket/af_packet/src/main.c
* :github:`32948` - [Coverity CID :219492] Out-of-bounds access in tests/drivers/timer/nrf_rtc_timer/src/main.c
* :github:`32947` - [Coverity CID :219493] Unchecked return value in tests/kernel/workq/work/src/main.c
* :github:`32946` - [Coverity CID :219494] Logically dead code in boards/xtensa/intel_s1000_crb/pinmux.c
* :github:`32945` - [Coverity CID :219495] Pointless string comparison in tests/lib/devicetree/api/src/main.c
* :github:`32944` - [Coverity CID :219497] Logically dead code in subsys/bluetooth/host/gatt.c
* :github:`32943` - [Coverity CID :219498] Out-of-bounds access in tests/drivers/timer/nrf_rtc_timer/src/main.c
* :github:`32942` - [Coverity CID :219499] Argument cannot be negative in tests/net/socket/af_packet/src/main.c
* :github:`32941` - [Coverity CID :219501] Unchecked return value in subsys/net/l2/bluetooth/bluetooth.c
* :github:`32940` - [Coverity CID :219502] Improper use of negative value in tests/net/socket/af_packet/src/main.c
* :github:`32939` - [Coverity CID :219504] Logically dead code in subsys/net/lib/lwm2m/lwm2m_engine.c
* :github:`32938` - [Coverity CID :219508] Unchecked return value in lib/libc/minimal/source/stdlib/malloc.c
* :github:`32937` - [Coverity CID :219508] Unchecked return value in lib/libc/minimal/source/stdlib/malloc.c
* :github:`32936` - [Coverity CID :219509] Side effect in assertion in tests/net/socket/tcp/src/main.c
* :github:`32935` - [Coverity CID :219510] Improper use of negative value in tests/drivers/timer/nrf_rtc_timer/src/main.c
* :github:`32934` - [Coverity CID :219511] Uninitialized scalar variable in tests/kernel/mbox/mbox_api/src/test_mbox_api.c
* :github:`32933` - [Coverity CID :219512] Unrecoverable parse warning in tests/kernel/mem_protect/mem_protect/src/mem_domain.c
* :github:`32932` - [Coverity CID :219513] Logically dead code in drivers/wifi/esp/esp.c
* :github:`32931` - [Coverity CID :219514] Out-of-bounds access in tests/drivers/timer/nrf_rtc_timer/src/main.c
* :github:`32930` - [Coverity CID :219515] Side effect in assertion in subsys/bluetooth/controller/ll_sw/ull_sched.c
* :github:`32929` - [Coverity CID :219516] Improper use of negative value in tests/drivers/timer/nrf_rtc_timer/src/main.c
* :github:`32928` - [Coverity CID :219518] Macro compares unsigned to 0 in subsys/bluetooth/mesh/transport.c
* :github:`32927` - [Coverity CID :219519] Unchecked return value in drivers/ethernet/eth_sam_gmac.c
* :github:`32926` - [Coverity CID :219520] Unsigned compared against 0 in drivers/wifi/esp/esp.c
* :github:`32925` - [Coverity CID :219521] Unchecked return value in tests/kernel/workq/work/src/main.c
* :github:`32924` - [Coverity CID :219522] Unchecked return value in tests/subsys/dfu/mcuboot/src/main.c
* :github:`32923` - [Coverity CID :219523] Side effect in assertion in subsys/bluetooth/controller/ll_sw/ull_adv_sync.c
* :github:`32922` - [Coverity CID :219524] Logically dead code in drivers/wifi/esp/esp.c
* :github:`32921` - [Coverity CID :219525] Unchecked return value in tests/subsys/settings/functional/src/settings_basic_test.c
* :github:`32920` - [Coverity CID :219526] Operands don't affect result in tests/boards/mec15xxevb_assy6853/qspi/src/main.c
* :github:`32919` - [Coverity CID :219527] Resource leak in tests/net/socket/getaddrinfo/src/main.c
* :github:`32918` - [Coverity CID :219528] Arguments in wrong order in tests/drivers/pwm/pwm_loopback/src/main.c
* :github:`32917` - [Coverity CID :219529] Unchecked return value in subsys/bluetooth/controller/ll_sw/ull_filter.c
* :github:`32916` - [Coverity CID :219530] Dereference before null check in drivers/modem/ublox-sara-r4.c
* :github:`32915` - [Coverity CID :219531] Improper use of negative value in tests/drivers/timer/nrf_rtc_timer/src/main.c
* :github:`32914` - [Coverity CID :219532] Out-of-bounds access in tests/drivers/timer/nrf_rtc_timer/src/main.c
* :github:`32913` - [Coverity CID :219535] Dereference after null check in drivers/sensor/icm42605/icm42605.c
* :github:`32912` - [Coverity CID :219536] Dereference before null check in drivers/ieee802154/ieee802154_nrf5.c
* :github:`32911` - [Coverity CID :219537] Out-of-bounds access in samples/boards/nrf/system_off/src/retained.c
* :github:`32910` - [Coverity CID :219538] Illegal address computation in subsys/bluetooth/controller/ll_sw/nordic/lll/lll_adv_aux.c
* :github:`32909` - [Coverity CID :219540] Side effect in assertion in subsys/bluetooth/controller/ll_sw/ull_sched.c
* :github:`32908` - [Coverity CID :219541] Unused value in subsys/bluetooth/controller/ticker/ticker.c
* :github:`32907` - [Coverity CID :219542] Dereference null return value in subsys/bluetooth/mesh/heartbeat.c
* :github:`32906` - [Coverity CID :219543] Out-of-bounds access in samples/boards/nrf/mesh/onoff_level_lighting_vnd_app/src/smp_svr.c
* :github:`32905` - [Coverity CID :219544] Logically dead code in drivers/wifi/esp/esp.c
* :github:`32904` - [Coverity CID :219545] Side effect in assertion in subsys/bluetooth/controller/ll_sw/ull_adv_aux.c
* :github:`32903` - [Coverity CID :219546] Unchecked return value in tests/kernel/workq/work/src/main.c
* :github:`32902` - [Coverity CID :219547] Improper use of negative value in tests/drivers/timer/nrf_rtc_timer/src/main.c
* :github:`32898` - Bluetooth: controller: Control PDU buffer leak into Data PDU buffer pool
* :github:`32877` - acrn:  test case of kernel.timer and kernel.timer.tickless failed
* :github:`32875` - Benchmarking Zephyr vs. RIOT-OS
* :github:`32867` - tests/kernel/sched/schedule_api  不 启动 带 stm32wb55 在...上 nucleo
* :github:`32866` - bt_le_ext_adv_create returns -5 with 0x2036 opcode status 1
* :github:`32862` - MCUboot, use default UART_0 value for RECOVERY_UART_DEV_NAME
* :github:`32860` - Periodic advertising/synchronization on nRF52810
* :github:`32853` - lwm2m: uninitialized 变量 在...中 这 函数
* :github:`32839` - tests/kernel/timer/timer_api/test_timeout_abs 仍然 失败 在...上 multiple 平台
* :github:`32835` - twister: integration_platforms stopped working as it should
* :github:`32828` - tests: posix: Test case portability.posix.common.tls.newlib.posix_realtime fails on nrf9160dk_nrf9160
* :github:`32827` - question: Specify size of malloc arena
* :github:`32818` - Function z_swap_next_thread() missing coverage in sched.c
* :github:`32817` - Supporting fedora in the getting started docs
* :github:`32816` - ehl_crb: tests/kernel/timer/timer_api/timer_api/test_sleep_abs (kernel.timer.tickless) failed.
* :github:`32809` - Fail to build ARC zephyr with MetaWare toolchain
* :github:`32800` - Race conditions with setting thread attributes after ``z_ready_thread``?
* :github:`32798` - west 刷写 失败 用于 reel 板
* :github:`32778` - Cannot support both HID boot report keyboard and mouse on a USB HID device
* :github:`32774` - Sensor BMI160: 设置 的 undersampling 模式  不 工作
* :github:`32771` - STM32 带 Ethernet 崩溃 当...时 接收 包 早
* :github:`32757` - Need openthread merge
* :github:`32755` - mcumgr: shell output gets truncated
* :github:`32745` - Bluetooth PAST shell command
* :github:`32742` - Bluetooth: GAP: LE connection complete event handling priority
* :github:`32741` - ARM32 / ARM64 separation
* :github:`32735` - Subsys: Logging: Functions purely to avoid compiling error affects test coverage
* :github:`32724` - qemu 定时器 更改 引入 新 CI 失败
* :github:`32723` - kernel/sched: 仅 发送 IPI 到 中止  线程 如果  硬件 支持 它
* :github:`32721` - samples/bluetooth/periodic_adv/, print random address after every reset
* :github:`32720` - ./samples/microbit/central_eatt 构建 失败 在 v2.5.0 发布
* :github:`32718` - NUCLEO-F446RE: Enable CAN Module
* :github:`32715` - async uart api not working on stm32 with dmamux
* :github:`32705` - KERNEL_COHERENCE on xtensa doesn't quite work yet
* :github:`32702` - RAM overflow with bbc:microbit for samples/bluetooth/peripheral...
* :github:`32699` - Setting custom BOARD_ROOT raises FileNotFoundError
* :github:`32697` - sam_e70b_xplained: running tests/kernel/timer/timer_api failed
* :github:`32696` - intel_adsp_cavs15: run testcases failed of tests/kernel/common
* :github:`32695` - intel_adsp_cavs15: cannot get output of some testcases
* :github:`32691` - Function z_find_first_thread_to_unpend() missing coverage in sched.c
* :github:`32688` - up_squared: tests/kernel/timer/timer_api failed.
* :github:`32679` - twister with --device-testing sometimes overlaps tests
* :github:`32677` - z_user_string_nlen() might lead to non-recoverable errors, despite suggesting the opposite
* :github:`32657` - canopen sample wont respond on pdo mapping with CO_ODs from objdict.eds
* :github:`32656` - reel_board: tests/lib/devicetree/devices/ build failure
* :github:`32655` - reel_board: tests/kernel/timer/timer_api/ failure
* :github:`32644` - Cannot build any project with system-wide DTC
* :github:`32619` - samples: usb: audio: Samples for usb audio fail building
* :github:`32599` - bbc_microbit build failure is blocking CI
* :github:`32589` - ehl_crb: tests/kernel/context fails sporadically
* :github:`32581` - shell/usb cdc_acm: shell  不 工作 在...上 CDC_ACM
* :github:`32579` - Corrupt CBOR payloads in MCUMGR when sending multiple commands together
* :github:`32572` - tests/kernel/timer/timer_api/test_timeout_abs 失败 在...上 stm32 板
* :github:`32566` - lwm2m: 长 endpoint 名称  truncated due 到 短 缓冲区
* :github:`32537` - Fatal error syscall_list.h
* :github:`32536` - Codec phy connection ASSERTION FAIL [event.curr.abort_cb]
* :github:`32515` - zephyr/kernel/thread.c:382 failed
* :github:`32514` - frdm_k64f:running testcase tests/subsys/debug/coredump/ and tests/subsys/debug/coredump_backends/ failed
* :github:`32513` - intel_adsp_cavs15: run testcases of fifo failed
* :github:`32512` - intel_adsp_cavs15: 运行 testcases 的 队列 失败
* :github:`32511` - Zephyr build fail with LLVM on Ubuntu for target ARC
* :github:`32509` - west build -p auto -b nrf52840dk_nrf52840 samples/bluetooth/hci_uart FAILED with  zephyr-v2.5.0
* :github:`32506` - k_sleep: Invalid return value when using absolute timeout.
* :github:`32499` - k_sleep duration is off by 1 tick
* :github:`32497` - 不 检查 的 缓冲区 大小 在...中 l2cap_chan_le_recv
* :github:`32492` - AArch64: Rework secure states (NS vs S) discussion
* :github:`32485` - CONFIG_NFCT_PINS_AS_GPIOS not in Kconfig.soc for nRF53
* :github:`32478` - twister: Twister cannot properly handle runners errors (flashing)
* :github:`32475` - twister error building mcux acmp driver
* :github:`32474` - pm: review post sleep wake up application notification scheduling
* :github:`32469` - Twister: potential race conditions.
* :github:`32468` - up_squared: tests/kernel/smp  failed.
* :github:`32467` - x86_64: page fault with access violation error complaining supervisor thread not allowed to rwx
* :github:`32459` - the cbprintf unit tests don't actually test all variations
* :github:`32457` - samples: drivers: espi: Need to handle failures in temperature retrieval
* :github:`32448` - C++ 异常  不 工作 在...上 multiple 平台
* :github:`32445` - 2021 GSoC Project Idea: Transplantation for embarc_mli
* :github:`32444` - z_cstart bug
* :github:`32433` - pwm_stm32: warning: non-portable use of "defined"
* :github:`32431` - RTC driver support on STM32F1 series
* :github:`32429` - 仅 一个 PWM 通道 支持 在...中 STM32L4 ?
* :github:`32420` - bbc_microbit_v2 构建 错误 用于 lis2dh
* :github:`32414` - [Coverity CID :218733] Explicit null dereferenced in tests/ztest/error_hook/src/main.c
* :github:`32413` - [Coverity CID :216799] Out-of-bounds access in tests/net/lib/dns_addremove/src/main.c
* :github:`32412` - [Coverity CID :216797] Dereference null return value in tests/net/6lo/src/main.c
* :github:`32411` - [Coverity CID :218744] Out-of-bounds access in subsys/bluetooth/host/gatt.c
* :github:`32410` - [Coverity CID :218743] Out-of-bounds access in subsys/bluetooth/host/gatt.c
* :github:`32409` - [Coverity CID :218742] Out-of-bounds access in subsys/bluetooth/host/gatt.c
* :github:`32408` - [Coverity CID :218741] Out-of-bounds access in subsys/bluetooth/host/att.c
* :github:`32407` - [Coverity CID :218740] Out-of-bounds access in subsys/bluetooth/host/gatt.c
* :github:`32406` - [Coverity CID :218737] Out-of-bounds write in subsys/bluetooth/host/gatt.c
* :github:`32405` - [Coverity CID :218735] Out-of-bounds access in subsys/bluetooth/host/att.c
* :github:`32404` - [Coverity CID :218734] Out-of-bounds access in subsys/bluetooth/host/smp.c
* :github:`32403` - [Coverity CID :218732] Out-of-bounds access in subsys/bluetooth/host/att.c
* :github:`32402` - [Coverity CID :218731] Out-of-bounds access in subsys/bluetooth/shell/gatt.c
* :github:`32401` - [Coverity CID :218730] Operands don't affect result in subsys/bluetooth/host/conn.c
* :github:`32400` - [Coverity CID :218729] Out-of-bounds access in subsys/bluetooth/host/gatt.c
* :github:`32399` - [Coverity CID :218728] Out-of-bounds access in subsys/bluetooth/host/gatt.c
* :github:`32398` - [Coverity CID :218727] Out-of-bounds access in subsys/bluetooth/host/gatt.c
* :github:`32397` - [Coverity CID :218726] Out-of-bounds access in subsys/bluetooth/host/att.c
* :github:`32385` - clock_control: int is returned on enum return value
* :github:`32382` - 时钟 问题 用于 STM32F103RE custom 板
* :github:`32376` - samples: driver: watchdog: Sample fails on disco_l475_iot1
* :github:`32375` - Networking 栈 崩溃 当...时 运行 在...中 cooperative 计划 模式 仅
* :github:`32365` - samples: hci_rpmsg build fail for nrf5340
* :github:`32344` - sporadic failure in tests/kernel/mem_protect/userspace/kernel.memory_protection.userspace
* :github:`32343` - openthread manual joiner hangs
* :github:`32342` - review use of cpsid in aarch32 / CONFIG_PM
* :github:`32331` - 使用 的 unitialized 变量 在...中 can_set_bitrate()
* :github:`32321` - /tmp/ccTlcyeD.s:242: Error: Unrecognized Symbol type  " "
* :github:`32320` - drivers: flash: stm32: Flush ART Flash cache after erase operation
* :github:`32314` - 2021 GSoC Project Idea: Enable Interactive Zephyr Test Suite
* :github:`32291` - Zephyr don't build sample hello world for Particle Xenon
* :github:`32289` - USDHC: 失败 在...之后 复位
* :github:`32279` - Question about flasing Adafruit Feather Sense with Zephyr
* :github:`32270` - TCP connection stalls
* :github:`32269` - shield: cmake: Shield conf is not loaded during build
* :github:`32265` - STM32F4 stuck handling I2C interrupt
* :github:`32261` - 问题 带 CONFIG_STACK_SENTINEL
* :github:`32260` - STM32 counter 驱动 错误 在...中 估算 alarm 时间
* :github:`32258` - power mgmt: pm_devices: Get rid of z_pm_core_devices array
* :github:`32257` - Common DFU partition enumeration API
* :github:`32256` - Bluetooth mesh : Long friendship establishment after reset
* :github:`32252` - Building anything for nrf5340pdk_nrf5340_cpuappns/mps2_an521_ns(any non-secure platforms) pulls external git trees
* :github:`32237` - twister failing locally - fails to link native_posix w/lld
* :github:`32234` - Documentation: How to update Zephyr itself (with west)
* :github:`32233` - Often disconnect timeouts when running the BLE peripheral HR sample on Nitrogen96
* :github:`32224` - Treat devicetree binding deprecation usage as build error when running w/twister
* :github:`32212` - Tx power levels are not similar on ADV and CONN modes when set manually (nRF52)
* :github:`32206` - CMSIS-DSP 支持 seems 损坏 在...上 链接
* :github:`32205` - [misc] AArch64 improvements and fixes
* :github:`32203` - Cannot set static address when using hci_usb or hci_uart on nRF5340 attached to Linux Host
* :github:`32201` - arch_switch() on ARM64 isn't quite right
* :github:`32197` - arch_switch() on SPARC isn't quite right
* :github:`32195` - ARMv8-nofp support
* :github:`32193` - Plan to support raspberry pi Pico?
* :github:`32158` - twister: inconsistent total testcases number with same configuration
* :github:`32145` - 内核 线程 和 内核 栈 deadlock 在...中 许多 scenarios
* :github:`32137` - Provide test execution times per ztest testcase
* :github:`32118` - drivers/flash/soc_flash_nrf: nRF anomaly 242 workaround is not implemented
* :github:`32098` -  Implement a driver for the   Microphone / audio sensor (MP23ABS1) in Sensotile.Box
* :github:`32084` - Custom Log Backend breaks performance
* :github:`32075` - net: lwm2m: Testing Strategy for LWM2M Engine
* :github:`32072` - tests/kernel/common seems to fail on nrf52833dk_nrf52833
* :github:`32071` - devicetree: ``bus:`` does not work in ``child-binding``
* :github:`32052` - p4wq has a race with work item re-use
* :github:`32023` - samples: bluetooth: peripheral_hids: Unable to communicate with paired device after board reset
* :github:`32000` - 2021 GSoC Call for Project Ideas - deadline Feb.19, 2021 12:00PM PST
* :github:`31985` - riscv: Long execution time when TICKLESS_KERNEL=y
* :github:`31982` - 测试 内核 队列 回归问题 引入 由 FPU sharing PR #31772
* :github:`31980` - Communicating with BMI160 chip over SPI
* :github:`31969` - test_tcp_fn:net2 mximxrt1060/1064/1050 fails on test_client_invalid_rst with semaphore timed out
* :github:`31964` - up_squared: tests/kernel/timer/timer_api failed.
* :github:`31922` - hci_usb: HCI ACL packet with size divisible by 64 not sent
* :github:`31856` - power: ``device_pm_get_sync`` not thread-safe
* :github:`31854` - undefined reference to ``sys_arch_reboot``
* :github:`31829` - net: lwm2m: Update IPSO objects to version 1.1
* :github:`31799` - uart_configure does not return -ENOTSUP for stm32 uart with 9 bit data length.
* :github:`31774` - Add an application power management sample (PM_POLICY_APP)
* :github:`31762` - ivshmem application in acrn
* :github:`31761` - logging:buffer_write with len=0 causes kernel panic
* :github:`31757` - GCC compiler option should include '-mcpu=hs38' for HSDK
* :github:`31742` - Bluetooth: BLE 5 data throughput to Linux host
* :github:`31721` - tests: nrf: posix: portability.posix.common.tls.newlib fails on nrf9160dk_nrf9160
* :github:`31711` - UART failure with CONFIG_UART_ASYNC_API
* :github:`31613` - Undefined reference errors when using External Library with k_msgq_* calls
* :github:`31588` - Bluetooth: Support for multiple connectable advertising sets with different identities.
* :github:`31585` - BMD345: Extended BLE range with PA/LNA
* :github:`31503` - drivers: i2c: i2c_nrfx_twim  Power Consumption rises after I2C data transfer
* :github:`31416` - ARC MPU version number misuse ver3, should be ver4
* :github:`31348` - twister: CI: Run twister daily builds with "--overflow-as-errors"
* :github:`31323` - Compilation warning regards the SNTP subsys
* :github:`31299` - tests/kernel/mbox/mbox_usage 失败 在...上 hsdk 板
* :github:`31284` - [stm32] PM restore console after sleep mode
* :github:`31280` - devicetree: Add a macro to easily get optionnal devicetree GPIO properties
* :github:`31254` - Bluetooth: 扩展 advertising 带 一个 advertising 设置 失败 在...之后  第一 时间
* :github:`31248` - i2c shell functions non-functional on nRF53
* :github:`31217` - Multi-threading 刷写 访问  不 支持 由 flash_write_protection_set()
* :github:`31191` - Samples: TF-M: Enable NS test app(s)
* :github:`31179` - ``iso bind`` for slave not working as intended
* :github:`31169` - kconfig configuration (prj.conf) based on zephyr version
* :github:`31164` - 问题 到 构建 lorawan 从 samples
* :github:`31150` - tests/subsys/canbus/isotp/conformance: failing on nucleo_f746zg
* :github:`31149` - tests/subsys/canbus/isotp/implementation: failing on nucleo_f746zg
* :github:`31103` - CMSIS RTOS v2 API implementation bugs in osEventFlagsWait
* :github:`31058` - SWO log backend clock frequency is off on some CPUs
* :github:`31036` - BMI 160 i2c version not working. I modified to i2c in kconfig to make it use i2c.
* :github:`31031` - samples/bluetooth/mesh is not helpful
* :github:`30991` - Unable to add new i2c sensor to nrf/samples
* :github:`30943` - MPU fault with STM32L452
* :github:`30936` - 测试 套接字 tcp: 增加  tls 测试
* :github:`30929` - PDM Driver for nrf52840dk
* :github:`30841` - 如何 到 禁用 reception 的 套接字 CAN frames
* :github:`30771` - 日志记录 故障 instruction 地址 在...中  日志记录 线程
* :github:`30770` - mps2_an521: no input to shell from Windows qemu host
* :github:`30618` - Add arduino header/spi support for HSDK board
* :github:`30544` - nrf5340 pwm "Unsupported board: pwm-led0 devicetree alias is not defined"
* :github:`30540` - CONFIG_TRACING 不 工作 在...之后 更新 从 v2.1.0 到 2.2.0
* :github:`30520` - recv() call to Ublox Sara R4 cant return 0
* :github:`30465` - Spurious interrupts not handled in ARMv7-R code with GICv2.
* :github:`30441` - hci_uart uses wrong BT_BUF_ACL_SIZE on dual chip solutions + multicore
* :github:`30429` - Thread Border Router with NRC/RCP sample and nrf52840dk not starting
* :github:`30416` - 不 restore 可能 带 mesh shell app 从 测试 使用 qemu_x86 在...上 RaspberryPi3
* :github:`30395` - 增加 possibility 到 使用 alternative list 的 平台 默认 用于 CI 运行
* :github:`30355` - Multiple vlan 接口 在...上 相同 接口 不 工作
* :github:`30353` - RFC: Logging subsystem overhaul
* :github:`30325` - Stack overflow with http post when using civetweb
* :github:`30204` - Support for Teensy 4.0 and 4.1
* :github:`30195` - 缺失 错误 检查 的 device_get_binding() 和 flash_area_open()
* :github:`30192` - mec15xxevb_assy6853: running tests/subsys/power/power_mgmt_soc failed
* :github:`30162` - Build zephyr with Metaware toolchain for HSDK fails
* :github:`30121` - Make log subsystem power aware
* :github:`30101` - tests should not be silently skipped due to insufficient RAM
* :github:`30074` - Occasional Spinlocks on zephyr 2.4.0 (ASSERTION FAIL [z_spin_lock_valid(l)] @ WEST_TOPDIR/zephyr/include/spinlock.h:92)
* :github:`30055` - 内存 corruption 用于 newlib-nano 带 float printf 和 禁用 堆
* :github:`29946` - SD card initialization is wrong
* :github:`29915` - eth: stm32h747i_disco: sem timeout and hang on debug build
* :github:`29798` - test spi loopback with dma fails on nucleo_f746zg
* :github:`29733` - SAM0 will wake up with interrupted execution after deep sleep
* :github:`29722` - West 刷写  不 able 到 刷写 带 openocd
* :github:`29689` - tests: drivers: gpio: gpio_basic_api: correct dts binding
* :github:`29610` - documentation says giving a semaphore can release IRQ lock
* :github:`29599` - gPTP: frdm_k64f : can not converge time
* :github:`29581` - LoRaWAN sample for 96b_wistrio - Tx timeout
* :github:`29545` - samples: tfm_integration: tfm_ipc: No module named 'cryptography.hazmat.primitives.asymmetric.ed25519'
* :github:`29526` - generic page pool for MMU-based systems
* :github:`29476` - Samples: TF-M: Add PSA FF API Sample
* :github:`29349` - Using float when driver init in RISC-V arch might cause system to get stuck.
* :github:`29224` - PTS: Test framework: Bluetooth: GATT/SR/GAC/BI-01-C - FAIL
* :github:`29107` - Bluetooth: hci-usb uses non-standard interfaces
* :github:`29038` - drivers/usb/device/usb_dc_native_posix_adapt.c sees weird commands and aborts
* :github:`28901` - implement searchable bitfields
* :github:`28900` - 增加 支持 用于 内存 un-mapping
* :github:`28873` - z_device_ready() lies
* :github:`28803` - Use generic config option for early platfrom init (AKA "warm boot")
* :github:`28722` - Bluetooth: provide ``struct bt_conn`` to ccc_changed callback
* :github:`28597` - Bluetooth: controller: Redesign the implementation/use of NODE_RX_TYPE_DC_PDU_RELEASE
* :github:`28551` - up_squared: samples/boards/up_squared/gpio_counter failed.
* :github:`28535` - RFC: Add lz4 Data Compresssion library Support
* :github:`28438` - Example downstream manifest+module repo in zephyrproject-rtos
* :github:`28249` - driver: espi: mchp: eSPI OOB driver does not support callbacks for incoming OOB messages from eSPI master.
* :github:`28105` - sporadic "Attempt to resume un-suspended thread object" faults on x86-64
* :github:`28096` - fatfs 更新 到 最新 upstream 版本
* :github:`27855` - i2c bitbanging on nrf52840
* :github:`27697` - Add support for passing -nogui 1 to J-Link Commander on MS Windows
* :github:`27692` - Allow to select between advertising packet/scan response for BT LE device name
* :github:`27525` - Including STM32Cube's USB PD support to Zephyr
* :github:`27484` - sanitycheck: Ease error interception from calling script
* :github:`27415` - 决定 如果 我们 保持  single 线程 支持 (CONFIG_MULTITHREADING=n) 在...中 Zephyr
* :github:`27356` - deep 审查 和 redesign 的 API 用于 工作 队列 functionality
* :github:`27203` - tests/subsys/storage/flash_map failure on twr_ke18f
* :github:`27048` - Improve out-of-tree driver experience
* :github:`27033` - Update terminology related to I2C
* :github:`27032` - zephyr 网络 栈 套接字 APIs  不 线程 safe
* :github:`27000` - Avoid oppressive language in code base
* :github:`26952` - SMP 支持 在...上 ARM64 平台
* :github:`26889` - subsys: power: Need syscall that allows to force sleep state
* :github:`26760` - 改进 caching 配置 和 move 它 到  cross 架构
* :github:`26728` - 允许 k_poll 用于 multiple 消息 队列
* :github:`26495` - 创建 k_poll 工作 带 KERNEL_COHERENCE
* :github:`26491` - PCIe: add API to get BAR region size
* :github:`26363` - samples: subsys: canbus: canopen: objdict: CO_OD.h is not normally made.
* :github:`26246` - Printing 64-bit values in LOG_DBG
* :github:`26172` - Zephyr Master/Slave not conforming with Core Spec. 5.2 connection policies
* :github:`26170` - HEXDUMP 日志 gives 警告 当...时 日志记录 函数 名称
* :github:`26118` - Bluetooth: controller: nRF5x: refactor radio_nrf5_ppi.h
* :github:`25956` - Including 头文件 文件 从 模块 进入 app
* :github:`25865` - Device Tree Memory Layout
* :github:`25775` - [Coverity CID :210075] Negative array index write in samples/net/cloud/mqtt_azure/src/main.c
* :github:`25719` - sanitycheck log mixing between tests
* :github:`25601` - UART input does not work on mps2_an{385,521}
* :github:`25440` - Bluetooth: controller: ensure deferred PDU populations complete on time
* :github:`25389` - driver MMIO address range management
* :github:`25313` - samples:mimxrt1010_evk:samples/subsys/usb/audio: 构建 错误 不 usbd 查找
* :github:`25187` - Generic ethernet packet filtering based on link (MAC) address
* :github:`24986` - Convert dma_nios2_msgdma to DTS
* :github:`24731` - Bluetooth: controller: Network privacy not respected when address resolution is disabled
* :github:`24625` - lib: drivers: clock: rtc:  rtc api to maintain calendar time through reboot
* :github:`24228` - 系统 power 状态
* :github:`24142` - NRF5340 PA/LNA support
* :github:`24119` - STM32: SPI: Extend power saving SPI pin config to all stm32 series
* :github:`24113` - STM32 刷写 设备 tree 更新
* :github:`23727` - RFC: clarification and standardization of ENOTSUP/ENOSYS error returns
* :github:`23520` - JLink Thread-Aware Debugging (RTOS Plugin)
* :github:`23465` - Zephyr Authentication - ZAUTH
* :github:`23449` - "make clean" doesn't clean a lot of generated files
* :github:`23225` - Bluetooth: Quality of service: Adaptive channel map
* :github:`23165` - macOS 设置 失败 到 构建 用于 lack 的 "elftools" Python 打包
* :github:`22965` - 4 byte addressing in spi_nor driver for memory larger than 128Mb.
* :github:`22956` - nios2: k_busy_wait() never returns if called with interrupts locked
* :github:`22731` - Improve docker CI documentation
* :github:`22620` - 适配 CPU stats 跟踪 到 跟踪 infrastructure
* :github:`22078` - stm32: Shell module sample doesn't work on nucleo_l152re
* :github:`22061` - Ethernet switch support
* :github:`22060` - 构建 失败 带 gcc-arm-none-eabi-9-2019-q4-major
* :github:`22027` - i2c_scanner  不 工作 在...上 olimexino_stm32
* :github:`21993` - Bluetooth: controller: split: Move the LLL event prepare/resume queue handling into LLL
* :github:`21840` - need test case for CONFIG_MULTIBOOT on x86
* :github:`21811` - Investigate using Doxygen-generated API docs vs. Sphinx/Breath API docs
* :github:`21809` - 更新 记录 生成 工具 到 newer 版本
* :github:`21783` - 重命名 zassert 函数
* :github:`21489` - 允许 到 读取 任何 类型 期间 discovery
* :github:`21484` - Option for safe k_thread_abort
* :github:`21342` - z_arch_cpu_halt() should enter deep power-down where supported
* :github:`21293` - 增加 timeout  I2C read/write 函数 用于  stm32 移植
* :github:`21136` - ARC: 增加 支持 用于 减少 register 文件
* :github:`21061` - 记录 在...处 APIs   called 从 使用 doxygen
* :github:`21033` - 读取 出 堆 space 使用 和 unallocated
* :github:`20707` - Define GATT service at run-time
* :github:`20576` - DTS overlay files must include full path name
* :github:`20366` - Make babbelsim testing more easily available outside of CI
* :github:`19655` - Milestones toward generalized representation of timeouts
* :github:`19582` - zephyr_library: missing 'kernel-mode' vs 'app-mode' documentation
* :github:`19340` - ARM: Cortex-M: Stack Overflows when building with NO_OPTIMIZATIONS
* :github:`19244` - BLE throughput of DFU by Mcumgr is too slow
* :github:`19224` - deprecate spi_flash_w25qxxdv
* :github:`18934` - Update Documentation To Reflect No Concurrent Multi-Protocol
* :github:`18554` - Tracking Issue for C++ Support as of release 2.1
* :github:`18509` - Bluetooth:Mesh:Memory allocation  太 大
* :github:`18351` - logging: 32 bit float values don't work.
* :github:`17991` - Cannot generate coverage reports on qemu_x86_64
* :github:`17748` - stm32: clock-control: Remove usage of SystemCoreClock
* :github:`17745` - stm32: Move clock configuration to device tree
* :github:`17571` - mempool is expensive for cyclic use
* :github:`17486` - nRF52: SPIM: Errata work-around status?
* :github:`17375` - Add VREF, TEMPSENSOR, VBAT internal channels to the stm32 adc driver
* :github:`17353` - 配置 带 POSIX_API 禁用 NET_SOCKETS_POSIX_NAMES
* :github:`17314` - doc: add tutorial for using mbed TLS
* :github:`16539` - include/ directory and header cleanup
* :github:`16150` - Make more LWM2M parameters configurable at runtime
* :github:`15855` - Create a reliable footprint tracking benchmark
* :github:`15854` - Footprint Enhancements
* :github:`15738` - Networking with QEMU for mac
* :github:`15497` - USB DFU: STM32: usb dfu mode doesn't work
* :github:`15134` - samples/boards/reel_board/mesh_badge/README.rst : No compilation or flash instructions
* :github:`14996` - 增强 mutex 测试
* :github:`14973` - samples: Specify the board target required for the sample
* :github:`14806` - Assorted pylint warnings in Python scripts
* :github:`14591` - Infineon Tricore architecture support
* :github:`14581` - 网络 接口   able 到 declare 如果 它们 工作 带 IPv4 和 IPv6 dynamically
* :github:`14442` - x86 SOC/CPU definitions need clean up.
* :github:`14309` - Automatic device dependency tracking
* :github:`19760` - 提供 命令 到 检查 板 支持 features
* :github:`13553` - Ways to reduce Bluetooth Mesh message loss
* :github:`13469` - Shell does not show ISR stack usage
* :github:`13436` - 启用 cooperative 计划 via menuconfig  result 在...中  无效 配置
* :github:`13091` - sockets: Implement MSG_WAITALL flag
* :github:`12718` - Generic MbedTLS setup doesn't use MBEDTLS_ENTROPY_C
* :github:`12098` - Not possible to print 64 bit decimal values with minimal libc
* :github:`12028` - Enable 16550 UART driver on x86_64
* :github:`11820` - 套接字 实现 (POSIX-compatible) timeout 支持
* :github:`11529` - Get 配置 的  运行 内核 在...中 控制台
* :github:`11449` - checkpatch warns on .dtsi files about line length
* :github:`11207` - ENOSYS has ambiguous meaning.
* :github:`10621` - RFC: 启用 设备 由 使用 dts, 不 Kconfig
* :github:`10499` - docs: References to "user threads" are confusing
* :github:`10494` - sockets: Implement MSG_TRUNC flag for recv()
* :github:`10436` - Mess with ssize_t, off_t definitions
* :github:`10268` - Clean up remaining SPI_DW defines in soc.h
* :github:`10042` - MISRA C - Do not cast an arithimetic type to void pointer
* :github:`10041` - MISRA C - types that indicate size and signedness should be used instead of basic numerical types
* :github:`10030` - MISRA C - Document Zephyr's code guideline based on MISRA C 2012
* :github:`9954` - samples/hello_world 构建 失败 在...上 Windows/MSYS
* :github:`9895` - MISRA C Add 'u' or 'U' suffix for all unsigned integer constants
* :github:`9894` - MISRA C Make external identifiers distinct according with C99
* :github:`9889` - MISRA C  Avoid implicit conversion between integers and boolean expressions
* :github:`9886` - MISRA C Do not mix signed and unsigned types
* :github:`9885` - MISRA C Do not have dead code
* :github:`9884` - MISRA-C 检查 return 值 的  non-void 函数
* :github:`9882` - MISRA-C - Do not use reserved names
* :github:`9778` - Implement zephyr specific SEGGER_RTT_LOCK and SEGGER_RTT_UNLOCK macros
* :github:`9626` - 增加 支持 用于  FRDM-KL28Z 板
* :github:`9507` - pwm: No clear semantics to stop a PWM leads to diverse implementations
* :github:`9284` - Issues/experience trying to use TI ARM code gen tools in Zephyr
* :github:`8958` - Bluetooth: Proprietary vendor specific opcode discovery
* :github:`8400` - test kernel XIP case seems not well defined
* :github:`8393` - ``CONFIG_MULTITHREADING=n`` builds call ``main()`` with interrupts locked
* :github:`7317` - 增加 generation 的 SPDX TagValue 记录 到 每个 构建
* :github:`7297` - STM32: 驱动 记录 series 支持 用于 每个 驱动
* :github:`7246` - esp32 fails to build with xtensa-esp32-elf-gcc: error: unrecognized command line option '-no-pie'
* :github:`7216` - Stop using gcc's "-include" flag
* :github:`7214` - Defines from DTS and Kconfig should be available simultaneously
* :github:`7151` - 板 Move existing 板 到 默认 配置 guidelines"
* :github:`6925` - Provide Reviewer Guidelines as part of the documentation
* :github:`6291` - userspace: support MMU-based memory virtualization
* :github:`6066` - LwM2M: support object versioning in register / discover operations
* :github:`5517` - 扩展 toolchain/SDK 支持
* :github:`5325` - 支持 interaction 带 控制台 在...中 twister
* :github:`5116` - [Coverity CID: 179986] Null pointer dereferences in /subsys/bluetooth/host/mesh/access.c
* :github:`4911` - Filesystem support for qemu
* :github:`4569` - LoRa:  support LoRa
* :github:`1418` - kconfig options need some cleanup and reorganisation
* :github:`1415` - 问题 带 forcing 新 line 在...中 生成 documentation.
* :github:`1392` - No module named 'elftools'
* :github:`3933` - LWM2M: Create application/link-format writer object to handle discovery formatting
* :github:`3931` - LWM2M: Data Validation Callback
* :github:`3723` - WiFi support for ESP32
* :github:`3675` - LE Adv. Ext.: Extended Scan with PHY selection for non-conn non-scan un-directed without aux packets
* :github:`3674` - LE Adv. Ext.: Non-Connectable and Non-Scannable Undirected without auxiliary packet
* :github:`3634` - ARM: implement NULL pointer protection
* :github:`3514` - Bluetooth: controller: LE Advertising Extensions
* :github:`3487` - Keep Zephyr Device tree Linux compatible
* :github:`3420` - Percepio Tracealyzer Support
* :github:`3280` - Paging Support
* :github:`2854` - Modbus RTU Support
* :github:`2542` - battery: Add standard APIs for Battery Charging and Fuel Gauge Handling (Energy Management)
* :github:`2470` - Supervisory 和 监视 任务
* :github:`2381` - SQL Database
* :github:`2336` - IPv4 - Multicast Join/Leave Support
