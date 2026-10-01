.. _west-release-notes:

West 发行说明
##################

v1.5.0
******

主要更改：

- 添加自动缓存支持。
  向 ``west update`` 传递 ``--auto-cache <directory>`` 参数。

其他更改：

- 允许在 ``west update`` 中组合使用 ``--name-cache`` 和 ``--path-cache``。

- 在 manifest schema 中记录默认 revision 值。

缺陷修复：

- 允许 manifest projects 列表为空或缺失。

- 使 ``manifest.group-filter`` 列表顺序在冻结或解析 manifest 文件时确定。

v1.4.0
******

更改：

- 允许向配置字符串追加数据。
  要向 ``<name>`` 的值追加，输入：``west config -a <name> <value>``。

- 为 ``west manifest`` 添加 ``--untracked`` 参数选项。
  在工作区中运行 ``west manifest --untracked``，可打印所有未被 west
  跟踪或管理的文件和目录。

- 为 ``west list`` 添加 ``--inactive`` 参数选项，以支持打印非活动项目。

- 为 ``west manifest --resolve`` 和 ``west manifest --freeze`` 命令支持
  ``--active-only`` 参数选项。
  这使得可以冻结带有活动项目或组过滤器的区。

API 更改：

- ``west.manifest.Manifest`` 的 ``as_dict()``、``as_frozen_dict()``、``as_yaml()``
  和 ``as_frozen_yaml()`` 方法现在有一个可选的 ``active_only`` 参数（默认值为
  ``False``），用于返回包含所有项目或仅包含活动项目的对象。

v1.3.0
******

主要更改：

- 添加对 :ref:`west-aliases` 命令的支持。

- 采用 `pyproject TOML 规范`_ 用于打包。

.. _pyproject TOML specification:
   https://packaging.python.org/en/latest/specifications/pyproject-toml/

其他更改：

- 为子模块添加缓存支持。

- 默认将 manifest 文件解码为 UTF-8。

- 将 ``west diff`` 和 ``west status`` 的未知参数传递给底层 ``git`` 命令。

- 为 ``west diff`` 添加 ``--manifest`` 参数，以允许将当前工作区
  与 manifest 的 revision 进行比较。

- 环境变量可用于 west forall
  定义了以下变量：

  - ``WEST_PROJECT_NAME``
  - ``WEST_PROJECT_PATH``
  - ``WEST_PROJECT_ABSPATH``
  - ``WEST_PROJECT_REVISION``
  - ``WEST_PROJECT_URL``
  - ``WEST_PROJECT_REMOTE``

- 添加对早期参数 ``-q/--quiet`` 的支持，以减少冗长输出。

- 为 ``west init`` 添加 ``-o/--clone-opt`` 参数，以传递给 ``git clone``。

- 支持 Python 3.13，并移除对 Python 3.8 的支持。

- 防止 manifest 在 ``.west`` 目录中放置项目。

- 为 ``west init`` 添加 NTFS 变通方案和 ``--rename-delay``。

- 在调试 ``-vvv`` 下调用 die 时打印堆栈跟踪。

缺陷修复：

- 使用 ``'backslashreplace'`` 以避免在子进程输出畸形 UTF 时崩溃。

- 修复 ``west diff`` 对存在合并冲突的仓库的处理。
  同时改进错误打印并处理 ``git diff`` 返回码。

- 修复使用 git 子模块时 ``west manifest`` 命令的 ``--freeze`` 和 ``--resolve``。

v1.2.0
******

主要更改：

- 新的 ``west grep`` 命令，用于在 west 工作区的仓库中运行
  "grep 工具"。目前，``git grep``、`ripgrep`_ 和标准 ``grep`` 是
  受支持的 grep 工具。

  要在所有已克隆的活动仓库中获取 ``git grep foo`` 的结果，
  运行：

  .. code-block:: console

     west grep foo

  以下是使用 ``west grep`` 运行不同 grep 命令的其他示例：

  .. list-table::

     * - ``git grep --untracked``
       - ``west grep --untracked foo``
     * - ``ripgrep``
       - ``west grep --tool ripgrep foo``
     * - ``grep --recursive``
       - ``west grep --tool grep foo``

  要切换工作区的默认 grep 工具，运行本表中的相应
  命令：

  .. list-table::

     * - ``ripgrep``
       - ``west config grep.tool ripgrep``
     * - ``grep``
       - ``west config grep.tool grep``

  要了解更多详情，运行 ``west help grep``。

