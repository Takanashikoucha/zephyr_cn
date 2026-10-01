:orphan:

.. _zephyr_3.3:

Zephyr 3.3.0
############

我们很高兴地宣布 Zephyr 版本 3.3.0 的发布。

本次发布的主要增强功能包括：

* 引入了 :ref:`Fuel Gauge <fuel_gauge_api>` 子系统，用于电池电量
  监控。
* 引入了 :ref:`USB-C <usbc_api>` 设备栈，支持 PD（电源传输）。
* 引入了 :ref:`DSP（数字信号处理）<zdsp_api>` 子系统，
  以 CMSIS-DSP 作为默认后端。
* 使用 Zephyr SDK 时，所有架构均支持 Picolibc。

以下各节按组件提供详细的变更列表。

安全漏洞相关
******************************

本次发布解决了以下 CVE：

更详细的信息可参见：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* CVE-2023-0359：截至 2023-04-20 处于保密期

* CVE-2023-0779：截至 2023-04-22 处于保密期


API 变更
***********

* 仿真器创建 API 已更改，以更好地匹配
  :c:macro:`DEVICE_DT_DEFINE`。
  它还包括一个新的后端 API 指针，
  以允许传感器共享通用 API，用于更通用的测试。

本次发布中的变更
=======================

* 选择 :kconfig:option:`CONFIG_NEWLIB_LIBC` 时，
  不再默认选择 Newlib nano 变体。
  现在必须显式选择 :kconfig:option:`CONFIG_NEWLIB_LIBC_NANO`
  才能使用 nano 变体。

* 蓝牙：为 bt_le_per_adv_sync_transfer_subscribe 新增额外选项，
  以允许禁用同步报告，并启用同步报告过滤。
  这两个选项是互斥的。

* 蓝牙：新增 :kconfig:option:`CONFIG_BT_PER_ADV_SYNC_TRANSFER_RECEIVER`
  和 :kconfig:option:`CONFIG_BT_PER_ADV_SYNC_TRANSFER_SENDER`，
  以启用 PAST 实现，而不是
  :kconfig:option:`CONFIG_BT_CONN`。
* Flashdisk：:kconfig:option:`CONFIG_DISK_FLASH_VOLUME_NAME`、
  :kconfig:option:`CONFIG_DISK_FLASH_DEV_NAME`、
  :kconfig:option:`CONFIG_DISK_FLASH_START`、
  :kconfig:option:`CONFIG_DISK_FLASH_MAX_RW_SIZE`、
  :kconfig:option:`CONFIG_DISK_ERASE_BLOCK_SIZE`、
  :kconfig:option:`CONFIG_DISK_FLASH_ERASE_ALIGNMENT`、
  :kconfig:option:`CONFIG_DISK_VOLUME_SIZE` 和
  :kconfig:option:`CONFIG_DISK_FLASH_SECTOR_SIZE` Kconfig 选项已移除，
  建议改用新的 :dtcompatible:`zephyr,flash-disk` 设备树绑定。

* 之前位于 ``<zephyr/drivers/regulator/consumer.h>`` 中的
  调节器 API 现在是 ``<zephyr/drivers/regulator.h>`` 的一部分。

* 从本次发布开始，将不再创建带 ``zephyr-`` 前缀的标签。
  该项目将继续使用 ``v`` 标签，例如 ``v3.3.0``。

* 蓝牙：弃用蓝牙日志子系统，建议改用 Zephyr
  标准日志系统。要为蓝牙子系统中的特定模块启用调试，
  请启用 `CONFIG_BT_(模块名)_LOG_LEVEL_DBG`，
  而不是 `CONFIG_BT_DEBUG_(模块名)`。

* MCUmgr img_mgmt 现在要求在上传映像时
  使用完整的 sha256 哈希来跟踪进度，
  其中 sha256 哈希是被上传整个文件的哈希
  （与获取映像状态时使用的哈希不同）。
  使用截断的哈希或非 sha256 哈希仍然有效，
  但会导致客户端软件出现问题
  和 Zephyr/MCUmgr 未来更新（如映像验证）中的故障。

* MCUmgr 处理程序不再需要由应用代码注册，
  处理程序只需使用一个定义，该定义将在启动时
  调用提供的注册函数。如果应用注册了它，
  则应移除这些注册，以防止多次注册
  相同的处理程序。

* MCUmgr 蓝牙和 UDP 传输不再需要由
  应用代码注册，这些现在将在启动时
  自动注册（此功能可以通过设置
  :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_UDP_AUTOMATIC_INIT`
  为 UDP 传输禁用）。
  如果应用注册了传输，则应移除这些注册，
  以防止多次注册相同的传输。

* MCUmgr 传输 Kconfig 已从 ``select`` 更改为 ``depends on``，
  这意味着对于使用蓝牙传输的应用，
  现在需要启用以下内容：

  * :kconfig:option:`CONFIG_BT`
  * :kconfig:option:`CONFIG_BT_PERIPHERAL`

  对于 CDC 或串行传输：

  * :kconfig:option:`CONFIG_CONSOLE`

  对于 shell 传输：

  * :kconfig:option:`CONFIG_SHELL`
  * :kconfig:option:`CONFIG_SHELL_BACKEND_SERIAL`

  对于 UDP 传输：

  * :kconfig:option:`CONFIG_NETWORKING`
  * :kconfig:option:`CONFIG_NET_UDP`

* MCUmgr fs_mgmt 哈希/校验和函数、类型和变量名
  已更改为带 ``fs_mgmt_`` 前缀，
  以与其他 zephyr 和 MCUmgr API 保持一致。

* Zephyr 脚本中 Python 的 argparse 参数解析器用法
  已更新为禁用缩写，
  任何未来的 python 脚本或 python 代码更新
  都必须通过使用 ``allow_abbrev=False``
  来禁用允许缩写
  当设置 ``ArgumentParser()`` 时。

  如果树外脚本或命令依赖于
  其之前的行为，这可能会导致其失败，
  这些需要更新才能使
  构建工作。例如，如果脚本参数有 ``--reset-type``
  并且树外脚本通过传递 ``--reset`` 使用它，
  则需要更新为使用完整的参数名， ``--reset-type``。

* 重写 CAN API 以利用标志位域，
  而不是离散的结构体成员
  用于指示标准/扩展 CAN ID、远程传输请求
  （RTR），并新增对 CAN-FD 格式帧过滤的支持。

* 新增 :ref:`Zephyr 消息总线（Zbus）<zbus>` 子系统；
  一个面向消息的总线，
  启用线程之间一对一、一对多和多对多通信。

* zTest 现在支持通过
  :kconfig:option:`CONFIG_ZTEST_SUMMARY` 控制测试摘要打印。
  此 Kconfig 可设置为 ``n`` 以获得
  更简洁的测试输出。

* 仿真器现在支持后端 API 指针，
  允许单一类设备提供类似的仿真功能。
  这可用于为设备类编写单个测试，
  并使用不同芯片测试各种板级。

本次发布中移除的 API
============================

* 移除 :kconfig:option:`CONFIG_COUNTER_RTC_STM32_LSE_DRIVE*`
  现在应使用 LSE 时钟的 ``driving_capability`` 属性
  配置它

* 移除 :kconfig:option:`CONFIG_COUNTER_RTC_STM32_LSE_BYPASS`
  现在应使用 LSE 时钟的新 ``lse_bypass`` 属性
  配置它

* 移除 :kconfig:option:`CONFIG_COUNTER_RTC_STM32_BACKUP_DOMAIN_RESET`。
  其目的是控制板级复位时计数器值的复位。
  它已被移除，因为其范围太广
  （完整的备份 RAM 复位）。
  由 :kconfig:option:`CONFIG_COUNTER_RTC_STM32_SAVE_VALUE_BETWEEN_RESETS` 替换，
  该选项也允许控制计数器值的复位，
  但逻辑相反。

* 移除已弃用的 tinycbor 模块，
  使用此模块的代码应更新为
  使用 zcbor 作为替代。

* 移除已弃用的 GPIO 标志，
  用于设置去抖动、驱动强度和电压电平。
  所有驱动现在根据需要使用供应商特定标志。

* 移除已弃用的 ``UTIL_LISTIFY`` 辅助宏。

* 从 PWM API 移除已弃用的 ``pwm_pin*`` 函数族。

* 从 NVS 文件系统 API 移除已弃用的 ``nvs_init`` 函数。

* 移除已弃用的 ``DT_CHOSEN_*_LABEL`` 辅助宏。

* 从 :dtcompatible:`st,stm32-usb` 移除已弃用的属性 ``enable-pin-remap``。
  现在应使用 :dtcompatible:`st-stm32-pinctrl` 的 ``remap-pa11-pa12``。

本次发布中弃用
==========================

* ``xtools`` 工具链变体现在已弃用。
  当使用使用 Crosstool-NG 构建的
  自定义工具链时，
  应改用 :ref:`交叉编译工具链变体 <other_x_compilers>`。

* C++ 库 Kconfig 选项已重命名，
  以改进一致性。
  有关已弃用的 Kconfig 选项及其替换项的列表，
  请参见下文：

  .. table::
     :align: center

     +----------------------------------------+------------------------------------------------+
     | 已弃用                             | 替换项                                    |
     +========================================+================================================+
     | CONFIG_LIB_CPLUSPLUS                     | CONFIG_CPP                                  |
     +----------------------------------------+------------------------------------------------+
     | CONFIG_LIB_CPLUSPLUS_NEW                 | CONFIG_CPP_NEW                              |
     +----------------------------------------+------------------------------------------------+
     | CONFIG_LIB_CPLUSPLUS_NEWALLOC            | CONFIG_CPP_NEWALLOC                         |
     +----------------------------------------+------------------------------------------------+

* MCUmgr 子系统，特别是 SMP 传输 API，
  正在弃用 `zephyr_` 前缀，
  弃用带前缀的函数和回调类型定义，
  并将其替换为无前缀的变体。
  表示传输对象的 :c:struct:`zephyr_smp_transport` 类型
  现在已被 :c:struct:`smp_transport` 替换，
  后者被所有无前缀函数使用，
  而不是前者。

  已弃用的函数及其替换项：

  .. table::
     :align: center

     +-------------------------------------+---------------------------------------+
     | 已弃用                          | 直接替换项                   |
     +=====================================+=======================================+
     | :c:func:`zephyr_smp_transport_init` | :c:func:`smp_transport_init`          |
     +-------------------------------------+---------------------------------------+
     | :c:func:`zephyr_smp_rx_req`         | :c:func:`smp_rx_req`                  |
     +-------------------------------------+---------------------------------------+
     | :c:func:`zephyr_smp_alloc_rsp`      | :c:func:`smp_alloc_rsp`               |
     +-------------------------------------+---------------------------------------+
     | :c:func:`zephyr_smp_free_buf`       | :c:func:`smp_free_buf`                |
     +-------------------------------------+---------------------------------------+

  已弃用的回调类型及其替换项：

  .. table::
     :align: center

     +---------------------------------------------+---------------------------------------+
     | 已弃用                                  | 直接替换项                   |
     +=============================================+=======================================+
     | :c:func:`zephyr_smp_transport_out_fn`       | :c:func:`smp_transport_out_fn`        |
     +---------------------------------------------+---------------------------------------+
     | :c:func:`zephyr_smp_transport_get_mtu_fn`   | :c:func:`smp_transport_get_mtu_fn`    |
     +---------------------------------------------+---------------------------------------+
     | :c:func:`zephyr_smp_transport_ud_copy_fn`   | :c:func:`smp_transport_ud_copy_fn`    |
     +---------------------------------------------+---------------------------------------+
     | :c:func:`zephyr_smp_transport_ud_free_fn`   | :c:func:`smp_transport_ud_free_fn`    |
     +---------------------------------------------+---------------------------------------+

  注意：仅函数被标记为 ``__deprecated``，
  类型定义则没有。

* STM32 以太网 MAC 地址 Kconfig 相关符号
  （:kconfig:option:`CONFIG_ETH_STM32_HAL_RANDOM_MAC`、
  :kconfig:option:`CONFIG_ETH_STM32_HAL_MAC4`、...）
  已弃用，建议改用 zephyr 通用设备树
  ``local-mac-address`` 和 ``zephyr,random-mac-address`` 属性。

* STM32 RTC 源时钟现在应使用设备树配置。
  相关的 Kconfig :kconfig:option:`CONFIG_COUNTER_RTC_STM32_CLOCK_LSI` 和
  :kconfig:option:`CONFIG_COUNTER_RTC_STM32_CLOCK_LSE` 选项现在
  已弃用。

* STM32 中断控制器 Kconfig 符号，
  例如 :kconfig:option:`CONFIG_EXTI_STM32_EXTI0_IRQ_PRI`，
  已被移除。相关的 IRQ 优先级现在应在设备树中配置。

* `PWM_STM32_COMPLEMENTARY` 已弃用，
  建议改用 `STM32_PWM_COMPLEMENTARY`。

* 设置 API 的文件后端和 Kconfig 选项已弃用：

  :c:func:`settings_mount_fs_backend` 建议改用 :c:func:`settings_mount_file_backend`

  :kconfig:option:`CONFIG_SETTINGS_FS` 建议改用 :kconfig:option:`CONFIG_SETTINGS_FILE`

  :kconfig:option:`CONFIG_SETTINGS_FS_DIR` 建议改用从
  :kconfig:option:`CONFIG_SETTINGS_FILE_PATH` 创建所有父目录

  :kconfig:option:`CONFIG_SETTINGS_FS_FILE` 建议改用 :kconfig:option:`CONFIG_SETTINGS_FILE_PATH`

  :kconfig:option:`CONFIG_SETTINGS_FS_MAX_LINES` 建议改用 :kconfig:option:`CONFIG_SETTINGS_FILE_MAX_LINES`

* PCIe API :c:func:`pcie_probe` 和 :c:func:`pcie_bdf_lookup` 已弃用，
  建议改用对可用 PCIe 设备的集中扫描。

* POSIX API

    * 弃用 :c:macro:`PTHREAD_COND_DEFINE`、:c:macro:`PTHREAD_MUTEX_DEFINE`，
      建议改用标准的 :c:macro:`PTHREAD_COND_INITIALIZER` 和
      :c:macro:`PTHREAD_MUTEX_INITIALIZER`。
    * 在 minimal libc 中弃用 ``<fcntl.h>``、``<sys/stat.h>`` 头文件，
      建议改用 ``<zephyr/posix/fcntl.h>`` 和 ``<zephyr/posix/sys/stat.h>``。

* SPI DT :c:func:`spi_is_ready` 函数已弃用，
  建议改用 :c:func:`spi_is_ready_dt`。

* 使用字符串引用作为 LwM2M 路径的 LwM2M API 已弃用，
  建议改用使用 :c:struct:`lwm2m_path_obj` 的函数。

本次发布中的稳定 API 变更
==================================

* MCUmgr 事件已重新设计，
  以使用单一、统一的回调系统。
  这允许以较小的闪存大小更好地定制回调。
  使用现有回调系统的应用需要升级
  以使用新 API，
  请遵循 :ref:`迁移指南 <mcumgr_cb_migration>`

* :c:func:`net_pkt_get_frag`、:c:func:`net_pkt_get_reserve_tx_data` 和
  :c:func:`net_pkt_get_reserve_rx_data` 函数现在要求
  指定要分配的最小分片长度，
  以便它们在启用 :kconfig:option:`CONFIG_NET_BUF_VARIABLE_DATA_SIZE`
  的情况下也能正确工作。
  使用这些 API 的应用需要更新
  以提供预期的分片长度。

* 将控制器局域网（CAN）控制器驱动 API 标记为稳定。

本次发布中的新 API
========================

内核
******

* 新增 "EARLY" 初始化级别，
  在 z_cstart() 入口处立即运行

* 重构内部 CPU 计数 API，
  以允许运行时更改

* 新增支持在 C++ 代码中定义应用 main()

* 修复 SMP 上的竞态条件，
  当挂起线程时，
  第二个 CPU 可能在挂起线程完成
  上下文切换之前尝试运行该线程。

架构
*************

* ARC

  * 修复并重新设计 SMP 系统的中断管理
    （启用/禁用）
  * 为 ARC MWDT 工具链新增 TLS（线程本地存储）
  * 修复并重新设计 irq_offload 实现
  * 修复 ARCv3 64 位的多个日志和 cbprintf 问题
  * 为 MWDT 工具链新增 XIP 支持
  * 改进 DSP 支持，
    新增 DSP 和 AGU 上下文保存/恢复
  * 为 ARC DSP 目标新增 XY 内存支持
  * 新增架构特定的 DSP 测试
  * 为不支持的配置新增额外的编译时检查：
    ARC_FIRQ + ARC_HAS_SECURE
  * 为 ARC MWDT 工具链新增使用 ``__auto_type`` 类型的支持
  * 为 ARC MWDT 工具链新增使用 ``_Generic`` 和 ``__fallthrough`` 关键字的支持
  * 将 ARC MWDT 最低版本提升到 2022.09
  * 修复并重新设计 ARC MWDT 工具链的 C/C++ 头文件包含，
    该问题导致了 C++ 构建问题

* ARM

  * 故障处理程序现在返回更精确的 "reason" 代码。
  * 缓存函数现在使用适当的 ``sys_*`` 函数。
  * 将默认 RAM 区域从 ``SRAM`` 重命名为 ``RAM``。

* ARM64

  * 为 ARM64 MMU 实现 ASID 支持

* RISC-V

  * 将 :kconfig:option:`CONFIG_MP_NUM_CPUS` 转换为
    :kconfig:option:`CONFIG_MP_MAX_NUM_CPUS`。

  * 新增在 ISR 和异常期间
    硬件寄存器压栈/出栈的支持。

  * 新增覆盖 :c:func:`arch_irq_lock`、
    :c:func:`arch_irq_unlock` 和 :c:func:`arch_irq_unlocked` 的支持。

  * Zephyr CPU 编号现在与 hart ID 解耦。

  * 当 :kconfig:option:`CONFIG_MP_MAX_NUM_CPUS` 等于 ``1`` 时，
    不再包含二级引导代码。

  * IPI 不再硬编码为 :c:func:`z_sched_ipi`。

  * 为线程 FPU 访问
    实现按需上下文切换算法。

  * 通过 :kconfig:option:`CONFIG_RV_BOOT_HART`
    启用从非零索引的 RISC-V hart 引导。

  * Hart ID 现在通过设备树映射到 Zephyr CPU。

  * 为 ``MTVAL`` 在基于 QEMU 的平台上
    未正确更新新增变通方法。

蓝牙
*********

* 音频

  * 重构 BAP 广播源中扩展和周期性广播的处理。
  * 实现通用音频配置（CAP）发起方角色。
  * 新增对广播源子组和 BIS 编解码器配置的支持。
  * 将 CSI 和 VCP 功能重命名为使用 "P" 后缀
    表示配置，而不是使用 "S" 表示服务。
  * 新增广播源元数据更新函数。
  * 新增音频 ISO 结构体与音频流的（解）绑定。
  * 新增对加密广播的支持。
  * 新增更改 PACS 中支持上下文的能力。
  * 改进作为单播客户端的 CIS 的流耦合
  * 新增广播源元数据更新函数
  * 为单播组创建新增打包
  * 为广播源新增打包字段
  * 将 BASS 和 BASS 客户端重命名为
    BAP 扫描委托方和 BPA 广播助手
  * 新增对 BAP 广播接收端多个子组的支持
  * 用 PACS 替换 capabilities API

* 主机

  * 新增 ``BT_CONN_INTERVAL_TO_US`` 工具宏。
  * 将 HCI 分片逻辑改为异步，
    从而修复了数据和控制过程之间
    长期存在的潜在死锁。
  * 将本地广播地址添加到 :c:func:`bt_le_ext_adv_get_info`。
  * 改进 :c:func:`bt_disable` 的实现，
    以处理额外的边缘情况。
  * 移除所有蓝牙特定的日志宏和功能，
    改用操作系统范围的日志。
  * 新增 :c:func:`bt_le_per_adv_sync_lookup_index` 函数。
  * 修复删除周期性广播同步对象时
    对 bt_le_per_adv_sync_cb.term 的缺失调用。
  * 将本地广播地址添加到 bt_le_ext_adv_info。
  * 新增默认在日志中打印函数名。
  * 更改断开连接后广播重启的策略，
    现在仅针对外围设备角色的连接执行。
  * 新增保护，防止与同一设备绑定多次。
  * 将加密功能从 SMP 重构到其自己的文件夹，
    并新增 h8 加密函数。
  * 更改接收大于 MPS 的 L2CAP K 帧时的行为，
    断开连接而不是截断它。
  * 新增 :kconfig:option:`BT_ID_ALLOW_UNAUTH_OVERWRITE`，
    允许多身份下未授权的绑定覆盖。
  * 新增对 OTS 中对象计算校验和功能的支持。
  * 将 :kconfig:option:`BT_PRIVACY` 的语义改回
    指本地 RPA 地址生成。
  * 修改配对过程之外的 SMP 行为。
    栈在该状态下不再发送不必要的
    配对失败 PDU。

  * ISO：将 ISO seq_num 更改为 16 位

* Mesh

  * 将默认广播器更改为扩展广播器。
  * 使配置功能集动态化。
  * 使 mesh 栈可使用的
    最大同时蓝牙连接数
    可通过 :kconfig:option:`BT_MESH_MAX_CONN` 配置。
  * 更改广播持续时间计算，
    以避免不精确的估算。
  * 新增 :kconfig:option:`BT_MESH_FRIEND_ADV_LATENCY` Kconfig 选项。

* 控制器

  * 实现读/写连接接受超时 HCI 命令。
  * 实现睡眠时钟精度更新过程。
  * 实现额外的 ISO 相关 HCI 命令。
  * 实现 ISO-AL SDU 缓冲和 PDU 释放超时。
  * 新增处理不带 PDU 链接的分片 AD 的支持。
  * 新增对广播 PDU 的多个内存池的支持
  * 新增重试自动外围设备连接参数更新的支持。
  * 新增使用外部钩子延迟锚点移动的支持。
  * 新增用于详细断言的 ``LL_ASSERT_MSG`` 宏。
  * 新增长控制 PDU 支持。
  * 新增对广播 ISO 加密的支持。
  * 新增对中心 CIS/CIG 的支持，
    包括 ULL 和 Nordic LLL。
  * 新增在 Nordic LLL 中
    外围设备 CIS/CIG 的支持。
  * 新增 :kconfig:option:`BT_CTLR_SLOT_RESERVATION_UPDATE` Kconfig 选项。
  * 为 ISO 广播集成 ISOAL。

板级与 SoC 支持
********************

* 新增对这些 SoC 系列的支持：

  * Atmel SAMC20、SAMC21
  * Atmel SAME70Q19
  * GigaDevice GD32L23X
  * GigaDevice GD32A50X
  * NXP S32Z2/E2

* 在其他 SoC 系列中进行了以下更改：

  * STM32F1：USB 预分频器配置
    现在应使用 :dtcompatible:`st,stm32f1-pll-clock` 的 ``usbpre``
    或 :dtcompatible:`st,stm32f105-pll-clock` 的 ``otgfspre`` 属性
    完成。
  * STM32F7/L4：现在支持配置 MCO。
  * STM32G0：现在支持 FDCAN
  * STM32G4：现在支持电源管理
    （STOP0 和 STOP1 低功耗模式）。
  * STM32H7：现在支持 PLL2、USB OTG HS 和 ULPI PHY。
  * STM32L5：现在支持基于 RTC 的 :ref:`counter_api`。
  * STM32U5：现在支持通过 AES 设备的 :ref:`crypto_api`。
  * STM32F7/L4：现在支持配置 MCO。

* ARC 板级的更改：

  * 对 ``mdb-hw`` 和 ``mdb-nsim`` west runner 的
    多个修复，以改进可用性
  * 新增具有 DSP 功能的 ``nsim_em11d`` 板级
    （具有 AGU 和 XY 内存的 XY DSP）
  * 修复 HSDK 板级上 cy8c95xx I2C GPIO 端口初始化
  * 为 EM starter kit 板级新增 SPI 闪存支持
  * 对 nSIM 平台的多个修复 - 配置：
    添加缺失的 HW 功能或配置同步
  * 改进 creg_gpio 平台驱动 - 新增 pin_configure API
  * 为 XIP 测试新增单独的 QEMU 配置 ``qemu_arc_hs_xip``
  * 新增 ``nsim_hs_sram``、``nsim_hs_flash_xip`` nSIM 平台，
    以验证各种内存模型
  * 全面修订 nSIM 板级文档

* 新增对这些 ARM 板级的支持：

  * Adafruit ItsyBitsy nRF52840 Express
  * Adafruit KB2040
  * Atmel atsamc21n_xpro
  * GigaDevice GD32L233R-EVAL
  * GigaDevice GD32A503V-EVAL
  * nRF5340 Audio DK
  * Sparkfun pro micro RP2040
  * Arduino Portenta H7
  * SECO JUNO SBC-D23（STM32F302）
  * ST Nucleo G070RB
  * ST Nucleo L4A6ZG
  * NXP X-S32Z27X-DC（DC2）

* 新增对这些 ARM64 板级的支持：

  * i.MX93（Cortex-A）EVK 板级
  * Khadas Edge-V 板级
  * QEMU Virt KVM

* 新增对这些 X86 板级的支持：

  * Intel Raptor Lake CRB

* 新增对这些 RISC-V 板级的支持：

  * 为 ``longan_nano`` 板级新增 LCD 支持。

* 在 ARM 板级中进行了以下更改：

  * sam4s_xplained：启用 PWM
  * sam_e70_xplained：为 SPI 新增 DMA 设备树条目
  * sam_v71_xult：为 SPI 新增 DMA 设备树条目
  * tdk_robokit1：为 SPI 新增 DMA 设备树条目

  * 已移除以下 Nordic 板级的 scratch 分区，
    并将该区域使用的闪存重新分配给其他分区，
    以释放空间并依赖 MCUboot 中的
    swap-using-move 算法
    （该算法不会受到与 swap-using-scratch
    相同的故障或映像卡住问题的影响）：
    ``nrf21540dk_nrf52840``
    ``nrf51dk_nrf51422``
    ``nrf51dongle_nrf51422``
    ``nrf52833dk_nrf52833``
    ``nrf52840dk_nrf52811``
    ``nrf52840dk_nrf52840``
    ``nrf52840dongle_nrf52840``
    ``nrf52dk_nrf52805``
    ``nrf52dk_nrf52810``
    ``nrf52dk_nrf52832``
    ``nrf5340dk_nrf5340``
    ``nrf9160dk_nrf52840``
    ``nrf9160dk_nrf9160``

    请注意，Zephyr 3.3 之前的 MCUboot 和 MCUboot 映像更新
    可能与 Zephyr 3.3 及之后的版本不兼容，
    反之亦然。

  * ``nrf52840dongle_nrf52840`` 板级的默认控制台
    已从物理 UART（该板级上未连接到任何设备）
    更改为使用 USB CDC。
  * 已从以下板级移除强制配置 FPU：
    ``stm32373c_eval``
    ``stm32f3_disco``

  * 在 STM32 板级上，
    通常期望 48MHz 时钟的 USB、SDMMC 和熵设备配置
    现在使用设备树完成。
    当可用时，启用 HSI48 并将其配置为
    这些设备的域时钟，
    否则使用 PLL_Q 输出或 MSI。
    在某些板级上，
    之前的 PLL SAI 配置已更改为上述选项，
    因为 PLL SAI 还不能使用设备树配置。

* 在其他板级中进行了以下更改：

  * nrf52_bsim（原生仿真的 nRF52 设备，
    带有 BabbleSim）
    现在模拟 nRF52833，
    而不是 nRF52832 设备

* 新增对以下扩展板的支持：

  * Adafruit PCA9685
  * nPM6001 EK
  * nPM1100 EK
  * Semtech SX1262MB2DAS
  * Sparkfun MAX3421E

构建与基础设施
*******************************

* 代码重定位

  * ``zephyr_code_relocate`` API 已更改，
    以接受要重定位的文件列表
    和放置文件的位置。

* Sysbuild

  * 修复了重复的 sysbuild 映像名称
    导致无限 cmake 循环的问题。

  * 修复了板级修订版本
    未传递给 sysbuild 映像的问题。

  * sysbuild 控制映像的应用特定配置。

* 用户空间

  * 新增用户空间选项，
    用于禁用使用 ``relax`` 链接器选项。

* 工具

  * 新增静态代码分析器（SCA）工具支持。

驱动与传感器
*******************

* ADC

  * STM32：现在支持将多个通道
    顺序化为单个读取。
  * 修复 :c:macro:`ADC_CHANNEL_CFG_DT` 中的问题，
    该问题强制用户在与使用
    可配置模拟输入的 ADC 驱动一起使用
    不使用此类输入配置的 ADC 驱动相关节点中
    添加人为的 ``input-positive`` 属性。
  * 新增 TI CC13xx/CC26xx 系列的驱动。
  * 新增 Infineon XMC4xxx 系列的驱动。
  * 新增 ESP32 SoC 的驱动。

* 电池备份 RAM

  * STM32：新增驱动，
    以启用对来自 RTC 的备份寄存器的支持。

* CAN

  * 新增 RX 溢出计数器统计支持
    （STM32 bxCAN、Renesas R-Car 和 NXP FlexCAN）。
  * 新增对 ESP32-C3 上 TWAI 的支持。
  * 新增对多个 MCP2515 驱动实例的支持。
  * 新增 Kvaser PCIcan 驱动
    以及在 QEMU 下使用它的支持。
  * 使伪 CAN 测试驱动普遍可用。
  * 新增支持将 Native Posix Linux CAN 驱动
    编译到 v5.14 之前的 Linux 内核头文件。
  * 移除 CONFIG_CAN_HAS_RX_TIMESTAMP 和
    CONFIG_CAN_HAS_CANFD Kconfig 辅助符号。

* 时钟控制

  * STM32：HSI48 现在可以使用设备树配置。

* 计数器

  * STM32 基于 RTC 的计数器域时钟（LSE/SLI）
    现在应使用设备树配置。
  * 为 GigaDevice GD32 SoC 新增基于定时器的驱动。
  * 新增 NXP S32 系统定时器模块驱动。

* DAC

  * 新增对 GigaDevice GD32 SoC 的支持。
  * 新增对 Espressif ESP32 SoC 的支持。

* DFU

  * 移除 :c:macro:`BOOT_TRAILER_IMG_STATUS_OFFS`，
    建议改用两个新函数；
    :c:func:`boot_get_area_trailer_status_offset` 和
    :c:func:`boot_get_trailer_status_offset`

* 磁盘

  * STM32 SD 主机控制器时钟
    现在通过设备树配置。
  * Zephyr 闪存磁盘现在使用
    :dtcompatible:`zephyr,flash-disk` 设备树绑定
    配置
  * 通过在链接的闪存设备分区上
    设置 ``read-only`` 属性，
    可以将闪存磁盘标记为只读。

* DMA

  * 调整 GD32 gd32vf103 SoC 的
    不正确的 dma1 时钟源。
  * Atmel SAM：新增支持，
    用于在使用外设到内存
    或内存到外设传输时
    选择固定或递增地址模式。
  * STM32 DMA 变量作用域清理
  * Intel GPDMA 链接列表传输描述符
    适当对齐到 64 字节地址
  * Intel GPDMA 修复传输配置中的 bug，
    以初始化 cfg_hi 和 cfg_lo
  * STM32 DMA 对 STM32MP1 系列的支持
  * SAM XDMAC 修复，
    以启用与 SPI DMA 传输一起使用
  * Intel GPDMA 修复，
    以便在 dma stop 时返回错误
  * Intel GPDMA 在不需要时禁用中断
  * Intel GPDMA 修复寄存器/ip 所有权
  * STM32U5 GPDMA 修复忙标志 bug
  * STM32U5 新增挂起和恢复功能
  * Intel GPDMA 在 dma 状态中
    报告读取/写入的总字节数
    （线性链接位置）
  * 新增 DMA API get attribute 函数，
    为 Intel HDA 和 Intel GPDMA 驱动
    新增可用的散列/聚集块属性。
  * Intel GPDMA 新增电源管理功能
  * Intel HDA 新增电源管理功能
  * GD32 使用插槽选择外设
  * GD32 新增内存到内存支持
  * 新增 ESP32C3 GDMA 驱动
  * 新增 Intel HDA 欠载/过载（xrun）处理和报告
  * 新增 Intel GPDMA 欠载/过载（xrun）处理和报告
  * DMA API start/stop 被定义为可重复调用，
    并新增测试用例。
    STM32 DMA、Intel HDA 和 Intel GPDMA
    在补丁后都符合该约定。
  * 移除 NXP EDMA 未使用的互斥锁

* EEPROM

  * 为测试目的新增伪 EEPROM 驱动。

* 以太网

  * STM32：默认 MAC 地址配置
    现在基于 uid。
    可选地，用户可以使用设备树
    将其配置为随机或提供自己的地址。
  * STM32：在 F4/F7/H7 上
    新增对 STM32Cube HAL 以太网 API V2 的支持。
    默认禁用，
    可以通过 :kconfig:option:`CONFIG_ETH_STM32_HAL_API_V2` 启用。
  * STM32：在 STM32F107 设备上
    新增以太网支持。
  * STM32：现在支持
    MAC 中的多播哈希过滤。
    可以使用 :kconfig:option:`CONFIG_ETH_STM32_MULTICAST_FILTER` 启用。
  * STM32：现在支持
    通过 :kconfig:option:`CONFIG_NET_STATISTICS_ETHERNET`
    记录统计信息。
    需要使用 HAL 以太网 API V2。

* 闪存

  * 闪存：由于 flexspi 时钟初始化
    发生在 SOC 级别，
    将 CONFIG_FLASH_FLEXSPI_XIP
    移至 SOC 级别。

  * NRF：新增 CONFIG_SOC_FLASH_NRF_TIMEOUT_MULTIPLIER，
    用于调整闪存操作的超时时间。

  * spi_nor：为 Macronix MX25R* 超低功耗闪存设备
    在 jedec,spi-nor 绑定中
    新增属性 mxicy,mx25r-power-mode，
    用于控制低功耗/高性能模式。

  * spi_nor：新增检查闪存在初始化期间是否忙。这曾导致闪存设备在系统重启前不可用。该修复在继续之前等待闪存就绪。在重启前开始完整闪存擦除的情况下，这可能导致几分钟的等待时间（取决于闪存大小和擦除速度）。

  * rpi_pico：为 Raspberry Pi Pico 平台
    新增闪存驱动。

  * STM32 OSPI：sfdp-bfp 表和 jedec-id
    现在可以从设备树读取，
    并在需要时覆盖闪存内容。

  * STM32 OSPI：现在在 STM32U5 上
    支持 DMA 传输。

  * STM32：重新审视闪存驱动，
    以简化新系列的驱动复用，
    利用设备树 compatibles。

* FPGA

  * 为 Lattice iCE40
    新增初步支持。
  * 新增 Qomu 板级示例。

* GPIO

  * Atmel SAM：新增支持，
    用于配置开漏引脚
  * 新增 nPM6001 PMIC GPIO 的驱动
  * 新增 NXP S32 GPIO（SIUL2）驱动

* hwinfo

  * 为 ESP32-C3
    新增 hwinfo_get_device_id
  * 为 STM32H7 和 MP1
    为 iwdg 和 wwdg 新增复位原因

* I2C

  * SAM0 通过将停止条件
    从线程移到 ISR
    修复了虚假的尾部数据
  * I2C Shell 命令
    新增通过 `i2c speed`
    配置总线速度的能力
  * ITE 支持指令本地内存
  * NPCX 在事务超时时
    总线恢复
  * ITE 在传输失败时
    记录寄存器状态
  * ESP32 启用配置硬件超时，
    以考虑更长时间的时钟拉伸
  * ITE 修复 bug，
    该 bug 导致操作
    在驱动互斥锁之外执行
  * NRFX TWIM 使传输超时
    可配置
  * DW 修复初始化时
    清除 FIFO 的 bug
  * NPCX 简化 smb bank 寄存器使用
  * NXP LPI2C 启用目标模式
  * NXP FlexComm 为共享总线使用
    新增信号量
  * I2C 新增支持，
    用于在日志中
    转储所有事务、读取和写入的消息
  * STM32：从机配置
    现在支持 10 位寻址。
  * STM32：现在支持电源管理。
    支持 3 种模式：:kconfig:option:`CONFIG_PM`、
    :kconfig:option:`CONFIG_PM_DEVICE`、
    :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME`。
  * STM32：域时钟
    现在可以使用设备树配置

