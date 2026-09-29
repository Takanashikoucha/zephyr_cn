.. _external_module_zephelin:

Zephelin
########

简介
****

`Zephyr Profiling Library`_（ZPL，简称 Zephelin）是一个库，
用于捕获和报告 Zephyr 应用的运行时性能指标，以便对应用进行
剖析和详细分析，特别关注运行 AI/ML 推理工作负载的应用。

除上述功能外，Zephelin 还简化了对 `LiteRT`_ 和 `microTVM`_
等 AI 运行时的分析，帮助更好地理解底层瓶颈或潜在的优化机会。

Zephelin 特性：

* 在硬件上跟踪 Zephyr 应用的执行
* 使用 UART、USB 或 debug adapter 等后端获取跟踪
* 以 CTF 和 TEF 格式交付跟踪
* 从设备捕获跟踪的脚本
* 收集以下读数：

  * 内存 — 栈、heap、内核 heap 和内存 slab
  * 传感器 — 例如 die 温度传感器
  * 线程分析 — CPU 使用率
  * AI 运行时 — 例如 LiteRT 中的 tensor arena 使用量

* 在 LiteRT 或 microTVM 运行时中显示已执行神经网络层的详情：

  * 输入、输出和权重的维度
  * 层参数
  * 执行特定层所花费的时间和资源

* 库的编译级和运行时级配置

* 可配置剖析层级，控制所收集的子系统和数据量

以上所有内容都可以用 `Zephelin Trace Viewer`_ 分析。

在 Zephyr 中使用
****************

要将 Zephelin 作为 Zephyr :ref:`module <modules>` 使用，
在 Zephyr 子 manifest（例如 ``zephyr/submanifests/zephelin.yaml``）
中添加以下条目，然后运行 ``west update``，或者将其作为 West 项目
添加到项目的 ``west.yaml`` manifest：

.. code-block:: yaml

   manifest:
     projects:
       - name: zephelin
         url: https://github.com/antmicro/zephelin
         revision: main
         path: modules/zephelin # adjust the path as needed

更多信息请参见 `Zephelin 文档`_。

参考资料
********

.. target-notes::

.. _Zephyr Profiling Library:
   https://github.com/antmicro/zephelin

.. _Zephelin 文档:
   https://antmicro.github.io/zephelin/

.. _Zephelin Trace Viewer:
   https://antmicro.github.io/zephelin-trace-viewer

.. _LiteRT:
   https://ai.google.dev/edge/litert

.. _microTVM:
   https://tvm.apache.org/docs/
