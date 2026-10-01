:orphan:

..
  参见
  https://docs.zephyrproject.org/latest/releases/index.html#migration-guides
  了解本文档应包含的内容。

.. _migration_4.2:

Zephyr v4.2.0 迁移指南
######################

本文档描述了将应用从 Zephyr v4.1.0 迁移到 Zephyr v4.2.0 所需的更改。

其他更改（与迁移应用无直接关系）可在
:ref:`发布说明<zephyr_4.2>` 中查看。

.. contents::
    :local:
    :depth: 2

构建系统
************

* 已移除 HWMv1 支持，任何 HWMv1 格式的树外开发板或 SoC 必须迁移到
  :ref:`HWMv2 <hw_model_v2>` 才能与 Zephyr v4.2 及以后版本配合使用。

内核
******

开发板
******

* 所有基于 Nordic 芯片、默认使用 ``nrfjprog`` Nordic 命令行工具进行烧录的开发板，
  已改为默认使用新的 nRF Util（``nrfutil``）工具。
  这意味着你可能需要 `安装 nRF Util
  <https://www.nordicsemi.com/Products/Development-tools/nrf-util>`_，
  或者如果你希望继续使用 ``nrfjprog``，
  可以在调用 west 时指定 runner 实现：``west flash -r nrfjprog``。
  nRF Util 的完整文档可在
  `此处 <https://docs.nordicsemi.com/bundle/nrfutil/page/README.html>`_ 找到。

* 所有基于 nRF54L 系列 Nordic 芯片的开发板，现在默认在烧录时不擦除内部存储的任何部分。
  如果希望恢复到之前默认擦除将被烧录固件写入的页，
  可在调用 ``west flash`` 时将新的 ``--erase-mode`` 命令行开关设为 ``ranges``。
  注意 nRF54L 设备上的 RRAM 不物理分页，分页仅人为提供，
  页大小为 4096 字节，以便于 nRF52 软件向 nRF54L 设备的过渡。

* 配置选项 :kconfig:option:`CONFIG_NATIVE_POSIX_SLOWDOWN_TO_REAL_TIME`
  已弃用，由 :kconfig:option:`CONFIG_NATIVE_SIM_SLOWDOWN_TO_REAL_TIME` 取代。

* DT 绑定 :dtcompatible:`zephyr,native-posix-cpu`
  已弃用，由 :dtcompatible:`zephyr,native-sim-cpu` 取代。

* Zephyr 现在支持 :zephyr:board:`neorv32` 的 1.11.6 版本。
  NEORV32 处理器（SoC）实现需要更新到该版本才能与 Zephyr v4.2.0 兼容。

* :zephyr:board:`neorv32` 现在通过开发板变体（board variant）
  目标 NEORV32 处理器（SoC）模板。
  旧的 ``neorv32`` 开发板目标现在命名为 ``neorv32/neorv32/up5kdemo``。

* ``arduino_uno_r4_minima``、``arduino_uno_r4_wifi`` 和 ``mikroe_clicker_ra4m1``
  已迁移到新的基于 FSP 的配置。
  虽然没有重大功能更改，但设备树结构已显著修订。
  以下设备树绑定现已移除：
  ``renesas,ra-gpio``、``renesas,ra-uart-sci``、``renesas,ra-pinctrl``、
  ``renesas,ra-clock-generation-circuit`` 和 ``renesas,ra-interrupt-controller-unit``。
  相反，请使用以下替代项：
  - :dtcompatible:`renesas,ra-gpio-ioport`
  - :dtcompatible:`renesas,ra-sci-uart`
  - :dtcompatible:`renesas,ra-pinctrl-pfs`
  - :dtcompatible:`renesas,ra-cgc-pclk-block`

* Nucleo WBA52CG 开发板（``nucleo_wba52cg``）不再支持，
  因为它处于 NRND（不建议用于新设计）状态，
  且从 STM32CubeWBA 1.1.0 版本（2023 年 7 月）起不再受支持。
  建议迁移到 :zephyr:board:`nucleo_wba55cg`（``nucleo_wba55cg``），
  且无需任何更改即可完成。

* Espressif 开发板 ``esp32_devkitc_wroom`` 和 ``esp32_devkitc_wrover``
  共享几乎相同的特性。
  差异由 Kconfig 选项覆盖，因此两个开发板已合并为 ``esp32_devkitc``。

* STM32 开发板现在应通过包含 ``openocd-stm32.board.cmake``
  而非 ``openocd.board.cmake`` 来添加 OpenOCD 编程支持。
  ``openocd-stm32.board.cmake`` 文件使用制造商特定配置
  （如 STM32 批量擦除命令）扩展默认 OpenOCD runner。

* STM32N6570-DK 开发板的默认变体（``stm32n6570_dk/stm32n657xx``）
  现在应作为链式加载（chainloaded）应用，
  应使用 ``--sysbuild`` 构建。
  旧的默认行为（构建作为一级引导加载程序运行的应用）
  现在作为专用变体（``stm32n6570_dk/stm32n657xx/fsbl``）可用，
  必须显式选择。
  有关这些变体的更多信息，请参见开发板文档。

* 嵌入 TF-M BL2 启动阶段的 STM32 开发板
  （``b_u585i_iot02a//ns``、``nucleo_l552ze_q//ns`` 和 ``stm32l562e_dk//ns``）
  不再如之前那样在 BL2 中嵌入硬件加密加速器驱动，
  现在依赖 Mbed TLS 软件实现。
  这与升级到 TF-M v2.2 相关。
  硬件加密加速器在 TF-M 中仍受支持，但仅在运行时安全固件中。

设备驱动程序和设备树
*****************************

.. zephyr-keep-sorted-start re(^\w)

音频
=====

* :dtcompatible:`cirrus,cs43l22` 的绑定文件已重命名为
  与兼容字符串匹配的名称。

计数器
=======

