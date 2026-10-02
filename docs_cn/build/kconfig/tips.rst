.. _kconfig_tips_and_tricks:

Kconfig - 技巧与最佳实践
#################################

本页覆盖一些 Kconfig 最佳实践并解释一些 Kconfig 行为和功能，它们可能晦涩或
容易被忽略。

.. note::

   官方 Kconfig 文档是 `kconfig-language.rst
   <https://www.kernel.org/doc/html/latest/kbuild/kconfig-language.html>`__
   和 `kconfig-macro-language.rst
   <https://www.kernel.org/doc/html/latest/kbuild/kconfig-macro-language.html>`__。

.. contents::
   :local:
   :depth: 2


什么应该变成 Kconfig 选项
*************************

决定某事是否属于 Kconfig 时，区分有 prompt 的符号和没有的符号很有帮助。

如果符号有 prompt（例如 ``bool "Enable foo"``），那么用户可以在
``menuconfig`` 或 ``guiconfig`` 接口（见 :ref:`menuconfig`）中更改符号的值，
或通过手动编辑配置文件。相反，没有 prompt 的符号永远不能被用户直接更改，
即使通过手动编辑配置文件。

只在用户更改其值有意义时才给符号加 prompt。

没有 prompt 的符号称为 *隐藏* 或 *不可见* 符号，因为它们不显示在
``menuconfig`` 和 ``guiconfig`` 中。有 prompt 的符号也可以不可见，当其依赖
未满足时。

没有 prompt 的符号不能被用户直接配置（它们的值来自其他符号），因此对它们适用
的限制更少。如果某个派生设置在 Kconfig 中计算比例如在构建期间更容易，那么在
Kconfig 中做，但记住有 prompt 和没有 prompt 的符号之间的区别。

见 `optional prompts`_ 章节了解处理某些机器上固定而其他机器上可配置的设置
的方式。

什么不应变成 Kconfig 选项
*****************************

在 Zephyr 中，Kconfig 配置在选择目标开发板后完成。一般来说，使用 Kconfig 处理
对应固定的机器特定设置的值没有意义。通常，这种设置应该通过
:ref:`设备树 <dt-guide>` 处理。

特别避免添加以下类型的新 Kconfig 选项：

指定系统中设备名称的选项
===================================================

例如，如果你在编写 I2C 设备驱动，避免创建名为 ``MY_DEVICE_I2C_BUS_NAME`` 的
选项来指定控制你的设备的总线节点。替代方案见 :ref:`dt-drivers-that-depend`。

类似地，如果你的应用依赖硬件特定的 PWM 设备来控制 RGB LED，避免创建像
``MY_PWM_DEVICE_NAME`` 这样的选项。替代方案见 :ref:`dt-apps-that-depend`。

指定固定硬件配置的选项
================================================

例如，避免指定 GPIO 引脚的 Kconfig 选项。

适用于设备驱动的替代方案是在设备绑定中定义类型为 phandle-array 的 GPIO 说明符，
并从 C 使用 :ref:`devicetree-gpio-api` 设备树 API。类似建议适用于其他
devicetree.h 提供 :ref:`devicetree-hw-api` 引用系统中其他节点的情况。在源代码
中搜索使用这些 API 的驱动查找示例。

应用特定的设备树 :ref:`绑定 <dt-bindings>` 来标识开发板特定属性可能合适。示例
见 :zephyr_file:`tests/drivers/gpio/gpio_basic_api`。

对于应用，见 :zephyr:code-sample:`blinky` 了解基于设备树的替代方案。

``select`` 语句
*********************

``select`` 语句用于每当另一个符号为 ``y`` 时强制一个符号为 ``y``。例如，以下
代码在 ``USB_CONSOLE`` 为 ``y`` 时强制 ``CONSOLE`` 为 ``y``：

.. code-block:: kconfig

   config CONSOLE
   	bool "Console support"

   ...

   config USB_CONSOLE
   	bool "USB console support"
   	select CONSOLE

本节覆盖 ``select`` 的一些陷阱和良好用法。


``select`` 陷阱
================

``select`` 一开始可能看起来像通用有用的功能，但过度使用可能导致配置问题。

例如，假设上面的 ``CONSOLE`` 符号被一个不知道 ``USB_CONSOLE`` 符号（或简单
忘了）的开发者添加了一个新依赖：

.. code-block:: kconfig

   config CONSOLE
   	bool "Console support"
   	depends on STRING_ROUTINES

