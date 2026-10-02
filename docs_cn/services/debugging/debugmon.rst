.. _debugmon:

Cortex-M Debug Monitor
######################

监视模式调试（Monitor mode debugging）是 Cortex-M 的一项特性，提供一种非停止（non-halting）的
调试方法。借助该特性，即使正在等待断点，也可以继续执行高优先级中断。
该策略使得调试时间敏感的软件成为可能，否则这类软件
在核心停止时会崩溃（例如需要保持
通信链路存活的应用程序）。

Zephyr 提供了启用和配置 Debug Monitor 异常的支持。
它还包含中断的现成实现，可以与
SEGGER J-Link 调试器一起使用。

配置
*************

使用以下选项配置该模块。

* :kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK`：启用该模块。该选项本身
  需要一个调试监视中断的实现，该实现将在
  程序每次进入断点时执行。

使用 SEGGER 调试探针时，可以使用 SEGGER 提供的现成中断
实现。

* :kconfig:option:`CONFIG_SEGGER_DEBUGMON`：启用 SEGGER 调试监视中断。可以
  与 SEGGER JLinkGDBServer 和 SEGGER 调试探针一起
  使用。


用法
*****

启用监视模式调试时，进入断点不会停止
处理器，而是生成一个中断，其中断服务例程（ISR）实现在
``z_arm_debug_monitor`` 符号下。:kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK` 配置项将该中断
配置为
最低可用优先级，这使得处理器在
断点上自旋（spin）期间其他中断仍然可以执行。

使用 SEGGER 提供的 ISR
=========================

:kconfig:option:`CONFIG_SEGGER_DEBUGMON` 提供的现成实现提供了
使用常规 GDB 命令进行监视模式调试所需的
功能。配置 SEGGER 调试监视的步骤：

1. 构建启用了 :kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK`` 和 :kconfig:option:`CONFIG_SEGGER_DEBUGMON`
   配置项的示例。

2. 将 JLink GDB server 附加到目标。
   Linux 命令示例：``JLinkGDBServerCLExe -device <device> -if swd``。

3. 使用 GDB 连接到服务器。
   Linux 命令示例：``arm-none-eabi-gdb --ex="file build/zephyr.elf" --ex="target remote localhost:2331"``。

4. 在 GDB 中使用命令 ``monitor exec SetMonModeDebug=1`` 启用监视模式调试。

完成这些步骤后，使用常规 gdb 命令调试程序。


使用其他自定义 ISR
=====================
要提供自定义调试监视中断，请覆盖 ``z_arm_debug_monitor``
符号。此外，还需要手动配置某些寄存器
（参见 :zephyr:code-sample:`debugmon` 示例）。
