.. _external_module_wamr:

WebAssembly Micro Runtime（WAMR）
################################

简介
****

`WebAssembly Micro Runtime`_（WAMR）是一个轻量级独立 WebAssembly
运行时，面向嵌入式和资源受限设备设计。它允许应用在运行时加载并执行
WebAssembly（WASM）模块，因此功能可以在不重新烧录固件的情况下更新
或扩展，不受信任的代码可以在 WASM 规范定义的沙箱中运行。运行时 API、
执行模式和 ``wamrc`` AOT 编译器请参见 `WAMR 文档`_。

WAMR 通过专用平台层支持 Zephyr，并在其自身仓库中附带 Zephyr 模块
胶水代码（``zephyr/module.yml``、``zephyr/Kconfig`` 和
``zephyr/CMakeLists.txt``），因此应用只需选择几个 Kconfig 选项即可
将运行时链接进其镜像。

WAMR 采用带 LLVM 例外的 Apache License 2.0。

在 Zephyr 中使用
****************

要将 WAMR 作为 Zephyr 模块使用，在 Zephyr 子 manifest（例如
``zephyr/submanifests/wamr.yaml``）中添加以下条目，然后运行
``west update``，或者将其作为 West 项目添加到项目的 ``west.yml``
manifest：

.. code-block:: yaml

   manifest:
     projects:
       - name: wasm-micro-runtime
         url: https://github.com/wasm-micro-runtime/wasm-micro-runtime
         revision: main
         path: modules/wasm-micro-runtime # adjust the path as needed

配置运行时
==========

运行时默认禁用。在应用的 ``prj.conf`` 中启用它并使用 ``CONFIG_WAMR_*``
选项选择其特性：

.. code-block:: cfg

   CONFIG_WAMR=y
   CONFIG_WAMR_INTERP=y
   CONFIG_WAMR_AOT=y
   CONFIG_WAMR_LIBC_BUILTIN=y
   CONFIG_WAMR_GLOBAL_HEAP_POOL=y
   CONFIG_WAMR_GLOBAL_HEAP_SIZE=131072

每个选项都映射到常规 WAMR 构建脚本使用的对应 ``WAMR_BUILD_*``
CMake 变量，仍可在 CMake 命令行列（例如 ``-DWAMR_BUILD_AOT=0``）
覆盖以做一次性构建。

``WAMR_BUILD_TARGET`` 由板架构推导而来，因此通常无需传入。

WAMR 附带一组 `Zephyr 示例`_；构建和运行方法请参见其 ``README.md``。

参考资料
********

.. target-notes::

.. _WebAssembly Micro Runtime:
   https://github.com/wasm-micro-runtime/wasm-micro-runtime

.. _WAMR 文档:
   https://github.com/wasm-micro-runtime/wasm-micro-runtime/tree/main/doc

.. _Zephyr 示例:
   https://github.com/wasm-micro-runtime/wasm-micro-runtime/tree/main/product-mini/platforms/zephyr
