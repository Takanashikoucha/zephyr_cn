:orphan:

.. _migration_4.0:

迁移到 Zephyr v4.0.0 的指南
################################

本文档描述了将应用程序从 Zephyr v3.7.0 迁移到 Zephyr v4.0.0 时所需的更改。

任何其他更改（与迁移应用程序不直接相关）可在 :ref:`发布说明 <zephyr_4.0>` 中找到。

.. contents::
   :local:
   :depth: 2

构建系统
************

* 移除了 ``CONFIG_MCUBOOT_CMAKE_WEST_SIGN_PARAMS`` Kconfig 选项，
  因为为 MCUboot 签名映像时
  构建系统不再调用 ``west sign``。

* ``west sign`` 的 imgtool 部分已弃用，签名时应提供给 imgtool 的选项应改为在 :kconfig:option:`CONFIG_MCUBOOT_EXTRA_IMGTOOL_ARGS` 中设置。

内核
******

* 移除了已弃用的 :kconfig:option:`CONFIG_MP_NUM_CPUS`，
  应用程序应更新为使用
  :kconfig:option:`CONFIG_MP_MAX_NUM_CPUS`。

开发板
******

* ``native_posix`` 已弃用，改为 :zephyr:board:`native_sim<native_sim>`（:github:`76898`）。
* 基于 Nordic nRF53 和 nRF91 的开发板可使用 ``dts/common/nordic`` 中的通用设备树叠加层基于 TF-M 定义默认闪存和 RAM 分区。

* STM32WBA：用于获取构建 BLE 应用程序所需 blob 的命令现在为 ``west blobs fetch hal_stm32`` 而非 ``west blobs fetch stm32``。

* 开发板 ``qemu_xtensa`` 已弃用。改用 ``qemu_xtensa/dc233c``。

设备树
**********

* :c:macro:`DT_REG_ADDR` 宏及其变体现在扩展为无符号字面量（即带 ``U`` 后缀）。要将地址用作设备树索引使用 :c:macro:`DT_REG_ADDR_RAW` 变体。
* :c:macro:`DT_REG_SIZE` 宏及其变体也扩展为无符号字面量，此阶段不提供 raw 变体。

STM32
=====

* 在所有官方 STM32 开发板上，
  ``west flash`` 选择
  STM32CubeProgrammer 作为默认 west 运行器。
  如果你想强制选择其他运行器
  如 OpenOCD 或 pyOCD 用于烧录，
  应使用 west ``--runner`` 或 ``-r`` 选项指定。
  （:github:`75284`）
* ADC：如果使用属性 ``st,adc-clock-source = <ASYNC>``，则需显式定义域时钟。

模块
*******

Mbed TLS
========

* Kconfig 选项 ``CONFIG_MBEDTLS_TLS_VERSION_1_0`` 和 ``CONFIG_MBEDTLS_TLS_VERSION_1_1`` 已移除，因为 Mbed TLS 自 v3.0 起不再支持 TLS 1.0 和 1.1。（:github:`76833`）
* 以下 Kconfig 符号已重命名（:github:`76408`）：
  * ``CONFIG_MBEDTLS_ENTROPY_ENABLED`` 现在为 :kconfig:option:`CONFIG_MBEDTLS_ENTROPY_C`，
  * ``CONFIG_MBEDTLS_ZEPHYR_ENTROPY`` 现在为 :kconfig:option:`CONFIG_MBEDTLS_ENTROPY_POLL_ZEPHYR`。

* Kconfig 选项 ``CONFIG_MBEDTLS_SSL_EXPORT_KEYS`` 已移除，因为对应的构建符号已在 Mbed TLS 3.1.0 中移除且现在假设启用。（:github:`77657`）

TinyCrypt
=========

尽管 TinyCrypt 的正式弃用尚未开始，但从 Zephyr 代码库中移除已开始。正式弃用将在下一个版本中发生。

Trusted Firmware-M
==================

* 用于硬件回滚保护的
  安全计数器现在显式来自
  :kconfig:option:`CONFIG_TFM_IMAGE_SECURITY_COUNTER`，
  而非从映像版本自动确定。
  这已更改，
  因为隐式计数器计算
  与大于 ``0.0.1024`` 的版本不兼容。
  （:github:`78128`）

LVGL
====

zcbor
=====

