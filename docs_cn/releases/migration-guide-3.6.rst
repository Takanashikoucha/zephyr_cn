:orphan:

.. _migration_3.6:

迁移到 Zephyr v3.6.0 的指南
################################

本文档描述了将应用程序从 Zephyr v3.5.0 迁移到 Zephyr v3.6.0 时所需的更改。

任何其他更改（与迁移应用程序不直接相关）可在 :ref:`发布说明 <zephyr_3.6>` 中找到。

.. contents::
   :local:
   :depth: 2

构建系统
************

* 已弃用的 ``prj_<board>.conf`` Kconfig 文件支持已移除，
  使用此文件的项目应改为使用
  开发板 Kconfig 片段（``boards/<board>.conf``）。

* 迄今为止，在为原生（``ARCH_POSIX``）目标构建时 ``_POSIX_C_SOURCE``、``_XOPEN_SOURCE`` 和 ``_XOPEN_SOURCE_EXTENDED`` 被全局定义，在使用 PicolibC 构建时 ``_POSIX_C_SOURCE`` 也被定义。从本版本起，这些宏仅对需要它们的文件设置。如果你的库或应用程序需要这些宏，你可能会开始对原型仅在其中一个宏被定义时才暴露的函数收到“隐式声明”警告。如果是这种情况，你可以在 C 源文件中任何 include 之前定义对应的宏来修复，或者向你的应用程序添加 ``target_compile_definitions(app PRIVATE _POSIX_C_SOURCE=200809L)`` 的等价物，或向你的库添加 ``zephyr_library_compile_definitions(_POSIX_C_SOURCE=200809L)``。

* 通过设置 ``CONF_FILE`` 为 ``prj_<build>.conf``
  来指定构建类型现已弃用，
  用户应改为使用新的 ``-DFILE_SUFFIX`` 特性
  :ref:`application-file-suffixes`。

内核
******

* 系统堆大小及其可用性现在由 ``K_HEAP_MEM_POOL_SIZE`` 定义而非 :kconfig:option:`CONFIG_HEAP_MEM_POOL_SIZE` Kconfig 选项确定。子系统可以通过指定前缀为 ``CONFIG_HEAP_MEM_POOL_ADD_SIZE_`` 的 Kconfig 选项来指定其自身的自定义系统堆大小需求。旧的 Kconfig 选项仍然存在，但如果自定义需求更大则会被覆盖。要强制使用旧的 Kconfig 选项，即使其值小于所指示的自定义需求，已引入新的 :kconfig:option:`CONFIG_HEAP_MEM_POOL_IGNORE_MIN` 选项（默认禁用）。

* STM32H7 和 STM32F7
  现在应通过显式将 ``CONFIG_CACHE_MANAGEMENT``
  设置为 ``y``
  来激活缓存（Icache 和 Dcache）。

开发板
******

* 已弃用的 Nordic SoC Kconfig 选项
  ``NRF_STORE_REBOOT_TYPE_GPREGRET`` 已移除，
  使用此选项的应用程序应改为
  使用 :ref:`boot_mode_api`。
* NXP：在以下 NXP 开发板上
  启用 :ref:`linkserver<linkserver-debug-host-tools>`
  作为默认运行器：
  ``mimxrt685_evk_cm33``、``frdm_k64f``、``mimxrt1050_evk``、
  ``frdm_kl25z``、``mimxrt1020_evk``、``mimxrt1015_evk``

模块
*******

可选模块
================

以下模块已变为可选，默认不再通过 `west update` 下载：

* ``canopennode``（:github:`64139`）

要重新启用它们，使用 ``west config manifest.project-filter -- +<module name>`` 命令，或 ``west config manifest.group-filter -- +optional`` 启用所有可选模块，然后再次运行 ``west update``。

MCUboot
=======

* MCUboot 已弃用的
  ``CONFIG_ZEPHYR_TRY_MASS_ERASE`` Kconfig 选项已移除。
  如果在烧录 MCUboot 时需要擦除，
  这现在应直接提供给 ``west`` 命令，
  例如 ``west flash --erase``。
  （:github:`64703`）

zcbor
=====

* 如果你有通过 Zephyr 依赖 zcbor 库的 zcbor 生成的代码，你必须使用 zcbor 0.8.1 重新生成文件。注意生成的类型和成员的名称已全面修订，因此使用生成代码的代码很可能需要更改。例如：

  * 前导单下划线和所有双下划线大部分消失，
  * 名称有时获得 ``_m`` 或 ``_l`` 等后缀以消除歧义。
  * 所有枚举（choice）名称现在获得 ``_c`` 后缀，因此枚举名称不再与对应的成员名称完全匹配（因为这违反了 C++ 命名空间规则）。

* 函数 :c:func:`zcbor_new_state`、:c:func:`zcbor_new_decode_state` 和宏 :c:macro:`ZCBOR_STATE_D` 已获得与无序映射解码相关的新参数。除非你正在使用那个新功能，这些都可以设置为 NULL 或 0。

