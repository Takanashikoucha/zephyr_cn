:orphan:

..
  参见
  https://docs.zephyrproject.org/latest/releases/index.html#migration-guides
  了解本文档应包含的内容。

.. _migration_4.1:

Zephyr v4.1.0 迁移指南
######################

本文档描述了将应用从 Zephyr v4.0.0 迁移到 Zephyr v4.1.0 所需的更改。

其他更改（与迁移应用无直接关系）可在
:ref:`发布说明<zephyr_4.1>` 中查看。

.. contents::
    :local:
    :depth: 2

构建系统
************

* 已移除对 Zephyr 3.6 中弃用的构建类型功能的支持，
  :ref:`application-file-suffixes`/:ref:`sysbuild_file_suffixes` 已取代该功能。

* Sysbuild

  * Kconfig 选项 ``SB_CONFIG_MCUBOOT_MODE_SWAP_WITHOUT_SCRATCH`` 已弃用，
    并被 ``SB_CONFIG_MCUBOOT_MODE_SWAP_USING_MOVE`` 取代。如果应用之前选择了旧选项，
    应更新为选择新选项。

BOSSA Runner
=============

``bossac`` runner 在烧录时默认不再执行完整擦除。
要执行完整擦除，请在执行 ``west flash`` 时传入 ``--erase`` 选项。

内核
******


k_pipe API
==========

k_pipe API 已重新设计，``CONFIG_PIPES`` 中使用的 API 现已弃用。
当 ``CONFIG_MULTITHREADING`` 启用时，k_pipe API 默认启用。
函数重命名和修改如下：

.. list-table::
   :header-rows: 1

   * - 旧 API
     - 新 API
     - 更改
   * - ``k_pipe_put(..)``
     - ``k_pipe_write(..)``
     - 移除了 ``min_xfer`` 参数（不再支持基于阈值的部分传输），
       ``bytes_written`` 现在是返回值
   * - ``k_pipe_get(..)``
     - ``k_pipe_read(..)``
     - 移除了 ``min_xfer`` 参数（不再支持基于阈值的部分传输），
       ``bytes_read`` 现在是返回值
   * - ``k_pipe_flush(..)`` 和 ``k_pipe_buffer_flush(..)``
     - ``k_pipe_reset(..)``
     - 重置管道，丢弃管道中的所有数据，非阻塞。
   * - ``k_pipe_alloc_init(..)``、``k_pipe_cleanup(..)``
     - **已移除**
     - 不再支持管道的动态分配
   * - ``k_pipe_read_avail(..)``、``k_pipe_write_avail(..)``
     - **已移除**
     - 不再支持查询管道中的字节数
   * - 无
     - ``k_pipe_close(..)``
     - 关闭管道，唤醒所有挂起的读者和写者并返回错误码。
       之后不允许再对该管道进行读写。
       可再次调用 ``k_pipe_init(..)`` 重新打开管道。
       **注意**，管道中的所有数据在管道被清空之前对读者可用。


安全
********

* 新增了栈金丝雀（stack canaries）选项，为用户提供对栈保护的更精细控制。
  由于此更改，:kconfig:option:`CONFIG_STACK_CANARIES` 不再启用
  编译器选项 ``-fstack-protector-all``。希望使用该选项的用户现在必须启用
  :kconfig:option:`CONFIG_STACK_CANARIES_ALL`。

开发板
******

* Shield ``mikroe_weather_click`` 现在同时支持 I2C 和 SPI 接口。
  用户应使用 ``mikroe_weather_click_i2c`` 或 ``mikroe_weather_click_spi``
  代替 ``mikroe_weather_click`` 来选择所需配置。

* 所有基于 nRF52 的开发板在使用 ``west flash`` 烧录时，
  现在默认使用软（系统）复位而非引脚复位。
  如果希望在 nRF52 系列芯片上继续使用引脚复位，可使用 ``west flash --pinreset``。

* 在 nRF52 和 nRF53 系列上使用 ``west flash`` 烧录新固件映像时，
  擦除外置存储现在始终正确遵循 ``--erase`` 标志（及其缺失），
  无论使用 ``nrfjprog`` 还是 ``nrfutil`` 后端均如此。
  在此版本之前，``nrjfprog`` 后端总是只擦除外置闪存中新固件使用的扇区，
  而 ``nrfutil`` 后端总是擦除整个外置闪存。

