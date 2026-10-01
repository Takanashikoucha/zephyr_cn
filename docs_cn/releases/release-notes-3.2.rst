:orphan:

.. _zephyr_3.2:

Zephyr 3.2.0
############

我们很高兴地宣布 Zephyr 版本 3.2.0 的发布。

本次发布的主要增强功能包括：

* 引入了 :ref:`sysbuild`。
* 新增对 :ref:`bin-blobs` 的支持（另见 :ref:`west-blobs`）。
* 新增对 Picolibc 的支持（参见 :kconfig:option:`CONFIG_PICOLIBC`）。
* 所有受支持的板级已从 ``pinmux`` 转换为 :ref:`pinctrl-guide`。
* 新增对 :ref:`i3c_api` 控制器的初步支持。
* 支持 :ref:`W1 api<w1_api>`。
* 改进了从 Kconfig 访问设备树 compatibles（新生成的
  ``DTS_HAS_..._ENABLED`` 配置）。

以下各节按组件提供详细的变更列表。

安全漏洞相关
******************************

本次发布解决了以下 CVE：

更详细的信息可参见：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2022-2993：截至 2022-11-03 处于保密期

* CVE-2022-2741：截至 2022-10-14 处于保密期

API 变更
***********

本次发布中的变更
=======================

* Zephyr 现在要求 Python 3.8 或更高版本

* 更改了 :c:struct:`spi_cs_control` 以移除匿名结构体。
  这可能会导致结构体静态初始化的破坏。
  更新了 :c:macro:`SPI_CS_CONTROL_PTR_DT` 以反映
  此更改。

* :kconfig:option:`CONFIG_LEGACY_INCLUDE_PATH` 选项现在默认
  禁用，所有上游代码和模块已转换为使用
  ``<zephyr/...>`` 头文件路径。该选项仍然可用，以
  方便外部应用的迁移，但将在 3.4
  发布中移除。提供了 :zephyr_file:`scripts/utils/migrate_includes.py` 脚本
  以自动化迁移。

* ``include/zephyr/zephyr.h`` 不再定义 ``__ZEPHYR__``。
  此定义可被第三方代码用于条件编译
  Zephyr 代码。此定义已由 Zephyr 构建系统
  注入。因此，使用 Zephyr 构建系统集成的任何第三方代码
  都不需要更改。外部构建系统需要
  自行注入此定义（如果尚未注入）。

* ``include/zephyr/zephyr.h`` 已弃用，建议改用
  :zephyr_file:`include/zephyr/kernel.h`，因为它仅包含该头文件。
  应用除将 ``#include
  <zephyr/zephyr.h>`` 替换为 ``#include <zephyr/kernel.h>`` 外
  不需要任何更改。

* 蓝牙：启用 :kconfig:option:`CONFIG_BT_EATT` 的应用
  必须设置 GATT 参数结构体中的 :c:member:`chan_opt` 字段。
  要保持旧行为，请使用 :c:enumerator:`BT_ATT_CHAN_OPT_NONE`。

* CAN

  * Zephyr SocketCAN 定义已从 :zephyr_file:`include/zephyr/drivers/can.h`
    移至 :zephyr_file:`include/zephyr/net/socketcan.h`，SocketCAN ``struct can_frame`` 已
    重命名为 :c:struct:`socketcan_frame`，SocketCAN ``struct can_filter`` 已重命名
    为 :c:struct:`socketcan_filter`。SocketCAN 工具函数现在可在
    :zephyr_file:`include/zephyr/net/socketcan_utils.h` 中使用。

  * CAN 控制器 ``struct zcan_frame`` 已重命名为 :c:struct:`can_frame`，``struct
    zcan_filter`` 已重命名为 :c:struct:`can_filter`。

  * :c:enum:`can_state` 枚举已重命名为包含 STATE 一词，以
    使上下文更清晰：

    * ``CAN_ERROR_ACTIVE`` 重命名为 :c:enumerator:`CAN_STATE_ERROR_ACTIVE`。
    * ``CAN_ERROR_WARNING`` 重命名为 :c:enumerator:`CAN_STATE_ERROR_WARNING`。
    * ``CAN_ERROR_PASSIVE`` 重命名为 :c:enumerator:`CAN_STATE_ERROR_PASSIVE`。
    * ``CAN_BUS_OFF`` 重命名为 :c:enumerator:`CAN_STATE_BUS_OFF`。
    * ``CAN_BUS_ON`` 重命名为 :c:enumerator:`CAN_STATE_BUS_ON`。
    * ``CAN_BUS_UNKNOWN`` 重命名为 :c:enumerator:`CAN_STATE_BUS_UNKNOWN`。
    * ``CAN_TX_OK`` 重命名为 :c:enumerator:`CAN_STATE_TX_OK`。
    * ``CAN_TX_ERR`` 重命名为 :c:enumerator:`CAN_STATE_TX_ERR`。
    * ``CAN_TX_ARB_LOST`` 重命名为 :c:enumerator:`CAN_STATE_TX_ARB_LOST`。
    * ``CAN_TX_BUS_OFF`` 重命名为 :c:enumerator:`CAN_STATE_TX_BUS_OFF`。
    * ``CAN_TX_UNKNOWN`` 重命名为 :c:enumerator:`CAN_STATE_TX_UNKNOWN`。
    * ``CAN_TX_EINVAL`` 重命名为 :c:enumerator:`CAN_STATE_TX_EINVAL`。
    * ``CAN_NO_FREE_FILTER`` 重命名为 :c:enumerator:`CAN_STATE_NO_FREE_FILTER`。
    * ``CAN_TIMEOUT`` 重命名为 :c:enumerator:`CAN_STATE_TIMEOUT`。

本次发布中移除的 API
============================

* 移除了以下与已弃用的内核工作队列 API 相关的函数、宏和结构体：

  * ``k_work_pending()``
  * ``k_work_q_start()``
  * ``k_delayed_work``
  * ``k_delayed_work_init()``
  * ``k_delayed_work_submit_to_queue()``
  * ``k_delayed_work_submit()``
  * ``k_delayed_work_pending()``
  * ``k_delayed_work_cancel()``
  * ``k_delayed_work_remaining_get()``
  * ``k_delayed_work_expires_ticks()``
  * ``k_delayed_work_remaining_ticks()``
  * ``K_DELAYED_WORK_DEFINE``

* 移除对 MPU9150 到 AK8975 传感器启用直通模式的支持。

* 移除已弃用的 SPI :c:struct:`spi_cs_control` 字段，
  用于 GPIO 管理，已被 :c:struct:`gpio_dt_spec` 替换。

* 移除通过 Kconfig ``CONFIG_CANFD_MAX_DLC`` 配置 CAN-FD 最大 DLC 值的支持。

* 移除已弃用的 civetweb 模块以及相关的支持代码和示例。

本次发布中弃用
==========================

* :c:macro:`DT_SPI_DEV_CS_GPIOS_LABEL` 和
  :c:macro:`DT_INST_SPI_DEV_CS_GPIOS_LABEL` 已弃用，建议改用
  :c:macro:`DT_SPI_DEV_CS_GPIOS_CTLR` 及其变体。

* :c:macro:`DT_GPIO_LABEL`、:c:macro:`DT_INST_GPIO_LABEL`、
  :c:macro:`DT_GPIO_LABEL_BY_IDX` 和 :c:macro:`DT_INST_GPIO_LABEL_BY_IDX`，
  已弃用，建议改用 :c:macro:`DT_GPIO_CTLR` 及其变体。

* :c:macro:`DT_LABEL` 和 :c:macro:`DT_INST_LABEL` 已弃用
  建议改用 :c:macro:`DT_PROP` 及其变体。

* :c:macro:`DT_BUS_LABEL` 和 :c:macro:`DT_INST_BUS_LABEL` 已弃用
  建议改用 :c:macro:`DT_BUS` 及其变体。

* STM32 LPTIM 域时钟现在应使用设备树配置。
  相关的 Kconfig :kconfig:option:`CONFIG_STM32_LPTIM_CLOCK` 选项现在
  已弃用。

* 设备树中的 ``label`` 属性作为基本属性已弃用。
  该属性对特定绑定仍然有效，例如 :dtcompatible:`gpio-leds` 和
  :dtcompatible:`fixed-partitions`。

* 以 ``bt_mesh_cfg_`` 为前缀的蓝牙 mesh 配置客户端 API
  已弃用，建议改用新前缀 ``bt_mesh_cfg_cli_`` 的 API。

* Pinmux API 现在已正式弃用，建议改用引脚控制 API。
  其移除计划在 3.4 发布中进行。
  有关引脚控制的更多详细信息，请参见 :ref:`pinctrl-guide`。

* Flash Map API 宏 :c:macro:`FLASH_MAP_` 已弃用，
  它们使用 DTS 节点 label 属性来引用分区，
  已被使用 DTS 节点标签的 :c:macro:`FIXED_PARTITION_` 替换。
  替换列表：

  .. table::
     :align: center

     +-----------------------------------+------------------------------------+
     | 已弃用，接受 label 属性  | 替换项，接受 DTS 节点标签  |
     +===================================+====================================+
     | :c:macro:`FLASH_AREA_ID`          | :c:macro:`FIXED_PARTITION_ID`      |
     +-----------------------------------+------------------------------------+
     | :c:macro:`FLASH_AREA_OFFSET`      | :c:macro:`FIXED_PARTITION_OFFSET`  |
     +-----------------------------------+------------------------------------+
     | :c:macro:`FLASH_AREA_SIZE`        | :c:macro:`FIXED_PARTITION_SIZE`    |
     +-----------------------------------+------------------------------------+
     | :c:macro:`FLASH_AREA_LABEL_EXISTS`| :c:macro:`FIXED_PARTITION_EXISTS`  |
     +-----------------------------------+------------------------------------+
     | :c:macro:`FLASH_AREA_DEVICE`      | :c:macro:`FIXED_PARTITION_DEVICE`  |
     +-----------------------------------+------------------------------------+

  :c:macro:`FLASH_AREA_LABEL_STR` 已弃用，无替换项，
  因为其唯一目的是获取 DTS 节点属性 label。

本次发布中的稳定 API 变更
==================================

* CAN

  * 新增 :c:func:`can_start` 和 :c:func:`can_stop` API 函数，用于启动和停止 CAN
    控制器。应用需要调用 :c:func:`can_start` 将 CAN 控制器
    从 :c:enumerator:`CAN_STATE_STOPPED` 状态中恢复，
    然后才能传输和接收 CAN 帧。
  * 新增 :c:func:`can_get_capabilities`，用于获取 CAN 控制器
    支持的能力位掩码。
  * 新增 :c:enumerator:`CAN_MODE_ONE_SHOT`，用于启用 CAN 控制器单次传输模式。
  * 新增 :c:enumerator:`CAN_MODE_3_SAMPLES`，用于启用 CAN 控制器三重采样接收
    模式。

* I3C

  * 新增一组用于 I3C 控制器的新 API。

* W1

  * 引入 :ref:`W1 api<w1_api>`，用于与 1-Wire 主设备交互。

本次发布中的新 API
========================

* 内存管理驱动

  * 新增 :c:func:`sys_mm_drv_update_page_flags` 和
    :c:func:`sys_mm_drv_update_region_flags`，用于更新与
    内存页和区域相关的标志。

内核
******

* 使用多个 :c:macro:`SYS_INIT` 宏的源文件
  如果具有相同的初始化函数，现在必须使用 :c:macro:`SYS_INIT_NAMED`
  并为每个实例使用唯一的名称。

架构
*************

* ARC

  * 为所有 UP ARC 目标新增对非多线程模式的支持。
  * 新增对 :kconfig:option:`CONFIG_ISR_STACK_SIZE`
    和 :kconfig:option:`CONFIG_ARC_EXCEPTION_STACK_SIZE` 值的额外编译时检查。
  * 为 ARC MWDT 工具链变体新增生成符号文件的支持。
  * 新增 ARC MWDT 工具链版本检查。
  * 新增对 SoC 级别上 ARC 目标的 GCC mcpu 选项调优的支持。
  * 将 ARCv3 64 位目标切换到使用新的链接器输出格式值。
  * 为 ARCv3 64 位目标新增累加器寄存器保存/恢复，
    为 ARCv3 32 位目标清理它。
  * 修复 ASM ARC 中断处理代码中的 SMP 竞态条件。

* ARM

  * 改进了 Cortex-M 上的 HardFault 处理。
  * 启用 IRQ 向量表的自动放置。
  * 为 Cortex-M 启用 S2RAM，挂钩提供的 API 函数。
  * 新增 icache 和 dcache 维护函数，并切换到新的
    Kconfig 符号（:kconfig:option:`CONFIG_CPU_HAS_DCACHE` 和
    :kconfig:option:`CONFIG_CPU_HAS_ICACHE`）。
  * 在写入 ``SCTLR`` 以禁用 MPU 后新增数据/指令同步屏障。
  * 在 Cortex-R52 上使用 ``spsr_cxsf`` 而不是不可预测的 ``spsr_hyp``。
  * 移除 GCC 12 的 ``-Wstringop-overread`` 警告。
  * 修复系统关闭失败的处理。
  * 修复错误系统调用下不正确的 ``ssf`` 问题。
  * 修复 mmu 的区域检查问题。

* ARM64

  * :c:func:`arch_mem_map` 现在支持 :c:enumerator:`K_MEM_PERM_USER`。
  * 新增 :kconfig:option:`CONFIG_WAIT_AT_RESET_VECTOR`，在复位向量处自旋
    以允许调试器附加。
  * 实现勘误 822227 "使用不支持的 16K 翻译粒度
    可能导致 Cortex-A57 错误触发域故障"。
  * 为某些平台启用单线程支持。
  * 当设置 :kconfig:option:`CONFIG_INIT_STACKS` 时，
    IRQ 栈现在会被初始化。
  * 修复从用户空间使用缓存 API 的问题。
  * 修复 IPI 传递方式的问题。
  * TF-A（TrustedFirmware-A）现在作为模块发布。

* RISC-V

  * 引入对 RV32E 的支持。
  * 减少 RV32E 的被调用方保存寄存器。
  * 将 Zicsr、Zifencei 和 BitManip 引入为独立的扩展。
  * 为需要每个 ``mret`` 都由 ``ecall`` 平衡的平台
    引入 :kconfig:option:`CONFIG_RISCV_ALWAYS_SWITCH_THROUGH_ECALL`。
  * IRQ 向量表现在用于向量模式。
  * 为 CLIC 禁用 :kconfig:option:`CONFIG_IRQ_VECTOR_TABLE_JUMP_BY_CODE`。
  * ``STRINGIFY`` 宏现在用于 CSR 辅助函数。
  * :kconfig:option:`CONFIG_CODE_DATA_RELOCATION` 现在受支持。
  * PLIC 和 CLIC 现在已解耦。
  * ``jedec,spi-nor`` 不再需要由 RISC-V 架构
    链接脚本设置为 ``okay``。
  * 移除 ``SOC_ERET`` 的使用。
  * 移除 ``ulong_t`` 的使用。
  * 新增基于 TLS 的 :c:func:`arch_is_user_context` 实现。
  * 修复启用 SMP 的构建中的 PMP。
  * 修复每线程 m-mode/u-mode 入口数组。
  * :c:func:`semihost_exec` 函数现在对齐到 16 字节边界。

* Xtensa

  * 宏 ``RSR`` 和 ``WSR`` 已重命名为 :c:macro:`XTENSA_RSR`
    和 :c:macro:`XTENSA_WSR`，以提供适当的命名空间。
  * 修复计时函数中从周期
    转换为纳秒时的舍入错误。
  * 修复平均 "周期到纳秒" 的计算，以实际
    返回纳秒而不是周期。

板级与 SoC 支持
********************

* 新增对这些 SoC 系列的支持：

  * GigaDevice GD32VF103、GD32F3X0、GD32F403 和 GD32F450。
  * Raspberry Pi RP2040
  * NXP i.MXRT595、i.MX8MQ、i.MX8MP

* 移除对这些 SoC 系列的支持：


* 在其他 SoC 系列中进行了以下更改：

  * stm32h7：新增 SMPS 支持
  * stm32u5：启用 TF-M

* ARC 板级的更改：


* 新增对这些 ARM 板级的支持：

  * GigaDevice GD32F350R-EVAL
  * GigaDevice GD32F403Z-EVAL
  * GigaDevice GD32F450I-EVAL
  * OLIMEX-STM32-H405
  * NXP MIMXRT595-EVK
  * NXP MIMX8MQ-EVK
  * NXP MIMX8MP-EVK
  * Raspberry Pi Pico
  * ST Nucleo G031K8
  * ST Nucleo H7A3ZI Q
  * ST STM32G081B Evaluation

* 新增对这些 ARM64 板级的支持：

  * Intel SoC FPGA Agilex 开发套件

* 移除对这些 ARM 板级的支持：


* 移除对这些 X86 板级的支持：

* 新增对这些 RISC-V 板级的支持：

  * GigaDevice GD32VF103V-EVAL
  * Sipeed Longan Nano 和 Nano Lite

* 在其他板级中进行了以下更改：

  * sam_e70_xplained：新增对 CAN-FD 驱动的支持
  * mimxrt11xx：新增 SoC 级电源管理
  * mimxrt11xx：新增对 GPT 定时器作为 OS 定时器的支持


* 新增对以下扩展板的支持：