现在启用 ``USB_CONSOLE`` 会强制 ``CONSOLE`` 为 ``y``，即使 ``STRING_ROUTINES``
为 ``n``。

要修复问题，``STRING_ROUTINES`` 依赖也需要添加到 ``USB_CONSOLE``：

.. code-block:: kconfig

   config USB_CONSOLE
   	bool "USB console support"
   	select CONSOLE
   	depends on STRING_ROUTINES

   ...

   config STRING_ROUTINES
   	bool "Include string routines"

从 ``if`` 和 ``menu`` 语句继承依赖的更隐蔽情况很常见。

尝试解决问题的另一种方式可能是将 ``depends on`` 变成另一个 ``select``：

.. code-block:: kconfig

   config CONSOLE
   	bool "Console support"
   	select STRING_ROUTINES

   ...

   config USB_CONSOLE
   	bool "USB console support"
   	select CONSOLE

在实践中，这往往会放大问题，因为添加到 ``STRING_ROUTINES`` 的任何依赖现在都需要
复制到 ``CONSOLE`` 和 ``USB_CONSOLE`` 两者。

一般来说，每当符号的依赖被更新时，所有（直接或间接）选择它的符号的依赖也都必须
被更新。这在实践中经常被忽略，即使对于上面最简单的情况。

符号互相选择的链应特别避免，除了下面 :ref:`good_select_use` 中涵盖的简单辅助
符号。

``select`` 的宽松使用也往往使 Kconfig 文件更难阅读，既由于额外的依赖，也由于
``select`` 的非局部性质，它隐藏了符号可能被启用的方式。


``select`` 的替代方案
=========================

对于上一节的示例，更好的解决方案通常是将 ``select`` 变成 ``depends on``：

.. code-block:: kconfig

   config CONSOLE
   	bool "Console support"

   ...

   config USB_CONSOLE
   	bool "USB console support"
   	depends on CONSOLE

这使得生成无效配置成为不可能，意味着依赖永远只需在一个地方更新。

反对在这里使用 ``depends on`` 的可能是启用 ``USB_CONSOLE`` 的配置文件现在也需要
启用 ``CONSOLE``：

.. code-block:: cfg

   CONFIG_CONSOLE=y
   CONFIG_USB_CONSOLE=y

这归结为权衡，但如果启用 ``CONSOLE`` 是常态，那么缓解措施是将 ``CONSOLE`` 默认
设为 ``y``：

.. code-block:: kconfig

   config CONSOLE
   	bool "Console support"
   	default y

这给出配置文件中单个赋值：

.. code-block:: cfg

   CONFIG_USB_CONSOLE=y

注意不想要启用 ``CONSOLE`` 的配置文件现在必须显式禁用它：

.. code-block:: cfg

   CONFIG_CONSOLE=n


.. _good_select_use:

将 ``select`` 用于辅助符号
===================================

``select`` 的一个良好且安全的用法是设置捕获某些条件的"辅助"符号。这种辅助符号
最好没有 prompt 或依赖。

例如，指示特定 CPU/SoC 有 FPU 的辅助符号可以定义如下：

.. code-block:: kconfig

   config CPU_HAS_FPU
   	bool
   	help
      If y, the CPU has an FPU

   ...

   config SOC_FOO
       bool
       select CPU_HAS_FPU

   ...

   config SOC_BAR
       bool
       select CPU_HAS_FPU

这使得其他符号能够以通用方式检查 FPU 支持，而无需查找特定架构：

.. code-block:: kconfig

   config FPU
   	bool "Support floating point operations"
   	depends on CPU_HAS_FPU

替代方案可能是有如下依赖，可能在多处重复：

.. code-block:: kconfig

   config FPU
   	bool "Support floating point operations"
   	depends on SOC_FOO || SOC_BAR || ...

不可见辅助符号没有 ``select`` 也可能有用。例如，以下代码定义一个辅助符号，如果
机器有任意定义的"大"量内存则其值为 ``y``：

.. code-block:: kconfig

   config LARGE_MEM
   	def_bool MEM_SIZE >= 64

.. note::

   这是以下内容的缩写：

   .. code-block:: kconfig

      config LARGE_MEM
      	bool
      	default MEM_SIZE >= 64


``select`` 建议
=========================

总结起来，这里是 ``select`` 的一些推荐实践：

