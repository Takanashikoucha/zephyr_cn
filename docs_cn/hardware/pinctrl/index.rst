.. _pinctrl-guide:

引脚控制
###########

这是引脚控制的高层指南。API 参考材料参见 :ref:`pinctrl_api`。

简介
************

控制引脚复用以及引脚方向、上拉/下拉电阻等引脚配置参数的硬件块称为**引脚控制器**。引脚控制器的主要用户是 SoC 硬件外设，因为控制器能够暴露外设信号，例如将 ``I2C0`` 的 ``SDA`` 信号映射到引脚 ``PX0``。不仅如此，它通常还允许配置外设正确运行所必需的某些引脚设置，例如根据工作频率设置摆率（slew-rate）。可用的配置选项因厂商/SoC 而异，从简单的上拉/下拉选项到更高级的设置（如去抖动、低功耗模式等）。

引脚控制在硬件中的实现方式因厂商/SoC 而异。常见的是*集中式*方法，即所有引脚配置参数（包括信号映射）由单个硬件块（通常称为引脚复用器 pinmux）控制。下图说明了这种方法。``PX0`` 可以根据 ``AF`` 控制位映射到 ``UART0_TX``、``I2C0_SCK`` 或 ``SPI0_MOSI``。上拉/下拉等其他配置参数通过同一硬件块中的 ``CONFIG`` 位控制。多个 SoC 系列（如 NXP 和 STM32 的许多系列）采用此模型。

.. figure:: images/hw-cent-control.svg

    引脚控制集中在单个每引脚硬件块中的示例

其他厂商/SoC 使用*分布式*方法。在这种情况下，引脚映射和配置由多个硬件块控制。下图说明了一种分布式方法，其中引脚映射由外设控制，例如 Nordic nRF SoC 中就是如此。

.. figure:: images/hw-dist-control.svg

    引脚控制分布在外设寄存器与每引脚硬件块之间的示例

从用户角度看，无论硬件如何实现，引脚控制器的使用方式都没有区别：用户总是应用一个状态。唯一的区别在于驱动程序的实现。一般来说，为采用分布式方法的硬件实现引脚控制器驱动程序需要更多工作量，因为驱动程序需要掌握依赖外设的寄存器知识。

引脚控制与 GPIO
====================

引脚控制器驱动程序覆盖的一些功能与 GPIO 驱动程序重叠。例如，上拉/下拉电阻通常既可以由引脚控制驱动程序启用，也可以由 GPIO 驱动程序启用。在 Zephyr 中，引脚控制驱动程序的作用是执行外设信号复用，并配置该外设正确运行所需的其他引脚参数。因此，引脚控制驱动程序的主要用户是 SoC 外设。相比之下，GPIO 驱动程序用于对引脚进行通用控制，即手动读取或控制其逻辑电平的场景。

状态模型
***********

设备驱动程序要正确运行，需要应用特定的引脚配置。一些设备驱动程序需要静态配置，通常在初始化时设置。另一些需要在运行时根据工作条件更改配置，例如在设备挂起时启用低功耗模式。这些需求使用**状态**来建模，这一概念借鉴自 Linux 内核。每个设备驱动程序拥有一组状态，每个状态有唯一名称，并包含一组完整的引脚配置（参见下图）。这实际上意味着状态之间相互独立，因此不需要按任何特定顺序应用。状态模型的另一个优点是将设备驱动程序与引脚配置隔离开来。

.. table:: 使用状态模型编码的示例引脚配置
    :align: center

    +----+------------------+----+------------------+
    | ``UART0`` 外设                             |
    +====+==================+====+==================+
    | ``default`` 状态     | ``sleep`` 状态       |
    +----+------------------+----+------------------+
    | TX | - 引脚: PA0       | TX | - 引脚: PA0       |
    |    | - 上拉/下拉: NONE     |    | - 上拉/下拉: NONE     |
    |    | - 低功耗: NO  |    | - 低功耗: YES |
    +----+------------------+----+------------------+
    | RX | - 引脚: PA1       | RX | - 引脚: PA1       |
    |    | - 上拉/下拉: UP       |    | - 上拉/下拉: NONE     |
    |    | - 低功耗: NO  |    | - 低功耗: YES |
    +----+------------------+----+------------------+