* 函数 :c:func:`zcbor_bstr_put_term` 和 :c:func:`zcbor_tstr_put_term` 已获得新参数 ``maxlen``，指参数 ``str`` 的最大长度。此参数直接传递到底层 :c:func:`strnlen`。

* 函数 :c:func:`zcbor_tag_encode`
  已重命名为 :c:func:`zcbor_tag_put`。

* 打印已显著更改，例如 :c:func:`zcbor_print` 现在称为 :c:func:`zcbor_log`，无参数的 :c:func:`zcbor_trace` 已消失，取而代之的是 :c:func:`zcbor_trace_file` 和 :c:func:`zcbor_trace`，两者都接受 ``state`` 参数。

设备驱动程序和设备树
*****************************

设备树标签
=================

* 与已弃用的设备树标签属性相关的各种已弃用宏已移除。这些列在以下表格中。表格还提供了替代方案。

  然而，如果你仍在使用 ``device_get_binding(DT_LABEL(node_id))`` 之类的代码，考虑改为使用 ``DEVICE_DT_GET(node_id)`` 之类的代码。``DEVICE_DT_GET()`` 宏避免了运行时字符串比较，也更安全，因为如果设备不存在它将导致构建失败。

  .. list-table::
     :header-rows: 1

     * - 已移除的宏
       - 替代方案

     * - ``DT_GPIO_LABEL(node_id, gpio_pha)``
       - ``DT_PROP(DT_GPIO_CTLR(node_id, gpio_pha), label)``

     * - ``DT_GPIO_LABEL_BY_IDX(node_id, gpio_pha, idx)``
       - ``DT_PROP(DT_GPIO_CTLR_BY_IDX(node_id, gpio_pha, idx), label)``

     * - ``DT_INST_GPIO_LABEL(inst, gpio_pha)``
       - ``DT_PROP(DT_GPIO_CTLR(DT_DRV_INST(inst), gpio_pha), label)``

     * - ``DT_INST_GPIO_LABEL_BY_IDX(inst, gpio_pha, idx)``
       - ``DT_PROP(DT_GPIO_CTLR_BY_IDX(DT_DRV_INST(inst), gpio_pha, idx), label)``

     * - ``DT_SPI_DEV_CS_GPIOS_LABEL(spi_dev)``
       - ``DT_PROP(DT_SPI_DEV_CS_GPIOS_CTLR(spi_dev), label)``

     * - ``DT_INST_SPI_DEV_CS_GPIOS_LABEL(inst)``
       - ``DT_PROP(DT_SPI_DEV_CS_GPIOS_CTLR(DT_DRV_INST(inst)), label)``

     * - ``DT_LABEL(node_id)``
       - ``DT_PROP(node_id, label)``

     * - ``DT_BUS_LABEL(node_id)``
       - ``DT_PROP(DT_BUS(node_id), label)``

     * - ``DT_INST_LABEL(inst)``
       - ``DT_INST_PROP(inst, label)``

     * - ``DT_INST_BUS_LABEL(inst)``
       - ``DT_PROP(DT_BUS(DT_DRV_INST(inst)), label)``

多级中断
====================

* 对于启用了 :kconfig:option:`CONFIG_MULTI_LEVEL_INTERRUPTS` 的平台，设备树宏的 ``IRQ`` 变体现在返回设备树中看到的值而非 Zephyr 多级编码的 IRQ 编号。要获取 Zephyr 多级编码格式的 IRQ 编号，改用 ``IRQN`` 变体。例如，考虑以下设备树：

  .. code-block:: devicetree

    plic: interrupt-controller@c000000 {
            riscv,max-priority = <7>;
            riscv,ndev = <1024>;
            reg = <0x0c000000 0x04000000>;
            interrupts-extended = <&hlic0 11>;
            interrupt-controller;
            compatible = "sifive,plic-1.0.0";
            #address-cells = <0x0>;
            #interrupt-cells = <0x2>;
    };

    uart0: uart@10000000 {
            interrupts = <10 1>;
            interrupt-parent = <&plic>;
            clock-frequency = <0x384000>;
            reg = <0x10000000 0x100>;
            compatible = "ns16550";
            reg-shift = <0>;
    };

  ``plic`` 是二级中断聚合器，``uart0`` 是 ``plic`` 的子节点。``DT_IRQ_BY_IDX(DT_NODELABEL(uart0), 0, irq)`` 将返回 ``10``（设备树中看到的值），而 ``DT_IRQN_BY_IDX(DT_NODELABEL(uart0), 0)`` 将返回 ``(((10 + 1) << CONFIG_1ST_LEVEL_INTERRUPT_BITS) | 11)``。

  应在多级中断配置中工作的驱动程序和应用程序应更新为使用 ``IRQN`` 变体，即：

  * ``DT_IRQ(node_id, irq)`` -> ``DT_IRQN(node_id)``
  * ``DT_IRQ_BY_IDX(node_id, idx, irq)`` -> ``DT_IRQN_BY_IDX(node_id, idx)``
  * ``DT_IRQ_BY_NAME(node_id, name, irq)`` -> ``DT_IRQN_BY_NAME(node_id, name)``
  * ``DT_INST_IRQ(inst, irq)`` -> ``DT_INST_IRQN(inst)``
  * ``DT_INST_IRQ_BY_IDX(inst, idx, irq)`` -> ``DT_INST_IRQN_BY_IDX(inst, idx)``
  * ``DT_INST_IRQ_BY_NAME(inst, name, irq)`` -> ``DT_INST_IRQN_BY_NAME(inst, name)``