* 将 zcbor 库更新到版本 0.9.0。完整发布说明在 https://github.com/NordicSemiconductor/zcbor/blob/0.9.0/RELEASE_NOTES.md 迁移指南在 https://github.com/NordicSemiconductor/zcbor/blob/0.9.0/MIGRATION_GUIDE.md 迁移指南复制于此：

  * ``zcbor_simple_*()`` 函数已移除以避免对其使用的混淆。它们仍在 C 文件中因为被其他函数使用。相反，使用当前支持的简单值的特定函数，即 ``zcbor_bool_*()``、``zcbor_nil_*()`` 和 ``zcbor_undefined_*()``。如果严格需要已移除的变体，在你的代码中添加你自己的前向声明。

  * 代码生成命名：

    * 更多 C 关键字现在大写以避免命名冲突。如果你的代码生成为有那些名称你可能需要大写某些实例。

    * 对带 .size 说明符的 bstr 元素的命名进行了修复，这可能意味着当你重新生成时这些元素在你的代码中更改名称。

设备驱动程序和设备树
*****************************

* LiteX 以太网控制器的 ``compatible`` 已从 ``litex,eth0`` 重命名为 :dtcompatible:`litex,liteeth`。（:github:`75433`）

* LiteX UART 控制器的 ``compatible`` 已从 ``litex,uart0`` 重命名为 :dtcompatible:`litex,uart`。（:github:`74522`）

* Microchip ``mcp23xxx`` 系列的
  设备树绑定已拆分。
  ``microchip,mcp230xx`` 和 ``microchip,mcp23sxx``
  的用户应将设备树 ``compatible`` 值
  更改为特定的芯片变体，
  例如 :dtcompatible:`microchip,mcp23017`。
  ``ngpios`` 设备树属性已移除，
  因为由型号名称隐含。
  带开漏输出的芯片变体
  （``mcp23x09``、``mcp23x18``）
  现在正确反映在其驱动程序 API 中，
  这些设备的用户应确保
  向 :c:func:`gpio_pin_set` 传递适当的值。
  （:github:`65797`）

* ``power-domain`` 属性已移除，改为 ``power-domains``。新属性允许添加多个电源域。``power-domain-names`` 也可用，以可选命名 ``power-domains`` 中每个条目。``power-domains`` 属性中单元的数量需用 ``#power-domain-cells`` 定义。

模数转换器（ADC）
=================================

* 对所有通过 ``st,adc-clock-source`` 属性选择异步时钟的 STM32 ADC，现在必须也用 ``clock`` 属性显式定义域时钟源。

时钟控制
=============

* nRF53 系列中存在的
  LFXO/HFXO（高/低频晶体振荡器）
  现在可用设备树配置。
  Kconfig 选项
  :kconfig:option:`CONFIG_SOC_ENABLE_LFXO`、
  :kconfig:option:`CONFIG_SOC_LFXO_CAP_EXTERNAL`、
  :kconfig:option:`CONFIG_SOC_LFXO_CAP_INT_6PF`、
  :kconfig:option:`CONFIG_SOC_LFXO_CAP_INT_7PF`、
  :kconfig:option:`CONFIG_SOC_LFXO_CAP_INT_9PF`、
  :kconfig:option:`CONFIG_SOC_HFXO_CAP_DEFAULT`、
  :kconfig:option:`CONFIG_SOC_HFXO_CAP_EXTERNAL`、
  :kconfig:option:`CONFIG_SOC_HFXO_CAP_INTERNAL`
  和 :kconfig:option:`CONFIG_SOC_HFXO_CAP_INT_VALUE_X2`
  已弃用。

  LFXO 现在可如此配置：

  .. code-block:: devicetree

     /* 使用外部电容器 */
     &lfxo {
           load-capacitors = "external";
     };

     /* 使用内部电容器（值需选择：6、7、9pF
     &lfxo {
           load-capacitors = "internal";
           load-capacitance-picofarad = <...>;
     };

  HFXO 现在可如此配置：

  .. code-block:: devicetree

     /* 使用外部电容器 */
     &hfxo {
           load-capacitors = "external";
     };

     /* 使用内部电容器（值需选择：7pF...20pF
      * 以 0.5pF 步长，单位：femtofarads）
      */
     &hfxo {
           load-capacitors = "internal";
           load-capacitance-femtofarad = <...>;
     };

加密
======

* 在 TinyCrypt 库弃用后（:github:`79566`），基于 TinyCrypt 的 shim 驱动程序已标记为已弃用。（:github:`79653`）

磁盘
====

* SDMMC 子系统驱动程序现在要求随磁盘定义提供 ``disk-name`` 属性，其用于将 SD 设备注册到磁盘子系统时。这允许同时注册多个 SD 设备。如果不确定，``disk-name = "SD"`` 可用作合理默认。

