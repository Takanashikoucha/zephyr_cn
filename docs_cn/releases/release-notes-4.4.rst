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

.. _zephyr_4.4:

Zephyr 4.4.0
############

我们很高兴宣布 Zephyr 4.4.0 版本的发布。

本次发布的主要增强功能包括：

**OpenRISC 支持**
  Zephyr 现在支持 :zephyr:board-catalog:`OpenRISC 架构 <#arch=openrisc>`。

**工具链更新：Zephyr SDK 1.0 和 C17**
  Zephyr 4.4 是第一个支持 :ref:`Zephyr SDK 1.0 <toolchain_zephyr_sdk>` 的发布版本，
  具有升级的 GNU 工具链、实验性 Clang/LLVM 支持，以及多平台 QEMU 和 OpenOCD
  主机工具。

  Zephyr 现在默认以 C17 作为其最低要求的 C 标准版本。

**网络增强**
  Wi-Fi 管理栈现在支持 :ref:`wifi_mgmt_p2p`，允许设备发现并直接连接，
  而无需传统接入点。

  网络栈还添加了对 :zephyr:code-sample:`WireGuard VPN <wireguard-vpn>` 的支持，
  实现安全、低开销的隧道传输。

**USB 主机**
  实验性 USB 主机支持已大幅扩展，引入了新的主机类驱动框架，
  并支持在作为 USB 主机的 Zephyr 设备上使用 :abbr:`UVC（USB 视频类）` 摄像头。

**新驱动类**
  Zephyr 4.4 添加了几个新的驱动 API，包括：

  - :ref:`一次性可编程（OTP）内存设备 <otp>`，用于配置和读取永久设备数据，

  - :ref:`生物识别 API <biometrics_api>`，用于集成生物识别传感器，如指纹
    扫描仪或面部识别系统，以及

  - :ref:`唤醒控制器（WUC）API <wuc_api>`，用于管理可将系统从低功耗状态
    唤醒的唤醒源。

**Zbus 异步监听器和代理代理**
  Zbus 异步监听器通过工作队列启用非阻塞观察者回调。

  :ref:`Zbus 代理代理 <zbus_proxy_agent>` 通过 IPC 跨 CPU 和域边界
  扩展发布-订阅消息传递。

**基于压力的 CPU 频率调节**
  实验性 :ref:`CPU 频率调节 <cpu_freq>` 子系统现在包含
  :ref:`基于压力的策略 <pressure_policy>`，根据调度器负载调整 CPU 频率。

**ARM Cortex-M 上下文切换性能改进**
  新的 ARM Cortex-M 上下文切换实现，通过
  :kconfig:option:`CONFIG_USE_SWITCH` 启用，带来了显著的性能改进。

**NAND 闪存支持**
  新的闪存转换层（FTL）磁盘驱动（:dtcompatible:`zephyr,ftl-dhara`）提供磨损
  均衡和坏块管理，并使 NAND 闪存内存可作为标准磁盘设备使用。

**开发者体验改进**
  引入了几个新工具来帮助常见的开发和问题排查任务：

  - :ref:`dtdoctor` 用于帮助诊断设备树构建错误。
  - :ref:`traceconfig <kconfig_traceconfig>` 构建目标用于帮助理解 Kconfig 符号的来源
    及其最终值。
  - :ref:`交互式占用率图表 <footprint_tools_plot>` 用于可视化应用程序的 RAM/ROM 使用情况。

**扩展的板级支持**
  本次发布新增了对 120 块 :ref:`新开发板 <boards_added_in_zephyr_4_4>` 和 45 个
  :ref:`新盾牌 <shields_added_in_zephyr_4_4>` 的支持。

从 Zephyr v4.3.0 迁移到 Zephyr v4.4.0 时所需或建议的更改概述可在单独的 :ref:`迁移指南 <migration_4.4>` 中找到。

以下章节按组件提供详细的更改列表。

安全漏洞相关
******************************

本次发布解决了以下 CVE：

* :cve:`2025-12890` `蓝牙：外设：对格式错误的连接请求处理不当
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-8hrf-pfww-83v9>`_
* :cve:`2025-27809` `TLS 客户端可能无意中跳过服务器身份验证
  <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-03-1/>`_
* :cve:`2025-27810` `TLS 握手中的潜在身份验证绕过
  <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-03-2/>`_
* :cve:`2025-2962` `dns_copy_qname 中的无限循环
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-2qp5-c2vq-g2ww>`_
* :cve:`2025-52496` `AESNI 支持检测中的竞态条件
  <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-1/>`_
* :cve:`2025-52497` `解析 PEM 加密材料时的堆缓冲区下溢读取
  <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-2/>`_
* :cve:`2025-49600` `LMS 验证中未检查的返回值允许签名绕过
  <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-3/>`_
* :cve:`2025-49601` `mbedtls_lms_import_public_key() 中的越界读取
  <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-4/>`_
* :cve:`2025-49087` `带 PKCS#7 填充的分组密码解密的时序侧信道
  <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-5/>`_
* :cve:`2025-48965` `使用 mbedtls_asn1_store_named_data() 后的空指针解引用
  <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-6/>`_
* :cve:`2025-47917` `mbedtls_x509_string_to_names() 中误导性的内存管理
  <https://mbed-tls.readthedocs.io/en/latest/security-advisories/mbedtls-security-advisory-2025-06-7/>`_
* :cve:`2025-7403`：截至 2025-09-05 处于保密期

更详细的信息可在以下地址找到：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

API 更改
***********

移除的 API 和选项
========================

* 已移除 :kconfig:option:`CONFIG_I3C_USE_GROUP_ADDR` 以及对 I3C 设备组地址的支持。

* 已移除 ``--disable-unrecognized-section-test`` Twister 选项。该测试已移除，
  该选项成为默认行为。

* 已移除弃用的 ``kscan`` 子系统。

* 已移除 :dtcompatible:`meas,ms5837` 并用 :dtcompatible:`meas,ms5837-30ba`
  和 :dtcompatible:`meas,ms5837-02ba` 取代。

* 已从 :c:struct:`video_driver_api` 中移除 ``get_ctrl`` 驱动 API。

* 已移除 ``CONFIG_NET_PKT_BUF_DATA_POOL_SIZE`` 和 ``CONFIG_NET_TCP_ACK_TIMEOUT``
  网络选项。

* 已移除 :kconfig:option:`CONFIG_BT_CONN_TX_MAX` Kconfig 选项。待处理
  TX 缓冲区的数量现在与 :kconfig:option:`CONFIG_BT_BUF_ACL_TX_COUNT` Kconfig
  选项对齐。

* 已移除 :kconfig:option:`CONFIG_CRYPTO_TINYCRYPT_SHIM` Kconfig 选项。它
  自 Zephyr 4.0 起已弃用，用户被建议迁移到替代
  加密后端。

* 已移除 :kconfig:option:`CONFIG_BT_MESH_USES_TINYCRYPT` Kconfig 选项。它
  自 Zephyr 4.0 起已弃用。用户被建议使用
  :kconfig:option:`CONFIG_BT_MESH_USES_MBEDTLS_PSA` 或
  :kconfig:option:`CONFIG_BT_MESH_USES_TFM_PSA` 替代。

