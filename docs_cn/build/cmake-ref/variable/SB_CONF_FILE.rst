SB_CONF_FILE
############

Sysbuild 的 Kconfig 配置文件，或文件列表。

默认值为 :cmake:variable:`APPLICATION_CONFIG_DIR` 中的 :file:`sysbuild.conf`（如果该文件存在）。
Sysbuild 是可选启用（opt-in）的功能，因此该文件是可选的。

这些文件中的设置会覆盖 sysbuild 自身 Kconfig 树的默认值。路径相对于 :cmake:variable:`APP_DIR` 解析。

参见 :cmake:module:`sysbuild_kconfig`。
