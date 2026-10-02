.. _dt-syntax:

语法与结构
####################

顾名思义，设备树是一棵树。
这棵树的人类可读文本格式称为 DTS（devicetree source，设备树源），
定义在 `设备树规范`_ 中。

.. _设备树规范: https://www.devicetree.org/

本页的目的是以比规范更渐进的方式介绍设备树。
不过，你可能仍需参考规范才能理解一些详细情况。

.. contents:: Contents
   :local:

示例
*******

以下是一个示例 DTS 文件：

.. code-block:: devicetree

   /dts-v1/;

   / {
           a-node {
                   subnode_nodelabel: a-sub-node {
                           foo = <3>;
                   };
           };
   };

``/dts-v1/;`` 行意味着文件内容在 DTS 语法版本 1 中，
它已取代现在过时的"版本 0"。

节点
*****

与任何树数据结构一样，设备树有 *节点* 的层次结构。
上面的树有三个节点：

#. 一个根节点：``/``
#. 一个名为 ``a-node`` 的节点，是根节点的子节点
#. 一个名为 ``a-sub-node`` 的节点，是 ``a-node`` 的子节点

.. _dt-node-labels:

节点可以被分配 *节点标签*，这是引用带标签节点的唯一简写。
上面，``a-sub-node`` 有节点标签 ``subnode_nodelabel``。
一个节点可以有零个、一个或多个节点标签。
你可以使用节点标签在设备树其他地方引用该节点。

设备树节点有 *路径* 标识它们在树中的位置。
与 Unix 文件系统路径一样，设备树路径是用斜杠（``/``）分隔的字符串，
根节点的路径是单个斜杠：``/``。
否则，每个节点的路径通过将节点的祖先名称与节点自身名称拼接、用斜杠分隔来形成。
例如，``a-sub-node`` 的完整路径是 ``/a-node/a-sub-node``。

属性
**********

设备树节点还可以有 *属性*。属性是名称/值对。
属性值可以是任何字节序列。
在某些情况下，值是称为 *单元格*（cell）的数组。
单元格只是一个 32 位无符号整数。

节点 ``a-sub-node`` 有一个名为 ``foo`` 的属性，
其值是值为 3 的单元格。
``foo`` 值的大小和类型由 DTS 中的尖括号（``<`` 和 ``>``）暗示。

更多示例属性值见下面的 :ref:`dt-writing-property-values`。

设备树反映硬件
****************************

在实践中，设备树节点通常对应某些硬件，
节点层次结构反映硬件的物理布局。
例如，考虑一块开发板，其 SoC 上的 I2C 总线控制器
连接着三个 I2C 外设，如下所示：

.. figure:: zephyr_dt_i2c_high_level.png
   :alt: 带三个 I2C 外设的开发板表示
   :figclass: align-center

对应 I2C 总线控制器和每个 I2C 外设的节点
都会出现在设备树中。反映硬件布局，
I2C 外设节点是总线控制器节点的子节点。
表示其他类型硬件的类似约定也存在。

DTS 看起来类似这样：

.. code-block:: devicetree

   /dts-v1/;

   / {
           soc {
                   i2c-bus-controller {
                           i2c-peripheral-1 {
                           };
                           i2c-peripheral-2 {
                           };
                           i2c-peripheral-3 {
                           };
                   };
           };
   };

实践中的属性
**********************

在实践中，属性通常描述或配置节点所代表的硬件。
例如，I2C 外设的节点有一个属性，
其值是外设在总线上的地址。

这里是一个表示相同示例的树，
但带有处理 I2C 设备时可能看到的
真实世界节点名称和属性。

.. figure:: zephyr_dt_i2c_example.png
   :figclass: align-center

   带真实世界名称和属性的 I2C 设备树示例。
   节点名称位于每个节点顶部，灰色背景。
   属性显示为"名称=值"行。

这是对应的 DTS：

