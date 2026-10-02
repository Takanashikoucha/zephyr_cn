.. _dt-phandles:

Phandle
########

设备树中*phandle*的概念与 C 中的指针非常类似。
你可以像使用指针引用 C 中的结构一样，
使用 phandle 引用设备树中的节点。

.. contents:: Contents
   :local:

获取 phandle
****************

获取设备树节点 phandle 的通常方式
是从其节点标签之一获取。
例如，对于此设备树：

.. code-block:: DTS

   / {
           lbl_a: node-1 {};
           lbl_b: lbl_c: node-2 {};
   };

你可以编写 phandle 为：

- ``/node-1`` 写为 ``&lbl_a``
- ``/node-2`` 写为 ``&lbl_b`` 或 ``&lbl_c``

注意 ``&nodelabel`` 设备树语法
与"取地址"C 语法的相似之处。

使用 phandle
**************

.. note::

   本节中的"类型"指设备树绑定文档
   :ref:`dt-bindings-properties` 中记录的
   类型名称之一。

以下是你将使用 phandle 的主要方式。

一个节点：phandle 类型
======================

你可以使用 phandle 从 ``node-a`` 引用 ``node-b``，
其中 ``node-b`` 以某种方式与 ``node-a`` 相关。

一个常见示例是 ``node-a`` 代表生成中断的某些硬件，
``node-b`` 代表接收被置位中断的中断控制器。
在这种情况下，你可以编写：

.. code-block:: DTS

   node_b: node-b {
           interrupt-controller;
   };

   node-a {
           interrupt-parent = <&node_b>;
   };

这使用设备树规范中定义的标准 ``interrupt-parent`` 属性
来捕获两个节点之间的关系。

这些属性类型为 ``phandle``。

零个或多个节点：phandles 类型
================================

你可以使用 phandle 创建引用其他节点的数组。

一个常见示例出现在 :ref:`引脚控制 <pinctrl-guide>` 中。
引脚控制属性如 ``pinctrl-0``、``pinctrl-1`` 等
可能包含多个 phandle，
每个"指向"包含与该硬件外设引脚配置
相关信息的节点。
以下是单个属性中六个 phandle 的示例：

.. code-block:: DTS

   pinctrl-0 = <&quadspi_clk_pe10 &quadspi_ncs_pe11
               &quadspi_bk1_io0_pe12 &quadspi_bk1_io1_pe13
               &quadspi_bk1_io2_pe14 &quadspi_bk1_io3_pe15>;

这些属性类型为 ``phandles``。

带元数据的零个或多个节点：phandle-array 类型
================================================

你可以使用 phandle 引用并配置
一个或多个由其他节点"拥有"的资源。

这是最复杂的情况。
下一节有示例和更多细节。

这些属性类型为 ``phandle-array``。

.. _dt-phandle-arrays:

phandle-array 属性
************************

这些属性通常用于指定由另一个节点拥有的资源
以及关于该资源的附加元数据。

高层描述
=====================

通常，这种类型的属性写得像此示例中的
``phandle-array-prop``：

.. code-block:: dts

   node {
           phandle-array-prop = <&foo 1 2>, <&bar 3>, <&baz 4 5>;
   };

即，属性值写为逗号分隔的"组"序列，
每个"组"写在尖括号（``< ... >``）内。
每个"组"以一个 phandle（``&foo``、``&bar``、``&baz``）开头。
每个"组"中 phandle 后面的值称为*说明符*。
上面示例中有三个说明符：

#. ``1 2``
#. ``3``
#. ``4 5``

每个"组"中的 phandle 用于"指向"
控制你感兴趣资源的硬件。
说明符描述资源本身，
以及任何必要的附加元数据。

本节其余部分描述一个常见示例。
后续部分记录关于如何在实践中使用
phandle-array 属性的更多规则。

示例 phandle-arrays：GPIOs
=============================

phandle-array 属性最常见的用例
可能是指定 SoC 上的一个或多个 GPIO，
另一个芯片连接到这些 GPIO。
因此，我们将聚焦于这个用例。
但是，还有**许多其他用例**
在设备树中用 phandle-array 属性处理。

