.. _dt-bindings-file-syntax:

设备树绑定语法
##########################

本页记录 Zephyr 绑定格式的语法。Zephyr 绑定
文件是 YAML 文件。在介绍页中给出了一个 :ref:`简单示例 <dt-bindings-simple-example>`。

.. contents:: 目录
   :local:
   :depth: 3

顶层键
**************

绑定文件的顶层将键映射到值。顶层键如下所示：

.. code-block:: yaml

   # 当描述文本过长时，可以使用此字段
   # 来提高可读性，例如：
   #
   # title: 绑定设备的硬件型号。
   #
   # description |
   #   一段 20 行的内容。
   #   ...
   title: 长描述的简洁标题 [可选]

   # 对所绑定设备的顶层描述：
   description: |
      这是 Vendomatic 公司的 foo-device。

      跨多行的描述（如此处）是可以的，
      对于复杂的绑定推荐使用。

      格式帮助参见 https://yaml-multiline.info/。

   # 可以使用这种语法从其他绑定引入定义：
   include: other.yaml

   # 用于将节点匹配到此绑定：
   compatible: "manufacturer,foo-device"

   properties:
     # 此绑定的节点需要满足的属性的
     # 要求和描述放在这里。

   child-binding:
     # 可以使用此键来约束
     # 匹配此绑定的节点的子节点。

   # 如果节点描述总线硬件（如 SoC 上的
   # SPI 总线控制器），用 'bus:' 说明是哪种总线，如下所示：
   bus: spi

   # 如果节点是出现在总线上的设备（如外部
   # SPI 存储芯片），用 'on-bus:' 说明总线类型，如下所示。
   # 与 'compatible' 一样，此键也会影响节点
   # 匹配绑定的方式。
   on-bus: spi

   examples:
     # 可以在这里放一个示例节点，展示如何使用该绑定。
     # - |
     #  ...
     # 或
     # - ...

   foo-cells:
     # 'foo' 域的"说明符"单元格名称放在这里；
     # 'foo' 的示例值有 'gpio'、'pwm' 和 'dma'。
     # 更多信息见下文。

以下各节解释这些键。

.. _dt-bindings-title:

标题（Title）
*****

所绑定设备的*可选*简短描述，通常是硬件型号。
其格式通常为"厂商 家族 型号"（Vendor Family Model）。如果使用缩写，
应在括号中写出全称。命名应尽量贴近
厂商数据手册。

标题不应超过 100 个字符。较长的描述应使用
description 字段。标题中不应使用"binding"、"schema"或"driver"
等词，因为一切都是绑定。

.. code-block:: YAML

   title: Acme Foo UART (Universal Asynchronous Receiver/Transmitter)

.. _dt-bindings-description:

描述（Description）
*******************

节点硬件的自由格式描述放在这里。
也可以放数据手册链接或示例节点/属性。

.. _dt-bindings-compatible:

Compatible
**********

此键用于如 :ref:`dt-binding-compat` 所述
将节点匹配到此绑定。在绑定文件中它应如下所示：

.. code-block:: YAML

   # 注意逗号分隔的厂商前缀和设备名
   compatible: "manufacturer,device"

以下设备树节点将匹配上面的绑定：

.. code-block:: devicetree

   device {
   	compatible = "manufacturer,device";
   };

假设没有绑定具有 ``compatible: "manufacturer,device-v2"``，
它也会匹配这个节点：

.. code-block:: devicetree

    device-2 {
        compatible = "manufacturer,device-v2", "manufacturer,device";
    };

每个节点的 ``compatible`` 属性按顺序尝试。
:ref:`绑定 <dt-binding-compat>` 由
(:ref:`compatible <dt-bindings-compatible>`,
:ref:`on-bus <dt-bindings-on-bus>`) 对唯一标识，
其中 :ref:`on-bus <dt-bindings-on-bus>` 可以未指定。
指定的 :ref:`on-bus <dt-bindings-on-bus>` 优先于未指定的。
使用第一个匹配的绑定。

