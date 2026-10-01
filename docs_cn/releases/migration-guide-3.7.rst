:orphan:

.. _migration_3.7:

迁移到 Zephyr v3.7.0 的指南
################################

本文档描述了将应用程序从 Zephyr v3.6.0 迁移到 Zephyr v3.7.0 时所需的更改。

任何其他更改（与迁移应用程序不直接相关）可在 :ref:`发布说明 <zephyr_3.7>` 中找到。

.. contents::
   :local:
   :depth: 2

构建系统
************

* 完全重构了 SoC 和开发板的定义方式。
  这要求所有树外 SoC 和开发板
  移植到新的模型。
  参见 :ref:`hw_model_v2` 了解更多详细信息。
  （:github:`69607`）

* 以下构建时生成的头文件：

  .. list-table::
     :header-rows: 1

     * - 受影响的头文件
     * - ``app_version.h``
     * - ``autoconf.h``
     * - ``cmake_intdef.h``
     * - ``core-isa-dM.h``
     * - ``devicetree_generated.h``
     * - ``driver-validation.h``
     * - ``kobj-types-enum.h``
     * - ``linker-kobject-prebuilt-data.h``
     * - ``linker-kobject-prebuilt-priv-stacks.h``
     * - ``linker-kobject-prebuilt-rodata.h``
     * - ``mcuboot_version.h``
     * - ``offsets.h``
     * - ``otype-to-size.h``
     * - ``otype-to-str.h``
     * - ``strerror_table.h``
     * - ``strsignal_table.h``
     * - ``syscall_list.h``
     * - ``version.h``
     * - ``zsr.h``

  以及系统调用的头文件和源文件现在都被命名空间化到 ``zephyr/`` 文件夹。此更改大部分是自动化的，脚本可在 :github:`63973` 找到。暂时，兼容性 Kconfig（:kconfig:option:`CONFIG_LEGACY_GENERATED_INCLUDE_PATH`）默认启用，因此下游应用程序将继续编译，CMake 配置期间将生成一条警告消息。此 Kconfig 将被弃用并最终在未来移除，建议开发者尽快更新这些受影响头文件的 include 路径。

内核
******

* 所有架构现在都必须定义
  新的 ``struct arch_esf``，
  它描述栈帧的成员。
  此新结构体替换了
  命名的结构体 ``z_arch_esf_t``。
  （:github:`73593`）

* 命名的结构体 ``z_arch_esf_t`` 现在已弃用。改用 ``struct arch_esf``。（:github:`73593`）

* 头文件 :zephyr_file:`include/zephyr/arch/arch_interface.h`
  已从 ``include/zephyr/sys/``
  移到 ``include/zephyr/arch/``。
  树外源文件需要更新 include 路径。
  （:github:`64987`）

开发板
******

* 重排了 SparkFun Pro Micro RP2040
  的 ``pro_micro`` 连接器 gpio-map
  中的 D1 和 D0，
  以匹配原始 Pro Micro 定义。
  树外扩展板必须更新以反映此更改。
  （:github:`69994`）
* ITE：重命名所有 SoC 变体 Kconfig 选项，例如 ``CONFIG_SOC_IT82202_AX`` 重命名为 :kconfig:option:`CONFIG_SOC_IT82202AX`。所有符号重命名如下：``SOC_IT81202BX``、``SOC_IT81202CX``、``SOC_IT81302BX``、``SOC_IT81302CX``、``SOC_IT82002AW``、``SOC_IT82202AX``、``SOC_IT82302AX``。且将 ``SOC_SERIES_ITE_IT8XXX2`` 重命名为 ``SOC_SERIES_IT8XXX2``。（:github:`71680`）
* 对 native_sim/posix：:kconfig:option:`CONFIG_EMUL` 不再在设置 :kconfig:option:`CONFIG_I2C` 时默认启用。需要此设置启用的用户应在其项目配置文件中设置。（:github:`73067`）

* LiteX：将 LiteX VexRiscV 中断控制器节点的 ``compatible`` 从 ``vexriscv-intc0`` 重命名为 :dtcompatible:`litex,vexriscv-intc0`。（:github:`73211`）

* ``lairdconnect`` 开发板现在为 ``ezurio`` 开发板。Laird Connectivity 已重新品牌为 `Ezurio <https://www.ezurio.com/laird-connectivity>`_。

模块
*******

Mbed TLS
========

* TLS 1.2、RSA、AES、DES 和除 SHA-256 外的所有哈希算法（SHA-224、SHA-384、SHA-512、MD5 和 SHA-1）不再默认启用。其相应的 Kconfig 选项现在需要显式启用才能使用。（:github:`72078`）
* 此前名为 ``CONFIG_MBEDTLS_MAC_*_ENABLED`` 的 Kconfig 选项已重命名。``_MAC`` 和 ``_ENABLED`` 部分已从名称中移除。（:github:`73267`）
* :kconfig:option:`CONFIG_MBEDTLS_HASH_ALL_ENABLED` Kconfig 选项已修复以实际启用所有可用的哈希算法。此前，它仅启用 SHA-2 系列。（:github:`73267`）
* ``CONFIG_MBEDTLS_HASH_SHA*_ENABLED`` Kconfig 选项已移除。它们是其他 Kconfig 选项的重复项，这些选项现在名为 ``CONFIG_MBEDTLS_SHA*``。（:github:`73267`）
* ``CONFIG_MBEDTLS_MAC_ALL_ENABLED`` Kconfig 选项已移除。其等价物是 :kconfig:option:`CONFIG_MBEDTLS_HASH_ALL_ENABLED` 和 :kconfig:option:`CONFIG_MBEDTLS_CMAC` 的组合。（:github:`73267`）
* Kconfig 选项 ``CONFIG_MBEDTLS_MAC_MD4_ENABLED``、``CONFIG_MBEDTLS_CIPHER_ARC4_ENABLED`` 和 ``CONFIG_MBEDTLS_CIPHER_BLOWFISH_ENABLED`` 已移除，因为 Mbed TLS 不再支持它们。（:github:`73222`）
* 当系统中有任何 PSA 加密提供者可用时（即 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_CLIENT` 设置），期望的 PSA 加密功能必须使用适当的 ``CONFIG_PSA_WANT_*`` 显式启用。（:github:`72243`）
* 当系统中有任何 PSA 加密提供者可用时（即 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_CLIENT` 设置），TLS/X509/PK/MD 模块将使用 PSA 加密 API 而非旧版 API。（:github:`72243`）

