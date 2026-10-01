:orphan:

.. _cmake-style:

CMake 风格指南
######################

这些指南的一个子集由 ``CMakeStyle`` 合规检查在 CI 中执行。你可以在本地使用 ``scripts/cmake/cmake_style.py`` 运行相同的检查（目录被递归搜索以查找 ``CMakeLists.txt`` 和 ``*.cmake`` 文件）：

.. code-block:: console

   pip install tree-sitter tree-sitter-cmake
   ./scripts/cmake/cmake_style.py path/to/CMakeLists.txt
   ./scripts/cmake/cmake_style.py drivers/

通用格式
******************

- **缩进**：使用 **2 个空格**进行缩进。避免使用制表符以确保不同环境之间的一致性。
- **行长度**：在可能的情况下将行长度限制为 **100 列**。
- **空行**：使用空行分隔 CMake 文件中逻辑上不同的部分。
- **开括号前不加空格**：不要在命令和开括号之间添加空格。使用 ``if(...)`` 而不是 ``if (...)``。

  .. code-block:: cmake

     # Good:
     if(ENABLE_TESTS)
       add_subdirectory(tests)
     endif()

     # Bad:
     if (ENABLE_TESTS)
       add_subdirectory(tests)
     endif()

命令和语法
*******************

- **小写命令**：始终使用**小写** CMake 命令（例如 ``add_executable``、``find_package``）。这提高可读性和一致性。

  .. code-block:: cmake

     # Good:
     add_library(my_lib STATIC src/my_lib.cpp)

     # Bad:
     ADD_LIBRARY(my_lib STATIC src/my_lib.cpp)

  由 CMake 模块定义的命令，以及扩展现有混合大小写命令的 Zephyr 或 sysbuild 扩展命令，是例外：它们遵循混合大小写 ``Module_Action`` 命名约定，必须以其规范大小写拼写（例如 CMake 的 ``ExternalProject_Add`` 被 Zephyr 的 ``ExternalZephyrProject_Add`` 扩展）。``CMakeStyle`` 检查将这些从小写规则中豁免。小写命令的扩展保持小写（例如 ``add_dependencies`` 被 sysbuild 的 ``sysbuild_add_dependencies`` 扩展）。

- **每行一个文件参数**：将文件参数跨多行断开以便于扫描和识别每个源文件或项。

  .. code-block:: cmake

     # Good:
     target_sources(my_target PRIVATE
       src/file1.cpp
       src/file2.cpp
     )

      # Bad:
     target_sources(my_target PRIVATE src/file1.cpp src/file2.cpp)

变量命名
***************

- **缓存变量或跨 CMake 文件共享的变量使用大写**：使用 ``option`` 或 ``set(... CACHE ...)`` 定义缓存变量时，使用**大写名称**。

  .. code-block:: cmake

     option(ENABLE_TESTS "Enable test suite" ON)
     set(CMAKE_CXX_STANDARD 17 CACHE STRING "C++ standard version")

- **本地变量使用小写**：对于 CMake 文件中的本地变量，使用**小写**或**snake_case**。

  .. code-block:: cmake

     set(output_dir "${CMAKE_BINARY_DIR}/output")

- **一致的前缀**：为变量使用一致的前缀以避免名称冲突，特别是在大型项目中。

  .. code-block:: cmake

     set(MYPROJECT_SRC_DIR "${CMAKE_SOURCE_DIR}/src")

引用
*******

- **引用字符串和变量**：始终引用字符串字面量和变量以防止意外行为，特别是在处理可能包含空格的路径或参数时。

  .. code-block:: cmake

     # Good:
     set(my_path "${CMAKE_SOURCE_DIR}/include")

     # Bad:
     set(my_path ${CMAKE_SOURCE_DIR}/include)

- **不引用布尔值**：对于布尔值（``ON``、``OFF``、``TRUE``、``FALSE``），避免引用它们。

  .. code-block:: cmake

     option(BUILD_SHARED_LIBS "Build shared libraries" OFF)

避免硬编码路径
**********************

- 使用 CMake 变量（``CMAKE_SOURCE_DIR``、``CMAKE_BINARY_DIR``、``CMAKE_CURRENT_SOURCE_DIR``）而不是硬编码路径。

  .. code-block:: cmake

     set(output_dir "${CMAKE_BINARY_DIR}/bin")

条件逻辑
*****************

- 使用 ``if``、``elseif`` 和 ``else`` 配合适当的缩进，并用 ``endif()`` 关闭。

  .. code-block:: cmake

     if(ENABLE_TESTS)
       add_subdirectory(tests)
     endif()

文档
*************

- 使用注释记录 CMake 文件中的复杂逻辑。

  .. code-block:: cmake

     # Find LlvmLld components required for building with llvm
     find_package(LlvmLld 14.0.0 REQUIRED)