* 已移除 :kconfig:option:`CONFIG_NET_L2_ETHERNET` 和
  :kconfig:option:`CONFIG_NET_L2_ETHERNET_FRAME_FILTER` 选项。

弃用的 API 和选项
===========================

* 调度器 Kconfig 选项 CONFIG_SCHED_DUMB 和 CONFIG_WAITQ_DUMB 已
  重命名并弃用。请改用 :kconfig:option:`CONFIG_SCHED_SIMPLE` 和
  :kconfig:option:`CONFIG_WAITQ_SIMPLE`。

* :kconfig:option:`CONFIG_LWM2M_ENGINE_MESSAGE_HEADER_SIZE` Kconfig 选项已被移除。
  所需的头大小应包含在消息大小中，使用
  :kconfig:option:`CONFIG_LWM2M_COAP_MAX_MSG_SIZE` 配置。应特别注意确保
  使用的 CoAP 块大小（:kconfig:option:`CONFIG_LWM2M_COAP_BLOCK_SIZE`）
  能够容纳带头的给定消息大小。之前的头空间为 48 字节。

* TLS 凭据类型 ``TLS_CREDENTIAL_SERVER_CERTIFICATE`` 已重命名并
  弃用，请改用 :c:enumerator:`TLS_CREDENTIAL_PUBLIC_CERTIFICATE`。

* ``arduino_uno_r4_minima`` 和 ``arduino_uno_r4_wifi`` 板级目标已弃用，
  改为带有修订版本的新 ``arduino_uno_r4`` 板
  （``arduino_uno_r4@minima`` 和 ``arduino_uno_r4@wifi``）。

* ``esp32c6_devkitc`` 板级目标已弃用并重命名为
  ``esp32c6_devkitc/esp32c6/hpcore``。

* ``xiao_esp32c6`` 板级目标已弃用并重命名为
  ``xiao_esp32c6/esp32c6/hpcore``。

* :kconfig:option:`CONFIG_HAWKBIT_DDI_NO_SECURITY` Kconfig 选项已
  弃用，因为 hawkBit 服务器在 0.8.0 版本中已移除对匿名身份验证的支持。

* 遗留 USB 设备栈已弃用，将在 Zephyr 4.5 中移除。
  请改用新的 :ref:`USB 设备栈 <usb_device_stack_next>`。

* :kconfig:option:`CONFIG_NET_L2_ETHERNET` 已弃用。

本次发布中的稳定 API 更改
=================================

* ``net_mgmt`` 事件处理器 :c:type:`net_mgmt_event_handler_t`
  和请求处理器 :c:type:`net_mgmt_request_handler_t` 的 API 签名已更改。事件值
  类型从 ``uint32_t`` 更改为 ``uint64_t``。

新的 API 和选项
====================

..
  在此处链接新 API，如果你认为有必要可以分组，无需花哨，
  只需列出链接，其中应包含文档。如果你认为需要添加更多细节，
  请将其添加到 API 文档代码中。

* 架构

  * :kconfig:option:`CONFIG_OPENRISC`
  * :kconfig:option:`CONFIG_RISCV_ISA_RV64`
  * :kconfig:option:`CONFIG_RISCV_ISA_ZICBOM`
  * :kconfig:option:`CONFIG_RISCV_ISA_ZICBOZ`
  * :kconfig:option:`CONFIG_RISCV_ISA_ZICBOZ`

* 蓝牙

  * 音频

    * :c:macro:`BT_BAP_ADV_PARAM_CONN_QUICK`
    * :c:macro:`BT_BAP_ADV_PARAM_CONN_REDUCED`
    * :c:macro:`BT_BAP_CONN_PARAM_SHORT_7_5`
    * :c:macro:`BT_BAP_CONN_PARAM_SHORT_10`
    * :c:macro:`BT_BAP_CONN_PARAM_RELAXED`
    * :c:macro:`BT_BAP_ADV_PARAM_BROADCAST_FAST`
    * :c:macro:`BT_BAP_ADV_PARAM_BROADCAST_SLOW`
    * :c:macro:`BT_BAP_PER_ADV_PARAM_BROADCAST_FAST`
    * :c:macro:`BT_BAP_PER_ADV_PARAM_BROADCAST_SLOW`
    * :c:func:`bt_csip_set_member_set_size_and_rank`
    * :c:func:`bt_csip_set_member_get_info`
    * :c:func:`bt_bap_unicast_group_foreach_stream`
    * :c:func:`bt_cap_unicast_group_create`
    * :c:func:`bt_cap_unicast_group_reconfig`
    * :c:func:`bt_cap_unicast_group_add_streams`
    * :c:func:`bt_cap_unicast_group_delete`
    * :c:func:`bt_cap_unicast_group_foreach_stream`

  * 主机

    * :c:func:`bt_le_get_local_features`
    * :c:func:`bt_le_bond_exists`
    * :c:func:`bt_br_bond_exists`
    * :c:func:`bt_conn_lookup_addr_br`
    * :c:func:`bt_conn_get_dst_br`
    * LE 连接子评分不再是实验性的。
    * 从 :c:func:`bt_unpair` 中移除经典绑定信息的删除，并添加
      :c:func:`bt_br_unpair`。
    * 从 :c:func:`bt_foreach_bond` 中移除经典绑定信息的查询，并添加
      :c:func:`bt_br_foreach_bond`。
    * 为 :c:func:`bt_br_set_discoverable` 添加新参数 ``limited`` 以支持经典的
      有限可发现模式。
    * 为经典 L2CAP 启用重传和流量控制，包括
      :kconfig:option:`CONFIG_BT_L2CAP_RET`、:kconfig:option:`CONFIG_BT_L2CAP_FC`、
      :kconfig:option:`CONFIG_BT_L2CAP_ENH_RET` 和 :kconfig:option:`CONFIG_BT_L2CAP_STREAM`。
    * :c:func:`bt_avrcp_get_cap`
    * 改进经典免提单元，包括
      :kconfig:option:`CONFIG_BT_HFP_HF_CODEC_NEG`、:kconfig:option:`CONFIG_BT_HFP_HF_ECNR`、
      :kconfig:option:`CONFIG_BT_HFP_HF_3WAY_CALL`、:kconfig:option:`CONFIG_BT_HFP_HF_ECS`、
      :kconfig:option:`CONFIG_BT_HFP_HF_ECC`、:kconfig:option:`CONFIG_BT_HFP_HF_VOICE_RECG_TEXT`、
      :kconfig:option:`CONFIG_BT_HFP_HF_ENH_VOICE_RECG`、
      :kconfig:option:`CONFIG_BT_HFP_HF_VOICE_RECG`、
      :kconfig:option:`CONFIG_BT_HFP_HF_HF_INDICATORS`、
      :kconfig:option:`CONFIG_BT_HFP_HF_HF_INDICATOR_ENH_SAFETY` 和
      :kconfig:option:`CONFIG_BT_HFP_HF_HF_INDICATOR_BATTERY`。
    * 改进经典免提音频网关，包括
      :kconfig:option:`CONFIG_BT_HFP_AG_CODEC_NEG`、:kconfig:option:`CONFIG_BT_HFP_AG_ECNR`、
      :kconfig:option:`CONFIG_BT_HFP_AG_3WAY_CALL`、:kconfig:option:`CONFIG_BT_HFP_AG_ECS`、
      :kconfig:option:`CONFIG_BT_HFP_AG_ECC`、:kconfig:option:`CONFIG_BT_HFP_AG_VOICE_RECG_TEXT`、
      :kconfig:option:`CONFIG_BT_HFP_AG_ENH_VOICE_RECG`、
      :kconfig:option:`CONFIG_BT_HFP_AG_VOICE_TAG`、
      :kconfig:option:`CONFIG_BT_HFP_AG_HF_INDICATORS`、
      :kconfig:option:`CONFIG_BT_HFP_AG_HF_INDICATOR_ENH_SAFETY`、
      :kconfig:option:`CONFIG_BT_HFP_AG_HF_INDICATOR_BATTERY` 和
      :kconfig:option:`CONFIG_BT_HFP_AG_REJECT_CALL`。
    * 为 :c:struct:`bt_hfp_ag_cb` 添加回调函数 ``get_ongoing_call()``。
    * :c:func:`bt_hfp_ag_ongoing_calls`
    * 支持经典 L2CAP 信令回声请求和响应功能，包括
      :c:struct:`bt_l2cap_br_echo_cb`、:c:func:`bt_l2cap_br_echo_cb_register`、
      :c:func:`bt_l2cap_br_echo_cb_unregister`、:c:func:`bt_l2cap_br_echo_req` 和
      :c:func:`bt_l2cap_br_echo_rsp`。
    * :c:func:`bt_a2dp_get_conn`
    * :c:func:`bt_rfcomm_send_rpn_cmd`

