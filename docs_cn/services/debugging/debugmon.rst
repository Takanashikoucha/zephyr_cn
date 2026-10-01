.. _debugmon:

Cortex-M Debug Monitor
######################

Monitor mode debugging 为 Cortex-M feature（提供
非 halting 的调试方法。借此（即使等待
breakpoint 时也可继续执行高 priority interrupts。
此策略使调试 time-sensitive software 成为可能（否则
core halts 时会崩溃（如须保持
communication links 存活的 applications）。

Zephyr 提供启用并配置 Debug Monitor exception 的支持。
其还包含 interrupt 的 ready 实现（可与
SEGGER J-Link debuggers 一起使用。

Configuration
*************

用以下 options 配置此 module。

* :kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK`: 启用 module。此 option 本身
  需 debug monitor interrupt 的实现（其将在
  程序每次进入 breakpoint 时执行。

用 SEGGER debug probe（可使用 SEGGER 提供的 ready interrupt
实现。

* :kconfig:option:`CONFIG_SEGGER_DEBUGMON`: 启用 SEGGER debug monitor interrupt。可
  与 SEGGER JLinkGDBServer 和 SEGGER debug probe 一起
  使用。


Usage
*****

启用 monitor mode debugging 时（进入 breakpoint 不会 halt
processor（而是生成 interrupt（其 ISR 实现于
``z_arm_debug_monitor`` symbol 下。:kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK` config 将此 interrupt
配置为
最低可用 priority（这将允许 processor 在
breakpoint 上 spin 期间其他 interrupts 执行。

Using SEGGER-provided ISR
=========================

:kconfig:option:`CONFIG_SEGGER_DEBUGMON` 提供的 ready 实现提供
用常规 GDB commands 以 monitor mode 调试所需
functionality。配置 SEGGER debug monitor 的步骤：

1. 构建启用 :kconfig:option:`CONFIG_CORTEX_M_DEBUG_MONITOR_HOOK`` 和 :kconfig:option:`CONFIG_SEGGER_DEBUGMON`
   configs 的 sample。

2. 将 JLink GDB server 附加到 target。
   Linux command 示例：``JLinkGDBServerCLExe -device <device> -if swd``。

3. 用 GDB installation 连接到 server。
   Linux command 示例：``arm-none-eabi-gdb --ex="file build/zephyr.elf" --ex="target remote localhost:2331"``。

4. 用 command ``monitor exec SetMonModeDebug=1`` 在 GDB 中启用 monitor mode debugging。

这些步骤后（用常规 gdb commands 调试 program。


Using other custom ISR
======================
要提供自定义 debug monitor interrupt（覆盖 ``z_arm_debug_monitor``
symbol。另外（须手动配置某些 registers
（参见 :zephyr:code-sample:`debugmon` sample）。