其他更改：

- manifest 文件格式现在支持每个 ``projects:`` 元素中的 ``description`` 字段。
  示例参见 :ref:`west-manifests-projects`。

- ``west list --format`` 现在在格式字符串中接受 ``{description}``，
  它会打印项目的 ``description:`` 值。

- ``west compare`` 现在总是打印关于
  :ref:`west-manifest-rev` 的信息。

缺陷修复：

- 如果目标目录已存在，``west init`` 会中止。

API 更改：

- ``west.commands.WestCommand`` 的 ``check_call()`` 和
  ``check_output()`` 方法现在接受任何可以传递给
  底层子进程函数的 kwargs。

- ``west.commands.WestCommand.run_subprocess()``：
  ``subprocess.run()`` 的新包装器。之所以不能命名为 ``run()``，
  是因为 ``WestCommand`` 已经有一个同名的方法。

- ``west.commands.WestCommand`` 的 ``dbg()``、``inf()``、
  ``wrn()`` 和 ``err()`` 方法现在都接受一个 ``end`` kwarg，
  它会被传递给对 ``print()`` 的调用。

- ``west.manifest.Project`` 现在有一个 ``description`` 属性，
  它包含 manifest 数据中 ``description:`` 字段的解析值。

.. _ripgrep: https://github.com/BurntSushi/ripgrep#readme

v1.1.0
******

主要更改：

- ``west compare``：将工作区状态与 manifest 进行比较的新命令。

- 支持新的 ``manifest.project-filter`` 配置选项。
  详情参见 :ref:`west-config-index`。当设置了该选项时，
  ``west manifest --freeze`` 和 ``west manifest --resolve`` 命令目前无法使用。
  此限制可在后续版本中移除。

- 包含逗号（``,``）或空白的项目名称现在会生成
  警告。如果设置了新的 ``manifest.project-filter``
  配置选项，这些警告将成为错误。在 west 的某个未来主要版本中，
  这些警告可能会被提升为错误。

其他更改：

- ``west forall`` 现在接受一个 ``--group`` 参数，可用于
  将命令限制为仅在一个或多个组中运行。运行
  ``west help forall`` 了解详情。

- 所有 west 命令现在都会输出 west API 模块中
  警告级别或更高级别的日志消息。此外，west 的 ``--verbose`` 参数
  可使用一次以包含信息性消息，或使用两次以包含
  所有命令的调试消息。

缺陷修复：

- 对错误消息、调试日志记录和错误处理的各项改进。

API 更改：

- ``west.manifest.Manifest.is_active()`` 现在遵循
  ``manifest.project-filter`` 配置选项的值。

v1.0.1
******

主要更改：

- manifest schema 版本 "1.0" 现在可在本版本中使用。就
  功能而言，它与 "0.13" schema 版本完全相同，但可供不希望使用 "0.x"
  manifest "version:" 字段的应用程序使用。此功能的详情参见 :ref:`west-manifest-schema-version`。

缺陷修复：

- west 在收到中断信号时不再以成功的错误码退出。
  相反，它以一个平台相关的错误码退出，并向调用环境发出
  进程被中断的信号。

v1.0.0
******

本版本的主要更改：

- :ref:`west-apis` 现在被声明为稳定。任何破坏性更改都
  将通过从 v1.x.y 到 v2.x.y 的主要版本升级来通知。

- West v1.0 不再与 Zephyr v1.14 LTS 版本兼容。该 LTS
  早已被 Zephyr v2.7 LTS 取代。如果你需要使用 Zephyr v1.14，
  必须使用 west v0.14 或更早版本。

- 与 Zephyr 的其他部分一样，west 现在要求 Python v3.8 或更高版本

- west 命令不再接受缩写形式的命令行参数。
  例如，现在必须指定 ``west update --keep-descendants``，而不能
  使用 ``west update --keep-d`` 这样的缩写。这是应用于
  Zephyr 所有 Python 脚本命令行接口的一项更改。
  当命令更新为添加与现有选项名称相似但行为不同的新选项时，
  缩写在实践中造成了问题。

其他更改：

- 所有内置 west 函数已停止使用 ``west.log``

- ``west update``：新的 ``--submodule-init-config`` 选项。
  详情参见 commit `9ba92b05`_。

缺陷修复：

