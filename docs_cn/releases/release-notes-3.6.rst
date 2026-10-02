:orphan:

.. _zephyr_3.6:

Zephyr 3.6.0
############

我们很高兴宣布 Zephyr 3.6.0 版本的发布。

本版本的主要增强功能包括：

* 新增 :ref:`GNSS 子系统 <gnss_api>`，使 Zephyr 应用具备地理感知能力。
* 新增用于 :ref:`键盘矩阵 <gpio-kbd>` 的 API 和驱动程序。
* 新增 socket 和 CoAP 服务库，分别简化 socket 和 CoAP 服务器的实现，同时优化资源使用。
* 集成 Trusted Firmware-M（TF-M）2.0，包括 Mbed TLS 3.5.2 的更新。
* 改进 LLEXT 工具，简化 Zephyr 构建系统中的模块创建。
* 用户空间支持扩展到 Xtensa 架构。
* 构建系统现支持链接时优化（LTO），减小最终镜像大小。
* 默认支持 Bluetooth Mesh 协议 1.1。
* 大幅更新 :zephyr:board:`native simulator <native_sim>` 的文档，明确支持的外设及其用法。
* 新增 30 余款受支持的开发板，覆盖 Zephyr 支持的所有架构。

从 Zephyr v3.5.0 迁移到 Zephyr v3.6.0 时所需或建议的变更概述，可参见单独的 :ref:`迁移指南 <migration_3.6>`。

以下章节按组件列出详细变更。

安全漏洞相关
******************************

本版本解决了以下 CVE：

更详细的信息可参见：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2023-5779 `Zephyr 项目缺陷跟踪器 GHSA-7cmj-963q-jj47
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-7cmj-963q-jj47>`_

* CVE-2023-6249 `Zephyr 项目缺陷跟踪器 GHSA-32f5-3p9h-2rqc
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-32f5-3p9h-2rqc>`_

* CVE-2023-6749 `Zephyr 项目缺陷跟踪器 GHSA-757h-rw37-66hw
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-757h-rw37-66hw>`_

* CVE-2023-6881 `Zephyr 项目缺陷跟踪器 GHSA-mh67-4h3q-p437
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-mh67-4h3q-p437>`_

* CVE-2023-7060：保密至 2024-03-14

* CVE-2024-1638 `Zephyr 项目缺陷跟踪器 GHSA-p6f3-f63q-5mc2
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-p6f3-f63q-5mc2>`_

架构
*************

* ARC

  * 为 ARCv3 处理器（HS5x 和 HS6x）启用了硬件预取器和共享集群缓存（SCM - Shared Cluster Memory）。
  * 禁用了具有两个或更多寄存器组的平台的线程本地存储（TLS）支持。
  * 修复了使用 MetaWare 工具链为硬件平台构建的应用程序运行不稳定的问题（.device_states 段中出现垃圾数据）。

* ARM

  * MPU 区域现在在初始化前始终被清除。
  * 统一使用 :c:func:`arch_secondary_cpu_init` 以在所有架构间保持一致。
  * 将 :c:func:`z_arm_prep_c` 重命名为 :c:func:`z_prep_c` 以在所有架构间保持一致。
  * 将异常头文件重命名以在所有架构间保持一致。
  * 新增 GDB 桩（目前仅支持 Zynq-7000）。
  * 新增使用 :kconfig:option:`CONFIG_ARM_CUSTOM_INTERRUPT_CONTROLLER` 支持自定义中断控制器。
  * 将 MMU 和 MPU 初始化移至 :c:func:`z_prep_c`，以便 Cortex-A 和 Cortex-R 可由各个核心进行初始化。
  * 将通用 Cortex-M MPU 代码移至 ``arch/arm/core/mpu``。

* Xtensa

  * 删除了未使用的 Kconfig 选项 ``CONFIG_XTENSA_NO_IPC``。

  * 通过 MMU 新增用户空间支持。

Bluetooth
*********

* 音频

  * 将 ``bt_bap_scan_delegator_subgroup`` 改为 :c:struct:`bt_bap_bass_subgroup`，
    使其不再依赖 :kconfig:option:`CONFIG_BT_BAP_SCAN_DELEGATOR`。
  * 修改 :c:func:`bt_bap_stream_send` 不再接受时间戳参数，
    新增 :c:func:`bt_bap_stream_send_ts` 用于接受时间戳。
  * 修改 :c:func:`bt_cap_stream_send` 不再接受时间戳参数，
    新增 :c:func:`bt_cap_stream_send_ts` 用于接受时间戳。
  * 将分配号值从 :file:`include/zephyr/bluetooth/audio/lc3.h` 移至
    :file:`include/zephyr/bluetooth/audio/audio.h`，并移除了 ``LC3`` 前缀。
  * CAP 发起方 API 已简化并遵循相同的参数模式。
  * 新增 Kconfig 选项使 MCC 功能可选，以减少简单客户端的内存使用。
  * 新增 CAP Commander 的音量变更和音量偏移变更功能。
  * 通过修改 ISO 数据路径的配置方式，新增在应用程序（而非控制器）中执行解码的支持。
  * 新增 :c:func:`bt_csip_set_member_unregister` 用于注销 CSIS 实例。
  * 新增辅助函数用于获取和设置编解码器配置及编解码器能力中的分配号值。
  * 新增对新单声道音频位置的支持。
  * 新增流 ISO 状态回调，使用户了解 CIS 的状态。
  * 新增 :c:func:`bt_pacs_set_available_contexts_for_conn` 用于按连接设置可用上下文。
  * 重构 :c:struct:`bt_bap_base` 为抽象结构体并新增辅助函数，
    使 Zephyr 支持所有 BASE 而不论其大小。

* 主机

  * 在 :c:struct:`bt_conn_cb` 中新增 ``recycled()`` 回调，
    在连接对象被释放时通知监听者，使其可用于不同用途。
    不保证哪个监听者能获得该对象，因为只响应第一次请求。
  * 修改 :c:func:`bt_iso_chan_send` 不再接受时间戳参数，
    新增 :c:func:`bt_iso_chan_send_ts` 用于接受时间戳。

* Mesh

  * 新增可延迟消息功能，用于在接入层对传输的响应施加随机延迟。
    该功能通过 :kconfig:option:`CONFIG_BT_MESH_ACCESS_DELAYABLE_MSG`
    Kconfig 选项启用。
  * Bluetooth Mesh 协议 1.1 现在默认支持。

* 控制器

  * 新增 ESP32 控制器的 deinit 实现。

* HCI 驱动

  * 将 ST HCI SPI Bluetooth 驱动从 Zephyr 驱动中分离，
    以基于 ST SPI 协议 V1 和 V2 提供更多功能。
    因此引入了 :dtcompatible:`st,hci-spi-v1` 和 :dtcompatible:`st,hci-spi-v2`。

开发板与 SoC 支持
********************

* 新增以下 SoC 系列的支持：

  * 新增 Renesas R-Car Gen4 系列的支持。
  * 新增 STM32F303xB SoC 变体的支持。
  * 新增 STM32H7B0xx SoC 变体的支持。
  * 新增 STM32L010xx SoC 变体的支持。
  * 新增 STM32L081xx SoC 变体的支持。
  * 新增 STM32U5A9xx SoC 变体的支持。
  * 新增 NXP S32K1 设备的支持。
  * 新增 NXP IMX8ULP SoC 的支持。
  * 新增 NXP MIMXRT595 DSP 核心的支持。

* 在其他 SoC 系列中做了以下变更：

  * Nordic SoC 现在隐含 :kconfig:option:`CONFIG_XIP` 而非选择它，
    这使得通过禁用它可以创建基于 RAM 的应用程序。
  * STM32WBA 系列现在支持 BLE。
  * xtensa: imx8: 将通用 i.MX8 SoC 拆分为 i.MX8QXP 和 i.MX8QM。
  * LPC55xxx: 修复了系统硬件时钟频率。

