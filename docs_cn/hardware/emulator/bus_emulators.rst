.. _bus_emul:

外部总线及总线连接外设的模拟器
####################################################

概述
========

Zephyr 支持一个简单的模拟器框架，用于在不依赖真实硬件的情况下测试外部外设驱动。

模拟器用于模拟外部硬件设备，以支持各种子系统的测试。例如，可以为 I2C 罗盘（compass）编写一个模拟器，
使其出现在 I2C 总线上，并能像真实硬件设备一样被使用。

模拟器通常会实现一些专门用于测试的特殊功能。例如，罗盘模拟器可能支持在 I2C 总线速度过高时返回虚假数据，
或者在校准尚未完成时返回无效的测量值。这使得可以测试高层代码能否正确处理这些情况。
如果模拟了所有失败条件，测试覆盖率甚至可以接近 100%。

概念
=======

下面的图表顶部显示的是应用代码/高层测试。这正是我们最终想要运行的应用。

.. figure:: img/arch.svg
   :align: center
   :alt: 模拟器架构，显示测试、模拟器和驱动

在应用之下是外设驱动，例如 AT24 EEPROM 驱动。我们可以使用通过总线控制器模拟器连接的外设模拟器来测试外设驱动：
总线控制器模拟器将例如来自 AT24 驱动（外设驱动）的 I2C 流量传递到 AT24 仿真器（即外设模拟器）。

另外，我们可以使用 API 测试在真实硬件上测试 STM32 和 NXP 的 I2C 驱动。
这些测试需要总线上连接某种外设设备，但有了它，我们就可以验证驱动的大部分功能。

将两者结合起来，我们就可以完全在 native_sim 上测试应用和外设代码。
由于我们知道真实硬件上的 I2C 驱动工作正常，因此可以预期应用和外设驱动在真实硬件上也能正常工作。

使用上面的框架，我们可以借助所有非芯片驱动的模拟器，在 native_sim 上测试整个应用（例如嵌入式控制器）。

采用这种方法，我们可以：

* 为每个驱动编写单独的测试（绿色），覆盖所有失败模式、错误条件等。

* 确保驱动的测试覆盖率达到 100%（绿色）。

* 为驱动的组合编写测试，例如通过 I2C 总线通信的 I2C GPIO 扩展器驱动所提供的 GPIO，
  且这些 GPIO 控制着充电器。所有这些都可以在模拟环境中或真实硬件上工作。

* 编写一个复杂的应用，将所有这些部分组合起来并在 native_sim 上运行。
  我们可以在主机上开发，使用源代码级调试等。

* 通过添加 Kconfig 和设备树（devicetree）片段，
  将应用移植到任何提供所需特性（例如 I2C、足够多的 GPIO）的板卡上。

创建设备驱动模拟器
=================================

模拟器子系统以 :ref:`device_model_api` 为模型。你使用 :c:func:`EMUL_DT_DEFINE()` 或
:c:func:`EMUL_DT_INST_DEFINE()` API 之一来创建模拟器实例。

外设设备的模拟器复用与真实设备驱动相同的设备树节点。
这意味着你的模拟器使用与真实驱动相同的 ``compat`` 值来定义 ``DT_DRV_COMPAT``。

.. code-block:: C

  /* From drivers/sensor/bm160/bm160.c */
  #define DT_DRV_COMPAT bosch_bmi160

  /* From drivers/sensor/bmi160/emul_bmi160.c */
  #define DT_DRV_COMPAT bosch_bmi160

``EMUL_DT_DEFINE()`` 函数接受两种 API 类型：

  #. ``bus_api`` —— 指向模拟器所连接的上游总线的 API。``bus_api`` 参数是必需的。
     支持的模拟总线类型包括 I2C、SPI、eSPI 和 MSPI。
  #. ``_backend_api`` —— 指向模拟器所对应的设备类特定的后端（backend）API。``_backend_api`` 参数是可选的。

下面的图表以 BC1.2 充电检测器驱动作为模型设备类，演示了 ``bus_api`` 和 ``_backend_api`` 的逻辑组织。