驱动与传感器
*******************

* ADC

  * 新增对 stm32u5 系列的支持
  * stm32：新增共享 IRQ 支持

* CAN

  * 将 ``zephyr,can-primary`` chosen 属性重命名为 ``zephyr,canbus``。
  * 新增 :c:macro:`CAN_STATE_ERROR_WARNING` CAN 控制器状态。
  * 新增 Atmel SAM Bosch M_CAN CAN-FD 驱动。
  * 新增 NXP LPCXpresso Bosch M_CAN CAN-FD 驱动。
  * 新增 ST STM32H7 Bosch M_CAN CAN-FD 驱动。
  * 重新设计 NXP FlexCAN 驱动中的传输错误处理，以在仲裁丢失或
    确认缺失时自动重试传输，并在 :c:func:`can_send` 中
    在 :c:macro:`CAN_STATE_BUS_OFF` 时尽早失败。
  * 为 ST STM32 bxCAN 驱动新增对禁用自动重传（"one-shot" 模式）的支持。
  * 将仿真的 CAN 环回驱动转换为通过
    设备树而不是 Kconfig 进行配置。

* 计数器

  * stm32：新增基于定时器的计数器驱动（目前仅支持 stm32f4）。

* DAC

  * 新增对 GigaDevice GD32 SoC 的支持
  * 新增对 stm32u5 系列的支持

* 磁盘

  * stm32 sdmmc：从轮询转换为 IT 驱动模式，并新增硬件
    流控选项

* DMA

  * 新增对挂起和恢复传输的支持
  * 新增对应用和嵌入式处理器之间具有 DMA 的 SoC 的支持，
    允许识别传输方向。
  * mimxrt11xx：新增对 DMA 的支持

* EEPROM

  * 新增对 TMP116 数字温度传感器中存在的 EEPROM 的支持。

* 熵

  * 新增对 stm32u5 系列的支持

* 以太网

  * 新增对 Synopsys DesignWare MAC 驱动的支持，
    在 stm32h7 系列上实现。
  * stm32（基于 hal）：新增混杂模式支持
  * stm32（基于 hal）：新增 PTP L2 时间戳支持
  * mimxrt11xx：新增对 10/100M ENET 的支持

* 闪存

  * stm32g0：新增双 bank 支持
  * stm32_qspi：通用增强（为 SPI-NOR 存储器生成复位脉冲、
    使用 4IO 进行读/写（4READ/4PP）、支持不同的 QSPI bank、
    支持 spi-nor 上的 4B 寻址）

  * ite_i8xxx2：驱动已重新设计，写/擦除保护
    管理已移至 flash_write()
    和 flash_erase() 调用的实现。驱动保留了写保护 API，
    该 API 自 2.6 发布以来已设计为移除。


* GPIO

  * 为 GigaDevice GD32 SoC 新增驱动

* I2C

  * 为 GigaDevice GD32 SoC 新增驱动
  * 为所有驱动新增统计功能
  * 为 Renesas R-Car 平台新增 I2C 驱动
  * 新增对 TCA9548A I2C 开关的支持

* I2S

  * mimxrt10xx：新增对 I2S 的支持
  * mimxrt11xx：新增对 I2S 的支持

* 中断控制器

  * 为 GigaDevice RISC-V GD32 SoC 新增 ECLIC 驱动
  * 为 GigaDevice GD32 SoC 新增 EXTI 驱动

* MBOX

  * 新增 MBOX NRFX IPC 驱动

* MEMC

  *  新增对 stm32f7 系列的支持

* 引脚控制

  * 引入新的基于状态的引脚控制（``pinctrl``）API，受
    Linux 设计原则启发。``pinctrl`` API 将替换现有的
    pinmux API，因此建议所有使用 pinmux 的平台进行迁移。
    有关设计原则和实现指南的详细指南可在
    :ref:`pinctrl-guide` 中找到。
  * 已支持 ``pinctrl`` API 的平台：

    * GigaDevice GD32
    * Nordic（初步支持）
    * Renesas R-Car
    * STM32

* PWM

  * stm32：DT 绑定：`st,prescaler` 属性已从 pwm
    移至父定时器节点。
  * stm32：实现了 PWM 捕获 API
  * 为 GigaDevice GD32 SoC 新增驱动。仅支持 PWM 输出。
  * mimxrt1021：新增对 PWM 的支持

* 传感器

  * 新增 Invensense MPU9250 9 轴 IMU 驱动。
  * 新增 ITE IT8XX2 测速仪驱动。
  * 新增 STM L5 die 温度驱动。
  * 新增 STM I3G4250D 陀螺仪驱动。
  * 新增 TI TMP108 驱动。
  * 新增 Winsen MH-Z19B CO2 驱动。
  * 在 sbs_gauge 和 LM75 驱动中将设备配置访问常量化。
  * 从各种驱动中移除 DEV_DATA/DEV_CFG 的使用。
  * 在各种 STM
    驱动中将 ODR 和 range 属性从 Kconfig 移至设备树。
  * 重构 INA230 驱动以新增对 INA237 变体的支持。
  * 重构各种驱动以使用 I2C/SPI/GPIO DT API。
  * 在 LIS2DH 驱动中启用电平触发中断。
  * 修复 TMP112 驱动以避免 I2C 突发写可移植性问题。
  * 修复 LSM6DS0 驱动中的 SENSOR_DEG2RAD_DOUBLE 宏。
  * 修复 LSM303DLHC 磁力计驱动中的增益系数。

* 串行

  * stm32：实现了半双工选项。
  * 为 GigaDevice GD32 SoC 新增驱动。支持轮询和中断驱动模式。

* SPI

  * stm32：实现了帧格式选项（TI 与 Motorola）。
  * mimxrt11xx：新增对 Flexspi 的支持

* 定时器

  * stm32 lptim：新增对 stm32h7 的支持

* USB

  * 新增对 stm32u5 系列的支持（OTG 全速）

* 看门狗

  * 新增对 stm32u5 系列的支持（独立和窗口）
  * mimxrt1170：新增对 CM7 上看门狗的支持


网络
**********

* CoAP：

  * 重构 ``coap_client``/``coap_server`` 示例以更好地使用
    observe API。
  * 新增 PATCH、iPATCH 和 FETCH 方法。
  * 对块传输处理的一些修复。

* DNS：

  * 使 mdns 和 llmnr 响应器加入其多播组。
  * 新增对 mdns/dns_sd 服务类型枚举的支持。

* ICMPv6：

  * 新增对路由信息选项处理的支持。

* IPv4：

  *  为多播监视新增 IPv4 支持。

* LwM2M：

  * 为 :c:func:`lwm2m_rd_client_stop` 函数新增一个参数以强制关闭 LwM2M 会话。
  * 用 double 替换自定义 ``float32_value_t`` 类型。
  * 新增 :kconfig:option:`LWM2M_FIRMWARE_PORT_NONSECURE`/
    :kconfig:option:`LWM2M_FIRMWARE_PORT_SECURE` 选项，允许
    指定自定义端口或固件更新。
  * 新增 :c:func:`lwm2m_update_device_service_period` API 函数。
  * 为 observe 和通知事件新增 observe 回调。
  * 新增对多个 LwM2M 固件更新对象实例的支持。
  * 改进了 LwM2M 内容写入器中的错误处理。
  * 为 LwM2M 内容写入器新增单元测试。
  * 在版本 1.1 中实现了 LwM2M Security、Server、Connection Monitor 对象。
  * LwM2M 协议栈中的多个小 bug 修复。
  * 新增对以下对象的支持：

    * LWM2M Software Management（ID 9）
    * LwM2M Gateway（ID 25）
    * IPSO Current（ID 3317）
    * uCIFI Battery（ID 3411）
    * IPSO Filling level（ID 3435）

* 其他：

  * gptp：时钟同步比率为 double 而非 float
  * 新增对路由生命周期和优先级的支持。
  * 重构网络协议栈中的各种 packed 结构体，以避免
    gcc 的非对齐访问警告。
  * 为环回接口新增自动环回地址注册。
  * 修复 ARP 的源地址选择。
  * 允许在现有驱动之上实现自定义 IEEE802154 L2。
  * 引入了网络包过滤框架。

* MQTT：

  * 修复了不完整的 :c:func:`zsock_sendmsg` 写入处理。
  * 修复了 SOCKS5 传输中 :c:func:`zsock_setsockopt` 的错误处理。

* OpenThread：

  * 将 OpenThread 版本更新到提交 ``ce77ab3c1d7ad91b284615112ae38c08527bf73e``。
  * 修复了 Zephyr 闹钟实现中的溢出 bug。
  * 新增基于 PSA API 的加密后端。
  * 允许将 OpenThread 设置存储在 RAM 中。

* 套接字：

  * 修复了负载大小超过网络 MTU 时的 :c:func:`zsock_sendmsg`。
  * 新增套接字处理优先级。
  * 修复了 DNS 回调延迟时 :c:func:`zsock_getaddrinfo` 中可能的崩溃。

* Telnet：

  * 修复了单个包中多个命令的处理。
  * 默认启用命令处理。

* TCP：

  * 新增向对端发送我们的 MSS 的支持。
  * 修复了向本地地址发送数据包的问题。
  * 修复了连接关闭从双方发起时 TCP 和套接字层之间可能的死锁。
  * TCP 实现中的其他多个小 bug 修复和改进。

* TLS：

  * 新增对 ``TLS_CERT_NOCOPY`` 套接字选项的支持，允许
    优化 mbed TLS 堆使用。
  * 修复了底层 TCP 连接关闭时的 ``POLLHUP`` 检测。
  * 修复了握手错误时的 mbedtls 会话复位。

内核
******

* 使用多个 :c:macro:`SYS_INIT` 宏的源文件
  如果具有相同的初始化函数，现在必须使用 :c:macro:`SYS_INIT_NAMED`
  并为每个实例使用唯一的名称。

架构
*************

* ARC

  * 为所有 UP ARC 目标新增对非多线程模式的支持。
  * 新增对 :kconfig:option:`CONFIG_ISR_STACK_SIZE`
    和 :kconfig:option:`CONFIG_ARC_EXCEPTION_STACK_SIZE` 值的额外编译时检查。
  * 为 ARC MWDT 工具链变体新增生成符号文件的支持。
  * 新增 ARC MWDT 工具链版本检查。
  * 新增对 SoC 级别上 ARC 目标的 GCC mcpu 选项调优的支持。
  * 将 ARCv3 64 位目标切换到使用新的链接器输出格式值。
  * 为 ARCv3 64 位目标新增累加器寄存器保存/恢复，
    为 ARCv3 32 位目标清理它。
  * 修复 ASM ARC 中断处理代码中的 SMP 竞态条件。

* ARM

  * 改进了 Cortex-M 上的 HardFault 处理。
  * 启用 IRQ 向量表的自动放置。
  * 为 Cortex-M 启用 S2RAM，挂钩提供的 API 函数。
  * 新增 icache 和 dcache 维护函数，并切换到新的
    Kconfig 符号（:kconfig:option:`CONFIG_CPU_HAS_DCACHE` 和
    :kconfig:option:`CONFIG_CPU_HAS_ICACHE`）。
  * 在写入 ``SCTLR`` 以禁用 MPU 后新增数据/指令同步屏障。
  * 在 Cortex-R52 上使用 ``spsr_cxsf`` 而不是不可预测的 ``spsr_hyp``。
  * 移除 GCC 12 的 ``-Wstringop-overread`` 警告。
  * 修复系统关闭失败的处理。
  * 修复错误系统调用下不正确的 ``ssf`` 问题。
  * 修复 mmu 的区域检查问题。

* ARM64

  * :c:func:`arch_mem_map` 现在支持 :c:enumerator:`K_MEM_PERM_USER`。
  * 新增 :kconfig:option:`CONFIG_WAIT_AT_RESET_VECTOR`，在复位向量处自旋
    以允许调试器附加。
  * 实现勘误 822227 "使用不支持的 16K 翻译粒度
    可能导致 Cortex-A57 错误触发域故障"。
  * 为某些平台启用单线程支持。
  * 当设置 :kconfig:option:`CONFIG_INIT_STACKS` 时，
    IRQ 栈现在会被初始化。
  * 修复从用户空间使用缓存 API 的问题。
  * 修复 IPI 传递方式的问题。
  * TF-A（TrustedFirmware-A）现在作为模块发布。

* RISC-V

  * 引入对 RV32E 的支持。
  * 减少 RV32E 的被调用方保存寄存器。
  * 将 Zicsr、Zifencei 和 BitManip 引入为独立的扩展。
  * 为需要每个 ``mret`` 都由 ``ecall`` 平衡的平台
    引入 :kconfig:option:`CONFIG_RISCV_ALWAYS_SWITCH_THROUGH_ECALL`。
  * IRQ 向量表现在用于向量模式。
  * 为 CLIC 禁用 :kconfig:option:`CONFIG_IRQ_VECTOR_TABLE_JUMP_BY_CODE`。
  * ``STRINGIFY`` 宏现在用于 CSR 辅助函数。
  * :kconfig:option:`CONFIG_CODE_DATA_RELOCATION` 现在受支持。
  * PLIC 和 CLIC 现在已解耦。
  * ``jedec,spi-nor`` 不再需要由 RISC-V 架构
    链接脚本设置为 ``okay``。
  * 移除 ``SOC_ERET`` 的使用。
  * 移除 ``ulong_t`` 的使用。
  * 新增基于 TLS 的 :c:func:`arch_is_user_context` 实现。
  * 修复启用 SMP 的构建中的 PMP。
  * 修复每线程 m-mode/u-mode 入口数组。
  * :c:func:`semihost_exec` 函数现在对齐到 16 字节边界。

* Xtensa

  * 宏 ``RSR`` 和 ``WSR`` 已重命名为 :c:macro:`XTENSA_RSR`
    和 :c:macro:`XTENSA_WSR`，以提供适当的命名空间。
  * 修复计时函数中从周期
    转换为纳秒时的舍入错误。
  * 修复平均 "周期到纳秒" 的计算，以实际
    返回纳秒而不是周期。

蓝牙
*********

* 音频

  * 在需要时实现中心安全建立。
  * 为连接调用新增额外的安全级别选项。
  * 如果可用，将单播客户端和服务器切换到双向 CIS。
  * 为 CSIS 新增新的 RSI 广播回调。
  * 新增多个上下文处理改进，包括获取上下文的公共函数。
  * 为 CSIS 客户端新增有序访问过程，以及按排名存储活动成员。
  * 新增对 HAS 中写入预设名称的支持。
  * 新增对使用 PACS 作为广播接收端角色的支持。
  * 清理 MICP 实现，包括重命名多个结构体和函数。
  * 实现 CAP 接受方角色。
  * 新增对 ASCS 元数据验证的支持。
  * 开始向应用公开广播接收端广播数据。
  * 新增对单播服务器启动、重新配置、释放、禁用和元数据的支持。
  * 新增对多 CIS 的支持。
  * 实现 HAS 客户端对预设切换的支持。
  * 新增为音频流设置供应商特定非 HCI 数据路径的支持。

* 方向查找

  * 新增对可选择将 IQ 样本转换为 8 位的支持。
  * 新增对 ``int16_t`` 格式 VS IQ 样本报告的支持。

* 主机

  * 新增对 LE 安全连接权限检查的支持。
  * 新增对无 EATT 的多个变长读取过程的支持。
  * 在结构体
    :c:struct:`bt_le_ext_adv_cb` 中新增新回调 :c:func:`rpa_expired`，
    以在启用 :kconfig:option:`CONFIG_BT_PRIVACY` 时
    将广播负载更新与可解析私有地址（RPA）轮换同步。
  * 新增新的 :c:func:`bt_le_set_rpa_timeout()` API 调用，
    以在启用 :kconfig:option:`CONFIG_BT_RPA_TIMEOUT_DYNAMIC` 时
    动态更改可解析私有地址（RPA）超时。
  * 新增 :c:func:`bt_conn_auth_cb_overlay`，
    用于叠加蓝牙 LE 连接的认证回调。
  * 移除 ``CONFIG_BT_HCI_ECC_STACK_SIZE``。
    新的蓝牙长工作队列
    （:kconfig:option:`CONFIG_BT_LONG_WQ`）用于处理 ECC 命令，
    而不是之前的专用线程。
  * :c:func:`bt_conn_get_security` 和 :c:func:`bt_conn_enc_key_size` 现在接受
    ``const struct bt_conn*`` 参数。
  * GATT 多个通知的处理已重写，现在
    仅作为低级 API 使用。
  * 新增作为客户端支持任意位置的 GATT CCC 的支持。
  * 用安全信息扩展 :c:struct:`bt_conn_info` 结构体。
  * 新增新的 :kconfig:option:`CONFIG_BT_PRIVACY_RANDOMIZE_IR`，
    防止主机使用控制器提供的身份根。
  * 新增对通过 EATT 的 GATT 的支持。
  * 实现即时警报客户端。

* Mesh

  * 新增对可选择 RPL 后端的支持。
  * 更改分段消息的发送方式，避免批量传输。
  * 新增异步配置客户端 API。
  * 为健康客户端新增模型发布支持。
  * 将中继消息移至单独的缓冲区池。
  * 减少发送分段确认消息的延迟。
    将 :kconfig:option:`CONFIG_BT_MESH_SEG_ACK_PER_SEGMENT_TIMEOUT` 设置为 100
    可获得之前的时序。
  * 重构 shell 命令。

