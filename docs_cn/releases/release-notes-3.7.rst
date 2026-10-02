:orphan:

.. _zephyr_3.7:

Zephyr 3.7.0
############

我们很高兴宣布 Zephyr 3.7.0 版本的发布。

本版本是最后一个非维护 3.x 版本，因此将是下一个
:ref:`长期支持（LTS）版本 <release_process_lts>`。

本版本的主要增强功能包括：

* 引入全新的、完全 :ref:`重构的硬件模型 <hw_model_v2>`。
  它改变了 Zephyr 中 SoC 和开发板的命名、定义和构建方式。
  更多信息可参见 :ref:`board_porting_guide`。
* 备受期待的 :ref:`HTTP 服务器 <http_server_interface>` 库及相关服务 API，
  允许在 Zephyr 中轻松实现 HTTP/1.1 和 HTTP/2 服务器。
  资源可静态或动态注册，并包含 WebSocket 支持。
* :ref:`POSIX 支持 <posix_support>` 已扩展，
  IEEE 1003-2017 :ref:`系统接口 <posix_system_interfaces_required>`
  的大多数选项获得支持，
  以及 :ref:`PSE51 <posix_aep_pse51>`、
  :ref:`PSE52 <posix_aep_pse52>` 和 :ref:`PSE53 <posix_aep_pse53>`
  所需的大多数选项和选项组。
* Bluetooth 主机扩展了对 Nordic UART Service（NUS）、
  Hands-free Audio Gateway（AG）、
  Advanced Audio Distribution Profile（A2DP）
  和 Audio/Video Distribution Transport Protocol（AVDTP）的支持。
* 传感器抽象模型已重构，采用
  :ref:`先读后解码方法 <sensor-read-and-decode>`，
  比之前的 fetch/get API 支持更多类型的传感器和数据流。
* 新的 :ref:`LLEXT 扩展开发者套件（EDK）<llext_build_edk>`
  使在 Zephyr 中开发并集成自定义扩展更加容易，
  包括在 Zephyr 树之外。
* :zephyr:board:`Native simulator <native_sim>` 现在支持利用
  原生主机网络堆栈，而无需依赖复杂的主机环境设置。
* Trusted Firmware-M（TF-M）2.1.0 和 Mbed TLS 3.6.0 已集成到 Zephyr。
  这两个版本都是 LTS 版本。此外，:ref:`psa_crypto`
  已被采用作为 TinyCrypt 的替代方案，
  提供更强的安全性和性能。
* 新的 :ref:`精确时间协议 <ptp_interface>`（PTP，IEEE 1588）
  实验性实现允许以亚微秒精度跨设备同步时间。
* 新增文档页以帮助开发者为 :ref:`vscode_ide` 和
  :ref:`clion_ide` 设置本地开发环境。

从 Zephyr v3.6.0 迁移到 Zephyr v3.7.0 时所需或建议的变更概述，
可参见单独的 :ref:`迁移指南 <migration_3.7>`。

虽然可参考之前 3.x 版本的发布说明获取完整变更日志，
但自上一个 LTS 版本 Zephyr 2.7.0 以来的其他主要增强和变更包括：

* 新增 Picolibc 作为新的默认 C 库的支持。
* 新增以下类型硬件外设的支持：

  * 1-Wire
  * 电池充电器
  * 蜂窝 Modem
  * 电量计
  * GNSS
  * 硬件自旋锁
  * I3C
  * RTC（实时时钟）
  * SMBus

* 新增片段（snippets）支持。片段是可跨平台使用的通用配置设置。
* 新增可链接可加载扩展（LLEXT）支持。
* 破坏性变更摘要（更多细节请参考之前版本的发布说明和迁移指南）：

  * 所有 Zephyr 公共头文件已移至 :file:`include/zephyr`，
    意味着包含时需以 ``<zephyr/...>`` 为前缀。
  * Pinmux API 已删除。需要使用引脚控制作为替代，
    详见 :ref:`pinctrl-guide`。

  * 以下已弃用或实验性功能已被删除：

    * 6LoCAN
    * civetweb 模块。可参见 Zephyr 3.7 的新 :ref:`http_server_interface`
      作为替代。
    * tinycbor 模块。可使用 zcbor 作为替代。

以下章节按组件列出详细变更。

安全漏洞相关
******************************

本版本解决了以下 CVE：

更详细的信息可参见：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2024-3077 `Zephyr 项目缺陷跟踪器 GHSA-gmfv-4vfh-2mh8
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gmfv-4vfh-2mh8>`_

* CVE-2024-3332  `Zephyr 项目缺陷跟踪器 GHSA-jmr9-xw2v-5vf4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jmr9-xw2v-5vf4>`_

* CVE-2024-4785：保密至 2024-08-07

* CVE-2024-5754：保密至 2024-09-04

* CVE-2024-5931：保密至 2024-09-10

* CVE-2024-6135：保密至 2024-09-11

* CVE-2024-6137：保密至 2024-09-11

* CVE-2024-6258：保密至 2024-09-05

* CVE-2024-6259：保密至 2024-09-12

* CVE-2024-6442：保密至 2024-09-22

* CVE-2024-6443：保密至 2024-09-22

* CVE-2024-6444：保密至 2024-09-22

API 变更
***********

本版本删除的 API
============================

  * 删除了 Bluetooth 子系统特定的调试符号。
    它们已被 Zephyr 日志符号替代。

  * 从 PCIe API 中删除了已弃用的 ``pcie_probe`` 和 ``pcie_bdf_lookup`` 函数。

  * 删除了已弃用的 ``CONFIG_EMUL_EEPROM_AT2X`` Kconfig 选项。

  * 从设备 PM API 中删除了 ``pm_device_state_lock``、
    ``pm_device_state_is_locked`` 和 ``pm_device_state_unlock`` 函数。

  * 删除了已弃用的 MCUmgr 传输 API 函数：``zephyr_smp_rx_req``、
    ``zephyr_smp_alloc_rsp`` 和 ``zephyr_smp_free_buf``。

本版本弃用的 API
==========================

  * Bluetooth 广告选项 :code:`BT_LE_ADV_OPT_USE_NAME` 和
    :code:`BT_LE_ADV_OPT_FORCE_NAME_IN_AD` 现已弃用。
    这意味着以下宏已弃用：

    * :c:macro:`BT_LE_ADV_CONN_NAME`
    * :c:macro:`BT_LE_ADV_CONN_NAME_AD`
    * :c:macro:`BT_LE_ADV_NCONN_NAME`
    * :c:macro:`BT_LE_EXT_ADV_CONN_NAME`
    * :c:macro:`BT_LE_EXT_ADV_SCAN_NAME`
    * :c:macro:`BT_LE_EXT_ADV_NCONN_NAME`
    * :c:macro:`BT_LE_EXT_ADV_CODED_NCONN_NAME`

    应用程序开发者现在需要自行设置广告名称，
    通过更新广告数据或扫描响应数据。

* CAN

  * 弃用 :c:func:`can_calc_prescaler` API 函数，
    因为它允许位速率错误。
    同一网络上节点之间的位速率错误会导致它们在
    帧起始（SOF）同步完成后逐渐偏离，导致总线错误。
  * 弃用 :c:func:`can_get_min_bitrate` 和 :c:func:`can_get_max_bitrate`
    API 函数，改用 :c:func:`can_get_bitrate_min` 和
    :c:func:`can_get_bitrate_max`。
  * 弃用 :c:macro:`CAN_MAX_STD_ID` 和 :c:macro:`CAN_MAX_EXT_ID` 宏，
    改用 :c:macro:`CAN_STD_ID_MASK` 和 :c:macro:`CAN_EXT_ID_MASK`。

