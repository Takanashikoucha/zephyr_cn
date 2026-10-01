:orphan:

.. _west-apis:
.. _west-apis-west:

West API
#########

本页记录 :ref:`west <west>` 提供的 Python API，
以及 zephyr 仓库中 :ref:`west 扩展 <west-extensions>` 使用的一些
附加 API。

**目录**：

.. contents::
   :local:

.. NOTE: 文档作者：

   1. 请保持这些条目按包/模块名排序。
   2. 如果你在这里添加一个 :ref: 目标，也请将其添加到 west-not-found.rst 中。

.. _west-apis-commands:

west.commands
*************

.. module:: west.commands

所有内置命令和扩展命令都实现为在此定义的
:py:class:`WestCommand` 类的子类。
这里还提供了一些异常类型。

WestCommand
===========

.. autoclass:: west.commands.WestCommand

   实例属性：

   .. py:attribute:: name

      与传递给构造函数的值相同。

   .. py:attribute:: help

      与传递给构造函数的值相同。内置命令必需，扩展忽略，
      参见 https://github.com/zephyrproject-rtos/west/issues/927

   .. py:attribute:: description

      与传递给构造函数的值相同。

   .. py:attribute:: accepts_unknown_args

      与传递给构造函数的值相同。

   .. py:attribute:: requires_workspace

      与传递给构造函数的值相同。

   .. versionadded:: 0.7.0

   .. py:attribute:: parser

      通过调用 ``WestCommand.add_parser()`` 创建的
      参数解析器。

   实例属性（property）：

   .. py:attribute:: manifest

      一个属性，返回当前 manifest 文件的
      :py:class:`west.manifest.Manifest`
      实例，如果未提供则中止程序。
      只有在 ``do_run()`` 方法中使用才是安全的。

   .. versionadded:: 0.6.1
   .. versionchanged:: 0.7.0
      现在可以设置。

   .. py:attribute:: has_manifest

      如果读取 manifest 属性会成功而不是
      出错，则为 True。

   .. py:attribute:: config

      一个可设置的属性，返回
      :py:class:`west.configuration.Configuration` 实例，
      如果未提供则中止程序。
      只有在 ``do_run()`` 方法中使用才是安全的。

   .. versionadded:: 0.13.0

   .. py:attribute:: has_config

      如果读取 config 属性会成功而不是
      出错，则为 True。

   .. versionadded:: 0.13.0

   .. py:attribute:: git_version_info

      一个 Git 版本信息的元组。

   .. versionadded:: 0.11.0

   .. py:attribute:: color_ui

      如果 west 配置允许彩色输出，
      则为 True，否则为 False。

   .. versionadded:: 1.0.0

   构造函数：

   .. automethod:: __init__

   .. versionadded:: 0.6.0
      *requires_installation* 参数（在 v0.13.0 中移除）。
   .. versionadded:: 0.7.0
      *requires_workspace* 参数。
   .. versionchanged:: 0.8.0
      *topdir* 参数现在可以是任何 ``os.PathLike``。
   .. versionchanged:: 0.13.0
      已弃用的 *requires_installation* 参数被移除。
   .. versionadded:: 1.0.0
      *verbosity* 参数。

   方法：

   .. automethod:: run

   .. versionchanged:: 0.6.0
      添加了 *topdir* 参数。

   .. automethod:: add_parser

   .. automethod:: add_pre_run_hook
   .. versionadded:: 1.0.0

   .. NOTE: 以下 'method'（而非 'automethod'）指令是在
      west v1.2 发布期间为了便利而添加的，用于规避本 Zephyr 文档中
      一个无法在不发布 west 点版本的情况下修复的构建
      失败问题。（west 中的 docstring 存在一些 RST 语法
      错误）。

      应在下次发布时改回 automethod 调用。

   .. method:: check_call(args, **kwargs)

      在 ``Verbosity.DBG_MORE`` 级别记录该调用后，
      运行 ``subprocess.check_call(args, **kwargs)``。

   .. versionchanged:: 1.2.0
      *cwd* 关键字参数被替换为兜底的 ``**kwargs``。
   .. versionchanged:: 0.11.0

   .. method:: check_output(args, **kwargs)

      在 Verbosity.DBG_MORE 级别记录该调用后，
      运行 ``subprocess.check_output(args, **kwargs)``。

   .. versionchanged:: 1.2.0
      *cwd* 关键字参数被替换为兜底的 ``**kwargs``。
   .. versionchanged:: 0.11.0

   .. method:: run_subprocess(args, **kwargs)

      在 Verbosity.DBG_MORE 级别记录该调用后，
      运行 ``subprocess.run(args, **kwargs)``。

   .. versionadded:: 1.2.0

    所有子类都必须提供以下抽象方法，
    它们用于实现上述方法：

   .. automethod:: do_add_parser

   .. automethod:: do_run

   当命令需要打印输出时，应使用以下方法。
   引入这些方法是为了实现从已弃用的
   ``west.log`` 模块到按命令接口的过渡，
   该接口将在未来版本中允许为 west 命令
   提供全局"安静"模式：

   .. automethod:: dbg
   .. versionchanged:: 1.2.0
      *end* 参数。
   .. versionadded:: 1.0.0

   .. automethod:: inf
   .. versionchanged:: 1.2.0
      *end* 参数。
   .. versionadded:: 1.0.0

   .. automethod:: wrn
   .. versionchanged:: 1.2.0
      *end* 参数。
   .. versionadded:: 1.0.0

   .. automethod:: err
   .. versionchanged:: 1.2.0
      *end* 参数。
   .. versionadded:: 1.0.0

   .. automethod:: die
   .. versionadded:: 1.0.0

   .. automethod:: banner
   .. versionadded:: 1.0.0

   .. automethod:: small_banner
   .. versionadded:: 1.0.0

