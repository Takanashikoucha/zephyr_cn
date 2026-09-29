.. _assert:

断言
##########

Zephyr 提供多种断言机制用于捕获编程错误：

- **运行时断言**在代码运行期间检查某个条件，若检查失败则触发 :ref:`致命错误 <fatal>`。
  推荐的 API 是支持模块感知的 ``ZASSERT()`` 宏；旧的 ``__ASSERT()`` 宏现在只是其上的
  一层薄兼容层，已被弃用。
- **构建断言**（``BUILD_ASSERT()``）完全在编译期求值，且始终会被检查。

.. note::

   本文档中描述的运行时 ``ZASSERT()`` 宏与 :ref:`Ztest <test-framework>` 框架提供的
   小写 ``zassert_*`` 宏（``zassert_true()``、``zassert_equal()``、...）无关。
   ``zassert_*`` 宏用于报告测试失败，而 ``ZASSERT()`` 宏在检测到编程错误时
   触发致命错误。

运行时断言
******************

ZASSERT()
=========

支持模块感知的断言 API 声明在 :zephyr_file:`include/zephyr/sys/zassert.h` 中。
每个源文件通过加入一个断言*模块*来选择断言级别，该级别是编译期常量。由于
级别在编译期已知，编译器可以根据断言所属模块的断言级别来优化断言代码的
占用空间。

断言级别
----------------

每个模块解析为四个级别之一：

- ``ZASSERT_LEVEL_OFF`` -- 断言被完全从编译中移除。
- ``ZASSERT_LEVEL_TERSE`` -- 断言会被检查；失败时仅报告固定的
  ``ASSERTION FAIL`` 横幅。位置、条件、消息和参数不会被编译进去。
- ``ZASSERT_LEVEL_NORMAL`` -- 断言会被检查；失败时仅报告位置
  （``ASSERTION FAIL @ file:line``）。条件、消息和参数不会被编译进去。
- ``ZASSERT_LEVEL_VERBOSE`` -- 断言会被检查；失败时报告字符串化的
  条件、位置以及可选消息。

:kconfig:option:`CONFIG_ASSERT` 是总开关。
禁用它时，所有模块都被强制为 ``ZASSERT_LEVEL_OFF``，所有 ``ZASSERT()`` /
``ZASSERT_MODULE()`` 的用法都编译为空，与任何模块配置的级别无关。

:note:
   ``ZASSERTS`` 的占用空间缩减依赖编译器优化在编译期裁剪未使用的条件、
   参数和字符串字面量。较低的优化级别可能无法进行死代码消除，
   导致即使模块断言级别设置较低，断言产物仍残留在二进制中。

选择模块
------------------

在翻译单元中任何 :c:macro:`ZASSERT` 使用之前，在文件作用域放置一次
:c:macro:`ZASSERT_MODULE`：

.. code-block:: c

   #include <zephyr/sys/zassert.h>

   ZASSERT_MODULE(MYMODULE);

模块名是一个大写标识符。其默认级别取自 Kconfig 符号
``CONFIG_ASSERT_MODULE_<module>_LEVEL``（此处为 ``CONFIG_ASSERT_MODULE_MYMODULE_LEVEL``）。
文件可以通过传递显式级别作为第二个参数来覆盖模块默认值，例如
``ZASSERT_MODULE(MYMODULE, ZASSERT_LEVEL_VERBOSE)``。

选定模块后，像条件检查一样使用 :c:macro:`ZASSERT`，可附带
:c:func:`printf` 风格的可选消息：

.. code-block:: c

   ZASSERT(x == 3, "x was %d, expected 3", x);

如果条件为假且模块级别至少为 ``ZASSERT_LEVEL_TERSE``，则触发致命错误。
位置仅在 ``ZASSERT_LEVEL_NORMAL`` 及以上级别时被编译进去并打印，
而条件、消息及其参数仅在 ``ZASSERT_LEVEL_VERBOSE`` 级别下
才被编译进去并打印。

对于头文件和内联函数，避免在文件作用域使用 ``ZASSERT_MODULE()``，因为
该选择会泄漏到包含该头文件的每个文件中。请改用以下方法之一。

将 :c:macro:`ZASSERT_MODULE` 放在函数体内。这样选择就是块作用域的，
不会泄漏到包含方，且普通的 :c:macro:`ZASSERT` 在该函数内可用：