* MMC 子系统驱动程序现在要求随磁盘定义提供 ``disk-name`` 属性，其用于将 MMC 设备注册到磁盘子系统时。这允许同时注册多个 MMC 设备。如果不确定，``disk-name = "SD2"`` 可用作合理默认。

增强串行外设接口（eSPI）
===========================================

GNSS
====

* u-blox M10 驱动程序已重命名为 M8，因为其仅支持 M8 基于的设备。现有设备树 compatible 应更新为 :dtcompatible:`u-blox,m8`，且 Kconfig 符号交换为 :kconfig:option:`CONFIG_GNSS_U_BLOX_M8`。

* API :c:func:`gnss_set_periodic_config` 和 :c:func:`gnss_get_periodic_config` 已移除。（:github:`76392`）

输入
=====

* :c:macro:`INPUT_CALLBACK_DEFINE` 现在有额外的 ``user_data`` 空指针参数，可用于引用任何用户数据结构。要恢复当前行为可将其设置为 ``NULL``。回调函数参数中必须添加 ``void *user_data`` 参数。

* :dtcompatible:`analog-axis` ``invert`` 属性已重命名为 ``invert-input``（现在还有 ``invert-output`` 可用）。

PWM
===

* Raspberry Pi Pico PWM 驱动程序现在自适应配置频率。这导致设备树参数处理方式更改。如果指定 :dtcompatible:`raspberry,pico-pwm` 的 ``divider-int-0`` 或每个通道的变体，或如果这些设置为 0，驱动程序动态用指定周期配置分频比。如果为 ``divider-int-0`` 指定非零值，驱动程序将以指定分频比运行。这与先前行为不变。请显式指定 ``divider-int-0`` 以与之前相同的行为。

SDHC
====

* NXP USDHC 驱动程序现在假设存在卡如果未配置卡检测方式，而非用外设的内部卡检测信号检查卡存在。要用内部卡检测信号，应在使用的 USDHC 节点中添加设备树属性 ``detect-cd``。

传感器
=======

* Microchip MCP9808 温度传感器的现有驱动程序已转换并重命名以支持所有 JEDEC JC 42.4 兼容温度传感器。它现在用 :dtcompatible:`jedec,jc-42.4-temp` compatible 字符串而非 ``microchip,mcp9808`` 字符串。
* :dtcompatible:`current-sense-amplifier` 感测电阻现在以毫欧（``sense-resistor-milli-ohms``）而非微欧指定，以将最大可表示电阻从 4.2k 增加到 4.2M。
* :dtcompatible:`current-sense-amplifier` 属性 ``sense-gain-mult`` 和 ``sense-gain-div`` 现在限制为最大 ``UINT16_MAX`` 值，以启用内部计算中更小舍入误差。

* :dtcompatible:`nxp,kinetis-acmp` 中带 ``nxp,`` 前缀的属性已弃用，改为无前缀的属性。:dtcompatible:`nxp,kinetis-acmp` 的基于传感器的驱动程序已更新以同时支持新和弃用的属性名称。弃用属性名称的使用应更新为新属性名称。

串口
======

 * :c:func:`uart_irq_tx_ready` 的用户现在需检查 ``ret > 0`` 以确保 FIFO 可接受数据字节，而非 ``ret == 1``。函数现在返回可无截断提供给 :c:func:`uart_fifo_fill` 的字节数的下界。

 * LiteX：``CONFIG_UART_LITEUART`` 已重命名为 :kconfig:option:`CONFIG_UART_LITEX`。

稳压器
=========

* nRF52/53 系列中存在的
  内部稳压器现在可用设备树配置。
  由开发板级别 Kconfig 选项选择的
  Kconfig 选项
  :kconfig:option:`CONFIG_SOC_DCDC_NRF52X`、
  :kconfig:option:`CONFIG_SOC_DCDC_NRF52X_HV`、
  :kconfig:option:`CONFIG_SOC_DCDC_NRF53X_APP`、
  :kconfig:option:`CONFIG_SOC_DCDC_NRF53X_NET`
  和 :kconfig:option:`CONFIG_SOC_DCDC_NRF53X_HV`
  已弃用。

  nRF52 系列示例：

  .. code-block:: devicetree

      /* 在 DC/DC 模式配置 REG/REG1 */
      &reg/reg1 {
          regulator-initial-mode = <NRF5X_REG_MODE_DCDC>;
      };

      /* 启用 REG0（HV 模式） */
      &reg0 {
          status = "okay";
      };

  nRF53 系列示例：

  .. code-block:: devicetree

      /* 在 DC/DC 模式配置 VREGMAIN */
      &vregmain {
          regulator-initial-mode = <NRF5X_REG_MODE_DCDC>;
      };

      /* 在 DC/DC 模式配置 VREGRADIO */
      &vregradio {
          regulator-initial-mode = <NRF5X_REG_MODE_DCDC>;
      };

      /* 启用 VREGH（HV 模式） */
      &vregh {
          status = "okay";
      };