模数转换器（ADC）
=================================

* 以下设备树绑定的 io-channel 单元已从 2（``positive`` 和 ``negative``）减少到通用的 ``input``，使其能够与 TI LMP90xxx ADC 设备一起使用各种 ADC DT 宏：

  * :dtcompatible:`ti,lmp90077`
  * :dtcompatible:`ti,lmp90078`
  * :dtcompatible:`ti,lmp90079`
  * :dtcompatible:`ti,lmp90080`
  * :dtcompatible:`ti,lmp90097`
  * :dtcompatible:`ti,lmp90098`
  * :dtcompatible:`ti,lmp90099`
  * :dtcompatible:`ti,lmp90100`

* :dtcompatible:`microchip,mcp3204` 和 :dtcompatible:`microchip,mcp3208` 设备树绑定的 io-channel 单元已从 ``channel`` 重命名为通用的 ``input``，使其能够与 Microchip MCP320x ADC 设备一起使用各种 ADC DT 宏。

蓝牙 HCI
=============

* 蓝牙 HCI 驱动程序 API 中的可选 :c:func:`setup()` 函数（通过 :kconfig:option:`CONFIG_BT_HCI_SETUP` 启用）已获得类型为 :c:struct:`bt_hci_setup_params` 的函数参数。默认情况下，该结构体为空，但驱动程序可以选择 :kconfig:option:`CONFIG_BT_HCI_SET_PUBLIC_ADDR` 如果它们支持设置控制器的公共身份地址，该地址随后将传递在 ``public_addr`` 字段中。（:github:`62994`）

* 基于 ST BlueNRG-MS 的开发板
  应使用 :dtcompatible:`st,hci-spi-v1`
  而非 :dtcompatible:`zephyr,bt-hci-spi`。

控制器局域网（CAN）
=============================

* 现在可在 ``native_posix`` 和 :zephyr:board:`native_sim<native_sim>` 中无论是否使用嵌入式 C 库的原生 Linux SocketCAN 驱动程序已重命名以反映这一点：

  * 设备树 compatible 已从 ``zephyr,native-posix-linux-can`` 重命名为 :dtcompatible:`zephyr,native-linux-can`。
  * 主 Kconfig 选项已从 ``CONFIG_CAN_NATIVE_POSIX_LINUX`` 重命名为 :kconfig:option:`CONFIG_CAN_NATIVE_LINUX`。

* 引入了两个新的结构体（用于持有通用的 CAN 控制器驱动程序配置（``struct can_driver_config``）和数据（``struct can_driver_data``）字段）。树外的 CAN 控制器驱动程序需要更新为使用这些新的通用配置和数据结构体连同其初始化宏。

* 可选的 ``can_get_max_bitrate_t`` CAN 控制器驱动程序回调已移除，改为通用的访问器函数。树外的 CAN 控制器驱动程序需要更新为不再提供此回调。

* CAN 收发器 API 函数 :c:func:`can_transceiver_enable` 现在接受 :c:type:`can_mode_t` 参数，用于将 CAN 控制器操作模式传播到 CAN 收发器。树外的 CAN 控制器和 CAN 收发器驱动程序需要更新以匹配此新的 API 函数签名。

* 用于过滤经典 CAN/CAN FD 帧的 ``CAN_FILTER_FDF`` 标志已移除，因为没有已知的 CAN 控制器实现对此的支持。应用程序仍可在需要时在其接收回调函数中过滤经典 CAN/CAN FD 帧。

* 用于在 Data 帧和远程传输请求（RTR）帧之间过滤的 ``CAN_FILTER_DATA`` 和 ``CAN_FILTER_RTR`` 标志已移除，因为并非所有 CAN 控制器都实现了基于 RTR 位的单个接收过滤支持。应用程序现在可以使用 :kconfig:option:`CONFIG_CAN_ACCEPT_RTR` 来接受匹配 CAN 过滤器的传入 RTR 帧或拒绝所有传入的 CAN RTR 帧（默认）。启用 :kconfig:option:`CONFIG_CAN_ACCEPT_RTR` 时，应用程序仍可在需要时在其接收回调函数中过滤 Data 帧和 RTR 帧。

