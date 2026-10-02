:orphan:

..
  此处应包含：移除/弃用的 API、新开发板、新驱动、显著功能。如果你认为某个新功能对用户有用，
  请将其放在第一段"其他增强"下；如果你认为某内容值得在项目媒体（发布博客、发布直播）中提及，
  请将其放在"主要增强"下。
..
  如果你在描述某个功能或特性，考虑将其添加到实际项目文档中，而非发布说明，这样信息才不会随时间丢失。
..
  不要列出 bug 修复和小更改，它们已在 git log 中，这不是变更日志。
..
  条目是否有包含详情的链接？直接添加链接即可，如果你认为需要更多细节，
  请将其放在链接显示的内容中。
..
  你是否在考虑自动生成此内容？什么都不要放。
..
  该条目是否要求用户更改其应用程序？请将其放到迁移指南中。（TODO：将移除的 API 部分移到迁移指南）

.. _zephyr_4.5:

Zephyr 4.5.0（工作草稿）
############################

我们很高兴宣布 Zephyr 4.5.0 版本的发布。

本次发布的主要增强功能包括：

**Infineon TriCore 支持**
  Zephyr 现在支持 :zephyr:board-catalog:`Infineon TriCore 架构 <#arch=tricore>`。

**新驱动类**

  Zephyr 4.5 添加了几个新的驱动 API，包括：

  - :ref:`时钟监视器 <clock_monitor_api>` 用于运行时观察时钟频率
  - :ref:`LIN <lin>` 用于本地互连网络（LIN）汽车串行总线

**新子系统**

  Zephyr 4.5 添加了几个新的子系统 API，包括：

  - :ref:`精密计时 <precision_timing>` 用于共享的受检时间运算、时钟操作和 PI 控制
  - :ref:`视频 <video_api>` 用于控制视频驱动

从 Zephyr v4.4.0 迁移到 Zephyr v4.5.0 时所需或建议的更改概述可在单独的 :ref:`迁移指南 <migration_4.5>` 中找到。

以下章节按组件提供详细的更改列表。

安全漏洞相关
******************************

本次发布解决了以下 CVE：

* :cve:`2026-8718` 截至 2026-08-08 处于保密期

* :cve:`2026-9263` 截至 2026-06-28 处于保密期

API 更改
***********

..
  仅包含移除、弃用和新的 API。更改内容放在迁移指南中。

移除的 API 和选项
========================

* 架构

   * ARM

      * ``CONFIG_PLATFORM_SPECIFIC_INIT``
      * ``z_arm_platform_init()``

   * RISC-V

      * ``CONFIG_EXTRA_EXCEPTION_INFO``

   * x86

      * ``CONFIG_SSE``
      * ``CONFIG_SSE_FP_MATH``

   * Xtensa

      * ``CONFIG_XTENSA_BACKTRACE_EXCEPTION_DUMP_HOOK``

* 蓝牙

  * 控制器

    * ``CONFIG_BT_CTRL_ADV_ADI_IN_SCAN_RSP``

  * 主机

    * ``CONFIG_BT_RECV_CONTEXT`` 选项及其选项 ``CONFIG_BT_RECV_WORKQ_SYS``
      和 ``CONFIG_BT_RECV_WORKQ_BT`` 已被移除。主机现在始终在专用的蓝牙 RX 工作队列上
      处理低优先级 HCI 数据包（即原 ``CONFIG_BT_RECV_WORKQ_BT`` 行为）。参见迁移指南。

    * 选定的主机工作项已从系统工作队列移到专用的蓝牙 RX 工作队列。
      从那些工作项到达的应用程序回调现在在蓝牙 RX 线程中运行。参见迁移指南
      了解受影响的回调族。

    * ``CONFIG_BT_HCI_RAW_H4`` 和 ``CONFIG_BT_HCI_RAW_H4_ENABLE`` Kconfig
      选项已被移除。自 Zephyr 4.2 起它们已无效果，
      当时 HCI 原始层已改为对所有缓冲区无条件使用 H:4 数据包编码。
      仍设置这些选项的应用程序可简单删除它们。

    * ``CONFIG_BT_AUTO_PHY_UPDATE``，由 ``BT_AUTO_PHY_CENTRAL`` 和
      ``BT_AUTO_PHY_PERIPHERAL`` 选项取代
    * ``_bt_gatt_ccc``
    * ``BT_GATT_CCC_INITIALIZER``
    * ``CONFIG_BT_CONN_TX_MAX``
    * ``CONFIG_BT_FIXED_PASSKEY``
    * ``bt_passkey_set()``
    * ``BT_PASSKEY_INVALID``

  * Mesh

    * ``CONFIG_BT_MESH_BLOB_IO_FLASH_WITH_ERASE``
    * ``CONFIG_BT_MESH_BLOB_IO_FLASH_WITHOUT_ERASE``

  * 服务

    * ``CONFIG_BT_DIS_MANUF``
    * ``CONFIG_BT_DIS_MODEL``

* 开发板

    * 移除了以下弃用的开发板别名：

      * ``arduino_uno_r4_minima``
      * ``arduino_uno_r4_wifi``
      * ``esp32c6_devkitc``
      * ``esp32_devkitc_wroom/esp32/procpu``
      * ``esp32_devkitc_wroom/esp32/appcpu``
      * ``esp32_devkitc_wrover/esp32/procpu``
      * ``esp32_devkitc_wrover/esp32/appcpu``
      * ``neorv32``
      * ``panb511evb``
      * ``raytac_an54l15q_db/nrf54l15/cpuapp``
      * ``scobc_module1``
      * ``xiao_esp32c6``

    * 以下开发板已被弃用并重命名：

      * ``adafruit_metro_rp2350/rp2350b/m33`` 改为 ``adafruit_metro_rp2350/rp2350b/m33_0``
      * ``motion_2350_pro/rp2350a/m33`` 改为 ``motion_2350_pro/rp2350a/m33_0``
      * ``motion_2350_pro/rp2350a/hazard3`` 改为 ``motion_2350_pro/rp2350a/hazard3_0``
      * ``beetle_rp2350/rp2350a/m33`` 改为 ``beetle_rp2350/rp2350a/m33_0``
      * ``beetle_rp2350/rp2350a/hazard3`` 改为 ``beetle_rp2350/rp2350a/hazard3_0``
      * ``pico2_spe/rp2350a/m33`` 改为 ``pico2_spe/rp2350a/m33_0``
      * ``pico_plus2/rp2350b/m33`` 改为 ``pico_plus2/rp2350b/m33_0``
      * ``pico_plus2/rp2350b/hazard3`` 改为 ``pico_plus2/rp2350b/hazard3_0``
      * ``rpi_pico2/rp2350a/m33`` 改为 ``rpi_pico2/rp2350a/m33_0``
      * ``rpi_pico2/rp2350a/m33/w`` 改为 ``rpi_pico2/rp2350a/m33_0/w``
      * ``rpi_pico2/rp2350a/m33/mcuboot`` 改为 ``rpi_pico2/rp2350a/m33_0/mcuboot``
      * ``rpi_pico2/rp2350a/m33/w/mcuboot`` 改为 ``rpi_pico2/rp2350a/m33_0/w/mcuboot``
      * ``rpi_pico2/rp2350a/hazard3`` 改为 ``rpi_pico2/rp2350a/hazard3_0``
      * ``xiao_rp2350/rp2350a/m33`` 改为 ``xiao_rp2350/rp2350a/m33_0``
      * ``xiao_rp2350/rp2350a/hazard3`` 改为 ``xiao_rp2350/rp2350a/hazard3_0``
      * ``rp2350_zero/rp2350a/m33`` 改为 ``rp2350_zero/rp2350a/m33_0``
      * ``rp2350_zero/rp2350a/hazard3`` 改为 ``rp2350_zero/rp2350a/hazard3_0``
      * ``rp2350b_core/rp2350b/m33`` 改为 ``rp2350b_core/rp2350b/m33_0``
      * ``rp2350b_core/rp2350b/hazard3`` 改为 ``rp2350b_core/rp2350b/hazard3_0``
      * ``w5500_evb_pico2/rp2350a/m33`` 改为 ``w5500_evb_pico2/rp2350a/m33_0``
      * ``w6100_evb_pico2/rp2350a/m33`` 改为 ``w6100_evb_pico2/rp2350a/m33_0``
      * ``w6300_evb_pico2/rp2350a/m33`` 改为 ``w6300_evb_pico2/rp2350a/m33_0``

* 构建系统

    * ``CONFIG_BUILD_NO_GAP_FILL``
    * ``cmake/app/boilerplate.cmake``
    * 名为 ``<board>_<revision>.conf`` 的开发板修订版 Kconfig 片段，由
      ``<board>_<revision>_defconfig`` 取代
    * ``zephyr_code_relocate(FILES ...)`` 中的模式展开，由 ``file(GLOB ...)`` 取代
    * CMake ``flash``、``debug``、``debugserver``、``attach`` 和 ``rtt`` 目标，
      由对应的 ``west`` 命令取代
    * ``WEST_DIR`` 构建系统变量
    * ``ZephyrUnittest`` CMake 包，由
      ``find_package(Zephyr COMPONENTS unittest)`` 取代

* CAN

    * ``bus-speed``
    * ``bus-speed-data``

* 比较器

    * :dtcompatible:`nxp,kinetis-acmp` 的 ``nxp,enable-output-pin``、``nxp,use-unfiltered-output``、``nxp,high-speed-mode``、
      ``nxp,enable-sample``、``nxp,filter-count``、``nxp,filter-period`` 和 ``nxp,window-mode``
      属性

* 计数器

    * ``CONFIG_COUNTER_MAXIM_DS3231``
    * :dtcompatible:`nxp,lptmr` 的 ``prescaler`` 属性

* hawkBit

    * ``<zephyr/mgmt/hawkbit.h>``

* 设备树

    * ``zephyr,memory-region-mpu``

* 以太网

    * 带有 ``CONFIG_ETH_NUMAKER`` 的 NuMaker 以太网驱动已被
      :kconfig:option:`CONFIG_ETH_NUMAKER_DWC_ETHER_1000` 取代。参见迁移指南。

* 调试

  * 实验性 ``CONFIG_ASSERT_CUSTOM_HEADER`` 选项及其 ``zephyr_custom_assert.h``
    包含钩子已按实验性 API 策略在未经弃用期的情况下被移除。
    需要自定义断言处理的应用程序应改为覆盖弱 zassert 钩子
    （``zassert_fail``/``zassert_vprint``/``zassert_post_action``）。

* LLEXT

    * ``llext_get_fn_table``，由 ``llext_get_fn_table_entry`` 取代

* Mbed TLS

    * ``CONFIG_MBEDTLS_MD``
    * ``CONFIG_MBEDTLS_LMS``
    * ``CONFIG_MBEDTLS_TLS_VERSION_1_2``
    * ``CONFIG_MBEDTLS_DTLS``
    * ``CONFIG_MBEDTLS_TLS_VERSION_1_3``
    * ``CONFIG_MBEDTLS_TLS_SESSION_TICKETS``
    * ``CONFIG_MBEDTLS_CTR_DRBG_ENABLED``
    * ``CONFIG_MBEDTLS_HMAC_DRBG_ENABLED``

* MCUboot

    * ``CONFIG_MCUBOOT_BOOTLOADER_MODE_SWAP_WITHOUT_SCRATCH``，由
      :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_MODE_SWAP_USING_MOVE` 取代

* MCUmgr

    * ``CONFIG_MCUMGR_GRP_OS_INFO_HARDWARE_INFO_SHORT_HARDWARE_PLATFORM``

* 网络

    * ``CONFIG_NET_TC_SKIP_FOR_HIGH_PRIO``
    * ``CONFIG_NET_SOCKETS_POLL_MAX``
    * ``CONFIG_NET_TEST_PROTOCOL``，连同其唯一被测系统的
      ``samples/net/sockets/tcp`` 示例。
    * ``CONFIG_NET_GPTP_CLOCK_ACCURACY_*``
    * ``net_ipv6_set_hop_limit()``
    * ``net_if_ipv4_get_netmask()``
    * ``net_if_ipv4_set_netmask()``
    * ``net_if_ipv4_set_netmask_by_index()``
    * ``openthread_state_changed_cb_register()``
    * ``openthread_state_changed_cb_unregister()``
    * ``openthread_start()``
    * ``openthread_api_mutex_lock()``
    * ``openthread_api_mutex_try_lock()``
    * ``openthread_api_mutex_unlock()``
    * ``struct openthread_state_changed_cb``
    * ``TLS_CREDENTIAL_SERVER_CERTIFICATE``
    * ``start_11r_roaming``
    * ``IEEE802154_HW_SLEEP_TO_TX``

* Nordic

    * :dtcompatible:`nordic,owned-memory` 和
      :dtcompatible:`nordic,owned-partitions` 的 ``owner-id``、``perm-read``、``perm-write``、``perm-execute``、``perm-secure`` 和
      ``non-secure-callable`` 属性
    * ``CONFIG_BOARD_ENABLE_CPUNET``，由 :kconfig:option:`CONFIG_SOC_NRF53_CPUNET_ENABLE` 取代
    * ``CONFIG_GPIO_AS_PINRESET``
    * ``CONFIG_NRFS_LOCAL_DOMAIN_DVFS_SCALE_DOWN_AFTER_INIT``，由
      :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_HSFLL_LOCAL_REQ_LOW_FREQ` 取代
    * ``CONFIG_SOC_DCDC_NRF52X``
    * ``CONFIG_SOC_DCDC_NRF52X_HV``
    * ``CONFIG_SOC_DCDC_NRF53X_APP``
    * ``CONFIG_SOC_DCDC_NRF53X_NET``
    * ``CONFIG_SOC_DCDC_NRF53X_HV``

* POSIX

    * ``CONFIG_POSIX_READER_WRITER_LOCKS``

* 随机数

    * ``CONFIG_CTR_DRBG_CSPRNG_GENERATOR``
    * ``CONFIG_CS_CTR_DRBG_PERSONALIZATION``

* Shell

    * ``kernel log_level``，由 ``log enable`` 取代

