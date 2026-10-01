.. _shields:

Shield
#######

Shield（又称"add-on"或"daughter board"）附加到 board 上以扩展其功能和服务，
便于模块化的原型开发。
在 Zephyr 中，shield 功能提供 Zephyr 格式的 shield 描述，
便于与应用程序兼容。

Shield 激活
*****************

通过向 west 命令添加匹配的 ``--shield`` 参数激活一个或多个 shield 的支持：

  .. zephyr-app-commands::
     :app: your_app
     :board: your_board
     :shield: x_nucleo_idb05a1,x_nucleo_iks01a1
     :goals: build


或者，可以在项目的 CMakeLists.txt 中默认设置：

.. code-block:: cmake

	set(SHIELD x_nucleo_iks01a1)

.. _shield-interfaces:

Shield 接口
*****************

Shield 由两个关键特征定义：

#. **物理连接器** - 机械接口
#. **电气信号** - 每个引脚实际做什么

Shield 和 board 之间的连接通过 Devicetree 文件完成：

- Board 侧：board 的 devicetree 文件用 :ref:`GPIO nexus 节点 <gpio-nexus-node>`
  将连接器引脚映射到微控制器的实际 GPIO 引脚。
  它还定义通过连接器暴露的总线的标签
  （如 ``arduino_i2c``、``arduino_spi``、``arduino_uart``）。

- Shield 侧：shield 的 .overlay 文件引用这些相同的标签
  来描述其组件如何连接到 board。

在构建时，board 的 devicetree 和 shield 的 overlay 组合在一起
以创建硬件设置的完整图景。

例如，假设你有一个带 Arduino 连接器但没有内置加速度计的 board。
你可以用 Arduino shield 添加一个：

#. Board 的 Devicetree 定义 ``arduino_i2c`` 标签：
   它是 Arduino 连接器上可用的 I2C 总线

#. 加速度计 shield 的 overlay 文件也引用 ``arduino_i2c``
   以表示它使用相同的 I2C 总线。
   如果需要从连接器使用 GPIO 引脚，
   它引用由 board 的 Devicetree 定义的 GPIO nexus 节点
   （如 ``arduino_header``）。

然后当你用此 shield 为此 board 构建时，Zephyr 自动"将它们连接起来"。

.. note::

   某些 boards 和 shields 可能仅支持 shield 硬件接口功能集的有限子集。
   参见其文档获取更多细节。


Arduino MKR
-----------

这是 Arduino MKR boards 的外形规格。

.. figure:: ../../../boards/arduino/mkrzero/doc/img/arduino_mkrzero.jpg
   :align: center
   :width: 200px
   :alt: Arduino MKR Zero

   Arduino MKR Zero，一个带 Arduino MKR shield 接口的 board 示例

相关 devicetree 节点标签：

- ``arduino_mkr_header`` 参见 :dtcompatible:`arduino-mkr-header`
  了解 devicetree 文件中使用的 GPIO 引脚定义和 includes 的详细信息。
- ``arduino_mkr_i2c``
- ``arduino_mkr_spi``
- ``arduino_mkr_serial``


Arduino Nano
------------

这是 Arduino Nano boards 的外形规格。

.. figure:: ../../../boards/arduino/nano_33_iot/doc/img/nano_33_iot.jpg
   :align: center
   :width: 300px
   :alt: Arduino Nano 33 IOT

   Arduino Nano 33 IOT，一个带 Arduino Nano shield 接口的 board 示例

相关 devicetree 节点标签：

- ``arduino_nano_header`` 参见 :dtcompatible:`arduino-nano-header`
  了解 devicetree 文件中使用的 GPIO 引脚定义和 includes 的详细信息。
- ``arduino_nano_i2c``
- ``arduino_nano_spi``
- ``arduino_nano_serial``


Arduino Uno R3
--------------

这是 Arduino Uno R3 board 的外形规格。

.. figure:: ../../../boards/shields/mcp2515/doc/keyestudio_can_bus_ks0411.jpg
   :align: center
   :width: 300px
   :alt: Keyestudio CAN-BUS Shield (KS0411)

   Keyestudio CAN-BUS，一个 Arduino shield 示例（Credit: Keyestudio）

相关 devicetree 节点标签：

- ``arduino_header`` 参见 :dtcompatible:`arduino-header-r3`
  了解 devicetree 文件中使用的 GPIO 引脚定义和 includes 的详细信息。
