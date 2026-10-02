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

.. _zephyr_4.1:

Zephyr 4.1.0
############

我们很高兴宣布 Zephyr 4.1.0 版本的发布。
本次发布的主要增强功能包括：

**性能改进**
  已实现多个核心 Zephyr 内核函数的性能改进，惠及所有支持的硬件架构。

  还添加了对 :zephyr_file:`thread_metric <tests/benchmarks/thread_metric>` RTOS
  基准测试的官方移植，使开发人员更容易测量 Zephyr 在其硬件上的性能并与其他 RTOS 进行比较。

**对 IAR 编译器的实验性支持**
  :ref:`toolchain_iar_arm` 现在可用于构建 Zephyr 应用程序。这是一个实验性功能，
  预计将在未来版本中改进。

**Zephyr 上 Rust 的初始支持**
  现在可以使用 Rust 编写 Zephyr 应用程序。:ref:`language_rust` 可通过可选的 Zephyr 模块使用，
  并提供了多个代码示例作为起点。

**USB MIDI 类驱动**
  引入了新的 :ref:`USB MIDI 2.0 <usbd_midi2>` 设备驱动，允许 Zephyr 设备
  通过 USB 与 MIDI 控制器和乐器通信。

**扩展的板级支持**
  本次发布新增了对 70 块 :ref:`新开发板 <boards_added_in_zephyr_4_1>` 和 11 个
  :ref:`新盾牌 <shields_added_in_zephyr_4_1>` 的支持。

  这包括 :zephyr:board:`rpi_pico2` 和 :zephyr:board:`ch32v003evt` 等非常流行的开发板，
  若干具备 CAN+USB 能力的开发板使其成为运行基于 Zephyr 的开源 `CANnectivity`_
  固件的绝佳候选，以及所有支持架构上的数十块其他开发板。

.. _CANnectivity: https://cannectivity.org/

从 Zephyr v4.0.0 迁移到 Zephyr v4.1.0 时所需或建议的更改概述可在单独的 :ref:`迁移指南 <migration_4.1>` 中找到。

以下章节按组件提供详细的更改列表。

安全漏洞相关
******************************

本次发布解决了以下 CVE：

* :cve:`2025-1673` `Zephyr 项目问题跟踪器 GHSA-jjhx-rrh4-j8mx
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jjhx-rrh4-j8mx>`_

* :cve:`2025-1674` `Zephyr 项目问题跟踪器 GHSA-x975-8pgf-qh66
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-x975-8pgf-qh66>`_

* :cve:`2025-1675` `Zephyr 项目问题跟踪器 GHSA-2m84-5hfw-m8v4
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-2m84-5hfw-m8v4>`_

更详细的信息可在以下地址找到：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

API 更改
***********

移除的 API 和选项
========================

* 已移除遗留的蓝牙 HCI 驱动 API。它已被遵循标准 Zephyr 驱动模型的
  :c:group:`新 API <bt_hci_api>` 取代。

* 已移除 ``CAN_MAX_STD_ID``（由 :c:macro:`CAN_STD_ID_MASK` 取代）和
  ``CAN_MAX_EXT_ID``（由 :c:macro:`CAN_EXT_ID_MASK` 取代）CAN API 宏。

* 已移除 ``can_get_min_bitrate()``（由 :c:func:`can_get_bitrate_min` 取代）和
  ``can_get_max_bitrate()``（由 :c:func:`can_get_bitrate_max` 取代）CAN API 函数。

* 已移除 ``can_calc_prescaler()`` CAN API 函数。

* 已移除 :kconfig:option:`CONFIG_NET_SOCKETS_POSIX_NAMES` 选项。
  它是一个遗留选项，用于允许用户在未启用 POSIX API 的情况下调用 BSD 套接字 API。
  此移除意味着要使用 POSIX API 套接字调用，需要启用 :kconfig:option:`CONFIG_POSIX_API` 选项。
  如果应用程序不想或无法启用该选项，则套接字 API 调用需要加 ``zsock_`` 前缀。

* 已移除返回*字节*计数且仅支持 8 位深度的 ``video_pix_fmt_bpp()`` 函数，
  改用返回*位*计数且支持任意色彩深度的 :c:func:`video_bits_per_pixel()`。

* ``video_stream_start()`` 和 ``video_stream_stop()`` 驱动 API 已由 ``video_set_stream()`` 取代。

* :kconfig:option:`CONFIG_WIFI_NM_WPA_SUPPLICANT_CRYPTO`

