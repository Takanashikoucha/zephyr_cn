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
* 新增对 45+ 个新板级的支持
* 网络：对 CoAP、连接管理器、DHCP、以太网、gPTP、ICMP、IPv6 和 LwM2M 的改进
* 蓝牙：对控制器、音频、网状，以及主机栈的总体改进
* 改进 LVGL 图形库集成
* 集成 CodeChecker 静态分析器支持
* Picolibc 现在是默认 C 标准库

从 Zephyr v3.4.0 迁移应用到 Zephyr v3.5.0 时
所需或建议的更改概述
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

* 新增对通过 :c:func:`k_thread_stack_alloc` 动态线程栈分配的支持
* 新增对 :c:func:`k_spin_trylock` 的支持
* 新增 :c:func:`k_object_is_valid` 以检查内核对象是否有效。这替换了在树中重复的代码。

架构
*************

* ARC

  * 为 ARC VPX 处理器引入标量移植
  * 为 ARCv3 HS（32 位和 64 位）SMP 平台引入支持，最多 12 个 CPU 核心
  * 重新设计 ARC MWDT 工具链的 GNU 辅助工具使用。现在辅助工具可以从 Zephyr SDK（如果 SDK 已安装）使用
  * 修复动态线程栈分配
  * 修复 STR 汇编宏偏移计算问题，这可能导致 ARCv3 64bit 的构建错误
  * 清理并使 ARC MWDT 工具链路径（ARCMWDT_TOOLCHAIN_PATH）的处理更用户友好

* ARM

  * Arm Cortex-M 的架构支持已从 Arm Cortex-A 和 Cortex-R 中分离。这包括处理任务（如 IRQ 管理、异常处理、线程处理和交换）的单独源模块。有关实现详情，请参见 :github:`60031`。

* ARM64

* RISC-V

  * 新增支持，用于使用 PMP 检测空指针异常。
  * 新增 :kconfig:option:`CONFIG_RISCV_RESERVED_IRQ_ISR_TABLES_OFFSET` 选项，允许在指定偏移处使用 IRQ 向量，以满足 Core-Local Interrupt Controller RISC-V 规范设定的要求。
  * 新增 :kconfig:option:`CONFIG_RISCV_SOC_HAS_CUSTOM_SYS_IO` 选项，允许使用自定义系统输入/输出函数。
  * 引入 :kconfig:option:`CONFIG_RISCV_TRAP_HANDLER_ALIGNMENT` 选项，用于设置 trap 处理代码的正确对齐，这取决于 ``MTVEC.BASE`` 字段大小并且是平台或应用特定的。

* Xtensa

  * 新增基本 MMU v2 支持。

* x86

  * 为 Intel Alder Lake 板级新增支持
  * 为 Intel Sensor Hub（ISH）新增支持

* POSIX

  * 已重新设计以使用原生仿真器。
  * 已新增板级。
  * 对于新板级，可以使用嵌入式 C 库，并避免与主机符号和库的冲突。
  * :ref:`POSIX OS 抽象<posix_support>` 在这些新板级中受支持。
  * 现在支持 AMP 目标。
  * 为 LLVM 源剖析/覆盖率新增支持。

蓝牙
*********

