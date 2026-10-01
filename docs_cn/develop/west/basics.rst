.. _west-basics:

基础
######

本页介绍 West 的基本概念，并提供进一步阅读的参考。

West 的内置命令允许你在同一个 :term:`工作区 <west workspace>` 目录下操作 :term:`项目 <west project>`（Git 仓库）。

West 的工作方式如下：``west init`` 命令创建 :term:`West 工作区 <west workspace>` 并克隆 :term:`清单仓库 <west manifest repository>`；而 ``west update`` 命令负责最初克隆、之后更新工作区中清单里列出的 :term:`项目 <west project>`。

示例工作区
*****************

如果你已按照 :ref:`getting_started`（入门指南）操作，你的本地 :term:`West 工作区 <west workspace>`——在本例中即名为 :file:`zephyrproject` 的文件夹及其所有子文件夹——看起来像这样：

.. code-block:: none

   zephyrproject/                 # west topdir
   ├── .west/                     # marks the location of the topdir
   │   └── config                 # per-workspace local configuration file
   │
   │   # The manifest repository, never modified by west after creation:
   ├── zephyr/                    # .git/ repo
   │   ├── west.yml               # manifest file
   │   └── [... other files ...]
   │
   │   # Projects managed by west:
   ├── modules/
   │   └── lib/
   │       └── zcbor/             # .git/ project
   ├── tools/
   │   └── net-tools/             # .git/ project
   └── [ ... other projects ...]

.. _west-workspace:

工作区概念
******************

以下是关于该结构你需要理解的基本概念。更多细节见 :ref:`west-workspaces`。

topdir（顶层目录）
  如上例所示，:file:`zephyrproject` 是工作区顶层目录的名称，即 *topdir*（:file:`zephyrproject` 只是一个示例名——它可以是任何名字，如 ``z``、``my-zephyr-workspace`` 等）。

  你通常使用 :ref:`west init <west-init-basics>` 命令创建 topdir 以及若干其他文件和目录。

.west 目录
  topdir 中包含 :file:`.west` 目录。当 West 需要定位 topdir 时，它会查找 :file:`.west` 目录并采用其父目录。查找从当前工作目录开始（若失败，则回退到从 :envvar:`ZEPHYR_BASE` 环境变量指定的位置重新开始查找）。

配置文件
  文件 :file:`.west/config` 就是工作区的 :ref:`本地配置文件 <west-config>`。

清单仓库
  每个 West 工作区都恰好包含一个 *清单仓库*，它是一个包含 *清单文件* 的 Git 仓库。清单仓库的位置由本地配置文件中的 :ref:`manifest.path 配置选项 <west-config-index>` 指定。

  对于上游 Zephyr，:file:`zephyr` 就是清单仓库；但你可以配置 West 使用工作区中的任何 Git 仓库作为清单仓库，唯一要求是该仓库包含一个有效的清单文件。其他选项见 :ref:`west-topologies`，清单文件格式的细节见 :ref:`west-manifests`。

清单文件
  清单文件是一个 YAML 文件，用于定义 *项目*，即工作区中由 West 管理的其余 Git 仓库。清单文件默认命名为 :file:`west.yml`，可通过 ``manifest.file`` 本地配置选项覆盖。

  使用 :ref:`west update <west-update-basics>` 命令，可以依据清单文件的内容更新工作区中的各个项目。

项目
  项目是由 West 管理的 Git 仓库。项目在清单文件中定义，可以位于工作区内的任何位置。在上面的示例工作区中，``zcbor`` 和 ``net-tools`` 就是项目。

  默认情况下，Zephyr :ref:`构建系统 <build_overview>` 使用 West 获取工作区中所有项目的位置，因此它们包含的任何代码都可以作为 :ref:`modules`（模块）使用。但请注意，模块和项目 :ref:`在概念上并不相同 <modules-vs-projects>`。

扩展
  任何 West 已知的仓库（无论是清单仓库还是任何项目仓库）都可以定义 :ref:`west-extensions`（West 扩展）。扩展就是使用该工作区时可以运行的额外 West 命令。

  zephyr 仓库利用该特性提供 Zephyr 专属命令，例如 :ref:`west build <west-building>`。将这些命令定义为扩展，使 West 核心无需了解任何工作区所用 Zephyr 版本的具体细节。

被忽略的文件
  工作区中还可以包含 West 不管理的其他 Git 仓库或文件和目录。除了 :file:`.west`、清单仓库以及清单文件中指定的项目之外，West 基本上忽略工作区中的所有内容。

west init 和 west update
*************************

两个最重要的工作区相关命令是 ``west init`` 和 ``west update``。

.. _west-init-basics:

``west init`` 基础
--------------------

该命令用于创建 West 工作区。

.. important::

   ``west init`` 运行后，West 不会修改清单仓库的内容。请使用普通的 Git 命令来拉取新版本等。

你通常只需运行一次，例如：

.. code-block:: shell

   west init -m https://github.com/zephyrproject-rtos/zephyr --mr v2.5.0 zephyrproject

该命令将：

#. 创建顶层目录 :file:`zephyrproject`，并在其中创建 :file:`.west` 和 :file:`.west/config`
#. 从 https://github.com/zephyrproject-rtos/zephyr 克隆清单仓库，放入 :file:`zephyrproject/zephyr`
#. 在本地 zephyr 克隆中检出 ``v2.5.0`` git 标签
#. 在 :file:`.west/config` 中设置 ``manifest.path`` 为 ``zephyr``
#. 设置 ``manifest.file`` 为 ``west.yml``

此时你的工作区已几乎就绪；只需再运行 ``west update`` 将其余项目克隆到工作区中即可。

更多细节见 :ref:`west-init`。

.. _west-update-basics:

``west update`` 基础
----------------------

该命令确保你的工作区中包含与清单文件中各项目相匹配的 Git 仓库。

.. important::

   每当你检出清单仓库中的不同版本（revision）时，都应运行 ``west update``，以确保工作区包含新版本所期望的项目仓库。

``west update`` 命令通过以下步骤读取清单文件的内容：

#. 找到顶层目录。在上面的 ``west init`` 示例中，即找到 :file:`zephyrproject`。
#. 加载顶层目录中的 :file:`.west/config`，读取 ``manifest.path``（如 ``zephyr``）和 ``manifest.file``（如 ``west.yml``）选项。
#. 加载由这些选项指定的清单文件（如 :file:`zephyrproject/zephyr/west.yml`）。

随后，它依据清单文件决定缺失的项目应放置在何处、从哪些 URL 克隆，以及应在本地检出哪些 Git 版本。已存在的项目仓库会就地更新：拉取（fetch）并检出清单文件中对应的 Git 版本。

更多细节见 :ref:`west-update`。

其他内置命令
***********************

见 :ref:`west-built-in-cmds`。

.. _west-zephyr-extensions:

Zephyr 扩展命令
*****************

关于 Zephyr 扩展命令的信息，参见以下页面：

- :ref:`west-build-flash-debug`
- :ref:`west-sign`
- :ref:`west-zephyr-ext-cmds`
- :ref:`west-shell-completion`

故障排查
***************

见 :ref:`west-troubleshooting`。
