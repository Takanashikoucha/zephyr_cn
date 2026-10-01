:orphan:

.. _zephyr_3.4:

Zephyr 3.4.0
############

我们很高兴地宣布 Zephyr 版本 3.4.0 的发布。

本次发布的主要增强功能包括：

* 输入子系统：处理来自各种类型输入设备的输入事件，并将其分发到应用中的其他线程。
* Barrier API：新增对数据内存屏障的架构无关 API。
* USB 设备支持：

  * USB 设备控制器 API（UDC API）和 nRF USBD 控制器驱动。
  * 使用新 UDC API 的 USB 设备栈实现。

* 为 USB-C 栈新增 Power Delivery Source 支持。
* 蓝牙：新增对带响应的周期性广播（PAwR）的支持。
* 缓存 API 函数现在完全由编译器内联。
* 新增对实时时钟（RTC）的 API。
* 新增 Retention 子系统。
* 为 Xtensa 新增 MMU 的初步支持。
* SMBus（系统管理总线）API。
* 对测试框架和 twister 的各种改进：

  - 在 twister 中引入 3 个新的测试框架，支持 pyTest、GoogleTest 和 Robot Framework。
  - 完成向新 Ztest API 的过渡，并弃用遗留 Ztest。

* 新增 Snippets：支持可跨平台使用的通用配置设置。

以下各节按组件提供详细的变更列表。

安全漏洞相关
******************************

本次发布解决了以下 CVE：

更详细的信息可参见：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2023-1901：截至 2023-07-04 处于保密期

* CVE-2023-1902：截至 2023-07-04 处于保密期

API 变更
***********

本次发布中的变更
=======================

* 使用 mcuboot 映像管理器（:kconfig:option:`CONFIG_MCUBOOT_IMG_MANAGER`）的任何应用现在还需要选择 :kconfig:option:`CONFIG_FLASH_MAP` 和 :kconfig:option:`CONFIG_STREAM_FLASH`，这防止 cmake 依赖循环，如果映像管理器 Kconfig 被手动启用而没有同时手动启用其他选项。

* 在应用中包含 hawkbit 现在需要选择额外的 Kconfig 选项，之前这些选项会自动选择，但已从 Kconfig 文件中的 ``select`` 选项更改为 ``depends on``：

    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_NVS`                     |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_FLASH`                   |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_FLASH_MAP`               |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_STREAM_FLASH`            |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_REBOOT`                  |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_HWINFO`                  |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_NET_TCP`                 |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_NET_SOCKETS`             |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_IMG_MANAGER`             |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_NETWORKING`              |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_HTTP_CLIENT`             |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_DNS_RESOLVER`            |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_JSON_LIBRARY`            |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_NET_SOCKETS_POSIX_NAMES` |
    +--------------------------------------------------+
    | :kconfig:option:`CONFIG_BOOTLOADER_MCUBOOT`      |
    +--------------------------------------------------+

* 在应用中包含 updatehub 现在需要选择额外的 Kconfig 选项，之前这些选项会自动选择，但已从 Kconfig 文件中的 ``select`` 选项更改为 ``depends on``：

   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_FLASH`                   |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_STREAM_FLASH`            |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_FLASH_MAP`               |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_REBOOT`                  |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_MCUBOOT_IMG_MANAGER`     |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_IMG_MANAGER`             |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_IMG_ENABLE_IMAGE_CHECK`  |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_BOOTLOADER_MCUBOOT`      |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_MPU_ALLOW_FLASH_WRITE`   |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_NETWORKING`              |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_NET_UDP`                 |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_NET_SOCKETS`             |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_NET_SOCKETS_POSIX_NAMES` |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_COAP`                    |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_DNS_RESOLVER`            |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_JSON_LIBRARY`            |
   +--------------------------------------------------+
   | :kconfig:option:`CONFIG_HWINFO`                  |
   +--------------------------------------------------+

* 传感器驱动 API 澄清 :c:func:`sensor_trigger_set`，说明用户分配的传感器触发器将由驱动作为指针存储，而不是副本，并传回到处理程序。这使处理程序能够使用 :c:macro:`CONTAINER_OF` 在触发器嵌入在更大的结构体中时获取上下文指针，并要求触发器不分配在栈上。在栈上分配传感器触发器的应用需要更新。

* 将几个驱动转换到 :ref:`input` 子系统。

  * ``gpio_keys``：从 ``gpio`` 移出，替换自定义 API 以使用输入事件代替，:dtcompatible:`zephyr,gpio-keys` 绑定未更改，但现在需要设置 ``zephyr,code``。
  * ``ft5336``：从 ``kscan_api`` 移至 :ref:`input`，将 Kconfig 选项从 ``CONFIG_KSCAN_FT5336``、``CONFIG_KSCAN_FT5336_PERIOD`` 和 ``KSCAN_FT5336_INTERRUPT`` 重命名为 :kconfig:option:`CONFIG_INPUT_FT5336`、:kconfig:option:`CONFIG_INPUT_FT5336_PERIOD` 和 :kconfig:option:`CONFIG_INPUT_FT5336_INTERRUPT`。
  * ``kscan_sdl``：从 ``kscan_api`` 移至 :ref:`input`，将 Kconfig 选项从 ``KSCAN_SDL`` 重命名为 :kconfig:option:`CONFIG_INPUT_SDL_TOUCH`，将 compatible 从 ``zephyr,sdl-kscan`` 重命名为 :dtcompatible:`zephyr,input-sdl-touch`。
  * ``nuvoton,npcx-kscan`` 移至 :ref:`input`，将 Kconfig 选项名从 ``KSCAN_NPCX_...`` 重命名为 ``INPUT_NPCX_KBD...``，将 compatible 从 ``nuvoton,npcx-kscan`` 重命名为 :dtcompatible:`nuvoton,npcx-kbd`。
  * 转换为使用输入 API 的触摸屏驱动可以使用 :dtcompatible:`zephyr,kscan-input` 驱动以保持 Kscan 兼容性。

* :c:func:`main` 的声明已从 ``void main(void)`` 更改为 ``int main(void)``。main 函数要求返回值零。所有其他返回值均保留。这使 Zephyr 与 C 和 C++ 语言规范对 "hosted" 环境的要求保持一致，避免编译器警告和错误。这些编译器消息在应用在 "hosted" 模式（即没有 ``-ffreestanding`` 编译器标志）下构建时生成。由于 ``-ffreestanding`` 标志目前在应用使用 picolibc 时启用，因此目前只有使用 picolibc 的应用会受到此更改的影响。

