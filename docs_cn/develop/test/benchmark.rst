.. _ztest_benchmarking:

基准测试框架
######################

Zephyr 基准测试框架提供周期精确（cycle-accurate）的性能测量。它自动化了数据收集和统计计算，为评估 Zephyr 生态系统中的执行指标提供了一种标准化方式。

概览
********

该框架通过以下方式帮助识别回归并优化关键路径：

* **标准化 API**：与现有 ``ztest`` 约定保持一致的宏。
* **统计分析**：计算均值（Mean）、标准差（Standard Deviation）、标准误差（Standard Error）以及最小/最大值（Min/Max）。
* **开销补偿**：包含一个对照测试，用于计入基准测试框架自身的执行时间。

配置
*************

要使用基准测试框架，必须启用以下 Kconfig 选项：

.. code-block:: cfg

   CONFIG_ZTEST=y
   CONFIG_ZTEST_BENCHMARK=y

使用
*****

基准测试套件（benchmark suite）的定义方式与普通 ztest 测试套件类似：首先使用 ``ZTEST_BENCHMARK_SUITE`` 定义套件，然后使用 ``ZTEST_BENCHMARK`` 或 ``ZTEST_BENCHMARK_TIMED`` 宏向套件中添加单个基准测试。

.. code-block:: c

   #include <zephyr/ztest.h>

   ZTEST_BENCHMARK_SUITE(<test suite name>, <setup_fn>, <teardown_fn>);


标准基准测试
===================

标准基准测试是基于样本（sample）的，即执行测试指定的次数并测量所花费的总周期数。这对于基准测试关键路径很有用，可以帮助了解以周期为单位的原始 CPU 性能。它提供了对代码效率的洞察，并有助于从 CPU 使用角度识别瓶颈。这种基准测试方法适合执行时间一致、且不受 I/O 操作或上下文切换等外部因素显著影响的代码。

.. code-block:: c

   #include <zephyr/ztest.h>

   ZTEST_BENCHMARK_SUITE(<suite name>, NULL, NULL);

   ZTEST_BENCHMARK(<suite name>, <benchmark name>, <number of samples>, <setup_fn>, <teardown_fn>)
   {
       /* Code to benchmark */
   }

标准基准测试遵循如下流程：在每个样本之前调用 setup 函数，测试函数执行指定数量的样本，然后在每个样本之后调用 teardown 函数。

定时基准测试
================

与标准基准测试不同，定时基准测试测量的是代码的执行时间而不是周期数。这对于基准测试执行时间可能多变的代码很有用，或者当你想测量实际花费的时间而不是关键路径的 CPU 周期数时。它提供了性能特征的更广泛视图，尤其适用于涉及 I/O 操作、上下文切换或其他可能影响执行时间（超出原始 CPU 性能）的因素的代码。

.. code-block:: c

   ZTEST_BENCHMARK_TIMED(<suite name>, <benchmark name>, <time in ms>, <setup_fn>, <teardown_fn>)
   {
         /* Code to benchmark */
   }


与偏好隔离的标准基准测试不同，定时基准测试只执行一次 setup 和 teardown 函数，允许测试函数在专门的时间窗口内热运行（hot）。这会给出更贴近实际的测量结果，因为它包含了真实世界场景中会遇到的系统开销，例如中断、上下文切换和其他后台任务。

理解结果
*********************

标准基准测试结果
=============================

.. code-block:: console

   <suite name> ###############################################
   <benchmark name> ===========================================
      Sample size:<number of samples>, total cycles: <total amount of cycles>
      Mean(u): <mean cycles per sample>
      Standard deviation(s): <cycles>
      Standard Error(SE): <cycles>
      Min: <cycles> (run #<sample number>)
      Max: <cycles> (run #<sample number>)


统计指标
"""""""""""""""""""

* **均值（Mean, u）**：每个样本花费的平均周期数。它提供了一个中心值，代表预期的执行开销。

* **标准差（Standard Deviation, s）**：衡量执行开销相对于均值的波动或分散程度。标准差较低说明行为是确定性的、一致的。

* **标准误差（Standard Error, SE）**：估计样本均值与系统"真实"均值之间可能相差多远。它提供了对测试统计可靠性的洞察。SE 越低，对结果的置信度越高。

* **最小/最大值（Min/Max）**：观测到的最小和最大周期数，以及它们出现在哪个样本上。

直白地说，对所有指标而言数值越低越好。更低的均值、最小值和最大值表示更好的原始性能；更低的标准差和标准误差表示性能更一致、因此更可靠。

定时基准测试结果
==========================

.. code-block:: console

   <benchmark name> ===============================================
      Samples: <Number of samples executed during the benchmark>
      Total Time: <Gross execution time>
      Work Time: <Net execution time> ns (Net)
      Ops/Sec: <average operations per second>
      Cycles/Op: <average cycles per operation>

统计指标
"""""""""""""""""""
* **总时间（Total Time）**：基准测试所有样本花费的总时间，包括开销在内。

* **工作时间（Work Time）**：被测代码花费的总时间，排除了基准测试框架自身的开销。这提供了对被测代码实际性能更准确的度量。

* **每秒操作数（Ops/Sec）**：每秒可执行的操作（样本）数量，通过样本数除以净工作时间（以秒为单位）计算得出。该指标对于理解被测代码的吞吐量特别有用。

* **每操作周期数（Cycles/Op）**：每个操作花费的平均 CPU 周期数，通过净周期数除以样本数计算得出。该指标从 CPU 使用角度提供了对代码效率的洞察。

一般来说，Ops/Sec 数值越高越好，因为它表示更高的吞吐量；同理 Cycles/Op 数值越低越好。由于 Cycles/Op 和 Ops/Sec 指标源自相同的底层数据，它们从不同视角反映的是相同的性能特征：高 Ops/Sec 应对应低 Cycles/Op，反之亦然。


基准测试输出选项
========================

基准测试框架提供了多种输出基准测试数据的选项。默认情况下，结果以详尽的、人类可读的格式打印，便于理解和解读。
另外，你还可以启用 :kconfig:option:`CONFIG_ZTEST_BENCHMARK_OUTPUT_CSV` Kconfig 选项，以 CSV 格式输出结果，便于脚本导入进行进一步分析。
CSV 输出包含与详尽输出完全相同的各项指标，但格式更适合自动化分析和报告。

标准基准测试的 csv 输出格式如下：

.. code-block:: console

   S,<suite name>,<benchmark name>,<sample size>,<total cycles>,<mean>,<stddev>,<stderr>,<min>,<min sample>,<max>,<max sample>

定时基准测试的 csv 输出格式如下：

.. code-block:: console

   T,<suite name>,<benchmark name>,<samples>,<total time>,<work time>,<ops/sec>,<cycles/op>


重要注意事项
************************

* **噪声**：基准测试天生对系统噪声敏感。为了获得尽可能准确的结果，请禁用可能干扰计时的不必要后台任务和中断。

* **缓存预热**：由于缓存未命中，基准测试的第一个样本往往较慢，在小样本量下这会使结果略微失真；请选择足够大的样本数以减轻该影响。

* **使用 setup/teardown 函数**：*强烈*建议使用 setup 和 teardown 函数，尽可能隔离被测代码。基准测试代码中过多的 setup/teardown 代码会引入噪声，对小的关键路径*显著*地扭曲结果。


API 参考
*************

.. doxygengroup:: ztest_benchmark
