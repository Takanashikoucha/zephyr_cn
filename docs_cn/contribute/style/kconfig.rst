.. _kconfig_style:

Kconfig 风格指南
########################

本文档提供 Zephyr 项目中编写 Kconfig 文件的风格指南。
遵循这些指南可确保整个代码库的一致性和可读性，
帮助开发者更容易地理解和维护配置选项。

以下各节提供带示例的指南，用于说明正确的
Kconfig 格式和命名约定。


基本格式规则
**********************

编写 Kconfig 文件时，遵循以下基本格式规则：

* **行长度**：保持行在 100 列或更少。
* **缩进**：使用制表符进行缩进，``help`` 条目文本除外，
  后者应放置在一个制表符再加两个空格的位置。
* **间距**：在选项声明之间保留一个空行。
* **注释**：注释应写成 ``# Comment`` 而不是 ``#Comment``。
* **条件块**：在每个顶层 ``if`` 和 ``endif`` 语句的前/后
  插入一个空行。
* **文件结尾**：文件以一个（且仅一个）换行符结尾。

有关如何使用 ``select`` 等语句，参见
:ref:`kconfig_tips_and_tricks` 以获取更多信息。

这些格式规则由 CI 中的 ``KconfigFormat`` 合规检查强制执行。
你可以使用 ``scripts/kconfig/kconfig_style.py`` 脚本在本地
检查 Kconfig 文件，它会报告所有风格问题
（目录会被递归搜索以查找 Kconfig 文件）：

.. code-block:: console

   ./scripts/kconfig/kconfig_style.py path/to/Kconfig
   ./scripts/kconfig/kconfig_style.py drivers/sensor/

符号命名和结构
***************************

以下示例展示了正确的 Kconfig 符号命名和结构：

.. literalinclude:: kconfig_demo_simple.txt
   :language: kconfig
   :start-after: start-after-here

.. literalinclude:: kconfig_demo_complex.txt
   :language: kconfig
   :start-after: start-after-here


命名约定
******************

* 作为一般规则，涉及同一组件的符号应与其他符号
  有所区分。这通常通过使用一个公共前缀来实现。
  此前缀可以是一个简单关键字，或者（如驱动的情况）
  由多个关键字组成以获得更精确的区分。

* 公共前缀通常指示符号所属的子系统或组件。

* 使能符号的名称应由一系列关键字组成，从最一般到最
  具体的范围提供该符号的上下文（例如 *驱动类型* ->
  *驱动名称*）。

* 使能符号的 prompt 应使用与符号名称相同的逻辑，
  但关键字顺序相反。

   * 遵循这种风格可以让在 UI 中搜索符号更容易，
     因为可以按某个范围关键字进行过滤。

* 当使能符号依赖于设备树节点时，考虑依赖
  :ref:`自动创建的 <auto-dts-kconfig>`
  ``DT_HAS_<node>_ENABLED`` 符号。

* 当基于设备树节点的 compatible 构建复杂表达式时，
  使用 :ref:`自动定义的 <auto-dts-kconfig>`
  :samp:`DT_COMPAT_{VND_DEVICE}`，而不是手动定义一个
  等于 :samp:`{vnd,device}` 的变量。

按子树的具体格式：

* **驱动（/drivers）**：符号使用 ``{驱动类型}_{驱动名称}``
  格式，prompt 使用 ``{驱动名称} {驱动类型} driver``。

* **传感器（/drivers/sensors）**：符号使用
  ``SENSOR_{传感器名称}`` 格式，prompt 使用
  ``{传感器名称} {传感器类型} sensor driver``。

* **架构（/arch）**：许多符号跨架构共享。在创建新符号之前，检查其他架构中是否已经存在类似的符号。

* **示例（/samples）**：符号使用 ``SAMPLE_`` 前缀，
  以防止与外部模块冲突。

* **测试（/tests）**：符号使用 ``TEST_`` 前缀，
  以防止与外部模块冲突。

* **板级（/boards）**：符号使用 ``BOARD_`` 前缀。

* **SoC（/soc）**：为符号选择最合适的基础前缀：
  如果涉及某 SoC 供应商的多个系列，使用
  ``SOC_VENDOR_{SoC 供应商}_``；如果涉及整个 SoC 系列
  （family），使用 ``SOC_FAMILY_{SoC 系列}_``；如果涉及
  整个 SoC 产品线（series），使用
  ``SOC_SERIES_{SoC 产品线}_``；如果只涉及某个具体的
  SoC，则使用 ``SOC_{SoC}_``——这些术语的含义及其
  来源参见 :ref:`soc_porting_guide`。这是为了防止
  与其他供应商和外部模块冲突。

示例
========

.. note::

   为简洁起见，以下示例仅展示符号和 prompt 行。

**驱动示例：**

.. literalinclude:: kconfig_example_driver.txt
   :language: kconfig
   :start-after: start-after-here

**传感器示例：**

.. literalinclude:: kconfig_example_sensor.txt
   :language: kconfig
   :start-after: start-after-here

**示例（Sample）：**

.. literalinclude:: kconfig_example_sample.txt
   :language: kconfig
   :start-after: start-after-here

**测试：**

.. literalinclude:: kconfig_example_test.txt
   :language: kconfig
   :start-after: start-after-here

**SoC：**

.. literalinclude:: kconfig_example_soc.txt
   :language: kconfig
   :start-after: start-after-here

配置符号组织
*********************************

当某个功能使用配置符号（config symbol）来配置其行为时：

* 使用 ``menuconfig`` 而不是 ``config`` 来定义使能该
  功能的符号（即使该配置符号没有 prompt）。

* 用 ``if`` 语句将这些配置符号封装起来，以声明它们
  对使能符号的依赖（这会自动在 UI 中把这些符号
  分组到使能符号之下）。

* 配置符号的名称应以使能符号的名称作为前缀，
  以表明其范围和上下文。

* 在配置符号的 prompt 中，描述该符号所配置的内容，
  不要重复范围关键字，因为 UI 中的分组已经提供了
  这一上下文。

文件组织
*****************

当组织 Kconfig 文件时：

* 让 Kconfig 文件尽量靠近它所配置的源文件。

* 处理大型 Kconfig 文件（例如包含许多配置符号）时，
  考虑将其中（部分）符号分组到一个单独的文件中，
  并使用 ``source`` 指令导入，以提高可读性。
