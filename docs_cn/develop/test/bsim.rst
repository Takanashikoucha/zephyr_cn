.. _bsim:

BabbleSim
#########

BabbleSim 与 Zephyr
********************

在 Zephyr 项目中，我们使用 `Babblesim`_ 模拟器来测试一些 Zephyr 无线协议，包括蓝牙 LE 协议栈、802.15.4 以及部分网络协议栈。

BabbleSim_ 是一款物理层模拟器，与 Zephyr :ref:`bsim 开发板<bsim boards>` 组合使用，可以模拟由蓝牙 LE 和 15.4 设备组成的网络。当我们以 :ref:`bsim 开发板<bsim boards>` 为目标构建 Zephyr 时，会生成一个 Linux 可执行文件，其中包含应用、Zephyr 操作系统以及硬件（HW）模型。

当存在无线活动时，该 Linux 可执行文件会连接到 BabbleSim 物理层模拟，以模拟无线信道。

在 BabbleSim 文档中，你可以找到有关如何 `获取 <https://babblesim.github.io/fetching.html>`_ 和 `构建 <https://babblesim.github.io/building.html>`_ 模拟器的更多信息。在 :ref:`nrf52_bsim<nrf52_bsim>`、:ref:`nrf5340bsim<nrf5340bsim>` 和 :ref:`nrf54l15bsim<nrf54l15bsim>` 开发板的文档中，你可以找到有关如何以这些特定开发板为目标构建 Zephyr 的更多信息以及一些示例。

测试类型
**************

无无线活动的测试：用 twister 运行 bsim 测试
====================================================

:ref:`bsim 开发板<bsim boards>` 可以在无无线活动的情况下使用，这种情况下不需要将它们连接到物理层模拟。得益于这一点，这些目标开发板可以像 :zephyr:board:`native_sim<native_sim>` 一样配合 :ref:`twister <twister_script>` 使用，运行所有标准的 Zephyr twister 测试，但使用的是真实 SoC 硬件的模型及其驱动程序。

有无线活动的测试
=========================

当存在无线活动时，BabbleSim 测试至少需要一个正在运行的物理层模拟，大多数测试还需要多于 1 个模拟设备。因此，这些测试通过为每个测试运行一个专用脚本来执行，该脚本会启动所需的模拟设备以及带有相应参数的物理层可执行文件，以及其他任何所需的工具。

要能够用 twister 运行它们，应使用 :ref:`bsim harness <twister_bsim_harness>`。

这些测试保存在 :zephyr_file:`tests/bsim/` 文件夹中。

请查看下面的子章节，了解如何构建和运行这些测试，以及它们遵循的约定。

有两类主要的测试：

* 自检查嵌入式应用/测试：其中一些模拟设备的应用被构建时包含若干检查，用于判定测试是通过还是失败。这些嵌入式应用测试使用 :ref:`bs_tests<bsim_boards_bs_tests>` 系统报告通过或失败，并且在很多情况下会将多个测试构建进同一个二进制文件。

* 使用 EDTT_ 工具的测试：其中 EDTT（python）测试通过 RPC 机制控制嵌入式应用，并判定测试是否通过。目前这些测试涵盖了蓝牙认证测试套件中一个非常重要的子集。

关于不同类型测试如何与 BabbleSim 和 bsim 开发板关联的更多信息，可以在 :ref:`bsim 开发板测试章节<bsim_boards_tests>` 中找到。

测试覆盖率与 BabbleSim
***************************

由于 :ref:`bsim 开发板 <bsim boards>` 基于 POSIX 架构，你可以轻松收集测试覆盖率信息。

请查看 :ref:`覆盖率生成页面 <coverage_posix>` 了解更多信息，并注意你只需向 twister 传递 ``--coverage`` 选项，即可自动使用 :kconfig:option:`CONFIG_COVERAGE` 构建并生成覆盖率报告。

.. _BabbleSim:
   https://BabbleSim.github.io

.. _EDTT:
   https://github.com/EDTTool/EDTT

构建和运行测试
******************************

请查看 :ref:`nrf52_bsim <nrf52bsim_build_and_run>` 页面，了解如何设置模拟器的说明。

你可以使用 :ref:`twister <twister_script>` 构建和运行这些测试。要运行多设备测试，你需要向 twister 传递选项 ``--fixture bsim_multi_test``。

例如，从 ${ZEPHYR_BASE} 出发，你可以用以下命令构建并运行一个蓝牙测试：

.. code-block:: bash

   twister -p nrf52_bsim/native -T tests/bsim/bluetooth/host/adv/chain/ --fixture bsim_multi_test

如果测试二进制文件已经构建好，你也可以直接使用该测试的独立测试脚本运行它。例如：

.. code-block:: bash

   BOARD=nrf52_bsim/native tests/bsim/bluetooth/host/adv/chain/tests_scripts/adv_chain.sh

:ref:`Twister 命令行选项 <twister_commandline_options>` 如 ``-n, --no-clean``、``--aggressive-no-clean`` 或 ``-b, --build-only`` 在调试或修复问题时可能很有用。

