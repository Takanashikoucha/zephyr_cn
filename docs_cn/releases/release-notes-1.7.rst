.. _zephyr_1.7:

Zephyr 内核 1.7.0
####################

我们很高兴宣布 Zephyr 内核 1.7.0 版本的发布。
该版本继续完善 1.6.0 内核版本引入的统一内核，
简化了 Zephyr 的整体架构和编程接口。
这是最后一个支持 1.5.0 版本及更早版本中已弃用的旧版 nano 内核和 micro 内核 API 的版本。

该版本引入了新的原生 IP 协议栈，取代了旧版 uIP 协议栈，
保留了旧版功能，增加了额外的能力，并允许未来的改进。

我们引入了对 RISC V 和 Xtensa 架构的支持，
目前总共支持 6 种架构。

新增了对基于 ARM 的板卡的设备树支持。
初始设备树支持包括 flash/sram 基地址和 UART 设备。
板卡支持包括 NXP Kinetis 基于的 SoC、ARM Beetle、TI CC3200 LaunchXL，
以及基于 STML32L476 的 SoC。
计划是在未来的 Zephyr 版本中增加对其他架构的支持
并扩展设备支持。

以下章节提供了自内核版本 1.6.0 以来按组件划分的详细变更列表。

内核
******

* 引入 k_poll API：k_poll() 在精神上类似于 POSIX poll() API，
  它允许单个线程监视多个事件而无需主动轮询它们，
  而是等待一个或多个变为就绪。
* 优化了某些线程字段的内存使用
* 从内核代码中移除 micro/nano 内核术语的使用，
  并引入了启用/禁用旧版 API 的旧版选项。（使用 legacy.h）


架构
*************

* ARM：新增对设备树的支持
* ARM：修复 Cortex M0(+) 上的异常优先级访问
* ARM：重构以使用 CMSIS

板卡
******

* 新增 ARM MPS2_AN385 板卡
* 新增 Atmel SAM E70 Xplained 板卡
* 新增 Nordic pca10056 PDK 板卡
* 新增 NXP FRDM-KW41Z 板卡
* 新增 ST Nucleo-F334R8、Nucleo-L476G、STM3210C-EVAL 和 STM32373C-EVAL 板卡
* 新增基于 Quark SE C1000 和 Intel Curie 的 Panther 和 tinyTILE 板卡
* 新增对 Zedboard Pulpino 的支持，这是一个基于 RISC V 的板卡
* 新增 RISC V 的 Qemu 目标和 Xtensa 架构的模拟器目标。

驱动程序与传感器
*******************

* 新增 Atmel SAM pmc、gpio、uart 和 ethernet 驱动
* 新增 STM32F3x 时钟、flash、gpio、pinmux 驱动
* 新增 stm32cube pwm 和时钟驱动
* 新增 cc3200 gpio 驱动
* 新增 mcr20a ieee802154 驱动
* 新增 mcux pinmux、gpio、uart 和 spi 驱动
* 新增 Beetle 时钟控制和看门狗驱动

网络
**********

本版本移除了旧版 uIP 协议栈并引入了新的原生 IP 协议栈。
因此代码库中有很多变更。原生 IP 协议栈
将支持与 1.6 中旧版 IP 协议栈相同的功能，
并添加以下所述的新网络特性。

* IP 协议栈代码迁移至 subsys/net/ip 目录。
* IP 协议栈同时支持 IPv6 和 IPv4，且它们可以同时启用。
* 可以同时启用多种网络技术，如 Bluetooth IPSP 和 IEEE 802.15.4。
  IP 协议栈不提供已启用网络技术之间的路由功能，
  应用需要决定将网络数据包发送到哪里。
* 网络技术被抽象在 IP 层 2（L2）中，
  并作为网络接口呈现给系统的其余部分。
  存在以太网、Bluetooth 和 IEEE 802.15.4 的 L2 驱动。
* 创建了 Bluetooth 互联网协议支持配置（IPSP）支持。
  它将通过 Bluetooth 面向连接的通道（L2CAP）提供 IPv6 连接。