对于以下设备：

.. code-block:: devicetree

   spi-bus {
           device-3 {
                   compatible = "manufacturer,device";
           };
   };

以下两个绑定可以共存，并按以下顺序匹配：

``manufacturer,device-spi.yaml``

.. code-block:: YAML

   compatible: "manufacturer,device"
   on-bus: spi

``manufacturer,device.yaml``

.. code-block:: YAML

   compatible: "manufacturer,device"

以下绑定可以共存但不会匹配。

``manufacturer,device-i2c.yaml``

.. code-block:: YAML

   compatible: "manufacturer,device"
   on-bus: i2c

如果找到多个匹配同一 compatible 的绑定，则报告错误。

``manufacturer`` 前缀标识设备厂商。
接受的厂商前缀列表见
:zephyr_file:`dts/bindings/vendor-prefixes.txt`。``device`` 部分
通常来自数据手册。

有些绑定适用于没有特定厂商的通用设备类别。
在这些情况下，没有厂商前缀。一个示例是
:dtcompatible:`gpio-leds` compatible，
常用于描述连接到 GPIO 的板级 LED。

.. _dt-bindings-properties:

属性（Properties）
**********

``properties:`` 键描述匹配该绑定的节点
所包含的属性。例如，UART 外设的绑定可能如下所示：

.. code-block:: YAML

   compatible: "manufacturer,serial"

   properties:
     reg:
       type: array
       description: UART 外设 MMIO 寄存器空间
       required: true
     current-speed:
       type: int
       description: 当前波特率
       required: true

在这个例子中，compatible 为 ``"manufacturer,serial"`` 的节点必须包含
名为 ``current-speed`` 的属性。该属性的值必须是单个
整数。类似地，节点必须包含 ``reg`` 属性。

构建系统使用绑定为出现在 DTS 文件中的设备树属性
生成 C 宏。关于如何从这些宏在源代码中
读取属性值，更多介绍见 :ref:`dt-from-c`。一般来说，
构建系统只为匹配绑定的 ``properties:``
键中列出的属性生成宏。绑定中未提及的属性
通常被构建系统忽略。

唯一的例外是，构建系统始终为
标准属性（如 :ref:`reg <dt-important-props>`，其含义
由设备树规范定义）生成宏。无论节点
是否有匹配的绑定，这都会发生。

属性条目语法
=====================

``properties:`` 中的属性条目使用这种语法：

.. code-block:: none

   <property name>:
     required: <true | false>
     type: <string | int | boolean | array | uint8-array | string-array |
            phandle | phandles | phandle-array | path | compound>
     deprecated: <true | false>
     default: <default>
     description: <属性描述>
     enum:
       - <item1>
       - <item2>
       ...
       - <itemN>
     const: <string | int | array | uint8-array | string-array>
     min: <int>
     max: <int>
     min-len: <int>
     max-len: <int>
     specifier-space: <space-name>
     dependency-mode: <normal | reverse | ignore | child-ignore>

.. _dt-bindings-example-properties:

属性定义示例
===========================

以下是更多示例。

.. code-block:: YAML

   properties:
       # 描述类似 'current-speed = <115200>;' 的属性。我们假设
       # 它对示例节点是必需的，设置 'required: true'。
       current-speed:
           type: int
           required: true
           description: bar-device 的初始波特率

       # 描述可选属性，如 'keys = "foo", "bar";'
       keys:
           type: string-array
           description: bar-device 的按键

       # 描述可选属性，如 'maximum-speed = "full-speed";'
       # enum 指定字符串属性可取的已知值
       maximum-speed:
           type: string
           description: 配置 USB 控制器以特定速度工作。
           enum:
              - "low-speed"
              - "full-speed"
              - "high-speed"
              - "super-speed"

       # 描述可选属性，如 'resolution = <16>;'
       # enum 指定整数属性可取的已知值
       resolution:
         type: int
         enum:
          - 8
          - 16
          - 24
          - 32

       # 描述必需属性 '#address-cells = <1>'；const
       # 指定该属性的值预期为 1
       "#address-cells":
           type: int
           required: true
           const: 1

       int-with-default:
           type: int
           default: 123
           description: 整数寄存器的值，默认值为上电配置。

       array-with-default:
           type: array
           default: [1, 2, 3] # 等同于 'array-with-default = <1 2 3>'

       string-with-default:
           type: string
           default: "foo"

       string-array-with-default:
           type: string-array
           default: ["foo", "bar"] # 等同于 'string-array-with-default = "foo", "bar"'

       uint8-array-with-default:
           type: uint8-array
           default: [0x12, 0x34] # 等同于 'uint8-array-with-default = [12 34]'

