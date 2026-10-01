.. _zephyr_1.5:

Zephyr 内核 1.5.0
####################

Zephyr 工程团队很高兴宣布 Zephyr 内核 1.5.0 的发布。
这是首个遵循 3 个月发布节奏的版本。
该版本包含大量修复以及对重要特性的支持。
其他变更包括对新驱动程序、传感器和板卡的支持。

随版本发布的主要增强功能：

- TCP 支持
- 集成 Paho MQTT 库支持（含 QoS）
- 闪存文件系统支持
- 集成 mbedTLS 加密库
- 改进的 BR/EDR 支持（尤其是 L2CAP）
- 支持 Altera Nios II/f 软 CPU 架构

以下是自 v1.4.0 以来按组件划分的详细变更列表：

内核
******

- 新增 nano_fifo_put_list() API，允许在 nanokernel FIFO 上入队一组元素。
- 移除未使用的内存池结构体字段。
- 增强内存池代码。

架构
*************

- ARM：更新以包含浮点寄存器。
- Altera Nios II/f 软 CPU 架构支持
    - 内部中断控制器
    - Avalon 定时器
    - Avalon JTAG UART（轮询模式）作为 qemu-system-nios2 的默认，
      16550 UART 作为 Altera MAX10 的默认。

板卡
******

- 新增 Nios II QEMU 板卡。
- 新增 Altera MAX10 FPGA 配置。

驱动程序与传感器
*******************

- 传感器：新增 I2C HMC5883L 磁力计驱动。
- 传感器：新增 I2C TMP112 温度传感器驱动。
- 传感器：新增 MAX44009 光照传感器驱动。
- 传感器：新增 LPS25HB 驱动。
- HAL：更新 QMSI 驱动至 1.1
- 新增 DMA QMSI shim 驱动。
- 新增 Quark SE USB 设备控制器驱动。
- 为 QMSI 驱动新增 suspend/resume。
- 为 QMSI 驱动的临界区新增保护。
- 新增 Zephyr 文件系统 API。
- 新增 ENC28J60 以太网 SPI 模块驱动。

网络
**********

- TCP 支持
- IP 协议栈中连接处理的修复。
- 允许发送零长度用户数据 IP 数据包。

网络缓冲区

- 新增 net_buf_simple API，用于轻量级栈上（或静态）缓冲区，
  适用于 net_buf（及其关联的池）过于重的场景。
  net_buf API 现在将 net_buf_simple 作为内部实现细节使用。
- 新增对网络缓冲区分片的支持。
- 新增更多 net_buf 大端辅助函数。

蓝牙
*********

- 对 nble 驱动的多个修复与改进。
- 新增处理带外数据（如本地地址）的 API。
- 多处较小的修复与改进。

构建与基础设施
************************

- 新增 "qemugdb" 目标，用于在 1234 端口启动本地 GDB。
- 新增脚本，用于过滤构建输出中的已知问题。
- Sanity：新增 "-R" 选项，以启用断言构建所有测试。

库
*********

- 文件系统：导入开源 FAT FS 0.12a 代码。
- 加密：导入 mbedTLS 库。
- 加密：更新 TinyCrypt 库至 2.0。

文档
*************

- 修复构建过程中的所有文档警告。
- 修复若干拼写错误、商标和语法问题。
- 将所有板卡文档迁移至 wiki。
- 将代码贡献文档迁移至 wiki。
- 在依赖项列表中新增 "ncurses" 包。
- 更新 macOS 说明。

测试与示例
****************

- 示例：用新的 SYS_LOG 宏替换旧的调试宏。
- 新增 TMP112 传感器应用。
- 新增 Quark SE 电源管理示例应用。
- 为内存传输示例新增 DMA 内存。
- 新增 MAX44009 光照传感器示例。
- 新增 MQTT 发布者和订阅者示例。
- 新增 mbedTLS 示例客户端。

JIRA 相关条目
******************


故事
========

