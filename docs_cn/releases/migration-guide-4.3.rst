:orphan:

..
  参见
  https://docs.zephyrproject.org/latest/releases/index.html#migration-guides
  了解本文档应包含的内容。

.. _migration_4.3:

Zephyr v4.3.0 迁移指南
######################

本文档描述了将应用从 Zephyr v4.2.0 迁移到 Zephyr v4.3.0 所需的更改。

其他更改（与迁移应用无直接关系）可在
:ref:`发布说明<zephyr_4.3>` 中查看。

.. contents::
    :local:
    :depth: 2

构建系统
************

内核
******

* :c:func:`device_init` 早期版本由于 bug 在设备初始化失败时返回正的 +errno 值。
  现已修复为返回正确的负的 -errno 值。
  为此问题实现了变通方案的应用现在应相应更新其代码。

基础库
**************

* UTF-8 工具声明（:c:func:`utf8_trunc`、:c:func:`utf8_lcpy`）
  已从 ``util.h`` 移至单独的
  :zephyr_file:`include/zephyr/sys/util_utf8.h` 文件。

* ``Z_MIN``、``Z_MAX`` 和 ``Z_CLAMP`` 宏已重命名为
  :c:macro:`min`、:c:macro:`max` 和 :c:macro:`clamp`。

* 头文件 ``<zephyr/posix/time.h>``、``<zephyr/posix/signal.h>`` 不应再使用。
  应以标准路径 ``<time.h>`` 和 ``<signal.h>`` 包含它们，由 C 库提供。
  非 POSIX C 库维护者可包含 :zephyr_file:`include/zephyr/posix/posix_time.h`
  和 :zephyr_file:`include/zephyr/posix/posix_signal.h`
  以可移植地提供 POSIX 定义。

* POSIX 限制不再定义在 ``<zephyr/posix/posix_features.h>`` 中。
  类似地，应以标准路径通过 ``<limits.h>`` 包含它们，由 C 库提供。
  非 POSIX C 库维护者可包含
  :zephyr_file:`include/zephyr/posix/posix_limits.h`
  以获取 Zephyr 的定义。
  某些运行时不变的值可能需要通过 :c:func:`sysconf` 查询。

* 文件描述符表大小及其可用性现在由 ``ZVFS_OPEN_SIZE`` 宏定义决定，
  而非 :kconfig:option:`CONFIG_ZVFS_OPEN_MAX` Kconfig 选项。
  子系统可通过指定前缀为 ``CONFIG_ZVFS_OPEN_ADD_SIZE_`` 的 Kconfig 选项
  指定其自定义文件描述符表大小需求。
  旧 Kconfig 选项仍然存在，但如果自定义需求更大则会被覆盖。
  要强制使用旧 Kconfig 选项，即使其值小于指定的自定义需求，
  已引入新的 :kconfig:option:`CONFIG_ZVFS_OPEN_IGNORE_MIN` 选项
  （默认禁用）。

开发板
******

* b_u585i_iot02a/ns：闪存布局已更改，
  以与上游 TF-M 2.2.1 开发板配置同步。
  新布局扩展了闪存分区，将次要分区移到外部 NOR 闪存。
  此更改目前阻止从旧 Zephyr 版本映像升级到 Zephyr 4.3 版本映像。
  更多细节参见 TF-M 迁移和发布说明。

* nucleo_h753zi：闪存布局已更新，
  固件升级可能因与之前布局不兼容而失败。
  新布局包括将存储分区扩展为 2 个扇区、移除 scratch 分区
  以及重新排序所有闪存分区以改善结构。

* mimxrt11x0：lpadc1 重命名为 lpadc2，lpadc0 重命名为 lpadc1。

* NXP ``frdm_mcxa166`` 重命名为 ``frdm_mcxa346``。
* NXP ``frdm_mcxa276`` 重命名为 ``frdm_mcxa266``。

* Panasonic ``panb511evb`` 重命名为 ``panb611evb``。