* 控制器

  * 将新的 LLCP 实现设为默认实现。
    启用 :kconfig:option:`CONFIG_BT_LL_SW_LLCP_LEGACY`
    可返回到遗留实现。
    :kconfig:option:`CONFIG_BT_LL_SW_LLCP_LEGACY` 已标记
    为弃用，建议改用新的 :kconfig:option:`CONFIG_BT_LL_SW_LLCP`，
    该选项现在是默认选项。
  * 将扩展广播标记为稳定，不再是实验性的。
  * 新增 deinit() 基础设施，以正确支持禁用
    蓝牙支持，包括控制器。
  * 实现外围 CIS 创建过程。
  * 实现 CIS 终止过程。
  * 新增对周期性广播 ADI 的支持。
  * 实现扩展扫描响应数据分片操作的支持。
  * 为 AD 数据启用背靠背 PDU 链接。
  * 新增新的 :kconfig:option:`CONFIG_BT_CTLR_SYNC_PERIODIC_SKIP_ON_SCAN_AUX`，
    以允许跳过周期性同步事件。
  * 新增新的 :kconfig:option:`CONFIG_BT_CTLR_SCAN_AUX_SYNC_RESERVE_MIN`，
    用于最小时间预留。
  * 实现 ISO 测试模式 HCI 命令。
  * 新增在 BIG 内选择多个 BIS 同步的支持。
  * 实现当 BIG 事件终止时刷新待处理的 ISO TX PDU。
  * 新增新的 :kconfig:option:`CONFIG_BT_CTLR_ADV_DATA_CHAIN`，
    以启用实验性的广播数据链接支持。

* HCI 驱动

  * 新增 Telink B91 HCI 驱动。

板级与 SoC 支持
********************

* 新增对这些 SoC 系列的支持：

  * Atmel SAML21、SAMR34、SAMR35
  * GigaDevice GD32E50X
  * GigaDevice GD32F470
  * NXP i.MX8MN、LPC55S36、LPC51U68
  * renesas_smartbond da1469x SoC 系列

* 在其他 SoC 系列中进行了以下更改：

  * gigadevice：启用 SEGGER RTT
  * Raspberry Pi Pico：新增 ADC 支持
  * Raspberry Pi Pico：新增 PWM 支持
  * Raspberry Pi Pico：新增 SPI 支持
  * Raspberry Pi Pico：新增看门狗支持

* ARC 板级的更改：

  * 新增对 qemu_arc_hs5x 板级的支持（ARCv3、32 位、UP、HS5x）
  * 简化 SMP nSIM ARC 平台的多 runner 设置
  * 修复基于 mdb 的 west runner（mdb-nsim 和 mdb-hw）的 mdb 执行文件夹

* 新增对这些 ARM 板级的支持：

  * Arduino MKR Zero
  * Atmel atsaml21_xpro
  * Atmel atsamr34_xpro
  * Blues Wireless Swan
  * Digilent Zybo
  * EBYTE E73-TBB
  * GigaDevice GD32E507V-START
  * GigaDevice GD32E507Z-EVAL
  * GigaDevice GD32F407V-START
  * GigaDevice GD32F450V-START
  * GigaDevice GD32F450Z-EVAL
  * GigaDevice GD32F470I-EVAL
  * NXP lpcxpresso51u68、RT1060 EVKB
  * NXP lpcxpresso55s36
  * Olimex LoRa STM32WL DevKit
  * PAN1770 评估板
  * PAN1780 评估板
  * PAN1781 评估板
  * PAN1782 评估板
  * ST STM32F7508-DK Discovery Kit
  * TDK RoboKit 1
  * WeAct Studio Black Pill V1.2
  * WeAct Studio Black Pill V3.0
  * XIAO BLE
  * da1469x_dk_pro

* 新增对这些 ARM64 板级的支持：

  * i.MX8M Nano LPDDR4 EVK 板级系列

* 新增对这些 RISC-V 板级的支持：

  * ICE-V Wireless
  * RISCV32E 仿真（QEMU）

* 新增对这些 Xtensa 板级的支持：

  * ESP32-NET
  * intel_adsp_ace15_mtpm

* 移除对这些 Xtensa 板级的支持：

  * Intel S1000

* 在其他板级中进行了以下更改：

  * sam_e70_xplained：使用 EEPROM 设备树绑定来配置以太网 MAC
  * sam_v71_xult：使用 EEPROM 设备树绑定来配置以太网 MAC
  * rpi_pico：为 Picoprobe、Jlink 和 Blackmagicprobe 新增 west runner 配置

* 新增对以下扩展板的支持：

  * ARCELI W5500 ETH
  * MAX7219 LED 显示驱动扩展板
  * Panasonic Grid-EYE（AMG88xx）

USB
***

  * CDC ACM、DFU 和 MSC 类实现中的小 bug 修复和改进。
    除此之外没有其他重大更改。

设备树
**********

