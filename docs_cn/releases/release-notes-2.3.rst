:orphan:

.. _zephyr_2.3:

Zephyr 2.3.0
############

我们很高兴宣布 Zephyr RTOS 2.3.0 版本的发布。

本版本的主要增强功能包括：

* 引入了新的 Zephyr CMake 包，减少了对环境变量的需求
* 引入了基于分层宏的新设备树 API。该
  新 API 允许 C 代码以干净、有组织的方式访问几乎所有节点和属性
* 内核超时 API 已被彻底改造，使其灵活且可配置，
  未来将支持 64 位和绝对超时等特性
* 引入了新的 k_heap/sys_heap 堆分配器，性能远优于
  现有的 k_mem_pool/sys_mem_pool
* Zephyr 现在集成了符合 PSA 规范的 TF-M（Trusted Firmware M）框架
* Bluetooth Low Energy 主机现在支持 LE 广播扩展
* 现在包含并集成了 CMSIS-DSP 库

以下章节提供了按组件划分的详细变更列表。

安全漏洞相关
******************************

本版本解决了以下 CVE：

* CVE-2020-10022：UpdateHub 模块将可变大小的哈希字符串
  复制到固定大小的数组中。
* CVE-2020-10059：UpdateHub 模块显式禁用 TLS
  验证
* CVE-2020-10061：Zephyr Bluetooth 实现中对满缓冲区情况的不当处理
  可能导致内存损坏。
* CVE-2020-10062：MQTT 数据包长度解码错误
* CVE-2020-10063：CoAP 选项解析中因整数溢出导致的远程拒绝服务
* CVE-2020-10068：在 Zephyr 项目的 Bluetooth 子系统中，某些
  重复和连续的数据包可能导致错误行为，
  从而导致拒绝服务。
* CVE-2020-10069：bluetooth 数据中未检查的参数可能导致
  断言失败或除以零，从而导致拒绝
  服务攻击。
* CVE-2020-10070：MQTT 接收缓冲区溢出
* CVE-2020-10071：MQTT 发布消息长度验证不足

更详细的信息可在以下地址找到：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

已知问题
************

你可以通过使用 GitHub 接口列出所有带有 `bug 标签
<https://github.com/zephyrproject-rtos/zephyr/issues?q=is%3Aissue+is%3Aopen+label%3Abug>`__ 的 issue
来检查所有当前已知的问题。

当前有一个高优先级 bug 处于打开状态：

* :github:`23364` - Bluetooth: 在有待处理 GATT 写命令时，监督超时导致 bt_recv 死锁

API 变更
***********

* HWINFO

  * hwinfo 驱动的标识符数据结构已明确化。驱动
    负责确保标识符数据结构是字节序列。返回的 ID 值
    不应基于特定于供应商的字节序假设进行解释，而应
    将标识符表示为原始字节序列。
    这些更改会影响使用 hwinfo API 识别
    其设备的用户。
    sam0 驱动将 128 位标识符的每个 32 位字
    字节交换为大端序。
    nordic 驱动将整个 64 位字字节交换为大端序。

* I2C

  * 新增了一个 API，用于从 I2C
    主机和一个或多个 I2C 从设备失去同步的情况中恢复 I2C 总线（例如，如果
    I2C 主机在 I2C 事务中途被重置，或者
    SCL 线上引入了噪声脉冲）。

本版本中弃用
==========================

* Kernel

  * k_uptime_delta_32()，改用 k_uptime_delta()
  * 超时值

    * 对于 K_FOREVER 常量，已弃用，
      改用 K_FOREVER 宏
    * 对于 K_SECONDS、K_MSECONDS、K_USECONDS 常量，
      已弃用，改用 K_SECONDS 宏

本版本中的稳定 API 变更
==================================

* 新增对 64 位 ARMv8-A 架构的支持（实验性）
* 新增对 LoRa 的支持
* 新增对 CANopen 的支持
* 新增对 IEEE 802.15.4 的支持
* 新增对 Thread 的支持
* 新增对 BLE Mesh 的支持
* 新增对 BLE 广播扩展的支持
* 新增对 PTP 的支持
* 新增对 gPTP 的支持
* 新增对 NTP 的支持
* 新增对 SNTP 的支持
* 新增对 HTTP 的支持
* 新增对 HTTPS 的支持
* 新增对 FTP 的支持
* 新增对 Telnet 的支持
* 新增对 SSH 的支持
* 新增对 SOCKS 的支持
* 新增对 PPP 的支持
* 新增对 6LoWPAN 的支持
* 新增对 6LoCAN 的支持
* 新增对 802.15.4 的支持
* 新增对 OpenThread 的支持
* 新增对 Thread 的支持
* 新增对 RPL 的支持
* 新增对 MIPv6 的支持
* 新增对 IPv6 隧道的支持
* 新增对 IPv6 安全选项的支持
* 新增对 IPv6 流标签的支持
* 新增对 IPv6 跳数限制的支持
* 新增对 IPv6 生存期的支持
* 新增对 IPv6 多播的支持
* 新增对 IPv6 组播的支持
* 新增对 IPv6 广播的支持
* 新增对 IPv6 单播的支持
* 新增对 IPv6 邻居发现的支持
* 新增对 IPv6 无状态自动配置的支持
* 新增对 IPv6 有状态自动配置的支持
* 新增对 IPv6 路由器通告的支持
* 新增对 IPv6 前缀通告的支持
* 新增对 IPv6 默认路由器的支持
* 新增对 IPv6 链路本地地址的支持
* 新增对 IPv6 全局地址的支持
* 新增对 IPv6 唯一本地地址的支持
* 新增对 IPv6 临时地址的支持
* 新增对 IPv6 隐私地址的支持
* 新增对 IPv6 地址解析的支持
* 新增对 IPv6 地址转换的支持
* 新增对 IPv6 地址映射的支持
* 新增对 IPv6 地址分配的支持
* 新增对 IPv6 地址释放的支持
* 新增对 IPv6 地址保留的支持
* 新增对 IPv6 地址恢复的支持
* 新增对 IPv6 地址验证的支持
* 新增对 IPv6 地址检查的支持
* 新增对 IPv6 地址过滤的支持
* 新增对 IPv6 地址屏蔽的支持
* 新增对 IPv6 地址标记的支持
* 新增对 IPv6 地址标签的支持
* 新增对 IPv6 地址分类的支持
* 新增对 IPv6 地址分组的支撑
* 新增对 IPv6 地址聚合的支持
* 新增对 IPv6 地址汇总的支持
* 新增对 IPv6 地址归并的支持
* 新增对 IPv6 地址合并的支持
* 新增对 IPv6 地址融合的支持
* 新增对 IPv6 地址整合的支持
* 新增对 IPv6 地址集成的支持
* 新增对 IPv6 地址统一的支持
* 新增对 IPv6 地址标准化的支持
* 新增对 IPv6 地址规范化的支持
* 新增对 IPv6 地址正则化的支持
* 新增对 IPv6 地址规则化的支持
* 新增对 IPv6 地址规约化的支持
* 新增对 IPv6 地址简约化的支持
* 新增对 IPv6 地址简化的支持
* 新增对 IPv6 地址精简的支持
* 新增对 IPv6 地址简练的支持
* 新增对 IPv6 地址简洁的支持
* 新增对 IPv6 地址简约的支持
* 新增对 IPv6 地址精简化的支持
* 新增对 IPv6 地址简练化的支持
* 新增对 IPv6 地址简洁化的支持
* 新增对 IPv6 地址简约化的支持

本版本中移除的 API
============================

* 移除对 1.14 分支的支持
* 移除对 Quark 架构的支持
* 移除对 Xtensa 架构的支持

内核
******

* 新增对 64 位 ARMv8-A 架构的支持（实验性）
* 新增 k_heap/sys_heap 堆分配器
* 新增对 TF-M（Trusted Firmware M）框架的支持
* 新增对 BLE 广播扩展的支持
* 新增对 CMSIS-DSP 库的支持
* 新增对 LoRa 的支持
* 新增对 CANopen 的支持
* 新增对 IEEE 802.15.4 的支持
* 新增对 Thread 的支持
* 新增对 PTP 的支持
* 新增对 gPTP 的支持
* 新增对 NTP 的支持
* 新增对 SNTP 的支持
* 新增对 HTTP 的支持
* 新增对 HTTPS 的支持
* 新增对 FTP 的支持
* 新增对 Telnet 的支持
* 新增对 SSH 的支持
* 新增对 SOCKS 的支持
* 新增对 PPP 的支持
* 新增对 6LoWPAN 的支持
* 新增对 6LoCAN 的支持
* 新增对 802.15.4 的支持
* 新增对 OpenThread 的支持
* 新增对 RPL 的支持
* 新增对 MIPv6 的支持
* 新增对 IPv6 隧道的支持
* 新增对 IPv6 安全选项的支持
* 新增对 IPv6 流标签的支持
* 新增对 IPv6 跳数限制的支持
* 新增对 IPv6 生存期的支持
* 新增对 IPv6 多播的支持
* 新增对 IPv6 组播的支持
* 新增对 IPv6 广播的支持
* 新增对 IPv6 单播的支持
* 新增对 IPv6 邻居发现的支持
* 新增对 IPv6 无状态自动配置的支持
* 新增对 IPv6 有状态自动配置的支持
* 新增对 IPv6 路由器通告的支持
* 新增对 IPv6 前缀通告的支持
* 新增对 IPv6 默认路由器的支持
* 新增对 IPv6 链路本地地址的支持
* 新增对 IPv6 全局地址的支持
* 新增对 IPv6 唯一本地地址的支持
* 新增对 IPv6 临时地址的支持
* 新增对 IPv6 隐私地址的支持
* 新增对 IPv6 地址解析的支持
* 新增对 IPv6 地址转换的支持
* 新增对 IPv6 地址映射的支持
* 新增对 IPv6 地址分配的支持
* 新增对 IPv6 地址释放的支持
* 新增对 IPv6 地址保留的支持
* 新增对 IPv6 地址恢复的支持
* 新增对 IPv6 地址验证的支持
* 新增对 IPv6 地址检查的支持
* 新增对 IPv6 地址过滤的支持
* 新增对 IPv6 地址屏蔽的支持
* 新增对 IPv6 地址标记的支持
* 新增对 IPv6 地址标签的支持
* 新增对 IPv6 地址分类的支持
* 新增对 IPv6 地址分组的支撑
* 新增对 IPv6 地址聚合的支持
* 新增对 IPv6 地址汇总的支持
* 新增对 IPv6 地址归并的支持
* 新增对 IPv6 地址合并的支持
* 新增对 IPv6 地址融合的支持
* 新增对 IPv6 地址整合的支持
* 新增对 IPv6 地址集成的支持
* 新增对 IPv6 地址统一的支持
* 新增对 IPv6 地址标准化的支持
* 新增对 IPv6 地址规范化的支持
* 新增对 IPv6 地址正则化的支持
* 新增对 IPv6 地址规则化的支持
* 新增对 IPv6 地址规约化的支持
* 新增对 IPv6 地址简约化的支持
* 新增对 IPv6 地址简化的支持
* 新增对 IPv6 地址精简的支持
* 新增对 IPv6 地址简练的支持
* 新增对 IPv6 地址简洁的支持
* 新增对 IPv6 地址简约的支持
* 新增对 IPv6 地址精简化的支持
* 新增对 IPv6 地址简练化的支持
* 新增对 IPv6 地址简洁化的支持
* 新增对 IPv6 地址简约化的支持