required
========

在属性定义中添加 ``required: true``，
如果节点匹配该绑定但不包含该属性，构建将失败。

默认设置为 ``required: false``；即属性默认是可选的。
因此使用 ``required: false`` 是冗余的，强烈
不推荐。

type
====

属性的类型约束其值。可用
类型如下。关于在 DTS 文件中
编写每种类型值的更多细节，见 :ref:`dt-writing-property-values`。
关于 ``phandle*`` 类型属性的更多信息
见 :ref:`dt-phandles`。

.. list-table::
   :header-rows: 1
   :widths: 1 3 2

   * - 类型
     - 描述
     - DTS 中的示例

   * - ``string``
     - 恰好一个字符串
     - ``status = "disabled";``

   * - ``int``
     - 恰好一个 32 位值（单元格）
     - ``current-speed = <115200>;``

   * - ``boolean``
     - 为真时不带值、为假时不存在的标志
     - ``hw-flow-control;``

   * - ``array``
     - 零个或多个 32 位值（单元格）
     - ``offsets = <0x100 0x200 0x300>;``

   * - ``uint8-array``
     - 零个或多个字节，十六进制表示（设备树规范中的 'bytestring'）
     - ``local-mac-address = [de ad be ef 12 34];``

   * - ``string-array``
     - 零个或多个字符串
     - ``dma-names = "tx", "rx";``

   * - ``phandle``
     - 恰好一个 phandle
     - ``interrupt-parent = <&gic>;``

   * - ``phandles``
     - 零个或多个 phandle
     - ``pinctrl-0 = <&usart2_tx_pd5 &usart2_rx_pd6>;``

   * - ``phandle-array``
     - phandle 与 32 位单元格（通常是说明符）的列表
     - ``dmas = <&dma0 2>, <&dma0 3>;``

   * - ``path``
     - 以 phandle 路径引用或路径字符串形式表示的节点路径
     - ``zephyr,bt-c2h-uart = &uart0;`` 或
       ``foo = "/path/to/some/node";``

   * - ``compound``
     - 更复杂类型的兜底（不会生成宏）
     - ``foo = <&label>, [01 02];``

deprecated
==========

具有 ``deprecated: true`` 的属性向用户和工具
表明该属性打算逐步淘汰。

如果设备树包含被标记为弃用的属性，工具
将报告警告。（在
:ref:`twister_script` 中，该警告对上游拉取请求升级为错误。）

默认设置为 ``deprecated: false``。
因此使用 ``deprecated: false`` 是冗余的，强烈
不推荐。

.. _dt-bindings-default:

default
=======

可选的 ``default:`` 设置给出一个值，
当设备树节点中缺少该属性时使用。

例如，对于此绑定片段：

.. code-block:: YAML

   properties:
     foo:
       type: int
       default: 3

如果匹配节点中缺少属性 ``foo``，则输出
就好像 DTS 中出现了 ``foo = <3>;`` 一样
（只是默认值使用 YAML 数据类型）。

注意，对同一属性同时声明 ``default:`` 和 ``required: true`` 的绑定
会产生警告，因为这两个设置是冗余的：``required: true``
在属性缺失时已经使构建失败，因此默认值
永远不会生效。绑定仍可以用 ``required: true`` 覆盖
继承的 ``default:`` 以强制显式值；
这是有明确定义的，不会被报告。仅通过 ``include:``
到达的绑定在构建期间不会单独加载，
因此它的警告在生成文档时看到，
而不是在构建应用时看到。

