.. _profiling-perf:

Perf
####

Perf 是一个基于栈跟踪（stack tracing）的性能分析工具，
可用于以极小的代码开销进行轻量级性能分析。

工作原理
**************

``perf record`` shell 命令会启动一个定时器，其回调为 perf 跟踪函数。
定时器由中断驱动，因此 perf 跟踪函数在中断期间被调用。
Zephyr 内核在调用中断处理程序之前，会在中断栈、
``callee_saved`` 结构体或架构特定的异常帧中保存返回地址和帧指针。
因此，perf 跟踪函数利用返回地址和帧指针来生成栈跟踪。

在 Cortex-M 上，perf 对 SysTick 处理程序进行了包装，
以便在常规定时器 ISR 使用处理程序栈之前，
采样被中断的线程模式进程栈指针（PSP）帧。
后端在向 Arm 栈遍历器传递该帧之前会先对其进行校验。

Cortex-M 后端不适用于非安全可信执行（Non-secure Trusted Execution）镜像，
因为非安全固件无法访问安全异常帧。

:zephyr_file:`scripts/profiling/stackcollapse.py` 脚本可用于利用 ELF 文件中的符号，
将栈跟踪中的返回地址转换为函数名，
并以 `FlameGraph`_ 所期望的格式打印出来。

配置
*************

可以使用以下选项配置该模块：

* :kconfig:option:`CONFIG_PROFILING_PERF`：启用该模块。此选项会在 shell 中添加
  ``perf`` 命令。

* :kconfig:option:`CONFIG_PROFILING_PERF_BUFFER_SIZE`：设置 perf 缓冲区的大小，
  样本在打印前先保存在该缓冲区中。

架构后端可能需要额外的栈展开（stack-unwind）支持。Cortex-M 后端
需要 SysTick、线程栈信息、额外的异常信息、Arm 栈遍历支持，
以及单处理器（uniprocessor）配置。

使用
*****

关于如何使用 perf 工具的示例，请参考 :zephyr:code-sample:`profiling-perf` 示例。

 .. _FlameGraph: https://github.com/brendangregg/FlameGraph/