.. code-block:: devicetree

   /dts-v1/;

   / {
           soc {
                   i2c@40003000 {
                           compatible = "nordic,nrf-twim";
                           reg = <0x40003000 0x1000>;

                           apds9960@39 {
                                   compatible = "avago,apds9960";
                                   reg = <0x39>;
                           };
                           ti_hdc@43 {
                                   compatible = "ti,hdc", "ti,hdc1010";
                                   reg = <0x43>;
                           };
                           mma8652fc@1d {
                                   compatible = "nxp,fxos8700", "nxp,mma8652fc";
                                   reg = <0x1d>;
                           };
                   };
           };
   };

.. _dt-unit-address:

单元地址
**************

除了展示更多真实世界名称和属性外，
上面的示例引入了一个新的设备树概念：单元地址。
单元地址是节点名称中 "at" 符号（``@``）之后的部分，
如 ``i2c@40003000`` 中的 ``40003000``，
或 ``apds9960@39`` 中的 ``39``。
单元地址是可选的：``soc`` 节点没有一个。

在设备树中，单元地址给出节点在其父节点地址空间中的地址。
以下是不同类型硬件的一些示例单元地址。

内存映射外设
    外设寄存器映射基地址。
    例如，名为 ``i2c@40003000`` 的节点代表一个 I2C 控制器，
    其寄存器映射基地址是 0x40003000。

I2C 外设
    外设在 I2C 总线上的地址。
    例如，上一节 I2C 控制器的子节点
    ``apds9960@39`` 的 I2C 地址是 0x39。

SPI 外设
    表示外碎片选线编号的索引。
    （如果没有片选线，使用 0。）

内存
    物理起始地址。
    例如，名为 ``memory@2000000`` 的节点代表
    从物理地址 0x2000000 开始的 RAM。

内存映射 flash
    与 RAM 一样，物理起始地址。
    例如，名为 ``flash@8000000`` 的节点代表
    物理起始地址为 0x8000000 的 flash 设备。

固定 flash 分区
    当设备树用于存储 flash 分区表时适用。
    单元地址是分区在 flash 内存中的起始偏移。
    例如，考虑这个 flash 设备及其分区：

    .. code-block:: devicetree

       flash@8000000 {
           /* ... */
           partitions {
                   partition@0 { /* ... */ };
                   partition@20000 {  /* ... */ };
                   /* ... */
           };
       };

    名为 ``partition@0`` 的节点与其 flash 设备起始的偏移为 0，
    因此其基地址是 0x8000000。
    类似地，名为 ``partition@20000`` 的节点的基地址是 0x8020000。

.. _dt-important-props:

重要属性
********************

.. 文档维护者：如果你向此列表添加属性，
   确保它也从 gen_devicetree_rest.py 链接过来。

设备树规范定义了几个标准属性。
一些最重要的是：

compatible
    节点所代表硬件设备的名称。

    推荐格式是 ``"vendor,device"``，如 ``"avago,apds9960"``，
    或这些的序列，如 ``"ti,hdc", "ti,hdc1010"``。
    ``vendor`` 部分是厂商的缩写名称。
    文件 :zephyr_file:`dts/bindings/vendor-prefixes.txt` 包含
    一个通常接受的 ``vendor`` 名称列表。
    ``device`` 部分通常取自数据手册。

    当硬件行为是通用的时，
    它也有时是像 ``gpio-keys``、``mmio-sram`` 或
    ``fixed-clock`` 这样的值。

    构建系统使用 compatible 属性查找节点的正确
    :ref:`绑定 <dt-bindings>`。
    设备驱动使用 ``devicetree.h`` 查找
    具有相关 compatible 的节点，
    以确定可管理的可用硬件。

    ``compatible`` 属性可以有多个值。
    当设备是更通用家族的特定实例时，
    额外值很有用，允许系统从最特定到最不特定匹配设备驱动。

    在 Zephyr 的绑定语法中，此属性类型为 ``string-array``。