- 避免选择有 prompt 或依赖的符号。优先使用 ``depends on``。如果 ``depends on``
  导致配置文件中烦人的膨胀，考虑为最常见的值添加 Kconfig 默认值。

  罕见的例外可能包括你确定选择符号和被选符号的依赖永远不会不同步的情况，例如
  处理同一 ``if`` 内定义在彼此附近的两个简单符号时。

  常识适用，但要意识到 ``select`` 在实践中经常导致问题。``depends on`` 通常
  是更干净且更安全的解决方案。

- 随意选择没有 prompt 和依赖的简单辅助符号。它们是简化 Kconfig 文件的绝佳工具。

- 像 I2C 和 SPI 这样的总线是例外，遵循相同的思路还有 MFD 等。这些总线上的驱动
  应使用 ``select`` 以允许在设备树中启用总线上的设备时自动激活必要的总线驱动。

.. code-block:: kconfig

   config ADC_FOO
      bool "external SPI ADC foo driver"
      select SPI

（缺少）条件包含
******************************

``if`` 块为 ``if`` 内的每个项添加依赖，就像使用 ``depends on`` 一样。

与 ``if`` 相关的一个常见误解是认为以下代码条件性地包含文件
:file:`Kconfig.other`：

.. code-block:: kconfig

   if DEP

   source "Kconfig.other"

   endif

实际上，Kconfig 中没有条件包含。``if`` 在 ``source`` 周围没有特殊含义。

.. note::

   条件包含不可能实现，因为 ``if`` 条件可能包含（直接或间接）对尚未定义的符号的
   前向引用。

假设上面的 :file:`Kconfig.other` 包含此定义：

.. code-block:: kconfig

   config FOO
   	bool "Support foo"

在这种情况下，``FOO`` 最终会有此定义：

.. code-block:: kconfig

   config FOO
   	bool "Support foo"
   	depends on DEP

注意在 :file:`Kconfig.other` 中 ``FOO`` 的定义中添加 ``depends on DEP`` 是冗余
的，因为 ``DEP`` 依赖已经由 ``if DEP`` 添加。

一般来说，尽量避免添加冗余依赖。它们可能使 Kconfig 文件的结构更难理解，也使更改
更容易出错，因为可能很难发现同一依赖被添加了两次。


.. _stuck_symbols:

menuconfig 和 guiconfig 中的"卡住"符号
*******************************************

有一个与带 prompt 的相互依赖配置符号相关的常见微妙陷阱。考虑这些符号：

.. code-block:: kconfig

   config FOO
   	bool "Foo"

   config STACK_SIZE
   	hex "Stack size"
   	default 0x200 if FOO
   	default 0x100

假设这里的意图是每当 ``FOO`` 启用时使用更大的堆栈，且配置初始时 ``FOO`` 禁用。
另外，记住 Zephyr 通过合并配置文件（包括例如 :file:`prj.conf`）在构建目录中
:file:`zephyr/.config` 创建初始配置。此配置文件在 ``menuconfig`` 或
``guiconfig`` 运行之前存在。

首次进入配置接口时，``STACK_SIZE`` 的值为 0x100，符合预期。启用 ``FOO`` 后，
你可能合理期望 ``STACK_SIZE`` 的值变为 0x200，但它保持 0x100。

要理解发生了什么，记住 ``STACK_SIZE`` 有 prompt，意味着它可由用户配置，并考虑
Kconfig 必须从初始配置继续的一切是：

.. code-block:: cfg

   CONFIG_STACK_SIZE=0x100

由于 Kconfig 无法知道 0x100 值来自 ``default`` 还是用户输入的，它必须假设来自
用户。由于 ``STACK_SIZE`` 可由用户配置，配置文件中的值被尊重，任何符号默认值被
忽略。这就是为什么切换 ``FOO`` 时 ``STACK_SIZE`` 的值看起来"冻结"在 0x100。

正确的修复取决于意图是什么。这里是一些不同场景和建议：

- 如果 ``STACK_SIZE`` 总是可以自动派生且不需要可由用户配置，那么只需去掉 prompt：

  .. code-block:: kconfig

     config STACK_SIZE
     	hex
     	default 0x200 if FOO
     	default 0x100

  没有 prompt 的符号忽略保存配置中的任何值。