* ``counter_native_posix`` 已重命名为 ``counter_native_sim``，
  连同其 Kconfig 选项和 DT 绑定。
  :dtcompatible:`zephyr,native-posix-counter` 已弃用，
  由 :dtcompatible:`zephyr,native-sim-counter` 取代。
  :kconfig:option:`CONFIG_COUNTER_NATIVE_POSIX` 及其相关选项
  已改为 :kconfig:option:`CONFIG_COUNTER_NATIVE_SIM`（:github:`86616`）。

DAI
===

* 设备树属性 ``dai_id`` 已重命名为 ``dai-id``。
* 设备树属性 ``afe_name`` 已重命名为 ``afe-name``。
* 设备树属性 ``agent_disable`` 已重命名为 ``agent-disable``。
* 设备树属性 ``ch_num`` 已重命名为 ``ch-num``。
* 设备树属性 ``mono_invert`` 已重命名为 ``mono-invert``。
* 设备树属性 ``quad_ch`` 已重命名为 ``quad-ch``。
* 设备树属性 ``int_odd`` 已重命名为 ``int-odd``。

DMA
===

* 设备树属性 ``nxp,a_on`` 已重命名为 ``nxp,a-on``。
* 设备树属性 ``dma_channels`` 已重命名为 ``dma-channels``。
* Xilinx DMA 控制器的绑定文件已重命名为使用正确的厂商前缀
  （``xlnx`` 而非 ``xilinx``）并与兼容字符串匹配。

设备树
==========

* dts/common 中许多厂商特定和架构特定的文件已移到更具体的位置。
  因此，任何从 Zephyr 树中 ``#include <common/some_file.dtsi>``
  包含文件的 dts 文件都需要改为仅 ``#include <some_file.dtsi>``。

* Silicon Labs Series 2 的 SoC 级 dts 文件已按设备超家族（superfamily）
  重组到子目录中。
  因此，使用 Series 2 SoC 的开发板的任何 dts 文件都需要将包含从
  ``#include <silabs/some_soc.dtsi>`` 改为 ``#include <silabs/xg2[1-9]/some_soc.dtsi>``。

* :c:macro:`DT_ENUM_HAS_VALUE` 和 :c:macro:`DT_INST_ENUM_HAS_VALUE` 宏
  现在用于数组时检查所有值，而不仅仅是第一个。

* 设备树和绑定中的属性名使用连字符（``-``）作为分隔符，
  替换之前使用的所有下划线（``_``）。
  对于本地代码，可通过运行 ``scripts/utils/migrate_bindings_style.py`` 脚本
  将绑定中的属性名迁移为使用连字符。

显示
=======

* 在 STM32 设备上，LTDC 驱动（:dtcompatible:`st,stm32-ltdc`）的
  RGB565 格式 ``PIXEL_FORMAT_RGB565`` 已被 ``PIXEL_FORMAT_BGR565`` 替换，
  以匹配 Zephyr 预期的格式。
  此更改确保显示和视频捕获示例的正确行为。

EEPROM
========

* :dtcompatible:`ti,tmp116-eeprom` 已重命名为 :dtcompatible:`ti,tmp11x-eeprom`，
  因为它同时支持 tmp117 和 tmp119。

增强串行外设接口（eSPI）
===========================================

* 设备树属性 ``io_girq`` 已重命名为 ``io-girq``。
* 设备树属性 ``vw_girqs`` 已重命名为 ``vw-girqs``。
* 设备树属性 ``pc_girq`` 已重命名为 ``pc-girq``。
* 设备树属性 ``poll_timeout`` 已重命名为 ``poll-timeout``。
* 设备树属性 ``poll_interval`` 已重命名为 ``poll-interval``。
* 设备树属性 ``consec_rd_timeout`` 已重命名为 ``consec-rd-timeout``。
* 设备树属性 ``sus_chk_delay`` 已重命名为 ``sus-chk-delay``。
* 设备树属性 ``sus_rsm_interval`` 已重命名为 ``sus-rsm-interval``。

熵源
=======

* ``fake_entropy_native_posix`` 已重命名为 ``fake_entropy_native_sim``，
  连同其 Kconfig 选项和 DT 绑定。
  :dtcompatible:`zephyr,native-posix-rng` 已弃用，
  由 :dtcompatible:`zephyr,native-sim-rng` 取代。
  :kconfig:option:`CONFIG_FAKE_ENTROPY_NATIVE_POSIX` 及其相关选项
  已改为 :kconfig:option:`CONFIG_FAKE_ENTROPY_NATIVE_SIM`（:github:`86615`）。

以太网
========

* 已移除 Kconfig 选项 ``ETH_STM32_HAL_MII``（:github:`86074`）。
  PHY 接口类型现在通过设备树中的 ``phy-connection-type`` 属性选择。

* :dtcompatible:`st,stm32-ethernet` 驱动现在需要在设备树中
  将 ``phy-handle`` phandle 设置为对应的 PHY 节点（:github:`87593`）。

* Kconfig 选项 ``ETH_STM32_HAL_PHY_ADDRESS``、``ETH_STM32_CARRIER_CHECK``、
  ``ETH_STM32_CARRIER_CHECK_RX_IDLE_TIMEOUT_MS``、``ETH_STM32_AUTO_NEGOTIATION_ENABLE``、
  ``ETH_STM32_SPEED_10M``、``ETH_STM32_MODE_HALFDUPLEX`` 已移除，
  因为它们不再需要，
  且驱动现在使用以太网 PHY API 与 PHY 驱动通信，
  后者负责配置 PHY 设置（:github:`87593`）。

* ``ethernet_native_posix`` 已重命名为 ``ethernet_native_tap``，
  连同其 Kconfig 选项：
  :kconfig:option:`CONFIG_ETH_NATIVE_POSIX` 及其相关选项
  已弃用，由 :kconfig:option:`CONFIG_ETH_NATIVE_TAP` 取代（:github:`86578`）。

