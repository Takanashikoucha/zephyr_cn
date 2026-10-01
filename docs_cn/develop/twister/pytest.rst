.. _integration_with_pytest:

与 pytest 测试框架集成
######################################

*请注意 Twister 与 pytest 的集成仍在进行中。并非每种平台类型（目前）都在 pytest 中受支持。
如果你发现集成的任何问题或有改进想法，请告知我们并打开一个 GitHub issue/enhancement。*

简介
************

Pytest 是一个 Python 框架，它 *"让编写小型、可读的测试变得容易，并且可以扩展以支持
应用和库的复杂功能测试"*（`<https://docs.pytest.org/en/7.3.x/>`_）。
Python 以其丰富的免费库和用于脚本编写的易用性著称。此外，pytest 利用插件（plugins）
和夹具（fixtures）的概念，增强了其可扩展性和可重用性。
一个 pytest 插件 ``pytest-twister-harness`` 被引入，用于提供 pytest 与 Twister 之间的集成，
使 Zephyr 社区能够在保持 Twister 作为主框架的同时利用 pytest 功能。

与 Twister 集成
************************

默认情况下，无需做任何操作即可在 Twister 中启用 pytest 支持。
该插件作为 Zephyr 代码树的一部分开发。为了实现免安装运行，
Twister 首先用该插件的路径扩展 ``PYTHONPATH``，然后在 pytest 调用期间，
向命令追加 ``-p twister_harness.plugin`` 参数。
如果偏好使用已安装的插件版本，必须向 Twister 调用添加 ``--allow-installed-plugin`` 标志。

基于 Pytest 的测试套件与其他 Twister 测试的发现方式相同，即通过 tests.yaml 文件的存在。
在其中，``harness`` 关键字告诉 Twister 如何处理给定测试。
对于 ``harness: pytest``，Twister 工作流的大多数环节（测试套件发现、
并行化、构建和报告）与其他测试框架保持一致。变化发生在执行步骤。
下图展示了该集成的简化概览。

.. figure:: figures/twister_and_pytest.svg
   :figclass: align-center


如果使用 ``harness: pytest``，Twister 将测试执行委托给 pytest，
通过将其作为子进程调用。必需参数（如构建目录、要使用的设备等）
通过 YAML 配置文件传递。当 pytest 完成时，Twister 查找 pytest 报告（results.xml）
并相应设置测试结果。

如何创建 pytest 测试
***************************

一个包含 pytest 测试、应用源代码和 Twister 配置 .yaml 文件的示例文件夹
可以如下所示：

.. code-block:: none

   test_foo/
   ├─── pytest/
   │    └─── test_foo.py
   ├─── src/
   │    └─── main.c
   ├─── CMakeList.txt
   ├─── prj.conf
   └─── testcase.yaml

一个 pytest 测试的示例位于
:zephyr_file:`samples/subsys/testsuite/pytest/shell/pytest/test_shell.py`。
使用 ``testcase.yaml`` 文件中提供的配置，Twister 从 ``src`` 构建应用，
然后如果 .yaml 文件包含 ``harness: pytest`` 条目，它在单独的子进程中调用 pytest。
示例配置文件可能如下：

.. code-block:: yaml

   tests:
      some.foo.test:
         harness: pytest
         tags: foo

默认情况下，pytest 尝试在与二进制源代码目录相邻的 ``pytest`` 目录中查找测试。
放置在 .yaml 文件 ``harness_config`` 节下的 ``pytest_root`` 关键字
可用于指向其他文件、目录或子测试（更多信息 :ref:`参见此处 <pytest_root>`）。

Pytest 扫描给定位置查找测试，遵循其默认
`发现规则 <https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#conventions-for-python-test-discovery>`_。

传递额外参数
=======================

有两种方式向被调用的 pytest 子进程传递额外参数：

#. 从 .yaml 文件，使用放置在 ``harness_config`` 节下的 ``pytest_args`` -
   更多信息 :ref:`参见此处 <pytest_args>`。
#. 通过 Twister 命令行接口作为 ``--pytest-args`` 参数。
   当想要从测试套件中选择特定测试用例时，这特别有用。例如，可以使用命令：

   .. code-block:: console

      $ west twister --platform native_sim -T samples/subsys/testsuite/pytest/shell \
      -s samples/subsys/testsuite/pytest/shell/sample.pytest.shell \
      --pytest-args='-k test_shell_print_version'

   命令行参数将扩展 .yaml 文件中的参数。如果同一参数在两处都存在，
   命令行的优先。

Fixtures（夹具）
********

dut
===

