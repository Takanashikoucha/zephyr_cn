.. _create_first_safety_requirements:

创建你的第一个 Zephyr RTOS 需求
#########################################

仓库概述
*******************

Zephyr 的需求在 ``reqmgmt`` 仓库中使用 `StrictDoc <https://github.com/strictdoc-project/strictdoc>`_ 进行管理。该仓库包含：

- :file:`docs/`：包含 StrictDoc 格式的需求文档
- :file:`tools/`：实用脚本和配置
- :file:`strictdoc.toml`：StrictDoc 的项目配置
- :file:`tasks.py`：使用 Invoke 进行任务自动化


步骤 1：创建或编辑需求文件
*****************************************

导航到仓库中的 :file:`docs/` 文件夹。

文件夹概述
---------------

:file:`docs/` 文件夹包含所有以 StrictDoc 格式编写的需求文档。

:file:`docs/` 文件夹包含两个子文件夹，组织方式如下：

- :file:`system_requirements/`
  包含描述 Zephyr RTOS 总体目标、约束和预期行为的高层系统需求。

  - :file:`system_requirements.sgra`
    包含定义需求正式结构的语法（GRAMMAR）
  - :file:`index.sdoc` 包含实际的需求陈述

- :file:`software_requirements/`
  包含组件级需求。该文件夹中的每个文件对应一个特定的子系统或模块。

  - :file:`software_requirements.sgra` 包含所有软件需求的语法
  - 一组 :file:`.sdoc` 片段文件，它们共同编译成一份大型软件需求文档，例如：

    - :file:`interrupts.sdoc`
    - :file:`queues.sdoc`
    - :file:`semaphore.sdoc`
    - :file:`threads.sdoc`

这些文件是模块化的，允许贡献者独立地针对系统的特定领域进行工作。
你可以编辑现有的 :file:`.sdoc` 文件，也可以创建新文件。下面是一个需求块的基本示例：

.. code-block:: text

   [REQUIREMENT]
   UID: ZEP-SRS-17-1
   STATUS: Draft
   TYPE: Functional
   COMPONENT: File System
   TITLE: Create file
   STATEMENT: >>>
   Zephyr shall provide file create capabilities for files on the file system.
   <<<

将 UID 设置为 ``TBD``，以便 StrictDoc 能在后续步骤中自动生成它。

步骤 2：保存文件
*********************

将文件保存在 :file:`docs/` 文件夹中的系统或软件需求子文件夹中。
如果你创建新文件，请给它一个有意义的名称，通常指其内容所针对的组件或功能。

步骤 3：自动分配 UID
**********************************

从仓库根目录运行以下命令：

.. code-block:: bash

   strictdoc manage auto-uid .

该命令会：

- 遍历项目目录

- 找到 ``UID: TBD`` 的需求

- 为每个需求分配唯一标识符

步骤 4：验证 UID 分配
*********************************

再次打开文件。你现在应该看到类似如下内容：

.. code-block:: text

   UID: ZEP-SRS-17-2
   STATUS: Draft
   TYPE: Functional
   COMPONENT: File System
   TITLE: Create file
   STATEMENT: >>>
   Zephyr shall provide file create capabilities for files on the file system.
   <<<

注意：UID 格式可以在 :file:`strictdoc.toml` 中配置。

可选：生成 HTML 文档
*************************************

构建需求文档的 HTML 版本：

.. code-block:: bash

   strictdoc export .

这会在 :file:`output/` 文件夹中生成可浏览的文档。

可选：启动 Web 编辑器
*******************************

交互式浏览和编辑需求：

.. code-block:: bash

   strictdoc server .

这会启动一个用于编辑和评审需求的本地 Web 界面。

总结
*******

- 在 :file:`docs/` 中创建或编辑一个 ``UID: TBD`` 的需求
- 运行 ``strictdoc manage auto-uid .`` 分配 UID
- 可选地生成 HTML 文档或启动 Web 编辑器

StrictDoc 帮助 Zephyr 跨平台维护结构化、可追溯、可编辑的需求。