* STM32 开发板的 OpenOCD 配置文件已更改，
  以支持最新 OpenOCD 版本（> v0.12.0），
  其中 HLA/SWD 传输已弃用
  （参见 https://review.openocd.org/c/openocd/+/8523
  和 commit https://sourceforge.net/p/openocd/code/ci/34ec5536c0ba3315bc5a841244bbf70141ccfbb4/）。
  连接到运行 v2j24 之前固件的 ST-Link 适配器时可能遇到问题
  （其不支持新传输）。
  在此情况下，应升级 ST-Link 固件，
  或者（如果不可能）将 OpenOCD 配置脚本更改为
  ``source "interface/stlink-hla.cfg"`` 并显式选择 ``hla_swd`` 接口，
  以保持与 OpenOCD v0.12.0 或更早版本的向后兼容性。

设备驱动程序和设备树
*****************************

.. zephyr-keep-sorted-start re(^\w)

ADC
===

* ``iadc_gecko.c`` 驱动被 ``adc_silabs_iadc.c`` 替换。
  :dtcompatible:`silabs,gecko-iadc` 被 :dtcompatible:`silabs,iadc` 替换。

* :dtcompatible:`st,stm32-adc` 及其衍生兼容字符串现在要求定义
  ``clock-names`` 属性，且与 ``clocks`` 属性中的时钟数匹配。
  期望的时钟名称为 ``adcx``（寄存器时钟）、``adc-ker``（内核源时钟）
  和 ``adc-pre``（设置 ADC 预分频器，
  对于位于 RCC 寄存器中的系列）。

时钟控制
=============

* :kconfig:option:`CONFIG_CLOCK_STM32_HSE_CLOCK` 不再用户可配置。
  其值现在始终取自 ``&clk_hse`` DT 节点的 ``clock-frequency`` 属性
  （但仅当节点启用时，否则符号未定义）。
  此更改应仅影响 STM32 MPU 平台，
  且使其与 STM32 MCU 平台的现有实践对齐。

* :dtcompatible:`st,stm32f1-rcc` 和 :dtcompatible:`st,stm32f3-rcc`
  不再存在。
  因此 ``adc-prescaler``、``adc12-prescaler`` 和 ``adc34-prescaler``
  属性也不再定义。
  它们通过在 ADC ``clocks`` 属性中增加预分频器作为额外时钟来替换。

比较器
==========

* :dtcompatible:`nordic,nrf-comp` 和 :dtcompatible:`nordic,nrf-lpcomp`
  的 ``psel`` 和 ``extrefsel`` 属性类型已更改为整数。
  这些属性的值范围从 :c:macro:`NRF_COMP_AIN0` 到
  :c:macro:`NRF_COMP_AIN_VDDH_DIV5`，
  其中 :c:macro:`NRF_COMP_AIN0` 到 :c:macro:`NRF_COMP_AIN7`
  代表外部输入 AIN0 到 AIN7，
  :c:macro:`NRF_COMP_AIN_VDD_DIV2` 代表内部参考 VDD/2，
  :c:macro:`NRF_COMP_AIN_VDDH_DIV5` 代表 VDDH/5。
  旧的 ``string`` 属性类型已弃用。

DMA
===

* DMA 不再在其 API 中实现用户模式系统调用。
  系统调用被确定在访问上定义过于宽泛，
  且无法以安全方式实现系统调用参数验证步骤。

以太网
========

* :dtcompatible:`microchip,vsc8541` PHY 驱动现在要求
  ``reset-gpios`` 条目在复位用作低有效时指定 GPIO_ACTIVE_LOW 标志。
  之前低有效特性硬编码在驱动中。
  （:github:`91726`）

* CRC 校验和生成卸载到硬件现在在 Xilinx GEM 以太网驱动
  （:dtcompatible:`xlnx,gem`）中显式禁用而非显式启用。
  默认情况下，卸载现在默认启用以提高性能，
  然而，对于 QEMU 目标，卸载始终禁用，
  因为硬件中的校验和生成不被仿真，
  无论是否通过设备树显式禁用。
  （:github:`95435`）

  * 替换了启用 RX 校验和卸载的设备树属性
    ``rx-checksum-offload`` 为 ``disable-rx-checksum-offload``，
    后者现在主动禁用它。
  * 替换了启用 TX 校验和卸载的设备树属性
    ``tx-checksum-offload`` 为 ``disable-tx-checksum-offload``，
    后者现在主动禁用它。

* Xilinx GEM 以太网驱动（:dtcompatible:`xlnx,gem`）
  现在在运行时从设计配置寄存器获取与当前目标 SoC
  （Zynq-7000 或 ZynqMP）匹配的 AMBA AHB 数据总线宽度，
  使设备树属性 ``amba-ahb-dbus-width`` 过时，
  因此已被移除。

