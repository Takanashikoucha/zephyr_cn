.. _dt-from-c:

从 C/C++ 访问设备树
############################

本指南介绍 Zephyr 的 ``<zephyr/devicetree.h>`` API，
用于从 C 源文件读取设备树。它假设你熟悉
:ref:`devicetree-intro` 和 :ref:`dt-bindings` 中的概念。
参考材料见 :ref:`dt-reference`。

给 Linux 开发者的说明
***************************

熟悉设备树的 Linux 开发者应注意，这里描述的 API
与 Linux 上使用设备树的方式差异很大。

Linux 内核不会生成一个包含所有设备树数据的 C 头文件
然后用宏 API 对其抽象，而是直接读取其二进制形式的
设备树数据结构。二进制表示在运行时被解析，
例如用于加载和初始化设备驱动。

Zephyr 不采用这种方式，因为设备树二进制及其
相关处理代码的体积太大，无法从容容纳在
Zephyr 支持的相对受限的设备上。

.. _dt-node-identifiers:

节点标识符
****************

要获取某个设备树节点的信息，你需要它的*节点标识符*。
这只是一个引用该节点的 C 宏。

获取节点标识符的主要方式如下：

按路径
   使用 :c:macro:`DT_PATH()` 连同节点在设备树中从根节点开始的
   完整路径。当你恰好知道要找的确切节点时，这通常很有用。

按节点标签
   使用 :c:macro:`DT_NODELABEL()` 从 :ref:`节点标签
   <dt-node-labels>` 获取节点标识符。节点标签通常由 SoC 的 :file:`.dtsi`
   文件提供，用于给节点命名以匹配 SoC 数据手册，如 ``i2c1``、
   ``spi2`` 等。

按别名
   使用 :c:macro:`DT_ALIAS()` 获取特殊 ``/aliases`` 节点
   某个属性的节点标识符。应用有时会这样做（例如
   :zephyr:code-sample:`blinky`，它使用 ``led0`` 别名），
   需要引用*某个*特定类型的设备（"板子的用户 LED"）
   但不关心具体使用哪一个。
   你也可以使用 :c:macro:`DT_HAS_ALIAS()` 验证别名
   节点是否存在。

按实例编号
   这主要由设备驱动完成，因为实例编号是一种
   基于匹配的 compatible 引用单个节点的方式。用
   :c:macro:`DT_INST()` 获取，但这样做时要小心。见下文。

按 chosen 节点
   使用 :c:macro:`DT_CHOSEN()` 获取 ``/chosen`` 节点
   属性的节点标识符。

按父/子节点
   使用 :c:macro:`DT_PARENT()` 和 :c:macro:`DT_CHILD()` 获取
   父节点或子节点的节点标识符，从你已有的节点标识符开始。

引用同一节点的两个节点标识符是相同的，可以互换使用。

.. _dt-node-main-ex:

以下是一个虚构硬件的 DTS 片段，本文件将全程用它举例：

.. literalinclude:: main-example.dts
   :language: devicetree
   :start-after: start-after-here

以下是获取 ``i2c@40002000`` 节点节点标识符的几种方式：

- ``DT_PATH(soc, i2c_40002000)``
- ``DT_NODELABEL(i2c1)``
- ``DT_ALIAS(sensor_controller)``
- ``DT_INST(x, vnd_soc_i2c)``，其中 ``x`` 为某个未知编号。详见
  :c:macro:`DT_INST()` 文档。

.. important::

   设备树名称中的非字母数字字符（如连字符（``-``）和 at 符号（``@``））
   会被转换为下划线（``_``）。DTS 中的名称
   也会被转换为小写。

.. _node-ids-are-not-values:

节点标识符不是值
*******************************

没有办法把它存储在变量中。你不能写：

.. code-block:: c

   /* 这些会导致编译器错误： */

   void *i2c_0 = DT_INST(0, vnd_soc_i2c);
   unsigned int i2c_1 = DT_INST(1, vnd_soc_i2c);
   long my_i2c = DT_NODELABEL(i2c1);

如果你想要一个简短的形式以减少输入，使用 C 宏：

.. code-block:: c

   /* 改用类似这样的形式： */

   #define MY_I2C DT_NODELABEL(i2c1)

   #define INST(i) DT_INST(i, vnd_soc_i2c)
   #define I2C_0 INST(0)
   #define I2C_1 INST(1)

属性访问
***********************

读取属性值应使用哪个 API 取决于节点和属性。

- :ref:`dt-checking-property-exists`
- :ref:`simple-properties`
- :ref:`reg-properties`
- :ref:`interrupts-properties`
- :ref:`phandle-properties`

.. _dt-checking-property-exists:

检查属性与值
==============================

你可以使用 :c:macro:`DT_NODE_HAS_PROP()` 检查节点是否具有某个属性。
对于上面:ref:`示例设备树 <dt-node-main-ex>`：

.. code-block:: c

   DT_NODE_HAS_PROP(DT_NODELABEL(i2c1), clock_frequency)  /* 展开为 1 */
   DT_NODE_HAS_PROP(DT_NODELABEL(i2c1), not_a_property)   /* 展开为 0 */