* I3C

  * 新增新的目标设备 API :c:func:`i3c_target_tx_write`，
    用于显式写入 TX FIFO。

  * 根据 I3C 规范，
  * GETMRL 和 GETMWL
    在 :c:func:`i3c_device_basic_info_get` 中
    都是可选的，
    因为 MRL 和 MWL 是可选的。

  * 新增新的驱动，
    用于支持 Cadence I3C 控制器。

* 中断控制器

  * STM32：驱动配置和初始化
    现在基于设备树
  * 新增 NXP S32 外部中断控制器（SIUL2）驱动。

* IPM

  * ipm_stm32_ipcc：修复问题，
    该问题导致中断掩码
    未正确清理，
    从而导致无限 TXF 中断。

* MBOX

  * 新增 NXP S32 消息接收单元（MRU）驱动。

* PCIE

  * 之前移除的对 I/O BAR 的访问支持
    已恢复。

  * 新增新的 API :c:func:`pcie_scan`，
    用于扫描设备。

    * 这将遍历
      预期存在的总线和设备。
      旧方法是尝试
      总线和设备的所有可能组合，
      以确定是否存在设备。
      :c:func:`pci_init` 和 :c:func:`pcie_bdf_lookup`
      已更新为使用此新 API。

    * :c:func:`pcie_scan` 还引入了
      发现新设备时的回调机制。

* 引脚控制

  * 通用引脚控制属性
    现在在单个文件的根级别定义：
    :zephyr_file:`dts/bindings/pinctrl/pincfg-node.yaml`。
    引脚控制绑定
    预期在需要的级别包含它。例如，使用分组表示方法的驱动需要在孙级别包含它，而使用节点方法的驱动需要在子级别包含它。此更改只会影响树外引脚控制驱动，因为所有树内驱动都已更新。
  * 新增 NXP S32 SIUL2 驱动
  * 新增 Nuvoton NuMicro 驱动
  * 新增 Silabs Gecko 驱动
  * 在 i.MX 驱动中
    新增对 i.MX93 的支持
  * 在 Gigadevice 驱动中
    新增对 GD32L23x/GD32A50x 的支持

* PWM

  * Atmel SAM：新增支持，
    用于选择引脚极性
  * 新增 NXP PCA9685 LED 控制器的驱动

* 调节器

  * 完成 API 全面修订，
    以支持 PMIC 等设备。
    API 现在提供清晰简洁的 API，
    允许执行以下操作：

      - 启用/禁用调节器输出
        （引用计数）
      - 列出支持的电压
      - 获取/设置工作电压
      - 获取/设置最大电流
      - 获取/设置工作模式
      - 获取错误，例如过电流。

    设备树部分
    保持与 Linux 绑定的兼容性，
    例如，
    以下属性得到很好的支持：

      - ``regulator-boot-on``
      - ``regulator-always-on``
      - ``regulator-min-microvolt``
      - ``regulator-max-microvolt``
      - ``regulator-min-microamp``
      - ``regulator-max-microamp``
      - ``regulator-allowed-modes``
      - ``regulator-initial-mode``

    通用驱动类层
    处理通用功能，
    以使驱动实现保持简洁。
    例如，
    在调用驱动之前
    验证允许的电压范围。

    还引入了
    用于配置 DVS（动态电压缩放）的
    实验性父 API。

  * 重构 NXP PCA9420 驱动，
    以与新 API 保持一致。
  * 新增对 nPM6001 PMIC 的支持
    （LDO 和 BUCK 转换器）。
  * 新增对 nPM1100 PMIC 的支持
    （允许动态更改其模式）。
  * 新增新的测试，
    允许使用 ADC API
    验证调节器输出电压。
  * 新增新的测试，
    检查 API 行为，
    假设我们有行为良好的驱动。

* 复位

  * STM32：STM32 复位驱动
    现在可用。
    设备复位线配置
    应使用设备树完成。

* SDHC

  * i.MX RT USDHC：

    - 支持 HS400 和 HS200 模式。
      该模式用于 eMMC 设备，
      并将为这些卡
      启用高速操作。
    - 在不支持非缓存内存的
      SoC（如 RT595）上
      支持 DMA 操作。
      DMA 将启用
      更高性能的 SD 模式，
      例如 HS400 和 SDR104，
      以可靠地使用
      SD 主机控制器传输数据