* :dtcompatible:`nxp,enet-mac` 和 :dtcompatible:`xlnx,gem` 驱动
  不再在初始化时通过 :c:func:`phy_configure_link`
  配置 phy 的链路速度和双工模式。
  相反，如果希望限制自动协商的通告速度
  （当 mac 仅支持 phy 支持速度的子集时），
  用户必须使用 phy 的 ``default-speeds`` 设备树属性。
  （:github:`91572`）

多功能设备
===

* AXP2101 的驱动支持已从 AXP192 中分离。
  因此，Kconfig 符号 ``MFD_AXP192_AXP2101`` 已移除。
  :kconfig:option:`MFD_AXP192` 现在用于 AXP192 设备，
  而 :kconfig:option:`MFD_AXP2101` 用于 AXP2101 设备。

杂项
====

* nrf_etr 驱动已迁移到 drivers/debug。
  因此，相关 Kconfig 符号已从 ``NRF_ETR`` 重命名为
  :kconfig:option:`DEBUG_NRF_ETR`，连同其他 ``NRF_ETR`` 符号。
  此外，驱动现在需要通过 :kconfig:option:`DEBUG_DRIVER` 显式启用，
  因为不再默认构建。

PWM
===

* :dtcompatible:`nxp,pca9685` 的 ``invert`` 属性已移除，
  现在可以使用 :c:macro:`PWM_POLARITY_INVERTED` 或
  :c:macro:`PWM_POLARITY_NORMAL` 标志作为指定单元，
  因为 space "pwm" 现在命名为：``['channel', 'period', 'flags']``
  （旧值：``['channel', 'period']``），
  且 ``#pwm-cells`` 常量值从 2 更改为 3。

PHY
===

* 兼容属性为 :dtcompatible:`st,stm32u5-otghs-phy` 的节点
  现在需要使用新属性 clock-reference
  在 SYSCFG_OTGHSPHYCR 寄存器中选择 CLKSEL（phy 参考时钟）。
  选择直接依赖于位于 RCC_CCIPR2 寄存器中的
  OTGHSSEL（OTG_HS PHY 内核时钟源选择）的值。

SPI
===

* 宏 :c:macro:`SPI_CS_CONTROL_INIT`、:c:macro:`SPI_CS_CONTROL_INIT_INST`、
  :c:macro:`SPI_CONFIG_DT`、:c:macro:`SPI_CONFIG_DT_INST`、
  :c:macro:`SPI_DT_SPEC_GET` 和 :c:macro:`SPI_DT_SPEC_INST_GET`
  已更改，不再需要提供延迟参数。
  这是因为 SPI 外设芯片选择的时序参数
  现在应通过 ``spi-cs-setup-delay-ns`` 和 ``spi-cs-hold-delay-ns``
  属性在 DT 中指定。
  （:github:`87427`）

传感器
=======

* 兼容属性为 :dtcompatible:`invensense,icm42688` 的节点
  现在还需要包含 :dtcompatible:`invensense,icm4268x` 才能工作。

步进电机
=======

* :dtcompatible:`zephyr,gpio-stepper` 已被
  :dtcompatible:`zephyr,h-bridge-stepper` 替换。

USB
===

* USB 视频类之前配置源视频设备的帧率和格式。
  现在这应由应用在主机会选择格式后完成
  （:github:`93192`）。

.. zephyr-keep-sorted-stop

蓝牙
*********

* :c:struct:`bt_le_cs_test_param` 和
  :c:struct:`bt_le_cs_create_config_params`
  现在要求将主模式和子模式作为单个参数提供。
* :c:struct:`bt_conn_le_cs_config`
  现在将主模式和子模式作为单个参数报告。
* :c:struct:`bt_conn_le_cs_main_mode` 和
  :c:struct:`bt_conn_le_cs_sub_mode`
  已被 :c:struct:`bt_conn_le_cs_mode` 替换。

蓝牙控制器
====================

* 以下已重命名：

  * :kconfig:option:`CONFIG_BT_CTRL_ADV_ADI_IN_SCAN_RSP` 到
    :kconfig:option:`CONFIG_BT_CTLR_ADV_ADI_IN_SCAN_RSP`
  * :c:struct:`bt_hci_vs_fata_error_cpu_data_cortex_m` 到
    :c:struct:`bt_hci_vs_fatal_error_cpu_data_cortex_m`，
    且现在包含程序计数器值。

