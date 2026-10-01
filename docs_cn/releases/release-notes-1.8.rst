.. _zephyr_1.8:

Zephyr 内核 1.8.0
####################

我们很高兴宣布 Zephyr 内核 1.8.0 版本的发布。

本版本的主要增强功能包括：

* 无滴答内核
* IP 协议栈改进
* Bluetooth 5.0 特性
* 生态系统：通过第三方工具（openocd、Segger Systemview）进行跟踪、调试支持
* 改进 Mac 和 Windows 开发环境上的构建支持
* Xtensa GCC 支持
* MMU/MPU 支持的初始实现
* 扩展的设备支持

以下章节提供了按组件划分的详细变更列表。

内核
******

* 内核使用 k_cycle_get_32 而非 sys_cycle_get_32
* 为内核新增 k_panic() 和 k_oops() API
* 为内核新增 k_thread_create() API
* 为内核新增 k_queue API
* 新增无滴答内核支持

架构
*************

* arm：更新 core 以使用 struct k_thread
* arm：新增 ARM MPU 支持
* dts：新增 ARM CMSDK 支持
* arm：新增 NXP MPU 的初始支持
* arm：为基于 nRF52832 SoC 的板卡新增设备树支持
* arm：修复 nRF52840-QIAA SoC 的设备树支持
* arm：为 nRF52840 SoC 与板卡新增设备树支持
* arm：为 nRF51822 SoC 与板卡新增设备树支持
* dts：引入 st/mem.h 用于 FLASH 与 SRAM 大小
* dts：将 IRQ 优先级放入 interrupt 属性
* arm：支持 MKL25Z soc
* arm：新增 FPU 支持
* x86：定义 MMU 数据结构
* 新增对 ARC EM Starter Kit 版本 2.3 的支持



板卡
******

* 新增 qemu_xtensa 板卡定义
* 新增信息更丰富的 page fault 处理器 x86 板卡
* xtensa：构建与其他 Zephyr 架构类似
* 为 x86 板卡定义 MMU 数据结构
* 新增对板卡 disco_l475_iot1 的支持
* 新增 STM32F413 Nucleo 板卡
* 新增对 CC3220SF_LAUNCHXL 板卡的支持
* 支持新的 ARM 板卡 FRDM-KL25Z
* arduino_101 板卡默认启用 GPIO
* boards：转换为使用新引入的整型大小类型
* arm：新增对 Nucleo L432KC 板卡的支持
* arm：新增对 STM32L496G Discovery 板卡的支持
* arm：新增对 STM32F469I-DISCO 板卡的支持
* BBC micro:bit：为 5x5 LED 显示新增驱动与 API

驱动程序与传感器
*******************

* UART 中断驱动 API 定义更清晰
* 支持 pull 式控制台 API
* 新增 nRF5 IEEE 802.15.4 无线电驱动
* 新增 KW41Z IEEE 802.15.4 无线电驱动
* 新增 MCUX TRNG 驱动
* 新增对 SiFive Freedom E310 pinmux 驱动的支持
* drivers/sensor：将格式化字符串转换为使用 PRI 定义
* 新增 lps22hb 传感器驱动
* 新增 lsm6dsl 传感器驱动
* 新增心率传感器驱动
* 新增对 max30101 心率传感器的支持
* 新增对 lis2dh 加速度计的支持

网络
**********

* 新增 HTTPS 服务器支持
* 新增 HTTP Basic-Auth 支持
* 新增 IPv6 分片支持
* 为 well-known 响应为 CoAP 新增块传输支持
* 网络缓冲区处理的重大重构
* 如果配置中启用，开始收集 TCP 统计信息
* 新增 IEEE 802.15.4 安全支持
* 新增 DNS 解析器示例应用
* 新增 IPv6 多播监听器（MLDv2）支持
* 新增 NATS 协议示例应用
* HTTP 客户端和服务器连接性修复
* 网络示例 Coverity 修复
* 网络示例 llvm 编译器警告修复
* MQTT 发布者连接性修复
* 6lo IPv6 报头压缩修复
* CoAP 连接性修复
* DHCPv4 连接性修复
* TCP 连接性修复
* DNS 文档和连接性修复
* IPv6 连接性修复
* IPv4 ARP 修复
* IEEE 802.15.4 配置调整修复
* 移除 ORFD（Overly Reduced Function Device）802.15.4 支持
* 网络卸载驱动修复
* 修复各种内存泄漏
* 在接受数据包前正确检查 TCP 和 UDP 校验和
* 按正确顺序启动 RX 和 TX 网络线程
* 网络示例文档修复与澄清
* RPL 网格路由修复
* 网络链路（MAC）地址修复

蓝牙
*********

