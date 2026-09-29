DEFAULT_IMAGE
#############

sysbuild 构建中主应用镜像的名称。

这是以 ``APP_TYPE MAIN`` 添加的镜像，也是 :file:`domains.yaml` 中报告为默认域（default domain）的镜像。
在 :file:`sysbuild.cmake` 文件中使用它来引用主镜像，而无需硬编码其名称。

参见 :cmake:command:`ExternalZephyrProject_Add`。