关于上游 Zephyr 绑定中 ``default`` 的相关规则，
见 :ref:`dt-bindings-default-rules`。

示例见 :ref:`dt-bindings-example-properties`。在
:ref:`dt-bindings-example-properties` 中未使用的属性类型上放置 ``default:``
会报告错误。

enum
====

``enum:`` 行后跟属性可能包含的值列表。
如果 DTS 中的属性值不在绑定的 ``enum:`` 列表中，
报告错误。示例见 :ref:`dt-bindings-example-properties`。

.. _dt-bindings-min-max:

min 和 max
===========

``min:`` 和 ``max:`` 键约束
``type: int`` 或 ``type: array`` 属性的有效值范围。
如果 DTS 中的属性值在 ``[min, max]`` 范围之外，
报告错误。

两个键都是可选且独立的；可以只指定 ``min:``、
只指定 ``max:`` 或两者都指定。它们不能与同一属性上的 ``enum:`` 组合。

对于 ``type: array``，数组的每个元素都与范围比较。

示例：

.. code-block:: YAML

   properties:
     # 0 到 100 之间的亮度百分比
     brightness:
       type: int
       min: 0
       max: 100
       description: LED 亮度（百分比）

     # 毫秒为单位的超时，最小 1 ms（无上限）
     timeout-ms:
       type: int
       min: 1
       description: 毫秒为单位的超时

.. _dt-bindings-min-len-max-len:

min-len 和 max-len
===================

``min-len:`` 和 ``max-len:`` 键约束
数组类型属性（``array``、``uint8-array``、``string-array``、
``phandles`` 和 ``phandle-array``）的元素数量（长度）。
如果 DTS 中属性值的长度在 ``[min-len, max-len]`` 范围之外，
报告错误。

两个键都是可选且独立的；可以只指定 ``min-len:``、
只指定 ``max-len:`` 或两者都指定。

示例：

.. code-block:: YAML

   properties:
     # 恰好 3 个整数的数组
     coordinates:
       type: array
       min-len: 3
       max-len: 3
       description: 3D 坐标

     # 最多 4 个 GPIO phandle 的列表
     gpios:
       type: phandle-array
       max-len: 4
       description: 最多 4 个 GPIO

const
=====

这指定属性必须取的常数值。
它主要用于约束特定硬件
常见属性的值。

.. _dt-bindings-specifier-space:

specifier-space
==================

.. warning::

   以非惯例方式命名属性时滥用此功能
   是不当行为。

   例如，此功能不用于像将属性命名为
   ``my-pin`` 然后用此功能将其分配到 "gpio" 说明符空间
   这样的情况。引用 GPIO 的属性应使用惯例名称，即
   以 ``-gpios`` 或 ``-gpio`` 结尾。

此属性（如果存在）手动设置
``phandle-array`` 类型属性关联的说明符空间。

通常，说明符空间隐式编码在属性名中。
名为 ``foos`` 且类型为 ``phandle-array`` 的属性隐式具有
说明符空间 ``foo``。作为特殊情况，``*-gpios`` 属性
的说明符空间是 "gpio"，因此 ``foo-gpios`` 的说明符空间是 "gpio"
而不是 "foo-gpio"。

如果遵循该惯例会导致尴尬或非惯例的名称，
你可以使用 ``specifier-space`` 手动提供空间。

例如：

.. code-block:: YAML

   compatible: ...
   properties:
     bar:
       type: phandle-array
       specifier-space: my-custom-space

在上面，``bar`` 属性的说明符空间被设置为 "my-custom-space"。

然后你可以在设备树中这样使用该属性：

.. code-block:: DTS

   controller1: custom-controller@1000 {
           #my-custom-space-cells = <2>;
   };

   controller2: custom-controller@2000 {
           #my-custom-space-cells = <1>;
   };

   my-node {
           bar = <&controller1 10 20>, <&controller2 30>;
   };

