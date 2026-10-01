:orphan:

.. _zephyr_1.9:

Zephyr 内核 1.9.2
###################

这是一个包含修复的维护版本。

内核
******
* 通用队列项获取已修复，使用 K_FOREVER 时始终返回有效项

蓝牙
*********
* BLE Mesh 的多个稳定性修复
* BLE Controller 的多个稳定性修复

Zephyr 内核 1.9.1
###################

这是一个包含修复和 BLE Controller 中两个新特性的维护版本。

驱动程序与传感器
*******************
* 修复 mcux 以太网驱动缓冲区溢出
* 修复 STM32 PWM 预分频器问题

网络
**********
* 修复 DNS 中对 IPv6 的支持

蓝牙
*********
* BLE Controller 的多个稳定性修复
* BLE Controller 中对 PA/LNA 放大器的支持
* BLE Controller 中对额外 VS 命令的支持

Zephyr 内核 1.9.0
###################

我们很高兴宣布 Zephyr 内核 1.9.0 版本的发布

本版本计划的主要增强功能包括：

* Bluetooth 5.0 支持（除广播扩展外的所有特性）
* 通过 Bluetooth 认证的 BLE Controller
* BLE Mesh
* 轻量级机器对机器（LwM2M）支持
* Pthreads 兼容 API
* BSD Sockets 兼容 API
* MMU/MPU（续）：线程隔离、分页
* 将设备树支持扩展到更多架构
* 改版测试套件，增加覆盖率
* 栈哨兵支持（详见下文）

以下章节提供了按组件划分的详细变更列表。

内核
******

* 为内核新增 POSIX 线程 IPC 支持
* kernel：为栈引入不透明数据类型
* 时间片和无滴答内核改进

架构
*************

* arm：新增 STM32F405、STM32F417、STM32F103x8 SoC
* arm：新增 TI CC2650 SoC
* arm：移除 TI CC3200 SoC
* arm：为 nRF52、STM32L4 和 STM32F3 新增 MPU 支持
* xtensa：新增 ESP32 支持
* 栈哨兵：在栈内存区域的最低 4 字节放置哨兵值，
  并在包括服务中断或上下文切换在内的多个时间点检查它。
* x86：为应用内存启用 MMU
* ARC：新增初始 MPU 支持，包括为 ARC 配置检查栈哨兵
  （针对不具备硬件栈边界检查功能的配置）
* ARC：支持普通、非 FIRQ 中断的嵌套中断

板卡
******

* 为基于 Intel Quark 的单片机板卡新增设备树支持，
  例如 Arduino_101、tinytile 和 Quark_d2000_crb。
* arm：新增 Atmel SAM4S Xplained 板卡
* arm：新增 Olimex STM32-E407 和 STM32-P405 板卡
* arm：新增 STM32F412 Nucleo 和 STM32F429I-DISC1 板卡
* arm：新增 TI SensorTag 板卡
* arm：移除 TI CC3200 LaunchXL 板卡
* arm：新增 VBLUno51 和 VBLUno52 板卡
* xtensa：新增 ESP32 板卡支持
* ARC：新增对 EMSK EM7D v2.2 版本（含 MPU）的支持
* ARC：板卡配置重组，外设配置从 soc 迁移到
  板卡级别

驱动程序与传感器
*******************

* 新增 KW40Z IEEE 802.15.4 无线电驱动支持
* 新增 APDS9960 传感器驱动
* 为 nrf RTC Timer 新增 TICKLESS KERNEL 支持
* 新增 Kinetis adc 和 pwm 驱动
* 移除已弃用的 PWM 驱动 API
* 为 ESP32 新增 GPIO、pin mux、看门狗、随机数生成器
  和 UART 驱动
* sensor：新增 BMM150 地磁传感器驱动

网络
**********

* 新增 LWM2M 支持
* 新增 net-app API 支持。这是一个更高级的 API，
  可被应用用于创建具有透明 TLS（用于 TCP）或 DTLS（用于 UDP）
  支持的客户端/服务器应用。
