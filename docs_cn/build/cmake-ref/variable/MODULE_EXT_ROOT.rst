MODULE_EXT_ROOT
###############

包含模块外部根目录（module external root）的目录列表。这些根目录保存着 Zephyr 模块的
CMake 与 Kconfig 胶水代码（用于那些自身不携带这些代码的模块）。

参见 :cmake:module:`sysbuild_root`，了解 sysbuild 如何为镜像构建解析此变量。