- 如果 ``STACK_SIZE`` 通常应可由用户配置，但当 ``FOO`` 启用时需要设为 0x200，
  那么当 ``FOO`` 启用时禁用其 prompt，如 `optional prompts`_ 中所述：

  .. code-block:: kconfig

     config STACK_SIZE
     	hex "Stack size" if !FOO
     	default 0x200 if FOO
     	default 0x100

- 如果 ``STACK_SIZE`` 通常应自动派生，但在罕见情况下需要设为自定义值，那么添加
  另一个选项使 ``STACK_SIZE`` 可由用户配置：

  .. code-block:: kconfig

     config CUSTOM_STACK_SIZE
     	bool "Use a custom stack size"
     	help
        Enable this if you need to use a custom stack size. When disabled, a
        suitable stack size is calculated automatically.

     config STACK_SIZE
     	hex "Stack size" if CUSTOM_STACK_SIZE
     	default 0x200 if FOO
     	default 0x100

  只要 ``CUSTOM_STACK_SIZE`` 禁用，``STACK_SIZE`` 就会忽略保存配置中的值。

在 ``menuconfig`` 或 ``guiconfig`` 接口中试验更改是一个好主意，以确保事情按你
预期的方式工作。在做这些中等复杂的更改时尤其如此。


配置文件中对无 prompt 符号的赋值
**********************************************************

配置文件中对隐藏（无 prompt，也称为 *不可见*）符号的赋值总是被忽略。隐藏符号
通过例如 ``default`` 和 ``select`` 间接从其他符号获取其值。

一个常见混淆来源是打开输出配置文件（:file:`zephyr/.config`），看到一堆对隐藏
符号的赋值，并假设当配置被 Kconfig 读回时这些赋值必须被尊重。实际上，
:file:`zephyr/.config` 中所有对隐藏符号的赋值都被 Kconfig 忽略，与其他配置文件
一样。

要理解为什么 :file:`zephyr/.config` 仍包含对隐藏符号的赋值，有助于意识到
:file:`zephyr/.config` 服务于两个独立目的：

1. 它保存配置，且

2. 它保存配置输出。:file:`zephyr/.config` 被 CMake 文件解析以让它们查询配置设置
   等。

:file:`zephyr/.config` 中对隐藏符号的赋值只是配置输出。Kconfig 本身在计算符号值
时忽略对隐藏符号的赋值。

.. note::

   *最小配置*，可以从 :ref:`menuconfig 和 guiconfig 接口 <menuconfig>` 内部生成，
   可以被认为是更接近仅保存配置，没有完整配置输出。


``depends on`` 与 ``string``/``int``/``hex`` 符号
*****************************************************

``depends on`` 不仅适用于 ``bool`` 符号，也适用于 ``string``、``int`` 和 ``hex``
符号（以及 choice）。

下面的 Kconfig 定义在 ``FOO_DEVICE`` 禁用时会隐藏 ``FOO_DEVICE_FREQUENCY`` 符号
并禁用其任何配置输出。

.. code-block:: kconfig

   config FOO_DEVICE
   	bool "Foo device"

   config FOO_DEVICE_FREQUENCY
   	int "Foo device frequency"
   	depends on FOO_DEVICE

一般来说，检查只有相关符号才在 ``menuconfig``/``guiconfig`` 接口中显示是一个好
主意。``FOO_DEVICE_FREQUENCY`` 在 ``FOO_DEVICE`` 禁用（且可能隐藏）时显示使符号
之间的关系更难理解，即使代码在 ``FOO_DEVICE`` 禁用时从不查看
``FOO_DEVICE_FREQUENCY``。


``menuconfig`` 符号
**********************

如果符号 ``FOO`` 的定义紧跟着依赖 ``FOO`` 的其他符号，那么那些符号成为 ``FOO``
的子项。如果 ``FOO`` 用 ``config FOO`` 定义，那么子项显示为相对于 ``FOO`` 缩进。
改用 ``menuconfig FOO`` 定义 ``FOO`` 则将子项放在以 ``FOO`` 为根的单独菜单中。

``menuconfig`` 对求值没有影响。它只是一个显示选项。

``menuconfig`` 可以减少菜单数量并使菜单结构更容易导航。例如，假设你有以下定义：

.. code-block:: kconfig

   menu "Foo subsystem"

   config FOO_SUBSYSTEM
   	bool "Foo subsystem"

   if FOO_SUBSYSTEM

   config FOO_FEATURE_1
   	bool "Foo feature 1"

   config FOO_FEATURE_2
   	bool "Foo feature 2"

   config FOO_FREQUENCY
   	int "Foo frequency"

   ... lots of other FOO-related symbols

   endif # FOO_SUBSYSTEM

   endmenu

