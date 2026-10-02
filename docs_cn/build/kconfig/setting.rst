.. _setting_configuration_values:

设置 Kconfig 配置值
####################################

:ref:`menuconfig 和 guiconfig 接口 <menuconfig>` 可以在应用开发期间用于测试
配置。本页解释如何使设置永久化。

所有 Kconfig 选项都可以在 :ref:`Kconfig 搜索页面 <kconfig-search>` 中搜索。

.. note::

   在对 Kconfig 文件做更改之前，也去 :ref:`kconfig_tips_and_tricks` 页面
   过一遍是一个好主意。


可见与不可见 Kconfig 符号
*************************************

做 Kconfig 更改时，理解 *可见* 和 *不可见* 符号之间的区别很重要。

- 可见符号是带有 prompt 定义的符号。可见符号显示在交互式配置接口中（因此
  *可见*），并可以在配置文件中设置。

  以下是一个可见符号的示例：

  .. code-block:: kconfig

     config FPU
     	bool "Support floating point operations"
     	depends on HAS_FPU

  该符号在 ``menuconfig`` 中显示如下，可以切换：

  .. code-block:: none

     [ ] Support floating point operations

- *不可见* 符号是没有 prompt 的符号。不可见符号不显示在交互式配置接口中，
  用户无法直接控制其值。它们的值来自默认值或其他符号。

  以下是一个不可见符号的示例：

  .. code-block:: kconfig

     config CPU_HAS_FPU
     	bool
     	help
     	  This symbol is y if the CPU has a hardware floating point unit.

  在这种情况下，``CPU_HAS_FPU`` 通过其他具有 ``select CPU_HAS_FPU`` 的符号
  启用。


在配置文件中设置符号
**************************************

可见符号可以通过在配置文件中设置来配置。初始配置通过合并开发板的
:file:`*_defconfig` 文件与应用设置（通常来自 :file:`prj.conf`）生成。更多细节
见下面的 :ref:`initial-conf`。

配置文件中的赋值使用此语法：

.. code-block:: cfg

   CONFIG_<symbol name>=<value>

等号周围不应有空格。

``bool`` 符号可以通过分别设置为 ``y`` 或 ``n`` 来启用或禁用。上面示例中的
``FPU`` 符号可以像这样启用：

.. code-block:: cfg

   CONFIG_FPU=y

.. note::

   布尔符号也可以设置为 ``n``，使用像这样格式的注释：

   .. code-block:: cfg

      # CONFIG_SOME_OTHER_BOOL is not set

   这是你在保存到构建目录中 :file:`zephyr/.config` 的合并配置中看到的格式。

   出于历史原因接受这种风格：Kconfig 配置文件可以被解析为 makefile（尽管
   Zephyr 不使用这）。使 ``n`` 值的符号对应未设置的变量简化了 Make 中的测试。

其他符号类型像这样赋值：

.. code-block:: cfg

   CONFIG_SOME_STRING="cool value"
   CONFIG_SOME_INT=123

注释使用 #：

.. code-block:: cfg

   # This is a comment

配置文件中的赋值只有在符号的依赖满足时才被尊重。否则会打印警告。要弄清楚符号
的依赖是什么，使用 :ref:`交互式配置接口 <menuconfig>` 之一（你可以用 :kbd:`/`
直接跳转到符号），或在 :ref:`Kconfig 搜索页面 <kconfig-search>` 中查找符号。


.. _initial-conf:

初始配置
*************************

应用的初始配置来自合并三个来源的配置设置：

1. 存储在 :file:`boards/<VENDOR>/<BOARD>/<BOARD>_defconfig` 的
   ``BOARD`` 特定配置文件

2. 任何以 ``CONFIG_`` 为前缀的 CMake 缓存条目

3. 应用配置

应用配置可以来自下面的来源（每个文件都称为 Kconfig 片段，它们然后被合并以获取
用于特定构建的最终配置）。默认情况下，使用 :file:`prj.conf`。

#. 如果设置了 ``CONF_FILE``，其中指定的配置文件被合并并用作应用配置。
   ``CONF_FILE`` 可以通过多种方式设置：

   1. 在 :file:`CMakeLists.txt` 中，在调用 ``find_package(Zephyr)`` 之前

   2. 通过传递 ``-DCONF_FILE=<conf file(s)>``，直接或通过 ``west``

   3. 从 CMake 变量缓存

#. 否则，如果 :file:`boards/<BOARD>.conf` 存在于应用配置目录中，使用它与
   :file:`prj.conf` 的合并结果。

