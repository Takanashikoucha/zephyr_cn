.. _dt-design:

设计目标
############

Zephyr 对设备树的使用随时间发生了显著变化，
并且预计还会有进一步变化。以下是
通用设计目标，以及关于它们如何影响 Zephyr
源代码的具体示例，
还有仍需完成工作的领域。

硬件信息的单一来源
**************************************

Zephyr 内置的设备驱动和示例应用应
从设备树获取可配置的硬件描述。

示例
========

- 新的设备驱动应使用设备树 API 确定要创建哪些 :ref:`设备
  <dt-create-devices>`。

- 树内示例应用应使用 :ref:`别名 <dt-alias-chosen>`
  确定给定类型的多个可能通用设备中
  当前构建将使用哪一个。例如，:zephyr:code-sample:`blinky` 示例
  用它来确定要闪烁的 LED。

- 新 SoC 的启动时引脚复用和引脚控制应通过
  基于设备树的 pinctrl 驱动实现

示例剩余工作
=====================

- Zephyr 的 :ref:`twister_script` 当前使用 :file:`board.yaml` 文件
  确定开发板支持的硬件。这应
  改为从设备树获取。

- 传统设备驱动当前使用 Kconfig 确定
  特定 compatible 的哪些实例被启用。
  这可以也应该用设备树
  覆盖（overlay）来完成。

- 开发板级文档仍包含手工
  生成和维护的硬件支持表格。
  这可以也应该从
  开发板级设备树获取。

- ``struct device`` 关系的运行时确定应使用
  从设备树获取的信息完成，
  例如用于设备电源管理。

.. _dt-source-compatibility:

与其他操作系统的源码兼容性
*************************************************

Zephyr 的设备树工具基于一个通用层，
该层可与其他设备树使用者（如 Linux 内核）
互操作。

Zephyr 绑定语言的*语义*可以支持
Zephyr 特定属性，
但不应表达 Zephyr 特定关系。

示例
========

- Zephyr 的设备树源码解析器 :ref:`dtlib.py <dt-scripts>`
  与 `dtc`_ 等其他工具双向
  源码兼容：
  :file:`dtlib.py` 可以解析 ``dtc`` 输出，
  ``dtc`` 可以解析
  :file:`dtlib.py` 输出。

- Zephyr 的"扩展 dtlib"库 :file:`edtlib.py`
  不应包含
  Zephyr 特定功能。其目的是为
  中断和总线等通用元素提供
  设备树的高层视图。

  只有构建在
  :file:`edtlib.py` 之上的高层 :file:`gen_defines.py` 脚本
  包含 Zephyr 特定知识和功能。

.. _dtc: https://git.kernel.org/pub/scm/utils/dtc/dtc.git/about/

示例剩余工作
=====================

- Zephyr 有自定义的 :ref:`dt-bindings` 语言*语法*。虽然 Linux 的
  dtschema 尚不满足 Zephyr 的需求，
  但应尝试在 Zephyr 自己的绑定中遵循
  它能表示的内容。

- 由于绑定语言不够灵活，Zephyr 无法支持
  Linux 支持的完整绑定集合。

- Zephyr 与 Linux 之间的设备树源码共享
  尚未实现。

.. _dt-multi-api-hardware:

建模通过多个 Zephyr API 暴露的硬件
******************************************************

当硬件块可以通过不同的 Zephyr API 使用时，
设备树应将硬件身份与软件驱动和
子系统使用每个硬件实例的方式分开。

指南
==========

- 让 ``compatible`` 属性专注于设备编程模型。
  避免仅为了路由软件 API 选择而更改它。
  当硬件接口在架构上
  明显不同时（例如使用独立的寄存器
  块），使用不同的 ``compatible`` 是合适的。

- 使用 ``/chosen`` 进行单例系统级选择。
  如果系统必须为全局功能（如
  系统定时器、控制台或熵源）选择恰好一个实例，
  用平台无关的
  chosen 属性表示该选择，即使
  其他相同的硬件实例被
  其他 API 使用。另见 :ref:`devicetree-zephyr-chosen-nodes`。

- 在正确的集成层级放置选择。
  如果它是硅片级
  固定属性，在 SoC ``.dtsi`` 中描述。
  如果它因开发板、
  产品或应用而异，在开发板 ``.dts`` 或覆盖文件中描述。

如果硬件设备的不同用途具有
不同的必需
属性、子节点或总线语义，则它们不必共享
一个绑定模式。在这种情况下，使用不同的 ``compatible`` 值
或将设备建模为多功能设备。

示例
========

**使用 ``/chosen`` 的单例选择**

系统定时器是单例功能。``zephyr,system-timer``
chosen 属性选择哪个硬件定时器实例
提供它，而其他相同实例
仍可供其他 API 使用。

例如，两个相同的 LPTMR 定时器实例
可以在硬件描述中共享相同的
``compatible``：

.. code-block:: devicetree

   lptmr1: timer@44300000 {
       compatible = "nxp,lptmr";
       reg = <0x44300000 0x1000>;
       /* ... */
   };

   lptmr2: timer@424d0000 {
       compatible = "nxp,lptmr";
       reg = <0x424d0000 0x1000>;
       /* ... */
   };

集成层然后可以选择哪个提供单例系统
定时器功能：

.. code-block:: devicetree

   / {
       chosen {
           zephyr,system-timer = &lptmr1;
       };
   };

system-timer 驱动绑定到 ``/chosen`` 节点。
counter 驱动跳过该实例并使用
剩余的那个。
