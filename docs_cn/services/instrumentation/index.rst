.. _instrumentation:

Instrumentation
###############

Overview
********

instrumentation（插桩）子系统为 Zephyr 应用提供由编译器管理的运行时系统插桩能力。它使开发者能够跟踪函数调用、观察上下文切换，并以最少的插桩工作量来分析应用性能。

与 :ref:`tracing <tracing>` 子系统（提供 RTOS 感知的结构化事件 API 跟踪）不同，instrumentation 子系统工作在更低的层次，它利用编译器插桩钩子来实现。这种方式使得无需在代码中手动编写跟踪调用，即可捕获几乎任何函数的进入和退出事件。

.. admonition:: Tracing vs. Instrumentation
   :class: hint

   **何时使用 Tracing**：当你需要 RTOS 感知的事件跟踪（例如线程切换、信号量操作等）并希望最小化开销时，选择 tracing 子系统。

   **何时使用 Instrumentation**：当你需要函数级别的详细执行视图以更好地理解代码流程，或在不添加手动跟踪点的情况下识别性能瓶颈时，选择 instrumentation。

instrumentation 子系统依赖编译器对自动函数插桩的支持。启用后，编译器会自动在应用中每个函数的入口和出口处插入对特殊插桩处理函数的调用（显式标记为 ``__no_instrumentation__`` 的函数除外）。目前仅支持使用 ``-finstrument-functions`` 编译器标志的 GCC。

该子系统在 RAM 初始化完成后自动初始化，并使用触发器/停止器函数来控制记录何时处于激活状态。默认的触发器和停止器函数都设置为 ``main()``（可通过 Kconfig 配置），这意味着插桩会捕获从 ``main()`` 开始直到其返回的整个执行过程。

记录的数据存储在 RAM 中，可以通过一个 UART 后端从主机计算机访问，该后端暴露了一组简单的命令。:zephyr_file:`scripts/instrumentation/zaru.py` 脚本允许通过高层命令行界面执行这些命令，并轻松获取适合进一步分析（例如使用 `Perfetto`_）格式的数据。

Operational Modes
*****************

instrumentation 子系统支持两种可独立或同时启用的模式：

Callgraph Mode (Tracing)
========================

在调用图模式（通过 :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_CALLGRAPH` 启用）下，子系统将函数进入和退出事件连同时间戳和上下文信息一起记录到内存缓冲区中。这可以实现：

- 重建完整的函数调用图
- 观察线程上下文切换
- 分析执行流程和时序关系

跟踪缓冲区可以工作于环形缓冲区模式（默认，覆盖旧条目）或固定缓冲区模式（写满后停止）。缓冲区大小可通过 :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_CALLGRAPH_TRACE_BUFFER_SIZE` 配置。

.. code-block:: console
   :caption: 调用图模式输出示例。更多详情请参见 :ref:`zaru_usage`。

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

在统计模式（通过 :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_STATISTICAL` 启用）下，子系统会累积触发点和停止点之间执行的每个唯一函数的计时统计数据。这提供了每个函数的总执行时间，有助于识别性能瓶颈。子系统最多可跟踪 :kconfig:option:`CONFIG_INSTRUMENTATION_MODE_STATISTICAL_MAX_NUM_FUNC` 个唯一函数。

.. code-block:: console
   :caption: 统计模式输出示例（开销最大的前 10 个函数）。更多详情请参见
             :ref:`zaru_usage`。

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

通过以下方式启用 instrumentation：

.. code-block:: cfg

   CONFIG_INSTRUMENTATION=y
   CONFIG_INSTRUMENTATION_MODE_CALLGRAPH=y    # 用于 tracing
   CONFIG_INSTRUMENTATION_MODE_STATISTICAL=y  # 用于 profiling

instrumentation 子系统通过 UART 控制台与目标设备通信。请确保 ``zephyr_console`` chosen 节点指向所需的 UART 控制器。

:ref:`Retained memory <retention_api>` 可使触发器/停止器函数地址在重启后保持。该功能是可选的，通过 :kconfig:option:`CONFIG_INSTRUMENTATION_DYNAMIC_TRIGGER` Kconfig 选项启用。启用后，设备树必须指定一个保留内存区域：

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

完整的配置示例请参见 :zephyr:code-sample:`instrumentation` 示例。其他选项包括缓冲区大小、触发函数以及函数/文件排除列表（参见以 :kconfig:option-regex:`CONFIG_INSTRUMENTATION_*` 开头的 Kconfig 选项）。

.. _zaru_usage:

``zaru.py`` Usage
*****************

``zaru.py`` 命令行工具（位于 :zephyr_file:`scripts/instrumentation/zaru.py`）提供了控制 instrumentation 并通过 UART 从目标设备提取数据的接口。

该工具提供多个命令：

- ``status``：检查目标设备是否支持

  - callgraph（tracing）模式
  - statistical（profiling）模式
  - 动态触发器/停止器函数配置

- ``trace``：捕获并显示函数调用跟踪。
- ``profile``：捕获并显示函数性能分析数据。
- ``reboot``：重启目标设备。

你可以通过运行 ``zaru.py <command> --help`` 获取每个命令的帮助。

默认情况下，``zaru.py`` 尝试使用 ``/dev/ttyACM0`` 连接目标设备。你可以使用 ``--serial`` 选项指定其他串口：

.. code-block:: console

   $ ./scripts/instrumentation/zaru.py --serial /dev/ttyACM1 status

``--build-dir`` 选项可用于指定 Zephyr 构建目录，这对于定位用于符号解析的 ELF 文件是必需的。如果未提供，``zaru.py`` 将尝试自动查找。

详细的使用说明请参见 :zephyr:code-sample:`instrumentation` 示例文档。

Limitations and Considerations
******************************

Compiler support
  instrumentation 子系统需要支持 ``-finstrument-functions`` 的 GCC。不支持其他编译器。

Stack size requirements
  插桩会为每个函数调用增加开销，从而增加栈使用量。你可能需要增大线程栈大小，以适应插桩处理函数和嵌套函数调用所需的额外空间。

Execution overhead
  所有函数调用都会产生插桩开销。由于增加了插桩调用，代码体积会增大，性能也会受到影响。

Initialization constraints
  在 RAM 初始化之前运行的代码（例如早期启动函数）不会被捕获，因为它在 instrumentation 子系统初始化之前运行。

为减少开销，请使用触发器/停止器函数仅对感兴趣的代码区域进行插桩，并通过 :kconfig:option:`CONFIG_INSTRUMENTATION_EXCLUDE_FUNCTION_LIST` 和 :kconfig:option:`CONFIG_INSTRUMENTATION_EXCLUDE_FILE_LIST` 排除性能关键函数。

API Reference
*************

.. doxygengroup:: instrumentation_api

.. _Perfetto: https://perfetto.dev/
