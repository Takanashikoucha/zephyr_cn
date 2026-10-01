.. _zephyr_1.6:

Zephyr 内核 1.6.0
####################

我们很高兴宣布 Zephyr 内核 1.6.0 版本的发布。
该版本引入了统一内核，取代了分离的 nano 内核和 micro 内核，
简化了 Zephyr 的整体架构和编程接口。
新增了对 ARM Cortex-M0/M0+ 系列的支持，并扩展了 Cortex-M 的板卡支持。
此外，该版本为文档、构建基础设施和测试增加了许多改进。

随版本发布的主要增强功能：

* 引入统一内核；nano 内核和 micro 内核已被移除。
* 旧版 API 仍受支持，但已被弃用。
* 旧版测试和示例已迁移至 tests/legacy 和 samples/legacy。
* 新增统一内核文档，并移除了旧版 nanokernel/microkernel 文档。
* 新增对若干 ARM Cortex-M 板卡的支持
* 新增对 USB 大容量存储和文件系统访问的支持。
* 新增原生蓝牙控制器支持。目前支持 nRF51 与 nRF52。

以下是自 v1.5.0 以来按组件划分的详细变更列表：

内核
******

* 引入统一内核。
* 移除已弃用的 Tasks IRQs。
* 移除已弃用的动态中断 API。
* 新增 DLIST 以操作双向链表的所有元素。
* SLIST：新增 sys_slist_get() 以获取并移除头部，同时新增
  append_list 和 merge_slist。
* 新增 nano_work_pending 以检查其是否处于待执行状态。
* 统一：新增对 k_malloc 和 k_free 的支持。
* 将内核对象 event 重命名为 alert，memory map 重命名为 memory slab。
* 变更内存池、内存映射、消息队列和事件处理 API。

架构
*************

* ARC：移除 CONFIG_TIMER0_CLOCK_FREQ。
* ARC：统一链接脚本。
* ARC：移除动态中断。
* ARM：新增使用浮点 ABI 的选项。
* ARM：新增 NXP Kinetis kconfig 选项以配置时钟。
* ARM：移除动态中断和异常。
* ARM：Atmel：新增看门狗寄存器的常量和结构体。
* ARM：新增对 ARM Cortex-M0/M0+ 的支持。
* x86：移除动态中断和异常。
* x86：声明中断控制器的内部 API。
* x86：变更 IRQ 控制器，在无法确定源向量时返回 -1。
* x86：将 Quark SoC 归入 intel_quark 家族。
* x86：优化并简化 IRQ 和异常桩。

板卡
******

* 将板卡 Quark SE devboard 重命名为 Quark SE C1000 devboard。
* 将板卡 Quark SE SSS devboard 重命名为 Quark SE C1000 SS devboard。
* Quark SE C1000：在传感器子系统上禁用 IPM 并启用 UART0。
* 移除 basic_cortex_m3 和 basic_minuteia 板卡。
* Arduino 101：移除备份/恢复脚本。要恢复原始 bootloader
  请改用 flashpack 工具。
* 将 nRF52 Nitrogen 重命名为 96Boards Nitrogen。
* 新增 ARM LTD Beetle SoC 和 V2M Beetle 板卡。
* 新增 Texas Instruments CC3200 LaunchXL 支持。
* 新增对 Nordic Semiconductor nRF51822 的支持。
* 新增对 NXP Hexiwear 板卡的支持。

驱动程序与传感器
*******************

* SPI：修复 SPI 端口编号中的拼写错误。
* Pinmux：移除 Quark dev 未使用的文件。
* I2C：新增 KSDK shim 驱动。
* Ethernet：新增 KSDK shim 驱动。
* Flash：新增 KSDK shim 驱动
* I2C：将配置参数变更为 SoC 特定。
* QMSI：在 QMSI shim 驱动中实现 suspend 和 resume 函数
* 新增 HP206C 传感器。
* 将 config_info 指针变更为 const。
* 新增对 SoCWatch 驱动的支持。
* 新增 FXOS8700 加速度计/磁力计传感器驱动。

网络
**********

