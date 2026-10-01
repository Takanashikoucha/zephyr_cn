.. _toolchain_gnuarmemb:

GNU Arm 嵌入式
################

#. 下载并安装适用于你的操作系统的 `GNU Arm 嵌入式`_ 构建版本，
   并在文件系统中解压。

   .. note::

      在 Windows 上，本指南假设你安装到目录
      :file:`C:\\gnu_arm_embedded`。
      你也可以选择 ARM GCC 安装程序使用的默认安装路径，
      在这种情况下你需要相应调整下面指南中的路径。

   .. warning::

      在 macOS Catalina 或更高版本上，
      你可能需要 :ref:`更改安全策略 <mac-gatekeeper>`
      以让工具链能从终端运行。

#. :ref:`设置以下环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``gnuarmemb``。
   - 将 :envvar:`GNUARMEMB_TOOLCHAIN_PATH` 设置为工具链安装目录。

#. 要检查你是否在当前环境中正确设置了这些变量，
   参考以下示例 shell 会话
   （:envvar:`GNUARMEMB_TOOLCHAIN_PATH` 的值在你的系统上可能不同）：

   .. code-block:: console

      # Linux, macOS:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      gnuarmemb
      $ echo $GNUARMEMB_TOOLCHAIN_PATH
      /home/you/Downloads/gnu_arm_embedded

      # Windows:
      > echo %ZEPHYR_TOOLCHAIN_VARIANT%
      gnuarmemb
      > echo %GNUARMEMB_TOOLCHAIN_PATH%
      C:\gnu_arm_embedded

   .. warning::

      在 macOS 上，如果你在建议的步骤中遇到问题，
      brew 上有一个非官方包可能对你有帮助。
      运行 ``brew install gcc-arm-embedded`` 并配置变量

      - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``gnuarmemb``。
      - 将 :envvar:`GNUARMEMB_TOOLCHAIN_PATH` 设置为 brew 安装目录（类似 ``/usr/local``）

.. _GNU Arm 嵌入式: https://developer.arm.com/open-source/gnu-toolchain/gnu-rm