一般来说，应保留此功能用于隐式说明符空间
命名惯例不起作用的情况。一个合适的
示例是说明符空间为 "mbox" 而非 "mboxe" 的 ``mboxes`` 属性。
可以这样写该属性：

.. code-block:: YAML

   properties:
     mboxes:
       type: phandle-array
       specifier-space: mbox

.. _dt-bindings-dependency-mode:

dependency-mode
=================

``dependency-mode`` 设置控制 phandle 属性在
Zephyr 中计算依赖图时如何处理。

默认情况下，任何 :ref:`phandle 属性 <phandle-properties>` 都会在
包含该属性的节点与其引用的节点之间创建依赖。``dependency-mode``
设置允许你覆盖此行为。

可能的值
---------------

``dependency-mode`` 设置接受以下值：

``normal`` 或未指定
   默认行为。引用节点依赖于被引用节点
   （phandle 指向的节点）。

``reverse``
   反转依赖方向。不是引用节点依赖于
   被引用节点，而是被引用节点依赖于引用节点。

``ignore``
   phandle 属性不创建依赖。

``child-ignore``
   类似于 ``ignore``，但仅当被引用
   节点是引用节点的子节点时才忽略依赖。如果被引用节点
   不是子节点，则创建正常依赖。

   当 phandle 可能引用子节点（无需依赖）
   或外部节点（需要依赖）时使用此值。

使用 dependency-mode
----------------------

``dependency-mode`` 设置在绑定文件的
属性定义内指定。以下是一个示例：

.. code-block:: YAML

   compatible: "vendor,ethernet-controller"

   properties:
     phy-handle:
       type: phandle
       description: |
         指定对表示 PHY 设备的节点的引用。
       dependency-mode: ignore

另一个使用 ``child-ignore`` 的示例：

.. code-block:: YAML

   compatible: "vendor,node-with-optional-phandle"

   properties:
     optional-ref:
       type: phandle
       description: |
         引用子节点或外部设备。
         子节点引用不创建依赖，但外部
         设备引用会创建。
       dependency-mode: child-ignore

使用该绑定的示例 DTS：

.. code-block:: DTS

   root {
           external_dev: external-device@2000 {
                   compatible = "vendor,external-device";
                   reg = <0x2000 0x100>;
           };

           parent_dev: parent-device@1000 {
                   compatible = "vendor,node-with-optional-phandle";
                   reg = <0x1000 0x100>;
                   optional-ref = <&internal_child>; /* 子节点：忽略依赖 */

                   internal_child: internal-device {
                           compatible = "vendor,internal-device";
                   };
           };

           peer_dev: peer-device@3000 {
                   compatible = "vendor,node-with-optional-phandle";
                   reg = <0x3000 0x100>;
                   optional-ref = <&external_dev>; /* 外部：正常依赖 */
           };
   };

默认行为
----------------

如果未指定 ``dependency-mode``，默认值为 ``normal``，
即引用节点依赖于被引用节点。

.. _dt-bindings-child:

Child-binding（子绑定）
*********************

当节点的所有子节点共享相同
属性时，可以使用 ``child-binding``。每个子节点
获得 ``child-binding`` 的内容作为其绑定，
不过子节点上显式的 ``compatible = ...`` 优先（
如果为其找到绑定的话）。

考虑一个 PWM LED 节点的绑定如下，其中子节点
被要求具有 ``pwms`` 属性：

.. code-block:: devicetree

   pwmleds {
           compatible = "pwm-leds";

           red_pwm_led {
                   pwms = <&pwm3 4 15625000>;
           };
           green_pwm_led {
                   pwms = <&pwm3 0 15625000>;
           };
           /* ... */
   };

该绑定如下所示：

.. code-block:: YAML

   compatible: "pwm-leds"

   child-binding:
     description: 使用 PWM 的 LED

     properties:
       pwms:
         type: phandle-array
         required: true

``child-binding`` 也可以递归工作。例如，此绑定：

