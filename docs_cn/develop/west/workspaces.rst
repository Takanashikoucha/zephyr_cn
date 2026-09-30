.. _west-workspaces:

Workspaces
##########

本
页
更
详细
地
描述
在
:ref:`west-basics`
中
引入
的
*west
workspace*
概念。

.. _west-manifest-rev:

``manifest-rev``
branch
***************************

West
在
每个
project
中
创建
并
控制
一
个
命名
为
``manifest-rev``
的
Git
branch。
这
个
branch
指向
manifest
文件
在
:ref:`west-update`
最后
运行
时
为
project
指定
的
revision。
其他
workspace
管理
命令
可能
用
``manifest-rev``
作为
截至
这
次
最新
更新
的
upstream
revision
的
参考
点。
除
其他
目的
外，
``manifest-rev``
branch
允许
manifest
文件
用
SHAs
作为
project
revisions。

虽然
``manifest-rev``
是
普通
的
Git
branch，
west
会
在
下次
update
时
重新
创建
和/或
重置
它。
由
于
这
个
原因，
检出
它
或
其他
方式
修改
它
是
**危险
的**。
例如，
你
手动
添加
到
这
个
branch
的
任何
commits
可能
在
下次
你
运行
``west
update``
时
丢失。
相反，
检出
一
个
另一
名称
的
本地
branch，
并
要么
将
它
rebase
到
新
的
``manifest-rev``
之上，
或
将
``manifest-rev``
merge
到
它
中。

.. note::

   West
   不
   在
   manifest
   仓库
   中
   创建
   ``manifest-rev``
   branch，
   因为
   west
   不
   管理
   manifest
   仓库
   的
   branches
   或
   revisions。

``refs/west/*``
Git
refs
****************************

West
也
在
本地
project
仓库
中
为
自己
保留
所有
以
``refs/west/``
开头
的
Git
refs
（如
``refs/west/foo``）。
与
``manifest-rev``
不同，
这些
refs
不
是
普通
的
branches。
West
这里
的
行为
是


.. note::

   以下为原文（待翻译）

=========================================================

- Useful for those focused on a single application
- A repository containing a Zephyr application acts as the central repository
  and names other projects required to build it in its :file:`west.yml`. This
  includes the zephyr repository and any modules.
- Analogy with existing mechanisms: Git submodules with the application as
  the super-project, zephyr and other projects as submodules

A workspace using this topology looks like this:

.. code-block:: none

   west-workspace/
   │
   ├── application/         # .git/     │
   │   ├── CMakeLists.txt               │
   │   ├── prj.conf                     │  never modified by west
   │   ├── src/                         │
   │   │   └── main.c                   │
   │   └── west.yml         # main manifest with optional import(s) and override(s)
   │                                    │
   ├── modules/
   │   └── lib/
   │       └── zcbor/       # .git/ project from either the main manifest or some import.
   │
   └── zephyr/              # .git/ project
       └── west.yml         # This can be partially imported with lower precedence or ignored.
                            # Only the 'manifest-rev' version can be imported.


Here is an example :file:`application/west.yml` which uses
:ref:`west-manifest-import`, available since west 0.7, to import Zephyr v2.5.0
and its modules into the application manifest file:

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

You can still selectively "override" individual Zephyr modules if you use
``import:`` in this way; see :ref:`west-manifest-ex1.3` for an example.

Another way to do the same thing is to copy/paste :file:`zephyr/west.yml`
to :file:`application/west.yml`, adding an entry for the zephyr
project itself, like this:

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

(The ``west-commands`` is there for :ref:`west-build-flash-debug` and other
Zephyr-specific :ref:`west-extensions`. It's not necessary when using
``import``.)

The main advantage to using ``import`` is not having to track the revisions of
imported projects separately. In the above example, using ``import`` means
Zephyr's :ref:`module <modules>` versions are automatically determined from the
:file:`zephyr/west.yml` revision, instead of having to be copy/pasted (and
maintained) on their own.

T3: Forest topology
===================

- Useful for those supporting multiple independent applications or downstream
  distributions with no "central" repository
- A dedicated manifest repository which contains no Zephyr source code,
  and specifies a list of projects all at the same "level"
- Analogy with existing mechanisms: Google repo-based source distribution

A workspace using this topology looks like this:

.. code-block:: none

   west-workspace/
   ├── app1/               # .git/ project
   │   ├── CMakeLists.txt
   │   ├── prj.conf
   │   └── src/
   │       └── main.c
   ├── app2/               # .git/ project
   │   ├── CMakeLists.txt
   │   ├── prj.conf
   │   └── src/
   │       └── main.c
   ├── manifest-repo/      # .git/ never modified by west
   │   └── west.yml        # main manifest with optional import(s) and override(s)
   ├── modules/
   │   └── lib/
   │       └── zcbor/      # .git/ project from either the main manifest or
   │                       #       from some import
   │
   └── zephyr/             # .git/ project
       └── west.yml        # This can be partially imported with lower precedence or ignored.
                           # Only the 'manifest-rev' version can be imported.

Here is an example T3 :file:`manifest-repo/west.yml` which uses
:ref:`west-manifest-import`, available since west 0.7, to import Zephyr
v2.5.0 and its modules, then add the ``app1`` and ``app2`` projects:

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

You can also do this "by hand" by copy/pasting :file:`zephyr/west.yml`
as shown :ref:`above <west-t2>` for the T2 topology, with the same caveats.

.. _workspace-as-git-repo:

Not supported: workspace topdir as .git repository
**************************************************

Some users have asked for support making the workspace :ref:`topdir
<west-workspace>` a git repository, like this example:

.. code-block:: none

   my-workspace/                  # workspace topdir
   ├── .git/                      # puts the entire workspace in a git repository
   ├── .west/                     # marks the location of the topdir
   └── [ ... other projects ...]

This is **not** an officially supported topology. As a design decision, west
assumes that the workspace topdir itself is not a git repository.

You may be able to make something like this "work" for yourself and your own
goals. However, future versions of west might contain changes which can "break"
your setup.