在这种情况下，可能更好的做法是去掉 ``menu`` 并将 ``FOO_SUBSYSTEM`` 变成
``menuconfig`` 符号：

.. code-block:: kconfig

   menuconfig FOO_SUBSYSTEM
   	bool "Foo subsystem"

   if FOO_SUBSYSTEM

   config FOO_FEATURE_1
   	bool "Foo feature 1"

   config FOO_FEATURE_2
   	bool "Foo feature 2"

   config FOO_FREQUENCY
   	int "Foo frequency"

   ... lots of other FOO-related symbols

   endif # FOO_SUBSYSTEM

在 ``menuconfig`` 接口中，这将显示如下：

.. code-block:: none

   [*] Foo subsystem  --->

注意使没有子项的符号成为 ``menuconfig`` 是无意义的。应该避免，因为它看起来与所有
子项不可见的符号相同：

.. code-block:: none

   [*] I have no children  ----
   [*] All my children are invisible  ----


宏参数中的逗号
*************************

Kconfig 使用逗号分隔宏参数。这意味着像这样的结构会失败：

.. code-block:: kconfig

    config FOO
        bool
        default y if $(dt_chosen_enabled,"zephyr,bar")

要解决这个问题，创建一个带文本的变量并使用这个变量作为参数，如下：

.. code-block:: kconfig

    DT_CHOSEN_ZEPHYR_BAR := zephyr,bar

    config FOO
        bool
        default y if $(dt_chosen_enabled,$(DT_CHOSEN_ZEPHYR_BAR))

.. note::

   变量 :samp:`DT_COMPAT_{VND_MY_DEVICE} := {vnd,my-device}` 由 Zephyr 为设备树
   绑定中找到的每个 ``compatible`` 自动创建；不需要定义这种变量。细节见
   :ref:`auto-dts-kconfig`。

在 menuconfig/guiconfig 中检查更改
****************************************

添加新符号或对 Kconfig 文件做其他更改时，之后在 :ref:`menuconfig 或
guiconfig <menuconfig>` 中查找符号是一个好主意。要快速到达符号，使用跳转功能
（按 :kbd:`/`）。

这里是一些要检查的事情：

* 符号放在好的位置吗？检查它们显示在有意义的菜单中，靠近相关符号。

  如果一个符号依赖另一个，那么通常是一个好主意将它放在它依赖的符号紧后面。然后
  它会在 ``menuconfig`` 接口中显示为相对于它依赖的符号缩进，在 ``guiconfig`` 中
  显示为以符号为根的单独菜单。如果几个符号放在它们依赖的符号后面，这也有效。

* 从 prompt 容易猜出符号做什么吗？

* 如果添加许多符号，它们可以被设置为的所有值组合都有意义吗？

  例如，如果添加两个符号 ``FOO_SUPPORT`` 和 ``NO_FOO_SUPPORT``，且两者可以同时
  启用，那么那是一个无意义的配置。在这种情况下，可能更好的做法是有单个
  ``FOO_SUPPORT`` 符号。

* 有任何重复的依赖吗？

  这可以通过选择符号并按 :kbd:`?` 查看符号信息来检查。如果有重复的依赖，那么使用
  符号信息中显示的 ``Included via ...`` 路径来弄清楚它们来自哪里。


使用 :file:`scripts/kconfig/lint.py` 检查更改
*****************************************************

做 Kconfig 更改后，你可以使用 :zephyr_file:`scripts/kconfig/lint.py` 脚本检查
一些潜在问题，如未使用的符号和不可能启用的符号。使用 ``--help`` 查看可用选项。

一些检查必然有点启发式，所以符号被检查标记不一定意味着有问题。如果检查由于 C 中
的令牌粘贴（``CONFIG_FOO_##index##_BAR``）返回误报，只需忽略它。

调查未知符号 ``FOO_BAR`` 时，运行 ``git grep FOO_BAR`` 查找引用是一个好主意。使用
例如 ``git grep FOO`` 和 ``git grep BAR`` 搜索符号名称的某些组件也是个好主意，
因为它有助于发现令牌粘贴。


风格建议和简写
************************************

本节给出一些风格建议并解释一些常见 Kconfig 简写。


提取公共依赖
================================