- 加载失败的 west 扩展命令有时会打印堆栈跟踪。
  这已修复，west 现在在这种情况下会打印合理的错误消息。

- ``west config`` 现在会在缺少选项名称中 ``.`` 的
  格式错误的配置选项参数上失败

API 更改：

- west 包现在包含一些静态
  分析器（如 `mypy`_）自动检测其类型注解所需的元数据文件。
  详情参见 commit `d9f00e24`_。

- 用于 Zephyr v1.14 LTS 兼容性的已弃用 ``west.build`` 模块
  已被移除

- 用于 Zephyr v1.14 LTS 兼容性的已弃用 ``west.cmake`` 模块
  已被移除

- ``west.log`` 模块现在已弃用。该模块使用全局状态，
  这使得将其作为 API 使用时可能不太方便，因为多个不同的 python
  模块都可能依赖它。

- :ref:`west-apis-commands` 模块新增了一些 API，为未来的一项更改
  （为命令输出添加全局冗长度控制）奠定基础，
  并着手从 ``west`` 包的 API 中移除全局状态：

  - 新的 ``west.commands.WestCommand.__init__()`` 关键字参数：``verbosity``
  - 新的 ``west.commands.WestCommand`` 属性：``color_ui``
  - 新的 ``west.commands.WestCommand`` 方法，扩展命令应使用这些方法
    打印输出，而不是直接写入 sys.stdout 或
    sys.stderr：``inf()``、``wrn()``、``err()``、``die()``、``banner()``、
    ``small_banner()``
  - 新的 ``west.commands.VERBOSITY`` 枚举

.. _9ba92b05: https://github.com/zephyrproject-rtos/west/commit/9ba92b054500d75518ff4c4646590bfe134db523
.. _d9f00e24: https://github.com/zephyrproject-rtos/west/commit/d9f00e242b8cb297b56e941982adf231281c6bae
.. _mypy: https://www.mypy-lang.org/

v0.14.0
*******

缺陷修复：

- 使用格式错误的本地配置文件运行的 west 命令
  会以令人困惑的方式打印堆栈跟踪。这已修复，west 现在在这种情况下
  会打印合理的错误消息。

- 修复了 west 查找 zephyr 仓库方式中的一个缺陷。该
  缺陷本身通常出现在新的工作区中第一次运行 ``west build``
  这样的扩展命令时；除非你在工作区的顶层目录中
  运行该命令，否则以前会失败（只是第一次，后续命令调用不会失败）。

- 当用户没有权限打开 manifest 文件时，west 现在会打印
  合理的错误消息，而不是打印堆栈跟踪。

API 更改：

- ``west.manifest.MalformedConfig`` 异常类型已移动到
  ``west.configuration`` 模块

- ``west.manifest.MalformedConfig`` 异常类型已移动到
  :ref:`west.configuration <west-apis-configuration>` 模块

- ``west.configuration.Configuration`` 类现在在某些情况下
  抛出 ``MalformedConfig`` 而不是 ``RuntimeError``

v0.13.1
*******

缺陷修复：

- 在工作区之外调用 west.manifest.Manifest.from_file() 时，
  west 重新回退到 ZEPHYR_BASE 环境变量
  来定位工作区。

v0.13.0
*******

新功能：

- 你现在可以在 ``manifest: self: userdata:`` 值中将任意用户数据
  与 manifest 仓库本身关联，如下所示：

  .. code-block:: YAML

     manifest:
       self:
         userdata: <any YAML value can go here>

缺陷修复：

