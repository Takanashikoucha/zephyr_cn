.. _twister_robot_harness:

Robot
#####
Zephyr 支持 `Robot Framework <https://robotframework.org/>`_ 作为自动化测试的解决方案之一。

Robot 文件允许以人类可读的文本格式表达交互式测试场景，并在仿真或硬件上执行它们。目前 Zephyr 集成支持在 `Renode <https://renode.io/>`_ 仿真框架、QEMU 和 Native Simulator 中运行 Robot 测试。

要用 twister 执行 Robot 测试套件，运行以下命令：

.. code-block:: console

   $ west twister --platform hifive1 --test samples/subsys/shell/shell_module/sample.shell.shell_module.robot

编写 Robot 测试
===================

Robot Framework 本身提供的关键字列表，参见 `Robot 官方文档 <https://robotframework.org/robotframework/>`_。

有关在 Renode 中编写和运行 Robot Framework 测试的信息，可在 Renode 文档的 `测试章节 <https://renode.readthedocs.io/en/latest/introduction/testing.html>`_ 中找到。该章节提供了最常用关键字的列表，以及指向其定义源代码的链接。

可以通过以下方式扩展该框架：在 Robot 测试套件文件中直接定义新关键字、作为外部 Python 库，或者像 Renode 那样通过 XML-RPC 动态扩展。详情参见 Robot 官方文档中的 `扩展 Robot Framework <https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#extending-robot-framework>`_ 章节。

运行单个测试套件
==========================

要运行单个测试套件而非整组测试，可以运行：

.. code-block:: bash

   $ west twister -p qemu_riscv32 -s arch.shared_interrupt

``robot`` 测试框架用于在仿真目标（Qemu、Native Simulator、Renode）中执行 Robot Framework 测试套件。

robot_testsuite: <robot 文件路径>（默认为空）
    指定一个或多个包含要运行的 Robot Framework 测试套件的文件的文件路径。

robot_option: <robot 选项>（默认为空）
    发送给 robotframework 的一个或多个选项。