* SPI

    * :c:macro:`SPI_CONFIG_DT`、:c:macro:`SPI_CONFIG_DT_INST`、
      :c:macro:`SPI_DT_SPEC_GET`、:c:macro:`SPI_DT_SPEC_INST_GET`、:c:macro:`SPI_DT_IODEV_DEFINE`、
      :c:macro:`SPI_DT_INST_IODEV_DEFINE` 和 :c:macro:`SPI_CS_CONTROL_INIT` 的可选延迟参数已被移除。

* Stream Flash

    * ``stream_flash_erase_page()``

* 跟踪

  * ``_track_list_k_*`` 对象跟踪列表头、``SYS_PORT_TRACK_NEXT()`` 宏以及
    :file:`include/zephyr/tracing/tracking.h` 头文件。对象跟踪现通过
    :ref:`对象核心框架 <object_cores_api>` 枚举对象。

* ZTest

    * ``CONFIG_ZTEST_SHUFFLE_SUITE_REPEAT_COUNT``
    * ``CONFIG_ZTEST_SHUFFLE_TEST_REPEAT_COUNT``

* 已移除对 imgtool 的 West 签名支持，该支持在 Zephyr 4.0 中已弃用。

* 已移除 ``scripts/logging/dictionary/log_parser_uart.py`` 字典日志脚本，
  该脚本在 Zephyr 4.3 中已弃用。请改用
  :zephyr_file:`scripts/logging/dictionary/live_log_parser.py`。

* 已移除 ``west flash``、``west debug`` 及其他调用 runner 的命令的 ``--skip-rebuild`` 选项，
  该选项在 Zephyr 4.3 中已弃用。请改用 ``--no-rebuild``。

弃用的 API 和选项
===========================

* 音频编解码器

  * :c:struct:`audio_codec_api` 结构体已被弃用。音频编解码器驱动现在应使用
    :c:macro:`DEVICE_API` 宏来声明其驱动 API。

* 蓝牙

  * :kconfig:option:`CONFIG_BT_CUSTOM` 栈选择已被弃用。它源于整个蓝牙主机
    可被卸载到 Zephyr 蓝牙 API 之后的时代，树中已无用户；HCI 传输层是常规设备驱动。
    基于 HCI 的栈 :kconfig:option:`CONFIG_BT_HCI` 是树中唯一的选择；该选项本身
    保留作为树外栈的扩展点。

  * HCI 驱动 ``setup()`` 操作、:c:func:`bt_hci_setup`、
    :c:struct:`bt_hci_setup_params` 和 :kconfig:option:`CONFIG_BT_HCI_SETUP` 已被
    弃用。驱动现在改为在其 :c:member:`bt_hci_driver_api.open` 内部
    通过其自身传输层执行厂商特定初始化。参见迁移指南。

* 构建系统

  * ``zephyr_file_copy()`` CMake 函数已被弃用。请改用原生
    ``file(COPY_FILE ...)`` CMake 命令。

