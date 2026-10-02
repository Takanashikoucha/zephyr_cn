.. _timing_functions:

执行时间函数
########################

时间函数可用于获取一段代码的执行时间，以辅助分析和优化。

请注意，时间函数可能使用与默认内核定时器不同的定时器，所使用的定时器由架构、SoC 或板级配置指定。

配置
*************

要允许使用时间函数，需要启用 :kconfig:option:`CONFIG_TIMING_FUNCTIONS`。

用法
*****

要收集时间信息：

1. 调用 :c:func:`timing_init` 初始化定时器。

2. 调用 :c:func:`timing_start` 发出开始收集时间信息的信号。这通常会启动定时器。

3. 调用 :c:func:`timing_counter_get` 标记代码执行的开始。

4. 调用 :c:func:`timing_counter_get` 标记代码执行的结束。

5. 调用 :c:func:`timing_cycles_get` 获取代码执行开始和结束之间的定时器周期数。

6. 使用总周期数调用 :c:func:`timing_cycles_to_ns` 将周期数转换为纳秒。

7. 从第 3 步重复，以收集其他代码块的时间信息。

8. 调用 :c:func:`timing_stop` 发出结束收集时间信息的信号。这通常会停止定时器。

示例
-------

下面展示一个如何使用时间函数的示例：

.. code-block:: c

   #include <zephyr/timing/timing.h>

   void gather_timing(void)
   {
       timing_t start_time, end_time;
       uint64_t total_cycles;
       uint64_t total_ns;

       timing_init();
       timing_start();

       start_time = timing_counter_get();

       code_execution_to_be_measured();

       end_time = timing_counter_get();

       total_cycles = timing_cycles_get(&start_time, &end_time);
       total_ns = timing_cycles_to_ns(total_cycles);

       timing_stop();
   }

API 文档
*****************

.. doxygengroup:: timing_api
.. doxygengroup:: timing_api_arch
.. doxygengroup:: timing_api_soc
.. doxygengroup:: timing_api_board
