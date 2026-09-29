.. _dt-writing-bindings:

上游绑定规则
###########################

本节包含编写希望提交到上游 Zephyr Project 的绑定的
通用规则。（对于你不打算贡献给 Zephyr Project 的绑定，
无需遵循这些规则，但遵循是个好主意。）

Zephyr 设备树维护者做出的决定优先于
本节内容。如果发生这种情况，请让他们知道，
以便他们更新此页面，或者你自己发送补丁。

.. contents:: 目录
   :local:

始终检查现有绑定
******************

Zephyr 追求设备树 :ref:`dt-source-compatibility`。因此，如果
你的设备在权威位置已有现有绑定，编写 Zephyr 绑定时
应尝试复制其属性，并且必须
为任何 Zephyr 特定的偏离提供正当理由。

特别是，以下情况适用此规则：

- 主线 Linux 内核中已有现有绑定。现有
  绑定见 `Linus 的树`_ 中的 :file:`Documentation/devicetree/bindings`，
  更多信息见 `Linux 设备树文档`_。

- 你的硬件厂商在 Linux 内核之外提供了官方绑定。

.. _Linus 的树:
   https://github.com/torvalds/linux/

.. _Linux 设备树文档:
   https://www.kernel.org/doc/html/latest/devicetree/index.html

通用规则
*************

编写 Zephyr 的设备树绑定时，尽可能
遵循 `Linux 制定的设计指南`_。

.. _Linux 制定的设计指南:
   https://docs.kernel.org/devicetree/bindings/writing-bindings.html

文件名
==========

匹配 compatible 的绑定必须有基于 compatible 的文件名。

- 例如，compatible ``vnd,foo`` 的绑定必须命名为 ``vnd,foo.yaml``。
- 如果绑定是总线特定的，可以在文件名后附加总线；
  例如，如果绑定 YAML 有 ``on-bus: bar``，
  可以将文件命名为 ``vnd,foo-bar.yaml``。

建议即要求
=====================

提交绑定时，:ref:`dt-bindings-default` 中的所有建议
都是要求。

特别是，如果使用 ``default:`` 功能，
必须在属性描述中为
该值提供正当理由。

描述（Descriptions）
==================

编写属性 ``description:``
字符串只有两种可接受的方式。

如果描述较短，可以使用这种风格：

.. code-block:: yaml

   description: my short string

如果描述较长或跨多行，必须使用
这种风格：

.. code-block:: yaml

   title: 我相信你需要一个简短标题。

   description: |
     My very long string
     goes here.
     Look at all these lines!

这种 ``|`` 风格防止 YAML 解析器
去除多行描述中的换行符。这进而使这些长字符串
在 :ref:`devicetree_binding_index` 中正确显示。

如果使用绑定的属性变得复杂，
可以用示例提供一个最小节点。例如：

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

命名约定
==================

属性名中不要使用大写字母（``A`` 到 ``Z``）
或下划线（``_``）。用小写字母（``a`` 到 ``z``）
替代大写。用连字符（``-``）替代下划线。（此规则的唯一
例外是你正在复制来自 Linux 等地方
的成熟绑定。）

厂商前缀规则
*************************

以下通用规则适用于 :ref:`compatible
<dt-important-props>` 属性中的厂商前缀。

- 如果你的设备由特定厂商制造，
  其 compatible 应有厂商前缀。

  如果你的绑定描述的是
  :zephyr_file:`dts/bindings/vendor-prefixes.txt` 列表中
  知名厂商的硬件，必须使用该厂商
  前缀。

- 如果你的设备不是由特定硬件厂商制造，**不要**
  发明厂商前缀。厂商前缀不是 compatible
  属性的强制部分，除非引用实际厂商，
  compatible 不应包含它们。此规则有一些例外，
  但强烈不推荐这种做法。

- 除非同时包含新前缀的使用者，
  否则不要向 Zephyr 的 :file:`dts/bindings/vendor-prefixes.txt`
  文件提交添加内容。这意味着至少
  一个使用该厂商前缀的绑定和设备树，
  理想情况下还应包含
  处理该 compatible 的设备驱动。

  对于自定义绑定，可以在
  :ref:`DTS_ROOT <dts_root>` 的任何目录中添加自定义
  :file:`dts/bindings/vendor-prefixes.txt` 文件。设备树工具
  会尊重这些
  前缀，在自己的绑定或设备树中使用它们时
  不会生成警告或错误。