* Host：为流控制强制新增 ATT 和 SMP 数据包跟踪
* Host：GATT 数据库变更为链表，为动态分配做准备
* Bluetooth 5.0：控制器自报为 5.0-capable
* Bluetooth 5.0：引入通道选择算法 #2 支持
* Bluetooth 5.0：新增多 PHY 支持，包括 2Mbit/s 和长距离编码
* Bluetooth 5.0：集成 Scan Request 通知
* Controller：新增低占空比定向广播支持
* Controller：新增扫描重复过滤支持
* Controller：在控制器中强制完整的角色分离，以实现更小的构建
* Controller：引入高级控制器配置，含若干新的 Kconfig 选项
* Controller：将无线电中断变更为直接 ISR，以减少中断延迟
* 在 Host 和 Controller 中新增 HCI 控制器到 Host 流控制支持
* BR/EDR：新增 HFP (e)SCO 音频信道建立支持
* BR/EDR：新增对功能性 SDP 服务器的支持

构建与基础设施
************************

* 支持构建主机工具
* 新增独立的 DTS 目标
* 新增对 MSYS2 的支持
* 使用 -O2 而非 -Os 用于 SDK 0.9 的 ARC

库
*********

* 新增软件驱动 I2C 库
* 创建 HTTP 库
* 新增 HTTP 服务器库支持
* 新增最小 JSON 库
* 将 TinyCrypt 更新至 0.2.6 版本
* 新增最小 JSON 库

HAL
****

* 新增 Atmel SAM 家族 I2C (TWIHS) 驱动
* 新增 Atmel SAM 串口 (UART) 驱动
* 为 Atmel SAM SoC 新增 WDT 驱动
* 新增 Atmel SAM4S SoC 支持
* 导入 Nordic 802.15.4 无线电驱动
* 新增 NXP MPU 的初始支持
* 将 QMSI 更新至 1.4 RC4
* 新增 FPU 支持
* 新增对 STM32F413 的基本支持
* 引入 STM32F4x DMA 驱动
* pinmux：stm32：新增对 Nucleo L432KC 的支持
* 新增对 STM32L496G Discovery 板卡的支持
* 为 STM32F407 新增 dts
* 新增对 STM32F4DISCOVERY Board 的支持
* 新增对 STM32F469XI 的支持
* 新增对 STM32F469I-DISCO 的支持

文档
*************

* 为新板卡移植新增板卡文档
* 新增板卡移植指南
* 在移植和用户指南中新增安全章节
* 继续将 wiki.zephyrproject.org 材料迁移到网站和 github wiki
* 改进生成文档的 CSS 格式和外观
* 新增带内核版本号的面包屑导航头
* 更新 Linux、Windows 和 macOS 的入门设置指南
* 更新和新增以跟随新的和更新的内核特性
* 损坏链接和拼写检查扫描
* 从网站移除已弃用的内核文档（1.6 发布前）（如需要仍可在 git 仓库中获取）

测试与示例
*****************

* 新增测试以验证相同 tick 超时到期顺序
* 为内核新增 clock_test
* 新增无滴答测试
* 新增简单的 CC2520 crypto dev 测试
* 为 Bluetooth 示例新增组合 observer 与 broadcaster 应用
* 新增同时等待 IPv4 和 IPv6 的支持
* 在某些应用中启用无滴答内核选项

JIRA 相关条目
******************

.. comment  List derived from Jira query: ...

