.. _custom_cmake_toolchains:

自定义 CMake 工具链
#######################

要使用在外部 CMake 文件中定义的自定义工具链，:ref:`设置以下环境变量 <env_vars>`：

- 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为你的工具链名称
- 将 ``TOOLCHAIN_ROOT`` 设置为包含你的工具链 CMake 配置文件的目录路径。

Zephyr 随后会包含位于 :file:`TOOLCHAIN_ROOT` 目录中的工具链 cmake 文件：

- :file:`cmake/toolchain/<toolchain name>/generic.cmake`：配置工具链用于"通用"用途，
  主要指对生成的 :ref:`设备树` 文件运行 C 预处理器。
- :file:`cmake/toolchain/<toolchain name>/target.cmake`：配置工具链用于"目标"用途，
  即构建 Zephyr 和你的应用程序源代码。

这里 <toolchain name> 与 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
中提供的名称相同。
参见 Zephyr 文件 :zephyr_file:`cmake/modules/FindHostTools.cmake` 和
:zephyr_file:`cmake/modules/FindTargetTools.cmake` 了解你的
:file:`generic.cmake` 和 :file:`target.cmake` 文件应包含哪些内容的更多细节。

你也可以在生成 Zephyr 应用的构建系统时，将 ``ZEPHYR_TOOLCHAIN_VARIANT`` 和
``TOOLCHAIN_ROOT`` 设置为 CMake 变量，如下所示：

.. code-block:: console

   west build ... -- -DZEPHYR_TOOLCHAIN_VARIANT=... -DTOOLCHAIN_ROOT=...

.. code-block:: console

   cmake -DZEPHYR_TOOLCHAIN_VARIANT=... -DTOOLCHAIN_ROOT=...

如果你这样做，``-C <initial-cache>`` `cmake 选项`_ 可能有用。如果你将
:makevar:`ZEPHYR_TOOLCHAIN_VARIANT`、:makevar:`TOOLCHAIN_ROOT` 和其他设置
保存在名为 :file:`my-toolchain.cmake` 的文件中，然后可以用
``cmake -C my-toolchain.cmake ...`` 调用 cmake 以节省输入。

Zephyr 包含 :file:`include/zephyr/toolchain.h`，它又会根据编译器标识符
（如 ``__llvm__`` 或 ``__GNUC__``）包含一个工具链特定的头文件。
一些自定义编译器将自己标识为它们所基于的编译器，例如 ``llvm``，
然后 :file:`toolchain/llvm.h` 会被包含。
但这个被包含的文件可能对自定义工具链并不正确。
为了解决这个问题，从而让 :file:`include/other.h` 被包含，
将 set(TOOLCHAIN_USE_CUSTOM 1) cmake 行添加到位于
:file:`<TOOLCHAIN_ROOT>/cmake/toolchain/<toolchain name>/` 下的
generic.cmake 和/或 target.cmake 文件。

当 :makevar:`TOOLCHAIN_USE_CUSTOM` 被设置时，:file:`other.h` 必须
在代码树之外可用，且必须包含自定义工具链的正确头文件。
:file:`other.h` 头文件的一个合适位置是 ``TOOLCHAIN_ROOT`` 指定目录下的
:file:`include/zephyr/toolchain` 目录。
要让工具链头文件被包含在 Zephyr 的构建中，
:makevar:`USERINCLUDE` 可以设置为指向包含目录，如下所示：

.. code-block:: console

   west build -- -DZEPHYR_TOOLCHAIN_VARIANT=... -DTOOLCHAIN_ROOT=... -DUSERINCLUDE=...

.. _cmake 选项:
   https://cmake.org/cmake/help/latest/manual/cmake.1.html#options
