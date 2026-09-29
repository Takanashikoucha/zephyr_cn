SB_APPLICATION_CONFIG_DIR
#########################

用于搜索 sysbuild 自身配置文件的目录。

设置后，在定位 :cmake:variable:`SB_CONF_FILE` 时优先于 :cmake:variable:`APPLICATION_CONFIG_DIR`。

参见 :cmake:module:`sysbuild_kconfig`。