* 新增 MQTT TLS 支持
* 新增自动配置 IEEE 802.15.4 和 Bluetooth IPSP 网络的支持
* 新增 TCP 接收窗口支持
* 网络示例应用配置文件统一，大部分相似配置文件被合并
* 为 HTTP(S) 服务器示例应用新增 Bluetooth 支持
* BSD Socket 兼容 API 层，允许使用广为人知的跨平台 API
  编写和/或移植简单的网络应用
* 网络 API 文档修复
* 网络 shell 增强
* Trickle 算法修复
* HTTP 服务器和客户端库改进
* CoAP API 修复
* IPv6 修复
* RPL 修复

蓝牙
*********

* Bluetooth Mesh 支持（所有必需特性和大部分可选特性）
* GATT Service Changed Characteristic 支持
* IPSP net-app 支持：一个简化的网络 API，减少了应用开发者
  连接网络时必须经历的常见任务的重复。
* BLE 控制器通过认证，所有必需测试通过
* 基于控制器的隐私（包括所有可选特性）
* 控制器中的扩展扫描器过滤策略支持
* 控制器角色（Advertiser、Scanner、Master 和 Slave）在源代码中分离，
  可条件包含
* Flash 访问与 BLE 无线电活动协作
* Bluetooth Kconfig 选项已重命名为与 Bluetooth API 相同的（一致的）
  前缀，即 BT_* 而非 BLUETOOTH_*。
  控制器 Kconfig 选项已缩短为使用 CTLR 而非 CONTROLLER。
* 移除已弃用的 NBLE 支持

构建与基础设施
************************

* 变更说明

库
*********

* mbedTLS 更新至 2.6.0
* TinyCrypt 更新至 0.2.7

HAL
****

* 新增对 stm32f417 SOC 的支持
* 新增对 stm32f405 SOC 的支持
* pinmux：stm32：96b_carbon：新增对 SPI 的支持
* 在 stm32 soc 上新增 rcc 节点
* 为 stm32l4 的 USART1 在 PB6/PB7 上新增 pin 配置
* 移除 TI cc3200 SOC 和 LaunchXL 板卡支持

文档
*************

* 新增 CONTRIBUTING.rst 和贡献指南材料
* 重新组织配置选项文档以便于访问
* 修复受支持板卡章节的导航侧边栏问题
* 修复隐藏在标题后面的链接目标
* 完成 wiki.zephyrproject.org 内容到文档和 GitHub wiki 的迁移。
  所有指向旧 wiki 的链接已更新。
* 通过 .rst、Kconfig（用于自动生成配置文档）和源代码 doxygen 注释
  （用于 API 文档）进行损坏链接和拼写检查扫描。
* 为新接口新增 API 文档，并改进现有接口的文档。
* 为随本版本支持的板卡新增文档。
* 将文档生成所需的 Python 包添加到新的 python
  pip requirements.txt


构建系统与工具
**********************
* 将后处理主机工具转换为 python，包括以下工具：
  gen_offset_header.py gen_idt.py gen_gdt.py gen_mmu.py


测试与示例
*****************

* 在 schedule_api 测试中新增测试用例以压力测试轮询调度。
* 在 scheduling_api_test 中新增测试用例以压力测试优先级调度。