* 音频

  改进编解码配置和编解码能力的内存使用。修复 BAP 和 BAP 相关服务（ASCS、PACS、BASS）中的多个 bug，以及缺失的功能，例如适当的通知处理。

  * 新增 BAP ``bt_bap_stream_get_tx_sync``
  * 新增 CAP 流发送和 tx 同步
  * 新增 ``bt_audio_codec_cap_get`` 辅助函数
  * 为 CAP 新增长读/写支持
  * 修复 ASCS 源 ASE 链路丢失状态转换
  * 修复 ASCS 可能的 ASE 泄漏
  * 修复 ASCS 以在 ASE 不在流状态时丢弃 ISO PDU
  * 修复 BAP ``bt_bap_scan_delegator_find_state`` 实现
  * 修复 BAP 在 ``broadcast_sink_create`` 中 PA 同步和 ID 的问题
  * 修复 TMAS 特征权限
  * 修复 ``tbs_client`` 缺失的发现完成事件
  * 修复音频栈以在音频元数据中接受空 CCID 列表
  * 修复 ASCS 中 metadata_backup 的大小错误
  * 修复可能的 ASCS ASE 卡在释放状态
  * 重构 ``bt_audio_codec_cap`` 为扁平数组
  * 重构 ``bt_audio_codec_cfg`` 为扁平数组
  * 移除 ``CONFIG_BT_PACS_{SNK,SRC}_CONTEXT``
  * 从广播汇点移除扫描和 PA 同步
  * 将 ``bt_codec`` 重命名为 ``bt_audio_codec_{cap, conf, data}``
  * 重命名编解码 QoS 帧
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
  * 新增 ``BT_CONN_PARAM_ANY`` 以允许将任何值设置到连接参数
  * 新增高级广播 ISO 参数
  * 新增高级单播 ISO 参数
  * 新增用于管理蓝牙设置存储的新 API
  * 修复 HCI ISO 数据包分片
  * 修复发送到控制器的 HCI ISO SDU 长度
  * 修复 OTS ``bt_ots_init`` 参数结构体命名
  * 修复过程未完成时的 OTS 内存泄漏
  * 修复连接引用泄漏
  * 修复强制配对请求处理
  * 修复主机以在启动遗留广播时使可解析私有地址无效
  * 修复 ``bt_iso_cig_reconfigure`` 的问题
  * 修复 ``bt_conn_le_start_encryption`` 中可能的缓冲区溢出
  * 修复某些 SMP 问题
  * 修复以在连接断开时中止配对
  * 更新 L2CAP 接受回调
  * 更新 LE L2CAP 连接回调以在连接响应之后
  * 更新 PAwR 实现以在 BT_PRIVACY=y 时使用 RPA 作为响应器地址
  * 修复 OTS ``bt_ots_init`` 参数结构体命名
  * 修复过程未完成时的 OTS 内存泄漏
  * 修复连接引用泄漏
  * 修复强制配对请求处理
  * 修复主机以在启动遗留广播时使可解析私有地址无效
  * 修复 ``bt_iso_cig_reconfigure`` 的问题
  * 修复 ``bt_conn_le_start_encryption`` 中可能的缓冲区溢出
  * 修复某些 SMP 问题
  * 修复以在连接断开时中止配对
  * 更新 L2CAP 接受回调
  * 更新 LE L2CAP 连接回调以在连接响应之后
  * 更新 PAwR 实现以在 BT_PRIVACY=y 时使用 RPA 作为响应器地址

* 网状

  * 新增 TF-M 支持。
  * 新增支持，用于同时使用 tinycrypt 和 PSA 基于的加密
  * 新增对完整虚拟地址（具有冲突解决）的支持。引入 :kconfig:option:`CONFIG_BT_MESH_LABEL_NO_RECOVER` Kconfig 选项以恢复订阅列表和模型发布的地址。
  * 新增统计模块。
  * 修复问题，其中作为 LPN 操作的节点在通过回环接口发送分段消息时触发 Friend Poll 消息。
  * 修复问题，其中在节点上配置成功完成，当配置器使用相同的公共密钥时。
  * 修复问题，其中从除系统工作队列之外的协作线程调用的 :c:func:`settings_load` 函数导致 GATT Mesh Proxy 服务注册失败。
  * 修复问题，其中节点可能进入 IV Update In Progress 状态，如果带有当前 IV Index 和 IV Update 标志设置为 1 的旧 SNB 被重新发送。

  * 网状协议 v1.1 更改

    * 新增持久存储私有 GATT Proxy 状态。
    * 为固件分发服务器模型中的固件分发上传 OOB 启动消息新增支持。该消息支持可以通过 :kconfig:option:`CONFIG_BT_MESH_DFD_SRV_OOB_UPLOAD` Kconfig 选项启用。
    * 在配置中使用 OOB 方法时新增扩展配置协议超时。
    * 新增对组成数据页 2、129 和 130 的支持。
    * 新增组成数据页 0、1、2、128、129 和 130 的文档。
    * 新增传输层中分片和重组的文档。
    * 新增 SAR 配置模型的文档
    * 修复问题，其中操作码聚合器服务器模型在没有操作码聚合器客户端模型时无法编译。
    * 修复问题，其中在私有 GATT Proxy 广播中使用身份地址而不是不可解析私有地址。
    * 修复 Proxy 隐私参数支持。
    * 修复问题，其中组成数据页 128 在已实例化远程配置服务器模型的节点上不存在。
    * 修复问题，其中大型组成数据服务器模型不支持除 0 之外的组成数据页。
    * 修复问题，其中与远程配置服务器模型一起在节点上实例化的远程配置客户端模型无法重新配置自身。
    * 修复问题，其中分片和重组中的确认定时器在传入段确认消息不包含至少一个新标记为已确认的段时未重新启动。
    * 修复问题，其中按需私有 Proxy 服务器和客户端模型具有相互依赖，不允许分别编译。