旧版批处理脚本
====================

在 twister bsim harness 被添加之前，构建和运行多设备 bsim 测试依赖 :zephyr_file:`tests/bsim/` 文件夹中的两个脚本：``compile.sh`` 和 ``run_parallel.sh``。这些脚本被 CI 系统用于构建所需的镜像并批量执行这些测试。它们也被设计为用户构建和执行自己测试的工具。这些脚本现在仍然可以使用，但建议用户过渡到使用 :ref:`twister <twister_script>` 和 ``tests.yaml`` 定义。

这些脚本期望设置若干环境变量。例如，从 Zephyr 根文件夹出发，你可以运行：

.. code-block:: bash

   # Build all the tests
   ${ZEPHYR_BASE}/tests/bsim/compile.sh

   # Run them (in parallel)
   RESULTS_FILE=${ZEPHYR_BASE}/myresults.xml \
      SEARCH_PATH=${ZEPHYR_BASE}/tests/bsim \
         ${ZEPHYR_BASE}/tests/bsim/run_parallel.sh

或者只构建并运行特定子集，例如 host 广播测试：

.. code-block:: bash

   # Build the Bluetooth host advertising tests
   ${ZEPHYR_BASE}/tests/bsim/bluetooth/host/adv/compile.sh

   # Run them (in parallel)
   RESULTS_FILE=${ZEPHYR_BASE}/myresults.xml \
      SEARCH_PATH=${ZEPHYR_BASE}/tests/bsim/bluetooth/host/adv \
         ${ZEPHYR_BASE}/tests/bsim/run_parallel.sh

请查看 ``run_parallel.sh`` 的帮助信息，了解如何用该脚本批量运行测试的更多选项和示例。

构建测试所需的二进制文件之后，你可以直接使用该测试的独立测试脚本运行它。

例如，你可以用以下命令构建网络测试所需的二进制文件：

.. code-block:: bash

   WORK_DIR=${ZEPHYR_BASE}/bsim_out ${ZEPHYR_BASE}/tests/bsim/net/compile.sh

然后直接运行其中一个测试：

.. code-block:: bash

   ${ZEPHYR_BASE}/tests/bsim/net/sockets/echo_test/tests_scripts/echo_test_802154.sh

约定
===========

测试代码
---------

请参见 :zephyr_file:`蓝牙示例测试 <tests/bsim/bluetooth/host/misc/sample_test/README.rst>` 了解适用于测试代码的约定。

测试脚本
------------

请遵循现有约定，不要设计一次性的专用 runner（例如 python 脚本或另一个 shell 抽象层）。

理由是：如果所有测试都以相同的方式、使用相同的变量等运行，维护者执行涉及构建系统或兼容性变更的跨树更新时会更容易、更快。

如果你有一个改进测试脚本的好主意，请提交一个 PR 修改*所有*测试脚本，以便让所有人受益并保持同质性。你当然可以先在 RFC issue 或 babblesim discord 频道中讨论。

以下划线（``_``）开头的脚本不会被自动发现和运行。它们既可以作为主脚本的辅助函数，也可以用作本地开发工具，例如在本地构建和运行测试、调试等。

以下是约定：

- 每个测试由一个扩展名为 ``.sh`` 的 shell 脚本定义，位于名为 ``tests_scripts/`` 的子文件夹中。
- 建议每个脚本文件只运行一个测试。这有利于 CI 中运行的并行化。
- 脚本假定其所需的二进制文件已经构建好，不应自行编译二进制文件。
- 脚本会为每个模拟设备和物理层模拟生成进程。
- 如果测试通过，脚本必须向调用它的 shell 返回 0；如果测试失败，则返回非 0。
- 每个测试必须有唯一的模拟 id，以支持并行运行不同的测试。
- 脚本和镜像都不应修改 ``${BSIM_OUT_PATH}/results/<simulation_id>/`` 或 ``/tmp/`` 文件夹之外的工作站文件系统内容。也就是说，它们不应留下散落的文件。
- 需要多次连续模拟的测试（例如，模拟设备配对、断电，然后作为一次新的模拟重新上电）应为每个模拟段使用单独的模拟 id，确保每个段的无线活动都可以事后（a posteriori）检查。
- 避免过长的测试。如果测试运行时间超过 20 秒，应考虑是否可能将其拆分为若干独立的测试。
- 如果测试运行时间超过 5 秒，请将 ``EXECUTE_TIMEOUT`` 设置为至少是实测运行时间 5 倍的值。
- 不要把 ``EXECUTE_TIMEOUT`` 设置为低于默认值的值。
- 测试输出不应过于冗长：预期输出少于一百行。请大量使用 ``LOG_DBG()``，但不要默认启用 ``DBG`` 日志级别。
- 使用物理层模拟的测试脚本应将传递给测试脚本的任何额外参数直接传递给 Phy 可执行文件。例如，这用于以检查模式（``-c``）运行 Phy，此时 Phy 会验证上一次模拟与本次模拟产生了完全相同的无线流量。