* ``stm32f4_disco`` 上的 CAN1 和 USART1 已禁用，
  因为 I2C1 上存在引脚冲突，I2C1 现在用于控制连接到音频插孔输出的音频编解码器。

设备树
**********

* :dtcompatible:`microchip,cap1203` 驱动器的兼容字符串已更改为
  :dtcompatible:`microchip,cap12xx`，并已更新以支持多通道。
  可用通道数从设备树数组属性 ``input-codes`` 的长度推导而来。
  :kconfig:option:`CONFIG_INPUT_CAP1203_POLL` 已移除：
  如果设备树属性 ``int-gpios`` 存在，则使用中断模式，否则使用轮询模式。
  :kconfig:option:`CONFIG_INPUT_CAP1203_PERIOD` 已被设备树属性
  ``poll-interval-ms`` 取代。
  在中断模式下，支持设备树属性 ``repeat``。

树莓派
=============

* ``CONFIG_SOC_SERIES_RP2XXX`` 已重命名为 :kconfig:option:`CONFIG_SOC_SERIES_RP2040`。

STM32
=====

* MCO 时钟源和预分频器现在完全由 DTS 配置（如之前引入的那样）。
  Kconfig 配置方法现已移除。

* ADC 属性 ``st,adc-sequencer`` 和 ``st,adc-clock-source`` 现在使用
  字符串值而非整数值。

模块
*******

Mbed TLS
========

* 如果平台有 CSPRNG 源可用（即 :kconfig:option:`CONFIG_CSPRNG_ENABLED`
  已设置），则 Kconfig 选项 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_EXTERNAL_RNG`
  是随机数源的默认选择，取代
  :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_LEGACY_RNG`。
  这有助于减少 Mbed TLS 库的 ROM/RAM 占用。

* 新增的 Kconfig 选项 :kconfig:option:`CONFIG_MBEDTLS_PSA_KEY_SLOT_COUNT`
  用于指定 PSA Crypto 核心中可用的密钥槽数量。
  之前该值未显式设置，因此使用 Mbed TLS 的默认值 32。
  新 Kconfig 选项默认值为 16，以在 RAM 消耗和常见用例之间找到合理折中。
  如果最终应用不需要那么多密钥槽，可进一步降低以减少 RAM 消耗。

Trusted Firmware-M
==================

LVGL
====

* 配置选项 :kconfig:option:`CONFIG_LV_Z_FLUSH_THREAD_PRIO` 现已更名为
  :kconfig:option:`CONFIG_LV_Z_FLUSH_THREAD_PRIORITY`，
  其值现在解释为绝对优先级而非协作式优先级。

* 配置选项 :kconfig:option:`CONFIG_LV_Z_VBD_CUSTOM_SECTION` 现已更名为
  :kconfig:option:`CONFIG_LV_Z_VDB_CUSTOM_SECTION`。

设备驱动程序和设备树
*****************************

* 设备驱动程序 API 已放入可迭代部分（:github:`71773` 和 :github:`82102`），
  以支持运行时检查。详见 :ref:`device_driver_api`。
  树外驱动程序实现应使用 :c:macro:`DEVICE_API()` 宏
  来定义所有上游驱动类。

ADC
===

* 兼容字符串 ``compatible`` 已从 ``nxp,kinetis-adc12`` 重命名为 :dtcompatible:`nxp,adc12`。

时钟
=====
* 设备树属性 ``freqs_mhz`` 已重命名为 ``freqs-mhz``。
* 设备树属性 ``cg_reg`` 已重命名为 ``cg-reg``。
* 设备树属性 ``pll_ctrl_reg`` 已重命名为 ``pll-ctrl-reg``。

计数器
=======

* 设备树属性 ``primary_source`` 已重命名为 ``primary-source``。
* 设备树属性 ``secondary_source`` 已重命名为 ``secondary-source``。
* 设备树属性 ``filter_count`` 已重命名为 ``filter-count``。
* 设备树属性 ``filter_period`` 已重命名为 ``filter-period``。

控制器局域网（CAN）
=============================

* :dtcompatible:`infineon,xmc4xxx-can-node` 的设备树属性 ``clock_div8``
  已重命名为 ``clock-div8``（:github:`83782`）。

显示
=======