* NuMaker 以太网驱动 ``eth_numaker.c`` 现在支持 ``gen_random_mac``，
  且 EMAC 数据闪存特性已移除（:github:`87953`）。

* :zephyr_file:`include/zephyr/net/ethernet.h` 中的枚举
  ``ETHERNET_DSA_MASTER_PORT`` 和 ``ETHERNET_DSA_SLAVE_PORT``
  已重命名为 ``ETHERNET_DSA_CONDUIT_PORT`` 和 ``ETHERNET_DSA_USER_PORT``。

* 以太网速度的枚举已重命名为更独立于所用介质。
  ``LINK_HALF_10BASE_T``、``LINK_FULL_10BASE_T``、``LINK_HALF_100BASE_T``、
  ``LINK_FULL_100BASE_T``、``LINK_HALF_1000BASE_T``、``LINK_FULL_1000BASE_T``、
  ``LINK_FULL_2500BASE_T`` 和 ``LINK_FULL_5000BASE_T``
  已重命名为 :c:enumerator:`LINK_HALF_10BASE`、:c:enumerator:`LINK_FULL_10BASE`、
  :c:enumerator:`LINK_HALF_100BASE`、:c:enumerator:`LINK_FULL_100BASE`、
  :c:enumerator:`LINK_HALF_1000BASE`、:c:enumerator:`LINK_FULL_1000BASE`、
  :c:enumerator:`LINK_FULL_2500BASE` 和 :c:enumerator:`LINK_FULL_5000BASE`。
  ``ETHERNET_LINK_10BASE_T``、``ETHERNET_LINK_100BASE_T``、
  ``ETHERNET_LINK_1000BASE_T``、``ETHERNET_LINK_2500BASE_T`` 和
  ``ETHERNET_LINK_5000BASE_T`` 已分别重命名为
  :c:enumerator:`ETHERNET_LINK_10BASE`、:c:enumerator:`ETHERNET_LINK_100BASE`、
  :c:enumerator:`ETHERNET_LINK_1000BASE`、:c:enumerator:`ETHERNET_LINK_2500BASE` 和
  :c:enumerator:`ETHERNET_LINK_5000BASE`（:github:`87194`）。

* ``ETHERNET_CONFIG_TYPE_LINK``、``ETHERNET_CONFIG_TYPE_DUPLEX``、
  ``ETHERNET_CONFIG_TYPE_AUTO_NEG`` 以及相关的
  ``NET_REQUEST_ETHERNET_SET_LINK``、``NET_REQUEST_ETHERNET_SET_DUPLEX``、
  ``NET_REQUEST_ETHERNET_SET_AUTO_NEGOTIATION`` 已移除。
  应改用 :c:func:`phy_configure_link` 连同 :c:func:`net_eth_get_phy`
  来配置链路（:github:`90652`）。

* :c:func:`phy_configure_link` 增加了 ``flags`` 参数。
  将其设为 ``0`` 以保持旧行为（:github:`91354`）。

闪存
=====

* 文件 ``flash_hp_ra.h`` 已重命名为 ``soc_flash_renesas_ra_hp.h``。
* 文件 ``flash_hp_ra.c`` 已重命名为 ``soc_flash_renesas_ra_hp.c``。
* 文件 ``flash_hp_ra_ex_op.c`` 已重命名为 ``soc_flash_renesas_ra_hp_ex_op.c``。

* Flash HP Renesas RA 双银行模式的 Kconfig 符号
  :kconfig:option:`CONFIG_DUAL_BANK_MODE` 已移除。
* Flash HP Renesas RA 的 Kconfig 符号 :kconfig:option:`CONFIG_RA_FLASH_HP`
  已重命名为 :kconfig:option:`CONFIG_SOC_FLASH_RENESAS_RA_HP`。
* Flash HP Renesas RA 写保护的 Kconfig 符号
  :kconfig:option:`CONFIG_FLASH_RA_WRITE_PROTECT`
  已重命名为 :kconfig:option:`CONFIG_FLASH_RENESAS_RA_HP_WRITE_PROTECT`。

* 文件 ``renesas,ra-nv-flash.yaml`` 已拆分为 2 个文件
  ``renesas,ra-nv-code-flash.yaml`` 和 ``renesas,ra-nv-data-flash.yaml``。
* ``renesas,ra-nv-flash`` 的 ``compatible`` 已拆分为
  :dtcompatible:`renesas,ra-nv-code-flash.yaml`
  和 :dtcompatible:`renesas,ra-nv-data-flash.yaml`。

GPIO
====

* 为支持引脚众多的 RP2350B，Raspberry Pi-GPIO 配置已更改。
  :dtcompatible:`raspberrypi,rpi-gpio` 的先前角色已迁移到
  :dtcompatible:`raspberrypi,rpi-gpio-port`，
  而 :dtcompatible:`raspberrypi,rpi-gpio` 现在留作占位符和映射器。
  标签也随之更改，因此常规使用无需更改。
* ``arduino-nano-header-r3`` 已重命名为 :dtcompatible:`arduino-nano-header`。
  因为 R3 来自 Arduino UNO R3，其已从先前版本更改了连接器，
  且与 Arduino Nano 无关。
* 文件 ``include/zephyr/dt-bindings/gpio/nordic-npm1300-gpio.h``
  已移到 :zephyr_file:`include/zephyr/dt-bindings/gpio/nordic-npm13xx-gpio.h`，
  且将所有 ``NPM1300`` 实例重命名为 ``NPM13XX``
* ``CONFIG_GPIO_NPM1300`` 已重命名为 :kconfig:option:`CONFIG_GPIO_NPM13XX`，
  ``CONFIG_GPIO_NPM1300_INIT_PRIORITY`` 已重命名为
  :kconfig:option:`CONFIG_GPIO_NPM13XX_INIT_PRIORITY`

I2S
===
* :dtcompatible:`nxp,mcux-i2s` 驱动添加了属性 ``mclk-output``。
  将此属性设置为