.. figure:: img/device_class_emulator.svg
   :align: center
   :alt: 设备类示例，演示 BC1.2 充电检测器。

真实代码以绿色显示，模拟器代码以黄色显示。

``bus_api`` 将 BC1.2 模拟器连接到 ``native_sim`` 的 I2C 控制器。真实的 BC1.2 驱动保持不变，
其操作方式与系统中存在物理 I2C 控制器时完全相同。``native_sim`` 的 I2C 控制器使用 ``bus_api``
向模拟器发起寄存器的读取和写入。

``_backend_api`` 提供了一种机制，让测试能够带外（out of band）操纵模拟器。每个设备类定义自己的 API 函数。
后端 API 函数专注于高层行为，不为特定的模拟器提供挂钩（hooks）。

以 BC1.2 充电检测器为例，后端 API 提供了用于模拟将充电器连接和断开到被模拟的 BC1.2 设备的函数。
每个模拟器负责更新正确的厂商特定寄存器，并可能需要发出中断。

示例测试流程：

  #. 测试使用 Zephyr BC1.2 驱动 API 注册 BC1.2 检测回调。
  #. 测试使用 BC1.2 模拟器后端连接充电器。
  #. 测试验证 BC1.2 检测回调以正确的充电器类型被调用。
  #. 测试使用 BC1.2 模拟器后端断开充电器。

在这种架构下，同一测试可以用于同一驱动类中所有受支持的驱动。

可用的模拟器
===================

Zephyr 包含以下模拟器：

* I2C 模拟器驱动，允许驱动连接到模拟器，从而无需访问真实硬件即可执行测试。

* SPI 模拟器驱动，对 SPI 起同样的作用。

* eSPI 模拟器驱动，对 eSPI 起同样的作用。该模拟器正在开发中，以支持更多功能。

* MSPI 模拟器驱动，允许驱动连接到模拟器，从而无需访问真实硬件即可执行测试。

I2C 模拟特性
----------------------

在 I2C 模拟总线的绑定（binding）中，有一个用于基于地址转发的自定义属性。给定以下设备树节点：

.. code-block:: devicetree

   i2c0: i2c@100 {
     status = "okay";
     compatible = "zephyr,i2c-emul-controller";
     clock-frequency = <I2C_BITRATE_STANDARD>;
     #address-cells = <1>;
     #size-cells = <0>;
     #forward-cells = <1>;
     reg = <0x100 4>;
     forwards = <&i2c1 0x20>;
   };

最后一个属性 ``forwards`` 表示：发往地址 ``0x20`` 的任何读/写请求都应被转发到 ``i2c1`` 的相同地址。
这使我们在同一镜像上同时测试通信的控制器端和目标端成为可能。

.. note::
   ``#forward-cells`` 属性应始终为 1。``forwards`` 属性中的每个条目由 phandle 后跟地址组成。
   在上例中，``<&i2c1 0x20>`` 将发往 ``i2c0`` 端口 ``0x20`` 的所有读/写操作转发到 ``i2c1`` 的同一端口。
   由于模拟控制器不使用额外的单元（cells），单元数量应保持为 1。

示例
=======

以下是 Zephyr 中的一些示例：

#. 通过 I2C 和 SPI 连接到模拟器的 Bosch BMI160 传感器驱动：

   .. zephyr-app-commands::
      :zephyr-app: tests/drivers/sensor/bmi160
      :board: native_sim
      :goals: build

#. 同一测试可以构建第二个 EEPROM，它是一个通过 I2C 连接到模拟器的 Atmel AT24 EEPROM 驱动：

   .. zephyr-app-commands::
      :zephyr-app: tests/drivers/eeprom/api
      :board: native_sim
      :goals: build
      :gen-args: -DDTC_OVERLAY_FILE=at2x_emul.overlay -DEXTRA_CONF_FILE=at2x_emul.conf

API 参考
=============

.. doxygengroup:: io_emulators