reg
    用于寻址设备的信息。值特定于设备
    （即根据 compatible 属性不同）。

    ``reg`` 属性是 ``(address, length)`` 对的序列。
    每个对称为"寄存器块"。值按惯例用十六进制书写。

    以下是一些常见模式：

    - 通过内存映射 I/O 寄存器访问的设备
      （如 ``i2c@40003000``）：
      ``address`` 通常是 I/O 寄存器空间的基地址，
      ``length`` 是寄存器占用的字节数。
    - I2C 设备（如 ``apds9960@39`` 及其兄弟节点）：
      ``address`` 是 I2C 总线上的从地址。
      没有 ``length`` 值。
    - SPI 设备：``address`` 是片选线编号；
      没有 ``length``。

    你可能会注意到 ``reg`` 属性与上面描述的
    常见单元地址之间的一些相似之处。
    这不是巧合。``reg`` 属性可以看作
    比单元地址更详细的设备内可寻址资源的视图。

status
    描述节点是否启用的字符串。

    设备树规范允许此属性有
    ``"okay"``、``"disabled"``、``"reserved"``、``"fail"`` 和
    ``"fail-sss"`` 值。
    Zephyr 将任何非 ``"okay"`` 值视为禁用。
    特别是，``"reserved"`` 用于记录节点存在
    但在其他地方启用（例如多域应用中由另一个核心或域启用）；
    它由 ``edtlib`` 以与 ``"disabled"`` 相同的方式处理。
    其余值（``"fail"`` 和 ``"fail-sss"``）的使用
    目前未被 Zephyr 使用。

    如果节点的 status 属性是 ``"okay"`` 或未定义
    （即不存在于设备树源中），
    则该节点被视为启用。
    status 为 ``"disabled"`` 的节点被显式禁用。
    对应物理设备的设备树节点必须启用，
    Zephyr 驱动模型中对应的 ``struct device`` 才会
    被分配和初始化。

    注意当父节点被禁用时，子节点不会被隐式禁用，
    即如果需要，子节点应被显式禁用。

interrupts
    设备生成的中断的信息，编码为一个或多个
    *中断说明符*的数组。
    每个中断说明符有若干单元格。
    更多细节见 `设备树规范 release v0.3`_
    第 2.4 节，*Interrupts and Interrupt Mapping*
    （中断和中断映射）。

.. _设备树规范release-v0.3:
   https://www.devicetree.org/specifications/

.. highlight:: none

.. note::

   早期版本的 Zephyr 经常使用 ``label`` 属性，
   它与标准 :ref:`节点标签 <dt-node-labels>` 不同。
   在新设备树绑定中使用 label 属性，
   以及在新代码中使用 :c:macro:`DT_LABEL` 宏，
   被积极不推荐。
   出于历史原因，label 属性继续存在于
   某些现有绑定和覆盖中，
   但不应在新绑定或设备实现中使用。

.. _dt-writing-property-values:

编写属性值
***********************

本节描述如何在 DTS 格式中编写属性值。
下面表格中的属性类型在 :ref:`dt-bindings` 中详细描述。

为保持简单，跳过了一些具体内容；
如果你对细节好奇，见设备树规范。

.. list-table::
   :header-rows: 1
   :widths: 1 4 4

   * - 属性类型
     - 如何编写
     - 示例

   * - string
     - 双引号
     - ``a-string = "hello, world!";``

   * - int
     - 尖括号（``<`` 和 ``>``）之间
     - ``an-int = <1>;``

   * - boolean
     - 为 ``true`` 时无值（为 ``false``，使用 ``/delete-property/``）
     - ``my-true-boolean;``

   * - array
     - 尖括号（``<`` 和 ``>``）之间，用空格分隔
     - ``foo = <0xdeadbeef 1234 0>;``

   * - uint8-array
     - 十六进制 *无* 前导 ``0x``，方括号（``[`` 和 ``]``）之间。
     - ``a-byte-array = [00 01 ab];``

   * - string-array
     - 用逗号分隔
     - ``a-string-array = "string one", "string two", "string three";``

   * - phandle
     - 尖括号（``<`` 和 ``>``）之间
     - ``a-phandle = <&mynode>;``

   * - phandles
     - 尖括号（``<`` 和 ``>``）之间，用空格分隔
     - ``some-phandles = <&mynode0 &mynode1 &mynode2>;``

   * - phandle-array
     - 尖括号（``<`` 和 ``>``）之间，用空格分隔
     - ``a-phandle-array = <&mynode0 1 2>, <&mynode1 3 4>;``

上面的附加说明：

