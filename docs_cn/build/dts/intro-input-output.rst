.. _devicetree-in-out-files:

输入与输出文件
######################

本节更详细地描述
:ref:`devicetree-scope-purpose` 中图表所示的
输入和输出文件。

.. figure:: zephyr_dt_inputs_outputs.svg
   :figclass: align-center

   设备树输入（绿色）与输出（黄色）文件

.. _dt-input-files:

输入文件
***********

有四种类型的设备树输入文件：

- 源文件（``.dts``）
- 包含文件（``.dtsi``）
- 覆盖文件（``.overlay``）
- 绑定（``.yaml``）

:file:`zephyr` 目录中的设备树文件如下所示：

.. code-block:: none

  boards/<ARCH>/<BOARD>/<BOARD>.dts
  dts/common/skeleton.dtsi
  dts/<ARCH>/.../<SOC>.dtsi
  dts/bindings/.../binding.yaml

一般来说，每个受支持的
开发板都有一个描述其硬件的 :file:`BOARD.dts` 文件。
例如，``reel_board`` 有 :zephyr_file:`boards/phytec/reel_board/reel_board.dts`。

:file:`BOARD.dts` 包含一个或多个 ``.dtsi`` 文件。
这些 ``.dtsi`` 文件描述 Zephyr 运行的 CPU 或片上系统（SoC），
可能通过包含其他 ``.dtsi`` 文件。
它们还可以描述多个开发板共享的其他通用硬件特性。
除这些包含外，:file:`BOARD.dts` 还描述开发板的特定硬件。

:file:`dts/common` 目录包含 :file:`skeleton.dtsi`，
一个用于定义完整设备树的最小包含文件。
架构特定的子目录（:file:`dts/<ARCH>`）包含
用于扩展 :file:`skeleton.dtsi` 的 CPU 或 SoC 的 ``.dtsi`` 文件。

C 预处理器在所有设备树文件上运行以展开宏引用，
包含通常通过 ``#include <filename>`` 指令完成，
尽管 DTS 有 ``/include/ "<filename>"`` 语法。

:file:`BOARD.dts` 可以使用*覆盖*（overlay）
扩展或修改。覆盖也是 DTS 文件；:file:`.overlay` 扩展
只是使其目的明确的约定。覆盖将基础设备树适配用于不同目的：

- Zephyr 应用可以使用覆盖启用默认禁用的外设、
  为应用特定目的选择板上的传感器等。
  与 :ref:`kconfig` 一起，
  这使得无需修改源代码即可重新配置
  内核和设备驱动成为可能。

- 覆盖也用于定义 :ref:`shields`。

构建系统自动拾取存储在特定位置的 :file:`.overlay` 文件。
也可以通过 :makevar:`DTC_OVERLAY_FILE` CMake 变量
显式列出要包含的覆盖。详见 :ref:`set-devicetree-overlays`。

构建系统通过拼接 :file:`BOARD.dts` 和任何 :file:`.overlay` 文件
（覆盖放在最后）来组合它们。这依赖于允许
合并设备树中重叠节点定义的 DTS 语法。
工作原理示例见 :ref:`dt_k6x_example`（
在 ``.dtsi`` 文件的上下文中，但覆盖的原则相同）。
将 :file:`.overlay` 文件的内容放在最后
允许它们覆盖 :file:`BOARD.dts`。

:ref:`dt-bindings`（它们是 YAML 文件）
本质上是胶水。它们以允许
构建系统生成设备驱动和应用可用的 C 宏的方式描述
设备树源文件、包含文件和覆盖文件的内容。
:file:`dts/bindings` 目录包含绑定。

.. _dt-scripts:

脚本与工具
*****************

以下位于 :zephyr_file:`scripts/dts/` 的
库和脚本从输入文件创建输出文件。
其源代码有大量文档。

:zephyr_file:`dtlib.py <scripts/dts/python-devicetree/src/devicetree/dtlib.py>`
    低层 DTS 解析库。

:zephyr_file:`edtlib.py <scripts/dts/python-devicetree/src/devicetree/edtlib.py>`
    构建在 dtlib 之上、使用绑定
    解释属性并提供设备树高层视图的库。
    使用 dtlib 完成 DTS 解析。

:zephyr_file:`gen_defines.py <scripts/dts/python-devicetree/src/devicetree/edtlib.py>`
    使用 edtlib 从设备树和绑定生成
    C 预处理器宏的脚本。

此外，如果标准 ``dtc``（设备树编译器）工具
安装在你的系统上，它会在最终设备树上运行。
这只是为了捕获错误或警告。输出未被使用。
开发板可能需要向 ``dtc`` 传递额外标志，
例如用于警告抑制。
开发板目录可以包含
名为 :file:`pre_dt_board.cmake` 的文件
来配置这些额外标志，如下所示：

.. code-block:: cmake

   list(APPEND EXTRA_DTC_FLAGS "-Wno-simple_bus_reg")

Shield 目录可以包含
名为 :file:`pre_dt_shield.cmake` 的文件，
其功能与上述 :file:`pre_dt_board.cmake` 相同。

.. _dt-outputs:

输出文件
************

这些在你的应用构建目录中创建。

.. warning::

   不要直接包含头文件。:ref:`dt-from-c` 解释
   应改为做什么。

:file:`<build>/zephyr/zephyr.dts.pre`
    预处理后的 DTS 源。
    这是一个中间输出文件，
    是 :file:`gen_defines.py` 的输入，
    用于创建 :file:`zephyr.dts` 和 :file:`devicetree_generated.h`。

:file:`<build>/zephyr/include/generated/zephyr/devicetree_generated.h`
    生成的宏和描述设备树的附加注释。
    被 ``devicetree.h`` 包含。

:file:`<build>/zephyr/zephyr.dts`
    最终合并的设备树。
    该文件由 :file:`gen_defines.py` 输出。
    它对于调试任何问题很有用。
    如果安装了设备树编译器 ``dtc``，
    它也会在此文件上运行，
    以捕获任何附加警告或错误。