JIRA 相关条目
******************
* ``ZEP-230`` - 定义 I2S 驱动 API
* ``ZEP-601`` - 启用 CONFIG_DEBUG_INFO
* ``ZEP-702`` - 将 Nordic 的 Phoenix 链路层集成到 Zephyr
* ``ZEP-749`` - TinyCrypt 使用旧的、未优化的 micro-ecc 版本
* ``ZEP-896`` - nRF5x 系列：新增对电源和时钟外设的支持
* ``ZEP-1067`` - BMM150 驱动
* ``ZEP-1396`` - 新增 ksdk adc shim 驱动
* ``ZEP-1426`` - 在所有目标上启用 CONFIG_BOOT_TIME_MEASUREMENT？
* ``ZEP-1552`` - 提供 apds9960 传感器驱动
* ``ZEP-1647`` - 找出新的 breathe/doxygen/sphinx 版本组合，这些版本受支持
* ``ZEP-1744`` - UPF 56 BLE 控制器问题
* ``ZEP-1751`` - 新增模板 YAML 文件
* ``ZEP-1819`` - 在 nrf_rtc_timer 定时器中新增无滴答内核支持
* ``ZEP-1843`` - 提供基于可用硬件过滤测试用例的机制
* ``ZEP-1892`` - 修复 Fix Release 的问题
* ``ZEP-1902`` - 缺少 arm/nucleo_f334r8 的板卡文档
* ``ZEP-1911`` - 缺少 arm/stm3210c_eval 的板卡文档
* ``ZEP-1917`` - 缺少 arm/stm32373c_eval 的板卡文档
* ``ZEP-1918`` - 修复连接参数请求流程
* ``ZEP-2018`` - 移除已弃用的 PWM API
* ``ZEP-2020`` - tests/crypto/test_ecc_dsa 在 riscv32 上间歇性失败
* ``ZEP-2025`` - 为 k64 新增 mcux pwm shim 驱动
* ``ZEP-2031`` - ESP32 架构配置
* ``ZEP-2032`` - Espressif 开源工具链支持
* ``ZEP-2039`` - 实现基于 stm32cube LL 的时钟控制驱动
* ``ZEP-2054`` - 将所有辅助脚本转换为使用 python3
* ``ZEP-2062`` - 将 gen_offset_header 转换为 python 脚本
* ``ZEP-2063`` - 将 gen_idt 转换为 python
* ``ZEP-2068`` - 任务也需要在 QRC 中被跟踪
* ``ZEP-2071`` - samples：警告：(SPI_CS_GPIO && SPI_SS_CS_GPIO && I2C_NRF5) 选择具有未满足直接依赖的 GPIO
* ``ZEP-2085`` - 将 CONTRIBUTING.rst 添加到根文件夹 w/contributing 指南
* ``ZEP-2089`` - ESP32 的 UART 支持
* ``ZEP-2115`` - 用于配置网络的联网应用通用 API
* ``ZEP-2116`` - 用于创建客户端/服务器应用的联网应用通用 API
* ``ZEP-2141`` - tests/net/ipv6/src/main.c 中的 Coverity CID 169303
* ``ZEP-2150`` - 将 Arduino 101 迁移到设备树
* ``ZEP-2151`` - 将 Quark D2000 迁移到设备树
* ``ZEP-2156`` - 使用 LLVM/icx (tests/kernel/sprintf) 的构建警告 [-Wformat]
* ``ZEP-2168`` - nRF51 (Cortex M0) 上启用 TICKLESS_KERNEL 时定时器似乎损坏
* ``ZEP-2171`` - 将所有板卡 pinmux 代码从 drivers/pinmux/stm32 迁移到相应的 board/soc 位置
* ``ZEP-2184`` - 将 data、bss、noinit 段拆分为应用和内核区域
* ``ZEP-2188`` - x86：实现简单的栈内存保护
* ``ZEP-2217`` - schedule_api 测试在 ARM 上启用无滴答内核时失败
* ``ZEP-2218`` - 启用无滴答内核运行 schedule_api 时出现意外短的时间片
* ``ZEP-2220`` - 将 MPU 扩展到 stm32 家族
* ``ZEP-2225`` - 注销 GATT 服务的能力
* ``ZEP-2226`` - BSD Sockets API：基本阻塞 API
* ``ZEP-2227`` - BSD Sockets API：非阻塞 API
* ``ZEP-2229`` - test_time_slicing_preemptible 在 bbc_microbit 和其他 NRF 板卡上失败
* ``ZEP-2250`` - sanitycheck 未正确过滤 defconfigs
* ``ZEP-2258`` - 发现 Coverity 静态扫描问题
* ``ZEP-2265`` - ARM MPU 的栈声明宏
* ``ZEP-2267`` - 创建发布说明
* ``ZEP-2270`` - 将 mpu_stack_guard_test 从使用 k_thread_spawn 转换为 k_thread_create
* ``ZEP-2274`` - 使用 LLVM/icx (tests/net/ipv6_fragment) 的构建警告 [-Wpointer-sign]
* ``ZEP-2278`` - 禁用完整调试时 KW41-Z 802.15.4 驱动挂起
* ``ZEP-2279`` - echo_server TCP 处理器被 SYN flood 损坏
* ``ZEP-2280`` - 为 KBUILD_ZEPHYR_APP 新增测试用例
* ``ZEP-2285`` - 非板卡出现在文档的板卡列表中
* ``ZEP-2286`` - 为 ESP32 编写 GPIO 驱动
* ``ZEP-2289`` - [DoS] 大 TCP 数据包导致的内存泄漏
* ``ZEP-2296`` - ESP32：看门狗驱动
* ``ZEP-2297`` - ESP32：Pin mux 驱动
* ``ZEP-2303`` - 并发传入 TCP 连接
* ``ZEP-2305`` - linker：实现 MMU 对齐约束
* ``ZEP-2306`` - echo server 因 IPv6 hop-by-hop 选项异常而挂起
* ``ZEP-2308`` - （新）缺少网络 API 细节文档
* ``ZEP-2310`` - 改进配置文档索引组织
* ``ZEP-2314`` - 测试用例失败：tests/benchmarks/timing_info/testcase.ini#test
* ``ZEP-2316`` - 测试用例失败：tests/bluetooth/shell/testcase.ini#test_br
* ``ZEP-2318`` - 某些内核对象段未对齐
* ``ZEP-2319`` - tests/net/ieee802154/l2 在初始化前使用信号量
* ``ZEP-2321`` - [PTS] 由于 BTP_TIMEOUT 错误，SM/GATT/GAP 的所有 TC 失败。
* ``ZEP-2326`` - x86：验证用户缓冲区的 API
* ``ZEP-2328`` - gen_mmu.py 在某些情况下似乎生成不正确的表
* ``ZEP-2329`` - 错误的内存访问 tests/net/route
* ``ZEP-2330`` - 错误的内存访问 tests/net/rpl
* ``ZEP-2331`` - 错误的内存访问 tests/net/ieee802154/l2
* ``ZEP-2332`` - 错误的内存访问 tests/net/ip-addr
* ``ZEP-2334`` - CONFIG_DEBUG=y 时 bluetooth shell 构建警告
* ``ZEP-2335`` - 确保发布时 Licensing 页面是最新的
* ``ZEP-2340`` - 禁用广播导致卡住
* ``ZEP-2341`` - 构建警告：override：使用 LLVM/icx 重新分配符号 MAIN_STACK_SIZE (/tests/net/6lo)
* ``ZEP-2343`` - 发现 Coverity 静态扫描问题
* ``ZEP-2344`` - 发现 Coverity 静态扫描问题
* ``ZEP-2345`` - 发现 Coverity 静态扫描问题
* ``ZEP-2352`` - 网络 API 文档未说明回调何时从不同线程调用
* ``ZEP-2354`` - ESP32：随机数生成器
* ``ZEP-2355`` - 发现 Coverity 静态扫描问题
* ``ZEP-2358`` - samples:net:echo_server：发送 UDP 数据包失败
* ``ZEP-2359`` - samples:net:coaps_server：无法使用 IPv6 绑定
* ``ZEP-2360`` - Bluetooth Mesh 的初始实现
* ``ZEP-2361`` - 在原生 API 之上提供 POSIX 兼容层
* ``ZEP-2365`` - samples/net/wpanusb/test_15_4 在 nrf52840_pca10056 和 frdm_kw41z 上失败
* ``ZEP-2366`` - 实现 \__kernel 属性
* ``ZEP-2367`` - udp、tcp、context 网络测试中的 NULL 指针读取
* ``ZEP-2368`` - x86：QEMU：默认在启动时启用 MMU
* ``ZEP-2370`` - [test] 创建压力测试以测试 zephyr 上的抢占式调度
* ``ZEP-2371`` - [test] 创建压力测试以测试 zephyr 上相等优先级任务的轮询调度
* ``ZEP-2374`` - 构建警告：override：使用 LLVM/icx 重新分配符号 NET_IPV4 (/tests/net/dhcpv4)
* ``ZEP-2375`` - 使用 LLVM/icx (tests/net/udp) 的构建警告 [-Wpointer-sign]
* ``ZEP-2378`` - sample/bluetooth/ipsp：构建应用时 'ROM' 溢出
* ``ZEP-2379`` - samples/bluetooth：Bluetooth 初始化失败 (err -19)
* ``ZEP-2380`` - Zephyr 提交 3604c391e 破坏了 TCP
* ``ZEP-2382`` - 将测试转换为使用 ztest 框架
* ``ZEP-2383`` - Net-app API 需要支持 DTLS
* ``ZEP-2384`` - "Common" bluetooth 示例代码无法在树外构建
* ``ZEP-2385`` - 将 TinyCrypt 更新至 0.2.7
* ``ZEP-2395`` - 在 nrf52840 上通过 bluetooth 运行时 http_server 示例中的断言
* ``ZEP-2397`` - net_if_ipv6_addr_rm 在未初始化的 k_delayed_work 对象上调用 k_delayed_work_cancel()
* ``ZEP-2398`` - 网络栈测试用例仅在 x86 上测试
* ``ZEP-2403`` - 为 qemu_x86 启用 MMU 破坏了主动连接支持
* ``ZEP-2407`` - [Cortex m 系列] 当调度超过 8 个相等优先级的抢占线程时，Cortex m3 系列出现崩溃
* ``ZEP-2408`` - 设计内核对象共享策略机制
* ``ZEP-2412`` - 自提交 c1e5cb 起 Bluetooth tester 应用不工作
* ``ZEP-2423`` - samples/bluetooth/ipsp 的内置 TCP echo 在 TCP 关闭时崩溃
* ``ZEP-2432`` - ieee802154_shell.c 中的 net_mgmt 调用导致 BUS FAULT
* ``ZEP-2433`` - x86：进行取证分析以确定监督模式下的栈溢出上下文
* ``ZEP-2436`` - 无法在 Quark_D200_CRB 上看到控制台输出
* ``ZEP-2437`` - 为 quark d2000 构建应用时出现警告
* ``ZEP-2444`` - [nrf] 在 nrf51/nrf52 平台的情况下，调度测试 API 失败
* ``ZEP-2445`` - nrf52：使用 Bluetooth + Flash 驱动 + CONFIG_ASSERT 时 CPU 锁死
* ``ZEP-2447`` - 'make debugserver' 对 qemu_x86_iamcu 失败
* ``ZEP-2451`` - 将 Bluetooth IPSP 支持函数从 samples/bluetooth 迁移到单独的库
* ``ZEP-2452`` - https 服务器无法为 olimex_stm32_e407 构建
* ``ZEP-2457`` - generated/offsets.h 被不必要地重新生成
* ``ZEP-2459`` - 示例应用在 Quark SE C1000 上不工作
* ``ZEP-2460`` - tests/crypto/ecc_dh 在 qemu_nios2 上失败
* ``ZEP-2464`` - "允许 IPv6 接口初始化与延迟 IP 分配协同工作" 补丁破坏了非延迟 IPv6 分配
* ``ZEP-2465`` - 发现静态代码扫描（coverity）问题
* ``ZEP-2467`` - 发现静态代码扫描（coverity）问题
* ``ZEP-2468`` - 发现静态代码扫描（coverity）问题
* ``ZEP-2469`` - 发现静态代码扫描（coverity）问题
* ``ZEP-2474`` - 发现静态代码扫描（coverity）问题
* ``ZEP-2480`` - 使用 LLVM/icx (samples/net/coaps_server) 的构建警告 [-Wpointer-sign]
* ``ZEP-2482`` - 使用 LLVM/icx (samples/net/telnet) 的构建警告 [-Wpointer-sign]
* ``ZEP-2483`` - samples:net:http_client：无法在 IPv6 中获取 http 请求
* ``ZEP-2484`` - samples:net:http_server：无法在 IPv6 中工作
* ``ZEP-2485`` - 使用 LLVM/icx (samples/net/coaps_client) 的构建警告 [-Wpointer-sign]
* ``ZEP-2486`` - 使用 LLVM/icx (samples/net/mbedtls_dtlsserver) 的构建警告 [-Wpointer-sign]
* ``ZEP-2488`` - 使用 LLVM/icx (samples/net/irc_bot) 的构建警告 [-Wpointer-sign] 和 [-Warray-bounds]
* ``ZEP-2489`` - _x86_mmu_buffer_validate API 中的 bug
* ``ZEP-2496`` - tests/benchmarks/object_footprint 构建失败
* ``ZEP-2497`` - [TIMER] k_timer_start 应对 duration 参数接受 0 值
* ``ZEP-2498`` - [Display] k_timer_start 的 Minimum Duration 参数应为非零正值
* ``ZEP-2508`` - esp32 链接未正确统一 ELF 段
* ``ZEP-2510`` - BT：CONFIG_BT_HCI_TX_STACK_SIZE 对 BT_SPI 似乎太低
* ``ZEP-2514`` - XCC sanitycheck 构建编译错误的目标
* ``ZEP-2523`` - 在文件 /samples/net/zoap_server/src/zoap-server.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2525`` - 在文件 /samples/net/zoap_server/src/zoap-server.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2531`` - 在文件 /tests/net/lib/dns_resolve/src/main.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2528`` - 在文件 /samples/net/nats/src/nats.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2534`` - 在文件 /tests/kernel/irq_offload/src/irq_offload.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2535`` - 在文件 /tests/net/lib/zoap/src/main.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2537`` - 在文件 /tests/crypto/ecc_dh/src/ecc_dh.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2538`` - 在文件 /arch/arm/soc/st_stm32/stm32f1/soc_gpio.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2539`` - 在文件 /tests/net/ieee802154/l2/src/ieee802154_test.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2540`` - 在文件 /ext/lib/crypto/tinycrypt/source/ecc_dh.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2541`` - 在文件 /subsys/bluetooth/host/mesh/cfg.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2549`` - 在文件 /samples/net/leds_demo/src/leds-demo.c 中发现静态代码扫描（Coverity）问题
* ``ZEP-2552`` - ESP32 uart poll_out 始终返回 0
* ``ZEP-2553`` - k_queue_poll 未正确处理 -EADDRINUSE（另一线程已在轮询）
* ``ZEP-2556`` - ESP32 看门狗 WDT_MODE_INTERRUPT_RESET 模式失败
* ``ZEP-2557`` - ESP32：某些 GPIO 测试失败 (tests/drivers/gpio/gpio_basic_api)
* ``ZEP-2558`` - CONFIG_BLUETOOTH_* Kconfig 选项被静默忽略
* ``ZEP-2560`` - samples/net：zoap_server 示例无法添加多播地址
* ``ZEP-2561`` - samples/net：HTTP 客户端发送 POST 请求失败
* ``ZEP-2568`` - [PTS] 由于 BTP_ERROR，L2CAP/SM/GATT/GAP 的所有 TC 失败。
* ``ZEP-2575`` - 使用 LLVM/icx (samples/hello_world) 的错误：[ '-O: command not found']
* ``ZEP-2576`` - samples/net/sockets/echo、echo_async：发送 TCP 数据包失败
* ``ZEP-2581`` - CC3220 可执行二进制格式支持
* ``ZEP-2584`` - 将 mbedTLS 更新至 2.6.0
* ``ZEP-713``  - 在 ARC 上实现可抢占的普通 IRQ
