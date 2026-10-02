:orphan:

.. _zephyr_4.0:

Zephyr 4.0.0
############

我们很高兴宣布 Zephyr 4.0.0 版本的发布。

本次发布的主要增强功能包括：

* **安全存储子系统**：
  新引入的 :ref:`安全存储 <secure_storage>` 子系统允许在*所有*板级目标上使用 PSA 安全存储 API 和 PSA 加密 API 中的持久密钥。它现在是为静态数据提供设备特定保护的标准方式。（:github:`76222`）

* **ZMS（Zephyr 内存存储）子系统**：
  :ref:`ZMS <zms_api>` 是一个新的键值存储子系统，兼容所有非易失性存储类型，包括传统 NOR 闪存以及支持免擦写的高级技术，如 RRAM 和 MRAM。

* **模拟比较器**：
  新增了用于模拟比较器的 :ref:`比较器 <comparator_api>` 设备驱动子系统，并附带 shell 支持。它支持通过设备树进行初始配置，通过厂商特定 API 进行运行时配置。最初支持的有 :dtcompatible:`nordic,nrf-comp`、:dtcompatible:`nordic,nrf-lpcomp` 和 :dtcompatible:`nxp,kinetis-acmp`。

* **步进电机**：
  得益于新的 :ref:`步进电机 <stepper_api>` 设备驱动子系统（同样附带 shell 支持），现在可以使用标准 API 与步进电机交互。最初实现的驱动包括简单的 :dtcompatible:`zephyr,gpio-steppers` 和复杂的无传感器、带堵转检测能力并集成斜坡控制器的 :dtcompatible:`adi,tmc5041`。

* **触觉反馈**：
  新的 :ref:`haptics_api` 设备驱动子系统允许统一访问触觉控制器，使用户能够为其应用程序添加触觉反馈。

* **多媒体功能**
  Zephyr 的音频和视频功能已扩展，支持新的图像传感器、视频接口、音频接口和编解码器。

* **Prometheus 库**：
  网络栈中新增了一个 `Prometheus`_ 指标库。它提供了一种通过 HTTP 向 Prometheus 客户端暴露指标的方式，便于与其他通常使用 Prometheus 监控的系统一起对 Zephyr 设备进行统一的远程监控。

* **文档改进**：
  对在线文档进行了多项增强，以改善内容发现和导航。这些包括新的 :ref:`交互式板级目录 <boards>` 和用于 :zephyr:code-sample-category:`代码示例 <samples>` 的交互式目录。

* **扩展的板级支持**：
  Zephyr 4.0 支持超过 60 块 :ref:`新开发板 <boards_added_in_zephyr_4_0>` 和 :ref:`盾牌 <shields_added_in_zephyr_4_0>`。

.. _`Prometheus`: https://prometheus.io/

从 Zephyr v3.7.0 迁移到 Zephyr v4.0.0 时所需或建议的更改概述可在单独的 :ref:`迁移指南 <migration_4.0>` 中找到。

以下章节按组件提供详细的更改列表。

安全漏洞相关
******************************
本次发布解决了以下 CVE：

更详细的信息可在以下地址找到：
https://docs.zephyrproject.org/latest/security/vulnerabilities.html

* :cve:`2024-8798`：截至 2024-11-22 处于保密期
* :cve:`2024-10395`：截至 2025-01-23 处于保密期
* :cve:`2024-11263` `Zephyr 项目问题跟踪器 GHSA-jjf3-7x72-pqm9
  <https://github.com/zephyrproject-rtos/zephyr/security/advisories/GHSA-jjf3-7x72-pqm9>`_

API 更改
***********

本次发布中移除的 API
============================

* 宏 ``K_THREAD_STACK_MEMBER`` 自 v3.5.0 起已弃用，现已移除。
  请改用 :c:macro:`K_KERNEL_STACK_MEMBER`。

* ``CBPRINTF_PACKAGE_COPY_*`` 宏自 Zephyr 3.5.0 起已弃用，现已移除。

* ``_ENUM_TOKEN`` 和 ``_ENUM_UPPER_TOKEN`` 宏自 Zephyr 2.7.0 起已弃用，
  不再生成。

* 移除了已弃用的架构级 CMSIS 头文件
  ``include/zephyr/arch/arm/cortex_a_r/cmsis.h`` 和
  ``include/zephyr/arch/arm/cortex_m/cmsis.h``。现在需要包含 ``cmsis_core.h``。

* 移除了已弃用的 ``ceiling_fraction`` 宏。现在需要使用 :c:macro:`DIV_ROUND_UP`。

* 移除了已弃用的头文件
  ``include/zephyr/random/rand32.h``。现在需要包含 ``random.h``。

* 已弃用的 ``EARLY``、``APPLICATION`` 和 ``SMP`` 初始化级别不能再用于设备。

* 移除了已弃用的 net_pkt 函数。

本次发布中弃用的
==========================

* 弃用了 ``net_buf_put()`` 和 ``net_buf_get()`` API 函数，改用
  :c:func:`k_fifo_put` 和 :c:func:`k_fifo_get`。

* ``kscan_api`` 子系统已标记为弃用。

* 弃用了 TinyCrypt shim 驱动 ``CONFIG_CRYPTO_TINYCRYPT_SHIM``。

* ``native_posix`` 已弃用，改用
  :zephyr:board:`native_sim<native_sim>`。

* ``include/zephyr/net/buf.h`` 已弃用，改用
  ``include/zephyr/net_buf.h>``。旧头文件将在未来版本中移除，应避免使用。

架构
*************

* ARC

* ARM

  * 在 Cortex-M（arm_mpu_v8）上添加了对设备内存属性的支持

* ARM64

  * 添加了对 :c:func:`arch_stack_walk` 的初始支持，仅支持通过 esf 展开
  * 为 ARM64 添加了 sys_arch_reboot() 支持

  * 添加了对按需分页的支持。

  * 添加了对可链接可加载扩展（LLEXT）的支持。

* RISC-V

  * 致命异常时的栈跟踪现在根据构建配置打印栈指针（sp）或帧指针（fp）的地址。

  * 当启用 :kconfig:option:`CONFIG_EXTRA_EXCEPTION_INFO` 时，异常栈帧（arch_esf）
    有一个额外的字段 ``csf``，指向致命错误时的被调用者保存寄存器，
    可在 :c:func:`k_sys_fatal_error_handler` 中通过 ``esf->csf`` 访问。

    * 对于选择 ``RISCV_SOC_HAS_ISR_STACKING`` 的 SoC，``SOC_ISR_STACKING_ESF_DECLARE``
      必须包含 ``csf`` 成员，否则构建将失败。

* Xtensa

* x86

  * 添加了对 :c:func:`arch_stack_walk` 的初始支持，仅支持通过 esf 展开

内核
******

* 设备树设备现在导出到 :ref:`llext`。

蓝牙
*********

* 音频

  * :c:func:`bt_tbs_client_register_cb` 现在支持多个监听器，并且现在可能返回错误。

  * 添加了在编解码器能力和编解码器配置中获取和设置辅助监听流值的 API：

    * :c:func:`bt_audio_codec_cfg_meta_get_assisted_listening_stream`
    * :c:func:`bt_audio_codec_cfg_meta_set_assisted_listening_stream`
    * :c:func:`bt_audio_codec_cap_meta_get_assisted_listening_stream`
    * :c:func:`bt_audio_codec_cap_meta_set_assisted_listening_stream`

  * 添加了在编解码器能力和编解码器配置中获取和设置广播名称的 API：

    * :c:func:`bt_audio_codec_cfg_meta_get_broadcast_name`
    * :c:func:`bt_audio_codec_cfg_meta_set_broadcast_name`
    * :c:func:`bt_audio_codec_cap_meta_get_broadcast_name`
    * :c:func:`bt_audio_codec_cap_meta_set_broadcast_name`

* 主机

  * 添加了 API :c:func:`bt_gatt_get_uatt_mtu` 用于获取给定连接的当前非增强 ATT MTU（实验性）。
  * 添加了 :kconfig:option:`CONFIG_BT_CONN_TX_NOTIFY_WQ`。
    该选项允许为连接 TX 通知处理使用独立的工作队列
    （:c:func:`bt_conn_tx_notify`），使蓝牙协议栈更加独立于系统工作队列。

  * 主机现在在 ATT 超时时与对端断开连接。

  * 如果作为参数传入的连接指针不为 NULL，则对 :c:func:`bt_conn_le_create` 和 :c:func:`bt_conn_le_create_synced` 添加警告。

  * 添加了 Kconfig 选项 :kconfig:option:`CONFIG_BT_CONN_CHECK_NULL_BEFORE_CREATE`，强制
    :c:func:`bt_conn_le_create` 和 :c:func:`bt_conn_le_create_synced` 在作为参数传入的连接指针不为 NULL 时返回错误。

  * 修复了 L2CAP 中的 ltk 派生问题
  * 为发现（BR）添加了监听器回调
  * 更正了 BR 绑定类型（SSP）
  * 添加了对不可绑定模式（SSP）的支持
  * 更改 SSP，使得当所需级别低于 L3 时不执行 MITM
  * 在拉取数据前添加了对接收缓冲区长度的检查（AVDTP）
  * 为 SSP 添加了对安全级别 4 的支持
  * 修复了 LE LTK 无法派生的问题
  * 添加了对多命令数据包（l2cap）的支持
  * 改进了 L2CAP 代码以在 CFG RSP 中设置标志
  * 改进了 L2CAP 代码以处理所有配置选项
  * 改进了 SSP 代码以在 ssp 配对完成区域清除配对标志
  * 改进了 SMP 代码以检查远端是否支持 CID 0x0007
  * 添加了对 SMP CT2 标志的支持
  * 改进了 SSP 代码，使得配对失败时调用正确的回调

* 控制器

  * 添加了对周期性广播同步传输（PAST）的支持，支持发送和接收两种角色。
    该选项可通过 :kconfig:option:`CONFIG_BT_CTLR_SYNC_TRANSFER_SENDER` 和
    :kconfig:option:`CONFIG_BT_CTLR_SYNC_TRANSFER_RECEIVER` 启用。

* HCI 驱动

* Mesh

  * 引入了 mesh 专用工作队列以提高 mesh 消息传输的可靠性。要恢复旧行为，请启用 :kconfig:option:`CONFIG_BT_MESH_WORKQ_SYS`。

板级与 SoC 支持
********************

* 添加了对以下 SoC 系列的支持：

  * 添加了对 ESP32-C2 和 ESP8684 SoC 的支持。
  * 添加了 STM32U0 系列，支持 GPIO、串行、I2C、DAC、ADC、闪存、PWM 和计数器驱动。
  * 添加了 STM32WB0 系列，支持 GPIO、串行、I2C、SPI、ADC、DMA 和闪存驱动。
  * 添加了 STM32U545xx SoC 变体。
  * 添加了 NXP i.MX93 的 Cortex-M33 核心
  * 添加了 NXP MCXW71、MCXC242、MCXA156、MCXN236、MCXC444、RT1180

