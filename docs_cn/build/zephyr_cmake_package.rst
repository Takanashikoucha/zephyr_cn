.. _cmake_pkg:

Zephyr CMake 包
####################

Zephyr `CMake 包`_ 是创建基于 Zephyr 的应用的便捷方式。

.. note::
   :ref:`zephyr-app-types` 章节介绍本页使用的应用类型。

Zephyr CMake 包确保 CMake 可以自动选择用于构建应用的 Zephyr 安装，
无论它是 :ref:`Zephyr 仓库应用 <zephyr-repo-app>`、
:ref:`Zephyr 工作区应用 <zephyr-workspace-app>`，还是
:ref:`Zephyr 独立应用 <zephyr-freestanding-app>`。

开发基于 Zephyr 的应用时，开发者只需在应用 :file:`CMakeLists.txt` 文件
开头写 ``find_package(Zephyr)``。

要使用 Zephyr CMake 包，首先必须将其导出到 `CMake 用户包注册表`_。
这意味着在 CMake 用户包注册表中创建对当前 Zephyr 安装的引用。


.. tabs::

   .. group-tab:: Ubuntu

      在 Linux 上，CMake 用户包注册表位于：

      ``~/.cmake/packages/Zephyr``

   .. group-tab:: macOS

      在 macOS 上，CMake 用户包注册表位于：

      ``~/.cmake/packages/Zephyr``

   .. group-tab:: Windows

      在 Windows 上，CMake 用户包注册表位于：

      ``HKEY_CURRENT_USER\Software\Kitware\CMake\Packages\Zephyr``


Zephyr CMake 包允许 CMake 自动查找 Zephyr base。
必须导出一个或多个 Zephyr 安装。
导出多个 Zephyr 安装在开发或测试 Zephyr 独立应用、
带厂商 fork 的 Zephyr 工作区应用等时可能有用。


Zephyr CMake 包导出（west）
**********************************

使用 :ref:`west <get_the_code>` 安装 Zephyr 时，
推荐使用 ``west zephyr-export`` 导出 Zephyr。

.. _zephyr_cmake_package_export:

Zephyr CMake 包导出（无 west）
******************************************

Zephyr CMake 包用以下命令导出到 CMake 用户包注册表：

.. code-block:: bash

   cmake -P <PATH-TO-ZEPHYR>/share/zephyr-package/cmake/zephyr_export.cmake

这将把当前 Zephyr 导出到 CMake 用户包注册表。

.. _zephyr_cmake_package_zephyr_base:

Zephyr Base 环境设置
*******************************

Zephyr CMake 包搜索功能允许使用环境变量显式指定 Zephyr base。

要做到这，使用以下 ``find_package()`` 语法：

.. code-block:: cmake

   find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

这个语法指示 CMake 首先使用 Zephyr base 环境设置
:envvar:`ZEPHYR_BASE` 搜索 Zephyr，然后使用正常的搜索路径。

.. _zephyr_cmake_search_order:

Zephyr CMake 包搜索顺序
*********************************

当 Zephyr base 环境设置不用于搜索时，
将使用匹配以下标准的 Zephyr 安装：

* Zephyr 仓库应用将使用其位于的 Zephyr。
  例如：

  .. code-block:: none

        <projects>/zephyr-workspace/zephyr
        └── samples
            └── hello_world

  在这个示例中，``hello_world`` 将使用 ``<projects>/zephyr-workspace/zephyr``。


* Zephyr 工作区应用将使用共享相同工作区的 Zephyr。
  例如：

  .. code-block:: none

     <projects>/zephyr-workspace
     ├── zephyr
     ├── ...
     └── my_applications
          └── my_first_app

  在这个示例中，``my_first_app`` 将使用 ``<projects>/zephyr-workspace/zephyr``，
  因为这个 Zephyr 与 Zephyr 工作区应用位于相同的工作区中。

.. note::
   如果工作区使用 ``west`` 安装，Zephyr 工作区的根等同于 ``west topdir``