* 配置 MCLK 信号为输出。
  旧驱动版本使用宏 ``I2S_OPT_BIT_CLK_SLAVE`` 配置 MCLK 信号方向。
  （:github:`88554`）

LED
===

* ``CONFIG_LED_NPM1300`` 已重命名为 :kconfig:option:`CONFIG_LED_NPM13XX`

多功能设备
===

* 文件 ``include/zephyr/drivers/mfd/npm1300.h``
  已移到 :zephyr_file:`include/zephyr/drivers/mfd/npm13xx.h`，
  且将所有 ``npm1300``/``NPM1300`` 实例重命名为 ``npm13xx``/``NPM13XX``
* ``CONFIG_MFD_NPM1300`` 已重命名为 :kconfig:option:`CONFIG_MFD_NPM13XX`，
  ``CONFIG_MFD_NPM1300_INIT_PRIORITY`` 已重命名为
  :kconfig:option:`CONFIG_MFD_NPM13XX_INIT_PRIORITY`

杂项
====

* 文件 ``drivers/memc/memc_nxp_flexram.h``
  已移到 :zephyr_file:`include/zephyr/drivers/misc/flexram/nxp_flexram.h`，
  使文件可用 ``<zephyr/drivers/misc/flexram/nxp_flexram.h>`` 包含。
  不再需要修改 CMakeList.txt 来包含此驱动。
* 所有 memc_flexram_* 命名空间的东西（包括 Kconfig 和 C API）
  已改为仅 flexram_*。

* 选择 ``CONFIG_ETHOS_U`` 而非 ``CONFIG_ARM_ETHOS_U``
  以启用 Ethos-U NPU 驱动。
* 将所有前缀 ``CONFIG_ARM_ETHOS_U_`` 的配置重命名为 ``CONFIG_ETHOS_U_``。

调制解调器
=====

* 已移除 Kconfig 选项 :kconfig:option:`CONFIG_MODEM_CELLULAR_CMUX_MAX_FRAME_SIZE`，
  由 :kconfig:option:`CONFIG_MODEM_CMUX_WORK_BUFFER_SIZE` 和
  :kconfig:option:`CONFIG_MODEM_CMUX_MTU` 取代。

稳压器
=========

* 文件 ``include/zephyr/dt-bindings/regulator/npm1300.h``
  已移到 :zephyr_file:`include/zephyr/dt-bindings/regulator/npm13xx.h`，
  且将所有 ``NPM1300`` 实例重命名为 ``NPM13XX``
* ``CONFIG_REGULATOR_NPM1300`` 已重命名为 :kconfig:option:`CONFIG_REGULATOR_NPM13XX`，
  ``CONFIG_REGULATOR_NPM1300_COMMON_INIT_PRIORITY`` 已重命名为
  :kconfig:option:`REGULATOR_NPM13XX_COMMON_INIT_PRIORITY`，
  ``CONFIG_REGULATOR_NPM1300_INIT_PRIORITY`` 已重命名为
  :kconfig:option:`CONFIG_REGULATOR_NPM13XX_INIT_PRIORITY`
* :dtcompatible:`nordic,npm1300-regulator` 的 BUCK 和 LDO 节点 GPIO 属性
  现在指定为无 GPIO 控制器的整数数组，
  移除了需要存在并启用 :dtcompatible:`nordic,npm1300-gpio` 节点
  以通过 GPIO 控制输出轨的要求。
  例如，``enable-gpios = <&pmic_gpios 3 GPIO_ACTIVE_LOW>;``
  现在指定为 ``enable-gpio-config = <3 GPIO_ACTIVE_LOW>;``。

SPI
===

* ``CONFIG_SPI_MCUX_LPSPI`` 已重命名为 :kconfig:option:`CONFIG_SPI_NXP_LPSPI`，
  该驱动的任何子配置类似，包括
  :kconfig:option:`CONFIG_SPI_NXP_LPSPI_DMA` 和
  :kconfig:option:`CONFIG_SPI_NXP_LPSPI_CPU`。
* 设备树属性 ``port_sel`` 已重命名为 ``port-sel``。
* 设备树属性 ``chip_select`` 已重命名为 ``chip-select``。
* :dtcompatible:`andestech,atcspi200` 的绑定文件已重命名为
  与兼容字符串匹配的名称。

传感器
=======

* ``ltr`` 厂商前缀已重命名为 ``liteon``，
  且 :dtcompatible:`ltr,f216a` 名称已被 :dtcompatible:`liteon,ltrf216a` 替换。
  选择项 :kconfig:option:`DT_HAS_LTR_F216A_ENABLED`
  已被 :kconfig:option:`DT_HAS_LITEON_LTRF216A_ENABLED` 取代（:github:`85453`）

* :dtcompatible:`ti,tmp116` 已重命名为 :dtcompatible:`ti,tmp11x`，
  因为它支持 tmp116、tmp117 和 tmp119。

* :dtcompatible:`meas,ms5837` 已被 :dtcompatible:`meas,ms5837-30ba`
  和 :dtcompatible:`meas,ms5837-02ba` 替换。
  要使用两个变体之一，还需要使用 status 属性。

* :dtcompatible:`we,wsen-itds` 驱动已重命名为
  :dtcompatible:`we,wsen-itds-2533020201601`。
  设备树可配置如下：

  .. code-block:: devicetree

    &i2c0 {
      itds:itds-2533020201601@19 {
        compatible = "we,wsen-itds-2533020201601";
        reg = <0x19>;
        odr = "400";
        op-mode = "high-perf";
        power-mode = "normal";
        events-interrupt-gpios = <&gpio1 1 GPIO_ACTIVE_HIGH>;
        drdy-interrupt-gpios = <&gpio1 2 GPIO_ACTIVE_HIGH>;
      };
    };

* :dtcompatible:`raspberrypi,pico-temp.yaml` 的绑定文件已重命名为
  与兼容字符串匹配的名称。