* 新增以下 ARM 开发板的支持：

  * 新增 Adafruit QTPy RP2040 开发板的支持：``adafruit_qt_py_rp2040``。
  * 新增 FANKE FK7B0M1-VBT6 开发板的支持：``fk7b0m1_vbt6``。
  * 新增 Renesas R-Car Spider 开发板 CR52 的支持：``rcar_spider_cr52``。
  * 新增 ST Nucleo F722ZE 开发板的支持：``nucleo_f722ze``。
  * 新增 ST STM32H750B Discovery Kit 的支持：``stm32h750b_dk``。
  * 新增 ST STM32L4R9I Discovery 开发板的支持：``stm32l4r9i_disco``。
  * 新增 ST STM32U5A9J-DK Discovery Kit 的支持：``stm32u5a9j_dk``。
  * 新增 ST Nucleo WBA55CG 开发板的支持：``nucleo_wba55cg``。
  * 新增 ST STM32WB5MM-DK Discovery 开发板的支持：``stm32wb5mm_dk``。
  * 新增 Wiznet W5500 评估 Pico 开发板的支持：``w5500_evb_pico``。
  * 新增 ADI 开发板的支持：``adi_sdp_k1``、``adi_eval_adin1110ebz``、
    ``adi_eval_adin2111ebz``。
  * 新增 NXP UCANS32K1SIC 开发板的支持：``ucans32k1sic``。

* 新增以下 RISC-V 开发板的支持：

  * 新增 Lilygo TTGO T8-C3 开发板的支持：``ttgo_t8c3``。

* 新增以下 Xtensa 开发板的支持：

  * 新增 NXP iMX8ULP 开发板的支持：``nxp_adsp_imx8ulp``。
  * 新增 Heltec Wireless Stick Lite（V3）开发板的支持：``heltec_wireless_stick_lite_v3``。
  * 新增 KINCONY-KC868-A32 开发板的支持：``kincony_kc868_a32``。
  * 新增 Lolin ESP32-S2 Mini 开发板的支持：``esp32s2_lolin_mini``。
  * 新增 Lilygo TTGO LoRa32 开发板的支持：``ttgo_lora32``。
  * 新增 M5Stack AtomS3 开发板的支持：``m5stack_atoms3``。
  * 新增 M5Stack AtomS3-Lite 开发板的支持：``m5stack_atoms3_lite``。
  * 新增 M5Stack StampS3 开发板的支持：``m5stack_stamps3``。

* 为 ARM 开发板做了以下变更：

  * 新增使用 RT595 在 G1120B0MIPI 上支持低功耗。
  * 新增 NXP 开发板 ``mimx93_evk_a55`` 上 lpspi、lpi2c 的支持。
  * 修复 ``lpcxpresso55s69`` 上的分区命名，使用 TFM 启用的 Zephyr 平台所用的标准插槽命名。
  * 在 ``frdm_kl25z``、``mimxrt1015_evk``、``mimxrt1020_evk``、``mimxrt1050_evk``、``mimxrt685_evk``、``frdm_k64f`` 上启用 linkserver 调试器支持。
  * 将 NXP 开发板上的 MCUBoot FW Update 模式从 Swap & Scratch 切换为 Swap & Move。

* 为 RISC-V 开发板做了以下变更：

  * 在 ``longan_nano`` 上启用 ADC 支持。

* 为 native/POSIX 开发板做了以下变更：

  * :ref:`模拟 nrf5340 目标 <nrf5340bsim>` 现在包含 IPC 和 MUTEX 外设，
    并支持 OpenAMP 在核心间通信。
    现在可以在 net 核心中运行 BLE 控制器或 802.15.4 驱动，
    在 app 核心中运行应用程序和 BT 主机。

  * nrf*_bsim 模拟目标现在包含 UART 外设的模型。
    现在可以将 :ref:`nrf52_bsim <nrf52_bsim>` 的 UART 连接到另一个 UART，
    或将 UART 设为环回，利用新的和旧的 nRFx UART 驱动，支持任意模式。

  * 对于基于 native 模拟器的目标，现在可以通过 Kconfig 命令行选项设置，
    这些选项将由可执行文件处理，如同从调用 shell 提供一样。

  * 对于所有 native 开发板，即使启用了 UART，native 日志后端现在也会被使用。

  * nRF5x 硬件模型的多个 bug 修复和其他小改进。

  * 所有 native 开发板的多个文档更新和修复。

* 新增以下扩展板的支持：

  * 新增 M5Stack-Core2 底板的支持：``m5stack_core2_ext``。
  * 新增 MikroElektronika ACCEL 13 Click 的支持：``mikroe_accel13_click``。
  * 新增 Waveshare Pico UPS-B 的支持：``waveshare_pico_ups_b``。
  * 新增 X-NUCLEO-BNRG2A1：BLE 扩展板的支持：``x_nucleo_bnrg2a1``。
  * 新增 X-NUCLEO-IKS4A1：MEMS 惯性和环境多传感器 的支持：``x_nucleo_iks4a1``。

构建系统与基础设施
*******************************

* 新增链接时优化功能。
  该变更包括中断脚本生成器重建，并新增以下 Kconfig 选项：

  - :kconfig:option:`CONFIG_ISR_TABLES_LOCAL_DECLARATION`：
    LTO 兼容的中断表解析器
  - :kconfig:option:`CONFIG_LTO`：启用链接时优化

  目前 LTO 兼容的中断表解析器仅由 ARM 架构和 GCC 编译器/链接器支持。
  详见拉取请求 :github:`66392`。

* 删除了 ``COMPAT_INCLUDES`` 选项。该选项自 Zephyr v3.0 以来未被使用。

* 修复了开发板修订版本 ``0`` 未包含该修订版本 overlay 文件的问题。

* 为 sysbuild 模块新增 ``PRE_IMAGE_CMAKE`` 和 ``POST_IMAGE_CMAKE`` 钩子，
  允许模块在每个镜像的 cmake 调用前后运行代码。

* 新增 :kconfig:option:`CONFIG_ROM_END_OFFSET` 选项，允许减小镜像大小。
  该选项旨在与固件签名脚本配合使用，这些脚本在构建之外向镜像末尾添加额外数据。

* 为包含 MCUboot 的 sysbuild 镜像新增 MCUboot 镜像大小缩减功能。
  这防止了构建对 MCUboot 来说过大的固件镜像的问题。

* 弃用 :kconfig:option:`CONFIG_BOOTLOADER_SRAM_SIZE`。
  该选项的用户应迁移到在其开发板设备树文件中正确设置 RAM。

* 修复了扩展板按其所在根目录顺序而非 cmake 提供顺序处理的问题。

* 修复了某些扩展板与 sysbuild 一起使用时导致 cmake Kconfig 错误的问题。

* 修复了使用 Picolibc 或为 native（``ARCH_POSIX``）目标构建时
  宏 ``_POSIX_C_SOURCE`` 和 ``_XOPEN_SOURCE`` 被全局定义的问题。
  此变更后，用户可能需要为其自己的应用程序或库定义这些宏。

* 新增 sysbuild 设置签名脚本（``SIGNING_SCRIPT``）的支持。
  详见 :ref:`west-extending-signing`。

* 在构建系统中新增 ``FILE_SUFFIX`` 支持，
  允许为应用程序 Kconfig 片段文件名和设备树 overlay 文件名添加后缀。
  详见 :ref:`application-file-suffixes` 和 :ref:`sysbuild_file_suffixes`。

* 弃用 ``CONF_FILE`` ``prj_<build>.conf`` 构建类型。

* 新增 ``-Wdouble-promotion`` 作为默认编译警告，
  提醒开发者单精度浮点数容易被提升为双精度。

驱动与传感器
*******************

* ADC

  * ADC 电源管理现在在 STM32 设备上受支持。
  * STM32 ADC 驱动现在支持混合共享和独立 IRQ
    （例如在具有 5 个 ADC 的 STM32G473 上，ADC1 和 ADC2 共享一个 IRQ，
    而 ADC3、ADC4 和 ADC5 各有独立 IRQ）。
    目前在此类设备上无法在同一应用程序中启用所有实例。

* 辅助显示

  * 新增 Sparkfun SerLCD 驱动。

* 音频

  * 新增 NXP DMIC 外设的驱动 :file:`drivers/audio/dmic_mcux.c`。
    该外设存在于 ``iMX RT5xx`` 和 ``iMX RT6xx`` 器件上，以及一些 LPC SoC 上。

