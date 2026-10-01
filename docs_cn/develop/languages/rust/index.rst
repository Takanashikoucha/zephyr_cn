.. _language_rust:

Rust 语言支持
#####################

Rust 是一种现代系统编程语言，旨在在不牺牲底层控制能力的前提下提供内存安全、并发和性能。它通过独特的所有权模型，在编译时消除空指针解引用和数据竞争等常见缺陷。

Rust 对安全性和正确性的强调使其特别适合嵌入式系统以及可靠性至关重要的环境。此外，Rust 提供强大的抽象，且不依赖运行时或垃圾回收器，使开发者能够自信且高效地编写高层代码和底层硬件交互代码。

这些特性使 Rust 成为 Zephyr 上项目的有力选择，因为在这些项目中资源约束和系统稳定性至关重要。

启用 Rust 支持
*********************

要在 Zephyr 应用中启用 Rust 支持，需要完成以下几项工作：

1.  由于 Rust 目前是一个可选模块，因此需要启用该模块。最简单的方法是通过 west：

    .. code-block:: shell

       west config manifest.project-filter +zephyr-lang-rust
       west update

    执行后，Rust 语言支持会被放置在你的 Zephyr 工作区的 :samp:`modules/lang/rust` 目录中。

2.  通过 :file:`prj.conf` 中的 :kconfig:option:`CONFIG_RUST` 启用 Rust 支持。最简单的方法（同时也用于完成下一步的 CMake 配置）是从 :module_file:`modules/lang/rust/samples <zephyr-lang-rust:samples>` 中的某个示例开始。

3.  配置应用的 :file:`CMakeLists.txt` 文件以支持 Rust。这同样最适合从示例中复制，内容大致如下：

    .. code-block:: cmake

       cmake_minimum_required(VERSION 3.28.0)

       find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})

       project(my_app)
       rust_cargo_application()

4.  创建一个 :file:`Cargo.toml` 文件，用于描述如何构建 Rust 应用。以下来自 Hello World 示例：

    .. code-block:: toml

       [package]
       # This must be rustapp for now.
       name = "rustapp"
       version = "0.1.0"
       edition = "2021"
       description = "The description of my app"
       license = "Apache-2.0 or MIT"

       [lib]
       crate-type = ["staticlib"]

       [dependencies]
       zephyr = "0.1.0"
       log = "0.4.22"

    唯一必需的依赖项是 ``zephyr``，它提供用于与 Zephyr 交互的 zephyr crate。

5.  像构建其他 Zephyr 应用一样构建应用。目前只有少数目标支持 Rust（这些目标可以在 :module_file:`modules/lang/rust/etc/platforms.txt <zephyr-lang-rust:etc/platforms.txt>` 文件中查看）。

API 文档
*****************

模块中最新版本的 `API Documentation`_ 托管在 gh-pages 上。

.. _`API Documentation`:
   https://zephyrproject-rtos.github.io/zephyr-lang-rust/nostd/zephyr/index.html

该文档针对通用目标生成，并启用所有功能。一旦你拥有一个可构建的应用，就可以专门针对你的目标生成文档：

.. code-block:: shell

   west build -t rustdoc

   ...

   Generated /my/path/app/zephyr/build/doc/rust/target/riscv32i-unknown-none-elf/doc/rustapp/index.html

最后打印出的路径可以在浏览器中打开。顶层文档对应的是你的应用本身。在左侧栏找到 “zephyr” crate，即可进入 Zephyr 的文档。该页面还会为你的应用直接或间接使用的所有依赖项生成本地文档。