蓝牙
*********

蓝牙 HCI
=============

* HCI 绑定的 ``bt-hci-bus`` 和 ``bt-hci-quirks`` 设备树属性已更改为使用不带 ``BT_HCI_QUIRK_`` 和 ``BT_HCI_BUS_`` 前缀的小写字符串。
* Kconfig 选项 :kconfig:option:`BT_SPI` 现在自动基于设备树 compatible 选择，且可从开发板 ``.defconfig`` 文件中移除。

蓝牙音频
================

* VCP 的 Volume Renderer 回调函数 :code:`bt_vcp_vol_rend_cb.state` 和 :code:`bt_vcp_vol_rend_cb.flags` 现在包含连接的额外参数。这需添加到所有定义的 VCP Volume Renderer 回调函数实例。（:github:`76992`）

* Unicast Server 有新的注册函数 :c:func:`bt_bap_unicast_server_register`，其接受 :c:struct:`bt_bap_unicast_server_register_param` 作为参数。这允许 Unicast Server 在运行时动态注册 Source 和 Sink ASE 数量。旧的 :kconfig:option:`CONFIG_BT_ASCS_ASE_SRC_COUNT` 和 :kconfig:option:`CONFIG_BT_ASCS_ASE_SNK_COUNT` 已重命名为 :kconfig:option:`CONFIG_BT_ASCS_MAX_ASE_SRC_COUNT` 和 :kconfig:option:`CONFIG_BT_ASCS_MAX_ASE_SNK_COUNT`，以反映它们现在用作要使用的 ASE 的编译时最大配置。:c:func:`bt_bap_unicast_server_register` 需在使用 Unicast Server 前调用一次，且更具体地是在首次调用 :c:func:`bt_bap_unicast_server_register_cb` 前。在新的函数 :c:func:`bt_bap_unicast_server_unregister` 调用前无需再次调用。（:github:`76632`）

* Coordinated Set Coordinator 函数 :c:func:`bt_csip_set_coordinator_lock` 和 :c:func:`bt_csip_set_coordinator_release` 现在要求启用 :kconfig:option:`CONFIG_BT_BONDABLE` 且所有成员已绑定，以符合 CSIP 规范的要求。（:github:`78877`）

* 提供给 :c:func:`bt_bap_unicast_client_register_cb` 的回调结构体不再 :code:`const`，且现在可注册多个回调结构体。（:github:`78999`）

* 广播音频扫描服务（BASS）现在必须在扫描委托方中在运行时动态注册和取消注册。引入两个新 API :c:func:`bt_bap_scan_delegator_register()` 和 :c:func:`bt_bap_scan_delegator_unregister()`，以动态管理 BASS 和扫描委托方的注册和初始化。还应提及先前的回调注册函数 :c:func:`bt_bap_scan_delegator_register_cb()` 已移除并与 :c:func:`bt_bap_scan_delegator_register()` 合并。此更改允许在注册或取消注册扫描委托方和 BASS 相关功能时更灵活，无需构建时配置。现有的需更新为使用这些新 API。（:github:`78751`）

* 电话承载服务（TBS）和通用电话承载服务（GTBS）现在必须在运行时用 :c:func:`bt_tbs_register_bearer` 动态注册。服务也可用 :c:func:`bt_tbs_unregister_bearer` 取消注册。（:github:`76108`）

* 已从 ``bt_audio_codec_qos`` 重命名为 ``bt_bap_qos_cfg``。这影响所有使用 ``bt_audio_codec_qos`` 名称的结构体、枚举和定义。要用新命名，简单对 ``bt_audio_codec_qos`` 到 ``bt_bap_qos_cfg`` 和 ``BT_AUDIO_CODEC_QOS`` 到 ``BT_BAP_QOS_CFG`` 做查找替换。（:github:`76633`）