#. 否则，如果使用开发板修订版本且 :file:`boards/<BOARD>_<revision>.conf`
   存在于应用配置目录中，使用它与 :file:`prj.conf` 和
   :file:`boards/<BOARD>.conf` 的合并结果。

#. 否则，从应用配置目录使用 :file:`prj.conf`。如果它不存在，则会发出致命错误。

此外，应用可以有 SoC Kconfig 片段添加到配置，如果存在，文件
:file:`socs/<SOC>_<BOARD_QUALIFIERS>.conf` 将在主项目配置应用后且任何开发板
Kconfig 片段文件应用前被应用。

所有配置文件都从应用的配置目录获取，除了使用 ``CONF_FILE``、``EXTRA_CONF_FILE``、
``DTC_OVERLAY_FILE`` 和 ``EXTRA_DTC_OVERLAY_FILE`` 参数给出的绝对路径文件。对于
这些，Zephyr 模块中的文件可以通过转义 Zephyr 模块目录变量来引用，像这样
``\${ZEPHYR_<module>_MODULE_DIR}/<path-to>/<file>`` 当在应用的
:file:`CMakeLists.txt` 中设置任何上述变量时。

如何定义应用配置目录见
:ref:`Application Configuration Directory <application-configuration-directory>`。

如果符号同时在 :file:`<BOARD>_defconfig` 和应用配置中赋值，应用配置中设置的值
优先。

合并的配置保存到构建目录中的 :file:`zephyr/.config`。

只要 :file:`zephyr/.config` 存在且是最新的（比任何 ``BOARD`` 和应用配置文件
新），它将被优先使用于生成新的合并配置。:file:`zephyr/.config` 也是在
:ref:`交互式配置接口 <menuconfig>` 中做更改时被修改的配置。


.. _kconfig_warning_as_error:

将 Kconfig 警告视为错误
***********************************

一些 Kconfig 警告默认中止构建，例如对未定义符号的赋值。其他只被打印，例如当
符号被设置多于一次，或当赋值被忽略因为符号的依赖未满足。

设置 :makevar:`KCONFIG_WARNING_AS_ERROR` CMake 变量将 *每个* Kconfig 警告视为
错误：

.. code-block:: console

   west build -b <board> <app> -- -DKCONFIG_WARNING_AS_ERROR=y

这在 CI 中很有用，那里被静默忽略的配置设置很可能是错误。它通过
``zephyr_get()`` 读取，因此也可以作为 :ref:`环境变量 <env_vars>` 或通过
:ref:`cmake_build_config_package` 给出。


跟踪 Kconfig 符号
************************

可以创建 Kconfig 符号取另一个 Kconfig 符号的默认值。

当你想要一个特定于应用或子系统的符号但不想直接依赖通用符号时，这很有价值。
例如，你可能想要解耦设置以便它们可以独立配置，或确保你始终有一个本地命名的
设置，即使外部设置名称之后更改。

例如，考虑通用的 ``FOO_STRING`` 设置，子系统想要有 ``SUB_FOO_STRING`` 但仍
允许自定义。

可以像这样做：

.. code-block:: kconfig

    config FOO_STRING
            string "Foo"
            default "foo"

    config SUB_FOO_STRING
            string "Sub-foo"
            default FOO_STRING

这确保 ``SUB_FOO_STRING`` 的默认值与 ``FOO_STRING`` 相同，同时仍允许用户独立
配置两个设置。

也可以使 ``SUB_FOO_STRING`` 不可见并由此保持两个符号同步，除非跟踪符号的值在
:file:`defconfig` 文件中被更改。

.. code-block:: kconfig

    config FOO_STRING
            string "Foo"
            default "foo"

    config SUB_FOO_STRING
            string
            default FOO_STRING
            help
              Hidden symbol which follows FOO_STRING
              Can be changed through *.defconfig files.


配置不可见 Kconfig 符号
*************************************

对开发板的默认配置做更改时，你可能必须配置不可见符号。这在
:file:`boards/<VENDOR>/<BOARD>/Kconfig.defconfig` 中完成，它是一个普通的
:file:`Kconfig` 文件。

.. note::

    :file:`.config` 文件中的赋值对不可见符号没有影响，因此这种方案不只是一个
    组织问题。

:file:`Kconfig.defconfig` 中的赋值依赖于在多个位置定义 Kconfig 符号。作为示例，
假设我们想要将下面的 ``FOO_WIDTH`` 设置为 32：

.. code-block:: kconfig

    config FOO_WIDTH
    	int

要做到这，我们在 :file:`Kconfig.defconfig` 中按如下方式扩展 ``FOO_WIDTH`` 的
定义：

