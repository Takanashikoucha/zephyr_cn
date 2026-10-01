.. _mspi_api:

多比特 SPI 总线
#################

MSPI（多比特 SPI）作为通用 API 提供，用于容纳高级 SPI 外设和设备，这些外设和设备通常需要命令、地址和数据阶段，以及这些阶段中的多条信号线。虽然该 API 支持 :term:`XIP` 和扰码等高级特性，但它也兼容通用 SPI。

.. contents::
    :local:
    :depth: 2

.. _mspi-controller-api:

MSPI 控制器 API
*******************

当存在多比特 SPI 控制器时，可以使用 Zephyr 的 MSPI 控制器 API。例如 Ambiq MSPI、QSPI、OSPI、Flexspi 等。该 API 支持单比特到六比特 SDR/DDR IO，带可变延迟以及 :term:`XIP` 和扰码等高级特性。适用设备包括但不限于高速、高密度闪存/PSRAM 内存设备、显示器和传感器。

MSPI 接口包含 SoC 平台特定的控制器驱动（实现 MSPI API）以及引用这些 API 的设备驱动。控制器驱动和设备驱动之间的关系是多对多，以便在平台之间轻松切换。

以下是设备驱动初始化函数中初始化 MSPI 控制器和 MSPI 总线的一般步骤列表：

#. 初始化 MSPI 控制器驱动实例的数据结构。通常的设备定义宏如 :c:macro:`DEVICE_DT_INST_DEFINE` 可以使用，初始化函数、配置和数据作为宏的参数提供。

#. 初始化硬件，包括但不限于：

   * 将 :c:struct:`mspi_cfg` 与硬件自身能力进行比对，以防止错误使用。

   * 设置默认引脚复用。

   * 为控制器设置时钟。

   * 开启硬件电源。

   * 使用 :c:struct:`mspi_cfg` 以及可能的更多平台特定设置来配置硬件。

   * 通常，:c:struct:`mspi_cfg` 从设备树填充并包含静态的启动时参数。然而，如需要，可以使用 :c:func:`mspi_config` 在运行时用新参数重新初始化硬件。

   * 如适用，释放任何锁。

#. 执行设备驱动初始化。通常，:c:macro:`DEVICE_DT_INST_DEFINE` 可以使用。在设备驱动初始化函数内，执行以下必需步骤。

   #. 调用 :c:func:`mspi_dev_config`，传入从设备数据手册获取的设备特定硬件设置。

      * :c:struct:`mspi_dev_cfg` 应由设备树填充，辅助宏 :c:macro:`MSPI_DEVICE_CONFIG_DT` 可以使用。

      * 控制器驱动随后应验证 :c:struct:`mspi_dev_cfg` 的成员，以防止错误使用。

      * 控制器驱动应实现互斥锁，以防止意外访问。

      * 控制器驱动还可基于 :c:struct:`mspi_dev_id` 在不同设备之间切换。

   #. 如硬件支持，调用 API 进行额外设置

      * :c:func:`mspi_memmap_config` 用于内存映射访问（例如 :term:`XIP`）

      * :c:func:`mspi_scramble_config` 用于扰码特性

      * :c:func:`mspi_timing_config` 用于平台特定的时序设置。

   #. 如需要，使用 :c:func:`mspi_register_callback` 注册回调。

   #. 释放控制器互斥锁。

收发
==========
收发请求的类型为 :c:struct:`mspi_xfer`，它允许在操作模式由 :c:func:`mspi_dev_config` 确定并配置后，动态更改与传输相关的设置。