* 对其他 SoC 系列做了以下更改：

  * NXP S32Z270：添加了对新硅片切割版本 2.0 的支持。请注意，之前的
    版本（1.0 和 1.1）不再受支持。
  * NXP s32k3：修复了 RAM 保持问题
  * NXP s32k1：从设备树获取系统时钟频率
    版本（1.0 和 1.1）不再受支持。
  * 添加了 ESP32 WROVER-E-N16R4 变体。
  * STM32H5：通过 STMicroelectronics OpenOCD 分支添加了对 OpenOCD 的支持。
  * MAX32：启用了 Segger RTT 和 SystemView 支持。
  * Silabs Series 2：在初始化期间从设备树使用振荡器、时钟和 DCDC 配置。
  * Silabs Series 2：为 SMU（安全管理单元）添加了初始化。
  * Silabs Series 2：使用 sleeptimer 作为默认 OS 定时器，而非 systick。
  * NXP i.MX8MP：启用了 IRQ_STEER 中断控制器。
  * NXP RWxxx：

      * 添加了对从低功耗模式唤醒的额外支持
      * RW61x：增大了主栈大小，以避免运行 BLE 时栈溢出
      * RW612：启用了 SCTIMER

  * NXP IMXRT：修复了由 Kconfig 默认值来源的 Flash 配置块错误重定位引起的 flexspi 启动问题
  * NXP RT11xx：启用了 FlexIO
  * NXP IMXRT116x：修复了总线时钟以与 MCUXpresso SDK 的设置保持一致
  * NXP mimxrt685：修复了时钟以启用 DMIC
  * NXP MCX N 系列：修复了 NXP LPSPI 原生片选在使用带 DMA 的同步 API 时的 bug
  * Nordic nRF54H：添加了对 FLPR（快速轻量级处理器）RISC-V CPU 的支持。

.. _boards_added_in_zephyr_4_0:

* 添加了对以下开发板的支持：

   * :zephyr:board:`01space ESP32C3 0.42 OLED <esp32c3_042_oled>`（``esp32c3_042_oled``）
   * :zephyr:board:`ADI MAX32662EVKIT <max32662evkit>`（``max32662evkit``）
   * :zephyr:board:`ADI MAX32666EVKIT <max32666evkit>`（``max32666evkit``）
   * :zephyr:board:`ADI MAX32666FTHR <max32666fthr>`（``max32666fthr``）
   * :zephyr:board:`ADI MAX32675EVKIT <max32675evkit>`（``max32675evkit``）
   * :zephyr:board:`ADI MAX32690FTHR <max32690fthr>`（``max32690fthr``）
   * :zephyr:board:`arduino_nicla_vision`（``arduino_nicla_vision``）
   * :zephyr:board:`BeagleBone AI-64 <beaglebone_ai64>`（``beaglebone_ai64``）
   * :zephyr:board:`BeaglePlay (CC1352) <beagleplay>`（``beagleplay``）
   * :zephyr:board:`DPTechnics Walter <walter>`（``walter``）
   * :zephyr:board:`Espressif ESP32-C3-DevKitC <esp32c3_devkitc>`（``esp32c3_devkitc``）
   * :zephyr:board:`Espressif ESP32-C3-DevKit-RUST <esp32c3_rust>`（``esp32c3_rust``）
   * :zephyr:board:`Espressif ESP32-S3-EYE <esp32s3_eye>`（``esp32s3_eye``）
   * :zephyr:board:`Espressif ESP8684-DevKitM <esp8684_devkitm>`（``esp8684_devkitm``）
   * :zephyr:board:`Gardena Smart Garden Radio Module <sgrm>`（``sgrm``）
   * :zephyr:board:`mikroe STM32 M4 Clicker <mikroe_stm32_m4_clicker>`（``mikroe_stm32_m4_clicker``）
   * :zephyr:board:`Nordic Semiconductor nRF54L15 DK <nrf54l15dk>`（``nrf54l15dk``）
   * Nordic Semiconductor nRF54L20 PDK（``nrf54l20pdk``）
   * :zephyr:board:`Nordic Semiconductor nRF7002 DK <nrf7002dk>`（``nrf7002dk``）
   * :zephyr:board:`Nuvoton NPCM400_EVB <npcm400_evb>`（``npcm400_evb``）
   * :zephyr:board:`NXP FRDM-MCXA156 <frdm_mcxa156>`（``frdm_mcxa156``）
   * :zephyr:board:`NXP FRDM-MCXC242 <frdm_mcxc242>`（``frdm_mcxc242``）
   * :zephyr:board:`NXP FRDM-MCXC444 <frdm_mcxc444>`（``frdm_mcxc444``）
   * :zephyr:board:`NXP FRDM-MCXN236 <frdm_mcxn236>`（``frdm_mcxn236``）
   * :zephyr:board:`NXP FRDM-MCXW71 <frdm_mcxw71>`（``frdm_mcxw71``）
   * :zephyr:board:`NXP i.MX95 EVK <imx95_evk>`（``imx95_evk``）
   * :zephyr:board:`NXP MIMXRT1180-EVK <mimxrt1180_evk>`（``mimxrt1180_evk``）
   * :zephyr:board:`PHYTEC phyBOARD-Nash i.MX93 <phyboard_nash>`（``phyboard_nash``）
   * :zephyr:board:`Renesas RA2A1 Evaluation Kit <ek_ra2a1>`（``ek_ra2a1``）
   * :zephyr:board:`Renesas RA4E2 Evaluation Kit <ek_ra4e2>`（``ek_ra4e2``）
   * :zephyr:board:`Renesas RA4M2 Evaluation Kit <ek_ra4m2>`（``ek_ra4m2``）
   * :zephyr:board:`Renesas RA4M3 Evaluation Kit <ek_ra4m3>`（``ek_ra4m3``）
   * :zephyr:board:`Renesas RA4W1 Evaluation Kit <ek_ra4w1>`（``ek_ra4w1``）
   * :zephyr:board:`Renesas RA6E2 Evaluation Kit <ek_ra6e2>`（``ek_ra6e2``）
   * :zephyr:board:`Renesas RA6M1 Evaluation Kit <ek_ra6m1>`（``ek_ra6m1``）
   * :zephyr:board:`Renesas RA6M2 Evaluation Kit <ek_ra6m2>`（``ek_ra6m2``）
   * :zephyr:board:`Renesas RA6M3 Evaluation Kit <ek_ra6m3>`（``ek_ra6m3``）
   * :zephyr:board:`Renesas RA6M4 Evaluation Kit <ek_ra6m4>`（``ek_ra6m4``）
   * :zephyr:board:`Renesas RA6M5 Evaluation Kit <ek_ra6m5>`（``ek_ra6m5``）
   * :zephyr:board:`Renesas RA8D1 Evaluation Kit <ek_ra8d1>`（``ek_ra8d1``）
   * :zephyr:board:`Renesas RA6E1 Fast Prototyping Board <fpb_ra6e1>`（``fpb_ra6e1``）
   * :zephyr:board:`Renesas RA6E2 Fast Prototyping Board <fpb_ra6e2>`（``fpb_ra6e2``）
   * :zephyr:board:`Renesas RA8T1 Motor Control Kit <mck_ra8t1>`（``mck_ra8t1``）
   * :zephyr:board:`Renode Cortex-R8 Virtual <cortex_r8_virtual>`（``cortex_r8_virtual``）
   * :zephyr:board:`Seeed XIAO ESP32-S3 Sense Variant <xiao_esp32s3>`：``xiao_esp32s3``。
   * :zephyr:board:`sensry.io Ganymed Break-Out-Board (BOB) <ganymed_bob>`（``ganymed_bob``）
   * :zephyr:board:`SiLabs SiM3U1xx 32-bit MCU USB Development Kit <sim3u1xx_dk>`（``sim3u1xx_dk``）
   * :zephyr:board:`SparkFun Thing Plus Matter <sparkfun_thing_plus_matter_mgm240p>`（``sparkfun_thing_plus_matter_mgm240p``）
   * :zephyr:board:`ST Nucleo G431KB <nucleo_g431kb>`（``nucleo_g431kb``）
   * :zephyr:board:`ST Nucleo H503RB <nucleo_h503rb>`（``nucleo_h503rb``）
   * :zephyr:board:`ST Nucleo H755ZI-Q <nucleo_h755zi_q>`（``nucleo_h755zi_q``）
   * :zephyr:board:`ST Nucleo U031R8 <nucleo_u031r8>`（``nucleo_u031r8``）
   * :zephyr:board:`ST Nucleo U083RC <nucleo_u083rc>`（``nucleo_u083rc``）
   * :zephyr:board:`ST Nucleo WB05KZ <nucleo_wb05kz>`（``nucleo_wb05kz``）
   * :zephyr:board:`ST Nucleo WB09KE <nucleo_wb09ke>`（``nucleo_wb09ke``）
   * :zephyr:board:`ST STM32U083C-DK <stm32u083c_dk>`（``stm32u083c_dk``）
   * :zephyr:board:`TI CC1352P7 LaunchPad <cc1352p7_lp>`（``cc1352p7_lp``）
   * :zephyr:board:`vcc-gnd YD-STM32H750VB <yd_stm32h750vb>`（``yd_stm32h750vb``）
   * :zephyr:board:`WeAct Studio STM32F405 Core Board V1.0 <weact_stm32f405_core>`（``weact_stm32f405_core``）
   * :zephyr:board:`WeAct Studio USB2CANFDV1 <usb2canfdv1>`（``usb2canfdv1``）
   * :zephyr:board:`Witte Technology Linum Board <linum>`（``linum``）


