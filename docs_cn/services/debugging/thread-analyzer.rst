.. _thread_analyzer:

Thread analyzer
###################

Thread analyzer module 启用跟踪
thread 信息所需的所有 Zephyr options（如 thread stack size 使用和其他 runtime thread
runtime statistics。

分析在 application 调用
:c:func:`thread_analyzer_run` 或 :c:func:`thread_analyzer_print` 时按需执行。

例如（要构建启用 Thread Analyser 的 synchronization sample（
做以下：

   .. zephyr-app-commands::
      :zephyr-app: samples/synchronization/
      :board: qemu_x86
      :goals: build
      :gen-args: -DCONFIG_QEMU_ICOUNT=n -DCONFIG_THREAD_ANALYZER=y \
                   -DCONFIG_THREAD_ANALYZER_USE_PRINTK=y -DCONFIG_THREAD_ANALYZER_AUTO=y \
                   -DCONFIG_THREAD_ANALYZER_AUTO_INTERVAL=5


在 Qemu 中运行生成的 application（将获得
来自 Thread Analyzer 的额外
information::


	thread_a: Hello World from cpu 0 on qemu_x86!
	Thread analyze:
	 thread_b            : STACK: unused 740 usage 284 / 1024 (27 %); CPU: 0 %
	 thread_analyzer     : STACK: unused 8 usage 504 / 512 (98 %); CPU: 0 %
	 thread_a            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 98 %
	 idle                : STACK: unused 204 usage 116 / 320 (36 %); CPU: 0 %
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	Thread analyze:
	 thread_b            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 7 %
	 thread_analyzer     : STACK: unused 8 usage 504 / 512 (98 %); CPU: 0 %
	 thread_a            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 9 %
	 idle                : STACK: unused 204 usage 116 / 320 (36 %); CPU: 82 %
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	Thread analyze:
	 thread_b            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 7 %
	 thread_analyzer     : STACK: unused 8 usage 504 / 512 (98 %); CPU: 0 %
	 thread_a            : STACK: unused 648 usage 376 / 1024 (36 %); CPU: 8 %
	 idle                : STACK: unused 204 usage 116 / 320 (36 %); CPU: 83 %
	thread_b: Hello World from cpu 0 on qemu_x86!
	thread_a: Hello World from cpu 0 on qemu_x86!
	thread_b: Hello World from cpu 0 on qemu_x86!


Configuration
*************
用以下 options 配置此 module。

:kconfig:option:`CONFIG_THREAD_ANALYZER`
   启用 module。
:kconfig:option:`CONFIG_THREAD_ANALYZER_USE_PRINTK`
   用 printk 作为 thread statistics。
:kconfig:option:`CONFIG_THREAD_ANALYZER_USE_LOG`
   用 logger 作为 thread statistics。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO`
   自动运行 thread analyzer。
   用此 option 时无需向 application 添加任何 code。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO_INTERVAL`
   自动
   mode 中 module 在连续打印 thread analysis 间睡眠的时间。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO_STACK_SIZE`
  Thread analyzer automatic thread 的 stack。
:kconfig:option:`CONFIG_THREAD_NAME`
  打印 thread 的 name 而非其 ID。
:kconfig:option:`CONFIG_THREAD_RUNTIME_STATS`
  打印 thread runtime data（如 utilization。
  此 option 由 :kconfig:option:`CONFIG_THREAD_ANALYZER` 自动选择。
:kconfig:option:`CONFIG_THREAD_ANALYZER_LONG_FRAME_PER_INTERVAL`
  打印后重置 Longest Frame value statistics。
  用 :kconfig:option:`SCHED_THREAD_USAGE_ANALYSIS` 获取 average 和 longest
  frame thread statistics 时（每次
  打印 thread statistics 后将 Longest Frame value 重置为零。这允许观察
  最近 interval 期间的 longest frame（而非自启动以来的 longest frame。
:kconfig:option:`CONFIG_THREAD_ANALYZER_PRINT_THREAD_PRIORITY`
  打印每个 thread 的 priority。

API documentation
*****************

.. doxygengroup:: thread_analyzer
