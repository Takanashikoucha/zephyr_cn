.. _west-extensions:

扩展
##########

West 是"可插拔的"：你可以在不修改其源代码的情况下
向 west 添加自己的命令。这些命令称为 **west 扩展命令**，
简称"扩展"。扩展命令会出现在 ``west --help`` 输出的
一个专门章节中，该章节按定义它们的工程来组织。
本页提供 west 扩展命令的通用信息，并附有编写自己的扩展命令的教程。

使用 west 配合 Zephyr 时可以运行的一些命令，比如用于
:ref:`构建、烧录和调试 <west-build-flash-debug>` 的命令以及
:ref:`本文描述的这些命令 <west-zephyr-ext-cmds>`，都是扩展。
因此它们在 ``west --help`` 中的帮助信息显示如下：

.. code-block:: none

   extension commands from project manifest (path: zephyr):
     completion:           display shell completion scripts
     boards:               display information about supported boards
     shields:              display list of supported shields
     build:                compile a Zephyr application
     twister:              west twister wrapper
     sign:                 sign a Zephyr binary for bootloader chain-loading
     flash:                flash and run a binary on a board
     debug:                flash and interactively debug a Zephyr application
     debugserver:          connect to board and launch a debug server
     attach:               interactively debug a board
     ...

实现细节请参见 :file:`zephyr/scripts/west-commands.yml` 和
:file:`zephyr/scripts/west_commands` 目录。

禁用扩展命令
****************************

要禁用对扩展命令的支持，将 :ref:`配置 <west-config>` 选项
``commands.allow_extensions`` 设置为 ``false``。
要在每次运行 west 时全局设置，使用：

.. code-block:: console

   west config --global commands.allow_extensions false

如果需要，之后可以在某个特定的 :term:`west workspace` 中重新启用它们：

.. code-block:: console

   west config --local commands.allow_extensions true

请注意，包含扩展命令的文件只有在命令被显式运行时
才会被 west 导入。详情见下文。

添加 West 扩展
***********************

添加自己的扩展分三步：

#. 编写实现该命令的代码。
#. 在 :file:`west-commands.yml` 文件中添加关于它的信息。
#. 确保 :file:`west-commands.yml` 文件在 :term:`west manifest` 中被引用。

请注意，west 会忽略与内置命令同名的扩展命令。

步骤 1：实现你的命令
================================

创建一个 Python 文件来包含你的命令实现（关于当前支持的
Python 版本，请参见 `west PyPI 页面`_ 上 west 项目的元数据）。
你可以把它放在 :term:`west manifest` 跟踪的任何工程的任何位置，
或者放在 manifest 仓库本身中。
该文件必须包含 ``west.commands.WestCommand`` 类的一个子类。
当你的扩展被运行时，该类会被实例化并使用。

下面是一个可供起步的基本骨架。它包含一个 ``WestCommand`` 子类，
并实现了所有抽象方法。关于你可用的 west API 的更多细节，
参见 :ref:`west-apis`。

.. code-block:: py

   '''my_west_extension.py

   Basic example of a west extension.'''

   from textwrap import dedent            # just for nicer code indentation

   from west.commands import WestCommand  # your extension must subclass this

   class MyCommand(WestCommand):

       def __init__(self):
           super().__init__(
               'my-command-name',  # gets stored as self.name
               '', # ignored self.help, will not be required by future west versions
               # self.description:
               description=dedent('''
               A multi-line description of my-command.

               You can split this up into multiple paragraphs and they'll get
               reflowed for you. You can also pass
               formatter_class=argparse.RawDescriptionHelpFormatter when calling
               parser_adder.add_parser() below if you want to keep your line
               endings.'''))

       def do_add_parser(self, parser_adder):
           # This is a bit of boilerplate, which allows you full control over the
           # type of argparse handling you want. The "parser_adder" argument is
           # the return value of an argparse.ArgumentParser.add_subparsers() call.
           parser = parser_adder.add_parser(self.name,
                                            description=self.description)

           # Add some example options using the standard argparse module API.
           parser.add_argument('-o', '--optional', help='an optional argument')
           parser.add_argument('required', help='a required argument')

           return parser           # gets stored as self.parser

       def do_run(self, args, unknown):
           # This gets called when the user runs the command, e.g.:
           #
           #   $ west my-command-name -o FOO BAR
           #   --optional is FOO
           #   required is BAR
           self.inf('--optional is', args.optional)
           self.inf('required is', args.required)