* 对以下开发板做了更改：

  * nrf54l15bsim 目标现在包含 AAR、CCM 和 ECB 外设的模型，以及许多
    其他改进。
  * 已停止支持 Google Kukui EC 开发板（``google_kukui``）。
  * STM32：弃用了通过 Kconfig 配置 MCO，改用通过设备树设置。
    参见 ``samples/boards/st/mco`` 示例。
  * STM32：STM32CubeProgrammer 现在是所有 STMicroelectronics STM32 开发板的默认运行器。
  * 移除了 ``nrf54l15pdk`` 开发板，请改用 :zephyr:board:`nrf54l15dk`。
  * PHYTEC：``mimx8mp_phyboard_pollux`` 已重命名为 :zephyr:board:`phyboard_pollux<phyboard_pollux>`，
    旧名称已标记为弃用。
  * PHYTEC：``mimx8mm_phyboard_polis`` 已重命名为 :zephyr:board:`phyboard_polis<phyboard_polis>`，
    旧名称已标记为弃用。
  * MPS3/AN547 的开发板限定符从以下更改：

    * ``mps3/an547`` 改为 ``mps3/corstone300/an547``（用于安全），
    * ``mps3/an547/ns`` 改为 ``mps3/corstone300/an547/ns``（用于非安全）。

  * 为 Thingy53 添加了将网络核心引脚转发到网络核心的 SPI 外设（默认禁用）
    包括引脚映射。
  * 为 NXP ``frdm_ke17z`` 和 ``frdm_ke17z512`` 添加了 uart、flexio pwm、flexio spi、看门狗、闪存、rtc、i2c、lpspi、edma、gpio、acmp、adc 和 lptmr 支持
  * 在 NXP 开发板上启用了 MCUmgr 支持
  * 在 NXP ``frdm_mcxw71`` 上启用了 MCUboot、FlexCAN、LPI2C、VREF、LPADC 和定时器（TPM、LPTMR、计数器、看门狗）
  * 在 NXP ``imx95_evk`` 上启用了 I2C、PWM
  * 在 NXP ``s32z2xxdc2`` 上启用了 FLEXCAN、LPI2C
  * 在 NXP ``s32z270dc2`` 上启用了 DSPI 和 EDMA3
  * 在 NXP ``imx8mm`` 和 ``imx8mn`` 上启用了 ENET 以太网
  * 为 NXP ``imx8qm`` 和 ``imx8qxp`` 的 DSP 核心添加了支持，以启用 openAMP 示例


.. _shields_added_in_zephyr_4_0:

* 添加了对以下盾牌的支持：

  * :ref:`ADI EVAL-ADXL362-ARDZ <eval_adxl362_ardz>`
  * :ref:`ADI EVAL-ADXL372-ARDZ <eval_adxl372_ardz>`
  * :ref:`Digilent Pmod ACL <pmod_acl>`
  * :ref:`MikroElektronika BLE TINY Click <mikroe_ble_tiny_click_shield>`
  * :ref:`Nordic SemiConductor nRF7002 EB <nrf7002eb>`
  * :ref:`Nordic SemiConductor nRF7002 EK <nrf7002ek>`
  * :ref:`ST X-NUCLEO-WB05KN1: BLE 扩展板 <x-nucleo-wb05kn1>`
  * :ref:`WeAct Studio MiniSTM32H7xx OV2640 摄像头传感器 <weact_ov2640_cam_module>`

构建系统与基础设施
*******************************

* 为 jlink、pyocd 和 linkserver 运行器的 west flash 命令添加了对 .elf 文件的支持。

* 将 pickled EDT 生成从 gen_defines.py 提取到 gen_deft.py。这将以下
  参数从 cmake 变量 ``EXTRA_GEN_DEFINES_ARGS`` 移动到 ``EXTRA_GEN_EDT_ARGS``：

   * ``--dts``
   * ``--dtc-flags``
   * ``--bindings-dirs``
   * ``--dts-out``
   * ``--edt-pickle-out``
   * ``--vendor-prefixes``
   * ``--edtlib-Werror``

* 在签名镜像时改为直接从构建系统调用 imgtool，而非调用
  ``west sign``。

* 在 sysbuild 中使用 ``SB_CONFIG_MCUBOOT_MODE`` 添加了对选择 MCUboot 运行模式的支持。

* 在构建系统中添加了对 RAM 加载 MCUboot 运行模式的支持，包括 sysbuild 支持。

* 为 Twister 添加了一个脚本参数，以启用硬件特定参数，例如系统特定的
  超时

文档
*************

* 添加了新的 :ref:`交互式开发板目录 <boards>`，允许用户按名称、架构、厂商或 SoC 等条件搜索开发板。
* 添加了新的 :zephyr:code-sample-category:`交互式代码示例目录 <samples>`，用于快速
  按名称和描述查找代码示例。
* 添加了 :rst:dir:`zephyr:board` 指令和 :rst:role:`zephyr:board` 角色，用于将 Sphinx 页面标记为
  开发板文档并从其他页面引用它们。大多数现有开发板文档页面
  已更新为使用此指令，完整迁移计划在下个版本进行。
* 添加了 :rst:dir:`zephyr:code-sample-category` 指令，用于在文档中描述和分组代码示例。
* 在 :ref:`设备树绑定 <devicetree_binding_index>` 文档中添加了指向与绑定兼容字符串匹配的驱动源代码（如果在 Zephyr 树中能找到）的链接。
* 在所有代码示例 README 页面中添加了一个按钮，允许直接在 GitHub 上浏览示例的源代码。
* 将 Zephyr C API 文档从主文档中移出。API 参考现在具有丰富的
  工具提示并链接到专用的 Doxygen 站点。
* 添加了两个新的构建命令 ``make html-live`` 和 ``make html-live-fast``，它们自动
  在本地托管生成的文档。当检测到输入 ``.rst`` 文件在文件系统中的更改时，
  它们还会自动重新构建并重新托管文档。

驱动与传感器
*******************

* ADC

  * 在 ESP32 中添加了正确的 ADC2 校准条目。
  * 修复了 ESP32-S3 中的校准方案。
  * STM32H7：通过实现 boost 模式添加了对更高采样频率的支持。
  * 添加了对 Renesas RA8 ADC 驱动的初始支持（:dtcompatible:`renesas,ra-adc`）
  * 为 Analog Devices MAX32 SoC 系列添加了驱动（:dtcompatible:`adi,max32-adc`）。
  * 添加了对 NXP S32 SAR_ADC 的支持（:dtcompatible:`nxp,s32-adc-sar`）
  * 添加了对 Ambiq Apollo3 系列的支持（:dtcompatible:`ambiq,adc`）。

* CAN

  * 添加了对 Renesas RA CANFD 的初始支持（:dtcompatible:`renesas,ra-canfd-global`、
    :dtcompatible:`renesas,ra-canfd`）
  * 为 S32Z27x 添加了 Flexcan 支持（:dtcompatible:`nxp,flexcan`、:dtcompatible:`nxp,flexcan-fd`）
  * 改进了 NXP S32 CANXL 错误报告（:dtcompatible:`nxp,s32-canxl`）

* 时钟控制

  * STM32 MCO（微控制器时钟输出）现在可在 STM32U5 系列上使用。
  * STM32 MCO 现在可以且应该通过设备树配置。
  * STM32：:kconfig:option:`CONFIG_CLOCK_CONTROL` 现在在家族级别默认启用，不再
    需要在开发板级别启用。
  * STM32H7：PLL FRACN 现在可以配置（参见 :dtcompatible:`st,stm32h7-pll-clock`）
  * 添加了对 Renesas RA 时钟控制驱动的初始支持（:dtcompatible:`renesas,ra-cgc-pclk`、
    :dtcompatible:`renesas,ra-cgc-pclk-block`、:dtcompatible:`renesas,ra-cgc-pll`、
    :dtcompatible:`renesas,ra-cgc-external-clock`、:dtcompatible:`renesas,ra-cgc-subclk`、
    :dtcompatible:`renesas,ra-cgc-pll-out`）
  * Silabs：添加了对 Series 2+ 时钟管理单元的支持（参见 :dtcompatible:`silabs,series-clock`）
  * 添加了对 Nordic nRF54H 系列时钟控制器的初始支持。

* 编解码器（音频）

  * 为 Wolfson WM8904 音频编解码器添加了驱动（:dtcompatible:`wolfson,wm8904`）

* 比较器

  * 引入了用 :kconfig:option:`CONFIG_COMPARATOR` 选择的比较器设备驱动子系统
  * 引入了用 :kconfig:option:`CONFIG_COMPARATOR_SHELL` 选择的比较器 shell 命令
  * 添加了对 Nordic nRF COMP 的支持（:dtcompatible:`nordic,nrf-comp`）
  * 添加了对 Nordic nRF LPCOMP 的支持（:dtcompatible:`nordic,nrf-lpcomp`）
  * 添加了对 NXP Kinetis ACMP 的支持（:dtcompatible:`nxp,kinetis-acmp`）

* 计数器

  * 添加了对 Renesas RA8 AGT 计数器驱动的初始支持（:dtcompatible:`renesas,ra-agt`）
  * 为 Analog Devices MAX32 SoC 系列添加了驱动（:dtcompatible:`adi,max32-counter`）。
  * 更新了 NXP counter_mcux_lptmr 驱动以支持 lptmr
    外设的多个实例。
  * 将 NXP S32 系统定时器模块驱动转换为原生 Zephyr 代码
  * 为 NXP nxp_sys_timer 添加了晚和短相对报警区域的支持（:dtcompatible:`nxp,s32-sys-timer`）

* 加密

  * 添加了对 STM32L4 AES 的支持。

* DAC

  * DAC API 现在支持将通道路径指定为内部。已在 STM32 驱动中添加支持。

* 磁盘

  * STM32F7 SDMMC 驱动现在支持使用 DMA。
  * STM32 内存控制器驱动现在支持 STM32H5 的 FMC。
  * SDMMC 子系统驱动现在会在磁盘
    去初始化时关闭 SD 卡的电源

* 显示

  * NXP ELCDIF 驱动现在支持使用 PXP 沿水平
    或垂直轴翻转图像。使用
    :kconfig:option:`CONFIG_MCUX_ELCDIF_PXP_FLIP_DIRECTION` 设置所需的
    翻转。
  * ST7789V 驱动现在支持 BGR565，通过
    :kconfig:option:`CONFIG_ST7789V_BGR565` 启用。
  * 为 SSD1327 OLED 显示控制器添加了驱动（:dtcompatible:`solomon,ssd1327fb`）。
  * 为 SSD1322 OLED 显示控制器添加了驱动（:dtcompatible:`solomon,ssd1322`）。
  * 为 IST3931 单色显示控制器添加了驱动（:dtcompatible:`istech,ist3931`）。

* DMA

  * 为 Analog Devices MAX32 SoC 系列添加了驱动（:dtcompatible:`adi,max32-dma`）。
  * 为 NXP dma_mcux_pxp 驱动添加了翻转功能（:dtcompatible:`nxp,pxp`）
  * 为 NXP EMDA 驱动（:dtcompatible:`nxp,edma`）添加了对 eDMAv5 和循环模式的支持（:github:`80584`）

* EEPROM

  * 添加了对使用 EEPROM 模拟器与嵌入式 C 标准库一起使用的支持
    （:dtcompatible:`zephyr,sim-eeprom`）。

* 熵

  * 添加了对 Renesas RA8 熵驱动的初始支持（:dtcompatible:`renesas,ra-rsip-e51a-trng`）
  * 为 Analog Devices MAX32 SoC 系列添加了驱动（:dtcompatible:`adi,max32-trng`）。

