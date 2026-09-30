.. _west-config:

配置
#############

本
页
记录
west
的
配置
文件
系统、
``west
config``
命令
和
内置
命令
使用
的
配置
选项。
对
``west.configuration``
模块
的
API
文档，
参考
:ref:`west-apis-configuration`。

West
配置
文件
------------------------

West
的
配置
文件
语法
是
INI-like；
这里
是
一
个
示例
文件：

.. code-block:: ini

   [manifest]
   path
   =
   zephyr

   [zephyr]
   base
   =
   zephyr

上面，
``manifest``
section
有
选项
``path``
设置
为
``zephyr``。
说
同一
件事
的
另一
种
方式
是
在这
个
文件
中
``manifest.path``
是
``zephyr``。

有
三
种
类型
的
配置
文件：

1. **System**：
   这
   个
   文件
   中
   的
   设置
   影响
   west
   的
   行为
   对
   登录
   到
   电脑
   的
   每个
   用户。
   其
   位置
   取决于
   平台：

   - Linux:
     :file:`/etc/westconfig`
   - macOS:
     :file:`/usr/local/etc/westconfig`
   - Windows:
     :file:`%PROGRAMDATA%\\west\\config`

2. **Global**
   （per
   user）：
   这
   个
   文件
   中
   的
   设置
   影响
   west
   在
   电脑
   上
   被
   特定
   用户
   运行
   时
   如何
   行为。

   - All
     platforms:
     默认
     是
     用户
     home
     目录
     中
     的
     :file:`.westconfig`。


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
   * - ``manifest.file``
     - String, default ``west.yml``. Relative path from the manifest repository
       root directory to the manifest file used by ``west init`` and other
       commands which parse the manifest.
   * - ``manifest.group-filter``
     - String, default empty. A comma-separated list of project groups to
       enable and disable within the workspace. Prefix enabled groups with
       ``+`` and disabled groups with ``-``. For example, the value
       ``"+foo,-bar"`` enables group ``foo`` and disables ``bar``. See
       :ref:`west-manifest-groups`.
   * - ``manifest.path``
     - String, relative path from the :term:`west workspace` root directory
       to the manifest repository used by ``west update`` and other commands
       which parse the manifest. Set locally by ``west init``.
   * - ``manifest.project-filter``
     - Comma-separated list of strings.

       The option's value is a comma-separated list of regular expressions,
       each prefixed with ``+`` or ``-``, like this:

       .. code-block:: none

          +re1,-re2,-re3

       Project names are matched against each regular expression (``re1``,
       ``re2``, ``re3``, ...) in the list, in order. If the entire project name
       matches the regular expression, that element of the list either
       deactivates or activates the project. The project is deactivated if the
       element begins with ``-``. The project is activated if the element
       begins with ``+``. (Project names cannot contain ``,`` if this option is
       used, so the regular expressions do not need to contain a literal ``,``
       character.)

       If a project's name matches multiple regular expressions in the list,
       the result from the last regular expression is used. For example,
       if ``manifest.project-filter`` is:

       .. code-block:: none

          -hal_.*,+hal_foo

       Then a project named ``hal_bar`` is inactive, but a project named
       ``hal_foo`` is active.

       If a project is made inactive or active by a list element, the project
       is active or not regardless of whether any or all of its groups are
       disabled. (This is currently the only way to make a project that has no
       groups inactive.)

       Otherwise, i.e. if a project does not match any regular expressions in
       the list, it is active or inactive according to the usual rules related
       to its groups (see :ref:`west-project-group-examples` for examples in
       that case).

       Within an element of a ``manifest.project-filter`` list, leading and
       trailing whitespace are ignored. That means these example values
       are equivalent:

       .. code-block:: none

          +foo,-bar
          +foo , -bar

       Any empty elements are ignored. That means these example values are
       equivalent:

       .. code-block:: none

           +foo,,-bar
           +foo,-bar

   * - ``update.auto-cache``
     - String. If non-empty, ``west update`` will use its value as the
       ``--auto-cache`` option's value if not given on the command line.
   * - ``update.fetch``
     - String, one of ``"smart"`` (the default behavior starting in v0.6.1) or
       ``"always"`` (the previous behavior). If set to ``"smart"``, the
       :ref:`west-update` command will skip fetching
       from project remotes when those projects' revisions in the manifest file
       are SHAs or tags which are already available locally. The ``"always"``
       behavior is to unconditionally fetch from the remote.
   * - ``update.name-cache``
     - String. If non-empty, ``west update`` will use its value as the
       ``--name-cache`` option's value if not given on the command line.
   * - ``update.narrow``
     - Boolean. If ``true``, ``west update`` behaves as if ``--narrow`` was
       given on the command line. The default is ``false``.
   * - ``update.path-cache``
     - String. If non-empty, ``west update`` will use its value as the
       ``--path-cache`` option's value if not given on the command line.
   * - ``update.sync-submodules``
     - Boolean. If ``true`` (the default), :ref:`west-update` will synchronize
       Git submodules before updating them.
   * - ``zephyr.base``
     - String, default value to set for the :envvar:`ZEPHYR_BASE` environment
       variable while the west command is running. By default, this is set to
       the path to the manifest project with path :file:`zephyr` (if there is
       one) during ``west init``. If the variable is already set, then this
       setting is ignored unless ``zephyr.base-prefer`` is ``"configfile"``.
   * - ``zephyr.base-prefer``
     - String, one the values ``"env"`` and ``"configfile"``. If set to
       ``"env"`` (the default), setting :envvar:`ZEPHYR_BASE` in the calling
       environment overrides the value of the ``zephyr.base`` configuration
       option. If set to ``"configfile"``, the configuration option wins
       instead.