* :dtcompatible:`st,stm32h7-fdcan` CAN 控制器驱动程序现在支持通过设备树配置域/内核时钟。此前，驱动程序仅支持使用 PLL1_Q 时钟作为内核时钟，但现在默认为 HSE 时钟，这是芯片的默认值。使用 PLL1_Q 时钟的 FDCAN 的开发板需要如下覆盖 ``clocks`` 属性：

  .. code-block:: devicetree

    &fdcan1 {
            clocks = <&rcc STM32_CLOCK_BUS_APB1_2 0x00000100>,
                     <&rcc STM32_SRC_PLL1_Q FDCAN_SEL(1)>;
    };

显示
=======

* 基于 ILI9XXX 的显示屏现在使用 MIPI DBI 驱动程序类。这些显示屏现在必须在 MIPI DBI 驱动程序包装设备内声明，该设备将管理与显示屏的接口。注意 `cmd-data-gpios` 引脚已随此更新更改极性，以更好地与新 `dc-gpios` 名称对齐。示例参见下方：

  .. code-block:: devicetree

    /* 传统 ILI9XXX 显示屏定义 */
    &spi2 {
        ili9340: ili9340@0 {
            compatible = "ilitek,ili9340";
            reg = <0>;
            spi-max-frequency = <32000000>;
            reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
            cmd-data-gpios = <&gpio0 12 GPIO_ACTIVE_LOW>;
            rotation = <270>;
            width = <320>;
            height = <240>;
        };
    };

    /* 带 MIPI DBI 设备的新显示屏定义 */

    mipi_dbi {
        compatible = "zephyr,mipi-dbi-spi";
        reset-gpios = <&gpio0 6 GPIO_ACTIVE_LOW>;
        dc-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        spi-dev = <&spi2>;
        #address-cells = <1>;
        #size-cells = <0>;

        ili9340: ili9340@0 {
            compatible = "ilitek,ili9340";
            reg = <0>;
            mipi-max-frequency = <32000000>;
            rotation = <270>;
            width = <320>;
            height = <240>;
        };
    };

闪存
=====

* :dtcompatible:`st,stm32-ospi-nor` 和 :dtcompatible:`st,stm32-qspi-nor` 通过 **reg** 属性给出 nor 闪存基地址和大小（以字节计）。<size> 属性不再使用。

  .. code-block:: devicetree

    mx25lm51245: ospi-nor-flash@70000000 {
            compatible = "st,stm32-ospi-nor";
            reg = <0x70000000 DT_SIZE_M(64)>; /* 512 Mbits*/
    };

通用输入/输出（GPIO）
==========================

* :dtcompatible:`nxp,pcf8574` 驱动程序已重命名为 :dtcompatible:`nxp,pcf857x`。（:github:`67054`）以支持 pcf8574 和 pcf8575。Kconfig 选项已从 :kconfig:option:`CONFIG_GPIO_PCF8574` 重命名为 :kconfig:option:`CONFIG_GPIO_PCF857X`。设备树可配置如下：

  .. code-block:: devicetree

    &i2c {
      status = "okay";
      pcf8574: pcf857x@20 {
          compatible = "nxp,pcf857x";
          status = "okay";
          reg = <0x20>;
          gpio-controller;
          #gpio-cells = <2>;
          ngpios = <8>;
      };

      pcf8575: pcf857x@21 {
          compatible = "nxp,pcf857x";
          status = "okay";
          reg = <0x21>;
          gpio-controller;
          #gpio-cells = <2>;
          ngpios = <16>;
      };
    };

输入
=====

* 触摸屏驱动程序 :dtcompatible:`focaltech,ft5336` 和 :dtcompatible:`goodix,gt911` 对其相应的 ``reset-gpios`` 使用了不正确的极性。这已修复，因此这些信号现在必须在设备树中标记为 :c:macro:`GPIO_ACTIVE_LOW`。（:github:`64800`）

中断控制器
==================

* 通过 :c:func:`shared_irq_isr_register()` 传递给 ``shared_irq`` 中断控制器驱动程序 API 的 ``isr_t`` 回调函数的函数签名已更改。该回调现在接受额外的 `irq_number` 参数。此 API 的树外用户需要更新。（:github:`66427`）

瑞萨 RA 系列驱动程序
=========================

* 若干瑞萨 RA 系列驱动程序 Kconfig 选项已重命名：

  * ``CONFIG_CLOCK_CONTROL_RA`` -> :kconfig:option:`CONFIG_CLOCK_CONTROL_RENESAS_RA`
  * ``CONFIG_GPIO_RA`` -> :kconfig:option:`CONFIG_GPIO_RENESAS_RA`
  * ``CONFIG_PINCTRL_RA`` -> :kconfig:option:`CONFIG_PINCTRL_RENESAS_RA`
  * ``CONFIG_UART_RA`` -> :kconfig:option:`CONFIG_UART_RENESAS_RA`