- ``arduino_adc`` 参见 :dtcompatible:`arduino,uno-adc`
- ``arduino_pwm`` 参见 :dtcompatible:`arduino-header-pwm`
- ``arduino_serial``
- ``arduino_i2c``
- ``arduino_spi``

技术细节参见 `Arduino Uno R3 pinout`_。


Camera 和显示连接器
-----------------------------

这些描述与摄像头和显示器的连接（严格来说不是 shields）。

- :dtcompatible:`arducam,dvp-20pin-connector`
- :dtcompatible:`nxp,cam-44pins-connector`
- :dtcompatible:`nxp,parallel-lcd-connector`
- :dtcompatible:`raspberrypi,csi-connector`
- :dtcompatible:`st,dsi-lcd-qsh-030-connector`
- :dtcompatible:`st,dvp-cam-zif-30-connector`
- :dtcompatible:`weact,dcmi-camera-connector`


ESP-01
------

这是用于 ESP-01 Wi-Fi 模块的 8 针 header。

相关 devicetree 节点标签：

- ``esp_01_header`` 参见 :dtcompatible:`esp-01-header`
  了解 devicetree 文件中使用的 GPIO 引脚定义和 includes 的详细信息。
- ``esp_01_serial``


Feather
-------

这是 Adafruit Feather 系列 boards 的外形规格。
用于 Feather boards 的 shields 称为 Featherwings。

.. figure:: ../../../boards/shields/adafruit_adalogger_featherwing/doc/adafruit_adalogger_featherwing.webp
   :align: center
   :width: 300px
   :alt: Adafruit Adalogger Featherwing Shield

   Adafruit Adalogger，一个 Featherwing 示例（Credit: Adafruit）

相关 devicetree 节点标签：

- ``feather_header`` 参见 :dtcompatible:`adafruit-feather-header` 了解 GPIO 引脚定义。
- ``feather_adc``
- ``feather_i2c``
- ``feather_serial``
- ``feather_spi`

Microbit
--------

这是用于 Microbit boards 的边缘连接器。

.. figure::  ../../../boards/bbc/microbit_v2/doc/img/bbc_microbit2.jpg
   :align: center
   :width: 500px
   :alt: Microbit V2 board

   Microbit V2 board 使用 Microbit shield 接口

参见 :dtcompatible:`microbit,edge-connector` 了解 GPIO 引脚定义和技术要求链接。


mikroBUS™
---------

这是由 Mikroe 开发的 add-on boards 接口标准。

.. figure:: ../../../boards/shields/mikroe_3d_hall_3_click/doc/images/mikroe_3d_hall_3_click.webp
   :align: center
   :alt: 3D Hall 3 Click
   :height: 300px

   3D Hall 3 Click，一个 mikroBUS™ shield 示例

相关 devicetree 节点标签：

- ``mikrobus_header`` 参见 :dtcompatible:`mikro-bus`
  了解 GPIO 引脚定义和技术规格链接。
- ``mikrobus_adc``
- ``mikrobus_i2c``
- ``mikrobus_pwm``
- ``mikrobus_spi``
- ``mikrobus_serial``

注意，带多个 mikroBUS™ 连接器的 boards 可能定义例如 ``mikrobus_2_spi``。


Pico
----

这是 Raspberry Pi Pico boards 的外形规格。

.. figure::  ../../../boards/shields/waveshare_ups/doc/waveshare_pico_ups_b.jpg
   :align: center
   :width: 300px
   :alt: Waveshare Pico UPS-B shield

   Waveshare Pico UPS-B，一个 Pico shield 示例

相关 devicetree 节点标签：

- ``pico_header`` 参见 :dtcompatible:`raspberrypi,pico-header` 了解 GPIO 引脚定义。
- ``pico_i2c`` 一个引用与节点标签 ``pico_i2c0`` 或 ``pico_i2c1``
  相同节点的节点标签。
  它引用应优先或默认使用的节点。
- ``pico_i2c0``
- ``pico_i2c1``
- ``pico_serial``
- ``pico_spi``


ST Morpho
---------

ST Microelectronics 的开发 boards 通常使用 ST Morpho shield 接口。

.. figure:: ../../../boards/shields/x_nucleo_gfx01m2/doc/x_nucleo_gfx01m2.webp
   :align: center
   :width: 300px
   :alt: X-NUCLEO-GFX01M2

   X-NUCLEO-GFX01M2，一个 ST Morpho shield 示例

相关 devicetree 节点标签：

- ``st_morpho_header``  参见 :dtcompatible:`st-morpho-header`
  了解 devicetree 文件中使用的 GPIO 引脚定义和 includes 的详细信息。
- ``st_morpho_lcd_spi``
- ``st_morpho_flash_spi`