例如，考虑一个外部芯片，其中断引脚
连接到 SoC 上的 GPIO。
你通常需要提供该 GPIO 的信息
（GPIO 控制器和引脚编号）
给该芯片的 :ref:`设备驱动 <device_model_api>`。
你通常还需要向驱动提供关于 GPIO 的其他元数据，
如它是低有效还是高有效，
应在 SoC 内启用哪种内部上拉电阻
才能与设备通信等。

在设备树中，将有一个节点代表
控制一组引脚的 GPIO 控制器。
这反映了 GPIO IP 块在硬件中通常的开发方式。
因此，设备树中没有单个节点
代表一个 GPIO 引脚，
你也不能用单个 phandle 来表示它。

相反，你会使用 phandle-array 属性，
如下所示：

.. code-block::

   my-external-ic {
           irq-gpios = <&gpioX pin flags>;
   };

在此示例中，``irq-gpios`` 是一个 phandle-array 属性，
其值中只有一个"组"。
``&gpioX`` 是控制该引脚的 GPIO 控制器节点的 phandle。
``pin`` 是引脚编号（0、1、2、...）。
``flags`` 是描述引脚元数据的位掩码
（例如 ``(GPIO_ACTIVE_LOW | GPIO_PULL_UP)``）；
更多细节见 :zephyr_file:`include/zephyr/dt-bindings/gpio/gpio.h`。

处理 ``my-external-ic`` 节点的设备驱动
然后可以使用 ``irq-gpios`` 属性的值
为芯片设置中断处理，
正如它在你开发板上的使用方式。
这让你能在设备树中配置设备驱动，
而无需更改驱动源代码。

此类属性也可以包含多个值：

.. code-block::

   my-other-external-ic {
           handshake-gpios = <&gpioX pinX flagsX>, <&gpioY pinY flagsY>;
   };

上面示例指定了两个引脚：

- ``&gpioX`` GPIO 控制器上的 ``pinX``，标志 ``flagsX``
- ``&gpioY`` 上的 ``pinY``，标志 ``flagsY``

你可能想知道"引脚和标志"约定是如何建立和强制执行的。
要回答这个问题，我们需要在继续讨论设备树绑定
之前引入一个称为说明符空间的概念。

.. _dt-specifier-spaces:

说明符空间
****************

*说明符空间*是一种方式，
允许节点描述你应如何在
phandle-array 属性中使用它们。

在转向具体示例并提供关于如何在实践中
使用 DTS 文件和绑定文件工作的进一步阅读
参考之前，
我们将从 DTS 文件中说明符空间如何工作的
抽象高层描述开始。

高层描述
=====================

如上所述，phandle-array 属性
是 phandle 后跟若干单元格的"组"序列：

.. code-block:: dts

   node {
           phandle-array-prop = <&foo 1 2>, <&bar 3>;
   };

每个 phandle 后面的单元格称为*说明符*。
在此示例中，有两个说明符：

#. ``1 2``：两个单元格
#. ``3``：一个单元格

每个 phandle-array 属性都有一个关联的*说明符空间*。
这听起来很复杂，但它实际上只是一种方式，
以硬件特定的方式为每个 phandle 后面的单元格
分配含义。每个说明符空间都有唯一名称。
有一些用于常用硬件的"标准"名称，
但你也可以创建自己的。

设备树节点通过名称编码说明符中
必须出现的单元格数量，
使用 ``#SPACE_NAME-cells`` 属性。
例如，假设 ``phandle-array-prop`` 的
说明符空间名为 ``baz``。
那么 ``foo`` 和 ``bar`` 节点
需要有以下 ``#baz-cells`` 属性：

.. code-block:: DTS

   foo: node@1000 {
           #baz-cells = <2>;
   };

   bar: node@2000 {
           #baz-cells = <1>;
   };

没有 ``#baz-cells`` 属性，
设备树工具将无法验证
``phandle-array-prop`` 中每个说明符的单元格数量。

