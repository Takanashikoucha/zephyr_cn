.. _west-workspaces:

工作区
########

本页更详细地描述在 :ref:`west-basics` 中引入的 *west 工作区* 概念。

.. _west-manifest-rev:

``manifest-rev`` 分支
***************************

West 在每个项目中创建并控制一个名为 ``manifest-rev`` 的 Git 分支。
该分支指向 manifest 文件在 :ref:`west-update` 最后一次运行时
为该项目指定的修订版。
其他工作区管理命令可能将 ``manifest-rev`` 用作
截至最近一次更新时上游修订版的参考点。
除其他用途外，``manifest-rev`` 分支允许 manifest 文件
使用 SHA 作为项目修订版。

虽然 ``manifest-rev`` 是普通的 Git 分支，west 会在下次更新时
重新创建和/或重置它。因此，检出它或以其他方式自行修改它是**危险的**。
例如，你手动添加到该分支的任何提交，
可能在你下次运行 ``west update`` 时丢失。
相反，检出一个其他名称的本地分支，
然后要么将其 rebase 到新的 ``manifest-rev`` 之上，
要么将 ``manifest-rev`` 合并到该分支中。

.. note::

   West 不在 manifest 仓库中创建 ``manifest-rev`` 分支，
   因为 west 不管理 manifest 仓库的分支或修订版。