- 有时我们会将 Zephyr 的 vendor-prefixes.txt 文件
  与 Linux 内核的对应文件同步；此过程
  不受前一条规则约束。

- 如果你的绑定描述的是由 Zephyr
  特定驱动处理节点的抽象硬件类别，
  通常最好使用 ``zephyr`` 作为
  厂商前缀。示例见 :ref:`dt_vendor_zephyr`。

.. _dt-bindings-default-rules:

默认值规则
************************

在任何使用 ``default:`` 的设备树绑定中，
该属性的 ``description:`` **必须**解释*为什么*
选择该值，以及任何需要
提供不同值的条件。此外，如果更改一个属性
需要同时更改另一个属性才能
创建一致的配置，则这些属性应设为
必需。

无需记录默认值本身；它已经
存在于 :ref:`devicetree_binding_index` 输出中。

当绑定中的值对特定开发板或硬件配置
可能不正确时，使用 ``default:`` 存在风险。例如，
在充电 IC 绑定中为连接的电源电池容量设置默认值
很可能不正确。对于此类属性，
最好将属性设为 ``required: true``，
强制用户做出明确选择。

驱动开发者应自行判断值是否可以
安全地设置默认值。默认值的候选包括：

- 仅在异常条件下（如中间硬件）
  才会不同的延时
- 具有标准初始配置的设备配置（如
  USB 音频耳机）
- 与厂商指定的上电复位值匹配的默认值
  （只要它们独立于其他属性）

``status``、``#address-cells`` 和 ``#size-cells`` 的默认值
不能在绑定中定义。这些属性的默认行为
已在设备树规范 `§2.3.4 <https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html#status>`_ 和 `§2.3.5 <https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html#address-cells-and-size-cells>`_ 中定义。

按这些规则编写描述的示例：

.. code-block:: yaml

   properties:
     cs-interval:
       type: int
       default: 0
       description: |
         片选取消有效与有效之间的最小间隔。
         默认值对应寄存器字段的复位值。
     hold-time-ms:
       type: int
       default: 20
       description: |
         在发起通信前保持电源使能 GPIO 有效的时间。
         默认值来自制造商数据手册的推荐，
         仅在极低温下才会改变。

一些**不要**做的示例及原因：

.. code-block:: yaml

   properties:
     # 描述未提及默认值
     foo:
       type: int
       default: 1
       description: number of foos

     # 描述提及默认值而非
     # 为什么选择它
     bar:
       type: int
       default: 2
       description: bar size; default is 2

     # 默认值的解释在注释中而非
     # 描述中。这不会显示在绑定索引中。
     baz:
       type: int
       # This is the recommended value chosen by the manufacturer.
       default: 2
       description: baz time in milliseconds

``zephyr,`` 前缀
**********************

以下情况必须在属性名中添加此前缀：

- 与上游 Linux 共享的绑定的 Zephyr 特定扩展。
  一个示例是 ``zephyr,vref-mv`` ADC 通道属性，
  它是 :zephyr_file:`dts/bindings/adc/adc-controller.yaml`
  中定义的 ADC 控制器的通用属性。
  该通道绑定与类似的 Linux 绑定部分共享，
  Zephyr 特定扩展用此前缀标记。

- 特定于 Zephyr 设备驱动的配置值。一个示例
  是 :dtcompatible:`ti,bq274xx`
  绑定中的 ``zephyr,lazy-load`` 属性。虽然设备树
  总体上是硬件描述和
  配置语言，但它是 Zephyr 为单个 ``struct device``
  配置驱动行为的唯一机制。因此，作为折衷，
  我们允许 Zephyr 设备树绑定中有一些软件配置，
  只要它们使用此前缀表明它们是 Zephyr 特定的。

在为特定于 Zephyr 的设备树 compatible 命名时
可以使用 ``zephyr,`` 前缀。一个示例是
:dtcompatible:`zephyr,ipc-openamp-static-vrings`。在这种情况下，
允许但不要求
为绑定中定义的属性添加 ``zephyr,`` 前缀。