* 时钟控制

  * 函数 :c:func:`z_nrf_clock_control_get_onoff` 已被弃用。
    参见 :ref:`迁移指南 <migration_4.5>` 了解详细信息。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_K32SRC_ACCURACY` 已被弃用。
    参见 :ref:`迁移指南 <migration_4.5>` 了解详细信息。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_K32SRC` 已被弃用。
    参见 :ref:`迁移指南 <migration_4.5>` 了解详细信息。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_SUBSYS_HFAUDIO` 已被弃用。
    参见 :ref:`迁移指南 <migration_4.5>` 了解详细信息。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_SUBSYS_HF24M` 已被弃用。
    参见 :ref:`迁移指南 <migration_4.5>` 了解详细信息。

  * 宏 :c:macro:`CLOCK_CONTROL_NRF_SUBSYS_HF` 已被弃用。
    参见 :ref:`迁移指南 <migration_4.5>` 了解详细信息。

  * 枚举 :c:enumerator:`clock_control_nrf_type` 已被弃用。
    参见 :ref:`迁移指南 <migration_4.5>` 了解详细信息。

  * Kconfig 选项 :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF` 及所有依赖 kconfig 已被
    弃用。参见 :ref:`迁移指南 <migration_4.5>` 了解详细信息。Kconfig
    位于 ``drivers/clock_control/Kconfig.nrf`` 和 ``modules/hal_nordic/nrfx/Kconfig``
    文件中。

* 控制器局域网（CAN）

  * :c:func:`can_set_state_change_callback` 已弃用，改为
    :c:func:`can_init_state_change_callback`、:c:func:`can_add_state_change_callback` 和
    :c:func:`can_remove_state_change_callback`。新的 API 函数允许添加多个 CAN
    控制器状态变化回调（:github:`117889`）。

* CPU 负载

  * :kconfig:option:`CONFIG_CPU_LOAD_METRIC` 和 :c:func:`cpu_load_metric_get` 已弃用。
    CPU 负载指标模块已合并到统一的 :ref:`cpu_load` 模块中；请使用
    :kconfig:option:`CONFIG_CPU_LOAD` 配合
    :kconfig:option:`CONFIG_CPU_LOAD_BACKEND_RUNTIME_STATS` 后端和 :c:func:`cpu_load_get_cpu`。

* :abbr:`DMIC（数字麦克风接口）`

  * :c:struct:`_dmic_ops` 结构体已被弃用。DMIC 驱动现在应使用
    :c:macro:`DEVICE_API` 宏来声明其驱动 API。

* 燃料表

  * 已弃用各种燃料表属性枚举和联合体字段，改为
    带有显式单位后缀的新版本。

* LoRa

  * 已将 :c:func:`lora_recv_duty_cycle` 重命名为 :c:func:`lora_recv_duty_cycle_async`，
    以与现有的同步/异步命名约定保持一致。

* MCUmgr

  * :c:type:`smp_transport_get_mtu_fn` 类型和 :c:struct:`smp_transport_api_t` 的
    ``get_mtu`` 成员已被弃用，因为 SMP 层不使用它们。详见
    :ref:`迁移指南 <migration_4.5>`。

  * :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_UART_MTU` 和
    :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_SHELL_MTU` 已被弃用，因为它们仅设置
    已弃用的 ``get_mtu`` 回调返回的值。详见 :ref:`迁移指南 <migration_4.5>`。

* Nordic

  * 内部 SoC 平台 Kconfig 符号 ``NRF_PLATFORM_HALTIUM`` 和
    ``NRF_PLATFORM_LUMOS`` 已被弃用。请改用特定的 SOC_SERIES_* Kconfig 选项。

  * sysbuild Kconfig 选项 ``SB_CONFIG_NRF_HALTIUM_GENERATE_UICR`` 已被
    重命名为 :kconfig:option:`SB_CONFIG_NRF_GENERATE_UICR`。

  * Nordic SoC 头文件 :file:`<haltium_power.h>` 和 :file:`<haltium_pm_s2ram.h>`
    已分别重命名为 :file:`<soc_power.h>` 和 :file:`<soc_pm_s2ram.h>`。

* Raspberry Pi

  * RP2350 ``SOC_RP2350A_HAZARD3``、``SOC_RP2350A_M33``、``SOC_RP2350B_HAZARD3`` 和
    ``SOC_RP2350B_M33`` Kconfig 符号，以及 ``soc.yml`` 中对应的裸 ``hazard3``/``m33``
    cpuclusters，已弃用，改为 ``SOC_RP2350A_HAZARD3_0``、
    ``SOC_RP2350A_M33_0``、``SOC_RP2350B_HAZARD3_0`` 和 ``SOC_RP2350B_M33_0`` 及其
    ``hazard3_0``/``m33_0`` cpuclusters，以将 RP2350 双核集群命名与硬件
    模型 v2 对齐。旧的 Kconfig 符号和 ``soc.yml`` 条目将在
    未来发布中移除。所有树内开发板已完成迁移。

* 环形缓冲区

  * 环形缓冲区项 API（:c:func:`ring_buf_item_init`、:c:func:`ring_buf_item_put`、
    :c:func:`ring_buf_item_get`、:c:func:`ring_buf_item_space_get`）已弃用，改为
    :c:struct:`sys_ringq`（参见 :ref:`fixed_size_ringq_api`）。

  * 零拷贝 claim/finish API（:c:func:`ring_buf_put_claim`、:c:func:`ring_buf_put_finish`、
    :c:func:`ring_buf_get_claim`、:c:func:`ring_buf_get_finish`）已弃用，改为
    新的 :c:func:`ring_buf_put_ptr` / :c:func:`ring_buf_get_ptr` API。仍在使用它的代码必须
    启用 :kconfig:option:`CONFIG_RING_BUFFER`。

  * :kconfig:option:`CONFIG_RING_BUFFER` 已弃用。环形缓冲区 API 现在是仅头文件且
    始终可用，因此不再需要该选项来使用环形缓冲区。它现在仅作为弃用开关，
    用于在树外代码迁移到替代 API 期间恢复遗留的 claim/finish 和项 API。

* 网络缓冲区

  * :c:func:`net_buf_max_len` 和 :c:func:`net_buf_simple_max_len` 已弃用。请使用
    :c:func:`net_buf_tailroom` 和 :c:func:`net_buf_simple_tailroom`。参见
    :ref:`迁移指南 <migration_4.5>` 了解详细信息。

* 网络

  * 已弃用 LLMNR 支持（:kconfig:option:`CONFIG_LLMNR_RESOLVER` 和
    :kconfig:option:`CONFIG_LLMNR_RESPONDER`）。LLMNR 正在逐步淘汰；请使用
    mDNS（:kconfig:option:`CONFIG_MDNS_RESOLVER` /
    :kconfig:option:`CONFIG_MDNS_RESPONDER`）替代。

* 网络链路层

  * 已弃用 :kconfig:option:`CONFIG_NET_L2_PTP`。
    改用 :kconfig:option:`CONFIG_NET_L2_PTP_TIMESTAMPING`。

* SPI

  * SPI API 现在使用包容性术语（controller/peripheral、SDO/SDI）。
    旧名称已弃用：``SPI_OP_MODE_MASTER``/``SPI_OP_MODE_SLAVE``（请使用
    :c:macro:`SPI_OP_MODE_CONTROLLER`/:c:macro:`SPI_OP_MODE_PERIPHERAL`）、
    :c:struct:`spi_config` 的 ``slave`` 成员（请使用 ``peripheral``）、
    ``SPI_MOSI_OVERRUN_*`` 宏（请使用
    :c:macro:`SPI_SDO_OVERRUN_UNKNOWN`、:c:macro:`SPI_SDO_OVERRUN_DT`、
    :c:macro:`SPI_SDO_OVERRUN_DT_INST`）、``CONFIG_SPI_SLAVE``（请使用
    :kconfig:option:`CONFIG_SPI_PERIPHERAL`）、``zephyr,bt-hci-spi-slave`` 设备树
    兼容字符串（请使用 :dtcompatible:`zephyr,bt-hci-spi-peripheral`）以及
    迁移指南中列出的绑定的 ``mosi-gpios``/``miso-gpios`` 风格设备树属性。

* 定时器

  * 新的 :c:func:`sys_clock_no_timeout` 钩子用于处理
    :kconfig:option:`CONFIG_SYSTEM_CLOCK_SLOPPY_IDLE`，取代
    :c:func:`sys_clock_set_timeout` 使用 ``ticks=K_TICKS_FOREVER`` 的调用。
  * 新的 :c:func:`sys_clock_idle_enter` 钩子用于处理进入低功耗状态，
    取代 :c:func:`sys_clock_set_timeout` 使用 ``idle=true`` 的调用。

* :abbr:`USB（通用串行总线）`

  * 已弃用 :dtcompatible:`st,stm32u5-otghs-phy` 的属性 ``clock-reference``。
    不要指定该属性；底层驱动不再需要它。

* 视频

  * 视频驱动 API（``<zephyr/drivers/video.h>``）中的所有函数已移到
    视频子系统（``<zephyr/video/video.h>``）。应用程序只需重命名 ``#include`` 即可。

* West

  * ``west spdx --init`` 已弃用。使用
    :kconfig:option:`CONFIG_BUILD_OUTPUT_META` 的构建现在会向 CMake 请求
    ``west spdx`` 读取的基于文件的 API，因此构建目录不再需要在配置前
    准备。参见 :ref:`west-spdx`。

* 工作队列

  * :c:member:`k_work_q.thread` 已弃用。请改用 :c:member:`k_work_q.thread_id`。

新的 API 和选项
====================

..
  在此处链接新 API，如果你认为有必要可以分组，无需花哨，
  只需列出链接，其中应包含文档。如果你认为需要添加更多细节，
  请将其添加到 API 文档代码中。

.. zephyr-keep-sorted-start re(^\* \w) ignorecase

* ADC

  * 可选的 :c:member:`adc_driver_api.ref_get` 回调和
    :c:func:`adc_ref_get`，使应用程序和
    :c:func:`adc_raw_to_millivolts_dt` 能够对任何 :c:enum:`adc_reference` 使用
    驱动拥有的运行时毫伏刻度。静态
    :c:member:`adc_driver_api.ref_internal` 仍然是回调为 NULL 时
    :c:enumerator:`ADC_REF_INTERNAL` 的回退。
    :c:func:`adc_raw_to_millivolts_dt` 在 :c:func:`adc_ref_get` 失败时
    回退到通道 DT ``zephyr,vref-mv``。
  * :kconfig:option:`CONFIG_ADC_STM32_VREFINT_CALIBRATE`（在初始化时和
    ``sequence.calibrate`` 时从 VREFINT 测量 VREF+）

* 架构

  * :kconfig:option:`CONFIG_ARM_MPU_CM7_UNMAPPED_REGION`（Arm Cortex-M7 的
    未映射地址的兜底 MPU 区域，erratum 1013783 的解决方法）
  * :kconfig:option:`CONFIG_CORTEX_M_ERRATUM_440977_WORKAROUND`（在提升优先级的
    BASEPRI 写入后保留 ISB；在 Arm Cortex-M7 上默认启用，该 erratum
    440977 适用于 r0p0/r0p1 核心。其他 Cortex-M 核心不再在中断
    加锁/解锁快速路径中执行屏障，加快了内核热路径）
  * :kconfig:option:`CONFIG_EXCEPTION_DUMP`（默认启用，可禁用以在
    尺寸受限的构建中编译掉故障处理器输出）
  * :kconfig:option:`CONFIG_RISCV_ISA_EXT_ZKR`（RISC-V Zkr 熵源扩展，
    从 ``riscv,isa-extensions`` 设备树属性启用）
  * :kconfig:option:`CONFIG_RISCV_USER_STRING_NLEN_VALIDATE`（RISC-V，在
    ``arch_user_string_nlen()`` 中逐块验证用户字符串，而不是依赖
    故障修复，适用于加载访问故障不精确的 SoC）
  * :kconfig:option:`CONFIG_RISCV_SOC_HAS_SYSCALL_INTMASK`（RISC-V SoC 钩子，
    用于在用户模式系统调用主体中屏蔽中断，而不清除 ``mstatus.MIE``）
  * :kconfig:option:`CONFIG_RISCV_SOC_SYSCALL_CLOSE_ECALL`（RISC-V SoC 钩子，
    用于在用户模式系统调用主体运行前关闭 ecall 异常，
    适用于无法在该异常开放期间传递由主体引发的故障的 SoC）

* 音频

  * :c:member:`pcm_stream_cfg.gain_db`
  * :c:struct:`audio_codec_eq_cfg`

* 蓝牙

  * 音频

    * :c:func:`bt_aics_client_free_instance`
    * :c:func:`bt_ascs_register`
    * :c:func:`bt_ascs_unregister`
    * :c:func:`bt_bap_unicast_client_qos_from_group`
    * :c:func:`bt_bap_qos_cfg_eq`
    * :c:member:`bt_bap_unicast_group_info.c_to_p_interval`
    * :c:member:`bt_bap_unicast_group_info.p_to_c_interval`
    * :c:member:`bt_bap_unicast_group_info.c_to_p_latency`
    * :c:member:`bt_bap_unicast_group_info.p_to_c_latency`
    * :c:member:`bt_bap_unicast_group_info.framing`
    * :c:member:`bt_bap_unicast_group_info.packing`
    * :c:member:`bt_bap_unicast_group_info.has_been_connected`
    * :c:member:`bt_bap_unicast_group_info.c_to_p_ft`
    * :c:member:`bt_bap_unicast_group_info.p_to_c_ft`
    * :c:member:`bt_bap_unicast_group_info.iso_interval`
    * :c:member:`bt_cap_initiator_cb.unicast_start_codec_configured`
    * :c:member:`bt_cap_initiator_cb.unicast_start_qos_configured`
    * :c:member:`bt_cap_initiator_cb.unicast_start_enabled`
    * :c:member:`bt_cap_initiator_cb.unicast_start_connected`
    * :c:member:`bt_cap_initiator_cb.unicast_start_started`
    * :c:member:`bt_cap_initiator_cb.unicast_stop_disabled`
    * :c:member:`bt_cap_initiator_cb.unicast_stop_stopped`
    * :c:member:`bt_cap_initiator_cb.unicast_stop_released`
    * :c:func:`bt_vocs_client_free_instance`

  * 经典

    * :kconfig:option:`CONFIG_BT_SMP_DERIVE_LTK`
    * :kconfig:option:`CONFIG_BT_SMP_DERIVE_LK`
    * :c:func:`bt_sdp_unregister_service`

  * HCI 驱动

    * :c:macro:`BT_HCI_PKT_CMD_DEFINE`
    * :c:macro:`BT_HCI_PKT_CMD_DEFINE_STATIC`
    * :c:func:`bt_hci_pkt_reset_cmd`
    * :c:func:`bt_hci_pkt_push_cmd_hdr`
    * :c:func:`bt_hci_pkt_pull_cmd_complete`
    * :c:func:`bt_hci_pkt_pull_cmd_status`
    * :c:func:`bt_hci_pkt_parse_cmd_rsp`
    * :c:func:`bt_hci_lockstep_cmd_send_sync`
    * :c:func:`bt_hci_lockstep_reset`
    * :c:func:`bt_hci_set_public_addr` 和 :c:func:`bt_hci_get_public_addr`
    * :c:func:`bt_hci_can_close`

  * 主机

    * :c:func:`bt_att_get_max_notify_size`
    * :c:func:`bt_conn_take`
    * :c:func:`bt_conn_drop`
    * :c:func:`bt_id_reset_irk`
    * :c:macro:`BT_IRK_SIZE`
    * :c:func:`bt_iso_chan_state_str`
    * :c:member:`bt_iso_chan_ops.send_failed`
    * :c:func:`bt_iso_get_chan_by_conn`
    * :c:func:`bt_le_per_adv_update_did`
    * :c:member:`bt_le_adv_param.tx_power` 和 :c:enumerator:`BT_LE_ADV_OPT_TX_POWER`，
      用于按扩展广播集请求特定的 TX 功率级别。
    * :c:member:`bt_conn_cb.le_param_update_rejected`
    * ``BT_HCI_QUIRK_NO_FLOW_CONTROL`` HCI 设备怪癖，用于
      广播但拒绝控制器到主机流控命令的控制器。
    * :c:member:`bt_rfcomm_dlc.rx_credit_limit`，用于配置每-DLC 初始 RX 信用计数。
    * :c:func:`bt_rfcomm_dlc_recv_complete`，用于将 RX 信用归还给对等方。应用程序
      可从 :c:member:`bt_rfcomm_dlc_ops.recv` 回调返回 ``-EINPROGRESS`` 以延迟
      缓冲区释放和流控信用补充，直到处理完成。
    * :c:func:`bt_le_bond_addr_res_support`、:c:enum:`bt_le_addr_res_support` 和
      :c:member:`bt_conn_auth_info_cb.addr_res_support_read`
    * :c:enumerator:`BT_LE_SCAN_OPT_EXT_FILTER_POLICY`
    * :kconfig:option:`CONFIG_BT_SCAN_EXT_FILTER_POLICY`
    * :c:member:`bt_le_scan_recv_info.direct_addr`

  * Mesh

    * :c:struct:`bt_mesh_lpn_timing`
    * :c:func:`bt_mesh_stat_lpn_timing_get`
    * :c:func:`bt_mesh_stat_lpn_timing_reset`
    * :kconfig:option:`CONFIG_BT_MESH_LPN_OFFER_WAIT_TIMEOUT`

* 时钟控制

  * :kconfig:option:`CLOCK_CONTROL_NRF_ONOFF`
  * 以下函数现在支持兼容 ``nordic,nrf-clock-hfclk``、
    ``nordic,nrf-clock-lfclk``、``nordic,nrf-clock-hfclk192m``、``nordic,nrf-clock-hfclk24m``、
    ``nordic,nrf-clock-hfclkaudio``、``nordic,nrf-clock-xo``、``nordic,nrf-clock-xo24m`` 的设备：
    参见 :ref:`迁移指南 <migration_4.5>` 了解详细信息。
    * :c:func:`clock_control_request`
    * :c:func:`clock_control_request_sync`
    * :c:func:`clock_control_release`
    * :c:func:`clock_control_cancel_or_release`

* CPUFreq

  * :kconfig:option:`CONFIG_CPU_FREQ_POLICY_TIMING_NOISE`

* 加密

  * :c:enumerator:`CRYPTO_CIPHER_MODE_CFB`
  * :c:enumerator:`CRYPTO_CIPHER_MODE_OFB`
  * :c:func:`cipher_cfb_op`
  * :c:func:`cipher_ofb_op`

* 调试

  * 引入 ZASSERT，一种细粒度的按模块/文件断言机制。
    每个源文件通过 ``ZASSERT_MODULE(<MODULE>)`` 选择断言模块，
    级别从 ``CONFIG_ASSERT_MODULE_<MODULE>_LEVEL`` 解析，
    可按文件覆盖。
    有四个级别：off（编译掉）、terse（仅检查）、
    normal（检查 + 仅位置）和 verbose（检查 + 位置、条件和消息）。
    失败行为可通过弱钩子 ``zassert_fail()``、
    ``zassert_vprint()`` 和 ``zassert_post_action()`` 自定义。
    遗留的 ``__ASSERT()`` 族继续作为 ZASSERT ``DEFAULT`` 模块上的
    薄兼容层基本不变地工作。

* 设备树

  * :c:macro:`DT_IRQN_BY_NAME`
  * :c:macro:`DT_INST_IRQN_BY_NAME`

* 显示

  * :c:enumerator:`PIXEL_FORMAT_YUYV`
  * :c:macro:`PANEL_PIXEL_FORMAT_YUYV`

* 熵

  * :kconfig:option:`CONFIG_ENTROPY_RISCV_ZKR`（基于
    RISC-V Zkr 扩展 ``seed`` CSR 的架构熵驱动）

* FIDO2

  * :c:func:`fido2_up_reset`
  * :c:macro:`FIDO2_BLE_SERVICE_UUID_VAL`
  * :c:macro:`FIDO2_BLE_SERVICE_DATA_PAIRING_MODE`
  * :kconfig:option:`CONFIG_FIDO2_TRANSPORT_BLE`
  * :kconfig:option:`CONFIG_FIDO2_BLE_REQUIRE_AUTHENTICATED_LINK`
  * :kconfig:option:`CONFIG_FIDO2_BLE_RX_WORKQ_STACK_SIZE`
  * :kconfig:option:`CONFIG_FIDO2_BLE_CONTROL_POINT_LENGTH`
  * :kconfig:option:`CONFIG_FIDO2_BLE_RX_QUEUE_DEPTH`
  * :kconfig:option:`CONFIG_FIDO2_BLE_TX_FRAME_COUNT`
  * :kconfig:option:`CONFIG_FIDO2_BLE_KEEPALIVE_INTERVAL_MS`
  * :kconfig:option:`CONFIG_FIDO2_BLE_RX_TIMEOUT_MS`

* 燃料表

  * :c:func:`fuel_gauge_set_buffer_prop` 和可选的
    :c:member:`fuel_gauge_driver_api.set_buffer_property` 回调，用于写入
    可变长度缓冲区属性，与 :c:func:`fuel_gauge_get_buffer_prop` 对称。

* 触觉

  * :c:enum:`haptics_monitor`
  * :c:enum:`haptics_monitor_type`
  * :c:enum:`haptics_source`
  * :c:enum:`haptics_trigger_type`
  * :c:union:`haptics_config`
  * :c:func:`haptics_calibrate`
  * :c:func:`haptics_monitor_get`
  * :c:func:`haptics_monitor_set`
  * :c:func:`haptics_select_source`
  * :c:func:`haptics_set_level`
  * :c:func:`haptics_set_trigger`
  * :c:func:`haptics_stream_samples`
  * :c:func:`haptics_trigger`

* HWSPINLOCK

  * :c:macro:`HWSPINLOCK_SPINLOCK_ARRAY_DT_DEFINE`
  * :c:macro:`HWSPINLOCK_SPINLOCK_ARRAY_DT_INST_DEFINE`
  * :c:macro:`HWSPINLOCK_COMMON_CONFIG_FROM_DT_NODE`
  * :c:macro:`HWSPINLOCK_COMMON_CONFIG_FROM_DT_INST`

* Kconfig

  * 添加 ``dt_partition_mtd`` 预处理器函数（:github:`111599`）

* 内核

  * :c:func:`k_thread_runtime_stats_is_enabled`
  * :c:func:`atomic_test_and_set_bit_to`
  * :c:macro:`K_MSGQ_DEFINE_STATIC`
  * :c:macro:`K_MSGQ_DEFINE_TYPE`
  * :c:macro:`K_MSGQ_DEFINE_STATIC_TYPE`
  * :c:func:`k_sleep_ticks`
  * 中断控制 API 的命名空间等效形式，推荐用于新代码；
    无前缀的名称仍完全受支持：
    :c:func:`k_irq_lock`、:c:func:`k_irq_unlock`、:c:func:`k_irq_enable`、
    :c:func:`k_irq_disable`、:c:func:`k_irq_is_enabled`、
    :c:func:`k_irq_connect_dynamic` 和 :c:func:`k_irq_disconnect_dynamic`

* LIN

  * :c:func:`lin_start`
  * :c:func:`lin_stop`
  * :c:func:`lin_configure`
  * :c:func:`lin_get_config`
  * :c:func:`lin_send`
  * :c:func:`lin_receive`
  * :c:func:`lin_response`
  * :c:func:`lin_read`
  * :c:func:`lin_wakeup_send`
  * :c:func:`lin_set_event_callback`
  * :c:func:`lin_set_rx_filter`
  * :c:func:`lin_get_transceiver`
  * :kconfig:option:`CONFIG_LIN`

* LoRa

  * :c:func:`lora_recv_duty_cycle`
  * :c:func:`lora_recv_duty_cycle_async`
  * :c:func:`lora_energy_detect`
  * :c:func:`lora_rssi`

* 管理

  * MCUmgr

    * 添加了对 SPI MCUmgr SMP 传输的支持，可通过
      :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_SPI` 启用。

    * 添加实验性 :ref:`传输管理组 <mcumgr_smp_group_11>`：
      :kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT`、
      :kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_LOCKING`、
      :kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_MAX_BRIDGES`、
      :kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_GROUP_ID_DEFAULT`、
      :kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_GROUP_ID_CUSTOM_VALUE`、
      :kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_GROUP_ID_CUSTOM_VALUE_GROUP_ID`、
      :kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_GROUP_ID_CUSTOM_FUNCTION` 和
      :kconfig:option:`CONFIG_MCUMGR_GRP_TRANSPORT_INFO_FUNCTIONS`。

* 调制解调器

  * :c:enumerator:`CELLULAR_MODEM_INFO_SERIAL_NUMBER`

* 多媒体流水线

  * :kconfig:option:`CONFIG_MPIPE`（参见 :ref:`mpipe`）

* 网络

  * 添加 :c:func:`net_eth_set_if_type_wifi` 用于将以太网接口类型设置为 Wi-Fi。
  * 添加公共邻居缓存 API：:c:func:`net_if_ipv4_nbr_flush` 和
    :c:func:`net_if_ipv6_nbr_flush` 丢弃接口已学习的邻居，
    :c:func:`net_if_ipv4_nbr_rm` 和 :c:func:`net_if_ipv6_nbr_rm`
    移除单个邻居。在以太网链路上，IPv4 缓存即 ARP 缓存。
  * 添加 :c:func:`net_dhcpv4_set_reboot_hint` 用于为 DHCPv4 客户端
    注入先前租用的地址，用于 INIT-REBOOT。
  * 添加 mDNS 响应器接口策略
    （:kconfig:option:`CONFIG_MDNS_RESPONDER_IFACE_POLICY_ALLOWLIST`、
    :kconfig:option:`CONFIG_MDNS_RESPONDER_IFACE_POLICY_DENYLIST`），配合
    :kconfig:option:`CONFIG_MDNS_RESPONDER_IFACE_LIST` 用于控制
    mDNS 响应器在哪些网络接口上运行。
  * 添加 :c:func:`mdns_responder_enable_iface` 和
    :c:func:`mdns_responder_disable_iface`
    （:kconfig:option:`CONFIG_MDNS_RESPONDER_RUNTIME_IFACE_CONTROL`），
    用于在运行时启用或禁用网络接口上的 mDNS 响应器。
  * 添加支持 IPv6 前缀委派的 DHCPv6 服务器
    （:kconfig:option:`CONFIG_NET_DHCPV6_SERVER`）：
    :c:func:`net_dhcpv6_server_start`、:c:func:`net_dhcpv6_server_stop` 和
    :c:func:`net_dhcpv6_server_foreach_lease`。
  * 添加 IPv6 路由器角色，即路由器通告的发送
    （:kconfig:option:`CONFIG_NET_IPV6_ND_RA_TX`）：
    :c:func:`net_if_ipv6_router_start`、:c:func:`net_if_ipv6_router_stop` 和
    :c:func:`net_if_ipv6_prefix_set_advertise`。
  * 为 DHCPv6 客户端添加请求路由器支持，委派的
    前缀可通过 :c:member:`net_dhcpv6_params.downstream_ifaces`
    向下级联到下游链路。
  * 添加 :c:func:`net_eth_mcast_addr_add`、:c:func:`net_eth_mcast_addr_rm` 和
    :c:func:`net_eth_mcast_addr_foreach`。以太网 L2 现在跟踪
    接口监听的链路层组播地址，因此仅在组被其第一个用户加入
    或被最后一个用户离开时才要求以太网驱动更改其接收过滤器。
    此前 IP 层加入和包套接字成员关系被分别转发给驱动，
    离开一个组可能使设备停止监听需要相同链路层地址的另一个组。
    这很容易发生，因为 IPv4 组播地址以 32:1 映射到链路层地址。
    驱动还可以将 ``ETHERNET_CONFIG_TYPE_FILTER`` 视为
    地址已更改的提示，并通过 :c:func:`net_eth_mcast_addr_foreach`
    迭代它们来重新编程其过滤器，这适用于按地址哈希过滤的设备。
    接口可跟踪的地址数量是启用的子系统所请求数量的总和，
    :kconfig:option:`CONFIG_NET_L2_ETHERNET_MCAST_FILTER_COUNT` 可在
    应用程序需要更多时提高它。
    给定 :c:func:`net_eth_mac_filter` 或
    ``NET_REQUEST_ETHERNET_SET_MAC_FILTER`` 的组播目的
    地址以相同方式计数，因此应用程序设置的每个
    此类过滤器现在也必须由其取消设置，
    取消设置从未设置的过滤器将以 ``-ENOENT`` 失败。
  * 在 ``ZSOCK_SOL_PACKET`` 级别添加 ``ZSOCK_PACKET_ADD_MEMBERSHIP`` 和
    ``ZSOCK_PACKET_DROP_MEMBERSHIP`` 套接字选项
    （:kconfig:option:`CONFIG_NET_SOCKETS_PACKET_MCAST_MEMBERSHIP`），
    使包套接字可要求网络接口开始或停止监听
    额外的 L2 组播地址。在以太网上，如果设备支持过滤，
    该地址被编程到设备的接收过滤器；
    不过滤的设备仍会将组上送。
    接口无法满足的加入会被报告给应用程序，
    ``ENOMEM`` 表示接口无法跟踪另一个地址，
    ``ENOTSUP`` 表示它不是以太网接口。
    成员关系变更由
    :c:macro:`NET_EVENT_PACKET_MCAST_MEMBERSHIP_ADD` 和
    :c:macro:`NET_EVENT_PACKET_MCAST_MEMBERSHIP_DROP` 网络管理事件报告。
    套接字关闭时仍持有的成员关系会自动丢弃，
    :kconfig:option:`CONFIG_NET_SOCKETS_PACKET_MCAST_MEMBERSHIP_COUNT` 设置
    可同时激活多少个成员关系。
  * 添加 TCP 对接收数据的选择性确认（:rfc:`2018`、
    :kconfig:option:`CONFIG_NET_TCP_SACK`，默认启用）。Zephyr 现在
    在握手中提供 SACK 并报告接收队列中持有的乱序数据，
    使支持 SACK 的发送方可以仅重传缺失的数据。
    接收到的 SACK 块在重传时尚未使用。
  * :kconfig:option:`CONFIG_PTP_NETWORK_MODE_HYBRID`
  * 为 zperf 添加实验性 iperf3 支持
    （:kconfig:option:`CONFIG_NET_ZPERF_IPERF3`），
    取代 iPerf 2（:kconfig:option:`CONFIG_NET_ZPERF_IPERF2`）。
    两者的 zperf API 和 shell 命令相同。参见 :ref:`zperf_iperf3`。
  * 添加 SNTP 服务器（:kconfig:option:`CONFIG_SNTP_SERVER`），
    在每个启用的地址族上 UDP 端口 123 应答时间查询。
    应用程序设置系统时钟后，通过 :c:func:`sntp_server_clock_source`
    告知服务器其时钟源；在此之前，服务器会告知客户端
    其时间不应被使用。SNTP 客户端现在仅通过
    :kconfig:option:`CONFIG_SNTP` 选择，两者共享
    :kconfig:option:`CONFIG_SNTP_LIB`。
  * 添加 :c:func:`dns_resolve_is_active` 用于在不读取
    上下文内部的情况下检查 DNS 解析上下文是否处于活动状态。
  * 添加 :c:func:`coap_client_reregister_observe` 用于在不拆除
    持续 CoAP 观察的情况下刷新它（:rfc:`7641` 重新注册）。

* POSIX

  * :kconfig:option:`CONFIG_POSIX_AEP_CHOICE_NETAPP`，一个 Zephyr 特定的子配置文件，
    具有 PSE52 的功能加上 PSE53 的网络接口，但不支持多进程。

* 电源管理

  * :c:macro:`LOG_DBG_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_WRN_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_ERR_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_DBG_PM_DEVICE_RUNTIME_PUT`
  * :c:macro:`LOG_WRN_PM_DEVICE_RUNTIME_PUT`
  * :c:macro:`LOG_ERR_PM_DEVICE_RUNTIME_PUT`
  * :c:macro:`LOG_INST_DBG_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_INST_WRN_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_INST_ERR_PM_DEVICE_RUNTIME_GET`
  * :c:macro:`LOG_INST_DBG_PM_DEVICE_RUNTIME_PUT`
  * :c:macro:`LOG_INST_WRN_PM_DEVICE_RUNTIME_PUT`
  * :c:macro:`LOG_INST_ERR_PM_DEVICE_RUNTIME_PUT`

* 脉冲 IO

  * 添加 :ref:`Pulse IO <pulse_io_api>` 子系统，一个厂商中立的
    API，用于在 GPIO 线上生成和捕获定时数字边缘的硬件。

* 环形缓冲区

  * :c:struct:`sys_ringq`（参见 :ref:`fixed_size_ringq_api`）
  * :c:func:`ring_buf_put_ptr`
  * :c:func:`ring_buf_get_ptr`
  * :c:func:`ring_buf_commit`
  * :c:func:`ring_buf_consume`

* 安全存储

  * :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_CRYPT_CUSTOM`，
    允许实现你自己的 :c:func:`secure_storage_its_transform_aead_crypt`。（:github:`118542`）
  * :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_SCHEME_IS_CONFIGURABLE`
  * :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_TRANSFORM_AEAD_KEY_SIZE_IS_CONFIGURABLE`