* 电池备份 RAM

  * STM32WL 设备现在支持 BBRAM。

* CAN

  * 新增系统调用 :c:func:`can_get_mode()` 用于获取 CAN 控制器的当前操作模式。

  * 新增系统调用 :c:func:`can_get_transceiver()` 用于获取与 CAN 控制器关联的 CAN 收发器。

  * 新增 CAN 统计信息的访问函数。

  * 在 CAN 统计信息中新增通用位错误计数器。

  * 为以下驱动新增 CAN 统计信息支持：

    * :dtcompatible:`microchip,mcp2515`
    * :dtcompatible:`espressif,esp32-twai`
    * :dtcompatible:`kvaser,pcican`

  * 为 Nuvoton NuMaker 系列新增 CAN 控制器驱动
    （:dtcompatible:`nuvoton,numaker-canfd`）。

  * 为 Infineon XMC4xxx 系列新增 CAN 控制器驱动
    （:dtcompatible:`infineon,xmc4xxx-can` 和 :dtcompatible:`infineon,xmc4xxx-can-node`）。

  * 在 :dtcompatible:`nxp,flexcan` 驱动中新增对 NXP S32K1xx 系列的支持。

  * 所有基于 Bosch M_CAN 的前端驱动现在使用命名 IRQ，"int0" 和 "int1"。

  * :dtcompatible:`zephyr,native-linux-can` 驱动现在支持使用嵌入式 C 库构建。

  * 新增从 :ref:`CAN shell <can_shell>` 设置"raw"时序值的支持。

* 时钟控制

  * Renesas R-Car 时钟控制驱动现在支持 Gen4 SoC。
  * 将 ``CONFIG_CLOCK_CONTROL_RA`` 重命名为 :kconfig:option:`CONFIG_CLOCK_CONTROL_RENESAS_RA`。
  * 在 STM32 设备上，:dtcompatible:`st,stm32-hse-clock` 现在允许设置 ``css-enabled``
    属性以启用 HSE 时钟安全系统（CSS）。

* 计数器

  * nRFx 计数器驱动现在与模拟 nrf*_bsim 目标配合工作。
  * 新增顶值配置支持并修复了 native posix 驱动中的一个 bug。
  * 为 NXP RT6xx、RT5xx 和 LPC55xxx 新增 MRT 计数器支持。

* 加密

  * STM32WB 设备现在通过 AES 块支持加密 API。

* 显示

  * 在 STM32 LTDC 驱动中引入帧缓冲配置。

* DMA

  * STM32WBA 设备现在支持 GPDMA。
  * 为 NXP 的 eDMA IP 引入新的 DMA 驱动 :file:`drivers/dma/dma_nxp_edma.c`。

* 熵

  * "native_posix" 熵驱动现在接受新的命令行选项 ``seed-random``。
    使用时，随机数生成器将从 ``/dev/urandom`` 获取种子。
  * 在 STM32 设备上，RNG 块现在在池满时挂起以节省功耗。

* 以太网

  * "native_posix" 以太网驱动现在支持使用嵌入式 C 库构建。
  * 在 STM32H7 上启用硬件校验和卸载。
  * 新增 Open Alliance TC6 T1S 驱动的实现。
  * 新增 xmc4xxx 驱动。
  * 新增 NXP enet 驱动（含 PTP 支持）。
  * 新增 KSZ8081 PHY 驱动。
  * 在 NXP mcux 驱动中新增正确的 IPv4 多播支持。
  * 新增 LAN8651 T1S 支持。
  * 在 STM32 中新增 DSA 支持。
  * 新增 tja1103 PHY 支持。
  * 新增 Nuvoton numaker 支持。
  * 修复 lan865x 驱动。传输速度改进，IRQ 处理修复。
  * 修复 s32_gmac 驱动。链路 up/down 处理修复。
  * 修复 phy_mii 驱动。无效的 phy id 检查不正确。
  * 修复 sam_gmac 驱动。PTP 时钟调整对负值处理错误。
  * 修复 adin2111 驱动。与 adin2110 配合工作时初始化不正确。
  * 修复 ksz8081 驱动。日志变更，RMII 时钟修复，GPIO 引脚修复。
  * 新增 NXP ENET 的驱动 :file:`drivers/ethernet/eth_nxp_enet.c`，
    这是旧驱动 :file:`drivers/ethernet/eth_mcux.c` 的重构。
    旧驱动因缺乏 PHY 抽象的根本问题而变得难以维护。
    新驱动仍为实验性，需要进一步成熟。
    最终旧驱动将被弃用，转而支持此新驱动。

* 闪存

  * 重新设计 Atmel SAM 控制器以充分利用闪存页布局。
  * ``spi_nor`` 驱动现在在 ``spi_nor_wait_until_ready`` 中的轮询之间休眠。
    如果不需要（例如由于引导加载程序中的 ROM 限制），
    可以禁用 :kconfig:option:`CONFIG_SPI_NOR_SLEEP_WHILE_WAITING_UNTIL_READY`。
  * 在 STM32G4 和 STM32L4 系列上新增闪存读出保护配置。

  * ``nordic_qspi_nor`` 驱动现在支持用户可配置的 QSPI 超时，
    通过 :kconfig:option:`CONFIG_NORDIC_QSPI_NOR_TIMEOUT_MS`。

* GNSS

  * 新增 GNSS 设备驱动 API 和子系统，用于解析和发布位置、
    日期时间和卫星信息，通过
    :kconfig:option:`CONFIG_GNSS` 和 :kconfig:option:`CONFIG_GNSS_SATELLITES` 启用。
    GNSS 子系统和设备驱动基于 :ref:`modem` 子系统，
    使用 ``modem_pipe`` 模块、modem 后端和 ``modem_chat`` 模块
    与 modem 通信。对于已包含蜂窝 modem 的系统，
    由于子系统的复用，添加 GNSS modem 非常高效。

  * 新增 GNSS 专用的、安全的字符串转整数解析工具，
    通过 :kconfig:option:`CONFIG_GNSS_PARSE` 启用。

  * 新增 NMEA0183 解析工具，通过
    :kconfig:option:`CONFIG_GNSS_NMEA0183` 启用。

  * 新增大量 GNSS 数据日志记录，通过
    :kconfig:option:`CONFIG_GNSS_DUMP_TO_LOG` 启用。

  * 新增基于 UART 的通用 NMEA0183 modem 设备驱动，
    对应设备树兼容字符串 :dtcompatible:`gnss-nmea-generic`。

  * 为 Quectel LCX6G 系列 GNSS modem 新增功能完整的设备驱动，
    对应设备树兼容字符串 :dtcompatible:`quectel,lc26g`、
    :dtcompatible:`quectel,lc76g` 和 :dtcompatible:`quectel,lc86g`。

* GPIO

  * Renesas R-Car GPIO 驱动现在支持 Gen4 SoC。
  * 将 ``CONFIG_GPIO_RA`` 重命名为 :kconfig:option:`CONFIG_GPIO_RENESAS_RA`。
  * 新增 GPIO 驱动（:file:`drivers/gpio/gpio_mcux_rgpio.c`）。
    该驱动用于 i.MX93 和 i.MX8ULP。

* I2C

  * :c:func:`i2c_get_config` 现在在 STM32 驱动上受支持。

* I2S

  * STM32H7 设备现在支持 I2S。

* I3C

  * 旧版虚拟寄存器定义从 ``I3C_DCR_I2C_*`` 重命名为 ``I3C_LVR_I2C_*``。

  * 新增在搜索空闲 I3C 地址时指定起始地址的能力。
    这需要 :c:func:`i3c_addr_slots_next_free_find` 的新函数参数。

  * 在 :c:struct:`i3c_msg` 和 :c:struct:`i3c_ccc_taget_payload` 中
    新增名为 ``num_xfer`` 的字段，作为输出指示实际传输的字节数。

  * Cadence I3C 驱动（:file:`drivers/i3c/i3c_cdns.c`）：

    * 新增处理控制器中止的支持，其中目标不为寄存器读取发出数据结束
      但继续发送数据。

    * 更新超时计算，使其与 CPU 速度耦合而非固定重试次数。

  * NXP MCUX I3C 驱动（:file:`drivers/i3c/i3c_mcux.c`）：

    * 修复 ``mcux_i3c_config_get()`` 未向调用者返回配置的问题。

    * 改进 FIFO 读取例程以支持更高速率。

    * 移除自动 IBI 中对 MCTRLDONE 的无限等待。

    * 为 :dtcompatible:`nxp,mcux-i3c` 新增 ``disable-open-drain-high-pp`` 属性，
      允许开路时钟的替代高电平时间。