* Zephyr 独立应用将使用注册在 CMake 用户包注册表中的 Zephyr。
  例如：

  .. code-block:: none

     <projects>/zephyr-workspace-1
     └── zephyr                       (Not exported to CMake)

     <projects>/zephyr-workspace-2
     └── zephyr                       (Exported to CMake)

     <home>/app
     ├── CMakeLists.txt
     ├── prj.conf
     └── src
         └── main.c

  在这个示例中，只有 ``<projects>/zephyr-workspace-2/zephyr``
  被导出到 CMake 包注册表，因此这个 Zephyr 将被 Zephyr 独立应用
  ``<home>/app`` 使用。

  如果用户想测试应用与 ``<projects>/zephyr-workspace-1/zephyr`` 一起工作，
  可以通过使用 Zephyr Base 环境设置做到，
  即在运行 CMake 之前设置 ``ZEPHYR_BASE=<projects>/zephyr-workspace-1/zephyr``。

  .. note::

     第一次 CMake 调用时选择的 Zephyr 包将用于所有后续构建。
     要更改 Zephyr 包，例如要使用 Zephyr base 环境设置测试应用，
     那么必须先做一次全新构建（见 :ref:`application_rebuild`）。

Zephyr CMake 包版本
****************************

编写应用时，可以指定构建应用必须使用的 Zephyr 版本号 ``x.y.z``。

指定版本对 Zephyr 独立应用特别有用，因为它确保应用用最小 Zephyr 版本构建。

它还有助于 CMake 在系统中有多个 Zephyr 安装时选择用于构建的正确 Zephyr。

例如：

  .. code-block:: cmake

     find_package(Zephyr 2.2.0)
     project(app)

将要求 ``app`` 用最小 Zephyr 2.2.0 构建。
CMake 将搜索所有导出的候选项以找到匹配此版本标准的 Zephyr 安装。

因此可以有多个 Zephyr 安装，并让 CMake 根据提供的版本号
自动在它们之间选择，详见 `CMake 包版本`_。

例如：

.. code-block:: none

   <projects>/zephyr-workspace-2.a
   └── zephyr                       (Exported to CMake)

   <projects>/zephyr-workspace-2.b
   └── zephyr                       (Exported to CMake)

   <home>/app
   ├── CMakeLists.txt
   ├── prj.conf
   └── src
       └── main.c

在这种情况下，有两个已发布版本的 Zephyr 安装在各自的工作区中。
工作区 2.a 和 2.b，对应 Zephyr 版本。

要确保 ``app`` 用最小版本 ``2.a`` 构建，
可以使用以下 ``find_package`` 语法：

.. code-block:: cmake

   find_package(Zephyr 2.a)
   project(app)


注意 ``2.a`` 和 ``2.b`` 都满足此要求。

CMake 还支持关键字 ``EXACT``，以确保使用精确版本，如果需要的话。
在这种情况下，应用 CMakeLists.txt 可以写成：

.. code-block:: cmake

   find_package(Zephyr 2.a EXACT)
   project(app)

如果找不到满足所需版本的 Zephyr，例如应用指定

.. code-block:: cmake

   find_package(Zephyr 2.z)
   project(app)

那么将打印类似下面的错误：

.. code-block:: none

   Could not find a configuration file for package "Zephyr" that is compatible
   with requested version "2.z".

   The following configuration files were considered but not accepted:

     <projects>/zephyr-workspace-2.a/zephyr/share/zephyr-package/cmake/ZephyrConfig.cmake, version: 2.a.0
     <projects>/zephyr-workspace-2.b/zephyr/share/zephyr-package/cmake/ZephyrConfig.cmake, version: 2.b.0


.. note:: 对 Zephyr 仓库应用和 Zephyr 工作区应用指定版本号也可能有益。
          在这些情况下指定版本确保应用仅在 Zephyr 仓库或工作区匹配时
          才会构建。这在只有工作区的一部分被更新时避免意外构建
          可能有用。


多个 Zephyr 安装（Zephyr 工作区）
************************************************

测试新的 Zephyr 版本，同时保持工作区中现有 Zephyr 不变，
有时是有益的。

或者在同一工作区中同时拥有上游 Zephyr、厂商特定 Zephyr 和自定义 Zephyr。