* 定时器

  * :c:func:`z_sys_clock_lpm_enter`

* USB Type-C

  * :kconfig:option:`CONFIG_USBC_LOG_PD_MSG_NAMES`

* 工具

  * :c:macro:`ARGS_UNUSED`，用于将多个参数标记为未使用。

* Zbus

  * :kconfig:option:`CONFIG_ZBUS_RUNTIME_CHANNEL_REGISTRATION`
  * :c:func:`zbus_runtime_channel_init`
  * :c:func:`zbus_runtime_channel_register`
  * :c:func:`zbus_runtime_channel_unregister`

.. zephyr-keep-sorted-stop

新开发板
**********

..
  你可以在发布周期中贡献新开发板时更新此列表，以便让可能正在查看发布说明工作草稿的人看到。
  但请注意，此列表将在发布时重新计算，因此你*不必*更新它。
  无论如何，只需链接开发板，更多细节放在开发板描述中。

* Adafruit Industries, LLC

  * :zephyr:board:`adafruit_feather_esp32c6`（``adafruit_feather_esp32c6``）
  * :zephyr:board:`adafruit_trrs_trinkey`（``adafruit_trrs_trinkey``）

* Advanced Micro Devices (AMD), Inc.

  * :zephyr:board:`acp_7_0_adsp`（``acp_7_0_adsp``）
  * :zephyr:board:`acp_7_x_adsp`（``acp_7_x_adsp``）
  * :zephyr:board:`zynqmp_apu`（``zynqmp_apu``）
  * :zephyr:board:`zynqmp_rpu`（``zynqmp_rpu``）

* Aesc Silicon

  * :zephyr:board:`elemrv_flask_h`（``elemrv_flask_h``）

* Ai-Thinker Co., Ltd.

  * :zephyr:board:`ai_m64p_32s_kit`（``ai_m64p_32s_kit``）
  * :zephyr:board:`aipi_eyes_s2`（``aipi_eyes_s2``）

* Alif Semiconductor

  * :zephyr:board:`balletto_b1_dk`（``balletto_b1_dk``）
  * :zephyr:board:`ensemble_e8_ak`（``ensemble_e8_ak``）

* Analog Devices, Inc.

  * :zephyr:board:`max32651evkit`（``max32651evkit``）

* Antmicro

  * :zephyr:board:`stm32h7_hdmi_board`（``stm32h7_hdmi_board``）
  * :zephyr:board:`stm32h7_renode_reference_board`（``stm32h7_renode_reference_board``）

* Arduino

  * :zephyr:board:`arduino_nano_connect`（``arduino_nano_connect``）
  * :zephyr:board:`arduino_nesso_n1`（``arduino_nesso_n1``）

* ARM Ltd.

  * :zephyr:board:`fvp_corstone1000`（``fvp_corstone1000``）

* Armfly

  * :zephyr:board:`armfly_stm32h743xih6`（``armfly_stm32h743xih6``）

* Barth Elektronik GmbH

  * :zephyr:board:`stg_800`（``stg_800``）

* BeagleBoard.org Foundation

  * :zephyr:board:`beaglebadge`（``beaglebadge``）
  * :zephyr:board:`beagleconnect_zepto`（``beagleconnect_zepto``）
  * :zephyr:board:`pocketbeagle_2_industrial`（``pocketbeagle_2_industrial``）

* BLIIoT Technology Co., Ltd.

  * :zephyr:board:`am62x_m4_bl350`（``am62x_m4_bl350``）

* Bouffalo Lab (Nanjing) Co., Ltd.

  * :zephyr:board:`bl618g0`（``bl618g0``）

* CAN-module, FOP

  * :zephyr:board:`canbridge_g473`（``canbridge_g473``）
  * :zephyr:board:`usbcan_iso`（``usbcan_iso``）
  * :zephyr:board:`usbcanfd_dual`（``usbcanfd_dual``）
  * :zephyr:board:`usbcanfd_solo`（``usbcanfd_solo``）

* Chengdu Ebyte Electronic Technology

  * :zephyr:board:`e80_900mbl_01`（``e80_900mbl_01``）
  * :zephyr:board:`eora_hub_900tb`（``eora_hub_900tb``）

* Chengdu Heltec Automation Technology Co., Ltd.

  * :zephyr:board:`heltec_t114_v2`（``heltec_t114_v2``）

* Cirrus Logic, Inc.

  * :zephyr:board:`crd40l26`（``crd40l26``）

* emtrion GmbH

  * :zephyr:board:`emsbc_neon_cm7`（``emsbc_neon_cm7``）

* Espressif Systems

  * :zephyr:board:`esp32p4_function_ev_board`（``esp32p4_function_ev_board``）
  * :zephyr:board:`esp32p4x_function_ev_board`（``esp32p4x_function_ev_board``）
  * :zephyr:board:`esp32s3_box3`（``esp32s3_box3``）

* Eurovibes

  * :zephyr:board:`eurovibes_stm32g431_sertest-ng`（``eurovibes_stm32g431_sertest-ng``）

* FlySky

  * :zephyr:board:`fs_i6s`（``fs_i6s``）

* Heimann Sensor GmbH

  * :zephyr:board:`htpa_eval`（``htpa_eval``）

* Intel Corporation

  * :zephyr:board:`intel_nvl_s_rvp`（``intel_nvl_s_rvp``）

* Jhoinrch

  * :zephyr:board:`rh02`（``rh02``）
  * :zephyr:board:`rh02_plus_2026`（``rh02_plus_2026``）

* KAGA FEI Co., Ltd.

  * :zephyr:board:`ec4l15ba1`（``ec4l15ba1``）

* KinCony Electronics Co., Ltd.

  * :zephyr:board:`kincony_kc868_a8`（``kincony_kc868_a8``）

* Lilygo Shenzhen Xinyuan Electronic Technology Co., Ltd

  * :zephyr:board:`t_deck`（``t_deck``）