.. code-block:: c

   static inline void f(void *ptr)
   {
           ZASSERT_MODULE(MYMODULE);

           ZASSERT(ptr != NULL, "ptr must not be NULL");
   }

对于级别固定的断言，使用 :c:macro:`ZASSERT_TERSE`、
:c:macro:`ZASSERT_NORMAL` 或 :c:macro:`ZASSERT_VERBOSE`。这些形式在
调用点选择级别，且不在作用域中声明任何内容：

.. code-block:: c

   ZASSERT_TERSE(ptr != NULL);
   ZASSERT_NORMAL(ptr != NULL);
   ZASSERT_VERBOSE(ptr != NULL, "ptr must not be NULL");

``ZASSERT_LEVEL_TERSE``、``ZASSERT_LEVEL_NORMAL`` 和 ``ZASSERT_LEVEL_VERBOSE``
宏定义用于配置模块断言级别，而
``ZASSERT_TERSE()``、``ZASSERT_NORMAL()`` 和 ``ZASSERT_VERBOSE()`` 执行
级别固定的断言。

.. note::

   ``ZASSERT()`` 及其文件作用域模块有若干规则：

   - ``ZASSERT_MODULE()`` 必须出现在翻译单元中第一个 ``ZASSERT()`` 之前，
     且每个文件只能选择一个模块。
   - 在没有模块处于作用域时使用 ``ZASSERT()`` 会导致编译错误。请
     先选择一个模块，或使用级别固定的 ``ZASSERT_TERSE()``、``ZASSERT_NORMAL()``
     或 ``ZASSERT_VERBOSE()`` 形式。
   - :kconfig:option:`CONFIG_ASSERT` 仍是总开关：禁用它时，
     模块级别被强制为 ``ZASSERT_LEVEL_OFF``，与配置的级别无关。


定义模块的 Kconfig 级别
---------------------------------

``CONFIG_ASSERT_MODULE_<module>_LEVEL`` 符号由模板
:zephyr_file:`subsys/debug/zassert/Kconfig.template.assert` 生成。从 Kconfig
文件引入该模板，先设置模块名和人类可读的描述：

.. code-block:: kconfig

   module = MYMODULE
   module-str = the MYMODULE assert module
   source "subsys/debug/zassert/Kconfig.template.assert"

这会生成面向用户的 ``Off`` / ``Terse`` / ``Normal`` / ``Verbose`` 选择项，
以及派生的、不可赋值的整型符号 ``CONFIG_ASSERT_MODULE_MYMODULE_LEVEL``，
供 ``ZASSERT_MODULE(MYMODULE)`` 使用。
该选择项默认为 ``Verbose``，且仍可被 :file:`prj.conf` 覆盖。

示例
-------

:zephyr:code-sample:`assert` 示例演示了在总断言开关开启的情况下，
为单个文件启用详细（verbose）断言。
一个精简版本：

.. code-block:: c

   #include <zephyr/kernel.h>
   #include <zephyr/sys/zassert.h>

   ZASSERT_MODULE(MYMODULE);

   int main(void)
   {
           int x = 2;

           ZASSERT(x == 3, "x was %d, expected 3", x);

           return 0;
   }

当 ``CONFIG_ASSERT_MODULE_MYMODULE_LEVEL_VERBOSE=y`` 时，失败的检查产生：

.. code-block:: none

   ASSERTION FAIL [x == 3] @ .../src/main.c:...
   x was 2, expected 3

定制失败行为
--------------------------------

整个断言冷路径被整合为一组小的、可覆盖的弱链接函数，
声明在 :zephyr_file:`include/zephyr/sys/zassert.h` 中，
实现在 :zephyr_file:`subsys/debug/zassert/zassert.c` 中：

- :c:func:`zassert_fail` 报告失败的断言（位置，以及当存在消息时的
  消息及其参数），然后调用 :c:func:`zassert_post_action`。
  覆盖它是捕获或重定向整个断言输出的唯一入口。
- :c:func:`zassert_post_action` 执行终止动作。默认实现
  在失败线程运行于用户模式时调用 :c:func:`k_oops`，
  否则调用 :c:func:`k_panic`。