传感器
=======

* :dtcompatible:`st,lsm6dsv16x` 传感器驱动程序已更改以支持配置 int1 和 int2 引脚。DT 属性 ``irq-gpios`` 已移除，替换为两个新属性 ``int1-gpios`` 和 ``int2-gpios``。这些属性必须在设备树中配置，类似以下示例：

  .. code-block:: devicetree

    / {
        lsm6dsv16x@0 {
            compatible = "st,lsm6dsv16x";

            int1-gpios = <&gpioa 4 GPIO_ACTIVE_HIGH>;
            int2-gpios = <&gpiod 11 GPIO_ACTIVE_HIGH>;
            drdy-pin = <2>;
        };
    };

串口
======

* 运行时配置
  现在对 Nordic UART 驱动程序
  默认禁用。
  更改的动机是
  此特性很少使用，
  且禁用它显著减少了内存占用。

定时器
=====

* 在低功耗模式下计数节拍时选择的 :dtcompatible:`st,stm32-lptim` lptim 在设备树中由 **stm32_lp_tick_source** 标识如下。stm32_lptim_timer 驱动程序已更改以支持此。

  .. code-block:: devicetree

    stm32_lp_tick_source: &lptim1 {
            status = "okay";
    };

蓝牙
*********

* ATT 现在有其自身的 TX 缓冲区池。如果使用 :kconfig:option:`CONFIG_BT_L2CAP_TX_BUF_COUNT` 配置了额外的 ATT 缓冲区，它们现在应通过 :kconfig:option:`CONFIG_BT_ATT_TX_COUNT` 配置。
* Host 和 Controller 两侧的 HCI 实现已为 IPC 传输重命名。``CONFIG_BT_RPMSG`` Kconfig 选项现在为 :kconfig:option:`CONFIG_BT_HCI_IPC`，且 ``zephyr,bt-hci-rpmsg-ipc`` 设备树 chosen 现在为 ``zephyr,bt-hci-ipc``。现有的示例也已重命名，从 ``samples/bluetooth/hci_rpmsg`` 到 ``samples/bluetooth/hci_ipc``。（:github:`64391`）
* 由 :c:func:`bt_gatt_cb_register` 追加的 BT GATT 回调列表不再在 :c:func:`bt_enable` 时清除。回调现在可在初始 :c:func:`bt_enable` 调用前注册，且不应再在 :c:func:`bt_disable` :c:func:`bt_enable` 周期后重新注册。（:github:`63693`）
* 蓝牙 UUID 已在 ``BT_UUID_DECLARE_16``、``BT_UUID_DECLARE_32`` 和 ``BT_UUID_DECLARE_128`` 中修改为 rodata，因为返回值已更改为 ``const``。指向 UUID 的任何指针必须前缀 ``const``，否则将有编译警告。例如将 ``struct bt_uuid *uuid = BT_UUID_DECLARE_16(xx)`` 改为 ``const struct bt_uuid *uuid = BT_UUID_DECLARE_16(xx)``。（:github:`66136`）
* :c:func:`bt_l2cap_chan_send` API 在将 SDUs 分段为 PDUs 时不再从与其 `buf` 参数相同的池分配缓冲区。要重现先前行为，应用程序应注册 `alloc_seg` 通道回调并从与 `buf` 相同的池分配。
* :c:func:`bt_l2cap_chan_send` API 现在要求应用程序为 L2CAP 头保留足够的字节。在缓冲区分配时调用 ``net_buf_reserve(buf, BT_L2CAP_SDU_CHAN_SEND_RESERVE);`` 完成。
* `BT_ISO_TIMESTAMP_NONE` 已移除，且 :c:func:`bt_iso_chan_send` 的 `ts` 参数也已移除。:c:func:`bt_iso_chan_send` 现在始终无时间戳发送。要带时间戳发送，可使用 :c:func:`bt_iso_chan_send_ts`。
* ``CONFIG_BT_HCI_RESERVE`` 和 ``CONFIG_BT_HCI_RAW_RESERVE`` Kconfig 选项已移除。所有缓冲区现在默认获得 1 字节的头余量，HCI 传输实现可依赖此（无论其是否需要）。

