.. _twister_script_harness:

Script
######

``script`` 测试框架（harness）将 shell 脚本作为测试用例执行。它从 ``tests_scripts`` 测试框架配置项解析脚本，
将每个脚本作为子进程运行，并根据脚本退出码报告单独的通过/失败结果。

``script`` 测试框架同时作为 :ref:`bsim <twister_bsim_harness>`、
:ref:`pytest <twister_pytest_harness>` 和 :ref:`ctest <twister_ctest_harness>` 测试框架的基类，
提供共享的子进程执行、输出流和日志处理功能。

tests_scripts: <脚本路径列表>（默认 tests_scripts）
    指定测试场景运行时需执行的 shell 脚本路径列表（相对于测试源目录）。
    每个条目可以是单个文件的路径、一个目录或一个通配符（glob）模式。
    指定目录时，收集该目录中所有 ``.sh`` 文件（包括其子目录，排除以 ``_`` 开头的文件）。
    默认为 ``tests_scripts`` 目录。

    .. code-block:: yaml

        harness: script
        harness_config:
          tests_scripts:
            - tests_scripts/test_a.sh
            - ../../test/test_b.sh
            - $ENV_VAR/tests_scripts

传递给 Twister 的 ``--`` 之后的任何额外命令行参数，都会作为额外的位置参数转发给每个脚本。