* 以太网

  * 在以太网驱动 api 中添加了 :c:func:`get_phy` 函数，返回与网络接口关联的 phy 设备。
  * 在以太网硬件能力 api 中添加了 2.5G 和 5G 链路速度。
  * 在 :c:func:`net_eth_get_hw_capabilities` 中添加了对空 api 指针的检查，修复了 netusb 崩溃。
  * 添加了 synopsis dwc_xgmac 以太网驱动。
  * 添加了 NXP iMX NETC 驱动。
  * Adin2111

    * 修复了使用通用 spi 协议时导致双重 RX 缓冲区读取的 bug。
    * 修复了 OA 读取失败时基本线程终止的问题。
    * 跳过 adin1110 的端口 2 检查，因为它不适用，因为没有端口 2。
  * ENC28J60

    * 添加了对 ``zephyr,random-mac-address`` 属性的支持。
    * 修复了初始化时影响载波状态的中断服务与 L2 初始化之间的竞态条件。
  * ENC424j600：添加了在运行时通过 net 管理 api 更改 mac 地址的能力。
  * ESP32：添加了从 DT 配置中断的功能。
  * Lan865x

    * 为 IPv6 启用所有多播 MAC 地址。现在可以接收所有多播 mac 地址，
      从而正确处理 IPv6 邻居发现协议。
    * 修复了设置 mac 地址或混杂模式时传输停止的问题。
  * LiteX

    * 将 ``compatible`` 从 ``litex,eth0`` 重命名为 :dtcompatible:`litex,liteeth`。
    * 添加了对 liteX 以太网驱动多个实例的支持。
    * 为 liteX 以太网驱动添加了对 VLAN 的支持。
    * 添加了 phy 支持。
  * Native_posix

    * 实现了从命令行获取接口名称的功能。
    * 现在在创建接口出错时在错误消息中打印错误编号。
  * NXP ENET_QOS：修复了对 ``zephyr,random-mac-address`` 属性的检查。
  * NXP ENET：

    * 修复了熔丝 MAC 地址初始化代码。
    * 修复了处理带时间戳帧的 tx 错误的代码路径。
    * 修复了初始化期间网络载波状态的竞态条件。
  * NXP S32：添加了用于启用 VLAN 混杂和未标记以及启用 SI 消息中断的配置。
  * STM32

    * 驱动现在可以配置为使用抢占式 RX 线程优先级，这在
      高网络流量负载情况下可能有用（减少抖动）。
    * 添加了对 DT 定义的 mdio 的支持。
    * 修复了某些情况下网络断开连接后发生的总线错误。
  * TC6：将读取块合并为连续的 net 缓冲区。这修复了 IPv6 邻居发现协议，
    因为 64 字节不足以容纳所有头部。
  * PHY 驱动更改

    * 添加了 Qualcomm AR8031 phy 驱动。
    * 添加了 DP83825 phy 驱动。
    * PHY_MII

      * 修复了通用 phy_mii 驱动未使用来自设备树的 ``no-reset`` 属性值的问题。
      * 从 phy_mii 驱动的日志输出中移除了多余的空行。
    * KSZ8081

      * 修复了初始化期间不必要的长复位时间。
      * 移除了每次链路配置时不必要的复位，该复位会阻塞系统工作队列
      * 修复了与 strap-in 覆盖位相关的问题。


* 闪存

  * 修复了 SPI NOR 驱动问题，其中 wp、hold 和 reset 引脚在启用运行时 SFDP 时
    从设备 tee 错误初始化（:github:`80383`）
  * 更新了所有 Espressif 的 SoC 驱动初始化以允许新芯片组和八线闪存支持。
  * 在 SPI NOR 驱动配置中添加了 :kconfig:option:`CONFIG_SPI_NOR_ACTIVE_DWELL_MS`，
    允许设置在触发深度掉电（DPD）之前驱动等待的时间。
    该选项取代 ``CONFIG_SPI_NOR_IDLE_IN_DPD``，旨在减少不必要的电源
    状态变化和其他操作之间的 SPI 传输，特别是在对 SPI NOR 设备
    进行突发类型访问时。
  * 添加了 :kconfig:option:`CONFIG_SPI_NOR_INIT_PRIORITY` 以允许选择 SPI NOR 驱动初始化优先级。
  * flash API 已扩展，增加了 :c:func:`flash_copy` 实用函数，允许在
    两个 Flash API 设备之间执行直接数据复制。
  * 修复了 Flash 模拟器问题，其中偏移量被假定为绝对值而非相对于
    设备基地址（:github:`79082`）。
  * 扩展了 STM32 OSPI 驱动以支持 QUAL、DUAL 和 SPI 模式。此外，添加了
    自定义写入和 SFDP:BFP 操作码的支持。
  * 添加了从 Cortex-M4 核心运行 STM32H7 闪存驱动的可能性。
  * 为 STM32F7 SoC 实现了读取保护处理（RDP 级别）。
  * 添加了对 Renesas RA8 Flash 控制器驱动的初始支持（:dtcompatible:`renesas,ra-flash-hp-controller`）
  * 为 Analog Devices MAX32 SoC 系列添加了驱动（:dtcompatible:`adi,max32-flash-controller`）。
  * 为 NXP 的 MCUX Flexspi 驱动添加了对 W25Q512JV 和 W25Q512NW-IQ/IN 的支持
  * 为准确性将绑定 :dtcompatible:`nxp,iap-msf1` 重命名为 :dtcompatible:`nxp,msf1`

* GPIO

  * tle9104：通过设置属性 ``parallel-out12`` 和
    ``parallel-out34`` 添加了对并行输出模式的支持。
  * 将 NXP S32 SIUL2 驱动转换为原生 Zephyr 代码
  * 将 NXP 唤醒驱动转换为原生 Zephyr 代码

* 触觉反馈

  * 引入了用 :kconfig:option:`CONFIG_HAPTICS` 选择的触觉反馈设备驱动子系统
  * 添加了对 TI DRV2605 触觉驱动 IC 的支持（:dtcompatible:`ti,drv2605`）
  * 为 DRV2605 触觉驱动添加了触发 ROM 事件的示例（:zephyr:code-sample:`drv2605`）

* I2C

  * 添加了对 Renesas RA8 I2C 驱动的初始支持（:dtcompatible:`renesas,ra-iic`）

* I2S

  * 添加了对 ESP32-S3 和 ESP32-C3 驱动的支持。

* I3C

  * 添加了对初始化期间 SETAASA 优化的支持。在 ``i3c-devices.yaml`` 中添加了
    ``supports-setaasa`` 属性。
  * 添加了向支持在总线上作为次要控制器运行的任何设备发送 DEFTGTS 的功能。
  * 在 :c:func:`i3c_device_basic_info_get` 中添加了获取 GETMXDS 的功能（如果 BCR mxds
    位已设置）。
  * 添加了用于发送 ENTTM、VENDOR、DEFTGTS、SETAASA、
    GETMXDS、SETBUSCON、RSTACT DC、ENTAS0、ENTAS1、ENTAS2 和 ENTAS3 CCC 的辅助函数。
  * 添加了用于发送 ENTTM、VENDOR、DEFTGTS、SETAASA、
    GETMXDS、SETBUSCON、RSTACT DC、ENTAS0、ENTAS1、ENTAS2 和 ENTAS3 CCC 的 shell 命令。
  * 添加了用于设置 I3C 速度、发送 HDR-DDR、拉高 IBI、
    启用 IBI、禁用 IBI 和扫描 I2C 地址的 shell 命令。
  * :c:func:`i3c_ccc_do_setdasa` 已修改为现在要求指定分配的
    动态地址，而非在函数内部确定动态地址。
  * :c:func:`i3c_determine_default_addr` 已移除
  * ``attach_i3c_device`` 现在不再要求将附加地址作为参数。现在
    由驱动从 ``i3c_device_desc`` 确定附加地址。

* 输入

  * 新功能：:dtcompatible:`zephyr,input-double-tap`。

  * 新驱动：:dtcompatible:`ilitek,ili2132a`。

  * 为所有键盘矩阵驱动添加了电源管理支持，为 :dtcompatible:`gpio-keys` 添加了
    ``no-disconnect`` 属性，以便可与不支持引脚
    断开的 GPIO 驱动的电源管理一起使用。

  * 为触摸屏通用属性和功能
    （屏幕尺寸、反转、xy 交换）添加了新框架。

  * 修复了损坏的 ESP32 输入触摸传感器驱动。

  * gt911：
    * 修复了 INT 引脚在探测期间始终设置的问题，以允许正确初始化
    * 修复了触摸点数组的 OOB 缓冲区写入
    * 添加了对多点触摸事件的支持

* 中断

  * 使用正确的 IRQ 标志和优先级更新了 ESP32 系列中断分配器。
  * 实现了为 Arm GIC 设置待处理中断的函数
  * 添加了一个安全配置选项，使多个操作系统可以共享同一个 GIC 并避免重新配置
    分发器

* LED

  * lp5562：添加了 ``enable-gpios`` 属性以描述 lp5562 的 EN/VCC GPIO。

  * lp5569：添加了 ``charge-pump-mode`` 属性以配置 lp5569 的电荷泵。

  * lp5569：添加了 ``enable-gpios`` 属性以描述 lp5569 的 EN/PWM GPIO。

  * LED 代码示例已整合到 :zephyr_file:`samples/drivers/led` 目录下。

* LED 灯带

  * 更新了 ws2812 GPIO 驱动以支持动态总线时序

* 邮箱

  * 添加了对 ESP32 和 ESP32-S3 SoC 的驱动支持。

* MDIO

  * 添加了 litex MDIO 驱动。
  * 为 stm32 mdio 添加了对 mdio shell 的支持。
  * 为 dwc_xgmac synopsis 以太网添加了 mdio 驱动。
  * 添加了 NXP IMX NETC mdio 驱动。
  * NXP ENET MDIO：通过保持 mdio 中断始终启用修复了不一致的行为。

* MEMC

  * 为使用 NXP FLEXSPI 的 APS6404L PSRAM 添加了驱动

* MFD

* 调制解调器

  * 添加了对 U-Blox LARA-R6 调制解调器的支持。
  * 添加了在初始化期间设置调制解调器 UART 波特率的支持。

* MIPI-DBI

  * 添加了 bitbang MIPI-DBI 驱动，支持 8080 和 6800 模式
    （:dtcompatible:`zephyr,mipi-dbi-bitbang`）。
  * 添加了对 STM32 FMC 内存控制器的支持（:dtcompatible:`st,stm32-fmc-mipi-dbi`）。
  * 为 NXP LCDIC 控制器添加了对 8080 模式的支持（:dtcompatible:`nxp,lcdic`）。
  * 修复了 NXP LCD 控制器的复位延迟计算（:dtcompatible:`nxp,lcdic`）