蓝牙 Mesh
=============

  * 蓝牙 Mesh ``model`` 声明已更改为添加前缀 ``const``。``model->user_data``、``model->elem_idx`` 和 ``model->mod_idx`` 字段已更改为新的运行时结构体，分别替换为 ``model->rt->user_data``、``model->rt->elem_idx`` 和 ``model->rt->mod_idx``。（:github:`65152`）
  * 蓝牙 Mesh ``element`` 声明已更改为添加前缀 ``const``。``elem->addr`` 字段已更改为新的运行时结构体，替换为 ``elem->rt->addr``。（:github:`65388`）
  * 已弃用 :kconfig:option:`CONFIG_BT_MESH_PROV_DEVICE`。此选项已被新选项 :kconfig:option:`CONFIG_BT_MESH_PROVISIONEE` 替换，以对齐 Mesh 协议规范 v1.1 第 5.4 节。（:github:`64252`）
  * 移除了 ``CONFIG_BT_MESH_V1d1`` Kconfig 选项。
  * 移除了 ``CONFIG_BT_MESH_TX_SEG_RETRANS_COUNT``、``CONFIG_BT_MESH_TX_SEG_RETRANS_TIMEOUT_UNICAST``、``CONFIG_BT_MESH_TX_SEG_RETRANS_TIMEOUT_GROUP``、``CONFIG_BT_MESH_SEG_ACK_BASE_TIMEOUT``、``CONFIG_BT_MESH_SEG_ACK_PER_HOP_TIMEOUT``、``BT_MESH_SEG_ACK_PER_SEGMENT_TIMEOUT`` Kconfig 选项。它们已被 :kconfig:option:`CONFIG_BT_MESH_SAR_TX_SEG_INT_STEP`、:kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_COUNT`、:kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_WITHOUT_PROG_COUNT`、:kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_STEP`、:kconfig:option:`CONFIG_BT_MESH_SAR_TX_UNICAST_RETRANS_INT_INC`、:kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_COUNT`、:kconfig:option:`CONFIG_BT_MESH_SAR_TX_MULTICAST_RETRANS_INT`、:kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_THRESHOLD`、:kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_DELAY_INC`、:kconfig:option:`CONFIG_BT_MESH_SAR_RX_SEG_INT_STEP`、:kconfig:option:`CONFIG_BT_MESH_SAR_RX_DISCARD_TIMEOUT`、:kconfig:option:`CONFIG_BT_MESH_SAR_RX_ACK_RETRANS_COUNT` Kconfig 选项取代。

蓝牙音频
================

  * ``<zephyr/bluetooth/audio/lc3.h>`` 中的 ``BT_AUDIO_CODEC_LC3_*`` 值已移到 ``<zephyr/bluetooth/audio/audio.h>``，且其名称的 ``LC3`` 部分已替换为更语义正确的名称：例如 ``BT_AUDIO_CODEC_LC3_CHAN_COUNT`` 现在为 ``BT_AUDIO_CODEC_CAP_TYPE_CHAN_COUNT``，``BT_AUDIO_CODEC_LC3_FREQ`` 现在为 ``BT_AUDIO_CODEC_CAP_TYPE_FREQ``，且 ``BT_AUDIO_CODEC_CONFIG_LC3_FREQ`` 现在为 ``BT_AUDIO_CODEC_CFG_FREQ`` 等。类似地，枚举也已重命名。例如 ``bt_audio_codec_config_freq`` 现在为 ``bt_audio_codec_cfg_freq``，``bt_audio_codec_capability_type`` 现在为 ``bt_audio_codec_cap_type``，``bt_audio_codec_config_type`` 现在为 ``bt_audio_codec_cfg_type`` 等。（:github:`67024`）
  * :c:func:`bt_bap_stream_send` 的 `ts` 参数已移除。:c:func:`bt_bap_stream_send` 现在始终无时间戳发送。要带时间戳发送，可使用 :c:func:`bt_bap_stream_send_ts`。
  * :c:func:`bt_cap_stream_send` 的 `ts` 参数已移除。:c:func:`bt_cap_stream_send` 现在始终无时间戳发送。要带时间戳发送，可使用 :c:func:`bt_cap_stream_send_ts`。

网络
**********

* CoAP 公共 API 有一些需要注意的细微更改。:c:func:`coap_remove_observer` 现在在观察者被移除时返回结果。此更改由新引入的 :ref:`coap_server_interface` 子系统使用。此外，:c:func:`coap_well_known_core_get` 的 ``request`` 参数已变为 ``const``。（:github:`64265`）

* CoAP 观察者事件已从 CoAP 资源中的回调函数移到网络事件子系统。``CONFIG_COAP_OBSERVER_EVENTS`` 配置选项已移除。（:github:`65936`）

* CoAP 公共 API 函数 :c:func:`coap_pending_init` 已更改。参数 ``retries`` 已替换为指向 :c:struct:`coap_transmission_parameters` 的指针。这允许指定可确认消息的重传参数。传递 NULL 指针以使用默认值是安全的。（:github:`66482`）

* CoAP 公共 API 函数 :c:func:`coap_service_send` 和 :c:func:`coap_resource_send` 已更改。已添加额外的参数（指向 :c:struct:`coap_transmission_parameters` 的指针）。传递 NULL 指针以使用默认值是安全的。（:github:`66540`）

