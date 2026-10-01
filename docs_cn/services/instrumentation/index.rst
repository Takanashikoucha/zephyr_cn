.. _instrumentation:

Instrumentation
###############

Overview
********

Instrumentation
subsystem
提供
Zephyr
applications
的
compiler-managed
runtime
system
instrumentation
capabilities。其
允许
developers
trace
function
calls、
observe
context
switches（并
用
minimal
manual
instrumentation
effort
profile
application
performance。

与
提供
RTOS-aware
tracing
和
structured
event
APIs 的
:ref:`tracing <tracing>`
subsystem
不同（instrumentation
subsystem
在
更低
level
运作（利用
compiler
instrumentation
hooks。此
approach
使
捕获
几乎
任何
function
entry
和
exit
events
成为
可能（而
无需
在
code
中
手动
tracing
calls。

.. admonition:: Tracing vs. Instrumentation
   :class: hint

   **何时
   用
   Tracing**：需
   RTOS-aware
   event
   tracing
   （如
   thread
   switches、
   semaphore
   operations
   等）且
   想
   minimize
   overhead
   时
   选择
   tracing
   subsystem。

   **何时
   用
   Instrumentation**：需
   function-level
   execution 的
   detailed
   view
   以
   更好
   理解
   code
   flow（或
   不
   添加
   manual
   trace
   points
   而
   识别
   performance
   bottlenecks
   时
   选择
   instrumentation。

Instrumentation
subsystem
依赖
compiler
对
automatic
function
instrumentation 的
支持。启用
后（compiler
自动
在
application
中
每个
function（显式
标记
``__no_instrumentation__`` 的
除外）的
entry
和
exit
插入
对
special
instrumentation
handler
functions 的
calls。当前（仅
支持
带
``-finstrument-functions``
compiler
flag 的
GCC。

Subsystem
在
RAM
initialization
后
自动
初始化（并
用
trigger/stopper
functions
控制
何时
recording
active。默认
trigger
和
stopper
functions
均
设为
``main()``（可
通过
Kconfig
配置）（意味
instrumentation
捕获
从
``main()``
开始
到
其
返回
的
整个
execution。

Recorded
data
存储
在
RAM 中（且
得益于
暴露
一组
simple
commands 的
UART
backend（可
从
host
computer
访问。
:zephyr_file:`scripts/instrumentation/zaru.py`
script
允许
通过
high-level
command-line
interface
执行
这些
commands（并
使
以
适合
further
analysis（如
用
`Perfetto`_）的
format
获取
data
变
容易。

Operational Modes
*****************

Instrumentation
subsystem
支持
可
独立
或
一起
启用
的
两种
modes：

Callgraph Mode (Tracing)
========================

Callgraph
mode（
:kconfig:option:`CONFIG_INSTRUMENTATION_MODE_CALLGRAPH`
启用）中（
subsystem
在
memory
buffer
中
记录
带
timestamps
和
context
information 的
function
entry
和
exit
events。这
使
以下
成为
可能：

- 重建
  完整
  function
  call
  graph
- 观察
  thread
  context
  switches
- 分析
  execution
  flow
  和
  timing
  relationships

Trace
buffer
可
以
ring
buffer
mode（默认（覆盖
旧
entries）或
fixed
buffer
mode（满
时
停止）运行。Buffer
size
可
通过
:kconfig:option:`CONFIG_INSTRUMENTATION_MODE_CALLGRAPH_TRACE_BUFFER_SIZE`
配置。