ST Zio
------

ST Microelectronics 的 STM32 Nucleo-144 开发 boards
暴露 ST Zio 连接器，
它是 Arduino Uno V3 连接器的扩展，
通过四个 headers（CN7、CN8、CN9 和 CN10）
访问更多 STM32 I/O。

相关 devicetree 节点标签：

- ``st_zio_header``  参见 :dtcompatible:`st-zio-header`
  了解 devicetree 文件中使用的 GPIO 引脚定义和 includes 的详细信息。


STMod+
------

这是在某些 STMicroelectronics Discovery 和 Evaluation boards
上找到的 20 针扩展连接器。

相关 devicetree 节点标签：

- ``stmod_plus_connector`` 参见 :dtcompatible:`st,stmod-plus-connector`
  了解 devicetree 文件中使用的 GPIO 引脚定义和 includes 的详细信息。
- ``stmod_adc``
- ``stmod_i2c``
- ``stmod_pwm``
- ``stmod_serial``
- ``stmod_spi``

当外设连接到 STMod+ 连接器并在 board devicetree 中启用时，
boards 可能暴露额外接口标签。


WisBlock
--------

这是由 RAKwireless 开发的 add-on boards 模块化接口标准。
它定义 Core、Sensor、I/O 和 Power Slots，
每个通过 24 针或 40 针 WisConnector 接受匹配类的模块。

.. figure:: ../../../boards/shields/rakwireless_rak19007/doc/img/rakwireless_rak19007.webp
   :align: center
   :alt: RAK19007 Base Board
   :width: 300px

   RAK19007，一个 WisBlock Base Board 示例（Credit: RAKwireless）

相关 devicetree 节点标签：

- ``wisblock_io`` 参见 :dtcompatible:`wisblock-io-slot` 了解 GPIO 引脚定义。
- ``wisblock_sensor_a`` 参见 :dtcompatible:`wisblock-sensor-slot` 了解 GPIO 引脚定义。
- ``wisblock_adc``
- ``wisblock_pwm``
- ``wisblock_i2c1``
- ``wisblock_i2c2``
- ``wisblock_i2s``
- ``wisblock_pdm``
- ``wisblock_spi``
- ``wisblock_uart0``
- ``wisblock_uart1``

注意，Sensor Slots 按实现的 Slot 标记为 ``wisblock_sensor_a`` 到 ``wisblock_sensor_f``。


Xiao
----

这是 Seeeduino XIAO boards 的外形规格。

.. figure:: ../../../boards/shields/seeed_xiao_expansion_board/doc/img/seeed_xiao_expansion_board.webp
     :align: center
     :width: 300px
     :alt: Seeed Studio XIAO Expansion Board

     Seeed Studio XIAO Expansion Board，一个 Xiao shield 示例（Credit: Seeed Studio）

相关 devicetree 节点标签：

- ``xiao_d`` 参见 :dtcompatible:`seeed,xiao-gpio` 了解 GPIO 引脚定义。
- ``xiao_spi``
- ``xiao_i2c``
- ``xiao_serial``
- ``xiao_adc``
- ``xiao_dac``


zephyr_i2c / Stemma QT / Quiic
------------------------------

这些是四针 I2C 连接器。
SparkFun 称这些连接器为 "Qwiic"，
Adafruit 称它们为 "Stemma QT"。
I2C 连接器有四个引脚；GND、+3.3 伏、I2C 数据线和 I2C 时钟线。
最常见的物理连接器是 1.0 mm 间距 JST-SH。

由于不同的品牌名称，接口标记为 "zephyr_i2c"。

.. figure::  ../../../boards/shields/adafruit_vcnl4040/doc/adafruit_vcnl4040.webp
   :align: center
   :width: 200px
   :alt: Adafruit VCNL4040 Shield

   Adafruit VCNL4040，一个 zephyr_i2c shield 示例（Credit: Adafruit）

参见 :dtcompatible:`stemma-qt-connector` 和 :dtcompatible:`grove-header`
了解描述和更多细节链接。

相关 devicetree 节点标签：

- ``zephyr_i2c``

ST M.2 serial memory 连接器
------------------------------

某些 STMicroelectronics Nucleo-144 开发 boards
暴露 ST 特定的 M.2 serial memory 连接器，
用于通过 XSPI 与外部串行存储器接口，
连同 I2C 和连接器 GPIO 等辅助信号。