* 控制器

  改进控制器中广播和连接 Isochronous 通道的支持，启用 LE 音频应用开发。控制器是实验性的，缺少 Isochronous 通道底层链路层中交错打包的实现。

  * 新增 Adv PDU 最小大小检查
  * 新增 Kconfig 选项以忽略 Tx HCI ISO 数据包序列号
  * 新增 Kconfig 以避免 ISO SDU 分片
  * 新增 Kconfig 以最大化 BIG 事件长度并抢占 PTO & CTRL 子事件
  * 新增 ``BT_CTLR_EVENT_OVERHEAD_RESERVE_MAX`` Kconfig
  * 为 ticker 事务新增内存屏障
  * 新增缺失的 nRF53x Tx 功率 Kconfig
  * 为连接 ISO 中的 Flush 超时新增支持
  * 修复 BIS 负载滑动窗口越界检查
  * 修复 CIS 中心 FT 计算
  * 修复 CIS 中心错误处理
  * 修复 CIS 非对称 PHY 使用
  * 修复在启用 DF 支持时的 CIS 加密
  * 修复用于质量测试和时间戳的 ISO-AL
  * 修复 HCI LE CIS Established 事件中的 PHY 值
  * 修复 ULL 在罕见条件下卡在信号量
  * 修复由于 PER CIS 活动集过晚导致的断言
  * 修复导致断言的编译器指令重排序
  * 修复连接 ISO 动态 tx 功率
  * 修复失败的广播一致性测试
  * 修复在 Coded PHY 不受支持时接收辅助 PDU 的处理
  * 修复在重新调度 ticker 节点时计划 ticker 节点中的泄漏
  * 修复缺失的主机特性重置
  * 修复 nRF53 SoC 背靠背 PDU 链接
  * 修复 nRF53 SoC 背靠背 Tx Rx 实现
  * 修复 Adv PDU 溢出计算中的回归
  * 修复导致断言和调度停滞的观察者中的回归
  * 修复 nRF SoC 上预编程 PPI 的使用
  * 在准备 FT 支持时移除具有无效状态的 HCI ISO 数据
  * 更新扩展广播报告以在未收到 ``AUX_ADV_IND`` 时不生成
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

  * i.MX RT SoC 不再默认启用 CONFIG_DEVICE_CONFIGURATION_DATA。使用外部 SDRAM 的板级应设置 CONFIG_DEVICE_CONFIGURATION_DATA 和 CONFIG_NXP_IMX_EXTERNAL_SDRAM 为启用。
  * i.MX RT SoC 不再支持 CONFIG_OCRAM_NOCACHE，因为此功能可以使用设备树内存区域实现
  * 重构 ESP32 SoC 文件夹。因此现在是适当的 SoC 系列。
  * RP2040：更改为在初始化时重置 I2C 设备

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

  * 新增对 nsim_vpx5 - 仿真（nSIM）平台（具有 ARCv2 VPX5 核心，接近 vpx5_integer_full 模板）的支持
  * 新增对 nsim_hs5x_smp_12cores - 仿真（nSIM）平台（具有 12 核 SMP 32 位 ARCv3 HS）的支持
  * 新增对 nsim_hs6x_smp_12cores - 仿真（nSIM）平台（具有 12 核 SMP 64 位 ARCv3 HS）的支持

* 新增对这些 ARM 板级的支持：

  * Nuvoton NuMaker 平台 M467
  * ST Nucleo U5A5ZJ Q
  * ST Nucleo WBA52CG

* 新增对这些 ARM64 板级的支持：

* 新增对这些 RISC-V 板级的支持：

* 新增对这些 X86 板级的支持：

* 新增对这些 ARM64 板级的支持：

* 新增对这些 RISC-V 板级的支持：

* 新增对这些 X86 板级的支持：

* 新增对这些 Xtensa 板级的支持：

* 新增对这些 ARM64 板级的支持：

* 新增对这些 RISC-V 板级的支持：

* 新增对这些 X86 板级的支持：

* 新增对这些 ARM64 板级的支持：

* 新增对这些 RISC-V 板级的支持：

* 新增对这些 X86 板级的支持：

* 新增对这些 Xtensa 板级的支持：

  * 新增 ``esp32_devkitc_wroom`` 和 ``esp32_devkitc_wrover``。
  * 新增 ``esp32s3_luatos_core``。
  * 新增 ``m5stack_core2``。
  * 新增利用 Diamond DC233c SoC 支持测试 Xtensa MMU 的 ``qemu_xtensa_mmu``。
  * 新增 ``xiao_esp32s3``。
  * 新增 ``yd_esp32``。

* 新增对这些 POSIX 板级的支持：

  * :zephyr:board:`native_sim(_64) <native_sim>`
  * nrf5340bsim_nrf5340_cpu(net|app)。仿真的 nrf5340 SoC，其无线电流量使用 Babblesim。

* 新增对这些 POSIX 板级的支持：

  * :zephyr:board:`native_sim(_64) <native_sim>`
  * nrf5340bsim_nrf5340_cpu(net|app)。仿真的 nrf5340 SoC，其无线电流量使用 Babblesim。

* 新增对这些 POSIX 板级的支持：

  * :zephyr:board:`native_sim(_64) <native_sim>`
  * nrf5340bsim_nrf5340_cpu(net|app)。仿真的 nrf5340 SoC，其无线电流量使用 Babblesim。

* 对这些 ARC 板级进行以下更改：

  * 为 hsdk4xd 平台关闭不支持的栈检查选项
  * 将 ARC QEMU 平台的供应商前缀从 "qemu" 更改为 "snps"

* 对这些 ARM 板级进行以下更改：

  * 在 ST nucleo 板级上新增 ST morpho 连接器描述。

  * rpi_pico：

    * 使用 openocd 调试时的默认适配器已更改为 cmsis-dap。

* 对这些 ARM 板级进行以下更改：

  * 在 ST nucleo 板级上新增 ST morpho 连接器描述。

  * rpi_pico：

    * 使用 openocd 调试时的默认适配器已更改为 cmsis-dap。

* 对这些 ARM64 板级进行以下更改：

* 对这些 RISC-V 板级进行以下更改：

* 对这些 X86 板级进行以下更改：

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

* 移除对这些 ARC 板级的支持：

* 移除对这些 ARM 板级的支持：

* 移除对这些 ARM64 板级的支持：

* 移除对这些 RISC-V 板级的支持：

* 移除对这些 X86 板级的支持：

* 移除对这些 Xtensa 板级的支持：

  * 移除 ``esp32``。改用 ``esp32_devkitc_*``。

* 对其他板级进行以下更改：

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

* Twister 现在支持测试套件 .yml 文件中的 ``required_snippets``，这可以用于在运行测试时包含 snippet（并排除 snippet 无法应用到的任何板级）。

* 中断

  * 新增对共享中断的支持

* 新增支持，用于在 sysbuild 中设置 MCUboot 加密密钥，然后传播到引导加载器和目标映像以自动创建加密更新。

* 构建时优先级检查：默认启用构建时优先级检查。如果最终 ELF 文件中的初始化序列与设备树层次结构不匹配，这会导致构建失败。可以通过禁用 :kconfig:option:`CONFIG_CHECK_INIT_PRIORITIES` 选项来关闭它。

* 新增新的 ``initlevels`` 目标，用于打印最终 ELF 文件中的最终设备和 :c:macro:`SYS_INIT` 初始化序列。

* 重新设计 syscall 代码生成，使并非所有 marshalling 函数都包含在最终二进制中。与禁用子系统关联的 Syscalls 不再生成其 marshalling 函数。

* 为树内代码子集部分启用关于影子变量的编译器警告。树外代码需要在我们能够完全启用影子变量警告之前进行修补。

构建系统和基础设施
*******************************

* SCA（静态代码分析）

  * 新增对 CodeChecker 的支持

* Twister 现在支持测试套件 .yml 文件中的 ``required_snippets``，这可以用于在运行测试时包含 snippet（并排除 snippet 无法应用到的任何板级）。

* 中断

  * 新增对共享中断的支持

* 新增支持，用于在 sysbuild 中设置 MCUboot 加密密钥，然后传播到引导加载器和目标映像以自动创建加密更新。

* 构建时优先级检查：默认启用构建时优先级检查。如果最终 ELF 文件中的初始化序列与设备树层次结构不匹配，这会导致构建失败。可以通过禁用 :kconfig:option:`CONFIG_CHECK_INIT_PRIORITIES` 选项来关闭它。

* 新增新的 ``initlevels`` 目标，用于打印最终 ELF 文件中的最终设备和 :c:macro:`SYS_INIT` 初始化序列。

* 重新设计 syscall 代码生成，使并非所有 marshalling 函数都包含在最终二进制中。与禁用子系统关联的 Syscalls 不再生成其 marshalling 函数。

* 为树内代码子集部分启用关于影子变量的编译器警告。树外代码需要在我们能够完全启用影子变量警告之前进行修补。

构建系统和基础设施
*******************************

* SCA（静态代码分析）

  * 新增对 CodeChecker 的支持

* Twister 现在支持测试套件 .yml 文件中的 ``required_snippets``，
  这可以用于在运行测试时包含 snippet
  （并排除 snippet 无法应用到的任何板级）。

* 中断

  * 新增对共享中断的支持

* 新增支持，用于在 sysbuild 中设置 MCUboot 加密密钥，
  然后
  传播
  到
  引导
  加载器
  和
  目标
  映像
  以
  自动
  创建
  加密
  更新。

* 构建时优先级检查：
  默认
  启用
  构建
  时
  优先级
  检查。
  如果
  最终
  ELF
  文件
  中的
  初始化
  序列
  与
  设备树
  层次
  结构
  不
  匹配，
  这
  会
  导致
  构建
  失败。
  可以
  通过
  禁用
  :kconfig:option:`CONFIG_CHECK_INIT_PRIORITIES`
  选项
  来
  关闭
  它。

* 新增新的 ``initlevels`` 目标，
  用于
  打印
  最终
  ELF
  文件
  中的
  最终
  设备
  和
  :c:macro:`SYS_INIT`
  初始化
  序列。

* 重新
  设计
  syscall
  代码
  生成，
  使
  并非
  所有
  marshalling
  函数
  都
  包含
  在
  最终
  二进制
  中。
  与
  禁用
  子系统
  关联
  的
  Syscalls
  不再
  生成
  其
  marshalling
  函数。