* :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_EXCLUSIVE` 选项在弃用后已被移除，
  改用 :kconfig:option:`CONFIG_PM_DEVICE_SYSTEM_MANAGED`。

* 已移除 ``z_pm_save_idle_exit()`` PM API 函数。

* 已移除结构体 ``z_arch_esf_t``。请改用 ``struct arch_esf``。

* 已移除以下网络选项：

    * ``CONFIG_NET_PKT_BUF_DATA_POOL_SIZE``
    * ``CONFIG_NET_TCP_ACK_TIMEOUT``

弃用的 API 和选项
===========================

* :c:func:`bt_le_set_auto_conn` API 函数。应用程序开发人员可以在其应用程序代码中
  在 :c:member:`bt_conn_cb.disconnected` 回调被调用时重新连接到对端，以实现相同的功能。

* :kconfig:option:`CONFIG_NATIVE_APPLICATION` 已弃用。

* 弃用了 Stream Flash API 中的 :c:func:`stream_flash_erase_page`。
  相同的功能可以使用 :c:func:`flash_area_erase` 或 :c:func:`flash_erase` 实现。
  不过，当 stream flash 本应执行擦除时，擦除设备会导致
  stream flash 中的数据丢失。只有两种情况应直接擦除设备：

  1. 当 Stream Flash 未配置为自行执行擦除时
  2. 当擦除用于在 Stream Flash 使用指定区域之前或之后移除数据时。

* Pipe API 已重新设计。
  当设置 ``CONFIG_MULTITHREADING`` 时，新 API 默认启用。

  * 弃用了 ``CONFIG_PIPES`` Kconfig 选项。
  * 引入了 ``k_pipe_close(..)`` 函数。
  * ``k_pipe_put(..)`` 转换为 ``k_pipe_write(..)``。
  * ``k_pipe_get(..)`` 转换为 ``k_pipe_read(..)``。
  * ``k_pipe_flush(..)`` 和 ``k_pipe_buffer_flush()`` 可转换为 ``k_pipe_reset(..)``。

  * 不再支持 pipe 的动态分配。

    - 已移除 ``k_pipe_alloc_init(..)`` API。
    - 已移除 ``k_pipe_cleanup(..)`` API。

  * 不再支持查询 pipe 中的字节数。

    - 已移除 ``k_pipe_read_avail(..)`` API。
    - 已移除 ``k_pipe_write_avail(..)`` API。

* 对于 native_sim 目标，:kconfig:option:`CONFIG_NATIVE_SIM_NATIVE_POSIX_COMPAT` 已默认
  切换为 ``n``，且该选项已弃用。

* :kconfig:option:`CONFIG_BT_BUF_ACL_RX_COUNT`

* 在 v3.7 中作为弃用项添加的所有 HWMv1 开发板名称别名现已移除
  （:github:`82247`）。

* TinyCrypt 库已弃用，因为其上游版本不再维护。
  PSA Crypto API 现在是 Zephyr 推荐的加密库。

* :kconfig:option:`CONFIG_BT_DIS_MODEL` 和 :kconfig:option:`CONFIG_BT_DIS_MANUF` 已弃用。
  应用程序开发人员可以使用新的 :kconfig:option:`CONFIG_BT_DIS_MODEL_NUMBER_STR` 和
  :kconfig:option:`CONFIG_BT_DIS_MANUF_NAME_STR` Kconfig 选项实现相同的配置。

新的 API 和选项
====================

..
  在此处链接新 API，如果你认为有必要可以分组，无需花哨，
  只需列出链接，其中应包含文档。如果你认为需要添加更多细节，
  请将其添加到 API 文档代码中。

* 架构

  * :kconfig:option:`CONFIG_ARCH_HAS_CUSTOM_CURRENT_IMPL`
  * :kconfig:option:`CONFIG_RISCV_CURRENT_VIA_GP`

* 蓝牙

  * 音频

    * :c:func:`bt_bap_broadcast_source_register_cb`
    * :c:func:`bt_bap_broadcast_source_unregister_cb`
    * :c:func:`bt_cap_commander_distribute_broadcast_code`
    * ``bt_ccp`` API（进行中）
    * :c:func:`bt_pacs_register`
    * :c:func:`bt_pacs_unregister`

  * 主机

    * :c:func:`bt_conn_is_type`

  * Mesh

    * :c:member:`bt_mesh_health_cli::update` 回调可用于定期更新
      健康客户端发布的消息。

  * 服务

    * :kconfig:option:`CONFIG_BT_DIS_MODEL_NUMBER` 和
      :kconfig:option:`CONFIG_BT_DIS_MANUF_NAME` Kconfig 选项可用于控制
      设备信息服务（DIS）中型号名称字符串和制造商名称字符串特性的存在。
      :kconfig:option:`CONFIG_BT_DIS_MODEL_NUMBER_STR` 和
      :kconfig:option:`CONFIG_BT_DIS_MANUF_NAME_STR` Kconfig 选项现在用于设置
      这些特性中的字符串值。它们取代了弃用的
      :kconfig:option:`CONFIG_BT_DIS_MODEL` 和 :kconfig:option:`CONFIG_BT_DIS_MANUF` Kconfig 的功能。

* 构建系统

  * Sysbuild

    * 新引入的 MCUboot 使用偏移量的交换模式可通过 sysbuild 使用
      ``SB_CONFIG_MCUBOOT_MODE_SWAP_USING_OFFSET`` 选择，此模式为实验性。

* 加密

  * :kconfig:option:`CONFIG_MBEDTLS_PSA_STATIC_KEY_SLOTS`
  * :kconfig:option:`CONFIG_MBEDTLS_PSA_KEY_SLOT_COUNT`

* I3C

  * :kconfig:option:`CONFIG_I3C_TARGET_BUFFER_MODE`
  * :kconfig:option:`CONFIG_I3C_RTIO`
  * :c:func:`i3c_ibi_hj_response`
  * :c:func:`i3c_ccc_do_getacccr`
  * :c:func:`i3c_device_controller_handoff`

* 管理

  * hawkBit

    * hawkBit 子系统现在内部使用状态机框架。
    * :kconfig:option:`CONFIG_HAWKBIT_TENANT`
    * :kconfig:option:`CONFIG_HAWKBIT_EVENT_CALLBACKS`
    * :kconfig:option:`CONFIG_HAWKBIT_SAVE_PROGRESS`

  * MCUmgr

    * 镜像管理 :c:macro:`MGMT_EVT_OP_IMG_MGMT_DFU_CONFIRMED` 现在具有镜像数据字段
      :c:struct:`img_mgmt_image_confirmed`。

* MCUboot

  * 当设置了加密密钥 Kconfig 时，签名十六进制文件的镜像头中现在会设置加密标志。

* 网络：

  * CoAP

    * :c:func:`coap_client_cancel_request`

  * DHCP

    * :kconfig:option:`CONFIG_NET_DHCPV4_SERVER_OPTION_ROUTER`
    * :kconfig:option:`CONFIG_NET_DHCPV4_OPTION_DNS_ADDRESS`
    * :kconfig:option:`CONFIG_NET_DHCPV6_OPTION_DNS_ADDRESS`

  * DNS

    * :kconfig:option:`CONFIG_MDNS_RESPONDER_PROBE`

  * 以太网

    * 允许用户在从以太网网络接收数据时指定协议扩展。
      这使得无需更改核心 Zephyr 网络代码即可为以太网协议类型注册处理器。:c:macro:`NET_L3_REGISTER`
    * :kconfig:option:`CONFIG_NET_L2_ETHERNET_RESERVE_HEADER`

  * HTTP

    * 扩展了 :c:macro:`HTTP_SERVICE_DEFINE` 以允许指定默认回退资源处理器。
    * :kconfig:option:`CONFIG_HTTP_SERVER_REPORT_FAILURE_REASON`
    * :kconfig:option:`CONFIG_HTTP_SERVER_TLS_USE_ALPN`

  * IPv4

    * :kconfig:option:`CONFIG_NET_IPV4_PMTU`

  * IPv6

    * :kconfig:option:`CONFIG_NET_IPV6_PMTU`

  * LwM2M

    * :c:func:`lwm2m_pull_context_set_sockopt_callback`

  * MQTT-SN

    * 添加了对网关广播和发现的支持：

      * :c:func:`mqtt_sn_add_gw`
      * :c:func:`mqtt_sn_search`

  * OpenThread

    * :kconfig:option:`CONFIG_OPENTHREAD_WAKEUP_COORDINATOR`
    * :kconfig:option:`CONFIG_OPENTHREAD_WAKEUP_END_DEVICE`
    * :kconfig:option:`CONFIG_OPENTHREAD_PLATFORM_MESSAGE_MANAGEMENT`
    * :kconfig:option:`CONFIG_OPENTHREAD_TCAT_MULTIRADIO_CAPABILITIES`

  * 套接字

    * 添加了对新套接字选项的支持：

      * :c:macro:`IP_LOCAL_PORT_RANGE`
      * :c:macro:`IP_MULTICAST_IF`
      * :c:macro:`IPV6_MULTICAST_IF`
      * :c:macro:`IP_MTU`
      * :c:macro:`IPV6_MTU`

  * 其他

    * :kconfig:option:`CONFIG_NET_STATISTICS_VIA_PROMETHEUS`

* 视频

  * :c:func:`video_set_stream()` 驱动 API 已取代 :c:func:`video_stream_start()` 和
    :c:func:`video_stream_stop()` 驱动 API。

* 其他

  * :kconfig:option:`CONFIG_BT_BUF_ACL_RX_COUNT_EXTRA`
  * :c:macro:`DT_ANY_INST_HAS_BOOL_STATUS_OKAY`
  * :c:struct:`led_dt_spec`
  * :kconfig:option:`CONFIG_STEP_DIR_STEPPER`

.. _boards_added_in_zephyr_4_1:

新开发板
**********
..
  你可以在发布周期中贡献新开发板时更新此列表，以便让可能正在查看发布说明工作草稿的人看到。
  但请注意，此列表将在发布时重新计算，因此你*不必*更新它。
  无论如何，只需链接开发板，更多细节放在开发板描述中。

* Adafruit Industries, LLC

   * :zephyr:board:`adafruit_feather_m4_express`（``adafruit_feather_m4_express``）
   * :zephyr:board:`adafruit_macropad_rp2040`（``adafruit_macropad_rp2040``）
   * :zephyr:board:`adafruit_qt_py_esp32s3`（``adafruit_qt_py_esp32s3``）

* Advanced Micro Devices (AMD), Inc.

   * :zephyr:board:`acp_6_0_adsp`（``acp_6_0_adsp``）

* Analog Devices, Inc.

   * :zephyr:board:`ad_swiot1l_sl`（``ad_swiot1l_sl``）
   * :zephyr:board:`max32650evkit`（``max32650evkit``）
   * :zephyr:board:`max32650fthr`（``max32650fthr``）
   * :zephyr:board:`max32660evsys`（``max32660evsys``）
   * :zephyr:board:`max78000evkit`（``max78000evkit``）
   * :zephyr:board:`max78000fthr`（``max78000fthr``）
   * :zephyr:board:`max78002evkit`（``max78002evkit``）

* Antmicro

   * :zephyr:board:`myra_sip_baseboard`（``myra_sip_baseboard``）

* BeagleBoard.org Foundation

   * :zephyr:board:`beagley_ai`（``beagley_ai``）

* FANKE Technology Co., Ltd.

   * :zephyr:board:`fk750m1_vbt6`（``fk750m1_vbt6``）

* Google, Inc.

   * :zephyr:board:`google_icetower`（``google_icetower``）
   * :zephyr:board:`google_quincy`（``google_quincy``）

* Infineon Technologies

   * :zephyr:board:`cy8ckit_062s2_ai`（``cy8ckit_062s2_ai``）

* Khadas

   * :zephyr:board:`khadas_edge2`（``khadas_edge2``）

* Lilygo Shenzhen Xinyuan Electronic Technology Co., Ltd

   * :zephyr:board:`ttgo_t7v1_5`（``ttgo_t7v1_5``）
   * :zephyr:board:`ttgo_t8s3`（``ttgo_t8s3``）

* M5Stack

   * :zephyr:board:`m5stack_cores3`（``m5stack_cores3``）

* Makerbase Co., Ltd.

   * :zephyr:board:`mks_canable_v20`（``mks_canable_v20``）

* MediaTek Inc.

   * MT8186（``mt8186``）
   * MT8188（``mt8188``）
   * MT8196（``mt8196``）

* NXP Semiconductors

   * :zephyr:board:`frdm_mcxw72`（``frdm_mcxw72``）
   * :zephyr:board:`imx91_evk`（``imx91_evk``）
   * :zephyr:board:`mcxw72_evk`（``mcxw72_evk``）
   * :zephyr:board:`mimxrt700_evk`（``mimxrt700_evk``）

* Nordic Semiconductor

   * nRF54L09 PDK（``nrf54l09pdk``）

* Norik Systems

   * :zephyr:board:`octopus_io_board`（``octopus_io_board``）
   * :zephyr:board:`octopus_som`（``octopus_som``）

* Panasonic Corporation

   * PAN B511 评估板（``panb511evb``）

* Peregrine Consultoria e Servicos

   * :zephyr:board:`sam4l_wm400_cape`（``sam4l_wm400_cape``）

* Qorvo, Inc.

   * :zephyr:board:`decawave_dwm3001cdk`（``decawave_dwm3001cdk``）

* RAKwireless Technology Limited

   * :zephyr:board:`rak3172`（``rak3172``）

* Raspberry Pi Foundation

   * :zephyr:board:`rpi_pico2`（``rpi_pico2``）

* Realtek Semiconductor Corp.

   * :zephyr:board:`rts5912_evb`（``rts5912_evb``）

* Renesas Electronics Corporation

   * :zephyr:board:`ek_ra2l1`（``ek_ra2l1``）
   * :zephyr:board:`ek_ra4l1`（``ek_ra4l1``）
   * :zephyr:board:`ek_ra4m1`（``ek_ra4m1``）
   * :zephyr:board:`fpb_ra4e1`（``fpb_ra4e1``）
   * :zephyr:board:`rzg3s_smarc`（``rzg3s_smarc``）
   * :zephyr:board:`voice_ra4e1`（``voice_ra4e1``）

* STMicroelectronics

   * :zephyr:board:`nucleo_c071rb`（``nucleo_c071rb``）
   * :zephyr:board:`nucleo_f072rb`（``nucleo_f072rb``）
   * :zephyr:board:`nucleo_h7s3l8`（``nucleo_h7s3l8``）
   * :zephyr:board:`nucleo_n657x0_q`（``nucleo_n657x0_q``）
   * :zephyr:board:`nucleo_wb07cc`（``nucleo_wb07cc``）
   * :zephyr:board:`stm32f413h_disco`（``stm32f413h_disco``）
   * :zephyr:board:`stm32n6570_dk`（``stm32n6570_dk``）

* Seeed Technology Co., Ltd

   * :zephyr:board:`xiao_esp32c6`（``xiao_esp32c6``）

* Shenzhen Fuyuansheng Electronic Technology Co., Ltd.

   * :zephyr:board:`ucan`（``ucan``）

* Silicon Laboratories

   * :zephyr:board:`siwx917_rb4338a`（``siwx917_rb4338a``）
   * :zephyr:board:`xg23_rb4210a`（``xg23_rb4210a``）
   * :zephyr:board:`xg24_ek2703a`（``xg24_ek2703a``）
   * :zephyr:board:`xg29_rb4412a`（``xg29_rb4412a``）

* Texas Instruments

   * :zephyr:board:`lp_em_cc2340r5`（``lp_em_cc2340r5``）

* Toradex AG

   * :zephyr:board:`verdin_imx8mm`（``verdin_imx8mm``）

* Waveshare Electronics

   * :zephyr:board:`rp2040_zero`（``rp2040_zero``）

* WeAct Studio

   * :zephyr:board:`mini_stm32h7b0`（``mini_stm32h7b0``）
   * WeAct Studio STM32H5 核心板（``weact_stm32h5_core``）

* WinChipHead

   * :zephyr:board:`ch32v003evt`（``ch32v003evt``）

* Würth Elektronik GmbH.

   * :zephyr:board:`we_oceanus1ev`（``we_oceanus1ev``）
   * :zephyr:board:`we_orthosie1ev`（``we_orthosie1ev``）

* 其他

   * :zephyr:board:`canbardo`（``canbardo``）
   * :zephyr:board:`candlelight`（``candlelight``）
   * :zephyr:board:`candlelightfd`（``candlelightfd``）
   * :zephyr:board:`esp32c3_supermini`（``esp32c3_supermini``）
   * :zephyr:board:`promicro_nrf52840`（``promicro_nrf52840``）

.. _shields_added_in_zephyr_4_1:

新盾牌
=============

  * :ref:`Abrobot ESP32 C3 OLED 盾牌 <abrobot_esp32c3oled_shield>`
  * :ref:`Adafruit Adalogger Featherwing 盾牌 <adafruit_adalogger_featherwing_shield>`
  * :ref:`Adafruit AW9523 GPIO 扩展器和 LED 驱动器 <adafruit_aw9523>`
  * :ref:`MikroElektronika ETH 3 Click <mikroe_eth3_click>`
  * :ref:`P3T1755DP Arduino® 盾牌评估板 <p3t1755dp_ard_i2c_shield>`
  * :ref:`P3T1755DP Arduino® 盾牌评估板 <p3t1755dp_ard_i3c_shield>`
  * :ref:`Digilent Pmod SD <pmod_sd>`
  * :ref:`Renesas DA14531 Pmod 板 <renesas_us159_da14531evz_shield>`
  * :ref:`RTKMIPILCDB00000BE MIPI 显示屏 <rtkmipilcdb00000be>`
  * :ref:`Seeed W5500 以太网盾牌 <seeed_w5500>`
  * :ref:`ST B-CAMS-OMV-MB1683 <st_b_cams_omv_mb1683>`

新驱动
***********
..
  与开发板相同，此列表也将在发布时重新计算。
  只需链接驱动，更多细节放在绑定描述中

* :abbr:`ADC（模数转换器）`

   * :dtcompatible:`adi,ad4114-adc`
   * :dtcompatible:`adi,ad7124-adc`
   * :dtcompatible:`st,stm32n6-adc`
   * :dtcompatible:`ti,ads114s06`
   * :dtcompatible:`ti,ads124s06`
   * :dtcompatible:`ti,ads124s08`
   * :dtcompatible:`ti,ads131m02`
   * :dtcompatible:`ti,tla2022`
   * :dtcompatible:`ti,tla2024`

* ARM 架构

   * :dtcompatible:`nxp,nbu`

* 音频

   * :dtcompatible:`cirrus,cs43l22`
   * :dtcompatible:`intel,adsp-mic-privacy`

* 蓝牙

   * :dtcompatible:`renesas,bt-hci-da1453x`
   * :dtcompatible:`silabs,siwx91x-bt-hci`
   * :dtcompatible:`st,hci-stm32wb0`

* 充电器

   * :dtcompatible:`nxp,pf1550-charger`

* 时钟控制

   * :dtcompatible:`atmel,sam0-gclk`
   * :dtcompatible:`atmel,sam0-mclk`
   * :dtcompatible:`atmel,sam0-osc32kctrl`
   * :dtcompatible:`nordic,nrf-hsfll-global`
   * :dtcompatible:`nuvoton,npcm-pcc`
   * :dtcompatible:`realtek,rts5912-sccon`
   * :dtcompatible:`renesas,rz-cpg`
   * :dtcompatible:`st,stm32n6-cpu-clock-mux`
   * :dtcompatible:`st,stm32n6-hse-clock`
   * :dtcompatible:`st,stm32n6-ic-clock-mux`
   * :dtcompatible:`st,stm32n6-pll-clock`
   * :dtcompatible:`st,stm32n6-rcc`
   * :dtcompatible:`wch,ch32v00x-hse-clock`
   * :dtcompatible:`wch,ch32v00x-hsi-clock`
   * :dtcompatible:`wch,ch32v00x-pll-clock`
   * :dtcompatible:`wch,rcc`

* 比较器

   * :dtcompatible:`silabs,acmp`

* 计数器

   * :dtcompatible:`adi,max32-rtc-counter`
   * :dtcompatible:`renesas,rz-gtm-counter`

* CPU

   * :dtcompatible:`wch,qingke-v2`

* :abbr:`DAC（数模转换器）`

   * :dtcompatible:`adi,max22017-dac`
   * :dtcompatible:`renesas,ra-dac`
   * :dtcompatible:`renesas,ra-dac-global`

* :abbr:`DAI（数字音频接口）`

   * :dtcompatible:`mediatek,afe`
   * :dtcompatible:`nxp,dai-micfil`

* 显示

   * :dtcompatible:`ilitek,ili9806e-dsi`
   * :dtcompatible:`renesas,ra-glcdc`
   * :dtcompatible:`solomon,ssd1309fb`

* :abbr:`DMA（直接内存访问）`

   * :dtcompatible:`infineon,cat1-dma`
   * :dtcompatible:`nxp,sdma`
   * :dtcompatible:`silabs,ldma`
   * :dtcompatible:`silabs,siwx91x-dma`
   * :dtcompatible:`xlnx,axi-dma-1.00.a`
   * :dtcompatible:`xlnx,eth-dma`

* :abbr:`DSA（分布式交换架构）`

   * :dtcompatible:`nxp,netc-switch`

* :abbr:`EEPROM（电可擦除可编程只读存储器）`

  *  :dtcompatible:`fujitsu,mb85rsxx`

* 以太网

   * :dtcompatible:`davicom,dm8806-phy`
   * :dtcompatible:`microchip,lan9250`
   * :dtcompatible:`microchip,t1s-phy`
   * :dtcompatible:`microchip,vsc8541`
   * :dtcompatible:`renesas,ra-ethernet`
   * :dtcompatible:`sensry,sy1xx-mac`

* 固件

   * :dtcompatible:`arm,scmi-power`

* 闪存控制器

   * :dtcompatible:`silabs,siwx91x-flash-controller`
   * :dtcompatible:`ti,cc23x0-flash-controller`

* :abbr:`FPGA（现场可编程门阵列）`

   * :dtcompatible:`lattice,ice40-fpga-base`
   * :dtcompatible:`lattice,ice40-fpga-bitbang`

* :abbr:`GPIO（通用输入/输出）`

   * :dtcompatible:`adi,max22017-gpio`
   * :dtcompatible:`adi,max22190-gpio`
   * :dtcompatible:`awinic,aw9523b-gpio`
   * :dtcompatible:`ite,it8801-gpio`
   * :dtcompatible:`microchip,mec5-gpio`
   * :dtcompatible:`nordic,npm2100-gpio`
   * :dtcompatible:`nxp,pca6416`
   * :dtcompatible:`raspberrypi,rp1-gpio`
   * :dtcompatible:`realtek,rts5912-gpio`
   * :dtcompatible:`renesas,ra-gpio-mipi-header`
   * :dtcompatible:`renesas,rz-gpio`
   * :dtcompatible:`renesas,rz-gpio-int`
   * :dtcompatible:`sensry,sy1xx-gpio`
   * :dtcompatible:`silabs,siwx91x-gpio`
   * :dtcompatible:`silabs,siwx91x-gpio-port`
   * :dtcompatible:`silabs,siwx91x-gpio-uulp`
   * :dtcompatible:`st,dcmi-camera-fpu-330zh`
   * :dtcompatible:`st,mfxstm32l152`
   * :dtcompatible:`stemma-qt-connector`
   * :dtcompatible:`ti,cc23x0-gpio`
   * :dtcompatible:`wch,gpio`

* IEEE 802.15.4 HDLC RCP 接口

   * :dtcompatible:`nxp,hdlc-rcp-if`
   * :dtcompatible:`uart,hdlc-rcp-if`

* :abbr:`I2C（集成电路总线）`

   * :dtcompatible:`nordic,nrf-twis`
   * :dtcompatible:`nxp,ii2c`
   * :dtcompatible:`ti,omap-i2c`
   * :dtcompatible:`ti,tca9544a`

* :abbr:`I3C（改进型集成电路总线）`

   * :dtcompatible:`snps,designware-i3c`
   * :dtcompatible:`st,stm32-i3c`

* IEEE 802.15.4

   * :dtcompatible:`nxp,mcxw-ieee802154`

* 输入

   * :dtcompatible:`cypress,cy8cmbr3xxx`
   * :dtcompatible:`ite,it8801-kbd`
   * :dtcompatible:`microchip,cap12xx`
   * :dtcompatible:`nintendo,nunchuk`

* 中断控制器

   * :dtcompatible:`renesas,rz-ext-irq`
   * :dtcompatible:`wch,pfic`

* 邮箱

   * :dtcompatible:`linaro,ivshmem-mbox`
   * :dtcompatible:`ti,omap-mailbox`

* :abbr:`MDIO（管理数据输入/输出）`

   * :dtcompatible:`microchip,lan865x-mdio`
   * :dtcompatible:`renesas,ra-mdio`
   * :dtcompatible:`sensry,sy1xx-mdio`

* 内存控制器

   * :dtcompatible:`renesas,ra-sdram`

* :abbr:`MFD（多功能设备）`

   * :dtcompatible:`adi,max22017`
   * :dtcompatible:`awinic,aw9523b`
   * :dtcompatible:`ite,it8801-altctrl`
   * :dtcompatible:`ite,it8801-mfd`
   * :dtcompatible:`ite,it8801-mfd-map`
   * :dtcompatible:`maxim,ds3231-mfd`
   * :dtcompatible:`nordic,npm2100`
   * :dtcompatible:`nxp,pf1550`

* :abbr:`MIPI DSI（移动行业处理器接口显示串行接口）`

   * :dtcompatible:`renesas,ra-mipi-dsi`

* 杂项

   * :dtcompatible:`nordic,nrf-bicr`
   * :dtcompatible:`nordic,nrf-ppib`
   * :dtcompatible:`renesas,ra-external-interrupt`

* :abbr:`MMU / MPU（内存管理单元 / 内存保护单元）`

   * :dtcompatible:`nxp,sysmpu`

* :abbr:`MTD（内存技术设备）`

   * :dtcompatible:`nxp,s32-qspi-hyperflash`
   * :dtcompatible:`nxp,xspi-mx25um51345g`
   * :dtcompatible:`ti,cc23x0-ccfg-flash`

* 网络

   * :dtcompatible:`silabs,series2-radio`

* :abbr:`PCIe（外围组件互连快速）`

   * :dtcompatible:`brcm,brcmstb-pcie`

* PHY

   * :dtcompatible:`renesas,ra-usbphyc`
   * :dtcompatible:`st,stm32u5-otghs-phy`

* 引脚控制

   * :dtcompatible:`realtek,rts5912-pinctrl`
   * :dtcompatible:`renesas,rzg-pinctrl`
   * :dtcompatible:`sensry,sy1xx-pinctrl`
   * :dtcompatible:`silabs,dbus-pinctrl`
   * :dtcompatible:`silabs,siwx91x-pinctrl`
   * :dtcompatible:`ti,cc23x0-pinctrl`
   * :dtcompatible:`wch,afio`

* :abbr:`PWM（脉冲宽度调制）`

   * :dtcompatible:`atmel,sam0-tc-pwm`
   * :dtcompatible:`ite,it8801-pwm`
   * :dtcompatible:`renesas,rz-gpt-pwm`
   * :dtcompatible:`zephyr,fake-pwm`

* 四线 SPI

   * :dtcompatible:`nxp,s32-qspi-sfp-frad`
   * :dtcompatible:`nxp,s32-qspi-sfp-mdad`

* 稳压器

   * :dtcompatible:`nordic,npm2100-regulator`
   * :dtcompatible:`nxp,pf1550-regulator`

* :abbr:`RNG（随机数生成器）`

   * :dtcompatible:`nordic,nrf-cracen-ctrdrbg`
   * :dtcompatible:`nxp,ele-trng`
   * :dtcompatible:`renesas,ra-sce5-rng`
   * :dtcompatible:`renesas,ra-sce7-rng`
   * :dtcompatible:`renesas,ra-sce9-rng`
   * :dtcompatible:`renesas,ra-trng`
   * :dtcompatible:`sensry,sy1xx-trng`
   * :dtcompatible:`silabs,siwx91x-rng`
   * :dtcompatible:`st,stm32-rng-noirq`

* :abbr:`RTC（实时时钟）`

   * :dtcompatible:`epson,rx8130ce-rtc`
   * :dtcompatible:`maxim,ds1337`
   * :dtcompatible:`maxim,ds3231-rtc`
   * :dtcompatible:`microcrystal,rv8803`
   * :dtcompatible:`ti,bq32002`

* SDHC

   * :dtcompatible:`renesas,ra-sdhc`

* 传感器

   * :dtcompatible:`adi,adxl366`
   * :dtcompatible:`hc-sr04`
   * :dtcompatible:`invensense,icm42370p`
   * :dtcompatible:`invensense,icm42670s`
   * :dtcompatible:`invensense,icp101xx`
   * :dtcompatible:`maxim,ds3231-sensor`
   * :dtcompatible:`melexis,mlx90394`
   * :dtcompatible:`nordic,npm2100-vbat`
   * :dtcompatible:`phosense,xbr818`
   * :dtcompatible:`renesas,hs400x`
   * :dtcompatible:`sensirion,scd40`
   * :dtcompatible:`sensirion,scd41`
   * :dtcompatible:`sensirion,sts4x`
   * :dtcompatible:`st,lis2duxs12`
   * :dtcompatible:`st,lsm6dsv16x`
   * :dtcompatible:`ti,tmag3001`
   * :dtcompatible:`ti,tmp435`
   * :dtcompatible:`we,wsen-pads-2511020213301`
   * :dtcompatible:`we,wsen-pdus-25131308XXXXX`
   * :dtcompatible:`we,wsen-tids-2521020222501`

* 串行控制器

   * :dtcompatible:`microchip,mec5-uart`
   * :dtcompatible:`realtek,rts5912-uart`
   * :dtcompatible:`renesas,rz-scif-uart`
   * :dtcompatible:`silabs,eusart-uart`
   * :dtcompatible:`silabs,usart-uart`
   * :dtcompatible:`ti,cc23x0-uart`
   * :dtcompatible:`wch,usart`

* :abbr:`SPI（串行外设接口）`

   * :dtcompatible:`ite,it8xxx2-spi`
   * :dtcompatible:`nxp,lpspi`
   * :dtcompatible:`nxp,xspi`
   * :dtcompatible:`renesas,ra-spi`

* 步进电机

   * :dtcompatible:`adi,tmc2209`
   * :dtcompatible:`ti,drv8424`

* :abbr:`TCPC（USB Type-C 端口控制器）`

   * :dtcompatible:`richtek,rt1715`

* 定时器

   * :dtcompatible:`mediatek,ostimer64`
   * :dtcompatible:`realtek,rts5912-rtmr`
   * :dtcompatible:`realtek,rts5912-slwtimer`
   * :dtcompatible:`renesas,rz-gpt`
   * :dtcompatible:`renesas,rz-gtm`
   * :dtcompatible:`riscv,machine-timer`
   * :dtcompatible:`ti,cc23x0-systim-timer`
   * :dtcompatible:`wch,systick`

* USB

   * :dtcompatible:`ambiq,usb`
   * :dtcompatible:`renesas,ra-udc`
   * :dtcompatible:`renesas,ra-usbfs`
   * :dtcompatible:`renesas,ra-usbhs`
   * :dtcompatible:`zephyr,midi2-device`

* 视频

   * :dtcompatible:`zephyr,video-emul-imager`
   * :dtcompatible:`zephyr,video-emul-rx`

* 看门狗

   * :dtcompatible:`atmel,sam4l-watchdog`
   * :dtcompatible:`nordic,npm2100-wdt`
   * :dtcompatible:`nxp,rtwdog`

* Wi-Fi

   * :dtcompatible:`infineon,airoc-wifi`
   * :dtcompatible:`silabs,siwx91x-wifi`

新示例
***********

..
  与开发板和驱动相同，此列表也将在发布时重新计算。
  只需链接示例，更多细节放在示例文档本身中。

* :zephyr:code-sample:`6dof_motion_drdy`
* :zephyr:code-sample:`ble_cs`
* :zephyr:code-sample:`bluetooth_ccp_call_control_client`
* :zephyr:code-sample:`bluetooth_ccp_call_control_server`
* :zephyr:code-sample:`coresight_stm_sample`
* :zephyr:code-sample:`usb-dfu`
* :zephyr:code-sample:`i2c-rtio-loopback`
* :zephyr:code-sample:`lvgl-screen-transparency`
* :zephyr:code-sample:`mctp_endpoint_sample`
* :zephyr:code-sample:`mctp_host_sample`
* :zephyr:code-sample:`openthread-shell`
* :zephyr:code-sample:`ot-coap`
* :zephyr:code-sample:`rtc`
* :zephyr:code-sample:`sensor_batch_processing`
* :zephyr:code-sample:`sensor_clock`
* 通用设备 FIFO 流（``stream_fifo``）
* :zephyr:code-sample:`tdk_apex`
* :zephyr:code-sample:`tmc50xx`
* :zephyr:code-sample:`uart`
* :zephyr:code-sample:`usb-midi2-device`
* :zephyr:code-sample:`usb-cdc-acm-console`
* :zephyr:code-sample:`webusb`

其他显著更改
*********************

..
  更多描述性的子系统或驱动更改。你真的想写一段话，
  还是只需链接到上面的 api/驱动/Kconfig/开发板页面就足够了？

* 已引入一个头文件用于分配 PSA Crypto API 中持久密钥的 ID 范围。
  它定义了分配给该 API 不同用户（应用程序、子系统等）的 ID 范围。
  该 API 的用户现在必须使用此头文件来构造持久密钥 ID。
  更多信息请参见 :zephyr_file:`include/zephyr/psa/key_ids.h`。（:github:`85581`）

* 已从 Twister 配置文件中移除空格分隔列表支持。
  此功能已弃用很长时间。仍在使用它们的项目可以使用
  :zephyr_file:`scripts/utils/twister_to_list.py` 脚本自动迁移 Twister 配置文件。

* Ztest 的测试用例名称现在包含 Ztest 套件名称，意味着生成的标识符
  有三个部分，看起来像：``<test_scenario_name>.<ztest_suite_name>.<ztest_name>``。
  这些扩展标识符用于日志输出、twister.json 和 testplan.json，
  以及 ``--sub-test`` 命令行参数。

* 可以使用 ``--no-detailed-test-id`` 命令行选项通过排除与父测试套件 id 相同的
  测试场景名称前缀来缩短测试用例名称。

* 为 HTTP 服务器动态资源添加了对 HTTP PUT/PATCH/DELETE 方法的支持。

* 驱动 API 结构现在可通过可迭代部分访问，并引入了新的
  :c:macro:`DEVICE_API_IS` 宏以允许检查设备是否支持
  给定 API。许多 shell 命令现在使用此功能提供"更智能"的自动补全，
  仅在预期设备参数时列出兼容的设备。

* Zephyr 的 :ref:`交互式开发板目录 <boards>` 已扩展，允许基于支持的硬件功能搜索开发板。
  新的 :rst:dir:`zephyr:board-supported-hw` Sphinx 指令现在可用于开发板的文档页面，
  以自动包含开发板支持的硬件功能列表，许多开发板已在文档中采用了此新功能。