Trusted Firmware-M
==================

* 默认 MCUboot 签名类型
  已从 RSA-3072 更改为 EC-P256。
  这影响在 TF-M 中启用 MCUboot
  （:kconfig:option:`CONFIG_TFM_BL2`）的构建。
  如果你希望继续使用 RSA-3072，
  需要将 :kconfig:option:`CONFIG_TFM_MCUBOOT_SIGNATURE_TYPE`
  设置为 ``"RSA-3072"``。
  否则，请确保拥有你所使用的签名类型的签名密钥。

LVGL
====

* :kconfig:option:`CONFIG_LV_Z_POINTER_KSCAN` 已移除，你需要将基于 kscan 的驱动程序转换为输入子系统，并在设备树中使用 :dtcompatible:`zephyr,lvgl-pointer-input` 替代。（:github:`73800`）

设备驱动程序和设备树
*****************************

* :dtcompatible:`nxp,kinetis-pit` pit 驱动程序
  已将其 compatible
  更改为 :dtcompatible:`nxp,pit`，
  并已更新以支持多个通道。
  要配置各个通道，
  你必须添加
  compatible 为 :dtcompatible:`nxp,pit-channel`
  的子节点并如下配置。
  :kconfig:option:`CONFIG_COUNTER_MCUX_PIT`
  也已重命名为
  :kconfig:option:`CONFIG_COUNTER_NXP_PIT`，
  关于 pit 绑定的重命名。
  （:github:`66336`）
  示例：

  .. code-block:: devicetree

    / {
        pit0: pit@40037000 {
            /* Other Pit DT Attributes */
            compatible = "nxp,pit";
            status = "disabled";
            num-channels = <1>;
            #address-cells = <1>;
            #size-cells = <0>;

            pit0_channel0: pit0_channel@0 {
                compatible = "nxp,pit-channel";
                reg = <0>;
                status = "disabled";
            };
    };

* :dtcompatible:`nxp,kinetis-ethernet`
  已弃用，改为 :dtcompatible:`nxp,enet`。
  所有树内 SoC 都已转换为使用此新模式。
  因此，所有使用 NXP ENET 外设的开发板
  需要在 DT 中对齐此绑定，
  这也伴随着一个不同版本的驱动程序。
  或者，以太网节点可以删除并重新定义为旧绑定以使用弃用的旧版驱动程序。
  新绑定的主要优势是能够通过 mdio API 抽象任意 phy。
  （:github:`70400`）
  基本开发板级别 ENET DT 定义示例：

  .. code-block:: devicetree

    &enet_mac {
        status = "okay";
        pinctrl-0 = <&pinmux_enet>;
        pinctrl-names = "default";
        phy-handle = <&phy>;
        zephyr,random-mac-address;
        phy-connection-type = "rmii";
    };

    &enet_mdio {
        status = "okay";
        pinctrl-0 = <&pinmux_enet_mdio>;
        pinctrl-names = "default";
        phy: phy@3 {
            compatible = "ethernet-phy";
            reg = <3>;
            status = "okay";
        };
    };

* :dtcompatible:`nxp,kinetis-lptmr` compatible 字符串已更改为 :dtcompatible:`nxp,lptmr`。旧字符串将可用一小段时间，但应替换，因为它将在未来被移除。

* 某些驱动程序 API 结构体已重命名以带所需的 ``_driver_api`` 后缀。（:github:`72182`）以下类型已重命名：

  * ``emul_sensor_backend_api`` 到 :c:struct:`emul_sensor_driver_api`
  * ``emul_bbram_backend_api`` 到 :c:struct:`emul_bbram_driver_api`
  * ``usbc_ppc_drv`` 到 :c:struct:`usbc_ppc_driver_api`

* :dtcompatible:`maxim,max31790` 的驱动程序已拆分为 MFD 和实际的 PWM 驱动程序。（:github:`68433`）此前，此设备的实例可以如此定义：

  .. code-block:: devicetree

    max31790_max31790: max31790@20 {
        compatible = "maxim,max31790";
        status = "okay";
        reg = <0x20>;
        pwm-controller;
        #pwm-cells = <2>;
    };

  这可转换为：

  .. code-block:: devicetree

    max31790_max31790: max31790@20 {
        compatible = "maxim,max31790";
        status = "okay";
        reg = <0x20>;

        max31790_max31790_pwm: max31790_max31790_pwm {
            compatible = "maxim,max31790-pwm";
            status = "okay";
            pwm-controller;
            #pwm-cells = <2>;
        };
    };

* :dtcompatible:`invensense,icm42688` 的驱动程序现在正确支持设备树配置（:github:`74267`）。先前的设备树可能尝试使用绑定为 accel/gyro 设置采样率和比例而无任何效果。设备树使用现在应使用提供的 defines 和 include 文件连同接受这些值的新绑定。例如：

  .. code-block:: devicetree

    #include <zephyr/dt-bindings/sensor/icm42688.h>

    icm42688: icm42688@0 {
        accel-pwr-mode = <ICM42688_ACCEL_LN>;
        accel-fs = <ICM42688_ACCEL_FS_16G>;
        accel-odr = <ICM42688_ACCEL_ODR_2000>;
        gyro-pwr-mode= <ICM42688_GYRO_LN>;
        gyro-fs = <ICM42688_GYRO_FS_2000>;
        gyro-odr = <ICM42688_GYRO_ODR_2000>;
    };

* :dtcompatible:`st,lis2mdl` 属性 ``spi-full-duplex`` 更改为 ``duplex = SPI_FULL_DUPLEX``。全双工现在是默认。

* :dtcompatible:`nxp,lpc-lpadc` 驱动程序的 DT 属性 ``nxp,reference-supply`` 已移除，用户应从设备树中移除此属性（如果存在）。添加了新的 phandle-array 类型 DT 属性 ``nxp,references``，用户可以使用此属性指定 lpadc 使用的参考电压和参考电压值。（:github:`75005`）

 * :dtcompatible:`microchip,ksz8081` phy 绑定的 DT 属性 ``mc,interface-type``、``mc,reset-gpio`` 和 ``mc,interrupt-gpio`` 已分别更改为 ``microchip,interface-type``、``reset-gpios`` 和 ``int-gpios``。（:github:`73725`）

充电器
=======

* ``charger_max20335`` 驱动程序丢弃了 ``constant-charge-current-max-microamp`` 属性，因为它未反映真实芯片功能。（:github:`69910`）

* 向 ``maxim,max20335-charger`` 绑定的 ``constant-charge-voltage-max-microvolt`` 属性添加了枚举键，以在构建时指示无效的设备树值。（:github:`69910`）

控制器局域网（CAN）
=============================

* 移除了以下已弃用的
  CAN 控制器设备树属性。
  使用这些属性的树外开发板
  可以切换到使用
  ``bitrate``、``sample-point``、
  ``bitrate-data`` 和 ``sample-point-data``
  设备树属性
  （或依赖 :kconfig:option:`CONFIG_CAN_DEFAULT_BITRATE`
  和 :kconfig:option:`CONFIG_CAN_DEFAULT_BITRATE_DATA`）
  来指定初始 CAN 比特率：

  * ``sjw``
  * ``prop-seg``
  * ``phase-seg1``
  * ``phase-seg2``
  * ``sjw-data``
  * ``prop-seg-data``
  * ``phase-seg1-data``
  * ``phase-seg2-data``

  ``bus-speed`` 和 ``bus-speed-data`` CAN 控制器设备树属性已弃用。（:github:`68714`）

* 手动总线关闭恢复支持已重构（:github:`69460`）：

  * 自动总线恢复将在驱动程序初始化时始终启用，无论 Kconfig 选项如何。由于 CAN 控制器初始化为“已停止”状态，此点不会启动不想要的总线关闭恢复。
  * Kconfig ``CONFIG_CAN_AUTO_BUS_OFF_RECOVERY`` 已重命名（并反转为 :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE`，默认禁用。此 Kconfig 选项启用对 :c:func:`can_recover()` API 函数和新的手动恢复模式的支持（见下一项）。
  * 添加了新的 CAN 控制器操作模式 :c:macro:`CAN_MODE_MANUAL_RECOVERY`。对此的支持仅在启用 :kconfig:option:`CONFIG_CAN_MANUAL_RECOVERY_MODE` 时启用。将此作为模式允许应用程序通过 :c:func:`can_get_capabilities` API 函数询问 CAN 控制器是否支持手动恢复模式。应用程序然后可以要么失败初始化，要么依赖自动总线关闭恢复。将此作为模式还允许不支持手动恢复模式的 CAN 控制器驱动程序在 :c:func:`can_set_mode` 中应用程序启动时早期失败，而不是在稍后调用 :c:func:`can_recover` 时失败。

加密
======

* NXP lpc55s36 上的 CSS 驱动程序已弃用。（:github:`71173`）

显示
=======

* 基于 GC9X01 的显示屏现在使用 MIPI DBI 驱动程序类。这些显示屏现在必须在 MIPI DBI 驱动程序包装设备内声明，该设备将管理与显示屏的接口。（:github:`73686`）示例参见下方：

  .. code-block:: devicetree

    /* Legacy GC9X01 display 定义 */
    &spi0 {
        gc9a01: gc9a01@0 {
            status = "okay";
            compatible = "galaxycore,gc9x01x";
            reg = <0>;
            spi-max-frequency = <100000000>;
            cmd-data-gpios = <&gpio0 8 GPIO_ACTIVE_HIGH>;
            reset-gpios = <&gpio0 14 GPIO_ACTIVE_LOW>;
            ...
        };
    };

    /* 带 MIPI DBI device 的新 display 定义 */

    #include <zephyr/dt-bindings/mipi_dbi/mipi_dbi.h>

    ...

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        dc-gpios = <&gpio0 8 GPIO_ACTIVE_HIGH>;
        reset-gpios = <&gpio0 14 GPIO_ACTIVE_LOW>;
        spi-dev = <&spi0>;
        #address-cells = <1>;
        #size-cells = <0>;

        gc9a01: gc9a01@0 {
            status = "okay";
            compatible = "galaxycore,gc9x01x";
            reg = <0>;
            mipi-max-frequency = <100000000>;
            ...
        };
    };

* 基于 ST7735R 的显示屏现在使用 MIPI DBI 驱动程序类。这些显示屏现在必须在 MIPI DBI 驱动程序包装设备内声明，该设备将管理与显示屏的接口。注意 ``cmd-data-gpios`` 引脚已随此更新更改极性，以更好地与新 ``dc-gpios`` 名称对齐。示例参见下方：

  .. code-block:: devicetree

    /* Legacy ST7735R display 定义 */
    &spi0 {
        st7735r: st7735r@0 {
            compatible = "sitronix,st7735r";
            reg = <0>;
            spi-max-frequency = <32000000>;
            reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
            cmd-data-gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;
            ...
        };
    };

    /* 带 MIPI DBI device 的新 display 定义 */

    #include <zephyr/dt-bindings/mipi_dbi/mipi_dbi.h>

    ...

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
        dc-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        spi-dev = <&spi0>;
        #address-cells = <1>;
        #size-cells = <0>;

        st7735r: st7735r@0 {
            compatible = "sitronix,st7735r";
            reg = <0>;
            mipi-max-frequency = <32000000>;
            mipi-mode = <MIPI_DBI_MODE_SPI_4WIRE>;
            ...
        };
    };

* 基于 UC81XX 的显示屏现在使用 MIPI DBI 驱动程序类。这些显示屏现在必须在 MIPI DBI 驱动程序包装设备内声明，该设备将管理与显示屏的接口。（:github:`73812`）注意 ``dc-gpios`` 引脚已随此更新更改极性。示例参见下方：

  .. code-block:: devicetree

    /* Legacy UC81XX display 定义 */
    &spi0 {
        uc8179: uc8179@0 {
            compatible = "ultrachip,uc8179";
            reg = <0>;
            spi-max-frequency = <4000000>;
            reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
            dc-gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;
            ...
        };
    };

    /* 带 MIPI DBI device 的新 display 定义 */

    #include <zephyr/dt-bindings/mipi_dbi/mipi_dbi.h>

    ...

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
        dc-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        spi-dev = <&spi0>;
        #address-cells = <1>;
        #size-cells = <0>;
        uc8179: uc8179@0 {
            compatible = "ultrachip,uc8179";
            reg = <0>;
            mipi-max-frequency = <4000000>;
            ...
        };
    };

* 基于 ST7789V 的显示屏现在使用 MIPI DBI 驱动程序类。这些显示屏现在必须在 MIPI DBI 驱动程序包装设备内声明，该设备将管理与显示屏的接口。（:github:`73750`）注意 ``cmd-data-gpios`` 引脚已随此更新更改极性，以更好地与新 ``dc-gpios`` 名称对齐。示例参见下方：

  .. code-block:: devicetree

    /* Legacy ST7789V display 定义 */
    &spi0 {
        st7789: st7789@0 {
            compatible = "sitronix,st7789v";
            reg = <0>;
            spi-max-frequency = <32000000>;
            reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
            cmd-data-gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;
            ...
        };
    };

    /* 带 MIPI DBI device 的新 display 定义 */

    #include <zephyr/dt-bindings/mipi_dbi/mipi_dbi.h>

    ...

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
        dc-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        spi-dev = <&spi0>;
        #address-cells = <1>;
        #size-cells = <0>;

        st7789: st7789@0 {
            compatible = "sitronix,st7789v";
            reg = <0>;
            mipi-max-frequency = <32000000>;
            mipi-mode = <MIPI_DBI_MODE_SPI_4WIRE>;
            ...
        };
    };

* 基于 SSD16XX 的显示屏现在使用 MIPI DBI 驱动程序类。（:github:`73946`）这些显示屏现在必须在 MIPI DBI 驱动程序包装设备内声明，该设备将管理与显示屏的接口。注意 ``dc-gpios`` 引脚已随此更新更改极性。示例参见下方：

  .. code-block:: devicetree

    /* Legacy SSD16XX display 定义 */
    &spi0 {
        ssd1680: ssd1680@0 {
            compatible = "solomon,ssd1680";
            reg = <0>;
            spi-max-frequency = <4000000>;
            reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
            dc-gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;
            ...
        };
    };

    /* 带 MIPI DBI device 的新 display 定义 */

    #include <zephyr/dt-bindings/mipi_dbi/mipi_dbi.h>

    ...

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
        dc-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        spi-dev = <&spi0>;
        #address-cells = <1>;
        #size-cells = <0>;

        ssd1680: ssd1680@0 {
            compatible = "solomon,ssd1680";
            reg = <0>;
            mipi-max-frequency = <4000000>;
            ...
        };
    };

* ``orientation-flipped`` 属性已从 SSD16XX 显示驱动程序移除，因为驱动程序现在支持显示旋转。用户应从设备树中移除此属性，并在运行时通过 :c:func:`display_set_orientation` 设置方向。（:github:`73360`）

增强串行外设接口（eSPI）
===========================================

* 宏 ``ESPI_SLAVE_TO_MASTER`` 和 ``ESPI_MASTER_TO_SLAVE`` 已分别重命名为 ``ESPI_TARGET_TO_CONTROLLER`` 和 ``ESPI_CONTROLLER_TO_TARGET``，以反映 eSPI 1.5 规范中的新术语。枚举值 ``ESPI_VWIRE_SIGNAL_SLV_BOOT_STS``、``ESPI_VWIRE_SIGNAL_SLV_BOOT_DONE`` 和所有 ``ESPI_VWIRE_SIGNAL_SLV_GPIO_<NUMBER>`` 信号已分别重命名为 ``ESPI_VWIRE_SIGNAL_TARGET_BOOT_STS``、``ESPI_VWIRE_SIGNAL_TARGET_BOOT_DONE`` 和 ``ESPI_VWIRE_SIGNAL_TARGET_GPIO_<NUMBER>``，以反映 eSPI 1.5 规范中的新术语。（:github:`68492`）Kconfig ``CONFIG_ESPI_SLAVE`` 已重命名为 :kconfig:option:`CONFIG_ESPI_TARGET`，类似地 ``CONFIG_ESPI_SAF`` 重命名为 :kconfig:option:`CONFIG_ESPI_TAF`。（:github:`73887`）

GNSS
====

* ``gnss-nmea-generic`` 驱动程序已添加基本电源管理支持。如果 ``CONFIG_PM_DEVICE=y``，驱动程序现在初始化为挂起模式，应用程序需要调用 :c:func:`pm_device_action_run` 带 :c:macro:`PM_DEVICE_ACTION_RESUME` 以启动驱动程序。（:github:`71774`）

输入
=====

* ``analog-axis`` 死区校准值已更改为相对于原始 ADC 值，类似 min 和 max。数据结构和属性已重命名以反映此（从 ``out-deadzone`` 到 ``in-deadzone``），且迁移到新定义时值应相应缩放。（:github:`70377`）

* ``holtek,ht16k33-keyscan`` 驱动程序已转换为使用 :ref:`input` 子系统，回调必须迁移为使用输入 API，:dtcompatible:`zephyr,kscan-input` 可用于向后兼容。（:github:`69875`）

中断控制器
==================

* 多级中断控制器查找表的静态自动生成已弃用，且仅在新兼容性 Kconfig :kconfig:option:`CONFIG_LEGACY_MULTI_LEVEL_TABLE_GENERATION` 启用时编译，其将在未来版本中最终移除。

  多级中断控制器驱动程序应更新为使用新创建的 ``IRQ_PARENT_ENTRY_DEFINE`` 宏向新的多级中断架构注册自身。为使宏更易用，``INTC_INST_ISR_TBL_OFFSET`` 宏用于推导给定驱动程序实例的软件 ISR 表偏移，对伪中断控制器子节点，改用 ``INTC_CHILD_ISR_TBL_OFFSET`` 宏。新增了设备树宏（``DT_INTC_GET_AGGREGATOR_LEVEL`` & ``DT_INST_INTC_GET_AGGREGATOR_LEVEL``）用于中断控制器驱动程序实例将其聚合器级别传递到 ``IRQ_PARENT_ENTRY_DEFINE`` 宏。

LED 灯带
=========

* :dtcompatible:`worldsemi,ws2812-gpio` 中定义的属性 ``in-gpios`` 已重命名为 ``gpios``。（:github:`68514`）

* ``chain-length`` 和 ``color-mapping`` 属性已添加到所有 LED 灯带绑定，且现在为必需。

* 添加了新的必需 ``length`` 函数，返回 LED 灯带设备的长度（像素数）。

* ``update_channels`` 函数变为可选，且移除了未实现的函数。

* ``CONFIG_WS2812_STRIP_DRIVER`` kconfig 选项已移除。此前，使用 :kconfig:option:`CONFIG_WS2812_STRIP_SPI`、:kconfig:option:`CONFIG_WS2812_STRIP_I2S`、:kconfig:option:`CONFIG_WS2812_STRIP_GPIO` 或 :kconfig:option:`CONFIG_WS2812_STRIP_RPI_PICO_PIO` 时，必须用 ``CONFIG_WS2812_STRIP_DRIVER`` 选择其中之一，但不再需要。请直接设置每个选项。

MDIO
====

* :kconfig:option:`CONFIG_MDIO_NXP_ENET_TIMEOUT` 现在以微秒而非毫秒为单位。（:github:`75625`）

传感器
=======

* :dtcompatible:`sensirion,shtcx` 传感器驱动程序的 ``chip`` 设备树属性已移除。芯片变体现在使用匹配的 compatible 属性选择。（:github:`74033`）新 shtc3 配置示例参见下方：

  .. code-block:: devicetree

    &i2c0 {
        status = "okay";

        shtc3: shtc3@70 {
            compatible = "sensirion,shtc3", "sensirion,shtcx";
            reg = <0x70>;
            measure-mode = "normal";
            clock-stretching;
        };
    };

串口
======

* Raspberry Pi UART 驱动程序 ``uart_rpi_pico`` 已移除。改用 ``uart_pl011``（:dtcompatible:`arm,pl011`）。（:github:`71074`）

稳压器
=========

* :dtcompatible:`nxp,vref` 驱动程序不再支持地选择功能，因为此设置不应由用户修改。DT 属性 ``nxp,ground-select`` 已移除，用户应从设备树中移除此属性（如果存在）。（:github:`70642`）

W1
==

* :dtcompatible:`zephyr,w1-gpio` 1-Wire 主驱动程序不再默认启用 GPIO 引脚的内部上拉电阻。配置现在取自设备树中指定的引脚配置标志。（:github:`71789`）

看门狗
========

* ``nuvoton,npcx-watchdog`` 驱动程序已更改以延长最大超时周期。一个看门狗计数的时间随不同的预分频器设置变化。移除了 :kconfig:option:`CONFIG_WDT_NPCX_DELAY_CYCLES`，因为它不再适合设置领先警告时间。相反，添加了 :kconfig:option:`CONFIG_WDT_NPCX_WARNING_LEADING_TIME_MS` 以毫秒设置领先警告时间。

蓝牙
*********

蓝牙 HCI
=============

 * 引入了新的 HCI 驱动程序 API（:github:`72323`），且旧的一个已弃用。新 API 遵循正常的 Zephyr 驱动程序模型，带设备树节点等。Host 现在通过查找 ``zephyr,bt-hci`` chosen 属性选择用作控制器的驱动程序实例。所有 HCI 驱动程序的设备树绑定从通用的 ``bt-hci.yaml`` 基础绑定派生。

  * 作为新 HCI 驱动程序 API 的一部分，``zephyr,bt-uart`` chosen 属性不再使用，而 UART HCI 驱动程序通过查找 HCI 驱动程序实例节点的父设备树节点选择其 UART。
  * 作为新 HCI 驱动程序 API 的一部分，``zephyr,bt-hci-ipc`` chosen 属性仅用于控制器侧，而 HCI 驱动程序现在依赖 compatible 字符串为 ``zephyr,bt-hci-ipc`` 的节点。
  * ``BT_NO_DRIVER`` Kconfig 选项已移除。HCI 驱动程序不再在 Kconfig choice 之后，而现可独立启用和禁用，主要基于其相应设备树节点是否启用。
  * ``BT_HCI_VS_EXT`` Kconfig 选项已删除，且功能现在包含在 :kconfig:option:`CONFIG_BT_HCI_VS` Kconfig 选项中。
  * ``BT_HCI_VS_EVT`` Kconfig 选项已移除，因为如果启用 :kconfig:option:`CONFIG_BT_HCI_VS` 选项，厂商事件支持是隐式的。
  * bt_read_static_addr() API 已移除。这并非完全公共 API，但由于由公共 hci_driver.h 头文件暴露，因此移除在此提及。改为启用 :kconfig:option:`CONFIG_BT_HCI_VS` Kconfig 选项，并使用厂商特定 HCI 命令 API 在可用时获取控制器的蓝牙静态地址。

蓝牙 Mesh
=============

* :c:struct:`bt_mesh_model` 的 model 元数据指针声明已更改为添加 ``const`` 限定符。:c:struct:`bt_mesh_models_metadata_entry` 的数据指针也获得 ``const`` 限定符。Model 的元数据结构体和元数据原始值可声明为非易失性存储器中的永久常量。（:github:`69679`）

* :c:struct:`bt_mesh_model` 的 model 元数据指针声明已更改为单个 ``const *``，且从 :c:struct:`bt_mesh_health_srv` 移除冗余元数据指针。因此，:code:`BT_MESH_MODEL_HEALTH_SRV` 定义更改为使用可变参数表示法。现在，当你的实现支持 :kconfig:option:`CONFIG_BT_MESH_LARGE_COMP_DATA_SRV` 且需为 Health Server model 指定元数据时，简单将元数据作为 :code:`BT_MESH_MODEL_HEALTH_SRV` 宏的最后一个参数传递，否则省略最后一个参数。（:github:`71281`）

蓝牙音频
================

* 启用 :kconfig:option:`CONFIG_BT_BAP_UNICAST_SERVER` 时 :kconfig:option:`CONFIG_BT_ASCS`、:kconfig:option:`CONFIG_BT_PERIPHERAL` 和 :kconfig:option:`CONFIG_BT_ISO_PERIPHERAL` 不再自动启用，且这些现在必须在项目配置文件中显式设置。（:github:`71993`）

* CAP 的 discover 回调函数 :code:`bt_cap_initiator_cb.unicast_discovery_complete` 和 :code:`bt_cap_commander_cb.discovery_complete` 现在包含 set 成员的额外参数。这需添加到所有定义的 CAP discover 回调函数实例。（:github:`72797`）

* :c:func:`bt_bap_stream_start` 不再连接 CIS。要连接 CIS，现在需在 :c:func:`bt_bap_stream_start` 前调用 :c:func:`bt_bap_stream_connect`。（:github:`73032`）

* 将 ``stream_lang`` 重命名为仅 ``lang``，以更好符合已分配号码文档。这影响 ``BT_AUDIO_METADATA_TYPE_LANG`` 宏和以下函数：

  * :c:func:`bt_audio_codec_cap_meta_set_lang`
  * :c:func:`bt_audio_codec_cap_meta_get_lang`
  * :c:func:`bt_audio_codec_cfg_meta_set_lang`
  * :c:func:`bt_audio_codec_cfg_meta_get_lang`

  （:github:`72584`）

* 将 ``lang`` 从 ``uint32_t`` 更改为 ``uint8_t [3]``。这修改以下函数：

  * :c:func:`bt_audio_codec_cap_meta_set_lang`
  * :c:func:`bt_audio_codec_cap_meta_get_lang`
  * :c:func:`bt_audio_codec_cfg_meta_set_lang`
  * :c:func:`bt_audio_codec_cfg_meta_get_lang`

  此结果是 ``"eng"`` 和 ``"deu"`` 等字符串值现在可用于设置新值，且防止获取值时不必要的数据复制。（:github:`72584`）

* 所有 ``set_sirk`` 出现已更改为仅 ``sirk``，因为 ``sirk`` 中的 ``s`` 代表 set。（:github:`73413`）

* 向 :c:func:`bt_audio_codec_cfg_get_chan_allocation` 添加 ``fallback_to_default`` 参数。要保持现有行为将参数设置为 ``false``。（:github:`72090`）

* 向 :c:func:`bt_audio_codec_cap_get_supported_audio_chan_counts` 添加 ``fallback_to_default`` 参数。要保持现有行为将参数设置为 ``false``。（:github:`72090`）

* 向 :c:func:`bt_audio_codec_cap_get_max_codec_frames_per_sdu` 添加 ``fallback_to_default`` 参数。要保持现有行为将参数设置为 ``false``。（:github:`72090`）

* 向 :c:func:`bt_audio_codec_cfg_meta_get_pref_context` 添加 ``fallback_to_default`` 参数。要保持现有行为将参数设置为 ``false``。（:github:`72090`）

蓝牙经典
=================

* Host BR/EDR 的源文件已移到 ``subsys/bluetooth/host/classic``。Host BR/EDR 的头文件已移到 ``include/zephyr/bluetooth/classic``。移除了 :kconfig:option:`CONFIG_BT_BREDR`。其已被新选项 :kconfig:option:`CONFIG_BT_CLASSIC` 替换。（:github:`69651`）

蓝牙 Host
=============

* 广告选项 :code:`BT_LE_ADV_OPT_USE_NAME` 和 :code:`BT_LE_ADV_OPT_FORCE_NAME_IN_AD` 在本版本中已弃用。应用程序需显式包含设备名称。一种方式是向传递给 host 的广告数据或扫描响应数据添加以下：

  .. code-block:: c

    BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME, sizeof(CONFIG_BT_DEVICE_NAME) - 1)

  （:github:`71686`）

* :c:type:`bt_l2cap_le_endpoint` 的字段 :code:`init_credits` 已移除，因为 Zephyr 3.4.0 及以后不再使用。对此字段的任何引用应移除。无需进一步操作。

* :c:macro:`BT_LE_ADV_PARAM` 现在返回 :code:`const` 指针。将结果存储在局部变量中的任何地方如 :code:`struct bt_le_adv_param *param = BT_LE_ADV_CONN;` 需更新为 :code:`const struct bt_le_adv_param *param = BT_LE_ADV_CONN;` 或用于初始化如 :code:`struct bt_le_adv_param param = *BT_LE_ADV_CONN;`

  :c:macro:`BT_LE_ADV_PARAM` 的更改还影响其所有派生项，包括但不限于：

  * :c:macro:`BT_LE_ADV_CONN`
  * :c:macro:`BT_LE_ADV_NCONN`
  * :c:macro:`BT_LE_EXT_ADV_SCAN`
  * :c:macro:`BT_LE_EXT_ADV_CODED_NCONN_NAME`

  （:github:`75065`）

* :kconfig:option:`CONFIG_BT_BUF_ACL_RX_COUNT` 现在需大于 :kconfig:option:`CONFIG_BT_MAX_CONN`。由于 HCI 接口的设计这一直如此。现在通过构建时断言强制执行。（:github:`75592`）

蓝牙加密
================

* 添加了 :kconfig:option:`CONFIG_BT_USE_PSA_API` 以显式请求用 PSA API 而非 TinyCrypt 进行加密操作。当然，这仅在系统中 PSA 加密提供者可用时（即 :kconfig:option:`CONFIG_PSA_CRYPTO_CLIENT` 设置）可能。（:github:`73378`）

网络
**********

* 弃用了 :kconfig:option:`CONFIG_NET_SOCKETS_POSIX_NAMES` 选项。这是一个旧版选项，曾用于允许用户在不启用 POSIX API 时调用 BSD socket API。这在构建希望启用 :kconfig:option:`CONFIG_POSIX_API` 选项的应用程序时可能导致复杂情况。这意味着如果应用程序想用正常 BSD socket 接口，则需启用 :kconfig:option:`CONFIG_POSIX_API`。如果应用程序不想或无法启用该选项，则 socket API 调用需前缀 ``zsock_`` 字符串。所有使用 BSD socket 接口的示例应用程序已更改为启用 :kconfig:option:`CONFIG_POSIX_API`。内部网络栈不启用 POSIX API 选项，这意味着使用 socket 的各种网络库已转换为使用 ``zsock_*`` API 调用。（:github:`69950`）

* Zperf zperf_results 结构体已更改以支持 64 位传输字节（total_len）和测试持续时间（time_in_us 和 client_time_in_us），而非 32 位。这将使长持续时间 zperf 测试显示正确的吞吐量结果。（:github:`69500`）

* 分配给网络接口的每个 IPv4 地址有与之关联的 IPv4 子网掩码，而非为整个接口设置。如果网络接口仅指定一个 IPv4 地址，从用户角度看无变化。但如果有多个 IPv4 地址 / 网络接口，则必须分别为每个 IPv4 地址指定子网掩码。（:github:`68419`）

* 虚拟网络接口 API 不再有 ``input`` 回调。Input 回调曾用于读取 IP 隧道中的内部 IPv4/IPv6 数据包。此传入隧道读取现在在 ``recv`` 回调中实现。（:github:`70549`）

* 虚拟局域网（VLAN）实现已更改为使用虚拟网络接口。无 API 更改，但 VLAN 网络接口的类型已从 ``ETHERNET`` 更改为 ``VIRTUAL``。这可能要求更改向网络接口设置 VLAN 标签的代码。例如在 :c:func:`net_eth_is_vlan_enabled()` API 中，第 2 个接口参数必须指向主以太网接口，而非 VLAN 接口。（:github:`70345`）

* 修改了 ``wifi connect`` 命令以用键值格式用于参数。在先前的实现中，我们用其在参数字符串中的位置识别选项。这使得处理可选参数或扩展对其他选项的支持困难。有此键值格式更容易扩展可传递给 connect 命令的选项。``wifi -h`` 将给出关于 connect 命令使用的更多信息。（:github:`70024`）

* Kconfig :kconfig:option:`CONFIG_NET_TCP_ACK_TIMEOUT` 已弃用。其使用仅限于 TCP 握手，且在此情况下总超时应取决于总重传超时（如其他情况），使配置冗余且令人困惑。改用 :kconfig:option:`CONFIG_NET_TCP_INIT_RETRANSMISSION_TIMEOUT` 和 :kconfig:option:`CONFIG_NET_TCP_RETRY_COUNT` 以在 TCP 级别控制总超时。（:github:`70731`）

* 在 LwM2M API 中，回调类型 :c:type:`lwm2m_engine_set_data_cb_t` 现在有额外参数 ``offset``。此参数用于指示 Coap 分块传输期间数据的偏移。任何 post write、validate 或某些固件回调应更新以包含此参数。（:github:`72590`）

* DNS 解析器和 mDNS/LLMNR 响应器已转换为使用 socket 服务 API。这意味着系统中可轮询的 socket 数量可能需要增加。请检查 ``CONFIG_NET_SOCKETS_POLL_MAX`` 和 :kconfig:option:`CONFIG_POSIX_MAX_FDS` 的值是否足够大。不幸的是无法给出这些的确切值，因为取决于应用程序需求和用法。（:github:`72834`）

* 数据包 socket（类型 ``AF_PACKET``）的 ``socket`` API 调用中的协议字段已更改。协议字段应在网络字节序中，以兼容 Linux socket 调用。Linux 期望如果要接收所有网络数据包，则协议字段为 ``htons(ETH_P_ALL)``。详见 https://www.man7.org/linux/man-pages/man7/packet.7.html 文档。（:github:`73338`）

* TCP 现在用 SHA-256 而非 MD5 用于 ISN 生成。此哈希计算的加密支持也从 Mbed TLS 更改为 PSA API。这通过使 :kconfig:option:`CONFIG_NET_TCP_ISN_RFC6528` 依赖 :kconfig:option:`PSA_WANT_ALG_SHA_256` 而非旧版 ``CONFIG_MBEDTLS_*`` 特性实现。（:github:`71827`）

其他子系统
****************

闪存映射
=========

* 闪存检查函数（:kconfig:option:`CONFIG_FLASH_AREA_CHECK_INTEGRITY_BACKEND`）的加密后端此前通过 TinyCrypt 或 Mbed TLS 提供，现在通过 PSA 或 Mbed TLS 提供。更新的 Mbed TLS 实现比先前的 TinyCrypt 实现占用空间略小，且 PSA 实现为用 TF-M 构建的设备提供更大的占用空间减少。PSA 是受支持的向前方式，但截至目前，如果你无法承受启用 PSA API（:kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_C` 对无 TF-M 的设备）的一次性成本，你仍可用 Mbed TLS。:github:`73511`

hawkBit
=======

* :kconfig:option:`CONFIG_HAWKBIT_PORT` 现在是 int 而非 string。需启用 :kconfig:option:`CONFIG_SETTINGS` 才能使用 hawkBit，因为其现在用设置子系统存储 hawkBit 配置。（:github:`68806`）

MCUmgr
======

* SHA-256 支持（当使用校验和/哈希函数时）此前通过 TinyCrypt 或 Mbed TLS 提供，现在通过 PSA 或 Mbed TLS 提供。PSA 是向前推荐的 API，但如果尚未启用（:kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_CLIENT`）且你有紧凑的代码尺寸约束，你可能通过改用 Mbed TLS 节省 1.3 KB。

调制解调器
=====

* ``CONFIG_MODEM_CHAT_LOG_BUFFER`` Kconfig 选项已重命名为 :kconfig:option:`CONFIG_MODEM_CHAT_LOG_BUFFER_SIZE`。（:github:`70405`）

.. _zephyr_3.7_posix_api_migration:

POSIX API
=========

* :ref:`POSIX API Kconfig 弃用项 <zephyr_3.7_posix_api_deprecations>` 可能要求更改 Kconfig 文件（``prj.conf`` 等），如发布说明中所述。可通过提供的迁移脚本获得更自动化的方法。简单运行以下：

  .. code-block:: bash

    $ python ${ZEPHYR_BASE}/scripts/utils/migrate_posix_kconfigs.py -r root_path

状态机框架
=======================

* :c:macro:`SMF_CREATE_STATE` 宏现在始终接受 5 个参数。参数数量现在独立于 :kconfig:option:`CONFIG_SMF_ANCESTOR_SUPPORT` 和 :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION` 的值。如果额外参数未使用，必须设置为 ``NULL``。（:github:`71250`）
* 当转换源是 :c:func:`smf_run_state` 调用的状态的父状态时，SMF 现在遵循更 UML 风格的转换流程。直到（但不包括）转换源和目标状态的最近公共祖先的退出动作将执行，且从（但不包括）最近公共祖先到目标状态的进入动作也将执行。（:github:`71675`）
* 此前，用 ``new_state`` 设置为 NULL 调用 :c:func:`smf_set_state` 将执行从当前状态到最顶层父状态的所有退出动作，期望最顶层退出动作终止状态机。传递 ``NULL`` 现在不允许。相反，在顶层创建 'terminate' 状态，并从其进入动作调用 :c:func:`smf_set_terminate`。

UpdateHub
=========

* 用于执行完整性检查的 SHA-256 实现不再用 :kconfig:option:`CONFIG_FLASH_AREA_CHECK_INTEGRITY_BACKEND` 选择。相反，使用的实现（现在为 Mbed TLS 或 PSA）基于 :kconfig:option:`CONFIG_PSA_CRYPTO_CLIENT` 选择。它仍默认使用 Mbed TLS（比先前占用空间更小），除非开发板用 TF-M 构建或启用 :kconfig:option:`CONFIG_MBEDTLS_PSA_CRYPTO_C`。（:github:`73511`）

架构
*************

* 函数 :c:func:`arch_start_cpu` 已重命名为 :c:func:`arch_cpu_start`。（:github:`64987`）

* ``CONFIG_ARM64_ENABLE_FRAME_POINTER`` 已弃用。改用 :kconfig:option:`CONFIG_FRAME_POINTER`。（:github:`72646`）

* x86

  * Kconfig ``CONFIG_DISABLE_SSBD`` 和 ``CONFIG_ENABLE_EXTENDED_IBRS`` 已弃用。改用 :kconfig:option:`CONFIG_X86_DISABLE_SSBD` 和 :kconfig:option:`CONFIG_X86_ENABLE_EXTENDED_IBRS`。（:github:`69690`）

* POSIX 架构：

  * LLVM fuzzing 支持已重构。测试应用程序现在需提供其自身的 ``LLVMFuzzerTestOneInput()`` 钩子，而非依赖开发板提供的。检查 ``samples/subsys/debug/fuzz/`` 以获取示例。（:github:`71378`）
