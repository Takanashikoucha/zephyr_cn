.. _kconfig_extensions:

Kconfig 扩展
##################

Zephyr 使用 `Kconfiglib <https://github.com/zephyrproject-rtos/Kconfiglib>`__
实现的 `Kconfig
<https://docs.kernel.org/kbuild/kconfig-language.html>`__，
其中包含一些 Kconfig 扩展：

- 默认值可以通过使用 ``configdefault`` 应用于现有符号，
  而不通过 :ref:`削弱 <multiple_symbol_definitions>` 符号的依赖关系。

  .. code-block:: none

     config FOO
         bool "FOO"
         depends on BAR

     configdefault FOO
         default y if FIZZ

  上面的语句等价于：

  .. code-block:: none

     config FOO
         bool "Foo"
         default y if FIZZ
         depends on BAR

  ``configdefault`` 符号不能包含 ``default`` 之外的任何字段，不过它们可以被包裹
  在 ``if`` 语句中。下面两个语句等价：

  .. code-block:: none

     configdefault FOO
         default y if BAR

     if BAR
     configdefault FOO
         default y
     endif # BAR

- ``source`` 语句中的环境变量被直接展开，意味着无需定义带有
  ``option env="ENV_VAR"`` 的 "bounce" 符号。

  .. note::

     自 Linux 4.18 起，``option env`` 也从 C 工具中移除了。

  引用环境变量的推荐语法是 ``$(FOO)`` 而非 ``$FOO``。这使用新的
  `Kconfig 预处理器
  <https://docs.kernel.org/kbuild/kconfig-macro-language.html>`__。
  展开环境变量的 ``$FOO`` 语法仅为向后兼容而支持。

- ``source`` 语句支持 glob 模式并包含每个匹配文件。模式必须匹配至少一个文件。

  考虑以下示例：

  .. code-block:: kconfig

     source "foo/bar/*/Kconfig"

  如果模式 ``foo/bar/*/Kconfig`` 匹配文件 :file:`foo/bar/baz/Kconfig` 和
  :file:`foo/bar/qaz/Kconfig`，上面的语句等价于以下两个 ``source`` 语句：

  .. code-block:: kconfig

     source "foo/bar/baz/Kconfig"
     source "foo/bar/qaz/Kconfig"

  如果没有文件匹配模式，会生成错误。

  接受的通配符模式与 Python `glob
  <https://docs.python.org/3/library/glob.html>`__ 模块的相同。

  对于模式匹配不到文件（或普通文件名不存在）也没关系的情况，有一个单独的
  ``osource``（*optional source*，可选源）语句可用。``osource`` 在没有文件匹配时
  是无操作。

  .. note::

     ``source`` 和 ``osource`` 类似于 Make 中的 ``include`` 和 ``-include``。

- 有 ``rsource`` 语句可用于包含使用相对路径指定的文件。路径相对于包含
  ``rsource`` 语句的 :file:`Kconfig` 文件的目录。

  例如，假设 :file:`foo/Kconfig` 是顶层 :file:`Kconfig` 文件，且
  :file:`foo/bar/Kconfig` 有以下语句：

  .. code-block:: kconfig

     source "qaz/Kconfig1"
     rsource "qaz/Kconfig2"

  这将包含两个文件 :file:`foo/qaz/Kconfig1` 和 :file:`foo/bar/qaz/Kconfig2`。

  ``rsource`` 可以用于创建 :file:`Kconfig` "子树"，可以自由移动。

  ``rsource`` 也支持 glob 模式。

  ``rsource`` 的缺点是它可能使弄清楚文件从哪里被包含更困难，因此只在需要时使用。

- 有 ``orsource`` 语句可用，它组合 ``osource`` 和 ``rsource``。

  例如，以下语句将包含当前目录中的 :file:`Kconfig1` 和 :file:`Kconfig2`
  （如果它们存在）：

  .. code-block:: kconfig

     orsource "Kconfig[12]"

- ``def_int``、``def_hex`` 和 ``def_string`` 关键字可用，类似于 ``def_bool``。
  这些同时设置类型并添加 ``default``。

- 符号名称可以使用 ``choice <symbol>`` 语法关联到 ``choice`` 组。这种 choice，
  称为 *命名 choice*，可以从其初始定义之外的地方修改。例如，以下语句定义命名
  choice ``FOOBAR``：

  .. code-block:: kconfig

    choice FOOBAR
        prompt "Example choice"
        default BAR

    config FOO
        bool "Foo"

    config BAR
        bool "Bar"

    endchoice

  然后以下语句可以在例如 ``Kconfig.defconfig`` 文件中使用，以覆盖 choice
  ``FOOBAR`` 的默认选项：

  .. code-block:: kconfig

    # Note how "prompt" is not present here
    choice FOOBAR
        default FOO
    endchoice

  .. note::
    *命名 choice* 功能源自 Linux，但自 kernel release 6.9 起 Linux 不再支持它，
    因此它成为了 Kconfiglib 语言扩展。