* M5Stack

  * :zephyr:board:`m5stack_paper_color`（``m5stack_paper_color``）
  * :zephyr:board:`m5stack_sticks3`（``m5stack_sticks3``）
  * :zephyr:board:`m5stack_unitc6l`（``m5stack_unitc6l``）

* Makerfabs

  * :zephyr:board:`matouch_mtro128g`（``matouch_mtro128g``）

* Microchip Technology Inc.

  * :zephyr:board:`m2s010_mkr_kit`（``m2s010_mkr_kit``）
  * :zephyr:board:`m2s_hello_fpga_kit`（``m2s_hello_fpga_kit``）
  * :zephyr:board:`pic32ck_gc01_cult`（``pic32ck_gc01_cult``）
  * :zephyr:board:`pic32cm_gc00_cpro`（``pic32cm_gc00_cpro``）
  * :zephyr:board:`pic32cm_sg00_cpro`（``pic32cm_sg00_cpro``）
  * :zephyr:board:`sama5d27_som1_ek1`（``sama5d27_som1_ek1``）

* MuseLab Electronics

  * :zephyr:board:`nano_ch32v317`（``nano_ch32v317``）
  * :zephyr:board:`nano_ch57x`（``nano_ch57x``）

* Nordic Semiconductor

  * :zephyr:board:`nrf93m1dk`（``nrf93m1dk``）

* Norik Systems

  * :zephyr:board:`dect_nr_plus_usb_dongle`（``dect_nr_plus_usb_dongle``）

* NUCODE Co., Ltd. (nuworks.io)

  * :zephyr:board:`nucode_nu32`（``nucode_nu32``）
  * :zephyr:board:`nucode_nu40`（``nucode_nu40``）

* Nuvoton Technology Corporation

  * :zephyr:board:`numaker_m031ki`（``numaker_m031ki``）
  * :zephyr:board:`numaker_m3351ki`（``numaker_m3351ki``）

* NXP Semiconductors

  * :zephyr:board:`frdm_imxrt1152`（``frdm_imxrt1152``）
  * :zephyr:board:`frdm_imxrt700`（``frdm_imxrt700``）
  * :zephyr:board:`imx952_evk`（``imx952_evk``）
  * :zephyr:board:`lpc845brk`（``lpc845brk``）
  * :zephyr:board:`lpcxpresso54628`（``lpcxpresso54628``）
  * :zephyr:board:`mimxrt685_aud_evk`（``mimxrt685_aud_evk``）
  * :zephyr:board:`mr_navq95b`（``mr_navq95b``）

* OLIMEX Ltd.

  * :zephyr:board:`esp32p4_pc`（``esp32p4_pc``）

* Others

  * :zephyr:board:`bl704l_dvk`（``bl704l_dvk``）
  * :zephyr:board:`esp32h2_supermini`（``esp32h2_supermini``）
  * :zephyr:board:`jz_f407vet6`（``jz_f407vet6``）
  * :zephyr:board:`stm32_debug_probe`（``stm32_debug_probe``）

* Pine64

  * :zephyr:board:`pinecone`（``pinecone``）

* QEMU

  * :zephyr:board:`qemu_cortex_a72`（``qemu_cortex_a72``）

* Radxa

  * :zephyr:board:`rock_3b`（``rock_3b``）
  * :zephyr:board:`rock_5b_plus`（``rock_5b_plus``）

* Raspberry Pi Foundation

  * :zephyr:board:`rpi_zero_2w`（``rpi_zero_2w``）

* Raytac Corporation

  * :zephyr:board:`raytac_an54lv_db_15`（``raytac_an54lv_db_15``）

* Realtek Semiconductor Corp.

  * :zephyr:board:`pke8721daf_c13_f10`（``pke8721daf_c13_f10``）

* Renesas Electronics Corporation

  * :zephyr:board:`rcar_ironhide_x5h`（``rcar_ironhide_x5h``）
  * :zephyr:board:`rza3m_ek`（``rza3m_ek``）

* Seeed Technology Co., Ltd

  * :zephyr:board:`reterminal_e1001`（``reterminal_e1001``）
  * :zephyr:board:`reterminal_e1003`（``reterminal_e1003``）
  * :zephyr:board:`wio_tracker_l1`（``wio_tracker_l1``）
  * :zephyr:board:`xiao_esp32c5`（``xiao_esp32c5``）
  * :zephyr:board:`xiao_nrf54lm20a`（``xiao_nrf54lm20a``）

* SEGGER Microcontroller GmbH

  * :zephyr:board:`nandeval_h743zi`（``nandeval_h743zi``）

* SHAKTI Processor Program

  * :zephyr:board:`nexys_ganga`（``nexys_ganga``）

* Shanghai Ruiside Electronic Technology Co., Ltd.

  * :zephyr:board:`ra8p1_titan`（``ra8p1_titan``）
  * :zephyr:board:`ra8p1_titan_mini`（``ra8p1_titan_mini``）

* Shenzhen JLC Technology Group Co., Ltd.

  * :zephyr:board:`skystar_gd32f407vet6`（``skystar_gd32f407vet6``）

* Shenzhen Luckfox Technology Co., Ltd.

  * :zephyr:board:`pico_ultra`（``pico_ultra``）

* Shenzhen Sipeed Technology Co., Ltd.

  * :zephyr:board:`m0sense`（``m0sense``）
  * :zephyr:board:`m1s_dock`（``m1s_dock``）

* Shenzhen Xunlong Software CO.,Limited

  * :zephyr:board:`opi_zero2w`（``opi_zero2w``）

* Silicon Laboratories

  * :zephyr:board:`kg100s_rb4332a`（``kg100s_rb4332a``）
  * :zephyr:board:`siwx917_ek2708a`（``siwx917_ek2708a``）
  * :zephyr:board:`xg26_dk2608a`（``xg26_dk2608a``）
  * :zephyr:board:`xg26_rb4121a`（``xg26_rb4121a``）

* STMicroelectronics

  * :zephyr:board:`nucleo_g491re`（``nucleo_g491re``）
  * :zephyr:board:`nucleo_u545re_q`（``nucleo_u545re_q``）

* Sutajio Ko-Usagi PTE Ltd.

  * :zephyr:board:`tomu`（``tomu``）

* Texas Instruments

  * :zephyr:board:`lp_am13e230`（``lp_am13e230``）
  * :zephyr:board:`lp_am243`（``lp_am243``）
  * :zephyr:board:`lp_mspm33c321a`（``lp_mspm33c321a``）

* Trenz Electronic

  * :zephyr:board:`te0950`（``te0950``）

* Tuya Inc.

  * :zephyr:board:`tyzs3`（``tyzs3``）

* u-blox

  * :zephyr:board:`ubx_evknorab2`（``ubx_evknorab2``）

* Udoo

  * :zephyr:board:`udoo_key`（``udoo_key``）

* Umeta & Ikki Automotive Parts

  * :zephyr:board:`uiapduino_pro_micro_ch32v003`（``uiapduino_pro_micro_ch32v003``）

* VIEWE Display Co., Ltd.

  * :zephyr:board:`uedx24240013_md50e`（``uedx24240013_md50e``）
  * :zephyr:board:`uedx32480035e_wb_a`（``uedx32480035e_wb_a``）

* Waveshare Electronics

  * :zephyr:board:`esp32c6_lcd_1_47`（``esp32c6_lcd_1_47``）
  * :zephyr:board:`esp32p4_wifi6`（``esp32p4_wifi6``）
  * :zephyr:board:`esp32p4_wifi6_dev_kit`（``esp32p4_wifi6_dev_kit``）
  * :zephyr:board:`waveshare_esp32p4_eth`（``waveshare_esp32p4_eth``）

* WeAct Studio

  * :zephyr:board:`ch32v00x_core`（``ch32v00x_core``）
  * :zephyr:board:`usb2canfdv2`（``usb2canfdv2``）
  * :zephyr:board:`weact_ra4m1_core`（``weact_ra4m1_core``）

* WinChipHead

  * :zephyr:board:`ch32h417evt`（``ch32h417evt``）
  * :zephyr:board:`ch32v103evt`（``ch32v103evt``）
  * :zephyr:board:`ch32v203c8t6evt`（``ch32v203c8t6evt``）
  * :zephyr:board:`ch32v305f_evt_r0`（``ch32v305f_evt_r0``）

* WIZnet Co., Ltd.

  * :zephyr:board:`w55rp20_evb_pico`（``w55rp20_evb_pico``）
  * :zephyr:board:`w6100_evb_pico`（``w6100_evb_pico``）
  * :zephyr:board:`w6100_evb_pico2`（``w6100_evb_pico2``）
  * :zephyr:board:`w6300_evb_pico2`（``w6300_evb_pico2``）

新盾牌
***********

..
  与开发板相同，此列表也将在发布时重新计算。

* :ref:`AD-APARDPFW-SL <ad_apardpfw_sl>`
* :ref:`Adafruit FeatherWing MAX3421E 盾牌 <adafruit_featherwing_max3421e>`
* :ref:`Analog Devices 低速混合信号实验平台 <adi_lsmspg>`
* :ref:`ArduCam Mega SPI 摄像头盾牌 <arducam_mega>`
* :ref:`DFRobot Gravity TM6605 触觉电机驱动模块 <dfrobot_gravity_tm6605>`
* :ref:`EVAL-AD5529R-ARDZ <eval_ad5529r_ardz>`
* :ref:`M5Stack Unit 手势 <m5stack_unit_gesture_shield>`
* :ref:`M5Stack Unit Mini OLED <m5stack_unit_minioled_shield>`
* :ref:`MB1280 STMod+ 扇出盾牌 <mb1280_stmod_plus>`
* :ref:`MikroElektronika EERAM 3.3V Click <mikroe_eeram_33v_click_shield>`
* :ref:`MikroElektronika 双线 ETH Click <mikroe_two_wire_eth_click_shield>`
* :ref:`NXP MX8 DSI OLED1A 面板 <nxp_mx8_dsi_oled1a>`
* :ref:`NXP MX9 DSI OLED 面板 <nxp_mx9_dsi_oled>`
* :ref:`OD-6010 SLCD 面板盾牌 <od_6010_shield>`
* :ref:`RAK19007 WisBlock 基座板第二代 <rakwireless_rak19007>`
* :ref:`Seeed Studio XIAO 用 COB LED 驱动板 <seeed_xiao_cob_led>`
* :ref:`ST B-M2MEM-PACK1 M.2 串行内存包 <st_b_m2mem_pack1_shield>`
* :ref:`X-NUCLEO-67W61M1：Wi-Fi 6 扩展板 <x_nucleo_67w61m1>`
* :ref:`X-NUCLEO-GNSS1A1：基于 Teseo-LIV3F 的 GNSS 扩展板 <x-nucleo-gnss1a1>`
* :ref:`X-NUCLEO-PGEEZ1 页面 EEPROM 扩展板 <x_nucleo_pgeez1_shield>`
* :ref:`X-NUCLEO-WBA25A1：BLE 扩展板 <x-nucleo-wba25a1>`

新驱动
***********

..
  与开发板相同，此列表也将在发布时重新计算。
  只需链接驱动，更多细节放在绑定描述中

* :abbr:`ADC（模数转换器）`

  * :dtcompatible:`adi,ad4190-8-adc`（:github:`111922`）
  * :dtcompatible:`adi,ad4195-8-adc`（:github:`111922`）
  * :dtcompatible:`infineon,autanalog-sar-fifo`（:github:`110289`）
  * :dtcompatible:`infineon,autanalog-sar-fir`（:github:`110289`）
  * :dtcompatible:`m5stack,m5pm1-adc`（:github:`109961`）
  * :dtcompatible:`realtek,ameba-adc`（:github:`106677`）
  * :dtcompatible:`realtek,bee-adc`（:github:`105264`）
  * :dtcompatible:`ti,adc081c021`（:github:`114289`）
  * :dtcompatible:`ti,adc081c027`（:github:`114289`）
  * :dtcompatible:`ti,adc101c021`（:github:`114289`）
  * :dtcompatible:`ti,adc101c027`（:github:`114289`）
  * :dtcompatible:`ti,adc121c021`（:github:`114289`）
  * :dtcompatible:`ti,adc121c027`（:github:`114289`）
  * :dtcompatible:`ti,ads1118`（:github:`94152`）
  * :dtcompatible:`ti,ads1220`（:github:`102479`）
  * :dtcompatible:`ti,ads7828`（:github:`114359`）
  * :dtcompatible:`ti,ads7830`（:github:`114359`）
  * :dtcompatible:`ti,mspm0-adc12`（:github:`94736`）
  * :dtcompatible:`ti,tla2528-adc`（:github:`110722`）

* ARM 架构

  * :dtcompatible:`infineon,edge-npu`（:github:`106826`）
  * :dtcompatible:`nordic,nrf-wicr`（:github:`108141`）
  * :dtcompatible:`nordic,nrf71-uicr`（:github:`106134`）

* 音频

  * :dtcompatible:`st,stm32-dfsdm`（:github:`108302`）
  * :dtcompatible:`st,stm32-dfsdm-dmic`（:github:`108302`）
  * :dtcompatible:`ti,tas2563`（:github:`103148`）
  * :dtcompatible:`ti,tlv320aic26`（:github:`106836`）
  * :dtcompatible:`wolfson,wm8960`（:github:`106212`）
  * :dtcompatible:`zephyr,dummy-codec`（:github:`109891`）
  * :dtcompatible:`zephyr,native-sim-dmic`（:github:`109898`）

* 辅助显示

  * :dtcompatible:`nxp,slcd`（:github:`102796`）
  * :dtcompatible:`slcd-panel`（:github:`102796`）

* 蓝牙

  * :dtcompatible:`espressif,esp-hosted-mcu-bt-hci`（:github:`114532`）
  * :dtcompatible:`realtek,ameba-bt-hci`（:github:`109287`）

* 蜂鸣器

  * :dtcompatible:`gpio-buzzer`（:github:`108911`）
  * :dtcompatible:`pwm-buzzer`（:github:`108911`）