如果一系列符号/choice 共享公共依赖，依赖可以用 ``if`` 提取。

作为示例，考虑以下代码：

.. code-block:: kconfig

   config FOO
   	bool "Foo"
   	depends on DEP

   config BAR
   	bool "Bar"
   	depends on DEP

   choice
   	prompt "Choice"
   	depends on DEP

   config BAZ
   	bool "Baz"

   config QAZ
   	bool "Qaz"

   endchoice

这里，``DEP`` 依赖可以像这样提取：

.. code-block:: kconfig

   if DEP

   config FOO
   	bool "Foo"

   config BAR
   	bool "Bar"

   choice
   	prompt "Choice"

   config BAZ
   	bool "Baz"

   config QAZ
   	bool "Qaz"

   endchoice

   endif # DEP

.. note::

   内部，代码的第二种版本被转换为第一种。

如果一系列共享依赖的符号/choice 都在同一菜单中，依赖可以放在菜单本身：

.. code-block:: kconfig

   menu "Foo features"
   	depends on FOO_SUPPORT

   config FOO_FEATURE_1
   	bool "Foo feature 1"

   config FOO_FEATURE_2
   	bool "Foo feature 2"

   endmenu

如果 ``FOO_SUPPORT`` 为 ``n``，整个菜单消失。


冗余默认值
==================

``bool`` 符号隐式默认为 ``n``，``string`` 符号隐式默认为空字符串。因此，
``default n`` 和 ``default ""``（几乎）总是冗余的。

Zephyr 中推荐的风格是对 ``bool`` 和 ``string`` 符号跳过冗余默认值。这也生成更
清晰的文档：（*隐式默认为 n* 而不是 *n if <依赖，可能继承>*）。

然而，``int`` 和 ``hex`` 符号*应该*始终给出默认值，因为它们隐式默认为空字符串。
这 partly 为了与 C Kconfig 工具兼容，尽管隐式 0 默认与其他符号类型相比可能
也不太可能是预期值。

``default n``/``default ""`` 不冗余的唯一情况是在多个位置定义符号并希望覆盖例如
后续定义上的 ``default y``。注意 ``default n`` 不覆盖先前定义的 ``default y``。

也就是说，下面的示例中 FOO 会被设为 ``n``。如果第一个定义中省略了 ``default n``，
FOO 会被设为 ``y``。

  .. code-block:: kconfig

     config FOO
     	bool "foo"
     	default n

     config FOO
     	bool "foo"
     	default y

在下面的示例中 FOO 会得到值 ``y``。

  .. code-block:: kconfig

     config FOO
     	bool "foo"
     	default y

     config FOO
     	bool "foo"
     	default n

.. _kconfig_shorthands:

常见 Kconfig 简写
=========================

Kconfig 有两个处理 prompt 和默认值的简写。

- ``<type> "prompt"`` 是同时给符号/choice 类型和 prompt 的简写。这两个定义相等：

  .. code-block:: kconfig

     config FOO
     	bool "foo"

  .. code-block:: kconfig

     config FOO
     	bool
     	prompt "foo"

  第一种风格，使用简写，在 Zephyr 中优先。

- ``def_<type> <value>`` 是同时给类型和值的简写。这两个定义相等：

  .. code-block:: kconfig

     config FOO
     	def_bool BAR && BAZ

  .. code-block:: kconfig

     config FOO
     	bool
     	default BAR && BAZ

在同一定义中同时使用 ``<type> "prompt"`` 和 ``def_<type> <value>`` 简写是冗余的，
因为它给出类型两次。

``def_<type> <value>`` 简写通常只对没有 prompt 的符号有用，且有些晦涩。

.. note::

   对于在多个位置定义的符号（例如在 Zephyr 中的 ``Kconfig.defconfig`` 文件中），
   最好只为符号的"基础"定义给出符号类型，并对剩余定义使用 ``default``（而不是
   ``def_<type> value``）。这样，如果符号的基础定义被删除，符号最终没有类型，
   这会生成指向其他定义的警告。这使得额外定义更容易发现和移除。


Prompt 字符串
=============

对于启用驱动/子系统 FOO 的 Kconfig 符号，考虑只将 "Foo" 作为 prompt，而不是
"Enable Foo support" 或类似。在可开关选项的上下文中通常很清楚，并使事情一致。

风格
=====

风格指南见 :ref:`coding_style`。

较少知名/使用的 Kconfig 功能
**********************************