* 创建了 DHCPv4 支持。
* 创建了名为 ZoAP 的 CoAP 实现，取代基于 uIP 的实现。
* 更新 6Lo 实现以同时支持 Bluetooth 和 IEEE 802.15.4
* 创建了应用 API（net_context），用于创建连接
  并向外部系统传输数据。
* 新增了示例应用（wpanusb），用于将 IEEE 802.15.4 无线电
  通过 USB 导出到 Linux 等外部操作系统。
* 新增了 DNS 客户端库。
* 更新了 TCP 实现。
* 创建了 MQTT 发布者支持。
* 创建了网络测试生成器（zperf）。
* 创建了 telnet 控制台支持。
* 创建了 IRC 客户端示例应用。
* 创建了 HTTP 服务器和客户端示例应用。
* 创建了 net-shell 模块，用于与网络子系统进行交互。
* 创建了 ieee15_4 shell 模块，用于与
  IEEE 802.15.4 Soft MAC 进行专用交互。
* 创建了网络管理 API，用于通用网络设置请求
  以及网络事件通知系统（发送者/监听者）。
* 重新设计了缓冲区与池分配 API。

蓝牙
*********

* 重新设计缓冲区池以减少内存消耗
* 重新设计线程模型以减少内存消耗
* 利用新的 k_poll API 将所有 TX 线程合并为一个
* 新增更多 SDP 功能
* 改进 RFCOMM 支持
* 降低控制器中的延迟
* 新增 SPI HCI 驱动

库
*********

* 更新 mbedTLS 库
* 将 TinyCrypt 更新至 0.2.5 版本

HAL
****

* 将 FAT FS 更新至 rev 0.12b
* 更新 Nordic MDK 头文件
* 将 QMSI 更新至 1.4 RC3
* 导入用于 SAM E70 和 SAM3X 的 Atmel SDK (ASF)
* 导入 Nordic SDK HAL 和 802.15.4 无线电驱动
* 将 NXP KSDK 重命名为 MCUX
* 导入用于 KW41Z 的 NXP MCUX
* 导入 Segger J-Link RTT 库
* 导入用于 F4 和 L4 的 stm32cube

文档
*************

* 内核组件文档的通用改进和新增
* 将受支持板卡信息移回网站站点。
* 新的网站文档主题，与新的 zephyrproject.org 站点配套。
* 新的本地内容生成主题（read-the-docs）
* 通用拼写检查和组织改进。
* 新增全站术语表。
* 新增移植指南。
* 将示例 README 文件转换为包含在网站中的文档。
* 改进了 :ref:`boards` 和 :zephyr:code-sample-category:`samples` 的一致性。


JIRA 相关条目
******************


.. comment  List derived from https://jira.zephyrproject.org/issues/?filter=10345