* IEEE 802.15.4

  * 删除 :kconfig:option:`CONFIG_IEEE802154_SELECTIVE_TXPOWER` Kconfig 选项。

* 输入

  * :dtcompatible:`zephyr,input-longpress` 的 ``short-codes`` 属性
    现在是可选的。节点可以通过仅指定 input 和 long codes 来使用。
  * 新增键盘矩阵驱动支持，包括新的
    :dtcompatible:`gpio-kbd-matrix` 和 :dtcompatible:`input-keymap` 驱动。
    详见 :ref:`gpio-kbd`。
  * 新增一对输入码到 HID 码的转换函数。详见
    :c:func:`input_to_hid_code` 和 :c:func:`input_to_hid_modifier`。
  * 为 :dtcompatible:`gpio-keys` 和 :dtcompatible:`focaltech,ft5336`
    新增电源管理支持。
  * 新增 :dtcompatible:`zephyr,native-linux-evdev` 设备节点，
    用于从 Linux evdev 设备节点获取输入事件。
  * 为 :dtcompatible:`gpio-qdec` 新增光学编码器和电源管理支持。
  * 新驱动 :dtcompatible:`analog-axis`。
  * 新增 ESP32 触摸传感器驱动，包括 :dtcompatible:`espressif,esp32-touch`。

* MDIO

  * 修复 NXP s32 NETC 驱动的初始化优先级。
  * 修复因 MDIO 时钟未初始化导致的 SAM GMAC 传输超时错误。
  * 修复节点状态非 okay 时 ESP32 MDIO 驱动被启用的问题。
  * 在 S32 GMAC 上新增 C22 和 C45 API 支持。
  * 为 NXP ENET 外设新增 MDIO 驱动。
  * 新增 xmc4xxx MDIO 驱动。
  * 修复因 mdio.h 驱动头文件未包含 errno.h 导致的构建错误。

* MFD

  * 新增 :dtcompatible:`maxim,max20335` 的支持。
  * 新增 :dtcompatible:`adi,ad5592` 的支持。
  * 为 :dtcompatible:`nordic,npm1300` 和
    :dtcompatible:`nordic,npm6001` 新增独立的初始化优先级。

* PCIE

  * 通过预先禁用 IO/内存解码修复 MMIO 大小计算。

  * 修改为使用 PNP ID 进行 PRT 检索。

* MEMC

  * 为 NXP FlexRAM 新增驱动。

* MIPI-DBI

  * 引入新的 :ref:`MIPI DBI 驱动类 <mipi_dbi_api>`。

* 引脚控制

  * Renesas R-Car pinctrl 驱动现在支持 Gen4 SoC。
  * 将 ``CONFIG_PINCTRL_RA`` 重命名为 :kconfig:option:`CONFIG_PINCTRL_RENESAS_RA`。
  * Renesas R-Car pinctrl 驱动现在支持 R8A77951 和
    R8A77961 SoC 的电压控制。
  * 新增 ZynqMP / Mercury XU 的驱动。
  * 新增 i.MX8QM/QXP 的驱动。
  * 新增 Renesas RZ/T2M 的驱动。
  * 在 STM32 设备上，当 :kconfig:option:`CONFIG_PM` 启用且
    :kconfig:option:`CONFIG_DEBUG` 禁用时，
    分配给 JTAG/SW 端口的引脚现在可以设置为模拟状态。

* PWM

  * 修复 ESP32S3 低频 PWM 问题。

* 稳压器

  * 新增 API 函数

    * :c:func:`regulator_set_active_discharge`
    * :c:func:`regulator_get_active_discharge`
    * :c:func:`regulator_list_current_limit`

  * ``startup-delay-us`` 和 ``off-on-delay-us`` 现在对所有稳压器受支持。
  * 新增非多线程支持。
  * 新增 :dtcompatible:`maxim,max20335-regulator` 的支持。
  * 为 :dtcompatible:`nxp,pca9420` 新增 ASYS UVLO 配置。
  * 为 :dtcompatible:`renesas,smartbond-regulator` 新增 LDO/DCDC 支持。
  * 为 :dtcompatible:`nordic,npm1300-regulator` 新增 LDO 软启动配置。
  * 修复 :dtcompatible:`x-powers,axp192-regulator` 的初始化优先级。
  * 修复 :dtcompatible:`nordic,npm1300-regulator` 的 LDO GPIO 控制。

* 保留内存

  * 新增用于寄存器的保留内存驱动后端。

  * 保留内存 API 状态从实验性变更为不稳定。

* RTC

  * 新增 Atmel SAM 驱动。

* SMBUS：

  * SMBUS 现在在 STM32 设备上受支持。

* SDHC

  * 为 Cadence SDHC IP 新增 SDHC 驱动。
  * 为 Infineon CAT1 IP 新增 SDHC 驱动。
  * 在 iMX USDHC SDHC 驱动中新增 SDIO 命令支持。

* 传感器

  * 修复 LTRF216A 驱动中的算术溢出。
  * 修复 MAX31865 驱动中的负温度计算。
  * 新增 TI TMAG5273 3D 霍尔传感器驱动。
  * 新增 Vishay VCNL36825T 接近传感器驱动。
  * 新增 BMA4xx 加速度计传感器模拟器。
  * 在 VEML7700 环境光传感器驱动中新增白通道支持。
  * 新增 ST LIS2DE12 加速度计传感器驱动。
  * 新增 Bosch BMP581 压力传感器驱动。
  * 在传感器 shell 中新增触发多个传感器设备的支持。
  * 新增 Aosong AGS10 TVOC 空气质量气体传感器驱动。
  * 扩展 MAX31865 温度传感器驱动以支持运行时更改三线模式。
  * 修复 Bosch BMI160 陀螺仪范围计算并新增属性获取支持。
  * 优化 Bosch BMA4xx 加速度计采样计算，提高精度。
  * 从 TI BQ274xx 电量计驱动中移除浮点算术。
  * 修复 ST 驱动对 HAL_ST 模块的 Kconfig 依赖。
  * 新增 Bosch BMA4xx 加速度计传感器驱动。
  * 新增 ST LIS2DU12 加速度计传感器驱动。
  * 扩展 NTC 热敏电阻驱动以支持 TDK NTCG103JF103FT1。
  * 新增 NXP S32 正交解码器驱动。
  * 修复 LSM6DSV16x 陀螺仪范围表。
  * 修复 ADLTC2990、TSL2540、MAX17055 驱动中缺失的返回值检查。
  * 新增 ST LPS28DFW 压力传感器驱动。
  * 修复 BMI323 驱动中的中断。
  * 为多个 ST 传感器驱动新增设备树属性宏。
  * 新增 Renesas HS300x 温度/湿度传感器驱动。
  * 新增 Gas Sensing Solutions' ExplorIR-M CO2 传感器驱动。
  * 修复 ADXL367 加速度计传感器驱动中的自测试延迟。
  * 新增 ST LPS22DF 压力传感器驱动。
  * 新增流 API 并在 ICM42688 驱动中实现。
  * 在 ADXL367 加速度计传感器驱动中新增触发支持。
  * 在 LSM6DSL 加速度计传感器驱动中新增 PM 挂起和恢复支持。
  * 新增 AMS TSL2561 光传感器驱动。
  * 扩展 BQ274xx 驱动以支持配置和确认化学配置文件。
  * 扩展 LIS2DH 和 LSM6DSV16x 驱动以支持在设备树中配置 INT1/INT2。
  * 在 NPM1300 充电驱动中新增芯片温度测量支持。
  * 新增 ADLTC2990 传感器模拟器。
  * 扩展 MPU6050 驱动以支持 MPU6886 变体。
  * 新增 ADXL367 加速度计传感器驱动。
  * 新增 LiteOn LTR-F216A 照度传感器驱动。
  * 新增 Memsic MC3419 加速度计传感器驱动。
  * 新增 AMD SB 温度传感器驱动。
  * 新增 ESP32S3 内部温度传感器驱动。
  * 新增用于设置 ST 传感器设备树属性的自文档化宏
    （例如 LSM6DSV16X_DT_ODR_AT_60Hz）（:github:`65410`）。