.. _west-apis-commands-output:

Verbosity（冗长度）
========

从 west v1.0 开始，west 命令应使用
west.commands.WestCommand.dbg()、west.commands.WestCommand.inf() 等
方法打印输出（见上文）。本节记录一个相关的枚举，
用于声明冗长度级别。

.. autoclass:: west.commands.Verbosity

   .. autoattribute:: QUIET
   .. autoattribute:: ERR
   .. autoattribute:: WRN
   .. autoattribute:: INF
   .. autoattribute:: DBG
   .. autoattribute:: DBG_MORE
   .. autoattribute:: DBG_EXTREME

.. versionadded:: 1.0.0

异常
==========

.. autoclass:: west.commands.CommandError
   :show-inheritance:

   .. py:attribute:: returncode

      此错误的推荐程序退出码。

.. autoclass:: west.commands.CommandContextError
   :show-inheritance:

.. _west-apis-configuration:

west.configuration
******************

.. automodule:: west.configuration

从 west v0.13 开始，推荐的读取类是
:py:class:`west.configuration.Configuration`。

注意，如果你在编写 :ref:`west 扩展 <west-extensions>`，
可以将当前的 ``Configuration`` 对象作为 ``self.config`` 访问。
参见 :py:class:`west.commands.WestCommand`。

Configuration API
=================

这是从 west v0.13 开始推荐的 API。

.. autoclass:: west.configuration.ConfigFile

.. autoclass:: west.configuration.Configuration
   :members:

   .. versionadded:: 0.13.0

已弃用的 API
==============

以下 API 也使用 :py:class:`west.configuration.ConfigFile`，
但它们默认操作一个存储当前工作区
配置的全局对象。事实证明这是一个糟糕的设计决定，
因为 west 的 API 可以从多个工作区使用。
它们在 west v0.13.0 中被弃用。

这些 API 为与旧扩展的兼容性而保留。
当可以假定 west v0.13.0 或更高版本时，
不应在新代码中使用它们。

.. autofunction:: west.configuration.read_config

.. versionchanged:: 0.8.0
   已弃用的 *read_config* 参数被移除。

.. versionchanged:: 0.6.0
   由于找不到本地配置文件而产生的错误被忽略。

.. autofunction:: west.configuration.update_config

