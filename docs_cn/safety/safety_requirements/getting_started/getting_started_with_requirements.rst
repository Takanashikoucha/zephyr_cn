.. _getting_started_with_safety_requirements:

需求管理入门
############################################

Zephyr 的需求管理由 `StrictDoc <https://github.com/strictdoc-project/strictdoc>`_ 提供支持，这是一款用于编写、组织和发布结构化需求的轻量级工具。
本节介绍如何设置和使用 `reqmgmt <https://github.com/zephyrproject-rtos/reqmgmt>`_ 仓库中提供的工具链。

概述
*********

``reqmgmt`` 仓库是 Zephyr 的官方需求工作区。它支持：

- 编写系统与软件需求
- 将需求与验证工件关联
- 生成可浏览的 HTML 文档
- 运行用于编辑和评审的本地 Web 界面

安装
************

StrictDoc 需要 Python 3.7 或更高版本。安装方法（你可能需要用 pip3 代替 pip）：

.. code-block:: bash

   pip install strictdoc

克隆 Zephyr 需求仓库：

.. code-block:: bash

   git clone https://github.com/zephyrproject-rtos/reqmgmt
   cd reqmgmt

使用
*****

将需求导出为 HTML：

.. code-block:: bash

   strictdoc export .

这会在 :file:`output/` 目录中生成一个静态站点。

启动本地 Web 界面：

.. code-block:: bash

   strictdoc server .

你应该会看到类似如下内容：

.. code-block:: bash

   Uvicorn running on http://127.0.0.1:5111 (Press CTRL+C to quit)

打开本地浏览器，粘贴上述地址，即可访问用于导航和编辑需求的基于浏览器的编辑器。

结构
*********

该仓库包含：

- :file:`docs/` — 按子系统组织的需求文档
- :file:`strictdoc.toml` — StrictDoc 的配置文件
- :file:`tasks.py` — 用于构建和验证需求的自动化辅助脚本

在线文档
******************

你可以在以下地址在线查看已发布的需求：

`https://zephyrproject-rtos.github.io/reqmgmt <https://zephyrproject-rtos.github.io/reqmgmt>`_

后续步骤
**********

- 浏览 :file:`docs/` 文件夹，查看示例需求文件
- 使用 Web 界面创建或编辑自己的需求
- 将需求与测试用例或源码模块关联，以实现可追溯性

``StrictDoc`` 通过规范化系统目标与软件实现之间的关联，帮助 Zephyr 迈向安全关键就绪状态。
