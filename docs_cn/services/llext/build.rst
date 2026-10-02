Building
extensions
###################

LLEXT 子系统允许创建可以加载到正在运行的 Zephyr 应用中的 extensions。在构建这些 extensions 时，能够访问主 Zephyr 应用使用的 headers 和编译器标志通常非常有用。

实现这一点的最简单途径是将 extension 作为 Zephyr 应用的一部分进行构建，使用 `native Zephyr CMake features <llext_build_native_>`_。这将产生一个单一的构建，同时提供主 Zephyr 应用和 extension(s)，它们都将自动使用相同的参数进行构建。

在某些情况下，涉及完整的 Zephyr 构建系统可能不可行或不方便；也许 extension 使用不同的编译器套件构建，或作为完全不同项目的一部分。在这种情况下，extension 开发者需要导出主 Zephyr 应用使用的 headers 和编译器标志。这可以使用 `LLEXT Extension Development Kit <llext_build_edk_>`_ 完成。

.. _llext_build_native:

Use
Zephyr
CMake
features
*******************************

Zephyr 构建系统提供了一组可用于将 extensions 作为 Zephyr 应用一部分进行构建的功能。这是构建 extensions 最简单的方式，因为它只需要对应用构建系统进行最少的添加。

Building
the
extension
----------------------

一个 extension 可以通过在 app 的 ``CMakeLists.txt`` 中调用 :cmake:command:`add_llext_target` 函数来定义，提供 target 名称、输出和源文件。用法与标准的 :cmake:command:`add_custom_target <command:add_custom_target>` CMake 函数类似：

.. code-block:: cmake

   add_llext_target(
       <target_name>
       OUTPUT <ext_file.llext>
       SOURCES <src1> [<src2>...]
   )

其中：

- ``<target_name>`` 是最终 CMake target 的名称，它将产生 LLEXT 二进制文件；
- ``<ext_file.llext>`` 是输出文件的名称，将包含打包后的 extension；
- ``<src1> [<src2>...]`` 是将被编译以创建 extension 的源文件列表。

extension 构建过程的具体步骤取决于当前选中的 :ref:`ELF object format <llext_kconfig_type>`。

``<target_name>`` 的以下自定义属性被定义，并可以使用 ``get_target_property()`` CMake 函数获取：

``lib_target``

    源编译和/或链接步骤的 target 名称。

``lib_output``

    编译和/或链接步骤产生的二进制文件。

``pkg_input``

     用作打包步骤输入的文件。

``pkg_output``

    最终的 extension 文件名称。

Tweaking
the
build
process
--------------------------

以下 CMake 函数可用于在 extension 构建过程中对构建系统行为进行精细修改。下面的每个函数都以 LLEXT target 名称作为其第一个参数；除此之外，它在功能上等同于常见的 Zephyr ``target_*`` 版本。

* :cmake:command:`llext_compile_definitions`
* :cmake:command:`llext_compile_features`
* :cmake:command:`llext_compile_options`
* :cmake:command:`llext_include_directories`
* :cmake:command:`llext_link_options`

Custom
build
steps
------------------

``add_llext_command`` CMake 函数可用于添加将在 extension 构建过程中执行的自定义构建步骤。该命令将在指定的构建步骤处运行，并且可以引用 target 的属性以获取构建相关细节。

函数签名如下：

.. code-block:: cmake

   add_llext_command(
       TARGET <target_name>
       [PRE_BUILD | POST_BUILD | POST_PKG]
       COMMAND <command> [args...]
   )

不同的构建步骤如下：

``PRE_BUILD``

    在 extension 代码被链接之前（如果架构使用动态库）。此步骤可以访问 ``lib_target`` 及其属性。

``POST_BUILD``

    在 extension 代码构建之后，但在将其打包到 ``.llext`` 文件之前。此步骤预期通过读取 :file:`lib_output` 的内容来创建 :file:`pkg_input` 文件。

``POST_PKG``

    在 extension 输出文件创建之后。该命令可以操作最终的 llext 文件 :file:`pkg_output`。

``COMMAND`` 之后的所有内容都将原样传递给 ``add_custom_command()``（包括多个命令和其他选项）。

.. _llext_build_edk:

LLEXT
Extension
Development
Kit
(EDK)
*************************************

当作为独立项目、在主要 Zephyr 构建系统之外构建 extensions 时，能够访问与主 Zephyr 应用使用的同一套生成的 headers 和编译器标志非常重要，因为它们直接影响 Zephyr headers 的解析方式以及 extension 的整体编译方式。

