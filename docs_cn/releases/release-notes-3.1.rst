:orphan:

.. _zephyr_3.1:

Zephyr 3.1.0
############

以下各节按组件提供详细的变更列表。

API 变更
***********

本次发布中的变更
=======================

* 所有 Zephyr 公共头文件已移至 ``include/zephyr``，这意味着
  包含它们时需要以 ``<zephyr/...>`` 为前缀。由于此更改
  可能会破坏许多应用或库，
  提供了 :kconfig:option:`CONFIG_LEGACY_INCLUDE_PATH` 以允许使用
  旧的包含路径。此选项现在默认启用，以允许
  平滑过渡。为了便于迁移到新的包含前缀，
  还提供了一个用于自动化的脚本：
  :zephyr_file:`scripts/utils/migrate_includes.py`。

* LoRaWAN：:c:func:`lorawan_send` 中的消息类型参数已从
  ``uint8_t`` 更改为 ``enum lorawan_message_type``。如果之前
  传入 ``0`` 表示未确认消息，现在必须更改为 ``LORAWAN_MSG_UNCONFIRMED``。
* 蓝牙：启用 :kconfig:option:`CONFIG_BT_EATT` 的应用
  必须设置 GATT 参数结构体中的 :c:member:`chan_opt` 字段。
  要保持旧行为，请使用 :c:enumerator:`BT_ATT_CHAN_OPT_NONE`。

* 磁盘子系统：SPI 模式的 SD 卡现在使用 SD 子系统与
  SD 卡通信。有关新设备树绑定格式要求的示例，
  请参见 :ref:`磁盘访问 API <disk_access_api>`。

* Kconfig 预处理器函数 ``dt_nodelabel_has_compat`` 已被重新定义，
  以与 ``dt_nodelabel_has_prop`` 函数和
  :c:func:`DT_NODE_HAS_COMPAT` 等设备树宏保持一致。
  现在该函数不再考虑被检查节点的状态。
  其原有功能由新引入的 ``dt_nodelabel_enabled_with_compat`` 函数提供。

* CAN

  * 在以下 CAN 回调函数签名中新增了 ``const struct device`` 参数：

    * ``can_tx_callback_t``
    * ``can_rx_callback_t``
    * ``can_state_change_callback_t``

  * 允许从用户空间调用以下 CAN API 函数：

    * :c:func:`can_set_mode()`
    * :c:func:`can_calc_timing()`
    * :c:func:`can_calc_timing_data()`
    * :c:func:`can_set_bitrate()`
    * :c:func:`can_get_max_filters()`

  * 更改 :c:func:`can_set_bitrate()` 以在比特率超过 800 kbit/s 时使用 75.0% 的采样点，
    超过 500 kbit/s 时使用 80.0%，所有其他比特率使用 87.5%。

  * 拆分 CAN classic 和 CAN-FD API：

    * :c:func:`can_set_timing()` 拆分为 :c:func:`can_set_timing()` 和
      :c:func:`can_set_timing_data()`。
    * :c:func:`can_set_bitrate()` 拆分为 :c:func:`can_set_bitrate()` 和
      :c:func:`can_set_bitrate_data()`。

  * 将 ``enum can_mode`` 转换为 ``can_mode_t`` 位域，并重命名 CAN 模式
    定义：

    * ``CAN_NORMAL_MODE`` 重命名为 :c:macro:`CAN_MODE_NORMAL`。
    * ``CAN_SILENT_MODE`` 重命名为 :c:macro:`CAN_MODE_LISTENONLY`。
    * ``CAN_LOOPBACK_MODE`` 重命名为 :c:macro:`CAN_MODE_LOOPBACK`。
    * 之前的 ``CAN_SILENT_LOOPBACK_MODE`` 可以使用位掩码 ``(CAN_MODE_LISTENONLY |
      CAN_MODE_LOOPBACK)`` 设置。

  * STM32H7：:kconfig:option:`CONFIG_NOCACHE_MEMORY` 不再负责在定义时
    禁用数据缓存。请改用 ``CONFIG_DCACHE=n``。

  * 将 STM32F1 引脚节点配置名称转换为包含重映射信息
    （在 NO_REMAP/REMAP_0 以外的情况下）
    例如：

    * ``i2c1_scl_pb8`` 重命名为 ``i2c1_scl_remap1_pb8``

本次发布中移除的 API
============================

* STM32F1 串行线 JTAG 配置（SWJ CFG）配置选择
  已从 Kconfig 移至 :ref:`设备树 <dt-guide>`。

* 移除 Kconfig 选项 ``CONFIG_BT_CTLR_NRF52840`` 和
  ``CONFIG_BT_CTLR_NRF52833``。
  这些选项现在由设备树属性 ``nordic,radio`` 控制。

* 移除 Kconfig 选项 ``CONFIG_BT_CTLR_FEM_NRF21540``。
  此 FEM 配置是硬件描述，因此已移至
  :ref:`设备树 <dt-guide>`。

* 移除 Kconfig 选项 ``CONFIG_BT_CTLR_GPIO_PA``、
  ``CONFIG_BT_CTLR_GPIO_PA_PIN``、``CONFIG_BT_CTLR_GPIO_PA_POL_INV``、
  ``CONFIG_BT_CTLR_GPIO_PA_OFFSET``、``CONFIG_BT_CTLR_GPIO_LNA``、
  ``CONFIG_BT_CTLR_GPIO_LNA_PIN``、``CONFIG_BT_CTLR_GPIO_LNA_POL_INV`` 和
  ``CONFIG_BT_CTLR_GPIO_LNA_OFFSET``。
  这些选项现在由设备树属性 ``nordic,fem`` 控制。

* 移除 Kconfig 选项 ``CONFIG_BT_CTLR_GPIO_PDN_PIN``、
  ``CONFIG_BT_CTLR_GPIO_PDN_POL_INV``、``CONFIG_BT_CTLR_GPIO_CSN_PIN``、
  ``CONFIG_BT_CTLR_GPIO_CSN_POL_INV`` 和 ``CONFIG_BT_CTLR_GPIO_PDN_CSN_OFFSET``。
  这些选项现在由设备树属性 ``nordic,fem`` 控制。

本次发布中弃用
==========================

* 弃用 Kconfig 选项 ``CONFIG_BT_CTLR_NRF52840`` 和
  ``CONFIG_BT_CTLR_NRF52833``。
  这些选项现在由设备树属性 ``nordic,radio`` 控制。

本次发布中的稳定 API 变更
==================================

* 蓝牙

  * 音频

    * 新增对 Content Control ID（CCID）的支持。
    * 新增对 Coordinated Set ID（CSID）的支持。
    * 新增对 Media Control（MCS）的支持。
    * 新增对 Volume Control（VC）的支持。
    * 新增对 Volume Offset Control（VOC）的支持。
    * 新增对 Audio Input Control（AIC）的支持。
    * 新增对 Media Proxy（MP）的支持。

  * 方向查找

    * 新增对周期性广播同步建立的支持。
    * 新增对 CTE 无连接接收的支持。
    * 新增对 CTE 无连接发送的支持。
    * 新增对 CTE 连接接收的支持。
    * 新增对 CTE 连接发送的支持。

  * 主机

    * 新增对 LE 广播扩展的支持。
    * 新增对周期性广播的支持。
    * 新增对等时通道的支持。
    * 新增对 ISO 广播组（BIG）的支持。
    * 新增对 ISO 广播流（BIS）的支持。
    * 新增对 ISO 连接流（CIS）的支持。
    * 新增对 ISO 连接组（CIG）的支持。
    * 新增对 ISO 广播接收端（BIS Receiver）的支持。
    * 新增对 ISO 广播发送端（BIS Broadcaster）的支持。
    * 新增对 ISO 连接接收端（CIS Receiver）的支持。
    * 新增对 ISO 连接发送端（CIS Sender）的支持。
    * 新增对 ISO 连接组控制（CIG Controller）的支持。
    * 新增对 ISO 广播组控制（BIG Controller）的支持。

  * Mesh

    * 新增对 Proxy Client 的支持
    * 新增对通过 PB-GATT 进行 Provisioners 的支持
    * 新增一个心跳发布回调选项

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

Trusted Firmware-m
******************

* 更新到 TF-M 1.6.0

文档
*************

* 重新组织和整合文档，以提高可读性和
  用户体验。
* 用新的
  Kconfig 文档引擎替换现有的静态渲染 Kconfig 文档，
  该引擎动态渲染 Kconfig 内容
  以提高搜索性能。
* 在 "Developing with Zephyr"
  类别下新增 "Language Support" 子类别，
  提供有关 C 和 C++ 语言及标准
  库支持状态的详细信息。
* 在 "Developing with Zephyr" 类别下新增 "Toolchain" 子类别，
  列出所有支持的
  工具链以及有关如何配置
  和使用它们的说明。

测试与示例
*****************

  * 新增了一个专用框架来测试 STM32 clock_control 驱动。

Issue 摘要
*************

本节列出了安全漏洞、其他已知 bug 以及
v3.1.0 开发期间处理的所有 issue。

安全漏洞相关
==============================

本次发布解决了以下 CVE：

更详细的信息可参见：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2022-1841：截至 2022-08-18 处于保密期
* CVE-2022-1042：截至 2022-06-19 处于保密期
* CVE-2022-1041：截至 2022-06-19 处于保密期

Known bugs
==========