* 对 uIP 网络协议栈的微小修复（该协议栈将在 1.7 中弃用）

蓝牙
*********

* 新增原生蓝牙控制器支持。目前支持 nRF51 与 nRF52。
* 控制器与主机实现的新位置：subsys/bluetooth/
* 新增 raw HCI API，以在仅控制器构建中启用物理 HCI 传输。
* 新增 USB 和 UART 的 raw HCI 示例应用。
* 为安全管理器协议新增跨传输配对支持。
* 新增 RFCOMM 支持（用于蓝牙经典）
* 新增基本的持久存储支持（基于文件系统）
* 将 bt_driver API 重命名为 bt_hci_driver，为蓝牙无线电驱动做准备。

构建基础设施
********************

* Makefile：将 outdir 变更为板卡特定目录，以避免构建冲突。
* Makefile：变更为使用 HOST_OS 环境变量。
* Makefile：新增对第三方构建系统的支持。
* Sanity：新增使用环境变量进行过滤的支持。
* Sanity：新增对多工具链的支持。
* Sanity：将 ISSM 和 ARM GCC 嵌入式工具链加入受支持的工具链。
* Sanity：新增传递给构建的额外参数。
* Sanity：移除链接器 VMA/LMA 偏移检查。
* Sysgen：新增 --kernel_type 参数。
* 修改构建基础设施以支持统一内核。
* SDK：Zephyr：新增对最低必需版本的检查。
* 从 Linux 内核导入 get_maintainer.pl。

库
*********

* libc：新增 inttypes.h 中标准类型的一个子集。
* libc：新增对 'z' 长度说明符的支持。
* libc：移除由编译器提供的 stddef.h。
* libc：printf：改进打印代码。
* printk：新增对修饰符的支持。
* 新增 Zephyr 的 CoAP 实现。
* 文件系统：新增扩展或缩小文件的 API。
* 文件系统：新增获取卷统计信息的 API。
* 文件系统：新增刷新已打开文件缓存的 API。

HAL
****

* QMSI：更新至 1.3.1 版本。
* HAL：导入 CC3200 SDK。
* 导入 Nordic MDK nRF51 文件。
* 导入 Kinetis SDK 以太网 phy 驱动。
* 导入 SDK RNGA 驱动。

文档
*************

* 驱动程序：改进 Zephyr 驱动模型。
* 更新设备电源管理 API。
* 统一内核入门。
* 将受支持板卡信息迁移至 wiki.zephyrproject.org 站点。
* 修订内核事件记录器和时序的文档。

测试与示例
****************

* 修复不正确的 printk 用法。
* 移除动态异常测试。
* 新增 USB 示例。
* 新增 CoAP 客户端和服务器的测试与示例。
* 新增 philosophers 统一示例。
* 移除 printf/printk 包装器。
* 新增统一内核 API 示例。
* 导入 TinyCrypt 的 CTR、ECC DSA 和 ECC DH 算法测试用例。

弃用项
************

* 弃用 microkernel 和 nanokernel API。
* 移除动态 IRQs 和异常。
* 移除 Tasks IRQs。

JIRA 相关条目
******************

