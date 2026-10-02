.. _nanopb_reference:

Nanopb
######

`Nanopb <https://jpa.kapsi.fi/nanopb/>`_ 是 Google 的
`Protocol Buffers <https://protobuf.dev/>`_ 的 C 语言实现。

要求
************

Nanopb 使用 protocol buffer 编译器生成源文件和头文件，
请确保已安装 ``protoc`` 可执行文件并且可用。

.. tabs::

   .. group-tab:: Ubuntu

      使用 ``apt`` 安装依赖：

         .. code-block:: shell

            sudo apt install protobuf-compiler

   .. group-tab:: macOS

      使用 ``brew`` 安装依赖：

         .. code-block:: shell

            brew install protobuf

   .. group-tab:: Windows

      使用 ``choco`` 安装依赖：

         .. code-block:: shell

            choco install protoc


配置
*************

请确保在你的 ``CMakeLists.txt`` 文件中按如下方式包含 ``nanopb``：

.. code-block:: cmake

   list(APPEND CMAKE_MODULE_PATH ${ZEPHYR_BASE}/modules/nanopb)
   include(nanopb)

可以通过 ``zephyr_nanopb_sources()`` CMake 函数添加 ``proto`` 文件，
该函数确保在构建指定目标之前生成头文件和源文件。

Nanopb 具有 `生成器选项 <https://jpa.kapsi.fi/nanopb/docs/reference.html#generator-options>`_，
可用于配置消息或字段。这允许设置固定大小或完全跳过字段。

内部 CMake 生成器有一个扩展，可自动使用 CMake 变量配置 ``*.options.in`` 文件。

参见 :zephyr_file:`samples/modules/nanopb/src/simple.options.in` 和
:zephyr_file:`samples/modules/nanopb/CMakeLists.txt` 了解使用示例。