* 使用 MIPI DBI 驱动且通过设备树 ``mipi-mode`` 属性设置 MIPI DBI 模式的显示屏，
  现在应使用同名的字符串属性，如下所示：

  .. code-block:: devicetree

     /* 旧显示屏定义 */

     st7735r: st7735r@0 {
         ...
         mipi-mode = <MIPI_DBI_MODE_SPI_4WIRE>;
         ...
     };

     /* 新显示屏定义 */

     st7735r: st7735r@0 {
         ...
         mipi-mode = "MIPI_DBI_MODE_SPI_4WIRE";
         ...
     };

* 设备树属性 ``pclk_pol`` 和 ``data_cmd-gpios``
  已重命名为 ``pclk-pol`` 和 ``data-cmd-gpios``。

DAC
===

* 设备树属性 ``voltage_reference`` 和 ``power_down_mode``
  已重命名为 ``voltage-reference`` 和 ``power-down-mode``。

增强串行外设接口（eSPI）
===========================================

熵源
=======

* 基于 BT HCI 的熵源驱动现在直接发送 HCI 命令来解析随机数据，
  而不再等待 BT 连接就绪。
  这对于 BT 控制器拥有硬件随机数生成器、应用处理器需要在 BT 完全启用前
  获取随机数据的平台很有帮助。
  （:github:`79931`）

以太网
========

* 已移除弃用的 eth_mcux 驱动。
* Silabs gecko 以太网更改：

  * 设备树属性 ``location-phy_mdc`` 已重命名为 ``location-phy-mdc``。
  * 设备树属性 ``location-phy_mdio`` 已重命名为 ``location-phy-mdio``。
  * 设备树属性 ``location-rmii_refclk`` 已重命名为 ``location-phy-refclk``。
  * 设备树属性 ``location-rmii_crs_dv`` 已重命名为 ``location-phy-crs-dv``。
  * 设备树属性 ``location-rmii_txd0`` 已重命名为 ``location-phy-txd0``。
  * 设备树属性 ``location-rmii_txd1`` 已重命名为 ``location-phy-txd1``。
  * 设备树属性 ``location-rmii_tx_en`` 已重命名为 ``location-phy-tx-en``。
  * 设备树属性 ``location-rmii_rxd0`` 已重命名为 ``location-phy-rxd0``。
  * 设备树属性 ``location-rmii_rxd1`` 已重命名为 ``location-phy-rxd1``。
  * 设备树属性 ``location-rmii_rx_er`` 已重命名为 ``location-phy-rx-er``。
  * 设备树属性 ``location-phy_pwr_enable`` 已重命名为 ``location-phy-pwr-enable``。
  * 设备树属性 ``location-phy_reset`` 已重命名为 ``location-phy-reset``。
  * 设备树属性 ``location-phy_interrupt`` 已重命名为 ``location-phy-interrupt``。

GNSS
====

GPIO
====

* 设备树属性 ``pin_mask`` 已重命名为 ``pin-mask``。
* 设备树属性 ``pinmux_mask`` 已重命名为 ``pinmux-mask``。
* 设备树属性 ``vbatts_pins`` 已重命名为 ``vbatts-pins``。
* 设备树属性 ``bit_per_gpio`` 已重命名为 ``bit-per-gpio``。
* 设备树属性 ``off_val`` 已重命名为 ``off-val``。
* 设备树属性 ``on_val`` 已重命名为 ``on-val``。
* 兼容字符串 ``compatible`` 已从 ``ti,ads114s0x-gpio`` 重命名为 :dtcompatible:`ti,ads1x4s0x-gpio`。

硬件自旋锁
==========

* 设备树属性 ``num_locks`` 已重命名为 ``num-locks``。

I2C
===

* 兼容字符串 ``compatible`` 已从 ``nxp,imx-lpi2c`` 重命名为 :dtcompatible:`nxp,lpi2c`。
* 设备树属性 ``port_sel`` 已重命名为 ``port-sel``。

I2S
===

* 设备树属性 ``fifo_depth`` 已重命名为 ``fifo-depth``。

输入
=====

LED
===

* 设备树属性 ``max_curr_opt`` 已重命名为 ``max-curr-opt``。

PWM
===

* 兼容字符串 ``compatible`` 已从 ``renesas,ra8-pwm`` 重命名为 :dtcompatible:`renesas,ra-pwm`。

中断控制器
==================

LED 灯带
=========

杂项
====