例如：

.. code-block:: none

   <projects>/zephyr-workspace
   ├── zephyr
   ├── zephyr-vendor
   ├── zephyr-custom
   ├── ...
   └── my_applications
        └── my_first_app


在这种设置中，``find_package(Zephyr)`` 选择使用哪个 Zephyr
有以下优先级顺序：

* 项目名称：``zephyr``
* 当 Zephyr 项目按字典序排序时的第一个项目，在这种情况下。

  * ``zephyr-custom``
  * ``zephyr-vendor``

这意味着 ``my_first_app`` 将使用 ``<projects>/zephyr-workspace/zephyr``。

可以在应用中指定 Zephyr 偏好列表。

Zephyr 偏好列表可以指定为：

.. code-block:: cmake

   set(ZEPHYR_PREFER "zephyr-custom" "zephyr-vendor")
   find_package(Zephyr)

   project(my_first_app)


``ZEPHYR_PREFER`` 是一个列表，允许多个 Zephyr。
如果列表中指定了 Zephyr 但在系统中未找到，它将被简单忽略，
``find_package(Zephyr)`` 将继续到下一个候选项。


这允许临时创建新的 Zephyr 发布进行测试，而不触及当前 Zephyr。
测试完成后，``zephyr-test`` 文件夹可以简单删除。
这样的 CMakeLists.txt 可以写成：

.. code-block:: cmake

   set(ZEPHYR_PREFER "zephyr-test")
   find_package(Zephyr)

   project(my_first_app)

.. _cmake_build_config_package:

Zephyr 构建配置 CMake 包
*****************************************

有两个 Zephyr 构建配置包，以更通用的方式
提供对 Zephyr 中构建设置的控制。这些包是：

* **ZephyrBuildConfiguration**：适用于工作区中所有 Zephyr 应用
* **ZephyrAppConfiguration**：仅适用于你当前正在构建的应用

它们类似于每用户 :file:`.zephyrrc` 文件，可用于设置 :ref:`env_vars`，
但它们设置的是 CMake 变量。它们还允许你通过项目仓库
在所有用户之间自动共享构建设置。它们还允许更高级的
用例，如加载额外的 CMake 样板代码。

Zephyr 构建配置 CMake 包将在 Zephyr 样板代码中加载，
在初始属性和 ``ZEPHYR_BASE`` 已定义之后，但在 CMake 代码执行之前。
ZephyrBuildConfiguration 先包含，ZephyrAppConfiguration 随后。
这意味着应用特定的包如果需要可以覆盖工作区设置。
这允许 Zephyr 构建配置 CMake 包设置或扩展属性，如：
``DTS_ROOT``、``BOARD_ROOT``、``TOOLCHAIN_ROOT`` / 其他工具链设置、
固定覆盖，以及任何可以控制的其他属性。
它还允许包含额外的样板代码。

要提供 ZephyrBuildConfiguration 或 ZephyrAppConfiguration，
分别创建 :file:`ZephyrBuildConfig.cmake` 和/或
:file:`ZephyrAppConfig.cmake` 并将它们放在适当位置。
CMake ``find_package`` 机制将按以下步骤搜索这些文件。
其他默认 CMake 包搜索路径和提示被禁用，
这些包没有实现版本检查。这也意味着这些包不能
安装在 CMake 包注册表中。搜索步骤是：

1. 如果分别设置了 ``ZephyrBuildConfiguration_ROOT`` 或
   ``ZephyrAppConfiguration_ROOT``，在此前缀路径内搜索。
   如果找到匹配文件，执行此文件。如果未找到匹配文件，
   转到步骤 2。