* 串口

  * 新增支持 Renesas RA 和 RZ/T2M 上 UART 的驱动。
  * 为 ITE IT8xxx2 新增更高波特率支持。
  * 新增支持 Intel Lightweight UART 的驱动。
  * 新增 UART 异步 RX 辅助函数。
  * 在 NS16550 驱动上新增异步 API 支持。
  * 更新 ``uart_esp32`` 以使用设备树中的串口端口配置。
  * 新增适配 API，为仅实现异步 API 的驱动提供中断驱动 API。

  * 模拟 UART 驱动（:file:`drivers/serial/uart_emul.c`）：

    * 新增模拟基于中断的 TX。
    * 新增用于测试的模拟错误。
    * 修改为使用本地工作队列进行数据传输。
    * 修改 FIFO 大小及其处理以更接近真实硬件。

  * 在 STM32 设备上，现在可以通过在目标串口节点中设置 ``fifo-enable``
    属性来启用 FIFO，具有以下好处：
    在 TX 中，FIFO 允许以突发模式工作，减轻负载较重应用程序的调度压力。
    它还允许与对帧间延迟变化敏感的 UART 设备更可靠地通信。
    在 RX 中，FIFO 减少溢出发生。

* SPI

  * 在 STM32H7 设备上，``fifo-enable`` 属性允许使用 SPI 块 FIFO。
    该功能仍为实验性，需要进一步成熟。
  * 在受 BSY 位勘误影响的 STM32 设备上，实现了变通方案。

* USB

  * 在 STM2G0 设备上，``clk_hsi48`` 节点中的 ``crs-usb-sof`` 属性
    启用时钟恢复系统支持，实现更稳定的 HSI48 时钟，
    从而增强 USB 连接的鲁棒性。
  * 在兼容的 STM32 设备上，等时端点现在通过双缓冲功能正常工作。
  * 为 DWC2 控制器新增 UDC 驱动。
  * 为 Nuvoton NuMaker 系列 USBD 控制器新增支持。

* W1

  * 新增 1-Wire GPIO 主驱动。详见 :dtcompatible:`zephyr,w1-gpio`
    设备树绑定。

* Wi-Fi

  * 新增 Infineon airoc 驱动。
  * 修复 esp32 驱动。减小最小堆大小，禁用离开时自动重连。
  * 修复 esp_at 驱动。允许无 IPv4 支持构建。被动接收模式修复。依赖 UART 运行时配置。
  * 修复 winc1500 驱动。断开连接时未返回断开结果事件。

网络
**********

* CoAP：

  * 新增 Echo 和 Request-Tag CoAP 选项（RFC 9175）的支持。
  * 将 :c:func:`coap_remove_observer` API 函数的返回类型改为 bool。
  * 引入 CoAP 服务库，简化 CoAP 服务器功能的实现。
  * 更新 CoAP 服务器示例以使用 CoAP 服务库。
  * 为 CoAP 服务器新增 shell 模块。
  * 修复 :c:func:`coap_packet_remove_option` 中的空指针解引用。
  * 使用网络事件子系统新增 CoAP 观察者/服务网络事件。
  * 修改 :c:func:`coap_pending_init` API 函数以接受
    :c:struct:`coap_transmission_parameters` 而非重试次数。
  * 新增 API 函数：

    * :c:func:`coap_get_transmission_parameters`
    * :c:func:`coap_set_transmission_parameters`
    * :c:func:`coap_handle_request_len`
    * :c:func:`coap_well_known_core_get_len`
    * :c:func:`coap_uri_path_match`
    * :c:func:`coap_packet_is_request`
    * :c:func:`coap_find_observer`
    * :c:func:`coap_find_observer_by_token`
    * :c:func:`coap_pendings_count`
    * :c:func:`coap_header_set_code`

* 连接管理器：

  * 新增通用 Wi-Fi 连接后端。

* DHCP：

  * 在初始化网络接口时新增缺失的 DHCPv6 状态结构初始化。
  * DHCP 分配的 IPv4 地址现在在接口 down 时被移除。
  * 新增 DHCPv4 服务器实现。
  * 重新组织 DHCPv4 文件结构。所有 DHCPv4 相关文件现在归组于
    ``subsys/net/lib/dhcpv4`` 中。
  * 将 DHCPv6 文件移至 ``subsys/net/lib/dhcpv6`` 以与 DHCPv4 对齐。

* DNS：

  * 新增在所有网络接口上启用 mDNS 监听器的支持。
  * 在 ``mdns_responder`` 示例中新增 VLAN 支持。
  * 修复 DNS 包上设置的 TTL/跳数限制。
  * 新增 :kconfig:option:`CONFIG_DNS_RESOLVER_AUTO_INIT`，
    允许禁用启动时默认 DNS 上下文的自动初始化。

* 以太网：

  * 现在支持手动注册 ARP 条目。
  * 在设备树中新增 PHY 模式选择。
  * 新增 TX 注入模式支持。

* gPTP：

  * 转发 sync 消息时现在使用本地端口标识。
  * 修复 BMCA 信息的双次转换字节序。
  * GM PRIO 根系统 id 现在始终用于 announce 消息。
  * 创建 gPTP 处理器线程栈大小 Kconfig 选项。
  * 反转出站包的优先级。

* ICMP：

  * 修复接收未处理的 ICMP 消息时发出错误的问题。
  * 修复在未正确设置源 IP 地址时 ICMP Echo Reply 可能被发送的 bug。
  * 修复优先级检查失败时 ICMP Echo Request 处理器中的数据包泄漏。
  * 改进处理邻居发现模块的线程安全性。
  * 新增 IPv6 邻居可达性提示支持，允许减少活跃连接的 ICMPv6 流量。

* IP：

  * 修复支持校验和卸载的接口上 IP 分片包的 L3/L4 校验和计算/验证。
  * 修复 IP 分片包上未设置 net_context 导致发送回调未被调用的问题。
  * 现在可以为单播和多播报包分别设置不同的 IPv4 TTL 值和 IPv6 跳数限制值。
    这可以通过每个 socket 的 :c:func:`setsockopt` API 控制。
  * 改进 IP 协议栈中的源 IP 地址验证。
    从非环回接口上的环回地址收发到的地址将被丢弃。
  * 新增函数用于验证 IPv6 地址是站点本地还是全局。
  * 为 :c:struct:`net_pkt` 结构新增设置对等 IP 地址的支持，
    用于卸载接口。这允许 :c:func:`recvfrom` 在卸载情况下返回有效地址。

* LwM2M：

  * 新增 :kconfig:option:`CONFIG_LWM2M_UPDATE_PERIOD`，
    无论生命周期值如何都配置 LwM2M 更新周期。
  * 修复组合读/写访问权限检查。
  * 新增删除对象和资源实例的 shell 命令。
  * 修复分块传输中分块 ACK 以错误响应码发送的 bug。
  * 修复 LwM2M 版本 1.1 的对象版本报告。
  * 在 LwM2M 引擎中新增 DTLS 连接标识符支持。
  * 新增 LwM2M 服务器禁用可执行资源支持。
  * 实现 LwM2M 服务器选择回退机制，用于注册阶段。
    引擎现在会在当前服务器不可用或被禁用时尝试选择不同服务器。
  * 新增在设置中存储 LwM2M 错误列表的支持。
  * 修复无滴答模式下 pmin 观察者属性处理。
  * 新增通过 ``set_socket_state()`` 回调通知应用程序正在进行的 CoAP 传输的支持。
  * 弃用无符号 64 位整数值类型，因为它在规范中未表示。
    改用有符号 64 位整数。
  * 新增 LwM2M 网关对象回调，允许处理带前缀路径的 LwM2M 消息。
  * 新增 LwM2M 专用宏用于启动时对象初始化。
  * 其他多个小 bug 修复和改进。

* 杂项：

  * 新增使用宏 :c:macro:`NET_MGMT_REGISTER_EVENT_HANDLER`
    进行编译时网络事件处理的支持。
  * 新增 :kconfig:option:`CONFIG_NET_MGMT_EVENT_WORKER` 选项，
    允许使用系统工作队列或同步方式发出网络事件。
  * 删除冗余的网络连接 API 文档页。
  * 改进网络连接子系统的线程安全性。
  * 删除 ``eth_native_posix`` 示例。
  * 从 ``struct net_pkt_cb_ieee802154`` 中删除冗余的 ``arb`` 和 ``fv2015`` 字段。
  * 在网络接口层面引入独立 TX 互斥锁，
    防止对不可重入驱动的并发 TX 访问。
  * 修复环回地址未注册 netmask 的问题。
  * 在 net_context 层面新增绑定到特定网络接口的支持。
  * 新增 IGMPv3 支持。
  * 新增网络事件 ``NET_EVENT_HOSTNAME_CHANGED``，在主机名变更时触发。
  * 重构 net_context 选项 getter/setter 以减少代码重复。
  * 修复 ARP 层面在 ARP 包创建出错时可能泄漏数据包的问题。
  * 新增分析 SNTP 时间不确定性的支持。
  * 修复底层设备未就绪时网络接口仍被启动的问题。
  * 为 dummy 接口新增启动/停止函数。
  * 在文档中新增详细的 :ref:`网络配置 <network_configuration_guide>` 指南。
  * 新增 :kconfig:option:`CONFIG_NET_HOSTNAME_DYNAMIC` 选项，
    允许在运行时设置主机名。

* MQTT-SN：

  * 新增 :c:func:`mqtt_sn_get_topic_name` API 函数。
  * 修复使用通配符订阅时接收 Register 消息的处理。

* OpenThread：

  * 实现以下 OpenThread 平台 API：

    * ``otPlatRadioSetRxOnWhenIdle()``
    * ``otPlatResetToBootloader()``
    * ``otPlatCryptoPbkdf2GenerateKey()``

  * 更新 OpenThread 平台 UART 驱动，使其在启动时不再等待与主机的通信开始。
  * 在 OpenThread 平台中新增 BLE TCAT 实现。
  * 为 OpenThread 的 Crypto PSA 后端新增额外算法。
  * 修复 ``otPlatAssertFail()`` 以打印实际 assert 的位置而非函数本身。

* PPP：

  * 修复接口 down 时 PPP 连接终止的问题。

* Shell：

  * 重构网络 shell 模块，将其从大单文件拆分为按命令划分的子模块。
  * 修复执行环回 ping 时出现意外超时消息的问题。
  * 新增 ``net sockets`` 命令以打印打开的 socket 和 socket 服务的信息。
  * 通过 shell 添加 IPv4/IPv6 多播地址时，如需要则加入 IPv4/IPv6 多播组。
  * 修复 ``tcp connect`` 命令的操作（TCP 上下文过早释放）。
  * 在 telnet shell 后端中新增 Echo 选项支持。
  * 修复 telnet shell 后端中非致命 EAGAIN 或 ENOBUFS 错误时不必要的连接关闭。
  * 修复 ping 回复处理器中的双重包解引用。
  * 修复执行 ``net arp`` 命令时可能的死锁。
  * 为 ``net stats`` 命令新增更详细的以太网统计打印。
  * 新增 ``net dhcpv4 server`` 命令用于 DHCPv4 服务器管理。
  * 新增管理 TLS 凭据的 shell 模块。

* Socket：

  * 新增 v4 映射到 v6 的支持，允许 IPv4 和 IPv6 共享同一端口空间。
  * 新增 :c:macro:`IPV6_V6ONLY` socket 选项支持。
  * 新增 :c:macro:`SO_ERROR` socket 选项支持。
  * 修复 :c:func:`select` 在出错时未设置 ``writefds`` 的问题。
  * 新增对象核心支持，允许跟踪网络 socket 及其统计信息。
  * 新增 :c:func:`recvmsg` 支持。
  * 新增 :c:macro:`IP_PKTINFO` 和 :c:macro:`IPV6_RECVPKTINFO`
    socket 选项支持。
  * 新增 :c:macro:`IP_TTL` socket 选项支持。
  * 新增 IPv4 多播 :c:macro:`IP_ADD_MEMBERSHIP` 和
    :c:macro:`IP_DROP_MEMBERSHIP` socket 选项支持。
  * 新增 IPv6 多播 :c:macro:`IPV6_ADD_MEMBERSHIP` 和
    :c:macro:`IPV6_DROP_MEMBERSHIP` socket 选项支持。
  * 改进 BSD socket API 的 doxygen 文档。
  * 修复 TLS socket 中的 POLLERR 错误报告。
  * 修复 :c:func:`poll` 期间的 DTLS 握手处理。
  * 将 DTLS socket :c:func:`connect` 行为与常规 TLS 对齐（connect 调用期间握手）。
  * 新增 Socket Service 库，允许注册多个基于 socket 的网络服务
    并在单个线程中处理它们。
  * 为 Socket Service 新增 ``echo_service`` 示例。
  * 新增 :c:macro:`SO_DOMAIN` socket 选项支持。
  * 修复使用 :c:func:`poll` 监控 socket 时的 DTLS 连接超时。
  * 修复包 socket 上包环回时空链路层地址指针解引用。
  * 其他多个小 bug 修复和改进。

* TCP：

  * TCP 协议栈现在对关闭端口上的连接尝试回复 RST 包。
  * 修复 :c:func:`accept` 调用中传递的远程地址。
  * 修复主动握手期间的引用计数，防止 TCP 上下文过早释放。
  * 修复 :kconfig:option:`CONFIG_NET_TCP_CONGESTION_AVOIDANCE`
    禁用时的编译问题。
  * 重构 TCP 数据排队 API 以防止 TCP 协议栈溢出 TX 窗口。
  * 修复释放 TCP 上下文时 TCP 工作队列与其他线程之间可能的竞态条件。
  * 修复输入线程与 TCP 工作队列之间可能的竞态条件。
  * 新增 TCP Keep-Alive 功能支持。
  * 修复被动连接关闭期间 TCP 状态机可能卡在 LAST_ACK 状态的 bug。
  * 修复对等方未响应时 TCP 状态机可能卡在 FIN_WAIT_1 状态的 bug。
  * 其他多个小 bug 修复和改进。

* TFTP：

  * 修复复制 TFTP 错误消息时潜在的缓冲区溢出。
  * 改进出错时的日志记录。

* Wi-Fi：

  * 在 Wi-Fi shell 中新增 Wi-Fi 驱动版本信息。
  * 在 Wi-Fi shell 中新增 AP（接入点）模式支持。
  * 新增监管信道信息。
  * 将 Wi-Fi 绑定添加到连接管理器。
  * 修复 Wi-Fi shell。SSID 打印修复。帮助文本修复。信道验证修复。
  * 修复 TWT 功能。拆卸状态未更新。省电修复。

* zperf：

  * 改进 IP 地址绑定。Zperf 现在默认绑定到任意地址，
    并允许通过 Kconfig/API 提供的地址覆盖。
  * 修复传输时的 TCP 包计数。
  * 重构 UDP/TCP 接收以使用 Socket Service 节省内存。
  * 修复中断下载时 zperf 会话泄漏。
  * 修复 Mbps、Kbps 和 bps 之间的计算比例。
  * zperf 示例现在支持将网络代码重定位到 RAM。

USB
***

* 设备支持：

  * 引入新的 USB Audio 2 实现，使用设备树进行实例化，
    将描述符复杂性从应用程序中隐藏。初始实现仅限于全速，
    提供基本隐式和显式反馈所需的最小功能集。
    不支持中断通知。
  * 新增 SetFeature(TEST_MODE) 支持。

设备树
**********

绑定
========

  * 引入新的 SPI 属性 ``spi-cpol``、``spi-cpha`` 和 ``spi-hold-cs``，
    用于宏 :c:macro:`SPI_CONFIG_DT` 在设备树文件中设置 SPI 模式。

库 / 子系统
**********************

* 管理

  * 修复 MCUmgr 镜像管理中的一个问题，其中擦除已擦除的插槽会返回未知错误。
    现在返回成功。

  * 修复 MCUmgr UDP 传输结构体被静态初始化的问题。
    这节省了约 ~5KiB 闪存。

  * 修复 MCUmgr 中的一个问题，其中在仅 IPv4 上启用 UDP 传输
    但内核中启用了 IPv6 支持时会导致用户数据缓冲区溢出。

  * 在 MCUmgr OS 管理组中实现日期时间功能。
    这利用了 RTC 驱动 API。

  * 修复 MCUmgr 控制台 UART 输入中的一个问题，其中 FIFO 在 ISR 之外被读取，
    这在下一个 USB 堆栈中不受支持。

  * 修复 ``mcuboot erase`` DFU shell 命令可用于擦除
    MCUboot 或当前运行应用程序插槽的问题。

  * 修复通过 UDP 传输发送过大消息时错误返回
    :c:enumerator:`MGMT_ERR_EINVAL` 而非 :c:enumerator:`MGMT_ERR_EMSGSIZE` 的问题。

  * 修复在 Direct XIP 模式下确认镜像时，即使从次级插槽执行
    也始终确认主级插槽镜像的问题。现在始终确认当前活动镜像。

  * 新增获取已注册命令组的支持，以支持在运行时注册和注销
    默认命令组，允许应用程序为同一命令组支持多个实现。

  * 修复 MCUmgr FS 管理中的一个问题，其中返回错误时信号量锁不会被释放，
    导致可能的死锁。

  * 新增自定义 payload MCUmgr 处理器的支持。
    可通过 :kconfig:option:`CONFIG_MCUMGR_MGMT_CUSTOM_PAYLOAD` 启用。

  * 修复 MCUmgr 镜像管理中的一个问题，其中向已擦除的插槽发送擦除命令时
    会返回错误。

  * 新增镜像插槽大小检查支持，以确保更新可被 MCUboot 利用。
    这可以通过在同时构建应用程序和 MCUboot 时使用 sysbuild
    并启用 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_TOO_LARGE_SYSBUILD`
    来实现，或通过启用
    :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_TOO_LARGE_BOOTLOADER_INFO`
    使用 MCUboot 的引导加载程序信息共享来实现。

* 日志

  * 新增在基于字典的日志中从二进制中移除字符串字面量的选项。

  * 优化最常见的日志消息（含最多 2 个数值参数的字符串）。
    优化针对代码大小（在 riscv32 上观察到显著收益）和性能。

  * 扩展日志前端 API 以可选实现用于优化消息的专用函数。
    可选 API 通过 :kconfig:option:`CONFIG_LOG_FRONTEND_OPT_API` 启用。

  * 为日志前端新增运行时消息过滤支持。

  * 新增支持多个 UART 日志后端实例的选项。

  * 修复 :kconfig:option:`CONFIG_LOG_PRINTK` 启用时
    :c:func:`printk` 的用户空间问题。

  * 新增对使用字符指针 ``%p`` 的日志消息的编译时检测。
    在基于字典的日志且字符串从二进制中剥离时应避免这种情况。
    检测到错误情况时，用户消息将被替换为建议添加指针转换的错误消息。

  * 删除对 v2 日志的剩余引用。将 :c:func:`log2_generic` 重命名为 :c:func:`log_generic`。

* Modem 模块

  * 在 ``modem_pipe`` 模块中新增 ``TRANSMIT_IDLE`` 事件，
    使用 :c:func:`modem_pipe_transmit()` 将字节放入缓冲区后
    通知用户后端已传输所有字节。
    如果用于动态管理 :c:func:`modem_pipe_transmit()` 调用之间的延迟，
    该事件将大幅提高传输大量数据的效率。

  * 在所有 modem 后端中实现 ``TRANSMIT_IDLE`` 事件。

  * 扩展所有 modem 模块以利用 ``TRANSMIT_IDLE`` 事件
    动态管理 :c:func:`modem_pipe_transmit()` 调用之间的延迟。
    此改进在传输大量连续数据时将系统工作队列利用率降低了 86%，
    同时仅将吞吐量降低了 12%。此优化还允许较低优先级的线程
    （如延迟日志线程）在传输期间运行（之前被
    不间断的 :c:func:`modem_pipe_transmit()` 调用阻塞）。

  * 改进 ``modem_pipe`` 事件分发。``modem_pipe`` 模块现在在
    使用 :c:func:`modem_pipe_attach()` 附加管道时，
    如有数据就绪则每次调用 ``RECEIVE_READY`` 事件，
    并在管道打开或附加时始终调用 ``TRANSMIT_IDLE``。
    这确保 modem 管道模块的事件驱动用户可完全依赖事件来启动读取/传输工作。
    已新增测试套件以补充这些改进。

  * 扩展 ``modem_cmux`` 模块以支持同时作为 DTE（用户应用程序）和 DCE（modem）。
    通过此改进，两个 Zephyr 应用程序可以通过各自的
    ``modem_cmux`` 实例相互通信。

* Picolibc

  * 更新到 1.8.6 版本。这从构建系统中移除了
    :c:macro:`_POSIX_C_SOURCE` 定义，
    因此使用 Zephyr 需求之外 API 的应用程序需要自行添加此定义。

  * 新增 :c:func:`printf` 模式 :kconfig:option:`CONFIG_PICOLIBC_IO_LONG_LONG` 和
    :kconfig:option:`CONFIG_PICOLIBC_IO_MINIMAL`。
    这些为应用程序提供更细粒度的控制，以控制库提供的支持级别
    从而控制文本空间使用。默认情况下，
    基于其他配置参数选择正确的支持级别。

  * 新增 :kconfig:option:`CONFIG_PICOLIBC_ASSERT_VERBOSE`。
    该选项默认关闭，控制 :c:func:`assert` 函数在断言失败时
    是否显示详细信息（包括文件名、行号、函数名和失败表达式文本）。
    保持禁用可节省文本空间。

  * 使用 Picolibc 时现在可以禁用 :kconfig:option:`CONFIG_THREAD_LOCAL_STORAGE`。
    这在诊断使用 Picolibc 时的问题时非常有帮助，
    因为这些问题通常由启用 TLS 引起而非由库本身引起。

  * 库中的多项改进，包括 printf 和 ctype 等领域的代码大小缩减
    以及 math 库中的多个修复。

* 电源管理

  * 引入 Atmel SAM SUPC 函数以允许唤醒源和关机。
  * 通过使用基于 RTC 的空闲计时器（在 cortex systick 关闭时
    跟踪 tick 演进），STM32F4 设备现在支持 stop 模式。

  * :c:func:`pm_device_runtime_put_async()` 新增参数以指定操作的最小延迟。
    这在设备被使用时避免多次状态转换很有用。

  * 挂起或恢复时不需要阻塞的设备现在可以定义为 ISR 安全
    （``PM_DEVICE_ISR_SAFE``）。对于这些设备，Zephyr 能够减少 RAM 消耗，
    且运行时设备电源管理可安全地从中断中使用。

  * 设备运行时电源管理优化。:c:func:`pm_device_runtime_get` 和
    :c:func:`pm_device_runtime_put` 不再等待仍在队列中的挂起操作完成。
    在这种情况下，挂起的工作直接取消并更新设备状态。

  * 新增以下 Kconfig 选项以自定义不同电源域的初始化优先级。

    * :kconfig:option:`CONFIG_POWER_DOMAIN_GPIO_INIT_PRIORITY`
    * :kconfig:option:`CONFIG_POWER_DOMAIN_GPIO_MONITOR_INIT_PRIORITY`
    * :kconfig:option:`CONFIG_POWER_DOMAIN_INTEL_ADSP_INIT_PRIORITY`

* 加密

  * Mbed TLS 更新到 3.5.2。完整发布说明可参见：
    https://github.com/Mbed-TLS/mbedtls/releases/tag/v3.5.2

* 保留

  * 修复 :kconfig:option:`CONFIG_RETENTION_BUFFER_SIZE` 值超过 256 时
    由于使用 8 位变量导致无限循环的问题。

* SD

  * 新增 SDIO 设备支持。