* 文件 ``include/zephyr/drivers/sensor/npm1300_charger.h``
  已移到 :zephyr_file:`include/zephyr/drivers/sensor/npm13xx_charger.h`，
  且将所有 ``NPM1300`` 实例重命名为 ``NPM13XX``

* ``CONFIG_NPM1300_CHARGER`` 已重命名为 :kconfig:option:`CONFIG_NPM13XX_CHARGER`

串行
=======

* ``uart_native_posix`` 已重命名为 ``uart_native_pty``，
  连同其 Kconfig 选项和 DT 绑定。
  :dtcompatible:`zephyr,native-posix-uart` 已弃用，
  由 :dtcompatible:`zephyr,native-pty-uart` 取代。
  :kconfig:option:`CONFIG_UART_NATIVE_POSIX` 及其相关选项
  已改为 :kconfig:option:`CONFIG_UART_NATIVE_PTY`。
  选择项 :kconfig:option:`CONFIG_NATIVE_UART_0`
  已被 :kconfig:option:`CONFIG_UART_NATIVE_PTY_0` 取代，
  但现在也可以在运行时用命令行选项 ``--<uart_name>_stdinout``
  选择 UART 是否连接到进程 stdin/out 而非 PTY。
  :kconfig:option:`CONFIG_NATIVE_UART_AUTOATTACH_DEFAULT_CMD`
  已被 :kconfig:option:`CONFIG_UART_NATIVE_PTY_AUTOATTACH_DEFAULT_CMD` 取代。
  :kconfig:option:`CONFIG_UART_NATIVE_WAIT_PTS_READY_ENABLE` 已弃用。
  它启用的功能现在始终启用，因为没有任何缺点。
  :kconfig:option:`CONFIG_UART_NATIVE_POSIX_PORT_1_ENABLE` 已弃用。
  此选项现在不起作用。
  相反，用户应实例化尽可能多的 :dtcompatible:`zephyr,native-pty-uart` 节点，
  数量等于他们想要的 native PTY UART 实例数。
  （:github:`86739`）

步进电机
=======

* ``stepper_enable(const struct device * dev, bool enable)`` 函数
  已重构为 :c:func:`stepper_enable` 和 :c:func:`stepper_disable`。

定时器
=====

* ``native_posix_timer`` 已重命名为 ``native_sim_timer``，
  因此其 Kconfig 选项 :kconfig:option:`CONFIG_NATIVE_POSIX_TIMER`
  已弃用，由 :kconfig:option:`CONFIG_NATIVE_SIM_TIMER` 取代（:github:`86612`）。

* :dtcompatible:`andestech,machine-timer`、:dtcompatible:`neorv32-machine-timer`、
  :dtcompatible:`telink,machine-timer`、:dtcompatible:`lowrisc,machine-timer`、
  :dtcompatible:`niosv-machine-timer` 和 :dtcompatible:`scr,machine-timer`
  已在 :dtcompatible:`riscv,machine-timer` 下统一。

  ``MTIME`` 和 ``MTIMECMP`` 寄存器的地址现在必须用
  ``reg`` 和 ``reg-names`` 属性显式指定。
  ``reg-names`` 属性现在**必需**，
  且必须列出与 ``reg`` 中每个条目一一对应的名称。
  （:github:`84175` 和 :github:`89847`）

  示例：

  .. code-block:: devicetree

    mtimer: timer@d1000000 {
        compatible = "riscv,machine-timer";
        interrupts-extended = <&cpu0_intc 7>;
        reg = <0xd1000000 0x8
               0xd1000008 0x8>;
        reg-names = "mtime", "mtimecmp";
    };

* 现在可以在 cpus DTS 组中使用 ``timebase-frequency`` 属性
  提供 :kconfig:option:`CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC` 的值，
  而不再使用数值：:github:`91296`

视频
=====

* 8 位 RAW Bayer 格式 BGGR8 / GBRG8 / GRBG8 / RGGB8
  已通过在前面添加 S 前缀重命名：

  ``VIDEO_PIX_FMT_BGGR8`` 变为 :c:macro:`VIDEO_PIX_FMT_SBGGR8`
  ``VIDEO_PIX_FMT_GBRG8`` 变为 :c:macro:`VIDEO_PIX_FMT_SGBRG8`
  ``VIDEO_PIX_FMT_GRBG8`` 变为 :c:macro:`VIDEO_PIX_FMT_SGRBG8`
  ``VIDEO_PIX_FMT_RGGB8`` 变为 :c:macro:`VIDEO_PIX_FMT_SRGGB8`

* 在 STM32 设备上，DCMI 驱动（:dtcompatible:`st,stm32-dcmi`）
  现在依赖基于端点的 video-interfaces.yaml 绑定
  用于传感器接口属性（如总线宽度和同步信号）。
  另外，``capture-rate`` 属性已被帧间隔 API
  :c:func:`video_set_frmival` 的使用替换。
  参见（:github:`89627`）。

* :c:enum:`video_endpoint_id` 已丢弃。
  它不再是任何视频 API 中的参数。

* :c:enum:`video_buf_type` 已添加。
  它是以下视频 API 中的必需参数：
  :c:func:`set_stream`、:c:func:`video_stream_start`、:c:func:`video_stream_stop`

* ``video_format.pitch`` 已更新为由驱动显式设置，
  这是之前应用必需的任务。
  此更新使应用能按驱动正确分配缓冲区大小。
  现有应用不会因此更改被破坏，
  但可以简化，如提交 ``33dcbe37cfd3593e8c6e9cfd218dd31fdd533598``
  中的示例所示。

* 使用 :zephyr:board:`native simulator <native_sim>` 的示例和项目
  现在需要指定 ``--snippet`` :ref:`video-sw-generator <snippet-video-sw-generator>`
  才能正确构建。

