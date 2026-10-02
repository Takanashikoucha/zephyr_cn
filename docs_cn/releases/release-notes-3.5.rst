:orphan:

.. _zephyr_3.5:

Zephyr 3.5.0
############

我们很高兴地宣布 Zephyr 版本 3.5.0 的发布。

本次发布的主要增强功能包括：

* 新增对可链接可加载扩展（llext）的支持
* 新增 native_sim 仿真器目标（native_posix 的继任者）
* 新增电池充电器驱动 API
* 新增硬件自旋锁驱动 API
* 新增调制解调器子系统
* 新增对 45 个以上新板级的支持
* 网络：对 CoAP、连接管理器、DHCP、以太网、gPTP、ICMP、IPv6 和 LwM2M 的改进
* 蓝牙：对控制器、音频、Mesh，以及主机栈的总体改进
* 改进 LVGL 图形库集成
* 集成 CodeChecker 静态分析器支持
* Picolibc 现在是默认 C 标准库

从 Zephyr v3.4.0 迁移应用到 Zephyr v3.5.0 时所需或建议的更改概述
可在单独的 :ref:`migration guide<migration_3.5>` 中找到。

以下各节按组件提供详细的变更列表。

安全漏洞相关
******************************
本次发布解决了以下 CVE：

更详细的信息可参见：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2023-3725 `Zephyr 项目 bug 跟踪器 GHSA-2g3m-p6c7-8rr3
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-2g3m-p6c7-8rr3>`_

* CVE-2023-4257 `Zephyr 项目 bug 跟踪器 GHSA-853q-q69w-gf5j
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-853q-q69w-gf5j>`_

* CVE-2023-4258 `Zephyr 项目 bug 跟踪器 GHSA-m34c-cp63-rwh7
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-m34c-cp63-rwh7>`_

* CVE-2023-4259 `Zephyr 项目 bug 跟踪器 GHSA-gghm-c696-f4j4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gghm-c696-f4j4>`_

* CVE-2023-4260 `Zephyr 项目 bug 跟踪器 GHSA-gj27-862r-55wh
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-gj27-862r-55wh>`_

* CVE-2023-4263 `Zephyr 项目 bug 跟踪器 GHSA-rf6q-rhhp-pqhf
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rf6q-rhhp-pqhf>`_

* CVE-2023-4264 `Zephyr 项目 bug 跟踪器 GHSA-rgx6-3w4j-gf5j
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-rgx6-3w4j-gf5j>`_

* CVE-2023-4424：截至 2023-11-01 处于保密期

* CVE-2023-5055：截至 2023-11-01 处于保密期

* CVE-2023-5139：截至 2023-10-25 处于保密期

* CVE-2023-5184 `Zephyr 项目 bug 跟踪器 GHSA-8x3p-q3r5-xh9g
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8x3p-q3r5-xh9g>`_

* CVE-2023-5563 `Zephyr 项目 bug 跟踪器 GHSA-98mc-rj7w-7rpv
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-98mc-rj7w-7rpv>`_

* CVE-2023-5753 `Zephyr 项目 bug 跟踪器 GHSA-hmpr-px56-rvww
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-hmpr-px56-rvww>`_

内核
******

* 新增对通过 :c:func:`k_thread_stack_alloc` 进行动态线程栈分配的支持
* 新增对 :c:func:`k_spin_trylock` 的支持
* 新增 :c:func:`k_object_is_valid`，用于检查内核对象是否有效。这替换了
  在整个代码树中重复出现的代码。

架构
*************

* ARC

  * 为 ARC VPX 处理器引入标量移植
  * 为 ARCv3 HS（32 位和 64 位）SMP 平台引入支持，最多 12 个 CPU 核心
  * 重新设计 ARC MWDT 工具链的 GNU 辅助工具使用方式。现在辅助工具可以从
    Zephyr SDK（如果已安装 SDK）中使用
  * 修复动态线程栈分配
  * 修复 STR 汇编宏偏移计算问题，该问题可能导致 ARCv3 64 位构建错误
  * 清理并使 ARC MWDT 工具链路径（ARCMWDT_TOOLCHAIN_PATH）的处理
    更用户友好

* ARM

  * Arm Cortex-M 的架构支持已从 Arm
    Cortex-A 和 Cortex-R 中分离。这包括用于处理
    IRQ 管理、异常处理、线程处理和切换等任务的独立源模块。
    有关实现细节，请参见 :github:`60031`。

* ARM64

* RISC-V

  * 新增使用 PMP 检测空指针异常的支持。
  * 新增 :kconfig:option:`CONFIG_RISCV_RESERVED_IRQ_ISR_TABLES_OFFSET`
    选项，允许在指定偏移处使用 IRQ 向量，以满足
    Core-Local Interrupt Controller RISC-V 规范设定的要求。
  * 新增 :kconfig:option:`CONFIG_RISCV_SOC_HAS_CUSTOM_SYS_IO` 选项，
    允许使用自定义系统输入/输出函数。
  * 引入 :kconfig:option:`CONFIG_RISCV_TRAP_HANDLER_ALIGNMENT` 选项，
    用于设置 trap 处理代码的正确对齐，该对齐取决于
    ``MTVEC.BASE`` 字段大小，并且是平台或应用特定的。

* Xtensa

  * 新增基本 MMU v2 支持。

* x86

  * 新增对 Intel Alder Lake 板级的支持
  * 新增对 Intel Sensor Hub（ISH）的支持

* POSIX

  * 已重新设计以使用原生仿真器。
  * 已新增板级。
  * 对于新板级，可以使用嵌入式 C 库，并避免与主机符号
    和库的冲突。
  * :ref:`POSIX OS 抽象<posix_support>` 在这些新板级中受支持。
  * 现在支持 AMP 目标。
  * 新增对 LLVM 源剖析/覆盖率的支持。

蓝牙
*********

* 音频

  改进编解码器配置和编解码器能力的内存使用。修复 BAP
  和 BAP 相关服务（ASCS、PACS、BASS）中的多个 bug，
  以及缺失的功能（例如适当的通知处理）。

  * 新增 BAP ``bt_bap_stream_get_tx_sync``
  * 新增 CAP 流发送和 tx 同步
  * 新增 ``bt_audio_codec_cap_get`` 辅助函数
  * 新增对 CAP 中长时间读/写的支持
  * 修复 ASCS 源 ASE 链路丢失状态转换
  * 修复 ASCS 可能的 ASE 泄漏
  * 修复 ASCS 在 ASE 不处于流状态时丢弃 ISO PDU
  * 修复 BAP ``bt_bap_scan_delegator_find_state`` 实现
  * 修复 BAP 在 ``broadcast_sink_create`` 中 PA 同步和 ID 的问题
  * 修复 TMAS 特征权限
  * 修复 ``tbs_client`` 缺失的发现完成事件
  * 修复音频栈在音频元数据中接受空 CCID 列表
  * 修复 ASCS 中 metadata_backup 的错误大小
  * 修复 ASCS ASE 可能卡在释放状态的问题
  * 重构 ``bt_audio_codec_cap`` 为扁平数组
  * 重构 ``bt_audio_codec_cfg`` 为扁平数组
  * 移除 ``CONFIG_BT_PACS_{SNK,SRC}_CONTEXT``
  * 从广播汇点中移除扫描和 PA 同步
  * 将 ``bt_codec`` 重命名为 ``bt_audio_codec_{cap, conf, data}``
  * 重命名编解码器 QoS 帧
  * 用 ``BT_HCI_CODING_FORMAT_LC3`` 替换 ``BT_AUDIO_CODEC_LC3_ID``
  * 用 errno 值替换 ``BT_AUDIO_CODEC_PARSE_ERR_`` 值。
  * 重新设计 PACS 通知系统
  * 基于 BAP QOS 更新 ASCS ISO QOS
  * 更新 BAP 以默认过滤 PA 数据重复
  * 更新 CSIP 以立即解锁非绑定设备。
  * 更新 PACS 以在重新连接时通知绑定客户端
  * 更新 ``bt_cap_stream_ops_register`` 以始终注册 BAP 回调
  * 更新 ASCS ACL 断开连接行为
  * 更新以将 ``bt_audio_codec_meta_get`` 拆分为 ``cfg`` 和 ``cap``

* 方向查找

* 主机

  * 新增每连接 SMP 可绑定标志覆盖
  * 新增 USE_NRPA 广播选项
  * 新增 ``BT_CONN_PARAM_ANY``，允许将任意值设置到连接参数
  * 新增高级广播 ISO 参数
  * 新增高级单播 ISO 参数
  * 新增用于管理蓝牙设置存储的新 API
  * 修复 HCI ISO 数据包分片
  * 修复发送到控制器的 HCI ISO SDU 长度
  * 修复 OTS ``bt_ots_init`` 参数结构体命名
  * 修复过程未完成时的 OTS 内存泄漏
  * 修复连接引用泄漏
  * 修复强制配对请求处理
  * 修复主机在启动遗留广播时使可解析私有地址失效
  * 修复 ``bt_iso_cig_reconfigure`` 的问题
  * 修复 ``bt_conn_le_start_encryption`` 中可能的缓冲区溢出
  * 修复某些 SMP 问题
  * 修复在连接断开时中止配对
  * 更新 L2CAP 接受回调
  * 更新 LE L2CAP 连接回调，使其位于连接响应之后
  * 更新 PAwR 实现，在 BT_PRIVACY=y 时使用 RPA 作为响应器地址

* Mesh

  * 新增 TF-M 支持。
  * 新增支持，可同时使用基于 tinycrypt 和基于 PSA 的加密
  * 新增对完整虚拟地址的支持，包含冲突解决。
    引入 :kconfig:option:`CONFIG_BT_MESH_LABEL_NO_RECOVER` Kconfig 选项，
    用于恢复订阅列表和模型发布的地址。
  * 新增统计模块。
  * 修复问题：作为 LPN 的节点在通过回环接口发送分段消息时
    触发 Friend Poll 消息。
  * 修复问题：当配置器使用相同的公共密钥时，
    节点上配置成功完成。
  * 修复问题：从系统工作队列以外的协作线程调用的
    :c:func:`settings_load` 函数导致 GATT Mesh Proxy 服务注册失败。
  * 修复问题：如果带有当前 IV Index 且 IV Update 标志设置为 1 的旧 SNB
    被重新发送，节点可能进入 IV Update in Progress 状态。

  * Mesh 协议 v1.1 变更

    * 新增持久化存储私有 GATT Proxy 状态。
    * 在固件分发服务器模型中新增对固件分发上传 OOB 启动消息的支持。
      该消息支持可以通过
      :kconfig:option:`CONFIG_BT_MESH_DFD_SRV_OOB_UPLOAD` Kconfig 选项启用。
    * 在配置中使用 OOB 方法时新增扩展配置协议超时。
    * 新增对 Composition Data 页 2、129 和 130 的支持。
    * 新增 Composition Data 页 0、1、2、128、129 和 130 的文档。
    * 新增传输层中分片和重组的文档。
    * 新增 SAR 配置模型的文档
    * 修复问题：操作码聚合器服务器模型在没有操作码聚合器客户端模型时
      无法编译。
    * 修复问题：私有 GATT Proxy 广播中使用身份地址
      而不是不可解析私有地址。
    * 修复 Proxy 隐私参数支持。
    * 修复问题：已实例化远程配置服务器模型的节点上
      不存在 Composition Data 页 128。
    * 修复问题：大型 Composition Data 服务器模型
      不支持除 0 之外的 Composition Data 页。
    * 修复问题：与远程配置服务器模型一起在节点上实例化的
      远程配置客户端模型无法重新配置自身。
    * 修复问题：分片和重组中的确认定时器在传入的段确认消息
      不包含至少一个新标记为已确认的段时未重新启动。
    * 修复问题：按需私有 Proxy 服务器和客户端模型之间存在
      相互依赖，导致无法分别编译。