* PM

  * 弃用 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_EXCLUSIVE`。
    类似的行为可通过 :kconfig:option:`CONFIG_PM_DEVICE_SYSTEM_MANAGED` 实现。

.. _zephyr_3.7_posix_api_deprecations:

* POSIX API

  * 已弃用的 :c:macro:`PTHREAD_BARRIER_DEFINE` 已删除。
  * 已弃用的 :c:macro:`EFD_IN_USE` 和 :c:macro:`EFD_FLAGS_SET` 已删除。

  * 为使用直接映射到 IEEE 1003.1-2017 选项和选项组的 Kconfig 选项，
    以下 Kconfig 选项已弃用（由以下替代）：

    * :kconfig:option:`CONFIG_EVENTFD_MAX`（:kconfig:option:`CONFIG_ZVFS_EVENTFD_MAX`）
    * :kconfig:option:`CONFIG_FNMATCH`（:kconfig:option:`CONFIG_POSIX_C_LIB_EXT`）
    * :kconfig:option:`CONFIG_GETOPT`（:kconfig:option:`CONFIG_POSIX_C_LIB_EXT`）
    * :kconfig:option:`CONFIG_MAX_PTHREAD_COUNT`（:kconfig:option:`CONFIG_POSIX_THREAD_THREADS_MAX`）
    * :kconfig:option:`CONFIG_MAX_PTHREAD_KEY_COUNT`（:kconfig:option:`CONFIG_POSIX_THREAD_KEYS_MAX`）
    * :kconfig:option:`CONFIG_MAX_TIMER_COUNT`（:kconfig:option:`CONFIG_POSIX_TIMER_MAX`）
    * :kconfig:option:`CONFIG_POSIX_LIMITS_RTSIG_MAX`（:kconfig:option:`CONFIG_POSIX_RTSIG_MAX`）
    * :kconfig:option:`CONFIG_POSIX_CLOCK`（:kconfig:option:`CONFIG_POSIX_CLOCK_SELECTION`、
      :kconfig:option:`CONFIG_POSIX_CPUTIME`、:kconfig:option:`CONFIG_POSIX_MONOTONIC_CLOCK`、
      :kconfig:option:`CONFIG_POSIX_TIMERS` 和 :kconfig:option:`CONFIG_POSIX_TIMEOUTS`）
    * :kconfig:option:`CONFIG_POSIX_FS`（:kconfig:option:`CONFIG_POSIX_FILE_SYSTEM`）
    * :kconfig:option:`CONFIG_POSIX_MAX_FDS`（:kconfig:option:`CONFIG_POSIX_OPEN_MAX` 和
      :kconfig:option:`CONFIG_ZVFS_OPEN_MAX`）
    * :kconfig:option:`CONFIG_POSIX_MAX_OPEN_FILES`（:kconfig:option:`CONFIG_POSIX_OPEN_MAX` 和
      :kconfig:option:`CONFIG_ZVFS_OPEN_MAX`）
    * :kconfig:option:`CONFIG_POSIX_MQUEUE`（:kconfig:option:`CONFIG_POSIX_MESSAGE_PASSING`）
    * :kconfig:option:`CONFIG_POSIX_PUTMSG`（:kconfig:option:`CONFIG_XOPEN_STREAMS`）
    * :kconfig:option:`CONFIG_POSIX_SIGNAL`（:kconfig:option:`CONFIG_POSIX_SIGNALS`）
    * :kconfig:option:`CONFIG_POSIX_SYSCONF`（:kconfig:option:`CONFIG_POSIX_SINGLE_PROCESS`）
    * :kconfig:option:`CONFIG_POSIX_UNAME`（:kconfig:option:`CONFIG_POSIX_SINGLE_PROCESS`）
    * :kconfig:option:`CONFIG_PTHREAD`（:kconfig:option:`CONFIG_POSIX_THREADS`）
    * :kconfig:option:`CONFIG_PTHREAD_BARRIER`（:kconfig:option:`CONFIG_POSIX_BARRIERS`）
    * :kconfig:option:`CONFIG_PTHREAD_COND`（:kconfig:option:`CONFIG_POSIX_THREADS`）
    * :kconfig:option:`CONFIG_PTHREAD_IPC`（:kconfig:option:`CONFIG_POSIX_THREADS`）
    * :kconfig:option:`CONFIG_PTHREAD_KEY`（:kconfig:option:`CONFIG_POSIX_THREADS`）
    * :kconfig:option:`CONFIG_PTHREAD_MUTEX`（:kconfig:option:`CONFIG_POSIX_THREADS`）
    * :kconfig:option:`CONFIG_PTHREAD_RWLOCK`（:kconfig:option:`CONFIG_POSIX_READER_WRITER_LOCKS`）
    * :kconfig:option:`CONFIG_PTHREAD_SPINLOCK`（:kconfig:option:`CONFIG_POSIX_SPIN_LOCKS`）
    * :kconfig:option:`CONFIG_SEM_NAMELEN_MAX`（:kconfig:option:`CONFIG_POSIX_SEM_NAMELEN_MAX`）
    * :kconfig:option:`CONFIG_SEM_VALUE_MAX`（:kconfig:option:`CONFIG_POSIX_SEM_VALUE_MAX`）
    * :kconfig:option:`CONFIG_TIMER`（:kconfig:option:`CONFIG_POSIX_TIMERS`）
    * :kconfig:option:`CONFIG_TIMER_DELAYTIMER_MAX`（:kconfig:option:`CONFIG_POSIX_DELAYTIMER_MAX`）

    请参见 :ref:`POSIX API 迁移指南 <zephyr_3.7_posix_api_migration>`。

  * SPI

  * 已弃用的 :c:func:`spi_is_ready` API 函数已删除。
  * 已弃用的 :c:func:`spi_transceive_async` API 函数已删除。
  * 已弃用的 :c:func:`spi_read_async` API 函数已删除。
  * 已弃用的 :c:func:`spi_write_async` API 函数已删除。

架构
*************

* ARC

  * 为 ARC-V 目标新增 ARC MWDT 工具链支持
  * 为多核目标新增硬件内存屏障 API 支持
  * 如果使用 ARC MWDT 工具链且使用 C++，则默认启用 TLS
  * 修复使用 ARC MWDT 工具链和最小 LibC 时 mbedtls 构建失败的问题，
    原因是标记边界检查接口 C 库扩展支持的宏不正确
  * 修复 ARC MWDT 工具链情况下的设备延迟初始化

* ARM

  * 新增 Cortex-M85 核心的初始支持

* ARM64

  * 在回溯中实现符号名称，通过选择 :kconfig:option:`CONFIG_SYMTAB` 启用

  * 为 Cortex-R82 新增编译器调优

* RISC-V

  * 由故障触发的致命错误消息现在包含被调用者保存寄存器状态。

  * 实现栈展开

    * 可选择帧指针以启用精确栈跟踪，代价是大小略微增加和速度略微降低。

    * 可选择 :kconfig:option:`CONFIG_EXCEPTION_STACK_TRACE_SYMTAB`
      启用符号名称

* Xtensa

  * 新增保存/恢复 HiFi AudioEngine 寄存器的支持。

  * 新增利用 MPU 的支持。

  * 新增自动生成中断处理器的支持。

  * 新增在构建时生成向量表以包含在链接脚本中的支持。

  * 新增 kconfig :kconfig:option:`CONFIG_XTENSA_BREAK_ON_UNRECOVERABLE_EXCEPTIONS`
    以保护使用 break 指令处理不可恢复异常。
    通过此 kconfig 启用 break 指令可能导致无限中断风暴，
    这可能妨碍调试工作。

  * 修复通过系统调用传递第 7 个参数时处理不正确的问题。

  * 修复 :c:func:`arch_user_string_nlen` 访问未映射内存
    导致不可恢复异常的问题。

内核
******

  * 新增 :c:func:`k_uptime_seconds` 函数以简化 ``k_uptime_get() / 1000`` 的使用。

  * 新增 :c:func:`k_realloc`，使用内核堆实现传统 :c:func:`realloc` 语义。

  * 设备现在可以通过启用 :kconfig:option:`CONFIG_DEVICE_DT_METADATA`
    存储设备树元数据（如 nodelabel）。
    该选项在 shell 中可能有用，因为设备可以通过
    :c:func:`device_get_by_dt_nodelabel` 等 API
    使用人类友好的名称获取。

  * 如果关联的设备树节点设置了特殊的 ``zephyr,deferred-init`` 属性，
    任何设备初始化都可以延迟。
    设备可以稍后通过 :c:func:`device_init` 初始化。

  * 静态分配线程栈的声明已更新以利用
    :c:macro:`K_THREAD_STACK_LEN` 用于单线程栈声明和数组线程栈声明。
    这确保所有线程栈的正确对齐。对于用户线程，
    根据架构对齐要求，这可能增加静态分配栈对象的大小。

  * 修复 :c:func:`k_thread_abort`（和 join）中的边缘情况死锁，
    其中 SMP 系统上竞争的 ISR 可能卡在自旋中
    以互相通知被中断的线程。

  * 修复 :kconfig:option:`CONFIG_SCHED_SCALABLE` 和
    :kconfig:option:`CONFIG_SCHED_DEADLINE` 一起使用时
    会损坏调度队列的 bug。

Bluetooth
*********

* 音频

  * 从 :c:struct:`bt_bap_broadcast_assistant_cb.recv_state_removed`
    中删除 ``err``，因为它冗余。

  * broadcast_audio_assistant 示例已重命名为 bap_broadcast_assistant。
    broadcast_audio_sink 示例已重命名为 bap_broadcast_sink。
    broadcast_audio_source 示例已重命名为 bap_broadcast_source。
    unicast_audio_client 示例已重命名为 bap_unicast_client。
    unicast_audio_server 示例已重命名为 bap_unicast_server。
    public_broadcast_sink 示例已重命名为 pbp_public_broadcast_sink。
    public_broadcast_source 示例已重命名为 pbp_public_broadcast_source。

  * CAP Commander 和 CAP Initiator 现在不再需要为
    :code:`BT_CAP_SET_TYPE_AD_HOC` 集发现 CAS。
    这允许应用程序在例如未实现 CAP Acceptor 角色的
    BAP 单播服务器上使用该 API。

* 主机

  * 新增 Nordic UART Service（NUS），通过 :kconfig:option:`CONFIG_BT_ZEPHYR_NUS` 启用。
    该服务暴露声明多个 GATT 服务实例的能力，
    允许将多个串行端点用于不同用途。

  * 实现 Hands-free Audio Gateway（AG），通过 :kconfig:option:`CONFIG_BT_HFP_AG` 启用。
    它作为音频网关设备工作。充当音频网关的典型设备是蜂窝电话。
    它控制设备（Hands-free Unit），即远程音频输入和输出机制。

  * 实现 Advanced Audio Distribution Profile（A2DP）和
    Audio/Video Distribution Transport Protocol（AVDTP）。
    A2DP 通过 :kconfig:option:`CONFIG_BT_A2DP` 启用，
    AVDTP 通过 :kconfig:option:`CONFIG_BT_AVDTP` 启用。
    它们实现了实现单声道、立体声或多声道模式下
    高质量音频内容分发的协议和流程。
    典型用例是从立体声音乐播放器向耳机或扬声器流式传输音乐内容。
    音频数据以适当格式压缩以高效利用有限带宽。

  * 重构数据和命令的传输路径。"BT TX" 线程已删除，
    连同 HCI 片段和 L2CAP 段的缓冲区池。
    与控制器通信现在完全在系统工作队列上下文中进行。

  * :kconfig:option:`CONFIG_BT_PER_ADV_SYNC_TRANSFER_RECEIVER` 和
    :kconfig:option:`CONFIG_BT_PER_ADV_SYNC_TRANSFER_SENDER`
    现在依赖 :kconfig:option:`CONFIG_BT_CONN`，
    因为没有连接时它们无法工作。

  * 改进 :c:func:`bt_foreach_bond` 以支持 Bluetooth Classic 密钥遍历。

* HCI 驱动

  * 完全重新设计 HCI 驱动接口。
    详见 :ref:`migration_3.7` 中的 Bluetooth HCI 章节。
  * 新增 Ambiq Apollo3 Blue 系列的支持。
  * 新增 NXP RW61x 的支持。
  * 新增 Infineon CYW208XX 的支持。
  * 新增 Renesas SmartBond DA1469x 的支持。
  * 删除不再维护的 B91 驱动。
  * 在 mimxrt1170_evkb 和 mimxrt1040_evk 开发板上
    新增 NXP IW612 的支持。
    可通过 :kconfig:option:`CONFIG_BT_NXP_NW612` 启用。

开发板与 SoC 支持
********************

* 新增以下 SoC 系列的支持：

  * 新增 Ambiq Apollo3 Blue 和 Apollo3 Blue Plus SoC 系列的支持。
  * 新增 Synopsys ARC-V RMX1xx 模拟平台的支持。
  * 新增 STM32H7R/S SoC 系列的支持。
  * 新增 NXP mke15z7、mke17z7、mke17z9、MCXNx4x、RW61x 的支持
  * 新增 Analog Devices MAX32 SoC 系列的支持。
  * 新增 Infineon Technologies AIROC™ CYW20829 Bluetooth LE SoC 系列的支持。
  * 新增 MediaTek MT8195 音频 DSP 的支持
  * 新增 Nuvoton Numaker M2L31X SoC 系列的支持。
  * 新增 Microchip PolarFire ICICLE Kit SMP 变体的支持。
  * 新增 Renesas RA8 系列 SoC 的支持。

* 在其他 SoC 系列中做了以下变更：

  * Intel ACE 音频 DSP：使用专用寄存器报告 boot 状态而非任意内存。
  * ITE：重命名所有 ITE SoC 变体的 Kconfig 符号。
  * STM32：在兼容系列上启用 ART Accelerator、I-cache、D-cache 和预取。
  * STM32H5：新增 Stop 模式和 :kconfig:option:`CONFIG_PM` 支持。
  * STM32WL：将 Sub-GHz SPI 频率从 12 降至 8MHz。
  * STM32C0：新增 :kconfig:option:`CONFIG_POWEROFF` 支持。
  * STM32U5：新增 Stop3 模式支持。
  * Synopsys：

    * nsim：将 nsim 平台拆分为 arc_classic（基于 ARCv2 和 ARCv3 ISA）
      和 arc_v（基于 RISC-V ISA）
    * nsim/nsim_hs5x/smp：将系统时钟频率与其他 SMP nSIM 配置对齐

  * NXP IMX8M：新增资源域控制器支持
  * NXP s32k146：将 RTC 时钟源设置为内部振荡器
  * GD32F4XX：修复不正确的 uart4 irq 号。
  * Nordic nRF54L：新增 FLPR（快速轻量级处理器）RISC-V CPU 的支持。
  * Espressif：从所有 ESP32 SoC 变体中移除 idf-bootloader 依赖。
  * Espressif：为 ESP32 SoC 变体新增 Simple boot 支持，
    允许使用单个二进制镜像加载应用程序而无需二级引导加载程序。
  * Espressif：重新设计并优化所有 SoC 的内存映射。
  * LiteX：

    * 新增 :c:func:`sys_arch_reboot()` 的支持。
    * :kconfig:option:`CONFIG_RISCV_ISA_EXT_A` 不再被错误地 y 选择。
  * rp2040：专有 UART 驱动已停用，由 PL011 替代。

  * Renesas RZ/T2M：为系统时钟控制寄存器新增默认值。

* 新增以下开发板的支持：

  * 新增 :zephyr:board:`Ambiq Apollo3 Blue 开发板 <apollo3_evb>` 的支持：``apollo3_evb``。
  * 新增 :zephyr:board:`Ambiq Apollo3 Blue Plus 开发板 <apollo3p_evb>` 的支持：``apollo3p_evb``。
  * 新增 :zephyr:board:`Raspberry Pi 5 开发板 <rpi_5>` 的支持：``rpi_5``。
  * 新增 :zephyr:board:`Seeed Studio XIAO RP2040 开发板 <xiao_rp2040>` 的支持：``xiao_rp2040``。
  * 新增 :zephyr:board:`Mikroe RA4M1 Clicker 开发板 <mikroe_clicker_ra4m1>` 的支持：``mikroe_clicker_ra4m1``。
  * 新增 :zephyr:board:`Arduino UNO R4 WiFi 开发板 <arduino_uno_r4>` 的支持：``arduino_uno_r4_wifi``。
  * 新增 :zephyr:board:`Renesas EK-RA8M1 开发板 <ek_ra8m1>` 的支持：``ek_ra8m1``。
  * 新增 :zephyr:board:`ST Nucleo H533RE <nucleo_h533re>` 的支持：``nucleo_h533re``。
  * 新增 :zephyr:board:`ST STM32C0116-DK Discovery Kit <stm32c0116_dk>` 的支持：``stm32c0116_dk``。
  * 新增 :zephyr:board:`ST STM32H745I Discovery <stm32h745i_disco>` 的支持：``stm32h745i_disco``。
  * 新增 :zephyr:board:`ST STM32H7S78-DK Discovery <stm32h7s78_dk>` 的支持：``stm32h7s78_dk``。
  * 新增 :zephyr:board:`ST STM32L152CDISCOVERY 开发板 <stm32l1_disco>` 的支持：``stm32l152c_disco``。
  * 新增 :zephyr:board:`ST STEVAL STWINBX1 开发套件 <steval_stwinbx1>` 的支持：``steval_stwinbx1``。
  * 新增 NXP 开发板的支持：``frdm_mcxn947``、``ke17z512``、``rd_rw612_bga``、``frdm_rw612``、``frdm_ke15z``、``frdm_ke17z``
  * 新增 :zephyr:board:`Synopsys ARC-V RMX1xx nSIM 基于模拟平台 <nsim_arc_v>` 的支持：``nsim_arc_v/rmx100``。
  * 新增 :zephyr:board:`Analog Devices MAX32690EVKIT <max32690evkit>` 的支持：``max32690evkit``。
  * 新增 :zephyr:board:`Analog Devices MAX32680EVKIT <max32680evkit>` 的支持：``max32680evkit``。
  * 新增 :zephyr:board:`Analog Devices MAX32672EVKIT <max32672evkit>` 的支持：``max32672evkit``。
  * 新增 :zephyr:board:`Analog Devices MAX32672FTHR <max32672fthr>` 的支持：``max32672fthr``。
  * 新增 :zephyr:board:`Analog Devices MAX32670EVKIT <max32670evkit>` 的支持：``max32670evkit``。
  * 新增 :zephyr:board:`Analog Devices MAX32655EVKIT <max32655evkit>` 的支持：``max32655evkit``。
  * 新增 :zephyr:board:`Analog Devices MAX32655FTHR <max32655fthr>` 的支持：``max32655fthr``。
  * 新增 :zephyr:board:`Analog Devices AD-APARD32690-SL <apard32690>` 的支持：``ad_apard32690_sl``。
  * 新增 :zephyr:board:`Infineon Technologies CYW920829M2EVK-02 <cyw920829m2evk_02>` 的支持：``cyw920829m2evk_02``。
  * 新增 :zephyr:board:`Nuvoton Numaker M2L31KI 开发板 <numaker_m2l31ki>` 的支持：``numaker_m2l31ki``。
  * 新增 :zephyr:board:`Espressif ESP32-S2 DevKit-C <esp32s2_devkitc>` 的支持：``esp32s2_devkitc``。
  * 新增 :zephyr:board:`Espressif ESP32-S3 DevKit-C <esp32s3_devkitc>` 的支持：``esp32s3_devkitc``。
  * 新增 :zephyr:board:`Espressif ESP32-C6 DevKit-C <esp32c6_devkitc>` 的支持：``esp32c6_devkitc``。
  * 新增 :zephyr:board:`Waveshare ESP32-S3-Touch-LCD-1.28 <esp32s3_touch_lcd_1_28>` 的支持：``esp32s3_touch_lcd_1_28``。
  * 新增 :zephyr:board:`M5Stack ATOM Lite <m5stack_atom_lite>` 的支持：``m5stack_atom_lite``。
  * 新增 :zephyr:board:`CTHINGS.CO Connectivity Card nRF52840 <ctcc>` 的支持：``ctcc``。

* 为开发板做了以下变更：

  * 在 :zephyr:board:`ST STM32H7B3I Discovery Kit <stm32h7b3i_dk>`：``stm32h7b3i_dk`` 上，
    启用完整缓存管理、Chrom-ART、双帧缓冲和完整刷新
    以获得最佳 LVGL 性能。
  * 在 ST STM32 开发板上，stm32cubeprogrammer runner 现在可以使用
    ``--extload`` 选项编程外部闪存。
  * 为所有 NXP 开发板新增 HEX 文件支持 Linkserver。
  * 更新 Linkserver west runner 以反映 LinkServer v1.5.xx CLI 的变更。
  * 为 NXP ``mimxrt1010_evk``、``mimxrt1160_evk``、``frdm_rw612``、``rd_rw612_bga``、``frdm_mcxn947`` 新增 LinkServer 支持。
  * 引入模拟的 :ref:`nrf54l15bsim<nrf54l15bsim>` 目标。
  * nrf5x bsim 目标现在支持 BT LE Coded PHY。
  * 在 native_sim 中添加支持的同时重构了 LLVM 模糊测试支持。
  * nRF54H20 PDK（预发布）转换为 :zephyr:board:`nrf54h20dk`。
  * :zephyr:board:`nrf54h20dk` 中的 PPR 核心目标默认从 RAM 运行。
    引入新的 ``xip`` 变体，从 MRAM（XIP）运行。
  * 重构 :zephyr:board:`beagleconnect_freedom` 外部天线开关处理。
  * 为 nRF5340 Audio DK 新增 Arduino dts 节点标签。
  * 将 nRF54L15 PDK 的默认修订版本从 0.2.1 更改为 0.3.0。
  * 在基于 nRF5340 SoC 的开发板中，
    用使用 on-off 管理器跟踪网络核心使用并暴露其 API
    的模块替代对控制网络核心 Force-OFF 信号的寄存器的直接访问，
    该 API 在 ``<nrf53_cpunet_mgmt.h>`` 中。
  * Laird Connectivity 开发板重新品牌为 Ezurio。

* 新增以下扩展板的支持：

  * :ref:`adafruit_2_8_tft_touch_v2`（``adafruit_2_8_tft_touch_v2``）
  * :ref:`adafruit_neopixel_grid_bff`（``adafruit_neopixel_grid_bff``）
  * :ref:`arduino_uno_click`（``arduino_uno_click``）
  * :ref:`dvp_fpc24_mt9m114`（``dvp_fpc24_mt9m114``）
  * :ref:`lcd_par_s035`（``lcd_par_s035``）
  * :ref:`mikroe_weather_click`（``mikroe_weather_click``）
  * :ref:`nxp_btb44_ov5640`（``nxp_btb44_ov5640``）
  * :ref:`reyax_lora`（``reyax_lora``）
  * :ref:`rk043fn02h_ct`（``rk043fn02h_ct``）
  * :ref:`rk043fn66hs_ctg`（``rk043fn66hs_ctg``）
  * :ref:`rpi_pico_uno_flexypin`（``rpi_pico_uno_flexypin``）
  * :ref:`seeed_xiao_expansion_board`（``seeed_xiao_expansion_board``）
  * :ref:`seeed_xiao_round_display`（``seeed_xiao_round_display``）
  * :ref:`sparkfun_carrier_asset_tracker`（``sparkfun_carrier_asset_tracker``）
  * :ref:`st_b_lcd40_dsi1_mb1166`（``st_b_lcd40_dsi1_mb1166``）
  * :ref:`waveshare_epaper`（``waveshare_epaper``）
  * :ref:`x_nucleo_bnrg2a1`（``x_nucleo_bnrg2a1``）

构建系统与基础设施
*******************************

  * 新增 CI 启用的黑盒测试以验证大多数 Twister 标志的正确性。

  * 为应用程序引入 ``socs`` 文件夹，允许 Kconfig 片段和设备树 overlay
    应用于使用特定 SoC 和开发板限定符的任何开发板目标（:github:`70418`）。
    同时为 sysbuild 新增支持（:github:`71320`）。

  * 新增 :ref:`开发板/SoC 刷写配置 <flashing-soc-board-config>` 设置
    （:github:`69748`）。

  * 弃用全局 CSTD cmake 属性，改用 :kconfig:option:`CONFIG_STD_C`
    选项选择 C 标准版本。此外，子系统可选择最低
    所需 C 标准版本，例如 :kconfig:option:`CONFIG_REQUIRES_STD_C11`。

  * 修复使用 sysbuild 时向应用程序传递 UTF-8 配置的问题（:github:`74152`）。

  * 修复 sysbuild 项目中 domain 文件在 sysbuild 配置变更后
    直接使用 ``west flash`` 时以过时信息加载和使用的问题
    （:github:`73864`）。

  * 修复 Zephyr 模块在未设置 Kconfig 文件时
    未在 sysbuild 中列出的问题（:github:`72070`）。

  * 新增 sysbuild ``SB_CONFIG_COMPILER_WARNINGS_AS_ERRORS`` Kconfig 选项，
    如果设置则为所有镜像启用"警告作为错误"工具链标志（:github:`70217`）。

  * 修复项目中使用的文件（例如设备树 overlay 或 Kconfig 片段）
    未被正确监视且 CMake 在文件变更时不重新配置的问题
    （:github:`74655`）。

  * 为 LinkServer runner 新增 Intel Hex 文件的闪存支持。

  * 新增 sysbuild ``sysbuild/CMakeLists.txt`` 入口点
    并新增 ``APPLICATION_CONFIG_DIR`` 支持
    以调整 sysbuild 功能（:github:`72923`）。

  * 修复 armfvp 查找路径包含冒号分隔列表时的问题（:github:`74868`）。

  * 修复 version.cmake 字段大小未强制的问题（:github:`74357`）。

  * 修复 sysbuild 在处理镜像前未清除 ``EXTRA_CONF_FILE``
    导致该选项无法传递到镜像的问题（:github:`74082`）。

  * 新增 sysbuild root 支持，其工作方式类似于现有 root 模块，
    调整相对于 ``APP_DIR`` 的路径（:github:`73390`）。

  * 为缺失的 blob 新增警告/错误消息（:github:`73051`）。

  * 修复某些系统上正确 python 可执行文件检测的问题（:github:`72232`）。

  * 新增为整个应用启用 LTO 的支持（:github:`69519`）。

  * 修复 ``FILE_SUFFIX`` 问题，涉及后缀双重应用、
    sysbuild 中未应用以及 CMake 函数中的变量名冲突
    （:github:`70124`、:github:`71280`）。

  * 新增使用 :kconfig:option:`CONFIG_SIZE_OPTIMIZATIONS_AGGRESSIVE`
    支持新的激进大小优化标志（适用于 GCC 和 Clang）（:github:`70511`）。

  * 修复 ``BUILD_VERSION`` 为空时打印的问题（:github:`70970`）。

  * 修复 sysbuild 中 ``sysbuild_cache_set()`` cmake 函数
    错误检测部分匹配以用于去重的问题（:github:`71381`）。

  * 修复检测错误 ``VERSION`` 文件的问题（:github:`71385`）。

  * 新增使用 :kconfig:option:`CONFIG_OUTPUT_DISASSEMBLY_WITH_SOURCE`
    禁用包含源代码的反汇编输出的支持（:github:`71535`）。

  * Twister 现在支持 ``--flash-before`` 参数，
    允许在打开串行端口前刷写 DUT（:github:`47037`）。

驱动与传感器
*******************

* ADC

  * 新增 ``ADC_DT_SPEC_*BY_NAME()`` 宏以通过名称从 DT 获取 ADC IO 通道信息。
  * 新增电压偏置支持：

    * 新增 :kconfig:option:`CONFIG_ADC_CONFIGURABLE_VBIAS_PIN`，
      由支持电压偏置的驱动选择。
    * 在 adc-controller 基础绑定中新增 ``zephyr,vbias-pins`` 属性
      以描述电压偏置引脚。
    * 在 TI ADC114s08 ADC 驱动中实现。
  * 示例变更

    * 将现有 ADC 示例重命名为 adc_dt。
    * 新增名为 adc_sequence 的示例，展示更多运行时
      :c:struct:`adc_sequence` 功能。
  * 新 ADC 驱动

    * 新增 ENE KB1200 的驱动。
    * 新增 NXP GAU ADC 的驱动。
  * ADI AD559x 变更

    * 新增对 ADI ad5593 的支持。
    * 为 ADI ad559x 新增 I2C 总线支持。
    * 为 ad559x 新增内部参考电压值配置
      以支持 :c:func:`adc_raw_to_millivolts()` 的调用。
    * 修复 ad559x 驱动中因 :kconfig:option:`CONFIG_THREAD_NAME`
      可用性导致的初始化不当操作问题。
    * 改进 ad559x 驱动中的 ADC 读取效率和验证。
  * ESP32 变更

    * 更新 ESP32 ADC 驱动以与 hal_espressif 版本 5.1 配合工作。
    * 为 ESP32S3 和 ESP32C3 新增 DMA 模式操作支持。
  * nRF 变更

    * 在 nrfx_saadc 驱动中新增 nRF54L15 和 nRF54H20 的支持。
    * 通过在不使用的通道上禁用突发模式改进 nRF SAADC 驱动，避免冻结。
    * 修复 ``adc_nrfx_saadc.c`` 设备驱动中
      单端模式下允许负 ADC 读数的 bug。
      注意此修复由于硬件限制阻止 nRF54H 和 nRF54L 系列
      执行 8 位分辨率单端读数。
  * NXP LPADC 变更

    * 在 NXP LPADC 驱动中启用采集时间功能。
    * 为 NXP LPADC 新增稳压器输出作为参考的支持。
    * 在 ``nxp,lpc-lpadc`` 绑定中将 phandle 类型 DT 属性
      ``nxp,reference-supply`` 更改为 phandle-array 类型 DT 属性
      ``nxp,references``。NXP LPADC 驱动现在支持使用
      ``nxp,references`` 传递参考电压值。
  * Smartbond 变更

    * 为 Smartbond SDADC 和 GPADC 驱动新增电源管理支持。
    * 修复 Smartbond ADC 驱动中 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME` 的支持。
  * STM32 变更

    * 修复 STM32 ADC 驱动中 DMA 支持的多个问题。
    * 新增 STM32H7R/S 系列的支持。
  * 其他驱动变更

    * 在 numaker ADC 驱动中新增 Nuvoton m2l31x 的支持。
    * 修复 ads1119 驱动中配置寄存器访问的问题。
    * 修复 kb1200 驱动中静态分析发现的未初始化值。
    * 修复 tla2021 驱动中 :c:func:`adc_raw_to_millivolts`
      返回实际电压一半的问题，通过更正参考电压值。


  * 新增 Nuvoton Numaker M2L31X 系列的支持。

