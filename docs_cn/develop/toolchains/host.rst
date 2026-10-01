.. _host_toolchains:

主机工具链
###############

在某些特定配置下，例如在 Linux 主机上为非 MCU 的 x86 目标构建时，
你可以直接复用操作系统提供的原生开发工具。

要使用主机上的 gcc，将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
:ref:`环境变量 <env_vars>` 设置为 ``host/gnu``。
要使用 clang，将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``host/llvm``。