* 以下网络接口 API 现在接受额外的 ``struct net_if * iface`` 参数：

  * :c:func:`net_if_ipv4_maddr_join`
  * :c:func:`net_if_ipv4_maddr_leave`
  * :c:func:`net_if_ipv6_maddr_join`
  * :c:func:`net_if_ipv6_maddr_leave`

* MCUmgr 传输现在需要在注册之前设置结构体，通过将函数指针设置为函数处理程序，这些已移至类型为 :c:struct:`smp_transport_api_t` 的 ``functions`` 结构体对象。由于这些更改，遗留传输注册函数和对象不再可用。注册函数现在返回一个值，成功为 0，如果发生错误则为负错误代码。

* 为 :c:struct:`dac_channel_cfg` 中的 DAC 通道新增新标志 :c:struct:`dac_channel_cfg` ``buffered``，以允许配置输出缓冲。此的实际解释取决于硬件，目前仅为 STM32 DAC 驱动实现。隐式地对于此驱动，这将默认从缓冲更改为无缓冲。

* MCUmgr fs_mgmt 组的文件访问钩子现在为所有 fs_mgmt 组函数调用（添加对文件状态和文件哈希/校验和的支持）。此外，如果文件访问状态未丢失，它现在将仅为文件访问调用一次，而不是每次收到命令时调用。请注意通知的结构已更改，``upload`` bool 已被枚举替换，以指示使用的函数，参见 :c:struct:`fs_mgmt_file_access` 了解新结构定义。

* 可迭代部分 API 现在可用于 :zephyr_file:`include/zephyr/sys/iterable_sections.h`。LD 链接器 snippets 可用于 :zephyr_file:`include/zephyr/linker/iterable_sections.h`。

* 缓存 API 函数现在完全由编译器内联。

* 蓝牙 HCI 头文件已重新设计，``hci.h`` 现在仅包含函数原型，新的 ``hci_types.h`` 定义所有 HCI 相关宏和结构体。之前的 ``hci_err.h`` 已合并到 ``hci_types.h``。

* 遗留 Ztest API 已弃用。所有新测试应使用新 Ztest API。

本次发布中的稳定 API 变更
==================================

* 移除 ``bt_set_oob_data_flag`` 并用两个新 API 调用替换它：
  * :c:func:`bt_le_oob_set_sc_flag` 用于设置/清除 SC 配对中的 OOB 标志
  * :c:func:`bt_le_oob_set_legacy_flag` 用于设置/清除遗留配对中的 OOB 标志

* :c:macro:`SYS_INIT` 回调不再需要 :c:struct:`device` 参数。新回调签名是 ``int f(void)``。自动迁移现有项目的工具脚本可在 :zephyr_file:`scripts/utils/migrate_sys_init.py` 中找到。

* 将 :c:struct:`spi_config` ``cs``（:c:struct:`spi_cs_control`）从指针更改为结构体成员。这允许在 C++ 中使用现有 SPI dt-spec 宏。对 ``cs`` 字段执行 ``NULL`` 检查以检查 CS 是否基于 GPIO 的 SPI 控制器驱动现在必须使用 :c:func:`spi_cs_is_gpio` 或 :c:func:`spi_cs_is_gpio_dt` 调用。

本次发布中的新 API
========================

* 引入 :c:func:`flash_ex_op` 函数。这允许对闪存设备执行额外的操作，由 Zephyr 闪存 API 或供应商特定头文件定义。对额外操作的支持由 :kconfig:option:`CONFIG_FLASH_EX_OP_ENABLED` 启用，该选项依赖于由驱动选择的 :kconfig:option:`CONFIG_FLASH_HAS_EX_OP`。

* 引入 :ref:`rtc_api` API，为实时时钟设备添加实验性支持。这些设备之前使用 :ref:`counter_api` API 结合 unix-time 和 broken-down time 之间的转换。新 API 添加强制函数 :c:func:`rtc_set_time` 和 :c:func:`rtc_get_time`，可选函数 :c:func:`rtc_alarm_get_supported_fields`、:c:func:`rtc_alarm_set_time`、:c:func:`rtc_alarm_get_time`、:c:func:`rtc_alarm_is_pending` 和 :c:func:`rtc_alarm_set_callback` 由 :kconfig:option:`CONFIG_RTC_ALARM` 启用，可选函数 :c:func:`rtc_update_set_callback` 由 :kconfig:option:`CONFIG_RTC_UPDATE` 启用，最后，可选函数 :c:func:`rtc_set_calibration` 和 :c:func:`rtc_get_calibration` 由 :kconfig:option:`CONFIG_RTC_CALIBRATION` 启用。

* 为辅助（基于字母数字的）显示引入 :ref:`auxdisplay_api`。

* 为 barrier 操作引入 :ref:`barriers_api`。

* 新增 :c:macro:`CAN_FRAME_ESI` CAN-FD 错误状态指示器标志。

内核
******

* 移除绝对符号 :c:macro:`___cpu_t_SIZEOF`、:c:macro:`_STRUCT_KERNEL_SIZE`、:c:macro:`K_THREAD_SIZEOF` 和 :c:macro:`_DEVICE_STRUCT_SIZEOF`

架构
*************

* ARC

  * 新增 MPUv8 支持
  * 新增对 ARC hostlink 通道上虚拟 UART 的支持
  * 改进 ARCv2 HS4x 处理器处理 - 新增适当的 Kconfig 选项，提供默认 mcpu
  * 改进 ARCMWDT 工具链处理：

    * 新增回滚以在 ARCMWDT_TOOLCHAIN_PATH 缺失时检查 METAWARE_ROOT
    * 重新设计 twister 中额外警告选项处理，使其可以与 ARCMWDT 一起使用
    * 默认使用 64bit MDB 二进制

  * 修复启用 MPU 且 ROM & RAM 位于不同内存区域时的过度 ROM 内存消耗
  * 修复 ARCMWDT 情况下的 DSP 寄存器处理
  * 改进 SMP 处理：

    * 修复线程中止由于异常导致的潜在活锁
    * 修复 IDU 掩码设置

  * 移除绝对符号 :c:macro:`___callee_saved_t_SIZEOF` 和 :c:macro:`_K_THREAD_NO_FLOAT_SIZEOF`