* :c:func:`video_query_ctrl` 现在接受单个 :c:struct:`video_ctrl_query` 参数，
  其现在包含 ``video_ctrl_query.dev`` 字段，
  以指定并读回正在查询哪个设备（:github:`91265`）。

看门狗
========
* ``CONFIG_WDT_NPM1300`` 已重命名为 :kconfig:option:`CONFIG_WDT_NPM13XX`，
  ``CONFIG_WDT_NPM1300_INIT_PRIORITY`` 已重命名为
  :kconfig:option:`CONFIG_WDT_NPM13XX_INIT_PRIORITY`

qSPI/oSPI/xSPI
=============

* 在 STM32 设备上，外部存储器的设备树描述
  对大小和地址现在拆分为两个独立属性，
  以符合规范建议。

  例如，以下外部闪存描述
  ``reg = <0x70000000 DT_SIZE_M(64)>; /* 512 Mbits /``
  更改为 ``reg = <0>;`` ``size = <DT_SIZE_M(512)>; / 512 Mbits */``。

  注意该属性给出存储器设备的实际大小（以位计）。
  先前映射地址信息现在在 SoC dtsi 级的
  xspi、ospi 或 qspi 节点中描述。

.. zephyr-keep-sorted-stop

蓝牙
*********

.. zephyr-keep-sorted-start re(^\w)

蓝牙音频
==============

* ``CONFIG_BT_CSIP_SET_MEMBER_NOTIFIABLE`` 已重命名为
  :kconfig:option:`CONFIG_BT_CSIP_SET_MEMBER_SIRK_NOTIFIABLE`。
  （:github:`86763`）

* ``bt_csip_set_member_get_sirk`` 已移除。
  使用 :c:func:`bt_csip_set_member_get_info`
  获取 SIRK（和其他信息）。（:github:`86996`）

* ``BT_AUDIO_CONTEXT_TYPE_PROHIBITED`` 已重命名为
  :c:enumerator:`BT_AUDIO_CONTEXT_TYPE_NONE`。
  （:github:`89506`）

蓝牙经典
=================

* 结构 :c:struct:`bt_hfp_ag_cb` 的 HFP AG 回调 ``sco_disconnected``
  的参数已更改为 SCO 连接对象 ``struct bt_conn *sco_conn``
  和 SCO 连接的分连原因 ``uint8_t reason``。

蓝牙 HCI
=============

* 通过 HCI 驱动接口传递的缓冲区类型
  现在作为缓冲区负载本身的一部分，
  以 H:4 编码前缀字节指示。
  bt_buf_set_type() 和 bt_buf_get_type() 函数已弃用，
  但仍可用，只是每个缓冲区只能调用一次。

* :c:func:`bt_hci_cmd_create` 函数已弃用，
  应改用新的 :c:func:`bt_hci_cmd_alloc` 函数。
  新函数不接受参数，
  因为命令发送函数已更新以进行命令头编码。

蓝牙主机
==============

* :zephyr_file:`include/zephyr/bluetooth/conn.h` 中的符号
  ``BT_LE_CS_TONE_ANTENNA_CONFIGURATION_INDEX_<NUMBER>``
  已重命名为 ``BT_LE_CS_TONE_ANTENNA_CONFIGURATION_A<NUMBER>_B<NUMBER>``。

* ISO 数据路径不再自动设置，
  应用应通过分别调用 :c:func:`bt_iso_setup_data_path` 和
  :c:func:`bt_iso_remove_data_path` 显式设置和移除。
  （:github:`75549`）

* ``BT_ISO_CHAN_TYPE_CONNECTED`` 已拆分为
  ``BT_ISO_CHAN_TYPE_CENTRAL`` 和 ``BT_ISO_CHAN_TYPE_PERIPHERAL``，
  以更好地描述 ISO 通道类型，
  因为每个角色的行为可能不同。
  任何对 ``BT_ISO_CHAN_TYPE_CONNECTED`` 的现有使用/检查
  可用两者的 ``||`` 替换。
  （:github:`75549`）

* :zephyr_file:`include/zephyr/bluetooth/gatt.h` 中的
  ``struct _bt_gatt_ccc`` 已重命名为
  结构 :c:struct:`bt_gatt_ccc_managed_user_data`。
  （:github:`88652`）

* :zephyr_file:`include/zephyr/bluetooth/gatt.h` 中的宏
  ``BT_GATT_CCC_INITIALIZER`` 已重命名为
  :c:macro:`BT_GATT_CCC_MANAGED_USER_DATA_INIT`。
  （:github:`88652`）

* ``CONFIG_BT_ISO_TX_FRAG_COUNT`` Kconfig 选项已移除，
  因为它完全未使用。
  其任何使用可简单移除。
  （:github:`89836`）

.. zephyr-keep-sorted-stop

网络
**********

* 结构 ``net_linkaddr_storage`` 已重命名为结构 :c:struct:`net_linkaddr`，
  旧结构 ``net_linkaddr`` 已移除。
  结构 :c:struct:`net_linkaddr` 现在包含存储链路地址的空间，
  而非指向链路地址的指针。
  这避免了克隆结构 :c:struct:`net_pkt` 时可能的悬空指针。
  这将使 IEEE 802.15.4 的结构 :c:struct:`net_pkt` 大小增加 4 个八位组，
  但对以太网等其他网络技术无大小增加。
  注意任何直接使用结构 :c:struct:`net_linkaddr`
  且带有 ``if (lladdr->addr == NULL)`` 等检查的代码
  将不再按预期工作（因为 addr 不是指针），
  如果代码想检查链路地址未设置，
  必须更改为 ``if (lladdr->len == 0)``。

* TLS 凭据类型 ``TLS_CREDENTIAL_SERVER_CERTIFICATE``
  已重命名为更通用的 :c:enumerator:`TLS_CREDENTIAL_PUBLIC_CERTIFICATE`，
  以更好地反映此凭据类型的用途。