* Zephyr 栈内部的广播 ID 生成已移除，现在由应用程序生成广播 ID。这意味着应用程序现在可完全决定是否使用静态或随机广播 ID。重用和静态定义广播 ID已添加到版本 1.0.2 的基本音频配置文件，其是此更改的基础。:c:func:`bt_cap_initiator_broadcast_get_id` 和 :c:func:`bt_bap_broadcast_source_get_id` 的所有实例已移除。（:github:`80228`）

* ``BT_AUDIO_BROADCAST_CODE_SIZE`` 已移除，应改用 ``BT_ISO_BROADCAST_CODE_SIZE``。（:github:`80217`）

蓝牙 Host
=============

广告商自动恢复已弃用
---------------------------------------------

.. note::

   此弃用由编译器检查。如果你没有警告，则不应受影响。

已弃用符号：
   * :c:enumerator:`BT_LE_ADV_OPT_CONNECTABLE`
   * :c:enumerator:`BT_LE_ADV_OPT_ONE_TIME`
   * :c:macro:`BT_LE_ADV_CONN`

新符号：
   * :c:enumerator:`BT_LE_ADV_OPT_CONN`
   * :c:macro:`BT_LE_ADV_CONN_FAST_1`
   * :c:macro:`BT_LE_ADV_CONN_FAST_2`

:c:enumerator:`BT_LE_ADV_OPT_CONNECTABLE` 是使广告商可连接并启用自动恢复的组合指令。要禁用自动恢复，使用 :c:enumerator:`BT_LE_ADV_OPT_CONN`。

扩展广告 API 带简写
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

扩展广告 API ``bt_le_ext_adv_*`` 隐式假设 :c:enumerator:`BT_LE_ADV_OPT_ONE_TIME` 且从不自动恢复广告。因此，以下查找替换可不假思索地应用：

替换所有

.. code-block:: diff

   -bt_le_ext_adv_create(BT_LE_ADV_CONN, ...)
   +bt_le_ext_adv_create(BT_LE_ADV_FAST_2, ...)

.. code-block:: diff

   -bt_le_ext_adv_update_param(..., BT_LE_ADV_CONN)
   +bt_le_ext_adv_update_param(..., BT_LE_ADV_FAST_2)

扩展广告 API 带自定义参数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

你可能有 :c:enumerator:`BT_LE_ADV_OPT_CONNECTABLE` 用于赋值给 :c:struct:`bt_le_adv_param`。如果你的结构体从不传递给 :c:func:`bt_le_adv_start`，你应：

* 用 :c:enumerator:`BT_LE_ADV_OPT_CONN` 替换 :c:enumerator:`BT_LE_ADV_OPT_CONNECTABLE`。
* 移除 :c:enumerator:`BT_LE_ADV_OPT_ONE_TIME`。

不使用自动恢复的旧版广告 API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

使用 :c:enumerator:`BT_LE_ADV_OPT_CONNECTABLE` 和 :c:enumerator:`BT_LE_ADV_OPT_ONE_TIME` 组合的任何 :c:func:`bt_le_adv_start` 调用应将该组合替换为 :c:enumerator:`BT_LE_ADV_OPT_CONN`。

使用自动恢复的旧版广告 API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

对此情况，应用程序必须接管重启广告商的责任。参见扩展广告示例以获取广告商重启的示例实现。相同技术可用于旧版广告。

网络
**********

* CoAP 公共 API 函数 :c:func:`coap_get_block1_option` 和 :c:func:`coap_get_block2_option` 已更改。``block_number`` 指针类型已从 ``uint8_t *`` 更改为 ``uint32_t *``。此外，:c:func:`coap_get_block2_option` 现在接受额外的 ``bool *has_more`` 参数，以存储 more 标志的值。（:github:`76052`）

* 结构体 :c:struct:`coap_transmission_parameters` 在启用 :kconfig:option:`CONFIG_COAP_RANDOMIZE_ACK_TIMEOUT` 时有新字段 ``ack_random_percent``。（:github:`79058`）

* 以太网桥接 shell 已移到网络 shell 下。这是为了使所有网络 shell 活动可在 ``net`` shell 命令下找到。此更改后桥接 shell 由 ``net bridge`` 命令使用。（:github:`77235`）

