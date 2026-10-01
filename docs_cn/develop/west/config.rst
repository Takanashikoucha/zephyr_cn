.. _west-config:

配置
#############

本页记录 west 的配置文件系统、``west config`` 命令以及内置命令所使用的配置选项。
关于 ``west.configuration`` 模块的 API 文档，请参见 :ref:`west-apis-configuration`。

West 配置文件
------------------------

West 的配置文件语法类似 INI，以下是一个示例文件：

.. code-block:: ini

   [manifest]
   path = zephyr

   [zephyr]
   base = zephyr

在上面这个文件中，``manifest`` 节的选项 ``path`` 被设置为 ``zephyr``。
换一种说法，即该文件中 ``manifest.path`` 的值为 ``zephyr``。

配置文件共有三种类型：

1. **系统**：该文件中的设置影响该计算机上所有已登录用户的 west 行为。
   其位置取决于平台：

   - Linux: :file:`/etc/westconfig`
   - macOS: :file:`/usr/local/etc/westconfig`
   - Windows: :file:`%PROGRAMDATA%\\west\\config`

2. **全局**（每个用户一份）：该文件中的设置影响特定用户在该计算机上运行 west 时的行为。

   - 所有平台：默认值为用户主目录下的 :file:`.westconfig`。
   - Linux 注意：如果设置了环境变量 ``XDG_CONFIG_HOME``，
     则使用 :file:`$XDG_CONFIG_HOME/west/config`。
   - Windows 注意：会依次检测以下环境变量来确定主目录：
     ``%HOME%``，然后是 ``%USERPROFILE%``，
     再然后是 ``%HOMEDRIVE%`` 与 ``%HOMEPATH%`` 的组合。

3. **本地**：该文件中的设置影响 west 在当前 :term:`west workspace` 中的行为。
   该文件为 :file:`.west/config`，相对于工作区根目录。

在列表中位置靠后的文件中的设置会覆盖靠前的设置。
例如，如果系统配置文件中 ``color.ui`` 为 ``true``，
而工作区配置文件中为 ``false``，则最终值为 ``false``。
同理，用户配置文件中的设置覆盖系统设置，依此类推。

.. _west-config-cmd:

west config
-----------

内置的 ``config`` 命令可用于获取和设置配置值。
可以向 ``west config`` 传入 ``--system``、``--global`` 或 ``--local``
选项来指定使用哪个配置文件。这些选项一次只能使用一个。
如果都不指定，则写入操作默认作用于 ``--local``，
读取操作则显示应用所有覆盖之后的最终值。

下面是一些常见用法的示例；运行 ``west config -h`` 可查看详细帮助，
更多内置选项的说明请参见 :ref:`west-config-index`。

将 ``manifest.path`` 设置为 :file:`some-other-manifest`：

.. code-block:: console

   west config manifest.path some-other-manifest

执行上述命令后，``west update`` 等命令会在 :file:`some-other-manifest`
目录（相对于工作区根目录）中查找 :term:`west manifest`，
而不是 ``west init`` 时给出的目录，因此请小心！

读取 ``zephyr.base``，即当调用环境中未设置 ``ZEPHYR_BASE`` 时
将要使用的值（同样相对于工作区根目录）：

.. code-block:: console

   west config zephyr.base

在不更改 ``manifest.path``（从而也不改变 ``west update`` 等命令行为）
的情况下切换到另一个 zephyr 仓库，可以使用：

.. code-block:: console

   west config zephyr.base some-other-zephyr

如果你使用 ``git worktree`` 等命令创建自己的 zephyr 目录，并希望
``west build`` 等命令使用它们而不是 manifest 中指定的 zephyr 仓库，
这会很有用。（运行 ``west config zephyr.base zephyr`` 即可恢复使用
上游 manifest 中的目录。）

将 ``color.ui`` 在全局（用户级）配置文件中设置为 ``false``，
使 west 在该用户任何工作区中运行时都不再输出彩色内容：

.. code-block:: console

   west config --global color.ui false

撤销上述更改：

.. code-block:: console

   west config --global color.ui true

.. _west-config-index:

内置配置选项
------------------------------

下表记录了 west 内置命令支持的配置选项。
Zephyr 扩展命令支持的配置选项在相应命令的页面中有文档说明。

.. NOTE: docs authors: keep this table sorted by section, then option.

.. list-table::
   :widths: 10 30
   :header-rows: 1

   * - 选项
     - 说明
   * - :samp:`alias.{ALIAS}`
     - 字符串。如果非空，``<ALIAS>`` 可作为 west 命令使用。
       参见 :ref:`west-aliases`。
   * - ``color.ui``
     - 布尔值。如果为 ``true``（默认值），则当标准输出为终端时，
       west 的输出会带颜色。
   * - ``commands.allow_extensions``
     - 布尔值，默认 ``true``；为 ``false`` 时禁用 :ref:`west-extensions`。
   * - ``grep.color``
     - 字符串，默认为空。设置为 ``never`` 可禁用 ``west grep`` 的彩色输出。
       如果已设置，``west grep`` 会把该值传递给 grep 工具的 ``--color`` 选项。
   * - ``grep.tool``
     - 字符串，取值为 ``"git-grep"``（默认）、``"ripgrep"`` 或 ``"grep"`` 之一。
       即 ``west grep`` 应使用的 grep 工具。
   * - ``grep.<TOOL>-args``
     - 字符串，默认为空。``<TOOL>`` 部分是一个模式，可以是任意
       ``grep.tool`` 的取值，例如 ``grep.ripgrep-args`` 就是一个配置选项示例。
       如果已设置，则为 ``west grep`` 应传递给对应 grep 工具的参数。
       运行 ``west help grep`` 查看详情。
   * - ``grep.<TOOL>-path``
     - 字符串，默认为空。``<TOOL>`` 部分是一个模式，可以是任意
       ``grep.tool`` 的取值，例如 ``grep.ripgrep-path`` 就是一个配置选项示例。
       即 ``west grep`` 应使用的对应工具的路径，而不是搜索该命令。
       运行 ``west help grep`` 查看详情。
   * - ``manifest.file``
     - 字符串，默认 ``west.yml``。从 manifest 仓库根目录到 ``west init``
       及其他解析 manifest 的命令所使用的 manifest 文件的相对路径。
   * - ``manifest.group-filter``
     - 字符串，默认为空。工作区内要启用和禁用的项目组的逗号分隔列表。
       启用的组前缀为 ``+``，禁用的组前缀为 ``-``。例如，取值
       ``"+foo,-bar"`` 启用组 ``foo`` 并禁用组 ``bar``。
       参见 :ref:`west-manifest-groups`。
   * - ``manifest.path``
     - 字符串，从 :term:`west workspace` 根目录到 ``west update`` 及其他
       解析 manifest 的命令所使用的 manifest 仓库的相对路径。
       由 ``west init`` 本地设置。
   * - ``manifest.project-filter``
     - 字符串的逗号分隔列表。

       该选项的取值是正则表达式的逗号分隔列表，
       每项以 ``+`` 或 ``-`` 开头，形如：

       .. code-block:: none

          +re1,-re2,-re3

       项目名会按顺序与列表中的每个正则表达式（``re1``、``re2``、
       ``re3``、...）进行匹配。如果项目名整体匹配某个正则表达式，
       则列表中的该项会停用或启用该项目。该项以 ``-`` 开头时项目被停用；
       以 ``+`` 开头时项目被启用。（如果使用了本选项，项目名中不能包含
       ``,``，因此正则表达式中也不需要包含字面的 ``,`` 字符。）

       如果项目名匹配了列表中的多个正则表达式，
       则以最后一个正则表达式的结果为准。例如，
       如果 ``manifest.project-filter`` 为：

       .. code-block:: none

          -hal_.*,+hal_foo

       则名为 ``hal_bar`` 的项目处于非活动状态，
       而名为 ``hal_foo`` 的项目处于活动状态。

       如果项目因列表中的某一项而被停用或启用，
       则无论其所属的组是否被禁用（部分或全部），
       该项目都处于活动或非活动状态。
       （目前这是让没有组的某个项目处于非活动状态的唯一方式。）

       否则，即项目不匹配列表中任何正则表达式时，
       其活动或非活动状态按照与其组相关的通常规则确定
       （参见 :ref:`west-project-group-examples` 中的示例）。

       在 ``manifest.project-filter`` 列表的某一项内部，
       前导和尾随空白会被忽略。也就是说，以下示例取值等价：

       .. code-block:: none

          +foo,-bar
          +foo , -bar

       空项会被忽略。也就是说，以下示例取值等价：

       .. code-block:: none

          +foo,,-bar
          +foo,-bar

   * - ``update.auto-cache``
     - 字符串。如果非空，``west update`` 在未于命令行给出
       ``--auto-cache`` 选项时，会将其取值作为 ``--auto-cache`` 选项的值。
   * - ``update.fetch``
     - 字符串，取值为 ``"smart"``（v0.6.1 起的默认行为）或
       ``"always"``（之前的行为）。如果设置为 ``"smart"``，
       当 manifest 文件中项目的修订号为本地已存在的 SHA 或标签时，
       :ref:`west-update` 命令会跳过从项目远程仓库获取。
       ``"always"`` 行为则是无条件从远程仓库获取。
   * - ``update.name-cache``
     - 字符串。如果非空，``west update`` 在未于命令行给出
       ``--name-cache`` 选项时，会将其取值作为 ``--name-cache`` 选项的值。
   * - ``update.narrow``
     - 布尔值。如果为 ``true``，``west update`` 的行为如同在命令行
       给出了 ``--narrow`` 选项。默认值为 ``false``。
   * - ``update.path-cache``
     - 字符串。如果非空，``west update`` 在未于命令行给出
       ``--path-cache`` 选项时，会将其取值作为 ``--path-cache`` 选项的值。
   * - ``update.sync-submodules``
     - 布尔值。如果为 ``true``（默认值），:ref:`west-update` 会先同步
       Git 子模块再更新它们。
   * - ``zephyr.base``
     - 字符串，west 命令运行期间为 :envvar:`ZEPHYR_BASE` 环境变量
       设置的默认值。默认情况下，``west init`` 期间会将其设置为
       路径为 :file:`zephyr` 的 manifest 项目的路径（如果存在）。
       如果该环境变量已经设置，则除非 ``zephyr.base-prefer`` 为
       ``"configfile"``，否则忽略本设置。
   * - ``zephyr.base-prefer``
     - 字符串，取值为 ``"env"`` 和 ``"configfile"`` 之一。如果设置为
       ``"env"``（默认值），则在调用环境中设置的 :envvar:`ZEPHYR_BASE`
       会覆盖 ``zephyr.base`` 配置选项的值。如果设置为
       ``"configfile"``，则配置选项的值优先。