* ARM

  * 移除绝对符号 :c:macro:`___basic_sf_t_SIZEOF`、:c:macro:`_K_THREAD_NO_FLOAT_SIZEOF`、:c:macro:`___cpu_context_t_SIZEOF` 和 :c:macro:`___thread_stack_info_t_SIZEOF`
  * 为 Cortex-M55 启用 fp16
  * 修复 arm-clang 和 TrustZone 的编译问题
  * 实现新 cache-management API
  * 新增对生成 zImage 头的支持
  * 在 CPU 空闲时引入新 :c:func:`z_arm_on_enter_cpu_idle` 钩子

* ARM64

  * 移除绝对符号 :c:macro:`___callee_saved_t_SIZEOF`
  * 为 v8r aarch64 启用 FPU 和 FPU_SHARING
  * 修复复位期间的 STACK_INIT 逻辑
  * 引入并启用安全异常栈
  * 修复 SMP 与 FPU 共享时的潜在死锁
  * 在 SCTLR 修改后添加 ISBs

* NIOS2

  * 移除绝对符号 :c:macro:`_K_THREAD_NO_FLOAT_SIZEOF`

* POSIX：

  * 新增 :c:macro:`Z_SPIN_DELAY`，允许在测试和示例中条件编译此架构的 k_busy_wait()。

* RISC-V

  * 新增 :kconfig:option:`CONFIG_PMP_NO_TOR`、:kconfig:option:`CONFIG_PMP_NO_NA4`，和 :kconfig:option:`CONFIG_PMP_NO_NAPOT`，允许禁用不支持的 PMP 范围模式。
  * 移除未使用符号：:c:macro:`_thread_offset_to_tp`、:c:macro:`_thread_offset_to_priv_stack_start`、:c:macro:`_thread_offset_to_user_sp`。
  * 新增对使用 :kconfig:option:`CONFIG_PMP_GRANULARITY` 设置 PMP 粒度的支持。
  * 从内联汇编访问 CSRs 切换为使用 :c:func:`csr_read` 辅助函数。
  * 启用单线程支持。

* SPARC

  * 移除绝对符号 :c:macro:`_K_THREAD_NO_FLOAT_SIZEOF`

* Xtensa

  * 修复嵌套中断期间的跨栈调用机制，该机制在某些条件下会导致栈损坏。
  * 为 Xtensa 新增 MMU 的初步支持。
  * 现在支持在禁用 :kconfig:option:`CONFIG_MULTITHREADING` 时构建，因此目标可以运行仅单线程操作。
  * 新增 C 结构体以表示中断帧，以帮助调试。

蓝牙
*********

* 通用

  * 将所有日志符号集中到一个新的 ``Kconfig.logging`` 文件中。
  * 弃用 ``BT_DEBUG_LOG`` 选项。应改用 ``BT_LOG``。
  * 将 ``BT_LOG`` 和 ``BT_LOG_LEGACY`` 选项设为隐藏。
  * 完全移除 ``BT_DEBUG``。

* 音频

  * 实现 CAP 发起方广播音频启动、停止和元数据更新过程。
  * 实现 CAP 单播音频启动、停止和元数据更新过程。
  * 实现电话和媒体音频服务（TMAS）。
  * 为 MCC 和 MCS 添加额外验证，包括操作码、值等。
  * 重构并扩展扫描委托器实现，包括与广播汇点的集成。
  * 新增支持从 PA 汇点创建广播汇点。
  * 新增支持 CSIP 中的可选特征。
  * 实现通过 UUID 发现而不是通过 UUID 读取多个特征。
  * 新增支持多个配置文件中的长读取和写入。
  * 新增支持长 BAP ASE 通知并优化长通知读取。
  * 将 MCS 通知卸载到系统工作队列。
  * 新增 CAP 发起方取消过程。

* 方向查找

* 主机

  * 将主机更新到 v5.4 规范。
  * GATT DB 哈希现在在加载设置时重新计算。
  * 新增对 SMP 按键通知的实验性支持。
  * 降低某些日志消息的严重性以避免日志泛滥。
  * 将 LE SC OOB 配对的处理从遗留 OOB 逻辑中分离。
  * 实现加密广播数据功能。
  * 新增对新的带响应的周期性广播（PAwR）的支持，既作为广播器也作为扫描器。
  * 新增支持从 PAwR 发起连接，以及在同步时接收连接。
  * 澄清 ``BT_PRIVACY`` Kconfig 选项启用的行为。
  * 引入新的 ``seg_recv`` L2CAP API，供应用直接接收段并显式管理信用。

* 网状

  * 新增对网状协议 d1.1r18 规范（由新的配置选项控制）的实验性支持。这包括：

    * 增强配置认证支持。
    * 网状远程配置支持，包括：

      * 远程配置服务器和客户端模型。
      * 组成数据页 128 和模型元数据页 128 支持。

    * 大型组成数据支持，包括：

      * 大型组成数据服务器和客户端模型。
      * 模型元数据页 0 支持。

    * 新的传输分片和重组（SAR）实现，包括：

      * SAR 配置服务器和客户端模型。

    * 网状私有信标支持，包括：

      * 网状私有信标服务器和客户端模型。

    * 操作码聚合器支持，包括：

      * 操作码聚合器服务器和客户端模型。

    * 代理请求支持，包括：

      * 请求 PDU RPL 配置服务器和客户端模型。
      * 按需私有代理服务器和客户端模型。

    * 组成数据页 1 支持。
    * 其他网状配置文件增强。
  * 新增对网状二进制大对象传输模型 d1.0r04_PRr00 规范（由新的配置选项控制）的实验性支持。
  * 新增对网状设备固件更新模型 d1.0r04_PRr00 规范（由新的配置选项控制）的实验性支持。
  * 修复多个配置文件错误。
  * 新增对 PSA 加密 API（由新的配置选项控制）的实验性支持。
  * 新增一个工作队列以存储网状设置，包括用于存储用户数据的新 API。
  * 禁用 C++ 的模型初始化宏，因为它们使用 C99 的复合字面量特性。
  * 移除已弃用的健康客户端和配置客户端 API。