* 以太网桥接代码已更改
  以允许类似 Linux 的配置体验。
  即使启用桥接，
  桥接的以太网接口也可正常使用。
  实际桥接由单独的虚拟网络接口完成，
  其将网络数据包
  引导到桥接的以太网接口。
  :c:func:`eth_bridge_iface_allow_tx` 已移除，
  因为不需要，
  桥接的以太网接口
  可正常发送和接收数据。
  :c:func:`eth_bridge_listener_add`
  和 :c:func:`eth_bridge_listener_remove` 已移除，
  因为相同功能
  可用混杂模式 API 实现。
  因为桥接接口是正常网络接口，
  :c:func:`eth_bridge_iface_add`
  和 :c:func:`eth_bridge_iface_remove`
  将接受网络接口指针
  作为第一个参数。
  （:github:`77987`）

* 为便于在网络子系统之外使用，网络缓冲区头文件已从 ``include/zephyr/net/buf.h`` 重命名为 :zephyr_file:`include/zephyr/net_buf.h`，且实现移到 :zephyr_file:`lib/net_buf/`。（:github:`78009`）

* ``NET_SOCKET_SERVICE_SYNC_DEFINE`` 和 ``NET_SOCKET_SERVICE_SYNC_DEFINE_STATIC`` 的 ``work_q`` 参数已移除，因为它始终被忽略。（:github:`79446`）

* 套接字服务的回调函数已更改。``struct k_work *work`` 参数已替换为 ``struct net_socket_service_event *pev`` 参数的指针。（:github:`80041`）

* 弃用 ``CONFIG_NET_SOCKETS_POLL_MAX`` 选项，改为 :kconfig:option:`CONFIG_ZVFS_POLL_MAX`。

其他子系统
****************

闪存映射
=========

 * ``CONFIG_SPI_NOR_IDLE_IN_DPD`` 已从 :kconfig:option:`CONFIG_SPI_NOR` 驱动程序移除。此功能的增强版本可通过在设备上启用 :ref:`pm-device-runtime` 获得（可用 :kconfig:option:`CONFIG_SPI_NOR_ACTIVE_DWELL_MS` 调节）。

hawkBit
=======

* :c:func:`hawkbit_autohandler` 现在接受一个参数。此参数必须设置为 ``true`` 以与更改前相同的行为。（:github:`71037`）

* ``<zephyr/mgmt/hawkbit.h>`` 已弃用，改为 ``<zephyr/mgmt/hawkbit/hawkbit.h>``。旧头文件将在未来版本中移除，且应避免其使用。hawkbit 自动处理程序已分离到 ``<zephyr/mgmt/hawkbit/autohandler.h>``。hawkbit 的配置部分现在在 ``<zephyr/mgmt/hawkbit/config.h>``。（:github:`71037`）

MCUmgr
======

* :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_BT` MCUmgr 传输的 ``MCUMGR_TRANSPORT_BT_AUTHEN`` Kconfig 选项已被 :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_BT_PERM_RW` Kconfig choice 替换。对蓝牙认证的要求现在由 :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_BT_PERM_RW_AUTHEN` Kconfig 选项指示。要移除对蓝牙认证的默认要求，需在项目配置中启用 :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_BT_PERM_RW` Kconfig 选项。

随机
======

* 在 TinyCrypt 库弃用后（:github:`79566`），CTR-DRBG 随机数生成器中 TinyCrypt 的使用已移除。从现在开始需 Mbed TLS 才能启用 :kconfig:option:`CONFIG_CTR_DRBG_CSPRNG_GENERATOR`。（:github:`79653`）

Shell
=====

* ``kernel threads`` 和 ``kernel stacks`` shell 命令已重命名为 ``kernel thread list`` 和 ``kernel thread stacks``

JWT（JSON Web Token）
===================

* 默认情况下，签名现在用 PSA Crypto API 为 RSA 和 ECDSA 计算。（:github:`78243`）向 PSA Crypto API 的转换是采用加密操作标准接口的一部分。（:github:`43712`）此外，在 TinyCrypt 库弃用后（:github:`79566`），JWT 子系统中 TinyCrypt 的使用已移除。（:github:`79653`）

* 添加以下新符号以允许同时指定签名算法和加密库：

  * :kconfig:option:`CONFIG_JWT_SIGN_RSA_PSA`（默认）用 PSA Crypto API 的 RSA 签名；
  * :kconfig:option:`CONFIG_JWT_SIGN_RSA_LEGACY` 用 Mbed TLS 的 RSA 签名；
  * :kconfig:option:`CONFIG_JWT_SIGN_ECDSA_PSA` 用 PSA Crypto API 的 ECDSA 签名。

  它们替换先前存在的 Kconfig ``CONFIG_JWT_SIGN_RSA`` 和 ``CONFIG_JWT_SIGN_ECDSA``。（:github:`79653`）