.. zephyr-keep-sorted-start re(^\w)

蓝牙音频
==============

* :c:struct:`bt_audio_codec_cfg` 现在要求显式设置目标延迟和目标 PHY，
  而非始终将目标延迟设置为 "Balanced"、目标 PHY 设置为 LE 2M。
  要保持当前功能，将 ``target_latency`` 设为
  :c:enumerator:`BT_AUDIO_CODEC_CFG_TARGET_LATENCY_BALANCED`，
  将 ``target_phy`` 设为 :c:enumerator:`BT_AUDIO_CODEC_CFG_TARGET_PHY_2M`。
  :c:macro:`BT_AUDIO_CODEC_CFG` 宏默认使用这些值。
  （:github:`93825`）
* 为 GMAP 设置 BGS 角色现在还需要支持并实现
  :kconfig:option:`CONFIG_BT_BAP_BROADCAST_ASSISTANT`。
  参见 :zephyr:code-sample:`bluetooth_bap_broadcast_assistant` 示例作为参考。
* BAP 扫描委托者（BAP Scan Delegator）不再自动更新 PA 同步状态，
  必须使用 :c:func:`bt_bap_scan_delegator_set_pa_state` 更新状态。
  如果 BAP 扫描委托者与 BAP 广播汇（BAP Broadcast Sink）一起使用，
  则 :c:struct:`bt_bap_broadcast_sink` 的接收状态的 PA 状态
  在 PA 状态更改时仍会自动更新。
  （:github:`95453`）


.. zephyr-keep-sorted-stop

蓝牙 HCI
=============

* 已从 ``bt-hci-bus`` 设备树属性中移除弃用的 ``ipm`` 值。
  应改用 ``ipc``。

蓝牙 Mesh
=============

* Kconfig 选项 ``CONFIG_BT_MESH_USES_MBEDTLS_PSA`` 和
  ``CONFIG_BT_MESH_USES_TFM_PSA`` 已移除。
  PSA Crypto 提供者的选择现在由 Kconfig
  :kconfig:option:`CONFIG_PSA_CRYPTO` 自动控制。

蓝牙主机
=============

* :kconfig:option:`CONFIG_BT_FIXED_PASSKEY` 已弃用。
  相反，应用现在可以使用
  :c:member:`bt_conn_auth_cb.app_passkey` 回调
  为配对提供密钥，该回调在启用
  :kconfig:option:`CONFIG_BT_APP_PASSKEY` 时可用。
  应用可以返回用于配对的密钥，
  或 :c:macro:`BT_PASSKEY_RAND` 让主机生成随机密钥。

电源管理
****************

* :kconfig:option:`CONFIG_PM_S2RAM` 和
  :kconfig:option:`PM_S2RAM_CUSTOM_MARKING`
  已重构为由 SoC 和设备树自动管理。
  应用不应再直接启用它们，
  相反，应在设备树中启用或禁用 "suspend-to-ram" 电源状态。

* 对于 NXP RW61x，设备树属性 ``exit-latency-us``
  已更新以反映更准确的实测唤醒时间。
  对于使用待机模式（PM3）的应用，
  此更新以及 ``min-residency-us`` 设备树属性的增加
  可能影响系统在电源模式之间的转换。
  在某些情况下，这可能导致功耗变化。

网络
**********

* HTTP 服务器现在尊重配置的 ``_config`` 值。
  检查你为 :c:macro:`HTTP_SERVICE_DEFINE_EMPTY`、
  :c:macro:`HTTPS_SERVICE_DEFINE_EMPTY`、:c:macro:`HTTP_SERVICE_DEFINE`
  和 :c:macro:`HTTPS_SERVICE_DEFINE` 提供适用值。

* 套接字地址长度类型 :c:type:`socklen_t` 的大小已更改。
  它现在定义为始终为 32 位 ``uint32_t``，以与 Linux 对齐。
  之前它被定义为 ``size_t``，
  意味着大小可能根据系统配置为 32 位或 64 位。

* :c:func:`net_icmp_init_ctx` API 已更改，
  现在接受额外的 ``family`` 参数
  以指示上下文应处理的分组族。
  对于 ICMPv4 上下文，使用 ``AF_INET``；
  对于 ICMPv6 上下文，使用 ``AF_INET6``。

