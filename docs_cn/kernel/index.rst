.. _kernel:

内核
####

Zephyr 内核是 Zephyr 应用的核心。它提供低开销、高性能的多线程执行环境，
并拥有丰富的可用功能。Zephyr 生态系统的其余部分——
包括设备驱动、网络栈和应用特定代码——
利用内核功能构建完整应用。

内核的可配置特性允许你仅纳入应用所需的功能，
使其非常适合内存有限的系统（低至 2 KB！）
或具有简单多线程需求的系统
（如一组中断处理程序和单个后台任务）。
此类系统的示例包括：嵌入式传感器集线器、环境传感器、
简单 LED 可穿戴设备和商店库存标签。

需要更多内存（50 到 900 KB）、多个通信设备
（如 Wi-Fi 和蓝牙低功耗）和复杂多线程的应用，
也可以使用 Zephyr 内核开发。
此类系统的示例包括：健身可穿戴设备、智能手表和物联网无线网关。

.. toctree::
   :maxdepth: 1
   :caption: 内核服务

   services/index

.. toctree::
   :maxdepth: 1
   :caption: 内存管理

   memory_management/index

.. toctree::
   :maxdepth: 1
   :caption: 数据结构

   data_structures/index

.. toctree::
   :maxdepth: 1
   :caption: 时间功能

   timing_functions/index

.. note::

   本章节为 Zephyr 内核核心文档的中文翻译。
   完整内容请参见上游英文文档 https://docs.zephyrproject.org/latest/kernel/