提供对 `DeviceAdapter`_ 类型对象的访问，它代表被测设备（Device Under Test）。
此夹具是 pytest 测试框架插件的核心。它用于启动 DUT（初始化日志、烧录设备、
连接串口等）。此夹具根据请求的类型（``native``、``qemu``、``hardware`` 等）
yield 准备好的设备。所有类型的设备共享相同的 API。
这允许编写与设备类型无关的测试。此夹具的作用域由放置在
``harness_config`` 节下的 ``pytest_dut_scope`` 关键字决定
（更多信息 :ref:`参见此处 <pytest_dut_scope>`）。


.. code-block:: python

   from twister_harness import DeviceAdapter

   def test_sample(dut: DeviceAdapter):
      dut.readlines_until(regex='Hello world')

shell
=====

提供 `Shell <shell_class_>`_ 类对象，带有用于与 shell 应用交互的方法。
它调用 ``wait_for_prompt`` 方法，在 DUT 就绪之前不启动场景。
shell 夹具调用 ``dut`` 夹具，因此可以访问其所有方法。
``shell`` 夹具添加了针对与 shell 交互优化的方法。
它可以代替 ``dut`` 用于测试。此夹具的作用域由放置在
``harness_config`` 节下的 ``pytest_dut_scope`` 关键字决定
（更多信息 :ref:`参见此处 <pytest_dut_scope>`）。

.. code-block:: python

   from twister_harness import Shell

   def test_shell(shell: Shell):
      shell.exec_command('help')

mcumgr
======

一个示例夹具，用于封装 ``mcumgr`` 命令行工具，该工具用于管理远程设备。
更多关于 MCUmgr 的信息可在此处找到 :ref:`mcu_mgr`。

.. note::
   此夹具要求 ``mcumgr`` 在系统 PATH 中可用

只有 MCUmgr 的选定功能被此夹具封装。例如，下面是一个使用 ``mcumgr`` 夹具的测试：

.. code-block:: python

   from twister_harness import DeviceAdapter, Shell, McuMgr

   def test_upgrade(dut: DeviceAdapter, shell: Shell, mcumgr: McuMgr):
      # free the serial port for mcumgr
      dut.disconnect()
      # upload the signed image
      mcumgr.image_upload('path/to/zephyr.signed.bin')
      # obtain the hash of uploaded image from the device
      second_hash = mcumgr.get_hash_to_test()
      # test a new upgrade image
      mcumgr.image_test(second_hash)
      # reset the device remotely
      mcumgr.reset_device()
      # continue test scenario, check version etc.


unlaunched_dut
==============

与 ``dut`` 夹具类似，但它不初始化设备。当需要更精细地控制构建过程时可以使用。
初始化设备的责任落在测试一侧。

.. code-block:: python

   from twister_harness import DeviceAdapter

   def test_sample(unlaunched_dut: DeviceAdapter):
      unlaunched_dut.launch()
      unlaunched_dut.readlines_until(regex='Hello world')

多 DUT 场景的夹具
********************************

多 DUT 夹具镜像单 DUT 夹具（``unlaunched_dut``、``dut``、``shell``），
但操作设备列表。它们对硬件和 ``native_sim`` 目标都有效；QEMU 不受支持。
它们要求 ``duts`` 条目存在于 ``twister_pytest_config.yaml`` 中。
Twister 自动生成此文件——对于模拟目标，它创建占位 DUT 条目，
因此无需硬件映射——然后调用 pytest。
当手动重新运行 pytest 而不通过 Twister 时（见 FAQ），同一配置文件被重用。
配置详情参见 Twister 文档中的 :ref:`twister_multi_duts_testing` 节。

unlaunched_duts
===============

类似于 ``unlaunched_dut``，但返回 `DeviceAdapter`_ 对象列表 -
每个保留的 DUT 一个 - 日志文件已初始化但设备尚未启动。

.. code-block:: python

   from twister_harness import DeviceAdapter

   def test_sample(unlaunched_duts: list[DeviceAdapter]):
      for dut in unlaunched_duts:
         dut.launch()
      unlaunched_duts[0].readlines_until(regex='Hello world')

duts
====

类似于 ``dut``，但返回已启动的 `DeviceAdapter`_ 对象列表。
所有设备并发烧录以减少设置时间。如果需要顺序烧录，
在你的 ``conftest.py`` 中覆盖此夹具。

.. code-block:: python

   from twister_harness import DeviceAdapter

   def test_sample(duts: list[DeviceAdapter]):
      assert len(duts) > 1
      duts[0].readlines_until(regex='Hello world')
      duts[1].readlines_until(regex='Hello world')

shells
======

类似于 ``shell``，但返回 `Shell <shell_class_>`_ 对象列表 -
每个保留的 DUT 一个 - 每个已经等待 shell 提示符。

.. code-block:: python

   from twister_harness import Shell

   def test_sample(shells: list[Shell]):
      assert len(shells) > 1
      shells[0].exec_command('help')
      shells[1].exec_command('help')