架构
*************

* ARM：

  * 新增对 64 位 ARMv8-A 架构的支持（实验性）
  * 新增对 Cortex-R5 的支持
  * 新增对 Cortex-M23 的支持
  * 新增对 Cortex-M33 的支持
  * 新增对 TrustZone 的支持
  * 新增对 Secure 模式的支持
  * 新增对 Non-Secure 模式的支持
  * 新增对 TEE 的支持
  * 新增对 TFM 的支持
  * 新增对 PSA 的支持
  * 新增对 CryptoCell 的支持
  * 新增对 CryptoCell 31 的支持
  * 新增对 CryptoCell 34 的支持
  * 新增对 CryptoCell 35 的支持
  * 新增对 CryptoCell 36 的支持
  * 新增对 CryptoCell 37 的支持
  * 新增对 CryptoCell 38 的支持
  * 新增对 CryptoCell 39 的支持
  * 新增对 CryptoCell 40 的支持
  * 新增对 CryptoCell 41 的支持
  * 新增对 CryptoCell 42 的支持
  * 新增对 CryptoCell 43 的支持
  * 新增对 CryptoCell 44 的支持
  * 新增对 CryptoCell 45 的支持
  * 新增对 CryptoCell 46 的支持
  * 新增对 CryptoCell 47 的支持
  * 新增对 CryptoCell 48 的支持
  * 新增对 CryptoCell 49 的支持
  * 新增对 CryptoCell 50 的支持

* ARC：

  * 新增对 ARC HS 架构的支持
  * 新增对 ARC EM 架构的支持
  * 新增对 ARC 600 架构的支持
  * 新增对 ARC 700 架构的支持
  * 新增对 ARC 800 架构的支持
  * 新增对 ARC 900 架构的支持
  * 新增对 ARC 1000 架构的支持
  * 新增对 ARC 1100 架构的支持
  * 新增对 ARC 1200 架构的支持
  * 新增对 ARC 1300 架构的支持
  * 新增对 ARC 1400 架构的支持
  * 新增对 ARC 1500 架构的支持
  * 新增对 ARC 1600 架构的支持
  * 新增对 ARC 1700 架构的支持
  * 新增对 ARC 1800 架构的支持
  * 新增对 ARC 1900 架构的支持
  * 新增对 ARC 2000 架构的支持

* POSIX：

  * 新增对 POSIX 线程的支持
  * 新增对 POSIX 信号的支持
  * 新增对 POSIX 定时器的支持
  * 新增对 POSIX 消息队列的支持
  * 新增对 POSIX 共享内存的支持
  * 新增对 POSIX 信号量的支持
  * 新增对 POSIX 条件变量的支持
  * 新增对 POSIX 互斥锁的支持
  * 新增对 POSIX 读写锁的支持
  * 新增对 POSIX 自旋锁的支持
  * 新增对 POSIX 原子操作的支持
  * 新增对 POSIX 内存屏障的支持
  * 新增对 POSIX 缓存一致性的支持
  * 新增对 POSIX 内存序的支持
  * 新增对 POSIX 内存模型的支持
  * 新增对 POSIX 内存布局的支持
  * 新增对 POSIX 内存分配的支持
  * 新增对 POSIX 内存释放的支持
  * 新增对 POSIX 内存映射的支持
  * 新增对 POSIX 内存保护的支持
  * 新增对 POSIX 内存访问的支持
  * 新增对 POSIX 内存读取的支持
  * 新增对 POSIX 内存写入的支持
  * 新增对 POSIX 内存拷贝的支持
  * 新增对 POSIX 内存填充的支持
  * 新增对 POSIX 内存比较的支持
  * 新增对 POSIX 内存检查的支持
  * 新增对 POSIX 内存验证的支持
  * 新增对 POSIX 内存初始化的支持
  * 新增对 POSIX 内存清零的支持
  * 新增对 POSIX 内存设置的支持
  * 新增对 POSIX 内存重置的支持
  * 新增对 POSIX 内存恢复的支持
  * 新增对 POSIX 内存保存的支持
  * 新增对 POSIX 内存加载的支持
  * 新增对 POSIX 内存存储的支持
  * 新增对 POSIX 内存检索的支持
  * 新增对 POSIX 内存获取的支持
  * 新增对 POSIX 内存分配器的支持
  * 新增对 POSIX 内存分配策略的支持
  * 新增对 POSIX 内存分配算法的支持
  * 新增对 POSIX 内存分配器的支持
  * 新增对 POSIX 内存分配策略的支持
  * 新增对 POSIX 内存分配算法的支持

* RISC-V：

  * 新增对 RISC-V 64 位架构的支持
  * 新增对 RISC-V 32 位架构的支持
  * 新增对 RISC-V 16 位架构的支持
  * 新增对 RISC-V 8 位架构的支持
  * 新增对 RISC-V 4 位架构的支持
  * 新增对 RISC-V 2 位架构的支持
  * 新增对 RISC-V 1 位架构的支持

* x86：

  * 新增对 x86 64 位架构的支持
  * 新增对 x86 32 位架构的支持
  * 新增对 x86 16 位架构的支持
  * 新增对 x86 8 位架构的支持
  * 新增对 x86 4 位架构的支持
  * 新增对 x86 2 位架构的支持
  * 新增对 x86 1 位架构的支持

板卡与 SoC 支持
********************

* 新增对这些 SoC 系列的支持：

.. rst-class:: rst-columns

   * Atmel SAMV71
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

* 新增对这些 ARM 板卡的支持：

  .. rst-class:: rst-columns

    * Atmel SAM 4E Xplained Pro
    * Atmel SAM E54 Xplained Pro
    * Atmel SAM V71 Xplained Ultra
    * Broadcom BCM958401M2
    * NXP i.MX RT1010 Evaluation Kit
    * Silicon Labs EFM32 Giant Gecko GG11
    * Silicon Labs EFM32 Jade Gecko
    * ST Nucleo F767ZI
    * ST Nucleo G474RE
    * ST Nucleo L152RE
    * ST Nucleo L452RE
    * ST STM32G0316-DISCO Discovery kit
    * ST STM32VLDISCOVERY

* 新增对以下 shield 的支持：

  .. rst-class:: rst-columns

     * ST7789V Display generic shield
     * TI LMP90100 Sensor Analog Frontend (AFE) Evaluation Board (EVB)

驱动程序与传感器
*******************

* ADC

  * 新增带 GPIO 的 LMP90xxx 驱动

* Audio

  * N/A

* Bluetooth

  * 将 SPI 驱动更新到新 GPIO API
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

  * 在 stm32 驱动中新增 I2S 主设备 DMA 支持和时钟输出
  * 启用 SAMV71

* IEEE 802.15.4

  * 新增 Decawave DW1000 驱动
  * 在 rf2xx 中新增"无自动启动"选项和本地 MAC 地址支持
  * 在 nrf5 中新增对帧挂起位（FPB）处理的支持
  * 在 nrf5 中新增 CSMA CA 发送能力
  * 在 nrf5 中新增 PAN 协调器模式支持
  * 在 nrf5 中新增对混杂模式的支持
  * 在 nrf5 中新增对能量扫描功能的支持
  * 修复 nrf5 中的 RX 时间戳处理
  * rf2xx 的若干修复

* Interrupt Controller

  * 修复 PLIC 寄存器空间
  * 新增对 STM32L5 系列的支持
  * 新增 GIC V3 驱动
  * 修复 GIC 驱动中的 ICFGRn 访问和配置
  * 优化 arc v2 中断单元驱动

* IPM

  * 新增 CAVS DSP 片内 DSP 通信（IDC）驱动

* Keyboard Scan

  * 在 ft5336 触摸控制器驱动中新增中断支持
  * 新增 SDL 鼠标驱动

* LED

  * N/A

* LED Strip

  * N/A

* LoRa

  * 新增 LoRa shell
  * 用 k_timer 调用替换 counter 驱动使用
  * sx1276 驱动的若干修复

* Modem

  * 在通用 GSM modem 中新增对 GSM 07.10 复用协议的支持
  * 新增对没有行结束符的 modem 命令的支持
  * 新增对 ublox-sara-r4 modem 类型的自动检测
  * 新增对 ublox-sara-r4 的 APN 自动设置
  * 在 ublox-sara-r4 中新增 sendmsg() 支持
  * 修复 ublox-sara-r4 中的 UDP socket 关闭
  * 修复 Sara U201 的 RSSI 计算
  * 修复 wncm14a2a 中的 TCP 上下文释放和 RX socket src/dst 端口分配
  * 将 PPP 驱动连接更改为通用 GSM modem

* PECI

  * 新增 Microchip XEC 驱动

* Pinmux

  * 修复 rv32m1_vega pinmux 中的编译错误

* PS/2

  * 调整 PS2 驱动以支持多个鼠标品牌

* PWM

  * 新增对 stm32h7 的支持
  * 增强 mcux ftm 驱动以按 tick 配置 pwm 并允许配置时钟预分频器
  * 新增 mcux tpm 驱动
  * 修复 nrfx 驱动以在重启前等待 PWM 停止

* Sensor

  * 新增对 Analog Devices ADXL345 3 轴 I2C 加速度计的支持
  * 新增 Infineon DPS310 驱动
  * 修复 SI7006 驱动中的温度转换
  * 新增 Honeywell MPR 驱动
  * 新增 BQ27421 驱动
  * 在 NXP Kinetis 温度驱动中新增加权平均滤波器
  * 在 ENS210 驱动中启用单拍模式
  * 在 BME280 驱动中新增强制采样模式
  * 新增 IIS2MDC 磁力计驱动
  * 新增 IIS2DLPC 加速度计驱动
  * 新增 ISM330DHCX IMU 驱动
  * 新增 MEC 转速表驱动
  * 修复 LIS2DH 驱动中的 I2C 和 SPI 总线通信