- 在 [issue
  #572](https://github.com/zephyrproject-rtos/west/issues/572) 中详述的某些情况下，
  west 报告的 manifest 仓库路径可能不正确。这已作为
  ``west.manifest`` API 模块中路径处理支持的一次更大规模重整的一部分
  得到修复。

- 修复了 ``west.Manifest.ManifestProject.__repr__`` 的返回值

:ref:`API <west-apis>` 更改：

- ``west.configuration.Configuration``：当前配置的新面向对象接口。
  它反映系统、全局和工作区本地配置值，并允许你
  从任意或所有这些位置读取、写入和删除配置
  选项。

- ``west.commands.WestCommand``：

  - ``config``：新属性，返回一个 ``Configuration`` 对象，如果未设置则
    中止程序。在扩展命令 ``do_run()`` 实现内部
    始终可用。
  - ``has_config``：新的布尔属性，当且仅当
    读取 ``self.config`` 会中止程序时为 ``True``。

- ``west.manifest`` 包中的路径处理已经
  以向后不兼容的方式被重整。更多详情参见 commit
  [56cfe8d1d1](https://github.com/zephyrproject-rtos/west/commit/56cfe8d1d1f3c9b45de3e793c738acd62db52aca)。

- ``west.manifest.Manifest.validate()``：现在返回验证后的数据
  作为 Python dict。如果传递给该函数的值是一个
  str，且需要 dict，这会很有用。

- ``west.manifest.Manifest``：新增：

  - path 属性 ``abspath``、``posixpath``、``relative_path``、
    ``yaml_path``、``repo_path``、``repo_posixpath``
  - ``userdata`` 属性，包含从 ``manifest: self: userdata:``
    解析的值，或为 None
  - ``from_topdir()`` 工厂方法

- ``west.manifest.ManifestProject``：新的 ``userdata`` 属性，同样
  包含从 ``manifest: self: userdata:`` 解析的值，或为 None

- ``west.manifest.ManifestImportFailed``：构造函数现在可以接受任何
  值；这可用于反映来自 :ref:`map
  <west-manifest-import-map>` 或其他复合值的导入失败。

- 已弃用的配置 API：

  以下 API 现在已弃用，建议使用 ``Configuration``
  对象。通常这会通过 ``WestCommand``
  实例的 ``self.config`` 来完成，但也可以直接实例化一个 ``Configuration``
  对象用于其他用途。

  - ``west.configuration.config``
  - ``west.configuration.read_config``
  - ``west.configuration.update_config``
  - ``west.configuration.delete_config``

v0.12.0
*******

新功能：

- West 现在可以在 `MSYS2 <https://www.msys2.org/>`_ 平台上运行。

- West manifest 文件现在可以包含与每个
  项目关联的任意用户数据。详情参见 :ref:`west-project-userdata`。

缺陷修复：

- ``west list`` 命令的 ``{sha}`` 格式键
  对 manifest 仓库已修复；现在会按预期打印 ``N/A``（"不适用"）。

:ref:`API <west-apis>` 更改：

- 添加了 ``west.manifest.Project.userdata`` 属性以支持
  项目用户数据。

v0.11.1
*******

新功能：

- ``west status`` 现在只为状态非空的
  项目打印输出。

缺陷修复：

- manifest 文件解析器错误地允许包含
  路径分隔符 ``/`` 和 ``\`` 的项目名称。这些无效字符现在
  会被拒绝。

  注意：如果你需要将项目放在工作区
  topdir 的子目录中，请使用 ``path:`` 键。如果你需要自定义项目相对于其 remote ``url-base:`` 的 fetch URL，请使用 ``repo-path:``。
  示例参见 :ref:`west-manifests-projects`。

- west v0.10.1 中对 ``west init --manifest-rev`` 选项
  所做的选择默认分支名称的更改，会使 manifest 仓库
  处于分离 HEAD 状态。这已通过内部改用 ``git clone``
  而不是 ``git init`` 和 ``git fetch`` 得到修复。详情参见 `issue #522`_。

- ``WEST_CONFIG_LOCAL`` 环境变量现在正确
  覆盖默认位置 :file:`<workspace topdir>/.west/config`。

- ``west update --fetch=smart``（``smart`` 是默认值）现在正确跳过
  对 `lightweight tags`_（轻量级标签）的 project revisions 的 fetch（它对
  注释标签已经能正确工作；只有轻量级标签会被不必要地
  fetch）。

其他更改：

- 上面提到的 issue #522 的修复引入了一个新的限制。
  ``west init --manifest-rev`` 选项值，如果给出，现在必须是一个
  分支或一个标签。特别是，以前可以用来 fetch 某个 pull
  请求的 GitHub 的 ``pull/1234/head`` 之类的"伪分支"
  现在不能再传递给 ``--manifest-rev``。用户现在必须在运行 ``west init`` 后
  手动 fetch 并检出这类 revision。

:ref:`API <west-apis>` 更改：

- ``west.manifest.Manifest.get_projects()`` 避免了
  `issue #523`_ 中描述的某些边缘情况下的错误结果。

- ``west.manifest.Project.sha()`` 现在对标签 revision 正确工作。
  （这适用于轻量级标签和注释标签两者。）

.. _lightweight tags: https://git-scm.com/book/en/v2/Git-Basics-Tagging
.. _issue #522: https://github.com/zephyrproject-rtos/west/issues/522
.. _issue #523: https://github.com/zephyrproject-rtos/west/issues/523

v0.11.0
*******

新功能：

- ``west update`` 现在支持 ``--narrow``、``--name-cache``、
  ``--path-cache`` 选项。这些可以受 ``update.narrow``、
  ``update.name-cache`` 和 ``update.path-cache`` :ref:`west-config` 选项的影响。
  这些可用于优化更新的速度。
- ``west update`` 现在支持一个 ``--fetch-opt`` 选项，它将被传递给
  更新每个项目时用于获取远程 revision 的 ``git fetch`` 命令。

缺陷修复：

- ``west update`` 现在默认同步项目中的 Git 子模块。
  这避免了 manifest 文件中的 URL 在子模块
  最初初始化后发生更改时出现的问题。可以通过将
  ``update.sync-submodules`` 配置选项设置为 ``false`` 来禁用
  此行为。

其他更改：

- :ref:`west-apis-manifest` 模块修复了 Project
  类的 docstring

v0.10.1
*******

新功能：

- :ref:`west-init` 命令的 ``--manifest-rev``（``--mr``）选项不再
  默认为 ``master``。相反，该命令会向仓库查询
  其默认分支名称并改用该名称。这允许用户从
  ``master`` 迁移到 ``main``，而不会破坏未提供该选项的
  脚本。

.. _west_0_10_0:

v0.10.0
*******

新功能：

- 项目 :ref:`submodules list
  <west-manifest-submodules>` 中的 ``name`` 键现在是可选的。

缺陷修复：

- West 现在检查 manifest schema 版本是否为
  :ref:`west-manifest-schema-version` 中记录的显式允许值之一。
  旧行为只是检查 schema 版本是否比引入 ``manifest: version:`` 键的 west
  版本更新。这错误地允许了无效的 schema 版本，
  例如 ``0.8.2``。

其他更改：

- manifest 文件的 ``group-filter`` 现在会通过 ``import`` 传播。
  这与 west v0.9.x 的处理方式不同。在 west v0.9.x 中，只有
  顶层 manifest 文件的 ``group-filter`` 有任何效果；任何被导入 manifest 的
  group filter 列表都会被忽略。

  从 west v0.10.0 开始，被导入 manifest 的
  group filter 列表也会被导入。详情参见 :ref:`west-group-filter-imports`。

  如果 ``manifest: version:`` 未给出或
  至少为 ``0.10``，新行为将生效。旧行为仍然仅在顶层
  manifest 文件中可用，需显式指定 ``manifest: version: 0.9``。
  关于 schema 版本的更多信息参见 :ref:`west-manifest-schema-version`。

  关于此更改的动机和额外背景，参见 `west pull request #482
  <https://github.com/zephyrproject-rtos/west/pull/482>`_。

v0.9.1
******

缺陷修复：

- 诸如 ``west manifest --resolve`` 之类的命令现在正确包含组
  和组过滤器信息。

其他更改：

- 如果你将 ``import`` 与 ``group-filter`` 组合使用，west 现在会发出警告。
  此组合的语义从 v0.10.x 开始已更改。
  更多信息参见上面 v0.10.0 的发行说明。

.. _west_0_9_0:

v0.9.0
******

.. warning::

   下面描述的 ``west config`` 修复是有代价的：通过该命令
   或 ``west.configuration`` API 设置配置选项时，配置文件中的任何注释或
   其他手动编辑都会被移除。

.. warning::

   不建议将本版本引入的 ``group-filter`` 功能与
   manifest 导入组合使用。由此产生的行为在 west
   v0.10 中已更改。

新功能：

- West manifest 现在支持 :ref:`west-manifest-submodules`。这允许你
  将 `Git submodules
  <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`_ 克隆到 west 项目
  仓库中，同时克隆项目仓库本身。

- West manifest 现在支持 :ref:`west-manifest-groups`。项目组可以
  被启用和禁用，以决定哪些项目是"活动"的，
  从而会被以下命令操作：``west update``、``west list``、
  ``west diff``、``west status``、``west forall``。

- ``west update`` 不再默认更新非活动项目。它现在
  支持一个 ``--group-filter`` 选项，允许对已启用和已禁用的项目组集合
  进行一次性修改。

- 不带参数运行 ``west list``、``west diff``、``west status`` 或 ``west forall``
  时，默认不打印非活动项目的信息。如果用户在命令行
  显式指定项目列表，则无论它们是否活动，都会包含
  它们的输出。

  这些命令现在还支持 ``--all`` 参数以包含所有
  项目，包括非活动项目。

- ``west list`` 现在在其 ``--format`` 参数中支持
  ``{groups}`` 格式字符串键。

缺陷修复：

- ``west config`` 命令和 ``west.configuration`` API 未能正确
  存储某些配置值，例如包含逗号的字符串。
  这已修复；详情参见 `commit 36f3f91e
  <https://github.com/zephyrproject-rtos/west/commit/36f3f91e270782fb05f6da13800f433a9c48f130>`_。

- ``manifest: self: path:`` 值为空的 manifest 文件是无效的，但
  west 以前会静默放行。West 现在会拒绝这类 manifest。

- 修复了影响 ``west init -l .`` 命令行为的缺陷；
  参见 `issue #435 <https://github.com/zephyrproject-rtos/west/issues/435>`_。

:ref:`API <west-apis>` 更改：

- 添加了 ``west.manifest.Manifest.is_active()``
- 添加了 ``west.manifest.Manifest.group_filter``
- 为 ``west.manifest.Project`` 添加了 ``submodules`` 属性，其类型
  为新添加的 ``west.manifest.Submodule``

其他更改：

- :ref:`west-manifest-import` 功能现在支持术语 ``allowlist``
  和 ``blocklist``，分别取代 ``whitelist`` 和 ``blacklist``。

  旧术语仍受支持以保持兼容性，但文档
  已更新为仅使用新术语。

v0.8.0
******

这是一个功能版本，通过在 ``import:`` 映射中添加对
``path-prefix:`` 键的支持来更改 manifest schema，
同时包含一些其他功能和修复。

- Manifest 导入映射现在支持 ``path-prefix:`` 键，它会将
  项目及其导入的仓库放在工作区的子目录中。
  示例参见 :ref:`west-manifest-ex3.4`。
- west 命令行应用程序现在也可以使用 ``python3 -m
  west`` 运行。这使得在特定 Python
  解释器下运行 west 更容易，而无需修改 :envvar:`PATH` 环境变量。
- :ref:`west manifest --path <west-manifest-path>` 打印
  west.yml 的绝对路径
- ``west init`` 现在支持一个 ``--mf foo.yml`` 选项，它使用
  :file:`foo.yml` 而不是 :file:`west.yml` 初始化
  工作区。
- ``west list`` 现在使用 ``manifest.path`` :ref:`configuration option <west-config>` 打印 manifest 仓库的路径，
  它可能与 manifest 数据中的 ``self: path:`` 值不同。旧行为
  仍然可用，但需要传递新的 ``--manifest-path-from-yaml``
  选项。
- 各种 Python API 更改；详情参见 :ref:`west-apis`。

v0.7.3
******

这是一个缺陷修复版本。

- 修复了一个错误：失败的导入可能使工作区处于不可用
  状态（详情参见 [PR #415](https://github.com/zephyrproject-rtos/west/pull/415)）

v0.7.2
******

这是一个缺陷修复和次要功能版本。

- 过滤掉 manifest 导入引入的重复扩展命令
- 修复通过路径查找 manifest 仓库时的
  ``west.Manifest.get_projects()``

v0.7.1
******

这是一个缺陷修复和次要功能版本。

- ``west update --stats`` 现在打印调用
  子进程的操作的耗时、west 的 Python 进程中每个项目花费的时间，
  以及更新每个项目的总时间。
- ``west topdir`` 总是打印 POSIX 风格路径
- 控制台输出的小改动

v0.7.0
******

west 0.7 中的主要用户可见功能是 :ref:`west-manifest-import`
 功能。它允许用户从多个不同的
 文件加载 west manifest 数据，并将结果解析为单一逻辑 manifest。

其他用户可见更改：

- "west 安装"的概念在本文档和 west API 文档中
  已更名为"west 工作区"。对新术语，大多数人似乎
  比旧术语更容易上手。
- West manifest 现在支持 :ref:`schema version
  <west-manifest-schema-version>`。
- "west config" 命令现在可以在工作区之外运行，例如
  运行 ``west config --global section.key value`` 全局
  设置某个配置选项的值。
- 新增 :ref:`west topdir <west-built-in-misc>` 命令，
  打印当前 west 工作区的根目录。
- ``west -vv init`` 命令现在打印正在执行的 git 操作
  及其结果。
- 现在强制执行"项目不能命名为 manifest"的限制；
  名称 "manifest" 保留给 manifest 仓库，
  可以在像 ``west list manifest`` 这样的命令中直接作为
  该仓库使用，而不必再像 ``west list
  path-to-manifest-repository`` 那样指定路径
- 没有名为 "zephyr" 的项目不再是错误。这是
  让 west 普遍适用于非 Zephyr 用例工作的一部分。
- 各种缺陷修复。

对 :ref:`west-apis` 的开发者可见更改是：

- west.build 和 west.cmake：已弃用；这是 Zephyr 特定功能，
  本不应属于 west。由于 Zephyr v1.14 LTS 依赖它，
  它将继续包含在发行版中，但当该版本 Zephyr 被淘汰时
  将被移除。
- west.commands：

  - WestCommand.requires_installation：已弃用；改用 requires_workspace
  - WestCommand.requires_workspace：新增
  - WestCommand.has_manifest：新增
  - WestCommand.manifest：现在可设置
- west.configuration：调用方现在可以在读取和写入配置文件时
  识别工作区目录
- west.log：

  - msg()：新增
- west.manifest：

  - 该模块现在使用标准 logging 模块而不是 west.log
  - QUAL_REFS_WEST：新增
  - SCHEMA_VERSION：新增
  - Defaults：移除
  - Manifest.as_dict()：新增
  - Manifest.as_frozen_yaml()：新增
  - Manifest.as_yaml()：新增
  - Manifest.from_file() 和 from_data()：这些工厂方法更
    灵活易用，更少依赖全局状态
  - Manifest.validate()：新增
  - ManifestImportFailed：新增
  - ManifestProject：半弃用，日后可能会被移除。
  - Project：构造函数现在接受 topdir 参数
  - Project.format() 及其调用方已移除。改用 f-string。
  - Project.name_and_path：新增
  - Project.remote_name：新增
  - Project.sha() 现在捕获 stderr
  - Remote：移除

West 现在要求 Python 3.6 或更高版本。此外，某些功能可能依赖
Python 字典按插入顺序排列；在 CPython 3.6 中这只是一个实现
细节，但从 Python 3.7 起它已成为语言规范的一部分。

v0.6.3
******

这个点版本修复了已弃用
``west.cmake`` 模块行为中的一个错误。

v0.6.2
******

这个点版本修复了 ``west
update --fetch=smart`` 行为中的一个错误，该错误引入于 v0.6.1。

所有 v0.6.1 用户必须升级。

v0.6.1
******

.. warning::

   不要使用这个点版本。请确保改用 v0.6.2。

这个点版本中的用户可见功能是：

- :ref:`west-update` 命令有一个新的 ``--fetch``
  命令行标志和 ``update.fetch`` :ref:`configuration option
  <west-config>`。默认值 "smart" 会跳过本地可用的 SHA 和
  标签的 fetch。
- ``west diff``、``west
  status``、``west forall`` 和 ``west update`` 命令中更好、更一致的错误处理。
  这些命令中的每一个都可以操作多个项目；如果与某个
  项目相关的子进程失败，这些命令现在会继续操作
  其余项目。如果这些子进程中有任何一个失败，它们现在也都
  会从 west 进程报告非零错误码（这一点之前对
  ``west forall`` 尤其不成立）。
- :ref:`west manifest <west-built-in-misc>` 命令的错误处理
  也得到了改善。
- :ref:`west list <west-built-in-misc>` 命令现在即使
  项目未被克隆也能工作，只要其格式字符串只要求
  可以从 manifest 文件读取的信息。如果
  格式字符串要求存储在项目仓库中的数据，例如包含
  ``{sha}`` 格式字符串键，它仍然会失败。
- 操作 git revision 的命令和选项现在接受缩写
  SHA。例如，``west init --mr SHA_PREFIX`` 现在可以工作。
  之前，``--mr`` 参数如果不是分支或标签，就必须是完整的 40 字符 SHA。

对 :ref:`west-apis` 的开发者可见更改是：

- west.log.banner()：新增
- west.log.small_banner()：新增
- west.manifest.Manifest.get_projects()：新增
- west.manifest.Project.is_cloned()：新增
- west.commands.WestCommand 实例现在可以在
  do_run() 调用期间通过新的 self.manifest 属性访问解析后的
  Manifest 对象。如果读取，它返回 Manifest 对象，
  如果无法解析则中止该命令。
- west.manifest.Project.git() 现在有一个 capture_stderr kwarg


v0.6.0
******

- 不再有单独的引导程序

  在 west v0.5.x 中，程序被拆分为两个组件：一个引导程序
  和一个按安装的克隆。更多细节参见 `v1.14 文档中的
  多仓库管理`_。

  这与 Google 的 Repo 工具的工作方式类似，
  使 west 最初能够快速迭代。然而它造成了困惑，而 west 现在已足够稳定，
  可以完全作为一个整体通过 PyPI 分发。

  从 v0.6.x 开始，所有核心 west 命令和辅助类
  都是通过 PyPI 分发的 west 包的一部分。这消除了
  复杂性，使得可以从系统任何地方导入 west 模块，
  而不仅仅是扩展命令。
- ``selfupdate`` 命令出于向后兼容性仍然存在，但
  现在只是打印错误消息后退出。
- Manifest 语法更改

  - west manifest 文件的 ``projects`` 元素现在可以直接指定
    其 fetch URL，如下所示：

    .. code-block:: yaml

       manifest:
         projects:
           - name: example-project-name
             url: https://github.com/example/example-project

    以这种方式设置了 ``url`` 属性的项目元素不得
    同时具有 ``remote`` 属性。
  - 项目名称必须唯一：此限制是支持未来
    工作所需的，但在 west v0.5.x 中不可能做到，因为不同的项目可能
    具有相同最终路径名组件的 URL，如下所示：

    .. code-block:: yaml

       manifest:
         remotes:
           - name: remote-1
             url-base: https://github.com/remote-1
           - name: remote-2
             url-base: https://github.com/remote-2
         projects:
           - name: project
             remote: remote-1
             path: remote-1-project
           - name: project
             remote: remote-2
             path: remote-2-project

    这些 manifest 现在可以写成项目使用 ``url``
    而不是 ``remote``，如下所示：

    .. code-block:: yaml

       manifest:
         projects:
           - name: remote-1-project
             url: https://github.com/remote-1/project
           - name: remote-2-project
             url: https://github.com/remote-2/project

- ``west list`` 命令现在支持 ``{sha}`` 格式字符串键

- ``west list`` 的默认格式字符串已更改为 ``"{name:12}
  {path:28} {revision:40} {url}"``。

- 命令 ``west manifest --validate`` 现在可以运行，
  用于加载并验证当前 manifest 文件，
  以及其他与 manifest 解析相关的错误处理修复。

- west 的 API 发生了不兼容的更改。
  在 west v1.0 宣布 API 稳定之前，
  预计还会有更多更改。

  - ``west.manifest.Project`` 构造函数的 ``remote`` 和 ``defaults``
    位置参数现在改为 kwargs。还添加了一个新的 ``url`` kwarg；
    如果给出，``Project`` 的 URL 被设置为该值，
    并且 ``remote`` kwarg 被忽略。

  - ``west.manifest.MANIFEST_SECTIONS`` 已移除。
    现在只有一个 section，即 ``manifest``。
    ``west.manifest.Manifest`` 工厂方法和构造函数中的 *sections* kwargs
    也已被移除。

  - ``west.manifest.SpecialProject`` 类已移除。
    改用 ``west.manifest.ManifestProject``。


v0.5.x
******

West v0.5.x 是 Zephyr 项目作为其 v1.14 长期支持（LTS）
版本的一部分广泛使用的第一个版本。`west v0.5.x 文档`_
可作为 Zephyr v1.14 文档的一部分获取。

West 在 v0.5.x 中的主要功能是：

- 使用 Git 仓库的多仓库管理，包括 west 本身的自更新
- 分层配置文件
- 扩展命令

v0.5.x 之前的版本
**********************

v0.5.x 之前 west 仓库中的标签是原型，
仅具有历史意义。

.. _v1.14 文档中的多仓库管理:
   https://docs.zephyrproject.org/1.14.0/guides/west/repo-tool.html

.. _west v0.5.x 文档:
   https://docs.zephyrproject.org/1.14.0/guides/west/index.html