* 控制器

  * 实现支持具有多个 CIS 使用场景的中心。
  * 实现支持多个外围 CIS 建立。
  * 将控制器更新到 v5.4 规范。
  * 新增支持与其他收发器共存。
  * 新增支持按顺序进行多个 CIS/CIG 设置/连接和拆除过程。
  * 扩展 ticker API 以返回过期信息。
  * 使用新的 ticket 过期信息特性重新实现扩展和周期性广播以及广播 ISO。
  * 修改 ticker 实现以重新调度使用 ``ticks_slot_window`` 的未保留 ticker。使用它实现连续扫描。
  * 新增支持在 SDU 分片中考虑 SDU 间隔，连同数据包序列号和时间戳。
  * 新增 ``BT_CTLR_TX_PWR_DBM`` 选项以直接以 dBm 设置发射功率。
  * 通过支持在已分配的 RX 节点上搭载通知优化 RX 路径。

* HCI 驱动

板级和 SoC 支持
********************

* 新增对这些 SoC 系列的支持：

  * 现在支持 STM32C0 系列（通过引入 STM32C031 SoC）。
  * 现在支持 STM32H5 系列（通过引入 STM32H503 和 STM32H573 SoC）。
  * 新增对 STM32U599 SoC 变体的支持
  * Nordic Semiconductor nRF9161

* 移除对这些 SoC 系列的支持：

* 对其他 SoC 系列进行以下更改：

* 新增对这些 ARC 板级的支持：

  * DesignWare ARC HS4x/HS4xD 开发套件（HSDK4xD）- ARCv2 HS47D，SMP 4 核
  * nsim_hs3x_hostlink - 基于 hostlink UART 的仿真（nSIM 基础）平台

* 新增对这些 ARM 板级的支持：

  * Aconno ACN52832
  * Alientek STM32L475 Pandora
  * Arduino GIGA R1 Wi-Fi
  * BeagleConnect Freedom
  * Infineon PSoC™ 6 BLE 原型套件（CY8CPROTO-063-BLE）
  * Infineon PSoC™ 6 Wi-Fi BT 原型套件（CY8CPROTO-062-4343W）
  * Infineon XMC4700 Relax Kit
  * MXChip AZ3166 IoT DevKit
  * Nordic Semiconductor nRF9161 DK
  * NXP MIMXRT1040-EVK
  * NXP MIMXRT1062 FMURT6
  * PHYTEC PhyBOARD Polis（NXP i.MX8M Mini）
  * PHYTEC PhyBOARD Pollux（NXP i.MX8M Plus）
  * Raspberry Pi Pico W
  * Raytac MDBT50Q-DB-33
  * Raytac MDBT50Q-DB-40
  * Seeed Studio Wio Terminal
  * Seeed Studio XIAO BLE Sense
  * Silicon Labs BRD2601B
  * Silicon Labs BRD4187C
  * Silicon Labs EFR32 Thunderboard 风格板级
  * ST Nucleo C031C6
  * ST Nucleo F042K6
  * ST Nucleo H563ZI
  * ST STM32H573I-DK Discovery
  * Xilinx KV260（Cortex-R5）

* 新增对这些 ARM64 板级的支持：

  * PHYTEC phyCORE-AM62x A53
  * NXP i.MX93 EVK A55（SOF 变体）

* 新增对这些 RISC-V 板级的支持：

  * Intel FPGA Nios® V/m
  * ITE IT82XX2 EV-Board

* 新增对这些 X86 板级的支持：

* 新增对这些 Xtensa 板级的支持：

  * ESP32S3-DevKitM

* 对这些 ARC 板级进行以下更改：

  * 为 qemu_arc_hs 新增 ARC MWDT 工具链支持
  * 改进 emsdp 平台支持：

    * 新增 DFSS 驱动支持
    * 新增 pinctrl 支持

* 对这些 ARM 板级进行以下更改：

  * ``atsamc21n_xpro``：启用 CAN 支持。
  * ``atsame54_xpro``：从 I2C 读取以太网 MAC。
  * 将 Nordic 板级 ``nrf9160dk_nrf9160`` 和 ``nrf9160dk_nrf52840`` 的默认板级修订版本更改为 0.14.0。要为不带外部闪存的 nRF9160 DK 的较旧修订版本构建，请在构建时指定该较旧板级修订版本。
  * ``nrf9160dk_nrf52840``：默认启用 external_flash_pins_routing 开关。
  * ``nrf9160dk_nrf9160``：更改 GPIO 扩展器上按钮和开关的顺序以匹配直接在 nRF9160 SoC 上使用 GPIO 时的顺序。
  * ``STM32H747i_disco``：启用对 ST B-LCD40-DSI1 显示扩展的支持
  * ``qemu_cortex_m0``：修复系统定时器的预分频器，使其频率实际为 1 MHz，而不是 2 MHz。

* 对这些 ARM64 板级进行以下更改：

  * FVP revc_2xaemv8a / aemv8r：新增以太网、PHY 和 MDIO 节点

* 对 POSIX 板级进行以下更改：

   * nrf52_bsim 现在包括以下支持和模型：

     * RADIO 中的 802.15.4。
     * EGU。
     * FLASH（NVMC & UICR）。
     * TEMP。
     * 连接到主机 ptty 的 UART。
     * 许多其他小 CMSIS API 和 nRF API 和驱动。

* 对这些 RISC-V 板级进行以下更改：

  * ``gd32vf103``：不再需要特殊 OpenOCD 版本。

* 对这些 X86 板级进行以下更改：

* 对这些 Xtensa 板级进行以下更改：

* 移除对这些 ARC 板级的支持：

* 移除对这些 ARM 板级的支持：

* 移除对这些 RISC-V 板级的支持：

  * BeagleV Starlight JH7100

* 移除对这些 X86 板级的支持：

* 移除对这些 Xtensa 板级的支持：

* 对其他板级进行以下更改：

* 新增对这些以下屏蔽板的支持：

  * Adafruit Data Logger Shield
  * nPM1300 EK（电源管理集成电路（PMIC））
  * Panasonic Grid-EYE Shields
  * ST B_LCD40_DSI1_MB1166

构建系统和基础设施
*******************************

* 修复一个问题，其中使用了较旧版本的 Zephyr SDK 工具链而不是最新兼容版本。

* 修复一个问题，其中使用 sysbuild 构建应用并指定 mcuboot 的验证仅为校验和时未构建可启动映像。

* 修复一个问题，其中如果不存在 prj.conf 文件则板级配置文件不会通过发出致命错误包含。结果，prj.conf 文件现在在项目中是强制性的。