* 控制器

  改进控制器中广播和连接 Isochronous 通道的支持，
  使 LE 音频应用开发成为可能。控制器是实验性的，
  缺少 Isochronous 通道底层链路层中交错打包的实现。

  * 新增 Adv PDU 最小大小检查
  * 新增忽略 Tx HCI ISO 数据包序列号的 Kconfig 选项
  * 新增避免 ISO SDU 分片的 Kconfig
  * 新增用于最大化 BIG 事件长度并抢占 PTO & CTRL 子事件的 Kconfig
  * 新增 ``BT_CTLR_EVENT_OVERHEAD_RESERVE_MAX`` Kconfig
  * 为 ticker 事务新增内存屏障
  * 新增缺失的 nRF53x Tx 功率 Kconfig
  * 新增对连接 ISO 中 Flush 超时的支持
  * 修复 BIS 负载滑动窗口越界检查
  * 修复 CIS 中央 FT 计算
  * 修复 CIS 中央错误处理
  * 修复 CIS 非对称 PHY 使用
  * 修复启用 DF 支持时的 CIS 加密
  * 修复用于质量测试和时间戳的 ISO-AL
  * 修复 HCI LE CIS Established 事件中的 PHY 值
  * 修复 ULL 在罕见条件下卡在信号量的问题
  * 修复由于 PER CIS 活动集过晚导致的断言
  * 修复导致断言的编译器指令重排序
  * 修复连接 ISO 动态 tx 功率
  * 修复失败的广播一致性测试
  * 修复在 Coded PHY 不受支持时接收辅助 PDU 的处理
  * 修复重新调度 ticker 节点时已调度 ticker 节点中的泄漏
  * 修复缺失的主机特性重置
  * 修复 nRF53 SoC 背靠背 PDU 链接
  * 修复 nRF53 SoC 背靠背 Tx Rx 实现
  * 修复 Adv PDU 溢出计算中的回归
  * 修复观察者中导致断言和调度停滞的回归
  * 修复 nRF SoC 上预编程 PPI 的使用
  * 在准备 FT 支持时移除具有无效状态的 HCI ISO 数据
  * 更新扩展广播报告，在未收到 ``AUX_ADV_IND`` 时不生成
  * 更新以在每个状态/角色 LLL 中拥有 ``EVENT_OVERHEAD_START_US`` 冗长断言
  * 更新以在扩展扫描期间达到 ``DATA_LEN_MAX`` 时停止跟随 ``aux_ptr``

板级和 SoC 支持
********************

* 新增对这些 SoC 系列的支持：

  * Nuvoton NuMaker M46x 系列
  * 新增对 STM32F072X8 SoC 变体的支持
  * 新增对 STM32L051X6 SoC 变体的支持
  * 新增对 STM32L451XX SoC 变体的支持
  * 新增对 STM32L4Q5XX SoC 变体的支持
  * 新增对 STM32WBA SoC 系列的支持

* 移除对这些 SoC 系列的支持：

* 对其他 SoC 系列进行以下更改：

  * i.MX RT SoC 不再默认启用 CONFIG_DEVICE_CONFIGURATION_DATA。
    使用外部 SDRAM 的板级应设置 CONFIG_DEVICE_CONFIGURATION_DATA
    和 CONFIG_NXP_IMX_EXTERNAL_SDRAM 为启用。
  * i.MX RT SoC 不再支持 CONFIG_OCRAM_NOCACHE，
    因为此功能可以使用设备树内存区域实现
  * 重构 ESP32 SoC 文件夹。因此现在是适当的 SoC 系列。
  * RP2040：更改为在初始化时重置 I2C 设备

* 新增对这些 ARC 板级的支持：

  * 新增对 nsim_vpx5 - 仿真（nSIM）平台的支持，
    具有 ARCv2 VPX5 核心，接近 vpx5_integer_full 模板
  * 新增对 nsim_hs5x_smp_12cores - 仿真（nSIM）平台的支持，
    具有 12 核 SMP 32 位 ARCv3 HS
  * 新增对 nsim_hs6x_smp_12cores - 仿真（nSIM）平台的支持，
    具有 12 核 SMP 64 位 ARCv3 HS

* 新增对这些 ARM 板级的支持：

  * Nuvoton NuMaker 平台 M467
  * ST Nucleo U5A5ZJ Q
  * ST Nucleo WBA52CG

* 新增对这些 ARM64 板级的支持：

* 新增对这些 RISC-V 板级的支持：

* 新增对这些 X86 板级的支持：

* 新增对这些 Xtensa 板级的支持：

  * 新增 ``esp32_devkitc_wroom`` 和 ``esp32_devkitc_wrover``。

  * 新增 ``esp32s3_luatos_core``。

  * 新增 ``m5stack_core2``。

  * 新增 ``qemu_xtensa_mmu``，利用 Diamond DC233c SoC
    支持测试 Xtensa MMU。

  * 新增 ``xiao_esp32s3``。

  * 新增 ``yd_esp32``。

* 新增对这些 POSIX 板级的支持：

  * :zephyr:board:`native_sim(_64) <native_sim>`
  * nrf5340bsim_nrf5340_cpu(net|app)。仿真的 nrf5340 SoC，
    其无线电流量使用 Babblesim。

* 对这些 ARC 板级进行以下更改：

  * 为 hsdk4xd 平台关闭不支持的栈检查选项
  * 将 ARC QEMU 平台的供应商前缀从 "qemu" 更改为 "snps"

* 对这些 ARM 板级进行以下更改：

  * 在 ST nucleo 板级上新增 ST morpho 连接器描述。

  * rpi_pico：

    * 使用 openocd 调试时的默认适配器已更改为 cmsis-dap。

* 对这些 ARM64 板级进行以下更改：

* 对这些 RISC-V 板级进行以下更改：

* 对这些 X86 板级进行以下更改：

* 对这些 Xtensa 板级进行以下更改：

  * esp32s3_devkitm：

    * 新增 USB-CDC 支持。

    * 新增 CAN 支持。

* 对这些 POSIX 板级进行以下更改：

  * nrf52_bsim：

    * 已重新设计以使用原生仿真器作为其运行器。
    * 多个硬件模型改进和修复。新增 GPIO & GPIOTE 外设。

* 移除对这些 ARC 板级的支持：

* 移除对这些 ARM 板级的支持：

* 移除对这些 ARM64 板级的支持：

* 移除对这些 RISC-V 板级的支持：

* 移除对这些 X86 板级的支持：

* 移除对这些 Xtensa 板级的支持：

  * 移除 ``esp32``。改用 ``esp32_devkitc_*``。

* 对其他板级进行以下更改：

* 新增对以下屏蔽板的支持：

  * Adafruit PiCowbell CAN 总线屏蔽板（用于 Pico）
  * Arduino UNO click 屏蔽板
  * G1120B0MIPI MIPI 显示
  * MikroElektronika MCP2518FD Click 屏蔽板（CAN-FD）
  * RK055HDMIPI4M MIPI 显示
  * RK055HDMIPI4MA0 MIPI 显示
  * Semtech SX1276MB1MAS LoRa 屏蔽板

构建系统和基础设施
*******************************

* SCA（静态代码分析）

  * 新增对 CodeChecker 的支持

* Twister 现在支持测试套件 .yml 文件中的 ``required_snippets``，
  这可以用于在运行测试时包含 snippet（并排除 snippet
  无法应用到的任何板级）。

* 中断

  * 新增对共享中断的支持

* 新增支持，用于在 sysbuild 中设置 MCUboot 加密密钥，
  然后传播到引导加载器和目标映像以自动创建加密更新。

* 构建时优先级检查：默认启用构建时优先级检查。
  如果最终 ELF 文件中的初始化序列与设备树层次结构不匹配，
  这会导致构建失败。可以通过禁用
  :kconfig:option:`CONFIG_CHECK_INIT_PRIORITIES` 选项来关闭它。

* 新增新的 ``initlevels`` 目标，用于打印最终 ELF 文件中的
  最终设备和 :c:macro:`SYS_INIT` 初始化序列。

* 重新设计 syscall 代码生成，使并非所有 marshalling 函数
  都包含在最终二进制中。与禁用子系统关联的 Syscalls
  不再生成其 marshalling 函数。

* 为树内代码子集部分启用关于影子变量的编译器警告。
  树外代码需要在我们能够完全启用影子变量警告之前进行修补。

驱动和传感器
*******************

* ADC

  * 为 STM32F0 HSI14 时钟（专用 ADC 时钟）新增支持
  * 为 STM32 ADC 源时钟和预分频器新增支持。在 STM32F1 和 STM32F3
    系列中，ADC 预分频器可以使用专用 RCC 时钟控制器选项配置。
  * 为所有 STM32 系列（F1 除外）的 ADC 序列器新增支持
  * 修复 STM32F4 ADC 温度和 Vbat 测量。
  * 为 TI ADS1112 新增驱动。
  * 为 TI TLA2021 新增驱动。
  * 为 Gecko ADC 新增驱动。
  * 为 NXP S32 ADC SAR 新增驱动。
  * 为 MAX1125x 系列新增驱动。
  * 为 MAX11102-MAX1117 新增驱动。

* CAN

  * 为具有集成收发器的 TI TCAN4x5x CAN-FD 控制器
    （:dtcompatible:`ti,tcan4x5x`）新增支持。
  * 为 Microchip MCP251xFD CAN-FD 控制器
    （:dtcompatible:`microchip,mcp251xfd`）新增支持。
  * 为 Bosch M_CAN 控制器驱动后端新增 CAN 统计支持。
  * 将 NXP S32 CANXL 驱动切换为使用时钟控制来使用 CAN 时钟，
    而不是在设备树中硬编码 CAN 时钟频率。

* 时钟控制

  * 为 Nuvoton NuMaker M46x 新增支持

* 计数器

  * 新增 :kconfig:option:`CONFIG_COUNTER_RTC_STM32_SUBSECONDS`，
    以启用亚秒作为 STM32 RTC 基于计数器驱动的基本时间 tick。

  * 为 Raspberry Pi Pico 定时器新增支持

* DAC

  * 为 Analog Devices AD56xx 新增支持
  * 为 NXP lpcxpresso55s36（LPDAC）新增支持

* 磁盘

  * Ramdisk 驱动现在使用设备树配置，
    并支持多个实例

* 显示

  * 为 ST7735S（在 ST7735R 驱动中）新增支持

* DMA

  * 为 NXP S32K 新增对 eDMA 驱动的支持
  * 为 NXP SMARTDMA 新增支持
  * 为显示加速新增对 NXP Pixel Pipeline（PXP）的支持
  * 为 SAM XDMAC 驱动新增 DMA get_status() 支持
  * 修复 Intel HDA 驱动中 L1 进入/退出、显式 SCS（采样容器）设置
  * 修复 STM32U5 以启用错误中断，修复块大小和数据大小配置
  * 改进 NXP LPC 驱动中用于调整静态内存使用的 Kconfig 选项

* EEPROM

  * 为 Fujitsu MB85RCxx 系列 I2C FRAM（:dtcompatible:`fujitsu,mb85rcxx`）新增支持。