.. py:data:: west.configuration.config

   当前配置的模块级全局 ConfigParser 实例。
   读取之前应使用 :py:func:`west.configuration.read_config` 初始化。

.. _west-apis-log:

west.log（已弃用）
*********************

.. automodule:: west.log

冗长度控制
=================

要设置全局冗长度级别，请使用 ``set_verbosity()``。

.. autofunction:: set_verbosity

定义了以下冗长度级别。

.. autodata:: VERBOSE_NONE
.. autodata:: VERBOSE_NORMAL
.. autodata:: VERBOSE_VERY
.. autodata:: VERBOSE_EXTREME

输出函数
================

主要函数是 ``dbg()``、``inf()``、``wrn()``、``err()`` 和
``die()``。``inf()`` 的两个特殊情况 ``banner()`` 和 ``small_banner()``
也可用，用于将输出分组为"章节"。

.. autofunction:: dbg
.. autofunction:: inf
.. autofunction:: wrn
.. autofunction:: err
.. autofunction:: die

.. autofunction:: banner
.. autofunction:: small_banner

.. _west-apis-manifest:

west.manifest
*************

.. automodule:: west.manifest

主要类是 :py:class:`Manifest` 和 :py:class:`Project`。
它们表示 :ref:`manifest 文件 <west-manifests>` 的内容。
解析 west manifest 的推荐方法是
:py:meth:`Manifest.from_topdir`。

常量和函数
=======================

.. autodata:: MANIFEST_PROJECT_INDEX
.. autodata:: MANIFEST_REV_BRANCH
.. autodata:: QUAL_MANIFEST_REV_BRANCH
.. autodata:: QUAL_REFS_WEST
.. autodata:: SCHEMA_VERSION

.. autofunction:: west.manifest.manifest_path

.. autofunction:: west.manifest.validate

.. versionchanged:: 0.13.0
   现在返回包含解析后的 YAML 数据的验证 dict。

Manifest 及子对象
========================

.. autoclass:: west.manifest.Manifest

   .. automethod:: __init__
   .. versionchanged:: 0.7.0
      *importer* 和 *import_flags* 关键字参数。
   .. versionchanged:: 0.13.0
      所有参数都改为仅关键字。*source_file* 参数被
      移除（改用 *topdir*）。该函数不再抛出
      ``WestNotFound``。
   .. versionadded:: 0.13.0
      *config* 参数。
   .. versionadded:: 0.13.0
      *abspath*、*posixpath*、*relative_path*、*yaml_path*、*repo_path*、
      *repo_posixpath* 和 *userdata* 属性。

   .. automethod:: from_topdir
   .. versionadded:: 0.13.0

   .. automethod:: from_file
   .. versionchanged:: 0.7.0
      添加了 ``**kwargs``。
   .. versionchanged:: 0.8.0
      *source_file*、*manifest_path* 和 *topdir* 参数
      现在可以是任何 ``os.PathLike``。
   .. versionchanged:: 0.13.0
      *manifest_path* 和 *topdir* 参数被移除。

   .. automethod:: from_data
   .. versionchanged:: 0.7.0
      添加了 ``**kwargs``，且 *source_data* 可以是 ``str``。
   .. versionchanged:: 0.13.0
      *manifest_path* 和 *topdir* 参数被移除。

   按名称或其他标识符访问子对象的便捷方法：

   .. automethod:: get_projects
   .. versionchanged:: 0.8.0
      *project_ids* 序列现在可以包含任何 ``os.PathLike``。
   .. versionadded:: 0.6.1

   附加方法：

   .. automethod:: as_dict
   .. versionadded:: 1.4.0
      *active_only* 参数。
   .. versionadded:: 0.7.0
   .. automethod:: as_frozen_dict
   .. versionadded:: 1.4.0
      *active_only* 参数。
   .. automethod:: as_yaml
   .. versionadded:: 1.4.0
      *active_only* 参数。
   .. versionadded:: 0.7.0
   .. automethod:: as_frozen_yaml
   .. versionadded:: 1.4.0
      *active_only* 参数。
   .. versionadded:: 0.7.0
   .. automethod:: is_active
   .. versionadded:: 0.9.0
   .. versionchanged:: 1.1.0
      现在遵循 ``manifest.project-filter`` 配置
      选项。参见 :ref:`west-config-index`。