标准状态
==============

分配给引脚控制状态的名称或其数量由设备驱动程序的需求决定。在许多情况下，初始化时应用单个状态就足够了，但在另一些情况下则需要更多状态。为保持一致性，已为最常见的用例建立了命名约定。下表详述了标准化状态及其用途。

.. table:: 标准化状态名称
    :align: center

    +-------------+----------------------------------+-------------------------+
    | 状态        | 标识符                           | 用途                    |
    +-------------+----------------------------------+-------------------------+
    | ``default`` | :c:macro:`PINCTRL_STATE_DEFAULT` | 设备处于工作状态时      |
    |             |                                  | 引脚的状态              |
    +-------------+----------------------------------+-------------------------+
    | ``sleep``   | :c:macro:`PINCTRL_STATE_SLEEP`   | 设备处于低功耗或睡眠  |
    |             |                                  | 模式时引脚的状态        |
    +-------------+----------------------------------+-------------------------+

注意未来可能引入其他标准状态。

自定义状态
=============

一些设备驱动程序可能需要使用标准状态之外的自定义状态。为此，设备驱动程序需要在自身作用域内定义名为 ``PINCTRL_STATE_{STATE_NAME}`` 的自定义状态标识符，其中 ``{STATE_NAME}`` 是大写的状态名。例如，如果要支持 ``mystate``，就需要在驱动程序作用域内存在名为 ``PINCTRL_STATE_MYSTATE`` 的定义。

.. note::
    自定义状态标识符必须从 :c:macro:`PINCTRL_STATE_PRIV_START` 开始

如果自定义状态需要从驱动程序外部访问（例如执行动态引脚控制），则自定义标识符应放在公开可访问的头文件中。

跳过状态
==============

在大多数情况下，Devicetree 中定义的状态就是编译后的固件中使用的状态。但有些情况下，某些状态会根据编译标志被条件性地使用。典型情况是 ``sleep`` 状态：该状态实际上仅在启用 :kconfig:option:`CONFIG_PM` 或 :kconfig:option:`CONFIG_PM_DEVICE` 时才会被使用。如果需要没有这些电源管理配置的固件变体，理论上应从 Devicetree 中移除 ``sleep`` 状态，以免浪费 ROM 空间存储这种未使用的状态。

当定义引脚控制配置时，如果存在展开为 ``1`` 的名为 ``PINCTRL_SKIP_{STATE_NAME}`` 的定义，``pinctrl`` Devicetree 宏可以跳过相应状态。对于 ``sleep`` 状态，``pinctrl`` API 已根据设备电源管理是否可用提供了这样的条件定义：

.. code-block:: c

    #if !defined(CONFIG_PM) && !defined(CONFIG_PM_DEVICE)
    /** Out of power management configurations, ignore "sleep" state. */
    #define PINCTRL_SKIP_SLEEP 1
    #endif

动态引脚控制
*******************

动态引脚控制指在运行时更改引脚配置的能力。当同一固件需要在略有差异的多个板卡上运行、而每个板卡将某外设路由到不同引脚组时，此功能非常有用。通过设置 :kconfig:option:`CONFIG_PINCTRL_DYNAMIC` 可启用此功能。

.. note::

    动态引脚控制只应用于尚未初始化的设备。在设备运行期间更改引脚配置可能导致意外行为。由于 Zephyr 尚不支持设备反初始化，此功能只应用于早期启动阶段。