* 构建系统

  * Sysbuild

    * 使用
      :kconfig:option:`SB_CONFIG_MCUBOOT_MODE_FIRMWARE_UPDATER`
      为固件加载器镜像设置/选择支持已添加到 sysbuild
      通过 ``SB_CONFIG_FIRMWARE_LOADER``，例如 :kconfig:option:`SB_CONFIG_FIRMWARE_LOADER_IMAGE_SMP_SVR`
      用于选择 :zephyr:code-sample:`smp-svr`。
    * 使用
      :kconfig:option:`SB_CONFIG_MCUBOOT_MODE_SINGLE_APP_RAM_LOAD`
      为 sysbuild 添加单应用 RAM 加载支持。

* 计数器

  * :c:func:`counter_reset`

* 调试

  * 核心转储

    * :kconfig:option:`CONFIG_DEBUG_COREDUMP_THREAD_STACK_TOP`，当选择 :kconfig:option:`CONFIG_DEBUG_COREDUMP_MEMORY_DUMP_MIN` 时为 ARM Cortex M 默认启用。
    * :kconfig:option:`CONFIG_DEBUG_COREDUMP_BACKEND_IN_MEMORY`
    * :kconfig:option:`CONFIG_DEBUG_COREDUMP_BACKEND_IN_MEMORY_SIZE`

* 显示

    * 添加了 :c:func:`display_clear` API 以允许以标准化方式清除显示内容。
    * 字符帧缓冲（CFB）子系统现在支持通过 :c:func:`cfb_draw_circle` 绘制圆形。

* I2C

  * :c:func:`i2c_configure_dt`。
  * :c:macro:`I2C_DEVICE_DT_DEINIT_DEFINE`
  * :c:macro:`I2C_DEVICE_DT_INST_DEINIT_DEFINE`

* I3C

  * :kconfig:option:`CONFIG_I3C_MODE`
  * :kconfig:option:`CONFIG_I3C_CONTROLLER_ROLE_ONLY`
  * :kconfig:option:`CONFIG_I3C_TARGET_ROLE_ONLY`
  * :kconfig:option:`CONFIG_I3C_DUAL_ROLE`
  * :c:func:`i3c_ccc_do_rstdaa`

* 内核

  * :c:macro:`K_TIMEOUT_ABS_SEC`
  * :c:func:`timespec_add`
  * :c:func:`timespec_compare`
  * :c:func:`timespec_equal`
  * :c:func:`timespec_is_valid`
  * :c:func:`timespec_negate`
  * :c:func:`timespec_normalize`
  * :c:func:`timespec_from_timeout`
  * :c:func:`timespec_to_timeout`
  * :c:func:`k_heap_array_get`

* LVGL（Light and Versatile Graphics Library）

    * LVGL 模块已同步到 v9.3，带来了许多上游改进和新功能。
    * LVGL 子系统现在支持多个同时显示，包括正确的输入设备到显示绑定。
    * 为 SSD1327、SSD1320、SSD1322 和 ST75256 等显示添加了 L8/Y8 像素格式支持。
    * :kconfig:option:`CONFIG_LV_Z_COLOR_MONO_HW_INVERSION`

* LoRaWAN

   * :c:func:`lorawan_request_link_check`