* :abbr:`CAN（控制器局域网）`

  * :dtcompatible:`bflb,bl61x-can`（:github:`110672`）
  * :dtcompatible:`espressif,esp32-twaifd`（:github:`107680`）
  * :dtcompatible:`realtek,bee-can`（:github:`105411`）

* 充电器

  * :dtcompatible:`adi,adp5360-charger`（:github:`105258`）
  * :dtcompatible:`silergy,sy6974b`（:github:`107439`）
  * :dtcompatible:`ti,bq24295`（:github:`114650`）
  * :dtcompatible:`ti,bq24296`（:github:`114650`）
  * :dtcompatible:`ti,bq24296m`（:github:`114650`）
  * :dtcompatible:`ti,bq24297`（:github:`114650`）
  * :dtcompatible:`ti,bq24298`（:github:`114650`）

* 时钟控制

  * :dtcompatible:`aesc,clock-controller`（:github:`116703`）
  * :dtcompatible:`bflb,bl616cl-clock-controller`（:github:`112738`）
  * :dtcompatible:`bflb,bl808-clock-controller`（:github:`105580`）
  * :dtcompatible:`bflb,mm-clk`（:github:`105580`）
  * :dtcompatible:`microchip,pic32cm-sg-gc-clock`（:github:`112582`）
  * :dtcompatible:`microchip,pic32cm-sg-gc-dfll48m`（:github:`112582`）
  * :dtcompatible:`microchip,pic32cm-sg-gc-dpll`（:github:`112582`）
  * :dtcompatible:`microchip,pic32cm-sg-gc-gclkgen`（:github:`112582`）
  * :dtcompatible:`microchip,pic32cm-sg-gc-gclkperiph`（:github:`112582`）
  * :dtcompatible:`microchip,pic32cm-sg-gc-mclkdomain`（:github:`112582`）
  * :dtcompatible:`microchip,pic32cm-sg-gc-mclkperiph`（:github:`112582`）
  * :dtcompatible:`microchip,pic32cm-sg-gc-rtc`（:github:`112582`）
  * :dtcompatible:`microchip,pic32cm-sg-gc-xosc`（:github:`112582`）
  * :dtcompatible:`microchip,pic32cm-sg-gc-xosc32k`（:github:`112582`）
  * :dtcompatible:`microchip,smartfusion2-clock`（:github:`106926`）
  * :dtcompatible:`nordic,nrf-clock-hfclk`（:github:`104658`）
  * :dtcompatible:`nordic,nrf-clock-hfclk192m`（:github:`104658`）
  * :dtcompatible:`nordic,nrf-clock-hfclkaudio`（:github:`104658`）
  * :dtcompatible:`nordic,nrf-clock-lfclk`（:github:`104658`）
  * :dtcompatible:`nordic,nrf-clock-xo`（:github:`104658`）
  * :dtcompatible:`nordic,nrf-clock-xo24m`（:github:`104658`）
  * :dtcompatible:`nuvoton,m4-hclk-clock`（:github:`103668`）
  * :dtcompatible:`nuvoton,m4-hxt-clock`（:github:`103668`）
  * :dtcompatible:`nuvoton,m4-lxt-clock`（:github:`103668`）
  * :dtcompatible:`nuvoton,m4-pll-clock`（:github:`103668`）
  * :dtcompatible:`nuvoton,numicro-m4-pcc`（:github:`103668`）
  * :dtcompatible:`nuvoton,numicro-m4-scc`（:github:`103668`）
  * :dtcompatible:`nxp,imxrt118x-arm-pll`（:github:`106881`）
  * :dtcompatible:`nxp,imxrt11xx-arm-pll`（:github:`106881`）
  * :dtcompatible:`nxp,lpc84x-clock`（:github:`105928`）
  * :dtcompatible:`nxp,mcxw7x-clock`（:github:`101937`）
  * :dtcompatible:`silabs,series0-cmu`（:github:`111754`）
  * :dtcompatible:`silabs,series0-hfxo`（:github:`111754`）
  * :dtcompatible:`silabs,series0-lfrco`（:github:`111754`）
  * :dtcompatible:`silabs,series0-lfxo`（:github:`111754`）
  * :dtcompatible:`st,stm32h5-pll-clock`（:github:`110914`）
  * :dtcompatible:`st,stm32n6-msi-clock`（:github:`108997`）
  * :dtcompatible:`wch,ch32h41x-pll-clock`（:github:`111725`）

* 时钟监视器

  * :dtcompatible:`nxp,cmu-fc`（:github:`107879`）
  * :dtcompatible:`nxp,cmu-fm`（:github:`107879`）
  * :dtcompatible:`nxp,freqme`（:github:`112403`）

* 比较器

  * :dtcompatible:`espressif,esp32-ana-cmpr`（:github:`113625`）
  * :dtcompatible:`infineon,autanalog-ptcomp-comp`（:github:`107488`）
  * :dtcompatible:`infineon,hppass-csg-comp`（:github:`109879`）
  * :dtcompatible:`infineon,lp-comp`（:github:`104636`）
  * :dtcompatible:`infineon,lp-comp-channel`（:github:`104636`）
  * :dtcompatible:`ti,mspm0-comparator`（:github:`94737`）

* 计数器

  * :dtcompatible:`arm,crsas-ma2-counter`（:github:`112815`）
  * :dtcompatible:`arm,crsas-ma2-timer`（:github:`112815`）
  * :dtcompatible:`nxp,irtc-wake-timer`（:github:`111552`）
  * :dtcompatible:`nxp,sysctr`（:github:`106300`）
  * :dtcompatible:`nxp,tstmr`（:github:`112255`）
  * :dtcompatible:`nxp,wake-timer`（:github:`110811`）
  * :dtcompatible:`realtek,ameba-counter`（:github:`106664`）
  * :dtcompatible:`realtek,bee-counter-rtc`（:github:`105193`）
  * :dtcompatible:`ti,k3-rtc-counter`（:github:`104048`）
  * :dtcompatible:`wch,adtm`（:github:`109728`）
  * :dtcompatible:`xlnx,ttc`（:github:`103117`）
  * :dtcompatible:`xlnx,ttc-counter`（:github:`103117`）
  * :dtcompatible:`xlnx,zynqmp-rtc`（:github:`107684`）

* :abbr:`CPU（中央处理器）`

  * :dtcompatible:`adi,max32-m4f-cpu1`（:github:`105310`）
  * :dtcompatible:`arm,armv8`（:github:`114145`）
  * :dtcompatible:`arm,cortex-a32`（:github:`107644`）
  * :dtcompatible:`arm,cortex-a57`（:github:`114109`）
  * :dtcompatible:`arm,cortex-a720`（:github:`113087`）
  * :dtcompatible:`arm,cortex-r8f`（:github:`114145`）
  * :dtcompatible:`intel,nova-lake`（:github:`111818`）
  * :dtcompatible:`intel,x86_64`（:github:`115174`）
  * :dtcompatible:`spinalhdl,vexiiriscv`（:github:`109932`）
  * :dtcompatible:`wch,qingke-v3c`（:github:`111171`）
  * :dtcompatible:`wch,qingke-v3f`（:github:`111725`）
  * :dtcompatible:`wch,qingke-v5f`（:github:`111725`）

* :abbr:`CPU（中央处理器）` 频率调节

  * :dtcompatible:`zephyr,cpu-freq-thermal-cap`（:github:`108242`）

* :abbr:`CRC（循环冗余校验）`

  * :dtcompatible:`ambiq,hw-crc32`（:github:`110366`）

* 加密加速器

  * :dtcompatible:`infineon,mxcrypto-crypto`（:github:`108439`）
  * :dtcompatible:`infineon,mxcrypto-trng`（:github:`108439`）
  * :dtcompatible:`infineon,mxcryptolite-crypto`（:github:`109693`）
  * :dtcompatible:`infineon,mxcryptolite-trng`（:github:`109693`）
  * :dtcompatible:`realtek,bee-aes`（:github:`114817`）
  * :dtcompatible:`realtek,bee-sha256`（:github:`114817`）
  * :dtcompatible:`ti,mspm0-aes`（:github:`94734`）

* :abbr:`DAC（数模转换器）`

  * :dtcompatible:`adi,ad5529r`（:github:`106256`）
  * :dtcompatible:`infineon,autanalog-ctdac`（:github:`107490`）
  * :dtcompatible:`infineon,hppass-csg-dac`（:github:`109967`）
  * :dtcompatible:`microchip,dac-g2`（:github:`109820`）
  * :dtcompatible:`ti,dac43508`（:github:`112038`）
  * :dtcompatible:`ti,dac53508`（:github:`112038`）
  * :dtcompatible:`ti,dac63508`（:github:`112038`）
  * :dtcompatible:`ti,mspm0-dac`（:github:`94725`）

* :abbr:`DAI（数字音频接口）`

  * :dtcompatible:`amd,acp-sdw-dai`（:github:`104450`）
  * :dtcompatible:`amd,tdm-dai`（:github:`108314`）

* :abbr:`DALI（数字可寻址照明接口）`

  * :dtcompatible:`zephyr,dali-pwm`（:github:`88128`）

* 磁盘

  * :dtcompatible:`virtio,blk`（:github:`112581`）
  * :dtcompatible:`zephyr,memc-ram-disk`（:github:`111528`）

* 显示

  * :dtcompatible:`charlieplex-led-matrix`（:github:`110137`）
  * :dtcompatible:`chipwealth,ch1115`（:github:`107434`）
  * :dtcompatible:`chipwealth,ch1116`（:github:`107434`）
  * :dtcompatible:`eink,ed2208-doa`（:github:`109961`）
  * :dtcompatible:`eink,ed2208-gca`（:github:`107510`）
  * :dtcompatible:`fitipower,ek79007`（:github:`116543`）
  * :dtcompatible:`himax,hx8353e`（:github:`108055`）
  * :dtcompatible:`ite,it8951`（:github:`108591`）
  * :dtcompatible:`levetop,lt7680`（:github:`112389`）
  * :dtcompatible:`raspberrypi,bcm2711-framebuffer`（:github:`109522`）
  * :dtcompatible:`raydium,rm67199`（:github:`98554`）
  * :dtcompatible:`raydium,rm692c9`（:github:`93134`）
  * :dtcompatible:`sinowealth,sh1107`（:github:`107434`）
  * :dtcompatible:`socionext,dpu`（:github:`93134`）
  * :dtcompatible:`solomon,ssd1305`（:github:`107434`）
  * :dtcompatible:`solomon,ssd1306b`（:github:`107434`）
  * :dtcompatible:`solomon,ssd1315`（:github:`107434`）
  * :dtcompatible:`solomon,ssd1683`（:github:`112893`）
  * :dtcompatible:`st,neochrom-gpu2d`（:github:`105970`）
  * :dtcompatible:`st,stm32-dma2d`（:github:`103687`）
  * :dtcompatible:`ultrachip,uc8253`（:github:`113230`）
  * :dtcompatible:`zephyr,panel-color-palette`（:github:`107945`）

* :abbr:`DMA（直接内存访问）`

  * :dtcompatible:`amd,acp-host-dma`（:github:`104450`）
  * :dtcompatible:`amd,acp-sdw-dma`（:github:`104450`）
  * :dtcompatible:`amd,acp-tdm-dma`（:github:`108314`）
  * :dtcompatible:`amd,versal2-dma-1.0`（:github:`101685`）
  * :dtcompatible:`infineon,mdma`（:github:`110847`）
  * :dtcompatible:`microchip,dmac-g3-dma`（:github:`109209`）
  * :dtcompatible:`nxp,gdma`（:github:`104868`）
  * :dtcompatible:`realtek,ameba-gdma`（:github:`105366`）
  * :dtcompatible:`realtek,bee-dma`（:github:`104754`）
  * :dtcompatible:`renesas,rza2m-dma`（:github:`107009`）
  * :dtcompatible:`ti,mspm0-dma`（:github:`91502`）
  * :dtcompatible:`xlnx,zynqmp-dma-1.0`（:github:`101685`）

* :abbr:`DSP（数字信号处理器）`

  * :dtcompatible:`nxp,powerquad`（:github:`110745`）

* :abbr:`EDAC（错误检测与纠正）`

  * :dtcompatible:`nxp,mecc`（:github:`105341`）

* :abbr:`ESPI（增强串行外设接口）`

  * :dtcompatible:`intel,espi-peci`（:github:`103773`）

* 以太网

  * :dtcompatible:`brcm,genet`（:github:`113360`）
  * :dtcompatible:`brcm,genet-mdio`（:github:`113360`）
  * :dtcompatible:`microchip,gmac-g1-eth`（:github:`105275`）
  * :dtcompatible:`microchip,gmac-g1-mdio`（:github:`105275`）
  * :dtcompatible:`microchip,lan8840`（:github:`110896`）
  * :dtcompatible:`nxp,imx-netc-vsi`（:github:`114331`）
  * :dtcompatible:`snps,dwmac`（:github:`114760`）
  * :dtcompatible:`snps,dwmac-mdio`（:github:`108046`）
  * :dtcompatible:`snps,dwmac-ptp-clock`（:github:`114242`）
  * :dtcompatible:`wch,ch9120`（:github:`111708`）
  * :dtcompatible:`wiznet,w5100s`（:github:`113315`）
  * :dtcompatible:`wiznet,w6300`（:github:`102727`）
  * :dtcompatible:`xlnx,gem-mdio`（:github:`87313`）
  * :dtcompatible:`zephyr,native-ptp-clock`（:github:`109265`）

* 固件

  * :dtcompatible:`arm,scmi-reset`（:github:`106306`）
  * :dtcompatible:`raspberrypi,bcm283x-firmware`（:github:`107536`）

* 闪存控制器

  * :dtcompatible:`aesc,spi-flash-controller`（:github:`110957`）
  * :dtcompatible:`infineon,rram-controller`（:github:`108532`）
  * :dtcompatible:`intel,pflash-cfi01`（:github:`112714`）
  * :dtcompatible:`microchip,igloo2-envm-controller`（:github:`111817`）
  * :dtcompatible:`microchip,nvmctrl-g2`（:github:`108440`）
  * :dtcompatible:`microchip,nvmctrl-g3`（:github:`109747`）
  * :dtcompatible:`microchip,smartfusion2-flash-controller`（:github:`106926`）
  * :dtcompatible:`nxp,iap-fmc84x`（:github:`105928`）
  * :dtcompatible:`realtek,ameba-flash-controller`（:github:`106690`）
  * :dtcompatible:`realtek,bee-nor-flash-controller`（:github:`107007`）