* ``ZEP-19`` - IPSP 节点支持
* ``ZEP-145`` - Arduino Due 没有 'make flash'
* ``ZEP-328`` - 硬件加密抽象
* ``ZEP-359`` - 将 QEMU 处理迁移到集中位置
* ``ZEP-365`` - Zephyr 的 MQTT 库
* ``ZEP-437`` - TCP/IP API
* ``ZEP-513`` - 在 gp 启用系统中，指定段中 small microkernel 对象的 extern 声明需要 __attribute__((section))
* ``ZEP-591`` - 将 MQTT 移植到新 IP 协议栈
* ``ZEP-604`` - 在 coap_server 示例应用中，CoAP resource separate 无法发送 separate 响应
* ``ZEP-613`` - TCP/UDP 客户端和服务器模式功能
* ``ZEP-641`` - Bluetooth Eddystone 示例未正确实现 Eddystone beacon
* ``ZEP-648`` - 新的 CoAP 实现
* ``ZEP-664`` - 扩展 spi_qmsi_ss 驱动以支持保存/恢复外设上下文
* ``ZEP-665`` - 扩展 gpio_qmsi_ss 驱动以支持保存/恢复外设上下文
* ``ZEP-666`` - 扩展 i2c_qmsi_ss 驱动以支持保存/恢复外设上下文
* ``ZEP-667`` - 扩展 adc_qmsi_ss 驱动以支持保存/恢复外设上下文
* ``ZEP-686`` - docs：Application Development Primer 和 Developing an Application and the Build System 中的信息大量重复
* ``ZEP-706`` - 无法在 Arduino 101 的 ARC 一侧设置调试断点
* ``ZEP-719`` - 新增 ksdk uart shim 驱动
* ``ZEP-734`` - 为 Thread 支持移植 AES-CMAC-PRF-128 [RFC 4615] 加密库
* ``ZEP-742`` - nRF5x 系列：使用 NRF_RTC 的系统时钟驱动
* ``ZEP-744`` - USB WebUSB
* ``ZEP-748`` - 启用 mbedtls_sslclient 示例在 quark se 板卡上运行
* ``ZEP-759`` - 新增对 Atmel SAM E70（Cortex-M7）芯片系列和 SAM E70 Xplained 板卡的初步支持
* ``ZEP-788`` - UDP
* ``ZEP-789`` - IPv4
* ``ZEP-790`` - ICMPv4
* ``ZEP-791`` - TCP
* ``ZEP-792`` - ARP
* ``ZEP-793`` - DNS 解析器
* ``ZEP-794`` - 互联网主机要求 - 通信层
* ``ZEP-796`` - DHCPv4
* ``ZEP-798`` - IPv6
* ``ZEP-799`` - 通过 TLS 的 HTTP
* ``ZEP-801`` - 支持 IPv6 的 DNS 扩展
* ``ZEP-804`` - IPv6 寻址架构
* ``ZEP-805`` - 互联网控制报文协议（ICMP）v6
* ``ZEP-807`` - IPv6 邻居发现
* ``ZEP-808`` - IPv6 无状态自动配置（SLAAC）
* ``ZEP-809`` - 通过 802.15.4 的 IPv6
* ``ZEP-811`` - Trickle 算法
* ``ZEP-812`` - 通过 802.15.4 的 IPv6 压缩格式
* ``ZEP-813`` - RPL：IPv6 路由协议
* ``ZEP-814`` - 路径选择中使用的路由度量
* ``ZEP-815`` - RPL 的目标函数零
* ``ZEP-816`` - 带滞后的最小秩（RPL）
* ``ZEP-818`` - 在新 IP 协议栈上工作的 CoAP
* ``ZEP-820`` - HTTP v1.1 服务器示例
* ``ZEP-823`` - 新 IP 协议栈 - 文档
* ``ZEP-824`` - 网络设备驱动移植指南
* ``ZEP-825`` - 从旧到新 IP 协议栈 API 的移植指南
* ``ZEP-827`` - HTTP 客户端示例应用
* ``ZEP-830`` - ICMPv6 参数问题支持
* ``ZEP-832`` - Hop-by-Hop 选项处理
* ``ZEP-847`` - 网络协议必须迁移至 subsys/net/lib
* ``ZEP-854`` - 带 DTLS 的 CoAP 示例
* ``ZEP-859`` - 将 ENC28J60 驱动迁移到 YAIP IP 协议栈
* ``ZEP-865`` - 将文件系统示例转换为可运行的测试
* ``ZEP-872`` - 无法使用 Ubuntu 并按照 wiki 说明在 Arduino 101 上烧录 Zephyr
* ``ZEP-873`` - DMA API 更新
* ``ZEP-875`` - 6LoWPAN - 基于上下文的压缩支持
* ``ZEP-876`` - 6LoWPAN - 基于偏移的 802.15.4 数据包重组
* ``ZEP-879`` - 6LoWPAN - 无状态地址自动配置
* ``ZEP-882`` - 6LoWPAN - IPv6 下一报头压缩
* ``ZEP-883`` - IP 协议栈 L2 接口管理 API
* ``ZEP-884`` - 802.15.4 - CSMA-CA 无线电协议支持
* ``ZEP-885`` - 802.15.4 - Beacon 帧支持
* ``ZEP-886`` - 802.15.4 - MAC 命令帧支持
* ``ZEP-887`` - 802.15.4 - 管理服务：RFD 级别支持
* ``ZEP-911`` - 细化线程优先级与锁定
* ``ZEP-919`` - 清除过时的 microkernel 与 nanokernel 代码
* ``ZEP-929`` - 验证仅抢占线程和仅协作线程配置
* ``ZEP-931`` - 确定内核文件命名与位置
* ``ZEP-936`` - 将驱动适配到统一内核
* ``ZEP-937`` - 将网络适配到统一内核
* ``ZEP-946`` - Galileo Gen1 板卡支持被移除？
* ``ZEP-951`` - CONFIG_GDB_INFO 构建在 ARM 上不工作
* ``ZEP-953`` - CONFIG_HPET_TIMER_DEBUG 构建警告
* ``ZEP-958`` - 简化 pinmux 接口并将 pinmux_dev 合并为单一 API
* ``ZEP-964`` - 新增用于禁用旧版 API 的（隐藏的？）Kconfig 选项
* ``ZEP-975`` - 将 DNS 客户端移植到新 IP 协议栈
* ``ZEP-1012`` - 将 NATS 客户端移植到新 IP 协议栈
* ``ZEP-1038`` - 硬实时中断支持
* ``ZEP-1060`` - 缺少文档的贡献者指南
* ``ZEP-1103`` - 提议并实现多核电源管理的同步流程
* ``ZEP-1165`` - 在 IRQ_CONNECT() 中支持枚举作为 IRQ 线参数
* ``ZEP-1172`` - 更新 logger Api 以允许为 SYS_LOG_BACKEND_FN 函数使用 hook
* ``ZEP-1177`` - 减少 Zephyr 对主机工具的依赖
* ``ZEP-1179`` - 使用 ISSM (icx) 的 LLVM 编译时出现构建问题
* ``ZEP-1189`` - Quark SE 的 SoC I2C 外设无法从 ARC 核心使用
* ``ZEP-1190`` - Quark SE 的 SoC SPI 外设无法从 ARC 核心使用
* ``ZEP-1222`` - 为 ARC 核心新增保存/恢复支持
* ``ZEP-1223`` - 为 arcv2_irq_unit 新增保存/恢复支持
* ``ZEP-1224`` - 为 arcv2_timer_0/sys_clock 新增保存/恢复支持
* ``ZEP-1230`` - 优化 ARC 上的中断返回代码。
* ``ZEP-1233`` - mbedDTLS DTLS 客户端稳定性在 net 分支的树顶上不工作
* ``ZEP-1251`` - 抽象驱动重入代码
* ``ZEP-1267`` - 收到路由器通告时 echo 服务器崩溃
* ``ZEP-1276`` - 将 disk_access_* 移出文件系统子系统
* ``ZEP-1283`` - 跳过 samples/power/power_mgr 中 gpio 切换的编译选项
* ``ZEP-1284`` - 移除 arch/arm/core/gdb_stub.S 及其引入的所有抽象
* ``ZEP-1288`` - 定义 _arc_v2_irq_unit 设备
* ``ZEP-1292`` - 将外部 mbed TLS 库更新至最新版本（2.4.0）
* ``ZEP-1300`` - ARM LTD V2M Beetle 支持 [阶段 2]
* ``ZEP-1304`` - 为 NXP Kinetis K64F 定义设备树绑定
* ``ZEP-1305`` - 为构建基础设施新增 DTS/DTB 目标
* ``ZEP-1306`` - 创建 DTS/DTB 解析器
* ``ZEP-1307`` - DTS 配置的管线处理
* ``ZEP-1308`` - zephyr 线程函数 k_sleep 在 nrf51822 上不工作
* ``ZEP-1320`` - 更新架构移植指南
* ``ZEP-1321`` - 术语表需要更新
* ``ZEP-1323`` - 消除 ./include 下对 fiber、task 和 nanokernel 的引用
* ``ZEP-1324`` - 去除对 CONFIG_NANOKERNEL 的引用
* ``ZEP-1325`` - 消除 TICKLESS_IDLE_SUPPORTED 选项
* ``ZEP-1327`` - 消除过时的内核目录
* ``ZEP-1329`` - 重命名带有 nano\_ 前缀的内核 API
* ``ZEP-1334`` - 为基于 QEMU 的板卡新增 make debug 支持
* ``ZEP-1337`` - 迁移事件记录器文件
* ``ZEP-1338`` - 使用新的 FATFS 版本 0.12b 更新外部 fs
* ``ZEP-1342`` - legacy/kernel/test_early_sleep/ 在 EMSK 上失败
* ``ZEP-1347`` - sys_bitfield_*() 接受 unsigned long* 而非 memaddr_t
* ``ZEP-1351`` - FDRM k64f SPI 不工作
* ``ZEP-1355`` - 连接无法建立
* ``ZEP-1357`` - iot/dns：客户端损坏
* ``ZEP-1358`` - BMI160 加速度计在所有轴上给出 0
* ``ZEP-1361`` - IP 协议栈损坏
* ``ZEP-1363`` - 缺少 arm/arduino_101_ble 的 wiki 板卡支持页面
* ``ZEP-1365`` - 缺少 arm/c3200_launchxl 的 wiki 板卡支持页面
* ``ZEP-1370`` - arduino_due 有 wiki 页面但没有 zephyr/boards 支持文件夹
* ``ZEP-1374`` - 新增 ksdk spi shim 驱动
* ``ZEP-1387`` - 为 Atmel ataes132a HW 加密模块新增驱动
* ``ZEP-1389`` - 新增对 KW41 SoC 的支持
* ``ZEP-1390`` - 新增对 FRDM-KW41Z 的支持
* ``ZEP-1393`` - 新增 ksdk pinmux 驱动
* ``ZEP-1394`` - 新增 ksdk gpio 驱动
* ``ZEP-1395`` - 为 FXOS8700 驱动新增数据就绪触发
* ``ZEP-1401`` - 增强就绪队列缓存和中断退出代码以减少中断延迟。
* ``ZEP-1403`` - 从 ARC 板卡移除 CONFIG_OMIT_FRAME_POINTER
* ``ZEP-1405`` - /subsys/bluetooth/host/l2cap_br.c 中的函数 l2cap_br_conn_req 引用未初始化的指针
* ``ZEP-1406`` - 更新 wiki 中的传感器驱动路径
* ``ZEP-1408`` - quark_se_c1000_ss enter_arc_state() 可能需要 cc 和内存 clobber
* ``ZEP-1411`` - 弃用 device_sync_call API 并直接使用信号量
* ``ZEP-1413`` - [ARC] test/legacy/kernel/test_tickless/microkernel 构建失败
* ``ZEP-1415`` - drivers/timer/* 代码注释仍引用 micro/nano 内核
* ``ZEP-1418`` - 新增对 Nordic nRF52840 及其 DK 的支持
* ``ZEP-1419`` - 由于 printk/printf 选择，SYS_LOG 宏可能导致潜在的不良行为
* ``ZEP-1420`` - 使中断禁用期间花费的时间具有确定性
* ``ZEP-1421`` - BMI160 陀螺仪驱动在 1-5 分钟后停止报告
* ``ZEP-1422`` - 启用 echo_client ipv6 后 Arduino_101 不响应 ipv6 ping 请求
* ``ZEP-1427`` - wpanusb dongle / 15.4 通信不稳定
* ``ZEP-1429`` - NXP MCR20A 驱动
* ``ZEP-1432`` - ksdk pinmux 驱动应公开 pinmux API
* ``ZEP-1434`` - menuconfig 屏幕截图显示 nanokernel 选项
* ``ZEP-1437`` - AIO：无法在 ISR 中获取挂起中断
* ``ZEP-1440`` - MINIMAL_LIBC 与 NEWLIB_LIBC 的 Kconfig 选择不可选
* ``ZEP-1442`` - Samples/net/dhcpv4_client：由于没有规则制作目标 prj\_.conf 而构建失败
* ``ZEP-1443`` - Samples/net/zperf：由于找不到 net_private.h 而构建失败
* ``ZEP-1448`` - Samples/net/mbedtls_sslclient：由于找不到 net/ip_buf.h 而构建失败
* ``ZEP-1449`` - samples：logger_hook
* ``ZEP-1456`` - nrf51 上运行 Bluetooth hci_uart 示例时出现断言
* ``ZEP-1457`` - 为 Zephyr 许可证样板新增 SPDX 标签
* ``ZEP-1460`` - Sanity check 将某些 qemu 步骤失败报告为 'build_error'
* ``ZEP-1461`` - 为 openocd 上游新增 zephyr 支持
* ``ZEP-1467`` - 清理 misc/ 并将功能迁移至 subsys/ 中的子系统
* ``ZEP-1473`` - 使用网关使 ARP 缓存混乱。
* ``ZEP-1474`` - BLE 连接参数请求/响应处理
* ``ZEP-1475`` - k_free 文档应说明 NULL 是有效的
* ``ZEP-1476`` - echo_client 显示端口不可达
* ``ZEP-1480`` - 更新入门指南中受支持的发行版
* ``ZEP-1481`` - Bluetooth 初始化失败
* ``ZEP-1483`` - H:4 HCI 驱动（h4.c）应依赖 UART 流控制以避免丢失数据包
* ``ZEP-1487`` - I2C_SS：I2C 在开始数据传输前未设置设备忙
* ``ZEP-1488`` - SPI_SS：SPI 在开始数据传输前未设置设备忙
* ``ZEP-1489`` - [GATT] 嵌套长特性值可靠写入
* ``ZEP-1490`` - [PTS] TC_CONN_CPUP_BV_04_C 测试用例失败
* ``ZEP-1492`` - 新增 Atmel SAM 家族 GMAC 以太网驱动
* ``ZEP-1493`` - Zephyr 项目文档版权
* ``ZEP-1495`` - 缺少网络 API 细节文档
* ``ZEP-1496`` - gpio_pin_enable_callback 错误
* ``ZEP-1497`` - Cortex-M0 移植的异常和中断优先级设置与获取损坏
* ``ZEP-1507`` - fxos8700 损坏的 gpio_callback 实现
* ``ZEP-1512`` - doc-theme 有自己的 conf.py
* ``ZEP-1514`` - samples/bluetooth/ipsp 构建失败：net/ip_buf.h No such file or directory
* ``ZEP-1525`` - driver：gpio：GPIO 驱动仍使用 nano_timer
* ``ZEP-1532`` - 错误的加速度计读数
* ``ZEP-1536`` - 将 PWM 示例的文档转换为 RST
* ``ZEP-1537`` - 将电源管理示例的文档转换为 RST
* ``ZEP-1538`` - 将 zoap 示例的文档转换为 RST
* ``ZEP-1539`` - 为所有网络示例创建 RST 文档
* ``ZEP-1540`` - 将 Bluetooth 示例转换为 RST
* ``ZEP-1542`` - 多会话 HTTP 服务器示例
* ``ZEP-1543`` - 带基本认证的 HTTP 服务器示例
* ``ZEP-1544`` - 启用 echo_server ipv6 后 Arduino_101 不响应 ipv6 ping 请求
* ``ZEP-1545`` - AON Counter：ARC 上 ISR 触发两次
* ``ZEP-1546`` - Zephyr OS 高精度时序子系统中的缺陷（函数 sys_cycle_get_32()）
* ``ZEP-1547`` - 新增对 H7 加密功能和 CT2 SMP auth 标志的支持
* ``ZEP-1548`` - Python 脚本调用不一致
* ``ZEP-1549`` - k_cpu_sleep_mode 未对齐的字节地址
* ``ZEP-1554`` - Xtensa 集成
* ``ZEP-1557`` - RISC V 移植
* ``ZEP-1558`` - Timer 到期函数中支持用户私有数据指针
* ``ZEP-1559`` - 为 ARC 架构实现 _tsc_read
* ``ZEP-1562`` - echo_server/echo_client 示例在运行一段时间后随机挂起
* ``ZEP-1563`` - 将 NRF51/NRF52 的板卡文档移回 git 树
* ``ZEP-1564`` - 6lo uncompress_IPHC_header 覆盖 IPHC 字段
* ``ZEP-1566`` - WDT：中断触发多次
* ``ZEP-1569`` - net/tcp：服务器模式下的 TCP 不支持多个并发连接
* ``ZEP-1570`` - net/tcp：服务器模式下的 TCP 无法关闭客户端连接
* ``ZEP-1571`` - 更新 "Changes from Version 1 Kernel" 以包含 "How-To Port Apps" 章节
* ``ZEP-1572`` - 将 QMSI 更新至 1.4
* ``ZEP-1573`` - net/tcp：net_context_recv 中用户提供的数据未传递给回调
* ``ZEP-1574`` - Samples/net/dhcpv4_client：由于对 net_mgmt_add_event_callback 的未定义引用而构建失败
* ``ZEP-1579`` - 指向 zephyr 技术文档的外部链接损坏
* ``ZEP-1581`` - [nRF52832] Blinky 在几分钟后挂起
* ``ZEP-1583`` - ARC：警告：未满足直接依赖 (SOC_RISCV32_PULPINO || SOC_RISCV32_QEMU)
* ``ZEP-1585`` - 在 CONFIG_LEGACY_KERNEL=n 时 legacy.h 应在 kernel.h 中禁用
* ``ZEP-1587`` - sensor.h 仍使用旧版 API 和结构体
* ``ZEP-1588`` - I2C 在 Arduino 101 上不工作
* ``ZEP-1589`` - 为 UART 设备定义 yaml 描述
* ``ZEP-1590`` - echo_server 在 FRDM-K64F 上运行显示 BUS FAULT
* ``ZEP-1591`` - wiki：新增 Networking 章节并指向 https://wiki.zephyrproject.org/view/Network_Interfaces
* ``ZEP-1592`` - echo-server 无法使用 newlib 构建
* ``ZEP-1593`` - /scripts/sysgen 应使用 SPDX 许可标签创建输出
* ``ZEP-1598`` - samples/philosophers 在 @quark_d2000 意外构建失败 section noinit will not fit in region RAM
* ``ZEP-1601`` - 通过 Telnet 的控制台
* ``ZEP-1602`` - 在 FRDM-K64F 上使用示例应用 echo_server 时 IPv6 ping 失败
* ``ZEP-1611`` - 几个 echo 请求后出现 Hardfault（通过 BLE 的 IPv6）
* ``ZEP-1614`` - 使用正确的 i2c 设备驱动名称
* ``ZEP-1616`` - net_addr_pton() 声明中混淆了 "network address" 和 "socket address" 概念
* ``ZEP-1617`` - mbedTLS 服务器/客户端无法在 qemu 上运行
* ``ZEP-1619`` - NET_NBUF_RX_COUNT 的默认值太低，导致启动时锁死
* ``ZEP-1623`` - （部分）网络文档仍引用 1.5 世界模型（含 fibers 和 tasks）且未更新
* ``ZEP-1626`` - SPI：ARC 上 spi 无法在 CPHA 模式下工作
* ``ZEP-1632`` - TCP ACK 数据包不应转发到应用 recv cb。
* ``ZEP-1635`` - MCR20A 驱动不稳定
* ``ZEP-1638`` - 没有（公开的）inet_ntop() 类似物
* ``ZEP-1644`` - UDP 的传入连接处理不完全正确
* ``ZEP-1645`` - 等待多个内核对象的 API
* ``ZEP-1648`` - 将板卡信息指向 wiki 页面的链接更新回 web 文档
* ``ZEP-1650`` - make clean（或 pristine）未移除所有文档生成产物
* ``ZEP-1651`` - i2c_dw 由于各种变更而故障。
* ``ZEP-1653`` - 使用 ISSM (altmacro) 的 LLVM 编译时出现构建问题
* ``ZEP-1654`` - 使用 LLVM 编译时出现构建问题（未知属性 '_alloc_align_）
* ``ZEP-1655`` - 使用 LLVM 编译时出现构建问题（memory pool）
* ``ZEP-1656`` - 提交 2e9fd88 后通过 BLE 的 IPv6 不再工作
* ``ZEP-1657`` - Zoap doxygen 文档需要完善
* ``ZEP-1658`` - IPv6 TCP 缓冲区不足，在大约 5 个请求后停止响应
* ``ZEP-1662`` - zoap_packet_get_payload() 应返回有效载荷长度
* ``ZEP-1663`` - sanitycheck 覆盖用户的 CCACHE 环境
* ``ZEP-1665`` - pinmux：quark_se_ss 缺少默认 pinmux 驱动配置
* ``ZEP-1669`` - API 文档未遵循代码中文档风格
* ``ZEP-1672`` - flash：Arduino_101_sss 上 flash 设备绑定失败
* ``ZEP-1674`` - frdm_k64f：启用以太网驱动后，未连接网线时应用无法启动
* ``ZEP-1677`` - SDK：在 Arduino 101 上 CONFIG_ARC_INIT=y 时 BLE 无法初始化/广播
* ``ZEP-1681`` - 在 c1000 的 soc_sleep/soc_deep_sleep 期间保存/恢复调试寄存器
* ``ZEP-1692`` - [PTS] GATT/SR/GPA/BV-11-C 失败
* ``ZEP-1701`` - 提供 HTTP API
* ``ZEP-1704`` - BMI160 示例运行失败
* ``ZEP-1706`` - Barebone Panther 板卡支持
* ``ZEP-1707`` - [PTS] 7 个 SM/MAS 用例失败
* ``ZEP-1708`` - [PTS] SM/MAS/PKE/BI-01-C 失败
* ``ZEP-1709`` - [PTS] SM/MAS/PKE/BI-02-C 失败
* ``ZEP-1710`` - 新增 TinyTILE 板卡支持
* ``ZEP-1713`` - xtensa：修复所有 checkpatch 问题
* ``ZEP-1716`` - 不支持多达 10 个并发会话的 HTTP 服务器示例。
* ``ZEP-1717`` - GPIO：GPIO LEVEL 中断无法在深度睡眠模式下正常工作
* ``ZEP-1723`` - 使用 ISSM 的 llvm/icx 编译器构建时，网络代码/MACROS 中的警告
* ``ZEP-1732`` - zoap_server 示例运行错误。
* ``ZEP-1733`` - 在 ZEP-686 上的工作导致与 3rd-party 代码集成的文档出现回归
* ``ZEP-1745`` - Bluetooth 示例构建失败
* ``ZEP-1753`` - dhcpv4_client 示例在 Arduino 101 上运行错误
* ``ZEP-1754`` - coaps_server 示例在 qemu 上测试失败
* ``ZEP-1756`` - net apps：使用 ISSM 的 llvm/icx 编译器构建时出现 [-Wpointer-sign] 构建警告
* ``ZEP-1758`` - STM32F10x 连接线 SoC 中 PLL2 未正确启用
* ``ZEP-1763`` - Nordic RTC 定时器驱动与 tickless idle 不匹配
* ``ZEP-1764`` - samples：示例用例使用硬编码设备名称，如 "GPIOB" "I2C_0"
* ``ZEP-1768`` - samples：用例缺少 testcase.ini
* ``ZEP-1774`` - 通过 802.15.4 的 IPv6 包含畸形数据包
* ``ZEP-1778`` - tests/power：多核用例无法按预期工作
* ``ZEP-1786`` - TCP 在 Arduino 101 板卡上不工作。
* ``ZEP-1787`` - 在 "CONFIG_LEGACY_KERNEL=n" 时内核事件记录器构建失败
* ``ZEP-1789`` - ARC："samples/logger-hook" 从 sys_ring_buf_get 崩溃 __memory_error
* ``ZEP-1799`` - timeout_order_test _ASSERT_VALID_PRIO 失败
* ``ZEP-1803`` - 运行 dma_transfer_stop 时发生错误
* ``ZEP-1806`` - 使用 LLVM/icx (gdb_server) 的构建警告
* ``ZEP-1809`` - net/ip 中 LLVM/icx 的构建错误
* ``ZEP-1810`` - net/lib/zoap 中 LLVM/icx 的构建失败
* ``ZEP-1811`` - net/ip/net_mgmt.c 中 LLVM/icx 的构建错误
* ``ZEP-1839`` - event_common_prepareA 中的 LL_ASSERT
* ``ZEP-1851`` - obj_tracing 的构建警告
* ``ZEP-1852`` - isr_radio_state_close() 中的 LL_ASSERT
* ``ZEP-1855`` - IP 协议栈缓冲区分配随时间失败
* ``ZEP-1858`` - Zephyr NATS 客户端无法响应 server MSG
* ``ZEP-1864`` - tests/drivers/uart/* 中 llvm icx 构建警告
* ``ZEP-1872`` - samples/net：HTTP 客户端示例应用必须在 QEMU x86 上运行
* ``ZEP-1877`` - samples/net：coaps_server 示例应用在 Arduino 101 上运行失败
* ``ZEP-1883`` - 在 ARC Genuino 101 上启用控制台
* ``ZEP-1890`` - Bluetooth IPSP 示例：用户数据大小太小
