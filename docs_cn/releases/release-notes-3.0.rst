:orphan:

.. _zephyr_3.0:

Zephyr 3.0.0
############

我们很高兴地宣布 Zephyr RTOS 版本 3.0.0 的发布。

以下各节按组件提供详细的变更列表。

安全漏洞相关
******************************

本次发布解决了以下 CVE：

更详细的信息可参见：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2021-3835：`Zephyr 项目 bug 跟踪器 GHSA-fm6v-8625-99jf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-fm6v-8625-99jf>`_

* CVE-2021-3861：`Zephyr 项目 bug 跟踪器 GHSA-hvfp-w4h8-gxvj
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hvfp-w4h8-gxvj>`_

* CVE-2021-3966：`Zephyr 项目 bug 跟踪器 GHSA-hfxq-3w6x-fv2m
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hfxq-3w6x-fv2m>`_

已知问题
************

您可以使用 GitHub 接口列出所有带有 `bug 标签
<https://github.com/zephyrproject-rtos/zephyr/issues?q=is%3Aissue+is%3Aopen+label%3Abug>`_
的 issue，从而检查所有当前已知的问题。

API 变更
***********

本次发布中的变更
=======================

* UART 异步 API 中的以下函数现在使用微秒而不是毫秒来表示
  超时：
  * :c:func:`uart_tx`
  * :c:func:`uart_rx_enable`

* 用原生 double 类型替换了自定义 LwM2M :c:struct:`float32_value` 类型。

* 新增了用于获取 USB 设备远程唤醒功能状态的函数。

* 将 ``ranges`` 和 ``dma-ranges`` 添加为无效属性，与 ``reg`` 和
  ``interrupts`` 一起与 DT_PROP_LEN() 一起使用。

* 现有的 :c:func:`crc16` 和 :c:func:`crc16_ansi` 函数已被
  修改。前者具有新的签名。后者现在正确计算
  CRC-16-ANSI 校验和。引入了一个新函数 :c:func:`crc16_reflect`
  用于计算反射 CRC。

* GATT 回调 ``bt_gatt_..._func_t`` 之前在断开连接事件时
  以参数 ``conn = NULL`` 调用。这未作为 API 的一部分
  记录。此行为已更改，使得断开连接发生时
  ``conn`` 参数正常提供。

本次发布中移除的 API
============================

* 移除了以下与无线电前端模块（FEM）相关的 Kconfig 选项：

  * ``CONFIG_BT_CTLR_GPIO_PA``
  * ``CONFIG_BT_CTLR_GPIO_PA_PIN``
  * ``CONFIG_BT_CTLR_GPIO_PA_POL_INV``
  * ``CONFIG_BT_CTLR_GPIO_PA_OFFSET``
  * ``CONFIG_BT_CTLR_GPIO_LNA``
  * ``CONFIG_BT_CTLR_GPIO_LNA_PIN``
  * ``CONFIG_BT_CTLR_GPIO_LNA_POL_INV``
  * ``CONFIG_BT_CTLR_GPIO_LNA_OFFSET``
  * ``CONFIG_BT_CTLR_FEM_NRF21540``
  * ``CONFIG_BT_CTLR_GPIO_PDN_PIN``
  * ``CONFIG_BT_CTLR_GPIO_PDN_POL_INV``
  * ``CONFIG_BT_CTLR_GPIO_CSN_PIN``
  * ``CONFIG_BT_CTLR_GPIO_CSN_POL_INV``
  * ``CONFIG_BT_CTLR_GPIO_PDN_CSN_OFFSET``

  此 FEM 配置是硬件描述，因此已移至
  :ref:`设备树 <dt-guide>`。有关在 Nordic 开源控制器上
  替代操作的更多信息，请参见 :dtcompatible:`nordic,nrf-radio`
  设备树绑定的 ``fem`` 属性。

* 移除 Kconfig 选项 ``CONFIG_USB_UART_CONSOLE``。
  选项 ``CONFIG_USB_UART_CONSOLE`` 仅在使用 CDC ACM UART 作为后端时
  与控制台驱动相关。由于 CDC ACM UART 的行为已更改
  以更紧密地模拟真实的 UART 控制器，
  该选项不再需要。

* 移除 Kconfig 选项 ``CONFIG_OPENOCD_SUPPORT``，建议改用
  ``CONFIG_DEBUG_THREAD_INFO``。

* 移除 ``flash_write_protection_set()`` 以及闪存写保护
  实现处理程序。

* 移除 ``CAN_BUS_UNKNOWN`` 并更改
  :c:func:`can_get_state` 的签名以返回错误代码。

* 移除 ``DT_CHOSEN_ZEPHYR_CANBUS_LABEL``，建议改用
  :c:macro:`DEVICE_DT_GET`。

* 移除 ``CONFIG_LOG_MINIMAL``。请改用 ``CONFIG_LOG_MODE_MINIMAL``。

* STM32 clock_control 驱动配置已从 Kconfig 移至 :ref:`设备树 <dt-guide>`。
  有关更多信息，请参见 :dtcompatible:`st,stm32-rcc` 设备树绑定。
  因此，移除了以下 Kconfig 符号：

  * ``CONFIG_CLOCK_STM32_SYSCLK_SRC_HSE``
  * ``CONFIG_CLOCK_STM32_SYSCLK_SRC_HSI``
  * ``CONFIG_CLOCK_STM32_SYSCLK_SRC_MSI``
  * ``CONFIG_CLOCK_STM32_SYSCLK_SRC_PLL``
  * ``CONFIG_CLOCK_STM32_SYSCLK_SRC_CSI``
  * ``CONFIG_CLOCK_STM32_HSE_BYPASS``
  * ``CONFIG_CLOCK_STM32_MSI_RANGE``
  * ``CONFIG_CLOCK_STM32_PLL_SRC_MSI``
  * ``CONFIG_CLOCK_STM32_PLL_SRC_HSI``
  * ``CONFIG_CLOCK_STM32_PLL_SRC_HSE``
  * ``CONFIG_CLOCK_STM32_PLL_SRC_PLL2``
  * ``CONFIG_CLOCK_STM32_PLL_SRC_CSI``
  * ``CONFIG_CLOCK_STM32_AHB_PRESCALER``
  * ``CONFIG_CLOCK_STM32_APB1_PRESCALER``
  * ``CONFIG_CLOCK_STM32_APB2_PRESCALER``
  * ``CONFIG_CLOCK_STM32_CPU1_PRESCALER``
  * ``CONFIG_CLOCK_STM32_CPU2_PRESCALER``
  * ``CONFIG_CLOCK_STM32_AHB3_PRESCALER``
  * ``CONFIG_CLOCK_STM32_AHB4_PRESCALER``
  * ``CONFIG_CLOCK_STM32_PLL_PREDIV``
  * ``CONFIG_CLOCK_STM32_PLL_PREDIV1``
  * ``CONFIG_CLOCK_STM32_PLL_MULTIPLIER``
  * ``CONFIG_CLOCK_STM32_PLL_XTPRE``
  * ``CONFIG_CLOCK_STM32_PLL_M_DIVISOR``
  * ``CONFIG_CLOCK_STM32_PLL_N_MULTIPLIER``
  * ``CONFIG_CLOCK_STM32_PLL_P_DIVISOR``
  * ``CONFIG_CLOCK_STM32_PLL_Q_DIVISOR``
  * ``CONFIG_CLOCK_STM32_PLL_R_DIVISOR``
  * ``CONFIG_CLOCK_STM32_LSE``
  * ``CONFIG_CLOCK_STM32_HSI_DIVISOR``
  * ``CONFIG_CLOCK_STM32_D1CPRE``
  * ``CONFIG_CLOCK_STM32_HPRE``
  * ``CONFIG_CLOCK_STM32_D2PPRE1``
  * ``CONFIG_CLOCK_STM32_D2PPRE2``
  * ``CONFIG_CLOCK_STM32_D1PPRE``
  * ``CONFIG_CLOCK_STM32_D3PPRE``
  * ``CONFIG_CLOCK_STM32_PLL3_ENABLE``
  * ``CONFIG_CLOCK_STM32_PLL3_M_DIVISOR``
  * ``CONFIG_CLOCK_STM32_PLL3_N_MULTIPLIER``
  * ``CONFIG_CLOCK_STM32_PLL3_P_ENABLE``
  * ``CONFIG_CLOCK_STM32_PLL3_P_DIVISOR``
  * ``CONFIG_CLOCK_STM32_PLL3_Q_ENABLE``
  * ``CONFIG_CLOCK_STM32_PLL3_Q_DIVISOR``
  * ``CONFIG_CLOCK_STM32_PLL3_R_ENABLE``
  * ``CONFIG_CLOCK_STM32_PLL3_R_DIVISOR``
  * ``CONFIG_CLOCK_STM32_PLL_DIVISOR``
  * ``CONFIG_CLOCK_STM32_MSI_PLL_MODE``

本次发布中弃用
==========================

* 移除已弃用的头文件 ``<power/reboot.h>`` 和 ``<power/power.h>``。
  应改用 ``<sys/reboot.h>`` 和 ``<pm/pm.h>``。
* :c:macro:`USBD_CFG_DATA_DEFINE` 已弃用，建议改用
  :c:macro:`USBD_DEFINE_CFG_DATA`
* :c:macro:`SYS_DEVICE_DEFINE` 已弃用，建议改用
  :c:macro:`SYS_INIT`。
* :c:func:`device_usable_check` 已弃用，建议改用
  :c:func:`device_is_ready`。
* 自定义 CAN 返回码（:c:macro:`CAN_TX_OK`、:c:macro:`CAN_TX_ERR`、
  :c:macro:`CAN_TX_ARB_LOST`、:c:macro:`CAN_TX_BUS_OFF`、
  :c:macro:`CAN_TX_UNKNOWN`、:c:macro:`CAN_TX_EINVAL`、
  :c:macro:`CAN_NO_FREE_FILTER` 和 :c:macro:`CAN_TIMEOUT`）已弃用，
  建议改用标准 errno 错误代码。
* :c:func:`can_configure` 已弃用，建议改用
  :c:func:`can_set_bitrate` 和 :c:func:`can_set_mode`。
* :c:func:`can_attach_workq` 已弃用，建议改用
  :c:func:`can_add_rx_filter_msgq` 和 :c:func:`k_work_poll_submit`。
* :c:func:`can_attach_isr` 已弃用，替换为
  :c:func:`can_add_rx_filter`。
* :c:macro:`CAN_DEFINE_MSGQ` 已弃用，替换为
  :c:macro:`CAN_MSGQ_DEFINE`。
* :c:func:`can_attach_msgq` 已弃用，替换为
  :c:func:`can_add_rx_filter_msgq`。
* :c:func:`can_detach` 已弃用，替换为
  :c:func:`can_remove_rx_filter`。
* :c:func:`can_register_state_change_isr` 已弃用，替换为
  :c:func:`can_set_state_change_callback`。
* :c:func:`can_write` 已弃用，建议改用 :c:func:`can_send`。

本次发布中的稳定 API 变更
==================================

本次发布中的新 API
========================

* 串行

  * 新增支持 8 位以上数据位的 API。

    * 新增 :kconfig:option:`CONFIG_UART_WIDE_DATA` 以启用这些新 API。

    * 新增以下函数，镜像 8 位数据的类似函数：

      * :c:func:`uart_tx_u16` 用于从缓冲区发送给定数量的数据。

      * :c:func:`uart_rx_enable_u16` 用于开始接收数据。

      * :c:func:`uart_rx_buf_rsp_u16` 用于设置接收缓冲区
        作为 ``UART_RX_BUF_REQUEST`` 事件的响应。

      * :c:func:`uart_poll_in_u16` 用于轮询输入。

      * :c:func:`uart_poll_out_u16` 用于以轮询模式输出数据。

      * :c:func:`uart_fifo_fill_u16` 用于用数据填充 FIFO。

      * :c:func:`uart_fifo_read_u16` 用于从 FIFO 读取数据。

* 设备树

  * 新增设备树辅助函数：

    * :c:macro:`DT_INST_ENUM_IDX`
    * :c:macro:`DT_INST_ENUM_IDX_OR`
    * :c:macro:`DT_INST_PARENT`

  * 新的 :ref:`devicetree-ranges-property` API

  * 移除：``DT_CHOSEN_ZEPHYR_CANBUS_LABEL``；请改用
    ``DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus))`` 获取设备，
    并在需要时从设备结构体读取名称。

  * 移除已弃用的宏：

    * ``DT_CLOCKS_LABEL_BY_IDX``
    * ``DT_CLOCKS_LABEL``
    * ``DT_INST_CLOCKS_LABEL_BY_IDX``
    * ``DT_INST_CLOCKS_LABEL_BY_NAME``
    * ``DT_INST_CLOCKS_LABEL``
    * ``DT_PWMS_LABEL_BY_IDX``
    * ``DT_PWMS_LABEL_BY_NAME``
    * ``DT_PWMS_LABEL``
    * ``DT_INST_PWMS_LABEL_BY_IDX``
    * ``DT_INST_PWMS_LABEL_BY_NAME``
    * ``DT_INST_PWMS_LABEL``
    * ``DT_IO_CHANNELS_LABEL_BY_IDX``
    * ``DT_IO_CHANNELS_LABEL_BY_NAME``
    * ``DT_IO_CHANNELS_LABEL``
    * ``DT_INST_IO_CHANNELS_LABEL_BY_IDX``
    * ``DT_INST_IO_CHANNELS_LABEL_BY_NAME``
    * ``DT_INST_IO_CHANNELS_LABEL``
    * ``DT_DMAS_LABEL_BY_IDX``
    * ``DT_INST_DMAS_LABEL_BY_IDX``
    * ``DT_DMAS_LABEL_BY_NAME``
    * ``DT_INST_DMAS_LABEL_BY_NAME``
    * ``DT_ENUM_TOKEN``
    * ``DT_ENUM_UPPER_TOKEN``


* CAN

  * 新增 :c:func:`can_get_max_filters` 用于获取 CAN 控制器设备
    支持的最大 RX 滤波器数量。

内核
******

  * 新增对事件对象的支持。线程可以等待事件对象，
    使得发布到该事件对象的任何事件在满足等待线程的事件条件时
    可以唤醒等待线程。
  * 扩展 CPU 运行时统计以跟踪当前、总计、峰值和平均使用率
    （受空闲线程调度的限制）。这允许开发者
    在需要调优系统时获取更多系统信息。
  * 新增用于线程运行时周期监控的 "thread_usage" API。
  * 修复配置了 SYSTEM_CLOCK_SLOPPY_IDLE 时的超时问题。

架构
*************

* ARM

  * AARCH32

    * 将内联汇编调用转换为使用 CMSIS 提供的函数
      :c:func:`arm_core_mpu_enable` 和 :c:func:`arm_core_mpu_disable`。
    * 用 `CONFIG_ARMV7_R` 替换 Kconfig `CONFIG_CPU_CORTEX_R` 以启用
      v7 和 v8 Cortex-R 之间的区分。
    * 更新 Cortex-R 系统调用行为以匹配 Cortex-M。

  * AARCH64

    * 修复启用大量 IRQ 时的越界错误，并忽略
      1020 到 1023 之间的特殊 INTD
    * 为 ARMv8R 新增 MPU 代码
    * 各种 MMU 修复
    * 新增 nocache 内存段支持
    * 为 ARM64 新增 Xen 超调用接口
    * 修复 SMP 调度代码中的竞态条件。

* Xtensa

  * 引入一种机制来自动确定哪些 scratch 寄存器
    用于内部代码，而不是硬编码。这是为了适应
    架构的可配置性，其中某些寄存器可能存在于
    一个 SoC 但不存在于另一个 SoC。

  * 为 Xtensa 新增 coredump 支持。

  * 为 Xtensa 新增 GDB stub 支持。

蓝牙
*********

* 将蓝牙中所有实验性功能更新为使用新的 ``EXPERIMENTAL``
  可选择的 Kconfig 选项
* 蓝牙现在与树的其他部分一样使用 logging v2

* 音频

  * 实现了 Content Control ID 模块（CCID）
  * 新增对 Coordinated Set Identification Service（CSIS）的支持
  * 新增临时对象传输客户端实现
  * 新增媒体控制客户端实现
  * 新增媒体控制服务器实现
  * 实现了 Media Proxy API
  * 实现了 CIG 重配置和状态处理
  * 更新了服务器和客户端的 CSIS API
  * 新增 Basic Audio Profile（BAP）单播和广播服务器支持

* 方向查找

  * 新增对按 CTE 类型过滤周期性广播同步的支持
  * 新增周期性广播同步建立的额外处理逻辑
  * 在 DF 连接模式下新增 CTE RX、采样和 IQ 报告处理
  * 新增连接模式下的 CTE 配置支持
  * 方向查找连接模式现在使用新重构的 LLCP
    实现

* 主机

  * :kconfig:option:`CONFIG_BT_SETTINGS_CCC_STORE_ON_WRITE` 现在默认
    启用。在写入后立即存储 CCC 降低了
    绑定对端之间 CCC 值不一致的风险
  * 新增对 L2CAP 通道重配置的支持。
  * 新增对 SMP 错误代码 0xF 的支持，其中对端拒绝分布式
    密钥
  * 新增 ``bt_gatt_service_is_registered()`` 用于验证服务注册
  * 在对象传输服务
    实现中新增创建和删除过程
  * 新增对重组扩展广播报告的支持
  * 新增对重组周期性广播报告的支持
  * 新增对设置长周期性广播数据的支持
  * 在转发到应用之前实现了 GATT 长写入重组
  * 已更正 GATT 服务器 DB 哈希计算逻辑
  * 新增在配对完成时存储 CCC 数据