* 熵

  * 新增要求，``entropy_get_entropy()`` 必须线程安全，
    因为随机子系统需要。

* 以太网

  * 新增 :kconfig:option:`CONFIG_ETH_NATIVE_POSIX_RX_TIMEOUT`，
    用于设置 native posix 的 rx 超时。
  * 为 adin2111 新增支持。
  * 为 NXP S32 GMAC 新增支持。
  * 为 eth_smsc91x 中的混杂模式新增支持。
  * 为 STM32H5X SOC 系列新增支持。
  * 为 MDIO 第 45 条 API 新增支持。
  * 为 YD-ESP32 板级以太网新增支持。
  * 修复 stm32，通过以设备 ID 作为 MAC 的基础来生成更唯一的 MAC 地址。
  * 修复 mcux，将 PTP 时间戳精度从 20us 提高到 200ns。
  * 修复使用 VLAN 时的以太网最大头大小。
  * 移除 ``mdio`` DT 属性。请在驱动中改用 :c:macro:`DT_INST_BUS()`。
  * 重构 smsc91x 中的设备节点层次结构。
  * 将 phy-dev 属性重命名为 phy-handle，以匹配 Linux
    ethernet-controller 绑定并将其移动到 ethernet.yaml，
    以供其他驱动使用。
  * 更新以太网 PHY，在 DT 绑定中使用 ``reg`` 属性。
  * 更新驱动 DT 绑定，一致地使用 ``ethernet-phy`` 设备树节点名称。
  * 更新 esp32 和 sam-gmac DT，使 phy 通过 phandle 而不是
    子节点指向，这使 phy 设备成为 mdio 的子节点。

* 闪存

  * 引入 npcx 闪存驱动，它支持通过单个 Flash Interface Unit（FIU）
    模块和 Direct Read Access（DRA）模式访问两个或更多 spi nor 闪存，
    以获得更好的性能。
  * 为 Nuvoton NuMaker M46x 嵌入式闪存新增支持
  * STM32 QSPI 驱动现在支持 Jedec SFDP 参数读取。
  * STM32 OSPI 驱动现在支持 IO 管理器的低端口和高端口。

* GPIO

  * 为 Nuvoton NuMaker M46x 新增支持

* I2C

  * STM32 V1 驱动现在支持大事务（超过 256 字节的块）
  * STM32 V2 驱动现在支持 10 位寻址。
  * I2C 设备现在可以在 STM32 上用作从 STOP 模式的唤醒源。
  * 修复 Silicon Labs I2C 目标回调中的长 ISR 执行
  * 在 TWIM 驱动中优雅地处理 nRF52 设备的 DMA 最大大小
  * 为 DesignWare 驱动中的 Intel LPSS DMA 使用新增支持
  * 新增使用 DeviceTree 过滤转储消息以进行调试
  * 为 Silicon Labs Gecko 驱动新增目标模式
  * 新增 Intel SEDI 驱动
  * 新增 Infineon XMC4 驱动
  * 新增 Microchip PolarFire SoC 驱动
  * 为 Apollo4 SoCs 新增 Ambiq 驱动

* I2S

  * 修复 NXP MCUX 驱动中 PCM 数据格式的处理。

* I3C

  * ``i3c_cdns``：

    * 修复在 :kconfig:option:`CONFIG_I3C_USE_IBI` 禁用时的构建错误。

    * 修复控制器忙时的传输问题。现在在继续另一个传输之前
      等待控制器空闲。

* IEEE 802.15.4

  * 在 ieee802154_radio_api 中引入了新的强制方法 attr_get()。
    驱动至少需要实现
    IEEE802154_ATTR_PHY_SUPPORTED_CHANNEL_PAGES 和
    IEEE802154_ATTR_PHY_SUPPORTED_CHANNEL_RANGES。
  * 移除了硬件能力 IEEE802154_HW_2_4_GHZ 和 IEEE802154_HW_SUB_GHZ，
    因为它们与标准不一致，并且一些已存在的驱动无法正确表达其通道页
    和通道范围（特别是 SUN FSK 和 HRP UWB 驱动）。这些能力被
    符合标准的新驱动属性 IEEE802154_ATTR_PHY_SUPPORTED_CHANNEL_PAGES
    替换，它适合所有树内驱动。
  * 从 ieee802154_radio_api 中移除了方法 get_subg_channel_count()。
    此方法无法正确表达已存在驱动的通道范围（特别是 SUN FSK
    驱动实现通道页 > 0 并且可能没有零基通道范围，或无法被表示的
    UWB 驱动）。此方法被新驱动属性
    IEEE802154_ATTR_PHY_SUPPORTED_CHANNEL_RANGES 替换，
    它适合所有树内驱动。

* 中断控制器

  * GIC：架构版本选择现在基于设备树

* 输入

  * 新驱动：:dtcompatible:`gpio-qdec`、:dtcompatible:`st,stmpe811`。

  * 从 Kscan 转换为 Input 的驱动：:dtcompatible:`goodix,gt911`
    :dtcompatible:`xptek,xpt2046` :dtcompatible:`hynitron,cst816s`
    :dtcompatible:`microchip,cap1203`。

  * 为转储所有事件到控制台新增 Kconfig 选项
    :kconfig:option:`CONFIG_INPUT_EVENT_DUMP` 和新 shell 命令
    :kconfig:option:`CONFIG_INPUT_SHELL`。

  * 将 ``zephyr,gpio-keys`` 合并到 :dtcompatible:`gpio-keys`，
    并为所有树内板级 ``gpio-keys`` 节点添加 ``zephyr,code`` 代码。

  * 将回调定义宏从 ``INPUT_LISTENER_CB_DEFINE``
    重命名为 :c:macro:`INPUT_CALLBACK_DEFINE`。

* PCIE

  * 在 shell 中新增支持以显示 PCIe 能力。

  * 新增虚拟通道支持。

  * 新增 kconfig :kconfig:option:`CONFIG_PCIE_INIT_PRIORITY`，
    用于指定主机控制器的初始化优先级。

  * 新增支持，用于从 ACPI PCI 路由表（PRT）获取 IRQ。

* ACPI

  * 采用 ACPICA 库作为新模块，以进一步增强 ACPI 支持。

* 引脚控制

  * 为 Nuvoton NuMaker M46x 新增支持

* PWM

  * 为 STM32 PWM 驱动新增 4 通道捕获。
  * 为 Intel Blinky PWM 新增驱动。
  * 为 MAX31790 新增驱动。
  * 为 Infineon XMC4XXX CCU4 新增驱动。
  * 为 Infineon XMC4XXX CCU8 新增驱动。
  * 新增 MCUX CTimer 基于 PWM 驱动。
  * 新增基于 TI CC13xx/CC26xx GPT 定时器的 PWM 驱动。
  * 重构 pwm_nrf5_sw 驱动，使其也可以在 nRF53 和
    nRF91 系列上使用。因此，驱动被重命名为 pwm_nrf_sw。
  * 为 Nuvoton NuMaker 系列新增驱动。
  * 新增基于 NXP S32 EMIOS 外设的 PWM 驱动。

* 调节器

  * 为 GPIO 控制的电压调节器新增支持

  * 为 AXP192 PMIC 新增支持

  * 为 NXP VREF 调节器新增支持

  * 修复：调节器现在可以指定其工作电压

  * nPM1300 现在支持 PFM 模式

  * 新增用于配置 "ship" 模式的新 API

  * 调节器 shell 允许配置 DVS 模式

* 重置

  * 为 Nuvoton NuMaker M46x 新增支持