* 引入支持在 zephyr 中扩展/替换签名机制，参见 :ref:`West extending signing <west-extending-signing>` 了解进一步详细信息。

* 修复一个问题，其中在使用 ``*_ROOT`` 变量与 Sysbuild 时，这些对映像丢失。

* 增强 ``zephyr_get`` CMake 辅助函数以可选支持将作用域变量合并到列表中。

* 新增用于设置/更新 sysbuild CMake 缓存变量的新 CMake 辅助函数：``sysbuild_cache_set``。

* 增强 ``zephyr_get`` CMake 辅助函数以查找多个变量并将结果返回到不同名称的变量中。

* 引入 ``EXTRA_CONF_FILE``、``EXTRA_DTC_OVERLAY_FILE``，和 ``EXTRA_ZEPHYR_MODULES`` 以更好地命名一致性和统一行为以在 Zephyr 自动构建设置查找之外应用额外构建设置。
  ``EXTRA_CONF_FILE`` 替换 ``OVERLAY_CONFIG``。
  ``EXTRA_ZEPHYR_MODULES`` 替换 ``ZEPHYR_EXTRA_MODULES``。
  ``EXTRA_DTC_OVERLAY_FILE`` 是新的，参见
  :ref:`Set devicetree overlays <set-devicetree-overlays>` 了解进一步详细信息。

* Twister 现在支持 ``gtest`` 框架以运行用 gTest 编写的测试。

* 新增用于在构建时验证设备初始化优先级的选项。要使用它，启用 :kconfig:option:`CONFIG_CHECK_INIT_PRIORITIES`，参见
  :ref:`check_init_priorities.py` 了解更多详细信息。

* 新增用于在编译时禁用宏扩展跟踪的新选项，
  :kconfig:option:`CONFIG_COMPILER_TRACK_MACRO_EXPANSION`。此选项可以
  禁用以减少在宏扩展期间发生错误时的编译器冗长性，e.g. 在设备定义宏中。

* Twister 现在支持通过使用 ``--alt-config-root`` 从替代根
  文件夹/s 加载测试配置。当找到测试时，Twister 将
  检查测试配置文件是否存在于任何替代测试
  配置根文件夹中。例如，给定
  ``$test_root/tests/foo/testcase.yaml``，Twister 将使用
  ``$alt_config_root/tests/foo/testcase.yaml`` 如果它存在。

* Twister 现在使用原生 YAML 列表用于之前使用
  空格分隔字符串定义的字段。例如：

  .. code-block:: yaml

     platform_allow: foo bar

  现在可以写成：

  .. code-block:: yaml

     platform_allow:
       - foo
       - bar

这适用于以下属性：

    - ``arch_exclude``
    - ``arch_allow``
    - ``depends_on``
    - ``extra_args``
    - ``extra_sections``
    - ``platform_exclude``
    - ``platform_allow``
    - ``tags``
    - ``toolchain_exclude``
    - ``toolchain_allow``

  请注意，旧的行为作为已弃用保留。
  :zephyr_file:`scripts/utils/twister_to_list.py` 脚本可用于
  自动迁移 Twister 配置文件。

* 当启用 MCUboot 映像签名时，如果项目中未设置签名密钥，cmake 现在将发出警告，
  如果签名是手动或在 zephyr 之外执行的，可以安全地忽略此警告。
  此警告通知用户生成的映像按原样将不可由 MCUboot 启动。

* Babblesim 现在包含在 west 清单中。用户可以通过
  west config 启用 ``babblesim`` 组来获取它。

* ``west sign`` 现在使用 "fixed-partition" 兼容节点的 DT 标签来识别
  应用映像插槽，而不是之前使用的 DT 节点标签属性。
  如果你一直在为 MCUboot 使用自定义分区布局，你将不得不
  用适当的 DT 节点标签标记你的 MCUboot 插槽分区；例如
  具有 "image-0" 标签属性的分区将不得不被给予 slot0_partition DT 节点标签。
  标签属性不必从分区节点中移除，但将不被使用。

  使用的 DT 节点标签列于下方

  .. table::
     :align: center

     +---------------------------------+---------------------------+
     | 具有标签属性的分区              | 必需的 DT 节点标签        |
     +=================================+===========================+
     | "image-0"                       | slot0_partition           |
     +---------------------------------+---------------------------+
     | "image-1"                       | slot1_partition           |
     +---------------------------------+---------------------------+

* 修复一个问题，其中为 ``BOARD_ROOT`` 值提供的相对路径
  可能错误地发出关于未找到 ``boards`` 目录的警告。

* 修复一个问题，其中相对路径对 sysbuild 映像不起作用。

驱动和传感器
*******************

* 设备模型

  * 不需要初始化例程的设备现在可以将 ``NULL``
    传递给 ``DEVICE_*_DEFINE()`` 宏。

* 辅助显示

  * 新增辅助显示（auxdisplay）外设，这允许
    与不具有图形功能的简单字母数字显示进行接口。
    此外设被标记为不稳定。

  * 新增 HD44780 驱动。

  * 新增 Noritake Itron 驱动。

  * 新增 Grove LCD 驱动（从现有示例移植）。

* ADC

  * MCUX LPADC 驱动现在使用通道参数
    选择软件通道配置缓冲区。
    使用 ``zephyr,input-positive`` 和
    ``zephyr,input-negative`` 设备树属性
    选择要链接软件通道配置的
    硬件通道(s)。
  * MCUX LPADC 驱动 ``voltage-ref`` 和 ``power-level`` 设备树属性
    已移位以匹配参考手册中描述的硬件，
    而不是匹配 NXP SDK 枚举标识符。
  * 新增对 STM32C0 和 STM32H5 的支持。
  * 为 STM32H7 新增 DMA 支持。
  * STM32：分辨率现在为每个 ADC 实例
    列在设备树中
  * STM32：采样时间现在为每个 ADC 实例
    列在设备树中
  * 为 Atmel SAM 系列 ADC 新增驱动。
  * 为 Gecko 增量 ADC 新增驱动。
  * 为 Infineon CAT1 ADC 新增驱动。
  * 为 TI ADS7052 新增驱动。
  * 为 TI ADS114S0x 系列新增驱动。
  * 为 Renesas SmartBond GPADC 和 SDADC 新增驱动。