.. autoclass:: west.manifest.ImportFlag
   :members:
   :member-order: bysource

.. autoclass:: west.manifest.Project

   .. (注意：属性是类 docstring 的一部分)

   .. versionchanged:: 0.7.0
      *remote* 属性被移除。当添加对 manifest ``import``
      键的支持后，其语义已无法保留。

   .. versionadded:: 0.7.0
      *remote_name* 和 *name_and_path* 属性。

   .. versionchanged:: 0.8.0
      *west_commands* 属性现在总是一个列表。在之前的
      版本中，它可能是字符串或 ``None``。

   .. versionadded:: 0.9.0
      *group_filter* 和 *submodules* 属性。

   .. versionadded:: 0.12.0
      *userdata* 属性。

   .. versionadded:: 1.2.0
      *description* 属性。

   构造函数：

   .. automethod:: __init__

   .. versionchanged:: 0.8.0
      *path* 和 *topdir* 参数现在可以是任何 ``os.PathLike``。

   .. versionchanged:: 0.7.0
      参数与之前版本不兼容地发生了变化。

   方法：

   .. automethod:: as_dict
   .. versionadded:: 0.7.0

   .. automethod:: git
   .. versionchanged:: 0.6.1
      *capture_stderr* kwarg。
   .. versionchanged:: 0.7.0
      （现已移除的）``Project.format`` 方法不再被
      应用于参数。

   .. automethod:: sha
   .. versionchanged:: 0.7.0
      现在捕获标准错误。

   .. automethod:: is_ancestor_of
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。

   .. automethod:: is_cloned
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。
   .. versionadded:: 0.6.1

   .. automethod:: is_up_to_date_with
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。

   .. automethod:: is_up_to_date
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。

   .. automethod:: read_at
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。
   .. versionadded:: 0.7.0

   .. automethod:: listdir_at
   .. versionchanged:: 0.8.0
      *cwd* 参数现在可以是任何 ``os.PathLike``。
   .. versionadded:: 0.7.0

.. autoclass:: west.manifest.ManifestProject

   支持 Project 方法的一个有限子集。
   调用其他方法的结果未作规定。

   .. versionchanged:: 0.8.0
      *url* 属性现在是空字符串而不是 ``None``。
      *abspath* 属性现在使用 ``os.path.abspath()``
      而不是 ``os.path.realpath()`` 创建，
      改进了对符号链接的支持。

   .. automethod:: as_dict

.. versionadded:: 0.6.0

.. autoclass:: west.manifest.Submodule

.. versionadded:: 0.9.0

异常
==========

.. autoclass:: west.configuration.MalformedConfig
   :show-inheritance:

.. autoclass:: west.manifest.MalformedManifest
   :show-inheritance:

.. autoclass:: west.manifest.ManifestVersionError
   :show-inheritance:

   .. versionchanged:: 0.8.0
      *file* 参数现在可以是任何 ``os.PathLike``。

.. autoclass:: west.manifest.ManifestImportFailed
   :show-inheritance:

   .. versionchanged:: 0.8.0
      *filename* 参数现在可以是任何 ``os.PathLike``。

   .. versionchanged:: 0.13.0
      *filename* 参数被重命名为 *imp*，现在可以接受任何值。

.. _west-apis-util:

west.util
*********

.. canon_path()、escapes_directory() 等有意未在此处记录。

.. automodule:: west.util

函数
=========

.. autofunction:: west.util.west_dir

   .. versionchanged:: 0.8.0
      *start* 参数可以是任何 ``os.PathLike``。

.. autofunction:: west.util.west_topdir

   .. versionchanged:: 0.8.0
      *start* 参数可以是任何 ``os.PathLike``。

异常
==========

.. autoclass:: west.util.WestNotFound
   :show-inheritance:
