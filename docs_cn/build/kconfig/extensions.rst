.. _kconfig_extensions:

Kconfig 扩展
##################

Zephyr 使用 `Kconfiglib <https://github.com/zephyrproject-rtos/Kconfiglib>`__
实现的 `Kconfig
<https://docs.kernel.org/kbuild/kconfig-language.html>`__，
其中包含一些 Kconfig 扩展：

- 默认值可以通过使用 ``configdefault``
  应用于现有符号而
  不通过
  :ref:`削弱 <multiple_symbol_definitions>` 符号的依赖关系。

  .. code-block:: none

     config FOO
         bool "FOO"
         depends on BAR

     configdefault FOO
         default y if FIZZ

  上面的
  语句
  等价于：

  .. code-block:: none

     config FOO
         bool "Foo"
         default y if FIZZ
         depends on BAR

  ``configdefault`` 符号
  不能
  包含
  ``default`` 之外的
  任何
  字段，
  不过
  它们
  可以
  被
  包裹
  在
  ``if`` 语句
  中。
  下面
  两个
  语句
  等价：

  .. code-block:: none

     configdefault FOO
         default y if BAR

     if BAR
     configdefault FOO
         default y
     endif # BAR

- ``source`` 语句
  中
  的
  环境变量
  被
  直接
  展开，
  意味着
  无需
  定义
  带有
  ``option env="ENV_VAR"`` 的
  "bounce" 符号。

  .. note::

     自
     Linux 4.18 起，
     ``option env``
     也
     从
     C 工具
     中
     移除
     了。

  引用
  环境变量
  的
  推荐
  语法
  是
  ``$(FOO)`` 而非
  ``$FOO``。
  这
  使用
  新的
  `Kconfig 预处理器
  <https://docs.kernel.org/kbuild/kconfig-macro-language.html>`__。
  展开
  环境变量
  的
  ``$FOO`` 语法
  仅
  为
  向后
  兼容
  而
  支持。

- ``source`` 语句
  支持
  glob 模式
  并
  包含
  每个
  匹配
  文件。
  模式
  必须
  匹配
  至少
  一个
  文件。

  考虑
  以下
  示例：

  .. code-block:: kconfig

     source "foo/bar/*/Kconfig"

  如果
  模式
  ``foo/bar/*/Kconfig`` 匹配
  文件
  :file:`foo/bar/baz/Kconfig` 和
  :file:`foo/bar/qaz/Kconfig`，
  上面
  的
  语句
  等价于
  以下
  两个
  ``source`` 语句：

  .. code-block:: kconfig

     source "foo/bar/baz/Kconfig"
     source "foo/bar/qaz/Kconfig"

  如果
  没有
  文件
  匹配
  模式，
  会
  生成
  错误。

  接受的
  通配符
  模式
  与
  Python `glob
  <https://docs.python.org/3/library/glob.html>`__ 模块
  的
  相同。

  对于
  模式
  匹配
  不到
  文件
  （或
  普通
  文件名
  不
  存在）
  也没
  关系
  的
  情况，
  有
  一个
  单独的
  ``osource``（*optional source*，
  可选
  源）
  语句
  可用。
  ``osource``
  在
  没有
  文件
  匹配
  时
  是
  无
  操作。

  .. note::

     ``source`` 和
     ``osource``
     类似于
     Make 中
     的
     ``include`` 和
     ``-include``。

- 有
  ``rsource`` 语句
  可用
  于
  包含
  使用
  相对
  路径
  指定
  的
  文件。
  路径
  相对于
  包含
  ``rsource`` 语句
  的
  :file:`Kconfig` 文件
  的
  目录。

  例如，
  假设
  :file:`foo/Kconfig` 是
  顶层
  :file:`Kconfig` 文件，
  且
  :file:`foo/bar/Kconfig` 有
  以下
  语句：

  .. code-block:: kconfig

     source "qaz/Kconfig1"
     rsource "qaz/Kconfig2"

  这
  将
  包含
  两个
  文件
  :file:`foo/qaz/Kconfig1` 和
  :file:`foo/bar/qaz/Kconfig2`。

  ``rsource``
  可以
  用于
  创建
  :file:`Kconfig` "子树"，
  可以
  自由
  移动。

  ``rsource``
  也
  支持
  glob 模式。

  ``rsource``
  的
  缺点
  是
  它
  可能
  使
  弄清楚
  文件
  从
  哪里
  被
  包含
  更
  困难，
  因此
  只在
  需要
  时
  使用。

- 有
  ``orsource`` 语句
  可用，
  它
  组合
  ``osource`` 和
  ``rsource``。

  例如，
  以下
  语句
  将
  包含
  当前
  目录
  中
  的
  :file:`Kconfig1` 和
  :file:`Kconfig2`（如果
  它们
  存在）：

  .. code-block:: kconfig

     orsource "Kconfig[12]"

- ``def_int``、``def_hex`` 和
  ``def_string`` 关键字
  可用，
  类似于
  ``def_bool``。
  这些
  同时
  设置
  类型
  并
  添加
  ``default``。

- 符号
  名称
  可以
  使用
  ``choice <symbol>`` 语法
  关联
  到
  ``choice`` 组。
  这种
  choice，
  称为
  *命名
  choice*，
  可以
  从
  其
  初始
  定义
  之外
  的
  地方
  修改。
  例如，
  以下
  语句
  定义
  命名
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

  然后
  以下
  语句
  可以
  在
  例如
  ``Kconfig.defconfig`` 文件
  中
  使用，
  以
  覆盖
  choice ``FOOBAR`` 的
  默认
  选项：

  .. code-block:: kconfig

    # 注意
    # 这里
    # 没有
    # "prompt"
    choice FOOBAR
        default FOO
    endchoice

  .. note::
    *命名
    choice* 功能
    源自
    Linux，
    但
    自
    kernel
    release
    6.9 起
    Linux
    不再
    支持
    它，
    因此
    它
    成为
    了
    Kconfiglib
    语言
    扩展。