本节列出一些更晦涩的 Kconfig 行为和功能，它们可能仍然有用。


``imply`` 语句
======================

``imply`` 语句类似于 ``select``，但尊重依赖且不强制值。例如，以下代码可用于在
FOO SoC 上默认启用 USB 键盘支持，同时仍允许用户关闭：

.. code-block:: kconfig

   config SOC_FOO
       bool
       imply USB_KEYBOARD

   ...

   config USB_KEYBOARD
   	bool "USB keyboard support"

``imply`` 像建议一样起作用，而 ``select`` 强制值。


可选 prompt
===============

可以在符号的 prompt 上放条件使其可选地可由用户配置。例如，某些开发板上硬编码为
0xFF 而其他开发板上可配置的值 ``MASK`` 可以表达如下：

.. code-block:: kconfig

   config MASK
   	hex "Bitmask" if HAS_CONFIGURABLE_MASK
   	default 0xFF

.. note::

   这是以下内容的缩写：

   .. code-block:: kconfig

      config MASK
      	hex
      	prompt "Bitmask" if HAS_CONFIGURABLE_MASK
      	default 0xFF

``HAS_CONFIGURABLE_MASK`` 辅助符号会被开发板选择以指示 ``MASK`` 可配置。当
``MASK`` 可配置时，它也会默认为 0xFF。


可选 choice
================

用 ``optional`` 关键字定义 choice 允许整个 choice 被关闭以不选择任何符号：

.. code-block:: kconfig

   choice
   	prompt "Use legacy protocol"
   	optional

   config LEGACY_PROTOCOL_1
   	bool "Legacy protocol 1"

   config LEGACY_PROTOCOL_2
   	bool "Legacy protocol 2"

   endchoice

在 ``menuconfig`` 接口中，这将显示为例如 ``[*] Use legacy protocol
(Legacy protocol 1) --->``，其中 choice 可以被关闭以不启用任何符号。


``visible if`` 条件
=========================

在菜单上放 ``visible if`` 条件会隐藏菜单和其中所有符号，同时仍允许符号默认值
生效。

作为动机示例，考虑以下代码：

.. code-block:: kconfig

   menu "Foo subsystem"
   	depends on HAS_CONFIGURABLE_FOO

   config FOO_SETTING_1
   	int "Foo setting 1"
   	default 1

   config FOO_SETTING_2
   	int "Foo setting 2"
   	default 2

   endmenu

当 ``HAS_CONFIGURABLE_FOO`` 为 ``n`` 时，``FOO_SETTING_1`` 和
``FOO_SETTING_2`` 不生成任何配置输出，因为上面的代码在逻辑上等价于以下代码：

.. code-block:: kconfig

   config FOO_SETTING_1
   	int "Foo setting 1"
   	default 1
   	depends on HAS_CONFIGURABLE_FOO

   config FOO_SETTING_2
   	int "Foo setting 2"
   	default 2
   	depends on HAS_CONFIGURABLE_FOO

如果我们希望符号在 ``HAS_CONFIGURABLE_FOO`` 为 ``n`` 时仍获得其默认值，但不可由
用户配置，那么我们可以改用 ``visible if``：

.. code-block:: kconfig

   menu "Foo subsystem"
   	visible if HAS_CONFIGURABLE_FOO

   config FOO_SETTING_1
   	int "Foo setting 1"
   	default 1

   config FOO_SETTING_2
   	int "Foo setting 2"
   	default 2

   endmenu

这在逻辑上等价于以下：

.. code-block:: kconfig

   config FOO_SETTING_1
   	int "Foo setting 1" if HAS_CONFIGURABLE_FOO
   	default 1

   config FOO_SETTING_2
   	int "Foo setting 2" if HAS_CONFIGURABLE_FOO
   	default 2

.. note::

   见 `optional prompts`_ 章节了解 prompt 上条件的含义。

当 ``HAS_CONFIGURABLE_FOO`` 为 ``n`` 时，我们现在得到符号的以下配置输出，而非
没有输出：

.. code-block:: cfg

   ...
   CONFIG_FOO_SETTING_1=1
   CONFIG_FOO_SETTING_2=2
   ...


其他资源
***************

`Kconfiglib docstring
<https://github.com/zephyrproject-rtos/Kconfiglib/blob/main/kconfiglib.py>`__ 中
的 *Intro to symbol values* 章节更详细地介绍符号值如何计算。