``refs/west/*`` Git 引用
****************************

West 还在本地项目仓库中为自己保留所有以 ``refs/west/`` 开头的
Git 引用（如 ``refs/west/foo``）。与 ``manifest-rev`` 不同，
这些引用不是普通分支。West 在此处的行为是实现细节；
用户不应依赖这些引用的存在或行为。

.. _west-developing-in-a-git-repository:

在 git 仓库中开发
******************************

``west`` 工作区中的"项目"是普通的 git 仓库。
放任不管时，west 只创建和更新 ``manifest-rev`` 分支
以及 ``refs/west/`` 下的引用；你创建的分支归你所有，
west 只在你用 ``west update --rebase`` 要求它时才 rebase 它们。

这也是为什么普通的 :ref:`west update <west-update>`
会让你停留在分离的 ``HEAD`` 上：
它检出新的 ``manifest-rev`` 并将你的分支留在原地。
理由参见 :ref:`west-update-detached-heads`。

.. note::

   Zephyr *模块* 和 west 项目不是同一回事，
   即使 west 项目通常也是模块；参见 :ref:`modules-vs-projects`。
   下面的 git 工作流适用于所有 west 项目，
   无论它们是否是 Zephyr 模块。

当你有本地更改时，效果良好的工作流是：

#. 在仓库中创建一个分支并像往常一样向其中提交：

   .. code-block:: console

      git -C <repository-path> switch --create <your-branch>

#. 用 ``west update --rebase`` 更新你的工作区，然后查看更改了什么：

   .. code-block:: console

      west update --rebase
      west compare

   你的分支保持检出状态，并被 rebase 到新的 ``manifest-rev`` 上。
   这是 west 触及你自己的分支的唯一时机。
   如果发生冲突，命令失败，你用 git 像往常一样解决。

#. 如果你不希望 west rebase 你的分支，
   普通的 ``west update`` 会切换到别处（除非这导致 git 冲突）。
   ``west update --keep-descendants`` 是一个从不失败的第三种选项。
   参见 ``west update --help`` 中的 ``checked out branch behavior`` 选项组，
   以及 :ref:`west-update` 获取所有细节。

在分离的 ``HEAD`` 上提交
=================================

不要在 ``west update`` 留下的分离 ``HEAD`` 上提交：
git 会警告你，这些提交无法从任何分支到达，
稍后可能被垃圾回收。
相反，为你的工作创建一个分支；
或者使用专为"无分支"工作设计的替代 git 客户端，例如 `JJ`_。

.. _JJ: https://www.jj-vcs.dev/

私有仓库
********************

你可以使用 west 从私有仓库获取。
这没有任何 west 特定的内容。

``west update`` 命令本质上在项目的 ``manifest-rev`` 分支
必须更新到新获取的提交时运行 ``git fetch YOUR_PROJECT_URL``。
确保获取成功是你的环境的责任。

你可以手动输入密码，或使用 Git 内置的任何
`credential helpers built in to Git`_。
由于 Git 内置了凭据存储，不需要 west 特定的功能。

以下章节涵盖运行 ``west update`` 而无需输入密码的常见情况，
以及如何排查问题。

.. _credential helpers built in to Git:
   https://git-scm.com/docs/gitcredentials

通过 HTTPS 获取
==================

在 Windows 上从 GitHub 获取时，近期版本的 Git
会在图形窗口中提示你一次 GitHub 密码，
然后存储它供将来使用（在默认安装中）。
因此，从 GitHub 无密码获取应该在你做过一次后
在 Windows 上"开箱即用"。

一般来说，你可以使用 "store" git 凭据助手
在磁盘上存储你的凭据。
参见 `git-credential-store`_ 手册页获取细节。

要对工作区中的所有仓库使用此助手，运行：

.. code-block:: shell

   west forall -c "git config credential.helper store"

要仅对 ``foo`` 和 ``bar`` 项目使用此助手，运行：

.. code-block:: shell

   west forall -c "git config credential.helper store" foo bar

要在你的计算机上默认使用此助手，运行：

.. code-block:: shell

   git config --global credential.helper store

在 GitHub 上，你可以设置 `personal access token`_
来代替你的账户密码使用。
（如果你的账户启用了双因素认证，这可能是必需的；
即使双因素认证被禁用，
也可能比以纯文本存储你的账户密码更可取。）

你可以使用 Git 凭据存储用 GitHub PAT（Personal Access Token）
进行认证，如下所示：

.. code-block:: shell

   echo "https://x-access-token:$GH_TOKEN@github.com" >> ~/.git-credentials

如果你不想在文件系统上存储任何凭据，
你可以改用 `git-credential-cache`_ 临时在内存中存储它们。

如果你配置了通过 SSH 获取，你可以使用 Git URL 重写功能。
以下命令指示 Git 对 GitHub 使用 SSH URL 而非 HTTPS URL：

.. code-block:: shell

   git config --global url."git@github.com:".insteadOf "https://github.com/"

.. _git-credential-store:
   https://git-scm.com/docs/git-credential-store#_examples
.. _git-credential-cache:
   https://git-scm.com/docs/git-credential-cache
.. _personal access token:
   https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

通过 SSH 获取
================

如果你的 SSH 密钥没有密码，获取应该直接可用。
如果有密码，你可以使用 `ssh-agent`_ 避免每次手动输入。

在 GitHub 上，参见 `Connecting to GitHub with SSH`_
获取配置和密钥创建的细节。

.. _ssh-agent:
   https://www.ssh.com/ssh/agent
.. _Connecting to GitHub with SSH:
   https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh

项目位置
*****************

项目可以位于工作区内部的任何位置，但不能"逃出"工作区。

换句话说，项目仓库不必位于 manifest 仓库的子目录中，
也不必是顶层目录的直接子目录。
然而，项目必须具有工作区内的路径。

你可以将工作区中某个项目的仓库目录替换为
指向你计算机上其他位置的符号链接，但 west 不会为你这样做。

.. _west-topologies:

支持的拓扑
********************

以下是 west 支持的示例源代码拓扑。

- T1：星形拓扑，zephyr 是 manifest 仓库
- T2：星形拓扑，Zephyr 应用是 manifest 仓库
- T3：森林拓扑，独立的 manifest 仓库

T1：星形拓扑，zephyr 是 manifest 仓库
====================================================

- zephyr 仓库作为中央仓库，
  并在其 :file:`west.yml` 中指定其 :ref:`modules`
- 与现有机制的类比：以 zephyr 作为超级项目的 Git submodules

这是默认拓扑。
参见 :ref:`west-workspace` 了解主线 Zephyr 如何是该拓扑的示例。

.. _west-t2:

T2：星形拓扑，应用是 manifest 仓库
=========================================================

- 对专注于单个应用的人有用
- 包含 Zephyr 应用的仓库作为中央仓库，
  并在其 :file:`west.yml` 中命名构建该应用所需的其他项目。
  这包括 zephyr 仓库和任何模块。
- 与现有机制的类比：以应用作为超级项目、
  zephyr 和其他项目作为 submodules 的 Git submodules

使用该拓扑的工作区看起来像这样：

.. code-block:: none

   west-workspace/
   │
   ├── application/         # .git/     │
   │   ├── CMakeLists.txt               │
   │   ├── prj.conf                     │  never modified by west
   │   ├── src/                         │
   │   │   └── main.c                   │
   │   └── west.yml         # main manifest with optional import(s) and override(s)
   │                                    │
   ├── modules/
   │   └── lib/
   │       └── zcbor/       # .git/ project from either the main manifest or some import.
   │
   └── zephyr/              # .git/ project
       └── west.yml         # This can be partially imported with lower precedence or ignored.
                            # Only the 'manifest-rev' version can be imported.


这是一个示例 :file:`application/west.yml`，
使用 :ref:`west-manifest-import`（自 west 0.7 可用）
将 Zephyr v2.5.0 及其模块导入应用 manifest 文件：

.. code-block:: yaml

   # Example T2 west.yml, using manifest imports.
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v2.5.0
         import: true
     self:
       path: application

如果你以这种方式使用 ``import:``，
你仍然可以选择性地"覆盖"单个 Zephyr 模块；
参见 :ref:`west-manifest-ex1.3` 获取示例。

做同一件事的另一种方式是将 :file:`zephyr/west.yml`
复制/粘贴到 :file:`application/west.yml`，
添加一个 zephyr 项目本身的条目，如下所示：

.. code-block:: yaml

   # Equivalent to the above, but with manually maintained Zephyr modules.
   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
     defaults:
       remote: zephyrproject-rtos
     projects:
       - name: zephyr
         revision: v2.5.0
         west-commands: scripts/west-commands.yml
       - name: net-tools
         revision: some-sha-goes-here
         path: tools/net-tools
       # ... other Zephyr modules go here ...
     self:
       path: application

（``west-commands`` 在那里是为了 :ref:`west-build-flash-debug`
和其他 Zephyr 特定的 :ref:`west-extensions`。
使用 ``import`` 时它不是必需的。）

使用 ``import`` 的主要优势是不必单独跟踪
被导入项目的修订版。在上面的示例中，使用 ``import`` 意味着
Zephyr 的 :ref:`module <modules>` 版本自动从
:file:`zephyr/west.yml` 修订版确定，
而不是必须被复制/粘贴（并维护）在它们自己。

T3：森林拓扑
==================

- 对支持多个独立应用或没有"中央"仓库的
  下游发行版的人有用
- 一个专用的 manifest 仓库，不包含任何 Zephyr 源代码，
  并指定一个全部位于同一"层级"的项目列表
- 与现有机制的类比：基于 Google repo 的源代码发行版

使用该拓扑的工作区看起来像这样：

.. code-block:: none

   west-workspace/
   ├── app1/               # .git/ project
   │   ├── CMakeLists.txt
   │   ├── prj.conf
   │   └── src/
   │       └── main.c
   ├── app2/               # .git/ project
   │   ├── CMakeLists.txt
   │   ├── prj.conf
   │   └── src/
   │       └── main.c
   ├── manifest-repo/      # .git/ never modified by west
   │   └── west.yml        # main manifest with optional import(s) and override(s)
   ├── modules/
   │   └── lib/
   │       └── zcbor/      # .git/ project from either the main manifest or
   │                       #       from some import
   │
   └── zephyr/             # .git/ project
       └── west.yml        # This can be partially imported with lower precedence or ignored.
                           # Only the 'manifest-rev' version can be imported.

这是一个示例 T3 :file:`manifest-repo/west.yml`，
使用 :ref:`west-manifest-import`（自 west 0.7 可用）
导入 Zephyr v2.5.0 及其模块，然后添加 ``app1`` 和 ``app2`` 项目：

.. code-block:: yaml

   manifest:
     remotes:
       - name: zephyrproject-rtos
         url-base: https://github.com/zephyrproject-rtos
       - name: your-git-server
         url-base: https://git.example.com/your-company
     defaults:
       remote: your-git-server
     projects:
       - name: zephyr
         remote: zephyrproject-rtos
         revision: v2.5.0
         import: true
       - name: app1
         revision: SOME_SHA_OR_BRANCH_OR_TAG
       - name: app2
         revision: ANOTHER_SHA_OR_BRANCH_OR_TAG
     self:
       path: manifest-repo

你也可以"手工"做这件事，
通过复制/粘贴 :file:`zephyr/west.yml`，
如 :ref:`上面 <west-t2>` 对 T2 拓扑所示，
带有相同的注意事项。

.. _workspace-as-git-repo:

不支持：工作区顶层目录作为 .git 仓库
**************************************************

一些用户已请求支持将工作区 :ref:`topdir <west-workspace>`
作为 git 仓库，如下面的示例：

.. code-block:: none

   my-workspace/                  # workspace topdir
   ├── .git/                      # puts the entire workspace in a git repository
   ├── .west/                     # marks the location of the topdir
   └── [ ... other projects ...]

这**不是**一个官方支持的拓扑。
作为一个设计决策，west 假设工作区顶层目录本身不是 git 仓库。

你可能能够为自己和你的目标让像这样的东西"可用"。
然而，west 的未来版本可能包含可以"破坏"你的配置的更改。