.. code-block:: YAML

   compatible: foo

   child-binding:
     child-binding:
       properties:
         my-property:
           type: int
           required: true

将应用于此 DTS 中的 ``grandchild`` 节点：

.. code-block:: devicetree

   parent {
           compatible = "foo";
           child {
                   grandchild {
                           my-property = <123>;
                   };
           };
   };

.. _dt-bindings-bus:

Bus（总线）
***

如果节点是总线控制器，在绑定中使用 ``bus:``
说明总线类型。例如，SoC 上 SPI 外设的绑定
如下所示：

.. code-block:: YAML

   compatible: "manufacturer,spi-peripheral"
   bus: spi
   # ...

绑定中存在此键会告知构建系统
匹配此绑定的任何节点的子节点
出现在这种类型的总线上。

这进而影响 ``on-bus:`` 如何用于
子节点绑定的匹配。

对于支持多种协议的单一总线（例如 I3C 和 I2C），
绑定中的 ``bus:`` 值可以是列表：

.. code-block:: YAML

   compatible: "manufacturer,i3c-controller"
   bus: [i3c, i2c]
   # ...

.. _dt-bindings-on-bus:

On-bus（在总线上）
**********************

如果节点是出现在总线上的设备，在绑定中使用 ``on-bus:``
说明总线类型。

例如，外部 SPI 存储芯片的绑定应包含此行：

.. code-block:: YAML

   on-bus: spi

基于 I2C 的温度传感器绑定应包含此行：

.. code-block:: YAML

   on-bus: i2c

为节点查找绑定时，构建系统检查
父节点的绑定是否包含 ``bus: <bus type>``。如果包含，
则只考虑具有匹配 ``on-bus: <bus type>`` 的绑定
和没有显式 ``on-bus`` 的绑定。先搜索具有显式 ``on-bus: <bus
type>`` 的绑定，然后搜索没有显式 ``on-bus`` 的绑定。
搜索对节点 ``compatible`` 属性中的每一项重复进行，
按顺序。

此功能允许同一设备根据
其出现在哪种总线上而有不同的绑定。例如，考虑
compatible 为 ``manufacturer,sensor`` 的传感器设备，
可以通过 I2C 或 SPI 使用。

因此传感器节点可以出现在设备树中
作为 SPI 或 I2C 控制器的子节点，如下所示：

.. code-block:: devicetree

   spi-bus@0 {
      /* ... 某个带 'bus: spi' 的 compatible 等 ... */

      sensor@0 {
          compatible = "manufacturer,sensor";
          reg = <0>;
          /* ... */
      };
   };

   i2c-bus@0 {
      /* ... 某个带 'bus: i2c' 的 compatible 等 ... */

      sensor@79 {
          compatible = "manufacturer,sensor";
          reg = <79>;
          /* ... */
      };
   };

你可以写两个不同的绑定文件来匹配这些
各自的传感器节点，即使它们有相同的 compatible：

.. code-block:: YAML

   # manufacturer,sensor-spi.yaml，匹配 SPI 总线上的 sensor@0：
   compatible: "manufacturer,sensor"
   on-bus: spi

   # manufacturer,sensor-i2c.yaml，匹配 I2C 总线上的 sensor@79：
   compatible: "manufacturer,sensor"
   properties:
     uses-clock-stretching:
       type: boolean
   on-bus: i2c

只有 ``sensor@79`` 可以有 ``use-clock-stretching`` 属性。
总线敏感逻辑在为 ``sensor@0`` 搜索绑定时
忽略 :file:`manufacturer,sensor-i2c.yaml`。

.. _dt-bindings-class:

Class（类）
*****

如果匹配该绑定的节点可以用作一个或多个 Zephyr
设备类的设备，使用 ``class:`` 声明这些类：

.. code-block:: YAML

   compatible: "manufacturer,adc"
   class: adc

