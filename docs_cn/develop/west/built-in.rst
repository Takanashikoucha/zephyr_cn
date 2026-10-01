.. _west-built-in-cmds:

内置命令
#################

本页更详细地描述 West 的内置命令，
其中一些在 :ref:`west-basics` 中已介绍。

一些命令与同名的 Git 命令相关，
但操作的是整个工作区。
例如，``west diff`` 显示工作区中多个 Git 仓库的本地更改。

一些命令接受项目作为参数。
这些参数可以是清单文件中指定的项目名称，
或（作为回退）本地文件系统中的路径。
对于接受项目参数的命令（如 ``west list``、``west forall`` 等），
省略项目参数通常默认为使用清单文件中的所有项目加上清单仓库本身。

获取额外帮助，请运行 ``west <command> -h``（例如 ``west init -h``）。

.. _west-init:

west init
*********

该命令用于创建 West 工作区。
它有两种用法：

1. 从远程 URL 克隆新的清单仓库
2. 围绕一个已存在的本地清单仓库创建工作区

**方式 1**：要从远程 URL 克隆新的清单仓库，使用：

.. code-block:: none

   west init [-m URL] [--mr REVISION] [--mf FILE] [directory]

新的工作区会在给定的 :file:`directory` 中创建，
并在该目录内部创建 :file:`.west`。
你可以用 ``-m`` 开关给出清单 URL，
用 ``--mr`` 给出要检出的初始版本（revision），
用 ``--mf`` 给出清单文件在仓库中的位置。

例如，运行：

.. code-block:: shell

   west init -m https://github.com/zephyrproject-rtos/zephyr --mr v1.14.0 zp

会将上游官方 zephyr 仓库克隆到 :file:`zp/zephyr`，
并检出 ``v1.14.0`` 版本。
该命令会创建 :file:`zp/.west`，
并将 :ref:`配置选项 <west-config>` ``manifest.path`` 设为 ``zephyr``，
以记录清单仓库在工作区中的位置。
清单文件位置使用默认值。

``-m`` 选项默认为 ``https://github.com/zephyrproject-rtos/zephyr``。
``--mf`` 选项默认为 ``west.yml``。
从 west v0.10.1 开始，
除非使用 ``--mr`` 选项覆盖，
West 将使用清单仓库中的默认分支。
（在先前版本中，``--mr`` 默认为 ``master``。）

如果未给出 ``directory``，则使用当前工作目录。

**方式 2**：要围绕一个已存在的本地清单仓库创建工作区，使用：

.. code-block:: none

   west init -l [--mf FILE] directory

这会在文件系统中 :file:`directory` **旁边**创建 :file:`.west`，
并将 ``manifest.path`` 设为 ``directory``。

如上所述，``--mf`` 默认为 ``west.yml``。

**重新配置工作区**：

如果你之后改变主意，
可以在运行 ``west init`` 之后，
自由使用 :ref:`west-config-cmd` 修改 ``manifest.path`` 和 ``manifest.file``。
只需确保之后运行 ``west update``，
将工作区更新为与新清单文件相匹配。

.. _west-update:

west update
***********

.. code-block:: none

   west update [-f {always,smart}] [-k] [-r]
              [--group-filter FILTER] [--stats] [PROJECT ...]

**哪些项目会被更新：**

默认情况下，该命令解析清单文件（通常是 :file:`west.yml`），
并更新其中指定的每个项目。
如果你的清单使用了 :ref:`项目分组 <west-manifest-groups>`，
则只有处于激活状态的项目会被更新。

要只操作项目的子集，请给出 ``PROJECT`` 参数。
每个 ``PROJECT`` 要么是清单文件中给出的项目名称，
要么是指向工作区内该项目的路径。
如果你显式指定了项目，无论其是否处于激活状态，都会被更新。

.. _west-update-procedure:

**项目更新流程：**

对于每个被更新的项目，该命令会：

#. 如果项目中尚不存在本地 Git 仓库，
   则在工作区中为其初始化一个
#. 检查项目在清单中的 ``revision`` 字段，
   如果该版本尚未在本地可用，则从远程获取（fetch）
#. 将项目的 :ref:`manifest-rev <west-manifest-rev>` 分支
   设置为上一步中版本所指定的提交（commit）
#. 在本地工作副本中检出 ``manifest-rev``，
   处于 `detached HEAD（分离头指针） <https://git-scm.com/docs/git-checkout#_detached_head>`_ 状态
   （关于这一选择的细节，见 :ref:`west-update-detached-heads`）
#. 如果清单文件为该项目指定了 :ref:`submodules <west-manifest-submodules>`（子模块）键，
   则按如下描述递归更新项目的子模块。