* MIPI-CSI

  * 改进了 NXP CSI 和 MIPI_CSI2Rx 驱动以支持可变帧率

* 引脚控制

  * 添加了对 Microchip MEC5 的支持
  * 为 NXP i.MX 添加了基于 SCMI 的驱动
  * 添加了对 i.MX93 M33 核心的支持
  * 添加了对 ESP32C2 的支持
  * STM32：:kconfig:option:`CONFIG_PINCTRL` 现在由需要它的驱动选择，
    不再需要在开发板级别启用。

* PWM

  * rpi_pico：驱动现在自适应地配置分频比。
  * 添加了对 Renesas RA8 PWM 驱动的初始支持（:dtcompatible:`renesas,ra8-pwm`）
  * 为 Analog Devices MAX32 SoC 系列添加了驱动（:dtcompatible:`adi,max32-pwm`）。
  * 修复了 NXP TPM 驱动在不具备合并通道能力的变体上的构建问题

* 稳压器

  * 将 CP9314 驱动升级到 B1 硅片修订版
  * 为 MPS MPM54304 添加了基本驱动

* RTC

  * STM32：HSE 现在可用作域时钟。
  * 添加了 NXP IRTC 驱动。

* RTIO

* SAI

  * 改进了 NXP 的 SAI 驱动，使其在 DT 中未提供时钟时使用默认时钟
  * 修复了 NXP SAI 驱动中导致 FIFO 下溢和上溢时崩溃的 bug
  * 修复了在初始化期间重置 NXP ESAI（不必要的）的 bug
  * 为 NXP 的 SAI 驱动添加了对 PM 操作的支持

* SDHC

  * 添加了对 ESP32-S3 驱动的支持。
  * SPI SDHC 驱动现在正确处理具有运行时 PM 支持的 SPI 设备
  * 改进了 NXP 的 imx SDHC 驱动，使其在未提供检测方法时假定卡片存在

* 传感器

  * 通用

    * 现有的 Microchip MCP9808 温度传感器驱动已转换并重命名，
      以支持所有 JEDEC JC 42.4 兼容的温度传感器。它现在使用
      :dtcompatible:`jedec,jc-42.4-temp` 兼容字符串，而非 ``microchip,mcp9808``
      字符串。
    * 为 NTC 热敏电阻驱动添加了对基于 VDD 的 ADC 参考的支持。
    * 添加了 Avago APDS9253（:dtcompatible:`avago,apds9253`）和 APDS9306
      （:dtcompatible:`avago,apds9306`）环境光传感器驱动。
    * 添加了增益和分辨率属性（:c:enum:`SENSOR_ATTR_GAIN` 和
      :c:enum:`SENSOR_ATTR_RESOLUTION`）。

  * ADI

    * 为 ADXL345、ADXL362 和 ADXL372 加速度计驱动添加 RTIO 流支持。

  * Bosch

    * 将 BMP390 合并到 BMP388。
    * 为 BMM150 和 BME680 驱动添加了对电源域的支持。
    * 添加了 BMP180 压力传感器驱动（:dtcompatible:`bosch,bmp180`）。

  * Memsic

    * 添加了 MMC56X3 磁力计和温度传感器驱动（:dtcompatible:`memsic,mmc56x3`）。

  * NXP

    * 添加了 P3T1755 数字温度传感器驱动（:dtcompatible:`nxp,p3t1755`）。
    * 添加了 FXLS8974 加速度计驱动（:dtcompatible:`nxp,fxls8974`）。

  * ST

    * 将驱动与 stmemsc HAL i/f v2.6 对齐。
    * 添加了 LSM9DS1 加速度计/陀螺仪/磁力计传感器驱动（:dtcompatible:`st,lsm9ds1`）。

  * TDK

    * 为 ICM42670 添加了对 I2C 总线的支持。

  * TI

    * 在现有的 INA230 驱动中添加了对 INA236 的支持。
    * 在现有的 TMAG5273 驱动中添加了对 TMAG3001 的支持。
    * 添加了 TMP1075 温度传感器驱动（:dtcompatible:`ti,tmp1075`）。

  * Vishay

    * 为 VCNL36825T 驱动添加了触发能力。

  * WE

    * 添加了 Würth Elektronik HIDS-2525020210002
      :dtcompatible:`we,wsen-hids-2525020210002` 湿度传感器驱动。
    * 为触发器添加了通用示例

* 串行

  * LiteX：将 ``compatible`` 从 ``litex,uart0`` 重命名为 :dtcompatible:`litex,uart`。
  * Nordic：移除了 ``CONFIG_UART_n_GPIO_MANAGEMENT`` Kconfig 选项（其中 n 是实例
    索引），这些选项在引入 pinctrl 驱动后已无用途。
  * NS16550：添加了对 Synopsys Designware 8250 UART 的支持。
  * Renesas：添加了对 SCI UART 的支持。
  * Sensry：为 Ganymed SY1XX 添加了 UART 支持。

* SPI

  * 添加了对 Renesas RA8 SPI 驱动的初始支持（:dtcompatible:`renesas,ra8-spi-b`）
  * 为 Analog Devices MAX32 驱动添加了 RTIO 支持。
  * Silabs：添加了对 EUSART 的支持（:dtcompatible:`silabs,gecko-spi-eusart`）

* 步进电机

  * 引入了用 :kconfig:option:`CONFIG_STEPPER` 选择的步进电机控制器设备驱动子系统
  * 引入了用 :kconfig:option:`CONFIG_STEPPER_SHELL` 控制
    步进电机的步进电机 shell 命令
  * 添加了对 ADI TMC5041 的支持（:dtcompatible:`adi,tmc5041`）
  * 添加了对 gpio-stepper-controller 的支持（:dtcompatible:`zephyr,gpio-steppers`）
  * 添加了步进电机 api 测试套件
  * 添加了步进电机 shell 测试套件

* 定时器

  * Silabs：添加了对 Sleeptimer 的支持（:dtcompatible:`silabs,gecko-stimer`）

* USB

  * 添加了对 STM32U59x/STM32U5Ax SoC 变体的 USB HS 支持。
  * 增强了 DWC2 UDC 驱动
  * 为 Smartbond、NuMaker USBD 和 RP2040 设备控制器添加了 UDC 驱动
  * 在 NXP USB 驱动（UDC）中启用了 SoF
  * 在 NXP EHCI USB 驱动中启用了缓存维护

* 视频

  * 引入了控制帧率的 API
  * 引入了用于通过视频缓冲区字段 ``line_offset`` 进行部分帧传输的 API
  * 引入了用于 :ref:`多堆 <memory_management_shared_multi_heap>` 视频缓冲区分配的 API，
    通过 :kconfig:option:`CONFIG_VIDEO_BUFFER_USE_SHARED_MULTI_HEAP`
  * 在 ``video-interfaces.yaml`` 中引入了通用视频链接属性的绑定。向
    新绑定的迁移在 :github:`80514` 中跟踪
  * 引入了缺失的 :kconfig:option:`CONFIG_VIDEO_LOG_LEVEL`
  * 添加了捕获视频并使用 LVGL 显示的示例
    （:zephyr:code-sample:`video-capture-to-lvgl`）
  * 添加了自动测试以检查彩条图案的正确性
  * 添加了对 GalaxyCore GC2145 图像传感器的支持（:dtcompatible:`galaxycore,gc2145`）
  * 添加了对 ESP32-S3 LCD-CAM 接口的支持（:dtcompatible:`espressif,esp32-lcd-cam`）
  * 添加了对 NXP MCUX SMARTDMA 接口的支持（:dtcompatible:`nxp,smartdma`）
  * 为更多 OmniVision OV2640 控制添加了支持（:dtcompatible:`ovti,ov2640`）
  * 为更多 OmniVision OV5640 控制添加了支持（:dtcompatible:`ovti,ov5640`）
  * STM32：实现了 :c:func:`video_get_ctrl` 和 :c:func:`video_set_ctrl` API。
  * 移除了 NXP RT10xx 平台上摄像头管线的初始化顺序循环依赖
    （:github:`80304`）
  * 添加了基于 NXP smartdma 的视频驱动（:dtcompatible:`nxp,video-smartdma`）
  * 添加了帧间隔 API 以支持可变帧率（video_sw_generator.c）
  * 为 OV5640 驱动添加了图像控制

* W1

  * 为 Analog Devices MAX32 SoC 系列添加了 1-Wire 主驱动（:dtcompatible:`adi,max32-w1`）

* 看门狗

  * 为 Analog Devices MAX32 SoC 系列添加了驱动（:dtcompatible:`adi,max32-watchdog`）。
  * 将 NXP S32 软件看门狗定时器驱动转换为原生 Zephyr 代码

* Wi-Fi

  * 添加了对 Wi-Fi Easy Connect（DPP）的支持。
  * 添加了对 Wi-Fi 凭据库的支持。
  * 为站点添加了企业支持。
  * 为网络示例添加了 Wi-Fi 代码片段支持。
  * 为各种 Wi-Fi 配置组合添加了构建测试。
  * 为 Wi-Fi shell 添加了监管域支持。
  * 为 Wi-Fi shell 添加了 WPS 支持。
  * 在 Wi-Fi shell 中添加了对 802.11r 连接命令的使用。
  * 在 hostap 状态消息中添加当前 PHY 速率。
  * 允许用户在 Wi-Fi shell 中重置 Wi-Fi 统计信息。
  * 在 Wi-Fi shell 中显示 RTS 阈值。
  * 修复了扫描结果中 SSID 数组长度大小。
  * 修复了 "wifi ap config" 命令使用 STA 接口而非 SAP 接口的问题。
  * 修复了 hostap 在执行断开连接时的内存泄漏。
  * 修复了 Wi-Fi shell 中 AP 和 STA 模式下的频段设置。
  * 修复了 Wi-Fi 6GHz 中正确的信道扫描范围。
  * 修复了 Wi-Fi shell 中扫描结果的打印。
  * 增大了 Wi-Fi shell 示例的主栈和 shell 栈大小。
  * 将 Wi-Fi shell 中已连接 STA 的最大数量增加到 8。
  * 将 AP 和 STA Wi-Fi 示例迁移到 samples/net/wifi 目录。
  * 将 Wi-Fi 测试与网络测试一起运行。
  * 更新了 ESP32 Wi-Fi 驱动以反映实际协商的 PHY 模式。
  * 添加了对 ESP32-C2 Wi-Fi 的支持。
  * 添加了对 ESP32 驱动 APSTA 的支持。
  * 添加了对 NXP RW612 驱动的支持。
  * 添加了 nRF70 Wi-Fi 驱动。