- :c:func:`zassert_vprint` 是所有断言文本流经的唯一原语。
  覆盖它即可从一处捕获或重定向每一条断言消息。
  :c:func:`zassert_print` 是围绕它的可变参数便捷封装，
  被旧的 ``__ASSERT_PRINT()`` 兼容垫片使用。

启用 :kconfig:option:`CONFIG_ASSERT_TEST` 时，后置动作处理程序
允许返回（而非中止），以便测试通过安装自定义钩子来验证断言行为。


构建断言
****************

Zephyr 提供一个用于执行构建期断言检查的宏。
它完全在编译期求值，且始终会被检查。

BUILD_ASSERT()
=============

它的语义与 C 的 ``_Static_assert`` 或 C++ 的
``static_assert`` 相同。如果求值失败，编译器会生成一个构建错误。
如果编译器支持，提供的消息会被打印以提供更多上下文。

与 ``__ASSERT()`` 不同，消息必须是静态字符串或静态字符串的拼接。
该宏不支持格式化或可变参数。

例如，假设以下检查失败：

.. code-block:: c

	BUILD_ASSERT(FOO == 2000, "Invalid value of FOO, expected 2000, got " STRINGIFY(FOO));

使用 GCC 时，输出类似：

.. code-block:: none

	tests/kernel/fatal/src/main.c: In function 'test_main':
	include/zephyr/toolchain/gcc.h:28:37: error: static assertion failed:
   "Invalid value of FOO, expected 2000, got 1000"
	 #define BUILD_ASSERT(EXPR, MSG) _Static_assert(EXPR, "" MSG)
				 ^~~~~~~~~~~~~~
	tests/kernel/fatal/src/main.c:370:2: note: in expansion of macro 'BUILD_ASSERT'
	  BUILD_ASSERT(FOO == 2000,
	  ^~~~~~~~~~~~~~~~


旧版 __ASSERT()
=================

``__ASSERT()`` 系列宏声明在
:zephyr_file:`include/zephyr/sys/__assert.h` 中，早于 ``ZASSERT()``，
现在是一个使用内置 ``DEFAULT`` 断言模块的兼容垫片。
新代码应优先使用带专用模块的 ``ZASSERT()``。

.. note::

   ``__ASSERT()`` 和 ``CONFIG_ASSERT*`` Kconfig 选项已被弃用。
   它们通过 ``DEFAULT`` 模块继续工作，但底层断言 API
   在未来版本中可能发生变化。

``DEFAULT`` 模块由 :kconfig:option:`CONFIG_ASSERT` 启用。
其级别由 :kconfig:option:`CONFIG_ASSERT_MODULE_DEFAULT_LEVEL` 控制，
通过 ``Off`` / ``Terse`` / ``Normal`` / ``Verbose`` 选择项配置
（:kconfig:option:`CONFIG_ASSERT_MODULE_DEFAULT_LEVEL_OFF` /
``CONFIG_ASSERT_MODULE_DEFAULT_LEVEL_TERSE`` /
``CONFIG_ASSERT_MODULE_DEFAULT_LEVEL_NORMAL`` /
:kconfig:option:`CONFIG_ASSERT_MODULE_DEFAULT_LEVEL_VERBOSE`）。
运行 Zephyr 测试用例时断言默认启用，
由 :kconfig:option:`CONFIG_TEST` 选项配置。

已弃用的旧符号仍被遵循，并派生 ``DEFAULT`` 模块
级别：:kconfig:option:`CONFIG_ASSERT_VERBOSE` 映射到 ``Verbose``，
:kconfig:option:`CONFIG_ASSERT_NO_COND_INFO`、
:kconfig:option:`CONFIG_ASSERT_NO_MSG_INFO` 和
:kconfig:option:`CONFIG_ASSERT_NO_FILE_INFO` 映射到 ``Terse``，
而 :kconfig:option:`CONFIG_ASSERT_LEVEL` ``== 0`` 使其保持 ``Off``。
当这些选项都未设置时，``DEFAULT`` 模块选择项回落到其自身的
:kconfig:option:`CONFIG_ASSERT_MODULE_DEFAULT_LEVEL_VERBOSE` 默认值，
保留"详细断言为默认"的旧行为。
要禁用所有断言（无论级别如何配置），请设置 ``CONFIG_ASSERT=n``。

API 参考
*************

.. doxygengroup:: zassert