.. figure:: ../../../boards/shields/st_b_m2mem_pack1/doc/b_m2mem_pack1.webp
   :align: center
   :width: 300px
   :alt: B-M2MEM-PACK1

   B-M2MEM-PACK1，一个 ST M.2 memory shield 示例。

相关 devicetree 节点标签：

- ``m2mem_connector``  参见 :dtcompatible:`st,m2-memory-connector`
  了解 devicetree 文件中使用的 GPIO 引脚定义和 includes 的详细信息。
- ``m2mem_i2c``
- ``m2mem_xspi``

.. _shield_porting_guide:

Shield 移植和配置
********************************

Shield 配置文件在 :zephyr_file:`boards/shields` 下的 board 目录中可用：

.. code-block:: none

   boards/shields/<shield>
   ├── shield.yml
   ├── <shield>.overlay
   ├── Kconfig.shield
   ├── Kconfig.defconfig
   └── pre_dt_shield.cmake

这些文件提供 shield 配置如下：

* **shield.yml**：此文件以 YAML 格式提供关于 shield 的元数据。
  它必须包含以下字段：

  * ``name``：在 Kconfig 和构建系统中使用的 shield 名称（必需）
  * ``full_name``：shield 的完整商业名称（必需）
  * ``vendor``：shield 的制造商/vendor（必需）
  * ``supported_features``：shield 支持的硬件功能列表（可选）。
    为了帮助用户识别 shield 支持的功能而无需深入其 overlay 文件，
    ``supported_features`` 字段可用于列出 shield 支持的功能类型。
    值应与 :zephyr_file:`dts/bindings/binding-types.txt` 文件中定义的值相同。

  示例：

  .. code-block:: yaml

     name: foo_shield
     full_name: Foo Shield for Arduino
     vendor: acme
     supported_features:
       - display
       - input

* **<shield>.overlay**：此文件提供以 devicetree 格式的 shield 描述，
  在编译前与 board 的 :ref:`devicetree <dt-guide>` 合并。

* **Kconfig.shield**：此文件定义用于默认 shield 配置的 shield Kconfig 符号。
  为便于与应用程序一起使用，
  此处的默认 shield 配置应与 :ref:`default_board_configuration` 中的一致。

* **Kconfig.defconfig**：此文件定义默认 shield 配置。
  它旨在与 :ref:`default_board_configuration` 一致。
  因此，shield 配置应考虑功能激活是应用程序的责任。

* **pre_dt_shield.cmake**：此可选文件可用于向 devicetree 编译器 ``dtc``
  传递额外参数。

此外，为避免与可能在 board 级别定义的设备的名称冲突，
建议特别是对于 shields devicetree 描述，
提供 ``<device>_<shield>`` 形式的设备 nodelabel，例如：

.. code-block:: devicetree

        sdhc_myshield: sdhc@1 {
                reg = <1>;
                ...
        };

添加源代码
******************

可以将源代码添加到 shields，
作为满足特定于 shield 的配置要求
（如：初始化例程、时序约束等）的方式，
以启用其与不同 Zephyr 组件的正确运行。

.. note::

   Shields 中的源代码不得用于上述目的之外的用途。
   Shield（和/或 targets）之间可复用的通用功能不应在此捕获。

要有效整合源代码：添加 :file:`CMakeLists.txt` 文件
以及相应的源文件（在 CMake 中引用，
类似 Zephyr 的其他区域，如：boards）。

Board 兼容性
*******************

硬件 shield-to-board 兼容性取决于
使用流行 boards 上众所周知的连接器
（如 Arduino 和 96boards）。
对于软件兼容性，boards 还必须提供与其支持的连接器匹配的配置。

这应在两个不同级别完成：

* Pinmux：连接器引脚应正确配置以匹配 shield 引脚

* Devicetree：board :ref:`devicetree <dt-guide>` 文件
  :file:`BOARD.dts` 应为每个连接器接口定义替代 nodelabel。
  例如，对于 Arduino I2C：

.. code-block:: devicetree

        arduino_i2c: &i2c1 {};

Board 特定 shield 配置
-----------------------------------

如果需要修改以使 shield 适应特定 board 或 board revision，
可以通过向 shield 添加 board 或 board revision 覆盖文件
来覆盖特定 board 的 shield 描述，如下：

.. code-block:: none

   boards/shields/<shield>
   └── boards
       ├── <board>_<revision>.overlay
       ├── <board>.overlay
       ├── <board>.defconfig
       ├── <board>_<revision>.conf
       └── <board>.conf