* ``ZEP-308`` - 构建系统清理与内核/应用构建分离
* ``ZEP-334`` - 统一内核
* ``ZEP-766`` - 通过 USB 大容量存储访问内部文件系统
* ``ZEP-1090`` - 使用新的 QMSI bootloader 流程进行 CPU x86 保存/恢复
* ``ZEP-1173`` - 新增对 bonding remove 的支持
* ``ZEP-48`` - 定义中断控制器的 API
* ``ZEP-181`` - 持久存储 API
* ``ZEP-233`` - 支持 USB 大容量存储设备类
* ``ZEP-237`` - 支持预构建的主机工具
* ``ZEP-240`` - 示例中的 printk/printf 用法
* ``ZEP-248`` - 新增 BOARD/SOC 移植指南
* ``ZEP-342`` - USB DFU
* ``ZEP-451`` - Quark SE 输出默认重定向到 IPM
* ``ZEP-521`` - ARM - 新增浮点 ABI 选择的选项
* ``ZEP-546`` - ARC 上未触发 UART 中断
* ``ZEP-584`` - 如果 SDK 过期则警告用户
* ``ZEP-592`` - Sanitycheck 对多工具链的支持
* ``ZEP-605`` - 通过 BR/EDR 的 SMP
* ``ZEP-614`` - 将 TinyCrypt 2.0 测试用例移植到 Zephyr
* ``ZEP-622`` - 新增截断/缩小文件的 FS API
* ``ZEP-627`` - 将 Trickle 支持从 Contiki 移植到当前协议栈
* ``ZEP-635`` - 新增扩展文件的 FS API
* ``ZEP-636`` - 新增获取卷总空间和空闲空间的 FS API
* ``ZEP-640`` - 从 Zephyr 移除动态 IRQs/异常
* ``ZEP-653`` - QMSI shim 驱动：Watchdog：实现 suspend 和 resume 回调
* ``ZEP-654`` - QMSI shim 驱动：I2C：实现 suspend 和 resume 回调
* ``ZEP-657`` - QMSI shim 驱动：AONPT：实现 suspend 和 resume 回调
* ``ZEP-661`` - QMSI shim 驱动：SPI：实现 suspend 和 resume 回调
* ``ZEP-688`` - 统一架构链接脚本中重复的部分
* ``ZEP-715`` - 新增 K64F 时钟配置
* ``ZEP-716`` - 新增 Hexiwear 板卡支持
* ``ZEP-717`` - 新增 ksdk I2C shim 驱动
* ``ZEP-718`` - 新增 ksdk 以太网 shim 驱动
* ``ZEP-721`` - 新增 FXOS8700 加速度计/磁力计传感器驱动
* ``ZEP-737`` - 从上游更新主机工具：fixdep.c
* ``ZEP-740`` - PWM API：检查 'flags' 参数是否真的需要
* ``ZEP-745`` - 重新审视 PWM 驱动 API 的设计
* ``ZEP-750`` - Arduino 101 板卡应支持使用原始 bootloader 的一种配置
* ``ZEP-758`` - 将 Quark SE Devboard 重命名为其官方名称：Quark SE C1000
* ``ZEP-767`` - 新增刷新已打开文件缓存的 FS API
* ``ZEP-775`` - 在 Arduino 101 上默认启用 USB CDC 并将串口重定向到 USB
* ``ZEP-783`` - ARM Cortex-M0/M0+ 支持
* ``ZEP-784`` - 新增对 Nordic Semiconductor nRF51822 SoC 的支持
* ``ZEP-850`` - 移除过时的板卡 basic_minuteia 和 basic_cortex_m3
* ``ZEP-906`` - [unified] 新增调度器时间片支持
* ``ZEP-907`` - 测试内存池支持（含 mailbox）
* ``ZEP-908`` - 新增将任务卸载到 fiber 的支持
* ``ZEP-909`` - 为 ARM 适配 tickless idle + 电源管理
* ``ZEP-910`` - 为 x86 适配 tickless idle
* ``ZEP-912`` - 完成内核对象类型的重命名
* ``ZEP-916`` - 消除内核对象 API 异常
* ``ZEP-920`` - 调查 malloc/free 支持
* ``ZEP-921`` - 杂项文档工作
* ``ZEP-922`` - 修订内核事件记录器的文档
* ``ZEP-923`` - 修订时序的文档
* ``ZEP-924`` - 修订中断的文档
* ``ZEP-925`` - 消息队列的 API 变更
* ``ZEP-926`` - 内存池的 API 变更
* ``ZEP-927`` - 内存映射的 API 变更
* ``ZEP-928`` - 事件处理的 API 变更
* ``ZEP-930`` - 切换到统一内核
* ``ZEP-933`` - 统一内核 ARC 移植
* ``ZEP-934`` - NIOS_II 移植
* ``ZEP-935`` - 内核记录器支持（验证）
* ``ZEP-954`` - 更新设备 PM API 以允许设置额外的电源状态
* ``ZEP-957`` - 为新的统一内核 API 用法创建示例 sample
* ``ZEP-959`` - 与上游 Linux 同步 checkpatch.pl
* ``ZEP-966`` - em_starterkit 需要支持 EM7D SOC
* ``ZEP-975`` - 将 DNS 客户端移植到新 IP 协议栈
* ``ZEP-981`` - 为 include/kernel.h 和 include/legacy.h 两者新增 doxygen 文档
* ``ZEP-989`` - 缓存下一个就绪线程，而不是以冗长的方式查找
* ``ZEP-993`` - Quark SE (x86)：重构保存/恢复执行上下文功能
* ``ZEP-994`` - Quark SE (ARC)：新增 PMA 示例
* ``ZEP-996`` - 从 i2c_qmsi 驱动重构保存/恢复功能
* ``ZEP-997`` - 从 spi_qmsi 驱动重构保存/恢复功能
* ``ZEP-998`` - 从 uart_qmsi 驱动重构保存/恢复功能
* ``ZEP-999`` - 从 gpio_qmsi 驱动重构保存/恢复功能
* ``ZEP-1000`` - 从 rtc_qmsi 驱动重构保存/恢复功能
* ``ZEP-1001`` - 从 wdt_qmsi 驱动重构保存/恢复功能
* ``ZEP-1002`` - 从 counter_qmsi_aonpt 驱动重构保存/恢复功能
* ``ZEP-1004`` - 扩展 counter_qmsi_aon 驱动以支持保存/恢复外设上下文
* ``ZEP-1005`` - 扩展 dma_qmsi 驱动以支持保存/恢复外设上下文
* ``ZEP-1006`` - 扩展 soc_flash_qmsi 驱动以支持保存/恢复外设上下文
* ``ZEP-1008`` - 扩展 pwm_qmsi 驱动以支持保存/恢复外设上下文
* ``ZEP-1023`` - 统一内核入门中的 workq
* ``ZEP-1030`` - 在传感器子系统上启用 SoC 外设的 QMSI shim 驱动
* ``ZEP-1043`` - 将 QMSI 更新至 1.2
* ``ZEP-1045`` - 新增/增强 shim 层以包装 SoC 特定的 PM 实现
* ``ZEP-1046`` - 实现 bootloader 与 Zephyr 之间的 RAM 共享
* ``ZEP-1047`` - 适配 QMSI boot loader 中新的 PM 相关启动流程变更
* ``ZEP-1106`` - 修复来自 TCF 的所有测试失败
* ``ZEP-1107`` - 将 QMSI 更新至 1.3
* ``ZEP-1109`` - Texas Instruments CC3200 LaunchXL 支持
* ``ZEP-1119`` - 将顶层 usb/ 迁移至 sys/usb
* ``ZEP-1120`` - 将顶层 fs/ 迁移至 sys/fs
* ``ZEP-1121`` - 新增启用 Zephyr 中 SoCWatch 的配置支持
* ``ZEP-1140`` - 新增 power_mgr 示例应用的统一内核版本，以使用新内核测试 PM 代码
* ``ZEP-1188`` - 新增获取唤醒事件挂起中断的 API
* ``ZEP-1191`` - 为 Hexiwear 板卡创建 wiki 页面
* ``ZEP-1235`` - 文件系统浏览的基本 shell 支持
* ``ZEP-1245`` - ARM LTD V2M Beetle 支持
* ``ZEP-1313`` - 移植和用户指南必须包含安全章节
* ``ZEP-1386`` - 修订电源管理文档以反映最新变更
* ``ZEP-199`` - Zephyr 驱动模型没有文档
* ``ZEP-436`` - 测试用例 tests/kernel/test_mem_safe 在 ARM 硬件上失败
* ``ZEP-471`` - 使用多播地址的以太网数据包不工作
* ``ZEP-472`` - 快速连续发送时以太网数据包丢失。
* ``ZEP-517`` - Windows 上构建失败 "zephyr/Makefile:869: \*\*\* multiple target patterns"
* ``ZEP-528`` - ARC 有两份几乎相同的链接脚本副本
* ``ZEP-577`` - 示例应用源代码在 Windows 上无法编译
* ``ZEP-601`` - 启用 CONFIG_DEBUG_INFO
* ``ZEP-602`` - 由 CPU 触发时，未处理的 CPU 异常/中断报告错误的故障向量
* ``ZEP-615`` - SPI flash w25qxxdv 驱动头文件中列出不受支持的 flash 擦除大小
* ``ZEP-639`` - device_pm_ops 结构体应定义为 static
* ``ZEP-686`` - docs："Application Development Primer" 和 "Developing an Application and the Build System" 中的信息大量重复
* ``ZEP-698`` - samples/task_profiler 问题
* ``ZEP-707`` - mem_safe 测试踩踏 .data 顶部和 .noinit 底部
* ``ZEP-724`` - Windows 上构建失败：'make: execvp: uname: File or path name too long'
* ``ZEP-733`` - 最小 libc 不应提供 stddef.h
* ``ZEP-762`` - 来自 mingw make 系统的意外 "abspath" 和 "notdir"
* ``ZEP-777`` - samples/driver/i2c_stts751：来自 "select DMA_QMSI" 的 kconfig 构建警告
* ``ZEP-778`` - Samples/drivers/i2c_lsm9ds0：来自 "select DMA_QMSI" 的 kconfig 构建警告
* ``ZEP-779`` - 使用当前 MinGW gcc 版本 5.3.0 会破坏 Windows 上的 Zephyr 构建
* ``ZEP-845`` - Arduino 101 上 ARC 的 UART 行为异常
* ``ZEP-905`` - 使用 CROSS_COMPILE 时 arduino_due 目标的 hello_world 编译失败
* ``ZEP-940`` - 无法获取 ATT 响应
* ``ZEP-950`` - USB：设备未出现在 USB20CV 测试套件中
* ``ZEP-961`` - samples：运行 aon_counter 用例后其他用例无法执行
* ``ZEP-967`` - Sanity 未以断言（-R）构建 'samples/usb/dfu'
* ``ZEP-970`` - Sanity 未以断言（-R）构建 'tests/kernel/test_build'
* ``ZEP-982`` - 最小 libc 中 EWOULDBLOCK != EAGAIN
* ``ZEP-1014`` - [TCF] tests/bluetooth/init 构建失败
* ``ZEP-1025`` - 统一内核构建有时因缺少 .d 依赖文件而损坏。
* ``ZEP-1027`` - GCC ARM 的文档不准确
* ``ZEP-1031`` - qmsi：dma：驱动测试在 LLVM 下失败
* ``ZEP-1048`` - grove_lcd 示例：禁用串口时示例不工作
* ``ZEP-1051`` - 两次 defrag 后 mpool 分配失败...
* ``ZEP-1062`` - 统一内核与 CONFIG_NEWLIB_LIBC 不兼容
* ``ZEP-1074`` - 收到 ATT insufficient Authentication 时 ATT 重试行为异常
* ``ZEP-1076`` - "samples/philosophers/unified" 使用动态栈时构建失败
* ``ZEP-1077`` - "samples/philosophers/unified" 在 NUM_PHIL<6 时出现构建警告
* ``ZEP-1079`` - 导入组件的许可证不明确
* ``ZEP-1097`` - 并发 tx 和 rx 时 ENC28J60 驱动失败
* ``ZEP-1098`` - ENC28J60 无法接收大数据帧
* ``ZEP-1100`` - 当前 master 仍自报为 1.5.0
* ``ZEP-1101`` - SYS_KERNEL_VER_PATCHLEVEL() 等将版本号人为限制为 4 位
* ``ZEP-1124`` - tests/kernel/test_sprintf/microkernel/testcase.ini#test 在 frdm_k64f 上失败
* ``ZEP-1130`` - 构建 test_hmac_prng 时发生 region 'RAM' overflowed
* ``ZEP-1138`` - 使用 ENC28J60 驱动时，接收的数据包未从 IP 协议栈传递到上层
* ``ZEP-1139`` - 修复电源管理与统一内核一起构建时的构建错误
* ``ZEP-1141`` - 使用统一内核类型时 TinyCrypt SHA256 测试因系统崩溃而失败
* ``ZEP-1144`` - 使用统一内核类型时 TinyCrypt AES128 固定密钥变文测试失败
* ``ZEP-1145`` - TinyCrypt HMAC 测试后系统挂起
* ``ZEP-1146`` - zephyrproject.org 主页需要针对 1.6 版本进行技术审查
* ``ZEP-1149`` - 将 ztest 框架移植到统一内核
* ``ZEP-1154`` - 统一内核下 tests/samples 失败
* ``ZEP-1155`` - 修复文件系统 API 命名空间
* ``ZEP-1163`` - LIB_INCLUDE_DIR 在 Makefile 第二遍中被破坏
* ``ZEP-1164`` - ztest 跳过等待测试用例完成执行
* ``ZEP-1179`` - 使用 ISSM (icx) 的 LLVM 编译时出现构建问题
* ``ZEP-1182`` - kernel.h doxygen 显示意外的 "asm" 块
* ``ZEP-1183`` - 初始化 bt 时 btshell 返回 "panic: errcode -1"
* ``ZEP-1195`` - 向应用传递错误的 ATT 错误码
* ``ZEP-1199`` - [L2CAP] 无信用额度接收数据包
* ``ZEP-1219`` - [L2CAP] 发送数据超过最大 PDU 大小
* ``ZEP-1221`` - 配对期间连接超时
* ``ZEP-1226`` - cortex M7 移植汇编器错误
* ``ZEP-1227`` - 统一内核下 ztest native 测试不工作
* ``ZEP-1232`` - 每日构建在断言上失败
* ``ZEP-1234`` - 因统一迁移移除 fiber* API 破坏了 USB 大容量存储补丁集
* ``ZEP-1247`` - 测试 tests/legacy/benchmark/latency_measure 对每日 sanitycheck 损坏
* ``ZEP-1252`` - 测试 test_chan_blen_transfer 无法为 quark_d2000_crb 构建
* ``ZEP-1277`` - flash 驱动 (w25qxxdv) 擦除函数未检查偏移对齐
* ``ZEP-1278`` - flash 驱动 (w25qxxdv) 擦除偏移的边界检查不正确
* ``ZEP-1287`` - ARC SPI 1 端口不工作
* ``ZEP-1289`` - k_sem_take 存在竞争条件
* ``ZEP-1291`` - libzephyr.a 对 phony "gcc" 目标的依赖
* ``ZEP-1293`` - ENC28J60 驱动在 Arduino 101 上不工作
* ``ZEP-1295`` - kernel.h:k_work_pending() 中不正确的 doxygen 注释
* ``ZEP-1297`` - test/legacy/kernel/test_mail：在 ARC 平台上失败
* ``ZEP-1299`` - 使用 DMA suspend 和 resume 操作时系统无法完全恢复
* ``ZEP-1302`` - 长帧 rx/tx 时 ENC28J60 失败
* ``ZEP-1303`` - 配置提到 >32 线程优先级，但内核不支持
* ``ZEP-1309`` - ARM 使用内存末尾作为其初始化栈
* ``ZEP-1310`` - ARC 使用内存末尾作为其初始化栈
* ``ZEP-1312`` - ARC：异步发送消息时软件在 k_mbox_get() 处崩溃
* ``ZEP-1319`` - 在 ARM 平台上启用 CONFIG_RUNTIME_NMI 时 Zephyr 无法编译
* ``ZEP-1341`` - power_states 测试应用向 post_ops 函数传递错误的电源状态值
* ``ZEP-1343`` - tests/drivers/pci_enum：因缺少提交而在 QEMU ARM 和 X86 上失败
* ``ZEP-1345`` - cpu 上下文保存和恢复可能损坏栈
* ``ZEP-1349`` - 中断启用时 ARC sleep 需要传递中断优先级阈值
* ``ZEP-1353`` - FDRM k64f 在正常 flash 模式下控制台输出损坏

已知问题
************

* ``ZEP-1405`` - /subsys/bluetooth/host/l2cap_br.c 中的函数 l2cap_br_conn_req
  引用了未初始化的指针