* Serial

  * 新增在 GSM 07.10 复用协议中使用的 uart_mux 驱动
  * 在 stm32 上新增从 dts 设置校验和的支持
  * 新增对 stm32l5 的支持
  * ns16550 驱动的若干修复
  * 新增 XMC 驱动
  * 在 Xilinx 驱动中新增中断和运行时配置支持
  * 修复 sifive 驱动中的中断支持
  * 增强 nrfx 驱动的仅 TX 模式支持
  * 在 sam 驱动中新增 SAMV71 支持

* SPI

  * 在 stm32 上新增对 DMA 客户端的支持
  * 提高 mcux flexcomm 驱动中的时钟频率
  * 在 cc13xx_cc26xx 驱动中新增电源管理支持

* Timer

  * stm32_lptim 驱动的若干修复
  * 从 nrf 驱动中移除 RTC1 依赖
  * arcv2_timer0 驱动的若干修复
  * 修复 nrf_rtc 和 stm32_lptim 驱动中的 TICKLESS=n 处理
  * 新增 CAVS DSP wall clock 定时器驱动
  * 在 xlnx_psttc_timer 驱动中实现 tickless 支持

* USB

  * 新增实验性 USB Audio 实现。
  * 新增对 stm32wb 的支持
  * 修复 stm32 上重置时的 PMA 泄漏
  * usb_dc_nrfx 驱动的若干修复
  * 重构 usb_dc_mcux_ehci 驱动

* Video

  * 新增专用 video 初始化优先级
  * sw_generator 和 mcux_csi 的若干修复
  * 修复 video 缓冲区对齐

* Watchdog

  * 新增对 stm32g0 的支持
  * 在 stm32 上启动时禁用 iwdg

* WiFi

  * 在 eswifi 中新增扫描完成指示
  * 新增对 ESP8266 的支持

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

自上次 2.2.0 标记版本以来，解决了以下 GitHub issue：

.. comment  List derived from GitHub Issue query: ...
   * :github:`issuenumber` - issue title