* ``ZEP-248`` - 新增 BOARD/SOC 移植指南
* ``ZEP-339`` - 无滴答内核
* ``ZEP-540`` - 新增异步传输回调的 API
* ``ZEP-628`` - 验证 RPL 路由节点支持
* ``ZEP-638`` - 考虑的特性：在可能时于构建时标记缺失的功能
* ``ZEP-720`` - 新增 MAX30101 心率传感器驱动
* ``ZEP-828`` - IPv6 - 多播加入/离开支持
* ``ZEP-843`` - 统一的 assert/不可恢复错误基础设施
* ``ZEP-888`` - 802.15.4 - 安全支持
* ``ZEP-932`` - 适配内核示例与测试项目
* ``ZEP-948`` - 重新审视时间片算法
* ``ZEP-973`` - 移除与设备 PM 函数和 DEVICE\_ 和 SYS\_* 宏相关的已弃用 API
* ``ZEP-1028`` - 缩小 k_block 结构体大小
* ``ZEP-1032`` - IPSP 路由器角色支持
* ``ZEP-1169`` - 在以太网驱动上示例 mbedDTLS DTLS 客户端稳定性
* ``ZEP-1171`` - 事件组内核 API
* ``ZEP-1280`` - 提供事件队列对象
* ``ZEP-1313`` - 移植和用户指南必须包含安全章节
* ``ZEP-1326`` - 清理 _THREAD_xxx API
* ``ZEP-1388`` - 新增对 KW40 SoC 的支持
* ``ZEP-1391`` - 新增对 Hexiwear KW40 的支持
* ``ZEP-1392`` - 新增 FXAS21002 陀螺仪传感器驱动
* ``ZEP-1435`` - 改进 Quark SE C1000 ARC 浮点性能
* ``ZEP-1438`` - AIO：AIO Comparator 在 D2000 和 Arduino101 上不稳定
* ``ZEP-1463`` - 在 segger SystemView 中新增 Zephyr 支持
* ``ZEP-1500`` - net/mqtt：MQTT 高级 API 的测试用例
* ``ZEP-1528`` - 为多核应用提供模板
* ``ZEP-1529`` - 无法退出 menuconfig
* ``ZEP-1530`` - menuconfig 底部菜单的热键有时不工作
* ``ZEP-1568`` - 用直接 CMSIS-core 调用替换 arm cortex_m scs 和 scb 功能
* ``ZEP-1586`` - menuconfig：Backspace 损坏
* ``ZEP-1599`` - printk() 对格式字符串中 '-' 指示符（左对齐）的支持
* ``ZEP-1607`` - JSON 编码/解码库
* ``ZEP-1621`` - 栈监控
* ``ZEP-1631`` - 从 ISR 使用 k_mem_pool_alloc（或类似 API）的能力
* ``ZEP-1684`` - 新增 Atmel SAM 家族看门狗 (WDT) 驱动
* ``ZEP-1695`` - 支持 ADXL362 传感器
* ``ZEP-1698`` - BME280 对 SPI 通信的支持
* ``ZEP-1711`` - xtensa 构建定义小写名称的 Kconfigs
* ``ZEP-1718`` - 对 IPv6 分片的支持
* ``ZEP-1719`` - TCP 与 6lo 不兼容
* ``ZEP-1721`` - 许多 TinyCrypt 测试用例仅在 ARM 和 x86 上运行
* ``ZEP-1722`` - xtensa：TinyCrypt 无法构建
* ``ZEP-1735`` - 控制器到 Host 流控制
* ``ZEP-1759`` - 构建所需的所有 python 脚本应迁移到 python 3 以最小化依赖
* ``ZEP-1761`` - 使用 ISSM 工具链的 llvm/icx 构建时 K_MEM_POOL_DEFINE 构建错误 "invalid register name"
* ``ZEP-1769`` - 实现 Set Event Mask 和 LE Set Event Mask 命令
* ``ZEP-1772`` - 重新引入控制器到 host 流控制
* ``ZEP-1776`` - 从 RX 线程发送 LE COC 数据可能导致死锁
* ``ZEP-1785`` - Tinytile：此板卡不支持烧录
* ``ZEP-1788`` - [REG] bt_enable：未注册 HCI 驱动
* ``ZEP-1800`` - 将外部 mbed TLS 库更新至最新版本（2.4.2）
* ``ZEP-1812`` - 在 HPET 定时器中新增无滴答内核支持
* ``ZEP-1816`` - 在 LOAPIC 定时器中新增无滴答内核支持
* ``ZEP-1817`` - 在 ARCV2 定时器中新增无滴答内核支持
* ``ZEP-1818`` - 在 cortex_m_systick 定时器中新增无滴答内核支持
* ``ZEP-1821`` - 更新 PM 应用以使用 mili/micro 秒而非 ticks
* ``ZEP-1823`` - 改进的基准测试
* ``ZEP-1825`` - 上下文切换 KPI
* ``ZEP-1836`` - 将当前 ecb_encrypt() 公开为 bt_encrypt()，以便 host 可以直接访问
* ``ZEP-1856`` - 移除旧版 micro/nano 内核 API
* ``ZEP-1857`` - 使用 LLVM/icx (bluetooth_handsfree) 的构建警告 [-Wpointer-sign]
* ``ZEP-1866`` - 新增 Atmel SAM 家族 I2C (TWIHS) 驱动
* ``ZEP-1880`` - "samples/grove/temperature"：生成 configure 文件时出现警告
* ``ZEP-1886`` - 使用 LLVM/icx (tests/net/nbuf) 的构建警告 [-Wpointer-sign]
* ``ZEP-1887`` - 使用 LLVM/icx (tests/drivers/spi/spi_basic_api) 的构建警告 [-Wpointer-sign]
* ``ZEP-1893`` - openocd：'make flash' 仅对 Zephyr SDK 有效，对所有其他工具链失败
* ``ZEP-1896`` - [PTS] L2CAP/LE/CFC/BV-06-C
* ``ZEP-1899`` - 缺少 xtensa/xt-sim 的板卡文档
* ``ZEP-1908`` - 缺少 arm/nucleo_96b_nitrogen 的板卡文档
* ``ZEP-1910`` - 缺少 arm/96b_carbon 的板卡文档
* ``ZEP-1927`` - AIO：AIO_CMP_POL_FALL 在 aio_cmp_configure 后立即触发
* ``ZEP-1935`` - 数据包丢失使 RPL 网格更易受攻击
* ``ZEP-1936`` - tests/drivers/spi/spi_basic_api/testcase.ini#test_spi - 断言失败
* ``ZEP-1946`` - 到下一事件的时间
* ``ZEP-1955`` - 嵌套中断在 Xtensa 架构上崩溃
* ``ZEP-1959`` - 新增 Atmel SAM 家族串口 (UART) 驱动
* ``ZEP-1965`` - net-tools HEAD 对 QEMU/TAP 损坏
* ``ZEP-1966`` - 似乎无法通过本地地址同时发送和接收
* ``ZEP-1968`` - "make mrproper" 移除顶层 dts/ 目录，之后导致 ARM 构建失败
* ``ZEP-1980`` - 将 app_kernel 基准测试迁移到统一内核
* ``ZEP-1984`` - net_nbuf_append()、net_nbuf_append_bytes() 存在数据完整性问题
* ``ZEP-1990`` - BBC micro:bit LED 显示的基本支持
* ``ZEP-1993`` - CDC_ACM 需要流控制
* ``ZEP-1995`` - samples/subsys/console 破坏 xtensa 构建
* ``ZEP-1997`` - 如果存在协处理器，启动期间崩溃
* ``ZEP-2008`` - 将无滴答 idle 测试移植到统一内核并清理
* ``ZEP-2009`` - 将 test_sleep 测试移植到统一内核并清理
* ``ZEP-2011`` - 通过 CoAP 请求获取 RPL 节点信息
* ``ZEP-2012`` - 无法访问未对齐内存的内核的网络协议栈存在故障
* ``ZEP-2013`` - 死对象监控代码
* ``ZEP-2014`` - 默认 samples/subsys/shell/shell 在 QEMU RISCv32 / NIOS2 上构建失败
* ``ZEP-2019`` - 启用 CONFIG_TICKLESS_IDLE 时 Xtensa 移植无法编译
* ``ZEP-2027`` - Bluetooth Peripheral 示例无法与某些 Android 设备配对
* ``ZEP-2029`` - xtensa：irq_offload() 在 XRC_D2PM 上不工作
* ``ZEP-2033`` - 通道选择算法 #2
* ``ZEP-2034`` - 高占空比不可连接广播
* ``ZEP-2037`` - 畸形 echo 响应
* ``ZEP-2048`` - 将 UART "baud-rate" 属性变更为 "current-speed"
* ``ZEP-2051`` - 从 C99 类型迁移到 zephyr 定义的类型
* ``ZEP-2052`` - arm：线程中未处理的异常导致整个系统宕机
* ``ZEP-2055`` - 为 github 在项目根目录新增 README.rst
* ``ZEP-2057`` - qemu_x86 上 tests/net/rpl 崩溃导致 sanitycheck 间歇性失败
* ``ZEP-2061`` - samples/net/dns_resolve 网络设置/README 令人困惑
* ``ZEP-2064`` - RFC：使 net_shell 命令处理器可复用
* ``ZEP-2065`` - struct dns_addrinfo 有未使用的字段
* ``ZEP-2066`` - 挑剔：与大多数 OS 相比 SOCK_STREAM/SOCK_DGRAM 值被交换
* ``ZEP-2069`` - samples：net：dhcpv4_client：在 frdm k64f 板卡上运行失败
* ``ZEP-2070`` - 从 bluetooth 的 ipsp 发送数据后 net pkt 未完全 unref
* ``ZEP-2076`` - samples：net：coaps_server：构建失败
* ``ZEP-2077`` - 使用 CONFIG_NET_L2_BLUETOOTH_ZEP1656 时修复 IID
* ``ZEP-2080`` - 20-30 分钟后 RPL 节点无响应。
* ``ZEP-2092`` - [NRF][BT] Makefile:946: recipe for target 'include/generated/generated_dts_board.h' failed
* ``ZEP-2114`` - tests/kernel/fatal : 对 QC1000/arc 失败
* ``ZEP-2125`` - 通过 menuconfig 启用 UART1 端口时编译错误
* ``ZEP-2132`` - 构建 samples/bluetooth/hci_uart 失败
* ``ZEP-2138`` - 发现静态代码扫描（coverity）问题
* ``ZEP-2143`` - Windows 10 上使用 MSYS2 编译错误
* ``ZEP-2152`` - 带协处理器的核心 Xtensa 启动时崩溃
* ``ZEP-2178`` - 发现静态代码扫描（coverity）问题
