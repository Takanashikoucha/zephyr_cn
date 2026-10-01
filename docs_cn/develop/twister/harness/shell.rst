.. _twister_shell_harness:

Shell
#####

shell 测试框架（harness）用于执行 shell 命令并解析其输出，
它利用 pytest 框架以及 Twister 的 pytest 测试框架。

以下选项适用于 shell 测试框架：

shell_commands: <命令及其期望输出的配对列表>（默认为空）
    指定要执行的 shell 命令及其期望输出。例如：

    .. code-block:: yaml

        harness_config:
          shell_commands:
          - command: "kernel cycles"
            expected: "cycles: .* hw cycles"
          - command: "kernel version"
            expected: "Zephyr version .*"
          - command: "kernel sleep 100"


    若未提供期望输出，则命令会被执行，其输出会被记录。

shell_commands_file: <字符串>（默认为空）
    指定一个包含测试中要使用的测试参数的文件（file）。
    该文件应包含命令及其期望输出的列表。例如：

    .. code-block:: yaml

      - command: "mpu mtest 1"
        expected: "The value is: 0x.*"
      - command: "mpu mtest 2"
        expected: "The value is: 0x.*"


    若未指定文件（file），shell 测试框架将使用测试目录中的默认文件
    ``test_shell.yml``。
    ``shell_commands`` 优先于 ``shell_commands_file``。