* 管理

  * MCUmgr

    * 使用
      :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_MODE_FIRMWARE_UPDATER`
      为镜像管理组添加固件加载器支持。
    * 使用
      :kconfig:option:`CONFIG_MCUMGR_GRP_OS_RESET_BOOT_MODE`
      为 OS 组重置命令添加可选启动模式（使用保留启动模式）。

* 网络：

  * CoAP

    * :c:macro:`COAPS_SERVICE_DEFINE`

  * DHCPv4

    * :kconfig:option:`CONFIG_NET_DHCPV4_INIT_REBOOT`

  * DNS

    * :c:func:`dns_resolve_service`
    * :c:func:`dns_resolve_reconfigure_with_interfaces`

  * HTTP

    * :kconfig:option:`CONFIG_HTTP_SERVER_COMPRESSION`

  * IPv4

    * :kconfig:option:`CONFIG_NET_IPV4_MTU`

  * LwM2M

    * :kconfig:option:`CONFIG_LWM2M_SERVER_BOOTSTRAP_ON_FAIL`
    * 实现了大于、小于和步进观察属性处理
      （参见 :kconfig:option:`CONFIG_LWM2M_MAX_NOTIFIED_NUMERICAL_RES_TRACKED`）。

  * 杂项

    * :c:func:`net_if_oper_state_change_time`

  * MQTT

    * :kconfig:option:`CONFIG_MQTT_VERSION_5_0`
    * :c:member:`mqtt_transport.if_name`

  * OpenThread

    * 将 OpenThread 相关 Kconfig 选项从 :zephyr_file:`subsys/net/l2/openthread/Kconfig`
      移动到 :zephyr_file:`modules/openthread/Kconfig`。
    * 重构了 OpenThread 网络 API，参见
      :ref:`迁移指南 <migration_4.4>` 的 OpenThread 部分。
    * :kconfig:option:`CONFIG_OPENTHREAD_SYS_INIT`
    * :kconfig:option:`CONFIG_OPENTHREAD_SYS_INIT_PRIORITY`

  * SNTP

    * :c:func:`sntp_init_async`
    * :c:func:`sntp_send_async`
    * :c:func:`sntp_read_async`
    * :c:func:`sntp_close_async`

  * 套接字

    * :kconfig:option:`CONFIG_NET_SOCKETS_INET_RAW`
    * :c:func:`socket_offload_dns_enable`
    * 为 :ref:`socket_service_interface` 库添加了新的文档页面。
    * 新的套接字选项：

      * :c:macro:`IP_MULTICAST_LOOP`
      * :c:macro:`IPV6_MULTICAST_LOOP`
      * :c:macro:`TLS_CERT_VERIFY_RESULT`

  * Wi-Fi

    * :kconfig:option:`CONFIG_WIFI_USAGE_MODE`
    * 在 Wi-Fi 管理文档中添加了新的部分
      （``doc/connectivity/networking/api/wifi.rst``），包含使用 FreeRADIUS 脚本
      为 Wi-Fi 生成测试证书的逐步说明。这有助于用户在自己的测试环境中
      复现该过程。
    * 将 hostap IPC 机制从 socketpair 更改为 k_fifo。根据启用的 Wi-Fi 配置选项，
      使用原生 Wi-Fi 栈时最多可节省 6-8 kB 内存。

  * zperf

    * :kconfig:option:`CONFIG_ZPERF_SESSION_PER_THREAD`
    * :c:member:`zperf_upload_params.data_loader`
    * :kconfig:option:`CONFIG_NET_ZPERF_SERVER`

* PCIe

   * :kconfig:option:`CONFIG_NVME_PRP_PAGE_SIZE`

* 电源管理

    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_USE_SYSTEM_WQ`
    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_USE_DEDICATED_WQ`
    * :kconfig:option:`CONFIG_PM_DEVICE_DRIVER_NEEDS_DEDICATED_WQ`
    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEDICATED_WQ_STACK_SIZE`
    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEDICATED_WQ_PRIO`
    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEDICATED_WQ_INIT_PRIO`
    * :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_ASYNC`

* SPI

  * :c:macro:`SPI_DEVICE_DT_DEINIT_DEFINE`
  * :c:macro:`SPI_DEVICE_DT_INST_DEINIT_DEFINE`

* 传感器

  * :c:func:`sensor_value_to_deci`
  * :c:func:`sensor_value_to_centi`

* 步进电机

  * :c:func:`stepper_stop()`

* 存储

  * :c:func:`flash_area_copy()`

* Sys

  * :c:func:`util_eq`
  * :c:func:`util_memeq`
  * :c:func:`sys_clock_gettime`
  * :c:func:`sys_clock_settime`
  * :c:func:`sys_clock_nanosleep`

* USB

  * :c:func:`uvc_set_video_dev`

* UpdateHub

  * :c:func:`updatehub_report_error`

* 视频

  * :c:type:`video_api_ctrl_t`
  * :c:func:`video_query_ctrl`
  * :c:func:`video_print_ctrl`
  * :c:type:`video_api_selection_t`
  * :c:func:`video_set_selection`
  * :c:func:`video_get_selection`
  * :ref:`video-sw-generator <snippet-video-sw-generator>`
  * :c:func:`video_get_csi_link_freq`
  * :c:macro:`VIDEO_CID_LINK_FREQ`
  * :c:macro:`VIDEO_CID_AUTO_WHITE_BALANCE` 以及 BASE 控制类的其他控制。
  * :c:macro:`VIDEO_CID_EXPOSURE_ABSOLUTE` 以及 CAMERA 控制类的其他控制。
  * :c:macro:`VIDEO_PIX_FMT_Y10` 和 ``Y12``、``Y14``、``Y16`` 变体
  * :c:macro:`VIDEO_PIX_FMT_SRGGB10P` 和 ``12P``、``14P`` 变体，适用于所有 4 种 bayer 变体。
  * :c:member:`video_buffer.index` 字段
  * :c:member:`video_ctrl_query.int_menu` 字段
  * :c:macro:`VIDEO_MIPI_CSI2_DT_NULL` 和其他 MIPI 标准值

* ZBus

  * Zbus 随着 API 版本 v1.0.0 的发布而达到稳定状态。
  * 运行时观察者现在可以在无堆的情况下工作。现在可以在静态、动态
    和无分配之间为运行时观察者节点进行选择。
  * 使用 :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_NONE` 的运行时观察者必须使用
    新函数 :c:func:`zbus_chan_add_obs_with_node`。

  * :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_DYNAMIC`
  * :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_STATIC`
  * :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_ALLOC_NONE`
  * :kconfig:option:`CONFIG_ZBUS_RUNTIME_OBSERVERS_NODE_POOL_SIZE`

.. _boards_added_in_zephyr_4_4:

新开发板
**********

..
  你可以在发布周期中贡献新开发板时更新此列表，以便让可能正在查看发布说明工作草稿的人看到。
  但请注意，此列表将在发布时重新计算，因此你*不必*更新它。
  无论如何，只需链接开发板，更多细节放在开发板描述中。

* Adafruit Industries, LLC

   * :zephyr:board:`adafruit_feather_esp32s2`（``adafruit_feather_esp32s2``）
   * :zephyr:board:`adafruit_feather_esp32s2_tft`（``adafruit_feather_esp32s2_tft``）
   * :zephyr:board:`adafruit_feather_esp32s2_tft_reverse`（``adafruit_feather_esp32s2_tft_reverse``）
   * :zephyr:board:`adafruit_feather_esp32s3`（``adafruit_feather_esp32s3``）
   * :zephyr:board:`adafruit_feather_esp32s3_tft`（``adafruit_feather_esp32s3_tft``）
   * :zephyr:board:`adafruit_feather_esp32s3_tft_reverse`（``adafruit_feather_esp32s3_tft_reverse``）

* Advanced Micro Devices (AMD), Inc.

   * :zephyr:board:`versal2_rpu`（``versal2_rpu``）
   * :zephyr:board:`versalnet_rpu`（``versalnet_rpu``）

* Aesc Silicon

   * :zephyr:board:`elemrv_flask_n`（``elemrv``）

* Ai-Thinker Co., Ltd.

   * :zephyr:board:`ai_wb2_12f_kit`（``ai_wb2_12f_kit``）

* Ambiq Micro, Inc.

   * :zephyr:board:`apollo510_evb`（``apollo510_evb``）

* Analog Devices, Inc.

   * :zephyr:board:`max32657evkit`（``max32657evkit``）

* Arduino

   * :zephyr:board:`arduino_nano_matter`（``arduino_nano_matter``）
   * :zephyr:board:`arduino_portenta_c33`（``arduino_portenta_c33``）

* ARM Ltd.

   * :zephyr:board:`mps4`（``mps4``）

* BeagleBoard.org Foundation

   * :zephyr:board:`pocketbeagle_2`（``pocketbeagle_2``）

* Blues Wireless

   * :zephyr:board:`cygnet`（``cygnet``）

* Bouffalo Lab (Nanjing) Co., Ltd.

   * :zephyr:board:`bl604e_iot_dvk`（``bl604e_iot_dvk``）

* Doctors of Intelligence & Technology

   * :zephyr:board:`dt_bl10_devkit`（``dt_bl10_devkit``）

* ENE Technology, Inc.

   * :zephyr:board:`kb1062_evb`（``kb1062_evb``）

* Espressif Systems

   * :zephyr:board:`esp32_devkitc`（``esp32_devkitc``）

* Ezurio

   * :zephyr:board:`bl54l15_dvk`（``bl54l15_dvk``）
   * ``bl54l15u_dvk``

* FANKE Technology Co., Ltd.

   * :zephyr:board:`fk743m5_xih6`（``fk743m5_xih6``）

* IAR Systems AB

   * :zephyr:board:`stm32f429ii_aca`（``stm32f429ii_aca``）

* Infineon Technologies

   * :zephyr:board:`kit_xmc72_evk`（``kit_xmc72_evk``）

* Intel Corporation

   * :zephyr:board:`intel_btl_s_crb`（``intel_btl_s_crb``）

* ITE Tech. Inc.

   * ``it515xx_evb``

* KWS Computersysteme Gmbh

   * :zephyr:board:`pico2_spe`（``pico2_spe``）
   * :zephyr:board:`pico_spe`（``pico_spe``）

* Lilygo Shenzhen Xinyuan Electronic Technology Co., Ltd

   * :zephyr:board:`tdongle_s3`（``tdongle_s3``）
   * :zephyr:board:`ttgo_tbeam`（``ttgo_tbeam``）
   * :zephyr:board:`ttgo_toiplus`（``ttgo_toiplus``）
   * :zephyr:board:`twatch_s3`（``twatch_s3``）

* M5Stack

   * :zephyr:board:`m5stack_fire`（``m5stack_fire``）

* Microchip Technology Inc.

   * :zephyr:board:`mec_assy6941`（``mec_assy6941``）
   * :zephyr:board:`sama7g54_ek`（``sama7g54_ek``）

* MikroElektronika d.o.o.

   * :zephyr:board:`mikroe_quail`（``mikroe_quail``）

* Nordic Semiconductor

   * :zephyr:board:`nrf54lm20dk`（``nrf54lm20dk``）

* Nuvoton Technology Corporation

   * :zephyr:board:`npck3m8k_evb`（``npck3m8k_evb``）
   * :zephyr:board:`numaker_m55m1`（``numaker_m55m1``）

* NXP Semiconductors

   * :zephyr:board:`frdm_mcxa153`（``frdm_mcxa153``）
   * :zephyr:board:`imx943_evk`（``imx943_evk``）
   * :zephyr:board:`mcx_n9xx_evk`（``mcx_n9xx_evk``）
   * :zephyr:board:`s32k148_evb`（``s32k148_evb``）

* Octavo Systems LLC

   * :zephyr:board:`osd32mp1_brk`（``osd32mp1_brk``）

* OpenHW Group

   * :zephyr:board:`cv32a6_genesys_2`（``cv32a6_genesys_2``）
   * :zephyr:board:`cv64a6_genesys_2`（``cv64a6_genesys_2``）

* Pimoroni Ltd.

   * :zephyr:board:`pico_plus2`（``pico_plus2``）

* QEMU

   * :zephyr:board:`qemu_rx`（``qemu_rx``）

* Raytac Corporation

   * :zephyr:board:`raytac_an54lq_db_15`（``raytac_an54lq_db_15``）
   * :zephyr:board:`raytac_an7002q_db`（``raytac_an7002q_db``）
   * :zephyr:board:`raytac_mdbt50q_cx_40_dongle`（``raytac_mdbt50q_cx_40_dongle``）

* Renesas Electronics Corporation

   * :zephyr:board:`ek_ra8p1`（``ek_ra8p1``）
   * :zephyr:board:`rsk_rx130`（``rsk_rx130``）
   * :zephyr:board:`rza2m_evk`（``rza2m_evk``）
   * :zephyr:board:`rza3ul_smarc`（``rza3ul_smarc``）
   * :zephyr:board:`rzg2l_smarc`（``rzg2l_smarc``）
   * :zephyr:board:`rzg2lc_smarc`（``rzg2lc_smarc``）
   * :zephyr:board:`rzg2ul_smarc`（``rzg2ul_smarc``）
   * :zephyr:board:`rzn2l_rsk`（``rzn2l_rsk``）
   * :zephyr:board:`rzt2l_rsk`（``rzt2l_rsk``）
   * :zephyr:board:`rzt2m_rsk`（``rzt2m_rsk``）
   * :zephyr:board:`rzv2h_evk`（``rzv2h_evk``）
   * :zephyr:board:`rzv2l_smarc`（``rzv2l_smarc``）
   * :zephyr:board:`rzv2n_evk`（``rzv2n_evk``）

* Seeed Technology Co., Ltd

   * :zephyr:board:`xiao_mg24`（``xiao_mg24``）
   * :zephyr:board:`xiao_ra4m1`（``xiao_ra4m1``）

* sensry.io

   * :zephyr:board:`ganymed_sk`（``ganymed_sk``）

* Shanghai Ruiside Electronic Technology Co., Ltd.

   * :zephyr:board:`art_pi2`（``art_pi2``）
   * :zephyr:board:`ra8d1_vision_board`（``ra8d1_vision_board``）

* Silicon Laboratories

   * :zephyr:board:`siwx917_rb4342a`（``siwx917_rb4342a``）
   * :zephyr:board:`slwrb4180b`（``slwrb4180b``）

* Space Cubics, LLC

   * :zephyr:board:`scobc_a1`（``scobc_a1``）

* STMicroelectronics

   * :zephyr:board:`nucleo_f439zi`（``nucleo_f439zi``）
   * :zephyr:board:`nucleo_u385rg_q`（``nucleo_u385rg_q``）
   * :zephyr:board:`nucleo_wba65ri`（``nucleo_wba65ri``）
   * :zephyr:board:`stm32h757i_eval`（``stm32h757i_eval``）
   * :zephyr:board:`stm32mp135f_dk`（``stm32mp135f_dk``）
   * :zephyr:board:`stm32mp257f_ev1`（``stm32mp257f_ev1``）
   * :zephyr:board:`stm32u5g9j_dk1`（``stm32u5g9j_dk1``）
   * :zephyr:board:`stm32u5g9j_dk2`（``stm32u5g9j_dk2``）

* Texas Instruments

   * :zephyr:board:`am243x_evm`（``am243x_evm``）
   * :zephyr:board:`lp_mspm0g3507`（``lp_mspm0g3507``）
   * :zephyr:board:`sk_am64`（``sk_am64``）

* u-blox

   * :zephyr:board:`ubx_evk_iris_w1`（``ubx_evk_iris_w1``）

* Variscite Ltd.

   * :zephyr:board:`imx8mp_var_dart`（``imx8mp_var_dart``）
   * :zephyr:board:`imx8mp_var_som`（``imx8mp_var_som``）
   * :zephyr:board:`imx93_var_dart`（``imx93_var_dart``）
   * :zephyr:board:`imx93_var_som`（``imx93_var_som``）

* Waveshare Electronics

   * :zephyr:board:`esp32s3_matrix`（``esp32s3_matrix``）
   * :zephyr:board:`rp2040_plus`（``rp2040_plus``）

* WeAct Studio

   * :zephyr:board:`bluepillplus_ch32v203`（``bluepillplus_ch32v203``）
   * :zephyr:board:`weact_stm32f446_core`（``weact_stm32f446_core``）

* WinChipHead

   * :zephyr:board:`ch32v003f4p6_dev_board`（``ch32v003f4p6_dev_board``）
   * :zephyr:board:`ch32v006evt`（``ch32v006evt``）
   * :zephyr:board:`ch32v303vct6_evt`（``ch32v303vct6_evt``）
   * :zephyr:board:`linkw`（``linkw``）

* WIZnet Co., Ltd.

   * :zephyr:board:`w5500_evb_pico2`（``w5500_evb_pico2``）

* Würth Elektronik GmbH.

   * :zephyr:board:`ophelia4ev`（``ophelia4ev``）

.. _shields_added_in_zephyr_4_4:

新盾牌
=============

* :ref:`Arduino Giga 显示盾牌 <arduino_giga_display_shield>`
* :ref:`Arduino Modulino 按钮 <arduino_modulino_buttons>`
* :ref:`Arduino Modulino 智能 LED <arduino_modulino_pixels>`
* :ref:`DVP 20 针 OV7670 <dvp_20pin_ov7670>`
* :ref:`EVAL AD4052 ARDZ <eval_ad4052_ardz>`
* :ref:`EVAL ADXL367 ARDZ <eval_adxl367_ardz>`
* :ref:`M5Stack Cardputer <m5stack_cardputer>`
* :ref:`MikroElektronika LTE IoT10 Click <mikroe_lte_iot10_click_shield>`
* :ref:`MikroElektronika 步进 18 Click <mikroe_stepper_18_click_shield>`
* :ref:`MikroElektronika 步进 19 Click <mikroe_stepper_19_click_shield>`
* :ref:`NPM2100 评估套件 <npm2100_ek>`
* :ref:`NXP ADTJA1101 <nxp_adtja1101>`
* :ref:`NXP M2 WiFi BT <nxp_m2_wifi_bt>`
* :ref:`OpenThread RCP Arduino <openthread_rcp_arduino_shield>`
* :ref:`RTK7 EKA6M3B00001BU <rtk7eka6m3b00001bu>`
* :ref:`RTKLCDPAR1S00001BE 显示屏 <rtklcdpar1s00001be>`
* :ref:`ST B-CAMS-IMX-MB1854 <st_b_cams_imx_mb1854>`
* :ref:`ST MB1897 摄像头模块 <st_mb1897_cam>`
* :ref:`ST STM32F4DIS CAM <st_stm32f4dis_cam>`
* :ref:`Waveshare Pico LCD 1.14 <waveshare_pico_lcd_1_14>`
* :ref:`Waveshare Pico OLED 1.3 <waveshare_pico_oled_1_3>`
* :ref:`X-Nucleo-GFX01M2 <x_nucleo_gfx01m2_shield>`

新驱动
***********

..
  与开发板相同，此列表也将在发布时重新计算。
  只需链接驱动，更多细节放在绑定描述中

* :abbr:`ADC（模数转换器）`

   * :dtcompatible:`adi,ad4050-adc` (:github:`97309`)
   * :dtcompatible:`adi,ad4052-adc` (:github:`97309`)
   * :dtcompatible:`adi,ad4130-adc` (:github:`97309`)
   * :dtcompatible:`ene,kb106x-adc` (:github:`100875`)
   * :dtcompatible:`ite,it51xxx-adc` (:github:`100875`)
   * :dtcompatible:`microchip,mcp356xr` (:github:`105389`)
   * :dtcompatible:`realtek,rts5912-adc` (:github:`100875`)
   * :dtcompatible:`renesas,rz-adc` (:github:`100934`)
   * :dtcompatible:`silabs,siwx91x-adc` (:github:`104471`)
   * :dtcompatible:`ti,am335x-adc` (:github:`105389`)
   * :dtcompatible:`ti,cc23x0-adc` (:github:`105389`)
   * :dtcompatible:`wch,adc` (:github:`101390`)

* 音频

   * :dtcompatible:`ambiq,pdm` (:github:`97309`)
   * :dtcompatible:`maxim,max98091` (:github:`105389`)
   * :dtcompatible:`ti,pcm1681` (:github:`105389`)
   * :dtcompatible:`ti,tlv320aic3110` (:github:`105389`)
   * :dtcompatible:`wolfson,wm8962` (:github:`105389`)

* 辅助显示

   * :dtcompatible:`gpio-7-segment` (:github:`100306`)

* :abbr:`CAN（控制器局域网）`

   * :dtcompatible:`adi,max32-can` (:github:`97309`)
   * :dtcompatible:`renesas,rz-canfd` (:github:`100934`)
   * :dtcompatible:`renesas,rz-canfd-global` (:github:`100934`)

* 充电器

   * :dtcompatible:`ti,bq25713` (:github:`105389`)
   * :dtcompatible:`x-powers,axp2101-charger` (:github:`105389`)

* 时钟控制

   * :dtcompatible:`bflb,bclk` (:github:`104349`)
   * :dtcompatible:`bflb,bl60x-clock-controller` (:github:`104349`)
   * :dtcompatible:`bflb,bl60x-pll` (:github:`104349`)
   * :dtcompatible:`bflb,bl60x-root-clk` (:github:`104349`)
   * :dtcompatible:`bflb,clock-controller` (:github:`104349`)
   * :dtcompatible:`ite,it51xxx-ecpm` (:github:`100875`)
   * :dtcompatible:`microchip,sam-pmc` (:github:`105389`)
   * :dtcompatible:`microchip,sama7g5-sckc` (:github:`105389`)
   * :dtcompatible:`nordic,nrf51-hfxo` (:github:`104471`)
   * :dtcompatible:`nordic,nrf52-hfxo` (:github:`104471`)
   * :dtcompatible:`nordic,nrf54l-hfxo` (:github:`104471`)
   * :dtcompatible:`nordic,nrfs-audiopll` (:github:`104471`)
   * :dtcompatible:`renesas,rx-cgc-pclk` (:github:`100934`)
   * :dtcompatible:`renesas,rx-cgc-pclk-block` (:github:`100934`)
   * :dtcompatible:`renesas,rx-cgc-pll` (:github:`100934`)
   * :dtcompatible:`renesas,rx-cgc-root-clock` (:github:`100934`)
   * :dtcompatible:`renesas,rza2m-cpg` (:github:`100934`)
   * :dtcompatible:`st,stm32mp13-cpu-clock-mux` (:github:`96134`)
   * :dtcompatible:`st,stm32mp13-pll-clock` (:github:`96134`)
   * :dtcompatible:`st,stm32mp2-rcc` (:github:`96134`)
   * :dtcompatible:`st,stm32u3-msi-clock` (:github:`96134`)
   * :dtcompatible:`ti,mspm0-clk` (:github:`105389`)
   * :dtcompatible:`ti,mspm0-osc` (:github:`105389`)
   * :dtcompatible:`ti,mspm0-pll` (:github:`105389`)
   * :dtcompatible:`wch,ch32v20x_30x-pll-clock` (:github:`101390`)

* 比较器

   * :dtcompatible:`ite,it51xxx-vcmp` (:github:`100875`)
   * :dtcompatible:`renesas,ra-acmphs` (:github:`100934`)
   * :dtcompatible:`renesas,ra-acmphs-global` (:github:`100934`)

* 计数器

   * :dtcompatible:`adi,max32-wut` (:github:`97309`)
   * :dtcompatible:`espressif,esp32-counter` (:github:`105389`)
   * :dtcompatible:`ite,it51xxx-counter` (:github:`100875`)
   * :dtcompatible:`ite,it8xxx2-counter` (:github:`100875`)
   * :dtcompatible:`neorv32,gptmr` (:github:`105006`)
   * :dtcompatible:`realtek,rts5912-timer` (:github:`100875`)
   * :dtcompatible:`ti,cc23x0-lgpt` (:github:`105389`)
   * :dtcompatible:`ti,cc23x0-rtc` (:github:`105389`)
   * :dtcompatible:`ti,mspm0-timer-counter` (:github:`105389`)
   * :dtcompatible:`wch,gptm` (:github:`101390`)
   * :dtcompatible:`zephyr,native-sim-counter` (:github:`100306`)

* CPU

   * :dtcompatible:`adi,max32-rv32` (:github:`97309`)
   * :dtcompatible:`arm,cortex-a320` (:github:`96852`)
   * :dtcompatible:`arm,cortex-a510` (:github:`96852`)
   * :dtcompatible:`arm,cortex-a7` (:github:`101582`)
   * :dtcompatible:`arm,cortex-a9` (:github:`101582`)
   * :dtcompatible:`cdns,swerv,s400` (:github:`102288`)
   * :dtcompatible:`cdns,swerv,s420` (:github:`102288`)
   * :dtcompatible:`intel,wildcat-lake` (:github:`99205`)
   * :dtcompatible:`riscv` (:github:`105006`)
   * :dtcompatible:`spinalhdl,vexriscv` (:github:`97925`)

* :abbr:`CRC（循环冗余校验）`

   * :dtcompatible:`nxp,crc` (:github:`100875`)
   * :dtcompatible:`nxp,lpc-crc` (:github:`101528`)
   * :dtcompatible:`sifli,sf32lb-crc` (:github:`98997`)
   * :dtcompatible:`silabs,gpcrc` (:github:`104471`)
   * :dtcompatible:`st,stm32-crc` (:github:`105302`)

* 加密加速器

   * :dtcompatible:`bflb,sec-eng-aes` (:github:`104371`)
   * :dtcompatible:`bflb,sec-eng-sha` (:github:`104371`)
   * :dtcompatible:`bflb,sec-eng-trng` (:github:`104349`)
   * :dtcompatible:`microchip,aes-g1` (:github:`105389`)
   * :dtcompatible:`microchip,sha-g1-crypto` (:github:`98894`)
   * :dtcompatible:`nxp,s32-crypto-hse-mu` (:github:`79351`)
   * :dtcompatible:`raspberrypi,pico-sha256` (:github:`85036`)
   * :dtcompatible:`sifli,sf32lb-crypto` (:github:`100583`)

* :abbr:`DAC（数模转换器）`

   * :dtcompatible:`microchip,dac-g1` (:github:`101431`)
   * :dtcompatible:`nxp,hpdac` (:github:`104642`)
   * :dtcompatible:`ti,dac5311` (:github:`90811`)
   * :dtcompatible:`ti,dac6311` (:github:`90811`)
   * :dtcompatible:`ti,dac7311` (:github:`90811`)
   * :dtcompatible:`ti,dac8311` (:github:`90811`)
   * :dtcompatible:`ti,dac8411` (:github:`90811`)
   * :dtcompatible:`zephyr,dac-emul` (:github:`100306`)

* 磁盘

   * :dtcompatible:`zephyr,ftl-dhara` (:github:`100858`)

* 显示

   * :dtcompatible:`eink,ac057tc1` (:github:`104142`)
   * :dtcompatible:`ilitek,ili9163c` (:github:`104071`)
   * :dtcompatible:`nxp,imx-lcdifv2` (:github:`103646`)
   * :dtcompatible:`qemu,ramfb` (:github:`103887`)
   * :dtcompatible:`sifli,sf32lb-lcdc` (:github:`99549`)
   * :dtcompatible:`sitronix,st7586s` (:github:`103296`)
   * :dtcompatible:`solomon,ssd1325` (:github:`102128`)
   * :dtcompatible:`waveshare,dsi2dpi` (:github:`100140`)

* :abbr:`DMA（直接内存访问）`

   * :dtcompatible:`infineon,dmac` (:github:`101583`)
   * :dtcompatible:`microchip,dmac-g1-dma` (:github:`96300`)
   * :dtcompatible:`microchip,dmac-g2-dma` (:github:`104404`)
   * :dtcompatible:`nxp,4ch-dma` (:github:`97841`)

* :abbr:`EDAC（错误检测与纠正）`

   * :dtcompatible:`nxp,eim` (:github:`94111`)
   * :dtcompatible:`nxp,erm` (:github:`94111`)

* 以太网

   * :dtcompatible:`davicom,dm9051` (:github:`104715`)
   * :dtcompatible:`ethernet-phy-fixed-link` (:github:`100454`)
   * :dtcompatible:`maxlinear,gpy111` (:github:`100995`)
   * :dtcompatible:`microchip,lan8742` (:github:`96134`)
   * :dtcompatible:`motorcomm,yt8521` (:github:`97535`)
   * :dtcompatible:`motorcomm,yt8531` (:github:`104945`)
   * :dtcompatible:`nxp,t1s-phy` (:github:`105033`)
   * :dtcompatible:`renesas,ra-eswm` (:github:`100995`)
   * :dtcompatible:`renesas,ra-ethernet-rmac` (:github:`100995`)
   * :dtcompatible:`renesas,ra-mdio-rmac` (:github:`100995`)
   * :dtcompatible:`st,stm32h5-ethernet` (:github:`100910`)
   * :dtcompatible:`st,stm32mp13-ethernet` (:github:`96134`)
   * :dtcompatible:`wch,ethernet` (:github:`101390`)
   * :dtcompatible:`wch,ethernet-controller` (:github:`101390`)
   * :dtcompatible:`wch,mdio` (:github:`101390`)
   * :dtcompatible:`wiznet,w6100` (:github:`101753`)
   * :dtcompatible:`xlnx,xps-ethernetlite-1.00.a` (:github:`95073`)
   * :dtcompatible:`xlnx,xps-ethernetlite-1.00.a-mac` (:github:`95073`)
   * :dtcompatible:`xlnx,xps-ethernetlite-1.00.a-mdio` (:github:`103944`)
   * :dtcompatible:`xlnx,xps-ethernetlite-3.00.a` (:github:`95073`)
   * :dtcompatible:`xlnx,xps-ethernetlite-3.00.a-mac` (:github:`95073`)
   * :dtcompatible:`xlnx,xps-ethernetlite-3.00.a-mdio` (:github:`103944`)

新示例
***********

..
  与开发板和驱动相同，此列表也将在发布时重新计算。
  只需链接示例，更多细节放在示例文档本身中。

* :zephyr:code-sample:`amp_audio_loopback`
* :zephyr:code-sample:`amp_audio_output`
* :zephyr:code-sample:`amp_blinky`
* :zephyr:code-sample:`amp_mbox`
* :zephyr:code-sample:`auxdisplay_digits`
* :zephyr:code-sample:`bmg160`
* :zephyr:code-sample:`debug-ulp`
* :zephyr:code-sample:`distance_polling`
* :zephyr:code-sample:`echo-ulp`
* :zephyr:code-sample:`fatfs-fstab`
* :zephyr:code-sample:`fuel_gauge`
* :zephyr:code-sample:`heart_rate`
* :zephyr:code-sample:`interrupt-ulp`
* :zephyr:code-sample:`light_sensor_polling`
* :zephyr:code-sample:`lvgl-multi-display`
* :zephyr:code-sample:`min-heap`
* :zephyr:code-sample:`mspi-timing-scan`
* :zephyr:code-sample:`net-pkt-filter`
* :zephyr:code-sample:`nrf_ironside_update`
* :zephyr:code-sample:`paj7620_gesture`
* :zephyr:code-sample:`pressure_interrupt`
* :zephyr:code-sample:`pressure_polling`
* :zephyr:code-sample:`psi5`
* :zephyr:code-sample:`renesas-elc`
* :zephyr:code-sample:`renesas_comparator`
* :zephyr:code-sample:`rz-openamp-linux-zephyr`
* :zephyr:code-sample:`sent`
* :zephyr:code-sample:`spis-wakeup`
* :zephyr:code-sample:`stepper`
* :zephyr:code-sample:`stream_drdy`
* :zephyr:code-sample:`uart_async`
* :zephyr:code-sample:`usb-cdc-acm-bridge`
* :zephyr:code-sample:`uuid`
* :zephyr:code-sample:`uvc`
* :zephyr:code-sample:`veml6031`

设备树
**********

* 迁移指南：:ref:`migration_4.4_devicetree`

* 用于 reg 属性迭代的新宏（:github:`104223`）

  * :c:macro:`DT_FOREACH_REG`
  * :c:macro:`DT_FOREACH_REG_SEP`
  * :c:macro:`DT_FOREACH_REG_VARGS`
  * :c:macro:`DT_FOREACH_REG_SEP_VARGS`
  * 每个宏的实例编号变体，例如 :c:macro:`DT_INST_FOREACH_REG`

* ``*-map`` 相关属性的定义（:github:`87595`）
  为 nexus 节点和说明符映射提供一级支持。
  有关这些属性的更多细节，请参见设备树规范 v0.4 第 2.5 节。

* 新的 :dtcompatible:`zephyr,mapped-partition` 绑定及相关的
  内存映射闪存分区 API。这是现有
  :dtcompatible:`fixed-partitions` 绑定的继任者

* 绑定不再允许为 ``status``、``#address-cells`` 和
  ``#size-cells`` 属性指定任何默认值。

* :c:macro:`DT_CHILD_BY_UNIT_ADDR_INT`

* :c:macro:`DT_INST_CHILD_BY_UNIT_ADDR_INT`

Kconfig
*******

* 添加了新的预处理器函数 ``dt_highest_controller_irq_number``（:github:`104819`）

内核
******

* 移除了在 Zephyr 4.2.0 中已弃用的 CONFIG_SCHED_DUMB 和
  CONFIG_WAITQ_DUMB 选项

* 通过 :kconfig:option:`CONFIG_SYS_HEAP_HARDENING` 添加了分层堆强化
  （Basic、Moderate、Full、Extreme），为 :c:func:`sys_heap_alloc` 和
  :c:func:`sys_heap_free` 提供渐进级别的运行时损坏检测，
  包括双重释放检测、邻居一致性检查，以及可选的
  每块金丝雀（:github:`104999`）。

* :ref:`cleanup_api`

  * :c:macro:`SCOPE_VAR_DEFINE`
  * :c:macro:`SCOPE_GUARD_DEFINE`
  * :c:macro:`SCOPE_DEFER_DEFINE`
  * :c:macro:`scope_var`
  * :c:macro:`scope_var_init`
  * :c:macro:`scope_guard`
  * :c:macro:`scope_defer`

库 / 子系统
**********************

* LoRa/LoRaWAN

   * :c:func:`lora_airtime`
   * 为 LoRa API 添加了信道活动检测（CAD）支持：
     :c:func:`lora_cad`、:c:func:`lora_cad_async`。
     CAD 参数和 LBT 模式通过
     :c:struct:`lora_modem_config` 配置。
   * 添加了 :c:func:`lora_recv_duty_cycle` 用于硬件驱动的
     无线电唤醒（RX 占空比循环）。

* Mbed TLS

  * 添加了 :kconfig:option:`CONFIG_MBEDTLS_VERSION_C` 以简化
    Mbed TLS 的版本信息导出。启用后，
    :c:func:`mbedtls_version_get_number()` 函数将可用。

  * Mbed TLS 已升级到 4.1.0 版本。从现在开始，该仓库将仅包含 TLS
    和 X.509，而加密支持已移至 TF-PSA-Crypto。
    为后者引入了一个新的 west 模块，基于上游发布 1.1.0。
    两个项目的发布说明可在以下地址找到：

    * https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-4.1.0
    * https://github.com/Mbed-TLS/TF-PSA-Crypto/releases/tag/tf-psa-crypto-1.1.0

* Zbus

   * 添加了异步监听器支持。异步监听器在工作队列上下文中执行，
     而非发布者的线程中，从而启用非阻塞操作，
     而无需专用的订阅者线程。
   * 添加了 :zephyr:code-sample:`zbus-async-listeners`。
   * 添加了实验性代理代理通信，带有 IPC 后端支持，
     用于跨域转发信道数据。
   * 添加了 :zephyr:code-sample:`zbus-proxy-agent-ipc`。
   * 添加了 :c:func:`zbus_chan_from_name` 函数。
     从其名称字符串获取 zbus 信道。
   * 添加了 :c:func:`zbus_async_listener_set_work_queue` 函数。
     为异步监听器设置工作队列。
   * 添加了 :c:func:`zbus_chan_pub_stats_msg_age` 函数。
     获取自上次发布以来的消息年龄（毫秒）。
   * 澄清了观察者优先级文档并修复了拼写和语法。
   * 更新了文档中的观察者类型图像。
   * 过滤掉了不支持 SMP 的测试。

其他显著更改
*********************

..
  更多描述性的子系统或驱动更改。你真的想写一段话，
  还是只需链接到上面的 api/驱动/Kconfig/开发板页面就足够了？

* 添加了对 Armv8.1-M MPU 的 PXN（特权执行禁止）属性的支持。
  使用此功能后，``__ramfunc`` 和 ``__ram_text_reloc`` 的 MPU 属性被修改，
  使得如果以 ``CONFIG_ARM_MPU_PXN`` 和 ``CONFIG_USERSPACE`` 编译，
  这些区域将设置 PXN 属性。
  这导致从这些区域执行的代码行为发生变化，因为
  如果这些区域设置了 pxn 属性，则无法在特权模式下执行。

* 移除了对 Nucleo WBA52CG 开发板（``nucleo_wba52cg``）的支持，
  因为它是 NRND（不推荐用于新设计）且自 2023 年 7 月的 1.1.0 版本起
  不再受 STM32CubeWBA 支持。
  建议改为迁移到 :zephyr:board:`nucleo_wba55cg`（``nucleo_wba55cg``）。

* 将 Mbed TLS 更新到 3.6.5 版本（从 3.6.4）。该版本的发布说明可在以下链接找到：

  * https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-3.6.5

* 将 TF-M 更新到 2.2.2 版本（从 2.2.0）。发布说明可在以下地址找到：

  * https://trustedfirmware-m.readthedocs.io/en/tf-mv2.2.2/releases/2.2.1.html
  * https://trustedfirmware-m.readthedocs.io/en/tf-mv2.2.2/releases/2.2.2.html

* TF-M NS 接口头文件现在通过 ``zephyr_interface`` CMake 库自动提供给
  非安全应用程序，无需显式链接 ``tfm_api``。

* NXP SoC DTSI 文件已通过将其移动到 ``dts/arm/nxp`` 下的
  特定于系列的子目录进行重新组织。

* 基于 :zephyr:board:`native_sim` 的目标现在可以 :ref:`交叉编译 <posix_arch_cross_compile>`
  （:github:`100182`）