.. _simple-properties:

简单属性
================

使用 ``DT_PROP(node_id, property)`` 读取基本的整数、布尔、字符串、
数值数组和字符串数组属性。

例如，读取上面:ref:`示例 <dt-node-main-ex>` 中 ``clock-frequency`` 属性的值：

.. code-block:: c

   DT_PROP(DT_PATH(soc, i2c_40002000), clock_frequency)  /* 这是 100000， */
   DT_PROP(DT_NODELABEL(i2c1), clock_frequency)          /* 这个也是， */
   DT_PROP(DT_ALIAS(sensor_controller), clock_frequency) /* 这个也是。 */

.. important::

   DTS 属性 ``clock-frequency`` 在 C 中拼写为 ``clock_frequency``。
   也就是说，属性名也需要将特殊字符转换为下划线。
   它们的名称也会被强制转为小写。

类型为 ``string`` 和 ``boolean`` 的属性工作方式完全相同。
对于字符串，``DT_PROP()`` 宏展开为字符串字面量；
对于布尔值，则展开为数字 0 或 1。例如：

.. code-block:: c

   #define I2C1 DT_NODELABEL(i2c1)

   DT_PROP(I2C1, status)  /* 展开为字符串字面量 "okay" */

.. note::

   不要对布尔属性使用 DT_NODE_HAS_PROP()。
   应改用上面所示的 DT_PROP()。
   它会根据属性是否存在展开为 0 或 1。

类型为 ``array``、``uint8-array`` 和 ``string-array`` 的属性
工作方式类似，只是这些情况下 ``DT_PROP()`` 展开为数组初始化器。
以下是一个设备树片段示例：

.. code-block:: devicetree

   foo: foo@1234 {
           a = <1000 2000 3000>; /* array */
           b = [aa bb cc dd];    /* uint8-array */
           c = "bar", "baz";     /* string-array */
   };

其属性可以这样访问：

.. code-block:: c

   #define FOO DT_NODELABEL(foo)

   int a[] = DT_PROP(FOO, a);           /* {1000, 2000, 3000} */
   unsigned char b[] = DT_PROP(FOO, b); /* {0xaa, 0xbb, 0xcc, 0xdd} */
   char* c[] = DT_PROP(FOO, c);         /* {"bar", "baz"} */

你可以使用 :c:macro:`DT_PROP_LEN()` 获取以元素数计的
逻辑数组长度。

.. code-block:: c

   size_t a_len = DT_PROP_LEN(FOO, a); /* 3 */
   size_t b_len = DT_PROP_LEN(FOO, b); /* 4 */
   size_t c_len = DT_PROP_LEN(FOO, c); /* 2 */

``DT_PROP_LEN()`` 不能用于特殊的 ``reg`` 或 ``interrupts``
属性。这些属性有替代宏，见下文。

.. _reg-properties:

reg 属性
================

``reg`` 的介绍见 :ref:`dt-important-props`。

给定节点标识符 ``node_id``，``DT_NUM_REGS(node_id)`` 是
节点 ``reg`` 属性中寄存器块的总数。

你**不能**用 ``DT_PROP(node,
reg)`` 读取寄存器块的地址和长度。相反，如果节点只有一个寄存器块，使用
:c:macro:`DT_REG_ADDR` 或 :c:macro:`DT_REG_SIZE`：

- ``DT_REG_ADDR(node_id)``：给定节点的寄存器块地址
- ``DT_REG_SIZE(node_id)``：其大小

如果节点有多个寄存器块，改用 :c:macro:`DT_REG_ADDR_BY_IDX` 或 :c:macro:`DT_REG_SIZE_BY_IDX`：

- ``DT_REG_ADDR_BY_IDX(node_id, idx)``：索引为
  ``idx`` 的寄存器块地址
- ``DT_REG_SIZE_BY_IDX(node_id, idx)``：索引为 ``idx`` 的块大小

这些宏的 ``idx`` 参数必须是整数字面量，
或展开为整数字面量且不需要任何算术运算的宏。
特别是，``idx`` 不能是变量。以下写法不可行：

.. code-block:: c

   /* 这会导致编译器错误。 */

   for (size_t i = 0; i < DT_NUM_REGS(node_id); i++) {
           size_t addr = DT_REG_ADDR_BY_IDX(node_id, i);
   }

.. _interrupts-properties:

interrupts 属性
=====================

``interrupts`` 的简要介绍见 :ref:`dt-important-props`。

给定节点标识符 ``node_id``，``DT_NUM_IRQS(node_id)`` 是
节点 ``interrupts`` 属性中中断说明符（interrupt specifier）的总数。

访问这些值最通用的 API 宏是
:c:macro:`DT_IRQ_BY_IDX`：

.. code-block:: c

   DT_IRQ_BY_IDX(node_id, idx, val)

这里，``idx`` 是 ``interrupts`` 数组的逻辑索引，即
属性中单个中断说明符的索引。``val``
参数是中断说明符内某个单元格的名称。要使用此
宏，请检查你所关心节点的绑定文件以找到
``val`` 名称。