* IGMP 多播库现在支持 IGMPv3。这导致现有 API 的细微更改。:c:func:`net_ipv4_igmp_join` 现在接受额外的参数（类型 ``const struct igmp_param *param``）。这允许 IGMPv3 排除/包含特定的地址组。如果此功能未使用或不可用（使用 IGMPv2 时），你可安全地传递 NULL 指针。IGMPv3 可用 Kconfig ``CONFIG_NET_IPV4_IGMPV3`` 启用。（:github:`65293`）

* 网络栈现在为多播数据包使用单独的 IPv4 TTL（生存时间）值。此前，单播和多播数据包使用相同的 TTL 值。IPv6 跳数限制值也已更改，使单播和多播数据包可以有不同的值。（:github:`65886`）

* 在 ``<zephyr/net/phy.h>`` 中定义的以太网 phy API 已从系统调用列表移除。这些 API 标记为可从用户模式调用，但实践中这不工作，因为设备无法从用户模式线程访问。这意味着 API 调用需从监督模式线程执行。

* Zperf 中 mbps 和 kbps、kbps 和 bps 的比率已更改为 1000，而非 1024，以对齐 iperf 比率。

* 已为网络缓冲区池最大分配大小添加到通用结构体 ``struct net_buf_data_alloc``（作为新字段 ``max_alloc_size``）。仅对固定大小缓冲区池特定的 ``struct net_buf_pool_fixed`` 的类似成员 ``data_size`` 已移除。

其他子系统
****************

LoRaWAN
=======

* 向 LoRaWAN 栈
  提供电池电量信息的回调的 API
  已从 ``lorawan_set_battery_level_callback``
  重命名为 :c:func:`lorawan_register_battery_level_callback`，
  且返回类型现在为 ``void``。
  这与下行链路和数据速率更改回调的
  类似函数更一致。
  （:github:`65103`）

MCUmgr
======

* 使用串行传输（shell 或 UART）的
  MCUmgr 应用程序
  现在必须选择 :kconfig:option:`CONFIG_CRC`，
  此前如果 MCUmgr 启用
  则错误地选择了此选项，
  而对非串行传输则不需要。
  （:github:`64078`）

Shell
=====

* 以下子系统和驱动程序 shell 模块现在默认禁用。每个所需的 shell 模块现在必须通过 Kconfig 显式启用（:github:`65307`）：

  * :kconfig:option:`CONFIG_ACPI_SHELL`
  * :kconfig:option:`CONFIG_ADC_SHELL`
  * :kconfig:option:`CONFIG_AUDIO_CODEC_SHELL`
  * :kconfig:option:`CONFIG_CAN_SHELL`
  * :kconfig:option:`CONFIG_CLOCK_CONTROL_NRF_SHELL`
  * :kconfig:option:`CONFIG_DAC_SHELL`
  * :kconfig:option:`CONFIG_DEBUG_COREDUMP_SHELL`
  * :kconfig:option:`CONFIG_EDAC_SHELL`
  * :kconfig:option:`CONFIG_EEPROM_SHELL`
  * :kconfig:option:`CONFIG_FLASH_SHELL`
  * :kconfig:option:`CONFIG_HWINFO_SHELL`
  * :kconfig:option:`CONFIG_I2C_SHELL`
  * :kconfig:option:`CONFIG_LOG_CMDS`
  * :kconfig:option:`CONFIG_LORA_SHELL`
  * :kconfig:option:`CONFIG_MCUBOOT_SHELL`
  * :kconfig:option:`CONFIG_MDIO_SHELL`
  * :kconfig:option:`CONFIG_OPENTHREAD_SHELL`
  * :kconfig:option:`CONFIG_PCIE_SHELL`
  * :kconfig:option:`CONFIG_PSCI_SHELL`
  * :kconfig:option:`CONFIG_PWM_SHELL`
  * :kconfig:option:`CONFIG_REGULATOR_SHELL`
  * :kconfig:option:`CONFIG_SENSOR_SHELL`
  * :kconfig:option:`CONFIG_SMBUS_SHELL`
  * :kconfig:option:`CONFIG_STATS_SHELL`
  * :kconfig:option:`CONFIG_USBD_SHELL`
  * :kconfig:option:`CONFIG_USBH_SHELL`
  * :kconfig:option:`CONFIG_W1_SHELL`
  * :kconfig:option:`CONFIG_WDT_SHELL`

* ``SHELL_UART_DEFINE`` 宏现在仅要求 ``_name`` 参数。同时，该宏接受额外的参数（环形缓冲区 TX & RX 大小参数）以兼容先前的 Zephyr 版本，但被忽略，且将在未来版本中移除。

* :kconfig:option:`CONFIG_SHELL_BACKEND_SERIAL_API` 现在不再在启用 :kconfig:option:`CONFIG_UART_ASYNC_API` 时自动默认为 :kconfig:option:`CONFIG_SHELL_BACKEND_SERIAL_API_ASYNC`，:kconfig:option:`CONFIG_SHELL_ASYNC_API` 也必须启用才能使用异步串行 shell（:github:`68475`）。

ZBus
====