* 电池备份 RAM

  * 新增 MCP7940N 电池备份 RTC SRAM 驱动。

* CAN

  * CAN 统计现在在调用 :c:func:`can_start` 时
    重置。

  * 将 NXP FlexCAN 设备树绑定 compatible
    从 ``nxp,kinetis-flexcan``
    重命名为
    :dtcompatible:`nxp,flexcan`。

  * 新增对使用设备树绑定
    :dtcompatible:`nxp,flexcan-fd`
    的 NXP FlexCAN 控制器
    CAN-FD 变体的支持。

  * 新增对使用设备树绑定
    :dtcompatible:`nxp,s32-canxl`
    的 NXP NXP S32 CANEXCEL 控制器的支持。

  * 新增对使用设备树绑定
    :dtcompatible:`atmel,sam0-can`
    的 Atmel SAM0 CAN 控制器的支持。

  * 重构 Bosch M_CAN 控制器驱动后端
    以允许通过设备树
    进行每实例配置。

  * 现在支持 STM32H5 系列。

* 时钟控制

  * Atmel SAM/SAM0：引入外设时钟控制。
  * Atmel SAM0：改进 ``samd20``/``samd21``/``samr21`` 时钟机制。
  * STM32F4：新增对 PLL I2S 的支持

* 控制台：

  * native_posix 和 bsim 控制台驱动
    已合并为一个通用驱动，
    可供所有基于 POSIX 架构的板级使用。

* 计数器

  * 为 STM32H7 和 STM32H5 上的
    基于定时器的计数器新增支持
  * 为 STM32C0 和 STM32H5 上的
    基于 RTC 的计数器新增支持

* 加密

  * 为 STM32H5 AES 新增支持

* DAC

  * 为 STM32H5 系列新增支持。

* 磁盘

  * SDMMC STM32L4+：现在与内部 DMA 兼容
  * NVME 磁盘现在使用 FATFS 支持，
    启用单个 I/O 队列

* 显示

  * 改进 MCUX ELCDIF 和 SSD16XX 显示控制器驱动
  * 为 ILI9342C 显示控制器新增支持
  * 为 OTM8009A 面板新增支持

* DMA

  * STM32C0：新增对 DMA 的支持
  * STM32H5：新增对 GPDMA 的支持
  * STM32H7：新增对 BDMA 的支持
  * 为 RP2040 SoC 新增 DMA 支持

* EEPROM

  * 对于 I2C EEPROM 目标驱动，
    从 :dtcompatible:`atmel,at24`
    切换到专用的 :dtcompatible:`zephyr,i2c-target-eeprom`。

* 熵

  * 为 STM32H5 系列新增支持。

* 闪存

  * 引入新闪存 API 调用 :c:func:`flash_ex_op`，
    它调用由闪存驱动提供的
    :c:func:`ec_op` 回调。
    这允许对闪存设备执行
    额外的操作，
    由 Zephyr 闪存 API 或
    供应商特定头文件定义。
    :kconfig:option:`CONFIG_FLASH_HAS_EX_OP`
    应由驱动选择
    以指示支持额外的操作。
    要启用额外的操作，
    用户应选择
    :kconfig:option:`CONFIG_FLASH_EX_OP_ENABLED`。
  * STM32F4：现在通过
    新闪存 API 调用 :c:func:`flash_ex_op`
    支持写保护和读取保护。
  * nrf_qspi_nor：
    用 ``nrf_qspi_nor_xip_enable``
    替换自定义 API 函数
    ``nrf_qspi_nor_base_clock_div_force``，
    除了强制时钟分频器之外，
    还防止驱动停用 QSPI 外设，
    从而使 XIP 操作实际成为可能。
  * flash_simulator：

    * 内存区域现在可以用作
      闪存模拟器的存储区域。
      使用内存区域
      允许闪存模拟器
      在设备重启后
      保留其内容。
    * 在 native_posix 中构建时，
      已添加命令行选项
      以选择
      闪存是否应在启动时清除，
      闪存内容是否保留在 RAM 中，
      或闪存内容文件是否在退出时删除。

  * spi_flash_at45：
    修复擦除过程
    以正确处理
    其初始扇区
    分成两部分
    （通常标记为 0a 和 0b）
    的芯片。
  * STM32H5 现在支持 OSPI

* GPIO

  * 将 ``gpio_keys`` 驱动
    转换到输入子系统。
  * 为 RP2040 SoC
    新增单端 IO 支持

  * STM32：支持新引入的实验性 API 以无需重新配置来启用/禁用中断

* I2C

  * 为 STM32C0 和 STM32H5 系列新增支持

* I2S

  * STM32：域时钟现在应由设备树配置。

* 输入

  * 引入 :ref:`input` 子系统。

* KSCAN

  * 为 kscan 兼容性驱动新增 :dtcompatible:`zephyr,kscan-input` 输入。
  * 将 ``ft5336`` 和 ``kscan_sdl`` 驱动转换到输入子系统。

* MIPI-DSI

  * 为 STM32H7 新增支持

* 其他

   * 为 RP2040 SoC 新增 PIO 支持

* PCIE

  * 启用按类/修订版本过滤 PCIe 设备。

* PECI

* 保留内存

  * 已新增保留内存（retained_mem）驱动，
    具有
    Nordic nRF GPREGRET
    和
    未初始化 RAM
    的
    后端。

* 引脚控制

  * 为 Infineon CAT1 新增支持
  * 为 TI K3 新增支持
  * 为 ARC emdsp 新增支持

* PWM

  * 为 STM32C0 新增支持。
  * STM32：现在支持 6-PWM 通道
  * 为 Microchip XEC BBLED 新增 PWM 驱动。

* 电源域

* 调节器

  * 调节器 API 现在可以通过使用 :kconfig:option:`CONFIG_REGULATOR_THREAD_SAFE_REFCNT` 在没有线程安全引用计数的情况下构建。此功能可以在不启用 :kconfig:option:`CONFIG_MULTITHREADING` 的应用中有用。
  * 为 ADP5360 PMIC 新增支持
  * 为 nPM1300 PMIC 新增支持
  * 为 Raspberry Pi Pico 核心供电调节器新增支持

* SDHC

  * 新增支持，用于使用 CPOL/CPHA SPI 时钟模式与 SD 卡一起使用，因为某些卡需要 SPI 时钟在不活动时切换到低