启用动态引脚控制的效果之一是 :c:struct:`pinctrl_dev_config` 将存储在 RAM 而非 ROM 中（但状态和引脚配置本身不存储于 RAM）。用户随后可使用 :c:func:`pinctrl_update_states` 用一组新状态更新存储在 :c:struct:`pinctrl_dev_config` 中的状态。这实际上意味着设备驱动程序在应用状态时，将应用更新后的状态中存储的引脚配置。

Devicetree 表示
*************************

Devicetree 旨在描述硬件，因此是存储引脚控制配置的自然选择。以下各节将概述状态和引脚配置在 Devicetree 中的表示方式。

状态
======

对于给定设备，其每个引脚控制状态在 Devicetree 中由 ``pinctrl-N`` 属性表示，``N`` 为从零开始的状态索引。``pinctrl-names`` 属性则按索引为每个状态属性分配唯一标识符，例如 ``pinctrl-names`` 列表的第 0 项就是 ``pinctrl-0`` 的名称。

.. code-block:: devicetree

    periph0: periph@0 {
        ...
        /* state 0 ("default") */
        pinctrl-0 = <...>;
        ...
        /* state N ("mystate") */
        pinctrl-N = <...>;
        /* names for state 0 up to state N */
        pinctrl-names = "default", ..., "mystate";
        ...
    };

引脚配置
=================

在 Devicetree 中表示引脚配置有多种方式。但所有方式最终编码的都是相同的信息：引脚复用和引脚配置参数。例如，``UART_RX`` 映射到 ``PX0`` 且启用上拉。表示方式的选择很大程度上取决于各厂商/SoC，因此引脚控制驱动程序的 Devicetree 绑定（binding）文件是查找细节的最佳去处。

下面示例展示了一种流行且通用的选项。这种选择的一个优点是可以基于共享的引脚配置进行分组，从而减少引脚控制定义的冗长性。另一个优点是特定状态的引脚配置参数被封装在单个 Devicetree 节点中。

.. code-block:: devicetree

    /* board.dts */
    #include "board-pinctrl.dtsi"

    &periph0 {
        pinctrl-0 = <&periph0_default>;
        pinctrl-names = "default";
    };

.. code-block:: c

    /* vnd-soc-pkgxx.h
     * File with valid mappings for a specific package (may be autogenerated).
     * This file is optional, but recommended.
     */
    ...
    #define PERIPH0_SIGA_PX0 VNDSOC_PIN(X, 0, MUX0)
    #define PERIPH0_SIGB_PY7 VNDSOC_PIN(Y, 7, MUX4)
    #define PERIPH0_SIGC_PZ1 VNDSOC_PIN(Z, 1, MUX2)
    ...

.. code-block:: devicetree

    /* board-pinctrl.dtsi */
    #include <vnd-soc-pkgxx.h>

    &pinctrl {
        /* Node with pin configuration for default state */
        periph0_default: periph0_default {
            group1 {
                /* Mappings: PERIPH0_SIGA -> PX0, PERIPH0_SIGC -> PZ1 */
                pinmux = <PERIPH0_SIGA_PX0>, <PERIPH0_SIGC_PZ1>;
                /* Pins PX0 and PZ1 have pull-up enabled */
                bias-pull-up;
            };
            ...
            groupN {
                /* Mappings: PERIPH0_SIGB -> PY7 */
                pinmux = <PERIPH0_SIGB_PY7>;
            };
        };
    };

另一种流行模型是为每个引脚配置和状态各建一个节点。虽然该模型可能使板卡引脚控制文件更短，但由于节点通常不能复用于多个状态，它要求为每个引脚映射和状态都建一个节点。如果不能自动生成，则不推荐此方法。

.. note::

    由于所有 Devicetree 信息都会被解析成 C 头文件，务必将其大小保持在最小。为此，预生成的节点应以 ``/omit-if-no-ref/`` 作为前缀。该前缀确保节点未被引用时被丢弃。

.. code-block:: devicetree

    /* board.dts */
    #include "board-pinctrl.dtsi"

    &periph0 {
        pinctrl-0 = <&periph0_siga_px0_default &periph0_sigb_py7_default
                     &periph0_sigc_pz1_default>;
        pinctrl-names = "default";
    };