* Mesh

  * 拆分 Proxy 服务，现在可以将其编译排除
  * 新增在每次重传时回调的选项
  * 新增对多个广播集的支持
  * 重构 Config Client 和 Health Client API 以允许异步使用

* 控制器

  * 新增对全新的 LL Control Procedures
    （LLCP）实现的支持，当前默认禁用，可以使用
    ``CONFIG_BT_LL_SW_LLCP_IMPL`` Kconfig 选择启用
  * 新增对广播等时组（BIG）的初步支持
  * 集成 ISO 同步 RX 数据路径
  * 将 FEM 配置（PA/LNA）从 Kconfig 迁移到设备树
  * 将支持的蓝牙 HCI 版本更新到 5.3
  * 新增对周期性广播器列表的支持
  * 新增对周期性广播同步接收启用的支持
  * 新增对扩展扫描的过滤访问列表过滤的支持
  * 新增对广播扩展动态 TX 功率控制的支持
  * 新增扩展广播报告中直接地址类型的处理
  * 实现了辅助 PDU 设备地址匹配
  * 实现了扩展广播报告通过 HCI 的分片
  * 实现了扩展广播和扫描报告的背靠背链接
  * 实现了周期性广播 ADI 支持，包括重复过滤
  * 引入了新的首选中心连接间隔特性


* HCI 驱动

  * 新增对新的可选 ``setup()`` 函数的支持，用于启动控制器
    所需的供应商特定设置代码
  * 修复 DTM 模式未通过 HCI 复位命令正确复位的问题
  * 将最大 ACL TX 缓冲区大小限制为 251 字节

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

USB
***


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

  * 新增 IPC 服务支持和具有静态 VRING 后端的 RPMsg

HAL
****

* STM32

  * stm32cube/stm32wb 及其库：升级到版本 V1.12.1
  * stm32cube/stm32mp1：升级到版本 V1.5.0
  * stm32cube/stm32u5：升级到版本 V1.0.2

* 新增 `GigaDevice HAL 模块
  <https://github.com/zephyrproject-rtos/hal_gigadevice>`_

MCUBoot
*******

* 修复了 nrf5340 上串行恢复的跳过问题。
* 修复了一个问题，该问题导致渐进擦除功能关闭，尽管
  通过 Kconfig 选择了它（由 #42c985cead 引入）。
* 在传入映像验证阶段新增对复位地址的检查，参见
  ``CONFIG_MCUBOOT_VERIFY_IMG_ADDRESS``。
* 允许加密映像的映像头大于 1 KB。
* 支持 Mbed TLS 3.0。
* stm32：看门狗支持。
* 许多文档改进。
* 修复了 Kconfig 中 cryptolib 选择器的死锁。
* 修复了带串行恢复的单应用槽支持。
* 新增各种钩子以能够更改映像数据的访问方式，参见
  ``CONFIG_BOOT_IMAGE_ACCESS_HOOKS``。
* 在串行恢复中新增对自定义命令的支持（PERUSER_MGMT_GROUP）：存储
  擦除 ``CONFIG_BOOT_MGMT_CUSTOM_STORAGE_ERASE``、自定义映像状态
  ``CONFIG_BOOT_MGMT_CUSTOM_IMG_LIST``。
* 在串行恢复中新增对直接映像上传的支持，参见
  ``CONFIG_MCUBOOT_SERIAL_DIRECT_IMAGE_UPLOAD``。

Trusted Firmware-m
******************

* 将 TF-M 更新到 1.5.0 发布版本，并附带一些额外挑选的
  提交。

文档
*************

* Doxygen HTML 页面使用新主题。它基于
  `doxygen-awesome-css <https://github.com/jothepro/doxygen-awesome-css>`_
  主题。

测试与示例
*****************

* 驱动：clock_control：为 stm32（u5、h7）新增测试套件。

