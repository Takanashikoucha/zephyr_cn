:orphan:

.. _west_projects_index:

West 项目索引
#############

本页作为与 :ref:`West <west>` 元工具兼容的项目（模块）的索引。

它主要列出 Zephyr 默认 :zephyr_file:`清单文件 <west.yml>` 中声明的组件。参见 :ref:`external-contributions` 获取关于这些导入组件的贡献和审查流程的更多信息。

它还维护一个 :ref:`外部项目 <west_external_projects>` 的注册表，这些项目在 Zephyr 项目外部维护，可以轻松集成到 Zephyr 工作区中。

活跃项目/模块
+++++++++++++++

下面的项目默认启用，当你调用 :command:`west update` 时将被下载。下面列出的许多项目或模块是构建通用 Zephyr 应用所必需的，其中包括 Zephyr 中许多可用平台的硬件支持。

要禁用任何活跃模块，例如特定的 HAL，使用以下命令::

        west config manifest.project-filter -- -hal_FOO
        west update

.. manifest-projects-table::
   :filter: active

非活跃和可选项目/模块
++++++++++++++++++++++++++++++++++++++

下面的项目是可选的，当你调用 :command:`west update` 时不会被下载。你可以添加下面列出的任何项目或模块，并使用它们编写应用代码，用添加的功能扩展你的工作区。

要启用下面的任何模块，使用以下命令::

        west config manifest.project-filter -- +nanopb
        west update

.. manifest-projects-table::
   :filter: inactive

.. _west_external_projects:

外部项目/模块
++++++++++++++++++++++++

下面列出的项目是外部项目，不直接导入到默认清单中。要使用下面的任何项目，你需要定义一个包含它们的自己的清单文件。参见 :ref:`west-manifest-import` 获取关于推荐方式的更多信息，同时仍从 Zephyr 的 :file:`west.yml` 继承必需的模块。

使用 :zephyr_file:`专用模板文件 <doc/develop/manifest/external/external.rst.tmpl>` 为下面的列表贡献新的外部模块：

.. toctree::
   :titlesonly:
   :maxdepth: 1
   :glob:

   external/*