.. code-block:: devicetree

    /* vnd-soc-pkgxx.dtsi
     * File with valid nodes for a specific package (may be autogenerated).
     * This file is optional, but recommended.
     */

    &pinctrl {
        /* Mapping for PERIPH0_SIGA -> PX0, to be used for default state */
        /omit-if-no-ref/ periph0_siga_px0_default: periph0_siga_px0_default {
            pinmux = <VNDSOC_PIN(X, 0, MUX0)>;
        };

        /* Mapping for PERIPH0_SIGB -> PY7, to be used for default state */
        /omit-if-no-ref/ periph0_sigb_py7_default: periph0_sigb_py7_default {
            pinmux = <VNDSOC_PIN(Y, 7, MUX4)>;
        };

        /* Mapping for PERIPH0_SIGC -> PZ1, to be used for default state */
        /omit-if-no-ref/ periph0_sigc_pz1_default: periph0_sigc_pz1_default {
            pinmux = <VNDSOC_PIN(Z, 1, MUX2)>;
        };
    };

.. code-block:: devicetree

    /* board-pinctrl.dts */
    #include <vnd-soc-pkgxx.dtsi>

    /* Enable pull-up for PX0 (default state) */
    &periph0_siga_px0_default {
        bias-pull-up;
    };

    /* Enable pull-up for PZ1 (default state) */
    &periph0_sigc_pz1_default {
        bias-pull-up;
    };

.. note::

    不推荐在预定义节点中添加引脚配置默认值。一般来说，引脚配置取决于板卡设计或外设的工作条件，因此该决策应由板卡做出。例如，默认启用上拉可能并不总是期望的，因为板卡上可能已焊接了上拉电阻，或者其取值取决于总线工作速度。默认值的另一个缺点是用户可能并不知晓它们的存在，例如：

    .. code-block:: devicetree

        /* not evident that "periph0_siga_px0_default" also implies "bias-pull-up" */
        /omit-if-no-ref/ periph0_siga_px0_default: periph0_siga_px0_default {
            pinmux = <VNDSOC_PIN(X, 0, MUX0)>;
            bias-pull-up;
        };

实现指南
*************************

引脚控制驱动程序
==================

引脚控制驱动程序需要实现单个函数：:c:func:`pinctrl_configure_pins`。该函数接收一组需要应用的引脚配置数组。此外，如果设置了 :kconfig:option:`CONFIG_PINCTRL_STORE_REG`，它还会接收给定引脚关联的设备寄存器地址。某些驱动程序可能需要此信息来执行设备特定的操作。

引脚配置存储在一个不透明类型中，该类型因厂商/SoC 而异：``pinctrl_soc_pin_t``。该类型需要在名为 ``pinctrl_soc.h`` 且位于 Zephyr 头文件搜索路径中的头文件里定义。它可以是一个简单的整数值，也可以是带多个字段的结构体。``pinctrl_soc.h`` 还需要定义一个名为 ``Z_PINCTRL_STATE_PINS_INIT`` 的宏，它接受两个参数：节点标识符和属性名（``pinctrl-N``）。基于此信息，该宏需要为给定节点的 ``pinctrl-N`` 属性中包含的所有引脚配置定义初始化器。

关于 Devicetree 引脚配置的表示方式，厂商可以自行决定哪种选项更适合其设备。但应遵循以下指南：

- 使用 ``pinctrl-N``（N=0, 1, ...）和 ``pinctrl-names`` 属性定义引脚控制状态。这些属性定义在 :file:`dts/bindings/pinctrl/pinctrl-device.yaml` 中。
- 使用 :file:`dts/bindings/pinctrl/pincfg-node.yaml` 中定义的标准引脚配置属性。

不符合这些指南的表示方式，如果同一厂商在其他操作系统（如 Linux）中已在使用，也可以被接受。