* ``ZEP-49`` - x86：统一分离的 SysV 和 IAMCU 代码
* ``ZEP-55`` - 在 ARC 上启用 nanokernel test_context
* ``ZEP-58`` - 调查 -fomit-frame-pointer 的使用
* ``ZEP-60`` - irq 优先级应重新基于安全值
* ``ZEP-69`` - 扩展 PWM API 以使用任意时间单位
* ``ZEP-203`` - 清理静态异常 API
* ``ZEP-225`` - 新增内核 API 将 SoC 置入深度睡眠（DS）状态
* ``ZEP-226`` - 更新示例 PMA 以支持设备 suspend/resume
* ``ZEP-227`` - 新增内核 API 将 SoC 置入低功耗状态（LPS）
* ``ZEP-228`` - 仿照 POSIX 设计的文件系统接口
* ``ZEP-232`` - 支持 USB 通信设备类 ACM
* ``ZEP-234`` - 提供直接内存访问（DMA）接口
* ``ZEP-243`` - 为板卡创建 Wiki 结构
* ``ZEP-249`` - nios2：在 nanokernel sanitycheck 运行中启用 altera_max10 板卡
* ``ZEP-254`` - nios2：定义 NANO_ESF 结构体并填充 _default_esf
* ``ZEP-270`` - nios2：确定 PERFOPT_ALIGN 的最佳值
* ``ZEP-271`` - nios2：启用微内核与测试用例
* ``ZEP-272`` - nios2：添加全局指针支持
* ``ZEP-273`` - nios2：实现烧录脚本
* ``ZEP-274`` - nios2：记录 GDB 调试流程
* ``ZEP-275`` - nios2：确定指令/数据缓存支持的范围
* ``ZEP-279`` - nios2：演示 nanokernel hello world
* ``ZEP-285`` - 基于 SPI Flash 的 FAT 文件系统支持
* ``ZEP-289`` - nios2：实现 kernel_event_logger
* ``ZEP-291`` - ENC28J60 以太网设备驱动
* ``ZEP-304`` - 调查 QEMU 对 Nios II 的支持
* ``ZEP-327`` - Thread 支持所需的加密库
* ``ZEP-340`` - TLS/SSL
* ``ZEP-354`` - 为 Quark SE 核心提供 DMA 驱动
* ``ZEP-356`` - DMA 设备支持
* ``ZEP-357`` - 支持 MAX44009 传感器
* ``ZEP-358`` - 新增 TMP112 传感器支持
* ``ZEP-412`` - 为 LMT 的 RTC 驱动新增驱动 API 重入支持
* ``ZEP-414`` - 为闪存驱动新增驱动 API 重入支持
* ``ZEP-415`` - aaU，我想使用 NATS 消息协议将传感器数据发送到云端
* ``ZEP-416`` - MQTT 客户端能力：QoS1、QoS2
* ``ZEP-424`` - AON 计数器驱动需新增驱动 API 重入支持
* ``ZEP-430`` - 为 PWM shim 驱动新增驱动 API 重入支持
* ``ZEP-434`` - HMC5883L 磁力计驱动
* ``ZEP-440`` - 为 WDT shim 驱动新增驱动 API 重入支持
* ``ZEP-441`` - 为 GPIO shim 驱动新增驱动 API 重入支持
* ``ZEP-489`` - nios2：处理未实现的乘法/除法指令
* ``ZEP-500`` - 域名系统（DNS）客户端库
* ``ZEP-506`` - nios2：支持在 Altera MAX10 上裸机启动和 XIP
* ``ZEP-511`` - 在 PMA 中新增深度睡眠支持
* ``ZEP-512`` - 为部分核心设备新增 suspend/resume 支持，以启用 PMA 中的深度睡眠支持
* ``ZEP-541`` - 将 QMSI 发布版本集成到 Zephyr
* ``ZEP-567`` - netz 示例代码
* ``ZEP-568`` - MQTT QoS 示例应用
* ``ZEP-573`` - IoT 应用必须使用 netz API
* ``ZEP-590`` - 将 Zephyr 的 TinyCrypt 更新至 2.0 版本
* ``ZEP-643`` - 新增文件系统 API 文档
* ``ZEP-650`` - Quark SE：实现 PM 参考应用
* ``ZEP-652`` - QMSI shim 驱动：RTC：实现 suspend 和 resume 回调
* ``ZEP-655`` - QMSI shim 驱动：PWM：实现 suspend 和 resume 回调
* ``ZEP-658`` - QMSI shim 驱动：GPIO：实现 suspend 和 resume 回调
* ``ZEP-659`` - QMSI shim 驱动：UART：实现 suspend 和 resume 回调
* ``ZEP-662`` - QMSI shim 驱动：Pinmux：实现 suspend 和 resume 回调