* ``CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_DYNAMIC`` 和 ``CONFIG_ZBUS_MSG_SUBSCRIBER_NET_BUF_STATIC`` zbus 选项已重命名。相反，应使用新的 :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_BUF_ALLOC_DYNAMIC` 和 :kconfig:option:`CONFIG_ZBUS_MSG_SUBSCRIBER_BUF_ALLOC_STATIC` 选项。（:github:`65632`）

* 要启用 zbus HLP 优先级提升，开发者必须在附加的线程内调用 :c:func:`zbus_obs_attach_to_thread`。观察者随后将假设附加的线程优先级，zbus 用其计算 HLP 优先级。（:github:`63183`）

用户空间
*********

* 若干用户空间相关函数已从 ``z_`` 命名空间移到内核命名空间。

  * ``Z_OOPS`` 到 :c:macro:`K_OOPS`
  * ``Z_SYSCALL_MEMORY`` 到 :c:macro:`K_SYSCALL_MEMORY`
  * ``Z_SYSCALL_MEMORY_READ`` 到 :c:macro:`K_SYSCALL_MEMORY_READ`
  * ``Z_SYSCALL_MEMORY_WRITE`` 到 :c:macro:`K_SYSCALL_MEMORY_WRITE`
  * ``Z_SYSCALL_DRIVER_OP`` 到 :c:macro:`K_SYSCALL_DRIVER_OP`
  * ``Z_SYSCALL_SPECIFIC_DRIVER`` 到 :c:macro:`K_SYSCALL_SPECIFIC_DRIVER`
  * ``Z_SYSCALL_OBJ`` 到 :c:macro:`K_SYSCALL_OBJ`
  * ``Z_SYSCALL_OBJ_INIT`` 到 :c:macro:`K_SYSCALL_OBJ_INIT`
  * ``Z_SYSCALL_OBJ_NEVER_INIT`` 到 :c:macro:`K_SYSCALL_OBJ_NEVER_INIT`
  * ``z_user_from_copy`` 到 :c:func:`k_usermode_from_copy`
  * ``z_user_to_copy`` 到 :c:func:`k_usermode_to_copy`
  * ``z_user_string_copy`` 到 :c:func:`k_usermode_string_copy`
  * ``z_user_string_alloc_copy`` 到 :c:func:`k_usermode_string_alloc_copy`
  * ``z_user_alloc_from_copy`` 到 :c:func:`k_usermode_alloc_from_copy`
  * ``z_user_string_nlen`` 到 :c:func:`k_usermode_string_nlen`
  * ``z_dump_object_error`` 到 :c:func:`k_object_dump_error`
  * ``z_object_validate`` 到 :c:func:`k_object_validate`
  * ``z_object_find`` 到 :c:func:`k_object_find`
  * ``z_object_wordlist_foreach`` 到 :c:func:`k_object_wordlist_foreach`
  * ``z_thread_perms_inherit`` 到 :c:func:`k_thread_perms_inherit`
  * ``z_thread_perms_set`` 到 :c:func:`k_thread_perms_set`
  * ``z_thread_perms_clear`` 到 :c:func:`k_thread_perms_clear`
  * ``z_thread_perms_all_clear`` 到 :c:func:`k_thread_perms_all_clear`
  * ``z_object_uninit`` 到 :c:func:`k_object_uninit`
  * ``z_object_recycle`` 到 :c:func:`k_object_recycle`
  * ``z_obj_validation_check`` 到 :c:func:`k_object_validation_check`
  * ``Z_SYSCALL_VERIFY_MSG`` 到 :c:macro:`K_SYSCALL_VERIFY_MSG`
  * ``z_object`` 到 :c:struct:`k_object`
  * ``z_object_init`` 到 :c:func:`k_object_init`
  * ``z_dynamic_object_aligned_create`` 到 :c:func:`k_object_create_dynamic_aligned`

架构
*************

Xtensa
======

* :kconfig:option:`CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC` 在架构层不再默认。相反，SoC 或开发板需要定义它。

* 暂存寄存器 ``ZSR_ALLOCA`` 已重命名为 ``ZSR_A0SAVE``。

* 将带连字符的文件重命名为下划线：

  * ``xtensa-asm2-context.h`` 到 ``xtensa_asm2_context.h``

  * ``xtensa-asm2-s.h`` 到 ``xtensa_asm2_s.h``

* ``xtensa_asm2.h`` 已移除。改用 ``xtensa_asm2_context.h`` 用于栈帧结构体。

* 将函数从 ``z_`` 命名空间重命名为 ``xtensa_`` 命名空间。

  * ``z_xtensa_irq_enable`` 到 :c:func:`xtensa_irq_enable`

  * ``z_xtensa_irq_disable`` 到 :c:func:`xtensa_irq_disable`

  * ``z_xtensa_irq_is_enabled`` 到 :c:func:`xtensa_irq_is_enabled`