* :abbr:`FPGA（现场可编程门阵列）`

  * :dtcompatible:`renesas,slg47910`（:github:`107551`）

* 燃料表

  * :dtcompatible:`adi,adp5360-fuel-gauge`（:github:`105258`）

* :abbr:`GNSS（全球导航卫星系统）`

  * :dtcompatible:`ericsson,f5521gw`（:github:`113055`）
  * :dtcompatible:`u-blox,m10`（:github:`110846`）

* :abbr:`GPIO（通用输入/输出）` 和接头

  * :dtcompatible:`allwinner,sun50i-h618-gpio`（:github:`110502`）
  * :dtcompatible:`allwinner,sunxi-gpio`（:github:`110502`）
  * :dtcompatible:`arduino-mega-header`（:github:`105160`）
  * :dtcompatible:`diodes,pi4ioe5v6408`（:github:`108505`）
  * :dtcompatible:`esp-01-header`（:github:`109705`）
  * :dtcompatible:`gpio-mmio-latch`（:github:`105732`）
  * :dtcompatible:`m5stack,m5pm1-gpio`（:github:`109961`）
  * :dtcompatible:`nordic,npm10xx-gpio`（:github:`108508`）
  * :dtcompatible:`raspberrypi,bcm283x-gpio`（:github:`110788`）
  * :dtcompatible:`realtek,rts5817-gpio`（:github:`105542`）
  * :dtcompatible:`st,m2-memory-connector`（:github:`109004`）
  * :dtcompatible:`st,stmod-plus-connector`（:github:`109705`）
  * :dtcompatible:`st-zio-header`（:github:`115412`）
  * :dtcompatible:`ti,tca9554`（:github:`111041`）
  * :dtcompatible:`ti,tla2528-gpio`（:github:`110722`）
  * :dtcompatible:`virtio,gpio`（:github:`114983`）
  * :dtcompatible:`wch,ch5xx-gpio`（:github:`111171`）

* 触觉

  * :dtcompatible:`cirrus,cs40l26`（:github:`106934`）
  * :dtcompatible:`cirrus,cs40l27`（:github:`106934`）
  * :dtcompatible:`cirrus,cs40l50`（:github:`105683`）
  * :dtcompatible:`cirrus,cs40l51`（:github:`105683`）
  * :dtcompatible:`cirrus,cs40l52`（:github:`105683`）
  * :dtcompatible:`cirrus,cs40l53`（:github:`105683`）
  * :dtcompatible:`titanmec,tm6605`（:github:`109104`）

* 硬件信息

  * :dtcompatible:`nxp,lpc-pmc-hwinfo`（:github:`114693`）
  * :dtcompatible:`nxp,mc-rgm`（:github:`111359`）
  * :dtcompatible:`nxp,otp-uid`（:github:`111493`）
  * :dtcompatible:`zephyr,hwinfo-nvmem`（:github:`118693`）

* :abbr:`I2C（集成电路总线）`

  * :dtcompatible:`ambiq,ios-i2c`（:github:`96059`）
  * :dtcompatible:`brcm,bcm2711-i2c`（:github:`105601`）
  * :dtcompatible:`ene,kb106x-i2c`（:github:`106693`）
  * :dtcompatible:`realtek,ameba-i2c`（:github:`108235`）
  * :dtcompatible:`realtek,bee-i2c`（:github:`105028`）
  * :dtcompatible:`zephyr,i2c-target-tmp103`（:github:`114727`）

* :abbr:`I2S（集成电路间音频）`

  * :dtcompatible:`zephyr,native-sim-i2s`（:github:`109902`）

* :abbr:`I3C（改进型集成电路总线）`

  * :dtcompatible:`microchip,xec-i3c`（:github:`116252`）

* IEEE 802.15.4

  * :dtcompatible:`silabs,efr32-ieee802154`（:github:`108596`）

* 输入

  * :dtcompatible:`tbs,crsf`（:github:`106941`）
  * :dtcompatible:`virtio,input`（:github:`111029`）

* 中断控制器

  * :dtcompatible:`amd,acp-intc`（:github:`104450`）
  * :dtcompatible:`brcm,bcm2835-armctrl-ic`（:github:`110189`）
  * :dtcompatible:`brcm,bcm2836-l1-intc`（:github:`110189`）
  * :dtcompatible:`microchip,smartfusion2-h2f-irqctrl`（:github:`106926`）

* :abbr:`IPC（处理器间通信）`

  * :dtcompatible:`nxp,ipc-rpmsg-lite`（:github:`104807`）

* :abbr:`LED（发光二极管）`

  * :dtcompatible:`issi,is31fl3193`（:github:`107555`）
  * :dtcompatible:`nordic,npm10xx-led`（:github:`108756`）
  * :dtcompatible:`nxp,pca9530`（:github:`112203`）
  * :dtcompatible:`nxp,pca9531`（:github:`112203`）
  * :dtcompatible:`nxp,pca9532`（:github:`112203`）
  * :dtcompatible:`ti,lp5860`（:github:`108801`）
  * :dtcompatible:`ti,lp5861`（:github:`108801`）
  * :dtcompatible:`ti,lp5862`（:github:`108801`）
  * :dtcompatible:`ti,lp5864`（:github:`108801`）
  * :dtcompatible:`ti,lp5866`（:github:`108801`）
  * :dtcompatible:`ti,lp5868`（:github:`108801`）
  * :dtcompatible:`zephyr,fake-leds`（:github:`110819`）
  * :dtcompatible:`zephyr,native-linux-leds`（:github:`111189`）

* :abbr:`LED（发光二极管）` 灯带

  * :dtcompatible:`worldsemi,ws2812-bflb-wo`（:github:`105325`）
  * :dtcompatible:`worldsemi,ws2812-pulse-io`（:github:`110466`）

* LIN

  * :dtcompatible:`renesas,ra-lin-sci-b`

* LoRa

  * :dtcompatible:`semtech,lr1121`（:github:`109912`）

* 邮箱

  * :dtcompatible:`arm,mhuv2`（:github:`110686`）
  * :dtcompatible:`brcm,bcm2711-mbox`（:github:`107536`）
  * :dtcompatible:`renesas,rcar-mfis-mbox`（:github:`108868`）

* MCUmgr

  * :dtcompatible:`zephyr,smp-spi`（:github:`106947`）

* 内存控制器

  * :dtcompatible:`bflb,bl808-psram-uhs`（:github:`110702`）
  * :dtcompatible:`bflb,bl808-psram-uhs-controller`（:github:`110702`）
  * :dtcompatible:`bflb,sf-bank`（:github:`107223`）
  * :dtcompatible:`bflb,sf-controller`（:github:`107223`）
  * :dtcompatible:`nxp,imx-snvs-gpr`（:github:`109842`）

* 杂项

  * :dtcompatible:`adi,tmc6460`（:github:`113438`）
  * :dtcompatible:`nxp,imx93-video-pll`（:github:`98554`）
  * :dtcompatible:`nxp,mcxw-hw-params`（:github:`108974`）
  * :dtcompatible:`ti,tdp2004`（:github:`111950`）

* 调制解调器

  * :dtcompatible:`fibocom,le250`（:github:`114755`）
  * :dtcompatible:`nordic,nrf91-sm-v2`（:github:`115058`）
  * :dtcompatible:`nordic,nrf93m1`（:github:`106289`）
  * :dtcompatible:`quectel,bc66`（:github:`111279`）
  * :dtcompatible:`quectel,bc660k`（:github:`111279`）
  * :dtcompatible:`quectel,bc66x`（:github:`111279`）
  * :dtcompatible:`quectel,eg21-g`（:github:`115561`）
  * :dtcompatible:`quectel,eg915u`（:github:`95921`）
  * :dtcompatible:`telit,le910c1tx`（:github:`106716`）
  * :dtcompatible:`telit,lex10q1`（:github:`109206`）
  * :dtcompatible:`trasna,lexi-r10`（:github:`107308`）

* :abbr:`MTD（内存技术设备）`

  * :dtcompatible:`bflb,sf-device`（:github:`107223`）
  * :dtcompatible:`bflb,sf-flash`（:github:`107223`）
  * :dtcompatible:`is66wv`（:github:`111074`）
  * :dtcompatible:`microchip,flash-g2`（:github:`108440`）
  * :dtcompatible:`microchip,flash-g3`（:github:`109747`）
  * :dtcompatible:`nordic,tz-nonsecure`（:github:`108883`）
  * :dtcompatible:`nordic,tz-secure`（:github:`108883`）
  * :dtcompatible:`nxp,imx-flexspi-nand`（:github:`104870`）
  * :dtcompatible:`nxp,mcxw-ifr`（:github:`108974`）
  * :dtcompatible:`realtek,bee-nor-flash`（:github:`107007`）

* 多线 :abbr:`SPI（串行外设接口）`

  * :dtcompatible:`microchip,xec-qmspi-controller`（:github:`113243`）
  * :dtcompatible:`microchip,xec-qmspi-device`（:github:`113243`）
  * :dtcompatible:`st,nor`（:github:`113368`）
  * :dtcompatible:`st,psram-device`（:github:`105219`）
  * :dtcompatible:`zephyr,peripheral-device`（:github:`103754`）

* 多功能设备

  * :dtcompatible:`ambiq,ios`（:github:`96059`）
  * :dtcompatible:`infineon,autanalog`（:github:`106227`）
  * :dtcompatible:`infineon,autanalog-ac-state`（:github:`106227`）
  * :dtcompatible:`infineon,autanalog-ctb`（:github:`107489`）
  * :dtcompatible:`infineon,autanalog-prb`（:github:`107487`）
  * :dtcompatible:`infineon,autanalog-ptcomp`（:github:`107488`）
  * :dtcompatible:`infineon,hppass-ac-state`（:github:`109196`）
  * :dtcompatible:`infineon,hppass-analog`（:github:`109196`）
  * :dtcompatible:`infineon,hppass-csg`（:github:`109694`）
  * :dtcompatible:`infineon,mxcrypto`（:github:`108439`）
  * :dtcompatible:`infineon,mxcryptolite`（:github:`109693`）
  * :dtcompatible:`m5stack,m5pm1`（:github:`109961`）
  * :dtcompatible:`ti,tla2528`（:github:`110722`）

* :abbr:`MUX（多路复用器）`

  * :dtcompatible:`adi,adgm3121`（:github:`112088`）
  * :dtcompatible:`adi,adgm3121-gpio`（:github:`112088`）
  * :dtcompatible:`gpio-mux`（:github:`112088`）
  * :dtcompatible:`nxp,inputmux`（:github:`109379`）
  * :dtcompatible:`nxp,trgmux`（:github:`112088`）

* 网络

  * gPTP

    * :kconfig:option:`CONFIG_NET_GPTP_STATIC_TIME_RECEIVER` 将节点作为
      静态配置的时间接收器运行，使其能够通过不发送
      Announce 消息的 IEEE 802.1AS 汽车配置文件桥进行同步。

  * :dtcompatible:`st,stm32wba-radio`（:github:`110546`）

* :abbr:`OPAMP（运算放大器）`

  * :dtcompatible:`infineon,autanalog-ctb-opamp`（:github:`107489`）

* :abbr:`OTP（一次性可编程）` 内存

  * :dtcompatible:`adi,axi-sysid`（:github:`115280`）
  * :dtcompatible:`nxp,otpc`（:github:`111707`）
  * :dtcompatible:`nxp,rt7xx-ocotp`（:github:`108075`）
  * :dtcompatible:`realtek,rts5817-ocotp`（:github:`111141`）

* :abbr:`PCIe（外设组件互连 Express）`

  * :dtcompatible:`brcm,iproc-pcie-ep-v2`（:github:`111490`）

* PHY

  * :dtcompatible:`lin-transceiver-gpio`
  * :dtcompatible:`st,stm32f7-usbphyc`（:github:`114696`）
  * :dtcompatible:`st,stm32n6-usbphyc`（:github:`114696`）

* 引脚控制

  * :dtcompatible:`aesc,pinctrl`（:github:`108137`）
  * :dtcompatible:`arm,v2m_musca_b1-pinctrl`（:github:`114671`）
  * :dtcompatible:`elan,em32-pinctrl`（:github:`103037`）
  * :dtcompatible:`nxp,lpc84x-iocon`（:github:`105928`）
  * :dtcompatible:`nxp,lpc84x-swm`（:github:`105928`）
  * :dtcompatible:`renesas,rcar-pfc-x5h`（:github:`108871`）
  * :dtcompatible:`wch,ch570-pinctrl`（:github:`111171`）
  * :dtcompatible:`wch,h41x-afio`（:github:`111725`）

* 电源域

  * :dtcompatible:`raspberrypi,bcm283x-power`（:github:`112918`）

* 电源管理

  * :dtcompatible:`microchip,supc-g1`（:github:`115872`）
  * :dtcompatible:`nxp,smc`（:github:`102228`）
  * :dtcompatible:`sifli,sf32lb52x-pmuc`（:github:`108093`）
  * :dtcompatible:`st,stm32-pwr-wkupctrl`（:github:`114092`）
  * :dtcompatible:`st,stm32f1-pwr-wkupctrl`（:github:`114092`）
  * :dtcompatible:`st,stm32f7-pwr-wkupctrl`（:github:`114092`）

* 脉冲 IO

  * :dtcompatible:`espressif,esp32-rmt`（:github:`110466`）
  * :dtcompatible:`zephyr,pulse-io-loopback`（:github:`110466`）

* :abbr:`PWM（脉冲宽度调制）`

  * :dtcompatible:`realtek,ameba-pwm`（:github:`106669`）
  * :dtcompatible:`realtek,bee-pwm`（:github:`105014`）
  * :dtcompatible:`ti,am3352-ecap`（:github:`88860`）
  * :dtcompatible:`ti,am3352-ehrpwm`（:github:`88757`）
  * :dtcompatible:`wch,adtm-pwm`（:github:`109728`）
  * :dtcompatible:`zephyr,pwm-bitbang`（:github:`106536`）