- ``phandle``、``phandles`` 和 ``phandle-array`` 类型中的值
  在 :ref:`dt-phandles` 中进一步描述

- 布尔属性存在即为真。它不应有值。
  布尔属性只有在 DTS 中完全缺失时才为假。

- 上面的 ``foo`` 属性值有三个 *单元格*，
  值依次为 0xdeadbeef、1234 和 0。
  注意允许十六进制和十进制数字且可以混合使用。
  由于 Zephyr 将 DTS 转换为 C 源代码，
  这里不需要指定单个字节的字节序。

- 64 位整数写为两个 32 位单元格，大端顺序。
  值 0xaaaa0000bbbb1111 写为 ``<0xaaaa0000 0xbbbb1111>``。

- ``a-byte-array`` 属性值是三个字节 0x00、0x01 和 0xab，依次排列。

- 允许圆括号、算术运算符和按位运算符。
  ``bar`` 属性包含一个值为 64 的单元格：

  .. code-block:: devicetree

     bar = <(2 * (1 << 5))>;

  注意整个表达式必须用圆括号括起来。

- 圆括号表达式求值为负值的单元格，
  如 ``<(-1)>`` 或 ``<(4 - 6)>``，
  对 ``int`` 和 ``array`` 类型属性保留为有符号值。
  写为正十进制或十六进制字面量
  （包括 ``0xffffffff``）或表达式求值为非负值的单元格
  保持无符号。

- 属性值通过 *phandle* 引用设备树中的其他节点。
  你可以使用 ``&foo`` 编写 phandle，
  其中 ``foo`` 是 :ref:`节点标签 <dt-node-labels>`。
  以下是一个示例设备树片段：

  .. code-block:: devicetree

     foo: device@0 { };
     device@1 {
             sibling = <&foo 1 2>;
     };

  节点 ``device@1`` 的 ``sibling`` 属性包含三个单元格，按此顺序：

  #. ``device@0`` 节点的 phandle，
     这里写为 ``&foo``，
     因为 ``device@0`` 节点有节点标签 ``foo``
  #. 值 1
  #. 值 2

  在设备树中，phandle 值是一个单元格
  -- 再次只是一个 32 位无符号 int。
  不过，Zephyr 设备树 API 通常将这些值
  暴露为 *节点标识符*。
  节点标识符在 :ref:`dt-from-c` 中更详细地介绍。

- 数组和类似类型属性值可以拆分为若干 ``<>`` 块，如下所示：

  .. code-block:: devicetree

     foo = <1 2>, <3 4>;                         // Okay for 'type: array'
     foo = <&label1 &label2>, <&label3 &label4>; // Okay for 'type: phandles'
     foo = <&label1 1 2>, <&label2 3 4>;         // Okay for 'type: phandle-array'

  如果值可以逻辑分组为子值块，
  可能时为可读性推荐此方式。

.. _dt-alias-chosen:

别名与 chosen 节点
************************

除 :ref:`节点标签 <dt-node-labels>` 外，
还有两种额外方式可以不指定完整路径而引用特定节点：
通过别名，或通过 chosen 节点。

以下是一个同时使用两者的示例设备树：

.. code-block:: devicetree

   /dts-v1/;

   / {
   	chosen {
   		zephyr,console = &uart0;
        };

   	aliases {
   		my-uart = &uart0;
   	};

   	soc {
   		uart0: serial@12340000 {
   			...
   		};
   	};
   };

``/aliases`` 和 ``/chosen`` 节点不引用实际硬件设备。
它们的目的是指定设备树中的其他节点。

上面，``my-uart`` 是路径为 ``/soc/serial@12340000`` 的节点的别名。
使用其节点标签 ``uart0``，相同的节点被设置为
chosen ``zephyr,console`` 节点的值。

Zephyr 示例应用有时使用别名允许
以通用方式覆盖应用使用的特定硬件设备。
例如，:zephyr:code-sample:`blinky` 使用它
通过 ``led0`` 别名抽象要闪烁的 LED。

``/chosen`` 节点的属性用于配置系统或子系统范围的值。
更多信息见 :ref:`devicetree-chosen-nodes`。