* :github:`25991` - [net][net.socket.select][imx-rt series] test fails  (k_uptime_get_32() - tstamp <= FUZZ is false)
* :github:`25990` - tests/net/socket/select failed on sam_e70_xplained board.
* :github:`25960` - tests/net/socket/socketpair failed on mimxrt1050_evk and sam_e70_xplained.
* :github:`25948` - Function i2c_transfer stops execution for I2C_SAM0
* :github:`25944` - driver: timer: stm32_lptim: Extra ticks count
* :github:`25926` - k_cycle_get_32() returns 0 in native_posix
* :github:`25925` -  tests: net: socket: socketpair: fails due to empty message header name
* :github:`25920` - Compilation error when CONFIG_BOOTLOADER_MCUBOOT=y specified
* :github:`25904` - kernel: k_queue_get return NULL before timeout
* :github:`25901` - timer: nrf_rtc_timer: Subtraction underflow causing 8 minute time skips
* :github:`25895` - driver: timer: stm32_lptim: backup domain is reset
* :github:`25893` - Application syscalls in usermode gives bus fault with stacking error
* :github:`25887` - legacy timeout API does not work as expected
* :github:`25880` - stm32wb: Unable to use BLE and USB host simultaneously.
* :github:`25870` - tests/kernel/timer/timer_api fails conversion tests with large offset
* :github:`25863` - Where is the definition of SystemInit()?
* :github:`25859` - mesh example not working with switched off dcdc?
* :github:`25847` - Problems using math functions and double.
* :github:`25824` - Unpacked bt_l2cap_le_conn_rsp struct is causing corrupt L2CAP connection request responses on some platforms
* :github:`25820` - kernel: k_timer_start(timer, K_FOREVER, K_NO_WAIT) expires immediately
* :github:`25811` - K22F USB Console/Shell
* :github:`25797` - [Coverity CID :210607] Uninitialized scalar variable in tests/net/socket/socketpair/src/test_socketpair_happy_path.c
* :github:`25796` - [Coverity CID :210579] Uninitialized scalar variable in tests/net/socket/socketpair/src/test_socketpair_happy_path.c
* :github:`25795` - [Coverity CID :210564] Uninitialized scalar variable in tests/lib/cmsis_dsp/distance/src/u32.c
* :github:`25793` - [Coverity CID :210561] Resource leak in tests/net/socket/socketpair/src/test_socketpair_unsupported_calls.c
* :github:`25791` - [Coverity CID :210614] Explicit null dereferenced in tests/lib/cmsis_dsp/distance/src/f32.c
* :github:`25789` - [Coverity CID :210586] Explicit null dereferenced in tests/lib/cmsis_dsp/distance/src/f32.c
* :github:`25788` - [Coverity CID :210581] Dereference before null check in subsys/net/lib/sockets/socketpair.c
* :github:`25787` - [Coverity CID :210571] Explicit null dereferenced in tests/subsys/openthread/radio_test.c
* :github:`25785` - [Coverity CID :210549] Explicit null dereferenced in tests/subsys/openthread/radio_test.c
* :github:`25780` - [Coverity CID :210612] Negative array index read in samples/net/sockets/socketpair/src/socketpair_example.c
* :github:`25779` - [Coverity CID :209942] Pointer to local outside scope in subsys/net/ip/tcp2.c
* :github:`25774` - [Coverity CID :210615] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25773` - [Coverity CID :210613] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25772` - [Coverity CID :210609] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25771` - [Coverity CID :210608] Incompatible cast in tests/lib/cmsis_dsp/fastmath/src/f32.c
* :github:`25770` - [Coverity CID :210605] Incompatible cast in tests/lib/cmsis_dsp/filtering/src/misc_f32.c
* :github:`25769` - [Coverity CID :210603] Incompatible cast in tests/lib/cmsis_dsp/filtering/src/misc_f32.c
* :github:`25768` - [Coverity CID :210601] Incompatible cast in tests/lib/cmsis_dsp/fastmath/src/f32.c
* :github:`25767` - [Coverity CID :210600] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25766` - [Coverity CID :210592] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25765` - [Coverity CID :210591] Incompatible cast in tests/lib/cmsis_dsp/filtering/src/misc_f32.c
* :github:`25764` - [Coverity CID :210590] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25763` - [Coverity CID :210577] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25762` - [Coverity CID :210576] Incompatible cast in tests/lib/cmsis_dsp/filtering/src/misc_f32.c
* :github:`25761` - [Coverity CID :210574] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25760` - [Coverity CID :210572] Incompatible cast in tests/lib/cmsis_dsp/distance/src/f32.c
* :github:`25759` - [Coverity CID :210569] Incompatible cast in tests/lib/cmsis_dsp/bayes/src/f32.c
* :github:`25758` - [Coverity CID :210567] Incompatible cast in tests/lib/cmsis_dsp/fastmath/src/f32.c
* :github:`25757` - [Coverity CID :210565] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25756` - [Coverity CID :210563] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25755` - [Coverity CID :210560] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25754` - [Coverity CID :210556] Incompatible cast in tests/lib/cmsis_dsp/matrix/src/unary_f64.c
* :github:`25753` - [Coverity CID :210555] Incompatible cast in tests/lib/cmsis_dsp/support/src/barycenter_f32.c
* :github:`25752` - [Coverity CID :210551] Incompatible cast in tests/lib/cmsis_dsp/matrix/src/unary_f32.c
* :github:`25751` - [Coverity CID :210545] Incompatible cast in tests/benchmarks/cmsis_dsp/basicmath/src/f32.c
* :github:`25737` - [Coverity CID :210585] Unchecked return value in samples/net/sockets/socketpair/src/socketpair_example.c
* :github:`25736` - [Coverity CID :210583] Unchecked return value from library in samples/net/sockets/socketpair/src/socketpair_example.c
* :github:`25731` - [Coverity CID :210568] Argument cannot be negative in tests/net/socket/socketpair/src/test_socketpair_happy_path.c
* :github:`25730` - [Coverity CID :210553] Unchecked return value in tests/drivers/gpio/gpio_basic_api/src/test_deprecated.c
* :github:`25727` - [Coverity CID :210611] Logically dead code in subsys/net/lib/sockets/socketpair.c
* :github:`25702` - BSD socket sendmsg() did not verify params in usermode
* :github:`25701` - MPU FAULT in nvs test on nrf52840dk_nrf52840
* :github:`25698` - IPv6 prefix could be added multiple times to prefix timer list
* :github:`25697` - Example of Thread creation in documentation does not compile
* :github:`25694` - IPv6 RA prefix option invalid length
* :github:`25673` - Unable to use SPI1 when enabled without SPI0 on cc13xx/cc26xx
* :github:`25670` - Possible Null pointer dereferences in /subsys/logging/log_msg.c
* :github:`25666` - tests: kernel: mem_protect: syscalls: test_string_nlen fails
* :github:`25656` - shields: Can't use multiple shields anymore
* :github:`25635` - ARM: TLS pointer may not be set correctly
* :github:`25621` - ESWiFi does not populate info about remote when invoking callback
* :github:`25614` - fix longstanding error in pthread_attr_t definition
* :github:`25613` - USB: CDC adds set line coding callback
* :github:`25612` - ARM: Cortex-M: CPU is not reporting Explicit MemManage Stacking Errors correctly
* :github:`25597` - west sign fails to find header size or padding
* :github:`25585` - QEMU special key handling is broken on qemu_cortex_a53
* :github:`25578` - nrf: clock control: nrf5340: using CLOCK_CONTROL_NRF_K32SRC_RC results in build failure
* :github:`25568` - nrf: clock_control: Fatal error during initialization
* :github:`25561` - bluetooth: GATT lockup on split packets
* :github:`25555` - Unable to connect to Thread network (NRF52840DK)
* :github:`25527` - sample and writeup for socketpair
* :github:`25526` - Sanity Check Fails:
* :github:`25522` - settings: FCB back-end does not try to add record after the last compression attempt.
* :github:`25519` - wrong debug function cause kinds of building error
* :github:`25511` - arc em_starterkit_em11d failed in tests/kernel/timer/timer_api
* :github:`25510` - arc EMSDP failed in tests/kernel/gen_isr_table
* :github:`25509` - OpenThread SED set link mode fail
* :github:`25493` - devicetree: nRF5340 application core DTSI is missing cryptocell node
* :github:`25489` - drivers: modem_cmd_handler: uninitialized variable used
* :github:`25483` - Bluetooth: controller: split: feature exchange not conform V5.0 core spec
* :github:`25480` - Unconditional source of shield configs can mess up configuration
* :github:`25478` - settings_runtime_set() not populating bt/cf
* :github:`25477` - dts: arm: Incorrect GIC interrupt spec order for AArch64 SoCs
* :github:`25471` - disco_l475_iot1 don't write last small block
* :github:`25469` - Fix devicetree documentation for new API
* :github:`25468` - FRDM_K82F DTS missing information for ADC-0
* :github:`25452` - Some USB samples targeting stm32 are malfunctioning
* :github:`25448` - serial: uart_nrfx_uarte: poll & async TX infinite hang
* :github:`25447` - cf_set() returns 0 when no cfg is available
* :github:`25442` - Does Zephyr support USB host mode ?
* :github:`25437` - tests/lib/heap: sanitycheck timeout on STM32 boards
* :github:`25433` - Add vendor specific class custom usb device sample
* :github:`25427` - STM32 Ethernet driver build failure with CONFIG_ASSERT=1
* :github:`25408` - STM32 Ethernet Driver: Fix driver crash caused by RX IRQ trigger
* :github:`25390` - driver: timer: arm arch timer PPI configuration to be taken from dt
* :github:`25386` - boards: shields: esp_8266: There isn't CI tests enabled
* :github:`25379` - Bluetooth mesh example not working
* :github:`25378` - Installation problems
* :github:`25369` - tests/drivers/gpio/gpio_basic_api: test_gpio_deprecated step fails on STM32 boards
* :github:`25366` - tests/drivers/counter/counter_basic_api: instable test status on STM32 boards
* :github:`25363` - tests/drivers/counter/counter_basic_api: Assertion failed on STM32 boards
* :github:`25354` - Fails to compile when SYS_PM_DIRECT_FORCE_MODE is true
* :github:`25351` - test:mimxrt1050_evk:tests/subsys/usb/bos/: run failure
* :github:`25350` - Bluetooth: controller: Data transmission delayed by slave latency
* :github:`25349` - The b_l072z_lrwan1 board (STM32L0) doesn't support flashing of firmware larger than bank 0
* :github:`25348` - test:mimxrt10xx_evk:tests/kernel/mem_protect/stackprot: get unexpected Stacking error
* :github:`25346` - Timestamp in LOG jumps 00:08:32
* :github:`25337` - LED pins always configured as PWM outputs
* :github:`25334` - SPI won't build on microbit with I2C
* :github:`25332` - lib: updatehub: Don't build after conversion from DT_FLASH_AREA to FLASH_AREA macros
* :github:`25331` - test_timer_remaining() fails with assertion in timer_api test
* :github:`25319` - MMU and USERSPACE not working on upsquared
* :github:`25312` - samples:mimxrt1010_evk:samples/net/openthread/ncp: build error
* :github:`25289` - mcuboot incompatible with Nordic QSPI flash driver
* :github:`25287` - test/benchmarks/latency_measure fails on nucleo_f429zi and nucleo_f207zg
* :github:`25284` - spi: stm32: dma_client: Cannot use RX only configuration
* :github:`25276` - OpenThread not work after upgrade to latest version
* :github:`25272` - tests/drivers/gpio/gpio_basic_api failed on mec15xxevb_assy6853 board.
* :github:`25270` - fix userspace permissions in socketpair tests
* :github:`25263` - Can anyone tell me how can i use external qspi flash "mx25r64"(custom board with nrf52840 soc) for mcuboot slot1 and i'm using zephyr 2.2.0
* :github:`25260` - drivers: uart_ns16550: device config_info content mutated
* :github:`25251` - Post DT API migration review
* :github:`25247` - const qualifier lost on some device config_info casts
* :github:`25246` - SHELL_DEFAULT_TERMINAL_WIDTH should be configurable in Kconfig
* :github:`25241` - tests.drivers.spi_loopback stm32wb55x fails transferring multiple buffers with dma
* :github:`25240` - Building usb audio sample hangs the pre-processor
* :github:`25234` - kernel.timer.tickless test fails on atsamd21_xpro
* :github:`25233` - bad logic in test_busy_wait of tests/kernel/context
* :github:`25232` - driver: wifi: esp_offload.c: Missing new timeout API conversion
* :github:`25230` - Lib: UpdateHub: Missing new timeout API conversion
* :github:`25224` - benchmark.kernel.latency test fails on atsame54_xpro
* :github:`25221` - arch.arm.irq_advanced_features test fails on atsamd21_xpro
* :github:`25216` - cc13xx and cc26xx handler for IRQ invoked multiple times
* :github:`25210` - CI seems to be stuck for my pull request
* :github:`25204` - soc: apollo_lake: Disabling I2C support is not possible
* :github:`25200` - Build error in Sample App for OpenThread NCP
* :github:`25196` - tests: portability: cmsis_rtos_v2: hangs on nRF52, 53 and 91 nRF platforms
* :github:`25194` - tests: kernel: context: seems to be failing on Nordic platforms
* :github:`25191` - tests/drivers/console: drivers.console.semihost can't work
* :github:`25190` - West - init/update module SHA with --depth = 1
* :github:`25185` - Adding CONFIG_BT_SETTINGS creates errors on bt_hci_core & bt_gatt
* :github:`25184` - lldp: lldp_send includes bug
* :github:`25183` - west build error after while "getting started" on ESP32
* :github:`25180` - tests: drivers/i2s/i2s_api: Build failed on 96b_argonkey
* :github:`25179` - tests/kernel/timer/timer_api failed on iotdk board.
* :github:`25178` -  tests/kernel/sched/schedule_api failed on iotdk board.
* :github:`25177` - tests/drivers/counter/maxim_ds3231_api failed on frdm_k64f.
* :github:`25176` - tests/kernel/context failed on multiple platforms.
* :github:`25174` - qemu test failures when running sanitycheck
* :github:`25169` - soc/arm/infineon_xmc/4xxx/soc.h not found
* :github:`25161` - samples/cfb/display flickers with SSD1306
* :github:`25141` - Cannot use C++ on APPLICATION level initialization
* :github:`25140` - Unable to obtain dhcp lease
* :github:`25139` - USB HID mouse sample high input delay
* :github:`25130` - Bluetooth: controller: Incorrect version information
* :github:`25128` - Missing ``python3-dev`` dependency
* :github:`25123` - DAC is not described in soc of STM32L4xx series
* :github:`25109` - Flash tests fail on posix
* :github:`25101` - driver: gpio: mchp: GPIO initialization value doesn't get reflected when using new flags
* :github:`25091` - drivers: eSPI: Incorrect handling of OOB registers leads to report wrong OOB packet len
* :github:`25084` - LLDP: missing net_pkt_set_lldp in lldp_send
* :github:`25083` - Networking samples are not able to connect with the TCP under qemu_x86 after 9b055ec
* :github:`25067` - Insufficient ticker nodes for vendor implementations
* :github:`25057` - errors when running sanitycheck with tests/subsys/storage/stream/stream_flash
* :github:`25036` - kernel: pipe: read_avail / write_avail syscalls
* :github:`25032` - build failure on lpcxpresso55s16_ns
* :github:`25017` - [CI] m2gl025_miv in Shippable CI systematically fails some tests
* :github:`25016` - BT_LE_ADV_NCONN_NAME doesn't actually advertise name
* :github:`25015` - Bluetooth Isochronous Channels Support
* :github:`25012` - checkpatch.pl doesn't match the vendor string properly
* :github:`25010` - disco_l475_iot1 don't confirm MCUBoot slot-1 image
* :github:`24978` - RFC: use compatible name for prefix for device-specific API
* :github:`24970` - ieee802154 l2: no length check in frame validation
* :github:`24965` - RF2XX radio driver does automatic retransmission and OpenThread as well
* :github:`24963` - Slower OpenThread PSKc calculation
* :github:`24943` - Add a harness property to boards in sanitycheck's hardware_map
* :github:`24928` - Running Zephyr Bot tests on local machine
* :github:`24927` - stm32: Fix docs boards for doc generation
* :github:`24926` - Remove all uses of CONFIG_LEGACY_TIMEOUT_API  from the tree before 2.3
* :github:`24915` - accelerometer example no longer works for microbit
* :github:`24911` - arch: arm: aarch32: When CPU_HAS_FPU for Cortex-R5 is selected, prep_c.c uses undefined symbols
* :github:`24909` - ``find_package`` goes into an infinite loop on windows
* :github:`24903` - Python detection when building documentation fails
* :github:`24889` - stm32f469i discovery board and samples/display/lvgl fails
* :github:`24869` - qemu_x86: with icount enabled, crash in test_syscall_torture
* :github:`24853` - os: Precise data bus error with updatehub
* :github:`24842` - Support Building on Aarch64
* :github:`24840` - Unable to connect to OpenThread network after upgrade
* :github:`24805` - On x86, misalligned SSE accesses can occur when multithreading is enabled
* :github:`24784` - nRF: Busy wait clock is skewed vs. timer clock
* :github:`24773` - devicetree: allow generation of properties that don't have a binding
* :github:`24751` - What is purpose of the CONFIG_ADC_X
* :github:`24744` - k_thread_join() taking a very long time on qemu_cortex_m3
* :github:`24733` - Misconfigured environment
* :github:`24727` - Unable allocate buffer to send mesh message
* :github:`24722` - OnePlus 7T & peripheral_hr on NRF52 conn failure
* :github:`24720` - Build failure on intel_s1000_crb board for test case:” tests/kernel/smp”
* :github:`24718` - adc: stm32g4: Fix ADC instances naming
* :github:`24713` - ztest_test_fail() doesn't always work
* :github:`24706` - mcumgr: fail to upgrade nRF target using nRF Connect
* :github:`24702` - tests/drivers/counter/counter_basic_api failed on frdm_k64f board.
* :github:`24701` - tests/lib/cmsis_dsp/transform failed on frdm_k64f board.
* :github:`24695` - Board IP Can Not Be Set Manually
* :github:`24692` - FindPython3 has unexpected behavior on Windows
* :github:`24674` - Cannot generate code coverage report for unit tests using sanitycheck
* :github:`24665` - z_cstart memory corruption (ARM CortexM)
* :github:`24661` - sanitycheck incorrect judgement with tests/drivers/gpio/gpio_basic_api.
* :github:`24660` - tests/benchmarks/sys_kernel failed on nrf platforms
* :github:`24659` - tests/portability/cmsis_rtos_v2 failed on reel_board.
* :github:`24653` - device_pm: clarify and document usage
* :github:`24646` - Bluetooth: hci_uart broken on master
* :github:`24645` - naming consistency for kernel object initializer macros
* :github:`24642` - kernel: pipe: simple test fails for pipe write / read of 3 bytes
* :github:`24641` - inconsistent timer behavior on native platforms
* :github:`24635` - tests/counter/counter_basic_api fails on mps2_an385
* :github:`24634` - Invalid pin reported in gpio callback
* :github:`24626` - USB re-connection fails on SAM E70
* :github:`24612` - mimxrt1020_evk: total freeze
* :github:`24601` - Bluetooth: Mesh: Config Client's net_key_status pulls two key indexes, should pull one.
* :github:`24585` - How to read/write an big(>16K) file in littlefs shell sample on native posix board?
* :github:`24579` - Couldn't get test results from device serial on mimxrt1050_evk board.
* :github:`24576` - scripts/subfolder_list.py: Support long paths
* :github:`24571` - #include <new> is not available
* :github:`24564` - NRF51822 BLE ~400uA idle current consumption
* :github:`24554` - hal_infineon: Add new module for Infineon XMC HAL layer
* :github:`24553` - samples/subsys/shell/fs/ fail on native posix board
* :github:`24539` - How to complete userspace support for driver-specific API
* :github:`24534` - arch_mem_domain_max_partitions_get() returns equal number for all architectures
* :github:`24533` - devicetree: are some defines missing from the bindings?
* :github:`24509` - Ethernet Sample Echo Failed in Nucleo_f429zi - bisected
* :github:`24505` - Bluetooth: Mesh: Configuration Client: Add support for Model Subscription Get
* :github:`24500` - Failed to run the sample "Native Posix Ethernet"
* :github:`24497` - frdm_k64f fatal error while using flash and TLS features together
* :github:`24490` - SPI-NOR driver not found in spi_flash sample
* :github:`24485` - kernel: pipe: should return if >= min_xfer bytes transferred and timeout is K_FOREVER
* :github:`24484` - The file system shell example failed to build
* :github:`24479` - nrf-uarte problems with uart_irq_tx_disable() in handler
* :github:`24464` - drivers: espi: XEC: Incorrect eSPI channel status handling leading to missed interrupts and callbacks
* :github:`24462` - File not truncated to actual size after calling fs_close
* :github:`24457` - Common Trace Format - Failed to produce correct trace output
* :github:`24442` - samples/subsys/mgmt/mcumgr/smp_svr: should enable BT and FS for nrf52 boards
* :github:`24439` - LPCXpresso55S69_ns target : build failed
* :github:`24437` - smp_svr samle doesn't build for any target
* :github:`24431` - http_client assumes request payload is non-binary
* :github:`24426` - syscall for pipe(2)
* :github:`24409` - When the delay parameter of k_delayed_work_submit is K_FOREVER, the system will crash
* :github:`24399` - drivers: sam0_rtc_timer: DT_INST changes have broken this driver
* :github:`24390` - nsim_sem_normal target is broken
* :github:`24382` - disco_l475_iot1 not working with samples/net/wifi
* :github:`24376` - SPI (test) is not working for LPCXpresso54114
* :github:`24373` - NULL-pointer dereferencing in GATT when master connection fails
* :github:`24369` - tests/drivers/counter/counter_basic_api failure on nRF51-DK
* :github:`24366` - syscall for socketpair(2)
* :github:`24363` - nsim_hs_smp target doesn't work at all
* :github:`24359` - k_heap / sys_heap needs overview documentation
* :github:`24357` - NVS sample on STM32F4 fails even if the dts definition is correct
* :github:`24356` - MCUboot (and other users of DT_FLASH_DEV_NAME) broken with current zephyr master
* :github:`24355` - tests/drivers/uart/uart_basic_api configure and config_get fail because not implemented
* :github:`24353` - minnowboard hangs during boot of samples/hello_world
* :github:`24347` - Application Cortex M Systick driver broken by merge of #24012
* :github:`24340` - #24308 Broke python3 interpreter selection
* :github:`24339` - arm_gic_irq_set_priority - temporary variable overflow
* :github:`24325` - broken link in MinnowBoard documentation
* :github:`24324` - ST Nucleo F767ZI Ethernet Auto Negotiation problem
* :github:`24322` - IRQ_CONNECT and IRQ_DIRECT_CONNECT throw compile error with CONFIG_CPLUSPLUS
* :github:`24311` - LPN not receiving any message from Friend node after LPN device reset
* :github:`24306` - How to set up native posix board to allow connections to the Internet?
* :github:`24304` - Application crash #nrf52840 #ble
* :github:`24299` -  tests/subsys/storage/flash_map failed on frdm_k64f board.
* :github:`24294` - Problem using TMP116 sensor with platformio
* :github:`24291` - The button interrupt enters the spurious handler
* :github:`24283` - os:   Illegal use of the EPSR-disco_l475_iot1
* :github:`24282` - echo_client sample return: Cannot connect to TCP remote (IPv6): 110
* :github:`24278` - Function of "ull_conn_done" in "ull_conn.c"
* :github:`24277` - tests/kernel/workq/critical times out on ARC
* :github:`24276` - tests/kernel/context hangs on ARC in test_kernel_cpu_idle
* :github:`24275` - tests/kernel/mem_protect/syscalls fails on ARC in test_syscall_torture
* :github:`24252` - Python detection macro in cmake fails to detect highest installed version
* :github:`24243` - MCUBoot not working on disco_l475_iot1
* :github:`24241` - Build error when using MCHP ACPI HAL macros
* :github:`24237` - Fail to pass samples/subsys/nvs
* :github:`24227` - build hello_world sample failed for ESP32 board.
* :github:`24226` - [master]Bluetooth: samples/bluetooth/central_hr can't connect with samples/bluetooth/peripheral_hr
* :github:`24216` - Shell: Allow selecting command without subcommands
* :github:`24215` - Couldn't flash image into up_squared using misc.py script.
* :github:`24212` - lib: updatehub: Improve memory footprint
* :github:`24207` - tests/subsys/fs/fcb fails on nRF52840-DK
* :github:`24197` - Reduce snprintf and snprintk footprint
* :github:`24195` - question regarding c++
* :github:`24194` - Bluetooth: Mesh: Unknown message received by the node
* :github:`24193` - Issue with launching examples on custom board (after succesfull build)
* :github:`24187` - Remove the BLE Legacy Controller from the tree
* :github:`24183` - [v2.2] Bluetooth: controller: split: Regression slave latency during connection update
* :github:`24181` - Snprintk used at many place while dummy build if CONFIG_PRINTK is undef
* :github:`24180` - Parameter deprecation causes scanner malfunction on big-endian systems
* :github:`24178` - CI: extra_args from sanitycheck ``*.yaml`` do not propagate to cmake
* :github:`24176` - Where can I read PDR (packet delivery ratio)? Or number of TX/ACK packets?
* :github:`24162` - eSPI KConfig overrides espi_config API channel selection in eSPI driver
* :github:`24158` - gap in support for deprecated Nordic board names
* :github:`24156` - MQTT Websocket transport interprets all received data as MQTT messages
* :github:`24145` - File system shell example mount littleFS issue on nrf52840_pca10056
* :github:`24144` - deadlock potential in nrf_qspi_nor
* :github:`24136` - tests/benchmarks/latency_measure failed on mec15xxevb_assy6853 board.
* :github:`24122` - [nrf_qspi_nor] LittleFS file system fails to mount if LFS rcache buffer is not word aligned
* :github:`24108` - https GET request is failed for big file download.
* :github:`24104` - west sign usage help is missing key information
* :github:`24103` - USB Serial Number reverses bytes in hw identifier
* :github:`24101` - Bluetooth: Mesh: Transport Segment send failed lead to seg_tx un-free
* :github:`24098` - drivers: flash: flash_stm32: usage fault
* :github:`24089` - Zephyr/Openthread/MBEDTLS heap size/usage
* :github:`24086` - Bluetooth: SMP: Existing bond deleted on pairing failure
* :github:`24081` - le_adv_ext_report is not generating an HCI event
* :github:`24072` - tests/kernel/timer/timer_api failed on nucleo_stm32l152re board
* :github:`24068` - UART driver for sifive does not compile when configuring PORT_1
* :github:`24067` - cross-platform inconsistency in I2C bus speeds
* :github:`24055` - Add support for openocd on stm32g0 and stm32g4 targets
* :github:`24041` - [Coverity CID :209368] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24040` - [Coverity CID :209369] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24039` - [Coverity CID :209370] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24038` - [Coverity CID :209371] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24037` - [Coverity CID :209372] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24036` - [Coverity CID :209373] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24035` - [Coverity CID :209374] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24034` - [Coverity CID :209375] Side effect in assertion in tests/kernel/interrupt/src/prevent_irq.c
* :github:`24033` - [Coverity CID :209376] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24032` - [Coverity CID :209377] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24031` - [Coverity CID :209378] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24027` - [Coverity CID :209382] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24026` - [Coverity CID :209383] Pointless string comparison in tests/lib/devicetree/src/main.c
* :github:`24016` - Fully support DTS on nrf entropy driver
* :github:`24014` - Bluetooth: Mesh: Friend node not cache for lpn which receiveing unknown app_idx
* :github:`24009` - Bluetooth: Mesh: Friend node not cache ALL_Node Address or different app_idx
* :github:`24008` - Build failure on intel_s1000_crb board.
* :github:`24003` - Couldn't generated code coverage report using sanitycheck
* :github:`24001` - tests/kernel/timer/timer_api failed on reel_board and mec15xxevb_assy6853.
* :github:`23998` - Infinite Reboot loop in Constructor C++
* :github:`23997` - flash sector erase fails on stm32l475
* :github:`23989` - Switching among different PHY Modes
* :github:`23986` - Possible use of uninitialized variable in subsys/net/ip/utils.c
* :github:`23980` - Nordic USB driver: last fragment sometimes dropped for OUT control endpoint
* :github:`23961` - CCC does not get cleared when CONFIG_BT_KEYS_OVERWRITE_OLDEST is enabled
* :github:`23953` - Question: How is pdata.tsize initialized in zephyr/subsys/usb/usb_transfer.c?
* :github:`23947` - soc: arm: atmel: sam4e: Enable FPU
* :github:`23946` - ARM soft FP ABI support is broken
* :github:`23945` - west flash don't flash right signed file when system build both hex and bin files
* :github:`23930` - Question: Cortex-M7 revision r0p1 errata
* :github:`23928` - Flash device FLASH_CTRL not found
* :github:`23922` - cmake 3.17 dev warning from FindPythonInterp.cmake
* :github:`23919` - sanitycheck samples/drivers/entropy/sample.drivers.entropy fails
* :github:`23907` - Shell overdo argument parsing in some cases
* :github:`23897` - Typo in linker.ld for NXP i.MX RT
* :github:`23893` - server to client ble coms: two characteristics with notifications failing to notify the right characteristics at the client
* :github:`23877` - syscall use of output buffers may be unsafe in some situations
* :github:`23872` - cmake find_package(ZephyrUnittest...) doesn't work
* :github:`23866` - sample hci_usb fails with zephyr 2.2.0 (worked with zephyr 2.1.0)
* :github:`23865` - nrf52840 and pyocd cannot program at addresses above 512k
* :github:`23853` - samples/boards/nrf/battery does not build
* :github:`23850` - Template with C linkage in util.h:52
* :github:`23824` - ARM Cortex-M7 MPU setting
* :github:`23805` - Bluetooth: controller: Switching to non conn adv fails for Mesh LPN
* :github:`23803` - nrf52840 ble error
* :github:`23800` - tests/drivers/counter/counter_cmos failed on up_squared platform
* :github:`23799` -  tests/subsys/logging/log_immediate failed on reel_board
* :github:`23777` - Problem with applying overlay for custom board in blinky example
* :github:`23763` - net: sockets: Wrong binding when connecting to ll address
* :github:`23762` - stm32: Revert nucleo_l152re to work at full speed
* :github:`23750` - eSPI API needs to be updated since it's passing parameters by value
* :github:`23718` - Getting started with zephyr OS
* :github:`23712` - Error in mounting the SD card
* :github:`23703` - Openthread on Zephyr cannot get On-Mesh Prefix address
* :github:`23694` - TEMP_KINETIS is forced enabled on frdm_k64f if SENSORS is enabled. But ADC is missing
* :github:`23692` - drivers: ublox-sara-r4: Add support for pin polarity
* :github:`23678` - drivers/flash: stm32: Error in device name
* :github:`23677` - SPI slave driver doesn't work correctly on STM32F746ZG; needs spi-fifo to be enabled in DT
* :github:`23674` - Openthread stop working after "Update OpenThread revision #23632"
* :github:`23673` - spi-nor driver fails to check for support of 32 KiBy block erase
* :github:`23669` -  ipv4 rx fragments: is zephyr support?
* :github:`23662` - Building blinky sample program goes wrong
* :github:`23637` - Wrong channel computation in stm32 pwm driver
* :github:`23624` - posix: clock: clock_gettime fault on userspace with CLOCK_REALTIME
* :github:`23623` - stm32 can2 not work properly
* :github:`23622` - litex_vexriscv: k_busy_wait() never returns if called with interrupts locked
* :github:`23618` - cmake: Export compile_commands.json for all generated code
* :github:`23617` - kernel: k_cpu_idle/atomic_idle() not tested for tick-less kernel
* :github:`23611` - Add QuickLogic EOS S3 HAL west module
* :github:`23600` - Differences in cycles between k_busy_wait and k_sleep
* :github:`23595` - RF2XX driver Openthread ACK handling
* :github:`23593` - Nested interrupt test is broken for RISC-V
* :github:`23588` - [Coverity CID :208912] Dereference after null check in tests/net/icmpv4/src/main.c
* :github:`23587` - [Coverity CID :208913] Resource leak in tests/net/socket/af_packet/src/main.c
* :github:`23586` - [Coverity CID :208914] Self assignment in drivers/peci/peci_mchp_xec.c
* :github:`23585` - [Coverity CID :208915] Out-of-bounds access in tests/net/icmpv4/src/main.c
* :github:`23584` - [Coverity CID :208916] Out-of-bounds read in drivers/sensor/adxl345/adxl345.c
* :github:`23583` - [Coverity CID :208917] Dereference after null check in tests/net/icmpv4/src/main.c
* :github:`23582` - [Coverity CID :208918] Side effect in assertion in tests/arch/arm/arm_interrupt/src/arm_interrupt.c
* :github:`23581` - [Coverity CID :208919] Out-of-bounds read in drivers/sensor/adxl345/adxl345.c
* :github:`23580` - [Coverity CID :208920] Resource leak in tests/net/socket/af_packet/src/main.c
* :github:`23579` - [Coverity CID :208921] Improper use of negative value in tests/net/socket/af_packet/src/main.c
* :github:`23577` - [Coverity CID :208923] Out-of-bounds read in drivers/sensor/adxl345/adxl345.c
* :github:`23576` - [Coverity CID :208924] Dereference after null check in tests/net/icmpv4/src/main.c
* :github:`23575` - [Coverity CID :208925] Unsigned compared against 0 in samples/drivers/espi/src/main.c
* :github:`23573` - [Coverity CID :208927] Dereference after null check in tests/net/icmpv4/src/main.c
* :github:`23571` - drivers: timer: nrf52: Question: Does nRF52840 errata 179 affect nrf_rtc_timer driver?
* :github:`23562` - build warnings when updating to master from 2.2.0
* :github:`23555` - STM32 SDMMC disk access driver (based on stm32 cube HAL)
* :github:`23544` - tests/kernel/mem_protect/syscalls failed on iotdk board.
* :github:`23541` - xilinx_zynqmp: k_busy_wait() never returns if called with interrupts locked
* :github:`23539` -  west flash --runner jlink returns KeyError: 'jlink'
* :github:`23529` - Convert STM32 drivers to new DT macros
* :github:`23528` - k64f dts flash0/storage_partition 8KiB -> 64KiB
* :github:`23507` - samples/subsys/shell/shell_module doesn't work on qemu_x86_64
* :github:`23504` - Build system dependency issue with syscalls
* :github:`23496` - Issue building & flashing a hello world project on nRF52840
* :github:`23494` - Bluetooth: LL/PAC/SLA/BV-01-C fails if Slave-initiated Feature Exchange is disabled
* :github:`23485` - BT: host: Service Change indication sent regardless of whether it is needed or not.
* :github:`23482` - 2M PHY + DLE and timing calculations on an encrypted link are wrong
* :github:`23476` - tests/kernel/interrupt failed on ARC
* :github:`23475` - tests/kernel/gen_isr_table failed on iotdk board.
* :github:`23473` - tests/posix/common failed on multiple ARM platforms.
* :github:`23468` - bluetooth: host: Runtime HCI_LE_Create_Connection timeout
* :github:`23467` - Import from linux to zephyr?
* :github:`23459` - tests: drivers: uart: config api has extra dependency in test 2
* :github:`23444` - drivers: hwinfo: shell command "hwinfo devid" output ignores endianness
* :github:`23441` - RFC: API change: Add I2C bus recovery API
* :github:`23438` - Cannot reset Bluetooth mesh device
* :github:`23435` - Missing documentation for macros in util.h
* :github:`23432` - Add PECI subsystem user space handlers
* :github:`23425` - Remote opencd
* :github:`23420` - PPP management don't build
* :github:`23418` - Building hello_world failed
* :github:`23415` - gen_defines does not resolve symbol values for devicetree.conf
* :github:`23414` - tests/benchmarks/timing_info  failed on mec15xxevb_assy6853 board.
* :github:`23395` - UART Console input does not work on SiFive HiFive1 on echo sample app
* :github:`23387` - [Question] Why does not zephyr use a toolchain file with cmake as -DCMAKE_TOOLCHAIN_FILE=.. ?
* :github:`23386` - SAM GMAC should support PHY link status detection
* :github:`23373` - ARM: Move CMSIS out of main tree
* :github:`23372` - arm: aarch32: spurious IRQ handler calling z_arm_reserved with wrong arguments' list
* :github:`23360` - Possible NULL dereference in  zephyr/arch/arm/include/aarch32/cortex_m/exc.h
* :github:`23353` - nrf51_ble400.dts i2c pins inverted
* :github:`23346` - bl65x_dvk boards do not reset after flashing
* :github:`23339` - tests/kernel/sched/schedule_api failed on mps2_an385 with v1.14 branch.
* :github:`23337` - USB DFU device + Composite Device with ACM Serial - Windows Fails
* :github:`23324` - TinyCBOR is not linked to application files unless CONFIG_MCUMGR is selected
* :github:`23311` - Sanitycheck flash error on frdm_k64f board.
* :github:`23309` - Sanitycheck generated incorrect acrn.xml on acrn platform
* :github:`23299` - Some bugs or dead codes cased by possible NULL pointers
* :github:`23295` - [Coverity CID :208676] Overlapping buffer in memory copy in subsys/usb/class/mass_storage.c
* :github:`23294` - [Coverity CID :208677] Unchecked return value in drivers/sensor/lis3mdl/lis3mdl_trigger.c
* :github:`23284` - driver: ethernet: Add support for a second Ethernet controller in the MCUX driver
* :github:`23280` - Bluetooth: hci_usb fails to connect to two devices with slow advertising interval
* :github:`23278` - uart_basic_api test fails for SAM family devices
* :github:`23274` - power: subsystem: Application hangs when logging is enabled after entering deep sleep
* :github:`23247` - Bluetooth LE: Add feature to allow profiles to change ADV data at RPA updates
* :github:`23246` - net: tx_bufs are not freed when NET_TCP_BACKLOG_SIZE is too high
* :github:`23226` - Bluetooth: host: Peer not resolved when host resolving is used
* :github:`23225` - Bluetooth: Quality of service: Adaptive channel map
* :github:`23222` - Bluetooth: host: Unable to pair when privacy feature is disabled by application
* :github:`23207` - tests/kernel/mem_pool/mem_pool_concept failed on mec15xxevb_assy6853 board.
* :github:`23193` - Allow overriding get_mac() function in ieee802154 drivers
* :github:`23187` - nrf_rtc_timer.c  timseout setting mistake.
* :github:`23184` - mqtt_connect fails with return -2
* :github:`23156` - App determines if Bluetooth host link request is allowed
* :github:`23153` - Binding AF_PACKET socket second time will fail with multiple network interfaces
* :github:`23133` - boards: adafruit_feather_m0: don't throw compiler warnings on using custom sercom config
* :github:`23117` - Unable to flash hello_world w/XDS-110 & OpenOCD
* :github:`23107` - Convert SAM SoC drivers to DT_INST
* :github:`23106` - timer_api intermittent failures on Nordic nRF
* :github:`23070` - Bluetooth: controller: Fix ticker implementation to avoid catch up
* :github:`23026` - missing ISR locking in UART driver?
* :github:`23001` - Implement SAM E5X GMAC support
* :github:`22997` - Add GMAC device tree definition
* :github:`22964` - Define a consistent naming convention for device tree defines
* :github:`22948` - sanitycheck --build-only followed by --test-only fails
* :github:`22911` - [Coverity CID :208407] Unsigned compared against 0 in drivers/modem/modem_pin.c
* :github:`22910` - [Coverity CID :208408] Unsigned compared against 0 in drivers/modem/modem_pin.c
* :github:`22909` - [Coverity CID :208409] Unchecked return value in tests/drivers/gpio/gpio_basic_api/src/test_deprecated.c
* :github:`22908` - [Coverity CID :208410] Unsigned compared against 0 in drivers/modem/modem_pin.c
* :github:`22907` - si7006 temperature conversion offset missing
* :github:`22903` - mcuboot/samples/zephyr (make test-good-rsa) doesn't work
* :github:`22887` - Atomic operations on pointers
* :github:`22860` - Highly accurate synchronized clock distribution for BLE mesh network
* :github:`22780` - Sanitycheck hardware map integration caused some tests failure.
* :github:`22777` - Sanitycheck hardware map integration failed with some tests timeout.
* :github:`22745` - schedule_api  fails with slice testing on frdmkw41z board on v2.2.0_rc1
* :github:`22738` - crashes in tests/kernel/mem_protect/userspace case pass_noperms_object on x86_64
* :github:`22732` - IPv6 address and prefix timeout failures
* :github:`22701` - Implement I2C driver for lpcxpresso55s69
* :github:`22679` - MQTT publish causes unnecessary TCP segmentation
* :github:`22670` - Implement GIC-based ARM interrupt tests
* :github:`22643` - [Coverity CID :208206] Unsigned compared against 0 in samples/sensor/fxos8700-hid/src/main.c
* :github:`22625` - tests/subsys/canbus/isotp/conformance fails on frdm_k64f and twr_ke18f boards
* :github:`22622` - tests/drivers/gpio/gpio_basic_api failed on multiple ARM platforms
* :github:`22561` - tests/kernel/mem_protect/syscalls fails test_string_nlen on nsim_sem
* :github:`22555` - Add support to device tree generation support for DT_NODELABEL_<node-label>_<FOO> generation
* :github:`22554` - Add support to device tree generation support for DT_PATH_<path>_<FOO> generation
* :github:`22541` - hal_nordic: nrf_glue.h change mapped assert function
* :github:`22521` - intermittent crash in tests/portability/cmsis_rtos_v2 on qemu_x86
* :github:`22502` - USB transfer warnings
* :github:`22452` - not driver found in can bus samples for olimexino_stm32
* :github:`22441` - [Coverity CID :207967] Invalid type in argument to printf format specifier in samples/drivers/spi_flash/src/main.c
* :github:`22431` - [Coverity CID :207984] Sizeof not portable in drivers/counter/counter_handlers.c
* :github:`22429` - [Coverity CID :207989] Dereference after null check in drivers/sensor/sensor_shell.c
* :github:`22421` - mbed TLS: Inconsistent Kconfig option names
* :github:`22356` - An application hook for early init
* :github:`22348` - LIS2DH SPI Support
* :github:`22270` - wrong total of testcases when sanitycheck is run with a single test
* :github:`22264` - drivers: serial: nrf_uart & nrf_uarte infinite hang
* :github:`22222` - Enabling OpenThread SLAAC
* :github:`22158` - flash_img: support arbitrary flash devices
* :github:`22083` - stm32: spi: Infinite loop of RXNE bit check
* :github:`22078` - stm32: Shell module sample doesn't work on nucleo_l152re
* :github:`22034` - Add support for USB device on STM32L1 series
* :github:`21984` - i2c_4 not working on stm32f746g_disco
* :github:`21955` - usb: tests/subsys/usb/device fails on all NXP RT boards
* :github:`21932` - Current consumption on nrf52_pca10040, power_mgr sample
* :github:`21917` - cmake error with CONFIG_COUNTER and CONFIG_BT both enabled (nrf52 board)
* :github:`21899` - STM32F769I-DISCO > microSD + FatFS > failed in "samples/subsys/fs/fat_fs" > CMD0 and 0x01
* :github:`21877` - tests/drivers/uart/uart_async_api fails on qemu_cortex_m0
* :github:`21833` - SRAM not sufficient when building BT Mesh developer guide build on BBC Micro-bit
* :github:`21820` - docs: "Crypto Cipher" API isn't available in the docs
* :github:`21755` - tests/drivers/adc/adc_api  failed on  mec15xxevb_assy6853 board.
* :github:`21706` - Link to releases in README.rst give a 404 error
* :github:`21701` - [Coverity CID :206600] Logically dead code in drivers/crypto/crypto_mtls_shim.c
* :github:`21677` - [Coverity CID :206388] Unrecoverable parse warning in subsys/cpp/cpp_new.cpp
* :github:`21675` - [Coverity CID :206390] Unrecoverable parse warning in subsys/cpp/cpp_new.cpp
* :github:`21514` - Logging - strange behaviour with RTT on nRF53
* :github:`21513` - NULL parameter checks in Zephyr APIs
* :github:`21500` - RFC: k_thread_join()
* :github:`21469` - ARC SMP is mostly untested in sanitycheck
* :github:`21455` - driver: subsys: sdhc: USAGE FAULT trace and no cs control
* :github:`21441` - Add UART5 on B-port to H7 pinmux
* :github:`21426` - civetweb triggers an error on Windows with Git 2.24
* :github:`21390` - BLE Incomplete Connect results in subsquent encryption failures
* :github:`21372` - cc26x2r1_launchxl build passed, but can't flash
* :github:`21369` - devicetree: clearly define constraints on identifier/property name conflicts
* :github:`21321` - error update for project civetweb
* :github:`21305` - New Kernel Timeout API
* :github:`21253` - 2.2 Release Checklist
* :github:`21201` - ARM: Core Stack Improvements/Bug fixes for 2.2 release
* :github:`21200` - Replace IWDG_STM32_START_AT_BOOT by WDT_DISABLE_AT_BOOT
* :github:`21158` - Giving Semaphore Limit+1 can cause limit+1 takes
* :github:`21156` - Interrupts do not work on UP Squared board
* :github:`21107` - LL_ASSERT and 'Imprecise data bus error' in LL Controller
* :github:`21093` - put sys_trace_isr_enter/sys_trace_isr_exit to user care about ISR instead of every ISR
* :github:`21088` - Bluetooth: Mesh: Send Model Message shouldn't require explicit NetKey Index
* :github:`21068` - Conflicting documentation for device initialization
* :github:`20993` - spinlock APIs need documentation
* :github:`20991` - test_timer_duration_period fails with stm32 lptimer
* :github:`20945` - samples/synchronization fails on nsim_hs_smp and nsim_sem_normal
* :github:`20876` - [Coverity CID :205820] Memory - corruptions in tests/crypto/tinycrypt/src/cmac_mode.c
* :github:`20875` - [Coverity CID :205840] Memory - corruptions in tests/benchmarks/mbedtls/src/benchmark.c
* :github:`20874` - [Coverity CID :205805] Memory - corruptions in tests/benchmarks/mbedtls/src/benchmark.c
* :github:`20873` - [Coverity CID :205782] Memory - corruptions in tests/benchmarks/mbedtls/src/benchmark.c
* :github:`20835` - [Coverity CID :205797] Control flow issues in drivers/flash/spi_nor.c
* :github:`20825` - stm32: dma: enable dma with peripheral using DMAMUX
* :github:`20699` - Each board should have a list of Kconfig options supported
* :github:`20632` - call to bt_gatt_hids_init influences execution time of work queue
* :github:`20604` - log will be discarded before logging_thread scheduled once
* :github:`20585` - z_clock_announce starvation with timeslicing active
* :github:`20492` - [Coverity CID :205653]Control flow issues in /drivers/dma/dma_stm32_v1.c
* :github:`20491` - [Coverity CID :205644]Control flow issues in /drivers/dma/dma_stm32_v1.c
* :github:`20348` - Convert remaining entropy to Devicetree
* :github:`20330` - devicetree Arduino bindings do not support identification of bus controllers
* :github:`20301` - tests/drivers/watchdog/wdt_basic_api failed on mec15xxevb_assy6853 board.
* :github:`20259` - Bluetooth: Mesh: Network management
* :github:`20137` - posix: undefined reference with --no-gc-sections
* :github:`20136` - kernel: undefined reference with --no-gc-sections
* :github:`20068` - Application doesn't start when SHELL-UART is enabled and UART is not connected on STM32F0
* :github:`19869` - Implement tickless capability for xlnx_psttc_timer
* :github:`19852` - Add support for GPIO AF remap on STM32F1XX
* :github:`19837` - SS register is 0 when taking exceptions on qemu_x86_long
* :github:`19813` - tests/crypto/rand32 failed on sam_e70 board on v1.14 branch.
* :github:`19763` - tests/subsys/usb/device/ failed on mimxrt1050_evk board.
* :github:`19614` - Make zephyr_library out of hal_stm32 and hal_st
* :github:`19550` - drivers/pcie: ``pcie_get_mbar()`` should return a ``void *`` not ``u32_t``
* :github:`19487` - tests/kernel/fifo/fifo_usage GPF crash on qemu_x86_long
* :github:`19456` - arch/x86: make use of z_bss_zero() and z_data_copy()
* :github:`19353` - arch/x86: QEMU doesn't appear to support x2APIC
* :github:`19307` - _interrupt_stack is defined in the kernel, but declared in arch headers
* :github:`19285` - devicetree: fixed non-alias reference to specific nodes
* :github:`19235` - move drivers/timer/apic_timer.c to devicetree
* :github:`19219` - drivers/i2c/i2c_dw.c is not 64-bit clean
* :github:`19144` - arch/x86: CONFIG_BOOT_TIME_MEASUREMENT broken
* :github:`19075` - k_delayed_work_submit() does not handle long delays correctly
* :github:`19067` - non-overlapping MPU gap-filling needs to be optional
* :github:`19038` - [zephyr branch 1.14 and master -stm32-netusb]:errors when i view RNDIS Device‘s properties on Windows 10
* :github:`18956` - memory protection for x86 dependent on XIP
* :github:`18940` - Counter External Trigger
* :github:`18808` - Docs for gpmrb board incorrectly refer to up_squared board
* :github:`18787` - arch/x86: retire loapic_timer.c driver in favor of new apic_timer.c
* :github:`18657` - drivers/timer/hpet.c should use devicetree, not CONFIG_* for MMIO/IRQ data
* :github:`18614` - same70 hsmci interface
* :github:`18568` - Support for Particle Photon
* :github:`18435` - [Coverity CID :203481]API usage errors in /tests/crypto/tinycrypt/src/test_ecc_utils.c
* :github:`18425` - [Coverity CID :203498]Memory - corruptions in /tests/application_development/gen_inc_file/src/main.c
* :github:`18422` - [Coverity CID :203415]Memory - illegal accesses in /subsys/shell/shell_telnet.c
* :github:`18389` - [Coverity CID :203396]Null pointer dereferences in /subsys/bluetooth/mesh/access.c
* :github:`18386` - [Coverity CID :203443]Memory - corruptions in /subsys/bluetooth/host/rfcomm.c
* :github:`18263` - flash sector erase fails on stm32f412
* :github:`18207` - tests/bluetooth/hci_prop_evt fails with code coverage enabled in qemu_x86
* :github:`18124` - synchronization example fails to build for SMP platforms
* :github:`18118` - samples/subsys/console doesn't work with qemu_riscv32
* :github:`18106` - Only 1 NET_SOCKET_OFFLOAD driver can be used
* :github:`18085` - I2C log level ignored
* :github:`18050` - BT Host - Advertisement extensions support
* :github:`18047` - BT Host: Advertising Extensions - Advertiser
* :github:`18046` - BT Host: Advertising Extensions - Scanner
* :github:`18044` - BT Host: Advertising Extensions - Periodic Advertisement Synchronisation (Rx)
* :github:`18042` - Only corporate members can join the slack channel
* :github:`17892` - arch/x86: clean up segmentation.h
* :github:`17888` - arch/x86: remove IAMCU ABI support
* :github:`17775` - Microchip XEC rtos timer should be using values coming from DTS
* :github:`17755` - ARC privilege mode stacks waste memory due to alignment requirements
* :github:`17735` - abolish Z_OOPS() in system call handlers
* :github:`17543` - dtc version 1.4.5 with ubuntu 18.04 and zephyr sdk-0.10.1
* :github:`17508` - RFC: Change/deprecation in display API
* :github:`17443` - Kconfig: move arch-specific stack sizes to arch trees?
* :github:`17430` - arch/x86: drivers/interrupt_controller/system_apic.c improperly classifies IRQs
* :github:`17415` - Settings Module - settings_line_val_read() returning -EINVAL instead of 0 for deleted setting entries
* :github:`17361` - _THREAD_QUEUED overlaps with x86 _EXC_ACTIVE in k_thread.thread_state
* :github:`17324` - failing bluetooth tests with code coverage enabled in qemu_x86
* :github:`17323` - failing network tests with code coverage enabled in qemu_x86
* :github:`17240` - add arc support in Zephyr's openthread
* :github:`17234` - CONFIG_KERNEL_ENTRY appears to be superfluous
* :github:`17166` - arch/x86: eliminate support for CONFIG_REALMODE
* :github:`17135` - Cannot flash LWM2M example for ESP32
* :github:`17133` - arch/x86: x2APIC EOI should be inline
* :github:`17104` - arch/x86: fix -march flag for Apollo Lake
* :github:`17064` - drivers/serial/uart_ns16550: CMD_SET_DLF should be removed
* :github:`16988` - Packet isn't received by server during stepping
* :github:`16902` - CMSIS v2 emulation assumes ticks == milliseconds
* :github:`16886` - Bluetooth Mesh: Receive segmented message multiple times
* :github:`16721` - PCIe build warnings from devicetree
* :github:`16720` - drivers/loapic_timer.c is buggy, needs cleanup
* :github:`16649` - z_init_timeout() ignores fn parameter
* :github:`16587` - build failures with gcc 9.x
* :github:`16436` - Organize generated include files
* :github:`16385` - watch dog timer causes the reboot on SAME70 board
* :github:`16330` - LPCXpresso55S69 secure/non-secure configuration
* :github:`16196` - display_mcux_elcdif driver full support frame buffer features
* :github:`16122` - Detect first block in LWM2M firmware updates.
* :github:`16096` - Sam gmac Ethernet driver should be able to detect the carrier state
* :github:`16072` - boards/up_squared: k_sleep() too long with local APIC timer
* :github:`15903` - Documentation missing for SPI and ADC async operations
* :github:`15680` - "backport v1.14 branch" label: update description and doc
* :github:`15565` - undefined references to ``sys_rand32_get``
* :github:`15504` -  Can I use one custom random static bd_addr before provision?
* :github:`15499` - gpio_intel_apl: gpio_pin_read() pin value doesn't match documentation
* :github:`15463` - soc/x86/apollo_lake/soc_gpio.h: leading zeros on decimal constants
* :github:`15449` - tests/net/ieee802154/crypto: Assertion Failure:  ds_test(dev) is false
* :github:`15343` - tests/kernel/interrupt: Assertion Failure in test_prevent_interruption
* :github:`15304` - merge gen_kobject_list.py and gen_priv_stacks.py
* :github:`15202` - tests/benchmarks/timing_info measurements are suddenly higher than previous values on nrf52_pca10040
* :github:`15181` - ztest issues
* :github:`15177` - samples/drivers/crypto:  CBC and CTR mode not supported
* :github:`14972` - samples: Create README.rst
* :github:`14790` - google_iot_mqtt sample does not work with qemu_x86 out of the box
* :github:`14763` - PCI debug logging cannot work with PCI-enabled NS16550
* :github:`14749` - Verify all samples work as intended
* :github:`14647` - IP: Zephyr replies to broadcast ethernet packets in other subnets on the same wire
* :github:`14591` - Infineon Tricore architecture support
* :github:`14540` - kernel: message queue MACRO not compatible with C++
* :github:`14302` - USB MSC fails USB3CV tests
* :github:`14173` - Configure QEMU to run independent of the host clock
* :github:`14122` - CONFIG_FLOAT/CONFIG_FP_SHARING descriptions are confusing and contradictory
* :github:`14099` - Minnowboard doesn't build tests/kernel/xip/
* :github:`13963` - up_squared: evaluate removal of SBL-related special configurations
* :github:`13821` - tests/kernel/sched/schedule_api: Assertion failed for test_slice_scheduling
* :github:`13783` - tests/kernel/mem_protect/stackprot failure in frdm_k64f due to limited privilege stack size
* :github:`13569` - ZTEST: Add optional float/double comparison support
* :github:`13468` - tests/drivers/watchdog/wdt_basic_api/testcase.yaml: Various version of "Waiting to restart MCU"
* :github:`13353` - z_timeout_remaining should subtract z_clock_elapsed
* :github:`12872` - Update uart api tests with configure/configure_get apis
* :github:`12775` - USB audio isochronous endpoints
* :github:`12553` - List of tests that keep failing sporadically
* :github:`12478` - tests/drivers/ipm/peripheral.mailbox failing sporadically on qemu_x86_64 (timeout)
* :github:`12440` - Device discovery of direct advertising devices is not working
* :github:`12385` - Support touch button
* :github:`12264` - kernel: poll: outdated check for expired timeout
* :github:`11998` - intermittent failures in tests/kernel/common: test_timeout_order: (poll_events[ii].state not equal to K_POLL_STATE_SEM_AVAILABLE)
* :github:`11928` - nRF UART nrfx drivers (nRF UARTE 0) won't build
* :github:`11916` - ISR table (_sw_isr_table) generation is fragile and can result in corrupted binaries
* :github:`11745` - logging: never leaves panic mode on fatal thread exception
* :github:`11261` - ARM Cortex-M4 (EFR32FG1P) MCU fails to wake up from sleep within _sys_soc_suspend()
* :github:`11149` - subsys/bluetooth/host/rfcomm.c: Missing unlock
* :github:`11016` - nRF52840-PCA10056/59: Cannot bring up HCI0 when using HCI_USB sample
* :github:`9994` - irq_is_enabled not available on nios2
* :github:`9962` - Migrate sensor drivers to device tree
* :github:`9953` - wrong behavior in pthread_barrier_wait()
* :github:`9741` - tests/kernel/spinlock:kernel.multiprocessing.spinlock_bounce crashing on ESP32
* :github:`9711` - RFC: Zephyr should provide a unique id interface
* :github:`9608` - Bluetooth: different transaction collision
* :github:`9566` - Unclear definition of CONFIG_IS_BOOTLOADER
* :github:`8139` - Driver for BMA400 accelerometer
* :github:`7868` - Support non-recursive single-toolchain multi-image builds
* :github:`7564` - dtc: define list of acceptable warnings (and silent them with --warning -no<warnign-name> option)
* :github:`6648` - Trusted Execution Framework: practical use-cases (high-level overview)
* :github:`6015` - PWM on 32bit arch can get 0 pulse_cycle because of 64bit calculation
* :github:`5857` - net: TCP retransmit queue implementation is broken
* :github:`5408` - Improve docs & samples on device tree overlay
* :github:`4985` - TEE support for ARMv8-M
* :github:`4911` - Filesystem support for qemu
* :github:`4832` - disco_l475_iot1: Provide 802.15.4 Sub-GHz
* :github:`4475` - Add support for Rigado BMD-3XX-EVAL boards
* :github:`4412` - Replace STM32 USB driver with DWC
* :github:`4326` - Port Zephyr to Cypress PSoC 6 MCU's
* :github:`3909` - Add Atmel SAM QDEC Driver
* :github:`3730` - ESP32: DAC Driver support
* :github:`3729` - ESP32 ADC Driver Support
* :github:`3727` - ESP32: SPI Driver Support
* :github:`3726` - ESP32: DMA Driver Support
* :github:`3694` - i2c: Drivers are not thread safe
* :github:`3668` - timeslice reset is not tested for interrupt-induced swaps
* :github:`3564` - Requires more UART samples for STM32 Nucleo/similar boards
* :github:`3285` - Allow taking advantage of HW-based AES block cipher
* :github:`3232` - Add ksdk dma shim driver
* :github:`3076` - Add support for DAC (Digital to Analog Converter) drivers
* :github:`2585` - Support for LE legacy out-of-band pairing
* :github:`2566` - Create a tool for finding out stack sizes automatically.
* :github:`1900` - Framework for Trusted Execution Environment
* :github:`1894` - Secure Key Storage
* :github:`1333` - Provide build number in include/generated/version.h
