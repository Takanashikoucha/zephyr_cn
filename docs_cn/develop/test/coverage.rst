.. _coverage:

生成覆盖率报告
###########################

借助 Zephyr，你可以生成代码覆盖率报告，分析代码的哪些部分被某个测试或应用覆盖。

你可以用两种方式做到这一点：

* 在真实的嵌入式目标或 QEMU 中，使用 Zephyr 的 gcov 集成
* 直接在主机上，通过编译面向 POSIX 架构的应用

嵌入式设备或 QEMU 中的测试覆盖率报告
*************************************************

概览
========
`GCC gcov <gcov_>`_ 是一个测试覆盖率程序，与 GCC 编译器配合使用，为程序分析和生成测试覆盖率报告，帮助你编写更高效、运行更快的代码，并发现未被测试的代码路径。

在 Zephyr 中，gcov 在应用运行期间将覆盖率剖析数据收集到 RAM 中（而不是文件系统）。gcov 的收集和报告支持受可用 RAM 大小的限制，因此目前仅对嵌入式目标的 QEMU 仿真启用。

细节
=======
启用该功能分两部分。第一部分是为设备启用覆盖率，第二部分是在测试应用中启用。如前所述，使用 gcov 的代码覆盖率取决于可用 RAM 的大小。因此，为设备启用覆盖率时，请确保设备有足够的 RAM。例如，像 ``frdm_k64f`` 这样的小型设备可以运行简单的测试应用，但消耗更多 RAM 的复杂测试用例在启用覆盖率后会发生崩溃。

要为设备启用覆盖率，请在 Kconfig.board 文件中选择 :kconfig:option:`CONFIG_HAS_COVERAGE_SUPPORT`。

要报告特定测试应用的覆盖率，请设置 :kconfig:option:`CONFIG_COVERAGE`。

生成代码覆盖率报告的步骤
=======================================

以下步骤将为单个应用生成 HTML 覆盖率报告。

1. 使用 CONFIG_COVERAGE=y 构建代码。

    .. zephyr-app-commands::
       :board: mps2/an385
       :gen-args: -DCONFIG_COVERAGE=y -DCONFIG_COVERAGE_DUMP=y
       :goals: build
       :compact:

#. 将仿真器输出捕获到日志文件中。你可能需要用 :kbd:`Ctrl-A X` 终止仿真器，以便在覆盖率数据转储打印完成后结束运行：

    .. code-block:: console

      $ ninja -Cbuild run | tee log.log

#. 从保存的日志文件生成 gcov 的 ``.gcda`` 和 ``.gcno`` 文件：

    .. code-block:: console

      $ python3 scripts/gen_gcov_files.py -i log.log

#. 找到 SDK 中放置的 gcov 二进制文件。之后调用 ``gcovr`` 时，你需要传入对应架构的 gcov 二进制文件路径：

    .. code-block:: console

      $ find $ZEPHYR_SDK_INSTALL_DIR -iregex ".*gcov"

#. 创建用于存放报告的输出目录：

    .. code-block:: console

      $ mkdir -p coverage-report

#. 运行 ``gcovr`` 生成报告：

    .. code-block:: console

      $ gcovr -r $ZEPHYR_BASE . --html -o coverage-report/coverage.html --html-details --gcov-executable <gcov_path_in_SDK>

    .. _coverage_posix:

使用 POSIX 架构的覆盖率报告
*********************************************

编译 POSIX 架构时，你利用主机的原生工具构建一个原生可执行文件，其中包含你的应用、Zephyr 操作系统以及一些基本的硬件仿真。

这意味着你可以使用开发任何其他桌面应用时所用的相同工具。

要使用 ``gcc`` 的 `gcov`_ 构建应用，只需在编译前设置 :kconfig:option:`CONFIG_COVERAGE`。运行应用时，``gcov`` 覆盖率数据会转储到相应的 ``gcda`` 和 ``gcno`` 文件中。你可以用喜欢的工具对这些文件进行后处理。例如：

.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :gen-args: -DCONFIG_COVERAGE=y
   :host-os: unix
   :board: native_sim
   :goals: build
   :compact:

.. code-block:: console

   $ ./build/zephyr/zephyr.exe
   # Press Ctrl+C to exit
   $ lcov --capture --directory ./ --output-file lcov.info -q --rc lcov_branch_coverage=1
   $ genhtml lcov.info --output-directory lcov_html -q --ignore-errors source --branch-coverage --highlight --legend

.. note::

   你需要一个较新版本的 lcov（至少 1.14），且支持中间文本格式。较新的 Linux 发行版中提供此类软件包。

   或者，你可以使用 gcovr（至少 4.2 版本）。

使用 Twister 的覆盖率报告
******************************

Zephyr 的 :ref:`twister 脚本 <twister_script>` 可以自动根据已执行的测试生成覆盖率报告。你只需使用 ``--coverage`` 命令行选项调用它即可。

例如，你可以执行：

.. code-block:: console

    $ west twister --coverage -p qemu_x86 -T tests/kernel

或者：

.. code-block:: console

    $ west twister --coverage -p native_sim -T tests/bluetooth