.. zephyr-keep-sorted-start re(^\w)

CoAP
====

* :c:type:`coap_client_response_cb_t` 签名已更改。
  参数列表现在作为 :c:struct:`coap_client_response_data`
  指针传递。

* :c:struct:`coap_client_request` 已更改
  以提高库对错误配置的韧性
  （即在结构体内使用临时指针）：

  * :c:member:`coap_client_request.path`
    现在是 ``char`` 数组而非指针。
    数组大小可通过
    :kconfig:option:`CONFIG_COAP_CLIENT_MAX_PATH_LENGTH` 配置。
  * :c:member:`coap_client_request.options`
    现在是 :c:struct:`coap_client_option` 数组而非指针。
    数组大小可通过
    :kconfig:option:`CONFIG_COAP_CLIENT_MAX_EXTRA_OPTIONS` 配置。

.. zephyr-keep-sorted-stop

调制解调器
*****

* ``CONFIG_MODEM_AT_SHELL_USER_PIPE``
  已重命名为 :kconfig:option:`CONFIG_MODEM_AT_USER_PIPE`。
* ``CONFIG_MODEM_CMUX_WORK_BUFFER_SIZE``
  已更新为 :kconfig:option:`CONFIG_MODEM_CMUX_WORK_BUFFER_SIZE_EXTRA`，
  其仅取默认值（:kconfig:option:`CONFIG_MODEM_CMUX_MTU` + 7）之上
  所需的额外字节数。

显示
*******

* RGB565 和 BGR565 像素格式在显示示例中可互换使用。
  这已修复。
  基于之前示例测试或开发的开发板和应用
  可能受此更改影响
  （更多信息参见 :github:`79996`）。

* SSD1363 使用 'greyscale' 的属性现在使用 'grayscale'。

PTP 时钟
*********

* :c:func:`ptp_clock_rate_adjust` API 的文档
  未提供适当且清晰的功能描述。
  驱动实现为相对于当前频率调整速率比。
  现在 PTP 和 gPTP 中引入了 PI 伺服，
  且此 API 函数已更改为基于标称频率调整速率比。
  实现 :c:func:`ptp_clock_rate_adjust` 的驱动
  应调整以适应新行为。

视频
*****

* 已从 :c:struct:`video_caps` 中移除
  ``min_line_count`` 和 ``max_line_count`` 字段。
  应用应基于新的 :c:member:`video_format.size` 分配缓冲区。

其他子系统
****************

.. zephyr-keep-sorted-start re(^\w)

蜂窝网络
========

 * :c:enum:`cellular_access_technology` 值已重新定义
   以与 3GPP TS 27.007 对齐。
 * :c:enum:`cellular_registration_status` 值已扩展
   以与 3GPP TS 27.007 对齐。

加密
======

* 哈希操作现在要求 :c:struct:`hash_pkt` 中的输入为常量。
  这不应影响任何现有代码，
  除非树外哈希后端实际就地执行该操作
  （参见 :github:`94218`）

闪存映射
=========

* 随着长期目标过渡到 PSA Crypto API 作为
  Zephyr 中唯一的加密支持，
  :kconfig:option:`FLASH_AREA_CHECK_INTEGRITY_MBEDTLS` 已弃用。
  :kconfig:option:`FLASH_AREA_CHECK_INTEGRITY_PSA`
  现在是默认选择：
  如果 TF-M 未启用或平台不支持，
  将使用 Mbed TLS 作为 PSA Crypto API 提供者。

日志
=======

* UART 字典日志解析脚本
  ``scripts/logging/dictionary/log_parser_uart.py`` 已弃用。
  相反，应使用更通用的
  :zephyr_file:`scripts/logging/dictionary/live_log_parser.py` 脚本。
  新脚本支持相同功能（及更多），
  但调用时需要不同的命令行参数。

MCUmgr
======

* :ref:`OS mgmt<mcumgr_smp_group_0>`
  :ref:`mcumgr_os_application_info` 命令
  对硬件平台的响应已更新，
  输出开发板目标而非开发板和开发板修订版本，
  后者现在包含 SoC 和开发板变体。
  旧行为已弃用，但仍可通过启用
  :kconfig:option:`CONFIG_MCUMGR_GRP_OS_INFO_HARDWARE_INFO_SHORT_HARDWARE_PLATFORM`
  使用。