* 保留内存

  * 新增支持，允许使用
    :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE`
    强制禁用互斥锁支持。

  * 修复用户模式支持不起作用的问题。

* RTC

  * 为 STM32 RTC API 驱动新增支持。此驱动与
    COUNTER API 的 RTC 基于实现的使用不兼容。

* SDHC

  * 为 Alder lake 平台上存在的 EMMC 主机控制器新增驱动
  * 为 SAM4E MCU 系列上存在的 Atmel HSMCI 控制器新增驱动

* 传感器

  * 重构 :dtcompatible:`ti,bq274xx` 以添加 ``BQ27427`` 支持，
    修复容量和功率通道的单位。
  * 新增 ADC 电流感测放大器和电压传感器驱动。
  * 新增 ADI LTC2990 电压、电流和温度传感器驱动。
  * 新增 AMS TSL2540 环境光传感器驱动。
  * 新增 Bosch BMI08x 加速度计/陀螺仪驱动。
  * 新增 DFRobot A01NYUB 距离传感器驱动。
  * 新增 Fintek F75303 温度传感器驱动。
  * 新增 Isentek IST8310 磁力计驱动。
  * 新增 Microchip TCN75A 温度传感器驱动。
  * 新增 NXP TEMPMON 驱动。
  * 新增 Seeed HM330X 灰尘传感器驱动。
  * 新增 TI TMAG5170 3D 霍尔传感器驱动。
  * 为 BMM150、LM75 和 Microchip 转速计驱动新增电源管理支持。
  * 为 BMM150 磁力计驱动新增触发支持。
  * 为 LIS2DH 加速度计驱动新增敲击触发支持。
  * 更新 ST 传感器驱动以使用 STMEMSC HAL i/f v2.3
  * 更新解码器 API 以垂直解码原始传感器数据。
  * NTC 热敏电阻和 INA23x 驱动中的各种修复和增强。

* 串行

  * 为 Nuvoton NuMaker M46x 新增支持

  * NS16550：重新设计设备初始化宏的方式。

    * ``CONFIG_UART_NS16550_ACCESS_IOPORT`` 和 ``CONFIG_UART_NS16550_SIMULT_ACCESS``
      被移除。对于使用 IO 端口访问的 UART，
      在设备树节点中添加 ``io-mapped`` 属性。

  * 为 ESP32S3 新增异步支持。

  * 为 ``native_posix`` 下的串行 TTY 新增支持。

  * 为 Efinix Sapphire SoCs 上的 UART 新增支持。

  * 新增 Intel SEDI UART 驱动。

  * 为 BCM2711 上的 UART 新增支持。

  * ``uart_stm32``：

    * 新增 RS485 支持。

    * 新增宽数据支持。

  * ``uart_pl011``：为 Ambiq SoCs 新增支持。

  * ``serial_test``：为中断和异步 API 新增支持。

  * ``uart_emul``：为中断 API 新增支持。

  * ``uart_rpi_pico``：修复 Modbus DE-RE 信号处理

* SPI

  * 移除由 Flash Interface Unit（FIU）模块实现的 npcx spi 驱动。
  * 为 Raspberry Pi Pico PIO 基于 SPI 新增支持。

* 定时器

  * TI CC13xx/26xx 系统时钟定时器 compatible 从
    :dtcompatible:`ti,cc13xx-cc26xx-rtc` 更改为
    :dtcompatible:`ti,cc13xx-cc26xx-rtc-timer`，
    相应的 Kconfig 选项从 :kconfig:option:`CC13X2_CC26X2_RTC_TIMER`
    更改为 :kconfig:option:`CC13XX_CC26XX_RTC_TIMER`，
    以改进一致性和可扩展性。除非修改了内部定时器，
    否则无需采取任何操作。

* USB

  * 为基于 STM32 的 MCU 新增 UDC 驱动，依赖于 HAL/PCD。
    此驱动与 UDC API（实验性）兼容。
  * 为 USB 驱动中的 STM32H5 系列新增支持。

* WiFi

  * 增加 esp32 默认网络（TCP workq、RX 和 mgmt 事件）栈大小到 2048 字节。
  * 减少 Wi-Fi 示例中 esp32s2_saola 的 RAM 使用。
  * 修复 winc1500 中的未定义声明。
  * 修复 eswifi 中的 SPI 缓冲区长度。
  * 修复 AP 模式中 esp32 数据发送和通道选择。
  * 修复 esp_at 驱动初始化和网络接口休眠状态设置。

网络
**********

* CoAP：

  * 优化 CoAP 客户端库，使其内部仅使用单个线程。
  * 将 CoAP 客户端库转换为内部使用 ``zsock_*`` API。
  * 修复 CoAP 客户端库中的一个 bug，
    该 bug 导致重传超时计算不正确。
  * 使用 64 位定时器值来计算传输超时。这修复了潜在问题：
    对于持续运行超过 49 天的设备，32 位正常运行时间计数器可能回绕，
    导致 CoAP 数据包在此事件时根本不超时。
  * API 文档改进。
  * 新增 API 函数：

    * :c:func:`coap_has_descriptive_block_option`
    * :c:func:`coap_remove_descriptive_block_option`
    * :c:func:`coap_packet_remove_option`
    * :c:func:`coap_packet_set_path`

* 连接管理器：

  * 新增对自动连接和自动断开行为的支持
    （由 :c:enum:`CONN_MGR_IF_NO_AUTO_CONNECT` 和
    :c:enum:`CONN_MGR_IF_NO_AUTO_DOWN` 标志控制）。
  * 将连接管理器 API 拆分到独立的头文件中。
  * 扩展连接管理器文档以涵盖新功能。

* DHCP：

  * 新增对 DHCPv4 单播回复处理的支持。
  * 新增对 DHCPv6 协议的支持。

* 以太网：

  * 修复 ARP 排队，使排队的网络数据包立即发送，
    而不是在核心网络栈中第二次排队。

* gPTP：

  * 新增对检测使用默认多播目标地址的 gPTP 数据包的支持。
  * 修复 Announce 和 Follow Up 消息处理。

* ICMP：

  * 修复 ICMPv6 错误消息类型检查。
  * 重新设计 ICMP 回调注册和处理，
    允许为同一 ICMP 消息注册多个处理程序。
  * 引入用于发送 ICMP Echo Request（ping）的 API。
  * 新增支持以注册 offloaded ICMP ping 处理程序。
  * 新增支持以设置 ping 的数据包优先级。

* IPv6：

  * 确保在移除 IPv6 地址时取消正在进行的 DAD 过程。
  * 修复一个 bug：Solicited-Node 多播地址
    可能仍在使用时被移除。

* LwM2M：

  * 新增对无滴答模式的支持。这从套接字循环中移除了 500 ms 超时，
    因此引擎不会持续唤醒 CPU。可以通过
    :kconfig:option:`CONFIG_LWM2M_TICKLESS` 启用。
  * 新增 :c:macro:`LWM2M_RD_CLIENT_EVENT_DEREGISTER` 事件。
  * 分块发送现在也支持 LwM2M 读取和组合读取操作。
    当 :kconfig:option:`CONFIG_LWM2M_COAP_BLOCK_TRANSFER` 启用时，
    任何大于 :kconfig:option:`CONFIG_LWM2M_COAP_MAX_MSG_SIZE` 的内容
    都会被拆分为分块传输。
  * 分块传输不再需要 token 匹配，
    因为这不符合 CoAP 规范（CoAP 不要求 token 重用）。
  * 对 bootstrap 的各种修复。现在客户端确保在关闭 DTLS 管道之前
    发送 Bootstrap-Finish 命令。也允许 Bootstrap 服务器关闭 DTLS 管道。
    在等待 bootstrap 命令时新增超时。
  * 新增对 X509 证书的支持。
  * 对字符串处理的各种修复。允许将字符串设置为零长度。
    在对不透明资源使用字符串操作时确保字符串终止。
  * 新增对 Connection Monitoring 对象版本 1.3 的支持。
  * 新增对 Security 对象的保护，防止服务器进行读/写。
  * 修复在观察 token 变更时可能的通知停滞。
  * 新增 shell 命令 ``lwm2m create``，
    允许创建 LwM2M 对象实例。
  * 新增针对 Leshan 服务器的 LwM2M 互操作性测试套件。
  * API 文档改进。
  * 其他若干小修复和改进。

* 其他：

  * 网络子系统、PTP 和 IEEE 802.15.4 中的时间和时间戳
    被更精确地指定，并相应更新了所有树内调用点。
    定时 TX 和 TX/RX 时间戳的字段已合并。
    参见 :c:type:`net_time_t`、:c:struct:`net_ptp_time`、
    :c:struct:`ieee802154_config`、:c:struct:`ieee802154_radio_api`
    和 :c:struct:`net_pkt` 以获取详细文档。
    由于这主要是内部 API，现有应用很可能在不修改的情况下继续工作。
  * 新增对额外 net_pkt 过滤钩子的支持：

    * :kconfig:option:`CONFIG_NET_PKT_FILTER_IPV4_HOOK`
    * :kconfig:option:`CONFIG_NET_PKT_FILTER_IPV6_HOOK`
    * :kconfig:option:`CONFIG_NET_PKT_FILTER_LOCAL_IN_HOOK`

  * 重新设计多个网络组件以使用 timepoint API。
  * 新增 API 函数，便于遍历接口上注册的所有 IPv4/IPv6
    （:c:func:`net_if_ipv4_addr_foreach`、:c:func:`net_if_ipv6_addr_foreach`）。
  * ``NET_EVENT_IPV6_PREFIX_ADD`` 和 ``NET_EVENT_IPV6_PREFIX_DEL`` 事件
    现在提供关于前缀的更详细信息
    （:c:struct:`net_event_ipv6_prefix`）。
  * 对网络子系统中被遮蔽变量的整体清理。
  * 新增 ``qemu_cortex_a53`` 网络支持。
  * 引入新的调制解调器子系统。
  * 新增 :zephyr:code-sample:`cellular-modem` 示例。
  * 新增对网络接口名称的支持（而不是重用底层设备名称）。
  * 由于服务退役，移除对 Google Cloud IoT 示例的支持。
  * 修复一个 bug：在混杂模式下传入的数据包
    在某些情况下可能已被 L2 修改。
  * 新增支持以在运行时设置 syslog 服务器（用于网络日志后端）
    的 IP 地址。
  * 移除不再使用的 ``queued`` 和 ``sent`` net_pkt 标志。
  * 新增支持以将 zperf TCP/UDP 服务器绑定到特定 IP 地址。

* MQTT-SN：

  * 改进内部缓冲区分配的线程安全性。
  * API 文档改进。

* OpenThread：

  * 重新设计 :c:func:`otPlatEntropyGet`，
    使其内部使用 :c:func:`sys_csrand_get`。
  * 引入 ``ieee802154_radio_openthread.h`` 无线电驱动扩展接口，
    专用于 OpenThread。新增 OpenThread 特有的发送模式
    :c:enum:`IEEE802154_OPENTHREAD_TX_MODE_TXTIME_MULTIPLE_CCA`。

* PPP：

  * 修复 PPP L2 对网络接口载波状态的使用。
  * 使 PPP L2 线程优先级可配置
    （:kconfig:option:`CONFIG_NET_L2_PPP_THREAD_PRIO`）。
  * 将 PPP L2 移出实验阶段。
  * 在载波断开时防止 PPP 连接重新建立。

* 套接字：

  * 新增对静态分配 socketpair 的支持（在没有堆的情况下）。
  * 使发送超时可配置
    （:kconfig:option:`CONFIG_NET_SOCKET_MAX_SEND_WAIT`）。
  * 新增对 ``FIONREAD`` 和 ``FIONBIO`` :c:func:`ioctl` 命令的支持。
  * 修复已连接数据报套接字的输入过滤。
  * 修复未连接套接字上的 :c:func:`getsockname` 操作。
  * 新增用于 DTLS Connection ID 支持的新安全套接字选项：

    * :c:macro:`TLS_DTLS_CID`
    * :c:macro:`TLS_DTLS_CID_VALUE`
    * :c:macro:`TLS_DTLS_PEER_CID_VALUE`
    * :c:macro:`TLS_DTLS_CID_STATUS`

  * 新增对 :c:macro:`SO_REUSEADDR` 和 :c:macro:`SO_REUSEPORT` 套接字选项的支持。

* TCP：

  * 修复数据重传中潜在的停滞（当数据仅被部分确认时）。
  * 使 TCP 工作队列优先级可配置
    （:kconfig:option:`CONFIG_NET_TCP_WORKER_PRIO`）。
  * 新增对 TCP 新 Reno 碰撞避免算法的支持。
  * 修复已绑定套接字上的源地址选择。
  * 修复在活动期间握手时关闭监听套接字时可能的内存泄漏。
  * 修复握手中 RST 数据包的处理。
  * 重构负责连接拆除的代码，以修复发现的 bug
    并简化未来维护。

* TFTP：

  * 新增 :zephyr:code-sample:`tftp-client` 示例。
  * API 文档改进。

* WebSocket

  * WebSocket 库不再在断开连接时自动关闭底层 TCP 套接字。
    这与连接行为一致，其中 WebSocket 库期望一个已连接的 TCP 套接字。

* Wi-Fi：

  * 新增被动扫描支持。
  * Wi-Fi 扫描 API 已更新，加入 Wi-Fi 扫描参数以允许选择扫描模式。
  * 更新 TWT 处理。
  * 新增对通用网络管理器 API 的支持。
  * 新增对 Wi-Fi 模式设置和选择的支持。
  * 为 Wi-Fi shell 中的 SSID 和 PSK 新增用户输入验证。
  * 新增扫描扩展，用于指定通道、限制扫描结果、过滤 SSID、
    设置主动和被动通道驻留时间以及频段。

USB
***

* USB 设备 HID
  * Kconfig 选项 USB_HID_PROTOCOL_CODE 在 v2.6 中被弃用，现已最终移除。

设备树
**********

API
===

新的通用宏：

- :c:macro:`DT_REG_ADDR_U64`
- :c:macro:`DT_REG_ADDR_BY_NAME_U64`
- :c:macro:`DT_INST_REG_ADDR_BY_NAME_U64`
- :c:macro:`DT_INST_REG_ADDR_U64`
- :c:macro:`DT_FOREACH_STATUS_OKAY_NODE_VARGS`
- :c:macro:`DT_FOREACH_NODE_VARGS`
- :c:macro:`DT_HAS_COMPAT_ON_BUS_STATUS_OKAY`

为依赖序号引入的新专用宏：

- :c:macro:`DT_DEP_ORD_STR_SORTABLE`

为固定闪存分区引入的新通用宏：

- :c:macro:`DT_MEM_FROM_FIXED_PARTITION`
- :c:macro:`DT_FIXED_PARTITION_ADDR`

绑定
========

* 通用或厂商无关：

  * 新绑定：

    * :dtcompatible:`current-sense-amplifier`
    * :dtcompatible:`current-sense-shunt`
    * :dtcompatible:`gpio-qdec`
    * :dtcompatible:`regulator-gpio`
    * :dtcompatible:`usb-audio-feature-volume`

  * 修改的绑定：

    * CAN（控制器局域网）控制器绑定：

          * 属性 ``phase-seg1-data`` 弃用状态从 False 更改为 True
          * 属性 ``phase-seg1`` 弃用状态从 False 更改为 True
          * 属性 ``phase-seg2-data`` 弃用状态从 False 更改为 True
          * 属性 ``phase-seg2`` 弃用状态从 False 更改为 True
          * 属性 ``prop-seg-data`` 弃用状态从 False 更改为 True
          * 属性 ``prop-seg`` 弃用状态从 False 更改为 True
          * 属性 ``sjw-data`` 默认值从 None 更改为 1
          * 属性 ``sjw-data`` 弃用状态从 False 更改为 True
          * 属性 ``sjw`` 默认值从 None 更改为 1
          * 属性 ``sjw`` 弃用状态从 False 更改为 True

    * 以太网控制器绑定：新增 ``phy-handle`` 属性
      （在某些绑定中，这从 ``phy-dev`` 重命名而来），
      匹配 Linux ethernet-controller 绑定。

    * RISC-V CPU 绑定使用的 ``riscv,isa`` 属性
      不再有 ``enum`` 值。

    * :dtcompatible:`neorv32,cpu`：

          * 新属性：``mmu-type``
          * 新属性：``riscv,isa``

    * :dtcompatible:`regulator-fixed`：

          * 新属性：``regulator-min-microvolt``
          * 新属性：``regulator-max-microvolt``
          * 属性 ``enable-gpios`` 不再需要

    * :dtcompatible:`ethernet-phy`：

          * 移除属性：``address``
          * 移除属性：``mdio``
          * 属性 ``reg`` 现在需要

    * :dtcompatible:`usb-audio-hs` 和 :dtcompatible:`usb-audio-hp`：

          * 新属性：``volume-max``
          * 新属性：``volume-min``
          * 新属性：``volume-res``
          * 新属性：``status``
          * 新属性：``compatible``
          * 新属性：``reg``
          * 新属性：``reg-names``
          * 新属性：``interrupts``
          * 新属性：``interrupts-extended``
          * 新属性：``interrupt-names``
          * 新属性：``interrupt-parent``
          * 新属性：``label``
          * 新属性：``clocks``
          * 新属性：``clock-names``
          * 新属性：``#address-cells``
          * 新属性：``#size-cells``
          * 新属性：``dmas``
          * 新属性：``dma-names``
          * 新属性：``io-channels``
          * 新属性：``io-channel-names``
          * 新属性：``mboxes``
          * 新属性：``mbox-names``
          * 新属性：``wakeup-source``
          * 新属性：``power-domain``
          * 新属性：``zephyr,pm-device-runtime-auto``

    * :dtcompatible:`ntc-thermistor-generic`：

          * 移除属性：``r25-ohm``

    * :dtcompatible:`ns16550`：

          * 新属性：``resets``
          * 新属性：``reset-names``

    * :dtcompatible:`fixed-clock`：

          * 移除属性：``clocks``

    * 所有 CPU 绑定都获得了新的 ``enable-method`` 属性。
      `pull request
      60210 <https://github.com/zephyrproject-rtos/zephyr/pull/60210>`_
      以获取详情。

