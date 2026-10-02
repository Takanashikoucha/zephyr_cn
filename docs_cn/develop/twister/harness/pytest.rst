.. _twister_pytest_harness:

Pytest
######

:ref:`pytest 测试框架 <integration_with_pytest>` 用于在 Zephyr 测试中执行 pytest 测试套件。以下选项适用于 pytest 测试框架：

.. _pytest_root:

pytest_root: <pytest 测试路径列表>（默认为 pytest）
    指定测试场景开始运行时需要执行的 pytest 目录、文件或子测试列表。默认 pytest 目录为 ``pytest``。pytest 运行完成后，Twister 将根据 pytest 报告检查测试场景是通过还是失败。环境变量和 Zephyr 模块目录变量会被展开（参见 :ref:`twister_module_dir_vars`）。例如，以下展示了一个有效的 pytest 根列表：

    .. code-block:: yaml

        harness_config:
          pytest_root:
            - "pytest/test_shell_help.py"
            - "../shell/pytest/test_shell.py"
            - "/tmp/test_shell.py"
            - "~/tmp/test_shell.py"
            - "$ZEPHYR_BASE/samples/subsys/testsuite/pytest/shell/pytest/test_shell.py"
            - "$ZEPHYR_HAL_NORDIC_MODULE_DIR/tests/pytest/test_hal.py"  # path inside a module
            - "pytest/test_shell_help.py::test_shell2_sample"  # select pytest subtest
            - "pytest/test_shell_help.py::test_shell2_sample[param_a]"  # select pytest parametrized subtest

.. _pytest_args:

pytest_args: <参数列表>（默认为空）
    指定传递给 ``pytest`` 的额外参数列表，例如：
    ``pytest_args: ['-k=test_method', '--log-level=DEBUG']``。注意
    ``--pytest-args`` 可以多次传递，以向 pytest 传递多个参数。

.. _pytest_dut_scope:

pytest_dut_scope: <function|class|module|package|session>（默认为 function）
    ``dut`` 和 ``shell`` pytest 固件共享的作用域。
    如果作用域设为 ``function``，Python 脚本中每个测试用例都会启动 DUT。
    对于 ``session`` 作用域，DUT 仅启动一次。


  以下是带有 pytest harness_config 选项的示例 YAML 文件。
  如果未指定 pytest_root，将使用默认 pytest_root 名称 "pytest"。
  请参见 samples/subsys/testsuite/pytest/ 中的示例。

  .. code-block:: yaml

      common:
        harness: pytest
      tests:
        pytest.example.directories:
          harness_config:
            pytest_root:
              - pytest_dir1
              - $ENV_VAR/samples/test/pytest_dir2
        pytest.example.files_and_subtests:
          harness_config:
            pytest_root:
              - pytest/test_file_1.py
              - test_file_2.py::test_A
              - test_file_2.py::test_B[param_a]

.. _required_devices:

required_devices: <所需设备条目列表>（默认为空）
    指定多 DUT 测试场景所需的额外 DUT。
    每个条目配置一个额外设备，与主 DUT 一起保留和烧录。
    空条目 ``{}`` 保留与主 DUT 相同平台和应用的第二个设备。

    多 DUT 测试支持硬件设备测试和
    ``native_sim`` 仿真。不支持
    QEMU。对于仿真目标，Twister
    自动创建所需的占位 DUT 条目，
    无需硬件映射。对于硬件测试，提供硬件映射
    文件（``--hardware-map``），每个所需设备对应一个匹配条目。
    更多细节参见
    :ref:`twister_multi_duts_testing` 章节。

    每个条目支持以下可选字段：


    platform: <字符串>（可选，默认为当前测试的平台）
        此所需设备使用的平台。如果未指定，
        使用与主 DUT 相同的平台。

    application: <字符串>（可选，默认为当前测试应用）
        在此所需设备上烧录的测试应用 ID。指定时，
        Twister 单独构建该应用，并在烧录前将其构建目录
        分配给保留的 DUT。
        如果未指定，使用与主 DUT 相同的应用。

        使用与 :ref:`required_applications <required_applications>` 相同的机制。

    path: <字符串>（可选）
        Twister 应搜索 ``application`` 中指定的应用的目录路径。
        可以是绝对路径，也可以是相对于包含测试 YAML 文件的目录的路径。
        环境变量和 Zephyr 模块目录变量会被展开
        （参见 :ref:`twister_module_dir_vars`）。如果未指定，
        Twister 在引用测试的 YAML 文件所在目录中搜索。

    fixture: <固件名称列表>（可选，默认为空）
        保留设备上必须存在的固件名称列表。
        详情参见 :ref:`Fixtures <twister_fixtures>`。

        固件支持使用 ``name:param`` 语法的可选参数后缀
        （例如 ``io_adapter:channel_a``）。当主 DUT 有带参数的固件时，
        Twister 使用该参数值来匹配所需设备——
        仅考虑对该固件名称携带**相同参数**的设备。
        这确保物理连接的 DUT 对
        （例如两块用同一固件参数在硬件映射中注册的接线板）
        总是被一起保留，且不与无关板卡混合。

        配对设置的示例硬件映射条目：

        .. code-block:: yaml

            - id: "01"
              platform: nrf52840dk/nrf52840
              serial: /dev/ttyACM0
              fixtures:
                - io_adapter:channel_a
            - id: "02"
              platform: nrf52840dk/nrf52840
              serial: /dev/ttyACM1
              fixtures:
                - io_adapter:channel_a

        主 DUT 和所需设备上均为 ``fixture: [io_adapter]`` 时，
        Twister 仅选择共享相同 ``channel_a`` 参数的板卡，
        保证选中物理配对的板卡。


    带多个所需设备的示例配置：

    .. code-block:: yaml

        tests:
          # Two DUTs, same platform and application
          multidut.basic:
            harness_config:
              required_devices:
                - {}
          # Second DUT fixed to a specific platform
          multidut.fixed_platform:
            harness_config:
              required_devices:
                - platform: nrf52840dk/nrf52840
          # Second DUT flashed with a different application
          multidut.other_app:
            harness_config:
              required_devices:
                - application: multidut.basic