- :github:`23302` - Poor TCP performance
- :github:`25917` - Bluetooth: Deadlock with TX of ACL data and HCI commands (command blocked by data)
- :github:`30348` - XIP can't be enabled with ARC MWDT toolchain
- :github:`31298` - tests/kernel/gen_isr_table failed on hsdk and nsim_hs_smp sometimes
- :github:`33747` - gptp does not work well on NXP rt series platform
- :github:`34226` - Compile error when building civetweb samples for posix_native
- :github:`34600` - Bluetooth: L2CAP: Deadlock when there are no free buffers while transmitting on multiple channels
- :github:`36358` - Potential issue with CMAKE_OBJECT_PATH_MAX
- :github:`37193` - mcumgr: Probably incorrect error handling with udp backend
- :github:`37704` - hello world doesn't work on qemu_arc_em when CONFIG_ISR_STACK_SIZE=1048510
- :github:`37731` - Bluetooth: hci samples: Unable to allocate command buffer
- :github:`38041` - Logging-related tests fails on qemu_arc_hs6x
- :github:`38544` - drivers: wifi: esWIFI: Regression due to 35815
- :github:`38654` - drivers: modem: bg9x: Has no means to update size of received packet.
- :github:`38880` - ARC: ARCv2: qemu_arc_em / qemu_arc_hs don't work with XIP disabled
- :github:`38947` - Issue with SMP commands sent over the UART
- :github:`39347` - Static object constructors do not execute on the NATIVE_POSIX_64 target
- :github:`39888` - STM32L4: usb-hid: regression in hal 1.17.0
- :github:`40023` - Build fails for ``native_posix`` board when using C++ <atomic> header
- :github:`41281` - Style Requirements Seem to Be Inconsistent with Uncrustify Configuration
- :github:`41286` - Bluetooth SDP: When the SDP attribute length is greater than SDP_MTU, the attribute is discarded
- :github:`41606` - stm32u5: Re-implement VCO input and EPOD configuration
- :github:`41622` - Infinite mutual recursion when SMP and ATOMIC_OPERATIONS_C are set
- :github:`41822` - BLE IPSP sample cannot handle large ICMPv6 Echo Request
- :github:`42030` - can: "bosch,m-can-base": Warning "missing or empty reg/ranges property"
- :github:`42134` - TLS handshake error using DTLS on updatehub
- :github:`42574` - i2c: No support for bus recovery imx.rt and or timeout on bus busy
- :github:`42629` - stm32g0: Device hang/hard fault with AT45 + ``CONFIG_PM_DEVICE``
- :github:`42842` - BBRAM API is missing a documentation reference page
- :github:`43115` - Data corruption in STM32 SPI driver in Slave Mode
- :github:`43246` - Bluetooth: Host: Deadlock with Mesh and Ext Adv on native_posix
- :github:`43249` - MBEDTLS_ECP_C not build when MBEDTLS_USE_PSA_CRYPTO
- :github:`43308` - driver: serial: stm32: uart will lost data when use dma mode[async mode]
- :github:`43390` - gPTP broken in Zephyr 3.0
- :github:`43515` - reel_board: failed to run tests/kernel/workq/work randomly
- :github:`43555` - Variables not properly initialized when using data relocation with SDRAM
- :github:`43562` - Setting and/or documentation of Timer and counter use/requirements for Nordic Bluetooth driver
- :github:`43646` - mgmt/mcumgr/lib: OS taskstat may give shorter list than expected
- :github:`43655` - esp32c3: Connection fail loop
- :github:`43811` - ble: gatt: db_hash_work runs for too long and makes serial communication fail
- :github:`43828` - Intel CAVS: multiple tests under tests/boards/intel_adsp/smoke are failing
- :github:`43836` - stm32: g0b1: RTT doesn't work properly after stop mode
- :github:`43887` - SystemView tracing with STM32L0x fails to compile
- :github:`43910` - civetweb/http_server - DEBUG_OPTIMIZATIONS enabled
- :github:`43928` - pm: going to PM_STATE_SOFT_OFF in pm_policy_next_state causes assert in some cases
- :github:`43933` - llvm: twister: multiple errors with set but unused variables
- :github:`44062` - Need a way to deal with stack size needed when running coverage report.
- :github:`44214` - mgmt/mcumgr/lib: Parasitic use of CONFIG_HEAP_MEM_POOL_SIZE in image management
- :github:`44219` - mgmt/mcumgr/lib: Incorrect processing of img_mgmt_impl_write_image_data leaves mcumgr in broken state in case of error
- :github:`44228` - drivers: modem: bg9x: bug on cmd AT+QICSGP
- :github:`44324` - Compile error in byteorder.h
- :github:`44377` - ISO Broadcast/Receive sample not working with coded PHY
- :github:`44403` - MPU fault and ``CONFIG_CMAKE_LINKER_GENERATOR``
- :github:`44410` - drivers: modem: shell: ``modem send`` doesn't honor line ending in modem cmd handler
- :github:`44579` - MCC: Discovery cannot complete with success
- :github:`44622` - Microbit v2 board dts file for lsm303agr int line
- :github:`44725` - drivers: can: stm32: can_add_rx_filter() does not respect CONFIG_CAN_MAX_FILTER
- :github:`44898` - mgmt/mcumgr: Fragmentation of responses may cause mcumgr to drop successfully processed response
- :github:`44925` - intel_adsp_cavs25: multiple tests failed after running tests/boards/intel_adsp
- :github:`44948` - cmsis_dsp: transofrm: error during building cf64.fpu and rf64.fpu for mps2_an521_remote
- :github:`44996` - logging: transient strings are no longer duplicated correctly
- :github:`44998` - SMP shell exec command causes BLE stack breakdown if buffer size is too small to hold response
- :github:`45105` - ACRN: failed to run testcase tests/kernel/fifo/fifo_timeout/
- :github:`45117` - drivers: clock_control: clock_control_nrf
- :github:`45157` - cmake: Use of -ffreestanding disables many useful optimizations and compiler warnings
- :github:`45168` - rcar_h3ulcb: failed to run test case tests/drivers/can/timing
- :github:`45169` - rcar_h3ulcb: failed to run test case tests/drivers/can/api
- :github:`45218` - rddrone_fmuk66: I2C configuration incorrect
- :github:`45222` - drivers: peci: user space handlers not building correctly
- :github:`45241` - (Probably) unnecessary branches in several modules
- :github:`45270` - CMake - TEST_BIG_ENDIAN
- :github:`45304` - drivers: can: CAN interfaces are brought up with default bitrate at boot, causing error frames if bus bitrate differs
- :github:`45315` - drivers: timer: nrf_rtc_timer: NRF boards take a long time to boot application in CONFIG_TICKLESS_KERNEL=n mode after OTA update
- :github:`45349` - ESP32: fails to chain-load sample/board/esp32/wifi_station from MCUboot
- :github:`45374` - Creating the unicast group before both ISO connections have been configured might cause issue
- :github:`45441` - SPI NOR driver assume all SPI controller HW is implemnted in an identical way
- :github:`45509` - ipc: ipc_icmsg: Can silently drop buffer if message is too big
- :github:`45532` - uart_msp432p4xx_poll_in() seems to be a blocking function
- :github:`45564` - Zephyr does not boot with CONFIG_PM=y
- :github:`45581` - samples: usb: mass: Sample.usb.mass_flash_fatfs fails on non-secure nrf5340dk
- :github:`45596` - samples: Code relocation nocopy sample has some unusual failure on nrf5340dk
- :github:`45647` - test: drivers: counter: Test passes even when no instances are found
- :github:`45666` - Building samples about BLE audio with nrf5340dk does not work
- :github:`45675` - testing.ztest.customized_output: mismatch twister results in json/xml file
- :github:`45678` - Lorawan: Devnonce has already been used
- :github:`45760` - Running twister on new board files
- :github:`45774` - drivers: gpio: pca9555: Driver is writing to output port despite all pins having been configured as input
- :github:`45802` - Some tests reported as PASSED (device) but they were only build
- :github:`45807` - CivetWeb doesn't build for CC3232SF
- :github:`45814` - Armclang build fails due to missing source file
- :github:`45842` - drivers: modem: uart_mux errors after second call to gsm_ppp_start
- :github:`45844` - Not all bytes are downloaded with HTTP request
- :github:`45845` - tests: The failure test case number increase significantly in CMSIS DSP tests on ARM boards.
- :github:`45848` - tests: console harness: inaccuracy testcases report
- :github:`45866` - drivers/entropy: stm32: non-compliant RNG configuration on some MCUs
- :github:`45914` - test: tests/kernel/usage/thread_runtime_stats/ test fail
- :github:`45929` - up_squared：failed to run test case tests/posix/common
- :github:`45951` - modem: ublox-sara-r4: outgoing datagrams are truncated if they do not fit MTU
- :github:`45953` - modem: simcom-sim7080: sendmsg() should result in single outgoing datagram
- :github:`46008` - stm32h7: gptp sample does not work at all
- :github:`46049` - Usage faults on semaphore usage in driver (stm32l1)
- :github:`46066` - TF-M: Unable to trigger NMI interrupt from non-secure
- :github:`46072` - [ESP32] Debug log error in hawkbit example "CONFIG_LOG_STRDUP_MAX_STRING"
- :github:`46073` - IPSP (IPv6 over BLE) example stop working after a short time
- :github:`46121` - Bluetooth: Controller: hci: Wrong periodic advertising report data status
- :github:`46124` - stm32g071 ADC drivers apply errata during sampling config
- :github:`46126` - pm_device causes assertion error in sched.c with lis2dh
- :github:`46157` - ACRN: some cases still failed because of the log missing
- :github:`46158` - frdm_k64f：failed to run test case tests/subsys/modbus/modbus.rtu/server_setup_low_none
- :github:`46167` - esp32: Unable to select GPIO for PWM LED driver channel
- :github:`46170` - ipc_service: open-amp backend may never leave
- :github:`46173` - nRF UART callback is not passed correct index via evt->data.rx.offset sometimes
- :github:`46186` - ISO Broadcaster fails silently on unsupported RTN/SDU_Interval combination
- :github:`46199` - LIS2DW12 I2C driver uses invalid write command
- :github:`46206` - it8xxx2_evb: tests/kernel/fatal/exception/ assertion failed -- "thread was not aborted"
- :github:`46208` - it8xxx2_evb: tests/kernel/sleep failed, elapsed_ms = 2125
- :github:`46234` - samples: lsm6dso: prints incorrect anglular velocity units
- :github:`46235` - subsystem: Bluetooth LLL: ASSERTION FAIL [!link->next]
- :github:`46255` - imxrt1010 wrong device tree addresses
- :github:`46263` - Regulator Control

Addressed issues
================

* :github:`46241` - Bluetooth: Controller: ISO: Setting CONFIG_BT_CTLR_ISO_TX_BUFFERS=4 breaks non-ISO data
* :github:`46140` - Custom driver offload socket creation failing
* :github:`46138` - 问题 带 构建 zephyr/samples/subsys/mgmt/mcumgr/smp_svr 使用 atsame70
* :github:`46137` - RFC: Integrate u8g2 monochrome graphcial library as module to Zephyr OS (https://github.com/olikraus/u8g2)
* :github:`46129` - net: lwm2m: Object Update Callbacks
* :github:`46102` - samples: net: W5500 implementation
* :github:`46097` - b_l072z_lrwan1 usart dma doesn't work
* :github:`46093` - get a run error "Fatal exception (28): LoadProhibited" while enable CONFIG_NEWLIB_LIBC=y
* :github:`46091` - samples: net: cloud: tagoio: Drop pinmux dependency
* :github:`46059` - LwM2M: Software management URI resource not updated properly
* :github:`46056` - ``unexpected eof`` with twister running ``tests/subsys/logging/log_api/logging.log2_api_immediate_printk_cpp`` on ``qemu_leon3``
* :github:`46037` - ESP32 :  fails to build the mcuboot, zephyr v3.1.0 rc2,  sdk 0.14.2
* :github:`46034` - subsys 设置  检查  return 值 的 函数 cs->cs_itf->csi_load(cs, &arg).
* :github:`46033` - twister: incorrect display of test results
* :github:`46027` - 测试 rpi_pico 测试 失败 在...上 twister 带 不 rule 到 创建 target 'bootloader/boot_stage2.S
* :github:`46026` - Bluetooth: Controller: llcp: Wrong effective time calculation if PHY changed
* :github:`46023` - drivers: reset: Use of reserved identifier ``assert``
* :github:`46020` - module/mcuboot: doesn't build with either RSA or ECISE-X25519 image encryption
* :github:`46017` - Apply for contributor
* :github:`46002` - NMP timeout when i am using  any mcumgr command
* :github:`45996` - stm32F7: DCache configuration is not correctly implemented
* :github:`45948` - net: socket: dtls: sendmsg() should result in single outgoing datagram
* :github:`45946` - net: context: outgoing datagrams are truncated if not enough memory was allocated
* :github:`45942` - tests: twister: harness: Test harness report pass when there is no console output
* :github:`45933` - webusb sample 代码 链接 错误 用于 esp32 板
* :github:`45932` - 测试 subsys/logging/log_syst : 失败 到 构建 在...上 rpi_pico
* :github:`45916` - USART 在...上 STM32: 使用 相同 名称 用于 不同 remapping 配置
* :github:`45911` - LVGL sample cannot be built with CONFIG_LEGACY_INCLUDE_PATH=n
* :github:`45904` - All tests require full timeout period to pass after twister overhaul when executed on HW platform
* :github:`45894` - up_squared：the 测试 shows pass 在...中  twister.log 它 但  不 seem 到 完成
* :github:`45893` - MCUboot authentication failure with RSA-3072 key on i.MX RT 1160 EVK
* :github:`45886` - ESP32: PWM parameter renaming broke compilation
* :github:`45883` - Bluetooth: Controller: CCM reads data before Radio stores them when DF enabled on PHY 1M
* :github:`45882` - Zephyr minimal C library contains files licensed with BSD-4-Clause-UC
* :github:`45878` - doc: release: Update release notes with CVE
* :github:`45876` - 板 h747/h745: 更新 dual 核心 刷写 和 调试 instructions
* :github:`45875` - bluetooth: hci_raw: avoid possible memory overflow in bt_buf_get_tx()
* :github:`45873` - SoC esp32: 使用 PYTHON_EXECUTABLE 从 构建 系统
* :github:`45872` - ci: make git credentials non-persistent
* :github:`45871` - ci: split Bluetooth workflow
* :github:`45870` - drivers: virt_ivshmem: Allow multiple instances of ivShMem devices
* :github:`45869` - doc: update requirements
* :github:`45865` - CODEOWNERS  错误
* :github:`45862` - USB ECM/RNDIS Can't receive broadcast messages
* :github:`45856` - blinky built with asserts on arduino nano
* :github:`45855` - Runtime 故障 当...时 运行 带 CONFIG_NO_OPTIMIZATIONS=y
* :github:`45854` - Bluetooth: Controller: llcp: Assert if LL_REJECT_IND PDU received while local and remote control procedure is pending
* :github:`45851` - For native_posix programs, k_yield doesn't yield to k_msleep threads
* :github:`45839` - Bluetooth: Controller: df: Possible memory overwrite if requested number of CTE is greater than allowed by configuration
* :github:`45836` - samples: Bluetooth: unicast_audio_server invalid check for ISO flags
* :github:`45834` - SMP Server Sample needs ``-DDTC_OVERLAY_FILE=usb.overlay`` for CDC_ACM
* :github:`45828` - mcumgr: img_mgmt_dfu_stopped is called on a successful erase
* :github:`45827` - bluetooth: bluetooth host: Adding the same device to resolving list
* :github:`45826` - Bluetooth: controller: Assert in lll.c when executing LL/CON/INI/BV-28-C
* :github:`45821` - STM32U5: clock_control: Issue to get rate of alt clock source
* :github:`45820` - bluetooth: host: Failed to set security right after reconnection with bonded Central
* :github:`45800` - 时钟 control 设置 用于 MCUX Audio 时钟  不正确
* :github:`45799` - LED strip driver flips colors on stm32h7
* :github:`45795` - driver: pinctrl: npcx: get build error when apply pinctrl mechanism to a DT node without reg prop.
* :github:`45791` - drivers/usb: stm32: Superfluous/misleading Kconfig option
* :github:`45790` - drivers: can: stm32h7: wrong minimum timing values
* :github:`45784` - nominate me as zephyr contributor
* :github:`45783` - drivers/serial: ns16550: message is garbled
* :github:`45779` - Implementing ARCH_EXCEPT on Xtensa unmasks nested interrupt handling bug
* :github:`45778` - Unable 到 使用 线程 aware 调试 带 STM32H743ZI
* :github:`45761` - MCUBoot with multi-image support on Zephyr project for i.MX RT1165 EVK
* :github:`45755` - ESP32 --defsym:1: undefined symbol \`printf' referenced in expression - using CONFIG_NEWLIB_LIBC
* :github:`45750` - tests-ci : kernel: timer: tickless test_sleep_abs Failed
* :github:`45751` - tests-ci : drivers: counter: basic_api test_multiple_alarms  Failed
* :github:`45739` - stm32h7: DCache configuration is not correctly implemented
* :github:`45735` - Ethernet W5500 Driver via SPI is deadlocking
* :github:`45725` - Bluetooth: Controller: df: CTE request not disabled if run in single shot mode
* :github:`45714` - Unable to get TCA9548A to work
* :github:`45713` - twister: map generation fails
* :github:`45708` - Bluetooth: Controller: llcp: CTE request control procedure has missing support for LL_UNKNOWN_RSP
* :github:`45706` - tests: error_hook: mismatch testcases in testplan.json
* :github:`45702` - 重启 instead 的 停止  系统
* :github:`45697` - RING_BUF_DECLARE broken for C++
* :github:`45691` - missing testcase tests/drivers/watchdog on nucleo stm32 boards
* :github:`45686` - missing testcase samples/drivers/led_pwm on nucleo stm32 boards
* :github:`45672` - Bluetooth: Controller: can't cancel periodic advertising sync create betwee ll_sync_create and reception of AUX__ADV_IND with SyncInfo
* :github:`45670` - Intel CAVS: log missing of tests/lib/p4workq/
* :github:`45664` - mqtt_publisher  不 工作 在...中 atsame54_xpro 板
* :github:`45648` - pm: device_runtime: API functions fault when PM not supported
* :github:`45632` - ESP32   get error "undefined reference to \`sprintf' "  while CONFIG_NEWLIB_LIBC=y
* :github:`45630` - ipc_service: Align return codes for available backends.
* :github:`45611` - GD32 build failure: CAN_MODE_NORMAL is redefined
* :github:`45593` - tests: newlib:  test_malloc_thread_safety fails on nrf9160dk_nrf9160_ns
* :github:`45583` - Typo 在...中 定义 的 lsm6ds0.h
* :github:`45580` - ESP32-C3: CONFIG_ESP32_PHY_MAX_TX_POWER undeclared error when building with CONFIG_BT=y
* :github:`45578` - cmake: gcc --print-multi-directory doesn't print full path and checks fails
* :github:`45577` - STM32L4: USB MSC doesn't work with SD card
* :github:`45568` - STM32H7xx: Driver for internal flash memory partially uses a fixed flash program word size, which doesn't fit for all STM32H7xx SOCs (e.g. STM32H7A3, STM32H7B0, STM32H7B3) leading to potential flash data corruption
* :github:`45557` - doc: Some generic yaml bindings don't show up in dts/api/bindings.html#dt-no-vendor
* :github:`45549` - bt_gatt_write_without_response_cb doesn't use callback
* :github:`45545` - K_ESSENTIAL option doesn't have any effect on k_create_thread
* :github:`45543` - 构建 samples/bluetooth/broadcast_audio_sink 提高  错误
* :github:`45542` - Implementing firmware image decompression in img_mgmt_upload()
* :github:`45533` - uart_imx_poll_in() seems to be a blocking function
* :github:`45529` - GdbStub get_mem_region bug
* :github:`45518` - LPCXpresso55S69 incorrect device name for JLink runner
* :github:`45514` - UDP Packet socket doesn't do L2 header processing
* :github:`45505` - NXP MIMXRT1050-EVKB: MCUBoot Serial Recover: mcumgr hangs when trying to upload image
* :github:`45488` - 构建 警告 当...时 不 GPIO 移植 启用
* :github:`45486` - MCUBootloader can't building for imxrt1160_evk_cm7 core
* :github:`45482` - 增加 构建 和 链接 Lua 在...中  project
* :github:`45468` -  uart_poll_in() blocking 或 不
* :github:`45463` - null function pointer called when using shell logger backend under heavy load
* :github:`45458` - it8xxx2_evb: tests/drivers/pwm/pwm_api assertion fail
* :github:`45443` - SAMD21: Wrong voltage reference set by enum adc_reference
* :github:`45440` - Intel CAVS: intel_adsp_hda testsuite is failing due to time out on intel_adsp_cavs15
* :github:`45431` - Bluetooth: Controller: df: Wrong antenna identifier inserted after switch pattern exhausted
* :github:`45426` - 数据 缓冲区 allocation: TCP 停止 工作
* :github:`45421` - Zephyr build image(sample blinky application) not getting flash through NXP Secure Provisioning Tool V4.0 for i.MX RT 1166EVK
* :github:`45407` - Support for flashing the Zephyr based application on i.MX RT 1160 EVK through SDP Mode(USB-HID/ UART) & PyOCD runner
* :github:`45405` - up_squared: most of the test case timeout
* :github:`45404` - Bluetooth: Controller: Periodic advertising scheduling is broken, TIFS/TMAFS maintenance corrupted
* :github:`45401` - test-ci: adc: lpcxpresso55s28: adc pinctl init error
* :github:`45394` - Bug when sending a BLE proxy mesh msg of length exactly 2x the MTU size
* :github:`45390` - MinGW-w64: Cannot build Zephyr project
* :github:`45395` - Programming NXP i.MX RT OTP fuse with west
* :github:`45372` - PWM 不 工作
* :github:`45371` - frdm_k64f: failed to run test case tests/net/socket/offload_dispatcher
* :github:`45367` - net: tcp: Scheduling dependent throughput
* :github:`45365` - Zephyr IP Stack Leaks in Promiscuous Mode
* :github:`45362` - sample/net/sockets/dumb_http_server 不 工作 带 enc28j60
* :github:`45361` - samples/bluetooth/hci_usb doesn't build for nucleo_wb55rg
* :github:`45359` - USB DFU sample does not work on RT series boards
* :github:`45355` - Twister 失败 当...时 west  不 当前
* :github:`45345` - Make FCB work with sectors larger than 16K
* :github:`45337` - timing: missing extern "C" in timing.h
* :github:`45336` - newlib: PRIx8 inttype incorrectly resolves to ``hh`` with newlib-nano
* :github:`45324` - NET_TCP_BACKLOG_SIZE  unused, 它  到  要么 实现 或 删除
* :github:`45322` - 测试 驱动 pwm_api 失败 带 stm32 设备
* :github:`45316` - 驱动 定时器 nrf_rtc_timer: SYS_CLOCK_TICKS_PER_SEC 太 高 用于 当...时 CONFIG_KERNEL_TICKLESS=n
* :github:`45314` - subsystem: Bluetooth LLL: ASSERTION FAIL [!link->next] @ ZEPHYR_BASE/subsys/bluetooth/controller/ll_sw/ull_conn.c:1952
* :github:`45303` - drivers: can: CAN classic and CAN-FD APIs are mixed together and CAN-FD is a compile-time option
* :github:`45302` - Bus Fault with Xilinx UART Lite
* :github:`45280` - GPIO 配置 问题
* :github:`45278` - twister: Run_id check feature breaks workflows with splitted building and testing.
* :github:`45276` - Add support for multiple zero-latency irq priorities
* :github:`45268` - Error newlibc ESP32
* :github:`45267` - kernel: Recursive spinlock in k_msgq_get() in the context of a k_work_poll handler
* :github:`45266` - teensy41: pwm sample unable to build
* :github:`45261` - mcumgr: conversion of version to string fails (snprintf format issue)
* :github:`45248` - Avoid redefining 32-bit integer types like __UINT32_TYPE__
* :github:`45237` - RFC: API Change: Bluetooth - replace callback in bt_gatt_subscribe_param
* :github:`45229` - sample: spi: bitbang: spi_bitbang sample has improper definition of its test
* :github:`45226` - samples/drivers/led_pwm: 构建 失败
* :github:`45219` - 驱动  transceivers  初始化 在...之后 controllers
* :github:`45209` - Minimal LIBC missing macros
* :github:`45189` - sam_e70b_xplained: failed to run test case tests/benchmarks/cmsis_dsp/basicmath
* :github:`45186` - 构建 Zephyr 在...上 Ubuntu 失败 当...时 ZEPHYR_TOOLCHAIN_VARIANT  设置 到 llvm
* :github:`45185` - Intel CAVS: tests under tests/ztest/register/ are failing
* :github:`45182` - MCUBoot Usage Fault on RT1060 EVK
* :github:`45172` - Bluetooth: attr->user_data is NULL when doing discovery with BT_GATT_DISCOVER_ATTRIBUTE
* :github:`45155` - STM32 serial port asynchronous initialization TX DMA channel error
* :github:`45152` - ``tests/subsys/logging/log_stack`` times out on ``qemu_arc_hs6x`` with twister
* :github:`45129` - mimxrt1050_evk: GPIO button pushed only once
* :github:`45123` - driver: can_stm32fd: STM32U5 series support
* :github:`45118` - Error claiming older doc is the latest
* :github:`45112` - Cannot install watchdog timeout on STM32WB
* :github:`45111` - fvp_base_revc_2xaemv8a: multiple test failures
* :github:`45110` - fvp_baser_aemv8r_smp: multiple test failures
* :github:`45108` - fvp_baser_aemv8r: multiple test failures
* :github:`45089` - stm32: usart: rx pin inversion missing
* :github:`45073` - nucleo_h743zi  failing twister builds due to NOCACHE_MEMORY warning
* :github:`45072` - [Coverity CID: 248346] Copy into fixed size buffer in /subsys/bluetooth/shell/bt.c
* :github:`45045` - mec172xevb_assy6906: tests/arch/arm/arm_irq_vector_table 失败 到 运行
* :github:`45012` - sam_e70b_xplained: failed to run test case tests/drivers/can/timing/drivers.can.timing
* :github:`45009` - twister: 许多 测试 失败 带 "mismatch 错误 在...之后 满足  SerialException.
* :github:`45008` - esp32: i2c_read() error was returned successfully at the bus nack
* :github:`45006` - Bluetooth HCI SPI fault
* :github:`44997` - zcbor 构建 错误 当...时 ZCBOR_VERBOSE  设置
* :github:`44985` - 测试 驱动  timing: 失败 到 设置 bitrate 的 800kbit/s 在...上 nucleo_g474re
* :github:`44977` - samples: 模块 canopennode: 失败 到 初始化 设置 subsystem 在...上 nucleo_g474re
* :github:`44966` - build fails for nucleo wb55 rg board.
* :github:`44956` - Deprecate the old spi_cs_control fields
* :github:`44947` - cmsis_dsp: matrix: error during building libraries.cmsis_dsp.matrix.unary_f64 for qemu_cortex_m3
* :github:`44940` - rom_report 创建 两个 identical identifier 但 用于 不同 路径 在...中 rom.json
* :github:`44938` - Pin assignments SPIS nrf52
* :github:`44931` - Bluetooth: Samples: broadcast_audio_source stack overflow
* :github:`44927` - 问题 在...中 使用 STM32 Hal 库
* :github:`44926` - intel_adsp_cavs25: can not build multiple tests under tests/posix/ and tests/lib/newlib/
* :github:`44921` - Can't run hello_world using mps_an521_remote
* :github:`44913` - Enabling BT_CENTRAL breaks MESH advertising
* :github:`44910` - 问题 当...时 安装 Python 额外 dependencies
* :github:`44904` - PR#42879 causes  挂起 在...中  shell history
* :github:`44902` - x86: FPU registers are not initialised for userspace (eager FPU sharing)
* :github:`44887` - it8xxx2_evb: tests/kernel/sched/schedule_api/ assertion fail
* :github:`44886` - Unable to boot Zephyr on FVP_BaseR_AEMv8R
* :github:`44882` - doc: Section/chapter "Supported Boards" missing from pdf documentation
* :github:`44874` - 错误 日志 用于 locking  mutex 在...中  ISR
* :github:`44872` - k_timer callback timing incorrect with multiple lightly loaded cores
* :github:`44871` - mcumgr endless loop in mgmt_find_handler
* :github:`44864` - tcp server tls error：server has no certificate
* :github:`44856` - Various 内核 timing-related 测试 失败 在...上 hifive1 板
* :github:`44837` - drivers: can: mcp2515: can_set_timing() performs a soft-reset of the MCP2515, discarding configured mode
* :github:`44834` - Add support for gpio expandeux NXP PCAL95xx
* :github:`44831` - west 刷写 用于 nucleo_u575zi_q  失败
* :github:`44830` - Unable to set compiler warnings on app exclusively
* :github:`44822` - STM32F103 Custom 板 时钟 配置 错误
* :github:`44811` - STRINGIFY  不 工作 带 mcumgr
* :github:`44798` - promote Michael to the Triage permission level
* :github:`44797` - x86: Interrupt handling not working for cores <> core0 - VMs not having core 0 assigned cannot handle IRQ events.
* :github:`44778` - stdint 类型 不 识别 在...中 soc_common.h
* :github:`44777` - disco_l475_iot1 default CONFIG_BOOT_MAX_IMG_SECTORS should be 512 not 256
* :github:`44758` - intel_adsp: kernel.common 测试  失败
* :github:`44752` - Nominate @brgl as contributor
* :github:`44750` - Using STM32 internal ADC with interrupt:
* :github:`44737` - Configurable LSE driving capability on H735
* :github:`44734` - regression in GATT/SR/GAS/BV-06-C qualification test case
* :github:`44731` - mec172xevb_assy6906: test/drivers/adc/adc_api test case build fail
* :github:`44730` - zcbor ARRAY_SIZE conflict with zephyr include
* :github:`44728` - Fresh Build and Flash of Bluetooth Peripheral Sample Produces Error on P-Nucleo-64 Board (STM32WBRG)
* :github:`44724` - can: drivers: mcux: flexcan: correctly handle errata 5461 and 5829
* :github:`44722` - lib: posix: support for pthread_attr_setstacksize
* :github:`44721` - drivers: can: mcan: can_mcan_add_rx_filter() unconditionally adds offset for extended CAN-ID filters
* :github:`44706` - drivers: can: mcp2515: mcp2515_set_mode() silently ignores unsupported modes
* :github:`44705` - Windows getting started references wget usage without step for installing wget
* :github:`44704` - Bootloader 链接 错误 在...期间 构建 用于 RPI_PICO
* :github:`44701` - advertising with multiple advertising sets fails with BT_HCI_ERR_MEM_CAPACITY_EXCEEDED
* :github:`44691` - west 签名 失败 到 查找 头文件 大小 或 padding
* :github:`44690` - ST kit b_u585i_iot02a and OCTOSPI flash support
* :github:`44687` - drivers: can: missing syscall verifier for can_get_max_filters()
* :github:`44680` - drivers: can: mcux: flexcan: can_set_mode() resets IP, discarding installed RX filters
* :github:`44678` - mcumgr: lib: cmd: img_mgmt: Warning about struct visibility emitted with certain Kconfig options
* :github:`44676` - mimxrt1050_evk_qspi 崩溃 或 freeze 当...时 访问 刷写
* :github:`44670` - tests-ci : kernel: tickless: concept test Timeout
* :github:`44671` - tests-ci : kernel: scheduler: deadline test failed
* :github:`44672` - tests-ci : drivers: counter: basic_api test failed
* :github:`44659` - Enhancement to k_thread_state_str()
* :github:`44621` - ASCS: Sink ASE stuck in Releasing state
* :github:`44600` - NMI testcase fails on tests/arch/arm/arm_interrupt with twister
* :github:`44586` - nrf5340: Random 崩溃 当...时  lot 的 中断  triggered
* :github:`44584` - SWO 日志 output  不 编译 用于 STM32WB55
* :github:`44573` - Do we have complete RNDIS stack available for STM32 controller in zephyr ?
* :github:`44558` - 可能 问题 带 定时器
* :github:`44557` - tests: canbus: isotp: implementation: fails on mimxrt1024_evk
* :github:`44553` - General Question: Compilation Time >15 Minutes?
* :github:`44546` - Bluetooth: ISO: Provide stream established information
* :github:`44544` - shell_module/sample.shell.shell_module.usb fails for thingy53_nrf5340_cpuapp_ns
* :github:`44539` - twister fails on several stm32 boards with tests/arch/arm testcases
* :github:`44535` - mgmt/mcumgr/lib: 不正确 使用 的 MGMT_ERR_ENOMEM, 在...中 最多 cases 在...处 它  使用
* :github:`44531` - bl654_usb without mcuboot maximum image size is not limited
* :github:`44530` - xtensa xcc build usb stack fail (newlib)
* :github:`44519` - Choosing CONFIG_CHIP Kconfig breaks LwM2M client client example build
* :github:`44507` - net: tcp: No retries of a TCP FIN message
* :github:`44504` - net: tcp: Context still open after timeout on connect
* :github:`44497` - 增加 guide 用于 禁用 MSD 在...上 JLink OB 设备 和 链接 到 从 smp_svr page
* :github:`44495` - sys_slist_append_list and sys_slist_merge_slist corrupt target slist if appended or merged list is empty
* :github:`44489` - Docs: missing documentation related to MCUBOOT serial recovery feature
* :github:`44488` - Self sensor library from private git repository
* :github:`44486` - nucleo_f429zi: multiple networking tests failing
* :github:`44484` - 驱动  mcp2515:  MCP2515 驱动 使用 错误 timing limits
* :github:`44483` - 驱动  mcan: 数据 phase prescaler bounds 检查 使用 错误 值
* :github:`44482` - 驱动  mcan: CAN_SJW_NO_CHANGE 不 接受 带 CONFIG_ASSERT=y
* :github:`44480` - bt_le_adv_stop null pointer exception
* :github:`44478` - Zephyr 在...上 Litex/Vexriscv 不 引导
* :github:`44473` - net: tcp: 连接  不 properly 终止 当...时 连接  lost
* :github:`44453` - Linker 警告 在...中 watchdog samples 和 测试 构建 用于 twr_ke18f
* :github:`44449` - qemu_riscv32 DHCP fault
* :github:`44439` - Bluetooth: Controller: Extended and Periodic Advertising HCI Component Conformance Test Coverage
* :github:`44427` - SYS_CLOCK_HW_CYCLES_PER_SEC not correct for hifive1_revb / FE310
* :github:`44404` - Porting stm32h745 for zephyr
* :github:`44397` - twister: test case error number discrepancy in the result
* :github:`44391` - tests-ci : peripheral: gpio: 1pin test Timeout
* :github:`44438` - tests-ci : arch: interrupt: arm.nmi test Unknown
* :github:`44386` - Zephyr SDK 0.14.0 does not contain a sysroots directory
* :github:`44374` - Twister: Non-intact handler.log files when running tests and samples folders
* :github:`44361` - drivers: can: missing syscall verifier for can_set_mode()
* :github:`44349` - Nordic BLE 失败 assertion 当...时 日志记录  启用
* :github:`44348` - 驱动  z_vrfy_can_recover()  不 编译
* :github:`44347` - ACRN: multiple tests failed due to incomplete log
* :github:`44345` - 驱动  M_CAN bus recovery 函数   错误 signature
* :github:`44344` - drivers: can: mcp2515 introduces a hard dependency on CONFIG_CAN_AUTO_BUS_OFF_RECOVERY
* :github:`44338` - intel_adsp_cavs18: multiple tests failed due to non-intact log
* :github:`44314` - rddrone_fmuk66: fatal error upon running basic samples
* :github:`44307` - LE Audio: unicast stream/ep or ACL disconnect reset should not terminate the CIG
* :github:`44296` - Bluetooth: Controller: DF: IQ sample of CTE signals are not valid if PHY is 1M
* :github:`44295` - Proposal for subsystem for media
* :github:`44284` - LE Audio: Missing recv_info for BAP recv
* :github:`44283` - Bluetooth: ISO: Add TS flag for ISO receive
* :github:`44274` - direction_finding_connectionless_rx/tx U-Blox Nora B106 EVK
* :github:`44271` - mgmt/mcumgr: BT transport: Possible buffer overflow (and crash) when reciving SMP when CONFIG_MCUMGR_BUF_SIZE < transport MTU
* :github:`44262` - mimxrt1050_evk: 构建 时间 太 长 用于 这 平台
* :github:`44261` - twister: 一些 更改 创建 测试 cases 工作 abnormally.
* :github:`44259` - intel_adsp_cavs18: tests/lib/icmsg failed
* :github:`44255` - 内核 在...期间 线程  运行 [thread_state]  在...中 _THREAD_QUEUED
* :github:`44251` - ``CONFIG_USB_DEVICE_REMOTE_WAKEUP`` gets 默认 值 `y` 如果 不 设置
* :github:`44250` - Can't build WiFi support on esp32, esp32s2, esp32c3
* :github:`44247` - west build -b nrf52dk_nrf52832 samples/boards/nrf/clock_skew failed
* :github:`44244` - Bluetooth: Controller: ISO BIS payload counter rollover
* :github:`44240` - 测试 驱动 pwm_api: PWM 驱动 测试 doesn't 编译 用于 mec172xevb_assy6906
* :github:`44239` - boards: arm: mec152x/mec172x CONFIG_PWM=y doesn't compile PWM driver
* :github:`44231` - 问题 trying 到 配置  environment
* :github:`44218` - libc: minimal: qsort_r not working as expected
* :github:`44216` - 测试 驱动 counter_basic_api: 构建 失败 在...上 LPCxpresso55s69_cpu
* :github:`44215` - 测试 subsys: cpp: over half 的 测试 失败 在...上 macOS 但  不 失败 在...上 Linux
* :github:`44213` - xtensa arch_cpu_idle not correct on cavs18+ platforms
* :github:`44199` - (U)INT{32,64}_C 宏 常量  不 匹配  Zephyr stdint 类型
* :github:`44192` - esp32 flash custom partition table
* :github:`44186` - Possible race condition in TCP connection establishment
* :github:`44145` - Zephyr Panic dump garbled on Intel cAVS platforms
* :github:`44134` - nRF52833 当前 consumption 太 高
* :github:`44128` - Deprecate DT_CHOSEN_ZEPHYR_FLASH_CONTROLLER_LABEL
* :github:`44125` - drivers/ethernet/eth_stm32_hal.c: eth_stm32_hal_set_config() always returns -ENOTSUP (-134)
* :github:`44110` - Bluetooth: synced callback may have wrong addr type
* :github:`44109` - 设备 tree 错误 在...期间 移植 zephyr 用于  custom 板
* :github:`44108` - ``CONFIG_ZTEST_NEW_API=y`` broken with ``CONFIG_TEST_USERSPACE=y``
* :github:`44107` - The SMP nsim boards are started incorrectly when launching on real HW
* :github:`44106` - 测试 的 dma 驱动 失败 在...上 dma_m2m_loop_test
* :github:`44101` -  构建 错误 当...时 CONFIG_MULTITHREADING=n
* :github:`44092` - rand32_ctr_drbg fails to call the respective initialization routing
* :github:`44089` - 日志记录 shell backend: null-deref 当...时 日志  dropped
* :github:`44072` - mcumgr smp 源码  检查 变量 没有 它  设置 和 causing automated 测试 失败
* :github:`44070` - west spdx TypeError: 'NoneType' object is not iterable
* :github:`44043` - Usage 故障 当...时 运行 刷写 shell sample 在...上 RT1064 EVK
* :github:`44029` - Unexpected behavior of CONFIG_LOG_OVERRIDE_LEVEL
* :github:`44018` - net: tcp: 运行 出 的 缓冲区 由 包 loss
* :github:`44012` - net: tcp: Cooperative scheduling transfer size limited
* :github:`44010` - frdm_k64f: failed to run testcase samples/kernel/metairq_dispatch/
* :github:`44006` - intel_adsp_cavs25: tests/drivers/dma/loop_transfer failed
* :github:`44004` - Bluetooth: ascs: Invalid ASE state transition: Releasing -> QoS Configured
* :github:`43993` - doc: Fix minor display issue for west spdx extension command
* :github:`43990` - 如何 到 创建 civetweb 运行 在...上  specified 网络 card
* :github:`43988` - Extracting the index of a child node referenced using alias
* :github:`43980` - No PWM signal on Nucleo F103RB using TIM1 CH2 PA9
* :github:`43976` - [lwm2m_engine / sockets] Possibility to decrease timeout on connect()
* :github:`43975` - 测试 内核 scheduler: 测试 从 kernel.scheduler.slice_perthread 失败 在...上 一些 nrf 平台
* :github:`43972` - UART: uart_poll_in() not working in Shell application
* :github:`43964` - k_timer callback timing gets unreliable with more cores active
* :github:`43950` - code_relocation: Add NOCOPY feature breaks windows builds
* :github:`43949` - drivers: espi: mec172x: ESPI flash write and erase operations not working
* :github:`43948` - drivers: espi: xec: MEC172x: Driver enables all bus interrupts but doesn't handle them causing starvation
* :github:`43946` - Bluetooth: Automatic ATT MTU negotiation
* :github:`43940` - 支持 用于 CH32V307 设备
* :github:`43930` - nRF52833 High Power Consumption with 32.768kHz RC Oscillator
* :github:`43924` - ipc_service: Extend API with zero-copy send
* :github:`43899` - can: stm32: Build issue on g4 target
* :github:`43898` - Twister:  test case number discrepancy in the result xml.
* :github:`43891` - networking: detect initialisation failures of backing drivers
* :github:`43888` - adc: stm32: compilation broken on G4 targets
* :github:`43874` - mec172xevb_assy6906: tests/drivers/spi/spi_loopback  test case UART output wrong.
* :github:`43873` - tests:ci:lpcxpresso55s06: portability.posix.common.newlib meet hard fault
* :github:`43872` - tests:ci:lpcxpresso55s06:libraries.cmsis_dsp.matrix.unary_f32 测试 失败
* :github:`43870` - test:ci:lpcxpresso55s06: hwinfo test meet hardfault
* :github:`43867` - mec172xevb_assy6906: tests/drivers/pwm/pwm_api  test case build fail.
* :github:`43865` - Add APDS-9250 I2C Driver
* :github:`43864` - mec172xevb_assy6906: tests/drivers/pwm/pwm_loopback  test case failed to build
* :github:`43858` - mcumgr seems 到 lock 上 当...时 它 接收 命令 用于 分组   不 exist
* :github:`43856` - mec172xevb_assy6906: tests/drivers/i2c/i2c_api  i2c_test failed
* :github:`43851` - LE Audio: Make PACS location optional
* :github:`43838` - mec172xevb_assy6906: tests/drivers/adc/adc_dma  test case build fail
* :github:`43842` - tests-ci : libraries: encoding: jwt test Timeout
* :github:`43841` - tests-ci : net: socket: tls.preempt test Timeout
* :github:`43835` - ``zephyr_library_compile_options()`` 失败 到 apply 如果  相同 设置  设置 用于 multiple 库 在...中  single project
* :github:`43834` - DHCP not work in ``Intel@PSE`` on ``Intel@EHL``
* :github:`43830` - LPC55S69 不 刷写 到 第二 核心
* :github:`43829` - http_client: http_client_req() returns incorrect number of bytes sent
* :github:`43818` - lib: os: ring_buffer: recent changes cause UART shell to fail on qemu_cortex_a9
* :github:`43816` - tests: cmsis_dsp: rf16 and cf16 tests are not executed on Native POSIX
* :github:`43807` - 测试 "cpp.libcxx.newlib.exception" 失败 在...上 平台 哪个 使用 zephyr.bin 到 运行 测试
* :github:`43794` - BMI160 Driver: Waiting time between SPI activation and reading CHIP IP is too low
* :github:`43793` - Alllow callbacks to CDC_ACM events
* :github:`43792` - mimxrt1050_evk: failed to run tests/net/socket/tls and tests/subsys/jwt
* :github:`43786` - 日志记录 日志 context redefined 带 XCC 当...时 使用 zephyr 日志记录 API 带 SOF
* :github:`43757` - it8xxx2_evb: k_busy_wait is not working accurately for ITE RISC-V
* :github:`43756` - 驱动 gpio: pca95xx  不 编译 带 CONFIG_GPIO_PCA95XX_INTERRUPT
* :github:`43750` - ADC 驱动 构建  损坏 用于 STM32L412
* :github:`43745` - Xtensa XCC Build spi_nor.c fail
* :github:`43742` - BT510 lis2dh sensor does not disconnect SAO pull-up resistor
* :github:`43739` - tests: dma: random failure on dma loopback suspend and resume case on twr_ke18f
* :github:`43732` - esp32: MQTT publisher sample stuck for both TLS and non-TLS sample.
* :github:`43728` - esp32 build error while applicaton in T2 topology
* :github:`43718` - Bluetooth: bt_conn: Unable to allocate buffer within timeout
* :github:`43715` - ESP32 UART devicetree binding design issue
* :github:`43713` - intel_adsp_cavs: 测试  不 运行 带 twister
* :github:`43711` - samples: tfm: psa Some TFM/psa samples fail on nrf platforms
* :github:`43702` - samples/arch/smp/pktqueue 不 工作 在...上 ESP32
* :github:`43700` - mgmt/mcumgr: Strange Kconfig names for MCUMGR_GRP_ZEPHYR_BASIC log levels
* :github:`43699` - Bluetooth Mesh working with legacy and extended advertising simultaneously
* :github:`43693` - LE Audio: Rename enum bt_audio_pac_type
* :github:`43669` - LSM6DSL IMU driver - incorrect register definitions
* :github:`43663` - stm32f091 test   tests/kernel/context/ test_kernel_cpu_idle  fails
* :github:`43661` - Newlib math 库 不 工作 带 user 模式 线程
* :github:`43656` - samples:bluetoooth:direction_finding_connectionless_rx antenna switching not working with nRF5340
* :github:`43654` - Nominate Mehmet Alperen Sener as Bluetooth Mesh Collaborator
* :github:`43649` - Best practice for "external libraries" and cmake
* :github:`43647` - Bluetooth: LE multirole: connection as central is not totally unreferenced on disconnection
* :github:`43640` - stm32f1: Convert ``choice GPIO_STM32_SWJ`` to dt
* :github:`43636` - Documentation incorrectly states that C++ new and delete operators are unsupported
* :github:`43630` - Zperf tcp download stalls with window size becoming 0 on Zephyr side
* :github:`43618` - Invalid thread indexes out of userspace generation
* :github:`43600` - 测试 mec15xxevb_assy6853: 最多 的  测试 cases 失败
* :github:`43587` - arm: trustzone: Interrupts using FPU causes usage fault when ARM_NONSECURE_PREEMPTIBLE_SECURE_CALLS is disabled
* :github:`43580` - hl7800: tcp stack freezes on slow response from modem
* :github:`43573` - return const struct device \* for device_get_binding(const char \*name)
* :github:`43568` - ITE eSPI driver expecting OOB header also along with OOB data from app code - espi_it8xxx2_send_oob() & espi_it8xxx2_receive_oob
* :github:`43567` - Bluetooth: Controller: ISO data packet dropped on payload array wraparound
* :github:`43553` - Request to configure SPBTLE-1S of STEVAL-MKSBOX1V1
* :github:`43552` - samples: bluetooth: direction_finding: Sample fails on nrf5340
* :github:`43543` - RFC: API Change: Bluetooth: struct bt_auth_cb field removal
* :github:`43525` - 默认 网络 接口 selection 由 up-state
* :github:`43518` - 'DT_N_S_soc_S_timers_40012c00_S_pwm' undeclared
* :github:`43513` - it8xxx2_evb: tests/kernel/sleep failed
* :github:`43512` - wifi: esp_at: sockets not cleaned up on close
* :github:`43511` - lvgl: 升级 到 8.2 构建 问题
* :github:`43505` - ``py`` 命令 不 查找 当...时 使用 nanopb 在...上 windows
* :github:`43503` - 构建 版本 detection 不 工作 当...时 Zephyr 内核   Git Submodule
* :github:`43490` - net: sockets: userspace accept() crashes with NULL addr/addrlen pointer
* :github:`43487` - LE Audio: Broadcast audio sample
* :github:`43476` - tests: nrf: Output of nrf5340dk_nrf5340_cpuapp_ns not available
* :github:`43470` - wifi: esp_at: race condition on mutex's leading to deadlock
* :github:`43469` - USBD_CLASS_DESCR_DEFINE section name bug
* :github:`43465` - 'Malformed data' on bt_data_parse() for every ble adv packet on bbc_microbit
* :github:`43456` - winc1500 wifi 驱动 失败 到 构建
* :github:`43452` - Missing SPI SCK on STM32F103vctx
* :github:`43448` - Deadlock detection in ``bt_att_req_alloc`` ineffective when ``CONFIG_BT_RECV_IS_RX_THREAD=n``
* :github:`43440` - Bluetooth: L2CAP send le data lack calling net_buf_unref() function
* :github:`43430` -  there 任何 计划 到 develop zephyr 到 mircrokenrel 架构
* :github:`43425` - zephyr+Linux+hypervisor on Raspberry Pi 4
* :github:`43419` - Pull request not updated after force push the original branch
* :github:`43411` - STM32 SPI DMA issue
* :github:`43409` - frdm_k64f: USB connection gets lost after continuous testing
* :github:`43400` - nrf board system_off sample application does not work on P1 buttons
* :github:`43392` - Bluetooth: ISO: unallocated memory written during mem_init
* :github:`43389` - LoRaWAN on Nordic and SX1276 & SX1262 Shield
* :github:`43382` - mgmt/mcumgr/lib: Echo OS command echoes back empty string witn no error when string is too long to handle
* :github:`43378` - TLS availability misdetection when ZEPHYR_TOOLCHAIN_VARIANT is not set
* :github:`43372` - pm: lptim: stm32h7: pending irq stops STANDBY
* :github:`43369` - Use Zephyr crc implementation for LittleFS
* :github:`43359` - Bluetooth: ASCS QoS 配置  不 失败 用于 preferred 设置
* :github:`43348` - twister:skipped case num issue when use --only-failed.
* :github:`43345` - Bluetooth: Controller: Extended and Periodic Advertising Link Layer Component Test Coverage
* :github:`43344` - intel_adsp_cavs25: samples/subsys/logging/syst  失败 带  timeout 当...时  sample  启用 到 运行 在...上 intel_adsp_cavs25
* :github:`43333` - RFC: Bring zcbor as CBOR decoder/encoder in replacement for TinyCBOR
* :github:`43326` - Unstable SD Card performance on Teensy 4.1
* :github:`43319` - 硬件 复位 cause API 设置 复位 pin bit 每个 时间  API  called
* :github:`43316` - stm32wl55 cannot enable PLL source as MSI
* :github:`43314` - LE Audio: BAP ``sent`` callback missing
* :github:`43310` - disco_l475_iot1: BLE not working
* :github:`43306` - sam_e70b_xplained:  平台   不 normal 在...之后 运行 测试 case tests/subsys/usb/desc_sections/
* :github:`43305` - wifi: esp_at: shell command "wifi scan" not working well
* :github:`43295` - mimxrt685_evk_cm33: Hard fault with ``CONFIG_FLASH=y``
* :github:`43292` - NXP RT11xx devicetree missing GPIO7, GPIO8, GPIO12
* :github:`43285` - nRF5x System Off demo fails to put the nRF52840DK into system off
* :github:`43284` - samples: drivers: watchdog failed in mec15xxevb_assy6853
* :github:`43277` - usb/dfu: upgrade request is not called while used from mcuboot, update doesn't happen
* :github:`43276` - tests: up_squared:  testsuite tests/kernel/sched/deadline/ failed
* :github:`43271` - tests: acrn_ehl_crb:  tests/arch/x86/info failed
* :github:`43268` - LE Audio: Add stream ops callbacks for unicast server
* :github:`43258` - HCI core data buffer overflow with ESP32-C3 in Peripheral HR sample
* :github:`43248` - Bluetooth: Mesh: Unable used with ext adv on native_posix
* :github:`43235` - STM32 platform does not handle large i2c_write() correctly
* :github:`43230` - Deprecate DT_CHOSEN_ZEPHYR_ENTROPY_LABEL
* :github:`43229` - nvs: 更改 nvs_init 到 接受  设备 reference
* :github:`43218` - nucleo_wb55rg: 划分 更新 必需 到 使用 0.13.0 BLE 固件
* :github:`43205` - UART 控制台 损坏 自...以来 099850e916ad86e99b3af6821b8c9eb73ba91abf
* :github:`43203` - BLE: With BT_SETTINGS and BT_SMP, second connection blocks the system in connection event notification
* :github:`43192` - lvgl: upgrade LVGL to 8.1 build error
* :github:`43190` - Bluetooth: audio: HCI command timeout on LE Setup Isochronous Data Path
* :github:`43186` - Bluetooth: import nrf ble_db_discovery library to zephyr
* :github:`43172` - CONFIG_BT_MESH_ADV_EXT doesn't build without CONFIG_BT_MESH_RELAY
* :github:`43163` - Applications 不 提取 LVGL cannot  配置 或 编译
* :github:`43159` - hal: stm32: ltdc pins should be very-high-speed
* :github:`43142` - Ethernet and PPP communication conflicts
* :github:`43136` - STM32 Uart log never take effect
* :github:`43132` - Thingy:52 i2c_nrfx_twim: Error 0x0BAE0001 occurred for message
* :github:`43131` - LPCXPresso55S69-evk dtsi file incorrect
* :github:`43130` - STM32WL ADC idles / doesn't work
* :github:`43117` - 不 可能 到 创建 更多 than 一个 shield.
* :github:`43109` - drivers:peci:xec: PECI Command 'Ping' does not work properly
* :github:`43099` - CMake: ARCH roots issue
* :github:`43095` - Inconsistent logging config result resulted from menuconfig.
* :github:`43094` - CMake 栈 overflow 在...之后 更改  build/zephyr/.config, 甚至 仅 timestamp.
* :github:`43090` - mimxrt685_evk_cm33: USB examples not working on Zephyr v3.0.0
* :github:`43087` - XCC build failures for all intel_adsp tests/platforms
* :github:`43081` - [Slack] Slack invite 工作 仅 在...上 非常 少数 mail 地址 - 这   更改
* :github:`43066` - stm32wl55 true RNG  falls in seed error
* :github:`43058` - PACS: Fix PAC capabilities to be exposed in PAC Sink/Source characteristic
* :github:`43057` - twister: error while executing twister script on windows machine for sample example code
* :github:`43046` - Wifi sample not working with disco_l475_iot1
* :github:`43034` - Documentation 用于 ``console_putchar`` 函数  不正确
* :github:`43024` - samples: tests task wdt fails on some stm32 nucleo target boards
* :github:`43020` - samples/subsys/fs/littlefs  不 工作 带 native_posix 板 在...上 WSL2
* :github:`43016` - Self inc/dec works incorrectly with logging API.
* :github:`42997` - Bluetooth: Controller: Receiving Periodic Advertising Reports with larger AD Data post v3.0.0-rc2
* :github:`42988` - Specify and standardize undefined behavior on empty response from server for http_client
* :github:`42960` - Bluetooth: Audio: Codec config parsing and documentation
* :github:`42953` - it8xxx2_evb: 测试 在...中 tests/kernel/timer/timer_api 失败
* :github:`42940` - Please add zsock_getpeername
* :github:`42928` - CSIS: Invalid usage of bt_conn_auth_cb callbacks
* :github:`42888` - Bluetooth: Controller: Extended Advertising - Advertising Privacy Support
* :github:`42881` - Arduino due missing 'arduino_i2c' alias.
* :github:`42877` -  k_cycle_get_32 returns 0 on start-up on native_posix
* :github:`42874` - ehl_crb: samples/kernel/metairq_dispatch 失败 当...时 它  运行 multiple 时间
* :github:`42870` - Build error due to minimal libc qsort callback cast
* :github:`42865` - openocd 配置 缺失 用于 stm32mp157c_dk2 板
* :github:`42857` - sam_e70b_xplained: failed to run test cases tests/net/npf and tests/net/bridge
* :github:`42856` - Bluetooth: BAP: Unicast client sample cannot connect
* :github:`42854` - k_busy_wait() never returns when called - litex vexriscv soc and cpu on xilinx ac701 board
* :github:`42851` - it8xxx2_evb: Mutlitple tests in tests/kernel/contex fail.
* :github:`42850` - CONFIG items disappeared in zephyr-3.0-rc3
* :github:`42848` - it8xxx2_evb: 测试 在...中 /tests/subsys/cpp/libcxx 失败
* :github:`42847` - it8xxx2_evb: Multiple tests in tests/subsys/portability/cmsis_rtos_v2 fail.
* :github:`42831` - Do the atomic* functions require protection from optimization?
* :github:`42829` - GATT: bt_gatt_is_subscribed does not work as expected when called from bt_conn_cb->connected
* :github:`42825` - MQTT client disconnection (EAGAIN) on publish with big payload
* :github:`42817` - ADC on ST Nucleo H743ZI board with DMA
* :github:`42800` - gptp_mi neighbor_prop_delay is not included in sync_receipt_time calculation due cast from double to uint64_t
* :github:`42799` - gptp correction field 在...中 sync 遵循 上 消息  不  正确 endianness
* :github:`42774` - pinctrl-0 问题 在...中 设备 tree 构建
* :github:`42723` - 测试 kernel.condvar: child 线程  不 运行
* :github:`42702` - upsquared: drivers.counter.cmos.seconds_rate is failing with busted maximum bound when run multiple times
* :github:`42685` - Socket echo server sample code not working in Litex Vexriscv cpu (Xilinx AC701 board)
* :github:`42680` - Missing bt_conn_(un)ref for LE Audio and tests
* :github:`42599` - 测试 内核 mem_protect: mem_protect 失败 在...之后 复位 在...上 stm32wb55 nucleo
* :github:`42588` - lsm6dso
* :github:`42587` - LE Audio: BAP Unicast API use array of pointers instead of array of streams
* :github:`42559` - 6LoCAN samples fail due to null pointer dereference
* :github:`42548` - acrn_ehl_crb:  twister failed to run tests/subsys/logging due to UnicodeEncodeError after switching to log v2
* :github:`42544` - Bluetooth: controller: llcp: handling of remote procedures with and without instant
* :github:`42534` - BLE 测试 函数  不 工作 properly
* :github:`42530` - Possibility to define pinmux item for Pin Control as a plain input/output
* :github:`42524` - 错误 implementation 的 SPI 驱动
* :github:`42520` - bt_ots Doxygen documentation does not seem to be included in the Zephyr project documentation.
* :github:`42518` - Bluetooth Ext Adv:Sync: While simultaneous advertiser are working, and skip is non-zero, sync terminates repeatedly
* :github:`42508` - TWIHS hangs
* :github:`42496` - ARM M4 MPU backed userspace livelocks on stack overflow when FPU enabled
* :github:`42478` - Unable to build mcuboot for b_u585i_iot02a
* :github:`42453` - Unable to update Firmware using MCUBoot on STM32G0 series
* :github:`42436` - NXP eDMA overrun errors on SAI RX
* :github:`42434` - NXP I2S (SAI) driver bugs
* :github:`42432` - i2c: unable to configure SAMD51 i2c clock frequency for standard (100 KHz) speeds
* :github:`42425` - i2c: sam0 driver does not prevent simultaneous transactions
* :github:`42351` - stm32H743 nucleo board cannot flash after tests/drivers/flash
* :github:`42343` - LE Audio: PACS: Server change location
* :github:`42342` - LE Audio: PACS notify changes to locations
* :github:`42333` - Cannot write to qspi flash in adafruit feather nrf52840, device tree is wrong
* :github:`42310` - Support for TCA6408A gpio expander, which existing driver as a base?
* :github:`42306` - Bluetooth: Host: More than ``CONFIG_BT_EATT_MAX`` EATT channels may be created
* :github:`42290` - ESP32 - Heltec Wifi - Possibly invalid CONFIG_ESP32_XTAL_FREQ setting (40MHz). Detected 26 MHz
* :github:`42235` - SocketCAN not supported for NUCLEO H743ZI
* :github:`42227` - Teensy41 support SDHC - Storage init Error
* :github:`42189` - Sub 1GHz Support for CC1352
* :github:`42181` - Ethernet PHY imxrt1060 Teensy not working, sample with DHCPv4_client fails
* :github:`42113` - Modbus RTU allow non-compliant client configuration
* :github:`42108` - upsquared: isr_dynamic & isr_regular test is failing
* :github:`42102` - doc: searches for sys_reboot() are inconsistent
* :github:`42096` - LE Audio: Media: Pass structs by reference and not value
* :github:`42090` - Bluetooth: Audio: MCS BSIM notification length warning
* :github:`42083` - Bluetooth: ISO: 包 排序 数量   incremented 用于 每个 通道
* :github:`42081` - Direction 查找 代码 支持 用于 nrf52811?
* :github:`42072` - west: spdx: Blank FileChecksum field for missing build file
* :github:`42050` - printk 缺陷  函数 called 从 printk  invoked 三个 时间 given certain 配置 变量
* :github:`42015` - LED api can't be called from devicetree phandle
* :github:`42011` - Establish guidelines for TSC working groups
* :github:`42000` - BQ274xx 驱动 不 工作 correctly
* :github:`41995` - tracing: riscv: Missing invoking the sys_trace_isr_exit()
* :github:`41947` - lpcxpresso55s16 SPI hardware chip select not working
* :github:`41946` - Bluetooth: ISO: Sending on RX-only CIS doesn't report error
* :github:`41944` - Assertion triggered when system is going to PM_STATE_SOFT_OFF
* :github:`41931` - drivers: audio: tlv320dac310x: device config used as non-const
* :github:`41924` - drivers: dma/i2c: nios2: config used as non-const
* :github:`41921` - Fast USB DFU workflow
* :github:`41899` - ESP32 Wifi mDNS
* :github:`41874` - Recursive spinlock error on ARM in specific circumstances
* :github:`41864` - ESP32 Wifi AP Mode DHCP Service
* :github:`41823` - Bluetooth: Controller: llcp: Remote request are dropped due to lack of free proc_ctx
* :github:`41788` - Bluetooth: Controller: llcp: Refectored PHY Update procedure asserts while waiting for free buffers to send notifications
* :github:`41787` - Alignment issue on Cortex M7
* :github:`41777` - periodic_adv periodic_sync lost data
* :github:`41773` - LoRaWAN: Unable to correctly join networks of any version on LTS
* :github:`41742` - stm32g0: stm32_temp: not working
* :github:`41710` - tests: ztest: ztress: Test randomly fails on qemu_cortex_a9
* :github:`41677` - undefined reference to \`__device_dts_ord_xx'
* :github:`41667` - doc: arm: mec172x:  MEC172x EVB documentation points to some inexistent jumpers
* :github:`41652` - Bluetooth: Controller: BIG: Channel map update BIG: Generation of BIG_CHANNEL_MAP_IND (sent 6 times)
* :github:`41651` - Bluetooth: Controller: BIG Sync: Channel map update of BIG
* :github:`41650` - STM32H7 SPI123 incorrect clock source used for prescaler calculation
* :github:`41642` - 部署 生成 docs 从 PRs
* :github:`41628` - Move LVGL glue code to zephyr/modules/
* :github:`41613` - 进程 审查 和 更新 Milestone 定义
* :github:`41597` - Unable to build mcuboot for BL654_DVK
* :github:`41596` - Split connected ISO client and server by Kconfig
* :github:`41594` - LE Audio: Upstream CCP/TBS
* :github:`41593` - LE Audio: Upstream BASS
* :github:`41592` - Object Transfer Service Client made "official"
* :github:`41590` - LE Audio: CAP API - Acceptor
* :github:`41517` - Hard 故障 如果 ``CONFIG_LOG2_MODE_DEFERRED``  启用
* :github:`41472` - Unable to mount fat file system on nucleo_f429zi
* :github:`41449` - PWM capture with STM32
* :github:`41408` - Low power states for STM32 H7
* :github:`41388` - tests: coverage: test code coverage report failed on mps2_an385
* :github:`41382` - nordic nrf52/nrf53 and missing cpu-power-states (dts) for automatic device PM control
* :github:`41375` - hal_nordic: update 15.4 driver to newest version
* :github:`41297` - QSPI flash need read, write via 4 lines not 1 line
* :github:`41285` - pthread_once has incorrect behavior
* :github:`41230` - LE Audio: API Architecture and documentation for GAF
* :github:`41228` - LE Audio: Add a codec to Zephyr
* :github:`41220` - STM32H7: Check for VOSRDY instead of ACTVOSRDY
* :github:`41201` - LE Audio: Improved media_proxy internal data structure
* :github:`41200` - LE Audio: Other postponed MCS cleanups
* :github:`41196` - LE Audio: Reconfigure Unicast Group after creation
* :github:`41194` - LE Audio: Remove support for bidirectional audio streams
* :github:`41192` - LE Audio: Change PACS from indicate to notify
* :github:`41191` - LE Audio: Update pac_indicate to actually send data
* :github:`41188` - LE Audio: Remove stream (dis)connected callback from stream ops
* :github:`41186` - LE Audio: CAP API - Initiator
* :github:`41169` - twister: program get stuck when serial in hardware map is empty string
* :github:`41151` - RFC: Provide k_realloc()
* :github:`41093` - Kconfig.defconfig:11: error: couldn't parse 'default $(dt_node_int_prop_int,/cpus/cpu@0,clock-frequency)'
* :github:`40970` - Upgrade qemu to fix breakage in mps3-an547
* :github:`40920` - Bluetooth audio: client/server naming scheme
* :github:`40901` - RFC: API Change: update LVGL from v7 to v8
* :github:`40874` - mps2_an521_ns: fail to handle user_string_alloc_copy() with null parameter
* :github:`40856` - PPP: gsm_modem: LCP never gets past REQUEST_SENT phase
* :github:`40775` - stm32: multi-threading broken after #40173
* :github:`40679` - libc/minimal: static variable of gmtime() does not located to z_libc_partition at usermode.
* :github:`40657` - Cannot 启用 次 pwm 出 通道 在...上 stm32f3
* :github:`40635` - gen_app_partitions.py  不 include 所有 object 文件 产生 由 构建 系统
* :github:`40620` - zephyr with cadence xtensa core dsp LX7 ，helloworld program  cannot be entered after the program is executed
* :github:`40593` - tests: lib: cmsis_dsp: Overflows in libraries.cmsis_dsp.matrix
* :github:`40591` - RFC: Replace TinyCBOR with ZCBOR within Zephyr
* :github:`40588` - mgmg/mcumg/lib: Replace TinyCBOR with zcbor
* :github:`40559` - Move LittlefFS 配置 头文件 和 CMakeLists.txt 从 模块 到 zephyr/modules
* :github:`40371` - modem: uart 接口  不 禁用 TX 中断 在...中 ISR
* :github:`40360` - 错误 消息 带  sample: Asynchronous 套接字 Echo Server 使用 选择
* :github:`40306` - ESP32 BLE transmit error
* :github:`40298` - Bluetooth assertions in lll_conn.c
* :github:`40204` - Bluetooth: ll_sync_create_cancel fails with BT_HCI_ERR_CMD_DISALLOWED before BT_HCI_EVT_LE_PER_ADV_SYNC_ESTABLISHED is generated
* :github:`40195` - CONFIG_BOARD default value using cmake -DBOARD define value
* :github:`39948` - kernel.common.stack_sentinel fails on qemu_cortex_a9
* :github:`39922` - Instruction fetch fault happens on RISC-V with XIP and userspace enabled
* :github:`39834` - [Coverity CID: 240669] Unrecoverable parse warning in subsys/jwt/jwt.c
* :github:`39738` - twister: tests: samples: Skips on integration_platforms in CI
* :github:`39520` - 增加 支持 用于  BlueNRG-LP SoC
* :github:`39432` - Periodic adv. syncing takes longer and bt_le_per_adv_sync_delete returns error after commit ecf761b4e9
* :github:`39314` - Invalid CONTROLLER_ID in usb_dc_mcux.c for LPC54114
* :github:`39194` - 进程 调查 GitHub 代码 审查 replacements
* :github:`39184` - HawkBit hash mismatch
* :github:`39176` - overflow in sensor_value_from_double
* :github:`39132` - subsys/net/ip/tcp2: 缺失 feature 到 减少 接收 Window 大小 发送 在...中  ACK messge
* :github:`38978` - Esp32 compilation error after enabling CONFIG_NEWLIB_LIBC
* :github:`38966` - Please add STM32F412VX
* :github:`38747` - data/json: encoding issues with array in object_array
* :github:`38632` - Multiple potential dead-locks modem_socket_wait_data
* :github:`38570` - Process: binary blobs in Zephyr
* :github:`38567` - Process: legitimate signed-off-by lines
* :github:`38548` - stm32: QSPI flash driver concurrent access issue
* :github:`38305` - Update to LVGL v8
* :github:`38279` - Bluetooth: Controller: assert LL_ASSERT(!radio_is_ready()) in lll_conn.c
* :github:`38268` - Multiple defects in "Multi Producer Single Consumer Packet Buffer" library
* :github:`38179` - twister: only report failures in merged junit output
* :github:`37798` - Change nRF5340DK board files to handle CPUNET pin configuration with DTS nodes
* :github:`37730` - http_client_req: Timeout likely not working as expected
* :github:`37710` - Bluetooth advert 包 大小  大小 的 maximum 包 不 大小 的 actual 数据
* :github:`37683` - STM32 Eth Tx DMA always uses first descriptor instead of going through circular buffer
* :github:`37324` - subsys/mgmt/hawkbit: Unable to finish download if CPU blocking function (i.e. ``flash_img_buffered_write``) is used
* :github:`37294` - RTT logs not found with default west debug invocation on jlink runner
* :github:`37191` - nrf5340: Support +3dBm TX power
* :github:`37186` - entropy: Bluetooth derived entropy device
* :github:`36905` - 改进 (k\_)malloc 和 堆 documentation
* :github:`36882` - MCUMGR: fs upload fail for first time file upload
* :github:`36645` - minimal libc: add strtoll and strtoull functions
* :github:`36571` - LoRa 支持 用于 random DevNonce 和 NVS 栈 状态 存储
* :github:`36266` - kernel timeout_list NULL pointer access
* :github:`35316` - log_panic() 挂起 内核
* :github:`34737` - Can't compile CIVETWEB with CONFIG_NO_OPTIMIZATIONS or CONFIG_DEBUG
* :github:`34590` - Functions getopt_long and getopt_long_only from the FreeBSD project
* :github:`34256` - Add support for FVP in CI / SDK
* :github:`34218` - Civetweb server crashing when trying to access invalid resource
* :github:`34204` - nvs_write: 坏 记录 return 值
* :github:`33876` - Lora sender sample build error for esp32
* :github:`32885` - Zephyr C++ support documentation conflicts to the code
* :github:`31613` - Undefined reference errors when using External Library with k_msgq_* calls
* :github:`30724` - CAN J1939 Support
* :github:`30152` - Settings nvs subsystem uses a hardcoded flash area label
* :github:`29981` - Improve clock initialization on LPC & MXRT600
* :github:`29941` - Unable to connect Leshan LwM2M server using x86 based LwM2M client
* :github:`29199` - github integration: ensure maintainers are added to PRs that affect them
* :github:`29107` - Bluetooth: hci-usb uses non-standard interfaces
* :github:`28009` - 增加 连接 状态 到  连接 info
* :github:`27841` - samples: disk: unable to access sd card
* :github:`27177` - Unable to build samples/bluetooth/st_ble_sensor for steval_fcu001v1 board
* :github:`26731` - Single channel selection - Bluetooth - Zephyr
* :github:`26038` - 构建 zephyr 带 llvm 失败
* :github:`25362` - better 支持 用于 posix API 读取 写入 在...中 socketpair 测试
* :github:`24733` - Misconfigured environment
* :github:`23347` - net: ieee802154_radio: API improvements
* :github:`22870` - 增加 Cortex-M4 测试 平台
* :github:`22455` - How to assign USB endpoint address manually in stm32f4_disco for CDC ACM class driver
* :github:`22247` - Discussion: Supporting the Arduino ecosystem
* :github:`22161` - 增加 shell 命令 用于  设置 subsystem
* :github:`21994` - Bluetooth: controller: split: Fix procedure complete event generation
* :github:`21409` - sanitycheck: cmd.exe colorized output
* :github:`20269` - 增加 支持 用于 opamps 在...中 MCUs
* :github:`19979` - Implement Cortex-R floating-point support
* :github:`19244` - BLE throughput of DFU by Mcumgr is too slow
* :github:`17893` - dynamic 线程 don't 工作 在...上 x86 在...中 一些 配置
* :github:`17743` - cross 编译 用于 RISCV32 失败 as compiler flags  不 supplied 由 板 但   在...中 target.cmake
* :github:`17005` - Upstreamability of SiLabs RAIL support
* :github:`16406` - west: runners: Add --id and --chiperase options
* :github:`16205` - 增加 支持 到 west 到 刷写 w/o  构建 但 given  binary
* :github:`15820` - mcumgr: taskstat show name & used size
* :github:`14649` - CI 测试   retry-free
* :github:`14591` - Infineon Tricore architecture support
* :github:`13318` - k_thread_foreach api breaks real time semantics
* :github:`9578` - Windows installation of SDK needs 'just works' installer
* :github:`8536` - imxrt1050: Replace systick with gpt or other system timer
* :github:`8481` - Remove the Kconfig helper options for nRF ICs once DT can replace them
* :github:`8139` - Driver for BMA400 accelerometer
* :github:`6654` - efm32wg_stk3800 bluetooth sample  不 编译 增加 支持
* :github:`6162` - LwM2M: 支持 队列 模式 Operation
* :github:`1495` - esp32: newlibc errors
* :github:`1392` - No module named 'elftools'
* :github:`3192` - Shutting down BLE support
* :github:`3150` - Si1153 Ambient Light Sensor, Proximity, and Gesture detector support