* 设备树 *label 属性* 的使用已弃用，
  该属性在树中的几乎所有绑定中已变为可选。

  在之前版本的 zephyr 中，
  设备树文件中通常会出现这样的 label 属性：

  .. code-block:: dts

     foo {
             label = "FOO";
             /* ... */
     };

  然后可以使用类似以下的内容来获取设备
  结构体，用于 :ref:`device_model_api`：

  .. code-block:: c

     const struct device *my_dev = device_get_binding("FOO");
     if (my_dev == NULL) {
             /* 要么设备初始化失败，要么没有这样的设备 */
     } else {
             /* 设备已准备好使用 */
     }

  这种方法存在多个问题。

  首先，它需要对系统中所有设备进行运行时字符串比较
  以查找每个设备，这是低效的，因为设备是
  静态分配的，并且在构建时已知。其次，由于
  配置错误的设备驱动导致的缺失设备无法轻松地区分
  设备初始化失败，因为两者都从
  ``device_get_binding()`` 返回 ``NULL`` 值。这导致了频繁的混淆。第三，
  label 属性和设备树 *节点标签* 之间的
  区分——尽管术语相似，但它们是
  不同的——是用户混淆的频繁来源，
  特别是由于两者都可以用于获取设备
  结构体。

  现在应通常使用节点标签
  来获取设备，而不是使用 label 属性。节点标签
  类似于以下设备树中的 ``lbl`` 标记：

  .. code-block:: dts

     lbl: foo {
             /* ... */
     };

  可以像这样获取设备结构体指针：

  .. code-block:: c

     /* 如果下一行导致构建错误，那么
      * 没有这样的设备。要么 fi

构建与基础设施
************************

* 构建系统

  * 新的 CMake 扩展函数：

    * ``dt_alias()``
    * ``target_sources_if_dt_node()``

  * 以下 CMake 扩展函数现在处理设备树别名：

    * ``dt_node_exists()``
    * ``dt_node_has_status()``
    * ``dt_prop()``
    * ``dt_num_regs()``
    * ``dt_reg_addr()``
    * ``dt_reg_size()``

* 设备树

  * 已移除对设备树 compatible ``ti,ina23x`` 的支持。
    请改用 :dtcompatible:`ti,ina230` 或 :dtcompatible:`ti,ina237`。

* West（扩展）

  * 新增对 gd32isp runner 的支持


库 / 子系统
**********************

* 管理

  * 修复了 mcumgr 串行 SMP 协议未将 CRC16 的长度添加到包长度的问题。
  * Kconfig 选项 OS_MGMT_TASKSTAT 现在默认禁用。

* 电源管理

  * 电源管理资源现在由使用
    :c:macro:`PM_DEVICE_DEFINE`、:c:macro:`PM_DEVICE_DT_DEFINE` 或
    :c:macro:`PM_DEVICE_DT_INST_DEFINE` 的设备手动分配。设备实例化宏现在
    接受对已分配资源的引用。可以使用
    :c:macro:`PM_DEVICE_GET`、:c:macro:`PM_DEVICE_DT_GET` 或
    :c:macro:`PM_DEVICE_DT_INST_GET` 获取该引用。由于此更改，不
    实现设备电源管理支持的设备将不使用不必要的
    内存。
  * 设备运行时电源管理 API 错误处理已简化。
  * :c:func:`pm_device_runtime_enable` 如果目标设备尚未
    挂起则挂起它。此更改确保设备状态始终保持在
    一致状态。
  * 改进了 PM 状态设备树宏命名
  * 新增 API 调用 :c:func:`pm_state_cpu_get_all` 以获取
    CPU 电源状态的信息。
  * ``pm/device.h`` 不再由 ``device.h`` 包含，因为设备 API
    不再依赖于 PM API。
  * 新增对电源域的支持。电源域实现为
    简单设备，并使用现有的 PM API 进行恢复和挂起，
    电源域下的设备在其变为活动或挂起时收到通知。
  * 新增操作 :c:enum:`PM_DEVICE_ACTION_TURN_ON`。此操作
    由电源域用于在变为活动时通知设备。
  * 新增 API（:c:func:`pm_device_state_lock`、
    :c:func:`pm_device_state_unlock` 和
    :c:func:`pm_device_state_is_locked`）以锁定设备 pm
    状态。当设备状态被锁定时，内核将不再
    在系统进入睡眠时挂起和恢复设备，
    并且设备运行时电源管理操作将失败。
  * :c:func:`pm_device_state_set` 已弃用，建议改用
    :c:func:`pm_device_action_run`。
  * 适当的多核支持。设备仅在最后一个
    活动 CPU 时挂起。在 Policy 和 SoC 接口中新增了 cpu 参数。

* 跟踪

  * 支持使用 python 系统调用生成器跟踪所有系统调用，
    以引入跟踪钩子调用。

* IPC

  * static_vrings：修复了工作队列（WQ）初始化
  * static_vrings：在访问 atomic_t 变量时引入了原子辅助函数
  * static_vrings：移至每个实例一个 WQ
  * static_vrings：在 DT 中新增 "zephyr,priority" 属性以设置实例的 WQ 优先级
  * static_vrings：新增配置参数以将共享内存初始化为零
  * 扩展 API 以新增 NOCOPY 函数
  * static_vrings：新增对 NOCOPY 操作的支持
  * 引入核间消息传递后端（icmsg），依赖于简单的核间消息传递缓冲区

* 日志

  * 新增支持二进制字典日志的 UART 前端。
  * 新增对 MIPI SyS-T 目录消息的支持。
  * 新增 cAVS HDA 后端。

* Shell

  * 新增用于使用内存段方法从多个文件创建子命令的 API：

    * :c:macro:`SHELL_SUBCMD_SET_CREATE` 用于创建子命令集。
    * :c:macro:`SHELL_SUBCMD_COND_ADD` 和 :c:macro:`SHELL_SUBCMD_ADD` 用于向
      集合添加子命令。

HALs
****

* Atmel

  * 新增设备树绑定、文档和脚本以支持
    基于状态的引脚控制（``pinctrl``）API。
  * 为以下 SoC 导入了新的头文件：

    * SAML21
    * SAMR34
    * SAMR35

* GigaDevice

  * 修复了 GD32_REMAP_MSK 宏
  * 修复了 gd32f403z pc3 缺失的 pincodes

* STM32:

  * 将 stm32f4 更新到新的 STM32cube 版本 V1.27.0
  * 将 stm32f7 更新到新的 STM32cube 版本 V1.16.2
  * 将 stm32g4 更新到新的 STM32cube 版本 V1.5.0
  * 将 stm32h7 更新到新的 STM32cube 版本 V1.10.0
  * 将 stm32l4 更新到新的 STM32cube 版本 V1.17.1
  * 将 stm32u5 更新到新的 STM32cube 版本 V1.1.0
  * 将 stm32wb 更新到新的 STM32cube 版本 V1.13.2（包括 hci 库）

MCUboot
*******

- 新增对写对齐大于 8B 的设备的初步支持。
- 新增带超时的进入串行恢复模式的选项。参见 ``CONFIG_BOOT_SERIAL_WAIT_FOR_DFU``。
- 使用了更小的 sha256 实现。
- 新增对串行恢复中 echo 命令的支持。参见 ``CONFIG_BOOT_MGMT_ECHO``。
- 修复了单加载器模式下页面大小大于 1024 B 的 SoC 闪存的映像解密。
- 修复了串行恢复中可能的输出缓冲区溢出。
- 新增用于验证与 Zephyr 集成的 GitHub 工作流。
- 移除已弃用的 ``DT_CHOSEN_ZEPHYR_FLASH_CONTROLLER_LABEL``。
- 修复了 ``CONFIG_LOG_IMMEDIATE`` 的使用。

Trusted Firmware-M
******************

* 允许在启用 TF-M 时在应用中启用 FPU。
* 新增选项以从构建中排除非安全 TF-M 应用。
* 将 ``mergehex.py`` 移至 ``scripts/build``。
* 新增自定义复位处理程序的选项。

文档
*************

测试与示例
*****************

* 大量测试已重新设计以使用新的 ztest API，
  有关更多详细信息，请参见
  :ref:`test-framework`。新引入的
  测试也应使用它。
* smp_svr 蓝牙 overlay（overlay-bt）已重新设计以
  提高吞吐量并启用包重组。
* 为新的 shell API 函数 :c:func:`shell_ready` 新增测试。
Issue Related Items
*******************

Known Issues
============

- :github:`22049` - Bluetooth: IRK handling issue when using multiple local identities
- :github:`25917` - Bluetooth: Deadlock with TX of ACL data and HCI commands (command blocked by data)
- :github:`30348` - XIP can't be enabled with ARC MWDT toolchain
- :github:`31298` - tests/kernel/gen_isr_table failed on hsdk and nsim_hs_smp sometimes
- :github:`33747` - gptp does not work well on NXP rt series platform
- :github:`34269` - LOG_MODE_MINIMAL BUILD error
- :github:`37193` - mcumgr: Probably incorrect error handling with udp backend
- :github:`37731` - Bluetooth: hci samples: Unable to allocate command buffer
- :github:`38041` - Logging-related tests fails on qemu_arc_hs6x
- :github:`38880` - ARC: ARCv2: qemu_arc_em / qemu_arc_hs don't work with XIP disabled
- :github:`38947` - Issue with SMP commands sent over the UART
- :github:`39598` - use of __noinit with ecc memory hangs system
- :github:`40023` - Build fails for ``native_posix`` board when using C++ <atomic> header
- :github:`41606` - stm32u5: Re-implement VCO input and EPOD configuration
- :github:`41622` - Infinite mutual recursion when SMP and ATOMIC_OPERATIONS_C are set
- :github:`41822` - BLE IPSP sample cannot handle large ICMPv6 Echo Request
- :github:`41823` - Bluetooth: Controller: llcp: Remote request are dropped due to lack of free proc_ctx
- :github:`42030` - can: "bosch,m-can-base": Warning "missing or empty reg/ranges property"
- :github:`43099` - CMake: ARCH roots issue
- :github:`43249` - MBEDTLS_ECP_C not build when MBEDTLS_USE_PSA_CRYPTO
- :github:`43308` - driver: serial: stm32: uart will lost data when use dma mode[async mode]
- :github:`43555` - Variables not properly initialized when using data relocation with SDRAM
- :github:`43562` - Setting and/or documentation of Timer and counter use/requirements for Nordic Bluetooth driver
- :github:`43836` - stm32: g0b1: RTT doesn't work properly after stop mode
- :github:`44339` - Bluetooth:controller: Implement support for Advanced Scheduling in refactored LLCP
- :github:`44377` - ISO Broadcast/Receive sample not working with coded PHY
- :github:`44410` - drivers: modem: shell: ``modem send`` doesn't honor line ending in modem cmd handler
- :github:`44948` - cmsis_dsp: transofrm: error during building cf64.fpu and rf64.fpu for mps2_an521_remote
- :github:`45218` - rddrone_fmuk66: I2C configuration incorrect
- :github:`45241` - (Probably) unnecessary branches in several modules
- :github:`45323` - Bluetooth: controller: llcp: Implement handling of delayed notifications in refactored LLCP
- :github:`45427` - Bluetooth: Controller: LLCP: Data structure for communication between the ISR and the thread
- :github:`45814` - Armclang build fails due to missing source file
- :github:`46073` - IPSP (IPv6 over BLE) example stop working after a short time
- :github:`46121` - Bluetooth: Controller: hci: Wrong periodic advertising report data status
- :github:`46126` - pm_device causes assertion error in sched.c with lis2dh
- :github:`46401` - ARM64: Relax 4K MMU mapping alignment
- :github:`46596` - STM32F74X RMII interface does not work
- :github:`46598` - Logging with RTT backend on STM32WB strange behavier
- :github:`46844` - Timer drivers likely have off-by-one in rapidly-presented timeouts
- :github:`46846` - lib: libc: newlib: strerror_r non-functional
- :github:`46986` - Logging (deferred v2) with a lot of output causes MPU fault
- :github:`47014` - can: iso-tp: implementation test failed with twister on nucleo_g474re
- :github:`47092` - driver: nrf: uarte: new dirver breaks our implementation for uart.
- :github:`47120` - shell uart: busy wait for DTR in ISR
- :github:`47477` - qemu_leon3: tests/kernel/fpu_sharing/generic/ failed when migrating to new ztest API
- :github:`47500` - twister: cmake: Failure of "--build-only -M" combined with "--test-only" for --device-testing
- :github:`47607` - Settings with FCB backend does not pass test on stm32h743
- :github:`47732` - Flash map does not fare well with MCU who do bank swaps
- :github:`47817` - samples/modules/nanopb/sample.modules.nanopb fails with protobuf > 3.19.0
- :github:`47908` - tests/kernel/mem_protect/stack_random works unreliably and sporadically fails
- :github:`47988` - JSON parser not consistent on extra data
- :github:`48018` - ztest: static threads are not re-launched for repeated test suite execution.
- :github:`48037` - Grove LCD Sample Not Working
- :github:`48094` - pre-commit scripts fail when there is a space in zephyr_base
- :github:`48102` - JSON parses uses recursion (breaks rule 17.2)
- :github:`48147` - ztest: before/after functions may run on different threads, which may cause potential issues.
- :github:`48287` - malloc_prepare ASSERT happens when enabling newlib libc with demand paging
- :github:`48299` - SHT3XD_CMD_WRITE_TH_LOW_SET should be SHT3XD_CMD_WRITE_TH_LOW_CLEAR
- :github:`48304` - bt_disable() does not work properly on nRF52
- :github:`48390` - [Intel Cavs] Boot failures on low optimization levels
- :github:`48394` - vsnprintfcb writes to ``*str`` if it is NULL
- :github:`48468` - GSM Mux does not transmit all queued data when uart_fifo_fill is called
- :github:`48473` - Setting CONFIG_GSM_MUX_INITIATOR=n results in a compile error
- :github:`48505` - BLE stack can get stuck in connected state despite connection failure
- :github:`48520` - clang-format: #include reorder due to default: SortIncludesOptions != SI_Never
- :github:`48603` - LoRa driver asynchronous receive callback clears data before the callback.
- :github:`48608` - boards: mps2_an385: Unstable system timer
- :github:`48625` - GSM_PPP api keeps sending commands to muxed AT channel
- :github:`48726` - net: tests/net/ieee802154/l2/net.ieee802154.l2 failed on reel board
- :github:`48841` - Bluetooth: df: Assert in lower link layer when requesting CTE from peer periodically with 7.5ms connection interval
- :github:`48850` - Bluetooth: LLCP: possible access to released control procedure context
- :github:`48857` - samples: Bluetooth: Buffer size mismatch in samples/bluetooth/hci_usb for nRF5340
- :github:`48953` - 'intel,sha' is missing binding and usage
- :github:`48954` - several NXP devicetree bindings are missing
- :github:`48992` - qemu_leon3: tests/posix/common/portability.posix.common fails
- :github:`49021` - uart async api does not provide all received data
- :github:`49032` - espi saf testing disabled
- :github:`49069` - log: cdc_acm: hard fault message does not output
- :github:`49148` - Asynchronous UART API triggers Zephyr assertion on STM32WB55
- :github:`49210` - BL5340 board cannot build bluetooth applications
- :github:`49213` - logging.add.log_user test fails when compiled with GCC 12
- :github:`49266` - Bluetooth: Host doesn't seem to handle INCOMPLETE per adv reports
- :github:`49313` - nRF51822 sometimes hard fault on connect
- :github:`49338` - Antenna switching for Bluetooth direction finding with the nRF5340
- :github:`49373` - BLE scanning - BT RX thread hangs on.
- :github:`49390` - shell_rtt thread can starve other threads of the same priority
- :github:`49484` - CONFIG_BOOTLOADER_SRAM_SIZE should not be defined by default
- :github:`49492` - kernel.poll test fails on qemu_arc_hs6x when compiled with GCC 12
- :github:`49494` - testing.ztest.ztress test fails on qemu_cortex_r5 when compiled with GCC 12
- :github:`49584` - STM32WB55 Failed read remote feature, remote version and LE set PHY
- :github:`49588` - Json parser is incorrect with undefined parameter
- :github:`49611` - ehl_crb: Failed to run timer testcases
- :github:`49614` - acrn_ehl_crb: The testcase tests/kernel/sched/schedule_api failed to run.
- :github:`49656` - acrn_ehl_crb: testcases tests/kernel/smp failed to run on v2.7-branch
- :github:`49746` - twister: extra test results
- :github:`49811` - DHCP cannot obtain IP, when CONFIG_NET_VLAN is enabled
- :github:`49816` - ISOTP receive fails for multiple binds with same CAN ID but different extended ID
- :github:`49889` - ctf trace: unknown event id when parsing samples/tracing result on reel board
- :github:`49917` - http_client_req() sometimes hangs when peer disconnects
- :github:`49963` - Random crash on the L475 due to work->handler set to NULL
- :github:`49996` - tests: drivers: clock_control: nrf_lf_clock_start and nrf_onoff_and_bt fails
- :github:`50028` - flash_stm32_ospi Write enable failed when building with TF-M
- :github:`50084` - drivers: nrf_802154: nrf_802154_trx.c - assertion fault when enabling Segger SystemView tracing
- :github:`50095` - ARC revision Kconfigs wrongly mixed with board name
- :github:`50149` - tests: drivers: flash fails on nucleo_l152re because of wrong erase flash size
- :github:`50196` - LSM6DSO interrupt handler not being called
- :github:`50256` - I2C on SAMC21 sends out stop condition incorrectly
- :github:`50306` - Not able to flash stm32h735g_disco - TARGET: stm32h7x.cpu0 - Not halted
- :github:`50345` - Network traffic occurs before Bluetooth NET L2 (IPSP) link setup complete
- :github:`50354` - ztest_new: _zassert_base : return without post processing
- :github:`50404` - Intel CAVS: tests/subsys/logging/log_immediate failed.
- :github:`50427` - Bluetooth: host: central connection context leak
- :github:`50446` - MCUX CAAM is disabled temporarily
- :github:`50452` - mec172xevb_assy6906: The testcase tests/lib/cmsis_dsp/matrix failed to run.
- :github:`50501` - STM32 SPI does not work properly with async + interrupts
- :github:`50506` - nxp,mcux-usbd devicetree binding issues
- :github:`50515` - Non-existing test cases reported as "Skipped" with reason  “No results captured, testsuite misconfiguration?” in test report
- :github:`50546` - drivers: can: rcar: likely inconsistent behavior when calling can_stop() with pending transmissions
- :github:`50554` - Test uart async failed on Nucleo F429ZI
- :github:`50565` - Fatal error after ``west flash`` for nucleo_l053r8
- :github:`50567` - Passed test cases are reported as "Skipped" because of incomplete test log
- :github:`50570` - samples/drivers/can/counter fails in twister for native_posix
- :github:`50587` - Regression in Link Layer Control Procedure (LLCP)
- :github:`50590` - openocd: Can't flash on various STM32 boards
- :github:`50598` - UDP over IPSP not working on nRF52840
- :github:`50614` - Zephyr if got the ip is "10.xxx.xxx.xxx" when join in the switchboard, then the device may can not visit the outer net, also unable to Ping.
- :github:`50620` - fifo test fails with CONFIG_CMAKE_LINKER_GENERATOR enabled on qemu_cortex_a9
- :github:`50652` - RAM Loading on i.MXRT1160_evk
- :github:`50655` - STM32WB55 Bus Fault when connecting then disconnecting then connecting then disconnecting then connecting
- :github:`50658` - BLE stack notifications blocks host side for too long
- :github:`50709` - tests: arch: arm: arm_thread_swap fails on stm32g0 or stm32l0
- :github:`50732` - net: tests/net/ieee802154/l2/net.ieee802154.l2 failed on reel_board due to build failure
- :github:`50735` - Intel CAVS18: tests/boards/intel_adsp/hda_log/boards.intel_adsp.hda_log.printk failed
- :github:`50746` - Stale kernel memory pool API references
- :github:`50766` - Zephyr build system doesn't setup CMake host environment correctly
- :github:`50776` - CAN Drivers allow sending FD frames without device being set to FD mode
- :github:`50777` - LE Audio: Receiver start ready command shall only be sent by the receiver
- :github:`50778` - LE Audio: Audio shell: Unicast server cannot execute commands for the default_stream
- :github:`50780` - LE Audio: Bidirectional handling of 2 audio streams as the unicast server when streams are configured separately not working as intended
- :github:`50781` - LE Audio: mpl init causes warnings when adding objects
- :github:`50783` - LE Audio: Reject ISO data if the stream is not in the streaming state
- :github:`50789` - west: runners: blackmagicprobe: Doesn't work on windows due to wrong path separator
- :github:`50801` - JSON parser fails on multidimensional arrays
- :github:`50812` - MCUmgr udp sample fails with shell - BUS FAULT
- :github:`50841` - high SRAM usage with picolibc on nRF platforms

Addressed issues
================

* :github:`50861` - Intel ADSP HDA and GPDMA Bugs
* :github:`50843` - tests: kernel: timer: timer_behavior: kernel.timer.timer - SRAM overflow on nrf5340dk_nrf5340_cpunet and nrf52dk_nrf52832
* :github:`50841` - high SRAM usage with picolibc on some userspace platforms
* :github:`50774` - ESP32 GPIO34 IRQ not working
* :github:`50771` - mcan driver has tx and rx error counts swapped
* :github:`50754` - MCUboot 更新 损坏 compilation 用于 板 没有 CONFIG_WATCHDOG=y
* :github:`50737` - tfm_ram_report does not work with sdk-ng 0.15.0
* :github:`50728` - missing SMP fixes for RISC-V
* :github:`50691` - Bluetooth: Host: CONFIG_BT_LOG_SNIFFER_INFO doesn't work as intended without bonding
* :github:`50689` - Suspected unaligned access in Bluetooth controller connection handling
* :github:`50681` - gpio: ite: gpio_ite_configure() neither supporting nor throwing error when gpio is configured with GPIO_DISCONNECTED flag
* :github:`50656` - 错误 定义 的 bank 大小 用于 intel 内存 management 驱动
* :github:`50654` - 一些 文件   ALWAYS 构建 没有 它们  使用
* :github:`50635` - hal: stm32: 有效 pins  移除 在...中  最后一个 版本
* :github:`50631` - Please Add __heapstats() to stdlib.h
* :github:`50621` - The history of the multi API / MFD discussions 2022 July - Sep
* :github:`50619` - tests/kernel/timer/starve 失败 到 运行 在...上 设备
* :github:`50618` - STM32 Ethernet
* :github:`50615` - ESP32 GPIO driver
* :github:`50611` - k_heap_aligned_alloc does not handle a timeout of K_FOREVER correctly
* :github:`50603` - Upgrade to loramac-node 4.7.0 when it is released to fix async LoRa reception on SX1276
* :github:`50579` - arch: arm: Using ISR_DIRECT_PM with zero-latency-interrupt violation
* :github:`50549` - USB: samhs: 设备  不 工作 在...之后 detach-attach 排序
* :github:`50545` - drivers: can: inconsistent behavior when calling can_stop() with pending transmissions
* :github:`50538` - lpcxpresso55s69_cpu0 samples/subsys/usb/dfu/sample.usb.dfu build failure
* :github:`50525` - Passed test cases reported as "Skipped" because test log lost
* :github:`50522` - mgmt: mcumgr: img_mgmt: Failure of erase returns nothing
* :github:`50520` - Bluetooth: bsim eatt_notif test fails with assertion in some environments
* :github:`50502` - iMX 7D GPIO Pinmux Array Has Incorrect Ordering
* :github:`50482` - mcumgr: img_mgmt: zephyr_img_mgmt_flash_area_id has wrong slot3 ID
* :github:`50468` - Incorrect Z_THREAD_STACK_BUFFER in arch_start_cpu for Xtensa
* :github:`50467` - 可能 内存 corruption 在...上 ARC 当...时 userspace  启用
* :github:`50465` - 可能 内存 corruption 在...上 RISCV 当...时 userspace  启用
* :github:`50464` - Boot banner can cut through output of shell prompt
* :github:`50455` - Intel CAVS15/25: tests/subsys/shell/shell failed with no console output
* :github:`50438` - Bluetooth: Conn: Bluetooth stack becomes unusable when communicating with both centrals and peripherals
* :github:`50432` - Bluetooth: Controller: Restarting BLE scanning not always working and sometimes crashes together with periodic. adv.
* :github:`50421` - Sysbuild-configured project using ``west flash --recover`` will wrongly recover (and reset) the MCU each time it flashes an image
* :github:`50414` - smp_dummy.h file is outside of zephyr include folder
* :github:`50394` - RT685 刷写 chip 大小  不正确
* :github:`50386` - Twister "FLASH overflow" does not account for imgtool trailer.
* :github:`50374` - CI failure in v3.1.0-rc2 full run
* :github:`50368` - esp32: counter 驱动 不 工作 带 absolute 值
* :github:`50344` - bl5340_dvk_cpuapp: undefined reference to ``__device_dts_ord_14``
* :github:`50343` - uninitialized 变量 在...中 kernel.workqueue 测试
* :github:`50342` - mcuboot: BOOT_MAX_ALIGN is redefined
* :github:`50341` - undefined reference to ``log_output_flush`` in sample.logger.syst.catalog
* :github:`50331` - net mem shell output indents TX DATA line
* :github:`50330` - 失败 到 查找 GICv3 Redistributor base 地址 用于 Cortex-R52 运行 在...中  聚集 不同 than 0
* :github:`50327` - JLink needs flashloader for MIMXRT1060-EVK
* :github:`50317` - boards/arm/thingy53_nrf5340: lack of mcuboot's gpio aliases
* :github:`50306` - Not able to flash stm32h735g_disco - TARGET: stm32h7x.cpu0 - Not halted
* :github:`50299` - CI fails building stm32u5  tests/subsys/pm/device_runtime_api
* :github:`50297` - mcumgr: fs_mgmt: hash/checksum: Build warnings on native_posix_64
* :github:`50294` - test-ci: timer_behavior: mimxrt1170_evk_cm7/1160: test failure
* :github:`50284` - Generated linker scripts break when ZEPHYR_BASE and ZEPHYR_MODULES share structure that contains symlinks
* :github:`50282` - samples: 驱动  babbling:  controller 不 启动
* :github:`50266` - 驱动  native_posix_linux:  不 接收 frames 在...期间 停止
* :github:`50263` - 驱动  mcan: transceiver  启用 在 驱动 initialization
* :github:`50257` - twister: --coverage 选项  不 工作 用于 qemu_x86_64 和 其他 板
* :github:`50255` - 测试 进程 崩溃 当...时 运行 twister 带 --coverage
* :github:`50244` - GPIO manipulation from a “counter” (ie HW timer) when Bluetooth (BLE) is enabled.
* :github:`50238` - ESP32: rtcio_ll_pullup_disable crash regression
* :github:`50235` - UDP: Memory leak when allocated packet is smaller than requested
* :github:`50232` - gpio_shell: Not functional anymore following DT label cleanup and deprecation
* :github:`50226` - MPU FAULT: Stacking error with lvgl on lv_timer_handler()
* :github:`50224` - tests/kernel/tickless/tickless_concept: Failed on STM32
* :github:`50219` - 内核 测试 失败 在...上 qemu_riscv32_smp
* :github:`50218` - rcar_h3ulcb:  失败 到 运行 RTR 测试 cases
* :github:`50214` - Missing human readable names in names file od deive structure
* :github:`50202` - Configuring ``GPIO25`` crashes ESP32
* :github:`50192` - nrf_qspi_nor 驱动  崩溃 如果 power management  启用
* :github:`50191` - nrf_qspi_nor-driver leaves CS pin to undefined state when pinctrl is enabled
* :github:`50172` - QSPI NAND Flash driver question
* :github:`50165` - boards: riscv: ite: No flash and RAM stats are shown whenever building ITE board
* :github:`50158` - Drivers: gpio: stm32u5 portG not working
* :github:`50152` - SMT32: incorrect internal temperature value
* :github:`50150` - 测试 驱动 刷写 构建 错误 带 b_u585i_iot02a_ns 板
* :github:`50146` - tests: kernel: mem_protect fails on ARMv6-M and ARMv8-M Baseline
* :github:`50142` - NXP i.MX RT1024 CPU GPIO access bug.
* :github:`50140` - ARP handling causes dropped packets when multiple outgoing packets are queued
* :github:`50135` - cannot 引导 上 在...上 custom 板
* :github:`50119` - non-IPI 路径 的 SMP  损坏
* :github:`50118` - Twister: ``--coverage-formats`` Does not work despite ``--coverage`` added
* :github:`50108` - drivers: console: rtt_console: undefined reference to ``__printk_hook_install``
* :github:`50107` - subsys: pm: device_runtime.c: compile error
* :github:`50106` - ram_report stopped working with zephyr-sdk 0.15
* :github:`50099` - 板 pinnacle_100_dvk  启用 QSPI 和 modem 由 默认
* :github:`50096` - 测试 驱动  gpio_basic_api 测试 cannot  构建 successfully 在...上 bl5340_dvk_cpuapp 板
* :github:`50073` - mcumgr: Bluetooth backend does not restart advertising after disconnect
* :github:`50070` - LoRa: Support on RFM95 LoRa module combined with a nRF52 board
* :github:`50066` - 测试 tests/drivers/can/shell 失败 在...中 daily 测试 在...上 许多 平台
* :github:`50065` - 测试 tests/subsys/shell/shell 测试 case 失败 在...中 daily 测试 在...上 许多 平台
* :github:`50061` - Bluetooth: Samples: bluetooth_audio_source does not send multiple streams
* :github:`50044` - reel_board: pyocd.yaml causes flashing error on reel board
* :github:`50033` - tests: subsys: fs: littlefs: filesystem.littlefs.custom fails to build
* :github:`50032` - tests: subsys: shell: shell.core and drivers.can.shell fails at shell_setup
* :github:`50029` - Unable 到 使用 函数 从 gsm_ppp 驱动
* :github:`50023` - 测试 一些 驱动 测试 的 frdm_k64f 构建 失败 在...中 twister (shows devicetree 错误
* :github:`50016` - jlinkarm.so 文件 重命名 在...中 最新 J-Link 驱动
* :github:`49988` - boards: pinnacle_100_dvk: UART1 flow control is not turned on
* :github:`49987` - Unable 到 编译 在...上 windows
* :github:`49985` - STM32:NUCLEO_WL55JC No serial RX in STOP mode
* :github:`49982` - SD: f_sync  总是 失败 使用  sdhc_spi 驱动
* :github:`49970` - strange behavior in the spi_flash example
* :github:`49960` - LoRaWAN Code won't linking when config with CN470 region
* :github:`49956` - ``NRF_DRIVE_S0D1`` option is not always overridden in the ``nordic,nrf-twi`` and ``nordic,nrf-twim`` nodes
* :github:`49953` - stm32 gpio_basic_api test fail with CONFIG_ZTEST_NEW_API
* :github:`49939` - stm32 adc driver_api test fails on stm32wb55 and stm32l5
* :github:`49938` - drivers/modem/gsm_ppp.c:  unnecessary modem_cmd_handler_tx_lock when CONFIG_GSM_MUX disabled
* :github:`49924` - 测试 驱动 pwm_api 和 pwm_loopback 测试 失败 在...上 frdm_k64f 板
* :github:`49923` - ASSERTION FAIL [!arch_is_in_isr()] @ WEST_TOPDIR/zephyr/kernel/sched.c:1449
* :github:`49916` - renesas smartbond family Kconfig visible to non-renesas devices
* :github:`49915` - Bluetooth: Controller: Syncing with devices with per. adv. int. < ~10ms eventually causes events from BT controller stop arriving
* :github:`49903` - riscv: Enabling IRQ vector table makes Zephyr unbootable
* :github:`49897` - STM32: NUCLEO_WL55JC internal (die) temperature incorrect
* :github:`49890` - drivers/can: stm32_fd: CONFIG_CAN_STM32FD_CLOCK_DIVISOR not applied in driver setup
* :github:`49876` - 驱动  twai: 驱动 失败 initialization
* :github:`49874` - STM32G0 HW_STACK_PROTECTION Warning
* :github:`49852` - uart: 额外 XOFF byte 在...中  读取 缓冲区
* :github:`49851` - Bluetooth Controller with Extended Advertising
* :github:`49846` - mimxrt1160_evk 网络 samples 停止 工作
* :github:`49825` - net: ip: tcp: use zu format specifier for size_t
* :github:`49823` - Example Application: Use of undocumented zephyr/module.yml in application folder
* :github:`49814` - Cortex-A9 fails to build cmsis due to missing core_ca.h
* :github:`49805` - stm32f1: can2 & eth pin remap not working
* :github:`49803` - I/O APIC Driver in Zephyr makes incorrect register access.
* :github:`49792` - test-ci:  adc-dma :  frdm-k64f: dma dest addess assert
* :github:`49790` - Intel CAVS25: Failure in tests/boards/intel_adsp/smoke sporadically
* :github:`49789` - it8xxx2_evb: tests/crypto/tinycrypt/ test takes longer on sdk 0.15.0
* :github:`49786` - nsim_em: 测试 失败 到 运行 tests/kernel/timer/timer_behavior
* :github:`49769` - STM32F1 CAN2 does not enable master can gating clock
* :github:`49766` - 记录 downstream 模块 配置 recommendations
* :github:`49763` - nucleo_f767zi: sample.net.gptp build fails
* :github:`49762` - esp32: testing.ztest.error_hook.no_userspace build fails due to array-bounds warnings
* :github:`49760` - frdm_kl25z: sample.usb.dfu Kconfig issue causing build failure
* :github:`49747` - CAN2 接口 在...上 STM32F105 不 工作
* :github:`49738` - Bluetooth: Controller: Restarting periodic advertising causes crash when ADV_SYNC_PDU_BACK2BACK=y
* :github:`49733` - Error log "Could not lookup stream by iso 0xXXXXXXXX" from unicast server if client release the stream
* :github:`49717` - mcumgr: Bluetooth transport fix prevents passing GATT notify status back to SMP
* :github:`49716` - Intel CAVS15/18: Failure in tests/arch/common/timing
* :github:`49715` -  函数 ospi_read_sfdp 在...中 drivers/flash/flash_stm32_ospi.c  损坏  栈
* :github:`49714` - 测试 tests/drivers/gpio/gpio_api_1pin 失败 在...上 mec172xevb_assy6906 在...中 daily 测试
* :github:`49713` - frdm_k64f: 测试 失败 到 运行 tests/drivers/adc/adc_dma/drivers.adc-dma
* :github:`49711` - tests/arch/common/timing/arch.common.timing.smp fails for CAVS15, 18
* :github:`49703` - eSPI: Add platform specific Slave to Master Virtual Wires
* :github:`49696` - twister: testplan: toolchain_exclude filter is overridden by integration_platforms
* :github:`49687` - West: Allow having .west folder and west.yml in the same folder
* :github:`49678` - Zephyr 3.2 module updates overview
* :github:`49677` - STM32U5 consumes more current using power management
* :github:`49663` - Bluetooth seems to not work randomly on target device
* :github:`49662` - hello world+ mcuboot is not working
* :github:`49661` - mcumgr: bt transport runs in system workqueue thread and can cause resource deadlock
* :github:`49659` - logging: LOG_* appends 0x0D to 0x0A
* :github:`49648` - tests/subsys/logging/log_switch_format, log_syst build failures on CAVS
* :github:`49637` - CMSIS-DSP tests broken with SDK 0.15.0
* :github:`49631` - arch: arm: FP stack warning with GCC 12 and ``CONFIG_FPU=y``
* :github:`49629` - Bluetooth: ISO Broadcast sample fails to send data on nRF5340
* :github:`49628` - Compilation 失败 当...时 ASAN  使用 带 gcc
* :github:`49618` - &usart2_rx_pd6 no more available for STM32L073RZ
* :github:`49616` - acrn_ehl_crb: The testcase tests/kernel/common failed to run.
* :github:`49609` - sdk: 失败 到 运行 tests/subsys/logging/log_core_additional
* :github:`49607` - ADC reading on E73-2G4M04S1B and nrf52dk
* :github:`49606` - BeagleBone Black / AM335x Support
* :github:`49605` - it8xxx2_evb: tests/kernel/timer/timer_api test failed after commit cb041d06
* :github:`49602` - Bluetooth: Audio: Build error when enable  CONFIG_LIBLC3
* :github:`49601` - mec15xxevb_assy6853: tests/drivers/adc/adc_api asynchronous test failed
* :github:`49599` - Bluetooth: Host: Unable to pair zephyr bluetooth peripheral with Secure connection and static passkey
* :github:`49590` - devicetree parsing  不 错误 出 在...上 duplicate node 名称
* :github:`49587` - cross-compile toolchain variant doesn't working properly with multilib toolchain
* :github:`49586` - Json parser is incorrect with undefined parameter
* :github:`49578` - [RFC] Deprecate <zephyr/zephyr.h>
* :github:`49576` - 测试 内核 定时器 timer_behavior: kernel.timer.timer 失败
* :github:`49572` - Reproducable 构建 带 MCUboot 签名
* :github:`49542` - sdk: it8xxx2_evb cannot build the hello_world sample after zephyr SDK upgrade to 0.15.0
* :github:`49540` - Bluetooth: Host: sync termination callback parameters not populated correctly when using per. adv. list feature.
* :github:`49531` - LE Audio: Broadcast Sink not supporting general and specific BIS codec configurations in the BASE
* :github:`49523` - k_sleep in native_posix always sleeps one tick too much
* :github:`49498` - net: lib: coap: update method_from_code() to report success/failure
* :github:`49493` - Bluetooth: ISO: samples/bluetooth/broadcast_audio_source error -122
* :github:`49491` - arch.interrupt test fails on ARM64 QEMU targets when compiled with GCC 12
* :github:`49482` - stm32g0 中断 用于 usart3,4,5,6 所有 设置 到 29
* :github:`49471` - stm32: dietemp node generates warning
* :github:`49465` - Bluetooth: Controller: Periodic adv. sync. degraded performance on latest main branch
* :github:`49463` - STM32G0B0 错误 出 在...上 stm32g0_disable_dead_battery 函数 在...中 soc.c
* :github:`49462` - 测试 tests/kernel/fatal/exception/ 测试 case 失败
* :github:`49444` - mcumgr: Outgoing packets that are larger than the transport MTU are wrongly split into different individual messages
* :github:`49442` - Intel CAVS25: Failure in tests/kernel/smp
* :github:`49440` - test-ci: mimxrt11xx: testing.ztest.base.verbose_x and crypto.tinycryp : run failure no console output
* :github:`49439` - test-ci: lpcxpresso54114_m4: libraries.devicetree.devices.requires test failure
* :github:`49410` - Bluetooth: Scan responses with info about periodic adv. sometimes stops being reported
* :github:`49406` - flash_stm32_ospi: OSPI wr in OPI/STR mode is for 32bit address only
* :github:`49360` - west boards doesn't print boards from modules
* :github:`49359` - nrf5*: crash when Bluetooth advertisements and flash write/erase are used simultaneously
* :github:`49350` - RFC: Add arch aligned memory Kconfig option
* :github:`49342` - Zephyr hci_usb sample cannot use LE coded phy
* :github:`49331` - device if got the ip is "10.4.239.xxx" when join in the switchboard, then the device can not visit the outer net.
* :github:`49329` - twister: frdm_k64f: test string mismatch
* :github:`49315` - loopback 套接字 发送 从 shell 挂起
* :github:`49305` - Can't 读取 和 写入 到  也不 刷写 在 地址 0x402a8000 在...上 RT1060
* :github:`49268` - 测试 samples/boards/stm32/power_mgmt/serial_wakeup 失败 在...上 mec15xxevb_assy6853 和 几个 stm32 板
* :github:`49263` - ztest: tracing backend works incorrectly when new ZTEST enabled.
* :github:`49258` - MCUboot not loading properly due to missing ALIGN
* :github:`49251` - STM32 HW TIMER + DMA + DAC
* :github:`49203` - Intel CAVS15: Failure in tests/boards/intel_adsp/hda,hda_log
* :github:`49200` - Intel CAVS: Failure in tests/kernel/interrupt
* :github:`49195` - Integrate Zephyr SDK 0.15.0 to the Zephyr main CI
* :github:`49184` - DHCP client is not ``carrier`` aware
* :github:`49183` - Missing handling of UNKNOWN_RSP in peripheral PHY UPDATE procedure
* :github:`49178` - subsys: pm:  stats:  typo causes build failure
* :github:`49177` - usb: sam0: 设备 驱动  leaking 内存 当...时 接口  复位
* :github:`49173` - Bluetooth: empty notification received by peer after unsubscribe
* :github:`49169` - v2m_musca_s1_ns fails to build several tfm related samples
* :github:`49166` - samples/drivers/flash_shell/sample.drivers.flash.shell 失败 到 构建 在...上  少数 nxp 平台
* :github:`49164` - samples/arch/smp/pi/sample.smp.pi 失败 在...上  数量 esp32 平台
* :github:`49162` - Calling cache maintenance APIs from user mode threads result in a bad syscall error.
* :github:`49154` - SDMMC driver with STM32 U575
* :github:`49145` - tests: kernel: fifo: fifo_timeout: kernel.fifo.timeout fails on nrf5340dk_nrf5340_cpuapp
* :github:`49142` - Bluetooth: Audio: MCC subscribe failure
* :github:`49136` - L2CAP ecred test cases failed.
* :github:`49134` - STM32G070RBT6 can not build with zephyr 3.1.99
* :github:`49119` - ARC: west: mdb runner: fix folder where MDB is run
* :github:`49116` - cmake cached BOARD_DIR variable does not get overwritten
* :github:`49106` - 增加 cherryusb as  模块
* :github:`49105` - hda_host and hda_link registers block size are not equal
* :github:`49102` - hawkbit - dns name randomly not resolved
* :github:`49100` - STM b_u585i_iot02a  NOR flash and OSPI_SPI_MODE, erase failed
* :github:`49086` - twister: frdm_k64f: twister process blocks after the flash error occurs
* :github:`49074` - GD32: Use clocks instead rcu-periph-clock property
* :github:`49073` - SOC_FLASH_LPC vs SOC_FLASH_MCUX
* :github:`49066` - Mcumgr img_mgmt_impl_upload_inspect() can cause unaligned memory access hard fault.
* :github:`49057` - USB Mass Storage Sample crashes due to overflow of Mass Storage Stack
* :github:`49056` - STM b_u585i_iot02a MCUboot crash
* :github:`49054` - STM32H7 apps are broken in C++ mode due to HAL include craziness
* :github:`49051` - Nrf52832 ADC SAMPLE cannot compile
* :github:`49047` - LORAWAN Devicetree sx1262 setup on rak4631_nrf52840 board
* :github:`49046` - Cannot use devices behind I2C mux (TCA9548A)
* :github:`49044` - doc: boards: litex_vexrisc: update with common environment variables and arty-a7-100t support
* :github:`49036` - soc: telink_b91: ROM region section overlap
* :github:`49027` - Regulator support for gpio-leds
* :github:`49019` - Fix multiple issues with adxl372 driver
* :github:`49016` - intel_adsp smoke test fails with CONFIG_LOG_MIPI_SYST_USE_CATALOG=y
* :github:`49014` - Advertising 地址 不 更新 在...之后 RPA Timeout 带 扩展 Advertising 启用
* :github:`49012` - pm breaks intel dai ssp in cavs25
* :github:`49008` - ESP32:  net_buf_get() FAILED
* :github:`49006` - tests: subsys: portability: cmsis_rtos_v2: portability.cmsis_rtos_v2 -   test_timer - does not end within 60 sec
* :github:`49005` - samples: tfm_integration: tfm_regression_test: sample.tfm.regression_ipc_lvl2 no console output within 210 sec - timeout
* :github:`49004` - unexpected eof in qemu_cortex and mps2
* :github:`49002` - tests: subsys: settings: functional: fcb: system.settings.functional.fcb fails
* :github:`49000` - tests: arch: arm: arm_thread_swap: arch.arm.swap.common.no_optimizations USAGE FAULT
* :github:`48999` - tests: arch: arm: arm_interrupt: arch.interrupt.no_optimizations Wrong crash type got 2 expected 0
* :github:`48997` - tests: kernel: workq: work_queue: kernel.workqueue fails
* :github:`48991` - Receiving message from pc over PCAN-USB FD
* :github:`48977` - kernel: mem_protect: mimxrt11xx series build failure
* :github:`48967` - modem: hl7800 runtime log control API is broken
* :github:`48960` - coap_packet_parse()  return 不同 值 based 在...上 错误 类型
* :github:`48951` - stm32wb55 BLE unable to connect / pair
* :github:`48950` - cmake: string quotes are removed from extra_kconfig_options.conf
* :github:`48937` - Compilation error when adding lwm2m client on CHIP/matter sample
* :github:`48921` - 构建 system/west: 增加  警告 如果 任何 project repo  不 匹配  manifest
* :github:`48918` - ztest: tests: add CONFIG_ZTEST_SHUFFLE=y to tests/subsys/logging/log_benchmark/prj.conf cause build failure
* :github:`48913` - net: Add pointer member to net_mgmt_event_callback struct to pass user data to the event handler.
* :github:`48912` - sample.drivers.flash.shell: Failed on NXP targets
* :github:`48911` - sample.drivers.flash.shell: Failed on atmel targets
* :github:`48907` - Does esp32 support BLE Mesh
* :github:`48897` - twister --sub-test never works
* :github:`48880` - BLE notifications on custom service not working anymore: <wrn> bt_gatt: Device is not subscribed to characteristic
* :github:`48877` - tests: kernel: mem_slab: mslab: kernel.memory_slabs fails
* :github:`48875` - tests: kernel: context: kernel.context fails at test_busy_wait and Kernel panic at test_k_sleep
* :github:`48863` - hawkbit subsystem - prints garbage if debug enabled and no update pending
* :github:`48829` - cbprintf is broken on multiple platforms with GCC 12
* :github:`48828` - Clicking a link leads to "Sorry, Page Not Found", where they ask to notify this GitHub
* :github:`48823` - Bluetooth: controller: llcp: limited nr. of simultaneous connections
* :github:`48813` - Bluetooth: bt_conn_disconnect randomly gives error "bt_conn: not connected!"
* :github:`48812` - Bluetooth controller extended advertisement crashes in lll layer
* :github:`48808` - Pinctl api breaks NXP imx6sx
* :github:`48806` - Bluetooth: controller: conformance test instability
* :github:`48804` - LE Audio: Add HAP sample to Zephyr footprint tracking
* :github:`48801` - test: driver: wdt: wdt cases fails in LPC platform randonly
* :github:`48799` - 为什么   命令 input incomplete?
* :github:`48780` - 板 bus 设备 label 名称  include 地址 在...上 bus
* :github:`48779` - net.socket.select: failed (qemu/mps2_an385)
* :github:`48757` - Windows10 Installation: Failed to run ``west update``
* :github:`48742` - 链接 失败 期间 构建 当...时 referencing 函数 在...中 ``zephyr/bluetooth/crypto.h``
* :github:`48739` - net: tcp: Implicit MSS value is not correct
* :github:`48738` - dts: label: label defined in soc does not take effects in final zephyr.dts
* :github:`48731` - gen_handles script fails with pwmleds handle
* :github:`48725` - arm_thread_swap:  tests/arch/arm/arm_thread_swap/ failed on reel_board
* :github:`48724` - mpu9250 驱动 init 函数 register 设置 使用  相同 配置 参数 twice.
* :github:`48722` - flash_map: pointer dereferencing causes build to fail
* :github:`48718` - Completely 禁用 IP 支持 leads 到  构建 错误 当...时 启用 IEEE 802.15.4 L2 支持
* :github:`48715` - 启用 NET_L2_IEEE802154 和 IEEE802154_RAW_MODE together 损坏  构建
* :github:`48699` - Is there a way to port the Bluetooth host stack to linux?
* :github:`48682` - ADC Support for STM32U575
* :github:`48671` - SAM V71B Initial USB Transfer Drops Data Bytes
* :github:`48665` - tests/usb/device: Add zassert to match zassume usage.
* :github:`48642` - nucleo_l011k4  不 构建
* :github:`48630` - Process: maintainer involvement in triaging issues
* :github:`48626` - jlink flasher 不 工作 带 最近 版本 的 pylink dependency
* :github:`48620` - LC3 External Source Code
* :github:`48591` - Can't run zephyr application from SDRAM on RT1060-EVKB
* :github:`48585` - net: l2: ieee802154: decouple l2/l3 layers
* :github:`48584` - Remove netifaces Python package dependency
* :github:`48578` - NRF GPIO Toggle introduces race condition when multithreaded
* :github:`48567` - MIMXRT1060 custom board support for NXP HAL modules
* :github:`48547` - ztest: Incorrect display of test duration value.
* :github:`48541` - subsys/net/l2/ppp/fsm.c: BUS FAULT
* :github:`48537` - Can gpio output configuration flags be expressed in the devicetree?
* :github:`48534` - SMF missing events
* :github:`48531` - RFC: Changing the sys_clock interface to fix race conditions.
* :github:`48523` - Mathematical operations in Kconfig
* :github:`48518` - ``samples/sensor/*``: Build issue when board expose sensors defined on both I2C and SPI buses
* :github:`48516` - 刷写 sam: 构建 错误 用于 sam4s_xplained
* :github:`48514` - bsim mesh establish_multi.sh doesn't 发送 数据 用于 一个 的 设备
* :github:`48512` - frdm_k64f : failed to run tests/drivers/dma/scatter_gather
* :github:`48507` - 错误 在...上 控制台 usb app.overlay
* :github:`48501` - Usage Fault :  Illegal use of EPSR , NRFSDK 2.0.0 and BLE DFU NRF52840 DK
* :github:`48492` - gdbstub for arc core
* :github:`48480` - ZTEST: duplicate symbol linker error
* :github:`48471` - net: tcp: Persistent timer for window probing does not implement exponential backoff
* :github:`48470` - Inconsistent return value of uart_mux_fifo_fill when called inside/outside of an ISR
* :github:`48469` - [bisected] 5a850a5d06e1  损坏 一些 测试 在...上 ARM64
* :github:`48465` - net: tcp: SYN flag received after connection is established should result in connection reset
* :github:`48463` - Grant Triage permission level to @aurel32
* :github:`48460` - Provide duration of each testsuite and testcase in ztest test summary.
* :github:`48459` - bluetooth: host: Dangling pointer in le_adv_recv
* :github:`48447` - ``hwinfo devid`` does not work correctly for NXP devices using ``nxp,lpc-uid`` device binding
* :github:`48444` - Problem upgrading ncs 1.5.1 upgrade to ncs 1.9.1 failed
* :github:`48424` - ZTEST Framework fails when ztest_run_all is called multiple times
* :github:`48416` - samples: samples/subsys/tracing is broken for UART tracing
* :github:`48392` - Compiling failure watchdog sample with nucleo_u575zi_q
* :github:`48386` - twister cannot take ``board@revision`` as platform filter
* :github:`48385` - Compilation failures on Cavs 18/20/25 GCC
* :github:`48380` - shell: Mixing mandatory arguments w/ SHELL_OPT_ARG_RAW causes crash
* :github:`48367` - 错误 时钟 assigned
* :github:`48343` - NVS nvs_recover_last_ate()  不 对齐 数据 长度
* :github:`48328` - Add API to get the nvs_fs struct from the settings backend
* :github:`48321` - twister: 缺陷 在...中 平台 名称 verification
* :github:`48306` - Lwm2m_client sample broken on native_posix target
* :github:`48302` - West search for "compatible" device tree property does not expand C preprocessor macros
* :github:`48290` - ESP32 ble no work while enable CONFIG_SETTINGS
* :github:`48282` - BT_H4 overriding BT_SPI=y causing build to fail - HCI Host only build SPI bus
* :github:`48281` - Fix github permissions for user "alevkoy"
* :github:`48267` - No model in devicetree_unfixed.h :
* :github:`48253` - 仅  第一 失败 测试  中止 和 marked 失败
* :github:`48223` - base64.c encode returns wrong count of output bytes
* :github:`48220` - adxl345: sensor value calculation should be wrong
* :github:`48216` - Running gPTP sample application on SAMe54 Xplained pro(Supports IEEE 802.1 AS gPTP clock) , PDelay Response Receipt Timeout
* :github:`48215` - docs: build the documentation failed due to "Could NOT find LATEX"
* :github:`48198` - NPCX Tachometer driver compiled despite status = "disabled"
* :github:`48194` - Support J-Link debugger for RaspberryPi Pico
* :github:`48185` - LV_Z_DISPLAY_DEV_NAME symbol has not got "parent" symbol with a type
* :github:`48175` - stm32 octospi flash driver
* :github:`48149` - Sensor Subsystem: client facing API: finding sensors
* :github:`48115` - tests: subsys: dfu: mcuboot_multi: dfu.mcuboot.multiimage hangs at first test case - test_request_upgrade_multi
* :github:`48113` - Zephyr support for STM32U5 series MCU
* :github:`48111` - LVGL: License agreement not found for the font arial.ttf
* :github:`48104` - [v 1.13 ] HID is not connecting to Linux based Master device
* :github:`48098` - 构建 错误 用于 samples/bluetooth/unicast_audio_server 的 nrf52dk-nrf52832 板
* :github:`48089` - AF_PACKET sockets not filling L2 header details in ``sockaddr_ll``
* :github:`48081` - tests/drivers/clock_control/stm32_clock_configuration/stm32u5_core not working with msis 48
* :github:`48071` - mec15xxevb_assy6853: test_i2c_pca95xx failed
* :github:`48060` - Have modbus RTU Client and modbus TCP Master on the same microcontroller
* :github:`48058` - Reading out a GPIO pin configured as output returns invalid value.
* :github:`48056` - Possible null pointer dereference after k_mutex_lock times out
* :github:`48055` - samples: subsys: usb: audio: headphones_microphone and headset - Can not get USB Device
* :github:`48051` - samples: logger: samples/subsys/logging/logger/sample.logger.basic failed on acrn_ehl_crb board
* :github:`48047` - Reference 到 过时 文件 在...中 cmake 打包 docs
* :github:`48007` - 测试 gpio 驱动 失败 在...中 pin_get_config
* :github:`47991` - BLE functionality for STM32WB55 is limited with full version of BLE stack
* :github:`47987` - test: samples/boards/mec15xxevb_assy6853/power_management failed after commit 5f60164a0fc
* :github:`47986` - Rework of STM32 bxCAN driver filter handling required
* :github:`47985` - ARC wrong .debug_frame
* :github:`47970` - 刷写 SFDP 参数 地址  不 正确
* :github:`47966` - TCP: Zero window probe packet incorrect
* :github:`47948` - _kernel.threads' always points to NULL(0x0000'0000)
* :github:`47942` - Mutex priority inheritance when thread holds multiple mutexes
* :github:`47933` - tests: subsys: logging: log_switch_format: logging.log_switch_format - test_log_switch_format_success_case - Assertion failed
* :github:`47930` - tests: arch: arm: arm_interrupt: arch.interrupt.no_optimizations - Data Access Violation - MPU Fault
* :github:`47929` - tests: arch: arm: arm_thread_swap: arch.arm.swap.common.no_optimizations - Data Access Violation - MPU Fault
* :github:`47925` - Asynchronous UART API (DMA) not working like expected on nrf52840
* :github:`47921` - 测试 pin_get_config 失败 在...上 it8xxx2_evb
* :github:`47904` - drivers: can: loopback driver only compares loopback frames against CAN IDs in installed filters
* :github:`47902` - drivers: can: mcux: flexcan: failure to handle RTR frames correctly
* :github:`47895` - samples: smp_svr missing CONFIG_MULTITHREADING=y dependency
* :github:`47860` - Bluetooth: shell: bt init sync enables Bluetooth asynchronously
* :github:`47857` - Zephyr USB-RNDIS
* :github:`47855` - tests: arch: arm: fpu: arch.arm.swap.common.fpu_sharing.no_optimizations - Data Access Violation - MPU Fault
* :github:`47854` - Multiple blinking LED's cannot be turned off
* :github:`47852` - samples: boards: nrf: s2ram No valid output on console
* :github:`47847` - 如何 到 PM 更改 pm_state
* :github:`47833` - Intel CAVS: cavstool.py 失败 到 提取 完成 日志 从 winstream 缓冲区 当...时 日志记录  frequent
* :github:`47830` - Intel CAVS: Build failure due to #47713 PR
* :github:`47825` - qemu_cortex_a53_smp: tests/kernel/profiling/profiling_api failed
* :github:`47822` - 栈 Overflow 当...时 calling spi 在  中断 在...上 STM32l4
* :github:`47783` - warning: attempt to assign the value 'y' to the undefined symbol UART_0_NRF_FLOW_CONTROL
* :github:`47781` - MCUbootloader with b_u585i_iot02a (stm32u585) boot error
* :github:`47780` - WS2812 驱动 不 工作 在...上 nRF52833DK
* :github:`47762` - 一些 github users 在...中  MAINTAINERS 文件  缺失 权限
* :github:`47751` - soc/arm/common/cortex_m doesn't work for out-of-tree socs
* :github:`47742` - NXP LPC MCAN driver front-end lacks pinctrl support
* :github:`47734` - tests/posix/eventfd/ : failed on both nucleo_f103rb and nucleo_l073rz with 20K RAM only
* :github:`47731` - JESD216 fails to read SFDP on STM32 targets
* :github:`47725` - qemu_arc: tests/kernel/context/ failed when migrating to new ztest API
* :github:`47719` - Configure-time library dependency problem
* :github:`47714` - 测试 tests/lib/sprintf/ 构建 失败
* :github:`47702` - twister: regression : Failures are counted as errors
* :github:`47696` - tests: arch: arm: arm_thread_swap: regression since use of new ztest API
* :github:`47682` - bt_gatt_unsubscribe 创建 写入 request 到 CCC 和 then 取消 它
* :github:`47676` - bt_data_parse  destructive 没有 警告
* :github:`47652` -  client-server based cavstool.py   stuck 当...时  ROM  不 启动
* :github:`47649` - ATT Notification buffer not released after reconnection
* :github:`47641` - Poor Ethernet Performance using NXP Enet MCUX Driver
* :github:`47640` - Zephyr and caches: a difficult love story.
* :github:`47613` - Samples / Tests without a testcase.yaml or sample.yaml
* :github:`47683` - TCP Connected Change the window size to 1/3/ff fail
* :github:`47609` - posix: pthread: descriptor leak with pthread_join
* :github:`47606` - nvs_read return 值  不 正确
* :github:`47592` - test: tests/drivers/gpio/gpio_basic_api failed after commit 2a8e3fe
* :github:`47588` - tests: sprintf: zero-length gnu_printf format string
* :github:`47580` - https connect failing with all the samples (qemu_x86 & mbedtls)
* :github:`47576` - undefined reference to ``__device_dts_ord_20`` When building with board hifive_unmatched on flash_shell samples
* :github:`47568` - uart_mcux_lpuart 驱动 activates  noise 错误 中断 但  不 clear  noise 错误 flag
* :github:`47556` - sample: 日志记录 构建 失败 用于 samples/subsys/logging/syst
* :github:`47551` - Enabling CONFIG_OPENTHREAD_SRP_CLIENT on NRF52840 dongle board leads to MBED compilation errors.
* :github:`47546` - Revert https://github.com/zephyrproject-rtos/zephyr/pull/47511
* :github:`47520` - 支持 用于 sub-ghz 通道 在...中 at86rf2xx radio 驱动
* :github:`47512` - up_squared: issues of EFI console feature
* :github:`47508` - 测试 arch:  xtensa_asm2 测试  损坏
* :github:`47483` - PPP + GSM MUX doesn't work with Thales PLS83-W modem
* :github:`47476` - SX127x LoRaWAN - Failing on Boot - Missing Read/Write functions?
* :github:`47461` - Unable to build the flash_shell samples with board cc1352r1_launchxl
* :github:`47458` - BQ274XX Sensors Driver - Fails with CONFIG_BQ274XX_LAZY_CONFIGURE
* :github:`47445` - USB OTG FS controller support on STM32F413 broken
* :github:`47428` - SRAM increase in Bluetooth  [samples: bbc_microbit: pong fails to build]
* :github:`47426` - ZTEST_USER 测试  skipped 在...上 系统 没有 userspace 支持
* :github:`47420` - Tests: unittest with new ZTEST API
* :github:`47409` - LE Audio: Read PACS available contexts as unicast client
* :github:`47407` - stm32l5: tfm: Build error on tests/arch/arm/arm_thread_swap_tz
* :github:`47379` - Crypto sample fail to build with cryp node in .dts for STM32u5 (error: unknown type name 'CRYP_HandleTypeDef' etc.)
* :github:`47356` - cpp: global static object initialisation may fail for MMU and MPU platforms
* :github:`47330` - ARM Cortex-R52 doesn't have SPSR_hyp
* :github:`47326` - 驱动 WINC1500: 问题 带 缓冲区 allocation 当...时 使用 套接字
* :github:`47323` - STM32WL LoRa SoC stuck at initialization due to SPI transmit buffer not emptying
* :github:`47307` - 测试 内核 fatal: 异常 构建 失败 在...上 multiple 平台
* :github:`47301` - Module request: Lua
* :github:`47300` - Intel CAVS: Failure in tests/lib/spsc_pbuf
* :github:`47292` - it8xxx2_evb: many test cases failed probably due to the west update
* :github:`47288` - tests: posix: increase coverage for picolibc
* :github:`47275` - builds are broken with gnuarmemb toolchain, due to picolibc tests/configuration
* :github:`47273` - linker script: Vector table regression due to change in definition of _vector_end
* :github:`47272` - nrf51_ble400: onboard chip should be updated to nRF51822_QFAC in dts
* :github:`47248` - LE Audio: Crash on originating call.
* :github:`47240` - net: tcp: Correctly handle overlapped TCP retransmits
* :github:`47238` - SD Card init issue when CONFIG_SPEED_OPTIMIZATIONS=y
* :github:`47232` - Please add STM32F412RX
* :github:`47222` - zephyr doc: Unable to open pdf document version 3.1.0
* :github:`47220` - Twister: Skipping ``*.cpp`` files
* :github:`47204` - CAN filter with RTR mask causes infinite loop in MCAN driver on filtered message arrival
* :github:`47197` - BLE latency decreasing and increasing over time (possibly GPIO issue)
* :github:`47146` - STM32F103:  USB clock prescaler isn't set during USB initialisation
* :github:`47127` - twister : frdm_k64f ：Non-existent tests appear and fail on tests/lib/cmsis_dsp/transform
* :github:`47126` - New ztest API: build failure on qemu_cortex_m3 when CONFIG_CMAKE_LINKER_GENERATOR=y
* :github:`47119` - ADC_DT_SPEC_GET not working for channels >= 10
* :github:`47114` - ``check_compliance.py`` crash on Ubuntu 22.04
* :github:`47105` - drivers: clock_control: stm32 common: wrong PLLCLK rate returned
* :github:`47104` - Bluetooth: Controller: Errors in implementation of tx buffer queue mechanism
* :github:`47101` - drivers: clock_control: stm32 common: PLL_Q divider not converted to reg val
* :github:`47095` - ppp network interface -  MQTT/TCP communication
* :github:`47082` - 驱动 modem: AT 命令 发送 在...之前 OK 从 上一个  接收
* :github:`47081` - on x86, k_is_in_isr() returns false in execption context
* :github:`47077` - Intel CAVS: tests/subsys/logging/log_switch_format/ are skipped as no result captured
* :github:`47072` - ZTEST Docs Page
* :github:`47062` - dt-bindings: clock: STM32G4 device clk sources selection helper macros don't match the SOCs CCIPR register
* :github:`47061` - pipes: Usage between task and ISR results in corrupted pipe state
* :github:`47054` - it8xxx2_evb: 刷写 失败 在...中 daily 测试
* :github:`47051` - drivers: usb: stm32: usb_write size on bulk transfer problematic
* :github:`47046` - samples/net/sockets/packet: Bus fault
* :github:`47030` - drivers: gpio: nrfx: return -ENOTSUP rather than -EIO for misconfigurations
* :github:`47025` - mimxrt1050_evk: reset cause
* :github:`47021` - Integrate Würth Elektronik Sensors SDK code for use in sensor drivers
* :github:`47010` - ACRN: 失败 到 运行  测试 case tests/drivers/coredump/coredump_api
* :github:`46988` - samples: net: openthread: coprocessor: RCP is missing required capabilities: tx-security tx-timing
* :github:`46985` - uOSCORE/uEDHOC integration as a Zephyr module
* :github:`46962` - 回归问题 在...中 apds9960 驱动
* :github:`46954` - Binaries found in hal_nxp without conspicuous license information
* :github:`46935` - Not printk/log output working
* :github:`46931` - flash_stm32_ospi.c: Unable to erase flash partition using flash_map API
* :github:`46928` - drivers: modem: gsm_ppp: support hardware flow control
* :github:`46925` - Intel CAVS: tests/lib/mem_block/ failed, caused by too frequent log output.
* :github:`46917` - frdm_k64f : failed to run tests/drivers/gpio/gpio_get_direction
* :github:`46901` - RFC: I3C I2C API
* :github:`46887` - Automatically 组织 BLE EIR/AD 数据 进入  struct instead 的 提供 它 在...中  simple_network_buffer.
* :github:`46865` - Intel CAVS: Support for different ports for client / server
* :github:`46864` - Intel CAVS: cavstool_client.py sporadically fails
* :github:`46847` - STOP2 模式 在...上 Nucleo-WL55JC1 不 访问
* :github:`46829` - LE Audio: Avoid multiple calls to ``bt_iso_chan_connect`` in parallel
* :github:`46822` - L2CAP disconnected packet timing in ecred reconf function
* :github:`46807` - lib: posix: semaphore: use consistent timebase in sem_timedwait
* :github:`46801` - Revisit 模块 和 inclusion 在...中  默认 manifest
* :github:`46799` - IRQ vector table: how to support different formats
* :github:`46798` - Zephyr  不 存储  新 IRK 当...时 另一个 设备 re-bonds 带  Zephyr 设备
* :github:`46797` - UART Asynchronous API continuous data receiving weird behaviour
* :github:`46796` - IRQ vector table
* :github:`46793` - 测试 posix: 使用 新 ztest API
* :github:`46765` - test-ci: kernel.timer: test_timer_remaining asserts
* :github:`46763` - LE Audio: Unicast Audio read PAC location
* :github:`46761` - logging: tagged arguments feature does not work with char arrays in C++
* :github:`46757` - Bluetooth: Controller: Missing validation of unsupported PHY when performing PHY update
* :github:`46749` - mbox: wrong syscall check
* :github:`46743` - samples: net: civetweb: websocket_server
* :github:`46740` - stm32 flash ospi fails on stm32l5 and stm32u5 disco
* :github:`46734` - drivers/disk: sdmmc: Doesn't compile for STM32F4
* :github:`46733` - ipc_rpmsg_static_vrings creates unaligned TX virtqueues
* :github:`46728` - mcumgr: rt1060: upload an image over the shell does not work
* :github:`46725` - stm32: QSPI 刷写 驱动   损坏 priority 配置
* :github:`46721` - HAL module request: hal_renesas
* :github:`46706` - 增加 缺失 检查 用于 segment 数量
* :github:`46705` - 检查 缓冲区 大小 在...中 rx
* :github:`46698` - sm351 驱动 故障 当...时 使用 global 线程
* :github:`46697` - Missed interrupts in NXP RT685 GPIO driver
* :github:`46694` - Bluetooth: controller: LLCP: missing release of tx nodes on disconnect when tx data paused
* :github:`46692` - Bluetooth: controller: LLCP: reduced throughput
* :github:`46689` - Missing handling of DISK_IOCTL_CTRL_SYNC in sdmmc_ioctl
* :github:`46684` - ethernet: w5500: 驱动   栈 overflowed 当...时 读取  invalid(corrupt) 包 长度
* :github:`46656` - 计划 timing 问题
* :github:`46650` - qemu_x86: shell  不 工作 带 tip 的 主
* :github:`46645` - NRFX samples use deprecated API
* :github:`46641` - tests : kernel: context test_kernel_cpu_idle fails on nucleo_f091 board
* :github:`46635` - 测试 subsys: modbus: testcase 挂起 上 当...时 运行 由 twister
* :github:`46632` - Intel CAVS: Assertion failures in tests/boards/intel_adsp/hda
* :github:`46626` - USB CDC ACM Sample Application build fail with stm32_mini_dev_blue board
* :github:`46623` - Promote user "tari" to traige permission level
* :github:`46621` - drivers: i2c: Infinite recursion in driver unregister function
* :github:`46602` - BLE paring/connection issue on Windows (Zephyr 3.1.0)
* :github:`46594` - openthread net_mgmt_event_callback expects event info.
* :github:`46582` - LE Audio: PACS notify warns about failure when not connected
* :github:`46580` - Suggestion for additional configuration of ``twister --coverage`` gcovr formats
* :github:`46573` - raspberry pi pico always in mass storage mode
* :github:`46570` - Compiler warning when enabling userspace, sockets and speed optimization
* :github:`46558` - Bluetooth: Controller: Crash on bt_le_adv_start() when using CONFIG_BT_CTLR_ADVANCED_FEATURES
* :github:`46556` - Kconfig search webpage no longer shows all flags
* :github:`46555` - test: samples/drivers/adc twister result wrong
* :github:`46541` - Duplicate IDs used for different Systemview trace events
* :github:`46525` - PWM of it8xxx2
* :github:`46521` - '__device_dts_ord___BUS_ORD' undeclared here (not in a function); did you mean '__device_dts_ord_94'?
* :github:`46519` - STM32F4 CAN2 peripheral not working
* :github:`46510` - bluetooth: controller: llcp: set refactored LLCP as default
* :github:`46500` - Removal of logging v1
* :github:`46497` - Modbus: Add support for FC03 without floating-point extension as client
* :github:`46493` - Ethernet W5500 driver fails initialization with latest change - revert needed
* :github:`46483` - Update RISC-V ISA configs
* :github:`46478` - mimxrt1050_evk_qspi freeze when erasing flash
* :github:`46474` - LE Audio: Add seq_num and TS to bt_audio_send
* :github:`46470` - twister : retry 失败 参数  不 有效
* :github:`46464` - frdm_k64f : sudden failure to flash program
* :github:`46459` - Test framework incorrectly uses c++ keyword ``this``
* :github:`46453` - nRF52840 PWM with pinctrl - Unable to build samples/basic/blinky_pwm
* :github:`46446` - lvgl: Using sw_rotate with SSD1306 shield causes memory fault
* :github:`46444` - Proposal to integrate Cadence QSPI driver from Trusted Firmware-A
* :github:`46434` - ESP32-C3 UART1 broken since introduction of pinctrl
* :github:`46426` - Intel CAVS: Assertion failures on tests/boards/intel_adsp/smoke
* :github:`46422` - SDK version 14.2 increases image size significantly
* :github:`46414` - mcuboot: rt1060: confirmed image causes usage fault
* :github:`46413` - No multicast reception on IMX1064
* :github:`46410` - Add devicetree binding for ``zephyr,sdmmc-disk``
* :github:`46400` - STM32WB BLE HCI interface problem.
* :github:`46398` - ``mem_protect/mem_map``  失败 在...上 ``qemu_x86_tiny`` 当...时 userspace  启用
* :github:`46383` - fatal error: sys/cbprintf_enums.h: No such file or directory
* :github:`46382` - twister -x / --extra-args escaping quotes issue with CONFIG_COMPILER_OPTIONS
* :github:`46378` - CONFIG_SYS_CLOCK_TICKS_PER_SEC affects app code speed with tickless kernel
* :github:`46372` - Intel-ADSP: sporadic core boot
* :github:`46369` - LE Audio: Bidirectional stream is not created
* :github:`46368` - twister  : frdm_k64f ：the test case tests/subsys/logging/log_switch_format/logger.syst.v2.immediate/ blocks
* :github:`46366` - test_thread_stats_usage fail on arm64 fvp
* :github:`46363` - Initial Setup: Ubuntu 20.04: ensurepip is not available
* :github:`46355` - Sample wifi_station not building for esp32: No SOURCES given to Zephyr library: drivers__ethernet
* :github:`46350` - net: tcp: 当...时  第一 FIN 消息  lost,  连接  不 properly close
* :github:`46347` - MCUMGR_SMP_BT: system workqueue blocked during execution of shell commands
* :github:`46346` - LE Audio: Fatal crash when sending Audio data
* :github:`46345` - get_maintainer.py incorrectly invoked by Github?
* :github:`46341` - Zephyr scheduler lock: add selective locking up to a given priority ceiling
* :github:`46335` - For ESP32, initialization of static object during declaration with derived class type doesn't work.
* :github:`46326` - Async UART for STM32 U5 support
* :github:`46325` - ESP32 strcmp error while enable MCUBOOT and NEWLIB_LIBC
* :github:`46324` - it8xxx2_evb: tests/kernel/sched/schedule_api fail due to k_sleep(K_MSEC(100)) not correct
* :github:`46322` - Time units in shtcx sensor
* :github:`46312` - sample: bluetooth: ipsp - TCP not running over IPSP
* :github:`46286` - python-devicetree tox run fails
* :github:`46285` - nrf_qspi_nor: Inconsistent state of HOLD and WP for QSPI command execution causes hang on startup for some flash chips
* :github:`46284` - ring 缓冲区 在...中 item 模式 崩溃
* :github:`46277` - IMX8MM: Running fail a zephyr sample in the imx8mm
* :github:`46269` - docs: include/zephyr/net/socket.h is not documented anywhere
* :github:`46267` - docs: include/zephyr/net/http_client.h is not documented anywhere
* :github:`46266` - zephyr,sdmmc-disk compatible lacks a binding
* :github:`46263` - Regulator Control
* :github:`46255` - imxrt1010 错误 设备 tree 地址
* :github:`46235` - subsystem: Bluetooth LLL: ASSERTION FAIL [!link->next]
* :github:`46234` - samples: lsm6dso: prints incorrect anglular velocity units
* :github:`46208` - it8xxx2_evb: tests/kernel/sleep failed, elapsed_ms = 2125
* :github:`46206` - it8xxx2_evb: tests/kernel/fatal/exception/ assertion failed -- "thread was not aborted"
* :github:`46199` - LIS2DW12 I2C 驱动 使用 无效 写入 命令
* :github:`46186` - ISO Broadcaster fails silently on unsupported RTN/SDU_Interval combination
* :github:`46183` - LE Audio: Broadcast sink stop sending syncable once synced
* :github:`46180` - Add GitHub app for Googler notifications
* :github:`46173` - nRF UART callback is not passed correct index via evt->data.rx.offset sometimes
* :github:`46170` - ipc_service: open-amp backend may never leave
* :github:`46167` - esp32: Unable to select GPIO for PWM LED driver channel
* :github:`46164` - 脚本 发布 ci 检查 用于 问题 associated 带 backport prs
* :github:`46158` - frdm_k64f：failed to run test case tests/subsys/modbus/modbus.rtu/server_setup_low_none
* :github:`46157` - ACRN: 一些 cases 仍然 失败 因为 的  日志 缺失
* :github:`46124` - stm32g071 ADC drivers apply errata during sampling config
* :github:`46117` - Kernel events can’t be manipulated without race conditions
* :github:`46100` - lib: posix: support for perror()
* :github:`46099` - libc: minimal: add strerror() function
* :github:`46075` - BT HCI Raw on STM32WB55RG
* :github:`46072` - subsys/hawkBit: Debug log error in hawkbit example "CONFIG_LOG_STRDUP_MAX_STRING"
* :github:`46066` - TF-M: Unable to trigger NMI interrupt from non-secure
* :github:`46065` - Bluetooth: controller: llcp: verify that refactored LLCP is used in EDTT
* :github:`46049` - Usage faults on semaphore usage in driver (stm32l1)
* :github:`46048` - Use dts memory-region property to retrieve memory region used by driver
* :github:`46008` - stm32h7: gptp sample  不 工作 在 所有
* :github:`45993` - Matter(CHIP) support
* :github:`45955` - stm32h7 i2s support
* :github:`45953` - modem: simcom-sim7080: sendmsg() should result in single outgoing datagram
* :github:`45951` - modem: ublox-sara-r4: outgoing datagrams are truncated if they do not fit MTU
* :github:`45938` - Unable to combine USB CDC-ACM and Modbus Serial due to dependecy on uart_configure().
* :github:`45934` - ipc_service: nocopy tx buffer allocation works unexpectedly with RPMSG backend
* :github:`45933` - webusb sample 代码 链接 错误 用于 esp32 板
* :github:`45929` - up_squared：failed to run test case tests/posix/common
* :github:`45914` - 测试 tests/kernel/usage/thread_runtime_stats/ 测试 失败
* :github:`45866` - drivers/entropy: stm32: non-compliant RNG configuration on some MCUs
* :github:`45848` - tests: console harness: inaccuracy testcases report
* :github:`45846` - New ZTEST API for noisily skipping a test based dependency failures
* :github:`45845` - 测试  失败 测试 case 数量 增加 significantly 在...中 CMSIS DSP 测试 在...上 ARM 板
* :github:`45844` - Not all bytes are downloaded with HTTP request
* :github:`45842` - drivers: modem: uart_mux errors after second call to gsm_ppp_start
* :github:`45827` - bluetooth: bluetooth host: Adding the same device to resolving list
* :github:`45807` - CivetWeb doesn't build for CC3232SF
* :github:`45802` - 一些 测试 reported as PASSED 设备 但 它们  仅 构建
* :github:`45774` - drivers: gpio: pca9555: Driver is writing to output port despite all pins been configured as input
* :github:`45760` - 运行 twister 在...上 新 板 文件
* :github:`45741` - LE Audio: Allow unique ``bt_codec_qos`` for each unicast stream
* :github:`45678` - Lorawan: Devnonce  已经  使用
* :github:`45675` - testing.ztest.customized_output: mismatch twister results in json/xml file
* :github:`45666` - Building samples about BLE audio with nrf5340dk does not work
* :github:`45658` - Build failure: civetweb/http_server with target blackpill_f411ce and CONFIG_DEBUG=y
* :github:`45647` - 测试 驱动 counter: 测试 passes 甚至 当...时 不 instances  查找
* :github:`45613` - LE Audio: Setting ISO chan path and CC from BAP
* :github:`45611` - GD32 build failure: CAN_MODE_NORMAL is redefined
* :github:`45596` - samples: Code relocation nocopy sample has some unusual failure on nrf5340dk
* :github:`45581` - samples: usb: mass: Sample.usb.mass_flash_fatfs fails on non-secure nrf5340dk
* :github:`45564` - Zephyr  不 引导 带 CONFIG_PM=y
* :github:`45558` - LE Audio: Update MICP API with new naming scheme
* :github:`45532` - uart_msp432p4xx_poll_in() seems to be a blocking function
* :github:`45509` - ipc: ipc_icmsg:  silently drop 缓冲区 如果 消息  太 大
* :github:`45441` - SPI NOR driver assume all SPI controller HW is implemnted in an identical way
* :github:`45374` - 创建  unicast 分组 在...之前 两者 ISO 连接   配置  cause 问题
* :github:`45349` - ESP32: fails to chain-load sample/board/esp32/wifi_station from MCUboot
* :github:`45315` - 驱动 定时器 nrf_rtc_timer: NRF 板 取  长 时间 到 引导 application 在...中 CONFIG_TICKLESS_KERNEL=n 模式 在...之后 OTA 更新
* :github:`45304` - drivers: can: CAN interfaces are brought up with default bitrate at boot, causing error frames if bus bitrate differs
* :github:`45270` - CMake - TEST_BIG_ENDIAN
* :github:`45234` - stm32: Allow multiple GPIOs to trigger an interrupt
* :github:`45222` - drivers: peci: user space handlers not building correctly
* :github:`45169` - rcar_h3ulcb: failed to run test case tests/drivers/can/api
* :github:`45168` - rcar_h3ulcb: failed to run test case tests/drivers/can/timing
* :github:`45157` - cmake: Use of -ffreestanding disables many useful optimizations and compiler warnings
* :github:`45130` - LE Audio: Allow CSIS set sizes of 1
* :github:`45117` - drivers: clock_control: clock_control_nrf
* :github:`45114` - Sample net/sockets/echo not working with disco_l475_iot1
* :github:`45105` - ACRN: failed to run testcase tests/kernel/fifo/fifo_timeout/
* :github:`45039` - Bluetooth: Controller: Broadcast multiple BIS (broadcast ISO streams)
* :github:`45021` - Configurable SDMMC bus width for STM32
* :github:`45012` - sam_e70b_xplained: failed to run test case tests/drivers/can/timing/drivers.can.timing
* :github:`45009` - twister: 许多 测试 失败 带 "mismatch 错误 在...之后 满足  SerialException.
* :github:`45008` - esp32: i2c_read() error was returned successfully at the bus nack
* :github:`44998` - SMP shell exec 命令 causes BLE 栈 breakdown 如果 缓冲区 大小  太 小 到 保持 response
* :github:`44996` - logging: transient strings are no longer duplicated correctly
* :github:`44980` - ws2812_spi allow setting CPHA in overlay
* :github:`44944` - LE Audio: Add ISO part to broadcast audio bsim tests
* :github:`44925` - intel_adsp_cavs25: multiple tests failed after running tests/boards/intel_adsp
* :github:`44898` - mgmt/mcumgr: Fragmentation of responses may cause mcumgr to drop successfully processed response
* :github:`44861` - WiFi 支持 用于 STM32 板
* :github:`44830` - Unable to set compiler warnings on app exclusively
* :github:`44824` - mgmt/mcumgr/lib: Use slist in group registration to unify with Zephyr code
* :github:`44725` - drivers: can: stm32: can_add_rx_filter() does not respect CONFIG_CAN_MAX_FILTER
* :github:`44622` - Microbit v2 board dts file for lsm303agr int line
* :github:`44579` - MCC: Discovery cannot complete with success
* :github:`44573` - Do we have complete RNDIS stack available for STM32 controller in zephyr ?
* :github:`44466` - Zephyr misses strict aliasing disabling
* :github:`44455` - LE Audio: Remove ``struct bt_codec *codec`` parameter from ``bt_audio_broadcast_sink_sync``
* :github:`44403` - MPU fault and ``CONFIG_CMAKE_LINKER_GENERATOR``
* :github:`44400` - LE Audio: Unicast server stream control
* :github:`44340` - Bluetooth: controller: Handle parallel (across connections) CU/CPRs in refactored LLCP
* :github:`44338` - Intel CAVS: tests/subsys/logging/log_immediate/ failed due to non-intact log
* :github:`44324` - 编译 错误 在...中 byteorder.h
* :github:`44228` - drivers: modem: bg9x: bug on cmd AT+QICSGP
* :github:`44219` - mgmt/mcumgr/lib: 不正确 processing 的 img_mgmt_impl_write_image_data 离开 mcumgr 在...中 损坏 状态 在...中 case 的 错误
* :github:`44214` - mgmt/mcumgr/lib: Parasitic use of CONFIG_HEAP_MEM_POOL_SIZE in image management
* :github:`44143` - 增加 picolibc as  模块
* :github:`44071` - LE Audio: Upstream remaining parts of topic branch
* :github:`44070` - west spdx TypeError: 'NoneType' object is not iterable
* :github:`44059` - Hearing Aid Role
* :github:`44058` - Hearing Access Service API
* :github:`44005` - add strtoll and strtoull to libc minimal
* :github:`43940` - 支持 用于 CH32V307 设备
* :github:`43933` - llvm: twister: multiple errors with set but unused variables
* :github:`43928` - pm: going to PM_STATE_SOFT_OFF in pm_policy_next_state causes assert in some cases
* :github:`43913` - LE Audio: Callbacks as singletons or lists?
* :github:`43910` - civetweb/http_server - DEBUG_OPTIMIZATIONS enabled
* :github:`43887` - SystemView 跟踪 带 STM32L0x 失败 到 编译
* :github:`43859` - Bluetooth: ISO: Add sequence number and timestamp to bt_iso_chan_send
* :github:`43828` - Intel CAVS: multiple tests under tests/boards/intel_adsp/smoke are failing
* :github:`43811` - ble: gatt: db_hash_work runs for too long and makes serial communication fail
* :github:`43788` - LE Audio: Broadcast Sink shall instantiate PACS
* :github:`43767` - LE Audio: Broadcast sink/source use list of streams instead of array
* :github:`43718` - Bluetooth: bt_conn: Unable to allocate buffer within timeout
* :github:`43655` - esp32c3: Connection fail loop
* :github:`43646` - mgmt/mcumgr/lib: OS taskstat may give shorter list than expected
* :github:`43515` - reel_board: failed to run tests/kernel/workq/work randomly
* :github:`43450` - twister: 平台 名称 从 quarantine 文件  不 校验
* :github:`43435` - Bluetooth: controller: llcp: failing EBQ and Harmony tests
* :github:`43335` - Automatic Automated Backports?
* :github:`43246` - Bluetooth: Host: Deadlock with Mesh and Ext Adv on native_posix
* :github:`43245` - GitHub settings: Update topics
* :github:`43202` - LE Audio: Avoid hardcoding context type for LC3 macros
* :github:`43135` - stm32: uart: Support for wakeup from stop
* :github:`43130` - STM32WL ADC idles / doesn't work
* :github:`43124` - twister: Create pytest-based PoC for twister v2
* :github:`43115` - Data corruption in STM32 SPI driver in Slave Mode
* :github:`43103` - LwM2M 库  使用 JSON 库 用于 parsing
* :github:`42890` - Bluetooth: Controller: Periodic Advertising: AD data fragmentation
* :github:`42889` - Bluetooth: Controller: Extended Advertising: AD data fragmentation
* :github:`42885` - Bluetooth: Controller: Group auxiliary PDU transmissions
* :github:`42842` - BBRAM API is missing a documentation reference page
* :github:`42700` - Support module.yml in zephyr repo
* :github:`42684` - New LLCP handling of Preferred PHY (default tx/rx phy) needs a review
* :github:`42649` - bt_ots_client_unregister()
* :github:`42629` - stm32g0: Device hang/hard fault with AT45 + ``CONFIG_PM_DEVICE``
* :github:`42574` - i2c: No support for bus recovery imx.rt and or timeout on bus busy
* :github:`42522` - LE Audio: Immediate alert service
* :github:`42472` - ztest: 增加 支持 用于 assumptions
* :github:`42450` - cmake: dts.cmake: Add Board overlays before shields
* :github:`42420` - mgmt/mcumgr/lib: Async image erase command with status check
* :github:`42356` - Repo size - board documentation - large PNGs
* :github:`42341` - LE Audio: CSIS Ordered Access procedure use rank
* :github:`42324` - mgmt/mcumgr/lib: Move to direct use of net_buf
* :github:`42277` - Zephyr Docs on West need to be updated to include SBOM generation
* :github:`42208` - tests/subsys/logging/log_api/ fails qemu_leon3 if ptr_in_rodata() is enabled for SPARC
* :github:`42197` - Bluetooth: Controller: llcp: No disconnect if remote does not response for initiated control procedure
* :github:`42134` - TLS handshake error using DTLS on updatehub
* :github:`42102` - doc: searches for sys_reboot() are inconsistent
* :github:`41954` - Bluetooth: Controller: BIS: Event timing calculations
* :github:`41922` - Bluetooth: Controller: ISOAL: TX: Implement SDU Fragmentation into Unframed PDUs
* :github:`41880` - Strict test ordering in new ztest API
* :github:`41776` - LLVM: support -fuse-ld=lld linker on qemu_x86.
* :github:`41772` - stm32: G0: adc: Add support for VBAT internal channel
* :github:`41711` - LE Audio: CAP Acceptor Implementation
* :github:`41355` - Bluetooth: API to determine if notification over EATT is possible
* :github:`41286` - Bluetooth SDP: When the SDP attribute length is greater than SDP_MTU, the attribute is discarded
* :github:`41281` - Style Requirements Seem to Be Inconsistent with Uncrustify Configuration
* :github:`41224` - LE Audio: Telephony and Media Audio Profile (TMAP)
* :github:`41217` - LE Audio: Support for a minimum CCP client
* :github:`41214` - LE Audio: Add public API to CCP/TBS
* :github:`41211` - LE Audio: BASS support for multiple connection
* :github:`41208` - LE Audio: BASS use multi-characteristic macro for receive states
* :github:`41205` - OTS: Debug metadata output
* :github:`41204` - LE Audio: BASS read long
* :github:`41203` - LE Audio: BASS write long
* :github:`41199` - LE Audio: Media API with one call per command, rather than sending opcodes
* :github:`41197` - LE Audio: Use BT_MEDIA_PROXY values instead of BT_MCS
* :github:`41193` - LE Audio: Couple IN audio stream with an OUT audio stream
* :github:`40933` - mgmt/mcumgr/lib: Divide the lib Kconfig into sub-Kconfigs dedicated to specific mgmt cmd group
* :github:`40893` - mgmt/mcumg/lib: Encode shell command execution result in additional field of response
* :github:`40855` - mgmt/mcumgr/lib: Add optional image/slot parameter to "image erase" mcumgr request command
* :github:`40854` - mgmt/mcumgr/lib: Extend taskstat response with "runtime" statistics
* :github:`40827` - Tensorflow example not working in zephyr v2.6
* :github:`40664` - Bluetooth: GATT: EATT:  Multiple notify feature not utilize new PDU fully
* :github:`40444` - Late C++ constructor initialization on native posix boards
* :github:`40389` - Inconsistent use of CMake / environment variables
* :github:`40309` - Multi-image support for MCUboot
* :github:`40146` - 在...上  状态 的 DT-defined regions 和 MPU
* :github:`39888` - STM32L4: usb-hid: regression in hal 1.17.0
* :github:`39491` - Add a hal module for Nuclei RISC-V core (NMSIS)
* :github:`39486` - 改进 emulator APIs 用于 测试
* :github:`39347` - Static object constructors do not execute on the NATIVE_POSIX_64 target
* :github:`39153` - Improve ztest test suites (setup/teardown/before/after + OOD)
* :github:`39037` - CivetWeb samples fail to build with CONFIG_NEWLIB_LIBC
* :github:`38727` - [RFC] Add hal_gigadevice to support GigaDevice SoC Vendor
* :github:`38654` - 驱动 modem: bg9x:  不 means 到 更新 大小 的 接收 包
* :github:`38613` - BLE 连接 参数 更新 带 inconsistent 值
* :github:`38544` - drivers: wifi: esWIFI: Regression due to 35815
* :github:`38494` - Flooded logs when using CDC_ACM as back-end
* :github:`38336` - Bluetooth: Host: separate authentication callbacks for each identity
* :github:`37883` - Mesh Bluetooth Sample not working with P-NUCLEO-WB55RG
* :github:`37704` - hello world doesn't work on qemu_arc_em when CONFIG_ISR_STACK_SIZE=1048510
* :github:`37212` - improve docs with diagram for boot flow of ACRN on x86 ehl_crb
* :github:`36819` - qemu_leon3 samples/subsys/portability/cmsis_rtos_v2 samples failing
* :github:`36644` - Toolchain C++ 头文件   included 当...时 libstdc++  不 选择
* :github:`36476` - Add intel HAL support
* :github:`36084` - Arduino Nano 33 BLE: USB gets disconnected after flashing
* :github:`36026` - wolfssl / wolfcrypt
* :github:`35931` - Bluetooth: controller: Assertion in ull_master.c
* :github:`35816` - 定时器 STM32: 使用 hw 定时器 用于 counting 和 中断 callback
* :github:`35778` - pwm : STM32: Timer handling interrupt callback handling
* :github:`35762` - SAMPLES: shell_module gives no console output on qemu_leon3
* :github:`35719` - WiFi Management expects networking to be offloaded
* :github:`35512` - OpenThread can't find TRNG driver on nRF5340
* :github:`34927` - 增加 错误 检查 到 twister 如果 设置 的 平台 between platform_allow 和 integration_platforms  empty
* :github:`34600` - Bluetooth: L2CAP: Deadlock when there are no free buffers while transmitting on multiple channels
* :github:`34571` - Twister mark successfully passed tests as failed
* :github:`34438` - CivetWeb sample only supports HTTP, Zephyr lacks TLS support
* :github:`34413` - Improve __used attribute to actually keep requested function/variable
* :github:`34227` - 使用 编译 时间 resolved 设备 bindings 在...中 刷写 map, 当...时 可能
* :github:`34226` - 编译 错误 当...时 构建 civetweb samples 用于 posix_native
* :github:`34190` - Newbie: Simple C++ List App Builds for QEMU but not Native Posix Emulation
* :github:`33876` - Lora sender sample build error for esp32
* :github:`33865` - Bluetooth: iso_server security is not applied
* :github:`33725` - Modularisation and Restructuring of Documentation
* :github:`33627` - 提供 alternative nvs_init   取 const struct 设备 instead 的 设备 名称
* :github:`33520` - 更新 模块 civetweb 缺陷 fixes 和 增加 栈 大小 requirement)
* :github:`33339` - API/functions to get remaining free heap size
* :github:`33185` - TCP traffic with IPSP sample not working on 96Boards Nitrogen
* :github:`33015` - spi_nor driver: SPI_NOR_IDLE_IN_DPD breaks SPI_NOR_SFDP_RUNTIME
* :github:`32665` - Bluetooth: controller: inclusion of vendor data type and function overrides provided by vendor LLL
* :github:`32608` - Revert practice of removing devicetree labels
* :github:`32516` - RFC: 1-Wire driver
* :github:`32197` - arch_switch() on SPARC isn't quite right
* :github:`31290` - dts: arm: st: standardize pwm default property st,prescaler to 0
* :github:`31208` - Bluetooth Mesh CCM Hardware Acceleration
* :github:`31175` - STM32F1 RTC
* :github:`30694` - 一些 板 启用 non-minimal peripherals 由 默认
* :github:`30505` - Rework pipe_api test for coverage
* :github:`30365` - TCP2 does not implement Nagle algorithm
* :github:`29866` - Drivers/PCIE: read/write 8/16/32 bit word to an endpoint's configuration space
* :github:`28145` - nRF52840 Dongle cannot scan LE Coded PHY devices
* :github:`27997` - 错误 在...中 copy paste lengthy 脚本 进入 shell 控制台
* :github:`27975` - [Thingy52_nrf52832 board] - Working with other led than led0
* :github:`27735` - Enable DT-based sanity-check test filtering
* :github:`27585` - 调查 使用  中断 栈 用于  idle 线程
* :github:`27511` - coverage: qemu platforms: sanitycheck generates many ``unexpected eof`` failures when enable coverage
* :github:`27033` - Update terminology related to I2C
* :github:`26938` - gpio: api to query pin configuration
* :github:`26179` - devicetree: Missing support of unquoted strings
* :github:`25442` - Does Zephyr support USB host mode ?
* :github:`25382` - devicetree: Add ranges property support for PCIe node
* :github:`24457` - Common 跟踪 Format - 失败 到 产生 正确 跟踪 output
* :github:`24373` - NULL-pointer dereferencing in GATT when master connection fails
* :github:`23893` - server to client ble coms: two characteristics with notifications failing to notify the right characteristics at the client
* :github:`23302` - Poor TCP performance
* :github:`23165` - macOS 设置 失败 到 构建 用于 lack 的 "elftools" Python 打包
* :github:`23111` - drivers:usb:device:sam0:  Descriptor tables are filled with zeros in attach()
* :github:`23032` - Need help to enable Sub-GHz for ieee802154_cc13xx_cc26xx
* :github:`22208` - gpio: clean up debounce configuration
* :github:`22079` - 增加 reception 通道 信息 到 advertise_report
* :github:`21980` - Doesn't Install on Raspberry Pi
* :github:`21234` - drivers: usb_dc_sam0: usb detach and reattach does not work
* :github:`19979` - Implement Cortex-R floating-point support
* :github:`19244` - BLE throughput of DFU by Mcumgr is too slow
* :github:`18551` - address-of-temporary idiom not allowed in C++
* :github:`16683` - [RFC] Missing parts of libc required for CivetWeb
* :github:`16674` - Checkpatch 生成 不正确 警告 用于 __DEPRECATED_MACRO
* :github:`15591` - Add STM32 LCD-TFT Display Controller (LTDC) Driver
* :github:`15429` - shields: improve cmake to define/extract pinmux and defconfig info
* :github:`15256` - Link Layer Control Procedure overhaul
* :github:`15214` - Enforce correct compilers in boilerplate.cmake
* :github:`14527` - [wip] Generic support for out-of-tree drivers
* :github:`14068` - Allow better control on SPI pin settings
* :github:`13662` - samples/subsys/usb/cdc_acm: Stuck at "Wait for DTR"
* :github:`13639` - Use dirsync for doxygen directory syncing
* :github:`13519` - BLE Split Link Layer Improvements
* :github:`13196` - LwM2M: support Access Control objects (object id 2)
* :github:`12272` - SD/MMC 接口 支持
* :github:`12191` - Nested 中断 测试  非常 差 coverage
* :github:`11975` - Logging subsystem doesn't work with prink char_out functions
* :github:`11918` - Runtime pin configuration
* :github:`11636` - Generic GPIO reset driver
* :github:`10938` - Standardize labels (string device names) used for device binding
* :github:`10516` - 迁移 驱动 到 Devicetree
* :github:`10512` - Console, logger, shell architecure
* :github:`8945` - Explore baselibc as a replacement for minimal libc
* :github:`8497` - Need a "monitor" spin-for-ISR API
* :github:`8496` - Need a "lock" wrapper around k_sem
* :github:`8139` - Driver for BMA400 accelerometer
* :github:`7876` - net: tcp: Zero Window Probes are not supported/handled properly
* :github:`7516` - Support binary blobs / libraries and glue code in vanilla upstream Zephyr
* :github:`6498` - 内核 high-resolution 定时器 支持
* :github:`5408` - Improve docs & samples on device tree overlay
* :github:`1392` - No module named 'elftools'
* :github:`2170` - I2C fail to read GY2561 sensor when GY2561 & GY271 sensor are attached to I2C bus.