* 传感器

  * 新增通用电压测量示例
  * 移除 STM32 Vbat 测量示例（被通用的替换）
  * 新增 STM32 Vref 传感器驱动
  * 新增 STM32 Vref/Vbat 测量通过新通用电压测量示例
  * 为 STM32C0 和 STM32F0x0 新增温度测量驱动
  * 移除 STM32 温度测量示例（被通用的替换）
  * 新增 STM32 温度测量通过通用温度测量示例

* 串行

  * 为 ``gd32vf103`` SoC 新增 UART3 和 UART4 配置。
  * uart_altera：为 Altera Avalon UART 新增驱动。
  * uart_emul：为仿真 UART 新增驱动。
  * uart_esp32：
    * 为 ESP32S3 SoC 新增支持。
    * 为 RS-485 半双工模式新增支持。
  * uart_hostlink：为通过 Synopsys ARC hostlink 通道的虚拟 UART 新增驱动。
  * uart_ifx_cat1：为 Infineon CAT1 UART 新增驱动。
  * uart_mcux：新增电源管理支持。
  * uart_mcux_flexcomm：为异步操作新增支持。
  * uart_mcux_lpuart：为奇偶校验新增支持。
  * uart_ns16550：现在支持每实例硬件访问模式，而不是所有实例的一个访问模式。
  * uart_pl011：修复中断支持。
  * uart_rpi_pico_pio：新增驱动以支持通过 Raspberry Pi Pico 上的可编程输入/输出（PIO）的 UART。
  * uart_xmc4xxx：为异步操作新增支持。
  * uart_stm32：现在支持驱动启用模式
  * 为 RP2040 SoC 新增硬件流控制支持

* SPI

  * 为 STM32H5 系列新增支持。

* 定时器

  * 新增支持，用于停止 Nordic nRF RTC 系统定时器，这修复了在启动在之前版本的 Zephyr 中构建的应用时的问题。

  * STM32：现在支持在时钟输入处的预分频器（默认不分频）。预分频器允许实现更高的 LPTIM 超时（当 lptim 由 LSE 时钟驱动时最高 256s），从而实现更高的核心睡眠持续时间，但影响 tick 精度。请谨慎使用。

* USB

   * 为 RP2040 SoC 新增远程唤醒支持
   * 新增电池充电（BC12）API 和 PI3USB9201 驱动实现。
   * 为 ITE IT82xx2 和 smartbond 平台新增 USB 设备控制器驱动（使用 usb_dc API）。
   * 为 UDC API 新增 USB 设备控制器驱动骨架。
   * 重新设计 DWC2 驱动并为 STM32F4 SoC 系列新增支持

* W1

  * 新增 DS2482-800 1-Wire 主驱动。参见 :dtcompatible:`maxim,ds2482-800` 设备树绑定了解更多详细信息。
  * 新增 :kconfig:option:`CONFIG_W1_NET_FORCE_MULTIDROP_ADDRESSING`，可以启用以强制 1-Wire 网络层使用多点寻址。

* 看门狗

  * 为 STM32C0 和 STM32H5 系列新增支持

网络
**********

* CoAP：

  * 新增 :c:func:`coap_append_descriptive_block_option` 和 :c:func:`coap_get_block1_option` API 以便于块传输处理。
  * 新增 :ref:`coap_client_interface` 辅助库，基于现有 CoAP API。
  * 修复 :c:func:`coap_header_get_token` 中缺失的 token 长度验证。
  * 修复 :c:func:`coap_response_received` 中缺失的响应检查。

* 连接管理器：

  * 用通用 L2 连接性 API 扩展库。
  * 大幅重构库内部。
  * 改进库中的线程安全。
  * 重新设计连接管理器事件如何通知 - 它们不再为每个接口单独引发，而是：

    * ``NET_EVENT_L4_CONNECTED`` 仅在第一个接口获得连接性后调用一次。
    * ``NET_EVENT_L4_DISCONNECTED`` 仅在所有接口失去连接性后调用。

  * 改进连接管理器测试覆盖。

* DHCPv4：

  * 修复 DHCPv4 输入处理程序中的潜在包泄漏。
  * 修复 ``dhcpv4_create_message()`` 中的潜在 NULL 指针解引用。
  * 新增机制以注册用于处理 DHCPv4 选项的回调。
  * 修改 ``dhcpv4_client`` 示例以在系统中的所有网络接口上触发 DHCP。

* DNS：

  * 修复在查询回调为 NULL 指针时的可能崩溃。
  * 新增在重新配置之前检查现有 DNS 服务器的检查。
  * 改进 DNS SD 中的调试日志。
  * 修复 mDNS 响应器中的 IPv4/IPv6 地址处理，如果两者都启用。
  * 移除 DNS SD 查询解析中的死代码。

* 以太网：

  * 修复在 ARP 请求传输错误的情况下双重包解引用。
  * 修复在以太网接口在 LLDP 初始化之前启用时的可能 slist 损坏。

* HTTP：

  * 新增 HTTP 服务和资源可迭代部分。

* ICMPv6：

  * 实现 IPv6 RA 递归 DNS 服务器选项处理。

* IEEE802154：

  * 修复 6LoWPAN IP 头压缩和分片的角落情况，其中对于短范围的包大小，分片在 IPHC 之后未正确工作。
  * 新增启动连续载波传输的新无线电 API 函数。
  * IEEE802154 L2 安全中的多个改进/修复。
  * 修复在处理信标/命令帧时的包泄漏。
  * 弃用 :kconfig:option:`CONFIG_IEEE802154_2015` Kconfig 选项。
  * 新增通过 IEEE802154 L2 的简单 Babblesim 回显测试。
  * 改进 IEEE802154 L2 测试覆盖。
  * 多个其他小 IEEE802154 L2 和文档改进/修复。

* IPv4：

  * 实现回退到 IPv4 链路本地地址，如果没有其他地址可用。
  * 修复 :c:func:`net_ipv4_is_ll_addr` 辅助函数以正确识别 LL 地址。
  * 修复 IPv4 分片中的可能 NULL 指针解引用。