* 已移除对旧版 Mbed TLS 哈希加密的支持，
  仅使用 PSA Crypto API。
  :kconfig:option:`CONFIG_MCUMGR_GRP_FS_HASH_SHA256`
  如果在构建中未启用 TF-M，
  将自动启用 Mbed TLS 及其 PSA Crypto 实现。

Mbed TLS
========

* 为了改善 Zephyr Kconfig 与 Mbed TLS 构建符号之间的
  1:1 匹配，以下 Kconfig 已重命名：

  * :kconfig:option:`CONFIG_MBEDTLS_MD` ->
    :kconfig:option:`CONFIG_MBEDTLS_MD_C`
  * :kconfig:option:`CONFIG_MBEDTLS_LMS` ->
    :kconfig:option:`CONFIG_MBEDTLS_LMS_C`
  * :kconfig:option:`CONFIG_MBEDTLS_TLS_VERSION_1_2` ->
    :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_TLS1_2`
  * :kconfig:option:`CONFIG_MBEDTLS_DTLS` ->
    :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_DTLS`
  * :kconfig:option:`CONFIG_MBEDTLS_TLS_VERSION_1_3` ->
    :kconfig:option:`CONFIG_MBEDTLS_SSL_PROTO_TLS1_3`
  * :kconfig:option:`CONFIG_MBEDTLS_TLS_SESSION_TICKETS` ->
    :kconfig:option:`CONFIG_MBEDTLS_SSL_SESSION_TICKETS`
  * :kconfig:option:`CONFIG_MBEDTLS_CTR_DRBG_ENABLED` ->
    :kconfig:option:`CONFIG_MBEDTLS_CTR_DRBG_C`
  * :kconfig:option:`CONFIG_MBEDTLS_HMAC_DRBG_ENABLED` ->
    :kconfig:option:`CONFIG_MBEDTLS_HMAC_DRBG_C`

RTIO
====

* 回调操作现在接受额外的参数，
  对应链中第一个错误的结果码。
* 无论链中先前提交的成功/错误状态如何，
  回调操作始终被调用。

安全存储
=============

* 用于标识存储条目的 :c:type:`psa_storage_uid_t` 大小
  已从 64 位更改为 30 位。
  此更改破坏了对先前存储条目的向后兼容性，
  其认证将开始失败。
  如果你正在从早期 Zephyr 版本更新现有安装
  并希望保留先前存在的条目，
  启用 :kconfig:option:`CONFIG_SECURE_STORAGE_64_BIT_UID`。
  （:github:`94171`）

Shell
=====

* 与 :kconfig:option:`SHELL_BACKEND_MQTT` 相关的 MQTT 主题已重命名。
  将 ``<device_id>_rx`` 重命名为 ``<device_id>/sh/rx``，
  将 ``<device_id>_tx`` 重命名为 ``<device_id>/sh/tx``。
  ``<device_id>`` 之后的部分现在可通过
  :kconfig:option:`SHELL_MQTT_TOPIC_RX_ID` 和
  :kconfig:option:`SHELL_MQTT_TOPIC_TX_ID` 配置。
  这允许保留之前的主题以实现向后兼容性。
  （:github:`92677`）

UpdateHub
=========

* 已移除旧版 Mbed TLS 作为加密支持的选项，
  现在所有情况均使用 PSA Crypto。
  :kconfig:option:`CONFIG_UPDATEHUB`
  如果在构建中未启用 TF-M，
  将自动启用 Mbed TLS 的 PSA Crypto 实现。

.. zephyr-keep-sorted-stop

模块
*******

* 已移除 TinyCrypt 库，因为上游版本不再维护。
  PSA Crypto API 现在是 Zephyr 推荐的加密库。

MCUboot
=======

* MCUboot 的默认操作模式已更改为使用偏移量交换，
  这提供了更快的交换更新、更少的开销，
  并减少了执行更新所需的闪存耐久性循环，
  之前的默认值是使用移动交换。
  如果开发板通过使主插槽比次插槽大一个扇区
  来针对使用移动交换进行优化，
  则此设置需要更改为使次插槽比主插槽大一个扇区
  （对于优化使用，仍支持两个插槽具有相同数量的扇区）。
  或者，可以在 sysbuild 中使用
  :kconfig:option:`SB_CONFIG_MCUBOOT_MODE_SWAP_USING_MOVE`
  选择之前的使用移动交换模式。