* ft8xx 驱动中的所有函数现在接受额外的 ``const struct *device`` 参数，
  以支持驱动的多实例。

  例外是定义在
  :zephyr_file:`include/zephyr/drivers/misc/ft8xx/ft8xx_reference_api.h` 文件中的
  函数和宏，它们将 API 转换为单实例模型，与 FT8xx 编程指南中定义的 API 兼容。
  这些函数未做修改。

* :c:func:`ft8xx_register_int` 函数现在接受额外的 ``void *user_data`` 参数，
  以便将用户定义的数据传递给中断处理程序。
  此外，ft8xx 中断处理程序的签名已更改，
  包含 ``void *user_data`` 参数。

MMU/MPU
=======

* 兼容字符串 ``compatible`` 已从 ``nxp,kinetis-mpu`` 重命名为 :dtcompatible:`nxp,sysmpu`，
  并添加了对应的绑定。
* Kconfig 选项 ``CPU_HAS_NXP_MPU`` 已重命名为 :kconfig:option:`CPU_HAS_NXP_SYSMPU`。

引脚控制
===========

  * 兼容字符串 ``compatible`` 已从 ``nxp,kinetis-pinctrl`` 重命名为 :dtcompatible:`nxp,port-pinctrl`。
  * 兼容字符串 ``compatible`` 已从 ``nxp,kinetis-pinmux`` 重命名为 :dtcompatible:`nxp,port-pinmux`。
  * Silabs Series 2 设备现在使用由 :dtcompatible:`silabs,dbus-pinctrl`
    选择的新引脚控制驱动。该驱动允许通过设备树配置 GPIO 属性，
    而不是为每个支持的信号硬编码。它还包括
    :zephyr_file:`include/zephyr/dt-bindings/pinctrl/silabs/xg24-pinctrl.h`
    等绑定头文件，以支持所有可能的数字总线信号。

    引脚控制现在应如下配置：

    .. code-block:: devicetree

      #include <zephyr/dt-bindings/pinctrl/silabs/xg24-pinctrl.h>

      &pinctrl {
        i2c0_default: i2c0_default {
          group0 {
            /* 使用上述包含的绑定进行引脚选择 */
            pins = <I2C0_SDA_PD2>, <I2C0_SCL_PD3>;
            /* 引脚组的共享属性 */
            drive-open-drain;
            bias-pull-up;
          };
        };
      };


PWM
===

* 兼容字符串 ``compatible`` 已从 ``nxp,kinetis-ftm-pwm`` 重命名为 :dtcompatible:`nxp,ftm-pwm`。

SDHC
====

* 设备树属性 ``power_delay_ms`` 已重命名为 ``power-delay-ms``
* 设备树属性 ``max_current_330`` 已重命名为 ``max-current-330``

传感器
=======

  * :dtcompatible:`we,wsen-pads` 驱动已重命名为
    :dtcompatible:`we,wsen-pads-2511020213301`。
    设备树可配置如下：

    .. code-block:: devicetree

      &i2c0 {
        pads:pads-2511020213301@5d {
          compatible = "we,wsen-pads-2511020213301";
          reg = <0x5d>;
          odr = <10>;
          interrupt-gpios = <&gpio1 1 GPIO_ACTIVE_HIGH>;
        };
      };

  * :dtcompatible:`we,wsen-pdus` 驱动已重命名为
    :dtcompatible:`we,wsen-pdus-25131308XXXXX`。
    设备树可配置如下：

    .. code-block:: devicetree

      &i2c0 {
        pdus:pdus-25131308XXXXX@78 {
          compatible = "we,wsen-pdus-25131308XXXXX";
          reg = <0x78>;
          sensor-type = <4>;
        };
      };

  * :dtcompatible:`we,wsen-tids` 驱动已重命名为
    :dtcompatible:`we,wsen-tids-2521020222501`。
    设备树可配置如下：

    .. code-block:: devicetree

      &i2c0 {
        tids:tids-2521020222501@3F {
          compatible = "we,wsen-tids-2521020222501";
          reg = <0x3F>;
          odr = <25>;
          interrupt-gpios = <&gpio1 1 GPIO_ACTIVE_LOW>;
        };
      };

  * :dtcompatible:`invensense,icp10125` 驱动已重命名为
    :dtcompatible:`invensense,icp101xx`。
    设备树可配置如下：

    .. code-block:: devicetree

      &i2c0 {
        icp101xx:icp101xx@63 {
           compatible = "invensense,icp101xx";
           reg = <0x63>;
        };
      };