* 传感器

  * 重构所有驱动，
    以使用 :c:macro:`SENSOR_DEVICE_DT_INST_DEFINE`
    启用新的传感器信息可迭代部分
    和 shell 命令。
    参见 :kconfig:option:`CONFIG_SENSOR_INFO`。
  * 重构所有传感器设备树绑定，
    以继承 :zephyr_file:`dts/bindings/sensor/sensor-device.yaml`
    中的新基础传感器设备属性。
  * 为 shell 新增传感器属性支持。
  * 新增 ESP32 和 RaspberryPi Pico
    裸片温度传感器驱动。
  * 新增 TDK InvenSense ICM42688
    六轴 IMU 驱动。
  * 新增 TDK InvenSense ICP10125
    压力和温度传感器驱动。
  * 新增 AMS AS5600
    磁角度传感器驱动。
  * 新增 AMS AS621x
    温度传感器驱动。
  * 新增 HZ-Grow R502A
    指纹传感器驱动。
  * 增强 FXOS8700、FXAS21002 和 BMI270 驱动，
    以在 I2C 之外
    支持 SPI。
  * 增强 ST LIS2DW12 驱动，
    以支持自由落体检测。
  * rpi_pico：新增裸片温度传感器驱动。
  * 新增 STM32 系列
    正交解码器驱动。
    目前仅在 STM32F4 上启用。

* 串行

  * Atmel SAM：UART/USART：
    新增支持，
    用于在运行时配置驱动
  * STM32：DMA
    现在在 STM32U5 系列上
    受支持。

  * uart_altera_jtag：
    新增 Nios-V UART 支持。

  * uart_esp32：
    新增异步操作支持。

  * uart_gecko：
    新增 pinctrl 支持。

  * uart_mchp_xec：
    现在在 MEC15xx SoC 上
    支持 UART。

  * uart_mcux_flexcomm：
    新增运行时配置支持。

  * uart_mcux_lpuart：
    新增 RS-485 支持。

  * uart_numicro：
    使用 pinctrl
    配置 UART 引脚。

  * uart_pl011：
    新增 pinctrl 支持。

  * uart_rpi_pico：
    新增运行时配置支持。

  * uart_xmc4xxx：
    新增中断支持，
    因此现在可以
    由中断驱动。
    还新增 FIFO 支持。

  * 新增 UART 驱动：

    * Cadence IP6528 UART。

    * NXP S32 LINFlexD UART。

    * OpenTitan UART。

    * QuickLogic USBserialport_S3B。

* SPI

  * 为 GD32 驱动
    新增 dma 支持。
  * Atmel SAM：

    * 新增使用 DMA
      进行传输的支持。
    * 为测试目的
      新增回环模式支持。

  * 新增 NXP S32 SPI 驱动。

* 定时器

  * 修正使用 mtime 设备的
    SMP RISC-V 系统上的
    CPU 编号

  * 为 riscv_machine_timer
    新增对 OpenTitan 特权定时器设备的
    支持

  * 重构 SYS_CLOCK_EXISTS，
    使其始终与
    kconfig 中定时器设备的存在
    匹配

  * 对 nrf_rtc_timer
    进行大量重新设计，
    包括多个修复

  * 修复 stm32_lptim 驱动中的
    预分频器校正
    以及自动重载的竞态条件

* USB

  * STM32F1：
    时钟总线配置
    不再由驱动自动完成。
    用户有责任
    使用 clock_control 设备树节点
    配置适当的总线预分频器，
    以实现 48MHz 总线时钟。
    请注意，在大多数情况下，
    核心时钟为 72MHz，
    默认预分频器配置
    设置为实现 48MHz USB 总线时钟。
    仅当核心时钟
    已经为 48MHz 时，
    才需要手动配置预分频器。
  * STM32（非 F1）：
    时钟总线配置
    现在预期在设备树中
    使用 ``clocks`` 节点属性完成。
    当目标上有
    专用的 HSI 48MHz 时钟时，
    默认将其配置为
    USB 总线时钟，
    但用户可以选择
    另一个 48MHz 时钟源。
    当没有 HSI48 可用时，
    用户应配置
    特定的 48MHz 总线时钟源。
  * STM32：
    现在支持 :c:func:`usb_dc_detach`
    和 :c:func:`usb_dc_wakeup_request`。
  * STM32：Vbus 检测现在受支持，并根据设备树中硬件检测引脚的存在确定。例如：pinctrl-0 = <&usb_otg_fs_vbus_pa9 ...>;
  * RPi Pico：
    修复缓冲区状态处理，
    修复无限未处理 irq 重新触发，
    修复 DATA PID 切换
    和控制传输处理。
  * NXP：
    启用高速支持，
    修复端点缓冲区写操作。
  * nRF USBD：
    移除 detach 时的
    HAL 驱动 uninit，
    修复 USB 栈禁用时
    端点禁用。
  * 为 nRF USBD、Kinetis USBFSOTG
    和虚拟控制器
    新增新的实验性
    USB 设备控制器（UDC）API
    和实现
  * 为 MAX3421E 和虚拟控制器
    新增新的实验性
    USB 主机控制器（UDC）API
    和实现

* 看门狗

  * 为 nPM6001 PMIC
    新增看门狗驱动。
  * 为 GigaDevice GD32 SoC
    新增自由看门狗驱动。
  * 为 GigaDevice GD32 SoC
    新增窗口看门狗驱动。
  * 新增 NXP S32
    软件看门狗定时器驱动。

网络
**********

* CoAP：

  * 实现在任意位置
    插入 CoAP 选项。

* 以太网：

  * 修复以太网 L2 之上的
    AF_PACKET/SOCK_RAW/IPPROTO_RAW 套接字。
  * 新增使用 net shell
    设置以太网 MAC 地址的支持。
  * 新增检查，
    用于在启用以太网接口时
    检查驱动启动/停止例程的
    返回值。
  * 为具有未识别协议字段的
    数据包新增 ``unknown_protocol`` 统计，
    而不是为此目的
    使用 ``error``。
  * 新增 NXP S32 NETC
    以太网驱动。

* HTTP：

  * 重新设计 HTTP 头：
    将方法移至单独的头部，
    新增状态响应代码头部，
    并将 HTTP 头
    分组到子目录中。
  * 使用 :c:func:`zsock_poll`
    处理 HTTP 超时，
    而不是延迟工作。

* ICMPv4：

  * 新增支持，
    用于自动生成
    Echo Request 负载。

* ICMPv6：

  * 新增支持，
    用于自动生成
    Echo Request 负载。
  * 修复 ND 包的
    统计计数。

* IEEE802154：

  * 改进短地址支持。
  * 改进 IEEE802154
    上下文线程安全性。
  * 将 IEEE802154 参数
    从 :c:struct:`net_pkt`
    解耦到
    :c:struct:`net_pkt_cb_ieee802154`。
  * 多个其他小修复/改进。

* IPv4：

  * 新增 IPv4 包分片支持，
    这允许在发送之前
    拆分大包，
    或在接收期间
    重组大于
    网络设备 MTU 的包。
    这默认禁用，
    但可以通过
    :kconfig:option:`CONFIG_NET_IPV4_FRAGMENT`
    启用。
  * 新增设置/读取
    DSCP/ECN 字段的支持。
  * 修复 IPv4 地址
    自动配置过程中的
    包泄漏。
  * 新增使用 ``net ipv4`` shell 命令
    配置 IPv4 地址的支持。
  * Zephyr 现在默认
    将 IGMP 所有系统 224.0.0.1 地址
    添加到所有 IPv4 网络接口。

* IPv6：

  * 使能够
    将路由添加到
    路由器的链路本地地址。
  * 新增设置/读取
    DSCP/ECN 字段的支持。
  * 改进 IPv6 分片的
    测试覆盖范围。
  * 新增使用 ``net ipv6`` shell 命令
    配置 IPv6 地址的支持。
  * 新增使用 ``net route`` shell 命令
    配置 IPv6 路由的支持。

* LwM2M：

  * 将 ``LWM2M_RD_CLIENT_EVENT_REG_UPDATE_FAILURE``
    重命名为
    :c:macro:`LWM2M_RD_CLIENT_EVENT_REG_TIMEOUT`。
    该事件现在用于
    注册超时的情况。
  * 为 LwM2M 资源
    新增用于历史数据存储的
    新 LwM2M API。
  * 更新 LwM2M API，
    在可能的情况下
    使用 ``const`` 指针。
  * 新增 shell 命令，
    用于锁定/解锁
    LwM2M 注册表。
  * 新增 shell 命令，
    用于为资源
    启用历史数据缓存。
  * 切换到
    内部使用 ``zsock_*`` 函数。
  * 新增 uCIFI LPWAN（ID 3412）
    对象实现。
  * 新增 BinaryAppDataContainer（ID 19）
    对象实现。
  * 弃用 :kconfig:option:`CONFIG_LWM2M_RD_CLIENT_SUPPORT`，
    因为它现在被视为
    LwM2M 库的
    不可分割的一部分。
  * 新增对
    SenML 对象链接
    数据类型的支持。
  * 修复导致
    观察路径顺序
    不正确的 bug。
  * 弃用基于字符串的
    LwM2M API。
    LwM2M API 现在使用
    :c:struct:`lwm2m_obj_path`
    表示对象/资源路径。
  * 通过拆分特定功能
    到单独的模块
    重构 ``lwm2m_client`` 示例。
  * LwM2M 库中的
    多个其他小修复。

* 其他：

  * 更新各种网络测试套件，
    以使用新的 ztest API。
  * 为 ``big_http_download`` 示例
    新增重定向支持，
    并更新 TLS 变体的
    服务器 URL。
  * 修复 ``net udp`` shell 命令中的
    内存泄漏。
  * 修复 :c:struct:`net_pkt` 的
    LL 地址克隆。
  * 新增支持，
    用于在 ``net ping`` shell 命令中
    设置 QoS 和负载大小。
  * 新增支持，
    用于中止 ``net ping`` shell 命令。
  * 在网络接口上
    引入载波和休眠管理。
    将接口管理状态
    与操作状态分离。
  * 改进网络中
    多个 DHCPv4 服务器时
    DHCPv4 的行为。
  * 修复 net_mgmt
    事件大小计算。
  * 新增 :kconfig:option:`CONFIG_NET_LOOPBACK_MTU` 选项，
    用于配置回环接口 MTU。
  * 重新实现 IP/UDP/TCP 校验和计算，
    以加快处理速度。
  * 从测试用例中
    移除 :kconfig:option:`CONFIG_NET_CONFIG_SETTINGS` 的使用，
    以改进在真实平台上的
    测试执行。
  * 新增 MQTT-SN 库和示例。
  * 修改变量缓冲区长度配置
    （:kconfig:option:`CONFIG_NET_BUF_VARIABLE_DATA_SIZE`）。
  * 修复 IGMPv2 成员报告
    目标地址。
  * 为连接列表处理
    新增互斥锁保护。
  * 在 :c:struct:`net_context` 中
    将用户数据指针
    与 FIFO 保留空间分离。
  * 为 ``net pkt`` shell 命令
    新增输入验证。

* OpenThread：

  * 为 ECDSA API
    实现 PSA 支持。
  * 在禁用断言时
    修复 :c:func:`otPlatRadioSetMacKey`。
  * 弃用 :c:func:`openthread_set_state_changed_cb`，
    建议改用更通用的
    :c:func:`openthread_state_changed_cb_register`。
  * 实现诊断 GPIO 命令。

* SNTP：

  * 切换到
    内部使用 ``zsock_*`` 函数。
  * 修复在
    IPv4 禁用时
    库的操作。

* 套接字：

  * 修复在
    TLS 套接字创建失败时
    可能的内存泄漏。

* TCP：

  * 将默认 TCP
    乱序接收队列超时
    扩展到 2 秒。
  * 重新实现 TCP 引用计数，
    以防止 TCP 连接上下文
    被过早释放的情况。

* Websockets：

  * 重新实现 websocket
    接收例程，
    以修复多个问题。
  * 实现适当的
    websocket 关闭过程。
  * 修复 bug，
    该 bug 导致 websocket
    覆盖底层 TCP 套接字
    使用的互斥锁。

* Wi-Fi：

  * 新增对
    省电配置的支持。
  * 新增对
    监管域配置的支持。
  * 新增对
    省电超时配置的支持。

* zperf

  * 新增选项，
    用于为 zperf
    设置 QoS。
  * 修复
    乱序/丢失包统计。
  * 为库
    定义公共 API，
    以允许
    在未启用 shell 的情况下
    测量吞吐量。
  * 新增
    异步上传选项。

USB
***

* 新的实验性 USB 支持：

  * 新增 USB 设备栈
    （device_next）、
    CDC ACM 和
    BT HCI USB 传输层的
    类实现。
  * 新增对
    USB 主机的
    初步支持

* USB 设备栈（device）：

  * 移除
    总线挂起时的
    传输取消。
  * 重新设计
    在栈禁用时
    禁用所有端点，
    以允许
    重新启用 USB 设备栈。
  * 修订
    在替代设置上
    端点启用/禁用。
  * 改进
    Windows 上
    使用 WinUSB 的
    USB DFU 支持。
  * 新增检查，
    以防止
    递归日志循环，
    并允许
    在 CDC ACM 类实现中
    使用 poll out
    发送超过一个字节。
  * 更正
    IAD 和接口描述符，
    移除
    不必要的 CDC 描述符，
    并修复
    RNDIS 以太网实现中的
    包接收。
  * 在 USB MSC 类中
    实现
    写操作后的
    缓存同步。


设备树
**********

API
===

新的通用宏：

- :c:macro:`DT_FOREACH_PROP_ELEM_SEP_VARGS`
- :c:macro:`DT_FOREACH_PROP_ELEM_SEP`
- :c:macro:`DT_INST_FOREACH_PROP_ELEM_SEP_VARGS`
- :c:macro:`DT_INST_FOREACH_PROP_ELEM_SEP`
- :c:macro:`DT_INST_GPARENT`
- :c:macro:`DT_NODE_MODEL_BY_IDX_OR`
- :c:macro:`DT_NODE_MODEL_BY_IDX`
- :c:macro:`DT_NODE_MODEL_HAS_IDX`
- :c:macro:`DT_NODE_MODEL_OR`

为 GPIO hogs 功能
引入的新专用宏
（参见 :zephyr_file:`drivers/gpio/gpio_hogs.c`）：

- :c:macro:`DT_GPIO_HOG_FLAGS_BY_IDX`
- :c:macro:`DT_GPIO_HOG_PIN_BY_IDX`
- :c:macro:`DT_NUM_GPIO_HOGS`

移除的
以下已弃用宏：

- ``DT_CHOSEN_ZEPHYR_ENTROPY_LABEL``
- ``DT_CHOSEN_ZEPHYR_FLASH_CONTROLLER_LABEL``

绑定
========

新的绑定：

  - 通用或供应商无关：

    - :dtcompatible:`usb-c-connector`
    - :dtcompatible:`usb-ulpi-phy`

  - AMS AG（ams）：

    - :dtcompatible:`ams,as5600`
    - :dtcompatible:`ams,as6212`

  - Synopsys, Inc.（前身为 ARC International PLC）（arc）：

    - :dtcompatible:`arc,xccm`
    - :dtcompatible:`arc,yccm`

  - ARM Ltd.（arm）：

    - :dtcompatible:`arm,cortex-a55`
    - :dtcompatible:`arm,ethos-u`

  - ASPEED Technology Inc.（aspeed）：

    - :dtcompatible:`aspeed,ast10x0-reset`

  - Atmel Corporation（atmel）：

    - :dtcompatible:`atmel,samc2x-gclk`
    - :dtcompatible:`atmel,samc2x-mclk`

  - Bosch Sensortec GmbH（bosch）：

    - :dtcompatible:`bosch,bmi270`
    - :dtcompatible:`bosch,bmi270`

  - Cadence Design Systems Inc.（cdns）：

    - :dtcompatible:`cdns,i3c`
    - :dtcompatible:`cdns,uart`

  - Espressif Systems（espressif）：

    - :dtcompatible:`espressif,esp32-adc`
    - :dtcompatible:`espressif,esp32-dac`
    - :dtcompatible:`espressif,esp32-eth`
    - :dtcompatible:`espressif,esp32-gdma`
    - :dtcompatible:`espressif,esp32-mdio`
    - :dtcompatible:`espressif,esp32-temp`

  - GigaDevice Semiconductor（gd）：

    - :dtcompatible:`gd,gd322-dma`
      具有
      新的辅助宏，
      用于
      轻松设置
      ``dma-cells`` 属性。
    - :dtcompatible:`gd,gd32-dma-v1`
    - :dtcompatible:`gd,gd32-fwdgt`
    - :dtcompatible:`gd,gd32-wwdgt`

  - Hangzhou Grow Technology Co., Ltd.（hzgrow）：

    - :dtcompatible:`hzgrow,r502a`

  - Infineon Technologies（infineon）：

    - :dtcompatible:`infineon,xmc4xxx-adc`
    - :dtcompatible:`infineon,xmc4xxx-flash-controller`
    - :dtcompatible:`infineon,xmc4xxx-intc`
    - :dtcompatible:`infineon,xmc4xxx-nv-flash`

  - Intel Corporation（intel）：

    - :dtcompatible:`intel,adsp-communication-widget`
    - :dtcompatible:`intel,adsp-dfpmcch`
    - :dtcompatible:`intel,adsp-dfpmccu`
    - :dtcompatible:`intel,adsp-mem-window`
    - :dtcompatible:`intel,adsp-sha`
    - :dtcompatible:`intel,adsp-timer`
    - :dtcompatible:`intel,hda-dai`
    - :dtcompatible:`intel,raptor-lake`
Issue Related Items
*******************

Known Issues
============