这可以通过要求 Zephyr 从主 Zephyr 应用的构建产物生成一个 Extension Development Kit（EDK）来实现，运行以下使用 ``llext-edk`` target 的命令：

.. code-block:: shell

    west build -t llext-edk

生成的 EDK 可以在构建目录的 ``zephyr`` 目录下找到。它是一个 tarball，包含构建 extensions 所需的 headers 和编译标志。extension 开发者随后可以在其构建系统中包含这些 headers 并使用这些编译标志来构建 extension。

EDK
definition
files
--------------------

EDK 包含几个便捷文件，它们定义了一组变量，包含项目所需的编译标志，以及启用时的其他构建相关信息。当前信息以以下格式导出：

- ``Makefile.cflags``，用于基于 Makefile 的项目；
- ``cmake.cflags``，用于基于 CMake 的项目。

headers 和标志的路径以 EDK 根目录作为前缀。对于 CMake 项目，这会自动从 ``CMAKE_CURRENT_LIST_DIR`` 获取；其他格式引用一个 ``LLEXT_EDK_INSTALL_DIR`` 变量，用户必须在包含生成的文件之前将其设置为 EDK 安装的路径。

.. note::
   变量名中的 ``LLEXT_EDK`` 前缀可以通过 :kconfig:option:`CONFIG_LLEXT_EDK_NAME` 选项更改。

Compile
flags
-------------

构建 extension 所需的完整标志列表由 ``LLEXT_CFLAGS`` 提供。还提供了更细粒度的标志集，可用于支持不同的使用场景，例如为单元测试构建 mocks：

``LLEXT_INCLUDE_CFLAGS``

        用于将包含非自动生成 headers 的目录添加到编译器 include 搜索路径的编译器标志。

``LLEXT_GENERATED_INCLUDE_CFLAGS``

        用于将包含自动生成 headers 的目录添加到编译器 include 搜索路径的编译器标志。

``LLEXT_ALL_INCLUDE_CFLAGS``

        用于将构建中使用的所有包含 headers 的目录添加到编译器 include 搜索路径的编译器标志。这是 ``LLEXT_INCLUDE_CFLAGS`` 和 ``LLEXT_GENERATED_INCLUDE_CFLAGS`` 的组合。

``LLEXT_GENERATED_IMACROS_CFLAGS``

        用于必须通过 ``-imacros`` 在构建中包含的自动生成 headers 的编译器标志。

``LLEXT_BASE_CFLAGS``

        控制目标 CPU 代码生成的其他编译器标志。上述列表中没有包含这些标志。

``LLEXT_CFLAGS``

        构建 extension 所需的所有标志。这是 ``LLEXT_ALL_INCLUDE_CFLAGS``、``LLEXT_GENERATED_IMACROS_CFLAGS`` 和 ``LLEXT_BASE_CFLAGS`` 的组合。

Target
information
------------------

EDK 包含标识当前 Zephyr 构建 target 的信息。当前定义了以下变量，镜像 Zephyr 构建系统中可用的信息：

``LLEXT_EDK_BOARD_NAME``
    Zephyr 构建中使用的板级名称。

``LLEXT_EDK_BOARD_QUALIFIERS``
    Zephyr 构建中使用的板级限定符（如果提供）。

``LLEXT_EDK_BOARD_REVISION``
    Zephyr 构建中使用的板级修订版本（如果提供）。

``LLEXT_EDK_BOARD_TARGET``
    Zephyr 构建中使用的完全限定的板级 target。

.. note::
   变量名中的 ``LLEXT_EDK`` 前缀可以通过 :kconfig:option:`CONFIG_LLEXT_EDK_NAME` 选项更改。

.. _llext_kconfig_edk:

LLEXT
EDK
Kconfig
options
-------------------------

LLEXT EDK 可以使用以下 Kconfig 选项进行配置：

:kconfig:option:`CONFIG_LLEXT_EDK_NAME`
    生成的 EDK tarball 的名称。这也用作 EDK 文件中定义的若干变量的前缀。

:kconfig:option:`CONFIG_LLEXT_EDK_USERSPACE_ONLY`
    如果设置，EDK 将包含不包含将 syscalls 路由到内核的代码的 headers。这在构建仅在用户模式下运行的 extensions 时很有用。

EDK
Sample
----------

关于如何使用 LLEXT EDK 的示例，请参见 :zephyr:code-sample:`llext-edk`。