* MQTT 公共 API 函数 :c:func:`mqtt_disconnect` 已更改。
  该函数现在接受额外的 ``param`` 参数以支持 MQTT 5.0 情况。
  参数是可选的，不与较旧 MQTT 版本（MQTT 3.1.1）一起使用
  ——MQTT 3.1.1 用户应传 NULL 作为参数。

* ``AF_PACKET/SOCK_RAW/IPPROTO_RAW`` socket 组合不再支持，
  因为 ``AF_PACKET`` socket 应仅接受 IEEE 802.3 协议号。
  作为替代，可使用 ``AF_PACKET/SOCK_DGRAM/ETH_P_ALL``
  或 ``AF_INET(6)/SOCK_RAW/IPPROTO_IP`` socket，
  取决于实际用例。

* HTTP 服务器现在尊重配置的 ``_concurrent`` 和 ``_backlog`` 值。
  检查你为 :c:macro:`HTTP_SERVICE_DEFINE_EMPTY`、
  :c:macro:`HTTPS_SERVICE_DEFINE_EMPTY`、:c:macro:`HTTP_SERVICE_DEFINE`
  和 :c:macro:`HTTPS_SERVICE_DEFINE` 提供适用值。

* :kconfig:option:`CONFIG_NET_ZPERF` 不再默认包含服务器支持。
  要使用服务器命令，启用 :kconfig:option:`CONFIG_NET_ZPERF_SERVER`。
  如果不需要服务器支持，:kconfig:option:`CONFIG_ZVFS_POLL_MAX`
  可能可以减少。

* L2 Wi-Fi shell 现在支持大多数命令的接口选项，
  为适应此更改，某些现有选项已重命名。
  以下表格总结更改：

  +------------------------+---------------------+--------------------+
  | 命令                   | 旧选项              | 新选项             |
  +------------------------+---------------------+--------------------+
  | ``wifi connect``       | ``-i``              | ``-g``             |
  | ``wifi ap enable``     |                     |                    |
  +------------------------+---------------------+--------------------+
  | ``wifi twt setup``     | ``-i``              | ``-p``             |
  +------------------------+---------------------+--------------------+
  | ``wifi ap config``     | ``-i``              | ``-t``             |
  +------------------------+---------------------+--------------------+
  | ``wifi mode``          | ``--if-index``      | ``--iface``        |
  | ``wifi channel``       |                     |                    |
  | ``wifi packet_filter`` |                     |                    |
  +------------------------+---------------------+--------------------+

* :c:type:`http_response_cb_t` HTTP 客户端响应回调签名已更改。
  回调函数现在返回 ``int`` 而非 ``void``。
  这允许应用中止 HTTP 连接。
  现有应用需更新其响应回调实现。
  要保持当前行为，仅从回调返回 0。

* ``net_mgmt`` 事件处理器 :c:type:`net_mgmt_event_handler_t`
  和请求处理器 :c:type:`net_mgmt_request_handler_t` 的 API 签名已更改。
  管理事件类型从 ``uint32_t`` 改为 ``uint64_t``。
  此更改允许事件编号值为位掩码而非枚举值。
  层代码仍保持为枚举值。
  如需从请求或事件处理器中的实际事件值获取层代码和管理事件命令，
  可使用 :c:macro:`NET_MGMT_LAYER_CODE` 和 :c:macro:`NET_MGMT_GET_COMMAND`。

* ``net_mgmt`` 类型 socket 的 socket 选项
  不能直接是网络管理事件类型，
  因为那些现在是 ``uint64_t``，
  且 socket 选项期望常规 32 位整数值。
  因此，创建新的 ``SO_NET_MGMT_ETHERNET_SET_QAV_PARAM``
  和 ``SO_NET_MGMT_ETHERNET_GET_QAV_PARAM`` socket 选项，
  将替换先前使用的 ``NET_REQUEST_ETHERNET_SET_QAV_PARAM``
  和 ``NET_REQUEST_ETHERNET_GET_QAV_PARAM`` 选项。

* DNS 服务器解析器配置函数 :c:func:`dns_resolve_reconfigure`
  和 :c:func:`dns_resolve_reconfigure_with_interfaces`
  现在需要用户提供 DNS 服务器信息的来源。
  例如当 DNS 服务器信息通过 DHCPv4 接收时，
  需指定 :c:enumerator:`DNS_SOURCE_DHCPV4`。

.. zephyr-keep-sorted-start re(^\w)

LwM2M
=====

* 加速度计对象：可选资源 Y 值、Z 值、最小范围值、最大范围值
  现在可按加速度计对象的规范可选使用。
  这些资源的用户现在需提供读缓冲区。

OpenThread
==========

* Zephyr 中的 OpenThread 协议栈集成经历了重大重构。
  实现已从 Zephyr 网络层（``subsys/net/l2/openthread/``）
  移到专用模块（``modules/openthread/``）。

* OpenThread 现在是 Zephyr 中的独立模块。
  它可独立于 Zephyr 的网络协议栈
  （L2 和 IEEE802.15.4 shim 层）使用。
  这启用了新用例，
  如直接使用其自身 IEEE802.15.4 驱动使用 OpenThread 的应用，
  或不需要完整 Zephyr 网络协议栈的应用。