网络
**********

* 802.15.4：

  * 实现了对不带关联位信标的支持。
  * 实现了对信标负载的支持。
  * 修复了在解密帧时 LL 地址字节序被两次交换的 bug。
  * 修复了检查目标地址时缺失的上下文锁释放。
  * 改进了 6LoWPAN 分片中的错误日志记录。
  * 改进了 802.15.4 管理命令中的错误日志记录。

* ARP：

  * 修复了 IPv4 地址冲突检测期间的 ARP 探测验证。

* CoAP：

  * 添加了新 API :c:func:`coap_rst_init` 以简化创建 RST 回复。
  * 在 CoAP 客户端中实现了对未知查询用 CoAP RST 响应回复。
  * 添加了对 ACK 随机因子参数的运行时配置的支持。
  * 添加了对 No Response CoAP 选项的支持。
  * 添加了演示用 GET 请求下载资源的新示例。
  * 修复了 CoAP 客户端中接收的 CoAP RST 回复的处理。
  * 修复了 CoAP 客户端中向应用程序报告套接字错误的问题。
  * 修复了 CoAP 客户端中响应重传的处理。
  * 修复了 CoAP 块编号被限制为 ``uint8_t`` 的 bug。
  * CoAP 客户端块传输支持中的各种修复。
  * 改进了 CoAP 客户端中对截断数据报的处理。
  * 改进了 CoAP 客户端的线程安全性。
  * 修复了某些内部函数中缺失的 ``static`` 关键字。
  * CoAP 客户端中的其他各种小修复。

* DHCPv4：

  * 添加了对解析从 DHCP 服务器接收的多个 DNS 服务器的支持。
  * 在 DHCPv4 服务器中添加了对 DNS Server 选项的支持。
  * 在 DHCPv4 服务器中添加了对 Router 选项的支持。
  * 添加了对允许在 DHCPv4 服务器中分配自定义地址的应用程序回调的支持。
  * 修复了 DHCPv4 客户端中 DNS 服务器列表的分配。
  * 修复了系统工作队列可能被 DHCPv4 客户端无限阻塞的 bug。

* DHCPv6：

  * 修复了系统工作队列可能被 DHCPv6 客户端无限阻塞的 bug。

* DNS/mDNS/LLMNR：

  * 添加了对收集 DNS 统计信息的支持。
  * 在 :c:func:`zsock_gai_strerror` 中添加了对更多错误代码的支持。
  * 修复了用大写字母编码的 DNS 响应的处理。
  * 修复了 DNS 分发器在多个网络接口上的操作。
  * 修复了查询计数等于 0 的 mDNS 查询报告错误的问题。
  * DNS/mDNS 实现中的其他各种小修复。

* 以太网：

* gPTP/PTP：

  * 修复了秒溢出/下溢的处理。
  * 修复了带偏移的 PTP 时钟调整。

* HTTP：

  * 添加了对由应用程序指定响应头和响应代码的支持。
  * 在 HTTP 服务器示例中添加了对 netusb 的支持。
  * 添加了对从应用程序回调访问 HTTP 请求头的支持。
  * 在 HTTP 服务器中添加了对通过 IPv6 套接字处理 IPv4 连接的支持。
  * 添加了在未指定本地主机的情况下创建 HTTP 服务器实例的支持。
  * 为 HTTP 客户端和服务器
    示例添加了支持 HTTP over IEEE 802.15.4 的 overlay。
  * 在 HTTP 服务器中添加了对静态文件系统资源的支持。
  * 修复了资源上传中止时 HTTP 服务器示例中的断言。
  * 重构了动态资源回调格式，以更容易处理短
    请求/回复。
  * 修复了 HTTP 服务器示例中可能的忙循环。
  * 修复了 HTTP 服务器中可能的错误 HTTP 头匹配。
  * 重构了 HTTP 服务器示例，以更好地演示服务器使用场景。
  * 修复了在同一连接上处理多个 HTTP/1 请求。
  * 改进了 HTTP 服务器测试覆盖范围。
  * HTTP 服务器中的其他各种小修复。

* IPv4：

  * 改进了 IGMP 测试覆盖范围。
  * 修复了启用 IGMPv3 时 IGMPv2 查询的处理。
  * 修复了原生 IPv4 选项的 :kconfig:option:`CONFIG_NET_NATIVE_IPV4` 依赖关系。
  * 修复了 :c:func:`send_ipv4_fragment` 中的 net_pkt 泄漏。
  * 修复了 send_ipv4_fragment 中的 tx_pkts 堆泄漏

* IPv6：

  * 为多播监听器发现 API 添加了公共头文件。
  * 添加了新的 :c:func:`net_ipv6_addr_prefix_mask` API 函数。
  * 使 IPv6 路由器请求超时可配置。
  * 修复了同时启用路由和 VLAN 支持时无限的 IPv6 数据包循环。
  * 修复了丢弃 NS 数据包时不必要的错误日志记录。
  * 修复了接受传入 DAD NS 消息的问题。
  * 改进 IPv6 路由的各种修复。
  * 为 IPv6-prepare 添加了 onlink 和转发检查

* LwM2M：

  * 位置对象：可选资源海拔、半径和速度现在可以
    按照位置对象规范可选使用。这些资源的
    用户现在需要提供读取缓冲区。
  * 在 DTLS 密码列表中添加 TLS_ECDHE_ECDSA_WITH_AES_128_CCM_8。
  * 添加了列出资源的 LwM2M shell 命令。
  * 添加了列出观察的 LwM2M shell 命令。
  * 添加了对接受作为整数解码的 SenML-CBOR 浮点数的支持。
  * 在使用证书且 URI 包含有效名称时，
    添加了对 X509 主机名验证的支持。
  * 使用 zcbor 0.9.0 为 lwm2m_senml_cbor 重新生成了生成的代码文件。
  * 改进了 LwM2M 引擎的线程安全性。
  * 修复了复合操作的块传输问题。
  * 修复了引导发现期间的 enabler 版本报告。
  * 从 LwM2M 客户端示例中移除了不需要的 Security 对象实例。
  * 修复了 U16 资源的缓冲区大小检查。
  * 移除了已弃用的 API 和配置。
  * 可选位置对象资源海拔、半径和速度现在可以
    按照位置对象规范可选使用。这些资源的
    用户现在需要提供读取缓冲区。
  * 修复了注册更新成功时重试计数器未重置的问题。
  * 修复了 REGISTRATION_TIMEOUT 事件未在注册
    错误时始终发出的问题。
  * 修复了 LwM2M 公共头文件中的 c++ 支持。
  * 修复了 DISCONNECTED 事件未在使用时始终发出的 bug。

* 杂项：

  * 添加了对网络数据包分配统计信息的支持。
  * 添加了实现 Prometheus 监控支持的新库。
  * 为 Echo Server 示例添加了 USB CDC NCM 支持。
  * 为捕获接口添加了数据包丢弃统计信息。
  * 添加了新的 :c:func:`net_hostname_set_postfix_str` API 函数，用于以
    非十六进制格式设置主机名后缀。
  * 在公共网络头文件中添加了 API 版本信息。
  * 实现了可选的周期性 SNTP 时间重新同步。
  * 改进了启动/停止虚拟接口时的错误报告。
  * 修复了使用可变大小缓冲区时数据包捕获库的构建错误。
  * 修复了禁用 IPv4 或 IPv6 时数据包捕获库的构建错误。
  * 修复了某些
    配置下 net 库中 CMake 关于缺失源的警告。
  * 修复了启用网络与 SystemView Tracing 时的编译问题。
  * 从 telnet 示例中移除了冗余的 DHCPv4 代码。
  * 修复了禁用 IPv6 时 Echo Client 示例中的构建警告。
  * 扩展了网络跟踪支持并添加了文档页面
    （:ref:`network_tracing`）。
  * 将网络缓冲区实现从 net 子系统移出到 lib 目录
  * 移除了 ``wpansub`` 示例。

* MQTT：

  * 更新了 mqtt_publisher 示例中关于 Mosquitto broker
    配置的信息。
  * 更新了 MQTT 测试使其自包含，不再需要外部 broker。
  * 优化了 MQTT 编码器/解码器中的缓冲区处理。

* 网络上下文：

  * 修复了启用 :kconfig:option:`CONFIG_NET_IPV4_MAPPING_TO_IPV6` 选项时
    使用 :c:func:`sendmsg` 设置 IPv4 目标地址的问题。
  * 修复了 :c:func:`net_context_bind` 中可能的非对齐内存访问。
  * 修复了读取 V6ONLY 选项时缺失的 NULL 指针检查。

* 网络接口：

  * 添加了新的 :c:func:`net_if_ipv4_get_gw` API 函数。
  * 修复了 VLAN 接口的校验和卸载检查。
  * 修复了在接口上注册 IP 地址时需要原生 IP 支持的问题。
  * 修复了若干 net_if 函数中缺失的互斥锁。
  * 修复了 IPv6 多播组的重新加入。
  * 修复了卸载接口的 :c:func:`net_if_send_data` 操作。
  * 修复了禁用 IPv6 时不必要的 IPv6 多播组加入。
  * 修复了使用 ``-Wtype-limits`` 构建时的编译器警告。

* OpenThread：

  * 在 OpenThread 无线电平台中添加了对
    :kconfig:option:`CONFIG_IEEE802154_SELECTIVE_TXCHANNEL`
    选项的支持。
  * 添加了 NAT64 发送和接收回调。
  * 添加了新的 Kconfig 选项：

    * :kconfig:option:`CONFIG_OPENTHREAD_NAT64_CIDR`
    * :kconfig:option:`CONFIG_OPENTHREAD_STORE_FRAME_COUNTER_AHEAD`
    * :kconfig:option:`CONFIG_OPENTHREAD_DEFAULT_RX_SENSITIVITY`
    * :kconfig:option:`CONFIG_OPENTHREAD_CSL_REQUEST_TIME_AHEAD`

  * 修复了已弃用/首选 IPv6 地址状态转换。
  * 修复了已弃用 IPv6 地址的处理。
  * Zephyr 的 OpenThread 移植中的其他各种小修复。

* Shell：

  * 添加了对用
    Kconfig 启用/禁用单个网络 shell 命令的支持。
  * 为 DHCPv4/6 客户端管理添加了新的 ``net dhcpv4/6 client`` 命令。
  * 为虚拟接口管理添加了新的 ``net virtual`` 命令。
  * 即使禁用了原生 IP 栈，``net ipv4/6`` 命令现在也可用。
  * 添加暴露连接管理器功能的新 ``net cm`` 命令。
  * 修复了 telnet shell 后端连接终止时可能的断言。
  * 事件监控线程栈大小现在可用 Kconfig 配置。
  * 将 ``bridge`` 命令迁移到 ``net`` 命令下，即 ``net bridge``。
  * 各种命令输出中的多个小改进。