* 为树内代码子集部分启用关于影子变量的编译器警告。树外代码需要在我们能够完全启用影子变量警告之前进行修补。

驱动和传感器
*******************

* ADC

  * 为 STM32F0 HSI14 时钟（专用 ADC 时钟）新增支持
  * 为 STM32 ADC 源时钟和预分频器新增支持。在 STM32F1 和 STM32F3 系列中，
    ADC 预分频器可以使用专用 RCC 时钟控制器选项配置。
  * 为所有 STM32 系列（F1 除外）的 ADC 序列器新增支持
  * 修复 STM32F4 ADC 温度和 Vbat 测量。
  * 为 TI ADS1112 新增驱动。
  * 为 TI TLA2021 新增驱动。
  * 为 Gecko ADC 新增驱动。
  * 为 NXP S32 ADC SAR 新增驱动。
  * 为 MAX1125x 系列新增驱动。
  * 为 MAX11102-MAX1117 新增驱动。

* CAN

  * 为具有集成收发器的 TI TCAN4x5x CAN-FD 控制器（:dtcompatible:`ti,tcan4x5x`）新增支持。
  * 为 Microchip MCP251xFD CAN-FD 控制器（:dtcompatible:`microchip,mcp251xfd`）新增支持。
  * 为 Bosch M_CAN 控制器驱动后端新增 CAN 统计支持。
  * 将 NXP S32 CANXL 驱动切换为使用时钟控制来使用 CAN 时钟，
    而不是在设备树中硬编码 CAN 时钟频率。

* 时钟控制

  * 为 Nuvoton NuMaker M46x 新增支持

* 计数器

  * 新增 :kconfig:option:`CONFIG_COUNTER_RTC_STM32_SUBSECONDS`
    以
    启用
    亚秒
    作为
    STM32
    RTC
    基于
    计数器
    驱动
    的
    基本
    时间
    tick。

  * 为 Raspberry Pi Pico 定时器新增支持

* DAC

  * 为 Analog Devices AD56xx 新增支持
  * 为 NXP lpcxpresso55s36（LPDAC）新增支持

* 磁盘

  * Ramdisk 驱动现在使用设备树配置，
    并
    支持
    多个
    实例

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

  * 新增要求，
    用于
    ``entropy_get_entropy()``
    必须
    线程
    安全，
    因为
    随机
    子系统
    需要。

* 以太网

  * 新增 :kconfig:option:`CONFIG_ETH_NATIVE_POSIX_RX_TIMEOUT`
    以
    设置
    native
    posix
    的
    rx
    超时。
  * 为 adin2111 新增支持。
  * 为 NXP S32 GMAC 新增支持。
  * 为 eth_smsc91x 中的混杂模式新增支持。
  * 为 STM32H5X SOC 系列新增支持。
  * 为 MDIO 第 45 条 API 新增支持。
  * 为 YD-ESP32 板级以太网新增支持。
  * 修复 stm32 以通过以设备 ID 作为 MAC 的基础来生成更唯一的 MAC 地址。
  * 修复 mcux 以将 PTP 时间戳精度从 20us 增加到 200ns。
  * 修复使用 VLAN 时的以太网最大头大小。
  * 移除 ``mdio`` DT 属性。请在驱动中改用 :c:macro:`DT_INST_BUS()`。
  * 重构 smsc91x 中的设备节点层次结构。
  * 将 phy-dev 属性重命名为 phy-handle，
    以
    匹配
    Linux
    ethernet-controller
    绑定
    并
    将其
    移动
    到
    ethernet.yaml
    以
    供
    其他
    驱动
    使用。
  * 更新以太网 PHY 以在 DT 绑定中使用 ``reg`` 属性。
  * 更新驱动 DT 绑定以一致地使用 ``ethernet-phy`` 设备树节点名称。
  * 更新 esp32 和 sam-gmac DT 以通过 phandle 而不是子节点指向 phy，
    这
    使
    phy
    设备
    成为
    mdio
    的
    子节点。