这种灵活性允许你在单个设备树属性中
写下硬件资源数组，
即使描述每个资源所需的元数据量
对不同节点可能不同。

单个节点也可以在不同说明符空间中
有不同数量的单元格。例如，我们可能有：

.. code-block:: DTS

   foo: node@1000 {
           #baz-cells = <2>;
           #bob-cells = <1>;
   };

有了这些，如果 ``phandle-array-prop-2`` 有
说明符空间 ``bob``，我们可以编写：

.. code-block:: DTS

   node {
           phandle-array-prop = <&foo 1 2>, <&bar 3>;
           phandle-array-prop-2 = <&foo 4>;
   };

这种灵活性允许你拥有一个节点
同时管理多种不同类型的资源。
该节点使用不同的 ``#SPACE_NAME-cells`` 属性
描述描述每种资源所需的元数据量
（每种情况需要多少个单元格）。

示例说明符空间：gpio
=============================

从上面的示例中，你已经熟悉了一个说明符空间
如何工作：在"gpio"空间中，说明符几乎总是有两个单元格：

#. 引脚编号
#. 与引脚相关的标志位掩码

因此，在实践中你看到的几乎所有 GPIO 控制器节点
都会像这样：

.. code-block:: DTS

   gpioX: gpio-controller@deadbeef {
           gpio-controller;
           #gpio-cells = <2>;
   };

将属性与说明符空间关联
********************************************

上面，我们描述了：

- 每个 phandle-array 属性都有一个关联的说明符空间
- 说明符空间通过名称标识
- 设备树节点使用 ``#SPECIFIER_NAME-cells`` 属性
  配置说明符中必须出现的单元格数量

在本节中，我们解释 phandle-array 属性
如何获得其说明符空间。

高层描述
=====================

一般来说，名为 ``foos`` 的 ``phandle-array`` 属性
隐式具有说明符空间 ``foo``。例如：

.. code-block:: YAML

   properties:
     dmas:
       type: phandle-array
     pwms:
       type: phandle-array

``dmas`` 属性的说明符空间是"dma"。
``pwms`` 属性的说明符空间是 ``pwm``。

特殊情况：GPIOs 和 IO channels
===================================

``*-gpios`` 和 ``*-io-channels`` 属性
被特殊处理，使得例如 ``foo-gpios`` 和
``bar-io-channels`` 分别解析为 ``#gpio-cells`` 和
``#io-channel-cells``，
而不是 ``#foo-gpio-cells`` 和 ``#bar-io-channel-cells``。

手动指定空间
===========================

你可以手动指定任何 ``phandle-array`` 属性的
说明符空间。见 :ref:`dt-bindings-specifier-space`。

命名说明符中的单元格
*******************************

编写绑定时，你应该为你硬件支持的
每个说明符空间中的单元格命名。
如何做到此点的细节见 :ref:`dt-bindings-cells`。

这允许 C 代码使用如下的设备树 API
按名称查询说明符中单元格的信息
并获取其值：

- :c:macro:`DT_PHA_BY_IDX`
- :c:macro:`DT_PHA_BY_NAME`

这个功能和这些宏被众多硬件特定
API 内部使用。以下是几个示例：

- :c:macro:`DT_GPIO_PIN_BY_IDX`
- :c:macro:`DT_PWMS_CHANNEL_BY_IDX`
- :c:macro:`DT_DMAS_CELL_BY_NAME`
- :c:macro:`DT_IO_CHANNELS_INPUT_BY_IDX`
- :c:macro:`DT_CLOCKS_CELL_BY_NAME`

另见
********

- :ref:`dt-writing-property-values`：如何在设备树属性中编写 phandle

- :ref:`dt-bindings-properties`：如何为 phandle 类型
  （``phandle``、``phandles``、``phandle-array``）的属性编写绑定

- :ref:`dt-bindings-specifier-space`：如何手动指定
  phandle-array 属性的说明符空间

- :ref:`dt-bindings-dependency-mode`：如何使用
  phandle 属性控制节点依赖