- :github:`33747` - gptp does not work well on NXP rt series platform
- :github:`37193` - mcumgr: Probably incorrect error handling with udp backend
- :github:`37731` - Bluetooth: hci samples: Unable to allocate command buffer
- :github:`40023` - Build fails for ``native_posix`` board when using C++ <atomic> header
- :github:`42030` - can: "bosch,m-can-base": Warning "missing or empty reg/ranges property"
- :github:`43099` - CMake: ARCH roots issue
- :github:`43249` - MBEDTLS_ECP_C not build when MBEDTLS_USE_PSA_CRYPTO
- :github:`43555` - Variables not properly initialized when using data relocation with SDRAM
- :github:`43562` - Setting and/or documentation of Timer and counter use/requirements for Nordic Bluetooth driver
- :github:`44339` - Bluetooth:controller: Implement support for Advanced Scheduling in refactored LLCP
- :github:`44948` - cmsis_dsp: transform: error during building cf64.fpu and rf64.fpu for mps2_an521_remote
- :github:`45241` - (Probably) unnecessary branches in several modules
- :github:`45323` - Bluetooth: controller: llcp: Implement handling of delayed notifications in refactored LLCP
- :github:`45814` - Armclang build fails due to missing source file
- :github:`46121` - Bluetooth: Controller: hci: Wrong periodic advertising report data status
- :github:`46401` - ARM64: Relax 4K MMU mapping alignment
- :github:`46846` - lib: libc: newlib: strerror_r non-functional
- :github:`47120` - shell uart: busy wait for DTR in ISR
- :github:`47732` - Flash map does not fare well with MCU who do bank swaps
- :github:`47908` - tests/kernel/mem_protect/stack_random works unreliably and sporadically fails
- :github:`48094` - pre-commit scripts fail when there is a space in zephyr_base
- :github:`48102` - JSON parses uses recursion (breaks rule 17.2)
- :github:`48287` - malloc_prepare ASSERT happens when enabling newlib libc with demand paging
- :github:`48608` - boards: mps2_an385: Unstable system timer
- :github:`48841` - Bluetooth: df: Assert in lower link layer when requesting CTE from peer periodically with 7.5ms connection interval
- :github:`48992` - qemu_leon3: tests/posix/common/portability.posix.common fails
- :github:`49213` - logging.add.log_user test fails when compiled with GCC 12
- :github:`49390` - shell_rtt thread can starve other threads of the same priority
- :github:`49484` - CONFIG_BOOTLOADER_SRAM_SIZE should not be defined by default
- :github:`49492` - kernel.poll test fails on qemu_arc_hs6x when compiled with GCC 12
- :github:`49494` - testing.ztest.ztress test fails on qemu_cortex_r5 when compiled with GCC 12
- :github:`49614` - acrn_ehl_crb: The testcase tests/kernel/sched/schedule_api failed to run.
- :github:`49816` - ISOTP receive fails for multiple binds with same CAN ID but different extended ID
- :github:`49889` - ctf trace: unknown event id when parsing samples/tracing result on reel board
- :github:`50084` - drivers: nrf_802154: nrf_802154_trx.c - assertion fault when enabling Segger SystemView tracing
- :github:`50095` - ARC revision Kconfigs wrongly mixed with board name
- :github:`50196` - LSM6DSO interrupt handler not being called
- :github:`50501` - STM32 SPI does not work properly with async + interrupts
- :github:`50506` - nxp,mcux-usbd devicetree binding issues
- :github:`50546` - drivers: can: rcar: likely inconsistent behavior when calling can_stop() with pending transmissions
- :github:`50598` - UDP over IPSP not working on nRF52840
- :github:`50652` - RAM Loading on i.MXRT1160_evk
- :github:`50766` - Disable cross-compiling when using host toolchain
- :github:`50777` - LE Audio: Receiver start ready command shall only be sent by the receiver
- :github:`50875` - net: ip: race in access to writable net_if attributes
- :github:`50941` - sample.logger.syst.catalog.deferred_cpp fails on qemu_cortex_m0
- :github:`51024` - aarch32 excn vector not pinned in mmu causing newlib heap overlap
- :github:`51127` - UART HW DMA ( UART Communication based on HW DMA ) - Buffer Overflow test in STM32H743 Controller
- :github:`51133` - Bluetooth: audio: Sink ASE does not go to IDLE state
- :github:`51250` - ESP32-C3 pin glitches during start-up
- :github:`51317` - Confusing license references in nios2f-zephyr
- :github:`51342` - Bluetooth ISO extra ``stream_sent`` callback after ``seq_num`` 16-bit rollover
- :github:`51420` - tests: subsys: logging: log_links: logging.log_links fails
- :github:`51422` - nsim_em: tests/subsys/logging/log_link_order run failed on nsim_em
- :github:`51449` - device: device_get_binding is broken for nodes with the same name
- :github:`51604` - doc: is the documentation GDPR compliant since it uses Google Analytics without prompting the user about tracking?
- :github:`51637` - shell: bypass shell_fprintf ASSERT fail
- :github:`51728` - soc: xtensa: esp32_net: Remove binary blobs from source tree
- :github:`51774` - thread safety of adv_new in Bluetooth subsys
- :github:`51814` - ARC irq_offload doesn't honor thread switches
- :github:`51820` - Longer strings aren't logged
- :github:`51825` - west: runners: jlink: JLink.exe name collision
- :github:`51977` - newlib integration: _unlink isn't mapped to unlink
- :github:`52055` - Bluetooth: Controller: Broadcast scheduling issues
- :github:`52269` - UART documentation for uart_irq_tx_enable/disable incomplete
- :github:`52271` - west sign: imgtool: zephyr.signed.hex and zephyr.signed.bin do not have the same contents
- :github:`52362` - nrf_qspi_nor driver crash if power management is enabled
- :github:`52395` - Cannot build applications with dts having (unused) external flash partition and disabling those drivers
- :github:`52491` - Value of EVENT_OVERHEAD_START_US is set to low
- :github:`52494` - SPI NOR DPD comment is misleading/wrong
- :github:`52510` - twister: truncated handler.log reports test as "failed"
- :github:`52513` - sample.modules.chre fails on qemu_leon3
- :github:`52575` - Kconfig: excessive ``select`` usage
- :github:`52585` - PDM event handler shouldn't stop driver on allocation failure
- :github:`52589` - Add support for different SDHC high-speed modes (currently defaults to SDR25)
- :github:`52605` - esp32-usb-serial tx-complete interrupt not working in interrupt mode on esp32c3
- :github:`52623` - qemu_x86: thousands of timer interrupts per second
- :github:`52667` - nrf_rtc_timer: Booting application with zephyr < 3.0.0 from mcuboot with zephyr >= 3.0.0
- :github:`52700` - posix: getopt: implement standards-compliant reset
- :github:`52702` - drivers: wifi: esp_at: Some issues on Passive Receive mode
- :github:`52705` - RNDIS fails to enumerate on Raspberry Pi Pico
- :github:`52741` - bl5340_dvk_cpuapp has wrong button for mcuboot button
- :github:`52764` - boards: esp32c3_devkitm: unable to read memory-mapped flash memory
- :github:`52792` - ATWINC1500 : (wifi_winc1500_nm_bsp.c : nm_bsp_reset) The reset function is not logical and more
- :github:`52825` - Overflow in settime posix function
- :github:`52830` - Annoying Slirp Message console output from qemu_x86 board target
- :github:`52868` - ESP32 Wifi driver returns EIO (-5) if connecting without a sleep sometime before calling
- :github:`52869` - ESP32 Counter overflow, with no API to reset it
- :github:`52885` - modem: gsm_ppp: CONFIG_GSM_MUX: Unable to reactivate modem after executing gsm_ppp_stop()
- :github:`52886` - tests: subsys: fs: littlefs: filesystem.littlefs.default and filesystem.littlefs.custom fails
- :github:`52887` - Bluetooth: LL assert with chained adv packets
- :github:`52924` - ESP32 get the build message "IRAM0 segment data does not fit."
- :github:`52941` - Zephyr assumes ARM M7 core has a cache
- :github:`52954` - check_zephyr_package() only checks the first zephyr package rather than all the considered ones.
- :github:`52998` - tests: drivers: can: Build failure with sysroot path not quoted on Windows
- :github:`53000` - Delaying logging via CONFIG_LOG_PROCESS_THREAD_STARTUP_DELAY_MS doesn't work if another backend is disabled
- :github:`53006` - Hawbkit with b_l4s5i_iot01a - wifi_eswifi: Cannot allocate rx packet
- :github:`53008` - Invalid ISO interval configuration
- :github:`53088` - Unable to chage initialization priority of logging subsys
- :github:`53123` - Cannot run a unit test on Mac OSX with M1 Chip
- :github:`53124` - cmake: incorrect argument passing and dereference in zephyr_check_compiler_flag() and zephyr_check_compiler_flag_hardcoded()
- :github:`53137` - Bluetooth: Controller: HCI 0x45 error after 3rd AD fragment with data > 248 bytes
- :github:`53148` - Bluetooth: Controller: BT_HCI_OP_LE_BIG_TERMINATE_SYNC on syncing BIG sync returns invalid BIG handle
- :github:`53172` - SHTCx driver wrong negative temperature values
- :github:`53173` - HCI-UART: unable to preform a DFU - GATT CONN timeout
- :github:`53198` - Bluetooth: Restoring security level fails and missing some notifications
- :github:`53265` - Bluetooth: Controller: ISO interleaved broadcast not working
- :github:`53319` - USB CDC ACM UART driver's interrupt-driven API hangs when no host is connected
- :github:`53334` - Bluetooth: Peripheral disconnected with BT_HCI_ERR_LL_RESP_TIMEOUT reason and SMP timeout
- :github:`53343` - subsys: logging: use of timestamping during early boot may crash MMU-based systems
- :github:`53348` - Bluetooth: Restoring connection to peripheral issue
- :github:`53375` - net: lwm2m: write method when floating point
- :github:`53475` - The ATT_MTU value for EATT should be set as the minimum MTU of ATT Client and ATT Server
- :github:`53505` - Some device tree integers may be signed or unsigned depending on their value
- :github:`53522` - k_busy_wait function hangs on when CONFIG_SYSTEM_CLOCK_SLOPPY_IDLE is set with CONFIG_PM.
- :github:`53537` - TFM-M doesn't generate tfm_ns_signed.bin image for FOTA firmware upgrade
- :github:`53544` - Cannot see both bootloader and application RTT output
- :github:`53546` - zephyr kernel Kconfig USE_STDC_LSM6DS3TR and hal_st CMakeLists.txt lsm6ds3tr-c variable name mismatched (hyphen sign special case)
- :github:`53552` - LE Audio: Device executes receiver start ready before the CIS is connected
- :github:`53555` - ESP32-C3 Is RV32IMA, Not RV32IMC?
- :github:`53570` - SDHC SPI driver should issue CMD12 after receiving data error token
- :github:`53587` - Issue with Auto-IP and Multicast/socket connection
- :github:`53605` - tests: posix: common: portability.posix.common fails - posix_apis.test_clock_gettime_rollover
- :github:`53613` - tests: drivers: uart: uart_mix_fifo_poll: tests ``drivers.uart.uart_mix_poll_async_api_*`` fail
- :github:`53643` - Invalid warning when BLE advertising times out
- :github:`53674` - net: lwm2m: senml cbor formatter relying on implementation detail / inconsistency of lwm2m_path_to_string
- :github:`53680` - HawkBit Metadata Error
- :github:`53728` - Sensor API documentation: no mention of blocking behaviour
- :github:`53729` - Can not build for ESP32 sample program - Zephyr using CMake build
- :github:`53767` - `@kconfig` is not allowed in headline
- :github:`53780` - sysbuild with custom board compilation failed to find the board
- :github:`53790` - Flash Init fails when CONFIG_SPI_NOR_IDLE_IN_DPD=y
- :github:`53800` - Raspberry Pi Pico - ssd1306 display attempts to initialize before i2c bus is ready for communication
- :github:`53801` - k_busy_wait adds 1us delay unnecessarily
- :github:`53823` - Bluetooth init failed on nrf5340_audio_dk_nrf5340_cpuapp
- :github:`53855` - mimxrt1050_evk invalid writes to flash
- :github:`53858` - Response on the shell missing with fast queries
- :github:`53867` - kconfig: Linked code into external SEMC-controlled memory without boot header
- :github:`53871` - Bluetooth: IPSP Sample Crash on nrf52840dk_nrf52840
- :github:`53873` - Syscall parser creates syscall macro for commented/ifdefed out syscall prototype
- :github:`53917` - clang-format key incompatible with IntelliJ IDEs
- :github:`53933` - tests: lib: spsc_pbuf: lib.spsc_pbuf... hangs
- :github:`53937` - usb: stm32g0: sometimes get write error during CDC ACM enumeration when using USB hub
- :github:`53939` - USB C PD stack no callback for MSG_NOT_SUPPORTED_RECEIVED policy notify
- :github:`53964` - gpio_emul: ``gpio_*`` functions not callable within an ISR
- :github:`53980` - Bluetooth: hci: spi: race condition leading to deadlock
- :github:`53993` - platform: Raspberry Pi Pico area: USB Default config should be bus powered device for the Raspberry Pi Pico
- :github:`53996` - bt_conn_foreach() includes invalid connection while advertising
- :github:`54014` - usb: using Bluetooth HCI class in composite device leads to conflicts
- :github:`54037` - Unciast_audio_client sample application cannot work with servers with only sinks.
- :github:`54047` - Bluetooth: Host: Invalid handling of Service Changed indication if GATT Service is registered after Bluetooth initialization and before settings load
- :github:`54064` - doc: mgmt: mcumgr: img_mgmt: Documentation specifies that hash in state of images is a required field
- :github:`54076` - logging fails to build with LOG_ALWAYS_RUNTIME=y
- :github:`54085` - USB MSC Sample does not work for native_posix over USBIP
- :github:`54092` - ZCBOR code generator generates names not compatible with C++
- :github:`54101` - bluetooth: shell: Lots of checks of type (unsigned < 0) which is bogus
- :github:`54121` - Intel CAVS: tests/subsys/zbus/user_data fails
- :github:`54122` - Intel CAVS: tests/subsys/dsp/basicmath fails (timeout)
- :github:`54162` - Mass-Storage-Sample - USB HS support for the stm32f723e_disco board
- :github:`54179` - DeviceTree compile failures do not stop build
- :github:`54198` - reel board: Mesh badge demo fails to send BT Mesh message
- :github:`54199` - ENC28J60: dns resolve fails after few minutes uptime
- :github:`54200` - bq274xx incorrect conversions
- :github:`54211` - tests: kernel: timer: timer_behavior: kernel.timer.timer fails
- :github:`54226` - Code coverage collection is broken
- :github:`54240` - twister: --runtime-artifact-cleanup has no effect
- :github:`54273` - ci: Scan code workflow does not report a violation for unknown LicenseRef
- :github:`54275` - net: socket: tls: cannot send when using blocking socket
- :github:`54288` - modem: hl7800: power off draws excessive current
- :github:`54289` - Twister jobserver support eliminates parallel build for me
- :github:`54301` - esp32: Console doesn't work with power management enabled
- :github:`54317` - kernel: events: SMP race condition and one enhancement
- :github:`54330` - West build command execution takes more time or fails sometimes
- :github:`54336` - picolibc is incompatible with xcc / xcc-clang toolchains
- :github:`54364` - CANopen SYNC message is not received
- :github:`54373` - Mcuboot swap type is ``test`` when update fails
- :github:`54377` - mec172xevb: benchmark.kernel.core (and adc_api/drivers.adc) failing
- :github:`54407` - Bluetooth: Controller: ISO Central with continuous scanning asserts
- :github:`54411` - mgmt: mcumgr: Shell transport can lock shell up until device is rebooted
- :github:`54435` - mec172xevb: sample.drivers.sample.drivers.peci failing
- :github:`54439` - Missing documentation of lwm2m_rd_client_resume and lwm2m_rd_client_pause
- :github:`54444` - samples/modules/chre/sample.modules.chre should not attempt to build on toolchains w/o newlib
- :github:`54459` - hawkbit: wrong header size used while reading the version of the app
- :github:`54460` - Build system should skip ``zephyr/drivers/ethernet`` module if TAP & SLIP already provides a network driver in ``zephyr/drivers/net/slip.c``
- :github:`54498` - net: openthread: echo server do not work in userspace
- :github:`54500` - jwt: memory allocation problem after multiple jwt_sign calls
- :github:`54504` - LwM2M: Connection resume does not work after network error
- :github:`54506` - net: ieee802154_6lo: wrong fragmentation of packets with specific payload sizes
- :github:`54531` - Bluetooth: Controller: le_ext_create_connection fails with initiating_PHYs == 0x03
- :github:`54532` - Tests: Bluetooth: tester: BTP communication is not fully reliable on NRF52 board using UART
- :github:`54538` - LE Audio: BAP Unicast Client Idle/CIS disconnect race condition
- :github:`54539` - LE Audio: Unicast client should only disconnect CIS if both ASEs are not in streaming state
- :github:`54542` - Bluetooth pending tx packets assert on disable
- :github:`54554` - arch.arm.swap.tz fails to build for v2m_musca_b1_ns
- :github:`54576` - Errors during IPv4 defragmenting
- :github:`54577` - IPv6 defragmenting fails when segments do not overlap
- :github:`54581` - STM32H7 adc sequence init function unstable logic return
- :github:`54599` - net stats: many received TCP packets count as "dropped"
- :github:`54609` - driver: led: kconfig symbols mix up
- :github:`54610` - samples: kernel: metairq_dispatch: sample.kernel.metairq_dispatch hangs
- :github:`54630` - memcpy crashes with NEW_LIBC on stm32 cortex m7 with debugger attached
- :github:`54668` - shell: "log backend" command causes shell to lock up
- :github:`54670` - stm32: memcpy crashes with NEWLIBC
- :github:`54674` - modem: hl7800: DNS resolver does not start for IPv6 only
- :github:`54683` - Missing input validation in gen_driver_kconfig_dts.py
- :github:`54695` - usb mass storage on mimxrt595_evk_cm33 mount very slow
- :github:`54705` - CDC USB shell receives garbage when application starts
- :github:`54713` - LVGL Module File System Memory Leaks
- :github:`54717` - --generate-hardware-map produces TypeError: expected string or bytes-like object on Windows
- :github:`54719` - STM32 clock frequency calculation error
- :github:`54720` - QEMU bug with branch delay slots on ARC
- :github:`54726` - LittleFS test only works for specific device parameters
- :github:`54731` - USB DFU sample does not reliably upload image on RT1050
- :github:`54737` - Wrong order of member initialization for macro Z_DEVICE_INIT
- :github:`54739` - C++ Compatibility for DEVICE_DT_INST_DEFINE
- :github:`54746` - ESP32 SPI word size is not respected
- :github:`54754` - outdated version of rpi_pico hal configures USB PLL incorrectly
- :github:`54755` - small timer periods take twice as much time as they should
- :github:`54768` - nrf9160dk_nrf52840: flow control pins crossed
- :github:`54769` - Error when flashing to LPCXpresso55S06 EVK.
- :github:`54770` - Bluetooth: GATT: CCC and CF values written by privacy-disabled peer before bonding may be lost
- :github:`54773` - Bluetooth: GATT: Possible race conditions related to GATT database hash calculation after settings load
- :github:`54779` - file write gives -5 after file size reaches cache size
- :github:`54783` - stm32: NULL dereference in net_eth_carrier_on
- :github:`54785` - .data and .bss relocation to DTCM & CCM is broken with SDK 0.15+
- :github:`54798` - net: ipv4: IP packets get dropped in Zephyr when an application is receiving high rate data
- :github:`54805` - when invoke dma_stm32_disable_stream failed in interrupt callback, it will endless loop
- :github:`54813` - Bluetooth: host: Implicit sc_indicate declaration when Service Changed is disabled
- :github:`54824` - BT: Mesh: Utilizes some not initialized variables
- :github:`54826` - Clang/llvm build is broken: Error: initializer element is not a compile-time constant
- :github:`54833` - ESPXX failing in gpio tests
- :github:`54841` - Drivers: I2S: STM32: Mishandling of Master Clock output (MCK)
- :github:`54844` - RAK5010 board has wrong LIS3DH INT pin configured
- :github:`54846` - ESP32C3 SPI DMA host ID
- :github:`54855` - ESP32: Compilation errors after migrating to zephyr 3.2.0
- :github:`54856` - nRF52840 nRF52833 Bluetooth: Timeout in ``net_config_init_by_iface`` but interface is up
- :github:`54859` - LE Audio: BT_AUDIO_UNICAST_CLIENT_GROUP_STREAM_COUNT invalid descsi
- :github:`54861` - up_squared: CHRE sample output mangling fails regex verification

Addressed issues
================