这将生成 ``twister-out/coverage/index.html`` 报告，以及 ``gcovr`` 工具在 ``twister-out/coverage.json`` 中收集的覆盖率数据。

其他报告可以通过 ``--coverage-tool`` 和 ``--coverage-formats`` 命令行选项来选择。

要生成同时包含 Zephyr 源码和 Zephyr 仓库之外应用代码（参见 :ref:`应用类型 <zephyr-app-types>`）的代码覆盖率报告，请从项目目录调用 Twister 并使用 ``--coverage-basedir $ZEPHYR_BASE`` 命令行选项，例如：

.. code-block:: console

   $ west twister --coverage -p native_sim --coverage-basedir $ZEPHYR_BASE -T your_project_dir

.. note::

   默认情况下，Twister 调用 ``gcovr`` 工具，该工具以"所有符号链接均已解析为真实路径"为前提来过滤源文件（参见 `解析所有符号链接 <gcovr_symlinks_>`_）。因此，当开发环境包含带符号链接的目录时，为避免生成不完整的 ``gcovr`` 报告，要么 :ref:`ZEPHYR_BASE <important-build-vars>` 应包含真实路径，要么改用 ``lcov`` 工具并附加 Twister 命令行选项 ``--coverage-tool lcov``。

单元测试的流程有所不同，它们使用主机工具链构建，并且需要不同的开发板：

.. code-block:: console

   $ west twister --coverage -p unit_testing -T tests/unit

这会在与非单元测试相同的位置生成报告。

逐测试覆盖率矩阵
========================

默认情况下，覆盖率按测试场景进行聚合。要将覆盖率归因到单独的 :ref:`Ztest <test-framework>` 测试用例——例如回答"哪些测试执行了 ``foo.c`` 的第 X 行"——请传入 ``--coverage-per-test``：

.. code-block:: console

   $ west twister -p mps2/an385 -T tests/kernel --coverage --coverage-tool lcov \
       --coverage-per-test

这会启用 :kconfig:option:`CONFIG_ZTEST_COVERAGE_PER_TEST`，它在每个测试用例执行前重置 gcov 计数器，并在执行后转储一个带测试标签的独立覆盖率产物。在支持 semihosting 的平台上（QEMU 下的 ARM、RISC-V 和 Xtensa 目标，例如 ``mps2/an385``），逐测试数据会直接写入主机文件系统，避免了逐测试转储本会产生大量串行控制台流量的问题；其他平台则回退到串行控制台传输。

除了常规的聚合覆盖率报告外，这还会生成：

* 每个构建的 ``coverage/tests/`` 目录下，每个测试对应一个 ``<scenario>.<test>.info`` 跟踪文件（tracefile），以及
* ``twister-out/coverage/test_matrix.json``，一个机器可读的矩阵，包含 ``by_line`` 视图（``{file: {line: [tests]}}``）和 ``by_test`` 视图（``{test: {file: [lines]}}``）。

逐测试归因信息由矩阵（及其仪表盘）承载，而不是由聚合 lcov 报告承载：每个实例的覆盖率在聚合前被归并到一个跟踪文件中，因此运行结束时的报告规模与实例数量成正比，而不是与测试用例总数成正比。

.. note::

   ``--coverage-per-test`` 需要 ``lcov`` 覆盖率工具，因为矩阵依赖 lcov 的逐测试 ``TN`` 跟踪文件记录；``gcovr`` 没有等价功能。它同时隐含 ``--coverage``。

可视化矩阵
----------------------

``test_matrix.json`` 可以通过独立的 :zephyr_file:`scripts/gen_test_matrix_dashboard.py` 脚本转换为自包含的交互式 HTML 仪表盘（该脚本不依赖 Twister，可以对任何之前生成的矩阵运行）：

.. code-block:: console

   $ scripts/gen_test_matrix_dashboard.py -i twister-out/coverage/test_matrix.json

这会生成 ``twister-out/coverage/test_matrix.html``，其中逐测试列出其覆盖的文件数和行数，以及它*唯一*覆盖了多少行（没有其他测试触及的行，有助于发现冗余测试或关键测试），并允许你深入查看某个测试覆盖的文件，或查询哪些测试覆盖了给定的文件和行。

.. _gcovr_symlinks:
   https://github.com/gcovr/gcovr/blob/main/doc/source/guide/filters.rst#filters-for-symlinks

.. _gcov:
   https://gcc.gnu.org/onlinedocs/gcc/Gcov.html

使用不同的工具链
==========================

Twister 会查看环境变量 ``ZEPHYR_TOOLCHAIN_VARIANT``，以确定默认使用哪个 gcov 工具。下表列出了 Twister ``--gcov-tool`` 参数的默认值：

+-----------+-----------------------+
| 工具链    | ``--gcov-tool`` 取值  |
+-----------+-----------------------+
| host      | ``gcov``              |
+-----------+-----------------------+
| llvm      | ``llvm-cov gcov``     |
+-----------+-----------------------+
| zephyr    | ``gcov``              |
+-----------+-----------------------+