* 电池

  * 在 ``battery`` 绑定中新增 ``re-charge-voltage-microvolt`` 属性。
    这允许设置自动重新开始充电的限制。

* 电池备份 RAM

  * 新增 STM32G0 和 STM32H5 系列的支持。

* CAN

  * 扩展自动采样点定位支持以覆盖 :c:func:`can_calc_timing` 和
    :c:func:`can_calc_timing_data`。
  * 为 CAN 收发器新增可选 ``min-bitrate`` 设备树属性。
  * 新增设备树宏 :c:macro:`DT_CAN_TRANSCEIVER_MIN_BITRATE` 和
    :c:macro:`DT_INST_CAN_TRANSCEIVER_MIN_BITRATE`
    用于获取 CAN 收发器的最小支持位速率。
  * 新增在内部 ``CAN_DT_DRIVER_CONFIG_GET`` 和
    ``CAN_DT_DRIVER_CONFIG_INST_GET`` 宏中
    指定 CAN 控制器支持的最小位速率的支持。
  * 新增 :c:func:`can_get_bitrate_min` 和 :c:func:`can_get_bitrate_max`
    用于获取给定 CAN 控制器/CAN 收发器组合的最小和最大支持位速率，
    反映获取位速率限制不再可能失败。
    弃用现有的 :c:func:`can_get_max_bitrate` API 函数。
  * 更新 CAN 时序函数以在验证位速率时考虑最小支持位速率。
  * 使 ``sample-point`` 和 ``sample-point-data`` 设备树属性可选。
  * 将 :c:struct:`can_driver_config` 的 ``bus_speed`` 和
    ``bus_speed_data`` 字段重命名为 ``bitrate`` 和 ``bitrate_data``。
  * 新增 :dtcompatible:`nordic,nrf-can` 的驱动。
  * 在 :dtcompatible:`nuvoton,numaker-canfd` 驱动中
    为 Numaker M2L31X 新增驱动支持。
  * 新增主机通信测试套件。