该 API 还支持使用 :c:struct:`mspi_xfer_packet` 进行带有不同起始地址和大小的批量传输。然而，是否支持分散 IO 和回调管理取决于控制器实现。如果回调已使用 :c:func:`mspi_register_callback` 注册，控制器可以在每个异步/同步传输完成时，基于 :c:enum:`mspi_bus_event_cb_mask` 确定触发哪个用户回调。或者，即使回调已注册，也可以使用 :c:enum:`MSPI_BUS_NO_CB` 不触发任何回调。如果所实现的驱动支持，该 API 支持 :c:enum:`MSPI_BUS_XFER_COMPLETE_CB` 来指示传输完成，以及 :c:enum:`MSPI_BUS_TIMEOUT_CB` 来指示传输或请求超时。在这种情况下，如果控制器支持硬件命令队列，且分散 IO 和回调管理由驱动实现支持，用户便可充分利用硬件性能。

设备树
===========

以下是在设备树中定义 MSPI 控制器的示例：mspi 控制器的绑定应将 mspi-controller.yaml 作为基础之一引用。

.. code-block:: devicetree

   mspi0: mspi@400 {
           status = "okay";
           compatible = "zephyr,mspi-emul-controller";

           reg = <0x400 0x4>;
           #address-cells = <0x1>;
           #size-cells = <0x0>;

           clock-frequency = <0x17d7840>;
           op-mode = "MSPI_CONTROLLER";
           duplex = "MSPI_HALF_DUPLEX";
           ce-gpios = <&gpio0 0x5 0x1>, <&gpio0 0x12 0x1>;
           dqs-support;

           pinctrl-0 = <&pinmux-mspi0>;
           pinctrl-names = "default";
   };

以下是在设备树中定义 MSPI 设备的示例：mspi 设备的绑定应将 mspi-device.yaml 作为基础之一引用。

.. code-block:: devicetree

   &mspi0 {

           mspi_dev0: mspi_dev0@0 {
                    status = "okay";
                    compatible = "zephyr,mspi-emul-device";

                    reg = <0x0>;
                    size = <0x10000>;

                    mspi-max-frequency = <0x2dc6c00>;
                    mspi-io-mode = "MSPI_IO_MODE_QUAD";
                    mspi-data-rate = "MSPI_DATA_RATE_SINGLE";
                    mspi-hardware-ce-num = <0x0>;
                    read-instruction = <0xb>;
                    write-instruction = <0x2>;
                    instruction-length = "INSTR_1_BYTE";
                    address-length = "ADDR_4_BYTE";
                    rx-dummy = <0x8>;
                    tx-dummy = <0x0>;
                    memmap-config = <0x0 0x0 0x0 0x0>;
                    ce-break-config = <0x0 0x0>;
           };

   };

用户应在 DTS 中指定目标操作参数，如 ``mspi-max-frequency``、``mspi-io-mode`` 和 ``mspi-data-rate``，即使它们可能在运行时更改。这些参数应代表设备在正常操作期间的典型配置。

多外设
================
将 :c:struct:`mspi_dev_id` 定义为从设备树获取的设备索引和 CE GPIO 的集合后，该 API 支持同一控制器实例上的多个设备。控制器驱动实现可能支持也可能不支持设备切换，切换可以由软件或硬件执行。如果切换由软件处理，应在 :c:func:`mspi_dev_config` 调用中执行。

设备驱动应记录设备的当前操作条件，以支持软件控制设备切换，方法是保存并更新 :c:struct:`mspi_dev_cfg` 以及其他相关的 mspi 结构体或私有数据结构。特别是，包含设备身份的 :c:struct:`mspi_dev_id` 需要在每次 API 调用中使用。


配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_MSPI`
* :kconfig:option:`CONFIG_MSPI_ASYNC`
* :kconfig:option:`CONFIG_MSPI_PERIPHERAL`
* :kconfig:option:`CONFIG_MSPI_MEMMAP`
* :kconfig:option:`CONFIG_MSPI_SCRAMBLE`
* :kconfig:option:`CONFIG_MSPI_TIMING`
* :kconfig:option:`CONFIG_MSPI_INIT_PRIORITY`
* :kconfig:option:`CONFIG_MSPI_COMPLETION_TIMEOUT_TOLERANCE`
* :kconfig:option:`CONFIG_MSPI_DMA`

API 参考
*************

.. doxygengroup:: mspi_interface
