.. _codechecker:

CodeChecker 支持
###################

`CodeChecker <https://codechecker.readthedocs.io/>`__ 是一个静态分析基础设施。它执行构建系统上可用的分析工具，如 `Clang-Tidy <https://clang.llvm.org/extra/clang-tidy/>`__、`Clang Static Analyzer <https://clang-analyzer.llvm.org/>`__ 和 `Cppcheck <https://cppcheck.sourceforge.io/>`__。请参考各分析器的网站获取安装说明。

安装 CodeChecker
**********************

CodeChecker 本身是一个在 `pypi <https://pypi.org/project/codechecker/>`__ 上可用的 python 包。

.. code-block:: shell

    pip install codechecker

用 CodeChecker 构建
*************************

要运行 CodeChecker，:ref:`west build <west-building>` 应该用 ``-DZEPHYR_SCA_VARIANT=codechecker`` 参数调用，例如

.. code-block:: shell

    west build -b mimxrt1064_evk samples/basic/blinky -- -DZEPHYR_SCA_VARIANT=codechecker

配置 CodeChecker
***********************

CodeChecker 使用不同的命令步骤，每个都有各自的配置参数。下面的表格列出所有这些选项。

.. list-table::
   :header-rows: 1

   * - 参数
     - 描述
   * - ``CODECHECKER_ANALYZE_JOBS``
     - 分析中使用的线程数。（默认：<CPU 数量>）
   * - ``CODECHECKER_ANALYZE_OPTS``
     - 直接传递给 ``analyze`` 命令的参数。（例如 ``--timeout;360``）
   * - ``CODECHECKER_CLEANUP``
     - 在解析/存储后执行清理。这将删除所有 ``plist`` 文件。
   * - ``CODECHECKER_CONFIG_FILE``
     - 一个 JSON 或 YAML 文件，包含传递给所有命令的配置选项。
   * - ``CODECHECKER_EXPORT``
     - 报告类型的逗号分隔列表。允许的类型是：``html,json,codeclimate,gerrit,baseline``。
   * - ``CODECHECKER_NAME``
     - CodeChecker 运行元数据名称。（默认：``zephyr``）
   * - ``CODECHECKER_PARSE_EXIT_STATUS``
     - 默认情况下，CodeChecker 识别的问题不会导致构建失败，设置此选项以在分析期间失败。
   * - ``CODECHECKER_PARSE_OPTS``
     - 直接传递给 ``parse`` 命令的参数。（例如 ``--verbose;debug``）
   * - ``CODECHECKER_PARSE_SKIP``
     - 跳过分析解析，如果你只想存储结果则有用。
   * - ``CODECHECKER_STORE``
     - 在分析后运行 ``store`` 命令。
   * - ``CODECHECKER_STORE_OPTS``
     - 直接传递给 ``store`` 命令的参数。隐含 ``CODECHECKER_STORE``。（例如 ``--url;localhost:8001/Default``）
   * - ``CODECHECKER_STORE_TAG``
     - 将标识符 ``--tag`` 传递给 ``store`` 命令。
   * - ``CODECHECKER_TRIM_PATH_PREFIX``
     - 从分析结果中删除定义的路径，例如 ``/home/user/zephyrproject``。``west topdir`` 的值默认被添加。

这些参数可以在命令行上传递，或作为环境变量设置。

用 CodeChecker 运行 twister
********************************

当作为 ``twister`` 的一部分运行 CodeChecker 时，一些默认选项设置如下：

.. list-table::
   :header-rows: 1

   * - 参数
     - 值
   * - ``CODECHECKER_ANALYZE_JOBS``
     - ``1``
   * - ``CODECHECKER_NAME``
     - ``<board target>:<testsuite name>``
   * - ``CODECHECKER_STORE_TAG``
     - 应用源目录中 ``git describe`` 的值。

要覆盖这些值，设置环境变量或作为额外参数传递。