史诗
====

* ``ZEP-278`` - 在 Altera Max10 上启用 Nios II CPU
* ``ZEP-284`` - 闪存文件系统支持
* ``ZEP-305`` - 设备 Suspend / Resume 基础设施
* ``ZEP-306`` - PWM 启用
* ``ZEP-406`` - 驱动应当可重入

缺陷
===

* ``ZEP-68`` - 最终镜像包含某些例程的重复项
* ``ZEP-156`` - PWM Set Value API 行为不正确
* ``ZEP-158`` - PWM Set Duty Cycle API 不工作
* ``ZEP-180`` - make menuconfig 用户提供的选项在构建时被忽略
* ``ZEP-187`` - BLE API 没有文档
* ``ZEP-218`` - [drivers/nble][PTS_TEST] 修复对 Prepare Write Request 使用错误错误码响应的问题
* ``ZEP-221`` - [drivers/nble][PTS_TEST] 实现 Execute Write Request 处理器
* ``ZEP-369`` - 树外构建时，应用目标文件未放入 outdir
* ``ZEP-379`` - 调试时 _k_command_stack 可能初始化不当
* ``ZEP-384`` - 与 BMC150 传感器进行 I2C 通信后 D2000 挂起
* ``ZEP-401`` - 在 set_values 中 off time 为 0 时 PWM 驱动关闭引脚
* ``ZEP-423`` - Quark D2000 CRB 文档应包含烧录 bootloader 的说明
* ``ZEP-435`` - Ethernet/IPv4/TCP：ip_buf_appdatalen 返回错误值
* ``ZEP-456` - doc：``IDT security``` 章节消失
* ``ZEP-457`` - doc：contribute/doxygen/typedefs.rst：示例文件损坏
* ``ZEP-459`` - doc：HTML 中 kconfig 参考条目缺少标题
* ``ZEP-460`` - doc：记录 DEVICE* 宏的参数
* ``ZEP-461`` - 1.4.0 版本破坏了 BMI160 示例以及基于它的应用
* ``ZEP-463`` - 入门指南"next"链接未跳转到"匿名检出源代码"章节
* ``ZEP-469`` - Ethernet/IPv4/TCP：服务器模式下的 net_receive 与 net_reply
* ``ZEP-474`` - ND：邻居缓存未被清除
* ``ZEP-475`` - 定时器回调例程问题：检查的条件不正确
* ``ZEP-478`` - Linux 设置文档缺少在 Fedora 上安装 curses 开发包的步骤
* ``ZEP-497`` - Ethernet/IPv4/TCP：无法获取空闲缓冲区
* ``ZEP-499`` - TMP007 驱动对负温度返回无效值
* ``ZEP-514`` - 微内核内存池 defrag() 中的内存损坏
* ``ZEP-516`` - Ubuntu 设置说明缺少 'upgrade' 步骤
* ``ZEP-518`` - SPI 在 Arduino101 上不工作
* ``ZEP-522`` - TCP/客户端模式：断开连接
* ``ZEP-523`` - 由 DEFINE_FIFO 宏定义的 FIFO 使用同一个内存缓冲区
* ``ZEP-525`` - srctree 变更正在破坏应用
* ``ZEP-526`` - 构建 "kernel event logger" 示例应用在 BOARD=quark_d2000_crb 时失败
* ``ZEP-534`` - 扫描文档中 "platform/board/SoC" 的一致使用
* ``ZEP-537`` - doc：创建外部 wiki 页面 "Maintainers"
* ``ZEP-545`` - x86 QMSI ADC 的 CONFIG_ADC_QMSI_SAMPLE_WIDTH 默认值错误
* ``ZEP-547`` - [nble] 重连后加密启动失败
* ``ZEP-554`` - samples/drivers/aon_counter 检查 README 文件
* ``ZEP-555`` - ARM 上 CONFIG_FLOAT=y 时未正确链接 libgcc
* ``ZEP-556`` - I2C 传输期间系统挂起
* ``ZEP-565`` - Ethernet/IPv4/TCP：最近的提交正在破坏网络支持
* ``ZEP-571`` - ARC 内核 BAT 因嵌套中断中的竞争而失败
* ``ZEP-572`` - X86 内核 BAT 失败：内核分配失败！
* ``ZEP-575`` - Ethernet/IPv4/UDP：ip_buf_appdatalen 返回错误值
* ``ZEP-595`` - UART：usb 模拟 uart 在 poll 模式下不工作
* ``ZEP-598`` - 不支持 CoAP Link 格式过滤
* ``ZEP-611`` - 下载页面上的链接命名不一致
* ``ZEP-616`` - OS X 设置说明在 El Capitan 上不工作
* ``ZEP-617`` - MQTT 示例因缺少 netz.h 文件而构建失败。
* ``ZEP-621`` - samples/static_lib：fatal error: stdio.h: No such file or directory
* ``ZEP-623`` - MQTT 示例 mqtt.h 缺少 "mqtt_unsubscribe" 函数
* ``ZEP-632`` - MQTT 无法重新连接到 broker。
* ``ZEP-633`` - samples/usb/cdc_acm：undefined reference to 'uart_qmsi_pm_save_config'
* ``ZEP-642`` - 各驱动对 pwm_pin_set_values 参数的解释不一致
* ``ZEP-645`` - ARC QMSI ADC shim 驱动无法读取采样数据
* ``ZEP-646`` - 当 GY2561 与 GY271 传感器连接到 I2C 总线时，I2C 无法读取 GY2561 传感器
* ``ZEP-647`` - 电源管理状态存储应使用 GPS1 而非 GPS0
* ``ZEP-669`` - broker 将主题投递给客户端但客户端未读取时，MQTT 无法 pingreq。
* ``ZEP-673`` - Sanity 超时后崩溃且不终止 qemu
* ``ZEP-679`` - HMC5883L I2C 寄存器读取顺序
* ``ZEP-681`` - MQTT 客户端示例构建时产生过多警告。
* ``ZEP-687`` - docs：Subsystems/Networking 章节几乎为空
* ``ZEP-689`` - em_starterkit 上的构建失败
* ``ZEP-695`` - FatFs 无法使用 Newlib 编译
* ``ZEP-697`` - samples/net/test_15_4 无法通过 sanitycheck 构建
* ``ZEP-703`` - QMSI 更新后 USB 示例应用损坏
* ``ZEP-704`` - test_atomic 在 ARC 上无法完成
* ``ZEP-708`` - tests/kernel/test_ipm 在 Arduino 101 上失败
* ``ZEP-739`` - 为 quark_se devboard 构建示例时出现警告

已知问题
============

* ``ZEP-517`` - Windows 上构建失败 "zephyr/Makefile:869: \*\*\* multiple target patterns"
   - 无变通方案，将在未来版本中修复。

* ``ZEP-711`` - I2c：以 fast plus 模式写入失败
   - 无变通方案需要，不支持高速模式。

* ``ZEP-724`` - Windows 上构建失败：'make: execvp: uname: File or path name too long'
   - 无变通方案，将在未来版本中修复。

* ``ZEP-467`` - 使用 UART 和控制台时挂起。
   - 无变通方案，将在未来版本中修复。

* ``ZEP-599`` - 周期性 REST 资源的周期性回调函数未被调用
   - 无变通方案，将在未来版本中修复。

* ``ZEP-471`` - 使用多播地址的以太网数据包不工作
   - 无变通方案，将在未来版本中修复。

* ``ZEP-473`` - 目标多播地址不正确
   - 无变通方案，将在未来版本中修复。