你可以忽略 ``do_run()`` 的第二个参数（即上面的 ``unknown``），
因为 ``WestCommand`` 默认会拒绝未知参数。
如果你想改为接收一个未知参数列表，请在 ``super().__init__()``
的参数中添加 ``accepts_unknown_args=True``。

步骤 2：添加或更新你的 :file:`west-commands.yml`
==================================================

现在你需要向你的工程添加一个 :file:`west-commands.yml` 文件，
向 west 描述你的扩展。

以下是上面类定义的示例，假设它位于工程根目录的
:file:`my_west_extension.py` 中：

.. code-block:: yaml

   west-commands:
     - file: my_west_extension.py
       commands:
         - name: my-command-name
           class: MyCommand
           help: one-line help for what my-command-name does

这个 YAML 文件的顶层是一个带有 ``west-commands`` 键的映射。
该键的值是一个"命令描述符"序列。每个命令描述符
给出实现 west 扩展的某个文件的位置，以及这些扩展的名称，
还可以是定义它们的类的名称（如果未给出，
``class`` 值默认与 ``name`` 相同）。

该文件中的某些信息与 Python 代码中的定义重复。
这是因为 west 不会在用户运行 ``west my-command-name`` 之前
导入 :file:`my_west_extension.py`，原因如下：

- 它允许用户使用来自不受信任来源的 manifest 运行 ``west update``，
  然后使用其他 west 命令，而你的代码不会顺带被导入。
  由于导入 Python 模块在效果上等同于执行 shell 命令，
  这能在一定程度上让人放心。

- 这是一个小小的优化，因为你的代码只会在需要时才被导入。

因此，除非你的命令被显式运行，west 只是加载 :file:`west-commands.yml`
文件来获取它显示 ``west --help`` 输出中关于你的扩展的信息等基本所需的信息。

如果你有多个扩展，或者想把扩展拆分到多个文件中，
你的 :file:`west-commands.yml` 会像这样：

.. code-block:: yaml

   west-commands:
     - file: my_west_extension.py
       commands:
         - name: my-command-name
           class: MyCommand
           help: one-line help for what my-command-name does
     - file: another_file.py
       commands:
         - name: command2
           help: another cool west extension
         - name: a-third-command
           class: ThirdCommand
           help: a third command in the same file as command2

上面：

- :file:`my_west_extension.py` 用类 ``MyCommand`` 定义扩展 ``my-command-name``
- :file:`another_file.py` 定义两个扩展：

  #. 类为 ``command2`` 的 ``command2``
  #. 类为 ``ThirdCommand`` 的 ``a-third-command``

关于 :file:`west-commands.yml` 内容的架构描述，
参见 `west 仓库`_ 中的 :file:`west-commands-schema.yml` 文件。

步骤 3：更新你的 manifest
===========================

最后，你需要在 west manifest 中指定刚才编辑的
:file:`west-commands.yml` 的位置。如果扩展在某个工程中，
像这样添加它：

.. code-block:: yaml

   manifest:
      # [... other contents ...]

      projects:
        - name: your-project
          west-commands: path/to/west-commands.yml
        # [... other projects ...]

其中 :file:`path/to/west-commands.yml` 相对于工程根目录。
请注意，:file:`west-commands.yml` 这个名称虽然被鼓励使用，
但只是一种约定；如有需要，你可以把文件命名为其他名字。

或者，如果扩展在 manifest 仓库中，只需在 manifest 的 ``self`` 节中
做同样的事，像这样：

.. code-block:: yaml

   manifest:
     # [... other contents ...]

     self:
       west-commands: path/to/west-commands.yml

就这样；现在你可以运行 ``west my-command-name`` 了。
你的命令的名称、帮助信息以及包含其代码的工程
也会出现在 ``west --help`` 输出中。
如果你把更新后的仓库分享给其他人，他们也能使用它。

.. _west PyPI 页面:
   https://pypi.org/project/west/

.. _west 仓库:
   https://github.com/zephyrproject-rtos/west/