为避免不必要的获取，
``west update`` 不会获取那些本地已有的
Git SHA 或标签（tag）形式的 ``revision`` 值。
这是 ``-f``（``--fetch``）选项取默认值 ``smart`` 时的行为。
要强制该命令即使版本似乎在本地可用
也从项目远程获取，
可以使用 ``-f always``，
或将 :ref:`配置选项 <west-config>` ``update.fetch`` 设为 ``always``。
只要 Git 可接受，SHA 可以以唯一前缀的形式给出 [#fetchall]_。

如果项目的 ``revision`` 是既不是标签也不是 SHA 的 Git 引用
（即项目正在跟踪某个分支），
``west update`` 总是执行获取，
无论 ``-f`` 和 ``update.fetch`` 如何设置。

某些分支名称看起来可能像短 SHA，如 ``deadbeef``。
West 将其视为 SHA。
你可以在 ``revision`` 值前加 ``refs/heads/`` 前缀来消除歧义，
例如 ``revision: refs/heads/deadbeef``。

为安全起见，``west update`` 使用 ``git checkout --detach``
为每个被更新的项目在清单版本处检出分离的 ``HEAD``，
保留已检出的任何分支。
这通常是一个安全操作，不会修改你的任何本地分支。

但是，如果你曾在 West 检出的分离 ``HEAD`` 之上添加了一些本地提交，
git 会警告你留下了一些不再被任何分支引用的提交。
这些提交将来某个时候可能被垃圾回收而丢失。
如果项目中有本地提交，为避免这种情况，
请确保在运行 ``west update`` 之前已检出某个本地分支。

如果你更愿意对本地已检出的分支执行变基（rebase），
使用 ``-r``（``--rebase``）选项。

如果你希望只要本地分支指向新 ``manifest-rev`` 后代上的提交，
``west update`` 就保持该分支处于检出状态，
使用 ``-k``（``--keep-descendants``）选项。

.. note::

   如果项目在你的分支与清单引入的新提交之间存在 git 冲突，
   ``west update --rebase`` 将会失败。
   你应该像平时使用 ``git`` 那样立即解决这些冲突，
   或者使用 ``git -C <project_path> rebase --abort`` 暂时忽略传入的更改。

   在工作树干净的情况下，普通的 ``west update`` 从不失败，
   因为它不试图保留你的提交，只是将它们放在一边。

   ``west update --keep-descendants`` 提供一个折中选项，
   它同样从不失败，但不会将所有项目一视同仁：

   - 在你的分支与传入提交发生分叉的项目中，
     它甚至不尝试变基，
     就像普通 ``west update`` 一样保留你的分支；
   - 在所有其他不需要变基或合并的项目中，
     它保持你的分支原地不动。

**一次性项目分组操作：**

``--group-filter`` 选项可用于在单次 ``west update`` 命令期间
更改哪些项目分组被启用或禁用。
项目分组功能的细节见 :ref:`west-manifest-groups`。

``west update`` 命令的行为就好像 ``--group-filter`` 选项的值
被追加到 :ref:`配置选项 <west-config-index>` ``manifest.group-filter`` 之后。

例如，运行 ``west update --group-filter=+foo,-bar`` 的效果，
就像你临时将字符串 ``"+foo,-bar"`` 追加到 ``manifest.group-filter`` 的值、
运行 ``west update``、然后再将 ``manifest.group-filter`` 恢复为原始值。

注意，使用 ``--group-filter=VALUE`` 语法而不是 ``--group-filter VALUE``，
可以避免在只想禁用单个分组（例如 ``--group-filter=-bar``）时
解析命令行选项的问题。

**子模块更新流程：**

如果清单中的项目有 ``submodules`` 键，
子模块将按如下方式更新，具体取决于 ``submodules`` 键的值。

如果项目为 ``submodules: true``，
West 首先用以下命令同步项目的子模块：

.. code-block::

   git submodule sync --recursive

然后 West 会在项目仓库中运行以下命令之一，
取决于你是否使用 ``--rebase`` 选项运行 ``west update``：

.. code-block::

   # without --rebase, e.g. "west update":
   git submodule update --init --checkout --recursive

   # with --rebase, e.g. "west update --rebase":
   git submodule update --init --rebase --recursive

否则，项目为 ``submodules: <list-of-submodules>``（子模块列表）。
在这种情况下，West 用以下命令同步项目的子模块：

.. code-block::

   git submodule sync --recursive -- <submodule-path>

然后按如下方式更新列表中的每个子模块，
取决于你是否使用 ``--rebase`` 选项运行 ``west update``：

.. code-block::

   # without --rebase, e.g. "west update":
   git submodule update --init --checkout --recursive <submodule-path>

   # with --rebase, e.g. "west update --rebase":
   git submodule update --init --rebase --recursive <submodule-path>

如果 :ref:`west-config` 选项 ``update.sync-submodules`` 为 false，
则跳过 ``git submodule sync`` 命令。

.. _west-built-in-misc:

其他项目命令
**********************

West 还有几个用于管理工作区中项目的命令，此处作一总结。
运行 ``west <command> -h`` 获取详细帮助。

- ``west compare``：将工作区的状态与清单进行比较
- ``west diff``：在本地项目仓库中运行 ``git diff``
- ``west forall``：在本地项目仓库中运行任意命令
- ``west grep``：在本地项目仓库中搜索模式
- ``west list``：按照格式字符串，打印清单中每个项目的一行信息
- ``west manifest``：管理清单文件。见 :ref:`west-manifest-cmd`。
- ``west status``：在本地项目仓库中运行 ``git status``

其他内置命令
***********************

最后，以下是其他内置命令的总结。

- ``west config``：获取或设置 :ref:`配置选项 <west-config>`
- ``west topdir``：打印 West 工作区的顶层目录
- ``west help``：获取某个命令的帮助，
  或打印工作区中所有命令（包括 :ref:`west-extensions`）的信息

.. rubric:: 脚注

.. [#fetchall]

   当给定 SHA 作为版本时，
   West 可能会从 Git 服务器获取所有引用（refs）。
   这是因为某些 Git 服务器历史上不允许直接获取 SHA。