值是设备类名或名称列表。名称使用小写
字母、数字、``-`` 和 ``_``；格式错误或重复的名称会被拒绝。
每个名称应匹配通过
:c:macro:`DEVICE_API` 注册的设备 API 类（如 ``adc``）；
小写加连字符的名称会被转换为小写加下划线的 C 令牌，
方式与 compatible 相同。

此键声明节点驱动*可以*
实现哪些设备 API 类；节点实际构建哪个驱动和 API
仍是 Kconfig 的决定。列表值覆盖驱动可以
根据配置实现多个 API 的硬件：

.. code-block:: YAML

   compatible: "manufacturer,rtc"
   class: [rtc, counter]

``class:`` 通常在设备类基础绑定中声明一次
（例如 :zephyr_file:`dts/bindings/adc/adc-controller.yaml`），
以便包含它的每个绑定都继承该类。当绑定及其
包含的文件声明类时，值取并集：包含
多个类基础绑定的绑定属于它们所有的类。

类成员关系可以在构建时用
:c:macro:`DT_NODE_HAS_CLASS` 查询、用
:c:macro:`DT_FOREACH_CLASS_STATUS_OKAY` 遍历、用
:c:macro:`DT_NUM_CLASS_STATUS_OKAY` 计数，
并可用 Kconfig 中的 ``$(dt_class_enabled,<class name>)`` 测试。

要为绑定无法更改的设备添加类，
例如为来自下游模块的上游设备分类，
定义一个更具体的 compatible，其绑定包含原始绑定并声明
该 class，然后在节点上列出两个 compatible：

.. code-block:: YAML

   # vnd,foo-classed.yaml
   compatible: "vnd,foo-classed"
   include: vnd,foo.yaml
   class: xyz

.. code-block:: devicetree

   compatible = "vnd,foo-classed", "vnd,foo";

节点的绑定（及其类）来自第一个
有绑定的 compatible；驱动匹配节点的任何 compatible，
因此原始驱动仍然绑定。同一 compatible 的两个绑定是
错误，因此现有绑定不能被遮蔽。

.. _dt-bindings-examples:

示例（Examples）
********

如果你觉得想为你的绑定提供一个最小示例，
可以这样使用：

.. code-block:: yaml

   description: ...

   properties:
    ...

   examples:
     - |
       leds {
         compatible = "gpio-leds";

         uled: led {
         gpios = <&gpioe 12 GPIO_ACTIVE_HIGH>;
         };
       };

.. _dt-bindings-cells:

说明符单元格名称（\*-cells）
*******************************

本节记录如何在绑定中为说明符内的
单元格命名。这些概念在本指南后面
:ref:`dt-phandle-arrays` 中详细讨论。

考虑一个绑定的节点，其 phandle 可能出现在
``phandle-array`` 属性中，如下例中的 PWM 控制器 ``pwm1`` 和 ``pwm2``：

.. code-block:: DTS

   pwm1: pwm@deadbeef {
       compatible = "foo,pwm";
       #pwm-cells = <2>;
   };

   pwm2: pwm@deadbeef {
       compatible = "bar,pwm";
       #pwm-cells = <1>;
   };

   my-node {
       pwms = <&pwm1 1 2000>, <&pwm2 3000>;
   };

compatible ``"foo,pwm"`` 和 ``"bar,pwm"`` 的绑定必须
使用 ``pwm-cells:`` 为出现在 PWM 说明符中的
单元格命名，如下所示：

.. code-block:: YAML

   # foo,pwm.yaml
   compatible: "foo,pwm"
   ...
   pwm-cells:
     - channel
     - period

   # bar,pwm.yaml
   compatible: "bar,pwm"
   ...
   pwm-cells:
     - period

``*-names``（如 ``pwm-names``）属性也可以出现在节点上，
为每个条目命名。

这使得可以按名称访问说明符中的单元格，
例如使用 :c:macro:`DT_PWMS_CHANNEL_BY_NAME` 之类的 API。

如果说明符为空（如 ``#clock-cells = <0>``），
则 ``*-cells`` 可以省略（推荐）
或设置为空数组。注意空数组
在 YAML 中指定为如 ``clock-cells: []``。

