:orphan:

.. _zephyr_2.2:
.. _zephyr_2.2.1:

Zephyr 2.2.1
#############

这是 Zephyr 2.2 的维护版本，包含修复。

上一版本的发布说明见 :ref:`zephyr_2.2.0`。

安全漏洞相关
******************************

本版本解决了以下安全漏洞（CVE）：

  * 修复 CVE-2020-10028
  * 修复 CVE-2020-10060
  * 修复 CVE-2020-10063
  * 修复 CVE-2020-10066

更详细的信息可在以下地址找到：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

已修复 Issue
************

自上次 2.2.0 标记版本以来，解决了以下 GitHub issue：

* :github:`23494` - Bluetooth: LL/PAC/SLA/BV-01-C 在禁用从设备发起的特性交换时失败
* :github:`23485` - BT: host: 无论是否需要都会发送 Service Change 指示
* :github:`23482` - 2M PHY + DLE 以及加密链路上的时序计算不正确
* :github:`23070` - Bluetooth: controller: 修复 ticker 实现以避免追赶
* :github:`22967` - Bluetooth: controller: 无效数据包序列时断言失败
* :github:`24183` - [v2.2] Bluetooth: controller: split: 连接更新期间从设备延迟回归
* :github:`23805` - Bluetooth: controller: Mesh LPN 切换到非连接广播失败
* :github:`24086` - Bluetooth: SMP: 配对失败时删除现有绑定
* :github:`24211` - [v2.2.x] lib: updatehub: 在 Zephyr 2.x 上不工作
* :github:`24601` - Bluetooth: Mesh: Config Client 的 net_key_status 拉取两个密钥索引，应只拉取一个
* :github:`25067` - 厂商实现的 ticker 节点不足
* :github:`25350` - Bluetooth: controller: 从设备延迟导致数据传输延迟
* :github:`25483` - Bluetooth: controller: split: 特性交换不符合 V5.0 核心规范
* :github:`25478` - settings_runtime_set() 未填充 bt/cf
* :github:`25447` - cf_set() 在无可用配置时返回 0

.. _zephyr_2.2.0:

Zephyr 2.2.0
############

我们很高兴宣布 Zephyr RTOS 2.2.0 版本的发布。

本版本的主要增强功能包括：

* 新增对 64 位 ARMv8-A 架构的初始支持（实验性）。
* 通过第三方 CANopenNode 协议栈支持 CANopen 协议
* 通过集成 Semtech LoRaWAN 端点协议栈并新增 SX1276 LoRa modem 驱动，
  新增了对 LoRa 的支持。

以下章节提供了按组件划分的详细变更列表。

安全漏洞相关
******************************

本版本解决了以下安全漏洞（CVE）：

  * 修复 CVE-2020-10019
  * 修复 CVE-2020-10021
  * 修复 CVE-2020-10023
  * 修复 CVE-2020-10024
  * 修复 CVE-2020-10026
  * 修复 CVE-2020-10027
  * 修复 CVE-2020-10028
  * 修复 CVE-2020-10058

更详细的信息可在以下地址找到：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

API 变更
***********

本版本中弃用
==========================

* Settings

  * SETTINGS_USE_BASE64，以 base64 编码值被标记为移除。

本版本中的稳定 API 变更
==================================

* GPIO

  * GPIO API 已被重构，以支持来自 Linux DTS GPIO 绑定的已知标志。
    它们通常定义在板卡 DTS 文件中

    - GPIO_ACTIVE_LOW、GPIO_ACTIVE_HIGH 用于设置引脚有效电平
    - GPIO_OPEN_DRAIN、GPIO_OPEN_SOURCE 用于将引脚配置为开漏或开集
    - GPIO_PULL_UP、GPIO_PULL_DOWN 用于配置引脚偏置

  * 引脚逻辑电平的读/写由 gpio_pin_get、gpio_pin_set 函数支持。
  * 引脚物理电平的读/写由 gpio_pin_get_raw、gpio_pin_set_raw 函数支持。
  * 新增一组端口函数，可同时操作属于同一控制器的多个引脚。
  * 中断应通过专用的 gpio_pin_interrupt_configure() 函数配置。
    通过 gpio_pin_configure() 配置中断仍受支持，但该特性将在
    未来版本中移除。
  * 新增一组标志，允许基于引脚物理或逻辑电平设置任意中断配置（如果
    驱动支持）。
  * 新增一组标志，用于将引脚配置为输入、输出或输入/输出，
    以及设置输出初始状态。
  * 大部分旧 GPIO API 已被弃用。尽管已尽力保持向后兼容性，
    但由于工作范围所限，无法完全实现该目标。我们建议尽快
    切换到新 GPIO API。
  * 弃用 API 的行为可能与原始旧实现不同的领域包括：

    - 引脚中断配置，特别是涉及 GPIO_INT_ACTIVE_LOW 和
      GPIO_POL_INV 标志的情况。
    - 在无中断相关标志时调用 gpio_pin_configure() 的行为。
      在该弃用功能的新实现中，中断保持不变。
      在原始实现中，某些 GPIO 驱动会禁用中断。

  * 多个依赖 GPIO API 提供功能的驱动已被重构，
    以遵循引脚有效电平。这些驱动的任何外部用户
    都必须更新其 DTS 板卡文件。

    - bluetooth/hci/spi.c
    - display/display_ili9340.c
    - display/ssd1306.c
    - ieee802154/ieee802154_mcr20a.c
    - ieee802154/ieee802154_rf2xx.c
    - lora/sx1276.c
    - wifi/eswifi/eswifi_core.c
    - 大多数传感器驱动

* PWM

  * pwm_pin_set_cycles()、pwm_pin_set_usec() 和
    pwm_pin_set_nsec() 函数现在接受 flags 参数。新引入的
    标志为 PWM_POLARITY_NORMAL 和 PWM_POLARITY_INVERTED，
    用于指定 PWM 信号的极性。如果不需要标志，
    flags 参数可设为 0（默认为 PWM_POLARITY_NORMAL）。
  * 类似地，pwm_pin_set_t PWM 驱动 API 函数现在
    接受 flags 参数。PWM 控制器驱动必须检查
    flags 参数的值，如果设置了任何
    不受支持的标志，则返回 -ENOTSUP。

* USB

  * 之前由 USB 协议栈自动调用的 usb_enable() 函数，
    现在需要应用程序显式调用以启用 USB 子系统。
  * usb_enable() 函数现在接受一个参数 usb_dc_status_callback，
    应用程序可将其设置为回调以接收来自
    USB 协议栈的状态事件。该参数也可设为 NULL 表示不需要回调。

* nRF flash 驱动

  * nRF Flash 驱动已将默认写入块大小更改为 32 位
    对齐。之前对 8 位写入块大小的仿真可通过
    CONFIG_SOC_FLASH_NRF_EMULATE_ONE_BYTE_WRITE_ACCESS Kconfig 选项选择。
    仅建议为与旧存储内容兼容而使用
    8 位写入块大小仿真。

* Clock control

  * 回调原型（clock_control_cb_t）现在有一个额外参数
    （clock_control_subsys_t），指示哪个时钟子系统被启动。

本版本中移除的 API
============================

* Shell

  * SHELL_CREATE_STATIC_SUBCMD_SET（已弃用），被
    SHELL_STATIC_SUBCMD_SET_CREATE 取代
  * SHELL_CREATE_DYNAMIC_CMD（已弃用），被 SHELL_DYNAMIC_CMD_CREATE 取代

* 移除了 Newtron Flash File System (NFFS)。NFFS 被移除，
    因为它存在严重问题，且长时间未修复。在可能的地方，
    NFFS 的使用被 LittleFS 使用取代，作为更好的替代品。

内核
******

* 解决了在启用 SMP 的系统上观察到的一些竞争条件
* 如果提交的工作队列项已完成，则传播不同的错误码
* 在处理致命错误时禁用抢占
* 修复系统调用栈帧的问题（如果系统调用被抢占
  然后尝试 Z_OOPS()）
* 新增 k_thread_stack_space_get() 系统调用，用于分析线程栈
  空间。在某些情况下或某些架构上存在问题的旧方法
  （如 STACK_ANALYZE()）现已弃用。
* 许多内核对象 API 现在可选地返回运行时错误值，
  而不是依赖断言。这些返回值、失败断言
  或完全不做检查，由新的 Kconfig 选项
  ASSERT_ON_ERRORS、NO_RUNTIME_CHECKS、RUNTIME_ERROR_CHECKS 控制。
* 对 arch_cpu_start() API 的清理
* 自旋锁验证现在会转储错误使用的自旋锁的地址
* 对断言机制的若干改进
* k_poll() 可传入 0 个事件，此时它只是让调用者睡眠
* 新增 k_thread_foreach_unlocked() API
* 如果从 ISR 调用 k_sleep()，则新增断言
* 大量 64 位修复，主要与数据类型大小相关
* k_mutex_unlock() 现在是正确的重新调度点
* 对当前线程调用 k_thread_suspend() 现在会正确调用
  调度器
* 对任何线程调用 k_thread_suspend() 会取消该线程的任何
  待处理超时
* 修复协作线程的 meta-IRQ 抢占边界情况

架构
*************

* ARC：

  * 修复了若干与 irq 处理相关的问题

* ARM：

  * 新增对 ARMv8-A 64 位架构的初始支持（实验性）
  * 在 ARM Cortex-M 中新增对 Direct Dynamic Interrupts 的支持
  * 修复 ARM Cortex-R 架构移植中的若干严重 bug
  * 修复 ARMv8-M 栈限制检查中的若干严重 bug
  * 为 ARM Cortex-A53 新增 QEMU 仿真支持
  * 增强 ARM Cortex-R 架构的 QEMU 仿真支持
  * 扩展 ARM 特定内核特性的测试覆盖
  * 新增对 GIC SGI 和 PPI 中断类型的支持
  * 重构 GIC 驱动以支持多个 GIC 版本

* POSIX：

  * N/A

* RISC-V：

  * N/A

* x86：

  * 修复大于 INT_MAX 的 Kconfig 值的问题
  * 修复在 x86_64 上处理异常时 callee-saved 寄存器
    可能被不必要地保存到栈上的问题
  * 修复 x86_64 上上下文切换时保存 RFLAGS 的潜在竞争
  * 为 'acrn' 目标启用 64 位模式和 X2APIC
  * 如果线程在多个核心上被调度，则为 RIP 添加 0xB9 的毒值
  * 在 x86_64 上实现 CONFIG_USERSPACE
  * 修复在 qemu_x86_64 上加载 Zephyr 镜像时
    保留内存可能被覆盖的问题
  * x86_64 现在在遇到致命错误时会退出 QEMU，
    与 32 位行为一致
  * 对异常调试消息的清理和改进

板卡与 SoC 支持
********************

* 新增对这些 SoC 系列的支持：

.. rst-class:: rst-columns

   * Atmel SAM4E
   * Atmel SAMV71
   * Broadcom BCM58400
   * NXP i.MX RT1011
   * Silicon Labs EFM32GG11B
   * Silicon Labs EFM32JG12B
   * ST STM32F098xx
   * ST STM32F100XX
   * ST STM32F767ZI
   * ST STM32L152RET6
   * ST STM32L452XC
   * ST STM32G031
   * Intel Apollolake Audio DSP

* 新增对这些 Xtensa 板卡的支持：

  .. rst-class:: rst-columns

    * Up Squared board Audio DSP

* 新增对这些 ARM 板卡的支持：

  .. rst-class:: rst-columns

    * Atmel SAM 4E Xplained Pro
    * Atmel SAM E54 Xplained Pro
    * Atmel SAM V71 Xplained Ultra
    * Broadcom BCM958401M2
    * Cortex-A53 Emulation (QEMU)
    * Google Kukui EC
    * NXP i.MX RT1010 Evaluation Kit
    * Silicon Labs EFM32 Giant Gecko GG11
    * Silicon Labs EFM32 Jade Gecko
    * ST Nucleo F767ZI
    * ST Nucleo G474RE
    * ST Nucleo L152RE
    * ST Nucleo L452RE
    * ST STM32G0316-DISCO Discovery kit
    * ST STM32VLDISCOVERY

* 移除对这些 ARM 板卡的支持：

  .. rst-class:: rst-columns

     * TI CC2650


* 新增对以下 shield 的支持：

  .. rst-class:: rst-columns

     * ST7789V Display generic shield
     * TI LMP90100 Sensor Analog Frontend (AFE) Evaluation Board (EVB)

* 移除对以下 shield 的支持：

  .. rst-class:: rst-columns

     * Link board CAN

驱动程序与传感器
*******************

* ADC

  * 新增带 GPIO 的 LMP90xxx 驱动

* Audio

  * N/A

* Bluetooth

  * 将 SPI 驱动更新为新 GPIO API
  * 对 H:5（三线 UART）驱动的若干修复

* CAN

  * 支持 STM32 的 CAN_2，但不能同时使用 CAN_1 和 CAN_2。
  * 支持 STM32F3 和 STM32F4 系列
  * 在 mcux flexcan 驱动中新增 SocketCAN 支持
  * 修复 stm32 驱动中的位时序转换
  * 引入 can-primary 设备树别名

* Clock Control

  * 修改 nRF 平台驱动，使用单一设备支持多个
    子系统，每个时钟源一个。

* Console

  * N/A

* Counter

  * counter_read() API 函数已弃用，改用
    counter_get_value()。新 API 函数新增返回值，
    用于指示计数器是否读取成功。
  * 新增缺失的系统调用

* Crypto

  * 在 crypto_mtls_shim 中新增 AES GCM、ECB 和 CBC 支持
  * 新增 stm32 CRYP 驱动

* Debug

  * N/A

* Display

  * 新增通用 display 驱动示例
  * 新增对 BGR565 像素格式的支持
  * 新增对 LVGL v6.1 的支持
  * 引入基于 KSCAN 的 ft5336 触摸面板驱动
  * 新增对 LVGL 触摸输入设备的支持

* DMA

  * dw: 将 cavs 驱动重命名为 DesignWare
  * stm32: 改进通道支持

* EEPROM

  * 为 STM32L0 和 STM32L1 SoC 系列新增 EEPROM 驱动
  * 新增 EEPROM 仿真器（替换 native_posix EEPROM 驱动）

* Entropy

  * 新增对 sam0 的支持
  * 新增 LiteX PRBS 模块驱动

* ESPI

  * N/A

* Ethernet

  * 支持 SiLabs Giant Gecko GG11 以太网驱动
  * 修复 LiteX VexRiscv 的以太网网络

* Flash

  * 新增 Nordic JEDEC QSPI NOR flash 驱动
  * 将 native_posix flash 驱动与 drivers/flash/flash_simulator 统一
  * 修复：初始化时擦除 native_posix flash
  * 扩展 MCUX flash 驱动以支持 LPC55xxx 设备
  * stm32: 将 Flash 驱动中的寄存器访问替换为使用 STM32Cube
  * Nios2: qspi 非对齐读支持
  * sam0: 新增对 SAME54 的支持
  * 新增 stm32f1x 系列的 flash 驱动

* GPIO

  * 将所有驱动更新到新 API
  * 新增 LiteX GPIO 驱动

* Hardware Info

  * N/A

* I2C

  * 在 stm32 驱动中默认启用中断
  * 新增带 scan 命令的 I2C shell
  * 新增 LiteX I2C 控制器驱动
  * 在 stm32 驱动中新增对 STM32G0X 的支持
  * 在 mcux lpspi 驱动中新增对总线空闲超时属性的支持
  * 在 sam0 驱动中新增对 SAME54 的支持

* I2S

  * N/A

* IEEE 802.15.4

  * 新增对 IEEE 802.15.4 rf2xxx 驱动的支持

* Interrupt Controller

  * 新增对多个 GIC 版本的支持
  * 将 s1000 驱动重命名为 cavs
  * 新增 SweRV 可编程中断控制器驱动
  * 修复 RV32M1 中断控制器的无效通道 bug

* IPM

  * N/A

* Keyboard Scan

  * 新增 ft5336 触摸面板驱动

* LED

  * N/A

* LED Strip

  * 修复 ws2812 驱动

* LoRa

  * 通过复用 LoRaMac-node 库，新增支持 LoRa 技术
    所需的 API 和驱动。

* Modem

  * 新增对通用 GSM modem 的支持

* Neural Net

  * N/A

* PCIe

  * N/A

* Pinmux

  * 移除 CC2650 驱动

* PS/2

  * N/A

 * PTP Clock

   * N/A

* PWM

  * 新增 RV32M1 timer/PWM 驱动
  * 新增 LiteX PWM 外设驱动
  * 新增对反转 PWM 信号的支持

* Sensor

  * 修复 lis3mdl 驱动中的 DRDY 中断
  * 新增 nxp kinetis 温度传感器驱动
  * 重构 ccs811 驱动
  * 修复 tmp007 驱动以使用 i2c_burst_read
  * 引入 sensor shell 模块
  * 新增 ms5607 驱动

* Serial

  * nRF UARTE 驱动支持仅 TX 模式，接收器永久禁用。
  * 在 uart_pl011 驱动中启用共享中断支持
  * 在 ns16550 驱动中实现 configure API
  * 移除 cc2650 驱动
  * 新增 async API 系统调用

* SPI

  * 在 sam 驱动中新增对 samv71 的支持
  * 在 sam0 驱动中新增对 same54 的支持
  * 在 DW 驱动中新增 PM 忙状态支持
  * 新增 Gecko SPI 驱动
  * 新增 mcux flexcomm 驱动

* Timer

  * 优化 64 位 RISC-V 上 MTIME/MTIMECMP 的读取
  * 新增每核心 ARM 架构定时器驱动
  * 在 sam0 rtc timer 驱动中新增对 same54 的支持

* USB

  * 新增对 SAMV71 SoC 的支持
  * 新增对 SAME54 SoC 的支持
  * 将 USB 设备支持扩展到所有 NXP IMX RT 板卡

* Video

  * N/A

* Watchdog

  * 新增 SiLabs Gecko 看门狗驱动
  * 新增系统调用
  * 修复 stm32 wwdg 启用时的回调调用

* WiFi

  * 重构 eswifi 和 simplelink 驱动中的卸载机制

网络
**********

* 新增配置 OpenThread Sleepy End Device (SED) 的支持
* 为 net_buf API 新增 64 位支持
* 新增对 IEEE 802.15.4 rf2xxx 驱动的支持
* 新增 TLS 安全重新协商支持
* 新增对 Timestamp 和 Record Route IPv4 选项的支持。
  它们仅用于 ICMPv4 Echo-Request 数据包。
* 新增示例云应用，演示如何连接到 Azure 云
* 为某些 LWM2M IPSO 对象新增可选时间戳资源
* 新增 poll() 支持，当设置 POLLOUT 时可立即返回
* 新增 PPP 支持以启用与 Windows 的连接建立
* 在 echo-server 示例应用中新增签名证书支持
* 新增处理多个同时 mDNS 请求的支持
* 新增对 SiLabs Giant Gecko GG11 以太网驱动的支持
* 新增对使用 PPP 连接到数据网络的通用 GSM modem 的支持
* 为 LWM2M 新增 UTC 偏移和时区支持
* 为 packet socket 新增 RX 时间统计支持
* 更新 IEEE 802.154 nrf5 驱动和 OpenThread 中的 ACK 处理
* 更新 MQTT PINGREQ 计数处理
* 更新 wpan_serial 示例以支持更多板卡
* 更新 Ethernet e1000 驱动调试打印
* 更新 OpenThread 以使用 settings 子系统
* 更新 IPv6 以在路由中使用接口前缀
* 更新 socket 卸载支持以支持多个已注册接口
* 修复等待网络接口启动时的检查
* 修复 zperf 示例在网络缓冲区耗尽时的问题
* 修复 PPP IPv4 控制协议（IPCP）处理
* 修复 native_posix 以太网驱动以更快读取数据
* 修复 PPP 选项处理
* 修复 MQTT 以更快关闭连接
* 修复 6lo 解压期间的内存损坏
* 修复 echo-server 示例应用 accept 处理
* 修复 Websocket 以小块接收数据
* 修复 Virtual LAN (VLAN) 支持，为网络接口添加链路本地地址
* 对新 TCP 协议栈实现的若干修复
* 移除 NATS 示例应用

CAN 总线
*******

* 通过第三方 CANopenNode 协议栈支持 CANopen 协议。
* 新增原生 ISO-TP 子系统。
* 引入 CAN-PRIMARY 别名。
* MCUX flexcan 的 SocketCAN。

蓝牙
*********

* Host:

  * GAP: 新增动态 LE 扫描监听 API
  * GAP: 为可连接广播和白名单发起者预分配连接对象
  * GAP: 多身份支持修复
  * GAP: RPA 超时处理修复
  * GAP: 新增远程版本信息
  * GATT: 为 cfg_write 回调新增返回值
  * L2CAP: 将通道处理移到系统工作队列
  * L2CAP: 基于信用流控制的多个修复
  * SMP: 新增 pairing_accept 回调
  * SMP: 修复 Security Manager 超时处理

* Mesh:

  * 新增对 Mesh 配置数据库的支持
  * Friendship 特性的多个修复
  * 新增发送分段控制消息的支持
  * 新增发送可靠模型发布消息的支持

* BLE 分离软件控制器:

  * 多个修复，包括通过认证所需的所有修复
  * 为没有内置地址解析支持的平台实现软件延迟隐私
  * 新增动态 TX 功率控制，包括一组读取和写入
    TX 功率的厂商特定命令
  * 新增 Kconfig 选项 BT_CTLR_PARAM_CHECK，以启用额外参数
    检查
  * 新增对 SMI（稳定调制指数）的基本支持
  * Ticker: 实现动态重新调度
  * Nordic: 切换为使用单一时钟设备进行时钟控制
  * openisa: 新增加密和解密支持

* BLE 旧版软件控制器:

  * 多个修复
  * 新增动态 TX 功率控制支持

USB 设备协议栈
****************

* Stack:

  * API: 新增用户设备状态回调支持
  * 重构切换到备用接口
  * 使 USB 描述符电源选项可配置
  * 从 HWINFO 派生 USB 设备序列号字符串（USB MSC 要求）
  * 将 USB 传输函数移到适当文件，为重构做准备
  * Windows 操作系统兼容性：使用 BOS 描述符时将 USB 版本设为 2.1
  * 将 VBUS 控制转换为新 GPIO API

* Classes:

  * CDC ACM: 内存和性能改进，IN 事务期间避免 ZLP
  * DFU: 在 DFU_UPLOAD 期间将上传长度限制为请求缓冲区大小
  * Loopback: 接口配置事件后重新触发 usb_write

构建与基础设施
************************

* Zephyr 构建系统和工具支持的最小 Python 版本
  现在为 3.6。
* 将 :file:`generated_dts_board.h` 和 :file:`generated_dts_board.conf` 重命名为
  :file:`devicetree.h` 和 :file:`devicetree.conf`，连同各种相关
  标识符。包含 :file:`generated_dts_board.h` 现在会生成警告，
  提示改为包含 :file:`devicetree.h`。

库/子系统
***********************

* LoRa

  * 通过官方 LoRaMac-node 参考实现新增了对 LoRa 的支持。

* Logging

  * 即时模式改进：更少的中断锁定、更好的 RTT 使用、
    从线程上下文记录日志。
  * 改进对缺失 log_strdup 的通知。

* mbedTLS 更新至 2.16.4

HAL
****

* HAL 现在作为外部模块移出主树，
  并位于它们自己的独立仓库中。

文档
*************

* settings: 将缺失的 API 子组纳入文档
* 新板卡和示例的文档。
* API 文档的改进和清晰度。

测试与示例
*****************

* 新增展示 settings 子系统 API 用法的示例

Issue 相关条目
*******************

自上次 2.1.0 标记版本以来，解决了以下 GitHub issue：

.. comment  List derived from GitHub Issue query: ...
   * :github:`issuenumber` - issue title