.. code-block:: console
   :caption: Example of callgraph mode output. See :ref:`zaru_usage` for more details.

   $ ./scripts/instrumentation/zaru.py trace

      Thread Name      Thread ID  CPU  Mode     Timestamp          Function(s)
   ------------------------------------------------------------------------------------------------
               ... (truncated) ...

               main    0x20001a38   0)    0 |    187837720 ns |               sys_dlist_append();
               main    0x20001a38   0)    0 |    188802680 ns |             };   /* z_priq_simple_add */
               main    0x20001a38   0)    0 |    189282840 ns |           };   /* add_to_waitq_locked */
               main    0x20001a38   0)    0 |    189770000 ns |           add_thread_timeout();
               main    0x20001a38   0)    0 |    190732920 ns |         };   /* pend_locked */
               main    0x20001a38   0)    0 |    191198480 ns |         k_spin_release();
               main    0x20001a38   0)    0 |    192125560 ns |         z_swap() {
               main    0x20001a38   0)    0 |    192590080 ns |           k_spin_release();
               main    0x20001a38   0)    0 |    193520000 ns |           z_swap_irqlock() {
               main    0x20001a38   0)    0 |    193987840 ns |             __set_BASEPRI() {
               main    0x20001a38   0)    0 |    194474640 ns | /* --> Scheduler switched OUT from thread 'main' */
        thread-none   none-thread   0)    0 |    195178000 ns | /* <-- Scheduler switched IN thread 'thread-none' */
        thread-none   none-thread   0)    0 |    195851520 ns | z_thread_entry() {
        thread-none   none-thread   0)    0 |    196312600 ns |   k_sched_current_thread_query() {
        thread-none   none-thread   0)    0 |    196774680 ns |     z_impl_k_sched_current_thread_query();
        thread-none   none-thread   0)    0 |    197694480 ns |   };   /* k_sched_current_thread_query */
           thread_A    0x200000d8   0)    7 |    198160000 ns | thread_A() {
           thread_A    0x200000d8   0)    7 |    198443400 ns |   get_sem_and_exec_function() {
           thread_A    0x200000d8   0)    7 |    198727440 ns |     k_sem_take() {
           thread_A    0x200000d8   0)    7 |    199011840 ns |       z_impl_k_sem_take() {
           thread_A    0x200000d8   0)    7 |    199397520 ns |         k_spin_lock() {
           thread_A    0x200000d8   0)    7 |    199784200 ns |           __get_BASEPRI();
           thread_A    0x200000d8   0)    7 |    200557840 ns |           __set_BASEPRI_MAX();
           thread_A    0x200000d8   0)    7 |    201333640 ns |           __ISB();
           thread_A    0x200000d8   0)    7 |    202111360 ns |           z_spinlock_validate_pre();
           thread_A    0x200000d8   0)    7 |    202891000 ns |           z_spinlock_validate_post();
           thread_A    0x200000d8   0)    7 |    203664760 ns |         };   /* k_spin_lock */
           thread_A    0x200000d8   0)    7 |    204058000 ns |         k_spin_unlock() {
           thread_A    0x200000d8   0)    7 |    204450840 ns |           __set_BASEPRI();
           thread_A    0x200000d8   0)    7 |    205231640 ns |           __ISB();
           thread_A    0x200000d8   0)    7 |    206009600 ns |         };   /* k_spin_unlock */
           thread_A    0x200000d8   0)    7 |    206291600 ns |       };   /* z_impl_k_sem_take */
           thread_A    0x200000d8   0)    7 |    206572920 ns |     };   /* k_sem_take */

           ... (truncated) ...

Statistical Mode (Profiling)
============================

Statistical
mode（
:kconfig:option:`CONFIG_INSTRUMENTATION_MODE_STATISTICAL`
启用）中（
subsystem
累积
trigger
和
stopper
points 间
执行的
每个
unique
function 的
timing
statistics。这
提供
每
function 的
total
execution
time（并
帮助
识别
performance
bottlenecks。Subsystem
跟踪
最多
:kconfig:option:`CONFIG_INSTRUMENTATION_MODE_STATISTICAL_MAX_NUM_FUNC`
unique
functions。

.. code-block:: console
   :caption: Example of statistical mode output (top 10 most expensive functions). See
             :ref:`zaru_usage` for more details.

   $ ./scripts/instrumentation/zaru.py profile -n 10

   9.45% 0000061d main
   6.00% 0000049d k_msleep
   5.98% 00000469 k_sleep
   5.95% 0000aea1 k_sleep_ticks
   5.93% 0000ad6d z_impl_k_sleep_ticks
   5.66% 00000431 k_sem_take
   5.65% 00007e65 z_impl_k_sem_take
   5.51% 0000ac29 z_pend_curr
   2.83% 000063ed sys_clock_isr
   2.67% 0000d361 sys_clock_announce

Configuration
*************

用
以下
启用
instrumentation：

.. code-block:: cfg

   CONFIG_INSTRUMENTATION=y
   CONFIG_INSTRUMENTATION_MODE_CALLGRAPH=y    # For tracing
   CONFIG_INSTRUMENTATION_MODE_STATISTICAL=y  # For profiling

Instrumentation
subsystem
通过
UART
console
与
target
device
通信。确保
``zephyr_console``
chosen
node
指向
期望
UART
controller。

:ref:`Retained memory <retention_api>`
使
trigger/stopper
function
addresses
跨
reboots
持久。此
feature
可选（
:kconfig:option:`CONFIG_INSTRUMENTATION_DYNAMIC_TRIGGER`
Kconfig
option
启用。启用
后（devicetree
须
指定
retained
memory
region：

.. code-block:: devicetree

   / {
       sram@2003FC00 {
           compatible = "zephyr,memory-region", "mmio-sram";
           reg = <0x2003FC00 DT_SIZE_K(1)>;
           zephyr,memory-region = "RetainedMem";

           retainedmem {
               compatible = "zephyr,retained-ram";
               status = "okay";

               instrumentation_triggers: retention@0 {
                   compatible = "zephyr,retention";
                   status = "okay";
                   reg = <0x0 0x10>;
               };
           };
       };
   };

   /* Adjust main SRAM to exclude retained region */
   &sram0 {
       reg = <0x20000000 DT_SIZE_K(255)>;
   };

完整
configuration
示例
参见
:zephyr:code-sample:`instrumentation`
sample。
Additional
options
包括
buffer
sizes、
trigger
functions 和
function/file
exclusion
lists（参见
以
:kconfig:option-regex:`CONFIG_INSTRUMENTATION_*`
开头的
Kconfig
options）。

.. _zaru_usage:

``zaru.py`` Usage
*****************

``zaru.py``
command-line
tool（位于
:zephyr_file:`scripts/instrumentation/zaru.py`）
提供
控制
instrumentation
并
通过
UART
从
target
提取
data 的
interface。

Tool
提供
若干
commands：

- ``status``：检查
  target
  device
  是否
  支持

  - callgraph
    (tracing)
    mode
  - statistical
    (profiling)
    mode
  - dynamic
    trigger/stopper
    functions
    configuration

- ``trace``：捕获
  并
  显示
  function
  call
  traces。
- ``profile``：捕获
  并
  显示
  function
  profiling
  data。
- ``reboot``：重启
  target
  device。

可
运行
``zaru.py <command> --help``
获取
每个
command 的
help。

默认（``zaru.py``
尝试
用
``/dev/ttyACM0``
连接
target
device。可
用
``--serial``
option
指定
不同
serial
port：

.. code-block:: console

   $ ./scripts/instrumentation/zaru.py --serial /dev/ttyACM1 status

``--build-dir``
option
可
用于
指定
Zephyr
build
directory（其
用于
定位
ELF
file
以
做
symbol
resolution。未
提供
时（``zaru.py``
尝试
自动
查找。

详细
usage
instructions
参见
:zephyr:code-sample:`instrumentation`
sample
documentation。

Limitations and Considerations
******************************

Compiler
support
  Instrumentation
  subsystem
  需
  带
  ``-finstrument-functions``
  支持的
  GCC。其他
  compilers
  不
  支持。

Stack
size
requirements
  Instrumentation
  为
  每个
  function
  call
  添加
  overhead（这
  增加
  stack
  usage。很可能
  需
  增加
  thread
  stack
  sizes
  以
  容纳
  instrumentation
  handlers
  和
  nested
  function
  calls
  所需
  的
  额外
  space。

Execution
overhead
  所有
  function
  calls
  产生
  instrumentation
  overhead。Code
  size
  因
  添加
  的
  instrumentation
  calls
  而
  增加（且
  performance
  受
  影响。

Initialization
constraints
  RAM
  initialization
  前
  运行
  的
  code（如
  early
  boot
  functions）不
  被
  捕获（因其
  在
  instrumentation
  subsystem
  初始化
  前
  运行。

为
减少
overhead（用
trigger/stopper
functions
仅
instrument
感兴趣
的
code
regions（并
用
:kconfig:option:`CONFIG_INSTRUMENTATION_EXCLUDE_FUNCTION_LIST`
和
:kconfig:option:`CONFIG_INSTRUMENTATION_EXCLUDE_FILE_LIST`
排除
performance-critical
functions。

API Reference
*************

.. doxygengroup:: instrumentation_api

.. _Perfetto: https://perfetto.dev/