* 套接字：

  * 为套接字服务添加了专用的 ``net_socket_service_handler_t`` 回调函数类型。
  * 为 TLS 套接字添加了 TLS 1.3 支持。
  * 修复了关闭 NSOS 套接字时的套接字泄漏。
  * 将套接字服务库从实验性移出。
  * 弃用了 ``CONFIG_NET_SOCKETS_POLL_MAX``。
  * 将 ``zsock_poll()`` 和 ``zsock_select`` 实现移动到 ``zvfs``
    库。
  * 从套接字服务宏中移除了 ``work_q`` 参数，因为它不再
    使用。
  * 将原生 INET 套接字实现与套接字系统调用分离，
    以便在使用卸载套接字时不必构建它。
  * 修复了对端静默断开时 TLS 套接字 :c:func:`zsock_connect` 中可能的无限阻塞。
  * 修复了 :c:func:`zsock_recvmsg` 中 ``msg_controllen`` 未正确设置的问题。
  * 修复了轮询 TLS 套接字 POLLOUT 事件时可能的忙循环。

* TCP：

  * 修复了向套接字层传播连接错误。
  * 改进了对端未随数据发送 PSH 标志时的 ACK 回复逻辑。

* Websocket：

  * 在 Echo Server 示例中添加了对 Websocket 控制台的支持。
  * 修复了在不带 POSIX 的情况下构建 websockets 时对 ``MSG_DONTWAIT`` 的未定义引用。

* Wi-Fi：

  * 在 wifi shell 的连接命令中添加了对 80211R 快速 BSS 迁移参数使用的支持。
  * 修复了 shell 的 ap config 命令使用 sta 接口区域的问题
  * 为 NXP Wifi 驱动添加了 AP 配置 cmd 支持
  * 修复了 NXP WiFi 驱动中的休眠状态，使其在成功连接到 AP 后设置为关闭

* zperf：

  * 在 zperf 示例中添加了对 USB CDC NCM 的支持。
  * 修复了在某些
    配置下 zperf 示例中未启动 DHCPv4 客户端的问题。

USB
***

* 新的 USB 设备栈：

  * 添加了 USB CDC 网络控制模型实现
  * 增强了 USB 音频类 2 实现
  * 使 USB 设备栈支持高带宽
  * 增强了 CDC ACM 和 HID 类实现

设备树
**********

* 添加了对字符串数组和数组类型属性作为枚举的支持。
  为此添加了许多新宏，例如 :c:macro:`DT_ENUM_IDX_BY_IDX`。
* 添加了 :c:macro:`DT_ANY_COMPAT_HAS_PROP_STATUS_OKAY`。
* 添加了 :c:macro:`DT_NODE_HAS_STATUS_OKAY`。
* 添加了 :c:macro:`DT_INST_NUM_IRQS`。
* 添加了宏 :c:macro:`DT_NODE_FULL_NAME_UNQUOTED`、:c:macro:`DT_NODE_FULL_NAME_TOKEN`、
  和 :c:macro:`DT_NODE_FULL_NAME_UPPER_TOKEN`。
* ``DT_*_REG_ADDR`` 现在返回带 C 的 ``U`` 后缀的显式无符号值。
* 修复了 DTS 中双引号、反斜杠和换行符的转义，
  以便它们可用于字符串属性。
* 将 ``power-domain`` 基础属性重命名为 ``power-domains``，
  并引入了 ``power-domain-names`` 属性。``#power-domain-cells`` 现在也是必需的。
* 将 NXP 远程域控制器属性移动到其自己的 schema 文件

Kconfig
*******

库 / 子系统
**********************

* 调试

    * 为 probe-rs（基于 Rust 的嵌入式工具包）添加了 west 运行器。

* 按需分页

  * 添加了 LRU（最近最少使用）淘汰算法。

  * 添加了对按需内存映射的支持（:kconfig:option:`CONFIG_DEMAND_MAPPING`）。

  * 使按需分页与 SMP 兼容。

* 管理

  * MCUmgr

    * 添加了对 :ref:`mcumgr_smp_group_10` 的支持，允许列出
      受支持组的信息。
    * 通过添加前导零修复了 :c:enum:`OS_MGMT_ID_DATETIME_STR` 中毫秒的格式。
    * 添加了对使用通知钩子自定义 os mgmt 引导加载程序信息响应的支持，
      可通过 :kconfig:option:`CONFIG_MCUMGR_GRP_OS_BOOTLOADER_INFO_HOOK` 启用，
      数据结构为 :c:struct:`os_mgmt_bootloader_info_data`。
    * 添加了对 img mgmt 槽信息命令的支持，允许列出
      设备上镜像和槽的信息。
    * 添加了对 LoRaWAN MCUmgr 传输的支持，可通过
      :kconfig:option:`CONFIG_MCUMGR_TRANSPORT_LORAWAN` 启用。

  * hawkBit

    * :c:func:`hawkbit_autohandler` 现在接受一个参数。如果参数设置为 true，
      autohandler 将在运行后重新调度自身。如果参数设置为 false，
      autohandler 将不会重新调度自身。两个变体独立调度。
      autohandler 始终在系统工作队列中运行。

    * 使用 :c:func:`hawkbit_autohandler_wait` 函数等待 autohandler 完成。

    * 从 shell 运行 hawkBit 现在在系统工作队列中执行。

    * 使用 :c:func:`hawkbit_autohandler_cancel` 函数取消 autohandler。

    * 使用 :c:func:`hawkbit_autohandler_set_delay` 函数延迟 autohandler 的下一次运行。

    * hawkBit 头文件已分离为多个头文件。主头文件现在是
      ``<zephyr/mgmt/hawkbit/hawkbit.h>` `，autohandler 头文件现在是
      ``<zephyr/mgmt/hawkbit/autohandler.h>``，配置头文件现在是
      ``<zephyr/mgmt/hawkbit/config.h>``。

* 电源管理

  * 添加了初始 ESP32-C6 电源管理接口，以允许浅睡和深睡功能。

* 加密

  * Mbed TLS 已更新到 3.6.2 版本（从 3.6.0）。发布说明可在以下地址找到：

    * https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-3.6.1
    * https://github.com/Mbed-TLS/mbedtls/releases/tag/mbedtls-3.6.2

  * 添加了 Kconfig 符号 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_EXTERNAL_RNG_ALLOW_NON_CSPRNG`，
    允许在同时启用 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_EXTERNAL_RNG`
    时 ``psa_get_random()`` 使用非密码学
    安全随机源。这仅用于测试目的，不用于生产环境。
    （:github:`76408`）
  * 添加了 Kconfig 符号 :kconfig:option:`CONFIG_MBEDTLS_TLS_VERSION_1_3`，
    用于启用来自 Mbed TLS 的 TLS 1.3 支持。启用后，还可以启用以下
    新的 Kconfig 符号：

    * :kconfig:option:`CONFIG_MBEDTLS_TLS_SESSION_TICKETS` 用于启用会话票据
      （RFC 5077）；
    * :kconfig:option:`CONFIG_MBEDTLS_SSL_TLS1_3_KEY_EXCHANGE_MODE_PSK_ENABLED`
      用于 TLS 1.3 PSK 密钥交换模式；
    * :kconfig:option:`CONFIG_MBEDTLS_SSL_TLS1_3_KEY_EXCHANGE_MODE_EPHEMERAL_ENABLED`
      用于 TLS 1.3 临时密钥交换模式；
    * :kconfig:option:`CONFIG_MBEDTLS_SSL_TLS1_3_KEY_EXCHANGE_MODE_PSK_EPHEMERAL_ENABLED`
      用于 TLS 1.3 PSK 临时密钥交换模式。

* SD

  * 本次发布无重大更改

* 设置

  * 设置已扩展，允许使用
    ``SETTINGS_STATIC_HANDLER_DEFINE_WITH_CPRIO(...)`` 为 static_handlers 和
    ``settings_register_with_cprio(...)`` 为 dynamic_handlers 优先化提交处理程序。

* Shell：

  * 将 ``kernel threads`` 和 ``kernel stacks`` shell 命令重新组织到
    L1 ``kernel thread`` shell 命令下，作为 ``kernel thread list`` 和 ``kernel thread stacks``
  * 添加了多个 shell 命令以在运行时配置 CPU 掩码亲和性/将线程
    固定到特定 CPU，执行 ``kernel thread -h`` 查看更多信息。
  * 不带任何额外参数的 ``kernel reboot`` shell 命令现在将执行冷重启，
    而不需要键入 ``kernel reboot cold``。

* 存储

  * LittleFS：该模块已用上游提交的更改更新，
    从版本 2.8.1（最后一次模块更新）到
    发布的版本 2.9.3（含）。
  * 修复了 NVS 中由变量赋值不匹配引起的静态分析错误

  * LittleFS：修复了用于配置 LittleFS 实例块周期的 DTS 选项
    被忽略的问题（:github:`79072`）。

  * LittleFS：修复了前瞻缓冲区大小与实际分配缓冲区大小
    不匹配的问题（:github:`77917`）。

  * FAT FS：添加了 :kconfig:option:`CONFIG_FILE_SYSTEM_LIB_LINK`，允许在不启用文件系统
    子系统的情况下链接文件系统支持库。当用户希望
    直接使用文件系统库而绕过文件系统
    子系统时可使用该选项。

  * FAT FS：添加了 :kconfig:option:`CONFIG_FS_FATFS_LBA64`，用于在 FAT 文件系统驱动中启用
    对 64 位 LBA 和 GPT 的支持。

  * FAT FS：添加了 :kconfig:option:`CONFIG_FS_FATFS_MULTI_PARTITION`，启用对
    用 GPT 或 MBR 分区设备的支持。

  * FAT FS：添加了 :kconfig:option:`CONFIG_FS_FATFS_HAS_RTC`，用于在 FAT 文件系统上
    启用 RTC 以用于文件时间戳。

  * FAT FS：添加了 :kconfig:option:`CONFIG_FS_FATFS_EXTRA_NATIVE_API`，启用额外的 FAT
    文件系统驱动函数，这些函数不通过 Zephyr 文件系统子系统暴露，
    供打算在代码中直接调用它们的用户。

  * Stream Flash：修复了 :c:func:`stream_flash_erase_page` 未正确检查
    请求的擦除范围并可能允许擦除设备上任何页的问题（:github:`79800`）。

  * Shell：修复了使用 shell 挂载文件系统失败后
    在设备重置前无法再次成功挂载该文件系统的问题（:github:`80024`）。

  * :ref:`ZMS<zms_api>`：引入了一种新的存储系统，设计用于与所有类型的
    非易失性存储技术一起工作。它支持传统的片上 NOR 闪存以及
    像 RRAM 和 MRAM 这样根本不需要单独擦除操作的新技术。