Silabs
======

* 将 Rail 选项的名称与其他 SiSDK 相关选项对齐：

  * :kconfig:option:`CONFIG_RAIL_PA_CURVE_HEADER` 到
    :kconfig:option:`CONFIG_SILABS_SISDK_RAIL_PA_CURVE_HEADER`
  * :kconfig:option:`CONFIG_RAIL_PA_CURVE_TYPES_HEADER` 到
    :kconfig:option:`CONFIG_SILABS_SISDK_RAIL_PA_CURVE_TYPES_HEADER`
  * :kconfig:option:`CONFIG_RAIL_PA_ENABLE_CALIBRATION` 到
    :kconfig:option:`CONFIG_SILABS_SISDK_RAIL_PA_ENABLE_CALIBRATION`

* 修复了 :kconfig:option:`CONFIG_SOC_*` 的名称。
  这些选项之前包含 PART_NUMBER，而它们不应包含。

* 已从 Series 2 SoC 中移除单独的 ``em3`` 电源状态。
  系统根据振荡器的硬件外设请求
  自动转换到 EM2 或 EM3。

LVGL
====

* PIXEL_FORMAT_MONO10 和 PIXEL_FORMAT_MONO01 格式
  在 :zephyr_file:`modules/lvgl/lvgl_display_mono.c` 中被交换，
  导致使用 LVGL 配合单色显示时黑白反转。
  此问题现已修复。
  之前为达到预期行为而应用的任何变通方案
  应被移除，否则黑白将再次反转。

LED 灯带
=========

* 将 ``arduino,modulino-smartleds``
  重命名为 :dtcompatible:`arduino,modulino-pixels`

Trusted Firmware-M
==================

* BL2（MCUboot）的签名流程已更新。
  使用 TF-M NS 运行且需要 BL2 的开发板
  必须具有包含闪存控制器信息的闪存布局。
  这将确保在签名 hex/bin 文件时
  所有细节都存在于 S 和 NS 映像中。
  映像现在具有允许 FWU 状态机正确
  并允许 FOTA 的细节。
  （:github:`94470`）

  * ``--align`` 参数已修复为 1。
    现在，它设置为闪存 DT ``write_block_size`` 属性，
    但仍为特定厂商提供 1 作为回退。
  * ``--max-sectors`` 值现在基于映像数量计算，
    考虑最大映像大小。
  * ``--confirm`` 选项现在确认 S 和 NS HEX 映像，
    确保任何运行的映像对生产环境和开发环境均有效。
  * S 和 NS BIN 映像现在可用。
    这些是 FOTA 中应使用的正确映像。
    注意 S 和 NS 映像默认未确认，
    且应用负责用 ``psa_fwu_accept()`` 确认它们。
    否则，映像将在下次重启时回滚。

* 在 TF-M v2.1.0 发布后引入的 TF-M 证明（attestation）流程中
  识别出兼容性问题。
  因此，使用 TF-M v2.1 的系统无法升级到任何更晚的 TF-M 版本
  而不遇到故障。
  此限制影响使用 TF-M v2.1.0 到 v2.1.2 的 Zephyr 版本
  （具体为 Zephyr v3.7 到 v4.2），
  阻止这些版本之间的无缝升级。
  该问题已在 10 月 25 日在 mainline TF-M 中解决，
  且修复包含在 Zephyr v4.3.0 中。
  建议用户直接从任何早期 Zephyr 版本迁移到 Zephyr v4.3.0 或更晚版本
  以确保完整的 TF-M 证明功能和升级兼容性。
  （:github:`94859`）
  对于最初从 Zephyr v4.0 到 v4.2 构建的任何应用，
  :kconfig:option:`CONFIG_TFM_ZEPHYR_4_0_TO_4_2_COMPATIBILITY`
  必须设置才能成功升级到 v4.2 之后的任何版本，
  且对所有未来升级保持设置。
  （:github:`103793`）

* 已移除构建中 CMake 自动下载 MCUboot 和 ethos 的支持，
  改用树内版本的这些模块。
  要使用自定义版本，
  创建 :ref:`west manifest <west-manifest-files>`
  以拉取这些仓库的期望版本。
