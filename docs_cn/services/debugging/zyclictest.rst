.. _zyclictest:

Zyclictest
##########

Zyclictest module 启用估算 realtime
threads 的 worst case latencies。其可测量从
hardware interrupt 到 service
routine 再到 Zephyr thread 的时间。

此 module 及其名称受 Linux 上的 cyclictest program 启发。
因此其为 Zephyr cyclictest。

其思想为用 timer interrupt 作为 interrupt source（因为我们确切知道
其发生的时间点。在 interrupt service routine 中
取时间（并计算与 timer
interrupt 的 programmed time 的差。

另外 thread 也自行同步到 timer（并同样测量
与 programmed timer 的差。

两个时间放入作为测量结束时打印的
histogram 数据源的 array。

此测量以特定 interval time 循环进行。

若有人想知道 priority <p> 的 task 的 worst case latency（
则 application 须运行。其运行时（可启动
zyclictest（priority 至少比被探测 application thread
低一位。例如（若感兴趣的 thread 的
application 的
priority 为 -10（则须以 -11 或更低的
priority 启动 zyclictest。

另一重要 argument 为 interval time。其不
意味 interval 小于测量的 worst case latency。因此建议
设置至少为期望或测量
worst case latency 两倍的 interval。

若测量结束时指示有 overflows（则意味着
histogram 范围内无确定性 worst case latency。

为有意义的输出（建议设置
:kconfig:option:`CONFIG_SYS_CLOCK_TICKS_PER_SEC` 至少为 1000000（这
意味最小 resolution 为 1 microsecond。还需 tickless kernel
(:kconfig:option:`CONFIG_TICKLESS_KERNEL`:。

Mode of operation
*****************

Zyclictest 可无固定 cycles 数量 free running 启动。
此为默认。停止时打印至今的
result。

在 loop mode（option 以 -l <loops> 启动）中（zyclictest 运行
预定义 cycles 数量。到达该数量时
shell 有指示测试结束的消息。但可用 zyclictest stop -c
提前取消测试。

Configuration
*************

用以下 options 配置此 module。

* :kconfig:option:`CONFIG_ZYCLICTEST_SHELL`: 启用 shell command。


Usage
*****

zyclictest start [options]
  -i <interval>  Interval in microseconds
  -l <loops>     Use loop mode with predefined number of cycles
  -p <prio>      Setup priority of Thread

zyclictest stop [options]
  -c             Cancel loop mode prematurely
  -q             Quiet mode, print summary, but no histogram data

Example
*******

此示例中（想知道由 interrupt 唤醒（且作为
priority -10 的 cooperative task 运行的 thread 的 worst case latency。
期望 latency 小于 200 us。使用 free running mode。

1. 以 400 us 的 interval（期望
worst case latency 两倍）和 -11 的 priority（比
application thread 高一位）启动 zyclictest thread：

   .. code-block:: console

      zyclictest start -i 400 -p -11

2. 做应测试的任何事....

3. 停止测量：

   .. code-block:: console

      zyclictest stop

   Zyclictest 输出：

   ::

      Count: 547329
                         IRQ  Thread
      Max-Latency:        21      27
      Errors:              0       0
      Overflow:            0       0
      Histogram:
      [...]
       23                  0  547306
       24                  0       2
       25                  0       5
       26                  0       5
       27                  0       2
       28                  0       0
      [...]

4. 解释 result：

   无 errors 且无 overflows（意味测量可用。
   测试中有 547329 cycles。
   Worst case interrupt latency 为 21 us（thread 为 27 us。