2. 分别搜索 ``${ZEPHYR_BASE}/../*`` 或 ``${APPLICATION_SOURCE_DIR}``。
   如果找到匹配文件，执行此文件。如果未找到匹配文件，
   中止搜索。

推荐将文件放在步骤 2 的默认路径中，但用
``<PackageName>_ROOT`` 变量你有灵活性将它们放在任何地方。
这对独立应用特别必要，对于独立应用，
ZephyrBuildConfiguration 的默认路径通常不起作用。
在这种情况下，``<PackageName>_ROOT`` 变量
可以在 CMake 命令行上设置，**在** ``find_package(Zephyr ...)`` **之前**，
作为环境变量或从用 ``-C`` 命令行选项的 CMake 缓存初始化文件。

.. note:: ``<PackageName>_ROOT`` 变量以及默认路径只是搜索路径的前缀。
   这些前缀与额外的路径后缀组合，一起形成实际搜索路径。
   任何遵循 `CMake 包搜索过程`_ 的组合都是有效的并将工作。

如果你想完全禁用对这些包的搜索，
可以用特殊的 CMake ``CMAKE_DISABLE_FIND_PACKAGE_<PackageName>`` 变量做到。
只需将 ``CMAKE_DISABLE_FIND_PACKAGE_ZephyrBuildConfiguration`` 或
``CMAKE_DISABLE_FIND_PACKAGE_ZephyrAppConfiguration`` 设置为 ``TRUE``
即可禁用包。

示例文件夹结构可以像这样：

.. code-block:: none

   <projects>/zephyr-workspace
   ├── zephyr
   ├── ...
   ├── manifest repo (can be named anything)
   │    └── cmake/ZephyrBuildConfig.cmake
   ├── ...
   └── zephyr application
        └── share/zephyrapp-package/cmake/ZephyrAppConfig.cmake

示例 :file:`ZephyrBuildConfig.cmake` 可以在下面看到。

.. code-block:: cmake

   # ZephyrBuildConfig.cmake sample code

   # To ensure final path is absolute and does not contain ../.. in variable.
   get_filename_component(APPLICATION_PROJECT_DIR
                          ${CMAKE_CURRENT_LIST_DIR}/../../..
                          ABSOLUTE
   )

   # Add this project to list of board roots
   list(APPEND BOARD_ROOT ${APPLICATION_PROJECT_DIR})

   # Default to GNU Arm Embedded toolchain if no toolchain is set
   if(NOT ENV{ZEPHYR_TOOLCHAIN_VARIANT})
       set(ZEPHYR_TOOLCHAIN_VARIANT gnuarmemb)
       find_program(GNU_ARM_GCC arm-none-eabi-gcc)
       if(NOT ${GNU_ARM_GCC} STREQUAL GNU_ARM_GCC-NOTFOUND)
           # The toolchain root is located above the path to the compiler.
           get_filename_component(GNUARMEMB_TOOLCHAIN_PATH ${GNU_ARM_GCC}/../.. ABSOLUTE)
       endif()
   endif()

Zephyr CMake 包源代码
********************************

:zephyr_file:`share/zephyr-package/cmake` 中的
Zephyr CMake 包源代码包含 CMake 配置包，
它被 CMake ``find_package`` 函数使用。

它还包含将 Zephyr 导出为 CMake 配置包的代码。

以下是此目录中文件的概览：

:file:`ZephyrConfigVersion.cmake`
    Zephyr 包版本文件。此文件由 CMake 调用以确定
    此安装是否满足用户调用 ``find_package(Zephyr ...)``
    时指定的要求。它还负责检测 Zephyr 仓库或
    仅工作区安装。

:file:`ZephyrConfig.cmake`
    Zephyr 包文件。此文件由 CMake 调用以找到满足
    用户调用 ``find_package(Zephyr ...)`` 时指定要求的包。
    此文件负责源样板代码。

:file:`zephyr_package_search.cmake`
    用于检测 Zephyr 仓库和工作区候选项的通用文件。
    用于 ``ZephyrConfigVersion.cmake`` 和 ``ZephyrConfig.cmake`` 的通用代码。

:file:`zephyr_export.cmake`
    见 :ref:`zephyr_cmake_package_export`。

.. _CMake 包: https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html
.. _CMake 用户包注册表: https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html#user-package-registry
.. _CMake 包版本: https://cmake.org/cmake/help/latest/command/find_package.html#version-selection
.. _CMake 包搜索过程: https://cmake.org/cmake/help/latest/command/find_package.html#search-procedure
