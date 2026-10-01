.. _west-troubleshooting:

West 故障排除
####################

本页介绍 west 的常见问题及其解决方法。

``west update`` 获取失败
*********************************

排查获取问题的一个好方法是使用详细模式运行 ``west update``，如下所示：

.. code-block:: shell

   west -v update

输出包括 west 运行的 Git 命令及其输出。寻找类似这样的内容：

.. code-block:: none

   === updating your_project (path/to/your/project):
   west.manifest: your_project: checking if cloned
   [...other west.manifest logs...]
   --- your_project: fetching, need revision SOME_SHA
   west.manifest: running 'git fetch ... https://github.com/your-username/your_project ...' in /some/directory

上面最后一行中的 ``git fetch`` 命令示例就是需要成功运行的命令。

一个策略是进入 ``/path/to/your/project``，复制/粘贴并运行完整的
``git fetch`` 命令，然后使用你的凭据存储辅助工具的文档从那里开始调试。

如果你在企业防火墙之后，可能存在代理或其他问题，
``curl -v FETCH_URL``（用于 HTTPS URL）或 ``ssh -v FETCH_URL``（用于 SSH URL）
可能会有所帮助。

如果你直接运行时能让 ``git fetch`` 命令成功运行且不再提示
输入密码，那么你在同一个 shell 中运行 ``west
update`` 时也将无需输入密码。

"'west' is not recognized as an internal or external command, operable program or batch file.'
**********************************************************************************************

在 Windows 上，这意味着要么 west 未安装，要么你的 :envvar:`PATH`
环境变量不包含 pip 安装 :file:`west.exe` 的目录。

首先，确保你已经安装了 west；参见 :ref:`west-install`。然后尝试
从新的 ``cmd.exe`` 窗口运行 ``west``。如果仍然不行，
继续阅读。

你需要找到包含 :file:`west.exe` 的目录，然后将其添加到你的
:envvar:`PATH`。（这个 :envvar:`PATH` 更改本应在你安装
Python 和 pip 时自动完成，所以通常你不需要执行以下步骤。）

在 ``cmd.exe`` 中运行这个命令::

  pip3 show west

然后：

#. 在输出中寻找一行，其内容类似 ``Location:
   C:\foo\python\python38\lib\site-packages``。确切位置
   在你的电脑上会不同。
#. 在 ``scripts`` 目录 ``C:\foo\python\python38\scripts`` 中
   寻找名为 ``west.exe`` 的文件。

   .. important::

      注意 ``pip3 show`` 输出中的 ``lib\site-packages``
      被替换成了 ``scripts``！
#. 如果你在 ``scripts`` 目录中看到了 ``west.exe``，
   使用如下命令将 ``scripts`` 的完整路径添加到你的 :envvar:`PATH`::

     setx PATH "%PATH%;C:\foo\python\python38\scripts"

   **不要直接复制/粘贴这条命令**。``scripts`` 目录的位置
   在你的系统上会不同。
#. 关闭你的 ``cmd.exe`` 窗口并打开一个新窗口。
   此时你应该能够运行 ``west``。

"invalid choice: 'build'"（或 'flash' 等）
********************************************

如果你在尝试运行 Zephyr 扩展
命令（如 :ref:`west flash <west-flashing>`、:ref:`west build
<west-building>` 等）时看到类似这样的意外错误：

.. code-block:: none

   $ west build [...]
   west: error: argument <command>: invalid choice: 'build' (choose from 'init', [...])

   $ west flash [...]
   west: error: argument <command>: invalid choice: 'flash' (choose from 'init', [...])

最可能的原因是你在 :ref:`west workspace <west-workspace>` 之外运行了
命令。West 需要知道你的工作区
在哪里才能找到 :ref:`west-extensions`。

要修复此问题，你有两个选择：

#. 从工作区内部运行命令（例如你 :ref:`入门 <getting_started>` 时创建的 :file:`zephyrproject`
   目录）。

   例如，在工作区内部创建你的构建目录，或从工作区内部运行 ``west
   flash --build-dir YOUR_BUILD_DIR``。

#. 设置 :envvar:`ZEPHYR_BASE` :ref:`环境变量 <env_vars>` 并重新
   运行 west 扩展命令。如果已设置，west 将使用 :envvar:`ZEPHYR_BASE`
   来找到你的工作区。

如果你不确定某个命令是内置命令还是扩展命令，
从你的工作区内部运行 ``west
help``。输出会单独打印扩展命令，
对于主线 Zephyr，其内容如下所示：

.. code-block:: none

   $ west help

   built-in commands for managing git repositories:
     init:                 create a west workspace
     [...]

   other built-in commands:
     help:                 get help for west or a command
     [...]

   extension commands from project manifest (path: zephyr):
     build:                compile a Zephyr application
     flash:                flash and run a binary on a board
     [...]

"invalid choice: 'post-init'"
*****************************

如果你在运行 ``west init`` 时看到这个错误：

.. code-block:: none

   west: error: argument <command>: invalid choice: 'post-init'
   (choose from 'init', 'update', 'list', 'manifest', 'diff',
   'status', 'forall', 'config', 'selfupdate', 'help')

那么说明你安装的是旧版本的 west，并试图在一个需要
更新版本的工作区中使用它。

解决此问题的最简单方法是升级 west 并按如下方式重试：

#. 按照 :ref:`west-install` 中所示，使用 ``pip3 install`` 的 ``-U`` 选项
   安装最新版本的 west。

#. 备份 :file:`zephyrproject/.west/config` 中你想
   保存的任何内容。（如果你没有设置任何配置选项，
   可以安全地跳过此步骤。）

#. 完全删除 :file:`zephyrproject/.west` 目录（如果不删除，
   你会得到下一个问题中讨论的 "already in a workspace" 错误消息）。

#. 再次运行 ``west init``。