* :github:`23351` - boards: nucle_g474re: west flash doesn't work
* :github:`23321` - Bluetooth: LE SC OOB authentication in central connects using different RPA
* :github:`23310` - GUI: LVGL: possible NULL dereference
* :github:`23281` - UART console input does not work on SAM E5x
* :github:`23268` - Unnecessary privileged stacks with CONFIG_USERSPACE=y
* :github:`23244` - kernel.scheduler fails on frdmkw41z
* :github:`23231` - RISCV Machine Timer consistently interrupts long running system after soft reset
* :github:`23221` - status register value always reads 0x0000 in eth_mcux_phy_setup
* :github:`23209` - Bug in tls_set_credential
* :github:`23208` - Can not flash test images into up_squared board.
* :github:`23202` - Macro value for 10 bit ADC is wrong in MEC driver.
* :github:`23198` - rf2xx driver uses mutex in ISR
* :github:`23173` - west flash --nobuild,   west flash-signed
* :github:`23172` - Common west flash, debug arguments like --hex-file can't be used from command line
* :github:`23169` - "blinky" sample fails to build for BBC MicroBit (DT_ALIAS_LED0_GPIOS_CONTROLLER undefined)
* :github:`23168` - Toolchain docs: describe macOS un-quarantine procedure
* :github:`23165` - macOS setup fails to build for lack of "elftools" Python package
* :github:`23148` - bme280 sample does not compile
* :github:`23147` - tests/drivers/watchdog/wdt_basic_api failed on mec15xxevb_assy6853 board.
* :github:`23121` - Bluetooth: Mesh: Proxy servers only resends segments to proxy
* :github:`23110` - PTS: Bluetooth: GATT/SR/GAS/BV-07-C
* :github:`23109` - LL.TS Test LL/CON/SLA/BV-129-C fails (split)
* :github:`23072` - #ifdef __cplusplus missing in tracking_cpu_stats.h
* :github:`23069` - Bluetooth: controller: Assert in data length update procedure
* :github:`23050` - subsys/bluetooth/host/conn.c: conn->ref is not 0 after disconnected
* :github:`23047` - cdc_acm_composite sample doesn't catch DTR from second UART
* :github:`23035` - dhcpv4_client sample not working on sam e70
* :github:`23023` - Bluetooth: GATT CCC problem (GATT Server)
* :github:`23015` - Ongoing LL control procedures fails with must-expire latency (BT_CTLR_CONN_META)
* :github:`23004` - Can't use west to flash test images into up_squared board.
* :github:`23002` - unknown type name 'class'
* :github:`22999` - pend() assertion can allow user threads to crash the kernel
* :github:`22985` - Check if Zephyr is affected by SweynTooth vulnerabilities
* :github:`22982` - PTS: Test framework: Bluetooth: GATT/SR/GAS/BV-01-C,  GATT/SR/GAS/BV-07-C - BTP Error
* :github:`22979` - drivers: hwinfo: Build fails on some SoC
* :github:`22977` - ARM Cortex-M4 stack offset when not using Floating point register sharing
* :github:`22968` - Bluetooth: controller: LEGACY: ASSERTION failure on invalid packet sequence
* :github:`22967` - Bluetooth: controller: ASSERTION FAIL on invalid packet sequence
* :github:`22945` - Bluetooth: controller: ASSERTION FAIL Radio is on during flash operation
* :github:`22933` - k_delayed_work_submit_to_queue returns error code when resubmitting previously completed work.
* :github:`22931` - GPIO callback is not triggered for tests/drivers/gpio/gpio_basic_api on microchip mec15xxevb_assy6853 board
* :github:`22930` - PTS: Test Framework :Bluetooth: SM/MAS/PKE/BV-01-C INCONCLUSIV
* :github:`22929` - PTS: Test Framework :Bluetooth: SM/SLA/SIP/BV-01-C Error
* :github:`22928` - PTS: Test Framework: Bluetooth: SM/MAS/SIGN/BV-03-C, SM/MAS/SIGN/BI-01-C - INCONCLUSIV
* :github:`22927` - PTS: Test Framework: Bluetooth:  SM/MAS/SIP/BV-02-C-INCONCLUSIV
* :github:`22926` - Bluetooth: Cannot establish security and discover GATT when using Split LL
* :github:`22914` - tests/arch/arm/arm_irq_vector_table crashes for nRF5340
* :github:`22912` - [Coverity CID :208406] Macro compares unsigned to 0 in subsys/net/l2/ppp/ppp_l2.c
* :github:`22902` - eth_mcux_phy_setup called before ENET clock being enabled causes CPU to hang
* :github:`22893` - Problem using 3 instances of SPIM on NRF52840
* :github:`22890` - IP networking does not work on ATSAME70 Rev. B
* :github:`22888` - Can't flash test image into iotdk board.
* :github:`22885` - Sanitycheck timeout all test cases on mec15xxevb_assy6853 board.
* :github:`22874` - sanitycheck: when someone instance get stuck because of concurrent.futures.TimeoutErro exception, it always stuck
* :github:`22858` - WDT_DISABLE_AT_BOOT, if enabled by default, degrades functionality of the watchdog
* :github:`22855` - drivers: enc28j60: waits for wrong interrupt
* :github:`22847` - Test gpio_basic_api hangs on cc3220sf_launchxl
* :github:`22828` - kernel: fatal: interrupts left locked in TEST mode
* :github:`22822` - mesh: typo in condition in comp_add_elem of cfg_srv
* :github:`22819` - #define _current in kernel_structs.h leaks into global namespace
* :github:`22814` - mcuboot doesn't build with zephyr v2.1.0
* :github:`22803` - k_delayed_work_cancel documentation inconsistent with behavior
* :github:`22801` - Bluetooth: Split LL: Reconnection problem
* :github:`22786` - Bluetooth: SM/MAS/PROT/BV-01-C FAIL
* :github:`22784` - system hangs in settings_load() nrf52840 custom board
* :github:`22774` - Set USB version to 2.1 when CONFIG_USB_DEVICE_BOS is set
* :github:`22730` - CONFIG_BT_SETTINGS writes bt/hash to storage twice
* :github:`22722` - posix: redefinition of symbols while porting zeromq to zephyr
* :github:`22720` - armv8-m: userspace: some parts in userspace enter sequence need to be atomic
* :github:`22698` - log_stack_usage: prints err: missinglog_strdup()
* :github:`22697` - nrf52 telnet_shell panic. Mutex using in ISR.
* :github:`22693` - net: config: build break when CONFIG_NET_NATIVE=n
* :github:`22689` - driver: modem: sara-u2  error when connecting
* :github:`22685` - armv8-m: userspace: syscall return sequence needs to be atomic
* :github:`22682` - arm: cortex-a: no default board for testing
* :github:`22660` - gpio: legacy level interrupt disable API not backwards compatible
* :github:`22658` - [Coverity CID :208189] Self assignment in soc/xtensa/intel_apl_adsp/soc.c
* :github:`22657` - [Coverity CID :208191] Dereference after null check in subsys/canbus/isotp/isotp.c
* :github:`22656` - [Coverity CID :208192] Out-of-bounds access in tests/subsys/canbus/isotp/implementation/src/main.c
* :github:`22655` - [Coverity CID :208193] Unchecked return value in tests/bluetooth/mesh/src/microbit.c
* :github:`22654` - [Coverity CID :208194] Arguments in wrong order in tests/subsys/canbus/isotp/implementation/src/main.c
* :github:`22653` - [Coverity CID :208196] Out-of-bounds access in drivers/eeprom/eeprom_simulator.c
* :github:`22652` - [Coverity CID :208197] Pointless string comparison in tests/drivers/gpio/gpio_basic_api/src/main.c
* :github:`22651` - [Coverity CID :208198] Logical vs. bitwise operator in boards/xtensa/up_squared_adsp/bootloader/boot_loader.c
* :github:`22650` - [Coverity CID :208199] Arguments in wrong order in tests/subsys/canbus/isotp/conformance/src/main.c
* :github:`22649` - [Coverity CID :208200] Bad bit shift operation in drivers/interrupt_controller/intc_exti_stm32.c
* :github:`22648` - [Coverity CID :208201] Out-of-bounds write in soc/xtensa/intel_apl_adsp/soc.c
* :github:`22647` - [Coverity CID :208202] Arguments in wrong order in samples/subsys/canbus/isotp/src/main.c
* :github:`22646` - [Coverity CID :208203] Missing break in switch in drivers/interrupt_controller/intc_exti_stm32.c
* :github:`22645` - [Coverity CID :208204] Arguments in wrong order in samples/subsys/canbus/isotp/src/main.c
* :github:`22644` - [Coverity CID :208205] Improper use of negative value in tests/subsys/canbus/isotp/implementation/src/main.c
* :github:`22642` - [Coverity CID :208207] Arguments in wrong order in tests/subsys/canbus/isotp/conformance/src/main.c
* :github:`22641` - [Coverity CID :208208] Arguments in wrong order in tests/subsys/canbus/isotp/implementation/src/main.c
* :github:`22640` - [Coverity CID :208209] 'Constant' variable guards dead code in drivers/gpio/gpio_sx1509b.c
* :github:`22636` - Provide Linux-style IS_ERR()/PTR_ERR()/ERR_PTR() helpers
* :github:`22626` -  tests/drivers/counter/counter_basic_api failed on frdm_k64f board.
* :github:`22624` - tests/kernel/semaphore/semaphore failed on iotdk board.
* :github:`22623` - tests/kernel/timer/timer_api failed on mimxrt1050_evk board.
* :github:`22616` - Zephyr doesn't build if x86_64 SDK toolchain isn't install
* :github:`22584` - drivers: spi: spi_mcux_dspi: bus busy status ignored in async
* :github:`22563` - Common west flash/debug etc. arguments cannot be set in CMake
* :github:`22559` - crash in semaphore tests on ARC nsim_em and nsim_sem
* :github:`22557` - document guidelines/principles related to DT usage in Zephyr
* :github:`22556` - document DT macro generation rules
* :github:`22543` - No way to address a particular FTDI for OpenOCD
* :github:`22542` - GEN_ABSOLUTE_SYM cannot handle value larger than INT_MAX on qemu_x86_64
* :github:`22539` - bt_gatt: unable to save SC: no cfg left
* :github:`22535` - drivers: lora: Make the SX1276 driver independent of loramac module
* :github:`22534` - sanitycheck qemu_x86_coverage problem with SDK 0.11.1
* :github:`22532` - Doc build warning lvgl/README.rst
* :github:`22525` - stm32f7xx.h: No such file or directory
* :github:`22522` - GPIO test code tests/drivers/gpio/gpio_basic_api does not compile for microchip board mec15xxevb_assy6853
* :github:`22519` - sanitycheck failures for native_posix
* :github:`22514` - Bluetooth: gatt: CCC cfg not flushed if device was previously paired
* :github:`22510` - Build warnings in samples/net/cloud/google_iot_mqtt
* :github:`22489` - Request to enable CONFIG_NET_PKT_RXTIME_STATS for SOCK_RAW
* :github:`22486` - Do we have driver for Texas Instruments DRV2605 haptic driver for ERM and LRA actuators?
* :github:`22484` - Linker error when building google_iot_mqtt sample with zephyr-sdk 0.11.1
* :github:`22482` - Unable to use LOG_BACKEND_DEFINE macro from log_backend.h using C++
* :github:`22478` - Bluetooth - peripheral_dis - settings_runtime_set not working
* :github:`22474` - boards that have Kconfig warnings on hello_world.
* :github:`22466` - Add hx711 sensor
* :github:`22462` - onoff: why client must be reinitialized after each transition
* :github:`22455` - How to assign USB endpoint address manually in stm32f4_disco for CDC ACM class driver
* :github:`22452` - not driver found in can bus samples for olimexino_stm32
* :github:`22447` - samples: echo_client sample breaks for UDP when larger than net if MTU
* :github:`22444` - [Coverity CID :207963] Argument cannot be negative in tests/net/socket/websocket/src/main.c
* :github:`22443` - [Coverity CID :207964] Dereference after null check in subsys/canbus/canopen/CO_driver.c
* :github:`22442` - [Coverity CID :207965] Missing break in switch in drivers/i2c/i2c_ll_stm32_v1.c
* :github:`22440` - [Coverity CID :207970] Out-of-bounds access in samples/net/sockets/websocket_client/src/main.c
* :github:`22439` - [Coverity CID :207971] Negative array index read in subsys/net/l2/ppp/ipcp.c
* :github:`22438` - [Coverity CID :207973] Out-of-bounds access in tests/net/socket/websocket/src/main.c
* :github:`22437` - [Coverity CID :207974] Out-of-bounds read in tests/net/socket/websocket/src/main.c
* :github:`22436` - [Coverity CID :207975] Logically dead code in subsys/net/l2/ppp/ipcp.c
* :github:`22435` - [Coverity CID :207977] Logically dead code in subsys/canbus/canopen/CO_driver.c
* :github:`22434` - [Coverity CID :207978] Dereference after null check in subsys/canbus/canopen/CO_driver.c
* :github:`22433` - [Coverity CID :207980] Untrusted loop bound in tests/net/socket/websocket/src/main.c
* :github:`22432` - [Coverity CID :207982] Explicit null dereferenced in tests/lib/onoff/src/main.c
* :github:`22430` - [Coverity CID :207985] Argument cannot be negative in subsys/net/lib/websocket/websocket.c
* :github:`22424` - RFC: API Change: clock_control
* :github:`22417` - Build warnings with atsamr21_xpro
* :github:`22410` - arch: arm64: ARM64 port not working on real target
* :github:`22390` - Unable to build http_get with TLS enabled on cc32xx
* :github:`22388` - Build warnings in http_get on cc3220sf_launchxl
* :github:`22366` - Bug in sockets.c (subsys\net\lib\sockets)
* :github:`22363` - drivers: clock_control: clock_stm32_ll_h7.c Move Power Configuration code
* :github:`22360` - test_mqtt_disconnect in mqtt_pubsub fails
* :github:`22356` - An application hook for early init
* :github:`22343` - stm32f303 - irq conflict between CAN and USB
* :github:`22317` - samples/arc_secure_services fails on nsim_sem
* :github:`22316` - samples/philosophers coop_only scenario times out on nsim_sem and nsim_em
* :github:`22307` - net: ip: net_pkt_pull(): packet corruption when using CONFIG_NET_BUF_DATA_SIZE larger than 256
* :github:`22304` - ARM Cortex-M STMF401RE: execution too slow
* :github:`22299` - The file flash_stm32wbx.c generates compilation error
* :github:`22297` - nucleo_wb55rg:samples/bluetooth/peripheral/sample.bluetooth.peripheral fails to build on master
* :github:`22290` - ARC crashes due to concurrent system calls
* :github:`22280` - incorrect linker routing
* :github:`22275` - arm: cortex-R & M: CONFIG_USERSPACE: intermittent Memory region write access failures
* :github:`22272` - aggregated devicetree source file needs to be restored to build directory
* :github:`22268` - timer not working when duration is too high
* :github:`22265` - Simultaneous BLE pairings getting the same slot in keys structure
* :github:`22259` - Bluetooth: default value 80 on BT_ACL_RX_COUNT clamped to 64
* :github:`22258` - sanitycheck fails to merge OVERLAY_CONFIG properly
* :github:`22257` - test wdt_basic_api failed on nucleo_f746zg
* :github:`22245` - STM32G4xx: Wrong SystemCoreClock variable
* :github:`22243` - stm32g431rb: PLL setting result to slow exccution
* :github:`22210` - Bluetooth -  bt_gatt_get_value_attr_by_uuid
* :github:`22207` - Bluetooth ：Mesh：Provison init should after proxy
* :github:`22204` - CONFIG_BT_DEBUG_LOG vs atomic operations
* :github:`22202` - bt_rand() is called over HCI when BT_HOST_CRYPTO=y, even if BT_CTLR_LE_ENC=n
* :github:`22197` - dts: gen_defines.py bails out on new path property type
* :github:`22188` - drivers: espi: xec : eSPI driver should not send VWire SUS_ACK automatically in all cases
* :github:`22177` - Adafruit M0 boards are not set up to correctly flash in their code partitions
* :github:`22171` - West bossac runner inorrectly tries to include an offset parameter when flashing
* :github:`22128` - frdm_k82f:samples/drivers/spi_fujitsu_fram/sample.drivers.spi.fujitsu_fram fails
* :github:`22107` - mdns support with avahi as client
* :github:`22106` - intermittent emulator exit on samples/userspace/shared_mem on qemu_x86_64
* :github:`22088` - Bluetooth Mesh friendship is cleared due to no Friend response reception
* :github:`22086` - L2CAP/SMP: Race condition possible in native posix central when bonding.
* :github:`22085` - HCI/CCO/BV-07-C & HCI/GEV/BV-01-C failing in EDTT
* :github:`22066` - tests/kernel/mem_pool/mem_pool_threadsafe fails reliably on m2gl025_miv
* :github:`22062` - Adafruit Feather M0 does not flash correctly - incorrect flash code offset and bossa version incompatibility
* :github:`22060` - Build fails with gnuarmemb under windows
* :github:`22051` - Bluetooth Central: Discovery of 128bit primary service fails with later versions of gcc.
* :github:`22048` - Failing LL.TS Data Length Update Tests (split)
* :github:`22037` - qemu_cortex_r5 excludes too many tests
* :github:`22036` - sanitycheck for qemu_cortex_r5 fails
* :github:`22026` - west: openocd runner fails for boards without support/openocd.cfg
* :github:`22014` - RTC prescaler overflow on nRF(52)
* :github:`22010` - Bluetooth 'central' failure on native_posix
* :github:`22003` - 'central' failure on nrf52_pca10040
* :github:`21996` - Native POSIX or QEMU X86 emulation does not detect Bluetooth HCI Vendor-Specific Extensions
* :github:`21989` - websocket: recv_msg always returns full message length on last call
* :github:`21974` - make include hierarchy consistent with expected usage
* :github:`21970` - net: dns: mDNS resolving fails when responder is also enabled
* :github:`21967` - json: json_obj_parse will modify the input string
* :github:`21962` - drivers: usb: usb_dc_stm32: does not compile for stm32f3_disco board
* :github:`21949` - net: TCP: echo server deadlock from TCP packet
* :github:`21935` - SPI - STM32: transceive() should handle null tx buffer
* :github:`21917` - cmake error with CONFIG_COUNTER and CONFIG_BT both enabled (nrf52 board)
* :github:`21914` - net: dns: Answers to multiple mDNS queries sent in parallel aren't properly handled
* :github:`21888` - Print unmet Kconfig dependency
* :github:`21875` - sanitycheck warning for silabs,gecko-spi-usart.yaml
* :github:`21869` - IPv6 neighbors get added too eagerly
* :github:`21859` - Bluetooth LE Disconnect event not received
* :github:`21854` - HCI-UART: Bluetooth ACL data packets with 251 bytes not acknowledged
* :github:`21846` - RFC: API: Counter: counter_read() has no way of indicating failure
* :github:`21837` - net: socket: Add dependency to mbedtls
* :github:`21813` - tests/kernel/timer/timer_api failed on frdm_k64f board.
* :github:`21812` - tests/arch/arm/arm_irq_advanced_features failed on reel_board.
* :github:`21800` - Xtensa doesn't save SCOMPARE1 register on context switch
* :github:`21790` - tests/kernel/timer/timer_api fails on nucleo_g071rb board
* :github:`21789` - Merge topic-gpio back to master
* :github:`21784` - sanitycheck prints some build errors directly to the console
* :github:`21780` - OpenThread fails on nRF52840 Dongle (nrf52840_pca10059)
* :github:`21775` - echo_server and 802154 not build for NRF52811
* :github:`21768` - Make [CONFIG_NET_SOCKETS_SOCKOPT_TLS] dependent on [CONFIG_MBEDTLS] in menuconfig
* :github:`21764` - [SARA-R4] MQTT publisher not working - Impossible to connect to broker
* :github:`21763` - at86rf2xx radio driver does not report whether a TX was ACKed
* :github:`21756` - tests/kernel/obj_tracing failed on mec15xxevb_assy6853 board.
* :github:`21755` - tests/drivers/adc/adc_api  failed on  mec15xxevb_assy6853 board.
* :github:`21745` - tests: counter_basic_api: Failed on stm32 based boards
* :github:`21744` - dumb_http_server_mt with overlay-tls.conf does not connect
* :github:`21735` - ARM: Cortex-M: IRQ lock/unlock() API non-functional but accessible from user mode
* :github:`21716` - nucleo_g431rb: Hello world not working
* :github:`21715` - nucleo_g431rb: Blinky too slow / wrong clock setup?
* :github:`21713` - CDC ACM USB class issue with high transfer rate and ZLP
* :github:`21702` - [Coverity CID :206599] Out-of-bounds access in tests/bluetooth/uuid/src/main.c
* :github:`21700` - [Coverity CID :206606] Out-of-bounds access in tests/bluetooth/uuid/src/main.c
* :github:`21699` - [Coverity CID :206608] Dereference null return value in tests/net/icmpv4/src/main.c
* :github:`21695` - Documentation issues on v1.14-branch block backport
* :github:`21681` - nucleo_g431rb / STM32G4: Flashing works only once
* :github:`21679` - SPI broken on stm32f412 on master
* :github:`21676` - [Coverity CID :206389] Logically dead code in subsys/testsuite/ztest/src/ztest.c
* :github:`21674` - [Coverity CID :206392] Side effect in assertion in tests/kernel/timer/starve/src/main.c
* :github:`21673` - [Coverity CID :206393] Unintentional integer overflow in drivers/sensor/ms5607/ms5607.c
* :github:`21672` - [Coverity CID :206394] Logically dead code in subsys/testsuite/ztest/src/ztest.c
* :github:`21660` - Sample projects do not build for Nucleo WB55RG
* :github:`21659` - at86rf2xx radio driver not (reliably) sending ACKs
* :github:`21650` - _TEXT_SECTION_NAME_2 on ARM Cortex-R
* :github:`21637` - sanitycheck failed issue in parallel running.
* :github:`21629` - error with 'west update' on Windows 10
* :github:`21623` - DT: accept standard syntax for phandle in chosen node
* :github:`21618` - CI failing to complete tests
* :github:`21617` - Allow per module prj.conf
* :github:`21614` - host toolchain for x86 fails on empty CMAKE_C_FLAGS
* :github:`21607` - BME680 Sensor is not building
* :github:`21601` - '!radio_is_ready()' failed
* :github:`21599` - CONFIG_HEAP_MEM_POOL_SIZE and k_malloc, k_free not working in nrf51_pca10028
* :github:`21597` - sht3xd build error on olimexino_stm32
* :github:`21591` - Timeout error for the Microchip board during Sanitycheck
* :github:`21586` - Bluetooth Mesh fail to transmit messages after some time on nRF52840
* :github:`21581` - GNU ARM Embedded link broken in Getting Started
* :github:`21571` - CONFIG_BT_CENTRAL doesnot work fine with nrf51_pca10028
* :github:`21570` - how to select usb mps for SAME70 board
* :github:`21568` - mps2_an385:tests/kernel/tickless/tickless_concept/kernel.tickless.concept  fail
* :github:`21552` - Constant disconnects while attempting BT LE multi-central application.
* :github:`21551` - gpio: xec: GPIO Interrupt is not triggered for range GPIO240_276
* :github:`21546` - SPI broken for STM32L1
* :github:`21536` - tests/subsys/fs/fat_fs_api fails on native_posix_64
* :github:`21532` - can not build the image ,No targets specified and no makefile found
* :github:`21514` - Logging - strange behaviour with RTT on nRF53
* :github:`21510` - re-v
* :github:`21493` - System tick is not running
* :github:`21483` - sanitycheck messages in CI are not informative anymore
* :github:`21475` - sanitycheck: hardware map generation unexpected exit during the first attempt
* :github:`21466` - doc: extract_content.py not copying images in a table
* :github:`21450` - sample.net.cloud.google_iot_mqtt test is failing for frdm_k64f
* :github:`21448` - nrf52840 errata_98 / 89 mixup
* :github:`21443` - "HCI_USB" sample doesn't compile with "nucleo_wb55rg" board
* :github:`21438` - sanitycheck reports "FAILED: N/A" for failed or hung tests
* :github:`21432` - watchdog subsystem has no system calls
* :github:`21431` - missing async uart.h system calls
* :github:`21429` - Impossible to override syscalls
* :github:`21426` - civetweb triggers an error on Windows with Git 2.24
* :github:`21422` - Added nucleo-f767zi board support and would like to share
* :github:`21419` - RFC: API Change: usb: Make users call usb_enable. Provide global status callback.
* :github:`21418` - Crash when suspending system
* :github:`21410` - bt_ctlr_hci: Tx Buffer Overflow on LL/CON/MAS/BV-04-C, LL/CON/SLA/BV-05-C & LL/CON/SLA/BV-06-C
* :github:`21409` - sanitycheck: cmd.exe colorized output
* :github:`21385` - board frdm_kl25z build passed, but can't flash
* :github:`21384` - RFC: API Change: PWM: add support for inverted PWM signals
* :github:`21379` - Bluetooth: Mesh: Node Reset Not Clear Bind Key Information
* :github:`21375` - GATT: gatt_write_ccc_rsp with error (0x0e) removes always beginning from subscriptions head
* :github:`21365` - implicit casts in API headers must be replaced for C++ support
* :github:`21351` - tests/drivers/counter/counter_basic_api  failed on mimxrt1050_evk board.
* :github:`21341` - conditions required for safe call of kernel operations from interrupts
* :github:`21339` - Expired IPv6 router causes an infinite loop
* :github:`21335` - net: TCP: Socket echo server does not accept incoming connections when TLS is enabled
* :github:`21328` - Apparent network context leak with offloading driver (u-blox Sara r4)
* :github:`21325` - Where should the Digital-Input, Output, ADC driver be added?
* :github:`21321` - error update for project civetweb
* :github:`21318` - CONFIG_SYS_POWER_MANAGEMENT Makes Build Fail for nRF5340 and nRF9160
* :github:`21317` - intermittent SMP crashes on x86_64
* :github:`21306` - ARC: syscall register save/restore needs backport to 1.14
* :github:`21301` - Coverage report generated for qemu_x86 board is incomplete
* :github:`21300` - pyocd flash failing on bbc_microbit
* :github:`21299` - bluetooth: Controller does not release buffer on central side after peripheral reset
* :github:`21290` - Compiler warnings in flash.h: invalid conversion from 'const void*' to 'const flash_driver_api*'
* :github:`21281` - logging: msg_free may erroneously call log_free
* :github:`21278` - How to use pwm in nrf52832 for rgb led
* :github:`21275` - kl2x soc fixup is missing I2C_1 labels
* :github:`21257` - tests/net/net_pkt failed on mimxrt1050_evk board.
* :github:`21240` - Error west flash
* :github:`21229` - cc1plus: warning: '-Werror=' argument '-Werror=implicit-int' is not valid for C++
* :github:`21202` - Required upgrade of HAL
* :github:`21186` - Gatt discover callback gives invalid pointer to primary and secondary service UUID.
* :github:`21185` - zero-latency IRQ behavior is not documented?
* :github:`21181` - devicetree should support making properties with defaults required
* :github:`21177` - Long ATT MTU reports wrong length field in write callback.
* :github:`21171` - Module Request: Optiga Trust X
* :github:`21167` - libraries.libc.newlib test fails
* :github:`21165` - Bluetooth: Mesh: Friend Clear message from a Friend node
* :github:`21162` - Sanitycheck corrupted test case names in test-report.xml files
* :github:`21161` - question: openthread with other boards
* :github:`21148` - nrf51: uart_1 does not compile
* :github:`21139` - west: runners: blackmagicprobe: Keyboard Interrupt shouldn't kill the process
* :github:`21131` - Bluetooth: host: Subscriptions not removed upon unpair
* :github:`21126` - drivers: spi_nrfx_spim: Incorrect handling of extended SPIM configuration
* :github:`21123` - sanitycheck halt some test cases with parallel running.
* :github:`21121` - netusb: RNDIS host support
* :github:`21115` - Request a new repository for the Xtensa HAL
* :github:`21105` - Bluetooth API called before finished initialization.
* :github:`21103` - Bluetooth: host: Reduce overhead of GATT subscriptions
* :github:`21099` - echo server qemu_x86 e1000 cannot generate coverage reports
* :github:`21095` - [Coverity CID :206086] Out-of-bounds access in drivers/timer/cortex_m_systick.c
* :github:`21094` - native_posix doesn't call main function that's defined in C++
* :github:`21082` - tests/kernel/timer/timer_api failing on several nRF5x SoCs
* :github:`21074` - Enhance 802.1Qav documentation
* :github:`21058` - BLE: Enable/Disable Automatic sending of Connection Parameter update request on Timeout.
* :github:`21057` - BLE: No Valid Parameter check in send_conn_le_param_update()
* :github:`21045` - log_backend.h missing include for UTIL_CAT in LOG_BACKEND_DEFINE macro
* :github:`21036` - Add SMP function similar to bt_conn_get_info
* :github:`21025` - sam_e70_xplained reboots after 35secs
* :github:`20981` - mempool: MPU fault
* :github:`20974` - file resources exceeded with sanitycheck
* :github:`20953` - usb: nrf: usb on reel board becomes unavailable if USB cable is not connected at first
* :github:`20927` - ztest_1cpu_user_unit_test() doesn't work
* :github:`20915` - doc: Kconfig section in board_porting.rst should be moved or removed
* :github:`20904` - kernel.timer.tickless is failed due to missing TEST_USERSPACE flag
* :github:`20886` - [Coverity CID :205826] Memory - corruptions in tests/subsys/fs/nffs_fs_api/common/nffs_test_utils.c
* :github:`20885` - [Coverity CID :205819] Memory - corruptions in tests/subsys/fs/nffs_fs_api/common/nffs_test_utils.c
* :github:`20884` - [Coverity CID :205799] Memory - corruptions in tests/subsys/fs/nffs_fs_api/common/nffs_test_utils.c
* :github:`20877` - [Coverity CID :205823] Null pointer dereferences in tests/kernel/fifo/fifo_timeout/src/main.c
* :github:`20802` - reschedule not done after mutex unlock
* :github:`20770` - irq locking in logging backend can cause missing interrupts
* :github:`20755` - mcuboot: add as module and verify functionality
* :github:`20749` - samples:sample.net.dns_resolve.mdns:frdmk64f ipv4dns handler has not result
* :github:`20748` - build warnings on lpcxpresso54114_m0/m4 board
* :github:`20746` - Bluetooth: Mesh: Friend node Adding another Friend Update
* :github:`20724` - Packed pointer warning in LL Controller
* :github:`20698` - Bluetooth: host: Skip pre-scan done by bt_conn_create_le if not needed
* :github:`20697` - Confusing warning during cmake
* :github:`20673` - guiconfig not working properly?
* :github:`20640` -  Bluetooth: l2cap do not recover when faced with long packets and run out of buffers
* :github:`20629` - when CONFIG_BT_SETTINGS is enabled, stack stores id in flash memory each power up of device (call to bt_enable)
* :github:`20618` - Can unicast address be relayed when send message over gatt proxy?
* :github:`20576` - DTS overlay files must include full path name
* :github:`20561` - Crypto API: Separate IV from ciphertext based on struct cipher_ctx::flags
* :github:`20535` - [Coverity CID :205619]Null pointer dereferences in /tests/net/ieee802154/fragment/src/main.c
* :github:`20497` - [Coverity CID :205638]Integer handling issues in /drivers/pwm/pwm_mchp_xec.c
* :github:`20490` - [Coverity CID :205651]Uninitialized variables in /drivers/dma/dma_stm32.c
* :github:`20484` - Tests/kernel/gen_isr_table failing when enabling WDT driver
* :github:`20426` - sensors: grove temperature and light drivers out of date
* :github:`20414` - nRF51 issues with the split link layer
* :github:`20411` - samples: lis3mdl trigger not working with x_nucleo_iks01a1
* :github:`20388` - Allow for runtime reconfiguration of SPI master / slave
* :github:`20355` - west build for zephyr/samples/net/sockets/echo_server/ on qemu_xtensa target outputs elf with panic
* :github:`20315` - zperf TCP uploader fails
* :github:`20286` - Problem building for ESP32
* :github:`20278` - Something is wrong when trying ST7789V sample
* :github:`20264` - Bluetooth: Delay advertising events instead of dropping them on collision
* :github:`20256` - settings subsystem sample
* :github:`20217` - Extend qemu_cortex_r5 test coverage
* :github:`20172` - devicetree support for compound elements
* :github:`20161` - Facing issue to setup zephyr on ubuntu
* :github:`20153` - BLE small throughput
* :github:`20140` - CMake: syscall macro's are not generated for out of tree DTS_ROOT
* :github:`20125` - Add system call to enter low power mode and reduce latency for deep sleep entry
* :github:`20026` - sanitycheck corrupts stty in some cases
* :github:`20017` - Convert GPIO users to new GPIO API
* :github:`19982` - Periodically wake up log process thread consume more power
* :github:`19922` - Linear time to give L2CAP credits
* :github:`19869` - Implement tickless capability for xlnx_psttc_timer
* :github:`19761` - tests/net/ieee802154/fragment failed on reel board.
* :github:`19737` - No Function In Zephyr For Reading BLE Channel Map?
* :github:`19666` - remove kernel/include and ``arch/*/include`` from default include path
* :github:`19643` - samples/boards/arc_secure_services fails on nsim_sem
* :github:`19545` - usb: obtain configuration descriptor's bmAttributes and bMaxPower from DT
* :github:`19540` - Allow running and testing network samples in automatic way
* :github:`19492` - sanitycheck: unreliable/inconsistent catch of ASSERTION FAILED
* :github:`19488` - Reference and sample codes to get started with the friendship feature in ble mesh
* :github:`19473` - Missing NULL parameter check in k_pipe_get
* :github:`19361` - BLE Scan fails to start when running in parallel with BLE mesh
* :github:`19342` - Bluetooth: Mesh: Persistent storage of Virtual Addresses
* :github:`19245` - Logging: Assert with LOG_IMMEDIATE
* :github:`19100` - LwM2M sample with DTLS: does not connect
* :github:`19053` - 2.1 Release Checklist
* :github:`18962` - [Coverity CID :203909]Memory - corruptions in /subsys/mgmt/smp_shell.c
* :github:`18867` - zsock_poll() unnecessarily wait when querying for ZSOCK_POLLOUT
* :github:`18852` - west flash fails for cc1352r_launchxl
* :github:`18635` - isr4 repeatedly gets triggered after test passes in tests/kernel/gen_isr_table
* :github:`18583` - hci_usb: NRF52840 connecting addtional peripheral fails
* :github:`18551` - address-of-temporary idiom not allowed in C++
* :github:`18530` - Convert GPIO drivers to new GPIO API
* :github:`18483` - Bluetooth: length variable inconsistency in keys.c
* :github:`18452` - [Coverity CID :203463]Memory - corruptions in /tests/lib/ringbuffer/src/main.c
* :github:`18447` - [Coverity CID :203400]Integer handling issues in /tests/lib/fdtable/src/main.c
* :github:`18410` - [Coverity CID :203448]Memory - corruptions in /subsys/net/lib/lwm2m/ipso_onoff_switch.c
* :github:`18378` - [Coverity CID :203537]Error handling issues in /samples/subsys/nvs/src/main.c
* :github:`18280` - tests/drivers/adc/adc_api fails on frdmkl25z
* :github:`18173` - ARM: Core Stack Improvements/Bug fixes for 2.1 release
* :github:`18169` - dts: bindings: inconsistent file names and base.yaml include of general device controllers
* :github:`18137` - Add section on IRQ generation to doc/guides/dts/index.rst
* :github:`17852` - Cmsis_rtos_v2_apis test failed on iotdk board.
* :github:`17838` - state DEVICE_PM_LOW_POWER_STATE of Device Power Management
* :github:`17787` - openocd unable to flash hello_world to cc26x2r1_launchxl
* :github:`17731` - Dynamically set TX power of BLE Radio
* :github:`17689` - On missing sensor, Init hangs
* :github:`17543` - dtc version 1.4.5 with ubuntu 18.04 and zephyr sdk-0.10.1
* :github:`17310` - boards: shields: use Kconfig.defconfig system for shields
* :github:`17309` - enhancements to device tree generation
* :github:`17102` - RFC: rework GPIO interrupt configuration
* :github:`16935` - Zephyr doc website: Delay search in /boards to the end of the search.
* :github:`16851` - west flash error on zephyr v1.14.99
* :github:`16735` - smp_svr sample does not discover services
* :github:`16545` - west: diagnose dependency version failures
* :github:`16482` - mcumgr seems to compromise BT security
* :github:`16472` - tinycrypt ecc-dh and ecc-dsa should not select entropy generator
* :github:`16329` - ztest teardown function not called if test function is interrupted
* :github:`16239` - Build: C++ compiler warning '-Wold-style-definition'
* :github:`16235` - STM32: Move STM32 Flash driver to CMSIS STM32Cube definitions
* :github:`16232` - STM32: implement pinmux api
* :github:`16202` - Improve help for west build target
* :github:`16034` - Net packet size of 64 bytes doesn't work.
* :github:`16023` - mcuboot: enabling USB functionality in MCUboot crashes zephyr application in slot0
* :github:`16011` - Increase coverage of tests
* :github:`15906` - WEST ERROR: extension command build was improperly defined
* :github:`15841` - Support AT86RF233
* :github:`15729` - flash: should write_protection be emulated?
* :github:`15657` - properly define kernel <--> arch APIs
* :github:`15611` - gpio/pinctrl: GPIO and introduce PINCTRL API to support gpio, pinctrl DTS nodes
* :github:`15593` - How to use gdb to view the stack of a thread
* :github:`15580` - SAMD21 Adafruit examples no longer run on boards
* :github:`15435` - device fails to boot when spi max frequency set above 1000000
* :github:`15278` - CANopen Support
* :github:`15229` - network tests have extremely restrictive whitelist
* :github:`15171` - BLE Throughput
* :github:`14927` - checkpatch: not expected behavior for multiple git commit check.
* :github:`14922` - samples/boards/altera_max10/pio: Error configuring GPIO PORT
* :github:`14753` - nrf52840_pca10056: Leading spurious 0x00 byte in UART output
* :github:`14668` - net: icmp4: Zephyr strips record route and time stamp options
* :github:`14650` - missing system calls in Counter driver APIs
* :github:`14639` - All tests should be SMP-safe
* :github:`14632` - Default for TLS_PEER_VERIFY socket option are set to required, may lead to confusion when running samples against self-signed certs
* :github:`14621` - BLE controller: Add support for Controller(SW deferred)-based Privacy
* :github:`14287` - USB HID Get_Report and Set_Report
* :github:`14206` - user mode documentation enhancements
* :github:`13991` - net: Spurious driver errors due to feeding packets into IP stack when it's not fully initialized (assumed reason)
* :github:`13943` - net: QEMU Ethernet drivers are flaky (seemingly after "net_buf" refactor)
* :github:`13941` - Alternatives for OpenThread settings
* :github:`13894` - stm32f429i_disc1: Add DTS for USB controller
* :github:`13403` - USBD event and composite-device handling
* :github:`13232` - native_posix doc: Add mention of virtual USB
* :github:`13151` - Update documentation on linking Zephyr within a flash partition
* :github:`12968` - dfu/mcuboot: solution for Set pending: don't crash when image slot corrupt
* :github:`12860` - No test builds these files
* :github:`12814` - TCP connet Net Shell function seems to not working when using NET_SOCKETS_OFFLOAD
* :github:`12635` - tests/subsys/fs/nffs_fs_api/common/nffs_test_utils.c fail with Assertion failure on nrf52840
* :github:`12553` - List of tests that keep failing sporadically
* :github:`12537` - potential over-use of k_spinlock
* :github:`12490` - Produced ELF does not follow the linux ELF spec
* :github:`12359` - Default address selection for IPv6 should follow RFC 6724
* :github:`12331` - Proposal to improve the settings subsystem
* :github:`12134` - I cannot see a Zephyr way to change the clock frequency at runtime
* :github:`12130` - Is zephyr targeting high-end phone or pc doing open ended computation on the roadmap?
* :github:`12027` - Make icount work for real on x86_64
* :github:`11751` - Rework exception & fatal error handling framework
* :github:`11519` - Add at least build test for cc1200
* :github:`11490` - setup_ipv6() treats event enums as bitmasks
* :github:`11296` - Possible ways to implement clock synchronisation over BLE
* :github:`11213` - NFFS: Handle unexpected Power Off
* :github:`11172` - ARM Cortex A Architecture support - ARMv8-A
* :github:`10996` - Add device tree support for usb controllers on x86
* :github:`10821` - ELCE: DT, Kconfig, EDTS path forward
* :github:`10534` - Can we get rid of zephyr-env.sh?
* :github:`10423` - log_core.h error on pointer-to-int-cast on 64bit system
* :github:`10339` - gpio: Cleanup flags
* :github:`10305` - RFC: Add pin mask for gpio_port_xxx
* :github:`9947` - CMake build architecture documentation
* :github:`9904` - System timer handling with low-frequency timers
* :github:`9873` - External flash driver for the MX25Rxx
* :github:`9748` - NFFS issue after many writes by btsettings
* :github:`9506` - Ztest becomes unresponsive while running SMP tests
* :github:`9349` - Support IPv6 privacy extension RFC 4941
* :github:`9333` - Support for STM32 L1-series
* :github:`9330` - network: clean up / implement supervisor to manage net services
* :github:`9194` - generated syscall header files don't have ifndef protection
* :github:`8833` - OpenThread: Minimal Thread Device (MTD) option is not building
* :github:`8539` - Categorize Kconfig options in documentation
* :github:`8262` - [Bluetooth] MPU FAULT on sdu_recv
* :github:`8242` - File system (littlefs & FAT) examples
* :github:`8236` - DTS Debugging is difficult
* :github:`7305` - CMake improvements to modularize gperf targets
* :github:`6866` - build: requirements: No module named yaml and elftools
* :github:`6562` - Question: Is QP™ Real-Time Frameworks/RTOS or libev supported in Zephyr? Or any plan?
* :github:`6521` - Scheduler needs spinlock-based synchronization
* :github:`6496` - Question: Is dynamical module loader supported in Zephyr? Or any plan?
* :github:`6389` - OpenThread: otPlatRandomGetTrue() implementation is not up to spec, may lead to security issues
* :github:`6327` - doc: GPIO_INT config option dependencies aren't clear
* :github:`6293` - Refining Zephyr's Device Driver Model
* :github:`6157` - SMP lacks low-power idle
* :github:`6084` - api: pinmux/gpio: It isn't possible to set pins as input and output simultaneously
* :github:`5943` - OT: utilsFlashWrite does not take into account the write-block-size
* :github:`5695` - C++ Support doesn't work
* :github:`5436` - Add LoRa Radio Support
* :github:`5027` - Enhance Testing and Test Coverage
* :github:`4973` - Provide Linux-style ERR_PTR/PTR_ERR/IS_ERR macros
* :github:`4951` - Prevent full rebuilds on Kconfig changes
* :github:`4917` - Reintroduce generic "outputexports" target after CMake migration
* :github:`4830` - device tree: generate pinmux
* :github:`3943` - x86: scope SMAP support in Zephyr
* :github:`3866` - To optimize the layout of the meta data of mem_slab & mem_pool
* :github:`3810` - application/kernel rodata split
* :github:`3717` - purge linker scripts of macro-based meta-language
* :github:`3701` - xtensa: scope MPU enabling
* :github:`3636` - Define region data structures exposed by linker script
* :github:`3490` - Move stm32 boards dts file to linux dts naming rules
* :github:`3488` - Dissociate board names from device tree file names
* :github:`3469` - Unify flash and code configuration across targets
* :github:`3429` - Add TSL2560 ambient light sensor driver
* :github:`3428` - Add HTU21D humidity sensor driver
* :github:`3427` - Add MPL3115A2 pressure sensor driver
* :github:`3397` - LLDP: Implement local MIB support for optional TLVs
* :github:`3276` - Dynamic Frequency Scaling
* :github:`3156` - xtensa: Support C++
* :github:`3098` - extend tests/kernel/arm_irq_vector_table to other platforms
* :github:`3044` - How to create a Zephyr ROM library
* :github:`2925` - cross-platform support for interrupt tables/code in RAM or ROM
* :github:`2814` - Add proper support for running Zephyr without a system clock
* :github:`2807` - remove sprintf() and it's brethen
* :github:`2664` - Running SanityCheck in Windows
* :github:`2338` - ICMPv6 "Packet Too Big" support
* :github:`2307` - DHCPv6
* :github:`1903` - Wi-Fi Host Stack
* :github:`1897` - Thread over BLE
* :github:`1583` - NFFS requires 1-byte unaligned accesses to flash
* :github:`1511` - qemu_nios2 should use the GHRD design
* :github:`1468` - Move NATS support from sample to a library + API
* :github:`1205` - C++ usage