* 稳压器

  * :dtcompatible:`gd,gd32-bldo`（:github:`106501`）
  * :dtcompatible:`infineon,autanalog-prb-vref`（:github:`107487`）
  * :dtcompatible:`m5stack,m5pm1-regulator`（:github:`109961`）
  * :dtcompatible:`realtek,rts5817-regulator`（:github:`108545`）
  * :dtcompatible:`sifli,sf32lb52x-ldo`（:github:`108093`）
  * :dtcompatible:`ti,mspm0-vref`（:github:`94732`）

* 复位控制器

  * :dtcompatible:`wch,ch32-rcc-rctl`（:github:`115714`）

* 保留内存

  * :dtcompatible:`gd,gd32-backup-sram`（:github:`106501`）

* :abbr:`RNG（随机数生成器）`

  * :dtcompatible:`brcm,bcm2835-rng`（:github:`110191`）
  * :dtcompatible:`microchip,trng-g2-entropy`（:github:`108155`）
  * :dtcompatible:`realtek,ameba-trng`（:github:`106670`）
  * :dtcompatible:`realtek,bee-trng`（:github:`105335`）

* :abbr:`RTC（实时时钟）`

  * :dtcompatible:`ite,it8xxx2-rtc`（:github:`106350`）
  * :dtcompatible:`microchip,rtc-mss`（:github:`110842`）
  * :dtcompatible:`microchip,xec-hibtimer`（:github:`111476`）
  * :dtcompatible:`microchip,xec-rtc`（:github:`106116`）
  * :dtcompatible:`microcrystal,rv3028-rtc`（:github:`112978`）
  * :dtcompatible:`nxp,rtc-analog`（:github:`107196`）
  * :dtcompatible:`realtek,ameba-rtc`（:github:`105376`）

* :abbr:`SDHC（安全数字大容量）`

  * :dtcompatible:`bflb,sdhc`（:github:`105243`）
  * :dtcompatible:`microchip,sdhc-g1`（:github:`109211`）
  * :dtcompatible:`nuvoton,numaker-sdhc`（:github:`105437`）
  * :dtcompatible:`realtek,ameba-sdhost`（:github:`106687`）
  * :dtcompatible:`ti,am654-sdhci`（:github:`97172`）

* 传感器

  * :dtcompatible:`adi,adis1647x`（:github:`110012`）
  * :dtcompatible:`adi,adxl313`（:github:`114936`）
  * :dtcompatible:`adi,ltc4286`（:github:`105618`）
  * :dtcompatible:`adi,max30009`（:github:`112988`）
  * :dtcompatible:`bflb,tsen`（:github:`107717`）
  * :dtcompatible:`hamamatsu,s9706`（:github:`107607`）
  * :dtcompatible:`invensense,icm56622`（:github:`112362`）
  * :dtcompatible:`invensense,icm56686`（:github:`112362`）
  * :dtcompatible:`invensense,tad2144`（:github:`107994`）
  * :dtcompatible:`maxim,max30102`（:github:`108697`）
  * :dtcompatible:`maxim,max31826`（:github:`112398`）
  * :dtcompatible:`meas,htu21d`（:github:`106318`）
  * :dtcompatible:`meas,htu31d`（:github:`107532`）
  * :dtcompatible:`meas,ms5637`（:github:`106344`）
  * :dtcompatible:`microchip,pac194x`（:github:`105902`）
  * :dtcompatible:`nordic,nrf-vbat`（:github:`106102`）
  * :dtcompatible:`nxp,mcux-eqdc`（:github:`111927`）
  * :dtcompatible:`plantower,pmsa003i`（:github:`113377`）
  * :dtcompatible:`raspberrypi,bcm283x-vc-thermal`（:github:`110192`）
  * :dtcompatible:`realtek,bee-aon-qdec`（:github:`105129`）
  * :dtcompatible:`realtek,bee-basic-qdec`（:github:`105129`）
  * :dtcompatible:`realtek,bee-qdec`（:github:`105129`）
  * :dtcompatible:`sensylink,cht8315`（:github:`106391`）
  * :dtcompatible:`st,stm32-vddcore`（:github:`108053`）
  * :dtcompatible:`ti,fdc1004`（:github:`107233`）
  * :dtcompatible:`ti,tmp451`（:github:`108384`）
  * :dtcompatible:`zephyr,flow-meter`（:github:`111366`）
  * :dtcompatible:`zephyr,native-linux-temp`（:github:`114563`）

* 串行控制器

  * :dtcompatible:`elan,em32-uart`（:github:`103037`）
  * :dtcompatible:`microchip,uart-g1`（:github:`114034`）
  * :dtcompatible:`nxp,lpc84x-uart`（:github:`105928`）
  * :dtcompatible:`shakti,uart`（:github:`113000`）
  * :dtcompatible:`wch,ch5xx-uart`（:github:`111171`）
  * :dtcompatible:`wch,sdi-console`（:github:`109777`）

* :abbr:`SMbus（系统管理总线）`

  * :dtcompatible:`ite,it51xxx-smbus`（:github:`114832`）

* :abbr:`SPI（串行外设接口）`

  * :dtcompatible:`microchip,flexcom-g1-spi`（:github:`107467`）
  * :dtcompatible:`nuvoton,numaker-usci-spi`（:github:`109123`）
  * :dtcompatible:`realtek,ameba-spi`（:github:`108234`）
  * :dtcompatible:`realtek,bee-spi`（:github:`104958`）
  * :dtcompatible:`realtek,rts5817-spi`（:github:`106346`）
  * :dtcompatible:`renesas,rz-spi-b`（:github:`107073`）
  * :dtcompatible:`ti,mspm0-spi`（:github:`94726`）
  * :dtcompatible:`xlnx,zynqmp-qspi-1.0`（:github:`88466`）

* 转速表

  * :dtcompatible:`ene,kb106x-tach`（:github:`106739`）

* 定时器

  * :dtcompatible:`microchip,pit-g1-timer`（:github:`114034`）
  * :dtcompatible:`st,stm32u5-lptim`（:github:`112400`）
  * :dtcompatible:`ti,am26-rtitimer`（:github:`102545`）

* :abbr:`USB（通用串行总线）`

  * :dtcompatible:`espressif,esp32-usb-otg-fs`（:github:`111508`）
  * :dtcompatible:`espressif,esp32-usb-otg-hs`（:github:`111508`）
  * :dtcompatible:`infineon,usbhs`（:github:`106841`）
  * :dtcompatible:`microchip,udphs-g1-udc`（:github:`99620`）
  * :dtcompatible:`nordic,nrf-usbhs-bc12`（:github:`106759`）

* 视频

  * :dtcompatible:`zephyr,native-sim-video-fifo`（:github:`119658`）

* 唤醒控制器

  * :dtcompatible:`nxp,sleepcon-wuc`（:github:`113447`）
  * :dtcompatible:`nxp,wuc-wuu`（:github:`100866`）

* 看门狗

  * :dtcompatible:`arm,crsas-ma2-watchdog`（:github:`112700`）
  * :dtcompatible:`m5stack,m5pm1-wdt`（:github:`109961`）
  * :dtcompatible:`nordic,npm10xx-wdt`（:github:`109381`）
  * :dtcompatible:`nordic,nrf-gswdt`（:github:`110067`）
  * :dtcompatible:`nuvoton,numaker-wdt`（:github:`105247`）
  * :dtcompatible:`realtek,ameba-watchdog`（:github:`106672`）
  * :dtcompatible:`realtek,bee-core-wdt`（:github:`107021`）
  * :dtcompatible:`ti,mspm0-watchdog`（:github:`95304`）

* Wi-Fi

  * :dtcompatible:`bflb,wifi6`（:github:`113078`）
  * :dtcompatible:`espressif,esp-hosted-mcu`（:github:`114532`）
  * :dtcompatible:`espressif,esp-hosted-mcu-wifi`（:github:`114532`）
  * :dtcompatible:`realtek,ameba-wifi`（:github:`105614`）
  * :dtcompatible:`st,st67w611m1`（:github:`111583`）
  * :dtcompatible:`zephyr,wifi-hwsim`（:github:`111236`）

新示例
***********

..
  与开发板和驱动相同，此列表也将在发布时重新计算。
  只需链接示例，更多细节放在示例文档本身中。

* :zephyr:code-sample:`adi-gpio-wakeup`
* :zephyr:code-sample:`adi-pm`
* :zephyr:code-sample:`assert`
* :zephyr:code-sample:`autanalog_fir_fifo`
* :zephyr:code-sample:`bluetooth_cap_handover`
* :zephyr:code-sample:`buzzer-tone`
* :zephyr:code-sample:`coap-client-tcp`
* :zephyr:code-sample:`color-palette`
* :zephyr:code-sample:`coredump-udp-demo-shell`
* :zephyr:code-sample:`coresight_stm_shell`
* :zephyr:code-sample:`cpu_freq_thermal_cap`
* :zephyr:code-sample:`cpu_freq_timing_noise`
* :zephyr:code-sample:`cs40l26`
* :zephyr:code-sample:`dali`
* :zephyr:code-sample:`dhcpv6-pd`
* :zephyr:code-sample:`esp32-qdec-trigger`
* :zephyr:code-sample:`espnow`
* :zephyr:code-sample:`fido2`
* :zephyr:code-sample:`flow-meter`
* :zephyr:code-sample:`fota-http`
* :zephyr:code-sample:`frdm-mcxe31b-system-off`
* :zephyr:code-sample:`i2c-tiny-usb`
* :zephyr:code-sample:`logging_multidomain`
* :zephyr:code-sample:`lora-duty-cycle`
* :zephyr:code-sample:`lp586x`
* :zephyr:code-sample:`mcp-server-hello-world`
* :zephyr:code-sample:`mfd_charger`
* :zephyr:code-sample:`mspi-throughput`
* :zephyr:code-sample:`net-rtp`
* :zephyr:code-sample:`nrf-sys-event`
* :zephyr:code-sample:`nxp_mcx_s2ram`
* :zephyr:code-sample:`nxp_mcx_system_off`
* :zephyr:code-sample:`nxp_smartdma_mem_to_mem`
* :zephyr:code-sample:`pm-latency`
* :zephyr:code-sample:`pulse_io_byte_transfer`
* :zephyr:code-sample:`qdec_multi`
* :zephyr:code-sample:`quic-client-echo`
* :zephyr:code-sample:`quic-service-echo`
* :zephyr:code-sample:`riscv-aia-smp-uart-echo`
* :zephyr:code-sample:`riscv-aia-uart-echo`
* :zephyr:code-sample:`rpi-board-info`
* :zephyr:code-sample:`rpmsg-lite`
* :zephyr:code-sample:`rw612_pm_flash_check`
* :zephyr:code-sample:`spi-rtio-loopback`
* :zephyr:code-sample:`ssh-server-client`
* :zephyr:code-sample:`sx9500`
* :zephyr:code-sample:`tad2144`
* :zephyr:code-sample:`tflite-neutron`
* :zephyr:code-sample:`tfm_fwu`
* :zephyr:code-sample:`tm6605`
* :zephyr:code-sample:`tmc6460`
* :zephyr:code-sample:`tracing-pipeline`
* :zephyr:code-sample:`tsn-switch`
* :zephyr:code-sample:`wifi-ble-provisioning`
* :zephyr:code-sample:`wifi-mesh`
* :zephyr:code-sample:`wifi-mesh-ip`
* :zephyr:code-sample:`zms-cycle-count`
* :zephyr_file:`samples/drivers/clock_monitor/check_freq`
* :zephyr_file:`samples/drivers/clock_monitor/measure_freq`

库 / 子系统
**********************

* 加密

  * 添加了对 AES CFB 和 OFB 密码模式的支持。

* Mbed TLS

  * Mbed TLS 已更新到 4.1.1 版本。发布说明可在
    `此处 <https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-4.1.1>`_ 找到。

  * TF-PSA-Crypto 已更新到 1.1.1 版本。发布说明可在
    `此处 <https://github.com/Mbed-TLS/TF-PSA-Crypto/releases/tag/tf-psa-crypto-1.1.1>`_ 找到。

  * 添加 :kconfig:option:`CONFIG_TF_PSA_CRYPTO_DISPATCH_DIR`，
    使 TF-PSA-Crypto 能够使用加密操作分派的自定义实现。
    这通过使用加速器感知的分派实现使加密操作的
    硬件加速成为可能。

* TF-M

  * TF-M 已从 2.2.2 版本更新到 2.3.1 版本。发布说明可在以下地址找到：

  * https://trustedfirmware-m.readthedocs.io/en/latest/releases/2.3.0.html
  * https://trustedfirmware-m.readthedocs.io/en/tf-mv2.3.1/releases/2.3.1.html

  * TF-M 现在可通过将 ``ZEPHYR_TOOLCHAIN_VARIANT`` 设置为
    ``zephyr/llvm`` 使用 LLVM 编译。

* DFU

  * 添加 :kconfig:option:`CONFIG_IMG_CUSTOM_SECTOR_SIZE`，
    允许 MCUboot 使用不同的扇区大小来减小
    swap-using-offset 状态区域的大小。

* 管理

  * 添加 :ref:`fota_http` 库，一个空中固件客户端，
    通过 HTTP 或 HTTPS 将 MCUboot 镜像直接下载到
    次级槽位，支持可选的断点续传、重定向跟随、
    SHA-256 验证和 ``fota`` shell 命令。

* LoRa / LoRaWAN

  * 添加原生 LoRaWAN 后端
    （:kconfig:option:`CONFIG_LORA_MODULE_BACKEND_NATIVE`），
    直接在 LoRa 无线电驱动之上实现 LoRaWAN 1.0.x Class A，
    不依赖 Semtech LoRaMac-node。目前支持 EU868 区域。
  * :c:member:`lora_modem_config.sync_word`

* 管理

  * MCUmgr

    * 镜像管理客户端现在支持 SHA-512 镜像摘要。
      它可以列出并选择用于测试或确认的镜像，
      针对使用 :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_USES