类（Classes）
*******

DeviceAdapter
=============

.. autoclass:: twister_harness.DeviceAdapter

   .. automethod:: launch

   .. automethod:: close

   .. automethod:: readline

   .. automethod:: readlines

   .. automethod:: readlines_until

   .. automethod:: write

.. _shell_class:

Shell
=====

.. autoclass:: twister_harness.Shell

   .. automethod:: exec_command

   .. automethod:: wait_for_prompt

   .. automethod:: get_filtered_output


Zephyr 项目中 pytest 测试的示例
**********************************************

* :zephyr:code-sample:`pytest_shell`
* MCUmgr 测试 - :zephyr_file:`tests/boot/with_mcumgr`
* LwM2M 测试 - :zephyr_file:`tests/net/lib/lwm2m/interop`
* GDB 桩（stub）测试 - :zephyr_file:`tests/subsys/debug/gdbstub`


FAQ（常见问题）
***

如何每个 pytest 会话只烧录/运行应用一次？
==========================================================

   ``dut`` 是负责烧录/运行应用的夹具。默认情况下，其作用域设为 ``function``。
   这可以通过向 .yaml 文件添加放置在 ``harness_config`` 节下的
   ``pytest_dut_scope`` 关键字来更改：

   .. code-block:: yaml

      harness: pytest
      harness_config:
         pytest_dut_scope: session

   更多信息可 :ref:`参见此处 <pytest_dut_scope>`。

如何只运行 python 文件中的某个特定测试？
======================================================

   这可以用几种方式实现。在 .yaml 文件中，可以使用放置在 ``harness_config``
   下的 ``pytest_root`` 条目添加，并附上应运行的测试列表：

   .. code-block:: yaml

      harness: pytest
      harness_config:
         pytest_root:
            - "pytest/test_shell.py::test_shell_print_help"

   特定测试也可以由 pytest ``-k`` 选项选择（关于 pytest 关键字过滤器的更多信息
   可 `在此处 <https://docs.pytest.org/en/latest/example/markers.html#using-k-expr-to-select-tests-based-on-their-name>`_
   找到）。它可以通过在 .yaml 文件的 ``pytest_args`` 中添加 ``-k`` 过滤器来应用：

   .. code-block:: yaml

      harness: pytest
      harness_config:
         pytest_args:
            - "-k test_shell_print_help"

   或者通过向 Twister 命令添加它，覆盖 .yaml 文件中的参数：

   .. code-block:: console

      $ west twister ... --pytest-args='-k test_shell_print_help'

如何在测试中获取所用设备类型的信息？
=====================================================

   这可以从 ``dut`` 夹具（代表 `DeviceAdapter`_ 对象）获取：

   .. code-block:: python

      device_type: str = dut.device_config.type
      if device_type == 'hardware':
         ...
      elif device_type == 'native':
         ...

如何在不通过 Twister 重建应用的情况下本地重新运行 pytest 测试？
============================================================================

   这可以通过再次运行 Twister 并向 Twister 命令添加 ``--test-only`` 参数实现。
   另一种方式是运行 Twister 并设置最高详细级别（``-vv``），
   然后从日志中复制粘贴用于生成 pytest 的命令
   （日志以 ``Running pytest command: ...`` 开头）。

   首先，用 Twister 运行场景：

   .. code-block:: console

      $ west twister -vv -ll debug -T samples/subsys/testsuite/pytest/shell \
      -s sample.pytest.shell --device-testing -p nrf54l15dk/nrf54l15/cpuapp --device-serial \
      /dev/ttyACM1 --west-flash=--erase

   Twister 自动在构建目录中生成配置文件 ``twister_pytest_config.yaml``，
   包含所有测试参数（包括设备配置等）。

   然后，如果尚未设置，导出所需的 PYTHONPATH 环境变量：

   .. code-block:: console

      $ export PYTHONPATH=$ZEPHYR_BASE/scripts/pylib/pytest-twister-harness/src

   最后，运行 pytest 命令：

   .. code-block:: console

      $ pytest -s -v -p twister_harness.plugin \
      --twister-config=twister-out/.../sample.pytest.shell/twister_pytest_config.yaml \
      samples/subsys/testsuite/pytest/shell/pytest


是否可能并行运行 pytest 测试？
=================================================

   基本上 ``pytest-harness-plugin`` 并非以并行运行 pytest 测试为意图编写的，
   尤其是那些专用于硬件的测试。其假设是测试的并行化由 Twister 完成，
   它负责管理可用资源（作业和硬件）。如果有人出于某些原因
   （例如通过 `pytest-xdist 插件 <https://pytest-xdist.readthedocs.io/en/stable/>`_）
   想这样做，则自行承担风险。


限制
***********

* 并非每种平台类型（目前）都在插件中受支持。
