.. _thread_analyzer:

线程分析器（Thread analyzer）
###################

线程分析器模块启用跟踪
线程信息所需的所有 Zephyr 选项，例如线程栈大小使用情况以及其他运行时线程
运行统计数据。

分析在应用程序调用
:c:func:`thread_analyzer_run` 或 :c:func:`thread_analyzer_print` 时按需执行。

例如，要构建启用 Thread Analyser 的 synchronization 示例，
请执行以下操作：

   .. zephyr-app-commands::
      :zephyr-app: samples/synchronization/
      :board: qemu_x86
      :goals: build
      :gen-args: -DCONFIG_QEMU_ICOUNT=n -DCONFIG_THREAD_ANALYZER=y \
                   -DCONFIG_THREAD_ANALYZER_USE_PRINTK=y -DCONFIG_THREAD_ANALYZER_AUTO=y \
                   -DCONFIG_THREAD_ANALYZER_AUTO_INTERVAL=5


在 Qemu 中运行生成的应用程序，将获得
来自 Thread Analyzer 的额外
信息::


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


配置
*************
使用以下选项配置该模块。

:kconfig:option:`CONFIG_THREAD_ANALYZER`
   启用该模块。
:kconfig:option:`CONFIG_THREAD_ANALYZER_USE_PRINTK`
   使用 printk 输出线程统计数据。
:kconfig:option:`CONFIG_THREAD_ANALYZER_USE_LOG`
   使用日志记录器（logger）输出线程统计数据。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO`
   自动运行线程分析器。
   使用该选项时无需向应用程序添加任何代码。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO_INTERVAL`
   自动
   模式下，模块在连续两次打印线程分析之间睡眠的时间。
:kconfig:option:`CONFIG_THREAD_ANALYZER_AUTO_STACK_SIZE`
  线程分析器自动线程的栈。
:kconfig:option:`CONFIG_THREAD_NAME`
  打印线程名称而非线程 ID。
:kconfig:option:`CONFIG_THREAD_RUNTIME_STATS`
  打印线程运行数据，例如利用率。
  该选项由 :kconfig:option:`CONFIG_THREAD_ANALYZER` 自动选择。
:kconfig:option:`CONFIG_THREAD_ANALYZER_LONG_FRAME_PER_INTERVAL`
  打印后重置最长帧（Longest Frame）值统计。
  使用 :kconfig:option:`SCHED_THREAD_USAGE_ANALYSIS` 获取平均帧和最长帧
  线程统计时，每次
  打印线程统计后将最长帧值重置为零。这使得可以观察
  最近一个区间期间的最长帧，而非自启动以来的最长帧。
:kconfig:option:`CONFIG_THREAD_ANALYZER_PRINT_THREAD_PRIORITY`
  打印每个线程的优先级。

API 文档
*****************

.. doxygengroup:: thread_analyzer
