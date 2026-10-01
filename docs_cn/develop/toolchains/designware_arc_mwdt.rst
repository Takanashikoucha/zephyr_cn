.. _toolchain_designware_arc_mwdt:

DesignWare ARC MetaWare 开发工具包（MWDT）
##################################################

#. 你需要在主机上安装 `ARC MWDT <https://www.synopsys.com/dw/ipdir.php?ds=sw_metaware>`__。

#. 你需要在主机上安装 :ref:`Zephyr SDK <toolchain_zephyr_sdk>`。

   .. note::
      Zephyr SDK 用作设备树编译器（DTC）、QEMU 等工具的来源。
      尽管 ARC MWDT 工具链用于 Zephyr RTOS 构建，但 GNU 预处理器和 GNU
      objcopy 可能用于设备树预处理和 ``.bin`` 文件生成等步骤。
      我们也将 Zephyr SDK 用作这些 ARC GNU 工具的来源。
      要设置 ARC GNU 工具链，请使用 SDK 安装包（完整版或精简版）
      而非手动安装单独的压缩包。
      它会安装并注册工具链和主机工具到系统中，
      让你避免构建 Zephyr 时的工具链相关问题。

#. :ref:`设置以下环境变量 <env_vars>`：

   - 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``arcmwdt``。
   - 将 :envvar:`ARCMWDT_TOOLCHAIN_PATH` 设置为工具链安装目录。
     MWDT 安装提供 :envvar:`METAWARE_ROOT`，
     所以只需将 :envvar:`ARCMWDT_TOOLCHAIN_PATH` 设置为
     ``$METAWARE_ROOT/../``（Linux）或 ``%METAWARE_ROOT%\..\``（Windows）。

   .. tip::
      如果你只在一台机器上安装了一个 ARC MWDT 工具链版本，
      你可以跳过设置 :envvar:`ARCMWDT_TOOLCHAIN_PATH`——它会被自动检测。

#. 要检查你是否在当前环境中正确设置了这些变量，
   参考以下示例 shell 会话
   （:envvar:`ARCMWDT_TOOLCHAIN_PATH` 的值在你的系统上可能不同）：

   .. code-block:: console

      # Linux:
      $ echo $ZEPHYR_TOOLCHAIN_VARIANT
      arcmwdt
      $ echo $ARCMWDT_TOOLCHAIN_PATH
      /home/you/ARC/MWDT_2023.03/

      # Windows:
      > echo %ZEPHYR_TOOLCHAIN_VARIANT%
      arcmwdt
      > echo %ARCMWDT_TOOLCHAIN_PATH%
      C:\ARC\MWDT_2023.03\