.. _dt-bindings-include:

Include（包含）
*********

绑定可以包含其他文件，
可用于在绑定之间共享通用属性
定义。使用 ``include:`` 键。其值
是字符串或列表。

最简单的情况下，可以通过
字符串形式给出文件名来包含另一个文件，如下所示：

.. code-block:: YAML

   include: foo.yaml

如果找到名为 :file:`foo.yaml` 的文件（
搜索过程见 :ref:`dt-where-bindings-are-located`），
它将被包含到此绑定中。

包含的文件通过简单的递归字典
合并并入绑定。构建系统会检查
合并后的绑定格式正确。可以在任何层级包含，
包括 ``child-binding``，如下所示：

.. code-block:: YAML

   # foo.yaml 将与本层内容合并
   include: foo.yaml

   child-binding:
     # bar.yaml 将与本层内容合并
     include: bar.yaml

如果某个键在绑定和
其包含的文件中以不同值出现，则是错误，
有两个例外：绑定可以对
:ref:`属性定义 <dt-bindings-properties>` 使用 ``required: true``，
而包含文件使用 ``required: false``（``required: true``
优先，允许绑定加强来自包含
文件的要求），以及 ``class:`` 值按
:ref:`dt-bindings-class` 所述取并集。

注意，在包含文件使用 ``required: true`` 的地方
使用 ``required: false`` 来削弱要求是错误。
这是为了保持组织整洁。

文件 :zephyr_file:`base.yaml <dts/bindings/base/base.yaml>` 包含
许多常见属性的定义。编写新绑定时，
好的做法是检查 :file:`base.yaml` 是否已定义
所需的部分属性，如果是则包含它。

注意，可以这样使 base.yaml 中定义的属性变为必需，
以 :ref:`reg <dt-important-props>` 为例：

.. code-block:: YAML

   reg:
     required: true

这依赖字典合并来填充 ``reg`` 的其他键，
如 ``type``。

要包含多个文件，可以使用字符串列表：

.. code-block:: YAML

   include:
     - foo.yaml
     - bar.yaml

这会包含文件 :file:`foo.yaml` 和 :file:`bar.yaml`。（
可以将此列表写成 YAML 单行 ``include: [foo.yaml, bar.yaml]``。）

包含多个文件时，包含文件中属性重叠的 ``required`` 键
按逻辑或（OR）合并。这确保 ``required:
true`` 始终被遵守。

在某些情况下，你可能想从文件包含
部分属性定义，而非全部。在这种情况下，``include:``
应是列表，可以在列表中放映射来
过滤出只想要的定义，如下所示：

.. code-block:: YAML

   include:
     - name: foo.yaml
       property-allowlist:
         - i-want-this-one
         - and-this-one
     - name: bar.yaml
       property-blocklist:
         - do-not-include-this-one
         - or-this-one

每个映射元素必须有 ``name`` 键（要包含的文件名），
可以具有 ``property-allowlist`` 和 ``property-blocklist`` 键
来过滤包含哪些属性。

单个映射元素不能同时具有 ``property-allowlist`` 和
``property-blocklist`` 键。两个键都没有的映射元素有效；
不做额外过滤。

可以在单个 ``include:`` 列表中自由混用
字符串和映射：

.. code-block:: YAML

   include:
     - foo.yaml
     - name: bar.yaml
       property-blocklist:
         - do-not-include-this-one
         - or-this-one

最后，可以这样从子绑定过滤：

.. code-block:: YAML

   include:
     - name: bar.yaml
       child-binding:
         property-allowlist:
           - child-prop-to-allow

Nexus 节点与映射
********************

所有 ``phandle-array`` 类型属性都支持通过 ``*-map``
属性（如 ``gpio-map``）进行映射，
由设备树规范定义。

这用于例如为常见排针
定义连接器节点，如 ``arduino_header`` 节点，
惯例上定义在具有 Arduino 兼容扩展排针
的开发板的设备树中。