* 充电器

  * 在 ``maxim,max20335-charger`` 中新增 ``chgin-to-sys-current-limit-microamp`` 属性。
  * 在 ``maxim,max20335-charger`` 中新增 ``system-voltage-min-threshold-microvolt`` 属性。
  * 在 ``maxim,max20335-charger`` 中新增 ``re-charge-threshold-microvolt`` 属性。
  * 在 ``maxim,max20335-charger`` 中新增 ``thermistor-monitoring-mode`` 属性。

* 时钟控制

  * 为 STM32H5 系列新增 Microcontroller Clock Output（MCO）支持。
  * 为 STM32WL 系列新增 MSI 时钟支持。
  * 新增 Analog Devices MAX32 SoC 系列的驱动。
  * 新增 Nuvoton Numaker M2L31X 系列的支持。
  * 重构 ESP32 时钟控制驱动以支持 ESP32-C6。
  * 在 LiteX（:file:`drivers/clock_control/clock_control_litex.c`）中
    为 :c:func:`litex_clk_get_duty_cycle()` 和
    :c:func:`litex_clk_get_clkout_divider` 新增返回码检查。

* 计数器

  * 新增 Ambiq Apollo3 系列的支持。
  * 新增 STM32H7R/S 系列的支持。
  * 为 NXP MCXN947 新增 LPTMR 驱动
  * 在 ``nxp,lptmr`` 绑定中新增 ``resolution`` 属性
    以表示 LPTMR 外设用于其计数器的最大位宽。

* DAC

  * 新增 NXP RW SoC 系列 DAC（:dtcompatible:`nxp,gau-dac`）的支持。
  * 新增 Analog Devices AD5691 / AD5692 / AD5693 DAC 的支持
    （:dtcompatible:`adi,ad5691`、:dtcompatible:`adi,ad5692`
    和 :dtcompatible:`adi,ad5693`）。
  * 新增 Texas Instruments DACx0501 系列 DAC 的支持（:dtcompatible:`ti,dacx0501`）。

* 磁盘

  * 在 STM32 SD 驱动中新增 eMMC 设备支持。
    可通过 :kconfig:option:`CONFIG_SDMMC_STM32_EMMC` 启用。
  * 新增环回磁盘驱动，以暴露由文件支持的磁盘设备。
    可使用 :c:func:`loopback_disk_access_register`
    将文件注册到环回磁盘驱动。
  * 新增 :c:macro:`DISK_IOCTL_CTRL_INIT` 和
    :c:macro:`DISK_IOCTL_CTRL_DEINIT` 宏的支持，
    允许在运行时初始化和去初始化磁盘。
    这允许可热插拔磁盘设备（如 SD 卡）在运行时移除和重新插入。
  * 为 STM32H5 系列新增 SDMMC 支持。

* 显示

  * 所有树内支持 :ref:`mipi_dbi_api` 的显示
    已转换为使用它。基于 GC9X01X、UC81XX、SSD16XX、ST7789V、ST7735R 的
    显示已转换到此 API。使用这些显示的开发板
    需要更新其设备树，详见
    :ref:`migration_3.7` 中的显示章节示例。
  * 新增 ST7796S 显示控制器的驱动（:dtcompatible:`sitronix,st7796s`）
  * 在 ILI9XXX 显示驱动中新增 :c:func:`display_read` API 支持，
    可通过 :kconfig:option:`CONFIG_ILI9XXX_READ` 启用
  * 在 SSD16XXX 显示驱动中新增 :c:func:`display_set_orientation` API 支持
  * 新增 NT35510 MIPI-DSI 显示控制器的驱动
    （:dtcompatible:`frida,nt35510`）
  * 新增将 LED 灯带设备抽象为显示的驱动
    （:dtcompatible:`led-strip-matrix`）
  * 在 NXP eLCDIF 驱动中新增 :c:func:`display_set_pixel_format` API 支持。
    支持 ARGB8888、RGB888 和 BGR565 格式。
  * 在 SSD1306 驱动中新增运行时颜色反转支持，
    通过 :c:func:`display_set_pixel_format` API。
  * 现在可以在 ST7789V 驱动中禁用反转模式
    （:dtcompatible:`sitronix,st7789v`），使用 ``inversion-off`` 属性。
  * 新增 NXP MCXNx4x 的支持

* DMA

  * 错误回调配置重命名以更好地指示启用/禁用状态
  * 新增 NXP MCXN947 的支持

* DMIC

  * 新增 NXP ``rd_rw612_bga`` 的支持

* 熵

  * 新增 STM32H7R/S 系列的支持。

* EEPROM

  * 为 :dtcompatible:`zephyr,i2c-target-eeprom` 新增指定 ``address-width`` 的属性。

* eSPI

  * 重命名 eSPI 虚拟线方向宏、枚举值和 Kconfig
    以匹配 eSPI 1.5 规范中的新术语。

* 以太网

  * 引入 :kconfig:option:`CONFIG_ETH_DRIVER_RAW_MODE`。
    该选项允许在不使用 zephyr L2 以太网层的情况下构建以太网驱动。
  * 删除 ethernet-fixed-link DT 绑定。
  * 从以太网驱动中删除 VLAN 处理，
    因为它现在由通用以太网 L2 代码处理。
  * 在 eth_mcux、eth_nxp_enet 和 eth_nxp_s32_gmac、eth_stm32
    以及 eth_nxp_s32_netc 驱动中实现/重构硬件 MAC 地址过滤。
  * 新驱动

    * 为 NXP MCXN SoC 上存在的以太网控制器新增 eth_nxp_enet_qos 驱动。
    * 新增 adin1100 phy 的支持。
    * 新增 Realtek RTL8211F phy 的支持。
  * NXP ENET 驱动变更

    * eth_nxp_enet 驱动不再为实验性。
    * 弃用 eth_mcux 驱动。
    * 所有具有 :dtcompatible:`nxp,kinetis-ethernet` 兼容节点的开发板和 SoC
      重构为使用新的 :dtcompatible:`nxp,enet` 绑定。
    * 在 Kinetis 平台上为 nxp_enet 驱动新增网络设备电源管理支持。
    * 将 eth_nxp_enet 驱动转换为使用内核管理的专用工作队列
      进行 RX，而非手动无限循环。
    * 在 eth_nxp_enet 中启用 IPV6 时禁用硬件校验和加速，
      因为硬件不支持加速 ICMPv6 校验和。
    * 新增 :dtcompatible:`nxp,enet1g` 的支持。
    * 新增在某些平台上为 nxp_enet MAC 使用融合 MAC 地址的支持。
    * 修复使用 nxp_enet 驱动时 LAA 位未设置
      以及 nxp,unique-mac 属性描述令人困惑的问题。
    * 修复在 nxp_enet 驱动中使用非缓存 DMA 缓冲区时
      缓存维护被启用的问题。
    * 为 nxp_enet 驱动新增 MMIO 映射。
    * 明确 eth_nxp_enet 支持的 DSA。
  * NXP S32 以太网变更

    * eth_nxp_s32_gmac 驱动现在隐含 :kconfig:option:`CONFIG_MDIO`。
    * eth_nxp_s32_netc 驱动更新为使用新的 MBOX API。
  * Adin2111 驱动变更

    * 更正 adin2111 驱动中 IAMSK1 TX_READY_MASK 的位域位置。
    * 修改 adin2111 驱动始终在帧末尾附加 crc32。
    * 调整 eth_adin2111 驱动具有适当的多播器过滤掩码。
    * 修复 adin2111 驱动的"无 crc8 的通用 SPI"模式。
    * 为 adin2111 驱动新增 Open Alliance SPI 协议支持。
    * 为 adin2111 驱动新增自定义驱动扩展 API。
    * 在 adin2111 驱动中启用混杂模式支持。
    * 将 OA 缓冲区从 adin2111 驱动的设备数据中移出，
      使用通用 SPI 协议时节省约 32KB 空间。
    * 修复 eth_adin2111 驱动在 64 位平台上的构建警告。
    * adin2111 驱动的多个小变更。
  * STM32 以太网驱动变更

    * 为兼容 STM32 系列（STM32F7、STM32H5 和 STM32H7）新增 PTP 支持。
    * 修改 eth_stm32 使用 phy API 访问 phy
      以避免多任务时的冲突。
    * 从 STM32 F4、F7 和 H7 系列中删除旧版 STM32Cube HAL API 支持。
    * 在 eth_stm32_hal 驱动中新增 RX/TX 时间戳支持。
  * ESP32 以太网驱动变更

    * 在 esp32 以太网驱动中新增运行时设置 MAC 地址的支持。
    * 更新 esp32 以太网驱动以与 hal_espressif 版本 5.1 配合工作。
    * 修复 :kconfig:option:`CONFIG_NET_STATISTICS` 启用时
      esp32 以太网驱动的构建。
    * 修复 ESP32 以太网驱动未通过 GPIO 正确为外部 PHY 时钟的问题。
  * 其他以太网驱动变更

    * 在 w5500 以太网驱动中新增链路状态检测，可通过 Kconfig 配置。
    * 在 eth_liteeth 驱动中新增运行时设置 MAC 地址的能力。
    * 修复 eth_stellaris 驱动中的问题，
      之前未考虑驱动接收的中断数可能少于
      以太网控制器接收的数据包数。
    * 为 enc28j60 新增设置 RX 过滤器的设备树属性。
    * 修复 enc28j60 驱动中出错时 ESTAT TXABRT 位未清除的问题。
    * 在 PTP 子系统启用时，
      为 native_posix 以太网驱动的 ptp_clock 驱动实现
      新增启用条件。
    * 修复 KSZ8xxx 的 DSA 驱动以正确初始化 LAN 设备。
    * 修复 ksz8863 中尾部标签启用使用错误寄存器地址的问题。
  * Phy 驱动变更

    * 修复 KSZ8081 phy 驱动中关于复位、自动协商、
      链路检测和缺失/刷屏日志消息的多个控制问题。
    * 更改 KSZ8081 DT 绑定中复位和中断 gpios 的属性名。
    * 修复 phy_mii 驱动在使用 fixed-link 模式时的总线故障。

* 闪存

  * 新增 Ambiq Apollo3 系列的支持。
  * 新增 SPI NOR 驱动（spi_nor.c）多实例支持。
  * 通过引入设备能力到 :c:struct:`flash_parameters`
    和工具函数 :c:func:`flash_params_get_erase_cap`
    新增非擦除设备的初步支持，
    该函数允许获取设备提供的擦除类型；
    新增 :c:macro:`FLASH_ERASE_C_EXPLICIT`，
    目前是唯一支持的擦除类型，由所有闪存设备设置。
  * 新增 :c:func:`flash_flatten` 函数，可用于设备，
    无论是否有擦除要求，当擦擦除用于
    从该设备移除/扰乱数据而非为随机数据写入准备设备时。
  * 新增 :c:func:`flash_fill` 工具函数，
    允许在选定设备中的提供范围内写入单个值。
  * 在 nrf54l15 设备上新增 RRAM 支持。
  * 在 STM32 OSPI 驱动中新增非忙等待轮询支持。
  * 新增 STM32 XSPI 外部 NOR 闪存驱动的支持（:dtcompatible:`st,stm32-xspi-nor`）。
  * 在 STM32 OSPI、QSPI 和 XSPI 驱动中
    新增外部 NOR 闪存上的 XIP 支持。
  * STM32 OSPI 驱动：clk、dqs、ncs 端口现在可通过设备树配置
    （参见 :dtcompatible:`st,stm32-ospi`）。
  * 为 NXP MCXN947 新增 FlexSPI 支持
  * 新增 Nuvoton Numaker M2L31X 系列的支持。

* 电量计

  * max17048：将电压单位从 mV 更正为 uV。

* GNSS

  * 新增 GNSS 设备驱动 API 测试套件。
  * 新增 u-blox UBX 协议的支持。
  * 新增 u-blox M8 GNSS modem 的设备驱动（:dtcompatible:`u-blox,m8`）。
  * 新增 Luatos Air530z GNSS modem 的设备驱动（:dtcompatible:`luatos,air530z`）。

* GPIO

  * 新增 Ambiq Apollo3 系列的支持。
  * 新增 Broadcom Set-top box（brcmstb）SoC GPIO 驱动。
  * 新增 :c:macro:`STM32_GPIO_WKUP` 标志，
    允许在 STM32 L4、U5、WB 和 WL SoC 系列上
    将特定引脚配置为从 Power Off 状态唤醒的源。
  * 新增 Analog Devices MAX32 SoC 系列的驱动。
  * 新增 Nuvoton Numaker M2L31X 系列的支持。
  * 在 Renesas RZ/T2M GPIO 驱动（:dtcompatible:`renesas,rzt2m-gpio`）中
    新增中断支持。

* 硬件信息

  * 为 STM32WB、STM32WBA 和 STM32WL 系列新增设备 EUI64 ID 支持和实现。

* I2C

  * 新增 Ambiq Apollo3 系列的支持。
  * 在 STM32 V2 驱动中，新增 :kconfig:option:`CONFIG_I2C_STM32_V2_TIMING`
    支持，它自动计算应根据当前使用的时钟配置
    用于配置硬件块的总线时序。为避免将此重量级算法
    嵌入生产应用程序，提供专用示例
    :zephyr:code-sample:`stm32_i2c_v2_timings`
    以获取算法的输出。一旦获得总线时序配置，
    可以禁用 :kconfig:option:`CONFIG_I2C_STM32_V2_TIMING`，
    使用设备树配置总线时序。
  * 新增 STM32H5 系列的支持。
  * 新增 NXP MCXN947 的支持
  * 新增 Analog Devices MAX32 SoC 系列的驱动。
  * 新增 Nuvoton Numaker M2L31X 系列的支持。
  * LiteX I2C 驱动（:file:`drivers/i2c/i2c_litex.c`）：

    * 新增从设备树设置位速率的支持。
    * 新增 :c:func:`i2c_litex_recover_bus()` 和
      :c:func:`i2c_litex_get_config()` API 实现。

* I2S

  * 新增 STM32H5 系列的支持。
  * 扩展 MCUX Flexcomm 驱动以支持额外通道和格式。
  * 新增 Nordic nRF54L 系列的支持。
  * 修复 nRF I2S 驱动中的分频器计算。

* I3C

  * 新增查询总线和 CCC 命令的 shell 支持。

  * 新增支持 NPCX 上 I3C 控制器的驱动。

  * 改进 :dtcompatible:`nxp,mcux-i3c` 并修复 bug，
    包括更优雅地处理总线忙而非简单返回错误。

* 输入

  * 新驱动：:dtcompatible:`adc-keys`、:dtcompatible:`chipsemi,chsc6x`、
    :dtcompatible:`cirque,pinnacle`、:dtcompatible:`futaba,sbus`、
    :dtcompatible:`pixart,pat912x`、:dtcompatible:`pixart,paw32xx`、
    :dtcompatible:`pixart,pmw3610` 和 :dtcompatible:`sitronix,cf1133`。
  * 将 :dtcompatible:`holtek,ht16k33` 和
    :dtcompatible:`microchip,xec-kbd` 从 kscan 迁移到输入子系统。

* LED

  * 在 LED shell 命令中新增设备补全，
    并使 ``get_info`` 命令以字符串形式显示颜色。

  * 新增 Lumissil Microsystems（ISSI 的一个部门）IS31FL3194 控制器的驱动
    （:dtcompatible:`issi,is31fl3194`）。

* LED 灯带

  * 在所有 LED 灯带绑定中新增 ``chain-length`` 和 ``color-mapping`` 属性。

  * 更新灯带前先检查其长度，如果提供的数据过长则返回错误。

  * 新增返回 LED 灯带长度的长度函数
    （:c:func:`led_strip_length`）。

  * 更新通道函数现在是可选的，可以留为未实现。

  * 各自的 :dtcompatible:`worldsemi,ws2812-gpio` 和
    :dtcompatible:`worldsemi,ws2812-rpi_pico-pio`
    设备树绑定的 ``in-gpios`` 和 ``output-pin`` 属性
    已重命名为 ``gpios``。

  * 删除 ``CONFIG_WS2812_STRIP`` 和 ``CONFIG_WS2812_STRIP_DRIVER`` Kconfig 选项。
    重构后它们变得无用。

  * 新增 Texas Instruments TLC59731 RGB 控制器的驱动。

* LoRa

  * 新增 Reyax LoRa 模块的驱动

* 邮箱

  * 新增基于 HSEM 的 STM32 驱动支持。

* MDIO

  * 使 ``bus_enable`` 和 ``bus_disable`` 函数对驱动实现可选，
    并从许多驱动中删除空实现。
  * 新增 NXP ENET QOS MDIO 控制器驱动。
  * 修复 NXP ENET MDIO 驱动阻塞系统工作队列的 bug。
  * :kconfig:option:`CONFIG_MDIO_NXP_ENET_TIMEOUT` 单位更改为微秒。
  * 新增 STM32 MDIO 控制器驱动支持。

* MFD

  * 新驱动 :dtcompatible:`nxp,lp-flexcomm`。
  * 新驱动 :dtcompatible:`rohm,bd8lb600fs`。
  * 新驱动 :dtcompatible:`maxim,max31790`。
  * 新驱动 :dtcompatible:`infineon,tle9104`
  * 新驱动 :dtcompatible:`adi,ad559x`
  * 为 :dtcompatible:`x-powers,axp192` 新增禁用 N_VBUSEN 的选项。
  * 为 :dtcompatible:`nordic,npm1300` 新增 GPIO 输入边沿事件。
  * 为 :dtcompatible:`nordic,npm1300` 新增长按复位配置。
  * 修复 :dtcompatible:`nordic,npm6001` 的滞回模式初始化。

* Modem

  * 删除已弃用的 ``GSM_PPP`` 驱动及其 dts 兼容字符串 ``zephyr,gsm-ppp``。

  * 删除之前由 ``GSM_PPP`` 使用的已弃用的 ``UART_MUX`` 和 ``GSM_MUX``。

  * 从 ``MODEM_CELLULAR`` 驱动中删除对 dts 兼容字符串 ``zephyr,gsm-ppp`` 的支持。

  * 从 ``MODEM_IFACE_UART_INTERRUPT`` 模块中删除与 ``UART_MUX`` 的集成。

  * 从 ``MODEM_SHELL`` 模块中删除与 ``UART_MUX`` 的集成。

  * 在 ``MODEM_CELLULAR`` 驱动中实现 modem 管道链接
    用于不同 modem 可用的额外 DLCI 通道。
    这包括通用 AT 模式 DLCI 通道，命名为
    ``user_pipe_<index>``，以及为 GNSS 隧道保留的 DLCI 通道，
    命名为 ``gnss_pipe``。

  * 新增一组 shell 命令以使用新实现的 modem 管道链接
    直接向 modem 发送 AT 命令。
    新 shell 命令的实现既功能完整，
    又与 ``MODEM_CELLULAR`` 驱动一起
    提供如何实现和使用 modem 管道链接模块的示例。

* PCIE

  * ``pcie_bdf_lookup`` 和 ``pcie_probe`` 已删除，
    因为它们自 v3.3.0 起已弃用。

* MIPI-DBI

  * 新增 release API
  * 新增通过设备树选择模式的支持

* MSPI

  * 新增实验性 :ref:`MSPI（多比特 SPI）<mspi_api>` API，
    启用对通常需要命令、地址和数据阶段
    以及可变延迟传输的高级 SPI 控制器和外设的支持。
    该 API 现在支持从单线 SDR 到六线 DDR 通信，
    支持同步/异步方式。
  * 在总线模拟器下新增 MSPI 总线模拟器
    以展示 MSPI API 的实现。
  * 新增 MSPI 闪存设备模拟器
    以展示 MSPI API 的使用和与 MSPI 总线控制器的接口。
  * 新增 APS6404L QPI pSRAM 设备驱动。
  * 新增 ATXP032 OPI NOR 闪存设备驱动。
  * 新增 Ambiq Apollo3p MSPI 控制器驱动。
  * 新增 :zephyr:code-sample:`mspi-async` 和
    :zephyr:code-sample:`mspi-flash` 示例
    以展示 MSPI 设备驱动的使用。
  * 新增 mspi/api 和 mspi/flash 测试用例
    供开发者检查其实现。

* 引脚控制

  * 新增 Renesas RA8 系列的驱动
  * 新增 Infineon PSoC6（旧版）的驱动
  * 新增 Analog Devices MAX32 SoC 系列的驱动。
  * 新增 Ambiq Apollo3 的驱动
  * 新增 ENE KB1200 的驱动
  * 新增 NXP RW 的驱动
  * Espressif 驱动现在支持 ESP32C6
  * STM32 驱动现在支持 STM32C0 的 remap 功能
  * 新增 Nuvoton Numaker M2L31X 系列的支持。

* PWM

  * 新增 STM32H7R/S 系列的支持。
  * 为 NXP imxrt11xx 新增 QTMR PWM 驱动
  * 使 NXP MCUX PWM 驱动线程安全
  * 修复 :zephyr:code-sample:`pwm-blinky` 代码示例
    以展示 :zephyr:board:`beagleconnect_freedom` 的 PWM 支持。
  * 新增 ENE KB1200 的驱动。
  * 新增 Nordic nRF54H 和 nRF54L 系列 SoC 的支持。
  * 新增 Nuvoton Numaker M2L31X 系列的支持。

* 稳压器

  * 新驱动 :dtcompatible:`cirrus,cp9314`。
  * 在通用稳压器驱动中新增 ``regulator-boot-off`` 属性。
    更新 :dtcompatible:`adi,adp5360-regulator`、
    :dtcompatible:`nordic,npm1300-regulator`、
    :dtcompatible:`nordic,npm6001-regulator`
    和 :dtcompatible:`x-powers,axp192-regulator`
    以使用此新属性。
  * 为 :dtcompatible:`renesas,smartbond-regulator` 新增电源管理。
  * 新增 ``is_enabled`` shell 命令。
  * 删除单线程系统中的忙等待使用。
  * 修复 :dtcompatible:`x-powers,axp192-regulator` 的 DCDC2 输出控制。
  * 修复 :dtcompatible:`renesas,smartbond-regulator` 的电流和电压获取函数。
  * 修复 NXP VREF Kconfig 泄漏。
  * 修复 shell 中微值显示。
  * 修复 ``adset`` shell 命令中的 strcmp 使用 bug。

* 复位

  * 为 Nuvoton NPCX 芯片上的复位控制器新增驱动。
  * 为 NXP SYSCON 新增复位控制器驱动。
  * 为 NXP RSTCTL 新增复位控制器驱动。
  * 新增 Nuvoton Numaker M2L31X 系列的支持。

* RTC

  * 新增 Raspberry Pi Pico RTC 驱动。
  * 为所有 STM32 MCU 系列（除 STM32F1 外）新增 :kconfig:option:`CONFIG_RTC_ALARM` 支持。
  * 新增 Nuvoton Numaker M2L31X 系列的支持。

* RTIO

  * 将无锁队列从 RTIO 移至 lib，
    将 SPSC 和 MPSC 队列的 ``rtio_`` 前缀移除。
  * 新增测试并修复与链式回调请求相关的 bug。
  * 围绕 p4wq（rtio workq）创建封装器，
    在原生异步 RTIO 功能不可用时
    从阻塞行为转为非阻塞行为。

* SDHC

  * 新增 ESP32 SDHC 驱动（:dtcompatible:`espressif,esp32-sdhc`）。
  * 为 Renesas MMC 控制器新增 SDHC 驱动（:dtcompatible:`renesas,rcar-mmc`）。

* 传感器

  * 通用

    * 在新的 read/decoder API 中新增通道指定符。
    * 新增阻塞传感器读取调用 :c:func:`sensor_read`。
    * 使用 RTIO workqueues 服务解耦 RTIO 请求，
      将 :c:func:`sensor_submit_callback` 转为异步请求。
    * 将大多数驱动移至厂商子目录。

  * AMS

    * 新增 TSL2591 光传感器驱动（:dtcompatible:`ams,tsl2591`）。

  * Aosong

    * 新增 DHT20 数字输出湿度和温度传感器驱动
      （:dtcompatible:`aosong,dht20`）。

    * 为 dht11 驱动新增 :kconfig:option:`CONFIG_DHT_LOCK_IRQS`，
      允许在传感器读取期间锁定中断
      以防止读取传感器的问题。

  * Bosch

    * 将 BME280 更新到新的异步 API。

  * Infineon

    * 新增 TLE9104 电源轨开关诊断传感器驱动
      （:dtcompatible:`infineon,tle9104-diagnostics`）。

  * Maxim

    * 新增 DS18S20 1-Wire 温度传感器驱动（:dtcompatible:`maxim,ds18s20`）。
    * 新增 MAX31790 风扇速度和风扇故障传感器
      （:dtcompatible:`maxim,max31790-fan-fault`
      和 :dtcompatible:`maxim,max31790-fan-speed`）。

  * NXP

    * 新增低功耗比较器驱动（:dtcompatible:`nxp,lpcmp`）。

  * Rohm

    * 新增 BD8LB600FS 诊断传感器驱动（:dtcompatible:`rohm,bd8lb600fs-diagnostics`）。

  * Silabs

    * 对 SI7006 湿度/温度传感器驱动进行多个修复和增强。

  * ST

    * QDEC 驱动现在支持编码器模式配置
      （参见 :dtcompatible:`st,stm32-qdec`）。
    * 新增 STM32 数字温度传感器支持（:dtcompatible:`st,stm32-digi-temp`）。
    * 新增 IIS328DQ I2C/SPI 加速度计传感器驱动（:dtcompatible:`st,iis328dq`）。

  * TDK

    * 在 MPU6050 驱动中新增 MPU6500 3 轴加速度计
      和 3 轴陀螺仪传感器的支持。

  * TI

    * 新增 TMP114 驱动（:dtcompatible:`ti,tmp114`）。
    * 新增 INA226 双向电流和功率监控器驱动（:dtcompatible:`ti,ina226`）。
    * 新增 LM95234 四路远程二极管和本地温度传感器驱动
      （:dtcompatible:`national,lm95234`）。

  * 其他厂商

    * 新增 Angst+Pfister FCX-MLDX5 O2 传感器驱动（:dtcompatible:`ap,fcx-mldx5`）。
    * 新增 ENE KB1200 转速传感器驱动（:dtcompatible:`ene,kb1200-tach`）。
    * 新增 Festo VEAA-X-3 系列比例压力调节器驱动
      （:dtcompatible:`festo,veaa-x-3`）。
    * 新增 Innovative Sensor Technology TSic xx6 温度传感器驱动
      （:dtcompatible:`ist,tsic-xx6`）。
    * 新增 ON Semiconductor NCT75 温度传感器驱动（:dtcompatible:`onnn,nct75`）。
    * 新增 ScioSense ENS160 数字金属氧化物多气体传感器驱动
      （:dtcompatible:`sciosense,ens160`）。
    * 对 GROW_R502A 指纹传感器驱动进行多个修复和增强。

* 串口

  * 新增使用 NUS（Nordic UART Service）通过 Bluetooth LE 支持 UART 的驱动。
    该驱动允许使用 Bluetooth 作为传输
    用于当前 UART 支持的所有子系统（例如：Console、Shell、Logging）。
  * 在 STM32 驱动的异步 DMA 模式中新增 :kconfig:option:`CONFIG_NOCACHE_MEMORY` 支持。
    现在可以在 STM32 F7 和 H7 SoC 系列上
    在 :kconfig:option:`CONFIG_DCACHE` 启用时使用 DMA 模式的 UART，
    只要 DMA 缓冲区放在非缓存内存段中。
  * 新增 STM32H7R/S 系列的支持。

  * 在 Renesas RCar 平台的 UART 驱动中
    新增 HSCIF（带 FIFO 的高速串行通信接口）支持。

  * 新增 ENE KB1200 UART 的驱动。

  * 新增 Analog Devices MAX32 系列微控制器上 UART 的驱动。

  * 新增 Renesas RA8 设备上 UART 的驱动。

  * ``uart_emul``（:dtcompatible:`zephyr,uart-emul`）：

    * 为模拟 UART 驱动新增异步 API 支持。

  * ``uart_esp32``（:dtcompatible:`espressif,esp32-uart`）：

    * 新增反转 TX 和 RX 引脚信号的支持。

    * 新增 ESP32C6 SoC 的支持。

  * ``uart_native_tty``（:dtcompatible:`zephyr,native-tty-uart`）：

    * 新增模拟中断驱动 UART 的支持。

  * ``uart_mcux_lpuart``（:dtcompatible:`nxp,kinetis-lpuart`）：

    * 新增单线半双工通信支持。

    * 新增反转 TX 和 RX 引脚信号的支持。

  * ``uart_npcx``（:dtcompatible:`nuvoton,npcx-uart`）：

    * 新增异步 API 支持。

    * 新增 3MHz 波特率支持。

  * ``uart_nrfx_uarte``（:dtcompatible:`nordic,nrf-uarte`）：

    * 新增在 UART 不活动时将 TX 和 RX 引脚放入低功耗模式的支持。

  * ``uart_nrfx_uarte2``（:dtcompatible:`nordic,nrf-uarte`）：

    * 在设备挂起时阻止 UART 传输。

    * 修复某些事件未触发的问题。

  * ``uart_pl011``（:dtcompatible:`arm,pl011`）：

    * 新增运行时配置支持。

    * 新增复位设备支持。

    * 新增使用时钟控制确定频率的支持。

    * 新增硬件流控支持。

    * 新增 Ambiq Apollo3 SoC 上 UART 的支持。

  * ``uart_smartbond``（:dtcompatible:`renesas,smartbond-uart`）：

    * 新增电源管理支持。

    * 新增通过 DTR 和 RX 线唤醒的支持。

  * ``uart_stm32``（:dtcompatible:`st,stm32-uart`）：

    * 新增识别 DMA 缓冲区在数据缓存还是不可缓存内存中的支持。

  * 新增 Nuvoton Numaker M2L31X 系列的支持。

* SPI

  * 新增 NXP MCXN947 的支持
  * 新增 Ambiq Apollo3 系列基于 general IOM 的 SPI 支持。
  * 新增 Ambiq Apollo3 基于 BLEIF 的 SPI 支持，
    专用于内部 HCI。
  * 在 STM32 SPI 驱动上新增 :kconfig:option:`CONFIG_PM`
    和 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME` 支持。
  * 在 STM32F7x SoC 系列的 DMA SPI 模式中
    新增 :kconfig:option:`CONFIG_NOCACHE_MEMORY` 支持。
  * 新增 STM32H7R/S 系列的支持。
  * 新增 Analog Devices MAX32 SoC 系列的驱动。
  * 修复 gd32 spi 中不正确的寄存器分配。

* USB

  * 为 NXP EHCI 和 IP3511 USB 控制器新增 UDC shim 驱动。
  * IT82xx2、DWC2、STM32、RP2040、Smartbond
    USB 控制器驱动的多个修复和改进。

* 视频

  * 新增 STM32 数字相机接口（DCMI）驱动的支持（:dtcompatible:`st,stm32-dcmi`）。
  * 启用 NXP USB 设备控制器
  * 新增 ov7670 摄像头的支持
  * 新增 ov5640 摄像头的支持
  * 为 NXP MCUX 新增 CSI-2 MIPI 驱动
  * 新增 DVP FPC 24 引脚 mt9m114 摄像头模块扩展板的支持

* 看门狗

  * 新增 :kconfig:option:`CONFIG_WDT_NPCX_WARNING_LEADING_TIME_MS`
    以设置毫秒级的领先警告时间。
    删除不再使用的 :kconfig:option:`CONFIG_WDT_NPCX_DELAY_CYCLES`。
  * 新增 Ambiq Apollo3 系列的支持。
  * 新增 STM32H7R/S 系列的支持。
  * 新增 Nuvoton Numaker M2L31X 系列的支持。
  * 在 ESP32 SoC 变体中为外部 32kHz 晶振新增看门狗。

* Wi-Fi

  * 修复 esp-at 的消息解析。
  * 修复 esp-at 连接失败。
  * 为 esp-at 的 UDP socket 实现 :c:func:`bind` 和 :c:func:`recvfrom`。
  * 为 eswifi 新增设置最大数据大小的选项。
  * 修复 ESP32 Wi-Fi 驱动内存泄漏。

网络
**********

* ARP：

  * 新增 gratuitous ARP 传输支持。
  * 修复 ARP 模块内 TX 和 RX 线程之间可能的死锁。
  * 修复可能的 ARP 条目泄漏。
  * 改进 ARP 调试日志。

* CoAP：

  * 修复 CoAP observe age 溢出。
  * 增加 CoAP 重传上限（:kconfig:option:`CONFIG_COAP_MAX_RETRANSMIT`）。
  * 修复 CoAP 客户端库中的 CoAP 观察。
  * 新增 CoAP 客户端 :c:func:`coap_client_cancel_requests` API，
    允许取消活动观察。
  * 修复 CoAP 服务器示例中响应的 CoAP ID 生成。

* 连接管理器：

  * 新增对新 net_mgmt 事件的支持，
    允许独立跟踪 IPv4 和 IPv6 连接性：

    * :c:macro:`NET_EVENT_L4_IPV4_CONNECTED`
    * :c:macro:`NET_EVENT_L4_IPV4_DISCONNECTED`
    * :c:macro:`NET_EVENT_L4_IPV6_CONNECTED`
    * :c:macro:`NET_EVENT_L4_IPV6_DISCONNECTED`

* DHCPv4：

  * 新增封装的厂商特定选项支持。
    通过启用 :kconfig:option:`CONFIG_NET_DHCPV4_OPTION_CALLBACKS_VENDOR_SPECIFIC`
    可使用 :c:func:`net_dhcpv4_add_option_vendor_callback`
    注册回调以处理这些选项，
    之后使用 :c:func:`net_dhcpv4_init_option_vendor_callback` 初始化。
  * 新增"Vendor class identifier"选项支持。
    使用 :kconfig:option:`CONFIG_NET_DHCPV4_VENDOR_CLASS_IDENTIFIER`
    启用，使用 :kconfig:option:`CONFIG_NET_DHCPV4_VENDOR_CLASS_IDENTIFIER_STRING`
    设置。
  * DHCPv4 选项中的 NTP 服务器现在可用于设置系统时间。
    如果 :kconfig:option:`CONFIG_NET_CONFIG_CLOCK_SNTP_INIT` 启用则默认执行。
  * syslog 服务器地址现在可通过 DHCPv4 选项设置。
    如果 :kconfig:option:`CONFIG_LOG_BACKEND_NET_USE_DHCPV4_OPTION` 启用则默认执行。
  * 修复已注册回调的选项未从服务器请求的 bug。
  * 修复从服务器接收的 netmask 未正确应用的 bug。
  * 重新实现 DHCPv4 客户端 RENEW/REBIND 逻辑
    以符合 RFC2131。
  * 改进 DHCPv4 服务器中已拒绝地址的管理，
    现在可在配置时间后重用。
  * 根据 RFC6842 修复 DHCPv4 服务器响应中包含客户端 ID 选项。
  * 新增 :kconfig:option:`CONFIG_NET_DHCPV4_SERVER_NAK_UNRECOGNIZED_REQUESTS`，
    允许覆盖 RFC 定义的行为，
    并向未识别的客户端 NAK 请求。
  * 修复 DHCPv4 服务器中的客户端 ID 生成。
  * DHCPv4 客户端和服务器实现中的其他小修复。

* DHCPv6：

  * 修复 net_mgmt 事件中不正确的 DHCPv6 事件代码基。
  * 新增 :kconfig:option:`CONFIG_NET_DHCPV6_DUID_MAX_LEN`，
    允许配置最大支持 DUID 长度。
  * 新增 DHCPv6 文档页。

* DNS/mDNS/LLMNR：

  * 修复 mDNS Responder 在 mDNS Resolver 也启用时不工作的问题。
    mDNS Resolver 和 mDNS Responder 现在可同时使用。
  * 重构 LLMNR 和 mDNS 响应器以及 DNS 解析器
    以使用 socket 和 socket 服务 API。
  * 新增 ANY 查询资源类型。
  * 新增 mDNS 在运行时提供记录的支持。
  * 新增 DNS 记录缓存支持。
  * 修复 socket 创建失败时以及所有结果已返回时返回的错误码。
  * 修复 DNS 重传超时计算。

* gPTP/PTP：

  * 新增 IEEE 1588-2019 PTP 支持。
  * 新增 SO_TIMESTAMPING socket 选项支持
    以在 socket 辅助数据中获取时间戳信息。
  * 修复时间戳回调上的竞态条件。
  * 修复当我们不是 GM 时钟时时钟主同步发送 SM。

* HTTP：

  * 新增 HTTP/2 服务器库和示例应用程序，
    支持静态、动态和 Websocket 资源类型。
  * 新增 HTTP shell 组件。
  * 改进 HTTP 客户端错误报告。
  * 将 HTTP 客户端库从实验性移出。
  * 在 HTTP 客户端发送响应时新增 POLLOUT 监控。

* IPSP：

  * 删除 IPSP 支持。``CONFIG_NET_L2_BT`` 不再存在。

* IPv4：

  * 根据 RFC 5227 实现 IPv4 地址冲突检测。
  * 新增 :c:func:`net_ipv4_is_private_addr` API 函数。
  * IPv4 netmask 现在为每个地址单独设置
    而非为整个接口设置。
  * 其他小修复和改进。

* IPv6：

  * 根据 RFC 8981 实现 IPv6 隐私扩展。
  * 新增 :c:func:`net_ipv6_is_private_addr` API 函数。
  * 实现 IPv6 可达性提示。上层可使用
    :c:func:`net_if_nbr_reachability_hint`
    报告邻居可达性并避免不必要的邻居发现请求。
  * 新增 :kconfig:option:`CONFIG_NET_IPV6_MTU`
    允许设置自定义 IPv6 MTU。
  * 新增 :kconfig:option:`CONFIG_NET_MCAST_ROUTE_MAX_IFACES`
    允许为多播转发条目设置多个接口。
  * 新增 :kconfig:option:`CONFIG_NET_MCAST_ROUTE_MLD_REPORTS`
    允许在 MLDv2 报告中报告多播路由。
  * 修复多播报包的 IPv6 跳数限制处理。
  * 改进 IPv6 邻居发现测试覆盖。
  * 修复报告重复地址检测冲突的邻居通告包被丢弃的 bug。
  * 其他小修复和改进。

* LwM2M：

  * 新增 API 函数：

    * :c:func:`lwm2m_set_bulk`
    * :c:func:`lwm2m_rd_client_set_ctx`

  * 在 :c:type:`lwm2m_engine_set_data_cb_t` 回调类型中
    新增 ``offset`` 参数。
    这影响 post write 和 validate 回调以及一些固件回调。
  * 修复分块传输中接收分块号 0 时分块上下文未重置的问题。
  * 修复分块传输中与服务器的分块大小协商。
  * 新增 :kconfig:option:`CONFIG_LWM2M_ENGINE_ALWAYS_REPORT_OBJ_VERSION`，
    允许强制客户端始终报告对象版本。
  * 分块传输现在可用于无注册回调的资源。
  * 修复注册回调发送的空 ACK 未立即发送的 bug。
  * 删除已弃用的 API 函数和定义。
  * 其他小修复和改进。

* 杂项：

  * 改进整体网络 API Doxygen 文档。
  * 将 TFTP 库转换为使用 ``zsock_*`` API。
  * 新增 SNTP :c:func:`sntp_simple_addr` API 函数，
    在已知服务器 IP 地址时执行 SNTP 查询。
  * 新增 :kconfig:option:`CONFIG_NET_TC_THREAD_PRIO_CUSTOM`
    允许覆盖默认流量类线程优先级。
  * 修复 net config 库中 IPv6 事件处理器初始化顺序。
  * 重构 telnet shell 后端以使用 socket 和 socket 服务 API。
  * 修复 IGMP 包的双重解引用。
  * 在多个测试和示例中从 ``native_posix`` 迁移到 ``native_sim`` 支持。
  * 新增在网络缓冲区中复制用户数据的支持。
  * 修复零大小网络缓冲区的克隆。
  * 新增处理 40 位数据格式的 net_buf API。
  * 为 dummy L2 新增接收回调，
    适用于某些用例（例如数据包捕获）。
  * 实现伪接口，即"any"接口，
    用于数据包捕获用例。
  * 新增 cooked 模式捕获支持。
    这允许非 IP 基于的网络数据捕获。
  * 在启动或停止数据包捕获时生成网络事件。
  * 删除过时且未使用的 ``tcp_first_msg`` :c:struct:`net_pkt` 标志。
  * 新增 :zephyr:code-sample:`secure-mqtt-sensor-actuator` 示例。
  * 新增部分 L3 和 L4 校验和卸载支持。
  * 使用新的 CA 证书更新 :zephyr:code-sample:`mqtt-azure`，
    当前证书即将过期。
  * 为 Native Simulator 卸载 socket 新增驱动。
  * 重构 VLAN 支持以使用虚拟网络接口。
  * 为虚拟网络接口新增统计收集。
  * 修复 :kconfig:option:`CONFIG_NET_MGMT_EVENT_SYSTEM_WORKQUEUE`
    启用时 :c:func:`mgmt_event_work_handler` 中
    系统工作队列阻塞的问题。

* MQTT：

  * 为 MQTT TLS 后端新增 ALPN 支持。
  * 在 :c:struct:`mqtt_client` 上下文结构中新增用户数据字段。
  * 修复 MQTT Websockets 传输中潜在的 socket 泄漏。

* 网络接口：

  * 新增 API 函数：

    * :c:func:`net_if_ipv4_maddr_foreach`
    * :c:func:`net_if_ipv6_maddr_foreach`

  * 改进网络接口代码中的调试日志。
  * 在 :c:struct:`net_if_addr` 结构中新增引用计数器。
  * 修复接口 up 时的 IPv6 DAD 和 MLDv2 操作。
  * 为 OpenThread 接口新增唯一默认名称。
  * 其他小修复。

* OpenThread

  * 删除已弃用的 ``openthread_set_state_changed_cb()`` 函数。
  * 新增 BLE TCAT 广告 API 的实现。

* PPP

  * 删除已弃用的 ``gsm_modem`` 驱动和示例。
  * 优化 PPP 驱动中的内存分配。
  * :zephyr:code-sample:`cellular-modem` 示例中的杂项改进
  * 新增 PPP 底层数据包捕获支持。

* Shell：

  * 新增 ``net ipv4 gateway`` 命令以设置 IPv4 网关地址。
  * 在网络 shell 宏中新增参数验证。
  * 修复 net_mgmt socket 信息打印。
  * 重构 VLAN 信息打印。
  * 新增通过 ``net iface set_mac`` 命令设置随机 MAC 地址的选项。
  * 在打印多播地址信息时新增多播加入状态。

* Socket：

  * 实现新的网络 POSIX API：

    * :c:func:`if_nameindex`
    * :c:func:`inet_ntoa`
    * :c:func:`inet_addr`

  * 新增 socket API 调用跟踪支持。
  * TLS socket 不再是实验性 API。
  * 修复 ``AF_PACKET`` 类型 socket 的协议字段字节序。
  * 修复 TCP 的 :c:func:`getsockname`。
  * 改进使用 DTLS socket 时 :c:func:`sendmsg` 的支持。
  * 修复 socket 服务线程停止时
    :c:func:`net_socket_service_register` 函数停滞的问题。
  * 修复注销服务时潜在的 socket 服务线程停止。
  * 从 socket 服务库中删除异步超时支持。
  * 修复文件描述符短缺时使用 :c:func:`zsock_accept`
    时潜在的忙循环。

* Syslog：

  * 新增 API 函数：

    * :c:func:`log_backend_net_set_ip`
      以 IP 地址直接初始化 syslog net 后端。
    * :c:func:`log_backend_net_start`
      以方便 syslog net 后端激活。

  * 为 syslog net 后端新增结构化日志支持。
  * 为 syslog net 后端新增 TCP 支持。

* TCP：

  * 修复接受新 TCP 连接时可能的死锁。
  * 修复连接拆卸期间的 ACK 号验证。
  * 修复 FIN 包中包含的数据字节被忽略的 bug。
  * 修复初始 SYN 包传输失败时可能的 TCP 上下文泄漏。
  * 弃用 :kconfig:option:`CONFIG_NET_TCP_ACK_TIMEOUT`，
    因为它与其他配置冗余。
  * 改进调试日志，使其在高负载下更容易跟踪。
  * ISN 生成现在使用 SHA-256 而非 MD5。
    此外，它现在依赖 PSA API 而非旧版 Mbed TLS 函数
    进行哈希计算。
  * 改进无 PSH 标志时的 ACK 回复逻辑
    以减少冗余 ACK。

* Websocket：

  * 新增 Websocket API：

    * :c:func:`websocket_register`
    * :c:func:`websocket_unregister`

  * 将 Websocket 库转换为使用 ``zsock_*`` API。
  * 为 Websocket socket 新增 Object Core 支持。
  * 在发送时新增 POLLOUT 监控。

* Wi-Fi：

  * 减小 5 GHz 信道列表的内存使用。
  * 在 AP 模式中新增信道有效性检查。
  * 在 connect 调用中新增 BSSID 配置支持。
  * Wifi shell 帮助文本修复。选项解析修复。
  * 支持 WPA auto personal 安全模式。
  * 收集单播接收/发送网络包统计。
  * 新增 RTS 阈值配置支持。
    通过此，用户可设置 RTS 阈值值或禁用 RTS 机制。
  * 新增 AP 参数配置支持。
    通过此，用户可在构建和运行时设置 AP 参数。
  * 新增配置 ``max_inactivity`` BSS 参数的支持。
    用户可在构建和运行时设置此参数
    以控制在 STA 不活动后 AP 可能断开 STA 的最大时间。
  * 新增配置 ``inactivity_poll`` BSS 参数的支持。
    用户可设置仅构建的 AP 参数
    以控制 AP 是否在丢弃 STA 前轮询 STA。
  * 新增配置 ``max_num_sta`` BSS 参数的支持。
    用户可在构建和运行时设置此参数
    以控制最大 STA 条目数。

* zperf：

  * 修复 zperf 中 ``IP_TOS`` 和 ``IPV6_TCLASS`` 选项处理。
  * 修复长 zperf 会话期间的吞吐量计算。
  * 修复使用多播 IP 地址时 TCP 上传会话结束时的错误。
  * 修复 IPv6 socket 以 IPv4 地址绑定导致错误的 bug。
  * 新增在 zperf 会话期间指定使用网络接口的选项。
  * 新增 ``ZPERF_SESSION_PERIODIC_RESULT`` 事件
    用于 TCP 上传会话期间的定期更新。
  * 修复 zperf 会话出错时可能的 socket 泄漏。
  * 改进 zperf 示例默认配置下的性能。

USB
***

* 新 USB 设备堆栈：

  * 新增 HID 设备支持
  * 引入速度特定配置并使高速支持
    符合 USB2.0 规范
  * 新增通知支持和初始 BOS 支持

设备树
**********

* 新增 :c:macro:`DT_INST_NODE_HAS_COMPAT`
  以检查节点是否具有兼容字符串。
  这对于具有多个兼容字符串的节点很有用。
* 新增 :c:macro:`DT_CHILD_NUM` 及其变体
  以计算节点的子节点数。
* 新增 :c:macro:`DT_FOREACH_NODELABEL` 及其变体，
  可用于迭代设备树节点的节点标签。
* 新增 :c:macro:`DT_NODELABEL_STRING_ARRAY` 和
  :c:macro:`DT_NUM_NODELABELS` 及其变体。
* 新增 :c:macro:`DT_REG_HAS_NAME` 及其变体。
* 重构 :c:macro:`DT_ANY_INST_HAS_PROP_STATUS_OKAY`
  使结果可用于 :c:macro:`IS_ENABLED`、IF_ENABLED
  或 COND_CODE_x 等宏。
* 重构 :c:macro:`DT_NODE_HAS_COMPAT_STATUS`
  使其可在预处理器时求值。
* 将 dts 脚本中使用的 PyYaml 版本更新到 6.0
  以消除供应链漏洞。

Kconfig
*******

* 新增 ``substring`` Kconfig 预处理器函数。
* 新增 ``dt_node_ph_prop_path`` Kconfig 预处理器函数。
* 新增 ``dt_compat_any_has_prop`` Kconfig 预处理器函数。

库 / 子系统
**********************

* 调试

  * symtab

   * 通过启用 :kconfig:option:`CONFIG_SYMTAB`，
     符号表将在支持的架构上
     与 Zephyr 链接阶段可执行文件一起生成。

* 按需分页

  * NRU（Not Recently Used）驱逐算法已更新其选择逻辑
    以避免不断选择同一页驱逐。
    更新的逻辑现在在线性搜索
    上次驱逐页之后搜索新候选者。

  * 新增 LRU（Least Recently Used）驱逐算法。

* 格式化输出

  * 修复使用 ARCMWDT 编译 cbprintf 时的警告。

* 管理

  * hawkBit

    * hawkBit 子系统已重构为使用设置子系统
      存储 hawkBit 配置。

    * 通过启用 :kconfig:option:`CONFIG_HAWKBIT_SET_SETTINGS_RUNTIME`，
      hawkBit 设置可在运行时配置。
      使用 :c:func:`hawkbit_set_config` 函数
      设置 hawkBit 配置。
      也可通过 hawkBit shell 使用 ``hawkbit set`` 命令设置。

    * 当使用 hawkBit autohandler 且安装了更新时，
      设备现在会在安装完成后自动重启。

    * 通过启用 :kconfig:option:`CONFIG_HAWKBIT_CUSTOM_DEVICE_ID`，
      可注册回调函数以设置设备 ID。
      使用 :c:func:`hawkbit_set_device_identity_cb` 函数
      注册回调。

    * 通过启用 :kconfig:option:`CONFIG_HAWKBIT_CUSTOM_ATTRIBUTES`，
      可注册回调函数以设置发送到 hawkBit 服务器的设备属性。
      使用 :c:func:`hawkbit_set_custom_data_cb` 函数
      注册回调。

  * MCUmgr

    * 已删除已弃用的 mcumgr go 工具的说明，
      替代支持的客户端列表可参见
      :ref:`mcumgr_tools_libraries`。

    * 修复 SMP 结构未打包导致在
      不支持非对齐内存访问的设备上
      发生故障的问题。

    * 新增 :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_BT_DYNAMIC_SVC_REGISTRATION`，
      允许用户选择 MCUmgr BT 服务
      是在编译时静态注册还是在运行时动态注册。

    * 在 FS 组中，TinyCrypt 已被 PSA 调用
      替代用于 SHA 计算。

* 日志

  * 通过启用 :kconfig:option:`CONFIG_LOG_BACKEND_NET_USE_DHCPV4_OPTION`，
    网络后端的 syslog 服务器 IP 地址
    由 DHCPv4 Log Server Option（7）设置。

  * 在 POSIX 上使用实时时钟作为时间戳。

  * 新增 syslog（POSIX）支持。

  * 新增 :c:macro:`LOG_WRN_ONCE`
    用于记录警告消息，仅记录第一次出现。

  * 新增 :c:func:`log_thread_trigger`
    用于触发日志消息处理。

  * 修复 :kconfig:option:`CONFIG_MULTITHREADING`
    禁用时延迟日志不编译的情况。

  * 修复基于字典的日志与非字典混合时
    日志字符串可能从二进制中剥离的情况。

  * 修复某些情况下字典数据库未生成的问题。

  * 修复字典日志解析器未正确处理 long long 参数的问题。

  * 修复对 :kconfig:option:`CONFIG_LOG_MSG_APPEND_RO_STRING_LOC` 的支持。

* Modem 模块

  * 新增 modem 管道链接模块，
    全局共享 modem 管道，
    允许设备驱动为应用程序创建和设置管道。

  * 简化 modem 管道模块的同步机制
    以仅保护回调和用户数据。
    这与树内 modem 管道的实际使用一致。

  * 新增 ``modem_stats`` 模块，
    跟踪 modem 子系统中缓冲区的使用。

* 电源管理

  * 设备现在可以声明哪些系统电源状态导致断电。
    此信息可用于在设备需要时
    设置和释放电源状态约束。
    该功能通过 :kconfig:option:`CONFIG_PM_POLICY_DEVICE_CONSTRAINTS` 启用。
    使用函数 :c:func:`pm_policy_device_power_lock_get`
    和 :c:func:`pm_policy_device_power_lock_put`
    锁定和解锁设备中所有导致断电的电源状态。

  * 为设备电源管理新增 shell 支持。

  * 设备电源管理已与系统电源管理解耦。
    新的 :kconfig:option:`CONFIG_PM_DEVICE_SYSTEM_MANAGED` 选项
    用于启用设备在系统睡眠时是否必须挂起。

  * 使用 ``zephyr,pm-device-disabled``
    允许按电源状态单独禁用系统设备电源管理。
    这允许目标调整哪些状态应（以及不应）
    触发设备电源管理。