* 闪存

  * 引入
    npcx
    闪存
    驱动，
    它
    支持
    通过
    单个
    Flash
    Interface
    Unit
    （
    FIU
    ）
    模块
    和
    Direct
    Read
    Access
    （
    DRA
    ）
    模式
    的
    两个
    或
    更多
    spi
    nor
    闪存
    以
    获得
    更好的
    性能。
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
  * 新增使用 DeviceTree 调试转储消息的过滤
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

    * 修复在控制器忙时的传输问题。现在在继续另一个传输之前
      等待控制器空闲。

* IEEE 802.15.4

  * 在 ieee802154_radio_api 中引入了新的强制方法 attr_get()。
    驱动至少需要实现
    IEEE802154_ATTR_PHY_SUPPORTED_CHANNEL_PAGES 和
    IEEE802154_ATTR_PHY_SUPPORTED_CHANNEL_RANGES。
  * 移除了硬件能力 IEEE802154_HW_2_4_GHZ 和 IEEE802154_HW_SUB_GHZ，
    因为它们与标准不一致，
    并且
    一些
    已
    存在
    的
    驱动
    无法
    正确
    表达
    其
    通道
    页
    和
    通道
    范围
    （
    特别是
    SUN
    FSK
    和
    HRP
    UWB
    驱动
    ）。
    这些
    能力
    被
    符合
    标准的
    新
    驱动
    属性
    IEEE802154_ATTR_PHY_SUPPORTED_CHANNEL_PAGES
    替换，
    它
    适合
    所有
    树
    内
    驱动。
  * 从 ieee802154_radio_api 中移除了方法 get_subg_channel_count()。
    此
    方法
    无法
    正确
    表达
    已
    存在
    驱动
    的
    通道
    范围
    （
    特别是
    SUN
    FSK
    驱动
    实现
    通道
    页
    >
    0
    并且
    可能
    没有
    零
    基
    通道
    范围
    或
    无法
    被
    表示
    的
    UWB
    驱动
    ）。
    此
    方法
    被
    新
    驱动
    属性
    IEEE802154_ATTR_PHY_SUPPORTED_CHANNEL_RANGES
    替换，
    它
    适合
    所有
    树
    内
    驱动。

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

  * 将 ``zephyr,gpio-keys`` 合并到 :dtcompatible:`gpio-keys`
    并为
    所有
    树
    内
    板级
    ``gpio-keys``
    节点
    添加
    ``zephyr,code``
    代码。

  * 将回调定义宏从 ``INPUT_LISTENER_CB_DEFINE``
    重命名为
    :c:macro:`INPUT_CALLBACK_DEFINE`。

* PCIE

  * 在 shell 中新增支持以显示 PCIe 能力。

  * 新增虚拟通道支持。

  * 新增 kconfig :kconfig:option:`CONFIG_PCIE_INIT_PRIORITY`
    以
    指定
    主机
    控制器
    的
    初始化
    优先级。

  * 新增支持，用于从 ACPI PCI 路由表（PRT）获取 IRQ。

* ACPI

  * 采用 ACPICA 库作为新模块以进一步增强 ACPI 支持。

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
  * 重构 pwm_nrf5_sw 驱动，
    使
    其
    可以
    在
    nRF53
    和
    nRF91
    系列
    上
    使用。
    因此，
    驱动
    被
    重命名为
    pwm_nrf_sw。
  * 为 Nuvoton NuMaker 系列新增驱动。
  * 新增基于 NXP S32 EMIOS 外设的 PWM 驱动。

* 调节器

  * 为 GPIO 控制的电压调节器新增支持

  * 为 AXP192 PMIC 新增支持

  * 为 NXP VREF 调节器新增支持

  * 修复调节器现在可以指定其工作电压

  * nPM1300 现在支持 PFM 模式

  * 新增用于配置 "ship" 模式的新 API

  * 调节器 shell 允许配置 DVS 模式

* 重置

  * 为 Nuvoton NuMaker M46x 新增支持