* Analog Devices, Inc. (adi)：

  * 新绑定：

    * :dtcompatible:`adi,ad5628`
    * :dtcompatible:`adi,ad5648`
    * :dtcompatible:`adi,ad5668`
    * :dtcompatible:`adi,ad5672`
    * :dtcompatible:`adi,ad5674`
    * :dtcompatible:`adi,ad5676`
    * :dtcompatible:`adi,ad5679`
    * :dtcompatible:`adi,ad5684`
    * :dtcompatible:`adi,ad5686`
    * :dtcompatible:`adi,ad5687`
    * :dtcompatible:`adi,ad5689`
    * :dtcompatible:`adi,adin1110`
    * :dtcompatible:`adi,adltc2990`

  * 修改的绑定：

    * :dtcompatible:`adi,adin2111-mdio`（在 adin2111 总线上）：

          * 移除属性：``protocol``

* Altera Corp. (altr)：

  * 新绑定：

    * :dtcompatible:`altr,pio-1.0`

* Ambiq Micro, Inc. (ambiq)：

  * 新绑定：

    * :dtcompatible:`ambiq,am1805`
    * :dtcompatible:`ambiq,apollo4-pinctrl`
    * :dtcompatible:`ambiq,counter`
    * :dtcompatible:`ambiq,i2c`
    * :dtcompatible:`ambiq,mspi`
    * :dtcompatible:`ambiq,pwrctrl`
    * :dtcompatible:`ambiq,spi`
    * :dtcompatible:`ambiq,stimer`
    * :dtcompatible:`ambiq,uart`
    * :dtcompatible:`ambiq,watchdog`

* AMS AG (ams)：

  * 新绑定：

    * :dtcompatible:`ams,tsl2540`

* Andes Technology Corporation (andestech)：

  * 新绑定：

    * :dtcompatible:`andestech,atcwdt200`
    * :dtcompatible:`andestech,plic-sw`
    * :dtcompatible:`andestech,qspi-nor`

* ARM Ltd. (arm)：

  * 新绑定：

    * :dtcompatible:`arm,cortex-a76`
    * :dtcompatible:`arm,gic-v1`
    * :dtcompatible:`arm,gic-v2`
    * :dtcompatible:`arm,gic-v3`
    * :dtcompatible:`arm,psci-1.1`

* ASPEED Technology Inc. (aspeed)：

  * 修改的绑定：

    * :dtcompatible:`aspeed,ast10x0-reset`：

          * 空间 "reset" 的说明符 cells 现在命名为：['id']（旧值：None）
          * 空间 "clock" 的说明符 cells 现在命名为：None（旧值：['reset_id']）

* Atmel Corporation (atmel)：

  * 新绑定：

    * :dtcompatible:`atmel,sam-hsmci`

  * 修改的绑定：

    * :dtcompatible:`atmel,sam-mdio`：

          * 移除属性：``protocol``
          * 属性 ``#address-cells`` const 值从 None 更改为 1
          * 属性 ``#size-cells`` const 值从 None 更改为 0
          * 属性 ``#address-cells`` 现在需要
          * 属性 ``#size-cells`` 现在需要

* Bosch Sensortec GmbH (bosch)：

  * 新绑定：

    * :dtcompatible:`bosch,bmi08x-accel`
    * :dtcompatible:`bosch,bmi08x-accel`
    * :dtcompatible:`bosch,bmi08x-gyro`
    * :dtcompatible:`bosch,bmi08x-gyro`

  * 修改的绑定：

    * :dtcompatible:`bosch,bmm150`：

          * 新属性：``drdy-gpios``

    * :dtcompatible:`bosch,bmi270`：

          * 新属性：``irq-gpios``

* Broadcom Corporation (brcm)：

  * 新绑定：

    * :dtcompatible:`brcm,bcm2711-aux-uart`

* Cadence Design Systems Inc. (cdns)：

  * 新绑定：

    * :dtcompatible:`cdns,tensilica-xtensa-lx3`

* DFRobot (dfrobot)：

  * 新绑定：

    * :dtcompatible:`dfrobot,a01nyub`

* Efinix Inc (efinix)：

  * 新绑定：

    * :dtcompatible:`efinix,sapphire-gpio`
    * :dtcompatible:`efinix,sapphire-timer0`
    * :dtcompatible:`efinix,sapphire-uart0`

* EPCOS AG (epcos)：

  * 修改的绑定：

    * :dtcompatible:`epcos,b57861s0103a039`：

          * 移除属性：``r25-ohm``

* Espressif Systems (espressif)：

  * 修改的绑定：

    * :dtcompatible:`espressif,esp-at`（在 uart 总线上）：

          * 新属性：``external-reset``

    * :dtcompatible:`espressif,esp32-mdio`：

          * 移除属性：``protocol``
          * 属性 ``#address-cells`` const 值从 None 更改为 1
          * 属性 ``#size-cells`` const 值从 None 更改为 0
          * 属性 ``#address-cells`` 现在需要
          * 属性 ``#size-cells`` 现在需要

    * :dtcompatible:`espressif,riscv`：

          * 新属性：``mmu-type``
          * 新属性：``riscv,isa``

    * :dtcompatible:`espressif,esp32-spi`：

          * 新属性：``line-idle-low``

* Feature Integration Technology Inc. (fintek)：

  * 新绑定：

    * :dtcompatible:`fintek,f75303`

* FocalTech Systems Co.,Ltd (focaltech)：

  * 修改的绑定：

    * :dtcompatible:`focaltech,ft5336`（在 i2c 总线上）：

          * 新属性：``reset-gpios``

* Fujitsu Ltd. (fujitsu)：

  * 新绑定：

    * :dtcompatible:`fujitsu,mb85rcxx`

* Shenzhen Huiding Technology Co., Ltd. (goodix)：

  * 修改的绑定：

    * :dtcompatible:`goodix,gt911`（在 i2c 总线上）：

          * 总线列表从 ['kscan'] 更改为 []
          * 新属性：``alt-addr``

* Himax Technologies, Inc. (himax)：

  * 新绑定：

    * :dtcompatible:`himax,hx8394`

* Infineon Technologies (infineon)：

  * 新绑定：

    * :dtcompatible:`infineon,cat1-counter`
    * :dtcompatible:`infineon,cat1-spi`
    * :dtcompatible:`infineon,xmc4xxx-ccu4-pwm`
    * :dtcompatible:`infineon,xmc4xxx-ccu8-pwm`
    * :dtcompatible:`infineon,xmc4xxx-i2c`

* Intel Corporation (intel)：

  * 新绑定：

    * :dtcompatible:`intel,agilex5-clock`
    * :dtcompatible:`intel,alder-lake`
    * :dtcompatible:`intel,apollo-lake`
    * :dtcompatible:`intel,blinky-pwm`
    * :dtcompatible:`intel,elkhart-lake`
    * :dtcompatible:`intel,emmc-host`
    * :dtcompatible:`intel,ish`
    * :dtcompatible:`intel,loapic`
    * :dtcompatible:`intel,sedi-gpio`
    * :dtcompatible:`intel,sedi-i2c`
    * :dtcompatible:`intel,sedi-ipm`
    * :dtcompatible:`intel,sedi-uart`
    * :dtcompatible:`intel,socfpga-agilex-sip-smc`
    * :dtcompatible:`intel,socfpga-reset`
    * :dtcompatible:`intel,timeaware-gpio`

  * 移除的绑定：

    * ``intel,agilex-socfpga-sip-smc``
    * ``intel,apollo_lake``
    * ``intel,elkhart_lake``
    * ``intel,gna``

  * 修改的绑定：

    * :dtcompatible:`intel,niosv`：

          * 新属性：``mmu-type``
          * 新属性：``riscv,isa``

    * :dtcompatible:`intel,adsp-imr`：

          * 新属性：``zephyr,memory-attr``
          * 属性 ``zephyr,memory-region-mpu`` enum 值从 ['RAM', 'RAM_NOCACHE', 'FLASH', 'PPB', 'IO', 'EXTMEM'] 更改为 None
          * 属性 ``zephyr,memory-region-mpu`` 弃用状态从 False 更改为 True

    * :dtcompatible:`intel,lpss`：

          * 新属性：``dma-parent``

    * :dtcompatible:`intel,adsp-shim-clkctl`：

          * 新属性：``adsp-clkctl-clk-ipll``

* Isentek Inc. (isentek)：

  * 新绑定：

    * :dtcompatible:`isentek,ist8310`

* Integrated Silicon Solutions Inc. (issi)：

  * 新绑定：

    * :dtcompatible:`issi,is31fl3216a`
    * :dtcompatible:`issi,is31fl3733`