* 加密

  * TinyCrypt 仍可用，但现在正逐步淘汰，
    改用 PSA Crypto 以增强安全性和性能。
  * Mbed TLS 更新到 3.6.0。
    发布说明可参见：
    https://github.com/Mbed-TLS/mbedtls/releases/tag/v3.6.0
  * 当系统中有任何 PSA crypto 提供者可用时
    （:kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_CLIENT` 启用），
    所需的 PSA 功能现在必须通过 ``CONFIG_PSA_WANT_xxx``
    符号显式选择。
  * 新增选择符号 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_LEGACY_RNG`
    和 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_EXTERNAL_RNG`，
    以允许用户指定 Mbed TLS PSA crypto 核心
    应如何生成随机数。
    前者（默认）依赖旧版熵和 CTR_DRBG/HMAC_DRBG 模块，
    而后者依赖 CSPRNG 驱动。
  * :kconfig:option:`CONFIG_MBEDTLS_PSA_P256M_DRIVER_ENABLED`
    启用 Mbed TLS p256-m 驱动 PSA crypto 库的支持。
    这是 secp256r1 曲线的 Cortex-M SW 优化实现。

* CMSIS-NN

  * CMSIS-NN 已从 v4.1.0 更新到 v6.0.0：
    https://arm-software.github.io/CMSIS-NN/latest/rev_hist.html

* FPGA

  * 改进缺少 ``reset``、``load``、``get_status``
    和 ``get_info`` 方法的驱动处理。
  * 新增 Agilex 和 Agilex 5 的支持。

* 随机

  * 除现有的 :c:func:`sys_rand32_get` 函数外，
    :c:func:`sys_rand8_get`、:c:func:`sys_rand16_get`
    和 :c:func:`sys_rand64_get` 现在也可用。
    这些函数都基于 :c:func:`sys_rand_get` 实现。

* SD

  * SDMMC 和 SDIO 频率和时序选择逻辑已重构，
    以解决当使用的 SDHC 设备未报告
    该模式支持的最高频率时
    时序模式未被选择的问题。
    现在，如果主机控制器和卡都报告
    支持给定时序模式但不支持该模式支持的最高频率，
    将选择该时序模式并以降低的频率配置
    （:github:`72705`）。

* 状态机框架

  * :c:macro:`SMF_CREATE_STATE` 宏现在始终接受 5 个参数。
  * 已运行状态的父级转换源现在选择正确的最近公共祖先
    以执行 Exit 和 Entry Actions。
  * 向 :c:func:`smf_set_state` 传递 ``NULL`` 现在不被允许。

* 存储

  * FAT FS：现在可以暴露 FAT 的文件系统格式化功能
    而无需同时启用挂载失败时的自动格式化，
    通过设置 :kconfig:option:`CONFIG_FS_FATFS_MKFS` Kconfig 选项。
    如果 :kconfig:option:`CONFIG_FILE_SYSTEM_MKFS` 设置，
    该选项默认启用。

  * FS：现在可以在打开文件时使用 :c:func:`fs_open`
    并传递 ``FS_O_TRUNC`` 标志来截断文件。

  * Flash Map：Flash Area 完整性检查中
    TinyCrypt 已被 PSA Crypto 替代。

  * Flash Map：新增 :c:func:`flash_area_flatten`，
    用于擦除操作之前用于移除/扰乱数据
    而非为设备随机数据写入准备的情况。

  * Flash Map：新增 :c:macro:`FIXED_PARTITION_NODE_OFFSET`、
    :c:macro:`FIXED_PARTITION_NODE_SIZE`
    和 :c:macro:`FIXED_PARTITION_NODE_DEVICE`，
    允许从设备树节点而非标签获取固定分区信息。

  * 新增 :kconfig:option:`CONFIG_NVS_DATA_CRC`，
    为数据添加 CRC 保护。
    注意启用此选项会使 NVS 与
    之前未对数据使用 CRC 的现有存储不兼容。

  * 修复 NVS 问题，其中 :c:func:`nvs_calc_free_space`
    返回大于可用大小的值，
    因为未减去保留 ate 的空间。

  * 修复 ext2 在尝试格式化分区时
    错误计算可用空间的问题。

  * 修复 FAT 驱动在卸载后将磁盘留在初始化状态的问题。

* 任务看门狗

  * 新增 shell（主要用于开发期间的测试目的）。

* POSIX API

  * 改进 Kconfig 选项以反映标准 POSIX 选项和选项组。

  * 新增以下选项组的支持

    * :ref:`POSIX_MAPPED_FILES <posix_option_group_mapped_files>`
    * :ref:`POSIX_MEMORY_PROTECTION <posix_option_group_memory_protection>`
    * :ref:`POSIX_NETWORKING <posix_option_group_networking>`
    * :ref:`POSIX_SINGLE_PROCESS <posix_option_group_single_process>`
    * :ref:`POSIX_TIMERS <posix_option_group_timers>`
    * :ref:`XSI_SYSTEM_LOGGING <posix_option_group_xsi_system_logging>`

  * 新增以下选项的支持

    * :ref:`_POSIX_ASYNCHRONOUS_IO <posix_option_asynchronous_io>`
    * :ref:`_POSIX_CPUTIME <posix_option_cputime>`
    * :ref:`_POSIX_FSYNC <posix_option_fsync>`
    * :ref:`_POSIX_MEMLOCK <posix_option_memlock>`
    * :ref:`_POSIX_MEMLOCK_RANGE <posix_option_memlock_range>`
    * :ref:`_POSIX_READER_WRITER_LOCKS <posix_option_reader_writer_locks>`
    * :ref:`_POSIX_SHARED_MEMORY_OBJECTS <posix_shared_memory_objects>`
    * :ref:`_POSIX_THREAD_CPUTIME <posix_option_thread_cputime>`
    * :ref:`_POSIX_THREAD_PRIO_PROTECT <posix_option_thread_prio_protect>`
    * :ref:`_POSIX_THREAD_PRIORITY_SCHEDULING <posix_option_thread_priority_scheduling>`
    * :ref:`_XOPEN_STREAMS <posix_option_xopen_streams>`

  * 修复 eventfd ``F_SETFL`` 处理以避免覆盖内部标志。
  * 修复调试消息中打印的线程栈地址。
  * 修复信号代码中的宏参数使用。

* LoRa/LoRaWAN

  * 新增分块数据块传输服务，
    可通过 :kconfig:option:`CONFIG_LORAWAN_FRAG_TRANSPORT` 启用。
    除 Semtech 的默认分块解码器实现外，
    还提供内存占用较小的树内实现。

  * 新增示例以演示 LoRaWAN 空中固件升级（FUOTA）。

* ZBus

  * 通过优化消息订阅者交付通知期间
    克隆的通道引用复制
    改进 VDED 流程。

  * 通过静态初始化信号量和运行时观察者列表
    改进初始化阶段。
    这减少了 zbus 初始化的持续时间。

  * 新增隔离通道消息订阅者池的方法。
    某些通道现在可共享隔离池
    以避免交付失败并缩短通信延迟。
    只需启用 :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_POOL_ISOLATION`
    并使用 :c:func:`zbus_chan_set_msg_sub_pool` 函数
    更改通道使用的消息池。
    通道可共享同一消息池。

HAL
****

* Nordic

  * nrfx 更新到 3.5.0 版本。
  * 新增 nRF Services（nrfs）库。

* STM32

  * STM32F0 更新到 cube 版本 V1.11.5。
  * STM32F3 更新到 cube 版本 V1.11.5。
  * STM32F4 更新到 cube 版本 V1.28.0。
  * STM32F7 更新到 cube 版本 V1.17.2。
  * STM32G0 更新到 cube 版本 V1.6.2。
  * STM32G4 更新到 cube 版本 V1.5.2。
  * STM32H5 更新到 cube 版本 V1.2.0。
  * STM32H7 更新到 cube 版本 V1.11.2。
  * STM32L5 更新到 cube 版本 V1.5.1。
  * STM32U5 更新到 cube 版本 V1.5.0。
  * STM32WB 更新到 cube 版本 V1.19.1。
  * STM32WBA 更新到 cube 版本 V1.3.1。
  * 新增 STM32H7R/S，cube 版本 V1.0.0。

* ADI

  * 引入 ``hal_adi`` 模块，
    它是 Maxim 软件开发套件（MSDK）的子集，
    包含设备头文件和裸机外设驱动（:github:`72391`）。

* Espressif

  * HAL 更新到 v5.1 版本，包含新 SoC 底层文件。

MCUboot
*******

  * 修复 bootutil HKDF 实现中的内存泄漏

  * 强制 TLV 条目受保护

  * 修复禁用指令/数据缓存

  * 修复估计镜像开销大小计算

  * 修复 swap-move 算法无法验证多镜像的问题

  * 修复 imgtool 中 align 脚本错误

  * 修复 imgtool 中 hex 文件格式的 img verify

  * 修复读取闪存镜像复位向量的问题

  * 修复 mbedtls 中过早的 ``check_config.h`` 包含

  * 重构镜像依赖函数以减小代码大小

  * 为 ``ESP32-C6`` 新增 MCUboot 支持

  * 新增可选 MCUboot boot 横幅

  * 新增受保护区域的 TLV 查询

  * 在 bootutil 中新增使用内置密钥进行验证

  * 为 PSA Crypto 后端新增内置 ECDSA 密钥支持

  * 为次级镜像新增 ``OVERWRITE_ONLY_KEEP_BACKUP`` 选项

  * 新增 ``SOC_FLASH_0_ID`` 和 ``SPI_FLASH_0_ID`` 的定义

  * 修复 mbedtls 版本 >= 3.1 的 ASN.1 支持

  * 修复 ``boot_read_enc_key`` 中 bootutil 的有符号/无符号比较

  * 更新 imgtool version.py 以接受命令行参数

  * 新增 imgtool dumpinfo 改进

  * 修复多个 imgtool dumpinfo 问题

  * 修复 imgtool verify 命令用于 edcsa-p384 签名镜像

  * 新增 NXP MCXN947 支持

  * 本版本中的 MCUboot 版本为 ``2.1.0+0-dev``。

OSDP
****

* 修复 CP 安全通道握手中的问题，
  其中 R-MAC 可被流氓 PD 发送乱序安全通道响应
  回退到旧值，导致重放攻击。

Trusted Firmware-M
******************

* TF-M 更新到 2.1.0。
  发布说明可参见：
  https://tf-m-user-guide.trustedfirmware.org/releases/2.1.0.html

* 新增对 RSA-3072 以外的 MCUboot 签名类型的支持。
  类型可通过 :kconfig:option:`CONFIG_TFM_MCUBOOT_SIGNATURE_TYPE`
  Kconfig 选项选择。
  使用 EC-P256（新默认值）与 RSA 相比
  可减少数 KB 的闪存使用。

LVGL
****

LVGL 更新到 8.4.0。
发布说明可参见：
https://docs.lvgl.io/8.4/CHANGELOG.html#v8-4-0-19-march-2024

此外，Zephyr 中做了以下变更：

  * 通过启用 :kconfig:option:`CONFIG_LV_Z_MEMORY_POOL_CUSTOM_SECTION`
    新增将内存池缓冲区放在 ``.lvgl_heap`` 段中的支持

  * 删除基于 kscan 的指针输入封装代码。

  * 更正编码器按钮行为以正确发出 ``LV_KEY_ENTER`` 事件。

  * 改进 :samp:`invert-{x,y}` 和 ``swap-xy`` 配置的处理。

  * 在文件关闭时新增 ``LV_MEM_CUSTOM_FREE`` 调用。

  * 新增 DMA2D 符号缺失的 Kconfig 桩。

  * 集成 LVGL rounder 回调函数支持。

测试与示例
*****************

  * 新增片段以在 ``west build`` 期间通过传递 ``-S nus-console``
    轻松启用 Bluetooth LE 上的 UART。
    该片段设置 :kconfig:option:`CONFIG_BT_ZEPHYR_NUS_AUTO_START_BLUETOOTH`，
    允许使用 UART API 的非 Bluetooth 示例
    无需修改即可运行（例如：Console 和 Logging 示例）。

  * 从示例 ``net/cloud/tagoio`` 和 ``net/mgmt/updatehub``
    中删除 ``GSM_PPP`` 特定配置 overlay。
    ``GSM_PPP`` 设备驱动已弃用并删除。
    替代它的 ``MODEM_CELLULAR`` 设备驱动
    使用原生网络堆栈和 ``PM`` 子系统，
    与以太网类似，无需应用程序特定操作即可设置网络。

  * 删除 ``net/gsm_modem`` 示例，
    因为它依赖的 ``GSM_PPP`` 设备驱动已弃用并删除。
    该示例已被基于 ``MODEM_CELLULAR`` 设备驱动的
    示例 ``net/cellular_modem`` 替代。

  * BT LE Coded PHY 现在在 CI 中使用 nrf5x bsim 目标
    进行运行时测试。

  * 在 ``tests/net`` 测试中禁用外部以太网网络接口，
    因为这些测试旨在使用模拟网络接口。

问题相关项
*******************

已知问题
============

- :github:`74345` - Bluetooth: 在 nRF51 上因故障无法工作