* 保留内存

  * 新增支持，
    用于
    允许
    使用
    :kconfig:option:`CONFIG_RETAINED_MEM_MUTEX_FORCE_DISABLE`
    强制
    禁用
    互斥锁
    支持。

  * 修复用户模式支持不起作用的问题。

* RTC

  * 为 STM32 RTC API 驱动新增支持。此驱动与
    COUNTER
    API
    的
    RTC
    基于
    实现
    的
    使用
    不
    兼容。

* SDHC

  * 为 Alder lake 平台上存在的 EMMC 主机控制器新增驱动
  * 为 SAM4E MCU 系列上存在的 Atmel HSMCI 控制器新增驱动

* 传感器

  * 重构 :dtcompatible:`ti,bq274xx` 以添加 ``BQ27427`` 支持，
    修复
    容量
    和
    功率
    通道
    的
    单位。
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

  * NS16550：
    重新
    设计
    设备
    初始化
    宏
    的方式。

    * ``CONFIG_UART_NS16550_ACCESS_IOPORT`` 和 ``CONFIG_UART_NS16550_SIMULT_ACCESS``
      被移除。对于使用 IO 端口访问的 UART，
      在
      设备
      树
      节点
      中添加
      ``io-mapped``
      属性。

  * 为 ESP32S3 新增异步支持。

  * 为 ``native_posix`` 下的串行 TTY 新增支持。

  * 为 Efinix Sapphire SoCs 上的 UART 新增支持。

  * 新增 Intel SEDI UART 驱动。

  * 为 BCM2711 上的 UART 新增支持。

  * ``uart_stm32``：

    * 新增 RS485 支持。

    * 新增宽数据支持。

  * ``uart_pl011``：
    为
    Ambiq
    SoCs
    新增
    支持。

  * ``serial_test``：
    为
    中断
    和
    异步
    API
    新增
    支持。

  * ``uart_emul``：
    为
    中断
    API
    新增
    支持。

  * ``uart_rpi_pico``：
    修复
    Modbus
    DE-RE
    信号
    处理

* SPI

  * 移除
    由
    Flash
    Interface
    Unit
    （
    FIU
    ）
    模块
    实现
    的
    npcx
    spi
    驱动。
  * 为 Raspberry Pi Pico PIO 基于 SPI 新增支持。

* 定时器

  * TI CC13xx/26xx 系统时钟定时器
    compatible
    从
    :dtcompatible:`ti,cc13xx-cc26xx-rtc`
    更改为
    :dtcompatible:`ti,cc13xx-cc26xx-rtc-timer`，
    相应的
    Kconfig
    选项
    从
    :kconfig:option:`CC13X2_CC26X2_RTC_TIMER`
    更改为
    :kconfig:option:`CC13XX_CC26XX_RTC_TIMER`
    以
    改进
    一致性
    和
    可扩展性。
    除非
    修改
    了
    内部
    定时器，
    否则
    无需
    采取
    任何
    操作。

* USB

  * 为基于 STM32 的 MCU 新增 UDC 驱动，
    依赖于
    HAL/PCD。
    此
    驱动
    与
    UDC
    API
    （
    实验性
    ）
    兼容。
  * 为 USB 驱动中的 STM32H5 系列新增支持。

* WiFi

  * 增加
    esp32
    默认
    网络
    （
    TCP
    workq
    、
    RX
    和
    mgmt
    事件
    ）
    栈
    大小
    到
    2048
    字节。
  * 减少
    Wi-Fi
    示例
    中
    esp32s2_saola
    的
    RAM
    使用。
  * 修复
    winc1500
    中
    的
    未
    定义
    声明。
  * 修复
    eswifi
    中
    的
    SPI
    缓冲区
    长度。
  * 修复
    AP
    模式
    中
    esp32
    数据
    发送
    和
    通道
    选择。
  * 修复
    esp_at
    驱动
    初始化
    和
    网络
    接口
    休眠
    状态
    设置。