.. code-block:: kconfig

    if BOARD_MY_BOARD

    config FOO_WIDTH
    	default 32

    endif

.. note::

   由于符号的类型（``int``）已在第一个定义位置给出，这里不需要重复。只在符号
   的 "基础" 定义中给出类型一次是一个好主意，原因在 :ref:`kconfig_shorthands`
   中解释。

:file:`Kconfig.defconfig` 文件中的 ``default`` 值优先于符号 "基础" 定义中给出
的 ``default`` 值。内部，这通过先包含 :file:`Kconfig.defconfig` 文件实现。
Kconfig 使用第一个条件满足的 ``default``，其中空条件对应 ``if y``（始终满足）。

注意来自周围顶层 ``if``\ s 的条件传播到符号属性，因此上面的 ``default`` 等价于
``default 32 if BOARD_MY_BOARD``。

.. _multiple_symbol_definitions:

多个符号定义
---------------------------

当符号在多个位置定义时，每个定义作为一个碰巧共享相同名称的独立符号起作用。
这意味着属性不被追加到先前的定义。如果 **任何** 定义的条件导致符号解析为
``y``，符号将是 ``y``。因此不可能通过在多个位置定义使符号的依赖更严格。

例如，下面符号 ``FOO`` 的依赖在 ``DEP1`` **或** ``DEP2`` 为真时满足，不要求
两者都是：

.. code-block:: none

   config FOO
     ...
     depends on DEP1

   config FOO
     ...
     depends on DEP2

.. warning::
   没有显式依赖的符号仍遵循上面的规则。没有任何依赖的符号将导致符号始终可
   赋值。下面的定义将导致 ``FOO`` 始终默认启用，无论 ``DEP1`` 的值如何。

   .. code-block:: kconfig

      config FOO
         bool "FOO"
         depends on DEP1

      config FOO
         default y

   这种依赖削弱可以通过 :ref:`configdefault <kconfig_extensions>` 扩展避免，
   如果意图只是添加新的默认值而不修改符号的其他行为。

.. note::
   对 :file:`Kconfig.defconfig` 文件做更改时，之后始终在
   :ref:`交互式配置接口 <menuconfig>` 之一中检查符号的直接依赖。通常需要重复
   符号基础定义中的依赖以避免削弱符号的依赖。


Kconfig.defconfig 文件的动机
--------------------------------------

这种配置方案的一个动机是避免使固定的 ``BOARD`` 特定设置在交互式配置接口中可
配置。如果所有开发板配置都通过 :file:`<BOARD>_defconfig` 完成，所有符号都必须
可见，因为 :file:`<BOARD>_defconfig` 中给出的值对不可见符号没有影响。

使固定设置可由用户配置会使配置接口杂乱并使它们更难理解，并使意外创建损坏的
配置更容易。

处理固定的开发板特定设置时，也考虑它们是否应该通过 :ref:`设备树 <dt-guide>`
处理。


配置 choice
-------------------

有两种方式配置 Kconfig ``choice``：

1. 通过在配置文件中将 choice 符号之一设置为 ``y``。

   将一个 choice 符号设置为 ``y`` 自动给所有其他 choice 符号值 ``n``。

   如果多个 choice 符号被设置为 ``y``，只有最后设置为 ``y`` 的被尊重（其余得到
   值 ``n``）。这允许从开发板 :file:`defconfig` 文件的 choice 选择被应用
   :file:`prj.conf` 文件覆盖。

2. 通过在 :file:`Kconfig.defconfig` 中更改 choice 的 ``default``。

   与符号一样，更改 choice 的默认通过在多个位置定义 choice 完成。要使这工作，
   choice 必须有名称。

   作为示例，假设 choice 有以下基础定义（这里，choice 的名称是 ``FOO``）：

   .. code-block:: kconfig

      choice FOO
          bool "Foo choice"
          default B

      config A
          bool "A"

      config B
          bool "B"

      endchoice

   要将 ``FOO`` 的默认符号更改为 ``A``，你会添加以下定义到
   :file:`Kconfig.defconfig`：

   .. code-block:: kconfig

      choice FOO
          default A
      endchoice

:file:`Kconfig.defconfig` 方法应该在 choice 的依赖可能未满足时使用。在那种
情况下，你在用户使 choice 可见的任何时候设置默认选择。


更多 Kconfig 资源
====================

:ref:`kconfig_tips_and_tricks` 页面有一些编写 Kconfig 文件的技巧。

:zephyr_file:`kconfiglib.py <scripts/kconfig/kconfiglib.py>` 的 docstring
（文件顶部）详细介绍符号值如何计算。