Issue 相关条目
*******************
* :github:`41095` - libc: newlib: 'gettimeofday' causes stack overflow on non-POSIX builds
* :github:`41093` - Kconfig.defconfig:11: error: couldn't parse 'default $(dt_node_int_prop_int,/cpus/cpu@0,clock-frequency)'
* :github:`41077` - 控制台 gsm_mux:  不 发送 更多 than 128 bytes 的 数据 在...上 dlci
* :github:`41074` - can_mcan_send sends corrupted CAN frames with a byte-by-byte memcpy implementation
* :github:`41066` - twister --generate-map is broken
* :github:`41062` - kernel: userspace: Potential misaligned access
* :github:`41058` - stm32h723 : application gets hung during spi_transceive() operation
* :github:`41052` - tests-ci : portability: posix: fs.tls.newlib test Build failure
* :github:`41050` - MCUMgr Sample 失败 到 构建
* :github:`41043` - Sporadic Bus Fault when using I2C on a nrf52840
* :github:`41026` - LoRa: sx126x: DIO1 interrupt left enabled in sleep mode
* :github:`41024` - SPI Loopback test fails to build on iMX RT EVKs
* :github:`41017` - USB string descriptors can be re-ordered causing corruption and out-of-bounds-write
* :github:`41016` - i2c_sam0.c i2c_sam0_transfer operations do not execute a STOP
* :github:`41012` - irq_enable() doesn’t support enabling NVIC IRQ number more than 127
* :github:`40999` - Unable to boot smp_svr sample image as documentation suggests, or sign
* :github:`40974` - Xtensa High priority interrupts cannot be masked during initialization
* :github:`40965` - Halt on receipt of Google Cloud IoT Core MQTT message sized 648+ bytes
* :github:`40946` - Xtensa Interrupt nesting issue
* :github:`40942` - Xtensa 调试 缺陷
* :github:`40936` - STM32 ADC gets stuck in Calibration
* :github:`40925` - mesh_badge not working reel_board_v2
* :github:`40917` - twister --export-tests export all cases even this case can not run on given platform
* :github:`40916` - Assertion in nordic's BLE controller lll.c:352
* :github:`40903` - documentation generation fails on function typedefs
* :github:`40889` - samples: samples/kernel/metairq_dispatch failed on acrn_ehl_crb
* :github:`40888` - samples:    samples/subsys/portability/cmsis_rtos_v1/philosophers failed on ehl crb
* :github:`40887` - 测试 调试 测试 case subsys/debug/coredump 失败 在...上 acrn_ehl_crb
* :github:`40883` - Limitation 在...上 日志记录 模块
* :github:`40881` - Bluetooth: shell: fatal error because ctx_shell is NULL
* :github:`40873` - qemu_cortex_r5: fail to handle user_string_alloc_copy() with null parameter
* :github:`40870` - 测试 syscall: 失败 到 构建 在...上 fvp_baser_aemv8r_smp
* :github:`40866` - Undefined behavior in lib/os/cbprintf_packaged.c: subtraction involving definitely null pointer
* :github:`40838` - Nordic UART 驱动 (UARTE) 失败 到 transfer 缓冲区 从 读取 仅 内存
* :github:`40827` - Tensorflow example not working in zephyr v2.6
* :github:`40825` - STM32WB55RGV6: No output after west flash
* :github:`40820` - coap: blockwise: context 当前  不 匹配 total 大小 在...之后 transfer  完成
* :github:`40808` - Invalid CMake warning related to rimage
* :github:`40795` - Timer signal thread execution loop break SMP on ARM64
* :github:`40783` - samples/subsys/usb/dfu  should filter on FLASH driver
* :github:`40776` - HCI_USB with nRF52840 dongle disconnect after 30 s
* :github:`40775` - stm32: multi-threading broken after #40173
* :github:`40770` - tests/subsys/cpp/libcxx/cpp.libcxx.newlib fails on m2gl025_miv and qemu_cortex_m0
* :github:`40761` - Bluetooth: host: Wait for the response callback before clearing Service Changed data
* :github:`40759` - Bluetooth: host: Improper restore of CCC values and handling Service Change indication when bonded peer reconnects
* :github:`40758` - Bluetooth: host: CCC values are not immediately stored on GATT Server by default (risk of inconsistency)
* :github:`40744` - RT600 LittleFS Sample 产生 构建 警告 在...中 默认 配置
* :github:`40740` - 测试 日志记录 测试 case log_msg2.logging.log_msg2_64b_timestamp 失败 在...上 qemu_cortex_a9
* :github:`40724` - 测试 日志记录 日志记录 测试 cases 失败 在...中 multiple 板
* :github:`40717` - twister: failure in parsing code coverage file
* :github:`40714` - west flash, Invalid DFU suffix signature
* :github:`40688` - 在...中 "pinmux_stm32.c" 函数 "stm32_dt_pinctrl_remap" 不 工作
* :github:`40672` - EDTT: buffer overflow in edtt_hci_app
* :github:`40668` - 问题 带 twister 代码 coverage 测试 不 工作 带 minimal C 库 (nRF52840)
* :github:`40663` - WWDG not supported on STM32H7 family
* :github:`40658` - shtcx not reporting correct humidity value
* :github:`40646` - Can't read more than one OUTPUT|INPUT gpio pin in gpio_emul
* :github:`40643` - intel_adsp_cavs15:  zephyr_pre0.elf  相当 大 (530MB) 在...上 ADSP 用于 一些 测试 cases
* :github:`40640` - drivers: usb_dc_native_posix: segfault when using composite USB device
* :github:`40638` - drivers: usb_dc_mcux: processing endpoint callbacks in ISR context causes assertion
* :github:`40633` - CI documentation 构建 挂起 当...时 there   损坏 reference
* :github:`40624` - twister: coverage: Using --coverage flag for on-target test make tests last until time limit
* :github:`40622` - Dark mode readability problem in Unit Test Documentation
* :github:`40621` - npcx uart driver uses device PM callback to block suspension
* :github:`40614` - poll: the code judgment condition is always true
* :github:`40590` - gen_app_partitions scans object files unrelated to current image
* :github:`40586` - 测试 日志记录 Logging.add.user scenario 失败 在...上 所有 nrf 板
* :github:`40578` - MODBUS RS-485 transceiver support broken on several platforms due to DE race condition
* :github:`40569` - bisected: kernel.common.stack_protection_arm_fpu_sharing fails on mps3_an547
* :github:`40546` - Bluetooh:host: GATT notify multiple feature not working properly
* :github:`40538` - mcuboot build fails with nrf52 internal RC oscillator
* :github:`40517` - msgq: NULL handler assertion with data cache enabled
* :github:`40483` - ESP32: display sample over i2c not working
* :github:`40464` - Dereferencing NULL with getsockname() on TI Simplelink Platform
* :github:`40456` - Bluetooth: L2CAP tester application is missing preprocessor flags for ECFC function call
* :github:`40453` - LittleFS fails when block count is greater than block size
* :github:`40450` - Twister map file shows baud in quotes but should not be in quotes
* :github:`40449` - Twister 测试 失败 当...时 运行 在...上 actual 硬件 due 到 已弃用 命令 警告
* :github:`40439` - Undefined escape sequence: ill-formed for the C standard
* :github:`40438` - Ill-formed sources due to external linkage inline functions calling static functions
* :github:`40433` - RTT 失败 到 工作 在...中 program 带 大 global 变量
* :github:`40420` - Lower-case characters in Kconfig symbol names cause obscure errors
* :github:`40411` - Xtensa xcc compile build fails with SOF application on latest Zephyr main
* :github:`40376` - HiFIve1 失败 到 运行 tests/kernel/workq/work/
* :github:`40374` - up_squared: isr_dynamic 测试  失败
* :github:`40369` - tests/subsys/logging/log_core/ and tests/subsys/shell/shell/ hang on qemu_cortex_a53 and qemu_riscv64
* :github:`40367` - sample: cycle_64 is failing out due to a timeout on 64-bit versions of qemu_x86 and ehl_crb
* :github:`40348` - STM32L496 Uart rx interrupt callback fails to work with LVGL
* :github:`40329` - nucleo_g0b1re: FDCAN message RAM write fails on byte-oriented write
* :github:`40317` - Crash in ull.c when stressing periodic advertising sync (scanner side)
* :github:`40316` - Error undefined reference to '__aeabi_uldivmod' when build with Zephyr 2.7.0 for STM32
* :github:`40298` - Bluetooth assertions in lll_conn.c
* :github:`40290` - CAN_STM32: 构建 错误 带 CONFIG_CAN_AUTO_BUS_OFF_RECOVERY=n
* :github:`40256` - websocket: the size of a websocket payload is limited
* :github:`40254` - TF-M: BL2 signing is broken due to incompatible MCUboot version
* :github:`40244` - [v2.7-branch] hci_spi sample cannot be built for nrf51dk_nrf51422 and 96b_carbon_nrf51
* :github:`40236` - Unsigned int can't be used in condition compare with int
* :github:`40215` - RSSI in periodic adv. callbacks always -127 (sync_recv and cte_report_cb)
* :github:`40209` - Bluetooth: 第一 AUX_SYNC_IND 从不 接收 缺失 event 发送 到 host
* :github:`40202` - Bluetooth: Periodic advertising synchronization not re-established after advertiser reset without scan disable
* :github:`40198` - shell 模块 doesn't 工作 在...上 主 branch 用于 esp32 板
* :github:`40189` - k_poll infrastructure can miss "signals" in a heavily contended SMP system
* :github:`40169` - 驱动  net: compilation 损坏 和 不 测试 cases 在...中 CI
* :github:`40159` - Bluetooth Mesh branch incorrect return value
* :github:`40153` - mimxrt1050_evk: 失败 到 运行 samples/subsys/task_wdt
* :github:`40152` - task_wdt  get stuck 在...中  loop 在...处 硬件 复位  从不 fired
* :github:`40133` - mimxrt1060-evk flash shell command causes shell deadlock
* :github:`40129` - 'tests/net/socket/tls/net.socket.tls.preempt' fails with 'qemu_cortex_a9'
* :github:`40124` - 构建 失败 带 'CONFIG_SHELL_VT100_COMMANDS=n'
* :github:`40119` - OBJECT_TRACING for kernel objects
* :github:`40115` - logging: int-uint comparsion causes false assert & epic hang
* :github:`40107` - lwm2m: if network drops during firmware update, lock occurs
* :github:`40077` - driver: wdt: twrke18f: test_wdt fails
* :github:`40076` - 驱动 led pca9633  仅 使用 第一 设备 在...中 devicetree
* :github:`40074` - sara-r4: socket call fails due to regression
* :github:`40070` - canbus: isotp: Violations of k_fifo and net_buf API usage
* :github:`40069` - Bluetooth CCM encryption bug in MIC generation
* :github:`40068` - Test suite subsys.pm.device_runtime_api fail on qemu_x86_64
* :github:`40030` - STM32 SD hardware flow control gets disabled if disk_access_init is used
* :github:`40021` - mimxrt1060_evk_hyperflash 板 定义  损坏
* :github:`40020` - tests: kernel: mem_slab: mslab_api: undefined reference to z_impl_k_sem_give and z_impl_k_sem_take
* :github:`40007` - twister: cannot build samples/tests on Windows
* :github:`40003` - Bluetooth: host: zephyr writes to disconnected device and triggers a bus fault
* :github:`40000` - k_timer timeout handler is called with interrupts locked
* :github:`39989` - Zephyr  不 persist CCC 数据 写入 在...之前 bonding 当...时 bonding  完成 哪个 leads 到 loss 的 subscriptions 在...上 设备 复位
* :github:`39985` - Telnet shell breaks upon sending Ctrl+C character
* :github:`39978` - logging.log2_api_deferred and logging.msg2 tests fail on qemu_cortex_a9
* :github:`39973` - Bluetooth: hci_usb example returning "Unknown HCI Command" after reset.
* :github:`39969` - USB 不 automatically 启用 当...时 USB_UART_CONSOLE  设置
* :github:`39968` - samples: tfm_integration: tfm_psa_test broken on OS X (Windows?)
* :github:`39947` - open-amp problem with dcache
* :github:`39942` - usdhc disk_usdhc_access_write busy fail
* :github:`39923` - qspi_sfdp_read fails errata work around
* :github:`39919` - CONFIG_ISM330DHCX cannot compile due to missing file
* :github:`39904` - bl654_usb does not work with hci_usb sample application
* :github:`39900` - usb bug :USB device descriptor could not be obtained   on windows10
* :github:`39893` - Bluetooth: hci usb: scan duplicate filter not working
* :github:`39883` - BLE 栈 overlow due 到  默认 选项 值 当...时 编译 带 不 optimization
* :github:`39874` - [Coverity CID: 240214] Dereference before null check in drivers/dma/dma_mcux_edma.c
* :github:`39872` - [Coverity CID: 240218] Dereference after null check in subsys/bluetooth/controller/ll_sw/ull_scan_aux.c
* :github:`39870` - [Coverity CID: 240220] Argument cannot be negative in tests/net/socket/af_packet_ipproto_raw/src/main.c
* :github:`39869` - [Coverity CID: 240221] Unchecked return value from library in drivers/usb/device/usb_dc_native_posix.c
* :github:`39868` - [Coverity CID: 240222] Dereference before null check in drivers/dma/dma_mcux_edma.c
* :github:`39857` - [Coverity CID: 240234] Uninitialized scalar variable in subsys/bluetooth/shell/iso.c
* :github:`39856` - [Coverity CID: 240235] Explicit null dereferenced in subsys/bluetooth/controller/ll_sw/ull_scan_aux.c
* :github:`39852` - [Coverity CID: 240241] Out-of-bounds access in subsys/bluetooth/host/adv.c
* :github:`39851` - [Coverity CID: 240242] Dereference after null check in tests/bluetooth/tester/src/l2cap.c
* :github:`39849` - [Coverity CID: 240244] Untrusted value as argument in drivers/usb/device/usb_dc_native_posix.c
* :github:`39844` - [Coverity CID: 240658] Argument cannot be negative in tests/net/lib/dns_sd/src/main.c
* :github:`39843` - [Coverity CID: 240659] Out-of-bounds read in /zephyr/include/generated/syscalls/kernel.h (Generated Code)
* :github:`39841` - [Coverity CID: 240661] Unchecked return value in tests/net/net_pkt/src/main.c
* :github:`39840` - [Coverity CID: 240662] Improper use of negative value in subsys/mgmt/osdp/src/osdp.c
* :github:`39839` - [Coverity CID: 240663] Out-of-bounds access in tests/benchmarks/mbedtls/src/benchmark.c
* :github:`39835` - [Coverity CID: 240667] Improper use of negative value in samples/subsys/usb/cdc_acm_composite/src/main.c
* :github:`39833` - [Coverity CID: 240670] Out-of-bounds access in tests/net/lib/dns_sd/src/main.c
* :github:`39832` - [Coverity CID: 240671] Out-of-bounds access in drivers/flash/flash_mcux_flexspi_hyperflash.c
* :github:`39830` - [Coverity CID: 240673] Out-of-bounds read in /zephyr/include/generated/syscalls/kernel.h (Generated Code)
* :github:`39827` - [Coverity CID: 240676] Out-of-bounds access in drivers/ieee802154/ieee802154_dw1000.c
* :github:`39825` - [Coverity CID: 240678] Unchecked return value in drivers/ieee802154/ieee802154_cc1200.c
* :github:`39824` - [Coverity CID: 240679] Out-of-bounds access in samples/subsys/usb/cdc_acm_composite/src/main.c
* :github:`39823` - [Coverity CID: 240681] Improper use of negative value in drivers/bluetooth/hci/h4.c
* :github:`39817` - drivers: pwm: nxp: (potentially) Incorrect return value on API function
* :github:`39815` - [Coverity CID: 240688] Out-of-bounds access in tests/net/lib/dns_sd/src/main.c
* :github:`39813` - [Coverity CID: 240691] Out-of-bounds access in tests/benchmarks/mbedtls/src/benchmark.c
* :github:`39812` - [Coverity CID: 240692] Unintended sign extension in subsys/stats/stats.c
* :github:`39810` - [Coverity CID: 240696] Operands don't affect result in subsys/net/lib/lwm2m/lwm2m_util.c
* :github:`39809` - [Coverity CID: 240697] Out-of-bounds access in samples/subsys/usb/cdc_acm/src/main.c
* :github:`39807` - [Coverity CID: 240699] Out-of-bounds access in tests/bluetooth/tester/src/l2cap.c
* :github:`39806` - [Coverity CID: 240700] Unchecked return value in drivers/ieee802154/ieee802154_cc2520.c
* :github:`39805` - [Coverity CID: 240703] Improper use of negative value in drivers/bluetooth/hci/h4.c
* :github:`39797` - STM32 G4 series compile error when both ADC1 and ADC2 are opened
* :github:`39780` - On ESP32S2 platform zsock_getaddrinfo() call causes RTOS to crash
* :github:`39774` - modem: uart mux reading optimization never used
* :github:`39758` - 构建  损坏 如果 LWM2M_CANCEL_OBSERVE_BY_PATH 配置  设置
* :github:`39756` - kconfig: choice default is not set if hidden under invisible menu
* :github:`39726` - 如何 到 使用 PWM LED 驱动 用于 ESP32?
* :github:`39721` - bq274xx sensor - Fails to compile when CONFIG_PM_DEVICE enabled
* :github:`39720` -  XCC BUILD FAIL :K_MEM_SLAB_DEFINE && K_HEAP_DEFINE
* :github:`39718` - STM32L496G_DISCO uart 测试 失败 在...上 single 缓冲区 读取
* :github:`39712` - bq274xx sensor - Fails to compile when CONFIG_PM_DEVICE enabled
* :github:`39707` - Can't enable CONFIG_SHELL_LOG_BACKEND Log Shell Menus with pure Telnet Shell Backend
* :github:`39705` - Canot use POSIX_API and NET_SOCKETS together
* :github:`39704` - Using OpenThread makes the system unresponsive after 49.7 days
* :github:`39703` - stm32 uart testing fails on test_read_abort
* :github:`39687` - sensor: qdec_nrfx: PM callback has incorrect signature
* :github:`39675` - list_boards.py script doesn't properly traverse external board roots
* :github:`39672` - net_config_init count calculation appears incorrect.
* :github:`39660` - poll() not notified when a TLS/TCP connection is closed without TLS close_notify
* :github:`39655` - Linker error with CONFIG_NET_TCP=y
* :github:`39645` - STM32L496 Zephyr using LVGL disp_drv.flush_cb can not work
* :github:`39629` - 小 Compiler 警告 在...中 subsys/fs/shell.c:381:23 在...中 最新 发布 need 参数 更改 仅
* :github:`39627` - samples: http_get: cannot run on QEMU
* :github:`39624` - Bluetooth: Submitting more GATT writes than available buffers blocks for 30s and then errors out
* :github:`39619` - twister: integration_platforms getting unnoticeably skipped when --subset is used
* :github:`39609` - spi: slave: division by zero in timeout calculation
* :github:`39601` - 在...上 ESP32S2 平台 GPIO 中断 causes RTOS 到 挂起 当...时 配置 到 GPIO_INT_EDGE_BOTH
* :github:`39594` - Possible bug or undocumented behaviour of spi_write
* :github:`39588` - drivers: i2c: nrf: i2c error with burst write
* :github:`39575` - k_mutex_lock and k_sem_take with K_FOREVER return -EAGAIN value
* :github:`39569` - [ESP32] 崩溃 当...时 trying 到 设置  低 CPU 时钟 frequency
* :github:`39549` - Bluetooth: Incomplete Delayed Initialization of acl_mtu Allows Controller to Crash Host Layer
* :github:`39546` - mcumgr over serial does not add CRC to length of packet len
* :github:`39541` - can: mcux_flexcan: wrong timing calculation
* :github:`39538` - logging: rtt: Compilation fails when CONFIG_LOG_BACKEND_RTT_MODE_OVERWRITE=y and CONFIG_MULTITHREADING=n
* :github:`39523` - task watchdog crash/asset on NRF52840 - need to reorder task_wdt_feed() in task_wdt_add()
* :github:`39516` - function net_eth_vlan_enable does not properly validate vlan tag value
* :github:`39506` - Bluetooth: crash in att.c when repeatedly scanning/connecting/disconnecting
* :github:`39505` - question: ethernet: carrier_on_off
* :github:`39503` - Zephyr boot banner not updated on rebuild with opdated SHA
* :github:`39497` - doc: kernel: event object static initialization mismatch
* :github:`39487` - esp32 IRQ01 stack utilisation is 100%
* :github:`39483` - LSM6DS0 Gyroscope rad/s Calculation Error
* :github:`39463` - ESP32 GPIO intterupt
* :github:`39461` - Bluetooth: hci acl flow control: bugs of bluetooth hci ACL flow control
* :github:`39457` - mec15xxevb_assy6853: metairq_dispatch sample is failing due to timeout while monitoring serial output
* :github:`39438` - Scanning 用于 设备 发送 periodic advertisements 停止 工作 在...之后  在...期间 但 保持 reporting none periodic.
* :github:`39423` - mcuboot not upgrade  for stm32l1 series
* :github:`39418` - 测试 运行 testcase 失败 在...上 平台 mps2_an521_ns
* :github:`39416` - west debug throws error
* :github:`39405` - CTE report callback have the wrong pointer to bt_le_per_adv_sync
* :github:`39400` - stm32f103 example servo_motor don't work
* :github:`39399` - linker: Missing align __itcm_load_start / __dtcm_data_load_start linker symbols
* :github:`39392` - ARC nsim_sem fail on tests/crypto/tinycrypt_hmac_prng test when use ARCMWDT toolchain
* :github:`39340` - shell FS sample 停止 带  usage 故障 错误
* :github:`39311` - SPDX --init fails on windows systems
* :github:`39300` - Library globals in .sdata/.sbss sections doesn't put into memory partition in userspace
* :github:`39293` - Can not run normally on MIMXRT1061CVL5A SOC
* :github:`39269` - Fail to initialize BLE stack with optimization level zero
* :github:`39253` - modem: hl7800: IPv6 socket not created properly
* :github:`39242` - net: sockets: Zephyr Fatal in dns_resolve_cb if dns request was attempted in offline state
* :github:`39221` - Errors when debuging application in Eclipse using STM32L496G-DISCO
* :github:`39216` - Twister: Broken on NRF52840 with pyocd option timeout error
* :github:`39179` - twister: --generate-hardware-map ends up in RuntimeError
* :github:`39144` - gsm_ppp: stop & starting not working as expected with nullpointer dereference & no full modem init
* :github:`39136` - SD disk access runs into TXUNDERRUN and RXOVERRUN of SDMMC driver
* :github:`39131` - GATT DB hash calculation is wrong on characteristic declarations using 128-bit UUIDs.
* :github:`39096` - DNS responders assume interfaces are up at initialization
* :github:`39024` - drivers: sensors: FXOS8700: Interrupt pin routing configuration must be changed in standby power mode
* :github:`38988` - MCP2515 driver CS gpio active high support issue
* :github:`38987` - Unable to build ESP32 example code using west tool - zephyr
* :github:`38954` - Can't get FlexPWM working for imxrt1060
* :github:`38631` - printk to console fails for freescale kinetis 8.2.0 (Zephyr 2.6.0) on FRDM-K64F
* :github:`38624` - mcuboot gets the wrong value of DT_FIXED_PARTITION_ID
* :github:`38606` - drivers: adc: stm32h7: Oversampling Ratio set incorrectly
* :github:`38598` - net_context_put will not properly close TCP connection (might lead to tcp connection leak)
* :github:`38576` - net shell self-connecting 到 TCP  lead 到  崩溃
* :github:`38502` - 更新 mcumgr 库 到 fix 错误 callback 状态
* :github:`38446` - intel_adsp_cavs15: Fail to get testcases output on ADSP
* :github:`38376` - Raw Socket Failure when using 2 Raw Sockets and zsock_select() statement - improper mapping from sock to handlers
* :github:`38303` -  当前 BabbleSim 测试 构建 系统 based 在...上 bash 脚本 hides 警告
* :github:`38128` - [Coverity CID: 239574] Out-of-bounds access in subsys/storage/flash_map/flash_map.c
* :github:`38047` - twister: The --board-root parameter doesn't appear to work
* :github:`37893` - mcumgr_serial_tx_pkt with len==91 fails to transmit CRC
* :github:`37389` - nucleo_g0b1re: Swapping image in mcuboot results in hard fault and softbricks the device
* :github:`36986` - LittleFS mount fails (error -22)
* :github:`36962` - littlefs: 太 小 堆 用于 文件 缓存 (again).
* :github:`36852` - acrn_ehl_crb:  测试 的 tests/subsys/cpp/libcxx/ 失败
* :github:`36808` - xtensa xcc build  Fail ,   CONFIG_NO_OPTIMIZATIONS=y
* :github:`36766` - tests-ci :kernel.tickless.concept.tickless_slice : test failed
* :github:`34732` - stm32h747i_disco: Wrong Power supply setting LDO
* :github:`34375` - 驱动  CAN 配置 失败 当...时 CONFIG_CAN_FD_MODE  启用
* :github:`31748` - boards:lpcxpresso55s69: Manual toggling of CS required with ETH Click shield
* :github:`23052` - nrf52840_pca10056: Spurious RTS pulse and incorrect line level with hardware flow control disabled
* :github:`16587` - 构建 失败 带 gcc 9.x
* :github:`8924` - Get rid of -fno-strict-overflow