设备驱动程序
=============

本节将给出一些建议，说明设备驱动程序应如何使用 ``pinctrl`` API 成功配置其所需的引脚。

需要在设备对应的绑定（binding）文件中修改其 compatible，使其包含 ``pinctrl-device.yaml``。例如：

.. code-block:: yaml

    include: [base.yaml, pinctrl-device.yaml]

该文件的作用是为设备添加 ``pinctrl-N`` 和 ``pinctrl-names`` 属性。

从设备驱动程序的角度看，要使用 ``pinctrl`` API 需要执行两个步骤。第一步是定义引脚控制配置，包括所有状态和引脚，应使用 :c:macro:`PINCTRL_DT_DEFINE` 或 :c:macro:`PINCTRL_DT_INST_DEFINE` 宏来完成。第二步是保存对设备实例 :c:struct:`pinctrl_dev_config` 的引用，因为之后使用 API 时需要它。这可以通过 :c:macro:`PINCTRL_DT_DEV_CONFIG_GET` 和 :c:macro:`PINCTRL_DT_INST_DEV_CONFIG_GET` 宏实现。

值得一提的是，设备与其关联的引脚控制配置之间唯一的关联基于变量命名约定。:c:struct:`pinctrl_dev_config` 实例的命名方式使得之后可以根据设备的 Devicetree 节点标识符获取其引用。这可以最小化 ROM 占用，因为只有需要引脚控制的设备才会拥有一个引脚控制配置的引用。

驱动程序定义好引脚控制配置并保留其引用后，即可使用 API。应用状态最常见的方式是使用 :c:func:`pinctrl_apply_state`。也可以使用较低层的函数 :c:func:`pinctrl_apply_state_direct` 跳过状态查找（前提是状态已提前缓存，例如在初始化时）。由于状态查找耗时预计很短，推荐使用 :c:func:`pinctrl_apply_state`。

下面示例包含一个使用 ``pinctrl`` API 的完整设备驱动程序示例。

.. code-block:: c

    /* A driver for the "mydev" compatible device */
    #define DT_DRV_COMPAT mydev

    ...
    #include <zephyr/drivers/pinctrl.h>
    ...

    struct mydev_config {
        ...
        /* Reference to mydev pinctrl configuration */
        const struct pinctrl_dev_config *pcfg;
        ...
    };

    ...

    static int mydev_init(const struct device *dev)
    {
        const struct mydev_config *config = dev->config;
        int ret;
        ...
        /* Select "default" state at initialization time */
        ret = pinctrl_apply_state(config->pcfg, PINCTRL_STATE_DEFAULT);
        if (ret < 0) {
            return ret;
        }
        ...
    }

    #define MYDEV_DEFINE(i)                                                    \
        /* Define all pinctrl configuration for instance "i" */                \
        PINCTRL_DT_INST_DEFINE(i);                                             \
        ...                                                                    \
        static const struct mydev_config mydev_config_##i = {                  \
            ...                                                                \
            /* Keep a ref. to the pinctrl configuration for instance "i" */    \
            .pcfg = PINCTRL_DT_INST_DEV_CONFIG_GET(i),                         \
            ...                                                                \
        };                                                                     \
        ...                                                                    \
                                                                               \
        DEVICE_DT_INST_DEFINE(i, mydev_init, NULL, &mydev_data##i,             \
                              &mydev_config##i, ...);

    DT_INST_FOREACH_STATUS_OKAY(MYDEV_DEFINE)

.. _pinctrl_api:

引脚控制 API
****************

.. doxygengroup:: pinctrl_interface

动态引脚控制
====================

.. doxygengroup:: pinctrl_interface_dynamic

其他参考材料
************************

- `Linux 下的引脚复用与 GPIO 控制入门 <https://elinux.org/images/a/a7/ELC-2021_Introduction_to_pin_muxing_and_GPIO_control_under_Linux.pdf>`_