* ITE Tech. Inc. (ite)：

  * 新绑定：

    * :dtcompatible:`ite,it8xxx2-sha`

  * 修改的绑定：

    * :dtcompatible:`ite,it8xxx2-pinctrl-func`：

          * 新属性：``func3-ext``
          * 新属性：``func3-ext-mask``

    * :dtcompatible:`ite,riscv-ite`：

          * 新属性：``mmu-type``
          * 新属性：``riscv,isa``

    * :dtcompatible:`ite,enhance-i2c`：

          * 新属性：``target-enable``
          * 新属性：``target-pio-mode``

* Linaro Limited (linaro)：

  * 新绑定：

    * :dtcompatible:`linaro,ivshmem-ipm`

* Maxim Integrated Products (maxim)：

  * 新绑定：

    * :dtcompatible:`maxim,max11102`
    * :dtcompatible:`maxim,max11103`
    * :dtcompatible:`maxim,max11105`
    * :dtcompatible:`maxim,max11106`
    * :dtcompatible:`maxim,max11110`
    * :dtcompatible:`maxim,max11111`
    * :dtcompatible:`maxim,max11115`
    * :dtcompatible:`maxim,max11116`
    * :dtcompatible:`maxim,max11117`
    * :dtcompatible:`maxim,max11253`
    * :dtcompatible:`maxim,max11254`
    * :dtcompatible:`maxim,max31790`

* Microchip Technology Inc. (microchip)：

  * 新绑定：

    * :dtcompatible:`microchip,mcp251xfd`
    * :dtcompatible:`microchip,mpfs-i2c`
    * :dtcompatible:`microchip,tcn75a`

  * 修改的绑定：

    * :dtcompatible:`microchip,xec-pwmbbled`：

          * 新属性：``enable-low-power-32k``

    * :dtcompatible:`microchip,cap1203`（在 i2c 总线上）：

          * 总线列表从 ['kscan'] 更改为 []
          * 新属性：``input-codes``

    * :dtcompatible:`microchip,xec-ps2`：

          * 新属性：``wakerx-gpios``

* Motorola, Inc. (motorola)：

  * 修改的绑定：

    * :dtcompatible:`motorola,mc146818`：

          * 新属性：``clock-frequency``

* Murata Manufacturing Co., Ltd. (murata)：

  * 新绑定：

    * :dtcompatible:`murata,ncp15wb473`

* Nordic Semiconductor (nordic)：

  * 新绑定：

    * :dtcompatible:`nordic,npm1300-led`
    * :dtcompatible:`nordic,npm1300-wdt`

  * 移除的绑定：

    * ``nordic,nrf-cc310``
    * ``nordic,nrf-cc312``

  * 修改的绑定：

    * :dtcompatible:`nordic,nrf-ccm`：

          * 新属性：``headermask-supported``

    * :dtcompatible:`nordic,nrf-twi`：

          * 新属性：``easydma-maxcnt-bits``

    * :dtcompatible:`nordic,nrf-twim` 和 :dtcompatible:`nordic,nrf-twis`：

          * 新属性：``easydma-maxcnt-bits``
          * 新属性：``memory-regions``
          * 新属性：``memory-region-names``

    * :dtcompatible:`nordic,nrf-spi`、:dtcompatible:`nordic,nrf-spis` 和
      :dtcompatible:`nordic,nrf-spim`：

          * 新属性：``wake-gpios``

    * :dtcompatible:`nordic,npm1300-charger`：

          * 新属性：``thermistor-cold-millidegrees``
          * 新属性：``thermistor-cool-millidegrees``
          * 新属性：``thermistor-warm-millidegrees``
          * 新属性：``thermistor-hot-millidegrees``
          * 新属性：``trickle-microvolt``
          * 新属性：``term-current-percent``
          * 新属性：``vbatlow-charge-enable``
          * 新属性：``disable-recharge``

    * :dtcompatible:`nordic,nrf-uicr`：

          * 新属性：``nfct-pins-as-gpios``
          * 新属性：``gpio-as-nreset``

    * :dtcompatible:`nordic,npm1300`（在 i2c 总线上）：

          * 新属性：``host-int-gpios``
          * 新属性：``pmic-int-pin``

* Nuclei System Technology (nuclei)：

  * 修改的绑定：

    * :dtcompatible:`nuclei,bumblebee`：

          * 新属性：``mmu-type``
          * 新属性：``riscv,isa``

* Nuvoton Technology Corporation (nuvoton)：

  * 新绑定：

    * :dtcompatible:`nuvoton,nct38xx`
    * :dtcompatible:`nuvoton,nct38xx-gpio`
    * :dtcompatible:`nuvoton,npcx-fiu-nor`
    * :dtcompatible:`nuvoton,npcx-fiu-qspi`
    * :dtcompatible:`nuvoton,numaker-fmc`
    * :dtcompatible:`nuvoton,numaker-gpio`
    * :dtcompatible:`nuvoton,numaker-pcc`
    * :dtcompatible:`nuvoton,numaker-pinctrl`
    * :dtcompatible:`nuvoton,numaker-pwm`
    * :dtcompatible:`nuvoton,numaker-rst`
    * :dtcompatible:`nuvoton,numaker-scc`
    * :dtcompatible:`nuvoton,numaker-spi`
    * :dtcompatible:`nuvoton,numaker-uart`

  * 移除的绑定：

    * ``nuvoton,nct38xx-gpio``
    * ``nuvoton,npcx-spi-fiu``

  * 修改的绑定：

    * :dtcompatible:`nuvoton,npcx-sha`：

          * 新属性：``context-buffer-size``

    * :dtcompatible:`nuvoton,npcx-adc`：

          * 新属性：``vref-mv``
          * 移除属性：``threshold-reg-offset``

    * :dtcompatible:`nuvoton,adc-cmp`：

          * 新属性：``thr-sel``

    * :dtcompatible:`nuvoton,npcx-pcc`：

          * 新属性：``pwdwn-ctl-val``
          * 属性 ``clock-frequency`` enum 值从 [100000000, 96000000, 90000000, 80000000, 66000000, 50000000, 48000000, 40000000, 33000000] 更改为 [120000000, 100000000, 96000000, 90000000, 80000000, 66000000, 50000000, 48000000]
          * 属性 ``ram-pd-depth`` enum 值从 [12, 15] 更改为 [8, 12, 15]

* NXP Semiconductors (nxp)：

  * 新绑定：

    * :dtcompatible:`nxp,ctimer-pwm`
    * :dtcompatible:`nxp,fs26-wdog`
    * :dtcompatible:`nxp,imx-flexspi-w956a8mbya`
    * :dtcompatible:`nxp,irqsteer-intc`
    * :dtcompatible:`nxp,lpdac`
    * :dtcompatible:`nxp,mbox-imx-mu`
    * :dtcompatible:`nxp,mcux-dcp`
    * :dtcompatible:`nxp,mcux-edma-v3`
    * :dtcompatible:`nxp,pcf8563`
    * :dtcompatible:`nxp,pxp`
    * :dtcompatible:`nxp,s32-adc-sar`
    * :dtcompatible:`nxp,s32-clock`
    * :dtcompatible:`nxp,s32-emios`
    * :dtcompatible:`nxp,s32-emios-pwm`
    * :dtcompatible:`nxp,s32-gmac`
    * :dtcompatible:`nxp,s32-qspi`
    * :dtcompatible:`nxp,s32-qspi-device`
    * :dtcompatible:`nxp,s32-qspi-nor`
    * :dtcompatible:`nxp,s32k3-pinctrl`
    * :dtcompatible:`nxp,smartdma`
    * :dtcompatible:`nxp,tempmon`
    * :dtcompatible:`nxp,vref`

  * 修改的绑定：

    * :dtcompatible:`nxp,s32-netc-emdio`：

          * 移除属性：``protocol``
          * 属性 ``#address-cells`` const 值从 None 更改为 1
          * 属性 ``#size-cells`` const 值从 None 更改为 0
          * 属性 ``#address-cells`` 现在需要
          * 属性 ``#size-cells`` 现在需要

    * :dtcompatible:`nxp,mipi-dsi-2l`：

          * 属性 ``nxp,lcdif`` 不再需要

    * :dtcompatible:`nxp,imx-mipi-dsi`：

          * 属性 ``nxp,lcdif`` 不再需要

    * :dtcompatible:`nxp,pca9633`（在 i2c 总线上）：

          * 新属性：``disable-allcall``

    * :dtcompatible:`nxp,s32-sys-timer`：

          * 移除属性：``clock-frequency``
          * 属性 ``clocks`` 现在需要

    * :dtcompatible:`nxp,imx-lpspi`：

          * 新属性：``data-pin-config``

    * :dtcompatible:`nxp,s32-spi`：

          * 属性 ``clock-frequency`` 不再需要
          * 属性 ``clocks`` 现在需要

    * :dtcompatible:`nxp,imx-wdog`：

          * pinctrl 支持

    * :dtcompatible:`nxp,s32-swt`：

          * 移除属性：``clock-frequency``
          * 属性 ``clocks`` 现在需要

    * :dtcompatible:`nxp,lpc-lpadc`：

          * 新属性：``nxp,reference-supply``

    * :dtcompatible:`nxp,kinetis-pit`：

          * 新属性：``max-load-value``
          * 属性 ``clocks`` 现在需要

    * :dtcompatible:`nxp,mcux-edma`：

          * 新属性：``dmamux-reg-offset``
          * 新属性：``channel-gap``
          * 新属性：``irq-shared-offset``

    * :dtcompatible:`nxp,imx-elcdif`：

          * 新属性：``nxp,pxp``

* ON Semiconductor Corp. (onnn)：

  * 新绑定：

    * :dtcompatible:`onnn,ncp5623`

* Princeton Technology Corp. (ptc)：

  * 新绑定：

    * :dtcompatible:`ptc,pt6314`

* Quectel Wireless Solutions Co., Ltd. (quectel)：

  * 新绑定：

    * :dtcompatible:`quectel,bg95`

* QuickLogic Corp. (quicklogic)：

  * 新绑定：

    * :dtcompatible:`quicklogic,eos-s3-pinctrl`

  * 修改的绑定：

    * :dtcompatible:`quicklogic,usbserialport-s3b`：

      * pinctrl 支持

* Raspberry Pi Foundation (raspberrypi)：

  * 新绑定：

    * :dtcompatible:`raspberrypi,pico-header`
    * :dtcompatible:`raspberrypi,pico-i2c`
    * :dtcompatible:`raspberrypi,pico-spi-pio`
    * :dtcompatible:`raspberrypi,pico-timer`

* Raydium Semiconductor Corp. (raydium)：

  * 新绑定：

    * :dtcompatible:`raydium,rm67162`

* Renesas Electronics Corporation (renesas)：

  * 新绑定：

    * :dtcompatible:`renesas,smartbond-lp-osc`
    * :dtcompatible:`renesas,smartbond-timer`

  * 修改的绑定：

    * :dtcompatible:`renesas,smartbond-flash-controller`：

          * 新属性：``read-cs-idle-delay``
          * 新属性：``erase-cs-idle-delay``

* Smart Battery System (sbs)：

  * 新绑定：

    * :dtcompatible:`sbs,default-sbs-gauge`
    * :dtcompatible:`sbs,sbs-charger`

* Seeed Technology Co., Ltd (seeed)：

  * 新绑定：

    * :dtcompatible:`seeed,hm330x`

* SiFive, Inc. (sifive)：

  * 修改的绑定：

    * :dtcompatible:`sifive,i2c0`：

          * pinctrl 支持