* :github:`54873` - doc: Remove Google Analytics tracking code from generated documentation.
* :github:`54858` - espressif blobs does not follow zephyr requirements
* :github:`54872` - west 刷写 --elf-file  不 刷写 使用 .elf 文件 但 使用 zephyr.hex 到 刷写
* :github:`54813` - Bluetooth: host: Implicit sc_indicate declaration when Service Changed is disabled
* :github:`54804` - Warning (simple_bus_reg): /soc/can: missing or empty reg/ranges property
* :github:`54786` - doc: Version selector should link to latest LTS version instead of 2.7.0
* :github:`54782` - nrf_rtc_timer may not properly handle a timeout that is set in specific conditions
* :github:`54770` - Bluetooth: GATT: CCC and CF values written by privacy-disabled peer before bonding may be lost
* :github:`54763` - doc: Copyright 通知   更新 到 2015-2023
* :github:`54760` - net_lwm2m_engine: fcntl(F_GETFL) failed (-22) on es-wifi
* :github:`54730` - intel_adsp_ace15_mtpm: cpp.main.minimal test failing
* :github:`54718` -  rf2xx 驱动 使用  错误 bit mask 在...上 TRAC_STATUS
* :github:`54710` - Sending NODE_RX_TYPE_CIS_ESTABLISHED messes up LLCP
* :github:`54703` - boards: thingy53: Inconsistent method of setting USB related log level
* :github:`54702` - boards: thingy53: USB remote wakeup is not correctly disabled
* :github:`54686` - RP2040: Cleanup incorrect comment and condition from the USB driver
* :github:`54685` - drivers: serial: rp2040: fix rpi pico address mapping
* :github:`54671` - Bluetooth: spurious error when using hci_rpmsg
* :github:`54666` - LE Audio: EALREADY error of ase_stream_qos() not mapped
* :github:`54659` - boards: arm: nrf52840dongle_nrf52840: Defaults to UART which is not connected (and mcuboot build fails)
* :github:`54654` - LE Audio: Kconfig typo in ``pacs.c``
* :github:`54642` - Bluetooth: Controller: Assertion on disconnecting CIS and assertion on synchronizing to first encrypted BIS
* :github:`54614` - Cannot flash b_l4s5i_iot01a samples/hello_world
* :github:`54613` - Bluetooth: Unable to enable PAST as advertiser without periodic sync support
* :github:`54605` - native_posix_64 平台 损坏 在...中 Twister
* :github:`54597` - SRAM2 wrong on certain stm32h7 SOC (system crashes during startup)
* :github:`54580` - samples/subsys/task_wdt fails with timeout on s32z270dc2_r52 boards
* :github:`54575` - Automatic termination 带 return 代码 从  native_posix 主 函数
* :github:`54574` - USB RNDIS Reception and Descriptor Issue(s)
* :github:`54573` - gpio_hogs test uses an incorrect GPIO spec handle
* :github:`54572` - QEMU networking breakage (Updating nrf-sdk 2.1->2.2 , implies zephyr 3.1 -> 3.2)
* :github:`54569` - MMC subsys shares sdmmc kconfigs
* :github:`54567` - Assertion in z_add_timeout() fails in drivers.uart.uart_mix_poll_async_api test
* :github:`54563` - Variable uninitialised in flash_stm32_page_layout
* :github:`54558` - LPTIM Kconfig-related build failures for nucleo_g431rb
* :github:`54557` - sample.drivers.flash.shell 失败 到 构建 用于 adafruit_kb2040
* :github:`54556` - sample.display.lvgl.gui 失败 到 构建 用于 stm32f429i_disc1
* :github:`54545` - 板 rpi_pico: 坏 MPU 设置
* :github:`54544` - Bluetooth: controller: HCI/CCO/BI-45-C setHostFeatureBit failing
* :github:`54540` - psa_crypto variants of drivers/entropy/api and crypto/rand32 tests fail to build for nrf9160dk_nrf9160_ns and nrf5340dk_nrf5340_cpuapp_ns
* :github:`54537` - logging.add.async build fails on mtpm with xcc-clang
* :github:`54534` - PSoC6/Cat1 add binary blob for Cortex-M0+ core
* :github:`54533` - tests/drivers/can/timing fails on nucleo_f746zg
* :github:`54529` - Bluetooth: shell 缺失 help 消息 和 参数
* :github:`54528` - log switch_format, mipi_syst tests failing on intel_adsp_ace15_mtpm
* :github:`54522` - Can we embrace GNU Build IDs?
* :github:`54516` - twister: Quarantine verify works incorrectly with integration mode
* :github:`54509` - Zephyr does not configure TF-M correctly for Hard-Float
* :github:`54507` - CONFIG_PM=y results to hard fault system for STM32L083
* :github:`54499` - stm32u5 lptimer driver init must wait after interrupt reg
* :github:`54493` - samples/drivers/counter/alarm/ fails on nucleo_f746zg
* :github:`54492` - west: twister return code ignored by west
* :github:`54484` - Intel CAVS25: tests/boards/intel_adsp/ssp/ fails
* :github:`54472` - 如何 到 启用  node 在...中 主
* :github:`54469` - nsim_sem and nsim_em7d_v22 failed in zdsp.basicmath test
* :github:`54462` - usb_dc_rpi_pico 驱动 启用 一些 中断 它 doesn't handle
* :github:`54461` - SAM spi bus inoperable when interrupted on fast path
* :github:`54457` - DHCPv4 启动 甚至 当...时 接口  不 operationally 上
* :github:`54455` - 许多 测试  错误 component 和  wrongly 分类
* :github:`54454` - Twister summary in some cases provides an irrelevant example
* :github:`54450` - nuvoton_pfm_m487 失败 到 构建 due 到 缺失 M48x-pinctrl.h
* :github:`54440` - tests/net/lib/lwm2m/lwm2m_registry/subsys.net.lib.lwm2m.lwm2m_registry fails to build w/toolchains that don't support newlib
* :github:`54438` - question: why lwm2m_rd_client_stop might block
* :github:`54431` - adafruit kb2040 板 配置  无效 和 lack 刷写 controller
* :github:`54428` - esp32 invalid flash dependencies
* :github:`54427` - stm32 uart driver ``LOG_`` msg crashes when entering sleep mode
* :github:`54422` - modules: openthread: multiple definition in openthread config
* :github:`54417` - Intel CAVS18: tests/subsys/dsp/basicmath fails
* :github:`54414` - stm32u5 dma driver does not support repeated start-stop
* :github:`54412` - [hci_uart] nrf52840 & BlueZ 5.55 - start / stop scanning breaks
* :github:`54410` - [BUG] TLB driver fails to unmap L2 HPSRAM region when assertions are enabled
* :github:`54409` - ETH MAC 配置 用于 STM32H7X 和 STM32_HAL_API_V2 太 晚 和 失败
* :github:`54405` - Nominate @Vge0rge as contributor
* :github:`54401` - Uninitialized has_param struct sometimes causes BSIM "has.sh" test to fail
* :github:`54399` - Intel CAVS18: tests/subsys/zbus/user_data/user_data.channel_user_data FAILED
* :github:`54397` - 测试 posix_header 失败 在...上 一些 STM32 Nucleo 板
* :github:`54395` - mgmt: mcumgr: img_grp: Upload inspect fails when using swap using scratch
* :github:`54393` - Bluetooth: Controller: Starting a second BIG causes them to overlap and have twice the interval
* :github:`54387` - soc: arm: st_stm32: Incorrect SRAM devicetree definition for the STM32L471xx
* :github:`54384` - Removal of old runner options caused downstream breakage
* :github:`54378` - Net pkt PPP dependency bug
* :github:`54374` - ARC: west runner: mdb: incorrect handling of unsupported jtag adapters
* :github:`54372` - ARC: west runner: mdb: unexpected empty argument pass to MDB executable
* :github:`54366` - tests: pin_get_config failed on it8xxx2_evb, again
* :github:`54361` - Incorrect network stats for Neighbour Discovery packets
* :github:`54360` - enable HTTPS server on Zephyr RTOS
* :github:`54356` - Bluetooth: Scanner consumption while scanning
* :github:`54351` - Tests: bluetooth: failing unittests
* :github:`54347` - zephyr/posix/fcntl.h header works differently on native_posix platform
* :github:`54344` - Bluetooth: Controller: Central ACL connections overlap Broadcast ISO BIG event
* :github:`54342` - Bluetooth: Controller: Connected ISO Central causes Peripheral to drop ISO data PDUs
* :github:`54341` - Bluetooth: Controller: Direction finding samples do not reconnect after disconnection
* :github:`54335` - tests/kernel/fatal/no-multithreading/kernel.no-mt.cpu_exception failing on qemu_cortex_m3
* :github:`54334` - Need support to define partitions for usage with mcuboot
* :github:`54332` - LwM2M engine is does not go into non-block mode anymore in native_posix target
* :github:`54327` - intel_adsp: ace: various multicore bugs, timeouts
* :github:`54321` - ARC: unusable console after west flash or west debug with mdb runners
* :github:`54318` - boards: nucleo_g474re: openocd runner is not stable enough for intensive testing
* :github:`54316` - RTT is not working correctly on STM32U5 series
* :github:`54315` - Problem seen with touch screen on RT1170 when running the LVGL sample
* :github:`54310` - 使用 NOCOPY 代码 relocation 生成  警告 flag
* :github:`54287` - modem: hl7800: PSM hibernate draws excessive current
* :github:`54274` - newlib: 记录 CONFIG_NEWLIB_LIBC_NANO 默认 更改
* :github:`54258` - boards: arm: twr_ke18f: LPTMR always enabled, resulting in low system timer resolution
* :github:`54254` - tests: canbus: isotp: conformance: test fails with CONFIG_SYS_CLOCK_TICKS_PER_SEC=100
* :github:`54253` - v3.3.0-rc1: stm32: IPv6 neighbour solicitation packets are not received without CONFIG_ETH_STM32_MULTICAST_FILTER
* :github:`54247` - tests: net: tcp: net.tcp.simple fails
* :github:`54246` - Sample:subsys/ipc/rpmsg_server:The two cores cannot communicate in nRF5340
* :github:`54241` - The cy8c95xx I2C GPIO expander support was broken in #47841
* :github:`54236` - b_u585i_iot02a_ns: Can't build TFM enabled samples (TF-M 1.7.0)
* :github:`54230` - STM32H7: 内核 崩溃 带 BCM4=0
* :github:`54225` - Intel CAVS: tests/lib/c_lib/ fails
* :github:`54224` - 问题 带 picolibc 在...上 xtensa 平台
* :github:`54223` - Intel CAVS: tests/kernel/common/kernel.common.picolibc fails
* :github:`54214` - Display framebuffer allocation
* :github:`54210` - 测试 驱动 udc drivers.udc 失败
* :github:`54209` - USB C PD dead battery support
* :github:`54208` - Various RISC-V FPU context switching issues
* :github:`54205` - Regression: RiscV FPU regs not saved in multithreaded applications
* :github:`54202` - decawave_dwm1001_dev: i2c broken due to pinctrl_nrf fix
* :github:`54190` - RP2040 cannot be compiled with C11 enabled
* :github:`54173` - Bluetooth: GATT: Change awareness of bonded GATT Client is not maintained on reconnection after reboot
* :github:`54172` - Bluetooth: GATT: 写入 值 的 gatt_cf_cfg 数据   dropped 在...上 power 下
* :github:`54148` - qemu_x86_tiny places picolibc text outside of pinned.text
* :github:`54140` - BUS FAULT when running nmap towards echo_async sample
* :github:`54139` - Bluetooth: Audio: race hazard bt_audio_discover() callback vs unicast_client_ase_cp_discover()
* :github:`54138` - Buetooth: shell: `bt adv-data` isn't working properly
* :github:`54136` - Socket error after deregistration causes RD client state machine to re-register
* :github:`54123` - Intel CAVS 25: tests/boards/intel_adsp/ssp fails
* :github:`54117` - West flash fails on upload to Nucleo F303K8
* :github:`54104` - Bluetooth: Host: Bonding information distribution in the non-bondable mode
* :github:`54087` - tests:igmp:frdm_k64f: igmp test fails
* :github:`54086` - test:rio:frdm_k64f: rio user_space test fails with zephyr-v3.2.0-3842-g7ffc20082023
* :github:`54078` - No activity on can_tx when running the ISO-TP sample
* :github:`54072` - Bluetooth: Host: Periodic scanner does not differentiate between partial and incomplete data
* :github:`54065` - 如何 到 更改 C++ 版本 Compilation 选项 用于 Freestanding Application?
* :github:`54053` - CI:frdm_k64f: kernel.common.stack_protection test failure
* :github:`54034` - QSPI: Unable to build the project when introduced DMA into external flash interfacing
* :github:`54017` - Modules: TF-M: Resolve QCBOR issues with TF-M 1.7.0
* :github:`54005` - esp32 Severe crash using modules with embedded PSRAM (eg esp32-wroom-32E-n8r2)
* :github:`54002` - mgmt: mcumgr: bluetooth transport: Inability to use refactored transport as a library in some circumstances
* :github:`53995` - drivers: ethernet: stm32: Enable ethernet statistics in the driver
* :github:`53994` - net: ethernet: Multicast receive packets statistics are not getting updated
* :github:`53991` - LE Audio: samples/bluetooth/broadcast_audio_sink configure error
* :github:`53989` - STM32 usb networking stack threading issue
* :github:`53967` - net: http client: HTTP timeout can lead to deadlock of global system queue
* :github:`53954` - tests: lib: ringbuffer: libraries.ring_buffer hangs
* :github:`53952` - USB C PD sink sample stops working when connected to a non-PD source
* :github:`53942` - Websocket: No close message on websocket close
* :github:`53936` - Enabling CONFIG_TRACING and CONFIG_EVENTS causes undefined reference error
* :github:`53935` - stm32 iwdt wdt_install_timeout not working properly
* :github:`53926` - Bluetooth Mesh stack question
* :github:`53916` - Multichannel PWM for STM32U575
* :github:`53913` - net: ip: igmp: IGMP doesn't get initialised because the iface->config.ip.ipv4 pointer is not initialised
* :github:`53911` - Info request: SMP Hash
* :github:`53900` - led_set_brightness() is not setting brightness after led_blink() for STM32U575
* :github:`53885` - Ethernet TCP Client Issue description with iperf/zperf
* :github:`53876` - The handle of att indication violates the spec
* :github:`53862` - Switching from USB to UART
* :github:`53859` - RFC: 板 移植 guide:  不 assume OS 或 默认 移植 用于 板 文件
* :github:`53808` - Improve PLLI2S VCO precision
* :github:`53805` - peripheral_dis compilation reports RAM overflow for BBC microbit
* :github:`53799` - Info request: SMP hash definition
* :github:`53786` - BLE:DF: slot_plus_us is not set properly
* :github:`53782` - nrf5340dk: missing i2c bias pull up
* :github:`53781` - Allow resetting STM32 peripherals through RCC peripheral reset register
* :github:`53777` - mgmt: mcumgr: Change transport selects to depends on
* :github:`53773` - drivers: ethernet: stm32: Completion of enabling the multicast hash filter
* :github:`53756` - esp32 - 错误 值 用于  默认 CPU freq -> 崩溃 在...上 assert
* :github:`53753` - [DOC] Mismatch of driver sample overview
* :github:`53744` - ztest: assert() functions does not always retuns
* :github:`53723` - 设备 tree 宏 GPIO_DT_SPEC_INST_GET_BY_IDX_OR  不 工作
* :github:`53720` - Bluetooth: Controller: Incorrect address type for PA sync established
* :github:`53715` - mec15xxevb_assy6853: broken UART console output
* :github:`53707` - fs: fcb: Add option to disable CRC for FCB entries
* :github:`53697` - Can not run the usb mass storage demo on NXP mimxrt595_evk_cm33
* :github:`53696` - sysbuild should not parse the board revision conf
* :github:`53689` - 板 nrf52840dongle_nrf52840  缺失 存储 划分 定义
* :github:`53676` - net: lwm2m: inconsistent path string handling throughout the codebase
* :github:`53673` - samples: posix: gettimeofday does not build on native_posix
* :github:`53663` - Error while trying to flash nucleo_f446re: TARGET: stm32f4x.cpu - Not halted
* :github:`53656` - twister: samples: Bogus yaml for code_relocation sample
* :github:`53654` - SPI2 不 工作 在...上 STM32L412
* :github:`53652` - samples: mgmt: mcumgr: fs overlay does not work
* :github:`53642` - Display driver sample seems to mix up RGB565 and BGR565
* :github:`53636` - cdc_acm 失败 在...上 lpcxpresso55s69 板
* :github:`53630` - net: ieee802154_6lo: REGRESSION: L2 MAC byte swapping results in wrong IPHC decompression
* :github:`53617` - unicast_audio_client and unicast_audio_server example assert
* :github:`53612` - 文件 系统 (LFS?): 失败 到 扩展 文件 带 truncate
* :github:`53610` - k_malloc 和 设置
* :github:`53604` - testsuite: Broken Kconfig prevents building tests for nrf52840dk_nrf52840 platform
* :github:`53584` - STM32F1 PWM Input Capture Issue
* :github:`53579` - add_compile_definitions does not "propagate upwards" as supposed to when using west
* :github:`53568` - Kconfig search has white on white text
* :github:`53566` - 使用 fixup commits 期间 代码 审查
* :github:`53559` - mgmt: mcumgr: explore why UART interface is so slow (possible go application fault)
* :github:`53556` - Cannot add multiple out-of-the-tree secure partitions
* :github:`53549` - mgmt: mcumgr: callbacks: Callbacks events for a single group should be able to be combined
* :github:`53548` - net: ip: igmp: Mechanism to add MAC address for IGMP all systems multicast address to an ethernet multicast hash filter
* :github:`53535` - define a recommended process in zephyr for a CI framework integration
* :github:`53520` - tests: drivers: gpio: gpio_api_1pin: peripheral.gpio.1pin fails
* :github:`53513` - STM32 PWM Input Capture Issue
* :github:`53500` - ``net_tcp: context->tcp == NULL`` error messages during TCP connection
* :github:`53495` - RFC: treewide: python: argparse default configuration allows shortened command arguments
* :github:`53490` - Peridic current spike using tickless Zephyr
* :github:`53488` - Missing UUID for PBA and TMAS
* :github:`53487` - west: 刷写 stm32cubeprogrammer: 复位 命令 line 参数  错误
* :github:`53474` - Sysbuild cmake enters infinite loop if 2 images are added to a build with the same name
* :github:`53470` - Unable to build using Arduino Zero
* :github:`53468` - STM32 single-wire UART not working when poll-out more than 1 char
* :github:`53466` - Nucleo F413ZH CAN bus support
* :github:`53458` - IPv4 address autoconfiguration leaks TX packets/buffers
* :github:`53455` - GATT: Deadlock while sending GATT notification from system workqueue thread
* :github:`53451` - USB: Suspending CDC ACM can lead to endpoint/transfer state mismatch
* :github:`53446` - Bluetooth: Controller: ll_setup_iso_path not working if both CIS and BIS supported
* :github:`53438` - unable to wakeup from Stop2 mode
* :github:`53437` - WaveShare xnucleo_f411re: Error: ``** Unable to reset target **``
* :github:`53433` - flash content erase in bootloader region at run time
* :github:`53430` - drivers: display: otm8009a: import 3rd-party source
* :github:`53425` -  我们  支持 用于 rtc subsecond calculation 在...中 zephyr.
* :github:`53424` - Reopen issue #49390
* :github:`53423` - [bisected] logging.log_msg_no_overflow is failing on qemu_riscv64
* :github:`53421` - cpp: defined popcount macro prevents use of std::popcount
* :github:`53419` - net: stats: DHCP packets are not counted as part of UDP counters
* :github:`53417` - CAN-FD / MCAN driver: Possible variable overflow for some MCUs
* :github:`53407` - 支持 的 regex
* :github:`53385` - SWD 不 工作 在...上 STM32F405
* :github:`53366` - net: ethernet: provide a way to get ethernet config
* :github:`53361` - 增加 I2C 设备 SX1509B 到 Devicetree 带  相同 地址 在...上 不同 busses 生成 FATAL ERROR.
* :github:`53360` - 内核 k_msgq: 增加 peek_more 函数
* :github:`53347` - WINC1500 socket recv fail
* :github:`53340` - net: lwm2m: add BinaryAppDataContainer object (19)
* :github:`53335` - Undeclared constants in devicetree_generated.h
* :github:`53326` - usb: device: usb_dfu: k_mutex is being called from isr
* :github:`53315` - Fix possible underflow in tcp flags parse.
* :github:`53306` - 脚本 utils: migrate_mcumgr_kconfigs.py: 缺失 选项
* :github:`53301` - Bluetooth: Controller: Cannot recreate CIG
* :github:`53294` - samples: mgmt: mcumgr: smp_svr: UDP file can be removed
* :github:`53293` - mgmt: mcumgr: CONFIG_MCUMGR_GRP_IMG_REJECT_DIRECT_XIP_MISMATCHED_SLOT causes a build failure
* :github:`53285` - SNTP & DATE_TIME & SERVER ADDRESS configuration and behavior
* :github:`53280` - Bluetooth: security level failure with multiple links
* :github:`53276` - doc: mgmt: mcumgr: fix "some unspecified" error
* :github:`53271` - 模块 segger: KConfigs  损坏
* :github:`53259` - RFC: API Change: dma: callback status
* :github:`53254` - Bluetooth: bt_conn_foreach() reports unstable conn ref before the connection is completed
* :github:`53247` - ATT timeout followed by a segmentation fault
* :github:`53242` - Controller in HCI UART RAW mode responds to Stop Discovery mgmt command with 0x0b status code
* :github:`53240` - Task Watchdog Fallback Timeout Before Installing Timeout - STM32
* :github:`53236` - Make USB VBUS sensing configurable for STM32 devices
* :github:`53231` - drivers/flash/flash_stm32l5_u5.c : unable to use full 2MB flash with TF-M activated
* :github:`53227` - mgmt: mcumgr: Possible instability with USB CDC data transfer
* :github:`53223` - LE Audio: Add interleaved packing for LE audio
* :github:`53221` - Systemview trace id overlap
* :github:`53209` - LwM2M: Replace pathstrings from the APIs
* :github:`53194` - tests: kernel: timer: starve: DTS failure stm32f3_seco_d23
* :github:`53189` - Mesh CI failure with BT_MESH_LPN_RECV_DELAY
* :github:`53175` - Select pin properties from shield overlay
* :github:`53164` - mgmt: mcumgr: NMP Timeout with smp_svr example
* :github:`53158` - SPIM transaction timeout leads to crash
* :github:`53151` - fs: FAT_FS_API MKFS test uses driver specific calls
* :github:`53147` - usb: cdc_acm: log related warning promoted to error
* :github:`53141` - For pinctrl on STM32 pin cannot be defined as push-pull with low level
* :github:`53129` - Build fails on ESP32 when enabling websocket client API
* :github:`53103` - Zephyr shell on litex : number higher than 10 are printed as repeated hex
* :github:`53101` - esp32: The startup code hangs after reboot via sys_reboot(...)
* :github:`53094` - 扩展 Zperf 命令
* :github:`53093` - ARM: Ability to query CFSR on exception
* :github:`53059` - Bluetooth: peripheral GATT notification call takes a lot of time
* :github:`53049` - Bluetooth: LL assertion fail with peripherals connect/disconnect rounds
* :github:`53048` - Bluetooth: legacy advertising doesn't resume if CONFIG_BT_EXT_ADV=y
* :github:`53046` - Bluetooth: 失败 到 设置 security level 用于  第二 连接
* :github:`53043` - Bluetooth: Peripheral misses notifications from Central after setting security level
* :github:`53033` - tests-ci : libraries: encoding: jwt test Failed
* :github:`53034` - tests-ci : os: mgmt: info_net test No Console Output(Timeout)
* :github:`53035` - tests-ci : crypto: rand32: random_ctr_drbg test No Console Output(Timeout)
* :github:`53036` - tests-ci : testing: ztest: base.verbose_1 test No Console Output(Timeout)
* :github:`53037` - tests-ci : net: mqtt_sn: client test No Console Output(Timeout)
* :github:`53038` - tests-ci : net: socket: mgmt test No Console Output(Timeout)
* :github:`53039` - tests-ci : net: socket: af_packet.ipproto_raw test No Console Output(Timeout)
* :github:`53040` - tests-ci : net: ipv4: fragment test No Console Output(Timeout)
* :github:`53019` - random: Zephyr 启用 TEST_RANDOM_GENERATOR 当...时 它  不
* :github:`53012` - stm32u5: timer api: lptim: k_msleep is twice long as expected
* :github:`53010` - 定时器 大 drift 如果 硬件 定时器   低 resolution
* :github:`53007` - Bluetooth: Notification callback is called with incorrect connection reference
* :github:`53002` - 不正确 硬件 复位 cause 设置 用于 watchdog 复位 在...上 stm32h743zi
* :github:`52996` - kconfig: Use of multiple fragment files with OVERLAY_CONFIG not taking effect
* :github:`52995` - 增加 triage 权限 用于 dianazig
* :github:`52983` - Bluetooth: Audio: BT_CODEC_LC3_CONFIG_DATA fails to compile with _frame_blocks_per_sdu > 1
* :github:`52981` - LOG_MODE_MINIMAL  不 工作 带 USB_CDC 用于 nRF52840
* :github:`52975` - posix: clock: current method of capturing elapsed time leads to loss in seconds
* :github:`52970` - samples/net/wifi example does not work with ESP32
* :github:`52962` - Bluetooth non-functional on nRF5340 target
* :github:`52935` - 缺失 库
* :github:`52931` - Filesystem 写入 失败 带 一些 SD-Cards
* :github:`52925` - Using #define LOG_LEVEL 0 does not filter out logs
* :github:`52920` - qemu_cortex_r5: tests/ztest/base
* :github:`52918` - qemu_cortex_r5` CI fails
* :github:`52914` - drivers: adc: ADC_CONFIGURABLE_INPUTS confict between 2 ADCs
* :github:`52913` - twister 构建 失败 但 returns 退出 代码 的 0
* :github:`52909` - usb: usb don't work after switch from Zephyr 2.7.3 to 3.2.99 on i.MX RT1020
* :github:`52898` - mgmt: mcumgr: replace cmake functions without zephyr prefix to have zephyr prefix
* :github:`52882` - Sample applications that enable USB and error if it fails are incompatible with boards like thingy53 with auto-USB init (i.e. USB CDC for logging)
* :github:`52878` - Bluetooth: Unable use native_posix with shell demo
* :github:`52872` - Logging to USB CDC ACM limited to very low rate
* :github:`52870` - ESP32-C3 System clock resolution improvements
* :github:`52857` - Adafruit WINC1500 Wifi Shield doesn't work on nRF528XX
* :github:`52855` - Improve artifact generation for split build/test operation of twister
* :github:`52854` - twister 构建 失败 但 returns 退出 代码 的 0
* :github:`52838` - Bluetooth: audio：invalid ase state transition
* :github:`52833` - Bluetooth Controller assertion on sys_reboot() with active connections (lll_preempt_calc: Actual EVENT_OVERHEAD_START_US)
* :github:`52829` - kernel/sched: Fix SMP race on pend
* :github:`52818` - samples: subsys: usb: shell: sample.usbd.shell  fails - no output from console
* :github:`52817` - 测试 驱动 udc: dirvers.udc 失败
* :github:`52813` - stm32h7: dsi: ltdc: clock: PLL3: clock not set up correctly or side effect
* :github:`52812` - Various problems with pipes (Not unblocking, Data Access Violation, unblocking wrong thread...)
* :github:`52805` - Code crashing due to ADC Sync operation (STM32F4)
* :github:`52803` - Kconfig: STM32F4 UF2 family ID
* :github:`52795` - 移除 已弃用 tinycbor 模块
* :github:`52794` - Possible regression for printk() output of i2c sensor data on amg88xx sample
* :github:`52788` - Re-enable LVGL support for M0 processors.
* :github:`52784` - NRF_DRIVE_S0D1 选项  不 总是 设置 在...中  nordic,nrf-twi 和 nordic,nrf-twim nodes, 当...时 使用 shield?
* :github:`52779` - 错误 在...期间 增加  mcuboot folder 在...中 repo.
* :github:`52776` - ite: eSPI driver: espi_it8xxx2_send_vwire() is not setting valid flag along with respective virtual wire when invoked from app code.
* :github:`52754` - tests/drivers/bbram: Refactor to use a common prj.conf
* :github:`52749` - posix: getopt: cannot use getopt() in a standard way
* :github:`52739` - Newlib defines POSIX primitives when -std=gnu
* :github:`52721` - Minimal 日志记录  不 工作 如果 printk 和 引导 banner  禁用
* :github:`52718` - Simplify handling of fragments in ``net_buf``
* :github:`52709` - samples: subsys: nvs: sample.nvs.basic does not complete within twister default timeout
* :github:`52708` - samples: drivers: watchdog: sample.drivers.watchdog loops endlessly
* :github:`52707` - samples: subsys: task_wdt: sample.subsys.task_wdt loops endlessly
* :github:`52703` - tests: subsys: usb: device: usb.device USAGE FAULT exception
* :github:`52691` - cannot read octospi flash when partition size exceeds 4mb
* :github:`52690` - coredump: stm32l5: I-cache error on coredump backend in flash
* :github:`52675` - I2C: STM32F0 can't switch to HSI clock by default and change timing
* :github:`52673` - mcux: flexcan: forever waiting semaphore in can_send()
* :github:`52670` - tests: subsys: usb: device: usb.device hangs
* :github:`52652` - 驱动 sensors: bmi08x 配置 文件
* :github:`52641` - armv7: mpu: RASR size field incorrectly initialized
* :github:`52632` - MQTT over WebSockets: After hours of running time receiving published messages is strongly delayed
* :github:`52628` - spi: NXP MCUX LPSPI driver does not correctly change baud rate once configured
* :github:`52626` - Improve LLCP unit tests
* :github:`52625` - USB device: mimxrt685_evk_cm33: premature ZLP during control IN transfer
* :github:`52614` - Empty "west build --test-item" doesn't report warnings/errors
* :github:`52602` - tests: subsys: settings: file_littlefs: system.settings.file_littlefs.raw fails
* :github:`52598` - esp32c3 Unable to do any timing faster than 1ms
* :github:`52595` - Twister: unable 到 运行 测试 在...上 real 硬件
* :github:`52588` - ESP32c3 SPI driver DMA mode limited to 64 byte chunks
* :github:`52566` - 错误 在...期间 构建 esp32 samples/hello_world
* :github:`52563` - spi_transceive with DMA for STM32 does not work for devices with 16 bit words.
* :github:`52561` - fsl_flexcan missing flags
* :github:`52559` - Compiler cannot include C++ headers when both PICOLIBC and LIB_CPLUSPLUS options are set
* :github:`52556` - adc driver sample was failing with STM32 nucleo_f429zi board
* :github:`52548` - 晚 设备 驱动 initialization
* :github:`52539` - 损坏 linker 脚本 用于  esp32 平台
* :github:`52534` - Missing include to src/core/lv_theme.h in src/themes/mono/lv_theme_mono.h
* :github:`52528` - Zephyr support for Nordic devices Thingy with TFLM
* :github:`52527` - net: lwm2m: wrong SenML CBOR object link encoding
* :github:`52526` - Simplify lvgl.h file by creating more header files inside module's sub-filoders (src/widgets and src/layouts)
* :github:`52518` - lib: posix: usleep() does not follow the POSIX spec
* :github:`52517` - lib: posix: sleep() does not return the number of seconds left if interrupted
* :github:`52506` - GPIO multiple gaps cause incorrect pinout check
* :github:`52493` - net: lwm2m: add 32 bits floating point support
* :github:`52486` - Losing connection with JLink on STM32H743IIK6 with Zephyr 2.7.2
* :github:`52479` - incorrect canopennode SDO CRC
* :github:`52472` - 设置 compiler 选项 仅 用于  custom/external 模块
* :github:`52464` - LE Audio: Unicast Client failing to create the CIG
* :github:`52462` - uart: stm32: UART clock source not initialized
* :github:`52457` - compilation error with "west build -b lpcxpresso54114_m4 samples/subsys/ipc/openamp/ "
* :github:`52455` - ARC: MWDT: minimal libc includes
* :github:`52452` - drivers: pwm: loopback test fails on frdm_k64f
* :github:`52449` - net: ip: igmp: IGMP v2 membership reports are sent to 224.0.0.2 instead of the group being reported
* :github:`52448` - esp32: subsys: settings: not working properly on esp_wrover_kit
* :github:`52443` - Concerns 带 维护 分离 内核 设备 驱动 用于 fuel-gauge 和 charger ICs
* :github:`52415` - 测试 内核 定时器 timer_behavior: kernel.timer.timer 失败
* :github:`52412` - doc: mgmt: mcumgr: Clarify that hash in img_mgmt is a full sha256 hash and required
* :github:`52409` - STM32H7: ethernet: 设备 失败 到 接收 任何 IP 包 over ethernet 在...之后 接收 UDP/IP multicast 在  常量 rate 用于 一些 时间
* :github:`52407` - tests: subsys: mgmt: mcumgr: Test needed that enables all features/Kconfigs
* :github:`52404` - mgmt: mcumgr: Callback include file has file name typo
* :github:`52401` - mgmt: mcumgr: Leftover files after directory update
* :github:`52399` - cmake error
* :github:`52393` - Controller: ACL 包 NACKed 在...之后 数据 长度 更新
* :github:`52376` - Cannot 构建 apps 带 主 在...中  .cpp 文件
* :github:`52366` - LE Audio: Missing released callback for streams on ACL disconnect
* :github:`52360` - samples/net/sockets/socketpair does not run as expected
* :github:`52353` - bug: sysbuild lost board reversion here
* :github:`52352` - Questions about newlib library
* :github:`52351` - Bluetooth: Controller: ISOAL ASSERT failure
* :github:`52344` - Software-based Debounced GPIO
* :github:`52339` - usb: USB 设备 re-enabling  不 工作 在...上 Nordic 设备 回归问题
* :github:`52327` - websocket: websocket_recv_msg 损坏 当...时 there  不 数据 在...之后 头文件
* :github:`52324` - Bluetooth Mesh example seems broken on v3.2.99 - worked ok with v3.1.99
* :github:`52317` - drivers: wifi: eswifi: Offload sockets accessing invalid net_context, resulting in errors in FLASH_SR and blocking flash use
* :github:`52309` - SAM0 刷写 驱动 带 page emulated 启用  不 写入 数据 在 0 block
* :github:`52308` - pip3 is unable to build wheel for cmsis-pack-manager as part of the requirements.txt on Fedora 37.
* :github:`52307` - Linker Error using CONSOLE_GETCHAR and CONSOLE_GETLINE
* :github:`52301` - Zephyr-Hello World  不 工作
* :github:`52298` - CI fail multiple times due to download package from http://azure.archive.ubuntu.com/ubuntu failed.
* :github:`52296` - Regulator shell  不 构建 due 到 缺失 atoi define
* :github:`52291` - 板 thingy53: 启用 USB-CDC 由 默认
* :github:`52284` - unable to malloc during  tests/lib/cmsis_dsp/transform.cf64
* :github:`52280` - boards: thingy53 non-secure (thingy53_nrf5340_cpuapp_ns) does not build
* :github:`52276` - stm32: ST Kit B-L4S5I-IOT01A Octospi flash support
* :github:`52267` - http client includes chunking data in response body when making a non-chunked request and server responds with chunked data
* :github:`52262` - west 刷写 文件
* :github:`52242` - Fatal exception LoadProhibited from mcuboot when enabling newlib in wifi sample (esp32)
* :github:`52235` - counter_basic_api 测试 失败 到 构建 在...上 STM32 平台
* :github:`52228` - Bluetooth: L2CAP: receive a K-frame with payload longer than MPS if Enhanced ATT enabled
* :github:`52219` - jlink runner doesn't flash bin file if a hex file is present
* :github:`52218` - ADC read locked forever with CONFIG_DEBUG_OPTIMISATION=y on STM32U5
* :github:`52216` - spi_transceive with DMA on a STM32 slave returns value incorrect
* :github:`52211` - MCUX based QDEC driver
* :github:`52196` - Calling ``bt_le_ext_adv_stop()``  causes 失败 在...中 连接 当...时 支持 用于 multiple 连接  启用
* :github:`52195` - Bluetooth: GATT: add_subscriptions not respecting encryption
* :github:`52190` - [lpcxpresso55s28] 刷写 range 启动 从 保护 地址 哪个  不 compatible 带 最新 Jlink(v7.82a)
* :github:`52189` - 刷写 文件 系统 不 工作 在...上 stm32h735g_disco
* :github:`52181` - ADC Channel SCAN mode for STM32U5
* :github:`52171` - Bluetooth: BR/EDR: Inappropriate l2cap channel state set/get
* :github:`52169` - Mesh provisioning static OOB incorrect zero padding
* :github:`52167` - twister: Mechanism to pass CLI args through to ztest executable
* :github:`52154` - mgmt: mcumgr: Add Kconfig to automatically register handlers and mcumgr functionality
* :github:`52139` - ppp modem doesn't send NET_EVENT_L4_CONNECTED event
* :github:`52131` - tests-ci : kernel: timer: starve test No Console Output(Timeout)
* :github:`52125` - 定时器 accuracy 问题 带 STM32U5 板
* :github:`52114` - Can't make JerryScript Work with Zephyr
* :github:`52113` - Binary blobs in ``hal_telink`` submodules
* :github:`52111` - Incompatible LTO version of liblt_9518_zephyr.a
* :github:`52103` - STM32u5 dual bank flash issue
* :github:`52101` - ``bt_gatt_notify`` function does not notify data larger than 20 bytes
* :github:`52099` - mgmt: mcumgr: Rename fs_mgmt hash/checksum functions
* :github:`52095` - dfu/mcuboot: dfu/mcuboot.h used BOOT_MAX_ALIGN and BOOT_MAGIC_SZ but does not include ``bootutil/bootutil_public.h``
* :github:`52094` - STM32MP157 调试 method 使用 错误 GDB 移植 当...时 执行 命令 ``west 调试
* :github:`52085` - can: SAM M_CAN regression
* :github:`52079` - TLS handshake failure (after client-hello) with big_http_download sample
* :github:`52073` - ESP32-C3 UART1 not available after zephyr update to v3.2.99
* :github:`52065` - west: debugserver 命令  不 工作
* :github:`52059` - Bluetooth: conn: 在...中 multi role 配置 不正确 地址  设置 在...之后 advertising 恢复
* :github:`52057` - 测试 内核 定时器 starve: kernel.timer.starve 挂起
* :github:`52056` - Bluetooth: Missing LL data length update callback on Central and Peripheral sides
* :github:`52055` - Bluetooth: Controller: Broadcast scheduling issues
* :github:`52049` - Update mps2_an521_remote for compatibility with mps2_an521_ns
* :github:`52022` - RFC: API Change: mgmt: mcumgr: transport: Add query valid check function
* :github:`52021` - RFC: API Change: mgmt: mcumgr: Replace mgmt_ctxt struct with smp_streamer
* :github:`52009` - tests: kernel: fifo: fifo_timeout: kernel.fifo.timeout fails on nrf5340dk_nrf5340_cpuapp
* :github:`51998` - Nominate Attie Grande as zephyr Collaborator
* :github:`51997` - microTVM or zephyr bugs, No SOURCES given to Zephyr library
* :github:`51989` - stm32f303v(b-c)tx-pinctrl.dtsi, No such file or directory
* :github:`51984` - Bluetooth: Central rejects connection parameters update request from a connected peripheral
* :github:`51973` - Coding style problem, clang-format formatted code cannot pass CI.
* :github:`51951` - Zephyr Getting Started steps fail with Python v3.11
* :github:`51944` - lsm6dso sensnsor driver: to enable drdy in pulsed mode call ``lsm6dso_data_ready_mode_set()``
* :github:`51939` - mgmt: mcumgr: SMP is broken
* :github:`51931` - Failing unit test re. missing PERIPHERAL_ISO_SUPPORT KConfig selection
* :github:`51893` - LSM303dlhc sensor example not compiling for nRF52840
* :github:`51874` - Zephyr 3.1 bosch,bme280 device is in the final DTS and accessible, but DT_HAS_BOSCH_BME280_ENABLED=n
* :github:`51873` - sensor: bmp388: 缺失 如果 检查 around i2c 设备 就绪 函数
* :github:`51872` - Race condition in workqueue can lead to work items being lost
* :github:`51870` - Nucleo_h743zi 失败 到 format 存储 刷写 划分
* :github:`51855` - openocd: targeting wrong serial port / device
* :github:`51829` - qemu_x86: upgrading to q35 breaks networking samples.
* :github:`51827` - picolibc heap lock recursion mismatch
* :github:`51821` - native_posix: Cmake   运行 在 最少 twice 到 查找 ${CMAKE_STRIP}
* :github:`51815` - Bluetooth: bt_disable in loop with babblesim gatt test causes Zephyr link layer assert
* :github:`51798` - mgmt: mcumgr: image upload, then image erase, then image upload does not restart upload from start
* :github:`51797` - West espressif 安装 不 工作
* :github:`51796` - LE Audio: Improve stream coupling for CIS as the unicast client
* :github:`51788` - Questionable 测试 代码 在...中 ipv6_fragment 测试
* :github:`51785` - drivers/clock_control: stm32: Can support configure stm32_h7 PLL2 ?
* :github:`51780` - windows-curses Python package in requirements.txt can't install if using Python 3.11
* :github:`51778` - stm32l562e-dk: Broken TF-M psa-crypto sample
* :github:`51776` - POSIX API is not portable across arches
* :github:`51761` - Bluetooth : HardFault in hci_driver on sample/bluetooth/periodic_sync using nRF52833DK
* :github:`51752` - CAN documentation points to old sample locations
* :github:`51731` - Twister has a hard dependency on ``west.log``
* :github:`51728` - soc: xtensa: esp32_net: Remove binary blobs from source tree
* :github:`51720` - USB mass sample not working for FAT FS
* :github:`51714` - Bluetooth: Application with buffer that cannot unref it in disconnect handler leads to advertising issues
* :github:`51713` - 驱动 刷写 spi_nor: init 失败 当...时 刷写  busy
* :github:`51711` - Esp32-WROVER Unable to include the header file ``esp32-pinctrl.h``
* :github:`51693` - Bluetooth: Controller: Transmits packets longer than configured max len
* :github:`51687` - tests-ci : net: socket: tcp.preempt test Failed
* :github:`51688` - tests-ci : net: socket: tcp test Failed
* :github:`51689` - tests-ci : net: socket: poll test Failed
* :github:`51690` - tests-ci : net: socket: select test Failed
* :github:`51691` - tests-ci : net: socket: tls.preempt test Failed
* :github:`51692` - tests-ci : net: socket: tls test Failed
* :github:`51676` - stm32_hal -- undefined reference to "SystemCoreClock"
* :github:`51653` - mgmt: mcumgr: bt: issue with queued packets when device is busy
* :github:`51650` - Bluetooth: Extended adv reports with legacy data should also be discardable
* :github:`51631` - bluetooth: shell: linker error
* :github:`51629` - BLE stack execution fails with CONFIG_NO_OPTIMIZATIONS=y
* :github:`51622` - ESP32 mcuboot not support chip revision 1
* :github:`51621` - APPLICATION_CONFIG_DIR, CONF_FILE do not always pick up local ``boards/*.conf``
* :github:`51620` - Add Apache Thrift Module (from GSoC 2022 Project)
* :github:`51617` - RFC: Add Apache Thrift Upstream Module (from GSoC 2022 Project)
* :github:`51611` - check_compliance.py generates file checkpath.txt which isn't in .gitingore
* :github:`51607` - DT_NODE_HAS_COMPAT does not consider parents/path
* :github:`51604` - doc: is the documentation GDPR compliant since it uses Google Analytics without prompting the user about tracking?
* :github:`51602` - Stack overflow when using mcumgr fs_mgmt
* :github:`51600` - Bluetooth assert on flash erase using mcumgr
* :github:`51594` - mgmt: mcumgr: bt: thread freezes if device disconnects
* :github:`51588` - Doc:  Broken link in the "Electronut Labs Papyr" documentation page
* :github:`51566` - 损坏 网络 once lwM2M  恢复 在...之后 暂停
* :github:`51559` - lwm2m 测试  失败
* :github:`51549` - Memory report generation breaks if app and Zephyr is located on different Windows drives
* :github:`51546` - The blinky_pwm sample does not work on raspberry pi pico
* :github:`51544` - drivers/pwm/pwm_sam.c - update period and duty cycle issue (workaround + suggestions for fix)
* :github:`51529` - frdm_k64f: tests/net/socket/tls run failed on frdm_k64f
* :github:`51528` - spurious warnings when EXTRA_CFLAGS=-save-temps=obj is passed
* :github:`51521` - subsys: bluetooth: shell: gatt.c build fails with CONFIG_DEBUG_OPTIMIZATIONS and CONFIG_BT_SHELL=y
* :github:`51520` - samples: compression lz4 fails on small-ram stm32 platforms
* :github:`51508` - openocd: can't flash STM32H7 board using STLink V3
* :github:`51506` - it8xxx2_evb: 测试 suite 在...之后 watchdog 测试  display 失败 在...中  daily 测试
* :github:`51505` - drivers: modem: gsm: gsm_ppp_stop() does not change gsm->state
* :github:`51488` - lis2dw12 function latch is misunderstood with drdy latch
* :github:`51480` - tests-ci : drivers: watchdog test Build failure of mimxrt1064_evk
* :github:`51476` - Please 增加 documentation 或 sample 如何 到 使用 TLS_SESSION_CACHE 套接字 选项
* :github:`51475` - Twister: Mistake timeout as skipped
* :github:`51474` - driver: stm32: usb: add detach function support
* :github:`51471` - 网络 协议 MQTT: 当...时 qos=1, there   缺陷 在...中  subscription 和 publication
* :github:`51470` - tests-ci : 驱动 mipi_dsi: API 测试 构建 失败
* :github:`51469` - Intel CAVS: Failed in tests/kernel/spinlock
* :github:`51468` - mps3_an547:tests/lib/cmsis_dsp/filtering bus fault
* :github:`51464` - samples: drivers: peci: Code doesn't build for npcx7m6fb_evb board
* :github:`51458` - 仅 一个 instance 的 mcp2515
* :github:`51454` - Cmake error for Zephyr Sample Code in Visual Studio
* :github:`51446` - The PR #50334 breaks twister execution on various HW boards
* :github:`51437` - LoRaWan problem with uplink messages sent as a response to class C downlink
* :github:`51438` - tests-ci : net: http:  test Build failure
* :github:`51436` - tests-ci : drivers: drivers.watchdog: nxp-imxrt11xx series : watchdog build failure
* :github:`51435` - tests-ci : drivers: hwinfo: api test Failed
* :github:`51432` - Bluetooth: ISO: 移除 检查 用于 和 更改 seq_num 到 uint16_t
* :github:`51424` - tests: net: socket: tls: v4 dtls sendmsg test is testing v6
* :github:`51421` - tests: net: socket: tls: net.socket.tls region ``FLASH`` overflowed
* :github:`51418` - Intel CAVS: Assertion failed in tests/subsys/logging/log_links
* :github:`51406` - Blinky 不 执行 在...上 Windows
* :github:`51376` - Silabs WFX200 Binary Blob
* :github:`51375` - tests/lib/devicetree/devices/libraries.devicetree.devices: build failure (bl5340_dvk_cpuapp)
* :github:`51371` - hal: nxp: ARRAY_SIZE collision
* :github:`51370` - Driver error precision LPS22HH
* :github:`51368` - 测试 tests/subsys/cpp/cxx/cpp.main.picolibc: 构建 失败
* :github:`51364` - ESP32 WIFI: when allocating system_heap to PSRAM(extern ram), wifi station can't connet to ap(indicate that ap not found)
* :github:`51360` - I2C master read failure when 10-bit addressing is used with i2c_ll_stm32_v1
* :github:`51351` - I2C: ESP32 driver does not support longer clock stretching
* :github:`51349` - Turn power domains on/off directly
* :github:`51343` - qemu_x86_tiny doesn't place libc-hooks data in z_libc_partition
* :github:`51331` - lvgl: LV_FONT_CUSTOM_DECLARE does not work as string
* :github:`51323` - 内核 测试 Evaluate "platform_allow" usage 在...中 内核 测试
* :github:`51322` - 测试 内核 定时器 timer_behavior: kernel.timer.timer 失败
* :github:`51318` - x86_64: 线程 Local 存储 pointer 不 设置 在...之前 第一 线程 启动
* :github:`51301` - CI: mps3_an547: test failures
* :github:`51297` - Bluetooth: Implement H8 function from cryptographic toolbox
* :github:`51294` - ztest: Broken tests in main branch due to API-breaking change ``ZTEST_FAIL_ON_ASSUME``
* :github:`51290` - samples: application_development: external_lib: does not work on windows
* :github:`51276` - CAN 驱动 用于 ESP32 (TWAI)  不 启用  transceiver
* :github:`51265` - net: ip: cloning of net_pkt produces dangling ll address pointers and may flip overwrite flag
* :github:`51264` - drivers: ieee802154: nrf: wrapped pkt attribute access
* :github:`51263` - drivers: ieee802154: IEEE 802.15.4 L2 does not announce (but uses) promisc mode
* :github:`51261` - drivers: ieee802154: Drivers allocate RX packets from the TX pool
* :github:`51247` - Bluetooth: RPA expired callback inconsistently called
* :github:`51235` - nominate me as zephyr contributor
* :github:`51234` - it8xxx2_evb: The testcase tests/kernel/sleep/failed to run.
* :github:`51233` - up_squared: samples/boards/up_squared/gpio_counter run failed
* :github:`51228` - Bluetooth: Privacy in scan roles not updating RPA on timeout
* :github:`51223` - 问题 当...时 使用 fatfs example 在...中  out_of_tree_driver 带  文件 ff.h
* :github:`51214` - enc28j60 appears 到  unable 到 correctly 确定 网络 状态
* :github:`51208` - Bluetooth: Host: ``bt_le_oob_get_local`` gives incorrect address
* :github:`51202` - twister: Integration 错误 不 reported 也不 counted 在...中  控制台 output 但 当前 在...中  reports.
* :github:`51194` - samples/subsys/lorawan 构建 失败
* :github:`51185` - tests/drivers/counter/counter_basic_api 失败 到 构建 在...上 mimxrt685_evk_cm33
* :github:`51177` - Change SPI configuration (bitrate) with MCUXpresso SPI driver fails
* :github:`51174` - Bluetooth: l2cap needs check rx.mps when le_recv
* :github:`51168` - ITERABLE_SECTION_ROM stores data in RAM instead of ROM
* :github:`51165` - tools/fiptool/fiptool: 权限 拒绝
* :github:`51156` - esp32 wifi: 如何 到 使用 ap 模式 和 ap+station 模式
* :github:`51153` - modem: ppp: extract access technology when MODEM_CELL_INFO is enabled
* :github:`51149` - Esp32 wifi compilation error
* :github:`51146` - Running test: drivers:  disk: disk_access with  RAM disk  fails
* :github:`51144` - PR #51017 Broke GPIO builds for LPC11u6x platforms
* :github:`51142` - TestPlan generation 不 挑选 上 测试 缺失 测试 prefix
* :github:`51138` - 测试 tests/lib/cmsis_dsp/ 失败 在...上 一些 stm32 板
* :github:`51126` - Bluetooh: host: df: wrong size of a HCI command for connectionless CTE enable in AoD mode
* :github:`51117` - tests: kernel: workq: work: kernel.work.api fails test_1cpu_drain_wait
* :github:`51108` - Ethernet: Error frames are displayed when DHCP is suspended for a long time: <inf> net_dhcpv4: Received: 192.168.1.119
* :github:`51107` - Ethernet: Error frames are often displayed: <err> eth_mcux: ENET_GetRxFrameSize return: 4001
* :github:`51105` - esp32 wifi: http transmit rate is too slow
* :github:`51102` - issue installing zepyhr when i am using west cmd
* :github:`51076` - ADC channels 8-12 not working on LPC55s6X
* :github:`51074` - logging: syst: sample failure
* :github:`51070` - ModuleNotFoundError: No module named 'elftools'
* :github:`51068` - ModuleNotFoundError: No module named 'elftools'
* :github:`51065` - building tests/subsys/jwt failed on disco_l475_iot1  with twister
* :github:`51062` - lora_recv_async receives empty buffer after multiple receptions on sx12xx
* :github:`51060` - 10-bit addressing not supported by I2C slave driver for STM32 target
* :github:`51057` - Retrieve gpios used by a device (pinctrl)
* :github:`51048` - 固件 升级 问题 带 Mcumgr 在...上 STM32H743 controller
* :github:`51025` - mbedtls: 构建 警告
* :github:`51021` - openthread: 构建 警告
* :github:`51019` - NVS  允许 overwriting existing index 甚至 如果 there's 不 room 到 保持  旧 值
* :github:`51016` - mgmt: mcumgr: Add dummy shell buffer size Kconfig entry to shell mgmt
* :github:`51015` - Build Error for ST Nucleo F103RB
* :github:`51010` - Unable to communicate with LIS2DS12 on 52840DK or custom board
* :github:`51007` - Improve process around feature freeze exceptions
* :github:`51003` - Crash when using flexcomm5 as i2c on LPC5526
* :github:`50989` - Invalid ASE State Machine Transition
* :github:`50983` - RPI Pico usb hangs up in interrupt handler for composite devices
* :github:`50976` - JSON array encoding fails on array of objects
* :github:`50974` - DHCP (IPv4) NAK not respected when in renewing state
* :github:`50973` - DHCP (IPv4) seemingly dies by trying to assign an IP of 0.0.0.0
* :github:`50970` - SAME54_xpro 网络 驱动 不 attached
* :github:`50953` - LE Audio: Add support for setting ISO data path for broadcast sink
* :github:`50948` - SSD1306+lvgl sample fails to display
* :github:`50947` - stm32 static IPv4 networking in smp_svr sample application does not seem to work until a ping is received
* :github:`50940` - logging.log_output_ts64 fails on qemu_arc_hs5x
* :github:`50937` - 错误 当...时 构建 用于 esp32c3_devkitm
* :github:`50923` - RFC: Stable API change: Rework and improve mcumgr callback system
* :github:`50895` - ADC Voltage Reference issue with STM32U5 MCU
* :github:`50874` - Cant disable bluetooth for BLE peripheral after connection with Central
* :github:`50872` - 错误 在...期间 安装 python dependecies
* :github:`50868` - DHCP 从不 binds 如果  NAK  接收 期间  requesting 状态
* :github:`50853` - STM32F7 series can't run at frequencies higher than 180MHz
* :github:`50844` - zcbor 模块 API 哪个  使用 用于 mcu 引导 functionality  不 构建 在...中 cpp 文件 against v3.1.0
* :github:`50812` - MCUmgr udp sample fails with shell - BUS FAULT
* :github:`50801` - JSON parser fails on multidimensional arrays
* :github:`50789` - west: runners: blackmagicprobe: Doesn't work on windows due to wrong path separator
* :github:`50786` - Bluetooth: Host: Extended advertising reports may block the host
* :github:`50784` - LE Audio: Missing Media Proxy checks for callbacks
* :github:`50783` - LE Audio: 拒绝 ISO 数据 如果  stream  不 在...中  streaming 状态
* :github:`50782` - LE Audio:  MPL shell 模块  不 使用 opcodes
* :github:`50781` - LE Audio: ``mpl init`` causes warnings when adding objects
* :github:`50780` - LE Audio: Bidirectional handling of 2 audio streams as the unicast server when streams are configured separately not working as intended
* :github:`50778` - LE Audio: Audio shell: Unicast server cannot execute commands for the default_stream
* :github:`50776` - CAN 驱动 允许 发送 FD frames 没有 设备  设置 到 FD 模式
* :github:`50768` - storage: DT ``fixed-partition`` with ``status = "okay"`` requires flash driver
* :github:`50746` - Stale kernel memory pool API references
* :github:`50744` - net: ipv6: Allow on creating incomplete neighbor entries and routes in case of receiving Router Advertisement
* :github:`50735` - intel_adsp_cavs18: tests/boards/intel_adsp/hda_log/boards.intel_adsp.hda_log.printk failed
* :github:`50732` - net: tests/net/ieee802154/l2/net.ieee802154.l2 failed on reel_board due to build failure
* :github:`50709` - tests: arch: arm: arm_thread_swap fails on stm32g0 or stm32l0
* :github:`50684` - After enabling  CONFIG_SPI_STM32_DMA in project config file for STM32MP157-dk2 Zephyr throwing error
* :github:`50665` - MEC15xx/MEC1501: UART and special purpose pins missing pinctrl configuration
* :github:`50658` - Bluetooth: BLE stack notifications blocks host side for too long (``drivers/bluetooth/hci/spi.c`` and ``hci_spi``)
* :github:`50656` - 错误 定义 的 bank 大小 用于 intel 内存 management 驱动
* :github:`50655` - STM32WB55 Bus Fault when connecting then disconnecting then connecting then disconnecting then connecting
* :github:`50620` - fifo 测试 失败 带 CONFIG_CMAKE_LINKER_GENERATOR 启用 在...上 qemu_cortex_a9
* :github:`50614` - Zephyr if got the ip is "10.xxx.xxx.xxx" when join in the switchboard, then the device may can not visit the outer net, also unable to Ping.
* :github:`50603` - Upgrade to loramac-node 4.7.0 when it is released to fix async LoRa reception on SX1276
* :github:`50596` - Documentation: 损坏 链接 在...中  上一个 发布 documentation
* :github:`50592` - mgmt: mcumgr: Remove code/functions deprecated in zephyr 3.1 release
* :github:`50590` - openocd: Can't flash on various STM32 boards
* :github:`50587` - Regression in Link Layer Control Procedure (LLCP)
* :github:`50570` - samples/drivers/can/counter fails in twister for native_posix
* :github:`50567` - Passed test cases are reported as "Skipped" because of incomplete test log
* :github:`50565` - Fatal error after ``west flash`` for nucleo_l053r8
* :github:`50554` - Test uart async failed on Nucleo F429ZI
* :github:`50525` - Passed test cases reported as "Skipped" because test log lost
* :github:`50515` - Non-existing test cases reported as "Skipped" with reason  “No results captured, testsuite misconfiguration?” in test report
* :github:`50461` - Bluetooth: controller: LLCP: use of legacy ctrl Tx buffers
* :github:`50452` - mec172xevb_assy6906: The testcase tests/lib/cmsis_dsp/matrix failed to run.
* :github:`50446` - MCUX CAAM is disabled temporarily
* :github:`50438` - Bluetooth: Conn: Bluetooth stack becomes unusable when communicating with both centrals and peripherals
* :github:`50427` - Bluetooth: host: central connection context leak
* :github:`50426` - STM32: using SPI after STOP2 sleep causes application to hang
* :github:`50404` - Intel CAVS: tests/subsys/logging/log_immediate failed.
* :github:`50389` - Allow twister to be called directly from west
* :github:`50381` - BLE: 连接 slows 下 massively 当...时 connecting 到  第二 设备
* :github:`50354` - ztest_new: _zassert_base : return without post processing
* :github:`50345` - Network traffic occurs before Bluetooth NET L2 (IPSP) link setup complete
* :github:`50284` - Generated linker scripts break when ZEPHYR_BASE and ZEPHYR_MODULES share structure that contains symlinks
* :github:`50256` - I2C on SAMC21 sends out stop condition incorrectly
* :github:`50193` - Impossible to connect with a peripheral with BLE and zephyr 2.7.99, BT_HCI_ERR_UNKNOWN_CONN_ID error
* :github:`50192` - nrf_qspi_nor 驱动  崩溃 如果 power management  启用
* :github:`50188` - Avoid 使用 额外 net 缓冲区 用于 L2 头文件
* :github:`50149` - 测试 驱动 刷写 失败 在...上 nucleo_l152re 因为 的 错误 erase 刷写 大小
* :github:`50139` - net: ipv4: Add DSCP/ToS based QoS support
* :github:`50070` - LoRa: Support on RFM95 LoRa module combined with a nRF52 board
* :github:`50040` - shields: Settle on nodelabels naming scheme
* :github:`50028` - flash_stm32_ospi 写入 启用 失败 当...时 构建 带 TF-M
* :github:`49996` - tests: drivers: clock_control: nrf_lf_clock_start and nrf_onoff_and_bt fails
* :github:`49963` - Random crash on the L475 due to work->handler set to NULL
* :github:`49962` - RFC: Stable API Change:  SMP (Simple Management Protocol) transport API within MCUMgr drops ``zephyr_`` prefix in functions and type definitions and drop zst parameter from zephyr_smp_transport_out_fn
* :github:`49917` - http_client_req() sometimes hangs when peer disconnects
* :github:`49871` - zperf: Add support to stop/start download
* :github:`49870` - stm32 enables HSI48 clock with device tree
* :github:`49844` - shell 增加 中止 支持
* :github:`49843` - net: shell 扩展 ping 命令
* :github:`49821` - USB DFU implementation  不 工作 带 WinUSB 因为 的 缺失 设备 复位 API
* :github:`49811` - DHCP cannot obtain IP, when CONFIG_NET_VLAN is enabled
* :github:`49783` - net: ipv4: packet fragmentation support
* :github:`49746` - twister: extra test results
* :github:`49740` - LE Audio: Support for application-controlled advertisement for BAP broadcast source
* :github:`49711` - tests/arch/common/timing/arch.common.timing.smp fails for CAVS15, 18
* :github:`49648` - tests/subsys/logging/log_switch_format, log_syst build failures on CAVS
* :github:`49624` - Bluetooth: Controller: Recent RAM usage increase for hci_rpmsg build
* :github:`49621` - STM32WB55 BLE Extended Advertising support
* :github:`49620` - Add picolibc documentation
* :github:`49614` - acrn_ehl_crb: The testcase tests/kernel/sched/schedule_api failed to run.
* :github:`49611` - ehl_crb: 失败 到 运行 定时器 testcases
* :github:`49588` - Json parser is incorrect with undefined parameter
* :github:`49584` - STM32WB55 Failed read remote feature, remote version and LE set PHY
* :github:`49530` - Bluetooth: Audio: Invalid behavior testing
* :github:`49451` - Treat carrier UP/DOWN independently to interface UP/DOWN
* :github:`49413` - TI-AM62x: Add Zephyr Support for M4 and R5 cores
* :github:`49373` - BLE scanning - BT RX thread hangs on.
* :github:`49338` - Antenna switching for Bluetooth direction finding with the nRF5340
* :github:`49313` - nRF51822 sometimes hard fault on connect
* :github:`49298` - cc3220sf: add a launchpad_connector.dtsi
* :github:`49266` - Bluetooth: Host doesn't seem to handle INCOMPLETE per adv reports
* :github:`49234` - 选项 到 配置 coverage 数据 堆 大小
* :github:`49228` - ti: cc13xx_cc26xx: ADC support
* :github:`49210` - BL5340 board cannot build bluetooth applications
* :github:`49208` - drivers: modem: bg9x: not supporting UDP
* :github:`49148` - Asynchronous UART API triggers Zephyr assertion on STM32WB55
* :github:`49112` - lack 的 支持 用于 lpsram 缓存
* :github:`49069` - 日志 cdc_acm: hard 故障 消息  不 output
* :github:`49066` - Mcumgr img_mgmt_impl_upload_inspect() can cause unaligned memory access hard fault.
* :github:`49054` - STM32H7 apps are broken in C++ mode due to HAL include craziness
* :github:`49032` - espi saf testing disabled
* :github:`49026` - 增加  CI 检查 在...上 image 文件 大小 (specifically around 板
* :github:`49021` - uart async API  不 提供 所有 接收 数据
* :github:`48954` - several NXP devicetree bindings are missing
* :github:`48953` - 'intel,sha' is missing binding and usage
* :github:`48886` - 记录  进程 用于 treewide 更改
* :github:`48857` - samples: Bluetooth: Buffer size mismatch in samples/bluetooth/hci_usb for nRF5340
* :github:`48850` - Bluetooth: LLCP: possible access to released control procedure context
* :github:`48726` - net: tests/net/ieee802154/l2/net.ieee802154.l2 failed on reel board
* :github:`48625` - GSM_PPP API 保持 发送 命令 到 muxed AT 通道
* :github:`48616` - RFC: Change to clang-format coding style rules re binary operators
* :github:`48609` - drivers: gpio: expose gpio_utils.h to external GPIO drivers
* :github:`48603` - LoRa driver asynchronous receive callback clears data before the callback.
* :github:`48520` - clang-format: #include reorder due to default: SortIncludesOptions != SI_Never
* :github:`48505` - BLE stack can get stuck in connected state despite connection failure
* :github:`48473` - 设置 CONFIG_GSM_MUX_INITIATOR=n results 在...中  编译 错误
* :github:`48468` - GSM Mux does not transmit all queued data when uart_fifo_fill is called
* :github:`48394` - vsnprintfcb 写入 到 ``*str`` 如果 它  NULL
* :github:`48390` - [Intel Cavs] Boot failures on low optimization levels
* :github:`48317` - drivers: fpga: include driver for Lattice iCE40 parts
* :github:`48304` - bt_disable() does not work properly on nRF52
* :github:`48299` - SHT3XD_CMD_WRITE_TH_LOW_SET should be SHT3XD_CMD_WRITE_TH_LOW_CLEAR
* :github:`48150` - Sensor Subsystem: data types
* :github:`48148` - Sensor Subsystem: Base sensor DTS bindings
* :github:`48147` - ztest: before/after 函数  运行 在...上 不同 线程 哪个  cause potential 问题
* :github:`48037` - Grove LCD Sample Not Working
* :github:`48018` - ztest: static threads are not re-launched for repeated test suite execution.
* :github:`47988` - JSON parser not consistent on extra data
* :github:`47877` - ECSPI support for NXP i.MX devices
* :github:`47872` - Differentiating Samples, Tests & Demos
* :github:`47833` - Intel CAVS: cavstool.py 失败 到 提取 完成 日志 从 winstream 缓冲区 当...时 日志记录  frequent
* :github:`47830` - Intel CAVS: Build failure due to #47713 PR
* :github:`47817` - samples/modules/nanopb/sample.modules.nanopb fails with protobuf > 3.19.0
* :github:`47611` - ci: workflows: compliance: Add commit title to an error msg
* :github:`47607` - 设置 带 FCB backend  不 pass 测试 在...上 stm32h743
* :github:`47576` - undefined reference to ``__device_dts_ord_20`` When building with board hifive_unmatched on flash_shell samples
* :github:`47500` - twister: cmake: Failure of "--build-only -M" combined with "--test-only" for --device-testing
* :github:`47477` - qemu_leon3: tests/kernel/fpu_sharing/generic/ failed when migrating to new ztest API
* :github:`47329` - Newlib nano variant footprint reduction
* :github:`47326` - 驱动 WINC1500: 问题 带 缓冲区 allocation 当...时 使用 套接字
* :github:`47324` - drivers: modem: gsm_ppp: support common gpios
* :github:`47315` - LE Audio: CAP Initiator skeleton Implementation
* :github:`47299` - LE Audio: Advertising (service) data for one or more services/roles
* :github:`47296` - LE Audio: Move board files for nRF5340 Audio development kit upstream
* :github:`47274` - mgmt/mcumgr/lib: Rework of event callback framework
* :github:`47243` - LE Audio: Add support for stream specific codec configurations for broadcast source
* :github:`47242` - LE Audio: Add subgroup support for broadcast source
* :github:`47092` - driver: nrf: uarte: new dirver breaks our implementation for uart.
* :github:`47040` - 测试 驱动 gpio_basic_api 和 gpio_api_1pin: 转换 到 新 ztest API
* :github:`47014` - can: iso-tp: implementation test failed with twister on nucleo_g474re
* :github:`46988` - samples: net: openthread: coprocessor: RCP is missing required capabilities: tx-security tx-timing
* :github:`46986` - Logging (deferred v2) with a lot of output causes MPU fault
* :github:`46897` - tests: posix: fs: improve tests to take better advantage of new ztest features
* :github:`46844` - 定时器 驱动 可能  off-by-one 在...中 rapidly-presented timeouts
* :github:`46824` - Prevent new uses of old ztest API
* :github:`46598` - Logging with RTT backend on STM32WB strange behavier
* :github:`46596` - STM32F74X RMII 接口  不 工作
* :github:`46491` - Zephyr SDK 0.15.0 Checklist
* :github:`46446` - lvgl: Using sw_rotate with SSD1306 shield causes memory fault
* :github:`46351` - net: tcp: Implement fast-retransmit
* :github:`46326` - Async UART for STM32 U5 support
* :github:`46287` - Zephyr 3.2 release checklist
* :github:`46268` - Update RNDIS USB class codes for automatic driver loading by Windows
* :github:`46126` - pm_device causes assertion error in sched.c with lis2dh
* :github:`46105` - RFC: Proposal of Integrating Trusted Firmware-A
* :github:`46073` - IPSP (IPv6 over BLE) example stop working after a short time
* :github:`45921` - Runtime memory usage
* :github:`45910` - [RFC] Zbus: a message bus system
* :github:`45891` - mgmt/mcumgr/lib: Refactoring of callback subsystem in image management (DFU)
* :github:`45814` - Armclang 构建 失败 due 到 缺失 源码 文件
* :github:`45756` - Add overlay-bt-minimal.conf for smp_svr sample application
* :github:`45697` - RING_BUF_DECLARE broken for C++
* :github:`45625` - LE Audio: Update CSIP API with new naming scheme
* :github:`45621` - LE Audio: Update VCP API with new naming scheme
* :github:`45427` - Bluetooth: Controller: LLCP: Data structure for communication between the ISR and the thread
* :github:`45222` - drivers: peci: user space handlers not building correctly
* :github:`45218` - rddrone_fmuk66: I2C configuration incorrect
* :github:`45094` - stm32: Add USB HS device support to STM32H747
* :github:`44908` - Support ESP32 ADC
* :github:`44861` - WiFi 支持 用于 STM32 板
* :github:`44410` - drivers: modem: shell: ``modem send`` doesn't honor line ending in modem cmd handler
* :github:`44399` - Zephyr RTOS support for Litex SoC with 64 bit rocket cpu.
* :github:`44377` - ISO Broadcast/Receive sample not working with coded PHY
* :github:`44324` - 编译 错误 在...中 byteorder.h
* :github:`44318` - boards: arm: rpi_pico: Enable CONFIG_ARM_MPU=y for raspberry pi pico board
* :github:`44281` - Bluetooth: Use hardware encryption for encryption
* :github:`44164` - Implement the equivalent of PR #44102 in LLCP
* :github:`44055` - Immediate alert client
* :github:`43998` - posix: add include/posix to search path based on Kconfig
* :github:`43986` - interrupt feature for gpio_mcp23xxx
* :github:`43836` - stm32: g0b1: RTT doesn't work properly after stop mode
* :github:`43737` - Support compiling ```native_posix`` targets on Windows using the MinGW
* :github:`43696` - mgmt/mcumgr: RFC: Standardize Kconfig option names for MCUMGR
* :github:`43655` - esp32c3: Connection fail loop
* :github:`43647` - Bluetooth: LE multirole: connection as central is not totally unreferenced on disconnection
* :github:`43604` - Checkpatch: Support in-code ignore tags
* :github:`43411` - STM32 SPI DMA issue
* :github:`43330` - usb_dc_nrfx.c 启动 usbd_work_queue 带 不 名称
* :github:`43308` - driver: serial: stm32: uart will lost data when use dma mode[async mode]
* :github:`43294` - LoRaWAN stack & user ChannelsMask
* :github:`43286` - Zephyr 3.1 Release Checklist
* :github:`42998` -  board.dts 启用 peripherals 由 默认
* :github:`42910` - Bluetooth: Controller: CIS Data path setup: HCI ISO Data
* :github:`42908` - Bluetooth: Controller: CIG: LE Remove CIG
* :github:`42907` - Bluetooth: Controller: CIG: Disconnect: ACL disconnection leading to CIS Disconnection complete
* :github:`42906` - Bluetooth: Controller: CIG:  Disconnect:  Using HCI Disconnect:  Generate LL_CIS_TERMINATE_IND
* :github:`42905` - Bluetooth: Controller: CIG: LL Rejects: Remote request being rejected
* :github:`42902` - Bluetooth: Controller: CIG: Host reject: LE Reject CIS Request
* :github:`42900` - Bluetooth: Controller: CIG: LE Setup ISO Data Path
* :github:`42899` - Bluetooth: Controller: CIG: LE CIS Established Event
* :github:`42898` - Bluetooth: Controller: CIG: LE Accept CIS
* :github:`42897` - Bluetooth: Controller: CIG: LE CIS Request Event
* :github:`42896` - Bluetooth: Controller: CIG: LE Create CIS: NULL PDU scheduling
* :github:`42895` - Bluetooth: Controller: CIG: LE Create CIS: Control procedure with LL_CIS_REQ/RSP/IND PDU
* :github:`42894` - Bluetooth: Controller: CIG: LE Set CIG Parameters
* :github:`42700` - Support module.yml in zephyr repo
* :github:`42590` - mgmt/mcumgr/lib: RFC: Allow leaving out "rc" in successful respones and use "rc" only for SMP processing errors.
* :github:`42432` - i2c: unable to configure SAMD51 i2c clock frequency for standard (100 KHz) speeds
* :github:`42420` - mgmt/mcumgr/lib: Async image erase command with status check
* :github:`42374` - STM32L5: Entropy : Power Management not working due to entropy driver & stop mode
* :github:`42361` - OpenOCD 刷写 不 工作 在...上 cc1352r1_launchxl/cc26x2r1_launchxl
* :github:`41956` - Bluetooth: Controller: BIG: Synchronized receiver encryption support
* :github:`41955` - Bluetooth: Controller: BIG: Broadcaster encryption support
* :github:`41830` - CONF_FILE, OVERLAY_CONFIG parsing expands ``${ZEPHYR_<whatever>_MODULE_DIR}``
* :github:`41823` - Bluetooth: Controller: llcp: Remote request are dropped due to lack of free proc_ctx
* :github:`41822` - BLE IPSP sample cannot handle large ICMPv6 Echo Request
* :github:`41784` - virtio 设备 驱动
* :github:`41771` - 测试 驱动 adc: 测试 doesn't 构建 用于 mec172xevb_assy6906
* :github:`41765` - assert.h should not include non libc headers
* :github:`41694` - undefined reference to ``_open``
* :github:`41622` - Infinite mutual recursion when SMP and ATOMIC_OPERATIONS_C are set
* :github:`41606` - stm32u5: Re-implement VCO input and EPOD configuration
* :github:`41581` - STM32 subghzspi fails pinctrl setup
* :github:`41380` - stm32h7: Ethernet: 迁移 驱动 到  新 eth HAL API
* :github:`41213` - LE Audio: Update GA services to use the multi-instance macro
* :github:`41212` - LE Audio: Store of bonded data
* :github:`41209` - LE Audio: MCS support for multiple instances
* :github:`41073` - twister: no way to specify arguments for the binary zephyr.exe
* :github:`40982` - 构建 系统 West: 增加  警告 当...时 使用 repository  不 匹配 manifest
* :github:`40972` - Power management support for MEC172x
* :github:`40944` - BUILTIN_STACK_CHECKER 和 MPU_STACK_GUARD 带  线程 使用  FPU  故障  bulltin 栈 checker
* :github:`40928` - mgmt/mcumgr/lib: Check image consistency after writing last chunk
* :github:`40924` - mgmt/mcumgr/lib:  不 re-upload image, 由 默认 到  次 slot
* :github:`40868` - Add a pre and post initialization among CONFIG_APPLICATION_INIT_PRIORITY
* :github:`40850` - 增加 Zephyr 日志记录 支持 到 mgmt/mcumgr/lib
* :github:`40833` - driver: i2c: TCA9546a: Have compilation fails when driver init priority missmatch
* :github:`40642` - Why does CMake wrongly believe the rimage target is changing?
* :github:`40582` - how the zephyr supportting with running cadence hifi4 lx7,reset_vectorXEA2.s ?
* :github:`40561` - BLE notification and indication callback data are difficult to pass to other threads...
* :github:`40560` - Callbacks lack context information...
* :github:`39740` - Road from pinmux to pinctrl
* :github:`39712` - bq274xx sensor - Fails to compile when CONFIG_PM_DEVICE enabled
* :github:`39598` - 使用 的 __noinit 带 ecc 内存 挂起 系统
* :github:`39520` - 增加 支持 用于  BlueNRG-LP SoC
* :github:`39431` - arduino_nano_33_ble_sense: 增加 更多 设备 到  设备 Tree
* :github:`39331` - ti: cc13xx_cc26xx: watchdog timer driver
* :github:`39234` - Add support for the Sensririon SCD30 CO2 sensor
* :github:`39194` - 进程 调查 GitHub 代码 审查 replacements
* :github:`39037` - CivetWeb samples fail to build with CONFIG_NEWLIB_LIBC
* :github:`39025` - Bluetooth: Periodic Advertising, Filter Accept List, Resolving list related variable name abbreviations
* :github:`38947` - 问题 带 SMP 命令 发送 over  UART
* :github:`38880` - ARC: ARCv2: qemu_arc_em / qemu_arc_hs don't work with XIP disabled
* :github:`38668` - ESP32S I2S
* :github:`38570` - Process: binary blobs in Zephyr
* :github:`38450` - Python 脚本 用于 检查 PR 错误
* :github:`38346` - twister command line parameter clean up and optimizate twister documents
* :github:`38291` - Make Zephyr modules compatible with PlatformIO libdeps
* :github:`38251` - cmake: DTC_OVERLAY_FILE flags cancel board <board>.overlay files
* :github:`38041` - Logging-related 测试 失败 在...上 qemu_arc_hs6x
* :github:`37855` - STM32 - kconfigs to determine if peripheral is available
* :github:`37346` - STM32WL LoRa 增加  当前 在...中 "suspend_to_idle" 状态
* :github:`37056` - 澄清 设备 power 状态
* :github:`36953` - <err> lorawan: MlmeConfirm failed : Tx timeout
* :github:`36951` - twister: report information about tests instability
* :github:`36882` - MCUMGR: fs upload fail for first time file upload
* :github:`36724` - The road to a stable Controller Area Network driver API
* :github:`36601` - 增加 input 支持 到 audio_codec
* :github:`36553` - LoRaWAN Sample: ``join accept`` but "Join failed"
* :github:`36544` - RFC: API Change: Bluetooth: Read Multiple
* :github:`36343` - Bluetooth: Mesh: Modularizing the proxy feature
* :github:`36301` - soc: cypress: Port Zephyr to Cypress CYW43907
* :github:`36297` - Move BSS section to the end of image
* :github:`35986` - POSIX: multiple definition of posix_types
* :github:`35812` - ESP32 Factory app partition is not bootable
* :github:`35316` - log_panic() 挂起 内核
* :github:`35238` - ieee802.15.4 support for stm32wb55
* :github:`35237` - 构建 增强 twister 到 遵循 所有 module.yml 在...中 模块 list
* :github:`35177` - example-application: Add example library & tests
* :github:`34949` - console Bluetooth LE backend
* :github:`34597` - Mismatch between ``ot ping`` and ``net ping``
* :github:`34536` - Simple event-driven framework
* :github:`34324` - RTT  不 工作 在...上 STM32
* :github:`34269` - LOG_MODE_MINIMAL BUILD error
* :github:`34049` - Nordic nrf9160 switching between drivers and peripherals
* :github:`33876` - Lora sender sample build error for esp32
* :github:`33704` - BLE Shell Scan application filters
* :github:`32875` - Benchmarking Zephyr vs. RIOT-OS
* :github:`32756` - Enable mcumgr shell management to send responses to UART other than assigned to shell
* :github:`32733` - RS-485 support
* :github:`32339` - reimplement tests/kernel/timer/timer_api
* :github:`32288` - 增强  ADC functionality 在...上  STM32 设备 到 所有 available ADC 通道
* :github:`32213` - Universal 错误 代码 类型
* :github:`31959` - BLE firmware update STM32WB stuck in loop waiting for CPU2
* :github:`31298` - tests/kernel/gen_isr_table failed on hsdk and nsim_hs_smp sometimes
* :github:`30391` - Unit Testing in Zephyr
* :github:`30348` - XIP can't be enabled with ARC MWDT toolchain
* :github:`30212` - Disk rewrites same flash page multiple times.
* :github:`30159` - Clean code related to dts fixup files
* :github:`30042` - usbd: support more than one configuration descriptors
* :github:`30023` - 设备 model: 增加 调试 helpers 用于 当...时 device_get_binding() 失败
* :github:`29986` - Add support for a single node having multiple bus types
* :github:`29832` - Redundant 错误 检查 的 函数 uart_irq_update() 在...中 ``tests/drivers/uart/uart_basic_api/src/test_uart_fifo.c``
* :github:`29495` - SD card slow write SPI/Fatfs/stm32
* :github:`29160` - arm: Always include arch/arm/include
* :github:`29136` - usb: 增加 USB 设备 栈 shell 支持
* :github:`29135` - usb: 允许  instances 的  USB class 到  启用 和 禁用 在 runtime
* :github:`29134` - usb: 允许 更多 extensive 设置 的  设备 descriptor
* :github:`29133` - usb: USB 设备 栈  存储 和 验证  设备 状态
* :github:`29132` - usb: USB 设备 栈  track 和 检查  状态 的 control transfers
* :github:`29087` - Moving (some) boards to their own repo/module
* :github:`28998` - net: 如果 扩展 list 的 admin/operational 状态 的 网络 接口
* :github:`28872` - Support ESP32 as Bluetooth controller
* :github:`28864` - sanitycheck: Make sanitycheck test specifiacation compatible
* :github:`28617` - 启用 CONFIG_TEST 用于 所有 samples
* :github:`27819` - Memory Management for MMU-based devices for LTS2
* :github:`27258` - Ring 缓冲区  不 允许 到 partially put/get 数据
* :github:`26796` - 中断 在...上 Cortex-M  不 工作 带 CONFIG_MULTITHREADING=n
* :github:`26392` - e1000 ethernet driver needs to be converted to DTS
* :github:`26109` - devicetree: overloaded DT_REG_ADDR() and DT_REG_SIZE() for PCI devices
* :github:`25917` - Bluetooth: Deadlock with TX of ACL data and HCI commands (command blocked by data)
* :github:`25417` - net: socket: socketpair: check for ISR context
* :github:`25407` - No tests/samples covering socket read()/write() calls
* :github:`25055` - Redundant 刷写 shell 命令
* :github:`24653` - device_pm: 澄清 和 记录 usage
* :github:`23887` - drivers: modem: question: Should modem stack include headers to put into zephyr/include?
* :github:`23165` - macOS 设置 失败 到 构建 用于 lack 的 "elftools" Python 打包
* :github:`23161` - I2C and sensor deinitialization
* :github:`23072` - #ifdef __cplusplus missing in tracking_cpu_stats.h
* :github:`22049` - Bluetooth: IRK handling issue when using multiple local identities
* :github:`21995` - Bluetooth: controller: 拆分 移植 的 连接 event 长度
* :github:`21724` - dts: edtlib: handle child-binding or child-child-binding as 'normal' binding with compatible
* :github:`21446` - samples: add SPI slave
* :github:`21239` - devicetree: Generation of the child-bindigs items as a common static initializer
* :github:`20707` - Define GATT service at run-time
* :github:`20262` - dt-binding 用于 定时器
* :github:`19713` - usb: 调查 如果 网络 缓冲区   使用 在...中 USB 设备 栈 和 USB 驱动
* :github:`19496` - insufficient test case coverage for log subsystem
* :github:`19356` - LwM2M sample reorganization: split out LwM2M source into object-based .c files
* :github:`19259` - doc: two-column tricks for HTML breaks PDF
* :github:`19243` - Support SDHC & samples/subsys/fs on FRDM-K64F
* :github:`19152` - MK22F51212 MPU defines missing
* :github:`18892` - POSIX subsys: transition to #include_next for header consistency
* :github:`17171` - Insufficient code coverage for lib/os/fdtable.c
* :github:`16961` - 模块 增加  SHA1 检查 到 avoid 更新 模块 在...中  过去
* :github:`16942` - Missing test case coverage for include/misc/byteorder.h functions
* :github:`16851` - west flash error on zephyr v1.14.99
* :github:`16444` - drivers/flash/flash_simulator: 支持 用于 必需 读取 alignment
* :github:`16088` - Verify POSIX PSE51 API requirements
* :github:`15453` - Kconfig  enforce  在 最多 一个 控制台 驱动  启用 在  时间
* :github:`15181` - ztest issues
* :github:`14753` - nrf52840_pca10056: Leading spurious 0x00 byte in UART output
* :github:`14577` - Address latency/performance in nRF51 timer ISR
* :github:`13170` - Porting guide for advanced board (multi CPU SoC)
* :github:`12504` - STM32: add USB_OTG_HS example
* :github:`12401` - Target Capabilities / Board Directory Layout Capabilities
* :github:`12367` - Power management strategy of Zephyr can't work well on nRF52 boards.
* :github:`11594` - Cleanup GNUisms to make the code standards compliant
* :github:`9045` - A resource-saving programming model
* :github:`6198` - unit test: Add unit test example which appends source files to SOURCES list
* :github:`5697` - Driver API review/cleanup/rework
* :github:`3849` - 减少  overall 内存 usage 的  LwM2M 库
* :github:`2837` - Ability to use hardware-based block ciphers
* :github:`2647` - Better cache APIs needed.