串行
======

* 兼容字符串 ``compatible`` 已从 ``nxp,kinetis-lpuart`` 重命名为 :dtcompatible:`nxp,lpuart`。
* Silabs USART 驱动已拆分为 Series 2 的 :dtcompatible:`silabs,usart-uart`
  和 Series 0/1 的 ``silabs,gecko-usart``

步进电机
=======

  * 兼容字符串 ``compatible`` 已从 ``zephyr,gpio-steppers`` 重命名为 :dtcompatible:`zephyr,gpio-stepper`。
  * ``stepper_set_actual_position`` 函数已重命名为 :c:func:`stepper_set_reference_position`。
  * ``stepper_enable_constant_velocity_mode`` 函数已重命名为 :c:func:`stepper_run`。
    该函数不再接受速度参数。请事先使用
    :c:func:`stepper_set_microstep_interval` 函数设置期望速度。
  * ``stepper_move`` 函数已重命名为 :c:func:`stepper_move_by`。
  * ``stepper_set_target_position`` 函数已重命名为 :c:func:`stepper_move_to`。
  * ``stepper_set_max_velocity`` 函数已重命名为 :c:func:`stepper_set_microstep_interval`。
    该函数现在接受以纳秒为单位的步进间隔，以实现更精确的控制。
  * 通过 :c:func:`stepper_run` 设置最大速度的方法已弃用。
  * :kconfig:option:`STEPPER_ADI_TMC_RAMP_GEN` 已弃用，
    由新的 :kconfig:option:`STEPPER_ADI_TMC50XX_RAMP_GEN` 选项取代。
  * tmc5041 步进电机驱动已重命名为 tmc50xx。
  * 要控制 :dtcompatible:`adi,tmc50xx` 步进电机驱动的速度，
    使用 :c:func:`tmc50xx_stepper_set_max_velocity` 或 :c:func:`tmc50xx_stepper_set_ramp`。
  * 设备树属性 ``en_spreadcycle`` 已重命名为 ``en-spreadcycle``。
  * 设备树属性 ``i_scale_analog`` 已重命名为 ``i-scale-analog``。
  * 设备树属性 ``index_optw`` 已重命名为 ``index-otpw``。
  * 设备树属性 ``ìndex_step`` 已重命名为 ``index-step``。
  * 设备树属性 ``internal_rsense`` 已重命名为 ``internal-rsense``。
  * 设备树属性 ``lock_gconf`` 已重命名为 ``lock-gconf``。
  * 设备树属性 ``mstep_reg_select`` 已重命名为 ``mstep-reg-select``。
  * 设备树属性 ``pdn_disable`` 已重命名为 ``pdn-disable``。
  * 设备树属性 ``poscmp_enable`` 已重命名为 ``poscmp-enable``。
  * 设备树属性 ``test_mode`` 已重命名为 ``test-mode``。

SPI
===

* 兼容字符串 ``compatible`` 已从 ``nxp,imx-lpspi`` 重命名为 :dtcompatible:`nxp,lpspi`。
* 兼容字符串 ``compatible`` 已从 ``nxp,kinetis-dspi`` 重命名为 :dtcompatible:`nxp,dspi`。
* 兼容字符串 ``compatible`` 已从 ``silabs,gecko-spi-usart`` 重命名为 :dtcompatible:`silabs,usart-spi`。
* 兼容字符串 ``compatible`` 已从 ``silabs,gecko-spi-eusart`` 重命名为 :dtcompatible:`silabs,eusart-spi`。

稳压器
=========

RTC
===

* 兼容字符串 ``compatible`` 已从 ``nxp,kinetis-rtc`` 重命名为 :dtcompatible:`nxp,rtc`。

定时器
=====

* 兼容字符串 ``compatible`` 已从 ``nxp,kinetis-ftm`` 重命名为 :dtcompatible:`nxp,ftm`，
  并移到 ``dts/bindings/timer`` 下。
* 设备树属性 ``ticks_us`` 已重命名为 ``ticks-us``。

USB
===

* 设备树属性 ``phy_handle`` 已重命名为 ``phy-handle``。

视频
=====