* Silicon Laboratories (silabs)：

  * 新绑定：

    * :dtcompatible:`silabs,gecko-adc`

* Sino Wealth Electronic Ltd (sinowealth)：

  * 新绑定：

    * :dtcompatible:`sinowealth,sh1106`
    * :dtcompatible:`sinowealth,sh1106`

* Sitronix Technology Corporation (sitronix)：

  * 修改的绑定：

    * :dtcompatible:`sitronix,st7735r`（在 spi 总线上）：

          * 属性 ``reset-gpios`` 不再需要

* Standard Microsystems Corporation (smsc)：

  * 修改的绑定：

    * :dtcompatible:`smsc,lan91c111-mdio`：

          * 移除属性：``protocol``
          * 属性 ``#address-cells`` const 值从 None 更改为 1
          * 属性 ``#size-cells`` const 值从 None 更改为 0
          * 属性 ``#address-cells`` 现在需要
          * 属性 ``#size-cells`` 现在需要

    * :dtcompatible:`smsc,lan91c111`：

          * 新属性：``local-mac-address``
          * 新属性：``zephyr,random-mac-address``
          * 属性 ``reg`` 不再需要

* Synopsys, Inc. (snps)：

  * 新绑定：

    * :dtcompatible:`snps,dw-timers`

* Solomon Systech Limited (solomon)：

  * 修改的绑定：

    * :dtcompatible:`solomon,ssd1306fb`

          * 新属性：``inversion-on``
          * 新属性：``ready-time-ms``

* Sequans Communications (sqn)：

  * 新绑定：

    * :dtcompatible:`sqn,hwspinlock`

* STMicroelectronics (st)：

  * 新绑定：

    * :dtcompatible:`st,stm32-bxcan`
    * :dtcompatible:`st,stm32-spi-host-cmd`
    * :dtcompatible:`st,stm32f1-rcc`
    * :dtcompatible:`st,stm32f3-rcc`
    * :dtcompatible:`st,stm32wba-flash-controller`
    * :dtcompatible:`st,stm32wba-hse-clock`
    * :dtcompatible:`st,stm32wba-pll-clock`
    * :dtcompatible:`st,stm32wba-rcc`
    * :dtcompatible:`st,stmpe811`

  * 移除的绑定：

    * ``st,stm32-can``

  * 修改的绑定：

    * :dtcompatible:`st,stm32-pwm`：

          * 新属性：``four-channel-capture-support``

    * :dtcompatible:`st,stm32f4-adc`：

          * 新属性：``st,adc-clock-source``
          * 新属性：``st,adc-prescaler``
          * 新属性：``st,adc-sequencer``
          * 移除属性：``temp-channel``
          * 移除属性：``vref-channel``
          * 移除属性：``vbat-channel``

    * :dtcompatible:`st,stm32-adc`：

          * 新属性：``st,adc-clock-source``
          * 新属性：``st,adc-prescaler``
          * 新属性：``st,adc-sequencer``
          * 移除属性：``temp-channel``
          * 移除属性：``vref-channel``
          * 移除属性：``vbat-channel``

    * :dtcompatible:`st,stm32f1-adc`：

          * 新属性：``st,adc-sequencer``
          * 移除属性：``temp-channel``
          * 移除属性：``vref-channel``
          * 移除属性：``vbat-channel``

    * :dtcompatible:`st,stm32-ospi`：

          * 新属性：``io-low-port``
          * 新属性：``io-high-port``

    * :dtcompatible:`st,stm32c0-hsi-clock`：

          * 移除属性：``clocks``

    * :dtcompatible:`st,stm32-hse-clock`：

          * 移除属性：``clocks``

    * :dtcompatible:`st,stm32wl-hse-clock`：

          * 移除属性：``clocks``

    * :dtcompatible:`st,stm32g0-hsi-clock`：

          * 移除属性：``clocks``

    * :dtcompatible:`st,stm32h7-hsi-clock`：

          * 移除属性：``clocks``

    * :dtcompatible:`st,stm32-lse-clock`：

          * 移除属性：``clocks``

    * :dtcompatible:`st,stm32u5-pll-clock`：

          * 新属性：``fracn``

* Telink Semiconductor (telink)：

  * 修改的绑定：

    * :dtcompatible:`telink,b91-pwm`：

          * pinctrl 支持

    * :dtcompatible:`telink,b91`：

          * 新属性：``mmu-type``
          * 新属性：``riscv,isa``

    * :dtcompatible:`telink,b91-i2c`：

          * pinctrl 支持

    * :dtcompatible:`telink,b91-spi`：

          * pinctrl 支持

    * :dtcompatible:`telink,b91-uart`：

          * pinctrl 支持

* Texas Instruments (ti)：

  * 新绑定：

    * :dtcompatible:`ti,ads1112`
    * :dtcompatible:`ti,bq27z746`
    * :dtcompatible:`ti,cc13xx-cc26xx-rtc-timer`
    * :dtcompatible:`ti,cc13xx-cc26xx-timer`
    * :dtcompatible:`ti,cc13xx-cc26xx-timer-pwm`
    * :dtcompatible:`ti,cc32xx-pinctrl`
    * :dtcompatible:`ti,davinci-gpio`
    * :dtcompatible:`ti,davinci-gpio-nexus`
    * :dtcompatible:`ti,lp5009`
    * :dtcompatible:`ti,lp5012`
    * :dtcompatible:`ti,lp5018`
    * :dtcompatible:`ti,lp5024`
    * :dtcompatible:`ti,lp5030`
    * :dtcompatible:`ti,lp5036`
    * :dtcompatible:`ti,lp5569`
    * :dtcompatible:`ti,tas6422dac`
    * :dtcompatible:`ti,tcan4x5x`
    * :dtcompatible:`ti,tla2021`
    * :dtcompatible:`ti,tmag5170`
    * :dtcompatible:`ti,vim`

  * 移除的绑定：

    * ``ti,cc13xx-cc26xx-rtc``
    * ``ti,lp503x``

  * 修改的绑定：

    * :dtcompatible:`ti,cc32xx-i2c`：

          * pinctrl 支持

    * :dtcompatible:`ti,ina230`（在 i2c 总线上）：

          * 新属性：``alert-config``
          * 新属性：``adc-mode``
          * 新属性：``vbus-conversion-time-us``
          * 新属性：``vshunt-conversion-time-us``
          * 新属性：``avg-count``
          * 新属性：``rshunt-micro-ohms``
          * 移除属性：``rshunt-milliohms``
          * 属性 ``config`` 默认值从 None 更改为 0
          * 属性 ``config`` 弃用状态从 False 更改为 True
          * 属性 ``config`` 不再需要

    * :dtcompatible:`ti,ina237`（在 i2c 总线上）：

          * 新属性：``adc-mode``
          * 新属性：``vbus-conversion-time-us``
          * 新属性：``vshunt-conversion-time-us``
          * 新属性：``temp-conversion-time-us``
          * 新属性：``avg-count``
          * 新属性：``high-precision``
          * 新属性：``rshunt-micro-ohms``
          * 移除属性：``rshunt-milliohms``
          * 属性 ``adc-config`` 默认值从 None 更改为 0
          * 属性 ``config`` 默认值从 None 更改为 0
          * 属性 ``adc-config`` 弃用状态从 False 更改为 True
          * 属性 ``config`` 弃用状态从 False 更改为 True
          * 属性 ``adc-config`` 不再需要
          * 属性 ``config`` 不再需要

    * :dtcompatible:`ti,cc32xx-uart`：

          * pinctrl 支持

* 可作为示例和测试中真实厂商替代品的 (vnd)：

  * 新绑定：

    * :dtcompatible:`vnd,memory-attr`
    * :dtcompatible:`vnd,reg-holder-64`
    * :dtcompatible:`vnd,reserved-compat`

  * 修改的绑定：

    * :dtcompatible:`vnd,serial`：

          * 属性 ``reg`` 不再需要

* X-Powers (x-powers)：

  * 新绑定：

    * :dtcompatible:`x-powers,axp192`
    * :dtcompatible:`x-powers,axp192-gpio`
    * :dtcompatible:`x-powers,axp192-regulator`

* Xen Hypervisor (xen)：

  * 新绑定：

    * :dtcompatible:`xen,xen`

  * 移除的绑定：

    * ``xen,xen-4.15``

* Xilinx (xlnx)：

  * 新绑定：

    * :dtcompatible:`xlnx,zynqmp-ipi-mailbox`

* Shenzhen Xptek Technology Co., Ltd (xptek)：

  * 修改的绑定：

    * :dtcompatible:`xptek,xpt2046`（在 spi 总线上）：

          * 总线列表从 ['kscan'] 更改为 []

* Zephyr 特定绑定 (zephyr)：

  * 新绑定：

    * :dtcompatible:`zephyr,fake-rtc`
    * :dtcompatible:`zephyr,i2c-dump-allowlist`
    * :dtcompatible:`zephyr,lvgl-button-input`
    * :dtcompatible:`zephyr,lvgl-encoder-input`
    * :dtcompatible:`zephyr,lvgl-pointer-input`
    * :dtcompatible:`zephyr,mdio-gpio`
    * :dtcompatible:`zephyr,native-tty-uart`
    * :dtcompatible:`zephyr,ram-disk`
    * :dtcompatible:`zephyr,sensing`
    * :dtcompatible:`zephyr,sensing-phy-3d-sensor`

  * 移除的绑定：

    * ``zephyr,gpio-keys``

  * 修改的绑定：

    * :dtcompatible:`zephyr,mmc-disk`（在 sd 总线上）：

          * 新属性：``bus-width``

    * :dtcompatible:`zephyr,bt-hci-spi`（在 spi 总线上）：

          * 新属性：``controller-data-delay-us``

    * :dtcompatible:`zephyr,sdhc-spi-slot`（在 spi 总线上）：

          * 新属性：``pwr-gpios``

    * :dtcompatible:`zephyr,memory-region`：

          * 新属性：``zephyr,memory-attr``
          * 属性 ``zephyr,memory-region-mpu`` enum 值从 ['RAM', 'RAM_NOCACHE', 'FLASH', 'PPB', 'IO', 'EXTMEM'] 更改为 None
          * 属性 ``zephyr,memory-region-mpu`` 弃用状态从 False 更改为 True
          * 属性 ``reg`` 现在需要

库 / 子系统
**********************