* 任务看门狗

* 跟踪

  * 添加了对"用户事件"跟踪的支持，目的是允许驱动或
    应用程序开发人员快速为调试目的添加事件跟踪

* POSIX API

  * 添加了对以下选项组的支持：

    * :ref:`POSIX_DEVICE_IO <posix_option_group_device_io>`
    * :ref:`POSIX_SIGNALS <posix_option_group_signals>`

  * 添加了对以下选项的支持：

    * :ref:`_POSIX_SYNCHRONIZED_IO <posix_option_synchronized_io>`
    * :ref:`_POSIX_THREAD_PRIO_PROTECT <posix_option_thread_prio_protect>`

  * :ref:`POSIX_FILE_SYSTEM <posix_option_group_file_system>` 改进：

    * 在 :c:func:`open()` 中支持 :c:macro:`O_TRUNC` 标志。
    * 支持 :c:func:`rmdir` 和 :c:func:`remove`。

  * :ref:`_POSIX_THREAD_SAFE_FUNCTIONS <posix_option_thread_safe_functions>` 改进：

    * 支持 :c:func:`asctime_r`、:c:func:`ctime_r` 和 :c:func:`localtime_r`。

  * :ref:`POSIX_THREADS_BASE <posix_option_group_threads_base>` 改进：

    * 使用 :ref:`用户模式信号量 API <semaphores_v2>` 而非
      :ref:`自旋锁 API <smp_arch>` 进行池同步。

* LoRa/LoRaWAN

* ZBus

* JWT（JSON Web Token）

  * 添加了以下新符号，以允许同时指定签名
    算法和加密库：

    * :kconfig:option:`CONFIG_JWT_SIGN_RSA_PSA`（默认）使用 PSA Crypto API 的 RSA 签名；
    * :kconfig:option:`CONFIG_JWT_SIGN_RSA_LEGACY` 使用 Mbed TLS 的 RSA 签名；
    * :kconfig:option:`CONFIG_JWT_SIGN_ECDSA_PSA` 使用 PSA Crypto API 的 ECDSA 签名。

    （:github:`79653`）

* 固件

  * 引入对 ARM 系统控制和管理接口（SCMI）的基本支持，包括：

    * 时钟管理协议命令子集
    * 引脚控制协议命令子集
    * 共享内存和基于邮箱的传输

HAL
****

* Nordic

  * 将 nrfx 更新到 3.7.0 版本。
  * 添加了 nRF70 Wi-Fi 驱动的操作系统无关部分。

* STM32

  * 将 STM32C0 更新到 cube 版本 V1.2.0。
  * 将 STM32F1 更新到 cube 版本 V1.8.6。
  * 将 STM32F2 更新到 cube 版本 V1.9.5。
  * 将 STM32F4 更新到 cube 版本 V1.28.1。
  * 将 STM32G4 更新到 cube 版本 V1.6.0。
  * 将 STM32H5 更新到 cube 版本 V1.3.0。
  * 将 STM32H7 更新到 cube 版本 V1.11.2。
  * 将 STM32H7RS 更新到 cube 版本 V1.1.0。
  * 添加了 STM32U0 Cube 软件包（1.1.0）
  * 将 STM32U5 更新到 cube 版本 V1.6.0。
  * 将 STM32WB 更新到 cube 版本 V1.20.0。
  * 添加了 STM32WB0 Cube 软件包（1.0.0）
  * 将 STM32WBA 更新到 cube 版本 V1.4.1。

* ADI

* Espressif

  * 将 HAL 同步到 v5.1.4 版本，以更新 SoC 低层文件、RF 库和
    整体驱动支持。
* NXP

    * 将 MCUX HAL 更新到 SDK 版本 2.16.000
    * 将 NXP S32ZE HAL 驱动更新到 2.0.0 版本

* Silabs

  * 将 Series 2 更新到 Simplicity SDK 2024.6，而 Series 0/1 继续使用 Gecko SDK 4.4。

MCUboot
*******

  * 移除了损坏的目标配置头文件功能。
  * 从 ``boot_encrypt`` 中移除了 ``image_index``。
  * 将 boot_enc_decrypt 重命名为 boot_decrypt_key。
  * 更新为使用 ``EXTRA_CONF_FILE`` 而非已弃用的 ``OVERLAY_CONFIG`` 参数。
  * 将 ``boot_encrypt()`` 更新为 ``boot_enc_encrypt()`` 和 ``boot_enc_decrypt()``。
  * 将 ``boot_enc_valid`` 更新为接受槽而非镜像索引。
  * 将 ``boot_enc_load()`` 更新为接受槽号而非镜像。
  * 将 boot_serial 中的日志更新为调试级别。
  * 更新 Kconfig 以允许在 nRF 设备上禁用 NRFX_WDT。
  * 将 CMake ERROR 语句更新为 FATAL_ERROR。
  * 在引导前添加了正在引导的应用程序版本输出。
  * 为 hello-world 示例添加了 sysbuild 支持。
  * 为 bootutil 添加了 SIG_PURE TLV。
  * 为 bootutil 添加了写入块大小检查。
  * 添加了对意外闪存扇区大小的检查。
  * 为 MCUboot 代码添加了 SHA512 支持，并在 imgtool 中支持计算 SHA512 哈希。
  * 添加了对 USB DFU 选项的回退。
  * 为 bootutil 添加了更好的模式选择检查。
  * 将 bootutil 保护 TLV 大小添加到镜像大小检查。
  * 添加了移除具有冲突标志的镜像或需要不支持的功能的功能。
  * 为 MCUboot、Kconfig 选项添加了压缩镜像标志和 TLV，并在 imgtool 中支持
    生成带 ARM thumb 过滤器的压缩 LZMA2 镜像。
  * 在检查镜像前添加了镜像头验证。
  * 为 ``boot_is_header_valid()`` 函数添加了状态。
  * 添加了 ``CONFIG_MCUBOOT_ENC_BUILTIN_KEY`` Kconfig 选项。
  * 为 imgtool 添加了不可引导标志。
  * 为生成的头文件路径添加了 zephyr 前缀。
  * 添加了可选的 img mgmt 槽信息功能。
  * 为 bootutil 添加了额外镜像的最大镜像大小详情支持。
  * 添加了对自动计算最大扇区数的支持。
  * 添加了缺失的 ``boot_enc_init()`` 函数。
  * 添加了在 bootutil 中保持镜像在暂存区域加密的支持。
  * 修复了 NXP IMX.RT、LPC55x 和 MCXNx 平台的串行恢复
  * 修复了 imgtool 中公共 RSA 签名的问题。
  * 修复了 ``boot_serial_enter()`` 已定义但未使用的警告问题。
  * 修复了示例中 ``main()`` 返回错误类型的警告问题。
  * 修复了在 bootutil 中使用指针的问题。
  * 修复了 boot_serial 中槽号的不正确使用。
  * 修复了 bootutil 中 directXIP/RAM 加载的槽信息。
  * 修复了 bootutil 中未用 mbedTLS 清零 AES 和 SHA-256 上下文的问题。
  * 修复了 boot_serial 的 ``format`` 和 ``incompatible-pointer-types`` 警告。
  * 修复了 bootutil 中 ``find_swap_count`` 的错误定义。
  * 修复了 bootutil 交换移动最大应用大小计算。
  * 修复了 imgtool 中 getpub 对 ed25519 密钥失败的问题。
  * 修复了其他东西命名为 mcuboot 时 sysbuild 的问题。
  * 修复了 RAM 加载链加载地址。
  * 修复了在 bootutil 中断 swap-scratch 后正确获取镜像头的问题。
  * 本次发布中的 MCUboot 版本为 ``2.1.0+0-dev``。
  * 将以下 nxp 开发板添加为测试目标区域：``frdm_ke17z``、``frdm_ke17z512``、
    ``rddrone_fmuk66``、``twr_ke18f``、``frdm_mcxn947/mcxn947/cpu0``

OSDP
****

Trusted Firmware-M（TF-M）
*************************

* TF-M 已更新到 2.1.1 版本（从 2.1.0）。
  发布说明可在以下地址找到：https://trustedfirmware-m.readthedocs.io/en/tf-mv2.1.1/releases/2.1.1.html

Nanopb
******

* 将 nanopb 模块更新到 0.4.9 版本。
  完整发布说明在 https://github.com/nanopb/nanopb/blob/0.4.9/CHANGELOG.txt

LVGL
****

* 添加了 ``LV_ATTRIBUTE_MEM_ALIGN`` 的定义，以便库内部数据结构可以
  对齐到特定边界。
* 提供了对齐定义以满足某些 GPU 的对齐要求

zcbor
*****

* 将 zcbor 库更新到 0.9.0 版本。
  完整发布说明在 https://github.com/NordicSemiconductor/zcbor/blob/0.9.0/RELEASE_NOTES.md
  迁移指南在 https://github.com/NordicSemiconductor/zcbor/blob/0.9.0/MIGRATION_GUIDE.md
  要点：

    * 许多代码生成 bug 修复

    * 现在可以在运行时决定解码器是否应强制规范编码。

    * 允许 --file-header 接受包含头文件内容的文件路径

测试与示例
*****************

* 随着 ``native_posix`` 的弃用，许多明确在 native_posix 中运行的测试
  现在改为在 :zephyr:board:`native_sim<native_sim>` 中运行。
  然而 native_posix 作为平台仍受测试。
* 用无报警计数器的测试用例扩展了 counter_basic_api 的测试
* 为 fatfs API 测试添加了对测试 SDMMC 设备的支持
* 扩展了 net/vlan 以在每个 vlan-iface 上添加 IPv6 前缀配置
* 通过添加彩条增强了摄像头 fixture 测试以启用自动化
* 添加了使用针对 NXP ADSP 开发板优化的库进行数值计算（如 FFT、回声消除等）的示例
* 根据 NXP Kinetis MCU 的限制调整了 SPI_LOOPBACK 测试
* 启用了视频示例运行视频捕获（samples/drivers/video）

* 添加了 :zephyr:code-sample:`smf_calculator` 示例，演示状态机框架
  与 LVGL 结合使用以创建简单计算器应用程序的用法。
* 在可能的情况下整合了显示示例，以对所有盾牌使用单个测试用例

问题相关项
*******************

已知问题
=============

- :github:`71042` stream_flash：stream_flash_init() 的 size 参数允许忽略分区布局
- :github:`67407` stream_flash：stream_flash_erase_page 允许意外擦除流
- :github:`80875` stepper_api：stepper.h 的 c-prototype 不正确且 stepper_shell.c 缺少 NULL 检查