* 存储

  * 文件系统：LittleFS 模块更新到 2.8.1 版本。

  * 以下在 3.2 中标记为弃用的 Flash Map API 宏已被删除：
    ``FLASH_AREA_ID``、``FLASH_AREA_OFFSET``、``FLASH_AREA_SIZE``、
    ``FLASH_AREA_LABEL_EXISTS`` 和 ``FLASH_AREA_DEVICE``。

* POSIX API

  * 完成 ``POSIX_THREADS_EXT``、``XSI_THREADS_EXT``、
    ``POSIX_CLOCK_SELECTION`` 和 ``POSIX_SEMAPHORES`` 选项组的支持。

  * 完成 ``_POSIX_MESSAGE_PASSING`` 和
    ``_POSIX_PRIORITY_SCHEDULING`` 选项的支持。

  * 修复 Coverity-CID 211585、334906、334909 和 340851。

  * 改进 POSIX 文档的结构和准确性。

  * 改进 POSIX Kconfig 选项的导航和组织。

  * 新增使用 pthread_attr_t 分配和释放最多 8 MB 栈的支持。

  * 新增延迟和异步线程取消支持。

  * 新增哲学家就餐示例应用程序。

  * 新增命名信号量支持。

  * 在 Zephyr shell 中新增顶层 ``posix`` 命令。
    POSIX API 的 Zephyr shell 工具可作为子命令添加（例如 ``posix uname -a``）

  * 新增异步线程取消和 ``SIGEV_THREAD``、``CLOCK_REALTIME`` 支持。

  * 新增编译时常量 sysconf() 实现。

* LoRa/LoRaWAN

  * 新增 :kconfig:option:`CONFIG_LORAWAN_REMOTE_MULTICAST`
    LoRaWAN 远程多播支持，为 OTA 固件升级支持做准备。

* ZBus

  * 用信号量替代互斥锁以锁定通道并实现 zbus 操作的最高锁持有者协议（HLP）
    优先级提升。该功能避免优先级反转和抢占，
    使 VDED 投递过程更快更一致。（:github:`63183`）

  * 修复 :c:func:`zbus_chan_add` 和 :c:func:`zbus_chan_rm` 的文档，
    添加超时参数。（:github:`65544`）

  * 修复使用 zbus 时混合 C 和 C++ 文件产生的警告。（:github:`65222`）

  * :c:macro:`ZBUS_CHANNEL_DEFINE` 宏现在与 C++ 兼容。（:github:`65196`）

  * 修复 net buf 池固定定义参数顺序。（:github:`65039`）

  * 重构基准测试示例，添加消息订阅者。（:github:`64524`）

  * 将 ``CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_DYNAMIC`` 和
    ``CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_STATIC`` 重命名为
    :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_BUF_ALLOC_DYNAMIC` 和
    :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_BUF_ALLOC_STATIC`。（:github:`65632`）

HAL
****

* STM32

  * STM32F1 更新到 cube 版本 V1.8.5。
  * STM32F7 更新到 cube 版本 V1.17.1。
  * STM32H7 更新到 cube 版本 V1.11.1。
  * STM32L4 更新到 cube 版本 V1.18.0。
  * STM32U5 更新到 cube 版本 V1.4.0。
  * STM32WBA 更新到 cube 版本 V1.2.0。
  * STM32WB 更新到 cube 版本 V1.18.0。

MCUboot
*******

  * 修复 bootutil 中的兼容扇区检查。

  * 修复保存加密 TLV 不依赖加密启用的 Kconfig 问题。

  * 修复 sysflash include 文件中应用程序缺失条件检查的问题。

  * 修复 boot_serial 中单插槽加密镜像列表支持的问题。

  * 修复使用 tinycrypt 时允许选择 MBEDTLS Kconfig 的问题。

  * 修复 boot_serial 中禁用 echo 命令时缺失响应的问题。

  * 修复 USB 配置不生成可用镜像的问题。

  * 在 bootutil 中为 boot 状态写入新增调试日志。

  * 在 sysbuild 中新增估计镜像开销大小到缓存。

  * 新增固件加载器操作模式，允许使用专用的次级插槽镜像
    来更新主级镜像。

  * 当 USB CDC 串行恢复启用时，如果主线程不可抢占则新增错误。

  * 当 USB CDC 和 console 都启用并设置为同一设备时新增错误。

  * 删除已弃用的 ``CONFIG_ZEPHYR_TRY_MASS_ERASE`` Kconfig 选项。

  * 将 zcbor 更新到 0.8.1 版本并重新生成 boot_serial 文件。

  * 将 IO 函数从 main 移至单独文件。

  * 使 imgtool 的 ``align`` 参数可选。

  * 为 ``mimxrt1010_evk``、``mimxrt1015_evk``、
    ``mimxrt1040_evk``、``lpcxpresso55s06``、``lpcxpresso55s16``、
    ``lpcxpresso55s28``、``lpcxpresso55s36``、``lpcxpresso55s69_cpu0``
    新增 MCUBoot 支持。

  * 新增 :kconfig:option:`CONFIG_MCUBOOT_IMGTOOL_OVERWRITE_ONLY`，
    向 imgtool 传递 --overwrite-only 选项
    以在计算溢出时避免添加 swap 状态区域大小。
    它用于非 swap 更新模式。

  * 本版本中的 MCUboot 版本为 ``2.1.0+0-dev``。

zcbor
*****

zcbor 已从 0.7.0 更新到 0.8.1。
完整发布说明可参见：
https://github.com/zephyrproject-rtos/zcbor/blob/0.8.0/RELEASE_NOTES.md 和
https://github.com/zephyrproject-rtos/zcbor/blob/0.8.1/RELEASE_NOTES.md

亮点：

* 新增无序映射支持。
* 性能改进。
* 生成代码的命名改进。
* Bug 修复。

LVGL
****

LVGL 已从 8.3.7 更新到 8.3.11。
详细发布说明可参见：
https://github.com/zephyrproject-rtos/lvgl/blob/zephyr/docs/CHANGELOG.md

此外，Zephyr 中做了以下变更：

  * 为键盘输入新增 :dtcompatible:`zephyr,lvgl-keypad-input` 兼容字符串。

  * 修复 Zephyr 日志级别未正确映射到 LVGL 日志级别的问题。

  * 修复设置 :kconfig:option:`CONFIG_LV_Z_FULL_REFRESH` 时
    未将 :kconfig:option:`CONFIG_LV_Z_VDB_SIZE` 设置为 100 百分比的问题。

测试与示例
*****************

* :zephyr:board:`native_sim<native_sim>` 已替代 ``native_posix``
  作为默认测试平台。
  ``native_posix`` 仍受支持并用于测试，但将在未来版本中弃用。

* Bluetooth 分离堆栈测试（BT 主机和控制器运行在不同 MCU 中）
  现在基于 :ref:`nrf5340_bsim<nrf5340bsim>` 目标在 CI 中运行。
  基于这些目标的其他多个运行时 AMP 测试已添加到 CI，
  包括 OpenAMP、mbox 和 IPC 驱动/子系统
  以及 logger 多域功能的测试。

* 基于 :ref:`nrf52_bsim<nrf52_bsim>` 目标的运行时 UART 测试已添加到 CI。
  这些包括 nRFx UART 驱动测试和基于 HCI UART 驱动通信的
  主机和控制器在不同设备上的网络化 BT 堆栈测试。

* 修复 :zephyr:code-sample:`smp-svr` 示例中的一个问题，
  其中如果 USB 已初始化，应用程序将无法正确启动。

* 新增 LVGL 示例 :zephyr:code-sample:`lvgl-accelerometer-chart`，
  展示在图表控件中显示实时传感器数据。

* 在 :zephyr:code-sample:`ipm-esp32` 中新增 ESP32-S3 IPM 支持。

* 在 :zephyr:code-sample:`esp32-flash-memory-mapped` 中新增 ESP32 内存映射闪存访问示例。

* 新增 ESP32 PWM 环回测试用例。

* 在 mbox 示例中新增 NXP 开发板 ``MIMXRT1160-EVK``、``MIMXRT1170-EVK``、
  ``MIMXRT1170-EVKB``、``LPCXpresso55S69`` 的支持。

* 为 ``mimxrt11xx_cm7`` 新增示例 ``flexram-magic-addr``，
  展示如何使用 memc flexram 驱动时的 flexram 魔法地址功能。