* :zephyr_file:`include/zephyr/net/openthread.h` 文件中的大多数函数已弃用。
  这些弃用 API 仍可用于向后兼容，
  但新应用应使用 OpenThread 模块提供的新 API。
  以下列表总结更改：

  * 互斥锁处理：

    * 之前：

      * ``openthread_api_mutex_lock``
      * ``openthread_api_mutex_try_lock``
      * ``openthread_api_mutex_unlock``

    * 现在使用：

      * :c:func:`openthread_mutex_lock`
      * :c:func:`openthread_mutex_try_lock`
      * :c:func:`openthread_mutex_unlock`

  * OpenThread 启动：

    * 之前：``openthread_start``
    * 现在使用：:c:func:`openthread_run`

  * 回调注册：

    * 之前：

      * ``openthread_state_changed_cb_register``
      * ``openthread_state_changed_cb_unregister``

    * 现在使用：

      * :c:func:`openthread_state_changed_callback_register`
      * :c:func:`openthread_state_changed_callback_unregister`

  * 回调结构：

    * 之前：``openthread_state_changed_cb``
    * 现在使用：:c:struct:`openthread_state_changed_callback`

  * 以下 :c:struct:`openthread_context` 结构字段已弃用，
    不应再在新代码中使用：

    * ``instance``
    * ``api_lock``
    * ``work_q``
    * ``api_work``
    * ``state_change_cbs``

  * 之前不存在的新函数：

    * :c:func:`openthread_init` 初始化 OpenThread 协议栈。
    * :c:func:`openthread_stop` 停止并禁用 OpenThread 协议栈。
    * :c:func:`openthread_set_receive_cb`
      设置 OpenThread 协议栈的接收回调。

* ``subsys/net/l2/openthread/Kconfig`` 中的 OpenThread 相关 Kconfig 选项
  已移到 :zephyr_file:`modules/openthread/Kconfig`。
  所有 Kconfig 选项保持不变。
  你可像以前一样使用它们，
  但要修改它们，请在 menuconfig 或 guiconfig 中使用新路径。

* 如果启用 :kconfig:option:`CONFIG_NET_L2_OPENTHREAD` Kconfig 选项，
  Zephyr 的 L2 层将使用新的 OpenThread 模块 API 作为其后端。
  L2 层不再自己实现 OpenThread，
  而将实现委托给模块。

* 对通过 Zephyr 网络协议栈使用 OpenThread 的现有应用：

  * 你的应用应继续工作，因为旧 API 仍可用于兼容。
    但鼓励你迁移到新 API 以面向未来，
    并使用新的模块化结构。
  * 更新对 OpenThread Kconfig 选项的任何引用，
    在你的配置工具中使用新路径（``modules/openthread/Kconfig``）。

* 对使用 :c:struct:`openthread_context` 或其他弃用 API 的应用：

  * 开始迁移到新 API。
    弃用 API 将在未来版本中移除。
  * 避免直接使用 :c:struct:`openthread_context` 和相关字段；
    改用新的初始化和回调注册函数。

* 对新应用或不用 Zephyr L2 使用 OpenThread 的应用：

  * 使用新的初始化（:c:func:`openthread_init`）、
    运行（:c:func:`openthread_run`）
    和回调注册 API（:c:func:`openthread_state_change_callback_register`）。
  * 如果你的用例允许，现在可直接使用 OpenThread，
    无需启用 Zephyr 的 L2 或 IEEE802.15.4 层。

.. zephyr-keep-sorted-stop


其他子系统
****************

.. zephyr-keep-sorted-start re(^\w)

Modbus
======

* :c:struct:`modbus_serial_param` 中的 ``client_stop_bits`` 字段
  已重命名为 ``stop_bits``。
  该设置在客户端和服务器模式下均有效。
* 自定义停止位设置默认禁用，
  应由 :kconfig:option:`CONFIG_MODBUS_NONCOMPLIANT_SERIAL_MODE` 启用。

状态机框架
======================

* :c:func:`smf_set_handled` 已移除。
* 状态运行动作现在返回 :c:enum:`smf_state_result` 值而非 void，
  且返回码决定事件是否传播到父运行动作或已处理。
  完全处理事件的运行动作应返回 :c:enum:`SMF_EVENT_HANDLED`，
  将处理传播到父状态的运行动作应返回 :c:enum:`SMF_EVENT_PROPAGATE`。
* 扁平状态机忽略返回值；
  返回 :c:enum:`SMF_EVENT_HANDLED` 将是最技术准确的响应。

hawkBit
=======

* 当启用 :kconfig:option:`CONFIG_HAWKBIT_CUSTOM_DEVICE_ID` 时，
  device_id 不再前缀 :kconfig:option:`CONFIG_BOARD`。
  是用户的责任写回调在需要时前缀开发板名称。

.. zephyr-keep-sorted-stop

模块
*******

.. zephyr-keep-sorted-start re(^\w)

CMSIS
=====

* Cortex-M 开发板/SoC 现在需要 ``CMSIS_6`` 模块才能正确构建
  （而非 ``cmsis``，其为 CMSIS 5.9.0）。
  如果尝试构建 Cortex-M 开发板，
  执行 ``west update`` 确保 ``CMSIS_6`` 模块
  在运行 ``west build`` 或其他命令前可用。

  使用较旧 ``cmsis`` 模块的开发板、SoC 或模块
  （无论用本地副本还是通过
  :kconfig:option:`CONFIG_ZEPHYR_CMSIS_MODULE_DIR`）
  请求迁移到 ``CMSIS_6`` 模块，
  其可通过 :kconfig:option:`CONFIG_ZEPHYR_CMSIS_6_MODULE_DIR`
  配置访问。

  注意：Zephyr 将继续为 Cortex-A 和 Cortex-R 目标
  使用较旧 ``cmsis`` 模块。

.. zephyr-keep-sorted-stop

架构
*************

* 将 :kconfig:option:`CONFIG_SRAM_VECTOR_TABLE`
  从 ``zephyr/Kconfig.zephyr`` 移到 ``zephyr/arch/Kconfig``，
  并添加对 :kconfig:option:`CONFIG_XIP`、
  :kconfig:option:`CONFIG_ARCH_HAS_VECTOR_TABLE_RELOCATION`
  和 :kconfig:option:`CONFIG_ROMSTART_RELOCATION_ROM` 的依赖，
  以支持 RAM 中向量表的重定位。
* 将 :kconfig:option:`CONFIG_DEBUG_INFO`
  重命名为 :kconfig:option:`CONFIG_X86_DEBUG_INFO`，
  以更好地反映其用途。
  此选项现在仅对 x86 架构可用。
