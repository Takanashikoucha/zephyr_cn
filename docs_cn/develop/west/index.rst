.. _west:

West（Zephyr 的元工具）
#########################

Zephyr 项目包含一个名为 ``west`` 的"瑞士军刀"式命令行工具 [#west-name]_。West 在其自己的 `repository`_ 中开发。

West 的内置命令提供了一个多仓库管理系统，其功能灵感来自 Google 的 Repo 工具和 Git 子模块。West 也是"可插拔的"：你可以编写自己的 west 扩展命令，为 west 增加额外的功能。Zephyr 利用这一点来提供构建应用、烧录和调试应用等便利，以及更多功能。

与 ``git`` 和 ``docker`` 类似，顶层的 ``west`` 命令接受一些通用选项、一个要运行的子命令，以及该子命令的选项和参数::

  west [common-opts] <command> [opts] <args>

从 west v0.8 开始，你还可以像这样运行 west::

  python3 -m west [common-opts] <command> [opts] <args>

你可以运行 ``west --help``（或简写为 ``west -h``）获取可用 west 命令的顶层帮助，运行 ``west <command> -h`` 获取每个命令的详细帮助。

.. toctree::
   :maxdepth: 1

   install.rst
   release-notes.rst
   troubleshooting.rst
   basics.rst
   built-in.rst
   workspaces.rst
   manifest.rst
   config.rst
   alias.rst
   extensions.rst
   build-flash-debug.rst
   sign.rst
   zephyr-cmds.rst
   why.rst
   without-west.rst

关于 west 的 Python API 详情，参见 :ref:`west-apis`。

.. rubric:: 脚注

.. [#west-name]

   Zephyr 是拉丁语 `Zephyrus <https://en.wiktionary.org/wiki/Zephyrus>`_ 的英语名称，即古希腊的西风之神。

.. _repository:
   https://github.com/zephyrproject-rtos/west