* :file:`include/zephyr/drivers/video-controls.h` 已更新，
  视频控制 ID（CID）与 Linux 内核文件
  ``include/uapi/linux/v4l2-controls.h`` 中的定义匹配。
  大多数情况下，去掉类别前缀即可：``VIDEO_CID_CAMERA_GAIN`` 变为
  ``VIDEO_CID_GAIN``。
  新的 ``video-controls.h`` 源文件现在包含每个控制 ID 的描述，
  以帮助消除歧义。

* ``video_pix_fmt_bpp()`` 函数之前返回字节数，
  现已由返回位数的 ``video_bits_per_pixel()`` 取代。
  例如，``pitch = width * video_pix_fmt_bpp(pixfmt)`` 这样的调用
  需要替换为等效的
  ``pitch = width * video_bits_per_pixel(pixfmt) / BITS_PER_BYTE``。

* 视频 API 中的 :c:func:`video_buffer_alloc` 和 :c:func:`video_buffer_aligned_alloc`
  函数现在接受额外的超时参数。

* 驱动 API :c:func:`video_stream_start` 和 :c:func:`video_stream_stop`
  现已合并到新的 :c:func:`video_set_stream` 驱动 API 中。
  用户 API 保持不变，以与下游应用保持向后兼容。

看门狗
========

* 兼容字符串 ``compatible`` 已从 ``nxp,kinetis-wdog32`` 重命名为 :dtcompatible:`nxp,wdog32`。

Wi-Fi
=====

* 配置选项 :kconfig:option:`CONFIG_NXP_WIFI_BUILD_ONLY_MODE` 和
  :kconfig:option:`CONFIG_NRF_WIFI_BUILD_ONLY_MODE` 现已统一为
  :kconfig:option:`CONFIG_BUILD_ONLY_NO_BLOBS`，
  作为任何厂商启用无 blob 构建的通用入口点。

蓝牙
*********

蓝牙 HCI
=============

* :kconfig:option:`BT_CTLR` 已弃用。
  新引入的 :kconfig:option:`HAS_BT_CTLR` 应由相应的链路层 Kconfig 选项
  （例如 HCI 驱动选项或上游控制器的选项）选择。
  建议所有本地链路层的 HCI 驱动都选择新选项，
  因为这开启了指示构建时支持特定功能的可能性，例如主机协议栈可以利用。

蓝牙 Mesh
=============

* 随着 TinyCrypt 加密库弃用流程的开始，
  Kconfig 符号 :kconfig:option:`CONFIG_BT_MESH_USES_TINYCRYPT` 已设为弃用。
  不支持 TF-M 的平台默认选项为 :kconfig:option:`CONFIG_BT_MESH_USES_MBEDTLS_PSA`。

* 如果映像使用 TinyCrypt 和基于 PSA API 的加密库构建，
  Mesh 密钥表示不向后兼容。
  Mesh 不再为这些加密库存储密钥值，
  加密库将密钥存储在内部可信存储中。
  如果已配对的设备要更新其映像——该映像使用
  :kconfig:option:`CONFIG_BT_MESH_USES_TINYCRYPT` Kconfig 选项构建，
  而新映像使用 :kconfig:option:`CONFIG_BT_MESH_USES_MBEDTLS_PSA` 或
  :kconfig:option:`CONFIG_BT_MESH_USES_TFM_PSA` 构建——
  且未擦除持久存储区域，则应先解除配对，更新后再重新配对。
  如果映像通过 Mesh DFU 更改，使用 :c:enumerator:`BT_MESH_DFU_EFFECT_UNPROV`。

* 如果启用了存储到非易失性内存（:kconfig:option:`CONFIG_BT_SETTINGS`）
  且使用了 Mbed TLS 库（:kconfig:option:`CONFIG_BT_MESH_USES_MBEDTLS_PSA`），
  Mesh 明确依赖于安全存储子系统。
  应用应启用 :kconfig:option:`CONFIG_SECURE_STORAGE` 进行构建。

蓝牙音频
==============

* 以下 Kconfig 选项不再由 LE Audio Kconfig 选项自动启用，
  可能需要手动启用（:github:`81328`）：

    * :kconfig:option:`CONFIG_BT_GATT_CLIENT`
    * :kconfig:option:`CONFIG_BT_GATT_AUTO_DISCOVER_CCC`
    * :kconfig:option:`CONFIG_BT_GATT_AUTO_UPDATE_MTU`
    * :kconfig:option:`CONFIG_BT_EXT_ADV`
    * :kconfig:option:`CONFIG_BT_PER_ADV_SYNC`
    * :kconfig:option:`CONFIG_BT_ISO_BROADCASTER`
    * :kconfig:option:`CONFIG_BT_ISO_SYNC_RECEIVER`
    * :kconfig:option:`CONFIG_BT_PAC_SNK`
    * :kconfig:option:`CONFIG_BT_PAC_SRC`

* PACS 已更改以支持动态运行时配置。
  这意味着 PACS 现在必须先通过 :c:func:`bt_pacs_register` 注册才能使用。
  此外，:c:func:`bt_pacs_register` 还必须在
  :c:func:`bt_ascs_register` 调用之前调用。
  所有 Kconfig 选项仍然保留，运行时配置无法覆盖已禁用的 Kconfig 选项。
  （:github:`83730`）

* 多个服务和客户端（AICS、ASCS、CSIP、HAS、MCS、PACS、TBS、VCP 和 VOCS）
  现在依赖于 :kconfig:option:`CONFIG_BT_SMP`，可能需要显式启用。
  （:github:`84994`）

蓝牙经典
=================

蓝牙主机
==============

* :kconfig:option:`CONFIG_BT_BUF_ACL_RX_COUNT` 已弃用。
  ACL RX 缓冲区数量现在内部计算，等于 :kconfig:option:`CONFIG_BT_MAX_CONN` + 1。
  如果应用需要更多缓冲区，可使用新的
  :kconfig:option:`CONFIG_BT_BUF_ACL_RX_COUNT_EXTRA` 添加。

  例如，如果 :kconfig:option:`CONFIG_BT_MAX_CONN` 为 ``3`` 且
  :kconfig:option:`CONFIG_BT_BUF_ACL_RX_COUNT` 为 ``7``，
  则 :kconfig:option:`CONFIG_BT_BUF_ACL_RX_COUNT_EXTRA` 应设为
  ``7 - (3 + 1) = 3``。

  .. warning::

    :kconfig:option:`CONFIG_BT_BUF_ACL_RX_COUNT` 的默认值已设为 0。

* LE 传统配对不再默认启用，因为它不安全。
  保持启用会使设备容易受到降级攻击。
  如果应用仍需使用 LE 传统配对，应手动禁用
  :kconfig:option:`CONFIG_BT_SMP_SC_PAIR_ONLY`。

* :kconfig:option:`CONFIG_BT_ECC` 的提示已移除，
  因为它只提供内部 API，意味着内部用户应在各自的 Kconfig 选项中显式选择它。

蓝牙加密
================

蓝牙服务
==================

* :kconfig:option:`CONFIG_BT_DIS_MODEL` 和 :kconfig:option:`CONFIG_BT_DIS_MANUF`
  已弃用。应用开发者现在应使用
  :kconfig:option:`CONFIG_BT_DIS_MODEL_NUMBER_STR` 和
  :kconfig:option:`CONFIG_BT_DIS_MANUF_NAME_STR` Kconfig 选项
  来设置设备信息服务（DIS）中型号名称字符串和制造商名称字符串特性的值。

网络
**********

* Prometheus 指标创建方式已更改，用户不再需要单独的
  :c:struct:`prometheus_metric` 结构体。
  这意味着 Prometheus 宏 :c:macro:`PROMETHEUS_COUNTER_DEFINE`、
  :c:macro:`PROMETHEUS_GAUGE_DEFINE`、
  :c:macro:`PROMETHEUS_HISTOGRAM_DEFINE` 和
  :c:macro:`PROMETHEUS_SUMMARY_DEFINE`
  的原型已更改。（:github:`81712`）

* 新添加的 IPv4 地址的默认子网掩码现在通过
  :kconfig:option:`CONFIG_NET_IPV4_DEFAULT_NETMASK` 选项指定，
  而不再留空。如需，应用仍可通过
  :c:func:`net_if_ipv4_set_netmask_by_addr` 函数为地址指定自定义掩码。

* HTTP 服务器公共 API 函数签名 :c:type:`http_resource_dynamic_cb_t` 已更改，
  数据现在通过 :c:struct:`http_request_ctx` 传递，
  该结构体保存数据、数据长度和请求头信息。
  应通过该参数访问请求头，而不是直接在 :c:struct:`http_client_ctx` 中访问，
  以正确处理不同 HTTP/2 流上的并发请求。