大多数 Zephyr 设备树绑定都有一个名为 ``irq`` 的单元格，
即中断号。你可以使用 :c:macro:`DT_IRQN` 作为获取
该值处理后视图的便捷方式。

.. warning::

   这里的"处理后"对应 Zephyr 的设备树 :ref:`dt-scripts`，
   它会修改 :ref:`zephyr.dts <devicetree-in-out-files>` 中的 ``irq`` 号，
   以处理某些 SoC 上的硬件约束，并遵循 Zephyr 的
   多级中断编号。

   这部分目前文档不太完善，如果你在编写
   设备驱动，需要阅读脚本源代码和现有驱动以了解更多细节。

.. _phandle-properties:

phandle 属性
==================

.. note::

   phandle 的详细指南见 :ref:`dt-phandles`。

属性值可以使用 :ref:`dt-writing-property-values` 中介绍的
``&another-node`` phandle 语法引用其他节点。
包含 phandle 的属性在其绑定中的类型为 ``phandle``、``phandles`` 或 ``phandle-array``。
我们简称这些为"phandle 属性"。

你可以使用 :c:macro:`DT_PHANDLE`、
:c:macro:`DT_PHANDLE_BY_IDX` 或 :c:macro:`DT_PHANDLE_BY_NAME`
将 phandle 转换为节点标识符，
具体取决于你处理的属性类型。

phandle 属性的一种常见用例是引用树中的其他硬件。
在这种情况下，你通常想将设备树级别的
phandle 转换为 Zephyr 驱动级别的 :ref:`struct device <device_model_api>`。
做法见 :ref:`dt-get-device`。

另一种常见用例是访问 phandle 数组中的说明符值。
其通用 API 是 :c:macro:`DT_PHA_BY_IDX` 和 :c:macro:`DT_PHA`。
还有硬件特定的简写，如 :c:macro:`DT_GPIO_CTLR_BY_IDX`、
:c:macro:`DT_GPIO_CTLR`、
:c:macro:`DT_GPIO_PIN_BY_IDX`、:c:macro:`DT_GPIO_PIN`、
:c:macro:`DT_GPIO_FLAGS_BY_IDX` 和 :c:macro:`DT_GPIO_FLAGS`。

检查 phandle 属性中是否存在某个说明符值，
参见 :c:macro:`DT_PHA_HAS_CELL_AT_IDX` 和 :c:macro:`DT_PROP_HAS_IDX`。

.. _other-devicetree-apis:

其他 API
**********

以下是其他可用 API 的指引。

- :c:macro:`DT_CHOSEN`、:c:macro:`DT_HAS_CHOSEN`：用于
  特殊 ``/chosen`` 节点的属性
- :c:macro:`DT_HAS_COMPAT_STATUS_OKAY`、:c:macro:`DT_NODE_HAS_COMPAT`：
  与 ``compatible`` 属性相关的全局和节点特定测试
- :c:macro:`DT_BUS`：获取节点的总线控制器（如果存在）
- :c:macro:`DT_ENUM_IDX`：用于取值属于固定选项列表的属性
- :ref:`devicetree-flash-api`：管理固定 flash 分区和
  映射 flash 分区的 API。
  另见 :ref:`flash_map_api`，它以更用户友好的 API 封装了它。

设备驱动便捷宏
**************************

为编写设备驱动提供了专用宏，
它们通常依赖 :ref:`实例标识符 <dt-node-identifiers>`。

要使用这些宏，你必须将 ``DT_DRV_COMPAT`` 定义为你
驱动所实现支持的 ``compat`` 值。该 ``compat`` 值就是
传给 :c:macro:`DT_INST` 的值。

这样做后，你可以用更少的输入访问
你的 compatible 各个实例的属性，如下所示：

.. code-block:: c

   #include <zephyr/devicetree.h>

   #define DT_DRV_COMPAT my_driver_compat

   /* 这与 DT_INST(0, my_driver_compat) 相同： */
   DT_DRV_INST(0)

   /*
    * 这与
    * DT_PROP(DT_INST(0, my_driver_compat), clock_frequency)
    * 相同
    */
   DT_INST_PROP(0, clock_frequency)

通用 API 参考见 :ref:`devicetree-inst-apis`。

硬件特定 API
**********************

还在上述 API 之上定义了便捷宏，
以帮助提高硬件特定代码的可读性。详见 :ref:`devicetree-hw-api`。

生成的宏
****************

虽然 :file:`zephyr/devicetree.h` API 不是生成的，但它依赖于
一个生成的 C 头文件，该文件被放入每个应用构建目录：
:ref:`devicetree_generated.h <dt-outputs>`。该文件包含带有
设备树数据的宏。

这些宏的命名约定比较复杂，:ref:`devicetree_api` API
对其做了抽象。应将其视为实现细节，但了解它们很有用，
因为它们经常出现在编译器错误信息中。

本节包含这些生成宏的扩充巴科斯-诺尔范式（ABNF）文法，
注释中附有示例和更多细节。语法规范见 :rfc:`7405`
（它扩展了 :rfc:`5234`）。

.. literalinclude:: macros.bnf
   :language: abnf