* LwM2M：

  * 新增 :c:macro:`LWM2M_RD_CLIENT_EVENT_REG_UPDATE` 事件。
  * 在适用的地方新增 API 中缺失的 ``const`` 限定符。
  * 修复包传输时的套接字错误处理。
  * 改进回退到常规注册时的 LwM2M 上下文清理。
  * 新增注册回调函数以用于 FW 更新取消操作。
  * 新增注册回调函数以用于 LwM2M 发送操作。
  * 新增 ISPO 电压传感器对象支持。
  * 修复 LwM2M 客户端在挂起时的停止。
  * 修复小 CoAP RFC 不兼容性，其中不应假设块传输中的连续数据块将携带相同的 token。
  * 新增 TX 上的块传输支持。
  * 修复在创建 FW 更新对象时的可能越界内存访问。
  * 新增用专用回调函数（``set_socketoptions``）覆盖默认套接字选项配置的可能性。
  * 改进 LwM2M 测试覆盖。
  * 其他几个小改进和清理。

* 其他：

  * 为卸载设备新增通用 ``OFFLOADED_NETDEV_L2``，以允许卸载实现检测接口何时启用/禁用。
  * 将 ``net_buf_simple`` 例程分解到单独的源文件。
  * 修复 ``net_pkt_cursor_operate()`` 中的可能 NULL 指针解引用。
  * 重新实现 ``net_mgmt`` 以内部使用消息队列。这也修复了旧实现中的可能事件丢失。
  * 修复 ``net ping`` shell 命令中的错误处理以避免 shell 冻结。
  * 改进 ``net stats`` shell 命令中的以太网错误统计日志。
  * 将 SLIP TAP 实现移至单独文件，以防止关于以太网驱动缺失源文件的构建警告。
  * 修复 ``echo_server`` 和 ``echo_client`` 示例中的崩溃，当启用用户空间时。
  * 修复 ``mqtt_sn_publisher`` 示例中的 IPv6 支持。
  * 修复网络栈中与 arm-clang 的构建问题。
  * 新增 ``NET_IF_IPV6_NO_ND`` 和 ``NET_IF_IPV6_NO_MLD`` 接口标志，允许分别在接口上禁用 ND/MLD。
  * 重新设计网络接口互斥锁保护，以使用每个接口的单独互斥锁，而不是全局互斥锁。
  * 新增 :zephyr:code-sample:`aws-iot-mqtt`。
  * 在网络接口函数中新增几个缺失的 NULL 指针检查。

* OpenThread：

  * 实现以下 OpenThread 平台 API：

    * ``otPlatRadioSetMacFrameCounterIfLarger()``，
    * ``otPlatCryptoEcdsaGenerateAndImportKey()``，
    * ``otPlatCryptoEcdsaExportPublicKey()``，
    * ``otPlatCryptoEcdsaVerifyUsingKeyRef()``，
    * ``otPlatCryptoEcdsaSignUsingKeyRef()``。

  * 新增 :kconfig:option:`CONFIG_OPENTHREAD_CSL_TIMEOUT` 选项。
  * 移除不再需要的 ``CONFIG_OPENTHREAD_EXCLUDE_TCPLP_LIB``。
  * 新增通过 OpenThread 的简单 Babblesim 回显测试。

* SNTP：

  * 切换到内部使用 ``zsock_*`` 函数。

* 套接字：

  * 修复 ``SO_RCVBUF`` 和 ``SO_SNDBUF`` 套接字选项处理，使它们正确配置 TCP 窗口大小。
  * 修复 ``SO_SNDTIMEO`` 套接字选项处理 - 超时值被忽略，使用时套接字表现为非阻塞模式。
  * 重新设计 TLS 套接字实现，以允许从不同线程并行 TX/RX。
  * 实现 TLS 握手超时。
  * 为 TCP 套接字新增异步连接支持。
  * 修复阻塞 :c:func:`recv` 在套接字关闭时未被中断。
  * 修复阻塞 :c:func:`accept` 在套接字关闭时未被中断。
  * 改进套接字测试覆盖。

* TCP：

  * 通过改进包处理结果报告修复不正确的 TCP 统计。
  * 新增 :kconfig:option:`CONFIG_NET_TCP_PKT_ALLOC_TIMEOUT` 以允许配置包分配超时。
  * 改进 TCP 测试覆盖。
  * 修复 IPv6 的 TCP MSS 计算。
  * 修复重传数据的双重确认的可能。
  * 修复传入连接的本地地址设置。
  * 修复某些角落情况中的双重 TCP 上下文解引用。

* TFTP：

  * 新增 ``tftp_put()`` API 以支持 TFTP 写请求。
  * 引入 ``tftp_callback_t`` 回调以允许读取大文件。
  * 重新设计 ``struct tftpc`` 客户端上下文结构体，以允许从几个上下文并行通信。

* UDP：

  * :kconfig:option:`CONFIG_NET_UDP_MISSING_CHECKSUM` 现在默认启用。

* Websockets：

  * 在 :c:func:`websocket_recv_msg` 中实现适当的超时处理。
  * 修复解析长度字段时的隐式类型转换，这可能导致数据丢失。

* Wi-Fi：

  * 在 Wi-Fi shell 中显示 TWT（目标唤醒时间）配置响应状态。
  * 在 Wi-Fi shell 中新增更详细的 TWT 响应参数打印。
  * 新增 ``NET_EVENT_WIFI_TWT_SLEEP_STATE`` 事件以通知 TWT 睡眠状态。
  * 修复在扫描时并非所有安全模式都正确显示的问题。
  * 在发起 TWT 操作之前新增连接状态和 AP 能力验证。
  * TWT 间隔从毫秒更改为微秒，间隔变量也被重命名。
  * 用监听间隔和唤醒模式扩展省电配置参数。
  * 新增 :kconfig:option:`CONFIG_WIFI_MGMT_RAW_SCAN_RESULTS` 选项，启用用 ``NET_EVENT_WIFI_CMD_RAW_SCAN_RESULT`` 事件向应用提供 RAW（未处理）扫描结果。
  * Wi-Fi 管理/shell 模块中的其他几个小修复/清理。

* zperf

  * 为 TCP 基准测试新增禁用 Nagle 算法的额外参数。
  * 新增处理多个传入 TCP 会话的支持。
  * 使 zperf 线程优先级和栈大小可配置。
  * 模块中的几个小清理。

USB
***

* USB 设备支持

  * 修复 MPS 为 8 字节时的控制端点处理。

* 新的实验性 USB 支持

  * 新设备支持的多个改进，更好的字符串描述符支持，实现 usbd_class_shutdown API。
  * 为新设备支持新增 USB 大容量存储类和 CDC ECM 类实现。