* HTTP 服务器公共 API 函数签名 :c:type:`http_resource_websocket_cb_t` 已更改，
  增加了 :c:struct:`http_request_ctx` 参数。
  应用可使用它访问 HTTP 升级请求的请求头，
  这对决定是否接受或拒绝 websocket 连接可能很有用。

* :c:macro:`HTTP_SERVICE_DEFINE` 和 :c:macro:`HTTPS_SERVICE_DEFINE` 宏
  增加了额外的 ``_res_fallback`` 参数，
  允许在其他资源都不匹配请求路径时提供回退资源。
  要保持现有行为，可将 ``NULL`` 作为额外参数传入。

* :kconfig:option:`CONFIG_NET_L2_OPENTHREAD` 符号不再蕴含
  :kconfig:option:`CONFIG_NVS` Kconfig 选项。
  使用 OpenThread 的平台必须显式启用
  :kconfig:option:`CONFIG_NVS` 或 :kconfig:option:`CONFIG_ZMS` Kconfig 选项。

* ``CONFIG_NET_TC_SKIP_FOR_HIGH_PRIO`` 已弃用，
  由 :kconfig:option:`CONFIG_NET_TC_TX_SKIP_FOR_HIGH_PRIO` 取代，
  以避免命名歧义。

其他子系统
****************

闪存映射
=========

文件系统
==========

* EXT2 Kconfig 符号 ``CONFIG_MAX_FILES`` 已重命名为
  :kconfig:option:`CONFIG_EXT2_MAX_FILES`。

hawkBit
=======

* Kconfig 符号 :kconfig:option:`CONFIG_SMF` 和
  :kconfig:option:`CONFIG_SMF_ANCESTOR_SUPPORT`
  现在必须启用才能使用 hawkBit 子系统。

MCUmgr
======

* Kconfig 选项 :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_MODE_SWAP_WITHOUT_SCRATCH`
  已弃用，由 :kconfig:option:`CONFIG_MCUBOOT_BOOTLOADER_MODE_SWAP_USING_MOVE` 取代。
  如果应用之前选择了旧选项，应更新为选择新选项。

* 弃用的宏 ``MGMT_CB_ERROR_RET`` 已移除。

调制解调器
=====

LoRa
====

* 函数 :c:func:`lora_recv_async` 和回调 ``lora_recv_cb``
  现在包含额外的 ``user_data`` 参数，它是一个 void 指针。
  该参数可用于引用任何用户定义的数据结构。
  要保持当前行为，将该参数设为 ``NULL``。

安全存储
=============

* 存储后端不再通过 ``select`` 或 ``imply`` 自动启用其依赖项。
  用户必须确保在应用中启用依赖项。
  :kconfig:option:`CONFIG_SECURE_STORAGE_ITS_STORE_IMPLEMENTATION_SETTINGS`
  之前启用了 NVS 和 settings，
  这意味着如果未启用 ZMS，NVS settings 后端将被默认使用。
  （:github:`86181`）

流式闪存
=============

* 函数 :c:func:`stream_flash_init` 在 ``size`` 参数设为 0 时
  不再自动检测设备大小，此时将返回错误。
  用户现在必须显式提供设备大小。
  问题 :github:`71042` 提供了更改的理由。

架构
*************

* native/POSIX

  * :kconfig:option:`CONFIG_NATIVE_APPLICATION` 已弃用。
    使用该选项的树外开发板应迁移到 native_simulator runner（:github:`81232`）。
    树内开发板迁移的示例参见 :github:`61481`。
  * 对于 native_sim 目标，:kconfig:option:`CONFIG_NATIVE_SIM_NATIVE_POSIX_COMPAT`
    默认已切换为 ``n``，且该选项已弃用。
    请确保代码不再使用 :kconfig:option:`CONFIG_BOARD_NATIVE_POSIX` 选项（:github:`81232`）。

* x86

  * Kconfig 选项 ``CONFIG_DISABLE_SSBD`` 和 ``CONFIG_ENABLE_EXTENDED_IBRS``
    自 v3.7 起已弃用，现已移除。
    请改用 :kconfig:option:`CONFIG_X86_DISABLE_SSBD` 和
    :kconfig:option:`CONFIG_X86_ENABLE_EXTENDED_IBRS`。
