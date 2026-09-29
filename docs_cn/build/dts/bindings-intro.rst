.. _dt-binding-compat:

设备树绑定简介
###################################

.. note::

   详细的语法参考见 :ref:`dt-bindings-file-syntax`。

设备树节点通过其 :ref:`compatible
属性 <dt-important-props>` 与绑定匹配。

在 :ref:`build_configuration_phase` 期间，构建系统尝试将
设备树中的每个节点与一个绑定文件匹配。匹配成功时，构建
系统使用绑定文件中的信息来验证节点的内容，
并为该节点生成宏。

.. _dt-bindings-simple-example:

一个简单的示例
****************

以下是一个设备树节点示例：

.. code-block:: devicetree

   /* DTS 文件中的节点 */
   bar-device {
   	compatible = "foo-company,bar-device";
       num-foos = <3>;
   };

以下是与该节点匹配的最小绑定文件：

.. code-block:: yaml

   # 与节点匹配的 YAML 绑定

   compatible: "foo-company,bar-device"

   properties:
     num-foos:
       type: int
       required: true

构建系统将 ``bar-device`` 节点与其 YAML 绑定匹配，
因为节点的 ``compatible`` 属性与绑定的 ``compatible:`` 行匹配。

构建系统如何使用绑定
****************************************

构建系统使用绑定来验证设备树节点，
并将设备树的内容转换为生成的 :ref:`devicetree_generated.h
<dt-outputs>` 头文件。

例如，构建系统会使用上面的绑定检查
必需的 ``num-foos`` 属性是否存在于 ``bar-device`` 节点中，
且其值 ``<3>`` 具有正确的类型。

然后构建系统会为 ``bar-device`` 节点的
``num-foos`` 属性生成一个宏，该宏展开为整数字面量 ``3``。
该宏让你能在 C 代码中通过本指南后面
:ref:`dt-from-c` 讨论的 API 获取属性值。

再举一个例子，以下节点会导致构建错误，
因为它没有 ``num-foos`` 属性，而该属性在绑定中标记为必需：

.. code-block:: devicetree

   bad-node {
   	compatible = "foo-company,bar-device";
   };

节点与绑定的其他匹配方式
****************************************

如果节点的 ``compatible`` 属性包含多个字符串，构建
系统按列出的顺序查找 compatible 绑定并使用第一个
匹配项。

以这个节点为例：

.. code-block:: devicetree

   baz-device {
   	compatible = "foo-company,baz-device", "generic-baz-device";
   };

如果构建系统找不到带有
``compatible: "foo-company,baz-device"`` 行的绑定，
``baz-device`` 节点就会与带有 ``compatible:
"generic-baz-device"`` 行的绑定匹配。

没有 compatible 属性的节点可以与其父节点关联的绑定匹配。
这些称为"子绑定"（child bindings）。如果节点描述
总线上的硬件（如 I2C 或 SPI），则在将节点与绑定匹配时
也会考虑总线类型。（详见 :ref:`dt-bindings-on-bus`）。

关于一个不需要任何绑定的特殊节点的信息，
见 :ref:`dt-zephyr-user`。

.. _dt-where-bindings-are-located:

绑定的位置
**************************

绑定文件名通常与其 ``compatible:`` 行匹配。例如，
按惯例，上面的示例绑定将命名为 :file:`foo-company,bar-device.yaml`。

构建系统在以下位置的 :file:`dts/bindings`
子目录中查找绑定：

- zephyr 仓库
- 你的 :ref:`应用源目录 <application>`
- 你的 :ref:`开发板目录 <board_porting_guide>`
- 任何 :ref:`shield 目录 <shields>`
- 任何手动包含在 :ref:`DTS_ROOT <dts_root>`
  CMake 变量中的目录
- 任何在其 :ref:`modules_build_settings` 中定义了
  ``dts_root`` 的 :ref:`模块 <modules>`

将节点与绑定匹配时，构建系统会考虑上述任何位置
（包括任何子目录）中的任何 YAML 文件。文件名以 ``.yaml`` 或 ``.yml``
结尾的文件被视为 YAML 文件。

.. warning::

   绑定文件必须位于上述位置的 :file:`dts/bindings`
   子目录内部的某个地方。

   例如，如果 :file:`my-app` 是你的应用目录，则必须
   将应用特定的绑定放在 :file:`my-app/dts/bindings` 内。因此
   :file:`my-app/dts/bindings/serial/my-company,my-serial-port.yaml` 会被
   找到，但 :file:`my-app/my-company,my-serial-port.yaml` 会被忽略。
