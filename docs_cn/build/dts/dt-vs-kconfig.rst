.. _dt_vs_kconfig:

设备树与 Kconfig
#########################

除了设备树，Zephyr 还使用 Kconfig 语言
配置源代码。对于特定用途应使用设备树还是 Kconfig
有时令人困惑。本节应帮助你决定使用哪一个。

简而言之：

* 用设备树描述**硬件**及其**启动时配置**。
  示例包括板上的外设、启动时时钟频率、
  中断线等。
* 用 Kconfig 配置要构建到最终
  镜像中的**软件支持**。示例包括
  是否添加网络支持、应用需要哪些驱动等。

换句话说，设备树主要处理硬件，
Kconfig 处理软件。

例如，考虑一块包含具有 2 个 UART（或串口）
实例的 SoC 的开发板。

* 开发板具有这些 UART **硬件**这一事实
  用设备树中的两个 UART
  节点描述。它们提供 UART 类型（通过 ``compatible``
  属性）和某些设置（如硬件
  外设寄存器在内存中的地址范围（通过 ``reg`` 属性））。
* 此外，UART **启动时配置**也
  用设备树描述。这可能包括
  RX 中断线优先级和 UART 波特率等配置。
  这些可能在运行时可修改，
  但其启动时配置在设备树中描述。
* 从应用代码看，两个 UART 可互换，
  使用其中一个或另一个没有影响，
  这只是板级设计问题。它是纯
  **硬件配置**，应该用设备树完成。
* 是否在构建中包含 UART 的**软件支持**
  通过 Kconfig 控制。不需要使用 UART 的应用
  可以用 Kconfig 从构建中移除驱动源代码，
  即使开发板的设备树仍包含 UART 节点。

再举一个例子，考虑一个具有 2.4GHz 多协议无线电的设备，
同时支持 Bluetooth Low Energy 和 802.15.4 无线技术。

* 设备树应用于描述无线电**硬件**的存在、
  其兼容的驱动等。
* 无线电的**启动时配置**（如 dBm 为单位的 TX 功率）
  也应使用设备树指定。
* 在应用上，使用其中一个或另一个协议
  不会启用相同的代码，但会使用相同的硬件。
  这与**软件
  配置**相关。
* Kconfig 应确定无线电应构建哪些**软件功能**，
  例如选择 BLE 或 802.15.4 协议栈。

再举一个例子，先前用于启用特定
驱动实例（该驱动本身由 Kconfig 启用）的 Kconfig 选项
已被移除。设备使用设备树的
:ref:`status <dt-important-props>` 关键字在对应硬件
实例上单独选择。

这些规则存在**例外**：

* 由于 Kconfig 无法灵活控制某些实例特定的驱动
  配置参数（如内部缓冲区大小），
  这些选项可以在设备树中定义。但是，
  为明确它们是
  特定于 Zephyr 驱动而非硬件描述或配置，
  这些属性应以 ``zephyr,`` 为前缀，
  例如通用以太网设备树
  属性中的 ``zephyr,random-mac-address``。
* 设备树的 ``chosen`` 关键字，
  允许用户选择特定
  硬件设备实例用于特定用途。一个
  示例是选择特定 UART 用作系统控制台。

.. _auto-dts-kconfig:

从设备树自动生成 Kconfig 符号
*****************************************

在设备树处理步骤中，CMake 运行
:zephyr_file:`scripts/dts/gen_driver_kconfig_dts.py`，
它扫描所有
:ref:`DTS 根 <dts_root>` 目录（包括 :zephyr_file:`dts/bindings`）
并将 ``Kconfig.dts`` 写入构建的 ``KCONFIG_BINARY_DIR``（例如
:ref:`sysbuild` 情况下的 ``<build>/zephyr`` 或 ``<build>/<image>/zephyr``）。
对于绑定中出现的每个 ``compatible = "vendor,chip"``，
生成的文件包含：

.. code-block:: kconfig

   DT_COMPAT_VENDOR_CHIP := vendor,chip

   config DT_HAS_VENDOR_CHIP_ENABLED
           def_bool $(dt_compat_enabled,$(DT_COMPAT_VENDOR_CHIP))

赋值使字面 ``compatible`` 字符串对
:ref:`kconfig-functions` 中描述的预处理器函数可用，
以便 Kconfig 文件可以调用 ``$(dt_compat_on_bus,$(DT_COMPAT_<compatible>),i2c)`` 之类的
辅助函数。创建符号名时
``-``、``,`` 和 ``@`` 等字符被转换为下划线。

隐藏布尔符号在
Kconfig 运行后变为 ``CONFIG_DT_HAS_<compatible>_ENABLED``。
其值跟踪当前设备树是否包含至少
一个具有该 ``compatible`` 且 :ref:`status <dt-important-props>` 为
``okay`` 的节点。用于启用驱动的符号几乎肯定应为 ``default y``
并具有 ``depends on CONFIG_DT_HAS_<compatible>_ENABLED``，例如：

.. code-block:: kconfig

   config SENSOR_VENDOR_CHIP
           bool "Vendor Chip sensor"
           default y
           depends on DT_HAS_VENDOR_CHIP_ENABLED

由于这些符号是自动生成的，
添加具有 ``compatible`` 属性的新绑定
就足以使对应的
``DT_HAS_<compatible>_ENABLED`` 和 ``DT_COMPAT_<compatible>`` 结构
对 Kconfig 可用。