* 管理

  * 引入 MCUmgr 客户端支持，包含 img_mgmt 和 os_mgmt 处理程序。

  * 为 MCUmgr 的 :c:enumerator:`MGMT_EVT_OP_CMD_RECV`
    通知回调新增响应检查，允许应用拒绝 MCUmgr 命令。

  * MCUmgr SMP 版本 2 错误转换（转换为遗留 MCUmgr 错误代码）
    现在通过函数处理程序支持，
    在注册组时设置 :c:struct:`mgmt_group` 的 ``mg_translate_error``。
    参见 :c:type:`smp_translate_error_fn` 以获取函数详情。

  * 修复 MCUmgr img_mgmt 组的问题，
    其中初始数据包中的上传大小未被检查。

  * 修复 MCUmgr fs_mgmt 组的问题，
    其中某些状态码未被正确检查，
    这意味着返回的错误可能不是正确的错误，
    但只会在已经存在错误的情况下发生。

  * 修复 SMP 响应函数的问题，
    其中未检查初始 zcbor map 是否成功创建。

  * 修复 MCUmgr shell_mgmt 组的问题，
    其中接收命令的长度未被正确检查。

  * 为 MCUmgr img_mgmt 组新增可选的互斥锁支持，
    可以通过 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_MUTEX` 启用。

  * 新增 MCUmgr settings 管理组，
    允许从远程设备操作 zephyr settings，
    参见 :ref:`mcumgr_smp_group_3` 以获取详情。

  * 新增 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_ALLOW_CONFIRM_NON_ACTIVE_IMAGE_SECONDARY`
    和 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_ALLOW_CONFIRM_NON_ACTIVE_IMAGE_ANY`，
    允许控制是否允许 MCUmgr 客户端确认非活动映像。

  * 新增 :kconfig:option:`CONFIG_MCUMGR_GRP_IMG_ALLOW_ERASE_PENDING`，
    允许擦除等待下次启动的插槽（非 revert 插槽）。

  * 当 :kconfig:option:`CONFIG_MCUMGR_MGMT_HANDLER_USER_DATA` 启用时，
    为 :c:struct:`mgmt_handler` 新增 ``user_data`` 作为可选字段。

  * 为 os mgmt reset 命令新增可选 ``force`` 参数，
    这可以在 :c:enumerator:`MGMT_EVT_OP_OS_MGMT_RESET` 通知回调中检查，
    其数据结构为 :c:struct:`os_mgmt_reset_data`。

  * 通过 :kconfig:option:`CONFIG_MCUMGR_SMP_CBOR_MIN_ENCODING_LEVELS`
    新增可配置的 SMP 编码级别数量，
    当 :kconfig:option:`CONFIG_ZCBOR_CANONICAL` 启用时，
    自动递增树内组的最小编码级别。

  * 为 EC Host 命令协议新增 STM32 SPI 后端。

  * 修复 settings_mgmt 返回未知错误而不是指定无效键错误的问题。

  * 修复 fs_mgmt 在尝试对空文件进行哈希/校验和时
    返回参数过大错误而不是文件为空错误的问题。

* 文件系统

  * 新增对 ext2 文件系统的支持。
  * 新增支持从 shell/fs 在块设备上挂载 littlefs。
  * 为 FS_LITTLEFS_DECLARE_CUSTOM_CONFIG 宏新增对齐参数，
    当我们在 CONFIG_SDHC_BUFFER_ALIGNMENT 上对齐缓冲区时，
    可以为 SDMMC 设备加速读/写操作，
    因为我们可以避免从卡缓冲区到读/编程缓冲区的额外数据复制。

* 随机

  * ``CONFIG_XOROSHIRO_RANDOM_GENERATOR`` 已被弃用很长时间，现已最终移除。

* 保持

  * 新增 :ref:`blinfo_api` 子系统。

  * 新增支持，允许使用
    :kconfig:option:`CONFIG_RETENTION_MUTEX_FORCE_DISABLE`
    强制禁用互斥锁支持。

* 二进制描述符

  * 新增 :ref:`binary_descriptors`（``bindesc``）子系统。

* POSIX API

  * 为 :c:func:`pthread_create` 新增动态线程栈支持
  * 修复 :c:func:`stat`，使其返回文件统计而不是文件系统统计
  * 实现 :c:func:`pthread_barrierattr_destroy`、:c:func:`pthread_barrierattr_getpshared`、
    :c:func:`pthread_barrierattr_init`、:c:func:`pthread_barrierattr_setpshared`、
    :c:func:`pthread_condattr_destroy`、:c:func:`pthread_condattr_init`、
    :c:func:`pthread_mutexattr_destroy`、:c:func:`pthread_mutexattr_init`、:c:func:`uname`、
    :c:func:`sigaddset`、:c:func:`sigdelset`、:c:func:`sigemptyset`、:c:func:`sigfillset`、
    :c:func:`sigismember`、:c:func:`strsignal`、:c:func:`pthread_spin_destroy`、
    :c:func:`pthread_spin_init`、:c:func:`pthread_spin_lock`、:c:func:`pthread_spin_trylock`、
    :c:func:`pthread_spin_unlock`、:c:func:`timer_getoverrun`、:c:func:`pthread_condattr_getclock`、
    :c:func:`pthread_condattr_setclock`、:c:func:`clock_nanosleep`
  * 新增支持，通过 :c:func:`ioctl` 的
    :c:macro:`FIONREAD` 请求查询可读字节数
  * 新增 :kconfig:option:`CONFIG_FDTABLE`，用于条件编译文件描述符表
  * 为 POSIX 线程、互斥锁和条件变量新增日志
  * 修复 :c:func:`poll` 与事件文件描述符的问题

* LoRa/LoRaWAN

  * 将 ``loramac-node`` 从 v4.6.0 更新到 v4.7.0

* CAN ISO-TP

  * 新增对 CAN FD 的支持。

* RTIO

  * 新增原子完成计数器，修复单元测试捕获的竞态
  * 新增 :c:macro:`RTIO_SQE_NO_RESPONSE` 标志，
    用于不需要完成通知的提交
  * 移除不同执行器的未使用 Kconfig 选项

* ZBus

  * 将通道和观察者的元数据更改为符合数据/配置方法。
    ZBus 将不可变配置存储在 Flash 中的可迭代部分，
    将可变数据部分存储在 RAM 中。
  * 通道和观察者之间的关系使用称为 observation 的新实体进行映射。
    observation 使我们能够提高屏蔽 observation 的粒度。
    开发人员可以屏蔽单个 observation、禁用观察者，
    或使用运行时观察者。
  * 新增 API :c:macro:`ZBUS_CHAN_ADD_OBS` 宏，
    用于添加通道定义后的静态观察者。
    这可以替代运行时观察者功能，
    允许开发人员在通道定义之后在不同文件中添加静态观察者。
    它提高了使用 ZBus 的系统的可组合性，
    使定义后的通道观察依赖栈而不是堆。
  * 新增一种名为 Message Subscriber 的观察者类型。
    ZBus 的 VDED 在发布/通知过程中会发送消息的副本。
  * 更改 VDED 投递序列。
    参见 :ref:`documentation <zbus delivery sequence>`。
  * ZBus 运行时观察者现在依赖堆而不是内存池。
  * 新增可迭代部分迭代器 API（用于通道和观察者），
    现在可以接收 ``user_data`` 指针，
    以在函数调用之间保持上下文。
  * 新增 API :c:macro:`ZBUS_LISTENER_DEFINE_WITH_ENABLE` 和
    :c:macro:`ZBUS_SUBSCRIBER_DEFINE_WITH_ENABLE`，
    允许开发人员以编程方式定义观察者状态（启用/禁用）。
    使用该 API，开发人员可以创建初始禁用的观察者，
    并在运行时启用它们。

* 电源管理

  * 新增 :kconfig:option:`CONFIG_PM_NEED_ALL_DEVICES_IDLE`。
    当设置此选项时，如果有任何设备忙，
    电源管理将保持系统活动。
  * :c:func:`pm_device_runtime_get` 现在可以从 ISR 调用。
  * 电源状态可以直接在设备树中通过 ``status = "disabled";`` 禁用
  * 新增辅助函数 :c:func:`pm_device_driver_init`，
    用于将设备初始化到特定电源状态。

* 调制解调器模块

  * 新增 :ref:`modem` 子系统。

HAL
****

* Nordic

  * 将 nrfx 更新到版本 3.1.0。

* Nuvoton

  * 新增 Nuvoton NuMaker M46x

MCUboot
*******

  * 新增 :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_NO_DOWNGRADE`，
    允许通知应用，板上的 MCUboot 已配置为启用降级防止。
    此选项在 DirectXIP 模式下自动选择，
    对两种 swap 模式都可用。

  * 新增 :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_MODE_OVERWRITE_ONLY`，
    允许通知应用，板上的 MCUboot 将用次要插槽内容覆盖主要插槽，
    而不在主要插槽中保存原始映像。

  * 修复串行恢复在解密映像上不显示映像详情的问题。

  * 修复串行恢复在单插槽模式下错误地遍历 2 个映像插槽的问题。

  * 修复 boot_serial 重复未被处理的问题（当输出了输出时），
    这会导致命令分歧，其中随后发送的命令会发送前一个命令的输出。

  * 修复 boot_serial zcbor setup encoder 函数错误地将缓冲区地址
    包含在大小中的问题，这导致串行恢复在某些平台上失败。

  * 修复默认在 optimize 下错误构建 debug 模式的问题，
    这节省了相当多的闪存空间。

  * 修复串行恢复使用 MBEDTLS 时存在未定义操作的问题，
    当次要插槽映像加密时导致使用错误。

  * 修复 bootutil 在非 swap 模式下对最大对齐断言的问题。

  * 新增错误输出，当闪存设备无法打开且断言被禁用时，
    这现在会使引导加载器 panic。

  * 为共享数据函数定义新增当前运行的插槽 ID 和最大应用大小。

  * 为 imgtool 新增 P384 和 SHA384 支持。

  * 新增可选的串行恢复映像状态和映像集状态命令。

  * 为 imgtool 中的签名映像解析新增 ``dumpinfo`` 命令。

  * 为 imgtool 新增 ``getpubhash`` 命令，用于 dump 公钥的 sha256 哈希。

  * 新增支持，``getpub`` 可以将输出打印到文件（在 imgtool 中）。

  * 新增支持，在 imgtool 中 dump 公钥的原始版本。

  * 新增支持，通过 retention 子系统与应用共享 boot 信息。

  * 新增支持，串行恢复可以读取和处理加密的次要插槽分区。

  * 移除 ECDSA P224 支持。

  * 移除自定义映像列表 boot serial 扩展支持。

  * 重新设计 boot serial 扩展，
    使其可以通过切换到可迭代部分被模块或用户仓库使用。

  * 重新设计 Zephyr 的映像加密支持，
    静态 dummy 密钥文件不再在代码中，
    必须提供 pem 文件以提取私钥和公钥。
    Kconfig 菜单已更改为仅显示一个用于启用加密和选择密钥文件的选项。

  * 重新设计 ECDSA256 TLV 曲线无关，并重命名为 ``ECDSA_SIG``。

  * 用 zcbor 函数调用替换了 CDDL 自动生成的函数代码，
    这现在允许参数以任何顺序提供。

  * 本次发布中的 MCUboot 版本是 ``2.0.0+0-rc1``。

Nanopb
******

  * 将项目状态更改为 maintained。

  * 新增单独的 nanopb.cmake 文件，供应用包含。

  * 新增辅助 cmake 函数 ``zephyr_nanopb_sources``，
    以简化 ``.proto`` 文件包含。

LVGL
****

  * 将项目状态更改为 maintained。

  * 库已更新到发布 v8.3.7。

  * 新增 ``zephyr,lvgl-{pointer,button,encoder}-input`` 伪设备绑定。
    :kconfig:option:`CONFIG_LV_Z_KSCAN_POINTER` 仍然受支持，
    但触摸控制器需要一个 :dtcompatible:`zephyr,kscan-input` 子节点
    以发出输入事件。

  * LVGL shell 允许猴子测试（需要 :kconfig:option:`CONFIG_LV_USE_MONKEY`）
    和检查内存使用。

Trusted Firmware-A
******************

* 更新到 TF-A 2.9.0。

文档
*************

* 将 Sphinx 升级到 6.2

测试和示例
*****************

* 创建文件系统通用示例（``fs_sample``）。
  它源自 FAT（``fat_fs``）示例，
  同时支持 FAT 和 ext2 文件系统。

* 创建 zbus 确认通道示例，
  演示如何使用订阅者实现保证投递的通道。

* 创建 zbus 消息订阅者示例，
  演示如何使用消息订阅者。