Shield variants
***************

某些 shields 可能支持多个 variants 或 revisions。
在这种情况下，可以提供 shields 描述的多个版本：

.. code-block:: none

   boards/shields/<shield>
   ├── <shield_v1>.overlay
   ├── <shield_v1>.defconfig
   ├── <shield_v2>.overlay
   └── <shield_v2>.defconfig

在这种情况下，可以使用 shield 特定的 revision 名称：

  .. zephyr-app-commands::
     :app: your_app
     :shield: shield_v2
     :goals: build

你还可以为特定 shield revision 提供 board 特定配置：

.. code-block:: none

   boards/shields/<shield>
   ├── <shield_v1>.overlay
   ├── <shield_v1>.defconfig
   ├── <shield_v2>.overlay
   ├── <shield_v2>.defconfig
   └── boards
       └── <shield_v2>
           ├── <board>.overlay
           └── <board>.defconfig

.. _gpio-nexus-node:

GPIO nexus 节点
****************

Shield 外设访问的 GPIO 必须用 shield GPIO 抽象标识，
例如来自 ``arduino-header-r3`` compatible。
提供 header 的 boards 必须将 header 引脚映射到 SoC 特定引脚。
这通过在 board devicetree 文件中包含如下 `nexus 节点`_ 实现：

.. _nexus node:
    https://github.com/devicetree-org/devicetree-specification/blob/4b1dac80eaca45b4babf5299452a951008a5d864/source/devicetree-basics.rst#nexus-nodes-and-specifier-mapping

.. code-block:: devicetree

    arduino_header: connector {
            compatible = "arduino-header-r3";
            #gpio-cells = <2>;
            gpio-map-mask = <0xffffffff 0xffffffc0>;
            gpio-map-pass-thru = <0 0x3f>;
            gpio-map = <0 0 &gpioa 0 0>,    /* A0 */
                       <1 0 &gpioa 1 0>,    /* A1 */
                       <2 0 &gpioa 4 0>,    /* A2 */
                       <3 0 &gpiob 0 0>,    /* A3 */
                       <4 0 &gpioc 1 0>,    /* A4 */
                       <5 0 &gpioc 0 0>,    /* A5 */
                       <6 0 &gpioa 3 0>,    /* D0 */
                       <7 0 &gpioa 2 0>,    /* D1 */
                       <8 0 &gpioa 10 0>,   /* D2 */
                       <9 0 &gpiob 3 0>,    /* D3 */
                       <10 0 &gpiob 5 0>,   /* D4 */
                       <11 0 &gpiob 4 0>,   /* D5 */
                       <12 0 &gpiob 10 0>,  /* D6 */
                       <13 0 &gpioa 8 0>,   /* D7 */
                       <14 0 &gpioa 9 0>,   /* D8 */
                       <15 0 &gpioc 7 0>,   /* D9 */
                       <16 0 &gpiob 6 0>,   /* D10 */
                       <17 0 &gpioa 7 0>,   /* D11 */
                       <18 0 &gpioa 6 0>,   /* D12 */
                       <19 0 &gpioa 5 0>,   /* D13 */
                       <20 0 &gpiob 9 0>,   /* D14 */
                       <21 0 &gpiob 8 0>;   /* D15 */
    };

这指定如何将 ``<&arduino_header 11 0>`` 等 Arduino 引脚引用
转换为 ``<&gpiob 4 0>`` 等 SoC gpio 引脚引用。

在 Zephyr 中 GPIO specifiers 通常有两个参数
（由 ``#gpio-cells = <2>`` 指示）：
引脚编号和一组 flags。
Flags 的低 6 位对应可在 devicetree 中配置的功能。
在某些情况下，需要使用非零 flag 值来告诉 driver 特定引脚如何行为，
如：

.. code-block:: devicetree

    drdy-gpios = <&arduino_header 11 GPIO_ACTIVE_LOW>;

预处理后变为 ``<&arduino_header 11 1>``。
通常，此类 flag 的存在会导致 map 查找失败，
因为没有非零 flags 值的 map 条目。
``gpio-map-mask`` 属性指定，对于查找，
引脚的所有位和 flags 的低 6 位以外的所有位
用于标识 specifier。
然后 ``gpio-map-pass-thru`` 指定 flags 的低 6 位被复制，
因此 SoC GPIO 引用变为 ``<&gpiob 4 1>``，如预期。

参见 `nexus 节点`_ 了解此功能的更多信息。


.. _Arduino Uno R3 pinout:
  https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf
